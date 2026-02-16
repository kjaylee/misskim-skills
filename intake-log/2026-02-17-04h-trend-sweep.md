# 2026-02-17 04:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot (Sources)
- **SkillsMP:** 메인/검색/카테고리/스킬 페이지 모두 403(Cloudflare). `sitemap.xml`만 접근 가능 (**684 URLs**, 최근 `lastmod` 고정: `2026-02-06T13:28:47Z`).
- **MCP Market (`mcpmarket.com`):** 웹페치 경로는 Vercel checkpoint가 뜨지만, sitemap 직접 수집은 가능.
  - 파싱 결과: **70,172 URLs** (`server` 21,042 / `skills` 48,729)
  - 최신 서버 상위: `pubcrawl`, `rulecatch`, `app-store-rejections`, `power-automate`, `openapi-15` (lastmod 2026-02-15)
- **SkillHub.club:** 정상 접근. `sitemap.xml` 기준 **1,981 URLs**, 최근 스킬 업데이트 다수(2026-02-16).
  - 신규/상위 변경: `webapp-testing`, `cloudflare-mcp-server`, `mcp-cli-scripts`, `requesting-code-review`, `web-design-guidelines` 등
- **ClawHub (`clawhub.com/.ai`):** TLS connection reset. `clawhub search openapi --limit 5`도 `fetch failed`.
- **VSCode Agent Skills extension ecosystem (Marketplace API):**
  - `AutomataLabs.copilot-mcp`: **80,621 installs**, updated `2026-02-16`
  - `formulahendry.agent-skills`: **1,708 installs**, updated `2025-12-26`
  - `yamapan.agent-skill-ninja`: **517 installs**, updated `2026-02-08`

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillHub `requesthunt` 패턴 (Reddit/X/GitHub 수요 신호 수집) | ✅ 도입 | **필요성:** 현재 아이템 선정이 체감/수작업 리서치 의존이라 배포 병목(무엇을 만들지 결정 지연)이 큼. **기존 대체 한계:** 내부 `game-marketing`/플레이북은 전략 문서 중심이고, 실시간 수요 신호를 정량화하는 데이터 파이프가 없음. **비용/효과:** 중간 난이도 수집기+스코어링으로 높은 ROI. **과대포장 필터:** 별점/다운로드가 아니라 원문 신호(요청·불만·질문) 기반 검증 가능. |
| SkillHub `webapp-testing` 패턴 (Playwright 기반 기능 검증) | ✅ 도입 | **필요성:** 100+ 웹게임/툴의 기능 회귀를 수동 확인하는 시간이 큼. **기존 대체 한계:** 현재 브라우저 자동화 스킬은 범용 조작 중심이라 “반복 가능한 게임 스모크 테스트 템플릿”이 부족. **비용/효과:** 템플릿화 비용 대비 QA 속도/안정성 개선 효과 큼. **과대포장 필터:** 화려한 설명보다 실패 검출률·재현성으로 성능을 즉시 검증 가능. |
| MCP Market `app-store-rejections` | ⚠️ 참고만 | App Store 심사 대응 DB는 유용하지만, 현재 핵심 병목은 리젝 사유 분석이 아니라 계정/출시 절차. 실제 리젝 반복 발생 시 재검토. |
| MCP Market `openapi-15` | ⚠️ 참고만 | `openapi-tool-scaffold` 내부 스킬이 이미 존재해 즉시 신규 도입 필요성 낮음. REST 연동 처리시간이 다시 병목화되면 재검토. |
| SkillHub `cloudflare-mcp-server` | ⚠️ 참고만 | 원격 MCP 운영 관점 가치는 있으나 현재 배포 우선순위는 GitHub Pages/채널 확장. Cloudflare Worker 기반 운영 전환 시 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치수/업데이트는 강하지만 운영 중심이 OpenClaw라 도입/학습비 대비 즉시효용 낮음. VSCode 협업 표준화 시 재검토. |
| VSCode `Agent Skills` (formulahendry) | ⚠️ 참고만 | 설치 UX는 좋지만 업데이트 정체(2025-12-26) + 기능 중복(내부 스킬 레지스트리). IDE 유통 채널 확장 시 재검토. |
| SkillsMP / ClawHub 피드 접근성 이슈 | ⚠️ 참고만 | 원천 피드 품질 검증이 막혀 있어 “신규 발견” 신뢰도가 낮음. 접근 복구 전에는 대규모 도입 판단 보류. |

**❌ 불필요 판정: 14건**
(도메인 불일치/중복 기능/저신뢰 저설치 항목은 개별 나열 생략)

## ✅ Execution Plan (도입 항목만)
1. **`demand-signal-miner` 내부화 (requesthunt 패턴 흡수)**
   - 경로: `misskim-skills/skills/demand-signal-miner/`
   - 단계: Research → Audit → Rewrite
   - 산출: 채널별 수요 신호 수집(요청/불만/질문) + 점수화 + 아이디어 우선순위 리포트
   - 완료 기준: 24시간 샘플 수집 1회, 상위 3개 아이템 추천(근거 링크 포함)

2. **`webapp-smoke-qa` 내부화 (webapp-testing 패턴 흡수)**
   - 경로: `misskim-skills/skills/webapp-smoke-qa/`
   - 단계: Research → Audit → Rewrite
   - 산출: 게임/툴 공통 스모크 테스트 체크리스트(로딩, 입력, 점수/상태 변화, 에러 콘솔 감시)
   - 완료 기준: 대표 타이틀 5개 자동 스모크 통과/실패 리포트 생성

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/**
- **No blind installs** (직접 설치 금지)
