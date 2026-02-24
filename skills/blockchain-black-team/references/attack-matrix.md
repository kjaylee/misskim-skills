# Attack Matrix — 28 Vectors with Historical Mechanisms & Defense Patterns

## A. Smart Contract Vectors

### A1. Reentrancy
**Historical**: The DAO (2016, $60M), Curve/Vyper (2023, $70M), Cream Finance ($130M)
**Mechanism**: External call executes before state update completes. Attacker's callback re-enters the vulnerable function, draining funds in a loop.
**Solana variant**: CPI callback during token transfer hook (Token-2022). SPL Token classic has no hooks, limiting surface.
**Code pattern to find**:
```
// VULNERABLE: external call before state update
transfer(attacker, amount);
balances[attacker] -= amount;  // too late

// SAFE: state update before external call (CEI)
balances[attacker] -= amount;
transfer(attacker, amount);
```
**Defense**: Checks-Effects-Interactions (CEI), reentrancy guards, token program ID pinning.

### A2. Flash Loan + Price Manipulation
**Historical**: Mango Markets (2022, $114M), Euler (2023, $197M), Harvest (2020, $25M), PancakeBunny (2021, $45M), BonqDAO (2023, $120M)
**Mechanism**: Borrow massive capital in single TX → manipulate AMM/oracle price → exploit mispriced mint/redeem/liquidation → repay loan with profit.
**Key insight**: Any protocol that reads price from a manipulable source within the same TX is vulnerable.
**Code pattern to find**:
```
// VULNERABLE: same-block price read for critical operation
let price = get_oracle_price();  // can be stale or manipulated
let mint_amount = collateral * price / target;
mint(user, mint_amount);
```
**Defense**: TWAP oracles, staleness checks (>N slots = reject), confidence interval checks, mint/redeem cooldowns, per-block volume limits.

### A3. Oracle Manipulation
**Historical**: Mango (Pyth feed manipulation), BonqDAO (TellorFlex oracle), Harvest (Curve pool as oracle), Moonwell (2026, $1.78M bad debt)
**Mechanism**: Push stale/false price data to oracle → protocol acts on wrong price → value extraction.
**2026 reinforcement (Moonwell)**: Oracle-composition unit mismatch (`cbETH/ETH` ratio treated as USD price) created a 99%+ mispricing window and automated liquidations.
**Solana/Pyth specific**: Pyth confidence intervals, staleness (slot age), status checks.
**Code pattern to find**:
```
// VULNERABLE: no staleness check
let price = pyth_price.price;
// VULNERABLE: no confidence check
// VULNERABLE: no status check (Trading vs Unknown)

// VULNERABLE: ratio feed used directly as USD
let usd_price = cbeth_eth_ratio; // missing * eth_usd
```
**Defense**: `max_staleness_slots`, `min_confidence_ratio`, `price_status == Trading`, explicit unit normalization (`ratio * base_usd`), on-chain price sanity bands, multi-oracle fallback.

### A4. Access Control
**Historical**: Ronin ($624M — 5/9 validator keys), Wormhole ($320M — guardian signature bypass), Poly Network ($611M — role verification bypass)
**Mechanism**: Missing or bypassable authorization checks allow unauthorized callers to execute privileged operations.
**Solana specific**: Missing `has_one`, `constraint`, signer checks on authority accounts.
**Code pattern to find**:
```rust
// VULNERABLE: no authority check
pub fn admin_withdraw(ctx: Context<AdminWithdraw>) -> Result<()> {
    // missing: require!(ctx.accounts.authority.key() == expected)
}
```
**Defense**: Anchor `has_one`, `constraint`, explicit signer verification, multisig for critical ops.

### A5. Integer Overflow/Underflow
**Historical**: Compound ($147M — distribution math error), multiple early Solidity contracts
**Mechanism**: Arithmetic operation wraps around or produces unexpected result, allowing minting excess tokens or bypassing limits.
**Rust/Solana**: Rust panics on overflow in debug, wraps in release. Anchor uses checked math by default.
**Code pattern to find**:
```rust
// RISKY: unchecked arithmetic in release mode
let result = a * b / c;  // could overflow before division
// SAFE:
let result = (a as u128).checked_mul(b as u128)?.checked_div(c as u128)?;
```
**Defense**: `checked_*` operations, u128 intermediates, explicit overflow tests.

### A6. Account Substitution (Solana)
**Historical**: Cashio ($52M — fake collateral account), multiple Solana exploits
**Mechanism**: Attacker passes a different account than expected. If program doesn't verify account address/owner/discriminator, wrong data is used.
**Code pattern to find**:
```rust
// VULNERABLE: no address/owner verification
pub collateral_mint: Account<'info, Mint>,
// Attacker passes their own fake mint with inflated supply
```
**Defense**: `constraint = collateral_mint.key() == EXPECTED_MINT`, `has_one`, seed derivation checks.

### A7. Signature Replay
**Historical**: Wintermute ($160M), multiple
**Mechanism**: Reuse a valid signed transaction or message in a different context (chain, nonce, program).
**Defense**: Nonce accounts, domain separators, one-time-use flags.

### A8. Front-running / Sandwich
**Historical**: MEV ecosystem ($B+ annually)
**Mechanism**: Observer sees pending TX → inserts TX before (front) and after (back) to extract value.
**Defense**: Commit-reveal, private mempools, slippage limits, batch auctions.

### A9. Proxy Upgrade Attack
**Historical**: Nomad ($190M — implementation replacement), multiple UUPS
**Mechanism**: Compromise upgrade authority → replace program logic with malicious version.
**Solana**: `solana program deploy` requires upgrade authority. BPF loader upgrade mechanism.
**Defense**: Multisig upgrade authority, timelock, freeze authority, eventual immutability.

