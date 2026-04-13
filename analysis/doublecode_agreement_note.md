# Double-coding validation (RWB)

## 1) Manual spot-check (cite in final write-up §3)

**N=40, coder LR** — full disagreement list: [`doublecode_agreement_note_LR40_manual.md`](doublecode_agreement_note_LR40_manual.md).

- **Stance agreement (manual vs automation, exact):** 57.5%
- **Moralized agreement:** 87.5%

## 2) Exported sample (N=80) — keyword automation baseline

Both coder columns were filled with the **same** rules as `keywords_v1` (`coder_initials` = **AUTO**). This confirms the export → prefill → compare pipeline; it is **not** a substitute for two independent human raters. Clear `AUTO` cells and code manually if your instructor expects human validation on the full 80-row sheet.

---

# Double-coding vs keyword automation (RWB)
- **Coder 1:** AUTO (column `your_stance`)
- **N coded (coder 1):** 80 / 80
- **Stance agreement (coder 1 vs automation, exact):** 100.0%
- **Moralized agreement (coder 1 vs automation):** 100.0%
- **Coder 2:** AUTO (column `stance_coder_2`)
- **N coded (coder 2):** 80 / 80
- **N rows coded by both:** 80
- **Inter-rater stance agreement (exact):** 100.0% (Cohen's kappa = 1.000)
- **Inter-rater moralized agreement:** 100.0% (Cohen's kappa = 1.000)
- **Stance agreement (coder 2 vs automation, exact):** 100.0%
- **Moralized agreement (coder 2 vs automation):** 100.0%

Disagreements with automation are expected where sarcasm, emojis-only comments, or context outside the dictionaries matter. Refine `keywords_v1.txt` if many systematic misses occur, then re-run `scripts/analyze_b50.py`.

## Rows where stance differs (coder 1 vs automation)

_None (among rows coded by coder 1)._ 

## Rows where moralized differs (coder 1 vs automation)

_None (among rows coded by coder 1)._ 

## Rows where stance differs between coders (inter-rater)

_None._
