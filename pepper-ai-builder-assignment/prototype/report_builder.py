"""
Atlas Auto-Reporter — prototype pipeline.

Pulls current + prior period data from the mock source clients, computes
deltas, and produces a client-ready report. This is the "working prototype"
deliverable: it produces a real markdown report from mock-but-realistic data,
following the exact structure the PRD (../PRD.md) specifies.

In production, STEP 4 (narrative synthesis) is an LLM call (prompt template
included below as NARRATIVE_PROMPT_TEMPLATE). Here it's replaced by a
deterministic rule-based narrator so the script runs with zero API keys —
the input/output contract is identical either way: structured JSON in,
prose + citations out.
"""
import json
from datetime import date
import mock_sources as src

CLIENT = src.CLIENT


def pct_change(new, old):
    if old == 0:
        return None
    return round((new - old) / old * 100, 1)


# ---------------------------------------------------------------------------
# STEP 1: Fetch — pull current + prior period from every connected source
# ---------------------------------------------------------------------------
def fetch_all():
    cur = {
        "gsc": src.gsc_search_analytics(seed_offset=0),
        "ga4": src.ga4_run_report(seed_offset=0),
        "semrush_organic": src.semrush_domain_organic(seed_offset=0),
        "semrush_backlinks": src.semrush_backlinks_overview(seed_offset=0),
        "semrush_tracking": src.semrush_position_tracking(seed_offset=0),
        "ai_visibility": src.semrush_ai_visibility_overview(seed_offset=0),
        "ai_prompts": src.semrush_ai_prompt_mentions(seed_offset=0),
        "ai_citations": src.semrush_ai_citation_tracking(seed_offset=0),
        "wp_posts": src.wordpress_list_posts(),
        "wp_stale": src.wordpress_stale_posts(),
        "contentful": src.contentful_entries(),
    }
    prior = {
        "gsc": src.gsc_search_analytics(seed_offset=1),
        "ga4": src.ga4_run_report(seed_offset=1),
        "semrush_backlinks": src.semrush_backlinks_overview(seed_offset=1),
        "ai_visibility": src.semrush_ai_visibility_overview(seed_offset=1),
    }
    return cur, prior


# ---------------------------------------------------------------------------
# STEP 2: Aggregate — roll raw rows into report-level metrics
# ---------------------------------------------------------------------------
def aggregate(cur, prior):
    gsc_rows = cur["gsc"]["rows"]
    gsc_clicks = sum(r["clicks"] for r in gsc_rows)
    gsc_impr = sum(r["impressions"] for r in gsc_rows)
    gsc_ctr = round(gsc_clicks / gsc_impr, 4) if gsc_impr else 0
    gsc_pos = round(sum(r["position"] for r in gsc_rows) / len(gsc_rows), 1)

    prior_rows = prior["gsc"]["rows"]
    prior_clicks = sum(r["clicks"] for r in prior_rows)
    prior_impr = sum(r["impressions"] for r in prior_rows)
    prior_pos = round(sum(r["position"] for r in prior_rows) / len(prior_rows), 1)

    ga4_sessions = int(cur["ga4"]["totals"][0]["metricValues"][0]["value"])
    ga4_conversions = int(cur["ga4"]["totals"][0]["metricValues"][1]["value"])
    ga4_revenue = float(cur["ga4"]["totals"][0]["metricValues"][2]["value"])
    prior_sessions = int(prior["ga4"]["totals"][0]["metricValues"][0]["value"])
    prior_conversions = int(prior["ga4"]["totals"][0]["metricValues"][1]["value"])

    movers = sorted(cur["semrush_organic"], key=lambda r: r["Pd"])
    top_gainers = [r for r in movers if r["Pd"] < 0][:3]
    top_losers = [r for r in movers if r["Pd"] > 0][-3:]

    ai_cur = cur["ai_visibility"]
    ai_prior = prior["ai_visibility"]

    return {
        "gsc": {
            "clicks": gsc_clicks, "clicks_delta_pct": pct_change(gsc_clicks, prior_clicks),
            "impressions": gsc_impr, "impressions_delta_pct": pct_change(gsc_impr, prior_impr),
            "ctr": gsc_ctr, "avg_position": gsc_pos, "position_delta": round(prior_pos - gsc_pos, 1),
        },
        "ga4": {
            "sessions": ga4_sessions, "sessions_delta_pct": pct_change(ga4_sessions, prior_sessions),
            "conversions": ga4_conversions, "conversions_delta_pct": pct_change(ga4_conversions, prior_conversions),
            "revenue": ga4_revenue,
        },
        "rankings": {"top_gainers": top_gainers, "top_losers": top_losers},
        "backlinks": {
            "ascore": cur["semrush_backlinks"]["ascore"],
            "ascore_delta": cur["semrush_backlinks"]["ascore"] - prior["semrush_backlinks"]["ascore"],
            "total": cur["semrush_backlinks"]["total"],
        },
        "ai_visibility": {
            "score": ai_cur["visibility_score"],
            "score_delta": round(ai_cur["visibility_score"] - ai_prior["visibility_score"], 1),
            "share_of_voice": ai_cur["share_of_voice"],
            "top_competitor": ai_cur["top_competing_brands"][0],
            "per_engine": ai_cur["per_engine"],
            "best_mention": cur["ai_prompts"]["data"][0],
        },
        "ai_citations": cur["ai_citations"]["data"],
        "content_published": cur["wp_posts"],
        "stale_content": cur["wp_stale"],
    }


