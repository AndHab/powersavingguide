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


PAGES["loft-insulation"] = dict(
    title="Loft insulation: the best-value upgrade",
    description="Why loft insulation gives the biggest return of any home energy improvement, how much depth you need, what it costs and saves, how to lay it yourself, boarding for storage without crushing it, and the ventilation and damp pitfalls to avoid.",
    active="guides",
    blurb="Pound for pound the best home energy upgrade there is. How deep to go, how to lay it, and what it saves.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">If you do only one thing to a draughty, expensive house, make it the loft. Warm air rises, and in a home with little or no insulation above the ceiling a great deal of the heat you have paid for drifts straight up and out through the roof. Of every improvement available, topping up the loft returns the most warmth and the most money for the least outlay and effort, which is why every sensible list of energy jobs starts here.</p>

    <h2>Why the loft comes first</h2>
    <p>Around a quarter of the heat lost from an uninsulated house escapes through the roof, more than through any single wall and far more than through the windows everyone frets about. That alone would make it worth doing, but the loft has a second advantage that the walls and windows do not: it is cheap, it needs no specialist for a standard accessible loft, and it is quick. A roll of mineral wool, a craft knife and an afternoon is genuinely all a typical job takes. High heat loss meeting low cost is exactly the combination that makes something the best value in the house, and the loft is the clearest example of it.</p>

    <h2>Depth is what counts</h2>
    <p>The single number that matters is depth, because insulation works by trapping still air and the more thickness you have, the more it traps. Current guidance points to roughly 270mm of mineral wool, which is deeper than people expect, about the height of a house brick stood on end plus a bit. A great many lofts fall well short of this. Some have nothing at all; many have a thin layer laid decades ago that has since settled, compressed and lost much of its effect. A quick test is to look across the loft: if the tops of the joists are poking out above the insulation, you have nowhere near enough, since the joists themselves are usually only around 100mm deep.</p>
    <p>Topping a thin existing layer up to full depth is one of the most satisfying jobs going, because the difference is immediate. You lay the first layer between the joists and a second layer across them at right angles, which covers the joists themselves and stops them acting as cold bridges. Within a day or two of cold weather you notice the house holding its warmth for longer after the heating goes off, which is the whole point.</p>

    <h2>Doing it yourself</h2>
    <p>For an accessible loft this is firmly a job most people can do. Wear a mask, long sleeves and gloves, since mineral wool irritates skin and lungs, and work off boards laid across the joists rather than treading between them, where a foot can go through the ceiling below. Roll the first layer snugly between the joists without crushing it, then lay the second layer across the top. Cut it slightly oversize so it fills the space without gaps, as gaps are where the heat finds its way out. Take care around recessed downlights and any other heat source, leaving the clearance the fitting requires, and do not cover modern light fittings unless they are rated to be covered.</p>

    <h2>Boarding for storage without ruining it</h2>
    <p>The common mistake is to lay loft boards straight onto the joists for storage. Because full-depth insulation is far deeper than the joists, boarding directly on top squashes it flat, and crushed insulation loses much of its value, so you end up with a tidy storage deck and a cold house. The fix is raised loft legs, sometimes called boarding stilts, plastic or metal supports that lift the boards above the full depth of insulation and leave it uncompressed underneath. They cost a little more than boards alone and turn what would be a self-defeating job into one that keeps both the storage and the saving.</p>

    <h2>Ventilation and damp</h2>
    <p>A cold loft needs to breathe, and this is the detail that catches people out. The space above the insulation should stay ventilated through the gaps at the eaves, so that any moisture rising from the house below can escape rather than condensing on the cold roof timbers. Stuff insulation hard into the eaves and block that airflow and you risk trapping damp, which leads to mould and rot in the roof structure. Leave the eaves gaps clear, using eaves vents or baffles if needed to hold the insulation back from the very edge.</p>
    <p>One more placement point: insulate the loft floor, above the heated rooms, not the underside of the roof, unless you are deliberately creating a warm loft room. And do not insulate beneath the cold-water tank if you have one, since you want a little of the warmth from below to keep reaching it so it does not freeze in a hard winter. Insulate around and over the sides of the tank instead, and fit it an insulating jacket of its own.</p>

    <h2>What it saves</h2>
    <p>For a house going from little or no loft insulation up to full depth, this is typically one of the largest single savings on the heating bill available from any one measure, and because the materials are cheap the cost is usually repaid within a small number of winters and then keeps saving for the life of the house. Topping up an already-decent layer saves less, since the first inches do most of the work, but going from nothing to 270mm is transformative. Pair it with sealing the <a href="draught-proofing.html">draughts</a> and turning down the <a href="boiler-flow-temperature.html">boiler flow temperature</a> and you have done the three cheapest, highest-value heating jobs there are before spending serious money on anything.</p>
  </div></section>
''',
)

PAGES["draught-proofing"] = dict(
    title="Draught-proofing: the cheap heat you are losing",
    description="A room-by-room guide to draught-proofing a home: how to find the gaps, the cheap materials that seal doors, windows, floors, chimneys and loft hatches, what you must leave alone for ventilation, and why it makes a house feel warmer at a lower thermostat setting.",
    active="guides",
    blurb="Cheap, quick, and it makes a cold house feel warmer at once. How to find every gap and seal it properly.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Every draught is warm air you have paid to heat sliding out of the house, with cold air pulled in behind it to replace it. Sealing those gaps is among the cheapest jobs you can do, needs no skill, and is one of the few improvements you feel the same evening you finish it, because a room without draughts feels comfortable at a lower thermostat setting than a draughty one. That lower setting is where the saving quietly compounds, winter after winter.</p>

    <h2>First, find the draughts</h2>
    <p>You cannot seal what you have not found, and some of the worst gaps are not the obvious ones. On a cold, windy day, walk the house slowly with the back of a wet hand or, better, a lit candle or a stick of incense, and watch the flame or smoke. Where it pulls sideways or flickers, air is moving. Do this around door and window frames, along the bottom of skirting boards, at the loft hatch, around pipes coming through walls, at old vents and at the fireplace. The wet-hand method works too: bare skin feels moving air as a cool line even where you cannot see it.</p>

    <h2>Doors</h2>
    <p>External doors are usually the biggest single offender, and they leak in several places at once. Fit compression or brush draught strips around the frame so the door closes against a seal, a brush strip or weighted excluder along the bottom where the worst draught often is, a sprung flap or brush on the inside of the letterbox, and a cover over an unused keyhole. Internal doors to unheated spaces, an integral garage or an unheated porch, are worth sealing too. None of this is hard, and a complete door kit costs very little.</p>

    <h2>Windows</h2>
    <p>Openable windows leak around the opening edge, where self-adhesive foam or E-strip and P-strip rubber profiles seal the gap when the window shuts. Older sash windows are notorious draught sources and take a little more work, with brush strips in the runs and seals along the meeting rail, though the reward is large because they leak so much. Fixed panes that whistle around the frame can be sealed with a bead of frame sealant. For the cold radiating off the glass itself, which is a different problem from draughts, see <a href="secondary-glazing.html">secondary glazing</a> and <a href="curtains-for-warmth.html">curtains for warmth</a>.</p>

    <h2>Floors, skirting and service holes</h2>
    <p>In older houses with suspended timber floors, cold air rises straight up between the floorboards and along the gap where the boards meet the skirting. A flexible filler, a proprietary gap-filler strip, or simply a good rug takes the edge off, and the fuller treatment is on the <a href="underfloor-insulation.html">underfloor insulation</a> guide. Do not forget the small holes you never think about: where pipes and cables pass through external walls, behind kitchen units, around extractor ducting and waste pipes. A squirt of expanding foam or silicone seals each one in seconds, and together they add up.</p>

    <h2>Chimneys and the loft hatch</h2>
    <p>An open, unused chimney is effectively a hole in the roof through which warm air streams out around the clock; it can be one of the largest draughts in the whole house. A chimney balloon, an inflatable plug, or a sheep's-wool chimney draught excluder stops it, while still leaving the small amount of ventilation a flue needs to stay dry. Remember to remove it before ever lighting a fire. The loft hatch is another easily missed gap: fit draught stripping around its edge and a scrap of insulation to its back, so you are not letting heat pour up into the cold loft you took the trouble to <a href="loft-insulation.html">insulate</a>.</p>

    <h2>What you must leave alone</h2>
    <p>This is the part to get right, because over-sealing causes its own problems. A house needs a controlled amount of fresh air to carry away the moisture that cooking, washing and breathing put into it; block every route and that moisture condenses on cold surfaces and grows mould. So leave airbricks clear, leave the trickle vents in window frames open, and never seal the extractor fans in the kitchen and bathroom or the air supply to a fuel-burning appliance like an open fire or certain gas heaters. The aim is to stop the uncontrolled, wasteful draughts, not to make the house airtight.</p>

    <h2>Why it is worth doing first</h2>
    <p>Draught-proofing rarely tops the table for raw heat saved, since the gaps are small individually, but it wins on value because it is so cheap and so fast. The whole house can usually be done over a weekend for the price of a couple of takeaways, the payback is quick, and the gain in comfort is out of all proportion to the spend. Most importantly, a sealed room lets you sit comfortably with the thermostat turned down a notch, and as the <a href="thermostat-settings.html">thermostat settings</a> guide explains, that lower setting is where the real, repeating saving lives. Do this alongside the <a href="loft-insulation.html">loft</a> and a turned-down <a href="boiler-flow-temperature.html">boiler flow temperature</a> and you have the three best-value heating jobs done for very little money.</p>
  </div></section>
''',
)

