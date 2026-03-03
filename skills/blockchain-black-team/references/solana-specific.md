# Solana-Specific Attack Patterns

## Account Model Vulnerabilities

### Missing Owner Check
Solana accounts have an `owner` field (the program that controls them). If a program reads data from an account without verifying the owner, an attacker can pass a fake account owned by their own program with crafted data.

```rust
// VULNERABLE
let data = account.try_borrow_data()?;
let amount = u64::from_le_bytes(data[0..8]);

// SAFE (Anchor handles this via Account<> type)
#[account(owner = expected_program)]
pub data_account: Account<'info, MyData>,
```

### Missing Discriminator Check
Anchor uses an 8-byte discriminator (SHA256 hash of account type name) to prevent account type confusion. Raw Solana programs or non-Anchor accounts may lack this.

### Writable Account Not Required
If an instruction modifies an account but doesn't require `mut`, the runtime won't persist changes — but the instruction may still execute logic based on stale reads.

## CPI (Cross-Program Invocation) Patterns

### Unchecked CPI Target
```rust
// VULNERABLE: attacker can substitute any program
invoke(&instruction, &[account1, account2])?;

// SAFE: verify program ID
require!(token_program.key() == spl_token::ID);
```

### Signer Privilege Escalation
CPI can propagate signer status. If a PDA signs via `invoke_signed`, ensure seeds are not predictable or reusable by attacker.

### Arbitrary CPI with User-Provided Program
Never allow users to specify which program to CPI into for sensitive operations.

## PDA (Program Derived Address) Patterns

### Seed Grinding
PDA derivation uses `find_program_address` which searches for a valid bump. If seeds are predictable, attacker may find collisions.

### Missing Bump Verification
```rust
// VULNERABLE: attacker can provide wrong bump
pub fn init(ctx: Context<Init>, bump: u8) -> Result<()> {
    // uses attacker-provided bump

// SAFE: use canonical bump
#[account(seeds = [b"vault", user.key().as_ref()], bump)]
pub vault: Account<'info, Vault>,
```

### Cross-Seed Collision
If two different account types use overlapping seed patterns, they may derive to the same PDA.

```rust
// Type A: seeds = ["data", user_pubkey]
// Type B: seeds = ["data", user_pubkey]  ← COLLISION
// Fix: seeds = ["data_a", user_pubkey] / ["data_b", user_pubkey]
```

## Token Program Patterns

### SPL Token vs Token-2022
- SPL Token (classic): No transfer hooks, predictable behavior
- Token-2022: Transfer hooks enable callbacks during transfers → reentrancy surface
- Always verify which token program is being used

### Mint Authority Check
```rust
// Ensure only protocol can mint
require!(mint.mint_authority == Some(protocol_pda));
```

### Close Authority Drain
When closing a token account, remaining tokens + lamports go to destination. Verify destination is correct.

## Rent & Lamport Accounting

### Rent-Exempt Minimum
Accounts below rent-exempt minimum get garbage collected. Attacker can drain lamports to just below threshold.

### Account Close Lamport Drain
```rust
// When closing: all lamports go to `close` destination
#[account(mut, close = receiver)]
pub account_to_close: Account<'info, MyData>,
// Ensure `receiver` is the intended recipient
```

## Timing & Ordering

### Slot-Based vs Real-Time
Solana uses slots (~400ms) not wall-clock time. `Clock::get()?.unix_timestamp` is approximate and can be manipulated by validators within bounds.

### Transaction Ordering
Validators can reorder transactions within a block. MEV is possible on Solana via Jito and similar infrastructure.

## Oracle Composition & Unit Safety

### Ratio Feed Misuse (Unit Normalization Bug)
When protocols compose feeds (e.g., token/base ratio + base/USD), missing one leg can convert a ratio into a false USD price.

```rust
// VULNERABLE: ratio treated as final USD price
let cbeth_eth = ratio_feed.price;
let usd_price = cbeth_eth; // missing ETH/USD multiplier

// SAFE: explicit composition + sanity guard
let eth_usd = base_usd_feed.price;
let usd_price = cbeth_eth
    .checked_mul(eth_usd)
    .ok_or(ErrorCode::MathOverflow)?
    / SCALE;
require!(usd_price >= MIN_PRICE && usd_price <= MAX_PRICE, ErrorCode::InvalidPrice);
```

