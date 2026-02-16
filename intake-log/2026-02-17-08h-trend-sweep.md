# 2026-02-17 08:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot (Sources)
- **SkillsMP:** 브라우저 접근 정상. 총 **227,170 skills** 표시. `recent` 상단은 `android-testing.md`, `android-architecture.md` 등 특정 레포 분해형 스킬 비중이 높음.
- **MCP Market:** 브라우저 접근 정상. 총 **21,087 servers**. 추천/공식 섹션에서 `Godot(1,813)`, `Firecrawl(4,195)`, `Browserbase(3,131)` 확인.
- **SkillHub:** 브라우저 접근 정상. 총 **21.3K skills / 2.4M stars** 표기. `file-search(S 9.0)` 및 Hot 랭킹 노출.
- **ClawHub:** 브라우저 + CLI 정상. `explore`/`inspect`로 최신 항목 확인 (`openclaw-skill-observability`, `openclaw-watchdog` 등).
- **VSCode Agent Skills Extension:** Marketplace 검색 1,089 결과. `Copilot MCP + Agent Skills Manager` **80.6K installs (4.3★)**, `Agent Skills` **1.7K installs (5.0★)**.

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| ClawHub `openclaw-skill-observability` (v0.1.0) | ✅ 도입 | **필요성:** 지난 24시간 기준 비용/실패 세션 통합 뷰가 현재 워크플로에 없음. **기존 대체 한계:** `session_status`는 세션 단위 확인이라 집계 자동화가 약함. **비용 대비 효과:** 코드 규모가 작아 빠르게 내부화 가능, 운영 가시성 즉시 상승. **과대포장 필터:** 홍보 문구 대신 실제 코드(`index.mjs`)를 검토해 기능/한계를 확인했고, 그대로 설치 대신 내부 재작성으로 리스크 통제 가능. |
| MCP Market `Godot` MCP Server | ⚠️ 참고만 | 현재는 MiniPC 헤드리스 + 내부 `godot` 스킬로 주요 요구를 처리 중. 에디터 GUI 제어가 병목으로 드러날 때 재검토. |
| MCP Market `Firecrawl` MCP Server | ⚠️ 참고만 | 대규모 크롤링은 유용하지만 현재는 `browser-cdp-automation`/`web_fetch`로 충분. 크롤링 볼륨이 급증(예: 대량 경쟁분석)하면 재검토. |
| SkillHub `file-search` (S 9.0) | ⚠️ 참고만 | 검색 품질 가이드는 좋지만 내부 `rg/ast-grep` + 코딩 에이전트 루틴과 기능 중복. 서브에이전트 검색 실패율이 증가하면 재검토. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치/평점 신호는 강하지만 현재 운영 중심은 OpenClaw CLI. VSCode 표준 전환 시 가치가 커지므로 그 시점에 재검토. |

**❌ 불필요 판정: 11건**
(플랫폼/워크플로 미스매치, 기존 기능 중복, 신뢰 신호 부족 항목은 개별 나열 생략)

## ✅ Execution Plan (도입 항목만)
1. **Research**
   - 원본 `openclaw-skill-observability` 기능 단위를 분해(비용 집계/실패 세션 탐지/로그 요약).
2. **Audit**
   - 하드코딩 요금표/OS 의존(`journalctl`) 제거 대상 식별.
   - 외부 전송/민감정보 노출 경로 없음 재확인.
3. **Rewrite (internal)**
   - 경로: `misskim-skills/skills/openclaw-observability-lite/`
   - macOS/리눅스 공통 동작으로 재작성(가능한 범위에서 OpenClaw CLI 우선).
   - 출력: 24h 비용 추정표 + 실패 세션 요약 + 오류 지표 스냅샷.
4. **Validation**
   - 샘플 1회 실행해 숫자/세션 집계 일관성 검증.

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/**
- **No blind installs** (직접 설치 금지)