PAGES["tumble-dryer-cost"] = dict(
    title="The tumble dryer: your priciest habit",
    description="Why the tumble dryer is one of the most expensive appliances to run, how much a typical load costs, and the cheaper ways to dry clothes without one.",
    active="guides",
    blurb="One of the most expensive things you can plug in. What a load really costs, and the cheaper ways to dry.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Anything that makes heat is expensive to run, and a tumble dryer makes a lot of it. For households that dry every load by machine, it is often one of the largest single lines on the electricity bill, and one of the easiest to trim.</p>
    <h2>Why it costs so much</h2>
    <p>A conventional vented or condenser dryer pulls a couple of kilowatts and runs for an hour or more per load. Run the numbers through the <a href="appliance-running-cost.html">cost calculator</a> and a daily load adds up to a serious annual figure, often rivalling the fridge-freezer despite running a fraction of the hours. The heat is the expense.</p>
    <h2>Cheaper ways to dry</h2>
    <p>The cheapest dryer is a washing line or an airer, which cost nothing to run. Drying outdoors when the weather allows, or on an airer in a well-ventilated room, removes the cost entirely. Spinning clothes at a higher speed in the washing machine first wrings out more water, so whatever drying you do afterwards is shorter. Even half your loads air-dried roughly halves the dryer's bill.</p>
    <h2>If you must use the machine</h2>
    <p>Dry full loads rather than dribs and drabs, since the machine uses similar energy either way. Clean the lint filter every time, because a clogged filter makes the dryer work harder and longer. Use the moisture-sensor or eco programme if the machine has one, so it stops when the clothes are dry rather than running to a fixed timer.</p>
    <h2>The efficient option</h2>
    <p>If you dry a great deal and are replacing the machine anyway, a heat-pump dryer uses markedly less electricity than a conventional one, because it recycles its own warm air rather than heating fresh air and venting it. It costs more to buy and dries a little slower, but for a heavy user the running-cost saving is real over the life of the machine.</p>
  </div></section>
''',
)

PAGES["fridge-freezer-efficiency"] = dict(
    title="Getting your fridge and freezer to run cheaper",
    description="How to cut the running cost of a fridge and freezer: ideal temperatures, defrosting, door seals, placement and when an old one is worth replacing.",
    active="guides",
    blurb="They never switch off, so small tweaks add up all year. Temperatures, seals, frost and placement.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A fridge-freezer is modest moment to moment, but it is the one appliance that never switches off, so it quietly runs up a year-round bill. Small improvements to how it works repay themselves every single day.</p>
    <h2>Get the temperatures right</h2>
    <p>Colder than necessary just wastes energy. A fridge sits happily around three to five degrees and a freezer around minus eighteen; many people run them colder than that out of habit. Nudging an over-cold fridge up a degree or two saves energy without any risk to the food, so check the dial against a cheap fridge thermometer.</p>
    <h2>Defrost and clear the coils</h2>
    <p>Frost is an insulator in the wrong place: a freezer caked in ice has to work harder to stay cold, so defrost it before the build-up gets thick. At the back or underneath, the condenser coils gather dust that stops them shedding heat efficiently; a gentle vacuum once or twice a year keeps them clear and the motor running less.</p>
    <h2>Seals and placement</h2>
    <p>A perished door seal lets cold leak out and the motor run constantly. Test it by closing the door on a sheet of paper: if it slides out easily, the seal needs replacing. Placement matters too, since an appliance jammed next to the oven or in a sunny spot has to fight the heat. Give it a few centimetres of air around the back and keep it out of direct warmth.</p>
    <h2>Full, but not stuffed</h2>
    <p>A reasonably full freezer holds its cold better than an empty one, as the frozen mass acts as a buffer, so it cycles on less. A fridge, on the other hand, wants air to circulate, so do not cram it. And when it comes to replacing a very old unit, a fridge-freezer from twenty years ago can use several times the electricity of a modern efficient one, so the running-cost saving alone can justify the swap.</p>
  </div></section>
''',
)

PAGES["hypermiling"] = dict(
    title="Hypermiling: squeezing miles from a tank",
    description="A practical guide to hypermiling: the driving techniques that genuinely cut fuel use, which ones are worth it, which are myths, and how to do it without holding up traffic or driving unsafely.",
    active="guides",
    blurb="The techniques that genuinely stretch a tank, the ones that are myths, and how to do it safely.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Hypermiling is the art of driving to use as little fuel as possible. Taken sensibly it can cut a fuel bill by a useful margin; taken to extremes it annoys other drivers and is not worth the risk. Here is the worthwhile middle.</p>
    <h2>The techniques that work</h2>
    <p>The biggest gains come from anticipation. Reading the road far ahead lets you lift off early and coast towards a red light or a queue rather than accelerating up to it and braking hard, which throws away the fuel you just spent. Accelerate gently but purposefully, get into the highest sensible gear early, and hold a steady speed rather than surging and slowing. On the motorway, easing off the top of your speed makes a real difference, because the air resistance you fight rises steeply with speed.</p>
    <h2>Keep the car helping you</h2>
    <p>Correctly inflated tyres roll more easily, so check them monthly. Strip out weight you are carting around for no reason, and take roof bars and boxes off when they are not needed, since the drag they add is larger than people expect. Keep up with servicing, because a clogged air filter or dragging brake quietly costs fuel.</p>
    <h2>Myths and things not worth it</h2>
    <p>Coasting in neutral down hills saves little on a modern injection engine, which already cuts fuel on the overrun when you simply lift off in gear, and it removes engine braking, so it is not worth the safety trade. Drafting close behind lorries saves fuel and is dangerous, so do not. Switching the engine off at every brief stop helps in long waits but is pointless and annoying at a junction.</p>
    <h2>Do not become a hazard</h2>
    <p>The one rule that overrides the rest: never let saving fuel make you a nuisance or a danger. Crawling far below the flow of traffic, braking late to coast, or hovering near other vehicles undoes the point. Smooth, anticipatory, steady driving saves fuel and is also simply good driving. The general fuel advice is on the <a href="driving.html">fuel and driving</a> page.</p>
  </div></section>
''',
)

PAGES["led-lighting"] = dict(
    title="Switching to LED lighting",
    description="Why LED bulbs are an easy energy win, how much they save over halogen and old bulbs, choosing brightness and colour, and the few places to take care.",
    active="guides",
    blurb="Close to free money if you still have halogens. What LEDs save and how to choose them.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">If any energy saving deserves the phrase fit and forget, it is LED lighting. The bulbs sip electricity, last for years, and the swap pays for itself quickly and then keeps paying with no further effort.</p>
    <h2>The saving</h2>
    <p>An LED produces the same light as an old incandescent or halogen bulb for a fraction of the electricity, often around a tenth to a fifth. Lighting is not usually the biggest line on a bill, but if you still have halogen spotlights, which are notorious energy hogs, replacing a roomful makes a visible dent, and the bulbs last so long that you rarely change one again.</p>
    <h2>Choosing them</h2>
    <p>Ignore watts and look at lumens, which measure actual brightness; roughly, 800 lumens replaces an old 60-watt bulb. Colour temperature is a matter of taste: warm white around 2700K for a cosy living room, cooler white for a kitchen or workspace. Check the fitting matches, and if the bulb is on a dimmer, buy one marked dimmable, since a non-dimmable LED on a dimmer flickers or buzzes.</p>
    <h2>The few cautions</h2>
    <p>Very cheap bulbs can be a false economy, dying early or giving poor, harsh light, so middling quality is worth it for something that should last years. Enclosed light fittings trap heat and shorten an LED's life unless the bulb is rated for enclosed use. And dispose of old fluorescent tubes properly, as they contain a little mercury; ordinary LEDs do not.</p>
    <h2>Just do it gradually</h2>
    <p>There is no need to rip out every working bulb at once. Replace the ones you use most first, the kitchen and living room, then swap the rest as they fail. Within a year the house is done, the lighting bill has shrunk, and you have stopped buying bulbs.</p>
  </div></section>
''',
)

PAGES["understanding-energy-bill"] = dict(
    title="Understanding your energy bill",
    description="How to read an energy bill: what a kWh is, the difference between the unit rate and the standing charge, estimated versus actual readings, and how to spot what is really costing you.",
    active="guides",
    blurb="kWh, unit rate, standing charge, estimated readings: how to actually read the bill and find the cost.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Energy bills are written to be paid, not understood, but the structure is simple once you know the parts. Read it properly and you can see where the money goes and whether you are even being charged for what you used.</p>
    <h2>The kilowatt-hour</h2>
    <p>Everything is billed in kilowatt-hours, kWh, which is the unit of energy. One kWh is a thousand watts running for an hour: a one-bar electric fire for an hour, or a 100-watt item for ten hours. Your meter counts kWh, and that is what you pay for. Once you think in kWh, the running cost of anything is just its power times the hours it runs times the price per kWh, which is exactly what the <a href="appliance-running-cost.html">calculator</a> does.</p>
    <h2>Unit rate and standing charge</h2>
    <p>A bill has two charges. The unit rate is the price per kWh, what you pay for energy actually used. The standing charge is a fixed daily fee you pay regardless of usage, covering the cost of being connected. This matters: if you use very little, the standing charge can be most of your bill, so cutting usage has limits, and a tariff with a lower standing charge may suit a light user better.</p>
    <h2>Estimated versus actual</h2>
    <p>If the bill says estimated, the supplier has guessed your usage rather than read the meter, and the guess can be well out. Submit your own meter readings, or fit a smart meter, so you are billed for what you actually used rather than a pessimistic estimate that leaves you in credit or a cheery one that builds a debt.</p>
    <h2>Finding the cost</h2>
    <p>With the unit rate in hand, you can finally answer where the money goes. Note your meter before and after running something for a known time, and you have measured it directly. More simply, the heat-making appliances and the always-on ones are the usual culprits, as the <a href="electricity.html">electricity</a> and <a href="heating.html">heating</a> pages explain.</p>
  </div></section>
''',
)

PAGES["switching-suppliers"] = dict(
    title="How to compare and switch energy suppliers",
    description="A plain guide to comparing energy tariffs and switching supplier: what to look at beyond the headline rate, fixed versus variable, how switching works, and what does not change.",
    active="guides",
    blurb="What to look at beyond the headline price, fixed vs variable, and how switching actually works.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Switching supplier or tariff is one of the few savings that needs no lifestyle change at all, just a bit of admin. The trick is comparing the right things, because the headline price per unit is only part of the story.</p>
    <h2>Look past the unit rate</h2>
    <p>A low price per kWh can hide a high standing charge, and the cheapest deal for a heavy user is not the cheapest for a light one. Compare the total estimated annual cost for your own usage, not the unit rate alone. To do that you need your actual annual consumption in kWh, which is on a recent bill or your online account; with that figure a comparison is meaningful rather than guesswork.</p>
    <h2>Fixed or variable</h2>
    <p>A fixed tariff locks your unit rate for a term, giving certainty and protection if prices rise, but usually with an exit fee if you leave early. A variable tariff moves with the market, cheaper when prices fall and painful when they climb. Which is better depends on where prices are heading, which nobody truly knows, so it comes down to whether you value certainty or flexibility.</p>
    <h2>How switching works</h2>
    <p>Switching is mostly painless and behind the scenes. Your supply does not get cut off, no engineer visits, and the same gas and electricity flow through the same pipes and wires; only the company billing you changes. You provide a meter reading on the switch date so the old and new suppliers split the account correctly, and the process typically completes within a couple of weeks.</p>
    <h2>Use a genuine comparison</h2>
    <p>To see real, current deals, use a reputable comparison service that lists the whole market and shows total annual costs for your usage. This site does not publish a live tariff table, because prices change constantly and vary by region, and a stale table would be worse than none. Treat any comparison as a snapshot, and recheck when your fixed term ends rather than letting it roll onto a default rate, which is rarely the best.</p>
  </div></section>
''',
)

