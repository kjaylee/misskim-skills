# 2026-02-21 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **우선 수집:** `web_search + web_fetch` 시도.
- **실제 상태:** Brave `web_search` 429(quota), MCP Market 429(Vercel checkpoint), ClawHub API rate limit 발생.
- **대체 경로:** `r.jina.ai + direct API`로 수집 지속.
- **핵심 스냅샷:**
  - SkillsMP: `239,658` skills, 평균 `1,762.2`, 피크 `19,898 (@ Feb 4, 2026)`, Security `5,913`.
  - SkillHub: `21,564 skills / 5.1M stars`, Trending Top5 `discord / nano-banana-pro / gifgrep / feishu-drive / model-usage`.
  - ClawHub: partial latest 샘플 확보 후 429 (`aetherlang-karpathy-skill`, `semfind`, `agent-rate-limiter` 등).
  - VSCode Agent Skills: `copilot-mcp` `81,509 installs`, `agent-skills` `1,789 installs`, `agent-skill-ninja` `559 installs`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `file-search` 패턴 (ripgrep + ast-grep 운영 플레이북) | ✅ 도입 | **Q1 필요성:** 코드 탐색 과다 결과/문맥 오염 병목이 반복됨. **Q2 대체성:** 도구는 있으나 표준 실행 스킬이 없음. **Q3 비용효과:** 내부 문서형 재작성으로 저비용·즉시효과 가능. **Q4 과대포장 필터:** 별점 대신 최근 10개 작업의 탐색시간 단축률로 검증 가능. |
| ClawHub `agent-rate-limiter` | ⚠️ 참고만 | 429 대응 니즈는 맞지만 search-fallback 라인과 목적이 겹침. `installsCurrent=0`/낮은 지표로 신뢰 신호가 약해 즉시 도입 보류. **재검토:** fallback 실패율이 목표 초과(>10%)일 때. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | 설치 신호는 강하나 VSCode 종속 비용이 큼. OpenClaw CLI 운영으로 대체 가능. **재검토:** VSCode 협업 비중 50%+ 전환 시. |
| MCP Market direct intake | ⚠️ 참고만 | 필요 소스이나 이번 회차 429 차단으로 품질 비교 불가. **재검토:** checkpoint 해제 후 최신 상위 50개 재평가 시. |

**❌ 불필요 판정: 34건**

## ✅ 도입 실행 계획 (상세)
1. **Research:** SkillHub `file-search`의 단계(타깃 축소 → 패턴 검색 → 증거 캡처)만 추출.
2. **Audit:** 우리 코드베이스 기준 false-positive 억제 규칙(경로 우선순위, 제외 패턴) 정의.
3. **Rewrite:** `misskim-skills/skills/code-search-playbook/` 내부 스킬로 재작성 (외부 코드 무복사).
4. **Validate:** 최근 10개 코드 작업에서 탐색시간/오탐률 전후 비교.
5. **Adopt Gate:** 기준 통과 시 subagent 표준 진입 루틴으로 승격.

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-16h-trend-raw.json`
- `intake-log/2026-02-21-16h-trend-sweep.md`
