# 2026-02-17 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## 수집 소스 스냅샷
- **SkillsMP**: 227,170 skills. recent 정렬 상단이 `ahaodev/heji` Android 분해형 스킬(2/17)로 채워짐.
- **MCP Market**: 21,091 servers, 약 1시간 전 업데이트. latest에 `ShellCheck`, `Dolex`, `Appwrite`, `Mem0` 노출.
- **SkillHub**: 21.3K skills / 5.5M stars 표기, `Trending Today` + `S-rank` + 유료 Stack 중심 노출.
- **ClawHub**: 7,911 skills. `Agent Browser`, `ATXP`, `Ontology` 등 고다운로드 항목 확인.
- **VSCode Agent Skills extension 생태**: 검색 1,092 결과(Published Date 기준). `AutomataLabs.copilot-mcp` 80.7K installs, `formulahendry.agent-skills` 1.7K installs, 신생 확장 다수(설치수 1~200대).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| VSCode `agnix - Agent Config Linter` | ✅ 도입 | (1) **필요성**: 외부 스킬 intake 시 SKILL.md/AGENTS.md 정적 검증 자동화 공백 존재. (2) **기존대체**: 현재 체크리스트/수동 감사만으로는 규칙 누락 반복. (3) **비용대비효과**: 확장 자체 도입이 아니라 규칙셋 패턴 흡수라 비용 낮고 품질 게이트 효과 큼. (4) **과대포장검증**: 설치수는 작지만(17) 오히려 과장 마케팅 신호가 약하고, 문제-해결 정합성이 명확. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호(80.7K)는 강하지만 VSCode 중심 운영도구. 현재 OpenClaw CLI 오케스트레이션과 직접 결합도 낮음. **재검토 조건:** 팀 표준 IDE를 VSCode로 통합할 때. |
| MCP Market `Mem0` (latest) | ⚠️ 참고만 | 메모리 서버 효용은 있으나 `openclaw-mem` 실전 검증 기간과 기능 중복이 큼. **재검토 조건:** 회상 정확도/세션 연속성 지표 악화 시. |
| MCP Market `Godot` (featured) | ⚠️ 참고만 | 게임 도메인 적합성은 높지만 현재 MiniPC headless + 내부 godot skill로 1차 대응 가능. **재검토 조건:** 에디터 상호작용 자동화 병목이 반복될 때. |
| SkillsMP recent Android cluster (`android-testing`, `android-architecture` 등) | ⚠️ 참고만 | 구조는 좋지만 현재 핵심 파이프라인(웹게임/툴/마케팅 자동화)과 직접 정합 낮음. **재검토 조건:** Android 네이티브 라인 본격 착수 시. |
| ClawHub `Agent Browser` | ⚠️ 참고만 | 브라우저 자동화 가치 있음. 다만 현재 `browser-cdp-automation` + OpenClaw browser tool로 동일 문제를 해결 중. **재검토 조건:** 현 브라우저 자동화에서 안정성/속도 병목이 누적될 때. |
| SkillHub `AI Video Ad Generator Stack` | ⚠️ 참고만 | 수요는 맞지만 유료/크레딧 의존도가 높고 현재 내부 파이프라인과 일부 중복. **재검토 조건:** 영상 제작 리드타임이 SLA 초과할 때. |

❌ 불필요 판정: **19건**

## ✅ 도입 실행 계획 (구체)
### `agnix` 패턴 내부화 — `agent-config-lint-gate`
1. **Research**: `avifenesh/agnix` 규칙 범위(229 rules)와 파일 스펙(SKILL.md/AGENTS.md/CLAUDE.md/MCP config) 매핑.
2. **Audit**: 실행 시 외부 통신/권한 요구/자동 수정 동작 여부 점검(읽기 전용 lint 우선).
3. **Rewrite**: `misskim-skills/skills/agent-config-lint-gate/`로 내부 스킬 작성 (Research → Audit 결과 반영).
4. **검증**: 현재 `misskim-skills` 내 샘플 30개 대상으로 lint 테스트, false-positive/false-negative 기록.
5. **적용**: external intake 파이프라인의 사전 게이트로 연결(실패 시 Rewrite 단계 진입 금지).

## 보안
- VSCode 확장 탐색 중 `Lobstore Skills`가 **MoltHub** 연계 문구를 노출.
- 정책대로 **Molt Road/molt.host 계열 ABSOLUTE BLOCK** 유지, 즉시 평가 제외.
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`**, blind install 금지.