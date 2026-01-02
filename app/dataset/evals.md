1. MAST가 등장한 이유는 무엇인가?

Q: 왜 Multi-Agent LLM Systems(MAS)의 실패 원인을 체계적으로 분석할 필요가 있었는가?
A: MAS는 기대와 달리 단일 에이전트 대비 큰 성능 향상을 보여주지 못하고, 높은 실패율을 보였다. 기존에는 실패 원인을 명확히 구조화해 설명하는 체계가 없었기 때문에, MAS의 실패 패턴을 정리하고 일관된 기준을 만드는 것이 필요했다.
Context: “their performance gains often remain minimal compared to single-agent frameworks…This motivates the fundamental question we address: Why do MASs fail?”  ￼

⸻

2. MAST의 주요 구성은 무엇인가?

Q: MAST는 어떤 구성 요소로 이루어져 있는가?
A: MAST는 총 14개 실패 모드(failure modes)를 3개 상위 카테고리로 분류하여 구성된다: (1) Specification Issues, (2) Inter-Agent Misalignment, (3) Task Verification.
Context: “we identify 14 unique failure modes, organized into 3 overarching categories…”  ￼

⸻

3. MAS 실패의 가장 큰 비중을 차지하는 카테고리는?

Q: 어떤 실패 카테고리가 가장 많이 발생했는가?
A: Specification Issues가 약 41.77%로 가장 높은 비중을 차지했다.
Context: “Specification Issues (41.77%), Inter-Agent Misalignment (36.94%), Task Verification (21.30%).“  ￼

⸻

4. FM-1.1 Disobey Task Specification의 의미는?

Q: 실패 모드 FM-1.1은 무엇을 의미하는가?
A: 시스템이 사용자 과업(Task) 요구사항을 따르지 못하고 잘못 해석하거나 무시하는 경우이다.
Context: “Failures… reflect flaws… fail to follow task requirements (FM-1.1).”  ￼

⸻

5. Step Repetition(FM-1.3)이 발생하는 이유는?

Q: 왜 FM-1.3 Step Repetition이 MAS에서 자주 발생하는가?
A: 엄격한 turn 구조나 prompt 설계 문제가 반복적인 행동 루프를 유발하기 때문이다.
Context: “step repetitions (FM-1.3, 17.14%) due to rigid turn configurations…”  ￼

⸻

6. FC2 Inter-Agent Misalignment가 의미하는 것은?

Q: Inter-Agent Misalignment 카테고리는 어떤 유형의 실패를 다루는가?
A: MAS 내 여러 에이전트 간 협력·조율이 제대로 이루어지지 않아 목표 정렬이 깨지는 실패를 말한다.
Context: “failures arise from breakdowns in inter-agent interaction and coordination during execution.”  ￼

⸻

7. FM-2.4 Information Withholding 사례는 어떤 문제인가?

Q: FM-2.4는 어떤 상황에서 발생하는가?
A: 한 에이전트가 중요한 정보를 알고 있으나 이를 공유하지 않아 다른 에이전트가 계속 실패하는 경우이다.
Context: 예시에서 “The Phone Agent fails to communicate API requirements… leading to repeated failed attempts.”  ￼

⸻

8. FM-3.1 Premature Termination이란?

Q: MAS가 과업을 조기 종료하는 상황은 어떤 실패로 분류되는가?
A: FM-3.1 Premature Termination이며, 충분한 검증 없이 작업이 완료되었다고 잘못 판단하는 경우이다.
Context: “premature termination (FM-3.1, 7.82%).”  ￼

⸻

9. 왜 검증(Verification)이 중요한가?

Q: MAS에서 Task Verification 단계가 중요한 이유는?
A: MAS의 실패 중 상당수가 검증 부족 또는 잘못된 검증으로 인해 발생하기 때문에, 품질 관리는 필수 요소다.
Context: “Verification failures are prominent… incomplete or incorrect verification… 13.48% of all failures.”  ￼

⸻

10. Verifier만 있으면 MAS 품질이 향상되는가?

Q: Verifier 에이전트 도입만으로 MAS 신뢰성이 충분히 확보되는가?
A: 아니다. Verifier가 있어도 대부분의 시스템은 매우 낮은 성공률을 보였으며, 검증 단계가 피상적인 경우가 많다.
Context: “Verifier is not a silver bullet… ChatDev achieves only 33.33% correctness…”  ￼

