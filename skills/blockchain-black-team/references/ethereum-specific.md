# Ethereum/EVM-Specific Attack Patterns

## Storage & Proxy Patterns

### Delegatecall + Storage Collision
```solidity
// Proxy delegates to implementation
// If storage layouts don't match → state corruption
// Historical: Parity Multisig ($150M frozen)
```

### UUPS Upgrade Attack
```solidity
// If upgradeTo() lacks access control in implementation
// Attacker calls upgradeTo(malicious) directly on implementation
// Historical: multiple UUPS vulnerabilities
```

### Uninitialized Implementation
```solidity
// Implementation contract not initialized after deployment
// Attacker calls initialize() → becomes owner
// Defense: initializer in constructor or _disableInitializers()
```

## Reentrancy Patterns

### Classic Reentrancy
```solidity
// VULNERABLE
function withdraw(uint amount) {
    require(balances[msg.sender] >= amount);
    (bool ok,) = msg.sender.call{value: amount}("");  // callback
    balances[msg.sender] -= amount;  // too late
}
```

### Cross-Function Reentrancy
Attacker re-enters a different function that reads stale state.

### Cross-Contract Reentrancy
Attacker re-enters through a different contract that shares state.

### Read-Only Reentrancy (Vyper/Curve)
```python
# Vyper @nonreentrant only protects writes
# Read functions can be called during reentrancy
# Returns stale values → price manipulation
# Historical: Curve/Vyper 2023 ($70M)
```

## ERC-20 Patterns

### Infinite Approval Exploit
```solidity
// User approves protocol for type(uint256).max
// If protocol is compromised → drain all approved tokens
// Historical: BadgerDAO ($120M via frontend injection)
```

### Fee-on-Transfer Tokens
```solidity
// VULNERABLE: assumes received == sent
token.transferFrom(user, vault, amount);
// Actual received may be amount - fee
// Defense: check balance before/after
```

### Rebasing Tokens
Balance changes without transfers. Accounting breaks if not handled.

## Flash Loan Patterns

### Single-TX Manipulation
```
1. Flash borrow $100M
2. Swap on AMM → move price
3. Interact with target protocol at manipulated price
4. Swap back → restore price
5. Repay flash loan + fee
6. Profit from mispriced interaction
```

### Governance Flash Loan
```
1. Flash borrow governance tokens
2. Create + vote on malicious proposal (if no timelock)
3. Execute proposal → drain treasury
4. Return tokens
// Historical: Beanstalk ($182M)
```

## Oracle Patterns

### AMM as Oracle
Using Uniswap/Curve pool price as oracle → manipulable via flash loan.
**Defense**: Use TWAP, Chainlink, or multi-source oracles.

### Chainlink Stale Price
```solidity
(, int price,, uint updatedAt,) = priceFeed.latestRoundData();
require(block.timestamp - updatedAt < MAX_STALENESS);
require(price > 0);
```

## EVM Defense Checklist

1. ☐ Reentrancy guards on all state-changing external calls
2. ☐ CEI pattern (Checks-Effects-Interactions)
3. ☐ Access control on all admin functions
4. ☐ Proxy storage layout verified (no collisions)
5. ☐ Implementation initialized / disabled
6. ☐ Oracle staleness + validity checks
7. ☐ Flash loan resistance (TWAP, cooldowns, commit-reveal)
8. ☐ Approval management (no infinite approvals in protocol)
9. ☐ Fee-on-transfer / rebasing token handling
10. ☐ Timelock on governance actions
11. ☐ Upgrade authority secured (multisig + timelock)
12. ☐ No selfdestruct in libraries (Parity bug)
