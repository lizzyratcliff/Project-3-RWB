# KIN 7518 — Project 3 — **RWB**

**Official group name:** **RWB** (use this prefix on syllabus files: `RWB_PLAN.md`, `RWB_VISUAL.png`).  
**Public repo:** [github.com/lizzyratcliff/Project-3-RWB](https://github.com/lizzyratcliff/Project-3-RWB)  
**Course:** Social Issues in Sport (LSU)  
**Theme:** Conflict, Morality, and Polarization  
**Research plan:** [`RWB_PLAN.md`](RWB_PLAN.md)  
**Visualization:** [`RWB_VISUAL.png`](RWB_VISUAL.png)

## Team (RWB)

| Name | GitHub (optional) |
|------|-------------------|
| Jardyn Washington | _(add @handle if you want)_ |
| Elizabeth Ratcliff (Lizzy) | _(add @handle if you want)_ |
| Isabelle Besselman | _(add @handle if you want)_ |

## Research questions

### RQ 1 (primary)

**(a)** In the **B50** cross-platform social comment corpus (**Instagram**, **X**, **YouTube**)—collected around **sport–politics crossover** media where **Trump-related** political talk is prevalent—how do **moralized discourse** and **polarization cues** (pro- vs. anti-Trump positioning, partisan blame, us-vs-them framing) **differ across platforms**? **(b)** **Within each platform**, how are those categories **correlated** with **visible engagement** (likes; on **X**, retweets and replies)? Engagement is treated as a **descriptive correlate**, not a causal outcome.

### RQ 2 (optional)

On **X only**, are **`blue_verified`** or **follower count** **correlated** with **(a)** engagement and/or **(b)** a higher share of comments coded **moralized** or **polarized** (see plan §3)?

Full context, significance, methods, ethics, and roles are documented in **`RWB_PLAN.md`**.

## Run the analysis (optional)

Requires Python 3.10+ and local copies of the three Excel files under `dataset/`.

```bash
python -m pip install -r requirements.txt
python scripts/analyze_b50.py
```

- **`keywords_v1.txt`** — frozen v1 dictionaries (moral families + stance); edit and re-run to iterate.
- **`analysis/results_summary.md`** — aggregate tables only (no comment text); regenerate after keyword changes.
- **Double-coding / validation (§3):**
  1. `python scripts/export_coding_sample.py` — default **80** stratified rows → `analysis/doublecode_sample.csv` (gitignored; do not commit).
  2. **Coder 1** fills `your_stance`, `your_moralized_yes_no` (`yes`/`no`), `coder_initials`.
  3. **Coder 2** independently fills `stance_coder_2`, `moral_coder_2`, `coder_2_initials` (same stance labels as the plan).
  4. `python scripts/compare_doublecode_to_keywords.py` — writes **`analysis/doublecode_agreement_note.md`** (or `--out path`): coder vs automation **% agreement**, **inter-rater %** and **Cohen's kappa** when both coders are complete, and row lists for disagreements (still **no** comment text in that markdown).
  5. **Optional pipeline check:** `python scripts/prefill_doublecode_from_keywords.py` fills both coder columns with **AUTO** (keyword rules only), then `python scripts/compare_doublecode_to_keywords.py --out analysis/doublecode_agreement_AUTO80_body.md` and `python scripts/assemble_doublecode_agreement_note.py` rebuild the combined `doublecode_agreement_note.md` (keeps the **LR40 manual** section). Replace **AUTO** with real human codes for final validation.
  6. After any `keywords_v1.txt` change, re-run `python scripts/analyze_b50.py` and re-run the compare script.
- **Figure QA:** `analysis/results_summary.md` includes **Figure verification** counts; a second member should confirm they match `RWB_VISUAL.png` and the three Excel files.

## Dataset (local only)

B50 consists of three Excel exports (Instagram, X, YouTube comments). **Per course instructions, data files are not stored in this repository.** Each member keeps copies **locally** or on a **shared drive**.

Expected filenames (same folder on each machine, e.g. `dataset/`):

- `B50_INS_COMMENT.xlsx`
- `B50_X_COMMENT.xlsx`
- `B50_YT_COMMENT.xlsx`

`.gitignore` excludes `*.xlsx`, `*.csv`, `*.json`, and `*.pdf` so these are not committed by mistake.

## Collaboration workflow

Each team member works on their own branch and submits changes through pull requests. One member can serve as the manager who reviews and merges approved work into `main`.

**Cycle:** `git pull` → branch → work → commit → push → PR → review → merge.

1. **Collaborators:** Repository **owner** → **Settings** → **Collaborators** (or **Manage access**) → invite teammates with **Write** access.
2. **This repo is public** — treat it like a portfolio piece. **Do not commit** scraped social data.

## License / course use

This repository is for **coursework** (KIN 7518). Do not redistribute scraped social data.
