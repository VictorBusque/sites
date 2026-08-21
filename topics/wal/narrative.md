---
topic: wal
status: ready-for-build
language: en
source_context: topics/wal/context.md
created: 2026-08-21
updated: 2026-08-21
intended_slug: write-ahead-log
---

# The Durability Boundary

> **Purpose of this file:** the build brief for one standalone scrollytelling
> article. It teaches a junior engineer how to reason about write-ahead logging
> as a general durability pattern, using a database as the concrete system.

## 1. Story contract

| Field                        | Decision                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reader and assumed knowledge | Junior software engineers who know that databases have `INSERT`/`UPDATE`, transactions, RAM, disk, and an HTTP response, but do not yet have a model for `fsync`, commit, crash recovery, or checkpoints.                                                                                                                                                                                                                                                                                                                                                            |
| Central question             | What has a database actually promised when it says a write committed, even if its main data file has not yet changed?                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| One-sentence answer          | A WAL system may update live state immediately, but it acknowledges a commit only after it has durably recorded enough ordered history to recover that committed change if volatile state disappears; data files can catch up later.                                                                                                                                                                                                                                                                                                                                 |
| Core takeaway                | Treat durability as a boundary: identify live state, the durable record, the event that crosses the promise boundary, and the process that later materializes or compacts state.                                                                                                                                                                                                                                                                                                                                                                                     |
| Why it matters               | This model explains why `COMMIT` can be fast and crash-safe, what checkpoints do, and how to inspect related systems—such as logs, queues, replicas, or durable actors—without assuming their implementation is identical.                                                                                                                                                                                                                                                                                                                                           |
| Scope and exclusions         | Explain the common WAL rule, commit durability, redo, LSN/pageLSN intuition, checkpoints, sequential writes, and group commit. Do not teach a production recovery implementation, tuning guide, storage hardware configuration, MVCC, replication protocol, torn-page mechanics, or every difference between PostgreSQL, SQLite, and InnoDB. State that ARIES-style undo exists in some engines, but do not imply all systems use the same algorithm. Durable Objects are a comparison of the durability contract, not evidence that their internals are “just WAL.” |
| Narrative point of view      | Follow one illustrative counter update through a persistent three-lane system, deliberately crash it at named moments, then translate the model to other stateful systems.                                                                                                                                                                                                                                                                                                                                                                                           |
| Reading language             | English.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

### Reader journey

