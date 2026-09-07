"""Require retained SBOM and provenance statements in an OCI artifact copy."""

import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
predicates = set()
for blob in (root / "blobs" / "sha256").iterdir():
    try:
        document = json.loads(blob.read_bytes())
    except (ValueError, UnicodeDecodeError):
        continue
    if isinstance(document, dict) and "predicateType" in document:
        predicates.add(document["predicateType"])
assert "https://spdx.dev/Document" in predicates, predicates
assert any(value.startswith("https://slsa.dev/provenance/") for value in predicates), predicates
print("OCI copy preserves both SBOM and provenance")
