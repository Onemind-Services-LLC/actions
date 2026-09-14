import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "actions/install-apt-packages/install_apt_packages.sh"


class AptPackageTests(unittest.TestCase):
    def run_installer(self, packages, update_status=0):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "calls.jsonl"
            sudo = root / "sudo"
            sudo.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "args = sys.argv[1:]\n"
                "with open(os.environ['APT_TEST_LOG'], 'a') as output:\n"
                "    output.write(json.dumps(args) + '\\n')\n"
                "if args[0] == 'apt-get' and 'update' in args:\n"
                "    sys.exit(int(os.environ['APT_TEST_UPDATE_STATUS']))\n"
            )
            sudo.chmod(0o755)
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                env={
                    **os.environ,
                    "PATH": str(root) + os.pathsep + os.environ["PATH"],
                    "APT_PACKAGES": packages,
                    "APT_TEST_LOG": str(log),
                    "APT_TEST_UPDATE_STATUS": str(update_status),
                },
                capture_output=True,
                text=True,
            )
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, calls

    def test_installs_multiple_packages_and_version_pins(self):
        result, calls = self.run_installer("shellcheck\nskopeo:amd64=1.13.3+ds1-1build2")
        self.assertEqual(result.returncode, 0, result.stderr)
        apt_calls = [call for call in calls if call[0] == "apt-get"]
        self.assertEqual(len(apt_calls), 2)
        self.assertIn("update", apt_calls[0])
        install = apt_calls[1]
        self.assertEqual(install[install.index("--") + 1:], ["shellcheck", "skopeo:amd64=1.13.3+ds1-1build2"])

    def test_failed_index_refresh_prevents_installation(self):
        result, calls = self.run_installer("skopeo", update_status=23)
        self.assertEqual(result.returncode, 23)
        self.assertFalse(any(call[0] == "apt-get" and "install" in call for call in calls))

    def test_rejects_empty_lists_and_options_before_mutation(self):
        for packages in ("", "  \n\t", "--allow-unauthenticated skopeo", "skopeo;true"):
            with self.subTest(packages=packages):
                result, calls = self.run_installer(packages)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])
