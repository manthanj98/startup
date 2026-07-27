"""
Mock black-box clients for the 7 data sources listed in Data Available - Interview.xlsx.
Each function returns realistic-shaped data matching the documented output fields.
No real network calls are made — this simulates what Atlas's data layer already exposes.

Three sample clients are defined so the dashboard, config, and review screens each show
genuinely different data per brand, not one dataset reused everywhere. Each client is on a
different CMS (WordPress / Webflow / Contentful) so all three CMS sources get exercised.

Client dicts also carry the CSM-entered inputs (industry, competitor brands, priority prompts
and keywords) that the Configure screen collects — these drive both analysis views.
"""
import random
from datetime import date, timedelta

PERIOD_END = date(2026, 7, 19)
PERIOD_START = PERIOD_END - timedelta(days=27)
PRIOR_START = PERIOD_START - timedelta(days=28)
PRIOR_END = PERIOD_START - timedelta(days=1)

CLIENTS = {
    "northwind": {
        "name": "Northwind Outdoor Co.",
        "domain": "northwindoutdoor.com",
        "gsc_site_url": "sc-domain:northwindoutdoor.com",
        "ga4_property": "properties/384712201",
        "semrush_database": "us",
        "cadence": "monthly",
        "ai_brand": "northwind",
        # --- CSM-entered inputs (Configure screen) ---
        "industry": "Outdoor & camping gear",
        "cms": "wordpress",
        "recipients": "dana@northwindoutdoor.com, +2 cc",
        "competitor_brands": [
            {"name": "TrailForge", "domain": "trailforge.com"},
            {"name": "BasecampGear", "domain": "basecampgear.com"},
            {"name": "Summitware", "domain": "summitware.com"},
        ],
        "priority_prompts": [
            "what's the most durable 4 person tent for backpacking?",
            "best waterproof hiking boots for wide feet",
            "how do I choose a sleeping bag temperature rating?",
        ],
        "priority_keywords": ["waterproof hiking boots", "4 person tent", "merino wool base layer"],
        "competitors": ["trailforge.com", "basecampgear.com", "summitware.com"],
        "top_competitor": {"name": "TrailForge", "share_of_voice": 0.29, "top_engine": "chatgpt"},
        "queries": [
            "waterproof hiking boots", "insulated water bottle", "4 person tent",
            "trail running vest", "merino wool base layer", "northwind backpack review",
            "camp stove reviews", "down sleeping bag 20f", "hiking poles carbon",
            "rain shell jacket men", "gore-tex boots women", "bear canister rental",
        ],
        "keywords": [
            ("waterproof hiking boots", 18100), ("insulated water bottle", 9900),
            ("4 person tent", 6600), ("trail running vest", 1300),
            ("merino wool base layer", 4400), ("down sleeping bag 20f", 2400),
            ("hiking poles carbon", 1900), ("rain shell jacket men", 5400),
            ("gore-tex boots women", 3600), ("bear canister rental", 720),
        ],
        "best_mention": {
            "prompt_text": "what's the most durable 4 person tent for backpacking?",
            "ai_engine": "perplexity", "position": 2,
            "response_excerpt": "...Northwind's Summit 4 is a strong pick for durability, with reinforced "
                                 "stake points and a 3000mm rainfly rating that outperforms cheaper tents...",
            "sentiment": "positive", "competitor_brands_mentioned": ["TrailForge", "REI Co-op"],
        },
        "citations": [
            ("The Complete Tent Buying Guide (2026)", "guides/tent-buying-guide"),
            ("Layering 101: Base, Mid, Shell", "guides/layering-101"),
        ],
        "content_published": [
            ("5 Layering Mistakes Beginners Make", "blog/layering-mistakes", "2026-07-08T09:00:00"),
            ("Gear Checklist: 3-Day Backcountry Trip", "blog/gear-checklist", "2026-07-01T09:00:00"),
        ],
        "stale_content": [
            ("Best Tents Under $200 (2022)", "blog/tents-under-200", "2022-11-02T00:00:00"),
        ],
        "category_pillars": [
            {
                "id": "waterproof-durability",
                "pillar": "Waterproofing & Durability Claims",
                "title": "Durability claims are landing, but waterproof-rating detail is thin for Northwind",
                "mentions": 3, "mentions_total": 10,
                "queries": ["4 person tent", "rain shell jacket men", "gore-tex boots women"],
                "owned_page": {"title": "The Complete Tent Buying Guide (2026)", "slug": "guides/tent-buying-guide",
                                "last_modified": "2026-05-02T00:00:00"},
                "sentiment": {"positive": 3, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "Northwind is mentioned in 3 of 10 tracked answers about "
                     "4-person tent durability, all positive, anchored on the Summit 4's 3000mm rainfly rating."},
                    {"label": "Why it matters", "text": "Durability is the #1 reason cited in AI answers for "
                     "recommending a tent over a cheaper alternative — it's the deciding factor, not price."},
                    {"label": "Competitive contrast", "text": "TrailForge appears in 6 of 10 answers with a "
                     "published waterproof-rating comparison chart; Northwind has no equivalent page."},
                    {"label": "Source mechanism", "text": "Citing sources skew toward OutdoorGearLab and "
                     "SectionHiker — both cite spec-sheet comparison tables, which Northwind's product pages lack."},
                ],
                "recommendations": [
                    {"title": "Publish a waterproof-rating comparison table on the tent-buying guide",
                     "body": "OutdoorGearLab's tent roundup ranks well because it presents a side-by-side "
                              "waterproof-rating (mm) and hydrostatic-head table across competitors. Northwind's "
                              "guide currently only states its own rating in prose. Add a structured comparison "
                              "table (rainfly mm, floor mm, seam-taping method) so AI engines have a citable, "
                              "structured source that isn't a third party.",
                     "citation": {"text": "OutdoorGearLab — Best Tents", "url": "https://outdoorgearlab.com/best-tents"}},
                    {"title": "Add a durability FAQ block to the Summit 4 product page",
                     "body": "SectionHiker's citations come from direct answers to \"how long does this tent last "
                              "in high wind\" style questions. A product-page FAQ with specific, testable claims "
                              "(denier count, pole material, field-test conditions) gives AI engines a first-party "
                              "answer to cite instead of a review site.",
                     "citation": {"text": "SectionHiker — Northwind Summit 4 Review", "url": "https://sectionhiker.com/summit-4-review"}},
                ],
            },
            {
                "id": "sizing-fit",
                "pillar": "Sizing & Fit Guidance",
                "title": "Boot sizing questions skip Northwind entirely",
                "mentions": 0, "mentions_total": 10,
                "queries": ["waterproof hiking boots", "gore-tex boots women"],
                "owned_page": None,
                "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "For \"waterproof hiking boots wide feet\" style prompts, "
                     "Northwind shows up in 0 of 10 answers — Merrell, Salomon, and Oboz dominate."},
                    {"label": "Why it matters", "text": "Sizing/fit is one of the highest-intent questions before "
                     "a purchase; being absent here means losing the recommendation at the final decision step."},
                    {"label": "Source mechanism", "text": "Answers consistently cite REI's fit-guide article and "
                     "Reddit r/hiking threads — neither is a brand's own page, meaning the gap is winnable."},
                ],
                "recommendations": [
                    {"title": "Publish a wide-fit sizing guide for the boot line",
                     "body": "REI's fit-guide ranks because it gives concrete last-width measurements and a "
                              "\"if you wear X in brand Y, try size Z\" conversion table. Northwind has no sizing "
                              "content beyond a generic size chart — adding brand-to-brand conversions would give "
                              "AI engines a reason to cite Northwind directly for wide-fit queries.",
                     "citation": {"text": "REI Co-op — Hiking Boot Fit Guide", "url": "https://rei.com/learn/expert-advice/hiking-boots"}},
                ],
            },
            {
                "id": "layering-systems",
                "pillar": "Layering & Base-Layer Systems",
                "title": "Layering content converts well but is losing AI ground",
                "mentions": 2, "mentions_total": 10,
                "queries": ["merino wool base layer", "trail running vest"],
                "owned_page": {"title": "Layering 101: Base, Mid, Shell", "slug": "guides/layering-101",
                                "last_modified": "2025-03-18T00:00:00"},
                "sentiment": {"positive": 1, "neutral": 1, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "Layering 101 still earns citations, but mentions dropped "
                     "to 2 of 10 tracked answers as newer competitor guides published this year."},
                    {"label": "Why it matters", "text": "This pillar drives the highest on-site conversion rate of "
                     "any topic — losing AI visibility here costs more per lost mention than elsewhere."},
                    {"label": "Source mechanism", "text": "The page hasn't been updated since March 2025; competing "
                     "guides cite current-season fabric tech that Northwind's guide doesn't mention."},
                ],
                "recommendations": [
                    {"title": "Refresh Layering 101 with current-season fabric technology",
                     "body": "The guide predates this season's fabric releases, which competing cited guides cover. "
                              "A refresh adding current merino blends and synthetic alternatives would restore the "
                              "page's citation relevance without rebuilding it from scratch.",
                     "citation": {"text": "Northwind — Layering 101", "url": "https://northwindoutdoor.com/guides/layering-101"}},
                ],
            },
        ],
    },
    "basecamp": {
        "name": "Basecamp Gear",
        "domain": "basecampgear.com",
        "gsc_site_url": "sc-domain:basecampgear.com",
        "ga4_property": "properties/384712555",
        "semrush_database": "us",
        "cadence": "monthly",
        "ai_brand": "basecamp",
        "industry": "Climbing & mountaineering gear",
        "cms": "webflow",
        "recipients": "marco@basecampgear.com, +1 cc",
        "competitor_brands": [
            {"name": "Northwind Outdoor Co.", "domain": "northwindoutdoor.com"},
            {"name": "TrailForge", "domain": "trailforge.com"},
            {"name": "Summitware", "domain": "summitware.com"},
        ],
        "priority_prompts": [
            "best belay device for a beginner climber?",
            "lightest 60L backpacking pack",
            "what harness certification should I look for?",
        ],
        "priority_keywords": ["climbing harness beginner", "belay device assisted braking", "60l backpacking pack"],
        "competitors": ["northwindoutdoor.com", "trailforge.com", "summitware.com"],
        "top_competitor": {"name": "Northwind Outdoor Co.", "share_of_voice": 0.24, "top_engine": "google_aio"},
        "queries": [
            "climbing harness beginner", "carabiner set aluminum", "60l backpacking pack",
            "sleeping pad r-value", "crampons for hiking boots", "basecamp gear discount code",
            "bouldering crash pad", "ice axe self arrest", "approach shoes review",
            "rope bag climbing", "belay device assisted braking", "backpacking food dehydrated",
        ],
        "keywords": [
            ("climbing harness beginner", 8100), ("carabiner set aluminum", 3200),
            ("60l backpacking pack", 5400), ("sleeping pad r-value", 2900),
            ("crampons for hiking boots", 1600), ("bouldering crash pad", 2200),
            ("ice axe self arrest", 590), ("approach shoes review", 4100),
            ("rope bag climbing", 880), ("belay device assisted braking", 1300),
        ],
        "best_mention": {
            "prompt_text": "best belay device for a beginner climber?",
            "ai_engine": "chatgpt", "position": 1,
            "response_excerpt": "...Basecamp Gear's Halo assisted-braking device is frequently recommended for "
                                 "beginners because of its intuitive lever action and lower price point...",
            "sentiment": "positive", "competitor_brands_mentioned": ["Petzl", "Black Diamond"],
        },
        "citations": [
            ("Assisted-Braking Belay Devices Compared", "guides/belay-devices-compared"),
            ("How to Size a Climbing Harness", "guides/harness-sizing"),
        ],
        "content_published": [
            ("Trad vs Sport Climbing: Gear Differences", "blog/trad-vs-sport-gear", "2026-07-11T09:00:00"),
        ],
        "stale_content": [
            ("Top 5 Crash Pads of 2021", "blog/crash-pads-2021", "2021-09-14T00:00:00"),
            ("Ice Axe Buying Guide (2020)", "blog/ice-axe-guide-2020", "2020-12-01T00:00:00"),
        ],
        "category_pillars": [
            {
                "id": "beginner-safety",
                "pillar": "Safety & Certification Claims",
                "title": "Basecamp leads beginner belay questions, but harness certification detail is missing",
                "mentions": 4, "mentions_total": 10,
                "queries": ["belay device assisted braking", "climbing harness beginner"],
                "owned_page": {"title": "Assisted-Braking Belay Devices Compared", "slug": "guides/belay-devices-compared",
                                "last_modified": "2026-06-10T00:00:00"},
                "sentiment": {"positive": 4, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "Basecamp's Halo belay device is mentioned in 4 of 10 "
                     "answers about beginner-friendly belay gear, all positive."},
                    {"label": "Why it matters", "text": "Safety-adjacent gear questions are high-trust moments — "
                     "an AI engine naming a brand here carries more weight than a generic \"best gear\" list."},
                    {"label": "Competitive contrast", "text": "Petzl and Black Diamond dominate harness-certification "
                     "questions specifically (UIAA/CE standards) — Basecamp isn't cited there at all."},
                    {"label": "Source mechanism", "text": "Citing sources for harness questions lean on "
                     "manufacturer spec sheets — a gap Basecamp's product pages don't currently fill."},
                ],
                "recommendations": [
                    {"title": "Publish UIAA/CE certification details on every harness product page",
                     "body": "Petzl's product pages are cited because they state certification standards and "
                              "test-load figures directly on the page. Basecamp's harness pages currently omit "
                              "this — adding a standardized certification block would make them citable for "
                              "safety-specific prompts.",
                     "citation": {"text": "Petzl — Harness Safety Standards", "url": "https://petzl.com/US/en/Sport/harnesses"}},
                ],
            },
            {
                "id": "weight-packability",
                "pillar": "Weight & Packability",
                "title": "Pack-weight comparisons skip Basecamp's 60L line",
                "mentions": 1, "mentions_total": 10,
                "queries": ["60l backpacking pack", "sleeping pad r-value"],
                "owned_page": None,
                "sentiment": {"positive": 1, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "For \"lightest 60L backpacking pack\" prompts, Basecamp "
                     "appears once, versus Osprey and Gregory appearing in most answers."},
                    {"label": "Source mechanism", "text": "Answers cite a recurring \"pack weight class\" table "
                     "format (base weight, max load, fabric denier) that Basecamp's own pages don't publish."},
                ],
                "recommendations": [
                    {"title": "Add a base-weight comparison table to the 60L pack product page",
                     "body": "Competing product pages state base weight, max recommended load, and fabric denier "
                              "in a scannable table. Publishing the same structured data for Basecamp's 60L line "
                              "gives AI engines a first-party number to cite instead of defaulting to Osprey/Gregory.",
                     "citation": {"text": "Osprey — Pack Weight Comparison", "url": "https://osprey.com/us/en/packweight"}},
                ],
            },
            {
                "id": "winter-technical",
                "pillar": "Winter & Technical Gear",
                "title": "Ice-axe and crampon content is stale and losing citations",
                "mentions": 0, "mentions_total": 10,
                "queries": ["ice axe self arrest", "crampons for hiking boots"],
                "owned_page": {"title": "Ice Axe Buying Guide (2020)", "slug": "blog/ice-axe-guide-2020",
                                "last_modified": "2020-12-01T00:00:00"},
                "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "Basecamp appears in 0 of 10 tracked winter-technical "
                     "answers despite owning a guide on the topic."},
                    {"label": "Source mechanism", "text": "The existing guide dates from 2020 and references "
                     "discontinued products — AI engines favour current guides from Petzl and Black Diamond."},
                ],
                "recommendations": [
                    {"title": "Rewrite the ice-axe guide against the current product line",
                     "body": "The 2020 guide still references discontinued models, which makes it a poor citation "
                              "candidate. A rewrite against the current line, with self-arrest technique detail, "
                              "would make the page competitive for a pillar Basecamp currently forfeits entirely.",
                     "citation": {"text": "Basecamp — Ice Axe Buying Guide (2020)", "url": "https://basecampgear.com/blog/ice-axe-guide-2020"}},
                ],
            },
        ],
    },
    "alpine": {
        "name": "Alpine Supply Co.",
        "domain": "alpinesupply.co",
        "gsc_site_url": "sc-domain:alpinesupply.co",
        "ga4_property": "properties/384712901",
        "semrush_database": "us",
        "cadence": "weekly",
        "ai_brand": "alpine supply",
        "industry": "Ski & snow sports equipment",
        "cms": "contentful",
        "recipients": "jules@alpinesupply.co",
        "competitor_brands": [
            {"name": "TrailForge", "domain": "trailforge.com"},
            {"name": "Northwind Outdoor Co.", "domain": "northwindoutdoor.com"},
            {"name": "BasecampGear", "domain": "basecampgear.com"},
        ],
        "priority_prompts": [
            "best goggles for flat light conditions skiing?",
            "how do I pick backcountry ski boots?",
            "where can I rent an avalanche beacon?",
        ],
        "priority_keywords": ["goggles for flat light", "backcountry ski boots", "ski jacket waterproof rating"],
        "competitors": ["northwindoutdoor.com", "trailforge.com", "basecampgear.com"],
        "top_competitor": {"name": "TrailForge", "share_of_voice": 0.31, "top_engine": "perplexity"},
        "queries": [
            "ski jacket waterproof rating", "snowshoes for deep powder", "thermal base layer women",
            "avalanche beacon rental", "ski touring bindings", "alpine supply co coupon",
            "down mittens extreme cold", "goggles for flat light", "ski pole length chart",
            "backcountry ski boots", "heated socks battery", "gaiters for snowshoeing",
        ],
        "keywords": [
            ("ski jacket waterproof rating", 6700), ("snowshoes for deep powder", 2100),
            ("thermal base layer women", 5900), ("avalanche beacon rental", 880),
            ("ski touring bindings", 3400), ("down mittens extreme cold", 1200),
            ("goggles for flat light", 2600), ("ski pole length chart", 970),
            ("backcountry ski boots", 4300), ("heated socks battery", 1900),
        ],
        "best_mention": {
            "prompt_text": "best goggles for flat light conditions skiing?",
            "ai_engine": "google_aio", "position": 1,
            "response_excerpt": "...Alpine Supply Co.'s Contrast+ lens line is built specifically for flat-light "
                                 "days, with a rose-based tint that several reviewers say outperforms rivals...",
            "sentiment": "positive", "competitor_brands_mentioned": ["Smith", "Oakley"],
        },
        "citations": [
            ("Choosing Ski Goggle Lens Tints", "guides/goggle-lens-tints"),
            ("Avalanche Safety Gear Checklist", "guides/avalanche-safety-checklist"),
        ],
        "content_published": [
            ("Early-Season Snow Report: What to Bring", "blog/early-season-snow-report", "2026-07-16T09:00:00"),
            ("Backcountry Boot Fit Guide", "blog/boot-fit-guide", "2026-07-13T09:00:00"),
            ("Layering for -20F Days", "blog/layering-extreme-cold", "2026-07-09T09:00:00"),
        ],
        "stale_content": [],
        "category_pillars": [
            {
                "id": "flat-light-goggles",
                "pillar": "Lens & Tint Guidance",
                "title": "Alpine Supply owns the flat-light goggle conversation",
                "mentions": 6, "mentions_total": 10,
                "queries": ["goggles for flat light"],
                "owned_page": {"title": "Choosing Ski Goggle Lens Tints", "slug": "guides/goggle-lens-tints",
                                "last_modified": "2026-06-28T00:00:00"},
                "sentiment": {"positive": 6, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "Alpine Supply's Contrast+ lens is named in 6 of 10 "
                     "flat-light-goggle answers, ahead of Smith and Oakley."},
                    {"label": "Why it matters", "text": "Flat-light conditions are a recurring, specific pain "
                     "point — owning this niche question builds durable share of voice, not just one-off mentions."},
                    {"label": "Competitive contrast", "text": "Smith and Oakley are mentioned more often overall, "
                     "but not specifically for flat-light — Alpine Supply's specificity is the edge."},
                    {"label": "Source mechanism", "text": "Citations trace back to Alpine Supply's own lens-tint "
                     "guide — a rare case of a first-party page winning the citation, worth reinforcing."},
                ],
                "recommendations": [
                    {"title": "Expand the lens-tint guide with more condition-specific detail",
                     "body": "The existing guide is already the top-cited source for flat-light lens questions. "
                              "Add sections for other specific conditions (bluebird days, night skiing, mixed "
                              "cloud cover) to extend the same first-party-citation advantage to adjacent queries.",
                     "citation": {"text": "Alpine Supply Co. — Goggle Lens Tint Guide", "url": "https://alpinesupply.co/guides/goggle-lens-tints"}},
                ],
            },
            {
                "id": "avalanche-safety",
                "pillar": "Cold-Weather Safety Gear",
                "title": "Avalanche beacon rental questions favor local shops over Alpine Supply",
                "mentions": 0, "mentions_total": 10,
                "queries": ["avalanche beacon rental"],
                "owned_page": {"title": "Avalanche Safety Gear Checklist", "slug": "guides/avalanche-safety-checklist",
                                "last_modified": "2026-04-02T00:00:00"},
                "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "\"Avalanche beacon rental\" prompts return local gear "
                     "shop chains, not Alpine Supply, in every tracked answer."},
                    {"label": "Source mechanism", "text": "Answers cite location-based rental listings — a "
                     "different intent (rent-nearby) than Alpine Supply's buy-online model, which is likely "
                     "unwinnable without a rental/partner-locator page."},
                ],
                "recommendations": [
                    {"title": "Publish a rental-partner locator page",
                     "body": "AI engines are answering a \"where can I rent this near me\" question, which an "
                              "e-commerce-only site structurally can't win outright. A page listing partner shops "
                              "that rent Alpine Supply-brand beacons would at least make the brand citable inside "
                              "that local-intent answer.",
                     "citation": {"text": "REI — Avalanche Safety Gear Rental", "url": "https://rei.com/rentals/avalanche-safety"}},
                ],
            },
            {
                "id": "boot-fit",
                "pillar": "Boot Fit & Touring Setup",
                "title": "Backcountry boot-fit content is gaining but under-cited",
                "mentions": 2, "mentions_total": 10,
                "queries": ["backcountry ski boots", "ski touring bindings"],
                "owned_page": {"title": "Backcountry Boot Fit Guide", "slug": "blog/boot-fit-guide",
                                "last_modified": "2026-07-13T00:00:00"},
                "sentiment": {"positive": 2, "neutral": 0, "negative": 0},
                "bullets": [
                    {"label": "What's happening", "text": "The newly published boot-fit guide has started earning "
                     "mentions (2 of 10) within weeks of publishing."},
                    {"label": "Why it matters", "text": "Boot fit is the highest-consideration purchase in the "
                     "category — early AI traction here is worth reinforcing before competitors respond."},
                    {"label": "Source mechanism", "text": "Answers cite shell-fit and last-width measurements; the "
                     "guide covers fit process but not per-model measurements."},
                ],
                "recommendations": [
                    {"title": "Add per-model last-width and shell-fit measurements to the boot-fit guide",
                     "body": "The guide explains the fit process well but stops short of the per-model numbers "
                              "AI answers actually cite. Adding a measurements table per boot model would convert "
                              "early traction into a durable citation position.",
                     "citation": {"text": "Alpine Supply — Backcountry Boot Fit Guide", "url": "https://alpinesupply.co/blog/boot-fit-guide"}},
                ],
            },
        ],
    },
}


