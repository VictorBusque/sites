# Context — How does Google Maps calculate the best route?

Research record for a prospective scrollytelling article. Sources are numbered
[S1]… and quoted or paraphrased with their date and scope. Anything not
covered by a source here must not appear on the public page as fact.

## The honest boundary, stated first

Google has never published a description of the algorithms inside its
production routing engine. Every public Google statement about routing we
found describes **data and machine learning** (traffic, ETAs, road quality,
incident reports), not shortest-path machinery. What Google does publish
(S1–S6 below) plus the peer-reviewed state of the art (S7–S12) and open
production engines built on OpenStreetMap (S13–S15) let us teach, with
evidence, *what any continental-scale router must do* — and be explicit about
which parts are demonstrated on public systems rather than claimed for
Google's internals. This boundary is itself part of the story and belongs on
the page.

## Sources

- **[S1] Google, “Google Maps 101: How AI helps predict traffic and determine
  routes”, The Keyword (Google blog), October 2020.**
  https://blog.google/products-and-platforms/products/maps/google-maps-101-how-ai-helps-predict-traffic-and-determine-routes/
  Key verifiable claims:
  - “Every day, over 1 billion kilometers are driven with Google Maps in more
    than 220 countries and territories around the world.”
  - Live traffic comes from “aggregate location data” of people navigating —
    crowdsourced, not sensors.
  - Future traffic is predicted by combining that live data with a database of
    historical patterns, using machine learning; example given: highway 280 at
    65 mph 6–7am but 15–20 mph late afternoon.
  - ETA predictions “consistently accurate for over 97% of trips”; a DeepMind
    partnership (Graph Neural Networks) cut inaccurate ETAs further — “by up
    to 50%” in cities like Berlin, Jakarta, São Paulo, Sydney, Tokyo,
    Washington D.C.
  - Route choice factors listed by Google: predicted traffic, road quality
    (paved/unpacked/gravel), “the size and directness of a road — driving down
    a highway is often more efficient than taking a smaller road with multiple
    stops”, authoritative government data (speed limits, tolls, closures), and
    real-time driver incident reports.
  - During COVID, models were updated to prioritize historical patterns from
    “the last two to four weeks” over older patterns; worldwide traffic dropped
    “up to 50 percent” at the start of lockdowns (early 2020).
- **[S2] Google DeepMind, “Traffic prediction with advanced Graph Neural
  Networks”, September 2020.**
  https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/
  - The Maps traffic-prediction system: (1) “a route analyser that processes
    terabytes of traffic information to construct Supersegments” and (2) a GNN
    “which is optimised with multiple objectives and predicts the travel time
    for each Supersegment”.
  - A Supersegment is a set of adjacent road segments sharing significant
    traffic volume; one single model serves all of them.
  - GNN node = road segment; edges connect consecutive segments or segments
    joined at an intersection.
  - “more than one billion people that use Google Maps” (2020 wording).
- **[S3] Google, “20 years of Google Maps: 20 favorite features”, February
  2025.** https://blog.google/products-and-platforms/products/maps/20-years-google-maps-20-features/
  - “more than 2 billion users per month” today.
  - Fuel-efficient routing “now available globally”.
- **[S4] Google Maps Help, “Download areas and navigate offline”.**
  https://support.google.com/maps/answer/6291838
  - “If your Internet connection is slow or unavailable, your offline maps can
    guide you to your destination as long as the entire route is within the
    offline map.”
  - Offline: no public transport, cycling or walking directions; no traffic
    info or alternative routes while driving. Offline areas expire unless
    updated.
- **[S5] Wikipedia, “Google Maps” / “Lars Rasmussen (software developer)”**,
  accessed 2026-08.
  - Maps began as a C++ desktop program by Lars & Jens Rasmussen, Stephen Ma,
    Noel Gordon at Where 2 Technologies (Sydney, founded early 2003); acquired
    by Google October 2004; relaunched as the web app Google Maps (February
    2005).
- **[S6] Edsger W. Dijkstra, “A note on two problems in connexion with
  graphs”, *Numerische Mathematik* 1:269–271, 1959.** The shortest-path
  algorithm appears here, designed in 1956. In a 2001 CACM interview with
  Philip L. Frana, Dijkstra said: “What's the shortest way to travel from
  Rotterdam to Groningen? It is the algorithm for the shortest path, which I
  designed in about 20 minutes.” (Anecdote also confirmed by Britannica: “in
  20 minutes while sitting in a café”, 1956, with his fiancée.) He also noted
  it was designed without pencil and paper, and that the lack of a computer
  forced a simple proof — phrasing to keep if used: it is a documented
  anecdote, not a fact about Maps.