```text
Before: “Commit means the changed table page is already on disk.”
Bridge: One change exists visibly in three representations—live memory,
        durable ordered history, and a later materialized data page—and a
        response is physically held behind the durability boundary.
After:  “Commit means the system has made recovery possible. The durable log
        may be ahead of the data page; checkpointing closes that gap later.”
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** Your database returns `200 OK`, then the machine loses power. Did your write make it? Follow one update through memory, a write-ahead log, and a checkpoint to see exactly what “committed” promises.
- **Ending (1–3 sentences):** A commit is not a claim that every data page has been rewritten. It is the point at which the system has made the change durable enough to recover; WAL keeps that promise cheap by recording ordered history first, and checkpoints make the long-term state catch up. When you meet another stateful system, find its live state, durability boundary, recovery record, and catch-up process.

## 2. Evidence and editorial boundaries

The primary visual model uses an explicitly **illustrative** counter transaction. Its values, transaction ID, and LSN values teach ordering only; they are not measurements or a real database trace.

| ID  | Claim or datum that may appear                                                                                                                                                               | Type: verified / inference / illustrative | `context.md` source or anchor                                                                                                                               | Date / scope / caveat                                                                                             | Where used             |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------- |
| E1  | The WAL rule requires the relevant log record to be durable before the changed data page is written; a transaction’s commit record must be durable before acknowledgement.                   | verified                                  | Perplexity research → “Log Before Data”; “Normal Operation: Write Path”                                                                                     | General WAL rule; exact record formats and commit mechanics vary by engine.                                       | Acts 1–2; S02–S03      |
| E2  | WAL decouples commit durability from data-page flushing; sequential log appends are generally cheaper than forcing modified data pages at every commit.                                      | verified                                  | Perplexity research → “Normal Operation: Write Path”; “Performance Considerations and Trade-offs”                                                           | Performance is workload and storage dependent; use “typically,” not a universal speed claim.                      | Acts 2 and 5; S03, S06 |
| E3  | LSNs identify log positions; a pageLSN records the latest logged change reflected on a page, allowing recovery to avoid needless redo.                                                       | verified                                  | Gemini → “Log Sequence Number Architecture and Ordering Rules”; Perplexity → “WAL Data Structures”                                                          | Simplified page-oriented model; SQLite’s WAL mode uses frame numbers/indexing rather than this exact terminology. | Acts 3–4; S04–S05      |
| E4  | Checkpointing flushes or transfers outstanding changes and records a restart/recovery point, bounding WAL growth and recovery work.                                                          | verified                                  | Perplexity research → “Checkpointing”                                                                                                                       | Checkpoint implementation differs between engines.                                                                | Acts 5–6; S06          |
| E5  | ARIES-style recovery uses analysis, redo, and undo; redo repeats history and undo removes incomplete transactions.                                                                           | verified                                  | Gemini → “The ARIES Crash Recovery Protocol”                                                                                                                | Present as an ARIES-style model, not as the recovery procedure for every named database.                          | Act 4; S05             |
| E6  | SQLite WAL mode appends changed pages to a separate WAL file; a commit record is appended to the WAL, and checkpointing copies WAL changes to the database file.                             | verified                                  | Perplexity research → “SQLite WAL Mode”; SQLite WAL documentation in source list                                                                            | SQLite-specific explanatory comparison; it is not the general physical model for all WAL engines.                 | Act 6; S07             |
| E7  | PostgreSQL uses WAL before data pages, and its documentation describes redo after a crash and the benefit of sequential WAL writes; one sync can serve concurrent small transactions.        | verified                                  | Perplexity research → “PostgreSQL WAL”; source 25; PostgreSQL WAL introduction                                                                              | Do not claim a particular PostgreSQL internal undo protocol in public copy.                                       | Acts 2, 5; S06         |
| E8  | Relaxed durability settings can improve latency/throughput but can lose recently acknowledged transactions after a crash; the exact window and setting differ by engine.                     | verified                                  | Perplexity research → “Performance Considerations and Trade-offs”; ChatGPT → “Flush and Commit Protocols”                                                   | Explain as an explicit durability trade-off, not a corruption guarantee across all configurations.                | Act 5; S06             |
| E9  | SQLite WAL readers can use a stable end mark while a writer appends new commits; readers and a writer can proceed concurrently under its WAL-mode rules.                                     | verified                                  | SQLite WAL documentation in source list; Perplexity research → “SQLite WAL Mode”                                                                            | SQLite-specific; retains a single-writer constraint.                                                              | Act 6; S07             |
| E10 | Cloudflare Durable Object storage is transactional and strongly consistent per unique object; its runtime uses input/output gates around storage operations.                                 | verified                                  | Cloudflare Durable Objects SQLite-backed Storage API, supplementary research URL: https://developers.cloudflare.com/durable-objects/api/sqlite-storage-api/ | Comparison only. Do not claim its storage protocol, replication mechanism, or recovery implementation is WAL.     | Act 7; S08             |
| E11 | A SQLite-backed Durable Object runs application code and SQLite colocated; Cloudflare describes withholding outward communication until durable storage confirmation through an output gate. | verified                                  | Cloudflare “Zero-latency SQLite storage in every Durable Object,” supplementary research URL: https://blog.cloudflare.com/sqlite-in-durable-objects/        | Product/platform documentation; use only to explain the analogous acknowledgement boundary.                       | Act 7; S08             |
| E12 | `counter: 40 → 65`, `tx-42`, and LSNs 104–106 are an explanatory state model.                                                                                                                | illustrative                              | Narrative-owned deterministic model                                                                                                                         | Label “illustrative trace” in the first scene and never style it as telemetry.                                    | S01–S06                |

### Facts to preserve exactly

- **Write-ahead** means the relevant log record reaches stable storage before its modified data page can be written to disk (E1).
- A successful commit can precede the later write of changed data pages (E1, E2).
- Checkpointing is a catch-up/restart-bound process, not the event that makes every individual transaction committed (E4).
- “Redo” means applying durable history that is missing from materialized state. In ARIES-style recovery, redo can repeat history before undo removes loser transactions (E5).
- “Durable Object” is a comparative example; it must not be equated with a WAL implementation (E10, E11).

### Claims to avoid or qualify

- Never say WAL literally writes the logical change _before it changes RAM_. Common systems can modify an in-memory page while generating/buffering WAL; the durable ordering constraint concerns data-page flushes and acknowledgement (E1).
- Do not say “disk” unqualified when teaching durability. Use “durable/stable storage” in the rule, then explain `fsync` as the program asking the OS/storage stack to make the WAL durable; the reliability of the storage stack is a real operational dependency.
- Do not say all WAL records have both before- and after-images, or that all systems perform undo from WAL. Formats and recovery algorithms vary (E5, E6).
- Do not equate a checkpoint with truncating a log in every engine, nor promise a fixed checkpoint frequency (E4, E6).
- Do not attach benchmark numbers, claims such as “N× faster,” or a claimed durability window to the illustrative trace (E2, E8).
- Do not claim SQLite’s optional WAL mode, PostgreSQL WAL, InnoDB redo logs, event sourcing, and Durable Objects have identical concurrency, storage, or recovery semantics (E6–E11).

### Terminology

| Term                  | Reader-friendly definition                                                                                                                                                  | First use |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| live state            | The version a running process currently has in memory; it disappears in a crash.                                                                                            | Act 1     |
| WAL / durable history | An append-only, ordered record of changes whose durable portion can be used to recover state.                                                                               | Act 1     |
| durability boundary   | The point after which the system has enough durable information to keep its promise through a crash. This is the article’s explanatory label, not a universal product term. | Act 1     |
| `fsync` / flush       | The operation used to request that buffered WAL data be made durable before acknowledgement.                                                                                | Act 2     |
| commit                | The durable acknowledgement point for a transaction under the system’s configured durability rules; it does not necessarily mean the main data page is current.             | Act 2     |
| LSN                   | A monotonically increasing position in a WAL stream; use it as a bookmark for ordering.                                                                                     | Act 3     |
| pageLSN               | The LSN of the last logged change already reflected by a data page, in page-oriented systems that use this mechanism.                                                       | Act 4     |
| redo                  | Apply a durable change that the materialized data page is missing.                                                                                                          | Act 4     |
| undo                  | Remove work from transactions that did not complete, in systems/recovery algorithms that require it.                                                                        | Act 4     |
| checkpoint            | A controlled catch-up point that writes/transfers outstanding durable changes to the main data representation and limits later recovery work.                               | Act 5     |
| group commit          | Several transactions sharing one WAL flush, so one durability operation can acknowledge more than one commit.                                                               | Act 5     |

## 3. Narrative architecture

| Act                     | Reader question                                           | Before → after                                                                                 | Narrative beat and draft copy intent                                                                                                                                                                                                                       | Visual anchor                                                         | Scroll / state transformation                                                                                               | Evidence            | Static and reduced-motion fallback                                                                  |
| ----------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------- |
| 0 · Hook                | When the API says success, what survived?                 | “200 means disk changed” → “200 is a specific durability promise”                              | Open on `POST /increment` and a bright `200 OK`. Freeze it with the question: “What may disappear if the power goes now?”                                                                                                                                  | The response gate, visibly closed while a change is pending.          | Request appears; response pauses behind a vertical boundary.                                                                | E12                 | Still request/response diagram plus prose saying `200 OK` awaits durable confirmation.              |
| 1 · Mental model        | Where can one change exist?                               | One database blob → three separate representations                                             | Introduce a single illustrative change, `counter: 40 → 65`, in lanes for live memory, durable WAL, and materialized data page. Explain that the same fact can be ahead in one place and behind in another.                                                 | One labeled change capsule, `tx-42`.                                  | Rails reveal one at a time; old durable page remains `40`.                                                                  | E1, E12             | Three stacked labelled boxes and a plain state table.                                               |
| 2 · Mechanism           | When has the database earned the right to say commit?     | “Appending is enough” → “durable append, then acknowledgement”                                 | Generate update and commit records; show an amber pending frontier, a flush to stable storage, then turn the response gate green. State the log-before-page and acknowledgement rules plainly.                                                             | A moving flush frontier crossing `COMMIT`.                            | RAM changes; WAL entries append; flush frontier passes them; gate opens.                                                    | E1, E2, E12         | Resolved state with ordered numbered steps and text: log durable → acknowledge → page later.        |
| 3 · Critical detail     | Why does the data page stay old without losing the write? | Stale page means loss → stale page is recoverable                                              | Show the durable WAL at LSN 106 while the on-disk page stays at `40` / pageLSN 104. Make the gap visible as intentional deferred materialization.                                                                                                          | Bracket between WAL LSN 106 and pageLSN 104.                          | Camera/attention narrows to the two markers; irrelevant UI dims.                                                            | E2, E3, E12         | Side-by-side WAL/data-page comparison and explanatory caption.                                      |
| 4 · Stress / comparison | What happens if power fails at each moment?               | Crash is mysterious → crash outcome follows durable evidence                                   | Step through three named failures: before durable commit, after durable commit but before page write, and after the page catches up. Use only redo for the primary case; add a quiet sidebar that some systems must later undo incomplete work.            | A three-position crash cursor and surviving storage layer.            | RAM evaporates at each crash; restart reads known durable frontier; missing durable update replays only in the middle case. | E1, E3, E5, E12     | Three static crash cards with “survives / recovery action / final value.”                           |
| 5 · Change perspective  | Why not force every changed page at commit?               | WAL is extra work → WAL changes expensive random writes into a smaller sequential durable path | Accumulate four illustrative commits. Let a shared flush frontier cross them together; later show a checkpoint sweep moving data-page LSN forward. Mention relaxed settings as an explicit choice to move the promise boundary, not an optimization trick. | Parallel commit markers sharing one flush frontier; checkpoint sweep. | Several changes queue, become durable together, then materialize in a calm batch.                                           | E2, E4, E7, E8, E12 | Ordered diagram of group commit followed by checkpoint, with no performance numbers.                |
| 6 · Synthesis           | Is every WAL system physically the same?                  | A single universal implementation → a common rule expressed differently                        | Compare the generic model with a PostgreSQL-style page/LSN framing and SQLite WAL mode’s changed-page frames and checkpointing. State one useful concurrency fact about SQLite without turning this into a product matrix.                                 | The same three rails relabelled, not redrawn.                         | Labels morph; only architecture-specific labels change while the durability model stays.                                    | E3, E4, E6, E7, E9  | Comparison table and prose qualifications.                                                          |
| 7 · Takeaway            | How does this help me understand another stateful system? | “WAL is database trivia” → “durability boundary is a transferable question set”                | Preserve the generic model while relabelling it for a Durable Object contract. Finish with four questions a reader can use in unfamiliar systems.                                                                                                          | Four-question diagnostic card, backed by the stable three-rail model. | Database labels fade into generic labels; Durable Object comparison appears as a bounded callout.                           | E10, E11            | Four questions in normal DOM plus caveat that analogous contracts do not prove identical internals. |

## 4. Scene specifications

### Scene S01 — The promise is on hold

- **Narrative job:** Replace the assumption that a success response and a rewritten data page are the same event.
- **Placement:** Act 0; opens the article; hands off to the three-representation model.
- **Pattern:** Full-bleed hook with a compact diagram.
- **Primary visual anchor:** A single HTTP request card and a visibly closed response gate.
- **Analogy or explanatory device:** A physical gate is an explanatory device: it maps to withholding the outward acknowledgement until the durability condition is met. It does not map to a literal database component.
- **On-page prose:**
  - Heading: `When may a database say “done”?`
  - Step 1: “A request increments an illustrative counter from 40 to 65. The running process can see 65 almost immediately—but that alone would vanish with the process.”
  - Step 2: “The important question is not whether the value changed. It is whether the system has crossed the point at which it can honestly promise that the change can be recovered.”
  - Caption / annotation: “Illustrative trace. The response gate opens only after the scene’s durability boundary.”
- **Stage inventory:** Decorative `aria-hidden` SVG: request card, one amber `tx-42` capsule, response gate, text labels `request received`, `live state changed`, `response waiting`. Adjacent DOM prose states the conclusion.
- **State model:**

  | State / step | Stage state                  | Trigger       | Visible evidence              | Meaning                                                       |
  | ------------ | ---------------------------- | ------------- | ----------------------------- | ------------------------------------------------------------- |
  | 1            | Request arrives; gate closed | Scene enters  | `POST /increment`, amber gate | Work has begun, no promise yet.                               |
  | 2            | Memory badge becomes 65      | Step 1 active | `RAM: 65`                     | Live state alone is not durable.                              |
  | 3            | Boundary label appears       | Step 2 active | “durability boundary” rule    | The acknowledgement condition is named before details arrive. |

- **Motion choreography:** ENTER request card slides in → HOLD at closed gate → TRANSFORM live-state badge from 40 to 65 → RESOLVE with boundary label → EXIT by widening into three rails. Motion distinguishes observation from acknowledgement; the gate must not open in this scene.
- **Data / computation:** E12 only: `40 + 25 = 65`; show the calculation in DOM text.
- **Interaction:** None.
- **Accessibility and fallback:** Stage is decorative and `aria-hidden`; h1/dek and two paragraphs contain all conclusions. No-JS shows a static closed gate illustration. Reduced motion shows state 3, closed gate, and the 40→65 label without transitions.
- **Responsive rules:** At 390px, stack request, gate, and response vertically; retain the words “waiting for durable confirmation,” never rely on the gate color.
- **Acceptance check:** A reader can answer “Why is `200 OK` not shown yet?” without seeing animation: because only live memory has changed.

### Scene S02 — One change, three representations

- **Narrative job:** Establish the article’s durable visual grammar: live state, durable history, materialized state.
- **Placement:** Act 1; follows the withheld response; hands off to the write/flush sequence.
- **Pattern:** Sticky diagram scene.
- **Primary visual anchor:** The same `tx-42 · counter +25` capsule moving across three persistent horizontal rails.
- **Analogy or explanatory device:** Literal schematic, not a metaphor. “History” is a reader-friendly label paired everywhere with “WAL / append-only log.”
- **On-page prose:**
  - Heading: `One fact can be ahead in three places`
  - Step 1: “Live memory is fast, but a crash erases it. The materialized data page is durable, but it may still show the older value.”
  - Step 2: “Between them is the WAL: ordered durable history. It records enough information to recover committed work that has not reached the data page yet.”
  - Step 3: “These are not competing truths. They are different stages of the same change.”
  - Caption / annotation: “The blue, amber, and slate rails always name a state class as well as a location.”
- **Stage inventory:** Decorative SVG lanes: `LIVE STATE · RAM`, `DURABLE HISTORY · WAL`, `MATERIALIZED STATE · DATA PAGE`; memory cell 65, WAL blank/pending slot, data page value 40/pageLSN 104; persistent legend including words and icons; no generic card grid.
- **State model:**

  | State / step | Stage state                                | Trigger       | Visible evidence                         | Meaning                                                               |
  | ------------ | ------------------------------------------ | ------------- | ---------------------------------------- | --------------------------------------------------------------------- |
  | 1            | Only RAM shows 65                          | Step 1 active | Blue `65`; slate `40`                    | The write is observable but not promised.                             |
  | 2            | WAL rail receives pending record           | Step 2 active | Amber `LSN 105: +25`                     | Ordered history now exists, but has not crossed its durable frontier. |
  | 3            | All rails visible with different positions | Step 3 active | Explicit “same logical change” connector | A system can intentionally have a gap between log and data page.      |

- **Motion choreography:** ENTER rails draw in from left → HOLD showing only RAM change → TRANSFORM log slot appends to the right → RESOLVE with connector paths between representations → EXIT retains rails for the next scene. The direction is always left-to-right for history/order.
- **Data / computation:** E12. `pageLSN 104` is deliberately an earlier illustrative marker; text labels it as such.
- **Interaction:** None.
- **Accessibility and fallback:** Three DOM subsections repeat the lane labels and state values in a definition list. Reduced motion shows state 3. SVG stays decorative because prose supplies the model.
- **Responsive rules:** Convert lanes to a vertical sequence connected with arrows. Keep value and LSN labels at at least 12px; omit nonessential connector decoration, not labels.
- **Acceptance check:** At any scroll position the three labels, 65 in RAM, and 40 on the data page are visible or summarized in the current step text.

### Scene S03 — The durable commit line

- **Narrative job:** Teach the exact ordering that turns a pending update into an acknowledged commit.
- **Placement:** Act 2; follows the three lanes; hands off to an intentional log/page gap.
- **Pattern:** Sticky sequence diagram.
- **Primary visual anchor:** A vertical flush frontier travelling across a WAL strip containing `UPDATE` and `COMMIT` records.
- **Analogy or explanatory device:** “Frontier” is a visual label for the greatest durable log position (`flushedLSN` concept); it is not an additional physical file.
- **On-page prose:**
  - Heading: `Commit is a line the log must cross`
  - Step 1: “The transaction changes a cached page and appends an update record. Appending to a memory buffer is still not a durable promise.”
  - Step 2: “The database appends a commit record and flushes the WAL through it. Only after that durable flush may it acknowledge the transaction.”
  - Step 3: “The data page may remain at 40. WAL’s rule is log before page, not page before response.”
  - Caption / annotation: “In a real engine, precise record contents and buffering differ. The ordering rule is the lesson.”
- **Stage inventory:** Decorative SVG: WAL cells `104 prior state`, `105 UPDATE +25`, `106 COMMIT tx-42`; amber-to-green flush frontier; response gate; data page marked `pageLSN 104`; annotation `WAL durable through 106`.
- **State model:**

  | State / step | Stage state                       | Trigger       | Visible evidence                            | Meaning                                |
  | ------------ | --------------------------------- | ------------- | ------------------------------------------- | -------------------------------------- |
  | 1            | Update record buffered            | Step 1 active | Amber record 105; closed response           | Work can still be lost.                |
  | 2            | Commit record durable through 106 | Step 2 active | Green frontier; `fsync complete`; open gate | The system can acknowledge the commit. |
  | 3            | Data page still at 40             | Step 3 active | Slate page, `pageLSN 104`                   | Data-page flush is deferred safely.    |

- **Motion choreography:** ENTER focus narrows to WAL tail → HOLD at amber record → TRANSFORM frontier sweeps over records 105–106 and gate opens after it passes 106 → RESOLVE by highlighting the untouched data page → EXIT retains final state. The temporal delay between frontier and gate is perceptible but brief; never animate a response before the frontier.
- **Data / computation:** E1 and E12. Labels are fixed illustrative identifiers, not calculated performance timings.
- **Interaction:** None.
- **Accessibility and fallback:** Ordered DOM list: update generated, update/commit WAL records flushed, acknowledgement, later page write. Reduced motion displays final state with numbered order annotations.
- **Responsive rules:** On narrow screens, render the WAL cells as a vertical chronological list and place the response gate below `COMMIT`; show page state after it.
- **Acceptance check:** The resolved state visibly has both `WAL durable through 106` and `data page: 40`, while the response is open, with adjacent prose explaining why this is correct.

### Scene S04 — The gap is the feature

- **Narrative job:** Turn the apparent inconsistency between a durable log and stale page into the performance/correctness insight.
- **Placement:** Act 3; follows durable commit; hands off to crash cases.
- **Pattern:** Quiet split scene with a magnified LSN comparison.
- **Primary visual anchor:** Two aligned markers: WAL durable frontier 106 above pageLSN 104, with the gap bracketed and labelled “recoverable work.”
- **Analogy or explanatory device:** A bookmark, not a metaphorical storage object: LSNs are positions in ordered history. State that pageLSN is a common page-oriented technique, not an SQLite label.
- **On-page prose:**
  - Heading: `The log is ahead on purpose`
  - Step 1: “An LSN is a position in the log. Here the durable history reaches 106, but this data page says it reflects only 104.”
  - Step 2: “That difference is not missing data. It is work recovery can redo if the process dies before the page is written.”
  - Caption / annotation: “PageLSN is the page’s bookmark: it helps recovery tell whether a record already made it into that page.”
- **Stage inventory:** Decorative aligned ruler, three WAL ticks, one data-page header fragment, bracket, textual non-color cues (`ahead`, `already represented`), and small footnote `illustrative page-oriented model`.
- **State model:**

  | State / step | Stage state                            | Trigger       | Visible evidence                                         | Meaning                                                |
  | ------------ | -------------------------------------- | ------------- | -------------------------------------------------------- | ------------------------------------------------------ |
  | 1            | Markers aligned but unexplained        | Step 1 active | `durable WAL: 106`, `pageLSN: 104`                       | The gap is observable.                                 |
  | 2            | Gap bracket becomes “recoverable work” | Step 2 active | Bracket and redo arrow                                   | Recovery has a durable source for missing application. |
  | 3            | Rule card appears                      | Scene resolve | “Never flush this page before its WAL record is durable” | The WAL ordering constraint protects the gap.          |

- **Motion choreography:** ENTER ruler fades in → HOLD on mismatched markers → TRANSFORM bracket grows only across 105–106 → RESOLVE with a short redo arrow to page → EXIT leaves the markers visible. No simulated page mutation yet; reserve it for recovery.
- **Data / computation:** E3 and E12. No numerical scale or implication that adjacent LSNs equal one row/update size.
- **Interaction:** None.
- **Accessibility and fallback:** DOM text defines LSN/pageLSN; a compact table lists WAL=106, page=104, interpretation=records after 104 may need redo. Reduced motion is state 3.
- **Responsive rules:** Collapse to a labelled two-row table; use a short arrow between rows rather than a long ruler.
- **Acceptance check:** Reader can say why the data page being behind is safe: durable WAL has the missing work and pageLSN tells recovery where the page is.

### Scene S05 — Pull the plug at three moments

- **Narrative job:** Let the reader predict crash outcomes from the durable frontier rather than memorizing a recovery slogan.
- **Placement:** Act 4; follows the LSN gap; hands off to checkpointing.
- **Pattern:** Deterministic sticky crash inspector with scroll-driven states; optional accessible buttons duplicate the three states.
- **Primary visual anchor:** A crash cursor with three labelled stop positions over the exact transaction timeline introduced earlier.
- **Analogy or explanatory device:** “Power removed” literally represents loss of volatile state. It is not a claim about every real-world failure mode.
- **On-page prose:**
  - Heading: `After a crash, only the durable evidence gets a vote`
  - Step 1: “Crash before the commit record is durable: the live 65 disappears and no successful commit was promised. Restart keeps 40.”
  - Step 2: “Crash after the WAL commit is durable but before the page catches up: restart finds the committed history and redoes the missing change. The final value is 65.”
  - Step 3: “Crash after the page has caught up: the page already represents the change, so page/bookmark checks can avoid applying it again.”
  - Caption / annotation: “Some engines also need an undo phase for incomplete transactions. This primary trace isolates the simpler redo question: can a committed change be restored?”
- **Stage inventory:** Decorative SVG rails reused from S03; three focus positions; red bolt only on activation; volatile RAM layer visibly disappears; persistent WAL and data page remain; restart badge; outcome panel with `final value` and `recovery action`. Three semantic `<button>` controls: “Crash before durable commit,” “Crash after durable commit,” “Crash after page catch-up.”
- **State model:**

  | State / step | Stage state                 | Trigger       | Visible evidence                            | Meaning                                         |
  | ------------ | --------------------------- | ------------- | ------------------------------------------- | ----------------------------------------------- |
  | 1            | Pre-durable crash           | Step/button 1 | WAL frontier 104; page 40; final 40         | No durable commit exists to recover.            |
  | 2            | Post-durable/pre-page crash | Step/button 2 | WAL 106; page 40; redo arrow; final 65      | Redo restores committed work missing from page. |
  | 3            | Post-page crash             | Step/button 3 | WAL 106; pageLSN 106; `skip redo`; final 65 | Page already includes the change.               |

- **Motion choreography:** ENTER stable timeline → HOLD at chosen cursor → TRANSFORM red crash removes only RAM layer → RESOLVE restart scans durable frontier and either performs one redo arrow or displays skip → EXIT resolves on final state. Crash is a single non-flashing cut, never a repeated effect. Scroll activation and control activation must call the same named state function.
- **Data / computation:** E1, E3, E5, E12. Final values are computed deterministic states: pre-durable=`40`; other two=`40+25=65`.
- **Interaction:** Three native buttons in a labelled `fieldset`; clicking/focusing sets the corresponding stable state. Scroll steps update buttons’ `aria-pressed` state. Buttons work with keyboard, are not required to proceed, and a no-JS table exposes every outcome.
- **Accessibility and fallback:** Decorative stage `aria-hidden`; all state results live in the DOM steps and an outcome table. Reduced motion defaults to case 2—the central WAL payoff—with all three result cards visible beneath it. Include ARIES-style undo wording only in prose/caption, marked as a system-dependent extension.
- **Responsive rules:** Remove sticky height excess and show three vertically stacked outcome cards. Controls remain 44px minimum targets; never require horizontal scrubbing.
- **Acceptance check:** Selecting every crash point produces a coherent final value and action. In case 2, the page is visibly stale before restart but final value is visibly 65 after redo.

### Scene S06 — Commit now, catch up later

- **Narrative job:** Explain the operational payoff and make checkpointing concrete without presenting it as a clean-up animation with no correctness role.
- **Placement:** Act 5; follows crash inspection; hands off to engine comparison.
- **Pattern:** Sticky accumulation and checkpoint sweep.
- **Primary visual anchor:** Four compact transaction markers sharing one flush frontier, then a checkpoint sweep that advances pageLSN.
- **Analogy or explanatory device:** A “catch-up sweep” maps to checkpoint work, but is explicitly paired with the precise wording “writes/transfers outstanding changes and establishes a later recovery point.”
- **On-page prose:**
  - Heading: `The log makes the promise cheap; checkpoints keep it bounded`
  - Step 1: “For many small writes, a sequential WAL flush can make several commits durable together. This is group commit: shared durability work, not shared transactions.”
  - Step 2: “The main data pages still need to catch up. A checkpoint does that work over time and moves the recovery starting point forward.”
  - Step 3: “Some systems offer less strict commit flushing. That moves the durability boundary and can lose recent acknowledged work in a crash; it is a product decision, not free speed.”
  - Caption / annotation: “The scene has no throughput numbers. Its claim is about ordering and batching, not a universal benchmark.”
- **Stage inventory:** Decorative SVG: WAL records 107–110 with four separate tx IDs; one green `flush` frontier; data page pageLSN 106; checkpoint brush/sweep; recovery-start bookmark. An always-visible text distinction `commit makes durable` / `checkpoint materializes`.
- **State model:**

  | State / step | Stage state                                        | Trigger | Visible evidence                          | Meaning                                                        |
  | ------------ | -------------------------------------------------- | ------- | ----------------------------------------- | -------------------------------------------------------------- |
  | 1            | Four commits pending then one shared durable flush | Step 1  | Four tx IDs, one frontier                 | A flush may acknowledge multiple already-ordered transactions. |
  | 2            | Checkpoint advances page/bookmark                  | Step 2  | pageLSN 106→110; recovery marker moves    | Materialized state catches up and restart work is bounded.     |
  | 3            | Boundary trade-off note                            | Step 3  | Dashed alternative boundary; warning text | Relaxing flush changes what a success response promises.       |

- **Motion choreography:** ENTER WAL tail fills transaction by transaction → HOLD with amber records → TRANSFORM one frontier crosses all four in a single pass → RESOLVE checkpoint sweep moves pageLSN/bookmark later → EXIT morphs labels for comparison. The page update is a batch/sweep, never presented as instantaneous per-commit writing.
- **Data / computation:** E2, E4, E7, E8, E12. The four transactions are illustrative and do not demonstrate a measured batching ratio.
- **Interaction:** None.
- **Accessibility and fallback:** DOM text separately defines group commit and checkpoint. No-JS: an ordered two-panel diagram. Reduced motion displays durable WAL through 110 and pageLSN 110, with a textual note that these happened at different stages.
- **Responsive rules:** Use four small vertically listed records; replace wide sweep with an arrow labelled `checkpoint: pageLSN 106 → 110`.
- **Acceptance check:** The scene never implies checkpoint is required before a transaction is committed; both labels remain visible in every state.

### Scene S07 — Same rule, different machinery

- **Narrative job:** Prevent overgeneralization while leaving the reader able to recognize WAL ideas in PostgreSQL and SQLite documentation.
- **Placement:** Act 6; follows group commit/checkpoint; hands off to generic transfer model.
- **Pattern:** Comparison scene with a persistent generic rail model.
- **Primary visual anchor:** The generic rails remain fixed while only their labels and record shapes change.
- **Analogy or explanatory device:** “Same rule, different machinery” is the device. It maps a common contract, not feature parity.
- **On-page prose:**
  - Heading: `WAL is a family resemblance, not one file format`
  - Step 1: “The generic model is deliberately small: durable ordered history can be ahead of materialized state, and recovery/checkpointing close the gap.”
  - Step 2: “PostgreSQL commonly exposes LSNs and page-oriented WAL reasoning. SQLite WAL mode appends changed-page frames and commits in its WAL before checkpointing them into the main database file.”
  - Step 3: “SQLite’s WAL mode also lets readers hold a stable end mark while a writer appends later work—but it remains a single-writer design. Details such as records, readers, locks, and recovery are engine-specific.”
  - Caption / annotation: “Use the shared model to begin reading docs; use the engine docs for guarantees.”
- **Stage inventory:** Decorative SVG rails in generic labels, then label variants for `PostgreSQL-style WAL / LSN / data page` and `SQLite WAL frames / main DB / checkpoint`; a non-interactive comparison key. DOM table contains qualifications.
- **State model:**

  | State / step | Stage state                        | Trigger | Visible evidence                 | Meaning                                 |
  | ------------ | ---------------------------------- | ------- | -------------------------------- | --------------------------------------- |
  | 1            | Generic model                      | Step 1  | Generic labels                   | The transferable contract.              |
  | 2            | PostgreSQL-style labels            | Step 2  | LSN/page labels                  | One familiar page-oriented vocabulary.  |
  | 3            | SQLite labels and end-mark callout | Step 3  | Frames, main DB, reader end mark | A related but distinct WAL-mode design. |

- **Motion choreography:** ENTER generic state → HOLD → TRANSFORM labels and record shapes only, preserving rail positions → RESOLVE on side-by-side qualified table → EXIT fades names back to generic terms. The unchanging structure is the explanatory point.
- **Data / computation:** E3, E4, E6, E7, E9. No record byte sizes, segment sizes, or tuning defaults.
- **Interaction:** None.
- **Accessibility and fallback:** Comparison is fully expressed as a semantic table in DOM; SVG is decorative. Reduced motion shows generic diagram plus table.
- **Responsive rules:** Table becomes two labelled definition-list blocks, each immediately followed by its caveats; do not squeeze columns.
- **Acceptance check:** The public prose explicitly says different machinery and does not describe SQLite’s `-wal` file as PostgreSQL’s pageLSN mechanism.

### Scene S08 — The questions travel

- **Narrative job:** Turn WAL knowledge into a reusable debugging/documentation-reading habit, with a bounded Durable Objects example.
- **Placement:** Act 7; follows implementation comparison; closes the article.
- **Pattern:** Quiet synthesis scene with four diagnostic questions.
- **Primary visual anchor:** The three-rail model relabelled `live state`, `durable record`, and `materialized/recoverable state`, beside a four-item checklist.
- **Analogy or explanatory device:** The translation is a conceptual mapping, with a visible warning: “same question ≠ same implementation.”
- **On-page prose:**
  - Heading: `Find the durability boundary in any stateful system`
  - Step 1: “A database WAL is one answer to a general problem: live state is fast, but a system must decide when it may make an irreversible promise to the outside world.”
  - Step 2: “For a Cloudflare Durable Object, storage is transactional and strongly consistent for the object, and the runtime documents input/output gates around storage operations. That makes its outward acknowledgement boundary a useful comparison—not proof that its internals are the database diagram above.”
  - Step 3: “Ask: Where is live state? What durable evidence survives a crash? What event permits acknowledgement? How does durable history become current recoverable state?”
  - Caption / annotation: “Answer those four questions from the system’s own documentation before assuming it behaves like a database WAL.”
- **Stage inventory:** Decorative generic rails and four large numbered questions. A bounded callout labelled `Comparison, not implementation equivalence` names Durable Objects, transactional/strongly-consistent storage, and input/output gates. No Cloudflare logo or product imagery.
- **State model:**

  | State / step | Stage state                              | Trigger | Visible evidence            | Meaning                                                           |
  | ------------ | ---------------------------------------- | ------- | --------------------------- | ----------------------------------------------------------------- |
  | 1            | Database labels fade to generic terms    | Step 1  | Generic rail labels         | The mental model transfers at the contract level.                 |
  | 2            | Qualified Durable Object callout appears | Step 2  | Explicit comparison warning | Similar acknowledgement reasoning, unknown/independent internals. |
  | 3            | Four questions resolve                   | Step 3  | Numbered checklist          | The reader leaves with an actionable method.                      |

- **Motion choreography:** ENTER generic rails at rest → HOLD → TRANSFORM database-specific labels to generic labels → RESOLVE four questions with gentle sequential emphasis → EXIT none; this is the stable closing composition. No object-like motion is needed.
- **Data / computation:** E10, E11. No displayed latency, replication count, or claim about where a Durable Object persists data.
- **Interaction:** None.
- **Accessibility and fallback:** The four questions are a real ordered list in DOM. The comparison warning is ordinary prose, not a tooltip. Reduced motion shows the final checklist immediately.
- **Responsive rules:** Checklist is one-column; callout follows question 2 rather than floating beside it.
- **Acceptance check:** A reader can quote the four questions from the article without seeing a visual, and the Durable Objects paragraph says “comparison” and “not proof of identical internals.”

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** Operational schematic × scientific instrument: a precise systems observability display with editorial restraint.
- **Why this style fits this subject:** WAL is primarily about boundaries, order, evidence, and state transitions. Persistent rails, frontiers, and bookmarks make those relationships inspectable at rest, instead of hiding them behind a cute physical metaphor or an opaque dashboard.
- **Emotional register:** Curious and calm at first; briefly tense at the crash; then reassuringly deterministic. The reader should feel capable, not warned away by database mythology.
- **Avoid:** Literal filing cabinets, receipts, construction metaphors, faux-terminal walls, hacker-green-on-black, danger-red decoration, generic glass cards, floating database cylinders, animated particles, fabricated performance gauges, and “power outage” spectacle that obscures the state model.

### Design tokens and composition

| Concern                   | Direction                                                                                                                                                                                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Background and surfaces   | Near-black graphite field (`#101417` family) with faint low-contrast grid/noise; matte charcoal stages; warm off-white reading text. Maintain WCAG contrast for all prose and controls.                                                                                  |
| Palette semantics         | Blue = live/volatile state; amber = recorded but not yet shown durable; green = crossed durable boundary / acknowledgement permitted; slate = materialized page; restrained red = one-time crash event. Every state also has text/icon/pattern labels.                   |
| Typography                | Editorial system sans for h1/h2 and body; compact system mono for LSNs, IDs, SQL, and state readouts. Broad display heading, readable 42rem prose measure, no novelty typeface.                                                                                          |
| Grid and spatial language | A fixed three-rail horizontal coordinate system throughout desktop scenes. Time/order runs left→right; state class runs top→bottom. Vertical flush frontier and checkpoint sweep are the only major crossing gestures.                                                   |
| Shapes / illustration     | Fine 1px technical rules, square-to-slightly-rounded record capsules, solid frontier line, minimal iconography (memory chip, log strip, page), no pseudo-3D. Same `tx-42` token recurs so the reader recognizes identity across representations.                         |
| Annotation language       | Short, exact labels: `live`, `durable through LSN 106`, `pageLSN 104`, `redo`, `checkpoint`. Labels state condition and implication; values are marked `illustrative` at first use.                                                                                      |
| Motion character          | Mechanical, causal, and reversible under scroll: append, frontier advance, gate open, volatile layer disappears, redo reapplies, checkpoint catches up. Never continuously animate background, text, or completed state; no motion is required to discover a conclusion. |

