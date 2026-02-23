# Economic Mechanism Attacks

Game-theoretic and incentive-based exploits beyond code bugs.

## Category: Rational Actor Exploits

### Profitable Misbehavior
When the expected value of misbehaving > behaving:
- Cost of attack < profit from attack
- Penalty for getting caught < expected gain × (1 - detection probability)
- Defense: Make misbehavior unprofitable via slashing, bonds, reputation

### Tragedy of the Commons
Individual rational actions → collective harm:
- Each agent withdraws fast (rational) → bank run (collective disaster)
- Each keeper skips expensive checks (rational) → system vulnerable (collective)
- Defense: Align individual and collective incentives via mechanism design

## Category: Information Asymmetry

### Frontrunning
Observer has information advantage over protocol users:
- See pending TXs → sandwich attack
- See pending oracle update → trade before update
- Defense: Private mempools, commit-reveal, batch auctions

### Oracle Insider
Entity controlling oracle has information advantage:
- Delay/accelerate price updates for personal benefit
- Defense: Multi-oracle, decentralized oracles, freshness competition

## Category: Collateral/Liquidity Attacks

### Liquidity Crisis Cascade
```
Event → Large withdrawal → Pool imbalance → Slippage increase →
More withdrawals → Further imbalance → Depeg → Panic → Bank run
```
Critical parameters: withdrawal throttle, reserve ratio, circuit breaker threshold

### Collateral Correlation Attack
If all collateral assets are correlated:
- Single market event → all collateral drops → instant undercollateralization
- Defense: Diversified, uncorrelated collateral basket

### Strategic Default
When undercollateralized: rational to abandon position rather than top up.
- Defense: Liquidation before underwater, overcollateralization buffer

## Category: Governance/Agent Attacks

### Flash Governance
Borrow voting power → pass proposal → execute → return power.
- Historical: Beanstalk ($182M)
- Defense: Voting escrow with lockup, timelock, quorum over time

### Agent Collusion
Multiple agents coordinate off-chain to manipulate on-chain governance:
- Coordinated voting, parameter manipulation, selective liquidation
- Defense: Randomized agent selection, stake-weighted with minimum lockup

### Sybil Governance
Create many identities to dominate governance:
- Defense: Minimum stake, capability verification, reputation decay

## Category: Cross-Protocol Attacks

### Composability Risk
Protocol A depends on Protocol B:
- B changes behavior → A breaks
- B gets exploited → A loses funds deposited in B
- Defense: Isolation, independent collateral, circuit breakers on integration points

### Liquidity Fragmentation
Same asset across multiple protocols → liquidity thinned → easier to manipulate each.

## Modeling Framework

For each protocol mechanism, evaluate:
1. **Who are the actors?** (users, keepers, agents, validators)
2. **What are their incentives?** (profit, reputation, ideology)
3. **What actions are available?** (deposit, withdraw, vote, liquidate)
4. **What information do they have?** (public, private, delayed)
5. **Is there a profitable deviation from intended behavior?**
6. **What's the worst case if all actors are adversarial?**
