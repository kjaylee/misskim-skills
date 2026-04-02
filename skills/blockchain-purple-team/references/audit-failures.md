# Audit Failure Patterns — Why Professional Audits Miss Critical Vulnerabilities

## AF-1: Scope Blindness
**Pattern**: Audit scope covers smart contract code but not economic design, oracle behavior, or off-chain components.
**Historical**: Mango Markets — code was "correct" but economic incentives allowed $114M manipulation.
**Detection**: Review audit scope document. If it says "smart contract only" → economic attacks unreviewed.

## AF-2: Assumption Inheritance
**Pattern**: Auditor trusts external dependencies (oracle, token program, bridge) without verifying their failure modes.
**Historical**: Multiple protocols exploited via oracle manipulation that auditors assumed "Chainlink is reliable."
**Detection**: List all external dependencies. For each: "Did the audit consider failure/manipulation of this dependency?"

## AF-3: Temporal Blindness
**Pattern**: Audit is point-in-time snapshot. Protocol evolves after audit (upgrades, config changes, new integrations).
**Historical**: Compound governance bug introduced post-audit via proposal execution.
**Detection**: Compare current code hash to audited code hash. Any diff = unaudited surface.

## AF-4: Composition Blindness
**Pattern**: Each component audited separately. Cross-component interactions never tested.
**Historical**: Curve/Vyper — Vyper compiler audited, Curve contracts audited, but compiler bug + specific contract pattern = exploit.
**Detection**: Map all cross-component interactions. Verify each was explicitly tested.

## AF-5: Edge Case Negligence
**Pattern**: Auditor tests happy path and obvious attack paths. Unusual states (zero balance, max value, empty pool) untested.
**Historical**: Numerous "first depositor" attacks in DeFi vaults (share price manipulation when pool is empty).
**Detection**: For each operation, test with: zero, one, max, just-above-limit, just-below-limit inputs.

## AF-6: Economic Modeling Gap
**Pattern**: Auditor lacks game theory expertise. Can find code bugs but not incentive misalignments.
**Historical**: Beanstalk — code was technically correct, economic mechanism allowed flash governance.
**Detection**: Ask: "Was a game-theoretic analysis performed? By whom? With what adversary model?"

## AF-7: Multi-TX Blindness
**Pattern**: Auditor reviews each function in isolation. Multi-step attack sequences across functions/TXs unreviewed.
**Historical**: Many reentrancy exploits involve 2+ functions interacting.
**Detection**: For each pair of state-modifying functions: "Can calling A then B create inconsistency?"

## AF-8: Upgrade Path Blindness
**Pattern**: Current code is secure. But upgrade mechanism allows replacing it with anything.
**Historical**: Nomad bridge — upgrade key compromised → malicious implementation deployed.
**Detection**: "Who can upgrade? What's the timelock? Is there a veto?"

## AF-9: Off-Chain Component Omission
**Pattern**: On-chain code audited. Keeper/bot/frontend/backend completely unreviewed.
**Historical**: BadgerDAO — frontend compromise injected malicious approvals ($120M).
**Detection**: Map all off-chain components. For each: "Was this in audit scope?"

## AF-10: Known-Pattern Fixation
**Pattern**: Auditor checks known vulnerability checklist (reentrancy, overflow, access control) but misses protocol-specific logic bugs.
**Historical**: Compound distribution error — not a "known" vulnerability class, just wrong math.
**Detection**: Beyond checklist: "Does the implementation match the specification for EVERY operation?"

## AF-11: Cross-Component Configuration Desync (CCCCD)
**Pattern**: Each off-chain/on-chain component reviewed individually and found correct. The vulnerability emerges from a parameter/configuration mismatch across the integration boundary that no single audit covers.
**Historical**: Aave CAPO (2026-03-10, $26-27M): off-chain oracle updated with 7-day reference window; on-chain CAPO enforced 3% per 3-day cap. Both individually correct. The timestamp/ratio mismatch caused 2.85% price undervaluation → E-Mode liquidations.
**Detection**: Build "cross-component parameter alignment matrix" — for each off-chain/on-chain pair, verify parameter windows and thresholds are explicitly matched. Automated integration fuzzing must validate "what off-chain sends + how on-chain processes = correct outcome."

