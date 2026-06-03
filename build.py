#!/usr/bin/env python3
"""Static builder for Power Saving Guide. No dependencies: `python3 build.py`
writes the finished HTML, sitemap.xml, robots.txt and the IndexNow key into the
repo root. Content lives in the PAGES dict; add a page = one entry."""

import html
from datetime import date

SITE = "Power Saving Guide"
BASE = "https://powersavingguide.com"
YEAR = date.today().year
LAUNCH = "2026-06-03"
INDEXNOW_KEY = "a3f1c9e74b8d42a6915e0c7d2f6b8a41"

ANALYTICS = (
    '<script data-goatcounter="https://stats.powersavingguide.com/count" '
    'async src="//stats.powersavingguide.com/count.js"></script>'
)

NAV = [
    ("index", "Home"),
    ("electricity", "Electricity"),
    ("heating", "Heating & gas"),
    ("driving", "Fuel & driving"),
    ("appliance-running-cost", "Cost calculator"),
    ("guides", "Guides"),
    ("about", "About"),
]


def nav_html(active):
    out = []
    for slug, label in NAV:
        href = "index.html" if slug == "index" else f"{slug}.html"
        cls = ' class="active"' if slug == active else ""
        out.append(f'<li><a href="{href}"{cls}>{html.escape(label)}</a></li>')
    return "\n        ".join(out)


def page(slug, title, description, body, active=None):
    import json as _json
    full_title = title if slug == "index" else f"{title} | {SITE}"
    active = active or slug
    url = BASE + ("/" if slug == "index" else f"/{slug}.html")
    ogtype = "website" if slug == "index" else "article"
    if slug == "index":
        ld = {"@context": "https://schema.org", "@type": "WebSite",
              "name": SITE, "url": BASE + "/", "description": description}
    else:
        ld = {"@context": "https://schema.org", "@type": "Article",
              "headline": title, "description": description,
              "datePublished": LAUNCH, "dateModified": date.today().isoformat(),
              "inLanguage": "en-GB", "mainEntityOfPage": url,
              "author": {"@type": "Organization", "name": SITE},
              "publisher": {"@type": "Organization", "name": SITE}}
    ld = _json.dumps(ld, ensure_ascii=False).replace("<", "\\u003c")
    meta = f'''<link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <meta property="og:site_name" content="{SITE}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{ld}</script>'''
    if slug == "index":
        header = ""
    else:
        header = f'''
  <header class="page-head"><div class="wrap"><h1>{html.escape(title)}</h1></div></header>'''
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  {meta}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"></noscript>
  {ANALYTICS}
</head>
<body>
  <nav class="nav--bar"><div class="wrap nav-inner">
    <a class="brand" href="index.html">Power Saving Guide</a>
    <input type="checkbox" id="nt" class="navtoggle">
    <label for="nt" class="navburger" aria-label="Menu">≡</label>
    <ul>
        {nav_html(active)}
    </ul>
  </div></nav>
{header}
  <main>
{body}
  </main>
  <footer class="footer"><div class="wrap">
    <p class="foot-brand">Power Saving Guide</p>
    <p>A practical, independent guide to cutting your electricity, gas and fuel bills. Plain advice, no gadgets to buy.</p>
    <p class="foot-links"><a href="electricity.html">Electricity</a> · <a href="heating.html">Heating &amp; gas</a> · <a href="driving.html">Fuel &amp; driving</a> · <a href="appliance-running-cost.html">Cost calculator</a> · <a href="guides.html">Guides</a> · <a href="about.html">About</a> · <a href="privacy.html">Privacy</a></p>
    <p class="copy">&copy; <span>{YEAR}</span> {SITE}. Figures are worked examples; check your own tariff and meter. Cookieless analytics, see the <a href="privacy.html">privacy page</a>.</p>
  </div></footer>
