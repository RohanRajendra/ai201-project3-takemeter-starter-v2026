#!/usr/bin/env python3
"""
Re-label the `cold` rows of labels.csv by hand, blind.

    python label_cold.py

Shows each row whose note starts with "cold" one at a time, WITHOUT its current
label, and asks for yours. Keys:

    e = evidence    x = experience    a = assertion    s = set aside (no claim)
    r = re-read the rules    q = quit (progress is saved; run again to resume)

When every row is done it writes your labels into labels.csv (the note stays
`cold; hn:<id>`), moves any you set aside into data/set_aside.csv, and prints
how many of yours differ from the labels that were there before.
"""

import csv
import json
import sys
import textwrap
from pathlib import Path

import pandas as pd

PROGRESS = Path(".cold_progress.json")
KEYS = {"e": "evidence", "x": "experience", "a": "assertion", "s": "SET_ASIDE"}

RULES = """
What does the comment rest its point on?

  evidence    something a reader can check without trusting the writer:
              a link, a named source, a quote, an identifier (version, CVE,
              model or bill number), a date, or a number about the world.
              A fact about a named thing with none of those is NOT evidence.
  experience  something specific the writer built, used, ran or saw
              (where, or how often). Credentials or "in my experience" alone
              don't count.
  assertion   a claim, judgment or suggestion with neither.

  Rule 1  who does the reader have to trust? Own-system numbers = experience.
          A link, even to your own repo, = evidence.
  Order   evidence > experience > assertion.
  Rule 3  the support has to support the point.
  Scope   no claim at all (pure question, thanks, banter, not English) = s.
"""


def main():
    df = pd.read_csv("labels.csv")
    cold = df.index[df["note"].astype(str).str.startswith("cold")].tolist()
    done = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}

    print(RULES)
    for n, i in enumerate(cold, 1):
        if str(i) in done:
            continue
        print("=" * 72)
        print(f"{n} of {len(cold)}\n")
        for para in str(df.at[i, "text"]).split("\n"):
            print(textwrap.fill(para, 72) if para.strip() else "")
        while True:
            key = input("\n[e/x/a/s, r=rules, q=quit] > ").strip().lower()
            if key == "q":
                PROGRESS.write_text(json.dumps(done))
                print(f"Saved {len(done)} of {len(cold)}. Run again to resume.")
                return
            if key == "r":
                print(RULES)
                continue
            if key in KEYS:
                done[str(i)] = KEYS[key]
                PROGRESS.write_text(json.dumps(done))
                break

    changed = sum(df.at[int(i), "label"] != label for i, label in done.items())
    aside = [int(i) for i, label in done.items() if label == "SET_ASIDE"]
    for i, label in done.items():
        if label != "SET_ASIDE":
            df.at[int(i), "label"] = label

    if aside:
        moved = pd.DataFrame({
            "hn_id": [df.at[i, "note"].split("hn:")[-1] for i in aside],
            "text": [df.at[i, "text"] for i in aside],
            "why": ["set aside in cold re-label"] * len(aside),
        })
        path = Path("data/set_aside.csv")
        existing = pd.read_csv(path) if path.exists() else pd.DataFrame()
        pd.concat([existing, moved]).to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL)
        df = df.drop(index=aside)

    df.to_csv("labels.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    PROGRESS.unlink(missing_ok=True)
    print(f"\nDone. {len(done)} cold rows labelled; {changed} differ from before; "
          f"{len(aside)} set aside.")
    print(df["label"].value_counts().to_string())


if __name__ == "__main__":
    sys.exit(main())
