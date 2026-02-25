# Attack Matrix — 31 Vectors with Historical Mechanisms & Defense Patterns

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
**Historical**: Trail of Bits Comet audit (2026) + SkillInject benchmark (arXiv 2602.20156)
**Mechanism**: Attacker-controlled content (page/skill file/reference doc) injects instructions that make an autonomous agent use trusted tools (browser, wallet, RPC admin actions) to exfiltrate secrets or perform unauthorized actions.
**Bypass insight**: Even when model resists direct malicious prompts, structured "system-like" fragments and fake safety workflows can still trigger tool misuse.
**Defense**: Tool-level authorization policy (not prompt-only), data/command channel separation, explicit allowlists for side effects, and human approval for privileged actions.

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


