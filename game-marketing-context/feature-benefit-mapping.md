# 🗺️ Feature-Benefit Mapping Templates

Convert game features into player-facing benefits and marketing copy.
Referenced by: `game-marketing-context/SKILL.md`

---

## The Golden Rule

> **Players don't care about features. They care about what features DO for them.**

```
Feature: "HTML5/WASM technology"
Benefit: "Plays instantly on any device"
Message: "Tap once. You're playing. No download, no wait."
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
         This is what goes in marketing copy.
```

---

## Framework: Feature → Benefit → Message

### Step 1: List the Feature
What it IS (technical/objective)

### Step 2: Convert to Benefit  
What it DOES for the player (emotional/practical)

### Step 3: Write the Message
How you SAY it (copy that resonates)

### Step 4: Add Proof
WHY they should believe you (evidence)

---

## Portfolio-Level Feature-Benefit Map

| Feature | Benefit | Message | Proof |
|---------|---------|---------|-------|
| HTML5/WASM engine | Works everywhere | "Play on phone, tablet, or desktop — no app needed" | Links work on any browser |
| Telegram Mini App | Play without leaving chat | "Tap a link, you're playing. Don't even switch apps." | Telegram deep link demo |
| < 5MB initial load | Instant start even on slow networks | "Loads faster than opening Instagram" | Measurable load time |
| 30+ game library | Always something new | "Bored of this one? 29 more games waiting" | Portfolio page |
| Godot + Rust | Smooth 60fps performance | "Buttery smooth, even on older phones" | Frame rate metrics |
| Solo developer | Personal touch, fast updates | "Tell me what to fix — I'll ship it this week" | Update history |
| No account required | Zero friction entry | "No signup. No login. No email. Just play." | Onboarding flow |
| Optional rewarded ads | Respectful monetization | "Watch ads to earn rewards. Or don't. Your choice." | Ad implementation |
| Leaderboards | Social competition | "See your name at the top. Beat your friends." | Leaderboard screenshot |
| Daily check-in | Rewarding habit | "Come back daily — your streak means bigger rewards" | Streak counter UI |
| Cross-game rewards | Portfolio engagement | "Your progress in one game unlocks stuff in another" | Cross-promo system |
| Referral system | Earn by sharing | "Invite a friend, you both get rewarded" | Referral link flow |
| Localization (EN/KO/RU) | Plays in your language | "게임을 한국어로 즐기세요" | Language toggle |

---

## Game-Level Feature-Benefit Template

Use this for EACH game's marketing context file:

```markdown
## Feature-Benefit Map: {Game Name}

### Core Mechanic Features
| Feature | Benefit | Copy for Telegram | Copy for itch.io | Copy for Store |
|---------|---------|-------------------|-------------------|----------------|
| {mechanic 1} | {benefit} | "{telegram copy}" | "{itch copy}" | "{store copy}" |
| {mechanic 2} | {benefit} | "{telegram copy}" | "{itch copy}" | "{store copy}" |
| {mechanic 3} | {benefit} | "{telegram copy}" | "{itch copy}" | "{store copy}" |

### Social Features
| Feature | Benefit | Copy |
|---------|---------|------|
| {social 1} | {benefit} | "{copy}" |

### Progression Features
| Feature | Benefit | Copy |
|---------|---------|------|
| {progression 1} | {benefit} | "{copy}" |

### Quality-of-Life Features
| Feature | Benefit | Copy |
|---------|---------|------|
| {qol 1} | {benefit} | "{copy}" |
```

---

## Benefit Categories (Cheat Sheet)

When converting features to benefits, categorize the benefit type:

### 🎯 Functional Benefits (What it DOES)
- Saves time
- Works everywhere
- Easy to learn
- Runs smoothly
- Loads fast

**Copy style:** Direct, clear, factual
> "Loads in under 3 seconds, even on slow connections."

### 💚 Emotional Benefits (How it FEELS)
- Satisfying
- Exciting
- Relaxing
- Empowering
- Fun

**Copy style:** Evocative, experiential
> "That feeling when you clear the entire board in one combo? Yeah."

