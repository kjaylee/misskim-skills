# 2026-02-16 20:00 KST — Agent Skill Trend Sweep (Critical Absorption)

## Snapshot (Sources)
- **SkillsMP:** 메인 접근 403(Cloudflare), `sitemap.xml`만 정상 접근(총 684 URLs, 카테고리 63개 확인).
- **MCP Market (`mcpmarket.com`):** 전 경로 `x-vercel-mitigated: deny`로 403, 최신 피드 직접 수집 실패.
- **SkillHub.club:** 홈 메타 기준 `21.3K Skills / 2.4M Stars`. `AI Video Ad Generator` 스택 페이지에서 구성요소(스크립트/TTS/음악/렌더/후처리) 유지 확인.
- **ClawHub:** `clawhub.com → clawhub.ai` 리다이렉트 후 `Recv failure: Connection reset by peer`. CLI `clawhub search`도 fetch 실패.
- **VSCode Agent Skills ecosystem:** Marketplace API 쿼리 `agent skills` 총 **1,203 results**.  
  - `AutomataLabs.copilot-mcp`: **80,542 installs**, lastUpdated `2026-02-16T05:31:22Z`  
  - `formulahendry.agent-skills`: **1,702 installs**, lastUpdated `2025-12-26T02:13:18Z`

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|---|---|---|
| SkillHub `AI Video Ad Generator` stack | ✅ 도입 | **필요성:** 게임/툴 유입용 숏폼 영상 자동화 공백이 여전히 실존. **기존 대체 한계:** 현재 파이프라인은 카피/이미지/배포가 분절되어 end-to-end 영상 생성 부재. **비용/효과:** 구현비용 중간이지만 반복 마케팅 산출물 자동화 ROI 높음. **과대포장 필터:** 단순 홍보 문구가 아니라 ElevenLabs/Suno/Remotion/FFmpeg 단위로 검증 가능한 구조. |
| VSCode `Copilot MCP + Agent Skills Manager` (AutomataLabs) | ⚠️ 참고만 | **필요성:** 설치수/업데이트는 강한 신호. **기존 대체 한계:** 현재 운영 중심은 OpenClaw 오케스트레이션이라 VSCode 종속 이득이 제한적. **비용/효과:** 도입·교육·운영비 대비 즉시 생산성 상승 불확실. **과대포장 필터:** install 수는 품질 보증이 아님(운영 맥락 부적합). **재검토:** VSCode 팀 온보딩 표준화 시작 시. |
| VSCode `Agent Skills` (formulahendry) | ⚠️ 참고만 | **필요성:** 멀티 리포 소스 연결은 유용. **기존 대체 한계:** 현재는 OpenClaw 내부 스킬 배포로 대체 가능. **비용/효과:** 업데이트 정체(2025-12-26)로 유지 리스크 대비 이득 제한. **과대포장 필터:** 설치수 1.7K는 도입 근거로 약함. **재검토:** IDE 기반 배포 채널을 공식 확대할 때. |
| SkillsMP 피드 접근성 (403) | ⚠️ 참고만 | **필요성:** 대형 디렉터리라 관측 가치 높음. **기존 대체 한계:** 현재는 sitemap 수준 메타만 수집 가능해 품질 판정 불가. **비용/효과:** 우회 시도 비용 대비 신뢰도 낮음. **과대포장 필터:** 규모 수치(대량 등록)만으로 품질 판단 금지. **재검토:** 정상 recent/API 접근 복구 시. |
| MCP Market 피드 접근성 (403 deny) | ⚠️ 참고만 | **필요성:** MCP 신규 서버 탐지 채널로 중요. **기존 대체 한계:** 이번 회차는 원천 차단으로 실데이터 부재. **비용/효과:** 차단 상태에서 무리한 수집은 효율 낮음. **과대포장 필터:** 이전 캐시 재인용만으로 신규 도입 판단 금지. **재검토:** 차단 해제 후 latest 서버 재평가. |
| ClawHub 피드 접근성 (connection reset) | ⚠️ 참고만 | **필요성:** 생태계 동향 확인 채널. **기존 대체 한계:** 접속 실패로 신규 검증 불가. **비용/효과:** 복구 전 도입 검토 가치 낮음. **과대포장 필터:** 보안 이력 고려 시 가용성 회복 전엔 신뢰 불가. **재검토:** 연결 복구 후에도 Research→Audit→Rewrite 경로에서만 검토. |

**❌ 불필요 판정: 9건**
(저설치 VSCode 래퍼, 기능 중복 메타 스킬, 운영 맥락 불일치 항목은 개별 나열 생략)

## ✅ Execution Plan (도입 항목만)
1. **Research (즉시)**
   - `AI Video Ad Generator` 구성요소를 내부 모듈 단위로 분해: script planner → voiceover → BGM → render → post.
2. **Audit (즉시)**
   - 외부 API(특히 TTS/음원) 라이선스·요금·민감정보 전달 경로 점검.
3. **Rewrite (다음 실행 창)**
   - 외부 스택 직접 설치 없이 `misskim-skills/skills/game-video-ad-pipeline/` 내부형 스킬로 흡수.
4. **Exit Criteria**
   - 15~30초 광고 영상 1개 자동 생성 성공 + 민감정보 노출 0건 + 재실행 재현성 확보.

## Security Notes
- **Molt Road / molt.host: ABSOLUTE BLOCK 유지**
- 외부 스킬 원칙 고정: **Research → Audit → Rewrite → misskim-skills/** (No blind installs)
