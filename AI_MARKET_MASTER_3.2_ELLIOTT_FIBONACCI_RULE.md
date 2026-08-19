# AI Market Master Dashboard 3.2 — Elliott & Fibonacci Engine Rule

## Purpose

This rule defines the fixed Fibonacci framework used by the Elliott Wave Engine in AI Market Master Dashboard 3.2.

The engine must always evaluate TWO Fibonacci axes simultaneously:

1. **Long-Term Retracement Axis:** Major High 9,114 → Major Low 2,293
2. **Recovery Fibonacci Axis:** Correction Low 5,593 → Major High 9,114

These two axes must not be confused or substituted for one another.

---

## 1. Fixed Elliott Reference Values

- Major Low = **2,293**
- Major High = **9,114**
- Correction Low = **5,593**

These values remain fixed until the user explicitly changes them.

Correction Low 5,593 replaces the former 6,516 and must be used for all subsequent Elliott/Fibonacci analysis unless the user changes it.

---

# 2. Fibonacci Axis A — Long-Term Retracement

### Direction

**Major High 9,114 = 0%**

**Major Low 2,293 = 100%**

This is a **retracement/downside-depth axis**, not a recovery axis.

### Fixed levels

| Fibonacci | KOSPI |
|---:|---:|
| 0% | 9,114 |
| 23.6% | 7,505 |
| 38.2% | 6,509 |
| 50.0% | 5,704 |
| 61.8% | 4,898 |
| 78.6% | 3,902 |
| 100% | 2,293 |

### Purpose

Determine how deeply the market has retraced from the Major High relative to the complete 2,293 → 9,114 long-term cycle.

### Interpretation

- Around 23.6% = shallow long-term correction
- Around 38.2% = normal/important long-term retracement
- Around 50.0% = medium-depth structural correction
- Around 61.8% = deep retracement / major structural test
- 78.6% = very deep retracement
- 100% = complete retracement to Major Low

The engine must not call a Fibonacci level a confirmed support merely because price touches it. Price action, volume, HTS flow and Elliott structure must confirm it.

---

# 3. Fibonacci Axis B — Recovery Fibonacci

### Direction

**Correction Low 5,593 = 0%**

**Major High 9,114 = 100%**

This is the **recovery-progress axis**.

### Fixed levels

| Recovery | KOSPI |
|---:|---:|
| 0% | 5,593 |
| 23.6% | 6,424 |
| 38.2% | 6,938 |
| 50.0% | 7,354 |
| 61.8% | 7,770 |
| 78.6% | 8,359 |
| 100% | 9,114 |

### Purpose

Determine how far the market has recovered from the Correction Low toward the Major High.

### Interpretation

- 23.6% = initial recovery confirmation zone
- 38.2% = first important medium-term recovery level
- 50.0% = halfway recovery
- 61.8% = strong recovery / major confirmation zone
- 78.6% = near-complete recovery
- 100% = Major High recovery

A recovery level is not automatically a price target. It must be evaluated with Elliott structure, momentum and money flow.

---

# 4. Mandatory Dual-Axis Analysis

Every Elliott/Fibonacci analysis must calculate both axes.

For the current index, report:

1. Position on Long-Term Retracement Axis
2. Position on Recovery Fibonacci Axis
3. Distance to the next major level on each axis
4. Whether the two axes form a Confluence Zone
5. Elliott Wave interpretation
6. Confirmation/invalidation conditions

Do not report only one Fibonacci framework.

---

# 5. Current Example — KOSPI 6,471.17

Using the 2026-08-19 HTS close:

### Long-Term Retracement

9,114 → 2,293 framework:

- 38.2% = approximately **6,509**
- Current = **6,471.17**
- Therefore the index is slightly below the 38.2% long-term retracement level.

Approximate current long-term retracement depth:
**(9,114 - 6,471.17) / (9,114 - 2,293) ≈ 38.75%**

### Recovery

5,593 → 9,114 framework:

- 23.6% = approximately **6,424**
- Current = **6,471.17**
- Therefore the index is slightly above the 23.6% recovery level.

Approximate recovery progress:
**(6,471.17 - 5,593) / (9,114 - 5,593) ≈ 24.94%**

### Current Confluence

The current index is between approximately:

**6,424 Recovery 23.6%**

and

**6,509 Long-Term 38.2% Retracement**

This area is treated as a **dual-axis Fibonacci verification zone**.

It is not automatically a buy zone.

---

# 6. Elliott Wave Integration

