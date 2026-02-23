# Skill Intake Threat Model (v0)

## Assets to protect
- host filesystem integrity (esp. repos, SSH keys, config)
- secrets (API keys, tokens, cookies, `.npmrc`, `.env`, keychains)
- network perimeter (exfiltration, lateral movement)
- automation reliability (cron spam, infinite loops, stealth persistence)

## Primary threat actors
- malicious third-party skill authors
- compromised upstream dependency / supply-chain attacks
- well-meaning but unsafe skills (overbroad permissions, destructive defaults)

## High-risk behaviors
- executing arbitrary shell commands
- self-updating or downloading binaries at runtime
- hidden network calls / telemetry
- writing outside workspace / persistence (launchd/systemd/crontab)
- reading local credentials without explicit user request

## Gate guarantees (target)
- block or quarantine high-risk packages by default
- make behavior explicit before execution
- ensure rewrite into minimal, auditable internal skills
