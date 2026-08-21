---
topic: "<topic-folder-name>"
status: draft # draft | ready-for-build | built | superseded
language: en
source_context: topics/<topic-folder-name>/context.md
created: YYYY-MM-DD
updated: YYYY-MM-DD
intended_slug: <lowercase-hyphenated-slug>
---

# <Working article title>

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article. Complete every bracketed prompt with decisions grounded in
> `context.md`. This is not research notes and not final HTML copy: it is the
> agreed narrative, visual, interaction, and implementation plan a frontend
> developer can build without guessing.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | <Who is this for? What can they already understand?> |
| Central question | <The one question this article answers.> |
| One-sentence answer | <Accurate answer, in plain language.> |
| Core takeaway | <What a reader should still be able to explain tomorrow.> |
| Why it matters | <Concrete consequence, not a generic claim.> |
| Scope and exclusions | <What this story deliberately does not claim or cover.> |
| Narrative point of view | <e.g. follow one request, compare two paths, inspect a machine.> |
| Reading language | <Language of the public article.> |

### Reader journey

```text
Before: <the incomplete or misleading mental model>
Bridge: <the image / mechanism / comparison that changes it>
After:  <the accurate, useful mental model>
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** <Draft the reader-facing hook.>
- **Ending (1–3 sentences):** <Draft the conclusion. It must state the answer
  in prose, independent of the animation.>

## 2. Evidence and editorial boundaries

The page may only make claims this table can support. Cite source labels or
anchors that exist in `context.md`; do not promote an inference into a fact.
Use “illustrative” for values invented solely to explain a mechanism, and
make those values visibly illustrative in the page.

| ID | Claim or datum that may appear | Type: verified / inference / illustrative | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | <claim> | verified | <URL, source heading, or note> | <currency and limitation> | <act/scene> |

### Facts to preserve exactly

- <Exact terminology, number, date, unit, or qualification.>

### Claims to avoid or qualify

- <Unverified, disputed, time-sensitive, causal, or oversimplified claim and
  the wording boundary.>

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| <term> | <definition> | <act / section> |

## 3. Narrative architecture

Use only the acts that serve the story. The rhythm should vary (for example,
quiet → reveal → dense → quiet), and every act must change the reader's mental
model. Prose belongs in DOM order; scenes are enhancement, never the sole
place a conclusion exists.

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | <question> | <before → after> | <what the reader learns> | <one visual thing> | <enter → hold → resolve> | <E#> | <readable non-moving version> |
| 1 · Mental model |  |  |  |  |  |  |  |
| 2 · Mechanism |  |  |  |  |  |  |  |
| 3 · Critical detail |  |  |  |  |  |  |  |
| 4 · Change perspective |  |  |  |  |  |  |  |
| 5 · Stress / comparison |  |  |  |  |  |  |  |
| 6 · Synthesis |  |  |  |  |  |  |  |
| 7 · Takeaway |  |  |  |  |  |  |  |

## 4. Scene specifications

Create one section per visual scene. Omit unused scenes; add more when the
story needs them. A developer should be able to build each scene from this
brief without designing its logic on the fly.

### Scene S01 — <concrete name>

- **Narrative job:** <What misconception does it replace, or what new link
  does it establish?>
- **Placement:** Act <N>; follows <previous beat>; hands off <next insight>.
- **Pattern:** <sticky-scene / split / diagram / comparison / simulation /
  metrics / breather / other>.
- **Primary visual anchor:** <The first object, path, layer, or number seen.>
- **Analogy or explanatory device:** <Analogy in one sentence, its mapping to
  the real system, and its limit. Write “none” if literal is clearer.>
- **On-page prose:**
  - Heading: <concrete h2>
  - Step 1: <1–3 sentences, including the conclusion for this beat.>
  - Step 2: <...>
  - Caption / annotation: <What to watch and why it matters.>
- **Stage inventory:** <SVG nodes, lanes, labels, arrows, variables, controls;
  mark decorative layers `aria-hidden`.>
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | <stable initial state> | <step active / control> | <label/readout> | <meaning> |
  | 2 | <transformation> | <...> | <...> | <...> |
  | 3 | <resolved state> | <...> | <...> | <...> |

- **Motion choreography:** <ENTER → HOLD → TRANSFORM → RESOLVE → EXIT. Name
  the property that moves and the reason; include duration/easing only when
  it affects comprehension.>
- **Data / computation:** <Formula, deterministic inputs, source values, or
  “none”. State how every displayed number is computed or cite E#.>
- **Interaction:** <None, or keyboard-accessible control with label, effect,
  initial state, and no-pointer equivalent.>
- **Accessibility and fallback:** <DOM text equivalent; no-JS layout;
  reduced-motion stable state; SVG title/desc if informative.>
- **Responsive rules:** <What simplifies, stacks, relabels, or disappears at
  390px without losing the conclusion.>
- **Acceptance check:** <What must be visibly true when this scene is built.>

### Scene S02 — <concrete name>

<Copy the S01 structure for every additional scene.>

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** <e.g. editorial Swiss, neobrutalist, scientific
  field notebook, transit wayfinding, archival technical manual.>
- **Why this style fits this subject:** <Tie the aesthetic to the idea, not
  fashion.>
- **Emotional register:** <e.g. calm, precise, curious, tense then resolved.>
- **Avoid:** <specific motifs that would dilute or misrepresent the story.>

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | <named colors / paper, dark stage, texture; contrast requirement> |
| Palette semantics | <color → meaning; do not assign meaning by color alone> |
| Typography | <display, body, mono roles; hierarchy and density> |
| Grid and spatial language | <columns, rules, map, layers, depth, or other organizing system> |
| Shapes / illustration | <line weight, corners, icon/diagram grammar> |
| Annotation language | <labels, captions, units, precision> |
| Motion character | <restrained / mechanical / elastic etc.; what must never move> |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| <asset> | <purpose> | <source and permission> | <SVG / CSS / embedded image> | <equivalent> |

Prefer original inline SVG, CSS, or diagrams. Do not require an asset that
has not been supplied or cleared for use.

## 6. Build handoff

### Document outline

```text
<title>…</title>
main
  hero — <h1 and dek intent>
  section — <Act 1>
  sticky scene — <Act 2; steps 1…n>
  …
  conclusion — <final takeaway>
  post navigation