### Timelock Recovery Gap
If oracle config changes require long governance delay, attacker can exploit the gap before rollback.

Mitigation:
- Emergency oracle pause path (separate authority with strict scope)
- Fast rollback for feed misconfiguration
- Deployment-time invariant checks (unit tests + on-chain sanity range)

## New 2026 Patterns (Anchor/SPL/Jito Surface)

### Anchor IDL External-Account Overtrust
Anchor patched IDL generation to exclude externally owned account types from internal account definitions (`idl: Exclude external accounts`, 2026-02-22).

**Risk pattern**:
- Client/wallet tooling treats generated IDL as a trust source.
- External accounts appear “first-party safe” in automation or signing UX.
- Integrator skips owner/program checks because metadata looked authoritative.

**Mitigation**:
- Keep runtime owner checks in on-chain code as source of truth.
- In off-chain clients, validate `account.owner` and expected program IDs before signing.
- Treat IDL/schema as descriptive, never as an authorization boundary.


### Anchor IDL Program-ID Drift (PMP Refactor Surface)
Anchor `Refactor IDL PMP commands` (2026-02-27) introduced `--allow-localnet` and optional `--program-id` for IDL init/upgrade flows.

**Risk pattern**:
- CI/ops scripts that previously depended on implicit workspace/program resolution can now execute IDL writes against the wrong cluster/program when flags are omitted or environment variables drift.
- If a privileged deploy key runs the command with a wrong `program-id`, the wrong IDL metadata account may be initialized/upgraded.
- Off-chain clients that auto-consume IDL metadata can then trust a mismatched schema, creating a metadata-confusion foothold (D31 bypass variant).

**Mitigation**:
1. In production, pin both cluster and `program-id` explicitly in scripts (never rely on defaults)
2. Block `--allow-localnet` in release pipelines
3. Preflight check: fetch on-chain program metadata and assert expected authority + program id before `idl upgrade`
4. Postflight check: compare deployed IDL hash against expected artifact hash

**Sources**:
- https://github.com/solana-foundation/anchor/commit/21e67c99471134fe565c5dc6f3e23d7ee481a66a
- https://github.com/solana-foundation/anchor/commits/master.atom

### Slot-Flow Quota Capture (Redemption Griefing)
Protocols with global per-slot caps can be DoSed by one actor who consumes most of the quota early each slot.

**Attack shape**:
1. Attacker prepares redeemable balance.
2. Sends burst redeems at slot boundary.
3. Honest user redeems revert with slot-limit errors despite healthy collateral.

**Mitigation**:
- Per-actor fair-share limits (or stake-weighted quotas).
- Priority lanes for small/organic redeems.
- Burst scoring + grief penalties.

### Redeem Path Validation Bypass (Stake Nova Pattern)
Stake Nova (2026-02-27, Solana) was drained (~$2.39M) after an unchecked validation path in `RedeemNovaSol()` was combined with flash-loan liquidity.

**Solana-specific risk**:
- Redeem code may appear safe under normal flow but fail when atomic liquidity is amplified in one slot.
- If redeem output/account constraints are incomplete, attacker can drain vaults before invariant checks catch up.

**Mitigation**:
- Enforce strict `min_out` and account-binding checks at instruction boundary.
- Apply per-TX + per-slot redeem caps even for keeper-assisted flows.
- Require invariant assertions before and after transfer CPI (`supply`, `vault balances`, `user position`).

**Source**: https://hacked.slowmist.io/

### Typosquat Waves Targeting Solana Rust Tooling
Recent RustSec advisories (`rpc-check`, `tracing-check`) show short-lived malicious crates aimed at credential theft in a specific ecosystem.

**Mitigation**:
- Cargo.lock hash attestation in CI/runtime.
- Registry-source allowlist (crates.io only unless explicitly approved).
- Two-person review for dependency additions/renames near common crate names.