### Asset plan

| Asset                                               | Purpose                        | Source / license                  | Inline representation                                  | Alt / text equivalent                        |
| --------------------------------------------------- | ------------------------------ | --------------------------------- | ------------------------------------------------------ | -------------------------------------------- |
| Three-rail state schematic                          | Primary explanation            | Original work                     | Inline SVG / CSS lines                                 | Adjacent step prose plus static state tables |
| Transaction / WAL record capsules                   | Preserve identity and ordering | Original work                     | Inline SVG / HTML spans                                | Record order repeated in DOM lists           |
| Flush frontier, gate, crash, redo, checkpoint marks | Explain transformations        | Original work                     | Inline SVG paths and CSS transforms                    | Each event is stated in the active step text |
| Fine grid/noise                                     | Quiet atmosphere only          | Procedural CSS, no external asset | CSS gradients or tiny inline SVG filter if inexpensive | Decorative, `aria-hidden`                    |

## 6. Build handoff

### Document outline

```text
<title>How Write-Ahead Logging Makes Commits Durable — Víctor Busqué</title>
main
  hero — h1 “The durability boundary”; dek and one request/response hook
  section — “When may a database say ‘done’?” (Act 0)
  sticky scene — “One fact can be ahead in three places” (Act 1)
  sticky scene — “Commit is a line the log must cross” (Act 2)
  split scene — “The log is ahead on purpose” (Act 3)
  sticky scene — “After a crash, only the durable evidence gets a vote” (Act 4)
  sticky scene — “The log makes the promise cheap; checkpoints keep it bounded” (Act 5)
  comparison section — “WAL is a family resemblance, not one file format” (Act 6)
  conclusion — “Find the durability boundary in any stateful system” (Act 7)
  post navigation
```

