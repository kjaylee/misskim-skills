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

### Solana SDK Supply Chain Takeover (NPM Trusted Tooling)
GHSA-8f57-hh49-gmqf (2026-03-26) reported malicious behavior in `@solana-ipfs/sdk` (`>=0` vulnerable, first patched version: none): any computer using it should be considered fully compromised; all local secrets should rotate from a clean machine. This is a high-risk **off-protocol**, yet protocol-relevant risk because Solana JS tooling and infra scripts are part of the signing/operations trust boundary.

**Solana-specific risk**:
- A single compromised SDK in local/off-chain tooling can leak KMS/env credentials, RPC private keys, wallet seed material, or keeper operator tokens before a tx reaches chain.
- Impact is often non-deterministic: uninstalling package rarely fully restores trust because prior process execution may have dropped persistent payloads.
- Even if protocol code is clean, operational compromise can authorize privileged keeper actions, oracle feed tampering, or signing abuse.

**Mitigation**:
- Freeze/add to denylist any dependency with advisory `ghsa_id` from GitHub Advisory DB unless explicit exception signed by security owner.
- Keep tooling dependency allowlist with 2-person change gate + 7-day quarantine for newly published versions.
- Use separate ephemeral CI/runner host for any Solana JS tooling that touches signing material; rotate and attest credentials after package alerts.
- Add CI policy that blocks dependency install if `npm` package has security advisory severity ≥ HIGH and no patched version unless exception.

**Source**: https://api.github.com/advisories/GHSA-8f57-hh49-gmqf

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

### Campaign-Clone Env-Stealer Rotation (A45, RustSec 0031/0032)
After `time_calibrator` takedown, near-clone crates (`time_calibrators`, `dnp3times`) appeared within hours with the same `.env` exfiltration objective and fake `timeapi.io`-style endpoint theme.

**Solana keeper-specific risk**:
- Incident response often adds/changes utility crates quickly under uptime pressure.
- Name-level denylisting (`block time_calibrator`) is too narrow; next clone passes unless policy is campaign-wide.
- Cargo.lock attestation remains green if the malicious clone is intentionally merged and hash is re-attested.

**Mitigation upgrade**:
1. Security quarantine: reject newly published crates (<7 days) for keeper builds unless emergency waiver + dual review.
2. Campaign-level deny rule: when one malicious crate is confirmed, block semantic siblings (`time*`, `slot*`, `rpc*`) until manual clearance.
3. CI static scan for outbound HTTP/file-read in `build.rs` and global initializers of new crates.
4. Maintainer trust gate: require minimum maintainer age/history for newly added dependencies.

**Sources**:
- https://rustsec.org/advisories/RUSTSEC-2026-0031.html
- https://rustsec.org/advisories/RUSTSEC-2026-0032.html

### Solana Leader-Isolation / Stopping Liveness Attack (B47)
New comparative research (`arXiv:2603.02661`) identifies Solana as vulnerable to leader-isolation and stopping attacks under adversarial communication conditions.

**Solana-specific risk to protocol operators**:
- Deterministic leader schedule enables targeted pre-slot disruption of expected leaders.
- Even with honest keepers/oracles, slot progression/finality lag can push protocol freshness gates into repeated fail-closed mode.
- Availability degradation can cascade into rebalance delay, watchdog churn, and user-facing mint/redeem rejection spikes.

**Mitigation**:
1. Add leader-isolation chaos drills to ops runbook (targeted packet loss around known leader windows).
2. Track chain-liveness SLOs (`finalized slot lag`, `slot production continuity`) separately from RPC endpoint health checks.
3. Define explicit degraded-mode behavior (safe pause + operator escalation) when liveness SLO breaches persist.
4. Keep geographically/network-diverse keeper runners to reduce correlated path disruption.

**Source**: https://arxiv.org/abs/2603.02661

## Solana-Specific Defense Checklist Update
25. ☐ Dependency policy handles campaign-level clone waves (semantic sibling block + new-crate quarantine)
26. ☐ Leader-isolation/stopping chaos tests executed and linked to oracle freshness SLO alarms

### RPC Proxy HTTP Request Smuggling (D35, RUSTSEC-2026-0033)
Cloudflare `pingora-core` <0.8.0 allows HTTP request smuggling via premature Upgrade handling. CVSS 9.3 CRITICAL.

**Solana keeper-specific risk**:
- Microstable keeper does NOT directly depend on pingora-core (confirmed via Cargo.lock scan).
- However, if any RPC endpoint, oracle feed relay, or internal API used by the keeper is fronted by a Cloudflare/Pingora proxy (as documented in TOOLS.md: GCP VM 34.19.69.41 + Cloudflare), an unpatched proxy instance exposes internal services to request smuggling that bypasses WAF and IP allowlist controls.
- JSON-RPC over HTTPS has no valid use case for the `Upgrade` header — any Upgrade-bearing request to an RPC proxy should be considered anomalous and rejected.

**Mitigation**:
1. Patch all `pingora-core` deployments to >=0.8.0 (CVE-2026-2833).
2. Configure proxy/WAF to strip `Upgrade` and `Connection` headers for all RPC-bound routes.
3. Verify Cloudflare CDN edge is on patched Pingora for all keeper/oracle traffic paths.
4. Add chain-infra monitoring rule: alert on `Upgrade` headers observed in RPC request logs.
5. Migrate critical keeper↔RPC connections to HTTP/2 where possible.

**Defense Checklist Item**:
27. ☐ All proxy layers in RPC/oracle traffic path use pingora-core ≥0.8.0 or HTTP/2 (CVE-2026-2833 defense)

**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0033 | https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-2833

### ZK Trusted Setup Misconfiguration Future Watch (A49)
Microstable is currently Solana-native with no ZK components. However, if ZK proof integration is ever planned (private transactions, ZK oracle attestation, ZK governance proofs):

**Solana-specific ZK risks**:
- Solana's `zk-token` (SPL Token Confidential Transfers) uses BulletProofs, not Groth16 — different trusted setup model, but same class of ceremony verification requirement.
- Any custom Groth16 verifier implemented as a Solana program (on-chain verification) must have its verifying key cross-checked against the ceremony transcript.
- Program-level verifying key storage (as PDA data or hardcoded constants) can be inspected on-chain — publish and verify before deployment.

**Defense Checklist Item**:
28. ☐ If any ZK proof verifier is introduced: third-party ceremony verification (gamma2 ≠ delta2, correct circuit hash, Powers of Tau transcript) completed BEFORE deployment

