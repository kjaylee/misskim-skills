# 2026-02-18 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 루트/탐색 경로는 Cloudflare 403로 차단. `sitemap.xml`만 접근 가능(구조 확인용). 실시간 신규 스킬 본문은 직접 검증 불가.
- **MCP Market**: `mcpmarket.com` 직접 수집 성공. 홈 `Latest MCP Servers`에 `java-decompiler-1`, `dotnet-websearch`, `turtle-noir`, `sql-sentinel`, `openwrt` 확인. sitemap 기준 서버 URL **21,091개**.
- **SkillHub (skillhub.club)**: 홈 기준 **21.3K Skills / 4.6M Stars**. Hot 영역에 `systematic-debugging`, `file-search`, `context-optimization` 노출.
- **ClawHub**: `clawhub explore --sort newest --limit 20 --json` 수집 성공. 신규군에 `agent-audit`, `security-sentinel`, `fathom-meetings` 확인.
- **VSCode Agent Skills extension**: `formulahendry.agent-skills` 페이지 기준 **1,737 installs** 확인(검색군은 1,095 results 기준 유지).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `agent-audit` | ✅ 도입 | **Q1 필요성:** 서브에이전트/크론/모델 사용량이 늘면서 “비용-성과 감사”가 수동 병목. **Q2 대체성:** `session_status`/수동 점검으로는 통합 ROI 리포트 자동화가 부족. **Q3 비용효과:** read-only 감사 패턴 흡수 후 내부화 비용이 낮고 낭비 탐지 효과가 큼. **Q4 과대포장 필터:** 다운로드 2/별점 0으로 인기 신호는 약함 → 오직 실문제 정합성으로 채택. |
| ClawHub `security-sentinel` | ⚠️ 참고만 | **Q1:** 보안 점검 니즈는 상시 존재. **Q2:** `healthcheck`/기존 보안 루틴과 중복 범위 큼. **Q3:** 중복 도입 시 운영비 증가. **Q4:** 지표 약함(24 downloads, 0★). **재검토:** 비밀키/취약점 누락 사고가 반복될 때. |
| MCP Market `SQL Sentinel` | ⚠️ 참고만 | **Q1:** SQL 안전성은 중요하나 현재 핵심 파이프라인은 DB 직접운영 비중이 낮음. **Q2:** 현재 단계는 기존 도구로 충분. **Q3:** MCP 추가 운영비 대비 즉시효과 제한. **Q4:** latest 노출/0 usage는 품질 보증 아님. **재검토:** DB 질의 자동화 비중이 KPI로 상승할 때. |
| SkillHub `context-optimization` | ⚠️ 참고만 | **Q1:** 컨텍스트 절감 니즈는 유효. **Q2:** `openclaw-mem` + 내부 메모리 규율로 핵심 요구 대응 중. **Q3:** 추가 도입 효과 불확실. **Q4:** 스타/랭킹은 마케팅 편향 가능. **재검토:** 토큰 초과·회상 실패율이 임계치 초과 시. |
| SkillsMP `mintlify` (직접 검증 제한) | ⚠️ 참고만 | **Q1:** 문서 자동화는 유용. **Q2:** 현재 docs 파이프라인으로 운영 가능. **Q3:** 현 우선순위(수익화/QA/배포) 대비 ROI 낮음. **Q4:** 사이트 실시간 접근 차단 상태라 품질 검증 불충분. **재검토:** 외부 문서 배포가 실제 병목으로 측정될 때. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | **Q1:** IDE 내 탐색 편의성은 있음. **Q2:** 현재 운영축은 OpenClaw CLI/서브에이전트 중심. **Q3:** VSCode 종속 도입비 대비 체감효과 제한. **Q4:** 1,737 installs 신호만으로 품질 보장 불가. **재검토:** VSCode 중심 협업 비중이 명확히 증가할 때. |

❌ 불필요 판정: **15건**
- (요약) Molt 계열(정책 차단), 0-usage 최신 MCP 다수, 현재 우선순위와 불일치한 마케팅/트레이딩/소셜 자동화 항목.

## ✅ 도입 실행 계획
### `agent-cost-audit-gate` (신규 내부 스킬)
1. **Research**: `agent-audit`의 감사 관점(모델 선택/크론 낭비/ROI 계산 방식)만 추출.
2. **Audit**: read-only 보장, 외부 전송 금지, 민감정보 마스킹 규칙 확정.
3. **Rewrite**: `misskim-skills/skills/agent-cost-audit-gate/`로 내부 재작성(외부 코드 직접 의존 금지).
4. **Pilot**: 주 2회 자동 실행해 비용 절감 후보(모델 과사용, 과도한 cron)를 리포트.
5. **Gate**: 1주 검증 후 `cost-saving signal`이 유의하면 표준 운영 루틴 편입.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
