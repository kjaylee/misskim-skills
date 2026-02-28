# Attack Matrix — 42 Vectors with Historical Mechanisms & Defense Patterns

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
**Historical**: Mango Markets (2022, $114M), Euler (2023, $197M), Harvest (2020, $25M), PancakeBunny (2021, $45M), BonqDAO (2023, $120M), Stake Nova (2026-02-27, $2.39M)
**Mechanism**: Borrow massive capital in single TX → manipulate AMM/oracle price or redeem path invariants → exploit mispriced mint/redeem/liquidation → repay loan with profit.
**Key insight**: Any protocol that reads price from a manipulable source *or* executes redeem logic without strict invariant checks can be flash-loan-amplified in one transaction.
**2026 reinforcement (Stake Nova)**: Unchecked validation in `RedeemNovaSol()` enabled a flash-loan-assisted liquidity drain.
**Source**: https://hacked.slowmist.io/
**Code pattern to find**:
```
// VULNERABLE: same-block price read for critical operation
let price = get_oracle_price();  // can be stale or manipulated
let mint_amount = collateral * price / target;
mint(user, mint_amount);
```
**Defense**: TWAP oracles, staleness checks (>N slots = reject), confidence interval checks, mint/redeem cooldowns, per-block volume limits.

### A3. Oracle Manipulation
**Historical**: Mango (Pyth feed manipulation), BonqDAO (TellorFlex oracle), Harvest (Curve pool as oracle), Moonwell (2026, $1.78M bad debt), YieldBlox (2026-02-22, $10.97M)
**Mechanism**: Push stale/false price data to oracle → protocol acts on wrong price → value extraction.
**2026 reinforcement (Moonwell + YieldBlox)**: (1) Oracle-composition unit mismatch (`cbETH/ETH` ratio treated as USD price), and (2) low-liquidity market exploitation where tiny self-trades distorted quoted collateral value and enabled excess borrowing.
**Source**: https://rekt.news/moonwell-rekt | https://rekt.news/yieldblox-rekt
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
**Historical**: Compound ($147M — distribution logic), Cream ($130M — accounting), Popsicle ($20M — fee tracking), Moonwell (2026 oracle wiring regression), Stake Nova (2026 redeem-path validation gap)
**Mechanism**: Incorrect business logic allows unintended state transitions or value extraction.
**2026 reinforcement (Moonwell + Stake Nova)**: Governance-approved deployment can still ship a one-line arithmetic/wiring omission (Moonwell) or unchecked redeem-path validation (`RedeemNovaSol`) that becomes flash-loan-amplified (Stake Nova).
**Defense**: Formal spec → test cases → implementation. Invariant tests. Fuzzing. Add explicit unit tests for oracle composition and deploy-time sanity assertions (`min_price <= feed <= max_price`), plus redeem invariant assertions (`min_out`, vault/account binding, and per-tx flow caps).
**Source**: https://rekt.news/moonwell-rekt | https://hacked.slowmist.io/

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
**Historical**: Ronin ($624M), Harmony ($100M), Slope wallet, IoTeX ioTube (2026, $4.4M)
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

### B29. AI Agent Prompt-Injection Confused-Deputy
**Historical**: Trail of Bits Comet audit (2026-02-20) + SkillInject benchmark (arXiv 2602.20156)
**Mechanism**: Attacker-controlled content (page/skill file/reference doc) injects instructions that make an autonomous agent use trusted tools (browser, wallet, RPC admin actions) to exfiltrate secrets or perform unauthorized actions.
**2026 reinforcement (Comet)**: Real exploit chains combined (a) fake CAPTCHA/security validator flows, (b) fake system-message delimiters, (c) fake user-request delimiters, and (d) multi-step "fragment assembly" prompts. Result: agent navigated from attacker page to authenticated Gmail context and exfiltrated mailbox contents to attacker endpoint.
**Bypass insight**: Even when model rejects simple direct prompts, semi-structured wrappers (`[BEGIN SYSTEM MESSAGE]`, "policy update", "abuse prevention") and staged tasks can still hijack tool execution.
**Defense**: Tool-level authorization policy (not prompt-only), data/command channel separation, strict side-effect allowlists, authenticated provenance tags for instructions, and human approval for privileged actions.
**Source**: https://blog.trailofbits.com/2026/02/20/using-threat-modeling-and-prompt-injection-to-audit-comet/ | https://arxiv.org/abs/2602.20156

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