- **[S7] Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias
  Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner, Renato F.
  Werneck, “Route Planning in Transportation Networks”, arXiv:1504.05140
  (2015; book chapter in *Transportation Science* 2016).** The survey of the
  field; our performance numbers come from its Table 1 (Western Europe
  benchmark, PTV, travel-time metric, single-threaded Intel X5680 3.33 GHz,
  random point-to-point queries):
  - Western Europe instance: **18.0 million vertices, 42.5 million directed
    arcs**, 13 road categories.
  - **Dijkstra: 9,326,696 vertices scanned, 2,195,080 µs average query**
    (≈2.2 s). Bidirectional Dijkstra: 4,914,804 scanned, 1,205,660 µs.
  - **CH: 280 vertices scanned, 110 µs average query, 5 minutes preprocessing,
    0.4 GiB.**
  - CRP: 2,766 scanned, 1,650 µs, 1 hour preprocessing (metric customization
    designed for fast re-weighting, i.e. traffic).
  - Transit-node routing (TNR): 2.09 µs; Hub labels (HL): 0.56 µs with 18.8
    GiB; HL-∞ 0.25 µs; table lookup 0.06 µs with 1,208 GiB and 145.5 hours
    preprocessing.
  - Abstract: “one can compute driving directions in milliseconds or less even
    at continental scale… Some algorithms can answer queries in a fraction of
    a microsecond, while others can deal efficiently with real-time traffic.”
  - Dijkstra described: priority queue by tentative distance, arc relaxation,
    “label-setting” property — once settled, a vertex's distance is final;
    search space = set of scanned vertices; complexity O((|V|+|A|) log |V|)
    with binary heaps.
  - Bidirectional search: run forward from s and backward from t
    simultaneously, stop when search spaces meet; on road networks visits
    roughly half the vertices of plain Dijkstra.
  - A* goal-directed search: potential functions bend the search toward the
    target; with geometric (straight-line distance) bounds the search space
    shrinks toward the s–t corridor, but on road networks with travel-time
    metric, plain geographic A* “performs poorly compared to other modern
    methods”; ALT (A*, landmarks, triangle inequality) picks landmarks during
    preprocessing and derives much stronger lower bounds.
  - Hierarchical methods: “Sufficiently long shortest paths eventually
    converge to a small arterial network of important roads, such as
    highways.” Using input road categories directly is “a popular heuristic…
    though there is no guarantee that it will find exact shortest paths.”
  - Contraction Hierarchies (per survey): order vertices by “importance”
    computed from the actual shortest-path structure, then iteratively
    contract the least important: remove it, add a shortcut between neighbors
    u,w when the unique shortest u–w path went through it; queries are
    bidirectional searches that only go “up” the hierarchy; preprocessing
    minutes on continental networks; CH is “a successor of Highway
    Hierarchies and Highway Node Routing… not only faster, but also
    conceptually simpler.”
- **[S8] Robert Geisberger, Peter Sanders, Dominik Schultes, Daniel Delling,
  “Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road
  Networks”, WEA 2008, LNCS 5038, pp 319–333. DOI 10.1007/978-3-540-68552-4_24.**
  The original CH paper. Nodes ordered by importance; hierarchy generated by
  iteratively contracting the least important node; query answered by
  bidirectional upward search in the augmented graph.
- **[S9] Peter E. Hart, Nils J. Nilsson, Bertram Raphael, “A Formal Basis for
  the Heuristic Determination of Minimum Cost Paths”, *IEEE Transactions on
  Systems Science and Cybernetics* SSC-4(2), 1968.** Introduces the A*
  algorithm and admissibility: a heuristic that never overestimates remaining
  cost keeps the search optimal. (Developed at SRI for Shakey the robot —
  history widely documented; use only if verified wording is found; the paper
  itself suffices for the algorithm.)
- **[S10] Ittai Abraham, Daniel Delling, Andrew Goldberg, Renato F. Werneck,
  “A Hub-Based Labeling Algorithm for Shortest Paths on Road Networks”, SEA
  2011.** Hub labels: preprocessing assigns each vertex a small set of “hub”
  labels; a query intersects two label sets. Basis of the fastest known exact
  queries (sub-microsecond, per S7 Table 1).
