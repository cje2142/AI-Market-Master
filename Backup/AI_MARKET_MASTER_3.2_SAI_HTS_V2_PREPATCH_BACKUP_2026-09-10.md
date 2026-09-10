# AI Market Master 3.2 — SAI HTS-Operational v2 Pre-patch Backup

Date: 2026-09-10
Status: NON-AUTHORITATIVE / PRE-PATCH / RECOVERY CHECKPOINT
Purpose: Preserve the current v1 scoring state before redesigning C1-C8 around the user's repeatably available HTS dataset.

## 1. Pre-patch official state
- Strategy Action Index v1: FORMULA ACTIVATED / runtime data-dependent.
- AI Master Score: DATA UNAVAILABLE.
- Six official Authority files remain unchanged in count.
- 24 Analysis Engines / 8 Dashboard categories remain unchanged.

Current blob SHAs before v2 patch:
- MASTER_RULE: `ea746bf62edbf61521dd26d1855d3b4aadc7b951`
- DASHBOARD_RULE: `0ec39d1418edf09098a7a431e904fc5bdfd60230`
- SCORING_RULE: `d19716d947ac3d4c00627398cf6d8699192fb4d6`
- TECHNICAL_RULE: `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f`
- BINANCE_RULE: `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d`
- ADAPTIVE_VALIDATION_RULE: `8833555b261e334b6b0f39d4ce272776fd97af71`
- VERSION_STATUS: `5429cc217ca8e4014c1ca3fdbc59db1badbb7ef9`
- CHANGELOG: `8432396f1d93c4bc313936badc7c31bfedd17e14`

## 2. Reason for redesign
The v1 formulas were structurally reproducible but several mandatory inputs were not repeatably available in the user's actual HTS export: C1 futures/OI normalization, C4 eight sector benchmark set, C5 HH/HL + formal support/resistance inputs, C6 5-day FX/rate history, C7 VKOSPI MA20 + fair basis, and C8 Binance-proxy numeric dependence.

The v2 objective is not to loosen truth standards. It is to make the official numeric components use data the user can repeatedly export from HTS while keeping missing-data, anti-double-counting, conflict, shock, mechanical-event and anti-circularity safeguards.

## 3. Repeatably available HTS input family
Observed available fields include:
- KOSPI/KOSDAQ advance/decline/unchanged counts
- arbitrage and non-arbitrage program net flow
- KOSPI/KOSPI100/KOSPI200/KTOP30/KOSDAQ/KOSDAQ150/KRX100 returns and traded value
- VKOSPI current level and daily change
- KOSPI200 futures current price/return/OI; one Call/Put strike; KOSDAQ futures; volatility futures
- global HTS market panel: mini S&P500, mini Nasdaq, Nikkei, Shanghai, Hang Seng, Shenzhen, prior US indices, SOX, DAX/CAC, USD/KRW, KTB3Y, CD91, WTI, Gold
- investor flow panel: Individual/Foreign/Institution cash and futures plus options/stock-futures/dollar-futures context
- customer deposits, receivables, margin credit and futures deposits time series
- KOSPI OHLC, MA5/20/50/60/200, VWAP20/50/60/200, volume averages, RSI9, MACD, signal/oscillator, ADX, ADL

## 4. v2 design direction to be patched
- C1: foreign cash/futures directional-share model using the participant panel; no contract/OI unit mixing.
- C2: traded-value-normalized arbitrage/non-arbitrage with wider operational saturation and non-arbitrage priority.
- C3: same advance/decline structure with moderately more responsive breadth normalization.
- C4: numeric Market Leadership/Rotation from recurring KOSPI-family vs KOSDAQ-family relative returns; sector detail remains qualitative E4 context.
- C5: recurring technical structure from MA/VWAP Trend Position + RSI/MACD Momentum + OHLC Session Structure; ADX/volume remain confirmation.
- C6: daily USD/KRW + KTB3Y/CD91 rate pressure + five-observation Customer Deposit trend.
- C7: daily VKOSPI change + KOSPI200 futures-vs-spot return lead; raw basis/OI/single-strike options/vol futures remain context.
- C8: HTS global panel becomes primary numeric source: current US futures + prior US close + SOX + Asia; Binance remains supporting/confirmation under BINANCE_RULE rather than mandatory C8 numeric input.
- Global SAI base weights remain 18/12/15/10/20/10/8/7 unless regression reveals a structural conflict.

## 5. Calibration boundary
All v2 normalizers, shocks and Action Bands are rule-design calibrations. They are not claimed to be empirically optimal until an out-of-sample market backtest exists.

Reliability > Speed.
Missing != Neutral.
HTS/KRX final Korean-market confirmation remains binding.