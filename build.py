#!/usr/bin/env python3
"""Crimson Fade: Kettu/Revenge (Vendetta spec 2) theme + background PNG.
Edit PALETTE and re-run; writes out/crimson-fade.json and out/crimson-fade-bg.png."""
import json, os, sys
import numpy as np
from PIL import Image

BASE = "https://sayer.pages.dev/themes"
BG_VERSION = 2  # bump when the PNG changes: Android caches images by address
OUT = os.path.dirname(os.path.abspath(__file__))

PALETTE = {
    # Pyrenad's hexes: #0f0000 #290303 #870303 #a10505
    # background image stops (top, middle, bottom)
    "grad_top": "#050000", "grad_mid": "#290303", "grad_bot": "#870303",
    # surfaces, darkest to lightest
    "bg0": "#090000", "bg1": "#0f0000", "bg2": "#1a0202", "bg3": "#290303",
    "mod": "#3a0505", "line": "#560909",
    # accent: her reds for fills, a lifted red for text on dark
    "accent": "#a10505", "accent_hi": "#ff4545", "accent_lo": "#870303",
    "link": "#ff5c5c",
    # text
    "text": "#f5eaea", "head": "#fff7f7", "sub": "#e6d3d3", "muted": "#c8a9a9",
    # status
    "green": "#3ecf6e", "yellow": "#f0b232", "danger": "#ff4f4f",
}


def a(hex_, alpha):
    return hex_ + format(round(alpha * 255), "02x")


