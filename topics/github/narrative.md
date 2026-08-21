---
topic: "github"
status: ready-for-build
language: en
source_context: topics/github/context.md
created: 2026-08-21
updated: 2026-08-21
intended_slug: git-github-at-scale
---

# What actually travels in a `git push`?

> **Revision note:** This replaces the earlier object-label-led story. The
> article now teaches one concrete example from first principles. It never asks
> a reader to infer what `tree`, `blob`, `commit`, or a symbolic ID means from
> an unexplained diagram. Every technical name follows an ordinary-language
> explanation, and every visual shows human-readable contents before Git’s
> terminology.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | An entry-level engineer who has used `git status`, `git add`, `git commit`, and `git push`, but pictures a push as uploading the current folder. They know what a folder, filename, branch, and pull request are. |
| Central question | If `git push` does not upload my working folder, what does it send instead? |
| One-sentence answer | Git sends the new pieces needed to describe a saved project version—file contents, folder listings, and a commit record—then asks the remote to move a branch label to that commit. |
| Core takeaway | A Git commit is a saved map of a project, not a copied working folder: file-content records hold bytes, folder-listing records give those bytes names and places, and a commit records one complete version. |
| Why it matters | Seeing the actual pieces makes commits, branches, pushes, pull requests, and GitHub’s role intuitive rather than magical. |
| Scope and exclusions | One deliberately tiny, fast-forward example only. The article does not teach all commands, hashes, pack compression, protocol negotiation, merges, rebases, detached HEAD, GitHub’s current infrastructure, replica counts, databases, or performance tuning. |
| Narrative point of view | Change one file in a three-file repository, make one commit, and pack exactly the newly needed pieces for a remote that already has the previous version. |
| Reading language | English. |

### Reader journey

```text
Before: A push sends the folder on my laptop to GitHub. A tree is an opaque
        Git word; a branch is a separate copy of the project.
Bridge: Open one before-and-after project map. Separate the file’s words from
        the folder listing that gives them a filename. Put that listing in a
        commit, then place only the new pieces in a parcel for the remote.
After:  Git sends records that describe a version, not a working folder. A
        branch is a label to one commit, and GitHub adds team features around
        the Git history.
```

### Plain-language opening and ending

- **Opening promise (1–2 sentences):** When you run `git push`, Git does not
  zip up the folder on your laptop and send it away. This page opens one tiny
  push and lays the actual pieces on a table.
- **Ending (1–3 sentences):** In this example, the remote already has the old
  version, so Git sends only three new records: the new words in `hello.txt`,
  the new folder listing that names those words, and the commit that saves that
  listing. Then it asks to move `main` to that commit. GitHub can host this
  history and add pull requests, reviews, and access rules around it.

## 2. Evidence and editorial boundaries

