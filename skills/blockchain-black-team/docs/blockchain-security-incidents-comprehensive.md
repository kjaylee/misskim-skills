# Blockchain Security Incidents — Comprehensive Timeline

> Scope: real-world incidents with explicit mechanisms. Entries without confirmed mechanisms are intentionally omitted.

## 2026
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
