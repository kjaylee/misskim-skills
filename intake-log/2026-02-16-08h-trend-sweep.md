# 2026-02-16 08:00 KST — Agent Skill Trend Sweep (SkillsMP · MCP Market · SkillHub · ClawHub · VSCode)

## Snapshot
- SkillsMP: **214,232 skills** (recent feed 상단 다수 0~1 star/저신뢰)
- MCP Market: **21,042 MCP servers**, Agent Skills Directory **48,091 skills**
- SkillHub: **21.3K skills / 1.4M stars**, Git History + Hot Rankings 노출
- ClawHub: `clawhub.com → clawhub.ai` 리다이렉트 후 TLS reset (직접 피드 수집 실패)
- VSCode Marketplace: "agent skills" 검색 **1,079 results**
- 보안: **Molt Road / molt.host ABSOLUTE BLOCK 유지** (관련 항목 도입 검토 제외)

## Critical Filter Table (✅ 도입 + ⚠️ 참고만)
| 항목 | 판정 | 근거 |
|------|------|------|
| SkillHub `AI Video Ad Generator` stack 패턴 | ✅ 도입 | **필요 문제:** 실사용 트래픽 0에 가까워 배포/마케팅 자동화 강화가 급함. **기존 대체 한계:** 현재 스킬은 콘텐츠/이미지/카피가 분절되어 있고, 광고 영상 end-to-end 파이프라인이 없음. **비용 대비 효과:** 중간 구현비용으로 반복 마케팅 산출물 자동화 기대. **과대포장 필터:** 유행어가 아니라 구성요소(스크립트/TTS/음악/렌더)와 산출물이 명확함. |
| MCP Market `Godot MCP Server` | ⚠️ 참고만 | **기존으로 충분?** 현재 `godot` 스킬 + 헤드리스 파이프라인으로 핵심 개발 가능. **재검토 조건:** 에디터 실시간 제어/디버그 자동화가 병목으로 측정될 때. |
| VSCode `Copilot MCP + Agent Skills` (AutomataLabs, 80,454 installs, 2026-02-11 업데이트) | ⚠️ 참고만 | 대규모 설치는 신호지만 현재 운영 중심은 OpenClaw 오케스트레이션. **재검토 조건:** VSCode 협업 비중이 실제로 커질 때(온보딩/팀 배포 필요). |
| VSCode `Agent Skills` (formulahendry, 1,694 installs, 2025-12-26 이후 업데이트 없음) | ⚠️ 참고만 | 기능은 유용하나 업데이트 템포가 느리고 현 워크플로우 우선순위와 불일치. **재검토 조건:** custom repo 배포 채널 확장 시. |
| SkillsMP 최신 `hs`(hardstop), `bazdmeg`류 품질게이트 스킬 | ⚠️ 참고만 | 개념은 좋지만 현재 SDD+TDD+감사 정책과 기능 중복이 큼. **재검토 조건:** 현 정책으로 실제 사고/누락이 발생할 때만. |

**❌ 불필요 판정: 18건**  
(저신뢰 지표, 기능 중복, 마케팅성 설명 대비 실사용 근거 부족 항목은 개별 나열 생략)

## ✅ 도입 실행 계획
1. **Research (오늘)**
   - `AI Video Ad Generator` 구성요소를 기능 단위로 분해 (스크립트 생성 / 보이스 / BGM / 렌더 / 후처리).
2. **Audit (오늘)**
   - 라이선스/유료 API 의존성/외부 업로드 리스크 점검.
3. **Rewrite (다음 실행)**
   - 외부 스택 직접 설치 없이 `misskim-skills/skills/game-video-ad-pipeline/` 내부형 스킬로 재작성.
4. **Exit Criteria**
   - 게임 1종 기준 15~30초 광고 영상 자동 생성 1회 성공 + 민감정보 노출 0건.

## Notes
- ClawHub는 네트워크 이슈로 이번 회차에 신규 피드 신뢰수집 실패. 다음 회차 재시도.
- 외부 항목은 계속 **Research → Audit → Rewrite → misskim-skills/** 원칙 고수.