def theme(p):
    sem = {
        # text
        "TEXT_NORMAL": p["text"], "TEXT_PRIMARY": p["text"], "TEXT_DEFAULT": p["text"],
        "TEXT_STRONG": p["head"], "TEXT_SECONDARY": p["sub"], "TEXT_MUTED": p["muted"],
        "HEADER_PRIMARY": p["head"], "HEADER_SECONDARY": p["sub"],
        "MOBILE_TEXT_HEADING_PRIMARY": p["head"],
        "TEXT_LINK": p["link"], "TEXT_BRAND": p["accent_hi"],
        "CHANNELS_DEFAULT": p["sub"], "CHANNEL_ICON": p["muted"],
        "REDESIGN_CHANNEL_NAME_TEXT": p["text"], "REDESIGN_CHANNEL_CATEGORY_NAME_TEXT": p["sub"],
        "INTERACTIVE_NORMAL": p["sub"], "INTERACTIVE_HOVER": p["head"],
        "INTERACTIVE_ACTIVE": p["head"], "INTERACTIVE_MUTED": p["muted"],
        # base surfaces (solid: nothing sits behind sidebars)
        "BACKGROUND_PRIMARY": p["bg1"], "BACKGROUND_SECONDARY": p["bg0"],
        "BACKGROUND_SECONDARY_ALT": p["bg2"], "BACKGROUND_TERTIARY": p["bg0"],
        "BACKGROUND_MOBILE_PRIMARY": p["bg1"], "BACKGROUND_MOBILE_SECONDARY": p["bg0"],
        "BACKGROUND_FLOATING": p["bg2"], "BACKGROUND_NESTED_FLOATING": p["bg2"],
        "BG_BASE_PRIMARY": p["bg1"], "BG_BASE_SECONDARY": p["bg0"], "BG_BASE_TERTIARY": p["bg0"],
        "BG_SURFACE_OVERLAY": p["bg2"], "BG_SURFACE_RAISED": p["bg2"],
        "BG_BACKDROP": a("#000000", 0.75),
        "CHAT_BACKGROUND": p["bg1"],
        "CARD_PRIMARY_BG": a(p["bg3"], 0.82), "CARD_SECONDARY_BG": a(p["bg2"], 0.82),
        "CARD_PRIMARY_PRESSED_BG": p["mod"],
        # surfaces that sit on the chat gradient: see-through
        "EMBED_BACKGROUND": a(p["bg3"], 0.78),
        "INPUT_BACKGROUND": a(p["bg2"], 0.85),
        "REDESIGN_CHAT_INPUT_BACKGROUND": a(p["bg2"], 0.85),
        "BACKGROUND_MESSAGE_HOVER": a("#ffffff", 0.04),
        "BACKGROUND_MENTIONED": a(p["accent"], 0.16),
        "BACKGROUND_MENTIONED_HOVER": a(p["accent"], 0.24),
        "SPOILER_HIDDEN_BACKGROUND": p["mod"], "SPOILER_REVEALED_BACKGROUND": a(p["mod"], 0.6),
        # modifiers
        "BACKGROUND_ACCENT": p["accent"],
        "BACKGROUND_MODIFIER_HOVER": a(p["mod"], 0.7), "BACKGROUND_MODIFIER_ACTIVE": p["mod"],
        "BACKGROUND_MODIFIER_SELECTED": p["mod"], "BACKGROUND_MODIFIER_ACCENT": p["line"],
        "BG_MOD_FAINT": a(p["mod"], 0.5), "BG_MOD_SUBTLE": a(p["mod"], 0.7), "BG_MOD_STRONG": p["mod"],
        "ANDROID_RIPPLE": a(p["accent"], 0.25),
        "THREAD_CHANNEL_SPINE": p["line"], "SCROLLBAR_AUTO_THUMB": p["line"],
        # buttons
        "REDESIGN_BUTTON_PRIMARY_BACKGROUND": p["accent"],
        "REDESIGN_BUTTON_PRIMARY_PRESSED_BACKGROUND": p["accent_lo"],
        "REDESIGN_BUTTON_PRIMARY_TEXT": "#ffffff",
        "REDESIGN_BUTTON_SECONDARY_BACKGROUND": p["bg3"],
        "REDESIGN_BUTTON_SECONDARY_BORDER": p["line"],
        "REDESIGN_BUTTON_TERTIARY_BACKGROUND": p["bg2"],
        "REDESIGN_INPUT_CONTROL_SELECTED": p["accent"],
        "REDESIGN_ACTIVITY_CARD_BACKGROUND": p["bg3"],
    }
    raw = {
        "BRAND_260": p["accent_hi"], "BRAND_300": p["accent_hi"], "BRAND_360": p["accent_hi"],
        "BRAND_400": p["accent"], "BRAND_500": p["accent"], "BRAND_530": p["accent"],
        "BRAND_560": p["accent_lo"], "BRAND_600": p["accent_lo"],
        "BRAND_630": p["mod"], "BRAND_730": p["bg2"],
        "PRIMARY_100": p["head"], "PRIMARY_130": p["head"], "PRIMARY_160": p["text"],
        "PRIMARY_200": p["text"], "PRIMARY_230": p["sub"], "PRIMARY_300": p["sub"],
        "PRIMARY_330": p["muted"], "PRIMARY_345": p["muted"], "PRIMARY_360": p["muted"],
        "PRIMARY_400": p["muted"], "PRIMARY_460": p["line"], "PRIMARY_500": p["line"],
        "PRIMARY_530": p["mod"], "PRIMARY_560": p["mod"], "PRIMARY_600": p["bg3"],
        "PRIMARY_630": p["bg2"], "PRIMARY_645": p["bg2"], "PRIMARY_660": p["bg1"],
        "PRIMARY_700": p["bg0"], "PRIMARY_730": p["bg0"], "PRIMARY_760": p["bg0"],
        "PRIMARY_800": p["bg0"], "PRIMARY_830": "#030001", "PRIMARY_860": "#030001",
        "PRIMARY_900": "#000000",
        "PLUM_3": p["text"], "PLUM_4": p["accent"], "PLUM_6": p["text"], "PLUM_9": p["sub"],
        "PLUM_10": p["muted"], "PLUM_11": p["sub"], "PLUM_13": p["muted"], "PLUM_14": p["line"],
        "PLUM_15": p["line"], "PLUM_16": p["mod"], "PLUM_17": p["bg0"], "PLUM_18": p["bg3"],
        "PLUM_19": p["bg3"], "PLUM_20": p["bg1"], "PLUM_21": p["bg1"], "PLUM_22": p["bg0"],
        "PLUM_23": p["bg0"], "PLUM_24": p["bg2"],
        "BLUE_345": p["link"], "BLUE_360": p["link"], "BLUE_400": p["link"],
        "WHITE": "#ffffff", "WHITE_500": "#ffffff", "BLACK": "#000000",
        "CHAT_MENTIONS_BACKGROUND_DARK": a(p["accent"], 0.30),
        "CHAT_MENTIONS_FOREGROUND_DARK": "#ffd9db",
    }
    return {
        "name": "Crimson Fade",
        "description": "Near-black fading into blood red, made for Pyrenad.",
        "authors": [{"name": "pressure"}],
        "spec": 2,
        "semanticColors": {k: [v] for k, v in sem.items()},
        "rawColors": raw,
        "plus": {
            "version": "0", "customOverlays": True, "mentionLineColor": p["accent_hi"],
            "icons": {
                "ic_radio_circle_checked": p["accent"], "ic_radio_circle_checked__overlay": p["head"],
                "ic_radio_square_24px": p["accent"], "ic_radio_square_checked_24px": p["accent"],
                "ic_radio_square_checked_24px__overlay": p["head"],
                "ic_selection_checked_24px": p["accent"], "ic_selection_checked_24px__overlay": p["head"],
                "img_guild_folder": p["accent"],
            },
        },
        "background": {"url": f"{BASE}/crimson-fade-bg.png?v={BG_VERSION}", "blur": 0, "alpha": 1},
    }


