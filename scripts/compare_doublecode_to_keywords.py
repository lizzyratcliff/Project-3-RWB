"""Compare manual double-coding in doublecode_sample.csv to keywords_v1 automated labels."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import analyze_b50 as a  # noqa: E402

CSV_PATH = REPO_ROOT / "analysis" / "doublecode_sample.csv"
OUT_PATH = REPO_ROOT / "analysis" / "doublecode_agreement_note.md"


def cohens_kappa(cat1: list[str], cat2: list[str]) -> float:
    """Cohen's kappa for two raters on the same n items (multiclass ok)."""
    n = len(cat1)
    if n == 0 or len(cat2) != n:
        return float("nan")
    po = sum(x == y for x, y in zip(cat1, cat2)) / n
    cats = set(cat1) | set(cat2)
    pe = 0.0
    for c in cats:
        p1 = sum(1 for x in cat1 if x == c) / n
        p2 = sum(1 for x in cat2 if x == c) / n
        pe += p1 * p2
    if pe >= 1 - 1e-12:
        return 0.0
    return (po - pe) / (1 - pe)


def _norm_moral(s: str) -> str:
    t = str(s).strip().lower()
    if t in ("y", "1", "true"):
        return "yes"
    if t in ("n", "0", "false"):
        return "no"
    return t


def _norm_stance(s: str) -> str:
    return str(s).strip()


