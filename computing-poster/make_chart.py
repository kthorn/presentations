"""Generate the charts and table.md: peak computing power over time.

Supercomputers vs. the machines in people's homes, on one log scale.
Data: data/machines.csv (one row per machine, with sources) and
data/top500_number1.csv (the #1 machine on every Top500 list since 1993).

Two layouts from the same data: chart.png (landscape poster, every machine
labeled) and chart-mobile.png (4:5 portrait for social media, a few labels).
"""
import csv
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
CHROME = Path.home() / ".cache/ms-playwright/chromium-1234/chrome-linux64/chrome"

X0, X1 = 1975, 2030                     # years
Y0, Y1 = 6, 19                          # log10 FLOPS

INK, INK2, MUTED, GRID, SURFACE, BAND = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#fcfcfb", "#e9e8e3"
# dataviz reference palette, validated all-pairs for these slots
SERIES = {
    "supercomputer": dict(color="#4a3aa7", shape="square"),
    "home":          dict(color="#2a78d6", shape="circle"),
    "phone":         dict(color="#1baf7a", shape="triangle"),
}
GROUP = {"tablet": "phone", "pc": "home", "console": "home"}

PREFIXES = [(3, "thousand", "kFLOPS"), (6, "million", "MFLOPS"), (9, "billion", "GFLOPS"),
            (12, "trillion", "TFLOPS"), (15, "quadrillion", "PFLOPS"), (18, "quintillion", "EFLOPS")]
MONTH = {"Jun": 6, "Nov": 11}
REPO = "github.com/kthorn/presentations/tree/main/computing-poster"


@dataclass(frozen=True)
class Layout:
    out: str
    W: int
    H: int
    margins: tuple          # L, R, T, B
    title: tuple            # one string per line
    subtitle: tuple
    footnote: tuple
    legend: dict            # group -> legend text
    # Label placement: name -> (dx, dy, anchor[, text]), or None for no label.
    # With label_all, unlisted machines are labeled to the right of the point;
    # without it, only listed machines get a marker and a label.
    labels: dict
    label_all: bool
    fs: dict                # font sizes
    band_label: str
    band_at: tuple          # (year, flops): label center, or the note's top-left corner
    band_note: bool = False  # horizontal note with a grey swatch instead of a label along the ribbon
    marker_r: float = 7
    pad: int = 60           # page margin for the title and footnote

    @property
    def plot(self):
        L, R, T, B = self.margins
        return L, T, self.W - R, self.H - B

    def sx(self, year):
        x0, _, x1, _ = self.plot
        return x0 + (year - X0) / (X1 - X0) * (x1 - x0)

    def sy(self, flops):
        _, y0, _, y1 = self.plot
        return y1 - (math.log10(flops) - Y0) / (Y1 - Y0) * (y1 - y0)


