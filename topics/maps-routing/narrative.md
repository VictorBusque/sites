---
topic: maps-routing
status: built
language: en
source_context: topics/maps-routing/context.md
created: 2026-08-21
updated: 2026-08-22
intended_slug: how-google-maps-routes
---

# The Flood and the Arrow: How a Map Finds Your Route

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article. It teaches a reader who uses a navigation app daily what actually
> happens between tapping origin and destination and seeing a route — the
> graph, the flood, the arrow, the hierarchy, and the re-pricing — with every
> number on the page computed live or cited.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Curious engineers and map users. They know what an app is, roughly what an algorithm is (a recipe), and nothing about graph theory. Words like *vertex* and *heuristic* are introduced on the page. |
| Central question | When you ask a map for the best route, what work happens — and how can it possibly be fast enough at the scale of a continent? |
| One-sentence answer | The map is a graph of intersections and street segments with a price on every segment; a shortest-path search finds the cheapest path, and the only way to make it instant at continental scale is to aim it (A*), exploit the road hierarchy (contraction hierarchies and friends), and precompute an index before you ever ask. |
| Core takeaway | Routing speed comes from search discipline plus preparation: Dijkstra is correct but blind; A* aims the same search with an admissible lower bound; real engines then preprocess the graph so a query touches hundreds of intersections instead of millions — and traffic works because re-pricing edges (not re-doing the world) is what the machinery is built around. |
| Why it matters | It explains why routing is an engineering problem at all (a continent is millions of intersections), why "fastest" ≠ "shortest" (weights are predicted times), and why the answer appears instantly every time. It also shows how to reason honestly about systems whose internals are secret: published science + open engines + a live demo on real data. |
| Scope and exclusions | Teach: graph model, Dijkstra, A* + admissibility, inherent hierarchy, contraction hierarchies (concept + scoreboard), live-traffic re-pricing, the honest boundary (Google's internals unpublished). Exclude: transit/multimodal routing, turn restrictions and costs, matrix APIs, map matching, ETA model internals, hub labels/transit nodes beyond one scoreboard row, Google Base Map data provenance, any claim about what Google runs internally. |
| Narrative point of view | Follow one real route request across one real neighborhood: Barcelona's Eixample, from Carrer de Còrsega to Carrer de Sardenya, on real OpenStreetMap data, computed live in the reader's browser. Zoom out to the continent twice, through cited numbers. |
| Reading language | English. |

### Reader journey

```text
Before: “The app knows the route the way I know my way home — it looks at
         the map and just picks the obvious road.”
Bridge: The map is a priced graph; a search floods it intersection by
        intersection; an aim (a lower bound) collapses the flood; hierarchy
        and preprocessing make a continent touchable; traffic is re-pricing.
After:  “A route request is a shortest-path query against a preprocessed
         graph with predicted-time weights; the engineering is making that
         query cheap — and I watched every count happen.”
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** Over a billion kilometers are driven
  with Google Maps every day. This page rebuilds, in front of you, on a real
  piece of a real city, the machinery any such router stands on — and shows
  why it must be built this way.
- **Ending (1–3 sentences):** A router is a graph with a price on every
  street, a search that never guesses, and hours of preparation done before
  you asked. Google has never published the exact algorithm behind that blue
  line — but every fast router at every scale answers the same way: aim the
  search, honor the hierarchy, precompute what the world will ask. The next
  time the line appears in a blink, you will know exactly what was paid for
  that blink — in advance.

## 2. Evidence and editorial boundaries

Source labels refer to `topics/maps-routing/context.md` [S#]. The page may
only make claims this table supports.

| ID | Claim or datum that may appear | Type | Source | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | “Every day, over 1 billion kilometers are driven with Google Maps in more than 220 countries and territories” | verified (Google's own claim) | [S1] | Oct 2020 blog; attribute “Google says” | Act 0 hook |
| E2 | Google Maps: 2B+ monthly users (Feb 2025) | verified (Google's own claim) | [S3] | attribute | Act 0 |
| E3 | Live traffic from aggregate location data of people navigating; future traffic = ML over live + historical patterns | verified | [S1] | 2020; describe as Google's published description | Act 5 |
| E4 | ETA predictions “consistently accurate for over 97% of trips”; DeepMind GNN partnership cut inaccurate ETAs further (up to 50% in some cities) | verified (Google's own claim) | [S1][S2] | attribute explicitly; Google measuring itself | Act 5 |
| E5 | GNN system: Supersegments built by a route analyzer from terabytes of traffic info; one GNN predicts travel time per Supersegment | verified | [S2] | Sept 2020 | Act 5 |
| E6 | Western Europe benchmark: 18.0M vertices, 42.5M arcs | verified | [S7] §Table 1 context (PTG instance) | 2015 survey run | Act 4 scoreboard |
| E7 | Table 1 rows: Dijkstra 9,326,676 scanned / 2,195,080 µs; Bidir. Dijkstra 4,914,804 / 1,205,660 µs; CRP 2,766 / 1,650 µs; CH 280 / 110 µs, 5 min preprocessing, 0.4 GiB; TNR 2.09 µs; HL 0.56 µs, 18.8 GiB | verified | [S7] Table 1 | single-threaded X5680; travel-time metric | Act 4 scoreboard |
| E8 | “One can compute driving directions in milliseconds or less even at continental scale… fraction of a microsecond… others can deal efficiently with real-time traffic.” | verified quote | [S7] abstract | 2015 | Act 4 |
| E9 | “Sufficiently long shortest paths eventually converge to a small arterial network of important roads” | verified quote | [S7] §2.4 | — | Act 4 |
| E10 | Class-based hierarchy use is “a popular heuristic… no guarantee that it will find exact shortest paths” | verified quote/paraphrase | [S7] §2.4 | — | Act 4 |
| E11 | CH: order nodes by importance computed from actual shortest-path structure; contract least important, adding shortcuts; bidirectional upward query; Geisberger–Sanders–Schultes–Delling WEA 2008 | verified | [S7][S8] | — | Act 4 |
| E12 | Valhalla production hierarchy: level 0 = motorway/trunk/primary (4° tiles), 1 = secondary/tertiary (1°), 2 = residential/service (0.25°) | verified | [S13] | — | Act 4 |
| E13 | Dijkstra 1956 design, 1959 publication; 2001 interview: designed “in about 20 minutes” answering Rotterdam→Groningen | verified anecdote | [S6] | present as documented anecdote | Act 2 intro |
| E14 | A*: Hart, Nilsson, Raphael 1968; admissible (never overestimating) heuristic keeps optimality | verified | [S9] | — | Act 3 |
| E15 | Plain geographic A* on road networks with time metric “performs poorly compared to other modern methods”; ALT strengthens bounds via landmarks | verified | [S7] §2.2 | — | Act 3 close |
| E16 | Offline maps can guide a route as long as the entire route is within the saved area; no traffic/alternatives offline | verified | [S4] | — | Act 6 |
| E17 | OSM database: 10.8B nodes / 1.2B ways (as of 2026-08) | verified | [S12] | dated | Act 1 aside |
| E18 | Google Maps origin: Where 2 Technologies, Sydney, early 2003; acquired Oct 2004; web launch 2005 | verified | [S5] | — | Act 0 aside (optional) |
| E19 | Demo dataset: Eixample extract, © OpenStreetMap contributors (ODbL), fetched 2026-08-21; 1,281 intersections, 1,814 street segments after graph build | verified (artifact of this build) | [S16] | fixed snapshot; counts deterministic | Acts 1–5 |
| E20 | Demo speeds: free-flow km/h per class — primary/secondary 50, tertiary 40, residential 30, living streets 20 | illustrative | narrative decision over [S16] | labeled on page as our illustrative free-flow prices | Acts 1–5 |
| E21 | Computed demo numbers: Dijkstra settles 1,123/1,281; A* settles 311; identical optimal route 3,464 m, 4.38 min, 53 junctions, 85% arterial length; straight line 2,459 m | computed (deterministic from E19+E20; verified offline and reproduced in-browser by identical engine) | `topics/maps-routing/_work/verify.js` | deterministic given dataset | Acts 2–4 |
| E22 | Traffic scenario: Rosselló ×2.5 (illustrative jam) → route abandons Rosselló (1,104 m → 135 m), takes Carrer de València 2,276 m; time 4.38 → 5.87 min; settled 311 → 1,037 | computed (illustrative scenario over real graph) | verify.js | multiplier is illustrative; response is computed | Act 5 |
| E23 | Hierarchy pruning demo: local streets usable only within 400 m of origin/destination → 428 settled, same optimal route *in this demo*; at 250 m no route exists | computed (illustrative model of classical heuristic) | build_graph.py | must be labeled heuristic, contrasted with CH's guarantee (E10, E11) | Act 4 |
| E24 | CRP: customizable metrics — separator overlay, re-weighing for traffic without redoing structure; OSRM ships CH and MLD (traffic-friendly) | verified | [S11][S14] | CRP is Microsoft/Bing work — never imply Google uses it | Act 5 |

### Facts to preserve exactly

- 1B+ km/day, 220+ countries/territories (E1); “over 97% of trips” (E4);
  2B+ monthly users (E2); terabytes of traffic info → Supersegments (E5).
- Western Europe 18.0M/42.5M; all Table 1 numbers as listed in E7; ratios
  shown must be computed in-page from these (arithmetic, not new claims).
- Dijkstra designed 1956, published 1959; the “20 minutes” is a 2001
  interview quote (E13).
- A* 1968 citation (E14); CH 2008 citation, KIT group (E11).
- Valhalla's three levels with road classes (E12).
- OSM counts with date (E17); demo data © OpenStreetMap contributors ODbL
  (E19) — attribution stays on the page.

### Claims to avoid or qualify

- Never state what algorithm Google runs internally. Boundary stated in Act 0
  and Act 6: internals unpublished; we demonstrate the published state of the
  art on open data and open engines.
- Never say CH/TNR/HL is “what Google uses”. CRP attribution: Microsoft
  research, Bing production (E24).
- “Best route” = cheapest under the app's cost model (predicted time,
  directness, road quality — E3); don't reduce to pure distance.
- ETA accuracy is Google's own published claim (E4) — attribute.
- Don't call the demo speeds “real Barcelona speed limits” — they are
  illustrative free-flow prices (E20); page labels them as such.
- Don't present class-pruned hierarchy (E23) as exact — the survey's
  “no guarantee” point must land before CH is presented as the fix.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| graph | intersections and streets reduced to dots and lines with a price on each line | Act 1 |
| vertex / intersection | a dot: a place where streets meet (or end) | Act 1 |
| edge / segment | a line: a stretch of street between two intersections, with a length and a price | Act 1 |
| cost / price | the number minimized — seconds of travel under a price model | Act 1 |
| settle | the moment a search commits a final, provably-cheapest time to one intersection | Act 2 |
| frontier | the settled region's growing boundary | Act 2 |
| heuristic / lower bound | a distance-to-go estimate that never overestimates | Act 3 |
| admissible | never overestimates — the property that keeps A* optimal | Act 3 |
| arterial | the important-road skeleton: primary/secondary streets here, motorways at continental scale | Act 4 |
| contraction | removing an unimportant intersection and bridging its neighbors with a shortcut | Act 4 |
| re-pricing | changing edge costs (traffic) without changing the map's shape | Act 5 |

## 3. Narrative architecture

Rhythm: quiet hook → model reveal → dense flood scene → sharp arrow scene →
quiet breather → dense hierarchy double-beat → metrics scoreboard → pricing
scene → quiet synthesis. Prose carries every conclusion in DOM order.

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | “What am I actually asking the app to do?” | App magically knows → it must compute over structure | Hero + prose: 1B+ km/day; the line appears in a blink; the map is secretly a question about a graph; the honesty contract (Google's internals unpublished; we rebuild the published machinery on a real neighborhood) | Ghost numeral 12; hero copy | none (prose + reveal) | E1 E2 E18 | Plain prose |
| 1 · Mental model | “What does the machine actually see?” | Picture of a city → graph of priced segments | Sticky S01: real Eixample streets → intersections light up as vertices → segments as edges → each gets a price in seconds (illustrative speeds, labeled) → origin and destination marked (Còrsega → Sardenya); routing = cheapest path | One real street morphing from a drawing into two vertices + a priced edge | step states 1–5 over pinned street map | E19 E20 E17 | Steps stack under static map; every count in text |
| 2 · Mechanism | “How does a correct search explore?” | It picks the obvious road → it provably floods | Sticky S02: Dijkstra settles nearest-first; frontier floods with no sense of destination; 1,123/1,281 settled (88%); target settles → route final 3,464 m / 4.4 min; the count is the problem: continental scale (cited: 9.3M scanned, ~2.2 s) | The flood: dots igniting in settle order | steps 1–5; settle-order slices; readout counts | E21 E7 E13 E6 | Stacked steps + text states all counts |
| 3 · Critical detail | “How do you aim a correct search?” | Search is blind by nature → a lower bound aims it | Sticky S03: add h = straight-line ÷ 50 km/h; never overestimates → still optimal; frontier collapses into a corridor; 311 settled vs 1,123 — same route, same 4.4 min; limit: at continental scale geometric A* alone still insufficient (cited) | The arrow: same stage, corridor vs flood silhouette | steps 1–5; both-frontier comparison state | E21 E14 E15 | Stacked steps with counts in text |
| 4 · Change perspective + stress | “How does a continent become touchable?” | Better aiming → different structure: hierarchy | Sticky S04: long routes converge to arterials (quote); class-prune demo (400 m) → 428 settled, same route *here*, no guarantee *in general* → CH computes importance, contracts, shortcuts (mini diagram) → then metrics scene: continental scoreboard (Table 1 rows; computed ratios: ~33,000× fewer scans, ~20,000× faster vs Dijkstra; 5 min preprocessing) | The skeleton: locals dim, arterials glow, then the 3-node contraction diagram | steps 1–5 + metrics block | E9 E10 E11 E23 E7 E8 E12 | Stacked steps; scoreboard is a real `<table>`/text |
| 5 · Weights change | “Where does traffic fit?” | The graph is static → only prices move | Sticky S05: same request; Rosselló ×2.5 (illustrative jam, labeled); route abandons Rosselló for València; 4.38 → 5.87 min; settled 311 → 1,037 (search works harder when prices defy distance); Google's published traffic stack (live crowdsourced + historical + GNN Supersegments; 97% ETA claim attributed); CRP/MLD: machinery built for re-pricing | One street's price flipping, the blue line moving one block | steps 1–5 | E22 E3 E4 E5 E24 | Stacked steps; all numbers in text |
| 6 · Synthesis | “So what is the answer?” | A stack of tricks → one coherent machine | Prose + breather + callout: graph → correct search → aim → hierarchy/preprocessing → live prices; offline fact (the whole graph can live in your pocket); the honest boundary restated; ending promise kept | Big serif synthesis line | none | E16 | Prose |

## 4. Scene specifications

### Common stage contract (applies to S01–S05)

- One shared SVG stage: the embedded Eixample map (all 1,814 segments drawn
  as paths, arterial/tertiary/local stroke classes; viewBox ≈ 3615×1943
  units). Street geometry from the dataset; dots for the 1,281 intersections
  exist once and are reused by every scene.
- All algorithm state is computed once on load by the page's canonical
  engine (binary heap, counter tie-break — identical to the verified offline
  engine) and stored as settle orders, paths, and per-vertex classes; scene
  steps only *select* from that precomputed state (no scroll handlers beyond
  the scaffold runtime's step activation).
- Reduced motion / no JS: each scene keeps its step paragraphs stacked under
  a static stage showing the scene's final or most informative state; all
  counts exist in the step text.
- Mobile (390px): the stage is the full-bleed map recentered per scene via
  per-scene viewBox chosen at build time (label-free geometry, dots ≥ 3px),
  step cards bottom-docked as usual; street-name labels appear ≥ 850px only.
- Settled dots use the house semantic colors: blue = frontier/examined,
  acid = settled/final route, orange = the thing to watch (origin, target,
  jammed street).

### Scene S01 — The city, reduced to a graph

- **Narrative job:** replace “the app sees a picture” with “the router sees
  a priced graph”.
- **Placement:** Act 1; follows hook prose; hands off “now search it”.
- **Pattern:** sticky-scene.
- **Primary visual anchor:** one intersection lighting up as a dot, one
  street collapsing into an edge with a price.
- **Analogy:** none needed — the real thing is on stage. The map *is* the
  analogy target.
- **On-page prose:**
  - Heading: “A map is a graph”
  - Step 1: “This is a real slice of Barcelona — the Eixample — drawn from
    1,814 real street segments. A router doesn't see it as a picture.”
  - Step 2: “It sees intersections: 1,281 places where streets meet or end.
    Every one becomes a vertex.”
  - Step 3: “And it sees street segments: the stretch between two
    intersections. Every one becomes an edge with a length in meters.”
  - Step 4: “Then it prices every edge in seconds — here, free-flow time by
    street class (50 km/h avenues, 40 side, 30 residential, 20 living
    streets; illustrative prices, labeled as such).”
  - Step 5: “Routing is now one question: the cheapest total price from
    origin to destination. Ours: Còrsega → Sardenya, 2,459 m apart as the
    crow flies.”
  - Caption: “What to watch: the drawing dissolving into dots, lines, and
    prices — the only city a router knows.”
- **Stage inventory:** full street layer (decorative, aria-hidden stage),
  intersection dots, one highlighted edge with live price label, O/D pins,
  per-scene header readout `1,281 VERTICES · 1,814 EDGES`.
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | streets only, pins dim | step 1 | map + O/D pins | the real city |
  | 2 | dots appear (fade-in stagger), streets dim | step 2 | 1,281 dots | intersections = vertices |
  | 3 | one example edge highlighted + length label | step 3 | “184 m” chip | segments = edges |
  | 4 | arterial/tertiary/local strokes differentiate + price chip “26 s” | step 4 | class colors | edges are priced |
  | 5 | O pin pulses orange, D ring; readout active | step 5 | O/D labels | the question is set |

- **Motion choreography:** ENTER map fades up; HOLD step 2 dots stagger in
  (50–100ms increments, ≤450ms total); TRANSFORM steps 3–4 highlight swaps
  (150–300ms, --ease-swift); RESOLVE step 5 pins settle with one ping echo;
  ambient: faint grid drift only.
- **Data / computation:** counts are dataset facts (E19); example edge
  length/price computed at load from the dataset; class speeds E20 shown in
  a chip; all displayed in DM Mono.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** stage aria-hidden; step text carries all
  counts; no-JS: static final state (step-5 look) above stacked steps.
- **Responsive rules:** labels drop below 850px; map recentered to route
  corridor; dots ≥ 3px; price chip moves into a fixed slot top-right.
- **Acceptance check:** with JS off, the article still shows the map, and the
  step paragraphs state 1,281/1,814/2,459 m.

### Scene S02 — Dijkstra's flood

- **Narrative job:** show what *correct* costs: the search provably floods,
  indifferent to destination — and that the flood, not the math, is the
  problem at scale.
- **Placement:** Act 2; follows Dijkstra prose (1956/1959 + 20-minute
  anecdote quote, E13); hands off “aim it”.
- **Pattern:** sticky-scene.
- **Primary visual anchor:** the frontier — dots igniting blue then dimming
  to settled, ring by ring, around the origin.
- **Analogy:** ripples on water from the origin — mapping is exact (nearest
  first, settle order is by price); limit stated: ripples have no direction
  preference, and neither does this search.
- **On-page prose:**
  - Heading: “Dijkstra's flood”
  - Step 1: “Start at Còrsega. Hold every other intersection at infinity;
    the origin costs zero. Settle the cheapest unsettled intersection,
    always.”
  - Step 2: “Settling an intersection is final: its price can never improve.
    Each settle re-prices its neighbors — that's the whole algorithm.”
  - Step 3: “Watch it ignore the destination. The flood grows by *price*,
    in every direction — backwards, sideways, away.”
  - Step 4: “To reach Sardenya it settles 1,123 of 1,281 intersections —
    88% of the neighborhood — for one question.”
  - Step 5: “When Sardenya finally settles, its price is provably minimal:
    3,464 m, 4.4 minutes. Correct — and hopeless at continental scale: on an
    18-million-vertex Europe, the same flood scans 9.3 million vertices per
    query.”
  - Caption: “What to watch: the blue ring — the frontier — always growing
    where the city is cheapest, never where you're going.”
- **Stage inventory:** street layer at low opacity; settle dots (blue → dim);
  route polyline hidden until step 5 (acid); live readout
  `SETTLED n / 1281`; small counter chip.
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | O dot only | step 1 | readout 0/1,281 | initialization |
  | 2 | settle order slice ~30% | step 2 | readout ~377 | nearest-first growth |
  | 3 | slice ~70%, frontier ring emphasized | step 3 | readout ~800 | blind growth |
  | 4 | slice 100% minus D unset… full 1,123 | step 4 | readout 1,123 | the cost of correctness |
  | 5 | route polyline + D ping | step 5 | `3,464 M · 4.4 MIN` | final, provable |

  (Exact slice percentages chosen at build from the real settle order; the
  step-4 count is exact.)
- **Motion choreography:** dots appear in settle order within a step using
  short staggered transitions (150–250ms each, capped duration); frontier
  dots pulse once; route draws as stroke-dashoffset in 700ms on step 5 with
  one settling ping on D. Reverse scroll must replay slices exactly
  (state-selected, not animation-dependent).
- **Data / computation:** settle order from the canonical engine (E21);
  slice sizes computed from it; readout text bound to actual counts.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** counts in step text; no-JS static state =
  full flood + route visible; aria-hidden stage.
- **Responsive rules:** recentered corridor viewBox on mobile; readout chip
  10px minimum.
- **Acceptance check:** readout numbers match E21 exactly at steps 4–5.

### Scene S03 — The arrow (A*)

- **Narrative job:** show that a never-overestimating estimate aims the same
  correct search — and what aiming can and cannot fix.
- **Placement:** Act 3; hands off “structure beats aiming”.
- **Pattern:** sticky-scene (same stage).
- **Primary visual anchor:** the corridor — A*'s settled set drawn over the
  ghost of Dijkstra's flood.
- **Analogy:** a heat-seeking vs flood — mapping: h adds a
  distance-to-go bias to the queue order; limit: h must never overestimate
  or optimality is lost (that's why it's ÷ fastest speed, not a guess).
- **On-page prose:**
  - Heading: “Aim the search”
  - Step 1: “Keep Dijkstra exactly. Add one number per intersection: a lower
    bound on time-to-go — straight-line distance ÷ 50 km/h, the fastest
    price on this map. The result is A*, 1968.”
  - Step 2: “A lower bound can't lie upward: the queue now prefers
    intersections that make *progress* toward Sardenya.”
  - Step 3: “The flood collapses into a corridor. Behind, the ghost of the
    old flood — everything Dijkstra examined and A* never touched.”
  - Step 4: “311 settled instead of 1,123 — 3.6× less work — and the route
    is identical: 3,464 m, 4.4 minutes. Never-overestimating keeps it
    provably optimal.”
  - Step 5: “Aiming helps, but a corridor still widens with distance: across
    a continent, geometric bounds alone leave millions of intersections in
    the search. The next idea changes the map itself.”
  - Caption: “What to watch: the same city, the same answer — the search
    space is what changed.”
- **Stage inventory:** A* settle dots (blue), Dijkstra ghost dots (dim
  outline), corridor emphasis, route acid, readout
  `A* SETTLED n · DIJKSTRA 1,123`.
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | formula chip `h = ∆ / 50 km/h` beside O | step 1 | chip | the bound |
  | 2 | A* slice ~35% | step 2 | readout ~110 | aimed growth |
  | 3 | Dijkstra ghost appears underneath | step 3 | two layers | what aiming saves |
  | 4 | full 311 + ratio chip `3.6×` | step 4 | readout 311 vs 1,123 | the payoff |
  | 5 | zoom-out breath: ghost + corridor full | step 5 | continent caption | limits of aiming |

- **Motion choreography:** ghost layer fades to 18% opacity (600ms);
  corridor dots stagger in; ratio chip pop; no long-running animation.
- **Data / computation:** all counts engine-computed (E21).
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** all numbers in step text; static state =
  both layers + route.
- **Responsive rules:** as S02; formula chip wraps above stage on mobile.
- **Acceptance check:** readout shows 311 vs 1,123; route identical to S02's.

### Scene S04 — The skeleton (hierarchy → contraction)

- **Narrative job:** move from “search smarter” to “prepare the map”:
  inherent hierarchy, its classical heuristic and its lack of guarantee,
  then CH as the computed-importance fix.
- **Placement:** Act 4; follows breather; hands off scoreboard metrics.
- **Pattern:** sticky-scene + companion metrics block.
- **Primary visual anchor:** locals dimming, arterial skeleton glowing, and
  the 3-node contraction diagram (u—v—w becomes u——w with a shortcut).
- **Analogy:** motorways as the highway system's trunk — mapping: long
  optimal paths converge onto the arterial subgraph (E9); limit: road *class*
  is a human label, not a proof (E10) — CH derives importance from actual
  shortest paths instead.
- **On-page prose:**
  - Heading: “The map has a skeleton”
  - Step 1: “Look at our own optimal route: 85% of its length is arterial.
    Long routes converge onto important roads — it's why they exist.”
  - Step 2: “Production routers exploit this openly: Valhalla keeps three
    levels — motorway/primary, secondary/tertiary, residential — and searches
    the coarse level first.”
  - Step 3: “Model it here: keep local streets only within 400 m of origin
    and destination. The search settles 428 intersections instead of 1,123 —
    and still finds the same optimal route *in this demo*. But pruning by
    road class has no correctness guarantee in general.”
  - Step 4: “Contraction Hierarchies get importance the honest way: compute
    it from the map's own shortest paths, then contract unimportant
    intersections — remove them, bridge neighbors with a shortcut.”
  - Step 5: “A query then searches upward: local streets until the arterial
    skeleton, across the skeleton, down at the destination. Hundreds of
    settled intersections at continental scale — see the scoreboard.”
  - Caption: “What to watch: the skeleton survive while the local grid dims;
    then one intersection vanish into a shortcut.”
- **Stage inventory:** class-dimmed local layer, arterial glow, prune-radius
  rings at O and D (400 m), settle dots under pruning (428), inset
  contraction diagram (u—v—w → u——w) as an SVG mini-panel, readout
  `SETTLED 428 · PRUNE 400 M`.
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | route shown, arterial share chip 85% | step 1 | chip | routes use the skeleton |
  | 2 | Valhalla level chips over map (L0/L1/L2 legend) | step 2 | legend | production precedent |
  | 3 | locals dim except two 400 m rings; pruned settle dots 428 | step 3 | readout 428 | heuristic + its caveat |
  | 4 | inset diagram animates contraction | step 4 | u—v—w → u——w | CH's mechanism |
  | 5 | arrow path up-across-down along skeleton | step 5 | 3-phase route | the query shape |

- **Motion choreography:** dimming 400ms; rings draw 600ms; contraction
  inset: middle node shrinks while shortcut line draws (500ms, swift);
  skeleton route pulses once.
- **Data / computation:** 85% share, 428 settled, 400 m radius all computed
  (E21, E23); CH inset is a labeled mechanism diagram (no data).
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** step 3/5 text carries 428 and the caveat;
  inset duplicated as text: “remove v; add shortcut u→w when v lay on their
  shortest path”.
- **Responsive rules:** inset moves below stage on mobile; rings stay
  visible at 390px.
- **Acceptance check:** readout 428 at step 3; no text claims guarantee.

### Scene S05 — The price of a street (traffic)

- **Narrative job:** the graph is fixed, the prices are not: re-pricing is
  how traffic enters the same machinery; and the system is built for it.
- **Placement:** Act 5; hands off synthesis.
- **Pattern:** sticky-scene.
- **Primary visual anchor:** Rosselló's price chip flipping, the blue line
  sliding one block south to València.
- **Analogy:** surge pricing on a road — mapping: multiplier on edge time;
  limit: our ×2.5 is illustrative; Google's real prices are predicted by ML.
- **On-page prose:**
  - Heading: “Traffic is a new price list”
  - Step 1: “Same graph, same request. Now the main street of our route —
    Carrer del Rosselló, 1,104 m of it — jams. We model it as ×2.5 on its
    free-flow price (an illustrative jam).”
  - Step 2: “The search doesn't rerun the world; it reads the same graph
    with new numbers. The old route now costs 5.9 minutes.”
  - Step 3: “So the line moves: the route abandons Rosselló (1,104 m →
    135 m) and takes Carrer de València, one block south — 2,276 m of it.
    Best answer, re-derived.”
  - Step 4: “Notice the search itself worked harder: 1,037 settled instead
    of 311 — defied prices make aiming weaker. Real systems precompute
    re-priceable structures for exactly this (CRP; OSRM's MLD).”
  - Step 5: “And where do prices come from? Google says: aggregate location
    data of people driving, historical patterns, and a graph neural network
    over “Supersegments” — terabytes in, seconds out; its ETAs are right on
    over 97% of trips, by its own measurement.”
  - Caption: “What to watch: the jammed street's price, then the route
    quietly stepping around it.”
- **Stage inventory:** Rosselló highlighted orange with price chip
  `26 s → 66 s` per segment class avg (computed), old route ghost, new route
  acid, readout `SETTLED 1,037 · 5.9 MIN`.
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Rosselló orange + ×2.5 chip | step 1 | chip | the jam |
  | 2 | old route ghosted with 5.9 min chip | step 2 | chip | old answer, new price |
  | 3 | new route draws via València | step 3 | line move | re-derivation |
  | 4 | settle layer 1,037 shown | step 4 | readout | work shifts too |
  | 5 | chips: live + history + GNN | step 5 | 3 chips | production stack |

- **Motion choreography:** price chip flip (200ms), route slide (700ms,
  ease-out), ghost fade (400ms); reverse-safe.
- **Data / computation:** scenario computed at load by the same engine
  (E22); every displayed number engine-written.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** both routes' streets and both totals in
  step text; static state = new route + jam chip.
- **Responsive rules:** chips stack; corridor viewBox; labels ≥ 8px.
- **Acceptance check:** 4.38 → 5.87 min and 311 → 1,037 appear in readouts
  and text; multiplier visibly labeled illustrative.

### Scene S06 — Scoreboard (metrics)

- **Narrative job:** make continental scale concrete: one benchmark, one
  table, computed ratios.
- **Placement:** Act 4/5 hinge (after S04, before S05); pattern: metrics.
- **Primary visual anchor:** `9,326,696 → 280` as Instrument Serif numerals.
- **On-page prose:** heading “One continent, one benchmark”; body: Western
  Europe, 18.0M vertices / 42.5M arcs; per-query averages from the 2015
  survey's Table 1: Dijkstra 9,326,676 scanned, ~2.2 s; bidirectional
  4,914,804, ~1.2 s; CH 280 scanned, 110 µs after 5 minutes of
  preprocessing; HL 0.56 µs (18.8 GiB). Ratios computed in-page:
  scan ratio ≈ 33,310×; time ratio ≈ 19,955×.
- **Data / computation:** table rows are cited E7; ratio chips computed by
  the page script from those literals.
- **Fallback:** a real HTML table (works no-JS); ratios also stated in text.

### Scene S07 — Breather

- Between S03 and S04: masked serif line — “Correct was never the problem.
  Fast was.” Plain stacked text fallback.

## 5. Visual direction

### Chosen aesthetic

- **Named style (as built, revised 2026-08-22):** the Google Maps skin —
  the article wears its subject. Light map canvases (#f1f3f4) with white
  roads and classic Maps-yellow arterials, the Maps-blue route line, a red
  destination pin and blue origin dot, traffic-red jams, Roboto + Roboto
  Mono on white Material cards. (First build used the house dark
  instrument-panel map room; it read too close to the QR post's blueprint
  stages, so the skin was replaced before the redesign shipped.)
- **Why it fits:** the subject is a navigation app; dressing the explainer
  in the app's own visual language makes every state instantly legible and
  one of a kind on the shelf.
- **Emotional register:** calm, precise, quietly amazed at scale.
- **Avoid:** skeuomorphic road textures, 3D tilts, satellite imagery,
  decorative vehicles, fake UI chrome that implies product features the
  data cannot support.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | House paper for prose; `--stage #121212` map rooms; map streets `#ffffff14–2a`; arterial slightly warmer `#ffffff30` |
| Palette semantics | acid = settled/route/final; blue = frontier/examined; orange = origin/target/jam (the watch); muted greys = past/ghost. Never color-only: every state has a label or position change |
| Typography | Unbounded display; Instrument Serif italic accents + big numerals; Newsreader body; DM Mono all chips/readouts/labels |
| Grid and spatial language | full-bleed map stages; corridor-centric composition (O bottom-left, D top-right diagonal); prose column 700px |
| Shapes / illustration | 1px-ish hairline streets (0.8–1.6 units), 2.6–3.4px dots, 3px route stroke with soft glow; rings for radii; no icons except pins |
| Annotation language | mono chips `KEY · VALUE`, units always, illustrative labels in caps where the value is illustrative |
| Motion character | mechanical, settle-and-stop; staggered dots as the only rhythm; no physics bounce |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| Eixample graph | the entire demo | © OpenStreetMap contributors, ODbL, extract 2026-08-21 | compact JSON arrays in the page script (~130 KB) | counts in prose |
| Contraction inset | CH mechanism | original | inline SVG diagram | step-4 text |
| No images, fonts as house | — | — | — | — |

## 6. Build handoff

### Document outline

```text
<title>How Google Maps Finds the Fastest Route — Víctor Busqué</title>
main
  hero — h1 “The flood and the arrow.” + dek + post-meta (SEP 2026 · ~15 MIN · 5 SCENES)
  post-prose 01 — the question, scale facts, honesty contract
  sticky S01 — ACT 01 · THE GRAPH (steps 1–5)
  post-prose 02 — Dijkstra history (E13) + what “settle” means
  sticky S02 — ACT 02 · THE FLOOD (steps 1–5)
  sticky S03 — ACT 03 · THE ARROW (steps 1–5)
  breather — “Correct was never the problem. Fast was.”
  post-prose 03 — hierarchy intro (E9) + Valhalla (E12)
  sticky S04 — ACT 04 · THE SKELETON (steps 1–5)
  metrics S06 — ACT 05 · THE SCOREBOARD (table + computed ratios)
  post-prose 04 — traffic: Google's published stack (E3–E5), CRP/MLD (E24)
  sticky S05 — ACT 06 · THE PRICE OF A STREET (steps 1–5)
  post-prose 05 — synthesis, offline fact (E16), ending; callout + aside (OSM attribution)
  post navigation (shared component)
```

- **Target:** `blog/not-ready/how-google-maps-routes.html` while building;
  ships to `blog/how-google-maps-routes.html`.
- **Enhancement ladder:** semantic HTML + static SVG map → CSS states keyed
  off `data-active-step` → scaffold runtime step activation (IO) → one-time
  load-time computation (canonical engine) writing per-step state classes
  and readouts. No rAF loops, no canvas, no scroll-timeline dependencies.
- **State source of truth:** `data-active-step` on each scene; precomputed
  state objects (settle orders, paths) in the page script; no competing
  scroll handlers.
- **Dependencies:** the two required shared chrome components
  (reading indicator + post navigator) only; no CDN scripts; fonts as house.
- **Performance budget / risks:** ~130 KB embedded graph (acceptable; below
  the site's heaviest posts); dot layers as pre-grouped SVG groups per scene
  step (no per-frame JS); cap DPR n/a (no canvas); all computation < 10 ms
  on load; no network requests at runtime.
- **No-JS / reduced-motion plan:** scenes collapse to stage-static +
  stacked steps (scaffold behavior, untouched); each stage's static state is
  its most informative state (S02: full flood + route; S03: corridor over
  ghost; S04: skeleton + inset; S05: new route); all counts in text.
- **Mobile plan:** corridor viewBox per scene; bottom-sheet steps (scaffold);
  chips ≥ 8px; street-name labels desktop-only; verify 390px and 320px.
- **Open implementation questions:** none — all numbers verified
  (`topics/maps-routing/_work/verify.js` reproduces E21/E22).

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `how-google-maps-routes` | permanent |
| Search title | How Google Maps Finds the Fastest Route — Víctor Busqué | 56 chars, keyword-first |
| H1 / shelf title | The Flood and the Arrow. | h1 contract (searcher vs reader) |
| Meta description / deck | Watch a real Barcelona neighborhood become a priced graph, flood it with Dijkstra, aim it with A*, collapse it with hierarchy — every count computed live in your browser. | 172 chars → trim to ≤160 at ship: “Watch a real Barcelona grid become a priced graph, flood with Dijkstra, aim with A*, collapse with hierarchy — every count computed live.” |
| Topic | Algorithms · Maps | manifest label |
| Tags | Google Maps, Dijkstra, A*, Routing, OpenStreetMap | manifest |
| Canonical | `https://victorbusque.com/blog/how-google-maps-routes.html` | verify domain at ship (site uses victorbusque.com + engineering. subdomain — match existing posts' canonical scheme) |
| Date | 2026-09 | publishing month |
| Internal links | post-nav neighbors (automatic); optional prose link to the GNSS post as “where your dot comes from” | none hand-written |

## 8. Definition of ready

- [x] Central question, takeaway, scope, ending explicit.
- [x] Every claim/number has an evidence ID or illustrative label.
- [x] Each scene has a state model, motion reason, fallback, mobile rule.
- [x] Aesthetic named and translated into tokens.
- [x] Outline + implementation plan name target, ladder, state truth,
      risks; no open blocking questions.
- [x] Publishing fields drafted; verified numbers committed in `_work/`.
