# 2026-02-21 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch` 시도.
- **실제 상태:** `web_search` 429(quota), MiniPC browser.proxy 노드 연결 불가.
- **대체 경로:** direct API/CLI/curl RSS로 수집 지속.
- **핵심 스냅샷:**
  - SkillsMP: `sitemap 684 URLs`, 최신 lastmod `2026-02-06` (본 페이지는 Cloudflare 차단).
  - MCP Market: 홈에서 `/mcp/*` 링크 `100`개 확인. 샘플 신호 `chrome-devtools(18288)`, `claude-flow(13562)`, `contextforge-gateway(4009)`.
  - SkillHub(Agent Skills): 홈페이지 `15,000+` 주장 확인 + `@skill-hub/cli` 비대화식 JSON 수집 성공.
  - ClawHub: `explore --json` 기준 샘플 `56개(47 unique)`.
  - VSCode Agent Skills: extensionquery 샘플 `24개(22 unique)`, `copilot-mcp 81,534 installs`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `@skill-hub/cli` 비대화식 intake 경로 | ✅ 도입 | **Q1 필요성:** Brave 429 + MiniPC disconnect 동시 발생 시 discovery가 멈춤. **Q2 대체성:** clawhub 단일 소스만으로는 멀티마켓 백업 불충분. **Q3 비용효과:** npx + `--json --no-select`만으로 즉시 적용 가능(저비용). **Q4 과대포장 필터:** CLI 실출력(슬러그/깃허브 스타)로 검증 가능. |
| MCP Market `contextforge-gateway` | ⚠️ 참고만 | MCP/REST 통합 가치는 있으나 현 단계에서는 OpenClaw gateway + 기존 도구 조합으로 대체 가능. **재검토:** MCP 서버 운영 수가 15개+로 증가해 관측/인증 병목이 생길 때. |
| ClawHub `find-skills` 및 상위 탐색군 | ⚠️ 참고만 | 탐색 니즈는 맞지만 현재 `clawhub search/explore + intake-log`와 기능 중복. **재검토:** 내부 탐색 리드타임이 2배 이상 악화될 때. |
| VSCode `copilot-mcp / agent-skills` 확장군 | ⚠️ 참고만 | 설치 신호는 강하나 OpenClaw CLI 중심 운영과 정합 낮음. **재검토:** VSCode 협업 비중이 50% 이상으로 전환될 때. |
| SkillsMP direct intake | ⚠️ 참고만 | 필요한 소스지만 이번 회차는 Cloudflare 차단으로 실데이터 검증이 제한됨. **재검토:** 안정 접근 경로 확보 후 최신 50개 재평가 시. |

**❌ 불필요 판정: 27건**

## ✅ 도입 실행 계획 (상세)
1. **Research:** SkillHub CLI의 `search --json --no-select` 출력 스키마를 intake 표준 필드로 매핑.
2. **Audit:** 외부 출력 필드 중 신뢰 가능한 것만 사용(`slug`, `repo_url`, `github_stars`), 마케팅 텍스트는 제외.
3. **Rewrite:** `misskim-skills/` 내부 수집 루틴에서 fallback 소스로 SkillHub CLI를 read-only 연결.
4. **Validate:** 다음 3회 스윕에서 `web_search` 장애 시에도 후보 최소 10건 이상 확보되는지 검증.
5. **Gate:** 안정성 기준 충족 시 정규 소스 승격, 미충족 시 즉시 롤백.

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-20h-trend-raw.json`
- `intake-log/2026-02-21-20h-trend-sweep.md`
