# 2026-02-18 12:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 기준 **233,309 skills**. browse 상단에서 `mintlify`, `feishu-doc`, `obsidian` 등 확인.
- **MCP Market**: 브라우저 기준 **21,157 servers**. latest에 `Java Decompiler`, `Dotnet Websearch`, `Turtle Noir`, `SQL Sentinel`, `OpenWrt`(대부분 0 usage).
- **SkillHub.ai**: 여전히 **“Coming soon”** 랜딩(실사용 카탈로그 부재).
- **ClawHub**: `clawhub explore --sort newest --limit 20 --json` 기준 `faster-whisper`, `web-qa-bot`, `arc-compliance-checker` 확인.
- **VSCode Agent Skills 검색**: Marketplace `agent skills` 결과 **1,095개**. `copilot-mcp`(80.9K), `agent-skills`(1.7K), `Lobstore Skills`(158) 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `arc-compliance-checker` | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake의 정책 준수 판정 자동화 공백이 실제 병목. **Q2 대체성:** 기존 체크리스트/수동 리뷰만으로는 예외·위반 추적 일관성 부족. **Q3 비용효과:** Python 기반 규칙 엔진 패턴 흡수 비용이 낮고 감사 리드타임 단축 효과가 큼. **Q4 과대포장 필터:** 다운로드/별점은 낮지만(19/0) 현재 우리 문제와 직접 정합이라 마케팅 지표보다 실효성 우선. |
| ClawHub `web-qa-bot` | ✅ 도입 | **Q1 필요성:** 기능 안정성 우선 정책 대비, 웹 도구/페이지의 스모크+시각 회귀 자동화가 아직 표준화되지 않음. **Q2 대체성:** `web-design-guidelines`+browser-cdp로 부분 대응 가능하나 회귀 테스트 파이프라인은 부재. **Q3 비용효과:** 기존 브라우저 스택 재사용으로 내부 경량 래퍼 구현 가능(도입비 중간, 회귀비용 절감 큼). **Q4 과대포장 필터:** 설치/별점 신호는 약함(0/0) → 원본 도입이 아닌 ‘패턴 흡수 후 내부 재작성’ 조건으로만 채택. |
| ClawHub `faster-whisper` | ⚠️ 참고만 | **Q1:** STT 지연 개선 가능성은 있음. **Q2:** 이미 `openai-whisper`/`openai-whisper-api` 보유. **Q3:** 모델/런타임 운영비(디스크·의존성) 발생. **Q4:** “4~6x” 마케팅 수치가 우리 워크로드에서 재현되는지 불명확. **재검토:** 음성 전사 평균 처리시간이 SLA 초과할 때 벤치마크 후 판단. |
| MCP Market `Task Master` | ⚠️ 참고만 | **Q1:** 작업 오케스트레이션 니즈는 존재. **Q2:** `scripts/queue-manager.sh` + OpenClaw subagent 운영으로 핵심 요구 충족 중. **Q3:** MCP 추가 운영복잡도 대비 즉시 이득 제한적. **Q4:** 높은 사용량(25K+)은 신호지만 우리 파이프라인 적합성 증거는 별도 필요. **재검토:** 큐 정체/우선순위 충돌이 주 3회 이상 발생 시. |
| SkillsMP `query-data` 계열 | ⚠️ 참고만 | **Q1:** 분석 질의 표준화는 유효. **Q2:** 현재 최우선 병목은 수익화/배포/QA 게이트. **Q3:** 도입해도 즉시 ROI 낮음. **Q4:** 대형 카탈로그 노출이 품질을 보장하진 않음. **재검토:** 운영 의사결정이 데이터 질의 병목으로 지연될 때. |
| VSCode `copilot-mcp` / `agent-skills` 확장군 | ⚠️ 참고만 | **Q1:** IDE 내 탐색 편의는 있음. **Q2:** 우리 운영축은 OpenClaw CLI 중심(비-IDE 자동화). **Q3:** VSCode 종속 도입비 대비 체감효과 낮음. **Q4:** 설치수(80.9K/1.7K)는 신호이나 품질·보안 보증 아님. **재검토:** VSCode 기반 작업 비중이 명확히 증가할 때. |

❌ 불필요 판정: **13건**
- (요약) 0-usage 최신 MCP 다수, 스택 중복형 ClawHub 신규군, 저신뢰 VSCode 파생 확장군.

## ✅ 도입 실행 계획
### 1) `skill-intake-policy-gate` (carry + 실행)
1. **Research**: `arc-compliance-checker` 규칙/예외/상태 모델만 추출.
2. **Audit**: 우리 기준으로 룰셋 고정(credential 노출, 위험 쉘, 원격 다운로드, Molt 계열 차단).
3. **Rewrite**: `misskim-skills/skills/skill-intake-policy-gate/` 내부 구현(외부 코드 직접 의존 금지).
4. **Gate 연동**: intake 파이프라인 precheck 단계에 강제 적용.

### 2) `web-regression-guard` (신규)
1. **Research**: `web-qa-bot`의 스모크/접근성/시각 회귀 시나리오 패턴만 추출.
2. **Audit**: 외부 호출·권한·브라우저 실행 경로 점검.
3. **Rewrite**: `misskim-skills/skills/web-regression-guard/` 내부 스킬로 재작성.
4. **Pilot**: 상위 3개 웹 자산에 주기 실행, flaky ratio/실패 재현율 측정 후 본 도입.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