# ---------- GSC: searchanalytics.query ----------
def gsc_search_analytics(client, dimensions=("query",), start=PERIOD_START, end=PERIOD_END, seed_offset=0):
    random.seed(hash((client["domain"], start, end, dimensions, seed_offset)) % (2**31))
    rows = []
    for q in client["queries"]:
        impressions = random.randint(800, 42000)
        ctr = round(random.uniform(0.01, 0.09), 4)
        clicks = int(impressions * ctr)
        position = round(random.uniform(2.5, 24.0), 1)
        rows.append({"keys": [q], "clicks": clicks, "impressions": impressions,
                     "ctr": ctr, "position": position})
    return {"rows": rows, "responseAggregationType": "byProperty"}


# ---------- GA4: properties.runReport ----------
def ga4_run_report(client, start=PERIOD_START, end=PERIOD_END, seed_offset=0):
    random.seed(hash((client["domain"], start, end, seed_offset, "ga4")) % (2**31))
    sessions = random.randint(18000, 52000)
    conversions = random.randint(300, 1100)
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


def ga4_by_landing_page_group(client, seed_offset=0):
    """GA4 runReport with a landingPage dimension, rolled up to the pillar that owns each page.

    This is what ties AI/search visibility to on-site conversion: each pillar's tracked pages
    contribute the sessions and conversions attributed to that topic.
    """
    random.seed(hash((client["domain"], seed_offset, "ga4group")) % (2**31))
    groups = {}
    for pillar in client["category_pillars"]:
        sessions = random.randint(900, 12000)
        conv_rate = random.uniform(0.008, 0.041)
        conversions = max(int(sessions * conv_rate), 1)
        groups[pillar["id"]] = {
            "sessions": sessions,
            "conversions": conversions,
            "conversion_rate": round(conversions / sessions, 4),
            "revenue": round(conversions * random.uniform(38, 61), 2),
        }
    return groups