### Transitive Payload Relay (tracings → tracing_checks, 2026-02-26)
New RustSec advisories (`RUSTSEC-2026-0027`, `RUSTSEC-2026-0028`) show a second-stage pattern: the top-level crate looks lightweight while malware is hidden in a transitive dependency.

**Solana/Anchor impact pattern**:
- Keeper teams often add telemetry crates (`tracing*`) during incident response.
- Direct dependency review can miss transitive payload crates that execute build/runtime hooks.
- Cargo.lock attestation protects against *unexpected* lock changes, but if a malicious dependency is deliberately merged and attested, runtime checks will still pass.

**Mitigation upgrade**:
- CI must diff full transitive graph (`cargo tree --locked`) for every dependency change.
- Quarantine newly published crates (<7 days) unless emergency security override is approved.
- Add crate-name distance checks (e.g., `tracing` vs `tracings`) before merge.
- Require two-person security sign-off specifically on Cargo.lock hash updates.

**Sources**:
- https://rustsec.org/advisories/RUSTSEC-2026-0027.html
- https://rustsec.org/advisories/RUSTSEC-2026-0028.html

### ZK Verifier Key Binding Drift (FOOMCASH Pattern)
FOOMCASH (2026-02-26, ~$2.26M) was exploited after verification-key configuration drift enabled forged/invalid zkSNARK proof acceptance.

**Solana-specific risk**:
- Programs integrating zk verifiers (Groth16/Plonk wrappers or proof-verification CPI) may trust mutable verifier account/config without strict hash binding.
- If verifier key, circuit ID, or public-input schema changes without hard invariants, proof checks can pass for the wrong statement.

**Pattern to detect in codebase**:
```rust
// RISKY: verifier account accepted from mutable config with weak governance
let verifier = load_verifier_account(ctx.accounts.verifier_config)?;
require!(verify_proof(proof, public_inputs, verifier), ErrorCode::InvalidProof);

// SAFER: pin expected verifier key hash / circuit id and assert on every call
require!(verifier.key_hash == EXPECTED_VK_HASH, ErrorCode::VerifierMismatch);
require!(public_inputs.version == EXPECTED_CIRCUIT_VERSION, ErrorCode::CircuitVersionMismatch);
```

**Mitigation**:
1. Immutable verifier-key hash (or two-step timelocked update with quorum)
2. Circuit ID + public-input schema version checks (domain separation)
3. Upgrade pipeline canary proofs (expected-pass + expected-fail)
4. Emergency pause if verifier-integrity check fails

**Sources**:
- https://hacked.slowmist.io/
- https://www.cryptotimes.io/2026/02/26/foomcash-loses-2-26m-in-copycat-zksnark-exploit/

## Hot Key & Stake Authority Patterns (2026 Addition)

### Social-Engineering-to-Stake-Authority-Hijack
Step Finance (2026-01-31, $27.3M): Executive device phished → stake delegation authority transferred to attacker wallet → 261,854 SOL unstaked in 90 minutes. Audited contracts, bug bounties, and security reviews were irrelevant.

**Solana-specific risk**: Stake delegation model separates `StakeAuthority` and `WithdrawAuthority`. Both can be re-assigned unilaterally by the current controller via a single signed instruction. No program code involved. Indistinguishable from legitimate on-chain operations.

**Keeper relevance**: Keeper hot keys on operator's machine have the same exposure. If keeper host is compromised:
- Attacker signs privileged keeper instructions (oracle updates, rebalance)
- Steals treasury-authority keypair → drains treasury
- If MANUAL_ORACLE_MODE path is accessible via keeper key, attacker gains price manipulation surface

**Pattern to detect in codebase**:
```rust
// Check: is the keeper keypair also the stake withdrawal authority?
// If yes → compromise of keeper host = loss of staked collateral
// SAFE: separate keypairs for keeper ops vs treasury/stake authority
```

**Defense**:
1. Hardware keys for any keypair controlling SOL stake or treasury withdrawal
2. Stake accounts split into small sub-accounts (cap loss per account)
3. `StakeAuthorize` changes require M-of-N signatures (multisig delegate)
4. Keeper keypair scope-limited: can only submit to program, cannot re-assign authority
5. EDR on all operator machines; phishing simulation training

