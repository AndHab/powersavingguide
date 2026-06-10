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
  - `immersion-heater-cost` → "How much does it cost to run an immersion heater?" (deepened 9 Jun 2026) — full-reheat table by cylinder size (7/9/12 kWh) at standard 26p vs example Economy 7 night 13p; tankful ≈ £1.80–3.15; ~£600–850/yr as a main heater, ~half on E7; the gas-boiler-backup-left-on money-waster; timer + cylinder jacket. vs gas ~3× per unit (8p). Cross-links economy-7, cylinder-jacket, hot-water-savings. **Appliance cost cluster now complete (all three deepened).**

- **Standing charges deepen (9 Jun 2026)** — `standing-charges-explained` Part A: added quick-answer box, real-figure table and FAQ schema using the live Ofgem cap standing charges (elec 57.19p/day, gas 29.04p/day, combined ~86p/day ≈ £315/yr; 1 Jul–30 Sep 2026, GB direct-debit average). Replaced the old illustrative 60p/30p worked example with the real dated figures. Note: like the gas unit rate, these move each quarter, so re-check at the next cap.

- **Is solar worth it deepen (9 Jun 2026)** — `is-solar-worth-it` rebuilt + retitled "Is solar worth it in 2026?". Added quick-answer box, "what it costs and generates" section, a worked payback table (4 kW £7,500, 3,600 kWh, 26p import, 15p export, by self-consumption → ~9-12 yr), current SEG rates (5-15p flat, ~16p with import bundling, 30p+ peak with battery), and FAQ schema. Figures verified via web (FMB/Heatable install costs; SEG comparison sources, mid-2026). Also corrected the now-stale "self-use worth several times export" claim — true at 5p SEG (~5x), under 2x at 15p. Install cost ~£7-8.5k (0% VAT), generation 3,400-4,000 kWh/yr.

- **Summer hot-weather batch (10 Jun 2026)** — four new long-form guides on the "what does heat do" angle, all live and cross-linked, figures web-verified:
  - `ev-range-in-hot-weather` — heatwave cuts range ~10-25% (vs ~25-30%+ winter), from AC + battery cooling; the key insight a heat pump does NOT help in summer (cooling is the AC compressor, which every EV has; some heat-pump cars lose slightly more in heat); rapid-charge slowdown when pack is hot; heat ages the battery; pre-cool while plugged in. Reciprocal link from `ev-charging-in-winter`.
  - `keeping-your-car-cool-fuel-economy` — AC fuel penalty by vehicle (~4% petrol / 5% diesel / 6% hybrid), windows-vs-AC speed crossover (~40-50 mph), dump trapped heat first. Linked from `driving`; links to the EV-heat guide.
  - `solar-panels-hot-weather` — temperature coefficient ~0.3-0.4%/°C above 25°C; cells 50-65°C in sun ≈ 10-15% off peak; but summer still wins on long days; ideal = cold + bright. Reciprocal link from `solar-panels-the-basics`.
  - `fridge-freezer-in-hot-weather` — fridge sheds heat to the room, so a hot kitchen raises cost; siting (away from oven/sun, ventilation gaps), settings (3-5°C / -18°C), habits. Reciprocal link from `fridge-freezer-efficiency`.

- **Scheduled: Ofgem cap auto-refresh** — one-time remote routine `trig_01YEVe8hNDKvYazmYMt5xzQN` fires 28 Aug 2026 08:00 UTC (Opus 4.8) to look up the Oct-Dec 2026 cap and update every hard-coded figure (rewriting the heat-pump-vs-gas narrative if the conclusion shifts), build, verify, push, IndexNow. Makes no changes if figures aren't published yet. Manage: https://claude.ai/code/routines/trig_01YEVe8hNDKvYazmYMt5xzQN

### Queue (future-date about one a week)

The clearly-queued flagships are now all done (EV cluster, cooling cluster, heat-pump-vs-gas, appliance cost trio, standing charges, solar). **Next move: pull a fresh Google Search Console cluster** rather than work from a stale queue — find a page getting impressions but not clicks and deepen it (Part A), or write a new spoke around whatever query cluster is emerging. Candidate evergreen ideas if no GSC signal: smart-thermostat payback, induction-vs-gas running cost deepen, EV battery degradation/longevity, octopus-style time-of-use tariff explainer.

### Figures to re-check at the next Ofgem cap (Oct-Dec 2026, announced ~late Aug 2026)
Hard-coded current-cap numbers live in several pages and will need a refresh: unit rates **gas 7.33p, elec 26.11p** (heat-pump, shower, immersion guides) and standing charges **elec 57.19p/day, gas 29.04p/day** (standing-charges guide). Solar SEG/install figures also drift; re-check `is-solar-worth-it` periodically.

## Method checklist for each flagship

1. Identify the target query/cluster (GSC if available, else keyword intent).
2. Pull current real figures from primary sources; note the check date.
3. Write long-form with a quick-answer box, at least one real-figure table, and an FAQ block with FAQPage schema.
4. Internal-link into the relevant hub (EV, heating, solar, appliances) both ways.
5. `python3 build.py`; grep the output for em-dashes and broken internal links.
6. Commit, push, ping IndexNow with the changed URLs.
