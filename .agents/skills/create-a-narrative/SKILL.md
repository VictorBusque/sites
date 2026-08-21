---
name: create-a-narrative
description: >
  Turns a researched topic at topics/<topic>/context.md into the standardized
  topics/<topic>/narrative.md build brief for a standalone scrollytelling
  article. Use after research is available and before a blog article is built:
  it establishes the story, evidence boundaries, analogies, scene states,
  visual direction, animation plan, accessibility fallbacks, and publishing
  handoff a frontend developer needs.
metadata:
  author: Víctor Busqué
  version: "1.0.0"
  site: notebook-of-curiosities
---

# Create a Scrollytelling Narrative

`context.md` records what research says. `narrative.md` makes an editorial and
implementation decision about how to teach it. It is the handoff between
research and the standalone page: specific enough to implement faithfully,
short enough to expose uncertainty before code hides it.

Use this skill for a topic with `topics/<topic>/context.md`. Do not use it to
write the final HTML; hand a ready narrative to `create-a-blog-entry`, which
uses the `scrollytelling` skill to build the article.

## The three-stage pipeline

```text
topics/<topic>/context.md
          │  research, sources, facts, caveats
          ▼
topics/<topic>/narrative.md
          │  story + visual and technical build brief
          ▼
blog/<slug>.html
          │  standalone published scrollytelling article
          ▼
js/posts.js + sitemap.xml
          published landing and search binding
```

Research material stays private in `topics/`; do not publish or link to it
from the site. A topic folder may outlive a draft, and a narrative may be
revised without changing its source research.

## Required inputs and outputs

- **Input:** `topics/<topic>/context.md`. Read it in full, including source
  lists, dates, conflicting claims, and caveats. If it is absent or too thin
  to support a central answer, stop and request research rather than filling
  holes with plausible-sounding facts.
- **Template:** `template/_narrative.md`, relative to this skill directory.
- **Output:** `topics/<topic>/narrative.md`. Copy the template first; preserve
  its headings and tables. Replace all prompts relevant to the topic and
  remove unused blank acts/scenes only after the required information has a
  clear home.

Start a topic with:

```sh
mkdir -p topics/<topic>
# add topics/<topic>/context.md through the research process
cp .agents/skills/create-a-narrative/template/_narrative.md \
  topics/<topic>/narrative.md
```

Never overwrite a substantive existing narrative without explicit instruction.
Update its frontmatter dates and decisions in place instead.

## Workflow

### 1. Audit the research, not just its conclusion

Read `context.md` as an evidence set. Extract:

1. the question it can honestly answer;
2. the mechanism or causal chain that makes the answer interesting;
3. verified facts and their sources, dates, geography, and definitions;
4. disagreements, estimates, forecasts, marketing claims, and missing data;
5. values that may be safely simulated as *illustrative* rather than presented
   as real measurements.

Build the template's evidence table before writing the story. Each claim or
number intended for copy, labels, charts, or readouts gets an ID (`E1`, `E2`,
…). Source references must be usable: a URL, a heading in the context file, or
another clear anchor. Mark conclusions derived by joining facts as
**inference**, and phrase them as such. Do not silently treat a future-dated
claim, a secondary summary, or a company statement as settled fact.

When sources conflict, say so in the narrative and decide whether the article
will compare the claims, qualify them, or omit the disputed detail. Source
quality is part of the story’s scope, not a formatting problem.

### 2. Make a story decision

Complete **Story contract** before scenes. A good central question has one
answer that can be stated plainly. Set the reader’s starting misconception and
ending mental model; this is the test for every later scene.

Find the explanatory form that best fits the mechanism:

- **follow one thing** through a system for queues, networks, and pipelines;
- **compare two paths** for trade-offs, before/after, or own-versus-rented
  infrastructure;
- **reveal layers** for architecture and composition;
- **change scale** for how local rules produce a system outcome;
- **show a constrained simulation** for a rule that changes visible state;
- **use a map/timeline** only when place/time is the essential relationship.

Write an analogy only when it decreases cognitive load. Specify its mapping
and its limit. For example, a shared fibre port may be compared to a branch of
a distribution network, but the narrative must state where that comparison
stops. Never substitute a clever metaphor for the actual mechanism.

The opening promises a concrete explanation. The ending gives the answer in
normal prose; readers must not need to remember an animation to find it.

### 3. Sequence a varied narrative

Use the act table. The common progression is hook → mental model → mechanism
→ critical detail → new perspective → comparison/stress → synthesis →
takeaway; omit acts that do no work. Each act answers a reader question and
changes the model from before to after.

