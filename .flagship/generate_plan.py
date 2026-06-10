#!/usr/bin/env python3
"""Generate the master topic + schedule plan for the year-long flagship queue.
Deterministic: authored topic list, season-aware Tue/Fri scheduling, dedup vs existing slugs.
Writes plan.json. No network, no deps."""
import json, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = date(2026, 6, 10)

# --- existing live slugs (dedup baseline + safe internal-link targets) ---
EXISTING = ("about air-conditioning-running-cost air-fryer-running-cost appliance-running-cost "
"best-time-to-charge-an-electric-car boiler-flow-temperature broadband-router-always-on "
"cavity-wall-insulation curtains-for-warmth cylinder-jacket-and-pipe-lagging dehumidifier-running-cost "
"dishwasher-efficiency draught-proofing driving drying-clothes-without-a-tumble-dryer "
"economy-7-and-night-rates electric-blanket-vs-heating electric-car-miles-per-kwh electricity "
"electric-shower-cost energy-labels-explained energy-performance-certificate-explained energy-saving-myths "
"ev-charging-at-home-cost ev-charging-in-winter ev-charging-no-driveway ev-cost-vs-petrol-per-year "
"ev-electricity-tariffs-explained ev-range-in-hot-weather ev-running-cost-vs-petrol fan-running-cost "
"fridge-freezer-efficiency fridge-freezer-in-hot-weather ground-vs-air-source-heat-pumps guides heating "
"heat-pump-running-cost-vs-gas-boiler heat-pumps-explained home-ev-charger-vs-3-pin-plug "
"home-vs-public-ev-charging-cost home-working-energy-cost hot-tub-running-cost hot-water-savings "
"how-condensing-boilers-work how-long-do-ev-batteries-last how-to-bleed-radiators hypermiling "
"immersion-heater-cost index induction-vs-gas-hob is-double-glazing-worth-it is-solar-worth-it "
"keeping-cool-without-air-con keeping-your-car-cool-fuel-economy kettle-energy-saving led-lighting "
"loft-insulation low-flow-showerheads oven-microwave-air-fryer-compared plug-in-hybrid-running-cost "
"portable-air-conditioner-vs-fan portable-heaters-running-cost privacy quick-wins-under-a-tenner "
"radiator-reflectors radiator-valves-and-zoning saving-energy-when-renting secondary-glazing "
"slow-cooker-economy smart-meters-explained smart-thermostats solar-battery-storage solar-panels-hot-weather "
"solar-panels-the-basics solar-water-heating solid-wall-insulation standby-power-the-full-story "
"standing-charges-explained storage-heaters-explained switching-suppliers television-and-entertainment-energy "
"thermostat-settings time-of-use-tariffs-explained tumble-dryer-cost underfloor-insulation "
"understanding-energy-bill using-a-plug-in-energy-monitor washing-at-30-degrees washing-machine-running-cost "
"winter-energy-checklist").split()

# --- 6 live today (no pubdate); link only into existing-live hubs ---
TODAY_PAGES = [
  ("is-it-cheaper-to-leave-heating-on-all-day", "Is it cheaper to leave the heating on all day?", "B"),
  ("what-temperature-should-i-set-my-thermostat", "What temperature should I set my thermostat?", "B"),
  ("cheaper-to-heat-one-room-or-whole-house", "Is it cheaper to heat one room or the whole house?", "B"),
  ("heated-clothes-airer-running-cost", "How much does it cost to run a heated clothes airer?", "A"),
  ("how-the-energy-price-cap-works", "How does the energy price cap work?", "C"),
  ("how-to-sleep-in-a-heatwave-without-air-con", "How to sleep in a heatwave without air conditioning", "I"),
]

