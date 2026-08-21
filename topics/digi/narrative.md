---
topic: "digi"
status: ready-for-build
language: es
source_context: topics/digi/context.md
created: 2026-08-20
updated: 2026-08-20
intended_slug: digi-costes
---

# Una tarifa barata empieza en el mapa

> **Build brief status:** reconstructed from the shipped article
> `blog/digi-costes.html` and its research context. It documents the page’s
> intended story and implementation contract so future revisions stay
> evidence-led. Research contains conflicting and future-dated reporting;
> do not add those figures to the public article until they are independently
> re-verified at the time of an edit.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Spanish-speaking general reader curious about why a low-cost telecom tariff can exist; no PON or telecom-market knowledge assumed. |
| Central question | Why can DIGI offer especially low fibre and mobile prices in parts of Spain without that price applying uniformly everywhere? |
| One-sentence answer | Its lowest-cost offers align selective own-network coverage, shared access capacity, long-term wholesale arrangements, and a simple operating model where the cost per line is most favorable. |
| Core takeaway | The low price starts with geography and network economics: the same product is not equally cheap to deliver at every address. |
| Why it matters | A tariff is the visible result of infrastructure decisions—where to build, what to share, and when to buy access—not only a marketing decision. |
| Scope and exclusions | Explains network and operating-cost logic; does not calculate DIGI’s profitability, establish predatory pricing, promise actual speeds, or compare every current tariff. |
| Narrative point of view | Follow the cost of one fibre/mobile line from a dense neighborhood, through shared infrastructure, to a hybrid national network. |
| Reading language | Spanish. |

### Reader journey

```text
Before: A very cheap telecom tariff must be a universal trick, loss leader, or
        simple marketing decision.
Bridge: Compare a dense, owned and shared access network with rented access;
        then show why mobile coverage can be built in layers.
After:  Low prices can follow from lower unit costs in selected places, while
        wholesale access and hybrid coverage serve the rest.
```

### Plain-language opening and ending

- **Opening promise:** La pregunta no es cómo puede DIGI vender muchos Mbps por
  pocos euros. Es dónde le cuesta muy poco entregar cada Mbps.
- **Ending:** La propuesta de DIGI no nace de una sola innovación de red. Nace
  de combinar capacidad compartida, despliegue selectivo, acceso mayorista y un
  catálogo simple; la tarifa barata es la consecuencia visible de esa
  arquitectura de costes.

## 2. Evidence and editorial boundaries

| ID | Claim or datum that may appear | Type | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | DIGI distinguishes own-network Fibra SMART coverage from indirect fibre access, with lower-cost economics on its own footprint. | verified | First research section, Accio / El Español links; “Arquitectura… frente a alquiler mayorista” | Current offer/pricing must be checked at edit time; do not reuse historic euro prices as current. | Intro, comparison |
| E2 | A PON access port serves multiple subscribers; context cites up to 64 per port and XGS-PON’s roughly 10 Gb/s gross capacity. | verified | “Diseño de la red de acceso (fibra)”, BandaAncha links | Hardware/configuration-specific; 10 Gb/s is not a per-home guarantee. | Fibre scenes, arithmetic panel |
| E3 | `10,000 Mb/s ÷ 64 = 156.25 Mb/s`. | illustrative calculation | Arithmetic using E2’s explanatory maximum | A simultaneous arithmetic average, not measured traffic or guaranteed throughput. | Arithmetic panel |
| E4 | Capacity/backhaul can be expanded in stages where density and traffic justify it. | verified | “Ingeniería de backbone y dimensionamiento”, BandaAncha / ZonaMovilidad links | General implementation logic; avoid claiming a universal deployment sequence. | Fibre scenes, arithmetic panel |
| E5 | The European Commission’s Orange–MásMóvil remedies included spectrum transfer and national-roaming-related commitments supporting DIGI’s mobile-network path. | verified | European Commission press release links in context | Confirm exact terms and current status before edits. | Mobile scene, analysis |
| E6 | Telefónica and DIGI announced a 16-year mobile-network agreement including national roaming and RAN sharing. | verified | Telefónica press release / context’s mobile-access section | Agreement announced July 2024; use the primary source for dates and terms. | Mobile scene, analysis |
| E7 | DIGI has used a simplified product/commercial model and lower mass-marketing intensity. | inference | “Eficiencia operativa y comercial” (El País, La Razón, ADSLZone) | Comparative cost advantage is an inference, not an audited cost breakdown. | Opening and closing |
| E8 | DIGI sold part of its Spanish fibre network to a Macquarie-led consortium. | verified | Reuters link in context | Supporting context only; not essential to the main visual argument. | Source list |

