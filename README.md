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
- **Double-coding sample (§3):** `python scripts/export_coding_sample.py 80` writes `analysis/doublecode_sample.csv` (CSV is gitignored — do not commit). After you fill manual columns, run `python scripts/compare_doublecode_to_keywords.py` to refresh `analysis/doublecode_agreement_note.md` (aggregate agreement vs `keywords_v1`; no comment text in that file).

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