# ---------- Semrush: domain_organic ----------
def semrush_domain_organic(client, seed_offset=0):
    random.seed(hash((client["domain"], seed_offset, "domorg")) % (2**31))
    rows = []
    for kw, vol in client["keywords"]:
        po = random.randint(1, 40)
        pp = po + random.randint(-6, 6)
        rows.append({
            "Ph": kw, "Po": po, "Pp": max(pp, 1), "Pd": po - max(pp, 1),
            "Nq": vol, "Cp": round(random.uniform(0.4, 3.2), 2),
            "Ur": f"https://{client['domain']}/{kw.replace(' ', '-')}",
            "Tr": round(random.uniform(0.005, 0.09), 4),
            "Tc": round(vol * random.uniform(0.4, 3.2) * 0.02, 2),
            "Fp": random.choice(["featured_snippet", "ai_overview", "people_also_ask", "none"]),
            "Fk": random.choice([0, 1, 2, 3]),
        })
    return rows


# ---------- Semrush: backlinks_overview ----------
def semrush_backlinks_overview(client, seed_offset=0):
    random.seed(hash((client["domain"], seed_offset, "bl")) % (2**31))
    return {
        "ascore": random.randint(28, 52),
        "total": random.randint(4800, 9200),
        "domains_num": random.randint(310, 640),
        "urls_num": random.randint(2200, 5600),
    }


