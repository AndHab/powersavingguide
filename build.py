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
INDEXNOW_KEY = "8941122d5f9c4564a7267b028b081df0"

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


def page(slug, title, description, body, active=None, pubdate=None):
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
              "datePublished": pubdate or LAUNCH, "dateModified": date.today().isoformat(),
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
    <p>These habits trim a useful slice off a fuel bill, commonly into the low tens of per cent for a heavy-footed driver who reforms. They will not rival the saving from simply driving less, so where a journey can be shared, cycled or skipped, that is the biggest lever of all. In summer, how you cool the car plays in too: the <a href="keeping-your-car-cool-fuel-economy.html">keeping your car cool</a> guide weighs air conditioning against open windows.</p>
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
    title="How much does it cost to run a tumble dryer?",
    description="What a tumble dryer costs to run in the UK: the energy and cost of a typical load, what it adds up to over a year, why a heat-pump dryer uses about half the electricity of a vented or condenser model, and the cheaper ways to dry.",
    active="guides",
    blurb="A conventional dryer costs around 80p a load; a heat-pump model about half that. The figures, and the cheaper ways to dry.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Anything that makes heat is expensive to run, and a tumble dryer makes a lot of it. For a household that dries every load by machine it is often one of the largest single lines on the electricity bill, rivalling the fridge-freezer despite running a tiny fraction of the hours. The good news is that the cost is easy to work out, and it is one of the easiest big bills to trim, because the cheapest dryer of all costs nothing.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A conventional vented or condenser dryer uses around 3 kWh for a full load, so at the standard electricity rate of about 26p a unit that is roughly 78p a load, or about 120 pounds a year drying three loads a week. A heat-pump dryer uses around half that, near 40p a load. Drying every day pushes a conventional dryer past 280 pounds a year. A washing line or airer costs nothing at all.</p>
    </div>

    <h2>Why a tumble dryer costs so much</h2>
    <p>A conventional vented or condenser dryer works by heating fresh air, blowing it through the wet clothes, and throwing the warm damp air away, either out of a vent or into a condenser tank. Heating air like that draws a lot of power, typically a couple of kilowatts, and it runs for an hour or more per load, so the energy mounts up. That is the whole story of the bill: not the time the machine runs, but the heat it makes while running. It is the same reason an <a href="electric-shower-cost.html">electric shower</a> or a kettle pulls so much, and the reason a dryer can cost as much over a year as appliances that are switched on far longer.</p>

    <h2>What a load costs</h2>
    <p>The sum is the one the <a href="appliance-running-cost.html">running cost calculator</a> does for any appliance: the energy a cycle uses, multiplied by your price per unit. The table uses the standard price-cap rate of about 26p per kWh, current in mid 2026. The energy per load varies with the machine, the programme and how wet the clothes go in, so treat these as typical full-load figures and check your own machine's rating.</p>

    <table class="ev-table">
      <thead><tr><th>Dryer type</th><th>Energy per load</th><th>Cost per load</th><th>Year at 3 loads/week</th><th>Year at 6 loads/week</th></tr></thead>
      <tbody>
        <tr><td>Vented or condenser</td><td>~3 kWh</td><td>~78p</td><td>~£122</td><td>~£244</td></tr>
        <tr><td>Heat-pump dryer</td><td>~1.5 kWh</td><td>~39p</td><td>~£61</td><td>~£122</td></tr>
      </tbody>
    </table>
    <p class="ev-note">At an example 26p per kWh. The split is the headline: a heat-pump dryer used six times a week costs about what a conventional one costs at three. Energy per load varies with load size, fabric and how hard the washing machine spun first, so your figure may differ.</p>

    <h2>What it adds up to over a year</h2>
    <p>The per-load figure looks small, but a tumble dryer is a daily-habit appliance, and the annual total is where it bites. Dry three loads a week on a conventional machine and you are spending well over a hundred pounds a year just on drying; dry every day, as a busy family easily can, and a vented or condenser dryer climbs past 280 pounds. That is why the dryer so often turns out to be one of the priciest things in the house despite running only an hour at a time. Knowing your own number is the first step: find the machine's energy per cycle, often on the <a href="energy-labels-explained.html">energy label</a> as a figure per 100 cycles, and scale it to how often you really run it.</p>

    <h2>Conventional versus heat-pump: the big split</h2>
    <p>Not all dryers are equal, and the difference is large. A heat-pump dryer does not throw its warm air away; it passes it over a heat pump that recovers the heat and reuses it, drying the clothes for roughly half the electricity of a vented or condenser machine, sometimes less. That is the gap the energy label makes obvious, with heat-pump models rating far better than the old vented sort. The trade-offs are a higher purchase price and a slightly longer, gentler cycle. For a light user who rarely dries by machine, a cheap vented dryer used occasionally is fine. For anyone drying often, the running-cost saving of a heat-pump model adds up over the life of the machine and usually outweighs the higher sticker price, the same logic the <a href="energy-labels-explained.html">energy labels</a> guide applies to any appliance that runs a lot.</p>

    <h2>The free alternative</h2>
    <p>The cheapest dryer is a washing line or a clothes airer, which cost nothing to run at all. Drying outdoors whenever the weather allows, or on an airer in a well-ventilated room, removes the cost entirely, and you do not have to do it for every load to save real money. Even air-drying half your washing roughly halves the dryer's annual bill. The single most effective trick before any drying, by machine or otherwise, is to spin the washing harder: a higher spin speed in the <a href="washing-machine-running-cost.html">washing machine</a> wrings out more water, so there is less left for the dryer or the line to remove, and the dryer runs for less time. The <a href="drying-clothes-without-a-tumble-dryer.html">drying clothes without a tumble dryer</a> guide covers the indoor options, including low-watt heated airers and dehumidifiers, for the days the weather will not help.</p>

    <h2>If you must use the machine</h2>
    <p>When the dryer is the only option, a few habits keep its cost down. Dry full loads rather than dribs and drabs, since the machine uses similar energy whether half or fully loaded, so part loads waste it. Clean the lint filter every single time, because a clogged filter chokes the airflow and makes the dryer work harder and run longer for the same result. Use the moisture-sensor or eco programme if the machine has one, so it stops the moment the clothes are dry rather than grinding on to a fixed timer. And dry similar fabrics together, since a load of light, fast-drying items finishes far quicker than a mixed load held up by one heavy towel. None of these costs anything, and together they trim a meaningful slice off every cycle.</p>

    <h2>The bottom line</h2>
    <p>A tumble dryer costs real money because it makes heat: a conventional vented or condenser model runs to about 78p a load and well over a hundred pounds a year at modest use, while a heat-pump dryer does the same job for roughly half. Read the energy per cycle off your machine, scale it to how often you dry, and you will know your own figure. Then cut it the obvious ways: spin harder first, air-dry whatever you can, run only full loads with a clean filter, and if you dry a great deal, let a heat-pump model pay back its higher price in lower bills.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to run a tumble dryer?","acceptedAnswer":{"@type":"Answer","text":"A conventional vented or condenser dryer uses about 3 kWh per load, costing roughly 78p at the 26p standard electricity rate. That is about 120 pounds a year drying three loads a week, or over 280 pounds drying daily. A heat-pump dryer uses around half the electricity, about 39p a load."}},{"@type":"Question","name":"Is a heat-pump tumble dryer cheaper to run?","acceptedAnswer":{"@type":"Answer","text":"Yes, markedly. A heat-pump dryer recovers and reuses its own warm air instead of venting it, so it dries for roughly half the electricity of a vented or condenser model, around 1.5 kWh against 3 kWh per load. It costs more to buy and dries a little slower, but for frequent use the running-cost saving outweighs the higher price."}},{"@type":"Question","name":"Why is my tumble dryer so expensive to run?","acceptedAnswer":{"@type":"Answer","text":"Because it makes heat. A conventional dryer draws a couple of kilowatts to heat air and runs for an hour or more per load, so even though it is on only a short time it uses a lot of energy. Used daily it can cost as much over a year as a fridge-freezer that never switches off."}},{"@type":"Question","name":"How can I reduce the cost of using a tumble dryer?","acceptedAnswer":{"@type":"Answer","text":"Spin the washing at a higher speed first so less water is left to dry, air-dry whatever loads you can on a line or airer, run only full loads, clean the lint filter every time, and use the moisture-sensor or eco programme. If you dry often, a heat-pump dryer roughly halves the electricity used."}}]}</script>
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
    <p>A reasonably full freezer holds its cold better than an empty one, as the frozen mass acts as a buffer, so it cycles on less. A fridge, on the other hand, wants air to circulate, so do not cram it. And when it comes to replacing a very old unit, a fridge-freezer from twenty years ago can use several times the electricity of a modern efficient one, so the running-cost saving alone can justify the swap. In a heatwave the appliance works harder still, which the <a href="fridge-freezer-in-hot-weather.html">fridge and freezer in hot weather</a> guide explains.</p>
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
    <p>A heat pump does not burn anything or glow like an electric heater. It works like a fridge in reverse, using a little electricity to gather warmth from the outside air, even on a cold day there is heat in it, and concentrate it to a useful temperature for your radiators and hot water. Because it moves existing heat rather than creating it, it can deliver several units of warmth for each unit of electricity, which is why it can beat a gas boiler on energy used even though electricity costs more per unit. Whether it beats a boiler on running cost too is a closer question, worked out in the <a href="heat-pump-running-cost-vs-gas-boiler.html">heat pump versus gas boiler running cost</a> guide.</p>
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
    title="How much does it cost to run an immersion heater?",
    description="What an immersion heater costs to run in the UK: the energy and cost of heating a tankful by cylinder size, what a year of immersion-heated water comes to, why it is dearer than gas, the quiet money-waster to switch off, and the Economy 7 trick that halves the bill.",
    active="guides",
    blurb="A tankful costs around £2 at the standard rate, about half that overnight on Economy 7. The figures, and the trap to avoid.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">An immersion heater is a large electric element that heats the water in a cylinder directly, like a giant kettle. It is reliable and useful as a backup, but because it heats with electricity rather than gas it is one of the dearer ways to make hot water. The cost is easy to work out, and it is just as easy to leave one quietly running up the bill, so it is worth knowing both what a tankful costs and the one trick that roughly halves it.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A typical immersion heats a full cylinder using around 7 to 12 kWh depending on tank size, so at the standard electricity rate of about 26p a unit that is roughly 1.80 to 3.15 pounds a tankful. Heated overnight on an Economy 7 night rate it costs about half that. Rely on the immersion for all your hot water and a year can run to several hundred pounds at the standard rate, which is why a gas boiler, or off-peak heating, makes such a difference.</p>
    </div>

    <h2>Why it costs what it does</h2>
    <p>A typical immersion element draws around three kilowatts and runs for an hour or more to bring a full tank up to temperature. The element itself is not inefficient; nearly all the electricity it draws ends up as heat in the water. The expense is the fuel: electricity costs about 26p a unit on the standard rate, while a gas boiler heats the same water at roughly 8p a unit of heat, as the <a href="hot-water-savings.html">hot water savings</a> guide explains. So heating water by immersion costs around three times what the same hot water costs from gas. That is the whole reason an immersion has a reputation as a pricey way to make hot water, and why it matters how, and when, you run one.</p>

    <h2>What a tankful costs</h2>
    <p>The energy to heat a cylinder depends on its size, because you are warming a fixed volume of water from cold mains temperature up to storage heat. The table below works out a full reheat for the common cylinder sizes, both at the standard price-cap rate of about 26p per kWh, current in mid 2026, and at an example Economy 7 night rate of around 13p. Put your own cylinder and rate through the <a href="appliance-running-cost.html">running cost calculator</a> using the element's wattage and the time it runs.</p>

    <table class="ev-table">
      <thead><tr><th>Cylinder size</th><th>Energy for a full reheat</th><th>Standard rate (26p)</th><th>Economy 7 night (13p)</th></tr></thead>
      <tbody>
        <tr><td>120 L (small or flat)</td><td>~7 kWh</td><td>~£1.80</td><td>~90p</td></tr>
        <tr><td>150 L (typical household)</td><td>~9 kWh</td><td>~£2.35</td><td>~£1.15</td></tr>
        <tr><td>210 L (large or family)</td><td>~12 kWh</td><td>~£3.15</td><td>~£1.55</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Energy to heat the tank from cold mains to a typical storage temperature; in practice you often top up a part-cooled tank rather than heat fully from cold, so a real reheat tends to use less. Economy 7 night rates vary by tariff and region, so check your own. The off-peak column shows the prize: the same hot water for about half the price.</p>

    <h2>What it adds up to over a year</h2>
    <p>One tankful is a couple of pounds; relying on the immersion for all your hot water is where it bites. A household heating roughly a tankful a day can spend somewhere around 600 to 850 pounds a year on the standard rate, depending on cylinder size and how much hot water you draw, and roughly half that if the heating is done overnight on Economy 7. As a backup used only when the boiler is down, the cost is trivial. As a main water heater on a flat daytime rate, it is one of the larger lines on the bill, which is the figure worth knowing before you decide how to run it.</p>

    <h2>The quiet money-waster</h2>
    <p>The classic and costly mistake is a household with a gas boiler that also has an immersion fitted as backup, left switched on permanently. It silently tops the tank up with expensive electricity whenever the water cools, doing a job the boiler would do for a third of the price, and most people never realise it is happening. If that describes your setup, make sure the immersion switch is off unless the boiler is actually out of action. Flicking that one switch off can shave a surprising amount off the electricity bill, and it is the first thing to check if your electricity use looks higher than it should.</p>

    <h2>The Economy 7 trick</h2>
    <p>There is one situation where an immersion genuinely makes sense as a main source, and the table hints at it. If you are on an <a href="economy-7-and-night-rates.html">Economy 7</a> or similar tariff with cheap night-time electricity, heat a well-insulated tankful overnight at the low rate and the stored hot water lasts much of the day, sidestepping the expensive daytime price entirely. This is how all-electric homes without gas keep their water-heating cost down. The catch is that the cheap night heat has to survive until you use it, so a good <a href="cylinder-jacket-and-pipe-lagging.html">cylinder jacket</a> and lagged pipes are essential; without them the tank cools through the day and you end up paying the dear daytime rate for a top-up, throwing away the saving. Cheap heat stored well is the whole game.</p>

    <h2>Use a timer, and size it to your use</h2>
    <p>Where the immersion is your main water heater, a timer is the difference between a sensible bill and a wasteful one. Set it to heat a tankful when you need it, once overnight on Economy 7 or once in the morning and perhaps again before evening, rather than maintaining a hot tank around the clock, which just pays to replace heat leaking from the cylinder hour after hour. Size the heating to your real use: a household that showers in the morning needs the water hot then, not at midnight and again at noon. Pair the timer with the cylinder jacket so each heated tankful stays hot between draw-offs instead of cooling and triggering another costly reheat. A timer, a jacket and the right tariff together turn the immersion from a money pit into a workable system.</p>

    <h2>The bottom line</h2>
    <p>An immersion heater costs around 1.80 to 3.15 pounds to heat a full tank at the standard rate, depending on cylinder size, and about half that overnight on Economy 7, because the element is efficient but electricity is dear. As a backup it costs next to nothing; as a main heater on a daytime rate it can run to several hundred pounds a year. Switch it off if a gas boiler can do the job, and if it is your main source, heat it overnight on a cheap night rate through a timer, with the cylinder well lagged so the cheap heat lasts. Run that way, even electric water heating need not be a frightening bill.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to run an immersion heater?","acceptedAnswer":{"@type":"Answer","text":"Heating a full cylinder uses about 7 to 12 kWh depending on tank size, so at the 26p standard electricity rate a tankful costs roughly 1.80 to 3.15 pounds. On an Economy 7 night rate of around 13p it costs about half that. Used as a main water heater it can add up to several hundred pounds a year on the standard rate."}},{"@type":"Question","name":"Is an immersion heater more expensive than gas?","acceptedAnswer":{"@type":"Answer","text":"Yes, about three times more per unit of heat. Electricity costs around 26p a unit on the standard rate, while a gas boiler heats water at roughly 8p a unit of heat. The immersion element is efficient, but the electricity it uses is simply dearer than gas, so a gas boiler heats the same water for far less."}},{"@type":"Question","name":"Should I leave my immersion heater on all the time?","acceptedAnswer":{"@type":"Answer","text":"No. Leaving it on permanently just pays to replace heat leaking from the tank around the clock. Use a timer to heat a tankful when you need it. If you have a gas boiler and the immersion is only a backup, keep it switched off unless the boiler is out of action, as leaving it on quietly wastes a lot of electricity."}},{"@type":"Question","name":"How can I heat water with an immersion more cheaply?","acceptedAnswer":{"@type":"Answer","text":"Get on an Economy 7 or similar tariff and heat the tank overnight at the cheap night rate, then insulate the cylinder with a good jacket and lag the pipes so the heat lasts through the day. Use a timer sized to your actual hot-water use rather than reheating continuously, and switch the immersion off entirely if a gas boiler can do the job."}}]}</script>
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
    title="How much does it cost to run an electric shower?",
    description="What an electric shower costs to run in the UK: why its huge wattage matters less than you fear, the cost of a shower by power rating and length, what it adds up to for a household over a year, how it compares with a gas mixer and a bath, and how to keep the bill down.",
    active="guides",
    blurb="A 9 to 10 kW monster used for minutes. A typical shower costs 30 to 40p; the lever is time, not the wattage.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">An electric shower is among the most powerful appliances in the home, heating cold mains water on the spot with an element of eight, nine or even ten and a half kilowatts. That enormous draw, used daily and often by several people, makes it look alarming on paper. But a shower lasts minutes, not hours, so the cost per shower turns out far gentler than the wattage suggests. This guide works out the real figures and where the bill actually comes from.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> An electric shower draws 8.5 to 10.5 kilowatts, but runs only minutes, so a typical 8-minute shower costs about 30p to 40p at the standard electricity rate of around 26p a unit. One person showering daily comes to roughly 120 pounds a year; a family of four nearer 480 pounds. The power rating is fixed, so the lever you control is time, and the eco or summer setting.</p>
    </div>

    <h2>Huge power, short burst</h2>
    <p>The big number on an electric shower is its power, not its cost. Ten kilowatts is vast, more than three or four ovens at once, which is why electric showers need their own heavy circuit. But power is the rate energy is used, and the energy that actually costs you is the power multiplied by the time. Because a shower lasts a handful of minutes rather than hours, that big rate over a short burst comes to a modest amount of energy. A brisk shower costs pence; a long, daily one for everyone in the house adds up to a real line on the bill. The trap is reading the kilowatt figure as if it ran for an hour, when it runs for eight minutes.</p>

    <h2>What a shower actually costs</h2>
    <p>The sum is the one the <a href="appliance-running-cost.html">running cost calculator</a> does for any appliance: the power in kilowatts, times the hours it runs, times your unit rate. The table works it out for the common shower powers and a range of shower lengths, at the standard price-cap rate of about 26p per kWh, current in mid 2026. Find your shower's rating, usually marked on the unit, and read across.</p>

    <table class="ev-table">
      <thead><tr><th>Shower power</th><th>5-minute shower</th><th>8-minute shower</th><th>10-minute shower</th></tr></thead>
      <tbody>
        <tr><td>8.5 kW</td><td>~18p</td><td>~30p</td><td>~37p</td></tr>
        <tr><td>9.5 kW</td><td>~21p</td><td>~33p</td><td>~41p</td></tr>
        <tr><td>10.5 kW</td><td>~23p</td><td>~37p</td><td>~46p</td></tr>
      </tbody>
    </table>
    <p class="ev-note">At an example 26p per kWh. The figures show why time is the lever: the same 10.5 kW shower costs twice as much at ten minutes as at five. The power rating barely moves the cost compared with how long you stand under it.</p>

    <h2>What it adds up to for a household</h2>
    <p>One shower is cheap; the habit is what counts. A single person taking an 8-minute shower every day on a 9.5 kW unit spends about 33p a time, which is roughly 120 pounds over a year. Scale that to a household and it climbs fast: four people showering daily is closer to 480 pounds a year, making the shower one of the larger slices of the electricity bill. That is the figure worth knowing, because it is the one a few shorter showers a week visibly dents. Put your own shower's power and your family's habits through the calculator and you will see your real annual number rather than a guess.</p>

    <h2>Electric shower versus a gas mixer and a bath</h2>
    <p>Two fair comparisons put the cost in context. Against a gas-heated mixer shower, the electric shower has a catch: it heats with electricity at about 26p a unit, while a gas combi heats water at roughly 8p a unit of heat, as the <a href="hot-water-savings.html">hot water</a> guide explains, so gas is the cheaper fuel per unit. Set against that, an electric shower heats only the water that flows through it, on demand, and often at a lower flow rate, so it wastes nothing standing in a tank. In practice the two can land closer than the fuel prices alone suggest, but a gas mixer usually costs a little less per equivalent shower. Against a bath, though, a reasonable electric shower wins comfortably: a bath uses a large volume of heated water, far more than a short shower, so the old advice to shower rather than bathe holds, as long as the shower stays brief. A long, luxurious shower can use as much as a bath, which is the point at which the advice breaks down.</p>

    <h2>Keeping the cost down</h2>
    <p>Because the power is fixed, time is the main lever, and it is a strong one: a five-minute shower costs little more than half what a ten-minute one does. A simple timer, or just not lingering, is the biggest saving available. Many electric showers also have a lower-power or eco setting, useful in summer when the incoming mains water is already warmer and needs less heating to reach temperature, so the element can run at reduced power; use it through the warmer months. Nudging the temperature setting down a touch reduces the draw as well. None of this is about cold, miserable showers, just brisk ones at a sensible heat.</p>

    <h2>Why a low-flow head is the wrong move here</h2>
    <p>One common saving does not apply to electric showers. Unlike a mixer shower, an electric shower controls its own flow as part of heating the water, so fitting a restrictive <a href="low-flow-showerheads.html">low-flow showerhead</a> can interfere with how it works and even cause it to overheat and cut out. The water saving on a mixer comes from throttling the flow; on an electric shower the flow is already modest and managed by the unit. The saving here comes almost entirely from spending less time under it, not from changing the head. Keep showers brisk, use the eco setting when the weather allows, and a frighteningly high-wattage shower need not mean a frightening bill.</p>

    <h2>The bottom line</h2>
    <p>An electric shower's huge wattage is misleading, because it runs only for minutes: a typical 8-minute shower costs about 30p to 40p at the standard rate, and the cost scales almost entirely with how long you stay under it. One person showering daily is around 120 pounds a year and a family of four nearer 480, so the household total is where it matters. A gas mixer is usually a little cheaper to run and a bath usually dearer than a short shower. Shorten the shower, use the eco setting in summer, leave the showerhead alone, and the bill stays modest however big the number on the unit.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to run an electric shower?","acceptedAnswer":{"@type":"Answer","text":"An electric shower draws 8.5 to 10.5 kW but runs only minutes, so a typical 8-minute shower costs about 30p to 40p at the 26p standard electricity rate. One person showering daily comes to roughly 120 pounds a year, and a family of four nearer 480 pounds. The cost scales with how long you shower, not with the wattage."}},{"@type":"Question","name":"Does the high kilowatt rating make an electric shower expensive?","acceptedAnswer":{"@type":"Answer","text":"Less than it looks. The kilowatt figure is the rate energy is used, and the cost is that rate times the time. Because a shower lasts minutes rather than hours, even a 10 kW shower uses only a modest amount of energy per use, around 30p to 46p depending on its power and how long you stay under it."}},{"@type":"Question","name":"Is an electric shower cheaper than a gas shower or a bath?","acceptedAnswer":{"@type":"Answer","text":"A gas-heated mixer shower is usually a little cheaper, because gas costs roughly 8p a unit of heat against electricity at about 26p, though the electric shower wastes nothing by heating only the water that flows. Against a bath, a short electric shower is cheaper, since a bath uses far more heated water. A long shower can match a bath."}},{"@type":"Question","name":"How can I reduce the cost of an electric shower?","acceptedAnswer":{"@type":"Answer","text":"Shorten the shower, since cost scales almost entirely with time: a five-minute shower costs little more than half a ten-minute one. Use the lower-power eco setting in summer when the mains water is warmer, and nudge the temperature down a touch. Do not fit a low-flow showerhead, which can make an electric shower overheat and cut out."}}]}</script>
''',
)

PAGES["smart-meters-explained"] = dict(
    title="Smart meters: what they do and what they do not",
    description="A clear, honest guide to smart meters: how they work, the in-home display, why a smart meter does not by itself save money, the half-hourly data that unlocks cheaper tariffs, and the common problems and how to deal with them.",
    active="guides",
    blurb="They end estimated bills and unlock cheaper tariffs, but the meter itself saves you nothing. Here is the real story.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Smart meters arrive wrapped in a lot of promise and a fair amount of suspicion, and the truth sits between the two. A smart meter is a useful piece of kit that ends estimated billing and opens the door to genuinely cheaper ways of buying energy, but the meter on its own does not lower your bill by a single penny. Everything depends on what you do with it.</p>

    <h2>What a smart meter actually is</h2>
    <p>A smart meter is simply a gas or electricity meter that records your usage digitally and sends the readings to your supplier automatically over a dedicated mobile-style network, with no phone line or home broadband involved. It replaces the old habit of someone reading the dial, or you sending a photo of it. For electricity it can record how much you use in each half-hour period; for gas it records totals at intervals. That automatic, accurate, frequent reading is the whole technical change. Everything else people associate with smart meters flows from having that data.</p>

    <h2>The in-home display, and its limits</h2>
    <p>Most installations come with a small screen, the in-home display, that shows your usage in near real time and in money as well as units. This is the part that can genuinely change behaviour, because for the first time you can watch the cost tick up when you switch the kettle, the shower or the oven on, and see the difference when you turn the heating down. For a week or two it is fascinating and educational, and it helps you find the hungry appliances the <a href="appliance-running-cost.html">running cost calculator</a> would otherwise have to estimate. The limit is human: the novelty fades, the display ends up ignored behind the fruit bowl, and the saving from watching it tails off. Treat it as a teaching tool for the first month rather than a permanent money-saver.</p>

    <h2>Why the meter alone saves nothing</h2>
    <p>This is the point the marketing skates over. A smart meter measures what you use more accurately; it does not use less for you. If your habits do not change and your tariff does not change, your bill is the same as it was with the old meter, give or take the end of estimated guesswork. The savings people attribute to smart meters really come from two things the meter makes possible: behaviour change prompted by seeing the cost, and access to tariffs that need half-hourly data to work. The meter is the key, not the saving itself.</p>

    <h2>Accurate bills, and the end of estimates</h2>
    <p>The most reliable benefit is mundane but real. With automatic readings you are billed for exactly what you used, not a supplier's estimate that leaves you either building up credit you have to chase back or sliding into a debt that lands as a nasty catch-up bill. As the <a href="understanding-energy-bill.html">understanding your bill</a> guide explains, an estimated bill can be well wide of the mark, so ending the estimates alone is worth having, especially if your usage is unusual or has changed.</p>

    <h2>The data that unlocks cheaper tariffs</h2>
    <p>The bigger prize is the half-hourly electricity data, because it makes time-of-use tariffs possible. These charge different prices at different times of day: cheap overnight or off-peak rates, dearer peak rates. If you can shift heavy use into the cheap windows, charging an electric car, running the washing or heating water with an <a href="immersion-heater-cost.html">immersion</a>, the savings can be substantial. The older <a href="economy-7-and-night-rates.html">Economy 7</a> arrangement was a blunt version of the same idea; smart meters allow far more flexible modern versions. Without a smart meter, none of these tariffs are open to you, which is the clearest practical reason to have one.</p>

    <h2>The common problems</h2>
    <p>Smart meters have earned some of their bad reputation. The biggest historical issue was that an early-generation meter often went dumb if you switched supplier, losing its smart features until the new supplier re-enrolled it; the later generation is designed to carry over between suppliers, so a meter installed now is far less likely to suffer this. Some homes in poor signal areas struggle to connect, since the meter relies on a wireless network. And the in-home display can lose its link to the meter, usually fixed by moving it closer or restarting it. None of these are reasons to refuse a meter outright, but they are worth knowing so you are not surprised.</p>

    <h2>Should you get one?</h2>
    <p>For most households the sensible answer is yes, but with clear eyes. Get one because it ends estimated bills, because it lets you find your hungry appliances, and above all because it is the entry ticket to time-of-use tariffs that can actually cut your costs if your usage is flexible. Do not get one expecting the box itself to shrink the bill, and do not feel you must accept one if you are happy submitting your own readings and your tariff gives you no reason to switch. The meter is a tool; the saving still comes from how you use energy and how you buy it.</p>
  </div></section>
''',
)

