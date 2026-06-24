#!/usr/bin/env python3
"""Token-cheap DeepSeek article pipeline.
flash writes -> deterministic harness checks (0 Claude tokens) -> pro critiques (DeepSeek tokens).
Drafts staged in .flagship/articles_ds/ (NOT assembled, so never live until approved).
Writes a consolidated report to .flagship/ds_batch_report.txt.
"""
import sys, json, urllib.request, re, os, time

KEY = open("/home/andreas/.config/goose/secrets.yaml").read()
KEY = re.search(r'DEEPSEEK_API_KEY:\s*"?(sk-[A-Za-z0-9]+)', KEY).group(1)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = set(json.load(open(os.path.join(ROOT, ".ds_live_slugs.json"))))
OUT = os.path.join(ROOT, ".flagship", "articles_ds"); os.makedirs(OUT, exist_ok=True)

TOPICS = [
 ("oil-filled-radiator-running-cost", "How much does it cost to run an oil-filled radiator?", "typical 1.5kW to 2.5kW; thermostat cycling means it does not draw full power all the time"),
 ("infrared-heater-running-cost", "How much does it cost to run an infrared heater?", "panels 300W to 1kW; heats objects/people not air"),
 ("convector-heater-running-cost", "How much does it cost to run a convector heater?", "typical 1kW to 2kW; fast warmth, poor at holding heat"),
 ("cost-to-run-a-microwave", "How much does it cost to run a microwave?", "700W to 1200W output, draws more; short run times so cost per use is small"),
 ("cost-to-run-a-hair-dryer", "How much does it cost to run a hair dryer?", "1.5kW to 2.2kW but only used for minutes"),
 ("cost-to-run-a-games-console", "How much does it cost to run a games console?", "PS5/Xbox ~150W-200W in play, much less idle; rest/standby modes matter"),
 ("cost-to-run-a-desktop-pc-all-day", "How much does it cost to run a desktop PC all day?", "office PC 60W-150W, gaming PC 300W-500W under load"),
 ("cost-to-run-a-pressure-washer", "How much does it cost to run a pressure washer?", "1.4kW to 2.1kW, used in short bursts"),
 ("cost-to-run-a-pond-pump", "How much does it cost to run a pond pump?", "runs 24/7 so low wattage adds up; 20W-100W typical"),
 ("cost-to-run-a-coffee-machine", "How much does it cost to run a coffee machine?", "heating element ~1kW-1.5kW for seconds per cup; standby/keep-warm is the hidden cost"),
]

def ds(model, system, user, json_mode=False, max_tokens=6000, temp=0.4):
    body = {"model": model, "messages": [{"role": "system", "content": system},
            {"role": "user", "content": user}], "temperature": temp,
            "max_tokens": max_tokens, "stream": False}
    if json_mode: body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.load(r)["choices"][0]["message"]["content"]

GEN_SYS = "You are a UK energy writer for an independent bill-saving site. Output ONLY valid JSON, no markdown."
def gen_user(slug, title, hint):
    return f"""Write a long-form guide as JSON, keys EXACTLY:
slug,title,description,blurb,lede,short_answer,sections,faq.
slug must be "{slug}". title around: {title}.
sections: array of 5-7 {{h2, html}} (raw HTML, <p>/<ul>/<li>, at least one <table class="ev-table"> with <thead>/<tbody>).
faq: array of 4-6 {{q,a}} (plain text). description 150-160 chars. blurb one sentence. lede + short_answer plain text.
Target 1100-1400 words across sections. Plain British English, practical and honest.
TOPIC NOTES: {hint}.
HARD RULES:
- ZERO em-dashes or en-dashes anywhere. Use commas, full stops, or "to" for ranges. Strict.
- Use ONLY these figures (Ofgem cap 1 Jul to 30 Sep 2026): electricity 26.11p per kWh, gas 7.33p per kWh, electricity standing charge 57.19p per day. Invent NO other prices. Every worked example must be arithmetically correct (e.g. 2kW for 1 hour = 2 kWh = 52p).
- Do NOT invent supplier names, grants, brands, or statistics you are unsure of.
- No AI-filler (delve, moreover, furthermore, robust, leverage, seamless, "it is worth noting").
- You MUST include 4 to 6 internal links as <a href="SLUG.html">, choosing only from this list of real pages, where relevant:
{", ".join(sorted(LIVE))}"""