# ---------- Semrush: Position Tracking (per-competitor) ----------
def semrush_position_tracking(client, seed_offset=0):
    competitors = client["competitors"]
    random.seed(hash((tuple(competitors), seed_offset, "track")) % (2**31))
    visibility = round(random.uniform(0.06, 0.19), 3)
    competitor_rows = [{"domain": c, "visibility": round(random.uniform(0.05, 0.24), 3)} for c in competitors]
    return {"visibility": visibility, "competitors": competitor_rows}


def semrush_competitor_comparison(client, seed_offset=0):
    """Per-competitor traditional-search standing (Position Tracking competitors[] shape).

    Returns our own visibility plus, for each named competitor brand, their SERP visibility,
    tracked-keyword count, and how many of those keywords overlap with ours.
    """
    random.seed(hash((client["domain"], seed_offset, "compcmp")) % (2**31))
    own = {
        "name": client["name"], "domain": client["domain"],
        "visibility": round(random.uniform(0.08, 0.22), 3),
        "keywords_tracked": random.randint(280, 620),
        "avg_position": round(random.uniform(8.0, 19.0), 1),
    }
    rivals = []
    for c in client["competitor_brands"]:
        rivals.append({
            "name": c["name"], "domain": c["domain"],
            "visibility": round(random.uniform(0.05, 0.28), 3),
            "keywords_tracked": random.randint(240, 780),
            "avg_position": round(random.uniform(6.0, 21.0), 1),
            "keyword_overlap": round(random.uniform(0.22, 0.71), 2),
        })
    return {"own": own, "competitors": rivals}


