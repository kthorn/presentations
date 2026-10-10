"""Generate slide1.svg — Projects for an audience of one.

The cocktail map is drawn from assets/mixology-em.json
(https://mixology.tools/api/v1/analytics/cocktail-space-em) so the
Last Word family can be highlighted.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
NAVY, CORAL, BLUE, INK = "#4D6182", "#F74F58", "#3A96DB", "#5C6B82"

TILE_W, IMG_H, GAP, TOP = 464, 410, 40, 236
XS = [64 + i * (TILE_W + GAP) for i in range(3)]


def cocktail_map(x0, y0, w, h):
    data = json.load(open(HERE / "assets/mixology-em.json"))["data"]
    xs = [r["x"] for r in data]
    ys = [r["y"] for r in data]
    pad = 18
    sx = lambda v: x0 + pad + (v - min(xs)) / (max(xs) - min(xs)) * (w - 2 * pad)
    sy = lambda v: y0 + pad + (max(ys) - v) / (max(ys) - min(ys)) * (h - 2 * pad)

    def in_family(r):
        return "word" in r["recipe_name"].lower() and 3.8 < r["x"] < 5.0 and 5.5 < r["y"] < 7.6

    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#FFFFFF"/>']
    family = [r for r in data if in_family(r)]
    for r in data:
        if not in_family(r):
            out.append(f'<circle cx="{sx(r["x"]):.1f}" cy="{sy(r["y"]):.1f}" r="2.6" fill="{NAVY}" fill-opacity="0.32"/>')
    for r in family:
        out.append(f'<circle cx="{sx(r["x"]):.1f}" cy="{sy(r["y"]):.1f}" r="4" fill="{CORAL}"/>')
    # callout for the Last Word cluster
    cx = sum(sx(r["x"]) for r in family) / len(family)
    cy = sum(sy(r["y"]) for r in family) / len(family)
    lx, ly = x0 + 24, y0 + h - 62
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="20" fill="none" stroke="{CORAL}" stroke-width="2.5"/>')
    out.append(f'<line x1="{cx - 14:.1f}" y1="{cy + 15:.1f}" x2="{lx + 120}" y2="{ly - 22}" stroke="{CORAL}" stroke-width="2"/>')
    out.append(f'<text x="{lx}" y="{ly}" font-size="17" font-weight="700" fill="{CORAL}" paint-order="stroke" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round">{len(family)} Last Word riffs,</text>')
    out.append(f'<text x="{lx}" y="{ly + 22}" font-size="17" font-weight="700" fill="{CORAL}" paint-order="stroke" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round">found as neighbors</text>')
    out.append(f'<text x="{x0 + w - 14}" y="{y0 + 26}" font-size="14" font-weight="600" fill="{INK}" text-anchor="end" paint-order="stroke" stroke="#FFFFFF" stroke-width="6" stroke-linejoin="round">{len(data):,} recipes · learned distances</text>')
    return "\n    ".join(out)


def armory_grid(x0, y0, w, h):
    names = ["kfc", "koopa", "staff", "mech"]
    cw, ch = w / 2, h / 2
    out = []
    for i, n in enumerate(names):
        x, y = x0 + (i % 2) * cw, y0 + (i // 2) * ch
        out.append(f'<image href="assets/armory-{n}.jpg" x="{x}" y="{y}" width="{cw}" height="{ch}" preserveAspectRatio="xMidYMid slice"/>')
    # one of his actual prompts, as a caption on the bucket
    out.append(f'<rect x="{x0 + 10}" y="{y0 + ch - 44}" width="{cw - 20}" height="34" rx="6" fill="#000000" fill-opacity="0.72"/>')
    out.append(f'<text x="{x0 + cw / 2}" y="{y0 + ch - 21}" font-size="15" font-weight="600" fill="#FFFFFF" text-anchor="middle">“Giant KFC chicken bucket”</text>')
    return "\n    ".join(out)


def mace_pair(x0, y0, w, h):
    """Film prop (core outlined) beside Claude's OpenSCAD render of the core."""
    half = w / 2
    # mace-film-crop.jpg is 740x1330; with meet it fills the half height
    k = min(half / 740, h / 1330)
    ox = x0 + (half - 740 * k) / 2
    oy = y0 + (h - 1330 * k) / 2
    out = [
        f'<rect x="{x0}" y="{y0}" width="{half}" height="{h}" fill="#FFFFFF"/>',
        f'<image href="assets/mace-film-crop.jpg" x="{x0}" y="{y0}" width="{half}" height="{h}" preserveAspectRatio="xMidYMid meet"/>',
        # the hex core, in film-crop pixel coordinates (297..526, 333..1248)
        f'<rect x="{ox + 297 * k:.1f}" y="{oy + 333 * k:.1f}" width="{229 * k:.1f}" height="{915 * k:.1f}" rx="12" '
        f'fill="none" stroke="{CORAL}" stroke-width="3" stroke-dasharray="7 5"/>',
        f'<rect x="{x0 + half}" y="{y0}" width="{half}" height="{h}" fill="#F8F8F8"/>',
        f'<image href="assets/mace-holder-crop.png" x="{x0 + half + 12}" y="{y0}" width="{half - 24}" height="{h}" preserveAspectRatio="xMidYMid meet"/>',
        f'<line x1="{x0 + half}" y1="{y0}" x2="{x0 + half}" y2="{y0 + h}" stroke="#D5DCE6" stroke-width="1.5"/>',
    ]
    for cx, label in ((x0 + half / 2, "The film prop"), (x0 + 1.5 * half, "Claude's OpenSCAD")):
        out.append(f'<rect x="{cx - 82}" y="{y0 + h - 52}" width="164" height="32" rx="6" fill="#000000" fill-opacity="0.72"/>')
        out.append(f'<text x="{cx}" y="{y0 + h - 30}" font-size="14" font-weight="600" fill="#FFFFFF" text-anchor="middle">{label}</text>')
    out.append(f'<rect x="{x0 + half / 2 - 84}" y="{y0 + h - 16}" width="168" height="14" rx="3" fill="#FFFFFF" fill-opacity="0.9"/>')
    out.append(f'<text x="{x0 + half / 2}" y="{y0 + h - 5}" font-size="10" fill="#5C6B82" text-anchor="middle">photo: Royal Armouries replica</text>')
    return "\n    ".join(out)


