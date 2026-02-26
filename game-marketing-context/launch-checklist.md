# 🚀 Launch Checklist with Marketing Touchpoints

Step-by-step launch process with every marketing touchpoint mapped.
Referenced by: `game-marketing-context/SKILL.md`

> **Note:** This complements `game-marketing/SKILL.md` Phase 0-4 playbook. 
> This checklist focuses specifically on marketing touchpoints and messaging alignment.

---

## Pre-Launch: D-14 to D-7

### Context & Strategy

```checklist
- [ ] Generate per-game marketing context file
      → Run game-marketing-context skill → `.openclaw/game-context/{game-slug}.md`
- [ ] Define primary & secondary persona for this game
      → Reference personas.md, select and customize
- [ ] Write positioning statement
      → Use competitive-positioning.md Formula
- [ ] Complete feature-benefit map
      → Use feature-benefit-mapping.md template
- [ ] Identify top 3 competitors + our advantage for each
- [ ] Define JTBD Four Forces for this specific game
- [ ] Set launch goals (DAU, retention, viral K targets)
```

### Assets

```checklist
- [ ] App icon — 512x512, works light/dark, stands out at small size
- [ ] Screenshots — 4+ per platform, with captions (benefit-focused)
- [ ] Gameplay GIF — < 5MB, shows the "aha moment" in < 3 seconds
- [ ] Trailer video — 30-60s, hook in first 2s, show gameplay not logos
- [ ] Social media banner — 1200x630 (OG image for link previews)
- [ ] Promo art — 1920x1080 (blog, Steam capsule if applicable)
- [ ] Store-ready descriptions written per platform-messaging.md
```

### Technical

```checklist
- [ ] Referral system live & tested (deep links work)
- [ ] Leaderboard live & tested
- [ ] Daily check-in system active
- [ ] Cross-promo links to other portfolio games embedded
- [ ] Analytics tracking: play count, DAU, session length, referral source
- [ ] Loading time < 3s on average connection
- [ ] Tested on: Android Chrome, iOS Safari, Desktop Chrome, Telegram webview
```

---

## Teaser Campaign: D-7 to D-1

### D-7: Seed Awareness

```checklist
- [ ] TELEGRAM: Teaser post in portfolio channel
      Message: "Something new is coming... 👀 Stay tuned."
      (No link yet — build curiosity)
- [ ] BLOG: Write launch blog post draft (don't publish yet)
      SEO target: "{game genre} telegram game" + related keywords
- [ ] CROSS-PROMO: Add "Coming Soon" banner in 2-3 existing games
```

### D-5: First Reveal

```checklist
- [ ] TELEGRAM: Reveal game name + 1 GIF
      Message: "🎮 Introducing {Game Name} — {tagline}. Launching {date}!"
- [ ] TWITTER/X: First reveal tweet with GIF
      Include: #indiegame #gamedev #{genre}
- [ ] REDDIT: Teaser post in r/IndieDev or r/gamedev (dev story angle)
```

### D-3: Build Anticipation

```checklist
- [ ] TELEGRAM: Gameplay preview post (longer GIF or short video)
      Include: "🔔 Turn on notifications to be first to play!"
- [ ] TIKTOK: First gameplay clip (hook: "이 게임 곧 나옴" / "New game dropping soon")
- [ ] Ask 3-5 friends/community members to be Day 1 players
```

### D-1: Final Prep

```checklist
- [ ] All store listings LIVE but not promoted yet
      - [ ] Telegram Bot configured, Mini App URL set
      - [ ] itch.io page published (can be "in development")
      - [ ] FindMini.app submission sent (allow processing time)
- [ ] Pre-schedule D-Day posts (or have drafts ready)
- [ ] Cross-promo "TOMORROW" teasers in existing games
- [ ] Verify all deep links, referral tracking, leaderboard
```

---

## Launch Day: D-0

### Morning (KST)

```checklist
- [ ] Final smoke test — play through as a new player
- [ ] Activate cross-promo in ALL existing games
      "🆕 New Game! {Name} — Play Now → {link}"
```

### Launch Hour