PAGES["thermostat-settings"] = dict(
    title="Thermostat settings that save money",
    description="How to set and use a heating thermostat to cut costs: the right temperature, timing, room thermostats versus radiator valves, and the truth about leaving heating on low all day.",
    active="guides",
    blurb="The right temperature, smart timing, and the truth about 'leaving it on low all day'.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The thermostat is the cheapest energy-saving tool in the house, because it costs nothing and controls the biggest bill. Used well it saves real money; used out of habit it quietly overspends.</p>
    <h2>The right temperature</h2>
    <p>Every degree counts. Dropping the thermostat by one degree trims a noticeable slice off a heating bill and is barely perceptible with a jumper on. A living room is comfortable for most people somewhere in the high teens to around twenty degrees, and bedrooms can be cooler. Set it to the lowest temperature that is genuinely comfortable, not the highest you can afford.</p>
    <h2>Time it to your life</h2>
    <p>There is no sense heating an empty house or a sleeping one to daytime warmth. Use the programmer or a smart thermostat to bring the heating up shortly before you get up and home, and let it drop back when you are out or in bed. This timing, matching the heat to when you are actually there to feel it, is where a lot of the saving hides.</p>
    <h2>Room thermostat and radiator valves together</h2>
    <p>The room thermostat controls the whole system; thermostatic radiator valves control each room. Use both: set the main thermostat for your main living space, and turn the valves down in rooms you rarely use so you are not heating spare bedrooms to the same level. This zoning means you heat where you live, not the whole house equally.</p>
    <h2>On low all day, or off?</h2>
    <p>A persistent myth says it is cheaper to leave the heating on low all day than to heat the house when you need it. For almost everyone it is not: a well-timed system that heats the house when occupied and lets it cool when empty uses less than one trickling away around the clock. Heat a house you are in, not one you are not.</p>
  </div></section>
''',
)

PAGES["hot-water-savings"] = dict(
    title="Cutting the cost of hot water",
    description="How to spend less heating water: cylinder versus combi, the right hot-water temperature, shorter showers, insulating the tank and pipes, and avoiding the expensive immersion heater.",
    active="guides",
    blurb="After heating the rooms, heating water is often the next biggest cost. Practical ways to trim it.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Heating water is usually the second largest energy use in a home after heating the rooms. Because so much of it runs on habit, there is plenty to trim without anyone going without a hot shower.</p>
    <h2>Showers, not baths</h2>
    <p>A bath uses a lot of hot water; a reasonable shower uses far less. The exception is a long power shower, which can use as much as a bath, so the saving comes from keeping showers brisk rather than the format alone. Cutting a few minutes off a daily shower, across a household, adds up to a meaningful amount of water heated over a year.</p>
    <h2>Set the right temperature</h2>
    <p>A hot-water cylinder set far hotter than you ever use it just loses more heat standing there, and you end up mixing in cold at the tap anyway. Around sixty degrees is the usual recommendation, hot enough for safety against bacteria but not needlessly scalding. Combi boilers heat on demand, so the equivalent is not running the hot tap longer than you need.</p>
    <h2>Insulate the tank and pipes</h2>
    <p>If you have a hot-water cylinder, a proper insulating jacket is one of the cheapest savings going: it stops the heat you have paid for leaking away while the tank sits there. Lagging the exposed hot-water pipes nearby helps too, keeping the water hotter for longer between the tank and the tap.</p>
    <h2>Mind the immersion heater</h2>
    <p>An electric immersion heater is an expensive way to make hot water, because it heats with electricity rather than gas. If yours is a backup to a gas boiler, make sure it is not quietly left switched on, topping up the tank with pricey electricity when the boiler would do the job for less. Run the figures through the <a href="appliance-running-cost.html">calculator</a> and the immersion's appetite is obvious.</p>
  </div></section>
''',
)

PAGES["cavity-wall-insulation"] = dict(
    title="Cavity wall insulation: is it right for your house?",
    description="What cavity wall insulation is, which houses can have it, what it saves, the damp concerns that get talked about, and how to tell whether your walls are already done.",
    active="guides",
    blurb="If your house has cavity walls and they are empty, filling them is one of the larger savings going.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Walls lose more heat than any other part of most houses simply because there is so much of them. Where a home has a hollow cavity between two skins of brick, filling that gap is among the higher-value jobs you can do, and on many houses it is already half the price it looks thanks to grant schemes.</p>
    <h2>Does your house even have a cavity?</h2>
    <p>Homes built from roughly the 1920s onwards tend to have two leaves of masonry with a gap between them; older solid-wall houses do not, and need a different approach covered on the <a href="solid-wall-insulation.html">solid wall</a> guide. A quick test is the brick pattern: an unbroken run of long bricks usually means a cavity, while a regular pattern of short brick ends shows a solid wall. The wall thickness at a window or door reveal is another clue, as a cavity wall is noticeably thicker than a single-skin one.</p>
    <h2>What it saves and what it costs</h2>
    <p>An empty cavity lets warmth pass straight through; injecting mineral wool, beads or foam through small holes in the mortar slows that loss considerably. For a typical semi the annual saving is one of the better ones available from a single measure, and the work takes a few hours with no mess indoors. The holes are made good afterwards and are barely visible once the mortar weathers in.</p>
    <h2>The damp question</h2>
    <p>You will hear stories of cavity insulation causing damp, and they are not pure myth: in exposed, wind-driven-rain locations, or where the original installation was poor, moisture has occasionally bridged the gap. The answer is not to avoid it but to use a reputable installer who surveys the property first, checks for exposure and existing damp, and fits a product suited to the situation. A proper survey weeds out the houses that should be left alone.</p>
    <h2>Check before you pay</h2>
    <p>Many houses had their cavities filled years ago without the current owner knowing. Before commissioning anything, ask a surveyor to drill a small inspection hole, or check the deeds and any past paperwork. There is no sense paying to insulate a cavity that is already full, and a borescope check costs a fraction of the job itself.</p>
  </div></section>
''',
)

PAGES["solid-wall-insulation"] = dict(
    title="Insulating a solid-wall house",
    description="How to insulate solid walls with no cavity: internal versus external insulation, the costs and disruption, the big saving on offer, and the pitfalls with older breathable walls.",
    active="guides",
    blurb="No cavity to fill? Solid walls lose the most heat of all, and there are two ways to tackle them.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Houses built before the 1920s usually have solid walls, a single thick skin of brick or stone with no gap inside. These lose more heat than any cavity wall, which makes insulating them the largest fabric improvement an older home can make, though also the most involved.</p>
    <h2>Two ways to do it</h2>
    <p>You can insulate from the inside or the outside. Internal wall insulation fixes insulated boards or a stud layer to the inner face of each external wall, which is cheaper per room but eats a little floor space and means redecorating and moving sockets, skirting and radiators. External insulation wraps the outside of the house in an insulating layer and a new render or cladding finish, which performs better and leaves rooms untouched, but costs considerably more and changes the look of the building.</p>
    <h2>The saving on offer</h2>
    <p>Because solid walls leak so much heat, the potential reduction in heating demand is large, often the biggest single fabric saving available to a pre-war house. The flip side is the upfront cost, which is high enough that the payback runs over many years rather than a handful. It is best thought of as a long-term investment in comfort and value as much as a quick money-saver, and it pairs naturally with other work like a re-render or an extension.</p>
    <h2>Mind the breathability</h2>
    <p>Old solid walls were built to let moisture move through them and dry out. Wrap them in the wrong materials and you can trap damp inside the masonry, causing rot and spoiled plaster. With older and historic buildings especially, use breathable insulation systems designed for solid walls and take advice from someone who understands traditional construction, rather than the cheapest modern board on the shelf.</p>
    <h2>Start with the cheap stuff first</h2>
    <p>Given the cost, solid-wall insulation should usually come after you have done the loft, sealed the <a href="draught-proofing.html">draughts</a> and tackled the easy wins. Those give quick returns for little money, whereas walls are the big, expensive finale. Do them in that order and you are never spending thousands while pennies are still leaking out of an unsealed letterbox.</p>
  </div></section>
''',
)

PAGES["underfloor-insulation"] = dict(
    title="Insulating under the floor",
    description="How to insulate suspended timber and solid ground floors, the draughts that come up through floorboards, what it saves, and the easy first steps before the full job.",
    active="guides",
    blurb="Cold feet and draughts from below? The floor is the forgotten surface, and often an easy fix.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Floors get overlooked because you cannot see the heat leaving through them, but a ground floor sits against cold earth or a ventilated void, and in an older house it can be a real source of both heat loss and the draughts that make a room feel chilly however high the thermostat goes.</p>
    <h2>Two kinds of floor</h2>
    <p>A suspended timber floor, common in older homes, has floorboards over a ventilated gap, and you can often feel air moving up between the boards on a windy day. A solid floor, typical of newer builds, is concrete laid on the ground. The two need different treatment: the timber kind can be insulated from below if there is a cellar or crawl space, or from above by lifting the boards, while a solid floor is usually only insulated as part of a major refurbishment when a new screed goes down.</p>
    <h2>The quick wins first</h2>
    <p>Before any major work, deal with the draughts cheaply. Filling the gaps between floorboards and along the skirting with sealant, a flexible filler or proprietary strips stops the worst of the cold air coming up, and a rug over bare boards adds both comfort and a little insulation for the price of a rug. These small steps take the edge off long before you contemplate lifting a floor.</p>
    <h2>The fuller job</h2>
    <p>For a suspended floor with access underneath, insulation can be supported between the joists from below, which is the least disruptive route as the room above stays intact. Where there is no access, the boards are lifted, insulation laid in, and the boards relaid. It is more work than a loft but follows the same logic, putting a warm layer between you and the cold, and it pairs well with rewiring or replumbing when the floor is up anyway.</p>
    <h2>Keep the air moving below</h2>
    <p>A suspended timber floor relies on those underfloor air bricks to stay dry and rot-free, so never block them in the name of stopping draughts. The job is to insulate above the ventilated void, not to seal the void itself. Done properly, the timbers stay dry and the room above stops feeling like it has a cold breath rising through it.</p>
  </div></section>
''',
)

PAGES["is-double-glazing-worth-it"] = dict(
    title="Is double glazing worth the money?",
    description="An honest look at whether double glazing pays for itself, the comfort and condensation benefits beyond the energy saving, and cheaper alternatives if you cannot justify new windows.",
    active="guides",
    blurb="The honest answer on whether new windows pay back, and what to do if they do not.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">New double or triple glazing is one of the most heavily marketed home improvements, and also one where the energy maths is more sobering than the salesperson lets on. It genuinely cuts heat loss and transforms how a room feels, but as a pure money-saving exercise the payback is long.</p>
    <h2>The energy saving alone is slow to repay</h2>
    <p>Windows are a smaller share of a home's total heat loss than walls or the roof, so replacing single glazing with modern units trims the heating bill by a modest amount each year. Set that against the cost of a houseful of new windows and the payback stretches across decades, longer than the windows might even last. On the saving alone, it rarely makes sense to rip out windows that are otherwise sound.</p>
    <h2>But the bill is not the only benefit</h2>
    <p>Where new glazing earns its keep is in everything the energy figure misses. A warm inner pane stops the cold downdraught you feel sitting by an old window, cuts the condensation that pools on single glazing and feeds mould, and quietens outside noise. If your windows are rotten, draughty or beyond repair, replacing them solves several problems at once, and then the energy saving is a welcome bonus rather than the whole case.</p>
    <h2>Cheaper ways to the same end</h2>
    <p>If the windows are sound but cold, you do not have to replace them to feel the benefit. <a href="secondary-glazing.html">Secondary glazing</a> adds an inner pane for a fraction of the cost, heavy lined <a href="curtains-for-warmth.html">curtains</a> cut the night-time loss, and good <a href="draught-proofing.html">draught-proofing</a> around the frames removes the worst of the cold air. For many homes that combination delivers most of the comfort for a tenth of the spend.</p>
    <h2>When it does add up</h2>
    <p>Replacement makes the most sense when you would be doing the work anyway, when the existing windows are failing, or when you are renovating and the disruption is already priced in. Looked at that way, choose the most efficient units you sensibly can, and treat the lower bills as the long tail of a decision made for comfort and condition first.</p>
  </div></section>
''',
)