⸻

11. MAST는 어떻게 개발되었는가?

Q: MAST는 어떤 방법론을 통해 도출되었는가?
A: Grounded Theory(GT), open coding, theoretical sampling을 기반으로 200개 이상의 MAS 대화 로그를 분석해 도출되었다.
Context: “we adopt the Grounded Theory approach… open coding… analyzing 200+ traces…”  ￼

⸻

12. Inter-Annotator Agreement는 어느 정도였는가?

Q: MAST의 신뢰도를 보여주는 annotator agreement 수치는?
A: 인간 annotator 간 Cohen’s Kappa는 0.88로 매우 높은 합의도를 나타냈다.
Context: “achieving a Cohen’s Kappa score of 0.88.”  ￼

⸻

13. LLM-as-a-Judge의 역할은?

Q: 연구에서 LLM-as-a-Judge는 어떤 목적으로 사용되었는가?
A: 인간 annotator를 대신해 MAS 실패 모드를 자동으로 분류하는 데 사용되었다.
Context: “we develop an LLM-as-a-judge pipeline integrated with MAST.”  ￼

⸻

14. 모델의 Few-shot 제공 여부에 따른 평가 차이는?

Q: LLM Annotator의 성능은 few-shot 예시 제공 여부에 따라 어떻게 달라졌는가?
A: few-shot 제공 시 F1이 0.80까지 향상되며 Cohen’s Kappa도 0.77로 증가했다.
Context: Table 2의 결과 “o1 few-shot… F1 0.80, κ=0.77.”  ￼

⸻

15. Specification Issues가 시스템 설계 문제라는 근거는?

Q: 왜 Specification Issues는 단순 LLM 한계가 아니라 시스템 설계 문제라고 보는가?
A: 동일한 명확한 prompt를 줘도 MAS가 설계 구조적 한계 때문에 여전히 잘못된 판단을 하기 때문이다.
Context: Wordle 사례 분석 “failures stem from MAS’s inherent design… not only prompt ambiguity.”  ￼

⸻

16. 왜 Inter-Agent Misalignment는 근본적 문제인가?

Q: Inter-Agent Misalignment는 왜 단순한 오류가 아니라 구조적 문제인가?
A: 정보 공유·정렬에 필요한 프로토콜과 조직 구조가 미흡하면 같은 모델을 사용해도 반복적으로 실패하기 때문이다.
Context: “breakdowns in inter-agent interaction… coordination failures.”  ￼

⸻

17. FC3 Task Verification 실패는 언제 일어나는가?

Q: FM-3.2 No or Incomplete Verification 실패는 어떤 상황인가?
A: 프로그램이 겉보기만 통과하고 실제 동작 요구를 충족하지 못했는데도 검증 과정이 이를 잡아내지 못하는 경우이다.
Context: Chess 예시 “verifier performs only superficial checks… runtime bugs remain.”  ￼

⸻

18. 왜 MAS 효율성 문제는 MAST에 포함되지 않았는가?

Q: MAS에서 종종 발생하는 비효율성 문제가 MAST에 포함되지 않은 이유는?
A: MAST는 정확도 중심 taxonomy이며, 비용·효율·속도는 별도 연구 주제라 의도적으로 제외되었다.
Context: “we deliberately pruned non-correctness metrics like efficiency… for focus.”  ￼

⸻

19. MAST가 개발자에게 주는 실질적 활용 가치는?

Q: MAST가 MAS 개발 과정에서 어떤 실용적 가치를 제공하는가?
A: 실패 유형을 정량적으로 파악해 어디를 개선해야 할지 명확히 도와주고, 개입 전후의 변화도 객관적으로 비교할 수 있게 한다.
Context: “developers can obtain breakdown of failure types… guiding debugging efforts.”  ￼

⸻

20. MAS 성능 향상을 위해 무엇이 필요한가?

Q: 단순히 모델 성능을 높이는 것 외에 MAS를 향상시키기 위해 필요한 것은?
A: 에이전트 조직 구조, 역할 설계, 커뮤니케이션 프로토콜, 검증 시스템 등 시스템 레벨 구조 개선이 필요하다.
Context: “failures came from system design, not just model limitations… fundamental changes to agent organization required.”  ￼