# --- queued topics: (slug, title, cluster, season) ; season in {summer,autumn,winter,spring,any} ---
QUEUE = [
  # I cooling / summer
  ("summer-energy-checklist", "Summer energy-saving checklist: cutting bills in the warm months", "I", "summer"),
  ("cost-of-cooling-a-flat-in-summer", "How much does it cost to keep a flat cool in summer?", "I", "summer"),
  ("evaporative-coolers-uk", "Do evaporative coolers work in the UK?", "I", "summer"),
  ("ceiling-fan-running-cost-worth-it", "Ceiling fans: running cost and are they worth it?", "I", "summer"),
  ("can-a-heat-pump-cool-your-home", "Can a heat pump cool your home in summer?", "I", "summer"),
  ("air-purifier-running-cost", "How much does it cost to run an air purifier?", "A", "summer"),
  # C grants (autumn/winter-weighted)
  ("boiler-upgrade-scheme-explained", "The Boiler Upgrade Scheme explained: the heat pump grant", "C", "autumn"),
  ("eco4-scheme-explained", "The ECO4 scheme explained: free energy upgrades for eligible homes", "C", "autumn"),
  ("great-british-insulation-scheme-explained", "The Great British Insulation Scheme explained", "C", "autumn"),
  ("uk-solar-panel-grants", "Are there grants for solar panels in the UK?", "C", "autumn"),
  ("heat-pump-grants-and-cost", "Heat pump grants and costs in the UK explained", "C", "autumn"),
  ("warm-home-discount-explained", "The Warm Home Discount explained", "C", "autumn"),
  ("winter-fuel-payment-explained", "The Winter Fuel Payment explained", "C", "winter"),
  ("cold-weather-payment-explained", "The Cold Weather Payment explained", "C", "winter"),
  ("help-if-you-cant-afford-your-energy-bill", "Help if you cannot afford your energy bill", "C", "winter"),
  # A appliance running-cost (filler / any, a few winter)
  ("microwave-running-cost", "How much does it cost to run a microwave?", "A", "any"),
  ("toaster-running-cost", "How much does it cost to run a toaster?", "A", "any"),
  ("electric-oven-running-cost", "How much does it cost to run an electric oven?", "A", "any"),
  ("hair-dryer-running-cost", "How much does it cost to run a hair dryer?", "A", "any"),
  ("games-console-running-cost", "How much does it cost to run a games console?", "A", "any"),
  ("gaming-pc-running-cost", "How much does it cost to run a gaming PC?", "A", "any"),
  ("desktop-computer-running-cost", "How much does it cost to run a desktop computer?", "A", "any"),
  ("laptop-running-cost", "How much does it cost to run a laptop?", "A", "any"),
  ("boiling-water-tap-running-cost", "How much does a boiling water tap cost to run?", "A", "any"),
  ("coffee-machine-running-cost", "How much does it cost to run a coffee machine?", "A", "any"),
  ("vacuum-cleaner-running-cost", "How much does it cost to run a vacuum cleaner?", "A", "any"),
  ("pressure-washer-running-cost", "How much does it cost to run a pressure washer?", "A", "any"),
  ("extractor-fan-running-cost", "How much does it cost to run an extractor fan?", "A", "any"),
  ("cctv-running-cost", "How much does it cost to run home CCTV?", "A", "any"),
  ("mini-fridge-running-cost", "How much does it cost to run a mini fridge?", "A", "any"),
  ("chest-freezer-running-cost", "How much does it cost to run a chest freezer?", "A", "any"),
  ("cheapest-way-to-boil-water", "What is the cheapest way to boil water?", "A", "any"),
  ("dishwasher-eco-mode-explained", "Does dishwasher eco mode actually save money?", "A", "any"),
  ("washing-machine-cheapest-cycle", "Which washing machine cycle is cheapest to run?", "A", "any"),
  ("electric-radiator-running-cost", "How much does it cost to run an electric radiator?", "A", "winter"),
  ("electric-heater-types-compared", "Electric heater types compared: which is cheapest to run?", "A", "winter"),
  ("electric-towel-rail-running-cost", "How much does it cost to run an electric towel rail?", "A", "winter"),
  ("electric-blanket-running-cost", "How much does it cost to run an electric blanket?", "A", "winter"),
  ("electric-fire-running-cost", "How much does it cost to run an electric fire?", "A", "winter"),
  ("christmas-lights-running-cost", "How much does it cost to run Christmas lights?", "A", "winter"),
  ("heat-pump-tumble-dryer-worth-it", "Is a heat pump tumble dryer worth it?", "A", "winter"),
  ("electric-underfloor-heating-running-cost", "How much does electric underfloor heating cost to run?", "A", "winter"),
  # B heating behaviour (winter-weighted)
  ("cost-of-central-heating-per-hour", "How much does central heating cost per hour?", "B", "winter"),
  ("cost-to-heat-a-house-uk", "How much does it cost to heat a house in the UK?", "B", "winter"),
  ("radiators-off-in-unused-rooms", "Should you turn radiators off in unused rooms?", "B", "winter"),
  ("portable-heater-vs-central-heating-cost", "Is a portable heater cheaper than central heating?", "B", "winter"),
  ("gas-vs-electric-heating-cost", "Gas vs electric heating: which is cheaper?", "B", "winter"),
  ("balancing-radiators-guide", "How to balance your radiators for an even, cheaper heat", "B", "winter"),
  ("does-turning-thermostat-up-heat-faster", "Does turning the thermostat up heat a room faster?", "B", "winter"),
  ("best-temperature-for-each-room", "What temperature should each room be?", "B", "winter"),
  ("smart-thermostat-payback", "Do smart thermostats actually save money?", "B", "winter"),
  ("underfloor-heating-vs-radiators-cost", "Is underfloor heating cheaper to run than radiators?", "B", "winter"),
  # D tariffs / meters (any)
  ("fixed-vs-variable-energy-tariff", "Fixed or variable energy tariff: which is cheaper?", "D", "any"),
  ("how-to-read-your-energy-meter", "How to read your gas and electricity meter", "D", "any"),
  ("submitting-meter-readings", "Why submitting meter readings saves you money", "D", "any"),
  ("prepayment-vs-direct-debit-cost", "Prepayment meter vs direct debit: the cost difference", "D", "any"),
  ("dual-fuel-vs-separate-suppliers", "Dual fuel or separate suppliers: which is cheaper?", "D", "any"),
  ("what-is-a-kwh", "What is a kWh, and why it is on your energy bill", "D", "any"),
  ("when-your-fixed-energy-deal-ends", "What to do when your fixed energy deal ends", "D", "any"),
  ("is-it-worth-switching-energy-2026", "Is it worth switching energy supplier in 2026?", "D", "any"),
  ("using-your-in-home-display", "How to use your smart meter in-home display to save", "D", "any"),
  ("economy-10-explained", "Economy 10 explained, and how it differs from Economy 7", "D", "any"),
  ("why-did-my-direct-debit-go-up", "Why has my energy direct debit gone up?", "D", "any"),
  ("octopus-agile-tracker-tariffs-explained", "Agile and tracker tariffs explained", "D", "any"),
  # E battery / smart / future (spring)
  ("home-battery-without-solar-worth-it", "Is a home battery worth it without solar panels?", "E", "spring"),
  ("battery-arbitrage-cheap-night-tariff", "Can you save money charging a home battery on a cheap night rate?", "E", "spring"),
  ("vehicle-to-grid-explained", "Vehicle-to-grid explained: can your EV power your home?", "E", "spring"),
  ("infrared-heating-panels-running-cost", "Infrared heating panels: running cost and are they worth it?", "E", "spring"),
  ("heat-battery-explained", "Heat batteries explained: a hot water cylinder alternative?", "E", "spring"),
  ("solar-diverter-explained", "Solar power diverters explained: heating water with surplus solar", "E", "spring"),
  ("battery-storage-payback", "Home battery storage payback explained", "E", "spring"),
  ("solar-panel-cleaning-and-maintenance", "Solar panel cleaning and maintenance: cost and worth it?", "E", "spring"),
  # F insulation gaps (autumn-weighted)
  ("how-thick-should-loft-insulation-be", "How thick should loft insulation be?", "F", "autumn"),
  ("room-in-roof-insulation", "Room-in-roof insulation explained", "F", "autumn"),
  ("external-wall-insulation-cost", "External wall insulation: cost and is it worth it?", "F", "autumn"),
  ("suspended-timber-floor-insulation", "Insulating a suspended timber floor", "F", "autumn"),
  ("draughtproofing-a-front-door", "Draughtproofing a front door, letterbox and keyhole", "F", "winter"),
  ("pipe-lagging-and-frozen-pipes", "Pipe lagging and preventing frozen pipes", "F", "winter"),
  ("chimney-draught-excluder", "Stopping chimney draughts: balloons, sheep and covers", "F", "winter"),
  ("garage-door-insulation", "Garage door insulation: is it worth it?", "F", "winter"),
  ("insulating-a-conservatory", "How to make a conservatory cheaper to heat", "F", "winter"),
  # G damp / ventilation (winter)
  ("condensation-and-mould-cheap-fixes", "Condensation and mould: the cheap fixes", "G", "winter"),
  ("dehumidifier-vs-heating-to-dry-air", "Is a dehumidifier cheaper than heating to dry the air?", "G", "winter"),
  ("ventilation-without-losing-heat", "How to ventilate your home without losing heat", "G", "winter"),
  ("why-house-feels-cold-with-heating-on", "Why your house feels cold even with the heating on", "G", "winter"),
  ("piv-units-explained", "Positive input ventilation explained", "G", "winter"),
  # H seasonal / lifestyle
  ("autumn-heating-prep-checklist", "Autumn checklist: getting your heating ready for winter", "H", "autumn"),
  ("cheapest-way-to-dry-clothes", "What is the cheapest way to dry clothes?", "H", "winter"),
  ("heat-your-home-without-central-heating", "Heating your home without central heating", "H", "winter"),
  ("stay-warm-without-turning-up-heating", "How to stay warm without turning up the heating", "H", "winter"),
  ("energy-saving-in-a-shared-house", "Energy saving in a student or shared house", "H", "any"),
  ("energy-saving-in-a-flat", "Energy saving in a flat or apartment", "H", "any"),
  ("save-energy-in-the-kitchen", "How to save energy in the kitchen", "H", "any"),
  ("save-energy-in-the-bathroom", "How to save energy in the bathroom", "H", "any"),
  ("energy-saving-with-a-baby", "Energy saving with a new baby", "H", "any"),
  # J EV / driving extension (spring)
  ("public-ev-charging-cost-explained", "How much does public EV charging cost?", "J", "spring"),
  ("should-you-charge-your-ev-to-100", "Should you charge your EV to 100%?", "J", "spring"),
  ("ev-total-cost-of-ownership", "EV vs petrol: the five-year cost of ownership", "J", "spring"),
  ("how-to-pick-an-ev-tariff", "How to pick the right EV electricity tariff", "J", "spring"),
  ("work-out-your-ev-charging-cost", "How to work out your own EV charging cost", "J", "spring"),
  ("phev-vs-ev-vs-petrol-running-cost", "Plug-in hybrid vs full EV vs petrol: running cost compared", "J", "spring"),
  ("charging-your-ev-from-solar", "Charging your EV from solar panels", "J", "spring"),
  ("how-long-does-it-take-to-charge-an-ev", "How long does it take to charge an electric car?", "J", "spring"),
]