</body>
</html>
'''


PAGES = {}

PAGES["index"] = dict(
    title="Cut your electricity, gas and fuel bills",
    description="Power Saving Guide is a practical, independent guide to using less energy at home and on the road: where your money goes, what actually works, and tools to do the sums.",
    body='''
  <section class="hero">
    <div class="wrap hero-inner">
      <p class="eyebrow">Practical, independent, no gadgets to sell</p>
      <h1>Use less. Pay less. Without the hair shirt.</h1>
      <p class="lede">Most household energy is spent in a handful of places, and most of the savings come from a handful of changes. This is a plain guide to which ones are worth the bother, backed by tools to work out what things actually cost you.</p>
      <p><a class="cta" href="appliance-running-cost.html">Work out a running cost</a> <a class="cta cta--ghost" href="electricity.html">Where the money goes</a></p>
    </div>
  </section>
  <section class="section"><div class="wrap">
    <div class="grid-cards">
      <a class="tile" href="electricity.html"><h2>Electricity</h2><p>The biggest users in the home, standby waste, lighting, and the quick wins that move the meter.</p></a>
      <a class="tile" href="heating.html"><h2>Heating &amp; gas</h2><p>Usually the largest bill of all. Thermostats, draughts, insulation and getting more from the boiler.</p></a>
      <a class="tile" href="driving.html"><h2>Fuel &amp; driving</h2><p>How driving style, tyres and a few habits change what you spend at the pump.</p></a>
      <a class="tile" href="appliance-running-cost.html"><h2>Cost calculator</h2><p>Enter an appliance's watts and how long it runs, and see the cost per use, per day and per year.</p></a>
      <a class="tile" href="guides.html"><h2>Guides</h2><p>Single-topic, practical guides that go a level deeper than the section pages.</p></a>
      <a class="tile" href="about.html"><h2>About</h2><p>Why this exists, and the one rule behind every page: spend effort where the energy actually goes.</p></a>
    </div>
  </div></section>
  <section class="section alt"><div class="wrap prose">
    <h2>The one idea worth keeping</h2>
    <p>If you take a single thing from this site, take this: chase the big users, not the small ones. Switching off a phone charger saves pennies a year, while turning the thermostat down by a degree or fixing draughts saves real money. A surprising amount of energy advice has you fussing over the trivial while the expensive stuff runs on unquestioned. The <a href="appliance-running-cost.html">cost calculator</a> exists to show you which is which, in your own money.</p>
  </div></section>
