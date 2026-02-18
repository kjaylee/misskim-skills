# 2026-02-19 04:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 접근 성공. 총 **239,658 skills**. recent 상단에서 `shadmin-feature-dev`, `nippo`, `check-tests-commit` 확인.
- **MCP Market**: 브라우저 접근 성공. 총 **21,325 servers**(Updated: just now). `Latest MCP Servers`에 `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants`, `Vigilo` 확인.
- **SkillHub (skillhub.club)**: 브라우저 기준 **21.3K skills / 4.3M stars**. Trending Today 상단 `feishu-drive`, `model-usage`, `github`, `wacli`, `trello` 노출.
- **ClawHub**: `clawhub explore --sort newest --limit 40 --json` 수집(실수집 38개). 신규군에서 `memory-tools`, `gstd`, `proxymock`, `openrouter-perplexity`, `exa-tool` 확인. `moltbook-cli-tool` 노출 확인.
- **VSCode Agent Skills extension 생태**: 검색 `agent skills` **1,099 results**. `AutomataLabs.copilot-mcp` **81K installs**, `formulahendry.agent-skills` **1.7K installs**, `yamapan.agent-skill-ninja` **537 installs**. `Lobstore Skills`는 MoltHub 연동 문구 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `openrouter-perplexity` | ✅ 도입 | **Q1 필요성:** 이번 회차에서 Brave Search quota 초과(429)로 리서치가 즉시 중단됨. **Q2 대체성:** 현재는 `browser/web_fetch` 수동 우회 위주라 자동 fallback이 부족. **Q3 비용효과:** 기존 OpenRouter 운용 맥락에서 패턴 흡수→내부 재작성 비용이 낮고, 검색 성공률 개선 효과가 큼. **Q4 과대포장 필터:** downloads 63 / 0★는 품질 보증이 아니므로 코드 직설치 없이 패턴만 흡수. |
| ClawHub `memory-tools` | ⚠️ 참고만 | **Q1:** 메모리 정합성 니즈는 유효. **Q2:** 현재 `openclaw-mem` + 메모리 규율로 1차 충족. **Q3:** 메모리 레이어 교체 비용/리스크가 큼. **Q4:** 높은 다운로드 신호(1,365)만으로 품질/적합도 확정 불가. **재검토:** 회상 실패가 주 3회 이상 반복될 때. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | **Q1:** 검색 백업 니즈는 명확. **Q2:** `openrouter-perplexity` 패턴과 목적 중복 가능성 높음. **Q3:** 추가 공급자/운영 포인트 증가 대비 즉시 이득 불명확. **Q4:** Latest 노출 + 0 usage는 품질 보증 아님. **재검토:** 1차 fallback 실패율이 임계치(>20%)를 넘을 때. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | **Q1:** 테스트-커밋 게이트 니즈는 유효. **Q2:** `verify-before-done` + `tdd-discipline`로 핵심 기능 대응 중. **Q3:** 도입 대비 편익이 제한적. **Q4:** recent 상단 노출/저신호(0★)만으로 채택 근거 약함. **재검토:** 회귀 버그가 2회 이상 연속 발생할 때. |
| SkillHub `skill-creator` | ⚠️ 참고만 | **Q1:** 스킬 제작 자동화 니즈는 존재. **Q2:** 내부 `skill-authoring`/기존 작성 규약으로 대체 가능. **Q3:** 추가 도입 시 템플릿 중복 관리비 발생. **Q4:** 평점/트라이 수는 참고 신호일 뿐 실품질 보증 아님. **재검토:** 내부 스킬 제작 리드타임이 현재 대비 30% 이상 악화될 때. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | **Q1:** 확장 생태 관리 수요는 존재. **Q2:** 현재 운영축은 OpenClaw CLI + 서브에이전트로 VSCode 의존도가 낮음. **Q3:** IDE 종속 도입비 대비 생산성 개선 불확실. **Q4:** 81K installs는 배포력 신호일 뿐 우리 환경 적합성 보증 아님. **재검토:** VSCode 중심 협업이 공식 표준으로 전환될 때. |

❌ 불필요 판정: **18건**
- (요약) Molt 계열 연동 항목(정책 차단), 트레이딩/개인취미 중심 저정합 스킬, 0-usage 최신 MCP 다수.

## ✅ 도입 실행 계획
### `search-fallback-openrouter` (내부 신규 스킬)
1. **Research**: `openrouter-perplexity`의 질의/응답 구조, citation 처리 방식만 추출.
2. **Audit**: 키 처리(`OPENROUTER_API_KEY`), 로그 마스킹, rate-limit/backoff 정책 점검.
3. **Rewrite**: `misskim-skills/skills/search-fallback-openrouter/`로 내부 재작성 (외부 코드 direct install 금지).
4. **Integration**: 검색 루틴을 `Brave 실패(429/quota) → OpenRouter fallback → browser 수동 fallback` 순으로 표준화.
5. **Validation**: 1주간 `검색 성공률`, `평균 응답시간`, `재시도 횟수` 계측 후 표준 채택 여부 결정.

## 보안
- **Molt Road / molt.host / MoltHub / Moltbook: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
