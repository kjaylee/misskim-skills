# Blockchain Security Incidents — Comprehensive Timeline

> Scope: real-world incidents with explicit mechanisms. Entries without confirmed mechanisms are intentionally omitted.

## 2026

- **2026-03-17 — dTRINITY dLEND (Ethereum — aToken Index Inflation / Phantom Collateral)** — Attacker exploited a deposit inflation vulnerability in dTRINITY's `dLEND` lending protocol on Ethereum, creating $257,061 in bad debt. Root cause: inflated internal liquidity index/accounting state allowed a ~$772 USDC deposit to be valued as ~$4.8M in collateral (6,215× inflation factor). Attack chain: (1) flash-loan USDC from Morpho, (2) deposit $772 USDC into dLEND-dUSD pool, (3) due to inflated internal index, protocol incorrectly credits attacker with $4.8M phantom collateral, (4) borrow 257,000 dUSD against phantom collateral, (5) execute 127 repeated deposit/withdrawal cycles draining remaining protocol USDC from aToken accounting layer, (6) repay flash loan; net extraction ~$257K. Protocol paused on Ethereum; Fraxtal and Katana deployments unaffected (isolated reserves). Team committed to full reimbursement. Transaction flagged by DeFiMon Alerts. Attacker: `0x08cfdff8d8ed5f1326628077f38d4f90df6417fd9`. Victim contract: `0x5cc741931d01cb1adde193222dfb1ad75930fd60`.
  **Root cause**: Internal lending pool index or accounting variable could be artificially inflated, allowing phantom collateral to be recognized. The 127-cycle amplification loop drained the remaining aToken-denominated liquidity.
  Vector mapping: **A68 Lending Pool aToken/Index Inflation Phantom Collateral Attack** (NEW VECTOR, 2026-03-18 daily cycle). Secondary: **A2 Flash Loan + Price/Accounting Manipulation**.
  Source: https://hacked.slowmist.io/ | https://cryip.co/dtrinitys-dlend-protocol-exploit-drains-around-257k-on-ethereum/ | https://x.com/DefimonAlerts/status/2033868831504965995

- **2026-03-15 — Venus Protocol (BNB Chain — Supply Cap Bypass + TWAP Oracle Manipulation)** — A 9-month patience attack culminating in $2.15M loss ($3.7M peak exposure). Root cause: dual failure — (1) supply cap enforcement existed only in the `deposit()` code path, not at the balance level; (2) TWAP oracle for thin-liquidity collateral (THE token) was manipulable via position size inflation. Attack chain: attacker accumulated 14.5M THE (84% of 14.5M supply cap) through legitimate deposits over 9 months without triggering automated risk alerts. Then directly transferred tokens to protocol contracts (bypassing deposit function and supply cap check) to establish 53.2M THE position — 3.67× the intended cap. Exploiting THE token's low on-chain liquidity (~$590K depth), manipulated TWAP from $0.27 to $0.53 (96% inflation). Against inflated collateral value, borrowed 6.67M CAKE + 2,801 BNB + 1,970 WBNB + 1.58M USDC + 20 BTCB at peak. Liquidation cascade followed. Venus paused 7 affected markets. Allez Labs (Venus risk manager) confirmed supply cap circumvention via direct transfer. Losses partially offset by protocol reserves.
  **Root cause**: Protocol supply cap enforced only at deposit function level; direct token transfer to contract address is not gated. TWAP oracle used on-chain DEX price without robust manipulation resistance for thin-liquidity collateral.
  Vector mapping: **A67 Supply Cap Bypass via Direct Protocol Contract Token Transfer + Slow-Accumulation TWAP Manipulation** (NEW VECTOR, 2026-03-17 daily cycle). Secondary: **A2 Flash Loan + Price Manipulation** (TWAP manipulation phase), **A3 Oracle Manipulation**.
  Source: https://hacked.slowmist.io/ | https://allez.xyz/research/venus-protocol-attack-analysis

