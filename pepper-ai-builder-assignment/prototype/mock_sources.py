"""
Mock black-box clients for the 7 data sources listed in Data Available - Interview.xlsx.
Each function returns realistic-shaped data matching the documented output fields.
No real network calls are made — this simulates what Atlas's data layer already exposes.
"""
import random
from datetime import date, timedelta

random.seed(42)

CLIENT = {
    "name": "Northwind Outdoor Co.",
    "domain": "northwindoutdoor.com",
    "gsc_site_url": "sc-domain:northwindoutdoor.com",
    "ga4_property": "properties/384712201",
    "semrush_database": "us",
    "competitors": ["trailforge.com", "basecampgear.com", "summitware.com"],
}

PERIOD_END = date(2026, 7, 19)
PERIOD_START = PERIOD_END - timedelta(days=27)
PRIOR_START = PERIOD_START - timedelta(days=28)
PRIOR_END = PERIOD_START - timedelta(days=1)


# ---------- GSC: searchanalytics.query ----------
def gsc_search_analytics(dimensions=("query",), start=PERIOD_START, end=PERIOD_END, seed_offset=0):
    random.seed(hash((start, end, dimensions, seed_offset)) % (2**31))
    queries = [
        "waterproof hiking boots", "insulated water bottle", "4 person tent",
        "trail running vest", "merino wool base layer", "northwind backpack review",
        "camp stove reviews", "down sleeping bag 20f", "hiking poles carbon",
        "rain shell jacket men", "gore-tex boots women", "bear canister rental",
    ]
    rows = []
    for q in queries:
        impressions = random.randint(800, 42000)
        ctr = round(random.uniform(0.01, 0.09), 4)
        clicks = int(impressions * ctr)
        position = round(random.uniform(2.5, 24.0), 1)
        rows.append({"keys": [q], "clicks": clicks, "impressions": impressions,
                     "ctr": ctr, "position": position})
    return {"rows": rows, "responseAggregationType": "byProperty"}


# ---------- GA4: properties.runReport ----------
def ga4_run_report(start=PERIOD_START, end=PERIOD_END, seed_offset=0):
    random.seed(hash((start, end, seed_offset, "ga4")) % (2**31))
    sessions = random.randint(38000, 52000)
    conversions = random.randint(600, 1100)
    revenue = round(conversions * random.uniform(38, 61), 2)
    engagement_rate = round(random.uniform(0.42, 0.61), 3)
    return {
        "rows": [{
            "dimensionValues": [{"value": "organic"}],
            "metricValues": [
                {"value": str(sessions)}, {"value": str(conversions)},
                {"value": str(revenue)}, {"value": str(engagement_rate)},
            ],
        }],
        "totals": [{"metricValues": [
            {"value": str(sessions)}, {"value": str(conversions)},
            {"value": str(revenue)}, {"value": str(engagement_rate)},
        ]}],
        "metadata": {"currencyCode": "USD", "timeZone": "America/Denver"},
    }


# ---------- Semrush: domain_organic ----------
def semrush_domain_organic(domain=CLIENT["domain"], seed_offset=0):
    random.seed(hash((domain, seed_offset, "domorg")) % (2**31))
    keywords = [
        ("waterproof hiking boots", 18100), ("insulated water bottle", 9900),
        ("4 person tent", 6600), ("trail running vest", 1300),
        ("merino wool base layer", 4400), ("down sleeping bag 20f", 2400),
        ("hiking poles carbon", 1900), ("rain shell jacket men", 5400),
        ("gore-tex boots women", 3600), ("bear canister rental", 720),
    ]
    rows = []
    for kw, vol in keywords:
        po = random.randint(1, 40)
        pp = po + random.randint(-6, 6)
        rows.append({
            "Ph": kw, "Po": po, "Pp": max(pp, 1), "Pd": po - max(pp, 1),
            "Nq": vol, "Cp": round(random.uniform(0.4, 3.2), 2),
            "Ur": f"https://{domain}/{kw.replace(' ', '-')}",
            "Tr": round(random.uniform(0.005, 0.09), 4),
            "Tc": round(vol * random.uniform(0.4, 3.2) * 0.02, 2),
            "Fp": random.choice(["featured_snippet", "ai_overview", "people_also_ask", "none"]),
            "Fk": random.choice([0, 1, 2, 3]),
        })
    return rows


# ---------- Semrush: backlinks_overview ----------
def semrush_backlinks_overview(target=CLIENT["domain"], seed_offset=0):
    random.seed(hash((target, seed_offset, "bl")) % (2**31))
    return {
        "ascore": random.randint(28, 52),
        "total": random.randint(4800, 9200),
        "domains_num": random.randint(310, 640),
        "urls_num": random.randint(2200, 5600),
    }


# ---------- Semrush: Position Tracking (per-competitor) ----------
def semrush_position_tracking(competitors=CLIENT["competitors"], seed_offset=0):
    random.seed(hash((tuple(competitors), seed_offset, "track")) % (2**31))
    visibility = round(random.uniform(0.06, 0.19), 3)
    competitor_rows = []
    for c in competitors:
        competitor_rows.append({"domain": c, "visibility": round(random.uniform(0.05, 0.24), 3)})
    return {"visibility": visibility, "competitors": competitor_rows}


