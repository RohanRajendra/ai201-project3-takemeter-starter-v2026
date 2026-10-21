#!/usr/bin/env python3
"""
The three stretch runs, using the notebook's own code.

    python stretch_runs.py epochs      # stretch 1: EPOCHS 3 -> 10, same data and split
    python stretch_runs.py extra       # stretch 3: + 50 extra `evidence` rows, train split only
    python stretch_runs.py question    # stretch 2: + the fourth label, `question`
    python stretch_runs.py compare     # print the README tables from the saved results

The split, training and evaluation functions are read straight out of
takemeter.ipynb (sections 3-5) and executed unchanged, so a stretch run differs
from the core run only in what this file passes them. labels.csv, results.json
and test_split.csv are never written; each run writes its own
results_stretch_<name>.json.

Every run starts from the same seed-42 split of labels.csv that produced
results.json, so the 35 core test posts are identical across runs:

  epochs    the core split as-is, EPOCHS=10.
  extra     the core split, plus the `extra_evidence` rows of labels_stretch.csv
            added to the TRAIN split only. EPOCHS=10, so it compares against
            `epochs`, not against run 1.
  question  the core split, plus the `question` rows of labels_stretch.csv split
            70/15/15 on their own (same seed) and appended to each split, so the
            test set is the same 35 core posts plus the held-out questions.
            EPOCHS=10.
"""

import ast
import json
import sys
from pathlib import Path

import pandas as pd

NOTEBOOK = "takemeter.ipynb"
CORE_LABELS = ["evidence", "experience", "assertion"]
SEED = 42
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
MAX_LENGTH = 128
BASE_MODEL = "distilbert-base-uncased"
STRETCH_EPOCHS = 10