```checklist
- [ ] TELEGRAM (Portfolio Channel):
      Full launch post (use channel launch post template from platform-messaging.md)
      Include: deep link, features, GIF, referral call
      
- [ ] TELEGRAM (Groups):
      Share in 2-3 relevant groups (add value, don't spam)
      "Hey! Just launched {Game Name} — a {genre} game you can play right here in Telegram.
       Would love your feedback! {link}"
      
- [ ] BLOG: Publish launch blog post
      Promote on Telegram + Twitter
      
- [ ] TWITTER/X: Launch tweet (GIF + link)
      "🎮 {Game Name} is LIVE!
       {Tagline}
       ▶️ Play now: {link}
       #indiegame #gamedev #{genre}"
      
- [ ] REDDIT: Launch post in r/WebGames (if browser-playable) + r/IndieGaming
      Use Reddit post formula from game-marketing/SKILL.md
```

### Evening

```checklist
- [ ] TIKTOK: Launch gameplay video (use content formula from game-marketing/SKILL.md)
- [ ] Reply to ALL early comments/feedback (engagement = algorithm boost)
- [ ] Monitor for crashes/bugs — fix immediately if found
- [ ] Celebrate (you shipped a game!)
```

---

## Post-Launch: D+1 to D+7

### D+1: Engage & Iterate

```checklist
- [ ] Read ALL player feedback (Telegram, itch.io, Reddit)
- [ ] Categorize feedback: Bug / UX Issue / Feature Request / Positive / Negative
- [ ] Update player language bank in context file (verbatim quotes!)
- [ ] Fix any critical bugs
- [ ] TELEGRAM: "Thank you for playing!" post with first stats
      "🎉 {X} players in the first 24 hours! Thank you!
       Keep the feedback coming 💚"
```

### D+3: Performance Review

```checklist
- [ ] Pull analytics: DAU, D1 retention, session length, referral conversion
- [ ] Compare to goals set in pre-launch
- [ ] Decision matrix:
      │ D1 Retention │ Action                                    │
      │─────────────│──────────────────────────────────────────│
      │ > 30%       │ 🟢 Scale marketing spend                  │
      │ 20-30%      │ 🟡 Minor UX tweaks, continue marketing    │
      │ 10-20%      │ 🟠 Significant UX overhaul needed         │
      │ < 10%       │ 🔴 Core loop problem — rethink or shelve  │
- [ ] Ship first update with quick wins from player feedback
- [ ] TELEGRAM: "Update! We heard you" post listing changes
```

### D+7: First Weekly Assessment

```checklist
- [ ] Full weekly analytics report:
      - Total unique players
      - DAU trend (growing/flat/declining)
      - D1 and D7 retention
      - Viral coefficient K
      - Revenue (if monetized)
      - Top referral sources
      - Top player language quotes
- [ ] Update per-game marketing context file with real data
- [ ] TELEGRAM: Weekly leaderboard post (automate going forward)
- [ ] TIKTOK: Second gameplay video (different angle/hook)
- [ ] BLOG: Devlog #1 (if targeting itch.io audience)
```

---

## Growth Phase: D+8 to D+30

### Weekly Rhythm

```
Monday:     Review last week's analytics, plan this week's content
Tuesday:    TikTok/Shorts video
Wednesday:  Blog post or devlog
Thursday:   TikTok/Shorts video  
Friday:     Telegram channel update (stats, upcoming features)
Saturday:   TikTok/Shorts video
Sunday:     Weekly leaderboard post (automated)
```

### D+14 Checkpoint

```checklist
- [ ] D7 retention analysis — core loop validated?
- [ ] Viral K assessment — organic growth working?
- [ ] Content routine established? (3+ posts/week)
- [ ] Player language bank has 10+ verbatim quotes?
- [ ] Referral system showing conversions?
- [ ] Cross-promo driving traffic between games?
- [ ] Update competitive positioning if landscape changed
```

### D+30 Growth Decision

