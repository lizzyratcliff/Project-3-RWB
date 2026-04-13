"""
Build KIN 7518 group deck from Template_Presentation_Outline structure + RWB project content.

Usage (repo root):
  python scripts/build_rwb_presentation.py

Output: RWB_KIN7518_Presentation.pptx
Requires: python-pptx
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "RWB_KIN7518_Presentation.pptx"
VISUAL = REPO / "RWB_VISUAL.png"


def _bullet_slide(prs: Presentation, title: str, lines: list[str], subtitle: str | None = None) -> None:
    layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = title
    if subtitle and len(slide.placeholders) > 0:
        pass # layout 1 has no subtitle placeholder on all themes
    body = slide.placeholders[1].text_frame
    body.clear()
    for i, line in enumerate(lines):
        if i == 0:
            p = body.paragraphs[0]
        else:
            p = body.add_paragraph()
        p.text = line
        p.level = 0
        p.font.size = Pt(20)
    slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(32)


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Slide 1: Title ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = (
        "Conflict, Morality & Polarization\nin Sport–Politics Social Comments (B50)"
    )
    sub = slide.placeholders[1]
    sub.text = (
        "Group RWB — KIN 7518 (Social Issues in Sport)\n"
        "Elizabeth Ratcliff · Jardyn Washington · Isabelle Besselman\n"
        "April 13, 2026"
    )
    slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(36)
    for p in sub.text_frame.paragraphs:
        p.font.size = Pt(18)

    # --- Slide 2: Social issue context (~3 min) ---
    _bullet_slide(
        prs,
        "Social issue context & framing",
        [
            "The problem: When sport and politics overlap online, comment sections become sites of moral "
            "outrage (virtue/vice, harm, betrayal) and partisan sorting — not just “sports talk.”",
            "Context: B50 captures audience comments on hybrid sport–politics crossover content with "
            "substantial Trump-related political talk (golf/sports crossover, public-figure media).",
            "Research question: How do moralized discourse and polarization cues differ across Instagram, "
            "X, and YouTube — and how do those categories relate to visible engagement (likes; plus X "
            "retweets/replies) within each platform? (Descriptive, not causal.)",
        ],
    )

    # --- Slide 3: Data & scope (~1 min) ---
    _bullet_slide(
        prs,
        "Data & scope",
        [
            "Dataset: Class corpus “B50” — merged public comments from Instagram, X, and YouTube exports.",
            "Size: 58,464 comments total — YouTube 45,623; Instagram 11,833; X 1,008.",
            "Scope: Same topical scrape (sport–politics crossover; heavy Trump-related audience talk) "
            "across platforms so cross-platform comparisons are meaningful.",
            "Why this data: Lets us describe how conflict/morality/polarization show up where sport and "
            "politics meet — and whether platform context matters.",
        ],
    )

    # --- Slide 4: Analytical strategy (~2 min) ---
    _bullet_slide(
        prs,
        "Analytical strategy",
        [
            "Key concepts: (1) Moralized = binary flag if text hits ≥1 of four keyword families "
            "(virtue/vice, harm/care, fairness/cheating, loyalty/betrayal). "
            "(2) Stance = pro-Trump, anti-Trump, partisan_other, neutral_unclear, or mixed — from "
            "transparent phrase/token lists (conservative; many real stances stay “neutral_unclear”).",
            "Method: Automated keyword classification + descriptive tables; χ² for platform × stance "
            "with Cramér’s V; Spearman ρ for moralized vs log(1+likes) within platform; Wilson CIs on X.",
            "Validation: Frozen dictionaries (keywords_v1.txt); manual double-coding spot-check "
            "(e.g., N=40: stance agreement vs automation ~57.5%; moralized ~87.5%) — see project notes.",
        ],
    )

    # --- Slide 5: Key findings + visual (~2 min) ---
    layout_blank = prs.slide_layouts[6]  # Blank (Office theme index may vary)
    try:
        s5 = prs.slides.add_slide(layout_blank)
    except Exception:
        s5 = prs.slides.add_slide(prs.slide_layouts[5])

    tx = s5.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(8.8), Inches(0.9))
    tx.text_frame.text = "Key findings"
    tx.text_frame.paragraphs[0].font.size = Pt(32)
    tx.text_frame.paragraphs[0].font.bold = True

    body = s5.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(6.2), Inches(5.8))
    tf = body.text_frame
    tf.word_wrap = True
    bullets = [
        "Volume: YouTube dominates raw N; X is small — we emphasize within-platform percentages.",
        "Moralized % (within platform): Instagram ~2.4%; X ~5.1%; YouTube ~5.6%.",
        "Polarization cues (dictionary-defined stance): Most rows are neutral_unclear; YouTube shows the "
        "largest pro-Trump share (~10.5% of YT comments) vs Instagram (~2.8%) and X (~5.8%). "
        "Association of platform x stance is statistically detectable but modest (Cramer's V ~ 0.09).",
        "Engagement (descriptive): On X, pro-Trump-tagged comments show much higher mean likes than other "
        "stance buckets — timing/humor/controversy matter; this is not proof of “agreement.”",
    ]
    for i, b in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(17)
        p.space_after = Pt(10)

    if VISUAL.exists():
        s5.shapes.add_picture(str(VISUAL), Inches(7.0), Inches(1.15), width=Inches(5.9))
    else:
        note = s5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.5), Inches(1.0))
        note.text_frame.text = "(Add RWB_VISUAL.png — file missing from repo path)"

    # --- Slide 6: Interpretation & implications (~2 min) ---
    _bullet_slide(
        prs,
        "Interpretation & implications",
        [
            "So what: Hybrid sport–politics content pulls audiences into moral and partisan language; "
            "the mix differs by platform norms and who shows up — YouTube’s thread in this scrape carries "
            "more dictionary-visible pro-Trump cues than Instagram, with X in between on several metrics.",
            "For sport organizations & communicators: Expect political spillover in comments; plan moderation, "
            "community guidelines, and framing with eyes open to polarization — not only “game talk.”",
            "Ethics & limits: Keyword methods miss sarcasm/implicit opinion; B50 is not representative of "
            "all voters or all platforms; we report language patterns in this corpus, not “truth” of claims.",
        ],
    )

    # --- Slide 7: Q&A (template “Slide 9”) ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Thank you"
    slide.placeholders[1].text = "Questions?\n\nRepo: github.com/lizzyratcliff/Project-3-RWB"
    slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(44)

    prs.save(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
