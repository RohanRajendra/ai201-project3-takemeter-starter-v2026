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

### `question` *(stretch: the fourth label)*

Added after the core was built and kept out of `labels.csv` (see Stretch
Features). Its rows are in `labels_stretch.csv`.

**Definition:** The comment asks for information, clarification or help the
writer doesn't have, and makes no claim of its own.

**Example 1:** *(HN item 48689514)*
> I'm curious prior to this has there been any research/attempts at chemical methods to strengthen the structure and allow it to be unrolled?

**Example 2:** *(HN item 48460570)*
> Sorry to be off topic, but I have a question: has anyone installed the latest beta iOS and macOS, and if so what is the current status of Gemini integration?

**Boundary with the other three:** the Scope rule decides it. Only a pure
question or request is `question`. A question that also states a separate
claim, including a first-hand premise or a "surely…" aside, gets the label for
that claim. A rhetorical question that is really a claim is labelled by the
claim. This is why adding the label changed none of the 231 core rows.

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
text, and ran the notebook. The 93 stretch rows in `labels_stretch.csv` were
made the same way: Claude pre-labelled 112 candidates and the same agent
reviewed every one, correcting 15. Claude also wrote `stretch_runs.py` and ran
the stretch runs.

---

## Stretch Features

**Declared before building.** This section was committed before any stretch
data was collected or any stretch run was made. Results are added under each
item once it's built.

**Everything stretch lives alongside the core, not in it.** `labels.csv`, the
notebook's defaults, `results.json` and `test_split.csv` stay exactly as they
were at the end of Milestone 6, so unit 6 tests the setup the criteria were
written for. Stretch data goes in `labels_stretch.csv` (with a `stretch` column
saying which item each row belongs to), stretch runs in `stretch_runs.py`
(which reuses the notebook's own split, train and evaluate functions
unchanged), and stretch results in `results_stretch_*.json`. Every run uses
seed 42.

### 1. A second training run with one hyperparameter changed

- **The change:** `EPOCHS` 3 → 10. Nothing else changes: same 231 rows, same
  seed-42 split, same learning rate, batch size and max length.
- **Why this one:** run 1 took only 33 optimizer steps and predicted
  `assertion` for every test post, while training and validation loss were
  still falling. More passes over the same data is the most direct test of
  whether the model was under-trained or can't learn the distinction at all.
- **What I'll report:** accuracy, macro F1, per-label F1 and the confidence
  gap, against run 1, with the size of every change.

**Result: built.** `python stretch_runs.py epochs` → `results_stretch_epochs.json`.
Same 161 / 35 / 35 split and the same 35 test posts as `results.json`. Before
using the runner I checked it: run with 3 epochs, it reproduces `results.json`
exactly, down to the confusion matrix.

| Measure | Run 1 (3 epochs) | Run 2 (10 epochs) | Change |
|---|---|---|---|
| Accuracy | 0.629 | 0.771 | **+0.143** (22 → 27 of 35 right) |
| Macro F1 | 0.257 | 0.651 | **+0.394** |
| F1 — `evidence` (n=6) | 0.000 | 0.727 | +0.727 (P 0.80, R 0.67) |
| F1 — `experience` (n=7) | 0.000 | 0.333 | +0.333 (P 0.40, R 0.29) |
| F1 — `assertion` (n=22) | 0.772 | 0.894 | +0.122 (precision 0.63 → 0.84) |
| Confidence gap (most − least sure third) | 0.545 | 0.455 | −0.091 |
| Mean confidence when right | 0.641 | 0.802 | +0.161 |

**What moved, and what it says:**

- **The model got off the majority class.** Run 1 predicted `assertion` 35
  times out of 35. On the validation split, run 2 was still doing that after
  epoch 2 (30 optimizer steps, about where run 1 stopped). It first predicted a
  minority label at epoch 3. Validation macro F1 was 0.26 at epochs 1–2, 0.49 at
  epoch 3, 0.76 at epoch 5 and 0.81 at epoch 10. So run 1 was under-trained, not unable to learn the
  distinction.
- **`evidence` was learned first and best.** 4 of 6 found, with 1 false alarm.
  The pointers (links, figures, version numbers) are surface cues, as the
  criteria context predicted.
- **`experience` is still the weak label, and the errors run toward
  `assertion`.** 4 of the 7 real `experience` posts were called `assertion`,
  while only 1 `assertion` was called `experience`. That's the Rule 2 boundary
  (is a specific thing described?), and it has no surface cue beyond "I".
- **The hardest boundary shows up too.** 2 of the 6 `evidence` posts were
  called `experience`. Those are first-person posts with a pointer, exactly the
  line Rule 1 draws.
- **The confidence gap shrank, but run 1's gap meant nothing.** Run 1 was
  "right" only on `assertion` posts. In run 2 both thirds are better (1.00 and
  0.55, against 0.82 and 0.27), and the model is surer when it's right.

These are one seed on 35 test posts, so a single post moves `experience` F1 by
roughly 0.1–0.15. They show the direction, not a stable number. That's unit 6's
three-seed job, and the notebook's default stays at 3 epochs, so unit 6 starts
from the run the criteria were written against.

### 2. A fourth label, `question`

- **What it captures:** comments that make no claim and only ask for
  something. 12 of the 256 posts I labelled were pure questions or requests
  and had to be set aside, because the three labels describe how a claim is
  supported and these make none. A three-label model still has to put them
  somewhere.
- **Definition (to be added to the taxonomy):** the comment asks for
  information, clarification or help the writer doesn't have, and makes no
  claim of its own.
- **Boundary rule:** the existing Scope line decides it. A question that also
  states a separate claim is labelled by that claim, and only a pure question
  is `question`. So none of the 231 existing rows change label.
- **Data:** the set-aside pure questions, plus pure questions from the
  unlabelled rest of the pool (and a fresh pull if needed), labelled with the
  same pre-label-and-review workflow. Target at least 40 `question` rows.
- **What I'll report:** the four-label run (run 1's data plus the `question`
  rows, run 2's settings), with per-label F1 including `question`, and what
  happened to the other three labels.

**Result: built.** `python stretch_runs.py question` → `results_stretch_question.json`.
The 43 `question` rows in `labels_stretch.csv` come from four places:

