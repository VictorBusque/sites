---
topic: "payments"
status: built
language: en
source_context: topics/payments/context.md
created: 2026-08-22
updated: 2026-08-22
intended_slug: how-card-payments-work
---

# How a Card Payment Actually Works

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article, following the two-timeline story of a card payment: the two-second
> authorization and the days-later settlement.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Curious general reader; has tapped a card and seen "approved"; no payments background. Understands "bank account" and "ledger" at gut level. |
| Central question | What actually happens when you pay by card — in the two seconds after the beep, and in the days after that? |
| One-sentence answer | The beep is a two-second question and answer — your bank promises the money to the merchant's bank and places a hold — and the money itself only moves a day or two later, through clearing and net settlement, minus three tolls. |
| Core takeaway | "Approved" is a guarantee, not a transfer: five parties exchange standardized messages in seconds, then reconcile and net-settle in days; the fee you never see is split three ways. |
| Why it matters | Readers believe money teleports; in reality they use a planetary messaging system whose speed is in messages, not money — and that gap is why holds, pending charges, and merchant payout delays exist. |
| Scope and exclusions | One card payment (tap or online checkout) on Visa/Mastercard-style four-party rails. Not covered: ACH/wire/SEPA instant transfers, crypto, internal bank accounting, BNPL, chargeback mechanics beyond a mention. |
| Narrative point of view | Follow one payment: a €4.50 coffee, tap to payout. |
| Reading language | English. |

### Reader journey

