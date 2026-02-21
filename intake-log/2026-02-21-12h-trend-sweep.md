# 2026-02-21 12:10 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 요약
- **브라우저 제약 준수:** Mac Studio `target=host` 브라우저 미사용.
- **수집 우선순위:** `web_search + web_fetch` 우선 시도.
- **실제 상태:** Brave `web_search` 429(quota), MCP Market 429(Vercel checkpoint)로 일부 차단.
- **대체 경로:** `r.jina.ai` + direct API/CLI로 수집 지속.
- **소스 스냅샷:**
  - SkillsMP: 총 `239,658`, 평균 `1,762.2`, 피크 `19,898 (@ Feb 4, 2026)`, `security` 검색 `8,590`.
  - SkillHub: `21.6K Skills / 4.8M Stars`, Trending Top5 `gifgrep / feishu-drive / model-usage / wacli / slack`.
  - clawhub.com(=clawhub CLI): newest 30 / trending 29 샘플 수집.
  - VSCode Agent Skills 관련 확장: relevance 필터 `32`개, 상위 `AutomataLabs.copilot-mcp (81,492 installs)`.
  - MCP Market: 직접 수집 차단(HTTP 429).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `file-search` 패턴 (ripgrep + ast-grep 워크플로) | ✅ 도입 | **Q1 필요성:** 코드 탐색 시 결과 과다/컨텍스트 오염 병목이 반복됨. **Q2 대체성:** 도구는 있으나 검색 전략을 강제하는 실행 스킬 부재. **Q3 비용효과:** 문서형 스킬 재작성으로 저비용·고빈도 절감 기대. **Q4 과대포장 필터:** 설치/별점 대신 최근 10개 작업의 탐색시간 단축률로 검증 가능. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | **Q1:** 니즈 일부 존재. **Q2:** OpenClaw + clawhub CLI로 대체 가능. **Q3:** VSCode 종속 비용 큼. **Q4:** 설치수 대비 리뷰 표본(8) 작아 품질 신뢰 제한. |
| ClawHub newest 저신뢰 클러스터 (`bitcoin-daily`, `update-plus`, `lobster` 등) | ⚠️ 참고만 | **Q1:** 일부 기능은 유용 가능. **Q2:** 요약/자동화/운영 영역 중복 다수. **Q3:** 설치·감사 비용 대비 ROI 낮음. **Q4:** 낮은 `installsCurrent`와 급증 패턴은 과대포장 가능성. |
| MCP Market direct intake | ⚠️ 참고만 | **Q1:** 필요. **Q2:** 이번 회차는 접근 차단으로 비교 근거 부족. **Q3:** 우회 자동화보다 접속 안정화가 우선. **Q4:** 차단 상태에선 품질검증 불가. |

**❌ 불필요 판정: 32건**

## ✅ 도입 실행 계획 (상세)
1. **Research**: SkillHub `file-search` 절차를 단계화(타깃 축소 → 패턴 탐색 → 증거 캡처).
2. **Audit**: 우리 워크스페이스 기준 false-positive 억제 규칙 정의.
3. **Rewrite**: `misskim-skills/skills/code-search-playbook/` 내부 스킬로 재작성 (외부 코드 무복사).
4. **Validate**: 최근 10개 코드 작업에서 탐색 시간/오탐률 측정.
5. **Adopt Gate**: 기준 통과 시 `subagent-dev`/`verify-before-done` 전 단계 공통 루틴으로 편입.

## 보안
- `Molt Road / molt.host` **ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)

## 산출물
- `intake-log/2026-02-21-12h-trend-raw.json`
- `intake-log/2026-02-21-12h-trend-sweep.md`
