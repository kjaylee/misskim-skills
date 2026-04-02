# observer-upgrade-20260402 결과

## 변경 내용
- `scripts/observer_scan.py`
  - `demo`, `test`, `sample` 계열 작업을 기본 자동 반응 대상에서 제외하도록 필터를 추가했다.
  - 상태 파일의 `observer.track`, `observer.priority` 를 읽도록 확장했다.
  - 자동 반응 후보는 `observer.track=true` 일 때만 남기도록 바꿨다.
  - 후보 정렬은 `priority` 내림차순, 다음으로 `minutes_since_reply` 내림차순으로 바꿨다.
- `scripts/generate_harness.py`
  - 생성되는 상태 파일의 `observer` 기본값에 `track`, `priority` 를 포함하도록 바꿨다.
- `config/observer-defaults.json`
  - 관찰자 기본값에 `track: false`, `priority: 0` 을 추가했다.
- 테스트 보강
  - `tests/test_observer_scan.py` 에 데모 제외, `observer.track` 강제, 우선순위 정렬 테스트를 추가했다.
  - `tests/test_generate_harness.py` 에 `observer.track`, `observer.priority` 기본값 검증을 추가했다.

## 검증 결과
### 부분 검증
```bash
python3 -m unittest tests.test_generate_harness tests.test_observer_scan -v
```
- 결과: 5개 테스트 통과

### 전체 검증
```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
- 결과: 13개 테스트 통과

## 완료 기준 점검
- 관찰자가 데모 작업을 집지 않는다: 통과
- 실제 작업은 `observer.track=true` 일 때만 자동 반응 대상이 된다: 통과
- `observer.priority` 가 높으면 먼저 선택된다: 통과
- 테스트 전부 통과한다: 통과
- `results.md` 기록 완료: 통과

## 메모
- `observer_react.py --state-file ...` 경로는 직접 지정 실행용이라 이번 스캔 필터와는 별개로 유지했다.
- 범위 밖 리팩터와 기존 크론 설정 변경은 하지 않았다.