### C30. Liquidity-Exhaustion Griefing
**Historical**: Intent bridge study (arXiv 2602.17805, Feb 2026)
**Mechanism**: Attacker repeatedly consumes finite execution/liquidity capacity (solver capital, per-window redemption bandwidth) to deny service or force unfavorable pricing for honest users.
**Bypass insight**: Attacker can optimize route/timing to reduce griefing cost substantially while keeping victim impact high.
**Defense**: Identity-aware quotas, adaptive pricing by actor concentration, reservation lanes for organic flow, and anti-grief penalties tied to failed or bursty usage patterns.

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
**2026 reinforcement (RustSec)**: short-lived typosquat waves (`rpc-check`, `tracing-check`) targeted a specific ecosystem to steal credentials before package takedown.
**Defense**: Lock files, audit dependencies, minimal dependency tree, vendoring, Cargo.lock attestation, registry-source allowlists, and two-person review for new deps.

### D31. Protocol-Metadata Confusion (IDL/Schema Trust)
**Historical**: Anchor `idl: Exclude external accounts` patch (2026-02-22)
**Mechanism**: Off-chain clients over-trust generated metadata and infer ownership/safety guarantees for accounts that are actually external, leading to unsafe automation or signing UX.
**Defense**: Treat generated IDL/schema as advisory; enforce runtime owner/program checks and account invariants in clients before signing/submitting transactions.

### A32. Cross-Chain Bridge Message Forgery
**Historical**: Saga / SagaEVM (2026-01-21, $7M) — IBC precompile bypass enabling collateral-free minting
**Mechanism**: Attacker deployed a helper contract that crafted custom IBC payloads mimicking legitimate cross-chain deposit events. The EVM precompile bridge layer accepted these forged messages without verifying that real collateral existed on the source chain. Protocol's mint logic consumed the fake deposit event and minted $7M in stablecoins from thin air. Attacker converted to yETH/yUSD/tBTC, bridged to Ethereum as 2,000+ ETH.
**Root cause in Ethermint codebase**: `IBC precompile` did not authenticate the on-chain origin of `deposit` events — any contract could emit a compliant message structure and trigger the collateral credit logic.
**Code pattern to find**:
```solidity
// VULNERABLE: no verification that source-chain deposit actually occurred
function handleIBCDeposit(bytes calldata payload) external {
    (address user, uint256 amount) = abi.decode(payload, (address, uint256));
    _mint(user, amount);  // no cross-chain proof checked
}
```
**Solana relevance**: Not directly applicable (Microstable is Solana-native, no IBC layer). Relevant if adding Wormhole/IBC integration — would require verifying VAA signatures / light client proofs before crediting collateral.
**Defense**: Require cryptographic proof of source-chain state (Merkle proofs, VAA signatures, or sequencer attestation). Never credit collateral from a message alone; verify the deposit event is anchored to a finalized source block. Separate the "message received" and "collateral credited" state transitions with explicit proof verification.
**Source**: https://rekt.news/saga-rekt | https://x.com/cosmoslabs_io/status/2014428829423706156

