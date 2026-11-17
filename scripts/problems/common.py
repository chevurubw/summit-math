import re
"""
Shared helpers for the problem generators.

Every problem is original: each template is a problem type found on the AMC 10/12,
written from scratch, with numbers and scenarios that change between versions.
Answers are computed in code (and checked by brute force where possible), so the
answer key cannot drift from the problem text.
"""
import json
import math
import random
from fractions import Fraction

LETTERS = ["A", "B", "C", "D", "E"]


# ---------- formatting ----------

def tex_num(v):
    """LaTeX for an int or Fraction."""
    if isinstance(v, Fraction):
        if v.denominator == 1:
            return str(v.numerator)
        sign = "-" if v < 0 else ""
        return f"{sign}\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"
    if isinstance(v, float):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:g}"
    return str(v)


class C:
    """A choice: what to show, plus a number used for sorting and uniqueness."""

    def __init__(self, tex, key):
        self.tex = tex
        self.key = float(key)


def num(v):
    return C(tex_num(v), float(v))


def sqrt_form(a, b):
    """a*sqrt(b) as a choice."""
    if b == 1:
        return C(str(a), a)
    coef = "" if a == 1 else str(a)
    return C(f"{coef}\\sqrt{{{b}}}", a * math.sqrt(b))


def simplify_sqrt(n):
    """n -> (a, b) with sqrt(n) = a*sqrt(b)."""
    a, b = 1, n
    f = 2
    while f * f <= b:
        while b % (f * f) == 0:
            a *= f
            b //= f * f
        f += 1
    return a, b


def money(v):
    return C(f"\\${v:,.2f}".replace(",", "{,}"), v)


def as_choice(v):
    return v if isinstance(v, C) else num(v)


def make_choices(answer, wrong, rng, sort=True):
    """Builds 5 unique choices. Numbers are listed in increasing order, like the real test."""
    answer = as_choice(answer)
    pool = []
    seen = {round(answer.key, 9)}
    for w in wrong:
        w = as_choice(w)
        k = round(w.key, 9)
        if k in seen:
            continue
        seen.add(k)
        pool.append(w)
    # Fill with nearby values if there were not enough distinct distractors
    step = 1
    while len(pool) < 4:
        base = int(round(answer.key))
        for cand in (base + step, base - step):
            if len(pool) >= 4:
                break
            k = round(float(cand), 9)
            if k in seen or (answer.key >= 0 and cand < 0):
                continue
            seen.add(k)
            pool.append(num(cand))
        step += 1
    chosen = pool[:4]
    allc = chosen + [answer]
    if sort:
        allc.sort(key=lambda c: c.key)
    else:
        rng.shuffle(allc)
    choices = {}
    ans_letter = None
    for L, c in zip(LETTERS, allc):
        choices[L] = f"${c.tex}$" if not c.tex.startswith("TEXT:") else c.tex[5:]
        if c is answer:
            ans_letter = L
    return choices, ans_letter


def text_choice(label, key):
    """A choice shown as plain text (no math)."""
    return C("TEXT:" + label, key)


# ---------- building problems ----------

