# 2026-02-22 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search`는 Brave quota 429.
- **MiniPC browser.proxy:** `target=node`로 점검했지만 openclaw 프로필 시작 실패 + chrome relay 탭 미연결.
- **대체 경로:** `r.jina.ai + direct API + CLI + HTML 파싱`.
- **소스 스냅샷:**
  - **SkillsMP:** 총 `239,658`, 평균 `1,826.2`, 피크 `29,797 @ 2026-02-19`, Security `5,913`, `security` 검색 `10,280`.
  - **MCP Market:** `mcpmarket.com`은 429 checkpoint, 대체 도메인 `market-mcp.com`에서 `/mcp/*` `100`개 및 signal 수집(예: `archon 19,110`, `triggerdev 18,629`, `chrome-devtools 18,288`, `contextforge-gateway 4,009`).
  - **SkillHub:** 홈페이지 `15,000+` 주장 + `@skill-hub/cli` trending/latest/search JSON 수집.
  - **ClawHub:** API 일시 성공 후 rate limit. trending/downloads/newest 샘플 확보.
  - **VSCode Agent Skills:** extensionquery 기준 `copilot-mcp 81,558`, `agent-skills 1,796`, `agent-skill-ninja 562`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub CLI non-interactive JSON fallback (`--json --no-select`) | ✅ 도입 | **Q1 필요성:** web_search 429 + MiniPC proxy 미가용 시 스윕이 멈춤. **Q2 대체성:** clawhub 단일 소스로는 멀티마켓 커버 부족. **Q3 비용효과:** npx 호출만으로 저비용 즉시 적용 가능. **Q4 과대포장 필터:** 홈페이지 문구가 아니라 CLI 실출력으로 검증 가능. |
| MCP Market detail-page signal harvester (`market-mcp.com/mcp/<slug>`) | ✅ 도입 | **Q1 필요성:** MCP Market 메인 차단 시 signal 공백 발생. **Q2 대체성:** 기존 링크 나열만으로 우선순위 비교가 어려움. **Q3 비용효과:** detail 페이지 파싱만으로 상위 signal 자동 추출 가능. **Q4 과대포장 필터:** 마케팅 문구 대신 수치(19110/18629/18288) 기반 정렬 가능. |
| MCP Market `contextforge-gateway` | ⚠️ 참고만 | MCP+REST 통합 니즈는 있으나 현재는 OpenClaw gateway + mcporter로 대체 가능. **재검토:** MCP 서버 운영 수가 15개+로 늘고 인증/관측 병목이 확인될 때. |
| VSCode `copilot-mcp / agent-skills / agent-skill-ninja` 확장군 | ⚠️ 참고만 | 설치 신호는 강하지만 OpenClaw CLI 중심 운영과 정합 낮음. **재검토:** VSCode 협업 비중이 50% 이상으로 전환될 때. |
| ClawHub newest `kagi-fastgpt / kagi-summarizer` | ⚠️ 참고만 | 검색 fallback 니즈는 맞지만 현재 실사용 신호가 `downloads/installs/stars = 0`. **재검토:** 2주 연속 installsCurrent 증가 + 안정 업데이트 확인 시. |

**❌ 불필요 판정: 23건**

## ✅ 도입 실행 계획 (상세)

### 1) SkillHub CLI fallback 경로 정식 편입
1. **Research:** `search/trending/latest --json --no-select` 출력 스키마 고정.
2. **Audit:** 수집 필드를 `slug`, `repo_url`, `github_stars` 중심으로 제한(홍보 문구 제외).
3. **Rewrite:** `misskim-skills/` intake 루틴에 read-only fallback으로 연결.
4. **Validate:** 다음 3회 스윕에서 web_search 장애 시 후보 10건 이상 확보되는지 검증.

### 2) MCP Market signal harvester 도입
1. **Research:** `market-mcp.com` 홈 `/mcp/*` 링크 + detail signal 추출 규칙 정의.
2. **Audit:** 문자열 파싱 오탐 방지 규칙(연도/UI 숫자 제외) 적용.
3. **Rewrite:** `misskim-skills/` intake 단계에서 MCP 후보에 signal score 부여.
4. **Validate:** 상위 10개 후보의 수동 점검 일치율 90% 이상이면 유지.

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-00h-trend-raw.json`
- `intake-log/2026-02-22-00h-trend-sweep.md`
