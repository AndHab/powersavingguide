#!/usr/bin/env python3
"""Insert into build.py ONLY the plan articles not already present in PAGES.
For finishing the flagship year-queue after the initial batch was inserted.
Run from repo root. Idempotent: already-present slugs are skipped."""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build.py")
PLAN = os.path.join(HERE, "plan.json")
ARTS = os.path.join(HERE, "articles")

spec = importlib.util.spec_from_file_location("asm", os.path.join(HERE, "assemble.py"))
asm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asm)  # main() is guarded, this only defines the render helpers

spec2 = importlib.util.spec_from_file_location("psgbuild", BUILD)
bld = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(bld)
existing = set(bld.PAGES)

def main():
    plan = json.load(open(PLAN))
    ordered = ([(p["slug"], p["cluster"], "") for p in plan["today_pages"]]
               + [(q["slug"], q["cluster"], q["pubdate"]) for q in plan["queue"]])

    blocks, new_slugs, missing, skipped = [], [], [], []
    for slug, cluster, pubdate in ordered:
        if slug in existing:
            continue
        fp = os.path.join(ARTS, slug + ".json")
        if not os.path.exists(fp):
            missing.append(slug); continue
        try:
            art = json.load(open(fp, encoding="utf-8"))
        except Exception as e:
            skipped.append((slug, f"bad json: {e}")); continue
        bad = [k for k in ("slug", "title", "description", "blurb", "lede",
                           "short_answer", "sections", "faq") if k not in art]
        if bad:
            skipped.append((slug, f"missing fields {bad}")); continue
        entry, err = asm.render_entry(art, pubdate)
        if err:
            skipped.append((slug, err)); continue
        blocks.append(entry)
        new_slugs.append(slug)

    if missing:
        print(f"STILL MISSING ({len(missing)}):", " ".join(missing))
    for s, why in skipped:
        print(f"SKIPPED {s}: {why}")
    if not blocks:
        sys.exit("Nothing new to insert." if not (missing or skipped) else
                 "No insertable articles (see above).")

    src = open(BUILD, encoding="utf-8").read()
    anchor = "\nGUIDES_ORDER = ["
    assert src.count(anchor) == 1, "GUIDES_ORDER anchor not unique"
    src = src.replace(anchor, "\n\n" + "\n".join(blocks) + "\n" + anchor, 1)

    qanchor = "    # Flagship year-queue (drip by pubdate)\n"
    assert qanchor in src, "year-queue comment anchor not found"
    slug_lines = "".join(f'    "{s}",\n' for s in new_slugs)
    src = src.replace(qanchor, qanchor + "    # batch 2 fill\n" + slug_lines, 1)

    open(BUILD, "w", encoding="utf-8").write(src)
    print(f"Inserted {len(blocks)} new PAGES entries into build.py.")

if __name__ == "__main__":
    main()
