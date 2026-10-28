#!/usr/bin/env python3
"""
Per-post predictions for the improved model, for the error write-up.

    python error_analysis.py

Re-runs the unit 6 improvement (EPOCHS = 10, every other setting unchanged) on
the same three seeds as notebook section 6, using the notebook's own split,
train and evaluate functions (read out of takemeter.ipynb by stretch_runs.py).
For each seed it checks the run reproduces results_three_seeds_after.json, then
records every test post: true label, predicted label, the model's confidence
and which confidence third it fell in (the same thirds results.json reports).

Writes error_analysis.json. Never touches labels.csv or any results file.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

import stretch_runs as s

SEEDS = [42, 7, 2024]
EPOCHS = 10


def predictions(nb, trainer, tokenizer, test, labels):
    """Predicted label, confidence and confidence third for every test post."""
    from datasets import Dataset

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length",
                         max_length=s.MAX_LENGTH)

    ds = Dataset.from_pandas(nb["to_ids"](test, labels)).map(tokenize, batched=True)
    scores = trainer.predict(ds).predictions
    exp = np.exp(scores - scores.max(axis=-1, keepdims=True))
    probs = exp / exp.sum(axis=-1, keepdims=True)
    predicted = probs.argmax(axis=-1)
    confidence = probs.max(axis=-1)

    # Same thirds as the notebook's confidence_report: rank by confidence.
    ranked = np.argsort(confidence)
    third = max(1, len(confidence) // 3)
    where = np.full(len(confidence), "middle", dtype=object)
    where[ranked[:third]] = "least_sure"
    where[ranked[-third:]] = "most_sure"

    return [
        {
            "text": text,
            "true": true,
            "predicted": labels[int(p)],
            "confidence": round(float(c), 4),
            "third": str(w),
            "probabilities": {l: round(float(x), 4) for l, x in zip(labels, row)},
        }
        for text, true, p, c, w, row in zip(test["text"], test["label"], predicted,
                                            confidence, where, probs)
    ]


def main():
    nb = s.notebook_functions()
    core = pd.read_csv("labels.csv")
    labels = s.CORE_LABELS
    reference = {r["seed"]: r for r in json.loads(Path("results_three_seeds_after.json").read_text())}

    out = []
    for seed in SEEDS:
        train, val, test = nb["split_dataset"](core, seed)
        trainer, tokenizer = nb["train_model"](train, val, labels, seed, EPOCHS,
                                               s.LEARNING_RATE, s.BATCH_SIZE, s.BASE_MODEL,
                                               quiet=True)
        result = nb["evaluate"](trainer, tokenizer, test, labels, seed=seed)
        ref = reference[seed]
        same = (round(result["accuracy"], 6) == round(ref["accuracy"], 6)
                and result["confusion"] == ref["confusion"])
        print(f"seed {seed}: accuracy {result['accuracy']:.3f}  "
              f"reproduces results_three_seeds_after.json: {same}")
        out.append({"seed": seed, "reproduces_after_run": same,
                    "accuracy": result["accuracy"], "confusion": result["confusion"],
                    "posts": predictions(nb, trainer, tokenizer, test, labels)})

    Path("error_analysis.json").write_text(json.dumps(out, indent=2))
    print("Wrote error_analysis.json")


if __name__ == "__main__":
    main()