| ID | Claim or datum that may appear | Type | `context.md` source or anchor | Date / scope / caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | Git stores file content in blobs, directory listings in trees, and snapshots/history links in commits. | verified | Sources [2], [12]–[15]: Git Book, “Git Objects” | The story uses only blob/tree/commit. Annotated tags exist but are irrelevant here. | S01–S03 |
| E2 | A blob contains file bytes but no filename; a tree contains entries that associate names and modes with blobs or other trees; a commit points to a root tree and parent commit(s). | verified | Sources [2], [5], [14], [17]–[19]: Git Book / refs material | “Folder listing” is the primary phrase. “Tree” follows it as Git’s technical name. | S01, S02 |
| E3 | The index is the staged candidate for the next commit; `git add` updates it and commit creation writes a tree and a commit from it. | verified | Sources [2], [13], [16], [20] | Explain as “the selected list for the next save.” Do not explain index file format. | Intro |
| E4 | Branches are refs: readable names that point to commits. | verified | Sources [5], [17]–[19] | Use a bookmark/label analogy. Do not make byte-cost or force-push claims. | S03 |
| E5 | Git stores and transfers groups of objects in packfiles; packfiles may use delta compression. | verified | Sources [1], [2], [4], [21] | Explain “compact parcel” and name packfile once. Do not teach compression or protocol negotiation. | S04 |
| E6 | A bare repository is repository data without a checked-out working directory. | verified | Sources [7], [8], [23] | Only needed to describe what a host can store; no filesystem or host architecture claim. | S05 |
| E7 | Git LFS keeps a pointer in Git and stores selected large payloads through LFS. | verified | “Metadata, Git LFS…” and sources [8], [10] | Optional side note; no backing-storage/provider claim. | S05 |
| E8 | Pull requests, issues, reviews, and permissions are host collaboration metadata rather than Git’s primitive object types. | verified | “Metadata, Git LFS…”; “Pull Requests and Merging”; GitHub docs [23], [24] | A PR can refer to commits and related refs; the PR record itself is not a blob/tree/commit. | S05, ending |
| E9 | GitHub historically described DGit/Spokes as application-level replication of ordinary Git repositories. | verified, historical | Source [9], “Introducing DGit” | Cite only as historical source context. Do not claim current server count, topology, or write process. | Sources note |
| E10 | Teaching repository before the edit: `hello.txt` contains `hello`; `README.md` and `src/app.js` are unchanged. After the edit, `hello.txt` contains `hello, Git`. | illustrative | Page-local model | Every scene must label this as an illustrative example. | Hero, S01–S04 |
| E11 | In the teaching example, the remote already has the old commit, old root tree, unchanged README blob, and unchanged `src` subtree. The minimum new Git objects are one changed-file blob, one new root tree, and one new commit. | illustrative inference | Derived from E1–E5 and E10 | This exact count depends on the stated simple repository and remote state. It is not a universal push count. | S02, S04 |

### Facts to preserve exactly

- A **blob** is saved file content with **no filename inside it**.
- A **tree** is Git’s name for a saved folder listing. It pairs filenames (and
  file modes) with blobs or nested folder listings. In the example, the root
  tree lists `hello.txt`, `README.md`, and `src/`.
- A **commit** points to one root tree and to the previous commit. It represents
  one saved project version; the commit does not contain a physical folder.
- A branch such as `main` is a readable label pointing to a commit.
- The explicit three-piece parcel is only correct because the remote already
  has the old version and the example changes only root-level `hello.txt`.
- The page’s visual labels must be descriptive: “new contents of hello.txt,”
  “new root folder listing,” and “new commit.” Do not use symbolic shorthand,
  pseudo-hashes, or unlabeled abbreviations.

### Claims to avoid or qualify

- Never say Git “does not send the folder” without immediately saying what it
  does send: records for new file contents, changed folder listings, and a
  commit, carried in a packfile for transfer.
- Do not state that every push sends three records, that every push sends only
  changed files, or that every pack is delta-compressed. Use “in this example.”
- Do not introduce terms such as DAG, reachability, MIDX, reftable, loose
  objects, SHA, protocol v2, `receive-pack`, `upload-pack`, quorum, or replica.
- Do not claim content identity makes code trusted or safe. Access rules and
  signatures are distinct concerns, outside this article’s scope.
- Do not describe GitHub’s present physical infrastructure. The host scene is a
  responsibility map, not a server map.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| selected list / index | The changes you chose for the next saved version with `git add`. | Intro |
