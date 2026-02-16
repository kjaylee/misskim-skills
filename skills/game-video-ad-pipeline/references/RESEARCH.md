# Research — Game Video Ad Generator

작성일: 2026-02-16 (KST)
패턴: Research → Audit → Rewrite (1단계)

> 참고: `web_search`는 Brave quota 초과(429)로 직접 사용 불가였고, 공식 문서/원문 URL 직접 fetch로 대체 조사함.

---

## 1) 무료/오픈소스 비디오 생성 도구 조사

## FFmpeg (기본)
- 강점
  - CLI/서버 자동화 표준, 의존성 최소, 속도/이식성 우수.
  - drawtext, scale/crop, concat 등 광고 숏폼 생성에 필요한 기본 기능 충분.
- 약점
  - 템플릿/장면 로직을 직접 스크립팅해야 함.
- 출처
  - https://ffmpeg.org/legal.html

## Remotion (MiniPC 설치됨)
- 강점
  - 코드 기반 템플릿화/재사용성 강함(장면 컴포넌트화).
  - 복잡한 모션/브랜딩 영상 제작에 유리.
- 약점
  - Node/React 스택 필요, 렌더링 파이프라인 복잡도 증가.
  - 라이선스 정책(회사 규모별 조건) 확인 필요.
- 출처
  - https://www.remotion.dev/docs/cli
  - https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md
  - https://www.remotion.dev/docs/licensing

## MoviePy (Python)
- 강점
  - Python 생태계와 결합 쉬움.
  - ffmpeg 래퍼로 빠른 프로토타이핑 용이.
- 약점
  - 결국 ffmpeg 의존, 고성능 대량 처리 시 직접 ffmpeg보다 비효율 가능.
- 출처
  - https://raw.githubusercontent.com/Zulko/moviepy/master/LICENCE.txt

## 기타 CLI 기반 오픈소스
- Shotcut (GUI 중심이지만 오픈소스 편집기)
  - FFmpeg 기반 포맷 지원 폭 넓음.
  - 출처: https://shotcut.org/, https://raw.githubusercontent.com/mltframework/shotcut/master/COPYING
- Kdenlive (GUI 중심)
  - FFmpeg/MLT 기반, 효과 체인/타이틀 기능 풍부.
  - 출처: https://kdenlive.org/features/, https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING
- MLT Framework
  - 비선형 편집 파운데이션, CLI 조합 가능.
  - 출처: https://raw.githubusercontent.com/mltframework/mlt/master/COPYING

---

## 2) 경쟁 스킬/도구 조사 (clawhub, SkillHub)

## ClawHub 생태계 관찰
- `clawvid` (OpenClaw 영상 생성 스킬)
  - 강점: TTS-기반 타이밍, Remotion 조합, 멀티 플랫폼 출력.
  - 한계: fal.ai 유료 API 의존(우리 목표 $0와 충돌).
  - 출처: https://raw.githubusercontent.com/neur0map/clawvid/main/README.md

- `deapi-clawdbot-skill`
  - 강점: 다양한 미디어 기능 통합.
  - 한계: 외부 API 비용 발생, 데이터 외부 전송.
  - 출처: https://raw.githubusercontent.com/zrewolwerowanykaloryfer/deapi-clawdbot-skill/main/README.md

- `openclaw-skill-suite` / `remotion-product-demos`
  - 강점: SKILL.md 중심 구조, 템플릿/레퍼런스 분리, 문서화 품질 높음.
  - 적용 포인트: 우리 스킬도 문서+스크립트+테스트 리포트 구조 채택.
  - 출처:
    - https://raw.githubusercontent.com/unisone/openclaw-skill-suite/main/README.md
    - https://raw.githubusercontent.com/unisone/openclaw-skill-suite/main/skills/remotion-product-demos/SKILL.md

## SkillHub 키워드 조사
- `skillhub.com`: 프리랜서 콘텐츠 플랫폼(에이전트 스킬 허브와 성격 다름)
- `skillhub.ai`: Coming soon
- 결론: 본 과제 맥락의 “AI agent skill marketplace” 비교 소스로는 ClawHub 쪽이 유효.
- 출처:
  - https://skillhub.com
  - https://skillhub.ai

---

## 3) 비판적 흡수 4질문 적용

1. 무엇을 흡수할 것인가?
- ClawHub 계열의 **템플릿 중심 워크플로우**와 **명확한 SKILL.md 구조**.
- Remotion/영상 스킬의 **장면 분리 사고방식**.

2. 무엇을 버릴 것인가?
- 유료 API(fal.ai, deapi 등) 의존.
- 키 관리/원격 호출/과금 추적이 필요한 아키텍처.

3. 어떻게 재작성할 것인가?
- 단일 Python 스크립트 + ffmpeg subprocess로 파이프라인 단순화.
- game id 기반 스크린샷 수집은 Steam 페이지 HTML 파싱(무키/무료).

4. 성공 기준은 무엇인가?
- 15~30초 MP4 생성 성공
- 1080x1920 또는 1920x1080 규격 준수
- 텍스트 오버레이 + 템플릿 선택 가능
- MiniPC/로컬에서 동일 실행 가능
- 비용 $0