PAGES["economy-7-and-night-rates"] = dict(
    title="Economy 7 and night-rate tariffs: are they worth it?",
    description="How Economy 7 and other night-rate electricity tariffs work, who genuinely saves on them and who loses, the role of storage heaters and immersion timers, and how to work out whether the split rate suits your home.",
    active="guides",
    blurb="Cheap electricity overnight, dearer by day. Brilliant for some homes, a quiet loss for others. How to tell which you are.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Economy 7 is the long-standing arrangement that gives you cheaper electricity for seven hours overnight in exchange for a higher price during the day. It can be a real money-saver or a quiet penalty, and which one it is depends almost entirely on when you use your electricity. Getting this wrong costs people money for years without their realising.</p>

    <h2>How the split rate works</h2>
    <p>On a standard single-rate tariff every unit costs the same whatever the hour. Economy 7 splits the day in two: a cheap rate for a seven-hour block at night, often somewhere between midnight and seven in the morning though the exact window varies by region and meter, and a more expensive rate the rest of the time. Your meter records day and night usage separately, either as two registers on one meter or as readings you submit as two figures. The night rate can be markedly cheaper than the single rate, but the crucial catch is that the day rate is markedly dearer than it.</p>

    <h2>Who genuinely saves</h2>
    <p>The tariff rewards a home that does a lot of its electrical work at night. Classic winners are houses heated by electric storage heaters, which deliberately soak up cheap night electricity into their bricks and release the warmth through the day, and homes that heat water with an <a href="immersion-heater-cost.html">immersion heater on a timer</a> overnight. Add in running the dishwasher and washing machine on a delay timer so they finish in the small hours, and charging an electric car overnight, and a household can push the majority of its usage into the cheap window. For these homes Economy 7 can cut the electricity bill considerably.</p>

    <h2>Who quietly loses</h2>
    <p>The flip side catches a lot of people. If you have gas central heating and gas hot water, most of your electricity goes on lighting, cooking, the kettle, the telly and appliances used in the evening, all of it at the expensive day rate. For that household the dear daytime price more than wipes out the cheap nights, and they would be better off on a flat single rate. Plenty of homes sit on Economy 7 by inheritance, because a previous occupant had storage heaters long since removed, and lose money on it year after year without knowing.</p>

    <h2>Doing the rough sum</h2>
    <p>You do not need to be precise to see which camp you are in. Find your day and night usage split from a recent bill or your meter's two registers. As a rough guide, Economy 7 tends to pay off only if you can get something approaching forty per cent or more of your electricity onto the night rate; below that the expensive daytime units usually cost you more than the cheap nights save. Feed your appliance wattages and likely night-time hours into the <a href="appliance-running-cost.html">running cost calculator</a> to see how much you could realistically shift, then weigh that cheap-rate saving against paying the higher day rate on everything else.</p>

    <h2>Making the most of it if you stay</h2>
    <p>If Economy 7 does suit you, the saving comes from discipline about timing. Use delay-start timers on the washing machine and dishwasher so they run in the cheap window, set the immersion and any storage heaters to charge overnight, and charge an EV then too. Be careful with high-power daytime use, since an electric shower or a load of tumble drying at the day rate is now noticeably dearer than it would be on a single tariff. The whole game is to move the heavy, schedulable loads into the night and keep expensive habits out of the day.</p>

    <h2>The modern picture</h2>
    <p>Economy 7 is the old, blunt version of charging by time of day. A <a href="smart-meters-explained.html">smart meter</a> opens up more flexible modern time-of-use tariffs with cheaper or even occasionally free off-peak periods, which can suit EV owners and flexible households better than the fixed seven-hour block. If you are weighing up Economy 7, it is worth checking whether a smart time-of-use tariff would serve you better, since the principle is the same but the windows and rates are often more generous. As with any tariff change, compare the total annual cost for your own pattern of use rather than the headline rates alone, as the <a href="switching-suppliers.html">switching guide</a> sets out.</p>
  </div></section>
''',
)

PAGES["solar-panels-the-basics"] = dict(
    title="Solar panels: the basics, in plain English",
    description="A jargon-free explanation of how domestic solar panels work, what a typical system is made of, what affects how much they generate, the difference between using and exporting power, and what to realistically expect from a roof in the UK.",
    active="guides",
    blurb="How a roof full of panels actually works, what drives the output, and why using your own power matters most.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Solar panels have gone from exotic to ordinary, but the way they work and, more importantly, the way they save you money is still widely misunderstood. Before deciding whether they are worth it for your home, which the <a href="is-solar-worth-it.html">is solar worth it</a> guide tackles, it helps to understand plainly what the kit does and what governs how much you get from it.</p>

    <h2>How a panel makes electricity</h2>
    <p>A solar photovoltaic panel turns daylight directly into electricity. It does not need direct sunshine or heat to work, only light, so it still generates on a bright overcast day, just less than in full sun. Each panel produces direct current, the same kind a battery gives, which is no use to your house as it stands. So the second key component, the inverter, converts that direct current into the alternating current your home and the grid actually use. Panels on the roof, an inverter somewhere like the loft or a cupboard, and the wiring to tie it into your consumer unit: that is the heart of a system.</p>

    <h2>What the parts are</h2>
    <p>A domestic installation is a roof array of panels wired together, an inverter, a generation meter that records how much the system produces, and the connection into your fuse board. Many systems now add a battery, which stores surplus daytime generation for use in the evening, and that battery changes the economics enough to deserve its own treatment in the <a href="solar-battery-storage.html">battery storage</a> guide. The size of a system is given in kilowatts peak, its output under ideal test conditions, and a typical house array might be a few kilowatts peak across eight to sixteen panels, roof space permitting.</p>

    <h2>What governs how much you get</h2>
    <p>Output depends on things you can influence and things you cannot. Roof direction matters most: a south-facing roof generates the most over a year, east and west less but spread across morning and afternoon, and north-facing roofs are generally not worth it. The pitch of the roof, the absence of shading from trees, chimneys or neighbouring buildings, and simply how sunny your region is all play in. So does the season, with long summer days producing several times what short, low-sun winter days manage, though a panel running hot in a heatwave gives up a little of its peak, as the <a href="solar-panels-hot-weather.html">solar panels in hot weather</a> guide explains. A realistic expectation for the UK is a system that does well from spring to autumn and modestly in deep winter, not one that runs your house off-grid year round.</p>

    <h2>The part that matters: using versus exporting</h2>
    <p>This is the single most important idea for the money side. Electricity your panels make and you use yourself at that moment is worth the full price you would otherwise have paid to buy it, which is the expensive retail rate. Electricity you generate but do not use is exported to the grid, and you are paid for that export at a much lower rate. So the value of a solar system depends heavily on how much of its output you consume yourself rather than spilling to the grid. A house with someone home in the daytime, or with the dishwasher, washing and hot water timed to run while the sun is up, captures far more value than one that exports most of its generation while everyone is out.</p>

    <h2>Shifting your use to the sunshine</h2>
    <p>Because self-used power is worth so much more than exported power, the practical trick with solar is to move flexible loads into daylight hours. Running the washing machine, dishwasher and any <a href="immersion-heater-cost.html">immersion water heating</a> in the middle of a sunny day, and charging an electric car then if you can, soaks up generation you would otherwise sell cheap and buy back dear. A battery does this automatically by storing the midday surplus for the evening peak. Either way, the aim is to consume your own sunshine rather than hand it to the grid for a pittance.</p>

    <h2>What to realistically expect</h2>
    <p>Solar is not a magic switch that ends your bills, and anyone promising that is overselling. A well-sited system meaningfully reduces the electricity you buy, most strongly in the lighter half of the year, and pays you a little for what you export. It works best as one part of a sensible whole, fitted to a home that has already done the cheap efficiency basics so the generation goes further. Understand it as a long-term reduction in your bills and a modest hedge against rising prices, and it makes sense; expect overnight independence and it will disappoint.</p>
  </div></section>
''',
)

PAGES["is-solar-worth-it"] = dict(
    title="Is solar worth it in 2026?",
    description="An honest, figure-backed look at whether domestic solar panels pay off in 2026: what a system costs, how much it generates, how the savings and export payments add up at current prices, a worked payback, where batteries fit, and the questions to ask before signing.",
    active="guides",
    blurb="What a system costs, what it generates, and a worked payback at 2026 prices. No hype, no doom.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Whether solar panels are worth it does not have one answer, because it depends on your roof, your habits and the prices of the day. But it does have a clear set of factors and, in 2026, some firm enough figures to put real numbers on the decision. Run your own situation through them honestly and you can judge a quote without leaning on the salesperson's optimism. The how-it-works detail sits in the <a href="solar-panels-the-basics.html">solar basics</a> guide; this one is about the money.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A typical 4 kW system costs around £7,000 to £8,500 fully installed in 2026, with no VAT, and generates roughly 3,400 to 4,000 kWh a year on a well-sited roof. Between the electricity you avoid buying at the roughly 26p cap rate and what you earn exporting the rest at a 5p to 15p export rate, a good system returns somewhere around £650 to £820 a year, paying back in roughly 9 to 12 years and then generating largely free power for many years more. A poor roof, heavy shade or a low export rate stretch that out.</p>
    </div>

    <h2>The roof comes first</h2>
    <p>No amount of clever financing rescues a poor roof. A south-facing, unshaded roof at a reasonable pitch is the strong case; east and west roofs still work but generate less; a north-facing or heavily shaded roof rarely justifies the cost. Shading is a particular killer, because even partial shade across part of the array at the wrong time of day can drag the output down disproportionately. Before anything else, be honest about which way your roof faces and what shades it through the day. If the roof is wrong, the rest of the sums do not matter.</p>

    <h2>What it costs and what it generates</h2>
    <p>A standard domestic system is around 4 kilowatts, roughly ten panels, and in 2026 costs about £7,000 to £8,500 fully installed, including the panels, inverter, mounting and electrical work, with residential solar carrying no VAT. On a well-sited roof that system generates somewhere around 3,400 to 4,000 kWh a year, concentrated in the brighter half of the year, with an east or west roof or any shading pulling the figure down. Those two numbers, the cost and the yearly generation, are the foundation of every payback sum, so be wary of a quote that is vague about either or that predicts generation well above the range for your orientation.</p>

    <h2>Where the value comes from: self-use versus export</h2>
    <p>Every unit your panels make is worth one of two things. If you use it in the house there and then, it saves you buying that unit from the grid, currently about 26p under the price cap. If you do not, it is exported and earns you the export rate instead. Power you use yourself is therefore worth more than power you export, but how much more depends on your export rate. On a low 5p export deal, self-used power is worth roughly five times as much, so self-consumption is everything. On one of the better 15p export deals now available, the gap narrows to under double, so exporting is far less of a loss than it used to be. Either way, the return rises the more of your own generation you consume, which is why a household with someone home in the day, or willing to shift the washing, dishwasher, hot water and car charging into daylight, gets more from the same panels than one that exports most of its midday output to an empty house.</p>

    <h2>Export rates in 2026, and the moving goalposts</h2>
    <p>You are paid for exported electricity through the Smart Export Guarantee, and the rates vary a great deal between suppliers. In 2026 flat export rates run from around 5p per kWh at the bottom to about 15p at the best, with a couple of deals near 16p that require you to also buy your electricity from the same supplier. Households with a battery can access time-of-use export tariffs that pay much more during peak evening windows, sometimes over 30p per kWh, though those need both a battery and that supplier's import tariff. Because these rates change and the price of the grid electricity you displace changes too, treat any single confident payback figure in a sales pitch with caution, and ask what export rate and what import price it assumed.</p>

    <h2>The payback, worked out</h2>
    <p>Put the numbers together for an example 4 kW system costing £7,500 and generating 3,600 kWh a year, displacing electricity at 26p and exporting the surplus at a 15p rate. The result depends heavily on how much you use yourself.</p>

    <table class="ev-table">
      <thead><tr><th>Self-consumption</th><th>Saved on bills</th><th>Export earnings</th><th>Total per year</th><th>Payback</th></tr></thead>
      <tbody>
        <tr><td>30% used at home</td><td>~£281</td><td>~£378</td><td>~£660</td><td>~11 years</td></tr>
        <tr><td>50% used at home</td><td>~£468</td><td>~£270</td><td>~£740</td><td>~10 years</td></tr>
        <tr><td>70% used at home</td><td>~£655</td><td>~£162</td><td>~£820</td><td>~9 years</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Example only: 4 kW system at £7,500, 3,600 kWh a year, 26p import, 15p export, mid 2026. On a low 5p export rate the totals fall and the gap between low and high self-consumption widens sharply, pushing a low user past fifteen years while a high user stays around ten. Your roof, prices and habits move all of these.</p>

    <h2>Where batteries fit</h2>
    <p>A <a href="solar-battery-storage.html">battery</a> stores your surplus midday generation for use in the evening, lifting self-consumption and the value of the system, especially for households out all day, and it unlocks the higher peak export tariffs mentioned above. The catch is the cost, typically several thousand pounds on top, so a battery improves the usefulness of solar while often lengthening the overall payback rather than shortening it. Whether to add one is a separate calculation, not an automatic yes. For some homes it transforms the case; for others, at today's better export rates, it is a costly extra the export payments would have covered more cheaply.</p>

    <h2>The honest long-term picture</h2>
    <p>A well-sited system with decent self-consumption pays for itself in roughly nine to twelve years at current prices and then generates largely free power for many years beyond, since panels last well over two decades. It is a long-term investment, closer to overpaying your mortgage than to a quick win, and it competes for your money with the cheaper efficiency jobs that pay back far faster. The sensible order is to do the <a href="loft-insulation.html">insulation</a>, <a href="draught-proofing.html">draught-proofing</a> and heating basics first, since they cost less and return sooner, and then consider solar as the larger, slower-burn step once the easy savings are banked.</p>

    <h2>Questions to ask before you sign</h2>
    <p>When you get a quote, ask what generation it predicts for your specific roof orientation and shading, not a generic figure; what self-consumption rate it assumes and why; what electricity price and export rate underpin the payback; whether a battery is included and what the sums look like without it; and what warranties cover the panels and, separately, the inverter, which is the component most likely to need replacing within the system's life. A reputable installer answers these plainly. Vague, pressured or too-good-to-be-true answers are the signal to walk away and get another quote.</p>

    <h2>The bottom line</h2>
    <p>In 2026 a well-sited 4 kW system costs around £7,000 to £8,500, generates 3,400 to 4,000 kWh a year, and returns roughly £650 to £820 of saved and earned money, paying back in about nine to twelve years before decades of nearly free power. The case is strongest on a good south-facing roof for a household that uses plenty of its own generation, and weakest on a poor or shaded roof or a low export rate. Do the cheap efficiency jobs first, get two or three honest quotes, and judge them on real generation and price assumptions rather than a single glossy payback number.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is solar worth it in 2026?","acceptedAnswer":{"@type":"Answer","text":"For a well-sited roof, usually yes over the long term. A typical 4 kW system costs around \\u00a37,000 to \\u00a38,500 installed with no VAT, generates 3,400 to 4,000 kWh a year, and returns roughly \\u00a3650 to \\u00a3820 a year in saved and exported electricity, paying back in about nine to twelve years and then producing largely free power for many years more. A poor or shaded roof or a low export rate make the case weaker."}},{"@type":"Question","name":"How much do solar panels cost in the UK in 2026?","acceptedAnswer":{"@type":"Answer","text":"A standard 4 kW domestic system, around ten panels, costs roughly \\u00a37,000 to \\u00a38,500 fully installed in 2026, including panels, inverter, mounting and electrical work. Residential solar carries no VAT. A battery, if added, typically costs several thousand pounds more."}},{"@type":"Question","name":"What is the payback time on solar panels?","acceptedAnswer":{"@type":"Answer","text":"Roughly nine to twelve years for a well-sited system at 2026 prices, displacing electricity at about 26p and exporting at a good 15p rate. The more of your own generation you use at home the faster it pays back. A low export rate or a poor roof can push payback past fifteen years."}},{"@type":"Question","name":"How much can you earn exporting solar electricity?","acceptedAnswer":{"@type":"Answer","text":"Under the Smart Export Guarantee, flat export rates in 2026 run from about 5p per kWh at the bottom to around 15p at the best, with a couple near 16p that require buying your electricity from the same supplier. Households with a battery can access peak export tariffs paying over 30p per kWh at certain times, but those need a battery and that supplier's import tariff."}}]}</script>
''',
)

PAGES["ev-charging-at-home-cost"] = dict(
    title="How much does it cost to charge an electric car at home?",
    description="A worked guide to the cost of charging an electric car at home in the UK: the cost of a full charge by battery size, the cost per mile on off-peak, standard and public rates, how home charging compares with petrol, and the tariff that decides it all.",
    active="guides",
    blurb="The cost of a full charge and the cost per mile, worked out for off-peak, standard and public rates.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Charging an electric car at home is the cheapest way to fuel a car there is, but only on the right tariff. The same car can cost 2p a mile or 8p a mile depending purely on when you plug in, and relying on public rapid chargers can cost more per mile than petrol. This guide works out the actual figures so you can see where you sit.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Charging is just buying electricity: the cost of a full charge is your battery size in kWh multiplied by your price per kWh. A typical car returns about 3.5 miles per kWh, so your cost per mile is simply your unit rate divided by 3.5. On a cheap overnight EV tariff that works out around 2p a mile; on a standard daytime rate around 7p a mile; on a public rapid charger more like 23p a mile.</p>
    </div>

    <h2>What a full charge costs</h2>
    <p>To charge from empty to full you pay for roughly the battery's usable capacity in kilowatt-hours, plus about 10 per cent on top for charging losses, which home AC charging always carries. The table below uses three real-world unit rates current in mid 2026: an off-peak EV rate of 8p, which is typical of dedicated EV tariffs running between about 7p and 9p; the standard price-cap rate of 26p; and a public rapid rate of 79p per kWh. Your own rates will differ, so put your real numbers through the <a href="appliance-running-cost.html">running cost calculator</a>.</p>

    <table class="ev-table">
      <thead><tr><th>Battery size</th><th>Off-peak (8p)</th><th>Standard (26p)</th><th>Public rapid (79p)</th></tr></thead>
      <tbody>
        <tr><td>40 kWh (small EV)</td><td>£3.20</td><td>£10.40</td><td>£31.60</td></tr>
        <tr><td>60 kWh (mid-size EV)</td><td>£4.80</td><td>£15.60</td><td>£47.40</td></tr>
        <tr><td>80 kWh (large EV)</td><td>£6.40</td><td>£20.80</td><td>£63.20</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Figures are the energy cost of a full charge at the rates above, before the roughly 10 per cent charging losses. In practice you rarely charge from completely empty to completely full, so a typical top-up costs less than the figures shown.</p>

    <h2>The cost per mile, and how far a charge goes</h2>
    <p>Cost per mile is the more useful number, because it lets you compare an EV directly with petrol. At about <a href="electric-car-miles-per-kwh.html">3.5 miles per kWh</a>, a full 60 kWh battery takes you roughly 210 miles, so you can read the cost of any journey straight off your unit rate.</p>

    <table class="ev-table">
      <thead><tr><th>Where you charge</th><th>Cost per mile</th><th>Cost of 100 miles</th></tr></thead>
      <tbody>
        <tr><td>Home, off-peak EV rate (8p)</td><td>2.3p</td><td>£2.29</td></tr>
        <tr><td>Home, standard rate (26p)</td><td>7.4p</td><td>£7.43</td></tr>
        <tr><td>Public rapid charger (79p)</td><td>22.6p</td><td>£22.57</td></tr>
        <tr><td>Petrol car at 50 mpg (£1.59/litre)</td><td>14.4p</td><td>£14.43</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Worked at 3.5 miles per kWh for the EV and 50 miles per gallon at £1.59 a litre for the petrol car. Cold weather, motorway speeds and a heavy right foot all push the EV figures up, just as they do a petrol car's.</p>
    <p class="ev-note">Rates checked June 2026: standard rate from the Ofgem price cap for July to September 2026 (26.11p per kWh); off-peak figure typical of dedicated EV tariffs (Intelligent Octopus Go, EDF GoElectric, British Gas EV, broadly 7p to 9p in the overnight window); public rapid average 79p per kWh from the Zapmap price index; petrol at the June 2026 UK average of about 159p a litre. Always check your own tariff and local pump price.</p>

    <h2>Why the tariff is everything</h2>
    <p>Look again at that table. The car has not changed between the first two rows, only the time of day you charged. A standard daytime rate makes an EV reasonably cheap; a dedicated overnight EV tariff, where the unit price in the small hours is a fraction of the daytime rate, drops the cost per mile to a level petrol cannot touch. This is the single biggest lever you control, and it dwarfs anything to do with the car itself. Getting a <a href="smart-meters-explained.html">smart meter</a> and moving onto a time-of-use or EV tariff is close to essential to get the most from charging at home. It is worth comparing the EV tariffs on offer, because the size of the off-peak window and the gap between the cheap and peak rates vary a good deal between them.</p>

    <h2>Home charger versus the three-pin plug</h2>
    <p>You can charge from an ordinary three-pin socket, but it is slow, adding only around 8 miles of range an hour, and a domestic socket is not designed for many hours of heavy continuous draw. A dedicated 7kW home wall charger is far quicker at roughly 25 to 30 miles of range an hour, safer for sustained charging, and crucially can be set to run only during your cheap off-peak window automatically. For anyone charging regularly at home, a proper charger usually earns its keep through convenience and by making off-peak charging effortless rather than something you have to start and stop by hand at midnight. The <a href="home-ev-charger-vs-3-pin-plug.html">3-pin plug versus 7kW wallbox</a> guide works through who genuinely needs a wallbox and who can manage on the cable that came with the car.</p>

    <h2>Home versus public charging</h2>
    <p>Home off-peak charging is the cheapest option by a wide margin, and as the cost-per-mile table shows, public rapid charging can actually cost more per mile than running a petrol car. You are paying for speed, convenience and the cost of the infrastructure. That is a fair deal as an occasional top-up on a long journey, but a driver who relies on rapid chargers for everyday miles throws away most of the running-cost advantage an EV should give. The model that saves the most is simple: do the bulk of your charging slowly and cheaply at home overnight, and use public chargers only to extend range on longer trips.</p>

    <h2>How it compares with petrol</h2>
    <p>On an off-peak home tariff an electric car is dramatically cheaper to fuel than petrol, around six times cheaper per mile in the worked example above. Even on a standard daytime rate it is usually cheaper, though by a smaller margin. The fuel saving is one of the clearest running-cost advantages of going electric, but it should be weighed against the whole picture of buying and owning the car rather than taken alone. A fuller side-by-side of fuel, servicing and the rest is in the <a href="ev-running-cost-vs-petrol.html">EV versus petrol running cost</a> guide, and the <a href="ev-cost-vs-petrol-per-year.html">year of charging versus a year of petrol</a> guide puts real annual figures on it. If you are still running a combustion car, the habits on the <a href="hypermiling.html">hypermiling</a> and <a href="driving.html">fuel and driving</a> pages are the way to trim its thirst; if you have gone electric, the equivalent skill is simply charging at the right time, which the <a href="best-time-to-charge-an-electric-car.html">best time to charge</a> guide covers in detail.</p>

    <h2>The bottom line</h2>
    <p>Charging an electric car at home costs whatever your unit rate says it does, and the rate is yours to choose. On a cheap overnight tariff a full charge of a mid-size car is a few pounds and your motoring costs about 2p a mile, which nothing burning petrol can match. Charge at the standard daytime rate and it is still cheaper than petrol, just less spectacularly. Lean on public rapid chargers for daily miles and you give the advantage back. Sort the tariff, charge overnight, and home charging is as cheap as motoring gets.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to charge an electric car at home?","acceptedAnswer":{"@type":"Answer","text":"A full charge costs your battery size in kWh multiplied by your electricity unit rate. For a 60 kWh car that is about \\u00a34.80 on an 8p off-peak EV rate, about \\u00a315.60 on the 26p price-cap standard rate, and far more on a public rapid charger. Cost per mile is your unit rate divided by roughly 3.5, so about 2p a mile off-peak and 7p a mile on a standard rate."}},{"@type":"Question","name":"Is it cheaper to charge an electric car at home than at public chargers?","acceptedAnswer":{"@type":"Answer","text":"Yes, by a wide margin. Home off-peak charging is around 2p a mile, while public rapid charging can be over 20p a mile, which is more than running a petrol car. Charge at home overnight and use public chargers only to extend range on long trips."}},{"@type":"Question","name":"Is it cheaper to charge an electric car at home than to run a petrol car?","acceptedAnswer":{"@type":"Answer","text":"On an off-peak home tariff an electric car costs around 2p a mile against roughly 14p a mile for a 50 mpg petrol car at \\u00a31.59 a litre, about six times cheaper. On a standard daytime electricity rate it is around 7p a mile, still cheaper than petrol but by less."}},{"@type":"Question","name":"How much does it cost to fully charge an electric car?","acceptedAnswer":{"@type":"Answer","text":"A full charge costs the usable battery capacity in kWh times your unit rate, plus about 10 per cent for charging losses. At an example 8p off-peak rate that is about \\u00a33.20 for a 40 kWh car, \\u00a34.80 for 60 kWh and \\u00a36.40 for 80 kWh."}}]}</script>
''',
)

PAGES["best-time-to-charge-an-electric-car"] = dict(
    title="The best time to charge an electric car",
    description="When to charge an electric car to pay the least: why the overnight off-peak window is so much cheaper, how to schedule charging automatically, charging from solar, and the timing that is kindest to the battery.",
    active="guides",
    blurb="The cheapest time to charge is the overnight off-peak window. How to make sure your car always uses it.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">With an electric car, when you charge matters far more than how you charge. The electricity itself is the same; what changes is the price per unit at different times of day. Get the timing right and your motoring costs a couple of pence a mile, cheaper than anything burning petrol. Get it wrong and you pay several times over for the very same miles.</p>

    <h2>The cheapest time is the overnight off-peak window</h2>
    <p>On a time-of-use or dedicated EV tariff, electricity in the small hours costs a fraction of the daytime rate, because demand on the grid is low and suppliers want to soak up cheap overnight generation. Charging in that window, rather than during the day, is the single biggest saving you can make on running an electric car. As the <a href="ev-charging-at-home-cost.html">cost of charging at home</a> guide shows, the same car can cost about 2p a mile charged off-peak against around 7p a mile on a standard daytime rate, with no change to the car at all. The whole game is making sure your charging happens in that cheap window.</p>

    <h2>You need the right tariff first</h2>
    <p>None of this works on a flat single-rate tariff, where electricity costs the same at three in the morning as at six in the evening. To unlock cheap overnight charging you need a <a href="smart-meters-explained.html">smart meter</a> and a time-of-use or EV tariff that has a defined off-peak window. These typically offer a set block of cheap hours overnight, often something like five hours in the small hours, though the length of the window and the gap between the cheap and peak rates vary between tariffs. It pays to compare them on those two points, because a wider window and a deeper discount are what make the saving large.</p>

    <h2>Avoid the peak</h2>
    <p>The flip side of the cheap window is an expensive one. Many time-of-use tariffs charge a premium during the early-evening peak, roughly the late afternoon to mid evening when the whole country gets home and switches things on. Charging then is the worst case, paying the top rate for energy you could have bought for a fraction overnight. If your car plugs in when you get home and starts charging immediately, it is drinking at the most expensive time of day. The answer is not to babysit the plug, but to schedule the charge so it waits for the cheap hours.</p>

    <h2>How to charge automatically in the cheap window</h2>
    <p>You should never have to set an alarm for the small hours. There are three ways to make charging happen off-peak on its own. Most electric cars let you set a charging schedule in the car itself, so it will not draw power until the time you specify even if it is plugged in earlier. Most dedicated home wall chargers can do the same, holding off until a set window. And some smart EV tariffs go further, taking control of the charging themselves to fill the car during the cheapest hours, sometimes spreading it across the night to catch the very lowest prices. Any of these turns plugging in when you get home into a charge that quietly happens at the cheap rate while you sleep.</p>

    <h2>If you have solar, daytime can be cheaper still</h2>
    <p>There is one exception to the overnight rule. If you have <a href="solar-panels-the-basics.html">solar panels</a>, the cheapest electricity you will ever have is the surplus your own roof generates on a sunny day, which would otherwise be exported for a low rate. Charging the car from that midday surplus costs you nothing beyond what you have already spent on the panels. Some chargers can be set to draw only from solar surplus, topping up the car whenever the panels are producing more than the house is using. For a solar household the best time to charge can be the middle of a sunny day rather than the dead of night, and the <a href="solar-battery-storage.html">solar battery</a> guide covers the related question of storing that surplus.</p>

    <h2>Timing that is kinder to the battery</h2>
    <p>The cheap overnight window happens to line up with what is best for the battery's long-term health, which is a happy coincidence. Slow AC charging at home is gentler on the cells than repeated rapid charging, and for daily use it is better not to sit the battery at a full 100 per cent or run it to empty. A common approach is to set the charge limit to around 80 per cent for everyday driving and only fill to 100 per cent before a long trip. Scheduling the charge to finish shortly before you leave in the morning, rather than hitting full at midnight and sitting there for hours, is gentler still. Off-peak overnight charging gives you all of this for free as a side effect of chasing the cheap rate.</p>

    <h2>Cold mornings: precondition while plugged in</h2>
    <p>In winter, warming the car's cabin and battery while it is still plugged in, rather than after you set off, draws that energy from the cheap mains supply instead of from the battery on the road. Most electric cars let you schedule preconditioning to finish around your departure time. Done while still on the charger in the off-peak window, it costs little and means you set off with a warm cabin and a battery already at temperature, which also improves your range for the journey. The <a href="ev-charging-in-winter.html">EV charging in winter</a> guide covers the cold-weather range loss and how to limit it in full.</p>

    <h2>The bottom line</h2>
    <p>The best time to charge an electric car is overnight, in the off-peak window of a time-of-use or EV tariff, set to run automatically so you never think about it. If you have solar, a sunny midday is better still. Avoid charging during the early-evening peak, schedule rather than babysit, and let the cheap hours do the work. Combined with the figures in the <a href="ev-charging-at-home-cost.html">cost of home charging</a> guide, this is what turns an electric car into the cheapest thing on the road to fuel.</p>
  </div></section>
''',
)

PAGES["electric-car-miles-per-kwh"] = dict(
    title="How many miles per kWh do electric cars get?",
    description="What miles per kWh means, the real-world efficiency of different electric cars, what drags it down in cold weather and at speed, how to measure your own, and why this one number decides your cost per mile.",
    active="guides",
    blurb="The efficiency figure that decides your cost per mile. Real-world numbers by car type and what drags them down.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Miles per kWh is the electric car's version of miles per gallon, and it is the single number that decides what your motoring costs. Most cars sit somewhere between 3 and 4 miles for every kilowatt-hour, with an average of around 3.5, but the spread is wide and the conditions you drive in move it about far more than people expect. This guide explains what the figure means, what real cars actually return, and how to find your own.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A typical electric car returns about 3 to 4 miles per kWh, averaging roughly 3.5. Small, light, aerodynamic cars manage 4 to 4.5 or better; large SUVs and performance models drop to 2.5 to 3. Cold weather, motorway speeds, a heavy load and hard acceleration all cut the figure, sometimes by a third in deep winter. Your cost per mile is simply your electricity unit rate divided by your miles per kWh.</p>
    </div>

    <h2>What miles per kWh actually means</h2>
    <p>A kilowatt-hour is a unit of energy, the same unit your electricity bill is priced in. Miles per kWh tells you how far the car travels on one of those units, so a car doing 3.5 miles per kWh covers three and a half miles for each unit it draws from the battery. It is the mirror image of the energy figure carmakers sometimes quote the other way round, in watt-hours per mile or per kilometre, where a lower number is better. Miles per kWh is the friendlier way to think about it for everyday sums, because it slots straight into a cost calculation: take what you pay per unit, divide by your miles per kWh, and you have your cost per mile. On a cheap overnight rate that lands around 2p a mile, which is the figure that makes an electric car so cheap to run, as the <a href="ev-charging-at-home-cost.html">cost of charging at home</a> guide sets out in full.</p>

    <h2>What real cars return</h2>
    <p>Manufacturer figures from the official test tend to flatter real driving, much as the old mpg figures did, so it is worth working from real-world numbers. As a rough guide, efficiency tracks the size, weight and shape of the car. A small, light, slippery hatchback is the most efficient thing on the road; a tall, heavy SUV or a fast performance car pushes more air aside and carries more mass, so it uses more energy for the same distance.</p>

    <table class="ev-table">
      <thead><tr><th>Type of car</th><th>Typical miles per kWh</th><th>Cost per mile off-peak (8p)</th><th>Range from 60 kWh</th></tr></thead>
      <tbody>
        <tr><td>Small, efficient EV</td><td>4.0 to 4.5</td><td>1.8p to 2.0p</td><td>240 to 270 mi</td></tr>
        <tr><td>Mid-size hatch or saloon</td><td>3.3 to 3.8</td><td>2.1p to 2.4p</td><td>200 to 230 mi</td></tr>
        <tr><td>Large SUV or performance EV</td><td>2.5 to 3.0</td><td>2.7p to 3.2p</td><td>150 to 180 mi</td></tr>
        <tr><td>Rough average across all</td><td>3.5</td><td>2.3p</td><td>210 mi</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Cost per mile worked at an example 8p off-peak EV rate; multiply through for your own rate (for instance at the 26p standard rate the figures are roughly three times higher). Range assumes a usable 60 kWh battery. These are mild-weather, mixed-driving figures; winter and motorway use sit lower.</p>

    <h2>What drags the figure down</h2>
    <p>The number on a spec sheet is a best case, and four things in particular pull your real efficiency below it. Cold is the largest. In winter the battery is less willing to give up its energy, and far more importantly the car has to heat the cabin from the battery rather than from waste engine heat as a petrol car does, so short cold trips can knock 20 to 30 per cent off your miles per kWh. The <a href="ev-charging-in-winter.html">EV charging in winter</a> guide goes into this in detail. Speed is the next: air resistance climbs steeply with speed, so a steady motorway cruise uses noticeably more energy per mile than town driving, which is the reverse of what people expect from a petrol car. Town driving actually suits an EV, because regenerative braking claws back energy every time you slow down. Weight and load matter too, so a full car, a roof box or a towed trailer all cost range. And a heavy right foot, with hard acceleration and high speeds, drains the battery far faster than a gentle, anticipatory style.</p>

    <h2>Why town driving beats the motorway</h2>
    <p>This catches a lot of new EV drivers out. In a petrol car, stop-start town driving is the thirsty bit and a steady motorway run is where you see your best economy. An electric car flips that. Regenerative braking means that much of the energy you would lose slowing for a junction is recovered back into the battery, so urban driving, full of gentle slowing and stopping, is where an EV is most efficient. The motorway, where you hold a high steady speed against rising air resistance and rarely brake, is where efficiency is worst. It is why a long fast journey eats range faster than the same miles around town, and why easing off the motorway speed is the single most effective thing you can do to stretch a charge on a long trip.</p>

    <h2>How to measure your own</h2>
    <p>You do not have to guess, because every electric car tracks this for you. The dashboard or the trip computer shows a lifetime and a recent average efficiency, usually in miles per kWh or watt-hours per mile, and watching it over a few weeks tells you your real figure far better than any published number. If you want to check it independently, note the odometer and the energy used between two full charges, or simply divide the miles you covered on a charge by the kWh you put back in. Knowing your own figure is what makes the cost sums real: drop it into the <a href="appliance-running-cost.html">running cost calculator</a> alongside your unit rate, or just divide your rate by your miles per kWh, and you have your true cost per mile rather than an average that may not match how or where you drive.</p>

    <h2>Why this number matters</h2>
    <p>Miles per kWh is the hinge between two things you do control, your tariff and your driving style, and the thing you care about, the cost of every mile. A more efficient car needs less energy for the same journey, so it costs less to run and goes further on a charge, but the conditions you drive in swing the figure enough that the same car can feel cheap in summer and thirsty in a cold snap. Pair a good real-world efficiency with a cheap overnight rate and the right charging habits, covered in the <a href="best-time-to-charge-an-electric-car.html">best time to charge</a> guide, and you reach the couple-of-pence-a-mile figure that no petrol car can match. The car matters, but as ever the tariff and the timing matter more.</p>

    <h2>The bottom line</h2>
    <p>Most electric cars return between 3 and 4 miles per kWh, around 3.5 on average, with small efficient cars doing better and large or fast ones worse. Cold weather, high speeds, heavy loads and hard driving all cut the figure, while gentle town driving and regenerative braking lift it. Watch your own car's readout for your true number, divide your unit rate by it for your cost per mile, and you will know exactly what your motoring costs rather than relying on a showroom figure.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How many miles per kWh does an electric car get?","acceptedAnswer":{"@type":"Answer","text":"Most electric cars return about 3 to 4 miles per kWh, averaging roughly 3.5. Small, efficient cars manage 4 to 4.5 or more, while large SUVs and performance cars drop to 2.5 to 3. Cold weather and motorway speeds can cut the figure by 20 to 30 per cent."}},{"@type":"Question","name":"What is a good miles-per-kWh figure?","acceptedAnswer":{"@type":"Answer","text":"Anything around 4 miles per kWh or better is good and typical of small, efficient cars. The average across all electric cars is about 3.5. Large or fast cars at 2.5 to 3 are normal for their size. The figure you actually achieve depends as much on weather, speed and driving style as on the car."}},{"@type":"Question","name":"Why does my electric car's range drop in winter?","acceptedAnswer":{"@type":"Answer","text":"Cold reduces miles per kWh in two ways: the battery gives up its energy less readily when cold, and the car must heat the cabin from the battery rather than from engine waste heat. Together these can cut efficiency by 20 to 30 per cent on short cold trips."}},{"@type":"Question","name":"How do I work out my cost per mile from miles per kWh?","acceptedAnswer":{"@type":"Answer","text":"Divide your electricity unit rate by your miles per kWh. At an 8p off-peak rate and 3.5 miles per kWh that is about 2.3p a mile; at the 26p standard rate it is about 7.4p a mile. Use your car's own efficiency readout for the most accurate figure."}}]}</script>
''',
)

