#!/usr/bin/env python3
"""
Review the pre-labelled `experience` candidates for the second improvement.

    python review_experience.py

Shows each post in data/improvement2_candidates.csv with the pre-label's
one-line reason. Keys:

    Enter or y = confirm `experience`
    a = it's `assertion`    e = it's `evidence`    s = set aside (no claim)
    ? = rules    q = quit (progress is saved; run again to resume)

Writes data/improvement2_review.csv (cand, verdict, label). Only confirmed
`experience` rows are added to labels.csv afterwards; overridden ones are
dropped, because this improvement adds examples of one label only.
"""

import csv
import json
import textwrap
from pathlib import Path

CANDIDATES = Path("data/improvement2_candidates.csv")
OUT = Path("data/improvement2_review.csv")
PROGRESS = Path(".experience_progress.json")
OVERRIDE = {"a": "assertion", "e": "evidence", "s": "SET_ASIDE"}

RULES = """
`experience`: backs its point with the writer's own first-hand experience,
something specific they built, used, ran or saw happen.

  Rule 2   a specific thing must be described: what they did, used or saw, and
           where or how often. A summary of repeated first-hand events counts.
           "In my experience", "I've always found" or credentials alone are
           `assertion`.
  Rule 1   numbers from the writer's own system or life are `experience`. A
           link or a public pointer that supports the point makes it
           `evidence` (evidence > experience > assertion).
  Rule 3   the experience has to back the point. A personal aside that
           doesn't support the claim isn't enough.
"""


def main():
    with open(CANDIDATES, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    done = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}

    print(RULES)
    for n, row in enumerate(rows, 1):
        if row["cand"] in done:
            continue
        print("\n" + "=" * 72)
        print(f"{n} of {len(rows)}   ({row['cand']}, HN {row['hn_id']})\n")
        for para in row["text"].split("\n"):
            print(textwrap.fill(para, 72) if para.strip() else "")
        print(f"\n  pre-label: experience, because {row['my_reason']}")
        while True:
            key = input("\n[Enter/y=experience  a=assertion  e=evidence  s=set aside  ?=rules  q=quit] > ").strip().lower()
            if key == "q":
                PROGRESS.write_text(json.dumps(done))
                print(f"Saved {len(done)} of {len(rows)}. Run again to resume.")
                return
            if key == "?":
                print(RULES)
                continue
            if key in ("", "y"):
                done[row["cand"]] = ["CONFIRM", "experience"]
                break
            if key in OVERRIDE:
                done[row["cand"]] = ["OVERRIDE", OVERRIDE[key]]
                break
        PROGRESS.write_text(json.dumps(done))

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cand", "verdict", "label"])
        for row in rows:
            writer.writerow([row["cand"], *done[row["cand"]]])
    PROGRESS.unlink(missing_ok=True)
    confirmed = sum(v[0] == "CONFIRM" for v in done.values())
    print(f"\nDone. {confirmed} of {len(rows)} confirmed as experience. Wrote {OUT}.")


if __name__ == "__main__":
    main()
