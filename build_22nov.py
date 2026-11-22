#!/usr/bin/env python3
"""Build the news-image 22 Nov 2026 entry — v6 layout (Vicko-approved):
- Top row: 2 biggest stories side by side, equal size (EU-Indonesia CEPA
  trade deal + Iran strikes on US bases in Bahrain), each with its own
  illustration (EU flag drawn; missile-defence scene drawn).
- Grid: 8 more big panels, 4 cols x 2 rows (Lviv strike, Peru quake,
  El Chapo Isidro capture, GTA VI review-bomb, Green SM Bike ends,
  UMP 2027, Herzog taps Eisenkot, COP31 deadlock), every panel with an
  illustration (all PIL-drawn except GTA gameplay + summit flags, which
  are generic generated illustrations reused from the 21 Nov edition).
- Briefs: exactly 12 numbered items, 2 cols x 6 rows, roomy.
- Markets ticker at the very bottom (Friday 20 Nov closes — weekend,
  no fresh closes; labelled honestly).
Total: 10 big + 12 briefs = 22 stories. Every story happened, or was
first reported, on Sunday 22 November 2026.
Date-rule calls (documented): Hero 1 CEPA was signed Sat 21 Nov but
reported widely Sun 22 Nov and was NOT in the 21 Nov edition (built Sat
afternoon); Hero 2 Bahrain strikes happened Sat night, first reported
Sun ~02:00 WIB. Both qualify under the edition's "happened OR first
reported" rule, so the brief's heroes stand. Brief 1 (Guns N' Roses at
GBK) is the Sat-night concert, covered in Sun-morning reports.
Deterministic, no network.
"""
from PIL import Image, ImageDraw, ImageFont
import math

BASE = "/home/hatch/workspace/make-fun/news-image-20261122"
ASSETS = BASE + "/assets"
OUT = BASE + "/entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

NAVY = (16, 32, 64)
GOLD = (212, 160, 32)
CREAM = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
TEAL = (0, 110, 110)
ORANGE = (198, 84, 0)
SLATE = (70, 90, 120)
GREY = (90, 90, 90)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)

W = H = 1024
img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, font, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def cover_crop(src, tw, th):
    sw, sh = src.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    r = src.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return r.crop((x, y, x + tw, y + th))

def load(name):
    return Image.open(f"{ASSETS}/{name}").convert("RGB")

def fit_headline(text, max_w, max_lines, start_size):
    """Largest serif-bold size (<= start_size) wrapping to <= max_lines."""
    for size in range(start_size, 15, -1):
        f = F(SERIF, size)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines, size
    f = F(SERIF, 16)
    return f, wrap(d, text, f, max_w)[:max_lines], 16

# ---------- outer border ----------
d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=8)

# ---------- masthead ----------
d.rectangle([8, 8, W - 8, 100], fill=NAVY)
f_title = F(SERIF, 46)
t = "THE WORLD IN ONE PAGE"
tw = d.textlength(t, font=f_title)
d.text(((W - tw) / 2, 14), t, font=f_title, fill=WHITE)
f_date = F(SANS_B, 24)
t2 = "SUNDAY,  22  NOVEMBER  2026"
tw2 = d.textlength(t2, font=f_date)
d.text(((W - tw2) / 2, 66), t2, font=f_date, fill=GOLD)

f_sub = F(SERIF_R, 19)
t3 = "What the world \u2014 and the timeline \u2014 was talking about  \u2022  22 STORIES IN ONE PAGE"
tw3 = d.textlength(t3, font=f_sub)
d.text(((W - tw3) / 2, 106), t3, font=f_sub, fill=NAVY)
d.line([24, 132, W - 24, 132], fill=GOLD, width=3)

