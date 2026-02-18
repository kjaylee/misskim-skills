# 2026-02-19 00:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 접근 성공. 총 **239,658 skills**. `recent` 상단에 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 계열 확인.
- **MCP Market**: 브라우저 접근 성공. 총 **21,325 servers**. `Latest MCP Servers`에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `Vigilo` 확인(다수 0 usage).
- **SkillHub (skillhub.club)**: **21.3K skills / 4.7M stars**. Hot/Trending에 `systematic-debugging`, `file-search`, `context-optimization` 지속 노출.
- **ClawHub**: `clawhub explore --sort newest --limit 40 --json` 수집. 신규군 `my-fitness-claw`, `wiz-light-control`, `lark-base`, `agent-audit`, `ddg-web-search` 확인.
- **VSCode Agent Skills 생태**: 검색 `agent skills` 기준 **1,095 results**. `formulahendry.agent-skills` **1,741 installs**, `copilot-mcp` 81K. `Lobstore Skills`는 MoltHub 연동 문구 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `ddg-web-search` | ✅ 도입 | **Q1 필요성:** 이번 회차도 `web_search`가 Brave 429로 즉시 실패해 리서치 파이프라인이 막힘. **Q2 대체성:** 현재는 `browser/web_fetch` 수동 우회만 있어 자동 fallback 표준이 없음. **Q3 비용효과:** 패턴 흡수 후 내부 래퍼화 비용이 낮고, 수집 성공률 즉시 개선 가능. **Q4 과대포장 필터:** 다운로드 607·1★는 강한 품질보증이 아니므로 코드 도입이 아닌 패턴만 채택. |
| MCP Market `Vigilo` | ⚠️ 참고만 | **Q1:** 에이전트 툴콜 감사 니즈는 유효. **Q2:** 현재 `sessions_history`/로그 체계로 1차 대응 가능. **Q3:** 별도 ledger 운영비가 즉시 ROI를 압도하지 못함. **Q4:** latest 노출·낮은 사용량은 품질 보증 아님. **재검토:** 감사/포렌식 요구가 주 2회 이상 반복될 때. |
| SkillHub `context-optimization` | ⚠️ 참고만 | **Q1:** 컨텍스트 비용 최적화는 중요. **Q2:** `openclaw-mem` + 내부 메모리 규율과 기능 중복. **Q3:** 추가 도입 대비 개선폭 불명확. **Q4:** star/랭킹은 마케팅 편향 가능. **재검토:** 토큰비 급증 또는 회상 실패율 임계치 초과 시. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | **Q1:** 테스트 자동화 목적은 맞음. **Q2:** `verify-before-done`/`tdd-discipline`/기존 CI 루틴으로 핵심 기능 충족. **Q3:** 외부 스킬 흡수 대비 편익 제한. **Q4:** 최신 노출(0~저별점)만으로 품질 판단 불가. **재검토:** 테스트 회귀가 반복되고 현 루틴으로 탐지 누락될 때. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | **Q1:** IDE 내 스킬 탐색 편의는 존재. **Q2:** 현재 운영축은 OpenClaw CLI + subagent. **Q3:** VSCode 종속 도입비 대비 실효 낮음. **Q4:** installs 1.7K/리뷰 표본 1건은 신뢰도 제한. **재검토:** VSCode 중심 협업이 공식 표준으로 전환될 때. |

❌ 불필요 판정: **17건**
- (요약) Molt 계열 연동 항목(정책 차단), 트레이딩/개인취미 중심 저신뢰 스킬, 0-usage 최신 MCP 다수.

## ✅ 도입 실행 계획
### `search-fallback-router` (신규 내부 스킬)
1. **Research**: `ddg-web-search`의 DuckDuckGo Lite 질의/파싱 구조만 추출.
2. **Audit**: 외부 전송 범위, query logging, 스팸/광고 필터 규칙 점검.
3. **Rewrite**: `misskim-skills/skills/search-fallback-router/`로 내부 재작성 (외부 코드 direct install 금지).
4. **Integration**: `web_search`가 429/쿼터초과면 자동 fallback 라우팅하도록 브리핑/트렌드 스윕 루틴에 연결.
5. **Validation**: 1주간 `검색 성공률`, `평균 지연`, `재시도 횟수` 비교 후 표준화 여부 결정.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
