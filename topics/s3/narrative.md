---
topic: s3
status: ready-for-build
language: en
source_context: topics/s3/context.md
created: 2026-08-21
updated: 2026-08-21
intended_slug: how-s3-works
---

# How One S3 Upload Earns Eleven Nines

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article. It teaches an engineer who has dragged a file into an S3 bucket (or
> only heard the “eleven nines” marketing line) what the service actually does
> between `PUT` and `200 OK`, and why that design — not heroic hardware — is
> where the durability number comes from.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Junior-to-mid engineers who know HTTP (`PUT`/`GET`, status codes), files, disks, and maybe the AWS console. They have no model for Availability Zones, erasure coding, metadata/data-plane separation, or what a durability “design target” means. |
| Central question | What is physically true about your data at the instant S3 returns `200 OK` — and how does that add up to “eleven nines”? |
| One-sentence answer | By the time S3 acknowledges a `PUT`, your object has been split into erasure-coded shards stored across at least three physically separate Availability Zones, and a strongly consistent metadata record points to them; eleven nines comes from spreading risk across failure domains and continuously repairing losses, not from any single reliable disk. |
| Core takeaway | Durability is a loop, not a hardware grade: shard data across independent failure domains, acknowledge only after redundancy is met, then detect and repair losses forever — and remember the loop protects against infrastructure failure, not against your own authorized `DELETE`. |
| Why it matters | This model explains why S3 latency is milliseconds rather than microseconds, what AWS’s “designed for” actually promises (a modeled target, not a measured loss rate), why accidental deletion needs versioning, and how to reason about trade-offs like S3 Express One Zone. |
| Scope and exclusions | Teach: object/bucket/key model, metadata–data separation, the write path, erasure coding mechanics, the repair loop, the read path, strong consistency since December 2020, durability-vs-availability-vs-backup. Exclude: the storage-class catalog (only Standard vs Express One Zone appears), pricing, SLA credits, IAM/bucket-policy detail, Glacier retrieval, cross-region replication mechanics (one sentence at most), cell-based deployment and shuffle sharding internals, and comparisons with Ceph/HDFS/GFS. Internal subsystems (ShardStore, Physalia, the witness) appear only as attributed sidebar facts, never as invented internals. |
| Narrative point of view | Follow one object — an illustrative `videos/aurora.mp4` — through the machine on its way in (write), while the machine breaks around it (stress), and on its way out (read). |
| Reading language | English. |

### Reader journey

