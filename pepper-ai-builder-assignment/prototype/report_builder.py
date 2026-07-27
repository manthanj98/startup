"""
Atlas Auto-Reporter — prototype pipeline.

Pulls current + prior period data from the mock source clients, computes
deltas, and produces a client-ready report. This is the "working prototype"
deliverable: it produces a real markdown report from mock-but-realistic data,
following the exact structure the PRD (../PRD.md) specifies.

Runs for all three sample clients defined in mock_sources.CLIENTS, so the
dashboard/config/review screens in ux-flow.html each show genuinely
different data per brand instead of one dataset reused everywhere.

In production, STEP 4 (narrative synthesis) is an LLM call (prompt template
included below as NARRATIVE_PROMPT_TEMPLATE). Here it's replaced by a
deterministic rule-based narrator so the script runs with zero API keys —
the input/output contract is identical either way: structured JSON in,
prose + citations out.
"""
import json
import re
from pathlib import Path
import mock_sources as src


def pct_change(new, old):
    if old == 0:
        return None
    return round((new - old) / old * 100, 1)


# ---------------------------------------------------------------------------
# STEP 1: Fetch — pull current + prior period from every connected source
# ---------------------------------------------------------------------------
def fetch_all(client):
    cur = {
        "gsc": src.gsc_search_analytics(client, seed_offset=0),
        "ga4": src.ga4_run_report(client, seed_offset=0),
        "ga4_by_pillar": src.ga4_by_landing_page_group(client, seed_offset=0),
        "semrush_organic": src.semrush_domain_organic(client, seed_offset=0),
        "semrush_backlinks": src.semrush_backlinks_overview(client, seed_offset=0),
        "semrush_tracking": src.semrush_position_tracking(client, seed_offset=0),
        "semrush_competitors": src.semrush_competitor_comparison(client, seed_offset=0),
        "semrush_category": src.semrush_category_share(client, seed_offset=0),
        "ai_visibility": src.semrush_ai_visibility_overview(client, seed_offset=0),
        "ai_by_competitor": src.ai_visibility_by_competitor(client, seed_offset=0),
        "ai_by_pillar": src.ai_visibility_by_pillar(client, seed_offset=0),
        "ai_prompts": src.semrush_ai_prompt_mentions(client, seed_offset=0),
        "ai_citations": src.semrush_ai_citation_tracking(client, seed_offset=0),
        "cms": src.cms_list_content(client),
    }
    prior = {
        "gsc": src.gsc_search_analytics(client, seed_offset=1),
        "ga4": src.ga4_run_report(client, seed_offset=1),
        "ga4_by_pillar": src.ga4_by_landing_page_group(client, seed_offset=1),
        "semrush_backlinks": src.semrush_backlinks_overview(client, seed_offset=1),
        "semrush_category": src.semrush_category_share(client, seed_offset=1),
        "ai_visibility": src.semrush_ai_visibility_overview(client, seed_offset=1),
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
            # Derive the leading competitor from the same per-competitor GEO rows the
            # Competitive tab renders, so the executive summary and the head-to-head
            # table never quote two different numbers for the same brand.
            "top_competitor": max(cur["ai_by_competitor"], key=lambda r: r["share_of_voice"]),
            "per_engine": ai_cur["per_engine"],
            "best_mention": cur["ai_prompts"]["data"][0],
        },
        "ai_citations": cur["ai_citations"]["data"],
        "cms": cur["cms"],
        "content_published": cur["cms"]["published"],
        "stale_content": cur["cms"]["stale"],
    }


