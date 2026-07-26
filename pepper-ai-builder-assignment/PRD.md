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
tracks the one category none of those generalist tools do natively at the same depth: AI search /
GEO visibility (ChatGPT, Perplexity, Google AI Overviews, Copilot, Claude) via Semrush AI Toolkit —
the same territory as point solutions like [Peec AI](https://peec.ai/) and
[Profound](https://www.tryprofound.com/). A CS reporting product built inside Atlas can lead with
that differentiator instead of bolting AI visibility on as an afterthought.

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
4. As a CS manager, I approve and send in one action, and the system remembers what I sent for next
   cycle's continuity ("last time we recommended X — here's what happened").
5. As a client, I receive a report that reads like a person wrote it for me specifically, with the
   AI-search-visibility section giving me a metric I can't get from my own GA4 dashboard.

## 5. Functional requirements

### 5.1 Client report configuration (one-time per client)
- Connected sources: GSC site URL, GA4 property, Semrush domain + competitor domains, CMS
  (WordPress/Webflow/Contentful) connection.
- Cadence: weekly or monthly, tied to each source's real data lag (GSC: 24–48h; GA4: near
  real-time) so the period boundary never includes unstable data.
- KPIs of record: which metrics this specific client cares about (e.g., conversions vs. AI share
  of voice vs. backlink growth) — drives what leads the executive summary.
- Recipients and a brand/template choice (logo, color) for the client-facing render.

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
| Content published this period | WordPress `GET /wp/v2/posts` (or Webflow items/live, Contentful entries) | title, date, link |
| Stale-content flags | WordPress `GET /wp/v2/posts` with `modified_before` | title, modified, link |

Endpoints intentionally **not** used in v1: GSC `urlInspection`/`sitemaps`/`mobileFriendlyTest`
(per-URL technical diagnostics belong in an audit product, not a recurring performance report),
Semrush `phrase_organic`/`phrase_kdi` (SERP/keyword-research tools, not reporting), Contentful
`tags` and WordPress/Contentful write endpoints (no write path needed — this product only reads
and drafts, it doesn't publish content).

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