def notebook_functions():
    """Imports and function definitions from the notebook's sections 3-5, nothing else."""
    cells = json.loads(Path(NOTEBOOK).read_text())["cells"]
    wanted = ("def split_dataset", "def train_model", "def evaluate")
    namespace = {"MAX_LENGTH": MAX_LENGTH}
    for cell in cells:
        source = "".join(cell["source"])
        if cell["cell_type"] != "code" or not any(w in source for w in wanted):
            continue
        tree = ast.parse(source)
        tree.body = [node for node in tree.body
                     if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
        exec(compile(tree, NOTEBOOK, "exec"), namespace)
    return namespace


def device():
    import torch
    if torch.cuda.is_available():
        return "cuda", torch.cuda.get_device_name(0), torch.__version__
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps", "Apple Silicon GPU (MPS)", torch.__version__
    return "cpu", "CPU", torch.__version__


def stretch_rows(name):
    df = pd.read_csv("labels_stretch.csv")
    return df[df["stretch"] == name][["text", "label", "note"]].reset_index(drop=True)


def run(name):
    nb = notebook_functions()
    core = pd.read_csv("labels.csv")
    train, val, test = nb["split_dataset"](core, SEED)
    labels = list(CORE_LABELS)

    if name == "extra":
        extra = stretch_rows("extra_evidence")
        overlap = set(extra["text"]) & set(core["text"])
        assert not overlap, f"{len(overlap)} extra rows duplicate labels.csv"
        train = pd.concat([train, extra], ignore_index=True)
    elif name == "question":
        questions = stretch_rows("question")
        assert not set(questions["text"]) & set(core["text"])
        q_train, q_val, q_test = nb["split_dataset"](questions, SEED)
        train = pd.concat([train, q_train], ignore_index=True)
        val = pd.concat([val, q_val], ignore_index=True)
        test = pd.concat([test, q_test], ignore_index=True)
        labels.append("question")
    elif name != "epochs":
        sys.exit(f"unknown run: {name}")

    sizes = {split: frame["label"].value_counts().reindex(labels).fillna(0).astype(int).to_dict()
             for split, frame in (("train", train), ("val", val), ("test", test))}
    print(json.dumps(sizes, indent=2))

    trainer, tokenizer = nb["train_model"](
        train, val, labels, SEED, STRETCH_EPOCHS, LEARNING_RATE, BATCH_SIZE, BASE_MODEL, quiet=True
    )
    results = nb["evaluate"](trainer, tokenizer, test, labels, seed=SEED)

    # The same numbers restricted to the 35 core test posts, so every run can be
    # compared on identical posts even when the test split has grown.
    if name == "question":
        core_test = nb["split_dataset"](core, SEED)[2]
        results["core_test_only"] = nb["evaluate"](trainer, tokenizer, core_test, labels, seed=SEED)

    dev, dev_name, torch_version = device()
    results.update({
        "run": name, "epochs": STRETCH_EPOCHS, "learning_rate": LEARNING_RATE,
        "batch_size": BATCH_SIZE, "max_length": MAX_LENGTH, "base_model": BASE_MODEL,
        "split_sizes": sizes, "device": dev, "device_name": dev_name,
        "torch_version": torch_version,
    })
    out = f"results_stretch_{name}.json"
    Path(out).write_text(json.dumps(results, indent=2))
    print(f"\naccuracy {results['accuracy']:.3f}   macro F1 {results['f1_macro']:.3f}")
    for label, scores in results["per_label"].items():
        print(f"  {label:<11} P {scores['precision']:.3f}  R {scores['recall']:.3f}  "
              f"F1 {scores['f1']:.3f}  (n={scores['support']})")
    c = results["confidence"]
    print(f"confidence gap {c['accuracy_most_confident_third'] - c['accuracy_least_confident_third']:+.3f}")
    print(f"Wrote {out}")


def compare():
    def load(path):
        return json.loads(Path(path).read_text()) if Path(path).exists() else None

    runs = [("Run 1: core, 3 epochs", load("results.json")),
            ("Run 2: 10 epochs", load("results_stretch_epochs.json")),
            ("Run 3: + 50 evidence", load("results_stretch_extra.json")),
            ("Run 4: + `question` (core 35 posts)",
             (load("results_stretch_question.json") or {}).get("core_test_only"))]
    runs = [(n, r) for n, r in runs if r]

    def gap(r):
        c = r["confidence"]
        return c["accuracy_most_confident_third"] - c["accuracy_least_confident_third"]

    # Macro F1 over the three core labels, so run 4 (whose model can also say
    # `question`) is averaged over the same labels as the others.
    def core_macro(r):
        return sum(r["per_label"][l]["f1"] for l in CORE_LABELS) / len(CORE_LABELS)

    rows = [("Accuracy", lambda r: r["accuracy"]), ("Macro F1 (3 core labels)", core_macro)]
    for label in CORE_LABELS:
        for metric in ("precision", "recall", "f1"):
            rows.append((f"{metric.capitalize() if metric != 'f1' else 'F1'} — `{label}`",
                         lambda r, l=label, m=metric: r["per_label"][l][m]))
    rows.append(("Confidence gap (most − least sure third)", gap))

    print("| Measure | " + " | ".join(n for n, _ in runs) + " |")
    print("|---|" + "---|" * len(runs))
    for name, get in rows:
        print(f"| {name} | " + " | ".join(f"{get(r):.3f}" for _, r in runs) + " |")

    q = load("results_stretch_question.json")
    if q:
        print("\nFour-label run, full test split (35 core posts + held-out questions):\n")
        print("| Label | Precision | Recall | F1 | Test n |")
        print("|---|---|---|---|---|")
        for label, s in q["per_label"].items():
            print(f"| `{label}` | {s['precision']:.3f} | {s['recall']:.3f} | {s['f1']:.3f} | {s['support']} |")
        print(f"| **All** | | | macro {q['f1_macro']:.3f} | {q['n_test']} (accuracy {q['accuracy']:.3f}) |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    compare() if sys.argv[1] == "compare" else run(sys.argv[1])