### A10. Logic Bug
**Historical**: Compound ($147M — distribution logic), Cream ($130M — accounting), Popsicle ($20M — fee tracking), Moonwell (2026 oracle wiring regression)
**Mechanism**: Incorrect business logic allows unintended state transitions or value extraction.
**2026 reinforcement (Moonwell)**: Governance-approved deployment can still ship a one-line arithmetic/wiring omission if unit-invariant tests are missing.
**Defense**: Formal spec → test cases → implementation. Invariant tests. Fuzzing. Add explicit unit tests for oracle composition and deploy-time sanity assertions (`min_price <= feed <= max_price`).

### A11. Rent/Lamport Drain (Solana)
**Historical**: Multiple small-scale
**Mechanism**: When account is closed, remaining lamports must go somewhere. If not properly handled, attacker can drain.
**Defense**: `close = destination` in Anchor, explicit lamport accounting.

### A12. CPI Confusion (Solana)
**Historical**: Crema Finance ($8.8M)
**Mechanism**: Program makes CPI to what it thinks is a trusted program, but attacker substitutes a malicious program at that address.
**Defense**: Verify program ID of CPI target: `Program<'info, Token>` with explicit ID check.

### A13. PDA Seed Collision (Solana)
**Historical**: Multiple
**Mechanism**: Two different logical entities derive to the same PDA because seeds overlap.
**Defense**: Include type discriminator in seeds, unique prefixes per entity type.

## B. Off-chain/Keeper Vectors

### B14. RPC Manipulation
**Mechanism**: MITM or compromised RPC returns false blockchain state → keeper makes wrong decisions.
**Defense**: Multi-RPC consensus, TLS pinning, response validation against known state.

### B15. Key Compromise
**Historical**: Ronin ($624M), Harmony ($100M), Slope wallet
**Mechanism**: Private key stolen from file/memory/HSM → full control of associated accounts.
**Defense**: HSM, threshold signatures, key rotation, file encryption, memory zeroization.

### B16. Race Condition
**Mechanism**: Multiple keepers submit conflicting TXs → inconsistent state.
**Defense**: Leader election, sequence numbers, idempotent operations.

### B17. Checkpoint Poisoning
**Mechanism**: Attacker modifies saved optimizer/state files → keeper resumes from corrupted state.
**Defense**: Checksums, authenticated encryption, read-only mounts.

### B18. Config Injection
**Mechanism**: Modify config file → change RPC endpoints, fee rates, authority keys.
**2026 reinforcement (Moonwell)**: Misconfigured oracle rollout plus unbypassable timelock can lock protocol into a bad config long enough for extraction.
**Defense**: Config file permissions (600), integrity checks, immutable deployment, and emergency fast-path for oracle rollback/kill-switch outside normal governance delay.

### B19. Memory/Log Leak
**Historical**: Slope wallet (private keys in Sentry logs)
**Mechanism**: Sensitive data (keys, seeds) leaked through logs, crash dumps, or memory.
**Defense**: Zeroize sensitive memory, log scrubbing, no-debug builds.

### B20. Denial of Service
**Historical**: Solana network halts (2021-2022)
**Mechanism**: Exhaust keeper resources (CPU/memory/RPC quota) → protocol stops operating.
**Defense**: Rate limiting, circuit breakers, graceful degradation, health monitoring.

## C. Economic Vectors

### C21. Bank Run / Depeg
**Historical**: UST/LUNA ($40B), USDC/SVB ($1B+ temporary), Iron Finance
**Mechanism**: Loss of confidence → mass redemption → reserves insufficient → depeg spiral.
**Defense**: Redemption throttling, dynamic fees, circuit breakers, overcollateralization buffer.

### C22. Collateral Manipulation
**Historical**: stETH depeg, Tether FUD events
**Mechanism**: Collateral asset loses value faster than protocol can adjust → undercollateralization.
**Defense**: Multi-collateral diversification, real-time CR monitoring, auto-rebalance, liquidation mechanisms.

### C23. Governance Attack
**Historical**: Beanstalk ($182M — flash loan governance)
**Mechanism**: Acquire voting power (via flash loan or sybil) → pass malicious proposal → drain treasury.
**Defense**: Timelock, quorum requirements, voting escrow, stake-weighted with lockup.

### C24. Sybil Attack
**Mechanism**: Create many identities to gain disproportionate influence.
**Defense**: Minimum stake, identity verification, reputation decay, capability gates.

### C25. MEV Extraction
**Mechanism**: Extract value from protocol transactions via ordering manipulation.
**Defense**: Commit-reveal, private submission, MEV-share, protocol-owned ordering.

## D. Infrastructure Vectors

### D26. Frontend XSS/Injection
**Historical**: BadgerDAO ($120M — Cloudflare Workers compromise injected approval TX)
**Mechanism**: Compromise frontend → inject malicious transaction approvals.
**Defense**: CSP headers, SRI hashes, no external scripts, static hosting.

### D27. RPC Endpoint Takeover
**Mechanism**: DNS hijack or BGP hijack redirects RPC traffic → false chain state.
**Defense**: Multiple independent RPCs, DNSSEC, certificate pinning.

### D28. Supply Chain
**Historical**: event-stream (2018), ua-parser-js (2021), multiple npm attacks
**Mechanism**: Compromise dependency → inject malicious code into build.
**Defense**: Lock files, audit dependencies, minimal dependency tree, vendoring.
