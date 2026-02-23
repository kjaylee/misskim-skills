# 2026-02-23 12:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **MiniPC browser.proxy:** 이번 회차는 미사용(필수 소스가 `web_fetch + r.jina.ai + CLI/API`로 충족).
- **`web_search`:** Brave quota/rate-limit `429`로 실패.
- **대체 경로:** `web_fetch`, `r.jina.ai`, `clawhub` CLI, VSCode Marketplace API.
- **SkillsMP:** 총 `269,875` skills, `Security 6,631`, `Mobile 4,817`, `LLM & AI 27,853`.
- **MCP Market:** 원본 `mcpmarket.com`은 `Vercel Security Checkpoint(429)`, mirror 기준 `6,409` servers.
- **SkillHub:** `311` tools (`233 MCP / 78 Skills`).
- **ClawHub:** 인기 상위 `gog(32,958)`, `self-improving-agent(30,641)`, `tavily-search(27,112)`.
- **VSCode Agent Skills:** `copilot-mcp(81,749)`, `agent-skills(1,818)`, `agnix(28)`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `Microsandbox` 패턴 (외부 설치 아님, 내부 재작성) | ✅ 도입 | **Q1 필요:** 외부 스킬 intake에서 “코드 실행 전 안전 검증” 공백이 실제 리스크. **Q2 대체:** 현재는 정적 리뷰 중심이라 실행계 리스크(실행 시 네트워크/파일 접근)를 충분히 검증하지 못함. **Q3 비용효과:** 외부 서버 도입 대신 격리 실행 규칙만 내부 스킬로 재작성하면 유지비 대비 보안효과 큼. **Q4 과대포장:** MCP Market 점수는 참고만 사용, 채택 근거는 내부 보안 갭 해소 여부로 제한. **실행계획:** (1) 위협모델/허용행위 정의 → (2) `misskim-skills/skills/skill-intake-sandbox-gate/` 초안(Research→Audit→Rewrite) → (3) 최근 intake 20건 드라이런 → (4) 오탐/미탐 튜닝 → (5) 통과 기준 충족 시 intake 기본 게이트 편입. |
| SkillHub `Context7`/`Playwright`/`Notion` 상위군 | ⚠️ 참고만 | **Q1:** 유용하지만 즉시 미해결 병목 아님. **Q2:** `context7-docs`, `playwright-testing`, 기존 Notion/문서 경로로 대체 가능. **Q3:** 신규 도입 대비 순증 불명확. **Q4:** signal(46.4k/27.5k)은 품질 보증 아님. **재검토:** 기존 문서/브라우저 워크플로 실패율이 주간 2배 이상 상승 시. |
| MCP Market 상위 `Archon`/`Trigger.dev`/`Chrome DevTools` | ⚠️ 참고만 | **Q1:** 자동화 니즈는 있으나 현 병목 직접 타격은 제한적. **Q2:** `coding-agent`, `parallel-agents`, `browser-cdp-automation`으로 기능 대체 가능. **Q3:** 신규 MCP 운영/권한 비용 대비 ROI 불명확. **Q4:** 랭킹 고점만으로 채택 금지. **재검토:** 기존 오케스트레이션/브라우저 라인 장애가 2주 연속 누적될 때. |
| VSCode `copilot-mcp`/`agent-skills`/`skill-ninja` | ⚠️ 참고만 | **Q1:** IDE 내부 관리 편의성은 인정. **Q2:** 현재 운영축은 OpenClaw CLI 중심이라 대체 가능. **Q3:** 에디터 종속성 증가 비용 큼. **Q4:** installs 대형 신호(81k+)는 시장성 지표일 뿐 우리 KPI 근거는 아님. **재검토:** VSCode 기반 협업 비중 50%+ 시. |
| ClawHub `self-improving-agent`/`ontology` | ⚠️ 참고만 | **Q1:** 학습/메모리 가치는 있으나 현재 핵심 병목은 intake 보안 게이트. **Q2:** `openclaw-mem` + 내부 메모리 운영으로 1차 대응 가능. **Q3:** 도입 시 행동 예측성·운영 복잡도 증가 가능. **Q4:** 다운로드(30k+) 단독 근거 채택 금지. **재검토:** 회고 자동화 실패가 2주 이상 지속될 때. |

**❌ 불필요 판정: 9건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`**

## 산출물
- `intake-log/2026-02-23-12h-trend-raw.json`
- `intake-log/2026-02-23-12h-trend-sweep.md`