PAGES["home-ev-charger-vs-3-pin-plug"] = dict(
    title="Do you need a home EV charger? 3-pin plug vs 7kW wallbox",
    description="Charging an electric car from an ordinary three-pin plug versus a dedicated 7kW home wallbox: the charge speeds compared, what a wallbox costs to fit, when a granny cable is genuinely enough, and why automatic off-peak charging tips the balance.",
    active="guides",
    blurb="A granny cable adds about 8 miles an hour; a 7kW wallbox three times that. When the slow plug is enough, and when it isn't.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">You do not strictly need a dedicated home charger to run an electric car. Every car comes able to charge from an ordinary three-pin socket, and for some drivers that is genuinely enough. But a proper 7kW wallbox charges roughly three times faster, is built for the sustained load, and can schedule itself to run only in your cheap overnight window. This guide works out who actually needs one and who can manage without.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A three-pin plug, the so-called granny cable, adds about 8 miles of range an hour. A 7kW home wallbox adds roughly 25 to 30. If you drive modest daily miles and park off-street overnight, a granny cable can keep up; if you cover bigger distances or want charging to happen automatically in the cheap hours, a wallbox earns its keep. Fitting one typically costs somewhere in the region of 800 to 1,200 pounds installed, and you need off-street parking to put it on.</p>
    </div>

    <h2>The two ways to charge at home</h2>
    <p>Home charging comes in two forms. The first is the cable supplied with the car, which plugs into a normal three-pin domestic socket. It is often nicknamed a granny cable, and it draws a modest amount of power, limited to what a household socket can safely deliver continuously, usually around 2.3 kilowatts. The second is a dedicated wall-mounted charge point, a wallbox, wired into your home's electrical supply on its own circuit and typically rated at 7kW. That is roughly three times the power, and the difference shows up entirely in how fast the car fills.</p>

    <table class="ev-table">
      <thead><tr><th>Charging method</th><th>Power</th><th>Range added per hour</th><th>Empty to full, 60 kWh</th></tr></thead>
      <tbody>
        <tr><td>Three-pin plug (granny cable)</td><td>~2.3 kW</td><td>~8 miles</td><td>~24 to 26 hours</td></tr>
        <tr><td>7kW home wallbox</td><td>7 kW</td><td>~25 to 30 miles</td><td>~8 to 9 hours</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Range added per hour assumes about 3.5 miles per kWh; see the <a href="electric-car-miles-per-kwh.html">miles per kWh</a> guide. Charging from completely empty to completely full is rare in practice; most home charging is an overnight top-up of whatever you used that day.</p>

    <h2>Why the granny cable can be enough</h2>
    <p>The slow figure looks alarming until you do the arithmetic on real driving. The average car covers well under 30 miles a day, and at 8 miles of range an hour a three-pin plug replaces that in around four hours, comfortably inside an overnight charge. If you park off-street, plug in every evening, and drive ordinary daily distances, the granny cable quietly keeps the battery topped up while you sleep, and you may never need anything faster. It is the long charge from near-empty, or the day you come home late and need a big top-up before an early start, that exposes its limits. As an everyday trickle for a modest commute, though, it genuinely works, and starting with it costs nothing extra.</p>

    <h2>Where the granny cable falls short</h2>
    <p>Two things count against relying on a three-pin plug. The first is simply speed: if you drive bigger daily miles, or need to recover a lot of range overnight, 8 miles an hour cannot always keep up, and you can wake to a car that is not charged enough for the day. The second is the load. A domestic socket and its wiring are not designed for many hours of heavy continuous draw night after night, and an old or worn socket can run warm under that duty. A granny cable should be plugged straight into a known-good wall socket, never through an extension lead or a multi-way adaptor, and it is worth having the socket and circuit checked if you intend to lean on it regularly. A wallbox sidesteps the problem entirely, because it is purpose-built for exactly this job.</p>

    <h2>The case for a 7kW wallbox</h2>
    <p>A dedicated wallbox buys three things. The obvious one is speed, refilling the car in a single overnight window even from a low state of charge, so charging never becomes the thing you have to plan around. The second is that it is designed for sustained charging on its own protected circuit, which is safer and steadier than asking a household socket to do the work for hours on end. The third, and quietly the most valuable, is control. A wallbox can be set to charge only during your cheap off-peak hours, switching on and off by itself, so plugging in when you get home becomes a charge that happens automatically at the lowest rate while you sleep. That automatic off-peak scheduling, covered in the <a href="best-time-to-charge-an-electric-car.html">best time to charge</a> guide, is what turns the theoretical 2p-a-mile cost from the <a href="ev-charging-at-home-cost.html">home charging cost</a> guide into what you actually pay, without you having to babysit a plug at midnight.</p>

    <h2>What a wallbox costs and what you need</h2>
    <p>Fitting a 7kW home charger typically runs somewhere in the region of 800 to 1,200 pounds including installation, depending on the unit you choose and how far it sits from your fuse board, with a long or awkward cable run adding to the labour. The practical requirement is off-street parking, a driveway or garage where the car sits next to the wall the box mounts on, since you cannot trail a cable across a public pavement. The installer will check your home's electrical supply and consumer unit can take the extra circuit, which most modern installations can. Support schemes exist in some cases, for instance for people in rented homes or flats without their own driveway, but the details and eligibility change, so check the current position rather than assuming a grant applies. Set against years of cheap, effortless overnight charging, the one-off cost is usually money well spent for anyone charging at home regularly.</p>

    <h2>Which one suits you</h2>
    <p>The honest dividing line is your mileage and your parking. If you have off-street parking, drive modest daily distances, and are happy to plug in every night, start with the granny cable that came with the car and see whether it keeps up, because it may well do and it costs nothing to try. If you cover bigger miles, sometimes need a large overnight top-up, or simply want charging to handle itself in the cheap hours without thought, a 7kW wallbox is worth fitting and quickly becomes invisible in the good way. What matters far more than which one you use is that you are charging at home at all, on the right tariff, in the off-peak window. Get that right and either method delivers the running-cost advantage that makes an electric car so cheap to fuel.</p>

    <h2>The bottom line</h2>
    <p>A three-pin granny cable adds about 8 miles of range an hour, which is enough for modest daily driving with off-street parking, but it is slow, leans hard on a domestic socket, and means manual timing. A 7kW wallbox adds three times the range an hour, is built for the load, and crucially schedules itself into your cheap overnight window. For light users the cable is a fine free start; for everyone charging regularly at home, the wallbox pays its way in speed, safety and effortless off-peak charging.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Can you charge an electric car from a normal three-pin plug?","acceptedAnswer":{"@type":"Answer","text":"Yes. Every electric car comes with a cable that plugs into an ordinary three-pin socket, drawing about 2.3 kW and adding roughly 8 miles of range an hour. It is fine for modest daily mileage with overnight charging, but plug it straight into a sound wall socket, never an extension lead, and have the socket checked if you use it heavily."}},{"@type":"Question","name":"How much faster is a 7kW wallbox than a three-pin plug?","acceptedAnswer":{"@type":"Answer","text":"About three times faster. A three-pin plug adds around 8 miles of range an hour, while a 7kW wallbox adds roughly 25 to 30. A 60 kWh battery takes about 8 to 9 hours from empty on a wallbox against around a full day on a three-pin plug."}},{"@type":"Question","name":"Do I need a home charger for an electric car?","acceptedAnswer":{"@type":"Answer","text":"Not necessarily. If you drive modest daily miles and park off-street, the supplied three-pin cable can keep the car topped up overnight. A dedicated 7kW wallbox is worth it if you cover bigger distances or want charging to run automatically in your cheap off-peak window."}},{"@type":"Question","name":"How much does it cost to install a home EV charger?","acceptedAnswer":{"@type":"Answer","text":"A 7kW home wallbox typically costs somewhere around 800 to 1,200 pounds installed, depending on the unit and the cable run to your fuse board. You need off-street parking to fit one. Support schemes exist in some cases, such as for renters or flats, but eligibility changes, so check the current position."}}]}</script>
''',
)

PAGES["ev-charging-in-winter"] = dict(
    title="EV charging in winter: range loss and how to limit it",
    description="Why electric cars lose range in cold weather, how much to expect, why rapid charging slows when the battery is cold, and the practical habits that claw most of it back: preconditioning, charging while plugged in, and parking warm.",
    active="guides",
    blurb="Cold can cut range by a fifth or more, mostly through cabin heating. Preconditioning and a few habits claw most of it back.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Every electric car loses range in winter, and the drop is real enough to catch people out on a cold morning. The good news is that most of the loss comes from heating the cabin rather than from any harm to the battery, which means a few simple habits, above all warming the car while it is still plugged in, claw most of it back. This guide explains why cold costs range, how much to expect, and what to do about it.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Expect to lose roughly 10 to 30 per cent of your range in cold weather, with the worst hit on short trips that never let the car warm through. Most of the loss is cabin heating drawn from the battery, not the battery itself failing. Rapid charging is also slower when the battery is cold. Precondition the car while it is plugged in, charge to a higher percentage in winter, and the cold becomes a manageable nuisance rather than a problem.</p>
    </div>

    <h2>Why cold cuts your range</h2>
    <p>Two things conspire in winter, and the smaller one gets most of the blame. The first is the battery itself: lithium cells are simply less willing to give up and take on energy when they are cold, so a freezing battery delivers a little less usable capacity and charges more slowly until it warms. The second, and by far the larger drain, is heating the cabin. A petrol car warms itself almost for free using waste heat from the engine; an electric car has no such waste heat, so every bit of warmth for the cabin, the screen and your seat comes straight out of the battery that would otherwise be driving you forward. On a cold day that heating load is substantial, and it is why the range gauge falls fastest in the first few miles before the car has warmed through.</p>

    <h2>How much range you lose</h2>
    <p>The honest figure is a range, not a single number, because it depends on how cold it is and how you drive. A mild, damp winter day might cost you only a little, while a hard frost on a short stop-start journey can take 30 per cent or more, because the car spends the whole trip heating a cold cabin and never settles into its efficient stride. Longer journeys fare better proportionally, since the heavy initial warm-up is spread over more miles. The effect shows up as a lower <a href="electric-car-miles-per-kwh.html">miles per kWh</a> figure, so the same charge takes you less far. It is worth planning winter journeys with a margin rather than to the last mile of the summer range, and treating the dashboard estimate as optimistic until the car is warm.</p>

    <table class="ev-table">
      <thead><tr><th>Conditions</th><th>Typical range loss</th></tr></thead>
      <tbody>
        <tr><td>Mild winter day, longer journey</td><td>around 10%</td></tr>
        <tr><td>Cold day, mixed driving</td><td>around 15 to 20%</td></tr>
        <tr><td>Hard frost, short stop-start trips</td><td>25 to 30% or more</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Indicative figures; the exact loss varies by car, temperature and journey. The pattern is consistent: the colder it is and the shorter the trip, the bigger the hit, because cabin heating is spread over fewer miles.</p>

    <h2>Why rapid charging slows in the cold</h2>
    <p>Cold does not only shorten range, it slows charging. A cold battery cannot safely accept energy as fast as a warm one, so if you pull up to a public rapid charger with a cold battery, the charge rate can be well below the headline figure, and the session takes longer than you expect. Many electric cars get round this by preconditioning the battery, gently warming it to its ideal charging temperature on the approach to a charger, often automatically when you set a rapid charger as your navigation destination. If your car offers that, use it on a winter trip, because arriving with a warm battery can roughly halve the time at the charger compared with turning up cold. Home charging is less affected, because the slow overnight rate sits well within what even a cold battery can take.</p>

    <h2>Precondition while plugged in</h2>
    <p>This is the single most useful winter habit, and it is the heart of the matter. Preconditioning means warming the cabin and the battery before you set off. Do it while the car is still plugged in at home and that energy comes from the mains rather than from the battery, so you start your journey with a warm car, a clear screen and a battery at temperature, all without spending a single mile of range. Most electric cars let you schedule this to finish around your usual departure time, and a wallbox makes it effortless. Timed to land at the end of your cheap <a href="best-time-to-charge-an-electric-car.html">off-peak window</a>, it costs very little and means you never scrape ice or set off into the cold drawing heat from a battery you need for the drive. Warming the car off the battery on the road is exactly the drain you are trying to avoid, so shifting it onto the mains while plugged in is close to free range.</p>

    <h2>Practical winter habits</h2>
    <p>A handful of small things add up. Charge to a higher percentage in winter than you might in summer, since the usable range is lower and you want the margin. Lean on the seat and steering-wheel heaters, which warm you directly for a fraction of the energy of heating the whole cabin, and ease back on the cabin blower once you are warm. Park in a garage or somewhere sheltered if you can, because a battery that starts the day less cold loses less to warming up. Keep a little more charge in the battery overnight in very cold spells, as a warmer, fuller battery copes better with the cold. And drive gently in the first few miles while everything warms through. None of these is dramatic on its own, but together they recover a good slice of the range the cold takes, and they cost nothing.</p>

    <h2>The battery is not being harmed</h2>
    <p>It is worth saying plainly, because the winter range drop worries people: the lost range is temporary and the battery is not being damaged. Capacity returns in full when the weather warms, and the cold-weather behaviour is just physics, not wear. If anything, gentle slow home charging in winter is kinder to the battery than repeated cold rapid charging, which is another reason to do the bulk of your charging overnight at home. Treat the winter dip as a seasonal nuisance to plan around rather than a fault, manage it with preconditioning and sensible habits, and an electric car gets through a British winter perfectly well.</p>

    <h2>The bottom line</h2>
    <p>Electric cars lose roughly 10 to 30 per cent of their range in cold weather, mostly because cabin heating comes from the battery rather than from waste engine heat, and rapid charging slows when the battery is cold. The fix is to precondition the car while it is plugged in, so the warm-up comes from the mains not the road, charge to a higher level in winter, use the seat heaters over the cabin heater, and keep the car sheltered. Do that and the cold becomes a planning detail, not a problem, and the battery comes to no lasting harm. Heat costs range too, in its own way, which the <a href="ev-range-in-hot-weather.html">EV range in hot weather</a> guide covers.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much range does an electric car lose in winter?","acceptedAnswer":{"@type":"Answer","text":"Typically 10 to 30 per cent, with the worst loss on short stop-start trips in a hard frost and the least on longer journeys in milder cold. Most of the loss is cabin heating drawn from the battery rather than any fault in the battery itself, and the range returns in full when the weather warms."}},{"@type":"Question","name":"Why does my EV charge slower in cold weather?","acceptedAnswer":{"@type":"Answer","text":"A cold battery cannot safely accept energy as quickly as a warm one, so rapid charging slows until it warms. Preconditioning the battery on the approach to a charger, which many cars do automatically when you navigate to one, can roughly halve the time compared with arriving cold. Slow home charging is barely affected."}},{"@type":"Question","name":"What is preconditioning on an electric car?","acceptedAnswer":{"@type":"Answer","text":"Preconditioning means warming the cabin and battery before you drive. Done while the car is still plugged in, the energy comes from the mains rather than the battery, so you set off warm with a battery at temperature and lose no range to the warm-up. Most cars let you schedule it to finish around your departure time."}},{"@type":"Question","name":"Does cold weather damage an EV battery?","acceptedAnswer":{"@type":"Answer","text":"No. The winter range drop is temporary and the capacity returns in full when it warms. Gentle slow home charging in winter is actually kinder to the battery than repeated cold rapid charging, so doing most of your charging overnight at home is best in the cold."}}]}</script>
''',
)

PAGES["ev-cost-vs-petrol-per-year"] = dict(
    title="A year of EV charging vs a year of petrol",
    description="What an electric car costs to fuel over a whole year compared with petrol, worked at typical mileage on off-peak, standard and public charging, why the tariff swings the answer so much, and how to do the sum for your own mileage.",
    active="guides",
    blurb="The annual fuel bill, worked out: a few hundred pounds on an off-peak tariff against four figures for petrol.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">The cost-per-mile figures for an electric car are striking, but they only land properly when you stretch them across a whole year of driving. Do that and the gap becomes a real sum of money: a few hundred pounds to fuel an EV at home on the right tariff against well over a thousand for a petrol car covering the same miles. The catch is that the tariff swings the answer enormously, so this guide works the annual figures and shows what decides them.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> At a typical 7,500 miles a year, an electric car charged on an off-peak home tariff costs around 170 pounds in electricity, against roughly 1,080 pounds of petrol for a 50 mpg car. On a standard daytime electricity rate the EV costs about 560 pounds, still well under petrol. Rely on public rapid chargers for everything, though, and the annual cost climbs past the petrol figure. The tariff, not the car, decides where you land.</p>
    </div>

    <h2>How the annual sum is built</h2>
    <p>The arithmetic is simple once you have three numbers: your annual mileage, the car's efficiency in <a href="electric-car-miles-per-kwh.html">miles per kWh</a>, and your price per unit. Divide the miles by the miles per kWh to get the kilowatt-hours you use in a year, then multiply by your unit rate. The worked figures below use 7,500 miles, close to the average for a UK car, an efficiency of 3.5 miles per kWh, and the same three real rates as the rest of the EV guides: an 8p off-peak EV rate, the 26p standard price-cap rate, and a 79p public rapid rate. The petrol comparison uses a 50 mpg car at 159p a litre. At 3.5 miles per kWh, 7,500 miles needs about 2,140 kWh of electricity over the year.</p>

    <table class="ev-table">
      <thead><tr><th>How you fuel it</th><th>Cost over 7,500 miles</th><th>Cost over 12,000 miles</th></tr></thead>
      <tbody>
        <tr><td>EV, home off-peak (8p)</td><td>~£170</td><td>~£275</td></tr>
        <tr><td>EV, standard rate (26p)</td><td>~£560</td><td>~£895</td></tr>
        <tr><td>EV, public rapid only (79p)</td><td>~£1,690</td><td>~£2,710</td></tr>
        <tr><td>Petrol car, 50 mpg (£1.59/l)</td><td>~£1,080</td><td>~£1,735</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Electricity at 3.5 miles per kWh; petrol at 50 mpg and 159p a litre. Rates checked June 2026: standard rate from the Ofgem price cap for July to September 2026 (26.11p per kWh); off-peak typical of dedicated EV tariffs (broadly 7p to 9p overnight); public rapid average 79p per kWh from the Zapmap price index; petrol at the June 2026 UK average of about 159p a litre. Your own mileage, efficiency and rates will differ.</p>

    <h2>The off-peak case: a few hundred pounds a year</h2>
    <p>The headline that makes people switch is in the top row. Fuel an electric car overnight on a dedicated EV tariff and a year of average driving costs less than 200 pounds in electricity. The same miles in a 50 mpg petrol car cost over a thousand, so the EV is roughly six times cheaper to fuel, a saving of the better part of 900 pounds a year that repeats every year you own the car. That is the real prize of home charging, and it rests entirely on getting onto a time-of-use tariff and charging in the cheap window, which the <a href="best-time-to-charge-an-electric-car.html">best time to charge</a> guide covers. Without that tariff the saving is far smaller, which is why sorting the tariff is the first thing to do, not the last.</p>

    <h2>The standard rate: still cheaper, by less</h2>
    <p>Not everyone can get onto an EV tariff, and charging at the standard price-cap rate tells a gentler version of the same story. At 26p a unit, a year of average driving costs around 560 pounds in electricity, roughly half the petrol figure. So even without the cheap overnight rate, an electric car charged at home is comfortably cheaper to fuel than petrol, just not by the spectacular margin the off-peak row shows. The lesson is that home charging beats petrol either way; the tariff decides whether the win is large or merely solid.</p>

    <h2>The public-only trap</h2>
    <p>The bottom EV row is the warning. A driver who cannot charge at home and relies on public rapid chargers for everything pays around 79p a unit, and at that rate a year of average driving costs more than running the petrol car. This is the one situation where an electric car can be dearer to fuel than petrol, and it is worth being honest about it. Public rapid charging is priced for speed and convenience and is a fair deal as an occasional top-up on a long trip, but as the everyday way to fuel a car it throws away the whole running-cost advantage. If you have no way to charge at or near home cheaply, the annual fuel sum is one of the things to weigh carefully before going electric.</p>

    <h2>Mileage changes the size, not the direction</h2>
    <p>The second column shows what happens at 12,000 miles a year, a high-mileage driver. Every figure rises, but the ranking holds: off-peak charging is still a few hundred pounds, the standard rate still well under petrol, and public-only still the dearest. In fact the more miles you drive, the bigger the absolute saving from charging cheaply at home, because the per-mile gap is multiplied over more miles. A high-mileage driver who can charge off-peak saves over 1,400 pounds a year against petrol. The headline is the same at any mileage: home off-peak charging wins handsomely, public-only loses, and how far you drive sets the size of the prize rather than who takes it.</p>

    <h2>Do the sum for yourself</h2>
    <p>Your own numbers are easy to work out and worth doing, because the averages may not match you. Take your real annual mileage, your car's own efficiency from its dashboard readout, and your actual unit rate, and run them through the same two steps: miles divided by miles per kWh gives your yearly kWh, times your rate gives your annual cost. The <a href="appliance-running-cost.html">running cost calculator</a> handles the same kind of sum, and the <a href="ev-charging-at-home-cost.html">cost of charging at home</a> guide has the per-charge and per-mile detail behind these annual totals. Whatever the exact figures, the shape is reliable: charge at home in the cheap hours and a year of motoring costs a fraction of the petrol equivalent.</p>

    <h2>The bottom line</h2>
    <p>Over a typical year an electric car charged on an off-peak home tariff costs around 170 pounds to fuel, against roughly 1,080 pounds of petrol, a saving near 900 pounds that returns every year. On a standard rate the EV still costs about half what petrol does. Only relying on public rapid chargers for everything flips the result, pushing the annual cost above petrol. Higher mileage widens the saving rather than narrowing it. The tariff is the decisive number, so charge at home, in the cheap window, and a year of driving costs a fraction of what the pump would take.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to charge an electric car for a year?","acceptedAnswer":{"@type":"Answer","text":"At a typical 7,500 miles a year and about 3.5 miles per kWh, an electric car uses roughly 2,140 kWh. On an 8p off-peak tariff that is about 170 pounds a year; on the 26p standard rate about 560 pounds; relying on 79p public rapid chargers about 1,690 pounds. Your mileage, efficiency and rate change the figure."}},{"@type":"Question","name":"Is an electric car cheaper to fuel than petrol over a year?","acceptedAnswer":{"@type":"Answer","text":"On a home tariff, yes, usually by a wide margin. Off-peak charging costs around 170 pounds a year against roughly 1,080 pounds of petrol for a 50 mpg car at average mileage, about six times cheaper. Even on a standard electricity rate the EV costs about half the petrol figure. Only charging exclusively on public rapid chargers can cost more than petrol."}},{"@type":"Question","name":"Does higher mileage make an EV more or less worth it than petrol?","acceptedAnswer":{"@type":"Answer","text":"More worth it, on fuel cost. The per-mile saving from charging cheaply at home is multiplied over more miles, so a high-mileage driver charging off-peak saves more in absolute terms. At 12,000 miles a year the off-peak EV saves over 1,400 pounds against petrol."}},{"@type":"Question","name":"When does an electric car cost more to run than petrol?","acceptedAnswer":{"@type":"Answer","text":"When you cannot charge at home and rely on public rapid chargers for everything. At around 79p a unit, a year of average driving on public rapid charging costs more than the petrol equivalent. Home charging, especially on an off-peak tariff, is always far cheaper than petrol."}}]}</script>
''',
)

PAGES["air-conditioning-running-cost"] = dict(
    title="How much does it cost to run air conditioning?",
    description="What air conditioning costs to run in the UK: the cost per hour and per day for a portable unit and a fixed split system, why a compressor is so much dearer than a fan, what the energy rating and the venting hose change, and how to keep the bill down on the hottest days.",
    active="guides",
    blurb="A compressor draws thirty to fifty times what a fan does. The cost per hour and per day, and how to keep it down.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">As hot spells get more common, more people are reaching for air conditioning, and it is one of the heaviest electrical loads a home can run. The good news is that the cost is easy to work out, because a cooling unit is just an appliance with a wattage like any other. The figure usually surprises people, in both directions: a portable unit run flat out through a heatwave adds a real sum to the bill, while a few sensible habits cut that sharply.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A portable air conditioner typically draws 1 to 1.5 kilowatts, so at the standard electricity rate of about 26p a unit it costs roughly 26p to 39p an hour, or around 2 to 3 pounds for an eight-hour day. A more efficient fixed split system averages less. A fan, by contrast, costs about a penny an hour. The compressor in an air conditioner is what makes the difference, drawing thirty to fifty times what a fan does.</p>
    </div>

    <h2>Why air conditioning costs so much more than a fan</h2>
    <p>The gulf comes down to what each device actually does. A fan does not cool the air at all; it moves it, and moving air cools your skin by helping sweat evaporate, which takes very little power. Air conditioning genuinely removes heat from the room and pumps it outside, using a compressor and refrigerant in the same way a fridge does, and shifting heat like that is energy-hungry. A fan draws tens of watts; an air conditioner draws a kilowatt or more. That is the whole story of the bill, and it is why the <a href="keeping-cool-without-air-con.html">keeping cool without air conditioning</a> guide treats real cooling as a last resort rather than a first move.</p>

    <h2>What it costs per hour and per day</h2>
    <p>The sum is the same one the <a href="appliance-running-cost.html">running cost calculator</a> does for any appliance: the power in kilowatts multiplied by the hours, multiplied by your price per unit. The table below uses the standard price-cap rate of about 26p per kWh, current in mid 2026, across the common types of cooling. Find your unit's wattage on its label or in its manual and read across.</p>

    <table class="ev-table">
      <thead><tr><th>Cooling device</th><th>Typical power</th><th>Cost per hour</th><th>Cost per 8-hour day</th></tr></thead>
      <tbody>
        <tr><td>Pedestal or tower fan</td><td>50 W</td><td>~1.3p</td><td>~10p</td></tr>
        <tr><td>Evaporative air cooler</td><td>60 to 100 W</td><td>~2p to 2.6p</td><td>~13p to 21p</td></tr>
        <tr><td>Fixed split system (inverter), average</td><td>600 to 800 W</td><td>~16p to 21p</td><td>~£1.25 to £1.67</td></tr>
        <tr><td>Portable air conditioner</td><td>1,000 to 1,500 W</td><td>~26p to 39p</td><td>~£2.09 to £3.13</td></tr>
      </tbody>
    </table>
    <p class="ev-note">At an example 26p per kWh (Ofgem price cap, July to September 2026, 26.11p). A split system cycles its compressor off once the room reaches temperature, so its average draw is below its peak; a cheap portable unit tends to run harder for longer. Run a 1.2 kW portable unit eight hours a day for a month and that is roughly 60 to 75 pounds on top of your usual bill.</p>

    <h2>Portable versus fixed: not the same machine</h2>
    <p>The two common types of home air conditioning behave very differently on cost. A portable unit on wheels is cheap to buy and needs no installation, but it is the least efficient option: it sits in the room it is cooling, dumps its heat through a hose out of a window, and a single-hose model draws warm air back into the room as it works, so it has to run harder. A fixed split system, with a quiet indoor unit and a compressor mounted outside, costs more to buy and must be installed, but it is far more efficient, cools more effectively, and its inverter compressor throttles back once the room is comfortable rather than running flat out. If you cool often, the running-cost saving of a fixed system can outweigh its higher purchase price over time, much as it does with any efficient appliance.</p>

    <h2>The venting hose matters more than people think</h2>
    <p>With a portable unit, the hose is the difference between cooling and just making noise. The hose carries the heat the unit has removed out of the window, and it must vent outside; if it does not, the unit is simply moving heat around the same room and adding its own motor heat on top, so the room never really cools and you pay for the privilege. The window gap around the hose needs sealing too, or hot outside air pours straight back in. Single-hose units have a built-in handicap, because the air they blow outside has to be replaced by air drawn in from elsewhere in the house, often warm. Twin-hose units avoid that and are noticeably more effective for the energy. Whatever the type, a unit venting properly through a sealed window does the job for far less running time than one fighting itself.</p>

    <h2>Read the energy rating before you buy</h2>
    <p>Air conditioners carry an <a href="energy-labels-explained.html">energy label</a> like other appliances, and for something that may run for hours on the hottest days it is worth reading. The figure to look at is the efficiency, often shown as a seasonal rating, which tells you how much cooling you get per unit of electricity. A more efficient unit delivers the same cool room for less power, and over several summers that gap repeats every time you switch it on. As with fridges and washing machines, the cheapest unit to buy is rarely the cheapest to run, and for a heavy seasonal load the running cost is the number that matters.</p>

    <h2>How to keep the cost down</h2>
    <p>The discipline that controls any heavy load applies here. Cool only the room you are in, not the whole house, and shut its door and windows so you are not cooling the outdoors. Do all the free things first: close curtains and blinds against the sun by day, open up at night to flush the heat out, and switch off indoor heat sources, all covered in the <a href="keeping-cool-without-air-con.html">keeping cool</a> guide, so the air conditioner has less work to do and runs for less time. Set the target temperature modestly, in the mid twenties rather than as cold as it will go, because every degree cooler costs more. Use the timer so it is not running in an empty room, and switch it off when you leave. Done this way, occasional targeted cooling on the worst days costs a fraction of running a unit flat out all summer.</p>

    <h2>The bottom line</h2>
    <p>Air conditioning costs real money because it removes heat rather than just moving air, drawing a kilowatt or more against a fan's few tens of watts. A portable unit runs to roughly 26p to 39p an hour at the standard rate, a fixed split system rather less, and a fan about a penny. Read the wattage off your unit, run it through the calculator, and you will know your own figure. Then keep it down the same way you would any big load: cool one room, do the free measures first, set a sensible temperature, and reserve the compressor for the days when shading and a fan are genuinely not enough.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to run air conditioning?","acceptedAnswer":{"@type":"Answer","text":"A portable air conditioner typically draws 1 to 1.5 kW, costing about 26p to 39p an hour at the 26p standard electricity rate, or roughly 2 to 3 pounds for an eight-hour day. A more efficient fixed split system averages less, around 16p to 21p an hour. Run a portable unit eight hours a day for a month and it adds roughly 60 to 75 pounds to the bill."}},{"@type":"Question","name":"Is a portable air conditioner cheaper to run than a fixed one?","acceptedAnswer":{"@type":"Answer","text":"No. A portable unit is cheaper to buy but less efficient to run, because it sits in the room, vents through a hose, and on single-hose models draws warm air back in. A fixed split system costs more upfront but its inverter compressor throttles back once the room is cool, so it uses less electricity for the same comfort."}},{"@type":"Question","name":"Why is air conditioning so much more expensive than a fan?","acceptedAnswer":{"@type":"Answer","text":"A fan only moves air, which cools your skin and takes very little power, tens of watts. Air conditioning actually removes heat from the room using a compressor and pumps it outside, which draws a kilowatt or more, thirty to fifty times as much. That is why a fan costs about a penny an hour and an air conditioner costs pounds a day."}},{"@type":"Question","name":"Does a portable air conditioner need to be vented out of a window?","acceptedAnswer":{"@type":"Answer","text":"Yes. The hose carries the removed heat outside, so it must vent through a window with the gap sealed. Without venting, the unit just moves heat around the same room and adds its own motor heat, so the room never properly cools and you pay for nothing. Twin-hose units are more effective than single-hose ones."}}]}</script>
''',
)