TILES = [
    dict(name="mixology.tools",
         body=["I wanted to do ML on cocktail recipes.", "No data existed, so I built a DB + website."],
         stat="18 months · 800+ commits · weekly use",
         art=cocktail_map),
    dict(name="infinitearmory.fly.dev",
         body=["Agent-crafted fantasy / sci-fi weapons,", "built for my son on a ski trip."],
         stat="~1 week · 150 commits · 1 demanding user",
         art=armory_grid),
    dict(name="Sauron's Mace cosplay",
         body=["Claude designed the 3D-printed core that", "holds the blades, then measured the fit."],
         stat="1 weekend · OpenSCAD · 3D printer",
         art=mace_pair),
]


def tile(x, t, i):
    return f"""
  <clipPath id="clip{i}"><rect x="{x}" y="{TOP}" width="{TILE_W}" height="{IMG_H}" rx="14"/></clipPath>
  <g clip-path="url(#clip{i})">
    {t["art"](x, TOP, TILE_W, IMG_H)}
  </g>
  <rect x="{x}" y="{TOP}" width="{TILE_W}" height="{IMG_H}" rx="14" fill="none" stroke="#D5DCE6" stroke-width="1.5"/>
  <text x="{x}" y="{TOP + IMG_H + 52}" font-size="30" font-weight="700" fill="{NAVY}">{t["name"]}</text>
  <text font-size="20" fill="{INK}">
    <tspan x="{x}" y="{TOP + IMG_H + 88}">{t["body"][0]}</tspan>
    <tspan x="{x}" y="{TOP + IMG_H + 116}">{t["body"][1]}</tspan>
  </text>
  <text x="{x}" y="{TOP + IMG_H + 160}" font-size="17" font-weight="700" letter-spacing="0.4" fill="{BLUE}">{t["stat"]}</text>"""


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" font-family="Montserrat, 'Helvetica Neue', Arial, sans-serif">
  <rect width="1600" height="900" fill="#FFFFFF"/>
  <text x="64" y="58" font-size="16" font-weight="700" letter-spacing="2.4" fill="{NAVY}">KURT THORN / AFTER HOURS</text>
  <text x="1536" y="58" font-size="16" font-weight="700" letter-spacing="1.2" fill="{BLUE}" text-anchor="end">01 / AUDIENCE OF ONE</text>
  <text x="64" y="128" font-size="52" font-weight="700" fill="{NAVY}">Projects for an audience of one.</text>
  <text x="64" y="180" font-size="24" fill="{INK}">Not throwaway, just never worth the engineering before. Now it is.</text>
  {"".join(tile(x, t, i) for i, (x, t) in enumerate(zip(XS, TILES)))}
</svg>
"""

(HERE / "slide1.svg").write_text(svg)
print("slide1.svg")
