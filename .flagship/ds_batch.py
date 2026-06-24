#!/usr/bin/env python3
"""Finalised token-cheap DeepSeek pipeline: flash writes -> harness-driven fix-loop
(DeepSeek self-corrects) -> deterministic auto-linker -> final harness.
0 Claude tokens/article. Drafts staged in .flagship/articles_ds/ (never live until assembled).
Report -> .flagship/ds_batch_report.txt
"""
import sys, json, urllib.request, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolink import autolink

KEY = re.search(r'sk-[A-Za-z0-9]+', open("/home/andreas/.config/goose/secrets.yaml").read()).group(0)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = set(json.load(open(os.path.join(ROOT, ".ds_live_slugs.json"))))
OUT = os.path.join(ROOT, ".flagship", "articles_ds"); os.makedirs(OUT, exist_ok=True)
ALLOW = ", ".join(sorted(LIVE))

TOPICS = [
 ("oil-filled-radiator-running-cost", "How much does it cost to run an oil-filled radiator?", "1.5kW to 2.5kW, thermostat cycling"),
 ("infrared-heater-running-cost", "How much does it cost to run an infrared heater?", "panels 300W to 1kW, heats objects not air"),
 ("convector-heater-running-cost", "How much does it cost to run a convector heater?", "1kW to 2kW, fast warmth, poor at holding heat"),
 ("cost-to-run-a-microwave", "How much does it cost to run a microwave?", "700W to 1200W output, short runs, small cost per use"),
 ("cost-to-run-a-hair-dryer", "How much does it cost to run a hair dryer?", "1.5kW to 2.2kW but used for minutes"),
 ("cost-to-run-a-games-console", "How much does it cost to run a games console?", "150W to 200W in play, rest/standby modes matter"),
 ("cost-to-run-a-desktop-pc-all-day", "How much does it cost to run a desktop PC all day?", "office 60W to 150W, gaming 300W to 500W"),
 ("cost-to-run-a-pressure-washer", "How much does it cost to run a pressure washer?", "1.4kW to 2.1kW, short bursts"),
 ("cost-to-run-a-pond-pump", "How much does it cost to run a pond pump?", "runs 24/7, 20W to 100W, low watt adds up"),
 ("cost-to-run-a-coffee-machine", "How much does it cost to run a coffee machine?", "1kW to 1.5kW for seconds per cup, keep-warm is the hidden cost"),
]

def ds(system, user, maxt=8000):
    import time as _t
    body = {"model": "deepseek-v4-flash", "messages": [{"role": "system", "content": system},
            {"role": "user", "content": user}], "temperature": 0.4, "max_tokens": maxt,
            "stream": False, "response_format": {"type": "json_object"}}
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(body).encode(),
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(json.load(r)["choices"][0]["message"]["content"])
        except Exception as e:
            last = e; _t.sleep(5 * (attempt + 1))
    raise last

def text_of(art):
    htmls = [s["html"] for s in art["sections"]]
    full = " ".join([art["lede"], art["short_answer"]] + htmls + [f["q"]+" "+f["a"] for f in art["faq"]])
    return full, htmls

def harness(art):
    iss = []
    for k in ("slug","title","description","blurb","lede","short_answer","sections","faq"):
        if k not in art: return [f"missing {k}"]
    full, htmls = text_of(art)
    wc = len(re.sub(r"<[^>]+>", " ", full).split())
    if wc < 1000: iss.append(f"too short ({wc} words, expand to 1100-1500)")
    if not (140 <= len(art["description"]) <= 165): iss.append(f"description {len(art['description'])} chars (need 150-160)")
    if any(d in full for d in ("—","–","‒","―","−")): iss.append("contains a dash character (remove ALL dashes, use commas or 'to')")
    rates = set(re.findall(r'(\d{1,2}\.\d{1,2})\s?p\s?(?:per kWh|/kWh|a unit)', full)) - {"26.11","7.33"}
    if rates: iss.append(f"uses non-cap per-kWh rates {rates} (only 26.11p elec / 7.33p gas allowed)")
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s?kWh[^.<]{0,40}?(\d+(?:\.\d+)?)\s?p\b(?!\s?(?:per kWh|/kWh|a unit|per unit))', full):
        k, p = float(m.group(1)), float(m.group(2))
        if p < 1000 and abs(k*26.11 - p) > 2.5 and abs(k*7.33 - p) > 1.5:
            iss.append(f"arithmetic wrong: {k}kWh is {k*26.11:.0f}p at 26.11p, not {p}p")
    return iss

def links_count(art):
    _, htmls = text_of(art)
    return set(re.findall(r'href="([a-z0-9-]+)\.html"', " ".join(htmls)))

