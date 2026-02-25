## 2026-02-26 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

### 📊 Executive Summary
- 브라우저 제약 준수: Mac Studio host 브라우저 미사용, MiniPC browser.proxy 미사용.
- 수집 경로: `web_search(1회 429 즉시 중단) + web_fetch/direct HTTP + clawhub CLI/API`.
- SkillsMP: direct `403`, r.jina `const skills=283,647`; 대체지표 `skills.sh All Time 74,583`.
- MCP Market: direct/retry 모두 `429`; fallback mirror `6,409 servers` 유지.
- SkillHub: `5.0M Stars`, `22,030 Skills Collected`, sitemap `<loc> 1,983`.
- ClawHub: API `200`(items 20), `search/explore` 정상. `moltbook-skill` 노출은 차단 정책 유지.
- VSCode Agent Skills: `copilot-mcp 82,426`, `agent-skills 1,920`, `agent-skill-ninja 584`.
- 변화 판단: 의미 있는 신규 변화 **0건**.

### 🔍 Filtered Candidates
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 중간 / Q4 높음(카운트·문구 과대포장 가능). |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능(coding-agent, browser-cdp) / Q3 낮음 / Q4 중간. |
| SkillHub 상위군 신규 도입 | ⚠️ 참고만 | Q1 부분적 / Q2 대체 가능 / Q3 낮음 / Q4 중간(스타 중심 지표). |
| ClawHub API 기반 intake 경로 강화 | ✅ 도입 | Q1 높음 / Q2 일부 불가 / Q3 높음 / Q4 중간(버즈·품질 분리 점검 필요). |
| VSCode Agent Skills 확장 직접 도입 | ⚠️ 참고만 | Q1 낮음 / Q2 대체 가능 / Q3 낮음 / Q4 중간(설치수 편향). |

**❌ 불필요 판정:** 5건

### ✅ Adopt Plan (Research → Audit → Rewrite)
1. Research: ClawHub API 신호(`downloads/installsCurrent/updatedAt`)를 intake scorecard 후보군으로 수집.
2. Audit: Molt 계열/외부 링크 포함 스킬 자동 제외 + 설명 과장/중복 여부 점검.
3. Rewrite: 검증 통과 항목만 내부 스킬로 재작성 후 `misskim-skills/`에 반영(블라인드 설치 금지).

### 보안 고정
- Molt Road/molt.host **ABSOLUTE BLOCK**
- 외부 스킬 **Research → Audit → Rewrite → misskim-skills/** 고정
