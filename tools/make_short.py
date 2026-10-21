"""Build a 9:16 silent product Short from still images.

Usage: python3 make_short.py spec.json out.mp4

spec.json:
{
  "images": ["a.jpg", "b.jpg"],          # 1-3 product images
  "hook": "Hot sleeper?",                 # big top line, whole video
  "lines": ["Benefit 1", "Benefit 2", "Benefit 3"],  # shown one at a time
  "cta": "mewellness.com.au"              # final beat
}
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
BEAT = 3.0                       # seconds per text beat
MINT = (94, 242, 208)
WHITE = (255, 255, 255)
BG = (10, 10, 10)
FONT_B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_M = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
if not os.path.exists(FONT_M):
    FONT_M = FONT_B

# Layout (keeps text clear of TikTok/Shorts UI: right rail and bottom ~280px)
IMG_TOP, IMG_SIZE, IMG_X = 330, 960, 60   # square image band
TEXT_Y = IMG_TOP + IMG_SIZE + 36        # benefit text area start
MAX_TEXT_W = 900


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
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


def fit_square(img):
    """Pad/crop source to a square, padding with a blurred copy so nothing is cut off."""
    img = img.convert("RGB")
    s = max(img.size)
    bg = img.resize((s, s)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (s, s), BG), 0.45)
    bg.paste(img, ((s - img.width) // 2, (s - img.height) // 2))
    return bg.resize((IMG_SIZE * 2 // 1, IMG_SIZE * 2 // 1), Image.LANCZOS)  # 2x for zoom headroom


def background(img):
    b = img.resize((H, H)).filter(ImageFilter.GaussianBlur(60))
    b = b.crop(((H - W) // 2, 0, (H - W) // 2 + W, H))
    return Image.blend(b, Image.new("RGB", (W, H), BG), 0.7)


def ease(t):
    return t * t * (3 - 2 * t)


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    srcs = [Image.open(os.path.join(base, p)) for p in spec["images"]]
    squares = [fit_square(s) for s in srcs]
    bgs = [background(s) for s in srcs]

    BEAT_S = spec.get("beat", BEAT)
    beats = [b if isinstance(b, dict) else {"label": "", "text": b} for b in spec["lines"]]
    beats.append({"label": spec.get("cta_label", "Shop now at"), "text": spec["cta"], "cta": True})
    total = BEAT_S * len(beats)
    nframes = int(total * FPS)
    per_img = total / len(squares)

    f_hook = ImageFont.truetype(FONT_B, 80)
    f_line = ImageFont.truetype(FONT_B, 54)
    f_cta = ImageFont.truetype(FONT_B, 66)
    f_small = ImageFont.truetype(FONT_B, 34)

    tmp = tempfile.mkdtemp()
    for i in range(nframes):
        t = i / FPS
        k = min(int(t // per_img), len(squares) - 1)
        local = (t - k * per_img) / per_img

        frame = bgs[k].copy()
        # Ken Burns: slow zoom 1.00 -> 1.10, alternating direction per image
        z = 1.0 + 0.10 * (local if k % 2 == 0 else 1 - local)
        sq = squares[k]
        cw = int(sq.width / z)
        off = (sq.width - cw) // 2
        crop = sq.crop((off, off, off + cw, off + cw)).resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR)
        frame.paste(crop, (IMG_X, IMG_TOP))

        # crossfade into next image over last 0.4s of a segment
        if k + 1 < len(squares):
            fade = (t - ((k + 1) * per_img - 0.4)) / 0.4
            if fade > 0:
                nxt = bgs[k + 1].copy()
                sq2 = squares[k + 1]
                z2 = 1.0
                nxt.paste(sq2.resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR), (IMG_X, IMG_TOP))
                frame = Image.blend(frame, nxt, min(fade, 1))

        d = ImageDraw.Draw(frame)

        # Hook (top, whole video)
        hl = wrap(d, spec["hook"], f_hook, MAX_TEXT_W)
        y = IMG_TOP - 44 - len(hl) * 96
        for ln in hl:
            d.text((80, y), ln, font=f_hook, fill=WHITE)
            y += 96
        d.rectangle((80, IMG_TOP - 28, 200, IMG_TOP - 20), fill=MINT)

        # Current beat (fade + slide in)
        b = min(int(t // BEAT_S), len(beats) - 1)
        bt = (t - b * BEAT_S) / 0.35
        a = ease(min(max(bt, 0), 1))
        beat = beats[b]
        is_cta = beat.get("cta", False)
        font = f_cta if is_cta else f_line
        if is_cta:
            size = 66
            while size > 40 and d.textlength(beat["text"], font=ImageFont.truetype(FONT_B, size)) > 820:
                size -= 2
            font = ImageFont.truetype(FONT_B, size)
        lines = wrap(d, beat["text"], font, MAX_TEXT_W - 40)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        al = int(255 * a)
        yy = TEXT_Y + int((1 - a) * 30)
        if beat["label"]:
            ld.text((80, yy), beat["label"].upper() if not is_cta else beat["label"], font=f_small, fill=MINT + (al,))
            yy += 56
        if is_cta:
            for ln in lines:
                ld.text((80, yy), ln, font=font, fill=WHITE + (al,))
                yy += 80
        else:
            ld.rounded_rectangle((80, yy + 12, 90, yy + 12 + 68 * len(lines) - 18), 5, fill=MINT + (al,))
            for ln in lines:
                ld.text((114, yy), ln, font=font, fill=WHITE + (al,))
                yy += 68
        frame = Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")
        frame.save(os.path.join(tmp, f"f{i:05d}.jpg"), quality=92)

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
        "-i", os.path.join(tmp, "f%05d.jpg"),
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",  # silent track: some platforms reject no-audio uploads
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", out_path,
    ], check=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
