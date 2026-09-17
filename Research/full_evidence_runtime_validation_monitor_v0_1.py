import argparse
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import full_evidence_runtime_log_v0_1 as runtime

DEFAULT_LOG = Path("Research/runtime/full_evidence_runtime_log_v0_1.jsonl")
DEFAULT_JSON = Path("Research/results/full_evidence_runtime_validation_monitor_v0_1.json")
DEFAULT_MD = Path("Research/results/full_evidence_runtime_validation_monitor_v0_1.md")
KST = timezone(timedelta(hours=9))


def _date(v):
    return date.fromisoformat(str(v)[:10])


def _add_months(d: date, months: int) -> date:
    month0 = d.month - 1 + months
    y = d.year + month0 // 12
    m = month0 % 12 + 1
    mdays = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
             31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return date(y, m, min(d.day, mdays[m - 1]))


def _regime_family(label):
    m = re.search(r"\bR([1-8])\b", str(label or "").upper())
    return f"R{m.group(1)}" if m else "UNCLASSIFIED"


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def analyze(log_path=DEFAULT_LOG, as_of=None):
    rows = runtime.build_projection(log_path)
    if as_of is None:
        as_of = datetime.now(KST).date()
    elif isinstance(as_of, str):
        as_of = date.fromisoformat(as_of)

    total = len(rows)
    quality = Counter(str(r.get("quality", "UNKNOWN")) for r in rows)
    actions = Counter(str(r.get("action_direction", "UNKNOWN")) for r in rows)
    mapper = Counter(str(r.get("mapper_status", "UNKNOWN")) for r in rows)
    regimes = Counter(_regime_family(r.get("validated_regime")) for r in rows)
    checkpoints = Counter(str(r.get("session_checkpoint", "UNKNOWN")) for r in rows)

    mature = {}
    for h in ("1d", "5d", "20d"):
        n = sum(1 for r in rows if r.get(f"outcome_status_{h}") == "MATURE")
        mature[h] = {
            "count": n,
            "coverage": (n / total if total else 0.0),
        }

    corrections = sum(int(r.get("correction_count") or 0) for r in rows)
    mapped = [r for r in rows if r.get("mapper_status") != "NOT MAPPED"]
    mapped_count = len(mapped)

    core_reductions = 0
    reducible_mapped = 0
    noncore_only_reductions = 0
    for r in mapped:
        if r.get("action_direction") != "REDUCE":
            continue
        cb, ca = r.get("core_before"), r.get("core_after")
        tb, ta = r.get("tactical_before"), r.get("tactical_after")
        lb, la = r.get("leverage_before"), r.get("leverage_after")
        if all(_is_num(x) for x in (cb, ca, tb, ta, lb, la)):
            reducible_mapped += 1
            if ca < cb:
                core_reductions += 1
            elif ta < tb or la < lb:
                noncore_only_reductions += 1

    first_date = min((_date(r["market_date"]) for r in rows), default=None)
    elapsed_days = (as_of - first_date).days if first_date else 0
    two_month_date = _add_months(first_date, 2) if first_date else None
    three_month_date = _add_months(first_date, 3) if first_date else None
    six_month_date = _add_months(first_date, 6) if first_date else None

    distinct_regimes = len([k for k, v in regimes.items() if k != "UNCLASSIFIED" and v > 0])
    reduce_actions = actions.get("REDUCE", 0)
    restore_actions = actions.get("RESTORE", 0)

    stage1_checks = {
        "samples_20": total >= 20,
        "regime_families_2": distinct_regimes >= 2,
    }
    stage1 = "MET" if all(stage1_checks.values()) else "NOT MET"

    # Protocol v0.2 deliberately uses qualitative phrases such as
    # 'risk-control observations', 'recovery/restoration observations',
    # 'substantial majority', and 'enough +20d outcomes'. This monitor must
    # not invent hidden numeric thresholds for those concepts.
    stage2a_explicit = {
        "samples_30": total >= 30,
        "two_months_elapsed": bool(two_month_date and as_of >= two_month_date),
        "regime_families_3": distinct_regimes >= 3,
    }
    stage2a = (
        "MANUAL REVIEW REQUIRED"
        if all(stage2a_explicit.values())
        else "NOT YET ELIGIBLE"
    )

    stage2b_due = bool(three_month_date and as_of >= three_month_date)
    stage2b_preferred = {
        "samples_40": total >= 40,
        "reduce_actions_10_tracking_only": reduce_actions >= 10,
        "restore_actions_10_tracking_only": restore_actions >= 10,
        "regime_families_3": distinct_regimes >= 3,
    }

    stage3_explicit = {
        "samples_60": total >= 60,
        "six_months_elapsed": bool(six_month_date and as_of >= six_month_date),
        "regime_families_adequate_manual": distinct_regimes >= 3,
    }
    stage3 = (
        "MANUAL REVIEW REQUIRED"
        if all(stage3_explicit.values())
        else "NOT YET ELIGIBLE"
    )

    return {
        "protocol": "Full Evidence Runtime Validation Protocol v0.2",
        "status": "MONITORING ONLY / NO HIDDEN SCORE / NOT OFFICIAL 3.2 AUTHORITY",
        "as_of": as_of.isoformat(),
        "first_sample_date": first_date.isoformat() if first_date else None,
        "elapsed_days": elapsed_days,
        "total_samples": total,
        "quality_counts": dict(sorted(quality.items())),
        "regime_family_counts": dict(sorted(regimes.items())),
        "distinct_classified_regime_families": distinct_regimes,
        "action_counts": dict(sorted(actions.items())),
        "mapper_status_counts": dict(sorted(mapper.items())),
        "session_checkpoint_counts": dict(sorted(checkpoints.items())),
        "correction_count": corrections,
        "outcome_maturity": mature,
        "execution_mapping": {
            "mapped_samples": mapped_count,
            "fully_observable_reduce_mappings": reducible_mapped,
            "core_reductions": core_reductions,
            "noncore_only_reductions": noncore_only_reductions,
            "noncore_only_reduction_rate": (
                noncore_only_reductions / reducible_mapped if reducible_mapped else None
            ),
        },
        "tracking_proxies_not_protocol_equivalents": {
            "reduce_actions": reduce_actions,
            "restore_actions": restore_actions,
            "note": (
                "REDUCE/RESTORE action counts are operational tracking only. "
                "They are not automatically equivalent to Protocol v0.2's broader "
                "deterioration/risk-control and recovery/restoration observation counts."
            ),
        },
        "milestones": {
            "two_month_date": two_month_date.isoformat() if two_month_date else None,
            "three_month_date": three_month_date.isoformat() if three_month_date else None,
            "six_month_date": six_month_date.isoformat() if six_month_date else None,
        },
        "stage1": {"status": stage1, "checks": stage1_checks},
        "stage2a_provisional": {
            "status": stage2a,
            "explicit_checks": stage2a_explicit,
            "manual_checks_required": [
                "at least 8 deterioration/risk-control observations",
                "at least 8 recovery/restoration observations",
                "substantial majority of eligible +5d outcomes matured",
                "enough +20d outcomes matured to inspect path quality",
                "false-positive/recovery-lag/Core-sale/turnover/failure-pattern review",
            ],
        },
        "stage2b_three_month_checkpoint": {
            "due": stage2b_due,
            "preferred_tracking_checks": stage2b_preferred,
            "note": (
                "Action counts shown here are tracking proxies only; final Protocol observation "
                "classification remains a documented review step."
            ),
        },
        "stage3_official_integration": {
            "status": stage3,
            "explicit_checks": stage3_explicit,
            "manual_checks_required": [
                "mature +20d outcomes for a substantial majority",
                "adequate regime diversity",
                "architecture/evidence/execution/regression formal review",
            ],
        },
    }