# ---------- PIL-drawn illustrations ----------
def eu_image(tw, th):
    """EU flag field: navy blue, circle of gold stars, big gold euro sign."""
    g = Image.new("RGB", (tw, th), (0, 51, 153))
    gd = ImageDraw.Draw(g)
    cx, cy = tw // 2, th // 2
    r = int(min(tw, th) * 0.32)
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        sx, sy = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        gd.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))
    f = F(SANS_B, int(th * 0.52))
    s = "\u20ac"
    sw = gd.textlength(s, font=f)
    gd.text((cx - sw / 2, cy - int(th * 0.30)), s, font=f, fill=(255, 204, 0))
    return g

def missile_image(tw, th):
    """Night air-defence scene: dark sky, stars, two missile trails with
    bright heads, interceptor arcs, ground silhouette with radar dish."""
    g = Image.new("RGB", (tw, th), (10, 16, 40))
    gd = ImageDraw.Draw(g)
    for (sx, sy, sr) in [(12, 10, 1), (30, 26, 1), (52, 8, 2), (74, 18, 1),
                         (96, 30, 1), (120, 12, 2), (142, 26, 1), (20, 44, 1),
                         (64, 40, 1), (108, 48, 1), (150, 8, 1)]:
        gd.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 210, 235))
    # missile trails: from lower-left and lower-right up to the sky
    gd.line([(8, th - 18), (70, 22)], fill=(255, 170, 60), width=3)
    gd.line([(8, th - 18), (70, 22)], fill=(255, 230, 160), width=1)
    gd.line([(tw - 8, th - 24), (96, 14)], fill=(255, 170, 60), width=3)
    gd.line([(tw - 8, th - 24), (96, 14)], fill=(255, 230, 160), width=1)
    gd.ellipse([66, 18, 76, 28], fill=(255, 240, 190))
    gd.ellipse([92, 10, 102, 20], fill=(255, 240, 190))
    # interceptor arcs (thin white curves)
    gd.arc([30, 30, 130, 110], 200, 340, fill=(180, 200, 230), width=2)
    # ground silhouette + radar dish
    gd.rectangle([0, th - 16, tw, th], fill=(6, 10, 26))
    gd.polygon([(18, th - 16), (30, th - 34), (42, th - 16)], fill=(6, 10, 26))
    gd.line([(120, th - 16), (120, th - 34)], fill=(120, 140, 180), width=3)
    gd.pieslice([108, th - 46, 132, th - 22], 180, 360, fill=(120, 140, 180))
    return g

def city_image(tw, th):
    """City skyline at dusk with a smoke plume and fire glow (strike)."""
    g = Image.new("RGB", (tw, th), (52, 38, 66))
    gd = ImageDraw.Draw(g)
    gd.rectangle([0, 0, tw, int(th * 0.45)], fill=(94, 70, 96))
    # buildings
    heights = [0.62, 0.45, 0.72, 0.52, 0.66, 0.40, 0.58]
    bw = tw // len(heights)
    for i, hf in enumerate(heights):
        x0 = i * bw + 2
        y0 = int(th * hf)
        gd.rectangle([x0, y0, x0 + bw - 4, th], fill=(24, 20, 36))
        for wy in range(y0 + 8, th - 6, 12):
            for wx in (x0 + 5, x0 + bw - 12):
                gd.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 200, 90))
    # smoke plume over the middle building
    cx = tw // 2 + 6
    for (dx, dy, r) in [(0, -6, 12), (-8, -18, 15), (6, -28, 18), (-2, -40, 14)]:
        gd.ellipse([cx + dx - r, int(th * 0.30) + dy - r,
                    cx + dx + r, int(th * 0.30) + dy + r], fill=(120, 110, 120))
    # fire glow at the roofline
    gd.ellipse([cx - 10, int(th * 0.52) - 6, cx + 10, int(th * 0.52) + 10],
               fill=(255, 120, 30))
    gd.ellipse([cx - 5, int(th * 0.52) - 2, cx + 5, int(th * 0.52) + 6],
               fill=(255, 220, 90))
    return g

