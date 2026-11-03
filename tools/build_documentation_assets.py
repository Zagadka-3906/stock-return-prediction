"""Build local SVG documentation figures and a schematic GIF (Pillow required)."""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
THEMES = {
    "dark": {"bg": "#0b1422", "panel": "#122235", "ink": "#edf4fb", "muted": "#93a8bb", "line": "#26394d", "mint": "#68e3be", "gold": "#efbd73", "blue": "#7cafff"},
    "light": {"bg": "#f3f7fa", "panel": "#ffffff", "ink": "#102739", "muted": "#536b7d", "line": "#d8e3eb", "mint": "#087f68", "gold": "#ad6a16", "blue": "#356dc2"},
}


def svg_start(width: int, height: int, title: str, desc: str, theme: dict) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            f'<rect width="{width}" height="{height}" rx="22" fill="{theme["bg"]}"/>')


def label(x: float, y: float, value: str, size: int, color: str, weight: int = 400, mono: bool = False) -> str:
    family = "'Cascadia Mono', 'DejaVu Sans Mono', monospace" if mono else "Inter, 'Segoe UI', Arial, sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{family}" font-weight="{weight}">{escape(value)}</text>'


def hero(mode: str) -> str:
    t = THEMES[mode]
    out = [svg_start(1280, 440, "Stock Return Prediction", "A-share daily cross-sectional modeling. Ranking panel is an illustration, not performance data.", t)]
    out += [label(56, 53, "QUANTITATIVE RESEARCH / DAILY CROSS-SECTION", 12, t["muted"], 600, True),
            label(56, 129, "Stock Return", 61, t["ink"], 700),
            label(56, 197, "Prediction", 61, t["ink"], 700),
            f'<rect x="58" y="227" width="46" height="4" rx="2" fill="{t["mint"]}"/>',
            label(56, 266, "Price &amp; volume. Relative strength. Verifiable outputs.".replace("&amp;", "&"), 17, t["muted"])]
    # An explicitly labelled ranking schematic, never a synthetic equity curve.
    out += [f'<rect x="787" y="34" width="437" height="260" rx="15" fill="{t["panel"]}" stroke="{t["line"]}"/>',
            label(811, 64, "CROSS-SECTION / RANKING SCHEMATIC", 11, t["muted"], 500, True)]
    for i, w in enumerate([245, 205, 170, 138, 100]):
        y = 87 + i * 32
        out += [label(811, y + 13, f"0{i+1}", 12, t["muted"], 500, True),
                f'<rect x="857" y="{y}" width="{w}" height="16" rx="4" fill="{t["mint"]}" opacity="{1-i*0.14:.2f}"/>',
                f'<circle cx="1194" cy="{y+8}" r="3" fill="{t["line"]}"/>']
    out += [label(811, 274, "Compare stocks within the same trading day.", 12, t["muted"]),
            f'<path d="M56 318H1224" stroke="{t["line"]}"/>']
    stats = [(56, "4,650", "STOCKS IN THE RESEARCH PANEL"), (362, "63 + 4", "BASE + PEER FEATURES"), (668, "2020-24", "CONNECTED WALK-FORWARD"), (974, "CSV + SHA256", "PREDICTIONS & EVIDENCE")]
    for x, main, sub in stats:
        out += [label(x, 368, main, 25, t["ink"], 600, True), label(x, 398, sub, 10, t["muted"], 500, True)]
    out.append("</svg>")
    return "\n".join(out)


def score(mode: str) -> str:
    t = THEMES[mode]
    parts = [(0.4 * 0.12280208457197295, "Rank IC", "0.4 x 0.122802", t["blue"]),
             (0.3 * 0.3735093425702569, "Annual excess", "0.3 x 0.373509", t["gold"]),
             (0.3 * (1 - 0.032374723105348766), "List stability", "0.3 x (1 - 0.032375)", t["mint"])]
    total = sum(p[0] for p in parts)
    out = [svg_start(1280, 320, "Score contribution of the 37-model research ensemble", "Historical 2020-2024 connected validation. Components are Rank IC 0.049121, annual excess 0.112053, and list stability 0.290288.", t),
           label(48, 42, "WHAT DRIVES THE COMPOSITE SCORE?", 12, t["muted"], 600, True),
           label(48, 85, "Three components. One historical research metric.", 26, t["ink"], 600),
           label(995, 84, f"S = {total:.6f}", 22, t["ink"], 600, True)]
    x = 48.0
    for value, name, formula, color in parts:
        w = 1184 * value / total
        out += [f'<rect x="{x:.3f}" y="116" width="{w:.3f}" height="42" fill="{color}"/>']
        x += w
    for x, (value, name, formula, color) in zip([48, 445, 842], parts):
        out += [f'<rect x="{x}" y="190" width="10" height="10" rx="2" fill="{color}"/>',
                label(x+20, 201, name, 16, t["ink"], 600),
                label(x+20, 229, f"+ {value:.6f}", 20, t["ink"], 600, True),
                label(x+20, 254, formula, 12, t["muted"], 400, True)]
    out += [label(48, 296, "2020-2024 connected validation | recorded 2026-10-11 | not an independent blind test or live return", 12, t["muted"]), "</svg>"]
    return "\n".join(out)


