# 2026-02-18 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 기준 **233,309 skills**. `recent` 상단에서 `query-data`, `data-analysis`, `browsing-workflow` 확인.
- **MCP Market**: 브라우저 기준 **21,135 servers**. Latest에 `Java Decompiler`, `Dotnet Websearch`, `AI Inspector` 노출(다수 0 usage).
- **SkillHub.ai**: 여전히 **“Coming soon”** 랜딩 상태(실사용 카탈로그 부재).
- **ClawHub**: `clawhub explore --sort newest --limit 30 --json`로 신규군 확인 (`arc-compliance-checker`, `agent-self-assessment`, `SnapRender` 등).
- **VSCode Agent Skills extension 검색**: Marketplace `agent skills` 결과 **1,093개**, 상위에 `copilot-mcp`(80.8K), `agent-skills`(1.7K), `agnix`(17) 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `arc-compliance-checker` | ✅ 도입 | **(1 필요성)** 외부 스킬 intake에서 정책 준수 판정이 아직 수동 편차가 큼. **(2 대체성)** 기존 체크리스트는 “통과/실패” 근거 구조화가 약함. **(3 비용대비효과)** 정책 규칙/위반 추적 모델 흡수로 감사 리드타임 단축 가능. **(4 과대포장 필터)** 다운로드 신호는 약하지만, 현재 우리의 실제 병목(일관된 컴플라이언스 게이트)과 직접 정합. |
| VSCode `avifenesh.agnix` (17 installs) | ⚠️ 참고만 | 규칙셋 아이디어는 유효하지만 VSCode 의존. **재검토:** 규칙 정의를 CLI 규칙팩으로 추출 가능할 때.
| MCP Market `AI Inspector` (latest, 0 usage) | ⚠️ 참고만 | 브라우저 브릿지 계열은 흥미롭지만 `browser-cdp-automation` + OpenClaw browser로 핵심 요구 충족. **재검토:** 브라우저 자동화 실패율/SLA가 악화될 때.
| SkillsMP `query-data` (PostHog) | ⚠️ 참고만 | 분석 질의 표준화는 의미 있으나 현재 최우선 병목은 배포/수익화 파이프라인. **재검토:** PostHog 조회가 운영 병목으로 측정될 때.
| ClawHub `SnapRender` | ⚠️ 참고만 | 시각 캡처/비교는 유용하나 현재 스택으로 이미 구현 가능. **재검토:** 정기 시각 diff 리포트 자동화가 분기 KPI로 승격될 때.

❌ 불필요 판정: **8건**
- (요약) MoltHub/Lobstore 계열(정책 차단), 0-usage 최신 유틸 다수, 스택/우선순위 불일치 항목.

## ✅ 도입 실행 계획
### `skill-intake-policy-gate` (신규 내부 스킬)
1. **Research**: `arc-compliance-checker`의 정책 모델(룰, 위반, 예외, 상태 추적)만 추출.
2. **Audit**: 우리 보안 기준으로 룰셋 재정의(외부 URL 실행 유도, credential 노출, 위험 쉘 패턴, Molt 계열 차단).
3. **Rewrite**: `misskim-skills/skills/skill-intake-policy-gate/`로 내부 재작성(외부 코드 직접 의존 금지).
4. **Gate 연동**: intake 파이프라인 precheck로 강제해 Research → Audit → Rewrite 전 단계에서 자동 차단.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
