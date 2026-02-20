# 2026-02-21 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **MiniPC browser.proxy:** relay 탭 미연결로 브라우저 세션 부착 실패 → `web_fetch + r.jina.ai + direct API/CLI`로 대체.
- **web_search:** Brave API quota/rate-limit 429 지속.
- **SkillsMP:** `239,658` skills, timeline 평균 `1,762.2`, 피크 `19,898 @ Feb 4, 2026`, `security` 검색 결과 `8,590`.
- **MCP Market:** web_fetch 경로는 Vercel 429 차단, direct sitemap 수집으로 `21,091 server URLs / 43,782 skill URLs` 확인.
- **SkillHub:** `21.6K Skills / 4.9M Stars`, Trending Top5 `gifgrep / feishu-drive / model-usage / wacli / slack`.
- **ClawHub:** newest 샘플 다수 저신뢰(`installsCurrent=0` 다수), trending 상위는 기존 대형 스킬군 중심.
- **VSCode Agent Skills:** Marketplace API 30개 수집, `copilot-mcp 81,476 installs (4.25/8)`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `prodlint` (production-readiness scan 패턴) | ✅ 도입 | **Q1 필요성:** AI 생성 코드/스크립트의 배포 전 보안·완성도 점검이 아직 수동 병목. **Q2 대체성:** `verify-before-done`/TDD는 테스트 절차 중심이고, secret·취약점·hallucinated import 전용 게이트가 약함. **Q3 비용효과:** 외부 서버를 설치하지 않고 규칙 패턴만 내부 스킬로 재작성 가능(중간비용/높은 리스크 절감). **Q4 과대포장 필터:** 인기지표가 아니라 `치명 이슈 검출률`로 검증 가능. |
| MCP Market `shellcheck` | ⚠️ 참고만 | 필요성은 높지만 MCP 도입 없이 shellcheck CLI 직접 게이트로 대체 가능. **재검토:** shell 스크립트 결함 재발률이 주간 기준 임계치 초과 시. |
| ClawHub `clawd-zero-trust` | ⚠️ 참고만 | 보안 방향은 맞지만 `healthcheck` 축과 중복 + `installsCurrent=0` 신뢰 약함. **재검토:** Zero Trust 요구가 명시되고 기존 healthcheck 결과가 미달일 때. |
| SkillHub Trending Top5 (`gifgrep/feishu-drive/model-usage/wacli/slack`) | ⚠️ 참고만 | 대부분 기존 보유 스킬과 기능 중복. **재검토:** 현재 스택에서 동일 기능 실패율이 상승할 때. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | 설치지표는 강하지만 VSCode 종속성이 큼. **재검토:** VSCode 워크플로 비중 50% 이상 전환 시. |
| SkillsMP `security` 클러스터(8,590) | ⚠️ 참고만 | 규모는 크지만 파생/중복 항목이 많아 즉시 흡수 품질 낮음. **재검토:** 내부 보안 게이트 커버리지 목표 미달 시. |

**❌ 불필요 판정: 39건**

## ✅ 도입 실행 계획 (상세)
1. **Research:** `prodlint` 계열이 다루는 production-readiness 체크리스트(하드코딩 secret, 위험 패턴, 의존성/임포트 무결성) 추출.
2. **Audit:** 오탐 억제를 위한 룰 등급(critical/high/warn)과 예외 정책 정의, 로그 마스킹 기준 확정.
3. **Rewrite:** 외부 코드 무복사 원칙으로 `misskim-skills/skills/production-readiness-gate/` 내부 스킬 재작성.
4. **Validation:** 최근 스크립트/툴 10개 대상 dry-run 점검 → 치명 검출률/오탐률 기록.
5. **Adopt Gate:** 기준 충족 시 intake/배포 전 공통 게이트로 편입.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-08h-trend-raw.json`
- `intake-log/2026-02-21-08h-trend-sweep.md`
