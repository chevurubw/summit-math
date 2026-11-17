"""AMC 12 only units: trigonometry, logarithms, complex numbers, polynomials, conics, sequences and series."""
import cmath
import itertools
import math
from fractions import Fraction as F

from common import Bank, C, comb, explain, num, simplify_sqrt, text_choice, par
from amc12_more1 import MORE as M1
from amc12_more2 import MORE as M2
from amc12_more3 import MORE as M3

MORE = {**M1, **M2, **M3}

banks = []


def bank(skill_id):
    b = Bank(skill_id, track="amc12")
    banks.append(b)
    return b


def surd(k, rad=1):
    """k * sqrt(rad), k a Fraction, simplified."""
    k = F(k)
    if rad == 0:
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


# exact sin/cos for special angles (degrees) as (k, rad) meaning k*sqrt(rad)
SIN = {0: (0, 1), 30: (F(1, 2), 1), 45: (F(1, 2), 2), 60: (F(1, 2), 3), 90: (1, 1)}


def sin_exact(d):
    d %= 360
    sign = 1
    if d > 180:
        d, sign = d - 180, -1
    if d > 90:
        d = 180 - d
    k, r_ = SIN[d]
    return F(k) * sign, r_


def cos_exact(d):
    return sin_exact(90 - d)


ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]
QUAD = ["first", "second", "third", "fourth"]


def rad_tex(d):
    fr = F(d, 180)
    if fr == 0:
        return "0"
    if fr == 1:
        return "\\pi"
    if fr.denominator == 1:
        return f"{fr.numerator}\\pi"
    return f"\\frac{{{'' if fr.numerator == 1 else fr.numerator}\\pi}}{{{fr.denominator}}}"


def ref_angle(d):
    d %= 180
    return min(d, 180 - d)


def sgn(v):
    return "+" if v >= 0 else "-"


# ---------------------------------------------------------------- trig values
b = bank("trig_values")


