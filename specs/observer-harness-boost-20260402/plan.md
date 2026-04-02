# observer harness boost

## 목표
관찰자와 하네스를 실제 실행형으로 더 고도화한다.

## 범위
- spawn-ready 를 사람이 읽는 문서만이 아니라 자동 실행용 구조 데이터까지 생성
- observer 가 선택한 작업에 대해 다음 액션 계획을 구조적으로 출력
- track/priority 외에 action kind, runtime hint, session hint 를 지원
- bun test 전체 통과

## 테스트
- bun test
- generate-harness 실행 시 spawn-ready.json 생성 확인
- observer-react 실행 시 action plan 필드 포함 확인

## 완료 조건
- spawn-ready.md + spawn-ready.json 동시 생성
- observer-react 결과에 실제 후속 실행 계획 정보 포함
- 테스트 통과

## 산출물
- specs/observer-harness-boost-20260402/results.md