def quake_image(tw, th):
    """Andes peaks with a red seismograph waveform across a dark strip."""
    g = Image.new("RGB", (tw, th), (30, 48, 74))
    gd = ImageDraw.Draw(g)
    # mountains
    gd.polygon([(0, th), (30, 18), (62, th)], fill=(58, 78, 110))
    gd.polygon([(40, th), (86, 8), (132, th)], fill=(74, 96, 130))
    gd.polygon([(110, th), (146, 22), (tw, th)], fill=(58, 78, 110))
    # snow caps
    gd.polygon([(80, 16), (86, 8), (92, 16), (88, 20), (84, 16)], fill=(235, 240, 245))
    gd.polygon([(140, 30), (146, 22), (152, 30), (148, 34), (144, 30)], fill=(235, 240, 245))
    # seismograph strip
    sy0 = int(th * 0.62)
    gd.rectangle([0, sy0, tw, th], fill=(12, 18, 32))
    pts = []
    x = 4
    amps = [2, 3, 2, 5, 3, 10, 22, 8, 16, 4, 3, 12, 6, 3, 2, 4, 2]
    mid = sy0 + (th - sy0) // 2
    for i, a in enumerate(amps):
        y = mid + (a if i % 2 == 0 else -a)
        pts.append((x, y))
        x += (tw - 8) // (len(amps) - 1)
    for a, b in zip(pts, pts[1:]):
        gd.line([a, b], fill=(231, 76, 60), width=2)
    return g

def badge_image(tw, th):
    """Gold sheriff-style star badge on navy (capture / law enforcement)."""
    g = Image.new("RGB", (tw, th), (16, 32, 64))
    gd = ImageDraw.Draw(g)
    cx, cy = tw // 2, th // 2
    ro, ri = int(min(tw, th) * 0.42), int(min(tw, th) * 0.18)
    pts = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
    gd.polygon(pts, fill=(212, 175, 55))
    gd.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=(16, 32, 64),
               outline=(212, 175, 55), width=2)
    f = F(SANS_B, int(th * 0.20))
    s = "$"
    sw = gd.textlength(s, font=f)
    gd.text((cx - sw / 2, cy - int(th * 0.11)), s, font=f, fill=(212, 175, 55))
    return g

def bike_image(tw, th):
    """Electric scooter silhouette with a lightning bolt (e-bike service)."""
    g = Image.new("RGB", (tw, th), (0, 90, 90))
    gd = ImageDraw.Draw(g)
    # ground line
    gd.line([(8, th - 18), (tw - 8, th - 18)], fill=(180, 230, 230), width=2)
    # wheels
    for wx in (34, tw - 40):
        gd.ellipse([wx - 13, th - 31, wx + 13, th - 5], outline=(235, 245, 245), width=3)
        gd.ellipse([wx - 3, th - 21, wx + 3, th - 15], fill=(235, 245, 245))
    # deck + stem + handlebar
    gd.line([(34, th - 22), (tw - 40, th - 22)], fill=(235, 245, 245), width=4)
    gd.line([(tw - 52, th - 22), (tw - 44, 22)], fill=(235, 245, 245), width=4)
    gd.line([(tw - 56, 22), (tw - 32, 22)], fill=(235, 245, 245), width=4)
    # seat post
    gd.line([(52, th - 22), (56, th - 44)], fill=(235, 245, 245), width=4)
    gd.line([(44, th - 44), (68, th - 44)], fill=(235, 245, 245), width=4)
    # lightning bolt
    bx, by = tw // 2 - 6, 12
    gd.polygon([(bx + 12, by), (bx - 2, by + 22), (bx + 6, by + 22),
                (bx - 4, by + 44), (bx + 14, by + 18), (bx + 6, by + 18)],
               fill=(255, 220, 60))
    return g

