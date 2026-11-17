"""Extra AMC 12 problem types (part 3): polynomials, conics and coordinates, sequences and series."""
import itertools
import math
from fractions import Fraction as F

from algebra_more2 import rad
from amc12_more1 import PI
from common import NAMES, C, Q, comb, num, par, sg

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ft(v):
    return num(F(v)).tex


def fp(v):
    """A fraction, in parentheses when negative."""
    v = F(v)
    return f"\\left({ft(v)}\\right)" if v < 0 else ft(v)


def big(v):
    return f"{v:,}".replace(",", "{,}")


def B(v):
    return C(big(v), v)


def poly_from_roots(roots, lead=1):
    c = [F(lead)]
    for rt in roots:
        n = [F(0)] * (len(c) + 1)
        for i, a in enumerate(c):
            n[i] += a
            n[i + 1] -= a * rt
        c = n
    return c


def ptex(coefs, var="x"):
    """Polynomial LaTeX from coefficients (highest degree first)."""
    deg = len(coefs) - 1
    out = []
    for i, a in enumerate(coefs):
        a = F(a)
        if a == 0:
            continue
        e = deg - i
        mag = abs(a)
        body = ("" if mag == 1 and e > 0 else ft(mag)) + (var if e >= 1 else "") + (f"^{{{e}}}" if e > 1 else "")
        if not out:
            out.append(("-" if a < 0 else "") + body)
        else:
            out.append(("- " if a < 0 else "+ ") + body)
    return " ".join(out) if out else "0"


def peval(c, x):
    v = F(0)
    for a in c:
        v = v * x + a
    return v


# ================================================================ poly_vieta
S = "poly_vieta"


def quad(r):
    a = r.choice([1, 1, 2, 3])
    b, c = r.randint(-12, 12), r.randint(-15, 15)
    return a, b, c


@reg(S, "basics")
def pv_q_sum(r):
    a, b, c = quad(r)
    if c == 0 or b == 0:
        return None
    ask = r.choice(["sum", "product"])
    v = F(-b, a) if ask == "sum" else F(c, a)
    p = f"What is the {ask} of the roots of ${ptex([a, b, c])} = 0$?"
    return Q(p, v, [-v, F(c, a) if ask == "sum" else F(-b, a), F(b, a) if ask == "sum" else F(-c, a), v + 1, F(c, b) if F(c, b) != v else v - 1], "Vieta's formulas.",
             f"the {ask} of the roots.", "for $ax^2 + bx + c$: sum $= -\\frac{b}{a}$, product $= \\frac{c}{a}$.", [f"{ask.capitalize()}: ${ft(v)}$."], "forgetting the minus sign on the sum." if ask == "sum" else "using $-\\frac{c}{a}$.")


@reg(S, "basics")
def pv_q_recip(r):
    a, b, c = quad(r)
    if c == 0 or b == 0:
        return None
    v = F(-b, c)
    p = f"If $r$ and $s$ are the roots of ${ptex([a, b, c])} = 0$, what is $\\frac{{1}}{{r}} + \\frac{{1}}{{s}}$?"
    return Q(p, v, [-v, F(c, -b), F(a, c), v + 1, F(-b, a)], "Combine over a common denominator.",
             "the sum of reciprocals.", "$\\frac{1}{r} + \\frac{1}{s} = \\frac{r + s}{rs}$.", [f"$r + s = {ft(F(-b, a))}$, $rs = {ft(F(c, a))}$.", f"Ratio: ${ft(v)}$."], "flipping the ratio.")


@reg(S, "basics")
def pv_q_diff(r):
    p1, p2 = r.sample(range(-9, 10), 2)
    S_, P_ = p1 + p2, p1 * p2
    v = abs(p1 - p2)
    p = f"What is the positive difference between the roots of ${ptex([1, -S_, P_])} = 0$?"
    return Q(p, v, [abs(S_), v + 1, v * v, abs(P_) if abs(P_) != v else v + 2, v - 1 if v > 1 else 3], "$(r - s)^2 = (r + s)^2 - 4rs$.",
             "$|r - s|$.", "use the sum and product, or the quadratic formula.", [f"$(r - s)^2 = {S_ * S_} - {4 * P_} = {v * v}$." if P_ >= 0 else f"$(r - s)^2 = {S_ * S_} + {-4 * P_} = {v * v}$.", f"$|r - s| = {v}$."], "forgetting the factor of 4.")


@reg(S, "basics")
def pv_q_shift(r):
    a, b, c = 1, r.randint(-10, 10), r.randint(-12, 12)
    k = r.randint(1, 4) * r.choice([1, -1])
    v = c - b * k + k * k
    p = f"If $r$ and $s$ are the roots of ${ptex([1, b, c])} = 0$, what is $(r{sg(k)[1:]})(s{sg(k)[1:]})$?".replace("( ", "(").replace("+ ", "+ ")
    p = f"If $r$ and $s$ are the roots of ${ptex([1, b, c])} = 0$, what is $(r{sg(k)})(s{sg(k)})$?"
    return Q(p, v, [c + k * k, c + b * k + k * k, v + 1, c - b * k, k * k], "Expand: $rs + k(r + s) + k^2$.",
             "the product.", f"$(r + k)(s + k) = rs + k(r + s) + k^2$ with $k = {k}$.", [f"$rs = {c}$, $r + s = {-b}$.", f"${c} + {par(k)} \\cdot {par(-b)} + {k * k} = {v}$."], "using $+b$ for the sum.") if b and c else None


@reg(S, "basics")
def pv_build(r):
    s1, p1 = r.randint(-9, 9), r.randint(-12, 12)
    k = r.randint(2, 4)
    v = k * k * p1
    p = f"If $r$ and $s$ are the roots of ${ptex([1, -s1, p1])} = 0$, the monic quadratic with roots ${k}r$ and ${k}s$ is $x^2 + bx + c$. What is $c$?"
    return Q(p, v, [k * p1, -k * s1, k * k * s1 if k * k * s1 != v else v + 1, p1, v + k], "The new product is $" + str(k * k) + "rs$.",
             "$c$.", f"$c = ({k}r)({k}s) = {k * k}rs$.", [f"$rs = {p1}$, so $c = {v}$."], "multiplying the product by " + str(k) + " only once.") if s1 and p1 else None


@reg(S, "basics")
def pv_cubic_pairs(r):
    roots = [r.randint(-6, 6) for _ in range(3)]
    c = poly_from_roots(roots)
    v = c[2]
    p = f"Let $r$, $s$, $t$ be the roots of ${ptex(c)} = 0$. What is $rs + st + tr$?"
    return Q(p, v, [-v, -c[1], -c[3] if -c[3] != v else v + 1, c[1], v + 2], "Vieta: the coefficient of $x$.",
             "$rs + st + tr$.", "for monic $x^3 + ax^2 + bx + c$: $rs + st + tr = b$.", [f"It's the coefficient of $x$: ${ft(v)}$."], "flipping the sign.") if c[2] != 0 and -c[1] != c[2] else None


@reg(S, "basics")
def pv_other_sum(r):
    roots = [r.randint(-7, 7) for _ in range(3)]
    c = poly_from_roots(roots)
    k = roots[0]
    v = roots[1] + roots[2]
    p = f"One root of ${ptex(c)} = 0$ is ${k}$. What is the sum of the other two roots?"
    return Q(p, v, [-c[1], v + 2 * k if v + 2 * k != v else v + 1, -v if v else 3, roots[1] * roots[2] if roots[1] * roots[2] != v else v - 2, v + 1], "Total sum minus the known root.",
             "the sum of the other two.", "Vieta: all three roots sum to $-a$ for $x^3 + ax^2 + \\ldots$.", [f"Sum of all: ${ft(-c[1])}$.", f"Minus ${k}$: ${v}$."], "forgetting to subtract the known root.") if -c[1] != v else None


@reg(S, "basics")
def pv_missing(r):
    rt, other = r.randint(-8, 8), r.randint(-8, 8)
    if rt == 0:
        return None
    c = rt * other
    k = -(rt + other)
    p = f"One root of $x^2 + kx{sg(c)} = 0$ is ${rt}$. What is $k$?" if c else None
    if p is None:
        return None
    return Q(p, k, [-k, other, rt + other if rt + other != k else k + 1, c, k + 2], "Find the other root from the product.",
             "$k$.", f"product of roots $= {c}$, so the other root is ${other}$; then $k = -(\\text{{sum}})$.", [f"Other root: $\\frac{{{c}}}{{{rt}}} = {other}$.", f"$k = -({rt}{sg(other)[1:]}) = {k}$." if True else ""], "forgetting $k$ is minus the sum.")


@reg(S, "basics")
def pv_ratio_sum(r):
    a, b, c = 1, r.randint(-9, 9), r.randint(1, 9) * r.choice([1, -1])
    v = F(b * b - 2 * c, c)
    p = f"If $r$ and $s$ are the roots of ${ptex([1, b, c])} = 0$, what is $\\frac{{r}}{{s}} + \\frac{{s}}{{r}}$?"
    return Q(p, v, [F(b * b, c), F(b * b + 2 * c, c), v + 1, F(b * b - 2 * c, 1), F(b * b - 4 * c, c) if b * b != 6 * c else v - 1], "Common denominator: $\\frac{r^2 + s^2}{rs}$.",
             "the value.", "$r^2 + s^2 = (r + s)^2 - 2rs$.", [f"$r^2 + s^2 = {b * b} - {par(2 * c)} = {b * b - 2 * c}$.", f"Divide by $rs = {c}$: ${ft(v)}$."], "forgetting the $-2rs$.") if b else None


@reg(S, "basics")
def pv_quartic_prod(r):
    a = r.choice([1, 2, 3])
    co = [a] + [r.randint(-9, 9) for _ in range(4)]
    if co[4] == 0:
        return None
    v = F(co[4], a)
    p = f"What is the product of the four roots of ${ptex(co)} = 0$?"
    return Q(p, v, [-v, F(-co[1], a), F(co[2], a) if F(co[2], a) != v else v + 1, F(co[4]) if a != 1 else v + 2, F(co[3], a) if F(co[3], a) != v else v - 1], "Vieta for degree 4.",
             "the product of the roots.", "for degree $n$, the product is $(-1)^n \\frac{\\text{constant}}{\\text{leading}}$; here $n = 4$, so no sign change.", [f"$\\frac{{{co[4]}}}{{{a}}} = {ft(v)}$."], "adding a minus sign (that's for odd degree).")