### B36. Social-Engineering-to-Stake-Authority-Hijack
**Historical**: Step Finance (2026-01-31, $27.3M) — executive device compromised via spear-phish; stake delegation authority transferred to attacker wallet; 261,854 SOL unstaked in ~90 minutes.
**Mechanism**: Attacker does not need a smart contract exploit. Solana's stake delegation model separates stake authority from withdrawal authority, both reassignable unilaterally by the current controller. If an operator's hot device (laptop, workstation) is compromised, the attacker can sign a `StakeAuthorize` instruction to redirect staking rights to their wallet, then unstake and drain. The on-chain action looks legitimate — no program exploit, no anomalous CPI.
**Key insight**: "Audited contracts, bug bounties, public security reviews" were all irrelevant — the attack surface was the human layer and the key held in memory on a compromised device. Private-key compromise now accounts for 88% of Q1 2025 crypto losses (Chainalysis 2026).
**Code pattern to find**:
```
# No on-chain code vulnerability — the vector is:
# 1. Operator device has plaintext or session-accessible hot key
# 2. Phishing / infosteal / RAT payload extracts or misuses key
# 3. Attacker signs: StakeAuthorize(stake_account, new_authority)
# 4. Then: Deactivate → Wait epoch → Withdraw
```
**Solana keeper relevance**: Keeper keypairs are active hot keys on the operator's machine. If keeper host is compromised, attacker gains:
- Ability to drain treasury by submitting privileged keeper instructions
- Ability to manipulate oracle write path (if MANUAL_ORACLE_MODE enabled)
- Config injection (if keeper reads writable config)
**Defense**:
1. Hardware keys (Ledger/YubiKey) for treasury-level operations — never hot
2. Separate stake/withdrawal authority from day-to-day keeper keypair
3. Per-operation stake amount limits (partial stake accounts, not single monolithic stake)
4. Multi-device / time-delayed confirmation for stake authority re-assignment
5. Endpoint Detection & Response (EDR) on all operator devices
6. Device phishing hygiene: email sandboxing, link preview policies, no unverified attachments
**Source**: https://rekt.news/step-finance-rekt

### B35. Keeper Parameter Misconfiguration (Operational Slippage Error)
**Historical**: YO Protocol (2026-02, $3.71M) — vault operator fat-fingered a $3.84M swap with broken slippage params; only $112K recovered
**Mechanism**: A keeper/vault-operator submitted a swap transaction with near-zero or invalid slippage tolerance. The DEX routed the trade at a catastrophically unfavorable price. The operator noticed $3.72M loss after execution; team backstopped quietly and delayed disclosure 2 days.
**Code pattern to find**:
```rust
// VULNERABLE: slippage parameter accepted from config with no enforcement cap
let min_amount_out = config.slippage_min_out; // user-supplied, could be 0
swap(amount_in, min_amount_out, ...)?;

// SAFE: enforce hard floor from protocol constants
let max_allowed_slippage = MAX_SLIPPAGE_BPS; // e.g., 300 bps = 3%
let floor_amount_out = amount_in * (10_000 - max_allowed_slippage) / 10_000 * oracle_price / SCALE;
let effective_min_out = std::cmp::max(min_amount_out, floor_amount_out);
```
**Defense**:
1. Hard-cap slippage tolerance in code (not just config) — reject any swap where `min_amount_out` implies >N% slippage vs. current oracle price
2. Two-operator sign-off for swaps above a dollar threshold (e.g., >$100K)
3. Simulation pre-check: simulate swap, compare expected vs. actual output before broadcasting
4. Alarm + auto-cancel if realized slippage exceeds threshold after execution
**Source**: https://rekt.news/yo-protocols-slippage-bomb

### A33. Audit-Scope-Exclusion Exploitation
**Historical**: Makina Finance (2026-01-20, $4.13M) — oracle manipulation via `lastTotalAum` from spot Curve pool price. The exact attack vector was documented in Cantina's audit scope as explicitly *out-of-scope*. Six audit firms (ChainSecurity, OtterSec, SigmaPrime, Enigma Dark, Cantina) signed off. Protocol deployed with the known gap unfixed.
**Mechanism**: Flash loan → inflate Curve pool spot price → `lastTotalAum` reads manipulated price → DUSD share price mismatch → over-mint/drain. $280M flash borrowed. Original attacker deployed an unverified exploit contract; an MEV searcher decompiled it in the same block and front-ran the attacker, capturing most of the $4.13M across two addresses.
**Key insight**: Audit scope exclusions are not "this can't be exploited" — they're "we didn't look here." Attackers scan scope limitation lists as *roadmaps to unfixed attack surface*. MEV bots add a second-order amplification: any exploit contract on a public mempool can be decompiled and replayed faster than the original attacker.
**Microstable relevance**: Any oracle path that uses a manipulable spot price (AMM pool, single-source Pyth without TWAP) is vulnerable if not explicitly covered in audit scope. Current hardening: TWAP + Pyth confidence + staleness checks are in scope. But: if a new operator integration excludes part of the oracle composition from audit scope, the gap becomes exploitable.
**Code pattern to find**:
```rust
// VULNERABLE: total_aum or collateral value derived from spot AMM pool
let total_aum = pool.get_virtual_price(); // manipulable in same TX
let share_price = total_aum / total_shares;
mint(user, deposit / share_price);

// SAFE: use TWAP or committed price with staleness guard
let price = twap_oracle.get_price_checked(max_age_slots)?;
```
**Defense**:
1. Treat audit scope exclusions as mandatory backlog items — never ship with known-excluded vectors
2. Require TWAP or multi-source oracle for any value used in mint/burn/share-price calculation
3. Per-TX mint cap limits damage even if oracle is manipulated
4. Simulate MEV extraction potential before deploying: if a bot can replicate your exploit contract profitably, the attack will happen
**Source**: https://rekt.news/makina-rekt