# ---------------------------------------------------------------------------
# STEP 2b: The two analysis views.
#
# Both views span the same four layers so the story is end-to-end rather than
# siloed per tool:
#   traditional search (GSC + Semrush) → GEO (Semrush AI) → conversion (GA4)
# The Competitive view slices that by named competitor brand; the Category view
# slices it by topic pillar within the client's industry.
# ---------------------------------------------------------------------------
def build_competitive_view(client, cur, prior):
    comp = cur["semrush_competitors"]
    geo_rows = {r["name"]: r for r in cur["ai_by_competitor"]}
    own_geo = cur["ai_visibility"]

    rivals = []
    for r in comp["competitors"]:
        geo = geo_rows.get(r["name"], {})
        search_gap = round(comp["own"]["visibility"] - r["visibility"], 3)
        geo_gap = round(own_geo["share_of_voice"] - geo.get("share_of_voice", 0), 3)
        rivals.append({
            "name": r["name"], "domain": r["domain"],
            "search_visibility": r["visibility"],
            "search_avg_position": r["avg_position"],
            "keyword_overlap": r["keyword_overlap"],
            "geo_share_of_voice": geo.get("share_of_voice", 0),
            "geo_visibility_score": geo.get("visibility_score", 0),
            "geo_top_engine": geo.get("top_engine", "—"),
            "search_gap": search_gap,
            "geo_gap": geo_gap,
            # Where we stand on each layer, so the UI can badge lead/trail per row.
            "leads_search": search_gap > 0,
            "leads_geo": geo_gap > 0,
        })

    trailing_geo = [r for r in rivals if not r["leads_geo"]]
    trailing_search = [r for r in rivals if not r["leads_search"]]
    return {
        "own": {
            "name": client["name"], "domain": client["domain"],
            "search_visibility": comp["own"]["visibility"],
            "search_avg_position": comp["own"]["avg_position"],
            "keywords_tracked": comp["own"]["keywords_tracked"],
            "geo_share_of_voice": own_geo["share_of_voice"],
            "geo_visibility_score": own_geo["visibility_score"],
        },
        "competitors": rivals,
        "summary": {
            "behind_on_geo": [r["name"] for r in trailing_geo],
            "behind_on_search": [r["name"] for r in trailing_search],
            "ahead_of_all_geo": len(trailing_geo) == 0,
        },
    }


def build_category_view(client, cur, prior):
    cat = cur["semrush_category"]
    prior_cat = prior["semrush_category"]
    ga4_groups = cur["ga4_by_pillar"]
    prior_ga4 = prior["ga4_by_pillar"]
    ai_pillars = cur["ai_by_pillar"]
    gsc_rows = {r["keys"][0]: r for r in cur["gsc"]["rows"]}
    semrush_rows = {r["Ph"]: r for r in cur["semrush_organic"]}

    pillars = []
    for p in client["category_pillars"]:
        # Traditional search: roll the pillar's own queries up from GSC + Semrush.
        pq = [gsc_rows[q] for q in p["queries"] if q in gsc_rows]
        clicks = sum(r["clicks"] for r in pq)
        impressions = sum(r["impressions"] for r in pq)
        avg_pos = round(sum(r["position"] for r in pq) / len(pq), 1) if pq else None
        sr = [semrush_rows[q] for q in p["queries"] if q in semrush_rows]
        semrush_pos = round(sum(r["Po"] for r in sr) / len(sr), 1) if sr else None

        geo = ai_pillars[p["id"]]
        ga = ga4_groups[p["id"]]
        prior_ga = prior_ga4[p["id"]]

        vs_category = round(geo["visibility_score"] - geo["category_avg_visibility"], 1)
        pillars.append({
            "id": p["id"], "pillar": p["pillar"], "title": p["title"],
            "search": {"clicks": clicks, "impressions": impressions,
                       "avg_position": avg_pos, "semrush_position": semrush_pos,
                       "queries": p["queries"]},
            "geo": {"visibility_score": geo["visibility_score"],
                    "category_avg": geo["category_avg_visibility"],
                    "vs_category": vs_category,
                    "mentions": geo["mentions"], "mentions_total": geo["mentions_total"]},
            "conversion": {"sessions": ga["sessions"], "conversions": ga["conversions"],
                           "conversion_rate": ga["conversion_rate"], "revenue": ga["revenue"],
                           "conversions_delta_pct": pct_change(ga["conversions"], prior_ga["conversions"])},
            "owned_page": p["owned_page"],
            "verdict": "winning" if vs_category > 0 else "losing",
            "bullets": p["bullets"],
            "recommendations": p["recommendations"],
        })

    return {
        "category": cat["category"],
        "own_share": cat["own_share"],
        "own_share_delta": round(cat["own_share"] - prior_cat["own_share"], 3),
        "own_rank": cat["own_rank"],
        "brands_tracked": cat["brands_tracked"],
        "named_competitors": cat["named_competitors"],
        "long_tail_share": cat["long_tail_share"],
        "total_category_prompts": cat["total_category_prompts"],
        "total_category_keywords": cat["total_category_keywords"],
        "pillars": pillars,
    }