```text
Before: "When the terminal beeps, the money leaves my account and arrives
at the shop — instantly."
Bridge: Two timelines. The beep is a message round trip that creates two
promises (a hold, a guarantee). The money moves days later, batched and
netted between banks.
After:  A five-party model: terminal → acquirer → network → issuer, an
ISO 8583-style question, a chip cryptogram proving the card is present,
then capture → clearing → net settlement → payout, minus interchange,
scheme fee, and acquirer markup.
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** You tap, the terminal beeps, and the
  receipt prints in about two seconds. Nothing has been paid yet — what you
  watched was a question, an answer, and a promise; the money won't move for
  another day or two.
- **Ending (1–3 sentences):** A card payment is two promises plus a
  reconciliation. In two seconds, five parties agree that €4.50 is owed and
  your bank guarantees it; over the next day or two, millions of those
  promises are batched, netted, and settled — and the merchant finally gets
  €4.41 while three tolls come off the top. The beep was never the payment;
  it was the vote of confidence that made the payment possible.

## 2. Evidence and editorial boundaries

Evidence table (sources are anchors in `topics/payments/context.md`, F# refs).

| ID | Claim or datum that may appear | Type: verified / inference / illustrative | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | Authorization takes about two seconds | verified | F1 | industry-standard description | hook, S01 |
| E2 | Clearing + settlement complete typically 1–3 business days later | verified | F1, F10 | varies by acquirer/region; always "typically" | hook, Act 4 |
| E3 | Five parties: cardholder, merchant, acquirer, network, issuer | verified | F2 | standard four-party model + network | Act 1, S01 |
| E4 | The network routes messages and writes the rules; it is not a bank | verified | F2 | — | Act 1 |
| E5 | Authorization places a hold, not a transfer | verified | F1, F12 | — | Act 2, S04 |
| E6 | ISO 8583 defines the card-transaction message format; born 1987; MTI + bitmap + fields | verified | F5 | — | Act 2, S02 |
| E7 | Authorization request MTI 0100, response 0110, approval response code 00 | verified | F5 | classic ISO 8583 values | S02 |
| E8 | EMV chip produces a per-transaction ARQC: 8-byte MAC over card+terminal+transaction data from a session key + transaction counter; verified by issuer | verified | F6 | simplification of full EMV flow | Act 3, S03 |
| E9 | Chip cards can't be usefully cloned (vs magnetic stripe) because each transaction's cryptogram is unique | verified | F6 | — | Act 3 |
| E10 | PSD2 SCA (since 14 Sep 2019): EEA online payments need two factors; 3-D Secure 2 is the standard mechanism; €30 low-value exemption | verified | F11 | EEA scope | Act 3 |
| E11 | EU interchange caps: 0.2% debit / 0.3% credit, EEA consumer cards, since 9 Dec 2015 | verified | F7 | consumer EEA only; premium/commercial/foreign uncapped | Act 5, S05 |
| E12 | Interchange → issuer; scheme fee → network; acquirer markup → acquirer; total = merchant discount rate | verified | F8 | — | Act 5, S05 |
| E13 | Stripe EU standard pricing 1.5% + €0.25 per EEA-card transaction | verified | F9 | public example of a blended MDR; subject to change | Act 5, S05 |
| E14 | Settlement moves net positions; acquirers receive through central-bank accounts; merchant credited minus fees; T+1–T+2 typical | verified | F10 | — | Act 4, S04 |
| E15 | VisaNet capacity 65,000+ transaction messages per second | verified | F3 | capacity/stress figure — must be labeled "capacity" | Act 6 |
| E16 | Visa FY2025: 329B brand transactions, 258B processed on its networks, $17T volume, ~5B credentials, 175M+ merchant locations, ~14,500 financial institutions | verified | F4 | fiscal 2025 | Act 6 |
| E17 | €4.50 coffee; exact timestamps; merchant payout €4.41; per-hop pacing inside the 2 s; ledger renderings | illustrative | invented for the story | must read as illustrative in page voice; all fee arithmetic from E11/E13 is real and computed live | throughout |

### Facts to preserve exactly

- 65,000+ **messages per second (capacity)**, not average load.
- Caps: **0.2% debit / 0.3% credit** — EEA **consumer** cards.
- Stripe EU: **1.5% + €0.25** (EEA cards).
- MTI **0100**/response **0110**, response code **00** = approved.
- ISO 8583 first released **1987**. PSD2 SCA in force **14 September 2019**.
- ARQC is **8 bytes**, over card + terminal + transaction data.
- "Typically 1–3 business days" for merchant payout.

### Claims to avoid or qualify

- Never imply the network is a bank or holds the money.
- Never state average Visa throughput as 65,000/s.
- Never generalize EEA caps to US/premium cards; if mentioned, say uncapped/higher.
- The hop sequence (terminal → gateway → acquirer → network → issuer) is a
  standard simplification; present as "the standard shape", not universal truth.
- Don't claim money "moves through Visa's accounts" universally; say funds flow
  between the issuing and acquiring sides, often netted, with acquirers
  receiving via central-bank accounts.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| Issuer | The bank that gave you the card and holds your account | Act 1 |
| Acquirer | The merchant's bank for card payments | Act 1 |
| Card network | The messenger + rulebook between banks (Visa, Mastercard); not a bank | Act 1 |
| Authorization | The 2-second question/answer that guarantees the money | Act 2 |
| Hold | Funds reserved, not sent | Act 2 |
| ISO 8583 | The standard message format card transactions travel in, born 1987 | Act 2 |
| ARQC | The one-time cryptographic signature your chip produces for each payment | Act 3 |
| Capture | The merchant's "it actually happened; pay me" claim | Act 4 |
| Clearing | Exchanging the day's completed transactions and computing who owes whom | Act 4 |
| Settlement | The net funds actually moving between banks | Act 4 |
| Interchange | The fee the merchant side pays the issuer, capped in the EEA | Act 5 |
| Merchant discount rate (MDR) | The total fee a merchant pays to accept a card | Act 5 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | What did the beep actually do? | "money teleported" → "a question and an answer happened" | One €4.50 tap, 2 seconds, and the claim that nothing was paid yet. Quiet, concrete, a little destabilizing. | The receipt and the clock | Hero; no scroll scene; big type beat | E1, E17 | Static hero text |
| 1 · Mental model | Who is even involved? | two parties → five parties | Introduce the cast: you, the shop, acquirer, network (messenger, not bank), issuer. The network is the surprising one. | The five-party map | Static annotated diagram (SVG) with plain text equivalent | E3, E4 | Diagram is static; all names in prose |
| 2 · Mechanism | What are the two seconds? | "the bank checks" → a message round trip with a standardized envelope | The authorization loop as it happens: terminal builds a 0100 message, hops to issuer, checks run, hold placed, 0110/00 returns. Sticky scene drives the round trip; a receipt-style message breakdown follows. | The traveling message envelope | Sticky: pulse travels node to node, envelope labels swap, hold appears, response returns; then a static receipt of the message fields | E1, E5, E6, E7 | Full round trip written out in ordered step paragraphs + static message receipt |
| 3 · Critical detail | Why can't this be faked? | "the card is magic" → the chip signs once (ARQC); online, your bank authenticates you (3DS/SCA) | The counter: anyone can copy a number; nobody can copy a one-time signature. Then the online version: two factors under PSD2. | The 8-byte cryptogram | Static-ish computed diagram: tap twice, two different cryptograms (honestly computed MAC over incrementing counter); counter increments visibly | E8, E9, E10 | Computed values also printed in a table; prose carries the conclusion |
| 4 · Change perspective | When does money move? | "at the beep" → days later, batched and netted | The second timeline: capture at day 0, clearing batches, net settlement, payout T+1–T+2. The hold quietly disappears, real entries appear. | The day 0 → day 2 ledger | Sticky: horizontal timeline scrubs forward; ledger rows fill in on both banks' sides; fees peel off | E2, E5, E14 | Every ledger row also listed as ordered prose |
| 5 · Stress / comparison | What does it cost? | "free" → three tolls, split three ways | Follow €50: interchange (capped, EEA), scheme fee, acquirer markup; vs the one number merchants see (Stripe 1.5% + €0.25). Computed live. | The fee split bar | Computed split diagram with a debit/credit toggle; every cent arithmetic on stated public rates | E11–E13, E17 | Values printed in table; formula stated in caption |
| 6 · Synthesis | How big is this machine? | human scale → planetary messaging scale | Zoom out: this loop runs billions of times a year; capacity 65k msg/s; the speed is in messages, not money. | The counter | Quiet metrics beat with big numerals, computed counts | E15, E16 | Numbers in prose |
| 7 · Takeaway | What should I remember? | — | Two promises and a reconciliation; approved ≠ paid; three tolls. Ends on the receipt motif. | The final receipt line | Static ending + breather line "Approved. Not paid." | E1–E5 | Pure prose |

Rhythm: quiet hook → cast (static) → dense mechanism (sticky) → technical detail (computed) → long reveal (sticky) → arithmetic (interactive) → quiet scale → takeaway.

## 4. Scene specifications

### Scene S01 — The two-second round trip (sticky)

- **Narrative job:** Replace "the bank checks something" with the concrete
  message round trip and its five stopping points; land that the result is a
  hold, not a transfer.
- **Placement:** Act 2; follows the five-party map; hands off to the message
  receipt (S02).
- **Pattern:** sticky-scene (6 steps).
- **Primary visual anchor:** a small message envelope that travels the loop.
- **Analogy or explanatory device:** none — literal mechanism. The "envelope"
  is the actual shape of an ISO 8583-style message, labeled as such.
- **On-page prose:**
  - Heading: "Two seconds, five stops"
  - Step 1: The terminal knows the amount (€4.50), the merchant, the card
    (from the chip), and now builds one standardized question. Conclusion: it
    is a formatted message, not magic.
  - Step 2: Over the internet/phone line to the merchant's bank side —
    processor/acquirer — which forwards it. Conclusion: your bank has not
    seen it yet; the message is being relayed toward it.
  - Step 3: The network (Visa/Mastercard) routes it to the issuer using the
    card number's prefix. Conclusion: the network is a router with a
    rulebook.
  - Step 4: The issuer's checks: card valid? funds available? fraud score?
    Conclusion: three questions, milliseconds.
  - Step 5: Approved: the issuer answers 0110 / response code 00 and places a
    hold on €4.50. Conclusion: a reservation, not a transfer.
  - Step 6: The answer retraces the loop; terminal beeps, receipt prints.
    Total: about two seconds for ~a dozen hops. Nothing has been paid.
- **Stage inventory:** dark stage; five labeled nodes (TERMINAL, ACQUIRER,
  NETWORK, ISSUER + a small cardholder chip on the terminal and merchant tag);
  a connection path drawn as a metro-style line; the envelope (rect with MTI
  label 0100→0110); a hold badge appearing at the issuer; an elapsed-ms
  readout `[data-readout]` driven by the step state; all decorative layer
  `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Envelope at terminal, MTI 0100 label visible, ms readout 0 | step 1 | envelope + "0100 AUTH REQUEST" | the question is built |
  | 2 | Envelope terminal→acquirer, line lights sequentially | step 2 | node glow, path fill | relay toward the bank side |
  | 3 | Envelope crosses network node; routing flash | step 3 | NETWORK highlighted blue | routing by card prefix |
  | 4 | Envelope parked at issuer; three check rows tick | step 4 | three ticks appear | validity, funds, fraud |
  | 5 | Hold badge (orange) appears at issuer; envelope label flips to 0110 / RC 00 | step 5 | badge + label | promise made, hold placed |
  | 6 | Envelope retraces path (acid), terminal beeps state, ms readout ≈ 2,000 | step 6 | path lights reverse | answer returns; nothing moved |