# ---------- Semrush AI: ai_visibility_overview ----------
def semrush_ai_visibility_overview(client, seed_offset=0):
    random.seed(hash((client["ai_brand"], seed_offset, "aivis")) % (2**31))
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
    tc = client["top_competitor"]
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
            {"name": tc["name"], "share_of_voice": tc["share_of_voice"], "change_vs_previous": 0.03,
             "top_engine": tc["top_engine"]},
        ],
    }


def ai_visibility_by_competitor(client, seed_offset=0):
    """Widened ai_visibility_overview.top_competing_brands[] — GEO standing per named competitor."""
    random.seed(hash((client["ai_brand"], seed_offset, "aicomp")) % (2**31))
    rows = []
    for c in client["competitor_brands"]:
        rows.append({
            "name": c["name"], "domain": c["domain"],
            "share_of_voice": round(random.uniform(0.04, 0.31), 3),
            "visibility_score": round(random.uniform(9, 44), 1),
            "mention_rate": round(random.uniform(0.06, 0.38), 3),
            "change_vs_previous": round(random.uniform(-0.05, 0.07), 3),
            "top_engine": random.choice(["chatgpt", "perplexity", "google_aio", "copilot", "claude"]),
        })
    return rows


def semrush_category_share(client, seed_offset=0):
    """Category-wide share of voice across the whole field, not just named competitors.

    Feeds the Category tab header: how much of the category's tracked prompt/keyword space
    this brand holds, versus the named field and the long tail of everyone else.
    """
    random.seed(hash((client["domain"], seed_offset, "catshare")) % (2**31))
    own_share = round(random.uniform(0.06, 0.21), 3)
    named = []
    remaining = 1.0 - own_share
    for c in client["competitor_brands"]:
        s = round(min(remaining * random.uniform(0.12, 0.38), remaining), 3)
        remaining = max(remaining - s, 0)
        named.append({"name": c["name"], "share": s})
    return {
        "category": client["industry"],
        "own_share": own_share,
        "named_competitors": named,
        "long_tail_share": round(max(remaining, 0), 3),
        "total_category_prompts": random.randint(600, 1800),
        "total_category_keywords": random.randint(2400, 9000),
        "own_rank": random.randint(2, 5),
        "brands_tracked": random.randint(9, 24),
    }