- **[S11] Daniel Delling, Andrew V. Goldberg, Thomas Pajor, Renato F. Werneck,
  “Customizable Route Planning”, WEA 2011 / *Transportation Science* 2015.**
  CRP: separator-based overlay whose *metric* (edge weights) can be
  re-customized in minutes-to-seconds — designed precisely so live traffic can
  change all edge weights without redoing the expensive structure. (Built at
  Microsoft for Bing; cited here as documented production-grade practice, not
  as a Google claim.)
- **[S12] OpenStreetMap database statistics, Taginfo, data through
  2026-08-21.** https://taginfo.openstreetmap.org/reports/database_statistics
  - **10,808,015,284 nodes; 1,212,231,057 ways; 12,034,906,656 objects total.**
  OSM is the base data of every open routing engine; Google builds its own map
  (Base map / Ground Truth) — do not conflate.
- **[S13] Valhalla (open-source routing engine, OSM-based), documentation:
  “Tile Specifications — Hierarchies/Levels”.**
  https://valhalla.github.io/valhalla/concepts/tiles/
  - Valhalla stores the graph in a **three-level hierarchy**: level 0 (4°
    tiles): motorway, trunk, primary; level 1 (1° tiles): secondary, tertiary;
    level 2 (0.25° tiles): unclassified, residential, service.
  - Documents, in a production engine, the same arterial/local split the CH
    literature formalizes.
- **[S14] Project-OSRM (open-source routing engine, OSM-based).** Its engine
  is parameterized by routing algorithm — Contraction Hierarchies or
  Multi-Level Dijkstra (MLD) — the latter allowing fast re-weighting for
  traffic. (Repository/wiki documentation; supports “open routers use CH-family
  machinery in production” as a verified statement about OSRM, not Google.)
- **[S15] GraphHopper (open-source routing engine, OSM-based),
  `PrepareContractionHierarchies.java`.** Documents CH as its speed-up
  technique with “several descriptions of contraction hierarchies available”.
- **[S16] Local map data for the interactive scenes**: OpenStreetMap extract
  of Barcelona's Eixample district (bounding box ≈ 41.387–41.404 N,
  2.142–2.178 E), fetched from the Overpass API on 2026-08-21 for this
  article; 1,491 highway ways (404 secondary, 371 residential, 351
  living_street, 244 tertiary, 96 primary, 25 secondary_link). Street graph
  built from it: intersections become vertices, street segments become edges,
  weights = length (haversine) and an inferred free-flow time. © OpenStreetMap
  contributors, ODbL. All demo counts in the article are computed live in the
  reader's browser from this embedded, real graph — never hand-authored.

## Facts to preserve exactly

- 1B+ km driven with Maps daily; 220+ countries/territories; 2B+ monthly users
  (S1, S3). “Over 97% of trips” ETA accuracy (S1, S2).
- Western Europe benchmark: 18.0M vertices / 42.5M arcs; Dijkstra scans
  9,326,696 vertices in 2,195,080 µs; CH scans 280 in 110 µs after 5 minutes
  of preprocessing (S7 Table 1). Ratios between these numbers may be computed
  and displayed (that is arithmetic on cited numbers, not new measurement).
- Valhalla's 3 levels with their road classes and tile sizes (S13).
- OSM counts with their date: 10.8B nodes / 1.2B ways as of 2026-08 (S12).
- Dijkstra 1956 design / 1959 publication; 20-minute café anecdote is a quote
  from a 2001 interview (S6).
- CH: Geisberger–Sanders–Schultes–Delling, WEA 2008 (S8).
- Offline mode: routes work offline if the whole route is inside the saved
  area; no traffic/alternatives offline (S4).
- Google Maps origin: Where 2 Technologies, Sydney, founded early 2003,
  acquired Oct 2004, web launch Feb 2005 (S5).

## Claims to avoid or qualify

- **Never claim Google uses Dijkstra/A*/CH/hub labels internally.** No public
  source says so. Frame: “Google doesn't publish its routing internals; here
  is the published state of the art any such system builds on, demonstrated on
  open engines and a real city graph.”
- “Best route” is Google's route choice under its cost model (time prediction,
  road quality, directness, tolls, incidents — S1); not a pure shortest path.
  Avoid presenting “shortest time” as the only criterion.
- Don't say Maps “uses Dijkstra today” or imply the 1959 algorithm alone is
  what answers a query at continental scale; the survey shows plain Dijkstra
  needs seconds there.