### Facts to preserve exactly

- The page’s **32 visible subscribers** are a legibility choice. Label it as a
  model; the context’s cited maximum is **up to 64 customers per port**.
- `156.25 Mb/s` is exactly `10,000 ÷ 64`, presented only as a simultaneous
  arithmetic average.
- Do not say XGS-PON gives each home 10 Gb/s simultaneously.
- The article’s caveat must remain: low prices alone do not prove predatory
  pricing.

### Claims to avoid or qualify

- Avoid time-sensitive client counts, market shares, ARPU, churn, specific
  current tariffs, IPO claims, staffing figures, or claimed percentage capex
  savings from the context unless primary, current evidence is added.
- Avoid “near-zero marginal cost,” “guaranteed comparable quality,” and a
  claim that DIGI covers only dense cities; use selected coverage / economic
  conditions rather than absolutes.
- The abstract metro map is not coverage evidence. It must state that it is a
  dense-neighborhood model, not a real coverage map.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| Fibra SMART | DIGI’s name for its own-fibre footprint, distinguished from indirect access. | Intro |
| OLT | The central optical equipment coordinating access for several fibre lines. | Scene S01 |
| XGS-PON | A shared fibre-access technology; it does not mean a dedicated 10 Gb/s cable per home. | Scene S02 |
| Acceso mayorista | Buying access to another operator’s infrastructure instead of owning that last-mile network. | Comparison |
| RAN sharing / roaming nacional | Ways to provide broad mobile access while an operator builds capacity of its own. | Scene S04 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | Is the tariff itself the explanation? | cheap price as mystery → cost geography as question | State that the relevant question is where Mbps are cheap to deliver. | Large headline on a dark, route-like field | Quiet entry; no required animation | E1, E7 | Hero and dek are complete prose. |
| 1 · Mental model | Why is fibre not equally economical everywhere? | one generic network → fixed investment plus nearby lines | Explain own Fibra SMART versus wholesale access; make the geographic qualification explicit. | Two-column explanatory prose | None | E1 | Static text and callout. |
| 2 · Mechanism | How does one central serve multiple homes? | one customer owns a route → shared access equipment | Move attention from one highlighted home to the shared OLT and then the whole dense cluster. | OLT with six homes | Step states 1–4: line → shared OLT → dense cluster → distributed cost | E1, E2 | Stacked steps explain all four states; stage remains a stable diagram. |
| 3 · Critical detail | Does 10 Gb/s mean a dedicated line for each home? | advertised rate as isolated capacity → scheduled shared capacity | Use a deliberately simple port/subscriber model and show the arithmetic’s limitation. | XGS-PON port and 32 visible subscriber marks | Reveal subscribers, coordinated turns, then expansion pressure | E2, E3, E4 | Text states the model and limitations; no animation required. |
| 4 · Change perspective | Why rent access in some places? | own network always better → build-or-rent is situational | Compare cost structures without claiming precise margins. | Two vertical lanes | Quiet comparison; no moving data | E1 | Fully static comparison cards. |
| 5 · Stress / comparison | What makes a neighborhood economical to build? | a country is one deployment unit → dense routes change per-line economics | Show an abstract network map; clarify it is illustrative, not a coverage map. | Transit-map-like route diagram | Static spatial comparison | E1, E4 | Adjacent prose states the criterion. |
| 6 · Synthesis | How can mobile coverage arrive before a national build? | own-or-rented binary → hybrid layered network | Show broad partner coverage, then a local own node and traffic handoff. | Two radio towers and a phone | Step states 1–4: partner coverage → own node → hybrid route → reduced dependence by zone | E5, E6 | Ordered prose preserves the explanation; stable final hybrid state in reduced motion. |
| 7 · Takeaway | What is the short answer? | cheap price as a single trick → system of cost choices | Summarize density, own FTTH, sharing, staged backhaul, and roaming. | Large concluding statement | Quiet resolution | E1–E7 | Complete closing text. |

