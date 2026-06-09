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
- **EV cluster spokes completed (9 Jun 2026)** — all four queued spokes written long-form (~1,600 words each), live now and fully cross-linked into the hub (zero broken links), since the cluster has live impressions and a self-contained four-page set links cleanly with no 404s:
  - `electric-car-miles-per-kwh` — real efficiency by car class, what cuts it, how to measure, cost-per-mile table. Hub links to it from the cost-per-mile section.
  - `home-ev-charger-vs-3-pin-plug` — charge-speed table (granny cable ~8 mi/hr vs 7kW ~25-30), install cost ~£800-1,200, when the cable is enough, auto off-peak scheduling. Hub links from the charger-vs-plug section.
  - `ev-charging-in-winter` — 10-30% range loss, cabin heating not battery harm, slow cold rapid-charging, preconditioning while plugged in. Linked from best-time-to-charge.
  - `ev-cost-vs-petrol-per-year` — annual cost at 7,500/12,000 miles across off-peak/standard/public/petrol, tariff sensitivity. Linked from the hub's petrol-comparison section.
- **Summer cooling cost cluster (9 Jun 2026)** — three cost-focused cooling guides, all live and cross-linked, sitting alongside the existing behavioural `keeping-cool-without-air-con` (which now links to all three). Built ahead of the summer "how much does it cost to run X" search spike:
  - `air-conditioning-running-cost` — cooling-cost hub: portable vs fixed split, cost-per-hour/day table at 26p, venting-hose point, energy label, how to cut.
  - `fan-running-cost` — high-volume reassurance query; cost-by-fan-type table, a penny an hour, whole-night/whole-summer figures.
  - `portable-air-conditioner-vs-fan` — the direct "vs" query; cost gap, where an evaporative cooler sits, when each is worth it.
- **Heat pump vs gas boiler running cost (9 Jun 2026)** — `heat-pump-running-cost-vs-gas-boiler`, queue item 6 done. Cost-per-kWh-of-heat table (gas 90% on the real Ofgem cap rate 7.33p ≈ 8.1p; heat pump at SCOP 3/3.5/4 on 26.11p; heat-pump tariff at 15p ≈ 4.3p), the spark-gap explanation, tariff dependence. Linked from `heat-pumps-explained`. Gas rate pinned to the Ofgem cap for 1 Jul–30 Sep 2026 (gas 7.33p, elec 26.11p, gas standing charge 29.04p/day); at the real gas rate a good heat pump (SCOP 3.5+) edges *ahead* of gas even on a standard tariff, not just level.

- **Appliance cost cluster, first two deepened (9 Jun 2026)** — Part A deepens of two short-form pages into full flagship treatment (quick-answer box, real-figure table at 26.11p, FAQ schema), H1 shifted to the question form to match the query:
  - `tumble-dryer-cost` → "How much does it cost to run a tumble dryer?" — ~3 kWh/load ≈ 78p, ~£122/yr at 3 loads/wk; heat-pump dryer ~half. Cross-links drying-without-a-dryer, washing-machine, energy-labels.
  - `electric-shower-cost` → "How much does it cost to run an electric shower?" — 8.5–10.5 kW table × shower length; 8-min ≈ 30–40p; one person ~£120/yr, family of four ~£480. Gas-mixer vs bath comparison (gas heat ~8p, consistent with the heat-pump guide). Cross-links hot-water-savings, low-flow-showerheads.

### Queue (future-date about one a week)

Broader energy clusters (high-intent, evergreen):
5. **Immersion heater cost for a year** — finish the appliance cluster: deepen `immersion-heater-cost` with the same table + FAQ treatment (Economy 7 angle, cylinder size, vs gas).
6. **Is solar worth it in 2026?** — payback with current export rates and install costs, deepen `is-solar-worth-it`.
7. **Standing charges explained** — already strong; candidate for a Part A deepen with current price-cap standing-charge figures.

## Method checklist for each flagship

1. Identify the target query/cluster (GSC if available, else keyword intent).
2. Pull current real figures from primary sources; note the check date.
3. Write long-form with a quick-answer box, at least one real-figure table, and an FAQ block with FAQPage schema.
4. Internal-link into the relevant hub (EV, heating, solar, appliances) both ways.
5. `python3 build.py`; grep the output for em-dashes and broken internal links.
6. Commit, push, ping IndexNow with the changed URLs.