```checklist
- [ ] Full month analytics:
      - DAU trajectory (growth curve shape)
      - D30 retention
      - Revenue vs target
      - Best performing channel
      - Best performing content type
      
- [ ] Decision framework:
      │ Signal              │ Decision                              │
      │────────────────────│──────────────────────────────────────│
      │ DAU growing + K>0.5│ 🟢 SCALE: Invest in paid acquisition  │
      │ DAU stable + K>0.3 │ 🟡 GROW: More content, optimize viral │
      │ DAU flat + K<0.3   │ 🟠 PIVOT: Major update or new feature │
      │ DAU declining       │ 🔴 ASSESS: Maintenance mode or sunset │
      
- [ ] If SCALE: Start paid campaigns (see game-marketing/SKILL.md Phase 3)
- [ ] If GROW: Double content output + A/B test messaging
- [ ] If PIVOT: Player survey → identify biggest gap → ship fix
- [ ] If ASSESS: Reduce investment, focus on next game
```

---

## Platform Expansion Touchpoints

When expanding to new platforms, use this checklist:

### itch.io Launch (usually D+7 to D+14)

```checklist
- [ ] Game page created with itch.io-specific copy (see platform-messaging.md)
- [ ] Browser embed tested and working
- [ ] 3-5 screenshots uploaded
- [ ] Tags selected (genre + "browser" + "html5" + "free")
- [ ] Devlog #1 posted
- [ ] Shared in r/WebGames and r/IndieGaming
- [ ] "Pay what you want" or free with tip jar enabled
```

### Mobile Store Launch (D+30 to D+60)

```checklist
- [ ] Store listing created with mobile-specific copy (see platform-messaging.md)
- [ ] ASO keywords researched and applied
- [ ] Screenshots with device frames and captions
- [ ] Localized for top 3 target markets
- [ ] Rating prompt implemented (after positive gameplay moment)
- [ ] First 10 reviews seeded (ask friends/community)
```

### Web Portal Launch (D+30 to D+60)

```checklist
- [ ] Poki SDK / CrazyGames SDK integrated
- [ ] Initial load size < 5MB
- [ ] Performance optimized for low-end devices
- [ ] Thumbnail image that pops in portal browse view
- [ ] Description written per portal guidelines
- [ ] Submitted for review
```

### Steam Launch (D+60 to D+90, if applicable)

```checklist
- [ ] Steam page live with coming soon / wishlist
- [ ] Capsule art created (header, small, hero)
- [ ] Steam-specific features added? (achievements, Steam Cloud)
- [ ] Exclusive content for Steam version (justify price)
- [ ] Wishlist campaign running (minimum 2 weeks before launch)
- [ ] Steam Next Fest applied for (if timing works)
- [ ] 10 reviews target plan (who will review on Day 1?)
```

---

## Marketing Context Maintenance Touchpoints

```checklist
- [ ] D+0:  Context file created (auto-draft from codebase)
- [ ] D+3:  Update with real player language (first feedback)
- [ ] D+7:  Update proof points with first week data
- [ ] D+30: Full context refresh with month-1 data
- [ ] D+90: Quarterly context review
- [ ] Each major update: Refresh features, benefits, messaging
- [ ] Each new platform: Add platform-specific section
```

---

## Quick Reference: Marketing Touchpoint Map

```
         D-14     D-7      D-3     D-0     D+1     D+7     D+14    D+30
          │        │        │       │       │       │        │       │
CONTEXT:  ●────────────────────────────────●───────────────●────────●
          create                           update          update   refresh
          
TELEGRAM: ─────────●────────●───────●───────●───────●──────●──weekly──
                  tease    reveal  launch  thanks  recap  routine

TIKTOK:   ───────────────────●───────●───────●──────●──────●──3x/week
                            tease   launch  +2d    +5d    routine

REDDIT:   ─────────●────────────────●───────────────────────●──────
                  devtease         launch                  devlog

BLOG:     ──────────────────────────●───────────────●──────●──weekly
                                  launch           devlog  routine

ITCH.IO:  ──────────────────────────●───────────────●──────
                                  submit           devlog

STORES:   ─────────────────────────────────────────────────●──────
                                                          submit
```

---

*Last updated: 2026-02-12 | Part of game-marketing-context skill*