def ai_visibility_by_pillar(client, seed_offset=0):
    """Per-pillar GEO standing — the AI half of each Category-tab pillar row.

    visibility_score is derived from the pillar's actual mention rate rather than drawn
    independently, so a pillar with 0 of 10 mentions can never report a healthy score (and
    can never be badged 'winning' against the category average).
    """
    random.seed(hash((client["ai_brand"], seed_offset, "aipillar")) % (2**31))
    out = {}
    for p in client["category_pillars"]:
        mention_rate = p["mentions"] / p["mentions_total"] if p["mentions_total"] else 0
        # Mention rate sets the base; a small jitter keeps the numbers from looking synthetic.
        visibility = mention_rate * 100 * random.uniform(0.62, 0.78)
        out[p["id"]] = {
            "visibility_score": round(max(visibility, 0.0), 1),
            "category_avg_visibility": round(random.uniform(14, 30), 1),
            "mentions": p["mentions"],
            "mentions_total": p["mentions_total"],
        }
    return out


# ---------- Semrush AI: ai_prompt_mentions ----------
def semrush_ai_prompt_mentions(client, seed_offset=0):
    bm = client["best_mention"]
    return {
        "data": [
            {
                "prompt_text": bm["prompt_text"], "ai_engine": bm["ai_engine"], "mentioned": True,
                "position": bm["position"], "response_excerpt": bm["response_excerpt"],
                "sentiment": bm["sentiment"],
                "citation_urls": [f"https://{client['domain']}/"],
                "competitor_brands_mentioned": bm["competitor_brands_mentioned"],
            },
        ]
    }


