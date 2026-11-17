"""Builds the mock exam banks in /content/mocks.

Run from the project root:  python3 scripts/problems/build_mocks.py
"""
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "content", "mocks")

import mock_amc12  # noqa: E402,F401
import mock_core_a  # noqa: E402,F401
import mock_core_b  # noqa: E402,F401
from mock_common import FAMILIES, build_family  # noqa: E402


def main():
    os.makedirs(OUT, exist_ok=True)
    ids = Counter(f["id"] for f in FAMILIES)
    dup = [k for k, v in ids.items() if v > 1]
    assert not dup, f"duplicate family ids: {dup}"

    out = {"both": [], "amc12": []}
    per_level = defaultdict(Counter)
    errors = []
    for fam in FAMILIES:
        try:
            items = build_family(fam)
        except Exception as e:  # report every broken family at once
            errors.append(f"{fam['id']}: {type(e).__name__}: {e}")
            continue
        out[fam["track"]].extend(items)
        per_level[(fam["track"], fam["level"])][fam["topic"]] += 1
    if errors:
        print("\n".join(errors))
        sys.exit(1)

    for track, items in out.items():
        with open(os.path.join(OUT, f"{'shared' if track == 'both' else 'amc12'}.json"), "w") as f:
            json.dump(items, f, indent=1, ensure_ascii=False)
            f.write("\n")
    for (track, level), c in sorted(per_level.items()):
        print(f"{track:6} level {level}: {sum(c.values())} families  {dict(c)}")
    print(f"total {sum(len(v) for v in out.values())} mock problems in {len(FAMILIES)} families")


if __name__ == "__main__":
    main()
