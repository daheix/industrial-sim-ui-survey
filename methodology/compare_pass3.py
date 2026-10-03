#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pass-3 blind re-extraction vs published values (v1.1.0): per-field
agreement, Cohen's kappa (13 categorical fields), and validation_years
tolerance check. Usage: python3 compare_pass3.py [recheck_dir]
Reads pass3_agent{1,2,3}.json + ../ui/data/tool_survey_raw.json
Writes pass3_agreement_result.json in recheck_dir."""
import json, os, sys, glob
from collections import Counter

RECHECK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(RECHECK, "..", "..", "ui", "data", "tool_survey_raw.json")
FIELDS = ["category", "industry", "ui_technology", "ui_pattern", "architecture",
          "plugin_mechanism", "scripting", "coupling", "workflow_guide",
          "template_support", "cloud_support", "ai_ml"]  # 12 categorical
TOL_YEARS = 5  # validation_years judged consistent within +/-5 years


def kappa(a, b):
    """Cohen's kappa for two equal-length label lists."""
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def main():
    blind = {}
    for p in sorted(glob.glob(os.path.join(RECHECK, "pass3_agent*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for t in d["tools"]:
            blind[t["tool_name"].lower()] = t
    _raw = json.load(open(RAW, encoding="utf-8"))
    raw = {r["tool_name"].lower(): r for r in (_raw["tools"] if isinstance(_raw, dict) else _raw)}

    rows, per_field = [], {f: {"a": [], "b": []} for f in FIELDS}
    years = []
    for name, b in sorted(blind.items()):
        r = raw.get(name)
        if r is None:
            print(f"WARN: {name} not in tool_survey_raw.json"); continue
        diffs = []
        for f in FIELDS:
            a, v = r.get(f), b.get(f)
            per_field[f]["a"].append(str(a)); per_field[f]["b"].append(str(v))
            if a != v:
                diffs.append(f"{f}: published={a!r} blind={v!r}")
        ya, yb = r.get("validation_years"), b.get("validation_years")
        years.append({"tool": name, "published": ya, "blind": yb,
                      "within_tol": None if (ya is None or yb is None) else abs(ya - yb) <= TOL_YEARS})
        rows.append({"tool": name, "n_field_diffs": len(diffs), "diffs": diffs,
                     "years": years[-1]})

    summary, n = {}, len(rows)
    for f, d in per_field.items():
        k, po = kappa(d["a"], d["b"])
        summary[f] = {"n": n, "agree": round(po, 4), "kappa": round(k, 4),
                      "interpretable": "no_var" if po in (0.0, 1.0) and
                      len(set(d["a"])) == 1 and len(set(d["b"])) == 1 else
                      ("poor" if k < 0.2 else "fair" if k < 0.4 else
                       "moderate" if k < 0.6 else "substantial" if k < 0.8 else "almost_perfect")}
    total_pairs = n * len(FIELDS)
    total_agree = sum(round(s["agree"] * n) for s in summary.values())
    out = {"pass": 3, "n_tools": n, "fields": FIELDS,
           "total_agreement": {"pairs": total_pairs, "agree": total_agree,
                               "rate": round(total_agree / total_pairs, 4)},
           "per_field": summary,
           "validation_years": {"tolerance": TOL_YEARS,
                                "within": sum(1 for y in years if y["within_tol"]),
                                "detail": years},
           "per_tool": rows}
    dst = os.path.join(RECHECK, "pass3_agreement_result.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"tools={n}  overall agreement={total_agree}/{total_pairs}="
          f"{out['total_agreement']['rate']:.1%}  -> {dst}")
    for f, s in summary.items():
        flag = "  <-- diff" if s["agree"] < 1.0 else ""
        print(f"  {f:18s} agree={s['agree']:.2f} kappa={s['kappa']:+.3f}{flag}")
    for row in rows:
        if row["diffs"]:
            print(f"[{row['tool']}] " + "; ".join(row["diffs"]))


if __name__ == "__main__":
    main()