def srgb_to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055) * 255.0


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64)


def background(p, w=1080, h=2400, tilt=20):
    stops = [(0.0, p["grad_top"]), (0.30, p["grad_top"]), (0.62, p["grad_mid"]), (1.0, p["grad_bot"])]
    # gradient axis tilted from vertical: dark top-left, red bottom-right
    th = np.radians(tilt)
    X, Y = np.meshgrid(np.arange(w) - w / 2, np.arange(h) - h / 2)
    d = X * np.sin(th) + Y * np.cos(th)
    reach = abs(w / 2 * np.sin(th)) + abs(h / 2 * np.cos(th))  # corners land on 0 and 1
    tt = (d / reach + 1) / 2
    img = np.zeros((h, w, 3))
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        m = (tt >= t0) & (tt <= t1)
        t = (tt[m] - t0) / (t1 - t0)
        t = t * t * (3 - 2 * t)  # smoothstep between stops: no visible kinks
        l0, l1 = srgb_to_lin(rgb(c0)), srgb_to_lin(rgb(c1))
        img[m] = l0 + (l1 - l0) * t[:, None]
    # soft glow at the red end of the axis for depth
    gx, gy = reach * 1.05 * np.sin(th), reach * 1.05 * np.cos(th)
    glow = np.exp(-(((X - gx) / (w * 0.75)) ** 2 + ((Y - gy) / (h * 0.45)) ** 2) * 1.6)
    img = img * (1 + 0.22 * glow[:, :, None])
    s = lin_to_srgb(img)
    rng = np.random.default_rng(7)
    grain = rng.normal(0, 1.1, (h, w, 1))  # mono grain, same on all channels
    dither = rng.random((h, w, 3)) - 0.5  # breaks 8-bit banding
    out = np.clip(np.round(s + grain * (0.4 + s / 255 * 2.5) + dither), 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGB")


def lum(h):
    l = srgb_to_lin(rgb(h[:7]))
    return 0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2]


def contrast(f, b):
    hi, lo = sorted((lum(f), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p = PALETTE
    with open(os.path.join(OUT, "crimson-fade.json"), "w") as f:
        json.dump(theme(p), f, indent=2)
    background(p).save(os.path.join(OUT, "crimson-fade-bg.png"), optimize=True)
    for fg in ("text", "sub", "muted", "link", "accent_hi"):
        for bg in ("bg1", "bg3", "grad_bot"):
            print(f"{fg:9} on {bg:8} {contrast(p[fg], p[bg]):5.1f}:1")
    print(f"white on accent    {contrast('#ffffff', p['accent']):5.1f}:1")