Fibonacci must be interpreted together with Elliott Wave structure.

The engine must distinguish:

- Confirmed Wave Count
- Preferred Wave Count
- Alternative Wave Count
- Unconfirmed/insufficient evidence

The 5,593 Correction Low must be treated as the fixed starting point for the current recovery analysis until the user changes it.

The engine must not automatically declare the 5,593 → current recovery to be a new impulse wave. It must first evaluate:

- Swing structure
- Higher highs / higher lows
- Momentum
- Volume
- Foreign/institution/program flow
- Global leading signals
- MA/VWAP structure
- Breakout/rejection behavior

---

# 7. Dynamic Swing Fibonacci

The two fixed axes above are mandatory and must always be shown.

A third **Dynamic Swing Fibonacci** may be calculated from confirmed recent swing points when sufficient HTS data is available.

Rules:

1. Use confirmed swing points rather than arbitrary intraday extremes.
2. Elliott structure must support the chosen swing points.
3. Do not silently replace the fixed 2,293 / 9,114 / 5,593 axes with dynamic swings.
4. Clearly label Dynamic Fibonacci separately.
5. If the swing is not sufficiently confirmed, label it **Observation Swing**, not Confirmed Swing.

---

# 8. Fibonacci Confluence Rule

A Fibonacci level becomes a meaningful Confluence Zone only when supported by independent evidence.

Possible confirming factors:

- Elliott Wave structure
- Moving Average
- VWAP
- Previous high/low
- Volume concentration
- RSI/MACD divergence
- ADX/trend condition
- Foreign flow
- Institutional flow
- Program trading
- Futures/options positioning
- Binance Global Leading signals

### Classification

- 1 factor = Fibonacci reference only
- 2 factors = Potential Confluence
- 3+ independent factors = High-Confluence Zone

Never treat Fibonacci alone as a trading trigger.

---

# 9. Support / Resistance Decision Rule

For each major Fibonacci level, state:

- Level
- Current distance
- Support or resistance role
- Evidence supporting the level
- Confirmation trigger
- Invalidation trigger

A level changes role after a confirmed breakout/breakdown and successful retest where applicable.

---

# 10. Strategy Connection

Fibonacci output feeds the Strategy Engine but does not independently determine portfolio action.

### Recovery strengthening

If price:
- holds above Recovery 23.6%,
- reclaims Long-Term 38.2%,
- and HTS/global flow improves,

then recovery probability increases.

### Recovery weakening

If price:
- loses Recovery 23.6%,
- remains below Long-Term 38.2%,
- and foreign/program selling remains strong,

then the recovery is considered technically weak and the next Fibonacci supports must be monitored.

### Structural risk

If price approaches/loses the 5,593 Correction Low:

- reassess the entire Elliott count,
- reassess the Recovery Fibonacci axis,
- do not continue using the previous recovery interpretation as if nothing changed.

If 5,593 is decisively broken, the engine must flag **Recovery Structure Failure / Elliott Recount Required**.

---

# 11. Required Dashboard Output

The Elliott & Fibonacci section must contain, at minimum:

### A. Long-Term Retracement
`9,114 → 2,293`

- Current level
- Current retracement percentage
- Key Fibonacci levels
- Current support/resistance interpretation

### B. Recovery Fibonacci
`5,593 → 9,114`

- Current recovery percentage
- Current recovery level
- Next recovery level
- Key support/resistance interpretation

### C. Dual-Axis Confluence

- Overlapping/nearby Fibonacci levels
- Strength of confluence
- HTS/technical/flow confirmation

### D. Elliott Wave

- Preferred count
- Alternative count if necessary
- Confirmation trigger
- Invalidation trigger

### E. Portfolio Relevance

- Whether the current zone favors holding, leverage reduction, staged re-entry, or waiting
- Never use Fibonacci alone as the portfolio trigger

---

# 12. Core Rule — DO NOT BREAK

**The Elliott & Fibonacci Engine must always analyze the market from both directions:**

> **Long-Term Retracement:** 9,114 → 2,293
>
> **Recovery Progress:** 5,593 → 9,114

The first measures **how much of the long-term rise has been retraced**.

The second measures **how much of the recent correction has been recovered toward the previous high**.

Both are required for every full dashboard execution.

Final principle:

**Fixed reference → Dual Fibonacci → Elliott structure → Technical Confluence → HTS Flow Confirmation → Scenario → Strategy**

Version: AI Market Master Dashboard 3.2
Date: 2026-08-19
