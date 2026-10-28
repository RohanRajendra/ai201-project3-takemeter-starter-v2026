#!/usr/bin/env python3
"""
Label the 30 staff posts by hand, blind, under the STAFF taxonomy.

    python label_staff.py

Prints the definitions and decision rules from data/staff_taxonomy.md exactly
as staff wrote them, then shows each post in data/staff_posts.csv one at a time
and asks for your label. Keys:

    a = analysis    h = hot_take    r = reaction
    ? = re-read the rules    q = quit (progress is saved; run again to resume)

When all 30 are done it writes my_staff_labels.csv (text, label), with each
post's text copied exactly so agreement.py can match it. It never opens
data/staff_labels.csv; get that from your TF only after this file exists.
"""

import csv
import json
import textwrap
from pathlib import Path

PROGRESS = Path(".staff_progress.json")
OUT = Path("my_staff_labels.csv")
KEYS = {"a": "analysis", "h": "hot_take", "r": "reaction"}


def rules():
    """The 'three labels' and 'decision rules' sections of the staff taxonomy, verbatim."""
    text = Path("data/staff_taxonomy.md").read_text(encoding="utf-8")
    start = text.index("## The three labels")
    end = text.index("## What to produce")
    return text[start:end].strip()


def main():
    with open("data/staff_posts.csv", newline="", encoding="utf-8") as f:
        posts = list(csv.DictReader(f))
    done = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}

    print(rules())
    for n, post in enumerate(posts, 1):
        if post["id"] in done:
            continue
        print("\n" + "=" * 72)
        print(f"{n} of {len(posts)}   ({post['id']})\n")
        for para in post["text"].split("\n"):
            print(textwrap.fill(para, 72) if para.strip() else "")
        while True:
            key = input("\n[a=analysis  h=hot_take  r=reaction  ?=rules  q=quit] > ").strip().lower()
            if key == "q":
                PROGRESS.write_text(json.dumps(done))
                print(f"Saved {len(done)} of {len(posts)}. Run again to resume.")
                return
            if key == "?":
                print("\n" + rules())
                continue
            if key in KEYS:
                done[post["id"]] = KEYS[key]
                PROGRESS.write_text(json.dumps(done))
                break

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        for post in posts:
            writer.writerow([post["text"], done[post["id"]]])
    PROGRESS.unlink(missing_ok=True)
    counts = {label: list(done.values()).count(label) for label in KEYS.values()}
    print(f"\nDone. Wrote {OUT} with {len(posts)} labels: {counts}")
    print("Now ask your TF for data/staff_labels.csv and put it in data/.")


if __name__ == "__main__":
    main()
