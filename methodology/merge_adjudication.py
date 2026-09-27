#!/usr/bin/env python3
"""Merge adjudication + validation_years re-derivation into a v1.1 dataset,
regenerate extraction form stats, and report every manuscript claim that changed.

Run AFTER adjudication_A/B/C.json and vyears_A/B/C.json exist.
Usage: python3 recheck/merge_adjudication.py --dry-run   (report only)
       python3 recheck/merge_adjudication.py --apply      (write dataset v1.1)
"""
import json, glob, os, sys, collections, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(BASE))
RAW = os.path.join(REPO, "sci/ui/data/tool_survey_raw.json")
FORM = os.path.join(REPO, "sci/ui/data/extraction_form.json")
TEX = os.path.join(BASE, "main_rebuild.tex")
apply = "--apply" in sys.argv

d = json.load(open(RAW))
tools = {r["tool_name"]: r for r in d["tools"]}
form = json.load(open(FORM))

# ---- load adjudication decisions ----
decisions = []
for f in sorted(glob.glob(os.path.join(BASE, "recheck/adjudication_*.json"))):
    decisions += json.load(open(f))["decisions"]
years = []
for f in sorted(glob.glob(os.path.join(BASE, "recheck/vyears_*.json"))):
    years += json.load(open(f))["years"]

print(f"decisions loaded: {len(decisions)}  years records: {len(years)}")

# ---- apply field decisions ----
changes = []
for dec in decisions:
    t, fld = dec["tool_name"], dec["field"]
    if t not in tools:
        print(f"!! decision for unknown tool: {t}"); continue
    cur, new = tools[t].get(fld), dec["final_value"]
    if cur != new:
        changes.append((t, fld, cur, new, dec.get("confidence", "?")))
        tools[t][fld] = new

# ---- apply validation_years (unified definition) ----
vy_changes = []
for y in years:
    t = y["tool_name"]
    if t not in tools:
        print(f"!! years for unknown tool: {t}"); continue
    cur, new = tools[t]["validation_years"], y["validation_years"]
    if cur != new:
        vy_changes.append((t, cur, new, y.get("confidence", "?")))
        tools[t]["validation_years"] = new

print(f"\nfield changes: {len(changes)}")
for c in changes: print("  ", c)
print(f"validation_years changes (of {len(years)} looked up): {len(vy_changes)}")

# ---- enum extensions actually used? ----
form_scripting = next(f for f in form["fields"] if f["name"] == "scripting")
used = set(str(r["scripting"]) for r in tools.values())
new_langs = sorted(used - set(form_scripting["values"]))
print(f"scripting enum extension needed: {new_langs or 'none'}")

# ---- recompute stats ----
def cnt(k): return dict(collections.Counter(r[k] for r in tools.values()).most_common())
stats = form.get("statistics", {})
def check(label, computed):
    old = None
    print(f"  {label}: {computed}")

