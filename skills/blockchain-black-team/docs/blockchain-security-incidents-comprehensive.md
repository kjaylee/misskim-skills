# Blockchain Security Incidents — Comprehensive Timeline

> Scope: real-world incidents with explicit mechanisms. Entries without confirmed mechanisms are intentionally omitted.

## 2026
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
