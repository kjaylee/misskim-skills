# Agent Skill Trend Sweep — 2026-02-15 20:00 KST

## 📊 Executive Summary
- **SkillsMP:** 214,232 skills. Browsing limited to top 5,000; top list dominated by facebook/react SKILL.md. No new must-have items.
- **MCP Market:** 21,012 servers (updated “just now”). Featured list now includes **Godot MCP** (1,798 uses) — direct fit for our Rust+Godot pipeline.
- **SkillHub:** 21.3K skills, 1.6M stars. **New: Git version history + Hot rankings** for provenance.
- **ClawHub:** Highlighted/popular skills visible (Trello/Slack/Caldav/etc) but security posture unchanged → no intake.
- **VSCode Agent Skills extension:** 1,688 installs. Marketplace/search/one‑click install; monitor for official endorsement.
- **Molt Road/molt.host:** **ABSOLUTE BLOCK** maintained (not accessed).

## 🔍 Source Notes
### SkillsMP (skillsmp.com)
- Count: **214,232 skills**; top browsing capped at 5,000.
- Recent top entries: `verify.md`, `extract-errors.md`, `fix.md`, `flags.md`, `flow.md` (facebook/react) → not relevant to current needs.

### MCP Market (mcpmarket.com)
- Count: **21,012 servers**.
- Featured/Official items visible: Bright Data, Firecrawl, ElevenLabs, Magic, Browserbase, **Godot**, Excel, Unity, FastAPI, Ghidra.

### SkillHub (skillhub.club)
- **New platform update:** Git version history + Hot rankings.
- Stats: **21.3K skills**, **1.6M stars**.
- Trending today: wacli, trello, video-frames, slack, nano-pdf (not required).

### ClawHub (clawhub.com)
- Highlighted: Trello, Slack, Caldav Calendar, Answer Overflow.
- Popular: Gog, Wacli, Tavily Web Search, Summarize, Github.
- **Security posture unchanged → no installs.**

### VSCode Agent Skills extension
- **Agent Skills** (Jun Han) shows **1,688 installs**; provides marketplace/search/install/sync for skills in VS Code.

## ✅/⚠️ Candidate Filter Table
| 항목 | 판정 | 근거 |
| --- | --- | --- |
| **Godot MCP Server** (MCP Market, 1,798 uses) | ✅ | 게임 파이프라인에 직접 부합. 에디터 실행/프로젝트 실행/디버그 출력 수집 기능이 유효. **실행 계획:** (1) MCP Market → GitHub 원본 repo 확인, 라이선스/유지보수 점검 (2) 보안 감사: 외부 호출/파일 접근/권한 범위 검토 (3) 샌드박스에서 실행 테스트 (4) 필요한 최소 기능만 남겨 **misskim-skills**로 리라이트 + 커밋 핀 고정 (5) SKILL.md/문서/테스트 추가. |
| **VSCode Agent Skills extension** | ⚠️ | 스킬 탐색/설치 UX 개선 여지 있으나 현재 CLI/내부 프로세스가 충분. **재검토 조건:** (a) Microsoft/Anthropic 공식 인증 또는 보안 리뷰 공개 (b) VSCode 기반 워크플로우로 전환 필요 시 (c) 오프라인/엔터프라이즈 사용 시나리오 확정 시. |

**불필요 판정:** 32건 (SkillsMP 상위 5, SkillHub 트렌딩 8, ClawHub 하이라이트/인기 9, MCP Market 비관련 10)

---
*Survey completed: 2026-02-15 20:00 KST*
*Sources: SkillsMP, MCP Market, SkillHub, ClawHub, VSCode Marketplace*
