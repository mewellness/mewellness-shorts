"""Render every product in products.json into out/<date>-<slug>.mp4 (compressed for upload)."""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.environ.get("SHORTS_IMG_DIR", os.path.join(HERE, "img"))
only = set(sys.argv[1:])

OUT = os.path.join(os.path.dirname(HERE), "videos")
for p in json.load(open(os.environ.get("SHORTS_SPEC", os.path.join(HERE, "products.json")))):
    if only and p["slug"] not in only:
        continue
    work = os.path.join("/tmp/shorts-work", p["slug"])
    os.makedirs(work, exist_ok=True)
    for img in p["images"]:
        shutil.copy(os.path.join(DL, img), work)
    spec = {k: p[k] for k in ("images", "hook", "lines", "cta")}
    spec["beat"] = 3.6
    if "cta_label" in p:
        spec["cta_label"] = p["cta_label"]
    json.dump(spec, open(os.path.join(work, "spec.json"), "w"))
    raw = os.path.join(work, "raw.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "make_short.py"), os.path.join(work, "spec.json"), raw], check=True)
    out = os.path.join(OUT, f"{p['date']}-{p['slug']}.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-c:v", "libx264", "-crf", "26",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "48k",
                    "-movflags", "+faststart", out], check=True)
    for ts in (2, 9, 17):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(ts), "-i", out, "-frames:v", "1",
                        "-vf", "scale=360:-1", os.path.join(work, f"thumb{ts}.png")], check=True)
    print("done", out, os.path.getsize(out))
