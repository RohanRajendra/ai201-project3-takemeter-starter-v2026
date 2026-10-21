# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

**Where the numbers come from.** Criteria 1–3 are measured on the held-out test
split, on each of the three unit-6 seeds (42, 7, 2024), using the entries in
`results_three_seeds_before.json` that section 6 of the notebook writes. Each
is **MET only if it holds on all three seeds.** Criteria 4 and 5 are single
measurements, and each names its own file.

---

## 1. Overall accuracy clearly beats always guessing `assertion`

On every one of seeds 42, 7 and 2024, overall accuracy on the held-out test
split is **at least 0.65** AND **at least 0.10 above** that seed's
always-`assertion` score. Measured in each entry of
`results_three_seeds_before.json`: `accuracy` is at least 0.65, and `accuracy`
minus `per_label.assertion.support / n_test` is at least 0.10 (that difference
rounded to two decimals, so exactly three posts out of 30 counts). MET only if
both hold on all three seeds.

**Why this target:** My 55% `assertion` share comes from only 33 claim-making
posts, so the real always-`assertion` score on a given split could land well
above or below 0.57, and a fixed 0.65 alone could end up no better than that
guesser. The +0.10 is three posts out of 30 beyond the guesser on that same
split, so the model has to pick out some `evidence` or `experience` posts
(criterion 2 checks `experience` on its own), and the 0.65 floor still asks
for 20 of 30 if a split is light on `assertion`. I didn't go higher because
each post is worth 3.3 points and the worst seed counts.

<!-- Context:
     - The fair floor here is not 33%. In the 40 posts I read, `assertion` was
       18 of the 33 that made a claim (about 55%), so a model that always says
       `assertion` would already score about 0.55.
     - The test split is about 30 posts (15% of 200), so each post is worth
       about 3.3 accuracy points.
-->

---

## 2. No label is left behind

Every label (`evidence`, `experience`, `assertion`) has an F1 of **at least
0.50** on the held-out test split, on every one of seeds 42, 7 and 2024
(`per_label.<label>.f1` in each entry of `results_three_seeds_before.json`).

**Why this target:** Always guessing `assertion` scores 0 F1 on `evidence`
and `experience`, so a floor on every label is what shows the model finds the
minority labels at all. I kept one floor rather than loosening it for
`evidence`: with only about 5 test posts it's the jumpiest label, but URLs and
version and CVE numbers give it surface cues, while `experience` has nothing
but "I" to separate it from `assertion`. 0.50 still means catching 2 or 3 of
the 5 `evidence` posts without many false alarms on the worst seed.

<!-- Context:
     - Expected shares from the reading tally: evidence about 18%, experience
       about 27%, assertion about 55%. With 200 rows that's roughly 36 / 54 / 110,
       and in a 30-post test split roughly 5 / 8 / 17.
     - `evidence` is likely to have fewer than 8 test posts, so its F1 moves in
       big steps between seeds. One miss out of 5 costs a lot.
     - `evidence` has strong surface cues (URLs, version and CVE numbers,
       digits), so it may be easier than its size suggests. `experience` vs
       `assertion` has no surface cue beyond "I", which is arguably the harder
       pair.
     - A single floor for all three is simplest to check. If you'd rather set a
       looser floor for the thinnest label, name it and the number here.
-->

---

## 3. Confident guesses are right more often

On every one of seeds 42, 7 and 2024, the model's most-confident third of test
predictions is more accurate than its least-confident third by **at least 20
percentage points**. Measured as `confidence.accuracy_most_confident_third`
minus `confidence.accuracy_least_confident_third` in each entry of
`results_three_seeds_before.json`; both are fractions, so 10 points = 0.10.

**Why this target:** Each third is about 10 posts, so a 10-point gap is a
single post and could just be noise. 20 points means at least two more right
out of ten. If confidence tracks my labels, comments with a link or CVE number
should sit in the confident third and the `experience`/`assertion` boundary
posts in the unsure third, and a gap that size should show up even on the
worst seed.

<!-- Context:
     - Each third is about 10 posts, so the difference moves in steps of about
       10 points. A target like 5 points is effectively "at least one more
       right in the confident third".
     - Why it matters for this taxonomy: a comment with a URL or a CVE number
       should be an easy, confident `evidence` call. The unsure ones should be
       the experience/assertion boundary. If confidence doesn't separate them,
       the confidence score is useless for triaging comments.
-->

---

## 4. My labels agree with someone else's

When I label the 30 staff posts (`data/staff_posts.csv`) under the staff
taxonomy, my labels match the staff labels on **at least 23 of 30** posts.
Measured in `agreement_results.json`, written by `python agreement.py`: `agreed`
is at least 23 AND `compared` is 30. A staff post whose text didn't match drops
out of `compared`, so it counts against this criterion; `agreement_rate` on its
own is not the pass condition.

**Why this target:** Staff say a rate in the 70s is normal for these 30, so I'm
aiming at the upper half of that range (23 = 77%, seven disagreements) rather
than above it. Their `analysis` rule makes a similar cut to my Rule 1 and
pointer rule but a stricter one: the fact has to carry the argument, so a
related number used as a flourish ("times are down 3% since 2017") would be
`evidence` under my rules but is a staff `hot_take`, and after 200 HN labels my
habit will push the wrong way there. `reaction` vs `hot_take` has no
counterpart in my taxonomy either, so I'll be applying that boundary cold.

<!-- Context:
     - This is the brief's "consistency" area, and the only check where someone
       other than me labelled the same posts.
     - It's measured under the STAFF taxonomy (analysis / hot_take / reaction,
       on a fictional running forum), not mine. The staff analysis/hot_take
       rule makes a similar but stricter cut than my pointer rule: the fact
       has to be load-bearing, not just present. So it tests whether I can
       apply a written rule the way its author meant it.
     - Staff say several of the 30 were chosen to be genuinely ambiguous, so
       30/30 isn't the expectation.
-->

---

## 5. Fine-tuning beats the zero-shot baseline

The trained model's macro F1 on `test_split.csv` beats the zero-shot
baseline's macro F1 on the same posts by **at least 0.15** (on macro F1's 0–1
scale, i.e. 15 percentage points). Baseline: `scores.f1_macro` in
`baseline_results.json`, from `python baseline.py` with `label_definitions.txt`
in place. Trained: `f1_macro` in `results.json`.

Same-posts check: `baseline.py` is run with no `--n` cap, and in
`baseline_results.json`, `held_out` is true and `n` equals `n_test` in
`results.json`. If any of these doesn't hold, the baseline was scored on
different posts, and the criterion can't be called MET.

**Why this target:** Macro F1 weights the roughly 5 `evidence` test posts as
heavily as the roughly 17 `assertion` ones, so one or two `evidence` posts
flipping can move it 0.05 to 0.10 on their own. 0.15 asks for a gain bigger than
that, and it should come from rules that aren't in the one-line definitions:
a link to your own repo is `evidence`, credentials alone are `assertion`, and a
fact with no pointer isn't `evidence`.

<!-- Context:
     - The baseline is a general zero-shot model reading only my one-line
       definitions. My labels hinge on rules that aren't in a one-liner, such as
       "a link to your own repo counts as evidence" and "credentials alone are
       assertion". Fine-tuning on 140 examples is the only way the model sees
       those rules applied.
     - This is a single comparison on the seed-42 split (results.json and
       test_split.csv come from the same run), not three seeds.
     - If the trained model can't beat a model that never saw my data, the 200
       labels taught it nothing the definitions didn't already say.
-->

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
