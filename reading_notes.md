# Reading notes — Milestone 1

## The community

**Hacker News comments** (news.ycombinator.com). Public, no login needed to read,
and not built around a single show or release. Every thread is a different
story (security bugs, AI model launches, Show HN projects, policy, history), so
the comments vary a lot in quality: some are a sourced paragraph, some are one
line of snark.

Posts were pulled with `collect_hn.py` through the public Algolia HN Search API
(no account, no key). It takes a random sample of 90 well-discussed stories
posted between 2026-05-01 and 2026-10-15 (150+ points, 60+ comments), and at
most 5 comments from each, so no single thread dominates. Comments are kept
whole. Comments under 12 or over 200 words, code-block comments, and
mostly-quoted replies are skipped. The pool is in `data/hn_candidates.csv` (450
comments). I read the first 40 before deciding anything.

## What I saw in 40 posts

Rough tally from the 40, by what the comment rests its point on:

| What the comment does | Count of 40 | Rows in `data/hn_candidates.csv` |
|---|---|---|
| Points at something the reader could check: a link, a CVE, a version number, a quote | 6 | 2, 5, 8, 13, 16, 34 |
| Rests on the writer's own first-hand experience ("I worked on…", "I tried it…") | 9 | 3, 12, 15, 17, 19, 20, 27, 32, 36 |
| Makes a claim with no support: opinion, speculation, advice, sarcasm | 18 | 0, 4, 6, 7, 11, 14, 18, 21, 22, 24, 25, 26, 30, 31, 33, 37, 38, 39 |
| Makes no claim at all, just asks for information | 6 | 1, 9, 10, 28, 29, 35 |
| Banter with no point (a username story) | 1 | 23 |

## Candidate distinctions (things I can point at, not "good vs bad")

1. **Some comments name something a reader could go and check; most don't.**
   Row 2 lists three CVE numbers. Row 16 gives a Firefox version and a support
   link. Row 13 quotes the DuckDB announcement word for word. Row 6 just says
   non-programmers "will likely make more mistakes than an LLM will", with
   nothing behind it.

2. **Some comments argue from "this happened to me"; others argue about the
   world in general.** Row 3 ("I worked on a system… tokenization was still
   >10% of total runtime") and row 19 ("I tried it for family location
   sharing… the UI felt clunky") rest on the writer's own experience. Row 25
   ("People trust software too much these days") is a general claim with no
   one's experience behind it.

3. **Length is not support.** Row 18 is the longest post in the 40, three
   paragraphs on why a model feels worse, and it never cites anything or
   describes anything the writer saw. Row 11 is three short sentences and makes
   the same kind of unsupported claim. A label that tracks effort or length
   would put these two far apart; a label that tracks support puts them
   together.

4. **About one comment in seven makes no claim at all, it only asks.** Rows 28,
   29 and 35 ask for information the writer doesn't have. This is a lot of the
   community. A taxonomy about how a take is supported has nowhere to put these.
   Rhetorical questions that are really claims ("is the solution really to keep
   swabbing until negative?", row 22) are a separate problem.

## Where this is heading

Distinctions 1 and 2 give two kinds of support (checkable vs first-hand) and
distinction 3 gives the third label (none). Distinction 4 is the thing a
three-label taxonomy won't cover. I'm noting it here so the stretch fourth label
comes from the reading, not from after-the-fact tidying.
