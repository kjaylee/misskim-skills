# 2026-02-19 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 수집 성공. 총 **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 확인.
- **MCP Market**: 브라우저 수집 성공. 총 **21,362 servers**(Updated: just now). `Latest MCP Servers` 상단 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club)**: 브라우저 수집 성공. **21.6K skills / 4.1M stars**. Hot/Rankings 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack` 확인.
- **ClawHub**: `clawhub explore --sort newest --limit 40 --json` 수집. 신규군 `clawguarddevin`, `openclaw-cache-kit`, `agent-spawner` 확인. Molt 계열(`moltbook-*`) 노출 감지.
- **VSCode Agent Skills extension**: Marketplace 검색 `agent skills` **1,103 results**. `Copilot MCP + Agent Skills Manager` **81.1K installs**, `Agent Skills` **1.8K installs**, `agnix - Agent Config Linter` **18 installs** 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `clawguarddevin` 패턴 | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake에서 악성 패턴(역쉘/탈취/난독화) 자동 스캔 공백이 현재 실존. **Q2 대체성:** 기존 운영은 수동 Audit 중심이라 누락 리스크 존재. **Q3 비용효과:** IOC 룰셋을 내부 게이트로 재작성하면 구현비가 낮고 사고비용 회피효과가 큼. **Q4 과대포장 필터:** 설치/별점 신호 약함(0~저신호). 채택 근거는 인기 아닌 보안 갭 해소. |
| VSCode `agnix` 룰셋(패턴 흡수) | ✅ 도입 | **Q1 필요성:** SKILL.md/AGENTS/MCP 설정 검증이 현재 텍스트 리뷰 의존이라 품질 편차가 큼. **Q2 대체성:** 내부에 동등한 자동 lint 게이트 부재. **Q3 비용효과:** VSCode 확장 자체 도입 대신 룰셋만 추출·재작성하면 유지비 낮고 리뷰시간 절감 효과 확실. **Q4 과대포장 필터:** 설치수는 낮지만(18) ‘룰 품질’이 핵심 자산이라 마케팅 신호 영향 작음. |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 뉴스레터 자동화 수요는 유효하나 현재 핵심 병목(게임/툴 배포·수익화 즉시 실행)과 직접 정합 낮음. **재검토:** Substack 채널 KPI를 월간 운영목표로 올릴 때. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 fallback 가치가 있으나 기존 fallback 라인(웹검색/대체 라우팅)과 중복 가능성이 큼. **재검토:** 검색 실패율이 SLA 임계치 초과 시. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 테스트-커밋 자동화는 유용하지만 내부 `verify-before-done` + SDD/TDD 규율로 핵심 수요를 이미 충족. **재검토:** 회귀 결함이 연속 발생할 때. |
| SkillHub 상위군(`coding-agent`, `feishu-drive`, `model-usage`) | ⚠️ 참고만 | 이미 보유/유사 역량이 높아 순증 가치가 낮음. 대형 star는 확산 신호일 뿐 운영 적합성 증거가 아님. **재검토:** 협업툴 스택 전환(Feishu 표준화) 시. |
| ClawHub `openclaw-cache-kit` | ⚠️ 참고만 | 비용절감 잠재력은 있으나 설정 변경 리스크(캐시 정책/heartbeat) 검증 없이 즉시 도입하면 운영 안정성 저하 가능. **재검토:** 주간 토큰비용이 기준치 초과하고 staging 검증 슬롯 확보될 때. |

❌ 불필요 판정: **81건**
- (요약) Molt 연계/트레이딩·취미성/저신뢰(0 usage·0★) 항목 다수는 현재 문제 해결과 무관해 제외.

## ✅ 도입 실행 계획
### 1) `skill-intake-malware-gate` (신규 내부 스킬)
1. **Research**: `clawguarddevin`의 IOC 분류 체계(역쉘·탈취·난독화·외부드롭퍼)만 추출.
2. **Audit**: 오탐률, 우회 가능 패턴, 로그 마스킹, 성능(대량 스캔 시 지연) 점검.
3. **Rewrite**: `misskim-skills/skills/skill-intake-malware-gate/`로 내부 구현(외부 의존 최소화).
4. **Integration**: 외부 스킬 인입 파이프라인의 pre-merge 게이트로 연결.
5. **Validation**: clean 샘플/악성 샘플 세트 회귀테스트 후 룰셋 고정.

### 2) `agent-config-lint-gate` (신규 내부 스킬)
1. **Research**: `agnix` 규칙군에서 SKILL.md/AGENTS/MCP 정합성 규칙만 선별.
2. **Audit**: 우리 규약(Research→Audit→Rewrite, 금지 도메인, 도구 정책)과 충돌 규칙 제거.
3. **Rewrite**: `misskim-skills/skills/agent-config-lint-gate/`로 CLI/CI 친화형 내부 구현.
4. **Integration**: intake PR 체크(필수) + 로컬 pre-commit 옵션 제공.
5. **Validation**: 정상/오류 샘플 파일셋으로 lint 정확도 기준 통과 시 운영 전환.

## 보안
- **Molt Road / molt.host / MoltHub / Moltbook: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