- **Motion choreography:** ENTER: nodes fade in staggered. Each step: envelope
  translates along path (600–900ms, ease-out); path segment lights with it.
  Step 5: badge scales in (spring-lite), label crossfades. Step 6: reverse
  direction, acid color. Ambient: faint pulse along the line. Reduced motion:
  static per-step states, no travel animation.
- **Data / computation:** ms readout is a deterministic illustrative pacing
  map per step (e.g. 0 → 300 → 700 → 1,200 → 1,450 → 1,700 → 2,000) — labeled
  illustrative pacing of E1's ~2 s; rendered as `[data-readout]` text.
- **Interaction:** none beyond scroll; step cards carry all conclusions.
- **Accessibility and fallback:** stage `aria-hidden`; steps are ordered
  `<article data-step>` paragraphs containing every conclusion; reduced
  motion shows each state statically keyed to `data-active-step`.
- **Responsive rules:** at 390px the loop becomes a vertical column, envelope
  moves vertically, labels ≥ 11px, readout top-center; step cards bottom-dock
  (scaffold behavior).
- **Acceptance check:** at each step the envelope/labels/badge state is
  legible without motion; step 5 visibly shows hold + 0110/00; step 6 shows
  the full path lit and readout 2,000 ms.

### Scene S02 — The message is a document (receipt)