''',
)

PAGES["appliance-running-cost"] = dict(
    title="Appliance running cost calculator",
    description="Work out what any appliance costs to run: enter its wattage, how long it runs and your price per kWh, and get the cost per use, per day and per year in your own currency.",
    active="appliance-running-cost",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Enter an appliance's power in watts, how long it runs and what you pay per unit (kWh), and this works out what it costs you per use, per day and per year. Everything happens in your browser; nothing is saved or sent.</p>
    <style>
      .calc label{display:block;font-weight:600;color:var(--ink-strong);margin:14px 0 5px}
      .calc input,.calc select{width:100%;max-width:340px;padding:10px 12px;border:1px solid var(--line);border-radius:9px;font-size:1rem;font-family:inherit;background:#fff}
      .calc .row{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:520px}
      .calc button{margin-top:20px;background:var(--accent);color:#10243a;border:0;border-radius:999px;padding:13px 28px;font-weight:700;font-size:1rem;cursor:pointer}
      .calc button:hover{filter:brightness(1.05)}
      #res{display:none;margin-top:26px;border:1px solid var(--line);border-radius:14px;padding:20px;background:#fff}
      #res .big{font-size:2.1rem;font-weight:700;color:var(--ink-strong);line-height:1.1}
      #res .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:8px}
      #res .b{text-align:center;border:1px solid var(--line);border-radius:12px;padding:14px 8px}
      #res .b .n{font-size:1.5rem;font-weight:700;color:var(--ink-strong)}
      #res .b .l{font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
    </style>
    <div class="calc">
      <div class="row">
        <div><label for="w">Power (watts)</label><input id="w" type="number" min="0" value="2000" inputmode="numeric"></div>
        <div><label for="price">Price per kWh (your currency)</label><input id="price" type="number" min="0" step="0.01" value="0.30" inputmode="decimal"></div>
      </div>
      <div class="row">
        <div><label for="hrs">Hours each time it runs</label><input id="hrs" type="number" min="0" step="0.1" value="1" inputmode="decimal"></div>
        <div><label for="days">Times per week</label><input id="days" type="number" min="0" step="1" value="7" inputmode="numeric"></div>
      </div>
      <button id="go">Work it out</button>
    </div>
    <div id="res">
      <p>This appliance costs about <span class="big" id="perUse"></span> each time you run it.</p>
      <div class="grid">
        <div class="b"><div class="n" id="perWeek"></div><div class="l">per week</div></div>
        <div class="b"><div class="n" id="perYear"></div><div class="l">per year</div></div>
        <div class="b"><div class="n" id="kwhYr"></div><div class="l">kWh per year</div></div>
      </div>
      <p class="note" id="tip" style="margin-top:14px;color:var(--muted);font-size:.9rem"></p>
    </div>
    <p style="margin-top:24px">Not sure of an appliance's wattage? It is usually printed on a label on the back or base, or in the manual. A plug-in energy monitor measures it directly and pays for itself quickly if you have a few mystery devices. For where the big users hide, see <a href="electricity.html">electricity in the home</a>.</p>
  </div></section>
  <script>
  (function(){
    var $=function(i){return document.getElementById(i);};
    function money(x){return x.toFixed(2);}
    $("go").addEventListener("click",function(){
      var w=parseFloat($("w").value),p=parseFloat($("price").value),h=parseFloat($("hrs").value),d=parseFloat($("days").value);
      if([w,p,h,d].some(function(x){return isNaN(x)||x<0;}))return;
      var kwhUse=w/1000*h;
      var perUse=kwhUse*p;
      var perYear=perUse*d*52;
      var kwhYr=kwhUse*d*52;
      $("perUse").textContent=money(perUse);
      $("perWeek").textContent=money(perUse*d);
      $("perYear").textContent=money(perYear);
      $("kwhYr").textContent=Math.round(kwhYr).toLocaleString();
      var tip="";
      if(perYear>100)tip="That is a meaningful chunk of a bill. Worth asking whether it can run less, run cooler, or be replaced with something more efficient.";
      else if(perYear<10)tip="This is a minnow. Switching it off religiously will save you very little; spend your effort on the bigger users.";
      else tip="A middling cost. Small habit changes here add up over a year without much sacrifice.";
      $("tip").textContent=tip;
      $("res").style.display="block";$("res").scrollIntoView({behavior:"smooth",block:"nearest"});
    });
  })();
  </script>
''',
)

