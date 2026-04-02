# observer-recovery-20260402 결과

## 목표 대비 요약
- 실제 작업용 프리셋은 새 상태 파일 생성 시 기본으로 `observer.track=true` 가 들어가도록 복구했다.
- 기존 상태 파일의 `observer.track` 가 없거나 `false` 여도, 실제 작업용 프리셋이면 관찰자가 호환 경로로 다시 집도록 복구했다.
- 데모, 테스트, 샘플 제외 정책은 그대로 유지했다.
- 테스트 오염으로 남던 비실작업 상태 파일도 정리되도록 테스트를 보강했다.

## 변경 파일
- `scripts/observer_scan.py`
- `scripts/generate_harness.py`
- `templates/harness-presets.json`
- `tests/test_observer_scan.py`
- `tests/test_observer_react.py`
- `tests/test_generate_harness.py`
- `tests/test_equal_rank_nudge_bot.py`
- `tests/test_harness_tick.py`

## 구현 내용
### 1) 새 생성 규칙 복구
실제 작업용 프리셋에 기본 추적값을 올렸다.
- `research`: `observer_track=true`
- `implementation`: `observer_track=true`
- `refactor`: `observer_track=true`
- `deploy`: `observer_track=true`
- `custom` 및 프리셋 미지정은 기존 기본값 유지 (`observer-defaults.json` 의 `track=false`)

즉, 앞으로 생성되는 실제 작업 하네스는 별도 수동 편집 없이 observer 후보에 들어간다.

### 2) 레거시 상태 파일 호환 경로 추가
`observer_scan.py` 에서 아래 규칙을 추가했다.
- `observer.enabled=false` 이면 항상 제외
- `observer.track=true` 이면 기존처럼 포함
- `observer.track` 가 없거나 `false` 여도, 실제 작업용 프리셋이면 `legacy preset 자동 추적` 으로 간주
- `--apply` 경로에서는 이 호환 판정을 상태 파일에 반영해서 `observer.track=true` 와 마이그레이션 메타데이터를 저장
  - `observer.track_migrated_at`
  - `observer.track_migration_reason=legacy preset 자동 추적`

### 3) 데모, 테스트, 샘플 제외 유지
기존 제외 규칙은 그대로 유지했다.
- `demo`
- `test`
- `sample`
- `데모`
- `테스트`
- `샘플`

### 4) 테스트 오염 방지
일부 테스트가 `tick-waiting-job`, `state-linked-nudge` 같은 비실작업 이름의 상태 파일을 남겨 실제 observer 후보를 오염시키고 있었다.
이번에 테스트 생성물 정리를 추가했고, 테스트용 잡 아이디도 `test-...` 접두로 바꿔 제외 규칙과 충돌하지 않게 정리했다.

## 판단 근거
### 왜 `observer.track=true 만 허용` 을 완전히 유지하지 않았는가
그 규칙 자체는 새 상태 파일 생성에는 유지했다. 다만 기존 상태 파일 다수가 아래 둘 중 하나였다.
- `observer.track` 없음
- `observer.track=false`

이 상태에서 새 생성 규칙만 바꾸면 과거 상태 파일은 계속 `eligible=0` 에 머문다. 그래서 이번 수정은 아래 두 층으로 나눴다.
- 앞으로는 실제 작업 프리셋이 기본으로 `track=true`
- 과거 상태 파일은 스캔 시점에 최소 호환 경로로 자동 복구

즉, 원칙은 유지하되 레거시 마이그레이션 틈만 메웠다.

### 왜 명시적 제외는 `observer.enabled=false` 로 남겼는가
레거시 상태 파일의 `track=false` 는 실제로는 명시적 거부가 아니라 예전 기본값인 경우가 많았다. 그래서 `track=false` 를 그대로 절대 제외 규칙으로 유지하면 복구가 안 된다.
이번 수정에서는 명시적 제외 스위치를 `observer.enabled=false` 로 해석해 호환성과 수동 제어 둘 다 살렸다.

## 검증 결과
### 전체 테스트
```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
- 결과: `17 tests` 통과

### 현재 저장소 실스캔 진단
```bash
python3 scripts/observer_scan.py
```
결과 요약:
- `checked: 6`
- `eligible: 0`
- 이유: 현재 남아 있는 대기 상태 파일이 모두 데모 계열이라 의도대로 제외됨

즉, 지금 워크스페이스에는 실제 대기 작업이 없어서 `eligible=0` 이고, 더 이상 `observer 가 죽어서 0` 인 상태는 아니다.

### 호환 경로 실검증
임시 실제 작업 상태 파일을 하나 만들고, 레거시 값처럼 `observer.track=false` 로 둔 뒤 스캔했다.

```bash
python3 scripts/generate_harness.py observer-live-check --preset implementation
python3 scripts/observer_scan.py
```
결과 요약:
- `eligible: 1`
- `top_job_id: observer-live-check`
- `top_track_source: legacy preset 자동 추적`

즉, 레거시 상태 파일도 실제 작업이면 다시 observer 후보로 들어간다.

### react 경로 실검증
임시 실제 작업 상태 파일을 하나 만들고 `observer.track=false` 로 둔 뒤 반응기를 실행했다.

```bash
python3 scripts/generate_harness.py observer-react-live --preset implementation
python3 scripts/observer_react.py --apply --seed 1
```
결과 요약:
- `should_act: true`
- `job_id: observer-react-live`
- 상태 파일 최종값:
  - `status: auto_execute`
  - `observer.track: true`
  - `observer.track_migration_reason: legacy preset 자동 추적`

## 수정 후 기대 동작
- 새 실제 작업 하네스는 기본으로 observer 후보가 된다.
- 과거 실제 작업 하네스도 observer_scan / observer_react 에서 다시 집힌다.
- 데모, 테스트, 샘플 작업은 계속 제외된다.
- 수동 제외가 필요하면 `observer.enabled=false` 로 막을 수 있다.

## git 커밋
- 아직 커밋하지 않음
- 이유: 작업 디렉터리에 이번 수정과 무관한 기존 변경과 미추적 파일이 함께 있어, 선택 스테이징 기준을 메인 에이전트 확인 후 하는 편이 안전함