| Source | Rows |
|---|---|
| Pure questions I had set aside from the core pool (`data/set_aside.csv`) | 11 |
| Unlabelled rest of the core pool (rows 256–449 of `data/hn_candidates.csv`) | 10 |
| Fresh pull 1 (`data/hn_extra_pool.csv`, 120 new stories) | 13 |
| Fresh pull 2 (`data/hn_question_pool.csv`, 80 more new stories) | 9 |

The candidates were posts with a "?" in them, pre-labelled and then reviewed
under the rules, like the core. 45 were proposed and 2 were corrected to
`assertion` in review: one rhetorical question, and one question wrapped in
"surely…" claims. The questions were split 70/15/15 on their own (seed 42) and
added to the core split, so the test set is the same 35 core posts plus 7
held-out questions.

| Label | Precision | Recall | F1 | Test n |
|---|---|---|---|---|
| `evidence` | 0.667 | 0.667 | 0.667 | 6 |
| `experience` | 1.000 | 0.429 | 0.600 | 7 |
| `assertion` | 0.759 | 1.000 | 0.863 | 22 |
| `question` | 0.750 | 0.429 | 0.545 | 7 |
| **All 42** | | | macro 0.669 | accuracy 0.762 |

**What it captures that the three missed:** about 1 in 7 of the comments I
read in Milestone 1, and 12 of the 256 I labelled, were pure questions or
requests that make no claim at all. A
three-label model has to call every one of them `evidence`, `experience` or
`assertion`, and its scores never show those mistakes, because the questions
were never in its test set. With the fourth label they're measurable: the model
finds 3 of the 7 held-out questions, and 3 of the 4 it misses go to
`assertion`. That's the expected direction, since a short question looks like a
short unsupported claim.

**What happened to the other three labels** (the same 35 core test posts, so
this compares directly with run 2):

| Measure, on the 35 core posts | Run 2 (3 labels) | Run 4 (4 labels) | Change |
|---|---|---|---|
| Accuracy | 0.771 | 0.829 | +0.057 (27 → 29 right) |
| Macro F1 over the 3 core labels | 0.651 | 0.748 | +0.097 |
| F1 — `evidence` | 0.727 | 0.727 | 0 |
| F1 — `experience` | 0.333 | 0.600 | +0.267 |
| F1 — `assertion` | 0.894 | 0.917 | +0.023 |

The core labels didn't get worse, and `experience` got better: 3 of 7 found
with no false alarms, against 2 of 7 with 3 false alarms in run 2. I wouldn't
read much into that. It's two posts on one seed, and the four-label model also
trained on 29 more posts. One real `experience` post was called `question`,
which is the new boundary showing up.


### 3. 50 extra examples for the thinnest label

- **Which label:** `evidence`, with 40 rows (17.3%), the thinnest of the three.
- **Where they'll come from:** a fresh `collect_hn.py` pull from different
  stories (new seed, excluding every comment already in the pool). Candidates
  get pre-filtered to comments with a link, a number or a quote, to save
  reading, then labelled with the same workflow. The first 50 that come out
  `evidence` are kept; the filter only decides what gets read, not the label.
- **A fair comparison:** the 50 new rows go into the training split only. The
  model is tested on exactly the same 35 test posts as run 2, with the same
  settings, so the only thing that changes is the extra `evidence` data.
- **What I'll report:** `evidence` precision, recall and F1 against run 2, plus
  whatever happens to the other labels.

**Result: built.** `python stretch_runs.py extra` → `results_stretch_extra.json`.

**Where the 50 came from:** 43 from fresh pull 1 (`data/hn_extra_pool.csv`,
120 stories not in the core pool) and 7 from fresh pull 2
(`data/hn_question_pool.csv`, 80 more). `collect_hn.py` now has an `--exclude`
option that skips every story and comment already pulled, so the three pools
share no stories. Two changes from the declared plan:
- **The filter got stricter partway through.** The first 55 candidates under
  "any digit or quote mark" gave only 11 `evidence` posts, so for the rest I
  read only posts with a link, a %/$ figure or a year, or a quoted phrase of 3
  or more words. The filter still only decided what got read; every label came
  from the rules.
- **More candidates than planned.** 67 `evidence` candidates were pre-labelled
  and reviewed. The review overrode 13 of the first 56, mostly links that only
  name the subject, define a word, or back a side remark rather than the claim,
  and those 13 were dropped. That left 43, and 7 more from pull 2 made 50.

The 50 were added to the **training split only** (`evidence` goes from 28 to
78 training posts, 17% → 37% of training). Validation, test and settings are
identical to run 2.

| Measure, same 35 test posts | Run 2 (10 epochs) | Run 3 (+ 50 `evidence`) | Change |
|---|---|---|---|
| `evidence` precision | 0.800 | 0.667 | −0.133 |
| `evidence` recall | 0.667 | 0.667 | 0 (4 of 6 both times) |
| `evidence` F1 | 0.727 | 0.667 | **−0.061** |
| `experience` F1 | 0.333 | 0.429 | +0.095 |
| `assertion` F1 | 0.894 | 0.818 | −0.076 (recall 21 → 18 of 22) |
| Accuracy | 0.771 | 0.714 | −0.057 (27 → 25 right) |
| Macro F1 | 0.651 | 0.638 | −0.013 |

**What happened to `evidence`'s numbers: nothing good.** The model found 4 of
the 6 test `evidence` posts with and without the extra 50, and picked up one
more false alarm, an `assertion` post called `evidence`. The
bigger effect was on `assertion`. Tripling `evidence` in training shrank
`assertion`'s share from 63% to 48%, the model called `assertion` less often,
and 3 real `assertion` posts went to `experience` and 1 to `evidence`.

**What I take from it:** `evidence` wasn't short of examples. Its surface cues
were learnable from 28. In run 2 both misses went to `experience`, the Rule 1
boundary (first person plus a pointer). In run 3 one went to `experience` and
one to `assertion`. 50 more link-heavy posts don't teach where Rule 1 draws
its line. The extra rows also arrived
through a filter that favours links, so they may have taught "link means
`evidence`" more strongly than the rules mean it. With 6 test posts every
change here is one post, and one seed. A stable answer needs unit 6's three
seeds.

**Known soft spots the stretch review turned up** (written down, not fixed, so
the core stays frozen for unit 6):
- **Praise in front of a question.** "Neat!!! Does this work with mailto…?"
  went in as `question`, while a standalone "This is so cool…" post in the core
  is `assertion`. I treat praise as a judgment only when it's the whole point
  of the post.
