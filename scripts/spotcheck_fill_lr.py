"""One-time helper: fill doublecode_sample.csv with Lizzy Ratcliff (LR) spot-check codes."""
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "analysis" / "doublecode_sample.csv"

# Order must match rows in CSV after export (40 rows). Stance: pro-Trump | anti-Trump | partisan_other | neutral_unclear | mixed
STANCE = [
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "pro-Trump",
    "neutral_unclear",
    "neutral_unclear",
    "pro-Trump",
    "neutral_unclear",
    "neutral_unclear",
    "pro-Trump",
    "partisan_other",
    "neutral_unclear",
    "pro-Trump",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "partisan_other",
    "pro-Trump",
    "pro-Trump",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "pro-Trump",
    "neutral_unclear",
    "neutral_unclear",
    "neutral_unclear",
    "pro-Trump",
    "anti-Trump",
    "pro-Trump",
    "neutral_unclear",
    "pro-Trump",
    "pro-Trump",
    "neutral_unclear",
    "pro-Trump",
    "partisan_other",
    "anti-Trump",
    "partisan_other",
]

MORAL = [
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "yes",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "yes",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "yes",
    "yes",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
    "no",
]


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    if len(df) != len(STANCE):
        raise SystemExit(f"Expected {len(STANCE)} rows, got {len(df)} — re-run export_coding_sample.py 40 first.")
    df["your_stance"] = STANCE
    df["your_moralized_yes_no"] = MORAL
    df["coder_initials"] = "LR"
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"Filled {len(df)} rows: {CSV_PATH}")


if __name__ == "__main__":
    main()
