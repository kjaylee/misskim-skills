# 2026-02-16 00:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

## Scope
- Sources checked: `skillsmp.com`, `mcpmarket.com`, `skillhub.club`, `clawhub.com`, VSCode Marketplace (`formulahendry.agent-skills`).
- Security guardrail: **Molt Road / molt.host 미접속 + ABSOLUTE BLOCK 유지**.

## Raw Signal Snapshot
- **SkillsMP**: 214,232 skills, recent feed 상단 다수가 0~1 star 저신뢰 항목.
- **MCP Market**: 21,042 servers, “최신 MCP 서버” 섹션에 신규 0-count 다수 노출.
- **SkillHub**: 21.3K skills, Hot 랭킹(6시간 주기) 제공.
- **ClawHub**: `Newest` 정렬 상위 대부분 0 star/0 install 근접.
- **VSCode Agent Skills 확장**: 1,691 installs, 마지막 업데이트 2025-12-26.

## Critical Filter Table
| 항목 | 판정 | 근거 |
|------|------|------|
| OpenAPI MCP Server (MCP Market 최신) | ✅ 도입 | **필요 문제**: 새 REST API 연동 시 스킬 제작 리드타임 큼. **기존 대체 한계**: 기존 스킬은 도메인별, 범용 REST→MCP 변환 부재. **비용/효과**: 중간 도입비용 대비 API 실험 속도 개선 기대. **과대포장 필터**: 최신 0-count라 숫자 신뢰도 낮아도, 기능 자체가 직접적 병목 해소. |
| Goop Shield (MCP Market 최신) | ✅ 도입 | **필요 문제**: 외부 스킬 intake 시 런타임 프롬프트/출력 방어 레이어 부족. **기존 대체 한계**: 현재는 사전 감사 중심, 실행 중 동적 방어는 약함. **비용/효과**: 샌드박스 PoC 비용은 있으나 공급망 리스크 감소 기대. **과대포장 필터**: 홍보성 문구 대비 실효 검증 필요해 제한적 파일럿으로만 도입. |
| audit-website (SkillHub Hot #2) | ⚠️ 참고만 | 현재 `web-design-guidelines` + 수동 점검으로 핵심 UX/접근성 커버 가능. SEO/보안 자동 점검 파이프라인을 대량 운영해야 할 때 재검토. |
| VSCode “Agent Skills” Extension (`formulahendry.agent-skills`) | ⚠️ 참고만 | 워크플로우가 OpenClaw 중심이라 즉시효용 낮음. VSCode 기반 협업 전환 또는 팀 온보딩 표준화 필요 시 재검토. |

**❌ 불필요 판정: 12건**
- 공통 사유: 저신뢰 지표(0-star/0-install), 기존 스킬 중복, 마케팅성 포장 대비 실사용 근거 부족.

## ✅ Adoption Plan (Research → Audit → Rewrite)
1. **OpenAPI MCP Server (Pilot)**
   - Research: 공식 repo/라이선스/권한 모델 확인.
   - Audit: 허용 도메인 allowlist, 인증정보 취급, request/response 로깅 정책 검증.
   - Rewrite: `misskim-skills/skills/openapi-bridge/` 로 최소권한 래퍼 스킬 작성.
   - Exit Criteria: 샘플 3개 API(결제/콘텐츠/분석) 호출 성공 + 민감정보 노출 0건.

2. **Goop Shield (Security Pilot)**
   - Research: 탐지 규칙, false-positive 처리 방식, 성능 오버헤드 확인.
   - Audit: 프롬프트 인젝션/데이터 유출 시나리오 20개 테스트셋으로 방어 성능 검증.
   - Rewrite: `misskim-skills/skills/runtime-guard/` 형태로 로컬 정책 결합 래퍼 작성.
   - Exit Criteria: 고위험 케이스 차단율 목표 달성 + 정상 워크플로우 오탐 허용범위 이내.

## Notes
- ClawHub에서 `moltbro/*` 계열 항목 노출 확인됨(예: humanize-ai-text). 정책상 **도입 제외**.
- 모든 외부 항목은 **No blind install** 원칙 유지.
