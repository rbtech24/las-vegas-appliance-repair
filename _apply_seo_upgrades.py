#!/usr/bin/env python3
"""
SEO upgrades for Las Vegas Appliance Repair Pros:
1) Technical: clean URLs, sitemap lastmod, canonical/og fixes
2) Local schema: SAB LocalBusiness + hours/geo/areas (phone stays placeholder)
3) Images: hero/media use real <img> + alt
4) Unique content for all services, brands, areas + expand thin standard pages
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "site_config.json").read_text(encoding="utf-8"))
DOMAIN = CFG["domain"].rstrip("/")
BRAND = CFG["brand"]
PHONE = CFG["phone_display"]
PHONE_RAW = CFG["phone_raw"]
EMAIL = CFG["email"]
CITY = CFG["city"]
STATE = CFG["state"]
TODAY = date.today().isoformat()

SERVICES = [
    ("refrigerator-repair", "Refrigerator Repair", "svc-refrigerator.jpg", "refrigerator"),
    ("freezer-repair", "Freezer Repair", "svc-freezer.jpg", "freezer"),
    ("washer-repair", "Washer Repair", "svc-washer.jpg", "washer"),
    ("dryer-repair", "Dryer Repair", "svc-dryer.jpg", "dryer"),
    ("dishwasher-repair", "Dishwasher Repair", "svc-dishwasher.jpg", "dishwasher"),
    ("oven-range-repair", "Oven & Range Repair", "svc-oven.jpg", "oven"),
    ("cooktop-repair", "Cooktop Repair", "svc-cooktop.jpg", "cooktop"),
    ("microwave-repair", "Microwave Repair", "svc-microwave.jpg", "microwave"),
    ("ice-maker-repair", "Ice Maker Repair", "svc-icemaker.jpg", "ice maker"),
    ("garbage-disposal-repair", "Garbage Disposal Repair", "svc-disposal.jpg", "garbage disposal"),
    ("wine-cooler-repair", "Wine Cooler Repair", "svc-wine.jpg", "wine cooler"),
    ("range-hood-repair", "Range Hood Repair", "svc-hood.jpg", "range hood"),
    ("stackable-laundry-repair", "Stackable Laundry Repair", "svc-stack.jpg", "stackable laundry"),
    ("commercial-appliance-repair", "Light Commercial Repair", "svc-commercial.jpg", "commercial appliance"),
]

BRANDS = [
    ("samsung", "Samsung"), ("lg", "LG"), ("whirlpool", "Whirlpool"), ("ge", "GE"),
    ("ge-profile", "GE Profile"), ("ge-cafe", "GE Café"), ("monogram", "Monogram"),
    ("maytag", "Maytag"), ("kitchenaid", "KitchenAid"), ("bosch", "Bosch"),
    ("frigidaire", "Frigidaire"), ("kenmore", "Kenmore"), ("amana", "Amana"),
    ("hotpoint", "Hotpoint"), ("electrolux", "Electrolux"), ("haier", "Haier"),
    ("fisher-paykel", "Fisher & Paykel"), ("sub-zero", "Sub-Zero"), ("wolf", "Wolf"),
    ("viking", "Viking"), ("thermador", "Thermador"), ("miele", "Miele"),
    ("jennair", "JennAir"), ("dacor", "Dacor"), ("speed-queen", "Speed Queen"),
    ("bertazzoni", "Bertazzoni"), ("blomberg", "Blomberg"), ("beko", "Beko"),
    ("hisense", "Hisense"), ("sharp", "Sharp"), ("panasonic", "Panasonic"),
    ("magic-chef", "Magic Chef"), ("inglis", "Inglis"), ("estate", "Estate"),
    ("roper", "Roper"), ("crosley", "Crosley"), ("admiral", "Admiral"),
    ("galanz", "Galanz"), ("premiere", "Premiere"), ("lg-signature", "LG SIGNATURE"),
]

AREAS = [
    ("summerlin", "Summerlin", "89134–89144 corridors", "west valley master-planned villages"),
    ("west-summerlin", "West Summerlin", "western villages past the 215", "newer smart-home kitchens"),
    ("summerlin-south", "Summerlin South", "south of Charleston", "family + guest-house loads"),
    ("centennial-hills", "Centennial Hills", "northwest growth belt", "builder package appliances"),
    ("spring-valley", "Spring Valley", "central west routes", "dense residential service days"),
    ("paradise", "Paradise", "Strip-adjacent / UNLV side", "condos and townhomes"),
    ("enterprise", "Enterprise", "southwest valley", "new construction warranty age"),
    ("mountains-edge", "Mountains Edge", "far southwest", "high laundry volume homes"),
    ("southern-highlands", "Southern Highlands", "south golf / hillside", "premium cooking packages"),
    ("the-lakes", "The Lakes", "west-central mature tract", "aging first-owner appliances"),
    ("lone-mountain", "Lone Mountain", "northwest foothills", "multi-gen laundry setups"),
    ("north-las-vegas", "North Las Vegas", "NLV citywide", "Aliante-to-downtown coverage"),
    ("downtown-las-vegas", "Downtown Las Vegas", "Arts District / high-rises", "compact appliance layouts"),
    ("whitney", "Whitney", "east valley", "practical same-week windows"),
    ("henderson", "Henderson", "Henderson city routes", "Green Valley through Anthem overflow"),
    ("green-valley", "Green Valley", "central Henderson", "established multi-appliance homes"),
    ("anthem", "Anthem", "south Henderson hills", "estate kitchens and built-ins"),
    ("seven-hills", "Seven Hills", "hillside Henderson", "pro-style ranges and fridges"),
    ("inspirada", "Inspirada", "south master plan", "newer packages past install window"),
    ("chinatown", "Chinatown / Spring Mountain", "Spring Mountain corridor", "multi-family + light commercial"),
    ("sunrise-manor", "Sunrise Manor", "east Las Vegas", "value-focused repair decisions"),
    ("aliante", "Aliante", "north NLV planned community", "route-day clustering"),
    ("skye-canyon", "Skye Canyon", "far northwest new builds", "install callbacks & startup faults"),
    ("providence", "Providence", "northwest villages", "builder-spec laundry pairs"),
    ("red-rock", "Red Rock / west foothills", "scenic west edge", "dusty condenser environments"),
    ("summerlin-centre", "Summerlin Centre", "core Summerlin retail spine", "busy household schedules"),
    ("the-strip-corridor", "The Strip Corridor", "resort-adjacent housing", "condos and short-term rentals"),
    ("boulder-highway", "Boulder Highway Corridor", "southeast arterial", "mixed housing stock"),
]

# ── Unique content libraries ──────────────────────────────────────────────

SERVICE_EXTRA = {
    "refrigerator-repair": {
        "hook": "A warm refrigerator in Las Vegas is an emergency for food safety—especially after 100°F afternoons that already stress condensers coated in desert dust.",
        "symptoms": [
            "Fridge section warm while freezer still cold (or the reverse)",
            "Water pooling under crisper drawers or at the water-filter housing",
            "Clicking compressor, buzzing inverter board, or fan that never shuts off",
            "Ice maker floods, hollow cubes, or zero production after a filter change",
            "Frost wall on the back panel or meat drawer freezing produce",
        ],
        "local": "Valley hard water scales filter heads and valves; garage-placed fridges fight ambient heat that factory ratings never assumed. We test sealed-system pressures when symptoms point beyond a simple defrost heater or evaporator fan.",
        "process": "We verify temperatures with a thermometer, check door gaskets and condenser airflow, pull error history on digital boards, and only open the sealed system when gauges and amp draw justify it.",
        "faqs": [
            ("How long can food stay safe if my fridge dies mid-day?", "Keep doors closed. Perishables above 40°F for more than about two hours become a risk—call for priority when routes allow."),
            ("Do you repair French-door and counter-depth models?", "Yes—Samsung, LG, Whirlpool, GE Profile, and built-in styles including many Sub-Zero service calls."),
            ("Is a sealed-system repair worth it?", "We quote parts and labor before recovery work. Older freestanding units sometimes lose to replacement; built-ins often win on repair."),
        ],
    },
    "freezer-repair": {
        "hook": "Chest and upright freezers in Las Vegas work overtime when outdoor heat soaks garages and laundry rooms—soft freeze and frost bloom are classic summer tickets.",
        "symptoms": [
            "Soft ice cream or thaw-refreeze ice crystals on packages",
            "Lid that won’t seal, warped gasket, or constant run",
            "Thick frost on walls within days of a manual defrost",
            "Compressor clicks but never builds cold",
            "Alarm beeping after power blips from monsoon storms",
        ],
        "local": "Garage freezers see 20–40°F swings between night and afternoon. We check ambient-limit ratings, condenser cleanliness, and whether the unit is fighting a west-facing wall that radiates heat.",
        "process": "Thermistor and control checks first, then sealed-system diagnosis if the evaporator isn’t getting cold. We discuss chest vs upright efficiency before major spend.",
        "faqs": [
            ("Can you fix a freezer that only fails in summer?", "Often yes—dirty condensers, weak start components, or undersized garage placement are common."),
            ("Do you recover refrigerant legally?", "Yes. Sealed-system work uses proper recovery equipment and process."),
        ],
    },
    "washer-repair": {
        "hook": "Las Vegas hard water and sandy dust shorten the life of inlet valves, drain pumps, and bearings—especially on high-efficiency front-loads that sip water.",
        "symptoms": [
            "Won’t drain, spin error, or clothes dripping wet at end of cycle",
            "Door lock won’t release or cycle stuck on sensing",
            "Burning rubber smell, drum wobble, or metal grinding",
            "Over-suds from wrong detergent or residual mold odor",
            "Fills then pauses forever on a board fault",
        ],
        "local": "Mineral scale sticks valves open/closed; laundry rooms without AC bake control boards. We carry common pumps, locks, and shift actuators for valley volume brands.",
        "process": "Error code pull, drain path inspection, spin balance test, and bearing/seal assessment before promising a one-trip fix.",
        "faqs": [
            ("Front-load vs top-load—do you service both?", "Yes, including pedestal models and laundry centers."),
            ("Is a bad bearing a replace decision?", "We quote drum/tub work honestly; sometimes replacement wins on mid-tier units."),
        ],
    },
    "dryer-repair": {
        "hook": "Long dry times here are not always “just a dirty lint trap”—roof vents, long flex runs, and gas igniter wear show up constantly in Summerlin and Henderson homes.",
        "symptoms": [
            "No heat on gas or electric, or heat that cuts out mid-cycle",
            "Takes two to three cycles to dry a normal load",
            "Squealing rollers, thumping drum, or burnt lint smell",
            "Thermal fuse trips repeatedly after a vent clean",
            "Moisture sensor leaves clothes damp on auto cycles",
        ],
        "local": "Attic and roof vents clog with dust and dryer lint faster in desert builds. We inspect airflow before condemning heating elements or gas valves.",
        "process": "Airflow first, then igniter/flame sensor or element/thermistor chain, then mechanical (rollers, belt, idler).",
        "faqs": [
            ("Do you clean dryer vents?", "We clear accessible transitions and advise on roof-cap service when restricted."),
            ("Gas dryer smell—should I shut it off?", "If you smell gas, shut supply and call—safety first, then diagnosis."),
        ],
    },
    "dishwasher-repair": {
        "hook": "Cloudy glasses and grit on plates usually mean hard-water film, a weak wash motor, or a chopper jammed with glass—not “buy new soap.”",
        "symptoms": [
            "Not draining, standing water, or garbage-disposal air-gap spitback",
            "No wash action / quiet hum without spray",
            "Door leaks at bottom corners after a gasket flatten",
            "Error codes for turbidity, heat, or drain",
            "White film that vinegar cycles don’t fully remove",
        ],
        "local": "Softener salt settings and rinse aid matter more here than in soft-water cities. We test heat, spray arms, and inlet valves under real cycle load.",
        "process": "Drain path and disposal knockout check, then wash system, then heat and control. We won’t upsell a new unit until the economics are clear.",
        "faqs": [
            ("Bosch and KitchenAid quiet units?", "Yes—we see European and premium wash systems weekly."),
            ("Is hard water killing my heater?", "It contributes to scale; we inspect and advise filtration/softener tweaks."),
        ],
    },
    "oven-range-repair": {
        "hook": "From builder electric ranges in Centennial Hills to dual-fuel pro ranges in Anthem, no-bake and igniter failures are among our most common kitchen calls.",
        "symptoms": [
            "Bake or broil won’t heat; cooktop still works",
            "Gas click without flame or weak blue flame",
            "Uneven cookies, hot spots, or convection fan noise",
            "Control board blank, F-codes, or clock reset loops",
            "Self-clean door lock stuck after a high-temp cycle",
        ],
        "local": "Self-clean cycles in dusty kitchens stress locks and sensors. We diagnose before another clean attempt melts a weak component.",
        "process": "Element/igniter amp tests, sensor calibration, board communication checks, and gas safety inspection on open-flame systems.",
        "faqs": [
            ("Do you service Wolf and Thermador?", "Yes—pro ranges need correct parts and process; we quote before major modules."),
            ("Electric vs gas?", "Both. Dual-fuel is common in remodels."),
        ],
    },
    "cooktop-repair": {
        "hook": "Induction zones that go dead, glass-top hot spots, and sealed-burner igniters that click forever are fixable more often than big-box return policies imply.",
        "symptoms": [
            "Single burner dead or flashing error on induction",
            "Clicking gas burner that won’t light after a boil-over",
            "Glass cracks—assess only; safety may require top replacement",
            "Knobs spin without spark; spark module failure",
            "Downdraft fan weak on JennAir-style units",
        ],
        "local": "Boil-overs + mineral water leave conductive residue on induction. We clean and test before parts when safe.",
        "process": "Isolate element/inverter vs UI, gas spark path, and safety thermostats. Crack assessments include honesty about replace-only glass tops.",
        "faqs": [
            ("Can a cracked glass cooktop be repaired?", "Usually the glass assembly is replaced as a unit for safety."),
        ],
    },
    "microwave-repair": {
        "hook": "Over-the-range microwaves fail door switches and magnetron circuits after years of steam from valley cooking—door safety is non-negotiable.",
        "symptoms": [
            "Runs but no heat; turntable still spins",
            "Shuts off when the door flexes; multiple door switches",
            "Loud hum, burning smell, or sparking (stop using immediately)",
            "OTR lights or vent fan dead while microwave works",
            "Touchpad unresponsive after a power surge",
        ],
        "local": "We stock common door-switch sets and evaluate whether magnetron work is economical vs replacement on mid-tier OTRs.",
        "process": "Safety-first high-voltage procedures, switch continuity, thermal cutouts, then magnetron/diode chain only when justified.",
        "faqs": [
            ("Is microwave repair safe DIY?", "No—capacitors store lethal charge. Call a tech."),
        ],
    },
    "ice-maker-repair": {
        "hook": "Samsung and LG ice systems dominate our ticket list: hollow cubes, frozen fills, and bucket floods after filter changes.",
        "symptoms": [
            "No ice, small ice, or ice that tastes like freezer air",
            "Water under the fridge after a new filter",
            "Ice room freezes solid in French-door units",
            "Error codes on dual ice makers (door + craft ice)",
            "Slow fill from scaled saddle valves",
        ],
        "local": "Hard water plugs inlet screens; low water pressure from RO systems starves valves. We test supply before condemning the ice mold heater or auger motor.",
        "process": "Harvest cycle observation, thermistor checks, water inlet test into a cup, and optical sensor cleaning on modular units.",
        "faqs": [
            ("Should I replace the whole fridge for ice problems?", "Usually not—ice systems are modular on most brands."),
        ],
    },
    "garbage-disposal-repair": {
        "hook": "Humming disposals after a spoon jam are a five-minute reset—or a motor replacement. We tell you which before you buy a whole new sink suite.",
        "symptoms": [
            "Hum with no grind; jam or failed start capacitor behavior",
            "Leaks at sink flange, dishwasher inlet, or dishwasher tailpiece",
            "Tripped reset button that won’t stay",
            "Loud metal-on-metal after foreign object",
            "Dishwasher won’t drain through disposal knockout",
        ],
        "local": "Hard-water scale and grease from holiday cooking kill units faster. We check plumbing connections to avoid second visits.",
        "process": "Power-off jam clear, amp draw, leak source isolation, flange reseal vs replace decision.",
        "faqs": [
            ("Can you install a replacement disposal?", "Yes—including matching horsepower to your plumbing setup."),
        ],
    },
    "wine-cooler-repair": {
        "hook": "Dual-zone wine units hate garage heat and direct sun through west windows—temperature swings oxidize wine long before the compressor dies completely.",
        "symptoms": [
            "Zone too warm or too cold; compressor short-cycles",
            "Heavy frost on evaporator plate",
            "Fan noise, door seal gaps, UV glass condensation",
            "Control panel errors after power blips",
            "Under-counter units choking on zero cabinet airflow",
        ],
        "local": "We measure actual bottle temps, not just display claims, and verify cabinet ventilation clearances common in Summerlin wet bars.",
        "process": "Sensors and fans first; sealed-system only with clear pressure evidence.",
        "faqs": [
            ("Do you service Sub-Zero wine storage?", "Yes—premium sealed systems quoted after diagnosis."),
        ],
    },
    "range-hood-repair": {
        "hook": "Weak suction isn’t always a bad blower—grease-clogged filters and long duct runs in open-concept remodels strangle airflow.",
        "symptoms": [
            "Fan runs but smoke hangs in the kitchen",
            "Lights dead; fan speeds intermittent",
            "Rattle at high speed; bent blower wheel",
            "Remote or touch controls unresponsive",
            "Makeup-air interlocks on high-CFM installs",
        ],
        "local": "Desert dust mixes with cooking oil into concrete-like filter cake. We clean, then test before parts.",
        "process": "Filter/duct check, motor amp draw, switch and UI diagnosis, duct termination advice.",
        "faqs": [
            ("Island hood vs under-cabinet?", "Both—ducted and recirculating configurations."),
        ],
    },
    "stackable-laundry-repair": {
        "hook": "Condo stacks and laundry centers fail in tight closets that trap heat—boards and motors overheat in ways freestanding garages never see.",
        "symptoms": [
            "Upper dryer won’t heat; lower washer won’t spin",
            "Stack bracket vibration and walking units",
            "Shared power issues or undersized circuits",
            "Door clearance problems after floor settling",
            "Error codes unique to combination units",
        ],
        "local": "High-rise and townhome work needs careful drain routing and quiet-hour awareness. We service LG, Electrolux, GE, and compact European stacks.",
        "process": "Isolate which machine faults, verify electrical share, then standard laundry diagnostics in-place without full unstack when possible.",
        "faqs": [
            ("Do you unstack units?", "When needed for safe repair—we protect floors and reinstall level."),
        ],
    },
    "commercial-appliance-repair": {
        "hook": "Break-room fridges, undercounter freezers, and small ice machines keep offices and cafés running—we focus on light commercial, not full commissary lines.",
        "symptoms": [
            "Undercounter fridge warm by lunch rush",
            "Ice machine short-cycling or scale-bound",
            "Reach-in door gaskets torn; energy waste",
            "Microwave or dishwasher fails health timing",
            "Glass-door merchandisers icing over",
        ],
        "local": "We schedule around business hours when possible and provide invoice detail property managers expect.",
        "process": "Commercial-duty parts when available; clear scope limits if the unit needs a specialist restaurant house.",
        "faqs": [
            ("Full restaurant kitchen lines?", "Light commercial and break rooms are our focus; we refer heavy production equipment when appropriate."),
        ],
    },
}

BRAND_EXTRA = {
    "samsung": ("French-door ice rooms, FlexZone pans, and linear compressors dominate Samsung tickets. We carry common ice auger motors, ethan valves, and main boards after confirming with live voltages—not guesswork from a blinking code alone.",
                ["Ice room freeze-ups on RF* French doors", "Washer vibration / off-balance sensor faults", "Range igniter and Wi-Fi board oddities", "Dryer moisture sensor false “dry”"]),
    "lg": ("LG Linear compressors and Direct Drive washers need brand-aware process. ThinQ error logs help when the panel still talks; sealed-system work is quoted only after amp and pressure evidence.",
           ["Fridge not cooling with Linear compressor codes", "Washer DD motor rotor faults", "Dryer gas valve coils", "Dishwasher heating element errors"]),
    "whirlpool": ("Whirlpool (and related KitchenAid/Maytag architecture) still powers half the valley’s laundry closets. Shift actuators, lid locks, and affinity-style boards are bread-and-butter diagnostics.",
                  ["Washer won’t spin / shift actuator", "Cabrio hub failures", "Fridge adaptive defrost issues", "Range bake element open"]),
    "ge": ("From hotpoint-era electrics to Profile electronics, GE spans decades in Las Vegas rentals and remodels. We bridge old mechanical thermostats and new sensor-driven boards.",
           ["Oven sensor / bake failures", "Fridge dispenser water issues", "Washer mode shifter", "Microwave door switches on OTR units"]),
    "ge-profile": ("Profile French-doors and dual-fuel ranges show up in Summerlin remodels. Ice systems and convection boards need OEM-quality parts for lasting fixes.",
                   ["Twin ice makers", "Dual-fuel ignition", "Advantium related OTR issues", "Washer UltraFresh odors / drain"]),
    "ge-cafe": ("Café matte finishes hide the same electronics as other GE platforms—plus unique UI assemblies. We order finish-matched parts when cosmetics matter.",
                ["Matte fingerprint UI failures", "Fridge Convertible drawers", "Range precision cook probes", "Dishwasher bottle jets clog"]),
    "monogram": ("Monogram built-ins and columns need careful panel work and sealed-system respect. We protect finished surfaces and quote multi-day plans when recovery is required.",
                 ["Column fridge sealed system", "Built-in water valve access", "Pro range modules", "Wine reserve temps"]),
    "maytag": ("Maytag commercial-style laundry is common in rentals. We focus on durable mechanicals—belts, pumps, igniters—before expensive boards.",
               ["Bravos spin problems", "Gas dryer igniters", "Centennial top-load hubs", "Fridge temperature control"]),
    "kitchenaid": ("KitchenAid dishwashers and ranges sit in serious home kitchens. Third rack rails, bottle jets, and dual convection faults are familiar territory.",
                   ["Dishwasher not cleaning upper rack", "Superba fridge issues", "Slide-in range errors", "Ice maker module"]),
    "bosch": ("Bosch quiet dishwashers and Euro laundry need European fastener patterns and drain-path know-how. We don’t force US-only parts when the platform needs the right module.",
              ["Dishwasher drain pump hum", "Axxis washer faults", "Induction cooktop zones", "Benchmark fridge alarms"]),
    "sub-zero": ("Sub-Zero sealed systems are a specialty—gauges, recovery, and dual compressor logic. We diagnose thoroughly before any refrigerant work and protect panel finishes.",
                 ["Refrigerator not cold / sealed system", "Condenser fan failures", "Icemaker on classic models", "Vacuum pump & micron verification"]),
    "wolf": ("Wolf ranges demand correct igniter, spark module, and control board process. Dual-fuel and rangetop units get pro-level checkout, not appliance-flipper shortcuts.",
             ["No bake / igniter", "Charbroiler issues", "Convection fan", "Module communication errors"]),
    "thermador": ("Thermador Freedom induction and steam ovens need brand documentation. We source correct parts and explain when a module is a multi-visit job.",
                  ["Induction zone dropouts", "Steam oven scale faults", "Column refrigeration", "Hood integration switches"]),
    "viking": ("Viking pro ranges and refrigeration need heavy-duty parts and careful gas leak checks. We scope honestly when cosmetics and performance both matter.",
               ["Oven ignition", "Griddle thermostat", "Fridge sealed system", "Outdoor series weather faults"]),
    "miele": ("Miele dishwashers and laundry are engineered for longevity—repairs often beat replacement. We use process that respects waterproof trays and Eco modes.",
              ["Dishwasher fault codes", "Washer drainage", "Cooktop residual heat", "Ventilation issues"]),
    "jennair": ("JennAir downdraft and luxury cooking packages need both appliance and venting insight. We check plenum paths before condemning cooktop electronics.",
                ["Downdraft fan weak", "Induction errors", "Built-in fridge", "Oven control locks"]),
}

# Generic brand filler for long-tail brands
def brand_bits(slug: str, name: str) -> tuple[str, list[str]]:
    if slug in BRAND_EXTRA:
        return BRAND_EXTRA[slug]
    return (
        f"{name} appliances appear across Las Vegas rentals, remodels, and new builds. "
        f"We diagnose {name} kitchen and laundry failures with model-specific literature, not generic guesswork, "
        f"and we quote repair vs replace with valley parts lead times in mind.",
        [
            f"{name} won’t start or complete a cycle",
            f"{name} error codes on the display",
            f"{name} leaks, noise, or temperature problems",
            f"{name} ice, water, or drain path faults",
        ],
    )


AREA_LANDMARKS = {
    "summerlin": ("Red Rock Casino corridor, Downtown Summerlin, and the villages west of the 215",
                  "Master-planned homes mix builder GE/Whirlpool packages with upgraded Sub-Zero and Wolf kitchens in custom estates. Afternoon heat on west exposures cooks garage freezers."),
    "west-summerlin": ("Farther west villages toward the foothills",
                       "Newer construction means more smart appliances and stackable laundry in casitas. Install mistakes from original builders still surface in year 2–5."),
    "summerlin-south": ("South of Charleston toward Rhodes Ranch adjacency",
                        "Busy family loads hammer washers and dryers; many homes run a second fridge in the garage that fights summer heat."),
    "centennial-hills": ("US-95 northwest growth, near Durango & the 215 belt",
                         "New-build packages fail early on ice makers and dishwashers after hard-water exposure. We see a lot of warranty-age boards and valves."),
    "spring-valley": ("Central west of I-15, dense residential grid",
                      "Fast route density means quicker same-day potential. Housing stock ranges from 90s electrics to recent remodels."),
    "paradise": ("Near UNLV / airport / Strip-adjacent housing",
                 "Condos and townhomes need stackable laundry expertise and careful elevator/parking coordination."),
    "enterprise": ("Southwest of the 215, toward Southern Highlands",
                   "Explosive growth = many appliances still under or just past manufacturer warranty. We document for warranty handoffs when applicable."),
    "mountains-edge": ("Far SW master plans",
                       "High laundry volume households; sandy dust loads dryer vents faster. Good candidate for vent + appliance combo advice."),
    "southern-highlands": ("Golf and hillside communities south",
                           "Premium ranges and built-ins are common—expect pro-brand diagnostics and careful finished-surface work."),
    "the-lakes": ("West-central lakes and parks neighborhoods",
                  "Mature appliances from first owners—bearings, igniters, and sealed systems hit end-of-life together."),
    "lone-mountain": ("Northwest foothills",
                      "Multi-generational homes run double laundry. Dusty condensers on fridges pulled away from walls are a pattern."),
    "north-las-vegas": ("City of North Las Vegas",
                        "Wide coverage from Aliante to older NLV tracts—mixed brands and budget repair decisions."),
    "downtown-las-vegas": ("Arts District, Fremont vicinity, high-rises",
                           "Compact kitchens, OTR microwaves, and condo HOA rules. We plan parking and access windows."),
    "whitney": ("East valley residential",
                "Practical repairs preferred over luxury upselling—clear diagnostic fees and honest replace calls."),
    "henderson": ("City of Henderson routes",
                  "We coordinate Green Valley, Anthem, and Seven Hills style calls—premium and standard stock both."),
    "green-valley": ("Central Henderson Green Valley",
                     "Established kitchens with mid-to-premium appliances; dishwashers and French-door fridges lead tickets."),
    "anthem": ("Anthem and Anthem Hills",
               "Estate kitchens, columns, and wine storage—schedule for longer diagnostic windows."),
    "seven-hills": ("Hillside Henderson",
                    "Pro ranges and built-ins; access and driveway grades matter for truck stock planning."),
    "inspirada": ("South Henderson master plan",
                  "Newer homes with builder stainless packages—ice makers and dishwashers after the free install period."),
    "chinatown": ("Spring Mountain corridor",
                  "Multi-family density plus light commercial break-room gear; flexible hours help restaurant-adjacent housing."),
    "sunrise-manor": ("East Las Vegas",
                      "Value laundry and kitchen repairs; we focus on durable fixes that make financial sense."),
    "aliante": ("North NLV Aliante",
                "Planned-community route days keep travel efficient—mention Aliante when booking."),
    "skye-canyon": ("Far NW new construction",
                    "Startup faults, incorrect installs, and first-year board failures—bring model numbers from manuals."),
    "providence": ("NW villages",
                   "Builder laundry pairs and package fridges; hard water shows up early on valves."),
    "red-rock": ("West scenic edge",
                 "Dusty air and elevation breezes dirty condensers; outdoor-adjacent laundry rooms need airflow checks."),
    "summerlin-centre": ("Near Downtown Summerlin retail spine",
                         "Busy professional schedules—we aim for route windows that respect workdays."),
    "the-strip-corridor": ("Resort-adjacent residential",
                           "Short-term rentals and condos: lockboxes, quiet hours, and compact appliances."),
    "boulder-highway": ("SE Boulder Highway corridor",
                        "Mixed housing ages and brands; flexible pricing conversations after diagnosis."),
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def clean_url_html(html: str) -> str:
    """Strip .html from internal hrefs, canonical, og:url (not assets)."""

    def fix_href(m: re.Match) -> str:
        q = m.group(1)
        url = m.group(2)
        if url.startswith("/assets") or url.startswith("http") or "mailto:" in url or "tel:" in url:
            return m.group(0)
        if url.endswith(".html"):
            url = url[:-5]
        return f"href={q}{url}{q}"

    html = re.sub(r'href=(["\'])([^"\']+)\1', fix_href, html)

    def fix_canon(m: re.Match) -> str:
        q = m.group(1)
        url = m.group(2)
        if url.endswith(".html"):
            url = url[:-5]
        # blog trailing
        if url.endswith("/blog/"):
            url = url[:-1]
        return f"{m.group(0)[: m.start(2) - m.start()]}{url}"

    # simpler canonical/og
    html = re.sub(
        r'(href|content)=(["\'])(https://www\.lasvegasappliancerepairpros\.com/[^"\']+?)\.html(\2)',
        r"\1=\2\3\4",
        html,
    )
    html = html.replace(f"{DOMAIN}/blog/", f"{DOMAIN}/blog")
    html = html.replace('href="/blog/"', 'href="/blog"')
    return html


def local_business_schema(include_context: bool = True) -> dict:
    hours = []
    for block in CFG["hours"]:
        for day in block["days"]:
            hours.append(
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": day,
                    "opens": block["opens"],
                    "closes": block["closes"],
                }
            )
    areas = [{"@type": "City", "name": f"{CITY}, {STATE}"}] + [
        {"@type": "Place", "name": f"{name}, {CITY}, {STATE}"} for _, name, *_ in AREAS
    ]
    data = {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{DOMAIN}/#business",
        "name": BRAND,
        "image": f"{DOMAIN}/assets/images/logo.png",
        "logo": f"{DOMAIN}/assets/images/logo.png",
        "url": f"{DOMAIN}/",
        "telephone": PHONE,
        "email": EMAIL,
        "description": f"{BRAND} provides residential and light commercial appliance repair across the Las Vegas Valley. Service-area business — book by phone.",
        "priceRange": CFG["price_range"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": CITY,
            "addressRegion": STATE,
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": CFG["geo"]["latitude"],
            "longitude": CFG["geo"]["longitude"],
        },
        "areaServed": areas,
        "openingHoursSpecification": hours,
        "knowsAbout": [
            "Appliance repair",
            "Refrigerator repair",
            "Washer and dryer repair",
            "Oven and range repair",
            "Dishwasher repair",
        ],
        "currenciesAccepted": "USD",
        "paymentAccepted": "Cash, Credit Card",
    }
    if CFG.get("sameAs"):
        data["sameAs"] = CFG["sameAs"]
    if CFG.get("service_area_business"):
        data["additionalType"] = "https://schema.org/Service"
    if include_context:
        data = {"@context": "https://schema.org", **data}
    return data


def inject_or_replace_schema(html: str, schema_obj: dict | list) -> str:
    block = (
        '<script type="application/ld+json">\n'
        + json.dumps(schema_obj, indent=2)
        + "\n</script>"
    )
    pat = re.compile(r'<script type="application/ld\+json">[\s\S]*?</script>', re.I)
    if pat.search(html):
        html = pat.sub(lambda _m: block, html, count=1)
    else:
        html = html.replace("</head>", block + "\n</head>", 1)
    return html


def breadcrumbs(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def service_unique_html(slug: str, name: str, img: str, kw: str) -> str:
    ex = SERVICE_EXTRA[slug]
    faqs = "".join(
        f"<details class=\"faq-item\"><summary>{esc(q)}</summary><div class=\"faq-a\">{esc(a)}</div></details>"
        for q, a in ex["faqs"]
    )
    sym = "".join(f"<li>{esc(s)}</li>" for s in ex["symptoms"])
    # related
    rel = [s for s in SERVICES if s[0] != slug][:4]
    rel_html = "".join(
        f'<li><a href="/services/{s[0]}">{esc(s[1])}</a></li>' for s in rel
    )
    brands = "".join(
        f'<a class="pill" href="/brands/{b[0]}">{esc(b[1])}</a>' for b in BRANDS[:12]
    )
    areas = "".join(
        f'<a class="pill" href="/areas/{a[0]}">{esc(a[1])}</a>' for a in AREAS[:12]
    )
    return f'''
<section class="page-hero">
  <img class="page-hero-img" src="/assets/images/generated/{img}" alt="{esc(name)} in Las Vegas, NV" width="1400" height="788" fetchpriority="high" />
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="/services">Services</a> / {esc(name)}</div>
    <h1>{esc(name)} in Las Vegas, NV</h1>
    <p>Phone-dispatched diagnostics for {esc(kw)} problems across the Las Vegas Valley.</p>
  </div>
</section>

<section class="section"><div class="container split">
  <article class="prose">
    <p class="lead">{esc(ex["hook"])}</p>
    <p><strong>{esc(BRAND)}</strong> provides professional <strong>{esc(name).lower()}</strong> for homes and light commercial spaces from Summerlin to Henderson and North Las Vegas. Book by phone at <a href="tel:{PHONE_RAW}">{esc(PHONE)}</a> — we do not use website forms.</p>
    <div class="blog-hero-img"><img src="/assets/images/generated/{img}" alt="{esc(name)} technician service Las Vegas" width="1200" height="675" loading="lazy" /></div>
    <h2>Why {esc(kw)} repairs fail more often in the desert</h2>
    <p>{esc(ex["local"])}</p>
    <h2>Common {esc(kw)} symptoms we diagnose</h2>
    <ul>{sym}</ul>
    <h2>How our {esc(name).lower()} visit works</h2>
    <p>{esc(ex["process"])}</p>
    <ol>
      <li>Call with brand, model (if available), neighborhood, and symptoms.</li>
      <li>On-site testing with meters, model literature, and safety checks.</li>
      <li>Clear options: repair now, order parts, or replace when numbers say so.</li>
      <li>Retest under load before we leave whenever parts are installed.</li>
    </ol>
    <h2>Repair vs replace for {esc(kw)} appliances</h2>
    <p>We run the numbers with you: age of the unit, cost of parts, likelihood of cascading failures, and what a comparable replacement costs installed in Las Vegas. Mid-tier freestanding machines sometimes lose to replacement; built-ins, pro ranges, and premium French-door systems often win on repair. You get the math before we order expensive modules.</p>
    <h2>What to have ready when you call</h2>
    <ul>
      <li>Brand and model number (sticker inside the door, on the frame, or behind the kickplate)</li>
      <li>Error codes exactly as displayed</li>
      <li>Neighborhood or ZIP in the Las Vegas Valley</li>
      <li>Gate codes, pets, and parking notes</li>
    </ul>
    <h2>{esc(name)} FAQs</h2>
    <div class="faq-list">{faqs}</div>
    <h2>Brands we repair for this service</h2>
    <div class="pill-row">{brands}</div>
    <p><a href="/brands">All brands</a> · <a href="/pricing">Pricing approach</a></p>
    <h2>Neighborhoods we cover</h2>
    <div class="pill-row">{areas}</div>
    <p><a href="/service-areas">All service areas</a> · <a href="/blog">Repair guides</a></p>
    <h2>Related services</h2>
    <ul class="feature-list">{rel_html}</ul>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call {esc(PHONE)} for {esc(name).lower()}</a></p>
  </article>
  <aside>
    <article class="area-card">
      <div class="media"><img src="/assets/images/generated/{img}" alt="{esc(name)}" width="640" height="400" loading="lazy" /></div>
      <div class="body">
        <h3>Book by phone</h3>
        <p class="muted">Tell us your neighborhood and appliance brand for a faster first visit.</p>
        <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">{esc(PHONE)}</a></p>
        <p style="margin-top:.75rem"><a href="/contact">Contact</a> · <a href="/pricing">Pricing</a></p>
      </div>
    </article>
  </aside>
</div></section>
<section class="cta-band">
  <div class="container">
    <h2>Call {esc(BRAND)}</h2>
    <p>Need {esc(name).lower()} in {esc(CITY)}? We’re ready.</p>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call {esc(PHONE)}</a></p>
  </div>
</section>
'''


def brand_unique_html(slug: str, name: str) -> str:
    blurb, issues = brand_bits(slug, name)
    issues_html = "".join(f"<li>{esc(i)}</li>" for i in issues)
    svcs = "".join(
        f'<a class="pill" href="/services/{s[0]}">{esc(s[1])}</a>' for s in SERVICES[:10]
    )
    img = "brands-hero.jpg"
    return f'''
<section class="page-hero">
  <img class="page-hero-img" src="/assets/images/generated/{img}" alt="{esc(name)} appliance repair Las Vegas" width="1400" height="788" fetchpriority="high" />
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="/brands">Brands</a> / {esc(name)}</div>
    <h1>{esc(name)} Appliance Repair in Las Vegas</h1>
    <p>Factory-aware diagnostics for {esc(name)} kitchen and laundry appliances across the valley.</p>
  </div>
</section>
<section class="section"><div class="container split">
  <article class="prose">
    <p class="lead">Searching for <strong>{esc(name)} repair in Las Vegas</strong>? {esc(BRAND)} services {esc(name)} refrigerators, laundry, cooking appliances, and related units with model-specific process—not one-size-fits-all guessing.</p>
    <p>{esc(blurb)}</p>
    <div class="blog-hero-img"><img src="/assets/images/generated/kitchen.jpg" alt="{esc(name)} kitchen appliances Las Vegas" width="1200" height="675" loading="lazy" /></div>
    <h2>Frequent {esc(name)} issues we see in the valley</h2>
    <ul>{issues_html}</ul>
    <h2>Desert conditions that affect {esc(name)} appliances</h2>
    <p>Hard water scales valves and heaters. Dust blankets condensers behind {esc(name)} fridges pulled tight to the wall. Garage heat pushes compressors past design ambient limits. We check those local factors before recommending sealed-system or major board work.</p>
    <h2>Parts, warranties, and repair vs replace</h2>
    <p>We prefer OEM or OEM-equivalent parts for {esc(name)} platforms when available. After diagnosis we explain labor + parts against replacement cost for your specific model age and condition. No bait pricing—diagnostic clarity first.</p>
    <h2>Services commonly paired with {esc(name)}</h2>
    <div class="pill-row">{svcs}</div>
    <p><a href="/services">All services</a> · <a href="/blog">Guides</a></p>
    <h2>How to book {esc(name)} service</h2>
    <p>Call <a href="tel:{PHONE_RAW}"><strong>{esc(PHONE)}</strong></a> with your model number (usually inside the door or on the frame). We are a phone-first shop—no web forms. Mention your neighborhood for routing.</p>
    <h2>{esc(name)} repair vs replace in Las Vegas</h2>
    <p>Premium {esc(name)} built-ins and recent laundry sets often justify repair. Older freestanding units with multiple failed subsystems may not. After testing we give a plain-language recommendation so you are not guessing from a YouTube video that was filmed in a different climate with different water quality.</p>
    <h2>Areas we serve for {esc(name)} calls</h2>
    <p>From Summerlin and Centennial Hills to Henderson, Green Valley, Enterprise, and North Las Vegas, our routes cover the valley. Same-day availability depends on density—calling early helps.</p>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call {esc(PHONE)} for {esc(name)} repair</a></p>
  </article>
  <aside>
    <article class="area-card">
      <div class="body">
        <h3>{esc(name)} service</h3>
        <p class="muted">Share your model number for faster parts matching.</p>
        <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">{esc(PHONE)}</a></p>
      </div>
    </article>
  </aside>
</div></section>
<section class="cta-band">
  <div class="container">
    <h2>Call {esc(BRAND)}</h2>
    <p>{esc(name)} down in Las Vegas? We’ll take a look.</p>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call {esc(PHONE)}</a></p>
  </div>
</section>
'''


def area_unique_html(slug: str, name: str, zips: str, stock: str) -> str:
    land, detail = AREA_LANDMARKS.get(
        slug,
        (f"{name} area of the Las Vegas Valley", f"We serve residential {name} with phone-dispatched diagnostics."),
    )
    # unique nearby
    idx = next(i for i, a in enumerate(AREAS) if a[0] == slug)
    nearby = [AREAS[(idx + k) % len(AREAS)] for k in (1, 3, 5, 7, 9, 11)]
    near_html = "".join(f'<a class="pill" href="/areas/{a[0]}">{esc(a[1])}</a>' for a in nearby)
    svcs = "".join(
        f'<li><a href="/services/{s[0]}">{esc(s[1])}</a></li>' for s in SERVICES[:8]
    )
    img = "areas-hero.jpg"
    return f'''
<section class="page-hero">
  <img class="page-hero-img" src="/assets/images/generated/{img}" alt="Appliance repair in {esc(name)}, Las Vegas NV" width="1400" height="788" fetchpriority="high" />
  <div class="container">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="/service-areas">Areas</a> / {esc(name)}</div>
    <h1>Appliance Repair in {esc(name)}, Las Vegas NV</h1>
    <p>{esc(stock).capitalize()} — call for diagnostics in {esc(name)}.</p>
  </div>
</section>
<section class="section"><div class="container split">
  <article class="prose">
    <p class="lead"><strong>Appliance repair in {esc(name)}</strong> from {esc(BRAND)}: phone-first booking, clear diagnostics, and techs who know how desert heat and hard water change failure patterns in this part of the valley.</p>
    <p>We regularly run routes near {esc(land)}. {esc(detail)}</p>
    <div class="blog-hero-img"><img src="/assets/images/generated/lifestyle.jpg" alt="Home in {esc(name)} Las Vegas appliance service" width="1200" height="675" loading="lazy" /></div>
    <h2>What {esc(name)} homes typically need</h2>
    <p>Housing here is known for {esc(stock)}. That mix drives tickets for refrigerators, washers, dryers, dishwashers, ovens, and ice makers. Whether you are in a first-owner builder package or a remodeled kitchen, we match parts and process to the platform in front of us.</p>
    <h2>Local service notes for {esc(name)}</h2>
    <ul>
      <li>Mention <strong>{esc(name)}</strong> when you call so dispatch places you on the best route day.</li>
      <li>Corridor / ZIP context: {esc(zips)} — helps us plan travel windows.</li>
      <li>Gate codes, HOA rules, and parking notes save a second trip.</li>
      <li>Garage fridges and west-facing laundry rooms fail more in summer—tell us placement.</li>
    </ul>
    <h2>Appliances we repair in {esc(name)}</h2>
    <ul class="feature-list">{svcs}</ul>
    <p><a href="/services">Full service list</a> · <a href="/brands">Brands</a></p>
    <h2>Why call a local valley tech?</h2>
    <p>National lead-gen sites resell your phone number. We answer as {esc(BRAND)}, quote a diagnostic approach before we roll, and explain repair vs replace without theater. Same-day windows depend on route density—{esc(name)} is on our regular map.</p>
    <h2>Seasonal patterns in {esc(name)}</h2>
    <p>Summer heat spikes garage refrigerator failures and long dryer times. Monsoon humidity and dust storms dirty condensers. Holiday cooking weeks overload dishwashers and ranges. Tell us when the symptom started—timing often points to the failed subsystem faster.</p>
    <h2>Brands we commonly service in {esc(name)}</h2>
    <p>Samsung, LG, Whirlpool, GE, Maytag, KitchenAid, Bosch, and premium lines like Sub-Zero and Wolf all appear on {esc(name)} routes. Bring the model number if you can; it shortens parts matching after diagnosis.</p>
    <h2>Nearby communities</h2>
    <div class="pill-row">{near_html}</div>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call for {esc(name)} service</a></p>
  </article>
  <aside>
    <article class="area-card">
      <div class="body">
        <h3>{esc(name)} booking</h3>
        <p class="muted">Call <a href="tel:{PHONE_RAW}">{esc(PHONE)}</a> — phone only, no forms.</p>
        <p class="price-note">Service-area business serving {esc(name)} and the greater Las Vegas Valley.</p>
      </div>
    </article>
  </aside>
</div></section>
<section class="cta-band">
  <div class="container">
    <h2>Call {esc(BRAND)}</h2>
    <p>Appliance issues in {esc(name)}? Call today.</p>
    <p><a class="btn btn-primary" href="tel:{PHONE_RAW}">Call {esc(PHONE)}</a></p>
  </div>
</section>
'''


def extract_shell(path: Path) -> tuple[str, str]:
    """Return (before_main_inclusive_open_tag handled), use header+footer from file."""
    t = path.read_text(encoding="utf-8")
    # head through <main> open
    i = t.index("<main")
    j = t.index(">", i) + 1
    head = t[:j]
    foot_i = t.index("</main>")
    foot = t[foot_i:]  # includes </main>...
    return head, foot


def rewrite_money_page(path: Path, body_inner: str, title: str, desc: str, canonical: str, schema: dict | list, image: str) -> None:
    head, foot = extract_shell(path)
    # update title/desc/canonical/og in head
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1, flags=re.S)
    head = re.sub(
        r'<meta name="description" content=".*?" />',
        f'<meta name="description" content="{esc(desc[:158])}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<link rel="canonical" href=".*?" />',
        f'<link rel="canonical" href="{esc(canonical)}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="og:title" content=".*?" />',
        f'<meta property="og:title" content="{esc(title)}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="og:description" content=".*?" />',
        f'<meta property="og:description" content="{esc(desc[:158])}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="og:url" content=".*?" />',
        f'<meta property="og:url" content="{esc(canonical)}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta property="og:image" content=".*?" />',
        f'<meta property="og:image" content="{esc(DOMAIN + "/assets/images/generated/" + image)}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta name="twitter:title" content=".*?" />',
        f'<meta name="twitter:title" content="{esc(title)}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta name="twitter:description" content=".*?" />',
        f'<meta name="twitter:description" content="{esc(desc[:158])}" />',
        head,
        count=1,
    )
    head = re.sub(
        r'<meta name="twitter:image" content=".*?" />',
        f'<meta name="twitter:image" content="{esc(DOMAIN + "/assets/images/generated/" + image)}" />',
        head,
        count=1,
    )
    head = inject_or_replace_schema(head, schema)
    head = clean_url_html(head)
    foot = clean_url_html(foot)
    out = head + "\n" + body_inner + "\n" + foot
    # foot still has </main> - body_inner should not include main tags; head ends after <main...>
    # foot starts with </main> - good
    path.write_text(out, encoding="utf-8")


def fix_home() -> None:
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    # hero with img
    html = re.sub(
        r'<section class="hero" style="background-image:url\(\'([^\']+)\'\)">\s*<div class="container hero-content">',
        r'<section class="hero">\n  <img class="hero-img" src="\1" alt="Las Vegas appliance repair — modern kitchen service" width="1400" height="788" fetchpriority="high" />\n  <div class="container hero-content">',
        html,
        count=1,
    )
    # service card media backgrounds -> img
    def card_media(m: re.Match) -> str:
        url = m.group(1)
        return f'<div class="media"><img src="{url}" alt="" width="640" height="400" loading="lazy" /></div>'

    html = re.sub(
        r'<div class="media" style="background-image:url\(\'([^\']+)\'\)"></div>',
        card_media,
        html,
    )
    # improve empty alts later from nearby h3 - simple pass
    def fill_alt(m: re.Match) -> str:
        block = m.group(0)
        title = re.search(r"<h3[^>]*>\s*<a[^>]*>([^<]+)</a>", block)
        if title:
            alt = esc(title.group(1).strip() + " in Las Vegas")
            block = block.replace('alt=""', f'alt="{alt}"', 1)
        return block

    html = re.sub(r'<article class="service-card">[\s\S]*?</article>', fill_alt, html)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            local_business_schema(include_context=False),
            breadcrumbs([("Home", f"{DOMAIN}/")]),
        ],
    }
    html = inject_or_replace_schema(html, schema)
    html = clean_url_html(html)
    # oven keyword on home
    if "oven repair" not in html.lower():
        html = html.replace(
            "ovens, dishwashers, and more",
            "ovens, ranges, dishwashers, and more—including oven repair and cooktop service",
            1,
        )
    path.write_text(html, encoding="utf-8")
    print("home updated")


def expand_about_pricing_contact() -> None:
    # light expansion via injection if short - skip full rewrite; ensure clean urls
    for name in ("about.html", "pricing.html", "contact.html", "faq.html", "brands.html", "services.html", "service-areas.html"):
        p = ROOT / name
        if not p.exists():
            continue
        t = clean_url_html(p.read_text(encoding="utf-8"))
        p.write_text(t, encoding="utf-8")


def patch_all_clean_urls_and_schema() -> None:
    for path in ROOT.rglob("*.html"):
        if path.name.startswith("_"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        # money pages rebuilt separately
        if rel.startswith("services/") or rel.startswith("brands/") or rel.startswith("areas/"):
            continue
        if rel == "index.html":
            continue
        html = path.read_text(encoding="utf-8")
        html = clean_url_html(html)
        # ensure page-hero has img if --hero-img present
        m = re.search(r'class="page-hero"[^>]*style="--hero-img:url\(\'([^\']+)\'\)"', html)
        if m and "page-hero-img" not in html:
            src = m.group(1)
            html = re.sub(
                r'<section class="page-hero"[^>]*>\s*<div class="container">',
                f'<section class="page-hero">\n  <img class="page-hero-img" src="{src}" alt="" width="1400" height="788" />\n  <div class="container">',
                html,
                count=1,
            )
            # alt from h1
            h1 = re.search(r"<h1>([\s\S]*?)</h1>", html)
            if h1:
                alt = esc(re.sub(r"<[^>]+>", "", h1.group(1)).strip())
                html = html.replace('class="page-hero-img" src="'+src+'" alt=""', f'class="page-hero-img" src="{src}" alt="{alt}"', 1)

        # For non-specialized pages, merge LocalBusiness into graph if simple schema
        if rel in ("privacy.html", "terms.html", "contact.html", "about.html", "pricing.html", "faq.html", "services.html", "brands.html", "service-areas.html", "blog/index.html"):
            can = re.search(r'rel="canonical" href="([^"]+)"', html)
            canon = can.group(1) if can else DOMAIN + "/"
            title_m = re.search(r"<title>(.*?)</title>", html, re.S)
            title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else BRAND
            crumbs = [("Home", f"{DOMAIN}/"), (title.split("|")[0].strip()[:40], canon)]
            graph = {
                "@context": "https://schema.org",
                "@graph": [local_business_schema(include_context=False), breadcrumbs(crumbs)],
            }
            html = inject_or_replace_schema(html, graph)

        path.write_text(html, encoding="utf-8")
    print("global clean urls + schema for standard pages")


def rebuild_services_brands_areas() -> None:
    # need a template shell - use about.html
    shell_src = ROOT / "about.html"
    shell = shell_src.read_text(encoding="utf-8")
    # grab head through <main...> and footer from </main>
    i = shell.index("<main")
    j = shell.index(">", i) + 1
    head_template = shell[:j]
    foot = shell[shell.index("</main>"):]
    foot = clean_url_html(foot)
    # fix footer links already cleaned

    def page(title, desc, canon, image, body, schema):
        head = head_template
        head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1, flags=re.S)
        head = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{esc(desc[:158])}" />', head, count=1)
        head = re.sub(r'<link rel="canonical" href=".*?" />', f'<link rel="canonical" href="{esc(canon)}" />', head, count=1)
        for prop, val in [
            ("og:title", title),
            ("og:description", desc[:158]),
            ("og:url", canon),
            ("og:image", f"{DOMAIN}/assets/images/generated/{image}"),
            ("twitter:title", title),
            ("twitter:description", desc[:158]),
            ("twitter:image", f"{DOMAIN}/assets/images/generated/{image}"),
        ]:
            head = re.sub(
                rf'<meta (?:property|name)="{prop}" content=".*?" />',
                f'<meta property="{prop}" content="{esc(val)}" />' if prop.startswith("og:") or prop.startswith("twitter:") and prop != "twitter:card"
                else f'<meta name="{prop}" content="{esc(val)}" />',
                head,
                count=1,
            )
            # fix og vs name - do simpler replacements
        head = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{esc(title)}" />', head, count=1)
        head = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{esc(desc[:158])}" />', head, count=1)
        head = re.sub(r'<meta property="og:url" content=".*?" />', f'<meta property="og:url" content="{esc(canon)}" />', head, count=1)
        head = re.sub(r'<meta property="og:image" content=".*?" />', f'<meta property="og:image" content="{esc(DOMAIN + "/assets/images/generated/" + image)}" />', head, count=1)
        head = re.sub(r'<meta name="twitter:title" content=".*?" />', f'<meta name="twitter:title" content="{esc(title)}" />', head, count=1)
        head = re.sub(r'<meta name="twitter:description" content=".*?" />', f'<meta name="twitter:description" content="{esc(desc[:158])}" />', head, count=1)
        head = re.sub(r'<meta name="twitter:image" content=".*?" />', f'<meta name="twitter:image" content="{esc(DOMAIN + "/assets/images/generated/" + image)}" />', head, count=1)
        head = inject_or_replace_schema(head, schema)
        head = clean_url_html(head)
        return head + "\n" + body + "\n" + foot

    biz = local_business_schema(include_context=False)
    for slug, name, img, kw in SERVICES:
        canon = f"{DOMAIN}/services/{slug}"
        desc = f"{name} in Las Vegas, NV from {BRAND}. Desert-smart diagnostics for {kw} problems. Call {PHONE}."
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "name": name,
                    "serviceType": kw,
                    "description": desc,
                    "url": canon,
                    "provider": {"@id": f"{DOMAIN}/#business"},
                    "areaServed": f"{CITY}, {STATE}",
                },
                biz,
                breadcrumbs([("Home", f"{DOMAIN}/"), ("Services", f"{DOMAIN}/services"), (name, canon)]),
            ],
        }
        body = service_unique_html(slug, name, img, kw)
        (ROOT / "services" / f"{slug}.html").write_text(
            page(f"{name} in Las Vegas, NV | {BRAND}", desc, canon, img, body, schema),
            encoding="utf-8",
        )
    print("services", len(SERVICES))

    for slug, name in BRANDS:
        canon = f"{DOMAIN}/brands/{slug}"
        desc = f"{name} appliance repair in Las Vegas, NV. {BRAND} diagnoses {name} kitchen and laundry failures. Call {PHONE}."
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "name": f"{name} Appliance Repair",
                    "description": desc,
                    "url": canon,
                    "provider": {"@id": f"{DOMAIN}/#business"},
                    "areaServed": f"{CITY}, {STATE}",
                },
                biz,
                breadcrumbs([("Home", f"{DOMAIN}/"), ("Brands", f"{DOMAIN}/brands"), (name, canon)]),
            ],
        }
        body = brand_unique_html(slug, name)
        (ROOT / "brands" / f"{slug}.html").write_text(
            page(f"{name} Appliance Repair Las Vegas | {BRAND}", desc, canon, "brands-hero.jpg", body, schema),
            encoding="utf-8",
        )
    print("brands", len(BRANDS))

    for slug, name, zips, stock in AREAS:
        canon = f"{DOMAIN}/areas/{slug}"
        desc = f"Appliance repair in {name}, Las Vegas NV. {stock.capitalize()}. Call {BRAND} at {PHONE}."
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Service",
                    "name": f"Appliance Repair in {name}",
                    "description": desc,
                    "url": canon,
                    "provider": {"@id": f"{DOMAIN}/#business"},
                    "areaServed": {"@type": "Place", "name": f"{name}, {CITY}, {STATE}"},
                },
                biz,
                breadcrumbs([("Home", f"{DOMAIN}/"), ("Service Areas", f"{DOMAIN}/service-areas"), (name, canon)]),
            ],
        }
        body = area_unique_html(slug, name, zips, stock)
        (ROOT / "areas" / f"{slug}.html").write_text(
            page(f"Appliance Repair in {name}, Las Vegas NV | {BRAND}", desc, canon, "areas-hero.jpg", body, schema),
            encoding="utf-8",
        )
    print("areas", len(AREAS))


def fix_blog_posts_urls() -> None:
    for path in (ROOT / "blog" / "posts").glob("*.html"):
        html = clean_url_html(path.read_text(encoding="utf-8"))
        path.write_text(html, encoding="utf-8")
    bi = ROOT / "blog" / "index.html"
    bi.write_text(clean_url_html(bi.read_text(encoding="utf-8")), encoding="utf-8")
    print("blog urls cleaned")


def rebuild_sitemap() -> None:
    urls = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name.startswith("_"):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "index.html":
            loc = f"{DOMAIN}/"
        elif rel.endswith("/index.html"):
            loc = f"{DOMAIN}/" + rel[: -len("/index.html")]
        elif rel.endswith(".html"):
            loc = f"{DOMAIN}/" + rel[:-5]
        else:
            continue
        if loc.endswith("/blog/"):
            loc = loc[:-1]
        urls.append(loc)
    urls = sorted(set(urls))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        # blogs monthly-ish, money weekly
        freq = "weekly"
        if "/blog/posts/" in u:
            freq = "monthly"
        lines.append(
            f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq></url>"
        )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("sitemap", len(urls))


def update_css() -> None:
    css_path = ROOT / "assets" / "css" / "styles.css"
    css = css_path.read_text(encoding="utf-8")
    extras = """

