---
name: game-marketing-context
description: >
  Shared game marketing context provider. Generates and maintains per-game marketing
  context documents that other skills (game-marketing, content-strategy, store-listing)
  automatically reference. Based on coreyhaines31/product-marketing-context pattern,
  adapted for indie HTML5/Godot game portfolio.
dependencies: []
triggers:
  - "새 게임 마케팅 컨텍스트 생성"
  - "게임 컨텍스트 업데이트"
  - "마케팅 포지셔닝"
  - "타겟 오디언스"
  - "경쟁 분석"
---

# 🎮 Game Marketing Context

Shared marketing context for the **eastsea.monster** indie game portfolio.
Other skills MUST check for context files before executing marketing tasks.

---

## How This Skill Works

### Context File Location

```
.openclaw/game-context/
├── _portfolio.md          ← Portfolio-wide context (this skill generates)
├── {game-slug}.md         ← Per-game context (generated per game)
└── _platform-guides.md    ← Platform-specific messaging reference
```

### Cross-Skill Reference Pattern

**All marketing-related skills MUST start with:**

```markdown
## Step 0: Load Context
1. Check if `.openclaw/game-context/_portfolio.md` exists → read it
2. If working on a specific game, check `.openclaw/game-context/{game-slug}.md` → read it
3. If neither exists, run `game-marketing-context` skill to generate them first
```

This ensures consistent messaging, personas, and positioning across all outputs.

---

## Portfolio Context (Always Active)

### Who We Are

| Field | Value |
|-------|-------|
| **Brand** | eastsea.monster (동해괴물) |
| **Portfolio** | 30+ HTML5/Godot games, 144+ tools |
| **Stack** | Rust(WASM) + Godot 4.6 (JS/TS prohibited) |
| **Primary Platform** | Telegram Mini App |
| **Secondary** | itch.io → mobile stores → Steam |
| **Differentiator** | Zero-install, instant-play, cross-platform indie games |
| **Revenue Model** | Ads (rewarded/interstitial) + Telegram Stars + cross-promo |

### Voice & Tone

- **Personality:** Playful, slightly irreverent, dev-friendly
- **Language:** English primary, Korean secondary (한국어)
- **Avoid:** Corporate jargon, hype without substance, crypto-bro language
- **Embrace:** Honest dev stories, "made by one person" authenticity, gameplay-first messaging
- **Emoji usage:** Moderate — enhance, don't overwhelm

---

## Target Audience Personas

> Full persona details: [`personas.md`](./personas.md)

### Quick Reference

| Persona | Age | Platform | Plays When | Key Motivation |
|---------|-----|----------|------------|----------------|
| 🚇 **Commuter Casual** | 18-35 | Telegram | Transit, breaks | Kill time, feel progress |
| 🏠 **Bedroom Indie Fan** | 16-28 | itch.io, Steam | Evenings, weekends | Discover unique experiences |
| 📱 **Mobile Snacker** | 25-45 | Google Play, App Store | Micro-moments | Quick dopamine, compete with friends |
| 🤖 **Telegram Native** | 20-35 | Telegram | In-chat, groups | Social flex, group challenges |
| 🎮 **Web Game Browser** | 14-30 | Poki, CrazyGames | Boredom, procrastination | Instant play, no commitment |

---

## Platform-Specific Messaging

> Full platform guide: [`platform-messaging.md`](./platform-messaging.md)

### One-Line Positioning Per Platform

| Platform | Positioning | Tone |
|----------|-------------|------|
| **Telegram Mini App** | "Play instantly in your chat — no download, no wait" | Casual, social |
| **itch.io** | "Handcrafted indie games by a solo dev — play free in your browser" | Authentic, dev-community |
| **Google Play / App Store** | "Quick, addictive games for your daily break" | Polished, mainstream |
| **Steam** | "Carefully crafted indie experiences worth your time" | Premium, curated |
| **Poki / CrazyGames** | "Jump in and play — no signup needed" | Ultra-casual, instant |

---

## Competitive Positioning

> Full framework: [`competitive-positioning.md`](./competitive-positioning.md)

### Portfolio Positioning Statement

> **For** mobile-first casual gamers **who** want instant entertainment without app store friction,
> **eastsea.monster** is a **portfolio of 30+ browser-based indie games** that delivers
> **zero-install, instant-play experiences across Telegram and the web.**
> **Unlike** traditional mobile games that require downloads and permissions,
> **we** let you play in one tap, right where you already are.

### JTBD Four Forces (Portfolio-Level)