- **2026-03-12 — CVE-2026-20435 (Hardware) — MediaTek Android Boot Chain TEE Bypass (Ledger Donjon disclosure)** — Not a DeFi protocol exploit but a critical hardware vulnerability with direct implications for crypto operator security. Ledger's Donjon research team publicly disclosed CVE-2026-20435: a boot chain vulnerability in MediaTek processors (Dimensity 7300 and related) using Trustonic's TEE (kinibi/t-base). Attacker with physical access to a powered-off Android device → USB → exploit bootloader before OS loads → bypass TEE secure boot verification → extract disk encryption keys from secure enclave → decrypt full storage offline → harvest seed phrases, PINs, wallet private keys in under 45 seconds. Demonstrated live on Nothing CMF Phone 1. Affects ~25% of Android phones globally. Confirmed wallet extraction: Trust Wallet, **Phantom (Solana)**, Kraken Wallet, Coinbase Wallet (Base), Rabby, Tangem. MediaTek issued OEM patch 2026-01-05 but deployment lag for budget/mid-range devices is 3+ months; EOL devices may never patch.
  **Root cause**: Boot chain flaw allows pre-OS TEE initialization to be bypassed; TEE's cryptographic guarantees collapse before the secure enclave is fully established. Distinct from TEE software vulnerabilities — this attacks the *initialization sequence* of the hardware root of trust.
  Vector mapping: **B63 Physical-Access Hardware TEE Bypass — Android MediaTek Boot Chain** (NEW VECTOR, 2026-03-16 daily cycle).
  Source: https://www.theblock.co/post/393154/ledger-researchers-expose-android-flaw-enabling-theft | https://dev.to/ohmygod/cve-2026-20435-how-a-mediatek-boot-chain-flaw-exposes-crypto-wallets-on-25-of-android-phones-34i0 | CVE-2026-20435

- **2026-03-10 — Aave wstETH CAPO Oracle Misconfiguration (Ethereum — Automated Risk Parameter Execution)** — Aave's CAPO (Capped Asset Price Oracle) anti-manipulation system became the damage source rather than the protection layer. Chaos Labs' off-chain Edge Risk engine computed a new `snapshotRatio` update for wstETH that inadvertently capped the reported price at ~2.85% below the actual market rate (oracle-reported ~1.19 ETH vs. actual ~1.228849 ETH). AgentHub — an automated on-chain parameter executor built by BGD Labs using Chainlink Automation — executed the update one block after computation with zero human review. Aave's liquidation engine immediately treated 34 healthy wstETH E-Mode positions as undercollateralized. 10,938 wstETH ($27.78M) was liquidated within seconds; borrow cap was manually reduced to 1 by Chaos Labs once the anomaly was detected, but 90%+ of damage had already occurred. Full reimbursement committed by Aave DAO. No attacker involved. Edge Risk had previously processed 1,200+ payloads across 3,000+ parameters without incident.
  **Root cause**: Fully automated risk management pipeline (off-chain risk AI engine → on-chain automated executor) with no human review gate, no pre-execution sanity check, and no time-delay between parameter computation and execution. Single-block latency from computation to damage.
  Vector mapping: **A62 Automated Risk Parameter Rate-Cap Oracle Misconfiguration (Agentic Execution, No Human Gate)** (NEW VECTOR, 2026-03-10).
  Source: https://rekt.news/aave-rekt | https://governance.aave.com/t/post-mortem-exchange-rate-misallignment-on-wsteth-core-and-prime-instances/24269 | https://x.com/yieldsandmore/status/2031468808012210538 | https://www.coindesk.com/business/2026/03/10/defi-lending-platform-aave-sees-a-rare-usd27-million-liquidations-after-a-price-glitch

- **2026-03-12 — DBXen (Ethereum — ERC-2771 staking exploit)** — DBXen's staking contract was drained for 65.28 ETH (~$150K) via an ERC-2771 meta-transaction sender identity mismatch. The `burnBatch()` function used `_msgSender()` (ERC-2771 context-aware, returns actual user), but the `onTokenBurned()` callback used `msg.sender` (returns the forwarder address). DBXen also accepted a permissionless (unguarded) trusted forwarder. Combined with a fee accounting bug that backdated fresh addresses to cycle 0, the attacker spoofed their identity as the forwarder, tricked the contract into crediting them with 3 years of accumulated staking rewards, and claimed 65.28 ETH + 2,305 DXN. Funds exited via LayerZero. Detected by BlockSec Phalcon monitoring.
  **Root cause**: Mixed `msg.sender` / `_msgSender()` usage across caller-context-dependent reward logic + permissionless forwarder + fresh-address backdating bug.
  Vector mapping: **A61 ERC-2771 Meta-Transaction Sender Context Inconsistency** (NEW VECTOR, 2026-03-12).
  Source: https://www.cryptotimes.io/2026/03/12/dbxen-staking-hack-attacker-exploits-erc2771-bug-to-drain-150k/ | https://x.com/Phalcon_xyz/status/2031955394025996688