PAGES["secondary-glazing"] = dict(
    title="Secondary glazing: warmth without new windows",
    description="How secondary glazing works, why it is so much cheaper than replacement, the options from cheap film to fitted panels, and why it suits period and listed homes.",
    active="guides",
    blurb="A cheap inner pane that gets you most of the benefit of double glazing without ripping anything out.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Secondary glazing puts a second layer of glazing on the room side of an existing window, trapping a pocket of still air that does the insulating. It will never quite match a sealed double-glazed unit, but it costs a fraction as much, keeps your original windows, and gets you most of the way there.</p>
    <h2>How it earns its place</h2>
    <p>The enemy at a window is the cold pane and the air movement around it. Add an inner layer and you create a buffer of trapped air, which slows heat loss, kills the chilly downdraught, and cuts condensation on the original glass. As a bonus it noticeably dampens outside noise, which is why it is popular on busy roads and near railways quite apart from any energy benefit.</p>
    <h2>From a few pounds to a proper fit</h2>
    <p>At the cheap end, shrink-fit insulating film taped over the frame and warmed tight with a hairdryer costs very little and works surprisingly well for a winter, though it is not pretty and goes on and off seasonally. Magnetic or clip-in acrylic panels are a tidy middle ground you can make yourself. At the top end, slim aluminium-framed secondary units are fitted permanently inside the reveal and open and close like a proper window. The right choice depends on budget and how it needs to look.</p>
    <h2>Made for period homes</h2>
    <p>Secondary glazing comes into its own where replacement is impossible or unwanted. Listed buildings and conservation areas often forbid swapping original windows, and owners of period houses frequently want to keep handsome old sashes. Because secondary glazing sits discreetly behind the existing window and changes nothing outside, it sidesteps all of that while still warming the room.</p>
    <h2>Seal it well to get the benefit</h2>
    <p>The trapped air only insulates if it stays trapped, so a good seal around the secondary layer matters more than the glazing itself. A loose film or a gappy panel leaks the benefit away. Combine it with <a href="draught-proofing.html">draught-proofing</a> of the main window and heavy <a href="curtains-for-warmth.html">curtains</a> at night, and a cold single-glazed room becomes genuinely comfortable for very little outlay.</p>
  </div></section>
''',
)

PAGES["radiator-reflectors"] = dict(
    title="Radiator reflector panels: do they work?",
    description="Whether reflective panels behind radiators actually save energy, where they help most, the difference between external walls and internal ones, and how to fit them cheaply.",
    active="guides",
    blurb="A few quid of foil behind the radiator, or pointless gadget? Where it genuinely helps.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Reflective panels slipped behind a radiator are one of those cheap measures that sound like a gimmick but have a real, if modest, basis. The idea is to bounce heat back into the room instead of letting it soak into the wall behind, and on the right wall it does just that.</p>
    <h2>The principle</h2>
    <p>A radiator warms the wall directly behind it as well as the room. If that wall is an external one, much of that heat then escapes outside. A reflective panel, foil-faced board or even good-quality kitchen foil on card, reflects the radiant heat back into the room rather than letting it warm the bricks and disappear. The effect is small per radiator but the cost is tiny, so the sums work out in its favour.</p>
    <h2>Only behind external walls</h2>
    <p>This is the part people miss: reflectors only help behind radiators on external walls, the ones with cold outdoors on the far side. A radiator on an internal wall is warming another part of your own house, so reflecting that heat back saves nothing worth bothering with. Walk round and note which radiators sit against outside walls, and treat only those.</p>
    <h2>Fitting it cheaply</h2>
    <p>You can buy purpose-made panels with a foil face and a thin insulating backing, which are easy to slide down behind the radiator on brackets or tabs. Or you can make your own from rigid foil-faced insulation board cut to size. Either way it tucks out of sight, needs no tools beyond scissors or a knife, and once it is in you forget about it.</p>
    <h2>Keep it in proportion</h2>
    <p>Reflectors are a genuine but minor saving, firmly in the every-little-helps category rather than the game-changers. They are most worthwhile in older, poorly insulated solid-wall homes where the wall behind is doing little to hold heat. If your walls are already well insulated there is little for a reflector to claw back, so spend your effort on the bigger fabric measures first and treat reflectors as a cheap finishing touch.</p>
  </div></section>
''',
)

PAGES["how-to-bleed-radiators"] = dict(
    title="How to bleed a radiator (and why it saves money)",
    description="A step-by-step guide to bleeding trapped air from radiators, how to tell which ones need it, why it makes heating cheaper, and what cold patches at the bottom mean instead.",
    active="guides",
    blurb="Cold at the top, warm at the bottom? Trapped air is making your boiler work harder. Free to fix.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A radiator with air trapped inside cannot fill with hot water, so part of it stays cold and the room never quite warms up. Bleeding that air out is a five-minute job that costs nothing, needs no plumber, and lets your heating do its work without the boiler running longer to compensate.</p>
    <h2>Spotting the ones that need it</h2>
    <p>With the heating on, run your hand up each radiator. If it is hot at the bottom but cold across the top, air is trapped in the upper section and it needs bleeding. Gurgling noises are another giveaway. Cold at the bottom with a warm top is a different problem, usually sludge rather than air, which is covered below.</p>
    <h2>Doing it safely</h2>
    <p>Turn the heating off and let the radiators cool so you are not dealing with scalding water. Find the small square bleed valve at the top corner, hold a cloth and a cup beneath it, and turn the radiator key anticlockwise a quarter turn or so. You will hear air hiss out; when water starts to dribble steadily instead of spitting, the air is gone, so close the valve again snugly. Work round the house, top floor radiators last, as air collects highest.</p>
    <h2>Check the pressure afterwards</h2>
    <p>Letting air and water out can drop the pressure in a sealed combi system. Glance at the boiler's pressure gauge once you are done, and if it has fallen below the normal band, usually marked on the dial, top it up using the filling loop as the boiler manual describes. It is a simple step but skipping it can leave the boiler locked out.</p>
    <h2>When bleeding is not the answer</h2>
    <p>If a radiator is cold at the bottom while the top is warm, the trouble is sludge, a build-up of rust and debris settling inside, and bleeding will not help. That calls for a power-flush or chemical clean of the system, a job for a heating engineer. Keeping the system free of sludge, and keeping radiators bled, both help it run at the lower <a href="boiler-flow-temperature.html">flow temperature</a> that makes a condensing boiler efficient.</p>
  </div></section>
''',
)

PAGES["boiler-flow-temperature"] = dict(
    title="Turn down your boiler flow temperature",
    description="Why lowering the central-heating flow temperature on a condensing combi boiler saves gas, how to find and change the setting on the common makes, what number to aim for, the difference from the room thermostat, and how to handle cold snaps.",
    active="guides",
    blurb="A free setting on most gas combis that can cut gas use noticeably, and almost nobody touches it. Here is exactly how.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">There is a setting on the front of most gas boilers that can cut your gas use by a useful margin, costs nothing to change, takes a couple of minutes, and that the overwhelming majority of households have never knowingly touched. It is the central-heating flow temperature, and the factory default it usually sits on is far higher than your boiler needs to keep you warm.</p>

    <h2>What the flow temperature actually is</h2>
    <p>When your heating is running, the boiler heats water and pumps it round the radiators; that water then returns to the boiler a little cooler, having given up its warmth to the rooms. The flow temperature is simply how hot the boiler heats that water before sending it out. Set high, it sends scalding water to the radiators; set lower, it sends warm rather than scalding water. Crucially, this is a separate control from how hot it heats the water for your taps and shower, and separate again from the thermostat on the wall.</p>

    <h2>Why a cooler flow burns less gas</h2>
    <p>Almost every boiler fitted in the last fifteen years or so is a condensing boiler, and the whole point of that design is a trick it can only pull off when the returning water is cool enough. Burning gas produces hot exhaust containing water vapour, and that vapour holds a surprising amount of recoverable heat. A condensing boiler has an extra-large heat exchanger that, if the returning water is cold enough to chill the exhaust below about fifty-five degrees, condenses that vapour back to liquid and harvests its hidden heat into your heating rather than losing it up the flue.</p>
    <p>Run the boiler too hot and the water coming back from the radiators stays hot, the exhaust never gets chilled enough to condense, and all that recoverable heat is thrown away outside. In that state an expensive condensing boiler performs no better than a crude old one from decades ago. Bring the flow temperature down and the return runs cooler, the boiler spends far more of its time actually condensing, and you get noticeably more heat from every unit of gas you pay for. The fuller explanation is on the <a href="how-condensing-boilers-work.html">how a condensing boiler works</a> guide, but that is the heart of it.</p>

    <h2>This is not the room thermostat, and not the hot water</h2>
    <p>This trips people up, so it is worth being plain. The room <a href="thermostat-settings.html">thermostat</a> decides how warm your rooms get and switches the heating on and off when the air reaches the temperature you set. The flow temperature decides how hot the water in the radiators is while the heating is running. Turning the flow temperature down does not make your house cooler; the thermostat still brings every room up to the same temperature as before. What changes is that the radiators run warm rather than searing, give their heat out more gently, and the boiler sips less gas to keep the house at the temperature you have always had.</p>
    <p>On a combi boiler there is usually a second, separate setting for domestic hot water, the water that comes out of your taps and shower. Leave that one hot, comfortably above sixty degrees, both so your showers are not feeble and for safety against bacteria in the system. The saving here comes only from the heating flow temperature, not the tap water.</p>

    <h2>Finding the setting on your boiler</h2>
    <p>The control varies by make, but it is almost always on the front panel and almost always marked with a radiator symbol to distinguish it from the tap symbol. On older boilers it is a physical dial; on newer ones it is a button-driven menu with a small display.</p>
    <p>On many <strong>Worcester Bosch</strong> models there is a knob or a menu item with a radiator icon; turn or set it down to the low fifties. On <strong>Vaillant</strong> boilers the heating flow target is usually set with the heating-temperature button, again shown as a radiator. <strong>Ideal</strong>, <strong>Baxi</strong>, <strong>Glow-worm</strong>, <strong>Viessmann</strong> and the rest each have their own layout, but all separate the heating temperature from the hot-water temperature, and all let you lower the heating one. If you have the manual, look up central-heating flow or radiator temperature; if you do not, the model number searched online brings it up in seconds. When in doubt, the dial or menu item next to the radiator symbol is the one you want, and the one next to the tap symbol is the one to leave alone.</p>

    <h2>What number to aim for</h2>
    <p>A good starting target for the heating flow is somewhere around fifty to fifty-five degrees, down from the seventy, seventy-five or even higher that many boilers ship on. That range keeps the return water cool enough for the boiler to condense reliably while still warming the house. It is a starting point, not a fixed rule: a very well insulated home can often go lower still, while a draughty house with small radiators may need it a touch higher to keep up. The way to settle it is to try the low fifties for a week or two and only nudge it up if the house genuinely struggles to get warm in the cold.</p>

    <h2>The trade-off, and how to handle a cold snap</h2>
    <p>Cooler radiators give out heat more gently, so two things change. Rooms warm up a little more slowly from cold, and on the very coldest days a low setting may not quite keep pace. Neither is a real problem once you adjust the approach. Instead of heating the house in short hot blasts, set the heating to come on earlier and run for longer at the lower, thriftier temperature, so it eases the house up to warmth rather than blasting it. In a genuine cold snap you can nudge the flow up temporarily and bring it back down when the weather turns, which is a small manual version of the weather-compensation feature some boilers and controls offer automatically.</p>

    <h2>What you might save, and the catch</h2>
    <p>Independent trials have put the gas saving from this single change into the region of several per cent to as much as a tenth of a heating bill, for nothing more than turning a dial, which makes it one of the best-value adjustments in the whole house. The only real catch is that the benefit depends on the boiler being able to condense, so it works best alongside the rest of the basics: <a href="how-to-bleed-radiators.html">bled radiators</a> that fill fully, a system free of sludge, and radiators left clear of furniture so the water gives up its heat and returns cool. Get those right, drop the flow to the low fifties, leave the hot water hot, and you have a meaningful, permanent saving that cost you two minutes and not a penny.</p>
  </div></section>
''',
)