LEFT, ABOVE_LEFT = (-13, 5, "end"), (-10, -12, "end")
POSTER = Layout(
    out="chart", W=2400, H=1600, margins=(150, 70, 190, 130),
    title=("Yesterday's supercomputer is in your living room",),
    subtitle=("Peak calculations per second, log scale. Each step up the grid is ten times faster.",),
    footnote=("Peak floating-point operations per second. Supercomputers rated at 64-bit precision (Top500 Rpeak); "
              "consoles, graphics cards and phones at their advertised 32-bit figure. Each line follows the best "
              f"machine so far. Data and sources: {REPO}",),
    legend={"supercomputer": "World's fastest supercomputer", "home": "Home PCs &amp; game consoles",
            "phone": "iPhones &amp; iPads"},
    labels={
        "CDC 6600": ABOVE_LEFT, "CDC 7600": ABOVE_LEFT, "Cray-1": ABOVE_LEFT,
        "Cray X-MP": ABOVE_LEFT, "Cray-2": (-12, -6, "end"),
        "Connection Machine CM-2": ABOVE_LEFT, "Cray Y-MP": (10, -12, "start"),
        "Connection Machine CM-5": ABOVE_LEFT, "ASCI Red": ABOVE_LEFT, "ASCI White": ABOVE_LEFT,
        "Earth Simulator": ABOVE_LEFT, "Blue Gene/L": None, "Roadrunner": ABOVE_LEFT,
        "Summit": ABOVE_LEFT, "Fugaku": ABOVE_LEFT, "Frontier": ABOVE_LEFT,
        "El Capitan": (-10, -14, "end"), "LineShine": (10, -12, "start"),
        "NVIDIA GeForce 256": None, "Intel Pentium III": (12, 14, "start"),
        "Sega Dreamcast": LEFT, "PlayStation 2": LEFT, "Xbox": None,
        "PlayStation 3": None, "Xbox One": None, "Xbox One X": (12, 16, "start"),
        "Xbox 360": ABOVE_LEFT, "NVIDIA GeForce 8800 GTX": (12, 18, "start"), "NVIDIA GTX 1080": LEFT,
        "Xbox Series X": None, "PS5 Pro": (12, 12, "start"),
        "PlayStation 5": (12, 18, "start"), "NVIDIA RTX 4090": None,
        "iPhone 17": None, "iPad Pro (M4)": None, "iPad Pro (M5)": (12, -6, "start"),
        "iPhone 17 Pro": (12, 20, "start"), "Nintendo Switch 2": (12, 5, "start"),
    },
    label_all=True,
    fs=dict(title=44, subtitle=21, legend=17, label=15, tick=17, unit=13, axis=15, band=19, foot=13),
    band_label="Home machines trail by about {lag} years", band_at=(1997, 2e10),
)

MOBILE = Layout(
    out="chart-mobile", W=800, H=1000, margins=(150, 24, 232, 142),
    title=("Yesterday's supercomputer", "is in your living room"),
    subtitle=("Calculations per second. Each gridline is 10× faster.",),
    footnote=("Advertised peak speeds: 64-bit for supercomputers, 32-bit for",
              "consoles, graphics cards and phones. Data and sources:", REPO),
    legend={"supercomputer": "Supercomputers", "home": "PCs &amp; consoles", "phone": "iPhones &amp; iPads"},
    labels={
        "Cray-1": (10, 24, "start"), "Cray-2": (-10, -10, "end"),
        "Connection Machine CM-5": (-10, -10, "end", "Connection Machine"),
        "ASCI Red": (-10, -10, "end"), "Roadrunner": (-10, -10, "end"), "El Capitan": (-10, -10, "end"),
        "Intel 486DX": (11, 5, "start", "486 PC"), "PlayStation 2": (-11, 5, "end"),
        "Xbox 360": (-11, 5, "end"), "PlayStation 4": (-11, 5, "end"), "PlayStation 5": (-11, 5, "end"),
        "NVIDIA RTX 5090": (-11, 5, "end", "RTX 5090"),
        "Original iPhone": (11, 5, "start"), "iPhone 17 Pro": (9, -4, "start", "iPhone\n17 Pro"),
    },
    label_all=False,
    fs=dict(title=40, subtitle=19, legend=18, label=17, tick=16, unit=12, axis=14, band=17, foot=13),
    band_label="Grey band: home machines trail\nsupercomputers by about {lag} years",
    band_at=(1976.5, 3e17), band_note=True, marker_r=6.5, pad=24,
)


def human(flops):
    for exp, word, _ in reversed(PREFIXES):
        if flops >= 10 ** exp:
            return f"{flops / 10 ** exp:.3g} {word}"
    return f"{flops:,.0f}"


def halo(attrs=""):
    return f'{attrs} paint-order="stroke" stroke="{SURFACE}" stroke-width="5" stroke-linejoin="round"'


def marker(shape, x, y, color, r=7):
    ring = f'stroke="{SURFACE}" stroke-width="2"'
    if shape == "circle":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" {ring}/>'
    if shape == "square":
        return f'<rect x="{x - r:.1f}" y="{y - r:.1f}" width="{2 * r}" height="{2 * r}" rx="2" fill="{color}" {ring}/>'
    r *= 1.25  # triangle
    pts = f"{x:.1f},{y - r:.1f} {x + r * 0.95:.1f},{y + r * 0.7:.1f} {x - r * 0.95:.1f},{y + r * 0.7:.1f}"
    return f'<polygon points="{pts}" fill="{color}" {ring}/>'


