# Timing Attacks

Exploiting temporal boundaries in blockchain protocols.

## Slot/Block Boundary Attacks

### Same-Slot Sequencing
Multiple TXs in the same slot can be ordered by the validator.
- Attack: Submit A and B knowing A will execute first
- Defense: Operations should be idempotent within a slot

### Epoch Boundary
Solana epochs trigger leader rotation, stake updates, inflation distribution.
- Attack: Exploit transition period where old and new state coexist
- Defense: Fence operations across epoch boundaries

### Staleness Window
Oracle prices are valid for N slots. The window edges are dangerous.
- Attack: Act at slot N-1 when price has moved but check still passes
- Defense: Shorter windows + dynamic adjustment based on volatility

## Timing-Based Race Conditions

### Keeper vs Attacker Race
```
Slot 100: Price drops sharply
Slot 101: Attacker submits mint with stale price
Slot 102: Keeper submits oracle update
```
If attacker wins the race → mints at old (higher) price.

### Multi-Keeper Race
```
Slot 100: Both keepers see same trigger
Slot 101: Keeper A submits TX
Slot 101: Keeper B submits TX (same slot)
```
Both succeed → double action (double liquidation, double rebalance).

## Clock Manipulation

### Solana Clock Approximation
`Clock::get()?.unix_timestamp` is leader-reported, not consensus.
- Variance: ±1-2 seconds from wall clock
- Attack: If protocol uses timestamp for critical logic, small manipulations possible

### Slot Duration Variance
Average 400ms but actual varies. High-load periods stretch slots.
- Attack: Assumptions about "N slots = M seconds" break under load

## Defense Patterns

1. **Idempotent operations** — Safe to execute multiple times
2. **Monotonic state** — State can only move forward
3. **Freshness over windows** — Use "most recent" not "within N slots"
4. **Leader election** — Single keeper acts per epoch/period
5. **Commit-reveal** — Hide intent until execution