PAGES["electricity"] = dict(
    title="Electricity in the home: where it goes",
    description="What uses the most electricity in a typical home, the truth about standby power, lighting, and the changes that actually lower an electricity bill.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Electricity bills feel mysterious, but the spending is not evenly spread. A few things dominate, and knowing which they are tells you where effort is repaid and where it is wasted.</p>
    <h2>The big users</h2>
    <p>Anything that makes heat is expensive to run, because heating is energy-hungry. Electric heating, immersion water heaters, tumble dryers, ovens, kettles and electric showers sit at the top of the list. After those come the appliances that run constantly: the fridge and freezer, which are modest moment to moment but never switch off, so they add up. Everything else, the telly, the laptop, the lights, is usually small by comparison.</p>
    <h2>Standby is real but small</h2>
    <p>Devices left on standby do draw power, and over a year a houseful of them adds up to a noticeable, if not enormous, sum. Switching things off at the wall is worth doing, especially older equipment and anything with a transformer that stays warm. Just keep it in proportion: standby is worth a tidy-up, not an obsession, while the dryer and the heating are where the real money is.</p>
    <h2>Lighting, the easy win</h2>
    <p>If you still have halogen or older bulbs, swapping to LED is close to free money. An LED uses a fraction of the electricity for the same light and lasts for years, so the swap pays for itself quickly and then keeps paying. It is one of the few changes that is genuinely fit and forget.</p>
    <h2>Work out your own numbers</h2>
    <p>Rather than trust rules of thumb, put your own appliances through the <a href="appliance-running-cost.html">running cost calculator</a>. Seeing that the tumble dryer costs more in a year than the standby of every gadget combined is the moment the priorities click into place.</p>
  </div></section>
''',
)

PAGES["heating"] = dict(
    title="Heating and gas: the biggest bill",
    description="Practical ways to cut heating and gas costs: thermostat settings, draught-proofing, insulation, radiator habits and getting more from your boiler, in order of value.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">For most homes, heating is the largest energy cost by a wide margin, often more than everything electrical put together. That also makes it where the biggest savings live.</p>
    <h2>Turn it down a touch</h2>
    <p>The single cheapest saving is the thermostat. Dropping the temperature by one degree cuts a noticeable slice off a heating bill and is barely perceptible day to day, especially with a jumper on. Heating rooms you are not using, and heating the house while everyone is out or asleep, are the other easy wins; a timer or a smart thermostat handles both without you thinking about it.</p>
    <h2>Stop the heat escaping</h2>
    <p>Heat you have paid for leaking straight out is the real waste. Draught-proofing doors, windows, letterboxes and unused chimneys is cheap and quick and makes a cold house feel warmer at once. Insulation, lofts first, then walls, costs more up front but is the highest-value improvement most homes can make, paying back over a few winters and then saving for decades.</p>
    <h2>Get more from the boiler</h2>
    <p>A few free tweaks help a gas boiler run more efficiently: bleeding radiators so they heat fully, keeping them clear of furniture, and on a condensing combi, turning the flow temperature down so it actually condenses. None of these costs anything, and together they squeeze more warmth from the same gas.</p>
    <h2>In order of value</h2>
    <p>Roughly: turn it down and time it, then stop the draughts, then insulate, then fine-tune the boiler. Do them in that order and you spend the least for the most, rather than splashing out on kit before the cheap basics are done.</p>
  </div></section>
''',
)

PAGES["driving"] = dict(
    title="Fuel and driving: spending less at the pump",
    description="How driving style, tyre pressure, weight and journey planning change your fuel use, and the habits that cut the cost of running a car without buying a new one.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">You cannot change the price of fuel, but you have more control over how much you burn than most people realise. The car matters, but how you drive it matters nearly as much.</p>
    <h2>Smooth wins</h2>
    <p>Hard acceleration and late braking pour fuel away. Reading the road ahead, easing off early and keeping a steady pace use far less, and on a motorway, sitting at a sensible speed rather than the limit makes a real difference because drag climbs steeply with speed. None of this means crawling; it means driving smoothly rather than in bursts.</p>
    <h2>Check the easy things</h2>
    <p>Under-inflated tyres increase rolling resistance and quietly cost you fuel and tyre life, so check the pressures monthly. Clear out the boot, since carrying weight you do not need costs energy to haul, and take off roof boxes and racks when they are not in use, because the drag they add is surprising.</p>
    <h2>Idling and short hops</h2>
    <p>An idling engine does zero miles to the gallon, so switch off in long waits. Short cold journeys are the least efficient miles a car does, as the engine never warms up, so combining errands into one trip, or walking the very short ones, saves more than it seems.</p>
    <h2>The honest limit</h2>
    <p>These habits trim a useful slice off a fuel bill, commonly into the low tens of per cent for a heavy-footed driver who reforms. They will not rival the saving from simply driving less, so where a journey can be shared, cycled or skipped, that is the biggest lever of all.</p>
  </div></section>
''',
)

PAGES["about"] = dict(
    title="About Power Saving Guide",
    description="About Power Saving Guide: an independent, plain-spoken guide to cutting energy bills, and the long-delayed sequel to a 2004 idea.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Power Saving Guide is an independent guide to using less electricity, gas and fuel, written plainly and with nothing to sell you.</p>
    <p>It has an embarrassingly long gestation. The idea started in 2004 as a little ebook about saving energy, meant to be sold to people on eBay, and then, as ideas do, it sat in a drawer for twenty years. The advice has only become more relevant since, and the format is better as a free, searchable site than a PDF anyway.</p>
    <p>The guiding principle is the one on the home page: spend your effort where the energy actually goes. A great deal of energy advice fixates on trivial savings while the expensive things run unquestioned. Everything here tries to keep the proportions honest, which is why the <a href="appliance-running-cost.html">calculator</a> works in real money rather than vague encouragement.</p>
    <p>Figures on the site are worked examples to illustrate the sums; your own tariff, climate and habits decide the real numbers. Corrections and suggestions are welcome.</p>
  </div></section>
''',
)

