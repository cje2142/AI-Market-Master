# Full Evidence Candidate Transition Engine v1.0 — Deterministic Test

Status: EXPERIMENTAL CANDIDATE TEST / NOT OFFICIAL 3.2 AUTHORITY

Result: **22/22 PASS**

| Test | Result |
|---|---|
| T1 no gate remains HOLD | PASS |
| T2 base reduction 100 to 95 | PASS |
| T3 additional reduction 95 to 90 | PASS |
| T4 strong reduction 90 to 80 | PASS |
| T5 strong reduction 80 to 70 | PASS |
| T6 deepest reduction 70 to 60 | PASS |
| T7 strong-gate fallback preserves discrete path | PASS |
| T8 reduction cooldown blocks repeat action | PASS |
| T9 R5 to R6 cooldown bypass | PASS |
| T10 Cost Gate FAIL blocks reduction | PASS |
| T11 unavailable Cost Gate remains explicit | PASS |
| T12 R6 emergency Cost Gate bypass | PASS |
| T13 material conflict forces HOLD | PASS |
| T14 blocked quality remains blocked | PASS |
| T15 missing evidence does not become neutral signal | PASS |
| T16 base restoration 60 to 70 | PASS |
| T17 additional restoration 80 to 90 | PASS |
| T18 return-to-100 restoration | PASS |
| T19 fast V-rebound 60 to 80 | PASS |
| T20 Cost Gate FAIL blocks restoration | PASS |
| T21 emergency bypass rejected for restoration | PASS |
| T22 standard restoration 95 to 100 | PASS |

Boundary: these tests validate frozen Candidate v1.0 transition semantics only. They do not establish profitability, market-timing performance, provisional adoption, or official 3.2 integration.
