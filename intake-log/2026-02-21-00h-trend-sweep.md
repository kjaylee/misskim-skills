# 2026-02-21 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **web_search:** Brave quota/rate limit 429로 실패.
- **MiniPC browser.proxy:** relay 탭 미연결로 사용 불가 → `web_fetch + direct API/CLI` 대체.
- **SkillsMP:** `239,658` skills 확인, Security 하위 `5,913`.
- **MCP Market:** Vercel Security Checkpoint(429)로 본회차 직접 수집 실패.
- **SkillHub (skillhub.club):** `21.6K Skills / 5.0M Stars`, Trending 상단 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **ClawHub API:** 최근 신규군 다수 저신뢰(`apprentice` 2 downloads, `tweet-processor` 3 downloads).
- **VSCode Agent Skills:** `copilot-mcp` 81,414 installs, `agent-skills` 1,776 installs.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub CLI + ClawHub `search-cluster`에서 보인 **멀티소스 검색 fallback 패턴** | ✅ 도입 | **Q1 필요성:** 현재 `web_search` 429로 신규 탐색이 실제 중단됨. **Q2 대체성:** 기존 `web_fetch` 단독은 URL 사전지식이 필요해 discovery 공백이 큼. **Q3 비용효과:** 외부 스킬 설치 없이 내부 라우팅 스킬로 재작성 가능(중간 비용/즉시 효과). **Q4 과대포장 필터:** 스타/다운로드가 아니라 현재 장애(검색 중단) 해소 여부로 검증 가능. |
| VSCode `AutomataLabs.copilot-mcp` / `formulahendry.agent-skills` | ⚠️ 참고만 | 설치수 신호는 강하지만 VSCode 확장 의존. 현재 운영축(OpenClaw CLI + subagent)과 직접 정합 낮음. **재검토:** VSCode 중심 협업 비중 50%+ 전환 시. |
| SkillsMP `Security` 카테고리 확장(5,913) | ⚠️ 참고만 | 보안 니즈는 분명하나 범주가 넓고 저품질 혼입 가능성 큼. **재검토:** 내부 intake 보안 게이트 탐지율 미달 시. |
| ClawHub `Apprentice` (watch-me-once 학습) | ⚠️ 참고만 | 컨셉은 유효하지만 실사용 신호가 매우 약함(2 downloads/0 current installs). **재검토:** 2주 연속 installsCurrent 증가 + 유지보수 업데이트 확인 시. |

**❌ 불필요 판정: 14건**

## ✅ 도입 실행 계획 (상세)
1. **Research:** SkillHub CLI 검색 UX(`npx @skill-hub/cli search`) + ClawHub `search-cluster` 입력/출력 패턴을 사양화.
2. **Audit:** 키/쿼터/로그 마스킹/도메인 allowlist 점검. Molt 계열(`molt.host`, `moltbook`) 하드 차단 룰 고정.
3. **Rewrite:** 외부 코드 무복사 원칙으로 `misskim-skills/skills/search-fallback-federation-lite/` 내부 재작성.
4. **Routing:** 기본은 `web_search`; `429` 또는 quota 초과 시에만 fallback 경로 발동.
5. **Validation:** 샘플 질의 20개로 성공률·지연·요약 품질 A/B 측정 후 상시 적용 여부 결정.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-00h-trend-raw.json`
- `intake-log/2026-02-21-00h-trend-sweep.md`
