"""Erzeugt assets/kreideberg.svg: weiße Kreidezeichnung eines Berggipfels mit Bogenschrift.

Eigene Zeichnung im Stil der Einladungskarte (Kreide auf Kraftpapier). Deterministisch (fester Seed),
damit Änderungen nachvollziehbar bleiben:  python3 scripts/kreideberg.py
"""
import math
import random
from pathlib import Path

W, H = 800, 430
BASE = 340
rnd = random.Random(2027)

# Umriss: niedrige Kette links, Hauptgipfel, langer Grat nach rechts, niedrige Kette rechts.
OUTLINE = [
    (0, 290), (14, 284), (30, 286), (44, 268), (52, 272), (66, 262), (80, 266), (92, 250),
    (100, 254), (114, 236), (122, 244), (134, 238), (146, 222), (156, 230), (170, 226),
    (184, 212), (196, 218), (210, 206), (222, 214), (238, 208), (250, 196), (266, 200),
    (284, 186), (300, 168), (310, 156), (318, 140), (326, 122), (334, 112), (340, 96),
    (348, 86), (352, 74), (362, 64), (370, 56), (380, 52), (388, 48), (396, 52), (402, 62),
    (410, 70), (424, 84), (438, 98), (456, 112), (474, 124), (494, 140), (512, 152),
    (534, 166), (556, 178), (578, 190), (598, 200), (612, 204), (624, 198), (636, 204),
    (650, 196), (662, 186), (676, 194), (690, 188), (700, 180), (716, 190), (730, 184),
    (744, 174), (756, 182), (770, 186), (786, 180), (800, 188),
]
FILL_OPACITY = .9


def ridge_noise(x0, y0, x1, y1, rough, depth, rng):
    """Mittelpunktverschiebung: unregelmäßige Bergkette zwischen zwei Punkten."""
    pts = [(x0, y0), (x1, y1)]
    for level in range(depth):
        nxt = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            nxt += [((ax + bx) / 2 + rng.uniform(-2, 2), (ay + by) / 2 + rng.uniform(-rough, rough)), (bx, by)]
        pts, rough = nxt, rough * 0.68
    return pts


_side = random.Random(7)
_peak = [p for p in OUTLINE if 284 <= p[0] <= 612]
OUTLINE = ridge_noise(0, 286, 284, 186, 44, 6, _side)[:-1] + _peak + ridge_noise(612, 204, 800, 184, 40, 6, _side)[1:]
SUMMIT = (384, 50)