```text
Before: “S3 is a giant, very reliable hard drive in the cloud; eleven nines
        means AWS buys exceptionally good disks.”
Bridge: One upload splits into shards across three buildings; the system only
        says “done” once redundancy exists, and a repair loop holds the
        redundancy there forever; a separate index answers every read.
After:  “S3 is two cooperating systems — a strongly consistent metadata index
        and an erasure-coded storage fleet — spread across failure domains.
        Durability is a race between failure and repair, won by design.”
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** You upload one video, and in about a second S3 says `200 OK`. AWS’s design target for that object is 99.999999999% yearly durability — store ten million objects and you’d expect to lose one every ten thousand years. Here is what happened to your bytes in that second.
- **Ending (1–3 sentences):** S3’s durability is not a property of any disk, rack, or building — it is a design loop: split every object into shards, spread them across at least three Availability Zones, acknowledge only when redundancy is real, and repair losses faster than the world can cause them. The same loop explains what S3 is not: not a local disk, and not a backup against your own `DELETE`. When you meet any storage system, ask where its metadata lives, how its data is spread, when it says “done”, and what repairs it.

## 2. Evidence and editorial boundaries

The illustrative object (`videos/aurora.mp4`, 42 MB) and the shard scheme
(6 data + 3 parity) are narrative-owned teaching values; S3’s real erasure
parameters are not public. Every scene readout derived from them is labeled
illustrative on the page.

| ID | Claim or datum that may appear | Type: verified / inference / illustrative | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | S3 is an object store: objects identified by a key within a bucket; the namespace is flat and “folders” are key-prefix conventions; bucket names are globally unique, buckets live in one region. | verified | Perplexity → “API and namespace”; sources [1][7][8] | Long-standing public API behavior. | Act 1; S02 |
| E2 | Standard-class durability is designed to be 99.999999999% per object-year; AWS frames this as: 10,000,000 objects would lose one every 10,000 years. It is a modeled design target, not a measured loss-rate promise. | verified | Perplexity → “Durability design” (sources [2][3]); Deepseek pro → “§5 Resilience and Durability”; Gemini → “Multi-AZ Spatial Distribution” | Keep “designed for” / “modeled” wording everywhere. | Acts 0, 4; S01, S05 |
| E3 | Standard storage classes store data redundantly across at least three AZs in a region; the design is meant to withstand the loss of an AZ (AZs have independent power, cooling, networking). | verified | Perplexity → “Durability design” (sources [2][3][5]); Deepseek pro → “§5”; ChatGPT → “Multi-AZ and Multi-Region Replication” | “At least three”; never a specific rack/node layout. | Acts 2–4; S03–S05 |
| E4 | The storage layer splits object data into chunks and uses erasure coding (data plus parity shards) for durability at lower overhead than full replication; exact code parameters are not public. | verified (mechanism) / caveat | Perplexity → “Storage layer” (sources [6][14]); Deepseek pro → “§2 Write Path”, “§5 Erasure coding”; Gemini → “Reed-Solomon Erasure Coding Mechanics”; ChatGPT hedges — see “Claims to qualify” | Present as the documented mechanism; never state real k/m values for S3. | Acts 2–3; S03–S04 |
| E5 | Writes are acknowledged only after redundancy targets for the storage class are met; the metadata record is inserted/updated after data placement, then `200 OK` returns. | verified | Perplexity → “Write Path” (sources [2][3][4][5][11][14]); Deepseek pro → “§2 Write Path · Durable acknowledgement” | Ordering claim is about acknowledgement vs. visibility, not internal step timing detail. | Act 2; S03 |
| E6 | Reads look up metadata to resolve shard locations, then fetch enough shards in parallel to reconstruct; using the fastest-responding shards improves tail latency; reads can be served by fewer than all shards. | verified | Perplexity → “Read path” (sources [6][9][11]); Deepseek pro → “§3 Read Path” | Simplified: internal retries/redirects mentioned at most in passing. | Act 5; S06 |
| E7 | Background processes continuously verify checksums, scrub stored data for bit rot, and reconstruct lost or corrupt fragments from surviving shards — minimizing time-to-repair is central to the durability target. | verified | Perplexity → “Storage layer”, “Durability design” (sources [2][3][4][5][6]); Deepseek pro → “§5 Continuous anti-entropy and repair”; ChatGPT → “Background Operations” | Repair speeds/fleet sizes are not quantified. | Acts 3–4; S04–S05 |
| E8 | Availability is a separate axis: S3 Standard is designed for 99.99% yearly availability (≈ tens of minutes of downtime per year). | verified | Perplexity → “Availability design” (sources [2][3][6][10][12][13]); Deepseek pro → “§6” | Distinguish design target from the 99.9% SLA credit line; SLA detail is out of scope. | Act 5; S06 caption |
| E9 | Since December 2020, S3 provides strong read-after-write consistency for all operations in all regions, at no extra cost — a `PUT`/`DELETE` is immediately visible to subsequent `GET`/`LIST`. | verified | AWS source [15]; Perplexity → “Consistency model” | Use December 2020 (AWS announcement); ignore ChatGPT’s lone “April 2021” date. | Act 6; S07 |
| E10 | Reported mechanism: strong consistency was retrofit without dropping caches, using per-object operation ordering plus an in-memory “witness” acting as a read barrier; a read falls through to the authoritative tier when the cache can’t be proven fresh. | verified (as reported) / attribution required | Gemini → “The Strong Read-After-Write Consistency Engine” (source [13], hidekazu-konishi summary of AWS re:Invent content); Perplexity → “Consistency model” (source [4]) | Present as “as AWS engineers have described”; internal names are illustrative of the published description, not API. | Act 6; S07 |
| E11 | Multipart upload splits large objects into parts uploaded in parallel; a final Complete call atomically assembles them into one object version. | verified | Perplexity → “Write path” (sources [1][9][12]); Deepseek pro → “§2” | One caption-level mention; no size thresholds taught beyond “large”. | Act 2; S03 caption |
| E12 | Long-published performance guidance: ~3,500 writes/s and ~5,500 reads/s per prefix, scalable by spreading keys across prefixes; AWS has since softened this guidance as partition splitting automated. | verified / dated guidance | Deepseek (simple) → “Performance Scaling via Prefixes”; Deepseek pro → “§8 Horizontal partitioning” (“legacy guidance… less important today”) | Present as historically documented ceilings, now softened — never as current hard limits. | Act 7 |
| E13 | S3 Express One Zone keeps data in a single AZ (co-located, directory buckets, session-based auth) for single-digit-millisecond latency, trading multi-AZ resilience; AWS still quotes 11-nines durability within the AZ, but AZ loss is not survived. | verified | Gemini → “S3 Express One Zone” sections (sources [3][16][18]); Deepseek pro → “§7 S3 Express One Zone” | Sidebar comparison only; do not turn into a product guide. | Act 5; S06 sidebar |
| E14 | ShardStore is S3’s publicly described (SOSP ’21) Rust key-value storage node managing raw disk extents with a decoupled LSM index, validated with the Shuttle model checker. | verified / sidebar | Gemini → “Storage Node Architecture: ShardStore” (sources [4][5][7][8], SOSP ’21 paper) | Named attribution: “as published by AWS researchers”. No invented internals. | Act 7 sidebar |
| E15 | Physalia is S3’s publicly described metadata store built from millions of small consensus cells placed topology-aware, bounding failure blast radius (“Millions of Tiny Databases”, USENIX ’20 lineage). | verified / sidebar | Gemini → “Distributed Metadata and Micro-Consensus” (sources [9][10][11]) | Same attribution rule; one sidebar sentence. | Act 7 sidebar |
| E16 | Durability guarantees do not protect against authorized deletes or overwrites; versioning, Object Lock, and backups address logical mistakes. | verified | Perplexity → “Design implications” (sources [2][5][8][9][3][4]) | Core honesty beat; never presented as a weakness hidden by AWS. | Act 7; S08 |
| E17 | Cross-region replication is asynchronous (eventual across regions) and exists for regional-disaster resilience; within a region S3 is strongly consistent. | verified | Deepseek pro → “§8 Global distribution patterns”; ChatGPT → “Multi-AZ and Multi-Region Replication” | One sentence maximum in this article. | Act 7 |
| E18 | Every request is authenticated and authorized (SigV4/IAM/policies) at stateless front-end servers before touching data or metadata. | verified | Perplexity → “API and namespace” (sources [9][11][14]); Deepseek pro → “§1 Front-end plane” | A gate in the write/read paths, not a security tutorial. | Acts 2, 5; S03, S06 |
| E19 | `videos/aurora.mp4` (42 MB) sharded 6+3 into nine 7 MB shards; overhead 63/42 = 1.5×; tolerates any 3 shard losses; whole-AZ loss (3 shards) leaves exactly 6 = k; 3× full replication would cost 126 MB = 3.0×. | illustrative | Narrative-owned deterministic model | Label “illustrative shard scheme — S3’s real parameters are not public” in every scene that shows it. | S03–S05 |
| E20 | Sequence numbers 101/102, cache and witness states in the consistency scene. | illustrative | Narrative-owned model, after E10’s published description | Caption: “simplified after AWS’s published description”. | S07 |

### Facts to preserve exactly

- “Designed for” durability/availability: always keep the qualifier; AWS presents 11 nines as a modeled design target (E2).
- The 10-million-objects / one-loss-per-10,000-years framing is AWS’s own; attribute it, don’t blur it into a guarantee (E2).
- “At least three Availability Zones” for Standard classes (E3).
- Strong consistency since December 2020, all operations, all regions, no extra cost (E9).
- Acknowledgement order: redundancy met → metadata visible → `200 OK` (E5).
- Durability ≠ availability ≠ backup: three different axes, never used interchangeably (E2, E8, E16).

### Claims to avoid or qualify

- ChatGPT frames Standard as “effectively 3× replication across AZs” with erasure coding “likely added”; other sources and AWS material describe erasure coding as the storage-layer mechanism. Resolution: teach multi-AZ redundancy (E3, safe) + erasure coding as the documented shard mechanism (E4), and say explicitly that AWS does not publish the exact scheme per class. Never state “S3 keeps three full copies.”
- Never present the 6+3 illustrative scheme as S3’s real parameters (E19).
- Do not quantify repair fleet size, repair time, or shard counts per AZ as fact (E7, E19).
- The witness/read-barrier description comes from AWS engineering talks summarized by third parties: attribute as “as AWS engineers have described”, and keep it as a mechanism sketch, not a specification (E10).
- Per-prefix 3,500/5,500: dated guidance, softened by AWS; never state as current hard limits (E12).
- Do not manufacture an outage narrative (fires, specific incidents); failure events in scenes are explicitly hypothetical failures of a disk/node/AZ (E3 supports survivability claims only).
- Latency: say “milliseconds to tens of milliseconds” character; do not attach benchmark numbers (E6, E8 context).
- Ignore ChatGPT’s “April 2021” consistency date; December 2020 per AWS (E9).

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| object / bucket / key | An object is the bytes plus metadata, named by a key (e.g. `videos/aurora.mp4`) inside a bucket; keys are flat strings — “folders” are just shared prefixes. | Act 1 |
| Availability Zone (AZ) | One or more separate datacenters in a region with independent power, cooling, and networking. | Act 1 |
| shard | One erasure-coded slice of an object: a data shard (part of the original bytes) or a parity shard (computed recovery information). | Act 2 |
| erasure coding | Splitting data into k data shards plus m parity shards so any k of the total can rebuild the whole — durability at a fraction of full-copy cost. | Act 2 |
| parity | Computed “spare” information: like a checksum, but strong enough to regenerate missing shards, not just detect errors. | Act 3 |
| metadata plane | The index system holding each object’s record: key, size, version, and pointers to where shards live. | Act 1 |
| data plane / storage fleet | The servers and disks that hold the actual erasure-coded bytes. | Act 1 |
| redundancy target | The minimum placement (shards across failure domains) that must exist before S3 says “stored”. | Act 2 |
| scrubbing / repair | Continuous background verification (checksums) and reconstruction of lost or corrupt shards from survivors. | Act 3 |
| durability vs availability | Durability: stored data is not lost. Availability: the service answers requests. Independent axes. | Act 4/5 |
| storage class | A named durability/latency/cost trade-off (e.g. Standard vs Express One Zone). | Act 5 |
| strong read-after-write consistency | Once a write is acknowledged, every subsequent read sees it — immediately. | Act 6 |
| witness | In AWS’s published description, the component that tracks the latest version per object so cached reads can be checked for freshness. | Act 6 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | What did I just trust? | “200 OK means saved somewhere” → “200 OK is an extreme, engineered promise” | One upload, one second, `200 OK`. Set the stakes with AWS’s own framing: ten million objects, one loss per ten thousand years. Promise: here is what happened to your bytes in that second. | A single object card and the eleven-nines promise stamped beside it. | Object card settles; the promise “11×9” stamps in; a faint wireframe of the machine teases behind. | E2, E19 | Object card + promise as static labeled figures; prose carries the hook. |
| 1 · Mental model | What kind of thing am I talking to? | “A big hard drive / folder tree” → “An object store: a flat key space served by two cooperating systems” | Introduce bucket+key, flat namespace, no real folders. Then the load-bearing split: a metadata plane (the index card: key, size, version, shard pointers) and a data plane (the bytes). Everything later hangs on this split. | One object visually separating into an index card and a stream of bytes. | The object splits; card and bytes take two labeled lanes; three AZ silhouettes appear under the bytes lane. | E1, E3, E18 | Two labeled boxes (index card, bytes) above three AZ outlines; full prose. |
| 2 · Mechanism | What happens between PUT and 200 OK? | “Bytes go to a disk, then I get a reply” → “Auth → shard fan-out across ≥3 AZs → redundancy met → metadata commit → only then 200” | Walk the write path gate by gate: authenticate at a stateless front-end (E18); stream bytes; split into 6+3 illustrative shards; fan out across disks, nodes, and three AZs; the ack gate stays shut until the redundancy target is met; then the metadata record commits and `200 OK` releases. Caption beat: very large objects arrive as parallel multipart parts (E11). | The closed ack gate with nine shard flights in progress. | Shards fly along three rails (AZ 1/2/3); gate light turns from “waiting” to “stored” only when all placement checks tick; index card writes last. | E3, E4, E5, E11, E18, E19 | Numbered write-path diagram: 1 auth, 2 shard, 3 place, 4 commit metadata, 5 200 OK. |
| 3 · Critical detail | Why shards instead of copies? | “Redundancy = backup copies” → “Erasure coding: any k of n rebuilds; overhead is a fraction; parity is regenerative math” | Slow down on the encoding itself with the illustrative 6+3 scheme: nine 7 MB shards, 1.5× overhead vs 3.0× for three full copies — more survivability per byte. Then introduce the loop: checksums, scrubbing, reconstruction. Durability is redundancy held in place by repair. | Nine shard tiles in a 3×3 grid, three per AZ; the “any 6 of 9” rule. | Grid tiles color/pattern-split into data vs parity; the rule “any 6 suffice” illuminates; overhead meter compares 1.5× vs 3.0×. | E4, E7, E19 | Static shard grid with legend, the rule in text, and the overhead comparison as a small table. |
| 4 · Stress | What happens when the machine breaks? | “Redundancy is for show until tested” → “Lose a disk, a node, a whole AZ — object stays readable; repair restores margin” | Interactive stress: knock out shards one by one; readout stays green until fewer than 6 remain. Kill an entire AZ — exactly 6 survive, still readable, zero margin — which is why repair speed is the real durability engine. Then watch reconstruction refill. State plainly: 11 nines is the modeled outcome of this loop (E2). | The same 3×3 grid, now with failure controls and a recoverability readout. | Clicked shards dim to failure hatching; counter “6 of 9 needed, 6 alive” holds; AZ-kill collapses one row; repair sweep regenerates tiles. | E2, E3, E4, E7, E19 | Failure buttons work without scroll animation; a static “worst case” card shows the AZ-loss state with counts. |
| 5 · Read path & trade-offs | How do the bytes come back — and what is this system not? | “S3 reads the file from disk” → “Metadata first, then parallel shard fetch (fastest 6), reconstruct, stream”; “S3 is universal storage” → “A regional object store with ms-scale latency; Express trades AZ redundancy for single-digit ms” | GET walks the same doors in reverse: auth, metadata lookup resolves shard locations, parallel fetch of enough shards — fastest responders win — reconstruct, stream. Availability note: 99.99% design target ≈ tens of minutes/year (E8). Sidebar: Express One Zone keeps everything in one AZ for single-digit ms — durability target still 11 nines, but the AZ itself is now the single point of failure (E13). | Six of nine shard tiles racing home to reassemble the object. | Shards lift from three AZ rows and converge; fastest six highlighted; the object reassembles and streams out. | E6, E8, E13, E18, E19 | Ordered read-path steps in text plus a resolved “reassembled” figure with the fastest-six labeled. |
| 6 · Consistency | What do I read right after I write? | “Caches probably serve stale data” → “Since Dec 2020, reads are guaranteed fresh: per-object ordering + a witness read barrier” | The problem: fast caches vs fresh answers. The reported solution: every write takes a sequence number per object; a witness tracks the latest committed version; a cached read is served only if proven fresh, otherwise it falls through to the authoritative store. Timeline: write v2 → witness bumps → stale cache blocked → GET returns v2. Attribution beat: “as AWS engineers have described” (E10). | A per-object timeline: v1 → v2 write, sequence marker 102, a cache lane blocked by the witness. | v2 lands with sequence 102; witness pointer advances; a read attempts the cache lane and is visibly checked, then served fresh. | E9, E10, E20 | Static two-lane diagram (write lane, read lane) with the rule in prose: acknowledge only what every later read can see. |
| 7 · Synthesis | What is the whole machine — and what does it not promise? | “A pile of tricks” → “One coherent machine with four questions you can reuse”; “11 nines protects me” → “It protects against hardware, not against my own DELETE” | Assemble the full schematic: front door, two planes, three AZs, repair loop, consistency layer — with quiet sidebar attributions (ShardStore, Physalia as published research; E14, E15). Then the honesty beat: an authorized `DELETE` is a valid command — durability does not cover you; versioning does (E16). One sentence on CRR for regional disasters (E17). Close with the four questions. | The complete machine on one card, then the four-question diagnostic. | Layers of the final diagram light up in the order the article introduced them; labels simplify to the four questions. | E12, E14, E15, E16, E17 | The full labeled schematic as a static figure; four questions as a real list in DOM order. |

## 4. Scene specifications

### Scene S01 — One second, one promise

- **Narrative job:** Replace “200 OK means saved somewhere” with “200 OK is an extreme, specifically engineered promise,” and set the stakes the article will cash out.
- **Placement:** Act 0; opens the article; hands off to the object-store model.
- **Pattern:** Full-bleed hook with compact figure.
- **Primary visual anchor:** One object card — `videos/aurora.mp4 · 42 MB` — beside a stamped “99.999999999% / yr” promise mark.
- **Analogy or explanatory device:** None; literal. The “stamp” is a visual framing of AWS’s published target, labeled as such.
- **On-page prose:**
  - Heading: `One upload, one second, eleven nines`
  - Step 1: “You PUT one 42 MB video (illustrative) and S3 answers `200 OK` about a second later. In that second, AWS accepted a design target of eleven nines of yearly durability for it.”
  - Step 2: “In AWS’s own framing: store ten million objects and you’d expect to lose one every ten thousand years. That is not a disk you can buy — it is a machine. This article follows your bytes through it.”
  - Caption / annotation: “Illustrative object. Durability figure: AWS design target for Standard classes.”
- **Stage inventory:** Decorative `aria-hidden` SVG: object card (filename, size), a progress sliver completing to `200 OK`, the “11×9” promise stamp, faint wireframe of doors/AZ rails behind. All conclusions duplicated in DOM prose.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Object card centered, progress sliver empty | Scene enters | `PUT videos/aurora.mp4` | A ordinary upload begins. |
  | 2 | Sliver completes; `200 OK` chip appears | Step 1 active | `200 OK · ~1 s` | The promise is already made — article explains how. |
  | 3 | Promise stamp presses in; wireframe fades up | Step 2 active | `99.999999999% / yr — design target` | The scale of what was just accepted. |

- **Motion choreography:** ENTER card settles → HOLD at empty sliver → TRANSFORM sliver fills, `200 OK` chip pops → RESOLVE stamp presses with a small squash → EXIT wireframe brightens into S02’s rails. Motion ties the one-second wait to the promise; nothing else moves.
- **Data / computation:** E19 (illustrative object), E2 (durability framing, attributed).
- **Interaction:** None.
- **Accessibility and fallback:** Stage `aria-hidden`; h1/dek and the two steps carry everything. No-JS: static card with `200 OK` and the stamp already shown. Reduced motion: state 3 image only, no transitions.
- **Responsive rules:** At 390px stack card, chip, and stamp vertically; stamp shrinks to a text line “eleven nines — AWS design target”; no color-only meaning.
- **Acceptance check:** A reader who never sees motion can state the article’s stakes: one upload was acknowledged, and the durability target attached to it.

### Scene S02 — Not a disk: a card and a stream

- **Narrative job:** Replace the “big hard drive with folders” model with the object-store model and the metadata/data-plane split that the rest of the article uses.
- **Placement:** Act 1; follows the hook; hands off to the write path.
- **Pattern:** Sticky diagram scene (3 steps).
- **Primary visual anchor:** One object splitting into an “index card” (metadata) and a byte stream (data), above three AZ silhouettes.
- **Analogy or explanatory device:** Library catalog vs stacks: the card names and locates, the stacks hold the material. Mapping: key/size/version/pointers ↔ catalog card; erasure-coded bytes ↔ volumes. Limit, stated in copy: S3 writes the card after the books are placed, the card is itself replicated and is the authority for consistency, and the “volumes” are shards split across three buildings — no library does that.
- **On-page prose:**
  - Heading: `Two systems answer your request: a card and a stream`
  - Step 1: “A bucket holds objects named by flat string keys — `videos/aurora.mp4` is one key, not a path through real folders (E1).”
  - Step 2: “S3 is really two systems. The metadata plane keeps each object’s record — key, size, version, and pointers to its shards. The data plane is the fleet of servers and disks holding the encoded bytes.”
  - Step 3: “They live separate lives on purpose: the card must be always right, the bytes must be never lost. Three Availability Zones — separate buildings with independent power and networks — wait under the data plane.”
  - Caption / annotation: “Every number on the card is real state; the split is the article’s load-bearing model.”
- **Stage inventory:** Decorative `aria-hidden` SVG: object capsule; index card (key, size `42 MB`, version `v1`, `shards → …` pointer field); byte stream as dashes; three AZ outlines labeled AZ 1/2/3; front door glyph. DOM prose carries all labels in text.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Whole object capsule | Scene enters | `videos/aurora.mp4` | The reader’s single mental blob. |
  | 2 | Capsule splits: card left, byte dashes right | Step 1–2 active | two labeled lanes | Two planes with different jobs. |
  | 3 | AZ silhouettes rise under byte lane; card gains `v1` and pointer fields | Step 3 active | `AZ 1 · AZ 2 · AZ 3` | Geography enters; the card holds the map. |

- **Motion choreography:** ENTER capsule → HOLD one beat → TRANSFORM split along a clean seam; card fields populate → RESOLVE AZ outlines draw up → EXIT rails thicken into S03’s write path. The split is the lesson; the seam must be crisp, not exploded debris.
- **Data / computation:** E1, E3, E19 (card fields match the illustrative object).
- **Interaction:** None.
- **Accessibility and fallback:** DOM prose restates card fields and AZ labels; no-JS shows the resolved split as a static figure with `<title>`/`<desc>` (“An object splits into a metadata record and encoded bytes across three Availability Zones”); reduced motion shows state 3.
- **Responsive rules:** At 390px lanes stack vertically (card above bytes above AZ row); AZ outlines become labeled chips; pointer field text wraps.
- **Acceptance check:** Reader can name the two planes and one field each holds — without the animation.

### Scene S03 — The gate stays shut until redundancy is real

- **Narrative job:** Establish the write path and its one non-negotiable rule: acknowledgement comes only after data placement across failure domains; metadata commits last.
- **Placement:** Act 2; follows the split model; hands off to the shard mechanics.
- **Pattern:** Sticky-scene, 5 steps.
- **Primary visual anchor:** The ack gate — a status lock on the response path that reads `storing…` until every placement check ticks.
- **Analogy or explanatory device:** The gate maps to S3 withholding the `200 OK` until redundancy targets are met. Limit, stated: it represents an ordering rule, not a literal component called “gate.”
- **On-page prose:**
  - Heading: `PUT: the reply waits for the shards`
  - Step 1: “The request hits stateless front-end servers: identity and permissions checked before anything touches data (E18).”
  - Step 2: “The stream is cut into an illustrative 6+3 scheme: six data shards plus three parity shards, nine slices of 7 MB (E19 — S3’s real parameters are not public).”
  - Step 3: “Shards fly to separate failure domains — different disks, nodes, and racks inside at least three AZs (E3, E4).”
  - Step 4: “Only when the redundancy target is met does the metadata record commit — key pointing at shard locations — and `200 OK` finally releases (E5). Durability first, visibility second.”
  - Caption: “Big objects travel as multipart parts in parallel, assembled atomically at the end (E11).”
- **Stage inventory:** Decorative `aria-hidden` SVG: auth door glyph; nine shard chips (D1–D6, P1–P3) flowing along three rails into AZ boxes; three placement checkboxes (`AZ 1 ✓ …`); the gate with `storing…`/`stored` states; index card writing last; `200 OK` chip. All step conclusions in DOM text.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Request at auth door; gate shut, `storing…` | Scene enters | `auth ✓` | Nothing touches data unauthenticated. |
  | 2 | Object slices into 9 chips at the seam | Step 2 active | `D1–D6 · P1–P3` | Erasure coding happens on the way in. |
  | 3 | Chips fly three rails; checkboxes tick as AZ placements land | Step 3 active | `AZ 1 ✓ AZ 2 ✓ AZ 3 ✓` | Placement spans failure domains. |
  | 4 | Gate flips `stored`; index card writes; `200 OK` releases | Step 4 active | card `v1 · shards → 9 locations` then `200 OK` | The acknowledgement order is the rule. |

- **Motion choreography:** ENTER request slides to auth → HOLD slicing one beat → TRANSFORM shard flights stagger ~80ms apart along straight rails; checkboxes tick on landing → RESOLVE gate flips, card writes, `200 OK` slides out → EXIT rails persist into S04’s grid. Straight, mechanical paths: shard flight is logistics, not celebration.
- **Data / computation:** E3, E4, E5, E11, E18, E19. Counts (9 chips, 3 AZs) from the illustrative scheme; no timing claims beyond “about a second” in prose (hook framing).
- **Interaction:** None.
- **Accessibility and fallback:** Steps in DOM order carry the full sequence; no-JS shows the resolved figure: numbered steps 1–5 (auth → shard → place → commit → 200 OK). Reduced motion: state 4 static with all checkpoints ticked.
- **Responsive rules:** At 390px rails collapse to three stacked AZ rows, shard chips shrink to `D`/`P` monograms with an HTML legend; the gate becomes a text status line `storing… → stored`.
- **Acceptance check:** Reader can answer “what is the last thing S3 does before returning 200 OK?” — commit the metadata record after redundancy is met.

### Scene S04 — Any six of nine

- **Narrative job:** Replace “redundancy means copies” with the erasure-coding rule — any k of n shards rebuild the object — and its cost advantage over full replication.
- **Placement:** Act 3; follows the write path; hands off to the stress test.
- **Pattern:** Sticky diagram scene (3 steps) with a static comparison panel.
- **Primary visual anchor:** A 3×3 shard grid (three columns = three AZs), six data tiles, three parity tiles, under the rule `any 6 of 9 rebuild`.
- **Analogy or explanatory device:** Parity tiles are “checksums that can redraw missing pieces”: mapping — a checksum detects, parity regenerates. Limit, stated: real parity is linear-algebra recovery information distributed across shards, not a spare copy kept in a corner.
- **On-page prose:**
  - Heading: `Why shards beat copies`
  - Step 1: “Six data shards carry the actual bytes; three parity shards carry computed recovery information. Any six of the nine rebuild the whole 42 MB object (E4, E19).”
  - Step 2: “This costs 1.5× the original size. Three full copies would cost 3.0× — and still die with the third loss in the worst case. Erasure coding buys more survivability per byte (E19 arithmetic, illustrative).”
  - Step 3: “Shards are not parked: checksums are verified on read and by background scrubbing, and anything lost or rotten is reconstructed from survivors (E7). Redundancy is not a state — it is a loop.”
  - Caption: “Illustrative 6+3 scheme. AWS does not publish S3’s real code parameters (E4).”
- **Stage inventory:** Decorative `aria-hidden` SVG: 3×3 grid, column headers AZ 1/2/3; D/P tile legend (pattern + label, not color alone); `any 6 of 9` rule plate; overhead meter comparing `1.5×` vs `3.0×` bars; a small scrub-sweep glyph.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Nine tiles uniform, unlabeled | Scene enters | grid + rule plate | The object exists as nine equal citizens. |
  | 2 | Tiles differentiate: 6 data (D hatch), 3 parity (P dots); rule illuminates | Step 1 active | `D×6 · P×3 — any 6 rebuild` | Roles differ; the rule is collective. |
  | 3 | Overhead meter fills 1.5× vs 3.0×; scrub sweep crosses grid | Steps 2–3 active | `1.5× vs 3.0×`, sweep trail | Cheaper than copies; held in place by repair. |

- **Motion choreography:** ENTER grid assembles → HOLD uniform → TRANSFORM tiles differentiate with pattern fills; rule plate lights → RESOLVE meter bars grow proportionally (1.5 vs 3.0 honest ratio), sweep crosses once → EXIT grid persists as the substrate for S05. Differentiation must be by pattern+label so the meaning survives grayscale.
- **Data / computation:** All from E19: 9 × 7 MB = 63 MB; 63/42 = 1.5×; 3 × 42 = 126 MB = 3.0×. Meter bars use these exact ratios.
- **Interaction:** None here (S05 makes the grid interactive).
- **Accessibility and fallback:** Rule and overhead comparison restated in prose and as an HTML mini-table; grid has `<title>`/`<desc>`; reduced motion shows state 3 with the meter resolved.
- **Responsive rules:** At 390px the grid stays 3×3 but tiles drop to `D`/`P` monograms; overhead meter becomes two HTML rows (“this scheme: 1.5×”, “three copies: 3.0×”).
- **Acceptance check:** Reader can state the rule (any 6 of 9) and why it beats copies on cost, from text alone.

### Scene S05 — Break the machine (interactive)

- **Narrative job:** Prove the rule under failure and reveal the deeper one: durability is the race between failure and repair — an AZ loss leaves exactly zero margin, which is why repair speed is the engine behind eleven nines.
- **Placement:** Act 4; follows the shard rule; hands off to the read path.
- **Pattern:** Constrained simulation with buttons.
- **Primary visual anchor:** The S04 grid, now live: shard tiles are buttons, a recoverability readout reads `readable — margin +2`, and an AZ-kill control collapses one column.
- **Analogy or explanatory device:** None; literal simulation of the stated rule.
- **On-page prose:**
  - Heading: `Lose a disk. Lose a datacenter. Still readable.`
  - Step 1: “Tap shards to fail them (or use the button controls). The object stays readable while at least six survive (E4 rule, E19 numbers).”
  - Step 2: “Kill an entire Availability Zone: three shards gone, exactly six remain — readable, with zero margin. This is the state the repair loop exists to exit (E3, E7).”
  - Step 3: “Trigger repair: survivors regenerate the missing shards into healthy failure domains, restoring margin. Eleven nines is the modeled outcome of this loop running forever — not a property of any disk (E2, E7).”
  - Caption: “Illustrative failures of the 6+3 scheme; S3’s real redundancy and repair go further.”
- **Stage inventory:** SVG grid (informative — needs `<title>`/`<desc>`); nine shard buttons (keyboard focusable, `aria-pressed`); controls `Fail random shard`, `Kill AZ 1`, `Repair all`, `Reset`; readout line `shards alive 9/9 · needed 6 · margin +3 · status: readable/at risk/lost`; repair sweep animation. All state mirrored in an `aria-live` polite readout.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | 9/9 alive, margin +3 | initial / Reset | `readable · margin +3` | Healthy baseline. |
  | 2 | Tapped tiles show failure hatching; counts update | shard button toggle | `alive 8 · margin +2` | Each loss eats margin, not the object. |
  | 3 | One AZ column collapsed | `Kill AZ 1` | `alive 6 · margin 0 · readable` | Survives a building; no slack left. |
  | 4 | Readout warns | alive < 6 | `alive 5 · status: unrecoverable (illustrative)` | The cliff is real but far below one AZ. |
  | 5 | Sweep regenerates hatched tiles into empty slots in other AZ columns | `Repair all` | counts return toward 9/9 | Repair restores margin; the loop closes. |

- **Motion choreography:** ENTER resolved grid → HOLD invite pulse on controls only → TRANSFORM failed tiles hatch; repair sweep crosses left→right regenerating tiles in ~600ms mechanical steps → RESOLVE full grid → EXIT settles toward S06. No tile ever “burns”: failure is hatching/dimming, repair is a steady sweep — the register stays calm because the system’s answer is calm.
- **Data / computation:** Pure E19 arithmetic: alive count, needed = 6, margin = alive − 6; status strings derived; no timing or probability claims.
- **Interaction:** Buttons and controls fully keyboard operable; every state change updates the live readout; `Reset` always available; no pointer-only affordance.
- **Accessibility and fallback:** Grid is informative SVG with `<title>`/`<desc>`; the readout text equals the visual truth; no-JS shows a static “worst case” card: AZ 1 dark, `6 of 9 alive — still readable`, plus the three-step prose. Reduced motion: instant state swaps, no sweep.
- **Responsive rules:** At 390px tiles remain tappable (≥44px targets), controls wrap to a 2×2 button row, readout becomes two short text lines; the lesson (6 needed, AZ loss survivable, repair restores margin) survives in text.
- **Acceptance check:** A reader using only the readout and buttons can answer: “After losing AZ 1, how much margin is left?” (zero) and “What fixes it?” (repair from survivors).

### Scene S06 — GET: six fastest shards win

- **Narrative job:** Complete the round trip — reads are metadata-first, parallel, and reconstruct from enough (not all) shards — and set honest expectations: milliseconds-scale latency, regional scope, and the Express One Zone trade.
- **Placement:** Act 5; follows the stress test; hands off to consistency.
- **Pattern:** Sticky diagram scene (3 steps) + comparison sidebar.
- **Primary visual anchor:** Six shard tiles lifting off from three AZ rows and converging into a reassembling object, the fastest six highlighted.
- **Analogy or explanatory device:** None; literal. “Fastest six win” is the latency insight: reads don’t wait for stragglers.
- **On-page prose:**
  - Heading: `GET: the card answers first, then the shards race`
  - Step 1: “Auth again — then the metadata record resolves which shards hold this version, before any bytes move (E6, E18).”
  - Step 2: “Fetches go out in parallel; only enough shards are needed — the fastest responders win, and the object is reconstructed and streamed (E6). Milliseconds to tens of milliseconds is the honest latency class: a fleet, not a local disk.”
  - Step 3: “Availability is a separate promise: designed for 99.99% a year — tens of minutes (E8). And if you need single-digit milliseconds, Express One Zone keeps everything in one AZ — still eleven nines by design, but the AZ itself becomes the single point of failure (E13).”
  - Caption: “Six of nine is an illustrative count; S3 fetches only what reconstruction requires (E6, E19).”
- **Stage inventory:** Decorative `aria-hidden` SVG: auth door; index card flashing its pointer field; three AZ rows of tiles; six flight arcs (staggered “arrival” ticks, first six highlighted); reassembling object; `~ms` latency chip; sidebar card comparing Standard vs Express (two rows, plain text).
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Request at auth; card in view | Scene enters | `GET videos/aurora.mp4` | Same front door as writes. |
  | 2 | Card pointer field highlights; AZ rows energize | Step 1 active | `shards → AZ 1·2·3` | Metadata resolves location first. |
  | 3 | Six tiles fly; first six arrivals highlighted; object reassembles; `~ms` chip | Steps 2–3 active | `6 of 9 fetched — fastest win` | Enough, not all; reconstruction is on the read path. |

- **Motion choreography:** ENTER request slides in → HOLD card highlight → TRANSFORM six staggered flights (~120ms apart), arrivals tick in arrival order, object fades together → RESOLVE `~ms` chip and Express sidebar appear → EXIT hands the timeline to S07. Arrival order, not speed lines, carries the idea.
- **Data / computation:** E6, E8, E13, E18, E19. No numeric latency beyond “milliseconds to tens of milliseconds”; availability budget “tens of minutes” matches E8 phrasing.
- **Interaction:** None.
- **Accessibility and fallback:** Steps carry the sequence and both latency/availability facts in prose; no-JS static figure shows card → shards → reassembled object with the sidebar table; reduced motion shows state 3.
- **Responsive rules:** At 390px flight arcs become a simple ordered list (`shard D2 — AZ 1 ✓` …) beside the reassembled object; Express sidebar stacks as a two-row HTML table.
- **Acceptance check:** Reader can answer “does a GET wait for all nine shards?” (no — only enough to reconstruct) and name one trade Express One Zone makes.

### Scene S07 — Why the read after the write is always fresh

- **Narrative job:** Explain the December 2020 consistency guarantee and the reported mechanism that makes caches safe: per-object ordering plus a witness read barrier — attributed, not asserted as internal truth.
- **Placement:** Act 6; follows the read path; hands off to synthesis.
- **Pattern:** Sticky timeline scene (3 steps).
- **Primary visual anchor:** A per-object timeline where `PUT v2` takes sequence number 102, a witness pointer advances, and a cache lane is checked before serving.
- **Analogy or explanatory device:** None; literal mechanism sketch, explicitly labeled “simplified after AWS’s published description (E10)”.
- **On-page prose:**
  - Heading: `Write v2, read v2 — always`
  - Step 1: “Before December 2020, overwrites and deletes on S3 could be briefly stale — caches served the old value while updates propagated (E9).”
  - Step 2: “Today every write to an object takes an ordered sequence — v2 of `report.pdf` lands as 102 after v1’s 101 — and, as AWS engineers have described, a witness component tracks the latest committed version per object (E9, E10, E20).”
  - Step 3: “A read may use a fast cache only if it can prove it is not behind the witness; otherwise it falls through to the authoritative metadata store. You never see v1 after v2 was acknowledged — the cache is either fresh or bypassed.”
  - Caption: “Sequence numbers 101/102 are illustrative; the guarantee is not.”
- **Stage inventory:** Decorative `aria-hidden` SVG: horizontal write lane (`v1 · 101` → `v2 · 102` commit tick); witness token with a pointer; read lane splitting into `cache` and `authoritative` paths; a blocked-stale glyph; `Dec 2020` era marker.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | v1 at 101; witness pointer at 101; era label `before Dec 2020` | Scene enters | `v1 · 101` | The old world: caches could lag. |
  | 2 | v2 commits at 102; witness pointer advances; cache lane still holds v1 | Step 2 active | `102 > cache 101` | Ordering is per-object; witness is current. |
  | 3 | Read arrives; cache path checked and blocked; authoritative path serves v2 | Step 3 active | `GET → v2` | Fresh-or-bypass: the read barrier in action. |

- **Motion choreography:** ENTER timeline draws → HOLD at v1 → TRANSFORM v2 slides to 102 with a firm commit tick; witness pointer advances one notch → RESOLVE read pulse tries cache (brief red-edge flashless “check” bracket), reroutes, returns v2 → EXIT timeline folds into the final schematic. The block must read as a reroute, never as an alarm.
- **Data / computation:** E9, E10, E20 (101/102 illustrative). No claims about latency cost.
- **Interaction:** None.
- **Accessibility and fallback:** The three steps state problem, ordering, and read barrier fully in prose; no-JS static two-lane figure with the v2/102 commit and the served v2 marked; reduced motion shows state 3.
- **Responsive rules:** At 390px the timeline scrolls horizontally within its container or stacks: write events as an ordered list, then the read decision as an if/else text card.
- **Acceptance check:** Reader can explain, in one sentence, why a stale cache can’t answer after v2 commits — the witness forces fresh-or-bypass.

### Scene S08 — The whole machine, and its honest limits

- **Narrative job:** Bind every mechanism into one schematic the reader can keep, add the attributed deep-dive notes, and deliver the honesty beat (durability ≠ protection from your own DELETE) plus the reusable four questions.
- **Placement:** Act 7; closes the article; includes the conclusion and post navigation handoff.
- **Pattern:** Synthesis scene + final diagnostic card.
- **Primary visual anchor:** The complete machine card — front door, two planes, three AZs with shard grid, repair sweep, witness layer — labeled in the order the article introduced them.
- **Analogy or explanatory device:** The four questions are the transferable device: Where does the metadata live? How is the data spread? When does it say “done”? What repairs it? Mapping: S3’s answers are the article; limit, stated: the questions transfer, the answers do not.
- **On-page prose:**
  - Heading: `Eleven nines is a loop you can audit`
  - Step 1: “One picture: a stateless front door; a strongly consistent metadata plane; an erasure-coded fleet across at least three AZs; a repair loop holding redundancy in place. AWS has published research on the parts — a formally verified Rust storage node (ShardStore) and metadata built from millions of tiny consensus cells (Physalia) (E14, E15).”
  - Step 2: “What this does not promise: an authorized `DELETE` is a valid command. Durability protects against infrastructure failure, not against you — that’s versioning’s job (E16). Cross-region replication exists for the regional-disaster case (E17).”
  - Step 3: “Keep four questions for any storage system: where is the metadata, how is the data spread, when does it say done, and what repairs it. S3’s answers are one, very polished, instance of the pattern.”
  - Caption: “Old advice worth a footnote: per-prefix throughput ceilings (3,500 writes/s, 5,500 reads/s) shaped key-naming habits; AWS has since automated partition splitting (E12).”
- **Stage inventory:** Informative final SVG schematic with `<title>`/`<desc>`; five labeled layers; four-question HTML card; versioning callout box. The schematic may light up per layer as steps activate; all labels also in text.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Machine card outline only | Scene enters | five dimmed layer labels | The inventory to be assembled. |
  | 2 | Layers light in article order: door → card → shards/AZs → repair → witness | Step 1 active | each label + one-line gloss | Every earlier act lands in one place. |
  | 3 | A `DELETE` glyph enters and is executed as a valid command; versioning callout appears | Step 2 active | `DELETE → gone (by design)` + versioning note | The honest limit of the promise. |
  | 4 | Labels dissolve into the four questions card | Step 3 active | four questions listed | The model becomes portable. |

- **Motion choreography:** ENTER outline → HOLD → TRANSFORM ordered layer illumination (steady, one per beat) → RESOLVE DELETE beat is quiet and textual, not destructive-looking → EXIT settle on the four-question card with the schematic still visible above. The finale’s character is composure: the machine holds.
- **Data / computation:** E12, E14, E15, E16, E17; no new numbers.
- **Interaction:** None (the DELETE beat is narrated, not a control — it must not feel like a game).
- **Accessibility and fallback:** The schematic is informative SVG with full `<title>`/`<desc>` and an HTML caption; all five layer glosses, the versioning caveat, and the four questions exist as real DOM text. No-JS and reduced motion: fully resolved static card + list.
- **Responsive rules:** At 390px the schematic stacks its five layers vertically as labeled rows; the four-question card is a simple list; DELETE beat remains a text callout.
- **Acceptance check:** Reader can recite the four questions and state, without the page, what eleven nines does and does not protect against.

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** Archival engineering manual — ink-on-paper article surfaces, schematic “machine room” stages drawn like numbered technical sheets (title blocks, measurement rules, leader lines), monospace readouts.
- **Why this style fits this subject:** S3 is an engineered machine that earns a promise through structure; a technical-manual register presents mechanisms as auditable drawings rather than marketing, and the paper/ink contrast separates reading (document) from mechanism (schematic sheet). The calm register matches the system’s own answer to failure: reroute and repair, never alarm.
- **Emotional register:** Calm, precise, quietly impressed. One moment of earned relief (AZ loss stays readable), one moment of sober honesty (DELETE).
- **Avoid:** AWS-brand orange as a brand gesture (accent is reserved for semantics), cloud/datacenter stock tropes (glowing blue server racks), fire/alarm theatrics for failures, dashboards of fake telemetry, and any red that manufactures urgency the system doesn’t have.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | Article on warm paper `#F4F1E9`; schematic stages on deep ink-navy sheets `#131C2B` with 1px rule frames and corner title blocks (“SHEET 03 · WRITE PATH”). Text contrast ≥ 4.5:1 on both. |
| Palette semantics | Ink `#1E2A3A` structure/text; paper white for lifted cards. Semantic accents only: amber `#C77800` = failure/loss (sparingly, never decoratively); teal `#0E7C6B` = confirmed durability/ack; slate blue tints + hatch patterns + explicit labels identify AZs (never color alone). |
| Typography | System stacks only, zero font downloads: display via `ui-sans-serif`-led grotesque stack with tight tracking for headings; body serif/sans hybrid stack at comfortable measure; `ui-monospace` for keys, readouts, status lines, and sheet numbers. |
| Grid and spatial language | Article column ~68ch centered; stages full-bleed within a framed sheet with a right-edge measurement rule; step paragraphs on paper beside/below the sheet; sticky scene pinned while its steps scroll. |
| Shapes / illustration | 1.5px technical line work, orthogonal paths, small square nodes; shard tiles are rounded-2px squares with pattern fills (hatch = data, dots = parity, cross-hatch = failed); leader lines with 3px terminals for annotations. |
| Annotation language | Monospace labels, lowercase-technical voice (`az 1 · 3 shards`), units always shown, illustrative values tagged `illus.`; sheet corner carries source/illustrative status of every readout. |
| Motion character | Mechanical and deterministic: 300–700ms, ease-out, staggered 80–120ms for sequences; straight flight paths; no bounce, no parallax, no ambient loops; nothing pulses except an active control invite; offscreen scenes pause. |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| Schematic sheet frame + title block | Stage chrome for all scenes | Original | CSS/SVG | N/A (decorative) |
| Shard tile set (D/P/failed patterns) | Grid scenes S03–S06 | Original | Inline SVG patterns | HTML legend (data/parity/failed) |
| AZ glyphs (building outline ×3) | Repeated geography anchor | Original | Inline SVG | Text labels `AZ 1/2/3` |
| Machine card (final schematic) | Synthesis figure | Original | Inline SVG with `<title>`/`<desc>` | HTML caption listing all five layers |

