## 2026-02-25 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용, MiniPC relay 미연결로 browser.proxy 미사용.
- **수집 경로:** `web_fetch + r.jina.ai + direct HTTP(UA) + clawhub CLI/API`.
- **SkillsMP:** `skillsmp.com` 노출치 `const skills=283,647` / `270000++`(자체 마케팅 문구), `skills.sh All Time 73,867`.
- **MCP Market:** `web_fetch 429` 지속, direct HTTP 기준 `skillStats.totalCount=50,371`; mirror(`market-mcp.com`) `6,409 MCP servers` 유지.
- **SkillHub:** `4.9M Stars`, `22,030 Skills Collected`, sitemap `<loc> 1,979`.
- **ClawHub:** API `/api/v1/skills` `200` 회복(직전 429), CLI `explore/search` 정상.
- **VSCode Agent Skills:** search 결과 `1,164`, `copilot-mcp 82.2K`, `agent-skills 1.9K`, `agent-skill-ninja 573`.
- **변화 판단:** 의미 있는 신규 변화 **2건**(ClawHub API 회복, SkillHub 수집량 +466).

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적(탐색 가치는 큼), Q2 가능(skills.sh/ClawHub 대체), Q3 중간(검증비용 큼), Q4 높음(카운트 불일치/과장 가능성). |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(coding-agent/browser-cdp), Q3 낮음(MCP 운영비), Q4 중간(랭킹 중심 과대포장 가능). |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적, Q2 가능(기존 스킬 다수 중복), Q3 낮음(선별비용↑), Q4 중간(스타/수집량 중심 신호). |
| ClawHub API 기반 intake 경로 강화 | ✅ 도입 | Q1 높음(수집 안정성 직접 개선), Q2 일부 불가(API 신호 대체 어려움), Q3 높음(저비용), Q4 낮음(직접 지표 확인 가능). |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음(OpenClaw CLI 중심), Q2 가능, Q3 낮음, Q4 중간(설치수 편향). |

**❌ 불필요 판정:** 5건

### ✅ Execution Plan (Research → Audit → Rewrite)
1. **Research:** ClawHub API 신호(`downloads/installsCurrent/updatedAt`)를 intake scorecard 필드로 고정.
2. **Audit:** 상위 10개 후보를 `Molt Road/molt.host` + 중복 스택 + 유지비(의존성) 기준으로 컷오프.
3. **Rewrite:** 통과 항목만 `misskim-skills/` 내부 포맷으로 재작성(원본 blind install 금지).

### 📁 Full Report
- `intake-log/2026-02-25-08h-trend-sweep.md`
- `intake-log/2026-02-25-08h-trend-raw.json`