**Source**: https://rekt.news/the-unfinished-proof | https://blog.zksecurity.xyz/posts/groth16-setup-exploit/

## Token-2022 Hook Security Patterns (2026 Addition)

### A51. ExtraAccountMetaList Account Injection (Transfer Hook Context Confusion)
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03)

Token-2022 transfer hooks receive additional accounts via `ExtraAccountMetaList`. If the hook program doesn't validate that these accounts match expected PDA seeds, an attacker can inject a malicious account (e.g., spoofed whitelist) to bypass transfer logic.

**Code pattern to find**:
```rust
// VULNERABLE: ExtraAccountMetaList account accepted without seed verification
fn execute_hook(ctx: Context<HookCtx>) -> Result<()> {
    require!(ctx.accounts.whitelist.allowed, ErrorCode::Blocked);  // attacker-supplied → always true
}

// SAFE: derive and verify PDA address before trusting account data
fn execute_hook(ctx: Context<HookCtx>) -> Result<()> {
    let (expected, _) = Pubkey::find_program_address(
        &[b"whitelist", ctx.accounts.mint.key().as_ref()],
        ctx.program_id,
    );
    require_keys_eq!(ctx.accounts.whitelist.key(), expected, ErrorCode::InvalidAccount);
    require!(ctx.accounts.whitelist.allowed, ErrorCode::Blocked);
}
```

**Microstable risk**: LOW (SPL Token classic, no hooks). HIGH if Token-2022 migration.

**Secondary: Confidential Transfer Auditor Key**: If `auditor_elgamal_pubkey` ≠ `[0u8; 32]`, auditor can decrypt all confidential balances — compliance backdoor. Explicitly disable unless required.

**Mitigation**:
1. Anchor `seeds` + `bump` constraints on ALL hook context accounts (no exceptions)
2. Explicitly set `auditor_elgamal_pubkey = None` in Confidential Transfer config
3. Include hook account seed validation in Token-2022 audit checklist

### A52. Transfer Hook Infinite Recursion Griefing (Asset Freeze DoS)
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03)

If a transfer hook triggers a CPI that transfers the *same mint*, the runtime invokes the hook again — recursive chain. Runtime halts with compute budget exceeded → every transfer of that mint reverts → asset freeze DoS.

**Microstable risk**: LOW currently. HIGH risk if Token-2022 mints are used.

**Attack surface**: Protocols that accept user-supplied Token-2022 collateral with user-controlled hooks.

**Mitigation**:
1. **Acyclicity invariant**: hook must never initiate a transfer of the same mint (prove mathematically, not just code-review)
2. Freeze hook upgrade authority post-deployment
3. Reject collateral mints with mutable hook authority or unverified hook acyclicity

## Firedancer Finality Patterns (2026 Addition)

### B50. Skip-Vote Structural Finality Lag
**Signal**: Zealynx Security Blog "Solana Smart Contract Audit Guide 2026" (2026-03); Solana SIMD-0370

Under Firedancer dynamic block sizing, validators running Agave or older hardware may skip voting on oversized blocks → structural finality delay. During the lag window, transactions may appear "on-chain" but not finalized — creating a micro-reorg risk window for finality-dependent operations.

**Distinct from B40**: B40 is about TX ordering (ACE fairness). B50 is about finality *timing* from heterogeneous validator hardware.
**Distinct from B47**: B47 requires an adversary targeting leaders. B50 is structural (no adversary needed).

**Microstable-specific risk**:
- Slot-based staleness guards (`STALE_ORACLE_PENALTY_PER_SLOT`, `Clock::get()?.slot`) are NOT directly affected (slots advance continuously)
- `Confirmed` commitment (keeper default) has a skip-vote micro-reorg window
- If bridge/large-withdrawal instructions using `Finalized` are added, they face unexpected latency

**Pattern to detect**:
```rust
// RISKY: hard-coded 400ms finality assumption
let deadline = current_slot + 1;  // assumes 400ms = finalized → no longer holds under Firedancer

// SAFER: use slot range with skip-vote buffer
let deadline = current_slot + 3;  // +2–3 slot buffer for heterogeneous validator lag
// AND: require Finalized commitment for irrevocable operations
```

**Mitigation**:
1. Use `Finalized` commitment for all irrevocable/large-value keeper operations
2. Add +2–3 slot slack to any deadline calculation assuming 400ms finality
3. Monitor `confirmed → finalized` slot delta in keeper telemetry; alert if > 3 slots

## Solana-Specific Defense Checklist Update
29. ☐ Token-2022 hooks: all ExtraAccountMetaList accounts verified via seed derivation (not caller-supplied)
30. ☐ Token-2022 hooks: acyclicity proven (no same-mint CPI transfer within hook); hook upgrade authority frozen
31. ☐ Firedancer skip-vote buffer: irrevocable operations use `Finalized` commitment; deadline calculations include +2–3 slot slack

---

## Firedancer Write-Lock LDoS — Single Global PDA Starvation (B64, 2026-03-16)

**Signal**: DreamWork Security (dev.to, 2026-03-13). New attack class specific to Firedancer era throughput.

**Pattern**: Protocols with a single monolithic global state PDA required for all writes are vulnerable to targeted write-lock flooding. An attacker submits high-priority-fee minimal-compute TXs write-locking the PDA. Firedancer's higher block density means more competing lock TXs per slot. Legitimate operations (oracle updates, liquidations) are starved.

```rust
// VULNERABLE ARCHITECTURE: single PDA for all writes
pub protocol_state: Account<'info, ProtocolState>,  // appears in every instruction context

// ATTACK: 10,000 TXs/slot each requesting write lock on protocol_state
// → oracle update keeper TX queued behind attacker flood
// → staleness accumulates → circuit breaker or hard halt
```

**Solana-specific checklist additions**:
32. ☐ Identify all global-state PDAs required as `writable` in critical paths (oracle update, liquidation)
33. ☐ For each global-state PDA: assess write-lock LDoS cost/impact ratio (if one account blocks all operations, HIGH risk)
34. ☐ Keeper priority fee strategy: dynamic fee escalation on write-lock contention (not fixed priority fee)
35. ☐ Graceful degradation: if oracle update blocked N consecutive slots, switch to TWAP-only mode (not hard halt)

---

## Firedancer Dense-Block Intra-Slot Oracle Staleness (B65, 2026-03-16)

