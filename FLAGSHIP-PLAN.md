# Power Saving Guide — Flagship plan

Higher-tier, deeply-researched, human-checked long-form articles, distinct from the twice-weekly autopilot. Same idea as the Brussels Keto flagship system: the interactive session writes these, the autopilot does not. Aim roughly one per week, scheduled forward with `pubdate=`.

## Why this exists

The autopilot keeps the library growing. Flagships are where we win specific, high-intent search clusters with genuinely better pages than the competition: real current figures, clear worked examples, scannable tables, FAQ schema, and tight internal linking into a topic hub. These are the pages that earn featured snippets and "People also ask" slots.

## Rules

- **Real figures, checked and dated.** Every monetary figure (unit rates, price cap, pump prices, public-charging averages) must come from a current source, with the check date stated on the page. Anchors used so far: the Ofgem price cap (updates quarterly), Zapmap price index for public charging, the June 2026 pump-price average, and published EV-tariff off-peak rates (Intelligent Octopus Go, EDF GoElectric, British Gas EV). Re-check on each new flagship; the price cap moves every quarter.
- **No fabricated price league tables.** Naming suppliers with specific live prices in a ranked table is Andreas's affiliate/comparison layer, inserted by hand against a real comparison feed. Flagships give the method and worked examples with clearly-labelled representative rates, plus a table the reader applies to their own rate. Do not invent a "best tariff" league.
- **No fabricated product or brand reviews.** Same stance as the keto venue-review refusal.
- **No backdating.** New pages are dated honestly (today, or future-dated for the drip).
- **Long-form**, roughly 1,200 to 1,800 words. British English. Zero em-dashes (hyphen-as-pause is fine).
- **Build with `python3 build.py`** (dependency-free; unlike the keto Hugo site this one builds locally), check the rendered HTML for em-dashes and broken internal links, then commit and push. Netlify CD publishes from the push. Ping IndexNow for the new/changed URLs.
- **Drip, do not dump.** Future-date with `pubdate=` so guides release about one a week via the builder's `_live()` gate. Bring one live immediately only when it is linked from a page already getting impressions (so no link 404s).

## The two moves

- **Part A — deepen a high-impression / low-position page.** Pull the cluster from Google Search Console, find the page already getting impressions but not clicks, and rebuild it into the definitive answer: quick-answer box, real-figure tables, FAQ schema, internal links. This is the highest-ROI move when GSC shows a page ranking.
- **Part B — write a new flagship** from the queue below, future-dated, building out a topic hub so the cluster links together.

## Status

GSC (early June 2026) shows the site picking up UK impressions on the EV home-charging cost cluster ("how much does it cost to charge an electric car at home" and variants). First flagship work targets that cluster.

### Done

- **EV home charging cost hub** — `ev-charging-at-home-cost` rebuilt (Part A deepen, 9 Jun 2026): quick-answer box, full-charge cost table by battery size, cost-per-mile table vs petrol, FAQ schema, dated real figures (price cap 26.11p, off-peak 7-9p, Zapmap rapid 79p, petrol ~159p/l). This is the cluster hub.
- **Best time to charge an electric car** — `best-time-to-charge-an-electric-car` (new, live 9 Jun 2026): off-peak window, automatic scheduling, solar daytime, battery-health timing, winter preconditioning. Links to and from the hub.
- **EV vs petrol running cost** — `ev-running-cost-vs-petrol` brought live early (was scheduled 12 Jun) to support the hub link.

### Queue (future-date about one a week)

EV cluster (finish the hub's spokes first while it has impressions):
1. **How many miles per kWh do electric cars get?** — real efficiency by car class, what cuts it (cold, speed, load), how to measure your own. Feeds the cost-per-mile sums.
2. **Do you need a home EV charger? 3-pin vs 7kW wallbox** — charge speeds, install cost ballpark, when a granny cable is genuinely enough, off-peak scheduling.
3. **EV charging in winter** — range and efficiency loss, preconditioning, why cold rapid-charging is slower, real percentage hit.
4. **Cost to charge an EV vs the price of petrol over a year** — annual running-cost comparison at typical mileage, sensitivity to tariff.

Broader energy clusters (high-intent, evergreen):
5. **How much does it cost to run a [tumble dryer / electric shower / immersion heater] for a year** — deepen the existing appliance pages with the same table + FAQ-schema treatment, since these are classic "how much does it cost" queries.
6. **Heat pump running cost vs gas boiler** — the real per-unit comparison with COP, where it wins and where it does not.
7. **Is solar worth it in 2026?** — payback with current export rates and install costs, deepen `is-solar-worth-it`.
8. **Standing charges explained** — already strong; candidate for a Part A deepen with current price-cap standing-charge figures.

## Method checklist for each flagship

1. Identify the target query/cluster (GSC if available, else keyword intent).
2. Pull current real figures from primary sources; note the check date.
3. Write long-form with a quick-answer box, at least one real-figure table, and an FAQ block with FAQPage schema.
4. Internal-link into the relevant hub (EV, heating, solar, appliances) both ways.
5. `python3 build.py`; grep the output for em-dashes and broken internal links.
6. Commit, push, ping IndexNow with the changed URLs.
