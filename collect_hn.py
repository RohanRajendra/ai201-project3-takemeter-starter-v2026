#!/usr/bin/env python3
"""
Collect public Hacker News comments for TakeMeter.

Pulls comments from a random sample of well-discussed HN stories through the
public Algolia HN Search API (no account, no key), cleans the HTML into plain
text, and writes a candidate pool to data/hn_candidates.csv. Labels are added
separately in labels.csv — this script never labels anything.

    python collect_hn.py                       # default pool
    python collect_hn.py --stories 120 --per-story 4 --seed 7 --out data/hn_extra.csv

Whole comments are kept. Comments are filtered, never trimmed:
  - 12 to 200 words (very long comments get truncated by the model anyway)
  - no code blocks, not mostly quoted text, not deleted or flagged
  - at most --per-story comments from any one story, so no thread dominates
"""

import argparse
import csv
import html
import json
import random
import re
import time
import urllib.request
from pathlib import Path

API = "https://hn.algolia.com/api/v1"

# 2026-05-01 to 2026-10-15, UTC.
WINDOW_START = 1777593600
WINDOW_END = 1792022400


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "takemeter-class-project"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def clean(comment_html):
    """HN comment HTML -> plain text, paragraphs kept as blank lines."""
    text = comment_html.replace("<p>", "\n\n")
    text = re.sub(r'<a href="([^"]*)"[^>]*>.*?</a>', lambda m: html.unescape(m.group(1)), text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def keep(comment_html, text):
    if "<pre>" in comment_html:
        return False
    words = len(text.split())
    if not 12 <= words <= 200:
        return False
    lines = [line for line in text.splitlines() if line.strip()]
    quoted = sum(1 for line in lines if line.lstrip().startswith(">"))
    if lines and quoted / len(lines) > 0.5:
        return False
    if sum(1 for c in text if ord(c) > 127) / len(text) > 0.05:
        return False
    return True


def stories(n, seed):
    """A random sample of well-discussed stories from the window."""
    pool = []
    for page in range(10):
        url = (f"{API}/search?tags=story&hitsPerPage=100&page={page}"
               f"&numericFilters=points>150,num_comments>60,"
               f"created_at_i>{WINDOW_START},created_at_i<{WINDOW_END}")
        hits = get(url)["hits"]
        if not hits:
            break
        pool.extend(hits)
        time.sleep(0.2)
    random.Random(seed).shuffle(pool)
    return pool[:n]


def comments_for(story_id):
    url = f"{API}/search?tags=comment,story_{story_id}&hitsPerPage=200"
    return get(url)["hits"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stories", type=int, default=90)
    parser.add_argument("--per-story", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="data/hn_candidates.csv")
    parser.add_argument("--exclude", nargs="*", default=[],
                        help="CSV files whose hn_id values should be skipped")
    args = parser.parse_args()

    seen = set()
    for path in args.exclude:
        with open(path, newline="") as f:
            seen.update(row["hn_id"] for row in csv.DictReader(f))

    rng = random.Random(args.seed)
    rows = []
    for story in stories(args.stories, args.seed):
        picked = []
        hits = comments_for(story["objectID"])
        rng.shuffle(hits)
        for hit in hits:
            raw = hit.get("comment_text") or ""
            if not raw or hit["objectID"] in seen:
                continue
            text = clean(raw)
            if keep(raw, text):
                picked.append({
                    "hn_id": hit["objectID"],
                    "story_id": story["objectID"],
                    "story_title": story["title"],
                    "created_at": hit["created_at"],
                    "text": text,
                })
                seen.add(hit["objectID"])
            if len(picked) == args.per_story:
                break
        rows.extend(picked)
        time.sleep(0.2)

    rng.shuffle(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} comments from {len({r['story_id'] for r in rows})} stories to {args.out}")


if __name__ == "__main__":
    main()
