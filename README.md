# AI Market Master Dashboard 3.2

## Purpose
AI based market analysis dashboard.

## Current Stable Version
**AI Market Master Dashboard 3.2**

Dashboard 3.2 is the official stable version. Dashboard 3.1 is preserved as the previous-version backup/reference.

## Core Principle

- HTS Data Priority
- Evidence Based Decision
- Reliability > Speed
- Validation First
- Multi Engine Consensus

## Dashboard Structure

24 Engine Architecture

01 Executive Summary
02 Observation Engine
03 Evidence Engine
04 Leading Indicator Engine
05 Smart Money Engine
06 Global Liquidity Engine
07 Program Trading Engine
08 Sector Rotation Engine
09 Technical Analysis Engine
10 Elliott Wave Analysis
11 Ultra Short Engine
12 Short Term Engine
13 Mid Term Engine
14 Long Term Engine
15 AI Cycle Engine
16 Portfolio Analysis
17 Strategy Engine
18 Scenario Forecast Engine
19 Change Detection Engine
20 Validation Engine
21 Revision Engine
22 Final AI Decision
23 Dashboard Checklist
24 Intraday Position Tracking Engine

## Binance Global Futures Layer

### Purpose
Binance 공개 Read-only 시장 데이터를 기존 24 Engine에 공급하는 24시간 글로벌 선행·보조 데이터 레이어.

### Data Priority Rule
- HTS/KRX 데이터가 최종 판단 기준이다.
- Binance TradFi/Crypto 데이터는 선행 신호 및 교차검증용으로 사용한다.
- Binance 신호가 HTS 데이터와 충돌하면 HTS를 우선하고 Binance 신호의 신뢰도를 낮춘다.
- Binance 데이터만으로 포트폴리오의 공격적 매매 결정을 확정하지 않는다.
- Reliability > Speed 원칙을 유지한다.

### Fixed Watchlist
1. EWYUSDT — 한국 주식시장 선행
2. SAMSUNGUSDT — 삼성전자 글로벌 선행
3. SKHYNIXUSDT — SK하이닉스 글로벌 선행
4. SOXLUSDT — 미국 반도체 Risk Appetite
5. QQQUSDT — Nasdaq/성장주 Risk Appetite
6. SPYUSDT — 미국 전체시장 Risk-on/Off
7. TMFUSDT — 장기 미국채/금리 방향
8. BTCUSDT — 24시간 글로벌 Risk Appetite/Liquidity 보조

### Binance Data Inputs
가능한 범위에서 다음 Read-only 데이터를 사용한다.
- Current Price / 24h Change
- OHLCV Candles
- Volume
- Mark Price
- Index Price
- Premium Index
- Open Interest / OI Change
- Funding Rate
- Top Trader Long/Short Ratio
- Top Trader Account Long/Short Ratio
- Order Book
- Recent Trades
- ADL Risk

데이터가 특정 심볼에서 제공되지 않으면 해당 항목은 생략하고 가용 데이터만 사용한다. 데이터를 추정하거나 생성하지 않는다.

### Global Futures Sub-Engines

#### G1 Global Risk
SPYUSDT + QQQUSDT + BTCUSDT를 이용해 글로벌 Risk-on/Risk-off 방향을 판단한다.

#### G2 Semiconductor / AI Cycle
SOXLUSDT + SAMSUNGUSDT + SKHYNIXUSDT를 이용해 글로벌 반도체 및 AI 메모리 위험선호를 확인한다. 기존 AI Cycle Engine의 HBM, DRAM/NAND, CAPEX, AI 서버 수요 및 공급/재고 데이터와 교차검증한다.

#### G3 Korea Leading
EWYUSDT + SAMSUNGUSDT + SKHYNIXUSDT를 이용해 한국장 개장 전 한국 주식/반도체 선행 방향을 판단한다.

#### G4 Rates / Liquidity
TMFUSDT를 기존 미국채 금리, USD/KRW, 달러, VIX, Fed, 유가 등 Macro 데이터와 결합해 금리 및 유동성 환경을 판단한다.