**Signal**: DreamWork Security (dev.to, 2026-03-13). Extends oracle staleness analysis to intra-slot dense-block scenarios.

**Pattern**: Slot-number-based staleness checks pass when oracle was updated in the same slot as the attacker TX (`slots_since_oracle = 0`). In a Firedancer dense block, price may move significantly between oracle update and attacker TX within the same slot.

```rust
// CHECK THAT MAY BE INSUFFICIENT in dense Firedancer slots:
let slots_since_oracle = current_slot - oracle.last_update_slot;
require!(slots_since_oracle <= MAX, OracleStale);
// → passes even if oracle.publish_time is 200ms ago and price moved 1%

// IMPROVED: add publish_time check
let time_since_oracle = Clock::get()?.unix_timestamp - oracle.publish_time;
require!(time_since_oracle <= MAX_SECONDS, OracleStale);
```

**Solana-specific checklist additions**:
36. ☐ Oracle staleness: verify both `slot` check AND `publish_time` (Unix timestamp) check are in place
37. ☐ Dense-slot scenario: confirm Pyth confidence interval check rejects when confidence > threshold regardless of slot match
38. ☐ TWAP deviation guard covers intra-slot divergence (not only cross-slot TWAP smoothing)

---

## Glassworm C2 via Solana Accounts (D39, 2026-03-17)

**Pattern**: Attackers use Solana accounts as a censorship-resistant, anonymous command-and-control channel for supply-chain payloads. This makes Glassworm-class malware invisible to traditional network security tools.

**Why Solana is an ideal C2**:
- Accounts are permanent — no takedown mechanism
- Reads are free and unlimited — no detection via rate-limit triggers
- IP logs: Solana RPC endpoints do not log per-client request origin
- Security scanners that flag suspicious HTTP C2 domains are blind to `api.mainnet-beta.solana.com` (legitimate DeFi infrastructure)

**Detection**: Monitor for unusual Solana RPC calls (especially `getAccountInfo`) originating from developer workstation JS processes or CI environments that are NOT the keeper binary. Network-layer: alert on `getAccountInfo` calls to unknown pubkeys from non-keeper processes.

**Solana protocol implication**: Any future Microstable feature that reads arbitrary user-supplied pubkeys via `getAccountInfo` should treat the returned data as untrusted external input — never `eval()` or interpret as code.

## B50 Reinforcement — Cross-Chain Bridge Finality Lag Attack (2026-03-17)

**Operational detail added**: Firedancer skip-vote finality lag creates a concrete **bridge double-spend window**:
1. Attacker submits deposit transaction in a large Firedancer-produced block (causes Agave skip-votes)
2. Cross-chain bridge sees *block inclusion* → releases funds on destination chain
3. Firedancer block finality is delayed → in edge case, block may be skipped entirely
4. Attacker received destination-chain funds for a deposit that never finalized on Solana

**Key**: No adversarial leader needed (distinct from B47). Normal Firedancer operation under heterogeneous validator hardware is sufficient.

**Solana-specific mitigation for bridge/cross-chain integrations**:
- Require `Finalized` commitment (not `Confirmed`) before any fund release
- Add +2–3 slot buffer on all deadline calculations
- Monitor `confirmed→finalized` delta: alert if >5 slots

## D45 — Solana Blockchain-as-C2 Channel (2026-03-20)

**Operational specifics for Solana DeFi environments:**

The Windsurf IDE malware (Bitdefender, March 20, 2026) established a critical precedent: Solana's **public read API is weaponizable as a censorship-resistant C2 channel** because:
1. `getTransaction(sig)` is unauthenticated and free on mainnet
2. Transaction `memo` and instruction data fields can store arbitrary bytes
3. Encrypted payload fragments survive indefinitely (blockchain immutability)
4. Attacker deploys C2 payload once; any infected client retrieves it forever

**Solana-specific attack surface for keeper infrastructure:**
- Default keypair location `~/.config/solana/*.json` is world-readable by default on many Unix systems
- `solana config get` reveals keypair path; if process inspector runs on same machine, path is trivially found
- Keeper `config.toml` RPC keys (Helius, QuickNode, Triton) are stored in plaintext in typical deployments

**Detection heuristics for Solana C2:**
- Non-keeper processes (e.g., `node`, extension workers, `.vsix` processes) making bulk `getTransaction` calls to mainnet
- `getTransaction` calls targeting old/unknown transaction signatures (not recent keeper TXs)
- High-frequency `getTransaction` to signatures that are not in the keeper's own TX log

---
<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-22 -->

## Token-2022 Extension Attack Patterns (2026-03-22)

### ExtraAccountMeta Injection (A56)
Transfer hooks receive extra accounts via `ExtraAccountMetaList` PDA at `seeds = [b"extra-account-metas", mint_pubkey]`. Protocol or hook program must re-derive and verify these PDAs — never trust them without seed validation.

### Transfer Fee Invisible Tax (A58)
Token-2022 fee extension deducts fee at protocol level. Protocols crediting `amount` (sent) instead of `post_balance - pre_balance` (received) are undercollateralized by the fee rate on every deposit.

### Anchor v1.0.0 Shadow Migration (A57 — current Solana Anchor ecosystem)
Anchor v1.0.0-rc.5 released 2026-03-20. Programs on Anchor 0.31.x face silent discriminator mismatch if off-chain tools migrate to v1.x before on-chain program compatibility is verified. Pin keeper Cargo.lock and add CI version-parity gate.

## 2026-03-23 New Patterns

### CPI Signer Authority Forwarding (Extended — see A70)
The brief entry under "Signer Privilege Escalation" is reinforced with a full attack vector.
Key addition: **DeFi aggregators/routers** are the primary risk surface. When a protocol acts as a router between user and external DEX:
- If the external DEX program account is passed as `AccountInfo` (not `Program<T>`), an attacker can substitute a malicious program.
- The malicious program receives `is_signer = true` for the user's account.
- It can use this to drain any account the user has authority over.
**Safe pattern**: user transfers to protocol vault first (user signs → your program), then protocol CPIs to DEX using PDA only. User signing authority never crosses into external program.

