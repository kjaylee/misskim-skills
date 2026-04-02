# autonomous-demo 스폰 지시문

## 현재 상태
초기 생성

## 작업 목표
배포 작업 수행

## 범위
배포 전 점검, 배포 실행, 배포 후 검증

## 테스트 또는 검증 기준
배포 전 체크리스트와 배포 후 헬스 확인

## 완료 조건
배포 결과와 검증 로그가 기록된다

## 산출물 경로
specs/autonomous-demo/plan.md, specs/autonomous-demo/spawn.md, .state/pipelines/autonomous-demo.json, specs/autonomous-demo/verify.md

## 금지 사항
검증 없는 배포 완료 보고 금지, 파괴적 변경 은폐 금지

## 실행 원칙
- 묻지 말고 범위 안에서 먼저 실행
- 범위 밖 변경 금지
- 테스트와 검증 증거 없이 완료 보고 금지

## 레드팀
- 공격 하나: 배포 범위가 퍼질 수 있음
- 공격 둘: 검증 없는 완료 보고 위험
- 방어: 배포 후 확인 항목을 문서와 상태 파일에 고정
- 합의: 위험 수용

## 최종 보고 형식
- 완료한 일
- 검증 결과
- 남은 위험

