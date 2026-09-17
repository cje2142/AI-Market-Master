# Compounding Overlay v0.3 — Top Drawdown Attribution

Status: Historical Proxy diagnostic only. No thresholds or strategy rules are changed by this analysis.
Period: 2006-01-02 ~ 2025-12-30 / cost 5bp per side

## Top drawdown episodes

| Peak → Trough | Hold price DD | v0.3 episode MDD improvement | First R5 | First Strong R5 | First 80% exposure | Min exposure | R8 after trough |
|---|---:|---:|---|---|---|---:|---|
| 2007-10-11 → 2008-10-24 | -52.9% | 8.8% | 2007-11-21 (-12.6%, final DD 23.8% realized) | 2008-01-29 (-20.3%, final DD 38.3% realized) | 2008-01-30 (-22.3%, final DD 42.1% realized) | 80.0% | 2008-12-22 (-41.2%, final DD 77.8% realized) |
| 2017-11-03 → 2020-03-19 | -41.2% | 10.0% | 2017-12-21 (-5.6%, final DD 13.7% realized) | 2018-02-07 (-8.4%, final DD 20.3% realized) | 2018-02-14 (-7.2%, final DD 17.5% realized) | 80.0% | 2020-04-23 (-25.1%, final DD 61.0% realized) |
| 2021-06-25 → 2022-09-30 | -36.1% | 2.4% | 2021-08-17 (-6.6%, final DD 18.3% realized) | 2022-02-04 (-16.8%, final DD 46.6% realized) | 2022-02-07 (-17.6%, final DD 48.7% realized) | 80.0% | 2022-10-26 (-33.3%, final DD 92.1% realized) |
| 2011-05-02 → 2011-09-26 | -27.5% | 2.2% | 2011-05-23 (-8.2%, final DD 29.8% realized) | 2011-08-04 (-11.4%, final DD 41.7% realized) | 2011-08-10 (-21.0%, final DD 76.5% realized) | 80.0% | 2011-10-17 (-17.6%, final DD 63.9% realized) |
| 2006-05-11 → 2006-06-13 | -18.3% | 9.0% | 2006-05-18 (-6.8%, final DD 37.4% realized) | 2006-06-07 (-13.7%, final DD 74.9% realized) | 2006-06-08 (-16.9%, final DD 92.3% realized) | 80.0% | 2006-07-06 (-14.1%, final DD 76.9% realized) |
| 2007-07-25 → 2007-08-17 | -17.9% | 4.0% | — | — | — | 90.0% | 2007-09-17 (-6.8%, final DD 37.9% realized) |

## Strong R5 follow-through diagnostic

- Strong R5 clustered episodes: 41
- Meaningful downside follow-through episodes: 14
- Follow-through ratio: 34.1%
- Diagnostic definition only: next-20d minimum <= -5% OR next-60d minimum <= -8%.

## Interpretation guide
- If first 80% exposure occurs after most of the final drawdown is already realized, the main defect is late defense rather than insufficient floor depth.
- If Strong R5 fires frequently without subsequent downside, the main defect is false-positive frequency / over-defense.
- If 80% is reached early but MDD improvement remains small, the 80% Historical Proxy floor itself limits maximum defense.
- This report diagnoses the frozen v0.3; it must not be used to silently retune v0.3 parameters.