# --- dedup guard ---
existing_set = set(EXISTING)
all_new = [t[0] for t in TODAY_PAGES] + [t[0] for t in QUEUE]
assert len(all_new) == len(set(all_new)), "duplicate slug within new set"
collide = existing_set & set(all_new)
assert not collide, f"collision with existing slugs: {collide}"

# --- Tue/Fri slot list starting after TODAY ---
def slots(n):
    out, d = [], TODAY + timedelta(days=1)
    while len(out) < n:
        if d.weekday() in (1, 4):  # Tue=1, Fri=4
            out.append(d)
        d += timedelta(days=1)
    return out

def season_of(d):
    m = d.month
    if m in (6, 7, 8): return "summer"
    if m in (9, 10): return "autumn"
    if m in (11, 12, 1, 2): return "winter"
    return "spring"  # 3,4,5

dates = slots(len(QUEUE))
assigned = {}            # slot index -> topic
used = [False] * len(dates)

# place season-tagged topics into earliest matching-season free slot; filler later
seasoned = [t for t in QUEUE if t[3] != "any"]
filler   = [t for t in QUEUE if t[3] == "any"]

for t in seasoned:
    want = t[3]
    idx = next((i for i, dt in enumerate(dates) if not used[i] and season_of(dt) == want), None)
    if idx is None:  # season full: take nearest free slot to that season's centre
        idx = next(i for i in range(len(dates)) if not used[i])
    used[idx] = True
    assigned[idx] = t