def rupiah_image(tw, th):
    """Green banknote field: big 'Rp' and gold coins (wages)."""
    g = Image.new("RGB", (tw, th), (0, 96, 52))
    gd = ImageDraw.Draw(g)
    gd.rectangle([6, 6, tw - 6, th - 6], outline=(212, 175, 55), width=2)
    f = F(SANS_B, int(th * 0.44))
    s = "Rp"
    sw = gd.textlength(s, font=f)
    gd.text(((tw - sw) / 2 - 18, int(th * 0.10)), s, font=f, fill=(255, 255, 255))
    for (cx, cy, r) in [(tw - 34, th - 26, 13), (30, th - 24, 11), (tw - 58, 20, 9)]:
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(212, 175, 55),
                   outline=(160, 120, 20), width=2)
        gd.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4],
                   outline=(160, 120, 20), width=1)
    return g

def israel_image(tw, th):
    """Israeli flag: white field, two blue stripes, Star of David."""
    g = Image.new("RGB", (tw, th), (255, 255, 255))
    gd = ImageDraw.Draw(g)
    stripe = int(th * 0.16)
    gd.rectangle([0, int(th * 0.14), tw, int(th * 0.14) + stripe], fill=(0, 56, 184))
    gd.rectangle([0, int(th * 0.70), tw, int(th * 0.70) + stripe], fill=(0, 56, 184))
    cx, cy = tw // 2, th // 2
    r = int(min(tw, th) * 0.26)
    def tri(up):
        pts = []
        for i in range(3):
            a = (-math.pi / 2 if up else math.pi / 2) + i * 2 * math.pi / 3
            pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
        return pts
    gd.polygon(tri(True), outline=(0, 56, 184), width=3)
    gd.polygon(tri(False), outline=(0, 56, 184), width=3)
    return g

# ---------- top row: 2 biggest panels ----------
TOP_Y, TOP_H, TOP_W = 140, 212, 478
TOP_X = [24, 522]

top_panels = [
    dict(kick="TRADE  \u2022  EU\u2013INDONESIA  \u2014  SIGNED SAT", kcol=NAVY,
         head="EU\u2013INDONESIA SEAL LANDMARK TRADE DEAL",
         body=("CEPA signed in Brussels after ~10 years of talks: up to "
               "98.5% of tariff lines liberalised; car tariffs up to 50% "
               "phased out in 5 years."),
         quote=("\u201c~ \u20ac600\u2013650m/yr duty savings; trade ~US$30bn/yr; "
                "provisional application early 2027.\u201d"),
         pic="EU_DRAWN"),
    dict(kick="CONFLICT  \u2022  BAHRAIN  \u2014  REPORTED 02:00", kcol=RED,
         head="IRAN HITS US BASES IN BAHRAIN",
         body=("IRGC missile + drone strikes target US Patriot radars at "
               "al-Riffa and Awali; Bahrain says several were intercepted; "
               "a civilian facility was hit."),
         quote=("\u201cAt least 3 tankers hit near the Strait of Hormuz; "
                "4th attack on Bahrain in 9 days.\u201d"),
         pic="MISSILE_DRAWN"),
]
for (x0, p) in zip(TOP_X, top_panels):
    x1, y0, y1 = x0 + TOP_W, TOP_Y, TOP_Y + TOP_H
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=2, fill=WHITE)
    d.rectangle([x0, y0, x0 + 8, y1], fill=p["kcol"])
    tx = x0 + 20
    f_k = F(SANS_B, 13)
    d.text((tx, y0 + 9), p["kick"], font=f_k, fill=p["kcol"])
    pw, ph = 160, 168
    px, py = x1 - 8 - pw, y0 + 34
    if p["pic"] == "EU_DRAWN":
        ph_img = eu_image(pw, ph)
    elif p["pic"] == "MISSILE_DRAWN":
        ph_img = missile_image(pw, ph)
    else:
        ph_img = cover_crop(load(p["pic"]), pw, ph)
    img.paste(ph_img, (px, py))
    d.rectangle([px, py, px + pw, py + ph], outline=NAVY, width=2)
    text_w = px - 12 - tx
    f_h, hlines, _ = fit_headline(p["head"], text_w, 2, 26)
    y = draw_lines(d, hlines, tx, y0 + 30, f_h, INK, 29)
    f_b = F(SANS, 13)
    blines = wrap(d, p["body"], f_b, text_w)
    if len(blines) > 4:
        print("WARNING top body wraps to", len(blines), "lines:", p["head"])
        blines = blines[:4]
    y = draw_lines(d, blines, tx, y + 4, f_b, (40, 40, 40), 17)
    if p["quote"]:
        f_q = F(SERIF_I, 12)
        qlines = wrap(d, p["quote"], f_q, text_w)
        if len(qlines) > 2:
            print("WARNING quote wraps to", len(qlines), "lines")
            qlines = qlines[:2]
        draw_lines(d, qlines, tx, y + 4, f_q, (90, 30, 30), 16)
    if y > y1 - 8:
        print("WARNING top panel overflow:", p["head"], "y =", y, "bottom =", y1)

