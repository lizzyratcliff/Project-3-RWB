# KIN 7518 — Project 3 — **RWB**

**Official group name:** **RWB** (use this prefix on syllabus files: `RWB_PLAN.md`, `RWB_VISUAL.png`).  
**Course:** Social Issues in Sport (LSU)  
**Theme:** Conflict, Morality, and Polarization  
**Research plan:** [`RWB_PLAN.md`](RWB_PLAN.md)  
**Visualization:** [`RWB_VISUAL.png`](RWB_VISUAL.png)

## Team (RWB)

| Name | GitHub (optional) |
|------|-------------------|
| Lizzy Ratcliff | _(add @handle if you want)_ |
| [Member 2] | @[username] |
| [Member 3] | @[username] |

*Add **RWB** teammates’ names and GitHub handles when ready.*

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
- **Double-coding sample (§3):** `python scripts/export_coding_sample.py 80` writes `analysis/doublecode_sample.csv` (CSV is gitignored — do not commit).

## Dataset (local only)

B50 consists of three Excel exports (Instagram, X, YouTube comments). **Per course instructions, data files are not stored in this repository.** Each member keeps copies **locally** or on a **shared drive**.

Expected filenames (same folder on each machine, e.g. `dataset/`):

- `B50_INS_COMMENT.xlsx`
- `B50_X_COMMENT.xlsx`
- `B50_YT_COMMENT.xlsx`

`.gitignore` excludes `*.xlsx`, `*.csv`, `*.json`, and `*.pdf` so these are not committed by mistake.

## GitHub setup and workflow

1. **Collaborators:** Repository **owner** → **Settings** → **Collaborators** (or **Manage access**) → invite both other members with appropriate access (e.g. **Write**).
2. **Workflow:** `git pull` → create a **feature branch** → commit → `git push` → open a **Pull Request** → teammate **review** → **merge** to `main`, as demonstrated in class.

## License / course use

This repository is for **coursework** (KIN 7518). Do not redistribute scraped social data.