```

### Implementation plan

- **Target:** `blog/<intended-slug>.html` (or `blog/not-ready/<intended-slug>.html`
  while parked).
- **Enhancement ladder:** <semantic HTML → CSS → IntersectionObserver/CSS
  timeline → requestAnimationFrame/Canvas only if needed>.
- **State source of truth:** <e.g. `data-active-step`, deterministic model,
  named function; no competing scroll handlers>.
- **Dependencies:** <normally none beyond the required shared reading
  indicator; list every approved exception and why it is necessary>.
- **Performance budget / risks:** <heavy SVG, canvas, image, or font risks and
  the mitigation; pause offscreen loops; cap DPR when applicable>.
- **No-JS / reduced-motion plan:** <How the full article remains readable and
  what stable visual state is shown.>
- **Mobile plan:** <390px decisions, sticky-track length, labels, touch targets.>
- **Open implementation questions:** <Questions that block a faithful build;
  write “none” only when resolved.>

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `<slug>` | permanent, lowercase, hyphenated |
| Search title | <descriptive keyword-first title> | ≤60 characters including brand where applicable |
| H1 / shelf title | <reader-facing title> | may differ from search title |
| Meta description / deck | <140–160 character promise> | must agree with manifest at ship time |
| Topic | <free-form topic> | manifest label |
| Tags | <tag 1, tag 2> | manifest labels |
| Canonical | `https://victorbusque.com/blog/<slug>.html` | verify current site domain before shipping |
| Date | `YYYY-MM` | publishing month |
| Internal links | <useful predecessor/successor or “none yet”> | update post navigation |

## 8. Definition of ready

Mark `status: ready-for-build` only when all apply:

- [ ] The central question, takeaway, scope, and ending are explicit.
- [ ] Every factual claim, number, and visual readout has an evidence ID or is
      labeled illustrative.
- [ ] Each scene has a narrative job, state model, motion reason, fallback,
      and mobile rule.
- [ ] At least one named aesthetic has been chosen and translated into usable
      visual decisions.
- [ ] The document outline and implementation plan name the target file and
      enhancement strategy.
- [ ] Publishing fields are drafted; unresolved items are recorded rather
      than guessed.