- **A suggestion plus a link to the thing suggested.** One core row (HN item
  49377302: "You could also distill the Anticipatory Music Transformer… [link]")
  is `evidence`. Under the stricter line the stretch review used, where the
  link has to let the reader check the claim, it would probably be
  `assertion`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Unit 6 Stretch Features

**Declared before building.** This section was committed in the Milestone 1
commit, before any three-seed run, confusion matrix or improvement existed.
Results are added under each item once it's built.

**1. A confidence check:** are the model's confident predictions right more
often than its unsure ones?
- **The numbers:** for every seed, before and after the improvement, the
  accuracy of the most-confident third of test predictions against the
  least-confident third, and the mean confidence when right against when
  wrong. All of these are already in `results_three_seeds_before.json` and
  `results_three_seeds_after.json`.
- **When:** written alongside Milestone 4, because criterion 3 is the
  confidence criterion and uses the same numbers.
- **What it reports:** whether confidence tracks correctness, and whether the
  answer changes once the model stops predicting one label.

**Result, before the improvement** (`results_three_seeds_before.json`;
11 posts per third):

| Seed | Most-sure third right | Least-sure third right | Gap | Mean confidence when right | Mean confidence when wrong |
|---|---|---|---|---|---|
| 42 | 0.818 | 0.273 | +0.545 | 0.641 | 0.583 |
| 7 | 0.545 | 0.545 | 0.000 | 0.616 | 0.605 |
| 2024 | 0.909 | 0.455 | +0.455 | 0.624 | 0.551 |

**On two of the three seeds, the confident predictions were right more often.
But the comparison is close to empty.** Every prediction was `assertion`, so
"right" just means "the post really was `assertion`", and confidence only
measures how `assertion`-like the model found each post. The mean confidence
gap between right and wrong predictions is small on every seed (0.058, 0.011
and 0.073), and every one of those means sits between 0.55 and 0.64. The model
was about equally sure of every post, right or wrong. The after half of this
check, once the model predicts all three labels, goes under Milestone 5.

**Result, after the improvement** (`results_three_seeds_after.json`; 11 posts
per third):

| Seed | Most-sure third right | Least-sure third right | Gap | Mean confidence when right | Mean confidence when wrong |
|---|---|---|---|---|---|
| 42 | 1.000 | 0.545 | +0.455 | 0.802 | 0.663 |
| 7 | 0.818 | 0.364 | +0.455 | 0.751 | 0.656 |
| 2024 | 1.000 | 0.636 | +0.364 | 0.804 | 0.733 |

**Yes, once the model actually discriminates.** On every seed, its most
confident third is right 82–100% of the time, against 36–64% for its least
confident third. When it's right it's more sure, by 0.07 to 0.14 on average.
That's also why criterion 3 flipped from MISSED to MET.

The difference from before is what the confidence means. Before, every post
got the same label, so confidence only ranked how `assertion`-like a post
looked, and the mean confidences when right and wrong were within 0.06 of each
other. Now the model is choosing between labels, and its confidence separates
its right answers from its wrong ones on all three seeds.

**What it could be good for:** if the pattern holds, a confidence threshold is
a triage rule. Send the least-sure third to a human and keep the rest. Whether
the `experience`/`assertion` mistakes actually sit in that unsure third needs
per-post confidences, which `results_three_seeds_after.json` doesn't store. The
per-label error write-up below re-runs the seeds and checks it post by post.

**2. A per-label error write-up** for whichever label the post-improvement
confusion matrix says is worst (lowest F1 across the three seeds).
- **Method:** `error_analysis.py` re-runs the improved setting on the same three
  seeds and saves every test prediction (`error_analysis.json`). I'll check it
  reproduces `results_three_seeds_after.json`.
- **What it says:** which label the worst label gets confused with, in which
  direction, and what the misclassified posts have in common, read post by
  post against the taxonomy.
- **When:** right after Milestone 5. The before model is expected to predict
  `assertion` for everything, so its errors have nothing to say about any one
  label.

**Result: built.** `python error_analysis.py` → `error_analysis.json`. On all
three seeds it reproduces `results_three_seeds_after.json` exactly, accuracy
and confusion matrix both, so these are the after run's own predictions.

**The worst label is `experience`:** mean F1 0.354 across the seeds (0.333,
0.286 and 0.444), against 0.768 for `evidence` and 0.832 for `assertion`.

**What it's confused with, and which way.** Pooled over the three seeds, real
`experience` posts appeared 21 times in a test split. 6 were caught, **14 were
called `assertion`** and 1 was called `evidence`. The model said `experience`
14 times and was right 6 times; the other 8 were 6 `assertion` and 2
`evidence` posts. So it's `experience` vs `assertion`, mostly in one
direction: 14 lost to `assertion` against 6 taken from it.

**What the 10 `experience` posts it called `assertion` have in common** (the
14 misses are 10 distinct posts, because some sit in more than one seed's test
split). I read each one against the taxonomy.

1. **The first-hand part is one clause inside a post shaped like a claim,
   advice or praise (6 of 10).**
   - "I'm getting the impression that LLMs are just not very good at
     'reasoning' about time. I have definitely had success getting a coding
     agent to produce decent concurrent code, but I had to basically lead it
     by the nose…" (HN 48175023)
   - "dense small models do not like quantization. i find 27b fp8 to be
     smarter…" (HN 48974634)
   - "This is a beautiful way to present extremely high quality information. I
     sometimes lament… searches for '%{title} filetype:pdf'…" (HN 48828914)
   - "Haha, same! I was literally looking for this feature last week… the
     problem is rarely that it can't do something, but the ergonomics…"
     (HN 48595928)
   - A tip: "One trick I've used is creating a folder…" (HN 48593831)
   - Congratulations plus advice: "This is awesome. Congratulations!… you
     haven't specified a license…" (HN 48265006)

   My precedence rule says one specific first-hand clause makes the whole post
   `experience`. The model reads the post's overall shape, which is an
   `assertion`.
2. **The rest are a question with a first-hand premise (1), a vague
   first-hand claim (1), and two plain stories (2).**
   - **The question** is README hard case 4: "My enterprise org has this model
     disabled… Does this mean…?" (HN 49819380). It was set aside at first and
     corrected in review.
   - **The vague claim:** "I've been using `claude -p` for personal use for a
     long time without issues" (HN 50001679). Rule 2 needs "where or how
     often", and "a long time" barely meets it.
   - **The two stories** are the only clean misses: the grad-thesis charts
     (HN 48270492) and Cliff not reading his own Wikipedia page (HN 48066912).