def tv1(r):
    d = r.choice([a for a in ANG if a % 90])
    fn = r.choice(["sin", "cos"])
    k, rr = sin_exact(d) if fn == "sin" else cos_exact(d)
    ans = surd(k, rr)
    wrong = [surd(-k, rr), surd(F(1, 2), 1), surd(F(1, 2), 3), surd(F(1, 2), 2), surd(F(-1, 2), 3), surd(F(-1, 2), 2), surd(F(-1, 2), 1)]
    ang = rad_tex(d) if r.random() < 0.5 else f"{d}^\\circ"
    q = QUAD[d // 90]
    ref = ref_angle(d)
    p = f"What is $\\{fn}\\left({ang}\\right)$?"
    steps = ([f"Convert to degrees: ${ang} = {ang} \\cdot \\frac{{180^\\circ}}{{\\pi}} = {d}^\\circ$."] if "pi" in ang else []) + [
        f"${d}^\\circ$ is in the {q} quadrant. Its reference angle (distance to the $x$-axis) is ${ref}^\\circ$.",
        f"From the special triangles, $\\{fn} {ref}^\\circ = {surd(abs(k), rr).tex}$.",
        f"In the {q} quadrant, {'sine' if fn == 'sin' else 'cosine'} is {'positive' if k > 0 else 'negative'}" + (" (sine is positive in quadrants I and II)" if fn == "sin" else " (cosine is positive in quadrants I and IV)") + f", so the value is ${ans.tex}$."]
    sol = explain(f"the exact value of $\\{fn}\\left({ang}\\right)$.", "every angle behaves like its reference angle in the first quadrant; only the sign changes with the quadrant.",
                  steps, f"${ans.tex}$.", "getting the size right but the sign wrong for the quadrant.")
    return (p, ans, wrong, ["Find the reference angle, then use the sign for the quadrant."], sol)


def tv2(r):
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
    sk, sr = sin_exact(d)
    ck, cr = cos_exact(d)
    t = (sk * math.sqrt(sr)) / (ck * math.sqrt(cr))
    tans = {1: surd(1), -1: surd(-1), math.sqrt(3): surd(1, 3), -math.sqrt(3): surd(-1, 3), 1 / math.sqrt(3): surd(F(1, 3), 3), -1 / math.sqrt(3): surd(F(-1, 3), 3)}
    ans = min(tans.items(), key=lambda kv: abs(kv[0] - t))[1]
    p = f"What is $\\tan {d}^\\circ$?"
    sol = explain(f"$\\tan {d}^\\circ$.", "$\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$, so find sine and cosine first.",
                  [f"Reference angle ${ref_angle(d)}^\\circ$, {QUAD[d // 90]} quadrant.", f"$\\sin {d}^\\circ = {surd(sk, sr).tex}$ and $\\cos {d}^\\circ = {surd(ck, cr).tex}$.",
                   f"Divide: $\\tan {d}^\\circ = \\dfrac{{{surd(sk, sr).tex}}}{{{surd(ck, cr).tex}}} = {ans.tex}$."],
                  f"${ans.tex}$.", "dividing cosine by sine, which gives the cotangent.")
    return (p, ans, [v for k_, v in tans.items() if v is not ans], ["$\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$."], sol)


def tv3(r):
    d = r.choice([15, 18, 20, 36, 40, 72, 75, 100, 105, 108, 140, 160, 200, 210, 225, 252, 270, 300, 330, 345])
    fr = F(d, 180)
    tex = rad_tex(d)
    ans = C(tex, float(fr) * math.pi)
    wrong = [C(rad_tex(d * 2), float(fr) * 2 * math.pi), C(rad_tex(d // 2) if d % 2 == 0 else "\\frac{\\pi}{7}", float(fr) / 2 * math.pi if d % 2 == 0 else math.pi / 7),
             C(f"\\frac{{{d}}}{{\\pi}}", d / math.pi), C(rad_tex(180 - d) if d < 180 else rad_tex(d - 90), (180 - d if d < 180 else d - 90) / 180 * math.pi)]
    g = math.gcd(d, 180)
    p = f"What is ${d}^\\circ$ in radians?"
    sol = explain(f"${d}^\\circ$ written in radians.", "a half turn is $180^\\circ = \\pi$ radians, so multiply degrees by $\\frac{\\pi}{180}$.",
                  [f"${d}^\\circ \\cdot \\frac{{\\pi}}{{180^\\circ}} = \\frac{{{d}\\pi}}{{180}}$.", f"Both ${d}$ and $180$ are divisible by ${g}$: $\\frac{{{d}}}{{180}} = {num(fr).tex}$.", f"So ${d}^\\circ = {tex}$."],
                  f"${tex}$.", "multiplying by $\\frac{180}{\\pi}$, which goes the other way (radians to degrees).")
    return (p, ans, wrong, ["Multiply by $\\frac{\\pi}{180}$."], sol)


def tv4(r):
    a, bb = r.sample([30, 45, 60], 2)
    sa, sr = sin_exact(a)
    cb, cr = cos_exact(bb)
    val = F(sa) ** 2 * sr + F(cb) ** 2 * cr
    p = f"What is $\\sin^2 {a}^\\circ + \\cos^2 {bb}^\\circ$?"
    sol = explain("the sum of two squared trig values at different angles.", "look up each exact value, square it, and add.",
                  [f"$\\sin {a}^\\circ = {surd(sa, sr).tex}$, so $\\sin^2 {a}^\\circ = {num(F(sa) ** 2 * sr).tex}$.", f"$\\cos {bb}^\\circ = {surd(cb, cr).tex}$, so $\\cos^2 {bb}^\\circ = {num(F(cb) ** 2 * cr).tex}$.",
                   f"Add: ${num(F(sa) ** 2 * sr).tex} + {num(F(cb) ** 2 * cr).tex} = {num(val).tex}$."],
                  f"${num(val).tex}$.", "using $\\sin^2 + \\cos^2 = 1$. That identity needs the same angle in both terms.")
    return (p, val, [1, val + F(1, 4), F(1, 2), F(3, 2) if val != F(3, 2) else F(5, 4), F(1, 4)], ["Use the exact values of sine and cosine at special angles."], sol)


def tvc1(r):
    step = r.choice([5, 6, 9, 10, 15, 18])
    angles = list(range(step, 90, step))
    total = sum(math.sin(math.radians(a)) ** 2 for a in angles)
    ans = F(round(total * 2), 2)
    assert abs(float(ans) - total) < 1e-9
    pairs = len(angles) // 2
    mid = 45 in angles
    p = f"What is $\\sin^2 {step}^\\circ + \\sin^2 {2 * step}^\\circ + \\cdots + \\sin^2 {angles[-1]}^\\circ$?"
    sol = explain("the sum of many squared sines.", "$\\sin(90^\\circ - \\theta) = \\cos\\theta$, so terms whose angles add to $90^\\circ$ pair up into $\\sin^2\\theta + \\cos^2\\theta = 1$.",
                  [f"There are ${len(angles)}$ terms, with angles ${step}^\\circ, {2 * step}^\\circ, \\ldots, {angles[-1]}^\\circ$.",
                   f"Pair the first and last: $\\sin^2 {step}^\\circ + \\sin^2 {90 - step}^\\circ = \\sin^2 {step}^\\circ + \\cos^2 {step}^\\circ = 1$. The same works for the next pair inward, and so on.",
                   f"That makes ${pairs}$ pairs worth $1$ each" + (", plus the middle term $\\sin^2 45^\\circ = \\frac{1}{2}$." if mid else "."),
                   f"Total: ${pairs}" + (" + \\frac{1}{2}" if mid else "") + f" = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting the unpaired middle term $\\sin^2 45^\\circ$, or trying to compute each term numerically.")
    return (p, ans, [len(angles), F(len(angles), 4), ans + F(1, 2), ans - 1, F(len(angles) + 1, 2)], ["Pair $\\sin^2\\theta$ with $\\sin^2(90^\\circ - \\theta) = \\cos^2\\theta$."], sol)


def tvc2(r):
    d = r.choice([15, 75, 105, 165])
    fn = r.choice(["sin", "cos"])
    val = math.sin(math.radians(d)) if fn == "sin" else math.cos(math.radians(d))
    combos = {}
    for s1 in (1, -1):
        for s2 in (1, -1):
            v = (s1 * math.sqrt(6) + s2 * math.sqrt(2)) / 4
            t = f"\\frac{{{'-' if s1 < 0 else ''}\\sqrt{{6}} {'+' if s2 > 0 else '-'} \\sqrt{{2}}}}{{4}}"
            combos[t] = v
    tex = min(combos, key=lambda t: abs(combos[t] - val))
    ans = C(tex, combos[tex])
    wrong = [C(t, v) for t, v in combos.items() if t != tex] + [C("\\frac{\\sqrt{3}}{4}", math.sqrt(3) / 4)]
    A, B, sg = {15: (45, 30, -1), 75: (45, 30, 1), 105: (60, 45, 1), 165: (120, 45, 1)}[d]
    sA, cA, sB, cB = sin_exact(A), cos_exact(A), sin_exact(B), cos_exact(B)
    prod = lambda x, y: surd(F(x[0]) * F(y[0]), x[1] * y[1])
    o = "+" if sg > 0 else "-"
    if fn == "sin":
        formula = f"\\sin({A}^\\circ {o} {B}^\\circ) = \\sin {A}^\\circ \\cos {B}^\\circ {o} \\cos {A}^\\circ \\sin {B}^\\circ"
        t1, t2, op = prod(sA, cB), prod(cA, sB), sg
    else:
        formula = f"\\cos({A}^\\circ {o} {B}^\\circ) = \\cos {A}^\\circ \\cos {B}^\\circ {'-' if sg > 0 else '+'} \\sin {A}^\\circ \\sin {B}^\\circ"
        t1, t2, op = prod(cA, cB), prod(sA, sB), -sg
    p = f"What is $\\{fn} {d}^\\circ$?"
    sol = explain(f"the exact value of $\\{fn} {d}^\\circ$.", f"${d}^\\circ$ is not a special angle, but ${d}^\\circ = {A}^\\circ {o} {B}^\\circ$ is built from special angles. Use the angle {'sum' if sg > 0 else 'difference'} formula.",
                  [f"${formula}$.", f"Values: $\\sin {A}^\\circ = {surd(*sA).tex}$, $\\cos {A}^\\circ = {surd(*cA).tex}$, $\\sin {B}^\\circ = {surd(*sB).tex}$, $\\cos {B}^\\circ = {surd(*cB).tex}$.",
                   f"The two products are ${t1.tex}$ and ${t2.tex}$.", f"Combine: ${t1.tex} {'+' if op > 0 else '-'} \\left({t2.tex}\\right) = {tex}$."],
                  f"${tex}$.", f"splitting the function, as in $\\{fn}(A {o} B) = \\{fn} A {o} \\{fn} B$. That is not an identity.")
    return (p, ans, wrong, ["Write the angle as a sum or difference of $30^\\circ$, $45^\\circ$, $60^\\circ$, and so on."], sol)


def tvc3(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    q = r.choice([1, 2, 3, 4])
    sx = 1 if q in (1, 4) else -1
    sy = 1 if q in (1, 2) else -1
    tanv = F(sy * a, sx * bb)
    ask = r.choice(["sin", "cos"])
    ans = F(sy * a, c) if ask == "sin" else F(sx * bb, c)
    quad = {1: "first", 2: "second", 3: "third", 4: "fourth"}[q]
    p = f"An angle $\\theta$ in the {quad} quadrant has $\\tan\\theta = {num(tanv).tex}$. What is $\\{ask}\\theta$?"
    sol = explain(f"$\\{ask}\\theta$ from $\\tan\\theta$ and the quadrant.", "think of $\\theta$ as pointing to a point $(x, y)$: $\\tan\\theta = \\frac{y}{x}$, $\\sin\\theta = \\frac{y}{r}$, $\\cos\\theta = \\frac{x}{r}$, where $r = \\sqrt{x^2 + y^2}$.",
                  [f"In the {quad} quadrant, $x$ is {'positive' if sx > 0 else 'negative'} and $y$ is {'positive' if sy > 0 else 'negative'}. With $\\frac{{y}}{{x}} = {num(tanv).tex}$, take $x = {sx * bb}$, $y = {sy * a}$.",
                   f"$r = \\sqrt{{{bb}^2 + {a}^2}} = {c}$ (a ${a}$, ${bb}$, ${c}$ right triangle).", f"$\\{ask}\\theta = \\frac{{{'y' if ask == 'sin' else 'x'}}}{{r}} = \\frac{{{sy * a if ask == 'sin' else sx * bb}}}{{{c}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "dropping the sign; the quadrant decides whether $x$ and $y$ are negative.")
    return (p, ans, [-ans, F(a, c) if ask == "cos" else F(bb, c), F(-bb, c) if ask == "sin" else F(-a, c), tanv, F(c, bb)], ["Draw a right triangle with the right legs, then use the quadrant for signs."], sol)


b.fill_unique("basics", [tv1, tv2, tv3, tv4] + MORE[b.skill_id]["basics"], 4101)
b.fill_unique("challenge", [tvc1, tvc2, tvc3] + MORE[b.skill_id]["challenge"], 4102)


# ---------------------------------------------------------------- trig identities
b = bank("trig_identities")


def ti1(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    s = F(a, c)
    ans = F(bb, c)
    neg = r.random() < 0.5
    quad = "second" if neg else "first"
    ans = -ans if neg else ans
    p = f"If $\\sin\\theta = {num(s).tex}$ and $\\theta$ is in the {quad} quadrant, what is $\\cos\\theta$?"
    sol = explain("$\\cos\\theta$ from $\\sin\\theta$.", "the Pythagorean identity $\\sin^2\\theta + \\cos^2\\theta = 1$ gives the size of $\\cos\\theta$; the quadrant gives its sign.",
                  [f"$\\cos^2\\theta = 1 - \\left({num(s).tex}\\right)^2 = 1 - {num(s * s).tex} = {num(F(bb * bb, c * c)).tex}$.", f"So $\\cos\\theta = \\pm{num(F(bb, c)).tex}$.",
                   f"In the {quad} quadrant cosine is {'negative' if neg else 'positive'}, so $\\cos\\theta = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting the sign: cosine is negative in the second quadrant.")
    return (p, ans, [-ans, s, 1 - s, F(a, bb), F(c, bb)], ["Use $\\sin^2\\theta + \\cos^2\\theta = 1$."], sol)


def ti2(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    s, co = F(a, c), F(bb, c)
    ask = r.choice(["sin2", "cos2"])
    ans = 2 * s * co if ask == "sin2" else co * co - s * s
    fn = "\\sin 2\\theta" if ask == "sin2" else "\\cos 2\\theta"
    p = f"If $\\sin\\theta = {num(s).tex}$ and $\\cos\\theta = {num(co).tex}$, what is ${fn}$?"
    if ask == "sin2":
        steps = ["Double angle formula: $\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$.", f"$2 \\cdot {num(s).tex} \\cdot {num(co).tex} = \\frac{{{2 * a * bb}}}{{{c * c}}} = {num(ans).tex}$."]
        trap = "doubling only the sine, $2\\sin\\theta$; that is not $\\sin 2\\theta$."
    else:
        steps = ["Double angle formula: $\\cos 2\\theta = \\cos^2\\theta - \\sin^2\\theta$.", f"${num(co * co).tex} - {num(s * s).tex} = \\frac{{{bb * bb - a * a}}}{{{c * c}}} = {num(ans).tex}$."]
        trap = "subtracting in the wrong order ($\\sin^2 - \\cos^2$), which flips the sign."
    sol = explain(f"${fn}$.", "use the double angle formula, then plug in the given values.", steps, f"${num(ans).tex}$.", trap)
    return (p, ans, [2 * s, s * co, -ans, 1 - 2 * co * co, ans + F(1, c)], ["$\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$ and $\\cos 2\\theta = \\cos^2\\theta - \\sin^2\\theta$."], sol)


def ti3(r):
    k = r.choice([F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(4, 3), F(5, 4), F(7, 5), F(6, 5)])
    ans = (k * k - 1) / 2
    p = f"If $\\sin x + \\cos x = {num(k).tex}$, what is $\\sin x \\cos x$?"
    sol = explain("the product $\\sin x\\cos x$.", "squaring a sum creates the product term, and $\\sin^2 x + \\cos^2 x = 1$ cleans up the rest.",
                  [f"Square both sides: $\\sin^2 x + 2\\sin x\\cos x + \\cos^2 x = {num(k * k).tex}$.", f"Replace $\\sin^2 x + \\cos^2 x$ with $1$: $1 + 2\\sin x\\cos x = {num(k * k).tex}$.",
                   f"$2\\sin x\\cos x = {num(k * k - 1).tex}$, so $\\sin x\\cos x = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting the $1$ from $\\sin^2 x + \\cos^2 x$, or forgetting to divide by $2$.")
    return (p, ans, [k * k, (k * k + 1) / 2, k / 2, 1 - k * k, ans * 2], ["Square both sides of the equation."], sol)


def ti4(r):
    d = r.choice([20, 35, 40, 50, 55, 70, 80])
    form = r.choice([("\\sec^2 {d}^\\circ - \\tan^2 {d}^\\circ", 1), ("\\sin^2 {d}^\\circ + \\sin^2 {e}^\\circ", 1), ("\\csc^2 {d}^\\circ - \\cot^2 {d}^\\circ", 1),
                     ("\\tan {d}^\\circ \\cdot \\tan {e}^\\circ", 1)])
    expr = form[0].replace("{d}", str(d)).replace("{e}", str(90 - d))
    e = 90 - d
    kind = form[0][:4]
    if kind == "\\sec":
        steps = ["Start from $\\sin^2\\theta + \\cos^2\\theta = 1$ and divide every term by $\\cos^2\\theta$.", "That gives $\\tan^2\\theta + 1 = \\sec^2\\theta$.", f"So $\\sec^2 {d}^\\circ - \\tan^2 {d}^\\circ = 1$."]
    elif kind == "\\csc":
        steps = ["Start from $\\sin^2\\theta + \\cos^2\\theta = 1$ and divide every term by $\\sin^2\\theta$.", "That gives $1 + \\cot^2\\theta = \\csc^2\\theta$.", f"So $\\csc^2 {d}^\\circ - \\cot^2 {d}^\\circ = 1$."]
    elif kind == "\\sin":
        steps = [f"The angles add to $90^\\circ$, so $\\sin {e}^\\circ = \\sin(90^\\circ - {d}^\\circ) = \\cos {d}^\\circ$.", f"The expression becomes $\\sin^2 {d}^\\circ + \\cos^2 {d}^\\circ$, which is $1$."]
    else:
        steps = [f"The angles add to $90^\\circ$, so $\\tan {e}^\\circ = \\tan(90^\\circ - {d}^\\circ) = \\cot {d}^\\circ = \\frac{{1}}{{\\tan {d}^\\circ}}$.", f"So $\\tan {d}^\\circ \\cdot \\frac{{1}}{{\\tan {d}^\\circ}} = 1$."]
    p = f"What is ${expr}$?"
    sol = explain(f"the value of ${expr}$, without a calculator.", "the angle isn't special, so an identity must make the expression collapse.", steps, "$1$.", "trying to estimate each trig value numerically.")
    return (p, 1, [0, 2, F(1, 2), -1, d], ["Use $\\sin^2 + \\cos^2 = 1$ and the cofunction identities like $\\sin(90^\\circ - x) = \\cos x$."], sol)


def tic1(r):
    ta, tb = r.choice([(F(1, 2), F(1, 3)), (F(2), F(3)), (F(1, 4), F(3, 5)), (F(1, 2), F(1, 5)), (F(3), F(1, 2)), (F(2, 3), F(1, 5))])
    if ta * tb == 1:
        return None
    ans = (ta + tb) / (1 - ta * tb)
    p = f"If $\\tan A = {num(ta).tex}$ and $\\tan B = {num(tb).tex}$, what is $\\tan(A + B)$?"
    sol = explain("$\\tan(A + B)$.", "the tangent addition formula $\\tan(A + B) = \\dfrac{\\tan A + \\tan B}{1 - \\tan A\\tan B}$.",
                  [f"Top: ${num(ta).tex} + {num(tb).tex} = {num(ta + tb).tex}$.", f"Bottom: $1 - {num(ta).tex} \\cdot {num(tb).tex} = 1 - {num(ta * tb).tex} = {num(1 - ta * tb).tex}$.",
                   f"Divide: $\\frac{{{num(ta + tb).tex}}}{{{num(1 - ta * tb).tex}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "using $+$ in the denominator, which is the formula for $\\tan(A - B)$ turned around.")
    return (p, ans, [ta + tb, (ta - tb) / (1 + ta * tb), -ans, ta * tb, (ta + tb) / (1 + ta * tb)], ["$\\tan(A + B) = \\frac{\\tan A + \\tan B}{1 - \\tan A \\tan B}$."], sol)


def tic2(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25)])
    k = r.randint(-5, 5)
    ask = r.choice(["max", "min"])
    ans = (c + k) if ask == "max" else (k - c)
    p = f"What is the {'maximum' if ask == 'max' else 'minimum'} value of ${a}\\sin x + {bb}\\cos x {'+' if k >= 0 else '-'} {abs(k)}$?"
    sol = explain(f"the {'largest' if ask == 'max' else 'smallest'} value of the expression.", "$a\\sin x + b\\cos x$ can be rewritten as one wave $R\\sin(x + \\varphi)$ with $R = \\sqrt{a^2 + b^2}$, so it swings between $-R$ and $R$.",
                  [f"$R = \\sqrt{{{a}^2 + {bb}^2}} = \\sqrt{{{a * a + bb * bb}}} = {c}$.", f"So ${a}\\sin x + {bb}\\cos x$ ranges from $-{c}$ to ${c}$.",
                   f"The {ask} of the whole expression is ${'' if ask == 'max' else '-'}{c} {'+' if k >= 0 else '-'} {abs(k)} = {ans}$."],
                  f"${ans}$.", f"adding ${a} + {bb}$; sine and cosine can't both equal $1$ at the same $x$.")
    return (p, ans, [a + bb + k if ask == "max" else k - a - bb, -ans, c, ans + 1, k], ["$a\\sin x + b\\cos x$ ranges between $-\\sqrt{a^2 + b^2}$ and $\\sqrt{a^2 + b^2}$."], sol)


TIC3 = {
    "\\cos 20^\\circ \\cos 40^\\circ \\cos 80^\\circ": ["Call the product $P$ and multiply by $\\sin 20^\\circ$: use $\\sin\\theta\\cos\\theta = \\frac{1}{2}\\sin 2\\theta$ three times.",
                                                        "$\\sin 20^\\circ\\cos 20^\\circ = \\frac{1}{2}\\sin 40^\\circ$; then $\\frac{1}{2}\\sin 40^\\circ\\cos 40^\\circ = \\frac{1}{4}\\sin 80^\\circ$; then $\\frac{1}{4}\\sin 80^\\circ\\cos 80^\\circ = \\frac{1}{8}\\sin 160^\\circ$.",
                                                        "So $P\\sin 20^\\circ = \\frac{1}{8}\\sin 160^\\circ = \\frac{1}{8}\\sin 20^\\circ$, and $P = \\frac{1}{8}$."],
    "\\sin 10^\\circ \\sin 50^\\circ \\sin 70^\\circ": ["Use $\\sin x = \\cos(90^\\circ - x)$: the product is $\\cos 80^\\circ \\cos 40^\\circ \\cos 20^\\circ$.",
                                                        "Multiply by $\\sin 20^\\circ$ and apply $\\sin\\theta\\cos\\theta = \\frac{1}{2}\\sin 2\\theta$ three times: $\\sin 20^\\circ \\to \\frac{1}{2}\\sin 40^\\circ \\to \\frac{1}{4}\\sin 80^\\circ \\to \\frac{1}{8}\\sin 160^\\circ$.",
                                                        "$\\sin 160^\\circ = \\sin 20^\\circ$, so the product is $\\frac{1}{8}$."],
    "\\cos 36^\\circ - \\cos 72^\\circ": ["From the regular pentagon (or solving $\\cos 2\\theta = -\\cos 3\\theta$ at $\\theta = 36^\\circ$): $\\cos 36^\\circ = \\frac{1 + \\sqrt{5}}{4}$ and $\\cos 72^\\circ = \\frac{\\sqrt{5} - 1}{4}$.",
                                          "Subtract: $\\frac{(1 + \\sqrt{5}) - (\\sqrt{5} - 1)}{4} = \\frac{2}{4} = \\frac{1}{2}$."],
    "\\sin 18^\\circ \\cos 36^\\circ": ["$\\sin 18^\\circ = \\cos 72^\\circ = \\frac{\\sqrt{5} - 1}{4}$ and $\\cos 36^\\circ = \\frac{\\sqrt{5} + 1}{4}$.",
                                         "Multiply: $\\frac{(\\sqrt{5} - 1)(\\sqrt{5} + 1)}{16} = \\frac{5 - 1}{16} = \\frac{1}{4}$."],
    "\\tan 20^\\circ \\tan 40^\\circ \\tan 80^\\circ": ["Identity: $\\tan\\theta \\tan(60^\\circ - \\theta)\\tan(60^\\circ + \\theta) = \\tan 3\\theta$.",
                                                        "With $\\theta = 20^\\circ$: $60^\\circ - 20^\\circ = 40^\\circ$ and $60^\\circ + 20^\\circ = 80^\\circ$, exactly our angles.", "So the product is $\\tan 60^\\circ = \\sqrt{3}$."],
    "\\cos\\frac{\\pi}{7}\\cos\\frac{2\\pi}{7}\\cos\\frac{4\\pi}{7}": ["Call the product $P$ and multiply by $\\sin\\frac{\\pi}{7}$. Apply $\\sin\\theta\\cos\\theta = \\frac{1}{2}\\sin 2\\theta$ three times.",
                                                                     "$P\\sin\\frac{\\pi}{7} = \\frac{1}{8}\\sin\\frac{8\\pi}{7}$.", "$\\sin\\frac{8\\pi}{7} = \\sin\\left(\\pi + \\frac{\\pi}{7}\\right) = -\\sin\\frac{\\pi}{7}$, so $P = -\\frac{1}{8}$."],
    "\\sin 20^\\circ \\sin 40^\\circ \\sin 80^\\circ": ["Identity: $\\sin\\theta\\sin(60^\\circ - \\theta)\\sin(60^\\circ + \\theta) = \\frac{1}{4}\\sin 3\\theta$.",
                                                        "With $\\theta = 20^\\circ$ the angles are $20^\\circ, 40^\\circ, 80^\\circ$.", "So the product is $\\frac{1}{4}\\sin 60^\\circ = \\frac{1}{4} \\cdot \\frac{\\sqrt{3}}{2} = \\frac{\\sqrt{3}}{8}$."],
    "\\cos 72^\\circ + \\cos 144^\\circ": ["$\\cos 144^\\circ = -\\cos 36^\\circ$.", "With $\\cos 72^\\circ = \\frac{\\sqrt{5} - 1}{4}$ and $\\cos 36^\\circ = \\frac{\\sqrt{5} + 1}{4}$: $\\frac{\\sqrt{5} - 1}{4} - \\frac{\\sqrt{5} + 1}{4} = -\\frac{2}{4} = -\\frac{1}{2}$."],
}


def tic3(r):
    choice = r.choice([("\\cos 20^\\circ \\cos 40^\\circ \\cos 80^\\circ", F(1, 8)), ("\\sin 10^\\circ \\sin 50^\\circ \\sin 70^\\circ", F(1, 8)),
                       ("\\cos 36^\\circ - \\cos 72^\\circ", F(1, 2)), ("\\sin 18^\\circ \\cos 36^\\circ", F(1, 4)),
                       ("\\tan 20^\\circ \\tan 40^\\circ \\tan 80^\\circ", None), ("\\cos\\frac{\\pi}{7}\\cos\\frac{2\\pi}{7}\\cos\\frac{4\\pi}{7}", F(-1, 8)),
                       ("\\sin 20^\\circ \\sin 40^\\circ \\sin 80^\\circ", None), ("\\cos 72^\\circ + \\cos 144^\\circ", F(-1, 2))])
    expr, val = choice
    if val is None:
        if "tan" in expr:
            ans = surd(1, 3)
            wrong = [surd(F(1, 3), 3), num(1), surd(F(1, 2), 3), num(F(1, 8))]
        else:
            ans = surd(F(1, 8), 3)
            wrong = [num(F(1, 8)), surd(F(1, 4), 3), surd(F(1, 8), 2), num(F(3, 8))]
    else:
        ans = num(val)
        wrong = [num(-val), num(val * 2), num(val / 2), num(F(1, 3)), num(F(3, 8))]
    approx = eval_expr(expr)
    assert abs(approx - ans.key) < 1e-9, (expr, approx, ans.key)
    p = f"What is ${expr}$?"
    sol = explain(f"the exact value of ${expr}$.", "these angles are linked (doubling, or $60^\\circ \\pm \\theta$, or the pentagon angles), so a classic identity collapses the expression.",
                  TIC3[expr], f"${ans.tex}$.", "estimating with decimals; the exact value comes from the identity.")
    return (p, ans, wrong, ["Look for a double angle or product identity that collapses the expression."], sol)


def eval_expr(expr):
    e = expr.replace("^\\circ", "").replace("\\", "")
    import re
    e = re.sub(r"frac\{pi\}\{(\d+)\}", r"(math.pi/\1)", e)
    e = re.sub(r"frac\{(\d+)pi\}\{(\d+)\}", r"(\1*math.pi/\2)", e)
    e = re.sub(r"(sin|cos|tan) (\d+)", r"math.\1(math.radians(\2))", e)
    e = re.sub(r"(sin|cos|tan)\(", r"math.\1(", e)
    e = e.replace("cos(math.pi", "math.cos(math.pi").replace("math.math.", "math.")
    e = re.sub(r"cos\((\()", r"math.cos(\1", e)
    e = e.replace(") math", ")*math").replace(")math", ")*math")
    e = re.sub(r"(math\.\w+\([^)]*\)\)?)\s*(math)", r"\1*\2", e)
    return eval(e, {"math": math})


b.fill_unique("basics", [ti1, ti2, ti3, ti4] + MORE[b.skill_id]["basics"], 4201)
b.fill_unique("challenge", [tic1, tic2, tic3] + MORE[b.skill_id]["challenge"], 4202)


# ---------------------------------------------------------------- law of sines and cosines
b = bank("trig_laws")


def tl1(r):
    a, bb = r.randint(2, 12), r.randint(2, 12)
    C_ = r.choice([60, 120, 90])
    c2 = a * a + bb * bb - (a * bb if C_ == 60 else -a * bb if C_ == 120 else 0)
    ans = surd(1, c2)
    p = f"In triangle $ABC$, $a = {a}$, $b = {bb}$, and $\\angle C = {C_}^\\circ$. What is the length of side $c$?"
    wrong = [surd(1, a * a + bb * bb), surd(1, a * a + bb * bb + (a * bb if C_ == 60 else -a * bb if C_ == 120 else a * bb)), num(a + bb), surd(1, abs(a * a - bb * bb) or 3), num(abs(a - bb) + 1)]
    cosv = {60: "\\frac{1}{2}", 120: "-\\frac{1}{2}", 90: "0"}[C_]
    mid = {60: a * bb, 120: -a * bb, 90: 0}[C_]
    sol = explain("side $c$, opposite the known angle $C$.", "two sides and the angle between them: use the Law of Cosines, $c^2 = a^2 + b^2 - 2ab\\cos C$.",
                  [f"$\\cos {C_}^\\circ = {cosv}$.", f"$2ab\\cos C = 2 \\cdot {a} \\cdot {bb} \\cdot {cosv} = {mid}$.", f"$c^2 = {a * a} + {bb * bb} - ({mid}) = {c2}$.", f"$c = \\sqrt{{{c2}}} = {ans.tex}$."],
                  f"${ans.tex}$.", "using $\\cos 120^\\circ = +\\frac{1}{2}$. It is negative, so the term gets added." if C_ == 120 else "forgetting to take the square root at the end.")
    return (p, ans, wrong, ["Law of Cosines: $c^2 = a^2 + b^2 - 2ab\\cos C$."], sol)


def tl2(r):
    a, bb = r.randint(3, 15), r.randint(3, 15)
    C_ = r.choice([30, 45, 60, 90, 120, 135, 150])
    k, rr = sin_exact(C_)
    area_k = F(a * bb, 2) * k
    ans = surd(area_k, rr)
    p = f"What is the area of a triangle with two sides of lengths ${a}$ and ${bb}$ that form a ${C_}^\\circ$ angle?"
    wrong = [num(a * bb), num(F(a * bb, 2)), surd(area_k * 2, rr), surd(F(a * bb, 4), rr if rr > 1 else 3), surd(area_k, 3 if rr != 3 else 2)]
    sol = explain("the area from two sides and the angle between them.", "Area $= \\frac{1}{2}ab\\sin C$. (The height to side $a$ is $b\\sin C$.)",
                  [f"$\\sin {C_}^\\circ = {surd(k, rr).tex}$.", f"Area $= \\frac{{1}}{{2}} \\cdot {a} \\cdot {bb} \\cdot {surd(k, rr).tex} = {ans.tex}$."],
                  f"${ans.tex}$.", "forgetting the $\\frac{1}{2}$, or using $\\cos C$ instead of $\\sin C$.")
    return (p, ans, wrong, ["Area $= \\frac{1}{2}ab\\sin C$."], sol)


def tl3(r):
    A, B = r.choice([(30, 90), (30, 60), (45, 90), (30, 45), (60, 45), (30, 120), (45, 60)])
    a = r.randint(2, 12)
    ka, ra = sin_exact(A)
    kb, rb = sin_exact(B)
    val = a * (float(kb) * math.sqrt(rb)) / (float(ka) * math.sqrt(ra))
    coef = F(a) * F(kb) / F(ka) / ra
    ans = surd(coef, rb * ra)
    assert abs(ans.key - val) < 1e-9
    p = f"In triangle $ABC$, $\\angle A = {A}^\\circ$, $\\angle B = {B}^\\circ$, and $BC = {a}$. What is $AC$?"
    wrong = [num(a), surd(a, 2) if ans.tex != surd(a, 2).tex else num(2 * a), surd(a, 3) if ans.tex != surd(a, 3).tex else num(3 * a), num(2 * a) if ans.key != 2 * a else surd(2 * a, 2), surd(F(a, 2), 3)]
    sol = explain("side $AC$.", "Law of Sines: each side divided by the sine of the opposite angle gives the same number.",
                  [f"$BC$ is opposite $\\angle A$ and $AC$ is opposite $\\angle B$.", f"$\\frac{{AC}}{{\\sin {B}^\\circ}} = \\frac{{{a}}}{{\\sin {A}^\\circ}}$, so $AC = {a} \\cdot \\frac{{\\sin {B}^\\circ}}{{\\sin {A}^\\circ}}$.",
                   f"$\\sin {B}^\\circ = {surd(kb, rb).tex}$ and $\\sin {A}^\\circ = {surd(ka, ra).tex}$.", f"$AC = {a} \\cdot \\frac{{{surd(kb, rb).tex}}}{{{surd(ka, ra).tex}}} = {ans.tex}$."],
                  f"${ans.tex}$.", "pairing a side with the wrong angle. Each side goes with the angle across from it.")
    return (p, ans, wrong, ["Law of Sines: $\\frac{a}{\\sin A} = \\frac{b}{\\sin B}$. Side $BC$ is opposite $A$ and $AC$ is opposite $B$."], sol)


def tl4(r):
    trips = [((3, 5, 7), 120), ((5, 7, 8), 60), ((3, 7, 8), 60), ((7, 8, 13), 120), ((5, 8, 7), 60), ((1, 1, 1), 60), ((3, 4, 5), 90), ((5, 16, 19), 120), ((7, 15, 13), 60)]
    (a, bb, c), ang = r.choice(trips)
    k = r.randint(1, 3)
    cosv = F(a * a + bb * bb - c * c, 2 * a * bb)
    A_, B_, C2 = a * k, bb * k, c * k
    p = f"A triangle has sides ${a * k}$, ${bb * k}$, and ${c * k}$. What is the measure, in degrees, of the angle opposite the side of length ${c * k}$?"
    sol = explain(f"the angle opposite the side of length ${C2}$.", "three sides known: solve the Law of Cosines for the cosine, $\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}$.",
                  [f"Top: ${A_}^2 + {B_}^2 - {C2}^2 = {A_ * A_} + {B_ * B_} - {C2 * C2} = {A_ * A_ + B_ * B_ - C2 * C2}$.", f"Bottom: $2 \\cdot {A_} \\cdot {B_} = {2 * A_ * B_}$.",
                   f"$\\cos C = {num(cosv).tex}$, and the angle in $(0^\\circ, 180^\\circ)$ with this cosine is ${ang}^\\circ$."],
                  f"${ang}^\\circ$.", "dropping the minus sign; a negative cosine means an obtuse angle.")
    return (p, ang, [180 - ang, 90 if ang != 90 else 60, 45, 150 if ang != 150 else 30, 30], ["Use the Law of Cosines to find $\\cos C$."], sol)


def tlc1(r):
    a, bb, c = r.randint(4, 14), r.randint(4, 14), r.randint(4, 14)
    if a + bb <= c or a + c <= bb or bb + c <= a:
        return None
    m2 = F(2 * bb * bb + 2 * c * c - a * a, 4)
    if m2.denominator != 1:
        return None
    ans = surd(1, int(m2))
    p = f"Triangle $ABC$ has $AB = {c}$, $AC = {bb}$, and $BC = {a}$. What is the length of the median from $A$ to side $BC$?"
    sol = explain("the length from $A$ to the midpoint $M$ of $BC$.", "Apollonius's Theorem: $AB^2 + AC^2 = 2AM^2 + 2BM^2$, which rearranges to $AM^2 = \\frac{2b^2 + 2c^2 - a^2}{4}$. (It comes from the Law of Cosines in triangles $ABM$ and $ACM$, whose angles at $M$ add to $180^\\circ$.)",
                  [f"$BM = \\frac{{{a}}}{{2}}$.", f"$AM^2 = \\frac{{2 \\cdot {bb}^2 + 2 \\cdot {c}^2 - {a}^2}}{{4}} = \\frac{{{2 * bb * bb} + {2 * c * c} - {a * a}}}{{4}} = {int(m2)}$.", f"$AM = \\sqrt{{{int(m2)}}} = {ans.tex}$."],
                  f"${ans.tex}$.", "averaging $AB$ and $AC$; a median is not the average of the two sides.")
    return (p, ans, [surd(1, int(m2) + 1), surd(F(1, 2), a * a), num(F(bb + c, 2)), surd(1, abs(bb * bb + c * c - a * a) or 5), surd(1, int(m2) * 2)],
            ["Apollonius: $m_a^2 = \\frac{2b^2 + 2c^2 - a^2}{4}$. Or use the Law of Cosines twice."], sol)


def tlc2(r):
    A = r.choice([30, 45, 60, 90, 120, 135, 150])
    a = r.randint(2, 12)
    k, rr = sin_exact(A)
    R = F(a, 2) / F(k) / rr
    ans = surd(R, rr)
    p = f"In triangle $ABC$, $BC = {a}$ and $\\angle A = {A}^\\circ$. What is the radius of the circle passing through $A$, $B$, and $C$?"
    sol = explain("the circumradius $R$.", "the Extended Law of Sines: $\\frac{a}{\\sin A} = 2R$, where $a = BC$ is the side opposite $A$.",
                  [f"$\\sin {A}^\\circ = {surd(k, rr).tex}$.", f"$2R = \\frac{{{a}}}{{{surd(k, rr).tex}}} = {surd(2 * R, rr).tex}$.", f"$R = {ans.tex}$."],
                  f"${ans.tex}$.", "forgetting the $2$: $\\frac{a}{\\sin A}$ is the diameter, not the radius.")
    return (p, ans, [num(F(a, 2)), num(a), surd(R * 2, rr), surd(F(a, 2), 3) if rr != 3 else num(a + 1), surd(R, 2) if rr != 2 else num(2 * a)], ["Extended Law of Sines: $\\frac{a}{\\sin A} = 2R$."], sol)


def tlc3(r):
    tris = [(5, 5, 6), (5, 5, 8), (13, 14, 15), (10, 13, 13), (9, 10, 17), (13, 13, 10), (7, 15, 20), (11, 13, 20)]
    a, bb, c = r.choice(tris)
    s = F(a + bb + c, 2)
    prod = int(s * (s - a) * (s - bb) * (s - c))
    area = math.isqrt(prod)
    sinC = F(2 * area, a * bb)
    p = f"A triangle has sides ${a}$, ${bb}$, and ${c}$. What is the sine of the angle between the sides of lengths ${a}$ and ${bb}$?"
    sol = explain(f"$\\sin C$, where $C$ is between the sides ${a}$ and ${bb}$.", "find the area two ways: Heron's formula gives a number, and $\\frac{1}{2}ab\\sin C$ contains the unknown.",
                  [f"Semiperimeter: $s = \\frac{{{a} + {bb} + {c}}}{{2}} = {num(s).tex}$.", f"Heron: Area $= \\sqrt{{s(s - a)(s - b)(s - c)}} = \\sqrt{{{num(s).tex} \\cdot {num(s - a).tex} \\cdot {num(s - bb).tex} \\cdot {num(s - c).tex}}} = \\sqrt{{{prod}}} = {area}$.",
                   f"Set $\\frac{{1}}{{2}} \\cdot {a} \\cdot {bb} \\cdot \\sin C = {area}$.", f"$\\sin C = \\frac{{2 \\cdot {area}}}{{{a * bb}}} = {num(sinC).tex}$."],
                  f"${num(sinC).tex}$.", "using the wrong pair of sides in $\\frac{1}{2}ab\\sin C$; they must be the two sides that form the angle.")
    return (p, sinC, [F(area, a * bb), F(2 * area, a * c), 1 - sinC, F(c, a + bb), sinC / 2], ["Find the area with Heron's formula, then use area $= \\frac{1}{2}ab\\sin C$."], sol)


b.fill_unique("basics", [tl1, tl2, tl3, tl4] + MORE[b.skill_id]["basics"], 4301)
b.fill_unique("challenge", [tlc1, tlc2, tlc3] + MORE[b.skill_id]["challenge"], 4302)


# ---------------------------------------------------------------- trig equations
b = bank("trig_equations")


def te1(r):
    k = r.randint(1, 5)
    fn = r.choice(["sin", "cos"])
    val = r.choice([0, F(1, 2), F(-1, 2), 1, -1])
    xs = set()
    for i in range(k * 360 * 2):
        d = i / 2
        v = math.sin(math.radians(d)) if fn == "sin" else math.cos(math.radians(d))
        if abs(v - float(val)) < 1e-9:
            xs.add(round(d / k, 6) % 360)
    ans = len(xs)
    per = ans // k
    one = [d for d in range(360) if abs((math.sin if fn == "sin" else math.cos)(math.radians(d)) - float(val)) < 1e-9]
    p = f"How many solutions does $\\{fn}({k if k > 1 else ''}x) = {num(F(val)).tex}$ have with $0 \\le x < 2\\pi$?"
    sol = explain("the number of solutions in one full turn of $x$.", f"substitute $t = {k if k > 1 else ''}x$. As $x$ runs over $[0, 2\\pi)$, $t$ runs over $[0, {2 * k if k > 1 else 2}\\pi)$, which is ${k}$ full turn{'s' if k > 1 else ''}.",
                  [f"In one turn, $\\{fn} t = {num(F(val)).tex}$ at " + ", ".join(f"$t = {rad_tex(d)}$" for d in one) + f": ${per}$ solution{'s' if per != 1 else ''}.",
                   f"Each of the ${k}$ turns repeats this, so there are ${k} \\cdot {per} = {ans}$ values of $t$, each giving one $x$."],
                  f"${ans}$.", f"counting only one turn of $t$ (${per}$); the ${k}x$ makes the graph repeat ${k}$ times." if k > 1 else "counting a value like $\\pm 1$ twice; it happens only once per turn.")
    return (p, ans, [ans + 1, ans - 1 if ans > 1 else ans + 2, 2 * k, k, ans * 2], [f"First count the solutions of $\\{fn} t = {num(F(val)).tex}$ for one full turn, then $t = {k}x$ makes ${k}$ full turns."], sol)


TE2 = {
    "2\\sin^2 x - 3\\sin x + 1 = 0": "With $s = \\sin x$: $2s^2 - 3s + 1 = (2s - 1)(s - 1) = 0$, so $\\sin x = \\frac{1}{2}$ or $\\sin x = 1$.",
    "2\\cos^2 x - \\cos x - 1 = 0": "With $c = \\cos x$: $2c^2 - c - 1 = (2c + 1)(c - 1) = 0$, so $\\cos x = -\\frac{1}{2}$ or $\\cos x = 1$.",
    "2\\sin^2 x + \\sin x - 1 = 0": "With $s = \\sin x$: $2s^2 + s - 1 = (2s - 1)(s + 1) = 0$, so $\\sin x = \\frac{1}{2}$ or $\\sin x = -1$.",
    "\\sin^2 x = \\frac{1}{4}": "Take square roots: $\\sin x = \\frac{1}{2}$ or $\\sin x = -\\frac{1}{2}$.",
    "4\\cos^2 x = 3": "$\\cos^2 x = \\frac{3}{4}$, so $\\cos x = \\frac{\\sqrt{3}}{2}$ or $\\cos x = -\\frac{\\sqrt{3}}{2}$.",
    "2\\cos^2 x + 3\\cos x + 1 = 0": "With $c = \\cos x$: $2c^2 + 3c + 1 = (2c + 1)(c + 1) = 0$, so $\\cos x = -\\frac{1}{2}$ or $\\cos x = -1$.",
    "\\tan^2 x = 1": "$\\tan x = 1$ or $\\tan x = -1$.",
}


def te2(r):
    forms = [("2\\sin^2 x - 3\\sin x + 1 = 0", [F(1, 2), 1], "sin"), ("2\\cos^2 x - \\cos x - 1 = 0", [1, F(-1, 2)], "cos"),
             ("2\\sin^2 x + \\sin x - 1 = 0", [F(1, 2), -1], "sin"), ("\\sin^2 x = \\frac{1}{4}", [F(1, 2), F(-1, 2)], "sin"),
             ("4\\cos^2 x = 3", None, "cos3"), ("2\\cos^2 x + 3\\cos x + 1 = 0", [F(-1, 2), -1], "cos"), ("\\tan^2 x = 1", None, "tan1")]
    expr, vals, fn = r.choice(forms)
    if fn == "cos3":
        ans = 4
        lines = ["$\\cos x = \\frac{\\sqrt{3}}{2}$: $x = \\frac{\\pi}{6}, \\frac{11\\pi}{6}$", "$\\cos x = -\\frac{\\sqrt{3}}{2}$: $x = \\frac{5\\pi}{6}, \\frac{7\\pi}{6}$"]
    elif fn == "tan1":
        ans = 4
        lines = ["$\\tan x = 1$: $x = \\frac{\\pi}{4}, \\frac{5\\pi}{4}$", "$\\tan x = -1$: $x = \\frac{3\\pi}{4}, \\frac{7\\pi}{4}$"]
    else:
        sols = set()
        lines = []
        for v in vals:
            these = []
            for i in range(720):
                d = i / 2
                f = math.sin(math.radians(d)) if fn == "sin" else math.cos(math.radians(d))
                if abs(f - float(v)) < 1e-9:
                    sols.add(d)
                    these.append(int(d))
            lines.append(f"$\\{fn} x = {num(F(v)).tex}$: " + ", ".join(f"$x = {rad_tex(d)}$" for d in these))
        ans = len(sols)
    p = f"How many solutions does ${expr}$ have with $0 \\le x < 2\\pi$?"
    sol = explain("the number of angles in one full turn that solve the equation.", "solve for the trig function first (it's a quadratic in disguise), then count the angles for each value.",
                  [TE2[expr], "Angles in $[0, 2\\pi)$: " + "; ".join(lines) + ".", f"Total: ${ans}$."],
                  f"${ans}$.", "forgetting that values like $\\pm 1$ give only one angle per turn, while other values give two.")
    return (p, ans, [ans + 1, ans - 1, 2, 6, ans + 2], ["Treat it as a quadratic in $\\sin x$ (or $\\cos x$), then count the angles for each value."], sol)


def te3(r):
    fn = r.choice(["sin", "cos"])
    target = r.choice([30, 45, 60, 120, 135, 150, 210, 240, 300])
    k, rr = sin_exact(target) if fn == "sin" else cos_exact(target)
    val = surd(k, rr)
    sols = sorted(d for d in range(0, 360) if abs((math.sin if fn == "sin" else math.cos)(math.radians(d)) - val.key) < 1e-9)
    ans = sols[-1]
    ref = ref_angle(sols[0])
    p = f"What is the largest angle $x$ in degrees with $0^\\circ \\le x < 360^\\circ$ such that $\\{fn} x = {val.tex}$?"
    sol = explain(f"the largest angle in one turn with $\\{fn} x = {val.tex}$.", "find the reference angle from the size of the value, then find every quadrant where the sign matches.",
                  [f"$\\{fn} {ref}^\\circ = {surd(abs(k), rr).tex}$, so the reference angle is ${ref}^\\circ$.",
                   f"{'Sine' if fn == 'sin' else 'Cosine'} is {'positive' if k > 0 else 'negative'} in quadrants " + " and ".join(QUAD[d // 90] for d in sols) + ".",
                   "Solutions: " + " and ".join(f"${d}^\\circ$" for d in sols) + f". The largest is ${ans}^\\circ$."],
                  f"${ans}^\\circ$.", "stopping at the first solution you find, which is usually the smallest.")
    return (p, ans, [sols[0], 360 - sols[0] if 360 - sols[0] != ans else 180, ans - 180 if ans >= 180 else ans + 180, 180 - sols[0] if 180 - sols[0] != ans else 90, sols[0] + 90],
            ["Find the reference angle, then the quadrants where the value has the right sign."], sol)


def te4(r):
    k = r.randint(2, 8)
    fn = r.choice(["sin", "cos", "tan"])
    base = 2 if fn != "tan" else 1
    per = F(base, k)
    tex = f"\\frac{{{'' if per.numerator == 1 else per.numerator}\\pi}}{{{per.denominator}}}" if per.denominator != 1 else (f"{per.numerator}\\pi" if per.numerator != 1 else "\\pi")
    ans = C(tex, float(per) * math.pi)
    wrong = [C(f"{2 * k}\\pi", 2 * k * math.pi), C(f"\\frac{{\\pi}}{{{2 * k}}}", math.pi / (2 * k)), C(f"{k}\\pi", k * math.pi), C("2\\pi", 2 * math.pi), C(f"\\frac{{\\pi}}{{{k}}}", math.pi / k)]
    bp = "2\\pi" if base == 2 else "\\pi"
    p = f"What is the period of $y = \\{fn}({k}x)$?"
    sol = explain(f"the length of one full cycle of $\\{fn}({k}x)$.", f"$\\{fn}$ repeats every ${bp}$. Inside, ${k}x$ moves ${k}$ times as fast as $x$, so the cycle finishes ${k}$ times sooner.",
                  [f"One cycle ends when ${k}x$ has grown by ${bp}$.", f"That needs $x$ to grow by $\\frac{{{bp}}}{{{k}}} = {tex}$."],
                  f"${tex}$.", f"multiplying the period by ${k}$ instead of dividing.")
    return (p, ans, wrong, [f"The period of $\\{fn} x$ is ${'2' if base == 2 else ''}\\pi$. Multiplying $x$ by ${k}$ divides the period by ${k}$."], sol)


TEC1 = {
    "2\\sin^2 x = \\sin x": "Move everything to one side and factor: $\\sin x(2\\sin x - 1) = 0$, so $\\sin x = 0$ or $\\sin x = \\frac{1}{2}$.",
    "\\sin 2x = \\sin x": "Use $\\sin 2x = 2\\sin x\\cos x$: $2\\sin x\\cos x - \\sin x = \\sin x(2\\cos x - 1) = 0$, so $\\sin x = 0$ or $\\cos x = \\frac{1}{2}$.",
    "\\cos 2x = \\cos x": "Use $\\cos 2x = 2\\cos^2 x - 1$: $2\\cos^2 x - \\cos x - 1 = (2\\cos x + 1)(\\cos x - 1) = 0$, so $\\cos x = 1$ or $\\cos x = -\\frac{1}{2}$.",
    "\\sin 2x = \\cos x": "Use $\\sin 2x = 2\\sin x\\cos x$: $2\\sin x\\cos x - \\cos x = \\cos x(2\\sin x - 1) = 0$, so $\\cos x = 0$ or $\\sin x = \\frac{1}{2}$.",
    "2\\cos^2 x = 1 + \\sin x": "Use $\\cos^2 x = 1 - \\sin^2 x$: $2 - 2\\sin^2 x = 1 + \\sin x$, so $2\\sin^2 x + \\sin x - 1 = (2\\sin x - 1)(\\sin x + 1) = 0$, giving $\\sin x = \\frac{1}{2}$ or $\\sin x = -1$.",
    "\\tan x = \\sin x": "Write $\\tan x = \\frac{\\sin x}{\\cos x}$: $\\sin x\\left(\\frac{1}{\\cos x} - 1\\right) = 0$, so $\\sin x = 0$ or $\\cos x = 1$ (which already has $\\sin x = 0$).",
}


def tec1(r):
    expr, sols = r.choice([("2\\sin^2 x = \\sin x", [0, 30, 150, 180]), ("\\sin 2x = \\sin x", [0, 60, 180, 300]),
                           ("\\cos 2x = \\cos x", [0, 120, 240]), ("\\sin 2x = \\cos x", [30, 90, 150, 270]),
                           ("2\\cos^2 x = 1 + \\sin x", [30, 150, 270]), ("\\tan x = \\sin x", [0, 180])])
    tot = sum(sols)
    ans = C(rad_tex(tot) if tot else "0", tot / 180 * math.pi)
    wrong = [C(rad_tex(tot + 180), (tot + 180) / 180 * math.pi), C(rad_tex(max(tot - 180, 30)), max(tot - 180, 30) / 180 * math.pi),
             C(rad_tex(2 * tot) if tot else "\\pi", (2 * tot if tot else 180) / 180 * math.pi), C(rad_tex(tot + 90), (tot + 90) / 180 * math.pi)]
    p = f"What is the sum of all solutions of ${expr}$ with $0 \\le x < 2\\pi$?"
    sol = explain("the sum of every solution in one turn.", "rewrite with one angle ($x$, not $2x$), move everything to one side, and factor.",
                  [TEC1[expr], "Solutions in $[0, 2\\pi)$: " + ", ".join(f"${rad_tex(d)}$" for d in sols) + ".", "Add: $" + " + ".join(rad_tex(d) for d in sols) + f" = {ans.tex}$."],
                  f"${ans.tex}$.", "dividing both sides by $\\sin x$ (or $\\cos x$), which throws away the solutions where it equals $0$.")
    return (p, ans, wrong, ["Use a double angle identity and factor."], sol)


def tec2(r):
    k = r.randint(2, 12)
    ans = F(k, 2)
    p = f"What is the maximum value of ${k}\\sin x \\cos x$?"
    sol = explain(f"the largest value of ${k}\\sin x\\cos x$.", "the double angle formula $\\sin 2x = 2\\sin x\\cos x$ turns the product into a single sine.",
                  [f"$\\sin x\\cos x = \\frac{{1}}{{2}}\\sin 2x$, so ${k}\\sin x\\cos x = {num(ans).tex}\\sin 2x$.", "The largest value of $\\sin 2x$ is $1$ (at $x = 45^\\circ$).", f"Maximum: ${num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering ${k}$, as if $\\sin x$ and $\\cos x$ could both be $1$ at once.")
    return (p, ans, [k, F(k, 4), 2 * k, F(k, 2) + 1, 1], ["$\\sin x\\cos x = \\frac{1}{2}\\sin 2x$."], sol)


def tec3(r):
    k = r.choice([2, 3, 4, 5, 6, 8, 10])
    f = lambda x: math.sin(x) - x / (k * math.pi)
    xs = [i * 0.001 for i in range(int(-k * math.pi * 1000) - 10, int(k * math.pi * 1000) + 10)]
    cnt = 0
    for a_, b_ in zip(xs, xs[1:]):
        fa, fb = f(a_), f(b_)
        if fa == 0 or fa * fb < 0:
            cnt += 1
    mc = len([m for m in range(1, k) if 2 * m < k])
    pos = 1 + 2 * mc
    assert 2 * pos + 1 == cnt, (k, cnt, pos)
    p = f"How many real solutions does $\\sin x = \\dfrac{{x}}{{{k}\\pi}}$ have?"
    sol = explain("how many times the line $y = \\frac{x}{" + f"{k}" + "\\pi}$ meets the sine curve.", "sketch both graphs. The line is very shallow, so it crosses many humps of the sine wave before it climbs above $1$.",
                  [f"$|\\sin x| \\le 1$, so any solution needs $\\left|\\frac{{x}}{{{k}\\pi}}\\right| \\le 1$, that is, $-{k}\\pi \\le x \\le {k}\\pi$.",
                   "Both sides are odd functions, so solutions come in pairs $\\pm x$, plus $x = 0$.",
                   "For $x > 0$ the line is positive, so it can only meet the positive humps of sine: $(0, \\pi)$, $(2\\pi, 3\\pi)$, $(4\\pi, 5\\pi)$, ...",
                   f"The first hump gives $1$ crossing (sine starts above the line and ends below it). Each later hump that starts before ${k}\\pi$ gives $2$ crossings (up through the line, then back down). There {'is' if mc == 1 else 'are'} ${mc}$ such hump{'s' if mc != 1 else ''}.",
                   f"Positive solutions: $1 + 2 \\cdot {mc} = {pos}$. Total: $2 \\cdot {pos} + 1 = {cnt}$."],
                  f"${cnt}$.", "forgetting the solution $x = 0$ or the negative solutions.")
    return (p, cnt, [cnt + 1, cnt - 1, cnt + 2, 2 * k, k + 1], [f"All solutions lie between $-{k}\\pi$ and ${k}\\pi$. Count crossings of the line with each hump of the sine curve."], sol)


b.fill_unique("basics", [te1, te2, te3, te4] + MORE[b.skill_id]["basics"], 4401)
b.fill_unique("challenge", [tec1, tec2, tec3] + MORE[b.skill_id]["challenge"], 4402)


# ---------------------------------------------------------------- logarithm rules
b = bank("log_rules")


def lr1(r):
    base = r.choice([2, 3, 4, 5, 8, 9, 10, 16, 25, 27])
    e = F(r.randint(-3, 5), r.choice([1, 1, 2, 3]))
    val = base ** e
    if isinstance(val, float) or F(val).denominator > 1000 and F(val).numerator > 1000:
        return None
    try:
        v = F(base) ** e if e.denominator == 1 else None
    except Exception:
        v = None
    root = None
    if e.denominator != 1:
        root = round(base ** (1 / e.denominator))
        if root ** e.denominator != base:
            return None
        v = F(root) ** e.numerator
    p = f"What is $\\log_{{{base}}} {num(v).tex}$?"
    steps = [f"Let $y = \\log_{{{base}}} {num(v).tex}$. By definition, ${base}^y = {num(v).tex}$."]
    if root is not None:
        steps += [f"Write both sides as powers of ${root}$: ${base} = {root}^{{{e.denominator}}}$ and ${num(v).tex} = {root}^{{{e.numerator}}}$.",
                  f"So $({root}^{{{e.denominator}}})^y = {root}^{{{e.denominator}y}} = {root}^{{{e.numerator}}}$, which means ${e.denominator}y = {e.numerator}$ and $y = {num(e).tex}$."]
    else:
        steps.append(f"Check: ${base}^{{{e.numerator}}} = {num(v).tex}$" + (" (a negative exponent means one over the power)" if e < 0 else " (any nonzero number to the $0$ power is $1$)" if e == 0 else "") + f". So $y = {e.numerator}$.")
    sol = explain(f"the exponent that turns ${base}$ into ${num(v).tex}$.", "a logarithm is an exponent: $\\log_b N = y$ means $b^y = N$.", steps, f"${num(e).tex}$.",
                  "dividing the number by the base, or forgetting that fractions and roots give negative or fractional exponents.")
    return (p, e, [-e, e + 1, 1 / e if e else 2, e * 2, F(e.numerator, e.denominator + 1)], ["Ask: what power of the base gives this number?"], sol)


def lr2(r):
    base = r.choice([2, 3, 5, 6, 10])
    a = r.randint(2, 20)
    target = base ** r.randint(2, 4)
    if target % a:
        return None
    bb = target // a
    e = round(math.log(target, base))
    p = f"What is $\\log_{{{base}}} {a} + \\log_{{{base}}} {bb}$?"
    sol = explain("the sum of two logs with the same base.", "Product Rule: $\\log_b x + \\log_b y = \\log_b(xy)$. Neither log is nice alone, but the product is a power of the base.",
                  [f"Combine: $\\log_{{{base}}}({a} \\cdot {bb}) = \\log_{{{base}}} {target}$.", f"${target} = {base}^{{{e}}}$, so the value is ${e}$."],
                  f"${e}$.", f"adding the inputs, $\\log_{{{base}}}({a} + {bb})$; the rule multiplies them.")
    return (p, e, [e + 1, e - 1, a + bb, e * 2, 1], ["$\\log x + \\log y = \\log(xy)$."], sol)


def lr3(r):
    a, bb, c = r.sample([2, 3, 5, 7, 9, 16], 3)
    p = f"What is $\\log_{{{a}}} {bb} \\cdot \\log_{{{bb}}} {c} \\cdot \\log_{{{c}}} {a}$?"
    sol = explain("a product of three logs with mixed bases.", "Change of Base: $\\log_x y = \\frac{\\ln y}{\\ln x}$. Writing every log this way makes the product cancel.",
                  [f"$\\log_{{{a}}} {bb} = \\frac{{\\ln {bb}}}{{\\ln {a}}}$, $\\log_{{{bb}}} {c} = \\frac{{\\ln {c}}}{{\\ln {bb}}}$, $\\log_{{{c}}} {a} = \\frac{{\\ln {a}}}{{\\ln {c}}}$.",
                   f"Multiply: $\\frac{{\\ln {bb}}}{{\\ln {a}}} \\cdot \\frac{{\\ln {c}}}{{\\ln {bb}}} \\cdot \\frac{{\\ln {a}}}{{\\ln {c}}}$. Every top matches a bottom.", "Everything cancels, leaving $1$."],
                  "$1$.", "trying to evaluate each log as a decimal; the chain cancels exactly.")
    return (p, 1, [0, a * bb * c, -1, F(1, 2), 2], ["Change of base: $\\log_a b = \\frac{\\ln b}{\\ln a}$. Multiply and cancel."], sol)


def lr4(r):
    base = r.choice([2, 3, 10])
    m, n = r.randint(1, 5), r.randint(1, 5)
    k = r.randint(2, 4)
    ans = m * k
    p = f"What is $\\log_{{{base}}} \\left({base ** m}^{{{k}}}\\right)$?"
    sol = explain(f"$\\log_{{{base}}}$ of a power.", "Power Rule: $\\log_b(x^k) = k\\log_b x$.",
                  [f"Bring the exponent down: ${k}\\log_{{{base}}} {base ** m}$.", f"${base ** m} = {base}^{{{m}}}$, so $\\log_{{{base}}} {base ** m} = {m}$.", f"${k} \\cdot {m} = {ans}$."],
                  f"${ans}$.", "adding the exponents instead of multiplying.")
    return (p, ans, [m + k, base ** m * k, k, m, ans + 1], ["$\\log(x^k) = k\\log x$."], sol)


def lrc1(r):
    p_, q_ = r.randint(2, 8), r.randint(2, 8)
    ans = F(p_ * q_, p_ + q_)
    p = f"If $\\log_a x = {p_}$ and $\\log_b x = {q_}$, what is $\\log_{{ab}} x$?"
    sol = explain("$\\log_{ab} x$.", "the base $ab$ is a product, and logs turn products into sums only in the input. So flip every log to make $x$ the base: $\\log_u v = \\frac{1}{\\log_v u}$.",
                  [f"$\\log_x a = \\frac{{1}}{{{p_}}}$ and $\\log_x b = \\frac{{1}}{{{q_}}}$.", f"$\\log_x(ab) = \\log_x a + \\log_x b = \\frac{{1}}{{{p_}}} + \\frac{{1}}{{{q_}}} = {num(F(p_ + q_, p_ * q_)).tex}$.",
                   f"Flip back: $\\log_{{ab}} x = \\frac{{1}}{{\\log_x(ab)}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"adding ${p_} + {q_}$; when the base is a product, the logs combine through their reciprocals.")
    return (p, ans, [p_ + q_, p_ * q_, F(p_ + q_, 2), F(p_ + q_, p_ * q_), ans + 1], ["Flip each: $\\log_x a = \\frac{1}{" + str(p_) + "}$ and $\\log_x b = \\frac{1}{" + str(q_) + "}$."], sol)


def lrc2(r):
    base = r.choice([2, 3, 5])
    e = r.randint(4, 8)
    n = base ** e
    p = f"What is $\\log_{{{base}}}\\frac{{2}}{{1}} + \\log_{{{base}}}\\frac{{3}}{{2}} + \\log_{{{base}}}\\frac{{4}}{{3}} + \\cdots + \\log_{{{base}}}\\frac{{{n}}}{{{n - 1}}}$?"
    sol = explain("a long sum of logs.", "add logs by multiplying inputs; the product of the fractions telescopes.",
                  [f"Combine: $\\log_{{{base}}}\\left(\\frac{{2}}{{1}} \\cdot \\frac{{3}}{{2}} \\cdot \\frac{{4}}{{3}} \\cdots \\frac{{{n}}}{{{n - 1}}}\\right)$.", f"Each top cancels the next bottom, leaving $\\frac{{{n}}}{{1}} = {n}$.",
                   f"${n} = {base}^{{{e}}}$, so the sum is ${e}$."],
                  f"${e}$.", f"counting the terms (${n - 1}$) instead of combining them.")
    return (p, e, [e + 1, e - 1, n - 1, n, 2 * e], ["Combine into one logarithm of a product. The product telescopes."], sol)


def lrc3(r):
    k = r.randint(4, 9)
    tgt = k + 1
    if tgt & (tgt - 1):
        return None
    ans = int(math.log2(tgt))
    p = f"Suppose $2^{{a_1}} = 3$, $3^{{a_2}} = 4$, $4^{{a_3}} = 5$, and so on up to ${k}^{{a_{{{k - 1}}}}} = {k + 1}$. What is $a_1 a_2 \\cdots a_{{{k - 1}}}$?"
    sol = explain("the product of all the exponents.", "each exponent is a log, and a chain of logs telescopes under change of base.",
                  ["$a_1 = \\log_2 3$, $a_2 = \\log_3 4$, ..., and in general $a_i = \\log_{i+1}(i + 2)$.",
                   f"Change of base: $a_1 a_2 \\cdots = \\frac{{\\ln 3}}{{\\ln 2}} \\cdot \\frac{{\\ln 4}}{{\\ln 3}} \\cdots \\frac{{\\ln {k + 1}}}{{\\ln {k}}}$.",
                   f"Everything cancels except $\\frac{{\\ln {k + 1}}}{{\\ln 2}} = \\log_2 {k + 1} = {ans}$."],
                  f"${ans}$.", "trying to find each $a_i$ as a decimal.")
    return (p, ans, [ans + 1, ans - 1, k, F(k + 1, 2), k - 1], ["Write each $a_i$ as a logarithm, then use change of base."], sol)


b.fill_unique("basics", [lr1, lr2, lr3, lr4] + MORE[b.skill_id]["basics"], 4501)
b.fill_unique("challenge", [lrc1, lrc2, lrc3] + MORE[b.skill_id]["challenge"], 4502)


# ---------------------------------------------------------------- log and exponential equations
b = bank("log_equations")


def le1(r):
    base = r.choice([2, 3, 5])
    k = r.randint(1, 4)
    x = r.randint(1, 30)
    val = base ** k
    a = val - x
    p = f"Solve $\\log_{{{base}}}(x + {a}) = {k}$." if a > 0 else None
    if p is None:
        return None
    sol = explain("$x$.", "undo the log by rewriting in exponential form: $\\log_b M = k$ means $M = b^k$.",
                  [f"$x + {a} = {base}^{{{k}}} = {val}$.", f"$x = {val} - {a} = {x}$.", f"Check: $x + {a} = {val} > 0$, so the log is defined."],
                  f"${x}$.", f"computing ${base} \\cdot {k}$ instead of ${base}^{{{k}}}$.")
    return (p, x, [val, val + a, k * base - a, x + 1, x - 1], ["Rewrite in exponential form."], sol)


def le2(r):
    base = r.choice([2, 3])
    e1, e2 = r.randint(1, 5), r.randint(1, 5)
    a, bb, c = r.randint(1, 4), r.randint(-5, 5), r.randint(1, 4)
    big = base ** c
    if c == a:
        return None
    x = F(bb, c - a)
    rhs = f"{a if a > 1 else ''}x {'+' if bb >= 0 else '-'} {abs(bb)}"
    p = f"Solve ${big}^{{x}} = {base}^{{{rhs}}}$."
    sol = explain("$x$.", f"write both sides as powers of the same base, ${base}$, then set the exponents equal.",
                  [f"${big} = {base}^{{{c}}}$, so ${big}^x = {base}^{{{c}x}}$.", f"Exponents must match: ${c}x = {rhs}$.", f"${c - a}x = {bb}$, so $x = {num(x).tex}$."],
                  f"${num(x).tex}$.", f"treating ${big}^x$ as ${base}^x$ and forgetting the power of ${c}$.")
    return (p, x, [-x if x else 1, F(bb, c + a), x + 1, F(bb, a), F(c, a)], [f"Write ${big}$ as a power of ${base}$."], sol)


def le3(r):
    base = r.choice([2, 3, 10])
    x = r.randint(3, 12)
    a = r.randint(1, x - 1)
    prod = x * (x - a)
    e = math.log(prod, base)
    if abs(e - round(e)) > 1e-9:
        p = f"Solve $\\log_{{{base}}} x + \\log_{{{base}}}(x - {a}) = \\log_{{{base}}} {prod}$."
        first = f"Combine the left side: $\\log_{{{base}}}(x(x - {a})) = \\log_{{{base}}} {prod}$, so $x(x - {a}) = {prod}$."
    else:
        e = round(e)
        p = f"Solve $\\log_{{{base}}} x + \\log_{{{base}}}(x - {a}) = {e}$."
        first = f"Combine the left side: $\\log_{{{base}}}(x(x - {a})) = {e}$, so $x(x - {a}) = {base}^{{{e}}} = {prod}$."
    sol = explain("$x$.", "combine the logs with the Product Rule, solve the quadratic, and keep only solutions where every log input is positive.",
                  [first, f"$x^2 - {a}x - {prod} = 0$ factors as $(x - {x})(x + {x - a}) = 0$, so $x = {x}$ or $x = {a - x}$.",
                   f"$x = {a - x}$ is negative, and $\\log_{{{base}}} x$ needs $x > 0$. So reject it.", f"$x = {x}$ works: $x = {x}$ and $x - {a} = {x - a}$ are both positive."],
                  f"${x}$.", "keeping the negative solution of the quadratic.")
    return (p, x, [a - x, x + a, x - a, prod, x + 1], ["Combine the logs, then remember logs need positive inputs."], sol)


def le4(r):
    base = r.choice([2, 3, 5])
    v = r.randint(2, 9)
    k = r.choice([2, 3])
    ans = v ** k
    p = f"If ${base}^{{x}} = {v}$, what is ${base ** k}^{{x}}$?"
    sol = explain(f"${base ** k}^x$ without finding $x$.", f"${base ** k}$ is a power of ${base}$, so ${base ** k}^x$ is a power of ${base}^x$.",
                  [f"${base ** k} = {base}^{{{k}}}$, so ${base ** k}^x = ({base}^{{{k}}})^x = ({base}^x)^{{{k}}}$.", f"Substitute ${base}^x = {v}$: ${v}^{{{k}}} = {ans}$."],
                  f"${ans}$.", f"multiplying ${v} \\cdot {k}$ instead of raising to the power ${k}$.")
    return (p, ans, [v * k, v + k, base ** k * v, v ** (k + 1), ans + 1], [f"${base ** k} = {base}^{{{k}}}$."], sol)


def lec1(r):
    m = r.randint(1, 4)
    x_e = 6 * m
    total = F(x_e) * (1 + F(1, 2) + F(1, 3))
    p = f"If $\\log_2 x + \\log_4 x + \\log_8 x = {num(total).tex}$, what is $\\log_2 x$?"
    sol = explain("$\\log_2 x$.", "put every log in base $2$. Since $4 = 2^2$ and $8 = 2^3$, $\\log_4 x = \\frac{\\log_2 x}{2}$ and $\\log_8 x = \\frac{\\log_2 x}{3}$.",
                  ["Let $L = \\log_2 x$. The equation becomes $L + \\frac{L}{2} + \\frac{L}{3} = " + num(total).tex + "$.", f"$1 + \\frac{{1}}{{2}} + \\frac{{1}}{{3}} = \\frac{{11}}{{6}}$, so $\\frac{{11}}{{6}}L = {num(total).tex}$.",
                   f"$L = {num(total).tex} \\cdot \\frac{{6}}{{11}} = {x_e}$."],
                  f"${x_e}$.", "using $\\log_4 x = 2\\log_2 x$; the bigger base gives the smaller log.")
    return (p, x_e, [total, x_e + 1, F(total, 3), x_e // 2, x_e * 2], ["Convert each log to base 2: $\\log_4 x = \\frac{1}{2}\\log_2 x$ and $\\log_8 x = \\frac{1}{3}\\log_2 x$."], sol)


def lec2(r):
    t1, t2 = r.sample([1, 2, 4, 8, 16, 32], 2)
    k, m = t1 + t2, t1 * t2
    l1, l2 = int(math.log2(t1)), int(math.log2(t2))
    ans = l1 + l2
    p = f"What is the sum of all real solutions of $4^{{x}} - {k} \\cdot 2^{{x}} + {m} = 0$?"
    sol = explain("the sum of the solutions $x$.", "$4^x = (2^x)^2$, so substituting $t = 2^x$ gives an ordinary quadratic.",
                  [f"With $t = 2^x$: $t^2 - {k}t + {m} = 0$.", f"Factor: $(t - {t1})(t - {t2}) = 0$, so $t = {t1}$ or $t = {t2}$ (both positive, so both are allowed).",
                   f"$2^x = {t1}$ gives $x = {l1}$; $2^x = {t2}$ gives $x = {l2}$.", f"Sum: ${l1} + {l2} = {ans}$."],
                  f"${ans}$.", f"adding the $t$ values (${k}$) instead of the $x$ values.")
    return (p, ans, [k, int(math.log2(m)) + 1, ans + 1, ans - 1 if ans else 2, m], ["Let $t = 2^x$. Then the product of the two values of $t$ is " + str(m) + "."], sol)


def lec3(r):
    k = r.randint(1, 3)
    ans = 6 ** k
    p = f"What positive number $x \\ne 1$ satisfies $\\dfrac{{\\log_2 x \\cdot \\log_3 x}}{{\\log_2 x + \\log_3 x}} = {k}$?"
    sol = explain("$x$.", "flipping the fraction splits it into two simple pieces, and $\\frac{1}{\\log_2 x} = \\log_x 2$.",
                  [f"Flip both sides: $\\frac{{\\log_2 x + \\log_3 x}}{{\\log_2 x \\cdot \\log_3 x}} = \\frac{{1}}{{{k}}}$.", "Split: $\\frac{1}{\\log_3 x} + \\frac{1}{\\log_2 x} = \\log_x 3 + \\log_x 2$.",
                   f"Combine: $\\log_x 6 = \\frac{{1}}{{{k}}}$, so $x^{{1/{k}}} = 6$ and $x = 6^{{{k}}} = {ans}$."],
                  f"${ans}$.", "trying to solve with decimals; the flip makes it exact.")
    return (p, ans, [5 ** k, 6 ** (k + 1), 2 ** k * 3, 36 ** k if k < 3 else 6 ** k + 6, ans // 2], ["Flip both sides of the equation."], sol)


b.fill_unique("basics", [le1, le2, le3, le4] + MORE[b.skill_id]["basics"], 4601)
b.fill_unique("challenge", [lec1, lec2, lec3] + MORE[b.skill_id]["challenge"], 4602)


# ---------------------------------------------------------------- change of base and digits
b = bank("log_change_base")


def lcb1(r):
    a = r.choice([2, 3, 5])
    k1, k2 = r.randint(1, 6), r.randint(1, 6)
    if k1 == k2:
        return None
    x, y = a ** k1, a ** k2
    ans = F(k1, k2)
    p = f"What is $\\log_{{{y}}} {x}$?"
    sol = explain(f"$\\log_{{{y}}} {x}$.", f"both numbers are powers of ${a}$, so change to base ${a}$.",
                  [f"${x} = {a}^{{{k1}}}$ and ${y} = {a}^{{{k2}}}$.", f"$\\log_{{{y}}} {x} = \\frac{{\\log_{{{a}}} {x}}}{{\\log_{{{a}}} {y}}} = \\frac{{{k1}}}{{{k2}}} = {num(ans).tex}$.",
                   f"Check: ${y}^{{{num(ans).tex}}} = ({a}^{{{k2}}})^{{{num(ans).tex}}} = {a}^{{{k1}}} = {x}$."],
                  f"${num(ans).tex}$.", "flipping the fraction; the input's exponent goes on top.")
    return (p, ans, [1 / ans, F(k1 - k2), F(x, y), ans + 1, F(k1, k1 + k2)], [f"Write both numbers as powers of ${a}$."], sol)


def lcb2(r):
    base = r.choice([2, 3, 5, 7])
    n = r.randint(20, 120)
    d = len(str(base ** n))
    lg = {2: "0.3010", 3: "0.4771", 5: "0.6990", 7: "0.8451"}[base]
    p = f"Using $\\log_{{10}} {base} \\approx {lg}$, how many digits does ${base}^{{{n}}}$ have?"
    sol = explain(f"the number of digits of ${base}^{{{n}}}$.", "a number with $d$ digits is between $10^{d-1}$ and $10^d$, so its $\\log_{10}$ is between $d - 1$ and $d$. Digits $= \\lfloor \\log_{10} N \\rfloor + 1$.",
                  [f"$\\log_{{10}} {base}^{{{n}}} = {n}\\log_{{10}} {base} \\approx {n} \\cdot {lg} = {n * float(lg):.2f}$.", f"So $10^{{{d - 1}}} < {base}^{{{n}}} < 10^{{{d}}}$.", f"The number of digits is ${d - 1} + 1 = {d}$."],
                  f"${d}$.", "forgetting the $+1$; $10^2 = 100$ has $3$ digits, not $2$.")
    return (p, d, [d + 1, d - 1, n, int(n * float(lg)), d + 2], ["A positive integer $N$ has $\\lfloor \\log_{10} N \\rfloor + 1$ digits."], sol)


def lcb3(r):
    k = r.randint(2, 6)
    ask = r.choice(["inv", "sq"])
    if ask == "inv":
        p = f"If $\\log_a b = {k}$, what is $\\log_b a$?"
        ans = F(1, k)
        steps = ["Change of base: $\\log_a b = \\frac{\\ln b}{\\ln a}$ and $\\log_b a = \\frac{\\ln a}{\\ln b}$.", "These are reciprocals, so $\\log_b a = \\frac{1}{\\log_a b}$.", f"$\\log_b a = \\frac{{1}}{{{k}}}$."]
        trap = "answering $-k$; switching base and input flips the fraction, not the sign."
    else:
        p = f"If $\\log_a b = {k}$, what is $\\log_{{a^2}} b^3$?"
        ans = F(3 * k, 2)
        steps = ["Change to base $a$: $\\log_{a^2} b^3 = \\frac{\\log_a b^3}{\\log_a a^2}$.", "Power Rule: top $= 3\\log_a b$, bottom $= 2$.", f"$\\frac{{3 \\cdot {k}}}{{2}} = {num(ans).tex}$."]
        trap = "multiplying by $2$ for the base; a power on the base divides."
    sol = explain("a log with the base and input changed.", "rewrite with change of base so the given $\\log_a b$ appears.", steps, f"${num(ans).tex}$.", trap)
    return (p, ans, [k, -k, F(k, 2), 2 * k, ans + 1], ["Use change of base."], sol)


def lcb4(r):
    n = r.choice([12, 18, 24, 36, 48, 54, 72, 96, 108])
    e2, e3 = 0, 0
    m = n
    while m % 2 == 0:
        e2 += 1
        m //= 2
    while m % 3 == 0:
        e3 += 1
        m //= 3
    if m != 1:
        return None
    p = f"If $\\log_{{10}} 2 = a$ and $\\log_{{10}} 3 = b$, then $\\log_{{10}} {n} = pa + qb$ for integers $p$ and $q$. What is $p + q$?"
    sol = explain("$p + q$.", f"factor ${n}$ into $2$s and $3$s, then use the Product and Power Rules.",
                  [f"${n} = 2^{{{e2}}} \\cdot 3^{{{e3}}}$.", f"$\\log_{{10}} {n} = {e2}\\log_{{10}} 2 + {e3}\\log_{{10}} 3 = {e2}a + {e3}b$.", f"$p + q = {e2} + {e3} = {e2 + e3}$."],
                  f"${e2 + e3}$.", "multiplying the exponents instead of adding them.")
    return (p, e2 + e3, [e2 * e3, e2, e3, e2 + e3 + 1, n // 6], [f"Factor ${n}$ into powers of 2 and 3."], sol)


def lcbc1(r):
    k = r.randint(3, 8)
    ans = k * k - 2
    p = f"If $\\log_a b + \\log_b a = {k}$, what is $(\\log_a b)^2 + (\\log_b a)^2$?"
    sol = explain("the sum of squares.", "$\\log_b a = \\frac{1}{\\log_a b}$, so this is the classic $t + \\frac{1}{t}$ setup: square it.",
                  [f"Let $t = \\log_a b$. Then $t + \\frac{{1}}{{t}} = {k}$.", f"Square: $t^2 + 2 + \\frac{{1}}{{t^2}} = {k * k}$ (the middle term is $2 \\cdot t \\cdot \\frac{{1}}{{t}} = 2$).", f"$t^2 + \\frac{{1}}{{t^2}} = {k * k} - 2 = {ans}$."],
                  f"${ans}$.", f"answering ${k}^2 = {k * k}$ and forgetting the middle term $2$.")
    return (p, ans, [k * k, k * k + 2, 2 * k, ans - 1, k * k - 1], ["Let $t = \\log_a b$. Then $\\log_b a = \\frac{1}{t}$."], sol)


def lcbc2(r):
    base = r.choice([2, 3, 4])
    lo, hi = r.randint(1, 4), r.randint(5, 8)
    cnt = base ** hi - base ** lo
    p = f"How many positive integers $n$ satisfy ${lo} \\le \\log_{{{base}}} n < {hi}$?"
    sol = explain("a count of integers in a log range.", f"$\\log_{{{base}}}$ is increasing, so raise ${base}$ to each part of the inequality.",
                  [f"${base}^{{{lo}}} \\le n < {base}^{{{hi}}}$, that is, ${base ** lo} \\le n < {base ** hi}$.", f"The integers are ${base ** lo}, {base ** lo + 1}, \\ldots, {base ** hi - 1}$.", f"Count: ${base ** hi - 1} - {base ** lo} + 1 = {cnt}$."],
                  f"${cnt}$.", "an off by one error at the ends: the left end is included, the right end is not.")
    return (p, cnt, [cnt + 1, cnt - 1, base ** hi, hi - lo, base ** (hi - lo)], ["Rewrite the inequality without logarithms."], sol)


def lcbc3(r):
    base = r.choice([2, 3, 5, 7])
    n = r.randint(100, 100000)
    ans = int(math.floor(math.log(n, base) + 1e-12))
    if base ** ans > n or base ** (ans + 1) <= n:
        ans = max(k for k in range(0, 40) if base ** k <= n)
    p = f"What is the greatest integer less than or equal to $\\log_{{{base}}} {n}$?"
    sol = explain(f"$\\lfloor \\log_{{{base}}} {n} \\rfloor$.", f"$\\log_{{{base}}} {n}$ is between $k$ and $k + 1$ exactly when ${n}$ is between ${base}^k$ and ${base}^{{k+1}}$. So find the powers of ${base}$ around ${n}$.",
                  [f"Powers of ${base}$: " + ", ".join(f"${base}^{{{j}}} = {base ** j}$" for j in range(max(0, ans - 2), ans + 2)) + ".", f"${base ** ans} \\le {n} < {base ** (ans + 1)}$.",
                   f"So ${ans} \\le \\log_{{{base}}} {n} < {ans + 1}$, and the floor is ${ans}$."],
                  f"${ans}$.", "counting the digits of the number, which only works for base $10$.")
    return (p, ans, [ans + 1, ans - 1, len(str(n)), ans + 2, ans - 2], [f"Find the largest power of ${base}$ that is at most ${n}$."], sol)


b.fill_unique("basics", [lcb1, lcb2, lcb3, lcb4] + MORE[b.skill_id]["basics"], 4701)
b.fill_unique("challenge", [lcbc1, lcbc2, lcbc3] + MORE[b.skill_id]["challenge"], 4702)


# ---------------------------------------------------------------- complex arithmetic
b = bank("cx_arithmetic")


def ctex(z):
    a, bb = F(z.real).limit_denominator(1000), F(z.imag).limit_denominator(1000)
    if bb == 0:
        return num(a).tex
    if a == 0:
        bt = "" if abs(bb) == 1 else num(abs(bb)).tex
        return ("-" if bb < 0 else "") + bt + "i"
    bt = "" if abs(bb) == 1 else num(abs(bb)).tex
    return f"{num(a).tex} {'+' if bb > 0 else '-'} {bt}i"


def zc(z, key=None):
    return C(ctex(z), key if key is not None else (z.real * 1000 + z.imag))


def pr(v):
    return f"({v})" if v < 0 else str(v)


def cxa1(r):
    a, bb, c, d = [r.randint(-6, 6) for _ in range(4)]
    if bb == 0 or d == 0:
        return None
    z = complex(a, bb) * complex(c, d)
    p = f"What is $({ctex(complex(a, bb))})({ctex(complex(c, d))})$?"
    wrong = [complex(a * c + bb * d, a * d + bb * c), complex(a * c, bb * d), complex(a * c - bb * d, a * d - bb * c), z.conjugate(), z + 1]
    wrong = [w for w in wrong if w != z]
    sol = explain("the product in the form $x + yi$.", "multiply like two binomials (FOIL), then replace $i^2$ with $-1$.",
                  [f"Terms: ${pr(a)} \\cdot {pr(c)} = {a * c}$, ${pr(a)} \\cdot {pr(d)}i = {a * d}i$, ${pr(bb)}i \\cdot {pr(c)} = {bb * c}i$, ${pr(bb)}i \\cdot {pr(d)}i = {bb * d}i^2$.",
                   f"$i^2 = -1$, so the last term is ${-bb * d}$.", f"Real part: ${a * c} + {pr(-bb * d)} = {a * c - bb * d}$. Imaginary part: ${a * d} + {pr(bb * c)} = {a * d + bb * c}$.", f"Product: ${ctex(z)}$."],
                  f"${ctex(z)}$.", "treating $i^2$ as $+1$, or multiplying only the real parts and the imaginary parts.")
    return (p, zc(z), [zc(w) for w in wrong], ["Expand and use $i^2 = -1$."], sol, False)


def cxa2(r):
    n = r.randint(10, 2030)
    vals = {0: "1", 1: "i", 2: "-1", 3: "-i"}
    ans = vals[n % 4]
    ch = [text_choice(f"${vals[k]}$", k) for k in range(4) if vals[k] != ans] + [text_choice("$0$", 9)]
    p = f"What is $i^{{{n}}}$?"
    sol = explain(f"$i^{{{n}}}$.", "powers of $i$ cycle with period $4$: $i^1 = i$, $i^2 = -1$, $i^3 = -i$, $i^4 = 1$, then it repeats.",
                  [f"Divide ${n}$ by $4$: ${n} = 4 \\cdot {n // 4} + {n % 4}$.", f"$i^{{{n}}} = (i^4)^{{{n // 4}}} \\cdot i^{{{n % 4}}} = 1 \\cdot i^{{{n % 4}}}$.", f"$i^{{{n % 4}}} = {ans}$."],
                  f"${ans}$.", "using the remainder after dividing by $2$ instead of $4$.")
    return (p, text_choice(f"${ans}$", 10 + n % 4), ch, ["Powers of $i$ repeat every 4."], sol, False)


def cxa3(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15)])
    s1, s2 = r.choice([1, -1]), r.choice([1, -1])
    z = complex(s1 * a, s2 * bb)
    p = f"What is $|{ctex(z)}|$?"
    sol = explain("the modulus (distance from $0$ in the complex plane).", "$|x + yi| = \\sqrt{x^2 + y^2}$, the Pythagorean distance to the point $(x, y)$.",
                  [f"$x = {s1 * a}$ and $y = {s2 * bb}$.", f"$\\sqrt{{{pr(s1 * a)}^2 + {pr(s2 * bb)}^2}} = \\sqrt{{{a * a} + {bb * bb}}} = \\sqrt{{{c * c}}} = {c}$."],
                  f"${c}$.", "adding the parts, or keeping a minus sign; squaring removes signs.")
    return (p, c, [a + bb, c * c, c + 1, abs(a - bb), c - 1], ["$|a + bi| = \\sqrt{a^2 + b^2}$."], sol)


def cxa4(r):
    c, d = r.randint(1, 5), r.randint(1, 5)
    q = complex(r.randint(-5, 5), r.randint(-5, 5))
    if q.imag == 0:
        return None
    w = complex(c, d)
    z = q * w
    p = f"What is $\\dfrac{{{ctex(z)}}}{{{ctex(w)}}}$?"
    wrong = [q.conjugate(), -q, q + 1, complex(q.imag, q.real)]
    wrong = [x for x in wrong if x != q]
    m2 = c * c + d * d
    top = z * w.conjugate()
    sol = explain("the quotient in the form $x + yi$.", "multiply the top and bottom by the conjugate of the bottom. That makes the bottom real: $(c + di)(c - di) = c^2 + d^2$.",
                  [f"Conjugate of ${ctex(w)}$ is ${ctex(w.conjugate())}$.", f"Bottom: ${c}^2 + {d}^2 = {m2}$.", f"Top: $({ctex(z)})({ctex(w.conjugate())}) = {ctex(top)}$.",
                   f"Divide each part by ${m2}$: $\\frac{{{ctex(top)}}}{{{m2}}} = {ctex(q)}$."],
                  f"${ctex(q)}$.", "dividing real part by real part and imaginary by imaginary; division doesn't work part by part.")
    return (p, zc(q), [zc(x) for x in wrong], ["Multiply the top and bottom by the conjugate of the denominator."], sol, False)


def cxac1(r):
    x, y = r.randint(-6, 6), r.randint(-6, 6)
    k = r.choice([2, 3])
    rhs = complex((1 + k) * x, (1 - k) * y)
    ans = x * x + y * y
    p = f"A complex number $z$ satisfies $z + {k}\\overline{{z}} = {ctex(rhs)}$. What is $|z|^2$?"
    sol = explain("$|z|^2$.", "write $z = x + yi$, so $\\overline{z} = x - yi$. Then match real parts and imaginary parts separately.",
                  [f"$z + {k}\\overline{{z}} = (x + yi) + {k}(x - yi) = {1 + k}x + ({1 - k})yi$.", f"Real parts: ${1 + k}x = {(1 + k) * x}$, so $x = {x}$.",
                   f"Imaginary parts: ${1 - k}y = {(1 - k) * y}$, so $y = {y}$.", f"$|z|^2 = x^2 + y^2 = {x * x} + {y * y} = {ans}$."],
                  f"${ans}$.", "forgetting that the conjugate flips the sign of the imaginary part.")
    return (p, ans, [ans + 1, x * x - y * y if x * x - y * y != ans else ans + 2, abs(x) + abs(y), int(abs(rhs) ** 2) if int(abs(rhs) ** 2) != ans else ans * 2, ans - 1],
            ["Write $z = x + yi$ and match real and imaginary parts."], sol)


def cxac2(r):
    n = r.randint(10, 300)
    s = sum(1j ** k for k in range(1, n + 1))
    s = complex(round(s.real), round(s.imag))
    options = {"0": 0, "i": 1j, "-1": -1, "i - 1": -1 + 1j, "-i": -1j, "1": 1}
    ans_t = next(t for t, v in options.items() if v == s)
    ch = [text_choice(f"${t}$", k) for k, t in enumerate(options) if t != ans_t][:4]
    left = n % 4
    lt = ["i", "-1", "-i"][:left]
    p = f"What is $i + i^2 + i^3 + \\cdots + i^{{{n}}}$?"
    sol = explain("the sum of the first " + f"${n}$ powers of $i$.", "every four consecutive powers are $i, -1, -i, 1$ in some rotation, and those add to $0$.",
                  [f"${n} = 4 \\cdot {n // 4} + {left}$: that is ${n // 4}$ full blocks of four, worth $0$ each.",
                   (f"The ${left}$ leftover term{'s' if left != 1 else ''} are $i^{{{n - left + 1}}}, \\ldots, i^{{{n}}}$, which equal $" + ", ".join(lt) + "$." if left else "There are no leftover terms."),
                   (f"Their sum: $" + " + ".join(lt).replace("+ -", "- ") + f" = {ans_t}$." if left else "So the whole sum is $0$.")],
                  f"${ans_t}$.", "forgetting that the sum starts at $i^1$, not $i^0$.")
    return (p, text_choice(f"${ans_t}$", 99), ch, ["Every block of 4 consecutive powers of $i$ adds to $0$."], sol, False)


def cxac3(r):
    a, bb = r.randint(1, 8), r.randint(1, 8)
    ans = 2 * (a * a + bb * bb)
    p = f"Let $z = {ctex(complex(a, bb))}$. What is the area of the square in the complex plane with vertices $z$, $iz$, $-z$, and $-iz$?"
    sol = explain("the area of the square.", "multiplying by $i$ rotates a point $90^\\circ$ around $0$. So the four points are $z$ rotated by $0^\\circ, 90^\\circ, 180^\\circ, 270^\\circ$: a square centered at $0$.",
                  [f"Each vertex is $|z| = \\sqrt{{{a}^2 + {bb}^2}} = \\sqrt{{{a * a + bb * bb}}}$ from the center.", f"$z$ and $-z$ are opposite corners, so a diagonal is $2|z|$, and diagonal$^2 = 4 \\cdot {a * a + bb * bb} = {4 * (a * a + bb * bb)}$.",
                   f"A square's area is $\\frac{{\\text{{diagonal}}^2}}{{2}} = \\frac{{{4 * (a * a + bb * bb)}}}{{2}} = {ans}$."],
                  f"${ans}$.", "treating $|z|$ as the side length; it is half the diagonal.")
    return (p, ans, [a * a + bb * bb, 4 * (a * a + bb * bb), ans + 2, (a + bb) ** 2, 2 * a * bb], ["Multiplying by $i$ rotates by $90^\\circ$, so the vertices form a square centered at $0$."], sol)


b.fill_unique("basics", [cxa1, cxa2, cxa3, cxa4] + MORE[b.skill_id]["basics"], 4801)
b.fill_unique("challenge", [cxac1, cxac2, cxac3] + MORE[b.skill_id]["challenge"], 4802)


# ---------------------------------------------------------------- polar form and De Moivre
b = bank("cx_polar")


def cp1(r):
    n = r.randint(2, 16)
    z = (1 + 1j) ** n
    z = complex(round(z.real), round(z.imag))
    p = f"What is $(1 + i)^{{{n}}}$?"
    wrong = [complex(2 ** n, 0), complex(z.imag, z.real) if z.imag != z.real else z + 2, -z, complex(2 ** (n // 2), 2 ** (n // 2)), z.conjugate()]
    wrong = [w for w in wrong if w != z]
    ang = 45 * n % 360
    mag = surd(1, 2 ** n)
    sol = explain(f"$(1 + i)^{{{n}}}$.", "De Moivre's Theorem: in polar form, raising to the $n$th power raises the length to the $n$th power and multiplies the angle by $n$.",
                  ["$1 + i$ has length $\\sqrt{1^2 + 1^2} = \\sqrt{2}$ and angle $45^\\circ$.", f"Length: $(\\sqrt{{2}})^{{{n}}} = {mag.tex}$. Angle: ${n} \\cdot 45^\\circ = {45 * n}^\\circ$" + (f", which is the same direction as ${ang}^\\circ$." if 45 * n != ang else "."),
                   f"A length of ${mag.tex}$ at ${ang}^\\circ$ is the point ${ctex(z)}$."],
                  f"${ctex(z)}$.", f"computing $1^{{{n}}} + i^{{{n}}}$; powers don't distribute over addition.")
    return (p, zc(z), [zc(w) for w in wrong], ["$1 + i = \\sqrt{2}\\,(\\cos 45^\\circ + i\\sin 45^\\circ)$."], sol, False)


def cp2(r):
    d = r.choice([30, 45, 60, 90, 120, 135, 150, 210, 225, 240, 270, 300, 315, 330])
    a, bb = r.choice([(1, 1), (2, 2), (1, 3), (3, 3)]) if d % 90 else (1, 1)
    examples = {45: (1, 1), 135: (-1, 1), 225: (-1, -1), 315: (1, -1), 90: (0, 1), 270: (0, -1)}
    if d not in examples:
        return None
    x, y = examples[d]
    k = r.randint(1, 5)
    z = complex(x * k, y * k)
    p = f"What is the argument (angle in degrees, from $0^\\circ$ to $360^\\circ$) of ${ctex(z)}$?"
    if x == 0:
        steps = [f"${ctex(z)}$ is the point $(0, {y * k})$, on the {'positive' if y > 0 else 'negative'} imaginary axis.", f"That direction is ${d}^\\circ$ from the positive real axis."]
    else:
        steps = [f"${ctex(z)}$ is the point $({x * k}, {y * k})$, in the {QUAD[d // 90]} quadrant.", f"Its real and imaginary parts have equal size, so it makes a $45^\\circ$ angle with the real axis.", f"In the {QUAD[d // 90]} quadrant that direction is ${d}^\\circ$."]
    sol = explain("the angle of the point, measured counterclockwise from the positive real axis.", "plot the point $(\\text{real}, \\text{imaginary})$ and read off its direction.", steps, f"${d}^\\circ$.", "using $\\tan^{-1}\\frac{y}{x}$ directly, which gives the wrong quadrant when $x < 0$.")
    return (p, d, [(d + 180) % 360, (d + 90) % 360, 360 - d if 360 - d != d else 0, 45 if d != 45 else 135, (d + 270) % 360], ["Plot the point and measure the angle from the positive real axis."], sol)


def cp3(r):
    a, bb, c = r.choice([(3, 4, 5), (1, 1, None), (5, 12, 13), (2, 2, None)])
    n = r.randint(2, 6)
    if c is None:
        val2 = a * a + bb * bb
        mod_n = F(val2) ** n
        ans = surd(1, int(mod_n)) if n % 2 else num(int(round(float(mod_n) ** 0.5)))
    else:
        ans = num(c ** n)
    p = f"What is $|({ctex(complex(a, bb))})^{{{n}}}|$?"
    sol = explain("the length of a power.", "lengths multiply when complex numbers multiply, so $|z^n| = |z|^n$. No need to expand.",
                  [f"$|{ctex(complex(a, bb))}| = \\sqrt{{{a}^2 + {bb}^2}} = \\sqrt{{{a * a + bb * bb}}}" + (f" = {c}$." if c else "$."), f"$|z|^{{{n}}} = \\left(\\sqrt{{{a * a + bb * bb}}}\\right)^{{{n}}} = {ans.tex}$."],
                  f"${ans.tex}$.", "expanding the power by hand, which is slow and easy to get wrong.")
    return (p, ans, [num((a + bb) ** n), num(c * n if c else n * 2), num((c or 2) ** (n - 1)), num((c or 2) ** (n + 1)), num(a ** n + bb ** n)], ["$|z^n| = |z|^n$."], sol)


def cp4(r):
    r1, r2 = r.randint(2, 6), r.randint(2, 6)
    a, bb = r.choice([30, 45, 60, 90, 120, 150]), r.choice([30, 45, 60, 90, 120, 150])
    ang = (a + bb) % 360
    p = f"If $z = {r1}(\\cos {a}^\\circ + i\\sin {a}^\\circ)$ and $w = {r2}(\\cos {bb}^\\circ + i\\sin {bb}^\\circ)$, then $zw = R(\\cos\\theta + i\\sin\\theta)$ with $R > 0$ and $0^\\circ \\le \\theta < 360^\\circ$. What is $R + \\theta$?"
    ans = r1 * r2 + ang
    sol = explain("$R + \\theta$ for the product.", "in polar form, multiplying complex numbers multiplies their lengths and adds their angles.",
                  [f"$R = {r1} \\cdot {r2} = {r1 * r2}$.", f"$\\theta = {a}^\\circ + {bb}^\\circ = {ang}^\\circ$.", f"$R + \\theta = {r1 * r2} + {ang} = {ans}$."],
                  f"${ans}$.", "adding the lengths or multiplying the angles; it's the other way around.")
    return (p, ans, [r1 + r2 + ang, r1 * r2 + a * bb % 360, r1 * r2 + abs(a - bb), ans + 90, ans - 30], ["Multiply the lengths and add the angles."], sol)


def cpc1(r):
    d = r.choice([15, 18, 20, 24, 30, 36, 40, 45, 48, 60, 72, 75, 80, 105, 135, 150])
    ask = r.choice(["one", "real"])
    if ask == "one":
        n = 360 // math.gcd(360, d)
        g = math.gcd(360, d)
        p = f"What is the smallest positive integer $n$ such that $(\\cos {d}^\\circ + i\\sin {d}^\\circ)^n = 1$?"
        steps = [f"By De Moivre, the power is $\\cos({d}n)^\\circ + i\\sin({d}n)^\\circ$.", f"This equals $1$ exactly when ${d}n$ is a multiple of $360$.",
                 f"$\\gcd({d}, 360) = {g}$, so we need ${d // g}n$ to be a multiple of ${360 // g}$. Since ${d // g}$ and ${360 // g}$ share no factor, $n = {n}$."]
    else:
        n = 180 // math.gcd(180, d)
        g = math.gcd(180, d)
        p = f"What is the smallest positive integer $n$ such that $(\\cos {d}^\\circ + i\\sin {d}^\\circ)^n$ is a real number?"
        steps = [f"By De Moivre, the power is $\\cos({d}n)^\\circ + i\\sin({d}n)^\\circ$.", f"It is real when $\\sin({d}n)^\\circ = 0$, that is, when ${d}n$ is a multiple of $180$.",
                 f"$\\gcd({d}, 180) = {g}$, so we need ${d // g}n$ to be a multiple of ${180 // g}$. Since they share no factor, $n = {n}$."]
    sol = explain("the smallest power that lands on the target.", "a number of length $1$ at angle $\\theta$, raised to the $n$th power, sits at angle $n\\theta$.", steps, f"${n}$.",
                  f"answering $\\frac{{360}}{{{d}}}$ even when it isn't a whole number.")
    return (p, n, [n * 2, n // 2 if n % 2 == 0 and n // 2 > 0 else n + 1, 360 // d if 360 % d == 0 and 360 // d != n else n + 3, d, n + 1], ["By De Moivre, the power multiplies the angle by $n$."], sol)


def cpc2(r):
    n = r.randint(2, 12)
    z = (complex(math.sqrt(3), 1)) ** n
    re_ = round(z.real)
    if abs(z.real - re_) > 1e-6:
        k = round(z.real / math.sqrt(3))
        if abs(k * math.sqrt(3) - z.real) > 1e-6:
            return None
        ans = surd(k, 3)
    else:
        ans = num(re_)
    ang = 30 * n % 360
    ck, cr = cos_exact(ang)
    p = f"What is the real part of $(\\sqrt{{3}} + i)^{{{n}}}$?"
    sol = explain("the real part of a large power.", "switch to polar form and use De Moivre's Theorem; the real part is length times cosine.",
                  ["$\\sqrt{3} + i$ has length $\\sqrt{3 + 1} = 2$ and angle $30^\\circ$ (since $\\tan\\theta = \\frac{1}{\\sqrt{3}}$).",
                   f"Power: length $2^{{{n}}} = {2 ** n}$, angle ${n} \\cdot 30^\\circ = {30 * n}^\\circ$" + (f", same direction as ${ang}^\\circ$." if 30 * n != ang else "."),
                   f"Real part: ${2 ** n} \\cos {ang}^\\circ = {2 ** n} \\cdot {surd(ck, cr).tex} = {ans.tex}$."],
                  f"${ans.tex}$.", "using the sine instead of the cosine for the real part.")
    return (p, ans, [num(2 ** n), num(-(2 ** n)), num(2 ** (n - 1)), num(0) if ans.key != 0 else num(1), surd(2 ** (n - 1), 3) if ans.tex != surd(2 ** (n - 1), 3).tex else num(-(2 ** (n - 1)))],
            ["$\\sqrt{3} + i = 2(\\cos 30^\\circ + i\\sin 30^\\circ)$."], sol)


def cpc3(r):
    d = r.choice([20, 30, 36, 40, 45, 60, 72])
    n = r.randint(2, 12)
    val = 2 * math.cos(math.radians(n * d))
    opts = {2: num(2), -2: num(-2), 1: num(1), -1: num(-1), 0: num(0), math.sqrt(3): surd(1, 3), -math.sqrt(3): surd(-1, 3), math.sqrt(2): surd(1, 2), -math.sqrt(2): surd(-1, 2)}
    best = min(opts, key=lambda k: abs(k - val))
    if abs(best - val) > 1e-9:
        return None
    ans = opts[best]
    ang = n * d % 360
    p = f"A complex number $z$ satisfies $z + \\dfrac{{1}}{{z}} = 2\\cos {d}^\\circ$. What is $z^{{{n}}} + \\dfrac{{1}}{{z^{{{n}}}}}$?"
    sol = explain(f"$z^{{{n}}} + z^{{-{n}}}$.", "if $z = \\cos\\theta + i\\sin\\theta$, then $\\frac{1}{z} = \\cos\\theta - i\\sin\\theta$ and $z + \\frac{1}{z} = 2\\cos\\theta$. The same pattern holds for every power.",
                  [f"Solving the quadratic $z^2 - 2\\cos {d}^\\circ \\, z + 1 = 0$ gives $z = \\cos {d}^\\circ \\pm i\\sin {d}^\\circ$.",
                   f"De Moivre: $z^{{{n}}} = \\cos {n * d}^\\circ \\pm i\\sin {n * d}^\\circ$ and $z^{{-{n}}} = \\cos {n * d}^\\circ \\mp i\\sin {n * d}^\\circ$. The sines cancel.",
                   f"So $z^{{{n}}} + z^{{-{n}}} = 2\\cos {n * d}^\\circ" + (f" = 2\\cos {ang}^\\circ" if n * d != ang else "") + f" = {ans.tex}$."],
                  f"${ans.tex}$.", f"raising $2\\cos {d}^\\circ$ to the ${n}$th power; the factor $2$ stays outside.")
    return (p, ans, [v for k, v in opts.items() if k != best][:5], ["Then $z = \\cos " + str(d) + "^\\circ \\pm i\\sin " + str(d) + "^\\circ$. Use De Moivre."], sol)


b.fill_unique("basics", [cp1, cp2, cp3, cp4] + MORE[b.skill_id]["basics"], 4901)
b.fill_unique("challenge", [cpc1, cpc2, cpc3] + MORE[b.skill_id]["challenge"], 4902)


# ---------------------------------------------------------------- roots of unity
b = bank("cx_roots_unity")


def ru1(r):
    n = r.randint(3, 12)
    ask = r.choice(["sum", "count", "product"])
    if ask == "sum":
        p = f"What is the sum of all the complex solutions of $z^{{{n}}} = 1$?"
        ans = 0
        steps = [f"The solutions are the roots of $z^{{{n}}} - 1 = 0$.", f"Vieta: the sum of the roots is $-\\frac{{\\text{{coefficient of }} z^{{{n - 1}}}}}{{\\text{{leading coefficient}}}}$.", f"There is no $z^{{{n - 1}}}$ term, so that coefficient is $0$ and the sum is $0$.",
                 "Picture: the roots are evenly spaced around a circle, so they balance at the center."]
        wrong = [1, n, -1, n - 1]
        trap = f"answering ${n}$ by adding the lengths instead of the complex numbers."
    elif ask == "count":
        k = r.randint(1, 50)
        p = f"How many complex numbers $z$ satisfy $z^{{{n}}} = {k}$?"
        ans = n
        steps = [f"$z^{{{n}}} - {k} = 0$ is a polynomial equation of degree ${n}$, so it has ${n}$ roots counted with multiplicity.",
                 f"They are all different: they have the same length $\\sqrt[{n}]{{{k}}}$ and angles spaced $\\frac{{360^\\circ}}{{{n}}}$ apart."]
        wrong = [1, 2, n - 1, n + 1]
        trap = "counting only the real solutions."
    else:
        ans = (-1) ** (n + 1)
        p = f"What is the product of all the complex solutions of $z^{{{n}}} = 1$?"
        steps = [f"The solutions are the roots of $z^{{{n}}} - 1 = 0$.", f"Vieta: the product of the roots of a degree ${n}$ monic polynomial is $(-1)^{{{n}}}$ times the constant term.", f"$(-1)^{{{n}}} \\cdot (-1) = {ans}$."]
        wrong = [0, n, -ans, 2]
        trap = "forgetting the $(-1)^n$ sign in Vieta's product formula."
    sol = explain("a fact about all the roots of $z^n = \\text{constant}$.", "treat the equation as a polynomial and use the Fundamental Theorem of Algebra and Vieta's formulas.", steps, f"${ans}$.", trap)
    return (p, ans, wrong, ["Use Vieta's formulas on $z^n - 1 = 0$."], sol)


def ru2(r):
    a, bb = r.randint(10, 200), r.randint(10, 200)
    w = cmath.exp(2j * math.pi / 3)
    val = w ** a + w ** bb
    canon = {"2": 2, "-1": -1, "2\\omega": 2 * w, "2\\omega^2": 2 * w * w, "-\\omega": -w, "-\\omega^2": -w * w}
    best = min(canon, key=lambda t: abs(canon[t] - val))
    if abs(canon[best] - val) > 1e-9:
        return None
    ra, rb = sorted((a % 3, bb % 3))
    pw = lambda e: "1" if e == 0 else "\\omega" if e == 1 else "\\omega^2"
    simp = {(0, 0): "$1 + 1 = 2$.", (1, 1): "$\\omega + \\omega = 2\\omega$.", (2, 2): "$\\omega^2 + \\omega^2 = 2\\omega^2$.",
            (0, 1): "$1 + \\omega = -\\omega^2$ (from $1 + \\omega + \\omega^2 = 0$).", (0, 2): "$1 + \\omega^2 = -\\omega$ (from $1 + \\omega + \\omega^2 = 0$).", (1, 2): "$\\omega + \\omega^2 = -1$ (from $1 + \\omega + \\omega^2 = 0$)."}[(ra, rb)]
    p = f"Let $\\omega$ be a complex number with $\\omega^3 = 1$ and $\\omega \\ne 1$. What is $\\omega^{{{a}}} + \\omega^{{{bb}}}$?"
    ch = [text_choice(f"${t}$", i) for i, t in enumerate(canon) if t != best][:4]
    sol = explain("the sum of two big powers of $\\omega$.", "since $\\omega^3 = 1$, only the exponent's remainder mod $3$ matters. Also $\\omega^3 - 1 = (\\omega - 1)(\\omega^2 + \\omega + 1) = 0$ with $\\omega \\ne 1$, so $1 + \\omega + \\omega^2 = 0$.",
                  [f"${a} = 3 \\cdot {a // 3} + {a % 3}$, so $\\omega^{{{a}}} = {pw(a % 3)}$.", f"${bb} = 3 \\cdot {bb // 3} + {bb % 3}$, so $\\omega^{{{bb}}} = {pw(bb % 3)}$.", "Add: " + simp],
                  f"${best}$.", "reducing the exponents mod $2$ or mod $4$ instead of mod $3$.")
    return (p, text_choice(f"${best}$", 50), ch, ["Reduce the exponents mod 3, and use $1 + \\omega + \\omega^2 = 0$."], sol, False)


def ru3(r):
    n = r.choice([3, 4, 6, 8, 12])
    sides = {3: surd(1, 3), 4: surd(1, 2), 6: num(1), 8: C("\\sqrt{2 - \\sqrt{2}}", math.sqrt(2 - math.sqrt(2))), 12: C("\\sqrt{2 - \\sqrt{3}}", math.sqrt(2 - math.sqrt(3)))}
    ans = sides[n]
    step = 360 // n
    ck, cr = cos_exact(step)
    p = f"The solutions of $z^{{{n}}} = 1$ are the vertices of a regular polygon in the complex plane. What is its side length?"
    wrong = [v for k, v in sides.items() if k != n] + [num(2)]
    sol = explain("the distance between two neighboring roots.", f"the roots lie on the unit circle, spaced $\\frac{{360^\\circ}}{{{n}}} = {step}^\\circ$ apart. A side is a chord of the unit circle with a ${step}^\\circ$ central angle.",
                  [f"Take neighbors $1$ and $\\cos {step}^\\circ + i\\sin {step}^\\circ$. The triangle with the center has two sides of length $1$ and a ${step}^\\circ$ angle between them.",
                   f"Law of Cosines: side$^2 = 1 + 1 - 2\\cos {step}^\\circ = 2 - 2 \\cdot {surd(ck, cr).tex}$.", f"Side $= {ans.tex}$."],
                  f"${ans.tex}$.", "using the radius ($1$) as the side; that only happens for the hexagon.")
    return (p, ans, wrong, ["The vertices lie on the unit circle, spaced $\\frac{360^\\circ}{n}$ apart."], sol)


def ru4(r):
    n, m = r.randint(4, 30), r.randint(4, 30)
    if n == m:
        return None
    g = math.gcd(n, m)
    p = f"How many complex numbers $z$ satisfy both $z^{{{n}}} = 1$ and $z^{{{m}}} = 1$?"
    sol = explain("roots shared by both equations.", "if $z^{" + str(n) + "} = 1$ and $z^{" + str(m) + "} = 1$, then $z^d = 1$ for any $d$ you can build as a combination of the exponents, including $\\gcd(" + f"{n}, {m}" + ")$.",
                  [f"$\\gcd({n}, {m}) = {g}$, and by Bezout, ${g} = {n}u + {m}v$ for some integers $u, v$. So $z^{{{g}}} = (z^{{{n}}})^u (z^{{{m}}})^v = 1$.",
                   f"Conversely, every solution of $z^{{{g}}} = 1$ solves both, since ${g}$ divides ${n}$ and ${m}$.", f"So the common roots are the ${g}$ roots of $z^{{{g}}} = 1$."],
                  f"${g}$.", "using the least common multiple; that counts roots of either equation, not both.")
    return (p, g, [math.lcm(n, m), min(n, m), g + 1, 1 if g != 1 else 2, abs(n - m)], ["The common roots are exactly the roots of $z^{\\gcd(n, m)} = 1$."], sol)


def ruc1(r):
    n = r.randint(3, 9)
    N = r.randint(n + 1, 60)
    w = cmath.exp(2j * math.pi / n)
    s = sum(w ** k for k in range(N + 1))
    if abs(s.imag) > 1e-9 or abs(s.real - round(s.real)) > 1e-9:
        return None
    ans = round(s.real)
    full, left = (N + 1) // n, (N + 1) % n
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. What is $1 + \\omega + \\omega^2 + \\cdots + \\omega^{{{N}}}$?"
    sol = explain("the sum of the powers of $\\omega$.", f"$\\omega$ is a primitive ${n}$th root of unity: $\\omega^{{{n}}} = 1$, and $1 + \\omega + \\cdots + \\omega^{{{n - 1}}} = \\frac{{\\omega^{{{n}}} - 1}}{{\\omega - 1}} = 0$.",
                  [f"The sum has ${N + 1}$ terms (from $\\omega^0$ to $\\omega^{{{N}}}$).", f"${N + 1} = {n} \\cdot {full} + {left}$: ${full}$ full blocks of ${n}$, each worth $0$.",
                   (f"The leftover term is $\\omega^{{{N}}} = \\omega^{{{n * full}}} = 1$." if left == 1 else "There are no leftover terms.")],
                  f"${ans}$.", f"forgetting the $1 = \\omega^0$ at the start, which changes the term count to ${N}$.")
    return (p, ans, [0 if ans else 1, N + 1, n, -1 if ans != -1 else 2, ans + 1], [f"Every block of ${n}$ consecutive powers adds to $0$."], sol)


def ruc2(r):
    n = r.randint(4, 8)
    a = r.randint(2, 4)
    ans = F(a ** n - 1, a - 1)
    p = f"Let $\\omega_1, \\omega_2, \\ldots, \\omega_{{{n - 1}}}$ be the solutions of $z^{{{n}}} = 1$ other than $z = 1$. What is $({a} - \\omega_1)({a} - \\omega_2)\\cdots({a} - \\omega_{{{n - 1}}})$?"
    sol = explain(f"the product of $({a} - \\omega_k)$ over every root except $1$.", "a polynomial equals its leading coefficient times the product of $(z - \\text{root})$. Plug in a number to evaluate the product.",
                  [f"$z^{{{n}}} - 1 = (z - 1)(z - \\omega_1)\\cdots(z - \\omega_{{{n - 1}}})$.", f"Also $z^{{{n}}} - 1 = (z - 1)(1 + z + z^2 + \\cdots + z^{{{n - 1}}})$, so $(z - \\omega_1)\\cdots(z - \\omega_{{{n - 1}}}) = 1 + z + \\cdots + z^{{{n - 1}}}$.",
                   f"At $z = {a}$: $1 + {a} + \\cdots + {a}^{{{n - 1}}} = \\frac{{{a}^{{{n}}} - 1}}{{{a} - 1}} = \\frac{{{a ** n - 1}}}{{{a - 1}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering ${a}^{{{n}}} - 1$, which still includes the factor $({a} - 1)$ from the root $z = 1$.")
    return (p, ans, [a ** n - 1, a ** (n - 1), ans + 1, a ** n, F(a ** n + 1, a + 1)],
            ["$z^n - 1 = (z - 1)(z - \\omega_1)\\cdots(z - \\omega_{n - 1})$, so the product of the other factors is $1 + z + \\cdots + z^{n-1}$."], sol)


def ruc3(r):
    n = r.randint(5, 100)
    w = cmath.exp(2j * math.pi / 3)
    val = (w ** n + w ** (-n)).real
    ans = round(val)
    p = f"If $\\omega^2 + \\omega + 1 = 0$, what is $\\omega^{{{n}}} + \\dfrac{{1}}{{\\omega^{{{n}}}}}$?"
    rem = n % 3
    sol = explain(f"$\\omega^{{{n}}} + \\omega^{{-{n}}}$.", "multiply $\\omega^2 + \\omega + 1 = 0$ by $(\\omega - 1)$: $\\omega^3 - 1 = 0$, so $\\omega^3 = 1$. Then exponents only matter mod $3$.",
                  [f"${n} = 3 \\cdot {n // 3} + {rem}$, so $\\omega^{{{n}}} = \\omega^{{{rem}}}$" + (" $= 1$." if rem == 0 else "."),
                   ("Then $\\frac{1}{\\omega^n} = 1$ too, and the sum is $1 + 1 = 2$." if rem == 0 else
                    f"$\\frac{{1}}{{\\omega^{{{rem}}}}} = \\omega^{{{3 - rem}}}$ (because $\\omega^{{{rem}}} \\cdot \\omega^{{{3 - rem}}} = \\omega^3 = 1$).")]
                  + ([] if rem == 0 else ["So the sum is $\\omega + \\omega^2 = -1$."]),
                  f"${ans}$.", "forgetting that $\\frac{1}{\\omega} = \\omega^2$ when $\\omega^3 = 1$.")
    return (p, ans, [2 if ans != 2 else -1, 0, 1, -2, 3], ["Multiply $\\omega^2 + \\omega + 1 = 0$ by $\\omega - 1$ to see $\\omega^3 = 1$."], sol)


b.fill_unique("basics", [ru1, ru2, ru3, ru4] + MORE[b.skill_id]["basics"], 5001)
b.fill_unique("challenge", [ruc1, ruc2, ruc3] + MORE[b.skill_id]["challenge"], 5002)


# ---------------------------------------------------------------- polynomials: Vieta
b = bank("poly_vieta")


def polystr(coeffs, var="x"):
    """coeffs high to low."""
    n = len(coeffs) - 1
    out = ""
    for i, c in enumerate(coeffs):
        e = n - i
        if c == 0:
            continue
        sgn = "-" if c < 0 else "+"
        ac = abs(c)
        term = ("" if ac == 1 and e > 0 else str(ac)) + (var if e >= 1 else "") + (f"^{{{e}}}" if e > 1 else "")
        out += (f"{'-' if c < 0 else ''}{term}" if not out else f" {sgn} {term}")
    return out


def roots_to_coeffs(rs):
    co = [1]
    for root_ in rs:
        new = co + [0]
        for i in range(len(co)):
            new[i + 1] -= root_ * co[i]
        co = new
    return co


def vieta3(co):
    return (f"For $x^3 + bx^2 + cx + d$ with roots $r, s, t$: $r + s + t = -b$, $rs + st + tr = c$, $rst = -d$. Here $b = {co[1]}$, $c = {co[2]}$, $d = {co[3]}$.")


def pv1(r):
    rs = [r.randint(-5, 6) for _ in range(3)]
    co = roots_to_coeffs(rs)
    ask = r.choice(["sum", "prod", "pair"])
    ans = {"sum": sum(rs), "prod": rs[0] * rs[1] * rs[2], "pair": rs[0] * rs[1] + rs[1] * rs[2] + rs[0] * rs[2]}[ask]
    words = {"sum": "the sum of the roots", "prod": "the product of the roots", "pair": "$rs + st + tr$, where $r$, $s$, $t$ are the roots,"}[ask]
    p = f"What is {words} of ${polystr(co)} = 0$?"
    last = {"sum": f"$r + s + t = -({co[1]}) = {ans}$.", "prod": f"$rst = -({co[3]}) = {ans}$.", "pair": f"$rs + st + tr = {co[2]} = {ans}$."}[ask]
    sol = explain({"sum": "the sum of the roots.", "prod": "the product of the roots.", "pair": "the sum of the products of the roots two at a time."}[ask],
                  "Vieta's formulas read these symmetric expressions straight off the coefficients, with no need to find the roots.", [vieta3(co), last],
                  f"${ans}$.", "dropping the minus sign in $-b$ or $-d$; the signs alternate.")
    return (p, ans, [-ans if ans else 1, co[1], co[3], co[2], ans + 1], ["For $x^3 + bx^2 + cx + d$: sum $= -b$, pair sum $= c$, product $= -d$."], sol)


def pv2(r):
    rs = [r.randint(-5, 6) for _ in range(3)]
    co = roots_to_coeffs(rs)
    ans = sum(x * x for x in rs)
    e1, e2 = -co[1], co[2]
    p = f"Let $r$, $s$, $t$ be the roots of ${polystr(co)} = 0$. What is $r^2 + s^2 + t^2$?"
    sol = explain("$r^2 + s^2 + t^2$.", "square the sum: $(r + s + t)^2 = r^2 + s^2 + t^2 + 2(rs + st + tr)$. Both pieces on the right side except the squares come from Vieta.",
                  [vieta3(co), f"So $r + s + t = {e1}$ and $rs + st + tr = {e2}$.", f"$r^2 + s^2 + t^2 = (r + s + t)^2 - 2(rs + st + tr) = {e1 * e1} - 2({e2}) = {ans}$."],
                  f"${ans}$.", "squaring the sum and forgetting to subtract the cross terms.")
    return (p, ans, [co[1] ** 2, co[1] ** 2 + 2 * co[2], ans + 2, abs(co[2]) * 2, ans - 1], ["$r^2 + s^2 + t^2 = (r + s + t)^2 - 2(rs + st + tr)$."], sol)


def pv3(r):
    rs = [x for x in [r.randint(-6, 6) for _ in range(3)] if x != 0]
    if len(rs) < 3:
        return None
    co = roots_to_coeffs(rs)
    ans = sum(F(1, x) for x in rs)
    p = f"Let $r$, $s$, $t$ be the roots of ${polystr(co)} = 0$. What is $\\dfrac{{1}}{{r}} + \\dfrac{{1}}{{s}} + \\dfrac{{1}}{{t}}$?"
    sol = explain("the sum of the reciprocals of the roots.", "use a common denominator: $\\frac{1}{r} + \\frac{1}{s} + \\frac{1}{t} = \\frac{st + rt + rs}{rst}$. Both top and bottom come from Vieta.",
                  [vieta3(co), f"Top: $rs + st + tr = {co[2]}$. Bottom: $rst = {-co[3]}$.", f"$\\frac{{{co[2]}}}{{{-co[3]}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "using $\\frac{1}{r + s + t}$, which is not the sum of reciprocals.")
    return (p, ans, [-ans if ans else 1, F(co[2], co[3]), F(co[1], co[3]), ans + 1, F(1, sum(rs)) if sum(rs) else 2], ["Combine: $\\frac{rs + st + tr}{rst}$."], sol)


def pv4(r):
    a = r.randint(2, 6)
    bb = r.randint(-20, 20)
    deg = r.choice([4, 5])
    p = f"What is the sum of all roots (real and complex, counted with multiplicity) of ${a}x^{{{deg}}} {'+' if bb >= 0 else '-'} {abs(bb)}x^{{{deg - 1}}} + 7x - 3 = 0$?"
    ans = F(-bb, a)
    sol = explain("the sum of all the roots.", "Vieta: for any polynomial, the sum of the roots is $-\\frac{\\text{coefficient of } x^{n-1}}{\\text{coefficient of } x^n}$. The other coefficients don't matter.",
                  [f"Leading coefficient: ${a}$. Coefficient of $x^{{{deg - 1}}}$: ${bb}$.", f"Sum $= -\\frac{{{bb}}}{{{a}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting to divide by the leading coefficient when it isn't $1$.")
    return (p, ans, [-ans if ans else 1, bb, F(bb, a) if bb else 2, F(3, a), F(-bb, deg)], ["The sum of the roots is $-\\frac{\\text{second coefficient}}{\\text{leading coefficient}}$."], sol)


def pvc1(r):
    rs = [r.randint(-4, 5) for _ in range(3)]
    co = roots_to_coeffs(rs)
    ans = sum(x ** 3 for x in rs)
    e1, e2, e3 = sum(rs), rs[0] * rs[1] + rs[1] * rs[2] + rs[0] * rs[2], rs[0] * rs[1] * rs[2]
    p = f"Let $r$, $s$, $t$ be the roots of ${polystr(co)} = 0$. What is $r^3 + s^3 + t^3$?"
    sol = explain("$r^3 + s^3 + t^3$.", "write it in terms of $e_1 = r + s + t$, $e_2 = rs + st + tr$, $e_3 = rst$: $r^3 + s^3 + t^3 = e_1^3 - 3e_1e_2 + 3e_3$.",
                  [vieta3(co), f"$e_1 = {e1}$, $e_2 = {e2}$, $e_3 = {e3}$.", f"$e_1^3 = {e1 ** 3}$, $3e_1e_2 = {3 * e1 * e2}$, $3e_3 = {3 * e3}$.", f"$r^3 + s^3 + t^3 = {e1 ** 3} - ({3 * e1 * e2}) + ({3 * e3}) = {ans}$."],
                  f"${ans}$.", "cubing the sum, $e_1^3$, and forgetting the correction terms.")
    return (p, ans, [e1 ** 3, e1 ** 3 - 3 * e1 * e2, ans + 3 * e3, ans - 1, 3 * e3], ["$r^3 + s^3 + t^3 = e_1^3 - 3e_1e_2 + 3e_3$, where $e_1, e_2, e_3$ come from Vieta."], sol)


def pvc2(r):
    m, d = r.randint(1, 6), r.randint(1, 5)
    rs = [m - d, m, m + d]
    co = roots_to_coeffs(rs)
    ans = rs[2]
    p = f"The three roots of $x^3 {'-' if co[1] < 0 else '+'} {abs(co[1])}x^2 {'+' if co[2] >= 0 else '-'} {abs(co[2])}x + k = 0$ form an arithmetic sequence. What is the largest root?"
    sol = explain("the largest root.", "name the roots $m - d$, $m$, $m + d$. Vieta's sum gives $m$, and Vieta's pair sum gives $d$. The unknown $k$ is not needed.",
                  [f"Sum of roots: $3m = {-co[1]}$, so $m = {m}$.", f"Pair sum: $(m - d)m + m(m + d) + (m - d)(m + d) = 3m^2 - d^2 = {co[2]}$.",
                   f"$3 \\cdot {m * m} - d^2 = {co[2]}$, so $d^2 = {3 * m * m - co[2]}$ and $d = {d}$.", f"Roots: ${m - d}, {m}, {m + d}$. The largest is ${ans}$."],
                  f"${ans}$.", "answering the middle root $m$.")
    return (p, ans, [m, m - d, ans + 1, 3 * m, d], ["If the roots are $m - d$, $m$, $m + d$, their sum is $3m$."], sol)


def pvc3(r):
    a, bb, c = r.randint(-6, 6), r.randint(-10, 10), r.randint(-9, 9)
    ans = a * a - 2 * bb
    p = f"What is the sum of the squares of the roots of $x^4 {'+' if a >= 0 else '-'} {abs(a)}x^3 {'+' if bb >= 0 else '-'} {abs(bb)}x^2 {'+' if c >= 0 else '-'} {abs(c)}x + 1 = 0$?"
    sol = explain("the sum of the squares of the four roots.", "$(\\text{sum of roots})^2 = \\text{sum of squares} + 2(\\text{sum of products two at a time})$, so sum of squares $= e_1^2 - 2e_2$.",
                  [f"Vieta for a monic quartic: $e_1 = -({a}) = {-a}$ and $e_2 = {bb}$ (the $x^2$ coefficient).", f"Sum of squares $= {-a}^2 - 2({bb}) = {a * a} - ({2 * bb}) = {ans}$.",
                   "(The answer can be negative: some roots are complex, and their squares can be negative.)"],
                  f"${ans}$.", "forgetting that $e_1 = -(\\text{coefficient of } x^3)$.")
    return (p, ans, [a * a + 2 * bb, a * a, ans + 2, -2 * bb, a * a - bb], ["Sum of squares $= e_1^2 - 2e_2$."], sol)


b.fill_unique("basics", [pv1, pv2, pv3, pv4] + MORE[b.skill_id]["basics"], 5101)
b.fill_unique("challenge", [pvc1, pvc2, pvc3] + MORE[b.skill_id]["challenge"], 5102)


# ---------------------------------------------------------------- remainder and factor theorem
b = bank("poly_remainder")


def evalp(co, x):
    v = 0
    for c in co:
        v = v * x + c
    return v


def xminus(a):
    return f"x {'-' if a >= 0 else '+'} {abs(a)}"


def subst(co, a):
    n = len(co) - 1
    parts = []
    for i, c in enumerate(co):
        e = n - i
        if c == 0:
            continue
        xa = f"({a})" if a < 0 else str(a)
        parts.append(f"{c}" + (f" \\cdot {xa}" + (f"^{{{e}}}" if e > 1 else "") if e else ""))
    return " + ".join(parts).replace("+ -", "- ")


def pr1_(r):
    co = [r.randint(-5, 5) for _ in range(r.randint(3, 5))]
    co[0] = co[0] or 1
    a = r.randint(-3, 3)
    ans = evalp(co, a)
    p = f"What is the remainder when $P(x) = {polystr(co)}$ is divided by ${xminus(a)}$?"
    sol = explain(f"the remainder of $P(x) \\div ({xminus(a)})$.", f"Remainder Theorem: $P(x) = (x - a)Q(x) + R$. Plug in $x = a$ and the first part vanishes, so $R = P(a)$. Here $a = {a}$.",
                  [f"$P({a}) = {subst(co, a)}$.", f"Evaluate: $P({a}) = {ans}$."],
                  f"${ans}$.", f"plugging in $x = {-a}$; the root of ${xminus(a)}$ is $x = {a}$.")
    return (p, ans, [evalp(co, -a), ans + 1, co[-1], sum(co), ans - 2], ["Remainder Theorem: the remainder on division by $x - a$ is $P(a)$."], sol)


def pr2_(r):
    a = r.randint(-3, 4)
    co = [1, r.randint(-5, 5), r.randint(-5, 5)]
    k = -evalp(co + [0], a)
    p = f"For what value of $k$ is ${xminus(a)}$ a factor of ${polystr(co + [0])} + k$?"
    sol = explain("the $k$ that makes the division exact.", f"Factor Theorem: ${xminus(a)}$ is a factor exactly when $P({a}) = 0$.",
                  [f"$P({a}) = {subst(co + [0], a)} + k = {-k} + k$.", f"Set it to $0$: $k = {k}$."],
                  f"${k}$.", f"plugging in $x = {-a}$ instead of $x = {a}$.")
    return (p, k, [-k if k else 1, k + 1, evalp(co + [0], -a), a ** 3, k - a], ["Factor Theorem: $x - a$ is a factor exactly when $P(a) = 0$."], sol)


def pr3_(r):
    a, bb = r.randint(1, 4), r.randint(-3, 3)
    n = r.randint(2, 8)
    ans = (a + bb) ** n
    p = f"What is the sum of the coefficients of $({a if a > 1 else ''}x {'+' if bb >= 0 else '-'} {abs(bb)})^{{{n}}}$ when it is expanded?"
    if bb == 0:
        return None
    sol = explain("the sum of all coefficients after expanding.", "plugging in $x = 1$ turns every term $c x^k$ into just $c$, so $P(1)$ is the sum of the coefficients. No expanding needed.",
                  [f"$P(1) = ({a} \\cdot 1 {'+' if bb >= 0 else '-'} {abs(bb)})^{{{n}}} = {a + bb if a + bb >= 0 else f'({a + bb})'}^{{{n}}}$.", f"$= {ans}$."],
                  f"${ans}$.", "adding only the first and last coefficients.")
    return (p, ans, [a ** n + bb ** n, (a - bb) ** n, ans + 1, n * (a + bb), 2 ** n], ["Plug in $x = 1$."], sol)


def pr4_(r):
    a, bb = r.sample(range(-4, 5), 2)
    pa, pb = r.randint(-10, 10), r.randint(-10, 10)
    m = F(pa - pb, a - bb)
    c = pa - m * a
    x0 = r.randint(-5, 6)
    ans = m * x0 + c
    p = (f"When $P(x)$ is divided by ${xminus(a)}$ the remainder is ${pa}$, and when divided by ${xminus(bb)}$ the remainder is ${pb}$. "
         f"The remainder when $P(x)$ is divided by $({xminus(a)})({xminus(bb)})$ is $R(x)$. What is $R({x0})$?")
    sol = explain(f"$R({x0})$.", "dividing by a quadratic leaves a remainder of degree at most $1$: $P(x) = (x - a)(x - b)Q(x) + mx + c$. Plugging in the two roots kills the first part.",
                  [f"Remainder Theorem: $P({a}) = {pa}$ and $P({bb}) = {pb}$, so $R({a}) = {pa}$ and $R({bb}) = {pb}$.",
                   f"$R$ is a line through $({a}, {pa})$ and $({bb}, {pb})$: slope $m = \\frac{{{pa} - ({pb})}}{{{a} - ({bb})}} = {num(m).tex}$.", f"$c = {pa} - " + (f"\\left({num(m).tex}\\right)" if m < 0 else num(m).tex) + f" \\cdot ({a}) = {num(c).tex}$, so $R(x) = {num(m).tex}x + ({num(c).tex})$.",
                   f"$R({x0}) = {num(m).tex} \\cdot ({x0}) + ({num(c).tex}) = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "assuming the remainder is a constant; dividing by a quadratic can leave a linear remainder.")
    return (p, ans, [pa + pb, ans + 1, -ans if ans else 2, m, c], ["The remainder is linear: $R(x) = mx + c$ with $R(" + str(a) + ") = " + str(pa) + "$ and $R(" + str(bb) + ") = " + str(pb) + "$."], sol)


def prc1_(r):
    n = r.randint(10, 60)
    a = r.randint(1, 5)
    if n % 2 == 0:
        rx, rc = a, 1
    else:
        rx, rc = 1 + a, 0
    x0 = 2
    ans = rx * x0 + rc
    rtex = f"{rx if rx != 1 else ''}x" + (f" + {rc}" if rc else "")
    p = f"Let $R(x)$ be the remainder when $x^{{{n}}} + {a}x$ is divided by $x^2 - 1$. What is $R(2)$?"
    sol = explain("the remainder, evaluated at $2$.", "working modulo $x^2 - 1$ means we may replace $x^2$ with $1$ anywhere. That shrinks any power of $x$ to $1$ or $x$.",
                  [f"$x^{{{n}}} = (x^2)^{{{n // 2}}}" + (" \\cdot x" if n % 2 else "") + f" \\equiv 1^{{{n // 2}}}" + (" \\cdot x = x" if n % 2 else " = 1") + "$.",
                   f"So $x^{{{n}}} + {a}x \\equiv {'x' if n % 2 else '1'} + {a}x$, and $R(x) = {rtex}$.", f"$R(2) = {ans}$."],
                  f"${ans}$.", f"plugging $x = 2$ into $x^{{{n}}} + {a}x$ directly; the remainder is a different polynomial.")
    return (p, ans, [2 ** n % 100 if 2 ** n % 100 != ans else ans + 3, ans + 1, ans - 1, a + 1, 2 * a], ["$x^2 \\equiv 1$, so $x^n$ reduces to $1$ or $x$ depending on whether $n$ is even or odd."], sol)


def prc2_(r):
    k = r.randint(-5, 5)
    q = [r.randint(-5, 5) for _ in range(3)]
    P = lambda x: (x - 1) * (x - 2) * (x - 3) + q[0] * x * x + q[1] * x + q[2]
    vals = [P(1), P(2), P(3)]
    x0 = r.choice([0, 4, 5])
    ans = P(x0)
    Q = lambda x: q[0] * x * x + q[1] * x + q[2]
    cub = (x0 - 1) * (x0 - 2) * (x0 - 3)
    p = f"A cubic polynomial $P(x)$ with leading coefficient $1$ has $P(1) = {vals[0]}$, $P(2) = {vals[1]}$, and $P(3) = {vals[2]}$. What is $P({x0})$?"
    sol = explain(f"$P({x0})$.", "split $P$ into a piece that is $0$ at $1, 2, 3$ and a piece that matches the given values: $P(x) = (x - 1)(x - 2)(x - 3) + Q(x)$, where $Q$ has degree at most $2$. This keeps the leading coefficient $1$.",
                  [f"At $x = 1, 2, 3$ the product is $0$, so $Q(1) = {vals[0]}$, $Q(2) = {vals[1]}$, $Q(3) = {vals[2]}$.",
                   f"Solve for $Q(x) = ax^2 + bx + c$ from these three equations: $Q(x) = {polystr(q) or '0'}$.",
                   f"$Q({x0}) = {Q(x0)}$ and $({x0} - 1)({x0} - 2)({x0} - 3) = {cub}$.", f"$P({x0}) = {cub} + {Q(x0) if Q(x0) >= 0 else f'({Q(x0)})'} = {ans}$."],
                  f"${ans}$.", "fitting a quadratic through the three points and forgetting the cubic part.")
    return (p, ans, [Q(x0), ans + 6, ans - 6, ans + 1, cub], ["Write $P(x) = (x - 1)(x - 2)(x - 3) + Q(x)$ where $Q$ has degree at most 2 and matches the given values."], sol)


def prc3_(r):
    n = r.randint(5, 60)
    rem = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}[n % 4]
    a, bb = rem
    x0 = 3
    ans = a * x0 + bb
    rt = polystr([a, bb]) if a else str(bb)
    p = f"Let $R(x)$ be the remainder when $x^{{{n}}}$ is divided by $x^2 + 1$. What is $R(3)$?"
    sol = explain("the remainder, evaluated at $3$.", "modulo $x^2 + 1$ we may replace $x^2$ with $-1$. Then powers of $x$ cycle like powers of $i$: $1, x, -1, -x$.",
                  [f"${n} = 4 \\cdot {n // 4} + {n % 4}$, and $x^4 = (x^2)^2 \\equiv 1$.", f"So $x^{{{n}}} \\equiv x^{{{n % 4}}} \\equiv {rt}$, and $R(x) = {rt}$.", f"$R(3) = {ans}$."],
                  f"${ans}$.", f"computing $3^{{{n}}}$; the remainder is a small polynomial, not the original one.")
    return (p, ans, [-ans if ans else 2, 3 ** n % 10, 1 if ans != 1 else 0, 3 if ans != 3 else -1, -3 if ans != -3 else 2], ["$x^2 \\equiv -1$, so the powers cycle $1, x, -1, -x$."], sol)


b.fill_unique("basics", [pr1_, pr2_, pr3_, pr4_] + MORE[b.skill_id]["basics"], 5201)
b.fill_unique("challenge", [prc1_, prc2_, prc3_] + MORE[b.skill_id]["challenge"], 5202)


# ---------------------------------------------------------------- roots of polynomials
b = bank("poly_roots")


def rt1_(r):
    rs = sorted(set(r.randint(-5, 6) for _ in range(3)))
    if len(rs) < 3:
        return None
    co = roots_to_coeffs(rs)
    ask = r.choice(["largest", "smallest"])
    ans = rs[-1] if ask == "largest" else rs[0]
    p = f"What is the {ask} root of ${polystr(co)} = 0$?"
    sol = explain(f"the {ask} root.", "Rational Root Theorem: with leading coefficient $1$, any rational root is an integer dividing the constant term. Test those, then factor.",
                  [f"Constant term: ${co[3]}$. Test its divisors" + (" (and $0$, since the constant is $0$)" if co[3] == 0 else "") + f": $x = {rs[0]}$ works.",
                   f"Factor out $({xminus(rs[0])})$ and solve the quadratic left over, or keep testing: the roots are ${rs[0]}$, ${rs[1]}$, ${rs[2]}$.",
                   f"So $P(x) = ({xminus(rs[0])})({xminus(rs[1])})({xminus(rs[2])})$, and the {ask} root is ${ans}$."],
                  f"${ans}$.", "reading roots off the factors with the wrong sign: $(x - 3)$ gives the root $+3$.")
    return (p, ans, [rs[1], -ans if ans else 7, rs[0] if ask == "largest" else rs[-1], co[-1], ans + 1], ["Test divisors of the constant term (Rational Root Theorem), then factor."], sol)


def rt2_(r):
    p_, q_ = r.sample([1, 4, 9, 16, 25], 2)
    k = r.choice([-1, 1])
    if k == -1:
        co = [1, 0, p_ + q_, 0, p_ * q_]
        ans = 0
    else:
        co = [1, 0, -(p_ + q_), 0, p_ * q_]
        ans = 4
    sp, sq = int(p_ ** 0.5), int(q_ ** 0.5)
    p = f"How many real solutions does ${polystr(co)} = 0$ have?"
    if k == 1:
        last = [f"$x^2 = {p_}$ gives $x = \\pm {sp}$, and $x^2 = {q_}$ gives $x = \\pm {sq}$.", "That is $4$ different real solutions."]
    else:
        last = [f"$x^2 = -{p_}$ and $x^2 = -{q_}$: a real square can't be negative.", "So there are $0$ real solutions (all four roots are imaginary)."]
    sol = explain("the number of real solutions.", "only even powers appear, so substitute $y = x^2$ to get a quadratic.",
                  [f"With $y = x^2$: $y^2 {'-' if k == 1 else '+'} {p_ + q_}y + {p_ * q_} = (y {'-' if k == 1 else '+'} {p_})(y {'-' if k == 1 else '+'} {q_}) = 0$."] + last,
                  f"${ans}$.", "counting the $y$ solutions instead of the $x$ solutions, or forgetting $\\pm$ square roots.")
    return (p, ans, [2, 1, 3, 4 if ans == 0 else 0, 8], ["Treat it as a quadratic in $x^2$."], sol)


def rt3_(r):
    rs = [r.randint(-4, 4) for _ in range(2)]
    a = r.choice([2, 3])
    rt = F(r.choice([1, -1, 3, -3]), a)
    numr = rt.numerator
    co = [a, -numr]
    full = [0] * 4
    q = roots_to_coeffs(rs)
    for i, c in enumerate(co):
        for j, d in enumerate(q):
            full[i + j] += c * d
    p = f"Which number is a root of ${polystr(full)} = 0$ and is not an integer?"
    sol = explain("a fractional root.", "Rational Root Theorem: a rational root $\\frac{p}{q}$ in lowest terms has $p$ dividing the constant term and $q$ dividing the leading coefficient.",
                  [f"Leading coefficient ${a}$, so a fractional root has denominator ${a}$.",
                   f"Factor: ${polystr(full)} = ({a}x {'-' if numr > 0 else '+'} {abs(numr)})({polystr(q)})$." if any(q[1:]) else f"Factor: ${polystr(full)} = ({a}x {'-' if numr > 0 else '+'} {abs(numr)}) \\cdot {polystr(q)}$.",
                   f"$({a}x {'-' if numr > 0 else '+'} {abs(numr)}) = 0$ gives $x = {num(rt).tex}$. The other factor gives the integer roots ${rs[0]}$ and ${rs[1]}$."],
                  f"${num(rt).tex}$.", "getting the sign of the fraction backwards when solving the linear factor.")
    return (p, rt, [-rt, 1 / rt if rt else 2, rt + 1, F(numr, a + 1), F(-numr, a + 1)], ["Rational roots have the form $\\frac{p}{q}$ with $p$ dividing the constant and $q$ dividing the leading coefficient."], sol)


def rt4_(r):
    a, bb = r.randint(-4, 5), r.randint(-6, 6)
    if a == bb:
        return None
    co = roots_to_coeffs([a, a, bb])
    p = f"The polynomial ${polystr(co)}$ has a double root. What is its other root?"
    sol = explain("the root that isn't repeated.", "call the roots $a$, $a$, $b$. A double root is a root of both $P$ and $P'$; then Vieta's sum finishes the job.",
                  [f"$P'(x) = {polystr([3, 2 * co[1], co[2]])}$. Testing small integers, $x = {a}$ makes both $P$ and $P'$ zero, so ${a}$ is the double root.",
                   f"Vieta: $a + a + b = -({co[1]}) = {2 * a + bb}$.", f"$b = {2 * a + bb} - 2({a}) = {bb}$."],
                  f"${bb}$.", "answering the double root itself.")
    return (p, bb, [a, -bb if bb else 3, bb + 1, co[-1], -a if a else 2], ["A double root of $P$ is also a root of $P'$. Or factor by testing small integers."], sol)


def rtc1_(r):
    a, bb = r.randint(1, 6), r.choice([2, 3, 5, 6, 7])
    c = a * a - bb
    p = f"The quadratic $x^2 + px + q$ with integer coefficients has $\\,{a} + \\sqrt{{{bb}}}\\,$ as a root. What is $q$?"
    sol = explain("the constant term $q$.", "with rational coefficients, irrational roots come in conjugate pairs: $a + \\sqrt{b}$ forces $a - \\sqrt{b}$.",
                  [f"The roots are ${a} + \\sqrt{{{bb}}}$ and ${a} - \\sqrt{{{bb}}}$.", "Vieta: $q$ is the product of the roots.", f"$q = ({a} + \\sqrt{{{bb}}})({a} - \\sqrt{{{bb}}}) = {a}^2 - ({bb}) = {c}$."],
                  f"${c}$.", f"adding $\\sqrt{{{bb}}}^2$ instead of subtracting it in the difference of squares.")
    return (p, c, [a * a + bb, -c if c else 1, a * a, bb, 2 * a], ["The other root must be the conjugate $" + str(a) + " - \\sqrt{" + str(bb) + "}$."], sol)


def rtc2_(r):
    y1, y2 = r.sample([-5, -4, -3, 3, 4, 5, -2, 2, 6], 2)
    a = -(y1 + y2)
    bb = y1 * y2 + 2
    co = [1, a, bb, a, 1]
    contrib = lambda y: y if abs(y) > 2 else (y // 2 if abs(y) == 2 else 0)
    tot = contrib(y1) + contrib(y2)
    p = f"What is the sum of all real roots of ${polystr(co)} = 0$?"
    lines = []
    for y in (y1, y2):
        if abs(y) > 2:
            lines.append(f"$x + \\frac{{1}}{{x}} = {y}$ means $x^2 {'-' if y > 0 else '+'} {abs(y)}x + 1 = 0$: discriminant ${y * y - 4} > 0$, two real roots adding to ${y}$")
        else:
            lines.append(f"$x + \\frac{{1}}{{x}} = {y}$ means $(x {'-' if y > 0 else '+'} 1)^2 = 0$: just the real root $x = {y // 2}$")
    sol = explain("the sum of the distinct real roots.", "the coefficients read the same forwards and backwards, so divide by $x^2$ and substitute $y = x + \\frac{1}{x}$, using $x^2 + \\frac{1}{x^2} = y^2 - 2$.",
                  [f"Divide by $x^2$: $\\left(x^2 + \\frac{{1}}{{x^2}}\\right) {sgn(a)} {abs(a)}\\left(x + \\frac{{1}}{{x}}\\right) + {bb} = 0$.",
                   f"Substitute: $y^2 - 2 {sgn(a)} {abs(a)}y + {bb} = 0$, i.e. $y^2 {sgn(a)} {abs(a)}y {sgn(bb - 2)} {abs(bb - 2)} = 0$, so $y = {y1}$ or $y = {y2}$.",
                   "Back to $x$: " + "; ".join(lines) + ".", f"Sum of the real roots: ${tot}$."],
                  f"${tot}$.", "counting roots from a $y$ with $|y| < 2$; $x + \\frac{1}{x}$ can never be between $-2$ and $2$ for real $x$.")
    return (p, tot, [-a, a, tot + 1, 0 if tot else 2, y1 * y2], ["Divide by $x^2$ and let $y = x + \\frac{1}{x}$."], sol)


def rtc3_(r):
    N = r.choice([6, 8, 10, 12, 15, 18, 20])
    ks = sorted({x * x * x - N * x for x in range(-10, 11)})
    k = r.choice([x * x * x - N * x for x in range(-5, 6)])
    roots = [x for x in range(-50, 51) if x ** 3 - N * x - k == 0]
    p = f"How many integers $x$ satisfy $x^3 - {N}x = {k}$?"
    ans = len(roots)
    r0 = roots[0]
    cq = r0 * r0 - N
    disc = 4 * N - 3 * r0 * r0
    sol = explain("the number of integer solutions.", "find one integer root by testing, factor it out, and study the quadratic that is left.",
                  [f"Rewrite as $x^3 - {N}x - ({k}) = 0$. Testing small integers, $x = {r0}$ works.",
                   f"Divide by $(x - ({r0}))$: $x^3 - {N}x - ({k}) = (x - ({r0}))(x^2 + {r0}x + ({cq}))$.",
                   f"The quadratic has discriminant $({r0})^2 - 4({cq}) = {disc}$" + (", which is negative: no more real roots." if disc < 0 else ", so its roots are $\\frac{" + f"{-r0} \\pm \\sqrt{{{disc}}}" + "}{2}$; check which are integers."),
                   "Integer solutions: " + ", ".join(f"$x = {x}$" for x in roots) + f". That is ${ans}$."],
                  f"${ans}$.", "assuming a cubic always has three integer roots.")
    return (p, ans, [3 if ans != 3 else 2, 1 if ans != 1 else 0, 0 if ans else 2, ans + 1, 4], ["Try the integer that makes it easy to see one root, then factor out that root."], sol)


b.fill_unique("basics", [rt1_, rt2_, rt3_, rt4_] + MORE[b.skill_id]["basics"], 5301)
b.fill_unique("challenge", [rtc1_, rtc2_, rtc3_] + MORE[b.skill_id]["challenge"], 5302)


# ---------------------------------------------------------------- conics: circles and parabolas
b = bank("con_parabolas")


def sq_shift(v, var):
    return f"({var} {'-' if v >= 0 else '+'} {abs(v)})"


def cpar1(r):
    h, k, rr = r.randint(-8, 8), r.randint(-8, 8), r.randint(1, 10)
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - rr * rr
    p = f"What is the radius of the circle $x^2 + y^2 {'+' if D >= 0 else '-'} {abs(D)}x {'+' if E >= 0 else '-'} {abs(E)}y {'+' if Fc >= 0 else '-'} {abs(Fc)} = 0$?"
    sol = explain("the radius.", "complete the square in $x$ and in $y$ to reach the form $(x - h)^2 + (y - k)^2 = r^2$.",
                  [f"$x^2 {sgn(D)} {abs(D)}x = {sq_shift(h, 'x')}^2 - {h * h}$ (half of ${D}$ is ${-h}$, squared is ${h * h}$).",
                   f"$y^2 {sgn(E)} {abs(E)}y = {sq_shift(k, 'y')}^2 - {k * k}$.",
                   f"Substitute: ${sq_shift(h, 'x')}^2 + {sq_shift(k, 'y')}^2 = {h * h} + {k * k} - ({Fc}) = {rr * rr}$.", f"$r^2 = {rr * rr}$, so $r = {rr}$."],
                  f"${rr}$.", f"answering $r^2 = {rr * rr}$ instead of $r$.")
    return (p, rr, [rr * rr, rr + 1, abs(h) + abs(k), rr - 1 if rr > 1 else rr + 2, abs(Fc) if abs(Fc) != rr else rr + 3], ["Complete the square in $x$ and in $y$."], sol)


def cpar2(r):
    h, k = r.randint(-6, 6), r.randint(-10, 10)
    a = r.choice([1, 2, -1, 3])
    bq, cq = -2 * a * h, a * h * h + k
    p = f"What is the sum of the coordinates of the vertex of the parabola $y = {polystr([a, bq, cq])}$?"
    sol = explain("$h + k$ for the vertex $(h, k)$.", "for $y = ax^2 + bx + c$, the vertex is on the axis of symmetry $x = -\\frac{b}{2a}$. Plug that $x$ back in to get $y$.",
                  [f"$a = {a}$, $b = {bq}$: $x = -\\frac{{{bq}}}{{2 \\cdot {a}}} = {h}$.", f"$y = {a} \\cdot ({h})^2 + ({bq})({h}) + {par(cq)} = {k}$.", f"Sum: ${h} + ({k}) = {h + k}$."],
                  f"${h + k}$.", "forgetting the minus sign in $-\\frac{b}{2a}$.")
    return (p, h + k, [h - k, k, h, cq, h + k + 1], ["The vertex is at $x = -\\frac{b}{2a}$."], sol)


def cpar3(r):
    pp = F(r.randint(1, 8), r.choice([1, 2, 4]))
    coef = 1 / (4 * pp)
    p = f"The parabola $y = {num(coef).tex}x^2$ has its focus at $(0, f)$. What is $f$?"
    sol = explain("the focus height $f$.", "the parabola $y = \\frac{1}{4p}x^2$ has vertex at the origin, focus at $(0, p)$, and directrix $y = -p$.",
                  [f"Match: $\\frac{{1}}{{4p}} = {num(coef).tex}$.", f"$4p = {num(1 / coef).tex}$, so $p = {num(pp).tex}$.", f"The focus is $(0, {num(pp).tex})$."],
                  f"${num(pp).tex}$.", "using the coefficient itself as $p$; it equals $\\frac{1}{4p}$.")
    return (p, pp, [coef, 4 * pp, 2 * pp, -pp, pp + 1], ["The parabola $y = \\frac{1}{4p}x^2$ has focus $(0, p)$."], sol)


def cpar4(r):
    a = r.randint(1, 3)
    m, c = r.randint(-5, 5), r.randint(-10, 10)
    disc = m * m + 4 * a * c
    ans = 2 if disc > 0 else 1 if disc == 0 else 0
    line = polystr([m, c]) if m else str(c)
    quad = polystr([a, -m, -c])
    p = f"How many points do the parabola $y = {a if a > 1 else ''}x^2$ and the line $y = {line}$ have in common?"
    meaning = {2: "positive, so two real solutions", 1: "zero, so one (the line is tangent)", 0: "negative, so no real solutions"}[ans]
    sol = explain("the number of intersection points.", "every intersection gives a solution of the equation you get by setting the two $y$ values equal. The discriminant counts real solutions.",
                  [f"${a if a > 1 else ''}x^2 = {line}$, so ${quad} = 0$.", f"Discriminant: $b^2 - 4ac = ({-m})^2 - 4({a})({-c}) = {disc}$.", f"It is {meaning}."],
                  f"${ans}$.", "sign errors when moving the line's terms to the left side.")
    return (p, ans, [0, 1, 2, 3, 4], ["Set the expressions equal and check the discriminant."], sol)


def cparc1(r):
    r1 = r.randint(3, 10)
    d = r.randint(r1 + 1, r1 + 10)
    r2 = r.randint(max(1, d - r1 + 1), d + r1 - 1)
    if r2 <= 0 or abs(r1 - r2) >= d:
        return None
    x = F(d * d + r1 * r1 - r2 * r2, 2 * d)
    half2 = r1 * r1 - x * x
    if half2 <= 0:
        return None
    hn = half2.numerator * half2.denominator
    ans = surd(F(2, half2.denominator), hn)
    p = f"Circles of radius ${r1}$ and ${r2}$ have centers ${d}$ units apart. What is the length of their common chord?"
    sol = explain("the chord through both intersection points.", f"put the centers at $(0, 0)$ and $({d}, 0)$. The chord is vertical, and subtracting the two circle equations gives its $x$-coordinate.",
                  [f"Circles: $x^2 + y^2 = {r1 * r1}$ and $(x - {d})^2 + y^2 = {r2 * r2}$.", f"Subtract: $x^2 - (x - {d})^2 = {r1 * r1} - {r2 * r2}$, so ${2 * d}x - {d * d} = {r1 * r1 - r2 * r2}$ and $x = {num(x).tex}$.",
                   f"Half the chord: $y^2 = {r1 * r1} - \\left({num(x).tex}\\right)^2 = {num(half2).tex}$, so $y = {surd(F(1, half2.denominator), hn).tex}$.", f"The chord is $2y = {ans.tex}$."],
                  f"${ans.tex}$.", "forgetting to double the half chord.")
    return (p, ans, [surd(F(1, half2.denominator), hn), num(r1 + r2 - d), num(min(r1, r2)), surd(2, r1 * r1 + 1), surd(F(4, half2.denominator), hn)],
            ["Put one center at the origin and the other at $(d, 0)$. Subtract the circle equations to find the chord's $x$-coordinate."], sol)


def cparc2(r):
    a, bb = r.randint(1, 6), r.randint(0, 40)
    k = bb - a * a
    d2 = a * a + k * k
    ans = surd(1, d2)
    p = f"What is the distance from the origin to the vertex of $y = x^2 - {2 * a}x + {bb}$?"
    sol = explain("the distance from $(0, 0)$ to the vertex.", "complete the square to read off the vertex, then use the distance formula.",
                  [f"$x^2 - {2 * a}x + {bb} = (x - {a})^2 - {a * a} + {bb} = (x - {a})^2 + ({k})$.", f"Vertex: $({a}, {k})$.", f"Distance: $\\sqrt{{{a}^2 + ({k})^2}} = \\sqrt{{{d2}}} = {ans.tex}$."],
                  f"${ans.tex}$.", f"using the $y$-intercept $(0, {bb})$ instead of the vertex.")
    return (p, ans, [surd(1, d2 + 1), num(a + abs(k)), surd(1, a * a + bb * bb), num(abs(k)), num(a)], ["Find the vertex by completing the square."], sol)


def cparc3(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
    rr = a
    px, py = r.choice([(c, 0), (0, c)]) if r.random() < 0.5 else (None, None)
    pts = [(x, y) for x in range(-c, c + 1) for y in range(-c, c + 1) if x * x + y * y == c * c]
    px, py = r.choice(pts)
    p = f"From the point $({px}, {py})$, a tangent line is drawn to the circle $x^2 + y^2 = {rr * rr}$. What is the length of the tangent segment?"
    sol = explain("the tangent length $t$.", "the radius to the point of tangency is perpendicular to the tangent, so center, tangent point, and outside point form a right triangle.",
                  [f"Distance from the center to $({px}, {py})$: $\\sqrt{{{px * px} + {py * py}}} = {c}$. This is the hypotenuse.", f"One leg is the radius, ${rr}$.", f"$t = \\sqrt{{{c}^2 - {rr}^2}} = \\sqrt{{{c * c - rr * rr}}} = {bb}$."],
                  f"${bb}$.", f"subtracting lengths (${c} - {rr}$) instead of using the Pythagorean Theorem.")
    return (p, bb, [c - rr, c, bb + 1, c + rr, rr], ["The radius to the point of tangency is perpendicular to the tangent."], sol)


b.fill_unique("basics", [cpar1, cpar2, cpar3, cpar4] + MORE[b.skill_id]["basics"], 5401)
b.fill_unique("challenge", [cparc1, cparc2, cparc3] + MORE[b.skill_id]["challenge"], 5402)


# ---------------------------------------------------------------- ellipses and hyperbolas
b = bank("con_ellipses")


def el1(r):
    a, bb, c = r.choice([(5, 3, 4), (5, 4, 3), (13, 5, 12), (13, 12, 5), (10, 6, 8), (10, 8, 6), (17, 8, 15), (25, 7, 24)])
    p = f"What is the distance between the foci of the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{bb * bb}}} = 1$?"
    sol = explain("the distance between the two foci.", "for an ellipse with semi-major axis $a$ and semi-minor axis $b$, the foci sit $c$ from the center, where $c^2 = a^2 - b^2$.",
                  [f"$a^2 = {a * a}$ (the larger denominator) and $b^2 = {bb * bb}$.", f"$c^2 = {a * a} - {bb * bb} = {c * c}$, so $c = {c}$.", f"The foci are at $(\\pm {c}, 0)$, which are $2c = {2 * c}$ apart."],
                  f"${2 * c}$.", "answering $c$, the distance from the center to one focus.")
    return (p, 2 * c, [c, 2 * a, 2 * bb, a + bb, 2 * (a - bb)], ["For an ellipse, $c^2 = a^2 - b^2$, and the foci are $2c$ apart."], sol)


def el2(r):
    a, bb = r.randint(2, 12), r.randint(2, 12)
    if a == bb:
        return None
    p = f"What is the area of the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{bb * bb}}} = 1$?"
    ans = C(f"{a * bb}\\pi", a * bb * math.pi)
    sol = explain("the area of the ellipse.", "an ellipse is a circle stretched by different amounts in each direction, so its area is $\\pi ab$ (a circle has $a = b = r$, giving $\\pi r^2$).",
                  [f"Semi-axes: $\\sqrt{{{a * a}}} = {a}$ and $\\sqrt{{{bb * bb}}} = {bb}$.", f"Area $= \\pi \\cdot {a} \\cdot {bb} = {a * bb}\\pi$."],
                  f"${a * bb}\\pi$.", "using the denominators directly instead of their square roots.")
    return (p, ans, [C(f"{a * a * bb * bb}\\pi", a * a * bb * bb * math.pi), C(f"{(a + bb)}\\pi", (a + bb) * math.pi), C(f"{2 * a * bb}\\pi", 2 * a * bb * math.pi), C(str(a * bb), a * bb), C(f"{max(a, bb) ** 2}\\pi", max(a, bb) ** 2 * math.pi)],
            ["An ellipse with semi-axes $a$ and $b$ has area $\\pi ab$."], sol)


def el3(r):
    a, bb, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (4, 3, 5), (12, 5, 13)])
    p = f"What is the distance between the foci of the hyperbola $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{{bb * bb}}} = 1$?"
    sol = explain("the distance between the two foci.", "for a hyperbola the foci are farther out than the vertices: $c^2 = a^2 + b^2$ (a plus sign, unlike the ellipse).",
                  [f"$a^2 = {a * a}$ and $b^2 = {bb * bb}$.", f"$c^2 = {a * a} + {bb * bb} = {c * c}$, so $c = {c}$.", f"Foci at $(\\pm {c}, 0)$: $2c = {2 * c}$ apart."],
                  f"${2 * c}$.", "using the ellipse formula $c^2 = a^2 - b^2$.")
    return (p, 2 * c, [c, 2 * a, 2 * bb, 2 * abs(a - bb) or 2, a + bb], ["For a hyperbola, $c^2 = a^2 + b^2$."], sol)


def el4(r):
    a, bb = r.randint(1, 9), r.randint(1, 9)
    if a == bb:
        return None
    ans = F(bb, a)
    p = f"The hyperbola $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{{bb * bb}}} = 1$ has asymptotes $y = \\pm mx$. What is $m$?"
    sol = explain("the slope of the asymptotes.", "far from the center, the $1$ is tiny compared to the other terms, so the curve hugs $\\frac{x^2}{a^2} = \\frac{y^2}{b^2}$.",
                  [f"$\\frac{{x^2}}{{{a * a}}} = \\frac{{y^2}}{{{bb * bb}}}$ gives $y = \\pm\\frac{{{bb}}}{{{a}}}x$.", f"$m = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "flipping the ratio to $\\frac{a}{b}$, or forgetting the square roots.")
    return (p, ans, [F(a, bb), F(bb * bb, a * a), ans + 1, F(1, 2), F(a * a, bb * bb)], ["The asymptotes of $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$ are $y = \\pm\\frac{b}{a}x$."], sol)


def elc1(r):
    h, k = r.randint(-5, 5), r.randint(-5, 5)
    a, bb = r.randint(2, 6), r.randint(2, 6)
    if a == bb:
        return None
    A, Bc = bb * bb, a * a
    D, E = -2 * A * h, -2 * Bc * k
    Fc = A * h * h + Bc * k * k - a * a * bb * bb
    p = f"What is the length of the major axis of the ellipse ${A}x^2 + {Bc}y^2 {'+' if D >= 0 else '-'} {abs(D)}x {'+' if E >= 0 else '-'} {abs(E)}y {'+' if Fc >= 0 else '-'} {abs(Fc)} = 0$?"
    ans = 2 * max(a, bb)
    sol = explain("the length of the longer axis.", "complete the square in $x$ and $y$ (after factoring out the coefficients), then divide to get the standard form.",
                  [f"${A}(x^2 {sgn(-2 * h)} {abs(2 * h)}x) + {Bc}(y^2 {sgn(-2 * k)} {abs(2 * k)}y) = {-Fc}$.",
                   f"Complete squares: ${A}{sq_shift(h, 'x')}^2 + {Bc}{sq_shift(k, 'y')}^2 = {-Fc} + {A * h * h} + {Bc * k * k} = {a * a * bb * bb}$.",
                   f"Divide by ${a * a * bb * bb}$: $\\frac{{{sq_shift(h, 'x')}^2}}{{{a * a}}} + \\frac{{{sq_shift(k, 'y')}^2}}{{{bb * bb}}} = 1$.",
                   f"Semi-axes ${a}$ and ${bb}$; the larger is ${max(a, bb)}$, so the major axis is $2 \\cdot {max(a, bb)} = {ans}$."],
                  f"${ans}$.", "answering the semi-major axis instead of the full axis.")
    return (p, ans, [max(a, bb), 2 * min(a, bb), a + bb, ans * 2, max(a, bb) ** 2], ["Complete the square, then divide to get the form $\\frac{(x - h)^2}{a^2} + \\frac{(y - k)^2}{b^2} = 1$."], sol)


def elc2(r):
    a, bb, c = r.choice([(5, 3, 4), (5, 4, 3), (13, 5, 12), (10, 6, 8), (17, 8, 15)])
    p = f"Point $P$ lies on the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{bb * bb}}} = 1$, and $F_1$ and $F_2$ are its foci. What is $PF_1 + PF_2$?"
    sol = explain("$PF_1 + PF_2$.", "this is the definition of an ellipse: the sum of the distances to the two foci is the same for every point, and equals the major axis $2a$.",
                  [f"Check at the vertex $({a}, 0)$: the foci are at $(\\pm {c}, 0)$ since $c^2 = {a * a} - {bb * bb}$. Distances: ${a - c}$ and ${a + c}$, which add to ${2 * a}$.",
                   f"So for every $P$ on the ellipse, $PF_1 + PF_2 = 2a = {2 * a}$."],
                  f"${2 * a}$.", "using the minor axis $2b$.")
    return (p, 2 * a, [2 * bb, 2 * c, a + bb, a + c, 2 * a + 1], ["The sum of distances from any point on an ellipse to its foci is the length of the major axis."], sol)


def elc3(r):
    a, bb, c = r.choice([(5, 3, 4), (5, 4, 3), (13, 5, 12), (13, 12, 5), (10, 6, 8), (17, 8, 15), (25, 7, 24)])
    ans = F(c, a)
    p = f"What is the eccentricity of the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{bb * bb}}} = 1$?"
    sol = explain("the eccentricity $e = \\frac{c}{a}$.", "eccentricity measures how stretched the ellipse is: focus distance over semi-major axis. $0$ is a circle; close to $1$ is very flat.",
                  [f"$a = {a}$, $b = {bb}$.", f"$c = \\sqrt{{{a * a} - {bb * bb}}} = {c}$.", f"$e = \\frac{{{c}}}{{{a}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "dividing by $b$ instead of $a$.")
    return (p, ans, [F(bb, a), F(c, bb), F(a, c), F(bb, c), 1 - ans if 1 - ans != ans else F(1, 3)], ["Eccentricity is $e = \\frac{c}{a}$, with $c^2 = a^2 - b^2$."], sol)


b.fill_unique("basics", [el1, el2, el3, el4] + MORE[b.skill_id]["basics"], 5501)
b.fill_unique("challenge", [elc1, elc2, elc3] + MORE[b.skill_id]["challenge"], 5502)


# ---------------------------------------------------------------- 3D and analytic geometry
b = bank("con_analytic")


QUADS = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17), (8, 9, 12, 17)]


def an1_(r):
    a, bb, c, d = r.choice(QUADS)
    k = r.randint(1, 2)
    P = [r.randint(-5, 5) for _ in range(3)]
    sg = [r.choice([1, -1]) for _ in range(3)]
    dl = [a * k, bb * k, c * k]
    r.shuffle(dl)
    Q = [P[i] + sg[i] * dl[i] for i in range(3)]
    s2 = sum(x * x for x in dl)
    p = f"What is the distance between $({P[0]}, {P[1]}, {P[2]})$ and $({Q[0]}, {Q[1]}, {Q[2]})$?"
    sol = explain("the 3D distance.", "the distance formula in three dimensions: $\\sqrt{(\\Delta x)^2 + (\\Delta y)^2 + (\\Delta z)^2}$. (It is the Pythagorean Theorem used twice.)",
                  [f"Differences: $\\Delta x = {Q[0] - P[0]}$, $\\Delta y = {Q[1] - P[1]}$, $\\Delta z = {Q[2] - P[2]}$.", f"Squares: ${dl[0] ** 2} + {dl[1] ** 2} + {dl[2] ** 2} = {s2}$.", f"$\\sqrt{{{s2}}} = {d * k}$."],
                  f"${d * k}$.", "adding the differences without squaring them.")
    return (p, d * k, [(a + bb + c) * k, d * k + 1, d * k - 1, c * k + 1, (d + 1) * k], ["$\\sqrt{(\\Delta x)^2 + (\\Delta y)^2 + (\\Delta z)^2}$."], sol)


def an2_(r):
    x, y = r.randint(-9, 9), r.randint(-9, 9)
    kind = r.choice(["y=x", "y=-x", "x=k", "y=k"])
    k = r.randint(-5, 5)
    if kind == "y=x":
        img, line = (y, x), "y = x"
        rule = "Reflecting over $y = x$ swaps the coordinates: $(a, b) \\to (b, a)$."
    elif kind == "y=-x":
        img, line = (-y, -x), "y = -x"
        rule = "Reflecting over $y = -x$ swaps and negates: $(a, b) \\to (-b, -a)$."
    elif kind == "x=k":
        img, line = (2 * k - x, y), f"x = {k}"
        rule = f"Reflecting over the vertical line $x = {k}$ keeps $y$. The new $x$ is as far past ${k}$ as the old one was before it: $x' = 2 \\cdot {k} - x$."
    else:
        img, line = (x, 2 * k - y), f"y = {k}"
        rule = f"Reflecting over the horizontal line $y = {k}$ keeps $x$. The new $y$ is $y' = 2 \\cdot {k} - y$."
    ans = img[0] + img[1]
    p = f"The point $({x}, {y})$ is reflected over the line ${line}$. What is the sum of the coordinates of its image?"
    sol = explain("the coordinate sum of the reflected point.", "a reflection puts the image the same distance from the line on the other side.",
                  [rule, f"Image: $({img[0]}, {img[1]})$.", f"Sum: ${img[0]} + ({img[1]}) = {ans}$."],
                  f"${ans}$.", "mixing up the rules for $y = x$ and $y = -x$.")
    return (p, ans, [x + y, -(x + y) if -(x + y) != ans else ans + 2, ans + 1, x - y, y - x], ["Picture the reflection, or use the rule for that line."], sol)


def an3_(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    if y1 == y2 or x1 == x2:
        return None
    m = F(y2 - y1, x2 - x1)
    xi = x1 - y1 / m
    p = f"Where does the line through $({x1}, {y1})$ and $({x2}, {y2})$ cross the $x$-axis? (Give the $x$-coordinate.)"
    sol = explain("the $x$-intercept.", "find the slope, write the line in point slope form, then set $y = 0$.",
                  [f"Slope: $m = \\frac{{{y2} - ({y1})}}{{{x2} - ({x1})}} = {num(m).tex}$.", f"Line: $y - ({y1}) = {num(m).tex}(x - ({x1}))$.",
                   f"Set $y = 0$: $-({y1}) = {num(m).tex}(x - ({x1}))$, so $x = {x1} - \\frac{{{y1}}}{{{num(m).tex}}} = {num(xi).tex}$."],
                  f"${num(xi).tex}$.", "finding the $y$-intercept (set $x = 0$) instead.")
    return (p, xi, [-xi if xi else 1, y1 - m * x1, xi + 1, m, x1 + x2], ["Find the equation of the line, then set $y = 0$."], sol)


def an4_(r):
    x, y = r.randint(-6, 6), r.randint(-6, 6)
    a1, b1, a2, b2 = r.randint(1, 5), r.randint(-5, 5), r.randint(-5, 5), r.randint(1, 5)
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    p = f"At what point do the lines ${a1}x {'+' if b1 >= 0 else '-'} {abs(b1)}y = {c1}$ and ${a2}x {'+' if b2 >= 0 else '-'} {abs(b2)}y = {c2}$ meet? Give the product of its coordinates."
    sol = explain("the intersection point, then $xy$.", "solve the system by elimination: scale the equations so one variable cancels.",
                  [f"Multiply the first by ${b2}$ and the second by ${b1}$, then subtract: $({a1} \\cdot {b2} - {par(a2)} \\cdot ({b1}))x = {c1} \\cdot {b2} - {par(c2)} \\cdot ({b1})$.",
                   f"${det}x = {c1 * b2 - c2 * b1}$, so $x = {x}$.", f"Substitute into the first equation: ${a1}({x}) {'+' if b1 >= 0 else '-'} {abs(b1)}y = {c1}$ gives $y = {y}$.", f"Product: $({x})({y}) = {x * y}$."],
                  f"${x * y}$.", "adding the coordinates instead of multiplying.")
    return (p, x * y, [x + y, x - y, -x * y if x * y else 2, x * y + 1, c1 * c2 if abs(c1 * c2) < 500 else x * y + 5], ["Solve the system."], sol)


def anc1_(r):
    a, bb, c = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)
    v = F(a * bb * c, 6)
    p = f"What is the volume of the tetrahedron with vertices $(0, 0, 0)$, $({a}, 0, 0)$, $(0, {bb}, 0)$, and $(0, 0, {c})$?"
    sol = explain("the volume of a corner tetrahedron.", "a tetrahedron is a pyramid: $V = \\frac{1}{3} \\cdot \\text{base area} \\cdot \\text{height}$.",
                  [f"Base: the right triangle in the $xy$-plane with legs ${a}$ and ${bb}$, area $\\frac{{{a} \\cdot {bb}}}{{2}} = {num(F(a * bb, 2)).tex}$.", f"Height: the distance up the $z$-axis, ${c}$.",
                   f"$V = \\frac{{1}}{{3}} \\cdot {num(F(a * bb, 2)).tex} \\cdot {c} = {num(v).tex}$."],
                  f"${num(v).tex}$.", "forgetting the $\\frac{1}{3}$ for a pyramid (that gives a prism's volume).")
    return (p, v, [a * bb * c, F(a * bb * c, 3), F(a * bb * c, 2), v + 1, F(a + bb + c, 6)], ["Volume of a pyramid is $\\frac{1}{3} \\cdot$ base area $\\cdot$ height."], sol)


def anc2_(r):
    combos = [(2, 3, 6), (1, 2, 2), (4, 4, 2), (3, 4, 12), (2, 2, 1), (6, 3, 2), (4, 6, 12)]
    a, bb, c = r.choice(combos)
    val2 = a * a * bb * bb + bb * bb * c * c + c * c * a * a
    ans = surd(F(1, 2), val2)
    p = f"What is the area of the triangle with vertices $({a}, 0, 0)$, $(0, {bb}, 0)$, and $(0, 0, {c})$?"
    sol = explain("the area of the slanted triangle.", "3D Pythagorean Theorem (de Gua's Theorem): for a corner tetrahedron, the square of the slanted face's area equals the sum of the squares of the three right triangle faces.",
                  [f"Right faces: $\\frac{{{a} \\cdot {bb}}}{{2}}$, $\\frac{{{bb} \\cdot {c}}}{{2}}$, $\\frac{{{c} \\cdot {a}}}{{2}}$.",
                   f"Area$^2 = \\frac{{{a * a * bb * bb} + {bb * bb * c * c} + {c * c * a * a}}}{{4}} = \\frac{{{val2}}}{{4}}$.", f"Area $= \\frac{{\\sqrt{{{val2}}}}}{{2}} = {ans.tex}$."],
                  f"${ans.tex}$.", "adding the three face areas instead of their squares.")
    return (p, ans, [num(F(a * bb * c, 2)), surd(1, val2), num(F(a * bb + bb * c + c * a, 2)), surd(F(1, 2), a * a + bb * bb + c * c), num(F(a * bb * c, 6))],
            ["The squared area of this triangle equals the sum of the squared areas of its three projections onto the coordinate planes."], sol)


def anc3_(r):
    n = r.choice([25, 50, 65, 85, 100, 125, 130, 169, 25 * 2, 5, 10, 13, 65, 145])
    cnt = sum(1 for x in range(-20, 21) for y in range(-20, 21) if x * x + y * y == n)
    reps = sorted({tuple(sorted((abs(x), abs(y)))) for x in range(-20, 21) for y in range(-20, 21) if x * x + y * y == n})
    lines = []
    for x, y in reps:
        k = 4 if (x == 0 or x == y) else 8
        why = "signs only" if x == 0 else "signs, and the order is the same" if x == y else "$4$ sign choices times $2$ orders"
        lines.append(f"${x}^2 + {y}^2$: ${k}$ points ({why})")
    p = f"How many points with integer coordinates lie on the circle $x^2 + y^2 = {n}$?"
    sol = explain(f"all integer pairs $(x, y)$ with $x^2 + y^2 = {n}$.", "list the ways to write the number as a sum of two squares, then count sign and order choices for each.",
                  [f"Check every $x$ with $x^2 \\le {n}$ to find the sums of two squares: " + ", ".join(f"${x}^2 + {y}^2$" for x, y in reps) + ".", "; ".join(lines) + ".", f"Total: ${cnt}$."],
                  f"${cnt}$.", "forgetting the negative coordinates, or the swapped order $(y, x)$.")
    return (p, cnt, [cnt // 2, cnt + 4, cnt - 4 if cnt > 4 else cnt + 8, 4, cnt * 2], ["List the ways to write the number as a sum of two squares, then count signs and orders."], sol)


b.fill_unique("basics", [an1_, an2_, an3_, an4_] + MORE[b.skill_id]["basics"], 5601)
b.fill_unique("challenge", [anc1_, anc2_, anc3_] + MORE[b.skill_id]["challenge"], 5602)


# ---------------------------------------------------------------- recursive sequences
b = bank("ser_recursion")


def rc1(r):
    a1, a2 = r.randint(1, 5), r.randint(1, 5)
    n = r.randint(6, 10)
    s = [a1, a2]
    while len(s) < n:
        s.append(s[-1] + s[-2])
    p = f"A sequence has $a_1 = {a1}$, $a_2 = {a2}$, and $a_n = a_{{n-1}} + a_{{n-2}}$ for $n \\ge 3$. What is $a_{{{n}}}$?"
    sol = explain(f"the ${n}$th term.", "each term is the sum of the two before it. Build the list one term at a time.",
                  [f"$a_3 = {s[1]} + {s[0]} = {s[2]}$, $a_4 = {s[2]} + {s[1]} = {s[3]}$, and so on.", "Terms: " + ", ".join(f"$a_{{{i + 1}}} = {v}$" for i, v in enumerate(s)) + "."],
                  f"${s[-1]}$.", "stopping one term early or late; count the index carefully.")
    return (p, s[-1], [s[-2], s[-1] + s[-3], s[-1] + 1, s[-1] * 2 - s[-2], sum(s[-3:])], ["Compute the terms one at a time."], sol)


def rc2(r):
    a1 = r.randint(1, 5)
    m, c = r.randint(2, 3), r.randint(-3, 4)
    n = r.randint(4, 7)
    s = [a1]
    while len(s) < n:
        s.append(m * s[-1] + c)
    p = f"If $a_1 = {a1}$ and $a_{{n+1}} = {m}a_n {'+' if c >= 0 else '-'} {abs(c)}$, what is $a_{{{n}}}$?"
    sol = explain(f"$a_{{{n}}}$.", f"apply the rule (multiply by ${m}$, then {'add' if c >= 0 else 'subtract'} ${abs(c)}$) over and over.",
                  [f"$a_{{{i + 2}}} = {m} \\cdot {pr(s[i])} {'+' if c >= 0 else '-'} {abs(c)} = {s[i + 1]}$" for i in range(len(s) - 1)],
                  f"${s[-1]}$.", f"adding ${abs(c)}$ before multiplying; the order in the rule matters.")
    return (p, s[-1], [s[-2], s[-1] + c, m * s[-1], s[-1] - 1, s[-1] + m], ["Apply the rule repeatedly."], sol)


def rc3(r):
    a1, a2 = r.randint(-5, 9), r.randint(-5, 9)
    n = r.randint(20, 400)
    s = [a1, a2]
    for _ in range(10):
        s.append(s[-1] - s[-2])
    ans = s[(n - 1) % 6]
    pos = (n - 1) % 6 + 1
    p = f"A sequence has $a_1 = {a1}$, $a_2 = {a2}$, and $a_{{n}} = a_{{n-1}} - a_{{n-2}}$ for $n \\ge 3$. What is $a_{{{n}}}$?"
    sol = explain(f"$a_{{{n}}}$, far down the sequence.", "a far term almost always means the sequence repeats. Write out terms until you see the start again.",
                  ["Terms: " + ", ".join(f"$a_{{{i + 1}}} = {v}$" for i, v in enumerate(s[:8])) + ".", f"$a_7 = a_1$ and $a_8 = a_2$, so the sequence repeats every $6$ terms.",
                   f"${n} = 6 \\cdot {(n - 1) // 6} + {pos}$, so $a_{{{n}}} = a_{{{pos}}} = {ans}$."],
                  f"${ans}$.", "an off by one error when matching the remainder to a position.")
    return (p, ans, [s[n % 6], s[(n + 1) % 6], -ans if ans else 3, a1 + a2, ans + 1], ["Write out the first eight terms and look for a cycle."], sol)


def rc4(r):
    k = r.randint(1, 4)
    c = r.randint(-5, 5)
    n = r.randint(5, 30)
    ans = k * (2 * n - 1) + c
    Sn, Sm = k * n * n + c * n, k * (n - 1) ** 2 + c * (n - 1)
    p = f"The sum of the first $n$ terms of a sequence is $S_n = {k if k > 1 else ''}n^2 {'+' if c >= 0 else '-'} {abs(c)}n$ for every $n$. What is the ${n}$th term?"
    sol = explain(f"the single term $a_{{{n}}}$.", f"$S_{{{n}}}$ and $S_{{{n - 1}}}$ contain the same terms except the last one, so $a_n = S_n - S_{{n-1}}$.",
                  [f"$S_{{{n}}} = {k} \\cdot {n}^2 {'+' if c >= 0 else '-'} {abs(c)} \\cdot {n} = {Sn}$.", f"$S_{{{n - 1}}} = {k} \\cdot {n - 1}^2 {'+' if c >= 0 else '-'} {abs(c)} \\cdot {n - 1} = {Sm}$.", f"$a_{{{n}}} = {Sn} - ({Sm}) = {ans}$."],
                  f"${ans}$.", f"answering $S_{{{n}}}$, which is the sum of all ${n}$ terms.")
    return (p, ans, [k * n * n + c * n, ans + 2 * k, k * 2 * n + c, ans - 1, k * n + c], ["$a_n = S_n - S_{n-1}$."], sol)


def rcc1(r):
    c = r.randint(1, 10)
    n = r.randint(10, 60)
    ans = c + (n - 1) * n // 2
    p = f"If $a_1 = {c}$ and $a_{{n+1}} = a_n + n$ for $n \\ge 1$, what is $a_{{{n}}}$?"
    sol = explain(f"$a_{{{n}}}$.", "each step adds the current index. Stack the steps: $a_n = a_1 + 1 + 2 + \\cdots + (n - 1)$.",
                  [f"$a_2 = a_1 + 1$, $a_3 = a_2 + 2$, ..., $a_{{{n}}} = a_{{{n - 1}}} + {n - 1}$.", f"Adding all these: $a_{{{n}}} = {c} + (1 + 2 + \\cdots + {n - 1})$.",
                   f"$1 + 2 + \\cdots + {n - 1} = \\frac{{{n - 1} \\cdot {n}}}{{2}} = {(n - 1) * n // 2}$.", f"$a_{{{n}}} = {c} + {(n - 1) * n // 2} = {ans}$."],
                  f"${ans}$.", f"adding up to ${n}$ instead of ${n - 1}$.")
    return (p, ans, [c + n * (n + 1) // 2, c + n, ans + n, c + (n - 1) * (n - 2) // 2, n * n], ["$a_n = a_1 + (1 + 2 + \\cdots + (n - 1))$."], sol)


def rcc2(r):
    k = r.randint(2, 5)
    n = r.randint(8, 30)
    s = [1]
    for i in range(2, n + 1):
        s.append(s[-1] * k + 1)
    ans = s[-1] % 10
    digs = [v % 10 for v in s]
    per = next(pp for pp in range(1, 11) if all(digs[i] == digs[i + pp] for i in range(1, len(digs) - pp)))
    p = f"If $a_1 = 1$ and $a_n = {k}a_{{n-1}} + 1$ for $n \\ge 2$, what is the units digit of $a_{{{n}}}$?"
    sol = explain(f"the last digit of $a_{{{n}}}$.", "the units digit of $a_n$ depends only on the units digit of $a_{n-1}$, so track only last digits and look for a repeat.",
                  ["Units digits of $a_1, a_2, \\ldots$: " + ", ".join(str(dg) for dg in digs[:min(len(digs), 12)]) + (", and so on." if len(digs) > 12 else "."),
                   f"From $a_2$ on, they repeat every ${per}$ term{'s' if per != 1 else ''}.", f"Following the cycle to $n = {n}$ gives units digit ${ans}$."],
                  f"${ans}$.", f"trying to compute $a_{{{n}}}$ in full; it has many digits. (In fact $a_n = " + (f"2^n - 1" if k == 2 else f"\\frac{{{k}^n - 1}}{{{k - 1}}}") + "$.)")
    return (p, ans, [d for d in range(10) if d != ans][:5], ["Track only the units digit, and look for a cycle."], sol)


def rcc3(r):
    x, y = r.randint(1, 6), r.randint(1, 6)
    n = r.randint(10, 300)
    s = [F(x), F(y)]
    for _ in range(10):
        s.append((s[-1] + 1) / s[-2])
    ans = s[(n - 1) % 5]
    pos = (n - 1) % 5 + 1
    p = f"A sequence has $a_1 = {x}$, $a_2 = {y}$, and $a_{{n+2}} = \\dfrac{{a_{{n+1}} + 1}}{{a_n}}$. What is $a_{{{n}}}$?"
    sol = explain(f"$a_{{{n}}}$.", "compute terms until the first two values come back; then the whole sequence repeats.",
                  ["Terms: " + ", ".join(f"$a_{{{i + 1}}} = {num(t).tex}$" for i, t in enumerate(s[:7])) + ".", "$a_6 = a_1$ and $a_7 = a_2$, so the period is $5$.",
                   f"${n} = 5 \\cdot {(n - 1) // 5} + {pos}$, so $a_{{{n}}} = a_{{{pos}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "an arithmetic slip in the fractions; double check each term.")
    return (p, ans, [s[n % 5], s[(n + 1) % 5], s[(n + 2) % 5], ans + 1, F(1, 2) if ans != F(1, 2) else 3], ["Compute terms until the sequence repeats."], sol)


b.fill_unique("basics", [rc1, rc2, rc3, rc4] + MORE[b.skill_id]["basics"], 5701)
b.fill_unique("challenge", [rcc1, rcc2, rcc3] + MORE[b.skill_id]["challenge"], 5702)


# ---------------------------------------------------------------- telescoping sums
b = bank("ser_telescoping")


def tsc1(r):
    n = r.randint(5, 100)
    ans = F(n, n + 1)
    p = f"What is $\\dfrac{{1}}{{1 \\cdot 2}} + \\dfrac{{1}}{{2 \\cdot 3}} + \\cdots + \\dfrac{{1}}{{{n} \\cdot {n + 1}}}$?"
    sol = explain("the sum.", "partial fractions: $\\frac{1}{k(k + 1)} = \\frac{1}{k} - \\frac{1}{k + 1}$. Written this way, neighboring terms cancel.",
                  [f"Rewrite: $\\left(1 - \\frac{{1}}{{2}}\\right) + \\left(\\frac{{1}}{{2}} - \\frac{{1}}{{3}}\\right) + \\cdots + \\left(\\frac{{1}}{{{n}}} - \\frac{{1}}{{{n + 1}}}\\right)$.",
                   "Each $-\\frac{1}{k}$ cancels the next $+\\frac{1}{k}$.", f"Only the first and last pieces survive: $1 - \\frac{{1}}{{{n + 1}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"stopping at $\\frac{{1}}{{{n}}}$ instead of $\\frac{{1}}{{{n + 1}}}$.")
    return (p, ans, [F(n - 1, n), F(1, n + 1), F(n + 1, n + 2), F(n, n + 2), F(1, 2)], ["$\\frac{1}{k(k + 1)} = \\frac{1}{k} - \\frac{1}{k + 1}$."], sol)


def tsc2(r):
    n = r.randint(5, 50)
    ans = F(n, 2 * n + 1)
    p = f"What is $\\dfrac{{1}}{{1 \\cdot 3}} + \\dfrac{{1}}{{3 \\cdot 5}} + \\cdots + \\dfrac{{1}}{{{2 * n - 1} \\cdot {2 * n + 1}}}$?"
    sol = explain("the sum.", "partial fractions with a gap of $2$: $\\frac{1}{(2k - 1)(2k + 1)} = \\frac{1}{2}\\left(\\frac{1}{2k - 1} - \\frac{1}{2k + 1}\\right)$. The $\\frac{1}{2}$ undoes the gap.",
                  [f"Rewrite: $\\frac{{1}}{{2}}\\left[\\left(1 - \\frac{{1}}{{3}}\\right) + \\left(\\frac{{1}}{{3}} - \\frac{{1}}{{5}}\\right) + \\cdots + \\left(\\frac{{1}}{{{2 * n - 1}}} - \\frac{{1}}{{{2 * n + 1}}}\\right)\\right]$.",
                   f"Everything in the middle cancels, leaving $\\frac{{1}}{{2}}\\left(1 - \\frac{{1}}{{{2 * n + 1}}}\\right)$.", f"$= \\frac{{1}}{{2}} \\cdot \\frac{{{2 * n}}}{{{2 * n + 1}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting the factor $\\frac{1}{2}$ in the partial fractions.")
    return (p, ans, [F(n, 2 * n - 1), F(2 * n, 2 * n + 1), F(1, 2), F(n + 1, 2 * n + 1), ans * 2], ["$\\frac{1}{(2k - 1)(2k + 1)} = \\frac{1}{2}\\left(\\frac{1}{2k - 1} - \\frac{1}{2k + 1}\\right)$."], sol)


def tsc3(r):
    n = r.randint(5, 99)
    ans = n + 1
    p = f"What is $\\left(1 + \\dfrac{{1}}{{1}}\\right)\\left(1 + \\dfrac{{1}}{{2}}\\right)\\cdots\\left(1 + \\dfrac{{1}}{{{n}}}\\right)$?"
    sol = explain("the product.", "write each factor as a single fraction: $1 + \\frac{1}{k} = \\frac{k + 1}{k}$. Each numerator cancels the next denominator.",
                  [f"Product: $\\frac{{2}}{{1}} \\cdot \\frac{{3}}{{2}} \\cdot \\frac{{4}}{{3}} \\cdots \\frac{{{n + 1}}}{{{n}}}$.", "The $2$ on top cancels the $2$ below, the $3$ cancels the $3$, and so on.",
                   f"What survives: $\\frac{{{n + 1}}}{{1}} = {n + 1}$."],
                  f"${n + 1}$.", f"answering ${n}$; the last numerator is ${n + 1}$.")
    return (p, ans, [n, n + 2, F(n + 1, 2), 2 ** n if n < 10 else 2 * n, F(n, n + 1)], ["Write each factor as $\\frac{k + 1}{k}$."], sol)


def tsc4(r):
    n = r.randint(5, 99)
    ans = F(n + 1, 2 * n)
    p = f"What is $\\left(1 - \\dfrac{{1}}{{2^2}}\\right)\\left(1 - \\dfrac{{1}}{{3^2}}\\right)\\cdots\\left(1 - \\dfrac{{1}}{{{n}^2}}\\right)$?"
    sol = explain("the product.", "difference of squares: $1 - \\frac{1}{k^2} = \\frac{(k - 1)(k + 1)}{k \\cdot k}$. Split into two products that each telescope.",
                  [f"Product $= \\left(\\frac{{1}}{{2}} \\cdot \\frac{{2}}{{3}} \\cdots \\frac{{{n - 1}}}{{{n}}}\\right) \\cdot \\left(\\frac{{3}}{{2}} \\cdot \\frac{{4}}{{3}} \\cdots \\frac{{{n + 1}}}{{{n}}}\\right)$.",
                   f"The first part telescopes to $\\frac{{1}}{{{n}}}$; the second to $\\frac{{{n + 1}}}{{2}}$.", f"Multiply: $\\frac{{1}}{{{n}}} \\cdot \\frac{{{n + 1}}}{{2}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "cancelling only one of the two chains and getting $\\frac{1}{n}$ or $\\frac{n + 1}{2}$.")
    return (p, ans, [F(1, 2), F(n - 1, n), F(1, n), F(n + 1, n), F(n, 2 * n + 2)], ["Factor each term: $1 - \\frac{1}{k^2} = \\frac{(k - 1)(k + 1)}{k \\cdot k}$."], sol)


def tscc1(r):
    n = r.randint(5, 40)
    s = sum(F(1, k * (k + 2)) for k in range(1, n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\dfrac{{1}}{{k(k + 2)}}$?"
    sol = explain("the sum.", "partial fractions: $\\frac{1}{k(k + 2)} = \\frac{1}{2}\\left(\\frac{1}{k} - \\frac{1}{k + 2}\\right)$. With a gap of $2$, terms cancel two places apart, so two survive at each end.",
                  [f"Write out: $\\frac{{1}}{{2}}\\left[\\left(1 - \\frac{{1}}{{3}}\\right) + \\left(\\frac{{1}}{{2}} - \\frac{{1}}{{4}}\\right) + \\left(\\frac{{1}}{{3}} - \\frac{{1}}{{5}}\\right) + \\cdots + \\left(\\frac{{1}}{{{n}}} - \\frac{{1}}{{{n + 2}}}\\right)\\right]$.",
                   f"Surviving: $+1$ and $+\\frac{{1}}{{2}}$ at the start; $-\\frac{{1}}{{{n + 1}}}$ and $-\\frac{{1}}{{{n + 2}}}$ at the end.",
                   f"$\\frac{{1}}{{2}}\\left(1 + \\frac{{1}}{{2}} - \\frac{{1}}{{{n + 1}}} - \\frac{{1}}{{{n + 2}}}\\right) = {num(s).tex}$."],
                  f"${num(s).tex}$.", "keeping only one surviving term at each end; with a gap of $2$ there are two.")
    return (p, s, [F(3, 4), s + F(1, n), F(n, n + 2), F(1, 2) * (1 - F(1, n + 2)), s - F(1, 2 * (n + 1))],
            ["$\\frac{1}{k(k + 2)} = \\frac{1}{2}\\left(\\frac{1}{k} - \\frac{1}{k + 2}\\right)$. Two terms survive at each end."], sol)


def tscc2(r):
    m = r.randint(3, 20)
    n = m * m - 1
    ans = m - 1
    p = f"What is $\\dfrac{{1}}{{\\sqrt{{1}} + \\sqrt{{2}}}} + \\dfrac{{1}}{{\\sqrt{{2}} + \\sqrt{{3}}}} + \\cdots + \\dfrac{{1}}{{\\sqrt{{{n}}} + \\sqrt{{{n + 1}}}}}$?"
    sol = explain("the sum.", "rationalize each term by multiplying by the conjugate. Each term becomes a difference of square roots, and the sum telescopes.",
                  ["$\\frac{1}{\\sqrt{k} + \\sqrt{k + 1}} \\cdot \\frac{\\sqrt{k + 1} - \\sqrt{k}}{\\sqrt{k + 1} - \\sqrt{k}} = \\frac{\\sqrt{k + 1} - \\sqrt{k}}{(k + 1) - k} = \\sqrt{k + 1} - \\sqrt{k}$.",
                   f"Sum: $(\\sqrt{{2}} - \\sqrt{{1}}) + (\\sqrt{{3}} - \\sqrt{{2}}) + \\cdots + (\\sqrt{{{n + 1}}} - \\sqrt{{{n}}})$.", f"Everything cancels except $\\sqrt{{{n + 1}}} - 1 = {m} - 1 = {ans}$."],
                  f"${ans}$.", f"forgetting to subtract the $\\sqrt{{1}} = 1$ at the start.")
    return (p, ans, [m, m + 1, ans * 2, F(m, 2), m * m - 1], ["Rationalize each denominator."], sol)


def tscc3(r):
    n = r.randint(4, 9)
    ans = math.factorial(n + 1) - 1
    p = f"What is $1 \\cdot 1! + 2 \\cdot 2! + 3 \\cdot 3! + \\cdots + {n} \\cdot {n}!$?"
    sol = explain("the sum.", "rewrite each term as a difference of factorials: $k \\cdot k! = (k + 1 - 1)k! = (k + 1)! - k!$.",
                  [f"Sum: $(2! - 1!) + (3! - 2!) + \\cdots + ({n + 1}! - {n}!)$.", f"Everything cancels except ${n + 1}! - 1!$.", f"${n + 1}! - 1 = {math.factorial(n + 1)} - 1 = {ans}$."],
                  f"${ans}$.", f"answering ${n + 1}!$ and forgetting the $-1$.")
    return (p, ans, [math.factorial(n + 1), math.factorial(n) * n, ans - n, math.factorial(n + 1) + 1, math.factorial(n + 2) // 2], ["$k \\cdot k! = (k + 1)! - k!$."], sol)


b.fill_unique("basics", [tsc1, tsc2, tsc3, tsc4] + MORE[b.skill_id]["basics"], 5801)
b.fill_unique("challenge", [tscc1, tscc2, tscc3] + MORE[b.skill_id]["challenge"], 5802)


# ---------------------------------------------------------------- infinite geometric series
b = bank("ser_geometric")


def ig1(r):
    a = r.randint(1, 20)
    rr = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2), F(-1, 3), F(1, 5), F(2, 5)])
    s = a / (1 - rr)
    p = f"What is the sum of the infinite geometric series ${a} + {num(a * rr).tex} + {num(a * rr * rr).tex} + \\cdots$?"
    sol = explain("the sum of the whole infinite series.", "an infinite geometric series with $|r| < 1$ adds up to $S = \\frac{a}{1 - r}$.",
                  [f"First term $a = {a}$. Ratio: $r = \\frac{{{num(a * rr).tex}}}{{{a}}} = {num(rr).tex}$, and $|r| < 1$.", f"$1 - r = 1 - \\left({num(rr).tex}\\right) = {num(1 - rr).tex}$.", f"$S = \\frac{{{a}}}{{{num(1 - rr).tex}}} = {num(s).tex}$."],
                  f"${num(s).tex}$.", "using $1 + r$ in the denominator, especially when $r$ is negative.")
    return (p, s, [a / (1 + rr), a * (1 - rr), s + a, 2 * a, s - rr], ["$S = \\frac{a}{1 - r}$ when $|r| < 1$."], sol)


def ig2(r):
    digits = r.randint(1, 3)
    rep = r.randint(1, 10 ** digits - 2)
    s = F(rep, 10 ** digits - 1)
    rs = str(rep).zfill(digits)
    D = 10 ** digits
    p = f"The repeating decimal $0.\\overline{{{rs}}}$ equals a fraction in lowest terms. What is the fraction?"
    sol = explain("the fraction in lowest terms.", f"multiplying by $10^{{{digits}}}$ shifts the decimal by one full block of the repeat, so subtracting removes the endless tail.",
                  [f"Let $x = 0.\\overline{{{rs}}}$. Then ${D}x = {rep}.\\overline{{{rs}}}$.", f"Subtract: ${D}x - x = {rep}$, so ${D - 1}x = {rep}$ and $x = \\frac{{{rep}}}{{{D - 1}}}$.",
                   f"Reduce (divide by ${math.gcd(rep, D - 1)}$): ${num(s).tex}$."],
                  f"${num(s).tex}$.", f"writing $\\frac{{{rep}}}{{{D}}}$, which is the terminating decimal $0.{rs}$.")
    return (p, s, [F(rep, 10 ** digits), F(rep, 10 ** digits + 1), F(rep + 1, 10 ** digits - 1), s * 2 if s < F(1, 2) else s / 2, F(rep, 9)], [f"Let $x = 0.\\overline{{{rs}}}$ and multiply by $10^{{{digits}}}$."], sol)


def ig3(r):
    rr = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2)])
    a = r.randint(1, 20)
    s = a / (1 - rr)
    p = f"An infinite geometric series has common ratio ${num(rr).tex}$ and sum ${num(s).tex}$. What is its first term?"
    sol = explain("the first term $a$.", "rearrange $S = \\frac{a}{1 - r}$ to $a = S(1 - r)$.",
                  [f"$1 - r = 1 - \\left({num(rr).tex}\\right) = {num(1 - rr).tex}$.", f"$a = {num(s).tex} \\cdot {num(1 - rr).tex} = {a}$."],
                  f"${a}$.", "multiplying by $r$ instead of $1 - r$.")
    return (p, a, [s * rr, s * (1 + rr), a + 1, s, a * 2], ["$a = S(1 - r)$."], sol)


def ig4(r):
    h = r.randint(2, 20) * 3
    rr = r.choice([F(1, 2), F(2, 3), F(1, 3), F(3, 4)])
    up = h * rr / (1 - rr)
    total = h + 2 * up
    p = f"A ball is dropped from {h} feet. Each bounce reaches ${num(rr).tex}$ of the previous height. What total distance does the ball travel before coming to rest?"
    sol = explain("the total distance, up and down.", "after the first drop, every bounce height is traveled twice (up, then down). The bounce heights form a geometric series.",
                  [f"First drop: ${h}$ feet.", f"Bounce heights: ${num(h * rr).tex}, {num(h * rr * rr).tex}, \\ldots$, a geometric series with sum $\\frac{{{num(h * rr).tex}}}{{1 - {num(rr).tex}}} = {num(up).tex}$.",
                   f"Each bounce is up and down: $2 \\cdot {num(up).tex} = {num(2 * up).tex}$.", f"Total: ${h} + {num(2 * up).tex} = {num(total).tex}$."],
                  f"${num(total).tex}$.", "counting each bounce only once (forgetting the trip back down), or doubling the first drop.")
    return (p, total, [h / (1 - rr), 2 * h / (1 - rr), total - h, h + h * rr / (1 - rr), total + h], ["After the first drop, every bounce goes up and comes back down."], sol)


def igc1(r):
    rr = r.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5)])
    s = rr / (1 - rr) ** 2
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{\\infty}} k \\left({num(rr).tex}\\right)^k$?"
    sol = explain("the sum $S = \\sum k r^k$ with $r = " + num(rr).tex + "$.", "the coefficients $1, 2, 3, \\ldots$ grow, so this isn't geometric. But $S - rS$ is, because the coefficients line up and differ by $1$.",
                  ["$S = r + 2r^2 + 3r^3 + \\cdots$ and $rS = r^2 + 2r^3 + \\cdots$.", "Subtract: $S - rS = r + r^2 + r^3 + \\cdots = \\frac{r}{1 - r}$.",
                   f"So $S = \\frac{{r}}{{(1 - r)^2}} = \\frac{{{num(rr).tex}}}{{\\left({num(1 - rr).tex}\\right)^2}} = {num(s).tex}$."],
                  f"${num(s).tex}$.", "using the plain geometric sum $\\frac{r}{1 - r}$ and ignoring the growing coefficients.")
    return (p, s, [rr / (1 - rr), 1 / (1 - rr) ** 2, s + 1, s * 2, s - rr], ["Let $S = \\sum k r^k$. Compute $S - rS$, which is a plain geometric series."], sol)


def igc2(r):
    a = r.randint(2, 12)
    r1, r2 = r.sample([F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(3, 4)], 2)
    s1, s2 = a / (1 - r1), a / (1 - r2)
    ans = s1 - s2
    p = f"Two infinite geometric series both start with ${a}$. One has ratio ${num(r1).tex}$ and the other has ratio ${num(r2).tex}$. What is the first sum minus the second?"
    sol = explain("the difference of the two sums.", "find each sum with $S = \\frac{a}{1 - r}$, then subtract.",
                  [f"First: $\\frac{{{a}}}{{1 - {num(r1).tex}}} = \\frac{{{a}}}{{{num(1 - r1).tex}}} = {num(s1).tex}$.", f"Second: $\\frac{{{a}}}{{1 - {num(r2).tex}}} = \\frac{{{a}}}{{{num(1 - r2).tex}}} = {num(s2).tex}$.",
                   f"Difference: ${num(s1).tex} - {num(s2).tex} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "subtracting in the wrong order.")
    return (p, ans, [-ans, s1, s2, ans + 1, a * (r1 - r2)], ["Compute each sum with $\\frac{a}{1 - r}$."], sol)


def igc3(r):
    a = r.randint(2, 20)
    rr = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4)])
    s_odd = a / (1 - rr * rr)
    p = f"In the infinite geometric series ${a} + {num(a * rr).tex} + {num(a * rr * rr).tex} + \\cdots$, what is the sum of the 1st, 3rd, 5th, ... terms?"
    sol = explain("the sum of every other term, starting with the first.", "skipping every other term makes a new geometric series with the same first term and ratio $r^2$.",
                  [f"Ratio $r = {num(rr).tex}$. The 1st, 3rd, 5th, ... terms are ${a}, {num(a * rr * rr).tex}, \\ldots$, with ratio $r^2 = {num(rr * rr).tex}$.",
                   f"Sum: $\\frac{{{a}}}{{1 - {num(rr * rr).tex}}} = \\frac{{{a}}}{{{num(1 - rr * rr).tex}}} = {num(s_odd).tex}$."],
                  f"${num(s_odd).tex}$.", "halving the full sum; the odd terms are bigger than the even terms, so they make up more than half.")
    return (p, s_odd, [a / (1 - rr), a / (1 + rr), s_odd * rr, s_odd + 1, a / (1 - rr) / 2], ["The odd-numbered terms form their own geometric series with ratio $r^2$."], sol)


b.fill_unique("basics", [ig1, ig2, ig3, ig4] + MORE[b.skill_id]["basics"], 5901)
b.fill_unique("challenge", [igc1, igc2, igc3] + MORE[b.skill_id]["challenge"], 5902)