# ---------- Semrush AI: ai_visibility_overview ----------
def semrush_ai_visibility_overview(brand="northwind", seed_offset=0):
    random.seed(hash((brand, seed_offset, "aivis")) % (2**31))
    engines = ["chatgpt", "perplexity", "google_aio", "copilot", "claude"]
    per_engine = []
    for e in engines:
        per_engine.append({
            "engine": e,
            "visibility_score": round(random.uniform(8, 41), 1),
            "share_of_voice": round(random.uniform(0.03, 0.22), 3),
            "mention_rate": round(random.uniform(0.05, 0.35), 3),
            "avg_position": round(random.uniform(1.2, 4.8), 1),
            "change_vs_previous": round(random.uniform(-6, 9), 1),
        })
    return {
        "visibility_score": round(sum(p["visibility_score"] for p in per_engine) / len(per_engine), 1),
        "share_of_voice": round(sum(p["share_of_voice"] for p in per_engine) / len(per_engine), 3),
        "total_prompts_tracked": 240,
        "total_mentions": random.randint(40, 140),
        "mention_rate": round(random.uniform(0.1, 0.3), 3),
        "avg_position": round(random.uniform(1.5, 4.0), 1),
        "sentiment": {"positive": 0.61, "neutral": 0.34, "negative": 0.05},
        "per_engine": per_engine,
        "top_competing_brands": [
            {"name": "TrailForge", "share_of_voice": 0.29, "change_vs_previous": 0.03, "top_engine": "chatgpt"},
            {"name": "BasecampGear", "share_of_voice": 0.21, "change_vs_previous": -0.01, "top_engine": "perplexity"},
        ],
    }


# ---------- Semrush AI: ai_prompt_mentions ----------
def semrush_ai_prompt_mentions(brand="northwind", seed_offset=0):
    random.seed(hash((brand, seed_offset, "aipm")) % (2**31))
    return {
        "data": [
            {
                "prompt_text": "what's the most durable 4 person tent for backpacking?",
                "ai_engine": "perplexity",
                "mentioned": True,
                "position": 2,
                "response_excerpt": "...Northwind's Summit 4 is a strong pick for durability, with reinforced "
                                     "stake points and a 3000mm rainfly rating that outperforms cheaper tents...",
                "sentiment": "positive",
                "citation_urls": [f"https://{CLIENT['domain']}/tents/summit-4"],
                "competitor_brands_mentioned": ["TrailForge", "REI Co-op"],
            },
            {
                "prompt_text": "best waterproof hiking boots for wide feet",
                "ai_engine": "chatgpt",
                "mentioned": False,
                "position": None,
                "response_excerpt": "...Top picks include Merrell, Salomon, and Oboz for wide-fit support...",
                "sentiment": "neutral",
                "citation_urls": [],
                "competitor_brands_mentioned": ["Merrell", "Salomon", "Oboz"],
            },
        ]
    }


# ---------- Semrush AI: ai_citation_tracking ----------
def semrush_ai_citation_tracking(domain=CLIENT["domain"], seed_offset=0):
    random.seed(hash((domain, seed_offset, "aicite")) % (2**31))
    return {
        "data": [
            {
                "url": f"https://{domain}/guides/tent-buying-guide",
                "page_title": "The Complete Tent Buying Guide (2026)",
                "citations_count": random.randint(18, 60),
                "avg_citation_position": round(random.uniform(1.1, 2.8), 1),
                "change_vs_previous": {"citations_count_delta": random.randint(-5, 22),
                                       "percent_change": round(random.uniform(-0.1, 0.6), 2),
                                       "trend": "positive"},
            },
            {
                "url": f"https://{domain}/guides/layering-101",
                "page_title": "Layering 101: Base, Mid, Shell",
                "citations_count": random.randint(5, 28),
                "avg_citation_position": round(random.uniform(1.5, 3.5), 1),
                "change_vs_previous": {"citations_count_delta": random.randint(-3, 10),
                                       "percent_change": round(random.uniform(-0.2, 0.4), 2),
                                       "trend": "neutral"},
            },
        ]
    }


# ---------- CMS: WordPress posts ----------
def wordpress_list_posts(after=PERIOD_START, before=PERIOD_END):
    return [
        {"id": 4821, "title": {"rendered": "5 Layering Mistakes Beginners Make"},
         "date": "2026-07-08T09:00:00", "modified": "2026-07-08T09:00:00",
         "status": "publish", "link": f"https://{CLIENT['domain']}/blog/layering-mistakes",
         "categories": [12]},
        {"id": 4790, "title": {"rendered": "Gear Checklist: 3-Day Backcountry Trip"},
         "date": "2026-07-01T09:00:00", "modified": "2026-07-15T14:20:00",
         "status": "publish", "link": f"https://{CLIENT['domain']}/blog/gear-checklist",
         "categories": [8]},
    ]


def wordpress_stale_posts(modified_before=PERIOD_START - timedelta(days=365)):
    return [
        {"id": 2210, "title": {"rendered": "Best Tents Under $200 (2022)"},
         "modified": "2022-11-02T00:00:00", "link": f"https://{CLIENT['domain']}/blog/tents-under-200"},
    ]


# ---------- CMS: Contentful entries ----------
def contentful_entries(content_type="guide", limit=10):
    return {
        "total": 1,
        "items": [{
            "sys": {"id": "3xQabc", "contentType": {"sys": {"id": content_type}},
                    "updatedAt": "2026-07-14T00:00:00Z", "publishedAt": "2026-07-15T00:00:00Z"},
            "fields": {"title": "Choosing the Right Sleeping Bag Temperature Rating"},
        }],
    }
