# 2026-02-22 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch` 시도.
- **실제 상태:** `web_search`는 Brave quota/rate limit `429`.
- **대체 경로:** `web_fetch + r.jina.ai`로 소스별 텍스트 수집.
- **SkillsMP:** `261,145 skills`, browse cap `5,000`, SKILL.md 오픈 표준 유지.
- **MCP Market:** `mcpmarket.com`은 429 checkpoint, `market-mcp.com` 대체 경로에서 `6,409` 서버/노출 `100`개 확인.
- **SkillHub:** `21.6K skills / 5.2M stars`, Trending 상단 `discord / nano-banana-pro / gifgrep / feishu-drive / model-usage`.
- **ClawHub:** API(`api/v1/skills`)는 429. `skills?sort=newest`에서 `approvals-ui`, `summarize-file`, `prospairrow-websites-mcp`, `nano-banana-pdf-skill` 등 신규군 확인.
- **VSCode Agent Skills:** 공식 docs에서 `chatSkills` 기여점+슬래시 명령 경로 확인. 확장 설치 신호 `copilot-mcp 81.5K`, `agent-skills 1.8K`, `agnix 26`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub newest 저신호 군 (`approvals-ui`, `summarize-file`, `prospairrow-websites-mcp`) | ⚠️ 참고만 | **Q1 필요성:** 일부 니즈는 있으나 현재 핵심 병목(일일 게임/서비스 파이프라인)과 직접 연결 약함. **Q2 대체성:** 기존 OpenClaw 툴/내부 스킬로 1차 대체 가능. **Q3 비용효과:** 설치·검증 비용 대비 즉시 ROI 불명확. **Q4 과대포장 필터:** newest 노출 대비 신호(0~1) 약함. **재검토:** pairing/승인 병목이 1주 이상 누적될 때. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | **Q1 필요성:** 고신호이나 지금 당장 못 하는 작업은 아님. **Q2 대체성:** `browser-cdp-automation`, `coding-agent` 등으로 대체 가능. **Q3 비용효과:** MCP 추가 운영 시 인증/보안/유지비 상승. **Q4 과대포장 필터:** 수치 신호는 강하지만 우리 KPI 직접 개선 근거 부족. **재검토:** 동일 실패가 2주 연속 재발할 때. |
| VSCode 확장군 (`copilot-mcp`, `agent-skills`, `agnix`) | ⚠️ 참고만 | **Q1 필요성:** 설정 검증·유통 니즈는 존재. **Q2 대체성:** OpenClaw CLI 중심 운영으로 당장 필수 아님. **Q3 비용효과:** IDE 종속 전환 비용 큼. **Q4 과대포장 필터:** 설치수 대비 운영효과는 환경 의존. **재검토:** VSCode 협업 비중 50%+일 때. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | **Q1 필요성:** 검색 소스로 유효. **Q2 대체성:** skillhub/clawhub/내부 스킬로 1차 커버 가능. **Q3 비용효과:** 대량 후보 검수비가 큼. **Q4 과대포장 필터:** 규모는 크지만 품질 신호 분리 비용이 높음. **재검토:** 신뢰도 점수/API 안정화 시. |

**✅ 도입: 없음 (이번 회차는 즉시 도입 근거 부족)**

**❌ 불필요 판정: 17건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-08h-trend-raw.json`
- `intake-log/2026-02-22-08h-trend-sweep.md`