AMERICAN = re.compile(r'\b(color|colors|optimize|organize|realize|favorite|liter|liters|fiber|aluminum|center|theater|traveler|gray|defense|license plate)\b', re.I)
FILLER = ["delve","moreover","furthermore","leverage","seamless","game-chang","it is worth noting","it's worth noting","robust"]
DASHES = ("—","–","‒","―","−")

def harness(art):
    issues = []
    for k in ("slug","title","description","blurb","lede","short_answer","sections","faq"):
        if k not in art: issues.append(f"missing key {k}")
    if issues: return issues
    blob = json.dumps(art, ensure_ascii=False)
    full = " ".join([art["lede"], art["short_answer"]] + [s.get("html","") for s in art["sections"]]
                    + [f["q"]+" "+f["a"] for f in art["faq"]])
    text = re.sub(r"<[^>]+>", " ", full)
    wc = len(text.split())
    if not (1000 <= wc <= 1700): issues.append(f"word count {wc} out of 1000-1700")
    if not (140 <= len(art["description"]) <= 165): issues.append(f"description {len(art['description'])} chars")
    for d in DASHES:
        if d in blob: issues.append(f"DASH {hex(ord(d))} present"); break
    links = re.findall(r'href="([a-z0-9-]+)\.html"', blob)
    bad = [l for l in set(links) if l not in LIVE]
    if bad: issues.append(f"links not in allowlist: {bad}")
    if len(set(links)) < 3: issues.append(f"only {len(set(links))} internal links (<3)")
    rates = set(re.findall(r'(\d{1,2}\.\d{1,2})\s?p\s?(?:per kWh|/kWh|a unit|per unit)', full))
    badrates = rates - {"26.11","7.33"}
    if badrates: issues.append(f"non-cap per-kWh rates: {badrates}")
    am = set(m.lower() for m in AMERICAN.findall(text))
    if am: issues.append(f"US spelling: {am}")
    fl = [w for w in FILLER if w in text.lower()]
    if fl: issues.append(f"AI filler: {fl}")
    # arithmetic: kWh figure followed within ~40 chars by a pence figure
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s?kWh[^.<]{0,40}?(\d+(?:\.\d+)?)\s?p\b', full):
        kwh, pence = float(m.group(1)), float(m.group(2))
        if pence < 1000 and abs(kwh*26.11 - pence) > 2.5 and abs(kwh*7.33 - pence) > 1.5:
            issues.append(f"arithmetic? {kwh}kWh -> {pence}p (expect ~{kwh*26.11:.0f}p elec)")
    return issues or ["CLEAN"]

CRIT_SYS = "You are a sceptical UK energy fact-checker. Be terse."
def critique(art):
    u = ("Fact-check this UK energy article JSON. List up to 4 CONCRETE problems: implausible wattage, "
         "wrong arithmetic, factually wrong claim, or unsupported statistic. If genuinely fine, reply exactly CLEAN.\n\n"
         + json.dumps({"title": art["title"], "sections": art["sections"], "faq": art["faq"]}, ensure_ascii=False))
    try:
        return ds("deepseek-v4-pro", CRIT_SYS, u, max_tokens=600, temp=0.2).strip()
    except Exception as e:
        return f"(critique failed: {e})"

def main():
    report = [f"DeepSeek batch report  ({len(TOPICS)} articles)\n" + "="*60]
    for slug, title, hint in TOPICS:
        line = f"\n### {slug}"
        try:
            raw = ds("deepseek-v4-flash", GEN_SYS, gen_user(slug, title, hint), json_mode=True)
            art = json.loads(raw)
            json.dump(art, open(os.path.join(OUT, slug+".json"), "w"), indent=1, ensure_ascii=False)
            h = harness(art)
            c = critique(art)
            wc = len(re.sub(r"<[^>]+>"," "," ".join(s["html"] for s in art["sections"])).split())
            line += f"  ({wc} words)\n  harness: {h}\n  pro-critique: {c}"
        except Exception as e:
            line += f"  GENERATION FAILED: {e}"
        report.append(line)
        print(line, flush=True)
    rep = "\n".join(report)
    open(os.path.join(ROOT, ".flagship", "ds_batch_report.txt"), "w").write(rep)
    print("\nDONE -> .flagship/ds_batch_report.txt")

if __name__ == "__main__":
    main()
