# 2026-02-23 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **MiniPC browser.proxy:** `target=node` 상태 점검 완료, relay attach 미연결로 브라우저 실사용 불가.
- **우선 경로:** `web_search + web_fetch` 시도.
- **실제 상태:** `web_search`는 Brave quota/rate-limit `429`로 실패.
- **대체 경로:** `web_fetch + r.jina.ai + VSCode Marketplace API`.
- **SkillsMP:** 전체 `269,875` skills, `Security 6,631`, `Mobile 4,817` 확인.
- **MCP Market:** `mcpmarket.com`은 Vercel checkpoint `429`; 대체 mirror(`market-mcp.com`) 기준 `6,409` 서버 노출.
- **SkillHub:** `311` tools 신호 유지, 상위 MCP/Skill 랭킹 재확인.
- **ClawHub:** downloads 상위 `gog(32.8k)`, `self-improving-agent(30.3k)`, `tavily-search(26.9k)`; newest 군은 installs 신호 매우 낮음.
- **VSCode Agent Skills:** `copilot-mcp(81,737)`, `agent-skills(1,816)`, `agnix(28)`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| agnix rulepack 흡수 (VSCode 확장 설치 아님) | ✅ 도입 | **Q1 필요:** 외부 스킬 intake의 정책 누락/형식 편차가 실제 반복 이슈. **Q2 대체:** 수동 리뷰만으로는 재현성 부족. **Q3 비용효과:** 룰셋만 내부 lint gate로 재작성 시 저비용·고효율. **Q4 과대포장:** 설치수(28)는 약하므로 확장 설치는 배제, 규칙만 흡수. **실행계획:** (1) 룰 항목 추출→(2) 보안정책 매핑→(3) `misskim-skills`용 lint 스크립트화→(4) 최근 intake 재검증 20건→(5) 오탐/미탐 튜닝 후 고정. |
| SkillHub `Apple Docs MCP` 패턴(직접 MCP 설치 아님) | ✅ 도입 | **Q1 필요:** iOS/카메라 앱 작업에서 Apple 공식 문서 탐색 속도/정확도 병목이 실제 발생. **Q2 대체:** 일반 웹검색은 버전·문맥 정확도가 낮음. **Q3 비용효과:** MCP 서버 도입 대신 문서 질의 패턴만 내부 스킬로 재작성하면 유지비 낮음. **Q4 과대포장:** star/download 숫자보다 Apple 플랫폼 정합성을 우선. **실행계획:** (1) API 범위 감사(AVFoundation/StoreKit/SwiftUI)→(2) read-only 질의 템플릿화→(3) `misskim-skills/skills/apple-dev-docs` 초안 작성→(4) 카메라앱 시나리오 5개 검증→(5) 통과 시 편입. |
| MCP Market 상위 `Chrome DevTools`/`Archon` 계열 | ⚠️ 참고만 | **Q1:** 자동화 니즈는 있으나 현재 즉시 미해결 병목은 아님. **Q2:** `browser-cdp-automation`/`coding-agent`로 대체 가능. **Q3:** 신규 MCP 운영비 대비 순증 불명확. **Q4:** 랭킹/점수는 품질 보증 아님. **재검토:** 기존 브라우저·코딩 파이프라인 실패율이 주간 기준 2배 이상 상승 시. |
| VSCode `copilot-mcp` 직접 도입 | ⚠️ 참고만 | **Q1:** IDE 편의성은 유효. **Q2:** 현재 운영축은 OpenClaw CLI 중심. **Q3:** 팀 표준 분산 비용 큼. **Q4:** installs(81k+)는 시장성 신호일 뿐 우리 ROI 근거는 아님. **재검토:** VSCode 협업 비중 50%+ 시. |
| ClawHub `self-improving-agent` | ⚠️ 참고만 | **Q1:** 학습 루프 가치는 있으나 현 병목은 품질게이트 일관성. **Q2:** `openclaw-mem` + 내부 회고 루틴으로 대체 가능. **Q3:** 도입 시 행동예측성 저하 리스크 존재. **Q4:** 다운로드 고신호(30.3k)만으로 채택 금지. **재검토:** 회고 루틴 자동화가 2주 연속 실패 시. |

**❌ 불필요 판정: 7건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`**

## 산출물
- `intake-log/2026-02-23-08h-trend-raw.json`
- `intake-log/2026-02-23-08h-trend-sweep.md`
