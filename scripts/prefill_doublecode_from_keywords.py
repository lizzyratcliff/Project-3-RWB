"""
Fill `analysis/doublecode_sample.csv` with keyword-automation labels for both coders.

Use only for **pipeline testing** or as a **baseline**. Plan §3 expects **two independent
human** coders; replace AUTO labels before treating validation as final.

Usage (after `export_coding_sample.py`):
  python scripts/prefill_doublecode_from_keywords.py
"""

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
CSV_PATH = REPO_ROOT / "analysis" / "doublecode_sample.csv"
sys.path.insert(0, str(SCRIPTS))

from compare_doublecode_to_keywords import _auto_labels  # noqa: E402


def main() -> None:
    if not CSV_PATH.exists():
        print(f"Missing {CSV_PATH} — run scripts/export_coding_sample.py first.", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(CSV_PATH)
    stances, morals = _auto_labels(df["comment_text"])
    df["your_stance"] = stances
    df["your_moralized_yes_no"] = morals
    df["coder_initials"] = "AUTO"
    df["stance_coder_2"] = stances
    df["moral_coder_2"] = morals
    df["coder_2_initials"] = "AUTO"
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"Prefilled {len(df)} rows with keyword automation (both coders = AUTO).")


if __name__ == "__main__":
    main()