def build_content_recommendations(client, category_view, cms):
    """Split recommendations into the two buckets the CSM actually acts on.

    New content   — pillars with no owning page where we're absent/weak: propose a new page.
    Existing content — pillars that own a page which is stale or underperforming: propose a refresh.

    Each item is routed to the client's CMS. WordPress exposes POST /wp/v2/posts, so those can be
    pushed as drafts; Webflow and Contentful are read-only in the documented API set, so they
    produce a brief for a human to paste in.
    """
    new_content, existing_content = [], []
    for p in category_view["pillars"]:
        rec = p["recommendations"][0] if p["recommendations"] else None
        if not rec:
            continue
        item = {
            "pillar": p["pillar"], "pillar_id": p["id"],
            "title": rec["title"], "body": rec["body"], "citation": rec["citation"],
            "geo_visibility": p["geo"]["visibility_score"],
            "vs_category": p["geo"]["vs_category"],
            "conversions": p["conversion"]["conversions"],
            "cms": cms["label"],
            "action": "Create draft in " + cms["label"] if cms["can_draft"] else "Brief for " + cms["label"],
            "can_draft": cms["can_draft"],
        }
        if p["owned_page"]:
            item["target_page"] = p["owned_page"]
            existing_content.append(item)
        else:
            new_content.append(item)

    # Highest-leverage first: biggest gap vs the category average.
    new_content.sort(key=lambda i: i["vs_category"])
    existing_content.sort(key=lambda i: i["vs_category"])
    return {"cms": cms["label"], "can_draft": cms["can_draft"],
            "new_content": new_content, "existing_content": existing_content}


# ---------------------------------------------------------------------------
# STEP 3: Insight rules — flag what's worth the CS manager's / client's attention
# ---------------------------------------------------------------------------
def build_insights(client, m):
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
                         f"{client['name']} now holds {ai['share_of_voice']*100:.0f}% share of voice across "
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
                         f"including \"{m['stale_content'][0]['title']}\" — a refresh candidate.")
    return insights


NARRATIVE_PROMPT_TEMPLATE = """You are drafting the executive summary for a {cadence} SEO/AI-search \
performance report for {client_name}. Write 3-4 sentences, plain language, for a marketing \
director audience (not an SEO specialist). Lead with the single most important trend. Every \
number you cite must come from the JSON below — never invent a figure. Flag one risk and one \
recommended next action.

DATA:
{metrics_json}

PRIOR REPORT ACTION ITEMS (for continuity, mention if resolved):
{prior_action_items}
"""