def load():
    """Machines with a FLOPS figure, placed at mid-year (or their Top500 debut list)."""
    with open(HERE / "data/machines.csv") as f:
        rows = [r for r in csv.DictReader(f) if r["peak_flops"]]
    for r in rows:
        r["group"] = GROUP.get(r["category"], r["category"])
        r["flops"] = float(r["peak_flops"])
        if r["top500_debut"]:
            y, m = r["top500_debut"].split("-")
            r["x"] = int(y) + (int(m) - 0.5) / 12
        else:
            r["x"] = int(r["year"]) + 0.5
    return rows


def load_top500():
    with open(HERE / "data/top500_number1.csv") as f:
        return [dict(x=int(r["year"]) + (MONTH[r["list"]] - 0.5) / 12, flops=float(r["rpeak_flops"]))
                for r in csv.DictReader(f)]


def envelopes(rows, top500):
    """Per group, the best-so-far machines in date order: the line we draw."""
    out = {}
    for g in SERIES:
        pts = [r for r in rows if r["group"] == g] + (top500 if g == "supercomputer" else [])
        best, line = 0, []
        for p in sorted(pts, key=lambda p: p["x"]):
            if p["flops"] > best:
                best = p["flops"]
                line.append((p["x"], p["flops"]))
        out[g] = line
    return out


def reach_year(line, flops):
    """When a group's line first reaches `flops` (log-linear between points)."""
    if line[0][1] > flops:
        return None
    for (xa, fa), (xb, fb) in zip(line, line[1:]):
        if fb >= flops:
            if fa >= flops:
                return xa
            t = (math.log10(flops) - math.log10(fa)) / (math.log10(fb) - math.log10(fa))
            return xa + t * (xb - xa)
    return None


def reach_flops(line, x):
    """A line's value at year x (log-linear between points)."""
    for (xa, fa), (xb, fb) in zip(line, line[1:]):
        if xa <= x <= xb:
            return 10 ** (math.log10(fa) + (x - xa) / (xb - xa) * (math.log10(fb) - math.log10(fa)))
    return line[-1][1]


def average_lag(env):
    """Average years between a home machine and the supercomputer that first matched it."""
    sup = env["supercomputer"]
    lags = [x - reach_year(sup, f) for x, f in env["home"] if reach_year(sup, f)]
    return sum(lags) / len(lags)


def lag_band(lay, env):
    """Grey ribbon: the supercomputer line, and the same line shifted later by the average lag.

    Returns the ribbon (drawn under the grid) and its label (drawn on top)."""
    sup, lag = env["supercomputer"], average_lag(env)
    # start the ribbon at the chart's left edge so it closes inside the plot
    top = [(X0, reach_flops(sup, X0))] + [(x, f) for x, f in sup if x > X0]
    edge = top + [(x + lag, f) for x, f in reversed(top)]
    poly = " ".join(f"{lay.sx(x):.1f},{lay.sy(f):.1f}" for x, f in edge)
    text = lay.band_label.format(lag=round(lag))
    year, flops = lay.band_at
    if lay.band_note:
        x, y, fs = lay.sx(year), lay.sy(flops), lay.fs["band"]
        return [f'<polygon points="{poly}" fill="{BAND}" clip-path="url(#plot)"/>'], [
                f'<rect x="{x:.1f}" y="{y - fs * 0.8:.1f}" width="{fs * 1.6:.1f}" height="{fs:.1f}" rx="3" fill="{BAND}"/>',
                multiline(x + fs * 2.2, y, text, f'font-size="{fs}" font-weight="600" fill="{INK2}" {halo()}')]
    # label in the open middle of the ribbon, angled to the long-run slope
    cx, cy = lay.sx(year), lay.sy(flops)
    rise = math.log10(reach_flops(sup, 2005) / reach_flops(sup, 1985)) / 20
    angle = math.degrees(math.atan2(lay.sy(flops * 10 ** rise) - cy, lay.sx(year + 1) - cx))
    return [f'<polygon points="{poly}" fill="{BAND}" clip-path="url(#plot)"/>'], [
        f'<text x="{cx:.1f}" y="{cy + 6:.1f}" font-size="{lay.fs["band"]}" font-weight="600" fill="{INK2}" text-anchor="middle" '
        f'transform="rotate({angle:.1f} {cx:.1f} {cy:.1f})">{text}</text>',
    ]


