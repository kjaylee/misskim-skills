# Defense Bypass Evolution — How Patched Vulnerabilities Get Re-Exploited

## DE-1: Patch Regression
**Pattern**: Fix for vulnerability A introduces vulnerability B.
**Example**: Adding a reentrancy guard that skips a critical state update on the guarded path.
**Detection**: After every fix, re-run ALL attack vectors (not just the fixed one).

## DE-2: Variant Attack
**Pattern**: Same root cause, different entry point or mechanism.
**Example**: Fix reentrancy on `withdraw()` but not on `withdrawAll()` or `emergencyWithdraw()`.
**Detection**: For each fix, list ALL functions with similar patterns. Verify fix applied to ALL.

## DE-3: Defense Decay
**Pattern**: Defense was valid at deployment but environment changed.
**Example**: Oracle staleness check of 120 slots was safe when prices moved slowly. After volatility spike, 120 slots = too long.
**Detection**: List all hardcoded parameters in defenses. For each: "Under what conditions does this become insufficient?"

## DE-4: Incomplete Root Cause Fix
**Pattern**: Symptom patched but root cause remains.
**Example**: Added `require(amount > 0)` but real issue is unchecked arithmetic elsewhere.
**Detection**: For each fix, ask: "What was the ROOT CAUSE? Does this fix address it or just one manifestation?"

## DE-5: Fix Creates New Attack Surface
**Pattern**: Defense mechanism itself becomes the attack vector.
**Example**: Circuit breaker that halts trading → attacker triggers circuit breaker to freeze protocol at advantageous state.
**Detection**: For each defense mechanism: "Can an attacker deliberately trigger this? What state does triggering create?"

## DE-6: Configuration Drift
**Pattern**: Defense depends on configuration that changes over time.
**Example**: Fee rate set to prevent flash loan attacks. Governance reduces fee → attack viable again.
**Detection**: Map all configurable parameters that affect security. Monitor for changes.

## DE-7: Dependency Update Bypass
**Pattern**: Fix depends on external library behavior. Library updates change behavior.
**Example**: Anchor version upgrade changes account validation semantics.
**Detection**: Pin dependency versions. Review security implications of every upgrade.

## DE-8: Gradual Erosion
**Pattern**: Defense has a threshold. Attacker stays just below threshold, accumulating over time.
**Example**: Rate limit of 1000 tokens/block. Attacker extracts 999/block for 1000 blocks = 999,000 tokens.
**Detection**: Evaluate defenses against sustained low-intensity attacks, not just single large attacks.

## DE-9: MEV as Unintended Beneficiary of Protocol Misconfiguration
**Pattern**: Protocol misconfiguration creates MEV opportunity. MEV bots automatically extract value — with NO incentive to report the underlying misconfiguration. The extractor profits regardless of whether the root cause is fixed.
**Example**: Aave CAPO misfire (2026-03-10): ~499 ETH in liquidator profits captured by MEV bots while $26-27M in user positions were liquidated. The MEV bots had zero incentive to report the CAPO bug — they profited from it.
**Detection**: Map all protocol misconfiguration scenarios and ask: "Does MEV bot participation create a perverse incentive to not report?" If yes → the misconfiguration is self-amplifying.
**Defense**: Protocol-level MEV awareness — monitor for anomalous MEV bot behavior that correlates with user harm. Consider MEV rebate mechanisms that align bot incentives with protocol health.

## Evolution Tracking Framework

For each known vulnerability + fix:
```
| Vuln ID | Fix Date | Fix Type | Root Cause Addressed? | Variant Check? | Regression Test? | Decay Risk? |
```

Review quarterly: "Has the environment changed enough to invalidate any fix?"
