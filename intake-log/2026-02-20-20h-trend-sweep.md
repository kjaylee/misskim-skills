# 2026-02-20 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **web_search**: Brave API quota 초과(429) 지속 → `web_fetch + direct API/CLI`로 대체.
- **SkillsMP (r.jina.ai 우회)**: `239,658` skills, timeline 평균 `1,762.2`, 피크 `19,898 (@ Feb 4, 2026)`, Security `5,913`.
- **MCP Market**: `Vercel Security Checkpoint`로 직접 수집 차단(429).
- **MCP fallback (mcp.so)**: 상단에 `search1api`, `perplexity`, `serper-mcp-server`, `brave-search` 확인.
- **SkillHub**: `21.6K Skills • 5.2M Stars`, Trending Today `gifgrep`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub**: newest 39개 샘플 재수집. 신규군 다수가 `installsCurrent=0`.
- **VSCode Agent Skills ecosystem**: 검색 `1,219` 결과, `AutomataLabs.copilot-mcp` `81,378 installs`, `formulahendry.agent-skills` `1,772 installs`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so `search1api/perplexity` 기반 **검색 fallback 패턴** | ✅ 도입 | **Q1 필요성:** 현재 `web_search` 429로 discovery가 실제 중단됨. **Q2 대체성:** `web_fetch` 단독은 URL 선인지식이 필요해 신규 탐색 공백 발생. **Q3 비용효과:** 외부 코드 설치 없이 내부 라우팅 스킬 재작성으로 빠른 복구 가능(중간 비용/즉시 효과). **Q4 과대포장 필터:** 다운로드 지표보다 “실제 장애(429) 해소”라는 기능 검증 축이 명확. |
| SkillsMP `Security` 카테고리 확장 신호 | ⚠️ 참고만 | 필요성은 높지만 이미 내부 보안 스캔 라인과 중복. **재검토 조건:** 현재 보안 룰팩 탐지율/오탐률 목표 미달 시. |
| ClawHub `x-twitter-scraper` | ⚠️ 참고만 | 수요는 “X 채널 리서치 자동화”일 때만 유효. 현재 핵심 KPI(게임/도구 매출 전환) 직접 기여가 약함. **재검토 조건:** X 기반 퍼포먼스 마케팅 실험 시작 시. |
| ClawHub `secureclaw-skill` | ⚠️ 참고만 | 보안 프레임워크 주장 강하나 `downloads 5 / installsCurrent 0` 신뢰 신호 약함. **재검토 조건:** 내부 보안 파이프라인에서 커버리지 공백이 확인될 때. |
| VSCode `copilot-mcp / agent-skills` 확장군 | ⚠️ 참고만 | 설치 수는 증가 중이나 운영축은 OpenClaw CLI. IDE 종속 도입 시 유지비 증가. **재검토 조건:** VSCode 중심 협업 비중 50%+ 전환 시. |

**❌ 불필요 판정: 57건**

## ✅ 도입 실행 계획 (상세)
1. **Research**: `search1api/perplexity/serper` 호출 스펙과 실패 코드(429/5xx) 매핑 정리.
2. **Audit**: 키 저장·로그 마스킹·쿼터 상한·개인정보 비기록 정책 체크리스트 작성.
3. **Rewrite**: 외부 코드 복사 없이 `misskim-skills/skills/search-fallback-mcp-lite/` 내부 재작성.
4. **Routing**: `web_search` 정상 시 기본 경로 유지, `429`/쿼터 초과시에만 fallback 호출.
5. **Validation**: 동일 질의 20개 샘플 A/B (`성공률`, `지연`, `요약 품질`) 비교 후 상시화 결정.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-20-20h-trend-raw.json`
- `intake-log/2026-02-20-20h-trend-sweep.md`
