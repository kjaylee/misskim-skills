# 2026-02-20 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **web_search**: Brave API 쿼터 초과(429)로 본 회차 검색 불가 → `web_fetch + direct API`로 대체.
- **SkillsMP (r.jina.ai 우회)**: 총 `239,658` skills, timeline 평균 `1,762.2`, 피크 `19,898 (@ Feb 4, 2026)`, Security `5,913`.
- **MCP Market**: `Vercel Security Checkpoint (429)`로 직접 수집 실패.
- **MCP fallback (mcp.so)**: 상단 `edgeone-pages-mcp`, `mcpadvisor`, `puppeteer`, `postgres`, `MiniMax-MCP` 등 확인.
- **SkillHub**: `21.6K Skills • 5.3M Stars`, Trending Today `gifgrep`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub**: newest 39개 샘플 다수 `installsCurrent=0`; 신규군 신뢰도 낮음.
- **VSCode Agent Skills ecosystem**: `agent skills` 검색 `1,218` 결과. `AutomataLabs.copilot-mcp` 81,333 installs.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| mcp.so `perplexity` / `search1api` 계열 (검색 대체 MCP 패턴) | ✅ 도입 | **Q1 필요성:** 현재 `web_search`가 429로 막혀 신규 소스 탐색이 실제로 중단됨. **Q2 대체성:** `web_fetch`는 URL을 이미 알아야 해서 discovery 공백이 남음. **Q3 비용효과:** API 키 1개 + 얇은 라우팅 스킬 재작성으로 복구 가능(중간 비용, 즉시 효과). **Q4 과대포장 필터:** 마켓 노출/다운로드 지표에 의존하지 않고, 외부 코드 무설치로 패턴만 흡수. |
| SkillsMP `security` 카테고리 확장 신호 (5,913) | ⚠️ 참고만 | **Q1:** 필요성은 높지만 이미 `agent-config-security-scan-lite` 트랙 진행 중. **Q2:** 신규 도입보다 기존 트랙 완성이 우선. **재검토:** 현재 보안 룰팩 탐지율이 목표치 미달일 때. |
| ClawHub `openclaw-gateway-fd-fix` | ⚠️ 참고만 | **Q1:** FD 이슈 대응 목적은 유효. **Q2:** 현재는 증상 재현 로그 부족 + 기존 운영 스크립트로 1차 대응 가능. **Q3/Q4:** installsCurrent 0, 과대해석 위험. **재검토:** `EMFILE/EBADF`가 2회 이상 재발할 때. |
| VSCode `AutomataLabs.copilot-mcp` / `formulahendry.agent-skills` / `agent-skill-ninja` | ⚠️ 참고만 | **Q1:** 생태계 확산 신호는 강함. **Q2:** 운영축이 OpenClaw CLI라 IDE 확장 직접 도입 ROI 낮음. **Q3:** 팀 표준/유지비 증가. **재검토:** VSCode 중심 협업 비중이 50% 이상일 때. |
| SkillHub Trending (`gifgrep`, `feishu-drive`, `model-usage`, `wacli`, `slack`) | ⚠️ 참고만 | **Q1/Q2:** 대부분 이미 보유/운영 중 기능군이라 순증 가치 낮음. **Q4:** 스타 급증은 품질 보증이 아니라 노출 지표 성격이 강함. **재검토:** 현재 스택 성능 저하나 기능 공백이 확인될 때. |

**❌ 불필요 판정: 51건**

## ✅ 도입 실행 계획 (검색 백업 경로)
1. **Research:** mcp.so의 `perplexity`/`search1api` 인터페이스를 분석해 필요한 최소 호출 스펙만 정리.
2. **Audit:** 키 취급/쿼터/개인정보/로그 정책 점검(민감질의 로깅 금지 기본).
3. **Rewrite:** 외부 스킬 코드 복사 없이 `misskim-skills/skills/search-fallback-mcp-lite/` 내부 재작성.
4. **Routing:** `web_search` 429/쿼터초과 시에만 fallback 활성화(정상 시 기존 경로 유지).
5. **Validation:** 동일 질의 20개 샘플에서 성공률/지연/품질 비교 후 임계치 충족 시 상시화.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-20-16h-trend-raw.json`
- `intake-log/2026-02-20-16h-trend-sweep.md`
