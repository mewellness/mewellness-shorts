"""Build 1080x1080 branded Airofit campaign images (Nov 2026)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
S = 1080
MINT = (94, 242, 208); WHITE = (255, 255, 255); INK = (10, 10, 10)
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
badge = Image.open(os.path.join(HERE, "badge.png"))

def square(img, focus_x=0.5):
    img = img.convert("RGB"); w, h = img.size
    if w > h:
        s = h; x = int((w - s) * focus_x); img = img.crop((x, 0, x + s, s))
    elif h > w:
        s = w; img = img.crop((0, 0, s, s))
    return img.resize((S, S), Image.LANCZOS)

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def inset(img, size=740, top=128):
    img = img.convert("RGB")
    bg = Image.new("RGB", (S, S), img.getpixel((5, 5)))
    img.thumbnail((size, size), Image.LANCZOS)
    bg.paste(img, ((S - img.width) // 2, top))
    return bg

INSET = {"elite_app.jpg", "core_hero.jpg", "elite_lungtest.jpg", "elite_apphome.png", "core_grey.jpg"}

def build(src, out, headline, sub, pill, focus_x=0.5):
    raw = Image.open(os.path.join(HERE, "src", src))
    im = inset(raw, 600, 120) if src == "elite_lungtest.jpg" else inset(raw) if src in INSET else square(raw, focus_x)
    # bottom gradient
    g = Image.new("L", (1, S))
    for y in range(S):
        g.putpixel((0, y), int(max(0, (y - S * 0.45) / (S * 0.55)) ** 1.3 * 235))
    shade = Image.new("RGB", (S, S), INK)
    im = Image.composite(shade, im, g.resize((S, S)))
    d = ImageDraw.Draw(im)
    # pill top-left
    fp = ImageFont.truetype(FB, 30)
    tw = d.textlength(pill, font=fp)
    d.rounded_rectangle((48, 48, 48 + tw + 52, 48 + 66), radius=33, fill=MINT)
    d.text((48 + 26, 48 + 33), pill, font=fp, fill=INK, anchor="lm")
    # badge bottom-right (same position as existing posts)
    im.paste(badge, (804, 876), badge)
    # headline + sub bottom-left, kept clear of badge
    fh = ImageFont.truetype(FB, 62); fs = ImageFont.truetype(FM, 34)
    hl = wrap(d, headline, fh, 700); sl = wrap(d, sub, fs, 700) if sub else []
    y = S - 72 - len(sl) * 46 - len(hl) * 72 - (16 if sl else 0)
    for line in hl:
        d.text((60, y), line, font=fh, fill=WHITE); y += 72
    y += 16
    for line in sl:
        d.text((60, y), line, font=fs, fill=(225, 235, 232)); y += 46
    im.save(os.path.join(HERE, "posts", out), quality=90)

os.makedirs(os.path.join(HERE, "posts"), exist_ok=True)
OFFER = "5% OFF · CODE AIROFIT5"
POSTS = [
 ("elite_hand.jpg", "01-launch.jpg", "Train the muscles most people ignore", "Airofit ELITE $486 · CORE $259", OFFER),
 ("core_photo_1.jpg", "02-core.jpg", "New: Airofit CORE", "No charging. No Bluetooth. $259", OFFER),
 ("elite_session.jpg", "03-diaphragm.jpg", "Your diaphragm is a muscle", "Train it in about 10 minutes a day", OFFER),
 ("elite_gym.jpg", "04-research.jpg", "What 46 studies found", "Breathing training and endurance", OFFER),
 ("elite_app.jpg", "05a-elite.jpg", "ELITE: measure every breath", "Live feedback + lung tests · $486", OFFER),
 ("core_hero.jpg", "05b-core.jpg", "CORE: just breathe", "App-guided, no charging · $259", OFFER),
 ("elite_lungtest.jpg", "06-progress.jpg", "See your progress", "Lung capacity and breath strength, with ELITE", OFFER),
 ("core_photo_3.jpg", "07-ten-minutes.jpg", "10 minutes. Sitting down.", "For runners, cyclists, swimmers and you", OFFER),
 ("core_photo_2.jpg", "08-gift.jpg", "The gift for the runner who has everything", "Airofit CORE $259 · ELITE $486", OFFER),
 ("core_grey.jpg", "09-four-days.jpg", "4 days left", "5% off Airofit ELITE and CORE", "ENDS 24 NOV · CODE AIROFIT5"),
 ("elite_apphome.png", "10-last-chance.jpg", "Last chance", "5% off ends tomorrow", "ENDS 24 NOV · CODE AIROFIT5"),
 ("elite_gym.jpg", "b1-clubs.jpg", "Training a squad?", "Team pricing on 5+ Airofit trainers", "CLUBS · GYMS · COACHES"),
]
for p in POSTS: build(*p)
print("built", len(POSTS))
