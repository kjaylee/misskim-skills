## 2026-02-25 12:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용, MiniPC browser.proxy 미사용.
- **수집 경로:** `web_search(초기 429 즉시 중단) + web_fetch/direct HTTP + r.jina + clawhub CLI/API`.
- **SkillsMP:** direct `403`, r.jina `const skills=283,647`; 대체지표 `skills.sh All Time 73,995`.
- **MCP Market:** r.jina 경유 `429` 신호 지속, direct HTTP `skillStats.totalCount=50,371`(변화 없음).
- **SkillHub:** `5.2M Stars`, `22,030 Skills Collected`, sitemap `<loc> 1,979`.
- **ClawHub:** API 첫 호출 `429` 후 1회 재시도 `200` 회복, `search/explore` 정상.
- **VSCode Agent Skills:** search 결과 `1,168`, `copilot-mcp 82,267`, `agent-skills 1,893`, `agent-skill-ninja 577`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 중간 / Q4 높음(카운트·마케팅 문구 편차). |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능(coding-agent, browser-cdp) / Q3 낮음 / Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 낮음 / Q4 중간(스타 중심 지표). |
| ClawHub API 기반 intake 경로 강화 | ✅ 도입 | Q1 높음 / Q2 일부 불가 / Q3 높음 / Q4 낮음. |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음 / Q2 대체 가능 / Q3 낮음 / Q4 중간(설치수 편향). |

**❌ 불필요 판정:** 5건

### ✅ Execution Plan (Research → Audit → Rewrite)
1. **Research:** ClawHub API `downloads/installsCurrent/updatedAt`를 intake scorecard 필드로 유지 고정.
2. **Audit:** 수집 후보를 `Molt Road/molt.host` 차단 + 중복 스택 + 유지비 기준으로 컷오프.
3. **Rewrite:** 통과 항목만 `misskim-skills/` 포맷으로 재작성(원본 blind install 금지).

### 📁 Full Report
- `intake-log/2026-02-25-12h-trend-sweep.md`
- `intake-log/2026-02-25-12h-trend-raw.json`
