# Composition Attacks

Individually safe operations combined to create exploits.

## Pattern: Cross-Instruction Composition
Operations A and B are each safe, but A followed by B in the same TX creates an inconsistent state.

### Example: Mint + Redeem in Same Slot
- Mint: safe (checks CR, charges fee)
- Redeem: safe (checks balance, returns collateral)
- Combined: mint with stale high price → redeem with current low price = profit

### Example: Deposit + Withdraw + Claim
- Each operation updates different counters
- But combined, reward tracking gets confused
- Historical: Popsicle Finance ($20M)

## Pattern: Cross-Protocol Composition
Protocol A and Protocol B are each safe, but interaction creates exploit.

### Example: Flash Loan from Protocol A → Exploit Protocol B
- A: Safe lending (loan + repay in same TX)
- B: Safe (except assumes capital = economic commitment)
- Combined: B can't distinguish real capital from flash-borrowed

### Example: Oracle from Protocol A → Pricing in Protocol B
- A: Safe AMM (prices reflect supply/demand)
- B: Safe oracle consumer (reads A's price)
- Combined: Manipulate A's pool → B acts on wrong price

## Pattern: Cross-Time Composition
Operations at time T1 and T2 are each safe, but the sequence creates exploit.

### Example: Stake → Wait for Price Change → Unstake
- Stake: safe
- Unstake: safe
- But: staking position gains value from external event without risk

## Pattern: Cross-Chain Composition
Bridge message at chain A and action at chain B create inconsistent state.

## Detection Methodology

For each pair of protocol operations (A, B):
1. List state changes of A
2. List preconditions of B
3. Ask: "Does A's state change affect B's preconditions?"
4. If yes: test A→B and B→A sequences for value extraction

For N operations, this is O(N²) pairs — automate with invariant tests.