def _auto_labels(texts: pd.Series) -> tuple[list[str], list[str]]:
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

    low = texts.astype(str).str.lower()
    auto_moral: list[str] = []
    auto_stance: list[str] = []
    for t in low:
        m, _ = a.moral_features(t, moral_families)
        auto_moral.append("yes" if m else "no")
        auto_stance.append(a.classify_stance(t, pro_t, pro_p, anti_t, anti_p, part))
    return auto_stance, auto_moral


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare doublecode_sample.csv to keyword automation.")
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_PATH,
        help=f"Output markdown (default: {OUT_PATH.name})",
    )
    args = parser.parse_args()
    out_md: Path = args.out

    if not CSV_PATH.exists():
        print(f"Missing {CSV_PATH} — run scripts/export_coding_sample.py first.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    for col in ("stance_coder_2", "moral_coder_2", "coder_2_initials"):
        if col not in df.columns:
            df[col] = ""

    c1_stance = df["your_stance"].fillna("").map(_norm_stance)
    c1_moral = df["your_moralized_yes_no"].fillna("").map(_norm_moral)
    c2_stance = df["stance_coder_2"].fillna("").map(_norm_stance)
    c2_moral = df["moral_coder_2"].fillna("").map(_norm_moral)

    c1_done = c1_stance.ne("") & c1_moral.ne("")
    if not c1_done.any():
        print("No manual codes yet — fill `your_stance` and `your_moralized_yes_no` (coder 1).", file=sys.stderr)
        sys.exit(1)

    texts = df["comment_text"]
    auto_stance, auto_moral = _auto_labels(texts)
    df["auto_stance"] = auto_stance
    df["auto_moralized"] = auto_moral

    id1_series = df.loc[c1_done, "coder_initials"].fillna("").astype(str).str.strip()
    id1 = id1_series[id1_series.ne("")].iloc[0] if id1_series.ne("").any() else "coder_1"

    stance_agree_1 = (c1_stance == df["auto_stance"])[c1_done].mean() * 100
    moral_agree_1 = (c1_moral == df["auto_moralized"])[c1_done].mean() * 100

    c2_done = c2_stance.ne("") & c2_moral.ne("")
    both = c1_done & c2_done
    n_both = int(both.sum())

    lines: list[str] = [
        "# Double-coding vs keyword automation (RWB)\n",
        f"- **Coder 1:** {id1} (column `your_stance`)\n",
        f"- **N coded (coder 1):** {int(c1_done.sum())} / {len(df)}\n",
        f"- **Stance agreement (coder 1 vs automation, exact):** {stance_agree_1:.1f}%\n",
        f"- **Moralized agreement (coder 1 vs automation):** {moral_agree_1:.1f}%\n",
    ]

    if n_both > 0:
        id2_series = df.loc[both, "coder_2_initials"].fillna("").astype(str).str.strip()
        id2 = id2_series.mode().iloc[0] if len(id2_series) else ""
        id2 = id2 or "coder_2"
        s1 = c1_stance[both].tolist()
        s2 = c2_stance[both].tolist()
        m1 = c1_moral[both].tolist()
        m2 = c2_moral[both].tolist()
        stance_ir = sum(x == y for x, y in zip(s1, s2)) / n_both * 100
        moral_ir = sum(x == y for x, y in zip(m1, m2)) / n_both * 100
        kap_s = cohens_kappa(s1, s2)
        kap_m = cohens_kappa(m1, m2)
        stance_agree_2 = (c2_stance == df["auto_stance"])[c2_done].mean() * 100
        moral_agree_2 = (c2_moral == df["auto_moralized"])[c2_done].mean() * 100
        lines.extend(
            [
                f"- **Coder 2:** {id2} (column `stance_coder_2`)\n",
                f"- **N coded (coder 2):** {int(c2_done.sum())} / {len(df)}\n",
                f"- **N rows coded by both:** {n_both}\n",
                f"- **Inter-rater stance agreement (exact):** {stance_ir:.1f}% (Cohen's kappa = {kap_s:.3f})\n",
                f"- **Inter-rater moralized agreement:** {moral_ir:.1f}% (Cohen's kappa = {kap_m:.3f})\n",
                f"- **Stance agreement (coder 2 vs automation, exact):** {stance_agree_2:.1f}%\n",
                f"- **Moralized agreement (coder 2 vs automation):** {moral_agree_2:.1f}%\n",
            ]
        )
    else:
        lines.append(
            "- **Coder 2:** _(empty — add `stance_coder_2` / `moral_coder_2` for inter-rater stats)_\n"
        )

    lines.extend(
        [
            "\nDisagreements with automation are expected where sarcasm, emojis-only comments, or context "
            "outside the dictionaries matter. Refine `keywords_v1.txt` if many systematic misses occur, "
            "then re-run `scripts/analyze_b50.py`.\n\n",
            "## Rows where stance differs (coder 1 vs automation)\n\n",
        ]
    )
    diff1 = df[c1_done & (c1_stance != df["auto_stance"])].copy()
    if len(diff1) == 0:
        lines.append("_None (among rows coded by coder 1)._ \n")
    else:
        for _, r in diff1.iterrows():
            idx = int(r.name)  # type: ignore[arg-type]
            lines.append(
                f"- **CSV row {idx + 2}** (sample index {idx + 1}, {r['platform']}) — manual: `{c1_stance.loc[r.name]}` / moral `{c1_moral.loc[r.name]}` "
                f"vs auto: `{r['auto_stance']}` / moral `{r['auto_moralized']}`\n"
            )

    lines.append("\n## Rows where moralized differs (coder 1 vs automation)\n\n")
    diffm = df[c1_done & (c1_moral != df["auto_moralized"])].copy()
    if len(diffm) == 0:
        lines.append("_None (among rows coded by coder 1)._ \n")
    else:
        for _, r in diffm.iterrows():
            idx = int(r.name)  # type: ignore[arg-type]
            lines.append(
                f"- **CSV row {idx + 2}** (sample index {idx + 1}, {r['platform']}) — manual moral `{c1_moral.loc[r.name]}` vs auto `{r['auto_moralized']}` "
                f"(stance manual `{c1_stance.loc[r.name]}` vs auto `{r['auto_stance']}`)\n"
            )

    if n_both > 0:
        lines.append("\n## Rows where stance differs between coders (inter-rater)\n\n")
        diff_ir = df[both & (c1_stance != c2_stance)].copy()
        if len(diff_ir) == 0:
            lines.append("_None._\n")
        else:
            for _, r in diff_ir.iterrows():
                idx = int(r.name)  # type: ignore[arg-type]
                lines.append(
                    f"- **CSV row {idx + 2}** ({r['platform']}) — coder1 `{c1_stance.loc[r.name]}` vs "
                    f"coder2 `{c2_stance.loc[r.name]}` (auto `{r['auto_stance']}`)\n"
                )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(lines), encoding="utf-8")
    print(f"Stance (c1 vs auto): {stance_agree_1:.1f}%  Moral (c1 vs auto): {moral_agree_1:.1f}%")
    if n_both > 0:
        print(
            f"Inter-rater stance: {stance_ir:.1f}% (kappa={kap_s:.3f})  "
            f"moral: {moral_ir:.1f}% (kappa={kap_m:.3f})"
        )
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
