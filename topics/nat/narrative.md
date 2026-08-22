---
topic: "nat"
status: built
language: en
source_context: topics/nat/context.md
created: 2026-08-22
updated: 2026-08-22
intended_slug: how-nat-works
---

# One address, millions of machines

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article. Complete every bracketed prompt with decisions grounded in
> `context.md`. This is not research notes and not final HTML copy: it is
> the agreed narrative, visual, interaction, and implementation plan a
> frontend developer can build without guessing.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Uses the internet daily; knows "IP address" as a vague identity; has heard "you're behind NAT" without a model. No networking background. |
| Central question | How can one IP address represent thousands — and a small pool of them, millions — of machines? |
| One-sentence answer | Because every IP address carries 65,536 numbered ports, and a NAT swaps each machine's private address for its own address plus a free port, keeping a lookup table so replies can be swapped back — an ISP can run that same table for an entire city. |
| Core takeaway | An IP address stopped being a machine's name and became a lease on 65,536 slots; the translation table — not the address — is what routes packets home, and whoever owns the table owns the rules. |
| Why it matters | It explains concrete daily life: why you can't host a game for a friend, why sites occasionally call you a criminal's neighbor, why your public IP is your neighbor's too, and why the fix (IPv6) is taking so long. |
| Scope and exclusions | TCP/UDP IPv4 NAT only; no NAT64/464XLAT internals, no IPv6 packet format, no firewalling claims, no measured ISP subscriber-per-address figures (computed arithmetic only, labeled illustrative). |
| Narrative point of view | Follow one packet out and its reply back; then zoom out to the ISP running a million-row ledger. |
| Reading language | English. |

### Reader journey