# ---------- Semrush AI: ai_citation_tracking ----------
def semrush_ai_citation_tracking(client, seed_offset=0):
    random.seed(hash((client["domain"], seed_offset, "aicite")) % (2**31))
    data = []
    for title, slug in client["citations"]:
        data.append({
            "url": f"https://{client['domain']}/{slug}",
            "page_title": title,
            "citations_count": random.randint(5, 60),
            "avg_citation_position": round(random.uniform(1.1, 3.5), 1),
            "change_vs_previous": {"citations_count_delta": random.randint(-5, 22),
                                   "percent_change": round(random.uniform(-0.2, 0.6), 2),
                                   "trend": "positive"},
        })
    return {"data": data}


# ---------- CMS: WordPress posts ----------
def wordpress_list_posts(client):
    return [
        {"id": 4000 + i, "title": {"rendered": title},
         "date": dt, "modified": dt, "status": "publish",
         "link": f"https://{client['domain']}/{slug}", "categories": [12]}
        for i, (title, slug, dt) in enumerate(client["content_published"])
    ]


def wordpress_stale_posts(client):
    return [
        {"id": 2000 + i, "title": {"rendered": title}, "modified": dt,
         "link": f"https://{client['domain']}/{slug}"}
        for i, (title, slug, dt) in enumerate(client["stale_content"])
    ]