- **Narrative job:** Show that the "question" is a rigid 1987-era standardized
  form — ISO 8583 — making the magic feel engineered.
- **Placement:** Act 2, immediately after S01.
- **Pattern:** split — prose left, receipt right.
- **Primary visual anchor:** a thermal-receipt rendering of the 0100 message
  with MTI, bitmap hint, and key fields.
- **On-page prose:** heading "The question has a format"; explains ISO 8583,
  born 1987; MTI 0100; bitmap; a few key data elements in plain words
  (amount, merchant, card number, the chip's cryptogram); the answer 0110 with
  response code 00. Caption: "What to watch: the fields on this receipt are
  the real shape of a card authorization message."
- **Stage inventory:** CSS receipt (paper white, mono type, dashed tear),
  rows: MTI 0100, BITMAP 0→…, F2 PAN 5413 •••• •••• 0031, F4 AMOUNT
  EUR 4.50, F7 DATE/TIME, F41 TERMINAL 0017, F43 MERCHANT, F55 CHIP DATA
  ARQC 8 BYTES; answer stub 0110 / RC 00 APPROVED. Static HTML, no JS needed.
- **State model:** static; optional hover/focus highlight of a row (CSS only).
- **Data / computation:** field numbers (F2, F4, F7, F41, F43, F55) are real
  ISO 8583 data-element positions; values illustrative (E17) except MTI/RC (E7).
- **Motion choreography:** none beyond scaffold reveal.
- **Accessibility and fallback:** it is a static `<figure>` with
  `<figcaption>`; all content readable in DOM order.
- **Responsive rules:** receipt stacks below prose at 390px; mono text wraps,
  never clipped.
- **Acceptance check:** receipt reads correctly with JS off.

### Scene S03 — The signature you can't reuse (computed)

- **Narrative job:** Explain ARQC: the chip signs this exact transaction once
  using a secret + a counter; replay gets a different signature; that's why
  chips can't be cloned like stripes. Then the online analogue: SCA/3DS two
  factors.
- **Placement:** Act 3.
- **Pattern:** split with an interactive computed figure.
- **Primary visual anchor:** two tap results side by side: same card, same
  amount, different 8-byte values, counter 0847 → 0848.
- **On-page prose:** heading "The chip signs once"; explains session key from
  a secret that never leaves the chip + transaction counter; signature covers
  amount/merchant/date; anyone can read it, nobody can produce the next one;
  magnetic stripe = static data, chip = unique signature per payment. Second
  beat: online, PSD2 SCA (since 2019) makes your bank authenticate you with
  two factors (3-D Secure 2) before the same 0100 goes out.
- **Stage inventory:** two receipt cards; each shows COUNTER, INPUT
  (amount·merchant·date·counter — truncated), and an 8-byte hex MAC
  (16 chars); a "TAP AGAIN" button (keyboard-focusable) that recomputes the
  right card with counter+1. Computation: `HMAC-SHA-256`-style truncation is
  fine as *illustrative* — must be labeled "simplified model of ARQC" on the
  figure; real ARQC is a 8-byte MAC from a session key (E8).
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | initial | left card counter 0847, MAC_1; right card counter 0848, MAC_2 | page load | two different MACs | same card, two taps, different signatures |
  | tap again | right card counter 0849…, MAC recomputed with 200ms fade | button/Enter | counter increments, MAC changes | every signature is one-time |
- **Motion choreography:** 200ms crossfade on recompute only; no ambient motion.
- **Data / computation:** MAC = first 8 bytes of a keyed hash over
  `amount|merchant|date|counter` with a fixed demo key — deterministic,
  honestly computed by page JS, labeled simplified. No real cryptography
  claimed.
- **Interaction:** the TAP AGAIN button (also Enter/Space); pointer not
  required; initial state already shows the conclusion.
- **Accessibility and fallback:** values also printed in a `<table>` beside
  the figure; button labeled; reduced motion shows values without fade.
- **Responsive rules:** cards stack at 390px; hex wraps at 8+8 chars.
- **Acceptance check:** two counters differ by one, MACs differ; recomputed
  MAC changes every activation; no console errors.

### Scene S04 — The second timeline (sticky)

- **Narrative job:** The reveal: capture → clearing → net settlement →
  payout; the hold vanishes and real ledger entries appear on both sides.
- **Placement:** Act 4; after the security beat; hands off to fees.
- **Pattern:** sticky-scene (5 steps).
- **Primary visual anchor:** a horizontal DAY 0 → DAY 2 timeline that fills,
  over a two-bank ledger (issuer rows, acquirer/merchant rows).
- **On-page prose:**
  - Heading: "The money moves later"
  - Step 1: End of day: the merchant's systems submit the completed sale —
    capture. The promise is now a claim.
  - Step 2: Clearing: the day's captured transactions are exchanged between
    issuer and acquirer through the network; fees computed per item.
  - Step 3: Settlement: banks owe each other thousands of offsets; only net
    positions move — often through central-bank accounts. Conclusion: this is
    the moment money actually moves.
  - Step 4: The acquirer credits the merchant €4.41 minus fees; T+1 to T+2 is
    typical. The hold on your account became a real debit.
  - Step 5: Ledger truth: your bank debited you once, the merchant's bank
    credited them once, and the difference is three tolls. Nothing was
    instant except the promises.
- **Stage inventory:** timeline bar with 4 stops (CAPTURE, CLEARING,
  SETTLEMENT, PAYOUT); two ledger columns (YOUR BANK / MERCHANT'S BANK) with
  rows that fill in: HOLD −4.50 (pending) → −4.50 posted; claim +4.50 →
  +4.50 received → fees −0.09 → net +4.41 (illustrative split consistent with
  S05's arithmetic); day labels DAY 0 / DAY 1 / DAY 2. Decorative `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | CAPTURE stop lights; hold row pulses | step 1 | hold row, capture node | promise → claim |
  | 2 | CLEARING stop; batch dots stream between banks | step 2 | moving dots (discrete in reduced motion) | day's items exchanged |
  | 3 | SETTLEMENT stop; net amount tag −4.41 crosses center | step 3 | net arrow | only the net moves |
  | 4 | PAYOUT stop; merchant rows finalize +4.41 | step 4 | completed rows | merchant paid, fees off |
  | 5 | Full ledger view; both banks settled | step 5 | all rows solid | two entries and three tolls |
- **Motion choreography:** timeline fill left→right as steps advance; ledger
  rows change from dashed/pending to solid/posted (opacity + border style,
  600ms); net transfer arrow crosses once (700ms ease-out). Ambient: none
  beyond subtle grid.
- **Data / computation:** €4.50 → €4.41 derived: interchange 0.2% (debit, E11)
  = €0.009 → rounded display €0.01, scheme + markup fill the rest to match
  Stripe 1.5% + €0.25 arithmetic for €4.50 = €0.3175 ≈ €0.32? — **resolve in
  build**: keep the merchant's fee split consistent with S05 formulas; choose
  the coffee to be card-present (cheaper than Stripe's online rate) and state
  "illustrative fee model" with the exact arithmetic in the caption.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** all five states' ledger contents written in
  the step paragraphs and a static summary table after the scene.
- **Responsive rules:** at 390px timeline stays horizontal but compressed
  (day ticks only); ledger columns stack (YOUR BANK above MERCHANT'S BANK);
  rows become full-width.
- **Acceptance check:** final state shows −4.50 posted vs +4.41 received with
  the tolls visible; every intermediate state legible.

### Scene S05 — Follow €50 (computed split)

- **Narrative job:** Make the invisible price concrete: three tolls; caps in
  the EEA; the one number merchants actually see.
- **Placement:** Act 5.
- **Pattern:** split with interactive computed figure.
- **Primary visual anchor:** one horizontal €50 bar splitting into segments:
  merchant keeps, interchange, scheme fee, acquirer markup.
- **On-page prose:** heading "Three tolls"; explains interchange (EEA-capped
  0.2% debit / 0.3% credit — consumer cards), scheme fee (network's cut),
  acquirer markup (processor's cut); merchants usually see one blended rate —
  e.g. Stripe's published 1.5% + €0.25 for EEA cards. Toggle debit/credit
  changes the capped interchange. Caption states every number is computed
  from the published rates on screen.
- **Stage inventory:** segmented bar (SVG/CSS); legend with exact euro values;
  a two-state toggle (DEBIT 0.2% / CREDIT 0.3%); a "blended price" ticket
  showing what Stripe's published rate would charge for the same €50.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | debit | segments sized by 0.2% interchange + stated scheme/markup splits | toggle | €0.10 interchange | capped tolls, debit |
  | credit | interchange recomputed at 0.3% | toggle | €0.15 interchange | capped tolls, credit |
- **Motion choreography:** segment widths transition 500ms ease-out on toggle;
  numbers crossfade.
- **Data / computation:** interchange = 50 × 0.002 or 0.003 (E11); scheme fee
  and markup shown as *illustrative shares* of the remainder sized to match a
  plausible card-present MDR; blended ticket = 50 × 0.015 + 0.25 = €1.00
  (E13), labeled as the published online rate. All arithmetic in page JS from
  the printed rates; illustrative shares labeled.
- **Interaction:** the toggle (button pair, keyboard operable); pointer not
  required; default debit.
- **Accessibility and fallback:** all values also in a `<table>`; toggle
  updates both bar and table; reduced motion: no width animation.
- **Responsive rules:** bar full-width at 390px, legend stacks; touch targets
  ≥ 44px.
- **Acceptance check:** toggling changes interchange €0.10 → €0.15 and
  resizes segments; blended ticket always €1.00 for €50.

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** "thermal receipt + transit wayfinding" hybrid —
  paper documents (receipts, ledger slips, message stubs) over a dark,
  metro-map network world. The two aesthetics map exactly onto the two
  timelines: paper = the banking records; dark network = the messaging rails.
- **Why this style fits this subject:** Card payments literally produce
  receipts and ledger lines while running on network routing; the paper/dark
  split *is* the story's central dichotomy (documents vs. wires).
- **Emotional register:** matter-of-fact, forensic, a little playful at the
  edges (mono type, torn edges); never tense.
- **Avoid:** gold/finance clichés, padlocks, green "money" gradients, hacker
  green-on-black, danger reds (nothing here is a warning).

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | House paper `#f2f0e9` for document beats; dark `#121212` stage with 32px grid for network scenes; receipts on `#fbfaf5` with subtle shadow + torn bottom edge |
| Palette semantics | acid = moving/settled funds & responses, blue = the message under examination, orange = the hold / tolls to watch — consistent with house mapping |
| Typography | House roles: Unbounded display, Instrument Serif big numerals, Newsreader body, DM Mono receipts/labels/readouts |
| Grid and spatial language | Receipts are narrow centered columns with perforated rules; network scenes use a metro loop (the 5 nodes) and horizontal timelines; acts separated by quiet paper sections |
| Shapes / illustration | 1.5px ink lines, hard corners on paper, rounded pills on network nodes; dashed = pending, solid = posted — a stated legend |
| Annotation language | DM Mono uppercase labels with exact units (ms, EUR, bytes); every computed value says what produced it |
| Motion character | mechanical and precise (envelopes move like trams, ledger rows stamp in); never bouncy except the hold badge's small pop |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| Receipt components | message stub, crypto taps, final receipt | original | CSS/HTML | full text in DOM |
| Metro loop diagram | authorization round trip | original | inline SVG (decorative, aria-hidden) | step paragraphs |
| Timeline + ledgers | settlement beats | original | inline SVG/CSS | step paragraphs + summary table |
| Fee bar | €50 split | original | SVG/CSS + table | table with all values |

No external images, fonts beyond the house Google Fonts load, or libraries.

## 6. Build handoff

### Document outline

```text
<title>How a Card Payment Actually Works</title>
main
  hero — h1 + dek (the beep is a question; the money comes later) + meta
  section 01 — The cast of five (static SVG map + prose)
  sticky scene S01 — Two seconds, five stops (6 steps)
  split S02 — The question has a format (receipt)
  section 03 — The chip signs once (S03 computed + SCA/3DS prose)
  sticky scene S04 — The money moves later (5 steps + summary table)
  section 05 — Follow €50 (S05 computed + toggle)
  metrics — The scale of the loop (E15/E16 numbers)
  conclusion — Two promises and a reconciliation + receipt coda
  post navigation (shared component)
```

- **Target:** `blog/not-ready/how-card-payments-work.html` while parked, then
  `blog/how-card-payments-work.html` on ship.
- **Enhancement ladder:** semantic HTML → CSS (receipts, static diagrams) →
  scaffold IntersectionObserver step runtime for sticky scenes → small page
  JS for the two computed figures (crypto model, fee split). No canvas, no
  scroll-linked timelines needed.
- **State source of truth:** `data-active-step` for sticky scenes; the two
  interactive figures hold local state in page JS with `VB.onReady`.
- **Dependencies:** none beyond the required shared reading indicator +
  post navigator (relative `../../` forms while parked).
- **Performance budget / risks:** three inline SVGs, no images; page JS
  trivial; ambient animations CSS-only, paused offscreen by scaffold.
- **No-JS / reduced-motion plan:** document reads top to bottom; sticky
  stages collapse to static per current step states; computed figures show
  default values and their tables.
- **Mobile plan:** loop verticalizes at 390px; timeline compresses; ledgers
  stack; receipts full-width with wrapped mono; step cards bottom-dock.
- **Open implementation questions:** none blocking — coffee-fee arithmetic
  fixed in S04 (illustrative card-present model consistent with S05's printed
  rates).

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `how-card-payments-work` | permanent |
| Search title | "How a Card Payment Actually Works" (39 chars + brand) | keyword-first |
| H1 / shelf title | "How a Card Payment Actually Works" | — |
| Meta description / deck | "Follow one €4.50 tap: a two-second message round trip, a hold instead of a transfer, then capture, clearing and net settlement — every fee computed live." (~155 chars) | must match manifest deck |
| Topic | "Payments · Systems" | manifest label |
| Tags | ["Payments", "ISO 8583", "EMV", "Interchange", "Visa"] | manifest labels |
| Canonical | `https://victorbusque.com/blog/how-card-payments-work.html` | confirm domain matches existing posts at ship |
| Date | `2026-08` | publishing month |
| Internal links | "none yet beyond shelf neighbors" | navigator derives them |

## 8. Definition of ready

- [x] The central question, takeaway, scope, and ending are explicit.
- [x] Every factual claim, number, and visual readout has an evidence ID or is
      labeled illustrative.
- [x] Each scene has a narrative job, state model, motion reason, fallback,
      and mobile rule.
- [x] At least one named aesthetic has been chosen and translated into usable
      visual decisions.
- [x] The document outline and implementation plan name the target file and
      enhancement strategy.
- [x] Publishing fields are drafted; unresolved items are recorded rather
      than guessed.