- Don't attribute Valhalla/OSRM design choices to Google, or vice versa.
- The A*/Shakey history: only use what S9 supports (the paper and
  admissibility); the Shakey origin story needs a solid secondary source
  before it goes on the page.
- OSM ≠ Google's map. Google's base map data is proprietary (do not detail
  beyond what sources say).
- ETA “97%” is Google's own claim about itself — attribute it (“Google
  says”), never state as independent measurement.
- Live-traffic crowdsourcing: aggregate location data of people navigating
  (S1). Avoid the stronger claim that “every Android phone” feeds traffic.

## Mechanisms the article may teach as verified public knowledge

1. **The map is a graph.** Intersections → vertices; street segments → edges;
   each edge has a cost (time = length / speed). Demonstrated live on real
   Barcelona OSM data [S16].
2. **Dijkstra 1959** — the reference solution: always settle the closest
   unsettled vertex; label-setting property; stops when the target settles.
   Live demo: on the Eixample graph, count settled vertices and watch the
   frontier flood outward with no sense of destination. Complexity
   O((|V|+|A|) log |V|) (S7).
3. **A\* 1968** — same algorithm plus an admissible lower bound on remaining
   cost (straight-line distance ÷ fastest road speed); never overestimates →
   still optimal; search bends toward the target (S7, S9). Live demo: same
   graph, same origin/destination, visibly smaller search space, identical
   route, honest settled-count comparison.
4. **Road networks have an inherent hierarchy** — long shortest paths converge
   onto arterials/motorways (S7 quote; Valhalla's 3 levels as production
   evidence S13). The naive version (only search important roads) is a
   heuristic without optimality guarantees (S7).
5. **Contraction Hierarchies** — preprocessing contracts unimportant vertices,
   inserting shortcuts; a node-importance order computed from the actual
   shortest-path structure; query = bidirectional upward search; hundreds of
   settled vertices at continental scale (S7, S8). Preprocessing trades
   hours-to-minutes of one-time work for per-query speedups of four orders of
   magnitude (S7 Table 1).
6. **Traffic changes the weights** — live + historical traffic re-prices
   edges; ETAs predicted with GNNs on Supersegments (S1, S2); CRP documents
   the engineering answer for fast metric re-customization (S11); OSRM's MLD
  is the open equivalent (S14). CH's shortcut structure is metric-dependent —
  the tension between static preprocessing and live weights is real and
  documented.
7. **The continental scoreboard** (S7 Table 1): Dijkstra 9.3M scanned / 2.2 s
   → bidirectional 4.9M / 1.2 s → CH 280 / 110 µs → TNR 2.09 µs → HL 0.56 µs;
   each step trades space/preprocessing for query speed.

## Live-computation plan (what the page computes in the browser)

- Embedded graph: real OSM Eixample streets [S16], embedded as compact arrays
  (coordinates quantized to 1e-5 deg ≈ 1 m; edge list with lengths; arterial
  flag per edge from OSM highway class: primary/secondary/trunk → arterial,
  else local).
- Dijkstra and A* run on the embedded graph in the page; settled counts,
  route length, and route time are computed, not authored. The offline build
  verifies the same numbers so the narrative can cite exact counts (they are
  then deterministic facts of the embedded dataset, labeled as such).
- A* heuristic: h(v) = great-circle distance(v, target) ÷ 120 km/h (an
  illustrative-but-admissible bound; 120 km/h ≥ any legal Barcelona street
  speed; the page labels the assumption).
- Hierarchy demo: re-run the search with local roads pruned to the arterial
  skeleton near origin/destination only (an honest, simplified model of the
  classical hierarchy heuristic; labeled illustrative; contrasted with the
  guarantee CH adds by *computing* importance rather than reading road
  classes).
- Continental scoreboard numbers are the cited Table 1 values (S7); any ratio
  shown is computed from them in-page.

## Open questions for the narrative

- How much of ETA/traffic (acts about weights) to include without diluting
  the shortest-path spine — leaning: one act, facts S1/S2/S11, no new
  simulation.
- Whether to show the A* ellipse vs Dijkstra disc in one sticky scene with two
  phases, or two scenes. (Design decision; both buildable.)
- Confirm reading time, slug, and which existing posts to cross-link
  (GNSS/GPS post is a natural neighbor: “how your phone knows where it is” →
  “how the map knows where you're going”).
