# Agent Skill Trend Sweep — 2026-02-17 12:07 KST

## Scope
- Sources: SkillsMP, MCP Market, SkillHub, ClawHub, VSCode Agent Skills extension
- Principle: **Critical absorption only** (problem-solution fit first)
- Security baseline: **Molt Road / molt.host ABSOLUTE BLOCK**, external skill intake = **Research → Audit → Rewrite → misskim-skills/**

## Collection Snapshot
- **SkillsMP**: 227,170 skills. Recent-sort top feed dominated by Android bundle drops (`android-testing`, `android-architecture`, `android-data-layer` etc., all 2026-02-17).
- **MCP Market**: 21,091 servers (updated ~1h). Latest list includes `ShellCheck`, `Dolex`, `K-Trendz`, `Appwrite`, `European Parliament`, `Mem0`.
- **SkillHub**: 20,922 skills. Top cards still centered on `file-search`, `skill-creator`, `systematic-debugging`, `mcp-builder`, `memory-systems`.
- **ClawHub**: 7,834 skills. Newest feed includes `Arc Security MCP`, `Lily Memory`, `OpenClaw Backup Safe`, plus many low-signal 0★ entries.
- **VSCode Agent Skills**: Search `agent skills` = 1,089 results. `AutomataLabs.copilot-mcp` 80.7K installs, `formulahendry.agent-skills` 1.7K installs, `agnix` 17 installs.

## Critical Filter Table
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `ShellCheck` MCP | ✅ 도입 | **필요성:** 쉘 스크립트 품질 게이트 공백(배포/자동화 스크립트 회귀). **대체성:** 수동 점검으로는 누락 반복. **비용대효과:** 저비용(정적 린트) 대비 실패 예방 ROI 큼. **과대포장 여부:** 단순 lint 도메인이라 검증 용이. |
| ClawHub `Arc Security MCP` | ⚠️ 참고만 | 보안 인테이크 문제와 방향은 맞지만 0★/0 signal 상태. **재검토:** 외부 스킬 흡수량이 주 10건+로 증가하거나 수동 Audit 병목 발생 시. |
| SkillHub `mcp-builder` | ⚠️ 참고만 | MCP 제작 속도 개선 아이디어는 유효하나 내부 `openapi-tool-scaffold`/`mcporter`로 1차 대응 가능. **재검토:** MCP 제작 리드타임이 2회 이상 지연될 때. |
| VSCode `agnix` (Agent Config Linter) | ⚠️ 참고만 | SKILL/AGENTS lint 자체는 유의미하지만 VSCode 의존(17 installs)으로 운영축(OpenClaw CLI)과 불일치. **재검토:** VSCode 표준 워크플로 전환 시. |
| ClawHub `Lily Memory` | ⚠️ 참고만 | 메모리 문제 해결 주장 있으나 현재는 `openclaw-mem` 실전 검증 구간. 중복 도입 시 운영 복잡도 증가. **재검토:** 현 메모리 지표 하락(회상 실패율 상승) 시. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호는 강함(80.7K)이나 IDE 플러그인 중심이라 현재 오케스트레이션(터미널/세션 기반)과 불일치. **재검토:** IDE 기반 협업 운영을 공식 채택할 때. |

**불필요 판정:** 14건

## ✅ Adoption Plan (ShellCheck MCP pattern)
1. **Research (오늘):** `shellcheck` MCP 원본 구조/라이선스/실행권한 범위 점검.
2. **Audit (오늘):** 네트워크 호출/임의 실행 경로/파일 접근 범위 검사.
3. **Rewrite (다음 스텝):** `misskim-skills/skills/shell-script-guard/` 내부형 스킬로 재작성(외부 의존 최소화).
4. **Gate Integration:** `scripts/*` 변경 시 lint precheck 단계 추가(실패 시 커밋 차단).
5. **Validation:** 최근 자주 만지는 배포/운영 스크립트 샘플 10개로 오탐/누락률 측정.

## Security Notes
- `moltworld` 및 Molt 계열 키워드 항목 확인했으나 **ABSOLUTE BLOCK 정책 유지**.
- 이번 회차 외부 원본은 **블라인드 설치 0건**.
