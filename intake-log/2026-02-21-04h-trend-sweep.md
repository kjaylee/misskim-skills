# 2026-02-21 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **web_search:** Brave quota/rate limit 429로 실패 → `web_fetch + direct API`로 대체.
- **SkillsMP:** 카테고리 합 기준 `254,084` skills, `Security 5,913`.
- **MCP Market:** `Vercel Security Checkpoint 429`로 본회차 직접 수집 실패.
- **MCP fallback(mcp.so):** `17,775` servers, 검색 관련 `Search1API/Perplexity/Serper/Jina/Playwright` 노출.
- **SkillHub:** `21.6K Skills / 4.6M Stars`, Trending 상위 `gifgrep/feishu-drive/model-usage/wacli/slack`.
- **ClawHub:** `.com` 인기군은 고다운로드(예: Tavily 24.3k), `.ai` latest 15개는 `installsCurrent=0` 집중.
- **VSCode Agent Skills:** 필터링 29개, `AutomataLabs.copilot-mcp` `81,453 installs`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so 검색군(`Search1API/Perplexity/Serper/Jina`) 기반 **검색 fallback 브로커 패턴** | ✅ 도입 | **Q1 필요성:** 현재 `web_search` 429로 신규 탐색이 실제 중단. **Q2 대체성:** `web_fetch` 단독은 URL 선인지식이 필요해 discovery 공백이 큼. **Q3 비용효과:** 외부 스킬 설치 없이 내부 스킬로 어댑터만 재작성 가능(중간비용/즉시효과). **Q4 과대포장 필터:** 인기 지표가 아니라 “검색 실패 복구율”로 성능 검증 가능. |
| ClawHub `Ontology` (20.1k downloads, ⭐31) | ⚠️ 참고만 | 구조화 메모리 장점은 있으나 현재 `openclaw-mem + memory-management`로 핵심 요구를 충족. **재검토:** 크로스-스킬 엔터티 의존 그래프가 실제 병목(연결 누락/충돌)으로 측정될 때. |
| SkillsMP `Security` 대분류(5,913) 확장 신호 | ⚠️ 참고만 | 니즈는 높지만 범주가 넓어 저품질 혼입이 큼. **재검토:** 내부 intake 보안 게이트 오탐/미탐 지표가 목표 미달일 때. |
| VSCode `AutomataLabs.copilot-mcp` 및 Agent Skills 확장군 | ⚠️ 참고만 | 설치수는 강하지만 VSCode 종속. 운영축(OpenClaw CLI + subagent)과 정합 낮음. **재검토:** VSCode 중심 협업 비중 50%+ 전환 시. |
| ClawHub `.ai` latest 신규군(예: `plans-methodology`, `product-launch`) | ⚠️ 참고만 | 대부분 `installsCurrent=0`으로 실사용 신호가 약함. **재검토:** 2주 연속 `installsCurrent` 증가 + 유지보수 릴리스 확인 시. |

**❌ 불필요 판정: 37건**

## ✅ 도입 실행 계획 (상세)
1. **Research:** 검색 fallback 브로커 요구사항 확정 (`web_search` 실패코드 429/5xx 매핑 + fallback 우선순위).
2. **Audit:** 키 보관 방식, 로그 마스킹, 도메인 allowlist, 요청당 비용 상한, 개인정보 비기록 점검.
3. **Rewrite:** `misskim-skills/skills/search-fallback-broker-lite/` 내부 재작성 (외부 코드/스크립트 무복사).
4. **Routing:** 기본은 `web_search`, 실패 조건(429/쿼터초과/타임아웃)에서만 fallback 발동.
5. **Validation:** 샘플 질의 20개 A/B(성공률·지연·요약품질) 후 상시적용 여부 결정.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-04h-trend-raw.json`
- `intake-log/2026-02-21-04h-trend-sweep.md`