- **2026-03-12 — bonk.fun (Solana — domain hijacking)** — A bonk.fun team account was hijacked; attackers took control of the protocol's domain and injected a wallet-draining script into the live website. Team member SolportTom issued emergency X warning advising all users not to use the bonk.fun domain. No confirmed fund loss amount published. Classic domain hijack → frontend script injection pattern; users on the canonical domain exposed to malicious transaction approval requests.
  **Root cause**: Compromised team DNS/domain account → canonical domain redirected to attacker-controlled server hosting malicious frontend. Server-level injection bypasses any client-side CSP meta tags.
  Vector mapping: **D26 Frontend XSS/Injection** (2026 reinforcement: domain-level hijacking > CDN worker compromise).
  Source: https://x.com/SolportTom/status/2031930573342519702 | https://hacked.slowmist.io/

- **2026-03-10 — Gondi NFT Platform (Ethereum — Sell & Repay contract)** — The NFT lending platform Gondi's `Sell & Repay` contract (deployed February 20, 2026) contained a logic flaw in its `Purchase Bundler` function. The function verified the caller was authorized to invoke the bundler but failed to separately verify that the caller was the actual owner or borrower of the specific NFT being operated on. Attacker exploited this dual-check gap to drain 78 high-value NFTs (44 Art Blocks, 10 Doodles, 2 Beeple artworks), totaling approximately $230,000 in losses. All NFT transfers were cryptographically valid — no oracle or flash loan involved.
  **Root cause**: function-level authorization ≠ asset-level ownership verification. The bundler enforced "caller can use this function" but not "caller actually owns/has borrower rights over this specific NFT."
  Vector mapping: **A4 Access Control — NFT Purchase Bundler Missing Asset Owner Verification** (A4 sub-pattern reinforcement, not a new vector).
  Source: https://www.theblock.co/post/392909/nft-platform-gondi-moves-users-whole-230000-contract-exploit | https://hacked.slowmist.io/

- **2026-03-06 — Solv Protocol BRO Vault (EVM — Ethereum + chain-agnostic)** — Attacker exploited a double-mint vulnerability in the `BitcoinReserveOffering` (BRO) vault contract. Mechanism: `mint()` initiates an ERC721 NFT transfer → `onERC721Received()` callback fires in the same contract → `_mint()` is called inside the callback → callback returns → `mint()` calls `_mint()` AGAIN. Since the exchange rate stays constant throughout a single transaction, each call to `mint()` produces 2× the intended BRO tokens. Attacker repeated this 22 times: 135 BRO → 567,000,000 BRO. Converted 165M BRO → SolvBTC → WBTC → WETH → 1,211 ETH (~$2.7M). Fewer than 10 users affected; Solv committed to full reimbursement of 38.0474 SolvBTC. Solv offered 10% white-hat bounty. Security firm Decurity's monitoring bot detected the attack.
  Vector mapping: **A46 ERC721 Callback Reentrancy / Dual-Execution Mint** (new vector).
  Source: https://www.quillaudits.com/blog/hack-analysis/solv-protocol-exploit | https://hacked.slowmist.io/ | https://financefeeds.com/solv-protocol-exploit-drains-2-7m-in-solvbtc-from-bro-vault/

- **2026-03-05 — Step Finance shutdown (Solana — aftermath of 2026-01-31 hack)** — Step Finance (Solana DeFi aggregator), SolanaFloor, and Remora Markets announced full operational shutdown, citing inability to recover from the $27.3M stake authority hijack incident of January 31, 2026 (B36). Audit trail confirmed: the attacker who exploited Step Finance's hot device / executive spear-phishing used `StakeAuthorize` instructions to redirect 261,854 SOL in ~90 minutes. No on-chain code flaw was involved — all audited contracts worked correctly. Operational outcome confirms B36's key insight: private-key compromise via social engineering can terminate a protocol regardless of code security posture.
  Vector mapping: **B36 Social-Engineering-to-Stake-Authority-Hijack** (aftermath/confirmation).
  Source: https://cryptopotato.com/the-end-of-step-finance-how-a-wallet-compromise-killed-the-solana-defi-aggregator/

- **2026-03-02/03 — Ledger/Canissolana (Solana)** — Reported unauthorized drain of ~$30,000 USDC from a hardware-wallet-secured Solana account. User claims no recent dApp interaction, no seed phrase exposure. Community analysis points to a previously signed `Approve` instruction that set an attacker-controlled delegate on the user's USDC ATA. SPL token delegates persist until explicitly revoked; the attacker waited, then called `TransferChecked` using only their delegate authority — no victim signature required. SOL (~2,000) was not drained (separate account authority). USDC drained to Bitget exchange. Ledger began investigation 2026-03-03.  
  Vector mapping: **B44 SPL Token Account Persistent Delegate Drain** (new).  
  Source: https://www.cryptotimes.io/2026/03/03/ledger-under-scrutiny-30k-usdc-vanishes-from-air-gapped-wallet/