| Force | Description |
|-------|-------------|
| **Push** (away from current) | "App stores are bloated — I just want to play something quick" |
| **Pull** (toward us) | "One link, instant play, no install — refreshingly simple" |
| **Habit** (status quo inertia) | "I already have games on my phone, why try something new?" |
| **Anxiety** (fear of switching) | "Will a browser game actually be fun? Will it feel cheap?" |

**Our job:** Maximize Push + Pull, minimize Habit + Anxiety through instant-play demos and social proof.

---

## Feature-Benefit Mapping

> Full templates: [`feature-benefit-mapping.md`](./feature-benefit-mapping.md)

### Portfolio-Level Map

| Feature | Benefit | Message |
|---------|---------|---------|
| HTML5/WASM | Plays on any device | "Play on phone, tablet, or desktop — your progress follows you" |
| Telegram integration | Zero friction | "Tap a link, you're playing. That's it." |
| 30+ games | Something for everyone | "Puzzle lover? Action fan? We've got you covered" |
| Solo dev | Rapid updates | "Tell me what you want — I'll ship it this week" |
| No ads until rewarded | Respect for player time | "Ads are optional — watch one to earn rewards, or just play" |
| Leaderboards | Social competition | "Beat your friends. Prove you're the best." |
| Daily check-in | Habit loop | "Come back daily — your rewards stack up" |
| Cross-game rewards | Portfolio engagement | "Play our other games to unlock exclusive items" |

---

## Launch Checklist with Marketing Touchpoints

> Full checklist: [`launch-checklist.md`](./launch-checklist.md)

### Quick View: Launch Timeline

```
D-7  ── Pre-launch context & assets
D-3  ── Teaser campaign starts
D-0  ── Launch day blitz
D+1  ── Community engagement
D+3  ── Performance review & iterate
D+7  ── First weekly report
D+14 ── Content routine established
D+30 ── Growth assessment & pivot/scale decision
```

---

## Generating Per-Game Context

When a new game needs marketing, generate a context file using the template:

### Auto-Draft Sources

Read these files from the game project to auto-generate context:

| Source File | Extracts |
|-------------|----------|
| `project.godot` | Game name, version, features, window size |
| `export_presets.cfg` | Target platforms, export settings |
| `README.md` | Description, screenshots, gameplay |
| `index.html` / landing page | User-facing copy, meta tags |
| Game's `package.json` or `Cargo.toml` | Dependencies, version |
| In-game strings / localization files | Player-facing language |

### Context Template

Use [`CONTEXT-TEMPLATE.md`](./CONTEXT-TEMPLATE.md) to generate per-game files.

### Sections to Fill

1. **Game Overview** — Name, genre, tagline, elevator pitch
2. **Target Players** — Which personas (from above) + game-specific refinements
3. **Core Loop** — What players do repeatedly (the "verb")
4. **Unique Hook** — What makes this game different from 1000 others
5. **Competition** — 3-5 similar games + our advantages
6. **Player Language** — Verbatim quotes from playtesters / reviews
7. **Platform Strategy** — Which platforms, in what order, with what messaging
8. **Visual Assets** — Screenshots, GIFs, video clips available
9. **Proof Points** — Play count, ratings, notable achievements
10. **Goals** — DAU target, revenue target, viral coefficient target

---

## Verbatim Player Language Collection

**Critical:** Collect exact words players use. Don't paraphrase.

### Sources

- Telegram group messages about our games
- itch.io comments and ratings
- Reddit threads mentioning our games
- Direct feedback in game channels
- App store reviews (when applicable)

### Format

```markdown
## Player Language Bank

### Positive
- "이거 중독성 미쳤다" — Telegram user, 2026-01
- "finally a game I can play without downloading anything" — Reddit, r/WebGames
- "the art style is so clean" — itch.io comment

### Negative (pain points to address)
- "I wish there were more levels" — itch.io
- "gets repetitive after 10 minutes" — Telegram feedback

### How they describe us to others
- "it's like a mini arcade in Telegram"
- "browser games but actually good"
```

**Use these exact phrases in marketing copy.** Real player words convert better than anything we write.

---

## Maintenance

### When to Update Context

- New game launched → Generate per-game context
- Major game update → Update game-specific sections
- New platform added → Update platform messaging
- Significant player feedback collected → Update player language bank
- Quarterly → Review and refresh all context files

### Context Freshness Check

```
Last portfolio context update: [DATE]
Per-game contexts: [COUNT] games covered
Player language entries: [COUNT] quotes collected
```

---

*Absorbed from: coreyhaines31/product-marketing-context pattern (2026-02-12)*
*Adapted for: indie HTML5/Godot game portfolio | eastsea.monster*
