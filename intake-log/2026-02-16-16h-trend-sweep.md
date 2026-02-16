# 2026-02-16 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot (Sources)
- **SkillsMP:** 메인/검색/API 모두 Cloudflare 403. 다만 `sitemap.xml`은 접근 가능(684 URLs, EN 카테고리 63개).
- **MCP Market:** `Latest MCP Servers`에서 신규 6개 노출: `PubCrawl`, `Rulecatch`, `App Store Rejections`, `Power Automate`, `Bareos`, `OpenAPI`.
- **SkillHub.club:** 메타 기준 `7,000+` skills, `2.0M stars`; `AI Video Ad Generator` 스택 노출 유지.
- **ClawHub:** `clawhub.com`/`clawhub.ai` 모두 connection reset (CLI `clawhub explore`도 fetch 실패).
- **VSCode Agent Skills ecosystem:** Marketplace API 쿼리 `agent skills` 총 **1,201** 결과. `AutomataLabs.copilot-mcp` 80,495 installs, 2026-02-16 업데이트 확인.

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| MCP Market `OpenAPI` (`/server/openapi-15`) | ✅ 도입 | **필요성:** REST API→도구화 병목이 현재 실존. **기존 대체 한계:** 도메인별 수작업 스킬은 확장속도 제한. **비용/효과:** Audit+Rewrite 중간비용 대비 온보딩 시간 단축 효과 큼. **과대포장 필터:** 현재 노출 카운트 0이라 원본 신뢰는 낮아, 패턴만 흡수 후 내부 재작성. |
| SkillHub `AI Video Ad Generator` (`/skill-stacks/resciencelab-solopreneur-pack`) | ✅ 도입 | **필요성:** 게임/툴 유입용 짧은 광고 영상 자동화 공백 존재. **기존 대체 한계:** 카피/이미지/배포가 분절, 영상 end-to-end 파이프라인 부재. **비용/효과:** 구현비용 중간~상, 재사용 마케팅 산출물 ROI 높음. **과대포장 필터:** 구성요소(스크립트/TTS/BGM/렌더)가 명시되어 검증 단위 분해 가능. |
| MCP Market `Rulecatch` (`/server/rulecatch`) | ⚠️ 참고만 | 코드 규칙/비용 모니터링은 유의미하지만 현행 SDD+TDD+자체 검증으로 1차 커버 가능. **재검토 조건:** 세션별 규칙 위반/비용 추적이 실제 병목으로 수치화될 때. |
| MCP Market `App Store Rejections` (`/server/app-store-rejections`) | ⚠️ 참고만 | App Store 심사 대응 지식베이스는 유용하나, 현재 막힌 핵심은 계정/배포 절차 쪽. **재검토 조건:** 실제 리젝 사유 분석 자동화가 필요해지는 시점(첫 리젝 반복 발생). |
| VSCode `Copilot MCP + Agent Skills Manager` (80,495 installs) | ⚠️ 참고만 | 대규모 설치·당일 업데이트는 강한 신호지만 운영 중심은 OpenClaw 오케스트레이션. **재검토 조건:** VSCode 중심 팀 온보딩/배포 표준화가 시작될 때. |
| SkillsMP 피드 접근성 (403) | ⚠️ 참고만 | 데이터 수집 자체가 불안정해 품질 판정 신뢰가 낮음. **재검토 조건:** Cloudflare 우회가 아닌 정상 접근 복구 후 `recent` 피드 재평가. |
| ClawHub 피드 접근성 (connection reset) | ⚠️ 참고만 | 최신 피드 신뢰수집 불가 상태. **재검토 조건:** 레지스트리 정상화 확인 후에도 반드시 Research→Audit→Rewrite 경로에서만 검토. |

**❌ 불필요 판정: 12건**
(저설치 VSCode wrapper/기능중복/도메인 불일치 항목은 개별 나열 생략)

## ✅ Execution Plan
1. **OpenAPI 패턴 내재화 (today)**
   - Research: OpenAPI MCP 기능 경계(인증/스키마/에러처리) 분해
   - Audit: 파괴적 메서드(write/delete) 기본 차단 + allowlist 설계
   - Rewrite: `misskim-skills/skills/openapi-tool-scaffold/` 강화(내부 표준 템플릿)
   - Exit: 내부 API 1개 read-only + safe-write 시나리오 통과

2. **Video Ad Pipeline 내재화 (today→next run)**
   - Research: 스크립트→보이스→BGM→렌더→후처리 모듈 입력/출력 규격화
   - Audit: 라이선스/유료 API 의존/외부 업로드 리스크 점검
   - Rewrite: `misskim-skills/skills/game-video-ad-pipeline/` 업데이트 (외부 스택 직접 설치 금지)
   - Exit: 15~30초 광고 영상 1개 자동 생성 + 민감정보 노출 0건

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/** (No blind installs)