```text
Before: "An IP address is a machine's name — one address, one device."
Bridge: The port wall (one address = 65,536 numbered slots) and the live
        translation table (a real state machine the reader scrolls through).
After:  "An address is a mailbox bank; NAT is the clerk swapping return
        addresses in a ledger; scale the clerk to a city and a /24 fronts
        a million machines."
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** There are about 4.3 billion IPv4
  addresses — fewer than one each for the world's 8 billion people — yet
  ~17-device households stream, call, and game without a care. The whole
  trick is a 16-bit field nobody talks about, and a clerk that rewrites
  envelopes.
- **Ending (1–3 sentences):** One IP address fronts a household; with port
  rationing, one address fronts a whole apartment block and a small pool
  fronts a city — millions of machines that will never have an address of
  their own. NAT bought the internet time by turning addresses from names
  into rented slots; IPv6, now carrying roughly half of Google's traffic,
  is the plan to give every machine its name back.

## 2. Evidence and editorial boundaries

The page may only make claims this table can support. Cite source labels or
anchors that exist in `context.md`; do not promote an inference into a fact.
Use "illustrative" for values invented solely to explain a mechanism, and
make those values visibly illustrative in the page.

| ID | Claim or datum that may appear | Type: verified / inference / illustrative | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | IPv4 = 32 bits → 4,294,967,296 addresses | verified | Core mechanism; RFC 793 header size | exact arithmetic | hero, act 1 |
| E2 | 16-bit ports → 65,536 per address (TCP & UDP) | verified | Core mechanism | exact | act 2 port wall |
| E3 | Well-known ports 0–1023; dynamic range 49152–65535 (16,384 ports) | verified | RFC 6335 via context §Terminology | exact | act 2 |
| E4 | NAT rewrites source IP+port, keeps table, reverses replies; unsolicited inbound dropped | verified | RFC 2663 / 3022 / 1631 | settled | acts 2–4 |
| E5 | Private ranges 10/8, 172.16/12, 192.168/16 | verified | RFC 1918 | exact | act 2 |
| E6 | IANA free pool depleted 3 Feb 2011; last five /8s to RIRs | verified | ARIN vault announcement | exact date | act 1 |
| E7 | RIR milestones: APNIC Apr 2011, RIPE NCC Sep 2012, LACNIC Jun 2014, ARIN Sep 2015 | verified | Wikipedia/RIRs | year-level only in copy | act 5 sidebar |
| E8 | World population passed 8 billion 15 Nov 2022 | verified | UN | exact date, copy says "about 8 billion" | hero, act 1 |
| E9 | Average US internet household: 17 connected devices (Q3 2023, n=8,000) | verified | Parks Associates | survey scope US | act 5 calculator default |
| E10 | 100.64.0.0/10 reserved for CGN shared space; 4,194,304 addresses; not globally routable | verified | RFC 6598 | exact | act 4 |
| E11 | CGN must support per-subscriber external port limits, configurable | verified | RFC 6888 REQ-4 | "MUST support", value varies | act 5 |
| E12 | Freed port not reused ≥120 s (TCP MSL); deterministic blocks like 1000–1999→A are the exception | verified | RFC 6888 REQ-8 | exact seconds | act 3 aside |
| E13 | Out of quota → drop new packet, ICMP host-unreachable SHOULD, never evict existing mappings | verified | RFC 6888 REQ-11 | exact | act 5 stress |
| E14 | Abuse tracing: operators log protocol, subscriber id, external addr/port, timestamp per mapping | verified | RFC 6888 §4 | exact fields | act 4 |
| E15 | Sharing breaks: console gaming between co-address subscribers, geolocation to the CGN, per-IP login limits, P2P/SIP inbound | verified | RFC 6269 via RFC 6598 §5.2 | list as documented issues | act 5 |
| E16 | Hole punching: outbound mapping first, then inbound accepted; STUN/TURN/ICE standardize it | verified | RFC 4787 vocabulary; RFC 8445/8489/8656 | mechanism only | act 6 |
| E17 | Google IPv6 stats ~45–50% of users (Apr 2026) | verified | Google via Wikipedia | date-labeled, weekday spread | ending |
| E18 | IPv4 secondary market ≈ $27.75/address average in 2025, −16% YoY | verified (secondary) | IPv4Center | market-report estimate, "≈" | act 1 aside |
| E19 | Linux netfilter idle timeouts: UDP 30 s unreplied / 120 s assured, TCP established 5 days | verified | context §Core mechanism | illustrative in simulator | act 3 |
| E20 | Subscribers/address = 64,512 ÷ ports granted; devices = subscribers × devices/home; pool tables | inference (computed) | arithmetic on E2, E3, E9, E11 | labeled COMPUTED, illustrative ratios | act 5 calculator |
| E21 | NAT proposed 1994 (RFC 1631) as a short-term fix; private space RFC 1918 1996 | verified | RFC dates | exact years | act 1 |
| E22 | The article's packet/ledger demo values (192.168.1.20:51724 → example.com:443 etc.) | illustrative | reserved doc ranges (RFC 5737 spirit) + invented ports | visibly illustrative | acts 2–4 |

### Facts to preserve exactly

- 4,294,967,296 · 65,536 · 0–1023 · 49152–65535 · 100.64.0.0/10 · 120 s ·
  3 Feb 2011 · 15 Nov 2022 · 17 devices (Q3 2023, US, n=8,000).

### Claims to avoid or qualify

- Never state how many subscribers a real ISP puts behind one address — use
  the computed table only, labeled illustrative (context §Disagreements).
- Never call NAT a firewall; say unsolicited packets "have no row to match".
- Port-block sizes (512/1024/2048) presented as examples, not a standard.
- IPv4 price quoted with "≈" and "market report"; no investment framing.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| port | one of 65,536 numbered slots an address offers per transport | act 2 |
| NAT | the family of boxes that swap private addresses for their own public one | act 1 |
| translation table | the NAT's ledger: outside slot ↔ inside machine | act 2 |
| port forwarding | a hand-written permanent ledger row (invite, not demand) | act 3 |
| CGNAT | the same ledger, operated by the ISP, shared across subscribers | act 4 |
| hole punching | both peers open outbound rows first so inbound passes after | act 6 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | Wait — my whole house has ONE address? | "IP = machine" → "IP is scarce; devices outnumber addresses" | 4.29 B addresses, 8 B people (E1, E6, E8); scarcity dates; the promise: one 16-bit field + a clerk. | hero counter: addresses per person ticking to a fraction | load-in count, no scroll dependency | E1 E6 E8 E18 E21 | prose + static numbers |
| 1 · Mental model | What IS an address if not a name? | address = machine → address = mailbox bank with 65,536 slots | The port wall: an address is 65,536 numbered slots (E2); well-known bottom rows, your laptop picks from the top (E3). Postal analogy with limits stated. | 256×256 grid of slots (one dot per port), ranges tinted | split scene, hover-free static tint; entrance stagger | E2 E3 | grid static, ranges labeled in text |
| 2 · Mechanism | How does my packet use a slot? | "the internet sees my packet" → "the clerk rewrites it" | THE LEDGER: outbound rewrite, row appended; reply matched and swapped back; second device gets second row. Every value computed. | live translation table + two packet slips | sticky scene, 6 steps keyed to data-active-step | E4 E5 E22 | steps as stacked prose, table rendered as HTML table |
| 3 · Critical detail | What does the ledger cost me? | "it just works" → "table = rules: no row, no entry; rows expire; rows are memory" | Unsolicited inbound dropped (why no hosting); idle expiry (why things time out) with honest 30 s/120 s/5-day timeouts (E19); port forwarding = permanent row; the box stopped being a wire (end-to-end note). | a red packet arriving with no row → DROP counter (computed) | sticky scene, 4 steps | E4 E12 E19 | prose carries each rule |
| 4 · Change perspective | Who else runs a ledger? | "NAT is my router" → "my ISP runs a city-sized one" | CGNAT: same mechanism, rented scale; 100.64.0.0/10 stage (E10); double NAT as two clerks in series; abuse tracing logs every row (E14). | two ledgers in series (home + ISP), one packet crossing both | sticky scene, 4 steps | E10 E14 E4 | stacked prose, series described in text |
| 5 · Stress / comparison | How far can one address stretch? | "sharing is rare" → "arithmetic of rationing" | Ports per subscriber is a dial (E11); computed: subscribers/address, devices/address, pool tables to a million (E20); exhaustion when the block runs out: drop, don't evict (E13); documented breakage list (E15); exhaustion dates (E7). | the dial + live computed readouts; port strip divided into per-subscriber blocks | interactive calculator (real inputs, computed outputs) + metrics | E7 E9 E11 E13 E15 E20 | calculator works without JS? No — falls back to a precomputed table of 3 example settings, labeled computed |
| 6 · Synthesis | How do games and calls even work? | "NAT blocks inbound" → "outbound-first punches a hole" | Hole punching: two peers open rows to each other; tables line up; STUN discovers, ICE tries, TURN relays when it fails (E16). | two mini-ledgers, arrows meeting mid-stage | sticky scene, 4 steps | E16 | prose sequence |
| 7 · Takeaway | So what is an address now? | full model | Ending prose states the answer plainly; IPv6 as the name-back plan (E17); closing callout. | none (breather + prose) | — | E17 | pure prose |

Rhythm: hook (loud) → port wall (quiet, wide) → ledger (dense, signature) →
rules (dense, small stage) → CGNAT (reveal) → calculator (interactive,
loud) → hole punch (kinetic) → quiet ending.

## 4. Scene specifications

### Scene S01 — The port wall

- **Narrative job:** replace "address = machine" with "address = 65,536
  numbered slots" before any packet moves.
- **Placement:** Act 1; after the hero prose; hands off the ledger scene
  (a slot will be claimed there).
- **Pattern:** split scene, bounded visual right.
- **Primary visual anchor:** a 256×256 grid — one small dot per port, the
  whole address on one wall.
- **Analogy or explanatory device:** mailbox bank in an office tower: one
  street address, thousands of numbered boxes. Limit (stated in copy): the
  wall is per-transport (TCP has one wall, UDP another) and boxes are
  claimed per conversation, not owned forever.
- **On-page prose:** heading "An address is 65,536 mailboxes." Steps: (1)
  the count and where it comes from (2^16, E2); (2) bottom rows reserved
  (0–1023, servers listen low; E3); (3) your laptop picks a free box near
  the top (49152–65535, E3) each time it starts a conversation.
- **Stage inventory:** CSS grid of 256×256 dots (aria-hidden; 65,536
  elements is heavy — render 64×64 groups? No: render 256 columns × 256
  rows as one dot each is 65,536 divs — too heavy. Build it as an SVG or
  canvas-free CSS `background` of radial-gradient tiling with three
  overlaid labeled range bands). Decision: a single div wall using
  repeating radial-gradient dots + absolutely-positioned translucent range
  bands (well-known, registered, ephemeral) with count labels. No per-port
  DOM. A "claimed slot" highlight is a single glowing dot positioned in the
  ephemeral band (step 3), labeled with a real computed port number
  (e.g. 51,724 — illustrative, E22).
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | settle | wall fades in, bands draw | reveal observer | "65,536 SLOTS" readout | the whole address at a glance |
  | reserve | well-known band tints orange | step 2 active | "0–1023 · RESERVED" label | servers listen low |
  | claim | one dot glows acid in ephemeral band | step 3 active | "51,724 · CLAIMED BY YOUR LAPTOP (ILLUSTRATIVE)" | clients pick high |
- **Motion choreography:** ENTER wall opacity+scale (decelerate); HOLD band
  tint crossfade; TRANSFORM single dot pop + count-up of readout; EXIT none.
- **Data / computation:** 65,536, 1,024, 16,384 are literals from E2/E3;
  the claimed dot position is computed from its port number ((port − 49152)
  mapped into the band's rect). One paragraph states: "If every dot were a
  grain of rice…" — no, keep numeric only.
- **Interaction:** none.
- **Accessibility and fallback:** stage aria-hidden; every count appears in
  adjacent DOM text; reduced-motion shows the fully-tinted static wall.
- **Responsive rules:** at 390px the wall becomes 128-wide (CSS scales via
  aspect-ratio; dot pitch halves, labels outside); bands keep labels ≥ 8px.
- **Acceptance check:** the wall shows exactly three labeled bands whose
  counts sum to 65,536; the claimed dot sits inside the labeled ephemeral
  band at any width.

### Scene S02 — The ledger (signature)

- **Narrative job:** the core mechanism — watch one packet get rewritten,
  one row born, one reply matched and swapped back.
- **Placement:** Act 2; after the port wall; hands off the rules scene.
- **Pattern:** sticky-scene, 6 steps.
- **Primary visual anchor:** the translation table — three rows of
  mono-set "ledger slips" — above a packet lane with two endpoints
  (INSIDE 192.168.1.0/24 · OUTSIDE 203.0.113.7).
- **Analogy or explanatory device:** clerk rewriting return addresses on
  envelopes leaving a building, keeping a clipboard so replies can be
  re-addressed. Limit (stated): the clerk also picks the slot number and
  destroys rows that go quiet — more power than any clerk.
- **On-page prose:** heading "Watch one packet become a ledger row."
  Steps: (1) laptop 192.168.1.20:51724 → example.com:443, packet leaves;
  (2) router swaps source to 203.0.113.7:50123 — a free slot it chose —
  and writes the row; (3) server replies to 203.0.113.7:50123; router
  matches the row, swaps destination back, delivers; (4) phone
  192.168.1.34:40,001 wants out too — same public address, different slot:
  50124; (5) a collision demo: laptop reboots and re-picks 50123? No —
  step 5 is "the server only ever saw the router; from outside, the whole
  house is one machine with many slots"; (6) teardown note: rows are
  temporary (bridge to Act 3).
- **Stage inventory:** packet slip (bordered mono card showing
  FROM/TO with swappable values, aria-hidden); two endpoint plates; ledger
  table (aria-hidden mirror); readout `[data-readout]` shows computed
  "ROWS: n". All addresses illustrative but RFC-correct in shape
  (192.168/16 private, 203.0.113/10 doc range, E22).
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | packet on inside lane, original FROM/TO | step 1 | slip values | private source |
  | 2 | slip crosses router midline, FROM swaps mid-crossing | step 2 | row 1 stamps in | rewrite + row |
  | 3 | reply slip enters from outside, TO swaps back | step 3 | row 1 flashes acid | match + reverse |
  | 4 | second packet from phone, slot 50124 | step 4 | row 2 stamps | multiplexing |
  | 5 | outside view: endpoints collapse, only router visible | step 5 | inside dims to 20% | one address, many slots |
  | 6 | both rows fade at 40% opacity with TO-counters | step 6 | "TTL" chips appear | state expires |
- **Motion choreography:** ENTER slip slides inside→router (ease-swift);
  TRANSFORM field swap is a crossfade on the two value spans (the one
  thing to watch); row stamps (translateY + settle, like a printed slip);
  HOLD; EXIT rows fade but never disappear before step 6's text lands.
  Each state is a named CSS class keyed off data-active-step; reverse
  scroll replays exact inverses (pure CSS states, no JS timeline).
- **Data / computation:** a page script builds the exact table HTML from a
  literal event list (deterministic); ROWS count and TTL chips are computed
  from that list — nothing hand-drawn that pretends to be dynamic.
- **Interaction:** none (scroll is the control).
- **Accessibility and fallback:** each step's paragraph states the full
  row contents in mono inline text (`203.0.113.7:50124 ⇄ 192.168.1.34:40001`);
  no-JS shows stage (static final table) then stacked steps.
- **Responsive rules:** at 390px the slip stacks FROM/TO vertically, ledger
  rows wrap to two lines per row, lane endpoints shrink to labels; nothing
  under the bottom-docked card (stage uses flex-start + padding per
  scaffold's mobile rules).
- **Acceptance check:** at step 2 the slip's FROM reads exactly what row 1
  shows as outside; at step 3 the reply's TO matches row 1 before the swap
  and the inside address after.

### Scene S03 — No row, no entry

- **Narrative job:** the ledger's rules as consequences, not trivia: drops,
  expiry, memory, and the one exception (port forwarding).
- **Placement:** Act 3; after the ledger; hands off CGNAT.
- **Pattern:** sticky-scene, 4 steps, small stage.
- **Primary visual anchor:** a red inbound slip hitting the router and
  falling, with a computed DROPPED counter.
- **Analogy or explanatory device:** none — literal is clearer.
- **On-page prose:** heading "The table decides everything." Steps:
  (1) a stranger sends to 203.0.113.7:50200 — no row — dropped (why you
  can't host); (2) rows expire: 30 s UDP quiet / TCP days (E19,
  illustrative-netfilter label); (3) port forwarding = a permanent
  hand-written row; (4) every row is RAM — the router now participates in
  every conversation (end-to-end principle, one sentence, no lecture).
- **Stage inventory:** router plate; inbound slip; DROP bin with computed
  counter; TTL chips; a "PERMANENT" stamp for step 3.
- **State model:** 1 red slip falls, counter 1→computed n; 2 rows show
  countdown chips expiring; 3 one row gets PERMANENT stamp, stops expiring;
  4 row-blocks pulse softly (ambient), "STATE = MEMORY" label.
- **Motion choreography:** fall = accelerate + rotate slightly (it means
  rejection, not grace); expiry = chip countdown text swap then row
  opacity out; PERMANENT stamp = scale-settle press.
- **Data / computation:** counter increments per scripted attempt (3
  scripted attempts, computed as attempts.length); TTL chips display the
  literal values with the netfilter-source label.
- **Interaction:** none.
- **Accessibility and fallback:** every rule restated in step prose;
  drop counter value also in prose ("three attempts, three drops").
- **Responsive rules:** slip shrinks; drop bin stays right of router; at
  390px stack vertically, keep counter ≥ 8px mono.
- **Acceptance check:** DROPPED count equals the number of red slips that
  reached the router at any scroll position.

### Scene S04 — Two clerks in series (CGNAT)

- **Narrative job:** scale change of perspective — the ISP runs the same
  ledger; your packet crosses two.
- **Placement:** Act 4; hands off the calculator.
- **Pattern:** sticky-scene, 4 steps.
- **Primary visual anchor:** two stacked ledger plates labeled HOME and
  ISP, one packet crossing both.
- **Analogy or explanatory device:** hotel front desk forwarding to a
  building, building to a district courier depot — limit stated: the two
  clerks don't share notes, which is exactly why some things break (bridge
  to Act 5's breakage list).
- **On-page prose:** heading "Your ISP runs one too." Steps: (1) the ISP's
  edge ledger: your router's whole house is one inside row to it;
  (2) 100.64.0.0/10 — a private stage bigger than needed for exactly this
  (E10); (3) one public address shared with your neighbors — the outside
  world can't tell your street apart (E14: every row logged for abuse
  tracing); (4) double NAT defined; you control one clerk, not the other.
- **Stage inventory:** HOME plate (act-2 table mini), ISP plate (same
  component, different values), packet slip crossing, a row counter on the
  ISP plate climbing to a labeled "CITY-SIZED (ILLUSTRATIVE)" density bar.
- **State model:** 1 packet crosses HOME (row 1) and stops at ISP edge;
  2 ISP row stamps (your house = one inside endpoint); 3 neighbor devices
  appear as more ISP rows, same outside address, distinct slots — density
  bar fills; 4 both plates labeled, "WHO OWNS THE TABLE OWNS THE RULES"
  readout.
- **Motion choreography:** crossings as in S02 (consistency teaches);
  density bar fills decelerate; nothing else moves.
- **Data / computation:** ISP rows shown = 6 scripted neighbors ( computed
  list), slots 50,001+ ascending collision-free — generated by the page
  script, count honest.
- **Interaction:** none.
- **Accessibility and fallback:** prose states the series and the shared
  outside address explicitly; no-JS shows final state plates + steps.
- **Responsive rules:** plates stack HOME above ISP at 390px, crossing
  becomes vertical arrow; labels keep size.
- **Acceptance check:** ISP plate's outside column shows one identical
  address on every row with distinct ports.

### Scene S05 — The rationing dial (calculator)

- **Narrative job:** let the reader prove the headline arithmetic
  themselves — this is where "millions" becomes honest.
- **Placement:** Act 5; after CGNAT; hands off hole punching.
- **Pattern:** interactive calculator + metrics + comparison strip.
- **Primary visual anchor:** a big computed number — DEVICES BEHIND ONE
  ADDRESS — reacting to two inputs.
- **Analogy or explanatory device:** none; numbers only.
- **On-page prose:** heading "How far does one address stretch?" Copy:
  usable slots ≈ 64,512 (65,536 − 1,024 reserved; approximate); the ISP
  dials ports-per-subscriber (REQ-4, E11); everything below is computed
  from the dial. Inputs: PORTS PER SUBSCRIBER (256–8,192, step 256),
  DEVICES PER HOME (1–40, step 1, default 17 = E9). Outputs (computed):
  subscribers/address; devices/address; a /24 pool row; a /22 pool row;
  a strip visual of the 64,512-slot strip divided into per-subscriber
  blocks. Below: what happens at exhaustion (drop, don't evict, E13) and
  the documented breakage list (E15) + exhaustion dates (E7) as a sidebar.
- **Stage inventory:** two range inputs (keyboard accessible, labeled);
  4 computed readout cards; slot-strip SVG with per-subscriber blocks;
  PRESET buttons: RATIONED (1024), GENEROUS (4096), MOBILE (256)
  labeled illustrative presets, not ISP facts.
- **State model:** single state recomputed on input; strip blocks
  regenerate (≤ 126 blocks) with distinct tints alternating two hues;
  readouts count up (VB.motion.countUp).
- **Motion choreography:** only value changes animate (decelerate count-up,
  strip blocks crossfade). No ambient loops.
- **Data / computation:** subscribers = floor(64512/portsPer); devices =
  subscribers × devicesPer; /24 = devices×256; /22 = devices×1024; all
  rendered with thousand separators; every card labeled COMPUTED FROM YOUR
  DIAL. No-JS: precomputed table for presets 1024/2048/4096 (rendered
  server-side in HTML), labeled computed.
- **Interaction:** both sliders + presets fully keyboard operable
  (native inputs), `aria-live="polite"` on the headline output.
- **Accessibility and fallback:** preset table in DOM carries the same
  numbers; slider labels in text.
- **Responsive rules:** cards 2×2 grid → 1 column at 390px; strip stays
  full-width, block labels hidden below 480px (blocks remain tinted).
- **Acceptance check:** at default (1,024 × 17): 63 subscribers, 1,071
  devices per address, 274,176 per /24 — page shows exactly these.

### Scene S06 — The hole punch

- **Narrative job:** resolve the "inbound is blocked" tension — the trick
  that makes games, calls and WebRTC work anyway.
- **Placement:** Act 6; before the ending prose.
- **Pattern:** sticky-scene, 4 steps.
- **Primary visual anchor:** two facing mini-ledgers (YOU / FRIEND), one
  arrow each, meeting mid-stage.
- **Analogy or explanatory device:** both people call each other's
  switchboards at once, so each switchboard has a row when the other's
  call arrives. Limit: only works when boxes behave predictably (many do;
  TURN relays when they don't).
- **On-page prose:** heading "Two tables, one trick." Steps: (1) STUN: each
  side first asks a broker "what do I look like from outside?" (learns its
  public address+slot, E16); (2) both fire outbound at the other's
  discovered endpoint — each row exists before the other's packet lands;
  (3) tables line up: full-speed direct conversation; (4) when it fails,
  TURN relays everything — slower, but always works.
- **Stage inventory:** two ledger cards (left/right), broker chip top
  center, two packet arrows, mid-stage meeting point glow on success.
- **State model:** 1 both sides pulse broker, addresses appear on their
  slips; 2 arrows leave both sides simultaneously; 3 arrows cross, both
  tables flash acid, steady beam establishes; 4 beam reroutes through a
  TURN relay chip, labeled relay.
- **Motion choreography:** simultaneous departure is the point — arrows
  animate with identical timing; beam = dashed line solidifying (dash
  offset), never pulsing after establishment.
- **Data / computation:** endpoint values illustrative (E22), mirrored
  between the two slips exactly (acceptance depends on the mirroring).
- **Interaction:** none.
- **Accessibility and fallback:** the four-step prose is complete on its
  own; stage decorative.
- **Responsive rules:** cards stack top/bottom at 390px, arrows rotate to
  vertical via the SVG's mobile transform; meeting point stays centered.
- **Acceptance check:** left slip's discovered endpoint equals the right
  card's original address and vice versa, at every width.

### Scene S07 — Ending

- **Narrative job:** state the answer in prose; name the exit (IPv6).
- **Placement:** Act 7. Pattern: breather + prose + callout.
- **Visual anchor:** breather line "An address is a lease on 65,536 slots."
- **Copy:** ending paragraph per §1; IPv6 sentence with E17 date label;
  callout: "Whoever owns the table owns the rules."

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** night-sorting-office ledger — the house
  editorial system (paper, ink, dark stage, acid/blue/orange semantics)
  with a postal-clerk motif: mono ledger slips, stamp-set rows, envelope
  packet cards.
- **Why this style fits this subject:** the mechanism IS clerical —
  rewriting addresses, stamping rows, expiring records. The aesthetic
  makes the table the protagonist instead of decorating around it.
- **Emotional register:** precise, calm, quietly astonished at the scale.
- **Avoid:** padlocks/shields (no security-theater), globe tropes, speed
  lines, any implication the demo is live traffic.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | house tokens as-is: paper prose, `--stage` dark canvases, 32px grid |
| Palette semantics | acid = a row born/matched (settled), blue = the packet under examination, orange = the field to watch/dropped inbound, red only for the drop bin |
| Typography | Unbounded headings, Newsreader body, DM Mono for every address/port/ledger value (addresses never in serif), Instrument Serif for the breather and big computed numerals |
| Grid and spatial language | lanes (inside/outside) separated by a dashed router midline; ledger rows as full-width slip cards; left mono labels |
| Shapes / illustration | 1px ink borders, square corners on slips, subtle stamp rotation (−1deg) on newly-born rows only |
| Annotation language | `ILLUSTRATIVE` chip on invented values; `COMPUTED` chip on derived ones; all caps mono 9-10px |
| Motion character | clerical: stamps settle, slips cross, nothing bounces; ambient = row TTL chips ticking |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| port wall | 65,536 slots at a glance | original | CSS gradient tiling + band overlays | counts in prose |
| ledger slips | translation table | original | styled divs, mono text | full rows in step prose |
| slot strip | rationing blocks | original | inline SVG generated by JS | counts in readouts |

No external assets. Google Fonts stylesheet stays the only third-party
presentation dependency.

## 6. Build handoff

### Document outline

```text
<title>How NAT Works: Millions Behind One IP — Víctor Busqué</title>
main
  hero — "One address, millions of machines." + dek + meta (POST 13)
  prose 01 — The shortage that made the trick necessary
  split S01 — the port wall
  prose 02 — bridge to mechanism
  sticky S02 — THE LEDGER (6 steps)
  sticky S03 — NO ROW, NO ENTRY (4 steps)
  prose — port forwarding aside + end-to-end note
  sticky S04 — TWO CLERKS (CGNAT, 4 steps)
  interactive S05 — THE RATIONING DIAL + exhaustion sidebar
  sticky S06 — THE HOLE PUNCH (4 steps)
  breather + prose 03 — ending, IPv6
  callout + tags + footer