PAGES["fan-running-cost"] = dict(
    title="How much does it cost to run a fan?",
    description="The reassuring answer to a common summer question: a fan costs only pennies an hour to run. The cost by fan type, what a whole night or a whole summer adds up to, and why a fan is so cheap compared with air conditioning.",
    active="guides",
    blurb="Almost nothing. A fan costs about a penny an hour, so a whole night runs to a few pence. The figures by fan type.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">When a heatwave hits and the fan goes on, a quiet worry follows it: is this thing running up the bill while I sleep? The reassuring answer is no. A fan is one of the cheapest appliances in the house to run, costing roughly a penny an hour, so even left on all night it adds only a few pence. This guide gives the real figures by fan type, so you can stop worrying and leave it on.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Most fans draw between about 5 and 100 watts, so at the standard electricity rate of about 26p a unit they cost from a fraction of a penny up to around 2.6p an hour. A typical pedestal or tower fan at 50 watts costs about 1.3p an hour, so running it for a twelve-hour night costs roughly 16p. Over a whole hot month of nightly use that is only a few pounds. A fan is about the cheapest cooling there is.</p>
    </div>

    <h2>Why a fan is so cheap to run</h2>
    <p>A fan does not cool the air, it moves it, and moving air is a light job for an electric motor. That breeze cools you by helping sweat evaporate from your skin, which is why a fan feels cooling even though the room temperature has not changed. Because all the motor is doing is spinning a blade, the power draw is tiny, measured in tens of watts rather than the kilowatts an <a href="air-conditioning-running-cost.html">air conditioner</a> pulls to actually remove heat from the room. That difference, a fan moving air versus a compressor shifting heat, is the whole reason one costs pennies and the other costs pounds.</p>

    <h2>What different fans cost</h2>
    <p>Fans vary in size from a tiny clip-on to a big floor blower, and the power draw varies with them, but every one of them is cheap. The table uses the standard price-cap rate of about 26p per kWh, current in mid 2026. To find your own fan's figure, look for the wattage printed on the motor housing or in the manual, or put it through the <a href="appliance-running-cost.html">running cost calculator</a>.</p>

    <table class="ev-table">
      <thead><tr><th>Fan type</th><th>Typical power</th><th>Cost per hour</th><th>Cost for a 12-hour night</th></tr></thead>
      <tbody>
        <tr><td>Small USB or clip-on fan</td><td>5 to 15 W</td><td>~0.1p to 0.4p</td><td>~2p to 5p</td></tr>
        <tr><td>Ceiling fan</td><td>15 to 30 W</td><td>~0.4p to 0.8p</td><td>~5p to 9p</td></tr>
        <tr><td>Pedestal or tower fan</td><td>40 to 60 W</td><td>~1.0p to 1.6p</td><td>~13p to 19p</td></tr>
        <tr><td>Large floor or industrial fan</td><td>100 W</td><td>~2.6p</td><td>~31p</td></tr>
      </tbody>
    </table>
    <p class="ev-note">At an example 26p per kWh. Even the thirstiest household fan running all night costs about the price of a chocolate bar, and the small ones cost almost nothing. Lower fan speeds draw less power still.</p>

    <h2>A whole night, a whole summer</h2>
    <p>Put it in terms of real use. Leaving a 50-watt pedestal fan running every night through a hot month, say twelve hours a night for thirty nights, uses about 18 kilowatt-hours, which at 26p comes to under 5 pounds for the month. A small bedside fan costs a fraction of that. Even if you ran fans in two rooms all summer, the total would be a handful of pounds, not the scary number people imagine. Set against the cost of cooling those rooms with air conditioning, which could run to that much in a couple of days, the fan is almost free.</p>

    <h2>Getting the most from a cheap breeze</h2>
    <p>Because a fan only cools the person feeling it, the one rule is to run it where someone is, not in an empty room, where it does nothing but spend its pennies for no benefit. Beyond that, a fan earns its keep helping move air through the house: placed in an open window in the evening it draws cool outside air in, or pushes warm air out, flushing the day's heat as the <a href="keeping-cool-without-air-con.html">keeping cool</a> guide describes. A bowl of ice in front of the fan adds a brief extra chill on the very hottest days. And a ceiling fan, being permanently sited and efficient, is a cheap way to keep a room comfortable for the lowest running cost of all.</p>

    <h2>When a fan is not enough</h2>
    <p>A fan has one limit: it cannot lower the air temperature, only make moving air feel cooler on the skin. On the rare days when the air itself is simply too hot, a fan blowing hot air around brings little relief, and that is the point at which real cooling earns its much higher cost. But those days are few, and the honest order is to exhaust the free measures and the cheap fan first, reserving the expensive compressor for when nothing else will do. For the great majority of warm evenings, a fan at a penny an hour is all the cooling the bill needs to carry.</p>

    <h2>The bottom line</h2>
    <p>A fan costs roughly a penny an hour to run, so a whole night is a few pence and a whole summer a few pounds, because all it does is move air rather than chill it. Leave it on while you are in the room without a second thought, use it to flush cool night air through the house, and keep the costly air conditioning for the handful of days a fan genuinely cannot cope with. Of all the ways to feel cooler, the fan is the one your bill will never notice.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much does it cost to run a fan?","acceptedAnswer":{"@type":"Answer","text":"Very little. Most fans draw 5 to 100 watts, so at the 26p standard electricity rate they cost from a fraction of a penny up to about 2.6p an hour. A typical 50-watt pedestal fan costs about 1.3p an hour, so a twelve-hour night is roughly 16p and a whole month of nightly use under 5 pounds."}},{"@type":"Question","name":"Is it expensive to leave a fan on all night?","acceptedAnswer":{"@type":"Answer","text":"No. A typical pedestal fan running for a twelve-hour night costs around 16p, and a small bedside fan far less. You can leave a fan on overnight while you are in the room without worrying about the bill. Just avoid running it in an empty room, where it cools no one."}},{"@type":"Question","name":"Which fan is cheapest to run?","acceptedAnswer":{"@type":"Answer","text":"Small USB and clip-on fans use the least power, just a few watts, costing almost nothing. Ceiling fans are also very efficient at 15 to 30 watts. Larger pedestal and floor fans use more but are still cheap, at roughly 1p to 2.6p an hour. Lower speeds draw less power than full blast."}},{"@type":"Question","name":"Is a fan cheaper than air conditioning?","acceptedAnswer":{"@type":"Answer","text":"Far cheaper. A fan costs about a penny an hour because it only moves air, while air conditioning draws a kilowatt or more to actually remove heat, costing pounds a day. A fan can be thirty to fifty times cheaper to run, which is why it should be the first choice and air conditioning the last resort."}}]}</script>
''',
)

PAGES["portable-air-conditioner-vs-fan"] = dict(
    title="Portable air conditioner vs fan: which is worth it?",
    description="A straight comparison of a portable air conditioner and a fan: what each actually does, the large gap in running cost, where an evaporative cooler sits between them, and how to decide which you need for a British summer.",
    active="guides",
    blurb="One moves air for pennies; one removes heat for pounds. What each is really for, and how to choose.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">When the house gets uncomfortably hot, the choice usually comes down to a fan or a portable air conditioner. They look like two answers to the same problem, but they are really different machines doing different jobs at wildly different running costs. Knowing which one you actually need, and on which days, saves both money and disappointment.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A fan moves air, which cools your skin for about a penny an hour. A portable air conditioner removes heat from the room and pumps it outside, which genuinely lowers the temperature but draws a kilowatt or more, costing roughly 26p to 39p an hour, thirty to fifty times as much. For most warm British days a fan is enough; a portable air conditioner earns its higher cost only on the small number of days when the air itself is simply too hot.</p>
    </div>

    <h2>They do different jobs</h2>
    <p>The key thing to understand is that a fan does not cool the air at all. It moves it, and that moving air cools you by speeding up the evaporation of sweat from your skin, so you feel cooler while the room stays the same temperature. A portable air conditioner does something fundamentally harder: it uses a compressor and refrigerant to pull heat out of the room's air and pump it outside through a hose, actually dropping the temperature. One makes you feel cooler; the other makes the room cooler. That distinction explains both the comfort difference and the cost difference between them.</p>

    <h2>The running-cost gap</h2>
    <p>Because the two do such different work, they sit at opposite ends of the cost scale. The table uses the standard price-cap rate of about 26p per kWh, current in mid 2026, and the gap is stark.</p>

    <table class="ev-table">
      <thead><tr><th>Device</th><th>Typical power</th><th>Cost per hour</th><th>Cost per 8-hour day</th></tr></thead>
      <tbody>
        <tr><td>Pedestal or tower fan</td><td>50 W</td><td>~1.3p</td><td>~10p</td></tr>
        <tr><td>Evaporative air cooler</td><td>60 to 100 W</td><td>~2p to 2.6p</td><td>~13p to 21p</td></tr>
        <tr><td>Portable air conditioner</td><td>1,000 to 1,500 W</td><td>~26p to 39p</td><td>~£2.09 to £3.13</td></tr>
      </tbody>
    </table>
    <p class="ev-note">At an example 26p per kWh. A portable air conditioner can cost in a single day what a fan costs in a month of nightly use. Full figures and how to cut them are in the <a href="air-conditioning-running-cost.html">air conditioning running cost</a> guide.</p>

    <h2>Where an evaporative cooler sits</h2>
    <p>Between the fan and the air conditioner sits a third option worth knowing about: the evaporative cooler, sometimes sold as an air cooler. It blows air over a wet pad, and as the water evaporates it takes a little heat with it, so the air coming out is slightly cooler than the air going in, unlike a plain fan. It uses only a little more power than a fan, so it is cheap to run. The catch is that it adds moisture to the room and works best in dry heat; in the muggy, humid warmth of a typical British hot spell its effect is modest, because the air is already damp and evaporation slows. It is a cheap half-step up from a fan, not a substitute for real air conditioning.</p>

    <h2>The portable air conditioner's catches</h2>
    <p>A portable unit does genuinely cool a room, but it comes with strings beyond the running cost. It must vent its heat outside through a hose in a window, and the window gap has to be sealed, or hot air pours back in and it never wins. Cheaper single-hose models have a built-in inefficiency, drawing replacement air in from the rest of the house as they blow air out, so part of their effort is wasted. They are also bulky, noisy, and only really cool the one room they stand in. None of this makes them useless, but it does mean a portable air conditioner is a considered purchase for genuine need, not a casual grab, and the <a href="air-conditioning-running-cost.html">running cost guide</a> covers getting the most from one.</p>

    <h2>How to decide</h2>
    <p>Work from the bottom up. For the large majority of warm days, the free measures plus a fan are enough: shade the windows against the sun, flush cool air through at night, and let a cheap breeze do the rest, all set out in the <a href="keeping-cool-without-air-con.html">keeping cool without air conditioning</a> guide. Reach for the fan first because it costs almost nothing. Consider an evaporative cooler if you want a touch more for not much more power, accepting it does little in humid heat. Buy a portable air conditioner only if you genuinely face a run of days when the air itself is too hot to sleep or work in, you cannot get relief any other way, and you accept the running cost and the venting faff. For most British summers that is a handful of days a year, which is worth weighing against the price of a machine that sits in a cupboard the rest of the time.</p>

    <h2>The bottom line</h2>
    <p>A fan and a portable air conditioner are not two versions of the same thing. The fan moves air to cool your skin for about a penny an hour and handles most warm days; the air conditioner removes heat to cool the room for pounds a day and is for the rare days nothing else can manage. An evaporative cooler is a cheap middle option that struggles in humid heat. Start with shading and a fan, step up only when you must, and you keep a British summer comfortable without letting the cooling become the thing that runs up the bill.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is a fan or a portable air conditioner better?","acceptedAnswer":{"@type":"Answer","text":"It depends on the day. A fan moves air to cool your skin for about a penny an hour and is enough for most warm days. A portable air conditioner actually lowers the room temperature but costs roughly 26p to 39p an hour, thirty to fifty times more, so it is worth it only on the few days the air itself is too hot for a fan to help."}},{"@type":"Question","name":"How much more does a portable air conditioner cost to run than a fan?","acceptedAnswer":{"@type":"Answer","text":"About thirty to fifty times as much. A fan drawing 50 watts costs around 1.3p an hour, while a portable air conditioner drawing 1 to 1.5 kW costs about 26p to 39p an hour at the 26p standard rate. A portable unit can cost in one day what a fan costs in a month."}},{"@type":"Question","name":"Does an evaporative air cooler work as well as air conditioning?","acceptedAnswer":{"@type":"Answer","text":"No. An evaporative cooler blows air over a wet pad, cooling it slightly, and uses only a little more power than a fan. But it adds moisture and works best in dry heat, so in the humid warmth of a typical British hot spell its effect is modest. It is a cheap step up from a fan, not a replacement for real air conditioning."}},{"@type":"Question","name":"Do I really need air conditioning in the UK?","acceptedAnswer":{"@type":"Answer","text":"For most people, no. Shading the windows, flushing cool air through at night and using a fan handle the great majority of warm days for pennies. A portable air conditioner is worth buying only if you face a run of genuinely too-hot days you cannot manage any other way, and you accept its much higher running cost and the need to vent it out of a window."}}]}</script>
''',
)

PAGES["heat-pump-running-cost-vs-gas-boiler"] = dict(
    title="Heat pump running cost vs a gas boiler",
    description="The real running-cost comparison between a heat pump and a gas boiler: how efficiency and the gap between electricity and gas prices decide it, the cost per unit of heat worked out, why the tariff matters so much, and where each comes out ahead.",
    active="guides",
    blurb="It hinges on efficiency and the gap between electricity and gas prices. The cost per unit of heat, worked out honestly.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Whether a heat pump is cheaper to run than a gas boiler is one of the most asked and most muddled questions in home energy, and the honest answer is that it depends on two numbers: how efficiently the heat pump runs, and the gap between what you pay for electricity and what you pay for gas. Get both in your favour and a heat pump is clearly cheaper; get them against you and it can cost about the same or more. This guide works out the real figures rather than the slogans.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A gas boiler is roughly 90 per cent efficient, so a unit of gas at the current price-cap rate of 7.33p gives heat at around 8.1p per kWh. A heat pump delivers about three to four units of heat per unit of electricity, so at the 26.11p standard electricity rate it gives heat at roughly 6.5p to 8.7p per kWh, depending on its efficiency. That means a good heat pump now edges ahead of gas even on a standard tariff, while a poorly performing one roughly matches it. On a dedicated heat-pump electricity tariff the heat pump wins comfortably. The deciding factor is the price gap between electricity and gas, not the technology.</p>
    </div>

    <h2>The two numbers that decide it</h2>
    <p>A gas boiler and a heat pump make heat in completely different ways, and comparing them fairly means reducing both to the same thing: the cost of a unit of useful heat delivered into your home. For a gas boiler that depends on the price of gas and the boiler's efficiency, which for a modern condensing boiler running well is around 90 per cent, so a little of the gas you pay for is lost. For a heat pump it depends on the price of electricity and the pump's efficiency, measured as its coefficient of performance or, over a year, its seasonal figure. Crucially a heat pump does not burn its electricity for heat; it uses it to move heat from outside into the house, so it delivers several units of heat for each unit of electricity, as the <a href="heat-pumps-explained.html">heat pumps explained</a> guide describes. A good system returns three to four units of heat per unit of power.</p>

    <h2>Cost per unit of heat, worked out</h2>
    <p>Put real prices in and the comparison comes alive. The figures below use the current Ofgem price-cap unit rates for 1 July to 30 September 2026, gas at 7.33p per kWh and electricity at 26.11p (direct debit, the England, Scotland and Wales average), plus a separate lower rate for a dedicated heat-pump tariff. The heat pump rows show different efficiencies, because a well-designed system in a well-insulated home achieves a higher figure than a poorly set one.</p>

    <table class="ev-table">
      <thead><tr><th>Heating</th><th>Assumption</th><th>Cost per kWh of heat</th></tr></thead>
      <tbody>
        <tr><td>Gas boiler</td><td>7.33p gas, 90% efficient</td><td>~8.1p</td></tr>
        <tr><td>Heat pump, standard rate</td><td>26.11p electricity, efficiency 3.0</td><td>~8.7p</td></tr>
        <tr><td>Heat pump, standard rate</td><td>26.11p electricity, efficiency 3.5</td><td>~7.5p</td></tr>
        <tr><td>Heat pump, standard rate</td><td>26.11p electricity, efficiency 4.0</td><td>~6.5p</td></tr>
        <tr><td>Heat pump, heat-pump tariff</td><td>15p electricity, efficiency 3.5</td><td>~4.3p</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Gas 7.33p and electricity 26.11p are the Ofgem price-cap unit rates for 1 July to 30 September 2026 (direct debit); both vary by region and tariff, so check your own bill. The heat-pump tariff row uses an example 15p rate typical of dedicated heat-pump deals. Standing charges are separate, and going all-electric removes the daily gas standing charge, about 29p a day under the same cap.</p>

    <h2>Why it is close, and which way it now leans</h2>
    <p>The table shows the heart of the matter. On a standard tariff, a heat pump running at a typical real-world efficiency of around 3.5 delivers heat at about 7.5p per kWh, a little under the gas boiler's 8.1p, so a well-performing pump now edges ahead of gas even before any special tariff. The reason it stays close at all is that electricity in Britain costs about three and a half times as much as gas per unit, while a good heat pump is roughly three to four times as efficient as a boiler at turning what you pay for into heat. Those two ratios nearly cancel, which is why the standard-tariff rows sit close to the gas figure rather than far below it. It also means the result is sensitive: a pump achieving a high efficiency comes out clearly cheaper, while one running poorly, in a draughty house or set up to run hot, can slip back to roughly level with or above gas. The fabric of the home and the quality of the installation matter as much as the box on the wall.</p>

    <h2>Why the tariff changes everything</h2>
    <p>The bottom row is where the heat pump pulls clear. Because it runs on electricity, a heat pump can use a dedicated heat-pump or time-of-use tariff, where the unit rate is well below the standard cap. Drop the electricity price and the heat pump's cost per unit of heat drops with it, comfortably below gas, while the gas boiler has no such lever. This is the same lesson the <a href="ev-charging-at-home-cost.html">EV charging</a> guides keep returning to: once a thing runs on electricity, the tariff you put it on becomes the biggest cost decision you make. A heat pump on the right electricity tariff is clearly cheaper to run than a gas boiler; the same heat pump on a flat standard rate is cheaper only by a little at best, and roughly level if it runs poorly.</p>

    <h2>What it means for a year's heating</h2>
    <p>A typical home needs very roughly 11,000 to 12,000 kWh of heat a year. At the per-unit figures above, that is around 900 to 980 pounds of gas through a boiler, a little less for a heat pump on a standard rate at a good efficiency, and roughly 500 pounds for a heat pump on a good heat-pump tariff, plus or minus a great deal depending on your home, your habits and your rates. Set against the boiler you also save its servicing and lose the gas standing charge, about 29p a day or some 105 pounds a year, if you go fully electric. These are illustrative, not a quote: your own annual heat demand and unit rates move the answer a lot, so treat the per-unit cost as the reliable comparison and scale it to your own usage.</p>

    <h2>Getting a heat pump into the cheaper column</h2>
    <p>Since the result is decided at the margin, the things that tip it are worth doing. Insulate and draught-proof first, because a warmer, tighter home lets the heat pump run at a lower flow temperature, which is exactly where it is most efficient, so the <a href="loft-insulation.html">insulation</a> and <a href="draught-proofing.html">draught-proofing</a> basics pay double. Size and set the system properly, running it steady and gentle rather than in hot blasts, the opposite of how many people run a boiler, as the <a href="boiler-flow-temperature.html">flow temperature</a> guide explains for boilers and which matters even more for a pump. And get onto a heat-pump electricity tariff. Do all three and a heat pump moves from break-even to clearly cheaper; skip them and it struggles to beat the boiler it replaced.</p>

    <h2>The bottom line</h2>
    <p>A heat pump is not automatically cheaper to run than a gas boiler, and anyone who tells you it always is, or never is, is skipping the arithmetic. On a standard tariff the two are close, because electricity costs about three and a half times what gas does while a good heat pump is three to four times as efficient, so the ratios nearly cancel and a well-set pump edges ahead. The heat pump wins clearly when it runs efficiently in a well-insulated home on a dedicated electricity tariff, and only slips behind when those are missing. Do the fabric, set it up to run gently, and put it on the right tariff, and the running cost lands firmly in its favour.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is a heat pump cheaper to run than a gas boiler?","acceptedAnswer":{"@type":"Answer","text":"It depends on the heat pump's efficiency and the gap between electricity and gas prices. On a standard tariff the two are close, with a good heat pump edging ahead, because electricity costs about three and a half times as much as gas while a good heat pump is three to four times as efficient. On a dedicated heat-pump electricity tariff the heat pump is comfortably cheaper."}},{"@type":"Question","name":"What is the cost per unit of heat for a heat pump versus gas?","acceptedAnswer":{"@type":"Answer","text":"A gas boiler at 90 per cent efficiency on the 7.33p price-cap gas rate gives heat at about 8.1p per kWh. A heat pump on the 26.11p standard electricity rate gives heat at about 6.5p to 8.7p per kWh depending on its efficiency, so level with or a little below gas. On a 15p heat-pump tariff at an efficiency of 3.5 it falls to about 4.3p per kWh, well below gas."}},{"@type":"Question","name":"Why is a heat pump not always cheaper than gas?","acceptedAnswer":{"@type":"Answer","text":"Because electricity in Britain costs about three and a half times as much as gas per unit, while a good heat pump is only about three to four times as efficient as a boiler. Those ratios nearly cancel on a standard tariff, so the result is close, with a good pump a little cheaper and a poorly performing one roughly level with gas. It depends on the pump running efficiently in a well-insulated home and ideally on a cheaper electricity tariff."}},{"@type":"Question","name":"How do I make a heat pump cheaper to run?","acceptedAnswer":{"@type":"Answer","text":"Insulate and draught-proof so the pump can run at a low flow temperature where it is most efficient, set it to run steady and gentle rather than in hot blasts, and get onto a dedicated heat-pump electricity tariff with a lower unit rate. Together these move a heat pump from breaking even with gas to clearly cheaper."}}]}</script>
''',
)

PAGES["ev-range-in-hot-weather"] = dict(
    title="Does hot weather affect EV range? What a heatwave does",
    description="Heat cuts an electric car's range too, not just cold: why a heatwave costs you miles through the air conditioning and the battery's own cooling, how much to expect, why a heat pump does not save you in summer, the effect on rapid charging and battery life, and how to limit it.",
    active="guides",
    blurb="Heat cuts range too, just less than cold. Why a heatwave costs you miles, and why a heat pump won't save you this time.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">Everyone knows winter shortens an electric car's range, and that a heat pump softens the blow. Far fewer people realise that a heatwave costs range too. The loss is smaller than a hard frost, but on a scorching day a car can drop a fifth of its range, and this time the heat pump that rescues you in January is no help at all. Here is why heat costs miles, how much, and what to do about it.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Yes, hot weather cuts EV range, typically by around 10 to 25 per cent in a heatwave compared with a mild day, mostly from running the air conditioning and from the battery's own cooling system. The hit is smaller than deep winter's, because the battery itself works happily when warm. Unlike winter, a heat pump does not save you, since in the heat every electric car leans on the same air-conditioning compressor. Pre-cool the cabin while plugged in, park in the shade, and avoid sitting at 100 per cent in extreme heat.</p>
    </div>

    <h2>Heat cuts range, but less than cold</h2>
    <p>An electric car is happiest in mild weather, somewhere around 20 degrees, where neither heating nor cooling is doing much work. Push the temperature up into the thirties and the range falls, just as it does in the cold, but by less. The reason is that the battery itself is content when warm; it gives up and takes on energy readily, which is the opposite of its sluggishness in the cold. So the heatwave penalty comes almost entirely from the extra loads the hot weather creates, not from the battery struggling, which is why it is a milder effect than the double hit of a cold battery plus cabin heating you get in winter, set out in the <a href="ev-charging-in-winter.html">EV charging in winter</a> guide.</p>

    <h2>Why a hot day costs you miles</h2>
    <p>Two things drain the battery in a heatwave. The first is the air conditioning, which on a very hot day runs hard to keep the cabin bearable, and that cooling energy comes from the battery that would otherwise be driving you forward. The second is the battery's own thermal management: modern electric cars actively cool the pack in extreme heat to protect the cells, and running that cooling draws power too. Together these are what trim your range. There is a silver lining, though, that petrol drivers do not get: an electric motor produces far less waste heat than an engine, so on a hot day the cabin starts off less brutally hot and the air conditioning has a slightly easier job than it does in a petrol car sitting behind a roasting engine bay.</p>

    <h2>How much range you lose</h2>
    <p>As with winter, the figure is a range rather than a single number, depending on how hot it is and how hard the air conditioning works. A warm day costs little; a full heatwave with the cooling running flat out can take a fifth or more off your usable range. The table sets the heat penalty against the familiar winter one for scale.</p>

    <table class="ev-table">
      <thead><tr><th>Conditions</th><th>Typical range vs a mild day</th></tr></thead>
      <tbody>
        <tr><td>Mild day, around 20C</td><td>baseline, the best you will see</td></tr>
        <tr><td>Hot day, around 30C, air con on</td><td>~10 to 15% less</td></tr>
        <tr><td>Heatwave, 35C and above, cooling hard</td><td>~15 to 25% less</td></tr>
        <tr><td>Hard winter frost, for comparison</td><td>~25 to 30% or more less</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Indicative figures; the exact loss varies by car and conditions. The pattern holds across studies: heat cuts range, but a hard frost cuts it more. The loss shows up as a lower <a href="electric-car-miles-per-kwh.html">miles per kWh</a> figure, so the same charge takes you less far.</p>

    <h2>Why a heat pump will not save you in summer</h2>
    <p>This is the part that surprises people. In winter, a heat-pump-equipped car claws back a big chunk of the range a cold day would otherwise cost, because the heat pump warms the cabin far more efficiently than a plain electric heater. A heatwave is a different problem. Cooling the cabin is done by the air-conditioning compressor, and every electric car has one of those whether or not it has a heat pump, so in the heat they are all on much the same footing. The heat pump is a winter saviour, not a summer one. In fact some cars with heat pumps show slightly larger range loss in extreme heat than those without, because makers tune the system around the bigger prize of cold-weather efficiency. If you bought a heat-pump car expecting it to rescue your range in August too, this is the reality: in the heat, you are leaning on the air conditioning like everyone else.</p>

    <h2>Rapid charging can slow in the heat too</h2>
    <p>Heat does not only cost range, it can slow charging. Just as a cold battery limits how fast it will charge, a battery that is already hot, from a long fast motorway run in a heatwave, may have its rapid-charging rate held back while the car cools the pack to a safe temperature. So a mid-journey rapid charge on a blazing day can take longer than you expect. Home charging is barely affected, because the slow overnight rate sits well within what the battery can handle at any sensible temperature.</p>

    <h2>The bigger issue: heat ages the battery</h2>
    <p>The temporary range dip is the least of it. Sustained high temperature is one of the things that ages a lithium battery fastest, more so than cold, so the heat question is as much about long-term battery health as about today's range. The practical steps are simple. Park in the shade or a garage whenever you can, so the pack is not baking in the sun all day. Avoid leaving the car sitting at a full 100 per cent charge in extreme heat, since a full battery held hot is the hardest case of all; for everyday use a charge limit of around 80 per cent is kinder. And use slow home charging rather than repeated rapid charging in hot spells, which is gentler on a warm pack.</p>

    <h2>How to limit the range loss</h2>
    <p>The single most useful habit is the summer twin of winter preconditioning: pre-cool the cabin while the car is still plugged in. Cooling the car down from the mains before you set off, rather than from the battery once you are moving, means you start your journey in a comfortable car with a battery at a sensible temperature, having spent no range on the initial blast of cooling. Most electric cars let you schedule this to finish around your departure time, the same feature covered for warming in the <a href="best-time-to-charge-an-electric-car.html">best time to charge</a> guide. Beyond that, park in the shade and use a windscreen sunshade so the cabin is not an oven to begin with, lean on ventilated or cooled seats where the car has them rather than chilling the whole cabin, and once the car is cool let the air conditioning tick over gently rather than running at maximum. Each of these trims the cooling load, and with it the miles the heatwave takes.</p>

    <h2>The bottom line</h2>
    <p>Hot weather cuts an electric car's range by roughly 10 to 25 per cent in a heatwave, mostly through the air conditioning and the battery's cooling, which is real but less than a hard winter's loss because the battery itself likes the warmth. The catch is that a heat pump, the hero of winter range, does nothing for you in summer, when every car relies on the same air conditioning. Pre-cool while plugged in, park in the shade, keep the charge off 100 per cent in extreme heat, and the heatwave becomes a manageable dip rather than a worry, for both your range today and your battery's life over the years.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Does hot weather reduce electric car range?","acceptedAnswer":{"@type":"Answer","text":"Yes. A heatwave typically cuts EV range by around 10 to 25 per cent compared with a mild day, mostly from running the air conditioning and the battery's own cooling system. The loss is smaller than a hard winter's, because the battery itself works happily when warm, so the heat penalty comes from the extra cooling loads rather than the battery struggling."}},{"@type":"Question","name":"Does a heat pump help EV range in hot weather?","acceptedAnswer":{"@type":"Answer","text":"No, not really. A heat pump is a winter feature: it warms the cabin efficiently and claws back range in the cold. In a heatwave the cabin is cooled by the air-conditioning compressor, which every electric car has, so heat-pump and non-heat-pump cars are on much the same footing. Some heat-pump cars even lose slightly more range in extreme heat."}},{"@type":"Question","name":"Is hot weather bad for an EV battery?","acceptedAnswer":{"@type":"Answer","text":"Sustained high heat ages a lithium battery faster than cold does, so it is worth managing. Park in the shade or a garage, avoid leaving the car at a full 100 per cent charge in extreme heat, use a charge limit around 80 per cent for everyday use, and favour slow home charging over repeated rapid charging in hot spells."}},{"@type":"Question","name":"How can I reduce EV range loss in summer?","acceptedAnswer":{"@type":"Answer","text":"Pre-cool the cabin while the car is still plugged in, so the cooling comes from the mains rather than the battery. Park in the shade and use a windscreen sunshade so the car is not an oven, use ventilated or cooled seats instead of chilling the whole cabin, and let the air conditioning run gently once the car is cool rather than at maximum."}}]}</script>
''',
)