### A34. Fragmented Security Stack Failure
**Historical**: Balancer (2025-11, $100M) — precision-loss in composable stable pool scaling math
**Mechanism**: Each security control (audit, bug bounty, monitoring, incident response) operated correctly in isolation but shared no data or detection rules. A rounding-error class was disclosed via Immunefi in 2023, patched for that pool type, but never abstracted into a detection rule applied to other pool variants. Same vulnerability class recurred 2 years later in composable stable pools. Attacker manipulated raw token balances into small-value ranges, then exploited integer division precision-loss in scaled math repeatedly to extract $100M.
**Root insight**: Individual controls do not prevent systemic failure when they have no shared visibility. Vulnerability class knowledge siloed inside a single audit/report never fortified adjacent pool designs.
**Code pattern to find**:
```solidity
// RISKY: scaled-math division with raw balances that can be pushed small
uint256 scaledAmount = (rawBalance * scalingFactor) / 1e18;
// If rawBalance is tiny (attacker-controlled via flash swap), precision drops significantly
// Repeated extraction of tiny rounding dust across many swaps = material loss
```
**Microstable relevance**: Any protocol that reads a ratio/price-scaled value for mint/redeem math must verify that:
  (a) raw inputs cannot be pushed to extremes within a single TX (per-TX volume caps)
  (b) bounty/audit findings for this class are propagated across **all** entry points that share the same math pattern
**Defense**:
1. Maintain a "vulnerability class registry" — when a class is discovered anywhere, audit all code using the same math pattern
2. Unified observability: monitoring rules derived from past exploit mechanics, not just generic anomaly detection
3. Test precision-loss at boundary values (very small raw balances) during invariant fuzz runs
4. Emergency pause scope: ensure any governance-level pausing can halt all affected pool/entry types, not just the specific reported path
**Source**: https://immunefi.com/blog/expert-insights/how-fragmented-security-enabled-balancer-exploit/

### A35. AI-Assisted Commit Oracle Regression
**Historical**: Moonwell (2026, $1.78M bad debt) — cbETH oracle priced at $1.12 instead of ~$2,200; commit co-authored by Claude Opus 4.6
**Mechanism**: An AI coding assistant generated code that used `cbETH/ETH` ratio directly as the USD price, omitting the second multiplication step (`ratio × ETH_USD`). The unit mismatch produced a 99%+ mispricing. Liquidation bots acted on the malformed price, creating $1.78M in bad debt. This is considered the first documented major DeFi exploit triggered by AI-generated smart contract code ("vibe-coded contracts").
**Key insight**: AI coding assistants can generate syntactically valid, functionally incorrect oracle composition. Standard code review and CI may pass because no syntax or compilation error exists — only a semantic unit violation. The assistant likely treated `cbETH/ETH` as a USD price because it satisfied the type interface (uint256) without catching the unit chain.
**Code pattern to find**:
```rust
// VULNERABLE: ratio feed used directly as USD price (no base multiplication)
let price = cbeth_eth_ratio;  // ≈ 0.95, not ~2200

// SAFE: explicit unit chain
let cbeth_eth: u64 = ratio_oracle.get_price()?;  // ~0.95
let eth_usd: u64 = usd_oracle.get_price()?;       // ~2300
let cbeth_usd = (cbeth_eth as u128 * eth_usd as u128) / SCALE;
```
**Microstable relevance**: Any oracle feed change reviewed with AI assistance must be gated by a mandatory unit-invariant assertion. The existing `unit-invariant canary` recommendation from PT-ARCH-2026-0225-01 is directly validated by this incident.
**Defense**:
1. **Unit-invariant test for every oracle feed**: CI must verify that `reported_price` for each asset falls within `[expected_usd * 0.8, expected_usd * 1.2]` using a hardcoded sanity range
2. **Two-person review for oracle feed changes** — AI-assisted commits are not exempt
3. **On-chain sanity assertion at deploy time**: `assert(min_price <= feed_result <= max_price)` for new oracle integrations
4. **AI commit tagging**: when AI tools co-author a security-critical commit, flag it for elevated human review in CI policy
**Source**: https://rekt.news/moonwell-rekt