Avoid a collection of fact cards. Prefer a causal progression: “this condition
exists, therefore this decision becomes rational, which changes this cost or
outcome.” Give technical density space to land with quiet beats. The goal is
not to fit every research fact: the goal is to make the selected answer clear
and defensible.

### 4. Specify scenes as buildable behavior

For every scene used, complete its specification rather than only naming an
animation. It must declare:

- narrative job, placement, and one primary visual anchor;
- reader-facing heading, step prose intent, and caption/annotation;
- every visible node, path, label, control, and readout;
- named stable states and what activates them;
- `ENTER → HOLD → TRANSFORM → RESOLVE → EXIT` choreography;
- data source, formula, or illustrative inputs for all numbers;
- a motion reason: what the transformation makes more understandable;
- semantic text equivalent, no-JS layout, reduced-motion stable state, and
  narrow-screen behavior;
- an observable acceptance check.

The visual is decorative if prose carries the conclusion; sticky stage
containers should therefore be `aria-hidden="true"`, while ordered step
paragraphs stay in normal DOM order. If a visual needs to be informative in
its own right, plan unique SVG `<title>`/`<desc>` text and a matching prose
explanation.

Use the simplest progressive enhancement that explains the change:

```text
semantic HTML → CSS → IntersectionObserver / CSS scroll timeline
              → requestAnimationFrame → Canvas/WebGL
```

Do not prescribe a custom scroll engine, an animation library, or Canvas just
because it looks impressive. A reader can reverse, skip, reload midway, or
reduce motion: each named state must make sense independently.

### 5. Choose an aesthetic with a reason

Name a recognized aesthetic or a precise hybrid (for example, editorial Swiss,
scientific field notebook, transit wayfinding, archival technical manual, or
neobrutalist). Then turn it into a usable system: palette semantics,
typography roles, grid, surface treatment, diagram grammar, annotation voice,
and motion character.

“Modern,” “minimal,” “premium,” “dark,” and a list of hex colors are not an
aesthetic direction. The chosen style must make the subject easier to read and
must also name what to avoid. Do not use visual tropes that imply facts the
research cannot support (for example, danger colors to manufacture urgency).

### 6. Hand off the build and publishing decisions

Complete the document outline and enhancement plan as instructions for
`create-a-blog-entry` and `scrollytelling`. Declare the future slug, whether
it begins parked in `blog/not-ready/`, the state source of truth, dependency
exceptions, performance risks, and no-JS / mobile strategy.

Draft SEO and manifest fields, but do not invent publication dates or metadata
that cannot yet be supported. Before a page ships, `create-a-blog-entry` and
the `seo` skill validate these fields against the public HTML, `js/posts.js`,
and `sitemap.xml`.

### 7. Review for readiness

Set `status: ready-for-build` only when the template’s Definition of ready is
true. A narrative with unresolved source conflicts, blank scene state models,
or “make it engaging” as its animation instruction is still a draft.

## Quality standards

A useful narrative is:

- **evidence-led:** it distinguishes fact, inference, and illustrative model;
- **story-led:** every scene changes understanding, not merely appearance;
- **implementation-ready:** another developer can build states and fallbacks
  without guessing; and
- **document-first:** the final page will remain a complete article without
  JavaScript and under `prefers-reduced-motion`.

Never include fake precision, invented statistics, unsourced quotes, or an
animation whose only purpose is visual spectacle. Do not copy long passages
from source material. Cite the research source in the evidence table and write
the planned public explanation in the site’s plain, precise voice.

## Final checklist

- [ ] `topics/<topic>/context.md` was read in full; its scope and source gaps
      are reflected in the narrative.
- [ ] `narrative.md` was created from `template/_narrative.md` and its
      frontmatter identifies its source context and intended slug.
- [ ] Central question, one-sentence answer, reader journey, and plain-text
      ending are concrete.
- [ ] Every planned public claim/readout has an `E#` source, a stated inference,
      or an explicit illustrative label.
- [ ] Each scene has a state table, animation purpose, text fallback,
      reduced-motion state, accessibility plan, and 390px rule.
- [ ] Analogies map to the mechanism and state their limits.
- [ ] A named aesthetic is translated into palette, typography, composition,
      diagram, and motion decisions.
- [ ] Build handoff names the standalone target, enhancement ladder, state
      source of truth, dependencies, performance risks, and publishing fields.
- [ ] Open questions are visible; no uncertainty is disguised as a decision.
