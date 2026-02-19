# 2026-02-19 20:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 수집 성공. 검색창 기준 **239,658 skills**. recent 상단 `shadmin-feature-dev`, `nippo`, `check-tests-commit`, `maxxit-lazy-trading`, `audio-extractor` 확인.
- **MCP Market**: 브라우저 수집 성공. 메인 기준 **21,362 servers**. `Latest MCP Servers` 상단 `Substack Publisher`, `DevOps Practices`, `LibreNMS`, `Gemini Search`, `Zen of Languages`, `MyInstants` 확인.
- **SkillHub (skillhub.club)**: 브라우저 수집 성공. 메인 기준 **21.6K skills / 4.0M stars**. Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack` 확인.
- **ClawHub**: `clawhub explore --sort newest --limit 30 --json` 수집. `guardian`, `openclaw-skillguard`, `agents-skill-security-audit`, `browser-auth`, `crypto-trader` 등 확인.
- **VSCode Agent Skills extension**: Marketplace 검색 `agent skills` **1,102 results**. `AutomataLabs.copilot-mcp` **81.1K installs**, `formulahendry.agent-skills` **1.8K installs**, `avifenesh.agnix` **19 installs** 확인.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `guardian` (v1.7.0 privacy-audit 패턴) | ✅ 도입 | **Q1 필요성:** 외부 스킬 재배포/내부화 시 개인경로·로컬데이터 유입 차단 게이트가 아직 약함. **Q2 대체성:** 기존 malware/lint 방향은 코드 악성·형식 검증 중심이라 패키징 개인정보 누출 검출을 완전 대체하지 못함. **Q3 비용효과:** 배포 전 정적 스캔(민감 경로/샘플데이터/하드코딩 토큰) 룰셋 구현비가 낮고 사고비용 회피효과가 큼. **Q4 과대포장 필터:** 다운로드/별점 신호보다 릴리스 노트의 구체적 누출 수정 내역이 채택 근거. |
| ClawHub `openclaw-skillguard` | ⚠️ 참고만 | 보안 스캔 방향은 유효하나 우리가 이미 추진 중인 `skill-intake-malware-gate`/`agent-config-lint-gate`와 범위 중복이 큼. **재검토:** 현재 게이트 구현 후 탐지 공백(오탐/미탐) 수치가 임계치 초과할 때. |
| VSCode `agnix - Agent Config Linter` | ⚠️ 참고만 | 룰셋 자산 가치는 높지만 VSCode 종속 도입은 현재 OpenClaw CLI 중심 운영과 정합 낮음. **재검토:** 내부 lint 게이트 MVP 완성 후 룰 커버리지 확장이 필요할 때(룰팩만 흡수). |
| MCP Market `Substack Publisher` | ⚠️ 참고만 | 뉴스레터 채널 확장성은 좋지만 현재 핵심 병목(게임/툴 배포·수익화)과 직접 정합이 낮음. **재검토:** Substack을 분기 KPI 채널로 승격할 때. |
| MCP Market `Gemini Search` | ⚠️ 참고만 | 검색 fallback 니즈는 유효하지만 기존 fallback 라인과 중복 가능성이 큼. **재검토:** 검색 실패율/SLA가 기준치를 초과할 때. |
| SkillsMP `check-tests-commit` 계열 | ⚠️ 참고만 | 자동 테스트-커밋은 유용하나 현재 SDD/TDD + verify-before-done 규율로 핵심 문제를 상당 부분 커버 중. **재검토:** 회귀 결함이 연속 발생할 때. |
| SkillHub Trending 상위군(`coding-agent`,`feishu-drive`,`model-usage`) | ⚠️ 참고만 | 확산 신호는 강하지만 보유 스킬/도구와 기능 중복이 커 순증 효과가 제한적. **재검토:** 협업 스택이 Feishu 중심으로 바뀌거나 모델 사용량 관제 병목이 생길 때. |

❌ 불필요 판정: **72건** (샘플 79건 기준)
- MoltHub 연계 항목 1건(`Lobstore Skills`) 포함 정책 차단, 트레이딩/저신뢰(0 usage·0★)·현업 미정합 항목 다수 제외.

## ✅ 도입 실행 계획
### `skill-package-privacy-gate` (신규 내부 스킬)
1. **Research**: `guardian`의 privacy-audit 포인트(개인경로, 샘플데이터, 기본 trusted source, 민감 파일 포함 실수)만 추출.
2. **Audit**: 우리 배포 정책(Research → Audit → Rewrite, 금지 도메인, no blind install)과 충돌 여부/오탐률 점검.
3. **Rewrite**: `misskim-skills/skills/skill-package-privacy-gate/`로 내부 재작성 (외부 코드 직접 도입 금지).
4. **Integration**: `clawhub publish` 전 preflight 체크 단계로 연결.
5. **Validation**: 정상 샘플 + 의도적 누출 샘플 회귀 테스트 통과 후 운영 전환.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
