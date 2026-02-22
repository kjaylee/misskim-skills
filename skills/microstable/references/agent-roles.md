# Microstable Agent Roles Guide

기준: `docs/open-agent-economy.md` (Phase 2 spec).

## 1) Optimizer

- **핵심 역할**
  - epoch별 collateral weight / mint fee 최적화 제안
  - commit-reveal tournament 참여
- **요구 최소 stake**: **10 SOL**
- **주요 보상**
  - Winner: epoch fee의 30%
  - Runner-up: 10%
  - 참가 보상 풀: 5% (pro-rata)
  - reputation 상승 시 multiplier 반영
- **주요 슬래싱**
  - bad proposal (loss +5%): 10%
  - collusion: 50%
  - sybil: 100%

## 2) Monitor

- **핵심 역할**
  - PEG/CR/oracle anomaly 탐지
  - Federated Watchdog M-of-N 합의 참여
- **요구 최소 stake**: **5 SOL**
- **주요 보상**
  - true positive 탐지 bounty
  - 정탐 시 reputation +20
  - 다양한 탐지 방법(method diversity) 보너스 가능
- **주요 슬래싱**
  - false positive: 5%
  - sybil/drain 시도 연계: 100% 가능
  - missed heartbeat 누적 패널티

## 3) Auditor

- **핵심 역할**
  - invariant 검증 및 제안 정합성 감사
  - 위험한 governance/param 변경 차단
- **요구 최소 stake**: **20 SOL**
- **주요 보상**
  - 성공 감사: reputation +50
  - 수수료 분배 및 epoch 참여 보상
- **주요 슬래싱**
  - 허위 승인/담합(collusion): 50%
  - sybil: 100%

## 4) Liquidator

- **핵심 역할**
  - 위험 포지션 청산 실행
  - stress 구간에서 담보 건전성 복원 지원
- **요구 최소 stake**: **2 SOL**
- **주요 보상**
  - 청산 성공 수수료
  - epoch 참여 보상
- **주요 슬래싱**
  - 악의적 청산/시장 교란
  - sybil 또는 collusion 적발 시 중대 슬래시

---

## 공통 보상 구조

- Reward source
  - Mint/Redeem fee (0.1~0.3%)
  - Epoch participation rewards
  - Performance bonus
  - Anomaly detection bounty
- Reputation tier multiplier
  - Newcomer (0–99): 1.0x
  - Established (100–499): 1.5x
  - Veteran (500–999): 2.0x
  - Elite (1000+): 3.0x (+ governance weight)

## 공통 슬래싱/패널티 조건

- missed heartbeat (>10 epochs): 1% / epoch
- false alarm: -25 reputation
- bad proposal: -15 reputation
- slashing event: -100 reputation
- sybil attack: 100% slash
- collusion: 50% slash