### 🏆 Social Benefits (How others SEE you)
- Impressive scores to share
- Cool games to recommend
- Bragging rights
- "I found it first" status

**Copy style:** Social proof, challenge
> "Show your friends who's really the best."

### 🧠 Identity Benefits (Who you BECOME)
- Smart player
- Indie supporter
- Early adopter
- Skilled gamer

**Copy style:** Aspirational, community
> "Join the players who prefer quality over quantity."

---

## Message Hierarchy

When writing ANY marketing copy, prioritize messages in this order:

### Level 1: Hook (first impression, < 2 seconds)
- The ONE thing that makes someone stop scrolling
- Usually the unique hook or instant benefit
- **Examples:**
  - "Play in 1 tap. No download."
  - "A puzzle game that fits in your Telegram chat."

### Level 2: Core Value Prop (next 5 seconds)
- What the game IS and why it's worth time
- Usually feature-benefit combo
- **Examples:**
  - "Match colorful tiles in quick 2-minute rounds. Challenge friends on the leaderboard."

### Level 3: Proof Points (if they're still reading)
- Evidence the game delivers on promises
- Usually numbers, quotes, or credentials
- **Examples:**
  - "50,000+ plays this month"
  - "★★★★★ on itch.io"
  - "From the developer of {popular game}"

### Level 4: CTA (what to do next)
- Clear, single action
- **Examples:**
  - "▶️ Play Now" (Telegram)
  - "Play in browser" (itch.io)
  - "Add to Wishlist" (Steam)

---

## Copy Formulas (Fill-in-the-Blank)

### Formula 1: Problem-Agitate-Solve
```
Tired of [problem]?
[Game Name] is a [genre] game that [solves problem].
[CTA]

Example:
Tired of games that take forever to load?
TilePop is a puzzle game that plays instantly in Telegram.
▶️ Tap to play now
```

### Formula 2: Benefit-Feature-Proof
```
[Benefit statement].
[Feature that enables it].
[Proof it's real].

Example:
Play anywhere, anytime — no download needed.
Built with web technology that runs in any browser.
Already played by 10,000+ people this week.
```

### Formula 3: Challenge/Dare
```
[Challenge statement].
[What they need to do].
[Social proof / stakes].

Example:
Think you can score over 500?
Play {Game Name} and prove it.
Only 3% of players have done it. 🏆
```

### Formula 4: Social Proof
```
[Number] players already [action].
[What they're experiencing].
[CTA to join].

Example:
10,000 players already hooked on TilePop.
Quick matches, daily rewards, and fierce leaderboard competition.
Join them → [link]
```

### Formula 5: Curiosity Gap
```
[Intriguing question or statement].
[Partial reveal].
[CTA to discover the answer].

Example:
The puzzle game Telegram doesn't want you to find.
(Because you'll never stop playing.)
👉 [link]
```

---

## Per-Persona Message Adaptation

Same feature, different messaging per persona:

### Example: "Leaderboard" Feature

| Persona | Message |
|---------|---------|
| 🚇 Commuter Casual | "See if your score beats other commuters 🚇" |
| 🏠 Bedroom Indie Fan | "Compete with the indie gaming community" |
| 📱 Mobile Snacker | "Check the global rankings — where do you stand?" |
| 🤖 Telegram Native | "Post your rank in the group chat and flex 💪" |
| 🎮 Web Game Browser | "Beat the high score. We dare you." |

---

## A/B Testing Priorities

When testing messaging, prioritize in this order:

1. **Hook / headline** (biggest impact)
2. **CTA text** (directly affects conversion)
3. **Screenshot captions** (store listing impact)
4. **Description first paragraph** (retention of store visitors)
5. **Feature ordering** (which feature leads)

### What to Test

| Element | Variant A | Variant B |
|---------|-----------|-----------|
| Hook approach | Benefit-led | Curiosity-led |
| Tone | Casual/fun | Direct/confident |
| CTA | "Play Now" | "Challenge Friends" |
| Social proof | Number-based | Quote-based |
| Feature lead | Instant play | Social competition |

---

*Last updated: 2026-02-12 | Part of game-marketing-context skill*
