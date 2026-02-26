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

### Typosquat Waves Targeting Solana Rust Tooling
Recent RustSec advisories (`rpc-check`, `tracing-check`) show short-lived malicious crates aimed at credential theft in a specific ecosystem.

**Mitigation**:
- Cargo.lock hash attestation in CI/runtime.
- Registry-source allowlist (crates.io only unless explicitly approved).
- Two-person review for dependency additions/renames near common crate names.

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
