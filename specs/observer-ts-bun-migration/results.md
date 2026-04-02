# observer-ts-bun-migration

## 한 일

- `package.json`, `tsconfig.json`을 추가해서 관찰자와 하네스 도구를 `bun run`과 `bun test` 기준으로 실행할 수 있게 정리했다.
- 아래 다섯 개 파이썬 스크립트와 동일한 기본 동작 경로를 타입스크립트로 추가했다.
  - `scripts/generate_harness.ts`
  - `scripts/equal_rank_nudge_bot.ts`
  - `scripts/harness_tick.ts`
  - `scripts/observer_scan.ts`
  - `scripts/observer_react.ts`
- 공통 로직은 `scripts/_observer_tooling.ts`로 묶어서 중복을 줄였다.
- 테스트를 `bun:test` 기준으로 이식했다.
  - `tests/test_generate_harness.test.ts`
  - `tests/test_equal_rank_nudge_bot.test.ts`
  - `tests/test_harness_tick.test.ts`
  - `tests/test_observer_scan.test.ts`
  - `tests/test_observer_react.test.ts`
- 기존 파이썬 스크립트는 삭제하지 않고 각 파일 상단에 deprecated 안내를 추가했다.

## 대체 경로

### 스크립트
- `scripts/generate_harness.py` -> `scripts/generate_harness.ts`
- `scripts/equal_rank_nudge_bot.py` -> `scripts/equal_rank_nudge_bot.ts`
- `scripts/harness_tick.py` -> `scripts/harness_tick.ts`
- `scripts/observer_scan.py` -> `scripts/observer_scan.ts`
- `scripts/observer_react.py` -> `scripts/observer_react.ts`

### 테스트
- `tests/test_generate_harness.py` -> `tests/test_generate_harness.test.ts`
- `tests/test_equal_rank_nudge_bot.py` -> `tests/test_equal_rank_nudge_bot.test.ts`
- `tests/test_harness_tick.py` -> `tests/test_harness_tick.test.ts`
- `tests/test_observer_scan.py` -> `tests/test_observer_scan.test.ts`
- `tests/test_observer_react.py` -> `tests/test_observer_react.test.ts`

## 실행 예

```bash
bun run generate-harness observer-ts-bun-demo --preset implementation
bun run observer-scan --seed 1
bun run observer-react --state-file "$PWD/.state/pipelines/observer-ts-bun-demo.json" --minutes-since-reply 10 --apply --seed 1
bun test tests/*.test.ts
```

## 검증 기록

### 자동 테스트

```bash
bun test tests/*.test.ts
```

결과:
- 13 pass
- 0 fail

### 수동 실행 확인

`generate_harness.ts` 실행으로 아래 산출물이 실제 생성되는 것을 확인했다.
- `specs/<job_id>/plan.md`
- `specs/<job_id>/spawn.md`
- `specs/<job_id>/spawn-ready.md`
- `.state/pipelines/<job_id>.json`

수동 검증 시나리오:
- `generate_harness.ts`로 상태 파일 생성
- 상태 파일에 `observer.track=true`, `observer.priority=7` 설정
- `observer_scan.ts --seed 1` 실행
- `observer_react.ts --state-file ... --minutes-since-reply 10 --apply --seed 1` 실행
- 최종 상태가 `auto_execute`로 바뀌고 `nudge.proposal_pending=false`가 되는 것 확인

관찰된 예시 결과:
- scan: `eligible=2`, `top_job=manual-observer-ts-bun-1087`
- react: `should_act=true`, `reason=대기 상태 오 분 초과`
- state: `status=auto_execute`, `proposal_pending=false`

## 메모

- 이번 범위에서는 기존 크론이나 기존 파이프라인 구조를 제거하지 않았다.
- 새 파이썬 파일은 추가하지 않았다.
- 기본 실행 경로는 이제 타입스크립트와 번 기준으로 확보됐다.