# ---------- grid: 8 more big panels, 4 cols x 2 rows ----------
GRID_Y = [360, 568]
GRID_H = 200
GRID_X = [24, 270, 516, 762]
GRID_W = 238
GTA_IMG = "media-generation-gta-vi-gameplay-vice-city-0-6fe41c38-2e55-4b68-b67a-04c75814b912.webp"
SUMMIT_IMG = "media-generation-summit-flags-0-210436bd-4fd7-4bb6-8afc-493c47774b2a.png"

grid_panels = [
    dict(kick="WAR IN UKRAINE  \u2022  LVIV", kcol=RED,
         head="RUSSIAN STRIKE HITS LVIV",
         body=("Missile hits a building: 2 killed, 10 injured; 2 more die "
               "in Kryvyi Rih. Poland reports airspace incursions."),
         pic="CITY_DRAWN"),
    dict(kick="DISASTER  \u2022  PERU", kcol=RED,
         head="6.7 QUAKE SHAKES PERU'S ANDES",
         body=("Strong quake strikes the Andes; no damage or casualties "
               "reported at the time."),
         pic="QUAKE_DRAWN"),
    dict(kick="CRIME  \u2022  MEXICO", kcol=NAVY,
         head="MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         body=("Fausto Isidro Meza Flores, among the FBI's most-wanted, "
               "is captured by the Mexican army."),
         pic="BADGE_DRAWN"),
    dict(kick="GAMING  \u2022  METACRITIC", kcol=ORANGE,
         head="GTA VI REVIEW-BOMBED: 99 vs 5.6",
         body=("Critics give Metascore 99; users score it 5.6 on "
               "Metacritic \u2014 a split verdict on the biggest launch ever."),
         pic=GTA_IMG),
    dict(kick="INDONESIA  \u2022  TRANSPORT", kcol=TEAL,
         head="GREEN SM BIKE STOPS RUNNING",
         body=("Electric motorbike service ends 20 Nov; refunds arranged "
               "for customer balances and partner units."),
         pic="BIKE_DRAWN"),
    dict(kick="INDONESIA  \u2022  WAGES", kcol=TEAL,
         head="UMP 2027 SET IN 22 PROVINCES",
         body=("Jakarta highest at Rp6,136,941; Bali up 42.15%, the "
               "biggest rise; NTT lowest at Rp2,602,441."),
         pic="RUPIAH_DRAWN"),
    dict(kick="ISRAEL  \u2022  POLITICS", kcol=NAVY,
         head="HERZOG TAPS EISENKOT FOR GOVERNMENT",
         body=("President Herzog asks ex-army chief Eisenkot to form the "
               "next government, bypassing Netanyahu."),
         pic="ISRAEL_DRAWN"),
    dict(kick="CLIMATE  \u2022  ANTALYA", kcol=TEAL,
         head="COP31 DEADLOCKED ON FOSSIL FUELS",
         body=("Climate talks stuck on the fossil-fuel future and "
               "international financing ahead of conclusion."),
         pic=SUMMIT_IMG),
]
for idx, p in enumerate(grid_panels):
    x0 = GRID_X[idx % 4]
    y0 = GRID_Y[idx // 4]
    x1, y1 = x0 + GRID_W, y0 + GRID_H
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=2, fill=WHITE)
    d.rectangle([x0, y0, x1, y0 + 5], fill=p["kcol"])
    pw, ph = GRID_W - 4, 88
    px, py = x0 + 2, y0 + 7
    if p["pic"] == "CITY_DRAWN":
        ph_img = city_image(pw, ph)
    elif p["pic"] == "QUAKE_DRAWN":
        ph_img = quake_image(pw, ph)
    elif p["pic"] == "BADGE_DRAWN":
        ph_img = badge_image(pw, ph)
    elif p["pic"] == "BIKE_DRAWN":
        ph_img = bike_image(pw, ph)
    elif p["pic"] == "RUPIAH_DRAWN":
        ph_img = rupiah_image(pw, ph)
    elif p["pic"] == "ISRAEL_DRAWN":
        ph_img = israel_image(pw, ph)
    else:
        ph_img = cover_crop(load(p["pic"]), pw, ph)
    img.paste(ph_img, (px, py))
    d.rectangle([px, py, px + pw, py + ph], outline=NAVY, width=2)
    tx = x0 + 10
    text_w = GRID_W - 20
    f_k = F(SANS_B, 11)
    d.text((tx, y0 + 100), p["kick"], font=f_k, fill=p["kcol"])
    f_h, hlines, _ = fit_headline(p["head"], text_w, 2, 18)
    y = draw_lines(d, hlines, tx, y0 + 114, f_h, INK, 18)
    f_b = F(SANS, 12)
    blines = wrap(d, p["body"], f_b, text_w)
    if len(blines) > 3:
        print("WARNING grid body wraps to", len(blines), "lines:", p["head"], blines)
        blines = blines[:3]
    y = draw_lines(d, blines, tx, y + 2, f_b, (40, 40, 40), 14)
    if y > y1 - 6:
        print("WARNING grid panel overflow:", p["head"], "y =", y, "bottom =", y1)