No external images, fonts, or libraries.

## 6. Build handoff

### Document outline

```text
<title>How Amazon S3 Works: Eleven Nines, Explained — Víctor Busqué</title>
main
  hero — h1 "How One S3 Upload Earns Eleven Nines" + dek (hook promise)
  section — Act 1 · object store model + two planes (S02 above/below)
  sticky scene — Act 2 · write path (S03; steps 1–4)
  sticky scene — Act 3 · shard rule + overhead (S04; steps 1–3)
  sticky scene — Act 4 · break-the-machine simulation (S05; steps 1–3 + controls)
  sticky scene — Act 5 · read path + Express sidebar (S06; steps 1–3)
  sticky scene — Act 6 · consistency timeline (S07; steps 1–3)
  section — Act 7 · synthesis schematic + DELETE honesty + four questions (S08)
  conclusion — plain-prose ending from §1
  post navigation — prev: write-ahead-log
```

### Implementation plan

- **Target:** `blog/not-ready/how-s3-works.html` while parked; ships to `blog/how-s3-works.html`.
- **Enhancement ladder:** semantic HTML (all steps/conclusions in DOM order) → CSS static resolved states → IntersectionObserver step activation (`data-active-step`) → small rAF helpers only for shard-flight timing and the repair sweep. No scroll-linked continuous animation beyond step interpolation; no Canvas.
- **State source of truth:** one observer sets `data-active-step` on each `.scene`; each scene exposes one pure function `applyStep(n)`; S05’s simulation keeps its own explicit state object (`alive: Set, azDown: bool`) rendered by the same pipeline — no competing scroll handlers.
- **Dependencies:** none beyond the required shared reading indicator (`../css/post-progress.css`, `../js/post-progress.js`; `../../` while parked).
- **Performance budget / risks:** eight SVG scenes is the main weight — keep each under ~15KB of markup, reuse `<defs>`/`<use>` for shard tiles and AZ glyphs; no fonts or images fetched; all animated loops pause offscreen via the observer; respect `prefers-reduced-motion` with pre-resolved states.
- **No-JS / reduced-motion plan:** every scene ships a static resolved figure or HTML table with the same conclusion; step prose is normal flow text; reduced motion swaps transitions for instant state application (S05 buttons remain functional).
- **Mobile plan:** 390px rules per scene (stacking, monograms, text readouts, ≥44px touch targets); sticky tracks shortened to ~120vh; the S05 control row wraps 2×2; nothing depends on hover.
- **Open implementation questions:** none — all states, values, and fallbacks are specified above.

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `how-s3-works` | matches `docs/ideas.md` queue item “How does AWS S3 work?” |
| Search title | How Amazon S3 Works: Eleven Nines, Explained | 44 chars; keyword-first |
| H1 / shelf title | How One S3 Upload Earns Eleven Nines | follows “How WAL Saves a $100 Transfer.” follow-one-thing pattern |
| Meta description / deck | Follow one S3 upload: erasure-coded shards across three Availability Zones, a continuous repair loop, and the read barrier behind strong consistency. | 148 chars; must agree with manifest at ship time |
| Topic | Cloud storage · Systems | manifest label, free-form |
| Tags | S3, AWS, Erasure coding, Durability | manifest labels |
| Canonical | `https://engineering.victorbusque.com/blog/how-s3-works.html` | current site domain per sitemap.xml |
| Date | `2026-09` | proposed publishing month; set at ship time, next post no (`09`) after WAL |
| Internal links | prev: `blog/write-ahead-log.html` (durability boundary ↔ durability loop) | add successor link on WAL post nav at ship time |

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
