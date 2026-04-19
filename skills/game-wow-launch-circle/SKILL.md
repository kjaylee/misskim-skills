---
name: game-wow-launch-circle
description: 게임 아이디어를 검토해 와우 팩터 5개를 추가하고, 스펙→TC→구현→QA→런칭까지 한 번에 밀어붙이는 일일 게임 런칭 써클. 기존 자동 게임 파이프라인을 대체/승격할 때 사용.
---

# Game Wow Launch Circle

게임을 "하나 더 만든다"가 아니라 "하나 더 기억나게 만든다"에 맞춘 런칭 실행 스킬.

## 적용 시점
- 사용자가 게임 아이디어 검토 + 구현 + 런칭 자동화를 원할 때
- 기존 자동 게임 파이프라인이 단순 생성기 수준이라 품질 승격이 필요할 때
- 일일 게임 크론을 실제 런칭 써클로 바꿀 때

## 핵심 목표
하루 1회, 아래를 **끝까지** 수행한다.
1. 아이디어 검토
2. 와우 팩터 5개 설계
3. 스펙/테스트케이스 작성
4. 구현
5. QA
6. 런칭

완료 기준은 "아이디어 생성"이 아니라 **실제 배포 경로 반영 + 검증 증거 확보**다.

## 입력 우선순위
1. `specs/game-idea-backlog.md`
2. `specs/daily-game-lv4.md`
3. `specs/game-production-pipeline.md`
4. `MEMORY.md`의 게임 제약/금지 규칙
5. 기존 `eastsea-blog/games/`와 `eastsea-blog/games/games-list.json`

## 절대 규칙
- 리듬게임 금지
- `#0a0a1a` 네온 다크 금지
- `neon-` 접두사 금지
- 단순 "클릭+웨이브 / 클릭+방치 / 클릭+카드" 금지
- 기존 게임과 메카닉 90% 이상 중복 금지
- 가능하면 `eastsea-blog/games/`를 런칭 원본으로 사용
- git은 `eastsea-blog/`에서만 수행
- 완료 전 보고 금지

## 와우 팩터 5종 강제
매 게임마다 아래 5개를 **명시적으로 설계**하고, 적어도 3개는 실제 플레이 루프에 구현한다.

1. **입력 훅**
   - 첫 10초 안에 "이 게임 조작감 다르네"가 느껴지는 입력/판정 차별점
2. **에스컬레이션 훅**
   - 30~90초 구간에서 난이도/리듬/패턴이 살아나는 상승 구조
3. **선택 훅**
   - 플레이 중 최소 1회 이상 의미 있는 선택(업그레이드, 분기, 리스크/보상)
4. **쇼오프 훅**
   - 스크린샷/GIF/점수 자랑이 쉬운 순간 연출
5. **리텐션 훅**
   - 재도전 이유가 생기는 목표(미션, 랭크, 데일리 변형, 잠금 해제 등)

## 와우 팩터 평가 기준
각 항목을 한 줄 감탄사가 아니라 아래 형식으로 쓴다.

```md
## Wow Factors
1. 이름
   - 왜 강한가:
   - 실제 구현 표면:
   - 리텐션/공유 효과:
```

## 실행 단계

### Phase 0 — 후보 선정
1. `specs/game-idea-backlog.md`에서 `🔍 검토중` 우선 탐색
2. 없으면 `💡 신규` 또는 장르 로테이션 기반 신규안 생성
3. 아래 기준으로 1개 선택
   - 기존 게임과 차별성
   - 1일 구현 가능성
   - 모바일 조작성
   - 쇼오프 가능성
   - 수익화/확장 여지
4. 선택 결과를 `specs/games/<slug>/spec.md` 상단에 기록

### Phase 1 — 스펙 작성
반드시 아래를 포함한다.
- 게임 한 줄 정의
- 핵심 메카닉
- 보조 시스템
- 게임 루프
- 와우 팩터 5개
- 금지 규칙 검토 결과
- 런칭 경로

### Phase 2 — 테스트케이스 작성
최소 아래를 포함한다.
- 타이틀 화면
- 시작 → 플레이 진입
- 핵심 메카닉 반응
- 와우 팩터 관련 TC 최소 3개
- 게임오버/재시작
- 모바일 390x844
- localStorage
- JS pageerror 0개

### Phase 3 — 구현
원칙:
- 작은 슬라이스로 구현
- 와우 팩터 5개 중 최소 3개는 실제 코드에 반영
- 나머지 2개는 최소한 UI/메타/런칭 훅으로 반영
- 게임 파일은 `eastsea-blog/games/<slug>/index.html`
- 리스트 반영은 `eastsea-blog/games/games-list.json`

### Phase 4 — QA
필수 검증:
- 파일 생성 확인
- 게임 진입 가능
- 조작 가능
- 와우 팩터 3개 이상 실제 동작 확인
- `undefined` 텍스트 0
- JS pageerror 0
- 모바일 뷰포트 확인
- 점수/결과/재시작 확인

가능하면 MiniPC/브라우저 검증을 우선하되, 불가하면 로컬 정적 검증 + 스모크 테스트 흔적을 남긴다.

### Phase 5 — 런칭
런칭은 아래를 모두 해야 한다.
1. `eastsea-blog/games/<slug>/index.html` 반영
2. `eastsea-blog/games/games-list.json` 반영
3. 필요 시 OG/설명 문구 보강
4. `git -C /Users/kjaylee/.openclaw/workspace/eastsea-blog add ...`
5. `git commit`
6. `git push`

현재 워크트리에 unrelated dirty change가 있어도, **해당 게임 경로와 리스트 파일만 pathspec으로 커밋**한다.

## 서브에이전트 사용 규칙
구현이 길어지면 서브에이전트를 써도 된다. 단, 스폰 지시서에 반드시 아래를 넣는다.
- 현재 상태
- 테스트/검증 기준
- 완료 조건
- 산출물 경로

메인은 최종 검증과 런칭만 닫는다.

## 상태 기록
매 실행마다 아래 파일을 남긴다.
- `.state/pipelines/game-wow-launch-YYYYMMDD.json`

필수 필드:
- job_id
- selected_slug
- selected_title
- wow_factors
- status
- test_commands
- completion_criteria
- artifacts
- launch_commit
- launch_url
- risks

## 최종 보고 형식
최종 보고는 짧게, 그러나 아래는 반드시 포함한다.
- 선택한 게임
- 추가한 와우 팩터 5개 요약
- 실제 구현된 와우 팩터 수
- 검증 결과
- 런칭 경로/커밋
- 남은 위험 1줄

## 실패 처리
아래 중 하나면 즉시 중단/보류한다.
- 기존 게임과 중복도가 너무 높음
- 구현 복잡도가 1일 범위를 명백히 초과
- QA 실패를 2회 이상 반복
- 런칭 pathspec이 dirty state와 충돌

이 경우에는 억지 런칭하지 말고:
- 스펙/TC/중단 사유까지 남기고
- 다음 후보로 넘어가거나
- 해당 실행을 `보류`로 종료한다.

## 권장 크론 프롬프트
```text
Read and follow:
/Users/kjaylee/.openclaw/workspace/misskim-skills/skills/game-wow-launch-circle/SKILL.md

Today, run one full cycle only.
Do not stop at idea generation.
Do not report before launch verification.
Use eastsea-blog as the launch repo.
```