### Implementation plan

- **Target:** `blog/write-ahead-log.html` when publishing; use `blog/not-ready/write-ahead-log.html` first only if the narrative is built as a parked work in progress.
- **Enhancement ladder:** Semantic article, headings, ordered steps, definition lists, tables, and conclusions → inline CSS and static SVG/CSS diagram → `IntersectionObserver` updates discrete `data-active-step` states → optional `requestAnimationFrame` only for a short, scroll-derived frontier interpolation if CSS transitions cannot make the state change legible. No Canvas/WebGL.
- **State source of truth:** Each scene has a `data-active-step` value. S05 uses one `setCrashCase(caseId)` function called by both observer and buttons; all readouts derive from an immutable illustrative model object, e.g. `{base: 40, delta: 25, updateLSN: 105, commitLSN: 106}`. Do not independently mutate text, classes, and SVG values.
- **Dependencies:** None beyond required post chrome: `../css/post-progress.css` and `../js/post-progress.js`. All article CSS, SVG, and scene runtime are in the standalone file. No remote fonts, assets, libraries, or fetches.
- **Performance budget / risks:** Inline SVG only, limited to a few dozen nodes per scene; CSS transforms/opacity for movement; no raster payload. Pause/remove any rAF loop when scene is outside viewport; ideally avoid rAF entirely. Do not use filters on large areas or animate grid/noise.
- **No-JS / reduced-motion plan:** Every step’s conclusion is DOM prose in document order. Each sticky visual has a static final/explanatory SVG state and a semantic table/list; S05 exposes all crash cases in a table. With reduced motion, use stable states and no crash flash/frontier sweep; retain labels for the sequencing that motion otherwise conveys.
- **Mobile plan:** At <=390px, turn horizontal rails into vertical labelled lanes, reduce sticky tracks to roughly 1.5–2 viewport heights, use static/state cards where long travel would be unreadable, convert comparison tables to definition lists, and preserve all state labels. S05 controls stay native, full-width, and at least 44px tall.
- **Open implementation questions:** Confirm whether the initial draft is parked or shipped; obtain the site’s preferred date/image convention before publishing. The article should not expose a fabricated social-card scene image; derive/ship a legitimate static OG image or use the project’s established post convention.

