# Eval & Experiment Design — Atlas Auto-Reporter

Goal: know, with evidence, whether Atlas Auto-Reporter actually recovers the 4+ hours/week the
brief cites, without quietly degrading report quality or the client relationship.

## 1. What we're measuring

Three questions, not one:
1. **Time**: does time-to-send actually drop?
2. **Quality**: is the AI-drafted output good enough that CS managers ship it with light edits,
   not a rewrite?
2b. **Trust**: does it introduce errors or a tone clients notice?

A time win that comes from CS managers rubber-stamping unread drafts isn't a win — it's a
liability that shows up later as a client-facing mistake. So time and quality/trust are measured
together, not as a single metric.

## 2. Baseline measurement (before shipping anything)

We don't have reliable baseline numbers today — "4+ hours" is a stated estimate, not instrumented
data. Before/instead of trusting it at face value:

- **Time-diary study**: for 2 full reporting cycles (covering both weekly- and monthly-cadence
  clients), CS managers log start/stop timestamps for each discrete reporting task (pull GSC data,
  pull GA4, pull Semrush, build deck/sheet, write narrative, send) via a lightweight form or a
  simple Chrome extension timer. Target ≥15 CS managers × ≥2 clients each = 30+ report-cycles of
  baseline data — enough to get a believable median and spread, not just a handful of anecdotes.
- Output: a distribution (not just a mean) of manual time-to-send per report, segmented by client
  complexity (number of sources connected, report length) — the 4-hour figure is very likely an
  average masking a wide range, and the experiment needs to compare like-for-like.

## 3. Experiment design

**Design**: staged rollout with a within-subject comparison, not a pure randomized A/B — CS
managers manage a fixed client roster, so randomizing "this report is automated, that one isn't"
for the same person on the same client in the same month introduces confusion, not clean signal.

- **Stage A — pilot (4 weeks)**: 4–5 CS managers each keep 2 comparable clients on the old manual
  process and move 2 comparable clients (similar source count, similar report length historically)
  to Atlas Auto-Reporter. Comparable pairing controls for the manager's own baseline speed and for
  client complexity.
- **Stage B — crossover (next 4 weeks)**: the same managers swap which clients are automated vs.
  manual. This washes out any per-client idiosyncrasy (e.g., one client's data source is just
  slower/messier) that pairing alone might miss.
- **Stage C — full rollout**: once Stage A+B clear the guardrails below, roll out to all CS
  managers, keep instrumentation on permanently (not just during the experiment) so regressions
  are caught continuously, not only during a one-time study.

**Unit of analysis**: one report-cycle (one client, one period). Not the CS manager-week, because
report complexity varies too much per client to aggregate at the person-week level without losing
signal.

## 4. Instrumentation (what gets logged automatically, no manual diary needed post-launch)

Per report-cycle, log:
- `config_opened_at`, `generate_clicked_at`, `draft_ready_at` (pipeline latency),
  `first_edit_at`, `last_edit_at`, `approved_at`, `sent_at`.
- `edit_diff_size`: character-level diff between AI draft and sent version, per section.
- `regenerate_count`: how many times a section was regenerated before send.
- `review_duration` = `sent_at - draft_ready_at` (proxy for how carefully it was reviewed).
- Post-send: any client reply flagging an error or confusion, tagged by the CS manager
  (`client_flagged_error: bool`, free-text reason).

This replaces the manual time-diary entirely once Auto-Reporter is the primary path — the
system observes its own usage instead of asking people to self-report.

## 5. Success criteria

| Metric | Threshold to call it a win | Guardrail (must not violate) |
|---|---|---|
| Time-to-send | Median drops ≥60% vs. matched-client baseline (targeting the ~4h → <30min goal in the PRD) | No client's report is *later* than its historical baseline |
| Edit rate | Median `edit_diff_size` <20% of drafted text | No report ships with 0 edits *and* <2 min review time (signals rubber-stamping, not quality) |
| Trust | — | Zero `client_flagged_error=true` incidents during pilot; any single incident triggers a pipeline review before Stage C |
| Adoption | ≥80% of pilot CS managers choose Auto-Reporter again for the same client's next cycle | Any manager reverting to fully manual for a client is interviewed for why (qualitative signal instrumentation won't catch) |

## 6. Dataset for offline eval (before touching real clients)

Before Stage A, run an **offline groundedness eval** on the synthesis step using a held-out set of
20–30 synthetic client-metric JSON payloads (the same shape `report_builder.py` produces),
covering edge cases:
- Flat/no-change period (nothing to say — draft shouldn't invent a trend).
- Sharp single-metric anomaly (e.g., a 90% traffic drop — should be flagged as anomalous, not
  narrated as a normal fluctuation, tying into the PRD's anomaly-annotation mitigation).
- Missing/null prior-period data (first report for a new client — no deltas possible).
- Conflicting signals (organic clicks down, AI visibility up — draft shouldn't pick one and ignore
  the other).

Score each generated draft against a rubric: (a) every numeric claim traces to a field in the
input JSON — automatable via regex/number-extraction diffed against the source JSON; (b) no
qualitative claim ("strong performance") contradicts the underlying delta sign; (c) reads at a
non-specialist level (a simple readability check, e.g. Flesch-Kincaid grade ≤ 10). This is a cheap
gate to run in CI on every prompt-template change, independent of the human pilot.

## 7. What would make us stop or roll back

- Any client-facing factual error traced to the AI draft (not a CS manager's own edit).
- Median review time trending toward zero while edit rate also trends toward zero (rubber-stamping
  without a corresponding quality bar — i.e., people trust it *because* they've stopped reading it).
- Time savings materialize but only for simple/single-source clients, with complex clients seeing
  no improvement or regressions (segment the results before declaring a win product-wide).