# ---------- briefs: exactly 12, 2 cols x 6 rows ----------
B_Y0, B_Y1 = 786, 938
d.rectangle([24, B_Y0, 1000, B_Y1], outline=NAVY, width=2)
f_h = F(SANS_B, 15)
d.text((36, B_Y0 + 8), "MORE IN BRIEF \u2014 22 NOV", font=f_h, fill=NAVY)
f_src = F(SANS, 10)
src = ("Sources: Reuters \u2022 AP \u2022 Al Jazeera \u2022 ANI \u2022 ANTARA "
       "\u2022 industry.co.id \u2022 beritanasional.com \u2014 22 Nov 2026")
sw = d.textlength(src, font=f_src)
d.text((988 - sw, B_Y0 + 11), src, font=f_src, fill=GREY)
d.line([36, B_Y0 + 30, 988, B_Y0 + 30], fill=GOLD, width=2)

BRIEFS = [
    "Guns N' Roses at GBK; MRT & Transjakarta ran late",
    "KA Siantar Ekspres hits minibus; loco on fire \u2014 Simalungun",
    "France: 4th weekend of cost-of-living protests \u2014 France",
    "Australia, Canada, Italy, UK urge aid into flooded Gaza",
    "Hong Kong Election Committee voting begins \u2014 Hong Kong",
    "FBI probes suspected breach of crime database \u2014 USA",
    "Nataru toll discount min 30% set for Java & Sumatra",
    "UMK Bekasi 2027 Rp6.48mn \u2014 highest in Indonesia",
    "DPR: banks must boost digital sovereignty + AI risk",
    "IMOS 2026: Honda shows new Super Cub, Vario Evo, ADV 160",
    "Myanmar quake 4.1 early Sunday morning \u2014 Myanmar",
    "Sudan: Tasis Alliance seizes Blue Nile's Bau region \u2014 Sudan",
]
f_num = F(SANS_B, 13)
f_txt = F(SANS, 13)
COL_X = [36, 516]
ROW_Y = [B_Y0 + 38, B_Y0 + 57, B_Y0 + 76, B_Y0 + 95, B_Y0 + 114, B_Y0 + 133]
for i, item in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    x0, y0 = COL_X[col], ROW_Y[row]
    num = f"{i + 1}."
    nw = d.textlength(num, font=f_num)
    if d.textlength(item, font=f_txt) > 460 - nw - 6:
        print("WARNING brief too long for one line:", i + 1, item)
    d.text((x0, y0), num, font=f_num, fill=NAVY)
    d.text((x0 + nw + 6, y0), item, font=f_txt, fill=INK)
    if col == 0:
        d.line([500, y0 + 2, 500, y0 + 15], fill=(200, 200, 190), width=1)

