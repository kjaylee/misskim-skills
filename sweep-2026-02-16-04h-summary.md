# 2026-02-16 04:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

## Scope
- Sources checked: `skillsmp.com`, `mcpmarket.com`, `skillhub.club`, `clawhub.ai`, VSCode Marketplace (`formulahendry.agent-skills`).
- Security guardrail: **Molt Road / molt.host 미접속 + ABSOLUTE BLOCK 유지**.

## Raw Signal Snapshot
- **SkillsMP**: 214,232 skills.
- **MCP Market**: 21,042 servers (updated ~1h ago), 최신 섹션에 `OpenAPI`, `Chromium`, `Goop Shield` 등 신규 노출.
- **SkillHub**: 21.3K skills, 1.4M stars, Git History + Hot Rankings 기능 강조.
- **ClawHub**: `Skills → Sort: Newest` 상단이 0-star/저다운로드 신생 스킬 다수.
- **VSCode Agent Skills extension**: 1,692 installs, last updated 2025-12-26.

## Critical Filter Table
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Server (MCP Market 최신) | ✅ 도입 | **필요 문제**: 신규 외부 API 연동 때 스킬 제작/검증 리드타임이 길다. **기존 대체 한계**: 도메인별 스킬은 있으나 범용 REST→MCP 브리지 부재. **비용 대비 효과**: 중간 수준 도입 비용으로 API 실험속도 개선 예상. **과대포장 필터**: 지표(0 사용)는 약하지만 기능 자체가 현재 병목과 직접 연결. |
| Goop Shield (MCP Market 최신) | ✅ 도입 | **필요 문제**: 외부 스킬 intake 시 런타임 방어 계층 부족. **기존 대체 한계**: 현재는 사전 감사 중심이라 실행 중 프롬프트/출력 방어가 약함. **비용 대비 효과**: 보안 PoC 비용은 있으나 공급망 리스크 감소 가치 큼. **과대포장 필터**: 마케팅 문구 가능성 있어도 제한적 파일럿으로 검증 가능. |
| Android Agent (ClawHub Newest) | ⚠️ 참고만 | 모바일 QA 자동화 잠재력은 있으나, 현재 MiniPC/기존 테스트 루프로 1차 커버 가능. **재검토 조건:** 실기기 Android 회귀테스트가 주 3회 이상 반복되거나, 터치 기반 자동화 병목이 발생할 때. |
| OpenClaw Commerce Shopify (ClawHub Newest) | ⚠️ 참고만 | 결제/스토어 연동 맥락은 맞지만 현재 우선순위는 Stripe 중심 직접 결제 퍼널. **재검토 조건:** Shopify 스토어 실제 운영 시작 + 상품/주문 자동화 필요가 명확해질 때. |
| VSCode “Agent Skills” Extension (`formulahendry.agent-skills`) | ⚠️ 참고만 | 설치/검색 UX는 좋지만 현재 운영은 OpenClaw 중심이며 마지막 업데이트도 2025-12 기준. **재검토 조건:** VSCode 기반 팀 협업 전환 또는 신규 온보딩 표준화 필요 시. |
| SkillHub Git History + Hot Rankings | ⚠️ 참고만 | 신호 품질은 좋아졌지만 랭킹 자체는 품질 보증 아님. **재검토 조건:** 특정 카테고리(마케팅/QA/배포)에서 2주 연속 상위 + 실제 레포 활동성 확인 시. |

**❌ 불필요 판정: 11건**
- 공통 사유: 기능 중복(기보유 스킬/툴로 대체 가능), 저신뢰 지표(0-star/저다운로드), 마케팅성 설명 대비 실사용 근거 부족.

## ✅ Adoption Plan (Research → Audit → Rewrite)
1. **OpenAPI MCP Server 파일럿**
   - Research: 공식 레포/라이선스/권한 요구사항 확인.
   - Audit: allowlist 기반 호출 제한, 인증정보 마스킹, 로깅 정책 검증.
   - Rewrite: `misskim-skills/skills/openapi-bridge/`로 최소권한 래퍼 작성.
   - Exit Criteria: 샘플 API 3종 호출 성공 + 민감정보 노출 0건.

2. **Goop Shield 보안 파일럿**
   - Research: 방어 규칙/오탐 처리/오버헤드 확인.
   - Audit: 프롬프트 인젝션·데이터 유출 시나리오 테스트셋으로 차단율 측정.
   - Rewrite: `misskim-skills/skills/runtime-guard/` 형태로 로컬 정책 결합.
   - Exit Criteria: 고위험 케이스 차단 목표 달성 + 정상 플로우 오탐 허용범위 이내.

## Notes
- 외부 항목은 모두 **Research → Audit → Rewrite → `misskim-skills/`** 원칙 유지.
- **No blind install** 계속 유지.
