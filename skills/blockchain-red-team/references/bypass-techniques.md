# Defense Bypass Techniques

## Methodology: 3-Question Framework

For every defense, ask:
1. **What assumption does this defense make?** (e.g., "oracle is fresh", "only one TX per slot")
2. **Can the assumption be violated?** (e.g., "Pyth can be stale for 120 slots")
3. **What happens when it's violated?** (e.g., "mint at stale high price, redeem at current low")

## Common Bypass Patterns

### BP-1: Timing Window Bypass
**Defense**: Staleness check rejects prices older than N slots
**Bypass**: Execute at slot N-1 (just within window but price already moved significantly)
**Key**: Many defenses use generous windows to avoid false rejections

### BP-2: Boundary Condition Bypass
**Defense**: `require!(amount >= MIN_AMOUNT)`
**Bypass**: Use `MIN_AMOUNT` exactly, repeated many times
**Key**: Minimum thresholds are often set for UX, not security

### BP-3: State Ordering Bypass
**Defense**: Check runs before operation
**Bypass**: Reach a state where the check passes but the operation has different semantics
**Key**: State machines with unexpected transitions

### BP-4: Multi-TX Bypass
**Defense**: Single-TX rate limit
**Bypass**: Split attack across multiple TXs in same block/slot
**Key**: Per-TX limits ≠ per-block/per-epoch limits

### BP-5: Authority Separation Bypass
**Defense**: Different authorities for different operations
**Bypass**: If authorities share infrastructure (same machine, same key file directory)
**Key**: Logical separation ≠ physical separation

### BP-6: Circuit Breaker Bypass
**Defense**: Halt operations when anomaly detected
**Bypass**: Attack below detection threshold (slow drain)
**Key**: Circuit breakers calibrated for catastrophic events miss gradual extraction

### BP-7: Multi-Collateral Arbitrage
**Defense**: Per-collateral limits
**Bypass**: Exploit price differences across collateral types
**Key**: Independent limits per asset don't prevent cross-asset arbitrage

### BP-8: Oracle Confidence Bypass
**Defense**: Reject prices with wide confidence intervals
**Bypass**: Wait for brief moment of narrow confidence during volatile period
**Key**: Confidence narrows periodically even in chaos

### BP-9: Fee Bypass
**Defense**: Dynamic fees increase during stress
**Bypass**: If fee calculation uses stale data, front-run the fee update
**Key**: Fee update frequency vs attack speed

### BP-10: Governance Delay Bypass
**Defense**: Timelock on parameter changes
**Bypass**: Attack with current parameters that are about to change
**Key**: Knowledge of pending changes is public on-chain