# ---------- CMS: Webflow live items ----------
def webflow_list_live_items(client):
    return {
        "items": [
            {"id": f"wf{i:04d}", "cmsLocaleId": "en", "lastPublished": dt, "lastUpdated": dt,
             "isDraft": False, "isArchived": False,
             "fieldData": {"name": title, "slug": slug}}
            for i, (title, slug, dt) in enumerate(client["content_published"])
        ]
    }


# ---------- CMS: Contentful entries ----------
def contentful_entries(client, content_type="guide", limit=10):
    items = []
    for i, (title, slug, dt) in enumerate(client["content_published"]):
        items.append({
            "sys": {"id": f"cf{i:04d}", "contentType": {"sys": {"id": content_type}},
                    "updatedAt": dt, "publishedAt": dt, "version": 4, "revision": 2},
            "fields": {"title": title, "slug": slug},
        })
    return {"total": len(items), "skip": 0, "limit": limit, "items": items}


# ---------- CMS: normalized dispatch ----------
CMS_LABEL = {"wordpress": "WordPress", "webflow": "Webflow", "contentful": "Contentful"}
# Only WordPress exposes a documented write endpoint (POST /wp/v2/posts). Webflow and
# Contentful are read-only in the workbook, so their recommendations produce briefs, not drafts.
CMS_CAN_DRAFT = {"wordpress": True, "webflow": False, "contentful": False}


def cms_list_content(client):
    """Read the client's CMS and return one normalized shape, so downstream code is CMS-agnostic."""
    cms = client["cms"]
    if cms == "wordpress":
        published = [{"title": p["title"]["rendered"], "url": p["link"], "modified": p["modified"]}
                     for p in wordpress_list_posts(client)]
        stale = [{"title": p["title"]["rendered"], "url": p["link"], "modified": p["modified"]}
                 for p in wordpress_stale_posts(client)]
    elif cms == "webflow":
        published = [{"title": it["fieldData"]["name"],
                      "url": f"https://{client['domain']}/{it['fieldData']['slug']}",
                      "modified": it["lastUpdated"]}
                     for it in webflow_list_live_items(client)["items"]]
        stale = [{"title": t, "url": f"https://{client['domain']}/{s}", "modified": d}
                 for t, s, d in client["stale_content"]]
    else:  # contentful
        published = [{"title": it["fields"]["title"],
                      "url": f"https://{client['domain']}/{it['fields']['slug']}",
                      "modified": it["sys"]["updatedAt"]}
                     for it in contentful_entries(client)["items"]]
        stale = [{"title": t, "url": f"https://{client['domain']}/{s}", "modified": d}
                 for t, s, d in client["stale_content"]]
    return {"cms": cms, "label": CMS_LABEL[cms], "can_draft": CMS_CAN_DRAFT[cms],
            "published": published, "stale": stale}