## AF-12: Leverage Mode Amplification Blindness
**Pattern**: Audits test "is the oracle price correct?" but not "what is the realistic oracle error bound, and does the protocol's LTV account for it?" High-leverage modes (90%+ LTV) amplify even small oracle errors into liquidation cascades.
**Historical**: Aave E-Mode: 2.85% oracle misfire consumed ~40% of the ~7% safety margin.
**Detection**: For high-LTV modes: model oracle price as a distribution, not point estimate. Verify LTV leaves margin beyond oracle's realistic maximum error. Stress-test simultaneous multi-account liquidation scenarios.

## AF-13: Fuzzer Structural Blind Spot — Precision Loss Accumulation
**Pattern**: All four major smart contract fuzzers (Foundry, Echidna, Medusa, Trident) structurally fail to detect precision loss accumulation across repeated operations. Audit reports present "Foundry invariant testing passed" as comprehensive fuzzing coverage, while the precision loss class remains undetected.
**Historical**: Smart Contract Fuzzer Showdown (2026-03-20, dev.to/ohmygod): 8 invariant-breaking challenges based on real DeFi hacks. Precision Loss: Foundry ❌ (500K+ timeout), Echidna ❌ (500K+), Medusa ❌, Trident N/A. Foundry also missed Oracle Manipulation (10M+ timeout) and Flash Loan Governance (10M+).
**Detection**: For any protocol with integer division in share/amount conversions: (a) explicitly test with high-operation-count sequences (deposit/redeem × 100+), (b) derive closed-form bound for N-operation precision error and assert it in a committed invariant test, (c) do NOT accept "fuzzers passed" as precision loss coverage — note this specific gap in close-out reports.

## AF-14: Approval-Execution Intent Drift
**Pattern**: Audit verifies that signatures are valid and quorum is met, but does not verify that signer intent remains equivalent from approval time to execution time. Durable nonce, off-band partial signatures, batched approvals, and delayed broadcast create a gap where perfectly valid signatures can authorize materially different real-world outcomes than signers believed.
**Historical**: Drift Protocol (2026-04-02 reporting): durable nonce accounts enabled pre-signed privileged transactions to remain valid long after approval, turning a multisig workflow into an admin-takeover path without requiring raw key theft.
**Detection**: For every privileged workflow ask: (a) can the transaction be pre-signed, partially signed, or stored for later broadcast, (b) is there an approval TTL, revoke path, or nonce invalidation flow, (c) do signers review a human-readable intent digest rather than opaque bytes, (d) does any authority transfer or limit lift require second-stage confirmation or timelock.

## AF-15: Framework Security-Default Drift
**Pattern**: Audit treats framework behavior as a stable trusted substrate and does not revisit protocol risk when the upstream framework later hardens default semantics. Security-relevant release-note items are misread as developer-experience improvements instead of evidence that older defaults were unsafe.
**Historical**: Anchor `v1.0.0` (2026-04-02) added owner checks on `reload()` and disallowed duplicate mutable accounts by default. This implies older Anchor-pinned protocols may keep latent exposure even when their app code is unchanged and previously audited.
**Detection**: Maintain an upstream security-delta review for every pinned framework/toolchain. If a release adds new default guards, ask: (a) which older code paths relied on the old behavior, (b) what compensating assertions exist today, (c) does the audit attestation explicitly cover the pinned framework version and its known semantic gaps, (d) is there a version SBOM linking on-chain program, keeper client, and deployment tooling.

## Meta-Insight
The common thread: **auditors optimize for known patterns and explicit scope.**
Purple Team optimizes for: **unknown patterns, implicit assumptions, and scope gaps.**
