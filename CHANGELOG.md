# Changelog

## v1.1.0 (2026-09-27)

Adjudication round after an independent second-pass re-extraction (see `methodology/`).

### Changed data

- **26 categorical cells revised** across 14 tools (industry, ui_pattern, architecture, scripting, coupling, ui_technology, workflow_guide, template_support, cloud_support, ai_ml), each with official-documentation evidence and a confidence level recorded in `methodology/adjudication_changelog.json`.
- **`validation_years` re-derived for all 46 tools** under a single definition (years since first documented public release, to 2026): 9 sampled tools corrected during adjudication, 36 further values changed by re-derivation, 1 unchanged (45 value changes total).
- **Enum extensions**: `scripting` now permits `delphi` (Altium Designer, DelphiScript) and `javascript` (Simpack, `.sjs`), recorded in `data/extraction_form.json`.
- `data/extraction_form.json` statistics regenerated from the released data.

### Methodology files added

- `methodology/agreement_result.json` — initial exact agreement **62.4% (73/117)**, Cohen's κ = 0.49, per-field agreement table, 44 disagreements.
- `methodology/adjudication_changelog.json` — cell-level old/new values for every revision.
- `methodology/recheck/` — raw second-pass extractions (`pass2_agent1..3.json`), adjudication decisions (`adjudication_A..C.json`), first-release-year evidence (`vyears_A..C.json`).
- `methodology/compare.py`, `methodology/merge_adjudication.py`, `methodology/verify_claims.py` — reproduction scripts.

### Impact

All headline statistics in the accompanying paper (UI stack, coupling categories, pattern distribution, feature rates, validation-year medians/ranges) were recomputed from v1.1.

## v1.0.0 (2026-09-27)

Initial release: 46 tools × 15 fields, extraction form, CSV export, MIT license, CITATION.cff.