## Solana-Specific Defense Checklist

1. ☐ All accounts have owner checks (Anchor `Account<>` type)
2. ☐ All PDAs use canonical bump (`bump` in Anchor constraints)
3. ☐ No seed collisions between different account types
4. ☐ CPI targets verified (`Program<'info, Token>`)
5. ☐ Signer checks on all privileged operations
6. ☐ Token program ID pinned (not user-provided)
7. ☐ Mint/freeze authority verified
8. ☐ Account close destinations verified
9. ☐ Checked arithmetic (no unchecked in release builds)
10. ☐ Oracle staleness + confidence + status validated
11. ☐ No sensitive data in logs or error messages
12. ☐ Upgrade authority secured (multisig or frozen)
13. ☐ Oracle feed composition enforces unit normalization + price sanity range
14. ☐ Keeper keypair is NOT the stake/treasury withdrawal authority (principle of least privilege)
15. ☐ Stake accounts split into sub-accounts (no single monolithic stake)
16. ☐ Dependency audit: `bytes`, `libcrux-psq`, `libcrux-ecdh` pinned to patched versions in Cargo.lock
17. ☐ Audit scope exclusions tracked as open backlog items (never ship with known-excluded vectors)
18. ☐ Transitive dependency review enforced (`cargo tree --locked`) + newly published crate quarantine window for keeper builds
19. ☐ ZK verifier integrations pin verification-key hash/circuit version and enforce canary-proof checks on upgrades

## Third-Party Staking Provider Authority Risk (Cross-Customer Blast Radius)

### Provider-API-to-Multi-Platform Authority Hijack (SwissBorg/Kiln, Sep 2025)
Staking providers (Kiln, Figment, Blockdaemon etc.) that hold `StakeAuthority`+`WithdrawAuthority` on behalf of multiple DeFi clients create a **cross-customer blast radius**. Compromise of the provider's central API → all clients' stake accounts simultaneously exposed.

**Solana on-chain mechanics**: `StakeAuthorize` instruction requires only current-authority signature. No program code. Indistinguishable from legitimate ops on-chain.

**Attack timeline**: Authority transfer (instant) → stake deactivation → 1 epoch cooldown (~2–2.5 days) → withdrawal.

**Microstable-specific risk**: LOW for core protocol (no third-party staking custodian). ELEVATED if LST collateral is added whose backing depends on a centralized provider API.

**Red-team application**:
- When evaluating new LST collateral: enumerate whose API holds stake/withdraw authority for that LST's backing validators.
- If a third-party custodian holds multi-customer authority: model a cascade attack on that custodian to assess collateral safety.

**Mitigation**:
1. Require LST collateral integration docs to detail staking authority model.
2. Prefer LSTs backed by validator networks using distributed or hardware-secured authority.
3. Apply additional haircut to LST collateral with known-centralized custodian authority.
4. Track known providers and their authority architecture in a curated registry.

**Sources**: SwissBorg/Kiln (Sep 2025, $41.5M); infstones.com (Feb 2026)

## Solana-Specific Defense Checklist Update
20. ☐ LST collateral staking authority model audited (no single-custodian blast radius)
21. ☐ crates.io ecosystem namespace provenance check before adding new DeFi SDK dependencies (CI + manual review)

## Anchor Post-CPI Stale Account Cache (A42)

### Mechanism
Anchor `Account<'info, T>` deserializes PDA data once at instruction entry. If a subsequent CPI modifies that PDA on-chain (e.g., via Token-2022 transfer hook), the in-memory Rust struct remains stale. Reads from the struct post-CPI yield pre-CPI values.

```rust
// VULNERABLE: no reload after CPI that may modify vault
let price = ctx.accounts.vault.price;           // cached at entry
token_2022::transfer_checked(cpi_ctx, amount)?; // hook may write vault.price
let minted = collateral * price / SCALE;        // uses stale pre-hook price!

// SAFE: reload after CPI
token_2022::transfer_checked(cpi_ctx, amount)?;
ctx.accounts.vault.reload()?;                   // re-fetch from on-chain bytes
let price = ctx.accounts.vault.price;
```

