"""Merge LR40 manual summary + AUTO80 compare body into `analysis/doublecode_agreement_note.md`."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LR40 = REPO_ROOT / "analysis" / "doublecode_agreement_note_LR40_manual.md"
AUTO_BODY = REPO_ROOT / "analysis" / "doublecode_agreement_AUTO80_body.md"
OUT = REPO_ROOT / "analysis" / "doublecode_agreement_note.md"

HEADER = """# Double-coding validation (RWB)

## 1) Manual spot-check (cite in final write-up §3)

**N=40, coder LR** — full disagreement list: [`doublecode_agreement_note_LR40_manual.md`](doublecode_agreement_note_LR40_manual.md).

- **Stance agreement (manual vs automation, exact):** 57.5%
- **Moralized agreement:** 87.5%

## 2) Exported sample (N=80) — keyword automation baseline

Both coder columns were filled with the **same** rules as `keywords_v1` (`coder_initials` = **AUTO**). This confirms the export → prefill → compare pipeline; it is **not** a substitute for two independent human raters. Clear `AUTO` cells and code manually if your instructor expects human validation on the full 80-row sheet.

---

"""


def main() -> None:
    if not AUTO_BODY.exists():
        raise SystemExit(f"Missing {AUTO_BODY} — run compare with --out first.")
    body = AUTO_BODY.read_text(encoding="utf-8")
    OUT.write_text(HEADER + body, encoding="utf-8")
    if not LR40.exists():
        print(f"Warning: {LR40} missing (header still references it).")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
