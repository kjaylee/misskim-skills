# observer-harness-boost-20260402 결과

## 변경 내용
- `scripts/generate_harness.ts`
  - `spawn-ready.md` 와 함께 `spawn-ready.json` 도 생성하도록 확장했다.
  - 상태 파일에 `spawn_ready_json_path` 와 `action_plan` 을 기록하도록 바꿨다.
  - 관찰자 기본 힌트에 `track`, `priority`, `action_kind`, `runtime_hint`, `session_hint` 를 포함하도록 확장했다.
  - 프리셋이 `research|implementation|refactor|deploy` 인 경우 `observer.action_kind` 와 기본 실행 힌트를 프리셋에 맞춰 채우도록 정리했다.
- `scripts/_observer_tooling.ts`
  - `action_kind`, `runtime_hint`, `session_hint` 파서와 기본값 계산 로직을 추가했다.
  - 상태 파일에서 바로 `action_plan` 을 조립하는 공통 함수를 추가했다.
  - 추천 실행 문자열 `recommendedCommand` 를 생성하도록 공통화했다.
- `scripts/observer_scan.ts`
  - 선택 후보와 결과 항목에 `action_plan` 을 포함하도록 확장했다.
  - 스캔 시 관찰자 힌트를 정규화해서 `action_plan` 과 우선순위 계산에 함께 쓰도록 바꿨다.
  - 상태 평가 호출을 타입스크립트 구현 기준에 맞춰 정리했다.
- `scripts/observer_react.ts`
  - 자동 실행 승격 결과에 `action_plan`, `spawn_ready_json_path` 를 함께 반환하도록 확장했다.
  - 단일 상태 파일 반응에서도 구조화된 후속 액션 계획을 항상 돌려주도록 바꿨다.
- `config/observer-defaults.json`
  - 기본 관찰자 힌트에 `action_kind: implementation`, `runtime_hint: subagent`, `session_hint: isolated` 를 추가했다.
- `templates/harness-presets.json`
  - 모든 프리셋 산출물 목록에 `spawn-ready.json` 을 추가했다.
- 테스트 갱신
  - `tests/test_generate_harness.test.ts`
  - `tests/test_observer_scan.test.ts`
  - `tests/test_observer_react.test.ts`
  - 생성 산출물, 관찰자 힌트, `action_plan`, 추천 실행 문자열을 함께 검증하도록 보강했다.

## 실행 예
### 하네스 생성
```bash
bun run generate-harness observer-harness-boost-manual-1775107427 --preset implementation
```

생성 결과 요약
```json
{
  "job_id": "observer-harness-boost-manual-1775107427",
  "spawn_ready": "specs/observer-harness-boost-manual-1775107427/spawn-ready.md",
  "spawn_ready_json": "specs/observer-harness-boost-manual-1775107427/spawn-ready.json",
  "state": ".state/pipelines/observer-harness-boost-manual-1775107427.json"
}
```

생성된 `spawn-ready.json` 핵심 예시
```json
{
  "observer": {
    "track": false,
    "priority": 0,
    "action_kind": "implementation",
    "runtime_hint": "subagent",
    "session_hint": "isolated"
  },
  "action_plan": {
    "actionKind": "implementation",
    "runtimeHint": "subagent",
    "sessionHint": "isolated",
    "spawnReadyPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.md",
    "spawnReadyJsonPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.json",
    "recommendedCommand": "cd '/private/tmp/observer-ts-bun-migration' && codex exec --full-auto \"$(cat 'specs/observer-harness-boost-manual-1775107427/spawn-ready.md')\""
  }
}
```

### 관찰자 스캔
수동 검증에서는 생성 직후 상태 파일에 아래 값만 추가로 넣고 확인했다.
- `observer.track = true`
- `observer.priority = 7`
- `created_at = 2026-04-02T00:00:00+00:00`

```bash
bun run observer-scan --seed 1
```

관찰된 결과 예시
```json
{
  "job_id": "observer-harness-boost-manual-1775107427",
  "priority": 7,
  "observer_track": true,
  "should_nudge": true,
  "action_plan": {
    "actionKind": "implementation",
    "runtimeHint": "subagent",
    "sessionHint": "isolated",
    "spawnReadyPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.md",
    "spawnReadyJsonPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.json"
  }
}
```

### 관찰자 반응
```bash
bun run observer-react --state-file .state/pipelines/observer-harness-boost-manual-1775107427.json --minutes-since-reply 10 --apply --seed 1
```

관찰된 결과 예시
```json
{
  "should_act": true,
  "job_id": "observer-harness-boost-manual-1775107427",
  "spawn_ready_path": "specs/observer-harness-boost-manual-1775107427/spawn-ready.md",
  "spawn_ready_json_path": "specs/observer-harness-boost-manual-1775107427/spawn-ready.json",
  "action_plan": {
    "actionKind": "implementation",
    "runtimeHint": "subagent",
    "sessionHint": "isolated",
    "spawnReadyPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.md",
    "spawnReadyJsonPath": "specs/observer-harness-boost-manual-1775107427/spawn-ready.json"
  }
}
```

## 테스트 결과
### 자동 테스트
```bash
bun test
```
- 결과: 13 pass, 0 fail

### 완료 기준 점검
- `spawn-ready.json` 생성: 통과
- 상태 파일 `observer` 기본 힌트 기록: 통과
- `observer-scan` 결과에 `action_plan` 포함: 통과
- `observer-react` 결과에 `action_plan` 포함: 통과
- `bun test` 통과: 통과
- `results.md` 작성: 통과

## 메모
- 이번 변경은 타입스크립트와 번 실행 경로만 확장했고, 파이썬 경로 추가는 하지 않았다.
- 수동 검증용 임시 산출물은 확인 후 정리했다.