PAGES["keeping-your-car-cool-fuel-economy"] = dict(
    title="Keeping your car cool without wrecking fuel economy",
    description="Air conditioning or windows down: which keeps a car cool for less fuel, why the answer depends on your speed, what the air con actually costs at the pump, and the free habits that cut the heat before you spend a drop of fuel on it.",
    active="guides",
    blurb="Air con or windows down? The honest answer depends on your speed. How to stay cool for the least fuel.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">The old summer argument, air conditioning or windows down, turns out to have a real answer, and it is not the same answer at every speed. Air conditioning costs fuel; open windows cost aerodynamics; and which one is cheaper depends on how fast you are going. Knowing the crossover, and the free tricks that cut the heat before either comes into play, keeps you cool for the least fuel.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Air conditioning typically costs around 4 to 8 per cent in fuel, more in stop-start traffic. Open windows cost nothing directly but add aerodynamic drag that grows sharply with speed. The rule of thumb: below about 40 to 50 mph, windows down is the cheaper way to stay cool; at motorway speed, air conditioning wins because drag dominates. Either way, dump the trapped heat before you set off and park in the shade, so you need less cooling in the first place.</p>
    </div>

    <h2>What the air conditioning costs</h2>
    <p>Air conditioning is not free, because the compressor that cools the air is driven by the engine, so it burns a little extra fuel whenever it runs. The penalty is modest on the open road and larger in slow traffic, where the engine is working less but the compressor still has to run. On a hot day it can shave a noticeable slice off your economy, a few per cent on most cars and a touch more on a hybrid, whose efficient engine feels the extra load proportionally more. The same idea governs cooling anywhere, which is why an <a href="air-conditioning-running-cost.html">air conditioner at home</a> is such a heavy load too: removing heat takes real energy, in a car as in a house.</p>

    <table class="ev-table">
      <thead><tr><th>Vehicle</th><th>Typical fuel economy hit from air con</th></tr></thead>
      <tbody>
        <tr><td>Petrol</td><td>~4% (around 1 to 4 mpg on a hot day)</td></tr>
        <tr><td>Diesel</td><td>~5%</td></tr>
        <tr><td>Hybrid</td><td>~6%</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Indicative averages; the real figure depends on the car, the heat and how hard the system works. The penalty is largest in slow, stop-start traffic and smallest at a steady cruise.</p>

    <h2>What open windows cost</h2>
    <p>Opening the windows feels like the free option, and at low speed it very nearly is. But moving air past an open window creates drag, and aerodynamic drag rises steeply with speed, so the faster you go the more those open windows cost you in fuel. Around town the effect is tiny. On the motorway it can rival or even exceed the cost of the air conditioning, because the car is fighting noticeably more wind resistance. The evidence varies between vehicles, with a boxy car losing more than a sleek one, and some careful tests finding little difference at all on certain cars, but the direction is consistent: the penalty for open windows grows with speed, while the penalty for air conditioning stays much the same.</p>

    <h2>The rule of thumb, by speed</h2>
    <p>Put the two together and a simple guide emerges. At low speeds, around town and up to roughly 40 to 50 mph, open windows are the cheaper way to stay cool, because the drag they add is small and you avoid the air-conditioning fuel penalty entirely. At higher speeds, on faster A-roads and the motorway, air conditioning wins, because aerodynamic drag now dominates and keeping the windows shut to stay slippery is worth more than the fuel the compressor uses. So the fuel-savvy approach is windows down in town, windows up and air conditioning on for the motorway. Larger, boxier vehicles cross over at a lower speed than small aerodynamic ones, but the principle is the same for all of them.</p>

    <h2>Cut the heat before you cool it</h2>
    <p>The cheapest cooling is the heat you never let build up. A car left in the sun becomes far hotter inside than the air outside, so the first job is to dump that trapped heat before you drive: open the doors or windows for a minute to let the oven-hot air out, and you start from a far lower temperature that needs much less cooling to manage. Park in the shade whenever you can, use a reflective windscreen sunshade to stop the dashboard and cabin baking, and leave the windows cracked a little when parked so heat does not build to the same extreme. Do these and whichever cooling method you then use, windows or air conditioning, has far less work to do, which is where the real fuel saving lives.</p>

    <h2>Use the cooling well</h2>
    <p>However you cool the car, a little restraint helps. Set a comfortable temperature rather than the coldest setting, because as with a home thermostat the harder you ask the system to work the more it costs. Once the cabin is cool, switching to recirculate keeps the already-cooled air going round rather than dragging in fresh hot air to chill from scratch, easing the load. And there is no point running the air conditioning in a stationary car with the engine idling just to cool down before you leave, since you burn fuel going nowhere; venting the hot air and driving off gets you cool sooner for less.</p>

    <h2>Electric cars: the same logic, in range</h2>
    <p>If you drive an electric car the trade-offs are identical, except the cost shows up as lost range rather than fuel. Air conditioning draws from the battery, open windows add the same speed-dependent drag, and the same low-speed-windows, high-speed-air-con rule applies. The one extra trick an electric car gives you is pre-cooling the cabin while it is still plugged in, so the initial blast of cooling comes from the mains and costs you no range at all, which the <a href="ev-range-in-hot-weather.html">EV range in hot weather</a> guide covers along with the rest of the summer range picture.</p>

    <h2>The bottom line</h2>
    <p>Staying cool need not cost much fuel if you match the method to the speed: windows down around town, where they are nearly free, and air conditioning on the motorway, where staying aerodynamic matters more than the few per cent the compressor uses. Better still, attack the heat before either: vent the trapped hot air, park in the shade and shade the windscreen, so there is far less heat to fight. Cool the car the smart way and a summer of driving costs barely more than a mild one.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is it more fuel-efficient to use air conditioning or open the windows?","acceptedAnswer":{"@type":"Answer","text":"It depends on speed. Below about 40 to 50 mph, open windows are cheaper, because the drag they add is small and you avoid the air-conditioning fuel penalty. At motorway speed, air conditioning wins, because aerodynamic drag from open windows grows sharply with speed and dominates. So windows down in town, windows up with air con on the motorway."}},{"@type":"Question","name":"How much does car air conditioning affect fuel economy?","acceptedAnswer":{"@type":"Answer","text":"Air conditioning typically costs around 4 to 8 per cent in fuel, roughly 4 per cent on a petrol car, a little more on a diesel and around 6 per cent on a hybrid. The penalty is largest in slow, stop-start traffic where the engine is doing little but the compressor still runs, and smallest at a steady cruise."}},{"@type":"Question","name":"Does opening car windows save fuel?","acceptedAnswer":{"@type":"Answer","text":"At low speeds, yes, because you avoid the air-conditioning fuel penalty and the extra drag is small. At higher speeds the drag from open windows grows steeply and can cost as much fuel as the air conditioning would, or more. The faster you drive, the less open windows save and the more sense it makes to shut them and use the air con."}},{"@type":"Question","name":"How can I keep my car cool and save fuel?","acceptedAnswer":{"@type":"Answer","text":"Dump the trapped heat before you drive by opening the doors or windows for a minute, park in the shade, and use a windscreen sunshade so the cabin does not bake. Then use windows down at low speed and air conditioning at high speed, set a comfortable rather than freezing temperature, and switch to recirculate once the car is cool."}}]}</script>
''',
)

PAGES["solar-panels-hot-weather"] = dict(
    title="Do solar panels work better or worse in hot weather?",
    description="Why solar panels actually produce slightly less when they get very hot, how the temperature coefficient works, why summer still gives by far the most generation despite the heat, what the ideal conditions really are, and what, if anything, you can do about it.",
    active="guides",
    blurb="Panels love light, not heat. Why a scorching day isn't their best, and why summer still wins overall.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">It seems obvious that the hotter and sunnier the day, the more your solar panels must be making. The first half is right and the second is not. Panels are driven by light, not heat, and in fact they produce slightly less for a given amount of sunlight when they get very hot. That sounds like bad news for a heatwave, but summer is still comfortably your best season for generation. Here is how that apparent contradiction works.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> Solar panels produce a little less per unit of sunlight when they get hot. Output falls by roughly 0.3 to 0.4 per cent for every degree the panel sits above 25C, and in strong sun a panel can reach 50 to 65C, trimming maybe 10 to 15 per cent off its peak. But summer still gives by far the most generation overall, because the long days and high sun more than make up for the heat penalty. A panel's ideal is a cold, bright, sunny day, not a baking one.</p>
    </div>

    <h2>Panels want light, not heat</h2>
    <p>A solar panel makes electricity from light, not from warmth, and these are not the same thing. You can have brilliant light on a cold, clear day, and you can have fierce heat under a hazy sky. What the panel converts is the light landing on it; the heat is, if anything, a mild hindrance. This is the point that catches people out, because we naturally lump "hot" and "sunny" together, when for a solar panel they pull in opposite directions. The <a href="solar-panels-the-basics.html">solar basics</a> guide covers how the panels turn that light into power; this one is about why the temperature of the panel matters separately.</p>

    <h2>Why heat reduces output</h2>
    <p>Every panel is rated at a standard cell temperature of 25 degrees, and its performance is measured against that. As the cells heat up beyond that point, the voltage they produce drops slightly, and so does their output. The figure is set by the panel's temperature coefficient, typically a loss of around 0.3 to 0.4 per cent for each degree above 25. That sounds trivial until you realise how hot a panel gets in full sun: sitting in direct sunlight on a still day, the cells can reach 50 to 65 degrees, well above the 25 they were rated at, so the accumulated penalty can be 10 to 15 per cent off the nameplate figure. The panel is still generating plenty; it is just generating a little less than its sticker would suggest, because it is running hot.</p>

    <h2>But summer still wins, easily</h2>
    <p>None of this means a heatwave is bad for your generation. The heat penalty is a small percentage knocked off a very large summer output, and that output is large because summer brings long days and a high sun, which together deliver far more light over a day than winter ever can. So your panels still make their most in the bright half of the year, heat penalty and all; a hot July day comfortably beats a cold December one despite the temperature working against it. The right way to think about it is that summer gives you a big cake with a thin slice taken off the top for heat, while winter gives you a much smaller cake to begin with.</p>

    <table class="ev-table">
      <thead><tr><th>Conditions</th><th>Generation</th></tr></thead>
      <tbody>
        <tr><td>Cold and bright, full sun</td><td>Best per hour, panels near their rated output</td></tr>
        <tr><td>Hot and sunny, heatwave</td><td>Slightly below peak, but long days mean a high daily total</td></tr>
        <tr><td>Warm but overcast or hazy</td><td>Much lower, because there is less light to convert</td></tr>
        <tr><td>Short winter days</td><td>Lowest total, little daylight however clear</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Light is what counts, and length of day with it. A cold sunny day gives the best output per hour; a hot sunny day gives the best total because the sun is up for so long.</p>

    <h2>The ideal conditions</h2>
    <p>If you wanted to design a perfect solar day, it would be cold and brilliantly sunny, the cells kept cool by the chill air while bathed in strong light. Those crisp, bright spring days, clear skies and a low temperature, are when panels often punch above their rated figure, which surprises owners who expected the height of summer to be the peak. The very hottest, stillest days of a heatwave are not quite the best per hour, because the panels are running hot, though the sheer length of daylight still makes them strong days overall.</p>

    <h2>Is there anything to do about it?</h2>
    <p>For a homeowner, almost nothing, and that is fine. Panels are mounted with an air gap behind them precisely so air can circulate and carry some heat away, which is part of why a roof array copes better than panels laid flat against a hot surface. Beyond ensuring nothing blocks that airflow, there is no day-to-day action worth taking; the heat penalty is a known, modest fact of how panels work, already accounted for in any sensible generation estimate. The more useful summer thought is what to do with all that long-day generation: a <a href="solar-battery-storage.html">solar battery</a> stores the midday surplus for the evening, and timing the washing, dishwasher and any car charging into the sunny middle of the day soaks up power you would otherwise export cheaply, which is where the real value lies, as the <a href="is-solar-worth-it.html">is solar worth it</a> guide explains.</p>

    <h2>The bottom line</h2>
    <p>Solar panels produce slightly less per unit of sunlight when they are hot, losing around 0.3 to 0.4 per cent a degree above 25, so on a baking day a panel running at 50 to 65 degrees gives maybe 10 to 15 per cent below its rated peak. But this is a thin slice off a big summer total: the long days and high sun mean summer is still by far your best generation season, and a cold, bright day is what a panel likes best per hour. Heat is a minor handicap, not a problem, and nothing for an owner to lose sleep over.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do solar panels produce less electricity in hot weather?","acceptedAnswer":{"@type":"Answer","text":"Slightly, yes. Panels are rated at a cell temperature of 25C, and output falls by roughly 0.3 to 0.4 per cent for every degree above that. In strong sun a panel can reach 50 to 65C, trimming around 10 to 15 per cent off its rated peak. It is still generating plenty, just a little less than the nameplate figure because it is running hot."}},{"@type":"Question","name":"Is summer or winter better for solar panels?","acceptedAnswer":{"@type":"Answer","text":"Summer, by a wide margin, despite the heat penalty. Summer's long days and high sun deliver far more light over a day than winter, so your panels make much more, even though running hot costs them a few per cent. A hot July day comfortably beats a cold December one for total generation."}},{"@type":"Question","name":"What is the ideal weather for solar panels?","acceptedAnswer":{"@type":"Answer","text":"Cold and brilliantly sunny. Strong light drives the output while the cool air keeps the panels near their rated temperature, so crisp, clear spring days often produce the best output per hour. The hottest days of a heatwave are slightly below peak per hour because the panels run hot, though long daylight still makes them strong overall."}},{"@type":"Question","name":"Can you stop solar panels overheating?","acceptedAnswer":{"@type":"Answer","text":"There is little a homeowner needs to do. Panels are mounted with an air gap behind them so air can circulate and carry heat away, which is why a roof array copes better than panels flat against a hot surface. Just keep that airflow clear; the modest heat penalty is normal and already built into any sensible generation estimate."}}]}</script>
''',
)

PAGES["fridge-freezer-in-hot-weather"] = dict(
    title="Why your fridge and freezer cost more to run in summer",
    description="A fridge or freezer works harder in a hot kitchen, because it has to pump its heat out into warmer surroundings. Why summer raises the running cost, where you put the appliance matters, the right settings, and the free habits that keep the bill down.",
    active="guides",
    blurb="A hot kitchen makes the fridge work harder. Why summer raises the cost, and the easy fixes.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">If your fridge seems to hum more in a heatwave, it is not your imagination. A fridge or freezer does not make cold so much as move heat, pumping it out of the cabinet into the room around it, and the hotter that room, the harder it has to work. Since the fridge-freezer runs around the clock all year, that extra summer effort quietly adds to the bill. The good news is that the fixes are simple and free.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> A fridge or freezer cools by pumping heat out into the room, so the hotter the room, the harder it works and the more it costs. A kitchen in a summer heatwave can push its running cost up noticeably. The fixes cost nothing: keep it out of direct sun and away from the oven, leave ventilation gaps around it, keep the door shut, let warm food cool before it goes in, and do not set it colder than it needs to be.</p>
    </div>

    <h2>Why heat makes it work harder</h2>
    <p>A fridge works by the same principle as an air conditioner: it gathers heat from inside the cabinet and dumps it out of the back, usually through the coils you can see or feel there. To do that it has to push the heat into the surrounding air, and that is only easy if the surrounding air is cooler than the heat being shed. In a warm kitchen the job gets harder, because the room it is dumping heat into is itself hot, so the compressor runs longer and more often to hold the inside cold. That is why the same appliance, holding the same temperature, costs more to run in a heatwave than in a cool month: not because the food is warmer, but because the room it lives in is.</p>

    <h2>Where you put it matters most</h2>
    <p>Because the fridge is fighting the temperature around it, its position is the biggest thing you control. Keep it out of direct sunlight, which can fall on it through a window and heat the cabinet directly. Keep it away from heat sources, above all the oven, but also a dishwasher, a boiler or a radiator, since standing next to something hot makes the fridge work against that heat all day. Avoid sites that bake in summer, like a conservatory or an unventilated garage. And leave a gap around the back and sides so the heat it sheds can actually escape, because a fridge crammed tight into a unit with no airflow ends up re-breathing its own warm air. While you are back there, brushing the dust off the coils now and then helps them shed heat efficiently, and a quick check that the door seals still grip keeps the cold where it belongs.</p>

    <h2>The right settings</h2>
    <p>It is tempting to crank the dial up in hot weather, but a fridge only needs to be cold enough to keep food safe, and every degree colder than that costs more to maintain. The table shows the sensible targets. Setting it colder than these wastes energy without keeping the food meaningfully safer.</p>

    <table class="ev-table">
      <thead><tr><th>Setting</th><th>Aim for</th></tr></thead>
      <tbody>
        <tr><td>Fridge temperature</td><td>3 to 5C</td></tr>
        <tr><td>Freezer temperature</td><td>-18C</td></tr>
        <tr><td>Gap around back and sides</td><td>a few centimetres for airflow</td></tr>
        <tr><td>Position</td><td>out of sun, away from the oven</td></tr>
      </tbody>
    </table>
    <p class="ev-note">A fridge thermometer costs little and takes the guesswork out, since the numbered dial is not a temperature. A well-stocked freezer also holds its cold better than an empty one, as the frozen mass acts as a buffer, so it cycles on less.</p>

    <h2>Hot-weather habits</h2>
    <p>A few small habits ease the load further when it is hot. Let warm leftovers cool to room temperature before putting them in, so the fridge is not asked to chill a hot dish in an already hot kitchen. Open the door less and close it promptly, because every opening lets cold air spill out and warm, humid summer air rush in to be cooled again. If the freezer has iced up, defrosting it helps, since a thick layer of frost makes it work harder. And resist over-filling the fridge so tightly that air cannot circulate inside, which leaves warm spots and makes the appliance run more to compensate.</p>

    <h2>The numbers, and when to replace</h2>
    <p>A fridge-freezer is one of the few appliances that never switches off, so it is a steady year-round cost, somewhere in the region of a couple of hundred kilowatt-hours a year for a modern one, more for an old or poorly placed model, and summer nudges that figure up. To see your own, the <a href="appliance-running-cost.html">running cost calculator</a> and the appliance's rated annual consumption tell you roughly what it costs at your unit rate. If yours is an old unit running hot and often, it is worth knowing that a tired fridge-freezer from twenty years ago can use several times the electricity of an efficient modern one, so when it finally needs replacing the <a href="energy-labels-explained.html">energy label</a> and the <a href="fridge-freezer-efficiency.html">fridge and freezer efficiency</a> guide are the place to start, since for an always-on appliance the running cost dwarfs the difference in purchase price.</p>

    <h2>The bottom line</h2>
    <p>Your fridge and freezer cost more in summer because they shed their heat into the room, and a hot room makes that harder, so the compressor runs more to hold the same cold. The cure is all about position and habits: keep the appliance out of the sun and away from the oven, give it room to breathe, set it no colder than it needs, let food cool before it goes in, and keep the door shut. None of it costs a penny, and together it keeps the one appliance that never rests from quietly costing you more than it should through the warm months.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Why does my fridge cost more to run in summer?","acceptedAnswer":{"@type":"Answer","text":"A fridge cools by pumping heat out of the cabinet into the room around it, and the hotter that room, the harder it has to push that heat away. In a warm kitchen the compressor runs longer and more often to hold the same inside temperature, so the same appliance costs more to run in a heatwave than in a cool month."}},{"@type":"Question","name":"Where should I not put a fridge or freezer?","acceptedAnswer":{"@type":"Answer","text":"Keep it out of direct sunlight and away from heat sources such as the oven, dishwasher, boiler or a radiator, and avoid hot spots like a conservatory or an unventilated garage. Leave a gap around the back and sides so the heat it sheds can escape, since a fridge crammed in with no airflow re-breathes its own warm air and works harder."}},{"@type":"Question","name":"What temperature should a fridge and freezer be?","acceptedAnswer":{"@type":"Answer","text":"Aim for 3 to 5C in the fridge and -18C in the freezer. Setting them colder than that costs more to maintain without keeping food meaningfully safer. The numbered dial is not a temperature, so a cheap fridge thermometer is worth using to check. A well-stocked freezer also holds its cold better than an empty one."}},{"@type":"Question","name":"How can I cut my fridge's running cost in hot weather?","acceptedAnswer":{"@type":"Answer","text":"Position it out of the sun and away from the oven, leave ventilation gaps around it, and keep the coils dust-free and the door seals intact. Let warm food cool before putting it in, open the door less, defrost an iced-up freezer, and do not set it colder than needed. If it is an old, inefficient unit, replacing it can cut the cost sharply."}}]}</script>
''',
)

PAGES["energy-saving-myths"] = dict(
    title="Energy-saving myths that cost you money",
    description="The common energy-saving beliefs that are wrong or exaggerated, from leaving the heating on low all day to unplugging phone chargers, and the small number of changes that genuinely move the bill instead.",
    active="guides",
    blurb="Leaving the heating on low all day, unplugging chargers, turning lights off for seconds: which advice is just wrong.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A surprising amount of received wisdom about saving energy is either plain wrong or so trivial that obsessing over it distracts from the things that actually matter. Believing the myths can cost you money directly, and worse, it can convince you that you are doing your bit while the expensive stuff runs unquestioned. Here are the common ones, and what the truth points you towards instead.</p>

    <h2>Leaving the heating on low all day is cheaper</h2>
    <p>This is the most stubborn myth of all. The claim is that it costs more to reheat a cold house than to keep it ticking over warm all day, so you should never let it cool. For almost every home this is false. A house constantly leaks heat to the colder outdoors, and the warmer you keep it the faster it leaks, so heating an empty house all day simply pays to replace heat you did not need. A well-timed system that warms the house when you are in and lets it cool when you are out or asleep uses less. The <a href="thermostat-settings.html">thermostat settings</a> guide covers how to time it properly.</p>

    <h2>Unplugging your phone charger saves meaningful money</h2>
    <p>A charger left in the wall with nothing plugged into it draws so little that switching it off saves a few pence a year at most. It is harmless to unplug it, but presenting it as a serious saving is the kind of advice that makes people feel virtuous while the <a href="tumble-dryer-cost.html">tumble dryer</a> quietly costs them a hundred times as much. The real standby savings come from the genuinely hungry always-on devices, as the <a href="standby-power-the-full-story.html">standby power</a> guide explains, not from the charger.</p>

    <h2>Turning lights off for a moment uses more than leaving them on</h2>
    <p>This was loosely true in the era of fluorescent tubes, where the start-up surge and the wear on the tube meant very brief switching had a small cost. With modern <a href="led-lighting.html">LED lighting</a> it is simply false: an LED costs effectively nothing to switch and wears no faster for it, so turn lights off whenever you leave a room, even briefly. The old rule has long outlived the technology that justified it.</p>

    <h2>Cranking the thermostat up heats the house faster</h2>
    <p>Turning the thermostat to its maximum does not make the house warm up any quicker; it only changes the temperature at which the heating stops. A thermostat is a target, not an accelerator. Setting it to twenty-eight to warm a cold room faster than setting it to twenty achieves nothing except that, if you forget it, the house overshoots to an expensive twenty-eight. Set it to the temperature you actually want and let it get there.</p>

    <h2>Boiling a full kettle is fine, the water keeps for later</h2>
    <p>Reboiling water you boiled earlier means heating it from cold again, so filling the kettle to the top for one cup wastes the energy used to heat all the water you did not use. The <a href="kettle-energy-saving.html">kettle guide</a> covers this, but the myth that a full kettle is harmless because the hot water is somehow saved is worth naming, because the water cools back down and the next cup starts from cold regardless.</p>

    <h2>Energy-saving gadgets and boxes that slash your bill</h2>
    <p>Be wary of devices sold with claims to cut your electricity use by some large percentage simply by being plugged in, whether described as power optimisers, voltage savers or similar. For an ordinary domestic supply these generally do little or nothing useful, and the bold percentage claims do not survive scrutiny. The things that genuinely cut bills are unglamorous: insulation, draught-proofing, heating controls, efficient habits and the right tariff. If a single plug-in box really delivered what is claimed, it would not need to be sold by the myth.</p>

    <h2>What actually moves the bill</h2>
    <p>Strip away the myths and the real list is short and dull, which is exactly why it works. Heating dominates most bills, so turning the thermostat down a degree, timing the heating to your day, sealing draughts and insulating the loft do the heavy lifting. After that come the hungry appliances, the <a href="tumble-dryer-cost.html">dryer</a>, the heating of <a href="hot-water-savings.html">water</a>, the electric shower, where habits and efficient use save real money. Put your own appliances through the <a href="appliance-running-cost.html">cost calculator</a> and the priorities sort themselves out. Spend your effort where the energy goes, and let the phone charger be.</p>
  </div></section>
''',
)