STAGES = [("01 / INPUT", "Daily panel", "OHLCV + market flags"),
          ("02 / FEATURES", "Price & peers", "63 base + 4 peer"),
          ("03 / MODELS", "Learn signals", "Trees / neural nets"),
          ("04 / COMBINE", "Rank & stabilize", "Blend / smooth / map"),
          ("05 / VERIFY", "Prediction CSV", "Reload / replay / hash")]


def pipeline_svg() -> str:
    t = THEMES["dark"]
    out = [svg_start(1280, 240, "Research pipeline", "Schematic sequence: daily panel, features, models, combination, verified predictions.", t),
           label(35, 35, "FROM DAILY OBSERVATIONS TO VERIFIED PREDICTIONS", 12, t["muted"], 600, True)]
    for i, (small, main, sub) in enumerate(STAGES):
        x = 35 + i * 246
        out += [f'<rect x="{x}" y="67" width="225" height="117" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>',
                label(x+15, 92, small, 10, t["mint"], 600, True), label(x+15, 125, main, 19, t["ink"], 600), label(x+15, 157, sub, 11, t["muted"], 400, True)]
        if i < 4:
            out += [f'<path d="M{x+230} 125h11m-4-4 4 4-4 4" fill="none" stroke="{t["mint"]}" stroke-width="1.5"/>']
    out += [label(35, 216, "Process illustration only. Model training and historical replay use separate documented entry points.", 11, t["muted"]), "</svg>"]
    return "\n".join(out)


def pipeline_gif() -> None:
    from PIL import Image, ImageDraw, ImageFont
    t = THEMES["dark"]
    def font(size: int, mono: bool = False):
        choices = (["C:/Windows/Fonts/CascadiaMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"] if mono else
                   ["C:/Windows/Fonts/segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
        for p in choices:
            if Path(p).is_file():
                return ImageFont.truetype(p, size)
        return ImageFont.load_default(size=size)
    fonts = {"small": font(10, True), "main": font(19), "sub": font(11, True), "top": font(12, True), "note": font(11)}
    frames = []
    for frame in range(60):
        im = Image.new("RGB", (1280, 240), t["bg"])
        d = ImageDraw.Draw(im)
        d.text((35, 20), "FROM DAILY OBSERVATIONS TO VERIFIED PREDICTIONS", font=fonts["top"], fill=t["muted"])
        active = min(frame // 10, 4)
        for i, (small, main, sub) in enumerate(STAGES):
            x = 35 + i * 246
            d.rounded_rectangle((x, 67, x+225, 184), radius=12, fill=t["panel"], outline=t["mint"] if i == active else t["line"], width=2 if i == active else 1)
            d.text((x+15, 81), small, font=fonts["small"], fill=t["mint"])
            d.text((x+15, 107), main, font=fonts["main"], fill=t["ink"])
            d.text((x+15, 145), sub, font=fonts["sub"], fill=t["muted"])
            if i < 4:
                d.line((x+230, 125, x+241, 125), fill=t["muted"])
                d.line((x+237, 121, x+241, 125, x+237, 129), fill=t["muted"])
        end = 35 + 1209 * min(frame / 49, 1)
        d.line((35, 197, 1244, 197), fill=t["line"], width=2)
        d.line((35, 197, end, 197), fill=t["mint"], width=2)
        d.ellipse((end-3, 194, end+3, 200), fill=t["mint"])
        d.text((35, 208), "Process illustration only. Not training progress or market performance.", font=fonts["note"], fill=t["muted"])
        frames.append(im.quantize(colors=64))
    frames[0].save(ASSETS / "pipeline.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True, disposal=2)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for mode in THEMES:
        (ASSETS / f"hero-{mode}.svg").write_text(hero(mode), encoding="utf-8")
        (ASSETS / f"score-{mode}.svg").write_text(score(mode), encoding="utf-8")
    (ASSETS / "pipeline.svg").write_text(pipeline_svg(), encoding="utf-8")
    pipeline_gif()
    for p in sorted(ASSETS.iterdir()):
        print(f"{p.name}: {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
