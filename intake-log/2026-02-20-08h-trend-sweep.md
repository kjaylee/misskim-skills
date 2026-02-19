# 2026-02-20 08:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: `239,658` skills, 평균 `1,762.2`, 피크 `19,898 (@ Feb 4, 2026)` 확인. Security 카테고리 `5,913` 스킬.
- **MCP Market**: `Vercel Security Checkpoint (429)`로 본회차 직접 수집 실패.
- **MCP 대체 소스(mcp.so)**: `17,764 MCP servers` 카탈로그 확인(차선 데이터).
- **SkillHub (skillhub.club)**: `21.6K Skills / 4.0M Stars`, Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub**: non-suspicious 상위 유지(`tavily-search` 23.3k/73), newest 샘플은 다수 `0 current installs`.
- **VSCode Agent Skills**: `copilot-mcp` 81k installs (4.3/5, 8), `formulahendry.agent-skills` 1.8k installs (5.0/5, 1, last updated Dec 2025).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillsMP `security-scan` 패턴 (affaan 계열) | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake에서 `.claude/settings/MCP` 설정 보안 점검 자동화 공백이 여전히 존재. **Q2 대체성:** 기존 `agent-config-lint-gate` 설계는 구조 lint 중심이라 보안 시그니처 룰셋이 부족. **Q3 비용효과:** 외부 코드 설치 없이 체크리스트/시그니처만 내부 룰로 흡수 가능(저비용·고효과). **Q4 과대포장:** 노출 수치(47.6k)는 다국어 미러로 부풀림 가능성 있어 ‘패턴만 흡수’로 제한. |
| ClawHub `counterclaw-core` | ⚠️ 참고만 | **Q1:** prompt injection/PII 방어 니즈는 맞음. **Q2:** 이미 추진 중인 `outbound-dlp-gate`/`credential-leak-gate`와 핵심 기능 중복. **Q3:** 현재 지표가 약함(8 downloads, 0 current installs) + 기본 admin 동작 리스크 안내 존재. **Q4:** 마케팅보다 초기 실험 단계로 보임. **재검토:** 내부 게이트 오탐/누락이 주간 임계치 초과 시. |
| ClawHub `sentry-issues` | ⚠️ 참고만 | **Q1:** 장애 분석 자동화 니즈는 유효. **Q2:** 현재는 Sentry 표준 도입이 선행되지 않아 즉시효용 제한. **Q3:** 토큰/프로젝트 운영비 + 계정 관리 비용 발생. **Q4:** 시장 과대포장 이슈보다는 단일 툴 의존 리스크. **재검토:** Sentry를 배포 기본 모니터링으로 채택할 때. |
| mcp.so `EdgeOne Pages MCP` (MCP Market 차선 관찰) | ⚠️ 참고만 | **Q1:** 즉시 배포 수요는 존재. **Q2:** 현재 GitHub Pages 파이프라인이 실운영 중이라 급한 대체 필요성 낮음. **Q3:** 플랫폼 추가는 운영표면/권한 관리 비용 증가. **Q4:** 노출 빈도는 높지만 우리 병목 직접 해결 근거는 약함. **재검토:** GitHub Pages 배포 실패가 주 2회 이상 반복될 때. |
| SkillHub `context-optimization` | ⚠️ 참고만 | **Q1:** 컨텍스트 최적화 문제는 존재. **Q2:** `openclaw-mem` + 내부 컨텍스트 절감 규율과 중복. **Q3:** 개념 문서형 스킬이라 즉시 실행 ROI 낮음. **Q4:** star 신호 대비 실사용 검증 데이터 부족. **재검토:** 토큰비/지연 지표가 2주 연속 악화 시. |
| VSCode `AutomataLabs.copilot-mcp` | ⚠️ 참고만 | **Q1:** 설치수(81k)로 생태계 신호는 강함. **Q2:** 운영축이 OpenClaw CLI라 IDE 확장 도입 이점 제한. **Q3:** IDE 종속 도입비(운영절차 변경) 큼. **Q4:** 설치수는 품질 보증이 아님(리뷰 8). **재검토:** VSCode 중심 협업 비중이 과반을 넘을 때. |
| VSCode `formulahendry.agent-skills` | ⚠️ 참고만 | **Q1:** 멀티 레포 탐색 기능은 유용. **Q2:** 현재 ClawHub/SkillHub + 내부 리라이트 루프로 대응 가능. **Q3:** 업데이트 정체(2025-12)로 유지보수 리스크. **Q4:** 평점 표본 1개는 신뢰도 낮음. **재검토:** 내부 탐색 리드타임이 주간 기준 악화될 때. |

**❌ 불필요 판정: 26건**
- 저신뢰 신규군(설치 0), 기존 보유 기능 중복군, 운영축 비정합 항목 제외.

## ✅ 도입 실행 계획
### `agent-config-security-scan-lite` (내부 룰팩 강화)
1. **Research**: SkillsMP `security-scan/security-review` 계열에서 점검 축(설정 파일, MCP 서버 선언, 훅, 민감 env, 주입 패턴)만 추출.
2. **Audit**: 위험 시그니처를 `high/medium/low`로 분리하고 오탐 방지 예외 규칙 설계.
3. **Rewrite**: 외부 코드 무복사 원칙으로 `misskim-skills/skills/agent-config-security-scan-lite/` 작성.
4. **Integration**: 외부 스킬 intake 파이프라인의 사전 게이트로 연결(Research → Audit → Rewrite 정책 고정).
5. **Validation**: 최근 intake 샘플 재검증(탐지율/오탐율) 후 임계치 충족 시 상시 적용.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)
- MCP Market 본회차 체크포인트 차단으로 직접 수집 실패: 다음 회차도 동일하면 MiniPC browser.proxy 재시도 후, 실패 시 web_fetch 차선 유지