PAGES["solar-battery-storage"] = dict(
    title="Solar battery storage: worth adding or not?",
    description="How a home battery works with solar panels, why it lifts self-consumption, the trade-off between usefulness and cost, battery sizing, lifespan and the case for charging a battery from cheap off-peak electricity even without solar.",
    active="guides",
    blurb="A battery stores your midday sun for the evening. It makes solar more useful but rarely pays back faster.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A home battery is the natural-seeming companion to solar panels, and the question of whether to add one comes up in almost every solar quote. The honest position is that a battery makes a solar system more useful and more satisfying to live with, but it does not automatically make it pay back sooner, and for some homes it does the opposite. Understanding why lets you judge whether it is right for you.</p>

    <h2>The problem a battery solves</h2>
    <p>As the <a href="solar-panels-the-basics.html">solar basics</a> guide explains, the power you generate and use yourself is worth far more than the power you export to the grid for a low rate. The trouble is timing: panels generate most at midday, while a typical household uses most electricity in the morning and evening. Without storage, much of the midday generation is exported cheaply just when you are not there to use it, and then you buy expensive grid electricity back in the evening. A battery bridges that gap by storing the daytime surplus and releasing it when you need it after dark.</p>

    <h2>How it lifts self-consumption</h2>
    <p>By soaking up the midday excess and feeding it back in the evening peak, a battery raises the share of your own generation that you actually use rather than export. That is genuinely valuable, because every stored unit you later use is a unit of expensive grid electricity you did not have to buy. For a household that is out all day, where solar alone would export most of its output, a battery can be the difference between a system that mostly benefits the grid and one that mostly benefits you. The usefulness gain is real and immediate.</p>

    <h2>Why it rarely speeds up payback</h2>
    <p>Here is the catch that the usefulness story hides. Batteries are expensive, and the saving a battery adds, the difference between the low export rate and the higher import rate on the units it shifts, is real but modest per unit. Add the cost of the battery to the system and the extra saving often takes a long time to repay, frequently longer than the panels alone. So a battery typically improves how much of your solar you capture while lengthening, not shortening, the payback of the whole package. It buys usefulness and resilience, not a faster return.</p>

    <h2>Sizing it sensibly</h2>
    <p>Bigger is not automatically better. A battery far larger than your evening usage spends much of its capacity idle, paying for storage you never fill or empty, while one too small spills surplus you could have kept. The sweet spot is roughly matched to the evening and overnight usage you want to cover from stored sun, taking account of how much surplus your panels actually produce. An oversized battery is a common way to spend money that never earns its keep, so be sceptical of a quote that simply pushes the largest unit.</p>

    <h2>Lifespan and the long view</h2>
    <p>A battery is a consumable in a way panels are not. It degrades with use over the years, holding less charge as it ages, and may well need replacing within the life of the panels above it. That replacement cost belongs in any honest payback sum, and it is one reason the battery economics are tighter than the panel economics. Treat the battery as a component with a finite life, not a one-off purchase that lasts as long as the roof array.</p>

    <h2>The off-peak twist, even without solar</h2>
    <p>There is a use for a home battery that does not need solar at all. On a time-of-use tariff with cheap overnight electricity, you can charge the battery from the grid in the cheap window and run the house from it during the expensive day, pocketing the difference. With a <a href="smart-meters-explained.html">smart meter</a> and a tariff that has a wide enough gap between off-peak and peak rates, this arbitrage can stack on top of solar, or stand on its own. It turns the battery from a solar accessory into a way of buying all your electricity at the cheap rate, which for some households is the stronger case of the two.</p>

    <h2>So, add one or not?</h2>
    <p>Add a battery if you are out during the day and would otherwise export most of your solar, if you value evening self-sufficiency and some resilience to short outages, or if a time-of-use tariff lets you charge cheaply overnight. Be cautious if your payback expectation is short, if someone is home to use power as it is generated anyway, or if the quote leans on an oversized unit. As with the panels themselves in the <a href="is-solar-worth-it.html">is solar worth it</a> guide, do the cheap efficiency basics first, and treat the battery as a considered add-on rather than a default yes.</p>
  </div></section>
''',
)

PAGES["portable-heaters-running-cost"] = dict(
    title="Portable electric heaters: what they really cost",
    description="The running cost of plug-in electric heaters, why they are expensive to run despite being cheap to buy, when a portable heater is actually the economical choice, and how the different types compare.",
    active="guides",
    blurb="Cheap to buy, dear to run. When a plug-in heater saves money and when it quietly drains your wallet.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A plug-in electric heater costs little to buy and warms a room quickly, which makes it tempting in a cold snap. What the price tag hides is that electric heating is one of the most expensive ways to make warmth there is, so a cheap heater can run up a startling bill if you use it as a main source. Used cleverly, though, it can genuinely save money. The difference is all in how and when you reach for it.</p>

    <h2>Why electric heat is expensive</h2>
    <p>Every plug-in heater is essentially the same on cost: it turns electricity into heat at full efficiency, so a two-kilowatt heater uses two kilowatt-hours an hour whatever its shape or marketing. The expense is not inefficiency but the price of the fuel, because electricity costs several times more per unit than the gas a central heating boiler burns. So heating a room electrically costs far more than heating it with gas, even though the heater itself was cheap. Put a typical heater's wattage and a few hours a day into the <a href="appliance-running-cost.html">running cost calculator</a> and the figure is sobering.</p>

    <h2>When a portable heater actually saves</h2>
    <p>Despite all that, there is a real case for one. If you are spending the evening in a single room while the rest of the house sits empty, heating just that room with a portable heater can cost less than firing up the whole central heating system to warm the entire house. The trick is that you are heating one small space instead of many, so even at the dear electric rate the total can come out lower. This is the heater's proper job: spot-heating one occupied room, not replacing the central heating for the whole home.</p>

    <h2>Heat the person, not the room</h2>
    <p>The cheapest electric warmth of all heats you rather than the air. A small radiant or halogen heater pointed at where you sit, or a low-wattage heated throw or electric blanket, warms you directly for a fraction of the power needed to bring a whole room up to temperature. A heated throw might draw a hundred watts or so against a fan heater's two thousand, an enormous difference for similar comfort if you are sitting still. As the <a href="electric-blanket-vs-heating.html">electric blanket</a> guide covers, heating the body is often the smartest electric heating there is.</p>

    <h2>Do the types differ on cost?</h2>
    <p>For the same wattage, all electric heaters cost the same to run for a given time, because they all convert electricity to heat completely; the watts on the label decide the cost, not the technology. What differs is how the heat feels and how it is delivered. A fan heater warms a room fast but noisily and stops the moment it is off. A convector or oil-filled radiator heats more gently and evenly and an oil-filled one stays warm a while after switching off. A radiant or halogen heater warms objects and people in its line of sight quickly, which suits spot-heating. Choose by how you want the heat, then control the cost through the wattage and the hours, not by hoping one type is secretly cheaper.</p>

    <h2>Keeping the bill in check</h2>
    <p>If you use a portable heater, run it on a thermostat or timer where it has one, so it is not blasting at full power once the room is warm, and pick the lowest setting that keeps you comfortable. Close the door to keep the heat in the room you are paying to warm, and combine it with the free measures: a draught-sealed room and a closed curtain hold the warmth so the heater works less. And never leave one running in an empty room, since at the electric rate that is money burned for nothing.</p>

    <h2>The honest place for them</h2>
    <p>A portable electric heater is a targeted tool, not a heating system. It earns its keep warming one occupied room when heating the whole house would be wasteful, or warming you directly while you sit, and it costs you dearly if used as a substitute for properly sorted-out central heating. Get the <a href="thermostat-settings.html">heating controls</a>, <a href="draught-proofing.html">draughts</a> and insulation right first, and keep the plug-in heater for the genuine spot-heating job it is good at.</p>
  </div></section>
''',
)

PAGES["winter-energy-checklist"] = dict(
    title="Getting your home ready for winter",
    description="A practical autumn checklist to cut winter energy bills: heating controls and timing, bleeding radiators, draughts and curtains, protecting pipes, servicing the boiler, and the order to tackle it in.",
    active="guides",
    blurb="A run-through to do each autumn so the cold months cost less. Mostly free, an afternoon's work.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Most of a year's energy spending lands in the cold months, so a little preparation in autumn pays off all winter. None of this is dramatic, and most of it costs nothing, but worked through as a checklist before the first real cold it turns a house that haemorrhages heat into one that holds it. Here is the run-through, roughly in the order worth doing.</p>

    <h2>Set and time the heating</h2>
    <p>Start where the money is. Set the room <a href="thermostat-settings.html">thermostat</a> to the lowest temperature that is genuinely comfortable, a degree lower than habit if you can manage it with a jumper, and programme the heating to come on shortly before you wake and return and to drop back when you are out or asleep. Turn down the radiator valves in rooms you rarely use so you are not heating empty space. This single afternoon of setting controls properly is the biggest saving on the list.</p>

    <h2>Tune the heating system</h2>
    <p>Before the system works hard all winter, get more out of every unit of gas. <a href="how-to-bleed-radiators.html">Bleed the radiators</a> so they fill with hot water right to the top, move furniture and long curtains off them so the heat reaches the room, and turn down the <a href="boiler-flow-temperature.html">boiler flow temperature</a> to the low fifties so a condensing boiler runs in its efficient mode. If the boiler has not been serviced in a while, autumn is the time, both for efficiency and to catch a fault before it leaves you cold in January.</p>

    <h2>Stop the heat escaping</h2>
    <p>Now seal the leaks. Walk the house on a windy day and <a href="draught-proofing.html">draught-proof</a> the doors, windows, letterbox, loft hatch and the gaps around pipes and skirting, leaving the deliberate ventilation alone. Check the <a href="loft-insulation.html">loft insulation</a> is at full depth and top it up if the joists are showing. Hang or close heavy lined <a href="curtains-for-warmth.html">curtains</a> at dusk to keep the day's warmth in. Together these make the house feel warmer at a lower setting, which is where the heating saving comes from.</p>

    <h2>Protect against the freeze</h2>
    <p>A cold snap can cost far more than a high bill if a pipe bursts. Lag any exposed water pipes in unheated lofts, garages and outbuildings, and insulate the boiler's external condensate pipe, which can freeze and lock the boiler out on the coldest mornings. Know where your stopcock is. If you will be away, leave the heating ticking over on a low frost-protection setting rather than off entirely, so the house never drops to the point where pipes freeze.</p>

    <h2>Sort the hot water and the smaller stuff</h2>
    <p>Fit or check the <a href="cylinder-jacket-and-pipe-lagging.html">cylinder jacket</a> if you have a hot-water tank, and lag the nearby pipes, so stored hot water stays hot. Swap any remaining old bulbs for <a href="led-lighting.html">LEDs</a> now the dark evenings are drawing in and the lights are on for longer. Dig out the draught excluders, the warm bedding and the heated throw before you need them, so comfort does not tempt you to crank the thermostat up.</p>

    <h2>The order that pays</h2>
    <p>If you do nothing else, set and time the heating and seal the worst draughts, because those two cost nothing and deliver most of the benefit. Tune the boiler and top up the loft next. Leave any big spending, new windows, major insulation, a new boiler, for a considered decision rather than a panic in the first cold week. Worked through each autumn, this checklist is the difference between dreading the winter bills and barely noticing them.</p>
  </div></section>
''',
)

PAGES["keeping-cool-without-air-con"] = dict(
    title="Keeping cool in summer without air conditioning",
    description="How to keep a home cool in hot weather using little or no energy: shading and timing the windows, blocking the sun, using fans efficiently, and why a fan and air conditioning cost wildly different amounts to run.",
    active="guides",
    blurb="Block the sun by day, flush the cool in at night, and use a fan not a compressor. Cool rooms for pennies.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Hot spells are becoming more common, and the instinct is to reach for air conditioning, which is one of the heaviest electrical loads a home can run. Before you do, a handful of free or near-free habits keep a house markedly cooler, and where you do need help, a fan costs a tiny fraction of what a cooling compressor does. The same logic that governs keeping heat in during winter governs keeping it out in summer.</p>

    <h2>Block the sun before it gets in</h2>
    <p>The biggest source of unwanted summer heat is sunlight pouring through glass and warming everything it lands on. The cheapest cooling is to stop it at the window. Close curtains and blinds on the sunny side of the house during the day, particularly south and west-facing windows in the afternoon, and the room stays noticeably cooler. External shading, an awning, a shutter, even a temporary reflective blind, works better still because it stops the heat before it passes the glass. The same heavy <a href="curtains-for-warmth.html">curtains</a> that keep warmth in during winter keep the sun's heat out in summer.</p>

    <h2>Time the windows to the temperature</h2>
    <p>Opening windows feels like the obvious move, but timing matters. On a hot day the air outside is often warmer than inside by afternoon, so throwing the windows open then lets heat in rather than out. Instead, keep windows and curtains shut through the hottest part of the day to hold the cool, then open them wide in the evening and overnight when the outside air has dropped below the inside temperature, flushing the day's heat out and drawing cool air in. Opening windows on opposite sides of the house creates a through-draught that clears warm air quickly.</p>

    <h2>Use fans the clever way</h2>
    <p>A fan does not cool the air; it moves it, and moving air cools you by helping sweat evaporate, so a fan is only worth running when someone is in the room to feel it. Running a fan in an empty room is pure waste. A fan placed to draw cool evening air in through a window, or to push hot air out, helps flush the house. The crucial point on cost is that a fan draws only tens of watts, so running one for hours costs very little, as the <a href="appliance-running-cost.html">running cost calculator</a> will show.</p>

    <h2>Turn off the heat sources indoors</h2>
    <p>Your home makes its own heat, and on a hot day it all adds up. The oven and hob throw out a lot, so cook outside, use the <a href="air-fryer-running-cost.html">air fryer</a> or microwave, or eat cold food on the hottest days. Lights, especially any remaining old bulbs, and electronics left running all give off warmth, so switch off what you are not using. Even drying washing indoors adds heat and humidity. Removing these small internal sources keeps the baseline temperature down for nothing.</p>

    <h2>The cost gap between a fan and a compressor</h2>
    <p>This is the number that should give anyone pause before buying a portable air conditioner. A fan uses tens of watts; a portable air conditioner with a compressor draws around a kilowatt or more, perhaps thirty to fifty times as much, so running one through a heatwave can add a serious sum to the bill. Air conditioning genuinely cools the air where a fan cannot, but it is an expensive last resort, not a first move. Exhaust the free measures and the fan first, and reserve real cooling for the rare days when nothing else is enough. For the hard figures, the <a href="fan-running-cost.html">fan running cost</a> and <a href="air-conditioning-running-cost.html">air conditioning running cost</a> guides work both out, and the <a href="portable-air-conditioner-vs-fan.html">portable air conditioner versus fan</a> guide compares them side by side.</p>

    <h2>If you do use cooling, use it well</h2>
    <p>Where air conditioning is genuinely needed, the same discipline that controls any heavy load keeps the cost down. Cool only the room you are in rather than the whole house, shut its door and windows so you are not cooling the outdoors, set the target temperature modestly rather than as cold as it will go, and switch it off when you leave. Combined with shading and night ventilation, occasional, targeted cooling on the worst days costs far less than running a unit flat out because the free measures were skipped.</p>
  </div></section>
''',
)

PAGES["saving-energy-when-renting"] = dict(
    title="Cutting energy bills when you rent",
    description="Practical ways tenants can lower energy bills without making permanent changes: the no-cost habits, the cheap removable measures, what to ask the landlord for, and the tenant rights around energy efficiency.",
    active="guides",
    blurb="You cannot insulate someone else's walls, but renters have more levers than they think. Here they are.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Most energy-saving advice assumes you own your home and can insulate the loft or replace the boiler. Renters are stuck with someone else's building and someone else's appliances, which feels like there is little to be done. In fact tenants have more levers than they think, between the free habits, cheap removable measures, and things the landlord can be asked or required to sort out.</p>

    <h2>Start with what costs nothing</h2>
    <p>The biggest savings need no permission and no spending, because they are about how you use the home rather than changing it. Set the <a href="thermostat-settings.html">thermostat</a> a degree lower and time the heating to when you are actually in, turn down the radiator valves in rooms you do not use, wash clothes at <a href="washing-at-30-degrees.html">thirty degrees</a> and dry them on an airer rather than the dryer, boil only the water you need, and switch off the hungry standby devices. None of this touches the building, and together it makes a real dent whatever the state of the place.</p>

    <h2>Cheap, removable measures</h2>
    <p>You can improve a rented home temporarily with things you take with you when you leave. Removable draught excluders for doors, the cheap self-adhesive foam strips for window and door gaps, a chimney balloon in an unused fireplace, and heavy lined <a href="curtains-for-warmth.html">curtains</a> all cut heat loss and come away cleanly. Shrink-fit window insulation film is an inexpensive winter fix for single-glazed windows and peels off in spring. A <a href="cylinder-jacket-and-pipe-lagging.html">cylinder jacket</a>, if there is an exposed hot-water tank, is cheap and you can take it with you. These are tenant-friendly because they leave no trace.</p>

    <h2>Take your lighting with you</h2>
    <p>If the place still has old halogen or incandescent bulbs, swap them for <a href="led-lighting.html">LEDs</a>, which pay for themselves quickly through lower bills. Keep the original bulbs in a drawer and put them back when you move, taking your LEDs to the next place. It is one of the few efficiency improvements you can literally pack and carry, and it works in any rental.</p>

    <h2>Choose your own tariff</h2>
    <p>If you pay the energy bills directly and the account is in your name, you are usually free to switch supplier and tariff just as an owner would, which needs no landlord involvement and changes nothing physical. Make sure you are not languishing on an expensive default rate, submit regular meter readings so you are billed for what you use rather than an estimate, and compare on total annual cost as the <a href="switching-suppliers.html">switching guide</a> sets out. This is often the single biggest saving available to a renter, because it sidesteps the building entirely.</p>

    <h2>What to ask the landlord for</h2>
    <p>Some improvements need the landlord, and many are in their interest too, since an efficient property is more lettable and protects the building. It is reasonable to ask for loft insulation to be topped up, draughty external doors and windows to be sorted, an ageing inefficient boiler to be replaced, and a hot-water cylinder to be properly insulated. Framing it around tenant comfort, lower running costs and avoiding damp and condensation, which insulation and ventilation help prevent, tends to land better than demands. Get agreement in writing before spending your own money on anything fixed.</p>

    <h2>Know the minimum standards</h2>
    <p>Rented homes are generally subject to minimum energy-efficiency standards, and a property below a certain energy rating may not legally be let in many cases. If you are in a cold, clearly inefficient home, it is worth checking the property's energy performance certificate, which a landlord must usually provide, and understanding the standards that apply where you live. A property that falls short can give you grounds to press for improvements. The exact rules vary by jurisdiction and change over time, so check the current local position rather than relying on a fixed figure, but the principle is that tenants are not entirely without protection here.</p>
  </div></section>
''',
)

PAGES["quick-wins-under-a-tenner"] = dict(
    title="Energy-saving quick wins under a tenner",
    description="Cheap, fast energy-saving buys that cost very little and pay back quickly: draught strips, radiator reflectors, LED bulbs, a chimney balloon, pipe lagging, a plug-in energy monitor and more, with what each one does.",
    active="guides",
    blurb="A shopping list of small buys that each pay for themselves fast. Stack them and the bill really moves.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Not every saving needs a big spend or a contractor. A handful of cheap buys, none of them more than the price of a takeaway, each pay for themselves within a season or two, and stacked together they take a meaningful slice off a bill. Here is the shopping list, with what each one actually does, so you can spend a tenner at a time and see it come back.</p>

    <h2>Draught strips and excluders</h2>
    <p>A few pounds of self-adhesive foam or rubber strip seals the gaps around doors and windows, and a door brush or excluder stops the draught under an external door. This is the classic quick win: cheap, quick to fit, and you feel the difference the same evening because the room holds its warmth and feels comfortable at a lower setting. The full method is on the <a href="draught-proofing.html">draught-proofing</a> guide, but a single strip pack is the place to start.</p>

    <h2>LED bulbs</h2>
    <p>A single <a href="led-lighting.html">LED bulb</a> costs little and uses a fraction of the electricity of the old halogen or incandescent it replaces, lasting for years. Replace the bulbs in the rooms where the lights are on longest first, the kitchen and living room, and each one pays for itself quickly. There is no cheaper fit-and-forget saving, and you can buy them one or two at a time.</p>

    <h2>A chimney draught excluder</h2>
    <p>An open, unused chimney lets warm air stream out around the clock and can be one of the biggest draughts in the house. A chimney balloon or a wool chimney draught excluder costs only a few pounds and plugs the gap while still letting the flue breathe a little. Just remember to remove it before lighting a fire. For a house with a redundant fireplace, this is a surprising amount of saving for very little money.</p>

    <h2>Pipe and cylinder lagging</h2>
    <p>Foam pipe lagging slips over exposed hot-water pipes for a pittance and keeps the water hot on its way to the tap, while also protecting cold pipes from freezing. If you have a hot-water tank, a <a href="cylinder-jacket-and-pipe-lagging.html">cylinder jacket</a> is one of the fastest paybacks of all, stopping the heat you have paid for leaking away while the tank waits. Both are cheap, both fit by hand, and both save every day.</p>

    <h2>Radiator reflector panels</h2>
    <p>Behind radiators on external walls, a reflective panel or even foil on card bounces heat back into the room instead of letting it soak into the cold wall and escape. The saving per radiator is small, but the cost is tiny, so on the radiators that sit against outside walls it is worth doing, as the <a href="radiator-reflectors.html">radiator reflector</a> guide explains. Only bother with the ones on external walls.</p>

    <h2>A plug-in energy monitor</h2>
    <p>This one does not save energy itself; it tells you where to look. A cheap plug-in monitor sits between an appliance and the socket and shows exactly what it draws, revealing the hungry devices and the worst standby offenders so you can act on facts rather than guesses. Used to find one genuinely thirsty appliance or a power-hungry old set-top box, it pays for itself many times over. The <a href="using-a-plug-in-energy-monitor.html">energy monitor</a> guide covers how to use one.</p>

    <h2>The radiator key and a shower timer</h2>
    <p>The smallest buys of all still earn their place. A radiator bleed key costs almost nothing and lets you <a href="how-to-bleed-radiators.html">bleed trapped air</a> so radiators heat fully and the boiler works less. A simple shower timer, or just a chosen four-minute song, nudges shorter showers and less hot water heated. Add these to the list above and you have spent a few tenners across a season for savings that repeat for years.</p>
  </div></section>
''',
)

PAGES["electric-blanket-vs-heating"] = dict(
    title="Electric blanket versus heating the whole house",
    description="Why heating the bed or the body with an electric blanket can cost a fraction of warming a whole house, how the running costs compare, the safety points to watch, and when each makes sense.",
    active="guides",
    blurb="Warming the bed costs pennies; warming the house costs pounds. When heating the person beats heating the room.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">There is an old principle in keeping warm cheaply: heat the person, not the building. An electric blanket is the clearest example of it. Warming the small space immediately around your body costs a tiny fraction of bringing a whole house, or even a whole bedroom, up to temperature, and on a cold night the difference in cost is enormous for very similar comfort.</p>

    <h2>Why heating the body wins on cost</h2>
    <p>To warm a room you have to heat all the air in it and, through that, the walls, furniture and everything else, and much of that warmth then leaks away to the colder outdoors and gets replaced again. An electric blanket skips all of that and puts a modest amount of heat exactly where you are. A typical electric blanket or heated throw draws somewhere in the region of fifty to a hundred and fifty watts, against the two or three thousand watts of a fan heater or the far larger output of central heating. Putting those figures into the <a href="appliance-running-cost.html">running cost calculator</a> shows the gap starkly: a few pence for an evening under a blanket, against pounds for heating the house.</p>

    <h2>Underblanket, overblanket and heated throws</h2>
    <p>There are a few forms and they suit different uses. An underblanket sits on the mattress beneath the sheet and warms the bed, often used to take the chill off before you get in and then switched off or turned low to sleep. An overblanket lies on top like a duvet and warms you as you lie under it. A heated throw is a portable version for the sofa, draped over you while you watch television or read. All work on the same cheap principle, and a heated throw in particular can let you keep the living-room heating lower through an evening because you are warm under it regardless.</p>

    <h2>The running-cost comparison</h2>
    <p>Consider a winter evening. Heating the living room with central heating or a <a href="portable-heaters-running-cost.html">portable electric heater</a> warms the whole space at a cost of pounds over a few hours. Sitting under a heated throw drawing a hundred watts or so costs a few pence for the same period, while the thermostat can sit lower because your body is warm. At bedtime, warming the bed with an underblanket for half an hour costs almost nothing, against the expense of heating the bedroom to stay comfortable all night. The blanket does not replace heating the house entirely, but it lets you heat it less, which is where the saving lands.</p>

    <h2>Safety, which matters here</h2>
    <p>Electric blankets are safe when looked after but deserve respect because they combine electricity, heat and bedding. Buy one carrying the proper safety marks, check it regularly for fraying, scorch marks or damaged wiring, and replace an old or worn one rather than nursing it along. Follow the instructions on whether it can be left on overnight, since many modern underblankets are designed for all-night use on a low setting while older or cheaper ones are meant only for pre-warming. Do not use one that is creased or folded in a way the maker warns against, keep it flat, and never combine a blanket with a hot-water bottle. Unplug it if in doubt.</p>

    <h2>When each makes sense</h2>
    <p>Heating the person is the smart, cheap choice when one or two people are sitting still in the evening or warming a bed, which is most of the time the question comes up. Heating the room or house properly still matters when there are several people spread around, when you need the whole space comfortable for activity rather than sitting, or to keep the building above the point where damp and cold cause problems. The two work together: keep the house at a sensible base temperature as the <a href="thermostat-settings.html">thermostat settings</a> guide describes, then top up your own comfort cheaply with a blanket or throw rather than cranking the heating for everyone.</p>
  </div></section>
''',
)

PAGES["using-a-plug-in-energy-monitor"] = dict(
    title="Using a plug-in energy monitor to find the hungry appliances",
    description="How a cheap plug-in energy monitor works, what to measure with it, how to read standby and running costs from it, the difference from a whole-house display, and how to turn its readings into savings.",
    active="guides",
    blurb="A few pounds of kit that ends the guesswork. Plug it in and see exactly what each appliance costs.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Most energy advice asks you to estimate and assume. A plug-in energy monitor replaces the guesswork with measurement. It is a cheap gadget that sits between an appliance and the socket and tells you exactly what that appliance draws, both when running and when idle, so you can spend your effort on the things that actually cost money rather than the things you imagine do.</p>

    <h2>What it is and how it works</h2>
    <p>A plug-in monitor is a small adaptor: you plug it into the wall, plug the appliance into it, and a display shows the power being drawn in watts, and usually the energy used in kilowatt-hours over time. Better ones let you enter your price per unit so they show running cost directly in money. They cost only a few pounds, and unlike a whole-house display they tell you about one specific device at a time, which is exactly what you need to hunt down a culprit.</p>

    <h2>Reading running cost</h2>
    <p>The instantaneous watts tell you how hungry something is at that moment, but the useful figure is the energy used over real use. Leave the monitor in place for a representative day or week on a fridge, a games console or a router, and it accumulates the kilowatt-hours, which you multiply by your price per unit, or read straight off if you entered the price. This is how you turn a vague worry into a number. Feed the same figures into the <a href="appliance-running-cost.html">running cost calculator</a> to project the annual cost, and the priorities sort themselves: the device costing fifty pounds a year earns attention, the one costing fifty pence does not.</p>

    <h2>Catching the standby offenders</h2>
    <p>The monitor is at its most revealing on standby power. Plug it into the cluster of devices around the television, or an old set-top box, or a desktop computer left in sleep, and read what they draw while apparently off. As the <a href="standby-power-the-full-story.html">standby power</a> guide explains, the offenders are wildly uneven: some devices genuinely sip nothing, while others quietly pull several watts around the clock. The monitor names and shames them in seconds, so you can put the real culprits on a switched socket and leave the innocent ones alone instead of unplugging everything on principle.</p>

    <h2>What is worth measuring</h2>
    <p>Spend your measuring time on the unknowns and the suspected hogs. The fridge and freezer, since they run constantly and the figure surprises people. The <a href="tumble-dryer-cost.html">tumble dryer</a> and washing machine on a real cycle. The cluster of always-on electronics. An old appliance you suspect is inefficient, to decide whether replacing it is worth it. Mystery devices whose label you cannot find. There is less point monitoring things whose cost you can already work out from a clear wattage label and obvious usage, like a lamp or a kettle.</p>

    <h2>From reading to saving</h2>
    <p>A monitor saves nothing by itself; it tells you where to act. Once it has found a hungry always-on device, you can switch it off properly, replace an inefficient old appliance whose running cost justifies the change, or simply use a thirsty one less or more cleverly. The value is in cutting through assumption: people routinely fret over trivial loads while a genuine drain runs unnoticed, and a few pounds of monitor, used on a handful of devices, pays for itself many times over by pointing your effort at the right target. It is the most useful few pounds in this whole list of <a href="quick-wins-under-a-tenner.html">quick wins</a>.</p>
  </div></section>
''',
)

PAGES["television-and-entertainment-energy"] = dict(
    title="Televisions, consoles and home entertainment: the real cost",
    description="How much electricity a modern television and games console actually use, why screen size and brightness matter, the standby trap with consoles and set-top boxes, and simple settings that cut the cost.",
    active="guides",
    blurb="The telly itself is modest; the box of tricks around it is where the waste hides. What to switch and what to ignore.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The corner of the living room with the television, the box that feeds it, a games console and a sound system feels like it ought to be an energy drain, and parts of it are, though not always the parts you expect. The screen itself is usually modest in use; the bigger waste tends to hide in what those devices do when you think they are off.</p>

    <h2>What a television actually draws</h2>
    <p>A modern flat television is fairly efficient in use, drawing perhaps several tens to a couple of hundred watts depending mostly on its size and how bright the picture is. A small set sips very little; a very large, very bright one in a dark room can draw noticeably more. Run a few hours an evening, even the larger sets cost a manageable amount over a year, which the <a href="appliance-running-cost.html">running cost calculator</a> will quantify for your own model and viewing. The television is rarely the villain of the electricity bill; it is a steady, middling cost rather than a heavy hitter.</p>

    <h2>Screen size and brightness</h2>
    <p>Two things move a television's consumption most: the size of the panel and the brightness setting. A bigger screen has more area to light, so consumption climbs with size. Many televisions also ship in a vivid, retina-searing shop-floor picture mode set far brighter than a normal room needs, which uses more power for a picture that is often less pleasant to watch. Switching to a standard or home picture mode, and turning the backlight down to a comfortable level, trims the running cost and usually improves the viewing. Any automatic brightness or eco setting that dims the panel to suit the room helps too.</p>

    <h2>The standby trap</h2>
    <p>Here is where the real waste tends to sit, and it is rarely the television. Games consoles are the prime suspects: left in a connected or instant-on standby so they can download updates and wake quickly, some draw a meaningful amount around the clock, far more than a truly-off device. Set-top boxes and digital recorders are similar, staying half-awake to record and update. Over a year, a console and a recorder idling in these modes can quietly cost more than the television does in active use. A <a href="using-a-plug-in-energy-monitor.html">plug-in energy monitor</a> reveals exactly which of your devices are doing this.</p>

    <h2>Settings that cut the cost</h2>
    <p>The fixes are mostly free. On a games console, switch off the instant-on or connected standby in its power settings and let it power down fully when you finish, accepting that it takes a little longer to start and updates when you next turn it on. On a television, use the picture and eco settings above. Across the whole cluster, the device-by-device habits matter less than one simple move described next.</p>

    <h2>The one-switch solution</h2>
    <p>Rather than hunting through menus or crawling behind the unit each night, put the television, console, sound bar and the rest of the entertainment cluster on a single switched extension lead, and turn the lot off at the wall with one switch when you go to bed. That kills the standby draw of everything in one action, while leaving devices that genuinely need to stay on, like anything that records overnight, on a separate socket. It is the same principle as the wider <a href="standby-power-the-full-story.html">standby power</a> advice: do not fuss over every gadget, target the cluster that actually wastes power and switch it off together.</p>
  </div></section>
''',
)

PAGES["broadband-router-always-on"] = dict(
    title="The broadband router and other always-on devices",
    description="Why the broadband router is usually left on around the clock, what it and other always-on devices cost, when leaving them on is justified, and how to think about the small but constant loads in a connected home.",
    active="guides",
    blurb="Small draw, but it never sleeps. What the router and the other always-on bits really add up to in a year.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A modern home hums with devices that never switch off: the broadband router, the smart speaker, the doorbell, the various little boxes with a standby light. None of them draws much at any one moment, but running every hour of every day, the constant loads add up to a real, if modest, slice of the electricity bill. Knowing which are worth leaving on, and which are quietly wasteful, keeps that slice in proportion.</p>

    <h2>What the router costs</h2>
    <p>A broadband router draws only a handful of watts, but because it typically runs around the clock those watts accumulate into a steady annual figure, the kind of small constant load that the <a href="appliance-running-cost.html">running cost calculator</a> shows is more than the moment-to-moment draw suggests. It is not a large cost, comfortably in the every-little-helps category rather than among the heavy hitters, but it is real, and it is the archetype of the always-on device: trivial per hour, noticeable per year.</p>

    <h2>Why people leave it on, and when that is right</h2>
    <p>Routers are usually left on permanently for good reasons. They take a few minutes to reconnect, some home services such as internet-connected security cameras, smart heating or a landline that runs over broadband depend on the connection staying up, and frequent power cycling does the hardware no favours. For a household that uses the connection through the day, or relies on always-connected devices, leaving the router on is the sensible choice and the small running cost is the price of the convenience. There is little point switching it off for the sake of pennies if it disrupts things you rely on.</p>

    <h2>When switching off is worth it</h2>
    <p>The case for turning it off is narrow but real. If the house is genuinely empty and nothing depends on the connection, for instance overnight in a home with no smart devices or while away on holiday, switching the router off saves its standing draw and is fine for the hardware over those longer breaks. The judgement is simply whether anything needs it while you are not there. For most connected homes the answer is yes for short absences and no for long ones, so the holiday switch-off is the main opportunity.</p>

    <h2>The other always-on bits</h2>
    <p>Beyond the router sit the smart speakers, the voice assistants, the video doorbell, the standby lights on chargers and appliances, and the clocks on the oven and microwave. Individually each is tiny; collectively they form the baseline load your house draws even when you are doing nothing. The honest position, set out more fully in the <a href="standby-power-the-full-story.html">standby power</a> guide, is that this baseline is worth a tidy-up but not an obsession. Find the genuinely thirsty always-on devices with a <a href="using-a-plug-in-energy-monitor.html">plug-in monitor</a> and deal with those; leave the truly trivial ones be.</p>

    <h2>Keeping it in proportion</h2>
    <p>The always-on loads are a useful reminder of the principle running through this whole site: chase the big users first. The router and its companions are worth knowing about and tidying where it costs you nothing, but they will never rival the heating, the hot water or the <a href="tumble-dryer-cost.html">tumble dryer</a>. Switch off the entertainment cluster at night, turn the router off when the house is empty for a stretch if nothing needs it, and then stop worrying about the small constant loads and put your effort where the real money goes.</p>
  </div></section>
''',
)

