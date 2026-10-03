# Changelog

## v1.2.0 (2026-10-03)

Correction round after an independent third blind re-extraction of a fresh 9-tool sample (seed 20261003, three extractors, same protocol as pass 2; see `methodology/pass3_*`).

### Changed data

- **5 categorical cells revised** across 4 tools, each backed by official-documentation evidence obtained during blind extraction (full old/new log in `methodology/pass3_adjudication.json`, class C):
  - **SALOME**: `plugin_mechanism` custom → `ipc_api`; `coupling` file_exchange → `orchestration` (official architecture page: CORBA servers with IDL interfaces; official Supervision page: YACS workflow graphs + JobManager for PBS/LSF/SGE/SLURM).
  - **ANSYS Workbench**: `coupling` co_simulation → `orchestration` (project schematic wires components rather than runtime solver data exchange).
  - **LS-DYNA**: `plugin_mechanism` none → `custom` (user-defined materials/subroutines).
  - **Actran**: `plugin_mechanism` none → `custom` (user subroutines).
- **`data/extraction_form.json` coding rules added** (v1.1 adjudication left 17 enum-boundary disagreements unresolved): explicit decision rules for `plugin_mechanism` (in-process vs language-agnostic IPC), `coupling` (orchestration vs co_simulation vs file_exchange), and a single reference-point definition for `validation_years` (first documented public release → 2026; acquisition/founding dates excluded).

### Methodology files added (pass 3)

- `methodology/pass3_agent{1,2,3}.json` — raw blind extractions of 9 tools (LS-DYNA, MSC Nastran, SALOME, Motor-CAD, ANSYS Workbench, Actran, AutoForm, CST Studio Suite, FreeCAD).
- `methodology/pass3_agreement_result.json` — raw third-pass exact agreement **68.5% (74/108)** vs. released v1.1.0; per-field κ from −0.125 (`plugin_mechanism`, near-constant variant breaks κ) to 1.0 (`category`).
- `methodology/pass3_adjudication.json` — all 34 disagreements classified: A=12 (released value documented, blind extraction could not reach the evidence), B=17 (enum-boundary ties → coding rules added, values unchanged), C=5 (released value wrong → corrected above). Post-adjudication pass-3 agreement **73.1% (79/108)**; substantive disagreement rate 4.6%.
- `methodology/compare_pass3.py` — third-pass comparison script; `methodology/verify_claims.py` updated to the v1.2 headline numbers (72 checks).

### Validation-years note

8/9 sampled tools fall within the ±5-year tolerance; the one exception (LS-DYNA: 37 vs. 50) is a reference-point difference (1989 LSTC founding vs. 1976 LLNL origin), which the new single definition in `extraction_form.json` resolves to 50; the released value is unchanged.

### Impact

Coupling distribution in the accompanying paper changes from 17/14/12/2/1 to 17/13/11/4/1; language-agnostic IPC-API tools change from 1/46 to 2/46. All paper statistics were recomputed from v1.2 (`verify_claims.py`: 72 passed, 0 failed).

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
