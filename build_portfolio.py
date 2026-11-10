#!/usr/bin/env python3
"""
Generates a light‑mode neofetch‑style portfolio SVG for Sweta Gupta.
The script is named **build_portfolio.py** and creates `profile_card_light.svg`
in the same directory – no dark‑mode version is produced.
"""
import base64
from pathlib import Path
from textwrap import dedent
from io import BytesIO

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops

# ------------------------------------------------------------------
# Configuration (adjust if needed)
# ------------------------------------------------------------------
AVATAR_FILENAME = "avatar.jpg"          # put avatar.jpg or avatar.png alongside this script
OUTPUT_LIGHT = "profile_card_light.svg"

# Light‑mode colour palette
BG_COLOR = "#ffffff"
FG_COLOR = "#24292f"
ACCENT_COLOR = "#0366d6"

# Layout constants
CARD_WIDTH = 800
CARD_HEIGHT = 400
AVATAR_SIZE = 200
PADDING = 30
LINE_HEIGHT = 20
FONT_FAMILY = "monospace"
FONT_SIZE = 14

# ------------------------------------------------------------------
# 1️⃣ Avatar processing – sharpen eyes & improve clarity
# ------------------------------------------------------------------
def process_avatar(in_path: Path) -> Image.Image:
    """Load the avatar, autocrop, boost contrast/brightness, and sharpen.
    Returns a square image of size ``AVATAR_SIZE``.
    """
    img = Image.open(in_path).convert("RGB")

    # Autocrop whitespace / background colour
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Resize to a square while preserving aspect ratio
    img = img.resize((AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)

    # Contrast & brightness adjustments – good defaults for most portraits
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Brightness(img).enhance(1.15)

    # Two‑pass unsharp masking to make the eyes pop
    for _ in range(2):
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    return img


def avatar_to_data_uri(img: Image.Image) -> str:
    """Encode a Pillow image as a base64 data‑URI for embedding in SVG."""
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


# ------------------------------------------------------------------
# 2️⃣ Portfolio text – exactly as you supplied (light‑mode only)
# ------------------------------------------------------------------
STATS_LINES = dedent(
    """
    An IoT Developer, An Open Source Contributor, Cloud Architecture ☁ & A Competitive Programmer
    👷 Software Developer @ GE Healthcare
    👨‍🎓 B.Tech in Electrical Engineering (2018‑2022) from National Institute of Technology Raipur – 8.51 CPI
    🔭 Diploma in Computer Applications from C.V.Raman University (2020) – 83.85%
    🥇 Runner‑Up Robothon_1.0 (Mar 2020) | Runner‑Up Apscript Hackathon (Feb 2021) |
       E‑Ujjwala Hackathon Finalist (Aug 2020) | Codeutsava 5.0 Winner (Feb 2022)

    💼 Currently @ GE Healthcare – open to new Full‑Time opportunities/roles.
    💬 Ask me about Full Stack Dev / DevOps / IoT & Electronics.
    🤔 Looking for help leveling up in Competitive Programming.

    ⚡ Fun fact: I am kinda boring and sometimes dumb though, but I am a determined guy.
    ♟ I play a lot of chess (1400‑1500 on chess.com) and Valorant (Diamond 3).

    ── Experiences ────────────────────────────────────────────────────────
    👷 Software Developer @ GE Healthcare
    🔬 Ex‑Research Student – Wolfram Summer School, 2021 (Education & Innovation Track)
    🕵️ Summer Research Intern – NIT Raipur (May 2020‑Aug 2020)
    👨‍💻 Embedded IoT Intern – SVA Robotics (Sep 2020‑Oct 2020)
    ✍️ Ex‑Core Member – IEEE Bombay Section Technical & Professional Committee (Aug 2020‑May 2022)
    👨‍🏫 Ex‑Head Coordinator – T