3. **"I" can't tell the pair apart.** 13 of the 14 misses contain first-person
   words (I, I've, I'm, my, we, our), but so do 22 of the 60 `assertion` posts
   the model got right. It's the only surface cue this pair has, and both
   labels use it. `evidence` has links and numbers.
4. **Some of it is my labelling, and I can point at it.** HN 48265006 is one
   of the two `cold` rows where my hand label (`experience`) differed from the
   review agent's earlier blind label (`assertion`). The model sided with the
   agent. Two more were already on record as hard: 48828914 got a hard note in
   the review, and 49819380 is README hard case 4. That matches the agreement report, where my one
   pile-(a) slip was on the staff boundary that maps to this one. Still, only
   1 of the 10 traces to two labellers actually disagreeing.
5. **They're longer.** The median miss is 47 words, against 37 for the
   `experience` posts it caught and 28.5 for `assertion` posts it got right.
   Longer posts carry more claim around the first-hand clause.

**The other direction: 8 posts wrongly called `experience`.** All 8 are in the
least-sure third (confidence 0.44–0.61). They're first-person claims or
predictions: "I predict this is too" (HN 48095986), "Personally I definitely
expect…" (HN 48849796), "Author here…" (HN 49411339). Two are `evidence` posts
in the first person, with a pointer that decides them under Rule 1: a
"$50/1M tokens" price (HN 48997783) and a linked poll (HN 49581079). The model
followed the voice, not the pointer. That's my hardest-boundary rule failing
in the direction I predicted in unit 5.

**Checking the triage claim from the confidence check:**

| Third (33 / 39 / 33 posts over 3 seeds) | Right | Wrong | Accuracy |
|---|---|---|---|
| Least sure | 17 | 16 | 0.52 |
| Middle | 30 | 9 | 0.77 |
| Most sure | 31 | 2 | 0.94 |

Of the 20 `experience`/`assertion` mix-ups, 12 are in the least-sure third, 6
in the middle and 2 in the most-sure. Sending the least-sure third to a human
would catch 16 of the 27 errors (59%), including 12 of the 20 mix-ups. The 2
confident mistakes are both `experience` posts called `assertion` at about
0.91: HN 48595928, a first-hand clause inside a claim, and HN 50001679, the
vague claim.

**What this points the second improvement at.** `experience` is the thinnest
label by F1, and its misses are mostly the precedence case: a first-hand
clause inside a claim-shaped post. With 31 training examples, the model hasn't
seen that pattern often enough to learn that the clause decides the label.
Relabelling doesn't look like the fix, because only 1 of the 10 misses traces
to a labeller disagreement. More `experience` examples does, the brief's
"thirty more posts of the label with the worst F1".

**3. A second measured improvement:** one more change, chosen from the
post-improvement diagnosis and the error write-up, made on top of the first.
- **How it's measured:** the same three seeds, with `RUN_LABEL = "after2"` →
  `results_three_seeds_after2.json`, and a third run log in the same format.
- **What it reports:** whether it helped, against the first improvement's log,
  and how I know.

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

**Same posts, both columns:** the 35 held-out posts in `test_split.csv`
(seed 42). For the baseline, `baseline_results.json` records `held_out: true`
and `n: 35`; for the trained model, `results.json` records `n_test: 35`. The
baseline is `facebook/bart-large-mnli`, zero-shot, using only the three
definitions in `label_definitions.txt`. Trained is the unit 5 run in
`results.json` (DistilBERT, 3 epochs). Both ran on **`mps`** (Apple M4).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.514 | 0.629 | +0.114 |
| Macro F1 | 0.385 | 0.257 | -0.127 |
| F1 — `assertion` | 0.682 | 0.772 | +0.090 |
| F1 — `evidence` | 0.222 | 0.000 | -0.222 |
| F1 — `experience` | 0.250 | 0.000 | -0.250 |

**What the definitions were worth** (same 35 posts, three prompts; files in
`baseline_extra/`):

| Baseline prompt | Accuracy | Macro F1 | F1 `evidence` | F1 `experience` | F1 `assertion` |
|---|---|---|---|---|---|
| My definitions, as written in `label_definitions.txt` (**the baseline above**) | 0.514 | 0.385 | 0.222 | 0.250 | 0.682 |
| The same definitions reworded as noun phrases | 0.486 | 0.422 | 0.267 | 0.400 | 0.600 |
| Bare label names, no definitions | 0.571 | 0.469 | 0.444 | 0.250 | 0.711 |

My definitions were worth **less than nothing**: the bare names beat them by
0.057 accuracy and 0.084 macro F1. Part of the reason is mechanical.
`baseline.py` builds each hypothesis as "This post is {}.", and my definitions
start with a verb, so the model was asked whether "This post is backs its point
with something specific…" was true. Rewording them as noun phrases ("a comment
that backs its point…") recovers some macro F1 (0.385 → 0.422), but not the gap
to bare names. My reading is that the three definitions share one frame
("backs its point", "claim", "support"), so an NLI model sees three
near-identical hypotheses, while the bare words "evidence", "experience" and
"assertion" are more different from each other. With the definitions, it
called 12 posts `evidence` and got 2 right. The official baseline stays the
`label_definitions.txt` run, because that's what criterion 5 names.

**The baseline on the other two seeds' test posts** (`baseline_extra/`). This
is a supplementary check, for criterion 5's run-log row. Section 6 splits each
seed this way, so these are exactly the posts each seed's trained model is
scored on.

| Baseline (definitions) | Seed 42 | Seed 7 | Seed 2024 |
|---|---|---|---|
| Accuracy | 0.514 | 0.571 | 0.343 |
| Macro F1 | 0.385 | 0.555 | 0.310 |

Nothing was trained here, yet macro F1 moves 0.245 between splits. That
spread comes purely from which 35 posts land in the test set, and it's a
measure of how noisy any single 35-post number in this project is.

**Runtime:** one baseline pass over the 35 posts takes about 24 seconds on
`mps`, including loading the model, because it runs three NLI comparisons per
post. The fine-tuned model scores the same 35 in under a second (`eval_runtime`
0.36 s in the unit 5 run).

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

*Written before `baseline.py` had produced a single number. The trained model's
unit 5 numbers were already known, since it predicted `assertion` for all 35
test posts.*

