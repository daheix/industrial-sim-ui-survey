# Industrial Simulation UI & Extension Architecture Survey — Replication Package

Replication package for the empirical study **"User Interface and Extension Architecture in Industrial Simulation Software: An Empirical Study of 46 Tools"**.

This package releases the complete, machine-readable extraction dataset so that every number reported in the paper can be independently recomputed.

## Contents

| File | Description |
|------|-------------|
| `data/tool_survey_raw.json` | Primary dataset: 46 tools × 15 fields, verbatim as extracted |
| `data/tool_survey_46x15.csv` | Same dataset as CSV (header + 46 rows) |
| `data/extraction_form.json` | Extraction form: field definitions, enums, and derived statistics |

## Fields (15)

`tool_name`, `category`, `industry`, `ui_technology`, `ui_pattern`, `architecture`, `plugin_mechanism`, `scripting`, `coupling`, `workflow_guide`, `template_support`, `cloud_support`, `ai_ml`, `validation_years`, `source_url`

Each record carries the primary official source URL used for extraction.

## Method notes

- Coverage: 37 commercial + 9 open-source tools; 8 engineering domains + 3 cross-cutting categories.
- Every field is an enum/boolean/integer defined in `extraction_form.json`; out-of-form values are not permitted.
- A second-pass consistency check on a 20% random sample (9 tools, seed `20260927`) is reported in the accompanying paper.

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
