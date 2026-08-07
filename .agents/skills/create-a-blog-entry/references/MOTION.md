# Motion Standards

Site-specific application of the motion-design skill. These rules govern every
animation on the site — figure choreography, reveals, micro-interactions.

## Personality

**Premium editorial, energetic accents.** Everything settles with grace
(ease-out deceleration), nothing bounces playfully. Energy lives in the accent
colors and in the algorithm's own motion, not in gimmicks.

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
   (background life — grid drift, floating numerals, pulse rings). A figure
   with only one layer reads as flat.
4. **1/3 rule.** No single element travels more than 1/3 of the canvas before
   a keyframe change; with 3+ moving elements, keep no more than 1/3 in active
   motion at once.
5. **Stagger budgets under 500ms total.** Hero lines: `.1s/.22s/.34s` delays.
   Card rows: 50–100ms increments. Never a visible queue of delayed items.
6. **Opacity alone is not enough** for a state change — pair it with position
   or scale (this is why "past" cells dim *and* stay in place while the marker
   moves on).

## Duration palette

| Element | Duration |
|---|---|
| Hover feedback | < 100ms |
| Button / fig-btn press | < 150ms |
| State change in a figure (cell probe, bar swap) | 150–300ms |
| Scripted figure step | 500–1300ms per step (default 950ms) |
| Ambient loop period | 2.5–4s |
| Entrance reveals | 800–1100ms |
| Masked line reveals | 1000ms, staggered |

Distance scales duration: a probe traveling far uses the top of the range; a
local highlight uses the bottom.

## Choreography for figures

- **One hero element per figure.** The reader should know what to watch before
  the caption tells them. Everything else is secondary or ambient.
- **Anticipation:** if an element will appear, give it a beat — a marker that
  fades/scales in just before it moves, a glow that builds before a swap.
- **Settling:** after a swap or a found state, let a pulse or ring echo
  (e.g. `.pop`, `node-ping`) so the reader registers the moment, then return
  to idle.
- **Consistency:** within a post, the same semantic state always uses the same
  color and motion (orange = probe, acid = found/settled, blue = scanning).
- **Scripted steps should feel causal:** each NEXT press should show one
  *decision* (one comparison, one swap, one arrival) — never several unrelated
  changes at once.

## Micro-interactions

- Hover on links: the underline grows from the right (`.links a::after`).
- Hover on cards: the stage lifts (`translateY(-6px)` + ink offset shadow),
  the ghost numeral darkens, the read arrow slides.
- `.fig-btn` press: scale to `.94` in `--ease-snap`.
- Buttons invert on hover (ink fill, paper text) in `--t-fast`.

## Loops that breathe

Ambient loops (pulses, pings, floating numerals) should be period-locked to
feel alive without demanding attention: 2.4–3s for pings, 7–10s for slow
floats, and marquee/grid drift at 26–30s. If two loops share a beat, offset
them (stagger delays) instead of syncing them.

## Reduced motion

The global `prefers-reduced-motion` block in `css/site.css` is the safety
net — it collapses durations to near-zero and forces reveals visible. When a
figure's *meaning* depends on motion (which it often does), the copy must
still carry the idea: captions explain what you would see, and scripted
figures remain step-through-able (the engine simply won't autoplay).