| blob | Git’s name for saved file contents, without the filename. | S01 |
| folder listing / tree | A saved map that says which names appear in a folder and which saved contents they mean. | S01 |
| commit | A saved project version: it points to the root folder listing and the version before it. | S02 |
| branch / ref | A readable label that points to one commit. | S03 |
| packfile | Git’s compact bundle for storing or transferring records. | S04 |
| bare repository | Repository data on a server, with no checked-out project folder. | S05 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Narrative beat and draft copy intent | Visual anchor | Scroll / state transformation | Evidence | Static and reduced-motion fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 · Hook | What actually goes over the wire? | vague folder upload → inspectable pieces on a table | Promise to open one tiny push. State that the article answers with a model, not live GitHub telemetry. | A project folder opens into three labeled cards. | Quiet unfold. | E10 | Hero and a visible “illustrative example” legend. |
| 1 · Select | What does `git add` do? | edit immediately becomes a commit → selected list sits between edit and saved version | Explain working folder, selected list/index, and commit in one short strip. | `hello.txt` moves from “edited” to “selected for next save.” | One line is marked selected. | E3, E10 | Static strip and prose. |
| 2 · Explain the tree | Why is a filename separate from its contents? | file means one indivisible thing → contents and folder map are separate records | Open a folder listing and show it naming `hello.txt` → new contents, while keeping unchanged entries attached to old records. | A literal three-row folder listing beside file-content cards. | Highlight filename → matching content; reveal the name “tree” after the reader has seen its job. | E1, E2, E10, E11 | Full annotated listing and prose. |
| 3 · Save a version | What is a commit? | commit is a copied folder → commit is a note pointing to the folder listing and earlier version | Add a commit card above the root listing. Then move the `main` bookmark. | Commit card, root listing, earlier commit, `main` label. | Connect listing → commit → previous commit; then move `main`. | E2, E4, E10, E11 | Stable final chain and caption. |
| 4 · Send the pieces | What does a push send? | “not the folder” with no replacement → a packfile holding concrete new records plus a branch update request | Place exactly three fully labeled records in a parcel; remote already owns the old records; show request to move main after receipt. | Parcel with readable contents list. | Pack cards → cross boundary → remote places cards → label update request. | E5, E10, E11 | Static before/after shelves and all labels. |
| 5 · Place GitHub | What does a hosting service add? | GitHub is only a remote folder → it hosts Git history and adds team features around it | Use a simple responsibility map: Git history, team work, optional large files. | Three shelves, not a network map. | Reveal shelves one by one. | E6–E9 | Prose, `dl`, and simple table. |
| 6 · Takeaway | What should I remember? | opaque upload → saved records + compact pack + host service | Repeat the three records in normal prose, with the bounded example caveat. | Three plain underlined phrases. | None. | E1–E8, E11 | Complete conclusion. |

## 4. Scene specifications

### Scene S01 — A filename is a map entry, not file contents

- **Narrative job:** Explain the tree before asking the reader to understand a
  commit or push. The reader should leave able to explain why Git needs both a
  content record and a folder listing.
- **Placement:** Acts 1–2; follows the `git add` strip; hands off a root folder
  listing to the commit scene.
- **Pattern:** `sticky-scene` with a literal folder-listing table and three
  plain content cards.
- **Primary visual anchor:** The row `hello.txt → “hello, Git”` lights up in a
  root folder listing, while the actual text sits in a separate card.
- **Analogy or explanatory device:** A folder’s table of contents. The table
  says that the name `hello.txt` leads to particular saved contents. Limit:
  the drawing omits modes and real internal IDs; it is a readable version of
  the relation, not a byte-for-byte tree file.
- **On-page prose:**
  - Heading: “Git keeps the words and the filename separately.”
  - Step 1: In the example, the contents of `hello.txt` changed. A blob is
    Git’s saved record for those contents alone; the blob does not say
    `hello.txt` anywhere inside it.
  - Step 2: Something must say where those contents belong. Git saves a folder
    listing with rows for `hello.txt`, `README.md`, and `src/`.
  - Step 3: The `hello.txt` row points to the new saved contents. The unchanged
    `README.md` row and `src/` row can keep pointing to the records the old
    version already used.
  - Step 4: Git calls this saved folder listing a **tree**. A tree can point to
    file contents (blobs) or to another tree for a subfolder.
  - Caption: “Read this as a folder map: names on the left, saved contents or
    subfolders on the right. The table is illustrative; the relationship is
    real.”