class Bank:
    def __init__(self, skill_id, track="both"):
        self.skill_id = skill_id
        self.track = track
        self.items = {"basics": [], "challenge": []}
        self._prompts = set()

    def add(self, level, prompt, answer, wrong, hints, solution, rng, sort=True, family=None):
        if prompt in self._prompts:
            return False
        choices, letter = make_choices(answer, wrong, rng, sort)
        self._prompts.add(prompt)
        n = len(self.items[level]) + 1
        self.items[level].append(
            {
                "id": f"{self.skill_id}_{'b' if level == 'basics' else 'c'}{n:02d}",
                "skillId": self.skill_id,
                "family": family or f"{self.skill_id}:{level}",
                "level": level,
                "track": self.track,
                "prompt": prompt,
                "choices": choices,
                "answer": letter,
                "hints": hints,
                "solution": solution.replace("ANSWER", f"**({letter})**"),
            }
        )
        return True

    def fill(self, level, templates, target, seed):
        """Runs the templates in turn until the bank has `target` unique problems."""
        rng = random.Random(seed)
        tries = 0
        i = 0
        while len(self.items[level]) < target:
            t = templates[i % len(templates)]
            i += 1
            tries += 1
            if tries > target * 200:
                raise RuntimeError(f"{self.skill_id} {level}: could not make {target} unique problems")
            out = t(rng)
            if out is None:
                continue
            prompt, answer, wrong, hints, solution = out[:5]
            sort = out[5] if len(out) > 5 else True
            self.add(level, prompt, answer, wrong, hints, solution, rng, sort, f"{self.skill_id}:{t.__name__}")

    def fill_unique(self, level, templates, seed):
        """One problem per template, so every problem in the bank is a different type."""
        rng = random.Random(seed)
        for t in templates:
            for _ in range(400):
                out = t(rng)
                if out is None:
                    continue
                prompt, answer, wrong, hints, solution = out[:5]
                sort = out[5] if len(out) > 5 else True
                try:
                    if self.add(level, prompt, answer, wrong, hints, solution, rng, sort, f"{self.skill_id}:{t.__name__}"):
                        break
                except (AssertionError, ValueError, ZeroDivisionError):
                    continue
            else:
                raise RuntimeError(f"{self.skill_id} {level}: template {t.__name__} never produced a valid problem")

    def all(self):
        return self.items["basics"] + self.items["challenge"]


NAMES = ["Ava", "Ben", "Carmen", "Dev", "Elena", "Farid", "Grace", "Hiro", "Isla", "Jamal", "Kira", "Leo",
         "Maya", "Nico", "Olivia", "Priya", "Quinn", "Rosa", "Sam", "Tara", "Uma", "Victor", "Wren", "Yusuf", "Zoe"]


def two_names(rng):
    a, b = rng.sample(NAMES, 2)
    return a, b


def write_unit(path, banks):
    data = []
    for b in banks:
        data.extend(b.all())
    with open(path, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    return data


def comb(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


def frac_tex(fr):
    return tex_num(Fraction(fr))


# ---------- worked solutions ----------

def explain(need, idea, steps, answer, trap=None):
    """A full worked solution, shown after a student answers.

    need:   what the question is really asking, in plain words
    idea:   the key idea or method
    steps:  list of steps; each can hold several sentences and display math ($$...$$)
    answer: the final line; "ANSWER" (the letter) is added after it
    trap:   optional common mistake, often the one behind a wrong choice
    """
    out = [f"**What we need:** {need}", f"**Key idea:** {idea}"]
    out += [f"**Step {i}.** {s}" for i, s in enumerate(steps, 1)]
    out.append(f"**Answer:** {answer} ANSWER")
    if trap:
        out.append(f"**Common mistake:** {trap}")
    return "\n\n".join(out)


def var(name):
    """The variable letter for a person in a word problem: Victor -> v."""
    return name[0].lower()


def Q(p, ans, wrong, hint, need, idea, steps, trap=None, ans_tex=None, sort=True):
    """Packs a problem in the form templates return. `ans` is a number (int or Fraction) or a C choice."""
    if ans_tex is None:
        ans_tex = ans.tex if isinstance(ans, C) else tex_num(ans)
    hints = [hint] if isinstance(hint, str) else list(hint)
    sol = explain(need, idea, steps, f"${ans_tex}$.", trap)
    return (tidy(p), ans, wrong, [tidy(h) for h in hints], tidy(sol), sort)


def tidy(s):
    """Writes a coefficient of 1 the way people do: '1x' becomes 'x' and '-1x' becomes '-x'."""
    return re.sub(r"(?<=[\s$(+\-{=])1(?=[a-z](?![a-z]))", "", s)


def sg(c):
    """' + 3' or ' - 3', for writing a signed term after another."""
    return f" + {c}" if c >= 0 else f" - {abs(c)}"


def par(v):
    """A number in parentheses when it is negative, for substituting into expressions."""
    return f"({v})" if v < 0 else f"{v}"