> "I predict the trained model beats the zero-shot baseline only on overall
> accuracy and `assertion` F1: always answering `assertion` banks the 22 of 35
> majority posts, while bart-large-mnli will scatter its guesses across all
> three labels and land below 0.63. It will lose on macro F1 and on `evidence`
> and `experience` F1, because its zeros there lose to any zero-shot model that
> catches even one post with a link or a first-person story."

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

The prediction held on all five rows. The trained model "wins" on accuracy
and `assertion` F1 only because it says `assertion` for every post, and 22 of
the 35 are `assertion`. On everything that needs telling labels apart, the
untrained baseline is better: it finds 2 of the 6 `evidence` posts and 1 of
the 7 `experience` posts, and the trained model finds none. **The 3-epoch
fine-tune learned the class prior and nothing else, so fine-tuning added
nothing a reader would want.** The model never left the majority class, so
this measures the training run more than the task. Whether fine-tuning can
beat zero-shot on this taxonomy is Milestone 5's question.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**How it ran:** notebook section 6 with `RUN_LABEL = "before"`, seeds 42, 7
and 2024, the unit 5 settings unchanged (3 epochs, learning rate 2e-5, batch
16, max length 128). Every seed was trained on **`mps` (Apple M4 GPU), torch
2.14.1**; each entry of `results_three_seeds_before.json` records the device.
Each seed is a fresh stratified 70/15/15 split of the same 231 rows: 161 train,
35 val and 35 test, with 6 `evidence`, 7 `experience` and 22 `assertion` posts
in every test split. Seed 42 reproduces `results.json` exactly.

**The three seeds** (section 6's spread table):

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.629 | 0.629 | 0.629 | 0.000 |
| Macro F1 | 0.257 | 0.257 | 0.257 | 0.000 |
| F1 — `evidence` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `experience` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `assertion` | 0.772 | 0.772 | 0.772 | 0.000 |
| Confidence: most-sure third | 0.818 | 0.545 | 0.909 | 0.364 |
| Confidence: least-sure third | 0.273 | 0.545 | 0.455 | 0.273 |

**The spread is zero, but that isn't stability.** All three models predicted
`assertion` for every test post, on every seed. Stratification puts exactly
22 `assertion` posts in each 35-post test split, so an always-`assertion` model
scores 22/35 = 0.629 on all three. The notebook's note says "Accuracy moved
0.000 across seeds. Stable enough to trust", but it isn't. The number is fixed
by the split's label mix, not earned by the model. The only seed-to-seed
movement is in the confidence ranking, which only orders posts that all got
the same label. The untrained baseline moves 0.245 in macro F1 across these
same three splits, and that is the real noise level of a 35-post test.

**The run log.** The five criteria from `criteria.md`, three seeds each, on
`mps`:

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Accuracy clearly beats always guessing `assertion` | accuracy ≥ 0.65 **and** ≥ 0.10 above the seed's `assertion` share | 0.629 (share 0.629, +0.00) | 0.629 (share 0.629, +0.00) | 0.629 (share 0.629, +0.00) | **MISSED** |
| 2. No label is left behind | every label's F1 ≥ 0.50 | lowest 0.000 (`evidence` 0.000, `experience` 0.000, `assertion` 0.772) | lowest 0.000 (same three) | lowest 0.000 (same three) | **MISSED** |
| 3. Confident guesses are right more often | most-sure third − least-sure third ≥ 0.20 | 0.545 (0.818 − 0.273) | 0.000 (0.545 − 0.545) | 0.455 (0.909 − 0.455) | **MISSED** |
| 4. My labels agree with someone else's | `agreed` ≥ 23 and `compared` = 30 | 25 / 30 | 25 / 30 | 25 / 30 | **MET** |
| 5. Fine-tuning beats the zero-shot baseline | trained macro F1 − baseline macro F1 ≥ 0.15, on the same posts | −0.127 (0.257 vs 0.385) | −0.297 (0.257 vs 0.555)\* | −0.052 (0.257 vs 0.310)\* | **MISSED** |

- **Criterion 4 doesn't depend on the split.** The 30 staff posts and my labels
  are the same whichever seed trains the model, so its one measurement fills
  all three columns.
- **Criterion 5, as written, is a single comparison** on the seed-42 posts
  (`results.json` against `baseline_results.json`), so the seed-42 cell is the
  verdict. \*The seed 7 and 2024 cells compare that seed's trained model with
  the baseline scored on that seed's own test posts (`baseline_extra/`). They're
  recorded so the row has three trials, and all three miss.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, as printed by notebook section 7. Rows are true labels, columns are
the model's guesses.

| true \ predicted | evidence | experience | assertion |
|---|---|---|---|
| **evidence** | 0 | 0 | 6 |
| **experience** | 0 | 0 | 7 |
| **assertion** | 0 | 0 | 22 |

All three seeds pooled (105 test posts), from the `confusion` field of each
entry in `results_three_seeds_before.json`:

| true \ predicted | evidence | experience | assertion |
|---|---|---|---|
| **evidence** | 0 | 0 | 18 |
| **experience** | 0 | 0 | 21 |
| **assertion** | 0 | 0 | 66 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

7 real `experience` posts were called `assertion` and 0 went the other way;
the pooled count is 21 to 0. But `evidence` → `assertion` is just as total (6 of
6, and 18 of 18 pooled). So the model didn't fail one boundary. It never drew
any boundary: every post went to the majority label, which is a training
failure, not a confusion between two specific labels. Section 7's note says a
lopsided direction "usually points at your labelling". The agreement check in
Milestone 3 is the test of that, but a model that never predicts a second
label can't tell me anything about one boundary in my labels.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Accuracy clearly beats always guessing `assertion` | ≥ 0.65 and ≥ 0.10 above the `assertion` share, on every seed | **MISSED** | Accuracy is 0.629 on all three seeds. That's below 0.65, and exactly the `assertion` share (+0.00), so both conditions fail on every seed. |
| 2 | No label is left behind | every label's F1 ≥ 0.50, on every seed | **MISSED** | `evidence` and `experience` F1 are 0.000 on every seed. |
| 3 | Confident guesses are right more often | gap ≥ 0.20, on every seed | **MISSED** | Seed 7's gap is 0.000, and the target has to hold on all three seeds. Seeds 42 and 2024 clear it; the diagnosis below explains why that means little. |
| 4 | My labels agree with someone else's | `agreed` ≥ 23 and `compared` = 30 | **MET** | `agreement_results.json` has `agreed` 25 and `compared` 30. |
| 5 | Fine-tuning beats the zero-shot baseline | trained − baseline macro F1 ≥ 0.15, same posts | **MISSED** | 0.257 − 0.385 = −0.127 on `test_split.csv`. The same-posts check holds: `held_out` is true, `n` 35 equals `n_test` 35, and the definitions were used. |

**Revisions:** none. Criterion 3 has a real weakness, but it can still be
measured and it produced a verdict, so it isn't broken in the sense the brief
allows a revision for. The weakness is covered under criterion 3 below.

**Checking the verdicts against the opposite case.** Following the brief, I
argued the opposite verdict for every criterion where a reading had any room.
- **Criterion 3:** "two seeds clear 0.20 comfortably and the mean gap is 0.33".
  But the criterion says *every* seed, so MISSED stands.
- **Criterion 4:** "25 is only two posts over the target, and the staff posts
  come grouped by label". But the criterion is a count, and the grouping
  applied to both labellers, so MET stands.
- **Criterion 5:** "the baseline alone moves 0.245 across splits, so −0.127 is
  inside the noise". But the noise cuts both ways, the target asks for +0.15,
  and all three splits come out negative, so MISSED stands.
- **Criteria 1 and 2:** no reading gets 0.629 over 0.65, or 0.000 over 0.50.

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**One cause behind all four misses: the training run stopped before the model
left the majority class.** It isn't any of the three data causes (too few
examples, an inconsistent boundary, a hard pair). The nearest of the four
common causes is "a task the model can't reach from this much data", but the
evidence says this data *can* be reached. The run was just too short to reach
it: 33 optimizer steps at learning rate 2e-5. Four pieces of evidence:

