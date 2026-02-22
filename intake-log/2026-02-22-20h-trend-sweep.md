# 2026-02-22 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch`.
- **실제 상태:** `web_search`는 Brave quota/rate limit `429`.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145 skills`, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com` 429 checkpoint, 대체 `market-mcp.com`에서 `6,409` 서버(`100` 노출).
- **SkillHub:** `21.6K skills / 5.3M stars`, Trending Top5 급등 확인.
- **ClawHub:** API `429`, 홈/미러 기준 popular/highlighted 신호 수집.
- **VSCode Agent Skills:** 공식 docs + marketplace API 기준 `copilot-mcp 81,666`, `agent-skills 1,805`, `agnix 27`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market 상위 자동화군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | **Q1 필요성:** 수치 신호는 강하지만 현재 병목(일일 산출/QA 안정화) 직접 해결은 아님. **Q2 대체성:** `browser-cdp-automation`/`coding-agent`/기존 OpenClaw 자동화로 대체 가능. **Q3 비용효과:** MCP 온보딩·보안·운영비 대비 즉시 ROI 불명확. **Q4 과대포장:** 랭킹 수치만으로 환경 적합성 보장 불가. **재검토:** 동일 실패 2주 누적 + 기존 스택 복구 불가 시. |
| ClawHub `ontology` | ⚠️ 참고만 | **Q1 필요성:** 구조화 메모리 니즈는 있으나 현 병목은 throughput/실행 루틴. **Q2 대체성:** `openclaw-mem` + `memory-management` + RAG 루틴으로 1차 대응 가능. **Q3 비용효과:** 그래프 메모리 운영복잡도 대비 즉시 생산성 상승 제한적. **Q4 과대포장:** 다운로드(25.7k) 신호는 강하지만 장기 운영성 데이터 부족. **재검토:** 회상 정확도 KPI 2주 연속 미달 시. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`) | ⚠️ 참고만 | **Q1 필요성:** IDE 협업엔 유효하나 현재 운영축(OpenClaw CLI)과 정합 낮음. **Q2 대체성:** `skill-authoring` + clawhub/rewrite 프로세스로 핵심 기능 대체 가능. **Q3 비용효과:** IDE 종속성 증가 대비 ROI 제한. **Q4 과대포장:** 설치수는 보조지표(품질/안정성 보증 아님). **재검토:** VSCode 협업 비중 50%+ 또는 외부 온보딩 병목 명확화 시. |
| SkillHub S-rank 군 (`systematic-debugging`, `file-search`, `skill-creator`) | ⚠️ 참고만 | **Q1 필요성:** 방법론 가치 있음. 다만 즉시 해결할 신규 공백은 제한적. **Q2 대체성:** 동일 계열 스킬/루틴을 이미 보유·내재화. **Q3 비용효과:** 신규 채택보다 기존 루틴 고도화가 비용효율 우위. **Q4 과대포장:** S-rank·star 급등은 자체 평가 지표라 마케팅성 과대포장 가능. **재검토:** 디버깅/탐색 실패율 목표치 초과 시. |

**✅ 도입: 없음 (이번 회차는 즉시 도입 근거 부족)**

**❌ 불필요 판정: 4건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-20h-trend-raw.json`
- `intake-log/2026-02-22-20h-trend-sweep.md`
