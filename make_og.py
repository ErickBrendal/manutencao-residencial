#!/usr/bin/env python3
"""Gera a imagem de preview (Open Graph) para o WhatsApp - 1200x630."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1200, 630
NAVY_TOP = (16, 40, 68)
NAVY_BOT = (9, 20, 35)
ORANGE = (244, 121, 32)
ORANGE_L = (255, 145, 60)
WHITE = (255, 255, 255)
WHATS = (37, 211, 102)
CARD = (18, 39, 66)

# ---------- background: vertical gradient + soft radial glow (numpy, sem artefatos) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
t = yy / H
bg = np.zeros((H, W, 3), np.float32)
for i in range(3):
    bg[..., i] = NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t

# radial glow centered top-middle
cx, cy = W * 0.5, -30.0
dist = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.3) ** 2)
glow = np.clip(1 - dist / 560.0, 0, 1) ** 1.6 * 0.32
for i in range(3):
    bg[..., i] = bg[..., i] + (ORANGE[i] - bg[..., i]) * glow

img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
draw = ImageDraw.Draw(img)


def font(size, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()


def center_text(d, y, text, fnt, fill, spacing=0):
    if spacing:
        widths = [d.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = (W - total) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=fnt, fill=fill)
            x += w + spacing
        return total
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return w


def diamond(d, x, y, s, col):
    d.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)], fill=col)


# ---------- TITLE ----------
f_title = font(86, True)
f_sub = font(31, True)

center_text(draw, 58, "MANUTENÇÃO", f_title, WHITE, spacing=2)
center_text(draw, 150, "RESIDENCIAL", f_title, WHITE, spacing=2)

# subtitle with side lines + diamonds
sub = "SERVIÇOS DOMÉSTICOS ESPECIALIZADOS"
sw = draw.textlength(sub, font=f_sub)
sx = (W - sw) / 2
sy = 262
draw.line([(sx - 78, sy + 16), (sx - 26, sy + 16)], fill=ORANGE, width=4)
draw.line([(sx + sw + 26, sy + 16), (sx + sw + 78, sy + 16)], fill=ORANGE, width=4)
diamond(draw, sx - 96, sy + 16, 6, ORANGE)
diamond(draw, sx + sw + 96, sy + 16, 6, ORANGE)
draw.text((sx, sy), sub, font=f_sub, fill=ORANGE_L)

# ---------- SERVICE PILLS ----------
services = ["Eletricista", "Pintor", "Montador", "Instalações"]
f_pill = font(27, True)
pad_x, gap, pill_h = 28, 20, 58
widths = [draw.textlength(s, font=f_pill) + pad_x * 2 for s in services]
total = sum(widths) + gap * (len(services) - 1)
x = (W - total) / 2
py = 332
for s, w in zip(services, widths):
    draw.rounded_rectangle([x, py, x + w, py + pill_h], radius=29, fill=CARD, outline=ORANGE, width=2)
    tw = draw.textlength(s, font=f_pill)
    draw.text((x + (w - tw) / 2, py + 13), s, font=f_pill, fill=WHITE)
    x += w + gap

# ---------- BOTTOM CARD (name + phone) ----------
bar_top, bar_bot = 438, 596
draw.rounded_rectangle([56, bar_top, W - 56, bar_bot], radius=22, fill=CARD, outline=ORANGE, width=2)

# whatsapp circle + phone glyph
wx, wy = 132, (bar_top + bar_bot) // 2
draw.ellipse([wx - 44, wy - 44, wx + 44, wy + 44], fill=WHATS)
gly = font(56, True)
gw = draw.textlength("✆", font=gly)
draw.text((wx - gw / 2, wy - 40), "✆", font=gly, fill=WHITE)

f_name = font(50, True)
f_phone = font(54, True)
tx = 210
draw.text((tx, bar_top + 30), "Douglas Santana", font=f_name, fill=WHITE)
draw.text((tx, bar_top + 90), "(11) 94897-0819", font=f_phone, fill=ORANGE_L)

img.save("og-image.png", "PNG")
print("og-image.png gerada:", img.size)