#### G5 Crypto Risk
BTCUSDT를 24시간 글로벌 고베타 위험선호 및 유동성 보조지표로 사용한다. BTC 단독 움직임은 글로벌 주식 신호로 확정하지 않고 다른 Risk 지표와 교차검증한다.

#### G6 Futures Positioning
Price + Volume + OI + Funding + Premium + Mark/Index Price + Long/Short + Order Book/Trades를 결합해 포지션 유입, 청산, 과열 및 단기 수급 변화를 판단한다.

### Signal Flow
Binance Global Futures Layer → Global Risk / Semiconductor / Korea Leading / Rates-Liquidity / Crypto Risk / Futures Positioning → 기존 3.2 Engines → KRX HTS 교차검증 → AI Master Score / Strategy Action Index → Portfolio Strategy.

### Engine Integration
Binance Global Futures Layer의 결과는 다음 엔진을 중심으로 보조 입력한다.
- 04 Leading Indicator Engine
- 05 Smart Money Engine
- 06 Global Liquidity Engine
- 09 Technical Analysis Engine
- 11 Ultra Short Engine
- 15 AI Cycle Engine
- 16 Portfolio Analysis
- 17 Strategy Engine
- 18 Scenario Forecast Engine
- 19 Change Detection Engine
- 20 Validation Engine
- 22 Final AI Decision
- 24 Intraday Position Tracking Engine

### Interpretation Rules
- Price ↑ + OI ↑: 신규 포지션 유입 가능성. 방향은 Funding/Long-Short/가격 구조로 추가 확인.
- Price ↑ + OI ↓: 숏 청산 가능성. 신규 매수로 단정하지 않는다.
- Price ↓ + OI ↑: 신규 숏 유입 가능성. 추가 확인 필요.
- Price ↓ + OI ↓: 롱 청산/포지션 축소 가능성. 추가 확인 필요.
- Funding 과도한 양수/음수는 포지션 과열 가능성으로만 해석한다.
- Mark/Index/Premium 괴리는 선물시장 수급 및 괴리 확인용으로 사용한다.
- 모든 해석은 단일 지표가 아니라 Multi Engine Consensus를 우선한다.

### Portfolio Strategy Rules

#### Bullish Confirmation
Global Risk 상승 + Semiconductor 상승 + Korea Leading 상승 + KRX HTS 수급/가격 확인 시 현물 유지, 레버리지 유지 또는 조건부 확대를 검토한다.

#### Bullish but Overheated
반도체/한국 선행지표가 강하지만 RSI/Fibonacci 저항, OI 급증, Funding 과열, 거래량 급증, HTS 수급 둔화 등이 나타나면 상승 추세는 인정하되 레버리지를 우선 축소하고 분할매도를 검토한다.

#### Risk-off Transition
SPY/QQQ/SOXL/BTC/EWY 및 삼성전자/SK하이닉스가 동반 약세이고 HTS 외국인·기관·프로그램 매도까지 확인되면 레버리지를 우선 축소한다. 현물은 기술적 지지와 HTS 수급을 확인해 단계적으로 대응한다.

#### Leverage Priority
포트폴리오 리스크 조절 시 레버리지 자산을 현물보다 먼저 확대/축소한다. 상승 추세에서도 과열 신호가 누적되면 레버리지부터 분할 축소한다.

### Scoring Integration
Binance 데이터는 별도 점수를 만들기보다 Global Risk, Semiconductor, Korea Leading, Rates/Liquidity, Crypto Risk, Futures Positioning 신호로 변환한 후 기존 AI Master Score와 Strategy Action Index의 보조 입력으로 사용한다.

### Final Decision Rule
Binance = 선행/보조 신호.
KRX HTS = 최종 확인.
최종 포트폴리오 전략 = Binance + HTS + Technical + Smart Money + AI Cycle + Risk의 Multi Engine Consensus.

## Version
Current Version:
**AI Market Master Dashboard 3.2 — Official Stable**

Previous Version:
AI Market Master Dashboard 3.1 — Preserved Backup/Reference

Binance Global Futures Layer:
Fixed Watchlist v1.0 — 2026-08-19

Latest 3.2 Binance Engine execution standard:
2026-08-23
