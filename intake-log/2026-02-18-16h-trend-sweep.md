# 2026-02-18 16:00 KST — Agent Skill Trend Sweep (비판적 흡수)

## 수집 소스 스냅샷
- **SkillsMP**: 브라우저 기준 총 **233,309 skills**. 상단 최신/노출 구간에서 `mintlify`, `imsg`, `feishu-doc` 등 확인.
- **MCP Market**: 브라우저 기준 총 **21,157 servers**. `최신 MCP 서버`에 `Java Decompiler`, `Dotnet Websearch`, `SQL Sentinel`, `OpenWrt` 등(대부분 0 usage) 확인.
- **SkillHub (skillhub.club)**: **21.3K skills / 4.8M stars**. Hot/Trending에서 `context-optimization`, `systematic-debugging`, `file-search` 등 확인.
- **ClawHub**: `/skills` 기준 **8,222 skills**. `Sort=Newest`에서 `Geepers Data`, `DeepReader`, `Audit OpenClaw Security` 등 확인.
- **VSCode Agent Skills extension**: `formulahendry.agent-skills` 기준 **1,733 installs / 5.0(1 review)**, v0.0.2(2025-12-23).

## 비판적 필터 결과
| 항목 | 판정 | 근거 |
|------|------|------|
| ClawHub `Geepers Data` | ✅ 도입 | **Q1 필요성:** Brave 검색 쿼터 제한으로 브리핑/리서치 데이터 수집이 간헐적으로 막힘. **Q2 대체성:** 현 `web_fetch`/브라우저 우회로는 가능하지만 구조화 API 묶음형 수집은 부재. **Q3 비용효과:** 저비용(패턴 흡수+내부 래퍼)으로 실패율 감소 효과 큼. **Q4 과대포장 필터:** 다운로드/별점은 낮음(5/0) → 인기지표가 아니라 ‘현재 병목 해결성’ 기준으로만 채택. |
| ClawHub `DeepReader` | ⚠️ 참고만 | **Q1:** X/Reddit/YouTube 읽기 니즈는 있음. **Q2:** `summarize`/`web_fetch`로 1차 대응 가능. **Q3:** 중복 도입 비용 대비 즉시 이득 제한. **Q4:** 초기 지표가 약해 품질 신뢰 부족. **재검토:** URL 추출 실패율이 주간 임계치 초과 시. |
| MCP Market `Task Master` | ⚠️ 참고만 | **Q1:** 작업 오케스트레이션 니즈는 존재. **Q2:** 현재 `queue-manager` + subagent 운영으로 핵심 요구 충족. **Q3:** MCP 추가 운영비 대비 단기 ROI 불명확. **Q4:** 높은 사용량은 참고 신호일 뿐 우리 적합성 증거는 아님. **재검토:** 큐 충돌/우선순위 역전이 주 3회 이상 발생 시. |
| MCP Market `Godot` MCP | ⚠️ 참고만 | **Q1:** 게임 개발 정합성은 높음. **Q2:** 현 `godot` 스킬 + MiniPC 헤드리스 파이프라인으로 대부분 해결. **Q3:** 즉시 전환 비용 대비 추가 이득 불명확. **Q4:** 노출/사용량은 품질 보증이 아님. **재검토:** 에디터 인터랙션 자동화 병목이 반복될 때. |
| SkillsMP `mintlify` | ⚠️ 참고만 | **Q1:** 문서 자동화 가치는 있음. **Q2:** 현재 마크다운+기존 docs 파이프라인으로 운영 가능. **Q3:** 지금 우선순위(수익화/QA 게이트) 대비 효과 낮음. **Q4:** 카탈로그 노출량이 품질/지속성 보장 아님. **재검토:** 대외 문서 배포 파이프라인이 실제 병목이 될 때. |
| SkillHub `context-optimization` | ⚠️ 참고만 | **Q1:** 토큰/컨텍스트 최적화 수요는 있음. **Q2:** `openclaw-mem` + 내부 메모리 규율로 핵심 기능 중복. **Q3:** 도입비 대비 즉시 개선폭 불확실. **Q4:** 대형 star 증감은 과장 가능성 있어 직접 벤치 필요. **재검토:** 컨텍스트 초과/비용 급증 지표 악화 시. |
| VSCode `formulahendry.agent-skills` 확장 | ⚠️ 참고만 | **Q1:** IDE 내 설치 편의는 있음. **Q2:** 우리 운영축은 OpenClaw CLI/서브에이전트 중심. **Q3:** VSCode 의존 도입비 대비 생산성 상승 제한. **Q4:** install 수(1.7K)와 평점 샘플(1건)만으로 품질 판단 불가. **재검토:** VSCode 중심 협업 비중이 명확히 증가할 때. |

❌ 불필요 판정: **18건**
- (요약) Molt 계열 연상 항목 포함 정책 차단 대상, 0-usage 최신 MCP 다수, 기존 스택 중복형 신규 스킬군.

## ✅ 도입 실행 계획
### 1) `data-source-fallback-bridge` (신규 내부 스킬)
1. **Research**: `Geepers Data`의 소스/엔드포인트 구조만 추출(코드 블라인드 설치 금지).
2. **Audit**: 인증/쿼터/개인정보/외부전송 리스크 점검 + 허용 도메인 화이트리스트 확정.
3. **Rewrite**: `misskim-skills/skills/data-source-fallback-bridge/`로 내부 재작성(우리 로깅/에러정책 반영).
4. **Pilot**: 브리핑/트렌드 스윕 파이프라인에 fallback으로 1주 적용, `수집 성공률·지연·재시도율` 비교.
5. **Gate**: 효과 확인 시 표준 수집 경로에 포함, 실패 시 즉시 롤백.

## 보안
- **Molt Road / molt.host / MoltHub: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → `misskim-skills/`** (blind install 금지)