def render_markdown(client, m, insights):
    lines = []
    lines.append(f"# {client['name']} — Search & AI Visibility Report")
    lines.append(f"**Period:** {src.PERIOD_START:%b %d} – {src.PERIOD_END:%b %d, %Y}  |  "
                 f"**Domain:** {client['domain']}\n")

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
    lines.append(f"*Source CMS: {m['cms']['label']}*\n")
    for p in m["content_published"]:
        lines.append(f"- [{p['title']}]({p['url']}) — {p['modified'][:10]}")
    if m["stale_content"]:
        lines.append("\n**Refresh candidates (12+ months stale):**")
        for p in m["stale_content"]:
            lines.append(f"- [{p['title']}]({p['url']}) — last updated {p['modified'][:10]}")
    lines.append("")

    # ---- TAB 1 ----------------------------------------------------------
    cv = m["competitive"]
    lines.append("## Tab 1 — Competitive Position")
    lines.append(f"How {client['name']} stacks up against the tracked competitor set, on traditional "
                 f"search and AI search together.\n")
    lines.append("| Brand | Search visibility | Avg. position | GEO share of voice | GEO visibility | Top engine |")
    lines.append("|---|---|---|---|---|---|")
    o = cv["own"]
    lines.append(f"| **{o['name']}** (us) | {o['search_visibility']*100:.1f}% | {o['search_avg_position']} "
                 f"| {o['geo_share_of_voice']*100:.1f}% | {o['geo_visibility_score']} | — |")
    for r in cv["competitors"]:
        lines.append(f"| {r['name']} | {r['search_visibility']*100:.1f}% | {r['search_avg_position']} "
                     f"| {r['geo_share_of_voice']*100:.1f}% | {r['geo_visibility_score']} | {r['geo_top_engine']} |")
    lines.append("")
    if cv["summary"]["behind_on_geo"]:
        lines.append(f"**Trailing on AI search vs:** {', '.join(cv['summary']['behind_on_geo'])}")
    if cv["summary"]["behind_on_search"]:
        lines.append(f"**Trailing on traditional search vs:** {', '.join(cv['summary']['behind_on_search'])}")
    if cv["summary"]["ahead_of_all_geo"]:
        lines.append("**Leading every tracked competitor on AI share of voice this period.**")
    lines.append("")

    # ---- TAB 2 ----------------------------------------------------------
    cat = m["category"]
    lines.append("## Tab 2 — Category Performance")
    lines.append(f"Position within **{cat['category']}** — {cat['brands_tracked']} brands tracked across "
                 f"{cat['total_category_prompts']:,} category prompts and {cat['total_category_keywords']:,} keywords.\n")
    lines.append(f"- **Category share of voice:** {cat['own_share']*100:.1f}% "
                 f"({cat['own_share_delta']*100:+.1f} pts vs prior) — rank #{cat['own_rank']} of {cat['brands_tracked']}")
    lines.append(f"- **Named competitors hold:** " +
                 ", ".join(f"{c['name']} {c['share']*100:.1f}%" for c in cat["named_competitors"]))
    lines.append(f"- **Long tail (all other brands):** {cat['long_tail_share']*100:.1f}%\n")

    lines.append("### Topic pillars — search → AI → conversion")
    lines.append("| Pillar | Clicks | Avg. pos | GEO visibility | vs category avg | Sessions | Conversions | Verdict |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for p in cat["pillars"]:
        s, geo, cvn = p["search"], p["geo"], p["conversion"]
        lines.append(f"| {p['pillar']} | {s['clicks']:,} | {s['avg_position'] or '—'} | {geo['visibility_score']} "
                     f"| {geo['vs_category']:+.1f} | {cvn['sessions']:,} | {cvn['conversions']:,} "
                     f"| {'✅ winning' if p['verdict'] == 'winning' else '⚠️ losing'} |")
    lines.append("")
    for p in cat["pillars"]:
        lines.append(f"**{p['title']}**")
        for b in p["bullets"]:
            lines.append(f"- *{b['label']}:* {b['text']}")
        lines.append("")

    # ---- CONTENT RECOMMENDATIONS ---------------------------------------
    cr = m["content_recommendations"]
    lines.append("## Content Recommendations")
    lines.append(f"*Routed to {cr['cms']}. " +
                 ("Drafts can be created directly via the CMS API.*" if cr["can_draft"]
                  else "This CMS is read-only in Atlas, so these are briefs for an editor to action.*") + "\n")

    lines.append("### New content (gaps with no owning page)")
    if cr["new_content"]:
        for i, item in enumerate(cr["new_content"], 1):
            lines.append(f"{i}. **{item['title']}** — *{item['pillar']}* ({item['action']})")
            lines.append(f"   {item['body']}")
            lines.append(f"   Reference: [{item['citation']['text']}]({item['citation']['url']})")
    else:
        lines.append("_No uncovered pillars this period._")
    lines.append("")

    lines.append("### Existing content (refresh / expand)")
    if cr["existing_content"]:
        for i, item in enumerate(cr["existing_content"], 1):
            tp = item.get("target_page") or {}
            lines.append(f"{i}. **{item['title']}** — *{item['pillar']}* ({item['action']})")
            if tp:
                lines.append(f"   Target page: {tp['title']} (last updated {tp['last_modified'][:10]})")
            lines.append(f"   {item['body']}")
            lines.append(f"   Reference: [{item['citation']['text']}]({item['citation']['url']})")
    else:
        lines.append("_No refresh candidates this period._")
    lines.append("")

    lines.append("---\n*Draft generated by Atlas Auto-Reporter. Review and edit before sending — "
                 "see PRD §5 (Human-in-the-loop review) for the approval workflow.*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# STEP 5: Sync — feed the same computed data into the UX flow artifact, so
# renderReport() in ux-flow.html shows numbers this run actually produced
# instead of a hand-copied snapshot. One entry per client, keyed by slug.
# ---------------------------------------------------------------------------
def build_review_json(client, m):
    g, a, bl, ai = m["gsc"], m["ga4"], m["backlinks"], m["ai_visibility"]
    return {
        "client_name": client["name"],
        "domain": client["domain"],
        "cadence": client["cadence"],
        "period_label": f"{src.PERIOD_START:%b %d}–{src.PERIOD_END:%b %d}",
        "summary": [
            {"src": "GSC", "text": f"Organic clicks {'grew' if g['clicks_delta_pct'] and g['clicks_delta_pct'] > 0 else 'fell'} "
                                    f"{abs(g['clicks_delta_pct']):.1f}% vs the prior period."},
            {"src": "GA4", "text": f"Organic-driven conversions are {'up' if a['conversions_delta_pct'] and a['conversions_delta_pct'] > 0 else 'down'} "
                                    f"{abs(a['conversions_delta_pct']):.1f}% (${a['revenue']:,.0f} in attributed revenue this period)."},
            {"src": "Semrush", "text": f"Domain Authority Score {'climbed' if bl['ascore_delta'] >= 0 else 'slipped'} to {bl['ascore']} "
                                       f"({bl['ascore_delta']:+d})."},
            {"src": "AI Toolkit", "text": f"AI search visibility {'rose' if ai['score_delta'] > 0 else 'dipped'} to {ai['score']} "
                                          f"({ai['score_delta']:+.1f}) — {client['name']} holds {ai['share_of_voice']*100:.0f}% share of voice "
                                          f"vs {ai['top_competitor']['name']} at {ai['top_competitor']['share_of_voice']*100:.0f}%."},
        ],
        "gsc": {"clicks": g["clicks"], "clicks_delta_pct": g["clicks_delta_pct"],
                "impressions": g["impressions"], "impressions_delta_pct": g["impressions_delta_pct"],
                "avg_position": g["avg_position"], "position_delta": abs(g["position_delta"])},
        "ga4": {"sessions": a["sessions"], "sessions_delta_pct": a["sessions_delta_pct"],
                "conversions": a["conversions"], "conversions_delta_pct": a["conversions_delta_pct"],
                "revenue": a["revenue"]},
        "backlinks": {"ascore": bl["ascore"], "ascore_delta": bl["ascore_delta"]},
        "ai_visibility": {
            "score": ai["score"], "score_delta": ai["score_delta"], "share_of_voice": ai["share_of_voice"],
            "top_competitor": {"name": ai["top_competitor"]["name"], "share_of_voice": ai["top_competitor"]["share_of_voice"]},
            "per_engine": [{"engine": e["engine"], "visibility_score": e["visibility_score"],
                            "share_of_voice": e["share_of_voice"], "avg_position": e["avg_position"],
                            "change_vs_previous": e["change_vs_previous"]} for e in ai["per_engine"]],
            "best_mention": {"ai_engine": ai["best_mention"]["ai_engine"], "sentiment": ai["best_mention"]["sentiment"],
                              "response_excerpt": ai["best_mention"]["response_excerpt"]},
        },
        "ai_citations": [{"page_title": c["page_title"], "url": c["url"], "citations_count": c["citations_count"],
                          "percent_change": c["change_vs_previous"]["percent_change"]} for c in m["ai_citations"]],
        "recommendations": [
            "Refresh the stale guide flagged above and add an FAQ block targeting the AI-cited queries.",
            f"Publish a comparison page targeting \"{m['rankings']['top_losers'][-1]['Ph'] if m['rankings']['top_losers'] else 'a declining query'}\" "
            f"to recover lost position.",
            f"Monitor {ai['top_competitor']['name']}'s AI share-of-voice gains — consider a prompt-level content gap analysis next cycle.",
        ],
        # --- CSM-entered inputs, echoed back so the Configure screen can prefill ---
        "inputs": {
            "industry": client["industry"],
            "cms": client["cms"],
            "cms_label": m["cms"]["label"],
            "recipients": client["recipients"],
            "competitor_brands": client["competitor_brands"],
            "priority_prompts": client["priority_prompts"],
            "priority_keywords": client["priority_keywords"],
        },
        # --- Tab 1: competitive position ---
        "competitive": m["competitive"],
        # --- Tab 2: category performance (share header + topic pillars) ---
        "category": m["category"],
        # --- Content recommendations, split new vs existing, routed to the client's CMS ---
        "content_recommendations": m["content_recommendations"],
    }


def sync_ux_flow(review_json_by_client):
    ux_path = Path(__file__).parent.parent / "ux-flow.html"
    html = ux_path.read_text()
    pattern = re.compile(
        r'(<script type="application/json" id="report-data">\n)(.*?)(\n</script>)',
        re.DOTALL,
    )
    new_html, n = pattern.subn(
        lambda m_: m_.group(1) + json.dumps(review_json_by_client, indent=2) + m_.group(3),
        html,
    )
    if n == 0:
        print("Warning: could not find #report-data block in ux-flow.html — skipped sync.")
        return
    ux_path.write_text(new_html)
    print(f"--- Synced live metrics for {len(review_json_by_client)} client(s) into {ux_path} ---")


def main():
    review_json_by_client = {}
    for slug, client in src.CLIENTS.items():
        cur, prior = fetch_all(client)
        metrics = aggregate(cur, prior)
        # The two analysis views, plus the CMS-routed content recommendations derived from them.
        metrics["competitive"] = build_competitive_view(client, cur, prior)
        metrics["category"] = build_category_view(client, cur, prior)
        metrics["content_recommendations"] = build_content_recommendations(
            client, metrics["category"], cur["cms"])
        insights = build_insights(client, metrics)
        report_md = render_markdown(client, metrics, insights)

        with open(f"sample_report_output_{slug}.md", "w") as f:
            f.write(report_md)
        with open(f"sample_metrics_{slug}.json", "w") as f:
            json.dump(metrics, f, indent=2, default=str)

        review_json_by_client[slug] = build_review_json(client, metrics)

        if slug == "northwind":
            # Keep the original filenames pointing at the primary walkthrough client.
            with open("sample_report_output.md", "w") as f:
                f.write(report_md)
            with open("sample_metrics.json", "w") as f:
                json.dump(metrics, f, indent=2, default=str)
            print(NARRATIVE_PROMPT_TEMPLATE.format(
                cadence=client["cadence"],
                client_name=client["name"],
                metrics_json=json.dumps({k: v for k, v in metrics.items() if k not in ("rankings",)},
                                         indent=2, default=str)[:800] + " ...(truncated)",
                prior_action_items="1. Refresh sleeping-bag guide (DONE — published Jul 8)\n"
                                    "2. Improve mobile page speed on /tents/* (IN PROGRESS)",
            ))

    sync_ux_flow(review_json_by_client)
    print("\n--- Reports written for: " + ", ".join(src.CLIENTS[s]["name"] for s in src.CLIENTS) + " ---")


if __name__ == "__main__":
    main()
