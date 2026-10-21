# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts **Hacker News comments** by what they rest their point on. A
comment is `evidence` if it points to something a reader can check without
trusting the writer (a link, a quote, a version or CVE number, a date, a
figure). It is `experience` if it rests on something specific the writer
built, used or saw. It is `assertion` if it offers neither. The labels say
nothing about whether a comment is right. They say how much of it a reader
would have to take on faith, which is the difference HN regulars pick up in a
sentence: a sourced correction, a war story, or a confident one-liner. Comments
that make no claim at all (pure questions, thanks, banter) are outside the
three labels and were set aside.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

Every label answers one question about a comment: **what does it rest its
point on?** Not whether it's right, smart or polite. A sourced comment can be
wrong, and an unsupported one can be true.

### `evidence`

**Definition:** The comment backs its point with something specific a reader
could check without taking the writer's word for it: a link, a named source, a
quote, a version or CVE number, a date, or a number about the world.

**Example 1:** *(HN item 49523310)*
> Apparently, remote improvements became separated from telemetry in Firefox version 148: https://support.mozilla.org/en-US/kb/remote-improvements#w_what-are-remote-improvements

**Example 2:** *(HN item 48059896)*
> At the moment it doesn't seem to be.
>
> Within an hour of be advised of, and running the mitigation for DirtyFrag, my upstream provider has blocked all WHM/cPanel/SSH/FTP/SFTP access with a heads-up on:
>
> CVE-2026-29201
> CVE-2026-29202
> CVE-2026-29203
>
> which look like a repeat of CVE-2026-41940 a week ago.

### `experience`

**Definition:** The comment backs its point with the writer's own first-hand
experience: something specific they built, used, ran, or saw happen.

**Example 1:** *(HN item 49014319)*
> I worked on a system a couple years ago with a BERT-based model (64M parameters) used for classification. The rest of the system could process data at gigabytes per second, and so here tokenization at a measly few megabytes per second really slowed things down. The model inference was more expensive than tokenization, but tokenization was still >10% of total runtime.

**Example 2:** *(HN item 48829152)*
> I tried it for family location sharing a few months back and, I don't remember exactly, but I remember the UI/UX feeling a bit slow/clunky in general, eventhough setting things up was user-friendly. Definitely potential there, though.

### `assertion`

**Definition:** The comment makes a claim, judgment or suggestion but offers
neither checkable support nor first-hand experience for it.

**Example 1:** *(HN item 48918161)*
> Multipass is just an apt-get or brew command away. People trust software too much these days.

**Example 2:** *(HN item 49499287)*
> This is a reach. Children can't vote. If that was a real concern you would be banning adults from social media.

### The hardest boundary

**Which two labels:** `evidence` vs `experience`. Both offer support, and HN
commenters constantly mix "here's a number" with "here's what happened to me".
The first `experience` example above is the post that sits on this line: it is
full of numbers (64M parameters, gigabytes per second, >10% of runtime), and
every one of them comes from a system only the writer has seen.

**The decision rule I used every time:**

