# 2026-02-18 04:00 KST — Agent Skill Trend Sweep Summary

## Source Status
- SkillsMP: 233,309 skills (recent feed: `query-data`, `data-analysis`, `browsing-workflow`)
- MCP Market: 21,135 servers (latest: `AI Inspector`, `Java Decompiler`, `Dotnet Websearch`)
- SkillHub: 21.3K skills / 5.7M stars (`requesthunt` 포함 Solopreneur Toolkit 유지)
- ClawHub: newest 30개 샘플 수집 (`agents-skill-security-audit` 등)
- VSCode Agent Skills: 1,211 results (`copilot-mcp` 80,815 installs)

## Decisions
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `agents-skill-security-audit` | ✅ 도입 | 외부 스킬 intake의 수동 보안검토 병목을 직접 해소 가능. 내부 재작성 비용 대비 리스크 감소 효과 큼. |
| SkillHub `requesthunt` | ✅ 도입 | 실수요 신호 수집 자동화 공백을 메움. 아이템 선정 리드타임 단축 기대. |
| VSCode `avifenesh.agnix` | ⚠️ 참고만 | lint 아이디어는 유효하나 VSCode 종속. CLI 추출 가능 시 재검토. |
| MCP Market `AI Inspector` | ⚠️ 참고만 | 현재 브라우저 자동화 스택과 기능 중복. 실패율 상승 시 재검토. |
| SkillsMP `query-data` | ⚠️ 참고만 | 분석 니즈는 있으나 현재 핵심 병목과 직접 정합 낮음. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | 설치 신호 강하나 운영축(OpenClaw CLI)과 불일치. |

❌ 불필요 판정: 4건

## Adopt Plan (only)
- `misskim-skills/skills/skill-intake-security-audit-lite/` 설계 착수 (Research → Audit → Rewrite)
- `misskim-skills/skills/request-signal-harvester/` 설계 착수 (Research → Audit → Rewrite)
- Molt Road/molt.host/MoltHub ABSOLUTE BLOCK 유지 + No blind install

## Log File
- `intake-log/2026-02-18-04h-trend-sweep.md`