GEN_SYS = "You are a UK energy writer. Output ONLY valid JSON, no markdown."
def gen_user(slug, title, hint):
    return (f'Write a JSON article, keys EXACTLY slug,title,description,blurb,lede,short_answer,sections,faq. '
            f'slug="{slug}". title about: {title}. sections 5-7 objects {{h2,html}} with at least one '
            f'<table class="ev-table"><thead><tbody>. faq 4-6 {{q,a}}. description 150-160 chars. '
            f'1100-1500 words, plain British English, practical. Topic notes: {hint}. '
            f'HARD RULES: zero em/en dashes (use commas or "to" for ranges). Use ONLY Ofgem cap figures '
            f'(electricity 26.11p/kWh, gas 7.33p/kWh, electricity standing charge 57.19p/day); invent no other prices; '
            f'every worked sum correct (2kW for 1h = 2 kWh = 52p). No invented brands/grants/stats. '
            f'No AI-filler (delve, moreover, robust, leverage, seamless).')

def fix_user(art, issues):
    return ("Fix this UK energy article JSON. Problems: " + "; ".join(issues) +
            ". Keep the topic, structure and all correct figures (electricity 26.11p/kWh, gas 7.33p/kWh). "
            "Use NO dash characters at all. Return the COMPLETE corrected JSON, same keys.\n\n" +
            json.dumps(art, ensure_ascii=False))

DASHES_CLASS = "—–‒―−"
def strip_dashes(art):
    def fx(s):
        s = re.sub(r'(\d)\s*[' + DASHES_CLASS + r']\s*(\d)', r'\1 to \2', s)  # numeric ranges -> "to"
        s = re.sub(r'\s*[' + DASHES_CLASS + r']\s*', ', ', s)                  # everything else -> pause comma
        return s
    for k in ("title", "description", "blurb", "lede", "short_answer"):
        art[k] = fx(art[k])
    for sec in art["sections"]:
        sec["h2"] = fx(sec["h2"]); sec["html"] = fx(sec["html"])
    for f in art["faq"]:
        f["q"] = fx(f["q"]); f["a"] = fx(f["a"])
    return art

HUB_LABELS = {"appliance-running-cost": "the running cost calculator", "electricity": "where your electricity goes",
              "using-a-plug-in-energy-monitor": "a plug-in energy monitor", "standby-power-the-full-story": "standby power",
              "heating": "home heating", "electric-blanket-vs-heating": "heating the person not the room"}
def ensure_links(art, min_links=4):
    have = links_count(art)
    if len(have) >= min_links:
        return art
    pick = [s for s in HUB_LABELS if s in LIVE and s not in have and s != art["slug"]][:min_links - len(have)]
    if pick and art["sections"]:
        anchors = ", ".join(f'<a href="{s}.html">{HUB_LABELS[s]}</a>' for s in pick)
        art["sections"][-1]["html"] += f"<p>For working out and trimming running costs, see {anchors}.</p>"
    return art

def gen_with_retry(sysmsg, usermsg, tries=3):
    for _ in range(tries):
        try:
            return ds(sysmsg, usermsg)
        except Exception:
            continue
    return None

def main():
    report = [f"DeepSeek batch (robust) - {len(TOPICS)} articles", "="*60]
    for slug, title, hint in TOPICS:
        entry = f"\n### {slug}"
        try:
            art = gen_with_retry(GEN_SYS, gen_user(slug, title, hint))
            if art is None:
                entry += "  FAILED: generation returned no valid JSON after retries"
                report.append(entry); print(entry, flush=True); continue
            art["slug"] = slug
            art = strip_dashes(art)
            # one NON-FATAL fix pass, only for length/arithmetic/description (dashes+links are deterministic)
            iss = [i for i in harness(art) if any(t in i for t in ("short", "arithmetic", "description"))]
            if iss:
                fixed = gen_with_retry("You output only valid corrected JSON.", fix_user(art, iss), tries=2)
                if fixed:
                    fixed["slug"] = slug
                    art = strip_dashes(fixed)
            art, _ = autolink(art, sorted(LIVE))      # deterministic in-text links
            art = ensure_links(art)                    # guarantee >=4 links via related footer
            json.dump(art, open(os.path.join(OUT, slug+".json"), "w"), indent=1, ensure_ascii=False)
            final = harness(art); nlinks = len(links_count(art))
            wc = len(re.sub(r"<[^>]+>", " ", text_of(art)[0]).split())
            verdict = "CLEAN" if (not final and nlinks >= 4) else f"check: {final} links={nlinks}"
            entry += f"  {wc}w, {nlinks} links -> {verdict}"
        except Exception as e:
            entry += f"  FAILED: {e}"
        report.append(entry); print(entry, flush=True)
    open(os.path.join(ROOT, ".flagship", "ds_batch_report.txt"), "w").write("\n".join(report))
    print("\nDONE", flush=True)

if __name__ == "__main__":
    main()
