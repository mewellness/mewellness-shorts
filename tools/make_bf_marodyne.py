"""Black Friday 2026 Marodyne LiV social assets: 4:5 feed image, 9:16 story image, 9:16 silent video."""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else D
PHOTO = os.path.join(D, "7456788-file-4591607381511854168.jpeg")
PB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
PSB = "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
PM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
for p in (PSB, PM):
    if not os.path.exists(p):
        PSB = PM = PB
GOLD = (232, 197, 71)
WHITE = (255, 255, 255)
MUTED = (175, 196, 188)
BG = (10, 10, 10)


def f(path, size):
    return ImageFont.truetype(path, size)


def bg(w, h):
    """Black base with deep green radial glow top-right and a soft gold glow."""
    img = Image.new("RGB", (w, h), BG)
    glow = Image.new("RGB", (w, h), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse((int(w * 0.25), -int(h * 0.35), int(w * 1.6), int(h * 0.55)), fill=(31, 91, 74))
    g.ellipse((-int(w * 0.5), int(h * 0.55), int(w * 0.6), int(h * 1.3)), fill=(20, 51, 43))
    glow = glow.filter(ImageFilter.GaussianBlur(w // 5))
    img = Image.blend(img, glow, 0.85)
    gold = Image.new("RGB", (w, h), (0, 0, 0))
    ImageDraw.Draw(gold).ellipse((int(w * 0.72), -int(w * 0.12), int(w * 1.12), int(w * 0.28)), fill=(60, 48, 16))
    gold = gold.filter(ImageFilter.GaussianBlur(w // 10))
    return Image.fromarray(__import__("numpy").clip(__import__("numpy").asarray(img, "int16") + __import__("numpy").asarray(gold, "int16"), 0, 255).astype("uint8"))


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), m)
    return out


def pill(d, x, y, text, size=30):
    ft = f(PB, size)
    tw = d.textlength(text, font=ft)
    pad, h = 26, int(size * 1.9)
    w = int(tw + pad * 2 + 30)
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=(46, 40, 18), outline=GOLD, width=2)
    cy = y + h // 2
    d.ellipse((x + pad - 2, cy - 7, x + pad + 12, cy + 7), fill=GOLD)
    d.text((x + pad + 26, cy), text, font=ft, fill=GOLD, anchor="lm")
    return w, h


def centre_pill(d, W, y, text, size):
    ft = f(PB, size)
    w = int(d.textlength(text, font=ft) + 52 + 30)
    pill(d, (W - w) // 2, y, text, size)


def photo_card(w):
    p = Image.open(PHOTO).convert("RGB")
    h = int(p.height * w / p.width)
    return rounded(p.resize((w, h), Image.LANCZOS), 36)


def shadow(base, card, x, y):
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x + 8, y + 26, x + card.width - 8, y + card.height + 30), 40, fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    base.alpha_composite(sh)
    base.alpha_composite(card, (x, y))


def headline(d, W, y, big=150, small=62):
    t1a, t1b = "Save ", "$500"
    fb = f(PB, big)
    w1 = d.textlength(t1a, font=fb) + d.textlength(t1b, font=fb)
    x = (W - w1) / 2
    d.text((x, y), t1a, font=fb, fill=WHITE, anchor="la")
    d.text((x + d.textlength(t1a, font=fb), y), t1b, font=fb, fill=GOLD, anchor="la")
    d.text((W / 2, y + big * 1.12), "on Marodyne LiV", font=f(PB, small), fill=WHITE, anchor="ma")
    return y + big * 1.12 + small * 1.35


def feed():
    W, H = 1080, 1350
    im = bg(W, H).convert("RGBA")
    d = ImageDraw.Draw(im)
    centre_pill(d, W, 70, "BLACK FRIDAY OFFER", 30)
    y = headline(d, W, 160)
    d.text((W / 2, y + 4), "$500 off, incl. GST. Ends 30 November.", font=f(PM, 36), fill=MUTED, anchor="ma")
    card = photo_card(940)
    cy = int(y + 80)
    shadow(im, card, (W - card.width) // 2, cy)
    d = ImageDraw.Draw(im)
    by = cy + card.height + 60
    d.text((W / 2, by), "10 minutes a day. Gentle low-intensity vibration.", font=f(PSB, 34), fill=WHITE, anchor="ma")
    # CTA button
    ft = f(PB, 38)
    t = "Enquire at mewellness.com.au"
    bw = int(d.textlength(t, font=ft) + 100)
    bx, byy = (W - bw) // 2, by + 74
    d.rounded_rectangle((bx, byy, bx + bw, byy + 84), 42, fill=GOLD)
    d.text((W / 2, byy + 42), t, font=ft, fill=BG, anchor="mm")
    d.text((W / 2, H - 46), "Offer ends 30 Nov 2026. T&Cs apply.", font=f(PM, 24), fill=(130, 150, 142), anchor="ms")
    return im.convert("RGB")


def story_base():
    W, H = 1080, 1920
    im = bg(W, H).convert("RGBA")
    d = ImageDraw.Draw(im)
    centre_pill(d, W, 230, "BLACK FRIDAY OFFER", 34)
    y = headline(d, W, 340, 170, 68)
    return im, y


def story():
    W, H = 1080, 1920
    im, y = story_base()
    d = ImageDraw.Draw(im)
    d.text((W / 2, y + 6), "$500 off, incl. GST", font=f(PM, 42), fill=MUTED, anchor="ma")
    card = photo_card(980)
    cy = int(y + 100)
    shadow(im, card, (W - card.width) // 2, cy)
    d = ImageDraw.Draw(im)
    by = cy + card.height + 70
    d.text((W / 2, by), "10 minutes a day.", font=f(PB, 52), fill=WHITE, anchor="ma")
    d.text((W / 2, by + 70), "Gentle low-intensity vibration.", font=f(PSB, 42), fill=WHITE, anchor="ma")
    ft = f(PB, 42)
    t = "Enquire at mewellness.com.au"
    bw = int(d.textlength(t, font=ft) + 110)
    bx, byy = (W - bw) // 2, by + 170
    d.rounded_rectangle((bx, byy, bx + bw, byy + 96), 48, fill=GOLD)
    d.text((W / 2, byy + 48), t, font=ft, fill=BG, anchor="mm")
    d.text((W / 2, byy + 150), "Ends 30 Nov 2026 · T&Cs apply", font=f(PM, 30), fill=(130, 150, 142), anchor="ma")
    return im.convert("RGB")


BEATS = [
    ("Black Friday", "The biggest Marodyne LiV saving of the year"),
    ("How it works", "Stand on it for 10 minutes a day"),
    ("What it is", "A gentle low-intensity vibration platform for home use"),
    ("The offer", "$500 off, incl. GST, until 30 November 2026"),
    ("Claim it", "Enquire at mewellness.com.au"),
]
BEAT_S, FPS = 3.2, 30


def wrap(d, text, ft, mw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=ft) <= mw:
            cur = t
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    return out


def video(path):
    W, H = 1080, 1920
    base, y = story_base()
    src = Image.open(PHOTO).convert("RGB")
    card_w = 980
    cy = int(y + 90)
    n = int(len(BEATS) * BEAT_S * FPS)
    tmp = tempfile.mkdtemp()
    fl, fs = f(PB, 34), f(PB, 58)
    for i in range(n):
        t = i / FPS
        frame = base.copy()
        # slow zoom inside card
        z = 1.0 + 0.10 * (t / (n / FPS))
        cw, ch = src.width / z, src.height / z
        crop = src.crop(((src.width - cw) / 2, (src.height - ch) / 2, (src.width + cw) / 2, (src.height + ch) / 2))
        card = rounded(crop.resize((card_w, int(src.height * card_w / src.width)), Image.LANCZOS), 36)
        shadow(frame, card, (W - card_w) // 2, cy)
        d = ImageDraw.Draw(frame)
        bi = min(int(t // BEAT_S), len(BEATS) - 1)
        local = t - bi * BEAT_S
        a = min(1.0, local / 0.35)
        lab, txt = BEATS[bi]
        ty = cy + card.height + 90
        col = tuple(int(c * a + 10 * (1 - a)) for c in GOLD)
        d.text((W / 2, ty), lab.upper(), font=fl, fill=col, anchor="ma")
        lines = wrap(d, txt, fs, 900)
        for k, ln in enumerate(lines):
            c2 = tuple(int(255 * a + 10 * (1 - a)) for _ in range(3))
            d.text((W / 2, ty + 70 + k * 76), ln, font=fs, fill=c2, anchor="ma")
        # progress dots
        for k in range(len(BEATS)):
            x = W / 2 + (k - 2) * 34
            d.ellipse((x - 7, ty - 52, x + 7, ty - 38), fill=GOLD if k <= bi else (60, 70, 66))
        frame.convert("RGB").save(f"{tmp}/{i:04d}.jpg", quality=90)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.jpg",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", path], check=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    feed().save(os.path.join(OUT, "marodyne-bf-feed.jpg"), quality=92)
    story().save(os.path.join(OUT, "marodyne-bf-story.jpg"), quality=92)
    video(os.path.join(OUT, "marodyne-bf.mp4"))
    print("done")
