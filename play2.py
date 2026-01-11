import numpy as np
import pandas as pd
from datasets import load_dataset
import pickle
from typing import Dict
import os

def count_modified_lines(patch: str) -> Dict[str, int]:
    """
    Count modified lines in a git patch.

    Returns:
        {
            "added": int,
            "deleted": int,
            "replaced": int,
            "total_modified": int
        }

    Definitions:
    - added: number of '+' lines (excluding diff headers)
    - deleted: number of '-' lines (excluding diff headers)
    - replaced: number of line pairs where a '-' is followed by a '+'
    - total_modified: added + deleted
    """

    added = 0
    deleted = 0
    replaced = 0

    prev_was_delete = False

    for line in patch.splitlines():
        # Skip metadata
        if (
            line.startswith("+++")
            or line.startswith("---")
            or line.startswith("diff ")
            or line.startswith("index ")
            or line.startswith("@@")
        ):
            prev_was_delete = False
            continue

        if line.startswith("-"):
            deleted += 1
            prev_was_delete = True

        elif line.startswith("+"):
            added += 1
            if prev_was_delete:
                replaced += 1
                prev_was_delete = False

        else:
            prev_was_delete = False

    return {
        "added": added,
        "deleted": deleted,
        "replaced": replaced,
        "total_modified": added + deleted,
    }


path = "/Users/vkgainz/Vim/human-swe-bench/verified.pkl"
if os.path.exists(path):
    with open(path, "rb") as f:
        ds = pickle.load(f)
else:
    ds = load_dataset("princeton-nlp/SWE-bench_verified", split = "test") # Full dataset
    with open(path, 'wb') as f:
        pickle.dump(ds, f)

print(len(ds))
print(ds[0].keys())

for key in ds[0].keys():
     print(f"SHOWING {key}")
     print(ds[8][key])

all_lines_modified = {}
for i in range(len(ds)):
    lines_modified = count_modified_lines(ds[i]['patch'])
    all_lines_modified[i] = lines_modified['added']
difficulties = []
modified = []
for idx, lines in sorted(all_lines_modified.items(), key = lambda v: v[1])[:400]:
    difficulty = ds[idx]['difficulty']
    difficulties.append(difficulty)
    modified.append(lines)
print(sorted(all_lines_modified.items(), key = lambda v: v[1])[-80])
print(pd.Series(difficulties).value_counts())
print(pd.Series(modified).value_counts().sort_index())



