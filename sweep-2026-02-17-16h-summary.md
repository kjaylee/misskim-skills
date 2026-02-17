# 2026-02-17 16:00 KST — Agent Skill Trend Sweep Summary

## Source Status
- SkillsMP: 227,170 skills (recent = Android 분해형 다수)
- MCP Market: 21,091 servers (latest: ShellCheck/Appwrite/Mem0 포함)
- SkillHub: Hot leaderboard 570 skills (6h refresh)
- ClawHub: explore 최신 22개 항목 확인
- VSCode Agent Skills: copilot-mcp 80,690 installs / formulahendry.agent-skills 1,714 installs
- Security: Molt Road/molt.host ABSOLUTE BLOCK 유지

## Decisions
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `ShellCheck` MCP | ✅ 도입 | 쉘 스크립트 품질 게이트 공백 직접 해소, 도입비용 대비 회귀 방지 효과 큼. |
| ClawHub `paypal` | ✅ 도입 | 직접결제 퍼널 강화와 정합, webhook 검증 템플릿 공백 보완 가능. |
| ClawHub `dependency-auditor` | ⚠️ 참고만 | 유용하나 `healthcheck`/기존 검증 루프와 일부 중복. |
| SkillHub `audit-website` | ⚠️ 참고만 | 내부 웹 품질 감사 체계로 1차 대체 가능. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호 강하나 VSCode UI 중심, 운영축 불일치. |
| SkillsMP recent Android cluster | ⚠️ 참고만 | 현재 핵심 파이프라인과 직접 연관 약함. |
| MCP Market `Mem0` | ⚠️ 참고만 | `openclaw-mem` 검증 기간과 기능 중복. |

❌ 불필요 판정: 12건

## Adopt Plan (only)
- `misskim-skills/skills/shell-script-guard/` 내부화 설계 (Research → Audit → Rewrite)
- `misskim-skills/skills/payments-paypal-funnel/` 신규 설계 (Research → Audit → Rewrite)
- 외부 스킬 원칙 유지: No blind install

## Log File
- `intake-log/2026-02-17-16h-trend-sweep.md`
