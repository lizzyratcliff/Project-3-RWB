"""
Export a random stratified sample of comments for independent double-coding (§3 validation).
Writes a CSV locally (gitignored by *.csv) — do not commit.

Usage from repo root:
  python scripts/export_coding_sample.py 80
"""

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
OUT = REPO_ROOT / "analysis" / "doublecode_sample.csv"


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    sys.path.insert(0, str(SCRIPTS_DIR))
    from analyze_b50 import load_all_comments  # noqa: PLC0415

    df = load_all_comments()
    per = max(1, n // df["platform"].nunique())
    parts = [g.sample(n=min(per, len(g)), random_state=42) for _, g in df.groupby("platform")]
    sample = pd.concat(parts, ignore_index=True)
    if len(sample) < n:
        remaining = df.loc[~df.index.isin(sample.index)]
        need = min(n - len(sample), len(remaining))
        if need > 0:
            sample = pd.concat(
                [sample, remaining.sample(n=need, random_state=43)], ignore_index=True
            )
    sample = sample.sample(n=min(n, len(sample)), random_state=44).reset_index(drop=True)
    out = sample[["platform", "comment_text", "likes"]].copy()
    out["your_stance"] = ""
    out["your_moralized_yes_no"] = ""
    out["coder_initials"] = ""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Wrote {len(out)} rows to {OUT} (keep local; do not commit)")


if __name__ == "__main__":
    main()
