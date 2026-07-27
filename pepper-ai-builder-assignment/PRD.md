# PRD — Atlas Auto-Reporter

**Author:** AI Builder candidate assignment · **Status:** Draft for review · **Owner surface:** Pepper Atlas

## 1. Problem

Every Customer Success manager at Pepper spends 4+ hours a week assembling recurring client
reports: pulling data out of GSC, GA4, Semrush, Semrush AI (GEO), and the client's CMS, stitching
it into a spreadsheet or deck, writing the narrative by hand, and emailing it out. The work is
mechanical (the data already lives in systems Atlas can reach), repetitive (same shape every
cycle), and low-leverage (it's assembly, not judgment) — yet it consumes the majority of a CS
manager's discretionary time and delays how quickly clients see wins or risks.

Competitor pressure confirms this is a solved-but-not-solved problem: agencies report spending
20–30 hours per client per month on reporting alone ([Whatagraph](https://whatagraph.com/agencies)),
and dedicated reporting platforms (AgencyAnalytics, Whatagraph, TapClicks) already claim to cut
that to single-digit hours with automated data pulls and, increasingly, AI-written narrative
sections (Whatagraph IQ, Semrush's 2025 AI summaries). Atlas's advantage is that it *already*
tracks the one category none of those generalist reporting tools do natively at the same depth:
AI search / GEO visibility (ChatGPT, Perplexity, Google AI Overviews, Copilot, Claude) via Semrush
AI Toolkit. A CS reporting product built inside Atlas can lead with that differentiator instead of
bolting AI visibility on as an afterthought — see the competitive landscape below for why that
matters and where the real white space is.

### Competitive landscape

The market splits into two camps, and neither one is building what this PRD proposes.

**AI-native GEO point solutions** — narrow, deep tools built for a brand or marketing team to
monitor and improve their own AI-search presence:
- [**Profound**](https://www.tryprofound.com/) — enterprise AEO platform; "Answer Engine Insights"
  tracks citation authority and sentiment across 10 answer engines, plus "Agents" that generate
  AI-optimized content and "Agent Analytics" for AI-crawler traffic.
- [**Scrunch AI**](https://scrunch.com/) — positions itself as the only AI-native platform pairing
  multi-LLM monitoring with auditing, optimization, *and* AI content delivery in one place, including
  hallucination detection and customer-journey mapping through AI conversations.
- [**Bluefish AI**](https://www.bluefishai.com/) — enterprise GEO plus conversational AI marketing
  agents that engage prospects directly; tracks positioning, accuracy, visibility, and favorability.
- [**Relixir**](https://relixir.ai/) — automated GEO content generation, claiming to move brands
  from 5th to 1st position in AI rankings within 30 days across 500+ customers.
- [**Peec AI**](https://peec.ai/) — GEO monitoring and competitive benchmarking, similar territory
  to Semrush AI Toolkit.
- **The Prompting Company** — early-stage GEO startup ([$6.5M raised, Oct 2025](https://techcrunch.com/2025/10/30/the-prompting-company-snags-6-5m-to-help-products-get-mentioned-in-chatgpt-and-other-ai-apps/)),
  narrowly focused on getting products mentioned in ChatGPT and similar apps.
- **Writesonic** — AI-visibility tracking across 10+ AI search platforms aimed at SMB/DTC brands,
  with the differentiator being direct-publish rewrites to Shopify/BigCommerce/WordPress product pages.
- **XFunnel** — was an independent AEO tool, **acquired by HubSpot in 2025** and folded into its
  suite — an early signal that GEO monitoring is consolidating into platforms that already own a
  recurring customer workflow, rather than surviving as a standalone product.

**Incumbent suites bolting AI-visibility onto an existing product** — the more direct warning sign
for Atlas, since it shows what happens when a company with an existing customer workflow adds this
capability:
- [**Adobe LLM Optimizer / Brand Visibility**](https://business.adobe.com/products/llm-optimizer.html) —
  Adobe acquired Semrush (completed April 2026) and layers Semrush's AI Optimization data (a
  289-million-prompt database) on top of LLM Optimizer, tracking ChatGPT, Google AI Mode, Copilot,
  and Perplexity inside Adobe's existing CX Enterprise suite.
- [**Sprinklr "LLM Insights"**](https://martech360.com/news/stack-platforms/guarding-the-voice-of-ai-sprinklr-launches-llm-insights-to-bridge-the-enterprise-visibility-gap/) —
  the first Voice-of-Customer platform to bring AEO into its existing enterprise stack, addressing
  LLMs defaulting to inaccurate/outdated brand narratives at buying moments.
- [**Meltwater AI Visibility** ("GenAI Lens")](https://www.meltwater.com/en/capabilities/ai-visibility) —
  PR/media-monitoring incumbent framing GEO as a *reputation* strategy, not just a search
  strategy; analyzes 8M+ citations/month across 8 LLMs.
- [**SimilarWeb GenAI Intelligence Toolkit**](https://aisearch.similarweb.com/ai-brand-visibility/) —
  web-analytics incumbent pairing AI Brand Visibility with *AI Traffic* — the one competitor here
  that ties visibility back to actual downstream site traffic, not just a mention.

**What this means for Atlas:** none of the above — point solution or bolted-on suite — targets the
specific workflow this PRD is about: a CS/agency team producing a *recurring client deliverable*.
They're all built for a brand's own marketing/comms team to monitor and act on their own AI
visibility, not for an agency stitching that signal into a report someone else is paying to
receive. The consolidation pattern (HubSpot → XFunnel, Adobe → Semrush) also validates the
underlying PRD bet: AI-visibility data is more valuable bundled into a platform that already owns
a recurring customer workflow than sold as a standalone monitoring dashboard — which is exactly
Atlas's position with Semrush AI Toolkit already in-house.

## 2. Goals / Non-goals

**Goals**
- Cut CS manager time-to-send for a recurring client report from ~4 hours to under 30 minutes.
- Produce a report a client would accept without the CS manager rewriting it from scratch.
- Keep a human in the loop before anything reaches a client — no silent auto-send by default.
- Make Atlas's AI-search-visibility data a first-class, headline section, not an appendix.

**Non-goals (this iteration)**
- Auth, billing, workspace/permission chrome — assumed to exist per the brief.
- Fully autonomous send with zero review (may become an opt-in later, see §9).
- Building new dashboards/BI — this is a report *document* product, not a metrics explorer.
- Real-time/streaming data — reports operate on period-over-period snapshots.

## 3. Users

| Persona | Role in this flow |
|---|---|
| **CS Manager** (primary) | Configures the client once, triggers/reviews each cycle's report, edits and sends |
| **Client stakeholder** (recipient) | Reads the finished report; may reply with questions Atlas doesn't handle (out of scope) |
| **CS Team Lead** (secondary) | Wants confidence reports go out on time and read consistently across the team |

## 4. User stories

1. As a CS manager, I connect a client's GSC property, GA4 property, Semrush domain, and CMS once,
   set a cadence (weekly/monthly) and the KPIs/competitors that matter to this client, and never
   redo that setup.
2. As a CS manager, when a reporting period closes, I see the client queued on a dashboard with a
   one-click "Generate report" action — I don't hunt for the data myself.
3. As a CS manager, I review an AI-drafted report where every claim is traceable to a source metric,
   edit anything that's off, regenerate a section I don't like, and add a personal note before sending.
4. As a CS manager, when the report flags a content gap, I get a **finished draft article** for it —
   title, meta, body, FAQ, internal links — not a note telling me to go write one. I review it and
   push it to the client's CMS, or hand it to the client's content team as-is.
5. As a CS manager, I approve and send in one action, and the system remembers what I sent for next
   cycle's continuity ("last time we recommended X — here's what happened").
6. As a client, I receive a report that reads like a person wrote it for me specifically, with the
   AI-search-visibility section giving me a metric I can't get from my own GA4 dashboard.

## 5. Functional requirements

### 5.1 Client report configuration — the CSM input page (one-time per client)

This is a real input surface, not a settings display. The CSM supplies the judgment the APIs
can't infer, and Atlas reuses it every cycle:

- **Brand** — the client's name as it should be matched in AI responses.
- **Industry / category** — defines the category the brand is benchmarked within, and therefore
  the prompt/keyword universe the Category view measures share against.
- **Key competitor brands** — a managed list (add/remove). These, not an algorithmic guess, drive
  the head-to-head Competitive view. The CSM knows who the client actually considers a rival,
  which is often not who ranks adjacent to them.
- **Priority prompts** — the questions the CSM believes matter, tracked across ChatGPT,
  Perplexity, Google AI Overviews, Copilot, and Claude.
- **Priority keywords** — weighted first in traditional-search reporting and pillar assembly.
- **CMS** — WordPress, Webflow, or Contentful; determines where content recommendations are
  routed and whether they can be pushed as drafts (see §5.6).
- **Cadence** — weekly or monthly, tied to each source's real data lag (GSC: 24–48h; GA4: near
  real-time) so the period boundary never includes unstable data.
- **Recipients** and a brand/template choice (logo, color) for the client-facing render.

### 5.1b The two analysis views

Both the CSM review screen and the client-facing deliverable present the analysis as two tabs.
Each tab spans the same four layers end-to-end — traditional search (GSC + Semrush) → AI search
(Semrush AI) → on-site conversion (GA4) — so the report answers "did visibility turn into
business result?", not just "what were the numbers per tool?". They differ in how they slice it:

**Tab 1 — Competitive position.** One row per CSM-named competitor brand: SERP visibility, average
position, keyword overlap, AI share of voice, AI visibility score, and which engine that
competitor is strongest on. Each row is badged lead/trail on both search and GEO, so the CSM can
see where the client is losing ground and on which surface.

**Tab 2 — Category performance.** A category-share header (share of voice, rank within the
category, prompts/keywords tracked, and the long tail of unnamed brands), then a per-topic-pillar
breakdown. Each pillar shows its search clicks and position, its Semrush position, its AI
visibility against the category average, and the GA4 sessions and conversions attributable to that
pillar's pages — with a winning/losing verdict versus the category average. Pillar AI visibility is
derived from the pillar's mention rate, so a topic with no AI mentions can never report a healthy
score.

### 5.2 Generation pipeline (triggered on schedule or on-demand)
1. **Fetch** — pull current period + prior period (for deltas) from every connected source.
   Endpoint mapping in §6.
2. **Aggregate** — roll raw rows into report-level metrics: totals, period-over-period deltas,
   top keyword movers, AI-visibility deltas per engine, content published/stale flags.
3. **Insight synthesis** — an LLM call receives the structured metrics JSON (never raw source
   payloads) plus the prior cycle's action items, and drafts: an executive summary (3–4
   sentences), section commentary, and recommended next actions. The prompt requires every
   number cited to trace back to a field in the input JSON — no invented figures. See
   `prototype/report_builder.py::NARRATIVE_PROMPT_TEMPLATE`.
4. **Assemble** — merge synthesis output with the data tables into the report document, with an
   inline source tag on every insight sentence (which endpoint it came from) so the CS manager
   (and, in an expanded surface, the client) can inspect provenance.

### 5.3 Review & edit
- Every generated sentence is inline-editable, tagged with its source, and has a "regenerate this
  section" control that re-runs step 3 for just that section.
- A free-text "note to client" field for context an API can't know (a call, a promised discount).
- Draft state persists — a CS manager can leave and come back before sending.

### 5.4 Send
- Approve & send delivers the report (rendered client-facing, sources/edit UI stripped) to the
  configured recipients and logs the send event, the review duration, and the edit diff size.
- Optional per-client "auto-approve if no material deltas" toggle for low-touch accounts — off by
  default (see Non-goals).

### 5.5 History & continuity
- Every sent report and its action items are stored so the next cycle's draft can reference
  resolved/unresolved items and avoid repeating a recommendation the client already acted on.

### 5.6 Drafted articles (CMS-routed)

Every pillar in the Category view resolves to a **finished draft article**, not a suggestion to
write one. A recommendation that says "publish a wide-fit sizing guide" still leaves the whole job
undone; the product's output is the draft itself, ready to review and publish. Drafts are split
into the two buckets a content team works from:

- **New content** — pillars with no owning page where the brand is absent or weak. Produces a new
  article drafted from scratch.
- **Existing content** — pillars that own a page which is stale or underperforming. Produces a
  rewrite, naming the target page and its last-modified date.

Each draft contains: title, slug, meta description, body sections with headings, an FAQ block
written against the tracked AI prompts, suggested internal links, and the schema types to emit.

**What's drafted versus what's computed.** The prose comes from an LLM drafting call
(`report_builder.DRAFT_PROMPT_TEMPLATE`), which receives the pillar's metrics, the competitor gap,
and the sources currently winning the citation. Everything around it is computed from live data
rather than authored: target keywords come from the pillar's own tracked queries, target prompts
from the CSM's priority list, internal links from other pillars' owned pages, and word count from
the drafted body. The drafting prompt explicitly forbids inventing product specifications —
it must leave a marked placeholder where a real measurement is needed, since a fabricated spec in
a published article is materially worse than a gap.

Drafts are sorted worst-gap-first (largest shortfall against the category average) and routed to
the client's configured CMS. WordPress exposes a documented write endpoint (`POST /wp/v2/posts`),
so those drafts can be pushed straight in as drafts. Webflow and Contentful are read-only in the
documented API set, so the draft is delivered for an editor to paste — the UI states which applies
rather than implying a write path that doesn't exist.

## 6. Data source → report section mapping

| Report section | Source · endpoint | Key fields used |
|---|---|---|
| Organic search performance | GSC `searchanalytics.query` | clicks, impressions, ctr, position, by query/page |
| Traffic & conversions | GA4 `properties.runReport` | sessions, conversions, totalRevenue, engagementRate |
| Keyword rankings & movers | Semrush `domain_organic` | Po, Pp, Pd, Nq, Tr, Tc |
| Domain authority | Semrush `backlinks_overview` | ascore, total, domains_num |
| Competitive position tracking | Semrush Position Tracking API | visibility, competitors[].position |
| AI search visibility (headline) | Semrush AI `ai_visibility_overview` | visibility_score, share_of_voice, per_engine[], sentiment, top_competing_brands[] |
| AI mention evidence / quotes | Semrush AI `ai_prompt_mentions` | prompt_text, response_excerpt, sentiment, citation_urls |
| Most AI-cited pages | Semrush AI `ai_citation_tracking` | url, page_title, citations_count, change_vs_previous |
| Competitive tab — search head-to-head | Semrush Position Tracking API (`competitors[]`) | visibility, avg position, keyword overlap, keywords tracked |
| Competitive tab — GEO head-to-head | Semrush AI `ai_visibility_overview.top_competing_brands[]` | share_of_voice, visibility_score, mention_rate, top_engine |
| Category tab — category share header | Semrush `domain_organic` + Semrush AI, rolled up to category | own share, rank, named-competitor shares, long tail |
| Category tab — per-pillar search | GSC `searchanalytics.query` + Semrush `domain_organic`, filtered to the pillar's queries | clicks, impressions, position, Po |
| Category tab — per-pillar GEO | Semrush AI `ai_visibility_overview` / `ai_prompt_mentions` per pillar | visibility_score, mentions, vs category average |
| Category tab — per-pillar conversion | GA4 `properties.runReport` with `landingPage` dimension, grouped by pillar | sessions, conversions, conversionRate, revenue |
| Content published this period | WordPress `GET /wp/v2/posts`, Webflow `GET /v2/collections/{id}/items/live`, or Contentful `GET /entries` — per the client's configured CMS | title, modified, link |
| Stale-content flags | Same CMS endpoint filtered by modification date (`modified_before` on WP) | title, modified, link |
| Drafted article push (WordPress only) | WordPress `POST /wp/v2/posts` | title, content, excerpt, slug, meta, status=draft |

Endpoints intentionally **not** used in v1: GSC `urlInspection`/`sitemaps`/`mobileFriendlyTest`
(per-URL technical diagnostics belong in an audit product, not a recurring performance report),
Semrush `phrase_organic`/`phrase_kdi` (SERP/keyword-research tools, not reporting), and Contentful
`tags` (taxonomy management, not measurement).

**A note on CMS write access.** Only WordPress exposes a documented write endpoint. Webflow's
listed endpoint is read-only (`items/live`), and Contentful's listed endpoints are Content Delivery
API reads. So content recommendations are *drafted into* WordPress but *briefed for* Webflow and
Contentful. The product states which applies per client rather than implying a write path that the
data layer can't honor. Closing that gap means adding the Webflow CMS write API and Contentful's
Content Management API — see §7.

## 7. What's missing from the documented data (and what we'd add)

The 7 sources cover performance data well but not the report *product* itself:

1. **Client goals/KPI config store** — nothing in the listed APIs holds "this client cares about
   conversions, not backlinks" or the competitor list. We'd add a first-party Atlas table
   (`client_report_config`) — this is product config, not a third-party pull.
2. **Delivery/email API** — none of the 7 sources can send anything. We'd add a transactional
   email provider (e.g., SendGrid, or Gmail API if send-as-the-CS-manager is desired) as a new
   integration purely for the "Approve & send" step.
3. **Prior-report / action-item store** — needed for continuity ("last cycle we recommended X").
   First-party Atlas table, not a third-party source.
4. **Brand/template asset store** — client logo, color, and email/PDF template for a white-labeled
   render. First-party asset storage, likely reusing whatever Atlas already has for client
   workspaces.
5. **PDF/branded-export renderer** — the report needs to leave Atlas as more than a link (some
   clients still forward a PDF to their own leadership). A rendering service (e.g., a headless
   Chromium export) sits downstream of the assembled report.
6. **Webflow CMS write API + Contentful Content Management API** — the documented endpoints for
   both are read-only, so content recommendations for those clients stop at a brief. Adding the
   write APIs would give Webflow and Contentful clients the same draft-into-CMS path WordPress
   already has, and is the single highest-leverage addition to the data layer for this product.
7. **Category/industry prompt-set definition** — the Category view benchmarks a brand against its
   category, which presumes a curated prompt and keyword universe per industry. Semrush AI supplies
   per-brand tracking but not "here is the canonical prompt set for outdoor gear." Atlas would
   maintain these as first-party category definitions, seeded from the CSM's industry selection and
   priority prompts, then expanded from observed competitor co-mentions.

None of these require a new *data* source category — they're config/storage/delivery plumbing
Atlas doesn't need Semrush or Google to provide.

## 8. Non-functional requirements

- **Latency**: generation (fetch → assemble) should complete in under 2 minutes so a CS manager
  can trigger it live on a client call if asked "can you show me this month's numbers now?"
- **Groundedness**: the synthesis prompt is constrained to the metrics JSON it's given: no source
  data, no invented number. Every claim carries a visible source tag in the review UI.
- **Idempotency**: re-generating a report for the same period must produce the same underlying
  metrics (deterministic aggregation); only the LLM narrative may vary, and only within the
  edit-before-send gate.
- **Auditability**: every send logs who approved it, what was edited vs. AI-drafted, and the
  source data snapshot used, for dispute resolution with a client.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| LLM invents or misstates a number | Synthesis prompt is fed only the pre-computed metrics JSON, not raw text; every sentence in review UI is tagged with its source field for spot-checking |
| CS manager rubber-stamps without reading | Track review duration and edit-diff size per send (feeds the eval in `eval-design.md`); flag near-zero-review sends to team leads for a spot audit, not a hard block |
| Client sees the same generic template every cycle and disengages | KPIs-of-record config + prior-action continuity keep the summary's lead metric client-specific each cycle |
| Report looks credible but a real anomaly (e.g., site outage causing a click cliff) is presented as a normal delta | Add an anomaly threshold flag (e.g., >30% single-metric swing) with a required manual annotation before send — logged as a follow-up |
| Over-automation erodes the CS relationship the client is paying for | Default posture is "draft for review," not "auto-send"; the note-to-client field keeps a human voice in every report |

## 10. Success metrics

Tied to the eval design in `eval-design.md`:
- **Primary**: median CS manager time from "period closes" to "report sent" drops from ~4h to <30 min.
- **Quality guardrail**: <20% of report text is edited before send, on average, after the first month.
- **Trust guardrail**: zero client-escalated factual errors in AI-drafted sections during pilot.
- **Adoption**: ≥80% of pilot CS managers use Atlas Auto-Reporter for the client's very next cycle
  (vs. reverting to manual).

## 11. Rollout

- **Phase 0 (this prototype)**: mock data, one sample client, human-in-the-loop review only.
- **Phase 1 (pilot)**: 3–5 CS managers, 10–15 clients with real source connections, manual send
  only, instrumented per §5.4/§10.
- **Phase 2 (GA)**: opt-in auto-approve for low-touch accounts, PDF export, action-item continuity
  across cycles.

## 12. Open questions

- Should clients ever see the source-tagged, editable view (self-serve), or is the clean rendered
  version the only client-facing artifact? (Assumed: latter, for now.)
- Where does the "note to client" text live for compliance/audit — same store as the report, or a
  separate CS notes system Atlas already has?
- Does GEO/AI-visibility data warrant its own standalone report product ahead of a client's
  broader SEO cadence, given it's Atlas's clearest competitive edge? Worth a follow-up spike.
