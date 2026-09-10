# AI Market Master 3.2 — SAI / Adaptive Design Pre-patch Backup

- 작성일: 2026-09-10 (Asia/Seoul)
- 저장소: https://github.com/cje2142/AI-Market-Master
- 기준 브랜치: `main`
- Pre-patch 기준 Commit SHA: `3d51641df48b264d1068ca17508a363af9b82151`
- 상태: **NON-AUTHORITATIVE / DESIGN SNAPSHOT / NUMERIC SAI NOT ACTIVATED**
- 범위: 이 백업 파일 1개 생성. 공식 Rules, VERSION_STATUS, CHANGELOG 개정 및 실제 산식 설계·실행은 다음 단계다.
- 설계 근거: ChatGPT 대화 “AI Market Master 규칙 확인” (`6a8fb4f3-ef10-83e9-a7c2-27677eae98fb`), 특히 최종 중복·충돌 정리 응답 `87ce6cb4-3353-4e26-87b2-494f3d8281a9`. 이전 제안과 충돌하면 최종 정리를 적용한다.
- 사실 근거: 위 커밋에 고정하여 실제로 다시 읽은 6개 Authority 및 VERSION_STATUS/CHANGELOG. 대화의 축약 SHA를 그대로 신뢰하지 않고 전체 SHA를 확인했다.

## 1. 비권위 및 복구 경계

Rules = 공식 권위. Backup = 설계·복구·회귀검증 참고.
이 문서는 7번째 Authority가 아니며, 규칙 개정·숫자 점수 활성화·시장모델 자동 편입 권한을 부여하지 않는다.
“확정 설계”는 백업할 설계 방향을 뜻하며 현재 공식 규칙에 이미 적용되었다는 뜻이 아니다.
현재 원문과 충돌하는 경우 해당 범위의 Rules 원문이 우선한다.

이 백업은 설계 내용과 Git 복구 기준점을 보존하는 manifest다. 6개 원문 전체를 내장한 오프라인 아카이브는 아니다.
복구 또는 비교 시 아래 고정 커밋의 경로에서 원문을 읽고 Git blob SHA를 대조한다. 최신 main을 과거 원문 대신 사용하지 않는다.
실제 복구·덮어쓰기는 이 단계에서 수행하지 않는다.

## 2. 현재 6 Authority 구조 및 확인된 SHA

아래 SHA는 파일 내용의 **Git blob SHA**이며 저장소 commit SHA와 구분한다.

