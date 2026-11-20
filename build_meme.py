#!/usr/bin/env python3
"""GTA 6 meme for make.fun gta6-meme-x-01 — 'GTA FLU' sick-day meme.

Handmade vector PIL, 1080x1080. Concept: the make.fun ghost caught the
'GTA Flu' — calling in sick for GTA 6 launch day. Vice City sunset,
ghost as sick patient (thermometer + ice pack), holding its magenta coin.
Judge criteria addressed: ghost recognisable & worked into scene (#1),
real GTA-fan joke (#2), GTA-6-specific details 212 GB / 13 years /
midnight unlock (#3), make.fun name in-image (#1/#4), short & readable (#5),
original (#6), clean image (#7).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
OUT = "/home/hatch/workspace/makefun-2026-11-16/gta6-meme-x-01-entry/meme_v3.png"

FONT_COND_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# ---------- Vice City sunset gradient ----------
stops = [
    (0, (34, 9, 63)),      # deep purple
    (340, (142, 30, 99)),  # magenta-purple
    (620, (214, 51, 108)), # pink-red
    (860, (255, 122, 61)), # orange
    (1080, (255, 179, 71)),# warm amber
]
for y in range(H):
    for i in range(len(stops) - 1):
        y0, c0 = stops[i]
        y1, c1 = stops[i + 1]
        if y0 <= y <= y1:
            t = (y - y0) / max(1, y1 - y0)
            col = tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
            break
    else:
        col = stops[-1][1]
    d.line([(0, y), (W, y)], fill=col)

# ---------- sun + halo rings behind ghost ----------
CX, SUN_Y = 540, 470
d.ellipse([CX - 300, SUN_Y - 300, CX + 300, SUN_Y + 300], fill=(255, 158, 94))
d.ellipse([CX - 265, SUN_Y - 265, CX + 265, SUN_Y + 265], fill=(255, 196, 107))
d.ellipse([CX - 225, SUN_Y - 225, CX + 225, SUN_Y + 225], fill=(255, 243, 176))

# ---------- palm silhouettes (dark purple) ----------
PALM = (42, 10, 62)

def bezier(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    return (x, y)

def frond(crown, tip, lift, base_w=26):
    """One drooping palm blade: tapered strip along a quadratic curve."""
    ctrl = ((crown[0] + tip[0]) / 2 + lift[0], (crown[1] + tip[1]) / 2 + lift[1])
    left, right = [], []
    for i in range(13):
        t = i / 12
        cx, cy = bezier(crown, ctrl, tip, t)
        # tangent for perpendicular
        tx = 2 * (1 - t) * (ctrl[0] - crown[0]) + 2 * t * (tip[0] - ctrl[0])
        ty = 2 * (1 - t) * (ctrl[1] - crown[1]) + 2 * t * (tip[1] - ctrl[1])
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = base_w * (1 - t) ** 0.8
        left.append((cx + nx * w, cy + ny * w))
        right.append((cx - nx * w, cy - ny * w))
    d.polygon(left + right[::-1], fill=PALM)

def palm(base_x, base_y, top_x, top_y, flip):
    """Curved trunk + 6 drooping fronds."""
    pts = []
    for i in range(9):
        t = i / 8
        x = base_x + (top_x - base_x) * t
        y = base_y + (top_y - base_y) * t
        x += math.sin(t * 1.2) * (14 if flip else -14) * t
        pts.append((x, y))
    d.line(pts, fill=PALM, width=26, joint="curve")
    crown = (top_x, top_y)
    s = -1 if flip else 1
    for dx, dy, lift in [
        (-190, -40, (0, -70)), (-170, 30, (-30, -50)), (-120, 90, (-40, -20)),
        (-40, 120, (-20, 10)), (50, 110, (20, 0)), (130, 70, (40, -30)),
        (185, 0, (30, -60)),
    ]:
        tip = (crown[0] + dx * s, crown[1] + dy)
        frond(crown, tip, (lift[0] * s, lift[1]))

palm(70, 1080, 150, 690, flip=False)
palm(1010, 1080, 930, 700, flip=True)

# ---------- birds ----------
for bx, by, s in [(330, 250, 16), (700, 210, 13), (770, 280, 11)]:
    d.line([(bx - s, by), (bx, by + s * 0.6), (bx + s, by)], fill=(60, 16, 80), width=4, joint="curve")

# ---------- make.fun ghost ----------
def arc_pts(cx, cy, r, a0, a1, step=2):
    pts = []
    a = a0
    while a <= a1:
        rad = math.radians(a)
        pts.append((cx + r * math.cos(rad), cy + r * math.sin(rad)))
        a += step
    return pts

# ghost outline path (screen coords, y down): left side up, dome over, right side down, 3 scallops
path = []
path.append((310, 700))
path.append((310, 410))
path += arc_pts(540, 410, 230, 180, 360)   # dome
path.append((770, 410))
path.append((770, 700))
path += arc_pts(693, 700, 77, 0, 180)      # scallop 1
path += arc_pts(540, 700, 77, 0, 180)      # scallop 2
path += arc_pts(387, 700, 77, 0, 180)      # scallop 3

# thick black outline: black polygon, then white inset polygon
d.polygon(path, fill=(0, 0, 0))
centroid = (540, 490)
inset = []
for (x, y) in path:
    dx, dy = x - centroid[0], y - centroid[1]
    L = math.hypot(dx, dy) or 1
    inset.append((x - dx / L * 13, y - dy / L * 13))
d.polygon(inset, fill=(255, 255, 255))

def sparkle(cx, cy, outer, inner):
    pts = []
    for i in range(8):
        a = math.radians(-90 + i * 45)
        r = outer if i % 2 == 0 else inner
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

# sparkle eyes
d.polygon(sparkle(452, 425, 36, 13), fill=(0, 0, 0))
d.polygon(sparkle(628, 425, 36, 13), fill=(0, 0, 0))

# sick "o" mouth
d.ellipse([522, 502, 558, 536], fill=(0, 0, 0))

# thermometer: white shaft with red line + red bulb, angled out of mouth
def rot_rect(cx, cy, length, width, ang_deg):
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    hl, hw = length / 2, width / 2
    return [
        (cx - ux * hl - px * hw, cy - uy * hl - py * hw),
        (cx + ux * hl - px * hw, cy + uy * hl - py * hw),
        (cx + ux * hl + px * hw, cy + uy * hl + py * hw),
        (cx - ux * hl + px * hw, cy - uy * hl + py * hw),
    ]

shaft = rot_rect(600, 570, 120, 26, 35)
d.polygon(shaft, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
d.line([(552, 528), (632, 592)], fill=(230, 40, 60), width=8)
d.ellipse([623, 581, 657, 615], fill=(230, 40, 60), outline=(0, 0, 0), width=3)

# sweat drop
d.polygon([(715, 318), (700, 352), (730, 352)], fill=(127, 200, 232))
d.ellipse([699, 340, 731, 372], fill=(127, 200, 232), outline=(0, 0, 0), width=3)

# ice pack on head (own layer, rotated)
pack = Image.new("RGBA", (300, 170), (0, 0, 0, 0))
pd = ImageDraw.Draw(pack)
pd.rounded_rectangle([20, 35, 280, 135], radius=28, fill=(191, 227, 240, 255), outline=(0, 0, 0, 255), width=5)
pd.rectangle([140, 55, 160, 115], fill=(255, 255, 255, 255))
pd.rectangle([110, 75, 190, 95], fill=(255, 255, 255, 255))
pack = pack.rotate(-18, expand=True, resample=Image.BICUBIC)
img.paste(pack, (300, 96), pack)
d = ImageDraw.Draw(img)  # refresh draw after paste

# little round hand + magenta coin with white star
d.ellipse([732, 610, 792, 670], fill=(255, 255, 255), outline=(0, 0, 0), width=5)
d.ellipse([766, 566, 842, 642], fill=(230, 0, 126), outline=(0, 0, 0), width=5)

def star(cx, cy, outer, inner, rot=-90):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36)
        r = outer if i % 2 == 0 else inner
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

d.polygon(star(804, 604, 26, 11), fill=(255, 255, 255))

# ---------- captions ----------
def text_center(y, s, font, fill, stroke, stroke_w):
    bbox = d.textbbox((0, 0), s, font=font)
    w = bbox[2] - bbox[0]
    d.text((540 - w / 2 - bbox[0], y), s, font=font, fill=fill,
           stroke_width=stroke_w, stroke_fill=stroke)

f_top = ImageFont.truetype(FONT_COND_BOLD, 66)
f_sub = ImageFont.truetype(FONT_COND_BOLD, 30)
f_big = ImageFont.truetype(FONT_COND_BOLD, 138)
f_pill = ImageFont.truetype(FONT_BOLD, 46)

text_center(38, "SORRY BOSS, I CAUGHT THE", f_top, (255, 255, 255), (0, 0, 0), 6)
text_center(122, "212 GB \u2022 13 YEARS OF WAITING \u2022 MIDNIGHT UNLOCK",
            f_sub, (255, 217, 61), (0, 0, 0), 3)
# v2: GTA FLU dikecilin (160 -> 138); diukur dari pixel: huruf putih
# mulai y+48 dan berakhir y+148, jadi y=767 bikin jaraknya seimbang —
# hantu (bawah 765) -> GTA FLU ~50px -> pil (atas 966) ~50px -> bawah 48px
text_center(767, "GTA FLU", f_big, (255, 255, 255), (0, 0, 0), 9)

# make.fun pill — v2: jarak dari GTA FLU dilebarin, bawah disisain 48px
d.rounded_rectangle([380, 966, 700, 1032], radius=33, fill=(230, 0, 126),
                    outline=(255, 255, 255), width=3)
# v3 FIX: teks di pil ternyata TIDAK di tengah vertikal — textbbox
# "make.fun" = (0,14,220,50), jadi anchor y=976 bikin tinta 990-1026,
# tengah 1008 vs tengah pil 999 (turun 9px, margin atas 24 / bawah 6).
# Anchor yang benar: 999 - (14+50)/2 = 967 -> tinta 981-1017, margin 15/15.
text_center(967, "make.fun", f_pill, (255, 255, 255), (0, 0, 0), 0)

img.save(OUT, "PNG")
# 480px legibility preview (judge shrinks square to 480x480)
img.resize((480, 480), Image.LANCZOS).save(
    "/home/hatch/workspace/makefun-2026-11-16/gta6-meme-x-01-entry/meme_480_v3.png", "PNG")
print("saved", OUT)
