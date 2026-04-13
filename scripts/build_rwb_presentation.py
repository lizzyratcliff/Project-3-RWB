"""
Build KIN 7518 group deck: outline structure + RWB content, RQ1 & RQ2, colors, speaker notes.

Usage (repo root):
  python scripts/build_rwb_presentation.py

Output: RWB_KIN7518_Presentation.pptx
Requires: python-pptx
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "RWB_KIN7518_Presentation.pptx"
VISUAL = REPO / "RWB_VISUAL.png"

# --- Theme (high-contrast, presentation-friendly) ---
NAVY = RGBColor(15, 30, 75)
INDIGO = RGBColor(67, 56, 202)
TEAL = RGBColor(13, 148, 136)
CORAL = RGBColor(225, 85, 84)
GOLD = RGBColor(217, 119, 6)
CREAM = RGBColor(255, 251, 240)
SKY = RGBColor(238, 246, 255)
WHITE = RGBColor(255, 255, 255)
CHARCOAL = RGBColor(40, 44, 52)
TITLE_SLIDE_BG = RGBColor(30, 58, 138)
QNA_BG = RGBColor(49, 46, 129)


def _rgb(fill, color: RGBColor) -> None:
    fill.solid()
    fill.fore_color.rgb = color


def _slide_bg(slide, color: RGBColor) -> None:
    _rgb(slide.background.fill, color)


def _left_accent(slide, prs: Presentation, color: RGBColor, width_in: float = 0.14) -> None:
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        Inches(width_in),
        prs.slide_height,
    )
    _rgb(bar.fill, color)
    bar.line.fill.background()


def _notes(slide, text: str) -> None:
    ns = slide.notes_slide
    ns.notes_text_frame.text = text.strip()


def _style_title(tf, size_pt: int, color: RGBColor, bold: bool = True) -> None:
    for p in tf.paragraphs:
        p.font.size = Pt(size_pt)
        p.font.bold = bold
        p.font.color.rgb = color


def _bullet_slide(
    prs: Presentation,
    title: str,
    lines: list[str],
    *,
    bg: RGBColor,
    accent: RGBColor,
    title_color: RGBColor,
    body_color: RGBColor,
    body_size: int = 20,
    notes: str,
) -> None:
    layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(layout)
    _slide_bg(slide, bg)
    _left_accent(slide, prs, accent)

    slide.shapes.title.text = title
    _style_title(slide.shapes.title.text_frame, 32, title_color)

    body = slide.placeholders[1].text_frame
    body.clear()
    body.word_wrap = True
    for i, line in enumerate(lines):
        p = body.paragraphs[0] if i == 0 else body.add_paragraph()
        p.text = line
        p.level = 0
        p.font.size = Pt(body_size)
        p.font.color.rgb = body_color
        p.space_after = Pt(8)

    _notes(slide, notes)


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Slide 1: Title ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    _slide_bg(slide, TITLE_SLIDE_BG)
    slide.shapes.title.text = (
        "Conflict, Morality & Polarization\nin Sport–Politics Social Comments (B50)"
    )
    sub = slide.placeholders[1]
    sub.text = (
        "Group RWB — KIN 7518 (Social Issues in Sport)\n"
        "Elizabeth Ratcliff · Jardyn Washington · Isabelle Besselman\n"
        "April 13, 2026"
    )
    _style_title(slide.shapes.title.text_frame, 36, WHITE)
    for p in sub.text_frame.paragraphs:
        p.font.size = Pt(19)
        p.font.color.rgb = RGBColor(226, 232, 240)
    _notes(
        slide,
        """
 Welcome everyone. We are Group RWB. This project is for KIN 7518 — we studied online comments on posts where sports and politics overlap, especially around content that also draws a lot of discussion of Donald Trump.

        In plain terms: when a golf clip or athlete story sits next to political talk, the comment section is not “only sports.” People use moral language — who is corrupt, who deserves respect, who is dangerous — and they sort into camps. We are not here to judge voters. We measured patterns in language so we can describe what shows up and how it differs across Instagram, X, and YouTube.

        You will hear two research questions. The first is our main question across all three platforms. The second zooms in on X because that file tells us whether an account had a blue check and roughly how many followers they had — so we can ask whether “who is commenting” relates to engagement and to our topic codes. Everything is descriptive: we are not claiming we proved why anything happened.
        """,
    )

    # --- Slide 2: Context + BOTH RQs ---
    _bullet_slide(
        prs,
        "Why this matters & our research questions",
        [
            "Social issue: Sport–politics crossover posts pull audiences into moral outrage and partisan cues — not just game talk.",
            "Context: Corpus B50 = comments on hybrid sport/politics media with substantial Trump-related audience discussion.",
            "RQ 1 (primary): How do moralized discourse & polarization cues differ across Instagram, X, and YouTube — and how do those labels line up with likes (and on X, retweets/replies)? Descriptive only.",
            "RQ 2 (X only): Among X comments, are blue-verified status or follower level tied to (a) engagement and (b) a higher share of moralized or stance-coded comments? Exploratory — X is our smallest slice (n=1,008).",
        ],
        bg=CREAM,
        accent=TEAL,
        title_color=TEAL,
        body_color=CHARCOAL,
        body_size=19,
        notes="""
        Start with the social problem in everyday language. When sports and politics meet online — think a headline that mixes an athlete, a politician, and a heated audience — comments often sound like mini-debates about good and evil, betrayal, fairness, and “us versus them.” That matters for media literacy, for how leagues and teams manage their channels, and for how toxic or civil a thread feels.

        Our data are a class corpus called B50: the same topical conversation scraped across three platforms. That lets us compare apples to apples in topic, not apples to oranges.

        Research Question 1 is the big picture: do the rates of “moralized” language and dictionary-defined political stance tags differ by platform, and within each site, do those tags travel together with visible engagement? We treat likes and shares as clues people noticed a comment — not proof everyone agreed with it.

        Research Question 2 is optional on the syllabus but we include it because X’s export has extra columns: verified badge and follower counts. We ask, in this small X sample, whether verified or high-follower accounts look different on engagement or on our topic codes. We will stress that X has only about a thousand comments here, so we frame RQ2 as exploratory and we use uncertainty intervals where we report percentages.
        """,
    )

    # --- Slide 3: Data & scope ---
    _bullet_slide(
        prs,
        "Data & scope",
        [
            "Dataset: B50 — merged public comments from Instagram, X (Twitter), and YouTube class exports.",
            "Scale: 58,464 comments — YouTube 45,623 · Instagram 11,833 · X 1,008.",
            "Same topical scrape (sport–politics crossover; heavy Trump-related talk) so cross-platform comparisons are meaningful.",
            "Takeaway: YouTube dominates raw volume; we emphasize within-platform percentages so one huge site does not drown out the others.",
        ],
        bg=SKY,
        accent=INDIGO,
        title_color=INDIGO,
        body_color=CHARCOAL,
        notes="""
        We are working with comments that were already public on social platforms and provided for class. We never put raw comment spreadsheets in the public GitHub repo — only aggregate tables and this slide deck.

        The total row count is a little under sixty thousand. YouTube is the giant bar in our figure — tens of thousands of rows. Instagram is mid-sized. X is the smallest. That size gap is why our main comparisons use percentages inside each platform, not only raw counts.

        “Scope” means we are not describing the whole internet or all voters. We describe this batch of posts and the people who chose to comment on them, as captured by the scrape and each platform’s rules at the time.
        """,
    )

    # --- Slide 4: Methods ---
    _bullet_slide(
        prs,
        "How we measured things (RQ1 & RQ 2)",
        [
            "Moralized (RQ 1): Binary yes/no if text matches any of four keyword families — virtue/vice, harm/care, fairness/cheating, loyalty/betrayal (see keywords_v1.txt).",
            "Stance / polarization cues (RQ 1): Categories like pro-Trump, anti-Trump, partisan_other, neutral_unclear, mixed — from phrase and token lists. Many real opinions stay “neutral_unclear” if they do not hit a list term — so polarized shares are conservative lower bounds.",
            "Stats (RQ 1): Descriptive tables; chi-square for platform × stance with Cramer’s V (effect size); Spearman correlation for moralized vs log(1+likes) within each platform.",
            "RQ 2 extras (X only): Split by blue_verified; split followers into low / mid / high thirds (tertiles). Report Wilson 95% intervals for key percentages — a better “margin of error” style band for proportions than a plain +/-.",
            "Validation: Manual double-coding spot-check (example: ~58% exact stance match vs automation on a 40-comment sample) — dictionaries are imperfect; sarcasm and slang trip us up.",
        ],
        bg=CREAM,
        accent=GOLD,
        title_color=NAVY,
        body_color=CHARCOAL,
        body_size=18,
        notes="""
        For a general audience, think of “moralized” as language that turns a disagreement into a moral fight — calling someone corrupt, a traitor, dangerous, or saying something is rigged or shameful. Our lists are frozen in a text file so anyone can audit them.

        “Stance” here does not mean we read every comment’s soul. We used transparent keyword rules. If someone supports Trump with slang our list missed, we still label neutral_unclear. So when you see a “percent pro-Trump,” read it as “percent that matched our pro-Trump dictionary,” not “percent who secretly love Trump.”

        For statistics in plain English: chi-square asks whether platform and stance label are related in the table; Cramer’s V says how strong that relationship is on a zero-to-one scale — we found a real but modest association. Spearman rho measures whether moralized comments tend to have higher or lower likes in a skewed world where most comments have very few likes.

        For RQ 2 on X, “blue verified” is the checkmark field from the export. Follower tertiles split X authors into three equal-count buckets: lower, middle, and higher follower counts within this file. Wilson intervals are like confidence ribbons for percentages — especially helpful when a subgroup is small.

        We also had humans spot-check a random sample so we are honest about where automation disagrees with a careful reader.
        """,
    )

    # --- Slide 5: RQ1 findings + chart ---
    try:
        s5 = prs.slides.add_slide(prs.slide_layouts[6])
    except Exception:
        s5 = prs.slides.add_slide(prs.slide_layouts[5])
    _slide_bg(s5, SKY)
    _left_accent(s5, prs, TEAL)

    tx = s5.shapes.add_textbox(Inches(0.35), Inches(0.32), Inches(9.0), Inches(0.85))
    tx.text_frame.text = "Key findings — RQ 1 (all platforms)"
    _style_title(tx.text_frame, 30, INDIGO)

    body = s5.shapes.add_textbox(Inches(0.35), Inches(1.15), Inches(6.15), Inches(5.9))
    tf = body.text_frame
    tf.word_wrap = True
    bullets_r1 = [
        "Volume (chart): YouTube >> Instagram >> X — always pair raw counts with within-platform %.",
        "Moralized rate: Instagram ~2.4% · X ~5.1% · YouTube ~5.6% of comments (within each site).",
        "Stance (dictionary-defined): Most rows neutral_unclear. YouTube shows the largest pro-Trump share (~10.5%) vs Instagram (~2.8%) & X (~5.8%). Platform × stance association is real but modest (Cramer’s V ~ 0.09).",
        "Engagement hint: On X, comments tagged pro-Trump have much higher mean likes than other stance buckets — could be controversy, timing, or visibility; not proof of agreement.",
    ]
    for i, b in enumerate(bullets_r1):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(17)
        p.font.color.rgb = CHARCOAL
        p.space_after = Pt(10)

    if VISUAL.exists():
        s5.shapes.add_picture(str(VISUAL), Inches(6.85), Inches(1.05), width=Inches(6.0))
    else:
        nb = s5.shapes.add_textbox(Inches(6.85), Inches(2.0), Inches(5.8), Inches(1.2))
        nb.text_frame.text = "(Chart: RWB_VISUAL.png)"
        for p in nb.text_frame.paragraphs:
            p.font.color.rgb = CORAL

    _notes(
        s5,
        """
        This slide answers Research Question 1 with the headline numbers. Point at the bar chart first: YouTube’s bar is huge — that is why we keep saying “within platform percents.” Otherwise YouTube would dominate every raw count story.

        Moralized percentages are single digits to low single digits on Instagram and a bit higher on X and YouTube in this scrape. In everyday language, explicit moral language — thieves, traitors, murder rhetoric, rigged elections in our lists — shows up in a small slice of rows, but not zero.

        For stance, remember the conservative coding. Even so, YouTube in this batch has the largest share of comments that matched our pro-Trump dictionary. Instagram is much lower on that measure in the same topical scrape. X sits in the middle on several stance breakdowns. Cramer’s V around 0.09 means: yes, platform and stance patterning relate in the table, but this is not a “platform completely determines politics” effect — nuance matters.

        The engagement bullet is easy to misread. Higher likes on pro-Trump-tagged X comments might mean agreement, might mean outrage clicks, might mean one viral thread. We are careful not to over-claim.

        Transition: RQ 2 narrows to X only and asks whether account status and audience size line up with those patterns.
        """,
    )

    # --- Slide 6: RQ2 findings ---
    _bullet_slide(
        prs,
        "Key findings — RQ 2 (X / Twitter only)",
        [
            "Sample: 1,008 X comments — interpret as exploratory; subgroup cells get small fast.",
            "Blue check: Not verified n=175 → ~8.0% moralized (95% Wilson CI ~4.8–13.0%). Verified n=833 → ~4.4% (CI ~3.2–6.1%). In this scrape, unverified rows show a higher moralized % — could be composition, topic, or chance; we do not claim verification “causes” tone.",
            "Stance by verification (row %): e.g. pro-Trump ~4% (not verified) vs ~6.1% (verified); anti-Trump higher in the small not-verified slice (~4% vs ~1.4%).",
            "Followers (tertiles, equal n each): moralized ~7.1% (low followers) → ~4.2% (mid) → ~3.9% (high) — suggestive pattern only; same caution as above.",
            "Bottom line: X metadata reminds us “who comments” may differ by status and reach; do not treat X in B50 as representative of all users.",
        ],
        bg=RGBColor(255, 245, 245),
        accent=CORAL,
        title_color=RGBColor(153, 27, 27),
        body_color=CHARCOAL,
        body_size=17,
        notes="""
        Research Question 2 is only about X because only that spreadsheet included verification and follower counts in a usable way for the whole class.

        Say clearly: about a thousand comments is enough for a classroom exercise but small for strong claims. When we split by verified versus not verified, one side has only 175 comments — that is why we report Wilson confidence intervals. In plain English, those intervals mean: “if we repeated similar sampling, a range like this would often contain the true underlying percent.” Wide intervals mean more uncertainty.

        The moralized comparison surprises some people: in this scrape, comments from accounts without a blue check showed a higher percent moralized than verified accounts, and the intervals overlap in a way that should make you cautious. Possible stories include who chooses to comment, what kinds of threads attracted unverified pile-ons, or how moderation and visibility differ — we are not picking one story with this table alone.

        Stance percentages by verification are also descriptive. You can read them as: verified accounts in this file lean a bit more toward dictionary-visible pro-Trump cues as a share of their comments, while the tiny not-verified slice shows more anti-Trump dictionary hits — but cell sizes mean do not dramatize small gaps.

        Follower tertiles split authors into three equal-sized groups by follower count within this X file. The pattern that lower-follower buckets have slightly higher moralized percentages is interesting for discussion but is not proof that having more followers makes people “nicer.” It is a correlation in one batch of posts.

        Close RQ2 by repeating the ethics point: this is one scrape; X is not the whole world; verified status changed in meaning over time; we are describing patterns, not judging people.
        """,
    )

    # --- Slide 7: Interpretation ---
    _bullet_slide(
        prs,
        "Interpretation & implications",
        [
            "RQ 1: Hybrid sport–politics content pulls moral and partisan language; the mix differs by platform — YouTube carries more dictionary-visible pro-Trump cues in this scrape than Instagram, with X between on several metrics.",
            "RQ 2: On X, verification and follower tier relate descriptively to moralized share and stance mix — treat as exploratory; smallest groups need humility.",
            "For sport orgs & communicators: Expect political spillover in comments; set moderation norms and messaging knowing threads may polarize.",
            "Limits: Keyword methods miss sarcasm and implicit opinion; engagement is not agreement; B50 is not representative of all voters or all platforms.",
        ],
        bg=CREAM,
        accent=INDIGO,
        title_color=NAVY,
        body_color=CHARCOAL,
        body_size=18,
        notes="""
        Pull both questions together for a general audience. First takeaway: when sports and politics overlap in this dataset, you see moral language and political cues, and the flavor differs by platform. YouTube’s slice in this scrape had the largest share of comments matching our pro-Trump list — still a minority of rows, with most comments uncoded as clearly pro or anti by our strict rules.

        Second takeaway: on X, account status and follower bins nudge the percentages in ways that should make us humble about “typical X user” claims. Verified and high-follower voices are not the whole commentariat.

        Practical implication for sports industry folks in the room: treat political spillover as predictable, not accidental. Community guidelines, moderator training, and how official accounts frame hybrid content all matter for whether a thread stays informative or turns into a flame war.

        Ethics and limits in one breath: we used automated dictionaries — they err. Likes can mean mockery. Our sample is one class corpus, not a census of America. We studied language on the page, not whether claims are factually true.

        If someone asks “so who is right politically?” — the project is not designed to answer that. We describe language patterns in a defined sample.
        """,
    )

    # --- Slide 8: Q&A ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    _slide_bg(slide, QNA_BG)
    slide.shapes.title.text = "Thank you"
    slide.placeholders[1].text = "Questions?\n\ngithub.com/lizzyratcliff/Project-3-RWB"
    _style_title(slide.shapes.title.text_frame, 44, WHITE)
    for p in slide.placeholders[1].text_frame.paragraphs:
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(221, 214, 254)
    _notes(
        slide,
        """
        Thank the audience and invite questions. If asked “why Trump?” — the corpus was collected around sport–politics crossover where that discourse was prevalent; we did not choose a random week of sports.

        If asked “can AI replace reading comments?” — we double-coded a sample and report disagreement; human judgment still matters for sarcasm and context.

        If asked “what should Instagram do?” — we are researchers in training, not policy lawyers; we can speak to patterns and tradeoffs, not mandates.

        Repo link is on screen for methods transparency.
        """,
    )

    prs.save(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