| Authority 경로 / 고정 원문 링크 | 소유 범위 | 확인된 Git blob SHA |
|---|---|---|
| [Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_MASTER_RULE.md) | 통합·24 Engine·실행·데이터·포트폴리오·완료 기준 | `ea746bf62edbf61521dd26d1855d3b4aadc7b951` |
| [Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_DASHBOARD_RULE.md) | 정확한 Trigger·고정 8 Dashboard·표시 | `0ec39d1418edf09098a7a431e904fc5bdfd60230` |
| [Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_SCORING_RULE.md) | 숫자 산식·입력·정규화·가중치·Missing/Partial·활성화 | `a4ac88c940e00fc4aacfee6b76979887c7433d1f` |
| [Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_TECHNICAL_RULE.md) | Elliott/Fibonacci 및 기술 계산 | `b0cb7dca80a5d7c7ccbab8e4157bf7cefb354f3f` |
| [Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_BINANCE_RULE.md) | Binance 8 Symbol·G1–G6·해석·Freshness/Fallback | `f9956ea5bb718fd1a866838fcfd6ce20a7bfcd7d` |
| [Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md](https://github.com/cje2142/AI-Market-Master/blob/3d51641df48b264d1068ca17508a363af9b82151/Rules/AI_MARKET_MASTER_3.2_ADAPTIVE_VALIDATION_RULE.md) | Regime·E1–E8·정성 우선순위·Transition·충돌·재검증 | `8833555b261e334b6b0f39d4ce272776fd97af71` |

보조 상태 파일은 Authority 수에 포함하지 않는다.

| 파일 | 확인된 Git blob SHA |
|---|---|
| VERSION_STATUS.md | `3a5db834441e57d45468afc2e8ddd0dab6db06e2` |
| CHANGELOG.md | `aa590b79046d176569479b996578dabe0e449caf` |

원문 구조 확인:
- Version: 3.2 Unified Stable / Current Version.
- 24개 내부 Analysis Engine 유지. Adaptive는 cross-engine framework이며 25번째 엔진이 아니다.
- Dashboard 8개 순서 유지: Observation → Evidence → Judgment → AI Cycle → Smart Money → Liquidity → Technical → Strategy.
- 8 Market Regime R1–R8 및 E1–E8 유지. Binance의 기존 G1–G6와 새 명칭을 충돌시키지 않는다.
- HTS/KRX가 한국시장 최종 확인층. Binance는 유효성·신선도 기준을 충족하는 선행/보조층이다.
- 일반 장중 입력의 24 → 16 → 17 제한과 Full Dashboard의 전체 재검증 경계를 유지한다.
- 기술 계산과 고정 Dual Fibonacci 기준은 TECHNICAL 소유이며 이 설계로 변경하지 않는다.

## 3. 현재 숫자 점수 상태

```text
AI Master Score = DATA UNAVAILABLE
Strategy Action Index = DATA UNAVAILABLE
Numeric SAI Activation = NOT PERMITTED
```

근거: SCORING §2–3, §9–10, §12–16; VERSION_STATUS의 Scoring; CHANGELOG의 Scoring firewall.
Base SAI, Adaptive Adjustment, Final SAI도 현재 계산·표시할 수 있는 공식 숫자가 아니다.
정성 Strategy posture, Confidence, Regime, Signal은 숫자 SAI와 별개다.

SCORING §3의 활성화 Gate 10개를 모두 명시하고 검증해야 한다:
1. Formula
2. Mandatory inputs
3. Input units / normalization
4. Weight or aggregation rule
5. Missing-data rule
6. Partial-data rule
7. Range / bounds
8. Interpretation bands if applicable
9. Actual calculation procedure
10. Validation / regression tests

SCORING §16의 공식 채택 절차 및 VERSION_STATUS/CHANGELOG 갱신도 향후 필요하다.
이 백업 생성은 해당 Gate의 충족 또는 상태 전환이 아니다.

## 4. 확정한 SAI 설계 방향 — 아직 미적용

### 4.1 목적과 계산 범위

AI Master Score는 통합 시장 상태 평가, SAI는 포트폴리오 공격/방어 운용의 행동 강도 지수로 구분한다.
설계 목표 범위는 Component -1.00~+1.00, SAI -100~+100이다.
이 범위는 미래 산식의 설계 목표이며 현재 SCORING에 채택된 공식 범위가 아니다.
Action Band와 실제 비중·매매 연결은 미완성이다. SAI만으로 자동 매매하지 않고 MASTER의 포트폴리오 위험·노출·기술 위치·합의 조건을 따른다.

현재 제공하는 HTS 원자료를 초기 입력으로 설계한다.
Z-score, percentile, 구조형 정규화, 수준과 변화율 결합은 데이터 유형별 검토 방식이며 정확한 계산식·기간·임계값은 미정이다.
HTS 스냅샷에 없는 과거 평균·표준편차·분포·변화율을 만들지 않는다.
과거 데이터가 필요한 산식은 실제 해당 데이터 확보 또는 명시적으로 검증된 대안이 있어야 한다.

### 4.2 기존 Evidence 소유권과 숫자 Component 매핑

새 Evidence Group을 만들지 않는다. 미래 SCORING 내부 계산용 Component만 정의한다.

| 설계 Component | 참조할 기존 Evidence | 초기 원자료 범위 |
|---|---|---|
| SAI-C1 Smart Money | E1 Smart Money | 외국인 현물·선물, 기관 방향성 수급 |
| SAI-C2 Program | E2 Program Flow | 총 프로그램, 차익·비차익 |
| SAI-C3 Breadth | E3 Breadth / Internal | 상승·하락 종목, ADL, 참여 폭 |
| SAI-C4 Sector | E4 Sector / Leadership | 업종 순환, 상대강도, 주도 집중·확산 |
| SAI-C5 Technical | E5 Technical Structure | 가격 구조, MA/VWAP, 거래량, 지지·저항, 모멘텀 |
| SAI-C6 Liquidity | E6 Liquidity / Macro | 환율·금리·예탁금·신용·유동성 중 실제 가용 HTS 입력 |
| SAI-C7 Risk | E7 Volatility / Derivatives Risk | 변동성·옵션·OI·파생 위험 중 실제 가용 입력 |
| 초기 숫자 Component 없음 | E8 Global Leading | 공식 글로벌 및 유효 Binance 확인층 |

Program ≠ Breadth를 유지한다. Program을 E1/C1에, Breadth/ADL을 E5/C5에 별도 독립 근거로 중복 계산하지 않는다.
총 프로그램과 하위 차익·비차익, 현물/선물 누적치와 그 파생치 등 내부 중복도 향후 산식에서 검증해야 한다.
E1–E8은 ADAPTIVE 소유다. C1–C7은 그 소유권을 재정의하지 않는 숫자 계산 설계다.
E8/Leading/Cycle은 초기 SAI 필수 숫자 입력에서 제외하되 기존 분석·Binance 실행 의무 자체를 제거하지 않는다.

### 4.3 가중치와 정성 우선순위 분리

- Base Weight: 공식 SCORING 개정 전까지 고정할 재현 가능한 기준. 실제 수치는 아직 없다.
- Conditional Weight: 향후 공식 산식이 활성화되고 검증된 Transition 조건이 충족될 때만 임시 적용할 독립적인 계산계수.
- Transition 종료·무효화 시 Base Weight로 복귀하는 방향을 유지하되 정확한 해제·만료·재설정 규칙은 후속 설계 대상이다.
- VH/H/M/L은 분석 우선순위다. 4/3/2/1, 백분율, 숨은 가중치로 변환하지 않는다.
- Signal 색, Bull/Bear 개수, Confidence, Strategy posture를 숫자 점수로 바꾸지 않는다.
- Base Weight 자동학습/자동 영구변경 및 관측 반복만으로 영구 변경하는 규칙은 폐기한다.
- 지속 검증 이력이 없으면 과거 Engine Reliability나 성과를 창작하지 않는다.

## 5. Adaptive Market Change 통합 설계 — 아직 미적용

### 5.1 Weight Shift Signal의 의미

새 HTS 데이터가 기존 검증된 예상 범위 또는 Regime 유지 조건을 벗어나는지를 검토한다.
검토 유형: Direction Reversal, Magnitude Shock, Cross-Group Break, Regime Boundary Break, Technical Invalidation, Risk Shock.
이들은 즉시 숫자 Weight를 바꾸는 트리거가 아니라 재검토·Transition Watch의 근거다.
예상 범위, 이전 검증 결과, 비교 시점이 없으면 해당 비교는 불가로 기록한다. 사후에 예측을 만들어 적중/실패를 판단하지 않는다.
정확한 Shock 크기·기간·무효화 임계값은 미정이며 이전 대화의 2σ 등 예시는 공식 값으로 채택하지 않는다.

### 5.2 기존 Transition Framework 안의 통합 흐름

```text
기존 Regime + 새로 검증한 원자료
→ 비정상 Evidence 변화 / Weight Shift Signal
→ Transition Watch / Market Change Candidate
→ 독립 축 및 후속 데이터 확인
→ Transition Confirming 또는 Candidate Rejected
→ Conflict Resolution / Cross-Engine Consensus / Regime Re-validation
→ 검증된 Transition 유지 또는 Regime Change 판단
```

Market Change Candidate / Confirmed / Rejected는 설계상 후보 추적 표현이다.
새 공식 Validation Status, 별도 엔진, 별도 R9 이상 Regime를 추가하지 않는다.
NORMAL / SHIFT WATCH / MODEL CANDIDATE / MODEL CONFIRMED 등 이전 표기는 별도 상태 머신으로 중복 도입하지 않고 기존 Transition 표현에 통합할 대상이다.

후보 기록 항목:
Current Regime, Trigger Evidence, Changed Evidence Groups, Direction of Change,
Price/Flow/Risk Relationship, Proposed Transition, Expected Market Behavior,
Invalidation Conditions, Status.
실제 비교에 필요한 데이터 출처·관측 시점·이전 검증 기대가 있을 때 함께 기록한다.

후속 데이터에서 같은 방향이 한 번 더 나왔다는 이유만으로 Confirmed로 승격하지 않는다.
ADAPTIVE §5·§13·§21을 유지한다:
- Price/Structure, Money Flow/Internal, Risk/Environment의 세 분석 축을 평가한다.
- Transition Confirming은 최소 2개 독립 축의 지지가 필요하다. 2개 Evidence Group과 2개 축은 같은 뜻이 아니다.
- Regime Change는 adaptive-priority review와 Regime Re-validation을 통과해야 한다.
- 일반 방향 판단은 보통 최소 2개 독립 Evidence Group이 필요하다.
- 강한 Strategy 변경은 보통 확인된 현재 Regime 또는 Transition, 최소 3개 독립 고우선순위 Evidence Group 정렬, 기술 위치 일치, 포트폴리오 위험 평가, 미해결 중대 데이터 충돌 없음이 필요하다.
- 핵심 근거 정상화 또는 무효화 조건 충족 시 후보를 폐기/재평가한다. 증거 부족은 억지 확인으로 처리하지 않는다.
- Extreme Risk는 MASTER의 기존 위험 통제를 따르며 숫자 산식 활성화나 Weight 영구변경을 허용하지 않는다.
- 장중 관찰만으로 Full Dashboard 재검증 완료 또는 구조적 Regime 변경을 주장하지 않는다.

### 5.3 Anti-Circularity

```text
Data Validation → Base Evidence Analysis
  ├─→ Base SAI (미래 SCORING 산식으로 독립 계산)
  └─→ Preliminary Regime
       → Adaptive Evidence Priority
       → Transition / Conflict / Cross-Engine Consensus
       → Regime Re-validation / Validation / Revision
       → Confirmed Market State
Base SAI + independently Confirmed Market State
  → Conditional SAI Adjustment (미래 SCORING Gate 충족 시)
  → Final SAI
  → MASTER Portfolio Response / Final Action
```

Base SAI를 Regime 판단의 근거로 사용하지 않는다.
Conditional/Final SAI를 같은 Regime의 독립 확인 근거로 되먹임하지 않는다.
Regime에 의해 올라간 정성 우선순위만으로 그 Regime을 재확인하지 않는다.
Candidate 상태에서는 Conditional Adjustment를 확정 적용하지 않는다.

## 6. 삭제·중복 처리 및 충돌 검증

“삭제”는 이전 설계안의 채택 제외를 의미하며 저장소 파일 삭제를 뜻하지 않는다.

| 검토 항목 | 최종 처리 | 실제 원문 대조 결과 / 근거 |
|---|---|---|
| 새 G1–G6 Evidence 체계 | 폐기, 기존 E1–E8 참조 | ADAPTIVE §7–8 및 BINANCE §16 명칭·소유권 충돌 방지 |
| Program/Internal 통합 | Program과 Breadth 분리 | E2/E3 유지, E1/E5 중복 확인 금지 |
| Leading/Cycle 초기 SAI 필수 | 제외/보조층 | HTS 중심 설계 및 MASTER §3, BINANCE §1–2와 일치; 기존 분석 의무는 유지 |
| 별도 Market Change Engine | 기존 Transition Framework에 통합 | MASTER §4, ADAPTIVE §13·26; 24 Engine 유지 |
| 새 Dashboard 상위 카테고리 | 추가하지 않음 | DASHBOARD §3–4·15–16; 8개 내부 배치 |
| Candidate → 다음 데이터 반복 → 즉시 Confirmed | 약한 승격 규칙 폐기 | ADAPTIVE §5·13의 독립 축과 재검증 조건 유지 |
| 정성 VH/H/M/L → 숫자 Weight | 금지 | ADAPTIVE §9·27, SCORING §7; 독립 숫자 산식만 후속 검토 |
| Base SAI → Regime → 가중치 → 동일 Regime 재확인 | 폐기, 계산 경로 분리 | MASTER §20, ADAPTIVE §12 순환 금지 |
| 자동 영구 Base Weight 변경 | 폐기 | MASTER §19, ADAPTIVE §23의 검증 이력 제한 유지 |
| Coverage 표시만으로 Partial 숫자 출력 | 금지 | SCORING §9–10; 명시적 누락·재가중·최소 Coverage 미완성 |
| Candidate인데 Adaptive Adjustment/Final 숫자가 있는 이전 출력 예시 | 채택 제외 | 후보 확인 조건 및 현재 숫자 비활성 상태와 충돌 |
| NORMAL/REVIEW/OVERRIDE 또는 MODEL 상태의 새 공식 Validation Status화 | 채택 제외 | MASTER §14, DASHBOARD §8의 상태 분리 유지 |
| Risk Override로 SAI Gate 우회 | 금지 | 기존 MASTER 위험 통제만 허용, SCORING Gate 유지 |
| 기술 계산을 SCORING/ADAPTIVE에 중복 정의 | 금지 | TECHNICAL 소유 계산 참조, 숫자 정규화만 SCORING 소유 |

검증 결론: 위 수정 방향은 현재 6 Authority / 24 Engine / 8 Dashboard의 범위 분리와 양립한다.
이 결과는 **문서 구조와 설계 경계의 정적 검증**이며, 실제 HTS 산식 계산·예측 성과·회귀 테스트 통과를 뜻하지 않는다.

기존 원문에서 확인한 별도 정합성 메모:
ADAPTIVE §24는 “Use only” 목록에 없는 “Selective Hold”를 Rotation 기본 posture에 사용한다.
이번 SAI 설계가 새로 만든 불일치는 아니며, 이 백업에서 공식 원문을 수정하지 않는다.
따라서 저장소 전체가 모든 표현 차원에서 무결하다고 포괄 선언하지 않는다. 후속 공식 개정 검토 시 다룰 수 있다.

## 7. 향후 공식 파일별 반영 경계

| 파일 | 이후 검토할 역할 |
|---|---|
| SCORING_RULE | Base Formula, C1–C7 정규화, 숫자 Weight, Missing/Partial, Conditional Adjustment, Range, Action Band, 계산 절차·검증 |
| ADAPTIVE_VALIDATION_RULE | Weight Shift 시장 해석, Candidate, Transition 확인/폐기, Regime 재검증 |
| MASTER_RULE | 기존 실행 흐름 안의 연결 및 포트폴리오 최종 위험 기준 |
| DASHBOARD_RULE | 기존 8개 내부의 Base/Final SAI, Shift, Transition 출력 위치; 공식 Gate 미충족 시 DATA UNAVAILABLE |
| TECHNICAL_RULE | 기존 기술 계산 권위 유지 |
| BINANCE_RULE | 기존 지원층·G1–G6·신선도 권위 유지 |

다음 단계의 예고일 뿐 이 파일 생성으로 어떤 공식 규칙도 개정하지 않는다.

## 8. 아직 미완성인 산식 및 검증 항목

핵심 미완성 5개:
1. SAI-C1–C7 각각의 실제 정규화 Formula.
2. Base Weight 숫자.
3. Missing/Partial 최소 Coverage.
4. Conditional Adjustment 숫자 및 최대 변경폭.
5. 실제 HTS 사례 기반 Validation / Regression Test.

위 5개를 완성하려면 다음 세부 명세도 필요하다:
- 필수/선택 입력 목록, 단위, 부호, 시점, 비교 기간, 실제 HTS 가용성.
- 정규화 window, 최소 표본수, 분산 0·극단값·범위 제한·타임프레임 불일치 처리.
- Component 내부 및 간 집계, 원자료 중복 제거, 가중치 합·정규화 방식.
- Missing ≠ Neutral; 허용 누락, Coverage 정의·분모, 재가중 허용 여부·계산법, Partial 표시.
- Conditional 적용 자격, 크기, 상한, 지속·해제·만료·복귀, 충돌 시 처리.
- Base/Conditional/Final 계산 절차, 정확한 Range/bounds, 반올림, Action Band 및 포트폴리오 연결 조건.
- 정상·반전·집중상승·분배·위험급변·누락·경계·중복·순환 금지 사례의 입력과 기대 결과.
- 원자료 및 검증 결과의 재현 가능한 출처/버전. 실제 이력이 없으면 누적 성능 주장을 하지 않는다.

이전 대화의 20/60일, ±2σ, Coverage 80%/60%, 예시 25%/30% Weight, 예시 SAI 숫자는 검증된 공식 파라미터가 아니다.
가용 데이터만으로 조용히 재정규화하거나 미정 숫자를 채워 넣지 않는다.

## 9. 1단계 검증 기록과 중단 지점

생성 전 확인:
- 6개 Authority 및 2개 상태 파일을 동일한 기준 커밋에서 읽음.
- 전체 blob SHA 확인; 이전 대화의 MASTER/DASHBOARD/SCORING/ADAPTIVE/VERSION_STATUS/CHANGELOG 축약 SHA와 일치.
- 기준 Git tree에서 요청한 신규 경로가 존재하지 않음을 확인.
- Rules 6개, 24 Engine, 8 Dashboard 및 숫자 비활성 상태 확인.
- 신규 파일의 비권위 경계, 확정 설계, 폐기안, 충돌 결과, 미완성 Gate를 구분.

생성 후 무결성 확인 절차:
1. GitHub에서 생성된 파일 전체를 다시 읽어 작성한 UTF-8 내용과 정확히 대조한다.
2. 생성 커밋과 파일 blob SHA를 확인한다.
3. 생성 커밋의 부모가 위 기준 커밋인지 확인하고, 변경 파일이 이 백업 1개뿐인지 확인한다.
4. 생성 후 Git tree의 6 Authority 및 VERSION_STATUS/CHANGELOG blob SHA가 위 표와 동일한지 확인한다.
5. 확인 결과와 생성 커밋은 작업 완료 보고에 남긴다. 이 문서 안에 자기 자신의 SHA나 아직 수행하지 않은 검증의 PASS를 미리 기록하지 않는다.

사용자 요청에 따라 1단계 생성·재읽기 검증 후 중단한다.
SAI-C1 실제 산식 설계, 공식 규칙 Patch, VERSION_STATUS/CHANGELOG 등록 및 숫자 활성화는 사용자 확인 이후 별도 단계다.