for i in range(len(dates)):
    if not used[i] and filler:
        assigned[i] = filler.pop(0)
        used[i] = True
# any leftover filler (shouldn't happen) -> append
leftover = [i for i in range(len(dates)) if not used[i]]
for i, t in zip(leftover, filler):
    assigned[i] = t

queue_out = []
for i, dt in enumerate(dates):
    slug, title, cluster, season = assigned[i]
    queue_out.append({"slug": slug, "title": title, "cluster": cluster,
                      "season": season, "pubdate": dt.isoformat()})

plan = {
  "generated_for": TODAY.isoformat(),
  "cadence": "Tue+Fri, twice weekly",
  "today_pages": [{"slug": s, "title": t, "cluster": c} for (s, t, c) in TODAY_PAGES],
  "queue": queue_out,
  "existing_slugs": EXISTING,
  "counts": {"today": len(TODAY_PAGES), "queue": len(queue_out), "existing": len(EXISTING)},
}
os.makedirs(os.path.join(HERE, "articles"), exist_ok=True)
with open(os.path.join(HERE, "plan.json"), "w") as f:
    json.dump(plan, f, indent=2)

print(f"today={len(TODAY_PAGES)} queue={len(queue_out)} "
      f"first={queue_out[0]['pubdate']} last={queue_out[-1]['pubdate']}")
# season sanity
import collections
by = collections.Counter(season_of(date.fromisoformat(q['pubdate'])) for q in queue_out)
print("slots by season:", dict(by))
xmas = next((q for q in queue_out if q['slug']=='christmas-lights-running-cost'), None)
print("christmas-lights ->", xmas['pubdate'] if xmas else "n/a")
wfp = next((q for q in queue_out if q['slug']=='winter-fuel-payment-explained'), None)
print("winter-fuel-payment ->", wfp['pubdate'] if wfp else "n/a")
