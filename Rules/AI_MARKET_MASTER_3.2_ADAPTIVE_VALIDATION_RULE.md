# AI Market Master 3.2 Adaptive Validation Rule

Version: 3.2 Unified Stable
Status: Adaptive Validation / Market Regime Authority

## 1. Scope
This file is the official authority for:
- Market Regime Detection
- Regime Transition Detection
- Regime Adaptive Evidence Priority
- adaptive conflict resolution
- anti-double-counting across Evidence Groups
- Regime re-validation
- adaptive Validation / Revision integration
- qualitative Strategy posture derived from Market Regime

This file does NOT own numeric scoring, technical calculations, Binance freshness, Dashboard layout or final portfolio risk-reduction order.

## 2. Legacy Restore Boundary
The following concepts are restored from verified legacy design intent:
- Change Detection
- Validation
- Revision
- Final AI Decision
- Performance Validation concept
- Engine Reliability concept
- Confidence / closed-loop learning / Self-Evolution principle

Legacy sources did not establish a complete reproducible numeric formula for AI Master Score, Strategy Action Index or Engine Reliability weights.
Therefore this rule restores analytical behavior, not undocumented numeric weights.

## 3. 3.2 New Adaptive Application Boundary
The following are new 3.2 rule-based applications:
- 8 Market Regimes
- E1-E8 Evidence Groups
- VH/H/M/L Evidence Priority Matrix
- Primary Regime + Transition Regime
- Conditional Evidence Escalation
- adaptive Conflict Resolution
- Regime Re-validation
- qualitative Regime-to-Strategy posture

These new applications must never be described as recovered historical numeric formulas.

## 4. Market Regimes
R1 Broad Risk-On
R2 Concentrated Leadership Bull
R3 Rotation
R4 Distribution
R5 Risk-Off Transition
R6 Panic / High Volatility
R7 Deep Correction / Support Test
R8 Recovery / Accumulation

Every Full Dashboard should determine, when data is sufficient:
- Primary Market Regime
- Transition Regime / Transition Risk
- Regime Confidence: High / Medium / Low

If data is insufficient, use the existing Validation Status framework rather than inventing a Regime.

## 5. Regime Detection Axes
Evaluate at least three independent analytical axes:

### A. Price / Structure
- index direction
- trend structure
- MA / VWAP
- support / resistance
- breakout / rejection / breakdown
- volume

### B. Money Flow / Internal
- foreign spot
- foreign futures
- program / non-arbitrage
- breadth / ADL
- sector leadership / relative strength

### C. Risk / Environment
- volatility
- USD/KRW
- rates / liquidity
- derivatives risk
- verified official global-leading evidence
- Binance global-leading support when valid under BINANCE_RULE

A single indicator or single Evidence Group must not determine the Primary Market Regime.
Primary Regime normally requires support from at least two independent axes.

## 6. Regime Definitions
### R1 Broad Risk-On
Price structure bullish + money flow supportive + breadth broadening + multi-sector participation + risk environment stable/improving.
Core signature: price up + money up + participation broadening.

### R2 Concentrated Leadership Bull
Index strong + leadership concentrated in limited sectors/large caps + supportive flow + breadth weaker than index performance.
Core signature: index up + leaders much stronger + participation narrow.

### R3 Rotation
Index broadly stable or moderately directional + old leadership weakens + new leadership strengthens + breadth does not collapse + evidence favors capital rotation rather than market exit.

### R4 Distribution
Price remains high / near resistance / relatively firm while internal flow, breadth or program evidence deteriorates; volatility/rejection risk may rise.
Core signature: price still firm + internal evidence weakening.

### R5 Risk-Off Transition
Internal weakness is confirmed and begins to transmit into price-structure deterioration, support failure, foreign/program selling and worsening risk environment.

### R6 Panic / High Volatility
Sharp decline + volatility expansion + broad selling/breadth collapse + support failure and/or liquidity stress.
Risk control dominates normal sector-rotation interpretation.

### R7 Deep Correction / Support Test
Large correction has reached or approached major support; selling pressure may be slowing but bottom is not confirmed.
Support touch alone never confirms Recovery.

### R8 Recovery / Accumulation
Support stabilizes + Smart Money/Program improve + breadth recovers + price structure begins to stabilize/reclaim + leadership re-emerges.
Early Recovery favors spot confirmation before leverage expansion.