PAGES["standing-charges-explained"] = dict(
    title="Standing charges explained, and what you can do about them",
    description="What the daily standing charge on your gas and electricity bill actually pays for, why you pay it even when you use nothing, why it varies by region and payment method, a worked example, and when a no-standing-charge tariff is worth it.",
    active="guides",
    blurb="The fixed daily fee you pay before using a single unit. What it covers, and the narrow cases where you can dodge it.",
    body='''
  <section class="section"><div class="wrap prose">
    <style>
      .ev-key{background:var(--paper-alt,#f4f1ea);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:6px 0 8px}
      .ev-key p{margin:0}
      .ev-table{width:100%;border-collapse:collapse;margin:14px 0;font-size:.97rem}
      .ev-table th,.ev-table td{border:1px solid var(--line);padding:9px 12px;text-align:left}
      .ev-table th{background:var(--paper-alt,#f4f1ea);font-weight:600}
      .ev-table td:not(:first-child),.ev-table th:not(:first-child){text-align:right}
      .ev-note{font-size:.9rem;color:var(--ink-soft,#5b5b5b)}
      @media(max-width:560px){.ev-table{font-size:.86rem}.ev-table th,.ev-table td{padding:7px 8px}}
    </style>

    <p class="lede">A standing charge is the fixed daily fee on your energy bill that you pay before you have drawn a single unit of gas or electricity. It shows up as a modest number in pence per day, it is easy to skim past, and across a year it grows into a real slice of what you hand over. Knowing what it covers, why it varies so much, and the few situations where you can sidestep it is worth the few minutes it takes to get your head round.</p>

    <div class="ev-key">
      <p><strong>The short answer.</strong> At the current Ofgem price cap, the average direct-debit standing charge is 57.19p a day for electricity and 29.04p a day for gas, so a dual-fuel home pays about 86p a day, roughly £315 a year, before using a single unit. It pays for staying connected to the network, not for the energy itself, so cutting your usage cannot reduce it. It varies by region and payment method, and only very low users come out ahead on a no-standing-charge tariff.</p>
    </div>

    <h2>What the standing charge actually pays for</h2>
    <p>The standing charge is the cost of keeping your home connected to the network rather than the cost of the energy you pull through it. It covers maintaining the wires, cables and pipes that reach your property, reading and servicing the meter, running your account, and a share of wider industry costs that suppliers are obliged to collect from everyone. Some of those costs are nothing to do with how much you personally burn; they are spread evenly across every connected household. A flat sitting empty for a month, drawing almost nothing, still owes the daily fee for staying plugged in.</p>

    <h2>Why your bill has two separate parts</h2>
    <p>Every energy bill is built from two numbers. There is the standing charge, a fixed amount per day that does not move whatever you do, and there is the unit rate, a price per kilowatt hour that you pay only on the energy you actually use. Use more and the second number climbs; the first stays put. This is why turning off lights and cutting your usage trims the variable part of the bill but never touches the fixed part. To see how the usage side stacks up appliance by appliance, the <a href="appliance-running-cost.html">running cost calculator</a> lets you plug in your own unit rate, but the standing charge sits underneath all of that as a floor you cannot cut by being frugal.</p>

    <h2>Two charges, gas and electricity</h2>
    <p>A home on mains gas and electricity pays a standing charge on each fuel, so there are two daily fees quietly running in the background, not one. A property with no gas supply pays only the electricity charge, which is one reason all-electric homes sometimes come out ahead on fixed costs even though their unit usage is higher. If you are on a two-rate meter such as <a href="economy-7-and-night-rates.html">Economy 7</a>, the standing charge works the same way; it is the day and night unit rates that differ, not the fixed daily fee.</p>

    <h2>Why it varies by region and how you pay</h2>
    <p>Two identical houses in different parts of the country can carry noticeably different standing charges. The biggest reason is the local network: the cost of distributing energy varies from region to region depending on the wires, the distances and the upkeep, and that regional cost is baked into the charge. How you pay matters too. Paying by direct debit is usually the cheapest route, while prepayment meters and paying on receipt of a paper bill can attract different fixed costs. The regulator caps the standing charge on standard tariffs, but the cap itself differs by region and by payment method, so there is no single national figure to memorise. The only number that matters is the one printed on your own tariff.</p>

    <h2>A worked example with the current cap</h2>
    <p>Put real numbers on it. At the Ofgem price cap for 1 July to 30 September 2026, the average direct-debit standing charges are 57.19p a day for electricity and 29.04p a day for gas. The table shows what each comes to over a week and a year.</p>

    <table class="ev-table">
      <thead><tr><th>Standing charge</th><th>Per day</th><th>Per week</th><th>Per year</th></tr></thead>
      <tbody>
        <tr><td>Electricity</td><td>57.19p</td><td>~£4.00</td><td>~£209</td></tr>
        <tr><td>Gas</td><td>29.04p</td><td>~£2.03</td><td>~£106</td></tr>
        <tr><td>Both combined</td><td>86.23p</td><td>~£6.04</td><td>~£315</td></tr>
      </tbody>
    </table>
    <p class="ev-note">Ofgem price cap, 1 July to 30 September 2026, Great Britain average for direct debit. Standing charges vary by region and differ again for prepayment or paying on receipt of a bill, so check your own tariff for the figure that applies to you.</p>

    <p>So a dual-fuel home hands over about 86p every day, some £315 a year, before boiling a kettle or running the heating, none of it related to how careful you are. Now picture a small, efficient flat that uses very little energy: those fixed daily fees make up a large fraction of its whole bill, while the actual energy is a smaller part. A large, busy family home pays exactly the same fixed fees, but they shrink to a small slice of a much bigger total. The floor is identical for both; what differs is how much usage stacks on top of it.</p>

    <h2>Can you avoid it? No-standing-charge tariffs</h2>
    <p>A handful of suppliers offer tariffs with no standing charge at all, and on paper that sounds like a clean escape. The catch is that the fixed cost has to be recovered somewhere, so these deals carry a higher unit rate to make up for it. That maths only works in your favour if you use very little energy, because then the saving on the missing daily fee outweighs the extra you pay per unit. A second home, a rarely used flat or a single person in a tiny space can come out ahead on a no-standing-charge deal; a normal household that uses a fair amount of energy almost always pays more overall, because the higher unit rate bites on every kilowatt hour. Run the comparison on your own usage before assuming a zero-standing tariff is cheaper, since for most homes it is not.</p>

    <h2>Who the standing charge hits hardest</h2>
    <p>The fixed nature of the charge falls heaviest on low users. If you have insulated well, switched to efficient appliances and cut your consumption right down, you reach a point where most of your bill is the standing charge and there is little usage left to trim. That can feel unfair, and it shapes where your effort is best spent: for a very low user the lever is the tariff and the standing charge itself, not yet more usage cuts. For a high user the priority is the other way round, since the unit rate on a lot of energy dwarfs the fixed fee, and the savings live in the heating, the hot water and the heavy appliances. The <a href="understanding-energy-bill.html">guide to reading your bill</a> shows where each of these numbers sits.</p>

    <h2>Where to find yours and what to check</h2>
    <p>Your standing charges are printed on every bill and on your annual statement, usually in the tariff details, shown separately for gas and electricity in pence per day. It is worth a look whenever your deal is up for renewal or when you are thinking of <a href="switching-suppliers.html">switching supplier</a>, because a tariff with a tempting unit rate can hide a high standing charge, and one with a low daily fee can carry a steep unit rate. Compare both numbers together rather than fixating on the headline price per unit. Work out roughly how much energy you use across a year, multiply by the unit rate, add the standing charge over 365 days, and you have a like-for-like total that tells you which deal costs less in practice for the way you live.</p>
  </div></section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much is the standing charge on energy bills?","acceptedAnswer":{"@type":"Answer","text":"At the Ofgem price cap for 1 July to 30 September 2026, the average direct-debit standing charge is 57.19p a day for electricity and 29.04p a day for gas, about 86p a day combined. That is roughly \\u00a3315 a year for a dual-fuel home before any energy is used. The figure varies by region and is different for prepayment or paying on receipt of a bill."}},{"@type":"Question","name":"What does the standing charge pay for?","acceptedAnswer":{"@type":"Answer","text":"It pays for keeping your home connected to the energy network rather than for the energy itself: maintaining the wires, cables and pipes to your property, reading and servicing the meter, running your account, and a share of wider industry costs spread across all households. You pay it even if you use nothing."}},{"@type":"Question","name":"Can you avoid paying a standing charge?","acceptedAnswer":{"@type":"Answer","text":"A few suppliers offer no-standing-charge tariffs, but they carry a higher unit rate to recover the fixed cost, so they only save money for very low users such as a second home or a rarely used flat. For a normal household the higher unit rate costs more overall, so compare both numbers on your own usage before switching."}},{"@type":"Question","name":"Why do I pay a standing charge if I use no energy?","acceptedAnswer":{"@type":"Answer","text":"Because the standing charge covers the cost of staying connected to the network, not the energy you draw. The wires, pipes and meter still have to be maintained and your account run whether or not you use anything, so the daily fee applies even to an empty property. Cutting your usage reduces the unit-rate part of the bill but never the standing charge."}}]}</script>
''',
)

PAGES["drying-clothes-without-a-tumble-dryer"] = dict(
    title="Drying clothes without a tumble dryer",
    description="The cheaper ways to dry a wash, from a hard spin and a washing line to heated airers and dehumidifiers, what each costs to run with worked examples, the condensation trap of drying indoors, and how to match the method to your home.",
    active="guides",
    blurb="The dryer is one of the thirstiest things in the house. Several cheaper ways to get a load dry, and what each really costs.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A tumble dryer is one of the thirstiest appliances in the house, and for much of the year you do not need it at all. There are cheaper ways to get a load dry, from the entirely free (a washing line and a hard spin) to a couple of low-watt gadgets that cost pennies a session. The skill is in matching the method to the weather, the space you have and how quickly you need the clothes back.</p>

    <h2>Why the tumble dryer is the expensive option</h2>
    <p>A tumble dryer dries clothes by heating air and tumbling the load through it, and heating air takes a great deal of electricity. A traditional vented or condenser dryer pulls something like two to three kilowatts while it runs, so a full cycle can get through a few units of electricity; at an example price of 30p per kWh that puts a single load somewhere around 60p to 90p, and several loads a week mount up over a year. Newer heat pump dryers are far gentler on electricity, often using roughly a third as much, though they cost more to buy and dry more slowly. The full breakdown sits on the <a href="tumble-dryer-cost.html">tumble dryer running cost</a> guide; the point here is that almost any method without a large heating element undercuts it, so the dryer is best kept for the days nothing else will do.</p>

    <h2>Get more water out before you start</h2>
    <p>The biggest free win happens in the washing machine, before drying begins at all. A faster spin flings more water out of the fabric mechanically, and water thrown out by the spin is water you do not then have to evaporate with electricity or time. Selecting a 1400 spin rather than 1000, where the fabric can take it, leaves the load noticeably drier coming out of the drum, which shortens every drying method that follows. Delicate items and certain fabrics need a gentler spin, so it is not a blanket rule, but for towels, bedding and everyday cottons a hard final spin is close to free money. The <a href="washing-machine-running-cost.html">washing machine running cost</a> guide covers the spin settings, and washing on a sensible <a href="washing-at-30-degrees.html">cool cycle</a> keeps the wash itself cheap to begin with.</p>

    <h2>The free option: line and air drying</h2>
    <p>Outdoors on a breezy day, even in winter, a washing line dries a load for nothing. Wind matters more than warmth here, since moving air carries moisture away even when it is cold, so a bright blustery January afternoon can dry a line of washing surprisingly well. Indoors, a clothes horse near a slightly open window or in a room with decent airflow costs nothing to run either, though it is slow and, done carelessly, it dumps moisture into the house. Air drying is the cheapest method there is, and for households with outdoor space and a flexible routine it handles most of the year on its own.</p>

    <h2>Heated clothes airers</h2>
    <p>A heated airer is a folding rack with warm bars, and its appeal is the modest power draw: typically somewhere around 100 to 300 watts, against the two to three kilowatts of a tumble dryer. Run a 300 watt airer for, say, five hours and you have used about 1.5 kWh, which at an example 30p per kWh is roughly 45p, and a smaller model left on for a shorter spell costs less again. Draping a sheet or a fitted cover over the loaded airer traps the warm air around the clothes and speeds things up considerably for no extra electricity. Drying is slower than a dryer, so an airer suits a household that can hang a load in the evening and collect it dry the next day rather than one needing clothes back within the hour. To check the figure for your own model, its wattage and a typical run time go straight into the <a href="appliance-running-cost.html">running cost calculator</a>.</p>

    <h2>Dehumidifiers: drying the room, not the clothes</h2>
    <p>A dehumidifier takes a different approach. Instead of heating the washing, it pulls moisture out of the air in the room, which speeds the drying of anything hanging there and, as a bonus, protects the house from damp and condensation. A typical domestic dehumidifier draws around 150 to 300 watts, similar territory to a heated airer, so running one for a few hours to dry a room of washing costs pennies rather than pounds. The water it removes collects in a tank you empty, visible proof of the moisture it is taking out of the air before that moisture can settle on cold walls and windows. In a damp flat the same machine earns its keep year round, not just on wash day.</p>

    <h2>Pairing an airer with a dehumidifier</h2>
    <p>The combination that works best for indoor drying is a heated or ordinary airer in a smallish room with the door shut and a dehumidifier running alongside it. The airer encourages evaporation, the dehumidifier whisks the resulting moisture out of the air so the clothes keep giving up water rather than reaching a soggy stalemate, and the closed room concentrates the effect. Two low-watt devices together still draw far less than a tumble dryer, so even running both for a few hours the total stays low, perhaps under a pound for a full load at example rates, while the room stays dry and the washing comes out fresh. For a flat with no outdoor space this pairing is often the cheapest reliable way to dry clothes through the wetter months.</p>

    <h2>The damp trap of drying indoors</h2>
    <p>A wet wash holds litres of water, and when it dries indoors that water has to go somewhere. Without ventilation or a dehumidifier it ends up on the coldest surfaces in the house, the windows and outside walls, where it feeds condensation and, in time, mould. That is the hidden cost of careless indoor drying: a cheaper energy bill paid for with a damp home. The fixes are simple. Crack a window or run an extractor fan in the room where clothes are drying, or let a dehumidifier do the same job by capturing the moisture directly. Slinging wet washing over radiators is tempting and cheapish, but it chills the radiator, makes the boiler work harder to heat the room and adds the same load of moisture to the air, so an airer next to a warm radiator beats draping clothes straight onto it.</p>

    <h2>Matching the method to your home</h2>
    <p>Which approach wins comes down to your space and your schedule. A house with a garden and a flexible routine should lean on the washing line whenever the weather allows and keep a cheap clothes horse for wet days. A flat with no outdoor space is the natural home for a heated airer and a dehumidifier working together, with the door shut and the moisture managed. Anyone who must have a load dry within the hour, for shift work or a sudden soaking, keeps a tumble dryer for those moments while drying everything else the cheaper way. Start with a hard spin every time, dry for free outdoors when you can, reach for the low-watt gadgets when you cannot, and save the dryer for the days nothing else will do.</p>
  </div></section>
''',
)

PAGES["hot-tub-running-cost"] = dict(
    title="What a hot tub really costs to run",
    description="A hot tub is one of the most expensive things you can keep at home. Why it costs so much, what drives the figure, and how to keep the running cost under control.",
    active="guides",
    blurb="One of the priciest things you can plug in at home. What drives the cost and how to tame it.",
    pubdate="2026-06-06",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A hot tub is a lovely thing to own and a quietly alarming thing to run. Unlike most appliances, which cost something only while you use them, a hot tub spends most of its life keeping a large body of water hot and gently circulating whether you are in it or not. That round-the-clock duty is what makes it one of the most expensive items a household can keep.</p>
    <h2>Why it costs so much</h2>
    <p>Two things run up the bill. The first is heating: keeping a few hundred litres of water at around 38 degrees, day and night, in the open air, means the heater fires regularly to replace heat lost to the cold around it. The second is the circulation and filtration pump, which runs for hours every day to keep the water clean, and which on many tubs also helps move heat about. Heating water is energy-hungry at the best of times, and a hot tub does it continuously, which is the opposite of how you keep an energy bill down.</p>
    <h2>What it adds up to</h2>
    <p>The honest answer is that it varies enormously, from a manageable monthly sum for a well-insulated tub used in summer to a genuinely painful one for a poorly insulated tub kept hot through a cold winter. Rather than trust a single scary figure, find your tub's heater and pump wattage and put them through the <a href="appliance-running-cost.html">running cost calculator</a> with a realistic estimate of how many hours a day each runs. The result is usually a wake-up call, and it tells you your own number rather than someone else's.</p>
    <h2>The factors that decide your bill</h2>
    <p>A handful of things separate a cheap-to-run tub from a ruinous one. Insulation is the biggest: a well-insulated cabinet and, above all, a thick, well-fitting, undamaged cover make a huge difference, because most of the heat escapes from the surface. The temperature you hold matters, since every degree costs more to maintain. So does the weather, as a cold, windy, exposed location loses heat far faster than a sheltered one. And of course how often and how long you use it, since opening the cover and reheating after a soak both add up.</p>
    <h2>How to cut the cost</h2>
    <p>Start with the cover, because it is the cheapest big win: keep it on whenever the tub is not in use, replace it when it becomes waterlogged and heavy, and consider a thermal blanket on the water surface underneath it. Set the temperature to the lowest you actually enjoy. Site the tub somewhere sheltered from wind. If you only use it at weekends, work out whether dropping the temperature between uses saves more than the energy to reheat, which depends on your tub and climate. And if you are on a tariff with cheap off-peak electricity, heating mainly in that window helps.</p>
    <h2>The honest bottom line</h2>
    <p>A hot tub is a luxury, and run as one it carries a luxury running cost that no amount of tweaking makes trivial. The sensible approach is to go in with eyes open: know roughly what it costs you using the calculator, keep that cover on religiously, hold a sensible temperature, and treat the bill as part of the price of the pleasure rather than a surprise. The single most effective thing you can do is also the simplest, which is to never leave it uncovered.</p>
  </div></section>
''',
)

PAGES["ground-vs-air-source-heat-pumps"] = dict(
    title="Ground source versus air source heat pumps",
    description="Both heat pumps move heat rather than burn fuel, but ground source and air source differ on efficiency, installation cost and disruption. How to tell which suits your home.",
    active="guides",
    blurb="Both move heat instead of making it. How the two types differ on efficiency, cost and disruption.",
    pubdate="2026-06-08",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">If you have read the <a href="heat-pumps-explained.html">heat pumps explained</a> guide, you know the basic trick: a heat pump gathers warmth from outside and concentrates it to heat your home, delivering several units of heat for each unit of electricity. The two main types, ground source and air source, do the same job but gather that warmth from different places, and that difference shapes the cost, the efficiency and how much your garden gets dug up.</p>
    <h2>Same idea, different source</h2>
    <p>An air source heat pump takes heat from the outside air using a unit that sits outside the house, much like an air conditioner working in reverse. A ground source heat pump takes heat from the ground instead, through pipes buried in trenches or sunk down boreholes, where the temperature stays fairly constant all year. That last point is the crux: the ground a metre or two down barely changes temperature between summer and winter, while the air can be freezing on the very days you most need heat.</p>
    <h2>Efficiency</h2>
    <p>Because the ground is a warmer, steadier source in winter than cold air, a ground source system tends to run more efficiently and more consistently, especially in the depths of a cold snap when an air source unit has to work hardest against the lowest temperatures. Air source pumps have improved a great deal and perform well in most British winters, but on the coldest days their efficiency dips while a ground source system carries on much as before. Over a year, ground source usually edges it on running cost.</p>
    <h2>Installation cost and disruption</h2>
    <p>This is where the picture flips. An air source unit is comparatively cheap and quick to install, needing little more than a spot outside for the unit and the connections indoors, which is why the great majority of installations are air source. Ground source is a bigger undertaking: you need either enough land for long trenches or the budget for deep boreholes, plus the groundworks to install the pipe loops, all of which costs substantially more and makes more mess. The hardware lasts a long time, but the upfront figure and the disruption are real barriers.</p>
    <h2>Which suits you</h2>
    <p>Air source suits most homes, particularly where space is limited, budgets are tighter, or you want a simpler job, and it pairs well with the same insulate-first approach every heating upgrade needs. Ground source comes into its own where you have the land and the budget, want the best long-term efficiency, or are building or deeply renovating anyway so the groundworks are less of an imposition. Both reward a well-insulated, draught-proofed home that can be kept warm with gentle, steady heat rather than short hot blasts.</p>
    <h2>The bottom line</h2>
    <p>Ground source heat pumps are generally the more efficient and steadier performers, but they cost more and need land and groundworks, while air source pumps are cheaper, simpler and good enough for most homes, at a small efficiency cost on the coldest days. For the average household the practical choice is usually air source; ground source makes most sense with the space, the budget and a long horizon. Either way, do the cheap fabric improvements first so whichever pump you fit has less work to do.</p>
  </div></section>
''',
)

PAGES["solar-water-heating"] = dict(
    title="Solar water heating: still worth it next to solar panels?",
    description="Solar thermal panels heat your water directly, which is different from the electricity-generating PV panels most people fit. How it works, what it delivers, and where it still makes sense.",
    active="guides",
    blurb="Solar thermal heats your water directly. How it differs from PV, and where it still earns its place.",
    pubdate="2026-06-10",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">When people say solar these days they usually mean the electricity-generating panels covered in the <a href="solar-panels-the-basics.html">solar basics</a> guide. But there is an older, more single-minded technology that is easy to forget: solar water heating, or solar thermal, which uses the sun to heat your hot water directly rather than to make electricity. It does one job, and for that job it does it well.</p>
    <h2>How it works</h2>
    <p>Solar thermal uses collectors on the roof, either flat panels or evacuated glass tubes, through which a fluid circulates. The sun heats that fluid, which is pumped down to a coil inside your hot-water cylinder, transferring its warmth to the water you actually use. It needs a compatible cylinder, usually one with two coils so the boiler or immersion can top up the heat when the sun cannot, and it works alongside your existing heating rather than replacing it.</p>
    <h2>What it delivers</h2>
    <p>On a sunny day in the warmer half of the year, solar thermal can provide most or all of a household's hot water, which is a meaningful chunk of the energy bill given that <a href="hot-water-savings.html">heating water</a> is often the second largest use in a home. In winter it delivers far less, because there is less sun and the incoming water is colder, so your boiler does most of the work then. Realistically it covers a good share of your annual hot water, concentrated in spring through autumn, rather than the whole year.</p>
    <h2>Solar thermal versus solar PV</h2>
    <p>This is the live question, because roof space and budget are limited. Solar thermal is very efficient at its one task of heating water, more so per square metre than PV is at the same job. But PV is far more flexible: it makes electricity you can use for anything, including heating water through an immersion via a simple diverter, as well as running the house and charging a car. Because of that flexibility, and falling panel prices, many households now fit PV instead and use some of its output for hot water, getting water heating as one benefit among several rather than a single-purpose system.</p>
    <h2>Is it worth it?</h2>
    <p>Solar thermal still makes sense in specific situations: where hot-water demand is high, where you want the most efficient possible water heating from limited roof space, or where you are replacing the cylinder anyway and the system can be fitted neatly. For many others, PV with a hot-water diverter is the more versatile use of the same roof and money. As with any larger investment, do the cheap efficiency basics first, get a proper assessment for your specific roof and demand, and treat the payback as long and steady rather than quick.</p>
    <h2>The bottom line</h2>
    <p>Solar water heating is a proven, efficient way to cover much of your hot water from spring to autumn, working alongside your boiler for the rest. Its limitation is that it does only that one thing, while solar PV makes flexible electricity that can heat water and much else, which is why PV has become the more popular choice. If hot water is your priority and the fit is right, solar thermal still earns its keep; for most, PV is the more adaptable option.</p>
  </div></section>
''',
)

PAGES["ev-running-cost-vs-petrol"] = dict(
    title="Electric car versus petrol: the running-cost comparison",
    description="Beyond the price at the pump or the plug, how an electric car and a petrol car compare to run day to day, where the savings are real, and the caveats that affect the total picture.",
    active="guides",
    blurb="Fuel is only part of it. How an EV and a petrol car really compare to run, and where the savings are real.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The headline reason people consider an electric car is running cost, and on the day-to-day numbers an EV genuinely tends to win, especially if you can charge at home. But fuel is only one line of the comparison, and an honest look at how the two stack up has to take in servicing, the caveats around charging, and the bigger costs of owning the car at all.</p>
    <h2>Energy versus fuel, per mile</h2>
    <p>This is where the EV pulls ahead. As the <a href="ev-charging-at-home-cost.html">home charging</a> guide sets out, an electric car charged on an off-peak overnight tariff can cost only a few pence a mile in energy, a level petrol simply cannot reach, because each mile of petrol is several times dearer than the equivalent cheap-rate electricity. Even on a standard electricity tariff the EV usually costs less per mile than a comparable petrol car. The size of the win depends heavily on your tariff, so the off-peak charging is the lever that turns a modest saving into a large one.</p>
    <h2>Servicing and maintenance</h2>
    <p>An electric car has far fewer moving parts than a petrol one: no oil changes, no exhaust, no clutch, far less to wear out, and regenerative braking even spares the brake pads. That generally means lower routine servicing and maintenance costs over the years. Petrol cars have a long, familiar list of consumables and services that quietly add up, and the EV sidesteps most of it.</p>
    <h2>The caveats</h2>
    <p>The day-to-day savings come with conditions worth stating plainly. If you cannot charge at home and rely on public rapid chargers, the per-mile cost rises sharply and can approach petrol, eroding the main advantage. Electric cars also tend to cost more to buy upfront, and depreciation and battery longevity are part of the lifetime sum, not just the energy. So the running-cost win is real but it sits inside a bigger picture that includes the purchase price and how you will charge.</p>
    <h2>The total picture</h2>
    <p>Put together, an electric car driven by someone who charges at home, especially off-peak, usually costs noticeably less to run and maintain than an equivalent petrol car, and the fuel saving is the clearest single advantage of going electric. Whether that adds up to a better overall deal depends on the upfront cost, how long you keep the car, and your charging situation. If you still run petrol, the habits on the <a href="hypermiling.html">hypermiling</a> page remain the way to trim its thirst; if you go electric, charging at the right time is the equivalent skill.</p>
    <h2>The bottom line</h2>
    <p>On running costs, the electric car generally wins: cheaper energy per mile, especially on an off-peak home tariff, and lower servicing thanks to far fewer moving parts. The caveats are upfront price, depreciation, and the fact that relying on public rapid charging undercuts the fuel saving. Decide on the whole-life cost and your charging reality, not the per-mile figure alone, but that per-mile figure is firmly in the EV's favour.</p>
  </div></section>
''',
)

PAGES["energy-performance-certificate-explained"] = dict(
    title="Your EPC explained: what the energy rating means",
    description="The A to G energy rating on your home, what an Energy Performance Certificate actually tells you, where it matters, its limitations, and how to improve your rating.",
    active="guides",
    blurb="The A-to-G rating on your home: what it really tells you, where it matters, and how to improve it.",
    pubdate="2026-06-14",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">If you have bought, sold or rented a home, you will have seen an Energy Performance Certificate, the coloured chart that rates a property from A down to G. It is one of the few official measures of how energy-efficient a home is, and it is worth understanding what it does and does not tell you, because it is easy to read too much or too little into it.</p>
    <h2>What an EPC is</h2>
    <p>An EPC rates a property's energy efficiency on a scale from A, the most efficient, to G, the least, based on an assessment of its construction, insulation, heating system, hot water and lighting. The certificate comes with an estimated energy cost and, usefully, a list of recommended improvements with a sense of their impact. It is produced by an accredited assessor who surveys the property, and it is valid for a number of years.</p>
    <h2>Where it matters</h2>
    <p>An EPC is required when a home is built, sold or let, so it follows your property at the big moments. For landlords it carries extra weight, because rented homes generally have to meet a minimum energy rating to be let legally, and that threshold has been tightening over time. The rating can also affect eligibility for some grants and schemes, and increasingly buyers and tenants look at it as a guide to what a place will cost to keep warm. The exact rules and minimum standards vary by jurisdiction and change, so check the current local position rather than assuming.</p>
    <h2>What it does and does not tell you</h2>
    <p>Here is the important caveat: an EPC is a standardised model, not a measurement of your actual bills. It assumes a typical household and standard patterns of use, so two identical homes get the same rating even if one family runs the heating constantly and another barely at all. Your real costs depend on how you live as much as on the building. Treat the EPC as a fair guide to the fabric and systems of the home, and a useful to-do list, rather than a prediction of your personal bill.</p>
    <h2>How to improve your rating</h2>
    <p>The improvements that lift an EPC are the same ones that genuinely cut bills, which is reassuring. Topping up <a href="loft-insulation.html">loft insulation</a>, insulating walls, <a href="draught-proofing.html">draught-proofing</a>, upgrading an old and inefficient heating system, improving hot-water and cylinder insulation, and switching to <a href="led-lighting.html">LED lighting</a> all tend to move the rating up. The certificate's own recommendation list is ranked roughly by impact, so it is a sensible place to start, and doing the cheap, high-value jobs first gets you the best return before any big spending.</p>
    <h2>The bottom line</h2>
    <p>An EPC rates your home's energy efficiency from A to G based on its fabric and systems, matters most when selling or letting and for meeting rental standards, and comes with a handy list of improvements. Just remember it is a model of the building, not a readout of your actual bills, which depend on how you live. Use it as a guide and a checklist, lean on the cheap fabric improvements first, and the rating and your bills tend to move up together.</p>
  </div></section>
''',
)

