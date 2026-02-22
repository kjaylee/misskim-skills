# 2026-02-22 12:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch`.
- **실제 상태:** `web_search`는 Brave quota/rate limit `429`로 실패.
- **대체 경로:** `web_fetch + r.jina.ai`로 소스별 텍스트 수집.
- **SkillsMP:** `261,145 skills`, browse cap `5,000`.
- **MCP Market:** `mcpmarket.com`은 429 checkpoint, `market-mcp.com`에서 `6,409` 서버/노출 `100` 확인.
- **SkillHub:** `21.6K skills / 5.1M stars`, Trending 상단 `discord / nano-banana-pro / gifgrep / feishu-drive / model-usage`.
- **ClawHub:** newest + popular + API 교차 확인(`planning-with-files`, `browser-use`, `swarm`, `clawstats`, `website-monitor`).
- **VSCode Agent Skills:** 공식 docs의 `chatSkills`/slash-command 경로와 확장군(`copilot-mcp`, `agent-skills`, `agnix`) 기능 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub 신규 운영/모니터링군 (`clawstats`, `website-monitor`) | ⚠️ 참고만 | **Q1 필요성:** 운영 니즈는 있으나 현재 핵심 병목(일일 게임/서비스 산출)과 직접 연결 약함. **Q2 대체성:** heartbeat 루틴 + healthcheck로 1차 대응 가능. **Q3 비용효과:** 유지 포인트 증가 대비 즉시 ROI 제한적. **Q4 과대포장:** newest 노출 대비 실사용 신호가 약함(`installsCurrent=0` 중심). **재검토:** 장애가 1주 내 2회 이상 재발하고 원인 포착이 지연될 때. |
| ClawHub 계획/비용 최적화군 (`planning-with-files`, `swarm`) | ⚠️ 참고만 | **Q1 필요성:** 니즈는 있으나 현재 운영 정책(메인 오케스트레이션 + 서브에이전트)과 충돌 가능. **Q2 대체성:** subagent+cron+checkpoint 체계로 유사 기능 수행 중. **Q3 비용효과:** 정책 충돌 검증 비용이 큼. **Q4 과대포장:** 마케팅 문구 대비 우리 환경 실증 데이터 부족. **재검토:** 서브에이전트 비용/실패율 KPI가 2주 연속 악화될 때. |
| MCP Market 상위군 (`Archon`, `Trigger.dev`, `Chrome DevTools`) | ⚠️ 참고만 | **Q1 필요성:** 고신호이나 즉시 해결 못 하는 구체 병목은 아님. **Q2 대체성:** `browser-cdp-automation`, `coding-agent`, 기존 DevOps 루틴으로 대체 가능. **Q3 비용효과:** MCP 인증/보안/운영 복잡도 증가 대비 즉시 ROI 불명확. **Q4 과대포장:** 순위 지표 강하지만 KPI 직접 개선 인과 부족. **재검토:** 동일 실패가 2주 연속 반복되고 기존 스택으로 복구 불가할 때. |
| SkillHub Trending 급등군 | ⚠️ 참고만 | **Q1 필요성:** 일부 유효하나 상위 다수가 기존 보유 스킬과 중복. **Q2 대체성:** OpenClaw 기본/내부 스킬로 상당수 커버. **Q3 비용효과:** 대량 큐레이션 검수 비용 큼. **Q4 과대포장:** 단기 star 급등은 품질 보장 지표가 아님. **재검토:** 상위 유지가 3회차 이상 지속되고 실제 사용 사례가 쌓일 때. |
| VSCode Agent Skills 확장군 (`copilot-mcp`, `agent-skills`, `agnix`) | ⚠️ 참고만 | **Q1 필요성:** IDE 협업 환경에는 유효하나 현재 운영축과 직접 정합 낮음. **Q2 대체성:** OpenClaw CLI + 내부 rewrite 프로세스로 핵심 기능 대체 가능. **Q3 비용효과:** IDE 종속 전환 비용 큼. **Q4 과대포장:** 생태계 성장 자체가 우리 생산성 향상을 보장하지 않음. **재검토:** VSCode 협업 비중 50%+ 시. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | **Q1 필요성:** 검색 소스로 유효하나 즉시 도입 선별 정확도 낮음. **Q2 대체성:** skillhub/clawhub/기보유 스킬로 1차 커버 가능. **Q3 비용효과:** 대량 후보 감사 비용 큼. **Q4 과대포장:** 규모(261k)는 강하지만 품질 선별 비용이 과대. **재검토:** 품질 점수/신뢰도 API 안정화 시. |

**✅ 도입: 없음 (이번 회차는 즉시 도입 근거 부족)**

**❌ 불필요 판정: 19건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-12h-trend-raw.json`
- `intake-log/2026-02-22-12h-trend-sweep.md`
