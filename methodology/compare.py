#!/usr/bin/env python3
"""Pass-2 agreement calculator for Paper 1 (sci/paper1_rebuild).

Compares blind second-pass extraction (recheck/pass2_agent*.json) against the
first-pass dataset (sci/ui/data/tool_survey_raw.json) for the 20% sample
(9 tools, seed 20260927). Field-level exact agreement over 13 scored fields.
source_url scored as presence/absence only; tool_name as identity check.
"""
import json, glob, collections, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sci/paper1_rebuild
REPO = os.path.dirname(os.path.dirname(BASE))                        # sci/..
SCORED = ["category", "industry", "ui_technology", "ui_pattern", "architecture",
          "plugin_mechanism", "scripting", "coupling", "workflow_guide",
          "template_support", "cloud_support", "ai_ml", "validation_years"]

orig = {r["tool_name"]: r for r in
        json.load(open(os.path.join(REPO, "sci/ui/data/tool_survey_raw.json")))["tools"]}

pass2 = {}
for f in sorted(glob.glob(os.path.join(BASE, "recheck/pass2_agent*.json"))):
    d = json.load(open(f))
    for t in d["tools"]:
        pass2[t["tool_name"]] = t

sample = sorted(pass2)
missing = [n for n in sample if n not in orig]
if missing:
    sys.exit(f"pass2 tools not in original dataset: {missing}")
if len(sample) < 9:
    print(f"WARNING: only {len(sample)}/9 sample tools present (agent pending?)\n")

agree = disagree = 0
per_field = collections.defaultdict(lambda: [0, 0])   # field -> [agree, total]
disagreements = []
url_present = [0, 0]

for name in sample:
    o, p = orig[name], pass2[name]
    for f in SCORED:
        ov, pv = o.get(f), p.get(f)
        # bools may arrive as strings
        if isinstance(ov, bool) and isinstance(pv, str):
            pv = pv.strip().lower() == "true"
        ok = (ov == pv)
        per_field[f][1] += 1
        if ok:
            agree += 1
            per_field[f][0] += 1
        else:
            disagree += 1
            disagreements.append((name, f, ov, pv))
    url_present[1] += 1
    if str(p.get("source_url", "")).startswith("http"):
        url_present[0] += 1

total = agree + disagree
pct = 100.0 * agree / total if total else 0.0
print(f"tools scored: {len(sample)}  fields/tool: {len(SCORED)}  total comparisons: {total}")
print(f"field-level exact agreement: {agree}/{total} = {pct:.1f}%")
print(f"source_url presence: {url_present[0]}/{url_present[1]}")
print("\nper-field agreement:")
for f in SCORED:
    a, n = per_field[f]
    print(f"  {f:20s} {a:2d}/{n:2d} = {100.0*a/n:5.1f}%" if n else f"  {f}: n/a")
print(f"\ndisagreements ({len(disagreements)}):")
for name, f, ov, pv in disagreements:
    print(f"  {name} | {f}: pass1={ov!r} pass2={pv!r}")

json.dump({"n_tools": len(sample), "comparisons": total, "agreement": agree,
           "agreement_pct": round(pct, 1),
           "per_field": {f: {"agree": a, "total": n} for f, (a, n) in per_field.items()},
           "disagreements": [{"tool": t, "field": f, "pass1": a, "pass2": b}
                             for t, f, a, b in disagreements]},
          open(os.path.join(BASE, "recheck/agreement_result.json"), "w"),
          ensure_ascii=False, indent=2)
print("\nwrote recheck/agreement_result.json")