def render_markdown(m):
    def pct(x):
        return f"{x * 100:.1f}%"

    maturity = m["outcome_maturity"]
    lines = [
        "# Full Evidence Runtime Validation Monitor v0.1",
        "",
        f"Protocol: **{m['protocol']}**",
        f"As-of: **{m['as_of']}**",
        f"Status: {m['status']}",
        "",
        "## Current progress",
        f"- Samples: **{m['total_samples']}**",
        f"- First sample: **{m['first_sample_date'] or 'NONE'}**",
        f"- Elapsed days: **{m['elapsed_days']}**",
        f"- Classified Regime families: **{m['distinct_classified_regime_families']}**",
        f"- Corrections preserved: **{m['correction_count']}**",
        f"- +1d mature: **{maturity['1d']['count']} / {m['total_samples']} ({pct(maturity['1d']['coverage'])})**",
        f"- +5d mature: **{maturity['5d']['count']} / {m['total_samples']} ({pct(maturity['5d']['coverage'])})**",
        f"- +20d mature: **{maturity['20d']['count']} / {m['total_samples']} ({pct(maturity['20d']['coverage'])})**",
        "",
        "## Protocol stages",
        f"- Stage 1 Operational: **{m['stage1']['status']}**",
        f"- Stage 2A Provisional adoption review: **{m['stage2a_provisional']['status']}**",
        f"- Stage 2B 3-month checkpoint due: **{m['stage2b_three_month_checkpoint']['due']}**",
        f"- Stage 3 Official integration: **{m['stage3_official_integration']['status']}**",
        "",
        "## Counts",
        f"- Quality: `{json.dumps(m['quality_counts'], ensure_ascii=False, sort_keys=True)}`",
        f"- Regimes: `{json.dumps(m['regime_family_counts'], ensure_ascii=False, sort_keys=True)}`",
        f"- Actions: `{json.dumps(m['action_counts'], ensure_ascii=False, sort_keys=True)}`",
        f"- Mapper: `{json.dumps(m['mapper_status_counts'], ensure_ascii=False, sort_keys=True)}`",
        "",
        "## Provisional-adoption timing",
        f"- 2-month earliest date: **{m['milestones']['two_month_date'] or 'N/A'}**",
        f"- 3-month checkpoint: **{m['milestones']['three_month_date'] or 'N/A'}**",
        f"- 6-month official-review date: **{m['milestones']['six_month_date'] or 'N/A'}**",
        "",
        "## Important boundary",
        "- This monitor does not create a score or decide adoption automatically.",
        "- REDUCE/RESTORE action counts are tracking proxies, not automatic substitutes for the Protocol's broader risk-control/recovery observation counts.",
        "- Qualitative maturity/diversity checks remain explicit manual review items rather than invented thresholds.",
        "- Official 3.2 Authority remains unchanged.",
    ]
    return "\n".join(lines) + "\n"


def write_reports(log_path=DEFAULT_LOG, json_path=DEFAULT_JSON, md_path=DEFAULT_MD, as_of=None):
    m = analyze(log_path, as_of=as_of)
    json_path, md_path = Path(json_path), Path(md_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(m), encoding="utf-8")
    return m


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", default=str(DEFAULT_LOG))
    p.add_argument("--json", default=str(DEFAULT_JSON))
    p.add_argument("--md", default=str(DEFAULT_MD))
    p.add_argument("--as-of", default=None)
    a = p.parse_args()
    m = write_reports(a.log, a.json, a.md, a.as_of)
    print(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