PAGES["how-condensing-boilers-work"] = dict(
    title="How a condensing boiler works, and how to help it",
    description="A plain explanation of condensing boiler technology, why the return water temperature matters, what the white plume from the flue means, and the simple habits that keep efficiency high.",
    active="guides",
    blurb="Understand what 'condensing' actually means and you understand how to get the most from your gas.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Nearly every gas boiler sold in recent years is a condensing model, and understanding the one trick it relies on tells you exactly how to get cheaper heating from it. The technology is clever but the principle is simple, and a couple of free habits keep it working as designed.</p>
    <h2>The trick it pulls</h2>
    <p>Burning gas produces hot exhaust that contains water vapour, and that vapour holds a surprising amount of usable heat. An old boiler threw it all up the chimney. A condensing boiler has a larger heat exchanger that cools the exhaust enough to condense that vapour back into liquid, releasing its hidden heat into your central heating instead of wasting it. That recovered heat is where the extra efficiency comes from.</p>
    <h2>Why the return water decides everything</h2>
    <p>The catch is that the exhaust only condenses if the water coming back from your radiators is cool enough to chill it, somewhere below about fifty-five degrees. If the system runs hot, the return water is hot, nothing condenses, and the boiler behaves no better than an old one. This is exactly why turning down the <a href="boiler-flow-temperature.html">flow temperature</a> matters so much: it keeps the return cool and the boiler condensing.</p>
    <h2>The white plume is a good sign</h2>
    <p>You may notice a cloud of white vapour from the flue outside, especially on cold mornings, and wonder if something is wrong. It is the opposite: that visible plume is the sign your boiler is condensing properly and working as intended. A small pipe also drips condensate to a drain, which can freeze and block in a hard frost, so lagging that pipe outdoors avoids a winter breakdown.</p>
    <h2>Helping it along</h2>
    <p>Beyond the flow temperature, the same housekeeping that helps any system helps this one: <a href="how-to-bleed-radiators.html">bleed the radiators</a> so they fill fully, keep them clear of furniture so heat circulates, and have the system cleaned if sludge is building up. Each of these keeps the return water flowing and cool, which keeps the boiler in its efficient mode and your gas bill lower than the factory settings would leave it.</p>
  </div></section>
''',
)

PAGES["smart-thermostats"] = dict(
    title="Are smart thermostats worth it?",
    description="What smart thermostats actually do, where the savings come from, the features worth having, who benefits most, and an honest take on whether they pay back for your household.",
    active="guides",
    blurb="Clever kit, but the saving comes from behaviour you could change for free. When it is worth buying.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A smart thermostat lets you control your heating from your phone, learns your routine, and can hold back the heat when nobody is home. It is genuinely useful, but it is worth being clear-eyed about where the savings come from, because the device does not save energy by itself.</p>
    <h2>What it actually does</h2>
    <p>At heart a smart thermostat does what a good programmable thermostat has always done, matching heat to when you are in, but it makes that easy and even automatic. It can sense when the house is empty, learn how long your home takes to warm up so it fires the boiler at the right moment, and let you switch the heating off from the bus when you realise you left it on. The convenience is real and removes the friction that stops people bothering with timers.</p>
    <h2>Where the saving really comes from</h2>
    <p>The honest truth is that the saving comes from heating your home less and at better times, which you can do for nothing with the existing programmer and a little discipline. What the smart device adds is making that discipline effortless and automatic, so households that would never reliably fiddle with a timer end up heating an empty house far less. If you already run a tight, well-timed schedule by hand, a smart model will save you little.</p>
    <h2>Features worth having</h2>
    <p>If you do buy one, the features that matter are presence detection or geofencing, so it holds back heat when everyone is out, and individual room control through smart radiator valves, so you heat the rooms in use rather than the whole house. Learning algorithms and weather compensation are nice but secondary. Flashy app graphics are marketing; zoning and occupancy sensing are where the money is saved.</p>
    <h2>Who benefits most</h2>
    <p>The best candidates are households with irregular routines, people out at unpredictable hours, and homes that are often half empty, because there is a lot of wasted heating for the device to catch. A retired couple at home all day on a fixed routine has far less to gain. Weigh the cost against your own pattern, and remember that the free habit changes on the <a href="thermostat-settings.html">thermostat settings</a> page deliver much of the same benefit with no kit at all.</p>
  </div></section>
''',
)

PAGES["radiator-valves-and-zoning"] = dict(
    title="Radiator valves and zoning: heat only where you live",
    description="How thermostatic radiator valves work, why zoning your heating saves money, how to set valves room by room, and how this combines with the main thermostat for the lowest bills.",
    active="guides",
    blurb="Stop heating empty rooms to the same temperature as the lounge. The cheapest way to zone a house.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Most homes heat every room to the same temperature whether anyone uses it or not, which is a quiet waste in spare bedrooms, hallways and the rooms you barely set foot in. Thermostatic radiator valves let you turn the heat down room by room, and used well they trim the bill without any loss of comfort where it counts.</p>
    <h2>What a thermostatic valve does</h2>
    <p>A thermostatic radiator valve, the numbered dial on the end of a radiator, senses the temperature of the room and throttles the flow of hot water to that radiator once the room reaches the set level. Unlike the old on-or-off valves, it holds a room at roughly the temperature you choose, so a setting of two or three keeps a room cooler than a setting of five. It is local control on top of the whole-house control of the main thermostat.</p>
    <h2>Why zoning saves</h2>
    <p>There is no value in heating a guest room, a utility or a rarely used dining room to full living-room warmth. Turning their valves down to a low frost-protection setting means those radiators barely come on, so the boiler has less work to do and less heat is wasted on empty space. You concentrate the warmth, and the gas, on the rooms where you actually sit.</p>
    <h2>Setting them sensibly</h2>
    <p>Set the valves higher in the rooms you live in and lower in those you do not, and leave the room with the main wall <a href="thermostat-settings.html">thermostat</a> on a high or fully open valve so the two controls do not fight each other. Bedrooms can usually sit a notch cooler than living areas for better sleep. A low setting rather than fully off keeps unused rooms above the point where damp and frozen pipes become a risk.</p>
    <h2>The two controls together</h2>
    <p>The wall thermostat decides when the whole system runs and to what temperature the main room reaches; the valves decide how much of that heat each other room gets. Use them as a pair: time the system to your day, set the main thermostat to the lowest comfortable level, and let the valves tail off the rooms you are not in. That combination is the cheapest zoning most homes can manage, and it needs no smart kit at all.</p>
  </div></section>
''',
)

PAGES["curtains-for-warmth"] = dict(
    title="Curtains and blinds: cheap insulation you already own",
    description="How heavy lined curtains cut heat loss through windows at night, the right way to hang and use them, the daytime trick with sunlight, and why they must not cover the radiator.",
    active="guides",
    blurb="Heavy curtains are window insulation you can use tonight. The small habits that make them work.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Before spending anything on windows, look at what hangs in front of them. A good pair of lined curtains, drawn at the right time, traps a layer of still air against the cold glass and cuts the heat a window loses overnight. It is about the cheapest insulation there is, and most of it is in how you use what you have.</p>
    <h2>Why they work</h2>
    <p>Glass is a poor insulator, and at night a window radiates your heat straight out. A heavy, close-fitting curtain creates a pocket of trapped air between fabric and glass that slows that loss, much as <a href="secondary-glazing.html">secondary glazing</a> does, only softer and cheaper. Thermal-lined or interlined curtains do this far better than thin unlined ones, and the heavier and more closely fitted they are, the more they hold the warmth in the room.</p>
    <h2>The timing trick</h2>
    <p>The habit matters as much as the curtain. Draw them at dusk, before the evening chill sets in, to keep the day's warmth inside, and open them fully in the morning. On a sunny winter day, open curtains on south-facing windows let free solar warmth flood in, so the rule is closed against the cold and dark, open to the sun. Done consistently, this single routine noticeably steadies a room's temperature for no cost at all.</p>
    <h2>Hang them to seal</h2>
    <p>A curtain only traps air if it fits closely. Curtains that reach the floor and overlap in the middle hold heat far better than short ones that stop at the sill with gaps down the sides, where warm air spills out and cold tumbles in. A pelmet or a deep rail across the top stops the chimney effect of air rising behind the curtain. The closer the fit all round, the better the seal.</p>
    <h2>Never trap the radiator</h2>
    <p>The one mistake to avoid is letting long curtains hang over the radiator beneath the window. That funnels the radiator's heat straight up the cold glass and out, exactly where you do not want it. Either tuck the curtains behind or onto the windowsill above the radiator, or use sill-length curtains there. Keep the heat coming into the room, not channelled out through the window.</p>
  </div></section>
''',
)