### Solana ACE (Application-Controlled Execution) Bypass Surface
**Status**: Emerging (2026-03-19, Chainstack Solana MEV 2026 analysis).
Solana's evolving ACE (Application-Controlled Execution) system lets dApps define execution constraints: ordering, slippage bounds, actor whitelists. Jito BAM (Blockspace Auction Mechanism) is the complementary infrastructure.
**Risk pattern**:
1. If ACE constraints are enforced at the application layer only (not runtime-enforced), an attacker can submit transactions that bypass the application's constraint-checking path (e.g., calling the program directly rather than through the ACE-gated interface).
2. BAM priority fee griefing: if an attacker pays enough priority in Jito BAM, they can reorder transactions relative to ACE-gated operations, potentially front-running within a bundle.
3. ACE constraint specification bugs: if the constraint language allows ambiguous expressions, edge cases may evaluate to "unconstrained" — effectively disabling the protection.
**Mitigation**: ACE constraints should be enforced on-chain (program-level checks), not merely off-chain (interface-level checks). Never rely on ACE as the sole protection against reordering or sandwiching.
**Microstable relevance**: LOW — does not currently use ACE. Monitor if implementing Jito bundles for keeper.

<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-24 -->

## 2026-03-24 Patterns

### tar-rs Supply Chain CI/CD Attack (A74)
Keeper Rust build pipelines using tar-rs ≤ 0.4.44 are vulnerable to:
1. **RUSTSEC-2026-0067** (CVE-2026-33056): `unpack_in` follows symlinks via `fs::metadata()` → crafted tarball can chmod keeper key directories to 0777.
2. **RUSTSEC-2026-0068**: PAX size header silently ignored when header size nonzero → crafted entries bypass size-based validation.

**Mitigation**: Pin `tar = ">=0.4.45"` in keeper Cargo.toml; run `cargo audit` in CI.

### Audit-Evading Economic Exploit Architecture (A75)
Exploitation of the gap between "technically correct code" and "economically safe protocol":
- All individual instructions are technically correct; no audit finding can be raised
- Multi-transaction oracle manipulation + deposit + mint + price-restore + withdraw sequence crosses audit scope boundary
- Detection: for every oracle-price-dependent function, enumerate the profit path when price deviates N%
- For MANUAL_ORACLE_MODE protocols: on-chain TWAP sanity gate is mandatory (reject writes > ±2% from TWAP)

**Microstable-specific gap**: `write_oracle_price` in MANUAL_ORACLE_MODE has no TWAP deviation cap on-chain. Add `MAX_MANUAL_PRICE_DEVIATION = 200bps` constant + pre-write check.

<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-25 -->

## 2026-03-25 Patterns

### rustls-webpki CRL Bypass in Keeper TLS (A77)
**Confirmed Keeper Exposure**: Cargo.lock has `rustls-webpki = "0.103.9"` (fix is `>=0.103.10`).

Attack scenario:
1. RPC provider (Helius/QuickNode/Triton) rotates TLS cert; old cert revoked via CRL with multiple distributionPoints
2. rustls-webpki 0.103.9 only checks first DP → subsequent DPs ignored → revocation status "unknown"
3. If keeper's rustls uses `UnknownStatusPolicy::Allow` → accepts revoked cert → MITM possible
4. Attacker intercepts keeper→RPC connection → injects malicious oracle price responses or suppresses circuit breaker TX

**Remediation**:
```bash
# In microstable/solana/ workspace:
cargo update -p rustls-webpki --precise 0.103.10
cargo update -p reqwest  # may pull in updated webpki transitively
cargo audit  # verify clean
```

### HPKE Nonce Reuse Attack Class (A76) — Future Risk
If any future Microstable component uses hpke-rs for keeper↔oracle or keeper↔relayer secure messaging:
- hpke-rs ≤ 0.5.x: u32 nonce counter wraps at 2^32 → nonce reuse → full message decryption possible
- Companion: X25519 non-contributive DH (RUSTSEC-2026-0072) → weak shared secret accepted
- Preemptive rule: any future HPKE adoption must pin hpke-rs ≥ 0.6.0 from day 1

---
*(2026-03-26 Red Team Evolution: A81 + A82)*

