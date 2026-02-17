# 2026-02-17 16:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## 수집 소스 스냅샷
- **SkillsMP**: 227,170 skills, recent 상단이 `ahaodev/heji` Android 분해형 스킬(2/17) 중심.
- **MCP Market**: 21,091 servers(약 1시간 전 업데이트), latest 섹션에 `ShellCheck`, `Dolex`, `K-Trendz`, `Appwrite`, `Mem0` 노출.
- **SkillHub**: Hot leaderboard 570 skills, 6시간 주기 업데이트.
- **ClawHub**: `clawhub explore` 최신 항목에 `paypal`, `dependency-auditor`, `bitwarden-secrets` 등 확인.
- **VSCode Agent Skills extension**: 
  - `AutomataLabs.copilot-mcp` 80,690 installs, 최신 버전 0.0.91(월요일 업데이트)
  - `formulahendry.agent-skills` 1,714 installs, 최신 버전 0.0.2(2025-12-26)

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| MCP Market `ShellCheck` MCP | ✅ 도입 | (1) 필요성: 쉘 스크립트 품질 게이트 공백 존재. (2) 기존대체: 수동 리뷰/기존 lint 루틴으로는 누락 빈도 높음. (3) 비용대비효과: 도입비용 낮고 회귀 방지 ROI 큼. (4) 과대포장검증: GitHub star 0이지만 문제-해결 정합성이 명확해 "패턴만" 흡수 가치 있음. |
| ClawHub `paypal` | ✅ 도입 | (1) 필요성: 직접결제 퍼널 강화(현재 우선순위 1)와 정합. (2) 기존대체: 현재 스킬 셋에 결제 webhook 검증/구독 흐름 템플릿 부재. (3) 비용대비효과: 결제 경로 구축 시 수익화 레버리지 큼. (4) 과대포장검증: 신생(2026-02-17)이라 신뢰 낮아 원본 미설치, 내부 재작성 전제. |
| ClawHub `dependency-auditor` | ⚠️ 참고만 | 멀티언어 의존성 감사는 유용하나, 현재 `healthcheck`/기존 검증 루프와 일부 중복. **재검토 조건:** 의존성 이슈 재발(주 2회 이상) 또는 보안 사고 징후 발생 시. |
| SkillHub `audit-website` | ⚠️ 참고만 | SEO/기술 감사 기능은 매력적이나 `web-design-guidelines` + 내부 QA 루틴으로 1차 대응 가능. **재검토 조건:** organic 유입 2주 연속 하락 또는 대량 랜딩페이지 운영 시작 시. |
| VSCode `Copilot MCP + Agent Skills Manager` | ⚠️ 참고만 | 설치 신호(80.7K)는 강하지만 VSCode UI 중심 도구로 현재 OpenClaw CLI 중심 운영과 불일치. **재검토 조건:** 팀 표준 IDE를 VSCode로 일원화할 때. |
| SkillsMP recent Android cluster (`android-testing`, `android-architecture` 등) | ⚠️ 참고만 | 품질 높은 Android 템플릿이지만 현재 핵심 파이프라인(웹게임/도구/배포)과 직접 연관 약함. **재검토 조건:** Android 네이티브 앱 라인 본격 착수 시. |
| MCP Market `Mem0` | ⚠️ 참고만 | 메모리 인프라 가치 있으나 `openclaw-mem` 실전 검증 중으로 기능 중복 위험 큼. **재검토 조건:** 회상 정확도 지표 악화 또는 openclaw-mem 검증 실패 시. |

❌ 불필요 판정: **12건**
- (목록 비공개 원칙 적용) 과대포장/중복/우선순위 미스매치 항목은 제외.

## ✅ 도입 실행 계획 (구체)
### 1) `ShellCheck` 패턴 내부화
1. Research: `ev3lynx727/mcp-shellcheck` 동작/입출력 확인.
2. Audit: 임의 실행/권한 요구/외부 통신 여부 점검.
3. Rewrite: `misskim-skills/skills/shell-script-guard/` 내부 스킬로 재작성.
4. 검증: `scripts/*.sh` 샘플 10개에 lint 적용, false-positive 기록.
5. 적용: 배치/배포 스크립트 preflight 체크에 연결.

### 2) `PayPal` 결제 스킬 패턴 내부화
1. Research: 원본 스킬 + PayPal 공식 webhook 검증 플로우 정리.
2. Audit: 서명검증/재전송 방지/비밀키 저장경로 점검.
3. Rewrite: `misskim-skills/skills/payments-paypal-funnel/` 신규 생성.
4. 검증: sandbox에서 단건 결제 + webhook 왕복 테스트.
5. 적용: 게임/툴 랜딩 결제 CTA 1개에 파일럿 연결.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`**
- Blind install 금지 유지
