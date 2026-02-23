# 2026-02-23 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 경로:** `web_search + web_fetch` 시도.
- **실제 상태:** `web_search`는 Brave 429(quota/rate limit).
- **대체 경로:** `web_fetch + 직접 HTTP(fetch/requests) + clawhub CLI + VSCode Marketplace API`.
- **MiniPC browser.proxy:** 이번 회차 미사용(필수 수집을 API/CLI로 충족).
- **SkillsMP:** 루트 403(Cloudflare challenge), 단 `robots/sitemap`은 접근 가능(684 URL).
- **MCP Market:** 헤드라인 `21,759 servers`, 최신 항목 다수 `0` 카운트.
- **SkillHub:** `21,159 skills found` 노출, 상위 항목 카운트 신뢰도 편차 확인.
- **ClawHub:** `explore/search/inspect` 정상 동작, 후보 빠른 1차 검증 가능.
- **VSCode Agent Skills:** `formulahendry.agent-skills 1,829(리뷰 1)`, `copilot-mcp 81,834(리뷰 8)`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `file-search` 패턴 (`fd/rg` 기반) | ✅ 도입 | **Q1 필요:** 대형 리포 탐색 속도/재현성 병목이 실제로 존재. **Q2 대체:** 현재 보유 스킬에 “파일/콘텐츠 탐색 전용 표준”이 없음. **Q3 비용효과:** 문서형 스킬 재작성이라 설치비 거의 0, 즉시 생산성 이득 가능. **Q4 과대포장:** 랭킹이 아니라 `inspect`로 SKILL.md 구조/의존성 확인 후 채택. **실행계획:** (1) upstream 조사 → (2) 안전 감사(명령 allowlist, 경로 스코프) → (3) `misskim-skills/skills/file-search-pro/`로 Rewrite(맥 fallback: `rg→grep`) → (4) 1주 파일탐색 작업에 파일럿 적용. |
| MCP Market 상위군 (`Superpowers`, `TrendRadar`, `Context7`) | ⚠️ 참고만 | **Q1:** 유용해 보이나 당장 미해결 핵심 병목 직접 타격은 약함. **Q2:** `coding-agent`/기존 OpenClaw 스택으로 기능 대체 가능. **Q3:** 신규 MCP 운영·권한·감사 비용 대비 ROI 불명확. **Q4:** 상위 점수와 최신 0카운트 항목 공존 → 지표 신뢰도 편차 큼. **재검토:** 기존 자동화 라인 실패율이 2주 연속 상승 시. |
| VSCode Agent Skills 확장군 (`agent-skills`, `copilot-mcp`, `agent-skill-ninja`) | ⚠️ 참고만 | **Q1:** IDE 내 편의는 인정. **Q2:** 현재 운영 중심은 OpenClaw CLI이므로 직접 필요성 낮음. **Q3:** 에디터 종속성·온보딩 비용 증가. **Q4:** installs 대비 리뷰 모수가 작아 품질 판단 근거 부족. **재검토:** VSCode 협업 비중 50% 이상으로 증가 시. |
| SkillsMP 플랫폼 직접 흡수 | ⚠️ 참고만 | **Q1:** 큰 카탈로그 주장은 있으나 실데이터 접근이 막혀 문제해결력을 검증 못함. **Q2:** 현재는 ClawHub/SkillHub/VSCode API로 1차 탐색 대체 가능. **Q3:** 우회 수집/추가 도구 도입 비용 대비 불확실성 큼. **Q4:** 외부 글의 대규모 수치(예: 66k+)는 교차검증 실패. **재검토:** 공식 API/직접 페이지 접근이 안정적으로 열릴 때. |
| ClawHub `openclaw-token-optimizer` | ⚠️ 참고만 | **Q1:** 비용절감 문제는 실제 유효. **Q2:** 현행 heartbeat/model-routing 운영과 일부 중복. **Q3:** 주장(50~80% 절감) 검증 비용 필요. **Q4:** 마케팅 문구 비중이 높아 블라인드 도입 금지. **재검토:** 토큰 비용 초과 경보가 1주 연속 발생할 때 A/B 테스트. |

**❌ 불필요 판정: 12건**

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬 정책 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)

## 산출물
- `intake-log/2026-02-23-20h-trend-raw.json`
- `intake-log/2026-02-23-20h-trend-sweep.md`
