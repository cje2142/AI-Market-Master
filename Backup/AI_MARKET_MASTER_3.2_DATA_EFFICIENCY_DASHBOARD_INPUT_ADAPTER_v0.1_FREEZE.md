# AI Market Master 3.2 — Data Efficiency Dashboard Input Adapter v0.1 Freeze

Date: 2026-09-18
Status: FROZEN RESEARCH INPUT CONTRACT / PROSPECTIVE VALIDATION ONLY

## Purpose
Add the minimum Candidate-specific inputs needed to eliminate the missing-data distortion observed in the first 2026-09-18 09:03 E2E sample.

This does NOT modify Official 3.2 Dashboard or Scoring Authority.

## New collection fields
The normal Dashboard already supplies:
- KOSPI return
- KOSDAQ return
- USD/KRW return

For Data Efficiency Candidate v0.1, collect three additional fields:
1. KOSPI200 return
2. KRX100 return
3. KTB3Y change in basis points

Canonical research field names:
- r_kospi200
- r_krx100
- d_ktb3y_bp

All market returns use decimal representation:
+2.36% -> 0.0236

KTB3Y is basis-point change:
+2bp -> 2.0

## Candidate calculations
C4:
- LC_RAW = average(KOSPI200, KRX100) - KOSPI
- N_LC = clip(LC_RAW/0.005, -1, +1)
- GR_RAW = KOSDAQ - KOSPI
- N_GR = clip(GR_RAW/0.015, -1, +1)
- C4 = 0.40*N_LC + 0.60*N_GR

C6:
- FX = -clip(r_USDKRW/0.008, -1, +1)
- KTB = -clip(dKTB3Y_bp/10, -1, +1)
- C6 = 0.50*FX + 0.50*KTB

## Completeness
C4 VERIFIED:
- KOSPI + KOSDAQ + KOSPI200 + KRX100

C4 PARTIAL:
- KOSPI + KOSDAQ + one large-cap candidate

C6 VERIFIED:
- USD/KRW + KTB3Y

C6 PARTIAL:
- exactly one of the two axes

## Runtime boundary
The adapter combines Official-derived C1/C2/C3/C5/C7 with Candidate-derived C4/C6 only for Data Efficiency research.

Official C4/C6 are not overwritten.

## Files
- Research/data_efficiency_dashboard_input_adapter_v0_1.py
- Research/test_data_efficiency_dashboard_input_adapter_v0_1.py

## Validation boundary
No inferred or guessed values are allowed.
If KOSPI200, KRX100 or KTB3Y is absent, the defined PARTIAL/DATA UNAVAILABLE rules apply.

Official 3.2 remains unchanged.
Data Efficiency Candidate v0.1 remains unchanged.
