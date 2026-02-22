# 2026-02-22 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch`.
- **실제 상태:** `web_search`는 Brave quota/rate limit `429`.
- **대체 경로:** `web_fetch + r.jina.ai`로 수집.
- **SkillsMP:** `261,145 skills`, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com`은 429 checkpoint, 대체 `market-mcp.com`에서 `6,409` 서버/노출 `100` 확인.
- **SkillHub:** `21.6K skills / 5.6M stars` + `542 skills / 55 sources / 111k downloads` 스냅샷.
- **ClawHub:** API 1페이지 `24`개 기준, 상대 고신호 `capability-evolver(1189/19/8)` 확인.
- **VSCode Agent Skills:** 공식 `chatSkills` 경로 + 설치 신호 `copilot-mcp 81,647`, `agent-skills 1,806`, `agnix 26` 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `capability-evolver` 계열 | ⚠️ 참고만 | **Q1 필요성:** 품질개선 니즈는 있으나 현재 핵심 병목은 일일 산출/검증 루틴 안정화. **Q2 대체성:** `parallel-agents`/`subagent-dev`/`verify-before-done`로 1차 대응 가능. **Q3 비용효과:** 운영 레이어 추가 대비 즉시 ROI 불명확. **Q4 과대포장:** installsCurrent 19는 신호지만 장기 재현 데이터 부족. **재검토:** 서브에이전트 실패율 2주 연속 악화 시. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | **Q1 필요성:** 수치 신호는 강하나 즉시 해결 못 하는 구체 병목은 아님. **Q2 대체성:** `browser-cdp-automation`/`coding-agent`/기존 자동화 스택으로 대체 가능. **Q3 비용효과:** MCP 인증·보안·운영 비용 대비 즉시 생산성 개선 불확실. **Q4 과대포장:** 랭킹 수치만으로 적합성 보장 불가. **재검토:** 동일 실패가 2주 누적되고 기존 스택 복구 불가 시. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`) | ⚠️ 참고만 | **Q1 필요성:** IDE 협업 환경엔 유효하지만 현재 운영축(OpenClaw CLI)과 직접 정합 낮음. **Q2 대체성:** 내부 `skill-authoring` + clawhub/rewrite 프로세스로 대체 가능. **Q3 비용효과:** IDE 종속도 증가 대비 ROI 제한. **Q4 과대포장:** 설치수는 보조지표일 뿐 도입 근거로 불충분. **재검토:** VSCode 협업 비중 50%+ 또는 외부 온보딩 병목 명확화 시. |

**✅ 도입: 없음 (이번 회차는 즉시 도입 근거 부족)**

**❌ 불필요 판정: 4건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-16h-trend-raw.json`
- `intake-log/2026-02-22-16h-trend-sweep.md`
