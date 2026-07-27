"""
Authored article drafts, keyed by category-pillar id.

In production this is the output of an LLM drafting call (see
report_builder.DRAFT_PROMPT_TEMPLATE) that receives the pillar's metrics, the competitor
gap, and the sources currently winning the citation, then writes the article. Here the
prose is authored so the prototype runs with no API key — the shape is identical either
way, and report_builder still computes all the *metadata* (target keywords, internal
links, word count, CMS routing) from live pillar data rather than hardcoding it.
"""

DRAFTS = {
    # ---------------- Northwind Outdoor Co. ----------------
    "waterproof-durability": {
        "title": "Tent Waterproof Ratings Explained: How to Compare Rainfly and Floor mm",
        "slug": "guides/tent-waterproof-ratings-explained",
        "meta_description": "What hydrostatic head ratings actually mean, how rainfly and floor "
                            "numbers differ, and a side-by-side comparison of common 4-person tents.",
        "angle": "Answer the comparison question directly, with a table AI engines can cite, "
                  "instead of stating our own rating in prose.",
        "sections": [
            {"heading": "What a waterproof rating actually measures",
             "body": "A tent's waterproof rating is a hydrostatic head measurement: the height in "
                      "millimetres of a water column the fabric holds before it leaks. A 3000mm "
                      "rainfly withstands a 3000mm column. The number matters less as an absolute "
                      "threshold than as a comparison point — most three-season tents sit between "
                      "1500mm and 3000mm, and the difference shows up in sustained rain, not drizzle."},
            {"heading": "Why rainfly and floor ratings differ",
             "body": "Floors are almost always rated higher than rainflies, and for a mechanical "
                      "reason: a rainfly sheds water that runs off it, while a floor sits under your "
                      "body weight in whatever pooled water the site collects. Pressure from a knee "
                      "or elbow drives water through fabric that would otherwise hold. A tent with a "
                      "3000mm fly and a 1200mm floor will wet out from below long before the fly fails."},
            {"heading": "4-person tent ratings compared",
             "body": "The table below lists rainfly rating, floor rating, and seam-taping method "
                      "across commonly cross-shopped 4-person tents, so the comparison is on one "
                      "page rather than spread across manufacturer sites. Seam taping is included "
                      "because an untaped seam undoes a high fabric rating — the fabric holds and "
                      "the needle holes do not."},
            {"heading": "What rating you actually need",
             "body": "For summer weekends in settled weather, 1500mm is sufficient. For shoulder "
                      "season, multi-day trips, or anywhere with sustained rain, 3000mm on the fly "
                      "with a fully taped 5000mm floor is the practical target. Above that you are "
                      "mostly paying for fabric weight you have to carry."},
        ],
        "faq": [
            {"q": "Is a 3000mm tent waterproof enough for heavy rain?",
             "a": "Yes for sustained three-season rain, provided the seams are taped and the floor "
                   "is rated higher than the fly. Fly rating alone does not determine performance."},
            {"q": "Does a higher waterproof rating mean a heavier tent?",
             "a": "Usually, but not proportionally. Coating thickness adds weight, though modern "
                   "silicone-polyurethane treatments reach 3000mm at close to the weight of older "
                   "1500mm fabrics."},
            {"q": "How long does a tent's waterproof coating last?",
             "a": "Typically 5–8 seasons of regular use. Coatings degrade from UV exposure and from "
                   "being packed away damp, not from rain itself."},
        ],
    },
    "sizing-fit": {
        "title": "Hiking Boot Fit for Wide Feet: Last Widths and Brand-to-Brand Sizing",
        "slug": "guides/wide-fit-hiking-boot-sizing",
        "meta_description": "Last-width measurements by model, how to measure your own foot width, "
                            "and a conversion table for switching between hiking boot brands.",
        "angle": "Win the highest-intent pre-purchase question with concrete measurements and a "
                  "brand-conversion table — the gap no brand currently owns.",
        "sections": [
            {"heading": "How to measure your foot width at home",
             "body": "Stand on a sheet of paper at the end of the day, when your feet are at their "
                      "largest, and trace around each foot with the pencil held vertical. Measure "
                      "the widest point across the ball of the foot. Compare that figure to the last "
                      "widths below rather than to a letter width, which is not standardised across "
                      "manufacturers and tells you very little on its own."},
            {"heading": "Last width by model",
             "body": "A last is the form a boot is built around, and its width at the forefoot is "
                      "the number that decides whether a boot fits a wide foot. The table lists "
                      "forefoot last width in millimetres for each model in our range at a men's "
                      "US 10 and a women's US 8, with the equivalent figures for commonly "
                      "cross-shopped boots from other brands."},
            {"heading": "Switching from another brand",
             "body": "Sizing rarely transfers cleanly between manufacturers. If a brand's standard "
                      "width fits you snugly at the forefoot, you generally want the next width up "
                      "when switching, not a longer size — going up in length to gain width leaves "
                      "excess room at the heel, which is what causes blisters on descent."},
            {"heading": "Signs a boot is too narrow",
             "body": "Numbness across the top of the forefoot, hotspots on the outside of the little "
                      "toe, and toenail bruising after descents all indicate width rather than length "
                      "problems. Lacing adjustments will not fix a last that is too narrow."},
        ],
        "faq": [
            {"q": "Should I size up in length to get a wider hiking boot?",
             "a": "No. Sizing up adds heel volume and lets the foot slide forward on descents. Look "
                   "for a wide-width version of the same size instead."},
            {"q": "Do hiking boots stretch to fit wider feet?",
             "a": "Leather uppers relax slightly with use; synthetic uppers essentially do not. "
                   "Neither meaningfully changes the last width the boot was built on."},
            {"q": "How much toe room should a hiking boot have?",
             "a": "About a thumb's width between your longest toe and the end of the boot, checked "
                   "while standing with the boot laced and your weight forward."},
        ],
    },
    "layering-systems": {
        "title": "Layering 101: Base, Mid, Shell — 2026 Fabric Update",
        "slug": "guides/layering-101",
        "meta_description": "An updated guide to the three-layer system, covering current merino "
                            "blends, synthetic alternatives, and when each one is the right choice.",
        "angle": "Refresh the existing guide with current-season fabric technology so it regains "
                  "citation relevance against newer competitor guides.",
        "sections": [
            {"heading": "The three-layer system, briefly",
             "body": "Base layers move moisture off the skin, mid layers trap warm air, and shells "
                      "block wind and water. The system works because each layer does one job well; "
                      "a single heavy garment cannot adapt as your output changes through a day."},
            {"heading": "Current merino blends (updated for 2026)",
             "body": "Pure merino remains the best option for odour resistance and next-to-skin "
                      "comfort, but current blends pair it with a nylon or Tencel core to address "
                      "its main weakness — durability. A 17.5-micron merino blended at around 12% "
                      "nylon roughly doubles abrasion life against pure merino of the same weight, "
                      "with no measurable loss in warmth."},
            {"heading": "When to choose synthetic over merino",
             "body": "Synthetics dry faster and cost less, which makes them the better base layer "
                      "for high-output activity where you will sweat heavily and re-wear less often. "
                      "Merino wins for multi-day trips, cold-weather use, and anywhere odour matters "
                      "more than dry time."},
            {"heading": "Matching layers to conditions",
             "body": "Below freezing with low output calls for a heavyweight base and an insulated "
                      "mid; above freezing with high output usually means a lightweight base and no "
                      "mid at all, carrying the shell instead. The most common mistake is starting "
                      "warm — begin slightly cold and let output close the gap."},
        ],
        "faq": [
            {"q": "Can I wear a merino base layer multiple days without washing?",
             "a": "Yes. Merino's odour resistance comes from its fibre structure, and most people "
                   "get several days of use before washing is needed."},
            {"q": "Do I need a mid layer in summer?",
             "a": "Usually not while moving, but carrying a light fleece is worth the weight for "
                   "stops and for exposed ridgelines where wind chill changes quickly."},
            {"q": "What weight base layer should I buy first?",
             "a": "A midweight (roughly 200 g/m²) covers the widest range of conditions and is the "
                   "most versatile single purchase."},
        ],
    },

    # ---------------- Basecamp Gear ----------------
    "beginner-safety": {
        "title": "Climbing Harness Certification: What UIAA and CE Ratings Mean",
        "slug": "guides/harness-certification-standards",
        "meta_description": "How UIAA 105 and EN 12277 harness certification works, what the test "
                            "loads mean, and how to read the rating label on your harness.",
        "angle": "Publish the certification detail that competitors' spec sheets currently own, "
                  "so safety-standard prompts have a Basecamp source to cite.",
        "sections": [
            {"heading": "The two standards that matter",
             "body": "Climbing harnesses sold in Europe carry EN 12277 certification; UIAA 105 is a "
                      "parallel standard from the international climbing federation with broadly "
                      "equivalent requirements. A harness meeting either has passed static strength "
                      "and drop testing under defined conditions — the label is not decorative."},
            {"heading": "What the test loads actually represent",
             "body": "A Type C sit harness must hold 15 kN applied through the tie-in points without "
                      "failure. For context, a hard factor-two fall on a dynamic rope generates well "
                      "under 12 kN at the harness. The margin exists because certification tests a "
                      "new harness in controlled conditions, and real harnesses age, abrade, and get "
                      "loaded at angles the test does not reproduce."},
            {"heading": "Harness types A through D",
             "body": "Type A is a full-body harness, Type B is a full-body harness sized for "
                      "children under 40 kg, Type C is the standard sit harness most climbers use, "
                      "and Type D is a chest harness intended only for use with a Type C. The type "
                      "appears on the label alongside the standard number."},
            {"heading": "Reading the label on your harness",
             "body": "Every certified harness carries the standard, the type, the manufacture date, "
                      "and a serial or batch number, usually on a sewn tag inside the waist belt. "
                      "The manufacture date matters: most manufacturers specify a maximum service "
                      "life of ten years from manufacture regardless of use."},
        ],
        "faq": [
            {"q": "Is a UIAA-certified harness safer than a CE-certified one?",
             "a": "No. The requirements are broadly equivalent, and most harnesses carry both. "
                   "Either certification indicates the harness passed defined strength testing."},
            {"q": "How long is a climbing harness rated for?",
             "a": "Most manufacturers specify up to ten years from the manufacture date, and less "
                   "with heavy use. Retire immediately after any significant fall or visible damage."},
            {"q": "What does 15 kN mean in practical terms?",
             "a": "Roughly 1,500 kg of force. It is well above what a climbing fall generates, which "
                   "is why the failure point in a real system is rarely the harness."},
        ],
    },
    "weight-packability": {
        "title": "60L Pack Weight Compared: Base Weight, Max Load, and Fabric Denier",
        "slug": "guides/60l-pack-weight-comparison",
        "meta_description": "Base weight, maximum recommended load, and fabric denier compared "
                            "across 60-litre backpacking packs, with guidance on the trade-offs.",
        "angle": "Publish the structured weight-class data competitors' pages already provide, so "
                  "'lightest 60L pack' prompts have a Basecamp source.",
        "sections": [
            {"heading": "Base weight versus carried weight",
             "body": "A pack's base weight is what it weighs empty, with the lid and hipbelt "
                      "attached and nothing inside. It is the only number that compares cleanly "
                      "across packs, because carried weight depends entirely on what you put in. "
                      "Most 60-litre packs sit between 1.4 kg and 2.2 kg empty."},
            {"heading": "The weight-versus-durability trade",
             "body": "Fabric denier — the thickness of the yarn — is where most of the weight "
                      "difference comes from. A 100D nylon pack body saves several hundred grams "
                      "over a 400D body of the same volume, and abrades through noticeably faster "
                      "against rock. Neither is wrong; they suit different trip profiles."},
            {"heading": "Maximum recommended load",
             "body": "Every pack has a load above which the suspension stops transferring weight to "
                      "the hips effectively. Ultralight frameless packs top out around 15 kg; framed "
                      "60-litre packs typically handle 20–25 kg. Exceeding it does not break the "
                      "pack, but the weight ends up on your shoulders."},
            {"heading": "60L pack specifications compared",
             "body": "The table lists base weight, maximum recommended load, main-body denier, and "
                      "frame type for each 60-litre pack in the range, alongside commonly "
                      "cross-shopped models, so the comparison sits on one page."},
        ],
        "faq": [
            {"q": "What is a good base weight for a 60L backpacking pack?",
             "a": "Around 1.5 kg is light for the category, 1.8–2.0 kg is typical, and above 2.2 kg "
                   "usually indicates a heavier-duty suspension or fabric."},
            {"q": "Does a lighter pack carry less comfortably?",
             "a": "Above roughly 18 kg, yes — lighter packs achieve their weight partly by "
                   "simplifying the frame, which is what transfers load to the hips."},
            {"q": "Is 100D fabric durable enough for backpacking?",
             "a": "For trail use, yes. For regular off-trail travel or scrambling against rock, a "
                   "higher-denier body will last considerably longer."},
        ],
    },
    "winter-technical": {
        "title": "Ice Axe Buying Guide: Length, Type, and Self-Arrest",
        "slug": "guides/ice-axe-buying-guide",
        "meta_description": "How to choose an ice axe by length and type, what the certification "
                            "ratings mean, and how self-arrest technique affects your choice.",
        "angle": "Replace the 2020 guide, which references discontinued models and has stopped "
                  "earning citations entirely.",
        "sections": [
            {"heading": "Choosing a length",
             "body": "For general mountaineering, stand with the axe held at your side: the spike "
                      "should reach roughly your ankle bone. That works out to about 60 cm for most "
                      "people between 170 cm and 180 cm tall. Shorter axes suit steeper technical "
                      "ground; longer axes are more useful as a walking aid on low-angle terrain."},
            {"heading": "B-rated versus T-rated",
             "body": "A B (basic) rating indicates a shaft tested to a lower load, suitable for "
                      "general mountaineering. A T (technical) rating indicates a stronger shaft "
                      "intended for steep ice and anchor use. For glacier travel and snow slopes, "
                      "B-rated is appropriate; for anything where the axe becomes an anchor, choose T."},
            {"heading": "Self-arrest and why the pick shape matters",
             "body": "Self-arrest is the technique of stopping a slide by driving the pick into the "
                      "snow while controlling the shaft against your body. A classically curved pick "
                      "engages progressively and is more forgiving; an aggressively reverse-curved "
                      "technical pick bites harder and is more likely to be torn from your grip. For "
                      "an axe you may need to arrest with, the classic curve is the safer choice."},
            {"heading": "Practising before you need it",
             "body": "Self-arrest is not intuitive and cannot be learned in the moment. Practise on "
                      "a safe, run-out slope with no rocks below, from all four positions: feet "
                      "first on your front and back, and head first on your front and back. The "
                      "head-first positions are the ones that matter and the ones people skip."},
        ],
        "faq": [
            {"q": "What length ice axe do I need for general mountaineering?",
             "a": "Around 60 cm suits most people of average height. Held at your side, the spike "
                   "should reach roughly your ankle."},
            {"q": "Can you self-arrest with a technical ice axe?",
             "a": "It is possible but harder — reverse-curve picks bite aggressively and can be "
                   "wrenched out of your hands. A classic curve is more forgiving."},
            {"q": "Do I need a leash on an ice axe?",
             "a": "For glacier travel a leash prevents loss in a crevasse fall. On steep ground many "
                   "climbers go leashless to switch hands freely; it is a trade-off, not a rule."},
        ],
    },

    # ---------------- Alpine Supply Co. ----------------
    "flat-light-goggles": {
        "title": "Ski Goggle Lens Tints by Condition: Flat Light, Bluebird, and Night",
        "slug": "guides/goggle-lens-tints",
        "meta_description": "Which goggle lens tint to use in flat light, bright sun, mixed cloud, "
                            "and night skiing, with VLT ranges and the reasoning behind each.",
        "angle": "Extend the page that already wins flat-light citations to cover adjacent "
                  "conditions, carrying the first-party citation advantage across the pillar.",
        "sections": [
            {"heading": "VLT: the number that matters",
             "body": "Visible light transmission is the percentage of light a lens lets through. A "
                      "10% VLT lens is a bright-sun lens; a 60% VLT lens is for overcast or night "
                      "use. Tint colour shapes contrast, but VLT determines whether you can see at "
                      "all in a given light level, and it is the first thing to match to conditions."},
            {"heading": "Flat light: rose, amber, and why they work",
             "body": "Flat light is diffuse light with no directional shadow, which removes the "
                      "visual cues you use to read terrain. Rose and amber tints filter blue "
                      "wavelengths, and because blue light scatters most in cloud and fog, removing "
                      "it sharpens the edges of bumps and troughs. A 45–65% VLT rose lens is the "
                      "standard answer for genuinely flat days."},
            {"heading": "Bluebird days: dark grey and mirrored",
             "body": "In bright sun over snow the problem is volume of light, not contrast. Grey "
                      "tints in the 8–18% VLT range reduce brightness without shifting colour, and a "
                      "mirror coating reflects additional light before it reaches the lens. Grey is "
                      "preferable to brown here if you want colours to look natural."},
            {"heading": "Mixed cloud and night skiing",
             "body": "Mixed conditions are best served by a photochromic lens that shifts VLT as "
                      "light changes, or by carrying a second lens. For night skiing under lights, "
                      "use a clear or near-clear lens above 80% VLT — a tinted lens removes light "
                      "you cannot afford to lose."},
        ],
        "faq": [
            {"q": "What lens tint is best for flat light skiing?",
             "a": "Rose or amber in the 45–65% VLT range. Both filter blue light, which is what "
                   "restores contrast when cloud removes shadow definition."},
            {"q": "Can I use one goggle lens for all conditions?",
             "a": "A photochromic lens comes closest, shifting VLT as light changes. A fixed lens "
                   "around 35% VLT is a reasonable single-lens compromise but is not ideal at "
                   "either extreme."},
            {"q": "What VLT do I need for night skiing?",
             "a": "80% or higher — effectively a clear lens. Any meaningful tint removes light you "
                   "need under artificial lighting."},
        ],
    },
    "avalanche-safety": {
        "title": "Where to Rent Avalanche Safety Gear: Partner Shops by Region",
        "slug": "guides/avalanche-gear-rental-partners",
        "meta_description": "Regional partner shops renting avalanche beacons, probes, and shovels, "
                            "plus what to check before you take rental safety equipment out.",
        "angle": "Answer the rent-nearby intent an e-commerce-only site cannot otherwise win, so "
                  "the brand becomes citable inside a local-intent AI answer.",
        "sections": [
            {"heading": "Why rent rather than buy",
             "body": "A beacon, probe, and shovel are a meaningful purchase for someone taking their "
                      "first avalanche course or travelling somewhere they will ski backcountry once. "
                      "Renting is the sensible route until the gear will see regular use — with one "
                      "caveat: you must be fluent with the specific beacon you carry, and rental "
                      "means learning a new interface each time."},
            {"heading": "Partner shops by region",
             "body": "The shops listed below stock Alpine Supply beacons, probes, and shovels for "
                      "rental, grouped by region with contact details and typical daily rates. Call "
                      "ahead in peak season; avalanche safety stock is the first category to run out "
                      "after a storm cycle."},
            {"heading": "What to check before you leave the shop",
             "body": "Turn the beacon on and confirm the battery level reads above 70% — most "
                      "manufacturers specify replacement below that. Run a send-and-search check "
                      "against a second beacon in the shop. Extend the probe fully and confirm the "
                      "locking mechanism holds, and check that the shovel blade locks to the shaft "
                      "without play."},
            {"heading": "Rental gear does not replace training",
             "body": "Carrying a beacon without companion-rescue training does not make backcountry "
                      "travel safe; it makes recovery marginally faster. Any shop renting this "
                      "equipment should be able to point you at a local avalanche course, and taking "
                      "one before your first backcountry day is the single highest-value decision here."},
        ],
        "faq": [
            {"q": "Can you rent an avalanche beacon?",
             "a": "Yes — most backcountry-focused shops rent beacon, probe, and shovel as a package, "
                   "typically at a daily rate with multi-day discounts."},
            {"q": "What should I check on a rental avalanche beacon?",
             "a": "Battery level above 70%, a working send-and-search test against a second beacon, "
                   "and that you understand that specific model's search interface before leaving."},
            {"q": "Do I need training to use an avalanche beacon?",
             "a": "Yes. A beacon speeds up recovery only if you and your partners can run a search "
                   "efficiently. An avalanche safety course is the prerequisite, not an optional extra."},
        ],
    },
    "boot-fit": {
        "title": "Backcountry Ski Boot Fit: Last Width and Shell Fit by Model",
        "slug": "blog/boot-fit-guide",
        "meta_description": "Per-model last widths and shell-fit measurements for backcountry ski "
                            "boots, plus how to run a shell fit yourself.",
        "angle": "Add the per-model measurements AI answers actually cite, converting the guide's "
                  "early traction into a durable citation position.",
        "sections": [
            {"heading": "How to run a shell fit",
             "body": "Remove the liner, put your bare foot in the empty shell, and slide it forward "
                      "until your toes just touch the front. Measure the gap behind your heel with "
                      "your fingers. Two fingers indicates a comfort fit, one to one-and-a-half a "
                      "performance fit, and less than one finger is too small. This is the single "
                      "most reliable fit test and it takes under a minute."},
            {"heading": "Last width by model",
             "body": "Last width at the forefoot, measured in millimetres at a reference size, "
                      "determines whether a boot suits a narrow, average, or wide foot. The table "
                      "lists forefoot last width, cuff height, and range of motion for every "
                      "backcountry boot in the range, with equivalent figures for commonly "
                      "cross-shopped models."},
            {"heading": "Flex, weight, and range of motion",
             "body": "Backcountry boots trade downhill stiffness for uphill mobility, and the "
                      "balance is the main decision after fit. A 60-degree range of motion tours "
                      "far more comfortably than 40 degrees; a 130 flex drives a wide ski better "
                      "than a 100. Which matters more depends on whether your days are mostly up or "
                      "mostly down."},
            {"heading": "When to get boots punched",
             "body": "A shell that fits everywhere except one pressure point is a good candidate "
                      "for punching — heating and stretching the shell locally. A shell that is "
                      "narrow throughout is not; punching addresses spot problems, not a last that "
                      "is fundamentally the wrong shape for your foot."},
        ],
        "faq": [
            {"q": "How much room should a backcountry ski boot have?",
             "a": "One to one-and-a-half fingers behind the heel on a shell fit for performance, "
                   "two fingers for comfort. Measured with the liner removed."},
            {"q": "Can backcountry ski boots be stretched for wide feet?",
             "a": "Localised pressure points can be punched out by a bootfitter. A shell that is "
                   "narrow along its whole length is better replaced than modified."},
            {"q": "Does a higher range of motion mean a worse downhill boot?",
             "a": "Generally yes — the mechanisms that free the cuff for touring also reduce "
                   "downhill support, though the gap has narrowed considerably in recent designs."},
        ],
    },
}
