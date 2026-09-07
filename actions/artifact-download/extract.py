"""Extract the verified ZIP files while retaining the downloader's directory layout."""

import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile


def extract_artifacts(staging, destination):
    if any(character in str(destination) for character in "\r\n"):
        raise ValueError("Artifact destination must be a single line")
    staging = Path(staging).resolve()
    destination = Path(destination).expanduser().resolve()
    archives = sorted(path for path in staging.rglob("*") if path.is_file())
    destination.mkdir(parents=True, exist_ok=True)
    for archive in archives:
        if archive.is_symlink() or not zipfile.is_zipfile(archive):
            raise ValueError("Expected a ZIP artifact produced by artifact-upload")
        target = destination / archive.parent.relative_to(staging)
        with zipfile.ZipFile(archive) as source:
            # Validate every member before writing any member of this archive.
            members = []
            for member in source.infolist():
                name = PurePosixPath(member.filename)
                if name.is_absolute() or ".." in name.parts or "\\" in member.filename:
                    raise ValueError("Unsafe artifact member path")
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise ValueError("Artifact symlinks are not supported")
                output = (target / member.filename).resolve()
                if not output.is_relative_to(destination):
                    raise ValueError("Artifact member escapes the destination")
                members.append((member, output))
            for member, output in members:
                if member.is_dir():
                    output.mkdir(parents=True, exist_ok=True)
                else:
                    output.parent.mkdir(parents=True, exist_ok=True)
                    with source.open(member) as reader, output.open("wb") as writer:
                        shutil.copyfileobj(reader, writer)
                    output.chmod(0o644)
        archive.unlink()
    return destination


if __name__ == "__main__":
    extracted = extract_artifacts(os.environ["STAGING_DIR"], os.environ["DESTINATION"])
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"download-path={extracted}\n")
