#!/usr/bin/env python3
"""Check internal links against the drip schedule.
For every page, each internal href="X.html" must point to a page that is live by THIS page's pubdate.
Imports PAGES from build.py without running main(). Reports broken + forward-link violations."""
import os, sys, re, importlib.util
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date(2026, 6, 10)
HREF = re.compile(r'href="([a-z0-9-]+)\.html"')

spec = importlib.util.spec_from_file_location("psgbuild", os.path.join(ROOT, "build.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # main() is guarded by __main__, so this only defines PAGES etc.
PAGES = mod.PAGES

def eff_date(slug):
    pd = PAGES[slug].get("pubdate")
    return date.fromisoformat(pd) if pd else date(1, 1, 1)  # no pubdate = live since forever

broken, forward = [], []
for slug, p in PAGES.items():
    this_live = date.fromisoformat(p["pubdate"]) if p.get("pubdate") else TODAY
    for tgt in set(HREF.findall(p["body"])):
        if tgt == slug:
            continue
        if tgt not in PAGES:
            broken.append((slug, tgt)); continue
        if eff_date(tgt) > this_live:
            forward.append((slug, tgt, this_live.isoformat(), PAGES[tgt].get("pubdate")))

if broken:
    print(f"BROKEN links ({len(broken)}) - target slug not in PAGES:")
    for s, t in broken:
        print(f"  {s}.html -> {t}.html  (no such page)")
if forward:
    print(f"FORWARD links ({len(forward)}) - target not live when source publishes:")
    for s, t, sd, td in forward:
        print(f"  {s} (live {sd}) -> {t} (live {td})")
if not broken and not forward:
    print("OK: all internal links resolve and respect the drip schedule.")
sys.exit(1 if (broken or forward) else 0)
