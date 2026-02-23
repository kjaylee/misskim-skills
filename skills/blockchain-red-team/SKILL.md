---
name: blockchain-red-team
description: Offensive penetration testing of blockchain protocols using novel attack techniques beyond known historical incidents. Use when performing advanced security testing, developing new exploit techniques, bypassing existing defenses, or stress-testing patched code on Solana (Anchor), Ethereum (Solidity), or any programmable blockchain. Triggers on red team, penetration test, exploit development, bypass testing, defense evasion, zero-day research, or advanced offensive security of DeFi/blockchain code.
---

# Blockchain Red Team — Novel Attack Technique Research & Exploitation

Develop and execute attack techniques that **haven't been seen in the wild yet**. While the Black Team maps historical incidents, the Red Team invents the next generation of attacks.

## When to Use

- Post-patch bypass testing (find new routes around Blue Team fixes)
- Zero-day research on smart contract patterns
- Novel economic attack modeling
- Defense evasion technique development
- Advanced MEV/sandwich/frontrunning research
- Pre-audit offensive stress testing

## Red Team vs Black Team

| Aspect | Black Team | Red Team |
|---|---|---|
| Time orientation | Past → Present | Present → Future |
| Source | Historical incidents | CTFs, audits, papers, original research |
| Goal | Map known patterns | Discover unknown patterns |
| Output | "This happened before" | "This could happen next" |

## Research Sources

### Primary (check weekly)
1. **CTF Writeups** — Paradigm CTF, Ethernaut, Damn Vulnerable DeFi, Capture the Ether
2. **Audit Reports** — Trail of Bits, OtterSec, Neodyme, Halborn, Certora, Zellic, Spearbit
3. **Academic Papers** — arXiv cs.CR, ACM CCS, USENIX Security, IEEE S&P
4. **MEV Research** — Flashbots, Jito Labs, Skip Protocol, MEV Share

### Secondary
5. **Framework Changes** — Anchor releases, SPL updates, OpenZeppelin updates
6. **Language Advisories** — RustSec, npm advisories, Solidity compiler bugs
7. **Formal Verification Findings** — Certora rules, Echidna/Medusa campaigns

## Attack Development Methodology

### Phase 1: Technique Discovery
Scan sources for novel patterns. For each discovery:
- What is the **core primitive** being exploited?
- Is this a known pattern variant or genuinely new?
- Cross-check against Black Team `references/attack-matrix.md`

### Phase 2: Weaponization
Transform research finding into concrete attack:
1. Identify **target surface** in protocol code (file:line)
2. Determine **preconditions** (what state is needed)
3. Develop **attack sequence** (step-by-step TX/action plan)
4. Estimate **impact** (funds at risk, protocol disruption)
5. Write **PoC sketch** (pseudocode or test case)

### Phase 3: Defense Bypass Research
For each existing defense in target code:
1. Read the defense implementation
2. Ask: "What assumption does this defense make?"
3. Ask: "Can that assumption be violated?"
4. Try **at least 3 bypass approaches**:
   - Timing-based (race the defense)
   - State-based (reach unexpected state first)
   - Composition-based (combine with another operation)

### Phase 4: Novel Economic Attacks
Beyond code bugs, explore economic mechanism failures:
- Game-theoretic analysis of protocol incentives
- Multi-agent collusion scenarios
- Cross-protocol composability attacks
- Liquidity crisis cascading models

## Technique Categories

### T1: Defense Bypass
Techniques to circumvent known patches. See `references/bypass-techniques.md`.

### T2: Composition Attacks
Combining individually safe operations into exploits. See `references/composition-attacks.md`.

### T3: Timing Attacks
Exploiting slot/block/epoch boundaries. See `references/timing-attacks.md`.

### T4: Economic Mechanism Attacks
Game-theoretic and incentive-based exploits. See `references/economic-attacks.md`.

## Report Format

```markdown
# Red Team Report — {Protocol Name}

## New Techniques Discovered: N
## Existing Defense Bypasses Found: N

## {ID}: {Technique Name}
- **Category**: T1/T2/T3/T4
- **Novelty**: New / Variant of {existing}
- **Source**: {CTF/paper/original research}
- **Target Surface**: {file:line}
- **Preconditions**: {required state}
- **Attack Sequence**: {numbered steps}
- **Impact**: {funds/disruption estimate}
- **PoC**: {code}
- **Defense Recommendation**: {specific fix}
```

## Cycling with Blue Team

Red Team finds → Blue Team fixes → Red Team re-tests (bypass attempts):
```
Red R1 → Blue fix → Red R2 (bypass) → Blue fix → ... → No bypasses found
```

On repeat runs: focus exclusively on **bypassing new patches**.