PAGES["privacy"] = dict(
    title="Privacy",
    description="Power Saving Guide's privacy approach: cookieless, self-hosted analytics, no tracking, and the calculators run entirely in your browser.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The short version: no tracking cookies, no data sold, and the calculators run entirely in your browser.</p>
    <h2>Analytics</h2>
    <p>To see which pages are read, the site uses a self-hosted, privacy-friendly analytics tool rather than handing your visit to a third party. It sets no cookies and does not track you across other sites; it records a page view with non-identifying details such as the page, the referring site and a broad country, and does not store your full IP address. Because nothing identifies you and no cookie is set, no consent banner is needed.</p>
    <h2>The calculators</h2>
    <p>Everything you type into the calculators stays in your browser. Nothing is sent to a server or saved anywhere.</p>
    <h2>Fonts and advertising</h2>
    <p>Pages load a typeface from Google Fonts, so your browser fetches font files from Google. The site may carry advertising in future to cover its costs; if it does, this page will be updated to describe exactly what that involves before any advertising appears.</p>
  </div></section>
''',
)


GUIDES_ORDER = []


def _guide_tile(slug):
    p = PAGES[slug]
    return (f'        <a class="tile" href="{slug}.html"><h2>{html.escape(p["title"])}</h2>'
            f'<p>{html.escape(p.get("blurb", p["description"]))}</p></a>')


PAGES["guides"] = dict(
    title="Guides",
    description="Practical, single-topic guides to saving energy at home and on the road, added regularly.",
    body='''
  <section class="section"><div class="wrap">
    <p class="lede">Single-topic guides that go a level deeper than the section pages. More are added regularly.</p>
    <div class="grid-cards">
''' + ("\n".join(_guide_tile(s) for s in GUIDES_ORDER) if GUIDES_ORDER else
       '      <a class="tile" href="electricity.html"><h2>Start with electricity</h2><p>While the dedicated guides grow, the section pages are the place to begin.</p></a>') + '''
    </div>
  </div></section>
''',
)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for slug, p in PAGES.items():
        out = page(slug, p["title"], p["description"], p["body"], p.get("active"))
        open(os.path.join(here, f"{slug}.html"), "w", encoding="utf-8").write(out)
    today = date.today().isoformat()
    urls = []
    for slug in PAGES:
        loc = BASE + ("/" if slug == "index" else f"/{slug}.html")
        prio = "1.0" if slug == "index" else "0.7"
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>")
    open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(here, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    open(os.path.join(here, INDEXNOW_KEY + ".txt"), "w", encoding="utf-8").write(INDEXNOW_KEY)
    print("built", len(PAGES), "pages + sitemap.xml + robots.txt + IndexNow key")


if __name__ == "__main__":
    main()