- **Stage inventory:** Decorative root-folder-listing table with three rows;
  content card `contents: hello, Git`; muted cards `README contents (unchanged)`
  and `src/ folder listing (unchanged)`; arrows; visible “illustrative example”
  label. `aria-hidden="true"` stage.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | New `hello.txt` content card is prominent; listing muted. | Step 1 active | “contents only” | A blob holds file contents, not its name. |
  | 2 | Root listing opens with three named rows. | Step 2 active | `hello.txt`, `README.md`, `src/` | A folder map supplies names and structure. |
  | 3 | `hello.txt` connects to new content; other rows connect to muted old records. | Step 3 active | “new” vs “unchanged” labels | A changed folder listing can reuse unchanged records. |
  | 4 | Heading “Git calls this a tree” becomes visible. | Step 4 active | “tree = saved folder listing” | Technical term follows the ordinary explanation. |

- **Motion choreography:** ENTER new contents → HOLD → TRANSFORM by opening
  the listing and drawing the `hello.txt` relation → RESOLVE by labeling the
  listing “tree” → EXIT. Each change answers one question; no ambient motion.
- **Data / computation:** E1–E3 and E10–E11. Three listing rows are fixed,
  illustrative teaching data. No hashes, object-size counters, or realistic
  IDs are shown.
- **Interaction:** None.
- **Accessibility and fallback:** Four DOM-order steps carry the explanation.
  Without JS, show the complete labeled table and all three relations. Reduced
  motion begins at state 4. The stage is decorative.
- **Responsive rules:** At 390px, listing rows stack with arrows directly below
  each row; text labels remain 12px or greater; no horizontal scroll.
- **Acceptance check:** A reader can answer: “What is a tree?” with “Git’s
  saved folder listing: it connects names such as `hello.txt` to saved contents
  or subfolders.”

### Scene S02 — A commit saves the folder map

- **Narrative job:** Explain a commit as a record that points to the root tree
  and previous commit, not as a copied folder or mysterious opaque node.
- **Placement:** Act 3; follows S01; hands off the exact three new records for
  S04.
- **Pattern:** `sticky-scene` with one plain-language commit note above the
  root folder listing.
- **Primary visual anchor:** A card reading “new saved version” with two clear
  lines: “project map: root folder listing” and “previous version: earlier
  commit.”
- **Analogy or explanatory device:** A dated bookmark card attached to a folder
  map. Mapping: the card identifies a project version by its root map and
  links it to the previous version. Limit: the simplified card omits author,
  message, and timestamps.
- **On-page prose:**
  - Heading: “A commit saves one complete project version.”
  - Step 1: The new root folder listing now describes the project: new
    `hello.txt`, unchanged `README.md`, and unchanged `src/`.
  - Step 2: A commit points to that root listing. That is how Git knows which
    folder map represents this version of the project.
  - Step 3: The commit also points to the earlier commit, connecting versions
    into history.
  - Step 4: `main` is a readable label (a ref) that moves from the earlier
    commit to this one. The label moves; the saved versions stay.
  - Caption: “The commit does not carry a folder inside it. It points to the
    folder map, which in turn points to the saved contents.”
