"""Compare LR manual codes in doublecode_sample.csv to keywords_v1 automated labels."""
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import analyze_b50 as a  # noqa: E402

CSV_PATH = REPO_ROOT / "analysis" / "doublecode_sample.csv"
OUT_PATH = REPO_ROOT / "analysis" / "doublecode_agreement_note.md"


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    if df["coder_initials"].isna().all():
        print("No manual codes yet — run spotcheck_fill_lr.py after export.")
        sys.exit(1)

    sec = a.load_keyword_sections(a.KEYWORDS_FILE)
    moral_families = {
        "virtue_vice": a.compile_family_patterns(sec.get("MORAL_VIRTUE_VICE", [])),
        "harm": a.compile_family_patterns(sec.get("MORAL_HARM", [])),
        "fairness": a.compile_family_patterns(sec.get("MORAL_FAIRNESS", [])),
        "loyalty": a.compile_family_patterns(sec.get("MORAL_LOYALTY", [])),
    }
    pro_t = a.compile_family_patterns(sec.get("STANCE_PRO_TOKEN", []))
    pro_p = a.compile_phrase_patterns(sec.get("STANCE_PRO_PHRASE", []))
    anti_t = a.compile_family_patterns(sec.get("STANCE_ANTI_TOKEN", []))
    anti_p = a.compile_phrase_patterns(sec.get("STANCE_ANTI_PHRASE", []))
    part = a.compile_family_patterns(sec.get("STANCE_PARTISAN_TOKEN", []))

    texts = df["comment_text"].astype(str).str.lower()
    auto_moral = []
    auto_stance = []
    for t in texts:
        m, _ = a.moral_features(t, moral_families)
        auto_moral.append("yes" if m else "no")
        auto_stance.append(a.classify_stance(t, pro_t, pro_p, anti_t, anti_p, part))

    df["auto_stance"] = auto_stance
    df["auto_moralized"] = auto_moral

    stance_agree = (df["your_stance"] == df["auto_stance"]).mean() * 100
    moral_agree = (df["your_moralized_yes_no"] == df["auto_moralized"]).mean() * 100

    lines = [
        "# Double-coding vs keyword automation (RWB)\n",
        f"- **Coder:** {df['coder_initials'].iloc[0]} (manual spot-check)\n",
        f"- **N:** {len(df)}\n",
        f"- **Stance agreement (exact):** {stance_agree:.1f}%\n",
        f"- **Moralized agreement (yes/no):** {moral_agree:.1f}%\n",
        "\nDisagreements are expected where sarcasm, emojis-only comments, or context ",
        "outside the dictionaries matter. Use this to refine `keywords_v1.txt`.\n\n",
        "## Rows where stance differs\n\n",
    ]
    diff = df[df["your_stance"] != df["auto_stance"]]
    if len(diff) == 0:
        lines.append("_None._\n")
    else:
        for idx, r in diff.iterrows():
            row_num = int(idx) + 1  # 1-based row within the 40-comment sample
            lines.append(
                f"- **Sample row {row_num}** ({r['platform']}) — manual: `{r['your_stance']}` / moral `{r['your_moralized_yes_no']}` "
                f"vs auto: `{r['auto_stance']}` / moral `{r['auto_moralized']}`\n"
            )

    OUT_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Stance agree: {stance_agree:.1f}%  Moral agree: {moral_agree:.1f}%")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
