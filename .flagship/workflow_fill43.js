export const meta = {
  name: 'psg-flagship-fill43',
  description: 'Write the 65 missing/faulty UK energy-saving flagship articles to .flagship/articles/*.json, with verification and one rewrite pass',
  phases: [
    { title: 'Write', detail: 'one writer per article, JSON file on disk is the deliverable' },
    { title: 'Verify', detail: 'dash/filler/figure/link/wordcount check, one rewrite on fail' },
  ],
}

const ART_DIR = '/home/andreas/git/powersavingguide/.flagship/articles'

const FIGURES = `CURRENT UK FIGURES (Ofgem price cap, 1 Jul to 30 Sep 2026 - use these unless you verify a newer one):
- Electricity unit rate: 26.11p per kWh
- Gas unit rate: 7.33p per kWh
- Standing charges: electricity 57.19p/day, gas 29.04p/day (GB direct-debit average)
- EV off-peak example: 7 to 9p/kWh (Intelligent Octopus Go ~5.5p); public rapid ~79p, public standard ~54p (Zapmap, mid 2026)
- Petrol ~159p/litre (mid 2026); 4kW solar ~£7,000 to £8,500 installed, 3,400 to 4,000 kWh/yr; SEG export 5 to 15p
Always state the rate and a check date under any cost table (e.g. "At 26.11p per kWh, Ofgem cap July to September 2026").`

const RULES = `HARD RULES:
- British English throughout.
- ZERO em-dashes and ZERO en-dashes anywhere. Use a hyphen with spaces as a pause, or rewrite the sentence. The characters U+2014 and U+2013 must never appear.
- No AI-filler vocabulary. Banned words/phrases: delve, dive in, navigate, landscape, realm, testament, tapestry, beacon, foster, unlock, unleash, elevate, embark, robust, seamless, leverage, harness (as verb), "it's worth noting", "in today's world", "when it comes to", "the bottom line is that", "in conclusion", "look no further", "game-changer", "supercharge", "boasts".
- Real, current figures only. Use the figures block; use WebSearch only when you need a specific current figure the block does not give you (grant amounts, scheme eligibility, a named tariff's current rate, a specific appliance wattage you are unsure of). Never invent figures.
- NO fabricated supplier price-league tables (no ranked "best tariff/best deal" tables naming suppliers with prices). Describe tariffs/schemes by type and give the method the reader applies to their own rate.
- NO fabricated product or brand reviews.
- For grant/policy topics: write evergreen ("how it works"), and include one sentence telling the reader to check the current rules and amounts on the official government/Ofgem page, since schemes change.`

const CLUSTER_HUBS = {
  A: ['appliance-running-cost', 'energy-labels-explained', 'standby-power-the-full-story'],
  B: ['heating', 'thermostat-settings', 'boiler-flow-temperature', 'heat-pumps-explained'],
  C: ['understanding-energy-bill', 'standing-charges-explained', 'heat-pumps-explained', 'loft-insulation'],
  D: ['understanding-energy-bill', 'switching-suppliers', 'smart-meters-explained', 'standing-charges-explained', 'economy-7-and-night-rates', 'time-of-use-tariffs-explained'],
  E: ['solar-panels-the-basics', 'solar-battery-storage', 'is-solar-worth-it'],
  F: ['loft-insulation', 'draught-proofing', 'cavity-wall-insulation', 'heating'],
  G: ['draught-proofing', 'heating', 'dehumidifier-running-cost'],
  H: ['winter-energy-checklist', 'quick-wins-under-a-tenner', 'energy-saving-myths', 'electricity', 'heating'],
  I: ['keeping-cool-without-air-con', 'fan-running-cost', 'air-conditioning-running-cost', 'portable-air-conditioner-vs-fan'],
  J: ['ev-charging-at-home-cost', 'ev-running-cost-vs-petrol', 'ev-electricity-tariffs-explained', 'best-time-to-charge-an-electric-car'],
}

const VERIFY = {
  type: 'object', additionalProperties: false,
  required: ['slug', 'pass', 'problems'],
  properties: {
    slug: { type: 'string' },
    pass: { type: 'boolean' },
    problems: { type: 'array', items: { type: 'string' } },
    words: { type: 'integer' },
  },
}

