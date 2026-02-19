# 2026-02-19 12:06 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 수집 성공. 총 **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 확인.
- **MCP Market**: 브라우저 수집 성공. 총 **21,362 servers**(Updated: just now). `Latest MCP Servers`에 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club)**: 브라우저 수집 성공. **21.6K skills / 4.4M stars**. Trending Today 상단 `feishu-drive`, `model-usage`, `github`, `wacli`, `trello` 확인.
- **ClawHub**: `clawhub explore --sort newest --limit 60 --json` 샘플 수집. 신규군에서 `clawwall`, `memory-hygiene`, `reddit-insights`, `voice-agent` 확인. Molt 계열(`moltbot-*`) 노출 감지.
- **VSCode Agent Skills extension**: Marketplace 검색 `agent skills` **1,103 results**. `AutomataLabs.copilot-mcp` **81.1K installs**, `formulahendry.agent-skills` **1.8K installs**, `yamapan.agent-skill-ninja` **538 installs** 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `clawwall` | ✅ 도입 | **Q1 필요성:** 외부 발신/게시 자동화에서 secret·PII 유출을 하드블록하는 전용 게이트가 현재 운영 공백. **Q2 대체성:** `healthcheck`·보안 규율은 하드닝/감사 중심이고, 메시지·payload 직전 DLP 차단은 직접 대체 불가. **Q3 비용효과:** regex+entropy+allowlist 기반 내부 재작성 비용이 낮고, 사고 회피 효과가 큼. **Q4 과대포장 필터:** installs/stars 0이라 인기 신호는 약함. 채택 근거는 ‘유행’이 아니라 ‘유출 리스크 공백 해소’. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | **Q1:** 배포 채널 확장에는 유효. **Q2:** 현재 우선 채널은 Telegram Mini App/itch/CrazyGames라 즉시 병목과는 거리 있음. **Q3:** OAuth/토큰 운영비용 대비 단기 ROI 불명확. **Q4:** latest 노출만으로 품질 보증 불가. **재검토:** 뉴스레터 채널 KPI를 공식 운영할 때. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | **Q1:** 검색 fallback 니즈는 실제 존재. **Q2:** 이미 fallback 루트(직접 fetch/대체 검색 전략) 운용 중이라 즉시 공백은 제한적. **Q3:** MCP 추가 유지비 대비 순증 이득이 작음. **Q4:** 최신 노출+0 usage 신호는 과대포장 가능. **재검토:** 검색 실패율이 SLA 임계치를 넘을 때. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | **Q1:** 테스트-커밋 게이트 수요는 유효. **Q2:** 내부 `verify-before-done` + SDD/TDD 순서 규율로 핵심 기능 이미 충족. **Q3:** 도입 대비 순증 생산성 낮음. **Q4:** recent 상단/저신호(0★)는 품질 근거 약함. **재검토:** 회귀 결함이 연속 2회 이상 발생 시. |
| SkillHub `feishu-drive`/`model-usage` 상위군 | ⚠️ 참고만 | **Q1:** 일반 생산성 확장 니즈는 있음. **Q2:** 현재 스택(`gog`, `session_status`, 기존 워크플로)으로 주요 요구 대응 가능. **Q3:** 신규 도입보다 기존 채널 확장이 ROI 우위. **Q4:** 대형 star는 확산 지표일 뿐 우리 환경 적합성 보증 아님. **재검토:** Feishu 협업 전환 또는 사용량 관제 병목이 생길 때. |
| ClawHub `memory-hygiene` | ⚠️ 참고만 | **Q1:** 메모리 정리 니즈는 존재. **Q2:** `openclaw-mem` + 내부 메모리 운영 규율과 중복. **Q3:** 추가 도입 대비 개선폭 불확실. **Q4:** installs 18/3★는 참고 신호지만 필수 근거는 아님. **재검토:** 회상 품질 저하가 지표로 확인될 때. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | **Q1:** VSCode 내 통합 관리 수요는 일부 유효. **Q2:** 현재 운영축은 OpenClaw CLI/서브에이전트라 IDE 의존도가 낮음. **Q3:** 설정/학습비 대비 즉시 ROI 제한. **Q4:** 81.1K installs는 배포력 지표이지 운영 적합성 보증 아님. **재검토:** VSCode 중심 협업이 표준으로 전환될 때. |

❌ 불필요 판정: **96건**
- (요약) Molt 계열(`moltbot-*`, MoltHub 연계 확장) 정책 차단, 트레이딩/취미성 저정합 스킬, 0-usage/저신뢰 신규 항목 다수.

## ✅ 도입 실행 계획
### `outbound-dlp-gate` (내부 신규 스킬)
1. **Research**: `clawwall`의 차단 패턴(비밀키/PII/도메인 allowlist)만 추출, 원본 코드 블라인드 설치 금지.
2. **Audit**: 오탐률, 로그 마스킹, bypass 가능성, 성능(지연), allow/deny 정책 충돌 점검.
3. **Rewrite**: `misskim-skills/skills/outbound-dlp-gate/`로 내부 재작성(우리 메시징/게시 워크플로우 전용 훅 포함).
4. **Integration**: 외부 전송 경로(메시지/게시/웹훅)에 pre-send 검사 게이트로 연결.
5. **Validation**: 정상 샘플 + 의도적 secret/PII 샘플 회귀 테스트 후 차단 룰셋 고정.

## 보안
- **Molt Road / molt.host / MoltHub / Moltbook: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
