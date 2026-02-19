# 2026-02-20 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: `r.jina.ai` 우회 수집. **239,658 skills** / 평균 주기 **1,762.2** / 피크 **19,898 (@ Feb 4, 2026)**.
- **MCP Market**: 웹페치 경로는 체크포인트 이슈가 있었지만, 원문 HTML 재수집으로 **21,507 servers** 확인. Latest 상단: `NotebookLM`, `Marketer`, `Ocean`, `Substack Publisher`, `Rug Munch Intelligence`, `FastAPI`.
- **SkillHub (skillhub.club)**: **21.6K skills / 4.0M stars**. Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub**: nonSuspicious 상위 + API 샘플 확인. `tavily-search`는 **downloads 23,180 / installsCurrent 133 / stars 71**. 최신 신규군은 다수 0~1 installs.
- **VSCode Agent Skills 생태계**: `copilot-mcp` **81,251 installs**, `formulahendry.agent-skills` **~1.75K installs**(v0.0.2, 2025-12-26, rating 5.0/1).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `tavily-search` | ✅ 도입 | **Q1 필요성:** Brave `web_search`가 실제 429/쿼터초과 상태라 검색 공백이 반복됨. **Q2 대체성:** `web_fetch`는 URL을 이미 알아야 해서 범용 검색을 대체 못 함. **Q3 비용효과:** API 키/소액 과금은 필요하지만, 조사 실패 재시도 비용(시간) 절감이 더 큼. **Q4 과대포장:** 단순 마케팅이 아닌 사용 신호(23,180 downloads, installsCurrent 133, stars 71) 확인. |
| MCP Market `FastAPI` | ⚠️ 참고만 | **Q1:** API 서버 자동화 니즈는 있음. **Q2:** 현재 `openapi-tool-scaffold`/기존 코드 스택으로 1차 대응 가능. **Q3:** 추가 MCP 도입 대비 즉시 ROI 불명확. **Q4:** 최신 노출만으로 품질 단정 불가. **재검토:** API 프로젝트 동시 3개+로 병목 발생 시. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | **Q1:** 채널 확장 니즈는 있으나 현재 핵심 병목(수익화/배포 자동화)과 직접 정합 낮음. **Q2:** 당장 대체 불필요(운영 채널 아님). **Q3:** 도입비 대비 회수 불확실. **Q4:** 최신 노출 신호만 존재. **재검토:** Substack이 분기 KPI 채널로 승격될 때. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | **Q1:** 설치 수(81K+)는 강한 확산 신호. **Q2:** 현재 운영축은 OpenClaw CLI 중심이라 VSCode 확장 직접 도입 이득 제한. **Q3:** IDE 종속 운영비가 큼. **Q4:** 대규모 설치 ≠ 우리 환경 적합성. **재검토:** VSCode 워크플로 비중이 50% 이상으로 올라갈 때. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | **Q1:** 멀티 저장소 브라우징 기능은 유용. **Q2:** 이미 ClawHub/SkillHub/직접 리라이트 루틴으로 핵심 흐름 대응 중. **Q3:** 업데이트 정체(v0.0.2, 2025-12)로 도입 효과 제한. **Q4:** 평점 표본 1개로 신뢰도 낮음. **재검토:** 내부 skill 탐색 리드타임이 주간 임계치 초과 시. |

**❌ 불필요 판정: 18건**
- 최신 저신뢰 신규군(0~1 installs), 기존 보유 스킬과 중복되는 SkillHub 상위군, 도메인 비정합 MCP/VSCode 확장 다수 제외.

## ✅ 도입 실행 계획
### `search-fallback-tavily-lite` (내부 재작성)
1. **Research**: `tavily-search`에서 필요한 최소 기능(검색/뉴스/URL extract)만 사양 추출.
2. **Audit**: API 키 저장 정책, 호출 도메인 allowlist, 비용 상한(일일/월간) 정의.
3. **Rewrite**: 외부 코드 무복사로 `misskim-skills/skills/search-fallback-tavily-lite/` 내부 구현.
4. **Integration**: `web_search` 429 또는 quota 초과 시에만 fallback 발동하도록 조건부 연결.
5. **Validation**: 1주 파일럿(실패율·응답시간·비용) 통과 시 상시 운영.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
- MCP Market 수집 실패 시: **MiniPC 브라우저 프록시 또는 web_fetch/원문 HTML 파싱 fallback만 허용**
