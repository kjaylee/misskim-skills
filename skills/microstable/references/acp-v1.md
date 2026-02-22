# ACP v1 (Agent Communication Protocol) — JSON-RPC Spec

기준 문서: `microstable/docs/open-agent-economy.md` 섹션 3.

## 1) Envelope

모든 요청/응답은 JSON-RPC 2.0 형식.

```json
{
  "jsonrpc": "2.0",
  "method": "acp.submit_proposal",
  "params": {},
  "id": "uuid-or-hash"
}
```

## 2) 공통 규칙

- **서명**: 메시지별 Ed25519 signature 필수 (`params.signature`)
- **검증 키**: on-chain AgentRegistry의 agent pubkey
- **Rate Limit**: 기본 `100 msg / epoch / agent`
- **에러 포맷**:

```json
{
  "jsonrpc": "2.0",
  "error": { "code": -32000, "message": "reason" },
  "id": "same-id"
}
```

---

## 3) Methods

## 3.1 `acp.register`

에이전트 등록.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.register",
  "params": {
    "agent_id": "opt_001",
    "agent_type": "Optimizer",
    "stake": 10,
    "pubkey": "...",
    "signature": "..."
  },
  "id": "reg-1"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "Active",
    "registered_at": 42,
    "min_stake_required": 10
  },
  "id": "reg-1"
}
```

---

## 3.2 `acp.submit_proposal`

Optimization tournament proposal 제출.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.submit_proposal",
  "params": {
    "agent_id": "opt_001",
    "epoch": 42,
    "proposal": {
      "weights": [0.4, 0.3, 0.2, 0.1],
      "mint_fee": 0.002
    },
    "evidence": {
      "loss_estimate": 0.0028,
      "backtest_ticks": 1000
    },
    "signature": "..."
  },
  "id": "prop-42-opt-001"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "accepted": true,
    "commit_hash": "...",
    "submission_end_tick": 2880
  },
  "id": "prop-42-opt-001"
}
```

---

## 3.3 `acp.vote`

proposal 또는 anomaly 해결안에 대한 투표.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.vote",
  "params": {
    "agent_id": "aud_001",
    "epoch": 42,
    "target_id": "proposal-or-alert-id",
    "vote": "yes",
    "reason": "invariant_ok",
    "signature": "..."
  },
  "id": "vote-42-aud-001"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "recorded": true,
    "quorum": "2/3",
    "yes_votes": 2
  },
  "id": "vote-42-aud-001"
}
```

---

## 3.4 `acp.report_anomaly`

Watchdog anomaly 보고.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.report_anomaly",
  "params": {
    "agent_id": "mon_001",
    "alert_type": "PEG_DEVIATION",
    "epoch": 42,
    "evidence": {
      "snapshot": { "peg": 0.987 },
      "oracle": { "price": 0.988 },
      "timestamp": 42
    },
    "signature": "..."
  },
  "id": "alert-42-mon-001"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "accepted": true,
    "votes": 2,
    "required_votes": 2,
    "consensus": true
  },
  "id": "alert-42-mon-001"
}
```

---

## 3.5 `acp.claim_reward`

보상 조회/청구.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.claim_reward",
  "params": {
    "agent_id": "opt_001",
    "claim_id": "opt_001:42:1",
    "signature": "..."
  },
  "id": "claim-opt-001-42"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "claimed": true,
    "amount": 30,
    "remaining_claimable": 0
  },
  "id": "claim-opt-001-42"
}
```

---

## 3.6 `acp.query_state`

프로토콜/토너먼트 상태 조회.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.query_state",
  "params": {
    "epoch": 42,
    "include": ["peg", "cr", "weights", "circuit_breakers"]
  },
  "id": "state-42"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "peg": 0.9992,
    "cr": 1.24,
    "weights": [0.4, 0.3, 0.2, 0.1],
    "circuit_breakers": { "cb1": false, "cb2": false, "cb3": false, "cb4": false }
  },
  "id": "state-42"
}
```

---

## 3.7 `acp.heartbeat`

liveness 신호.

### Request

```json
{
  "jsonrpc": "2.0",
  "method": "acp.heartbeat",
  "params": {
    "agent_id": "opt_001",
    "epoch": 43,
    "signature": "..."
  },
  "id": "hb-opt-001-43"
}
```

### Response

```json
{
  "jsonrpc": "2.0",
  "result": {
    "alive": true,
    "last_active": 43
  },
  "id": "hb-opt-001-43"
}
```

---

## 4) Validation Notes

- `weights` 길이/합(=1) 검증 필수
- stale evidence(>10 epochs) 거절
- 최소 stake 미달 시 proposal/report 권한 제한 가능
- 서명 누락/불일치 시 즉시 거절
- rate limit 초과 시 `429` 성격의 에러 코드 사용 권장