def axes(lay):
    x0, y0, x1, y1 = lay.plot
    fs, out = lay.fs, []
    for exp in range(Y0, Y1 + 1):
        y = lay.sy(10 ** exp)
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="{1.5 if exp % 3 == 0 else 0.75}"/>')
    for exp, word, unit in PREFIXES:
        if exp < Y0:
            continue
        y = lay.sy(10 ** exp)
        out.append(f'<text x="{x0 - 14}" y="{y - 2:.1f}" font-size="{fs["tick"]}" font-weight="600" fill="{INK2}" text-anchor="end">1 {word}</text>')
        out.append(f'<text x="{x0 - 14}" y="{y + fs["tick"]:.1f}" font-size="{fs["unit"]}" fill="{MUTED}" text-anchor="end">{unit}</text>')
    for year in range(math.ceil(X0 / 10) * 10, X1 + 1, 10):
        x = lay.sx(year)
        out.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y1}" stroke="{GRID}" stroke-width="0.75"/>')
        out.append(f'<text x="{x:.1f}" y="{y1 + 30}" font-size="{fs["tick"]}" font-weight="600" fill="{INK2}" text-anchor="middle">{year}</text>')
    out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{y1 + 30 + 2 * fs["axis"]}" font-size="{fs["axis"]}" fill="{MUTED}" text-anchor="middle">year introduced</text>')
    out.append(f'<text x="{x0 - 14}" y="{y0 - 26}" font-size="{fs["axis"]}" fill="{MUTED}" text-anchor="end">calculations</text>')
    out.append(f'<text x="{x0 - 14}" y="{y0 - 8}" font-size="{fs["axis"]}" fill="{MUTED}" text-anchor="end">per second</text>')
    return out


def series_lines(lay, env):
    out = []
    for g, line in env.items():
        d = " ".join(f'{"M" if i == 0 else "L"}{lay.sx(x):.1f},{lay.sy(f):.1f}' for i, (x, f) in enumerate(line))
        out.append(f'<path d="{d}" fill="none" stroke="{SERIES[g]["color"]}" stroke-width="2.5" stroke-opacity="0.6" '
                   f'stroke-linejoin="round" clip-path="url(#plot)"/>')
    return out


def points(lay, rows):
    out, labels = [], []
    for r in rows:
        if r["x"] < X0 or r["flops"] < 10 ** Y0:
            continue
        if not lay.label_all and r["name"] not in lay.labels:
            continue
        s = SERIES[r["group"]]
        x, y = lay.sx(r["x"]), lay.sy(r["flops"])
        out.append(marker(s["shape"], x, y, s["color"], lay.marker_r))
        place = lay.labels.get(r["name"], (12, 5, "start"))
        if place:
            dx, dy, anchor, *text = place
            labels.append(multiline(x + dx, y + dy, text[0] if text else r["name"],
                                    f'font-size="{lay.fs["label"]}" font-weight="600" fill="{INK}" text-anchor="{anchor}" {halo()}'))
    return out + labels


def multiline(x, y, text, attrs):
    """A <text> whose lines (split on newlines) stack downward from baseline y."""
    lines = text.split("\n")
    if len(lines) == 1:
        return f'<text x="{x:.1f}" y="{y:.1f}" {attrs}>{text}</text>'
    spans = "".join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else 1.2}em">{line}</tspan>' for i, line in enumerate(lines))
    return f'<text x="{x:.1f}" y="{y:.1f}" {attrs}>{spans}</text>'