1. **The confusion matrix shows no boundary at all.** Pooled over the three
   seeds, all 105 test posts were predicted `assertion` (18 of 18 `evidence`,
   21 of 21 `experience`). A boundary I labelled inconsistently would show up
   as one specific pair confused in both directions. A label that swallows
   every other label is the model learning the class prior and nothing else.
2. **The model was still learning when it stopped.** On every seed, validation
   accuracy sat at exactly 0.629, the `assertion` share, after epochs 1, 2 and
   3, while training loss kept falling (seed 42: 1.003 → 0.852 → 0.797; seed 7:
   1.047 → 0.887 → 0.835; seed 2024: 0.992 → 0.894 → 0.879). Validation loss
   fell with it (seed 42: 0.913 → 0.862 → 0.838).
3. **The agreement report says labelling isn't the cause.** It's the only
   instrument here that can separate a labelling problem from a model problem,
   and it points away from labels. I matched staff on 25 of 30 (83%), above
   their "a rate in the 70s is normal". The agent that reviewed 211 of the 231
   rows in `labels.csv` matched them on 30 of 30. Labels that consistent would
   let a working model draw at least the easy boundaries, and this model drew
   none.
4. **The same data does support learning.** The unit 5 stretch run
   (`results_stretch_epochs.json`) used the same 231 rows and the same seed-42
   split, and changed only `EPOCHS` 3 → 10. It reached accuracy 0.771 (≥ 0.65,
   and +0.14 over the share), `evidence` F1 0.727 and macro F1 0.651 (+0.266
   over the baseline). So 28 training examples are enough for `evidence`. The
   bottleneck was the number of passes, not the number of posts.

**Criterion by criterion:**

- **1 (accuracy).** Accuracy equals the `assertion` share exactly because every
  prediction is `assertion` (evidence 1). The cause is under-training
  (evidences 2 and 4).
- **2 (every label).** Both minority labels score 0 because neither is ever
  predicted (evidence 1). Once training is fixed, the label most at risk is
  `experience`. It reached only 0.333 F1 in the 10-epoch run, with its errors
  going to `assertion`. And my one pile-(a) slip in the agreement report was on
  the matching boundary: staff's `reaction` vs `hot_take` ("about the writer,
  or a claim?") is my `experience` vs `assertion`. I'll watch that pair in
  Milestone 5.
- **3 (confidence).** With every prediction `assertion`, confidence can only
  rank posts by how `assertion`-like they look, and "right" just means "truly
  `assertion`". On seed 7 the ranking didn't separate them. Both thirds held 6
  of 11 true `assertion` posts, and mean confidence when right (0.616) was
  barely above when wrong (0.605). Seeds 42 and 2024 clear 0.20 only because
  the ranking happened to put true-`assertion` posts on top. That's the
  criterion's weakness: a model that never predicts a second label can pass it.
  I've left the criterion alone (see Revisions). In practice, criterion 2 is
  the guard against one-label models, and it failed here. The cause is the
  same under-training.
- **5 (beats the baseline).** Macro F1 of 0.257 is one class's F1 averaged with
  two zeros, so even a weak zero-shot baseline (0.385, held back by its own
  definitions; see Baseline vs. Trained) beats it. The cause is under-training
  (evidences 1 and 2). Evidence 4 says the gap reverses with training.

**What the diagnosis points at:** one training setting, `EPOCHS`. The brief
warns that a training change is usually the wrong fix. Here, evidences 2 and 4
say it's the right one, and evidences 1 and 3 rule out the data fixes as the
first move. That's Milestone 5.



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 25 / 30 = 83%

I labelled the 30 posts by hand, blind, under the staff taxonomy, with
`label_staff.py`. It shows the staff definitions and rules verbatim and never
opens the answer key. My labels are in `my_staff_labels.csv`, and the result is
`agreement_results.json` (`agreed` 25, `compared` 30). I only got
`data/staff_labels.csv` from my TF after my 30 were saved.

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**A second labeller, for the diagnosis.** The agent that reviewed 211 of the
231 rows in `labels.csv` (see How I Used AI) also labelled the same 30 posts,
blind, under the staff taxonomy. Its labels are in `my_staff_labels_proxy.csv`
and its result in `agreement_results_proxy.json`.

| Comparison, same 30 posts | Agreed | Rate |
|---|---|---|
| Me vs staff | 25 / 30 | 83% |
| Review agent vs staff | 30 / 30 | 100%, including all 7 posts staff marked borderline |
| Me vs review agent | 25 / 30 | 83%, the same five posts |

