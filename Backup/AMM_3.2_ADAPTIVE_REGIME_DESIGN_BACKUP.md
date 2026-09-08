# AI Market Master 3.2 Adaptive Regime Design Backup

Status: 3.2 New Design Reference / Non-Authoritative
Purpose: Preserve the newly designed rule-based adaptive framework separately from restored legacy rules.

## 1. Design Boundary
This file is NOT a historical 3.0/3.1 rule recovery.
It is a new 3.2 application inspired by the legacy Validation / Revision / Engine Reliability philosophy.

The framework avoids dependence on persistent historical backtesting state by using current Market Regime to change evidence priority.

## 2. Market Regimes
R1 Broad Risk-On
R2 Concentrated Leadership Bull
R3 Rotation
R4 Distribution
R5 Risk-Off Transition
R6 Panic / High Volatility
R7 Deep Correction / Support Test
R8 Recovery / Accumulation

Each execution may show:
- Primary Market Regime
- Transition Regime / Transition Risk
- Regime Confidence: High / Medium / Low

A static Primary Regime must not hide a strengthening transition.

## 3. Regime Detection Axes
At minimum evaluate three independent axes:
A. Price / Structure: index direction, MA/VWAP, support/resistance, trend, volume
B. Money Flow / Internal: foreign spot/futures, program, breadth/ADL, sector leadership
C. Risk / Environment: volatility, USD/KRW, rates/liquidity, verified global-leading evidence

Primary Regime normally requires confirmation across at least two independent axes.
One indicator must not determine the Regime.

## 4. Evidence Groups
E1 Smart Money: foreign spot, foreign futures, institutional directional flow
E2 Program Flow: total program, arbitrage, non-arbitrage
E3 Breadth / Internal: advance/decline, ADL, market participation/spread
E4 Sector / Leadership: leadership, relative strength, rotation
E5 Technical Structure: price, MA/VWAP, volume, support/resistance, momentum, Elliott/Fibonacci context
E6 Liquidity / Macro: USD/KRW, rates, deposits, credit/margin, liquidity conditions
E7 Volatility / Derivatives Risk: volatility, options, OI and derivatives-risk structure
E8 Global Leading: Binance G1-G6, EWY, SOXL, QQQ/SPY, BTC, TMF and other verified global-leading data

## 5. Evidence Priority Levels
VH = Very High Priority
H = High Priority
M = Medium Priority
L = Low Priority

VH/H/M/L are qualitative evidence-priority labels only.
They are NOT numeric weights, percentages, scores or Strategy Action Index values.

## 6. Regime Adaptive Evidence Priority Matrix
| Market Regime | E1 Smart | E2 Program | E3 Breadth | E4 Sector | E5 Technical | E6 Liquidity | E7 Risk/Vol | E8 Global |
|---|---|---|---|---|---|---|---|---|
| Broad Risk-On | VH | H | VH | H | H | M | M | H |
| Concentrated Leadership Bull | VH | H | VH | VH | H | M | M* | H |
| Rotation | H | H | H | VH | H | M | M | M |
| Distribution | VH | VH | VH | H | VH | H | H | M |
| Risk-Off Transition | VH | VH | H | M | VH | VH | H | H |
| Panic / High Volatility | VH | H | VH | L | H | VH | VH | H |
| Deep Correction / Support Test | H | H | H | M | VH | H | H | M |
| Recovery / Accumulation | VH | VH | VH | H | H | H | M | H |

* In Concentrated Leadership Bull, E7 may be promoted from M to H when verified price-volatility divergence or abnormal derivatives risk directly threatens the Regime.

## 7. Conditional Evidence Escalation
A verified abnormal condition that directly threatens the current Regime may promote the affected Evidence Group by one level.
Examples:
- Price up + volatility sharply up → E7 escalation
- Index strength + breadth collapse → E3 escalation
- Bullish structure + foreign futures sharp sell reversal → E1 escalation

Normal escalation maximum: one level.
Extreme Risk conditions may invoke MASTER risk-control rules instead of normal escalation.

## 8. Anti-Double-Counting
The same underlying data must not be counted as independent confirmation across multiple Evidence Groups.
Examples:
- ADL / advance-decline belongs to E3 for adaptive confirmation; Technical may reference it but must not count it again as an independent E5 confirmation.
- Program / non-arbitrage belongs to E2 for adaptive confirmation; Smart Money may discuss it but must not count it again as an independent E1 confirmation.

## 9. Preliminary Regime and Anti-Circularity
Execution must not select a Regime, increase evidence priority because of that Regime, and then use that increased priority as the sole reason to reconfirm the same Regime.

Required sequence:
Data Validation → Base Evidence Analysis → Preliminary Regime → Adaptive Evidence Priority → Change / Transition Detection → Conflict Resolution → Cross-Engine Consensus → Regime Re-validation → Revision → Final AI Decision.

## 10. Conflict Resolution
Do not resolve conflict by simple Bull/Bear signal count.
Priority order:
1. Data Authority
2. Regime-relevant Evidence Priority
3. Independent confirmation
4. Data Quality / Freshness
5. Transition significance
6. Price confirmation

Important same-priority conflicts must be disclosed and may lower Confidence.

## 11. Minimum Confirmation
- Ordinary directional judgment: at least two independent Evidence Groups when available.
- Strong portfolio-strategy change: normally at least three independent high-priority Evidence Groups plus technical location and portfolio-risk validation.
- One Evidence Group alone cannot normally finalize major portfolio action.
- Extreme Risk conditions remain governed by MASTER risk controls.

## 12. Transition Rules
Transition Watch: emerging next-Regime evidence, current Regime maintained.
Transition Confirming: at least two independent axes support the next Regime.
Regime Change: next Regime survives adaptive-priority review and re-validation.
Strong Confirmation: broad alignment across price, flow/internal and risk/environment evidence.

A verified transition may be strategically more important than a still-valid static Primary Regime.

## 13. Qualitative Strategy Postures
No A1-A8 numeric labels are used.
Official qualitative postures:
- Defensive Observation
- Hold
- Constructive Hold
- Accumulation
- Risk Reduction Watch
- Staged Reduction
- Strong Risk Reduction
- Extreme Risk Control

These are qualitative Strategy states, not Strategy Action Index values.

Default Regime posture:
- Broad Risk-On → Constructive Hold / Accumulation
- Concentrated Leadership Bull → Hold / Constructive Hold
- Rotation → Selective Hold / Constructive Hold
- Distribution → Risk Reduction Watch / Staged Reduction
- Risk-Off Transition → Staged Reduction / Strong Risk Reduction
- Panic / High Volatility → Strong Risk Reduction / Extreme Risk Control
- Deep Correction / Support Test → Defensive Observation / Hold
- Recovery / Accumulation → Constructive Hold / Accumulation

Regime never creates an automatic trade. Final action also requires transition, evidence, technical location and portfolio exposure/risk.

## 14. Portfolio Response Boundary
Market Regime describes the market.
Portfolio Response Framework describes how the user's portfolio should respond.
Do not use overlapping names to imply they are the same layer.

Core spot preservation and risk-reduction priority remain owned by MASTER_RULE.

## 15. Scoring Boundary
This framework does not activate AI Master Score or Strategy Action Index.
No VH/H/M/L conversion to 4/3/2/1, percentages or hidden numeric weight is permitted unless SCORING_RULE later adopts a fully reproducible formula.

## 16. Final Design Principle
Market Regime sets analytical context.
Evidence Priority identifies what matters most in that context.
Validation and conflict resolution determine whether the Regime remains valid.
Portfolio context determines response intensity.
Reliability > Signal Count.
