# 📡 Platform-Specific Messaging Guide

Tailored messaging, tone, copy guidelines, and constraints per distribution platform.
Referenced by: `game-marketing-context/SKILL.md`

---

## Distribution Priority (Directive)

```
🥇 Telegram Mini App  →  🥈 itch.io  →  🥉 Google Play / App Store  →  4️⃣ Steam
```

---

## 1. Telegram Mini App (Primary)

### Platform Context
- **Audience:** 950M+ monthly users, 300M+ daily
- **Behavior:** In-chat, social, fast-switching
- **Monetization:** Telegram Stars + Ads (PropellerAds, AdsGram, Monetag)
- **Constraints:** Mini App webview, mobile-first, variable network speed

### Messaging Framework

| Element | Guideline |
|---------|-----------|
| **Tone** | Casual, social, emoji-friendly, group-chat energy |
| **Key Phrase** | "Play instantly — right here in Telegram" |
| **CTA Style** | "▶️ Play Now" / "🏆 Challenge Friends" / "🎮 Start Playing" |
| **Avoid** | "Download", "Install", "Sign up", external links |
| **Languages** | English (primary), Russian (CIS market), Korean |

### Copy Templates

#### Bot Description (512 chars)
```
🎮 {Game Name} — {Tagline}

{One sentence about core mechanic}
{One sentence about what makes it fun}

✨ Features:
• {Feature 1} → {Benefit}
• {Feature 2} → {Benefit}
• {Feature 3} → {Benefit}

🏆 Compete with friends on the leaderboard!
🎁 Daily rewards — come back every day!

Tap ▶️ to play instantly — no download needed!
```

#### Inline Share Message
```
🎮 I just scored {score} in {Game Name}! Can you beat me?
👉 Play now: {deep_link}
```

#### Channel Launch Post
```
🚀 NEW GAME ALERT!

🎮 {Game Name} — {Tagline}

{2-3 sentence hook}

⚡ Instant play — no download
🏆 Global leaderboard
🎁 Daily rewards
👥 Challenge your friends!

👉 Play now: {deep_link}

#newgame #{genre} #telegramgames
```

### Platform-Specific Tips
- Deep links: `https://t.me/{bot}?start={param}` or `https://t.me/{bot}/{app}`
- Inline mode for sharing scores — increases virality 3-5x
- Bot menu button should open game directly (no landing screen)
- Loading must be < 3 seconds (users bail after 5s in Telegram)
- Use Telegram's native share dialogs, not custom share buttons

---

## 2. itch.io

### Platform Context
- **Audience:** Indie game enthusiasts, game jam participants, aspiring devs
- **Behavior:** Browse-and-discover, read descriptions, value dev stories
- **Monetization:** "Pay what you want" / Free with tip jar / Paid ($1-10)
- **Constraints:** Browser embed (iframe), needs good page design

### Messaging Framework

| Element | Guideline |
|---------|-----------|
| **Tone** | Authentic, humble, developer-to-player, personal |
| **Key Phrase** | "A {genre} game made with love by a solo dev" |
| **CTA Style** | "Play in browser" / "Download for free" |
| **Avoid** | Marketing-speak, hype, "BEST GAME EVER" |
| **Language** | English (itch.io is English-dominant) |

### Copy Templates

#### Game Page Description
```markdown
# {Game Name}

{Tagline — one evocative sentence}

## About

{2-3 paragraph description. Tell a story:
- What inspired you
- What the game is about
- What makes it special}

## How to Play

{Simple, clear instructions. 3-5 bullet points.}

## Features

- {Feature 1}
- {Feature 2}
- {Feature 3}
- {Feature 4}

## Made With

Built with Godot 4.6 + Rust/WASM by a solo developer.
Part of the [eastsea.monster](https://eastsea.monster) game collection.

## Feedback

Love it? Hate it? Found a bug? 
Leave a comment or rate the game — every bit of feedback helps! 💚
```