## 7. Evidence Groups
E1 Smart Money — foreign spot, foreign futures, institutional directional flow
E2 Program Flow — total program, arbitrage, non-arbitrage
E3 Breadth / Internal — advance/decline, ADL, participation breadth
E4 Sector / Leadership — sector rotation, relative strength, leadership concentration/expansion
E5 Technical Structure — price structure, MA/VWAP, volume, support/resistance, momentum, Elliott/Fibonacci context
E6 Liquidity / Macro — USD/KRW, rates, deposits, margin/credit, liquidity conditions
E7 Volatility / Derivatives Risk — volatility, options, OI and derivatives-risk structure
E8 Global Leading — verified official global leading plus Binance G1-G6 / EWY / SOXL / QQQ-SPY / BTC / TMF when valid

## 8. Anti-Double-Counting Rule
The same underlying datum must not be counted as independent confirmation across multiple Evidence Groups.

Examples:
- ADL / advance-decline is counted in E3 for adaptive confirmation. E5 may reference it contextually but must not count it again as an independent Technical confirmation.
- Program / non-arbitrage is counted in E2 for adaptive confirmation. E1 may discuss it contextually but must not count it again as an independent Smart Money confirmation.

Independent confirmation means independent Evidence Groups or genuinely independent source evidence, not multiple derivatives of the same underlying datum.

## 9. Evidence Priority Levels
Use qualitative priority only:
- VH — Very High Priority
- H — High Priority
- M — Medium Priority
- L — Low Priority

These are analytical-priority labels, not numeric weights, percentages, probabilities, scores or Strategy Action Index values.

## 10. Regime Adaptive Evidence Priority Matrix
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

## 11. Conditional Evidence Escalation
A verified abnormal condition that directly threatens the current Regime may promote the affected Evidence Group by one priority level.
Examples:
- price up + volatility sharply up → E7 escalation
- index strength + breadth collapse → E3 escalation
- bullish structure + foreign futures sharp sell reversal → E1 escalation

Normal maximum escalation is one level.
Extreme Risk conditions use MASTER_RULE risk-control logic instead of normal escalation.

## 12. Preliminary Regime / Anti-Circularity
The system must not:
1. choose a Regime,
2. raise evidence priority because of that Regime,
3. use the raised priority as the sole reason to reconfirm the same Regime.

Required adaptive flow:
Data Validation → Base Evidence Analysis → Preliminary Market Regime → Regime Adaptive Evidence Priority → Change / Transition Detection → Conflict Resolution → Cross-Engine Consensus → Regime Re-validation → Revision → Final AI Decision.

Independent evidence must survive Regime Re-validation.

## 13. Transition Framework
Use:
- Transition Watch — next-Regime evidence appears but current Regime remains primary
- Transition Confirming — at least two independent axes support next Regime
- Regime Change — next Regime survives adaptive-priority review and re-validation
- Strong Regime Confirmation — broad alignment across price, flow/internal and risk/environment axes

A verified Regime Transition may be strategically more important than the static Primary Regime.

## 14. Conflict Resolution Order
When material evidence conflicts, do not use simple Bull/Bear signal counting.
Resolve in this order:
1. Data Authority
2. Regime-relevant Evidence Priority
3. Independent Confirmation
4. Data Quality / Freshness
5. Transition Significance
6. Price Confirmation

HTS/KRX remains final confirmation for Korean-market judgment under MASTER_RULE.
Binance cannot override verified HTS/KRX by itself.

## 15. Same-Priority Conflict
When VH/H Evidence Groups materially conflict:
- disclose the conflict
- preserve Primary Signal only if supported by independent evidence
- assess Transition implication
- reduce Confidence when conflict is decision-relevant
- specify Next Validation Condition

Do not force a directional conclusion merely because one side has more raw indicators.

## 16. Price vs Internal Conflict
### Price Strong / Internal Weak
Do not immediately classify Risk-Off.
Evaluate Distribution Transition Risk, especially near major resistance or after extended gains.

### Price Weak / Internal Improving
Do not immediately declare Recovery.
Use Support Test / Recovery Transition Watch until price stabilization or reclaim confirms.

## 17. Smart Money Conflict
Foreign Futures has higher short-term transition sensitivity.
Foreign Spot has stronger structural confirmation value.
If they diverge, require Program and Price confirmation before strong action.

## 18. Program Conflict
For structural interpretation, persistent Non-Arbitrage deterioration has greater significance than temporary arbitrage fluctuations.
Strong arbitrage buying must not hide persistent non-arbitrage selling.

## 19. Breadth Conflict
Index strength + weak breadth = concentration/divergence warning.
Index weakness + improving breadth = possible internal stabilization.
Breadth divergence alone does not finalize portfolio action but may escalate Transition Risk.

