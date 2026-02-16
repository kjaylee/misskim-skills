#!/usr/bin/env python3
"""
Game Video Ad Generator (FFmpeg-first, $0)

Input:  game id (Steam app id, e.g. 570 or steam:570)
Flow:   collect screenshots -> normalize clips -> overlay text -> render mp4
Output: 15~30s promo video (1080x1920 or 1920x1080)

No paid APIs. Uses only public storefront HTML fetch + local FFmpeg.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import urllib.request
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
from urllib.parse import urlparse

FPS = 30
ORIENTATIONS: Dict[str, Tuple[int, int]] = {
    "vertical": (1080, 1920),
    "horizontal": (1920, 1080),
}

TEMPLATES: Dict[str, Dict[str, str]] = {
    "action": {
        "style_filter": "eq=saturation=1.30:contrast=1.13:brightness=0.02,unsharp=5:5:0.85",
        "box_color": "0xE50914@0.32",
        "default_tagline": "High Impact Combat • Live Action Moments",
        "default_cta": "Play Now",
    },
    "puzzle": {
        "style_filter": "eq=saturation=1.08:contrast=1.02:brightness=0.05",
        "box_color": "0x0EA5E9@0.28",
        "default_tagline": "Think Fast • Solve Smart",
        "default_cta": "Challenge Your Brain",
    },
    "idle": {
        "style_filter": "eq=saturation=0.95:contrast=0.97:brightness=0.08",
        "box_color": "0xA855F7@0.26",
        "default_tagline": "Relaxed Progress • Big Rewards",
        "default_cta": "Start Your Idle Journey",
    },
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
ANIMATED_EXTS = {".gif", ".mp4", ".mov", ".mkv", ".webm"}
MEDIA_EXTS = IMAGE_EXTS | ANIMATED_EXTS


def log(msg: str) -> None:
    print(f"[game-video-ad] {msg}")


def run(cmd: Sequence[str]) -> None:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + "\n\nstdout:\n"
            + proc.stdout[-4000:]
            + "\n\nstderr:\n"
            + proc.stderr[-4000:]
        )


def check_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise RuntimeError(f"Required tool not found: {name}")


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def normalize_game_id(game_id: str) -> str:
    if game_id.startswith("steam:"):
        game_id = game_id.split(":", 1)[1]
    if not game_id.isdigit():
        raise ValueError("game-id must be Steam app id digits (e.g. 570 or steam:570)")
    return game_id


def fetch_url(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def _dedupe_keep_order(items: Sequence[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_steam_media(page_html: str, app_id: str, max_assets: int) -> Tuple[str, str, List[str]]:
    page_unescaped = html.unescape(page_html)
    page_normalized = page_unescaped.replace("\\/", "/")

    title_match = re.search(r'<meta property="og:title" content="([^"]+)"', page_html)
    desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', page_html)
    title = title_match.group(1).strip() if title_match else f"Steam {app_id}"
    description = desc_match.group(1).strip() if desc_match else ""

    full_urls = re.findall(
        r'"full":"(https://[^"]+/apps/' + re.escape(app_id) + r'/ss_[^"]+\.(?:jpg|png)[^"]*)"',
        page_normalized,
    )
    standard_urls = re.findall(
        r'"standard":"(https://[^"]+/apps/' + re.escape(app_id) + r'/ss_[^"]+\.(?:jpg|png)[^"]*)"',
        page_normalized,
    )

    urls = full_urls if full_urls else standard_urls
    urls = _dedupe_keep_order(urls)[:max_assets]

    if not urls:
        raise RuntimeError(
            "Could not find screenshot URLs from Steam page. "
            "Try another app id or pass --input-dir with local screenshots."
        )

    return title, description, urls


def download_media(urls: Sequence[str], out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_files: List[Path] = []
    for idx, url in enumerate(urls, start=1):
        parsed = urlparse(url)
        ext = Path(parsed.path).suffix.lower() or ".jpg"
        if ext not in MEDIA_EXTS:
            ext = ".jpg"
        out_path = out_dir / f"asset_{idx:02d}{ext}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, out_path.open("wb") as f:
            f.write(resp.read())
        if out_path.stat().st_size == 0:
            continue
        out_files.append(out_path)
    return out_files


def collect_local_media(input_dir: Path, max_assets: int) -> List[Path]:
    if not input_dir.exists():
        raise RuntimeError(f"input-dir does not exist: {input_dir}")
    media = [
        p
        for p in sorted(input_dir.iterdir())
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS
    ]
    if not media:
        raise RuntimeError(f"No media files in {input_dir}")
    return media[:max_assets]


def ffmpeg_escape_text(value: str) -> str:
    value = value.replace("\\", r"\\")
    value = value.replace("'", r"\'")
    value = value.replace(":", r"\:")
    value = value.replace("%", r"\%")
    value = value.replace(",", r"\,")
    return value


def build_base_filter(width: int, height: int, template: str) -> str:
    style = TEMPLATES[template]["style_filter"]
    return (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},setsar=1,{style}"
    )


def make_clip(
    input_file: Path,
    output_file: Path,
    segment_duration: float,
    width: int,
    height: int,
    fps: int,
    template: str,
) -> None:
    vf = build_base_filter(width, height, template)
    ext = input_file.suffix.lower()

    if ext in IMAGE_EXTS:
        cmd = [
            "ffmpeg",
            "-y",
            "-v",
            "warning",
            "-loop",
            "1",
            "-t",
            f"{segment_duration:.3f}",
            "-i",
            str(input_file),
            "-vf",
            vf,
            "-r",
            str(fps),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            str(output_file),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-v",
            "warning",
            "-stream_loop",
            "-1",
            "-t",
            f"{segment_duration:.3f}",
            "-i",
            str(input_file),
            "-vf",
            vf,
            "-r",
            str(fps),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "22",
            "-pix_fmt",
            "yuv420p",
            str(output_file),
        ]

    run(cmd)


def concat_clips(clips: Sequence[Path], concat_list: Path, merged_out: Path) -> None:
    with concat_list.open("w", encoding="utf-8") as f:
        for clip in clips:
            safe_path = str(clip.resolve()).replace("'", "'\\''")
            f.write(f"file '{safe_path}'\n")

    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "warning",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "21",
            "-pix_fmt",
            "yuv420p",
            str(merged_out),
        ]
    )


def parse_box_rgba(color_spec: str) -> Tuple[int, int, int, int]:
    hex_part, _, alpha_part = color_spec.partition("@")
    hex_clean = hex_part.lower().replace("0x", "")
    if len(hex_clean) != 6:
        return (0, 0, 0, 96)
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    alpha = float(alpha_part) if alpha_part else 0.3
    a = max(0, min(255, int(alpha * 255)))
    return (r, g, b, a)


def find_font_path() -> Path | None:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return p
    return None


def create_text_overlay_png(
    out_png: Path,
    width: int,
    height: int,
    text: str,
    y: int,
    fontsize: int,
    box_rgba: Tuple[int, int, int, int],
    max_chars_per_line: int,
) -> None:
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    wrapped = "\n".join(textwrap.wrap(text.strip(), width=max_chars_per_line))
    font_path = find_font_path()
    if font_path is not None:
        font = ImageFont.truetype(str(font_path), fontsize)
    else:
        font = ImageFont.load_default()

    spacing = max(6, fontsize // 5)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=spacing, align="center")
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = int((width - text_w) / 2)
    y = max(0, min(height - text_h - 1, y))

    pad_x = max(14, fontsize // 2)
    pad_y = max(10, fontsize // 3)
    rect = (x - pad_x, y - pad_y, x + text_w + pad_x, y + text_h + pad_y)
    draw.rounded_rectangle(rect, radius=max(12, fontsize // 3), fill=box_rgba)

    draw.multiline_text((x, y), wrapped, font=font, fill=(255, 255, 255, 255), spacing=spacing, align="center")
    image.save(out_png)


def overlay_text_and_finalize(
    merged_input: Path,
    output_file: Path,
    title: str,
    tagline: str,
    cta: str,
    duration: float,
    width: int,
    height: int,
    fps: int,
    template: str,
    temp_dir: Path,
) -> None:
    box_rgba = parse_box_rgba(TEMPLATES[template]["box_color"])

    title_png = temp_dir / "overlay_title.png"
    tagline_png = temp_dir / "overlay_tagline.png"
    cta_png = temp_dir / "overlay_cta.png"

    if width < height:
        title_chars, tagline_chars, cta_chars = 20, 34, 24
    else:
        title_chars, tagline_chars, cta_chars = 28, 48, 30

    create_text_overlay_png(
        out_png=title_png,
        width=width,
        height=height,
        text=title,
        y=int(height * 0.08),
        fontsize=int(height * 0.045),
        box_rgba=box_rgba,
        max_chars_per_line=title_chars,
    )
    create_text_overlay_png(
        out_png=tagline_png,
        width=width,
        height=height,
        text=tagline,
        y=int(height * 0.76),
        fontsize=int(height * 0.034),
        box_rgba=box_rgba,
        max_chars_per_line=tagline_chars,
    )
    create_text_overlay_png(
        out_png=cta_png,
        width=width,
        height=height,
        text=cta,
        y=int(height * 0.87),
        fontsize=int(height * 0.04),
        box_rgba=box_rgba,
        max_chars_per_line=cta_chars,
    )

    title_end = max(6.0, duration * 0.6)
    tagline_start = min(2.0, duration * 0.15)
    tagline_end = max(duration - 3.5, duration * 0.75)
    cta_start = max(duration - 4.0, duration * 0.75)

    filter_complex = (
        f"[0:v][1:v]overlay=0:0:enable='between(t\\,0\\,{title_end:.2f})'[v1];"
        f"[v1][2:v]overlay=0:0:enable='between(t\\,{tagline_start:.2f}\\,{tagline_end:.2f})'[v2];"
        f"[v2][3:v]overlay=0:0:enable='between(t\\,{cta_start:.2f}\\,{duration:.2f})',"
        "format=yuv420p[vout]"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "warning",
            "-i",
            str(merged_input),
            "-loop",
            "1",
            "-i",
            str(title_png),
            "-loop",
            "1",
            "-i",
            str(tagline_png),
            "-loop",
            "1",
            "-i",
            str(cta_png),
            "-filter_complex",
            filter_complex,
            "-map",
            "[vout]",
            "-t",
            f"{duration:.3f}",
            "-r",
            str(fps),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_file),
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate short game promo video using FFmpeg and screenshots."
    )
    parser.add_argument("--game-id", required=True, help="Steam app id, e.g. 570 or steam:570")
    parser.add_argument("--template", choices=sorted(TEMPLATES.keys()), default="action")
    parser.add_argument("--orientation", choices=sorted(ORIENTATIONS.keys()), default="vertical")
    parser.add_argument("--duration", type=float, default=20.0, help="Target seconds (15~30)")
    parser.add_argument("--max-shots", type=int, default=6, help="How many screenshots to use")
    parser.add_argument("--title", help="Override title text")
    parser.add_argument("--tagline", help="Override middle tagline")
    parser.add_argument("--cta", help="Override final CTA text")
    parser.add_argument("--input-dir", type=Path, help="Use local media folder instead of Steam fetch")
    parser.add_argument("--output", type=Path, help="Output mp4 path")
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary render directory for debugging",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.duration < 15 or args.duration > 30:
        raise ValueError("duration must be between 15 and 30 seconds")

    if args.max_shots < 3:
        raise ValueError("max-shots must be >= 3")

    check_tool("ffmpeg")
    check_tool("ffprobe")

    width, height = ORIENTATIONS[args.orientation]
    game_id = normalize_game_id(args.game_id)

    default_output = (
        Path("output")
        / f"game-{game_id}-{args.template}-{args.orientation}-{int(args.duration)}s.mp4"
    )
    output_path = (args.output or default_output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_root = Path(tempfile.mkdtemp(prefix="game-video-ad-"))
    log(f"temporary workspace: {tmp_root}")

    try:
        # 1) Collect assets
        if args.input_dir:
            title = args.title or f"Game {game_id}"
            description = ""
            media_files = collect_local_media(args.input_dir, args.max_shots)
            log(f"Using local media files: {len(media_files)}")
        else:
            page = fetch_url(f"https://store.steampowered.com/app/{game_id}/?l=english")
            title, description, media_urls = extract_steam_media(page, game_id, args.max_shots)
            download_dir = tmp_root / "downloaded"
            media_files = download_media(media_urls, download_dir)
            if len(media_files) < 3:
                raise RuntimeError(f"Not enough media downloaded ({len(media_files)}). Need at least 3.")
            log(f"Fetched screenshots from Steam: {len(media_files)}")

        title = args.title or title.replace(" on Steam", "").strip()
        fallback_tagline = description.split(".")[0].strip()
        if len(fallback_tagline) > 72:
            fallback_tagline = textwrap.shorten(fallback_tagline, width=72, placeholder="…")
        tagline = args.tagline or fallback_tagline or TEMPLATES[args.template]["default_tagline"]
        cta = args.cta or TEMPLATES[args.template]["default_cta"]

        # 2) Build normalized clips
        segment = args.duration / len(media_files)
        clips_dir = tmp_root / "clips"
        clips_dir.mkdir(parents=True, exist_ok=True)
        clip_paths: List[Path] = []

        for idx, media in enumerate(media_files, start=1):
            clip = clips_dir / f"clip_{idx:02d}.mp4"
            make_clip(media, clip, segment, width, height, FPS, args.template)
            clip_paths.append(clip)

        # 3) Concat clips
        merged_path = tmp_root / "merged.mp4"
        concat_list = tmp_root / "concat.txt"
        concat_clips(clip_paths, concat_list, merged_path)

        # 4) Overlay text and finalize
        overlay_text_and_finalize(
            merged_input=merged_path,
            output_file=output_path,
            title=title,
            tagline=tagline,
            cta=cta,
            duration=args.duration,
            width=width,
            height=height,
            fps=FPS,
            template=args.template,
            temp_dir=tmp_root,
        )

        # 5) Validate output
        out_duration = ffprobe_duration(output_path)
        if out_duration < 14.5:
            raise RuntimeError(f"Output duration too short: {out_duration:.2f}s")

        log("render complete")
        log(f"output: {output_path}")
        log(f"duration: {out_duration:.2f}s")
        log(f"resolution: {width}x{height}")
        return 0

    finally:
        if args.keep_temp:
            log(f"kept temp folder: {tmp_root}")
        else:
            shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[game-video-ad] ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
