# AI Market Master Dashboard 3.2

## Command Trigger Standard

### Full Dashboard Trigger

- Exact command: `AI Market Master 3.2 Dashboard 실행`
- This exact command is the official trigger for the full AI Market Master Dashboard 3.2 workflow.
- The full workflow must apply the 3.2 fixed dashboard layout, HTS Data Priority, Validation First, and Multi Engine Consensus rules.
- Similar or abbreviated phrases must not be treated as an exact trigger and must not silently execute the full Dashboard workflow.

### Binance Engine Trigger

- Exact command: `AI Market Master 3.2 Binance Engine 실행`
- This exact command is the official trigger for the Binance Engine workflow defined below.
- Similar or abbreviated phrases must not be treated as an exact trigger and must not silently execute the Binance Engine workflow.

## Binance Engine Execution Standard

- `AI Market Master 3.2 Binance Engine 실행`은 지정된 8개 대표종목 전체를 기본 분석한다.
- 대표종목: EWYUSDT / SAMSUNGUSDT / SKHYNIXUSDT / SOXLUSDT / QQQUSDT / SPYUSDT / TMFUSDT / BTCUSDT
- 각 종목은 가능한 범위에서 Price, OHLCV, Volume, OI, Funding, Long/Short, Top Trader, Premium, Order Book, Recent Trades, ADL Risk를 확인한다.
- 종목별 분석 → Global Leading Consensus → 국내시장/HTS 교차검증 순서로 판단한다.
- 특정 종목을 명시한 경우에만 단일종목 분석으로 전환한다.
- 데이터가 없는 항목은 추정하지 않고 `DATA UNAVAILABLE`로 표시한다.
- 일부 종목만 조회된 경우 `PARTIAL CONSENSUS`로 명시한다.
- 최종 판단은 AI Master Score와 Strategy Action Index에 반영한다.
