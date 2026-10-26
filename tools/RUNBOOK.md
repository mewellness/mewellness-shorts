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
7. Cross-post the same video (same Metricool/raw.githubusercontent media URL) as two more separate posts:
   - Instagram Reel at 19:00: instagramData {type "REEL", showReelOnFeed true, isAiGenerated false}.
     Caption = YouTube description with "#shorts" replaced by "#reels #mewellness".
   - TikTok video at 20:00: tiktokData {privacyOption "PUBLIC_TO_EVERYONE", commercialContentOwnBrand true,
     title = YouTube title without "#shorts", autoAddMusic false, isAigc false}.
     Caption = YouTube description with "#shorts" replaced by "#mewellness #fyp".
   Keep the "Always read the label..." line where the rules require it.

## Daily health check
Every run, before anything else: getScheduledPosts for yesterday through the next 7 days and look at every
provider status. Any post in ERROR:
- still in the future -> updateScheduledPost with identical content and date to re-queue it, then re-check;
- already past -> move it to the next free day for that network at its usual time (IG feed 10:00, YouTube 17:00,
  TikTok photo 18:00, IG Reel 19:00, TikTok video 20:00) with identical content;
- if anything is still in ERROR afterwards, or the error says the account limit was reached, notify the user
  with the exact error text.
Also, if tomorrow already has a YouTube Short but no IG Reel/TikTok video of it, create those two from the
Short's media URL (step 7).
