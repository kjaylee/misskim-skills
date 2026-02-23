# Skill Intake Gate Report

- Path: `/Users/kjaylee/.openclaw/workspace/misskim-skills/skills/game-video-ad-pipeline`
- Risk: **high** (score=24)
- Recommendation: `reject_or_rewrite`

## Matches by category
- doc_url: 20
- network: 9
- proc_exec: 3
- fs_write: 1

## Top findings
- `references/AUDIT.md:20` [doc_url] `- FFmpeg: https://ffmpeg.org/legal.html`
- `references/AUDIT.md:21` [doc_url] `- Remotion: https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md`
- `references/AUDIT.md:22` [doc_url] `- MoviePy: https://raw.githubusercontent.com/Zulko/moviepy/master/LICENCE.txt`
- `references/AUDIT.md:23` [doc_url] `- Shotcut: https://raw.githubusercontent.com/mltframework/shotcut/master/COPYING`
- `references/AUDIT.md:24` [doc_url] `- Kdenlive: https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING`
- `references/AUDIT.md:25` [doc_url] `- MLT: https://raw.githubusercontent.com/mltframework/mlt/master/COPYING`
- `references/RESEARCH.md:19` [doc_url] `- https://ffmpeg.org/legal.html`
- `references/RESEARCH.md:29` [doc_url] `- https://www.remotion.dev/docs/cli`
- `references/RESEARCH.md:30` [doc_url] `- https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md`
- `references/RESEARCH.md:31` [doc_url] `- https://www.remotion.dev/docs/licensing`
- `references/RESEARCH.md:40` [doc_url] `- https://raw.githubusercontent.com/Zulko/moviepy/master/LICENCE.txt`
- `references/RESEARCH.md:45` [doc_url] `- 출처: https://shotcut.org/, https://raw.githubusercontent.com/mltframework/shotcut/master/COPYING`
- `references/RESEARCH.md:48` [doc_url] `- 출처: https://kdenlive.org/features/, https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING`
- `references/RESEARCH.md:51` [doc_url] `- 출처: https://raw.githubusercontent.com/mltframework/mlt/master/COPYING`
- `references/RESEARCH.md:61` [doc_url] `- 출처: https://raw.githubusercontent.com/neur0map/clawvid/main/README.md`
- `references/RESEARCH.md:66` [doc_url] `- 출처: https://raw.githubusercontent.com/zrewolwerowanykaloryfer/deapi-clawdbot-skill/main/README.md`
- `references/RESEARCH.md:72` [doc_url] `- https://raw.githubusercontent.com/unisone/openclaw-skill-suite/main/README.md`
- `references/RESEARCH.md:73` [doc_url] `- https://raw.githubusercontent.com/unisone/openclaw-skill-suite/main/skills/remotion-product-demos/SKILL.md`
- `references/RESEARCH.md:80` [doc_url] `- https://skillhub.com`
- `references/RESEARCH.md:81` [doc_url] `- https://skillhub.ai`
- `scripts/generate-video.py:18` [proc_exec] `import subprocess`
- `scripts/generate-video.py:22` [network] `import urllib.request`
- `scripts/generate-video.py:25` [network] `from urllib.parse import urlparse`
- `scripts/generate-video.py:64` [proc_exec] `proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)`
- `scripts/generate-video.py:82` [proc_exec] `out = subprocess.check_output(`
- `scripts/generate-video.py:107` [network] `req = urllib.request.Request(`
- `scripts/generate-video.py:116` [network] `with urllib.request.urlopen(req, timeout=30) as resp:`
- `scripts/generate-video.py:140` [network] `r'"full":"(https://[^"]+/apps/' + re.escape(app_id) + r'/ss_[^"]+\.(?:jpg|png)[^"]*)"',`
- `scripts/generate-video.py:144` [network] `r'"standard":"(https://[^"]+/apps/' + re.escape(app_id) + r'/ss_[^"]+\.(?:jpg|png)[^"]*)"',`
- `scripts/generate-video.py:169` [network] `req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})`
- `scripts/generate-video.py:170` [network] `with urllib.request.urlopen(req, timeout=30) as resp, out_path.open("wb") as f:`
- `scripts/generate-video.py:542` [network] `page = fetch_url(f"https://store.steampowered.com/app/{game_id}/?l=english")`
- `scripts/generate-video.py:603` [fs_write] `shutil.rmtree(tmp_root, ignore_errors=True)`
