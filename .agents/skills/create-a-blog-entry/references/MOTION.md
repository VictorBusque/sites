# Motion Standards

Site-specific application of the motion-design and scrollytelling skills.
These rules govern every animation on the site — scene choreography, step
cards, reveals, micro-interactions.

## Personality

**Premium editorial, energetic accents.** Everything settles with grace
(ease-out deceleration), nothing bounces playfully. Energy lives in the accent
colors and in the mechanism's own motion, not in gimmicks.

Signature constants (defined in `css/site.css`):

- `--ease-out: cubic-bezier(.16, 1, .3, 1)` — 80% of movement
- `--ease-snap: cubic-bezier(.2, 0, 0, 1)` — micro-interactions, hovers
- `--ease-swift: cubic-bezier(.4, 0, .2, 1)` — on-screen state changes
- `--t-fast: 180ms`, `--t-med: 400ms`, `--t-slow: 800ms`, `--t-dramatic: 1100ms`

## Hard rules (never break)

1. **Never linear for spatial movement.** `linear` is reserved for spinners,
   progress bars and marquees. Movement always uses an easing curve.
2. **Directional easing.** Entrances decelerate (fast start, gentle landing).
   Exits accelerate. Looping ambient motion uses seamless sine-style in/out so
   the loop has no visible seam.
3. **Three motion layers, always.** Primary (the action the reader follows),
   secondary (a supporting glow/shadow/icon that lands with it), ambient
   (background life — grid drift, floating numerals, pulse rings). A scene
   with only one layer reads as flat.
4. **1/3 rule.** No single element travels more than 1/3 of the stage before
   a keyframe change; with 3+ moving elements, keep no more than 1/3 in active
   motion at once.
5. **Stagger budgets under 500ms total.** Hero lines: `.1s/.22s/.34s` delays.
   Card rows: 50–100ms increments. Never a visible queue of delayed items.
6. **Opacity alone is not enough** for a state change — pair it with position
   or scale (this is why "past" cells dim *and* stay in place while the
   marker moves on).

## Duration palette

| Element | Duration |
|---|---|
| Hover feedback | < 100ms |
| Button press | < 150ms |
| State change in a stage (cell probe, bar swap) | 150–300ms |
| Step-card enter/exit | 600–900ms, `--ease-out` |
| Ambient loop period | 2.5–4s |
| Entrance reveals | 800–1100ms |
| Masked line reveals | 1000ms, staggered |

Distance scales duration: a marker traveling far uses the top of the range; a
local highlight uses the bottom.

## Choreography for scenes

- **One hero element per scene.** The reader should know what to watch before
  the step text tells them. Everything else is secondary or ambient.
- **Choreograph every scene** `ENTER → HOLD → TRANSFORM → RESOLVE → EXIT`.
  No instant A→B jumps unless the contrast is the explanation.
- **Scroll is the timeline.** Each step of a sticky scene is one named state
  of the diagram — one decision, one arrival, one comparison. Never several
  unrelated changes per step. Map scroll into named states, not pixels.
- **Anticipation:** if an element will appear, give it a beat — a marker that
  fades/scales in just before it moves, a glow that builds before a swap.
- **Settling:** after a swap or a found state, let a pulse or ring echo
  (`.pop`, `.ping` keyframes are shared) so the reader registers the moment,
  then return to idle.
- **Consistency:** within an article, the same semantic state always uses the
  same color and motion (orange = the thing to watch, blue = examining,
  acid = found/settled).
- **Reversibility:** readers stop, reverse, and jump via the scrollbar. Every
  intermediate and reverse state must make sense, and the conclusion must
  exist in the step text — never only in a fleeting transition.

## Micro-interactions

- Hover on links: the underline grows from the right (`.links a::after`).
- Hover on cards: the stage lifts (`translateY(-6px)` + ink offset shadow),
  the ghost numeral darkens, the read arrow slides.
- Buttons invert on hover (ink fill, paper text) in `--t-fast`; press scales
  to `.94` in `--ease-snap`.
- Optional controls in a scene (toggle, replay) are keyboard reachable,
  visibly focused, and secondary to the scroll story — scrolling already
  drives progression, so do not force clicks.

## Loops that breathe

Ambient loops (pulses, pings, floating numerals) should be period-locked to
feel alive without demanding attention: 2.4–3s for pings, 7–10s for slow
floats, and marquee/grid drift at 26–30s. If two loops share a beat, offset
them (stagger delays) instead of syncing them.

## Reduced motion

The global `prefers-reduced-motion` block in `css/site.css` is the safety
net — it collapses durations to near-zero, forces reveals visible, and
restores sticky scenes to plain document flow (stage static, steps stacked,
all text visible). When a scene's *meaning* depends on a diagram state, the
step text always carries the conclusion — that is the fallback, and it is
never optional.