- **Stage inventory:** Root listing from S01; `earlier saved version` card;
  `new saved version` card with explanatory lines; `main` bookmark label;
  arrows. Decorative stage is `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Root listing is fully visible. | Step 1 active | all three project rows | A root tree is a complete project map. |
  | 2 | New saved-version card points to listing. | Step 2 active | “project map → root listing” | A commit chooses the root map. |
  | 3 | New card points to earlier saved-version card. | Step 3 active | “previous version” | Commits connect versions. |
  | 4 | `main` bookmark moves to new card; both cards remain. | Step 4 active | “main now points here” | A branch is a label, not a folder copy. |

- **Motion choreography:** ENTER root listing → HOLD → TRANSFORM by revealing
  the new commit’s two links → RESOLVE by moving the one `main` bookmark →
  EXIT. The bookmark is the only moving element in step 4.
- **Data / computation:** E2, E4, E10–E11. No commit hash, message, date,
  performance number, or branch-policy claim appears.
- **Interaction:** None.
- **Accessibility and fallback:** Steps state the full relation. No JS/reduced
  motion shows both version cards, the root listing, both links, and the final
  `main` position.
- **Responsive rules:** At 390px, stack new version → root listing → earlier
  version; present a small before/after label for `main` rather than a long
  diagonal arrow.
- **Acceptance check:** A reader can say, “A commit points to a folder map and
  the commit before it; `main` is only a label pointing to a commit.”

### Scene S03 — The parcel contains named pieces

- **Narrative job:** Give an intuitive, concrete replacement for “Git does not
  send the folder.”
- **Placement:** Act 4; follows commit construction; hands off to the host
  responsibility map.
- **Pattern:** `sticky-scene` with local/remote shelves and a readable parcel
  manifest, not symbolic node IDs.
- **Primary visual anchor:** A parcel marked “Git packfile” listing: “new
  contents of hello.txt,” “new root folder listing,” and “new commit.”
- **Analogy or explanatory device:** A parcel sent to an archive that already
  owns the previous edition. Mapping: only missing records need travel; limit:
  a packfile is a compact Git format, not a literal cardboard box or wire-level
  packet trace.
- **On-page prose:**
  - Heading: “This is what the example push sends.”
  - Step 1: The remote already has the earlier saved version and the unchanged
    README and `src/` records. Those do not need to travel again in this
    example.
  - Step 2: Git gathers records for transfer in a compact bundle called a
    **packfile**. Think of it as a parcel with a contents list.
  - Step 3: The parcel contains three new pieces: the changed file contents,
    the new root folder listing that names them, and the new commit that saves
    the listing.
  - Step 4: After receiving those records, the remote can accept a request to
    move `main` to the new commit. Its rules decide whether to accept that
    request.
  - Caption: “The exact three-piece parcel is specific to this tiny example.
    Real pushes depend on what the remote already has and what changed.”
- **Stage inventory:** Local shelf cards for old version and three new records;
  remote shelf with old version/unchanged cards; parcel manifest in ordinary
  language; `main` request card; “illustrative example” label. Stage is
  decorative and `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Both shelves show earlier version; only local shelf has three new labeled cards. | Step 1 active | “already at remote” | Existing records need not be resent. |
  | 2 | Empty packfile parcel opens. | Step 2 active | “compact Git bundle” | Packfile is the transfer container. |
  | 3 | Three fully named cards enter parcel. | Step 3 active | readable parcel manifest | This example sends concrete new records. |
  | 4 | Parcel reaches remote; `main` request becomes accepted state. | Step 4 active | “request: main → new commit” | Data transfer and branch permission are separate. |

- **Motion choreography:** ENTER local/remote shelves → HOLD the shared old
  version → TRANSFORM by placing three named cards in the parcel → RESOLVE with
  a single crossing and visible branch request. No speed lines, packet dots,
  fake progress, or hidden count.
- **Data / computation:** E5 and E10–E11. The parcel manifest is built from a
  fixed array of the exact three human-readable strings; its displayed count,
  if shown, derives from that array and says “3 in this example.”
- **Interaction:** None.
- **Accessibility and fallback:** Four ordered paragraphs say exactly what is
  sent. No JS/reduced motion shows parcel contents and final remote shelf in
  one stable state.
- **Responsive rules:** At 390px, use a vertical local shelf → parcel manifest
  → remote shelf. Do not compress the parcel strings into abbreviations.
- **Acceptance check:** A reader can answer “What did Git send?” by naming the
  three records in this example, and can explain why it did not resend the
  unchanged records.

### Scene S04 — Git history and the work around it

- **Narrative job:** Put GitHub in the right place after the reader understands
  the Git data it hosts.
- **Placement:** Act 5; follows S03; supports the final takeaway.
- **Pattern:** Quiet three-shelf reveal with a semantic `dl` and comparison
  table below.
- **Primary visual anchor:** Shelves titled “Git history,” “team work,” and
  “optional large files.”
- **Analogy or explanatory device:** A library. Git history is the collection;
  team work is the front desk where access and discussion happen; optional LFS
  storage is a separate oversized-items room. Limit: this is not a physical
  picture of GitHub servers.
