#!/usr/bin/env python3
"""Deterministic internal-linker (0 LLM tokens). Wraps mentions of other live pages
in <a href="slug.html"> inside an article's section HTML, skipping text already in tags/anchors.
DeepSeek won't add internal links reliably, so we add them here."""
import re, json, os

GENERIC = {"cost","running","costs","explained","the","to","a","an","of","vs","your","how","is",
           "worth","it","and","per","what","does","much","do","i","my","for","in","on","with","you"}

def phrase_for(slug):
    words = [w for w in slug.split("-") if w not in GENERIC]
    return " ".join(words) if len(words) >= 2 else None  # require >=2 distinctive words to avoid junk links

def build_map(live_slugs, self_slug):
    m = {}
    for s in live_slugs:
        if s == self_slug:
            continue
        p = phrase_for(s)
        if p:
            m[p.lower()] = s
    # longest phrases first so "air source heat pump" beats "heat pump"
    return sorted(m.items(), key=lambda kv: -len(kv[0]))

def link_html(html, phrase_map, used, max_total):
    parts = re.split(r"(<[^>]+>)", html)
    anchor_depth = 0
    for i, tok in enumerate(parts):
        if tok.startswith("<"):
            if tok.lower().startswith("<a"): anchor_depth += 1
            elif tok.lower().startswith("</a"): anchor_depth = max(0, anchor_depth-1)
            continue
        if anchor_depth or len(used) >= max_total:
            continue
        for phrase, slug in phrase_map:
            if slug in used:
                continue
            m = re.search(r"\b" + re.escape(phrase) + r"\b", tok, re.I)
            if m:
                a, b = m.span()
                parts[i] = tok[:a] + f'<a href="{slug}.html">' + tok[a:b] + "</a>" + tok[b:]
                used.add(slug)
                break
    return "".join(parts)

def autolink(art, live_slugs, max_total=6):
    pmap = build_map(live_slugs, art["slug"])
    used = set()
    for sec in art["sections"]:
        sec["html"] = link_html(sec["html"], pmap, used, max_total)
    return art, used

if __name__ == "__main__":
    import sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    live = json.load(open(os.path.join(root, ".ds_live_slugs.json")))
    fp = sys.argv[1]
    art = json.load(open(fp))
    art, used = autolink(art, live)
    json.dump(art, open(fp, "w"), indent=1, ensure_ascii=False)
    print(f"{art['slug']}: linked {len(used)} pages -> {sorted(used)}")
