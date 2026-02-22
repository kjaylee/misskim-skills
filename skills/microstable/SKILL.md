---
name: microstable
description: Microstable protocol agent participation skill. Enables AI agents to interact with the Microstable self-evolving multi-collateral stablecoin protocol. Use when an agent needs to: (1) Monitor protocol state (peg, collateral ratios, circuit breakers), (2) Register as a protocol agent (Optimizer/Monitor/Auditor/Liquidator), (3) Submit optimization proposals via commit-reveal tournaments, (4) Report anomalies and earn rewards, (5) Participate in the Open Agent Economy. Supports both local simulation and Solana devnet.
metadata:
  author: misskim
  version: "1.0.0"
---

# Microstable Agent Participation

Microstable Open Agent Economy 참여를 위한 OpenClaw 스킬입니다.

## 포함 파일

```text
microstable/
├── SKILL.md
├── scripts/
│   └── microstable-agent.py
└── references/
    ├── acp-v1.md
    └── agent-roles.md
```

## 핵심 워크플로우

1. **상태 확인**: peg, CR, oracle, CB 신호 확인
2. **에이전트 등록**: 역할별 stake로 등록
3. **제안 제출**: epoch별 최적화 proposal 제출 (commit hash 포함)
4. **토너먼트 평가**: winner 선정 + 보상 분배
5. **이상 감지 보고**: watchdog 합의/해결
6. **보상 조회/청구 + heartbeat**: 지속 참여 관리

## CLI 빠른 시작

작업 경로:

```bash
cd $WORKSPACE/misskim-skills/skills/microstable
```

### 1) 프로토콜 상태 조회

```bash
python3 scripts/microstable-agent.py state
```

### 2) 에이전트 등록

```bash
python3 scripts/microstable-agent.py --agent-id opt_001 register Optimizer 10
python3 scripts/microstable-agent.py --agent-id mon_001 register Monitor 5
```

### 3) 최적화 제안 제출

```bash
python3 scripts/microstable-agent.py \
  --agent-id opt_001 \
  propose 42 '[0.4,0.3,0.2,0.1]'
```

또는 객체 형태:

```bash
python3 scripts/microstable-agent.py \
  --agent-id opt_001 \
  propose 42 '{"weights":[0.41,0.29,0.2,0.1],"mint_fee":0.002}'
```

### 4) 토너먼트 결과 조회/평가

```bash
python3 scripts/microstable-agent.py tournament 42
```

### 5) 이상 감지 보고

```bash
python3 scripts/microstable-agent.py \
  --agent-id mon_001 \
  report PEG_DEVIATION '{"snapshot":{"peg":0.987},"oracle":{"price":0.988},"timestamp":42}'
```

합의 즉시 해결(보상/슬래시 반영):

```bash
python3 scripts/microstable-agent.py \
  --agent-id mon_001 \
  report PEG_DEVIATION '{"snapshot":{"peg":0.987},"oracle":{"price":0.988},"timestamp":42}' \
  --resolve --is-true
```

### 6) 보상 조회/청구

```bash
python3 scripts/microstable-agent.py rewards opt_001
python3 scripts/microstable-agent.py rewards opt_001 --claim
```

### 7) heartbeat

```bash
python3 scripts/microstable-agent.py --agent-id opt_001 heartbeat --epoch 43
```

## 에이전트 등록 플로우

1. 역할 선택: `Optimizer | Monitor | Auditor | Liquidator`
2. 최소 stake 충족
3. `register <agent-type> <stake>` 실행
4. 상태 `Active` 확인

최소 stake (spec):
- Optimizer: 10
- Monitor: 5
- Auditor: 20
- Liquidator: 2

## 프로포절 제출 플로우

1. Optimizer 계정 활성 상태 확인
2. `propose <epoch> <weights-json>` 제출
3. CLI가 commit hash 생성 + reveal payload 저장
4. `tournament <epoch>`에서 평가 및 winner 결정
5. 보상은 `rewards <agent-id>`로 조회/청구

## 모드

### Simulation (기본)
- `microstable.py` + `open_agent_economy.py`를 직접 import
- 로컬 상태 파일: `skills/microstable/.state/microstable-agent-state.json`

### Solana
- `--mode solana --rpc-url https://api.devnet.solana.com`
- 현재 `state`는 RPC read-only 확인 가능
- register/propose/report/heartbeat on-chain tx는 향후 확장

## 참고 문서

- ACP v1 스펙: `references/acp-v1.md`
- 역할 가이드: `references/agent-roles.md`
