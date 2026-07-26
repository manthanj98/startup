# Pepper AI Builder Assignment — Atlas Auto-Reporter

**The problem:** Pepper's CS managers spend 4+ hours/week manually stitching GSC, GA4, Semrush,
Semrush AI (GEO), and CMS data into client reports. This is a proposal + working prototype for an
Atlas-native feature that drafts that report automatically and puts a human in the loop before it
ships.

## What's in here

| Deliverable | File |
|---|---|
| **Product Requirements Doc** | [`PRD.md`](./PRD.md) — problem, users, functional spec, data mapping, gaps, risks, rollout |
| **Eval / experiment design** | [`eval-design.md`](./eval-design.md) — baseline, experiment, instrumentation, success criteria |
| **Working prototype** | [`prototype/`](./prototype) — runnable Python pipeline that produces a real report from mock (but realistic) source data |
| **UX flow** | [`ux-flow.html`](./ux-flow.html) — clickable 5-screen prototype: dashboard → configure → generate → review/edit → send |

## Running the prototype

```bash
cd prototype
python3 report_builder.py
```

This mocks the 7 documented data sources (`mock_sources.py`), fetches current + prior period data,
computes deltas and insights, and writes `sample_report_output.md` — a real, ready-to-review client
report for a sample client ("Northwind Outdoor Co."). It also prints the LLM prompt template used
for the narrative-synthesis step in production (see `NARRATIVE_PROMPT_TEMPLATE` in
`report_builder.py`); the shipped prototype uses a deterministic rule-based narrator instead of a
live LLM call so it runs with zero API keys, per the brief's "no real calls required."

## Design choices worth flagging

- **AI search visibility (GEO) is the headline section**, not an appendix — it's the one data
  category Atlas already tracks that generalist reporting tools (AgencyAnalytics, Whatagraph,
  TapClicks) don't, and is closer to what dedicated GEO tools like Peec AI / Profound do. See
  `PRD.md` §1 for the competitor research behind that call.
- **Human-in-the-loop by default.** Every insight sentence in the draft is source-tagged and
  editable; nothing sends without explicit approval. See `PRD.md` §9 for why (and the one opt-in
  auto-approve exception for low-touch accounts, deferred to Phase 2).
- **Two things aren't in the documented data and had to be added**: a client-goals/KPI config store
  and a delivery (email) API — neither is a "data source," both are product plumbing. Full list in
  `PRD.md` §7.
