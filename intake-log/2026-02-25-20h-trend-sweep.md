## 2026-02-25 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- **브라우저 제약 준수:** Mac Studio host 브라우저 미사용, MiniPC browser.proxy 미사용.
- **수집 경로:** `web_search(1회 429 즉시 중단) + web_fetch/direct HTTP + clawhub CLI/API`.
- **SkillsMP:** direct `403`, r.jina `const skills=283,647`; 대체지표 `skills.sh All Time 74,328`.
- **MCP Market:** direct/retry 모두 `429`; fallback mirror `6,409 servers` 유지.
- **SkillHub:** `4.8M Stars`, `22,030 Skills Collected`, sitemap `<loc> 1,983`.
- **ClawHub:** API `200`(items 18), `search/explore` 정상.
- **VSCode Agent Skills:** API search `1,296`, `copilot-mcp 82,370`, `agent-skills 1,912`, `agent-skill-ninja 584`.
- **변화 판단:** 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 중간 / Q4 높음(카운트·문구 과대포장 가능). |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능(coding-agent, browser-cdp) / Q3 낮음 / Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 낮음 / Q4 중간(스타 중심 지표). |
| ClawHub API 기반 intake 경로 강화 | ✅ 도입 | Q1 높음 / Q2 일부 불가 / Q3 높음 / Q4 중간(버즈·품질 분리 점검 필요). |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음 / Q2 대체 가능 / Q3 낮음 / Q4 중간(설치수 편향). |

**❌ 불필요 판정:** 5건

### ✅ 실행계획 (Research → Audit → Rewrite)
1. **Research:** ClawHub API `items/stats(updatedAt, installsCurrent, downloads)`를 intake scorecard 입력 필드로 표준화.
2. **Audit:** 신규 slug는 보안/중복/ROI 3게이트(보안패턴, 기존 스택 대체성, 유지비) 통과 전 채택 금지.
3. **Rewrite:** 통과 항목만 내부형으로 재작성해 `misskim-skills/`에 편입(외부 원본 blind install 금지).

### 📁 Artifacts
- `intake-log/2026-02-25-20h-trend-sweep.md`
- `intake-log/2026-02-25-20h-trend-raw.json`