- **2026-03-02 — Inverse Finance / LlamaLend (Ethereum)** — Attacker used ~$30M flash loan to inflate sDOLA (wrapped DOLA ERC4626 vault) share price via direct donation to vault `totalAssets`. 27 users whose LlamaLend collateral positions were denominated in sDOLA were forcibly liquidated as their collateral appeared undercollateralized after the artificial price spike. Profit: ~$240K. Inverse Finance itself was not breached; the exploit path ran through LlamaLend's collateral oracle reading sDOLA exchange rate.  
  Vector mapping: **A40 ERC4626/Share-Price Donation Attack**, **A2 Flash Loan + Price Manipulation**.  
  Source: https://www.cryptotimes.io/2026/03/02/inversefinance-faces-240k-loss-in-dola-manipulation-alert/ | https://hacked.slowmist.io/

- **2026-02-27 — SOF token + LAXO token (BNB Smart Chain)** — SOF (Feb 14, ~$248K) and LAXO (Feb 22, ~$190K). Both exploited a burn-path fee-exempt logic flaw. Attacker flash-borrowed ~$590M, swapped into pool token, sent tokens to fee-exempt mining contract, burned tokens (changing pool ratio denominator), then sold the 875 reward SOF tokens at the now-inflated rate to drain the entire pool BSC-USD. LAXO copycat attacker struck within 13 minutes of the original exploit.  
  Vector mapping: **A41 Burn-Path Fee-Exempt Flash Loan Amplification**, **A2 Flash Loan + Price Manipulation**.  
  Source: https://www.cryptotimes.io/2026/02/27/flash-loan-attack-drains-438k-from-sof-and-laxo-on-bnb-chain/

- **2026-02-25 — Holdstation DeFAI Smart Wallet (World Chain / BNB Chain / zkSync)** — Second exploit against Holdstation in <30 days (prior incident Jan 2026, ~$100K). 462,000 USDT confirmed stolen. Root cause officially under investigation; reported attack vector is MFA bypass ("Hacker bypassed MFA and drained user funds in 2 min"). Jan incident drained WLD/USD1/BNB/BERA across World Chain, BSC, Berachain, zkSync → ETH → BTC via THORChain, suggesting private key or session credential compromise enabling multi-chain sweep.  
  Vector mapping (tentative): **B15 Key Compromise / Session Credential Theft**. Full vector pending mechanism confirmation.  
  Note: "DeFAI" wallet integrates AI intent layer with on-chain execution — if the session layer controls signing authority, AI prompt-injection (B29) or credential theft may be amplified path.  
  Source: https://hacked.slowmist.io/ | https://x.com/HoldstationW/status/2026487570751008932

- **2026-02-27 — Stake Nova (Solana)** — Unchecked validation in `RedeemNovaSol()` was flash-loan-amplified to drain protocol liquidity (~$2.39M).  
  Vector mapping: **A2 Flash Loan + Price/Path Manipulation**, **A10 Logic Bug**.  
  Source: https://hacked.slowmist.io/

- **2026-02-26 — FOOMCASH** — Copycat exploit abused zkSNARK verification-key/configuration drift, enabling forged-proof acceptance and ~$2.26M drain.  
  Vector mapping: **A38 ZK Verifier Key Misbinding / Proof-Parameter Drift**.  
  Source: https://hacked.slowmist.io/ | https://www.cryptotimes.io/2026/02/26/foomcash-loses-2-26m-in-copycat-zksnark-exploit/

- **2026-02-22 — YieldBlox (Stellar)** — Attacker manipulated thin-liquidity collateral valuation, then borrowed against inflated oracle-derived value and drained ~$10.97M.  
  Vector mapping: **A3 Oracle Manipulation**.  
  Source: https://rekt.news/yieldblox-rekt

- **2026-02-21 — IoTeX ioTube bridge** — Validator private-key compromise granted admin control and drained assets (~$4.4M).  
  Vector mapping: **B15 Key Compromise**.  
  Source: https://hacked.slowmist.io/

- **2026-02-18 — Moonwell** — Oracle configuration error treated a cbETH/ETH ratio as USD, triggering liquidations and ~$1.78M bad debt.  
  Vector mapping: **A3 Oracle Manipulation**, **A10 Logic Bug**.  
  Source: https://hacked.slowmist.io/

