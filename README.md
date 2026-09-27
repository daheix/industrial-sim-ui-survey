# Industrial Simulation UI & Extension Architecture Survey — Replication Package

Replication package for the empirical study **"User Interface and Extension Architecture in Industrial Simulation Software: An Empirical Study of 46 Tools"**.

This package releases the complete, machine-readable extraction dataset so that every number reported in the paper can be independently recomputed.

## Contents

| File | Description |
|------|-------------|
| `data/tool_survey_raw.json` | Primary dataset: 46 tools × 15 fields, verbatim as extracted (v1.1) |
| `data/tool_survey_46x15.csv` | Same dataset as CSV (header + 46 rows) |
| `data/extraction_form.json` | Extraction form: field definitions, enums, and derived statistics |
| `methodology/agreement_result.json` | Second-pass re-extraction agreement statistics (9 tools × 13 fields) |
| `methodology/adjudication_changelog.json` | Cell-level adjudication log: every revised cell with old/new value and confidence |
| `methodology/recheck/` | Raw second-pass extractions and adjudication decision files (per agent) |
| `methodology/compare.py` | Recomputes agreement statistics from raw files |
| `methodology/merge_adjudication.py` | Replays the adjudication merge and recomputes dataset statistics |
| `methodology/verify_claims.py` | Checks every headline claim of the paper against `data/tool_survey_raw.json` |
| `CHANGELOG.md` | Version history |

## Fields (15)

`tool_name`, `category`, `industry`, `ui_technology`, `ui_pattern`, `architecture`, `plugin_mechanism`, `scripting`, `coupling`, `workflow_guide`, `template_support`, `cloud_support`, `ai_ml`, `validation_years`, `source_url`

Each record carries the primary official source URL used for extraction.

## Method notes

- Coverage: 37 commercial + 9 open-source tools; 8 engineering domains + 3 cross-cutting categories.
- Every field is an enum/boolean/integer defined in `extraction_form.json`; out-of-form values are not permitted.
- **Second-pass agreement**: a 20% random sample (9 tools, seed `20260927`) was re-extracted independently. Exact agreement over the 13 scored fields was **62.4% (73/117), Cohen's κ = 0.49** on pooled field–tool pairs (67.6% over the 12 categorical/boolean fields). All 44 disagreements were then adjudicated cell by cell against official documentation; see `methodology/`.
- **validation_years definition**: years since first documented public release, counted to 2026. This field was re-derived for all 46 tools under that single definition (first release year and evidence URL recorded in `methodology/adjudication_changelog.json` and `methodology/recheck/vyears_*.json`).
- **Tool names**: the paper's complete survey table uses exactly the `tool_name` values released here, so every table row maps one-to-one to a JSON record.

## Version history

- **v1.1.0 (2026-09-27)**: adjudication round applied — 26 categorical cells revised, `validation_years` re-derived for all 46 tools under the unified definition; scripting enum extended with `delphi` and `javascript`; extraction-form statistics regenerated; methodology logs released. See `CHANGELOG.md`.
- **v1.0.0 (2026-09-27)**: initial release.

## How to cite

```bibtex
@dataset{wu2026simui,
  author  = {Wu, Shouchun},
  title   = {Industrial Simulation UI \& Extension Architecture Survey (46 tools × 15 fields)},
  year    = {2026},
  publisher = {GitHub},
  url     = {https://github.com/daheix/industrial-sim-ui-survey}
}
```

## License

MIT (see `LICENSE`).
