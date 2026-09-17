# Full Evidence Candidate -> Risk Budget Connector v1.0 — Deterministic Test

Status: EXPERIMENTAL STEP-5 INTEGRATION TEST / NOT OFFICIAL 3.2 AUTHORITY

Result: **13/13 PASS**

| Test | Result |
|---|---|
| T1 HOLD produces no portfolio action | PASS |
| T2 Candidate reduction maps to Leverage first | PASS |
| T3 portfolio composition changes mapping, not market target | PASS |
| T4 Core Preservation Gate retained | PASS |
| T5 explicit Core authority reaches target | PASS |
| T6 restoration starts with Core | PASS |
| T7 leverage restore authority remains separate | PASS |
| T8 missing exact risk multipliers remain DATA PARTIAL | PASS |
| T9 REDUCE never inverts into restoration | PASS |
| T10 RESTORE never inverts into reduction | PASS |
| T11 lagged portfolio execution respects Candidate step cap | PASS |
| T12 Fast V-rebound portfolio move capped at +20pp | PASS |
| T13 BLOCKED Candidate never executes portfolio action | PASS |

Boundary: these tests validate Candidate-to-portfolio execution integration only. They do not establish profitability, market-timing performance, provisional adoption, or official 3.2 integration.