## 4. Scene specifications

### Scene S01 — Una central, varios hogares

- **Narrative job:** Establish that access infrastructure is shared and that
  proximity/density changes the per-line cost logic.
- **Placement:** Act 2; follows the own-versus-wholesale explanation; hands
  off the idea of shared capacity.
- **Pattern:** `sticky-scene` with a decorative SVG/CSS-style network stage.
- **Primary visual anchor:** The OLT in the center of six homes.
- **Analogy or explanatory device:** A shared distribution point rather than a
  private cable for every home. Mapping: homes connect through common central
  equipment; limit: the picture does not portray a full physical fibre plant.
- **On-page prose:**
  - Heading: “No es la misma fibra en todas partes.”
  - Step 1: A single installation cannot alone justify central equipment and
    access works.
  - Step 2: Several homes share passive fibre and an OLT.
  - Step 3: Dense neighborhoods place more homes near common infrastructure.
  - Step 4: Occupancy distributes investment/operations cost; it does not make
    the network free.
  - Caption / annotation: The highlighted homes and lines indicate what is
    shared, not a real network inventory.
- **Stage inventory:** six abstract homes, six connecting lines, central OLT,
  act label, state/readout. The stage is `aria-hidden="true"`; step prose is
  the text equivalent.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | One home highlighted, lines dim | `data-active-step="1"` | “1 hogar / 1 ruta” | Initial fixed cost is visible before sharing. |
  | 2 | All lines brighten | step 2 | “6 hogares / 1 OLT” | One access point serves more than one line. |
  | 3 | All homes gain active treatment | step 3 | “6 altas cercanas” | Density is the relevant deployment condition. |
  | 4 | OLT and field resolve | step 4 | “coste fijo / 6” | Cost is spread conceptually, not measured. |

- **Motion choreography:** ENTER a stable sparse field → HOLD one home →
  TRANSFORM by brightening shared routes → RESOLVE with the OLT emphasis →
  EXIT to the capacity scene. Transitions clarify relationships; no ambient
  movement is needed.
- **Data / computation:** Six homes are illustrative; never present them as a
  real OLT split or customer count. E1/E2 support the general mechanism.
- **Interaction:** None; scroll activates discrete states.
- **Accessibility and fallback:** Ordered step articles contain the complete
  conclusion. With no JS/reduced motion, show all homes/lines in a stable,
  visible configuration and stack the steps.
- **Responsive rules:** At ≤700px reduce home dimensions, preserve centered
  OLT, move the readout to the lower left, and make every step full-width.
- **Acceptance check:** A reader who stops at any state can identify homes,
  common OLT, and the changing relation between a single line and a dense
  group; the prose says why that relation matters.

### Scene S02 — Turnos sobre una fibra

- **Narrative job:** Correct the inference that advertised 10 Gb/s is a
  dedicated cable per subscriber, while avoiding an invented utilization claim.
- **Placement:** Act 3; follows sharing topology; hands off the arithmetic
  explanation.
- **Pattern:** `sticky-scene` plus a static arithmetic section.
- **Primary visual anchor:** “PUERTO XGS-PON · 10 Gb/s” above a field of 32
  abstract subscriber marks.