@reg(S, "basics")
def pv_double(r):
    b = r.randint(1, 12) * 2 * r.choice([1, -1])
    v = b * b // 4
    p = f"For what value of $c$ does $x^2{sg(b)}x + c = 0$ have exactly one (repeated) root?"
    return Q(p, v, [b * b, b // 2, -v, v + 1, b * b // 2], "Discriminant equals zero.",
             "$c$.", "$b^2 - 4c = 0$.", [f"${b * b} - 4c = 0$, $c = {v}$."], "forgetting the 4.")


@reg(S, "basics")
def pv_squares_poly(r):
    s1, p1 = r.randint(-8, 8), r.randint(-9, 9)
    if p1 == 0:
        return None
    v = -(s1 * s1 - 2 * p1)
    p = f"If $r$ and $s$ are the roots of ${ptex([1, -s1, p1])} = 0$, the monic quadratic with roots $r^2$ and $s^2$ is $x^2 + bx + c$. What is $b$?"
    return Q(p, v, [-v, s1 * s1, -(s1 * s1 + 2 * p1), p1 * p1, v + 1], "$b = -(r^2 + s^2)$.",
             "$b$.", "$r^2 + s^2 = (r + s)^2 - 2rs$.", [f"$r^2 + s^2 = {s1 * s1} - {par(2 * p1)} = {s1 * s1 - 2 * p1}$.", f"$b = {v}$."], "forgetting the minus sign in $b$.")


@reg(S, "basics")
def pv_eval_one(r):
    roots = [r.randint(-5, 6) for _ in range(3)]
    c = poly_from_roots(roots)
    v = (1 - roots[0]) * (1 - roots[1]) * (1 - roots[2])
    p = f"Let $r$, $s$, $t$ be the roots of ${ptex(c)} = 0$. What is $(1 - r)(1 - s)(1 - t)$?"
    return Q(p, v, [-v if v else 1, int(sum(c)) + 1, v + 2, int(c[3]), int(sum(c)) - 1 if int(sum(c)) - 1 != v else v + 1], "Plug in $x = 1$.",
             "the product.", "for monic $P(x) = (x - r)(x - s)(x - t)$, $P(1) = (1 - r)(1 - s)(1 - t)$.", [f"$P(1) = {' + '.join(ft(a) for a in c).replace('+ -', '- ')} = {v}$."], "using $P(-1)$.")


@reg(S, "basics")
def pv_factored_sum(r):
    a = r.randint(-8, 8)
    b, c = r.randint(-9, 9), r.randint(1, 15)
    v = a - b
    p = f"What is the sum of all roots (real and complex) of $(x{sg(-a)})({ptex([1, b, c])}) = 0$?".replace("(x + 0)", "x").replace("(x - 0)", "x")
    return Q(p, v, [a + b, a, -b, v + 1, a - c], "Add the roots of each factor.",
             "the sum.", "the linear factor gives one root; the quadratic gives two whose sum is $-b$.", [f"${a} + {par(-b)} = {v}$."], "including only real roots.")


@reg(S, "basics")
def pv_other_root(r):
    rt, other = r.randint(-9, 9), r.randint(-9, 9)
    if rt == 0 or other == 0:
        return None
    b, c = -(rt + other), rt * other
    p = f"One root of ${ptex([1, b, c])} = 0$ is ${rt}$. What is the other root?"
    return Q(p, other, [-other, rt, c, -b, other + 1], "Use the product (or sum) of the roots.",
             "the other root.", "sum of roots $= -b$.", [f"Other root: ${-b} - {par(rt)} = {other}$."], "taking the negative.") if rt != other else None


@reg(S, "basics")
def pv_q_cubes(r):
    s1, p1 = r.randint(-6, 6), r.randint(-8, 8)
    if s1 == 0 or p1 == 0:
        return None
    v = s1 ** 3 - 3 * p1 * s1
    p = f"If $r$ and $s$ are the roots of ${ptex([1, -s1, p1])} = 0$, what is $r^3 + s^3$?"
    return Q(p, v, [s1 ** 3, s1 ** 3 + 3 * p1 * s1, v + 1, s1 ** 3 - p1 * s1 if s1 ** 3 - p1 * s1 != v else v - 1, -v if v else 2], "$r^3 + s^3 = (r + s)^3 - 3rs(r + s)$.",
             "$r^3 + s^3$.", "express in terms of the sum and product.", [f"${par(s1)}^3 - 3 \\cdot {par(p1)} \\cdot {par(s1)} = {v}$."], "forgetting the $-3rs(r + s)$ term.")


@reg(S, "challenge")
def pvc_k_count(r):
    N = r.choice([6, 8, 10, 12, 18, 20, 24, 28, 30, 36])
    ks = set()
    for d in range(-N, N + 1):
        if d and N % d == 0:
            ks.add(d + N // d)
    p = f"For how many integers $k$ does $x^2 - kx + {N} = 0$ have two integer roots?"
    return Q(p, len(ks), [len(ks) // 2, len(ks) + 2, len(ks) - 1, sum(1 for d in range(1, N + 1) if N % d == 0), len(ks) + 1], "Factor " + str(N) + " as a product of two integers.",
             "the number of $k$ values.", f"the roots $p, q$ satisfy $pq = {N}$ and $k = p + q$.", [f"Pairs $(p, q)$ with $pq = {N}$ (including negatives) give the sums $k$: " + ", ".join(map(str, sorted(ks))) + ".", f"Distinct $k$: ${len(ks)}$."], "forgetting negative factor pairs.")


@reg(S, "challenge")
def pvc_recip_sq(r):
    roots = [r.choice([x for x in range(-5, 6) if x]) for _ in range(3)]
    c = poly_from_roots(roots)
    v = sum(F(1, x * x) for x in roots)
    p = f"Let $r$, $s$, $t$ be the roots of ${ptex(c)} = 0$. What is $\\frac{{1}}{{r^2}} + \\frac{{1}}{{s^2}} + \\frac{{1}}{{t^2}}$?"
    e1, e2, e3 = -c[1], c[2], -c[3]
    return Q(p, v, [sum(F(1, x) for x in roots) ** 2, v + 1, F(e2 * e2, e3 * e3), F(e2 * e2 + 2 * e1 * e3, e3 * e3) if F(e2 * e2 + 2 * e1 * e3, e3 * e3) != v else v * 2, F(e1 * e1 - 2 * e2, e3 * e3)], "Square $\\frac{1}{r} + \\frac{1}{s} + \\frac{1}{t}$.",
             "the sum.", "$\\sum \\frac{1}{r^2} = \\left(\\sum \\frac{1}{r}\\right)^2 - 2\\sum \\frac{1}{rs} = \\frac{(rs + st + tr)^2 - 2rst(r + s + t)}{(rst)^2}$.",
             [f"$r + s + t = {ft(e1)}$, $rs + st + tr = {ft(e2)}$, $rst = {ft(e3)}$.", f"$\\frac{{{ft(e2)}^2 - 2 \\cdot {par(int(e3))} \\cdot {par(int(e1))}}}{{{ft(e3 * e3)}}} = {ft(v)}$."], "forgetting the cross terms.")


@reg(S, "challenge")
def pvc_pair_product(r):
    roots = [r.randint(-6, 6) for _ in range(3)]
    c = poly_from_roots(roots)
    e1, e2, e3 = -c[1], c[2], -c[3]
    v = e1 * e2 - e3
    p = f"Let $r$, $s$, $t$ be the roots of ${ptex(c)} = 0$. What is $(r + s)(s + t)(t + r)$?"
    return Q(p, v, [e1 * e2, e1 * e2 + e3, -v if v else 1, e1 ** 3 - e3, v + 2], "$r + s = e_1 - t$.",
             "the product.", "$(r + s)(s + t)(t + r) = (r + s + t)(rs + st + tr) - rst$.", [f"$e_1 = {ft(e1)}$, $e_2 = {ft(e2)}$, $e_3 = {ft(e3)}$.", f"${ft(e1)} \\cdot {par(int(e2))} - {par(int(e3))} = {ft(v)}$."], "forgetting to subtract $rst$.")


@reg(S, "challenge")
def pvc_gp_roots(r):
    g = r.randint(1, 4) * r.choice([1, -1])
    q = r.choice([2, 3, F(1, 2)])
    roots = [g / F(q), F(g), g * F(q)]
    c = poly_from_roots(roots)
    if any(x.denominator != 1 for x in c):
        return None
    p = f"The roots of ${ptex(c)} = 0$ form a geometric sequence. What is the middle root (the geometric mean of the other two)?"
    return Q(p, g, [-g, roots[2] if roots[2] != g else g + 1, g * g, -c[1], g * 2], "In a geometric sequence $\\frac{g}{q}, g, gq$, the product of the roots is $g^3$.",
             "the middle root.", f"product of roots $= {ft(-c[3])} = g^3$.", [f"$g = \\sqrt[3]{{{ft(-c[3])}}} = {g}$."], "using the sum of the roots.")


@reg(S, "challenge")
def pvc_fourth(r):
    s1, p1 = r.randint(-5, 5), r.randint(-6, 6)
    if p1 == 0 or s1 == 0:
        return None
    q2 = s1 * s1 - 2 * p1
    v = q2 * q2 - 2 * p1 * p1
    p = f"If $r$ and $s$ are the roots of ${ptex([1, -s1, p1])} = 0$, what is $r^4 + s^4$?"
    return Q(p, v, [q2 * q2, s1 ** 4 - 2 * p1, v + 2 * p1 * p1 - 2, q2 * q2 + 2 * p1 * p1, v - 1], "Square $r^2 + s^2$.",
             "$r^4 + s^4$.", "$r^4 + s^4 = (r^2 + s^2)^2 - 2(rs)^2$.", [f"$r^2 + s^2 = {s1 * s1} - {par(2 * p1)} = {q2}$.", f"${par(q2)}^2 - 2 \\cdot {p1 * p1} = {v}$."], "forgetting $-2(rs)^2$.")


@reg(S, "challenge")
def pvc_shared(r):
    a = r.randint(-6, 6)
    b, c = r.sample([x for x in range(-7, 8) if x != a], 2)
    p1, p2 = poly_from_roots([a, b]), poly_from_roots([a, c])
    p = f"The equations ${ptex(p1)} = 0$ and ${ptex(p2)} = 0$ share exactly one root. What is it?"
    return Q(p, a, [b, c, -a if a else 1, a + 1, b + c - a if b + c - a not in (a, b, c) else a - 1], "Subtract the equations.",
             "the shared root.", "a common root satisfies both, so it satisfies their difference (a linear equation).",
             [f"Difference: $({ft(p1[1] - p2[1])})x + ({ft(p1[2] - p2[2])}) = 0$.", f"$x = {a}$."], "solving just one equation.")


@reg(S, "challenge")
def pvc_shift_poly(r):
    roots = [r.randint(-5, 5) for _ in range(3)]
    c = poly_from_roots(roots)
    v = -math.prod(x + 1 for x in roots)
    p = f"Let $r$, $s$, $t$ be the roots of ${ptex(c)} = 0$. The monic cubic $Q(x)$ has roots $r + 1$, $s + 1$, $t + 1$. What is $Q(0)$?"
    return Q(p, v, [-v if v else 2, int(peval(c, 1)), int(peval(c, -1)) if int(peval(c, -1)) != v else v + 1, math.prod(roots), v + 3], "$Q(x) = P(x - 1)$.",
             "$Q(0)$.", "shifting every root by 1 replaces $x$ with $x - 1$.", [f"$Q(0) = P(-1) = {v}$."], "using $P(1)$.")


# ================================================================ poly_remainder
S = "poly_remainder"


def rpoly(r, deg=3, lo=-6, hi=6):
    c = [r.randint(1, 4)] + [r.randint(lo, hi) for _ in range(deg)]
    return c


@reg(S, "basics")
def prm_neg(r):
    c = rpoly(r)
    a = r.randint(1, 4)
    v = peval(c, -a)
    p = f"What is the remainder when ${ptex(c)}$ is divided by $x + {a}$?"
    return Q(p, v, [peval(c, a), -v if v else 1, v + 1, c[-1], sum(c)], "Remainder Theorem.",
             "the remainder.", f"dividing by $x + {a}$ leaves remainder $P(-{a})$.", [f"$P(-{a}) = {ft(v)}$."], f"using $P({a})$.")


@reg(S, "basics")
def prm_const(r):
    a, n, b = r.randint(1, 4), r.randint(2, 5), r.randint(1, 5)
    v = a ** n * (-b)
    p = f"What is the constant term of $(x + {a})^{{{n}}}(x - {b})$?"
    return Q(p, v, [-v, a ** n, a * n * -b, a ** n + b, v + 1], "Set $x = 0$.",
             "the constant term.", "the constant term is the value at $x = 0$.", [f"${a}^{{{n}}} \\cdot (-{b}) = {v}$."], "dropping the sign.")


@reg(S, "basics")
def prm_alt(r):
    c = rpoly(r, r.randint(3, 5))
    v = peval(c, -1)
    p = f"What is $P(-1)$, the alternating sum of the coefficients, for $P(x) = {ptex(c)}$?"
    p = f"For $P(x) = {ptex(c)}$, what is $P(-1)$?"
    return Q(p, v, [sum(c), -v if v else 2, v + 2, c[-1], v - 1], "Substitute $x = -1$.",
             "$P(-1)$.", "odd powers flip sign; even powers don't.", [f"$P(-1) = {ft(v)}$."], "computing $P(1)$.")


@reg(S, "basics")
def prm_even_sum(r):
    a, b, n = r.randint(1, 3), r.randint(1, 3), r.randint(3, 6)
    P1, Pm1 = (a + b) ** n, (b - a) ** n
    kind = r.choice(["even", "odd"])
    v = F(P1 + Pm1, 2) if kind == "even" else F(P1 - Pm1, 2)
    p = f"When $({a if a > 1 else ''}x + {b})^{{{n}}}$ is expanded, what is the sum of the coefficients of the {'even' if kind == 'even' else 'odd'} powers of $x$ (counting the constant as $x^0$)?"
    return Q(p, v, [F(P1, 2), F(P1 + Pm1, 2) if kind == "odd" else F(P1 - Pm1, 2), F(P1), v + 1, F(Pm1)], "Use $P(1)$ and $P(-1)$.",
             "the sum.", "$\\frac{P(1) + P(-1)}{2}$ gives even powers; $\\frac{P(1) - P(-1)}{2}$ gives odd powers.", [f"$P(1) = {P1}$, $P(-1) = {Pm1}$.", f"Answer: ${ft(v)}$."], "assuming half the total.") if P1 != Pm1 and (P1 + Pm1) != 0 else None


@reg(S, "basics")
def prm_two_factors(r):
    r1, r2, r3 = r.sample(range(-5, 6), 3)
    c = poly_from_roots([r1, r2, r3])
    v = int(c[1] + c[2])
    p = f"The polynomial $x^3 + ax^2 + bx{sg(int(c[3]))}$ has factors $(x{sg(-r1)})$ and $(x{sg(-r2)})$. What is $a + b$?".replace("(x + 0)", "x").replace("(x - 0)", "x")
    return Q(p, v, [-v if v else 1, int(c[1]), int(c[2]), v + 1, int(c[1] - c[2])], "Find the third root from the constant term.",
             "$a + b$.", f"the roots are ${r1}$, ${r2}$, and a third root $t$ with $-{r1} \\cdot {r2} \\cdot t = {ft(c[3])}$.".replace("--", ""), [f"Third root: ${r3}$.", f"Expanding gives $a = {ft(c[1])}$, $b = {ft(c[2])}$; $a + b = {v}$."], "solving for $a$ and $b$ with a sign error.") if c[3] != 0 and r1 * r2 != 0 else None


@reg(S, "basics")
def prm_quotient(r):
    c = rpoly(r)
    a = r.randint(-3, 3)
    if a == 0:
        return None
    q = [c[0]]
    for coef in c[1:-1]:
        q.append(coef + q[-1] * a)
    v = sum(q)
    p = f"When ${ptex(c)}$ is divided by $x{sg(-a)}$, what is the sum of the coefficients of the quotient?"
    return Q(p, v, [sum(c), peval(c, a), v + 1, q[-1], -v if v else 2], "Synthetic division.",
             "the sum of the quotient's coefficients.", "the quotient's coefficients come from the synthetic division row.",
             [f"Synthetic division by ${a}$: quotient coefficients " + ", ".join(ft(x) for x in q) + ".", f"Sum: ${ft(v)}$."], "including the remainder.")


@reg(S, "basics")
def prm_linear_div(r):
    c = rpoly(r)
    a, b = r.choice([(2, 1), (3, 1), (2, 3), (3, 2), (2, -1)])
    v = peval(c, F(b, a))
    p = f"What is the remainder when ${ptex(c)}$ is divided by ${a}x{sg(-b)}$?"
    return Q(p, v, [peval(c, F(a, b)) if peval(c, F(a, b)) != v else v + 1, peval(c, b), peval(c, -F(b, a)), v * a, v + 2], "Find where the divisor is zero.",
             "the remainder.", f"${a}x{sg(-b)} = 0$ at $x = {ft(F(b, a))}$.", [f"$P\\left({ft(F(b, a))}\\right) = {ft(v)}$."], f"using $x = {b}$.")


@reg(S, "basics")
def prm_factored_plus(r):
    n = r.randint(2, 4)
    roots = r.sample(range(1, 7), n)
    cst = r.randint(-9, 9)
    x = r.randint(-2, 8)
    v = math.prod(x - k for k in roots) + cst
    form = "".join(f"(x - {k})" for k in roots) + f"{sg(cst)}"
    p = f"If $P(x) = {form}$, what is $P({x})$?"
    return Q(p, v, [cst, math.prod(x - k for k in roots), v + 1, -v if v else 2, math.prod(x + k for k in roots) + cst], "Just substitute.",
             f"$P({x})$.", "multiply the factors at the given $x$.", [f"Factors: " + " \\cdot ".join(f"{par(x - k)}" for k in roots).join(["$", "$"]) + f" $= {math.prod(x - k for k in roots)}$.", f"Plus ${cst}$: ${v}$."], "forgetting the constant.")


@reg(S, "basics")
def prm_degree(r):
    m, n = r.randint(2, 6), r.randint(2, 6)
    kind = r.choice(["comp", "prod", "power"])
    v = {"comp": m * n, "prod": m + n, "power": m * n}[kind]
    q = {"comp": f"$P(Q(x))$", "prod": f"$P(x) \\cdot Q(x)$", "power": f"$(P(x))^{{{n}}}$"}[kind]
    p = f"$P$ has degree ${m}$" + (f" and $Q$ has degree ${n}$" if kind != "power" else "") + f". What is the degree of {q}?"
    return Q(p, v, [m + n if v != m + n else m * n, m * n + 1 if v == m * n else m + n + 1, max(m, n), m ** n if m ** n < 1000 else v + 2, v - 1], "Track the leading term.",
             "the degree.", {"comp": "substituting a degree-$n$ polynomial into a degree-$m$ one multiplies degrees.", "prod": "multiplying adds degrees.", "power": "raising to a power multiplies the degree."}[kind], [f"Degree: ${v}$."], "adding instead of multiplying (or vice versa).")


@reg(S, "basics")
def prm_leading(r):
    a, b, m, n = r.randint(2, 4), r.randint(2, 4), r.randint(2, 4), r.randint(1, 3)
    v = a ** m * (-b) ** n if r.random() < .5 else a ** m * b ** n
    sgnb = -1 if v < 0 else 1
    p = f"What is the leading coefficient of $({a}x + 1)^{{{m}}}({'-' if sgnb < 0 and n % 2 else ''}{b}x - 5)^{{{n}}}$?"
    v = a ** m * ((-b) if sgnb < 0 and n % 2 else b) ** n
    return Q(p, v, [a * b, a ** m + b ** n, -v, a * m * b * n if a * m * b * n != v else v + 1, a ** m], "Multiply the leading terms.",
             "the leading coefficient.", "the leading term of a product is the product of leading terms.", [f"${a}^{{{m}}} \\cdot {par((-b) if sgnb < 0 and n % 2 else b)}^{{{n}}} = {v}$."], "multiplying exponents and bases incorrectly.")


@reg(S, "basics")
def prm_find_k(r):
    a, b, x0 = r.randint(-6, 6), r.randint(-9, 9), r.randint(1, 3)
    k = r.choice([x for x in range(-5, 6) if x])
    rem = k * x0 ** 3 + a * x0 + b
    p = f"When $kx^3{sg(a)}x{sg(b)}$ is divided by $x - {x0}$, the remainder is ${rem}$. What is $k$?".replace("+ 0x ", "").replace("- 0x ", "")
    return Q(p, k, [-k, k + 1, F(rem - b, x0 ** 3), F(rem, x0 ** 3) if F(rem, x0 ** 3) != k else k + 2, rem - a - b], "Remainder Theorem: $P(" + str(x0) + ") = " + str(rem) + "$.",
             "$k$.", "substitute and solve.", [f"${x0 ** 3}k{sg(a * x0)}{sg(b)} = {rem}$.", f"$k = {k}$."], "forgetting to cube " + str(x0) + ".") if a else None


@reg(S, "basics")
def prm_coeff(r):
    n = r.randint(3, 8)
    k = r.randint(1, n - 1)
    a = r.choice([1, 2, 3, -1, -2])
    v = comb(n, k) * a ** (n - k)
    p = f"What is the coefficient of $x^{{{k}}}$ in the expansion of $(x{sg(a)})^{{{n}}}$?"
    return Q(p, v, [comb(n, k), comb(n, k) * a ** k if comb(n, k) * a ** k != v else v + 1, -v, comb(n, k - 1) * a ** (n - k + 1), v * 2], "Binomial Theorem.",
             "the coefficient.", f"the $x^{{{k}}}$ term is $\\binom{{{n}}}{{{k}}} x^{{{k}}} \\cdot ({a})^{{{n - k}}}$.", [f"$\\binom{{{n}}}{{{k}}} = {comb(n, k)}$; $({a})^{{{n - k}}} = {a ** (n - k)}$.", f"Coefficient: ${v}$."], "raising the constant to the wrong power.")


@reg(S, "basics")
def prm_two_point(r):
    n = r.randint(3, 8)
    R0 = 2 - 2 ** n
    R1 = 2 ** n - 1
    x0 = r.choice([0, 3, -1])
    v = R1 * x0 + R0
    p = f"Let $R(x)$ be the remainder when $x^{{{n}}}$ is divided by $(x - 1)(x - 2)$. What is $R({x0})$?"
    return Q(p, v, [R1, 2 ** n, v + 1, -v if v else 1, R1 * x0 - R0], "$R(x) = ax + b$ with $R(1) = 1$ and $R(2) = 2^" + str(n) + "$.",
             "$R(" + str(x0) + ")$.", "the remainder agrees with $x^n$ at the roots of the divisor.", [f"$a + b = 1$ and $2a + b = {2 ** n}$, so $a = {R1}$, $b = {R0}$.", f"$R({x0}) = {v}$."], "dividing directly.")


@reg(S, "basics")
def prm_substitute(r):
    a, b = r.randint(-6, 6), r.randint(-6, 6)
    x0 = r.randint(-3, 5)
    v = (x0 - 1) ** 2 + a * (x0 - 1) + b
    p = f"If $P(x + 1) = {ptex([1, a, b])}$, what is $P({x0})$?"
    return Q(p, v, [x0 * x0 + a * x0 + b, (x0 + 1) ** 2 + a * (x0 + 1) + b, v + 1, -v if v else 3, x0 + a + b], "What $x$ makes $x + 1 = " + str(x0) + "$?",
             "$P(" + str(x0) + ")$.", f"set $x = {x0 - 1}$.", [f"$P({x0}) = {par(x0 - 1)}^2{sg(a)} \\cdot {par(x0 - 1)}{sg(b)} = {v}$.".replace("+ 0 \\cdot", "+ 0 \\cdot")], "plugging in " + str(x0) + " directly.")


@reg(S, "basics")
def prm_rational_count(r):
    a, c = r.choice([1, 2, 3, 4, 6]), r.choice([1, 2, 3, 4, 6, 8, 9, 10, 12])
    ps = [d for d in range(1, c + 1) if c % d == 0]
    qs = [d for d in range(1, a + 1) if a % d == 0]
    cands = {F(s * p_, q_) for p_ in ps for q_ in qs for s in (1, -1)}
    v = len(cands)
    p = f"By the Rational Root Theorem, how many distinct possible rational roots does ${a if a > 1 else ''}x^3 + bx^2 + cx + {c} = 0$ have (for integers $b$, $c$)?".replace("+ cx + ", "+ dx + ").replace("for integers $b$, $c$", "for integers $b$, $d$")
    return Q(p, v, [v // 2, len(ps) * len(qs) * 2, v + 2, len(ps) * 2, v - 2 if v > 2 else 5], "Candidates are $\\pm\\frac{p}{q}$ with $p \\mid " + str(c) + "$, $q \\mid " + str(a) + "$.",
             "the number of candidates.", "list them and remove duplicates.", [f"Divisors of ${c}$: " + ", ".join(map(str, ps)) + f"; divisors of ${a}$: " + ", ".join(map(str, qs)) + ".", f"Distinct $\\pm\\frac{{p}}{{q}}$: ${v}$."], "counting duplicates like $\\frac{2}{2} = 1$ twice.") if not (len(ps) * len(qs) * 2 == v and v // 2 == v) else None


@reg(S, "basics")
def prm_nonconst(r):
    a, n = r.randint(1, 4), r.randint(3, 7)
    v = (1 + a) ** n - a ** n
    p = f"When $(x + {a})^{{{n}}}$ is expanded, what is the sum of all the coefficients except the constant term?"
    return Q(p, v, [(1 + a) ** n, a ** n, v + 1, 2 ** n - 1, (1 + a) ** n - 1], "Sum of all coefficients minus the constant.",
             "the sum.", "all coefficients sum to $P(1)$; the constant is $P(0)$.", [f"$P(1) = {(1 + a) ** n}$, $P(0) = {a ** n}$.", f"Difference: ${v}$."], "subtracting 1 instead of the constant.")


@reg(S, "challenge")
def prmc_cube_div(r):
    n = r.randint(10, 100)
    x0 = r.choice([2, 3, -1, -2])
    e = n % 3
    v = x0 ** e
    p = f"Let $R(x)$ be the remainder when $x^{{{n}}}$ is divided by $x^3 - 1$. What is $R({x0})$?"
    return Q(p, v, [x0 ** n if abs(x0 ** n) < 10 ** 4 else v + 1, 1 if v != 1 else x0, x0 ** ((n + 1) % 3) if x0 ** ((n + 1) % 3) != v else v + 2, x0 ** 2 if e != 2 else x0, 0], "$x^3 \\equiv 1$.",
             "$R(" + str(x0) + ")$.", "reduce the exponent mod 3.", [f"${n} = 3 \\cdot {n // 3} + {e}$, so $x^{{{n}}} \\equiv x^{{{e}}}$.", f"$R(x) = x^{{{e}}}$, $R({x0}) = {v}$."], "plugging into $x^" + str(n) + "$.")


@reg(S, "challenge")
def prmc_interp(r):
    n = r.randint(2, 4)
    m = r.randint(n + 1, n + 4)
    v = math.prod(m - k for k in range(1, n + 1)) + m
    p = f"A monic polynomial $P(x)$ of degree ${n}$ satisfies $P(k) = k$ for $k = {', '.join(map(str, range(1, n + 1)))}$. What is $P({m})$?"
    return Q(p, v, [m, v - m, v + 1, math.factorial(n) + m, math.prod(m - k for k in range(1, n + 1))], "Consider $P(x) - x$.",
             f"$P({m})$.", f"$P(x) - x$ is monic of degree ${n}$ with roots $1, \\ldots, {n}$.", [f"$P(x) = " + "".join(f"(x - {k})" for k in range(1, n + 1)) + " + x$.", f"$P({m}) = {math.prod(m - k for k in range(1, n + 1))} + {m} = {v}$."], "answering " + str(m) + ".")


@reg(S, "challenge")
def prmc_omega(r):
    n = r.randint(10, 60)
    x0 = r.choice([1, 2, 3, -2])
    e = n % 3
    rem = {0: (0, 1), 1: (1, 0), 2: (-1, -1)}[e]
    v = rem[0] * x0 + rem[1]
    p = f"Let $R(x)$ be the remainder when $x^{{{n}}}$ is divided by $x^2 + x + 1$. What is $R({x0})$?"
    return Q(p, v, [x0 ** e if x0 ** e != v else v + 1, 1 if v != 1 else 0, -v if v else 2, v + 2, x0], "$x^3 - 1 = (x - 1)(x^2 + x + 1)$, so $x^3 \\equiv 1$.",
             "$R(" + str(x0) + ")$.", "reduce the exponent mod 3; then $x^2 \\equiv -x - 1$.", [f"$x^{{{n}}} \\equiv x^{{{e}}}$" + (", and $x^2 \\equiv -x - 1$." if e == 2 else "."), f"$R(x) = {ptex([rem[0], rem[1]]) if rem[0] else str(rem[1])}$, so $R({x0}) = {v}$."], "stopping at $x^" + str(e) + "$.")


@reg(S, "challenge")
def prmc_comp_sum(r):
    a, b, c = r.randint(1, 3), r.randint(-4, 4), r.randint(-4, 4)
    P1 = a + b + c
    v = a * P1 * P1 + b * P1 + c
    p = f"Let $P(x) = {ptex([a, b, c])}$. What is the sum of the coefficients of $P(P(x))$?"
    return Q(p, v, [P1, P1 * P1, v + 1, a * a + b * b + c * c, -v if v else 2], "Sum of coefficients $=$ value at 1.",
             "the sum.", "the sum of coefficients of $P(P(x))$ is $P(P(1))$.", [f"$P(1) = {P1}$.", f"$P({P1}) = {v}$."], "squaring $P(1)$.")


@reg(S, "challenge")
def prmc_double_factor(r):
    n = r.randint(3, 12)
    ask = r.choice(["a", "b"])
    v = -n if ask == "a" else n - 1
    p = f"The polynomial $x^{{{n}}} + ax + b$ is divisible by $(x - 1)^2$. What is ${ask}$?"
    return Q(p, v, [-v, n, -(n - 1) if ask == "b" else n - 1, v + 1, 1], "Both $P(1)$ and $P'(1)$ vanish.",
             f"${ask}$.", "a double root at 1 means $P(1) = 0$ and $P'(1) = 0$.", [f"$P'(1) = {n} + a = 0$, so $a = -{n}$.", f"$P(1) = 1 + a + b = 0$, so $b = {n - 1}$."], "only using $P(1) = 0$.")


@reg(S, "challenge")
def prmc_i_rem(r):
    n = r.randint(3, 15)
    z = (1, 0)
    for _ in range(n):
        z = (z[0] - z[1], z[0] + z[1])
    v = z[0] + z[1]
    p = f"Let $R(x)$ be the remainder when $(x + 1)^{{{n}}}$ is divided by $x^2 + 1$. What is $R(1)$?"
    return Q(p, v, [2 ** n, z[0] if z[0] != v else v + 1, z[1] if z[1] != v else v - 1, -v if v else 2, 2 ** (n // 2)], "Evaluate at $x = i$.",
             "$R(1)$.", f"$R(x) = Bx + A$ where $(1 + i)^{{{n}}} = A + Bi$.", [f"$(1 + i)^{{{n}}} = {z[0]}{sg(z[1])}i$.", f"$R(x) = {z[1]}x{sg(z[0])}$, $R(1) = {v}$."], "computing $2^" + str(n) + "$.")


@reg(S, "challenge")
def prmc_differences(r):
    a, b, c = r.randint(-5, 9), r.randint(-5, 9), r.randint(-5, 9)
    d1, d2 = b - a, c - b
    v = c + d2 + (d2 - d1)
    p = f"A polynomial $P$ of degree at most $2$ has $P(0) = {a}$, $P(1) = {b}$, and $P(2) = {c}$. What is $P(3)$?"
    return Q(p, v, [c + d2, 2 * c - b + 1 if 2 * c - b + 1 != v else v + 1, a + b + c, v - 1, 3 * c - 3 * b + a + 2], "Finite differences.",
             "$P(3)$.", "for a quadratic, second differences are constant.", [f"First differences: ${d1}$, ${d2}$; second difference: ${d2 - d1}$.", f"Next first difference: ${d2 + d2 - d1}$, so $P(3) = {c}{sg(2 * d2 - d1)} = {v}$."], "assuming the first difference is constant.")


# ================================================================ poly_roots
S = "poly_roots"


@reg(S, "basics")
def rts_quad(r):
    a, b = r.sample(range(-9, 10), 2)
    ask = r.choice(["larger", "smaller"])
    v = max(a, b) if ask == "larger" else min(a, b)
    p = f"What is the {ask} root of ${ptex([1, -(a + b), a * b])} = 0$?"
    return Q(p, v, [-v if v else 1, min(a, b) if ask == "larger" else max(a, b), a + b if a + b not in (a, b) else v + 1, a * b if a * b not in (a, b) else v - 1, v + 2], "Factor.",
             "the root.", "find two numbers with the right sum and product.", [f"$(x{sg(-a)})(x{sg(-b)}) = 0$, roots ${a}$ and ${b}$.".replace("(x + 0)", "x").replace("(x - 0)", "x")], "flipping the signs of the roots.")


@reg(S, "basics")
def rts_grouping(r):
    a, b = r.randint(1, 7), r.randint(1, 7)
    if a == b:
        return None
    c = poly_from_roots([-a, b, -b])
    v = max(b, -a)
    p = f"What is the largest root of ${ptex(c)} = 0$?"
    return Q(p, v, [a, -b, b * b, a * b, v + 1], "Factor by grouping.",
             "the largest root.", f"group as $x^2(x + {a}) - {b * b}(x + {a})$.", [f"$(x + {a})(x^2 - {b * b}) = 0$: roots $-{a}$, $\\pm {b}$.", f"Largest: ${v}$."], "picking " + str(a) + ".")


@reg(S, "basics")
def rts_real_prod(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    p = f"What is the product of the real roots of $(x^2 - {a * a})(x^2 + {b * b}) = 0$?"
    return Q(p, -a * a, [a * a, -a * a * b * b, a * a * b * b, 0, b * b], "Only one factor has real roots.",
             "the product of real roots.", f"$x^2 + {b * b} > 0$ always.", [f"Real roots: $\\pm {a}$; product $-{a * a}$."], "including the complex roots.")


@reg(S, "basics")
def rts_rational(r):
    p1, q1, p2, q2 = r.randint(1, 5), r.randint(2, 5), r.randint(-5, 5), r.randint(1, 5)
    r1, r2 = F(p1, q1), F(p2, q2)
    if r1 == r2 or r1.denominator == 1:
        return None
    lead = r1.denominator * r2.denominator
    c = [lead, -lead * (r1 + r2), lead * r1 * r2]
    if any(x.denominator != 1 for x in c):
        return None
    ask = r.choice(["larger", "smaller"])
    v = max(r1, r2) if ask == "larger" else min(r1, r2)
    p = f"What is the {ask} root of ${ptex(c)} = 0$?"
    return Q(p, v, [-v, min(r1, r2) if ask == "larger" else max(r1, r2), 1 / v if v else F(1, 2), v + 1, F(-c[1], c[0]) if F(-c[1], c[0]) not in (r1, r2) else v * 2], "Factor or use the quadratic formula.",
             "the root.", "factor into two linear terms.", [f"Roots: ${ft(r1)}$ and ${ft(r2)}$."], "flipping the fraction.")


@reg(S, "basics")
def rts_conj(r):
    a, b = r.randint(-6, 6), r.randint(1, 6)
    v = a * a + b * b
    p = f"A polynomial with real coefficients has ${ptex([a]) if a else ''}{' + ' if a else ''}{b if b > 1 else ''}i$ as a root. What is the product of this root and its conjugate?".replace("$ + ", "$")
    return Q(p, v, [a * a - b * b, 2 * a if 2 * a != v else v + 1, v + 1, b * b, a * a], "Complex roots come in conjugate pairs.",
             "the product.", "$(a + bi)(a - bi) = a^2 + b^2$.", [f"${a * a} + {b * b} = {v}$."], "computing $a^2 - b^2$.")


@reg(S, "basics")
def rts_multiplicity(r):
    roots = r.sample(range(-6, 7), 3)
    ms = [r.randint(1, 4) for _ in range(3)]
    ask = r.choice(["distinct", "sum"])
    v = 3 if ask == "distinct" else sum(a * m for a, m in zip(roots, ms))
    form = "".join(f"(x{sg(-a)})" + (f"^{{{m}}}" if m > 1 else "") for a, m in zip(roots, ms)).replace("(x + 0)", "x").replace("(x - 0)", "x")
    p = f"For ${form} = 0$, what is " + ("the number of distinct roots?" if ask == "distinct" else "the sum of the roots counted with multiplicity?")
    wr = [sum(ms), 2, 4, 6, 1] if ask == "distinct" else [sum(roots), -v if v else 1, v + 1, sum(-a * m for a, m in zip(roots, ms)) if v else 2, sum(ms)]
    return Q(p, v, wr, "Read the roots from the factors.",
             "the answer.", "each factor $(x - a)^m$ gives root $a$ with multiplicity $m$.", [f"Roots: " + ", ".join(f"${a}$ (×{m})" for a, m in zip(roots, ms)) + ".", f"Answer: ${v}$."], "ignoring multiplicities." if ask == "sum" else "counting with multiplicity.")


@reg(S, "basics")
def rts_x4(r):
    a = r.randint(1, 6)
    ask = r.choice(["count", "sumsq"])
    v = 2 if ask == "count" else 2 * a * a
    p = f"For $x^4 = {a ** 4}$, what is " + ("the number of real solutions?" if ask == "count" else "the sum of the squares of the real solutions?")
    return Q(p, v, [4, 1, 0, 3, 8] if ask == "count" else [0, a * a, 4 * a * a, a ** 4, -2 * a * a], "Factor as a difference of squares.",
             "the answer.", f"$x^4 - {a ** 4} = (x^2 - {a * a})(x^2 + {a * a})$.", [f"Real solutions: $\\pm {a}$.", f"Answer: ${v}$."], "counting complex solutions.")


@reg(S, "basics")
def rts_cubic_mid(r):
    roots = sorted(r.sample(range(-6, 8), 3))
    c = poly_from_roots(roots)
    p = f"The equation ${ptex(c)} = 0$ has three integer roots. What is the middle one?"
    return Q(p, roots[1], [roots[0], roots[2], -roots[1] if roots[1] else 4, -c[1] // 3 if -c[1] // 3 not in roots else roots[1] + 1, sum(roots)], "Test divisors of the constant term.",
             "the middle root.", "find one root by the Rational Root Theorem, then factor the quadratic.", [f"Roots: " + ", ".join(f"${x}$" for x in roots) + ".", f"Middle: ${roots[1]}$."], "taking the sign of a root wrong.") if sum(roots) not in roots else None


@reg(S, "basics")
def rts_biquad(r):
    a, b = r.sample(range(1, 8), 2)
    p = f"What is the sum of the positive roots of $x^4 - {a * a + b * b}x^2 + {a * a * b * b} = 0$?"
    return Q(p, a + b, [0, a * a + b * b, a * b, 2 * (a + b), abs(a - b)], "Substitute $u = x^2$.",
             "the sum.", f"$u^2 - {a * a + b * b}u + {a * a * b * b} = 0$ gives $u = {a * a}$ or ${b * b}$.", [f"$x = \\pm {a}$ or $\\pm {b}$; positive ones sum to ${a + b}$."], "adding all four roots (getting 0).")


@reg(S, "basics")
def rts_shift(r):
    roots = [r.randint(-6, 6) for _ in range(3)]
    k = r.randint(1, 5) * r.choice([1, -1])
    c = poly_from_roots(roots)
    v = sum(roots) + 3 * k
    p = f"The roots of $P(x) = {ptex(c)}$ have sum ${sum(roots)}$. What is the sum of the roots of $P(x{sg(-k)})$?"
    return Q(p, v, [sum(roots) - 3 * k, sum(roots) + k, sum(roots), v + 1, -v if v else 2], "If $P(r) = 0$, what makes $P(x - k)$ zero?",
             "the new sum.", f"$P(x{sg(-k)}) = 0$ when $x{sg(-k)}$ is a root, so each root shifts by ${k}$.", [f"${sum(roots)} + 3 \\cdot {par(k)} = {v}$."], "shifting the sum by only one " + str(k) + ".")


@reg(S, "basics")
def rts_irr_conj(r):
    a, b, n = r.randint(-6, 6), r.randint(1, 4), r.choice([2, 3, 5, 6, 7])
    ask = r.choice(["sum", "product"])
    v = 2 * a if ask == "sum" else a * a - b * b * n
    p = f"A polynomial with rational coefficients has ${a if a else ''}{' + ' if a else ''}{b if b > 1 else ''}\\sqrt{{{n}}}$ as a root. What is the {ask} of this root and its conjugate?".replace("$ + ", "$")
    return Q(p, v, [a * a + b * b * n if ask == "product" else 0 if v else a + 1, -v if v else 3, v + 1, a if a != v else v + 2, b * b * n], "The conjugate flips the sign of the radical.",
             f"the {ask}.", f"the conjugate is ${a if a else ''} - {b if b > 1 else ''}\\sqrt{{{n}}}$.", [f"{ask.capitalize()}: ${v}$."], "using a plus sign in the product.")


@reg(S, "basics")
def rts_monic_coef(r):
    roots = [r.randint(-5, 6) for _ in range(3)]
    c = poly_from_roots(roots)
    v = c[2]
    p = f"The monic cubic with roots ${roots[0]}$, ${roots[1]}$, ${roots[2]}$ is $x^3 + ax^2 + bx + c$. What is $b$?"
    return Q(p, v, [-v if v else 1, c[1], c[3] if c[3] != v else v + 1, sum(roots), v + 2], "Expand or use Vieta.",
             "$b$.", "$b = rs + st + tr$.", [f"${roots[0]} \\cdot {par(roots[1])} + {par(roots[1])} \\cdot {par(roots[2])} + {par(roots[2])} \\cdot {par(roots[0])} = {ft(v)}$."], "using the sum of the roots.")


@reg(S, "basics")
def rts_intersect(r):
    a, b = r.sample(range(-7, 8), 2)
    m, c = a + b, -a * b
    p = f"The line $y = {ptex([m, c])}$ meets the parabola $y = x^2$ at two points. What is the sum of their $x$-coordinates?"
    return Q(p, m, [-m if m else 1, c, a * b, m + 1, abs(a - b)], "Set the equations equal.",
             "the sum.", f"$x^2 - {ptex([m, c])} = 0$; Vieta gives the sum.".replace("- -", "+ "), [f"$x^2{sg(-m)}x{sg(-c)} = 0$, sum of roots $= {m}$."], "flipping the sign.") if m and c else None


@reg(S, "basics")
def rts_disc_count(r):
    b, c = r.randint(-10, 10), r.randint(-10, 15)
    d = b * b - 4 * c
    v = 2 if d > 0 else 1 if d == 0 else 0
    p = f"How many real roots does ${ptex([1, b, c])} = 0$ have?"
    return Q(p, v, [x for x in (0, 1, 2, 3, 4) if x != v], "Discriminant.",
             "the count.", "$b^2 - 4c$ positive, zero, or negative.", [f"${b * b} - {par(4 * c)} = {d}$.", f"So ${v}$ real root{'s' if v != 1 else ''}."], "forgetting the 4.")


@reg(S, "basics")
def rts_abs(r):
    a, b = r.sample(range(1, 8), 2)
    roots = [a, b]
    S_, P_ = a + b, a * b
    sols = {a, -a, b, -b}
    p = f"How many real solutions does $x^2 - {S_}|x| + {P_} = 0$ have?"
    return Q(p, len(sols), [2, 3, 1, 0, 8], "Let $u = |x| \\ge 0$.",
             "the count.", f"$u^2 - {S_}u + {P_} = 0$ gives $u = {a}$ or ${b}$.", [f"Each positive $u$ gives $x = \\pm u$: ${len(sols)}$ solutions."], "forgetting the negative values of $x$.")


@reg(S, "basics")
def rts_rational_eq(r):
    a, b, c = r.randint(-6, 6), r.randint(1, 6), r.choice([2, 3, 4, -1, -2])
    if c == 1:
        return None
    x = F(c * b + a, c - 1)
    if x == b:
        return None
    p = f"Solve $\\dfrac{{x{sg(a)}}}{{x - {b}}} = {c}$.".replace("x + 0", "x").replace("x - 0", "x")
    return Q(p, x, [-x if x else F(1), F(c * b - a, c - 1) if F(c * b - a, c - 1) != x else x + 2, F(c * b + a, 1 - c) if F(c * b + a, 1 - c) != x else x + 3, x + 1, F(b)], "Cross-multiply.",
             "$x$.", f"$x{sg(a)} = {c}(x - {b})$.", [f"$x{sg(a)} = {c}x{sg(-c * b)}$.", f"$x = {ft(x)}$."], "forgetting to distribute.")


@reg(S, "challenge")
def rtsc_cube_nonreal(r):
    a = r.randint(1, 8)
    sgn = r.choice([1, -1])
    v = a * a
    p = f"What is the product of the two nonreal solutions of $x^3 {'-' if sgn > 0 else '+'} {a ** 3} = 0$?"
    return Q(p, v, [-v, a ** 3, a, 2 * a, v + a], "Factor a sum or difference of cubes.",
             "the product.", f"$x^3 {'-' if sgn > 0 else '+'} {a ** 3} = (x {'-' if sgn > 0 else '+'} {a})(x^2 {'+' if sgn > 0 else '-'} {a}x + {a * a})$.", [f"The quadratic factor has the nonreal roots; their product is ${a * a}$."], "including the real root.")


@reg(S, "challenge")
def rtsc_quartic_sub(r):
    k = r.randint(1, 7)
    x1, x3 = r.sample(range(-4, 9), 2)
    x2, x4 = k - x1, k - x3
    xs = {x1, x2, x3, x4}
    u1, u2 = x1 * x1 - k * x1, x3 * x3 - k * x3
    if len(xs) != 4 or u1 == u2:
        return None
    v = 2 * k
    p = f"What is the sum of all real solutions of $(x^2 - {k}x)^2{sg(-(u1 + u2))}(x^2 - {k}x){sg(u1 * u2)} = 0$?".replace("+ 1(", "+ (").replace("- 1(", "- (").replace(" + 0(x^2", "").replace(" - 0(x^2", "").replace("x^2 - 1x", "x^2 - x")
    return Q(p, v, [k, u1 + u2 if u1 + u2 != v else v + 1, v + k, 4 * k if 4 * k != v else v + 2, v - 1], "Let $u = x^2 - " + str(k) + "x$.",
             "the sum.", f"$u^2{sg(-(u1 + u2))}u{sg(u1 * u2)} = 0$ gives $u = {u1}$ or ${u2}$.".replace(" + 0u", "").replace(" - 0u", ""), [f"Each of $x^2 - {k}x = {u1}$ and $x^2 - {k}x = {u2}$ has two real roots summing to ${k}$.", f"Solutions: " + ", ".join(map(str, sorted(xs))) + f"; sum ${v}$."], "only solving one of the quadratics.")


@reg(S, "challenge")
def rtsc_common(r):
    a = r.randint(-5, 5)
    b, c, d, e = r.sample([x for x in range(-6, 7) if x != a], 4)
    P_, Q_ = poly_from_roots([a, b, c]), poly_from_roots([a, d, e])
    p = f"The polynomials ${ptex(P_)}$ and ${ptex(Q_)}$ have exactly one common root. What is it?"
    return Q(p, a, [b, d, -a if a else 7, c, e], "Test small integer candidates in both.",
             "the common root.", "integer roots divide the constant term; check which candidate works for both.", [f"Roots of the first: ${a}, {b}, {c}$; of the second: ${a}, {d}, {e}$.", f"Common: ${a}$."], "picking a root of only one polynomial.")


@reg(S, "challenge")
def rtsc_double_k(r):
    a = r.randint(1, 4)
    v = 2 * a ** 3
    p = f"For which positive $k$ does $x^3 - {3 * a * a}x + k = 0$ have a repeated root?"
    return Q(p, v, [a ** 3, 3 * a * a, 4 * a ** 3, v + 1, a * a], "A repeated root is also a root of the derivative.",
             "$k$.", f"the derivative $3x^2 - {3 * a * a}$ vanishes at $x = \\pm {a}$.", [f"At $x = {a}$: ${a ** 3} - {3 * a ** 3} + k = 0$, so $k = {v}$ (positive).", f"At $x = -{a}$ we'd get $k = -{v}$."], "using $x = 0$.")


@reg(S, "challenge")
def rtsc_noninteger(r):
    r1, r2 = F(r.randint(1, 5), r.choice([2, 3])), F(-r.randint(1, 5), r.choice([2, 3]))
    k = r.randint(-4, 4)
    if r1.denominator == 1 or r2.denominator == 1:
        return None
    lead = r1.denominator * r2.denominator
    c = [x * lead for x in poly_from_roots([r1, r2, F(k)])]
    if any(x.denominator != 1 for x in c):
        return None
    v = r1 + r2
    p = f"The equation ${ptex(c)} = 0$ has one integer root and two non-integer rational roots. What is the sum of the non-integer roots?"
    return Q(p, v, [v + k, -v if v else 1, r1 * r2, F(-c[1], c[0]), v + 1], "Find the integer root, then use Vieta.",
             "the sum.", "sum of all roots $= -\\frac{b}{a}$; subtract the integer root.", [f"Integer root: ${k}$.", f"All roots sum to ${ft(F(-c[1], c[0]))}$; the other two sum to ${ft(v)}$."], "forgetting to remove the integer root.") if F(-c[1], c[0]) != v else None


@reg(S, "challenge")
def rtsc_count_quartic(r):
    p1, p2 = r.randint(-9, 9), r.randint(-9, 9)
    S_, P_ = p1 + p2, p1 * p2
    cnt = sum(2 if u > 0 else 1 if u == 0 else 0 for u in {p1, p2})
    p = f"How many real solutions does $x^4{sg(-S_)}x^2{sg(P_)} = 0$ have?".replace("+ 0x^2 ", "").replace("- 0x^2 ", "").replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, cnt, [x for x in (0, 1, 2, 3, 4) if x != cnt], "Let $u = x^2$; only $u \\ge 0$ gives real $x$.",
             "the count.", f"$u^2{sg(-S_)}u{sg(P_)} = 0$ gives $u = {p1}$ and $u = {p2}$.", [f"Positive $u$ gives two solutions; $u = 0$ gives one; negative $u$ gives none.", f"Total: ${cnt}$."], "counting four solutions automatically.") if p1 != p2 else None


@reg(S, "challenge")
def rtsc_sqrt_eq(r):
    x, b = r.randint(2, 10), r.randint(0, 6)
    if x - b <= 0:
        return None
    a = (x - b) ** 2 - x
    other = 2 * b + 1 - x
    p = f"Solve $\\sqrt{{x{sg(a)}}} = x{sg(-b)}$.".replace("x + 0", "x").replace("x - 0", "x")
    return Q(p, x, [other if other != x else x + 1, x + 1, x - 1, b, (x - b) ** 2 if (x - b) ** 2 != x else x + 2], "Square, then check for extraneous roots.",
             "the solution.", f"squaring: $x{sg(a)} = (x{sg(-b)})^2$; we need $x{sg(-b)} \\ge 0$.".replace("x + 0", "x").replace("x - 0", "x"),
             [f"The quadratic has roots ${x}$ and ${other}$.", f"Only $x = {x}$ makes $x{sg(-b)} \\ge 0$ (and checks).".replace("x + 0", "x").replace("x - 0", "x")], "keeping the extraneous root.") if other != x and other - b < 0 else None


# ================================================================ con_parabolas
S = "con_parabolas"


@reg(S, "basics")
def cpa_center(r):
    h, k, rr = r.randint(-8, 8), r.randint(-8, 8), r.randint(1, 9)
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - rr * rr
    p = f"What is the sum of the coordinates of the center of $x^2 + y^2{sg(D)}x{sg(E)}y{sg(Fc)} = 0$?".replace("+ 0x ", "").replace("- 0x ", "").replace("+ 0y ", "").replace("- 0y ", "").replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, h + k, [-(h + k) if h + k else 1, D + E, h - k if h - k != h + k else h + k + 1, rr, h + k + 2], "Complete the squares.",
             "the coordinate sum.", "the center is $\\left(-\\frac{D}{2}, -\\frac{E}{2}\\right)$.", [f"Center $({h}, {k})$; sum ${h + k}$."], "forgetting to halve and negate.")


@reg(S, "basics")
def cpa_directrix(r):
    a = F(r.choice([1, 2, 4, 8, -1, -2, -4]), r.choice([1, 2, 4, 8, 16]))
    v = -1 / (4 * a)
    p = f"What is the $y$-coordinate of the directrix of $y = {ft(a) if a != 1 else ''}x^2$?".replace("y = -1x", "y = -x")
    return Q(p, v, [-v, 4 * a, -4 * a if -4 * a != v else v + 1, 1 / (4 * a) if 1 / (4 * a) != -v else v * 2, -1 / (2 * a)], "Write it as $x^2 = 4py$.",
             "the directrix.", "for $x^2 = 4py$, the focus is $(0, p)$ and the directrix is $y = -p$.", [f"$x^2 = {ft(1 / a)}y$, so $p = {ft(1 / (4 * a))}$.", f"Directrix: $y = {ft(v)}$."], "giving the focus instead.")


@reg(S, "basics")
def cpa_axis(r):
    a = r.choice([1, 2, 3, -1, -2, 4])
    b = r.randint(-12, 12)
    c = r.randint(-9, 9)
    v = F(-b, 2 * a)
    p = f"What is the axis of symmetry of $y = {ptex([a, b, c])}$? Give the $x$-value."
    return Q(p, v, [-v if v else F(1), F(-b, a), F(b, 2 * a) if F(b, 2 * a) != v else v + 1, F(c, 1) if F(c) != v else v + 2, v + 1], "$x = -\\frac{b}{2a}$.",
             "the axis.", "the vertex formula.", [f"$-\\frac{{{b}}}{{2 \\cdot {par(a)}}} = {ft(v)}$."], "forgetting the 2.") if b else None


@reg(S, "basics")
def cpa_min(r):
    a = r.choice([1, 2, 3])
    h, k = r.randint(-6, 6), r.randint(-9, 9)
    b, c = -2 * a * h, a * h * h + k
    p = f"What is the minimum value of $y = {ptex([a, b, c])}$?"
    return Q(p, k, [c, h, -k if k else 1, k + a, a * h * h], "Complete the square.",
             "the minimum.", f"$y = {a if a > 1 else ''}(x{sg(-h)})^2{sg(k)}$.".replace("(x + 0)", "x").replace("(x - 0)", "x"), [f"Minimum at $x = {h}$: $y = {k}$."], "giving the $x$-coordinate.") if b else None


@reg(S, "basics")
def cpa_point_circle(r):
    h, k = r.randint(-5, 5), r.randint(-5, 5)
    x, y = r.randint(-8, 8), r.randint(-8, 8)
    v = (x - h) ** 2 + (y - k) ** 2
    p = f"A circle centered at $({h}, {k})$ passes through $({x}, {y})$. What is $r^2$?"
    return Q(p, v, [(x + h) ** 2 + (y + k) ** 2 if (x + h) ** 2 + (y + k) ** 2 != v else v + 1, x * x + y * y if x * x + y * y != v else v + 2, abs(x - h) + abs(y - k), v + 1, v * 2], "Distance squared.",
             "$r^2$.", "$r^2 = (x - h)^2 + (y - k)^2$.", [f"$({par(x - h)})^2 + ({par(y - k)})^2 = {v}$."], "adding the coordinates instead of subtracting.") if v else None


@reg(S, "basics")
def cpa_diameter(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    v = F(d2, 4)
    p = f"A circle has a diameter with endpoints $({x1}, {y1})$ and $({x2}, {y2})$. What is $r^2$?"
    return Q(p, v, [F(d2), F(d2, 2), v + 1, F((x1 + x2) ** 2 + (y1 + y2) ** 2, 4) if F((x1 + x2) ** 2 + (y1 + y2) ** 2, 4) != v else v * 3, F(abs(x1 - x2) + abs(y1 - y2), 2)], "The radius is half the diameter.",
             "$r^2$.", "$r^2 = \\frac{d^2}{4}$.", [f"$d^2 = {d2}$.", f"$r^2 = {ft(v)}$."], "using $d^2$ as $r^2$.") if d2 else None


@reg(S, "basics")
def cpa_y_ints(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)])
    h = a * r.choice([1, -1])
    v = 2 * b
    p = f"What is the distance between the $y$-intercepts of the circle $(x{sg(-h)})^2 + (y{sg(-k)})^2 = {c * c}$?".replace("(y + 0)", "y").replace("(y - 0)", "y")
    return Q(p, v, [b, c, 2 * c, 2 * a, v + 2], "Set $x = 0$.",
             "the distance.", f"$x = 0$ gives $(y{sg(-k)})^2 = {c * c} - {h * h} = {b * b}$.".replace("(y + 0)", "y").replace("(y - 0)", "y"), [f"$y = {k} \\pm {b}$; distance ${v}$."], "forgetting the factor of 2.")


@reg(S, "basics")
def cpa_x_ints(r):
    a = r.choice([1, -1, 2])
    p1, p2 = r.sample(range(-9, 10), 2)
    c = [a, -a * (p1 + p2), a * p1 * p2]
    v = abs(p1 - p2)
    p = f"What is the distance between the $x$-intercepts of $y = {ptex(c)}$?"
    return Q(p, v, [abs(p1 + p2) if abs(p1 + p2) != v else v + 1, v * v, v + 2, abs(p1 * p2) if abs(p1 * p2) != v else v - 1 if v > 1 else 7, v * 2], "Find the roots.",
             "the distance.", "factor to find the two roots.", [f"Roots ${p1}$ and ${p2}$; distance ${v}$."], "adding the roots.")


@reg(S, "basics")
def cpa_focus(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    pp = F(r.choice([1, 2, 3, -1, -2]), r.choice([1, 2, 4]))
    v = h + k + pp
    p = f"The parabola $y = {ft(1 / (4 * pp)) if 1 / (4 * pp) != 1 else ''}(x{sg(-h)})^2{sg(k)}$ has focus $(a, b)$. What is $a + b$?".replace("(x + 0)", "x").replace("(x - 0)", "x").replace(" + 0$", "$").replace(" - 0$", "$").replace("y = -1(", "y = -(")
    if (4 * pp).denominator != 1:
        return None
    return Q(p, v, [h + k - pp, h + k, v + 4 * pp - pp, -v if v else 1, h + k + 4 * pp], "Write as $(x - h)^2 = 4p(y - k)$.",
             "$a + b$.", f"$4p = {ft(4 * pp)}$, so $p = {ft(pp)}$; the focus is $(h, k + p)$.", [f"Focus $({h}, {ft(k + pp)})$; sum ${ft(v)}$."], "subtracting $p$.")


@reg(S, "basics")
def cpa_latus(r):
    pp = r.randint(1, 8)
    form = r.choice(["y^2 = {}x", "x^2 = {}y"])
    p = f"What is the length of the latus rectum of ${form.format(4 * pp)}$ (the chord through the focus perpendicular to the axis)?"
    return Q(p, 4 * pp, [2 * pp, pp, 8 * pp, 4 * pp + 1, 16 * pp], "Latus rectum $= 4p$.",
             "the length.", f"$4p = {4 * pp}$.", [f"At the focus, the half-width is $2p = {2 * pp}$; full length ${4 * pp}$."], "using $2p$.")


@reg(S, "basics")
def cpa_area(r):
    h, k, rr = r.randint(-8, 8), r.randint(-8, 8), r.randint(1, 9)
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - rr * rr
    p = f"What is the area of the circle $x^2 + y^2{sg(D)}x{sg(E)}y{sg(Fc)} = 0$?".replace("+ 0x ", "").replace("- 0x ", "").replace("+ 0y ", "").replace("- 0y ", "").replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, PI(rr * rr), [PI(abs(Fc)) if abs(Fc) != rr * rr and Fc else PI(rr * rr + 1), PI(2 * rr), PI(rr), PI(rr * rr + h * h), PI(rr * rr * 2)], "Complete the squares to find $r^2$.",
             "the area.", "$r^2 = \\left(\\frac{D}{2}\\right)^2 + \\left(\\frac{E}{2}\\right)^2 - F$.", [f"$r^2 = {h * h} + {k * k} - {par(Fc)} = {rr * rr}$.", f"Area: ${rr * rr}\\pi$."], "using $|F|$ as $r^2$.")


@reg(S, "basics")
def cpa_tangent_k(r):
    a = r.choice([1, 2, F(1, 2), 4])
    m = r.randint(-6, 6)
    a = F(a)
    v = -F(m * m) / (4 * a)
    p = f"For what $k$ is the line $y = {m if m not in (1, -1) else ('' if m == 1 else '-')}x + k$ tangent to $y = {ft(a) if a != 1 else ''}x^2$?".replace("y = 0x + k", "y = k")
    return Q(p, v, [-v if v else F(1), F(m * m) / (2 * a) if F(m * m) / (2 * a) != v else v + 1, F(m * m), v + 1, -F(m, 2)], "Set equal; the discriminant must be 0.",
             "$k$.", f"${ft(a)}x^2 - {m}x - k = 0$ needs $({m})^2 + 4 \\cdot {ft(a)} k = 0$.".replace("- -", "+ "), [f"$k = -\\frac{{{m * m}}}{{{ft(4 * a)}}} = {ft(v)}$."], "dropping the negative sign.") if m else None


@reg(S, "basics")
def cpa_two_circles(r):
    r1, r2 = r.randint(1, 8), r.randint(1, 8)
    d = r.choice([r1 + r2, abs(r1 - r2), r1 + r2 + r.randint(1, 4), r.randint(abs(r1 - r2) + 1, r1 + r2 - 1) if r1 + r2 - 1 > abs(r1 - r2) else r1 + r2])
    if d == 0:
        return None
    v = 1 if d in (r1 + r2, abs(r1 - r2)) else 0 if d > r1 + r2 or d < abs(r1 - r2) else 2
    p = f"Circles of radius ${r1}$ and ${r2}$ have centers ${d}$ apart. How many points do they have in common?"
    return Q(p, v, [x for x in (0, 1, 2, 3, 4) if x != v], "Compare the distance with $r_1 + r_2$ and $|r_1 - r_2|$.",
             "the count.", "two circles meet twice when $|r_1 - r_2| < d < r_1 + r_2$, once at equality, and not at all otherwise.",
             [f"$r_1 + r_2 = {r1 + r2}$, $|r_1 - r_2| = {abs(r1 - r2)}$, $d = {d}$.", f"So ${v}$ common point{'s' if v != 1 else ''}."], "ignoring internal tangency.")


@reg(S, "basics")
def cpa_through(r):
    p1, p2 = r.sample(range(-5, 6), 2)
    b, c = r.randint(-8, 8), r.randint(-9, 9)
    y1, y2 = p1 * p1 + b * p1 + c, p2 * p2 + b * p2 + c
    p = f"The parabola $y = x^2 + bx + c$ passes through $({p1}, {y1})$ and $({p2}, {y2})$. What is $c$?"
    return Q(p, c, [b, -c if c else 1, c + 1, y1 if y1 != c else c - 1, b + c if b + c != c else c + 2], "Two equations, two unknowns.",
             "$c$.", "substitute both points and subtract to find $b$.", [f"${y1} = {p1 * p1}{sg(p1)}b + c$ and ${y2} = {p2 * p2}{sg(p2)}b + c$.", f"$b = {b}$, $c = {c}$."], "solving for $b$ and stopping.")


@reg(S, "basics")
def cpa_focal_dist(r):
    pp = r.randint(1, 6)
    x0 = r.randint(1, 12) * pp
    v = x0 + pp
    p = f"The point $P$ on the parabola $y^2 = {4 * pp}x$ has $x$-coordinate ${x0}$. How far is $P$ from the focus?"
    return Q(p, v, [x0, x0 + 4 * pp, x0 - pp if x0 - pp > 0 else v + 1, 2 * x0, v + 1], "Distance to the focus equals distance to the directrix.",
             "the distance.", f"focus $({pp}, 0)$, directrix $x = -{pp}$.", [f"Distance to directrix: ${x0} + {pp} = {v}$."], "forgetting to add $p$.")


@reg(S, "basics")
def cpa_chord(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25)])
    k = a * r.choice([1, -1])
    v = 2 * b
    p = f"The line $y = {k}$ cuts the circle $x^2 + y^2 = {c * c}$. How long is the chord?"
    return Q(p, v, [b, c, 2 * c, 2 * a, v + 2], "Set $y = " + str(k) + "$.",
             "the chord length.", f"$x^2 = {c * c} - {k * k} = {b * b}$.", [f"$x = \\pm {b}$; chord ${v}$."], "forgetting the factor of 2.")


@reg(S, "challenge")
def cpac_min_dist(r):
    a = F(r.randint(1, 12), r.choice([1, 2, 4]))
    if a <= F(1, 2):
        return None
    v = a - F(1, 4)
    p = f"What is the square of the smallest distance from $(0, {ft(a)})$ to a point on $y = x^2$?"
    return Q(p, v, [a * a, a, a - F(1, 2), v + 1, a + F(1, 4)], "Minimize $x^2 + (x^2 - a)^2$.",
             "the squared distance.", f"with $u = x^2 \\ge 0$: $u + (u - {ft(a)})^2$ is smallest at $u = {ft(a - F(1, 2))}$.", [f"Value: ${ft(a - F(1, 2))} + \\frac{{1}}{{4}} = {ft(v)}$."], "using the vertex $(0, 0)$.")


@reg(S, "challenge")
def cpac_tangent_axes(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    p = f"Two circles are tangent to both coordinate axes and pass through $({a}, {b})$. What is the sum of their radii?"
    return Q(p, 2 * (a + b), [a + b, a * a + b * b, 2 * a * b, 4 * (a + b), (a + b) * 2 + 1], "Center $(r, r)$.",
             "the sum of the radii.", f"$(r - {a})^2 + (r - {b})^2 = r^2$.", [f"$r^2 - {2 * (a + b)}r + {a * a + b * b} = 0$.", f"By Vieta, the radii sum to ${2 * (a + b)}$."], "forgetting it's a quadratic with two roots.")


@reg(S, "challenge")
def cpac_focal_chord(r):
    pp = r.randint(1, 6)
    p = f"A line of slope $1$ passes through the focus of $y^2 = {4 * pp}x$. How long is the chord it cuts from the parabola?"
    return Q(p, 8 * pp, [4 * pp, 2 * pp, 16 * pp, 8 * pp + 2, 6 * pp], "Substitute $x = y + " + str(pp) + "$.",
             "the chord length.", f"$y^2 = {4 * pp}(y + {pp})$; the two $y$-values differ by $\\sqrt{{(4p)^2 + 16p^2}}$.",
             [f"$y^2 - {4 * pp}y - {4 * pp * pp} = 0$: $|y_1 - y_2| = \\sqrt{{{16 * pp * pp} + {16 * pp * pp}}} = {4 * pp}\\sqrt{{2}}$.", f"Slope 1: chord $= \\sqrt{{2}} \\cdot {4 * pp}\\sqrt{{2}} = {8 * pp}$."], "giving the latus rectum.")


@reg(S, "challenge")
def cpac_power(r):
    a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
    rr = r.randint(1, c - 1)
    v = c * c - rr * rr
    p = f"From $P = ({a}, {b})$, a line meets the circle $x^2 + y^2 = {rr * rr}$ at $A$ and $B$. What is $PA \\cdot PB$?"
    return Q(p, v, [c * c, rr * rr, c - rr, v + 1, (c - rr) ** 2], "Power of a point.",
             "the product.", "$PA \\cdot PB = OP^2 - r^2$ for every line through $P$.", [f"$OP = {c}$, so ${c * c} - {rr * rr} = {v}$."], "using $OP - r$.")


@reg(S, "challenge")
def cpac_circum(r):
    a, b = r.randint(1, 12), r.randint(1, 12)
    v = F(a * a + b * b, 4)
    p = f"What is the square of the radius of the circle through $(0, 0)$, $({a}, 0)$, and $(0, {b})$?"
    return Q(p, v, [F(a * a + b * b), F(a * a + b * b, 2), v + 1, F(a * b, 2), F(a + b, 2) ** 2 if F(a + b, 2) ** 2 != v else v * 2], "Right angle at the origin.",
             "$r^2$.", "the hypotenuse of a right triangle is a diameter of its circumcircle.", [f"Hypotenuse$^2 = {a * a + b * b}$.", f"$r^2 = \\frac{{{a * a + b * b}}}{{4}} = {ft(v)}$."], "using the hypotenuse as the radius.")


@reg(S, "challenge")
def cpac_radical(r):
    h1, k1, r1 = r.randint(-5, 5), r.randint(-5, 5), r.randint(2, 7)
    h2, k2, r2 = r.randint(-5, 5), r.randint(-5, 5), r.randint(2, 7)
    if k1 == k2:
        return None
    A = -2 * h1 + 2 * h2
    Bc = -2 * k1 + 2 * k2
    Cc = (h1 * h1 + k1 * k1 - r1 * r1) - (h2 * h2 + k2 * k2 - r2 * r2)
    v = F(-Cc, Bc)
    d2 = (h1 - h2) ** 2 + (k1 - k2) ** 2
    if not ((r1 - r2) ** 2 < d2 < (r1 + r2) ** 2):
        return None
    p = f"Circles $(x{sg(-h1)})^2 + (y{sg(-k1)})^2 = {r1 * r1}$ and $(x{sg(-h2)})^2 + (y{sg(-k2)})^2 = {r2 * r2}$ meet at two points. The line through them crosses the $y$-axis at $(0, b)$. What is $b$?".replace("(x + 0)", "x").replace("(x - 0)", "x").replace("(y + 0)", "y").replace("(y - 0)", "y")
    return Q(p, v, [-v if v else F(1), F(Cc, Bc) if F(Cc, Bc) != -v else v + 1, v + 1, F(k1 + k2, 2) if F(k1 + k2, 2) != v else v - 1, F(-Cc, A) if A and F(-Cc, A) != v else v * 2 if v else F(2)], "Subtract the two equations.",
             "$b$.", "subtracting the circle equations cancels $x^2$ and $y^2$, leaving the line through both intersection points.",
             [f"Difference: ${A}x{sg(Bc)}y{sg(Cc)} = 0$.", f"At $x = 0$: $y = {ft(v)}$."], "averaging the centers.")


@reg(S, "challenge")
def cpac_equilateral(r):
    k = r.randint(1, 6)
    a = F(1, k)
    p = f"An equilateral triangle has one vertex at the origin and the other two on $y = {ft(a)}x^2$. What is its side length?"
    return Q(p, rad(2 * k, 3), [rad(k, 3), num(2 * k), rad(2 * k, 2), rad(4 * k, 3), num(4 * k)], "By symmetry the other vertices are $(\\pm \\frac{s}{2}, h)$.",
             "the side length.", f"the height $\\frac{{\\sqrt{{3}}}}{{2}}s$ equals ${ft(a)}\\left(\\frac{{s}}{{2}}\\right)^2$.", [f"$\\frac{{\\sqrt{{3}}}}{{2}}s = \\frac{{s^2}}{{{4 * k}}}$, so $s = {2 * k}\\sqrt{{3}}$."], "using the 45-degree case.")


# ================================================================ con_ellipses
S = "con_ellipses"
TR = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25)]


@reg(S, "basics")
def ell_minor(r):
    a, b = r.sample(range(2, 15), 2)
    v = 2 * min(a, b)
    p = f"What is the length of the minor axis of $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$?"
    return Q(p, v, [2 * max(a, b), min(a, b), min(a, b) ** 2, v + 2, a + b], "The shorter axis.",
             "the minor axis.", "semi-axes are the square roots of the denominators.", [f"Semi-axes ${a}$ and ${b}$; minor axis $2 \\cdot {min(a, b)} = {v}$."], "forgetting to double.")


@reg(S, "basics")
def ell_hyp_vertices(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    o = r.choice(["x", "y"])
    p = f"What is the distance between the vertices of $\\dfrac{{{o}^2}}{{{a * a}}} - \\dfrac{{{'y' if o == 'x' else 'x'}^2}}{{{b * b}}} = 1$?"
    return Q(p, 2 * a, [2 * b, a, 2 * a * a, a + b, 2 * a + 2], "Vertices are at $\\pm a$ along the transverse axis.",
             "the distance.", "the positive term determines the axis.", [f"$a = {a}$; distance ${2 * a}$."], "using $b$.") if a != b else None


@reg(S, "basics")
def ell_find_b(r):
    b, c, a = r.choice(TR)
    p = f"An ellipse has foci $(\\pm {c}, 0)$ and vertices $(\\pm {a}, 0)$. What is the length of its minor axis?".replace(f"(\\pm {c}, 0)", f"(\\pm {b}, 0)")
    p = f"An ellipse has foci $(\\pm {b}, 0)$ and vertices $(\\pm {a}, 0)$. What is the length of its minor axis?"
    return Q(p, 2 * c, [c, 2 * b, a + b, 2 * a, rad(2, a * a + b * b)], "$b^2 = a^2 - c^2$ for ellipses.",
             "the minor axis.", "for an ellipse, $a^2 = b^2 + c^2$.", [f"Semi-minor: $\\sqrt{{{a * a} - {b * b}}} = {c}$.", f"Minor axis: ${2 * c}$."], "adding the squares.")


@reg(S, "basics")
def ell_y_on(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    x = r.randint(1, a - 1) if a > 1 else 1
    v = F(b * b * (a * a - x * x), a * a)
    p = f"The point $({x}, y)$ lies on $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$. What is $y^2$?"
    return Q(p, v, [F(b * b - x * x) if b * b > x * x else v + 1, F(b * b), v + 1, F(a * a - x * x), F(b * b * x * x, a * a)], "Substitute and solve.",
             "$y^2$.", f"$\\frac{{y^2}}{{{b * b}}} = 1 - \\frac{{{x * x}}}{{{a * a}}}$.", [f"$y^2 = {b * b} \\cdot \\frac{{{a * a - x * x}}}{{{a * a}}} = {ft(v)}$."], "subtracting directly.")


@reg(S, "basics")
def ell_hyp_ecc(r):
    a, b, c = r.choice(TR)
    v = F(c, a)
    p = f"What is the eccentricity of the hyperbola $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{{b * b}}} = 1$?"
    return Q(p, v, [F(b, a), F(a, c), F(c, b), v + 1, F(a * a + b * b, a * a)], "$c^2 = a^2 + b^2$, $e = \\frac{c}{a}$.",
             "the eccentricity.", "hyperbolas have $e > 1$.", [f"$c = \\sqrt{{{a * a} + {b * b}}} = {c}$.", f"$e = {ft(v)}$."], "using the ellipse relation.")


@reg(S, "basics")
def ell_center(r):
    h, k = r.randint(-8, 8), r.randint(-8, 8)
    a, b = r.randint(2, 6), r.randint(2, 6)
    p = f"What is the sum of the coordinates of the center of $\\dfrac{{(x{sg(-h)})^2}}{{{a * a}}} + \\dfrac{{(y{sg(-k)})^2}}{{{b * b}}} = 1$?".replace("(x + 0)", "x").replace("(x - 0)", "x").replace("(y + 0)", "y").replace("(y - 0)", "y")
    return Q(p, h + k, [-(h + k) if h + k else 1, h - k if h - k != h + k else h + k + 1, a + b, h + k + 2, h * k if h * k != h + k else h + k - 2], "Read off $(h, k)$.",
             "the sum.", "$(x - h)^2$ means center at $x = h$.", [f"Center $({h}, {k})$, sum ${h + k}$."], "flipping the signs.")


@reg(S, "basics")
def ell_hyp_diff(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    p = f"Point $P$ is on the hyperbola $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{{b * b}}} = 1$ with foci $F_1, F_2$. What is $|PF_1 - PF_2|$?"
    return Q(p, 2 * a, [a, 2 * b, a * a, 2 * a + 2 * b, rad(2, a * a + b * b)], "Definition of a hyperbola.",
             "the difference.", "$|PF_1 - PF_2| = 2a$.", [f"$a = {a}$, so ${2 * a}$."], "using $2c$.")


@reg(S, "basics")
def ell_eq_b2(r):
    b, c, a = r.choice(TR)
    p = f"An ellipse centered at the origin has foci $(\\pm {b}, 0)$ and passes through $({a}, 0)$. Its equation is $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{m}} = 1$. What is $m$?"
    return Q(p, c * c, [a * a + b * b, b * b, c, a * a, c * c + 1], "$b^2 = a^2 - c^2$.",
             "$m$.", "$m$ is the square of the semi-minor axis.", [f"$m = {a * a} - {b * b} = {c * c}$."], "adding instead of subtracting.")


@reg(S, "basics")
def ell_latus(r):
    a, b = r.randint(3, 12), r.randint(2, 11)
    if b >= a:
        a, b = b + 1, a
    v = F(2 * b * b, a)
    p = f"What is the length of a latus rectum of $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$ (the chord through a focus perpendicular to the major axis)?"
    return Q(p, v, [F(b * b, a), F(2 * a * a, b), F(2 * b, a), v + 1, F(2 * b)], "Plug $x = c$ into the equation.",
             "the length.", "at $x = c$, $y^2 = b^2\\left(1 - \\frac{c^2}{a^2}\\right) = \\frac{b^4}{a^2}$.", [f"$|y| = \\frac{{b^2}}{{a}} = {ft(F(b * b, a))}$; length ${ft(v)}$."], "forgetting to double.")


@reg(S, "basics")
def ell_x_int(r):
    a2, b2 = r.choice([4, 9, 16, 25, 36, 49]), r.choice([4, 9, 16, 25, 36])
    m = r.randint(1, 4)
    A, Bc = m * b2, m * a2
    v = 2 * math.isqrt(a2)
    p = f"What is the distance between the $x$-intercepts of ${A}x^2 + {Bc}y^2 = {m * a2 * b2}$?"
    return Q(p, v, [2 * math.isqrt(b2) if 2 * math.isqrt(b2) != v else v + 2, a2, v // 2, v * v, v + 1], "Divide to get standard form.",
             "the distance.", f"divide by ${m * a2 * b2}$: $\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$.", [f"$x$-intercepts $\\pm {math.isqrt(a2)}$; distance ${v}$."], "reading the coefficient as $a^2$.")


@reg(S, "basics")
def ell_rect(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    v = 2 * a * b
    p = f"What is the largest area of a rectangle inscribed in $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$ with sides parallel to the axes?"
    return Q(p, v, [4 * a * b, a * b, v + 1, 2 * (a + b), (a + b) ** 2 // 2], "Corners at $(a\\cos t, b\\sin t)$.",
             "the maximum area.", "area $= 4ab\\cos t\\sin t = 2ab\\sin 2t$.", [f"Maximum when $\\sin 2t = 1$: $2 \\cdot {a} \\cdot {b} = {v}$."], "using $4ab$, the bounding box.")


@reg(S, "basics")
def ell_identify(r):
    A, Bc = r.randint(1, 9) * r.choice([1, -1]), r.randint(1, 9) * r.choice([1, -1])
    Cc = r.randint(1, 30)
    if A < 0 and Bc < 0:
        kind = "none"
    elif A > 0 and Bc > 0:
        kind = "circle" if A == Bc else "ellipse"
    else:
        kind = "hyperbola"
    opts = ["circle", "ellipse", "parabola", "hyperbola", "none"]
    lab = {"none": "no points", "circle": "a circle", "ellipse": "an ellipse (not a circle)", "parabola": "a parabola", "hyperbola": "a hyperbola"}
    p = f"What is the graph of ${A}x^2{sg(Bc)}y^2 = {Cc}$?".replace("1x^2", "x^2").replace(" 1y^2", " y^2")
    return Q(p, C(f"\\text{{{lab[kind]}}}", opts.index(kind)), [C(f"\\text{{{lab[o]}}}", opts.index(o)) for o in opts if o != kind], "Look at the signs of the squared terms.",
             "the type of curve.", "same signs (positive): ellipse or circle; opposite signs: hyperbola; both negative with a positive right side: nothing.", [f"Here: {lab[kind]}."], "calling every second-degree curve an ellipse.")


@reg(S, "basics")
def ell_hyp_point(r):
    a, x0 = r.randint(2, 6), None
    b, y0 = r.randint(1, 6), r.randint(1, 8)
    x0 = a * r.randint(2, 4)
    k2 = F(x0 * x0, a * a) - 1
    v = F(y0 * y0) / k2
    p = f"The hyperbola $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{m}} = 1$ passes through $({x0}, {y0})$. What is $m$?"
    return Q(p, v, [F(y0 * y0), v + 1, F(y0 * y0) * k2, F(x0 * x0 - a * a), v * 2], "Substitute the point.",
             "$m$.", f"$\\frac{{{x0 * x0}}}{{{a * a}}} - \\frac{{{y0 * y0}}}{{m}} = 1$.", [f"$\\frac{{{y0 * y0}}}{{m}} = {ft(k2)}$, so $m = {ft(v)}$."], "forgetting to subtract 1.")


@reg(S, "basics")
def ell_area_general(r):
    a2, b2 = r.sample([1, 4, 9, 16, 25, 36], 2)
    v = math.isqrt(a2) * math.isqrt(b2)
    p = f"What is the area enclosed by ${b2}x^2 + {a2}y^2 = {a2 * b2}$?".replace(" 1x", " x").replace("+ 1y", "+ y").replace("$1x", "$x")
    return Q(p, PI(v), [PI(a2 * b2), PI(v * 2), PI(a2 + b2), PI(F(v, 2)), PI(max(a2, b2))], "Put it in standard form.",
             "the area.", "area $= \\pi ab$.", [f"$\\frac{{x^2}}{{{a2}}} + \\frac{{y^2}}{{{b2}}} = 1$, $a = {math.isqrt(a2)}$, $b = {math.isqrt(b2)}$.", f"Area: ${v}\\pi$."], "using $\\pi a^2 b^2$.")


@reg(S, "basics")
def ell_vertical(r):
    b, c, a = r.choice(TR)
    p = f"What is the distance between the foci of $\\dfrac{{x^2}}{{{c * c}}} + \\dfrac{{y^2}}{{{a * a}}} = 1$?"
    return Q(p, 2 * b, [b, 2 * a, 2 * c, rad(2, a * a + c * c), a + c], "$c^2 = a^2 - b^2$ with the larger denominator.",
             "the distance.", "the major axis is vertical (larger denominator under $y^2$).", [f"$\\sqrt{{{a * a} - {c * c}}} = {b}$; foci $(0, \\pm {b})$; distance ${2 * b}$."], "using $a^2 + b^2$.")


@reg(S, "basics")
def ell_conj(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    p = f"What is the length of the conjugate axis of $\\dfrac{{x^2}}{{{a * a}}} - \\dfrac{{y^2}}{{{b * b}}} = 1$?"
    return Q(p, 2 * b, [2 * a, b, b * b, a + b, rad(2, a * a + b * b)], "The conjugate axis has length $2b$.",
             "the length.", "the conjugate axis is perpendicular to the transverse axis.", [f"$b = {b}$; length ${2 * b}$."], "giving the transverse axis.") if a != b else None


@reg(S, "challenge")
def ellc_perimeter(r):
    b, c, a = r.choice(TR)
    p = f"$P$ is a point on $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{c * c}}} = 1$, not on the $x$-axis, and $F_1, F_2$ are the foci. What is the perimeter of triangle $PF_1F_2$?"
    return Q(p, 2 * a + 2 * b, [2 * a, 2 * a + 2 * c, a + b, 4 * a, 2 * b + 2 * c], "$PF_1 + PF_2 = 2a$.",
             "the perimeter.", "add the focal distance $2c$.", [f"$c = \\sqrt{{{a * a} - {c * c}}} = {b}$.", f"Perimeter: ${2 * a} + {2 * b} = {2 * a + 2 * b}$."], "forgetting $F_1F_2$.")


@reg(S, "challenge")
def ellc_far(r):
    b, c, a = r.choice(TR)
    ask = r.choice(["max", "min"])
    v = a + b if ask == "max" else a - b
    p = f"What is the {'largest' if ask == 'max' else 'smallest'} distance from a focus of $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{c * c}}} = 1$ to a point on the ellipse?"
    return Q(p, v, [a - b if ask == "max" else a + b, a, c, 2 * a, v + 1], "Extremes occur at the vertices on the major axis.",
             "the distance.", "from focus $(c, 0)$, the nearest vertex is at distance $a - c$ and the farthest at $a + c$.", [f"$c = {b}$.", f"Answer: ${v}$."], "using the minor axis endpoints.")


@reg(S, "challenge")
def ellc_chord(r):
    a, b = r.randint(3, 10), r.randint(2, 10)
    k = r.randint(1, a - 1)
    y2 = F(b * b * (a * a - k * k), a * a)
    v = 4 * y2
    p = f"The line $x = {k}$ cuts the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$ in a chord. What is the square of the chord's length?"
    return Q(p, v, [y2, 2 * y2, v + 1, F(4 * (b * b - k * k)) if b * b > k * k else v * 2, F(4 * b * b)], "Find $y^2$ at $x = " + str(k) + "$.",
             "the squared length.", "the chord runs from $-y$ to $y$, so its length is $2|y|$.", [f"$y^2 = {ft(y2)}$.", f"$(2y)^2 = {ft(v)}$."], "forgetting to double $y$.")


@reg(S, "challenge")
def ellc_perp(r):
    a, b = r.randint(3, 12), r.randint(2, 11)
    if b >= a:
        a, b = b + 1, a
    p = f"$P$ is a point on $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$ with $\\angle F_1PF_2 = 90^\\circ$, where $F_1, F_2$ are the foci. What is the area of triangle $F_1PF_2$?"
    return Q(p, b * b, [a * b, a * a - b * b, F(b * b, 2), a * a, 2 * b * b], "Let $m = PF_1$, $n = PF_2$.",
             "the area.", "$m + n = 2a$ and $m^2 + n^2 = (2c)^2$.", [f"$2mn = (m + n)^2 - (m^2 + n^2) = 4a^2 - 4c^2 = 4b^2$.", f"Area $= \\frac{{mn}}{{2}} = b^2 = {b * b}$."], "using $\\frac{1}{2} \\cdot 2c \\cdot b$.")


@reg(S, "challenge")
def ellc_rect_hyp(r):
    s = r.randint(1, 9)
    k = s * s
    v = 4 * s
    p = f"What is the distance between the foci of the hyperbola $xy = {k}$?"
    return Q(p, v, [2 * s, rad(2, 2 * k), v * 2, rad(4, 2 * k) if rad(4, 2 * k).key != v else num(v + 1), k], "It's a rotated rectangular hyperbola.",
             "the distance.", f"vertices $(\\pm {s}, \\pm {s})$ give $a = {s}\\sqrt{{2}}$; for a rectangular hyperbola $c = a\\sqrt{{2}}$.", [f"$c = {s}\\sqrt{{2}} \\cdot \\sqrt{{2}} = {2 * s}$.", f"Distance $2c = {v}$."], "using $a$ for $c$.")


@reg(S, "challenge")
def ellc_general(r):
    h, k = r.randint(-5, 5), r.randint(-5, 5)
    a2, b2 = r.choice([4, 9, 16, 25]), r.choice([4, 9, 16, 25])
    A, Bc = b2, a2
    D, E = -2 * h * A, -2 * k * Bc
    Fc = A * h * h + Bc * k * k - a2 * b2
    kind = r.choice(["ell", "hyp"])
    if kind == "hyp":
        Bc2, E2 = -Bc, 2 * k * Bc
        Fc2 = A * h * h - Bc * k * k - a2 * b2
        p = f"What is the sum of the coordinates of the center of ${A}x^2 - {Bc}y^2{sg(D)}x{sg(E2)}y{sg(Fc2)} = 0$?"
    else:
        p = f"What is the sum of the coordinates of the center of ${A}x^2 + {Bc}y^2{sg(D)}x{sg(E)}y{sg(Fc)} = 0$?"
    p = p.replace("+ 0x ", "").replace("- 0x ", "").replace("+ 0y ", "").replace("- 0y ", "").replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, h + k, [-(h + k) if h + k else 1, h - k if h - k != h + k else h + k + 2, h + k + 1, D + E if D + E not in (h + k,) else h + k - 1, a2 + b2], "Complete the square in $x$ and in $y$.",
             "the center's coordinate sum.", "group $x$ terms and $y$ terms, then factor out the leading coefficients.", [f"Center $({h}, {k})$, sum ${h + k}$."], "forgetting to divide by the leading coefficient.")


@reg(S, "challenge")
def ellc_tangent(r):
    a, b = r.randint(2, 6), r.randint(1, 6)
    m = r.randint(1, 4)
    v = a * a * m * m + b * b
    p = f"The line $y = {m if m > 1 else ''}x + k$ is tangent to $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$. What is $k^2$?"
    return Q(p, v, [a * a + b * b * m * m, a * a * m * m - b * b if a * a * m * m > b * b else v + 1, a * a + b * b, v + m, (a * m + b) ** 2], "The tangency condition is $k^2 = a^2m^2 + b^2$.",
             "$k^2$.", "substitute and set the discriminant to zero.", [f"$k^2 = {a * a} \\cdot {m * m} + {b * b} = {v}$."], "swapping $a$ and $b$.")


# ================================================================ con_analytic
S = "con_analytic"


@reg(S, "basics")
def ana_mid3(r):
    P1, P2 = [r.randint(-9, 9) for _ in range(3)], [r.randint(-9, 9) for _ in range(3)]
    m = [F(a + b, 2) for a, b in zip(P1, P2)]
    v = sum(m)
    p = f"What is the sum of the coordinates of the midpoint of $({P1[0]}, {P1[1]}, {P1[2]})$ and $({P2[0]}, {P2[1]}, {P2[2]})$?"
    return Q(p, v, [2 * v, v + 1, F(sum(P1) - sum(P2), 2), -v if v else F(1), F(sum(P1))], "Average each coordinate.",
             "the sum.", "midpoint coordinates are averages.", [f"Midpoint $({ft(m[0])}, {ft(m[1])}, {ft(m[2])})$; sum ${ft(v)}$."], "not dividing by 2.")


@reg(S, "basics")
def ana_perp(r):
    x1, y1, x2, y2 = [r.randint(-9, 9) for _ in range(4)]
    if x1 == x2 or y1 == y2:
        return None
    m = F(y2 - y1, x2 - x1)
    v = -1 / m
    p = f"What is the slope of a line perpendicular to the line through $({x1}, {y1})$ and $({x2}, {y2})$?"
    return Q(p, v, [m, -m, 1 / m, v + 1, F(x2 - x1, y2 - y1) if F(x2 - x1, y2 - y1) != v else v * 2], "Negative reciprocal.",
             "the slope.", "perpendicular slopes multiply to $-1$.", [f"Slope: ${ft(m)}$.", f"Perpendicular: ${ft(v)}$."], "forgetting the negative sign.")


@reg(S, "basics")
def ana_pt_line(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
    a *= r.choice([1, -1])
    x0, y0 = r.randint(-6, 6), r.randint(-6, 6)
    cc = r.randint(-20, 20)
    num_ = abs(a * x0 + b * y0 + cc)
    v = F(num_, c)
    p = f"What is the distance from $({x0}, {y0})$ to the line ${a}x{sg(b)}y{sg(cc)} = 0$?".replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, v, [F(num_), F(num_, a * a + b * b), v + 1, F(abs(a * x0 + b * y0), c) if F(abs(a * x0 + b * y0), c) != v else v * 2, F(num_, abs(a) + b)], "Point-to-line formula.",
             "the distance.", "$\\frac{|ax_0 + by_0 + c|}{\\sqrt{a^2 + b^2}}$.", [f"Numerator: $|{a * x0 + b * y0 + cc}| = {num_}$; denominator: ${c}$.", f"${ft(v)}$."], "forgetting the square root.") if num_ else None


@reg(S, "basics")
def ana_parallel(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
    c1, c2 = r.sample(range(-20, 21), 2)
    v = F(abs(c1 - c2), c)
    p = f"What is the distance between the parallel lines ${a}x + {b}y{sg(c1)} = 0$ and ${a}x + {b}y{sg(c2)} = 0$?".replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, v, [F(abs(c1 - c2)), F(abs(c1 + c2), c) if F(abs(c1 + c2), c) != v else v + 1, F(abs(c1 - c2), a + b), v * 2, F(abs(c1 - c2), c * c)], "$\\frac{|c_1 - c_2|}{\\sqrt{a^2 + b^2}}$.",
             "the distance.", "the parallel-lines distance formula.", [f"$\\frac{{{abs(c1 - c2)}}}{{{c}}} = {ft(v)}$."], "adding the constants.")


@reg(S, "basics")
def ana_shoelace(r):
    pts = [(r.randint(-6, 6), r.randint(-6, 6)) for _ in range(3)]
    A2 = abs(sum(pts[i][0] * pts[(i + 1) % 3][1] - pts[(i + 1) % 3][0] * pts[i][1] for i in range(3)))
    if A2 == 0:
        return None
    v = F(A2, 2)
    p = f"What is the area of the triangle with vertices $({pts[0][0]}, {pts[0][1]})$, $({pts[1][0]}, {pts[1][1]})$, $({pts[2][0]}, {pts[2][1]})$?"
    return Q(p, v, [F(A2), v + 1, v / 2, v + F(1, 2), F(A2 + 2, 2)], "Shoelace formula.",
             "the area.", "$\\frac{1}{2}|x_1y_2 - x_2y_1 + x_2y_3 - x_3y_2 + x_3y_1 - x_1y_3|$.", [f"The sum inside is $\\pm {A2}$.", f"Area $= {ft(v)}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "basics")
def ana_reflect(r):
    x, y = r.randint(-9, 9), r.randint(-9, 9)
    line = r.choice(["y = x", "y = -x", "the x-axis", "the y-axis"])
    img = {"y = x": (y, x), "y = -x": (-y, -x), "the x-axis": (x, -y), "the y-axis": (-x, y)}[line]
    v = img[0] - img[1]
    ln = {"y = x": "the line $y = x$", "y = -x": "the line $y = -x$", "the x-axis": "the $x$-axis", "the y-axis": "the $y$-axis"}[line]
    p = f"The point $({x}, {y})$ is reflected over {ln}. If the image is $(a, b)$, what is $a - b$?"
    return Q(p, v, [-v if v else 1, x - y if x - y != v else v + 1, x + y if x + y != v else v + 2, y - x if y - x != v else v - 1, v + 3], "Apply the reflection rule.",
             "$a - b$.", {"y = x": "swap the coordinates.", "y = -x": "swap and negate.", "the x-axis": "negate $y$.", "the y-axis": "negate $x$."}[line], [f"Image $({img[0]}, {img[1]})$; $a - b = {v}$."], "using the wrong reflection.")


@reg(S, "basics")
def ana_section(r):
    x1, y1, x2, y2 = [r.randint(-9, 9) for _ in range(4)]
    m, n = r.randint(1, 4), r.randint(1, 4)
    X = F(n * x1 + m * x2, m + n)
    Y = F(n * y1 + m * y2, m + n)
    v = X + Y
    p = f"Point $P$ is on segment $AB$ with $A = ({x1}, {y1})$, $B = ({x2}, {y2})$, and $AP : PB = {m} : {n}$. What is the sum of $P$'s coordinates?"
    return Q(p, v, [F(m * x1 + n * x2 + m * y1 + n * y2, m + n) if F(m * x1 + n * x2 + m * y1 + n * y2, m + n) != v else v + 1, F(x1 + x2 + y1 + y2, 2) if F(x1 + x2 + y1 + y2, 2) != v else v + 2, v + 1, -v if v else F(1), F(x1 + y1)], "Weighted average: closer to $A$ when $m$ is small.",
             "the coordinate sum.", f"$P = \\frac{{{n}A + {m}B}}{{{m + n}}}$.", [f"$P = ({ft(X)}, {ft(Y)})$; sum ${ft(v)}$."], "swapping the weights.") if m != n else None


@reg(S, "basics")
def ana_centroid(r):
    pts = [(r.randint(-9, 9), r.randint(-9, 9)) for _ in range(3)]
    G = (F(sum(p_[0] for p_ in pts), 3), F(sum(p_[1] for p_ in pts), 3))
    v = G[0] + G[1]
    p = f"What is the sum of the coordinates of the centroid of the triangle with vertices " + ", ".join(f"$({a}, {b})$" for a, b in pts) + "?"
    return Q(p, v, [3 * v, F(sum(a + b for a, b in pts), 2), v + 1, -v if v else F(1), v * 2], "Average the vertices.",
             "the sum.", "the centroid is the average of the three vertices.", [f"Centroid $({ft(G[0])}, {ft(G[1])})$; sum ${ft(v)}$."], "dividing by 2.")


@reg(S, "basics")
def ana_yint(r):
    x1, y1, x2, y2 = [r.randint(-9, 9) for _ in range(4)]
    if x1 == x2:
        return None
    m = F(y2 - y1, x2 - x1)
    b = y1 - m * x1
    p = f"What is the $y$-intercept of the line through $({x1}, {y1})$ and $({x2}, {y2})$?"
    return Q(p, b, [m, -b if b else F(1), y1 + m * x1 if y1 + m * x1 != b else b + 1, b + 1, -b / m if m and -b / m != b else b * 2 if b else F(2)], "Find the slope, then plug in a point.",
             "the $y$-intercept.", "$b = y_1 - mx_1$.", [f"$m = {ft(m)}$.", f"$b = {y1} - {fp(m)} \\cdot {par(x1)} = {ft(b)}$."], "giving the $x$-intercept.")


@reg(S, "basics")
def ana_collinear(r):
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    d = (r.randint(1, 4), r.randint(-5, 5))
    s, t = r.randint(1, 3), r.randint(4, 6)
    x2, y2 = x1 + s * d[0], y1 + s * d[1]
    x3, y3 = x1 + t * d[0], y1 + t * d[1]
    p = f"The points $({x1}, {y1})$, $({x2}, k)$, and $({x3}, {y3})$ lie on one line. What is $k$?"
    return Q(p, y2, [y2 + 1, -y2 if y2 else 1, y3 - y1, y1 + y3 - y2 if y1 + y3 - y2 != y2 else y2 + 2, y2 - 2], "Equal slopes.",
             "$k$.", "the slope from the first point to each other point is the same.", [f"Slope: $\\frac{{{y3 - y1}}}{{{x3 - x1}}} = {ft(F(y3 - y1, x3 - x1))}$.", f"$k = {y1} + {fp(F(y3 - y1, x3 - x1))} \\cdot {x2 - x1} = {y2}$."], "using the midpoint.")


@reg(S, "basics")
def ana_angle(r):
    m1, m2 = r.sample(range(-5, 6), 2)
    if 1 + m1 * m2 == 0:
        return None
    v = abs(F(m1 - m2, 1 + m1 * m2))
    p = f"Lines with slopes ${m1}$ and ${m2}$ meet at an acute angle $\\theta$. What is $\\tan\\theta$?"
    return Q(p, v, [abs(F(m1 - m2, 1 - m1 * m2)) if 1 - m1 * m2 and abs(F(m1 - m2, 1 - m1 * m2)) != v else v + 1, F(abs(m1 - m2)), v + 1, 1 / v if v and 1 / v != v else v + 2, F(abs(m1 + m2))], "$\\tan\\theta = \\left|\\frac{m_1 - m_2}{1 + m_1m_2}\\right|$.",
             "$\\tan\\theta$.", "tangent of the difference of the inclination angles.", [f"$\\left|\\frac{{{m1} - {par(m2)}}}{{1 + {par(m1)}{par(m2)}}}\\right| = {ft(v)}$."], "using $1 - m_1m_2$.") if v else None


@reg(S, "basics")
def ana_sphere(r):
    h, k, l, rr = r.randint(-5, 5), r.randint(-5, 5), r.randint(-5, 5), r.randint(1, 8)
    D, E, Fz, G = -2 * h, -2 * k, -2 * l, h * h + k * k + l * l - rr * rr
    p = f"What is the radius of the sphere $x^2 + y^2 + z^2{sg(D)}x{sg(E)}y{sg(Fz)}z{sg(G)} = 0$?".replace("+ 0x ", "").replace("- 0x ", "").replace("+ 0y ", "").replace("- 0y ", "").replace("+ 0z ", "").replace("- 0z ", "").replace(" + 0 =", " =").replace(" - 0 =", " =")
    return Q(p, rr, [rr * rr, rr + 1, abs(G) if abs(G) not in (rr,) and G else rr + 2, h + k + l if h + k + l not in (rr,) else rr + 3, rr * 2], "Complete three squares.",
             "the radius.", "$r^2 = h^2 + k^2 + l^2 - G$ with center $(h, k, l)$.", [f"Center $({h}, {k}, {l})$; $r^2 = {h * h + k * k + l * l} - {par(G)} = {rr * rr}$.", f"$r = {rr}$."], "forgetting the constant term.")


@reg(S, "basics")
def ana_rot(r):
    x, y = r.randint(-9, 9), r.randint(-9, 9)
    d = r.choice([90, 180, 270])
    img = {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[d]
    v = img[0] + 2 * img[1]
    p = f"The point $({x}, {y})$ is rotated ${d}^\\circ$ counterclockwise about the origin to $(a, b)$. What is $a + 2b$?"
    other = {90: (y, -x), 180: (x, y), 270: (-y, x)}[d]
    return Q(p, v, [other[0] + 2 * other[1] if other[0] + 2 * other[1] != v else v + 1, x + 2 * y if x + 2 * y != v else v + 2, v + 1, -v if v else 3, img[1] + 2 * img[0] if img[1] + 2 * img[0] != v else v - 1], "Rotation rules.",
             "$a + 2b$.", "$90^\\circ$: $(x, y) \\to (-y, x)$; $180^\\circ$: $(-x, -y)$; $270^\\circ$: $(y, -x)$.", [f"Image $({img[0]}, {img[1]})$; $a + 2b = {v}$."], "rotating clockwise.")


@reg(S, "basics")
def ana_perp_bis(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    if y1 == y2 or x1 == x2:
        return None
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    m = -F(x2 - x1, y2 - y1)
    b = my - m * mx
    p = f"What is the $y$-intercept of the perpendicular bisector of the segment from $({x1}, {y1})$ to $({x2}, {y2})$?"
    return Q(p, b, [my, -b if b else F(1), b + 1, my + m * mx if my + m * mx != b else b + 2, F(y1 + y2) - m * mx if F(y1 + y2) - m * mx != b else b - 1], "It passes through the midpoint with the negative-reciprocal slope.",
             "the $y$-intercept.", "midpoint plus perpendicular slope.", [f"Midpoint $({ft(mx)}, {ft(my)})$; slope ${ft(m)}$.", f"$b = {ft(my)} - {fp(m)} \\cdot {fp(mx)} = {ft(b)}$."], "using the original slope.")


@reg(S, "basics")
def ana_square_diag(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    if d2 == 0:
        return None
    v = F(d2, 2)
    p = f"Opposite vertices of a square are $({x1}, {y1})$ and $({x2}, {y2})$. What is the area of the square?"
    return Q(p, v, [F(d2), F(d2, 4), v + 1, F(abs(x1 - x2) * abs(y1 - y2)) if F(abs(x1 - x2) * abs(y1 - y2)) != v else v * 2, F((abs(x1 - x2) + abs(y1 - y2)) ** 2, 4) if F((abs(x1 - x2) + abs(y1 - y2)) ** 2, 4) != v else v + 2], "Area $= \\frac{d^2}{2}$.",
             "the area.", "a square's area is half the square of its diagonal.", [f"$d^2 = {d2}$, area ${ft(v)}$."], "using $d^2$.")


@reg(S, "basics")
def ana_equidistant(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    if x1 == x2:
        return None
    v = F(x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1, 2 * (x2 - x1))
    p = f"What point $(x, 0)$ on the $x$-axis is equally far from $({x1}, {y1})$ and $({x2}, {y2})$? Give $x$."
    return Q(p, v, [F(x1 + x2, 2) if F(x1 + x2, 2) != v else v + 1, -v if v else F(1), v + 1, F(y1 + y2, 2) if F(y1 + y2, 2) != v else v + 2, v * 2 if v else F(3)], "Set the squared distances equal.",
             "$x$.", f"$(x - {x1})^2 + {y1 * y1} = (x - {x2})^2 + {y2 * y2}$.".replace("- -", "+ "), [f"Expanding: ${2 * (x2 - x1)}x = {x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1}$.", f"$x = {ft(v)}$."], "averaging the $x$-coordinates.")


@reg(S, "challenge")
def anac_reflect_line(r):
    k = r.randint(-6, 6)
    x, y = r.randint(-8, 8), r.randint(-8, 8)
    img = (y - k, x + k)
    v = img[0] + img[1]
    p = f"The point $({x}, {y})$ is reflected over the line $y = x{sg(k)}$. What is the sum of the coordinates of its image?".replace(" + 0$", "$").replace(" - 0$", "$")
    return Q(p, v, [x + y, y + x + 2 * k if y + x + 2 * k != v else v + 1, v + 1, (y + k) + (x - k) if (y + k) + (x - k) != v else v - 2, -v if v else 3], "Shift so the line passes through the origin.",
             "the coordinate sum.", f"reflecting over $y = x + k$ sends $(x, y)$ to $(y - k, x + k)$.", [f"Image: $({img[0]}, {img[1]})$; sum ${v}$."], "swapping without shifting.")


@reg(S, "challenge")
def anac_pick(r):
    pts = [(0, 0), (r.randint(2, 10), 0), (r.randint(0, 10), r.randint(2, 10))]
    A2 = abs(pts[1][0] * pts[2][1] - pts[2][0] * pts[1][1])
    Bd = sum(math.gcd(abs(pts[i][0] - pts[(i + 1) % 3][0]), abs(pts[i][1] - pts[(i + 1) % 3][1])) for i in range(3))
    I = F(A2, 2) - F(Bd, 2) + 1
    p = f"How many lattice points lie strictly inside the triangle with vertices $(0, 0)$, $({pts[1][0]}, 0)$, and $({pts[2][0]}, {pts[2][1]})$?"
    return Q(p, I, [I + Bd, F(A2, 2), I + 1, I - 1 if I > 1 else I + 2, F(A2, 2) - Bd], "Pick's Theorem: $A = I + \\frac{B}{2} - 1$.",
             "the interior count $I$.", "find the area and the boundary lattice points ($\\gcd$ of each side's run and rise).", [f"Area: ${ft(F(A2, 2))}$. Boundary points: ${Bd}$.", f"$I = {ft(F(A2, 2))} - {ft(F(Bd, 2))} + 1 = {ft(I)}$."], "forgetting the $-1$.") if I >= 0 else None


@reg(S, "challenge")
def anac_angle3d(r):
    u, w, c = r.choice([((1, 1, 0), (0, 1, 1), F(1, 2)), ((1, 0, 0), (1, 1, 0), None), ((1, 1, 1), (1, 1, 0), None), ((1, 2, 2), (2, 1, -2), F(0)), ((2, 1, 2), (1, 2, 2), F(8, 9)), ((1, 0, 1), (0, 1, 1), F(1, 2)), ((3, 0, 4), (0, 3, 4), F(16, 25))])
    dot = sum(a * b for a, b in zip(u, w))
    nu, nw = sum(a * a for a in u), sum(a * a for a in w)
    cs2 = F(dot * dot, nu * nw)
    v = F(dot * abs(dot), nu * nw)
    p = f"What is $\\cos^2\\theta$, where $\\theta$ is the angle between the vectors $\\langle {u[0]}, {u[1]}, {u[2]} \\rangle$ and $\\langle {w[0]}, {w[1]}, {w[2]} \\rangle$?"
    return Q(p, cs2, [F(abs(dot), nu * nw) if F(abs(dot), nu * nw) != cs2 else cs2 + 1, 1 - cs2 if 1 - cs2 != cs2 else F(1, 3), cs2 + F(1, 9), F(dot, nu + nw) if F(dot, nu + nw) != cs2 else cs2 / 2 if cs2 else F(2, 3), F(1) if cs2 != 1 else F(1, 4)], "Dot product.",
             "$\\cos^2\\theta$.", "$\\cos\\theta = \\frac{u \\cdot w}{|u||w|}$.", [f"$u \\cdot w = {dot}$, $|u|^2 = {nu}$, $|w|^2 = {nw}$.", f"$\\cos^2\\theta = \\frac{{{dot * dot}}}{{{nu * nw}}} = {ft(cs2)}$."], "forgetting to square the magnitudes.")


@reg(S, "challenge")
def anac_cube_diag(r):
    s = r.randint(1, 9) * 3
    p = f"A cube has edge ${s}$. What is the distance from a vertex to the space diagonal that does not pass through it but starts at an adjacent vertex? (Take the vertex $(0, 0, {s})$... )"
    p = f"A cube has edge ${s}$. What is the distance from the vertex $({s}, 0, 0)$ to the space diagonal from $(0, 0, 0)$ to $({s}, {s}, {s})$?"
    return Q(p, rad(F(s, 3), 6), [rad(F(s, 2), 2), rad(F(s, 3), 3), num(s), rad(F(s, 2), 6), rad(s, 2)], "Use the right triangle with the diagonal.",
             "the distance.", "the distance from a point to a line through the origin is $\\frac{|P \\times d|}{|d|}$.", [f"$P = ({s}, 0, 0)$, $d = (1, 1, 1)$: $|P \\times d| = {s}\\sqrt{{2}}$, $|d| = \\sqrt{{3}}$.", f"Distance: ${s}\\sqrt{{\\frac{{2}}{{3}}}} = {rad(F(s, 3), 6).tex}$."], "using the face diagonal.")


@reg(S, "challenge")
def anac_mirror_path(r):
    x1, y1 = r.randint(-8, 0), r.randint(1, 9)
    x2, y2 = r.randint(1, 9), r.randint(1, 9)
    d2 = (x2 - x1) ** 2 + (y1 + y2) ** 2
    p = f"A path goes from $({x1}, {y1})$ to a point on the $x$-axis, then to $({x2}, {y2})$. What is the length of the shortest such path?"
    return Q(p, rad(1, d2), [rad(1, (x2 - x1) ** 2 + (y1 - y2) ** 2) if (x2 - x1) ** 2 + (y1 - y2) ** 2 else num(1), num(y1 + y2 + abs(x2 - x1)), rad(1, d2 + 1), rad(1, d2 - 1), num(y1 + y2)], "Reflect one endpoint over the $x$-axis.",
             "the length.", "the path's length equals the distance from one point to the other's reflection.", [f"Reflect $({x2}, {y2})$ to $({x2}, -{y2})$.", f"Distance: $\\sqrt{{{(x2 - x1) ** 2} + {(y1 + y2) ** 2}}} = {rad(1, d2).tex}$."], "using the straight-line distance (which doesn't touch the axis).")


@reg(S, "challenge")
def anac_lattice_seg(r):
    x1, y1 = r.randint(-20, 20), r.randint(-20, 20)
    g = r.randint(2, 12)
    dx, dy = r.randint(-5, 5), r.randint(-5, 5)
    if math.gcd(dx, dy) != 1:
        return None
    x2, y2 = x1 + g * dx, y1 + g * dy
    v = g + 1
    p = f"How many lattice points (including the endpoints) lie on the segment from $({x1}, {y1})$ to $({x2}, {y2})$?"
    return Q(p, v, [g, g - 1, abs(x2 - x1) + 1, v + 1, abs(y2 - y1) + 1 if abs(y2 - y1) + 1 not in (v, abs(x2 - x1) + 1) else v + 2], "$\\gcd$ of the run and rise.",
             "the count.", "the lattice points are equally spaced; there are $\\gcd(|\\Delta x|, |\\Delta y|) + 1$ of them.", [f"$\\gcd({abs(x2 - x1)}, {abs(y2 - y1)}) = {g}$.", f"Count: ${v}$."], "forgetting an endpoint.")


@reg(S, "challenge")
def anac_quad_area(r):
    pts = [(r.randint(-6, 0), r.randint(-6, 0)), (r.randint(1, 7), r.randint(-6, 0)), (r.randint(1, 7), r.randint(1, 7)), (r.randint(-6, 0), r.randint(1, 7))]
    A2 = abs(sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4)))
    v = F(A2, 2)
    p = f"What is the area of the quadrilateral with vertices " + ", ".join(f"$({a}, {b})$" for a, b in pts) + " (in order)?"
    return Q(p, v, [F(A2), v + 1, v / 2, v + 2, F((max(a for a, _ in pts) - min(a for a, _ in pts)) * (max(b for _, b in pts) - min(b for _, b in pts)))], "Shoelace formula.",
             "the area.", "sum $x_iy_{i+1} - x_{i+1}y_i$ around the polygon, halve the absolute value.", [f"The shoelace sum is $\\pm {A2}$.", f"Area: ${ft(v)}$."], "forgetting to halve.")


# ================================================================ ser_recursion
S = "ser_recursion"


@reg(S, "basics")
def srec_arith(r):
    a, d, n = r.randint(-20, 20), r.randint(-9, 9), r.randint(10, 60)
    if d == 0:
        return None
    v = a + (n - 1) * d
    p = f"An arithmetic sequence starts ${a}, {a + d}, {a + 2 * d}, \\ldots$. What is term number ${n}$?"
    return Q(p, v, [a + n * d, v - d if v - d != v else v + 1, a * d * n if a * d * n != v else v + 2, v + 1, n * d], "$a_n = a_1 + (n - 1)d$.",
             "the term.", "start at $a_1$ and add $d$ a total of $n - 1$ times.", [f"$d = {d}$.", f"${a} + {n - 1} \\cdot {par(d)} = {v}$."], "using $n$ steps instead of $n - 1$.")


@reg(S, "basics")
def srec_geo(r):
    a, q, n = r.randint(1, 6) * r.choice([1, -1]), r.choice([2, 3, -2, -3]), r.randint(4, 9)
    v = a * q ** (n - 1)
    p = f"A geometric sequence starts ${a}, {a * q}, {a * q * q}, \\ldots$. What is term number ${n}$?"
    return Q(p, B(v) if abs(v) >= 1000 else v, [B(a * q ** n) if abs(a * q ** n) >= 1000 else a * q ** n, B(-v) if abs(v) >= 1000 else -v, B(a * q ** (n - 2)) if abs(a * q ** (n - 2)) >= 1000 else a * q ** (n - 2), B(v + 1) if abs(v) >= 1000 else v + 1], "$a_n = a_1 r^{n - 1}$.",
             "the term.", "multiply by the ratio $n - 1$ times.", [f"$r = {q}$.", f"${a} \\cdot ({q})^{{{n - 1}}} = {big(v) if abs(v) >= 1000 else v}$."], "using $n$ factors of $r$.", ans_tex=big(v) if abs(v) >= 1000 else None)


@reg(S, "basics")
def srec_two_terms(r):
    a, d = r.randint(-15, 15), r.randint(-6, 6)
    m, n, q = r.sample(range(2, 30), 3)
    if d == 0:
        return None
    am, an, aq = a + (m - 1) * d, a + (n - 1) * d, a + (q - 1) * d
    p = f"In an arithmetic sequence, $a_{{{m}}} = {am}$ and $a_{{{n}}} = {an}$. What is $a_{{{q}}}$?"
    return Q(p, aq, [aq + d, aq - d, am + an - aq if am + an - aq != aq else aq + 2, aq + 1, a], "Find the common difference first.",
             f"$a_{{{q}}}$.", f"$d = \\frac{{a_{{{n}}} - a_{{{m}}}}}{{{n} - {m}}}$.", [f"$d = \\frac{{{an - am}}}{{{n - m}}} = {d}$.", f"$a_{{{q}}} = {am} + ({q} - {m}) \\cdot {par(d)} = {aq}$."], "dividing by the wrong gap.")


@reg(S, "basics")
def srec_alt(r):
    a, c = r.randint(-9, 9), r.randint(-9, 9)
    N = r.randint(20, 200)
    v = a if N % 2 == 1 else c - a
    p = f"If $a_1 = {a}$ and $a_{{n+1}} = {c} - a_n$, what is $a_{{{N}}}$?".replace("= 0 - a_n", "= -a_n")
    return Q(p, v, [c - a if v == a else a, -v if v else 1, c, v + 1, N * c - a if N * c - a != v else v + 2], "Write out a few terms.",
             f"$a_{{{N}}}$.", "the sequence alternates between two values.", [f"$a_1 = {a}$, $a_2 = {c - a}$, $a_3 = {a}$, ...", f"${N}$ is {'odd' if N % 2 else 'even'}, so $a_{{{N}}} = {v}$."], "computing the wrong parity.") if c - a != a else None


@reg(S, "basics")
def srec_sum_arith(r):
    a, d, n = r.randint(-10, 20), r.randint(-5, 9), r.randint(5, 40)
    v = n * (2 * a + (n - 1) * d) // 2
    p = f"What is the sum of the first ${n}$ terms of the arithmetic sequence ${a}, {a + d}, {a + 2 * d}, \\ldots$?"
    return Q(p, B(v) if abs(v) >= 1000 else v, [B(n * (a + a + n * d) // 2) if abs(n * (a + a + n * d) // 2) >= 1000 else n * (a + a + n * d) // 2, B(v + d) if abs(v) >= 1000 else v + d, B(n * (a + (n - 1) * d)) if abs(n * (a + (n - 1) * d)) >= 1000 else n * (a + (n - 1) * d), B(v - a) if abs(v - a) >= 1000 else v - a], "Average of first and last, times $n$.",
             "the sum.", "$S_n = \\frac{n}{2}(a_1 + a_n)$.", [f"$a_{{{n}}} = {a + (n - 1) * d}$.", f"$\\frac{{{n}}}{{2}}({a}{sg(a + (n - 1) * d)}) = {big(v)}$."], "using $a_{n+1}$ as the last term.", ans_tex=big(v) if abs(v) >= 1000 else None) if d else None


@reg(S, "basics")
def srec_square_minus(r):
    a = r.choice([2, -2, 0, 1, 3, -1])
    c = r.choice([1, 2, -1, -2])
    seq = [a]
    for _ in range(3):
        seq.append(seq[-1] ** 2 - c)
    if abs(seq[-1]) > 10 ** 7:
        return None
    v = seq[3]
    p = f"If $a_1 = {a}$ and $a_{{n+1}} = a_n^2{sg(-c)}$, what is $a_4$?"
    return Q(p, B(v) if abs(v) >= 1000 else v, [B(seq[2]) if abs(seq[2]) >= 1000 else seq[2], B(v + 1) if abs(v) >= 1000 else v + 1, B(-v) if abs(v) >= 1000 and v else (-v if v else 2), B(seq[2] ** 2 + c) if abs(seq[2] ** 2 + c) >= 1000 else seq[2] ** 2 + c], "Compute step by step.",
             "$a_4$.", "apply the rule three times.", [f"$a_2 = {seq[1]}$, $a_3 = {seq[2]}$, $a_4 = {big(v)}$."], "stopping at $a_3$.", ans_tex=big(v) if abs(v) >= 1000 else None) if len(set(seq)) > 1 and seq[2] ** 2 + c != v else None


@reg(S, "basics")
def srec_recip(r):
    a = F(r.choice([2, 3, -1, 5, -2]), r.choice([1, 2, 3]))
    if a == 1:
        return None
    seq = [a, 1 / (1 - a)]
    seq.append(1 / (1 - seq[1]))
    N = r.randint(20, 200)
    v = seq[(N - 1) % 3]
    p = f"If $a_1 = {ft(a)}$ and $a_{{n+1}} = \\dfrac{{1}}{{1 - a_n}}$, what is $a_{{{N}}}$?"
    return Q(p, v, [x for x in seq if x != v] + [v + 1, -v if v else F(1)], "Compute a few terms.",
             f"$a_{{{N}}}$.", "the sequence repeats every 3 terms.", [f"$a_1 = {ft(seq[0])}$, $a_2 = {ft(seq[1])}$, $a_3 = {ft(seq[2])}$, $a_4 = {ft(a)}$, ...", f"${N} \\equiv {(N - 1) % 3 + 1} \\pmod 3$, so $a_{{{N}}} = {ft(v)}$."], "miscounting the cycle position.") if len(set(seq)) == 3 and 0 not in seq else None


@reg(S, "basics")
def srec_index(r):
    a, d = r.randint(-10, 20), r.randint(2, 9)
    n = r.randint(10, 80)
    t = a + (n - 1) * d
    p = f"In the arithmetic sequence ${a}, {a + d}, {a + 2 * d}, \\ldots$, which term equals ${t}$?"
    return Q(p, n, [n - 1, n + 1, F(t, d) if F(t, d) != n else n + 2, F(t - a, d) if F(t - a, d) != n else n - 2, n * 2], "Solve $a_1 + (n - 1)d = " + str(t) + "$.",
             "$n$.", "rearrange the term formula.", [f"$(n - 1) \\cdot {d} = {t - a}$, $n - 1 = {n - 1}$, $n = {n}$."], "forgetting to add 1.")


@reg(S, "basics")
def srec_second(r):
    a1, a2 = r.randint(1, 5), r.randint(2, 9)
    p_, q_ = r.choice([(3, -2), (5, -6), (4, -3), (1, 2), (2, 3)])
    seq = [a1, a2]
    while len(seq) < 9:
        seq.append(p_ * seq[-1] + q_ * seq[-2])
    n = r.randint(5, 7)
    v = seq[n - 1]
    p = f"If $a_1 = {a1}$, $a_2 = {a2}$, and $a_n = {p_}a_{{n-1}}{sg(q_)}a_{{n-2}}$, what is $a_{{{n}}}$?".replace(" 1a", " a").replace("+ 1a", "+ a").replace("- 1a", "- a")
    return Q(p, B(v) if abs(v) >= 1000 else v, [B(seq[n - 2]) if abs(seq[n - 2]) >= 1000 else seq[n - 2], B(seq[n]) if abs(seq[n]) >= 1000 else seq[n], B(v + 1) if abs(v) >= 1000 else v + 1, B(v - p_) if abs(v - p_) >= 1000 else v - p_], "Build up term by term.",
             f"$a_{{{n}}}$.", "apply the recurrence repeatedly.", ["Terms: " + ", ".join(big(x) for x in seq[:n]) + "."], "mixing up which term gets which coefficient.", ans_tex=big(v) if abs(v) >= 1000 else None)


@reg(S, "basics")
def srec_count(r):
    a, d = r.randint(-20, 20), r.randint(2, 9)
    n = r.randint(8, 60)
    L = a + (n - 1) * d
    p = f"How many terms are in the list ${a}, {a + d}, {a + 2 * d}, \\ldots, {L}$?"
    return Q(p, n, [n - 1, n + 1, F(L - a, d) if F(L - a, d) != n else n + 2, F(L, d) if F(L, d) not in (n, n - 1, n + 1) else n + 3, L - a], "$\\frac{\\text{last} - \\text{first}}{d} + 1$.",
             "the count.", "count the steps, then add one.", [f"$\\frac{{{L} - {par(a)}}}{{{d}}} + 1 = {n - 1} + 1 = {n}$."], "forgetting the $+1$.")


@reg(S, "basics")
def srec_triangular(r):
    n = r.randint(5, 60)
    v = n * (n + 1) // 2
    p = f"Dots are arranged in triangles: $1$ dot, then $3$, then $6$, then $10$, ... (row $k$ adds $k$ dots). How many dots are in the ${n}$th triangle?"
    return Q(p, v, [n * n, n * (n - 1) // 2, v + n, 2 * v, v - 1], "$T_n = 1 + 2 + \\cdots + n$.",
             "$T_n$.", "triangular numbers.", [f"$\\frac{{{n} \\cdot {n + 1}}}{{2}} = {v}$."], "using $n^2$.")


@reg(S, "basics")
def srec_fib_sum(r):
    n = r.randint(6, 20)
    f = [0, 1, 1]
    while len(f) < n + 4:
        f.append(f[-1] + f[-2])
    v = f[n + 2] - 1
    p = f"With $F_1 = F_2 = 1$ and $F_{{k}} = F_{{k-1}} + F_{{k-2}}$, what is $F_1 + F_2 + \\cdots + F_{{{n}}}$?"
    return Q(p, v, [f[n + 2], f[n + 1], v - 1, f[n + 1] - 1 if f[n + 1] - 1 != v else v + 2, f[n] * 2], "$F_1 + \\cdots + F_n = F_{n+2} - 1$.",
             "the sum.", "each $F_k = F_{k+2} - F_{k+1}$, so the sum telescopes.", [f"$F_{{{n + 2}}} = {f[n + 2]}$.", f"Sum: ${v}$."], "forgetting the $-1$.")


@reg(S, "basics")
def srec_geo_mean(r):
    a, b = r.choice([(2, 8), (3, 12), (4, 9), (2, 18), (5, 20), (3, 27), (4, 25), (1, 49)])
    k = r.randint(1, 3)
    a, b = a * k, b * k
    v = math.isqrt(a * b)
    p = f"The numbers ${a}$, $x$, ${b}$ form a geometric sequence with $x > 0$. What is $x$?"
    return Q(p, v, [F(a + b, 2), v * 2, v + 1, a * b, b - a], "$x^2 = " + str(a) + " \\cdot " + str(b) + "$.",
             "$x$.", "the middle term of a geometric sequence is the geometric mean.", [f"$x^2 = {a * b}$, $x = {v}$."], "taking the arithmetic mean.")


@reg(S, "basics")
def srec_odd_diff(r):
    c = r.randint(-10, 10)
    N = r.randint(5, 40)
    v = c + N * N - 1
    p = f"If $a_1 = {c}$ and $a_{{n+1}} = a_n + 2n + 1$, what is $a_{{{N}}}$?"
    return Q(p, v, [c + N * N, N * N, v + 2 * N + 1, c + (N - 1) ** 2 if c + (N - 1) ** 2 != v else v + 1, v - 1], "The differences are $3, 5, 7, \\ldots$.",
             f"$a_{{{N}}}$.", "$a_N = a_1 + (3 + 5 + \\cdots + (2N - 1))$.", [f"$3 + 5 + \\cdots + {2 * N - 1} = {N}^2 - 1 = {N * N - 1}$.", f"$a_{{{N}}} = {c} + {N * N - 1} = {v}$."], "forgetting the sum starts at 3.")


@reg(S, "basics")
def srec_units_fib(r):
    n = r.randint(20, 300)
    f = [0, 1]
    for _ in range(n):
        f.append((f[-1] + f[-2]) % 10)
    v = f[n]
    p = f"With $F_1 = F_2 = 1$ and $F_k = F_{{k-1}} + F_{{k-2}}$, what is the units digit of $F_{{{n}}}$?"
    return Q(p, v, [(v + 1) % 10, (v + 3) % 10, (v + 5) % 10, (v + 7) % 10, (v + 9) % 10], "Units digits repeat with period 60.",
             "the units digit.", "track the sequence mod 10; it cycles every 60 terms.", [f"${n} \\bmod 60 = {n % 60}$; $F_{{{n % 60 or 60}}}$ has units digit ${v}$."], "assuming a period of 10.")


@reg(S, "basics")
def srec_product(r):
    c, N = r.randint(2, 9), r.randint(5, 80)
    v = c * N
    p = f"If $a_1 = {c}$ and $a_{{n+1}} = \\dfrac{{n + 1}}{{n}} a_n$, what is $a_{{{N}}}$?"
    return Q(p, v, [c * (N + 1), N, c * (N - 1), c + N, v + c], "Multiply the ratios.",
             f"$a_{{{N}}}$.", "the product $\\frac{2}{1} \\cdot \\frac{3}{2} \\cdots \\frac{N}{N - 1}$ telescopes to $N$.", [f"$a_{{{N}}} = {c} \\cdot {N} = {v}$."], "off by one in the last factor.")


@reg(S, "challenge")
def srecc_recip_add(r):
    k = r.randint(1, 9)
    N = r.randint(10, 100)
    v = F(1, k + N - 1)
    p = f"If $a_1 = {ft(F(1, k))}$ and $a_{{n+1}} = \\dfrac{{a_n}}{{1 + a_n}}$, what is $a_{{{N}}}$?"
    return Q(p, v, [F(1, k + N), F(1, k * N), F(1, N), v * 2, F(1, k + N - 2) if k + N - 2 > 0 else F(2)], "Look at $\\frac{1}{a_n}$.",
             f"$a_{{{N}}}$.", "$\\frac{1}{a_{n+1}} = \\frac{1}{a_n} + 1$, so the reciprocals form an arithmetic sequence.", [f"$\\frac{{1}}{{a_n}} = {k} + (n - 1)$.", f"$a_{{{N}}} = {ft(v)}$."], "off by one in the count.")


@reg(S, "challenge")
def srecc_sqrt(r):
    a, d = r.randint(1, 6), r.randint(1, 9)
    N = r.randint(5, 40)
    v2 = a * a + (N - 1) * d
    p = f"If $a_1 = {a}$ and $a_{{n+1}} = \\sqrt{{a_n^2 + {d}}}$, what is $a_{{{N}}}^2$?"
    return Q(p, v2, [a * a + N * d, (a + (N - 1) * d) ** 2 if (a + (N - 1) * d) ** 2 < 10 ** 6 else v2 + 1, v2 + 1, a + (N - 1) * d, v2 - d], "Square both sides.",
             f"$a_{{{N}}}^2$.", "the squares form an arithmetic sequence with difference " + str(d) + ".", [f"$a_n^2 = {a * a} + (n - 1) \\cdot {d}$.", f"$a_{{{N}}}^2 = {v2}$."], "adding " + str(d) + " to $a_n$ instead of $a_n^2$.")


@reg(S, "challenge")
def srecc_ratio6(r):
    a, b = r.choice([2, 3, 4, 5, F(1, 2)]), r.choice([3, 5, 7, 6, 2])
    a, b = F(a), F(b)
    if a == b:
        return None
    seq = [a, b]
    for _ in range(6):
        seq.append(seq[-1] / seq[-2])
    N = r.randint(20, 300)
    v = seq[(N - 1) % 6]
    p = f"If $a_1 = {ft(a)}$, $a_2 = {ft(b)}$, and $a_n = \\dfrac{{a_{{n-1}}}}{{a_{{n-2}}}}$, what is $a_{{{N}}}$?"
    return Q(p, v, list({x for x in seq[:6] if x != v})[:4] + [v * 2], "Compute six terms.",
             f"$a_{{{N}}}$.", "the sequence repeats with period 6.", ["Terms: " + ", ".join(f"${ft(x)}$" for x in seq[:7]) + ".", f"${N} \\equiv {(N - 1) % 6 + 1} \\pmod 6$, so $a_{{{N}}} = {ft(v)}$."], "assuming period 3.")


@reg(S, "challenge")
def srecc_alt_sum(r):
    n = r.randint(10, 300)
    v = n // 2 if n % 2 == 0 else -(n + 1) // 2
    v = sum((-1) ** k * k for k in range(1, n + 1))
    p = f"What is $-1 + 2 - 3 + 4 - \\cdots {'+' if n % 2 == 0 else '-'} {n}$?"
    return Q(p, v, [-v, n, v + 1, n * (n + 1) // 2, v - 1], "Pair up terms.",
             "the sum.", "each pair $-(2k - 1) + 2k$ equals $1$.", [f"${n // 2}$ pairs give ${n // 2}$" + ("." if n % 2 == 0 else f"; the last term $-{n}$ gives ${v}$.")], "missing the unpaired last term.")


@reg(S, "challenge")
def srecc_affine(r):
    a1, k, c = r.randint(2, 6), r.choice([2, 3]), None
    m = k - 1
    c = -m * r.randint(1, 3)
    fixed = F(-c, k - 1)
    if fixed == a1:
        return None
    n = r.randint(6, 12)
    v = (a1 - fixed) * k ** (n - 1) + fixed
    p = f"If $a_1 = {a1}$ and $a_{{n+1}} = {k}a_n{sg(c)}$, what is $a_{{{n}}}$?"
    return Q(p, B(int(v)), [B(int(a1 * k ** (n - 1))), B(int(v + k ** (n - 1))), B(int((a1 - fixed) * k ** n + fixed)), B(int(v - 1))], "Subtract the fixed point.",
             f"$a_{{{n}}}$.", f"the fixed point is $L = {ft(fixed)}$ (where $L = {k}L{sg(c)}$); then $a_n - L$ is geometric with ratio ${k}$.",
             [f"$a_n = ({a1} - {ft(fixed)}) \\cdot {k}^{{n - 1}} + {ft(fixed)}$.", f"$a_{{{n}}} = {big(int(v))}$."], "ignoring the constant term.", ans_tex=big(int(v))) if v.denominator == 1 else None


@reg(S, "challenge")
def srecc_trib(r):
    n = r.randint(5, 15)
    t = [1, 1, 2]
    while len(t) <= n:
        t.append(t[-1] + t[-2] + t[-3])
    v = t[n]
    nm = r.choice(NAMES)
    p = f"{nm} climbs a staircase of ${n}$ steps, taking $1$, $2$, or $3$ steps at a time. In how many ways can {nm} reach the top?"
    return Q(p, v, [t[n - 1], t[n + 1] if len(t) > n + 1 else v + t[n - 1], v + 1, 2 ** (n - 1), v - 1], "Count by the last move.",
             "the number of ways.", "$W(n) = W(n - 1) + W(n - 2) + W(n - 3)$ with $W(0) = 1$, $W(1) = 1$, $W(2) = 2$.",
             ["Building up: " + ", ".join(f"$W({i}) = {t[i]}$" for i in range(n + 1)) + "."], "forgetting the 3-step moves.")


@reg(S, "challenge")
def srecc_two_power(r):
    n = r.randint(5, 15)
    a = [1, 1]
    while len(a) < n:
        a.append(a[-1] + 2 * a[-2])
    v = a[n - 1]
    p = f"If $a_1 = a_2 = 1$ and $a_n = a_{{n-1}} + 2a_{{n-2}}$, what is $a_{{{n}}}$?"
    return Q(p, B(v) if v >= 1000 else v, [B(a[n - 2]) if a[n - 2] >= 1000 else a[n - 2], B(2 ** (n - 1)) if 2 ** (n - 1) >= 1000 else 2 ** (n - 1), B(v + 1) if v >= 1000 else v + 1, B(v * 2) if v * 2 >= 1000 else v * 2], "Closed form: $a_n = \\frac{2^n - (-1)^n}{3}$.",
             f"$a_{{{n}}}$.", "characteristic roots $2$ and $-1$.", [f"$\\frac{{2^{{{n}}} - ({(-1) ** n})}}{{3}} = {big(v)}$."], "using only the $2^n$ part.", ans_tex=big(v) if v >= 1000 else None)


# ================================================================ ser_telescoping
S = "ser_telescoping"


@reg(S, "basics")
def stel_log(r):
    k = r.randint(1, 5)
    N = 10 ** k
    p = f"What is $\\log_{{10}}\\frac{{2}}{{1}} + \\log_{{10}}\\frac{{3}}{{2}} + \\cdots + \\log_{{10}}\\frac{{{big(N)}}}{{{big(N - 1)}}}$?"
    return Q(p, k, [k + 1, N, k - 1 if k > 1 else 7, F(k, 2), 2 * k], "Combine into one log.",
             "the sum.", "the product inside telescopes.", [f"$\\frac{{2}}{{1}} \\cdot \\frac{{3}}{{2}} \\cdots \\frac{{{big(N)}}}{{{big(N - 1)}}} = {big(N)}$.", f"$\\log_{{10}} {big(N)} = {k}$."], "summing the fractions.")


@reg(S, "basics")
def stel_prod2(r):
    n = r.randint(4, 60)
    v = F((n + 1) * (n + 2), 2)
    p = f"What is $\\frac{{3}}{{1}} \\cdot \\frac{{4}}{{2}} \\cdot \\frac{{5}}{{3}} \\cdots \\frac{{{n + 2}}}{{{n}}}$?"
    return Q(p, v, [F(n + 2, 1), F((n + 1) * (n + 2)), F(n + 2, 2), v + 1, F(n * (n + 1), 2)], "Numerators and denominators overlap.",
             "the product.", "everything cancels except two numerators and the first two denominators.", [f"$\\frac{{{n + 1} \\cdot {n + 2}}}{{1 \\cdot 2}} = {ft(v)}$."], "keeping only one leftover factor.")


@reg(S, "basics")
def stel_gap3(r):
    n = r.randint(3, 15)
    v = sum(F(1, k * (k + 3)) for k in range(1, n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{1}}{{k(k + 3)}}$?"
    return Q(p, v, [v * 3, sum(F(1, k) - F(1, k + 3) for k in range(1, n + 1)) if v * 3 != v else v + 1, v + F(1, 3), F(n, n + 3), F(11, 18)], "$\\frac{1}{k(k + 3)} = \\frac{1}{3}\\left(\\frac{1}{k} - \\frac{1}{k + 3}\\right)$.",
             "the sum.", "the gaps of 3 leave three surviving terms at each end.", [f"$\\frac{{1}}{{3}}\\left(1 + \\frac{{1}}{{2}} + \\frac{{1}}{{3}} - \\frac{{1}}{{{n + 1}}} - \\frac{{1}}{{{n + 2}}} - \\frac{{1}}{{{n + 3}}}\\right) = {ft(v)}$."], "forgetting the factor of $\\frac{1}{3}$.")


@reg(S, "basics")
def stel_k_fact(r):
    n = r.randint(3, 8)
    v = 1 - F(1, math.factorial(n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{k}}{{(k + 1)!}}$?"
    return Q(p, v, [F(1), 1 - F(1, math.factorial(n)), v + F(1, math.factorial(n + 1)) * 2, F(n, n + 1), F(1, 2)], "$\\frac{k}{(k + 1)!} = \\frac{1}{k!} - \\frac{1}{(k + 1)!}$.",
             "the sum.", "it telescopes.", [f"$\\frac{{1}}{{1!}} - \\frac{{1}}{{{n + 1}!}} = 1 - \\frac{{1}}{{{math.factorial(n + 1)}}} = {ft(v)}$."], "stopping at $\\frac{1}{n!}$.")


@reg(S, "basics")
def stel_cubes(r):
    n = r.randint(3, 30)
    v = (n * (n + 1) // 2) ** 2
    p = f"What is $1^3 + 2^3 + \\cdots + {n}^3$?"
    return Q(p, B(v) if v >= 1000 else v, [B(n * (n + 1) // 2) if n * (n + 1) // 2 >= 1000 else n * (n + 1) // 2, B(n * (n + 1) * (2 * n + 1) // 6) if n * (n + 1) * (2 * n + 1) // 6 >= 1000 else n * (n + 1) * (2 * n + 1) // 6, B(v + n) if v + n >= 1000 else v + n, B(n ** 4 // 4) if n ** 4 // 4 >= 1000 else n ** 4 // 4], "Sum of cubes is the square of a triangular number.",
             "the sum.", "$\\sum k^3 = \\left(\\frac{n(n + 1)}{2}\\right)^2$.", [f"$\\left(\\frac{{{n} \\cdot {n + 1}}}{{2}}\\right)^2 = {n * (n + 1) // 2}^2 = {big(v)}$."], "using the sum of squares.", ans_tex=big(v) if v >= 1000 else None) if n * (n + 1) * (2 * n + 1) // 6 != v else None


@reg(S, "basics")
def stel_alt_sq(r):
    n = r.randint(5, 60)
    v = n * (n + 1) // 2
    p = f"What is ${n}^2 - {n - 1}^2 + {n - 2}^2 - {n - 3}^2 + \\cdots {'+' if n % 2 else '-'} 1^2$?"
    return Q(p, v, [n * n, v + n, n, v * 2, v - 1], "Pair: $k^2 - (k - 1)^2 = 2k - 1$.",
             "the sum.", "each difference of consecutive squares is a sum: $k^2 - (k - 1)^2 = k + (k - 1)$.", [f"The total is $" + str(n) + " + " + str(n - 1) + " + \\cdots + 1 = " + str(v) + "$."], "subtracting instead of adding the pairs.")


@reg(S, "basics")
def stel_tri_recip(r):
    n = r.randint(3, 60)
    v = F(2 * n, n + 1)
    p = f"What is $\\frac{{1}}{{1}} + \\frac{{1}}{{1 + 2}} + \\frac{{1}}{{1 + 2 + 3}} + \\cdots + \\frac{{1}}{{1 + 2 + \\cdots + {n}}}$?"
    return Q(p, v, [F(n, n + 1), F(2 * n, n + 2), v + 1, F(2, 1), F(n + 1, n)], "$\\frac{1}{T_k} = \\frac{2}{k(k + 1)}$.",
             "the sum.", "$2\\left(\\frac{1}{k} - \\frac{1}{k + 1}\\right)$ telescopes.", [f"$2\\left(1 - \\frac{{1}}{{{n + 1}}}\\right) = {ft(v)}$."], "forgetting the factor of 2.")


@reg(S, "basics")
def stel_3k(r):
    n = r.randint(5, 60)
    v = F(n, 3 * n + 1)
    p = f"What is $\\frac{{1}}{{1 \\cdot 4}} + \\frac{{1}}{{4 \\cdot 7}} + \\cdots + \\frac{{1}}{{{3 * n - 2} \\cdot {3 * n + 1}}}$?"
    return Q(p, v, [F(3 * n, 3 * n + 1), F(n, 3 * n - 2), F(n, n + 1), v + F(1, 3), F(1, 3)], "Partial fractions with a factor $\\frac{1}{3}$.",
             "the sum.", "$\\frac{1}{(3k - 2)(3k + 1)} = \\frac{1}{3}\\left(\\frac{1}{3k - 2} - \\frac{1}{3k + 1}\\right)$.", [f"$\\frac{{1}}{{3}}\\left(1 - \\frac{{1}}{{{3 * n + 1}}}\\right) = {ft(v)}$."], "forgetting the factor of $\\frac{1}{3}$.")


@reg(S, "basics")
def stel_prod_sq(r):
    n = r.randint(3, 60)
    v = F(2 * (n + 1), n + 2)
    p = f"What is $\\left(1 + \\frac{{1}}{{1 \\cdot 3}}\\right)\\left(1 + \\frac{{1}}{{2 \\cdot 4}}\\right)\\cdots\\left(1 + \\frac{{1}}{{{n} \\cdot {n + 2}}}\\right)$?"
    return Q(p, v, [F(n + 1, n + 2), F(2 * n, n + 1), F(2), v + 1, F(n + 2, n + 1)], "$1 + \\frac{1}{k(k + 2)} = \\frac{(k + 1)^2}{k(k + 2)}$.",
             "the product.", "split into $\\frac{k + 1}{k} \\cdot \\frac{k + 1}{k + 2}$; each part telescopes.", [f"$\\frac{{{n + 1}}}{{1}} \\cdot \\frac{{2}}{{{n + 2}}} = {ft(v)}$."], "telescoping only one of the two parts.")


@reg(S, "basics")
def stel_kk1(r):
    n = r.randint(3, 30)
    v = n * (n + 1) * (n + 2) // 3
    p = f"What is $1 \\cdot 2 + 2 \\cdot 3 + 3 \\cdot 4 + \\cdots + {n} \\cdot {n + 1}$?"
    return Q(p, B(v) if v >= 1000 else v, [B(n * (n + 1) * (2 * n + 1) // 6) if n * (n + 1) * (2 * n + 1) // 6 >= 1000 else n * (n + 1) * (2 * n + 1) // 6, B(v + n) if v + n >= 1000 else v + n, B(n * (n + 1) * (n + 2) // 6) if v // 2 >= 1000 else n * (n + 1) * (n + 2) // 6, B(v * 2) if v * 2 >= 1000 else v * 2], "$k(k + 1) = \\frac{k(k + 1)(k + 2) - (k - 1)k(k + 1)}{3}$.",
             "the sum.", "the sum telescopes to $\\frac{n(n + 1)(n + 2)}{3}$.", [f"$\\frac{{{n} \\cdot {n + 1} \\cdot {n + 2}}}{{3}} = {big(v)}$."], "using the sum of squares only.", ans_tex=big(v) if v >= 1000 else None)


@reg(S, "basics")
def stel_k2m1(r):
    n = r.randint(3, 40)
    v = sum(F(1, k * k - 1) for k in range(2, n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=2}}^{{{n}}} \\frac{{1}}{{k^2 - 1}}$?"
    return Q(p, v, [F(3, 4), v * 2, v + F(1, n), F(n - 1, n + 1), F(1, 2)], "$\\frac{1}{k^2 - 1} = \\frac{1}{2}\\left(\\frac{1}{k - 1} - \\frac{1}{k + 1}\\right)$.",
             "the sum.", "gap of 2: two terms survive at each end.", [f"$\\frac{{1}}{{2}}\\left(1 + \\frac{{1}}{{2}} - \\frac{{1}}{{{n}}} - \\frac{{1}}{{{n + 1}}}\\right) = {ft(v)}$."], "forgetting the factor of $\\frac{1}{2}$.")


@reg(S, "basics")
def stel_binom(r):
    n = r.randint(3, 50)
    v = 2 * (1 - F(1, n))
    p = f"What is $\\dfrac{{1}}{{\\binom{{2}}{{2}}}} + \\dfrac{{1}}{{\\binom{{3}}{{2}}}} + \\cdots + \\dfrac{{1}}{{\\binom{{{n}}}{{2}}}}$?"
    return Q(p, v, [1 - F(1, n), F(2), v + 1, F(n - 1, n + 1), 2 * (1 - F(1, n + 1))], "$\\frac{1}{\\binom{k}{2}} = \\frac{2}{k(k - 1)}$.",
             "the sum.", "$2\\left(\\frac{1}{k - 1} - \\frac{1}{k}\\right)$ telescopes.", [f"$2\\left(1 - \\frac{{1}}{{{n}}}\\right) = {ft(v)}$."], "forgetting the factor of 2.")


@reg(S, "basics")
def stel_pow2(r):
    n = r.randint(5, 20)
    v = 2 ** (n + 1) - 1
    p = f"What is $1 + 2 + 4 + \\cdots + 2^{{{n}}}$?"
    return Q(p, B(v) if v >= 1000 else v, [B(2 ** (n + 1)) if 2 ** (n + 1) >= 1000 else 2 ** (n + 1), B(2 ** n - 1) if 2 ** n - 1 >= 1000 else 2 ** n - 1, B(2 ** n) if 2 ** n >= 1000 else 2 ** n, B(v + 2) if v + 2 >= 1000 else v + 2], "$2^k = 2^{k+1} - 2^k$.",
             "the sum.", "each term is a difference of consecutive powers, so the sum telescopes.", [f"$2^{{{n + 1}}} - 1 = {big(v)}$."], "forgetting the $-1$.", ans_tex=big(v) if v >= 1000 else None)


@reg(S, "basics")
def stel_k2k(r):
    n = r.randint(3, 15)
    v = (n - 1) * 2 ** (n + 1) + 2
    p = f"What is $1 \\cdot 2 + 2 \\cdot 2^2 + 3 \\cdot 2^3 + \\cdots + {n} \\cdot 2^{{{n}}}$?"
    return Q(p, B(v) if v >= 1000 else v, [B(n * 2 ** (n + 1)) if n * 2 ** (n + 1) >= 1000 else n * 2 ** (n + 1), B(v - 2) if v - 2 >= 1000 else v - 2, B((n - 1) * 2 ** n + 2) if (n - 1) * 2 ** n + 2 >= 1000 else (n - 1) * 2 ** n + 2, B(v + 2 ** n) if v + 2 ** n >= 1000 else v + 2 ** n], "Let $S$ be the sum; compute $2S - S$.",
             "the sum.", "$2S - S$ shifts the terms, leaving a geometric series.", [f"$S = {n} \\cdot 2^{{{n + 1}}} - (2 + 4 + \\cdots + 2^{{{n}}}) = {n * 2 ** (n + 1)} - {2 ** (n + 1) - 2} = {big(v)}$."], "forgetting the geometric part.", ans_tex=big(v) if v >= 1000 else None)


@reg(S, "basics")
def stel_odd(r):
    n = r.randint(5, 60)
    v = n * n
    p = f"What is $1 + 3 + 5 + \\cdots + {2 * n - 1}$?"
    return Q(p, v, [n * (n + 1), (2 * n - 1) * n // 2 if (2 * n - 1) * n // 2 != v else v + 1, v - 1, 2 * n * n, n * (n - 1)], "$2k - 1 = k^2 - (k - 1)^2$.",
             "the sum.", "the odd numbers are differences of consecutive squares, so the sum telescopes to $n^2$.", [f"There are ${n}$ terms: ${n}^2 = {v}$."], "miscounting the terms.")


@reg(S, "basics")
def stel_one_minus(r):
    n = r.randint(3, 100)
    v = F(1, n)
    p = f"What is $\\left(1 - \\frac{{1}}{{2}}\\right)\\left(1 - \\frac{{1}}{{3}}\\right)\\cdots\\left(1 - \\frac{{1}}{{{n}}}\\right)$?"
    return Q(p, v, [F(1, n - 1), F(n - 1, n), F(1, 2), F(1, n + 1), F(2, n)], "Rewrite each factor as a fraction.",
             "the product.", "$\\frac{1}{2} \\cdot \\frac{2}{3} \\cdots \\frac{n - 1}{n}$ telescopes.", [f"Everything cancels except $\\frac{{1}}{{{n}}}$."], "keeping an extra factor.")


@reg(S, "challenge")
def stelc_three(r):
    n = r.randint(3, 30)
    v = F(1, 4) - F(1, 2 * (n + 1) * (n + 2))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{1}}{{k(k + 1)(k + 2)}}$?"
    return Q(p, v, [F(1, 4), F(1, 2) - F(1, (n + 1) * (n + 2)), v * 2, F(n, (n + 1) * (n + 2)), v + F(1, 12)], "$\\frac{1}{k(k + 1)(k + 2)} = \\frac{1}{2}\\left(\\frac{1}{k(k + 1)} - \\frac{1}{(k + 1)(k + 2)}\\right)$.",
             "the sum.", "write it as a difference of consecutive terms.", [f"$\\frac{{1}}{{2}}\\left(\\frac{{1}}{{2}} - \\frac{{1}}{{{n + 1} \\cdot {n + 2}}}\\right) = {ft(v)}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "challenge")
def stelc_cubes_prod(r):
    n = r.randint(3, 20)
    v = math.prod(F(k ** 3 - 1, k ** 3 + 1) for k in range(2, n + 1))
    p = f"What is $\\dfrac{{2^3 - 1}}{{2^3 + 1}} \\cdot \\dfrac{{3^3 - 1}}{{3^3 + 1}} \\cdots \\dfrac{{{n}^3 - 1}}{{{n}^3 + 1}}$?"
    return Q(p, v, [F(2, 3), F(1, n), v + F(1, 10), F(n * n + n + 1, 3 * n * (n + 1)), F(2 * (n * n + n + 1), 3 * n * n)], "Factor $k^3 \\pm 1$.",
             "the product.", "$\\frac{k^3 - 1}{k^3 + 1} = \\frac{k - 1}{k + 1} \\cdot \\frac{k^2 + k + 1}{k^2 - k + 1}$; each part telescopes (note $k^2 - k + 1 = (k - 1)^2 + (k - 1) + 1$).",
             [f"First part: $\\frac{{1 \\cdot 2}}{{{n} \\cdot {n + 1}}}$. Second part: $\\frac{{{n * n + n + 1}}}{{3}}$.", f"Product: ${ft(v)}$."], "telescoping only one part.")


@reg(S, "challenge")
def stelc_arctan(r):
    n = r.randint(2, 30)
    v = F(n, n + 2)
    p = f"What is $\\tan\\left(\\displaystyle\\sum_{{k=1}}^{{{n}}} \\arctan\\frac{{1}}{{k^2 + k + 1}}\\right)$?"
    return Q(p, v, [F(n, n + 1), F(1, n + 1), F(n + 1), v + 1, F(n - 1, n + 1)], "$\\arctan\\frac{1}{k^2 + k + 1} = \\arctan(k + 1) - \\arctan k$.",
             "the value.", "the sum telescopes to $\\arctan(n + 1) - \\arctan 1$.", [f"$\\tan(\\arctan {n + 1} - \\arctan 1) = \\frac{{{n + 1} - 1}}{{1 + {n + 1}}} = {ft(v)}$."], "stopping at $\\arctan n$.")


@reg(S, "challenge")
def stelc_k4(r):
    n = r.randint(3, 20)
    v = sum(F(k, k ** 4 + 4) for k in range(1, n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{k}}{{k^4 + 4}}$?"
    return Q(p, v, [F(3, 8), v + F(1, 8), v * 2, F(1, 4), v - F(1, 20)], "$k^4 + 4 = (k^2 - 2k + 2)(k^2 + 2k + 2)$ (Sophie Germain).",
             "the sum.", "$\\frac{k}{k^4 + 4} = \\frac{1}{4}\\left(\\frac{1}{(k - 1)^2 + 1} - \\frac{1}{(k + 1)^2 + 1}\\right)$, a gap-2 telescope.",
             [f"$\\frac{{1}}{{4}}\\left(1 + \\frac{{1}}{{2}} - \\frac{{1}}{{{n * n + 1}}} - \\frac{{1}}{{{(n + 1) ** 2 + 1}}}\\right) = {ft(v)}$."], "keeping only one surviving term at each end.")


@reg(S, "challenge")
def stelc_sq_frac(r):
    n = r.randint(3, 40)
    v = 1 - F(1, (n + 1) ** 2)
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{2k + 1}}{{k^2(k + 1)^2}}$?"
    return Q(p, v, [1 - F(1, n * n), F(1), F(n, n + 1), v + F(1, (n + 1) ** 2) * 2, 1 - F(1, n + 1)], "$\\frac{2k + 1}{k^2(k + 1)^2} = \\frac{1}{k^2} - \\frac{1}{(k + 1)^2}$.",
             "the sum.", "the numerator is $(k + 1)^2 - k^2$.", [f"$1 - \\frac{{1}}{{{(n + 1) ** 2}}} = {ft(v)}$."], "using $\\frac{1}{n^2}$ as the leftover.")


@reg(S, "challenge")
def stelc_fact2(r):
    n = r.randint(2, 7)
    v = sum(F(k * k + k - 1, math.factorial(k + 2)) for k in range(1, n + 1))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\frac{{k^2 + k - 1}}{{(k + 2)!}}$?"
    return Q(p, v, [F(1, 2), v + F(1, math.factorial(n + 2)), F(1, 2) - F(1, math.factorial(n + 2)), v * 2, F(n, n + 2)], "Write it as $\\frac{k}{(k + 1)!} - \\frac{k + 1}{(k + 2)!}$.",
             "the sum.", "check: $\\frac{k}{(k + 1)!} - \\frac{k + 1}{(k + 2)!} = \\frac{k(k + 2) - (k + 1)}{(k + 2)!}$.", [f"Telescoping: $\\frac{{1}}{{2!}} - \\frac{{{n + 1}}}{{{n + 2}!}} = {ft(v)}$."], "forgetting the leftover term.")


@reg(S, "challenge")
def stelc_fib(r):
    n = r.randint(4, 15)
    f = [0, 1, 1]
    while len(f) < n + 3:
        f.append(f[-1] + f[-2])
    v = 2 - F(1, f[n]) - F(1, f[n + 1])
    p = f"With $F_1 = F_2 = 1$ and $F_k = F_{{k-1}} + F_{{k-2}}$, what is $\\displaystyle\\sum_{{k=2}}^{{{n}}} \\frac{{F_k}}{{F_{{k-1}}F_{{k+1}}}}$?"
    return Q(p, v, [2 - F(1, f[n + 1]), F(2), 1 - F(1, f[n + 1]), v + F(1, f[n]), F(f[n], f[n + 1])], "$\\frac{F_k}{F_{k-1}F_{k+1}} = \\frac{1}{F_{k-1}} - \\frac{1}{F_{k+1}}$.",
             "the sum.", "since $F_{k+1} - F_{k-1} = F_k$, each term splits into a difference with gap 2.",
             [f"Survivors: $\\frac{{1}}{{F_1}} + \\frac{{1}}{{F_2}} - \\frac{{1}}{{F_{{{n}}}}} - \\frac{{1}}{{F_{{{n + 1}}}}} = 2 - \\frac{{1}}{{{f[n]}}} - \\frac{{1}}{{{f[n + 1]}}} = {ft(v)}$."], "keeping only one term at each end.")


# ================================================================ ser_geometric
S = "ser_geometric"


@reg(S, "basics")
def sgeo_ratio(r):
    a = r.randint(1, 20)
    q = F(r.randint(1, 4), r.randint(5, 6))
    Sum = a / (1 - q)
    p = f"An infinite geometric series has first term ${a}$ and sum ${ft(Sum)}$. What is the common ratio?"
    return Q(p, q, [1 - q, a / Sum, q * 2 if q * 2 < 1 else q / 2, F(1, 2) if q != F(1, 2) else F(1, 3), Sum / a if Sum / a != q else q + F(1, 10)], "$S = \\frac{a}{1 - r}$.",
             "$r$.", "solve for $r$.", [f"$1 - r = \\frac{{{a}}}{{{ft(Sum)}}} = {ft(a / Sum)}$.", f"$r = {ft(q)}$."], "giving $1 - r$.")


@reg(S, "basics")
def sgeo_neg(r):
    a = r.randint(1, 20)
    q = -F(1, r.randint(2, 6))
    v = a / (1 - q)
    p = f"What is ${a} {'-' if q < 0 else '+'} {ft(a * abs(q))} + {ft(a * q * q)} - {ft(a * abs(q ** 3))} + \\cdots$?"
    return Q(p, v, [a / (1 + q), a / (1 - abs(q)) if a / (1 - abs(q)) != v else v + 1, v + 1, F(a), F(a, 2)], "Ratio is negative.",
             "the sum.", f"$r = {ft(q)}$; $S = \\frac{{a}}{{1 - r}}$.", [f"$\\frac{{{a}}}{{1 + {ft(abs(q))}}} = {ft(v)}$."], "ignoring the negative ratio.")


@reg(S, "basics")
def sgeo_finite(r):
    a, q, n = r.randint(1, 5), r.choice([2, 3]), r.randint(4, 10)
    v = a * (q ** n - 1) // (q - 1)
    p = f"What is the sum of the first ${n}$ terms of ${a}, {a * q}, {a * q * q}, \\ldots$?"
    return Q(p, B(v) if v >= 1000 else v, [B(a * q ** n) if a * q ** n >= 1000 else a * q ** n, B(a * (q ** (n + 1) - 1) // (q - 1)) if a * (q ** (n + 1) - 1) // (q - 1) >= 1000 else a * (q ** (n + 1) - 1) // (q - 1), B(v - a) if v - a >= 1000 else v - a, B(a * q ** (n - 1)) if a * q ** (n - 1) >= 1000 else a * q ** (n - 1)], "$S_n = a\\frac{r^n - 1}{r - 1}$.",
             "the sum.", "finite geometric series formula.", [f"${a} \\cdot \\frac{{{q}^{{{n}}} - 1}}{{{q - 1}}} = {big(v)}$."], "using $n + 1$ terms.", ans_tex=big(v) if v >= 1000 else None)


@reg(S, "basics")
def sgeo_squares(r):
    a = r.randint(1, 9)
    q = F(r.randint(1, 3), r.randint(4, 5))
    v = a * a / (1 - q * q)
    p = f"An infinite geometric series has first term ${a}$ and ratio ${ft(q)}$. What is the sum of the squares of its terms?"
    return Q(p, v, [(a / (1 - q)) ** 2, a * a / (1 - q), v + 1, a / (1 - q * q), v * 2], "The squares form a geometric series with ratio $r^2$.",
             "the sum.", f"first term ${a * a}$, ratio ${ft(q * q)}$.", [f"$\\frac{{{a * a}}}{{1 - {ft(q * q)}}} = {ft(v)}$."], "squaring the original sum.")


@reg(S, "basics")
def sgeo_mixed_dec(r):
    a = r.randint(1, 9)
    b = r.randint(1, 9)
    if a == b:
        return None
    v = F(a, 10) + F(b, 90)
    p = f"What is $0.{a}\\overline{{{b}}}$ as a fraction in lowest terms?"
    return Q(p, v, [F(10 * a + b, 99), F(10 * a + b, 90) if F(10 * a + b, 90) != v else v + F(1, 90), F(a, 10) + F(b, 9), F(10 * a + b, 100), v + F(1, 10)], "Separate the non-repeating part.",
             "the fraction.", f"$0.{a}\\overline{{{b}}} = \\frac{{{a}}}{{10}} + \\frac{{{b}}}{{90}}$.", [f"$\\frac{{{9 * a} + {b}}}{{90}} = {ft(v)}$."], "treating both digits as repeating.")


@reg(S, "basics")
def sgeo_term_index(r):
    a, q = r.randint(1, 5), r.choice([2, 3])
    n = r.randint(4, 12)
    t = a * q ** (n - 1)
    p = f"In the geometric sequence ${a}, {a * q}, {a * q * q}, \\ldots$, which term equals ${big(t)}$?"
    return Q(p, n, [n - 1, n + 1, n * q if n * q != n else n + 2, F(t, a * q) if F(t, a * q) < 100 and F(t, a * q) != n else n + 3, n + 2], "Solve $" + str(a) + " \\cdot " + str(q) + "^{n-1} = " + big(t) + "$.",
             "$n$.", "divide by the first term, then find the power.", [f"${q}^{{n - 1}} = {big(t // a)}$, so $n - 1 = {n - 1}$, $n = {n}$."], "forgetting to add 1.")


@reg(S, "basics")
def sgeo_insert(r):
    a, q = r.randint(1, 5), r.choice([2, 3, 4])
    b = a * q ** 3
    p = f"Two numbers are inserted between ${a}$ and ${b}$ so that the four numbers form a geometric sequence. What is the smaller inserted number?"
    return Q(p, a * q, [a * q * q, F(a + b, 3), a * 2 if a * 2 != a * q else a * q + 1, q, a * q + q], "The ratio cubed is " + str(q ** 3) + ".",
             "the smaller inserted number.", "four terms span three ratio steps.", [f"$r^3 = \\frac{{{b}}}{{{a}}} = {q ** 3}$, so $r = {q}$.", f"Inserted: ${a * q}$ and ${a * q * q}$."], "using an arithmetic sequence.")


@reg(S, "basics")
def sgeo_solve_x(r):
    Sm = F(r.randint(2, 9), r.randint(1, 3))
    if Sm <= 1:
        return None
    v = 1 - 1 / Sm
    p = f"For what $x$ does $1 + x + x^2 + x^3 + \\cdots = {ft(Sm)}$?"
    return Q(p, v, [1 / Sm, 1 - Sm if 1 - Sm != v else v + 1, v / 2, Sm - 1 if Sm - 1 != v else v * 2, F(1, 2) if v != F(1, 2) else F(1, 3)], "$\\frac{1}{1 - x} = " + ft(Sm) + "$.",
             "$x$.", "solve the sum formula for $x$.", [f"$1 - x = {ft(1 / Sm)}$, $x = {ft(v)}$."], "answering $\\frac{1}{S}$.")


@reg(S, "basics")
def sgeo_from_second(r):
    a = r.randint(2, 20)
    q = F(r.randint(1, 3), r.randint(4, 6))
    v = a * q / (1 - q)
    p = f"What is ${ft(a * q)} + {ft(a * q * q)} + {ft(a * q ** 3)} + \\cdots$?"
    return Q(p, v, [a / (1 - q), v + 1, a * q, v * 2, a * q / (1 + q)], "First term " + ft(a * q) + ".",
             "the sum.", f"ratio ${ft(q)}$.", [f"$\\frac{{{ft(a * q)}}}{{1 - {ft(q)}}} = {ft(v)}$."], "using the wrong first term.")


@reg(S, "basics")
def sgeo_nested_squares(r):
    s = r.randint(2, 12)
    A = s * s
    v = 2 * A
    p = f"A square has side ${s}$. A second square is formed by joining the midpoints of its sides, a third by joining the midpoints of the second, and so on forever. What is the total area of all the squares?"
    return Q(p, v, [A, F(4 * A, 3), 4 * A, F(3 * A, 2), A + A // 2], "Each square has half the area of the one before.",
             "the total area.", f"areas ${A}, {ft(F(A, 2))}, {ft(F(A, 4))}, \\ldots$ with ratio $\\frac{{1}}{{2}}$.", [f"$\\frac{{{A}}}{{1 - \\frac{{1}}{{2}}}} = {v}$."], "using ratio $\\frac{1}{4}$.")


@reg(S, "basics")
def sgeo_even_terms(r):
    a = r.randint(1, 20)
    q = F(r.randint(1, 3), r.randint(4, 5))
    v = a * q / (1 - q * q)
    p = f"In the series ${a} + {ft(a * q)} + {ft(a * q * q)} + \\cdots$, what is the sum of the 2nd, 4th, 6th, ... terms?"
    return Q(p, v, [a / (1 - q * q), a * q / (1 - q), v + 1, a / (1 - q) / 2, v * 2], "These terms form a geometric series with ratio $r^2$.",
             "the sum.", f"first term ${ft(a * q)}$, ratio ${ft(q * q)}$.", [f"$\\frac{{{ft(a * q)}}}{{1 - {ft(q * q)}}} = {ft(v)}$."], "using ratio $r$.")


@reg(S, "basics")
def sgeo_alt_base(r):
    b = r.randint(2, 9)
    v = F(b, b + 1)
    p = f"What is $1 - \\frac{{1}}{{{b}}} + \\frac{{1}}{{{b * b}}} - \\frac{{1}}{{{b ** 3}}} + \\cdots$?"
    return Q(p, v, [F(b, b - 1), F(1, b + 1), v + F(1, b), F(b - 1, b), F(1, 2) if v != F(1, 2) else F(2, 3)], "Ratio $-\\frac{1}{" + str(b) + "}$.",
             "the sum.", "$\\frac{1}{1 - r}$ with negative $r$.", [f"$\\frac{{1}}{{1 + \\frac{{1}}{{{b}}}}} = {ft(v)}$."], "ignoring the alternating signs.")


@reg(S, "basics")
def sgeo_base_rep(r):
    b = r.randint(3, 12)
    d = r.randint(1, b - 1)
    v = F(d, b - 1)
    p = f"In base ${b}$, what is the value of $0.\\overline{{{d}}}_{{{b}}}$ as a fraction?"
    return Q(p, v, [F(d, b), F(d, 9) if F(d, 9) != v else v + F(1, b), F(d, b + 1), F(1, b - 1) if d != 1 else F(2, b - 1), v * 2 if v * 2 < 1 else v / 2], "$\\frac{d}{b} + \\frac{d}{b^2} + \\cdots$.",
             "the value.", "a geometric series with ratio $\\frac{1}{b}$.", [f"$\\frac{{{d}/{b}}}{{1 - 1/{b}}} = \\frac{{{d}}}{{{b - 1}}} = {ft(v)}$."], "using 9 as in base 10.")


@reg(S, "basics")
def sgeo_two_terms(r):
    a = F(r.randint(1, 30))
    q = F(1, r.choice([2, 3]))
    t2, t4 = a * q, a * q ** 3
    v = a / (1 - q)
    p = f"An infinite geometric series with positive terms has second term ${ft(t2)}$ and fourth term ${ft(t4)}$. What is its sum?"
    return Q(p, v, [t2 / (1 - q), a, v + 1, v * 2, t2 / (1 - q * q)], "$r^2 = \\frac{a_4}{a_2}$.",
             "the sum.", "find $r$, then the first term.", [f"$r^2 = {ft(q * q)}$, $r = {ft(q)}$; $a = {ft(a)}$.", f"Sum: ${ft(v)}$."], "using $a_2$ as the first term.")


@reg(S, "basics")
def sgeo_double(r):
    a, b = r.sample(range(2, 8), 2)
    v = F(a, a - 1) + F(b, b - 1)
    p = f"What is $\\displaystyle\\sum_{{k=0}}^{{\\infty}} \\left(\\frac{{1}}{{{a}^k}} + \\frac{{1}}{{{b}^k}}\\right)$?"
    return Q(p, v, [F(1, a - 1) + F(1, b - 1), F(a * b, (a - 1) * (b - 1)), v + 1, F(a + b, a + b - 1), v - F(1, 2)], "Split into two geometric series.",
             "the sum.", "each starts at $1$ (the $k = 0$ term).", [f"$\\frac{{1}}{{1 - 1/{a}}} + \\frac{{1}}{{1 - 1/{b}}} = {ft(F(a, a - 1))} + {ft(F(b, b - 1))} = {ft(v)}$."], "starting at $k = 1$.")


@reg(S, "basics")
def sgeo_tri_perim(r):
    P = r.randint(6, 60)
    p = f"A triangle has perimeter ${P}$. Joining the midpoints of its sides forms a smaller triangle; repeat forever. What is the total of all the perimeters?"
    return Q(p, 2 * P, [P, F(4 * P, 3), 4 * P, F(3 * P, 2), 3 * P], "Each new perimeter is half the last.",
             "the total.", "ratio $\\frac{1}{2}$ (the midsegment triangle has half the side lengths).", [f"$\\frac{{{P}}}{{1 - \\frac{{1}}{{2}}}} = {2 * P}$."], "using ratio $\\frac{1}{4}$ (that's for areas).")


@reg(S, "challenge")
def sgeoc_k2(r):
    x = F(1, r.choice([2, 3, 4, 5]))
    v = x * (1 + x) / (1 - x) ** 3
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{\\infty}} k^2 \\left({ft(x)}\\right)^k$?"
    return Q(p, v, [x / (1 - x) ** 2, x * (1 + x) / (1 - x) ** 2, v + 1, v / 2, x / (1 - x) ** 3], "$\\sum k^2 x^k = \\frac{x(1 + x)}{(1 - x)^3}$.",
             "the sum.", "differentiate the geometric series twice (or use the $S - xS$ trick twice).", [f"$\\frac{{{ft(x)} \\cdot {ft(1 + x)}}}{{{ft((1 - x) ** 3)}}} = {ft(v)}$."], "using the formula for $\\sum kx^k$.")


@reg(S, "challenge")
def sgeoc_grid(r):
    a, b = r.sample(range(2, 8), 2)
    v = F(1, (a - 1) * (b - 1))
    p = f"What is $\\displaystyle\\sum_{{i=1}}^{{\\infty}} \\sum_{{j=1}}^{{\\infty}} \\frac{{1}}{{{a}^i {b}^j}}$?"
    return Q(p, v, [F(1, a * b - 1), F(a * b, (a - 1) * (b - 1)), F(1, a - 1) + F(1, b - 1), v * 2, F(1, (a - 1) * b)], "The double sum factors.",
             "the sum.", "$\\left(\\sum \\frac{1}{" + str(a) + "^i}\\right)\\left(\\sum \\frac{1}{" + str(b) + "^j}\\right)$.", [f"$\\frac{{1}}{{{a - 1}}} \\cdot \\frac{{1}}{{{b - 1}}} = {ft(v)}$."], "adding instead of multiplying.")


@reg(S, "challenge")
def sgeoc_sum_sq(r):
    q = F(r.randint(1, 3), r.randint(4, 5))
    a = r.randint(1, 6)
    Sm = a / (1 - q)
    T = a * a / (1 - q * q)
    p = f"An infinite geometric series has sum ${ft(Sm)}$, and the series of the squares of its terms has sum ${ft(T)}$. What is the common ratio?"
    return Q(p, q, [1 - q, q * q, F(1, 2) if q != F(1, 2) else F(1, 3), T / Sm if T / Sm != q else q + F(1, 10), (Sm * Sm - T) / (Sm * Sm)], "$\\frac{T}{S^2} = \\frac{1 - r}{1 + r}$.",
             "$r$.", "divide $\\frac{a^2}{1 - r^2}$ by $\\left(\\frac{a}{1 - r}\\right)^2$.", [f"$\\frac{{1 - r}}{{1 + r}} = \\frac{{{ft(T)}}}{{{ft(Sm * Sm)}}} = {ft(T / (Sm * Sm))}$.", f"$r = {ft(q)}$."], "solving for $a$ first and making an algebra slip.")


@reg(S, "challenge")
def sgeoc_skip(r):
    b, m = r.choice([2, 3]), r.choice([2, 3, 4])
    v = F(1, b - 1) - F(1, b ** m - 1)
    p = f"What is the sum of $\\frac{{1}}{{{b}^k}}$ over all positive integers $k$ that are not multiples of ${m}$?"
    return Q(p, v, [F(1, b - 1), F(m - 1, m) * F(1, b - 1), F(1, b ** m - 1), v + F(1, 10), F(b ** m - b, b ** m - 1) if F(b ** m - b, b ** m - 1) != v else v * 2], "Total minus the multiples of " + str(m) + ".",
             "the sum.", f"the multiples of ${m}$ give a geometric series with ratio $\\frac{{1}}{{{b ** m}}}$.", [f"All $k$: $\\frac{{1}}{{{b - 1}}}$. Multiples of ${m}$: $\\frac{{1}}{{{b ** m - 1}}}$.", f"Difference: ${ft(v)}$."], "multiplying by $\\frac{" + str(m - 1) + "}{" + str(m) + "}$.")


@reg(S, "challenge")
def sgeoc_base2(r):
    b = r.randint(3, 12)
    d1, d2 = r.randint(1, b - 1), r.randint(0, b - 1)
    if d1 == d2:
        return None
    v = F(d1 * b + d2, b * b - 1)
    p = f"In base ${b}$, what is $0.\\overline{{{d1}{d2}}}_{{{b}}}$ as a fraction?"
    return Q(p, v, [F(d1 * b + d2, b * b), F(10 * d1 + d2, 99) if F(10 * d1 + d2, 99) != v else v + F(1, b), F(d1 * b + d2, b * b + 1), v * 2 if v * 2 < 1 else v / 2, F(d1 + d2, b - 1) if F(d1 + d2, b - 1) != v else v + F(1, b * b)], "Two-digit repeating block: denominator $b^2 - 1$.",
             "the value.", f"the block ${d1}{d2}_{{{b}}} = {d1 * b + d2}$ repeats every two places.", [f"$\\frac{{{d1 * b + d2}}}{{{b}^2 - 1}} = {ft(v)}$."], "using $99$ as in base 10.")


@reg(S, "challenge")
def sgeoc_arith_geo(r):
    a, d = r.randint(1, 5), r.randint(1, 4)
    q = F(1, r.choice([2, 3, 4]))
    v = a / (1 - q) + d * q / (1 - q) ** 2
    p = f"What is $\\displaystyle\\sum_{{k=0}}^{{\\infty}} ({a} + {d}k)\\left({ft(q)}\\right)^k$?"
    return Q(p, v, [a / (1 - q), v + d, d * q / (1 - q) ** 2, (a + d) / (1 - q), v * 2], "Split: $" + str(a) + "\\sum r^k + " + str(d) + "\\sum kr^k$.",
             "the sum.", "$\\sum r^k = \\frac{1}{1 - r}$ and $\\sum kr^k = \\frac{r}{(1 - r)^2}$.", [f"${a} \\cdot {ft(1 / (1 - q))} + {d} \\cdot {ft(q / (1 - q) ** 2)} = {ft(v)}$."], "forgetting the $k$-weighted part.")


@reg(S, "challenge")
def sgeoc_prod(r):
    x = F(1, r.choice([2, 3, 4, 5]))
    v = 1 / (1 - x)
    p = f"What is $\\displaystyle\\prod_{{k=0}}^{{\\infty}} \\left(1 + \\left({ft(x)}\\right)^{{2^k}}\\right)$?"
    return Q(p, v, [1 + x, 2 * (1 + x) if 2 * (1 + x) != v else v + 1, v + 1, 1 / (1 - x * x), v * v], "Multiply by $(1 - x)$ and watch it telescope.",
             "the product.", "$(1 - x)(1 + x)(1 + x^2)(1 + x^4)\\cdots = 1$, since each factor pairs to give $1 - x^{2^{k+1}}$.", [f"Product $= \\frac{{1}}{{1 - {ft(x)}}} = {ft(v)}$."], "multiplying only the first few terms.")
