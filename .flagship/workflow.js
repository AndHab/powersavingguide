export const meta = {
  name: 'psg-flagship-year',
  description: 'Write 109 long-form UK energy-saving flagships to .flagship/articles/*.json (research, verify, one rewrite pass)',
  phases: [
    { title: 'Manifest', detail: 'read plan.json' },
    { title: 'Write', detail: 'one writer per article, structured JSON to disk' },
    { title: 'Verify', detail: 'dash/filler/figure/link/wordcount check, one rewrite on fail' },
  ],
}

const ART_DIR = '/home/andreas/git/powersavingguide/.flagship/articles'
const PLAN = '/home/andreas/git/powersavingguide/.flagship/plan.json'

// ---- shared constraints injected into every writer ----
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

const WRITER_STATUS = {
  type: 'object', additionalProperties: false,
  required: ['slug', 'ok', 'words', 'internal_links'],
  properties: {
    slug: { type: 'string' },
    ok: { type: 'boolean' },
    words: { type: 'integer' },
    internal_links: { type: 'array', items: { type: 'string' } },
    used_websearch: { type: 'boolean' },
    note: { type: 'string' },
  },
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
const MANIFEST = {
  type: 'object', additionalProperties: false,
  required: ['articles', 'valid_slugs'],
  properties: {
    valid_slugs: { type: 'array', items: { type: 'string' } },
    articles: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['slug', 'title', 'cluster', 'pubdate', 'live_today'],
        properties: {
          slug: { type: 'string' }, title: { type: 'string' }, cluster: { type: 'string' },
          pubdate: { type: 'string' }, live_today: { type: 'boolean' },
        },
      },
    },
  },
}

function writerPrompt(a, validSlugs, hubs, problems) {
  const fix = problems
    ? `\nThis is a REWRITE. A previous draft failed verification for these reasons. Fix every one and rewrite the whole file:\n- ${problems.join('\n- ')}\n`
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

LENGTH & SHAPE: 1,200 to 1,800 words of genuinely useful prose. Structure:
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

OUTPUT: First, Write the article as JSON to exactly this path: ${ART_DIR}/${a.slug}.json
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
After writing the file, return the status object (slug, ok=true, words=<approx word count of the article>, internal_links=<list of slugs you linked to>, used_websearch).
Do your research first (WebSearch only if needed per the rules), then write. Make it the best page on the UK web for this query.`
}

function verifyPrompt(a, validSlugs) {
  return `Verify the article JSON at ${ART_DIR}/${a.slug}.json. Read it, then check ALL of:
1. No em-dash (U+2014) or en-dash (U+2013) anywhere in any field. (A plain hyphen "-" is fine.)
2. None of the banned AI-filler words appear: delve, dive in, navigate, landscape, realm, testament, tapestry, beacon, foster, unlock, unleash, elevate, embark, robust, seamless, leverage, "it's worth noting", "when it comes to", "in conclusion", "game-changer", boasts, supercharge.
3. Word count of lede + section html + short_answer is at least 1,100 words.
4. At least one section html contains <table class="ev-table"> AND an <p class="ev-note"> stating a rate.
5. At least 3 FAQ items, each with a non-empty plain-text answer.
6. Every internal link target (slug in any href="X.html") is in this valid set: ${validSlugs.join(', ')}
7. The file is valid JSON with all required fields (slug,title,description,blurb,lede,short_answer,sections,faq) and title matches "${a.title}".
8. Money is discussed with a literal £ and the rate/date is stated near any cost table.
Return {slug, pass (true only if ALL pass), problems (specific, actionable list, empty if pass), words}.`
}

// ---------------- run ----------------
phase('Manifest')
const manifest = await agent(
  `Read ${PLAN}. Return: (1) valid_slugs = the union of existing_slugs plus every slug in today_pages and queue. (2) articles = today_pages (live_today=true, pubdate="") followed by every queue entry (live_today=false, pubdate=its date), each as {slug,title,cluster,pubdate,live_today}. Preserve order: today_pages first, then queue in file order.`,
  { schema: MANIFEST, label: 'manifest', phase: 'Manifest', model: 'sonnet' }
)

const articles = manifest.articles
const validSlugs = manifest.valid_slugs
log(`Manifest: ${articles.length} articles, ${validSlugs.length} valid link targets`)

const results = await pipeline(
  articles,
  // stage 1: write
  (a) => agent(writerPrompt(a, validSlugs, CLUSTER_HUBS[a.cluster] || []), {
    label: `write:${a.slug}`, phase: 'Write', schema: WRITER_STATUS,
  }).then(s => ({ a, write: s })),
  // stage 2: verify, one rewrite on failure
  async (prev, a) => {
    if (!prev) return { slug: a.slug, pass: false, problems: ['write stage returned null'] }
    let v = await agent(verifyPrompt(a, validSlugs), { label: `verify:${a.slug}`, phase: 'Verify', schema: VERIFY, model: 'sonnet' })
    if (!v.pass) {
      log(`rewrite ${a.slug}: ${v.problems.slice(0, 3).join('; ')}`)
      await agent(writerPrompt(a, validSlugs, CLUSTER_HUBS[a.cluster] || [], v.problems), {
        label: `rewrite:${a.slug}`, phase: 'Write', schema: WRITER_STATUS,
      })
      v = await agent(verifyPrompt(a, validSlugs), { label: `reverify:${a.slug}`, phase: 'Verify', schema: VERIFY, model: 'sonnet' })
    }
    return { slug: a.slug, pass: v.pass, problems: v.problems, words: v.words, live_today: a.live_today }
  }
)

const done = results.filter(Boolean)
const passed = done.filter(r => r.pass)
const failed = done.filter(r => !r.pass)
log(`DONE: ${passed.length}/${articles.length} passed, ${failed.length} still failing`)
return {
  total: articles.length,
  passed: passed.length,
  failed: failed.map(f => ({ slug: f.slug, problems: f.problems })),
}