- **Analogy or explanatory device:** Turns on a shared resource. Mapping: the
  OLT schedules transmission; limit: the moving beam does not model real
  packet timing or measured load.
- **On-page prose:**
  - Heading: “Diez gigabits no son un cable por casa.”
  - Steps: one shared port; 32 shown for legibility / up to 64 cited; OLT
    coordinates turns; add ports/backhaul where traffic needs it.
  - Caption: `10,000 Mb/s ÷ 64 = 156.25 Mb/s` is a simultaneous arithmetic
    average, not a promised speed or measured result.
- **Stage inventory:** port, moving illustrative beam, 32 subscriber squares,
  readout and step cards. Stage is decorative and `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | One subscriber emphasized | step 1 | “un cliente” | A port is a shared access resource. |
  | 2 | First 16 / visible field becomes active | step 2 | “modelo: 32 de hasta 64” | The scene deliberately shows a partial model. |
  | 3 | All marks settle active | step 3 | “el puerto decide el turno” | Scheduling, not simultaneous dedication, is the mechanism. |
  | 4 | Some marks and beam shift to pressure color | step 4 | “puertos y transporte por etapas” | Capacity is reinforced in stages. |

- **Motion choreography:** ENTER port → HOLD single line → TRANSFORM into
  a field of lines → RESOLVE with coordinated state → EXIT under an explicit
  static calculation. The beam is illustrative only and stops under reduced
  motion.
- **Data / computation:** E2 and E3. `#share` must be generated by
  `(10000 / 64).toFixed(2) + ' Mb/s'`; do not hard-code a divergent value.
- **Interaction:** None.
- **Accessibility and fallback:** Step prose names all conclusions and the
  formula explains the only numeric readout. Reduced motion freezes a stable
  final subscriber field and disables the beam.
- **Responsive rules:** Use 15px squares in an 8-column field; keep labels at
  ≥8px but put the numerical caveat in regular body text nearby.
- **Acceptance check:** The page cannot be reasonably read as a claim that 32
  or 64 subscribers each receive guaranteed 10 Gb/s or 156.25 Mb/s.

### Scene S03 — Construir donde conviene, alquilar donde no

- **Narrative job:** Contrast two cost structures, not two universal quality
  tiers.
- **Placement:** Acts 4–5; follows capacity; hands off the economic meaning of
  selective geography.
- **Pattern:** Quiet comparison followed by a static abstract route map.
- **Primary visual anchor:** Dark “Fibra SMART” lane against light “Acceso
  indirecto” lane, then three colored metro-style paths.
- **Analogy or explanatory device:** Transit-map grammar. Mapping: routes and
  nodes stand for shared infrastructure near potential customers; limit: this
  is expressly not a real coverage map.
- **On-page prose:** Explain own FTTH as investment/maintenance spread across
  occupied network, and indirect access as recurring wholesale cost; explain
  reuse of routes and nearby installations in a dense-neighborhood model.
- **Stage inventory:** two semantic comparison sections; decorative abstract
  map, legend, and visible “MODELO… NO ES UN MAPA DE COBERTURA” label.
- **State model:** Static; no stateful animation is required.
- **Motion choreography:** None. The quiet beat gives the technical scenes
  room to land.
- **Data / computation:** E1/E4 only; no price, margin, or coverage count.
- **Interaction:** None.
- **Accessibility and fallback:** Comparison is real HTML (`dl`); map is
  `aria-hidden` and adjacent prose carries its conclusion.
- **Responsive rules:** Stack comparison lanes and use full-bleed map with the
  explanatory label preserved.
- **Acceptance check:** The reader understands “own where economics support
  it; wholesale where they do not” without seeing a fictional geographic claim.

### Scene S04 — Construir la radio por capas

- **Narrative job:** Explain the hybrid mobile strategy without implying that
  nationwide partner access disappears instantly.
