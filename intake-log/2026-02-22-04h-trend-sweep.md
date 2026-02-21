# 2026-02-22 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** `web_search`는 Brave quota/rate limit `429`.
- **MiniPC browser.proxy:** openclaw 프로필 시작 실패, chrome relay 탭 미연결.
- **대체 경로:** MiniPC `system.run` + Playwright(headless), `r.jina.ai`, direct API/CLI.
- **소스 스냅샷:**
  - **SkillsMP:** `261,145 skills`, browse cap `5,000`, open `SKILL.md` 표준.
  - **MCP Market:** `21,654 servers` (업데이트 `3 hours ago`), Official/Featured 상위 시그널 추출.
  - **SkillHub:** `541 skills / 55 GitHub sources / 111k downloads` (홈 기준).
  - **ClawHub:** `security-audit-toolkit`(`downloads 1,765`, `installsCurrent 6`, `stars 4`) 등 샘플 검증.
  - **VSCode Agent Skills:** 공식 문서/블로그에서 `chatSkills` GA 확인 + 확장 설치 신호(`copilot-mcp 81.5K`, `agent-skills 1.8K`, `agnix 26`).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `security-audit-toolkit` 패턴 흡수 (내부 보안 인테이크 게이트 v2) | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake의 공급망/시크릿/권한 검수 병목이 현재도 실문제. **Q2 대체성:** 기존 보안 규칙은 분산되어 재현 가능한 점수화가 부족. **Q3 비용효과:** 외부 설치 없이 패턴 재작성으로 저비용 적용 가능. **Q4 과대포장 필터:** 단순 홍보가 아니라 installsCurrent(6), stars(4), 최근 업데이트로 최소 실사용 신호 확인. |
| VS Code `chatSkills` 패키징 경로(공식 표준) 병행 지원 | ✅ 도입 | **Q1 필요성:** OpenClaw 밖 협업 환경에서 스킬 재사용 진입장벽 존재. **Q2 대체성:** clawhub만으로 VS Code/Copilot 네이티브 배포 경로를 직접 대체하지 못함. **Q3 비용효과:** 핵심 스킬 3개만 시범 포장해도 분배 비용 절감 효과 기대. **Q4 과대포장 필터:** 공식 문서/릴리스(1.109 GA) 근거라 마케팅성 주장보다 신뢰도 높음. |
| SkillsMP 대규모 카탈로그 직접 흡수 | ⚠️ 참고만 | 대규모 소스 가치는 있으나 Cloudflare/노이즈로 정밀 필터 품질이 낮음. **재검토:** 카테고리 API/신뢰도 필드가 안정 공개될 때. |
| MCP Market 상위 서버(Official/Featured) 즉시 도입 | ⚠️ 참고만 | 상위 지표는 강하지만 우리 기존 스택(`browser-cdp-automation`, `web_fetch`, `godot`)으로 1차 대체 가능. **재검토:** 동일 병목이 2주 연속 반복될 때. |
| SkillHub Marketplace/Desktop 즉시 도입 | ⚠️ 참고만 | 멀티툴 GUI 가치가 있으나 현재는 CLI 중심 운영과 정합 낮음. **재검토:** 비-CLI 협업 온보딩 수요가 명확해질 때. |
| VSCode 서드파티 확장(`agent-skills`, `agnix`) 직접 도입 | ⚠️ 참고만 | 설치수는 신호이나 운영축(OpenClaw CLI)과 불일치. **재검토:** VSCode 작업 비중이 50% 이상일 때. |

**❌ 불필요 판정: 16건**

## ✅ 도입 실행 계획 (상세)

### 1) 보안 인테이크 게이트 v2 (security-audit-toolkit 패턴 흡수)
1. **Research:** `clawhub inspect security-audit-toolkit --files --file`로 규칙 범주 추출.
2. **Audit:** 실행형 코드/외부 호출 제거, 정책 위반 패턴(시크릿/권한과다/원격실행)만 보존.
3. **Rewrite:** `misskim-skills/` 내부 스킬로 재작성(Research → Audit → Rewrite).
4. **Validate:** 악성/정상 fixture 20개 기준 탐지율·오탐률 측정 후 intake 게이트에 연결.

### 2) VS Code chatSkills 병행 배포 PoC
1. **Research:** 공식 `chatSkills` 규격(디렉토리명=SKILL name, package.json contribution) 체크리스트 고정.
2. **Audit:** 외부 의존 없는 핵심 스킬 3개 선별(보안/검색/QA 계열).
3. **Rewrite:** 미스김 스킬을 VS Code 포맷으로 포장(내부 repo에 별도 path).
4. **Validate:** VS Code 1.109에서 slash command 노출/자동 로드 동작 검증.

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-22-04h-trend-raw.json`
- `intake-log/2026-02-22-04h-trend-sweep.md`