PAGES["home-working-energy-cost"] = dict(
    title="The energy cost of working from home",
    description="Working from home shifts energy use onto your own bill, mostly through daytime heating. What it adds, what it saves against the commute, and how to keep the cost down.",
    active="guides",
    blurb="Home working moves energy onto your bill, mostly daytime heating. What it adds and how to trim it.",
    pubdate="2026-06-16",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Working from home moved a chunk of energy use out of the office and onto your own bill, and while the gadgets get the blame, the real cost is somewhere less obvious. Knowing where it actually goes lets you keep the home-working bill modest rather than letting it creep up unnoticed.</p>
    <h2>What home working adds</h2>
    <p>By far the biggest addition is heating. An empty house on a workday used to coast along cool until you got home; now it needs to be warm all day while you are in it, and daytime heating in winter is the single largest extra cost of working from home. The electronics, by contrast, are minor: a laptop draws very little, and even a desktop with a couple of monitors is small next to the heating, as the <a href="standby-power-the-full-story.html">standby power</a> and device guides explain. Add a few cups of tea from the <a href="appliance-running-cost.html">kettle</a> and some extra lighting, and the device side stays modest.</p>
    <h2>What it costs</h2>
    <p>Because heating dominates, your home-working cost depends mostly on the weather and your house: high through a cold winter, almost nothing in summer. The electricity for your kit is a small, steady addition you can estimate by putting your computer and monitor wattage through the <a href="appliance-running-cost.html">running cost calculator</a> for the hours you work. Do that and you will see the heating is the thing worth managing, not the laptop.</p>
    <h2>How to cut it</h2>
    <p>The trick is to stop heating the whole house when you only occupy one room of it. Work in one room and heat that room rather than the entire home, turning down the <a href="radiator-valves-and-zoning.html">radiator valves</a> elsewhere and setting the main <a href="thermostat-settings.html">thermostat</a> to suit where you actually are. A small amount of targeted heat, or even a heated throw while you sit still at a desk, costs far less than warming every room you are not in. Layer up, keep the door shut, and let the rest of the house stay cool. Switch your kit and screens off at the end of the day rather than leaving them idling.</p>
    <h2>The commute trade-off</h2>
    <p>It is worth keeping the whole ledger in view. Working from home adds to your home energy bill, but it removes the cost and energy of commuting, which for many people is far larger than the extra heating, especially if the commute was by car. So while your household bill goes up, your total spending and energy use often go down once the fuel or fares you are no longer paying are counted. The home-working cost is real, but it is usually a transfer from a bigger expense rather than a brand-new one.</p>
    <h2>The bottom line</h2>
    <p>The energy cost of working from home is mostly daytime heating, not the computer, so the way to control it is to heat the room you work in rather than the whole house, using zoning, a lower thermostat and a bit of layering. Against that, you save the commute, which often more than covers the extra. Manage the heating sensibly and home working need not cost much at all.</p>
  </div></section>
''',
)

PAGES["storage-heaters-explained"] = dict(
    title="Storage heaters: getting the cheap heat right",
    description="How night storage heaters work, why they only pay off on an off-peak tariff, what the input and output dials actually do, how to set them through the week, the difference modern high-retention models make, and a worked example of what they cost to charge.",
    active="guides",
    blurb="Cheap, even heat if you run them right; expensive if you don't. How to set the dials and feed them the right tariff.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">Storage heaters divide opinion, and most of that comes down to how they are run rather than the heaters themselves. Feed them the right tariff and set the controls properly and they give cheap, even warmth right through a winter. Run them badly, which is very common, and you end up paying peak rates for heat that has all leaked away by the time the evening turns cold. This guide is about staying on the right side of that line.</p>

    <h2>How a storage heater works</h2>
    <p>Inside the case sits a stack of dense ceramic or clay bricks, wrapped in insulation, with electric heating elements buried among them. Overnight, when electricity is cheaper, the elements warm those bricks to a high temperature and the insulation holds the heat in. Through the following day the bricks release that warmth slowly into the room. Nothing burns, there is no flue, and the appliance is really a battery for heat rather than for fuel. That one idea, charge cheaply at night and discharge slowly through the day, drives everything about how a storage heater should be run and explains every way they go wrong.</p>

    <h2>Why they only pay off on a night tariff</h2>
    <p>The whole economic case rests on cheap overnight electricity. A storage heater charges during the off-peak window of a two-rate tariff such as Economy 7 or Economy 10, paying the low night unit rate for the energy it banks. Put the same heater on a single flat rate and it charges at full price, losing its entire reason to exist; at that point an ordinary panel or convector heater would warm the room on demand for the same money and waste nothing storing it. So the first question to ask of any storage heater is what tariff is feeding it. The mechanics of those off-peak deals are set out in the <a href="economy-7-and-night-rates.html">Economy 7 and night rates</a> guide, and because the meter has to be able to tell night from day, the <a href="smart-meters-explained.html">smart meters</a> guide is worth reading alongside it.</p>

    <h2>The two dials: input and output</h2>
    <p>Older storage heaters carry two controls, and most of the trouble traces back to muddling them up. Input, sometimes labelled charge, decides how much heat the bricks take on overnight; turn it up ahead of a cold snap and down again in milder weather. Output, sometimes labelled boost or room temperature, works a flap that lets the stored heat escape during the day. The classic error is leaving output wide open first thing in the morning, so the heater pours out its warmth by lunchtime and has nothing left for the cold evening when you actually want it. Keep output low or shut while the house is empty, then open it up once you are home. A useful way to hold the two apart in your head: input is how much you charge, output is how fast you spend it.</p>

    <h2>Setting them through the week</h2>
    <p>Storage heaters reward a bit of forward thinking, because they respond to last night's setting rather than this minute's. Watch the forecast and lift the input the evening before a cold day, then drop it back when a milder spell arrives, so you are not banking a full charge the bricks will never need. That lag is the awkward part: a sudden mild day after you charged for frost leaves you with surplus heat and no way to claw the money back, while an unexpected cold snap catches the bricks half full. Over a week the pattern tends to settle, with the heaters in the rooms you live in set higher and those in halls and spare rooms kept low. If your weekend at home looks different from your working week, adjust the input to match, since there is no point charging a study heater for a Saturday you will spend in the kitchen.</p>

    <h2>Old bricks versus modern retention models</h2>
    <p>Not all storage heaters are the same vintage. The old manual sort, with nothing but an input and an output dial, leak heat steadily whether you want it or not, which is why so many flats heated this way are too warm at breakfast and chilly by nine in the evening. Newer high heat retention models are better insulated, hold their charge for longer, and add a fan, a proper room thermostat and a programmer, so they release heat closer to when you ask for it rather than dribbling it away all day. If you are stuck with ancient units and the bills are high, replacing them with modern retention models can sharpen the control considerably, though the heat still costs the same per unit; the gain is in waste avoided, not in cheaper electricity.</p>

    <h2>What they cost to charge</h2>
    <p>A storage heater is rated by how much energy it can bank, often quoted in kilowatt-hours. Suppose a heater stores 6 kWh in a full overnight charge. At an example off-peak rate of 12p per kWh that is about 72p to fill it, whereas the same 6 kWh charged at an example daytime rate of 30p would cost 1.80, so the night rate is plainly doing the heavy lifting. You can put your own heaters through the <a href="appliance-running-cost.html">running cost calculator</a> by entering the heater's wattage and the number of hours it charges overnight. The figure to keep an eye on is any daytime boost: that top-up is drawn at the expensive peak rate, so a heater that has run dry and gets boosted every evening can quietly cancel out the saving the off-peak charge was supposed to deliver. A couple of well-set heaters that rarely need boosting will always beat a houseful of badly set ones leaning on the boost button.</p>

    <h2>When something else makes more sense</h2>
    <p>Storage heaters earn their keep in homes off the gas grid, in many flats, and anywhere a night tariff is already in place. If your home has mains gas, a gas central heating system is usually cheaper to run than electric storage heat, so the comparison is worth doing before you spend on replacement units. A <a href="heat-pumps-explained.html">heat pump</a> is another route for an all-electric home, turning each unit of electricity into several units of heat, though it is a far larger project. And if you rent and the storage heaters came with the flat, the realistic aim is to run the ones you have well rather than to replace them, which is covered in the <a href="saving-energy-when-renting.html">saving energy when renting</a> guide. Whatever the setup, the principle holds: these heaters only ever make sense paired with a cheap night rate, and they only ever feel good when the output is held back until you are there to enjoy it.</p>
  </div></section>
''',
)

PAGES["energy-labels-explained"] = dict(
    title="Energy labels: reading the rating before you buy",
    description="How to read the energy efficiency label on appliances: what the A to G scale means after the 2021 reset, why the annual kWh figure matters more than the letter, a worked example of how a pricier efficient model can be cheaper overall, and where the label can mislead.",
    active="guides",
    blurb="The letter grade is the least useful part. How to read the annual kWh figure and buy the model that's cheaper to run.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">The coloured label stuck to the front of a new fridge or washing machine is one of the few honest comparisons you get while shopping, yet most people glance at the letter and move on. The letter is the least useful part. Buried in the small print is a number that tells you, in kilowatt-hours, roughly what the thing will cost to run every year, and that number is what separates a cheap appliance from a cheap-to-own one.</p>

    <h2>What the label actually tells you</h2>
    <p>An energy label packs several facts into one card. The big coloured arrow gives the overall efficiency grade. Below it sit the figures that earned that grade: an annual or per-cycle energy use in kWh, and depending on the product a water use, a spin rating, a noise level in decibels and a capacity. The grade is a quick summary, but it is the kWh figure that you can turn into money. The same label format now runs across fridges and freezers, washing machines, dishwashers, tumble dryers, televisions and more, so once you can read one you can read them all.</p>

    <h2>The A to G scale and the 2021 reset</h2>
    <p>For years the scale crept upward until almost everything was rated A, then A+, then A++ and A+++, which made the grades close to meaningless because nearly every model clustered at the top. In 2021 the labels were reset to a plain A to G scale, and the bar was raised hard, so that at launch hardly anything reached A and a great many decent appliances landed at C, D or E. A modern E is not a bad appliance; it is simply being judged against a tougher, more spread-out yardstick than the old A+++ ever was. If you are comparing an older model carrying a plus-rated label with a newer one on the reset scale, the letters are not speaking the same language, which is another reason to drop down to the kWh figure and compare like with like.</p>

    <h2>The number that matters most</h2>
    <p>Find the kWh figure and you can stop guessing. For a fridge or freezer it is usually given as kWh per year, since the appliance runs continuously. For a washing machine, dishwasher or dryer it is often given per 100 cycles, because how much you use it is up to you, so you scale it to your own washing habits. Either way the sum is the same one the <a href="appliance-running-cost.html">running cost calculator</a> does: kWh multiplied by your price per unit gives the yearly cost. A fridge-freezer listed at 150 kWh a year, at an example 30p per kWh, costs about 45 a year to run; one listed at 300 kWh costs about 90. That 45 gap repeats every year for the decade or more the appliance lasts.</p>

    <h2>Why a pricier model can be the cheaper one</h2>
    <p>This is where the label changes a buying decision. Say two washing machines sit side by side, one 60 cheaper to buy but using noticeably more electricity and water per cycle. Run the efficient one through a few years of your actual washing and the running-cost difference can swallow that 60 saving and keep going. The cheaper sticker price is real, but it is a one-off, while the running cost lands every year you own the thing. For appliances that run constantly, like the fridge-freezer, or often, like the washing machine, the lifetime running cost usually dwarfs the small difference in purchase price, so the efficient model is frequently the cheaper choice once you count the whole bill rather than just the till receipt.</p>

    <h2>Reading the label for the big users</h2>
    <p>Spend the effort where the energy goes. A fridge-freezer never switches off, so its annual kWh figure is worth real attention, as the <a href="fridge-freezer-efficiency.html">fridge and freezer</a> guide sets out. A washing machine's energy use is dominated by heating water, so the per-cycle figure and the wash temperatures it offers both matter, and the <a href="washing-machine-running-cost.html">washing machine running cost</a> guide goes into the detail. Tumble dryers vary enormously, with heat-pump models using a fraction of the electricity of the old vented sort, a gap the label makes obvious; the <a href="tumble-dryer-cost.html">tumble dryer</a> guide explains why. For a kettle or a toaster the label barely matters, because the appliance runs for minutes a day and the running cost is trivial whichever you pick.</p>

    <h2>Where the label can mislead</h2>
    <p>Treat the figures as a fair comparison, not a promise. The annual kWh is measured under a standard test programme that may look nothing like how you use the machine: a washing machine's quoted figure usually assumes the eco setting, which runs longer and cooler than the quick wash most people reach for, so your real use can run higher. Capacity matters too, since a large efficient appliance can use more in total than a small inefficient one if you only ever half-fill it, and the grade rewards efficiency for the size rather than the absolute amount. The label is excellent for ranking similar models against each other; it is weaker as a forecast of your own bill, which is why pairing it with the running-cost sum for your own habits is the sensible move.</p>

    <h2>Using it alongside the running-cost sums</h2>
    <p>The label and the calculator work best together. The label hands you a tested, comparable kWh figure you would struggle to measure yourself, and the running-cost calculator turns that figure into pounds at your own tariff over the hours you actually use the thing. Look past the letter to the kWh, scale it to how you really live, and weigh the yearly running cost against the difference in sticker price. Do that for the appliances that run long and often and you will buy fewer regrets, because the cheap appliance and the cheap-to-run appliance are rarely the same one, and the label is how you tell them apart before the money has left your pocket.</p>
  </div></section>
''',
)

PAGES["time-of-use-tariffs-explained"] = dict(
    title="Time-of-use tariffs explained",
    description="What a time-of-use electricity tariff is, how static off-peak and dynamic half-hourly deals differ, what you need to take part, who saves and who loses, a worked example of load-shifting, and how to decide whether one suits your household.",
    active="guides",
    blurb="Cheaper electricity at the right hours, dearer at the wrong ones. Whether load-shifting pays depends entirely on your household.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A time-of-use tariff charges a different price for electricity depending on the hour of the day, rather than one flat rate around the clock. Move some of your heavier use into the cheaper hours and you pay less for the very same kilowatt-hours. Fail to move anything, or pile usage into the dear window by accident, and you can finish worse off than on a plain single rate. It is a tool that rewards households able to shift load and quietly penalises those that cannot.</p>

    <h2>How a flat rate hides the truth</h2>
    <p>A standard single-rate tariff charges the same pence per unit whenever you draw it, three on a weekday afternoon or three in the morning, no difference. That is simple, but it bears little relation to what is actually happening on the grid. Electricity is far cheaper to produce and deliver at some moments than others: overnight when demand collapses, or on a blustery afternoon when wind output is high and there is more power than the country needs. A flat rate blends all of that into one averaged number, so steady daytime users effectively subsidise the quiet hours and nobody has any reason to change when they use power. A time-of-use tariff pulls those hidden differences into the open and lets you act on them.</p>

    <h2>Not the same as Economy 7</h2>
    <p>Anyone who grew up with storage heaters will recognise the idea from Economy 7, which hands you roughly seven cheap night-time hours and a dearer day rate, usually paired with night storage heaters or an immersion. Modern time-of-use tariffs are descendants of that, but they reach further. Instead of a single fixed night block, they may carry several price bands across the day, or a price that changes every half hour to track the wholesale market. The <a href="economy-7-and-night-rates.html">Economy 7 guide</a> covers the classic two-rate version in detail; the rest of this article is about the newer, more flexible kind that a smart meter makes possible.</p>

    <h2>The two main shapes</h2>
    <p>Broadly there are two flavours. The first is a static off-peak tariff: a fixed cheap window, often a few hours overnight or sometimes a short cheap slot in the small hours, a standard rate for most of the day, and in some cases a raised peak band in the early evening. You know all the prices in advance and they never move, so planning around them is straightforward. The second is a dynamic, half-hourly tariff, where the price for each half-hour slot is published a day ahead and follows the wholesale cost. On a windy night that can drop to very little, occasionally to almost nothing; during a cold, still evening the same tariff can climb well above a flat rate for a couple of hours. One rewards a fixed routine, the other rewards paying attention or automating the response.</p>

    <h2>What you need to take part</h2>
    <p>The common requirement is a smart meter recording your use in half-hourly chunks, because the supplier has to know not just how much you used but exactly when. The <a href="smart-meters-explained.html">smart meters guide</a> covers how that recording works and the privacy questions around it. Most modern smart meters can run in this half-hourly mode, though some of the earliest ones need a settings change or, occasionally, swapping out. You need no special wiring for the tariff itself, but devices that can store the cheap energy change the maths entirely: storage heaters, a hot-water cylinder, an electric car or a home battery all turn cheap hours into something genuinely worth chasing rather than a minor convenience.</p>

    <h2>Who saves and who loses</h2>
    <p>The whole game is load-shifting, taking flexible and heavy uses and moving them into the cheap hours. The dishwasher and washing machine set on a delay timer, an electric car charging overnight (the <a href="best-time-to-charge-an-electric-car.html">charging times guide</a> goes into this), an immersion or storage heaters topping up off-peak, a home battery filling when power is cheap and discharging when it is dear. A household with one or more of those can save real money every week. A flat that draws electricity steadily through the day and evening, with nothing large to move and a busy teatime peak, may simply pay more than it would on a plain single rate. The tariff does nothing for you on its own; it only pays if your home can bend its demand around the prices.</p>

    <h2>A worked example</h2>
    <p>Suppose a household has 8 kWh of shiftable load a day: a wash, a dishwasher cycle and an electric-car top-up of a few miles. On a flat tariff at an example 28p per unit, that 8 kWh costs about 2.24 a day. On a time-of-use tariff with an example overnight rate of 10p, shifting all 8 kWh into the cheap window costs 80p, a saving of roughly 1.44 a day, or somewhere near 500 across a year if held to. Now picture the same household leaving everything running on a peak rate of, say, 40p because nothing got shifted: that 8 kWh would cost 3.20, more than the flat tariff would have charged. The numbers swing both ways, which is precisely the point of the design. Put your own usage and your tariff's actual bands through the <a href="appliance-running-cost.html">running cost calculator</a> to see which side of the line you fall on.</p>

    <h2>Mind the peak</h2>
    <p>The trap with these tariffs is the expensive window, typically late afternoon into the evening when the country comes home, switches everything on and starts cooking. On a static off-peak deal the peak band might be a fixed few hours at a raised rate; on a dynamic tariff a cold, still evening with little wind can push the half-hourly price sharply higher for an hour or two. A whole night of cheap savings can be wiped out by twenty careless minutes at peak time with the oven, kettle, tumble dryer and immersion all running together. The discipline is to keep big loads out of that window, and ideally to coast through it on a battery or simply do less, leaving the heavy jobs for later when the price has fallen back.</p>

    <h2>Automation does the heavy lifting</h2>
    <p>Organising your life around electricity prices sounds exhausting, and done by hand it can be. In practice most of the benefit comes from a handful of things that look after themselves. Appliance delay timers start the wash overnight without you waking up. A smart car charger or the car's own scheduler fills the battery in the cheap window automatically. A home battery and many heat pump and immersion controllers can be told to favour the off-peak hours and largely manage themselves after that, and a <a href="solar-battery-storage.html">solar battery</a> in particular can charge when power is cheap and carry the house through the evening peak. Set those once and the tariff works quietly in the background, which is the difference between a deal that pays and one that becomes a chore you abandon after a fortnight.</p>

    <h2>Deciding whether it suits you</h2>
    <p>Two questions settle it. First, do you have flexible heavy loads you can genuinely move: an electric car, storage heaters, a hot-water cylinder, a battery, or at least appliances you are happy to run overnight on a timer? Second, are you willing to shape your day a little around the prices, or to automate it so you never have to think? If both answers are yes, a time-of-use tariff can take a meaningful slice off the bill. If you have almost nothing to shift and no appetite for juggling, a straightforward single rate may serve you better and worry you less. Before switching, check that your meter supports half-hourly readings, compare a tariff's full set of rates rather than only the eye-catching cheap one, and be honest about how your household really uses power across the day.</p>
  </div></section>
''',
)

PAGES["dehumidifier-running-cost"] = dict(
    title="Dehumidifier running cost: what it really costs to run",
    description="What a dehumidifier draws, the difference between compressor and desiccant types, a worked example of a winter's running cost, using one to dry laundry instead of a tumble dryer, sizing and humidistat settings, and when a dehumidifier is the wrong fix for damp.",
    active="guides",
    blurb="A modest electricity user that can save money by replacing the tumble dryer. The real numbers, plus when it only masks the damp.",
    body='''
  <section class="section"><div class="wrap prose">
    <p class="lede">A dehumidifier pulls moisture out of the air, which helps with condensation, musty smells and drying washing indoors. By the standards of a kettle or an oven it is not a heavy electricity user, but because people tend to leave one running for hours at a stretch, the cost of that habit is worth understanding before you buy or before you let it hum away all winter. The good news is that the numbers are usually smaller than people fear, and in one common use it can actually save you money.</p>

    <h2>What a dehumidifier actually draws</h2>
    <p>Most domestic dehumidifiers pull somewhere between 150 and 700 watts while the compressor is working, a long way below a tumble dryer or an electric heater. The exact figure depends on the type, the capacity and how hard the unit is having to work. The important point is that a dehumidifier with a humidistat does not run flat out the whole time it is switched on: once the air reaches the target humidity the compressor cycles off, and the unit then draws only the small power its fan and electronics need until the air gets damp enough to trigger it again. So the plate rating is the most it will ever use, not the average across a day. A <a href="using-a-plug-in-energy-monitor.html">plug-in energy monitor</a> is the quickest way to see what yours really pulls over a typical run, and the reading is often lower than the label suggests.</p>

    <h2>Compressor versus desiccant</h2>
    <p>There are two common types and they behave quite differently on the meter. A compressor, or refrigerant, dehumidifier chills a cold surface so moisture condenses out of the air, working on much the same principle as the back of a fridge. These are the more efficient choice in a normal heated home and are what most people should buy. A desiccant dehumidifier instead uses a moisture-absorbing wheel and a built-in heater to drive the water back off, which means it draws more power for the same amount of water removed, often half as much again or more. In return it keeps working well in a cold space where a compressor model struggles, so an unheated garage, a chilly utility room or a caravan over winter is where the desiccant type earns its higher draw. In a warm living room the compressor type wins comfortably on cost.</p>

    <h2>What a session costs</h2>
    <p>Because the compressor cycles on and off, working out a day's cost means estimating how long it actually runs, not how long it sits switched on. Suppose a 300 watt compressor unit runs for, on average, half of an eight-hour stint, so four hours of real compressor time, or about 1.2 kWh. At an example 28p per unit that is roughly 34p for the day. Keep that up across a damp autumn and winter, say a hundred such days, and you are looking at somewhere around 34, plus a little for the fan time in between. A larger or harder-working unit in a very damp house could be two or three times that. Drop your own model's wattage and a realistic run time into the <a href="appliance-running-cost.html">running cost calculator</a> for a figure that matches your home rather than a guess.</p>

    <h2>Drying laundry with one</h2>
    <p>This is where a dehumidifier often pays for itself outright. Drying clothes on an airer in a closed room with a dehumidifier running typically uses far less electricity than a tumble dryer, which is one of the hungriest appliances in the house, as the <a href="tumble-dryer-cost.html">tumble dryer guide</a> sets out. The dehumidifier lifts the evaporated moisture straight out of the air so the washing dries in hours rather than days, without the windows streaming and without feeding mould on the walls. For anyone with no tumble dryer, or trying to wean themselves off one, it sits neatly between a cold flat draped in slowly drying laundry and an expensive dryer. The <a href="drying-clothes-without-a-tumble-dryer.html">drying without a tumble dryer guide</a> covers the wider set of options it fits into.</p>

    <h2>The damp and condensation angle</h2>
    <p>The reason most people buy a dehumidifier in the first place is not really to save energy but to deal with condensation, musty smells and black mould on cold walls and around window reveals. Damp air also feels colder than dry air at the same temperature, so it takes a little more heating to feel comfortable, which means drier air can sometimes let you nudge the thermostat down a touch for a small indirect saving. But running a dehumidifier is treating the symptom rather than the cause. If the moisture is coming from poor ventilation, from drying washing on radiators, or from cold bridging where a wall meets a window, the machine hides the problem rather than curing it. It earns its place as part of the answer, not as the whole of it.</p>

    <h2>Sizing and running it well</h2>
    <p>A unit is rated by how many litres it can pull from the air in a day, and a bigger capacity is not automatically better to live with. A right-sized unit reaches the target humidity and then idles quietly; an oversized one mostly just costs more to buy and runs hard when it does not need to. Set the humidistat to a sensible target, somewhere around 50 to 60 per cent relative humidity, rather than the lowest setting, which only makes it run far longer for steadily diminishing comfort. Close the door of the room you are treating or drying in so the machine is not fighting the moisture of the whole house at once. Empty the tank promptly, or fit a continuous drain hose, so it does not switch off and let the air re-dampen overnight. And keep the air filter clean, because a clogged filter makes the fan labour for less effect.</p>

    <h2>When a dehumidifier is the wrong tool</h2>
    <p>If your damp is rising damp, a plumbing leak or penetrating damp soaking through a wall, a dehumidifier does nothing about the cause and you end up paying to run it indefinitely. The same is true when condensation is really a ventilation problem in disguise: a kitchen or bathroom with no working extractor, trickle vents painted shut years ago, or a home sealed so tightly after enthusiastic <a href="draught-proofing.html">draught-proofing</a> that moist air simply has nowhere to escape. In those cases better ventilation, a proper repair, or warming up the cold surface is the real fix, and sometimes a cheaper one than running a machine forever. The dehumidifier is brilliant at managing moisture; it is no substitute for stopping it at the source.</p>

    <h2>The bottom line</h2>
    <p>A dehumidifier is a modest electricity user that can genuinely save money when it stands in for a tumble dryer, and that can make a damp home far more comfortable to live in. Pick a compressor model for normal heated rooms and reserve a desiccant for genuinely cold spaces, size it to the job, run it on a humidistat with the door shut, and it will cost a few tens of pounds across a winter rather than the hundreds people sometimes imagine. The one thing to stay clear-eyed about is whether you are curing the damp or only keeping it at bay, because that decides whether the running cost is a sensible expense or a bill with no end.</p>
  </div></section>
''',
)


GUIDES_ORDER = [
    # Scheduled additions (drip out by pubdate)
    "hot-tub-running-cost", "ground-vs-air-source-heat-pumps", "solar-water-heating",
    "ev-running-cost-vs-petrol", "energy-performance-certificate-explained", "home-working-energy-cost",
    # Heating and the building fabric
    "loft-insulation", "draught-proofing", "cavity-wall-insulation", "solid-wall-insulation",
    "underfloor-insulation", "is-double-glazing-worth-it", "secondary-glazing",
    "curtains-for-warmth", "radiator-reflectors",
    "thermostat-settings", "smart-thermostats", "radiator-valves-and-zoning",
    "how-to-bleed-radiators", "boiler-flow-temperature", "how-condensing-boilers-work",
    "heat-pumps-explained", "heat-pump-running-cost-vs-gas-boiler",
    "portable-heaters-running-cost", "electric-blanket-vs-heating",
    "storage-heaters-explained",
    # Hot water
    "hot-water-savings", "cylinder-jacket-and-pipe-lagging", "immersion-heater-cost",
    "low-flow-showerheads",
    # Electricity and appliances
    "led-lighting", "standby-power-the-full-story", "tumble-dryer-cost",
    "fridge-freezer-efficiency", "washing-at-30-degrees", "washing-machine-running-cost",
    "dishwasher-efficiency", "kettle-energy-saving", "electric-shower-cost",
    "air-fryer-running-cost", "oven-microwave-air-fryer-compared", "slow-cooker-economy",
    "induction-vs-gas-hob", "using-a-plug-in-energy-monitor",
    "television-and-entertainment-energy", "broadband-router-always-on",
    "drying-clothes-without-a-tumble-dryer", "dehumidifier-running-cost", "energy-labels-explained",
    # Bills, tariffs and meters
    "understanding-energy-bill", "switching-suppliers", "smart-meters-explained",
    "economy-7-and-night-rates", "time-of-use-tariffs-explained", "standing-charges-explained",
    # Solar and renewables
    "solar-panels-the-basics", "is-solar-worth-it", "solar-battery-storage",
    "solar-panels-hot-weather",
    # Fuel, driving and EVs
    "hypermiling", "keeping-your-car-cool-fuel-economy",
    "ev-charging-at-home-cost", "best-time-to-charge-an-electric-car",
    "electric-car-miles-per-kwh", "home-ev-charger-vs-3-pin-plug",
    "ev-charging-in-winter", "ev-range-in-hot-weather", "ev-cost-vs-petrol-per-year",
    # Seasonal
    "winter-energy-checklist", "keeping-cool-without-air-con",
    "air-conditioning-running-cost", "fan-running-cost", "portable-air-conditioner-vs-fan",
    "fridge-freezer-in-hot-weather",
    # Myths, renting and quick wins
    "energy-saving-myths", "saving-energy-when-renting", "quick-wins-under-a-tenner",
]


def _live(slug):
    """A page is live if it has no pubdate or its pubdate has arrived."""
    pd = PAGES[slug].get("pubdate")
    return pd is None or date.fromisoformat(pd) <= date.today()


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
''' + ("\n".join(_guide_tile(s) for s in GUIDES_ORDER if _live(s)) if any(_live(s) for s in GUIDES_ORDER) else
       '      <a class="tile" href="electricity.html"><h2>Start with electricity</h2><p>While the dedicated guides grow, the section pages are the place to begin.</p></a>') + '''
    </div>
  </div></section>
''',
)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for slug, p in PAGES.items():
        if not _live(slug):
            continue
        out = page(slug, p["title"], p["description"], p["body"], p.get("active"), p.get("pubdate"))
        open(os.path.join(here, f"{slug}.html"), "w", encoding="utf-8").write(out)
    today = date.today().isoformat()
    urls = []
    for slug in PAGES:
        if not _live(slug):
            continue
        loc = BASE + ("/" if slug == "index" else f"/{slug}.html")
        prio = "1.0" if slug == "index" else "0.7"
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>")
    open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(here, "robots.txt"), "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    open(os.path.join(here, INDEXNOW_KEY + ".txt"), "w", encoding="utf-8").write(INDEXNOW_KEY)
    _livecount = sum(1 for s in PAGES if _live(s))
    print("built", _livecount, "of", len(PAGES), "pages (rest scheduled ahead) + sitemap.xml + robots.txt + IndexNow key")


if __name__ == "__main__":
    main()
