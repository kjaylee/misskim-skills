# 2026-02-16 12:04 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot
- **SkillsMP:** 214,232 skills. `sort=recent` 상단 다수가 0~1 star/저검증 항목(`run-tests`, `poster`, `premium-ui-design`, `hs` 등).
- **MCP Market:** 21,061 servers. 최신 섹션에 `OpenAPI`, `Rulecatch`, `App Store Rejections`, `Power Automate` 등 신규 노출(다수 0 사용량).
- **SkillHub:** 21.3K skills / 1.4M stars. `Hot Rankings`, `Git History` 활성화. Premium Stack에 `AI Video Ad Generator` 노출.
- **ClawHub:** `clawhub.com`, `clawhub.ai` 모두 **ERR_CONNECTION_RESET** (피드 수집 실패).
- **VSCode Agent Skills ecosystem:**
  - `formulahendry.agent-skills` 1,695 installs, Last updated 2025-12-26.
  - `AutomataLabs.copilot-mcp` 80,475 installs, Last updated 2026-02-11.

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| MCP Market `OpenAPI` (openapi-mcp-bridge) | ✅ 도입 | **필요성:** 내부 API를 MCP 도구로 빠르게 전환하는 병목이 현재 존재. **기존 대체 한계:** 개별 전용 스킬 수작업 방식은 확장 속도 제한. **비용 대비 효과:** 초기 Audit/Rewrite 비용 중간, 이후 API 온보딩 시간 단축 효과 큼. **과대포장 필터:** GitHub 0★로 신뢰 낮아 “원본 도입”은 배제하고 패턴만 흡수. |
| SkillHub `AI Video Ad Generator` Stack | ✅ 도입 | **필요성:** 게임/툴 유입을 위한 짧은 광고 영상 자동화가 아직 미완. **기존 대체 한계:** 현재 이미지·카피·배포가 분절되어 영상 end-to-end 파이프라인 부재. **비용 대비 효과:** 구현비용은 중간~상, 재사용 가능한 마케팅 자동화 ROI 높음. **과대포장 필터:** 설명이 구체적(스크립트/TTS/BGM/렌더/후처리)이라 검증 가능한 단위로 분해 가능. |
| MCP Market `Rulecatch` | ⚠️ 참고만 | 코드 규칙/비용 모니터링 가치는 있으나 현재 SDD+TDD+자체 검증 루프로 1차 커버 가능. **재검토 조건:** 세션 단위 비용/룰 위반 추적이 실제 병목으로 측정될 때. |
| VSCode `Copilot MCP + Agent Skills` (AutomataLabs) | ⚠️ 참고만 | 설치수는 강한 신호(80K+)지만 VSCode 중심 운영 + Cloud MCP 유도 의존성이 현재 워크플로우와 불일치. **재검토 조건:** VSCode 기반 팀 온보딩/배포를 본격화할 때. |
| VSCode `Agent Skills` (formulahendry) | ⚠️ 참고만 | 기능은 유용하나 업데이트 템포가 느림(2025-12-26 이후 정체). **재검토 조건:** 우리 스킬을 VSCode 배포 채널로 확장해야 할 때. |
| SkillsMP `hs` (hardstop) | ⚠️ 참고만 | 안전 게이트 아이디어는 유효하지만 현재 글로벌 안전 정책/감사 규칙과 중복. **재검토 조건:** 명령 실행 안전사고가 실제 발생해 보강 필요성이 생길 때. |
| ClawHub feed availability (`.com`, `.ai`) | ⚠️ 참고만 | 연결 재설정으로 신뢰 가능한 최신 수집 불가. **재검토 조건:** 접속 복구 후에도 반드시 Research→Audit→Rewrite 경로에서만 재평가. |

**❌ 불필요 판정: 15건**
(0~1 사용량 신규 항목, 기능 중복, 마케팅 문구 대비 실증 부족 항목은 개별 나열 생략)

## ✅ Execution Plan
1. **OpenAPI Bridge (today)**
   - Research: `openapi-mcp-bridge` 구조/인증 방식/파괴적 연산 가드 규칙 분해.
   - Audit: 외부 호출/비밀키 처리/요청 화이트리스트 정책 검증.
   - Rewrite: `misskim-skills/skills/openapi-tool-scaffold/` 내부형 스킬로 재작성.
   - Exit: 내부 API 1개를 MCP 도구화해 read-only + safe-write 시나리오 통과.

2. **Game Video Ad Pipeline (today→next run)**
   - Research: 스크립트→보이스→BGM→렌더→후처리 모듈 단위 요구사항 정의.
   - Audit: 유료 API 의존/라이선스/외부 업로드 리스크 점검.
   - Rewrite: `misskim-skills/skills/game-video-ad-pipeline/` 생성 (외부 스택 직접 설치 금지).
   - Exit: 15~30초 영상 1개 자동 생성 + 민감정보 노출 0건.

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/** (No blind installs)