PAGES["heat-pumps-explained"] = dict(
    title="Heat pumps explained without the jargon",
    description="What an air-source heat pump is, how it can deliver more heat than the energy it uses, why it likes a well-insulated house and low flow temperatures, and whether it suits your home.",
    active="guides",
    blurb="The technology behind heat pumps, in plain terms, and the kind of house that gets the best from one.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Heat pumps attract a lot of noise, some of it overcooked in both directions. Stripped of the jargon, a heat pump is a proven, efficient way to heat a home with electricity, and whether it is right for you comes down mostly to your house and how it is run rather than the technology itself.</p>
    <h2>Heat moved, not made</h2>
    <p>A heat pump does not burn anything or glow like an electric heater. It works like a fridge in reverse, using a little electricity to gather warmth from the outside air, even on a cold day there is heat in it, and concentrate it to a useful temperature for your radiators and hot water. Because it moves existing heat rather than creating it, it can deliver several units of warmth for each unit of electricity, which is why it can beat a gas boiler on energy used even though electricity costs more per unit.</p>
    <h2>It likes low and slow</h2>
    <p>A heat pump is happiest producing a gentle, steady warmth rather than blasting out very hot water on demand. It runs at lower flow temperatures than a traditional boiler, so it pairs best with larger radiators or underfloor heating and with a home that holds its heat. This is why the advice is always to insulate and <a href="draught-proofing.html">draught-proof</a> first: a leaky house forces the pump to work hard at high temperatures, which is where running costs and complaints come from.</p>
    <h2>The house makes or breaks it</h2>
    <p>In a well-insulated home with suitable radiators, a heat pump runs efficiently and cheaply and keeps the place comfortably warm all day. In a cold, draughty, poorly insulated house left to heat in short hot bursts, it struggles and disappoints. The technology is not the variable so much as the building and the way it is run, which is the same lesson as the rest of this site, just with the stakes raised.</p>
    <h2>Is it for you?</h2>
    <p>A heat pump makes the most sense if your home is reasonably insulated or you are willing to improve it, if you have somewhere outside for the unit, and if you can run the heating gently across the day rather than in spikes. It is a bigger decision than any single tweak here, often helped by grants, so treat it as a long-term step to take once the cheap fabric improvements are done, not before.</p>
  </div></section>
''',
)

PAGES["cylinder-jacket-and-pipe-lagging"] = dict(
    title="Cylinder jackets and pipe lagging: the cheapest hot-water saving",
    description="Why insulating a hot-water cylinder and its pipes is one of the best-value energy jobs, how to choose and fit a jacket, lagging exposed pipes, and what it saves each year.",
    active="guides",
    blurb="A few pounds of foam keeps your stored hot water hot for longer. One of the fastest paybacks anywhere.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">If you have a hot-water cylinder, wrapping it properly is one of the quickest paybacks in the whole house. You have already paid to heat that water; an insulating jacket simply stops it going cold while it waits to be used, and the materials cost less than a couple of takeaways.</p>
    <h2>The bare or thinly clad cylinder</h2>
    <p>An uninsulated copper cylinder sheds heat constantly, so the boiler or immersion has to reheat it again and again. A thick insulating jacket cuts that standing loss dramatically, keeping the water hot for far longer between heat-ups. Even cylinders with a thin sprayed-on factory layer benefit from a jacket over the top, since the original foam is often thinner than ideal. The colder the cupboard the cylinder sits in, the more a jacket saves.</p>
    <h2>Choosing and fitting one</h2>
    <p>Look for a jacket of generous thickness, the chunkier the better, sized to your cylinder's height and girth. Fitting is a job anyone can do: the segments wrap around and tie or strap into place, leaving the controls and the immersion boss accessible. It takes minutes and no tools. If the cylinder is in a warm airing cupboard you use to dry clothes, bear in mind a good jacket keeps that cupboard cooler, which is the point.</p>
    <h2>Lag the pipes too</h2>
    <p>The pipes leaving the cylinder lose heat just as the tank does, so slip foam pipe lagging over every accessible length of hot pipe, especially the first stretch from the cylinder. The pre-slit foam tubes cost very little, push on by hand and cut to length with a knife. Lagging the pipes keeps the water hotter on its way to the tap and means less cold water run off before it arrives.</p>
    <h2>While you are in there</h2>
    <p>Set the cylinder thermostat to a sensible level rather than scalding, as covered on the <a href="hot-water-savings.html">hot water</a> page, so you are not maintaining water far hotter than you ever use. And lag any cold pipes that run through unheated lofts while you are buying foam, since that protects them from freezing in winter. The whole exercise is an afternoon and a small spend for a saving that repeats every single day.</p>
  </div></section>
''',
)

PAGES["immersion-heater-cost"] = dict(
    title="The immersion heater: handy but pricey",
    description="Why an electric immersion heater is an expensive way to make hot water, when it makes sense to use one, how a timer helps, and the off-peak tariff trick for heating water cheaply.",
    active="guides",
    blurb="Heating water with electricity costs far more than with gas. When to use the immersion, and how to tame it.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">An immersion heater is a large electric element that heats the water in a cylinder directly, like a giant kettle. It is reliable and useful as a backup, but because it heats with electricity rather than gas it is one of the dearer ways to make hot water, and it is easy to leave it costing you money without noticing.</p>
    <h2>Why it costs what it does</h2>
    <p>A typical immersion draws around three kilowatts and runs for an hour or more to heat a full tank. Put those figures through the <a href="appliance-running-cost.html">running cost calculator</a> at the electricity price and the cost of a tankful is sobering, especially compared with heating the same water on a gas boiler, where each unit of energy is far cheaper. The element is not inefficient; electricity is simply expensive per unit.</p>
    <h2>The quiet money-waster</h2>
    <p>The classic mistake is a household with a gas boiler that also has an immersion as backup, left switched on permanently. It silently tops the tank up with costly electricity whenever the temperature drops, doing a job the boiler would do for a fraction of the price. If that describes your setup, make sure the immersion is off unless the boiler is out of action, and you may shave a surprising amount off the electricity bill.</p>
    <h2>Use a timer</h2>
    <p>Where the immersion is your main water heater, fit or use a timer so it heats a tankful when you need it rather than maintaining a hot tank around the clock. Heating once in the morning and perhaps once in the evening, sized to your use, beats reheating continuously. Pair the timer with a good <a href="cylinder-jacket-and-pipe-lagging.html">cylinder jacket</a> so the heated water stays hot between draw-offs instead of cooling and triggering another costly reheat.</p>
    <h2>The off-peak trick</h2>
    <p>If you are on an <a href="economy-7-and-night-rates.html">Economy 7</a> or similar tariff with cheap night-time electricity, an immersion comes into its own. Heat a well-insulated tankful overnight at the low rate and the stored hot water lasts much of the day, sidestepping the expensive daytime price. This is the one situation where an immersion can be a sensible main source, provided the cylinder is well lagged so the cheap night heat is not lost before you use it.</p>
  </div></section>
''',
)

PAGES["low-flow-showerheads"] = dict(
    title="Low-flow showerheads: save water and the energy to heat it",
    description="How an aerating or low-flow showerhead cuts hot-water use without a feeble shower, the energy saving that comes with using less hot water, and which showers they do and do not suit.",
    active="guides",
    blurb="Use less hot water in the shower and you cut the bill to heat it. A cheap swap with a quick payback.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Most of the cost of a shower is not the water itself but the energy used to heat it, so anything that cuts how much hot water you use cuts the bill twice over. A low-flow or aerating showerhead does exactly that, often without the weak dribble people fear.</p>
    <h2>How they keep the feel without the flow</h2>
    <p>An aerating showerhead mixes air into the water, so the spray feels full and powerful while actually using less water. Other designs use cleverly shaped nozzles to maintain pressure at a lower flow. Either way the aim is the same, a satisfying shower from fewer litres a minute, which means less hot water drawn and less energy spent heating it. For many people the difference in feel is barely noticeable once fitted.</p>
    <h2>The double saving</h2>
    <p>Using less hot water saves on both the water bill, if you are metered, and the far larger energy cost of heating it. Across a household showering daily, trimming the flow rate adds up to a meaningful annual saving for the price of a showerhead. Combine it with keeping showers brisk, as the <a href="hot-water-savings.html">hot water</a> page suggests, and the two together make a real dent without anyone feeling deprived.</p>
    <h2>Mind which shower you have</h2>
    <p>There is one important exception. Electric showers heat water on demand and already control their own flow, so a low-flow head offers little there and can occasionally upset them. The same caution applies to certain low-pressure gravity-fed systems, where restricting the flow further leaves a feeble trickle. Low-flow heads suit mains-pressure and combi-fed mixer showers best, so check what you have before buying.</p>
    <h2>Even cheaper options</h2>
    <p>If a new head is not worth it, a simple shower timer or even a favourite four-minute song nudges the habit in the right direction for nothing. Some water companies give aerators and flow regulators away free, so it is worth checking yours before paying. The principle holds either way: every litre of hot water you do not use is energy you do not pay to heat.</p>
  </div></section>
''',
)

