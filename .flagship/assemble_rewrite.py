#!/usr/bin/env python3
"""Replace existing thin PAGES["slug"] entries in build.py with deepened versions
built from .flagship/articles/<slug>.json. In-place, idempotent (re-running just
re-renders from JSON). Does NOT touch GUIDES_ORDER (these slugs are already listed).
Run from repo root."""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build.py")
ARTS = os.path.join(HERE, "articles")

# hub pages keep their own nav-active; everything else lights up "Guides"
HUB_ACTIVE = {"electricity": "electricity", "heating": "heating", "driving": "driving"}

STYLE = '''    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>'''

DASHES = ("—", "–", "‒", "―", "−")

def faq_jsonld(faq):
    obj = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": f["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c")

def build_body(art):
    parts = ['\n  <section class="section"><div class="wrap prose">\n', STYLE, "\n\n",
             f'    <p class="lede">{art["lede"]}</p>\n\n',
             f'    <div class="ev-key">\n      <p><strong>The short answer.</strong> {art["short_answer"]}</p>\n    </div>\n\n']
    for sec in art["sections"]:
        parts.append(f'    <h2>{sec["h2"]}</h2>\n{sec["html"]}\n\n')
    parts.append('  </div></section>\n')
    parts.append(f'  <script type="application/ld+json">{faq_jsonld(art["faq"])}</script>\n')
    return "".join(parts)

def render_entry(art):
    body = build_body(art)
    bad = [d for d in DASHES if d in body]
    if bad:
        return None, f"contains dash {[hex(ord(d)) for d in bad]}"
    if "'''" in body:
        return None, "body contains triple-single-quote"
    src_body = body.replace("\\", "\\\\")
    active = HUB_ACTIVE.get(art["slug"], "guides")
    lines = [f'PAGES[{art["slug"]!r}] = dict(',
             f'    title={art["title"]!r},',
             f'    description={art["description"]!r},',
             f'    active={active!r},',
             f'    blurb={art["blurb"]!r},',
             f"    body='''{src_body}''',",
             ")\n"]
    return "\n".join(lines), None

def replace_block(src, slug, new_block):
    """Replace the whole `PAGES["slug"] = dict( ... )` top-level block."""
    start_marker = f'PAGES["{slug}"] = dict('
    idx = src.find(start_marker)
    if idx == -1:
        return src, f"start marker not found"
    if src.find(start_marker, idx + 1) != -1:
        return src, "start marker not unique"
    # end = next top-level PAGES[ entry, or the GUIDES_ORDER section, after this block
    nxt_pages = src.find("\nPAGES[", idx + 1)
    nxt_guides = src.find("\nGUIDES_ORDER", idx + 1)
    cands = [c for c in (nxt_pages, nxt_guides) if c != -1]
    if not cands:
        return src, "no following anchor found"
    end = min(cands)
    # new_block already ends with ")\n"; preserve the blank line before next entry
    return src[:idx] + new_block + "\n" + src[end + 1:], None

def main():
    slugs = ["heating", "driving", "electricity", "led-lighting", "hot-water-savings", "thermostat-settings", "understanding-energy-bill", "fridge-freezer-efficiency", "standby-power-the-full-story", "radiator-reflectors", "hypermiling", "switching-suppliers", "low-flow-showerheads", "kettle-energy-saving", "oven-microwave-air-fryer-compared", "secondary-glazing", "solid-wall-insulation", "air-fryer-running-cost", "is-double-glazing-worth-it", "how-condensing-boilers-work", "how-to-bleed-radiators", "washing-at-30-degrees", "washing-machine-running-cost", "curtains-for-warmth", "underfloor-insulation", "cylinder-jacket-and-pipe-lagging", "dishwasher-efficiency", "cavity-wall-insulation", "induction-vs-gas-hob", "smart-thermostats", "slow-cooker-economy", "radiator-valves-and-zoning", "heat-pumps-explained", "ev-running-cost-vs-petrol", "ground-vs-air-source-heat-pumps", "solar-water-heating", "broadband-router-always-on", "hot-tub-running-cost", "television-and-entertainment-energy", "winter-energy-checklist", "using-a-plug-in-energy-monitor", "quick-wins-under-a-tenner", "saving-energy-when-renting", "electric-blanket-vs-heating"]
    src = open(BUILD, encoding="utf-8").read()
    done, errs = [], []
    for slug in slugs:
        fp = os.path.join(ARTS, slug + ".json")
        if not os.path.exists(fp):
            errs.append((slug, "no json")); continue
        art = json.load(open(fp, encoding="utf-8"))
        block, err = render_entry(art)
        if err:
            errs.append((slug, err)); continue
        src, err = replace_block(src, slug, block)
        if err:
            errs.append((slug, err)); continue
        done.append(slug)
    if errs:
        print("ERRORS:")
        for s, e in errs:
            print(f"  {s}: {e}")
        sys.exit("Aborting without writing build.py")
    open(BUILD, "w", encoding="utf-8").write(src)
    print(f"Replaced {len(done)} PAGES entries in build.py.")

if __name__ == "__main__":
    main()