/* SEO-friendly real images for heroes and cards */
.hero { position: relative; overflow: hidden; background: #081428; }
.hero-img {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: center; z-index: 0;
}
.hero::before { z-index: 1; }
.hero-content { z-index: 2; }

.page-hero { position: relative; overflow: hidden; background: #081428; }
.page-hero-img {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: center; z-index: 0;
}
.page-hero::before {
  content: ""; position: absolute; inset: 0; z-index: 1;
  background: linear-gradient(120deg, rgba(8,18,40,.88), rgba(10,31,68,.62));
}
.page-hero .container { position: relative; z-index: 2; }

.service-card .media, .post-card .media, .brand-card .media, .area-card .media {
  aspect-ratio: 16/10; overflow: hidden; background: #0b1528;
}
.service-card .media img, .post-card .media img, .brand-card .media img, .area-card .media img {
  width: 100%; height: 100%; object-fit: cover; display: block;
}
.blog-hero-img { margin: 1.25rem 0; border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); }
.blog-hero-img img { width: 100%; height: auto; display: block; }
.pill-row { display: flex; flex-wrap: wrap; gap: .45rem; margin: .75rem 0 1rem; }
.pill, .brand-pill {
  display: inline-block; padding: .35rem .7rem; border-radius: 999px;
  border: 1px solid var(--border); background: rgba(244,122,32,.08);
  color: var(--text) !important; font-size: 13px; text-decoration: none !important;
}
.pill:hover, .brand-pill:hover { background: rgba(244,122,32,.18); color: var(--accent) !important; }
.prose .lead { font-size: 1.12rem; color: var(--muted); }
"""
    if "page-hero-img" not in css:
        css += extras
    # remove glow on buttons if still present
    css = css.replace(
        "color:#fff !important; box-shadow: 0 4px 20px rgba(244,122,32,.4);",
        "color:#fff !important; box-shadow: none;",
    )
    css_path.write_text(css, encoding="utf-8")
    print("css updated")


def write_phone_readme() -> None:
    (ROOT / "REPLACE-PHONE.md").write_text(
        f"""# Replace phone before launch

Edit **`site_config.json`**:

```json
"phone_display": "(702) XXX-XXXX",
"phone_raw": "702XXXXXXX"
```

Then run a project-wide replace:

- Display form: `{PHONE}` → your display number  
- Raw/tel form: `{PHONE_RAW}` → digits only  
- Also update `build_lvar_site.py` constants if you regenerate pages  

Add your Google Business Profile URL to `sameAs` in `site_config.json` and re-run schema injection or tell the agent to refresh schema.

**Do not run ads or claim GBP until the real number is live on every page.**
""",
        encoding="utf-8",
    )


def main() -> None:
    update_css()
    fix_home()
    rebuild_services_brands_areas()
    patch_all_clean_urls_and_schema()
    fix_blog_posts_urls()
    expand_about_pricing_contact()
    rebuild_sitemap()
    write_phone_readme()
    # quick stats
    words = []
    for folder, n in [("services", 14), ("brands", 40), ("areas", 28)]:
        for p in (ROOT / folder).glob("*.html"):
            t = p.read_text(encoding="utf-8")
            m = re.search(r"<main[\s\S]*?</main>", t, re.I)
            text = re.sub(r"<[^>]+>", " ", m.group(0) if m else t)
            words.append((p.name, len(re.findall(r"\b\w+\b", text))))
        avg = sum(w for _, w in words[-n:]) / n
        print(f"{folder} avg words≈{avg:.0f}")
    print("done")


if __name__ == "__main__":
    main()