- **Placement:** Act 6; follows fixed-network map; hands off the conclusion.
- **Pattern:** `sticky-scene` with two abstract towers and a phone.
- **Primary visual anchor:** Partner coverage tower on the left, own node on
  the right, and an orange handoff route.
- **Analogy or explanatory device:** Layered coverage. Mapping: national
  roaming/RAN sharing supplies broad reach while own nodes grow in selected
  zones; limit: two towers do not depict real spectrum, coverage radii, or
  traffic volumes.
- **On-page prose:** broad coverage first; own spectrum/nodes where demand
  supports them; hybrid network; migration from variable wholesale use toward
  local capacity by zone.
- **Stage inventory:** radio-ground, two labeled towers, radio rings, phone,
  handoff line, act/readout labels. Stage remains decorative.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Partner tower visible; own node muted | step 1 | “cobertura alquilada” | Reach exists before a complete own build. |
  | 2 | Own node appears | step 2 | “nodo propio” | Local capacity can be introduced. |
  | 3 | Orange handoff appears | step 3 | “roaming + RAN sharing” | The system is hybrid. |
  | 4 | Partner tower de-emphasizes, not disappears | step 4 | “migración gradual” | Cost dependence may change by zone over time. |

- **Motion choreography:** ENTER partner coverage → HOLD → TRANSFORM by
  revealing own node/handoff → RESOLVE as hybrid composition. The partner
  tower must remain visible to avoid a false all-or-nothing story.
- **Data / computation:** E5/E6. No throughput, percentage, coverage, or
  traffic volume displayed.
- **Interaction:** None.
- **Accessibility and fallback:** Four DOM-order steps state the whole model.
  Reduced motion shows both towers and the handoff already visible.
- **Responsive rules:** At ≤700px shorten towers, reduce ring density, and
  wrap the handoff label rather than allowing it to overflow.
- **Acceptance check:** A reader can state why a wholesale/mobile-sharing
  agreement and local own nodes can coexist.

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** Editorial Swiss meets transit wayfinding.
- **Why this style fits this subject:** Telecom cost is about routes, shared
  nodes, capacity, and legible distinctions. A strict grid, high-contrast
  labels, and route-like diagrams make those relationships readable without
  resorting to generic “technology” decoration.
- **Emotional register:** Calm, forensic, and curious; technical complexity
  resolves into a simple geographic conclusion.
- **Avoid:** Telecom-blue corporate dashboard cards, photorealistic city maps,
  fake live telemetry, neon “network pulse” spectacle, and any visual that
  implies real coverage or measured utilization.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | Off-white paper for explanatory beats; deep navy stages (`#061a4a` / `#071b4e`) for system diagrams; fine low-opacity rules, no gradients used as data. |
| Palette semantics | Electric blue = network structure/owned route; cyan = active shared capacity; orange = the active caution/transition; pale text = labels. Meaning is repeated in copy/position, never color alone. |
| Typography | Condensed, heavy sans for headline hierarchy; Georgia-like serif for explanatory emphasis; system monospace for instrumentation and state labels. |
| Grid and spatial language | Rectilinear editorial grid; central network diagrams; transit-style lines/nodes for the dense-neighborhood abstraction. |
| Shapes / illustration | Thin outlined homes, port/tower blocks, straight paths, square subscriber marks, restrained shadows. |
| Annotation language | Uppercase mono labels, concrete unit-bearing readouts, explicit “MODELO” and “no es…” caveats. |
| Motion character | Decelerated discrete state changes; continuous beam only as an explicitly illustrative support layer. No uncontrolled loops. |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| Fibre topology | Explain sharing | Original abstraction | CSS/SVG-like HTML | Step prose S01 |
| Port/subscriber field | Explain scheduling | Original illustrative model | CSS/HTML | Step prose plus arithmetic note |
| Dense-neighborhood map | Explain selective deployment | Original abstraction | CSS/HTML | Adjacent map paragraph + “not coverage” label |
| Mobile towers | Explain hybrid coverage | Original abstraction | CSS/HTML | Step prose S04 |