def legend(lay):
    fs, out = lay.fs["legend"], []
    x, y = lay.plot[0], lay.plot[1] - 46
    for g, text in lay.legend.items():
        s = SERIES[g]
        out.append(marker(s["shape"], x + 8, y - fs * 0.3, s["color"], lay.marker_r))
        out.append(f'<text x="{x + 24}" y="{y}" font-size="{fs}" font-weight="600" fill="{INK}">{text}</text>')
        x += 24 + len(text.replace("&amp;", "&")) * fs * 0.59 + 2.4 * fs
    return out


def header(lay):
    fs, x, out = lay.fs, lay.pad, []
    y = 26 + fs["title"]
    for line in lay.title:
        out.append(f'<text x="{x}" y="{y}" font-size="{fs["title"]}" font-weight="700" fill="{INK}">{line}</text>')
        y += fs["title"] * 1.15
    y += fs["subtitle"] * 1.7 - fs["title"] * 1.15
    for line in lay.subtitle:
        out.append(f'<text x="{x}" y="{y:.0f}" font-size="{fs["subtitle"]}" fill="{INK2}">{line}</text>')
        y += fs["subtitle"] * 1.3
    y = lay.H - 24 - (len(lay.footnote) - 1) * fs["foot"] * 1.35
    for line in lay.footnote:
        out.append(f'<text x="{x}" y="{y:.0f}" font-size="{fs["foot"]}" fill="{MUTED}">{line}</text>')
        y += fs["foot"] * 1.35
    return out


def table(rows, env):
    """Markdown table: every machine, and which year's #1 supercomputer it matches."""
    lines = ["| Year | Machine | Kind | Peak calculations / sec | Precision | Matches the world's fastest of | Source |",
             "|---|---|---|---|---|---|---|"]
    kind = {"supercomputer": "Supercomputer", "pc": "PC", "console": "Console", "phone": "Phone", "tablet": "Tablet"}
    for r in sorted(rows, key=lambda r: (r["x"], r["name"])):
        match = ""
        if r["group"] != "supercomputer":
            when = reach_year(env["supercomputer"], r["flops"])
            match = f"~{int(when)}" if when else "before 1964"
        lines.append(f"| {r['year']} | {r['name']} | {kind[r['category']]} | {human(r['flops'])} ({r['flops']:.3g}) "
                     f"| {r['precision']} | {match} | [link]({r['source_url']}) |")
    return "\n".join(lines) + "\n"


def render(lay, rows, env):
    x0, y0, x1, y1 = lay.plot
    # relative to the SVG, so it renders the same from any checkout
    font_faces = "".join(f"@font-face{{font-family:Montserrat;font-weight:{w};src:url('fonts/Montserrat-{n}.ttf')}}"
                         for n, w in [("Regular", 400), ("SemiBold", 600), ("Bold", 700)])
    band, band_label = lag_band(lay, env)
    body = "\n  ".join(band + axes(lay) + series_lines(lay, env) + points(lay, rows) + band_label
                       + legend(lay) + header(lay))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{lay.W}" height="{lay.H}" viewBox="0 0 {lay.W} {lay.H}" font-family="Montserrat, 'Helvetica Neue', Arial, sans-serif">
  <style>{font_faces}</style>
  <rect width="{lay.W}" height="{lay.H}" fill="{SURFACE}"/>
  <clipPath id="plot"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath>
  {body}
</svg>
"""
    svg_path, png_path = HERE / f"{lay.out}.svg", HERE / f"{lay.out}.png"
    svg_path.write_text(svg)
    subprocess.run([str(CHROME), "--headless", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={lay.W},{lay.H}", f"--screenshot={png_path}", svg_path.as_uri()],
                   check=True, capture_output=True)
    print(f"{lay.out}.svg {lay.out}.png")


def build():
    rows = load()
    env = envelopes(rows, load_top500())
    for lay in (POSTER, MOBILE):
        render(lay, rows, env)
    (HERE / "table.md").write_text(table(rows, env))
    print("table.md")


if __name__ == "__main__":
    build()
