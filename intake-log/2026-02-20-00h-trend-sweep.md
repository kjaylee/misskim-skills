# 2026-02-20 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: Cloudflare 차단으로 직접 브라우저 접근 불가 → `r.jina.ai` 우회 수집. **총 239,658 skills**(홈/타임라인 일치). 상단 안내에 *top 5000 제한* 표기.
- **MCP Market**: 메인 HTML 파싱. **21,507 servers** 확인. `Latest MCP Servers` 상단 `NotebookLM`, `Marketer`, `Ocean`, `Substack Publisher`, `Rug Munch Intelligence`, `FastAPI` 노출.
- **SkillHub (skillhub.club)**: **21.6K skills / 4.3M stars**. Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack` (OpenClaw 기존 스택).
- **ClawHub**: Convex 공개 API(`/api/v1/skills`) 샘플 확인. `Docs Feeder`, `Z.AI Web Search`, `ClawDog Backup(의심 플래그)` 등 신규 노출.
- **VSCode Agent Skills extension**: `formulahendry.agent-skills` **1,761 installs**, **평점 5.0(리뷰 1)**, **v0.0.2(2025-12-26)**.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `Docs Feeder` | ⚠️ 참고만 | **Q1 필요성:** 문서 수집 자동화 수요는 있으나 긴급 병목은 아님. **Q2 대체성:** `web_fetch`/`summarize` + 내부 문서 체계로 1차 대응 가능. **Q3 비용효과:** 외부 스킬 도입·보안 리뷰 비용 대비 즉시 효과 제한. **Q4 과대포장:** 다운로드 0, 검증 부족. **재검토:** 문서 수집 실패율이 주간 임계치(>10%) 초과 시. |
| ClawHub `Z.AI Web Search` | ⚠️ 참고만 | **Q1 필요성:** Brave 429 발생으로 검색 fallback 니즈 존재. **Q2 대체성:** 현재는 `web_fetch`/URL 직접 탐색으로 우회 가능하지만 범용 검색은 부족. **Q3 비용효과:** API 키·쿼터·운영비 추가 필요. **Q4 과대포장:** 다운로드 낮아 품질 신뢰 부족. **재검토:** 검색 실패/쿼터 초과가 연속 3회 이상 발생 시. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | **Q1 필요성:** Substack 채널 운영이 현재 핵심 병목이 아님. **Q2 대체성:** Substack 자체 운영이 없으므로 기능 활용 여지 제한. **Q3 비용효과:** 도입 대비 당장 ROI 낮음. **Q4 과대포장:** 신뢰 지표 부족. **재검토:** Substack을 분기 KPI 채널로 승격할 때. |
| MCP Market `Task Master` | ⚠️ 참고만 | **Q1 필요성:** 작업 오케스트레이션은 필요하나, **Q2** 기존 `queue-manager`+서브에이전트 체계가 핵심 수요 충족. **Q3 비용효과:** MCP 추가 도입비 대비 즉시 효과 불명확. **Q4 과대포장:** GitHub 스타(4,465)만으로 품질 보장 불가. **재검토:** 큐 충돌/우선순위 역전이 주 3회 이상 발생 시. |

**❌ 불필요 판정: 10건**
- (요약) MCP Market 최신군 다수(NotebookLM/Marketer/Ocean/Rug Munch/ FastAPI) + ClawHub 신규 저신뢰 항목(backup/telegram/polymarket/openbot 등) + SkillHub 상위군(이미 보유) → 현재 문제 해결과 직접 정합 부족.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