def ridge_y(x):
    """Höhe des Umrisses an Stelle x (lineare Interpolation)."""
    for (x0, y0), (x1, y1) in zip(OUTLINE, OUTLINE[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return OUTLINE[-1][1]


def wobble(points, amount=1.2):
    return [(x + rnd.uniform(-amount, amount), y + rnd.uniform(-amount, amount)) for x, y in points]


def path_d(points):
    head, *tail = points
    return f"M{head[0]:.1f} {head[1]:.1f}" + "".join(f"L{x:.1f} {y:.1f}" for x, y in tail)


strokes = []


def stroke(points, width, opacity):
    strokes.append(
        f'<path d="{path_d(wobble(points))}" stroke-width="{width:.2f}" opacity="{opacity:.2f}"/>'
    )


# 1) Kreidestriche entlang der Hangneigung: dicht oben am Grat, nach unten ausdünnend.
for _ in range(1500):
    x = rnd.uniform(0, W)
    top = ridge_y(x)
    depth = rnd.betavariate(1.2, 2.6)          # meist nah am Grat
    y = top + 3 + depth * (BASE - top)
    # Hangrichtung: links vom Gipfel nach links unten, rechts davon nach rechts unten.
    sx, sy = SUMMIT
    if x < sx:
        angle = math.radians(rnd.uniform(118, 140))
    else:
        angle = math.radians(rnd.uniform(28, 50))
    length = rnd.uniform(5, 22) * (1.4 if 300 < x < 560 else 1.0)
    pts = [(x, y)]
    for i in range(1, 4):
        t = length * i / 3
        pts.append((x + math.cos(angle) * t + rnd.uniform(-1, 1), y + math.sin(angle) * t))
    fade = max(0.0, 1 - depth * 1.15)
    stroke(pts, rnd.uniform(0.8, 2.2), 0.35 + 0.6 * fade * rnd.uniform(0.6, 1))

# 2) Lange Rinnen/Grate am Hauptgipfel (lassen den Berg plastisch wirken).
for start, end, n in [((384, 52), (318, 250), 9), ((392, 56), (470, 236), 9), ((360, 64), (300, 210), 6),
                      ((410, 80), (540, 230), 7), ((340, 104), (262, 236), 5)]:
    for _ in range(n):
        (x0, y0), (x1, y1) = start, end
        dx, dy = rnd.uniform(-14, 14), rnd.uniform(-6, 6)
        pts = [(x0 + (x1 - x0) * t + dx * t + rnd.uniform(-2, 2), y0 + (y1 - y0) * t + dy * t)
               for t in (0, .2, .4, .6, .8, 1)]
        stroke(pts, rnd.uniform(0.7, 1.6), rnd.uniform(0.4, 0.8))

# 3) Dunkle, ausgewischte Schattenstreifen (Kraftpapier scheint durch), v. a. auf der rechten Flanke.
shadows = []
for _ in range(420):
    x = rnd.uniform(260, 700)
    top = ridge_y(x)
    y = top + rnd.uniform(6, 120)
    right = x > SUMMIT[0] - 10
    angle = math.radians(rnd.uniform(30, 52) if right else rnd.uniform(110, 128))
    length = rnd.uniform(10, 46)
    pts = [(x + math.cos(angle) * length * i / 3 + rnd.uniform(-1.2, 1.2), y + math.sin(angle) * length * i / 3)
           for i in range(4)]
    weight = 1.0 if right else 0.45
    shadows.append(f'<path d="{path_d(wobble(pts))}" stroke-width="{rnd.uniform(1, 3.2):.2f}" '
                   f'opacity="{rnd.uniform(.35, .85) * weight:.2f}"/>')

# 4) Kräftige Kontur des Grats (wie mit der Kreidekante gezogen), zweimal leicht versetzt.
for width, opacity in [(2.6, 0.95), (1.4, 0.7)]:
    stroke(OUTLINE, width, opacity)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Wir heiraten 2.0">
  <defs>
    <!-- Kreidekorn: Rauschen als Alphamaske, danach leichte Verzerrung der Kanten. -->
    <filter id="kreide" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="11" result="korn"/>
      <feColorMatrix in="korn" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  3.2 0 0 0 -1.05" result="maske"/>
      <feComposite in="SourceGraphic" in2="maske" operator="in" result="gekoernt"/>
      <feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="2" seed="4" result="welle"/>
      <feDisplacementMap in="gekoernt" in2="welle" scale="5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="kreide-flaeche" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency=".32 .5" numOctaves="4" seed="23" result="korn"/>
      <feColorMatrix in="korn" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  7 0 0 0 -2.6" result="maske"/>
      <feComposite in="SourceGraphic" in2="maske" operator="in" result="gekoernt"/>
      <feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="2" seed="5" result="welle"/>
      <feDisplacementMap in="gekoernt" in2="welle" scale="7" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <linearGradient id="ausblenden" x1="0" y1="0" x2="0" y2="1">
      <stop offset=".3" stop-color="#fff"/>
      <stop offset=".8" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="seiten" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset=".16" stop-color="#fff"/>
      <stop offset=".84" stop-color="#fff"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="vertikal" maskUnits="userSpaceOnUse" x="0" y="-50" width="{W}" height="{H + 100}">
      <rect y="-50" width="{W}" height="{H + 100}" fill="url(#ausblenden)"/>
    </mask>
    <!-- Unten und an den Seiten weich auslaufen lassen (kein harter Bildrand auf breiten Bildschirmen). -->
    <mask id="unten-weich" maskUnits="userSpaceOnUse" x="0" y="-50" width="{W}" height="{H + 100}">
      <rect y="-50" width="{W}" height="{H + 100}" fill="url(#seiten)" mask="url(#vertikal)"/>
    </mask>
    <path id="bogen" d="M290 118 A 100 100 0 0 1 490 118"/>
  </defs>
  <g mask="url(#unten-weich)" transform="translate(0 40)">
    <path d="{path_d(OUTLINE)}L{W} {BASE}L0 {BASE}Z" fill="#fffaf1" opacity="{FILL_OPACITY}" filter="url(#kreide-flaeche)"/>
    <g fill="none" stroke="#a67c58" stroke-linecap="round" filter="url(#kreide)">{"".join(shadows)}</g>
  </g>
  <g fill="none" stroke="#fffaf1" stroke-linecap="round" stroke-linejoin="round" filter="url(#kreide)" mask="url(#unten-weich)" transform="translate(0 40)">
    {"".join(strokes)}
  </g>
  <g fill="#fffaf1" font-family="'Josefin Sans', 'Avenir Next', Avenir, 'Century Gothic', 'Segoe UI', sans-serif" font-weight="400" text-anchor="middle">
    <text font-size="21" letter-spacing="8"><textPath href="#bogen" startOffset="50%">WIR HEIRATEN</textPath></text>
    <text x="390" y="52" font-size="15" letter-spacing="3">2.0</text>
  </g>
</svg>
'''

out = Path(__file__).resolve().parents[1] / "assets" / "kreideberg.svg"
out.write_text(svg, encoding="utf-8")
print(f"{out.name}: {len(strokes)} Striche, {out.stat().st_size // 1024} kB")