- **On-page prose:**
  - Heading: “GitHub adds a service around this history.”
  - Step 1: A host can keep Git’s saved contents, folder listings, commits, and
    branch labels in a bare repository—repository data without a checked-out
    project folder.
  - Step 2: The host also adds access rules and team tools: pull requests,
    issues, and reviews.
  - Step 3: A pull request points a team at commits to discuss. The discussion
    is not itself a blob, tree, or commit.
  - Step 4: Git LFS is optional: Git keeps a pointer for a selected large file,
    while LFS stores and retrieves the payload.
  - Caption: “A responsibility map, not a current GitHub server diagram.
    Historical public writing describes Git repositories replicated at the
    application layer; no current topology is claimed.”
- **Stage inventory:** Three titled shelves; readable cards; scope note.
  Decorative stage is `aria-hidden`.
- **State model:**

  | State / step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | Git-history shelf appears. | Step 1 active | contents, listings, commits, labels | Host can keep ordinary Git data. |
  | 2 | Team-work shelf appears. | Step 2 active | access, PR, review | Collaboration is around Git history. |
  | 3 | PR card connects toward commit card but stays on team shelf. | Step 3 active | “discusses commits” | PR record is not a commit. |
  | 4 | Optional-LFS shelf appears. | Step 4 active | pointer → large payload | Selected large data can be separate. |

- **Motion choreography:** ENTER Git history → HOLD → reveal team work → show
  PR relation → reveal optional LFS. Motion is limited to categorization; no
  network or data-center implication.
- **Data / computation:** E6–E9. No server count, region, provider, database,
  availability, throughput, or current infrastructure detail.
- **Interaction:** None.
- **Accessibility and fallback:** Ordered prose, a `dl`, and comparison table
  carry all conclusions. No JS/reduced motion shows all shelves stacked in
  reading order.
- **Responsive rules:** At 390px, shelves stack in the same order; scope note
  remains visible in flow and plain language.
- **Acceptance check:** A reader can explain that GitHub hosts Git history and
  adds team features without assuming the picture reveals its physical system.

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** Illustrated archival manual for a small office tool.
- **Why this style fits this subject:** The story needs the calm clarity of
  labeled paper records, not the intimidation of a terminal or an imaginary
  data center. Literal cards and folder listings turn abstract Git terms into
  inspectable objects.
- **Emotional register:** Patient, concrete, and reassuring.
- **Avoid:** Hacker aesthetics, terminal rain, real-looking hashes, generic
  “cloud” imagery, glowing maps, server racks, dashboards, fake telemetry,
  unlabeled nodes, and any card whose contents must be guessed.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | Warm paper field, near-black diagram stage, paper record cards, restrained rules. Maintain 4.5:1 text contrast. |
| Palette semantics | Charcoal = already at remote / unchanged; rust = new in the example; cobalt = a branch label; moss = optional service/LFS. Repeat all distinctions in words and layout. |
| Typography | Large practical sans headings, easy-reading system body face, system mono only for commands, filenames, and small Git terms. |
| Grid and spatial language | Wide editorial margins. Literal table rows for tree scenes; vertical card chain for commit; local → parcel → remote for transfer; shelves for responsibility map. |
| Shapes / illustration | Square-cornered record cards, broad arrows, visible headings, ample line spacing. Never an abbreviation-only node. |
| Annotation language | Sentence-case explanations. Technical terms appear in bold after a plain phrase: “saved folder listing (tree).” |
| Motion character | One clear reveal at a time, 180–400ms ease-out. No autonomous motion, parallax, or fake transmission effects. |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| Folder listing | Teach tree as a map of names to saved contents | Original teaching diagram | CSS/HTML or inline SVG | S01 steps and caption |
| Commit card | Teach commit links | Original teaching diagram | CSS/HTML or inline SVG | S02 steps and caption |
| Packfile parcel | Show exactly what travels in example | Original teaching diagram | CSS/HTML or inline SVG | S03 steps and caption |
| Responsibility shelves | Separate Git from host features | Original teaching diagram | CSS/HTML or inline SVG | S04 steps, `dl`, table |