### Quinn QUIC Validator Infrastructure Attack Class (A81)
- RustSec advisory in Quinn (Agave's QUIC transport library) — publicly disclosed March 2026 without private coordination.
- Remote process crash of Agave validators, no authentication required.
- Attack amplification: crash targeted honest validators → skew stake-weighted block production in attacker's favor during window before community upgrades.
- Microstable indirect risk: keeper RPC relies on Agave nodes. During validator crash event, all 3 default RPC endpoints may degrade simultaneously.
- **Defense requirement**: keeper must have ≥ 3 geographically-distributed RPC fallbacks. Retry-on-503 logic must be confirmed in keeper code. Alert if all RPCs fail simultaneously.

### Solana Blockchain as C2 Transport — Developer Targeting (A82)
- Confirmed attack campaign (Bitdefender, March 2026): malicious IDE extension uses Solana on-chain transaction data as payload delivery channel.
- Bypasses traditional C2 detection because traffic is indistinguishable from legitimate Solana network traffic.
- Target profile: Solana developers (Rust/Anchor/TS) — exactly the Microstable developer persona.
- Highest-value exfiltration from a Microstable developer machine:
  1. Anchor upgrade authority keypair (wallet.json / id.json)
  2. Keeper hot wallet seed phrase
  3. Helius/QuickNode/Pyth API keys
  4. AWS IAM credentials (CI/CD pipeline)
- **Mandatory mitigations for Microstable team**:
  1. IDE extension allowlist policy on all machines with keeper/deploy key access
  2. Anchor deploy keys in hardware wallet (Ledger) — never flat file on dev machine
  3. Keeper hot wallet: HSM or at minimum OS keychain, never plaintext .env
  4. API keys: 1Password / environment injection at runtime, never committed
  5. Rotate all secrets if any team member's machine shows unexpected Solana RPC traffic

## 2026-03-27 Patterns

### libcrux-ml-dsa Signature Verification Faults (A83)
- **RUSTSEC-2026-0076 (HIGH)**: malformed ML-DSA signature hints can trigger an out-of-bounds read during verification, producing panic-based remote DoS when verification service accepts attacker-controlled serialized signatures.
- **RUSTSEC-2026-0077 (HIGH)**: ML-DSA signer response norm check incorrectly validated, allowing malformed signatures to pass verification in some paths (integrity policy break).
- **Microstable relevance**: no `libcrux-ml-dsa` in `microstable/solana/Cargo.lock` today; attack is **latent**.
- **If adopted in keeper or program**: blocklist versions `<0.0.8` and require explicit fuzz tests for invalid/oversized hint cases.

### libcrux-sha3 Incremental SHAKE Discrepancy (A84)
- **RUSTSEC-2026-0074**: `libcrux-sha3` incremental `portable::incremental::Shake*::squeeze` dropped first output block when output exceeds RATE size.
- **Impact**: deterministic output mismatch / entropy drift in protocols that rely on long-output XOF streams.
- **Microstable relevance**: no `libcrux-sha3` dependency today; no direct exploit path.
- **Future migration guard**: require `libcrux-sha3 >= 0.0.8` for any PQ hashing/KEM rollout.

---


<!-- AUTO-ADDED BY REDTEAM DAILY EVOLUTION 2026-03-28 -->

## 2026-03-28 Patterns

### libcrux-poly1305 Standalone MAC Unauthenticated Panic (A85)
- **RUSTSEC-2026-0073 (HIGH, CVSS 8.7)**: incorrect constant for key length in `libcrux-poly1305` causes `libcrux_poly1305::mac` to always panic with out-of-bounds memory access.
- **Attack surface**: any service exposing a code path that calls `libcrux_poly1305::mac` with attacker-controlled input. Network-reachable, no authentication required (AV:N/AC:L/AT:N/PR:N/UI:N).
- **Scope boundary**: standalone MAC use only. `libcrux-chacha20poly1305` (AEAD) is **unaffected** — the vulnerability is isolated to the standalone MAC API, not the AEAD composition.
- **Patched**: `libcrux-poly1305 >= 0.0.5`
- **Microstable relevance**: no `libcrux-poly1305` dependency in Cargo.lock today; attack is **LATENT**.
- **Sibling cluster**: A83 (libcrux-ml-dsa), A84 (libcrux-sha3), A85 (libcrux-poly1305) — all `libcrux` PQ/crypto primitives advisory batch (2026-03-24). The cluster pattern suggests the libcrux library is undergoing broad security audit; expect additional advisories.
- **Future migration guard**: if any libcrux-* crate is introduced, verify advisory status for ALL libcrux-* sibling crates, not just the directly imported one. Pin to advisory-clean versions at adoption time.
- **Source**: https://rustsec.org/advisories/RUSTSEC-2026-0073.html | https://github.com/cryspen/libcrux/pull/1351

### Coordinated Mass-Deployment Malicious Crate Wave — Crypto Ecosystem Targeting (A86)
- **Signal**: 2026-03-26, RustSec batch removal of 20+ malicious crates in a single day; crate names include crypto/DeFi/trading targets: `monero-rpc-rs`, `monero-api`, `acceptxmr-rs` (Monero payment processor), `lfest-main` (trading framework), alongside Windows-ecosystem cloaks (`registry-win`, `win-crypto`, `windows-service-rs`, `openvpn-plugin-rs`, `win-base64-rs`, `winx-rs`, `lasso-rs`, `tauri-winrt-notifications`).
- **Attack pattern — carpet-bomb multi-vector**:
  1. Attacker registers 20+ crates simultaneously under different categories (crypto-utility, OS-wrapper, UI)
  2. Crates are dormant or functional for weeks; legitimate installs accumulate
  3. Malicious payload activates at a trigger time (e.g., specific date, environment variable) or exfiltrates continuously
  4. All crates are taken down in a coordinated wave — but any developer who installed during the active window is compromised
  5. **Key asymmetry**: crate-by-crate deny-listing is too slow; the attacker deploys faster than defenders remove
- **Why distinct from A44 (single direct-dep env-stealer)**: A44 is a targeted, single-crate injection aimed at one ecosystem. A86 is a carpet-bomb deployment across multiple package categories simultaneously — scale and cross-ecosystem targeting are the novel elements.
- **Why distinct from A45 (campaign-clone rotation)**: A45 is a reactive pattern (clone appears AFTER original takedown). A86 is a proactive parallel deployment — all clones are live simultaneously.
- **Crypto developer kill chain**: `monero-api` or `lfest-main` added to Solana project → exfiltrates RPC keys, Anchor deploy keypair, `.env` secrets → attacker sends privileged keeper/upgrade transactions with stolen keys.
- **Microstable relevance**: Cargo.lock clean ✅. Risk elevated when: (a) incident-response pressure to add new utility crates quickly, (b) new team members or contractors add dependencies without full review.
- **Mitigation upgrade** (extends A44/A45 defenses):
  1. Campaign-level detection: when 5+ crates are removed in one day in any registry, trigger immediate full Cargo dependency audit across ALL projects
  2. Category quarantine: if one crypto-adjacent crate is flagged malicious, quarantine the entire semantic cluster (Monero-related, trading-related, Windows-adjacent) for 7 days pending review
  3. Install telemetry: log ALL `cargo install`/`cargo build` events with new crate additions (date, crate name, version, maintainer age) — alert on any new crate <30 days old
  4. Out-of-band maintainer verification: for any DeFi-adjacent crate (matching name contains: monero, btc, eth, sol, defi, trade, crypto), require direct GitHub-verified maintainer identity check before allowlist approval
- **Source**: https://rustsec.org/advisories/ (batch, 2026-03-26)

### Solana-Specific Defense Checklist Update
39. ☐ libcrux-* adoption: full advisory check across ALL sibling crates (not just the directly imported one) before adoption
40. ☐ Registry mass-removal detection: CI/toolchain monitors crates.io security events; 5+ removals/day triggers immediate full Cargo audit

---
<!-- AUTO-ADDED 2026-03-29 (Red Team Daily Evolution) — A87~A90 Solana/Anchor-relevant patterns -->

## 2026-03-29 New Pattern Additions

### A87 — Groth16 Trusted Setup Ceremony Skip (ZK circuits on Solana/Anchor)
- **Solana context**: While mainstream Solana programs do not use Groth16 ZK proofs directly, Solana's ZK Token standard (Confidential Transfers in Token-2022) uses ElGamal + range proofs. Any custom Solana program integrating a Groth16 ZK verifier (via a Solana-native ZK VM or off-chain verifier contract) faces this attack surface.
- **Future risk trigger**: If Microstable adds confidential transfer support or a ZK proof-based compliance feature, mandatory ceremony verification must be part of the deployment checklist.
- **Detection command**: For any `verification_key.json`, verify `gamma_g2 != [G2_GENERATOR_X, G2_GENERATOR_Y]`. If equal → ceremony was not completed.
- **Checklist item 41**: ☐ Any ZK verifier deployed to Solana/Anchor must provide ceremony transcript with ≥ 1 external contributor. Verify `snarkjs zkey verify` output before deploy.

### A88 — Token-2022 TransferHook CPI Reentrancy (Solana analog of ERC-3525 SFT reentrancy)
- **Solana context**: SPL Token-2022 `TransferHook` extension fires an additional CPI instruction during every transfer. If the hook's target program re-enters the calling instruction before all accounts are finalized:
  - Balances, supply counters, or position states can be read mid-update (stale).
  - The calling program may have transferred tokens (changing ATA balances) but not yet updated its internal state.
  - A malicious hook could trigger a second deposit, borrow, or mint against the pre-update state.
- **Microstable current status**: spl-transfer-hook-interface 0.9.0/0.10.0 in Cargo.lock (transitive dep). No active hook handler in lib.rs. LATENT.
- **Guard pattern for Anchor programs using Token-2022 with TransferHook**:
```rust
// SAFE pattern: update ALL internal state before any SPL transfer that invokes a hook
ctx.accounts.vault.total_deposits = ctx.accounts.vault.total_deposits
    .checked_add(deposit_amount)
    .ok_or(ErrorCode::MathOverflow)?;  // state updated FIRST

// THEN initiate transfer (which will fire TransferHook CPI)
token_2022::transfer_checked(...)?;  // hook fires here against updated state
```
- **Checklist item 42**: ☐ If Token-2022 TransferHook is applied to mSTABLE or any vault collateral token, audit all callers: ensure state updates precede transfer calls (CEI for SPL).

### A89 — Supply Cap Enforcement: Internal Tracker vs. ATA Balance (Solana-Specific)
- **Microstable confirmation (2026-03-29)**: `total_collateral_value()` correctly uses `v.total_deposits` (internal counter). NOT vulnerable to donation attack. ✅ CONFIRMED SAFE.
- **General Solana pattern**: Programs that read `token_account.amount` from a vault ATA as the authoritative deposit counter are vulnerable to donation-bypass. Any `require!(vault_ata.amount <= cap)` check is bypassable by direct SPL token transfer to the ATA.
- **Vulnerable pattern**:
```rust
// VULNERABLE: reads ATA balance directly
let vault_balance = ctx.accounts.vault_ata.amount;
require!(vault_balance <= supply_cap, ErrorCode::SupplyCapExceeded);
```
- **Safe pattern** (what Microstable correctly implements):
```rust
// SAFE: reads internal program-controlled state
let protocol_deposits = ctx.accounts.vault.total_deposits;
require!(protocol_deposits <= supply_cap, ErrorCode::SupplyCapExceeded);
```
- **Checklist item 43**: ☐ Audit ALL supply/collateral caps: verify they read from program-internal state, not raw ATA `token_account.amount`.
- **Multi-horizon monitoring note**: Standard per-slot circuit breakers do not catch 9-month slow accumulation. Add 30-day/90-day rolling concentration alerts.

### A90 — RNG Failure Key Generation Oracle (libcrux-ed25519 / ed25519 Variants)
- **Solana context**: Solana validators and programs use ed25519 signatures. If keeper or validator software uses `libcrux-ed25519 < 0.0.4` for key generation, catastrophic RNG failure → all-zero key → predictable.
- **Keeper key generation risk**: Any Rust binary that generates ed25519 keypairs using libcrux-ed25519 without RNG error handling is vulnerable. Microstable keeper: libcrux-ed25519 NOT present (confirmed). Standard Solana `solana-keygen` uses a different code path.
- **Checklist item 44**: ☐ If any new Rust utility is introduced for Microstable keypair generation, verify: (a) does NOT use libcrux-ed25519 < 0.0.4; (b) always validates generated key != all-zeros before use; (c) uses hardware RNG source (HSM/TPM/TRNG) in production.

### Solana-Specific Defense Checklist Update
41. ☐ ZK verifier deployment: ceremony transcript with ≥1 external contributor + `snarkjs zkey verify` before mainnet deploy
42. ☐ Token-2022 TransferHook callers: CEI ordering enforced — internal state updated BEFORE transfer CPI
43. ☐ Supply cap enforcement: uses program-internal deposit tracker, NOT raw ATA `token_account.amount`
44. ☐ New keypair generation utilities: verify libcrux-ed25519 >= 0.0.4 + non-zero key validation + hardware RNG

---
<!-- AUTO-ADDED 2026-04-03 (Red Team Daily Evolution) — A95~A96 Anchor 1.0 trust-boundary patterns -->

## 2026-04-03 Anchor 1.0 Pattern Additions

### A95 — Anchor `reload()` Owner-Drift Bypass
- **Solana context**: Developers commonly call `.reload()` after CPI to refresh account state. Anchor's 2026 fix shows that, on older versions, `reload()` itself was not a complete trust barrier because owner validation had to be tightened.
- **Attack idea**: A CPI path mutates, closes, or otherwise changes the trust context of an account; the caller then `reload()`s and accepts the new bytes as trusted state without re-asserting owner/business invariants.
- **Why this matters on Solana**: CPI-heavy programs, Token-2022 hook flows, and migration paths frequently depend on post-CPI refresh. Reviewers who know A42 (missing reload) may miss the inverse pattern: reload is present, but still unsafe on older Anchor.
- **Checklist item 45**: ☐ On Anchor `<1.0.0`, every post-CPI `.reload()` must be preceded by an explicit owner assertion and followed by invariant re-checks (seed, mint, authority, status).

### A96 — Duplicate Mutable Account Aliasing
- **Solana context**: Passing the same pubkey into two mutable roles can collapse accounting assumptions even when owner/signer checks all pass.
- **Anchor 1.0 signal**: Default duplicate mutable-account rejection was added because this pattern was repeatedly dangerous in nested, optional, and `remaining_accounts` flows.
- **Audit question**: For every instruction with two or more mutable roles, ask: "what breaks if these two accounts are actually the same pubkey?"
- **Checklist item 46**: ☐ For every pair of mutable roles that must be distinct (`source/destination`, `user/fee vault`, `position_a/position_b`), add `require_keys_neq!` unless the instruction uses explicit `dup` and documents why aliasing is safe.

### Solana-Specific Defense Checklist Update
45. ☐ On Anchor `<1.0.0`, post-CPI `.reload()` requires manual owner assertion + invariant re-check
46. ☐ Add `require_keys_neq!` for every security-relevant mutable-role pair unless aliasing is explicitly intended via `dup`

---
<!-- AUTO-ADDED 2026-04-03 (Red Team Daily Evolution) — B77 Drift durable nonce admin-takeover generalization -->

## 2026-04-03 Additional Pattern Additions

### B77 — Durable Nonce Approval Laundering / Pre-Signed Multisig Admin Takeover
- **Solana context**: durable nonce accounts allow a transaction to remain executable far beyond the normal recent-blockhash lifetime. That is operationally useful, but it also means signer approval time can be separated from execution time by hours or days.
- **Why this matters on Solana specifically**:
  1. Multisig / council workflows often happen off-band in chat, ticket, or wallet UI approval flows.
  2. Signers may treat a durable-nonce transaction as a temporary test or maintenance action, not a transaction that can be stockpiled for later broadcast.
  3. Once quorum is collected, the attacker no longer needs real-time signer interaction.
- **Observed real-world signal**: Drift Protocol (April 2, 2026) disclosed a Security Council takeover involving durable nonce accounts and pre-signed transactions.
- **Attack shape**:
  1. Prepare durable nonce accounts in advance.
  2. Gather privileged signatures on opaque or misrepresented transactions.
  3. Wait until enough signatures are accumulated.
  4. Broadcast later to rotate authority, change limits, or unlock fund flows.
- **Detection pattern in Solana code / ops**:
```rust
// RISKY: privileged tx remains valid after signer review window closes
let message = Message::new_with_nonce(
    instructions,
    Some(&payer.pubkey()),
    &nonce_account,
    &nonce_authority,
);
let mut tx = Transaction::new_unsigned(message);
tx.try_partial_sign(&[signer_a, signer_b], durable_nonce_hash)?;
archive_or_forward(tx)?; // delayed execution risk
```
- **Why distinct from generic multisig compromise**: signer keys do not need to be stolen. The signed transaction itself becomes the weapon because execution is deferred.
- **Microstable current status**: reviewed keeper code uses fresh `get_latest_blockhash()` send-time signing, not durable nonce accounts. Current path is **not active**. Risk becomes immediate if upgrade-authority or emergency-admin flows adopt durable nonce signing.

### Solana-Specific Defense Checklist Update
47. ☐ Privileged multisig / upgrade / treasury transactions must not use durable nonce accounts by default; if emergency nonce flow exists, require short TTL, explicit instruction digest review, nonce rotation, and no shared storage of partially signed transactions

---
<!-- AUTO-ADDED 2026-04-06 (Red Team Daily Evolution) — A98~A99 Drift Protocol refined patterns -->

## 2026-04-06 Drift Protocol Refined Patterns

### A98 — Oracle Manipulation via Fake Asset with Minimal Liquidity (Solana-Specific Variant)
- **Solana context**: SPL token creation is cheap (<0.01 SOL). Raydium and other Solana AMMs have no minimum liquidity requirement for listing. Oracles that use AMM spot price without liquidity weighting are vulnerable.
- **Attack shape**:
  1. Mint 750M units of fake token (CVT in Drift case).
  2. Seed $3,000 liquidity on Raydium.
  3. Wash trade to maintain price near $1.
  4. Oracle accepts token as collateral based on spot price.
  5. Deposit fake tokens, withdraw real assets.
- **Why distinct from A3**: A3 manipulates price of REAL assets. A98 creates the asset itself — no underlying value exists.
- **Solana-specific defense**:
  - Pyth oracle: only lists assets on major exchanges (gatekeeping).
  - Custom oracle: minimum liquidity threshold (>$1M TVL), asset age requirement (30+ days), liquidity-weighted price.
- **Checklist item 48**: ☐ If protocol accepts custom collateral assets, require: (a) TVL > $1M on primary DEX, (b) asset age > 30 days, (c) liquidity-weighted oracle price, (d) manual governance whitelist.

### A99 — Zero-Timelock Governance Migration Attack (Solana-Specific Variant)
- **Solana context**: Solana programs often use PDAs as admin authorities. Migration of admin authority (e.g., Security Council) can change threshold and timelock settings.
- **Attack shape**:
  1. Protocol migrates governance to new council/multisig.
  2. Migration sets timelock = 0 for "operational flexibility".
  3. Attacker (already positioned) immediately executes privileged operations.
  4. No time for monitoring/alerting/response.
- **Observed real-world signal**: Drift Protocol migrated Security Council to 2/5 threshold on March 27, 2026 — with zero timelock. This eliminated the detection window.
- **Why distinct from A5**: Not a timelock bypass — it's a governance decision that REMOVES the timelock entirely.
- **Solana-specific defense**:
  - Enforce minimum timelock (24h) at program level.
  - Migration requires separate governance vote.
  - Monitor governance config changes.
- **Checklist item 49**: ☐ All governance/admin migrations must: (a) enforce ≥24h timelock, (b) require separate vote for timelock removal, (c) trigger monitoring alert on config change.

### Solana-Specific Defense Checklist Update
48. ☐ Custom collateral onboarding: TVL > $1M, age > 30 days, liquidity-weighted oracle, governance whitelist
49. ☐ Governance migration: enforce ≥24h timelock, separate vote for removal, monitoring alert

### A105 — Persistent Nonce Durable Pre-Signed Transaction Bypass (Drift Pattern)
- **Solana context**: Durable nonce accounts allow transactions to remain executable indefinitely beyond normal recent-blockhash lifetime (~150 slots). Pre-signed durable nonce transactions can be stockpiled and executed at attacker-chosen time.
- **Drift-specific attack chain** (April 1, 2026):
  1. March 23: Attacker initialized 4 persistent nonce accounts (2 linked to Drift Security Council signers, 2 attacker-controlled)
  2. Pre-signed instructions were obtained under guise of routine protocol maintenance
  3. March 27: Governance migration to 2/5 + zero timelock removed delay window
  4. April 1: Pre-signed txs executed in 12 minutes across 31 withdrawals
- **Why distinct from A99**: A99 covers the governance migration to zero timelock. A105 is the *mechanism* — durable nonces make ANY pre-signed privileged tx a deferred weapon, regardless of governance changes
- **Keeper/infrastructure relevance**: If Microstable privileged operations (upgrade, emergency admin, treasury) ever use durable nonce accounts, the same stockpiling attack applies. Keeper binary uses fresh `get_latest_blockhash()` per transaction — NOT currently using durable nonces
- **Detection command**: Search for `nonce_account` or ` durable_nonce` in all privileged admin scripts and program initialization paths
- **Checklist item 50**: ☐ No privileged operations use durable nonce accounts. If emergency nonce flow is added, require: (a) short TTL ≤10 slots, (b) explicit instruction digest review by all signers, (c) no stockpiling of partially-signed nonce transactions

### A106 — Stablecoin Issuer CCTP Exfil via Selective Inaction (Drift $232M USDC Pattern)
- **Solana context**: Circle's Cross-Chain Transfer Protocol (CCTP) is the primary USDC bridge from Solana to Ethereum. CCTP requires Circle's mint/burn mechanism — Circle can freeze minted USDC on destination chain
- **Drift-specific exploit**: $232M USDC bridged Solana → Ethereum via CCTP during active exploit. Circle had frozen 16 unrelated wallets 8 days earlier for a sealed U.S. civil case, demonstrating active freeze capability. Circle took 6+ hours to begin partial freezing — 0 freeze during active attack
- **Attack shape**:
  1. Drain Solana DeFi protocol using admin key compromise or smart contract exploit
  2. Convert assets to USDC
  3. Bridge USDC to Ethereum via CCTP (Circle's own infrastructure)
  4. Circle has freeze power but may delay or refuse during active exploit
- **Microstable specific risk**: Microstable accepts USDC, USDT, DAI, USDS as collateral. If USDC is the dominant collateral and a similar exploit occurs, $232M in USDC could be exfil'd via CCTP before Circle acts
- **Defense requirements**:
  1. Document Circle emergency freeze contact procedure and SLA (target: <30 min response)
  2. Maintain alternative circuit breaker that pauses mint/redeem if >$10M USDC exits via CCTP in <1 hour
  3. Cross-chain bridge usage monitoring with automatic alert
- **Source**: https://www.cryptotimes.io/2026/04/03/285m-gone-in-12-minutes-how-a-fake-token-and-stolen-keys-gutted-drift-protocol/

### B78 — Wide Cross-Slot Sandwich Attack (Firedancer Era, 93% of Solana MEV)
- **Signal**: dev.to analysis (2026-04), Solana MEV defense research
- **Pattern**: 93% of Solana sandwich attacks now span multiple validator slots — no longer detectable as same-block transactions:
  ```
  Slot N (Attacker-Controlled Validator): tx[last] = front-run buy
  Slot N+1 (Any Validator): tx[mid] = victim swap at inflated price
  Slot N+2 (Attacker-Controlled Validator): tx[0] = back-run sell
  ```
- **Distinct from B40**: B40 (ACE fairness) is about protocol-level ordering rules. B78 is about MEV extraction across slot boundaries made possible by validator-level coordination
- **Single bot dominance**: One program (vpeNALD) executes 51,600 TX/day, 88.9% success rate, ~$450K SOL/day extraction
- **Firedancer verification lag amplifier**: Firedancer's dynamic block sizing + skip-vote creates intra-slot price lag. Keeper oracle update TX in slot N may show `oracle_slot=N` while price publication was 200ms prior — attacker can sandwich against the stale inner-slot price
- **Microstable risk**: LOW (stablecoin mint/redeem with fixed-price oracles, not AMM swaps). Keeper oracle updates use Pyth with publish_time + slot freshness — Firedancer intra-slot lag is absorbed by the publish_time check
- **Mitigation**: Jito `dontfront` flag protects within-block ordering; wide-slot attacks require separate defense

### Solana-Specific Defense Checklist Update
50. ☐ No privileged operations use durable nonce accounts; emergency nonce flow has ≤10 slot TTL + instruction digest review
51. ☐ Circle CCTP exfil: documented freeze procedure SLA <30 min + circuit breaker on large USDC bridge outflows
52. ☐ Wide cross-slot sandwich: Jito dontfront for keeper TX when possible; monitor for multi-slot MEV patterns
53. ☐ Instruction introspection: if using `load_instruction_at_checked`, migrate to `get_instruction_relative`; no hardcoded absolute instruction index for prerequisite checks

### A108 — Improper Instruction Introspection: Absolute vs Relative Indexing
- **Signal**: dev.to "Solana's CPI Security Trap" (2026-04-09)
- **Pattern**: `load_instruction_at_checked(n)` with hardcoded absolute index allows single instruction to satisfy multiple checks
- **Fix**: Use `get_instruction_relative(offset)` — verifies instruction immediately adjacent to current instruction
- **Microstable**: Not used — zero instruction introspection calls in program code ✅

---
<!-- AUTO-ADDED 2026-04-11 (Red Team Daily Evolution) — A109 Anchor lifecycle hooks -->

## 2026-04-11 Anchor 1.0 Tooling-Plane Pattern Additions

### A109 — Anchor Lifecycle Hook Supply-Chain Persistence
- **Solana context**: Anchor 1.0 adds executable lifecycle hooks in `Anchor.toml` (`pre_build`, `post_build`, `pre_test`, `post_test`, `pre_deploy`, `post_deploy`). That makes project configuration an execution surface on developer and deploy machines.
- **Attack idea**: A malicious PR or compromised contributor adds a seemingly harmless hook or referenced script. Routine `anchor build/test/deploy` then runs attacker code that swaps artifacts, exfiltrates wallet material, or mutates release outputs before on-chain deployment.
- **Why this matters on Solana**: Solana projects often keep deploy authority, IDL workflows, local validators, and CLI wallets in the same operator environment. Compromise of the Anchor hook plane can become upgrade-authority compromise without any on-chain bug.
- **Microstable current status**: `programs/microstable/Cargo.toml` and `keeper/Cargo.toml` are still on Anchor `0.31.1`, and no `Anchor.toml` / `[hooks]` usage was found in the repo. The vector is **not active today**, but becomes immediately relevant on Anchor 1.0 migration.
- **Checklist item 54**: ☐ If migrating to Anchor `>=1.0.0`, treat `Anchor.toml` as executable code: forbid `[hooks]` by default, require CODEOWNER review for any hook, and run deploys from ephemeral/hardware-signer environments.

### Solana-Specific Defense Checklist Update
54. ☐ Anchor `>=1.0.0` migration: no lifecycle hooks by default; any `[hooks]` entry requires explicit review, allowlist, and isolated runner/hardware signer path