function writerPrompt(a, validSlugs, hubs, problems) {
  const fix = (problems && problems.length)
    ? `\nThis is a REWRITE. A previous draft failed verification for these reasons. Fix every one and rewrite the whole file (read the existing file first if it exists, keep what is good, fix what is listed):\n- ${problems.join('\n- ')}\n`
    : ''
  return `You are writing one deeply-researched, long-form UK energy-saving guide for powersavingguide.com.
${fix}
ARTICLE
- slug: ${a.slug}
- H1 / title (question form, use verbatim): ${a.title}
- cluster: ${a.cluster}
- primary hubs to link into (reciprocal, pick 2-3 that fit): ${hubs.join(', ')}

${FIGURES}

${RULES}

LENGTH & SHAPE: 1,300 to 1,800 words of genuinely useful prose. Structure:
- A lede (one strong opening paragraph, plain text).
- A "short answer" (2-4 sentences with the key number, plain text) - this becomes a quick-answer box.
- 4 to 6 sections, each a {h2 heading, html body}. At least ONE section must contain a real-figure table:
  <table class="ev-table"><thead><tr><th>...</th>...</tr></thead><tbody><tr><td>...</td>...</tr></tbody></table>
  followed by <p class="ev-note">At 26.11p per kWh, Ofgem cap July to September 2026.</p> (state the actual rate/source you used).
- A final "bottom line" style section.
- 3 to 5 FAQ items (question + plain-text answer), used for FAQPage schema.

INTERNAL LINKS: use only these valid slugs as link targets, as <a href="TARGET.html">natural anchor</a>. Link into 2-3 hub pages above and 1-2 sibling guides where genuinely relevant. Valid slugs:
${validSlugs.join(', ')}

HTML RULES for section html:
- Do NOT include the <h2> inside html (the h2 goes in its own field).
- Use <p>, <ul><li>, <h3>, <table class="ev-table">, <p class="ev-note">, <a href>. Nothing else.
- Write the pound sign as a literal £ (e.g. £122 a year). Do not include any <script> tag.
- No em/en dashes anywhere.

YOUR ONLY DELIVERABLE is the file. Write the article as JSON to exactly this path: ${ART_DIR}/${a.slug}.json
The JSON must have this shape:
{
  "slug": "${a.slug}",
  "title": "${a.title}",
  "description": "<140-160 char meta description, plain text>",
  "blurb": "<12-22 word guide-tile teaser, plain text>",
  "lede": "<opening paragraph, plain text>",
  "short_answer": "<2-4 sentence quick answer, plain text>",
  "sections": [ {"h2": "<heading>", "html": "<html body>"}, ... ],
  "faq": [ {"q": "<question>", "a": "<plain-text answer>"}, ... ]
}
Do your research first (WebSearch only if needed per the rules), then write the file. After the file is written, simply reply with the single line: DONE ${a.slug}
Make it the best page on the UK web for this query.`
}

function verifyPrompt(a, validSlugs) {
  return `Verify the article JSON at ${ART_DIR}/${a.slug}.json. Read it, then check ALL of:
1. No em-dash (U+2014) or en-dash (U+2013) anywhere in any field. (A plain hyphen "-" is fine.)
2. None of the banned AI-filler words appear: delve, dive in, navigate, landscape, realm, testament, tapestry, beacon, foster, unlock, unleash, elevate, embark, robust, seamless, leverage, "it's worth noting", "when it comes to", "in conclusion", "game-changer", boasts, supercharge.
3. Word count of lede + section html + short_answer is at least 1,200 words.
4. At least one section html contains <table class="ev-table"> AND an <p class="ev-note"> stating a rate.
5. At least 3 FAQ items, each with a non-empty plain-text answer.
6. Every internal link target (slug in any href="X.html") is in this valid set: ${validSlugs.join(', ')}
7. The file is valid JSON with all required fields (slug,title,description,blurb,lede,short_answer,sections,faq) and title matches "${a.title}".
8. Money is discussed with a literal £ and the rate/date is stated near any cost table.
Return {slug, pass (true only if ALL pass), problems (specific, actionable list, empty if pass), words}.`
}

