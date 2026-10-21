# Taxonomy stress test — Milestone 2

The brief asks for the definitions to be stress-tested before labelling: get an
AI tool to write posts that sit on the boundaries, and tighten the definitions
if they can't be classified cleanly.

**How it was run.** Claude wrote boundary posts in HN style, each aimed at one
boundary, with an intended label held back. A separate labelling agent, acting
for me, classified them using only the written definitions and rules. For each
post it reported CLEAN or UNCLEAR, where UNCLEAR means the written rules let it
defend two labels. Every UNCLEAR led to a rule change and a re-test. The
AI-written posts are only here; none of them are in `labels.csv`.

## Round 1 — draft v1

| Post | Aimed at | Labelled | Status |
|---|---|---|---|
| S1. Moved CI to office boxes, builds 14 → 4 min | evidence / experience | experience | CLEAN |
| S2. Hit it last week; Postgres mailing-list thread from March, fixed in 16.3 | evidence / experience | evidence | CLEAN |
| S3. "In my experience nobody reads the docs. Ever." | experience / assertion | assertion | CLEAN |
| S4. Every startup I've worked at (four now) rewrote the backend | experience / assertion | experience | **UNCLEAR** |
| S5. Rust is memory safe, so rewrite it | evidence / assertion | assertion | CLEAN |
| S6. Apple's platform security guide says iCloud backups aren't E2E by default | evidence / assertion | evidence | CLEAN |
| S7. "Is anyone surprised the ad company decided ad blockers are a security risk?" | assertion / out of scope | assertion | CLEAN |
| S8. Link to the writer's own write-up of a QR-code game state | evidence / experience | evidence | **UNCLEAR** |

**Gaps found and fixed in v2:**
- *S4:* Rule 2 didn't say whether a summary of repeated first-hand events is
  "specific". Now it is, if it says where or how often. Credentials alone
  ("20 years doing this") are not.
- *S8:* Rule 1 didn't say what a link to the writer's own work is. Now a
  followable link counts as `evidence` even when it's the writer's own repo or
  write-up, because the reader can look at the thing itself.
- *S5/S7:* "specific enough to look up" was undefined.

## Round 2 — v2

| Post | Aimed at | Labelled | Status |
|---|---|---|---|
| S4 (re-check) | | experience | CLEAN |
| S8 (re-check) | | evidence | CLEAN |
| N1. A week on an M2 Air, fan never came on "because there isn't one" | evidence / experience | experience | **UNCLEAR** |
| N2. "20 years building distributed systems… microservices are a fad" | experience / assertion | assertion | CLEAN |
| N3. "The benchmark is in my repo" + link; SQLite beat Postgres | evidence / experience | evidence | CLEAN |
| N4. "Remember when everyone said this about Java applets?" | evidence / assertion | assertion | **UNCLEAR** |

**Gap found and fixed in v3:** "named specifically enough to look up" and "a
general fact everyone knows" overlapped. A well-known fact about a named thing
(the M2 Air is fanless, Java applets died) was both. v3 replaces this with a
concrete test: **evidence needs a pointer**, meaning a link, a named document or
source, a quote, an identifier (version, CVE, model or bill number), a date, or
a number about the world. A fact about a named thing with no pointer is not
evidence, however well known. A comparison to a past event counts only if the
event is pinned down by a pointer.

## Round 3 — v3 (final)

| Post | Aimed at | Labelled | Status |
|---|---|---|---|
| N1 (re-check) | | experience | CLEAN |
| N4 (re-check) | | assertion | CLEAN |
| P1. Postgres has had logical replication "since version 10", so you don't need Kafka for CDC | evidence / assertion | evidence | CLEAN |
| P2. "Everyone knows Google kills products." | evidence / assertion | assertion | CLEAN |

**Result.** All 14 posts were labelled the way they were written to be
labelled, and after three rounds none were UNCLEAR. P1 and P2 are the real test
of v3, because they were written after the rule and aren't named in it.

## The real borderline post, argued both ways

HN item 49014319 (the first `experience` example in the README):

> I worked on a system a couple years ago with a BERT-based model (64M parameters) used for classification. … tokenization was still >10% of total runtime.

- **The case for `evidence`:** it is the most quantified post in the first 40.
  It has a parameter count, a throughput comparison (GB/s against MB/s) and a
  runtime share. These are the specifics a reader looks for when deciding
  whether a claim has support, and anyone could profile a BERT tokenizer to see
  whether it's that slow.
- **The case for `experience`:** every number describes a system only the
  writer has seen. Nothing links to it, names it or dates it. The parameter
  count describes their model, not a public one. If the writer misremembered,
  no reader could find out.

Both cases are strong, which is why the boundary needed a written rule rather
than a judgment each time. Rule 1, "who does the reader have to trust?",
decides it: the reader has to trust the writer, so it's `experience`.