# ---------------------------------------------------------------------------
# STEP 3: Insight rules — flag what's worth the CS manager's / client's attention
# ---------------------------------------------------------------------------
def build_insights(m):
    insights = []
    if m["gsc"]["clicks_delta_pct"] and m["gsc"]["clicks_delta_pct"] > 5:
        insights.append(f"Organic clicks grew {m['gsc']['clicks_delta_pct']}% vs the prior period, "
                         f"outpacing the {m['gsc']['impressions_delta_pct']}% growth in impressions — "
                         f"listings are converting better, not just showing up more.")
    elif m["gsc"]["clicks_delta_pct"] and m["gsc"]["clicks_delta_pct"] < -5:
        insights.append(f"Organic clicks fell {abs(m['gsc']['clicks_delta_pct'])}% vs the prior period — "
                         f"worth a CTR/title-tag review on the top pages below.")
    if m["gsc"]["position_delta"] > 0.3:
        insights.append(f"Average ranking position improved by {m['gsc']['position_delta']} spots "
                         f"across tracked queries.")
    if m["ga4"]["conversions_delta_pct"] and m["ga4"]["conversions_delta_pct"] > 0:
        insights.append(f"Organic-driven conversions are up {m['ga4']['conversions_delta_pct']}% "
                         f"(${m['ga4']['revenue']:,.0f} in attributed revenue this period).")
    if m["backlinks"]["ascore_delta"] != 0:
        direction = "climbed" if m["backlinks"]["ascore_delta"] > 0 else "slipped"
        insights.append(f"Domain Authority Score {direction} to {m['backlinks']['ascore']} "
                         f"({m['backlinks']['ascore_delta']:+d}).")
    ai = m["ai_visibility"]
    if ai["score_delta"] > 0:
        insights.append(f"AI search visibility score rose to {ai['score']} ({ai['score_delta']:+.1f}) — "
                         f"{CLIENT['name']} now holds {ai['share_of_voice']*100:.0f}% share of voice across "
                         f"tracked ChatGPT/Perplexity/Google AI Overview/Copilot/Claude prompts, vs "
                         f"{ai['top_competitor']['name']} at {ai['top_competitor']['share_of_voice']*100:.0f}%.")
    else:
        insights.append(f"AI search visibility dipped to {ai['score']} ({ai['score_delta']:+.1f}); "
                         f"{ai['top_competitor']['name']} leads share of voice at "
                         f"{ai['top_competitor']['share_of_voice']*100:.0f}%.")
    top_gainer = m["rankings"]["top_gainers"][0] if m["rankings"]["top_gainers"] else None
    if top_gainer:
        insights.append(f"Biggest keyword mover: \"{top_gainer['Ph']}\" jumped from position "
                         f"{top_gainer['Pp']} to {top_gainer['Po']} ({top_gainer['Nq']:,} monthly searches).")
    if m["stale_content"]:
        insights.append(f"{len(m['stale_content'])} page(s) haven't been updated in 12+ months, "
                         f"including \"{m['stale_content'][0]['title']['rendered']}\" — a refresh candidate.")
    return insights


NARRATIVE_PROMPT_TEMPLATE = """You are drafting the executive summary for a monthly SEO/AI-search \
performance report for {client_name}. Write 3-4 sentences, plain language, for a marketing \
director audience (not an SEO specialist). Lead with the single most important trend. Every \
number you cite must come from the JSON below — never invent a figure. Flag one risk and one \
recommended next action.

DATA:
{metrics_json}

PRIOR REPORT ACTION ITEMS (for continuity, mention if resolved):
{prior_action_items}
"""


