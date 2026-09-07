import importlib.util
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile


SOURCE = Path(__file__).resolve().parents[1] / "actions/artifact-download/extract.py"
SPEC = importlib.util.spec_from_file_location("artifact_extract", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ArtifactDownloadTests(unittest.TestCase):
    def test_single_and_multiple_artifacts_preserve_bytes_and_layout(self):
        for directories in [("",), ("image-a", "image-b")]:
            with self.subTest(directories=directories), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name in directories:
                    archive = root / "staging" / name / "artifact.zip"
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(archive, "w") as output:
                        output.writestr("image.tar", b"\x00OCI archive\xff")
                        output.writestr("nested/image.json", '{"digest":"fixture"}\n')
                MODULE.extract_artifacts(root / "staging", root / "output")
                for name in directories:
                    self.assertEqual((root / "output" / name / "image.tar").read_bytes(), b"\x00OCI archive\xff")
                    self.assertEqual((root / "output" / name / "nested/image.json").read_text(), '{"digest":"fixture"}\n')
                self.assertFalse(list((root / "staging").rglob("*.zip")))

    def test_unsafe_members_fail_before_any_member_is_written(self):
        for name in ("../escape", "/absolute", "nested/../../escape", "..\\escape", "symlink"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "staging").mkdir()
                with zipfile.ZipFile(root / "staging/artifact.zip", "w") as output:
                    output.writestr("valid.txt", "must not be written")
                    member = zipfile.ZipInfo(name)
                    if name == "symlink":
                        member.external_attr = (stat.S_IFLNK | 0o777) << 16
                    output.writestr(member, "../escape")
                with self.assertRaises(ValueError):
                    MODULE.extract_artifacts(root / "staging", root / "output")
                self.assertFalse(list((root / "output").rglob("*")))

    def test_existing_destination_symlink_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("staging", "output", "outside"):
                (root / name).mkdir()
            (root / "output/nested").symlink_to(root / "outside", target_is_directory=True)
            with zipfile.ZipFile(root / "staging/artifact.zip", "w") as output:
                output.writestr("nested/escape", "unsafe")
            with self.assertRaises(ValueError):
                MODULE.extract_artifacts(root / "staging", root / "output")
            self.assertFalse(list((root / "outside").iterdir()))
