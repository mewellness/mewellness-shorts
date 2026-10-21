# MeWellness daily YouTube Short — runbook

Goal: one YouTube Short published every day at 17:00 Australia/Sydney on the MeWellness channel, via Metricool (brand blogId 7456788).

## Content rules
- High-value MeWellness products only. Never ice baths, never the AFO, never sister brands (Air Relax, RehaCare etc.).
- Product pool (rotate, never the same product two days running, avoid repeating a product within 7 days):
  Oak Sleep HUB 2, OxyRevo Apex36, OxyRevo Quest30, OxyRevo Quest36, Neuradiant 1070, Neuronic LIGHT,
  Therabody JetBoots PRO Plus, OSKA Pulse, POWERbreathe K4, Theragun PRO Plus, ThermApparel RallyWrap,
  Rapid Release Pro3, Marodyne LiV, TheraFace Mask.
- Story structure (products.json format): hook (top line), then four beats labelled
  "The fact" / "Why it matters" / "What changes" / "Meet", then the CTA.
- Make it interesting: a genuine, checkable fact; why it matters in everyday life; how life changes with the product.
- Every new Short must use a NEW angle (different hook and fact) from previous Shorts for that product — check history.json.
- Australian advertising rules: facts must be physical/general and true. No claims that a product treats, cures,
  prevents or diagnoses any disease or condition, no testimonials, no "clinically proven". Add
  "Always read the label and follow the directions for use." to captions for light therapy, PEMF, hyperbaric,
  vibration platform products. Use prices only if already published (see history.json / existing posts).
- B2B products (Quest30, Quest36, Rapid Release Pro3): CTA mewellness.com.au/contact with a clinic-quote label.
- Silent video, no voiceover, no music.

## Images
Source images are the product photos already uploaded to Metricool for the @mewellnessau Instagram posts
(static.metricool.com URLs, found via getScheduledPosts on the brand, which includes published posts).
Download with curl into a scratch folder. They already carry the MeWellness logo badge.
Known image URLs per product are recorded in images.json.

## Build
1. Add an entry to a one-item products JSON (same format as products.json; include date, slug, images,
   hook, lines, cta, optional cta_label, title (ends with #shorts), desc, tags).
2. Point DL in render_all.py at the folder holding the images (or copy images next to the spec),
   run make_short.py / render_all.py. Output: videos/<date>-<slug>.mp4 (compressed, ~1-2 MB).
3. Look at frames at ~2s, ~9s and ~17s: text must not run off the right edge or past ~y=1650.
4. Commit the video and the updated history.json to main and push.
5. Public URL: https://raw.githubusercontent.com/mewellness/mewellness-shorts/main/videos/<file>.mp4
6. Metricool createScheduledPost: providers youtube, youtubeData {type "short", privacy "public",
   madeForKids false, isAiGeneratedContent false, category HOWTO_STYLE, title, tags}, autoPublish true,
   draft false, publicationDate <date>T17:00:00 Australia/Sydney.