def render_markdown(m, insights):
    lines = []
    lines.append(f"# {CLIENT['name']} — Search & AI Visibility Report")
    lines.append(f"**Period:** {src.PERIOD_START:%b %d} – {src.PERIOD_END:%b %d, %Y}  |  "
                 f"**Domain:** {CLIENT['domain']}\n")

    lines.append("## Executive Summary")
    for s in insights:
        lines.append(f"- {s}")
    lines.append("")

    lines.append("## Organic Search (Google Search Console)")
    g = m["gsc"]
    lines.append(f"| Metric | This Period | vs Prior |\n|---|---|---|")
    lines.append(f"| Clicks | {g['clicks']:,} | {g['clicks_delta_pct']:+.1f}% |")
    lines.append(f"| Impressions | {g['impressions']:,} | {g['impressions_delta_pct']:+.1f}% |")
    lines.append(f"| CTR | {g['ctr']*100:.2f}% | — |")
    lines.append(f"| Avg. Position | {g['avg_position']} | {g['position_delta']:+.1f} |\n")

    lines.append("## Web Analytics (GA4 — Organic Channel)")
    a = m["ga4"]
    lines.append(f"| Metric | This Period | vs Prior |\n|---|---|---|")
    lines.append(f"| Sessions | {a['sessions']:,} | {a['sessions_delta_pct']:+.1f}% |")
    lines.append(f"| Conversions | {a['conversions']:,} | {a['conversions_delta_pct']:+.1f}% |")
    lines.append(f"| Attributed Revenue | ${a['revenue']:,.0f} | — |\n")

    lines.append("## Keyword Rankings (Semrush)")
    lines.append("**Top gainers**")
    for r in m["rankings"]["top_gainers"]:
        lines.append(f"- \"{r['Ph']}\": {r['Pp']} → {r['Po']} ({r['Nq']:,} searches/mo)")
    lines.append("\n**Top losers**")
    for r in m["rankings"]["top_losers"]:
        lines.append(f"- \"{r['Ph']}\": {r['Pp']} → {r['Po']} ({r['Nq']:,} searches/mo)")
    lines.append(f"\nDomain Authority Score: **{m['backlinks']['ascore']}** "
                 f"({m['backlinks']['ascore_delta']:+d}), {m['backlinks']['total']:,} total backlinks.\n")

    lines.append("## AI Search Visibility (Semrush AI Toolkit — ChatGPT, Perplexity, Google AIO, Copilot, Claude)")
    ai = m["ai_visibility"]
    lines.append(f"Visibility score: **{ai['score']}** ({ai['score_delta']:+.1f}) · "
                 f"Share of voice: **{ai['share_of_voice']*100:.0f}%**\n")
    lines.append("| Engine | Visibility | Share of Voice | Avg. Position | Change |\n|---|---|---|---|---|")
    for e in ai["per_engine"]:
        lines.append(f"| {e['engine']} | {e['visibility_score']} | {e['share_of_voice']*100:.0f}% "
                     f"| {e['avg_position']} | {e['change_vs_previous']:+.1f} |")
    bm = ai["best_mention"]
    lines.append(f"\n> *Example mention ({bm['ai_engine']}, {bm['sentiment']}):* \"{bm['response_excerpt']}\"\n")

    lines.append("### Most-cited pages in AI answers")
    for c in m["ai_citations"]:
        lines.append(f"- [{c['page_title']}]({c['url']}) — {c['citations_count']} citations "
                     f"({c['change_vs_previous']['percent_change']*100:+.0f}%)")
    lines.append("")

    lines.append("## Content Published This Period")
    for p in m["content_published"]:
        lines.append(f"- [{p['title']['rendered']}]({p['link']}) — {p['date'][:10]}")
    if m["stale_content"]:
        lines.append("\n**Refresh candidates (12+ months stale):**")
        for p in m["stale_content"]:
            lines.append(f"- [{p['title']['rendered']}]({p['link']}) — last updated {p['modified'][:10]}")
    lines.append("")

    lines.append("## Recommended Next Actions")
    lines.append("1. Refresh the stale guide flagged above and add an FAQ block targeting the AI-cited queries.")
    lines.append("2. Publish a comparison page targeting \"" +
                 (m["rankings"]["top_losers"][-1]["Ph"] if m["rankings"]["top_losers"] else "a declining query") +
                 "\" to recover lost position.")
    lines.append(f"3. Monitor {ai['top_competitor']['name']}'s AI share-of-voice gains — consider a prompt-level "
                 f"content gap analysis next cycle.")
    lines.append("")
    lines.append("---\n*Draft generated by Atlas Auto-Reporter. Review and edit before sending — "
                 "see PRD §5 (Human-in-the-loop review) for the approval workflow.*")
    return "\n".join(lines)


def main():
    cur, prior = fetch_all()
    metrics = aggregate(cur, prior)
    insights = build_insights(metrics)
    report_md = render_markdown(metrics, insights)

    with open("sample_report_output.md", "w") as f:
        f.write(report_md)

    with open("sample_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    print(NARRATIVE_PROMPT_TEMPLATE.format(
        client_name=CLIENT["name"],
        metrics_json=json.dumps({k: v for k, v in metrics.items() if k not in ("rankings",)},
                                 indent=2, default=str)[:800] + " ...(truncated)",
        prior_action_items="1. Refresh sleeping-bag guide (DONE — published Jul 8)\n"
                            "2. Improve mobile page speed on /tents/* (IN PROGRESS)",
    ))
    print("\n--- Report written to sample_report_output.md ---")


if __name__ == "__main__":
    main()