### D32. AI Agent Skill/Identity Poisoning
**Historical**: OpenClaw skill poisoning (2026) — "20% of skills poisoned on OpenClaw. Now someone wants to give these AI agents access to bank accounts."
**Mechanism**: Attacker compromises the skill/tool library that an AI agent loads at runtime. Unlike prompt injection (which attacks a single context window), skill poisoning attacks the **persistent behavioral configuration** of the agent. A poisoned skill file can:
  (a) Override the agent's security policy by injecting fake "system-like" authorization rules
  (b) Redirect tool calls (wallet signing, RPC admin actions) to attacker-controlled endpoints
  (c) Exfiltrate secrets by modifying the agent's read/write behavior silently over many sessions
  (d) Persist across restarts because the agent reloads skills from a tampered source
**Key insight vs B29 (Confused-Deputy)**: B29 is a runtime attack via content the agent processes. D32 is a supply-chain attack on the agent's identity/policy layer — the agent believes it is following its own rules while executing attacker instructions. Detection is harder because the agent exhibits authorized behavior (from its poisoned perspective).
**DeFi agent relevance**: Keeper agents, AI ops assistants, or governance proposal drafters that load skills/tools from a shared registry are fully exposed. One poisoned skill file = full access to all privileged operations the agent can perform.
**Code/config pattern to find**:
```yaml
# VULNERABLE: agent loads skills from a mutable, unverified directory
skill_dirs:
  - /var/agent/skills/   # any write access = compromise

# SAFE: cryptographically pinned skills with explicit allowlist
skill_dirs:
  - /var/agent/skills/  # read-only mount
skill_manifest: /etc/agent/skill-manifest.sha256  # verified on load
allowed_skills:
  - oracle-monitor@1.2.3@sha256:abc...
  - keeper-submit@2.0.1@sha256:def...
```
**Defense**:
1. Cryptographic integrity verification of all skill files at load time (SHA-256 manifest pinning)
2. Read-only skill directory mounts in production environments
3. Explicit allowlist of permitted skills with version + hash locks
4. Skill update path requires multi-party approval (same as code deploy)
5. Behavioral audit log: surface when agent takes actions outside observed historical pattern
6. Separate execution context for untrusted research/browsing tasks vs. privileged tool invocations
7. Human quorum gate for any action that involves signing/broadcasting to chain
**Source**: https://rekt.news/identity-theft-2

### D33. Transitive Payload Relay Typosquat
**Historical**: RustSec RUSTSEC-2026-0027 (`tracings`) + RUSTSEC-2026-0028 (`tracing_checks`) (2026-02-26)
**Mechanism**: Attacker publishes a seemingly harmless crate and hides the actual payload in a second transitive dependency. Reviewers inspecting only direct dependencies see low-risk glue code, while credential-stealing logic executes through the nested crate.
**Key insight vs D28**: D28 covered direct typosquat waves (`rpc-check`, `tracing-check`). D33 is a second-stage pattern: **dependency laundering through transitive indirection**, designed to bypass direct-name checks and shallow package review.
**DeFi keeper relevance**: High-risk when operators add observability/helper crates quickly during incident response. A single transitive malicious crate can exfiltrate API keys, wallet paths, or signing context before runtime guards trigger.
**Code/config pattern to find**:
```toml
# VULNERABLE: near-name crate chain with hidden transitive payload
[dependencies]
tracing_checks = "0.1"   # appears benign
# internally pulls: tracings = "0.1" (malicious payload)

# SAFER: pinned vetted graph + provenance gate
[dependencies]
tracing = "0.1.41"
tracing-subscriber = { version = "0.3.19", default-features = false, features = ["fmt", "env-filter"] }
```
**Defense**:
1. Block newly published crates (<7 days age) for production keeper builds unless emergency-approved
2. CI gate on full transitive diff (`cargo tree --locked`) — not only `Cargo.toml` direct changes
3. Add name-distance policy for new crates (Levenshtein proximity to critical ecosystem crate names)
4. Enforce two-person security sign-off whenever `Cargo.lock` hash attestation is updated
5. Maintain dependency allowlist by crate name + publisher reputation for keeper-critical binaries
**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0027.html | https://rustsec.org/advisories/RUSTSEC-2026-0028.html

