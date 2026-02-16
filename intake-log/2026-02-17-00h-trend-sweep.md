# 2026-02-17 00:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot (Sources)
- **SkillsMP:** 메인/카테고리/docs 모두 Cloudflare 403. `sitemap.xml`만 접근 가능 (**684 URLs**, EN 기준 **63 categories**).
- **MCP Market (`mcpmarket.com`):** 전 경로 403 (`x-vercel-mitigated: deny`)로 latest server 직접 수집 실패.
- **SkillHub.club:** 접근 가능. 메타/헤더 기준 **21.3K Skills / 2.4M Stars**. `resciencelab-solopreneur-pack`에서 포함 스킬 9개 확인(`requesthunt`, `seo-geo`, `banner-creator` 등).
- **ClawHub:** `clawhub.com → clawhub.ai` 리다이렉트 후 TLS reset. CLI `clawhub search openapi --limit 5`도 `fetch failed`.
- **VSCode Agent Skills ecosystem:** Marketplace API `agent skills` 검색 **1,204 results**.
  - `AutomataLabs.copilot-mcp`: **80,580 installs**, updated `2026-02-16T05:31:22Z`
  - `formulahendry.agent-skills`: **1,705 installs**, updated `2025-12-26T02:13:18Z`
  - `gaoyuan.skills-vscode`: **582 installs**, updated `2026-02-12T09:04:05Z`

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillHub `requesthunt` 패턴 (Reddit/X/GitHub 수요 신호 수집) | ✅ 도입 | **필요성:** 현재 “무엇을 만들면 돈이 되는가” 판단이 수작업 리서치 의존이라 병목. **기존 대체 한계:** `game-marketing`/`monetization-playbook`은 전략 가이드 중심이고, 채널별 요청 신호 자동 수집·점수화가 없음. **비용/효과:** 구현비용 중간(수집기+스코어링) 대비 아이템 선정 속도 개선 효과 큼. **과대포장 필터:** 설치/별점 대신 데이터 출처(커뮤니티 원문) 검증 가능한 구조라 마케팅 과장 리스크 낮음. |
| SkillHub `seo-geo` | ⚠️ 참고만 | **필요성:** GEO/SEO는 중요. **기존 대체 한계:** 하지만 내부 `seo-optimizer`가 핵심 기능을 이미 커버. **비용/효과:** 지금 추가 도입은 중복 비용이 더 큼. **과대포장 필터:** “AI 검색 최적화” 문구만으로 신규 가치 확증 불가. **재검토:** AI 검색 유입 하락이 2주 이상 지속될 때. |
| VSCode `Copilot MCP + Agent Skills Manager` (AutomataLabs) | ⚠️ 참고만 | **필요성:** 설치수/업데이트는 강한 신호. **기존 대체 한계:** 운영 중심이 OpenClaw라 VSCode 종속 이득 제한. **비용/효과:** 도입·교육·운영비 대비 즉시 생산성 불확실. **과대포장 필터:** 대형 설치수는 품질/적합성 보증이 아님. **재검토:** VSCode 기반 팀 온보딩을 공식화할 때. |
| VSCode `Agent Skills` (formulahendry) | ⚠️ 참고만 | **필요성:** 멀티 소스 설치 UX는 유용. **기존 대체 한계:** 내부 스킬 저장소/오케스트레이션으로 대체 가능. **비용/효과:** 최근 업데이트 정체로 유지 리스크 존재. **과대포장 필터:** 별점/설치수만으로 운영 적합성 판단 불가. **재검토:** IDE 내 스킬 배포 채널을 확대할 때. |
| SkillsMP 피드 접근성 (403) | ⚠️ 참고만 | **필요성:** 대형 디렉터리라 관측 가치는 높음. **기존 대체 한계:** 실피드 접근 불가로 품질 판정 불가. **비용/효과:** 우회 시도 비용 대비 낮은 신뢰도. **과대포장 필터:** 규모 지표(몇만/몇십만 스킬)만으로 도입 금지. **재검토:** recent/API 정상 접근 복구 시. |
| MCP Market 피드 접근성 (403 deny) | ⚠️ 참고만 | **필요성:** MCP 신규 서버 탐지 채널로 중요. **기존 대체 한계:** 원천 차단으로 신규 데이터 부재. **비용/효과:** 차단 상태에서 무리한 수집 비효율. **과대포장 필터:** 과거 캐시 재인용만으로 도입 판단 금지. **재검토:** 차단 해제 후 latest 서버 재평가. |
| ClawHub 피드 접근성 (connection reset) | ⚠️ 참고만 | **필요성:** 생태계 동향 채널 가치 존재. **기존 대체 한계:** 접속 실패로 신규 검증 불가. **비용/효과:** 가용성 복구 전 도입 검토 효율 낮음. **과대포장 필터:** 노출/홍보 카피 기반 판단 금지. **재검토:** 연결 복구 후에도 Research→Audit→Rewrite 경로에서만 검토. |

**❌ 불필요 판정: 16건**
(저설치 VSCode 래퍼/기능 중복 스킬은 개별 나열 생략)

## ✅ Execution Plan (도입 항목만)
1. **Research (즉시)**
   - `requesthunt` 패턴을 내부 요구에 맞게 분해: 채널 수집기(Reddit/X/GitHub) → 문제군 클러스터링 → 수요 스코어링.
2. **Audit (즉시)**
   - 외부 API 키/약관/레이트리밋/PII 포함 가능성 점검.
   - 스크래핑 금지 채널은 API/공식 엔드포인트만 사용.
3. **Rewrite (다음 실행 창)**
   - 외부 스킬 직접 설치 없이 `misskim-skills/skills/demand-signal-miner/` 내부형 스킬로 재작성.
4. **Exit Criteria**
   - 24시간 내 3개 후보(게임/툴) 우선순위 리포트 자동 생성.
   - 각 후보에 근거 링크(원문) + 수요 점수 + 예상 제작비/수익 가설 포함.

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/** (No blind installs)
