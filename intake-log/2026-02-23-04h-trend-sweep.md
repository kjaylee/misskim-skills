# 2026-02-23 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **MiniPC browser.proxy:** `target=node` 점검했으나 relay attach 미연결로 실사용 불가.
- **우선 경로:** `web_search + web_fetch` 시도.
- **실제 상태:** `web_search`는 Brave quota/rate-limit `429`로 실패.
- **대체 경로:** `web_fetch + r.jina.ai + 검색 스니펫`.
- **SkillsMP:** `269,875` skills, peak `29,027`(@ 2026-02-19), 최근 변경은 타임라인 알고리즘/페이지네이션 캡(2026-02-06).
- **MCP Market:** 원본 `mcpmarket.com`은 Vercel checkpoint `429`로 직접 상세 수집 실패(리더보드/일간 랭킹 존재 신호만 확보).
- **SkillHub:** `311 tools` (`233 MCP / 78 Skills`).
- **ClawHub:** highlighted `Trello/Slack/Caldav/Answer Overflow`, popular `gog/ontology/summarize`.
- **VSCode Agent Skills extension:** 검색 `1,128` 결과, 상위 `copilot-mcp(81.7k)`, `agent-skills(1.8k)`, `agnix(28)`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| agnix rulepack 흡수 (VSCode 확장 자체 설치 아님) | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake의 설정/정책 lint 일관성 공백이 현재 실제 문제. **Q2 대체성:** 수동 Audit은 누락·편차 발생. **Q3 비용효과:** 확장을 도입하지 않고 룰 아이디어만 내부 CLI 게이트로 재작성하면 저비용. **Q4 과대포장 필터:** 설치수 28로 인기 신호는 약함 → 그래서 ‘확장 설치’가 아니라 ‘룰셋 흡수’만 채택. **실행계획:** (1) 룰 항목 추출(읽기 전용 조사) (2) 보안/정책 매핑 (3) `misskim-skills` 전용 lint 스크립트로 재작성 (4) 최근 intake 10건 재검증 (5) 오탐/미탐 튜닝 후 정식 편입. |
| SkillHub `Context7 MCP` | ⚠️ 참고만 | **Q1:** 최신 문서 정확도 개선 니즈는 있음. **Q2:** 이미 `context7-docs` 내부 스킬 보유. **Q3:** MCP 운영비 대비 즉시 순증 효과 불명확. **Q4:** 대형 숫자는 품질 보증 아님. **재검토:** 문서 버전 불일치 이슈가 주 3회+ 누적 시. |
| SkillHub `Playwright MCP` | ⚠️ 참고만 | **Q1:** 브라우저 자동화 니즈는 상시 존재. **Q2:** 기존 `browser-cdp-automation` + `playwright-testing`으로 대체 가능. **Q3:** 추가 MCP 운영 복잡도 대비 효과 제한. **Q4:** 인기도보다 현재 스택 중복도가 큼. **재검토:** 기존 브라우저 라인 안정성 저하 시. |
| ClawHub `Answer Overflow` | ⚠️ 참고만 | **Q1:** Discord 기반 문제해결 검색은 유용. **Q2:** 현재 `web_fetch/summarize`로 1차 대응 가능. **Q3:** 도입비는 낮지만 즉시 핵심 병목(keeper/배포) 직접 해결은 아님. **Q4:** 다운로드 신호만으로 즉시 도입 금지. **재검토:** 라이브러리 이슈 재현 실패가 반복될 때. |
| VSCode `copilot-mcp` 계열 확장 직접 도입 | ⚠️ 참고만 | **Q1:** IDE 편의성은 유효. **Q2:** 현재 운영축은 OpenClaw CLI 중심. **Q3:** 팀 표준 분산 비용이 큼. **Q4:** 설치수는 시장성 신호일 뿐 우리 ROI 증거는 아님. **재검토:** VSCode 협업 비중이 50% 이상으로 상승할 때. |

**❌ 불필요 판정: 4건**  
(예: MoltHub 연계 확장/도구, New Relic 전제 스킬, ESP32 전용 MCP, 캘린더 중복군)

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`**

## 산출물
- `intake-log/2026-02-23-04h-trend-raw.json`
- `intake-log/2026-02-23-04h-trend-sweep.md`
