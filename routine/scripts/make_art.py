import math
from PIL import Image, ImageDraw, ImageFont
F = '/home/user/box/routine/fonts/'
S = 2  # supersample
W, H = 2400, 3200
BG, INK, TEAL, SUN, MUTED = '#e9edf1', '#1e2d5a', '#3f7f86', '#f0a202', '#8a95a8'
img = Image.new('RGB', (W*S, H*S), BG)
d = ImageDraw.Draw(img)
cx, cy = 1200*S, 1360*S

K = 0.9
def pt(r, hour):
    r = r*K
    a = math.radians(hour/24*360 - 90)
    return cx + r*math.cos(a), cy + r*math.sin(a)

def circle(r, w, col):
    r = r*K
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=col, width=max(1, int(w)))

# concentric orbits, gaps widen outward
radii = [120, 190, 280, 400, 560, 760, 980]
for i, r in enumerate(radii):
    circle(r*S, (1.6 if i % 2 else 2.4)*S, INK if i in (3, 6) else MUTED)

# outer tick ring: 96 ticks (15 min)
R0 = 1020*S
for k in range(96):
    h = k/4
    L = 70 if k % 24 == 0 else (38 if k % 4 == 0 else 16)
    w = 4 if k % 24 == 0 else (2.4 if k % 4 == 0 else 1.4)
    x1, y1 = pt(R0, h); x2, y2 = pt(R0 + L*S, h)
    d.line([x1, y1, x2, y2], fill=INK if k % 4 == 0 else MUTED, width=int(w*S))

# elapsed arc on orbit 760 (06:00 -> 14:20)
now = 14 + 20/60
r = 760*S*K
start, end = 6/24*360 - 90, now/24*360 - 90
d.arc([cx-r, cy-r, cx+r, cy+r], start, end, fill=SUN, width=14*S)

# routine markers on orbit 560
routines = [6.5, 7.0, 8.5, 12.5, 18.0, 21.5, 22.5]
for t in routines:
    x, y = pt(560*S, t); rr = 22*S
    if t < now:
        d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=SUN)
    else:
        d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=BG, outline=INK, width=4*S)
    # faint radial spoke from orbit 400 to marker
    x0, y0 = pt(400*S, t); x1, y1 = pt(538*S, t)
    d.line([x0, y0, x1, y1], fill=MUTED, width=int(1.4*S))

# 24 hour dots on orbit 280
for hh in range(24):
    x, y = pt(280*S, hh); rr = (7 if hh % 6 == 0 else 4)*S
    d.ellipse([x-rr, y-rr, x+rr, y+rr], fill=INK if hh % 6 == 0 else MUTED)

# current-time hand + dot
x1, y1 = pt(980*S, now)
d.line([cx, cy, x1, y1], fill=INK, width=3*S)
rr = 14*S; d.ellipse([x1-rr, y1-rr, x1+rr, y1+rr], fill=SUN)
rr = 9*S; d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=INK)

# hour labels
lab = ImageFont.truetype(F+'noto-sans-kr-latin-300-normal.woff', 34*S)
for hh in (0, 6, 12, 18):
    x, y = pt(1160*S, hh)
    t = f'{hh:02d}'
    b = d.textbbox((0, 0), t, font=lab)
    d.text((x-(b[2]+b[0])/2, y-(b[3]+b[1])/2), t, font=lab, fill=INK)

# typography (bottom-left, quiet)
title = ImageFont.truetype(F+'gowun-batang-korean-400-normal.woff', 112*S)
small = ImageFont.truetype(F+'noto-sans-kr-korean-300-normal.woff', 36*S)
smallL = ImageFont.truetype(F+'noto-sans-kr-latin-300-normal.woff', 36*S)
mx = 200*S
d.text((mx, 2620*S), '궤도의 정적', font=title, fill=INK)
d.line([mx, 2800*S, mx+120*S, 2800*S], fill=SUN, width=5*S)
d.text((mx, 2850*S), '같은 자리를 다시 지나는 하루', font=small, fill=TEAL)
# right-bottom coordinates
txt = '7 / 4 / 14:20'
b = d.textbbox((0, 0), txt, font=smallL)
d.text((W*S-mx-b[2], 2850*S), txt, font=smallL, fill=MUTED)

img = img.resize((W, H), Image.LANCZOS)
img.save('/home/user/box/routine/art/orbital-stillness.png', optimize=True)
img.resize((W//2, H//2), Image.LANCZOS).save('/tmp/claude-0/-home-user/c6c987c8-c7e9-56a9-8898-465c850985b2/scratchpad/art_preview.png')
