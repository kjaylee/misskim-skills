# 2026-02-18 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 기준 총 **233,309 skills**. 최근 피드 상단에 `query-data`(PostHog), `data-analysis`, `browsing-workflow` 등 2/17 신규 항목 확인.
- **MCP Market**: 브라우저 기준 총 **21,135 servers**. 최신 섹션에 `AI Inspector`, `Java Decompiler`, `Dotnet Websearch` 등 신규(다수 0 사용량) 노출.
- **SkillHub**: **21.3K skills / 5.7M stars**. `Solopreneur Toolkit`에 `requesthunt`, `seo-geo`, `producthunt` 포함.
- **ClawHub**: `clawhub explore --sort newest --limit 30 --json` 수집. 신규군에 `agents-skill-security-audit`, `agents-skill-tdd-helper`, `openclaw-mentor/mentee` 확인.
- **VSCode Agent Skills ecosystem**: Marketplace API `agent skills` 검색 **1,211 results**. `AutomataLabs.copilot-mcp` 80,815 installs, `formulahendry.agent-skills` 1,723 installs.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `agents-skill-security-audit` | ✅ 도입 | **(1 필요성)** 외부 스킬 intake에서 공급망/권한 리스크 점검이 수동 체크리스트 의존. **(2 대체성)** 기존 `verify-before-done`/정책 문서만으로는 패턴 기반 탐지 자동화가 약함. **(3 비용대비효과)** 경량 정적 스캔 패턴 흡수 비용이 낮고, 사고 예방 가치가 큼. **(4 과대포장 필터)** 다운로드/별점 신호는 약하지만 “문제-해결 정합”이 명확해 내부 재작성 가치 있음. |
| SkillHub `requesthunt` (Solopreneur Toolkit) | ✅ 도입 | **(1 필요성)** 무엇을 만들지 결정할 때 실수요 신호 수집 자동화 공백 존재. **(2 대체성)** 현재 `game-marketing`/플레이북은 전략 중심이라 채널별 요청 데이터 점수화가 부족. **(3 비용대비효과)** 중간 구현비로 아이템 선정 리드타임 단축 기대. **(4 과대포장 필터)** 별점이 아니라 Reddit/X/GitHub 원문 신호로 검증 가능. |
| VSCode `avifenesh.agnix` (Agent Config Linter, 17 installs) | ⚠️ 참고만 | SKILL/AGENTS lint 아이디어는 유효하나 VSCode 종속. **재검토:** CLI 기반 lint 엔진 추출 가능하거나 VSCode 운영 비중이 올라갈 때. |
| MCP Market `AI Inspector` (latest, 0 usage) | ⚠️ 참고만 | 브라우저 자동화 브릿지 자체는 흥미롭지만 현재 `browser-cdp-automation` + OpenClaw browser로 핵심 요구 충족. **재검토:** 현재 브라우저 자동화 실패율/지연이 SLA를 넘길 때. |
| SkillsMP `query-data` (PostHog) | ⚠️ 참고만 | 제품 분석 니즈는 있으나 현재 PostHog 운영 파이프라인이 핵심 병목은 아님. **재검토:** 퍼널 지표 자동 조회가 실제 운영 병목으로 측정될 때. |
| VSCode `AutomataLabs.copilot-mcp` (80,815 installs) | ⚠️ 참고만 | 설치수는 강한 신호지만 운영축은 OpenClaw CLI 중심. **재검토:** 팀 IDE 표준을 VSCode로 전환하거나 IDE 배포 채널이 우선순위가 될 때. |

❌ 불필요 판정: **4건**
- (요약) `MoltHub/Lobstore` 계열(정책 차단), 기존 스킬 중복(`agents-skill-tdd-helper`), 운영축 불일치(`openclaw-mentor/mentee` 릴레이형), 최신 0-usage 범용 유틸 군 일부.

## ✅ 도입 실행 계획
### 1) `skill-intake-security-audit-lite` (신규 내부 스킬)
1. **Research**: `agents-skill-security-audit`의 탐지 룰(HTTP POST, credential keyword, ~/.env 접근 등) 분해.
2. **Audit**: 오탐/누락 케이스 정의(샘플 30개 스킬) + 위험등급 기준 확정.
3. **Rewrite**: `misskim-skills/skills/skill-intake-security-audit-lite/`로 내부 재작성.
4. **Gate 연동**: 외부 스킬 intake 파이프라인의 필수 precheck로 연결.

### 2) `request-signal-harvester` (신규 내부 스킬)
1. **Research**: `requesthunt` 흐름에서 채널별 수집 포인트(Reddit/X/GitHub Issues)만 추출.
2. **Audit**: 스팸/저품질 신호 제거 규칙과 점수 계산식(문제 빈도×지불의사 단서×반복성) 정의.
3. **Rewrite**: `misskim-skills/skills/request-signal-harvester/`로 내부 구현.
4. **Pilot**: 1주간 아이템 선정 루프에 적용, 후보 발굴 시간/전환률 비교.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 도입 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