PAGES["standby-power-the-full-story"] = dict(
    title="Standby power: the full story",
    description="How much standby and always-on power really costs a typical home, which devices are the worst offenders, how to find them, and a sensible plan that does not mean unplugging everything.",
    active="guides",
    blurb="The real numbers on standby waste, the worst culprits, and why unplugging your phone charger is pointless.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Standby power is the energy devices use while switched off but still plugged in and ready. It is real, and across a houseful of gadgets it adds up to a noticeable yearly sum, but it is also widely exaggerated and misdirected. Knowing which devices matter saves you both money and the faff of chasing trivial savings.</p>
    <h2>How much it actually is</h2>
    <p>Each device on standby sips only a few watts, but a modern home has dozens of them, and a few watts running every hour of every day quietly accumulates. Totted up, the always-on load of a typical household runs to a modest but worthwhile annual cost. It will never rival the heating or the tumble dryer, so keep it in proportion, but it is real money for very little effort to reclaim.</p>
    <h2>The worst offenders</h2>
    <p>Not all standby is equal. The biggest culprits are devices that stay genuinely active rather than truly asleep: set-top boxes and digital recorders that keep listening and recording, games consoles in a connected standby, older equipment with power-hungry transformers, and anything with a clock, display or instant-on feature. A <a href="using-a-plug-in-energy-monitor.html">plug-in energy monitor</a> reveals these in seconds, and the readings are often surprising.</p>
    <h2>Where unplugging is pointless</h2>
    <p>By contrast, a phone charger left in the wall with nothing attached draws so little that switching it off saves pennies a year, despite the persistent myth. The same goes for most modern low-standby electronics. Religiously unplugging trivial devices is effort spent for almost nothing, the very fussing-over-pennies this site warns against. Spend that energy on the real users instead.</p>
    <h2>A sensible plan</h2>
    <p>Rather than crawling behind furniture nightly, target the worst offenders. Put the television, console and the cluster of boxes around it on a single switched extension lead and turn the lot off at night with one switch. Choose true-off rather than standby on devices that offer it. Leave genuinely low-draw items alone. That gets you nearly all the saving for almost none of the bother, which is the right trade every time.</p>
  </div></section>
''',
)

PAGES["kettle-energy-saving"] = dict(
    title="Boiling the kettle for less",
    description="Why the kettle is a surprisingly heavy electricity user, the simple habit of boiling only what you need, descaling for efficiency, and whether eco kettles and flasks are worth it.",
    active="guides",
    blurb="A heavy hitter you use many times a day. The one habit that cuts its cost without any new gadget.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A kettle is one of the most powerful things in the house, pulling around three kilowatts, and the average home boils it several times a day. Each boil is brief, so no single one costs much, but the habit repeated for years makes the kettle a worthwhile target, and the fix costs nothing.</p>
    <h2>Only boil what you need</h2>
    <p>The single biggest saving is to boil only the water you are about to use. Filling the kettle to the top for a single mug means heating several extra cups of water for no reason, every time. Measure your mug into the kettle, or use the cup markings on the gauge, and you cut the energy per brew straight away. Across a tea-drinking household over a year, that small discipline adds up more than people expect.</p>
    <h2>Descale for speed and efficiency</h2>
    <p>In a hard-water area, limescale furs up the element and makes the kettle slower and less efficient, since the scale gets in the way of heat reaching the water. Descaling regularly with a cheap descaler or white vinegar keeps the element clear so the kettle boils quickly and uses less energy doing it. A heavily scaled kettle is both slower and thirstier.</p>
    <h2>Eco kettles and the flask trick</h2>
    <p>So-called eco kettles, with clear gauges and low minimum fills, mostly just make it easier to boil less, which you can do for free by paying attention. Rapid-boil kettles save time rather than energy. A genuinely useful habit for big tea drinkers is to boil once and keep the rest hot in a vacuum flask, so a single boil serves several drinks across the morning rather than reboiling each time.</p>
    <h2>Kettle versus the alternatives</h2>
    <p>For boiling water, an electric kettle is actually efficient, putting nearly all its energy straight into the water, so heating a mugful on a gas hob or in a pan is usually slower and no cheaper. The kettle is the right tool; the waste is purely in overfilling it. Put your own usage through the <a href="appliance-running-cost.html">cost calculator</a> and the case for boiling less makes itself.</p>
  </div></section>
''',
)

PAGES["air-fryer-running-cost"] = dict(
    title="Air fryer running cost: the hype and the reality",
    description="Why an air fryer is cheaper to run than a big oven for small meals, when it genuinely saves and when it does not, what a typical session costs, and how it compares with a microwave.",
    active="guides",
    blurb="Cheaper than the oven for small portions, but not magic. When the air fryer genuinely saves, and when it does not.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Air fryers became a sensation partly on the promise of slashing cooking bills, and there is truth in it, but also a fair amount of overstatement. An air fryer is essentially a small, fast fan oven, and its savings come from that smallness, not from any special efficiency.</p>
    <h2>Why it can save</h2>
    <p>A full-size oven has a large cavity to heat and takes time to come up to temperature, so cooking a modest portion in it wastes energy heating empty space. An air fryer heats a tiny chamber quickly and circulates hot air efficiently around the food, so for one or two portions it does the job in less time and far less energy. For chips, a couple of fillets or reheating, the saving over firing up the big oven is genuine.</p>
    <h2>When it does not save</h2>
    <p>The advantage shrinks or vanishes as the quantity grows. Cooking a large family meal in several small air-fryer batches can use as much energy as one ovenful, and a roast for six belongs in the oven. The air fryer wins on small, quick jobs and loses on big batch cooking, so it complements the oven rather than replacing it. Buying one will not cut your bills if you still use the oven for everything substantial.</p>
    <h2>What a session costs</h2>
    <p>A typical air fryer pulls one to two kilowatts but for a short time, so a fifteen or twenty minute cook costs only a few pence at usual electricity prices. Run your model's wattage and a realistic cooking time through the <a href="appliance-running-cost.html">cost calculator</a> to see your own figure. The headline saving against the oven is real for small meals, but it is pence per meal, not pounds, so set expectations accordingly.</p>
    <h2>Where it sits</h2>
    <p>Think of the air fryer as the right-sized tool for small, quick cooking, alongside the <a href="oven-microwave-air-fryer-compared.html">microwave</a> for reheating and the oven for big batches. Used that way it genuinely trims cooking energy. Bought as a miracle that pays for itself in weeks, it will disappoint. As ever, match the appliance to the job and the savings follow.</p>
  </div></section>
''',
)

PAGES["oven-microwave-air-fryer-compared"] = dict(
    title="Oven, microwave or air fryer: which is cheapest to cook in?",
    description="A practical comparison of the running cost of ovens, microwaves and air fryers, why the microwave wins for small jobs, and how to match the appliance to the meal to spend the least.",
    active="guides",
    blurb="The same meal can cost very different amounts depending on what you cook it in. A practical comparison.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The same plate of food can cost wildly different amounts to cook depending on which appliance you reach for. None is best for everything; the trick is matching the tool to the task. Here is how the kitchen's three workhorses compare, and when each wins.</p>
    <h2>The microwave: champion of small and quick</h2>
    <p>For heating a portion, defrosting, or cooking something small, the microwave is almost always the cheapest, because it puts energy directly into the food and heats nothing else. There is no large cavity to warm and no preheating, so a few minutes of microwaving costs very little. For reheating leftovers or a single serving, nothing beats it on cost.</p>
    <h2>The air fryer: small meals, crisp results</h2>
    <p>An <a href="air-fryer-running-cost.html">air fryer</a> sits between the two. It heats a small chamber fast, so for one or two portions of something that wants a crisp finish, chips, roast vegetables, a couple of fillets, it undercuts the big oven comfortably. Its limit is capacity: cook for a crowd and you are running batch after batch, at which point its edge over the oven disappears.</p>
    <h2>The oven: built for batches</h2>
    <p>A full oven is the thirstiest for a small job because of all the space it heats, but it comes into its own when that space is full. A whole roast, several trays at once, or a big batch cooked to portion and freeze spreads the oven's energy across a lot of food, which is the cheapest way to feed many. The oven is not wasteful when it is full; it is wasteful when it heats a vast cavity to warm one small dish.</p>
    <h2>The rule of thumb</h2>
    <p>Reheating or a single small portion goes in the microwave. A small crisp meal for one or two suits the air fryer. A big meal, or batch cooking to freeze, justifies the oven. Match the appliance to the quantity and you spend the least without owning anything new. Put your own appliances through the <a href="appliance-running-cost.html">cost calculator</a> with realistic times to see the gaps in your own money.</p>
  </div></section>
''',
)

PAGES["slow-cooker-economy"] = dict(
    title="The slow cooker: cheap cooking that runs all day",
    description="Why a slow cooker uses far less energy than it seems despite running for hours, how its low wattage keeps costs down, the meals it suits, and how it compares with the oven.",
    active="guides",
    blurb="Runs for eight hours yet barely sips power. Why the slow cooker is one of the cheapest ways to cook a meal.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A slow cooker seems like it ought to be expensive, sitting switched on for six or eight hours at a stretch. In fact it is one of the cheapest ways to cook a hot meal, because what matters is not how long something runs but how much power it draws while it does, and a slow cooker draws very little.</p>
    <h2>Low power beats long hours</h2>
    <p>A slow cooker typically pulls somewhere around a hundred to three hundred watts, a tiny fraction of an oven's two or three thousand. Multiply that small draw by a long cooking time and the total energy is still modest, often less than cooking the same casserole for a couple of hours in a hot oven. The well-insulated pot holds its heat, so the element only sips to maintain a gentle simmer. Run the figures through the <a href="appliance-running-cost.html">cost calculator</a> and the long runtime stops looking alarming.</p>
    <h2>The meals it loves</h2>
    <p>Slow cookers excel at exactly the dishes that are otherwise time-consuming and energy-hungry: stews, casseroles, curries, soups, pulled meats and dried beans and pulses. The long, low heat turns cheaper, tougher cuts of meat tender, so it saves on the shopping as well as the energy bill. It is a natural partner to batch cooking, since a big pot can be portioned and frozen for several future meals.</p>
    <h2>Versus the oven and hob</h2>
    <p>For a long-cooked dish, the slow cooker usually beats both the oven, which heats a huge cavity, and a pan simmering on the hob, which loses heat to the room. The convenience is part of the appeal too: load it in the morning, leave it, and come home to a cooked meal with no oven to mind. For quick cooking it is the wrong tool, but for anything that wants long, gentle heat it is hard to beat on cost.</p>
    <h2>Getting the most from it</h2>
    <p>Keep the lid on, since lifting it lets out heat and steam and lengthens the cook. Cut ingredients to a similar size so they cook evenly, and do not overfill. Use the low setting where the recipe allows, as it draws even less. With a little planning, the slow cooker quietly turns out cheap, generous meals for a few pence of electricity each.</p>
  </div></section>
''',
)

PAGES["induction-vs-gas-hob"] = dict(
    title="Induction versus gas hob: running cost and efficiency",
    description="How induction hobs compare with gas and conventional electric for cost and efficiency, why induction wastes the least heat, the price-per-unit twist, and what to weigh when choosing.",
    active="guides",
    blurb="Induction wastes the least heat of any hob, but electricity costs more per unit. How the sums shake out.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Choosing a hob pits efficiency against the price of the fuel. Induction is the most efficient way to cook on a surface, putting almost all its energy into the pan, but electricity costs more per unit than gas, so the cheapest hob to run is not as clear-cut as the efficiency figures alone suggest.</p>
    <h2>Why induction is so efficient</h2>
    <p>An induction hob heats the pan directly through a magnetic field, so very little energy is lost to the surroundings; the hob itself stays relatively cool and the heat goes where you want it. A gas flame, by contrast, licks around the sides of the pan and loses a good deal of its heat to the air, and a conventional electric ring wastes energy warming the element and the ceramic. In pure efficiency, induction is the clear winner, gas the laggard.</p>
    <h2>The price-per-unit twist</h2>
    <p>Efficiency is only half the sum. Because each unit of electricity costs considerably more than each unit of gas, induction's efficiency advantage is partly cancelled by the dearer fuel. The result is that, on running cost alone, induction and gas often end up broadly comparable, with the balance shifting as the relative prices of gas and electricity move. Neither is dramatically cheaper to cook on than the other for most households.</p>
    <h2>The other things in the balance</h2>
    <p>Cost is rarely the only factor. Induction is faster to heat, responsive, easy to clean with its flat surface, and safer with no flame and a cool top. Gas gives the visible flame many cooks prefer and works in a power cut. If you are moving away from gas in the home anyway, perhaps towards a <a href="heat-pumps-explained.html">heat pump</a>, an induction hob fits that direction. These practical differences often decide the choice more than the running cost does.</p>
    <h2>Whatever you cook on</h2>
    <p>Good habits cut hob energy on any fuel: use a pan that matches the ring or zone size so heat is not wasted around the edges, keep lids on to bring things to the boil faster and hold them there, and turn the heat down once a pan is simmering rather than leaving it on full. Those small disciplines save more, day to day, than the choice between fuels.</p>
  </div></section>
''',
)