```

- **Target:** `blog/not-ready/how-nat-works.html` while building; ships to
  `blog/how-nat-works.html` with the four chrome references switched
  `../../` → `../`.
- **Enhancement ladder:** semantic HTML + prose conclusions → CSS states
  keyed to `data-active-step` (scaffold runtime untouched) → one page
  script for computed readouts/table generation/slider math. No canvas, no
  custom scroll handlers, no MutationObservers.
- **State source of truth:** `data-active-step` on each sticky section +
  deterministic literal event lists in the page script; readouts filled via
  `VB.onReady` / `VBScene.onStep`.
- **Dependencies:** none beyond the two shared chrome components (the
  required exception) and Google Fonts.
- **Performance budget / risks:** port wall must not be 65,536 DOM nodes —
  CSS tiling only; slot strip capped at ≤ 253 blocks; no rAF loops at all
  (count-ups use VB.motion.countUp); total file target < 150 KB.
- **No-JS / reduced-motion plan:** every scene's stage is decorative
  (aria-hidden), all conclusions in step/prose text; the calculator shows
  the preset table (computed values in HTML); reduced-motion collapses to
  the stacked document per scaffold.
- **Mobile plan:** stages flex-start with tight top padding (scaffold
  portrait rules); S02 ledger rows two-line wrap; S06 arrows rotate;
  sliders full-width, 44px touch targets.
- **Open implementation questions:** none.

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `how-nat-works` | permanent, keyword-first |
| Search title | How NAT Works: Millions Behind One IP — Víctor Busqué | 53 chars |
| H1 / shelf title | One address, millions of machines. | display title |
| Meta description / deck | Watch one packet get its address rewritten by a NAT table, then see the same table scale to a whole ISP — the honest arithmetic of millions behind one IP. | 156 chars |
| Topic | Networks · NAT | manifest label |
| Tags | NAT, CGNAT, IPv4, Ports | manifest labels |
| Canonical | `https://engineering.victorbusque.com/blog/how-nat-works.html` | matches CNAME |
| Date | 2026-08 | publishing month |
| Internal links | `blog/starlink.html` (packet journey kinship) via prose link; post-nav handles neighbors | one contextual link in ending |

## 8. Definition of ready

Mark `status: ready-for-build` only when all apply:

- [x] The central question, takeaway, scope, and ending are explicit.
- [x] Every factual claim, number, and visual readout has an evidence ID or
      is labeled illustrative.
- [x] Each scene has a narrative job, state model, motion reason, fallback,
      and mobile rule.
- [x] At least one named aesthetic has been chosen and translated into
      usable visual decisions.
- [x] The document outline and implementation plan name the target file and
      enhancement strategy.
- [x] Publishing fields are drafted; unresolved items are recorded rather
      than guessed.
