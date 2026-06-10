#!/usr/bin/env python3
"""Assemble .flagship/articles/*.json into build.py as PAGES entries + GUIDES_ORDER slugs.
Deterministic, idempotent-ish (refuses if markers already present). Run from repo root."""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build.py")
PLAN = os.path.join(HERE, "plan.json")
ARTS = os.path.join(HERE, "articles")

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

DASHES = ("—", "–")

def faq_jsonld(faq):
    obj = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": f["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c")  # defend the </script> boundary; no '<' expected in FAQ text

def build_body(art):
    parts = ['\n  <section class="section"><div class="wrap prose">\n', STYLE, "\n\n",
             f'    <p class="lede">{art["lede"]}</p>\n\n',
             f'    <div class="ev-key">\n      <p><strong>The short answer.</strong> {art["short_answer"]}</p>\n    </div>\n\n']
    for sec in art["sections"]:
        parts.append(f'    <h2>{sec["h2"]}</h2>\n{sec["html"]}\n\n')
    parts.append('  </div></section>\n')
    parts.append(f'  <script type="application/ld+json">{faq_jsonld(art["faq"])}</script>\n')
    return "".join(parts)

def render_entry(art, pubdate):
    body = build_body(art)
    bad = [d for d in DASHES if d in body]
    if bad:
        return None, f"contains dash {[hex(ord(d)) for d in bad]}"
    if "'''" in body:
        return None, "body contains triple-single-quote"
    src_body = body.replace("\\", "\\\\")  # escape backslashes so triple-quoted literal round-trips exactly
    lines = [f'PAGES[{art["slug"]!r}] = dict(',
             f'    title={art["title"]!r},',
             f'    description={art["description"]!r},',
             f'    active="guides",',
             f'    blurb={art["blurb"]!r},']
    if pubdate:
        lines.append(f'    pubdate="{pubdate}",')
    lines.append(f"    body='''{src_body}''',")
    lines.append(")\n")
    return "\n".join(lines), None

def main():
    plan = json.load(open(PLAN))
    today = [(p["slug"], p["cluster"], "") for p in plan["today_pages"]]
    queue = [(q["slug"], q["cluster"], q["pubdate"]) for q in plan["queue"]]
    ordered = today + queue

    src = open(BUILD, encoding="utf-8").read()
    if "Flagship year-queue" in src:
        sys.exit("ERROR: build.py already contains the flagship batch markers. Aborting to avoid double-insert.")

    blocks, missing, skipped = [], [], []
    new_today_slugs, new_queue_by_cluster = [], {}
    for slug, cluster, pubdate in ordered:
        fp = os.path.join(ARTS, slug + ".json")
        if not os.path.exists(fp):
            missing.append(slug); continue
        try:
            art = json.load(open(fp, encoding="utf-8"))
        except Exception as e:
            skipped.append((slug, f"bad json: {e}")); continue
        for k in ("slug", "title", "description", "blurb", "lede", "short_answer", "sections", "faq"):
            if k not in art:
                skipped.append((slug, f"missing field {k}")); art = None; break
        if art is None:
            continue
        entry, err = render_entry(art, pubdate)
        if err:
            skipped.append((slug, err)); continue
        blocks.append(entry)
        if pubdate:
            new_queue_by_cluster.setdefault(cluster, []).append((pubdate, slug))
        else:
            new_today_slugs.append(slug)

    if missing:
        print(f"MISSING ({len(missing)}):", " ".join(missing))
    if skipped:
        print(f"SKIPPED ({len(skipped)}):")
        for s, why in skipped:
            print(f"  {s}: {why}")
    if not blocks:
        sys.exit("No article blocks rendered; aborting.")

    new_pages = "\n" + "\n".join(blocks) + "\n"

    # 1) insert PAGES blocks just before GUIDES_ORDER
    anchor = "\nGUIDES_ORDER = ["
    assert src.count(anchor) == 1, "GUIDES_ORDER anchor not unique"
    src = src.replace(anchor, "\n" + new_pages + anchor, 1)

    # 2) today slugs at the top of GUIDES_ORDER
    def fmt(slugs):
        out, line = [], "    "
        for s in slugs:
            piece = f'"{s}", '
            if len(line) + len(piece) > 96:
                out.append(line.rstrip()); line = "    "
            line += piece
        if line.strip():
            out.append(line.rstrip())
        return "\n".join(out)

    top_anchor = "GUIDES_ORDER = [\n"
    today_block = "    # Flagship batch - live today\n" + fmt(new_today_slugs) + "\n"
    src = src.replace(top_anchor, top_anchor + today_block, 1)

    # 3) queue slugs grouped by cluster, before the list close
    close_anchor = '"quick-wins-under-a-tenner",\n]'
    assert close_anchor in src, "GUIDES_ORDER close anchor not found"
    CL_NAMES = {"A": "Appliance running cost", "B": "Heating behaviour", "C": "Grants and bill support",
                "D": "Tariffs, meters and billing", "E": "Battery, smart energy and future tech",
                "F": "Insulation and draughtproofing", "G": "Damp, condensation and ventilation",
                "H": "Seasonal and lifestyle", "I": "Cooling", "J": "EV and driving"}
    qparts = ["    # Flagship year-queue (drip by pubdate)"]
    for cl in sorted(new_queue_by_cluster):
        slugs = [s for _, s in sorted(new_queue_by_cluster[cl])]
        qparts.append(f"    # {CL_NAMES.get(cl, cl)}")
        qparts.append(fmt(slugs))
    queue_block = "\n".join(qparts)
    src = src.replace(close_anchor, '"quick-wins-under-a-tenner",\n' + queue_block + "\n]", 1)

    open(BUILD, "w", encoding="utf-8").write(src)
    print(f"Inserted {len(blocks)} PAGES entries "
          f"({len(new_today_slugs)} live today, {len(blocks)-len(new_today_slugs)} queued).")

if __name__ == "__main__":
    main()