PAGES["dishwasher-efficiency"] = dict(
    title="Running a dishwasher cheaply (and beating the sink)",
    description="Why a modern dishwasher often uses less hot water and energy than washing up by hand, how to run it most efficiently with eco mode and full loads, and the habits that cut its cost.",
    active="guides",
    blurb="Often cheaper than washing up by hand, if you run it right. Eco mode, full loads, and skipping the pre-rinse.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">It surprises people, but a modern dishwasher run sensibly often uses less hot water and energy than washing the same dishes by hand under a running tap. The machine is efficient by design; the waste, where it exists, is in how it is loaded and which programme is chosen.</p>
    <h2>Why the machine can win</h2>
    <p>A dishwasher heats a precise, small amount of water and recirculates it, whereas a tap left running while you wash and rinse pours hot water away continuously. Filled properly and run on the right programme, the machine does a full load of dishes on less hot water than the sink method uses, and the energy to heat that water is the main cost either way. The hand-wash only wins if you are frugal with a bowl rather than a running tap.</p>
    <h2>Use eco mode and full loads</h2>
    <p>The single biggest saving is the eco programme. It washes at a lower temperature over a longer time, which uses noticeably less energy than the hotter, faster cycles, and still cleans normal dishes perfectly well. Just as important, run the machine only when it is full, since a half-empty load uses nearly as much water and energy as a full one. Waiting for a full load and choosing eco together cut the cost per item substantially.</p>
    <h2>Skip the pre-rinse</h2>
    <p>Rinsing plates under a hot tap before loading wastes exactly the hot water the machine is meant to save you, and modern dishwashers and detergents cope fine with scraped, unrinsed plates. Scrape the leftovers into the bin or compost, load them as they are, and let the machine do its job. The pre-rinse habit is a hangover from older, weaker machines and quietly undoes the dishwasher's efficiency.</p>
    <h2>A little maintenance</h2>
    <p>Keep the filter clean and the spray arms clear so the machine works effectively and does not need rewashing, and use rinse aid so dishes dry without a second hot cycle. If your machine can draw from a hot feed and you heat water cheaply with gas, that can help, though many are cold-fill and heat efficiently themselves. Run the wattage and cycle time through the <a href="appliance-running-cost.html">cost calculator</a> to see what an eco load really costs you.</p>
  </div></section>
''',
)

PAGES["washing-at-30-degrees"] = dict(
    title="Washing clothes at 30 degrees",
    description="Why washing laundry at a lower temperature saves a surprising amount of energy, why modern detergents make it effective, when a hotter wash is still worth it, and the other laundry savings.",
    active="guides",
    blurb="Most of a wash's energy goes on heating the water. Drop the temperature and clean clothes still come out clean.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Almost all the energy a washing machine uses goes on one thing: heating the water. The drum, the pumps and the spin draw very little by comparison. That single fact is why turning the temperature down is the easiest laundry saving there is, and why it works without leaving your clothes any less clean.</p>
    <h2>The heat is the cost</h2>
    <p>Because heating water dominates a wash's energy use, dropping from a hot wash to a cool one cuts the energy markedly. A thirty-degree wash uses considerably less than a forty or sixty, and a cold wash less still. The mechanical action of the drum and the detergent do most of the actual cleaning; the hot water is largely there out of old habit. Lower the temperature and you keep the cleaning while shedding most of the cost.</p>
    <h2>Modern detergents are made for it</h2>
    <p>Today's detergents are formulated to work at low temperatures, with enzymes that lift stains in cool water, so a thirty-degree wash gets everyday laundry perfectly clean. The era when you needed a hot wash to shift normal dirt is long gone. For the bulk of your washing, lightly soiled everyday clothes, low and cool is all it takes.</p>
    <h2>When to go hotter</h2>
    <p>There are sensible exceptions. Heavily soiled items, greasy work clothes, and laundry from someone unwell benefit from a hotter wash to deal with bacteria and stubborn grime, and towels and bedding occasionally like a warmer wash to stay fresh. Running an occasional hot maintenance wash also keeps the machine itself clean and free of odour-causing residue. The point is to reserve heat for when it is needed, not to use it by default.</p>
    <h2>The rest of the laundry savings</h2>
    <p>Wash full loads rather than half-empty ones, since the machine uses similar energy either way. Use a high spin speed to wring out more water, which shortens any drying that follows. And wherever you can, dry on a line or airer rather than the <a href="tumble-dryer-cost.html">tumble dryer</a>, which is by far the most expensive part of doing laundry. Together these turn washday into one of the cheaper chores rather than a hidden drain.</p>
  </div></section>
''',
)

PAGES["washing-machine-running-cost"] = dict(
    title="What a washing machine really costs to run",
    description="Where a washing machine's energy actually goes, how cycle temperature and load size change the cost, what a typical wash costs, and the settings that cut it without buying a new machine.",
    active="guides",
    blurb="The cost is almost all in heating the water. Where it goes, what a wash costs, and how to spend less.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A washing machine feels like a steady background cost, but the spending is lopsided in a way that, once you see it, tells you exactly how to spend less. Nearly all of it is one thing, and that one thing is easy to control.</p>
    <h2>Where the energy goes</h2>
    <p>The motor that turns the drum, the pumps that move the water, and the spin at the end all draw modest amounts. The heater that warms the water draws far more than the rest combined. So the running cost of a wash is dominated by the temperature you choose, not by the length of the cycle or the spin speed. This is why dropping to a <a href="washing-at-30-degrees.html">cooler wash</a> is the lever that matters most.</p>
    <h2>What a wash costs</h2>
    <p>A cool wash costs only a few pence in energy; a hot one several times that. The water itself adds a little if you are metered. Across a household doing several loads a week, the difference between always washing hot and mostly washing cool adds up to a worthwhile yearly sum. Put your machine's rated consumption, often listed per cycle on its label, through the <a href="appliance-running-cost.html">cost calculator</a>, or work from its wattage and a realistic cycle time, to see your own figure.</p>
    <h2>Load size matters too</h2>
    <p>A machine uses broadly similar energy whether half or fully loaded, so running it full rather than part-loaded cuts the cost per item without any change to the wash. Resist the temptation to put a small urgent load on its own; wait until you have a full drum, or use a half-load setting if the machine has a genuine one. Overstuffing is the opposite mistake, as clothes will not clean and you end up rewashing.</p>
    <h2>Settings that save</h2>
    <p>Choose the eco programme where there is one, as it uses less despite a longer run, and use the cool everyday cycles for normal laundry. Spin fast to wring out water and shorten any drying. Skip extra rinses unless you need them. None of this requires a new machine; it is simply using the one you have on its thriftier settings, with the temperature dial doing most of the work.</p>
  </div></section>
''',
)

PAGES["electric-shower-cost"] = dict(
    title="What an electric shower costs to run",
    description="Why electric showers are powerful energy users, how their high wattage but short run translates into real cost, how they compare with mixer showers and baths, and how to keep the bill down.",
    active="guides",
    blurb="One of the highest-wattage things in the house, used daily. What it really costs, and how to trim it.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">An electric shower is among the most powerful appliances in the home, heating cold mains water instantly with an element of eight, nine or even ten kilowatts. That huge draw, used daily and often by several people, makes it worth understanding, though its short run keeps the per-shower cost lower than the frightening wattage suggests.</p>
    <h2>High power, short burst</h2>
    <p>The number on an electric shower is its power, not its cost. Ten kilowatts is enormous, far more than an oven, but a shower lasts minutes rather than hours, so the energy per shower is the power multiplied by that short time. A brisk shower costs a manageable amount; a long, daily one for each member of a household adds up to a real line on the electricity bill. The <a href="appliance-running-cost.html">cost calculator</a>, fed your shower's kilowatts and a typical duration, shows the figure for your own routine.</p>
    <h2>How it compares</h2>
    <p>An electric shower heats only the water you use, on demand, which is efficient in that nothing is heated and then left to go cold. But it heats with expensive electricity rather than cheaper gas, so a similar shower from a gas-heated mixer can cost less per minute even though both use hot water. Against a bath, a reasonable electric shower still uses far less, so the old advice to shower rather than bathe holds, provided the shower stays short.</p>
    <h2>Keeping the cost down</h2>
    <p>The lever is time, since the power is fixed. Shorter showers cost proportionally less, so a timer, or simply not lingering, is the main saving. Many electric showers have a lower power or eco setting for summer, when the incoming water is warmer and less heating is needed, so use it. Lowering the temperature setting a touch reduces the draw as well.</p>
    <h2>Showerhead caution</h2>
    <p>Unlike a mixer shower, an electric shower is not a good candidate for a <a href="low-flow-showerheads.html">low-flow head</a>, since it controls its own flow and restricting it can cause problems. The saving here comes almost entirely from spending less time under it. Keep showers brisk and use the eco setting when you can, and a high-wattage shower need not mean a frightening bill.</p>
  </div></section>
''',
)

GUIDES_ORDER = [
    # Heating and the building fabric
    "loft-insulation", "draught-proofing", "cavity-wall-insulation", "solid-wall-insulation",
    "underfloor-insulation", "is-double-glazing-worth-it", "secondary-glazing",
    "curtains-for-warmth", "radiator-reflectors",
    "thermostat-settings", "smart-thermostats", "radiator-valves-and-zoning",
    "how-to-bleed-radiators", "boiler-flow-temperature", "how-condensing-boilers-work",
    "heat-pumps-explained",
    # Hot water
    "hot-water-savings", "cylinder-jacket-and-pipe-lagging", "immersion-heater-cost",
    "low-flow-showerheads",
    # Electricity and appliances
    "led-lighting", "standby-power-the-full-story", "tumble-dryer-cost",
    "fridge-freezer-efficiency", "washing-at-30-degrees", "washing-machine-running-cost",
    "dishwasher-efficiency", "kettle-energy-saving", "electric-shower-cost",
    "air-fryer-running-cost", "oven-microwave-air-fryer-compared", "slow-cooker-economy",
    "induction-vs-gas-hob",
    # Bills and tariffs
    "understanding-energy-bill", "switching-suppliers",
    # Fuel and driving
    "hypermiling",
]


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