## 6. Build handoff

### Document outline

```text
<title>Por qué DIGI puede ser tan barata en España — Víctor Busqué</title>
main
  hero — “Una tarifa barata empieza en el mapa.”
  intro — own versus wholesale fibre
  sticky scene S01 — one OLT, several homes
  sticky scene S02 — shared XGS-PON access
  static arithmetic — 10,000 ÷ 64, explicitly illustrative
  comparison + map — build selectively / rent access
  sticky scene S04 — layered mobile network
  analysis — 16-year agreement and caveat
  closing — cost architecture takeaway
  post navigation
```

### Implementation plan

- **Target:** `blog/digi-costes.html` (already shipped). Park redesign drafts
  at `blog/not-ready/digi-costes.html` until ready.
- **Enhancement ladder:** semantic HTML → page-local CSS →
  `IntersectionObserver` discrete step activation. No Canvas/WebGL or
  scroll-linked continuous animation is necessary.
- **State source of truth:** Every sticky scene owns `data-active-step` and
  derives its readout from a deterministic per-scene state array. Its step
  articles remain sequential `1…n` in DOM order.
- **Dependencies:** Required shared reading indicator only:
  `../css/post-progress.css` and `../js/post-progress.js`; otherwise inline
  CSS/JS. Do not add a chart, animation, map, or framework dependency.
- **Performance budget / risks:** CSS gradients and modest DOM diagrams only;
  the beam animation pauses in reduced motion. No offscreen render loop and no
  network-loaded scene asset.
- **No-JS / reduced-motion plan:** All conclusions exist in headings,
  paragraphs, and ordered step articles. Reduced motion removes animated beam,
  turns sticky stages into a stable visual plus stacked cards, and presents the
  hybrid-mobile final state.
- **Mobile plan:** At 390px, stages stay full viewport but text cards become
  full-width bottom sheets; network objects shrink rather than labels becoming
  unreadable; lanes stack; handoff text wraps; no conclusion is omitted.
- **Open implementation questions:** Before editing public metadata, reconcile
  the `engineering.victorbusque.com` domain in the existing post with the
  `victorbusque.com` convention in current repository guidance and sitemap.

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `digi-costes` | Existing shipped URL; do not rename. |
| Search title | Por qué DIGI puede ser tan barata en España — Víctor Busqué | Existing public title; re-check current SEO character guidance before modifying. |
| H1 / shelf title | Una tarifa barata empieza en el mapa. | Existing reader-facing display headline. |
| Meta description / deck | Por qué DIGI ofrece fibra y móvil baratos en España: red propia en zonas densas, capacidad compartida y acuerdos mayoristas que reducen el coste por línea. | Existing public description; manifest must match exactly. |
| Topic | Redes · Economía | Existing post metadata. |
| Tags | DIGI, fibra, XGS-PON, telecomunicaciones, España | Existing JSON-LD tags; align manifest convention if changed. |
| Canonical | `https://engineering.victorbusque.com/blog/digi-costes.html` | Existing public post; resolve domain convention before changing. |
| Date | 2026-08 | Existing publication context should be verified against manifest. |
| Internal links | Index; Starlink next post | Existing footer navigation. |

## 8. Definition of ready

- [x] The central question, takeaway, scope, and ending are explicit.
- [x] Every public numerical readout is either computed (E3) or bounded by a
      cited source; illustrative elements are labeled.
- [x] Each animated scene has a state model, motion reason, fallback, and
      mobile rule.
- [x] The aesthetic is named and translated into usable visual decisions.
- [x] The outline and implementation plan name the target and enhancement
      strategy.
- [x] Publishing fields reflect the shipped page; the domain inconsistency is
      explicitly recorded for resolution rather than guessed.