# ---------- markets ticker strip: 946..1014 ----------
d.rectangle([24, 946, 1000, 1014], outline=NAVY, width=2)
f_lab = F(SANS_B, 10)
d.text((36, 950), "MARKETS \u2014 22 NOV", font=f_lab, fill=NAVY)
f_note = F(SANS, 8)
note = "Fri 20 Nov close, reported 22 Nov"
nw_note = d.textlength(note, font=f_note)
d.text((988 - nw_note, 952), note, font=f_note, fill=GREY)

TICKER = [
    ("S&P 500", "6,910.39", "\u25bc", "-3.70%", RED),
    ("Dow Jones", "48,147.33", "\u25bc", "-1.93%", RED),
    ("Nasdaq", "22,617.73", "\u25bc", "-5.28%", RED),
    ("FTSE 100", "10,346.34", "\u25bc", "-1.02%", RED),
    ("DAX", "24,802.78", "\u25bc", "-2.60%", RED),
    ("Nikkei 225", "56,436.65", "\u25bc", "-5.06%", RED),
    ("Hang Seng", "22,410.80", "\u25bc", "-1.89%", RED),
    ("Kospi", "4,869.96", "\u25bc", "-5.21%", RED),
    ("Shanghai", "3,533.79", "\u25bc", "-1.22%", RED),
    ("ASX 200", "8,592.60", "\u25bc", "-1.58%", RED),
    ("Gold", "$3,515", "\u25bc", "-3%", RED),
    ("Brent", "$92.57", "\u25b2", "+0.64%", GREEN),
    ("Bitcoin", "~$58,831", "\u25bc", "-5.1%", RED),
    ("VIX", "35.89", "\u25b2", "+26%", RED),
]
ROWS = [TICKER[:7], TICKER[7:]]

def row_width(items, f_reg, f_b):
    w = 0
    for name, price, arrow, chg, _ in items:
        w += d.textlength(f"{name} {price} ", font=f_reg)
        w += d.textlength(f"{arrow} {chg}" if chg else arrow, font=f_b)
        w += 14
    return w - 14

for size in (9, 8.5, 8):
    f_reg = F(SANS, size)
    f_b = F(SANS_B, size)
    if all(row_width(r, f_reg, f_b) <= 952 for r in ROWS):
        break
print("ticker font size:", size)
for ri, items in enumerate(ROWS):
    y = 964 + ri * 12
    total = row_width(items, f_reg, f_b)
    x = 36 + (952 - total) / 2
    for name, price, arrow, chg, col in items:
        s1 = f"{name} {price} "
        d.text((x, y), s1, font=f_reg, fill=INK)
        x += d.textlength(s1, font=f_reg)
        s2 = f"{arrow} {chg}" if chg else arrow
        d.text((x, y), s2, font=f_b, fill=col)
        x += d.textlength(s2, font=f_b) + 14

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
