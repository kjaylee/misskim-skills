# 2026-02-24 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 경로:** `web_fetch` 기반 수집(이번 회차 `web_search` 미사용).
- **SkillsMP:** `269,875` 신호 복구(`r.jina.ai` 경유), 직접 루트는 Cloudflare 차단 지속.
- **MCP Market:** 원본 `mcpmarket.com` 429(Vercel checkpoint), 미러 `market-mcp.com`은 `6,409` 노출 유지.
- **SkillHub:** `21,159 skills found` 유지.
- **ClawHub:** 홈 기준 popular/highlighted 군 유지(`gog 33.7k`, `self-improving-agent 31.8k`, `tavily-search 27.9k`).
- **VSCode Agent Skills:** `agent-skills 1,832`, `copilot-mcp 81,720`, `agent-skill-ninja 570`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillsMP 직접 흡수 | ⚠️ 참고만 | **Q1** 카탈로그 탐색엔 유효하나 실제 품질 검증 신호는 약함. **Q2** ClawHub/SkillHub/VSCode API로 1차 대체 가능. **Q3** 우회 수집 유지비 대비 즉시 효과 제한. **Q4** 플랫폼 자기주장 수치(270k++)의 과장 가능성 상존. |
| MCP Market 상위군 즉시 도입 | ⚠️ 참고만 | **Q1** 일부 문제를 풀 수 있으나 이번 회차 신규 병목 직접 타격 없음. **Q2** 기존 `coding-agent`/`browser-cdp-automation`으로 대체 가능. **Q3** MCP 운영·권한 비용 대비 불확실. **Q4** 429/차단으로 신뢰도 검증 불완전. |
| SkillHub 상위군(`file-search`,`systematic-debugging`) | ⚠️ 참고만 | **Q1** 유용하지만 이미 내부 흡수/유사 스킬 보유. **Q2** 기존 스택으로 대체 가능. **Q3** 신규 도입보다 내부 고도화가 저비용. **Q4** 신호 수치 반복(예: 73.5k 다중 노출)로 과대해석 위험. |
| ClawHub popular 신규 도입 | ⚠️ 참고만 | **Q1** 가치는 있으나 직전 회차 대비 의미 있는 신규 후보 부재. **Q2** 현재 운영 스택으로 대체 가능 범위 큼. **Q3** 추가 도입비 대비 순증 효과 작음. **Q4** 다운로드 중심 지표만으로 채택 시 과대평가 위험. |
| VSCode Agent Skills 확장군 | ⚠️ 참고만 | **Q1** IDE 편의성은 인정. **Q2** OpenClaw CLI 중심 운영으로 대체 가능. **Q3** 에디터 종속·온보딩 비용 증가. **Q4** 설치 대비 리뷰 모수 작아 마케팅/관성 노이즈 가능. |

**❌ 불필요 판정: 5건**

## 결론
- 이번 회차 **의미 있는 신규 변화 0건** (신규 ✅ 도입 없음).

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 **Research → Audit → Rewrite → `misskim-skills/`** 고정

## 산출물
- `intake-log/2026-02-24-00h-trend-raw.json`
- `intake-log/2026-02-24-00h-trend-sweep.md`