**Trigger condition**: Any CPI (transfer, callback, hook) that writes to an account that the outer program also reads.

**Microstable risk**: LOW currently (SPL Token classic — no hooks). HIGH if any collateral migrates to Token-2022 with transfer hooks.

**Source**: https://blog.asymmetric.re/invocation-security-navigating-vulnerabilities-in-solana-cpis/

## ACE Fairness / Keeper Oracle-Freshness Ordering (B40)

### Mechanism
Solana's Alpenglow/ACE execution model reduces priority-fee-based ordering advantage. Keeper oracle-update TXs no longer predictably precede user mint/redeem TXs under congestion. Protocols that rely on keeper ordering guarantees face increased staleness windows.

**Microstable defense**: `MINT_ORACLE_STALENESS_MAX = 20 slots` is the guard. Under ACE congestion, keeper cycle may exceed 20 slots → OracleDegraded → liveness degradation (not value extraction).

**Mitigation**: Redundant keeper on second node; pre-benchmark keeper latency under ACE congestion scenarios.

**Source**: Blockdaemon Solana 2026 Technical Roadmap (2026-02-19)

## Commit/Reveal Threshold Segmentation Bypass (A43)

### Mechanism
Protocols with `if turnover >= threshold { require_commit_reveal() }` can be bypassed by splitting one large operation into multiple sub-threshold calls. Cumulative effect equals the large operation; commit/reveal delay is never triggered.

```rust
// Per-call check only (BYPASSABLE via segmentation):
if turnover >= LARGE_THRESHOLD { verify_commit_reveal()?; }

// Fix: add cumulative epoch tracking
if turnover >= LARGE_THRESHOLD
    || epoch_drift + turnover >= LARGE_THRESHOLD {
    verify_commit_reveal()?;
}
```

**Microstable specifics**: WEIGHT_STEP_LIMIT=2%, LARGE_THRESHOLD=4%, BATCH_WINDOW_SLOTS=32. 5 calls × 32 slots = 160 slots to zero any collateral weight.

**Requires**: 2-of-3 keeper compromise. Eliminates commit/reveal MEV-protection once keepers are compromised.

## Solana-Specific Defense Checklist Update
22. ☐ Post-CPI `.reload()` called on any PDA that a CPI hook may have modified (mandatory for Token-2022 integration)
23. ☐ ACE/Alpenglow ordering impact assessed for keeper oracle-freshness model; redundant keeper runner in place
24. ☐ Commit/reveal threshold checks include cumulative epoch drift (not per-call only)

### Utility-Impersonating Env-Stealer Crate (A44, RUSTSEC-2026-0030)
Fresh-named malicious crate (not a typosquat) added as a direct dependency that silently exfiltrates `.env` files via HTTP POST at build or init time. Distinct from Typosquat Waves and Transitive Payload Relay (D33).

**Microstable keeper specific attack path**:
1. Keeper's `Cargo.toml` gains a new crate added via social engineering or compromised PR.
2. `cargo build` runs on MiniPC (`/home/spritz/microstable-keeper/`); crate reads `.env` at same path.
3. `DEFAULT_KEEPER_ENV_PATH = "/home/spritz/microstable-keeper/.env"` — signing key exfiltrated.
4. Attacker issues malicious oracle/rebalance/circuit-breaker transactions with the leaked keypair.

**Defense (Solana keeper specific)**:
- Strict crate allowlist in `cargo deny` (`[bans]` section); reject any unlisted crate.
- `cargo audit --deny` in CI + `cargo deny check bans` pre-build gate.
- Run `cargo build` in a sandboxed environment with NO access to the production `.env` path (Docker/nsjail with `/home/spritz/microstable-keeper/.env` not bind-mounted).
- Move signing key out of `.env` into a hardware signer or remote KMS; no plaintext key at build path.
- Enforce mandatory >7-day quarantine window before any new crate is permitted in the production build.

**Sources**:
- RUSTSEC-2026-0030: https://rustsec.org/advisories/RUSTSEC-2026-0030.html