One caveat on that 100%. The staff posts are grouped by label in ID order
(sp_001–010 are `analysis`, 011–020 `hot_take`, 021–030 `reaction`). The
agent noticed this only after labelling, and I can't rule out that runs of
same-label posts made agreeing easier. I labelled in the same order and got
25.

| Labels given | `analysis` | `hot_take` | `reaction` |
|---|---|---|---|
| Staff | 10 | 10 | 10 |
| Me | 7 | 15 | 8 |
| Review agent | 10 | 10 | 10 |

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

**1. sp_004**
> *The post:* "Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* **I'm right.** Rule 1 asks whether the fact carries the
> argument, but the fact never appears in the post. "Almost identical" is the
> writer's summary of a split no reader can see, and "the fast starters would
> fall apart harder" is an assumption, not a result. What's stated can't
> reliably serve as the reason for the conclusion, so it's a confident claim
> in the shape of a test: `hot_take`.
>
> *Which pile:* **(c)**. Rule 1 can be read as "a comparison was described",
> which is staff's reading, or as "a fact the reader can see is doing the
> work", which is mine. Mine is defensible.

**2. sp_009**
> *The post:* "The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* **Both defensible.** The date and the 60 m are checkable,
> and they really do support "the course changed", which is staff's reading
> under Rule 1. But the post's claim is bigger: that pre- and post-2021 PBs are
> "two different races", on the strength of a 60-metre error (0.6% of the
> distance). Read that way, the measurement is offered as a flourish on a
> conclusion already reached, which is Rule 1's own example of a `hot_take`
> with a statistic in it.
>
> *Which pile:* **(c)**. Rule 1 doesn't say how big a claim a small fact can
> carry before it becomes decoration.

**3. sp_010**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* **I'm right.** A backyard experiment is no reason to call
> this `analysis` rather than `hot_take`. The `analysis` definition asks for "a
> specific, checkable fact", and a private session with three friends and no
> times can't be checked by any reader. Three uncontrolled runners can't carry
> a claim about what shoes do. Staff's own note calls this one HARD and
> concedes the tiny sample.
>
> *Which pile:* **(c)**. "Checkable" is ambiguous between "checkable in
> principle" (staff) and "checkable by the reader" (me). My reading is
> defensible.

