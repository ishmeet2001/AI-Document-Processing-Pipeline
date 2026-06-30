import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "unstructured-data-pipeline"

for path in (SRC_ROOT, PACKAGE_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


if __name__ == "__main__":
    sys.exit(pytest.main(["-q", "tests"]))
