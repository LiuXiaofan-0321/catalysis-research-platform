from __future__ import annotations

import sys
from pathlib import Path


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = RESEARCH_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from catalysis_research.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
