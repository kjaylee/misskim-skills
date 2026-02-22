# 2026-02-23 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **MiniPC browser.proxy 시도:** `target=node`만 사용했으나 Chrome relay에 attach된 탭이 없어 사용 불가.
- **우선 수집:** `web_search + web_fetch`.
- **실제 상태:** `web_search`는 Brave quota `429`로 실패.
- **대체 경로:** `web_fetch + r.jina.ai`.
- **SkillsMP:** `261,145` skills, Peak `29,027`(@ Feb 19, 2026), Tools `71,840`.
- **MCP Market:** `mcpmarket.com`은 429 checkpoint(원본 차단). 보조 신호로 `mcpmarket.cn` 상위 hosted `136` 확인.
- **SkillHub:** `21.6K skills / 5.2M stars`, Trending Top5(`feishu-doc`, `discord`, `nano-banana-pro`, `gifgrep`, `feishu-drive`).
- **ClawHub:** API 샘플 `24`개 확인, popular 상위 `tavily-search (26,479/99★)`.
- **VSCode Agent Skills extension:** `formulahendry.agent-skills` installs `1,807`, rating `5.0`(1 review), v`0.0.2`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `tavily-search` | ✅ 도입 | **Q1 필요성:** Brave 검색 429가 반복되어 검색 fallback 공백이 현재 실제 병목. **Q2 대체성:** `web_fetch`는 URL 기반이라 검색 대체 불완전. **Q3 비용효과:** API 비용은 있지만 조사/브리핑 중단 리스크를 즉시 낮춤. **Q4 과대포장 필터:** 다운로드/별점 신호는 참고만, blind install 없이 `Research→Audit→Rewrite` 전제. **실행계획:** (1) upstream 리서치 (2) 보안 감사 (3) `misskim-skills/`로 최소권한 재작성 (4) 7일 파일럿(Brave 실패 시만 호출) (5) 성공률 개선 미달 시 롤백. |
| MCP Market fallback 상위군 (`Context 7`, `n8n-mcp`) | ⚠️ 참고만 | **Q1:** 가치는 있으나 최우선 병목은 검색 fallback. **Q2:** 기존 `web_fetch/summarize/coding-agent`로 1차 대체 가능. **Q3:** MCP 온보딩·운영비 대비 즉시 ROI 불명확. **Q4:** 원본 `mcpmarket.com` 차단으로 신호 신뢰도 제한. **재검토:** 문서 버전 불일치/자동화 실패가 주 3회 이상 누적 시. |
| SkillHub 방법론군 (`systematic-debugging`, `file-search`) | ⚠️ 참고만 | **Q1:** 방법론적 가치는 있음. **Q2:** 기존 디버깅·검색 루틴과 중복 높음. **Q3:** 신규 도입보다 기존 루틴 강화가 저비용. **Q4:** S-rank/스타는 품질 보증 지표가 아님. **재검토:** 디버깅 재시도율 목표 초과 시. |
| VSCode `Agent Skills` extension | ⚠️ 참고만 | **Q1:** IDE 중심 협업엔 유효. **Q2:** 현재 운영축(OpenClaw CLI)과 중복 큼. **Q3:** IDE 종속 비용 대비 즉시 효과 제한. **Q4:** 설치수(1,807) 대비 리뷰 1건으로 검증 신호 약함. **재검토:** VSCode 협업 비중 50% 이상 상승 시. |

**❌ 불필요 판정: 6건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`**

## 산출물
- `intake-log/2026-02-23-00h-trend-raw.json`
- `intake-log/2026-02-23-00h-trend-sweep.md`
