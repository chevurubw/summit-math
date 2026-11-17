"""Shared pieces for the mock exam banks.

Mock problems are grouped into families. A family is one problem idea; its
variants change the numbers and the setting. The site never puts a family from
a student's previous mock on their next mock, so each new mock is a genuinely
different test, not the old one with new numbers.

Difficulty levels follow the AoPS competition ratings:
  1  AMC 10 problems 1 to 5          (AMC 12 does not use this level)
  2  AMC 10 6 to 10,  AMC 12 1 to 5
  3  AMC 10 11 to 15, AMC 12 6 to 10
  4  AMC 10 16 to 20, AMC 12 11 to 15
  5  AMC 10 16 to 20, AMC 12 11 to 15   (solid single idea problems)
  6  AMC 10 19 to 22, AMC 12 16 to 20
  7  AMC 10 22 to 25, AMC 12 21 to 25   (two or three ideas chained; see mock_hard.py)

Levels 1 to 4 describe the problems' own difficulty; the exact positions they land
in are set by mockSections in src/lib/mockSelect.ts.
"""
import hashlib
import math
import random
from fractions import Fraction as F

from common import C, explain, make_choices, num, simplify_sqrt, tex_num, var  # noqa: F401

FAMILIES = []


def family(fid, level, topic, skill, track="both"):
    """Registers a problem family. topic is a unit id; skill is the closest course skill."""
    def deco(fn):
        FAMILIES.append({"id": fid, "level": level, "topic": topic, "skill": skill, "track": track, "fn": fn})
        return fn
    return deco


def surd(k, rad=1):
    """k * sqrt(rad) as a choice, simplified. k may be a Fraction."""
    k = F(k)
    if rad == 0 or k == 0:
        return num(0)
    a, r2 = simplify_sqrt(rad)
    k *= a
    val = float(k) * math.sqrt(r2)
    if r2 == 1:
        return num(k)
    sign = "-" if k < 0 else ""
    k = abs(k)
    top = ("" if k.numerator == 1 else str(k.numerator)) + f"\\sqrt{{{r2}}}"
    t = top if k.denominator == 1 else f"\\frac{{{top}}}{{{k.denominator}}}"
    return C(sign + t, val)


def pi_mult(k):
    """k * pi as a choice."""
    k = F(k)
    if k == 0:
        return num(0)
    if k.denominator == 1:
        t = ("" if k == 1 else str(k.numerator)) + "\\pi"
    else:
        t = f"\\frac{{{'' if k.numerator == 1 else k.numerator}\\pi}}{{{k.denominator}}}"
    return C(t, float(k) * math.pi)


def polystr(coeffs, var="x"):
    """Polynomial from coefficients, highest degree first."""
    n = len(coeffs) - 1
    out = ""
    for i, c in enumerate(coeffs):
        e = n - i
        if c == 0:
            continue
        ac = abs(c)
        term = ("" if ac == 1 and e > 0 else tex_num(F(ac))) + (var if e >= 1 else "") + (f"^{{{e}}}" if e > 1 else "")
        if not out:
            out = ("-" if c < 0 else "") + term
        else:
            out += (" - " if c < 0 else " + ") + term
    return out or "0"


def signed(c):
    """' + 3' or ' - 3' for writing a constant after another term."""
    return f" - {tex_num(F(-c))}" if c < 0 else f" + {tex_num(F(c))}"


PLACES = ["a school fair", "a bake sale", "a hardware store", "a farmers market", "a museum gift shop", "a bookstore"]


def build_family(fam, variants=6):
    """Makes up to `variants` different versions of one family."""
    seed = int(hashlib.md5(fam["id"].encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    seen, items, tries = set(), [], 0
    while len(items) < variants and tries < 400:
        tries += 1
        out = fam["fn"](rng)
        if out is None:
            continue
        prompt, answer, wrong, hints, solution = out[:5]
        sort = out[5] if len(out) > 5 else True
        if prompt in seen:
            continue
        seen.add(prompt)
        choices, letter = make_choices(answer, wrong, rng, sort)
        items.append({
            "id": f"mock_{fam['id']}_{len(items) + 1}",
            "family": fam["id"],
            "difficulty": fam["level"],
            "topic": fam["topic"],
            "skillId": fam["skill"],
            "track": fam["track"],
            "prompt": prompt,
            "choices": choices,
            "answer": letter,
            "hints": hints,
            "solution": solution.replace("ANSWER", f"**({letter})**"),
        })
    if len(items) < 3:
        raise RuntimeError(f"family {fam['id']} made only {len(items)} versions")
    return items