**Who does the reader have to trust?** If the support can be checked by someone
who doesn't trust the writer (a link, a quote, a version number, a public
event pinned to a date, a number about the world), it's `evidence`, even when
it's told in the first person. If the only support is the writer's own account of what happened to them, it's
`experience`, even when it includes numbers from their own system ("our build
went from 14 to 4 minutes"). A link the reader can follow counts as `evidence`
even when it points to the writer's own repo, write-up or demo, because the
reader can go and look at the thing itself.

**The other rules, which keep the remaining cases consistent:**

- **Precedence.** Label by the strongest support the comment offers:
  `evidence` > `experience` > `assertion`. A comment with a link and a personal
  story is `evidence`.
- **`experience` vs `assertion`: is a specific thing described?**
  `experience` needs the writer to say what they did, used or saw, and where or
  how often: a job, a tool, a project, a device, a count of times. A summary of
  repeated first-hand events counts ("every startup I've worked at, four now,
  rewrote the backend"). Credentials on their own ("I've done this for 20
  years"), "in my experience…", "I've always found…" and "I think…" with
  nothing specific described are `assertion`.
- **Specific enough to look up means there's a pointer:** a link, a named
  document or source, a quote, an identifier (a version, CVE, model or bill
  number), a date, or a number about the world (a price, a count, a
  percentage). A fact about a named thing given with none of those ("the M2 Air
  has no fan", "Java applets died", "Rust is memory safe") is not `evidence`,
  however true or well known. A comparison to a past event counts only if the
  event is pinned down by one of those pointers. A named period that pins the
  event counts as a date ("during Trump's first term"); "recently" does not.
  Identifiers mean the kinds listed. A config key, API name or kernel parameter
  on its own is a fact about a named thing, not a pointer.
- **The support has to support the point.** A link to something unrelated to
  the claim doesn't make a comment `evidence`.
- **Scope.** A comment that makes no claim at all (a pure question, a
  thank-you, banter) doesn't fit any of the three, and was set aside rather
  than forced into one. A rhetorical question that is really a claim is
  labelled by that claim. A question that also states a separate claim is in
  scope and labelled by that claim. Posts not written in English are set aside,
  because neither labeller nor model can judge what they rest on. How many were
  set aside is in The Dataset.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Hacker News comments, pulled with
`collect_hn.py` through the public Algolia HN Search API (no account, no key).
It takes a random sample of 90 well-discussed stories posted between 2026-05-01
and 2026-10-15 (150+ points, 60+ comments), and at most 5 comments from each,
so no single thread dominates. Comments are kept whole, never trimmed. Comments
under 12 or over 200 words, code-block comments, and mostly-quoted replies are
skipped. That gives a 450-comment pool in `data/hn_candidates.csv`, already in
random order. I labelled the first 256 in pool order. 231 went into
`labels.csv`, and **25 were set aside** under the Scope rule: 12 pure questions
or requests, 7 thank-yous, banter or personal asides, and 1 post not in
English, plus 5 that I judged to make no claim during the cold pass. The set-aside posts are in `data/set_aside.csv` with the reason for
each. The HN item id for every labelled post is in its `note` column
(`hn:<id>`), so each one can be traced back to its source.

**How I labelled them:** In three passes, all against the written taxonomy
above.

1. **Cold, 20 rows (`cold` in `note`).** I labelled these by hand, blind,
   with `label_cold.py`. It shows one post at a time with the rules on screen
   and hides any existing label. Nothing else was looked up or consulted. I
   went through the cold set twice, and the second pass is the one recorded.
   5 of the 25 cold posts I judged to make no claim, so they were set aside.
2. **AI pre-labels, 211 rows.** Claude pre-labelled every remaining post with a
   label and a one-line reason naming the rule that decided it.
3. **Review of every pre-label, by an agent standing in for me.** A second
   Claude agent, set up to apply only my written rules, read each pre-labelled
   post in full and judged it before looking at the pre-label. It accepted 208
   (`pre-labelled, checked`) and corrected 3 (`pre-labelled, corrected in
   review (was …)`). I set the rule that any disagreement going past three
   rounds would come back to me, and none did; every one was settled within
   two. All three corrections came from one line tightened in review: a
   question that also states a separate claim is in scope, not set aside. One
   more post (in Italian) led to a new Scope line, setting aside posts not
   written in English.

Four rule clarifications came out of labelling and are now in the taxonomy
above: a named period counts as a date, a config key or API name on its own
isn't a pointer, and the two Scope lines above.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `assertion` | 146 | 63.2% |
| `experience` | 45 | 19.5% |
| `evidence` | 40 | 17.3% |
| **Total** | **231** | 100% |

No label is above the 70% cap. `assertion` is above the notebook's 60%
"getting lopsided" warning, which matches the reading in Milestone 1: most HN
comments make a claim and back it with nothing. Always guessing `assertion`
would already score about 0.63, so criterion 1 is written relative to that
share rather than as a fixed number.

**Hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1. A named period, with no date** *(HN item 49489231)*
> *The post:* "During Trump 1.0, retaliatory tariffs were targeted at swing states. E.g., on Harley-Davidsons manufactured in Wisconsin. The goal was to make it politically painful to the president and undermine his reelection chances. I imagine Carney is picking industries that are assymetricly painful to the USA…"
>
> *Could have been:* `evidence` or `assertion`.
>
> *I chose `evidence`, because:* the pointer rule needs a date, and "Trump 1.0"
> isn't one. But it pins the event to a four-year window, and with Harley-Davidson
> and Wisconsin named, a reader can look up exactly which tariffs are meant.
> "Jensen recently proposed…" (HN item 49690277) has no such anchor and stayed
> `assertion`. This post is why the taxonomy now says a named period that pins
> the event counts as a date, and "recently" does not.

**2. A quoted error message from the writer's own machine** *(HN item 48530797)*
> *The post:* "Nice idea! fwiw, false positives and all, but the Windows 11 default Windows Security doesn't like it: `leakless.exe: Operation did not complete successfully because the file contains a virus or potentially unwanted software.`"
>
> *Could have been:* `evidence` (a verbatim quote, a named product) or `experience`.
>
> *I chose `experience`, because:* Rule 1 asks who the reader has to trust. The
> quote isn't from a public source. It's what appeared on the writer's own
> screen when they ran the file, so the reader is taking their word for it.
> Quoting text only makes a post `evidence` when the source is something the
> reader can go and look at.

**3. First-hand details that don't back the point** *(HN item 48419032)*
> *The post:* "The only good use case for a credit card is if you are buying something from someone you do not trust. I have a CC and it use it a few times a year. But using them to pay for groceries or ordering something from Amazon is just moronic. … (no judging I grew up poor and had to hide from debt collectors when I was a kid)."
>
> *Could have been:* `experience` or `assertion`.
>
> *I chose `assertion`, because:* the post has real first-hand specifics ("a
> few times a year", "grew up poor"), which Rule 2 would count. But none of
> them is the reason groceries on a card is "moronic". They're asides.
> `experience` means the experience backs the point, the same test Rule 3
> applies to links. The same call covered "I personally don't like memory, so I
> disable it on all platforms" (HN item 48924776).

**4. A question with a first-hand premise** *(HN item 49819380)*
> *The post:* "My enterprise org has this model disabled because "security." Does this mean they literally need to go in and check a box? Or is it a standard thing that enterprise accounts get these later than the consumer/API accounts?"
>
> *Could have been:* set aside as a question, or `experience`.
>
> *I chose `experience`, because:* it isn't a pure question. Its first sentence
> states a first-hand fact, with scare quotes that carry a judgment. It was
> pre-labelled as set aside and corrected in review. That correction became the
> Scope line "a question that also states a separate claim is in scope".

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, fine-tuned for 3-way sequence
classification (`evidence`, `experience`, `assertion`), from notebook
sections 1–5.

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128
tokens, seed 42. Trained on **`mps` (Apple M4 GPU), torch 2.14.1**, which is
also recorded in `results.json`. The run took under a minute: 33 optimizer
steps, 17 seconds of training.

**Anything I changed from the defaults, and why:** Nothing. This first run
uses the notebook defaults on purpose, so it's the reference the stretch run
below is compared against. The only notebook edits are `LABELS`, which matches
the CSV exactly, and the name and email lines.

**Split sizes:** 70/15/15 stratified on seed 42, giving train 161, val 35,
test 35.

| Label | Train | Val | Test |
|---|---|---|---|
| `evidence` | 28 | 6 | **6** |
| `experience` | 31 | 7 | **7** |
| `assertion` | 102 | 22 | 22 |

Both minority labels have fewer than 8 posts in the test split. One post moves
`evidence` recall by 17 points and `experience` recall by 14, so their F1s will
jump between seeds in unit 6. That's expected from a 231-row set where
`assertion` is 63%, and it's why criterion 2 is a floor checked on every seed
rather than an average.

**What the run produced** (`results.json`, `test_split.csv`): the model
predicted `assertion` for all 35 test posts. That's accuracy 0.629 (22 of
35), exactly the `assertion` share of the split, and F1 0.00 for `evidence`
and `experience`. Training loss fell every epoch (1.003 → 0.852 → 0.797) and
validation loss with it (0.913 → 0.862 → 0.838), but 33 steps at 2e-5 never moved it off the
majority class. Unit 6 reads these numbers properly. This is noted here because
it's the baseline for the second training run.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: the easy/hard check on my criteria**

- *What I asked for:* With targets drafted for all five criteria, I asked
  Claude for one reason each target might turn out too easy and one it might
  turn out too hard. I told it not to say which was more likely and not to
  suggest numbers.
- *What came back:* For accuracy ≥ 0.65, it pointed out that my 55%
  `assertion` estimate came from only 33 posts. If the real share landed near
  65%, a fixed 0.65 would just be the score for always guessing `assertion`.
- *What I changed:* I made criterion 1 relative: at least 0.65 **and** at least
  0.10 above that seed's `assertion` share. The real share came out at 63%,
  and the first run scored 0.629 by predicting `assertion` for every post. The
  fixed version would nearly have passed a model that learned nothing.

**Moment 2: stress-testing the taxonomy**

- *What I asked for:* Eight posts written to sit on my label boundaries,
  classified using only my written rules, each marked CLEAN or UNCLEAR.
- *What came back:* Two were UNCLEAR: a summary of repeated experience
  ("every startup I've worked at, four now…"), and a link to the writer's own
  write-up. A second round exposed an overlap: a well-known fact about a named
  thing ("the M2 Air has no fan") could be read as either `evidence` or
  `assertion`.
- *What I changed:* I rewrote Rule 2 to count summaries of repeated first-hand
  events, ruled that links to your own work count as `evidence`, and added the
  pointer rule (evidence needs a link, source, quote, identifier, date or
  figure). After three rounds, 14 of 14 posts were clean. The full record is in
  `stress_test.md`.

**Pre-labelling disclosure:** Claude pre-labelled 211 of the 231 rows, each
with a one-line reason naming the rule that decided it. I didn't review those
one by one. I had a Claude agent review every pre-label as my stand-in,
applying only my written rules and judging each post before seeing its
pre-label. It corrected 3 and accepted the rest. I set the rule that any
disagreement going past three rounds came back to me, and none did. I
labelled the 20 `cold` rows by hand, blind, with `label_cold.py`. The criteria
targets and reasons were drafted by the same agent from my scaffold, then
checked over three rubric rounds and three easy/hard rounds before I filed
them. Claude also wrote `collect_hn.py`, drafted the taxonomy and the README
text, and ran the notebook.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