## 20. Technical Conflict
Technical indicators must not be resolved by indicator counting.
Within E5 prioritize:
1. Price Structure
2. Support / Resistance
3. MA / VWAP
4. Volume
5. Momentum
6. Elliott / Fibonacci context

Momentum cannot override confirmed price-structure failure by itself.
TECHNICAL_RULE remains calculation authority.

## 21. Minimum Confirmation
Ordinary directional Judgment normally requires at least two independent Evidence Groups when available.
Strong Strategy change normally requires:
- confirmed/current Regime or confirmed Transition
- at least three independent high-priority Evidence Groups aligned
- technical location consistent
- portfolio risk/exposure assessed
- no unresolved major data conflict

Extreme Risk conditions may invoke faster risk control under MASTER_RULE.

## 22. Confidence Adjustment
Material conflict among high-priority Evidence Groups may reduce:
High → Medium
Medium → Low

Do not reduce Confidence merely because low-priority evidence disagrees.
Confidence remains non-numeric and is governed by MASTER/DASHBOARD rules.

## 23. Validation / Revision / Engine Reliability Restoration
Validation must include, when data permits:
- data/source consistency
- flow consistency
- technical consistency
- scenario/forecast logic consistency
- conflict review
- outcome review when a prior validated expectation is actually available

Legacy Engine Reliability remains a qualitative validation concept unless persistent validated history and an official formula exist.
Do not fabricate historical reliability when prior validated outcomes are unavailable.

Revision may update:
- Preliminary / Primary Market Regime
- Transition status
- scenario
- Confidence
- Strategy posture
- Final AI Decision

Numeric AI Master Score / Strategy Action Index may be revised only when SCORING_RULE formally activates a reproducible formula.

## 24. Qualitative Strategy Postures
Use only qualitative Strategy states:
- Defensive Observation
- Hold
- Constructive Hold
- Accumulation
- Risk Reduction Watch
- Staged Reduction
- Strong Risk Reduction
- Extreme Risk Control

Do not prefix these with A1-A8 or convert them into numbers.
They are not Strategy Action Index values.

Default Market Regime posture:
- Broad Risk-On → Constructive Hold / Accumulation
- Concentrated Leadership Bull → Hold / Constructive Hold
- Rotation → Selective Hold / Constructive Hold
- Distribution → Risk Reduction Watch / Staged Reduction
- Risk-Off Transition → Staged Reduction / Strong Risk Reduction
- Panic / High Volatility → Strong Risk Reduction / Extreme Risk Control
- Deep Correction / Support Test → Defensive Observation / Hold
- Recovery / Accumulation → Constructive Hold / Accumulation

Regime never creates an automatic trade.

## 25. Portfolio Response Framework Boundary
Market Regime describes the market environment.
Portfolio Response Framework describes how the user's portfolio should respond after considering:
- Market Regime
- Transition
- Evidence Priority / conflict
- Technical location
- portfolio leverage/exposure/concentration
- MASTER_RULE risk-reduction priority

The same Market Regime may produce different portfolio actions for low-risk versus high-risk portfolios.

## 26. Full Adaptive Execution Chain
Data Validation
→ Base Evidence Analysis
→ Preliminary Market Regime
→ Regime Adaptive Evidence Priority
→ Change / Transition Detection
→ Conflict Resolution
→ Cross-Engine Consensus
→ Regime Re-validation
→ Validation
→ Revision
→ Final AI Decision
→ Portfolio Response Framework
→ Final Portfolio Action

## 27. Scoring Firewall
This rule must never activate numeric AI Master Score or Strategy Action Index.
VH/H/M/L must not be converted to 4/3/2/1, percentages, weighted averages or hidden numeric calculations.
SCORING_RULE is the sole numeric scoring authority.

## 28. Dashboard Mapping
Do not create a ninth Dashboard category.
Recommended mapping:
- Evidence Priority / Change Detection → Evidence
- Primary Regime / Transition / Conflict / Regime Confidence → Judgment
- regime-relevant sector/AI leadership → AI Cycle
- Smart Money priority evidence → Smart Money
- liquidity/risk evidence → Liquidity
- technical confirmation/invalidation → Technical
- Validation / Revision / Portfolio Response / Final Action → Strategy

## 29. Final Principle
Market Regime sets analytical context.
Evidence Priority identifies what matters most in that context.
Conflict is information, not noise to hide.
Validation determines whether the Regime remains valid.
Portfolio context determines response intensity.

Reliability > Signal Count.
Validation First.
No official numeric formula = no official numeric score.