print("\n=== manuscript claims vs recomputed ===")
n = len(tools)
arch = collections.Counter(r["architecture"] for r in tools.values())
pl = arch["plugin_based"] + arch["layered"]
print(f"  89.1% (41/46) plugin+layered -> {pl}/{n} = {100*pl/n:.1f}%   {'CHANGED' if pl != 41 else 'ok'}")
ui = collections.Counter(r["ui_technology"] for r in tools.values())
cu = ui["custom"]; print(f"  73.9% (34/46) custom -> {cu}/{n} = {100*cu/n:.1f}%   {'CHANGED' if cu != 34 else 'ok'}")
comm = [r for r in tools.values() if r["category"] == "commercial"]
oss = [r for r in tools.values() if r["category"] == "open_source"]
cc = sum(1 for r in comm if r["ui_technology"] == "custom")
print(f"  86.5% (32/37) commercial custom -> {cc}/{len(comm)} = {100*cc/len(comm):.1f}%   {'CHANGED' if cc != 32 else 'ok'}")
oq = sum(1 for r in oss if r["ui_technology"] == "qt")
print(f"  66.7% (6/9) oss Qt -> {oq}/{len(oss)} = {100*oq/len(oss):.1f}%   {'CHANGED' if oq != 6 else 'ok'}")
sc = collections.Counter(r["scripting"] for r in tools.values())
py = sc["python"]; print(f"  65.2% (30/46) python -> {py}/{n} = {100*py/n:.1f}%   {'CHANGED' if py != 30 else 'ok'}")
print(f"  scripting dist: {dict(sc)}")
up = collections.Counter(r["ui_pattern"] for r in tools.values())
print(f"  workbench 20/46 -> {up['workbench']}/{n}   {'CHANGED' if up['workbench'] != 20 else 'ok'}")
print(f"  ui_pattern dist: {dict(up)}")
cp = collections.Counter(r["coupling"] for r in tools.values())
print(f"  coupling: {dict(cp)} (text claims 14/11/16/3+2)")
pm = collections.Counter(r["plugin_mechanism"] for r in tools.values())
print(f"  plugin_mech: {dict(pm)} (text claims custom40/ipc1/none5)")
ipc = pm["ipc_api"]; print(f"  IPC 1/46 -> {ipc}/{n}")
years_all = sorted(r["validation_years"] for r in tools.values())
print(f"  validation range '3 to 40' -> {years_all[0]} to {years_all[-1]}   {'CHANGED' if (years_all[0], years_all[-1]) != (3, 40) else 'ok'}")
for cat in ("commercial", "open_source"):
    ys = sorted(r["validation_years"] for r in tools.values() if r["category"] == cat)
    med = ys[len(ys)//2] if len(ys) % 2 else (ys[len(ys)//2-1] + ys[len(ys)//2]) / 2
    print(f"  median {cat}: {med} (range {ys[0]}-{ys[-1]}) [manuscript: 20 (10-40) / 15 (3-30)]")
feat = {k: sum(1 for r in tools.values() if r[k] is True) for k in ("workflow_guide", "template_support", "cloud_support", "ai_ml")}
print(f"  features: {feat} -> " + ", ".join(f"{k} {100*v/n:.1f}%" for k, v in feat.items()) + " [ms: 67.4/63.0/50.0/37.0]")
# chi2 recompute
tab = collections.Counter((r["category"], "custom" if r["ui_technology"] == "custom" else "other") for r in tools.values())
a, b = tab[("commercial", "custom")], tab[("commercial", "other")]
c, e = tab[("open_source", "custom")], tab[("open_source", "other")]
nn = a+b+c+e; chi2 = nn*(a*e-b*c)**2/((a+b)*(c+e)*(a+c)*(b+e))
print(f"  chi2 UI x provenance: cell [{a},{b}]/[{c},{e}] chi2={chi2:.2f} [ms: 15.51]")

# rows of complete-survey table needing update
print("\n=== complete-survey table cells to patch ===")
for ch in changes:
    if ch[1] in ("ui_pattern", "architecture", "scripting", "coupling", "industry", "category", "ui_technology"):
        print(f"  {ch[0]} :: {ch[1]}: {ch[2]} -> {ch[3]}")

if apply:
    # field descriptions / enum updates
    next(f for f in form["fields"] if f["name"] == "validation_years")["description"] = \
        "Years since first documented public release (to 2026)"
    if new_langs:
        form_scripting["values"] += new_langs
    form.pop("statistics", None)
    form["statistics_note"] = "Derived from tool_survey_raw.json (46 tools); recompute with tools/regenerate_stats.py"
    form["statistics"] = {
        "total_tools": n, "by_category": cnt("category"), "by_industry": cnt("industry"),
        "by_architecture": cnt("architecture"), "by_ui_technology": cnt("ui_technology"),
        "by_ui_pattern": cnt("ui_pattern"), "by_plugin_mechanism": cnt("plugin_mechanism"),
        "by_scripting": cnt("scripting"), "by_coupling": cnt("coupling"),
        "features": {f"{k}_true": v for k, v in feat.items()},
    }
    json.dump(d, open(RAW, "w"), ensure_ascii=False, indent=2)
    json.dump(form, open(FORM, "w"), ensure_ascii=False, indent=2)
    json.dump({"adjudicated_cells": len(changes), "years_updated": len(vy_changes),
               "changes": [{"tool": t, "field": f, "old": o, "new": n2, "confidence": cf}
                           for t, f, o, n2, cf in changes],
               "years_changes": [{"tool": t, "old": o, "new": n2, "confidence": cf}
                                 for t, o, n2, cf in vy_changes]},
              open(os.path.join(BASE, "recheck/adjudication_changelog.json"), "w"),
              ensure_ascii=False, indent=2)
    print("\nAPPLIED: dataset v1.1 + form + recheck/adjudication_changelog.json written")
else:
    print("\nDRY-RUN only (use --apply to write)")