// ---------------- run ----------------
const INPUT = {"work": [{"slug": "gas-vs-electric-heating-cost", "title": "Gas vs electric heating: which is cheaper?", "cluster": "B", "problems": []}, {"slug": "best-temperature-for-each-room", "title": "What temperature should each room be?", "cluster": "B", "problems": []}, {"slug": "draughtproofing-a-front-door", "title": "Draughtproofing a front door, letterbox and keyhole", "cluster": "F", "problems": []}, {"slug": "pipe-lagging-and-frozen-pipes", "title": "Pipe lagging and preventing frozen pipes", "cluster": "F", "problems": []}, {"slug": "chimney-draught-excluder", "title": "Stopping chimney draughts: balloons, sheep and covers", "cluster": "F", "problems": []}, {"slug": "garage-door-insulation", "title": "Garage door insulation: is it worth it?", "cluster": "F", "problems": []}, {"slug": "insulating-a-conservatory", "title": "How to make a conservatory cheaper to heat", "cluster": "F", "problems": []}, {"slug": "condensation-and-mould-cheap-fixes", "title": "Condensation and mould: the cheap fixes", "cluster": "G", "problems": []}, {"slug": "dehumidifier-vs-heating-to-dry-air", "title": "Is a dehumidifier cheaper than heating to dry the air?", "cluster": "G", "problems": []}, {"slug": "ventilation-without-losing-heat", "title": "How to ventilate your home without losing heat", "cluster": "G", "problems": []}, {"slug": "why-house-feels-cold-with-heating-on", "title": "Why your house feels cold even with the heating on", "cluster": "G", "problems": []}, {"slug": "piv-units-explained", "title": "Positive input ventilation explained", "cluster": "G", "problems": []}, {"slug": "cheapest-way-to-dry-clothes", "title": "What is the cheapest way to dry clothes?", "cluster": "H", "problems": []}, {"slug": "heat-your-home-without-central-heating", "title": "Heating your home without central heating", "cluster": "H", "problems": []}, {"slug": "stay-warm-without-turning-up-heating", "title": "How to stay warm without turning up the heating", "cluster": "H", "problems": []}, {"slug": "home-battery-without-solar-worth-it", "title": "Is a home battery worth it without solar panels?", "cluster": "E", "problems": []}, {"slug": "battery-arbitrage-cheap-night-tariff", "title": "Can you save money charging a home battery on a cheap night rate?", "cluster": "E", "problems": []}, {"slug": "vehicle-to-grid-explained", "title": "Vehicle-to-grid explained: can your EV power your home?", "cluster": "E", "problems": []}, {"slug": "infrared-heating-panels-running-cost", "title": "Infrared heating panels: running cost and are they worth it?", "cluster": "E", "problems": []}, {"slug": "heat-battery-explained", "title": "Heat batteries explained: a hot water cylinder alternative?", "cluster": "E", "problems": []}, {"slug": "solar-diverter-explained", "title": "Solar power diverters explained: heating water with surplus solar", "cluster": "E", "problems": []}, {"slug": "battery-storage-payback", "title": "Home battery storage payback explained", "cluster": "E", "problems": []}, {"slug": "solar-panel-cleaning-and-maintenance", "title": "Solar panel cleaning and maintenance: cost and worth it?", "cluster": "E", "problems": []}, {"slug": "public-ev-charging-cost-explained", "title": "How much does public EV charging cost?", "cluster": "J", "problems": []}, {"slug": "should-you-charge-your-ev-to-100", "title": "Should you charge your EV to 100%?", "cluster": "J", "problems": []}, {"slug": "ev-total-cost-of-ownership", "title": "EV vs petrol: the five-year cost of ownership", "cluster": "J", "problems": []}, {"slug": "how-to-pick-an-ev-tariff", "title": "How to pick the right EV electricity tariff", "cluster": "J", "problems": []}, {"slug": "work-out-your-ev-charging-cost", "title": "How to work out your own EV charging cost", "cluster": "J", "problems": []}, {"slug": "phev-vs-ev-vs-petrol-running-cost", "title": "Plug-in hybrid vs full EV vs petrol: running cost compared", "cluster": "J", "problems": []}, {"slug": "charging-your-ev-from-solar", "title": "Charging your EV from solar panels", "cluster": "J", "problems": []}, {"slug": "how-long-does-it-take-to-charge-an-ev", "title": "How long does it take to charge an electric car?", "cluster": "J", "problems": []}, {"slug": "what-is-a-kwh", "title": "What is a kWh, and why it is on your energy bill", "cluster": "D", "problems": []}, {"slug": "when-your-fixed-energy-deal-ends", "title": "What to do when your fixed energy deal ends", "cluster": "D", "problems": []}, {"slug": "is-it-worth-switching-energy-2026", "title": "Is it worth switching energy supplier in 2026?", "cluster": "D", "problems": []}, {"slug": "using-your-in-home-display", "title": "How to use your smart meter in-home display to save", "cluster": "D", "problems": []}, {"slug": "economy-10-explained", "title": "Economy 10 explained, and how it differs from Economy 7", "cluster": "D", "problems": []}, {"slug": "why-did-my-direct-debit-go-up", "title": "Why has my energy direct debit gone up?", "cluster": "D", "problems": []}, {"slug": "octopus-agile-tracker-tariffs-explained", "title": "Agile and tracker tariffs explained", "cluster": "D", "problems": []}, {"slug": "energy-saving-in-a-shared-house", "title": "Energy saving in a student or shared house", "cluster": "H", "problems": []}, {"slug": "energy-saving-in-a-flat", "title": "Energy saving in a flat or apartment", "cluster": "H", "problems": []}, {"slug": "save-energy-in-the-kitchen", "title": "How to save energy in the kitchen", "cluster": "H", "problems": []}, {"slug": "save-energy-in-the-bathroom", "title": "How to save energy in the bathroom", "cluster": "H", "problems": []}, {"slug": "energy-saving-with-a-baby", "title": "Energy saving with a new baby", "cluster": "H", "problems": []}], "valid_slugs": ["about", "air-conditioning-running-cost", "air-fryer-running-cost", "air-purifier-running-cost", "appliance-running-cost", "autumn-heating-prep-checklist", "balancing-radiators-guide", "battery-arbitrage-cheap-night-tariff", "battery-storage-payback", "best-temperature-for-each-room", "best-time-to-charge-an-electric-car", "boiler-flow-temperature", "boiler-upgrade-scheme-explained", "boiling-water-tap-running-cost", "broadband-router-always-on", "can-a-heat-pump-cool-your-home", "cavity-wall-insulation", "cctv-running-cost", "ceiling-fan-running-cost-worth-it", "charging-your-ev-from-solar", "cheaper-to-heat-one-room-or-whole-house", "cheapest-way-to-boil-water", "cheapest-way-to-dry-clothes", "chest-freezer-running-cost", "chimney-draught-excluder", "christmas-lights-running-cost", "coffee-machine-running-cost", "cold-weather-payment-explained", "condensation-and-mould-cheap-fixes", "cost-of-central-heating-per-hour", "cost-of-cooling-a-flat-in-summer", "cost-to-heat-a-house-uk", "curtains-for-warmth", "cylinder-jacket-and-pipe-lagging", "dehumidifier-running-cost", "dehumidifier-vs-heating-to-dry-air", "desktop-computer-running-cost", "dishwasher-eco-mode-explained", "dishwasher-efficiency", "does-turning-thermostat-up-heat-faster", "draught-proofing", "draughtproofing-a-front-door", "driving", "drying-clothes-without-a-tumble-dryer", "dual-fuel-vs-separate-suppliers", "eco4-scheme-explained", "economy-10-explained", "economy-7-and-night-rates", "electric-blanket-running-cost", "electric-blanket-vs-heating", "electric-car-miles-per-kwh", "electric-fire-running-cost", "electric-heater-types-compared", "electric-oven-running-cost", "electric-radiator-running-cost", "electric-shower-cost", "electric-towel-rail-running-cost", "electric-underfloor-heating-running-cost", "electricity", "energy-labels-explained", "energy-performance-certificate-explained", "energy-saving-in-a-flat", "energy-saving-in-a-shared-house", "energy-saving-myths", "energy-saving-with-a-baby", "ev-charging-at-home-cost", "ev-charging-in-winter", "ev-charging-no-driveway", "ev-cost-vs-petrol-per-year", "ev-electricity-tariffs-explained", "ev-range-in-hot-weather", "ev-running-cost-vs-petrol", "ev-total-cost-of-ownership", "evaporative-coolers-uk", "external-wall-insulation-cost", "extractor-fan-running-cost", "fan-running-cost", "fixed-vs-variable-energy-tariff", "fridge-freezer-efficiency", "fridge-freezer-in-hot-weather", "games-console-running-cost", "gaming-pc-running-cost", "garage-door-insulation", "gas-vs-electric-heating-cost", "great-british-insulation-scheme-explained", "ground-vs-air-source-heat-pumps", "guides", "hair-dryer-running-cost", "heat-battery-explained", "heat-pump-grants-and-cost", "heat-pump-running-cost-vs-gas-boiler", "heat-pump-tumble-dryer-worth-it", "heat-pumps-explained", "heat-your-home-without-central-heating", "heated-clothes-airer-running-cost", "heating", "help-if-you-cant-afford-your-energy-bill", "home-battery-without-solar-worth-it", "home-ev-charger-vs-3-pin-plug", "home-vs-public-ev-charging-cost", "home-working-energy-cost", "hot-tub-running-cost", "hot-water-savings", "how-condensing-boilers-work", "how-long-do-ev-batteries-last", "how-long-does-it-take-to-charge-an-ev", "how-the-energy-price-cap-works", "how-thick-should-loft-insulation-be", "how-to-bleed-radiators", "how-to-pick-an-ev-tariff", "how-to-read-your-energy-meter", "how-to-sleep-in-a-heatwave-without-air-con", "hypermiling", "immersion-heater-cost", "index", "induction-vs-gas-hob", "infrared-heating-panels-running-cost", "insulating-a-conservatory", "is-double-glazing-worth-it", "is-it-cheaper-to-leave-heating-on-all-day", "is-it-worth-switching-energy-2026", "is-solar-worth-it", "keeping-cool-without-air-con", "keeping-your-car-cool-fuel-economy", "kettle-energy-saving", "laptop-running-cost", "led-lighting", "loft-insulation", "low-flow-showerheads", "microwave-running-cost", "mini-fridge-running-cost", "octopus-agile-tracker-tariffs-explained", "oven-microwave-air-fryer-compared", "phev-vs-ev-vs-petrol-running-cost", "pipe-lagging-and-frozen-pipes", "piv-units-explained", "plug-in-hybrid-running-cost", "portable-air-conditioner-vs-fan", "portable-heater-vs-central-heating-cost", "portable-heaters-running-cost", "prepayment-vs-direct-debit-cost", "pressure-washer-running-cost", "privacy", "public-ev-charging-cost-explained", "quick-wins-under-a-tenner", "radiator-reflectors", "radiator-valves-and-zoning", "radiators-off-in-unused-rooms", "room-in-roof-insulation", "save-energy-in-the-bathroom", "save-energy-in-the-kitchen", "saving-energy-when-renting", "secondary-glazing", "should-you-charge-your-ev-to-100", "slow-cooker-economy", "smart-meters-explained", "smart-thermostat-payback", "smart-thermostats", "solar-battery-storage", "solar-diverter-explained", "solar-panel-cleaning-and-maintenance", "solar-panels-hot-weather", "solar-panels-the-basics", "solar-water-heating", "solid-wall-insulation", "standby-power-the-full-story", "standing-charges-explained", "stay-warm-without-turning-up-heating", "storage-heaters-explained", "submitting-meter-readings", "summer-energy-checklist", "suspended-timber-floor-insulation", "switching-suppliers", "television-and-entertainment-energy", "thermostat-settings", "time-of-use-tariffs-explained", "toaster-running-cost", "tumble-dryer-cost", "uk-solar-panel-grants", "underfloor-heating-vs-radiators-cost", "underfloor-insulation", "understanding-energy-bill", "using-a-plug-in-energy-monitor", "using-your-in-home-display", "vacuum-cleaner-running-cost", "vehicle-to-grid-explained", "ventilation-without-losing-heat", "warm-home-discount-explained", "washing-at-30-degrees", "washing-machine-cheapest-cycle", "washing-machine-running-cost", "what-is-a-kwh", "what-temperature-should-i-set-my-thermostat", "when-your-fixed-energy-deal-ends", "why-did-my-direct-debit-go-up", "why-house-feels-cold-with-heating-on", "winter-energy-checklist", "winter-fuel-payment-explained", "work-out-your-ev-charging-cost"]}
const work = INPUT.work
const validSlugs = INPUT.valid_slugs
log(`Filling ${work.length} articles (${work.filter(a => a.problems.length).length} rewrites of faulty drafts)`)