## 6. Build handoff

### Document outline

```text
<title>How Git and GitHub Work at Scale — Víctor Busqué</title>
main
  hero — h1 “What actually travels in a git push?” + one-sentence promise
  intro — tiny illustrative project + edit / selected list / saved version
  sticky scene S01 — filename and contents; folder listing (tree) explained
  sticky scene S02 — commit points to root tree and previous commit; main moves
  sticky scene S03 — packfile parcel lists exactly three new records
  quiet correction — exact count belongs only to stated example
  sticky scene S04 — Git history, team work, optional LFS
  comparison / glossary — branch, Git history, pull request
  conclusion — three sent records + hosting service
  sources and scope
  post navigation
```

### Implementation plan

- **Target:** `blog/not-ready/git-github-at-scale.html` until publishing is
  approved. Move to `blog/git-github-at-scale.html` only with final metadata,
  manifest registration, sitemap, and post QA.
- **Enhancement ladder:** Semantic HTML prose, literal tables, definition list,
  and comparison table → page-local CSS/inline diagrams →
  `IntersectionObserver` for named discrete scene states. No Canvas, WebGL,
  custom scroll engine, animation library, remote asset, or live request.
- **State source of truth:** Each scene owns sequential `data-step="1"…` DOM
  steps. One page-local observer assigns `data-active-step`; CSS consumes it.
  S03 renders parcel names and its count from one fixed array.
- **Dependencies:** Parked depth uses only `../../css/post-progress.css` and
  `../../js/post-progress.js`. All other style/runtime assets are inline.
- **Performance budget / risks:** Four lightweight diagrams; no web fonts,
  images, rAF loop, or external request. Transitions use opacity/transform.
- **No-JS / reduced-motion plan:** The document remains complete as ordinary
  prose, tables, `dl`, and captions. No JS shows resolved diagrams. Reduced
  motion disables all transitions and starts every scene at a complete final
  state; sticky tracks may collapse to normal flow.
- **Mobile plan:** At 390px, every scene becomes a vertical sequence. S01 table
  rows place their destination card below each filename; S02 stacks cards;
  S03 places the full parcel manifest between shelves; S04 stacks shelves.
  All labels are at least 12px; nothing is abbreviated merely to fit.
- **Open implementation questions:** None. Validate the clear relation in S01
  with an entry-level reader before publication; if they cannot define tree
  after it, simplify further rather than adding terms.

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `git-github-at-scale` | Existing planned permanent slug. |
| Search title | How Git and GitHub Work at Scale | Descriptive primary query, within intended title budget before brand. |
| H1 / shelf title | What actually travels in a `git push`? | Concrete reader-facing question. |
| Meta description / deck | See what a Git push sends: new file contents, a folder listing, a commit, and a branch update request—then where GitHub fits in. | 142 characters; exact scope, no current-topology claim. |
| Topic | Systems · Developer tools | Free-form manifest label. |
| Tags | Git, GitHub, version control, commits, developer tools | Draft manifest labels. |
| Canonical | `https://engineering.victorbusque.com/blog/git-github-at-scale.html` | Confirm live domain convention before shipping. |
| Date | TBD at publication | Do not invent publication date. |
| Internal links | Index; add only a genuinely helpful related beginner explainer at ship time | Verify actual post navigation then. |

## 8. Definition of ready

- [x] The central question is concrete and its plain-prose answer names what
      the example sends.
- [x] “Tree” has an explicit beginner definition, literal visual model, state
      table, and acceptance test.
- [x] All technical names follow ordinary-language explanations; no symbolic
      IDs or unexplained nodes remain in the planned public page.
- [x] The exact three-record transfer is visibly limited to its illustrative
      remote state and repository layout.
- [x] Each visual has a document fallback, reduced-motion state, and 390px
      rule; the aesthetic favors readable records over technical spectacle.
- [x] Public fields exclude invented dates and unverified current GitHub
      infrastructure claims.
