# 2026-02-19 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 접근 성공. 총 **239,658 skills**. recent 상단에서 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading` 확인.
- **MCP Market**: 브라우저 접근 성공. 총 **21,325 servers**(Updated: just now). `Latest MCP Servers`에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants`, `Vigilo` 확인.
- **SkillHub (skillhub.club)**: 브라우저 DOM 기준 **21.6K skills / 4.3M stars**. Trending Today 상단 `feishu-drive`, `model-usage`, `github`, `wacli`, `trello` 노출.
- **ClawHub**: `clawhub explore --sort newest --limit 60 --json` 수집(실수집 **59개**). 신규군에서 `credential-scanner`, `flowclaw`, `loopwind`, `gamer-news` 확인.
- **VSCode Agent Skills 생태**: 검색 `agent skills` **1,102 results**. `AutomataLabs.copilot-mcp` **81K installs**, `formulahendry.agent-skills` **1,746 installs**, `yamapan.agent-skill-ninja` **537 installs** 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `credential-scanner` | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake 과정에서 비밀키/토큰 유출 탐지는 현재 수동 점검 의존이라 누락 리스크가 존재. **Q2 대체성:** `healthcheck`/기존 규율은 보안 posture 점검 중심이며, 파일 레벨 secret 패턴 스캔은 공백. **Q3 비용효과:** Python 단일 스크립트 기반으로 도입비가 낮고(Research→Audit→Rewrite), 사고 예방 효과가 큼. **Q4 과대포장 필터:** downloads 2/0★로 인기 신호는 약함. 채택 근거는 ‘인기’가 아닌 ‘공백 해결성’. |
| ClawHub `flowclaw` | ⚠️ 참고만 | **Q1:** 멀티모델 쿼터/라우팅 문제는 실제 존재. **Q2:** 현재 OpenClaw 모델 운영 + 수동 우선순위 조정으로 핵심 운영은 가능. **Q3:** 다중 인증/라우팅 자동화는 유지비가 큼. **Q4:** 초기 다운로드(8)·평점(0)만으로 안정성 판단 불가. **재검토:** 모델 쿨다운/쿼터 충돌로 작업 중단이 주 3회 이상 발생 시. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | **Q1:** Brave 429로 검색 백업 니즈는 명확. **Q2:** 이미 `search-fallback-openrouter` 추진 중이라 1차 대체 경로 존재. **Q3:** MCP 추가 운영 포인트 대비 단기 이득 불명확. **Q4:** latest 노출 + 0 usage는 품질 보증 아님. **재검토:** OpenRouter fallback 실패율이 20% 초과 시. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | **Q1:** 테스트-커밋 게이트 니즈는 유효. **Q2:** `verify-before-done` + `tdd-discipline`로 동일 문제를 이미 커버. **Q3:** 도입 대비 순증 생산성 작음. **Q4:** recent 상단 노출/저신호(0★)는 마케팅 노이즈 가능. **재검토:** 회귀 버그가 2회 이상 연속 발생 시. |
| SkillHub `context-optimization` | ⚠️ 참고만 | **Q1:** 컨텍스트 비용/정합 최적화 니즈는 존재. **Q2:** `openclaw-mem` + 내부 메모리 규율과 기능 중복. **Q3:** 추가 도입 대비 개선폭 불확실. **Q4:** 대형 star는 확산력 지표일 뿐 품질 보증 아님. **재검토:** 컨텍스트 초과/비용 급증이 임계치 초과 시. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | **Q1:** 확장 생태 관리 수요는 일부 존재. **Q2:** 현재 운영축은 OpenClaw CLI + subagent로 VSCode 종속 필요가 낮음. **Q3:** IDE 의존 도입비 대비 ROI 제한. **Q4:** 81K installs는 배포력 지표이지 우리 환경 적합성 보증이 아님. **재검토:** VSCode 중심 협업이 운영 표준으로 전환될 때. |

❌ 불필요 판정: **19건**
- (요약) Molt 계열 연동 항목(정책 차단), 트레이딩/개인취미 중심 저정합 스킬, 0-usage 최신 MCP 다수.

## ✅ 도입 실행 계획
### `credential-leak-gate` (내부 신규 스킬)
1. **Research**: `credential-scanner`의 탐지 패턴/출력 구조만 추출(코드 블라인드 설치 금지).
2. **Audit**: 오탐/누락률, 경로 순회 안전성, 로그 마스킹, 외부 네트워크 호출 여부 점검.
3. **Rewrite**: `misskim-skills/skills/credential-leak-gate/`로 내부 재작성 (우리 정책/리포 구조 반영).
4. **Integration**: 외부 스킬 intake 파이프라인에 `Research → Audit` 단계 전 자동 secret scan 게이트 추가.
5. **Validation**: `misskim-skills/`, `eastsea-blog/` 대상으로 파일 스캔 회귀 테스트 후 표준화.

## 보안
- **Molt Road / molt.host / MoltHub / Moltbook: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
