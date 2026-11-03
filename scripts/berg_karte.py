"""Erzeugt assets/berg-einladungskarte.webp: den Berg der Einladungskarte als weiße, transparente Kreide.

Quelle: Screenshot der Karte (nicht im Repository). Ablauf: Ausschnitt -> 3x hochskalieren -> Kreide über
den Blaukanal vom Kraftpapier trennen (lokale Papierhelligkeit abgezogen) -> steile Schwelle, damit das
Weiß deckend und die Kanten klar bleiben -> Kartenschrift entfernen -> Ränder weich auslaufen lassen.
    /usr/bin/python3 scripts/berg_karte.py "<screenshot.png>"
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

SRC = Path(sys.argv[1])
BOX = (104, 148, 762, 430)          # Bergausschnitt im Screenshot (809x706)
UP = 3                              # Hochskalierung

img = Image.open(SRC).convert('RGB').crop(BOX)
w, h = img.size
big = img.resize((w * UP, h * UP), Image.LANCZOS)
b = np.asarray(big.getchannel('B'), dtype=np.float32)

# Papierhelligkeit lokal schätzen (Kreide wegklappen, dann stark weichzeichnen) und abziehen.
paper = Image.fromarray(np.minimum(b, 135).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40 * UP))
diff = b - np.asarray(paper, dtype=np.float32)
alpha = np.clip((diff - 26) / 46, 0, 1)                 # steil: deckendes Weiß statt Schleier
alpha = alpha ** 0.8

yy, xx = np.mgrid[0:h * UP, 0:w * UP].astype(np.float32) / UP   # Koordinaten im Ausschnitt
# Reste der Kartenschrift „Wir heiraten 2.0" oberhalb der Flanken entfernen (Gipfel bleibt).
alpha[(yy < 50) & ((xx < 268) | (xx > 378))] = 0
# Ränder weich auslaufen lassen (keine harte Kante auf breiten Bildschirmen).
fx = np.clip(np.minimum(xx, w - xx) / 45, 0, 1)
fy = np.clip((h - yy) / 30, 0, 1)
alpha *= fx * fy

rgba = np.zeros((h * UP, w * UP, 4), dtype=np.uint8)
rgba[..., 0], rgba[..., 1], rgba[..., 2] = 255, 250, 241
rgba[..., 3] = (alpha * 255).astype(np.uint8)
out = Path(__file__).resolve().parents[1] / 'assets' / 'berg-einladungskarte.webp'
Image.fromarray(rgba, 'RGBA').save(out, 'WEBP', quality=90, method=6)
print(f'{out.name}: {w * UP}x{h * UP}, {out.stat().st_size // 1024} kB')