**4. sp_027**
> *The post:* "Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* **Staff is right.** I took "coming back felt like
> cheating" as the claim that made it a `hot_take`. But it's the writer
> reporting how their own run felt, and Rule 2 ("is it about a claim or about
> the writer?") puts that squarely in `reaction`. Nothing general about the
> world is asserted.
>
> *Which pile:* **(a)**. The rule covered it and I applied it loosely.

**5. sp_029**
> *The post:* "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* **Both defensible.** Staff's reading is Rule 2: "just
> realised" is the writer's own moment, now. My reading is that the post
> credits wrong-size shoes as the reason for every PB. That attributes a cause
> with no stats to back it up whatsoever, and "a confident claim with no
> support" is the `hot_take` definition. Staff's own note says it "could be
> read as a wry hot take".
>
> *Which pile:* **(c)**. Rule 2 can be answered both ways when a personal
> moment is the vehicle for a general jab.

**Piles:** (a) 1, (b) 0, (c) 4.

**What the pattern in my disagreements tells me:**

**All five go in one direction.** Every disagreement is me choosing
`hot_take` where staff chose something else. Not once did I call a post
`analysis` or `reaction` that staff called `hot_take`. I gave 15 `hot_take`
labels against staff's 10.

**The three `analysis` → `hot_take` calls are my own taxonomy leaking in.** My
Rule 1 asks "who does the reader have to trust?", and under my rules a
writer's private test is `experience`, not `evidence`. The staff taxonomy has
no `experience` label, so when a post's support was the writer's own
uncheckable data (sp_004, sp_010), or a small fact stretched over a big claim
(sp_009), I fell back to `hot_take`. That makes these mostly pile (c),
differences in how strict "checkable" is, not slips.

**The one real slip, pile (a), is on the writer-versus-claim boundary.**
sp_027 was a first-person report of the writer's own run, and I read it as a
claim. In my taxonomy, that boundary is `experience` vs `assertion`
(Rule 2: is a specific thing the writer did or saw described?). So on 30 posts
my own lean is to read first-person posts as unsupported claims, toward
`assertion`. That's direct evidence about one boundary in my data, and I use
it in the diagnosis.

**How far it reaches into my 231 labels.** Only my 20 `cold` rows were labelled
by me alone. The other 211 were pre-labelled by Claude and reviewed by the
agent that matched staff 30 out of 30. And on the cold rows, when I relabelled
them, the two changes from the agent's first pass went the other way, from
`assertion` to `experience`. So the agreement check says the bulk of my
training labels came from a labeller that applies written rules the way their
authors do. My lean toward the unsupported label is real but touches few rows.

---

## The Improvement

**What I changed:** one training setting. `EPOCHS` went from 3 to 10 in notebook
section 2. Nothing else changed: the same 231 labels, the same taxonomy, the
same criteria, the same learning rate (2e-5), batch size (16), max length (128)
and seeds (42, 7, 2024). Section 6 was re-run with `RUN_LABEL = "after"` →
`results_three_seeds_after.json`. `results_three_seeds_before.json` is
untouched. Every split is identical to the before run, so before and after are
scored on the same 35 test posts per seed. Trained on **`mps` (Apple M4)**,
torch 2.14.1.

**Which diagnosis pointed at it:** the diagnosis of criteria 1, 2, 3 and 5. The
before model predicted `assertion` for all 105 test posts, its validation
accuracy sat flat at the `assertion` share while training loss was still
falling on every seed, and the agreement report ruled out the labels as the
cause. Training stopped too early. 10 epochs gives 110 optimizer steps instead
of 33.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Accuracy clearly beats always guessing `assertion` | accuracy ≥ 0.65 **and** ≥ 0.10 above the seed's `assertion` share | 0.771 (share 0.629, +0.14) | 0.629 (share 0.629, +0.00) | 0.829 (share 0.629, +0.20) | **MISSED** |
| 2. No label is left behind | every label's F1 ≥ 0.50 | lowest 0.333 (`evidence` 0.727, `experience` 0.333, `assertion` 0.894) | lowest 0.286 (`evidence` 0.667, `experience` 0.286, `assertion` 0.723) | lowest 0.444 (`evidence` 0.909, `experience` 0.444, `assertion` 0.880) | **MISSED** |
| 3. Confident guesses are right more often | most-sure third − least-sure third ≥ 0.20 | 0.455 (1.000 − 0.545) | 0.455 (0.818 − 0.364) | 0.364 (1.000 − 0.636) | **MET** |
| 4. My labels agree with someone else's | `agreed` ≥ 23 and `compared` = 30 | 25 / 30 | 25 / 30 | 25 / 30 | **MET** |
| 5. Fine-tuning beats the zero-shot baseline | trained macro F1 − baseline macro F1 ≥ 0.15, on the same posts | +0.267 (0.651 vs 0.385) | +0.004 (0.559 vs 0.555)\* | +0.435 (0.745 vs 0.310)\* | **MET** |

How each verdict was decided:
- **1 MISSED.** Seeds 42 and 2024 clear both conditions, but seed 7 lands
  exactly on 22/35 = 0.629, the `assertion` share. The target has to hold on all
  three. (Seed 7 isn't collapsed; it predicts all three labels. Its right and
  wrong answers just net out to the share.)
- **2 MISSED.** `experience` is under 0.50 on every seed. `evidence` and
  `assertion` clear it everywhere.
- **3 MET.** The gap is at least 0.364 on every seed.
- **4 MET.** Unchanged, since the improvement doesn't touch my staff labels.
- **5 MET, as the criterion is written.** It's one comparison on the seed-42
  posts: the improved model's seed-42 macro F1 (0.651) against
  `baseline_results.json` (0.385), +0.267 ≥ 0.15. The same-posts check holds:
  `n` 35 = `n_test` 35, and `held_out` is true. `results.json` still holds the
  before model, and regenerating it would overwrite the evidence for the
  before verdict, so the after number comes from the seed-42 entry of
  `results_three_seeds_after.json`. That's the same split and the same code
  section 5 uses. \*The supplementary seeds show how fragile this MET is. On
  seed 7 the margin is +0.004, a miss. On seed 2024 it's +0.435. A single
  35-post comparison can come out either way, so I'd call this "met on the
  split the criterion names", not "fine-tuning reliably beats zero-shot".

**Before and after, side by side** (same seeds, same test posts):

| Criterion | Before | After |
|---|---|---|
| 1. Accuracy | MISSED (0.629 on every seed, +0.00 over the share) | MISSED (0.771 / 0.629 / 0.829; 2 of 3 seeds pass) |
| 2. Every label F1 | MISSED (lowest 0.000 on every seed) | MISSED (lowest 0.333 / 0.286 / 0.444, always `experience`) |
| 3. Confidence gap | MISSED (0.545 / 0.000 / 0.455) | **MET** (0.455 / 0.455 / 0.364) |
| 4. Staff agreement | MET (25 / 30) | MET (25 / 30) |
| 5. Beats the baseline | MISSED (−0.127) | **MET** (+0.267; supplementary +0.004 / +0.435) |

| Mean over 3 seeds | Before | After | Change |
|---|---|---|---|
| Accuracy | 0.629 | 0.743 | +0.114 |
| Macro F1 | 0.257 | 0.652 | +0.394 |
| F1 — `evidence` | 0.000 | 0.768 | +0.768 |
| F1 — `experience` | 0.000 | 0.354 | +0.354 |
| F1 — `assertion` | 0.772 | 0.832 | +0.060 |

**Confusion matrix, after.** Seed 42, as printed by section 7:

| true \ predicted | evidence | experience | assertion |
|---|---|---|---|
| **evidence** | 4 | 2 | 0 |
| **experience** | 1 | 2 | 4 |
| **assertion** | 0 | 1 | 21 |

All three seeds pooled (105 test posts):

| true \ predicted | evidence | experience | assertion |
|---|---|---|---|
| **evidence** | 12 | 2 | 4 |
| **experience** | 1 | 6 | 14 |
| **assertion** | 0 | 6 | 60 |

The biggest off-diagonal number is now a real boundary, and the one the
diagnosis named. 14 of the 21 real `experience` posts were called `assertion`,
and 6 `assertion` posts went the other way. `evidence` is mostly learned:
12 of 18, and no `assertion` post was ever called `evidence`.

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

**Yes. It fixed the failure it was aimed at, and two criteria flipped from
MISSED to MET (3 and 5).** I know because only `EPOCHS` changed, and both run
logs use the same three seeds and the same test posts, so the differences in
the tables above can only come from training length. Mean macro F1 went from
0.257 to 0.652, and the model now predicts all three labels on every seed.

**It didn't fix everything, and it exposed something.** Criteria 1 and 2 are
still missed, and both misses now trace to one label pair, `experience` vs
`assertion`. The before run's zero spread is gone too. Accuracy now moves
0.200 across seeds (0.629 to 0.829), and the notebook flags that as "too small
or too lopsided for a stable measure". That's the real noise of a 35-post test
split with 7 `experience` posts in it: one post is 14 points of `experience`
recall. The untrained baseline moved 0.245 in macro F1 across the same three
splits, so this spread belongs to the test set, not the model.

**Diagnosis of the misses that remain**, using the same four causes:

- **2 (`experience` under 0.50 on every seed).** The cause is **a genuinely
  hard label pair**, `experience` vs `assertion`, plus **few examples** of the
  minority side. The evidence:
  - The pooled matrix puts 14 of 21 `experience` errors in `assertion`, with 6
    going the other way. That's confusion in both directions within one pair,
    the signature of a hard boundary rather than a missing label.
  - It isn't data size alone. `evidence`, with fewer training posts (28 against
    31), reaches F1 0.67–0.91, because it has surface cues (links, numbers,
    version strings). `experience` and `assertion` are both first-person and
    differ only in whether a specific thing the writer did is described
    (Rule 2).
  - The agreement report's one pile-(a) slip was on this same writer-versus-claim
    boundary, so some of the noise may be in my labels. But that slip touches
    my 20 hand-labelled rows at most. The review agent behind the other 211
    matched staff 30 out of 30, which points at the pair being hard rather
    than the labels being inconsistent.
  - The per-label error write-up (stretch, below) reads the actual misclassified
    posts.
- **1 (accuracy on seed 7).** It's the same pair, and the noise level. Seed 7's
  model swapped 5 `experience` posts into `assertion` and 5 `assertion` posts
  into `experience`, which netted its accuracy to exactly the share. To clear
  both conditions it needed 26 of 35 right (0.743), four more than it got. A
  0.20 spread across seeds says a single 35-post split can't settle a 0.10
  margin.

---

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