- **2026-02-02 — CrossCurve (formerly EYWA) bridge (Multi-chain — Arbitrum primary)** — CrossCurve's cross-chain bridge protocol was attacked via a gateway verification bypass in the `ReceiverAxelar` contract. The `expressExecute` function had no `onlyGateway` caller check — any address could call it with fabricated cross-chain message payloads. Attacker directly called the receiver function (bypassing the Axelar relay entirely), triggering unauthorized token unlocks on the `PortalV2` contract across multiple networks. ~$3M drained; most activity on Arbitrum, converting stolen tokens to WETH via CoW Protocol. QuillAudits post-mortem confirmed access control was the root cause.
  Vector mapping: **A48 Unguarded Cross-Chain Receiver Function** (NEW), **A4 Access Control**.
  Source: https://www.scworld.com/brief/crosscurve-bridge-loses-3-million-in-smart-contract-exploit | https://thecyberexpress.com/crosscurve-bridge-3m-cyberattack/ | https://quillaudits.medium.com/crosscurve-1-4m-exploit-c2ef752c4e84

- **2026-02-23 — WLFI USD1** — Co-founder account compromise + coordinated social-engineering/FUD attempt; no confirmed loss reported.  
  Vector mapping: **B15 Key Compromise / Social Engineering**.  
  Source: https://hacked.slowmist.io/

- **2026-01-31 — Step Finance (Solana)** — Executive device(s) compromised via phishing ("well-known attack vector"). Stake authorization transferred to attacker wallet; 261,854 SOL (~$27.3M) unstaked and drained in 90 minutes. Smart contracts audited and bug-bounty covered — none of it mattered. $4.7M recovered via Token-22 freeze. STEP token down 93%.  
  Vector mapping: **B33 OpSec & Key Management / Stake Authority Hijack**.  
  Source: https://rekt.news/step-finance-rekt | https://x.com/StepFinance_/status/2018379876642804213

- **2026-01-21 — Saga / SagaEVM (Cosmos EVM)** — Helper contract crafted custom IBC precompile messages mimicking collateral deposits. Bridge accepted forged payloads with no source-chain verification → $7M Saga Dollar minted from thin air → converted to 2,000+ ETH on Ethereum. Root cause in Ethermint codebase; multiple EVM chains in blast radius. Depeg -25% to $0.75.  
  Vector mapping: **A32 Cross-Chain Bridge Message Forgery**.  
  Source: https://rekt.news/saga-rekt | https://x.com/cosmoslabs_io/status/2014428829423706156

- **2026-02 — YO Protocol** — Vault operator submitted a $3.84M swap with broken/zeroed slippage parameters; $3.71M lost to unfavorable routing. Team backstopped and delayed disclosure 2 days.  
  Vector mapping: **B35 Keeper Parameter Misconfiguration**.  
  Source: https://rekt.news/yo-protocols-slippage-bomb

- **2026-02 — Makina Protocol** — Flash loan used to manipulate a permissionless oracle feeding a DeFi protocol; $4.13M extracted. MEV bots front-ran attacker and captured most of the stolen funds.  
  Vector mapping: **A2 Flash Loan + Price Manipulation**, **A3 Oracle Manipulation**.  
  Source: https://rekt.news/makina-rekt

- **2026-03-04 — Sillytuna (Ethereum — Address Poisoning + Physical Coercion)** — Long-time on-chain whale "Sillytuna" lost 23,596,293 aEthUSDC (~$24M) via a two-phase attack. Phase 1 (digital): Attacker identified target from public on-chain footprint, generated a vanity look-alike wallet address (matching first/last 4–6 chars of victim's regular counterpart), and sent dust transactions to poison the victim's transaction history. When victim initiated a large transfer, they copied the look-alike address from recent transaction history. Phase 2 (physical): Reporting indicates physical coercion was also involved, preventing the victim from recovering or blocking the transaction. Funds transferred to attacker address (0x6fef…a246032); PeckShield flagged the on-chain movement in real time. Funds subsequently laundered to Monero. No smart contract vulnerability involved — all on-chain transactions were cryptographically valid. Represents the highest-profile confirmed address poisoning incident to date.
  Vector mapping: **B53 Address Poisoning + Physical Coercion Hybrid Attack** (new vector).
  Source: https://finance.yahoo.com/news/crypto-influencer-sillytuna-loses-24m-071842352.html | https://en.spaziocrypto.com/hack/sillytuna-24-million-stolen-with-address-poisoning/
