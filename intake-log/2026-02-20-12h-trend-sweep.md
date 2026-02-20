# 2026-02-20 12:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP (r.jina.ai 우회)**: 총 `239,658` skills, timeline 평균 `1,762.2`, 피크 `19,898 (@ 2026-02-04)`, Security 카테고리 `5,913`.
- **MCP Market**: `Vercel Security Checkpoint (429)`로 본회차 직접 수집 실패.
- **MCP 대체 소스 (mcp.so)**: `/servers` 상단에서 `edgeone-pages-mcp`, `Figma-Context-MCP`, `firecrawl-mcp-server`, `playwright-mcp` 등 확인.
- **SkillHub (skillhub.club)**: `21.6K Skills / 3.9M Stars`, Trending Today 상단 `coding-agent`, `feishu-drive`, `model-usage`, `wacli`, `slack`.
- **ClawHub CLI**: `explore --sort newest --limit 40` 기준 신규군 다수 `installsCurrent=0`; `little-snitch`(699/1), `causal-inference`(1026/0) 확인.
- **VSCode Agent Skills ecosystem (extensionquery API)**: `agent skills` 검색 총 `1,218` 결과. `AutomataLabs.copilot-mcp` `81,317 installs`(4.25/8), `formulahendry.agent-skills` `1,764 installs`(5.0/1), `gaoyuan.skills-vscode` `650 installs`.

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillsMP `security-scan` 패턴(affaan 계열) | ✅ 도입 | **Q1 필요성:** 외부 스킬 intake 시 `.claude/.github` 설정, MCP 선언, hook 기반 리스크를 자동 점검하는 실전 게이트가 아직 비어 있음. **Q2 대체성:** 기존 `healthcheck`/`verify-before-done`는 인프라/검증 중심이라 에이전트 설정 보안 시그니처를 직접 커버하지 못함. **Q3 비용효과:** 외부 코드 설치 없이 룰셋만 내부 재작성 가능(저비용). **Q4 과대포장 필터:** 47.6k 노출은 다국어 미러로 부풀림 가능성이 있어 코드 흡수 금지, 패턴만 흡수. |
| mcp.so `Figma-Context-MCP` | ⚠️ 참고만 | **Q1:** 디자인-코드 정합 이슈 해결에는 유효. **Q2:** 현재 `ui-ux-pro-max` + 코드 기반 구현 루프로 1차 대응 가능. **Q3:** Figma 토큰/권한/운영절차 추가비용 존재. **Q4:** 소개 페이지 중심 신호라 실제 운영 품질 데이터 부족. **재검토:** Figma handoff가 주간 3건 이상으로 증가할 때. |
| mcp.so `EdgeOne Pages MCP` | ⚠️ 참고만 | **Q1:** 빠른 HTML 배포 니즈는 존재. **Q2:** GitHub Pages 자동 배포가 현재 주력이며 즉시 대체 필요성 낮음. **Q3:** 플랫폼 추가 시 권한/운영표면 확대. **Q4:** 기능 소개 대비 실제 장애절감 데이터 부재. **재검토:** GitHub Pages 장애가 주 2회 이상 반복될 때. |
| ClawHub `little-snitch` | ⚠️ 참고만 | **Q1:** Mac egress 추적/방화벽 운영 니즈는 맞음. **Q2:** 현재는 Little Snitch 설치/권한 전제 부재. **Q3:** 루트 권한 포함 운영 절차 비용이 큼. **Q4:** installsCurrent 1로 품질신호 약함. **재검토:** macOS outbound 감사가 운영 KPI로 승격될 때. |
| VSCode `AutomataLabs.copilot-mcp` / `formulahendry.agent-skills` | ⚠️ 참고만 | **Q1:** 생태계 확산 신호(81k/1.7k)는 강함. **Q2:** 운영축이 OpenClaw CLI라 IDE 확장 직접 도입 이점 제한. **Q3:** IDE 의존 워크플로 도입·유지 비용 큼. **Q4:** 설치수는 운영 적합성 보증이 아님(리뷰 표본 작음). **재검토:** VSCode 중심 협업 비중이 과반을 넘을 때. |
| SkillHub `file-search` (S-rank 9.0) | ⚠️ 참고만 | **Q1:** 대규모 코드 탐색 생산성 개선 여지는 있음. **Q2:** 현재는 기존 grep/find + `systematic-debugging`으로 핵심 흐름 대응 가능. **Q3:** 도입 자체는 저비용이나 즉시 ROI 불명확. **Q4:** S-rank 점수는 참고값일 뿐 운영 KPI 대체 불가. **재검토:** 코드탐색 리드타임이 주간 임계치 초과 시. |

**❌ 불필요 판정: 21건**
- 저신뢰 신규군(installsCurrent 0 중심), 기능 중복군, 운영축 비정합 항목 제외.

## ✅ 도입 실행 계획
### `agent-config-security-scan-lite` (내부 보안 룰팩)
1. **Research:** SkillsMP `security-scan/security-review` 계열에서 설정 보안 체크 축만 추출 (`CLAUDE.md`, settings, MCP, hooks, env 노출).
2. **Audit:** 룰을 `critical/high/medium`로 분리하고 오탐 예외(허용 패턴) 정의.
3. **Rewrite:** 외부 코드 무복사 원칙으로 `misskim-skills/skills/agent-config-security-scan-lite/` 작성.
4. **Integration:** 외부 스킬 intake 단계의 preflight 게이트로 연결 (Research → Audit → Rewrite 강제).
5. **Validation:** 최근 intake 샘플 재검증 후 탐지율/오탐율 임계치 충족 시 상시 적용.

## 보안
- **Molt Road / molt.host ABSOLUTE BLOCK 유지**
- 외부 스킬은 **Research → Audit → Rewrite → `misskim-skills/`**만 허용 (blind install 금지)
- MCP Market은 이번 회차 429 고착: 다음 회차도 동일하면 MiniPC browser.proxy 재시도(attach 가능 시) 후 실패 시 web_fetch 차선 유지