#### Devlog Post
```markdown
# {Update Title} — {Game Name} Devlog #{number}

{Personal hook — what happened, what you learned, what changed}

## What's New
- {Change 1}
- {Change 2}
- {Change 3}

## Behind the Scenes
{Interesting dev story, challenge overcome, or decision made}

## What's Next
{What you're working on, what you want feedback on}

---
Thanks for playing! 🎮
```

### Platform-Specific Tips
- Tags matter hugely: use all relevant tags (genre, mechanic, platform, jam)
- Screenshots: 3-5, show gameplay not menus
- GIF as cover image = 2x more clicks than static image
- First 2 sentences of description show in search — make them count
- Join game jams — itch.io's discovery algorithm favors jam entries
- Devlog posts boost visibility — write one at launch minimum

---

## 3. Google Play / App Store (Mobile Stores)

### Platform Context
- **Audience:** Mainstream mobile gamers, 4B+ active devices
- **Behavior:** Search-driven, screenshot-scanners, review-readers
- **Monetization:** IAP, subscriptions, ads (AdMob/ironSource)
- **Constraints:** ASO rules, review process, size limits, store guidelines

### Messaging Framework

| Element | Guideline |
|---------|-----------|
| **Tone** | Polished, mainstream, benefit-focused |
| **Key Phrase** | "Fun, free, and made for your daily break" |
| **CTA Style** | "Install" (forced by store) — optimize everything around it |
| **Avoid** | "Indie" (mainstream users don't care), dev jargon, "Telegram" |
| **Languages** | Localize for target markets (EN, KO, RU, PT-BR, ES) |

### ASO (App Store Optimization) Templates

#### Title (30 chars)
```
{Game Name}: {Core Benefit}
Example: "TilePop: Quick Puzzle Fun"
```

#### Short Description (80 chars, Google Play)
```
{Action verb} {core mechanic} in this {adjective} {genre} game. Free to play!
Example: "Match & pop tiles in this colorful puzzle game. Free to play!"
```

#### Full Description (First 3 Lines = Visible)
```
🧩 {Game Name} — {Tagline}

{Hook sentence that makes them keep reading}
{What the game is in plain language}
{Why it's fun}

FEATURES:
★ {Benefit 1} — {what it means for the player}
★ {Benefit 2} — {what it means for the player}
★ {Benefit 3} — {what it means for the player}
★ {Benefit 4} — {what it means for the player}

PERFECT FOR:
• Quick breaks at work or school
• Commuting on the train
• Relaxing before bed
• Challenging friends

Download free. Play instantly. Have fun! 🎮
```

### Screenshot Guidelines
1. **Screenshot 1:** Hero shot — game at its most visually exciting moment
2. **Screenshot 2:** Core mechanic in action with caption
3. **Screenshot 3:** Progression/rewards
4. **Screenshot 4:** Social features (leaderboard, challenges)
5. **Screenshot 5:** Variety (different levels, modes)

**Rules:**
- Include captions on screenshots (benefit-focused, 3-5 words)
- Use device frames (modern phones)
- Consistent color scheme
- Vertical (portrait) for phones, horizontal for tablets

### Platform-Specific Tips
- Ratings matter enormously: prompt for rating after positive moments (not after ads)
- Reply to ALL reviews (positive and negative)
- Update regularly (Google Play rewards update frequency)
- Size: keep under 100MB, ideally under 50MB
- A/B test store listing via Google Play Experiments

---

## 4. Steam

### Platform Context
- **Audience:** Dedicated gamers, 130M+ monthly active
- **Behavior:** Wishlist-driven, review-dependent, sale-hunters
- **Monetization:** Premium ($2.99-14.99 for indie), DLC, bundles
- **Constraints:** Steam Direct fee ($100/game), review threshold for visibility

### Messaging Framework

| Element | Guideline |
|---------|-----------|
| **Tone** | Confident, premium-feeling but approachable |
| **Key Phrase** | "A carefully crafted indie experience" |
| **CTA Style** | "Add to Wishlist" (pre-launch) / "Play Now" (post-launch) |
| **Avoid** | "Mobile game", "browser game", "casual" (derogatory on Steam) |
| **Language** | English (primary), localize description for key markets |

### Copy Templates

#### Short Description (Steam, < 300 chars)
```
{Game Name} is a {adjective} {genre} game where you {core action}. 
{What makes it unique in one sentence}. 
{Emotional hook or challenge statement}.
```

#### About This Game (Long Description)
```
{Opening hook — evocative, sets the mood}

{Core gameplay paragraph — what you DO in this game}

{What makes it special paragraph — unique mechanics, art style, feel}

KEY FEATURES:
• {Feature 1 — written as a benefit}
• {Feature 2}
• {Feature 3}
• {Feature 4}
• {Feature 5}

{Closing — emotional appeal or challenge}

---
From the solo developer behind eastsea.monster — a collection of 30+ 
handcrafted games. Made with Godot + Rust, with love.
```

### Platform-Specific Tips
- **Wishlists are everything** — start collecting before launch
- **10 reviews** = shows on store page. **50 reviews** = eligible for promotion
- **Steam tags** affect discovery — choose carefully
- **Capsule art** is your billboard — invest in it
- **Demo** available = 2x more wishlists
- **Steam Next Fest** = massive visibility opportunity
- Don't mention "mobile" or "Telegram" — Steam users want desktop-first
- Consider adding exclusive content for Steam version (justify the price)

---

## 5. Web Portals (Poki / CrazyGames)

### Platform Context
- **Audience:** Ultra-casual, mainly young (14-25), desktop at school/work
- **Behavior:** Quick browse, play 2-3 games, leave. Algorithm-driven discovery.
- **Monetization:** Revenue share (50/50 Poki, varies CrazyGames)
- **Constraints:** SDK integration, performance requirements, no external links

### Messaging Framework

| Element | Guideline |
|---------|-----------|
| **Tone** | Ultra-simple, zero-friction, fun-first |
| **Key Phrase** | "Play free. Right now. No signup." |
| **CTA Style** | "Play" (literally one word) |
| **Avoid** | Long descriptions, backstory, complex features |
| **Language** | English |

### Copy Templates

#### Game Description (Poki, < 200 words)
```
{Game Name} is a {genre} game where you {core action}.

How to play:
- {Control 1}
- {Control 2}
- {Control 3}

{One sentence about what makes it fun}. 
Can you beat the high score?
```

### Platform-Specific Tips
- Poki: Must integrate Poki SDK for commercials/gameplay events
- CrazyGames: SDK optional but increases revenue share
- Performance is king — must run smooth on low-end Chromebooks
- Initial load < 5MB strongly preferred
- No external links allowed (they keep traffic on-platform)
- Thumbnail image = your only marketing — make it pop

---

## Cross-Platform Messaging Matrix

| Message Theme | Telegram | itch.io | Mobile Store | Steam | Web Portal |
|---------------|----------|---------|-------------|-------|------------|
| **Instant play** | "Play right in chat" | "Play in browser" | "Lightweight & fast" | ❌ Don't mention | "Play free now" |
| **Social** | "Challenge friends!" | "Rate & comment" | "Global leaderboard" | "Achievements" | "Beat high score" |
| **Quality** | "Smooth & polished" | "Handcrafted" | "★★★★★" | "Carefully crafted" | "Fun & addictive" |
| **Price** | "Free to play" | "Free / Pay what you want" | "Free" | "$X.99" | "Free" |
| **Dev story** | Brief, emoji | Full devlog | ❌ Not relevant | Brief, professional | ❌ Not relevant |
| **Portfolio** | "More games ↓" | "More by eastsea" | "More by developer" | "Publisher page" | ❌ Hidden |

---

*Last updated: 2026-02-12 | Part of game-marketing-context skill*