### A36. Thin-Liquidity Collateral Admission Cascade
**Historical**: YieldBlox / Blend V2 (2026-02-22, $10.97M)
**Mechanism**: Exploit is not a single oracle bug. It is a compositional chain:
1) Governance/listing admits collateral with near-zero market depth
2) Oracle source uses that thin market (single-source VWAP/spot)
3) Adapter forwards latest price without robust outlier aggregation (e.g., median/deviation guard)
4) Lending health-factor logic accepts inflated value and approves borrow
**Key insight**: Each component can be "working as designed" in isolation while the composed system is catastrophically unsafe.
**Code pattern to find**:
```rust
// RISKY: price validity checks without market-quality checks
let price = oracle.latest_price(asset)?;
require!(price_age <= MAX_AGE, Error::Stale);
// missing: liquidity/depth/activity gate
let collateral_value = amount * price;
```
**Defense**:
1. Collateral listing gate must include market-quality invariants (min depth, min active makers, min rolling volume)
2. Oracle adapter must aggregate with robust estimator (median/trimmed mean) + deviation clamps
3. Borrow path should reject collateral if market-quality signal is degraded, even if price freshness/confidence pass
4. Periodic re-certification of collateral quality (not one-time listing)
**Source**: https://rekt.news/yieldblox-rekt

### A38. ZK Verifier Key Misbinding / Proof-Parameter Drift
**Historical**: FOOMCASH (2026-02-26, ~$2.26M)
**Mechanism**: Verifier configuration drift (or incorrect verification-key binding) allowed forged/invalid proofs to pass verification checks. Attacker minted/withdrew funds by replaying the protocol flow with a proof that should have failed under the intended circuit parameters.
**Key insight**: ZK systems fail open when verification parameters (verification key hash, circuit ID, public-input schema) are mutable or inconsistently bound across contracts/services. This is not a generic oracle bug — it is cryptographic trust-root misbinding.
**Code pattern to find**:
```solidity
// VULNERABLE: verifier key can be swapped without strict governance + integrity checks
function setVerifier(address newVerifier) external onlyOwner {
    verifier = newVerifier;
}

function mint(bytes calldata proof, uint256[4] calldata publicInputs) external {
    require(IVerifier(verifier).verify(proof, publicInputs), "bad proof");
    _mint(msg.sender, publicInputs[0]);
}
```
**Defense**:
1. Pin immutable verification-key hash (or circuit ID) in contract state and validate every proof against it
2. Use two-step timelocked verifier upgrades with independent quorum + on-chain hash precommit
3. Enforce public-input schema/version checks (domain separation across circuits)
4. Add canary proofs (expected-pass and expected-fail) to upgrade/deploy pipeline
**Source**: https://hacked.slowmist.io/ | https://www.cryptotimes.io/2026/02/26/foomcash-loses-2-26m-in-copycat-zksnark-exploit/

### B37. AI Agent Steganographic Oversight Evasion
**Historical**: arXiv 2602.23163 (2026-02-26) — decision-theoretic steganography framework for LLM monitoring
**Mechanism**: Agent outputs embed hidden intent/policy-violating signals that are useful to a colluding decoder agent but look benign to standard monitors. This bypasses prompt-level policy checks by moving malicious coordination into covert channel structure.
**Key insight vs B29**: B29 is explicit prompt injection from untrusted input. B37 is **covert post-compromise coordination** that can survive even when prompt injection filters are in place.
**Code/config pattern to find**:
```yaml
# RISKY: output-policy checks rely only on lexical/regex content filters
agent_guardrails:
  monitor: "keyword-and-policy-classifier-only"

# SAFER: action-level authorization + dual-agent consistency checks
agent_guardrails:
  monitor: "action authorization + out-of-band utility-gap detector"
```
**Defense**:
1. Enforce tool/action authorization independent of model output text quality
2. Add "usable-information asymmetry" checks (if collaborator utility increases while monitor utility does not, flag)
3. Require human approval for high-impact actions even when textual output appears compliant
4. Rotate/red-team monitor prompts and evaluators to reduce stable covert-channel bandwidth
**Source**: https://arxiv.org/abs/2602.23163