const results = await pipeline(
  work,
  // stage 1: write (no schema - the file on disk is the deliverable)
  (a) => agent(writerPrompt(a, validSlugs, CLUSTER_HUBS[a.cluster] || [], a.problems), {
    label: `write:${a.slug}`, phase: 'Write',
  }),
  // stage 2: verify, one rewrite on failure
  async (prev, a) => {
    let v = await agent(verifyPrompt(a, validSlugs), { label: `verify:${a.slug}`, phase: 'Verify', schema: VERIFY, model: 'sonnet' })
    if (v && !v.pass) {
      log(`rewrite ${a.slug}: ${v.problems.slice(0, 3).join('; ')}`)
      await agent(writerPrompt(a, validSlugs, CLUSTER_HUBS[a.cluster] || [], v.problems), {
        label: `rewrite:${a.slug}`, phase: 'Write',
      })
      v = await agent(verifyPrompt(a, validSlugs), { label: `reverify:${a.slug}`, phase: 'Verify', schema: VERIFY, model: 'sonnet' })
    }
    if (!v) return { slug: a.slug, pass: false, problems: ['verify agent returned null'] }
    return { slug: a.slug, pass: v.pass, problems: v.problems, words: v.words }
  }
)

const done = results.filter(Boolean)
const passed = done.filter(r => r.pass)
const failed = done.filter(r => !r.pass)
log(`DONE: ${passed.length}/${work.length} passed, ${failed.length} still failing`)
return {
  total: work.length,
  passed: passed.length,
  failed: failed.map(f => ({ slug: f.slug, problems: f.problems })),
}