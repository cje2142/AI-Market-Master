# AI Market Master 3.2 — Data Efficiency Runtime Comparator v0.1 Freeze

Date: 2026-09-18
Status: FROZEN RESEARCH IMPLEMENTATION / PROSPECTIVE COMPARISON ONLY

## Scope
This milestone adds a minimal append-only comparator for:
- Official 3.2 C1-C8 + SAI
- Data Efficiency Candidate v0.1 C1-C7 + SAI_DE

It does not modify:
- official 3.2 scoring authority,
- adaptive/regime authority,
- Data Efficiency Candidate v0.1 freeze,
- Full Evidence Candidate v1.0 authority boundaries.

## Files
- Research/data_efficiency_runtime_comparator_v0_1.py
- Research/test_data_efficiency_runtime_comparator_v0_1.py

## Journal
Recommended canonical path:
- Research/runtime/data_efficiency_runtime_comparator_v0_1.jsonl

JSONL is append-only and authoritative. No CSV authority is introduced.

## Recorded comparison fields
- official C1-C8 / SAI
- candidate C1-C7 / SAI_DE
- SAI delta
- sign-direction agreement
- material divergence diagnostic (|delta| >= 0.15)
- C4 delta / direction flip
- C6 delta / direction flip
- C8 official shadow value
- nominal C8 weighted contribution (0.07*C8; diagnostic only)
- explicit C8 effect field supplied by upstream when available
- explicit missing-data effect supplied by upstream when available
- official/candidate data-weight coverage
- regime agreement
- T+1/T+5/T+20 PENDING placeholders and append-only outcome events

## Important boundaries
1. Comparator does not recompute official formulas.
2. It compares already-computed model outputs from the same observation.
3. C8_nominal_weighted_contribution is diagnostic only and is not claimed to equal the actual effect under Official PARTIAL renormalization.
4. Missing-data effect is not invented. If upstream cannot attribute it, it remains null.
5. Sign direction is descriptive only and is not an action threshold.
6. The 0.15 Material SAI Divergence threshold remains research-only.
7. No adoption decision is automated.

## Validation
Unit tests cover:
- comparison deltas,
- direction/regime agreement,
- material divergence,
- data coverage,
- invalid VERIFIED+missing rejection,
- append-only duplicate guard,
- T+5 outcome maturity,
- duplicate outcome rejection.

Actual prospective validation still follows Data Efficiency Candidate v0.1:
20 samples -> structural review
30 samples + 2 months -> early provisional comparison
~40 samples + 3 months -> provisional decision
60 samples + 6 months -> formal integration review

Official 3.2 remains unchanged.
