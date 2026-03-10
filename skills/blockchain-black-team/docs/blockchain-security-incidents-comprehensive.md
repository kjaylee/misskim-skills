# Blockchain Security Incidents — Comprehensive Timeline

> Scope: real-world incidents with explicit mechanisms. Entries without confirmed mechanisms are intentionally omitted.

## 2026
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