## 7. Publishing handoff

| Field                   | Proposed value                                                                                             | Evidence / note                                                                                            |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Slug                    | `write-ahead-log`                                                                                          | Lowercase, three words, contains primary term; permanent only when shipped.                                |
| Search title            | `How Write-Ahead Logging Makes Commits Durable — Víctor Busqué`                                            | Primary query first; check final character/pixel budget against current shared convention before shipping. |
| H1 / shelf title        | `The durability boundary`                                                                                  | Reader-facing title; deck immediately names WAL.                                                           |
| Meta description / deck | `See how write-ahead logging makes a commit survive a crash—and why data pages can safely catch up later.` | Concrete promise; final character count and manifest wording must be checked at implementation.            |
| Topic                   | `Databases`                                                                                                | Free-form manifest label; verify current manifest taxonomy preference.                                     |
| Tags                    | `WAL`, `databases`, `durability`, `systems`                                                                | Draft manifest labels.                                                                                     |
| Canonical               | `https://engineering.victorbusque.com/blog/write-ahead-log.html`                                           | Verified current domain from `CNAME`; confirm at ship time.                                                |
| Date                    | `TBD`                                                                                                      | Do not invent a publication month; set from actual publishing date.                                        |
| Internal links          | `none yet`                                                                                                 | Add only a genuine related published article; post navigation must follow current site convention.         |

## 8. Definition of ready

- [x] The central question, takeaway, scope, and ending are explicit.
- [x] Every factual claim, number, and visual readout has an evidence ID or is labeled illustrative.
- [x] Each scene has a narrative job, state model, motion reason, fallback, and mobile rule.
- [x] A named aesthetic has been chosen and translated into usable visual decisions.
- [x] The document outline and implementation plan name the target file and enhancement strategy.
- [x] Publishing fields are drafted; unresolved publication date/image decisions are recorded rather than guessed.
