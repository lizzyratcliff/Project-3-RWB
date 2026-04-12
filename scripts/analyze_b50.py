"""
B50 exploratory analysis for RWB (KIN 7518 P3).
Loads local Excel files (not in git), merges platforms, applies keywords_v1 rules,
writes aggregate summary to analysis/results_summary.md.

Usage (from repo root):
  python scripts/analyze_b50.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYWORDS_FILE = REPO_ROOT / "keywords_v1.txt"
OUTPUT_MD = REPO_ROOT / "analysis" / "results_summary.md"


def _df_to_md(table: pd.DataFrame | pd.Series) -> str:
    if isinstance(table, pd.Series):
        table = table.to_frame()
    try:
        return table.to_markdown()
    except ImportError:
        return "```\n" + table.to_string() + "\n```"


def load_keyword_sections(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if line.startswith("#"):
            continue
        if current is not None:
            sections[current].append(line.lower())
    return sections


def compile_family_patterns(tokens: list[str]) -> list[re.Pattern]:
    pats = []
    for t in tokens:
        if not t:
            continue
        esc = re.escape(t)
        pats.append(re.compile(rf"(?<!\w){esc}(?!\w)", re.IGNORECASE))
    return pats


def compile_phrase_patterns(phrases: list[str]) -> list[re.Pattern]:
    pats = []
    for p in phrases:
        if not p:
            continue
        pats.append(re.compile(re.escape(p), re.IGNORECASE))
    return pats


def any_match(text: str, patterns: list[re.Pattern]) -> bool:
    return any(p.search(text) for p in patterns)


def moral_features(text: str, families: dict[str, list[re.Pattern]]) -> tuple[bool, int]:
    hits = []
    for name, pats in families.items():
        hits.append(any_match(text, pats))
    intensity = sum(hits)
    return intensity > 0, intensity


def classify_stance(
    text: str,
    pro_tok: list[re.Pattern],
    pro_phr: list[re.Pattern],
    anti_tok: list[re.Pattern],
    anti_phr: list[re.Pattern],
    part_tok: list[re.Pattern],
) -> str:
    pro = any_match(text, pro_tok) or any_match(text, pro_phr)
    anti = any_match(text, anti_tok) or any_match(text, anti_phr)
    if pro and anti:
        return "mixed"
    if pro:
        return "pro-Trump"
    if anti:
        return "anti-Trump"
    if any_match(text, part_tok):
        return "partisan_other"
    return "neutral_unclear"


def load_all_comments() -> pd.DataFrame:
    frames = []
    triples = [
        ("Instagram", REPO_ROOT / "dataset" / "B50_INS_COMMENT.xlsx", "text"),
        ("X", REPO_ROOT / "dataset" / "B50_X_COMMENT.xlsx", "contents"),
        ("YouTube", REPO_ROOT / "dataset" / "B50_YT_COMMENT.xlsx", "text"),
    ]
    for platform, path, col in triples:
        if not path.exists():
            print(f"Missing file: {path}", file=sys.stderr)
            sys.exit(1)
        df = pd.read_excel(path)
        if col not in df.columns:
            print(f"Column {col!r} not in {path.name}; have {list(df.columns)}", file=sys.stderr)
            sys.exit(1)
        sub = df.copy()
        sub["platform"] = platform
        sub["comment_text"] = sub[col].astype(str).fillna("")
        sub["likes"] = pd.to_numeric(sub.get("likes"), errors="coerce").fillna(0)
        if platform == "X":
            sub["retweets"] = pd.to_numeric(
                sub.get("retweets count", sub.get("retweets_count")), errors="coerce"
            ).fillna(0)
            sub["replies"] = pd.to_numeric(
                sub.get("reply counts", sub.get("reply_counts")), errors="coerce"
            ).fillna(0)
            sub["followers"] = pd.to_numeric(sub.get("followers"), errors="coerce")
            bv = sub.get("blue_verified")
            if bv is not None:
                sub["blue_verified"] = bv.apply(
                    lambda x: bool(x) if isinstance(x, (bool, np.bool_)) else str(x).lower() in ("1", "true", "yes")
                )
            else:
                sub["blue_verified"] = False
        else:
            sub["retweets"] = np.nan
            sub["replies"] = np.nan
            sub["followers"] = np.nan
            sub["blue_verified"] = np.nan
        frames.append(sub)
    out = pd.concat(frames, ignore_index=True)
    return out


def main() -> None:
    if not KEYWORDS_FILE.exists():
        print(f"Missing {KEYWORDS_FILE}", file=sys.stderr)
        sys.exit(1)

    sec = load_keyword_sections(KEYWORDS_FILE)

    moral_families = {
        "virtue_vice": compile_family_patterns(sec.get("MORAL_VIRTUE_VICE", [])),
        "harm": compile_family_patterns(sec.get("MORAL_HARM", [])),
        "fairness": compile_family_patterns(sec.get("MORAL_FAIRNESS", [])),
        "loyalty": compile_family_patterns(sec.get("MORAL_LOYALTY", [])),
    }

    pro_tok = compile_family_patterns(sec.get("STANCE_PRO_TOKEN", []))
    pro_phr = compile_phrase_patterns(sec.get("STANCE_PRO_PHRASE", []))
    anti_tok = compile_family_patterns(sec.get("STANCE_ANTI_TOKEN", []))
    anti_phr = compile_phrase_patterns(sec.get("STANCE_ANTI_PHRASE", []))
    part_tok = compile_family_patterns(sec.get("STANCE_PARTISAN_TOKEN", []))

    df = load_all_comments()
    texts = df["comment_text"].str.lower()

    moral_rows = [moral_features(t, moral_families) for t in texts]
    df["moralized"] = [m[0] for m in moral_rows]
    df["moral_intensity"] = [m[1] for m in moral_rows]

    df["stance"] = [
        classify_stance(t, pro_tok, pro_phr, anti_tok, anti_phr, part_tok) for t in texts
    ]

    lines: list[str] = []
    lines.append("# B50 analysis — aggregate summary (RWB)\n")
    lines.append("Generated by `scripts/analyze_b50.py` using `keywords_v1.txt`. ")
    lines.append("No raw comment text is stored here.\n")

    lines.append("## Row counts by platform\n")
    lines.append(_df_to_md(df["platform"].value_counts()))
    lines.append("\n")

    lines.append("## % moralized by platform\n")
    g = df.groupby("platform")["moralized"].agg(["mean", "sum", "count"])
    g["pct_moralized"] = (g["mean"] * 100).round(2)
    lines.append(_df_to_md(g[["count", "sum", "pct_moralized"]]))
    lines.append("\n")

    lines.append("## Stance distribution by platform (row % within platform)\n")
    ct = pd.crosstab(df["platform"], df["stance"], normalize="index") * 100
    lines.append(_df_to_md(ct.round(2)))
    lines.append("\n")

    lines.append("## Median / mean likes by platform\n")
    eng = df.groupby("platform")["likes"].agg(["median", "mean", "count"]).round(2)
    lines.append(_df_to_md(eng))
    lines.append("\n")

    lines.append("## Median likes: moralized vs not (within platform)\n")
    for plat in df["platform"].unique():
        sub = df[df["platform"] == plat]
        lines.append(f"### {plat}\n")
        t = sub.groupby("moralized")["likes"].agg(["median", "mean", "count"]).round(2)
        lines.append(_df_to_md(t))
        lines.append("\n")

    lines.append("## Median likes by stance (within platform)\n")
    for plat in df["platform"].unique():
        sub = df[df["platform"] == plat]
        lines.append(f"### {plat}\n")
        t = sub.groupby("stance")["likes"].agg(["median", "mean", "count"]).round(2)
        lines.append(_df_to_md(t))
        lines.append("\n")

    xdf = df[df["platform"] == "X"].copy()
    if len(xdf) > 0:
        lines.append("## X only: median engagement\n")
        lines.append(_df_to_md(xdf[["likes", "retweets", "replies"]].agg(["median", "mean"]).round(2)))
        lines.append("\n")

        lines.append("## X only: % moralized by blue_verified\n")
        if xdf["blue_verified"].notna().any():
            mv = xdf.groupby("blue_verified")["moralized"].agg(["mean", "count"])
            mv["pct_moralized"] = (mv["mean"] * 100).round(2)
            lines.append(_df_to_md(mv[["count", "pct_moralized"]]))
            lines.append("\n")

        lines.append("## X only: stance % by blue_verified\n")
        if xdf["blue_verified"].notna().any():
            ct2 = pd.crosstab(xdf["blue_verified"], xdf["stance"], normalize="index") * 100
            lines.append(_df_to_md(ct2.round(2)))
            lines.append("\n")

        fx = xdf["followers"].dropna()
        if len(fx) > 5:
            try:
                xdf["follower_tertile"] = pd.qcut(
                    xdf["followers"], q=3, labels=["low", "mid", "high"], duplicates="drop"
                )
                lines.append("## X only: % moralized by follower tertile\n")
                mt = xdf.groupby("follower_tertile", observed=True)["moralized"].agg(["mean", "count"])
                mt["pct_moralized"] = (mt["mean"] * 100).round(2)
                lines.append(_df_to_md(mt[["count", "pct_moralized"]]))
                lines.append("\n")
            except ValueError:
                lines.append("## X follower tertiles: skipped (insufficient variation)\n\n")

    # Chi-square: stance vs platform (all non-neutral could collapse - use full table)
    try:
        from scipy.stats import chi2_contingency

        tab = pd.crosstab(df["platform"], df["stance"])
        chi2, p, dof, _ = chi2_contingency(tab)
        lines.append("## Chi-square: platform × stance\n")
        lines.append(f"- chi² = {chi2:.2f}, df = {dof}, p = {p:.4g}\n")
        lines.append("(Interpret cautiously: large N inflates chi²; expected counts should be checked.)\n\n")
    except ImportError:
        lines.append("## Chi-square: install scipy (`pip install scipy`) for platform × stance test\n\n")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