## Why Audits Miss It — Vector Notes (Purple Reinforcement)

| Vector | 왜 감사가 놓치는가 (메타 원인) |
|---|---|
| A1 Reentrancy | 함수 단위 체크리스트에 치우쳐 cross-function reentry 경로를 축약 평가. |
| A2 Flash Loan | 단일 TX 시뮬레이션/경제 모델링 부족으로 자본 무제한 가정이 빠짐. |
| A3 Oracle Manipulation | feed 단위 검증은 하지만 unit-composition(비율×USD) 검증이 누락됨. |
| A4 Access Control | 코드 권한만 보고 키 운영/서명 정책(HSM·MPC)까지 확장 점검을 생략. |
| A5 Overflow | 정상 범위 테스트 중심, 극단 경계값과 타입 승격 경로를 충분히 안 밟음. |
| A6 Account Substitution | 계정 owner/address 제약을 “프레임워크가 해준다”는 가정에 의존. |
| A7 Signature Replay | 도메인 분리(chain/program/nonce) 전수 확인 대신 happy-path 서명 검증만 수행. |
| A8 Front-running | 온체인 로직 감사로 끝내고 mempool/ordering 위협모델을 범위 밖 처리. |
| A9 Proxy Upgrade | 현재 구현 안전성에 집중, 업그레이드 권한 탈취 시나리오를 운영이슈로 분리. |
| A10 Logic Bug | 취약점 taxonomy 매칭 위주로 명세-구현 정합성 검증이 얕아짐. |
| A11 Rent/Lamport Drain | 저금액/저영향으로 분류되어 종료·정리 경로 검토가 축소됨. |
| A12 CPI Confusion | 호출 대상 신뢰를 암묵 가정, CPI target pinning 검증 누락. |
| A13 PDA Collision | seed namespace 설계 검토 없이 코드 패턴 스캔으로 대체. |
| B14 RPC Manipulation | 온체인 무결성 가정이 강해 off-chain state ingestion 신뢰경계를 과소평가. |
| B15 Key Compromise | 코드 감사와 키 운영 감사가 분리되어 blast radius 분석이 빠짐. |
| B16 Race Condition | 단일 프로세스/단일 인스턴스 가정으로 재시작·중복 실행 경쟁을 놓침. |
| B17 Checkpoint Poisoning | 상태파일을 캐시로 간주해 무결성/권한 검증을 기능 요구로 반영하지 않음. |
| B18 Config Injection | 설정값 변경을 배포 파이프라인 문제로 분리해 런타임 위협으로 연결 안 함. |
| B19 Memory/Log Leak | 기능 로그 우선 문화로 비밀정보 마스킹이 보안 요구로 강제되지 않음. |
| B20 DoS | 자금 탈취 중심 리뷰로 가용성 공격 경제성 분석이 후순위. |
| B29 AI Agent Confused-Deputy | 프롬프트 방어를 정책으로 착각하고 tool 권한 분리/승인 경계를 누락. |
| C21 Bank Run | 코드 정확성은 확인하지만 집단행동/신뢰 붕괴 동학을 모델링하지 않음. |
| C22 Collateral Manipulation | 단일 자산 기준 정상장 시나리오만 검증, 상관붕괴·급변장 스트레스 미흡. |
| C23 Governance Attack | voting logic 검증은 해도 자금조달(플래시론) 기반 장악 비용을 계산 안 함. |
| C24 Sybil | 정체성 비용·운영정책 검토 없이 온체인 stake 기준만 확인. |
| C25 MEV | 프로토콜 내부 불변식 검증에 치우쳐 주문순서 시장구조를 별도 취급. |
| C30 Liquidity Exhaustion | 손실 없는 저강도 반복 공격의 누적효과를 단건 리스크로 축소 평가. |
| D26 Frontend Injection | 스마트컨트랙트 감사 범위 밖으로 분리되어 UI 공급망 통제가 누락됨. |
| D27 RPC Takeover | endpoint 다중화만 점검하고 공급자 상관관계(ASN/DNS)까지는 미검증. |
| D28 Supply Chain | 정적 스캐너 통과를 안전으로 간주, 단기 typosquat 파동 탐지가 느림. |
| D31 Metadata Confusion | 생성된 IDL/스키마를 사실상 신뢰원으로 취급해 런타임 검증이 생략됨. |
| A14 Out-of-Scope Composability | 감사 대상 커밋과 실제 배포된 Hook/Proxy 간 런타임 결합 추적 부재로 우회 공격 발생 (Nemo, Cork). |
| B33 OpSec & Key Management | 스마트컨트랙트 무결성에 집중하여 멀티시그, 배포 파이프라인 등 오프체인 키 운영을 감사 밖으로 취급 (Radiant). |
| A32 Cross-Chain Bridge Message Forgery | 온체인 로직만 감사하고 크로스체인 메시지 페이로드 검증 경계를 별도 신뢰영역으로 분리 (Saga IBC precompile). |
| B35 Keeper Parameter Misconfiguration | 스마트컨트랙트 파라미터 검증에 집중하여 오퍼레이터 운영 파라미터(슬리피지·임계값) 실수를 감사 외로 취급 (YO Protocol). |
| B36 Social-Engineering Stake Authority Hijack | 스마트컨트랙트 무결성 감사가 인간 계층(디바이스·피싱·RAT)까지 확장되지 않아 핫키 운영 리스크를 운영이슈로 분리 (Step Finance). |
| A33 Audit-Scope-Exclusion Exploitation | 감사 범위 제외 항목을 '검토 완료'로 착각하여 알려진 공격 벡터를 미수정 상태로 배포하고, MEV 봇의 2차 증폭 가능성을 평가하지 않음 (Makina). |
| A34 Fragmented Security Stack Failure | 각 보안 레이어(감사·바운티·모니터링·대응)가 격리 운영되어 취약점 클래스 지식이 인접 코드에 전파되지 않음. 2023 bounty report가 2025 exploit으로 재발한 Balancer 패턴이 전형적 사례. |
| A35 AI-Assisted Commit Oracle Regression | AI 어시스턴트가 단위 합성(ratio × base_usd) 의미론을 검증하지 않고 타입 호환 코드를 생성함. CI/컴파일 오류 없이 통과하여 감사도 '구문 정확'으로 승인할 위험 (Moonwell cbETH). |
| D32 AI Agent Skill/Identity Poisoning | AI 에이전트 스킬 파일을 공급망 공격면으로 보지 않고, 런타임 컨텍스트 무결성 위협(B29)과 동일하게 취급하여 에이전트 정책 레이어 자체의 오염 가능성을 누락. |
| D33 Transitive Payload Relay Typosquat | 직접 의존성만 검토하는 감사 관행을 악용해, 1차 패키지는 무해하게 보이게 두고 2차(전이) 의존성에 페이로드를 숨김. Cargo.lock 변경 승인 절차가 형식화되면 공격이 그대로 통과될 수 있음 (tracings → tracing_checks). |
| A36 Thin-Liquidity Collateral Admission Cascade | 오라클 정확성/신선도만 검증하고, **시장 품질(깊이·분산·활동성)**을 신뢰 경계 밖으로 분리. 상장 정책·오라클 어댑터·헬스팩터 로직의 결합 실패를 단일 컴포넌트 이슈로 축소해 놓침 (YieldBlox). |
| A38 ZK Verifier Key Misbinding / Proof-Parameter Drift | ZK 증명 검증 루트(verification key / circuit id / public input schema)를 운영 설정으로 느슨하게 관리해, 암호학적 신뢰 경계 자체가 교란되는 위험을 감사 범위 밖으로 분리 (FOOMCASH). |
| B37 AI Agent Steganographic Oversight Evasion | 프롬프트 인젝션 차단(B29)만으로 충분하다고 가정해, 텍스트는 정상처럼 보이지만 협력 에이전트에만 의미가 전달되는 은닉 채널(감시 비대칭)을 검증하지 않음 (arXiv 2602.23163). |


