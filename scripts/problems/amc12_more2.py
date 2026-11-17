"""Extra AMC 12 problem types (part 2): logarithms and complex numbers."""
import cmath
import math
from fractions import Fraction as F

from algebra_more2 import rad
from amc12_more1 import PI, deg_rad, ex, exw, DG, cosd, sind
from common import NAMES, C, Q, comb, num, par, sg

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ft(v):
    return num(F(v)).tex


def big(v):
    return f"{v:,}".replace(",", "{,}")


# ================================================================ log_rules
S = "log_rules"


@reg(S, "basics")
def lr_power_eval(r):
    b = r.choice([2, 3, 4, 5, 6, 7])
    k = r.randint(2, 6 if b < 4 else 4)
    p = f"What is $\\log_{{{b}}} {b ** k}$?"
    return Q(p, k, [k + 1, k - 1, b * k if b * k != k else k + 2, F(b ** k, b), F(k, b) if F(k, b) != k else 2 * k], "Ask: " + str(b) + " to what power is " + str(b ** k) + "?",
             "the logarithm.", "$\\log_b b^k = k$.", [f"${b ** k} = {b}^{{{k}}}$.", f"So the log is ${k}$."], "dividing " + str(b ** k) + " by " + str(b) + ".")


@reg(S, "basics")
def lr_reciprocal(r):
    b = r.choice([2, 3, 4, 5, 10])
    k = r.randint(1, 4)
    p = f"What is $\\log_{{{b}}} \\frac{{1}}{{{b ** k}}}$?"
    return Q(p, -k, [k, F(-1, k), F(1, k), -k - 1, 0], "$\\frac{1}{b^k} = b^{-k}$.",
             "the logarithm.", "a reciprocal flips the sign of the exponent.", [f"$\\frac{{1}}{{{b ** k}}} = {b}^{{-{k}}}$, so the log is $-{k}$."], "dropping the negative sign.")


@reg(S, "basics")
def lr_root(r):
    b = r.choice([2, 3, 5, 7])
    m, n = r.randint(1, 5), r.randint(2, 5)
    if math.gcd(m, n) != 1:
        return None
    v = F(m, n)
    p = f"What is $\\log_{{{b}}} " + (f"\\sqrt{{{b}^{{{m}}}}}" if n == 2 else f"\\sqrt[{n}]{{{b}^{{{m}}}}}") + "$?"
    return Q(p, v, [F(n, m), m * n, F(m, n + 1), v + 1, F(1, n)], "Write the root as a fractional power.",
             "the logarithm.", "$\\sqrt[n]{b^m} = b^{m/n}$.", [f"$\\log_{{{b}}} {b}^{{{m}/{n}}} = {ft(v)}$."], "flipping the fraction.")


@reg(S, "basics")
def lr_sum(r):
    b = r.choice([6, 10, 12, 15, 20])
    k = r.randint(1, 3)
    N = b ** k
    divs = [d for d in range(2, N) if N % d == 0 and d * d != N]
    x = r.choice(divs)
    y = N // x
    p = f"What is $\\log_{{{b}}} {x} + \\log_{{{b}}} {y}$?"
    return Q(p, k, [k + 1, F(x + y, b) if F(x + y, b) != k else k + 2, k * 2, k - 1 if k > 1 else 3, F(k, 2)], "Combine into one log.",
             "the sum.", "$\\log_b x + \\log_b y = \\log_b(xy)$.", [f"${x} \\cdot {y} = {N} = {b}^{{{k}}}$.", f"So the sum is ${k}$."], "adding " + str(x) + " and " + str(y) + " inside the log.")


@reg(S, "basics")
def lr_diff(r):
    b = r.choice([2, 3, 5])
    k = r.randint(2, 5)
    y = r.choice([2, 3, 5, 6, 7])
    if y == b:
        return None
    x = y * b ** k
    p = f"What is $\\log_{{{b}}} {x} - \\log_{{{b}}} {y}$?"
    return Q(p, k, [k + 1, k - 1, F(x - y, b) if F(x - y, b) != k else k + 2, F(k, 2), 2 * k], "Combine into one log.",
             "the difference.", "$\\log_b x - \\log_b y = \\log_b \\frac{x}{y}$.", [f"$\\frac{{{x}}}{{{y}}} = {b ** k} = {b}^{{{k}}}$.", f"So the answer is ${k}$."], "subtracting inside the log.")


@reg(S, "basics")
def lr_power_rule(r):
    b = 2
    a1, e1, a2, e2 = r.choice([4, 8, 16]), r.randint(2, 4), r.choice([2, 4, 8, 32]), r.randint(1, 3)
    v = e1 * int(math.log2(a1)) - e2 * int(math.log2(a2))
    p = f"What is ${e1}\\log_2 {a1} - {e2 if e2 > 1 else ''}\\log_2 {a2}$?"
    return Q(p, v, [v + 1, v - 1, e1 * int(math.log2(a1)) + e2 * int(math.log2(a2)), e1 - e2, -v if v else 2], "Evaluate each log, then multiply.",
             "the value.", "$k\\log_b x = \\log_b x^k$.", [f"$\\log_2 {a1} = {int(math.log2(a1))}$, $\\log_2 {a2} = {int(math.log2(a2))}$.", f"${e1} \\cdot {int(math.log2(a1))} - {e2} \\cdot {int(math.log2(a2))} = {v}$."], "applying the coefficient to the wrong log.")


@reg(S, "basics")
def lr_base_power(r):
    b = r.choice([2, 3, 5])
    m = r.choice([1, 2, 3])
    x = r.choice([v for v in range(2, 10) if v != b])
    p = f"What is ${b ** m}^{{\\log_{{{b}}} {x}}}$?"
    return Q(p, x ** m, [x, m * x, x ** m + 1, b ** m * x, x * x if x * x != x ** m else x ** 3], "Write " + str(b ** m) + " as a power of " + str(b) + ".",
             "the value.", "$b^{\\log_b x} = x$.", [f"${b ** m}^{{\\log_{{{b}}} {x}}} = \\left({b}^{{\\log_{{{b}}} {x}}}\\right)^{{{m}}} = {x}^{{{m}}} = {x ** m}$."], "answering " + str(x) + ".") if m > 1 else None


@reg(S, "basics")
def lr_tower_base(r):
    b = r.choice([2, 3])
    m, n = r.randint(2, 4), r.randint(1, 7)
    v = F(n, m)
    p = f"What is $\\log_{{{b ** m}}} {b ** n}$?"
    return Q(p, v, [F(m, n), F(n, 1), n * m, v + 1, F(n, m + 1)], "Write both as powers of " + str(b) + ".",
             "the logarithm.", f"$\\log_{{{b}^{m}}} {b}^{n} = \\frac{{{n}}}{{{m}}}$.", [f"${b ** m} = {b}^{{{m}}}$ and ${b ** n} = {b}^{{{n}}}$.", f"$({b}^{{{m}}})^x = {b}^{{{n}}}$ gives $x = {ft(v)}$."], "flipping the fraction.") if v.denominator != 1 else None


@reg(S, "basics")
def lr_product_powers(r):
    n = r.randint(3, 12)
    ans = n * (n + 1) // 2
    p = f"What is $\\log_2 (2 \\cdot 4 \\cdot 8 \\cdots 2^{{{n}}})$?"
    return Q(p, ans, [n, 2 ** n, n * n, ans + n, ans - 1], "The log of a product is the sum of the logs.",
             "the log.", "add the exponents $1 + 2 + \\cdots + " + str(n) + "$.", [f"$\\frac{{{n} \\cdot {n + 1}}}{{2}} = {ans}$."], "multiplying the exponents.")


@reg(S, "basics")
def lr_ten(r):
    x, y = r.choice([(4, 25), (2, 50), (5, 20), (8, 125), (16, 625), (40, 25), (25, 40)])
    v = round(math.log10(x * y))
    p = f"What is $\\log_{{10}} {x} + \\log_{{10}} {y}$?"
    return Q(p, v, [v + 1, v - 1, F(x + y, 10) if F(x + y, 10) != v else v + 2, F(v, 2), 2 * v], "Combine the logs.",
             "the sum.", "$\\log x + \\log y = \\log(xy)$.", [f"${x} \\cdot {y} = {x * y} = 10^{{{v}}}$."], "adding the numbers.")


@reg(S, "basics")
def lr_fraction_base(r):
    b = r.choice([2, 3, 5])
    k = r.randint(2, 5)
    sgn = r.choice([1, -1])
    x = F(b ** k) if sgn > 0 else F(1, b ** k)
    v = -k if sgn > 0 else k
    p = f"What is $\\log_{{\\frac{{1}}{{{b}}}}} {ft(x)}$?"
    return Q(p, v, [-v, F(1, k), F(-1, k), v + 1, v - 1], "$\\frac{1}{" + str(b) + "} = " + str(b) + "^{-1}$.",
             "the logarithm.", "changing the base to its reciprocal flips the sign.", [f"$\\left(\\frac{{1}}{{{b}}}\\right)^{{{v}}} = {ft(x)}$."], "ignoring the sign change.")


@reg(S, "basics")
def lr_decimal(r):
    k = r.randint(1, 6)
    s = "0." + "0" * (k - 1) + "1"
    p = f"What is $\\log_{{10}} {s}$?"
    return Q(p, -k, [k, -k + 1, -k - 1, F(-1, k), F(1, k)], "Count the decimal places.",
             "the logarithm.", f"${s} = 10^{{-{k}}}$.", [f"$\\log_{{10}} 10^{{-{k}}} = -{k}$."], "counting the zeros instead of the decimal places.")


@reg(S, "basics")
def lr_nested(r):
    b, c = r.choice([(2, 3), (2, 2), (3, 2), (2, 5), (3, 3)])
    k = r.randint(1, 3 if c > 2 else 4)
    inner = c ** (b ** k)
    if inner > 10 ** 6:
        return None
    p = f"What is $\\log_{{{b}}}\\left(\\log_{{{c}}} {big(inner)}\\right)$?"
    return Q(p, k, [b ** k, k + 1, k - 1 if k > 1 else 5, c * k if c * k != k else k + 3, inner // c if inner // c < 1000 and inner // c not in (k,) else k + 4], "Work from the inside out.",
             "the value.", "evaluate the inner log first.", [f"$\\log_{{{c}}} {big(inner)} = {b ** k}$.", f"$\\log_{{{b}}} {b ** k} = {k}$."], "evaluating the outer log first.")


@reg(S, "basics")
def lr_ln(r):
    m, n = r.randint(1, 6), r.randint(1, 4)
    v = F(m, n)
    form = f"\\sqrt[{n}]{{e^{{{m}}}}}" if n > 1 else f"e^{{{m}}}"
    if n == 2:
        form = f"\\sqrt{{e^{{{m}}}}}"
    p = f"What is $\\ln {form}$?"
    return Q(p, v, [F(n, m), m * n, v + 1, F(1, n) if F(1, n) != v else v + 2, math.e if False else F(m, n + 1)], "$\\ln$ is $\\log_e$.",
             "the value.", "$\\ln e^x = x$.", [f"${form} = e^{{{ft(v)}}}$.", f"$\\ln$ of it: ${ft(v)}$."], "flipping the fraction.") if not (m == 1 and n == 1) else None


@reg(S, "basics")
def lr_compare(r):
    b = r.choice([2, 3])
    x = r.randint(2, 6)
    k = r.randint(2, 4)
    v = k * x
    p = f"If $\\log_{{{b}}} N = {x}$, what is $\\log_{{{b}}} N^{{{k}}}$?"
    return Q(p, v, [x ** k, x + k, F(x, k), v + 1, b ** x], "Power rule.",
             "$\\log_b N^k$.", "$\\log_b N^k = k \\log_b N$.", [f"${k} \\cdot {x} = {v}$."], "raising the log to the power.")


@reg(S, "basics")
def lr_log_sqrt_mult(r):
    b = r.choice([2, 3, 5])
    j, k = r.randint(1, 4), r.randint(1, 5)
    v = j + F(k, 2)
    p = f"What is $\\log_{{{b}}}\\left({b ** j}\\sqrt{{{b ** k}}}\\right)$?"
    return Q(p, v, [j + k, F(j + k, 2), v + F(1, 2), j * F(k, 2) if j * F(k, 2) != v else v + 1, v - 1], "Split the product.",
             "the value.", "$\\log(xy) = \\log x + \\log y$ and $\\sqrt{x} = x^{1/2}$.", [f"$\\log_{{{b}}} {b ** j} = {j}$; $\\log_{{{b}}} \\sqrt{{{b ** k}}} = {ft(F(k, 2))}$.", f"Total: ${ft(v)}$."], "forgetting the square root halves the exponent.")


@reg(S, "challenge")
def lrc_divisors(r):
    n = r.randint(1, 5)
    v = F(n * (n + 1) ** 2, 2)
    p = f"What is the sum of $\\log_{{10}} d$ over all positive divisors $d$ of $10^{{{n}}}$?"
    return Q(p, v, [F((n + 1) ** 2, 1), F(n * (n + 1), 2), v * 2, v + n, F(n * (n + 1) ** 2, 4)], "Pair each divisor $d$ with $\\frac{10^n}{d}$.",
             "the sum.", "the sum of logs is the log of the product of all divisors.",
             [f"$10^{{{n}}} = 2^{{{n}}}5^{{{n}}}$ has $({n + 1})^2 = {(n + 1) ** 2}$ divisors.", f"Their product is $(10^{{{n}}})^{{{(n + 1) ** 2}/2}}$.", f"Log: ${n} \\cdot \\frac{{{(n + 1) ** 2}}}{{2}} = {ft(v)}$."], "forgetting the divisors pair up.")


@reg(S, "challenge")
def lrc_combo(r):
    t = r.randint(2, 5)
    a, b, c, d = r.randint(1, 3), r.randint(1, 4), r.randint(1, 3), r.randint(0, 3)
    v = F(a + b * t, c + d * t)
    p = f"If $\\log_x y = {t}$, what is $\\log_{{x^{{{c}}}y^{{{d}}}}}\\left(x^{{{a}}} y^{{{b}}}\\right)$?".replace("y^{0}", "").replace("x^{1}", "x").replace("y^{1}", "y")
    return Q(p, v, [F(a + b, c + d) if c + d and F(a + b, c + d) != v else v + 1, F(a * b * t, c + d * t), F(c + d * t, a + b * t) if v != 1 else F(2), v + 1, F(a + b * t, c)], "Write everything in base $x$.",
             "the value.", "$\\log_x y = " + str(t) + "$ means $y = x^{" + str(t) + "}$.",
             [f"The argument is $x^{{{a} + {b} \\cdot {t}}} = x^{{{a + b * t}}}$; the base is $x^{{{c + d * t}}}$.", f"Ratio: $\\frac{{{a + b * t}}}{{{c + d * t}}} = {ft(v)}$."], "adding exponents without substituting.")


@reg(S, "challenge")
def lrc_floor_sum(r):
    N = r.randint(10, 100)
    ans = sum(int(math.log2(k)) if 2 ** int(math.log2(k)) <= k else int(math.log2(k)) - 1 for k in range(1, N + 1))
    ans = sum(k.bit_length() - 1 for k in range(1, N + 1))
    p = f"What is $\\lfloor \\log_2 1 \\rfloor + \\lfloor \\log_2 2 \\rfloor + \\lfloor \\log_2 3 \\rfloor + \\cdots + \\lfloor \\log_2 {N} \\rfloor$?"
    return Q(p, ans, [ans + 1, ans - 1, ans + N.bit_length(), N * (N.bit_length() - 1), ans + 2], "Group the numbers by the value of the floor.",
             "the sum.", "$\\lfloor \\log_2 k \\rfloor = j$ for $2^j \\le k < 2^{j+1}$: that's $2^j$ numbers (fewer for the last group).",
             ["Groups: " + ", ".join(f"$j = {j}$: ${min(N, 2 ** (j + 1) - 1) - 2 ** j + 1}$ numbers" for j in range(N.bit_length())) + ".", f"Weighted sum: ${ans}$."], "making the last group full size.")


@reg(S, "challenge")
def lrc_chain(r):
    m = r.randint(3, 7)
    n = 2 ** m - 1
    p = f"What is $\\log_2 3 \\cdot \\log_3 4 \\cdot \\log_4 5 \\cdots \\log_{{{n}}} {n + 1}$?"
    return Q(p, m, [m + 1, n - 1, F(n + 1, 2), m - 1, 2 * m], "Change of base telescopes.",
             "the product.", "$\\log_a b \\cdot \\log_b c = \\log_a c$.", [f"The product collapses to $\\log_2 {n + 1} = {m}$."], "multiplying approximate values.")


@reg(S, "challenge")
def lrc_reciprocals(r):
    bs = r.choice([(2, 3, 5), (2, 3), (3, 4), (2, 5), (2, 3, 7)])
    P = math.prod(bs)
    k = r.randint(2, 4)
    N = P ** k
    v = F(1, k)
    p = f"What is " + " + ".join(f"\\dfrac{{1}}{{\\log_{{{b}}} {big(N)}}}" for b in bs).join(["$", "$"]) + "?"
    return Q(p, v, [F(k), F(len(bs), k), F(1, k + 1), F(1, P), v * 2], "$\\frac{1}{\\log_b N} = \\log_N b$.",
             "the sum.", "flip each log, then add.", [f"Sum $= \\log_{{{big(N)}}}({' \\cdot '.join(map(str, bs))}) = \\log_{{{big(N)}}} {P}$.", f"${big(N)} = {P}^{{{k}}}$, so this is ${ft(v)}$."], "adding the bases.")


@reg(S, "challenge")
def lrc_system(r):
    a, b, c, d = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    det = a * d - b * c
    if det == 0:
        return None
    pval, qval = 1, 1
    X = F(pval * d - b * qval, det)
    Y = F(a * qval - c * pval, det)
    v = X + Y
    t = lambda e, s: "" if e == 0 else (s if e == 1 else f"{s}^{{{e}}}")
    p = f"If $\\log({t(a, 'x')}{t(b, 'y')}) = 1$ and $\\log({t(c, 'x')}{t(d, 'y')}) = 1$, what is $\\log(xy)$?"
    return Q(p, v, [F(2, a + b + c + d) * 2, F(1), v + 1, X, F(2, a + d) if F(2, a + d) != v else v * 2], "Let $u = \\log x$, $v = \\log y$.",
             "$\\log(xy)$.", f"${a}u + {b}v = 1$ and ${c}u + {d}v = 1$, a linear system.",
             [f"Solving: $u = {ft(X)}$, $v = {ft(Y)}$.", f"$\\log(xy) = u + v = {ft(v)}$."], "adding the equations without solving.") if v != 1 else None


@reg(S, "challenge")
def lrc_count_ineq(r):
    k = r.randint(2, 5)
    m = r.randint(1, 6)
    xs = [x for x in range(m + 1, 10 ** 4) if x * (x - m) < 2 ** k * 4 and math.log2(x) + math.log2(x - m) < k + 2]
    if not xs:
        return None
    p = f"How many integers $x$ satisfy $\\log_2 x + \\log_2 (x - {m}) < {k + 2}$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1 if len(xs) > 1 else 3, len(xs) + m, 2 ** (k + 2) - m, len(xs) + 2], "Combine, then remember the domain.",
             "the count.", f"we need $x > {m}$ and $x(x - {m}) < 2^{{{k + 2}}} = {2 ** (k + 2)}$.",
             [f"Checking integers $x > {m}$: " + ", ".join(map(str, xs)) + ".", f"Count: ${len(xs)}$."], "forgetting the domain $x > " + str(m) + "$.")


# ================================================================ log_equations
S = "log_equations"


@reg(S, "basics")
def le_same_base(r):
    b = r.choice([2, 3])
    m, n = r.randint(2, 4), r.randint(1, 7)
    v = F(n, m)
    p = f"Solve ${b ** m}^x = {b ** n}$."
    return Q(p, v, [F(m, n), F(b ** n, b ** m), v + 1, F(n, m + 1), n - m if n - m != v else v * 2], "Write both as powers of " + str(b) + ".",
             "$x$.", "match the exponents.", [f"${b}^{{{m}x}} = {b}^{{{n}}}$.", f"${m}x = {n}$, $x = {ft(v)}$."], "flipping the fraction.") if v.denominator != 1 else None


@reg(S, "basics")
def le_diff(r):
    b = r.choice([2, 3])
    k = r.randint(1, 3)
    x = r.randint(1, 10)
    a = x * (b ** k - 1)
    p = f"Solve $\\log_{{{b}}}(x + {a}) - \\log_{{{b}}} x = {k}$."
    return Q(p, x, [x + 1, a, b ** k, x * 2, a // k if a // k != x else x + 3], "Combine into one log.",
             "$x$.", f"$\\frac{{x + {a}}}{{x}} = {b ** k}$.", [f"$x + {a} = {b ** k}x$.", f"${b ** k - 1}x = {a}$, $x = {x}$."], "subtracting inside the log.")


@reg(S, "basics")
def le_equal_args(r):
    a, b = r.randint(2, 5), r.randint(1, 9)
    x = r.randint(1, 9)
    c = (a - 1) * x + b
    p = f"Solve $\\log_3({a}x + {b}) = \\log_3(x + {c})$."
    return Q(p, x, [x + 1, x - 1 if x > 1 else 5, c - b, F(c + b, a + 1), 2 * x], "Equal logs, same base: equal arguments.",
             "$x$.", "set the arguments equal, then check both are positive.", [f"${a}x + {b} = x + {c}$, so ${a - 1}x = {c - b}$, $x = {x}$.", "Both arguments are positive there."], "forgetting to check the domain.")


@reg(S, "basics")
def le_exp_eq(r):
    a, b = r.choice([(9, 27), (4, 8), (25, 125), (8, 16), (27, 81), (16, 32)])
    base = 3 if a in (9, 27) else 2 if a in (4, 8, 16) else 5
    ea, eb = round(math.log(a, base)), round(math.log(b, base))
    k = r.randint(1, 4)
    x = F(eb * k, eb - ea)
    p = f"Solve ${a}^{{x}} = {b}^{{x - {k}}}$."
    return Q(p, x, [-x, F(k, 1), x + 1, F(ea * k, eb - ea), F(eb * k, eb + ea)], "Write both sides with base " + str(base) + ".",
             "$x$.", "match the exponents.", [f"${base}^{{{ea}x}} = {base}^{{{eb}(x - {k})}}$.", f"${ea}x = {eb}x - {eb * k}$, so $x = {ft(x)}$."], "forgetting to distribute.")


@reg(S, "basics")
def le_base_unknown(r):
    x, k = r.choice([(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (4, 3), (5, 3), (2, 6), (3, 2), (7, 2)])
    p = f"Solve $\\log_x {x ** k} = {k}$ for $x > 0$."
    return Q(p, x, [x * x, x + 1, k, F(x ** k, k) if F(x ** k, k) < 1000 else x + 2, x - 1 if x > 2 else 6], "Rewrite in exponential form.",
             "$x$.", f"$x^{{{k}}} = {x ** k}$.", [f"$x = \\sqrt[{k}]{{{x ** k}}} = {x}$."], "dividing " + str(x ** k) + " by " + str(k) + ".")


@reg(S, "basics")
def le_quadratic_log(r):
    p1, p2 = r.sample(range(1, 7), 2)
    S_, P_ = p1 + p2, p1 * p2
    b = r.choice([2, 3])
    v = b ** S_
    p = f"What is the product of the solutions of $(\\log_{{{b}}} x)^2 - {S_}\\log_{{{b}}} x + {P_} = 0$?"
    return Q(p, v, [b ** P_, S_, P_, b ** p1 + b ** p2, v * b], "The two values of $\\log_{" + str(b) + "} x$ add to " + str(S_) + ".",
             "the product of the $x$ values.", "if $\\log x_1 + \\log x_2 = " + str(S_) + "$ then $x_1x_2 = " + str(b) + "^{" + str(S_) + "}$.",
             [f"$\\log_{{{b}}} x = {p1}$ or ${p2}$: $x = {b ** p1}$ or ${b ** p2}$.", f"Product: ${v}$."], "multiplying the logs.")


@reg(S, "basics")
def le_exp_product(r):
    a, b = r.randint(1, 3), r.randint(1, 3)
    k = r.randint(1, 4)
    tot = 3 * k
    x = F(tot, a + 2 * b)
    p = f"Solve $2^{{{a if a > 1 else ''}x}} \\cdot 4^{{{b if b > 1 else ''}x}} = " + ("8" if k == 1 else f"8^{{{k}}}") + "$."
    return Q(p, x, [F(tot, a + b), F(k, a + b), x + 1, F(3 * k, a * 2 * b), F(k, 1) if F(k, 1) != x else x * 2], "Write everything as powers of 2.",
             "$x$.", "add exponents on the left; match the right side.", [f"$2^{{{a}x + {2 * b}x}} = 2^{{{tot}}}$.", f"${a + 2 * b}x = {tot}$, $x = {ft(x)}$."], "treating $4^x$ as $2^x$.")


@reg(S, "basics")
def le_two_log(r):
    x = r.randint(2, 9)
    c = x * x - x
    p = f"Solve $2\\log_5 x = \\log_5 (x + {c})$."
    return Q(p, x, [x + 1, -x + 1, c, x * 2, x - 1], "Use the power rule on the left.",
             "$x$.", f"$x^2 = x + {c}$, keeping only positive $x$.", [f"$x^2 - x - {c} = 0$ factors as $(x - {x})(x + {x - 1}) = 0$.", f"$x = {x}$ (the other root is negative)."], "keeping the negative root.")


@reg(S, "basics")
def le_base_x(r):
    x = r.randint(2, 9)
    c = x * x - x
    p = f"Solve $\\log_x (x + {c}) = 2$."
    return Q(p, x, [x + 1, c, x * x, x - 1, 2 * x], "Rewrite in exponential form.",
             "$x$.", f"$x^2 = x + {c}$ with $x > 0$, $x \\ne 1$.", [f"$(x - {x})(x + {x - 1}) = 0$, so $x = {x}$."], "keeping the negative root.")


@reg(S, "basics")
def le_given_exp(r):
    b = r.choice([2, 3])
    c = r.choice([v for v in range(3, 10) if v not in (b, b * b, b ** 3)])
    m, k = r.randint(2, 3), r.randint(1, 2)
    v = c ** m * b ** (m * k)
    p = f"If ${b}^a = {c}$, what is ${b ** m}^{{a + {k}}}$?"
    return Q(p, v, [c ** m * b ** k, c * b ** (m * k), (c + k) ** m, v * b, c ** m + b ** (m * k)], "Rewrite with base " + str(b) + ".",
             "the value.", f"${b ** m}^{{a + {k}}} = ({b}^a)^{{{m}}} \\cdot {b}^{{{m * k}}}$.", [f"${c}^{{{m}}} \\cdot {b ** (m * k)} = {v}$."], "adding instead of multiplying the exponent.")


@reg(S, "basics")
def le_frac_exp(r):
    b = r.choice([4, 9, 16, 25, 27, 8])
    rt = {4: 2, 9: 3, 16: 2, 25: 5, 27: 3, 8: 2}[b]
    e = round(math.log(b, rt))
    m = r.randint(1, 5)
    if m % e == 0:
        return None
    v = F(m, e)
    x = rt ** m
    p = f"Solve $\\log_{{{b}}} x = {ft(v)}$."
    return Q(p, x, [b * m, rt ** (m + 1), x * rt if x * rt != x else x + 1, F(b * v.numerator, v.denominator), x - 1], "Exponential form.",
             "$x$.", f"$x = {b}^{{{ft(v)}}}$.", [f"${b} = {rt}^{{{e}}}$, so $x = {rt}^{{{m}}} = {x}$."], "multiplying " + str(b) + " by the exponent.")


@reg(S, "basics")
def le_growth(r):
    P0 = r.choice([100, 200, 500, 1000])
    d = r.randint(2, 8)
    k = r.randint(2, 6)
    target = P0 * 2 ** k
    p = f"A population of ${P0}$ doubles every ${d}$ hours. After how many hours will it reach ${big(target)}$?"
    return Q(p, k * d, [k, 2 ** k * d // 2, (k + 1) * d, d * target // P0 // 2, k * d - d], "How many doublings?",
             "the time.", f"$P = {P0} \\cdot 2^{{t/{d}}}$.", [f"$2^{{t/{d}}} = {2 ** k}$, so $\\frac{{t}}{{{d}}} = {k}$.", f"$t = {k * d}$ hours."], "dividing the target by the start without taking a log.")


@reg(S, "basics")
def le_exp_sum(r):
    a = r.randint(1, 3)
    x = r.randint(2, 6)
    tot = 2 ** x * (2 ** a + 1)
    p = f"Solve $2^{{x + {a}}} + 2^x = {tot}$."
    return Q(p, x, [x + 1, x - 1, x + a, tot // 2 ** a if tot // 2 ** a < 200 else x + 3, x * 2], "Factor out $2^x$.",
             "$x$.", f"$2^x(2^{{{a}}} + 1) = {tot}$.", [f"$2^x \\cdot {2 ** a + 1} = {tot}$, so $2^x = {2 ** x}$.", f"$x = {x}$."], "adding the exponents.")


@reg(S, "basics")
def le_nested(r):
    b, c = r.choice([(2, 3), (2, 2), (3, 2), (2, 5), (3, 3), (2, 4)])
    k = r.randint(1, 2)
    x = c ** (b ** k)
    p = f"Solve $\\log_{{{b}}}(\\log_{{{c}}} x) = {k}$."
    return Q(p, x, [c ** k, b ** k, c * b ** k, x * c, (c + b) ** k], "Peel off one log at a time.",
             "$x$.", f"$\\log_{{{c}}} x = {b}^{{{k}}} = {b ** k}$.", [f"$x = {c}^{{{b ** k}}} = {x}$."], "solving in the wrong order.")


@reg(S, "basics")
def le_halflife(r):
    m0 = r.choice([64, 80, 96, 128, 160, 320])
    h = r.randint(2, 10)
    k = r.randint(1, 4)
    ans = F(m0, 2 ** k)
    p = f"A substance has a half-life of ${h}$ years. Starting with ${m0}$ grams, how many grams remain after ${h * k}$ years?"
    return Q(p, ans, [F(m0, 2 * k), F(m0, 2 ** (k + 1)), m0 - h * k if m0 - h * k > 0 else F(m0, 3), F(m0, 2 ** (k - 1)) if k > 1 else F(m0, 3), ans + 1], "Count the half-lives.",
             "the remaining mass.", f"${h * k}$ years is ${k}$ half-lives.", [f"${m0} \\cdot \\left(\\frac{{1}}{{2}}\\right)^{{{k}}} = {ft(ans)}$."], "halving only once.")


@reg(S, "basics")
def le_e_quad(r):
    a, b = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (2, 5), (3, 4)])
    S_, P_ = a + b, a * b
    p = f"What is the sum of all real solutions of $e^{{2x}} - {S_}e^x + {P_} = 0$?"
    ans = C(f"\\ln {P_}", math.log(P_))
    return Q(p, ans, [C(f"\\ln {S_}", math.log(S_)), C(f"{S_}", S_), C(f"\\ln {a}", math.log(a) + 1e-6 if a == 1 else math.log(a)) if a > 1 else C("0", 1e-7), C(f"{P_}", P_), C(f"\\ln {P_ + 1}", math.log(P_ + 1))], "Let $u = e^x$.",
             "the sum.", f"$u^2 - {S_}u + {P_} = 0$ gives $u = {a}$ or ${b}$.", [f"$x = \\ln {a}$ or $\\ln {b}$.", f"Sum: $\\ln {a} + \\ln {b} = \\ln {P_}$."], "adding $u$ values instead of $x$ values.")


@reg(S, "challenge")
def lec_system(r):
    m, n = r.randint(-2, 6), r.randint(-2, 6)
    if (m + n) % 2 or m == n:
        return None
    a, b = m + n, m - n
    x, y = F(2) ** m, F(2) ** n
    v = x + y
    p = f"If $\\log_2 x + \\log_2 y = {a}$ and $\\log_2 x - \\log_2 y = {b}$, what is $x + y$?"
    return Q(p, v, [F(2) ** a, F(2) ** abs(b), v + 1, x * y, F(a + b, 1)], "Solve for each log first.",
             "$x + y$.", "add and subtract the equations.", [f"$\\log_2 x = {m}$, $\\log_2 y = {n}$.", f"$x = {ft(x)}$, $y = {ft(y)}$, sum ${ft(v)}$."], "adding the logs as if they were $x$ and $y$.")


@reg(S, "challenge")
def lec_xlogx(r):
    t1, t2 = r.choice([(4, -1), (3, -1), (2, -1), (5, -2), (3, -2), (6, -1), (4, -3)])
    b_, c_ = t1 + t2, -(t1 * t2)
    x1, x2 = F(2) ** t1, F(2) ** t2
    p = f"What is the product of all positive solutions of $x^{{\\log_2 x}} = {2 ** c_}x^{{{b_}}}$?".replace("x^{1}", "x")
    return Q(p, x1 * x2, [x1 + x2, F(2) ** c_, x1, F(b_), F(2) ** (b_ + 1)], "Take $\\log_2$ of both sides.",
             "the product.", f"with $t = \\log_2 x$: $t^2 = {c_} + {b_}t$.",
             [f"$t^2 - {b_}t - {c_} = 0$ gives $t = {t1}$ or ${t2}$.", f"$x = {ft(x1)}$ or ${ft(x2)}$; product $2^{{{t1 + t2}}} = {ft(x1 * x2)}$."], "forgetting the negative value of $t$.")


@reg(S, "challenge")
def lec_reciprocal(r):
    k = r.choice([2, 3])
    v = F(k * k + 1, k)
    t = {2: "\\sqrt{2}", 3: "\\sqrt[3]{2}"}[k]
    ans = C(f"{2 ** k} + {t}", 2 ** k + 2 ** (1 / k))
    p = f"What is the sum of the solutions of $\\log_x 2 + \\log_2 x = {ft(v)}$?"
    return Q(p, ans, [C(f"{2 ** k}", 2 ** k), C(f"{2 ** k} + {k}", 2 ** k + k), C(f"{ft(v)}", float(v)), C(f"{2 ** k} + \\frac{{1}}{{{k}}}", 2 ** k + 1 / k), C(f"2 + {t}", 2 + 2 ** (1 / k))], "Let $t = \\log_2 x$; then $\\log_x 2 = \\frac{1}{t}$.",
             "the sum.", f"$t + \\frac{{1}}{{t}} = {ft(v)}$ gives $t = {k}$ or $\\frac{{1}}{{{k}}}$.", [f"$x = 2^{{{k}}} = {2 ** k}$ or $x = 2^{{1/{k}}} = {t}$.", f"Sum: ${ans.tex}$."], "adding the $t$ values.")


@reg(S, "challenge")
def lec_equal_powers(r):
    a, b = r.choice([(2, 3), (2, 5), (3, 4), (2, 7), (3, 5)])
    k = r.randint(1, 4)
    p = f"If ${a}^x = {b}^y = " + (f"{a * b}" if k == 1 else f"{a * b}^{{{k}}}") + "$, what is $\\frac{{1}}{{x}} + \\frac{{1}}{{y}}$?"
    return Q(p, F(1, k), [F(k), F(2, k), F(1, a * b), F(k, 2), F(1, k + 1)], "Take logs: $x = " + str(k) + "\\log_{" + str(a) + "} " + str(a * b) + "$.",
             "the sum of reciprocals.", f"$\\frac{{1}}{{x}} = \\frac{{\\log_{{{a * b}}} {a}}}{{{k}}}$ and $\\frac{{1}}{{y}} = \\frac{{\\log_{{{a * b}}} {b}}}{{{k}}}$.",
             [f"Sum: $\\frac{{\\log_{{{a * b}}}({a} \\cdot {b})}}{{{k}}} = \\frac{{1}}{{{k}}}$."], "assuming $x = y$.")


@reg(S, "challenge")
def lec_count(r):
    a = r.randint(0, 8)
    k = r.randint(2, 6)
    ans = 2 ** k - 1
    p = f"How many integers $x$ satisfy $\\log_2 (x - {a}) < {k}$?" if a else f"How many integers $x$ satisfy $\\log_2 x < {k}$?"
    return Q(p, ans, [2 ** k, 2 ** k + a, k, 2 ** k - 2, 2 ** (k - 1)], "Mind the domain.",
             "the count.", f"need $0 < x - {a} < 2^{{{k}}}$.", [f"$x$ from ${a + 1}$ to ${a + 2 ** k - 1}$: ${ans}$ integers."], "including the endpoint or forgetting $x - " + str(a) + " > 0$.")


@reg(S, "challenge")
def lec_chain_eq(r):
    k = r.randint(2, 6)
    v = 2 ** k
    p = f"If $(\\log_2 3)(\\log_3 5)(\\log_5 y) = {k}$, what is $y$?"
    return Q(p, v, [5 ** k, 3 ** k, k * 5, v + 1, 2 * k], "Change of base telescopes.",
             "$y$.", "the product equals $\\log_2 y$.", [f"$\\log_2 y = {k}$, so $y = {v}$."], "using base 5.")


@reg(S, "challenge")
def lec_exp_system(r):
    m, n = r.sample(range(0, 6), 2)
    s, pr = 2 ** m + 2 ** n, 2 ** (m + n)
    v = m * m + n * n
    p = f"Real numbers $x$ and $y$ satisfy $2^x + 2^y = {s}$ and $2^{{x + y}} = {pr}$. What is $x^2 + y^2$?"
    return Q(p, v, [(m + n) ** 2, m + n, v + 1, 2 * m * n if 2 * m * n != v else v + 2, s], "$2^x$ and $2^y$ are roots of a quadratic.",
             "$x^2 + y^2$.", f"$2^x$ and $2^y$ have sum ${s}$ and product ${pr}$.", [f"They are ${2 ** m}$ and ${2 ** n}$, so $\\{{x, y\\}} = \\{{{m}, {n}\\}}$.", f"${m}^2 + {n}^2 = {v}$."], "squaring the sum.")


# ================================================================ log_change_base
S = "log_change_base"


@reg(S, "basics")
def lcb_express(r):
    b = r.choice([2, 3, 5])
    m, n = r.randint(1, 3), r.randint(1, 3)
    c = r.choice([x for x in (3, 5, 7) if x != b])
    v = F(n, m)
    p = f"If $\\log_{{{b}}} {c} = t$, what is $\\log_{{{b ** m}}} {c ** n}$ in terms of $t$?"
    lab = lambda q: "t" if q == 1 else ("-t" if q == -1 else (f"{q.numerator}t" if q.denominator == 1 else f"\\frac{{{q.numerator if q.numerator != 1 else ''}t}}{{{q.denominator}}}"))
    opts = {v, F(m, n), F(n * m), v + 1, F(n, m + 1), F(n + m)}
    opts.discard(v)
    return Q(p, C(lab(v), float(v)), [C(lab(q), float(q)) for q in list(opts)[:5]], "Pull the exponents out front.",
             "the expression.", f"$\\log_{{b^m}} x^n = \\frac{{n}}{{m}}\\log_b x$.", [f"$\\log_{{{b ** m}}} {c ** n} = \\frac{{{n}}}{{{m}}}\\log_{{{b}}} {c} = {lab(v)}$."], "flipping $\\frac{n}{m}$.") if not (m == 1 and n == 1) else None


@reg(S, "basics")
def lcb_product_two(r):
    a, b = r.sample([2, 3, 5, 7], 2)
    m, n = r.randint(2, 4), r.randint(2, 4)
    p = f"What is $\\log_{{{a}}} {b ** m} \\cdot \\log_{{{b}}} {a ** n}$?"
    return Q(p, m * n, [m + n, F(m, n), m * n + 1, a * b, 1], "Change of base: $\\log_a b \\cdot \\log_b a = 1$.",
             "the product.", "pull out the exponents.", [f"${m}\\log_{{{a}}} {b} \\cdot {n}\\log_{{{b}}} {a} = {m * n} \\cdot 1 = {m * n}$."], "adding the exponents.")


@reg(S, "basics")
def lcb_ratio(r):
    b = r.choice([3, 5, 7, 10])
    x = r.choice([2, 3])
    m, n = r.randint(2, 6), r.randint(1, 3)
    if m % n:
        return None
    v = F(m, n)
    p = f"What is $\\dfrac{{\\log_{{{b}}} {x ** m}}}{{\\log_{{{b}}} {x ** n}}}$?"
    return Q(p, v, [F(x ** m, x ** n), F(m - n), F(n, m), v + 1, F(x ** (m - n))], "The ratio is a change of base.",
             "the ratio.", f"$\\frac{{\\log_b A}}{{\\log_b B}} = \\log_B A$.", [f"$\\log_{{{x ** n}}} {x ** m} = {ft(v)}$."], "dividing inside the logs.") if F(x ** m, x ** n) != v else None


@reg(S, "basics")
def lcb_sqrt_base(r):
    b = r.choice([2, 3, 5])
    k = r.randint(1, 5)
    p = f"What is $\\log_{{\\sqrt{{{b}}}}} {b ** k}$?"
    return Q(p, 2 * k, [k, F(k, 2), 2 * k + 1, k * k if k * k != 2 * k else k + 3, b ** k // 2 if b ** k // 2 not in (2 * k,) else 4 * k], "$\\sqrt{" + str(b) + "} = " + str(b) + "^{1/2}$.",
             "the logarithm.", "a base of $b^{1/2}$ doubles the log.", [f"$\\left({b}^{{1/2}}\\right)^{{{2 * k}}} = {b}^{{{k}}}$."], "halving instead of doubling.")


@reg(S, "basics")
def lcb_square_base(r):
    t = F(r.randint(1, 9), r.randint(1, 4))
    m = r.randint(2, 3)
    v = t / m
    p = f"If $\\log_a b = {ft(t)}$, what is $\\log_{{a^{{{m}}}}} b$?"
    return Q(p, v, [t * m, t, t + m, F(m) / t, v + 1], "Base $a^m$ divides the log by $m$.",
             "the value.", "$\\log_{a^m} b = \\frac{1}{m}\\log_a b$.", [f"$\\frac{{{ft(t)}}}{{{m}}} = {ft(v)}$."], "multiplying by $m$.")


@reg(S, "basics")
def lcb_mixed(r):
    x, y = r.choice([(4, 2), (8, 2), (9, 3), (27, 3), (16, 2), (25, 5)]), r.choice([(4, 8), (9, 27), (8, 4), (27, 9), (25, 125), (16, 8)])
    v1 = F(round(math.log(x[1], x[0]) * 1000), 1000)
    v1 = F(1, round(math.log(x[0], x[1])))
    v2 = F(round(math.log(y[1], 2 if y[0] in (4, 8, 16) else 3 if y[0] in (9, 27) else 5)), round(math.log(y[0], 2 if y[0] in (4, 8, 16) else 3 if y[0] in (9, 27) else 5)))
    v = v1 + v2
    p = f"What is $\\log_{{{x[0]}}} {x[1]} + \\log_{{{y[0]}}} {y[1]}$?"
    return Q(p, v, [v1 * v2, v + 1, 1 / v1 + 1 / v2, v1 + 1 / v2, v - F(1, 2)], "Write each in a common base.",
             "the sum.", "convert each log to a power of a smaller base.", [f"$\\log_{{{x[0]}}} {x[1]} = {ft(v1)}$, $\\log_{{{y[0]}}} {y[1]} = {ft(v2)}$.", f"Sum: ${ft(v)}$."], "flipping one of the fractions.")


@reg(S, "basics")
def lcb_ln_ratio(r):
    b = r.choice([2, 3, 5])
    k = r.randint(2, 6)
    fn = r.choice(["\\ln", "\\log"])
    p = f"What is $\\dfrac{{{fn} {b ** k}}}{{{fn} {b}}}$?"
    return Q(p, k, [b ** (k - 1), k - 1, k + 1, F(b ** k, b), b * k], "Change of base.",
             "the ratio.", f"$\\frac{{{fn} A}}{{{fn} B}} = \\log_B A$.", [f"$\\log_{{{b}}} {b ** k} = {k}$."], "dividing the numbers inside.") if b ** (k - 1) != k else None


@reg(S, "basics")
def lcb_approx(r):
    p = "Using $\\log_{10} 2 \\approx 0.30$, which is closest to $\\log_2 10$?"
    if r.random() < .5:
        p = "Using $\\log_{10} 3 \\approx 0.48$, which is closest to $\\log_3 10$?"
        v, w = 2.08, [0.48, 1.48, 2.48, 3.08]
    else:
        v, w = 3.33, [0.30, 1.30, 2.70, 4.33]
    return Q(p, C(f"{v:.2f}", v), [C(f"{x:.2f}", x) for x in w], "$\\log_b a = \\frac{1}{\\log_a b}$.",
             "the approximation.", "take the reciprocal.", [f"$\\frac{{1}}{{{p[p.index('approx') + 7:p.index('approx') + 11]}}} \\approx {v:.2f}$."], "subtracting from 1 instead of taking the reciprocal.")


@reg(S, "basics")
def lcb_fraction_base(r):
    a, b = r.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5)])
    k = r.randint(2, 4)
    sgn = r.choice([1, -1])
    arg = F(a ** k, b ** k) if sgn > 0 else F(b ** k, a ** k)
    p = f"What is $\\log_{{\\frac{{{a}}}{{{b}}}}} {ft(arg)}$?"
    return Q(p, sgn * k, [-sgn * k, F(sgn, k), k + 1, F(a ** k, b) if F(a ** k, b) != sgn * k else 2 * k, 0], "Is the argument a power of the base?",
             "the log.", f"${ft(arg)} = \\left(\\frac{{{a}}}{{{b}}}\\right)^{{{sgn * k}}}$.", [f"So the log is ${sgn * k}$."], "missing the sign when the fraction is flipped.")


@reg(S, "basics")
def lcb_exp_log(r):
    b = r.choice([2, 3])
    m = r.choice([2, 3])
    x = r.randint(2, 9)
    base = b ** m
    ans = C(f"\\sqrt[{m}]{{{x}}}" if m == 3 else f"\\sqrt{{{x}}}", x ** (1 / m)) if round(x ** (1 / m)) ** m != x else num(round(x ** (1 / m)))
    p = f"What is ${b}^{{\\log_{{{base}}} {x}}}$?"
    return Q(p, ans, [num(x), num(x * m), num(x ** m), C(f"\\frac{{{x}}}{{{m}}}", x / m), num(x + m)], "Rewrite the log in base " + str(b) + ".",
             "the value.", f"$\\log_{{{base}}} {x} = \\frac{{1}}{{{m}}}\\log_{{{b}}} {x}$.", [f"${b}^{{\\frac{{1}}{{{m}}}\\log_{{{b}}} {x}}} = {x}^{{1/{m}}} = {ans.tex}$."], "answering " + str(x) + ".")


@reg(S, "basics")
def lcb_reciprocal_pair(r):
    a, b = r.sample([2, 3, 5, 6, 7], 2)
    k = r.randint(1, 3)
    N = (a * b) ** k
    p = f"What is $\\dfrac{{1}}{{\\log_{{{a}}} {big(N)}}} + \\dfrac{{1}}{{\\log_{{{b}}} {big(N)}}}$?"
    return Q(p, F(1, k), [F(k), F(2, k), F(1, a + b), F(1, k + 1), F(k, 2)], "Flip each log.",
             "the sum.", "$\\frac{1}{\\log_a N} = \\log_N a$.", [f"$\\log_{{{big(N)}}} {a} + \\log_{{{big(N)}}} {b} = \\log_{{{big(N)}}} {a * b} = \\frac{{1}}{{{k}}}$."], "multiplying the logs.")


@reg(S, "basics")
def lcb_digits_10(r):
    k = r.randint(2, 30)
    m = r.choice([2, 3, 5, 7])
    v = k + 1
    p = f"How many digits does ${m} \\cdot 10^{{{k}}}$ have?"
    return Q(p, v, [k, k + 2, m + k, k * m if k * m != v else v + 3, v + m], "Count using $\\log_{10}$.",
             "the number of digits.", "a number with $\\lfloor \\log_{10} N \\rfloor = k$ has $k + 1$ digits.", [f"$\\log_{{10}}({m} \\cdot 10^{{{k}}}) = {k} + \\log_{{10}} {m}$, with floor ${k}$.", f"Digits: ${v}$."], "answering " + str(k) + ".")


@reg(S, "basics")
def lcb_between(r):
    b = r.choice([2, 3, 5])
    N = r.randint(10, 5000)
    k = 0
    while b ** (k + 1) <= N:
        k += 1
    if b ** k == N:
        return None
    p = f"The number $\\log_{{{b}}} {N}$ lies between which two consecutive integers? Give the smaller one."
    return Q(p, k, [k + 1, k - 1, k + 2, N // b if N // b not in (k, k + 1, k - 1, k + 2) else k + 3, max(0, k - 2) if k - 2 >= 0 and k - 2 != k else k + 4], "Bracket " + str(N) + " between powers of " + str(b) + ".",
             "the smaller integer.", "find consecutive powers of the base around the number.", [f"${b}^{{{k}}} = {b ** k} < {N} < {b ** (k + 1)} = {b}^{{{k + 1}}}$."], "picking the upper integer.")


@reg(S, "basics")
def lcb_log_of_inverse(r):
    a, b = "a", "b"
    t = F(r.randint(1, 5), r.randint(1, 3))
    if t == 1:
        return None
    v = -1 / t
    p = f"If $\\log_{{a}} b = {ft(t)}$, what is $\\log_{{a}} \\frac{{1}}{{b}} \\cdot \\log_{{b}} a \\cdot \\frac{{1}}{{\\log_{{a}} b}}$?"
    v = -1 / t
    return Q(p, v, [1 / t, -t, t, -1, v + 1], "Use $\\log_b a = \\frac{1}{\\log_a b}$.",
             "the value.", "rewrite each factor in terms of $t = \\log_{" + str(a) + "} " + str(b) + "$.",
             [f"$\\log_{{{a}}} \\frac{{1}}{{{b}}} = -t$, $\\log_{{{b}}} {a} = \\frac{{1}}{{t}}$, last factor $\\frac{{1}}{{t}}$.", f"Product: $-t \\cdot \\frac{{1}}{{t}} \\cdot \\frac{{1}}{{t}} = -\\frac{{1}}{{t}} = {ft(v)}$."], "dropping the negative sign.")


@reg(S, "basics")
def lcb_compare(r):
    b = r.choice([2, 3])
    m = r.randint(2, 4)
    k = r.randint(2, 5)
    p = f"What is $\\log_{{{b ** m}}} x$ if $\\log_{{{b}}} x = {m * k}$?"
    return Q(p, k, [m * m * k, m * k, k + m, m, k * 2 if k * 2 != k else k + 1], "Divide by the exponent of the base.",
             "the log.", f"$\\log_{{{b}^{m}}} x = \\frac{{\\log_{{{b}}} x}}{{{m}}}$.", [f"$\\frac{{{m * k}}}{{{m}}} = {k}$."], "multiplying by " + str(m) + ".")


@reg(S, "basics")
def lcb_power_eq(r):
    a, b = r.choice([(4, 2), (8, 2), (9, 3), (27, 3), (8, 4), (27, 9), (32, 8), (125, 25)])
    v = F(round(math.log(b, min(a, b) if False else 2 if a in (4, 8, 32) else 3 if a in (9, 27) else 5) * 1000), 1000)
    base = 2 if a in (4, 8, 32) else 3 if a in (9, 27) else 5
    v = F(round(math.log(b, base)), round(math.log(a, base)))
    p = f"If ${a}^x = {b}$, what is $x$?"
    return Q(p, v, [1 / v, F(b, a), v + 1, F(a, b) if F(a, b) != 1 / v else v * 2, v / 2], "Write both as powers of " + str(base) + ".",
             "$x$.", f"$x = \\log_{{{a}}} {b}$.", [f"${base}^{{{round(math.log(a, base))}x}} = {base}^{{{round(math.log(b, base))}}}$, so $x = {ft(v)}$."], "dividing the numbers.")


@reg(S, "challenge")
def lcbc_two_vars(r):
    a, b = r.randint(2, 5), r.randint(2, 5)
    x, y = F(1, a), F(1, b)
    v = x + y
    p = f"If $\\log_N 2 = \\frac{{1}}{{{a}}}$ and $\\log_N 3 = \\frac{{1}}{{{b}}}$, what is $\\log_N 6$?"
    return Q(p, v, [F(1, a + b), F(1, a * b), F(2, a + b), v + 1, x * y], "$6 = 2 \\cdot 3$.",
             "$\\log_N 6$.", "the log of a product is the sum of the logs.", [f"$\\frac{{1}}{{{a}}} + \\frac{{1}}{{{b}}} = {ft(v)}$."], "adding denominators.")


@reg(S, "challenge")
def lcbc_digits_power(r):
    n = r.randint(10, 60)
    v = math.floor(n * math.log10(2)) + 1
    if abs(n * 0.30103 - round(n * 0.30103)) < 0.02:
        return None
    p = f"Using $\\log_{{10}} 2 \\approx 0.30103$, how many digits does $2^{{{n}}}$ have?"
    return Q(p, v, [v - 1, v + 1, n // 3, math.ceil(n * 0.30103) + 1 if math.ceil(n * 0.30103) + 1 != v else v + 2, n], "$\\lfloor \\log_{10} N \\rfloor + 1$ digits.",
             "the digit count.", "compute $\\log_{10} 2^{" + str(n) + "} = " + str(n) + " \\log_{10} 2$.", [f"${n} \\cdot 0.30103 \\approx {n * 0.30103:.3f}$.", f"Floor plus 1: ${v}$."], "forgetting to add 1.")


@reg(S, "challenge")
def lcbc_symmetric(r):
    k = r.randint(3, 8)
    v = k * k - 2
    p = f"If $\\log_a b + \\log_b a = {k}$, what is $(\\log_a b)^2 + (\\log_b a)^2 - (\\log_a b)(\\log_b a)$?"
    return Q(p, v - 1, [v, k * k, k * k - 1, v - 2, 2 * k], "$(\\log_a b)(\\log_b a) = 1$.",
             "the value.", "with $t + \\frac{1}{t} = " + str(k) + "$: $t^2 + \\frac{1}{t^2} = " + str(k) + "^2 - 2$.", [f"$t^2 + \\frac{{1}}{{t^2}} = {v}$; subtract $1$: ${v - 1}$."], "forgetting the product is 1.")


@reg(S, "challenge")
def lcbc_count_range(r):
    b = r.choice([2, 3])
    lo, hi = r.randint(1, 3), r.randint(4, 6)
    cnt = b ** hi - b ** lo + 1
    p = f"How many positive integers $n$ satisfy ${lo} \\le \\log_{{{b}}} n \\le {hi}$?"
    return Q(p, cnt, [cnt - 1, cnt + 1, b ** hi - b ** lo, hi - lo + 1, b ** (hi - lo)], "Convert to bounds on $n$.",
             "the count.", f"${b}^{{{lo}}} \\le n \\le {b}^{{{hi}}}$.", [f"${b ** lo} \\le n \\le {b ** hi}$: ${b ** hi} - {b ** lo} + 1 = {cnt}$."], "forgetting to include both endpoints.")


@reg(S, "challenge")
def lcbc_log_sum_pairs(r):
    n = r.randint(5, 10)
    v = F(n - 1, 1)
    p = f"What is $\\displaystyle\\sum_{{k=2}}^{{{n}}} \\log_{{k}} (k^{{\\log_{{2}} 2}})$?"
    p = f"What is $\\log_2 3 \\cdot \\log_3 2 + \\log_3 4 \\cdot \\log_4 3 + \\cdots + \\log_{{{n}}} {n + 1} \\cdot \\log_{{{n + 1}}} {n}$?"
    return Q(p, n - 1, [n, n - 2, 1, F(n - 1, 2), n + 1], "Each product is $\\log_a b \\cdot \\log_b a$.",
             "the sum.", "$\\log_a b \\cdot \\log_b a = 1$ for each pair.", [f"There are ${n - 1}$ terms (from $k = 2$ to ${n}$), each equal to $1$.", f"Sum: ${n - 1}$."], "miscounting the terms.")


@reg(S, "challenge")
def lcbc_abc(r):
    a, b = r.randint(2, 6), r.randint(2, 6)
    v = F(a * b, a + b)
    p = f"If $\\log_x w = {a}$ and $\\log_y w = {b}$, what is $\\log_{{xy}} w$?"
    return Q(p, v, [F(a + b), F(a * b), F(a + b, 2), F(a + b, a * b), v + 1], "Flip: $\\log_w x = \\frac{1}{" + str(a) + "}$.",
             "the value.", "$\\log_w(xy) = \\frac{1}{" + str(a) + "} + \\frac{1}{" + str(b) + "}$, then flip back.", [f"$\\log_w(xy) = {ft(F(1, a) + F(1, b))}$.", f"$\\log_{{xy}} w = {ft(v)}$."], "adding the logs directly.") if (a, b) != (6, 7) else None


@reg(S, "challenge")
def lcbc_compare_powers(r):
    a, b, m, n = r.choice([(2, 3, 300, 200), (2, 5, 70, 30), (3, 2, 50, 80), (5, 3, 40, 60), (2, 7, 100, 35), (3, 5, 120, 80)])
    v1, v2 = m * math.log10(a), n * math.log10(b)
    larger = f"{a}^{{{m}}}" if v1 > v2 else f"{b}^{{{n}}}"
    q = F(round(v1 / v2 * 100), 100)
    p = f"Which is larger, ${a}^{{{m}}}$ or ${b}^{{{n}}}$? (Use $\\log_{{10}} 2 \\approx 0.301$, $\\log_{{10}} 3 \\approx 0.477$, $\\log_{{10}} 5 \\approx 0.699$, $\\log_{{10}} 7 \\approx 0.845$.)"
    opts = [f"{a}^{{{m}}}", f"{b}^{{{n}}}", "\\text{they are equal}", "\\text{can't tell}"]
    ans = C(larger, opts.index(larger))
    return Q(p, ans, [C(o, i) for i, o in enumerate(opts) if o != larger] + [C("\\text{neither}", 9)], "Compare the logs.",
             "the larger number.", "compare $m\\log a$ with $n\\log b$.", [f"${m} \\log {a} \\approx {v1:.1f}$ and ${n} \\log {b} \\approx {v2:.1f}$.", f"So ${larger}$ is larger."], "comparing the exponents alone.")


# ================================================================ complex helpers
def ctex(z):
    """LaTeX for a complex number with Fraction parts."""
    a, b = F(z[0]), F(z[1])
    if b == 0:
        return ft(a)
    bi = ("" if abs(b) == 1 else ft(abs(b))) + "i"
    if b.denominator != 1:
        bi = f"\\frac{{{abs(b.numerator) if abs(b.numerator) != 1 else ''}i}}{{{b.denominator}}}" if abs(b.numerator) != 1 else f"\\frac{{i}}{{{b.denominator}}}"
        bi = f"\\frac{{{abs(b.numerator)}}}{{{b.denominator}}}i"
    if a == 0:
        return ("-" if b < 0 else "") + bi
    return f"{ft(a)} {'+' if b > 0 else '-'} {bi}"


def CZ(z):
    a, b = F(z[0]), F(z[1])
    return C(ctex((a, b)), float(a) * 1000 + float(b))


def cmul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def cdiv(z, w):
    d = w[0] * w[0] + w[1] * w[1]
    return (F(z[0] * w[0] + z[1] * w[1], d), F(z[1] * w[0] - z[0] * w[1], d))


def rz(r, lo=-9, hi=9):
    while True:
        z = (r.randint(lo, hi), r.randint(lo, hi))
        if z[0] and z[1]:
            return z


def zp(z):
    return f"({ctex(z)})"


# ================================================================ cx_arithmetic
S = "cx_arithmetic"


@reg(S, "basics")
def cxa_conj_product(r):
    z = rz(r)
    v = z[0] ** 2 + z[1] ** 2
    p = f"What is $({ctex(z)})({ctex((z[0], -z[1]))})$?"
    return Q(p, v, [z[0] ** 2 - z[1] ** 2, v + 1, CZ((z[0] ** 2 - z[1] ** 2, 2 * z[0] * z[1])), -v, 2 * z[0]], "A number times its conjugate.",
             "the product.", "$(a + bi)(a - bi) = a^2 + b^2$.", [f"${par(z[0])}^2 + {par(z[1])}^2 = {v}$."], "getting $a^2 - b^2$.")


@reg(S, "basics")
def cxa_square(r):
    z = rz(r, -6, 6)
    w = cmul(z, z)
    p = f"What is $({ctex(z)})^2$?"
    return Q(p, CZ(w), [CZ((z[0] ** 2 + z[1] ** 2, 2 * z[0] * z[1])), CZ((z[0] ** 2 - z[1] ** 2, z[0] * z[1])), CZ((z[0] ** 2, z[1] ** 2)), CZ((w[0], -w[1])), CZ((-w[0], w[1]))], "Expand; $i^2 = -1$.",
             "the square.", "$(a + bi)^2 = a^2 - b^2 + 2abi$.", [f"${z[0] ** 2} - {z[1] ** 2}{sg(2 * z[0] * z[1])}i$ simplifies to ${ctex(w)}$."], "using $i^2 = 1$.")


@reg(S, "basics")
def cxa_recip_real(r):
    z = rz(r, -8, 8)
    d = z[0] ** 2 + z[1] ** 2
    part = r.choice(["real", "imaginary"])
    v = F(z[0], d) if part == "real" else F(-z[1], d)
    p = f"What is the {part} part of $\\dfrac{{1}}{{{ctex(z)}}}$?"
    return Q(p, v, [F(1, z[0]) if part == "real" else F(-1, z[1]), -v, F(z[1], d) if part == "real" else F(z[0], d), F(z[0] if part == "real" else z[1], z[0] ** 2 - z[1] ** 2) if z[0] ** 2 != z[1] ** 2 else v + 1, v * 2], "Multiply by the conjugate.",
             f"the {part} part.", "$\\frac{1}{a + bi} = \\frac{a - bi}{a^2 + b^2}$.", [f"$\\frac{{{ctex((z[0], -z[1]))}}}{{{d}}}$.", f"{part.capitalize()} part: ${ft(v)}$."], "forgetting the sign from the conjugate.")


@reg(S, "basics")
def cxa_solve(r):
    z, a = rz(r, -5, 5), rz(r, -4, 4)
    b = cmul(a, z)
    p = f"Solve $({ctex(a)})z = {ctex(b)}$."
    return Q(p, CZ(z), [CZ((z[0], -z[1])), CZ((-z[0], z[1])), CZ((z[1], z[0])) if z[0] != z[1] else CZ((z[0] + 1, z[1])), CZ(cmul(b, (a[0], -a[1]))), CZ((z[0] + 1, z[1] - 1))], "Divide, using the conjugate.",
             "$z$.", f"$z = \\frac{{{ctex(b)}}}{{{ctex(a)}}}$; multiply top and bottom by ${ctex((a[0], -a[1]))}$.", [f"Numerator: $({ctex(b)})({ctex((a[0], -a[1]))}) = {ctex(cmul(b, (a[0], -a[1])))}$; denominator: ${a[0] ** 2 + a[1] ** 2}$.", f"$z = {ctex(z)}$."], "forgetting to divide by $|a|^2$.")


@reg(S, "basics")
def cxa_quad_roots(r):
    pp, q = r.randint(-6, 6), r.randint(1, 9)
    ask = r.choice(["q", "sum"])
    v = q if ask == "q" else pp + q
    p = f"The roots of $x^2 {'-' if pp > 0 else '+'} {abs(2 * pp)}x + {pp * pp + q * q} = 0$ are $p \\pm qi$ with $q > 0$. What is {'$q$' if ask == 'q' else '$p + q$'}?".replace("x^2 + 0x", "x^2").replace("- 0x", "")
    return Q(p, v, [v + 1, q * q, pp * pp + q * q, abs(v - 2) if abs(v - 2) != v else v + 2, -v if -v != v else v + 3], "Complete the square.",
             "the value.", f"$(x - {pp})^2 = -{q * q}$.".replace("- -", "+ "), [f"$x = {pp} \\pm {q}i$." if pp else f"$x = \\pm {q}i$.", f"Answer: ${v}$."], "taking the square root of a negative incorrectly.") if pp else None


@reg(S, "basics")
def cxa_mod_quotient(r):
    tr = [(3, 4), (5, 12), (8, 15), (6, 8), (1, 1)]
    a, b = r.sample(tr[:4], 2)
    za, zb = (a[0] * r.choice([1, -1]), a[1]), (b[0], b[1] * r.choice([1, -1]))
    ma, mb = math.isqrt(a[0] ** 2 + a[1] ** 2), math.isqrt(b[0] ** 2 + b[1] ** 2)
    v = F(ma, mb)
    p = f"What is $\\left|\\dfrac{{{ctex(za)}}}{{{ctex(zb)}}}\\right|$?"
    return Q(p, v, [F(mb, ma), F(ma * ma, mb * mb), v + 1, F(ma + mb, mb), F(ma, mb + 1)], "$|z/w| = |z|/|w|$.",
             "the modulus.", "divide the moduli.", [f"$|{ctex(za)}| = {ma}$, $|{ctex(zb)}| = {mb}$.", f"${ft(v)}$."], "dividing then taking only the real part.")


@reg(S, "basics")
def cxa_conj_info(r):
    a, b = r.randint(-8, 8), r.randint(1, 9)
    if a == 0:
        return None
    n = a * a + b * b
    p = f"A complex number $z$ has $z + \\overline{{z}} = {2 * a}$ and $z\\overline{{z}} = {n}$. What is $|\\text{{Im}}(z)|$?"
    return Q(p, b, [b * b, n - a, abs(a), b + 1, math.isqrt(n) if math.isqrt(n) != b else b + 2], "$z + \\overline{z} = 2\\,\\text{Re}(z)$ and $z\\overline{z} = |z|^2$.",
             "the imaginary part's size.", "find the real part, then use $|z|^2 = a^2 + b^2$.", [f"$\\text{{Re}}(z) = {a}$.", f"$b^2 = {n} - {a * a} = {b * b}$, so $|b| = {b}$."], "forgetting to halve $z + \\overline{z}$.")


@reg(S, "basics")
def cxa_i_product(r):
    n = r.randint(4, 30)
    e = n * (n + 1) // 2
    vals = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}
    v = vals[e % 4]
    p = f"What is $i \\cdot i^2 \\cdot i^3 \\cdots i^{{{n}}}$?"
    opts = [CZ(vals[k]) for k in range(4) if vals[k] != v] + [CZ((0, 0))]
    return Q(p, CZ(v), opts, "Add the exponents.",
             "the product.", f"the exponent is $1 + 2 + \\cdots + {n} = {e}$.", [f"${e} \\equiv {e % 4} \\pmod 4$, so $i^{{{e}}} = {ctex(v)}$."], "multiplying exponents.")


@reg(S, "basics")
def cxa_make_real(r):
    b, c, d = r.randint(1, 8), r.randint(1, 8), r.choice([1, 2, 3, 4, -1, -2])
    k = F(-b * c, d)
    p = f"For what real number $k$ is $(k + {b}i)({c} {'+' if d > 0 else '-'} {abs(d) if abs(d) != 1 else ''}i)$ a real number?"
    return Q(p, k, [-k, F(b * d, c), F(-b * d, c) if F(-b * d, c) != k else k + 1, k + 1, F(b * c)], "Set the imaginary part to zero.",
             "$k$.", "expand and collect the $i$ terms.", [f"Imaginary part: ${d}k + {b * c}$.", f"${d}k + {b * c} = 0$ gives $k = {ft(k)}$."], "setting the real part to zero.")


@reg(S, "basics")
def cxa_distance(r):
    a, b = rz(r), rz(r)
    d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    p = f"What is the distance between ${ctex(a)}$ and ${ctex(b)}$ in the complex plane?"
    return Q(p, rad(1, d2), [rad(1, (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2) if (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2 else num(1), num(abs(a[0] - b[0]) + abs(a[1] - b[1])), rad(1, d2 + 1), num(d2), rad(1, d2 + 2)], "$|z - w|$.",
             "the distance.", "subtract, then take the modulus.", [f"$z - w = {ctex((a[0] - b[0], a[1] - b[1]))}$.", f"$|z - w| = \\sqrt{{{d2}}} = {rad(1, d2).tex}$."], "adding instead of subtracting.") if d2 else None


@reg(S, "basics")
def cxa_rotate(r):
    z = rz(r)
    k = r.choice([1, 2, 3])
    w = z
    for _ in range(k):
        w = cmul(w, (0, 1))
    p = f"The point ${ctex(z)}$ is rotated ${90 * k}^\\circ$ counterclockwise about the origin. What complex number is its image?"
    return Q(p, CZ(w), [CZ(cmul(z, (0, -1)) if k != 3 else cmul(z, (0, 1))), CZ((z[1], z[0])) if (z[1], z[0]) != w else CZ((z[0] + 1, z[1])), CZ((-z[0], -z[1])) if k != 2 else CZ((z[1], -z[0] + 1)), CZ((z[0], -z[1])), CZ((-z[1], -z[0]))], "Multiply by $i$ for each $90^\\circ$.",
             "the image.", f"rotating by ${90 * k}^\\circ$ multiplies by $i^{{{k}}}$.", [f"$({ctex(z)}) \\cdot {ctex({1: (0, 1), 2: (-1, 0), 3: (0, -1)}[k])} = {ctex(w)}$."], "rotating clockwise.")


@reg(S, "basics")
def cxa_sqrt(r):
    w = rz(r, 1, 6)
    s = cmul(w, w)
    p = f"Which complex number $a + bi$ with $a > 0$ satisfies $(a + bi)^2 = {ctex(s)}$?"
    return Q(p, CZ(w), [CZ((w[1], w[0])) if w[0] != w[1] else CZ((w[0] + 1, w[1])), CZ((w[0], -w[1])), CZ((w[0] + 1, w[1])), CZ((s[0], s[1] // 2)) if s[1] % 2 == 0 and (s[0], s[1] // 2) != w else CZ((w[0], w[1] + 1)), CZ((w[0] * 2, w[1]))], "Match real and imaginary parts.",
             "$a + bi$.", f"$a^2 - b^2 = {s[0]}$ and $2ab = {s[1]}$.", [f"Trying factor pairs of ${s[1] // 2}$: $a = {w[0]}$, $b = {w[1]}$ works."], "forgetting $2ab$.")


@reg(S, "basics")
def cxa_sum_mod_sq(r):
    z, w = rz(r, -7, 7), rz(r, -7, 7)
    v = z[0] ** 2 + z[1] ** 2 + w[0] ** 2 + w[1] ** 2
    m = (z[0] + w[0]) ** 2 + (z[1] + w[1]) ** 2
    p = f"What is $|{ctex(z)}|^2 + |{ctex(w)}|^2$?"
    return Q(p, v, [m if m != v else v + 1, v + 2, z[0] ** 2 - z[1] ** 2 + w[0] ** 2 - w[1] ** 2, abs(z[0]) + abs(z[1]) + abs(w[0]) + abs(w[1]), v - 1], "$|a + bi|^2 = a^2 + b^2$.",
             "the sum.", "square each modulus.", [f"${z[0] ** 2 + z[1] ** 2} + {w[0] ** 2 + w[1] ** 2} = {v}$."], "adding the numbers first.")


@reg(S, "basics")
def cxa_over_conj(r):
    a, b = r.choice([(3, 4), (4, 3), (5, 12), (12, 5), (1, 2), (2, 1), (1, 3)])
    z = (a, b * r.choice([1, -1]))
    d = a * a + b * b
    w = cmul(z, z)
    v = (F(w[0], d), F(w[1], d))
    p = f"What is $\\dfrac{{{ctex(z)}}}{{{ctex((z[0], -z[1]))}}}$?"
    return Q(p, CZ(v), [CZ((v[0], -v[1])), CZ((F(1), F(0))), CZ((F(w[0]), F(w[1]))), CZ((-v[0], v[1])), CZ((F(a * a + b * b, d) - 2, v[1] + 1))], "Multiply top and bottom by the top.",
             "the quotient.", "$\\frac{z}{\\overline{z}} = \\frac{z^2}{|z|^2}$.", [f"$z^2 = {ctex(w)}$; $|z|^2 = {d}$.", f"Result: ${ctex(v)}$."], "answering 1.")


@reg(S, "basics")
def cxa_real_part_product(r):
    z, w = rz(r), rz(r)
    pr = cmul(z, w)
    part = r.choice(["real", "imaginary"])
    v = pr[0] if part == "real" else pr[1]
    p = f"What is the {part} part of $({ctex(z)})({ctex(w)})$?"
    return Q(p, v, [z[0] * w[0] + z[1] * w[1] if part == "real" else z[0] * w[1] - z[1] * w[0], -v if v else 1, z[0] * w[0] if part == "real" else z[1] * w[1], pr[1] if part == "real" else pr[0], v + 2], "Expand with FOIL.",
             f"the {part} part.", "$(a + bi)(c + di) = (ac - bd) + (ad + bc)i$.", [f"Product: ${ctex(pr)}$.", f"{part.capitalize()} part: ${v}$."], "using $+bd$ in the real part.") if v not in (pr[1] if part == "real" else pr[0],) else None


@reg(S, "basics")
def cxa_midpoint(r):
    z, w = rz(r), rz(r)
    m = (F(z[0] + w[0], 2), F(z[1] + w[1], 2))
    p = f"What complex number is the midpoint of ${ctex(z)}$ and ${ctex(w)}$?"
    return Q(p, CZ(m), [CZ((z[0] + w[0], z[1] + w[1])), CZ((F(z[0] - w[0], 2), F(z[1] - w[1], 2))), CZ((m[0], -m[1])) if m[1] else CZ((m[0] + 1, 1)), CZ((m[1], m[0])) if m[0] != m[1] else CZ((m[0], m[1] + 1)), CZ((m[0] + 1, m[1]))], "Average the two numbers.",
             "the midpoint.", "$\\frac{z + w}{2}$.", [f"$\\frac{{{ctex((z[0] + w[0], z[1] + w[1]))}}}{{2}} = {ctex(m)}$."], "not dividing by 2.") if (z[0] + w[0], z[1] + w[1]) != (0, 0) else None


@reg(S, "challenge")
def cxac_power_conj(r):
    n = r.randint(2, 8)
    p = f"How many complex numbers $z$ satisfy $z^{{{n}}} = \\overline{{z}}$?"
    return Q(p, n + 2, [n + 1, n, n - 1, 2 * n, n + 3], "Take moduli first.",
             "the count.", f"$|z|^{{{n}}} = |z|$, so $z = 0$ or $|z| = 1$. If $|z| = 1$, $\\overline{{z}} = \\frac{{1}}{{z}}$ and $z^{{{n + 1}}} = 1$.",
             [f"$z = 0$, plus the ${n + 1}$ roots of $z^{{{n + 1}}} = 1$: ${n + 2}$."], "forgetting $z = 0$.")


@reg(S, "challenge")
def cxac_weighted_powers(r):
    n = r.randint(5, 30)
    s = (0, 0)
    pw = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}
    for k in range(1, n + 1):
        s = (s[0] + k * pw[k % 4][0], s[1] + k * pw[k % 4][1])
    p = f"What is $i + 2i^2 + 3i^3 + \\cdots + {n}i^{{{n}}}$?"
    return Q(p, CZ(s), [CZ((s[1], s[0])) if s[0] != s[1] else CZ((s[0] + 1, s[1])), CZ((-s[0], -s[1])) if s != (0, 0) else CZ((1, 1)), CZ((s[0], -s[1])) if s[1] else CZ((s[0], 2)), CZ((s[0] + 2, s[1] - 2)), CZ((s[0] - 2, s[1]))], "Group the terms in blocks of 4.",
             "the sum.", "each block $ki^k + (k+1)i^{k+1} + (k+2)i^{k+2} + (k+3)i^{k+3}$ for $k \\equiv 1 \\pmod 4$ equals $(-(k+1) + (k+3)) + (k - (k+2))i = 2 - 2i$.",
             [f"Full blocks: ${n // 4}$, giving ${ctex((2 * (n // 4), -2 * (n // 4)))}$." if n >= 4 else "No full blocks.", f"Adding the leftover terms: ${ctex(s)}$."], "assuming the sum is 0 like $i + i^2 + i^3 + i^4$.")


@reg(S, "challenge")
def cxac_mod_eq(r):
    x, y = r.randint(-6, 6), r.randint(1, 6) * r.choice([1, -1])
    a = x * x + y * y + x
    p = f"A complex number $z$ satisfies $|z|^2 + z = {ctex((a, y))}$ and $\\text{{Re}}(z) > {x - 1 if x * x + y * y + x == a else 0}$ . What is $|z|^2$?"
    # need uniqueness of positive real-part root: x^2 + x + y^2 - a = 0 has roots x and -1-x
    other = -1 - x
    if other == x:
        return None
    pick = x
    cond = f"\\text{{Re}}(z) {'>' if x > other else '<'} {ft(F(x + other, 2))}"
    p = f"A complex number $z$ satisfies $|z|^2 + z = {ctex((a, y))}$ and ${cond}$. What is $|z|^2$?"
    v = x * x + y * y
    return Q(p, v, [other ** 2 + y ** 2 if other ** 2 + y ** 2 != v else v + 1, a, v + 1, y * y, abs(v - 2) if abs(v - 2) != v else v + 3], "Let $z = x + yi$; $|z|^2$ is real.",
             "$|z|^2$.", f"the imaginary part gives $y = {y}$; the real part gives $x^2 + {y * y} + x = {a}$.",
             [f"$x^2 + x - {a - y * y} = 0$ has roots ${x}$ and ${other}$; the condition picks $x = {x}$.", f"$|z|^2 = {x * x} + {y * y} = {v}$."], "taking the wrong root.")


@reg(S, "challenge")
def cxac_triangle(r):
    z, w = rz(r, -8, 8), rz(r, -8, 8)
    A = F(abs(z[0] * w[1] - z[1] * w[0]), 2)
    if A == 0:
        return None
    p = f"What is the area of the triangle with vertices $0$, ${ctex(z)}$, and ${ctex(w)}$ in the complex plane?"
    return Q(p, A, [2 * A, F(abs(z[0] * w[0] + z[1] * w[1]), 2) if F(abs(z[0] * w[0] + z[1] * w[1]), 2) != A else A + 1, A + 1, F(abs(z[0] * w[1] + z[1] * w[0]), 2) if F(abs(z[0] * w[1] + z[1] * w[0]), 2) != A else A + 2, A / 2], "Shoelace formula.",
             "the area.", "area $= \\frac{1}{2}|x_1 y_2 - x_2 y_1|$, which is $\\frac{1}{2}|\\text{Im}(\\overline{z}w)|$.",
             [f"$\\frac{{1}}{{2}}|{par(z[0])} \\cdot {par(w[1])} - {par(w[0])} \\cdot {par(z[1])}| = {ft(A)}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "challenge")
def cxac_count_reps(r):
    n = r.choice([5, 10, 13, 25, 50, 65, 85, 100, 125, 169, 9, 18, 45, 29])
    cnt = sum(1 for a in range(-n, n + 1) for b in range(-n, n + 1) if a * a + b * b == n)
    p = f"How many complex numbers $z = a + bi$ with $a$ and $b$ integers satisfy $z\\overline{{z}} = {n}$?"
    return Q(p, cnt, [cnt + 4, cnt // 2 if cnt // 2 != cnt else cnt + 8, cnt - 4 if cnt > 4 else cnt + 2, cnt * 2, cnt + 1], "Count lattice points on $a^2 + b^2 = " + str(n) + "$.",
             "the count.", "find all $(a, b)$ with $a^2 + b^2 = " + str(n) + "$, including signs and order.",
             [f"Checking each $a$ from $0$ up to $\\sqrt{{{n}}}$ and counting sign and order choices: ${cnt}$."], "forgetting negative values.")


@reg(S, "challenge")
def cxac_sum_sq(r):
    a, b = rz(r, -6, 6), rz(r, -6, 6)
    s, pr = (a[0] + b[0], a[1] + b[1]), cmul(a, b)
    s2 = cmul(s, s)
    v = (s2[0] - 2 * pr[0], s2[1] - 2 * pr[1])
    p = f"Complex numbers $z$ and $w$ satisfy $z + w = {ctex(s)}$ and $zw = {ctex(pr)}$. What is $z^2 + w^2$?"
    return Q(p, CZ(v), [CZ(s2), CZ((s2[0] + 2 * pr[0], s2[1] + 2 * pr[1])), CZ((v[0], -v[1])) if v[1] else CZ((v[0] + 1, 1)), CZ((s2[0] - pr[0], s2[1] - pr[1])), CZ((v[0] + 2, v[1]))], "$z^2 + w^2 = (z + w)^2 - 2zw$.",
             "$z^2 + w^2$.", "the same identity as for real numbers.", [f"$(z + w)^2 = {ctex(s2)}$.", f"Subtract $2zw = {ctex((2 * pr[0], 2 * pr[1]))}$: ${ctex(v)}$."], "forgetting the factor of 2.") if s != (0, 0) else None


@reg(S, "challenge")
def cxac_min_mod(r):
    a, b = r.choice([(3, 4), (5, 12), (8, 15), (6, 8), (9, 12), (7, 24)])
    a *= r.choice([1, -1])
    m = math.isqrt(a * a + b * b)
    rr = r.randint(1, m - 1)
    ask = r.choice(["min", "max"])
    v = m - rr if ask == "min" else m + rr
    p = f"Complex number $z$ satisfies $|z - ({ctex((a, b))})| = {rr}$. What is the {'smallest' if ask == 'min' else 'largest'} possible value of $|z|$?"
    return Q(p, v, [m + rr if ask == "min" else m - rr, m, rr, v + 1, abs(a) + b - rr], "$z$ lies on a circle.",
             "the extreme modulus.", f"the circle has center ${ctex((a, b))}$ (distance ${m}$ from the origin) and radius ${rr}$.",
             [f"Along the line through the origin: ${m} {'-' if ask == 'min' else '+'} {rr} = {v}$."], "using the wrong direction.")


# ================================================================ cx_polar
S = "cx_polar"


def cis_rect(rr, d):
    return rr * cosd(d), rr * sind(d)


def EX(x):
    return ex(x) if abs(x) > 1e-12 else C("0", 0)


def ztex(rr, d):
    """r cis d in a + bi form, for standard angles."""
    a, b = cis_rect(rr, d)
    at, bt = rex(a), rex(abs(b))
    if abs(b) < 1e-9:
        return at
    bt2 = "i" if bt == "1" else f"{bt}i"
    if abs(a) < 1e-9:
        return ("-" if b < 0 else "") + bt2
    return f"{at} {'+' if b > 0 else '-'} {bt2}"


def rex(x):
    """Exact form of x = k or k*sqrt(2) or k*sqrt(3), k rational with small denominators."""
    for m in (1, 2, 3):
        k = x / math.sqrt(m)
        q = F(k).limit_denominator(8)
        if abs(float(q) - k) < 1e-9:
            if m == 1:
                return ft(q)
            return rad(q, m).tex
    raise ValueError(x)


@reg(S, "basics")
def cp_to_rect(r):
    rr = r.choice([2, 4, 6, 8])
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
    if d % 90 == 45:
        rr = r.choice([2, 4]) * 1
    a, b = cis_rect(rr, d)
    try:
        t = ztex(rr, d)
    except ValueError:
        return None
    ans = C(t, a * 100 + b)
    wr = []
    for dd in (d + 90, d + 180, 360 - d, 90 - d if d < 90 else d - 90 + 30):
        try:
            wr.append(C(ztex(rr, dd % 360), cis_rect(rr, dd % 360)[0] * 100 + cis_rect(rr, dd % 360)[1]))
        except ValueError:
            pass
    try:
        wr.append(C(ztex(rr, (d + 30) % 360), cis_rect(rr, d + 30)[0] * 100 + cis_rect(rr, d + 30)[1]))
    except ValueError:
        pass
    p = f"Write ${rr}(\\cos {d}^\\circ + i\\sin {d}^\\circ)$ in the form $a + bi$."
    return Q(p, ans, wr, "$a = r\\cos\\theta$, $b = r\\sin\\theta$.",
             "the rectangular form.", "multiply out with exact values.", [f"$\\cos {d}^\\circ = {EX(cosd(d)).tex}$, $\\sin {d}^\\circ = {EX(sind(d)).tex}$.", f"Result: ${t}$."], "swapping sine and cosine.")


@reg(S, "basics")
def cp_mod_product(r):
    z, w = r.choice([(3, 4), (5, 12), (6, 8), (1, 1), (8, 15)]), r.choice([(3, 4), (5, 12), (1, 2), (2, 2), (7, 24)])
    mz2, mw2 = z[0] ** 2 + z[1] ** 2, w[0] ** 2 + w[1] ** 2
    ans = rad(1, mz2 * mw2)
    p = f"What is $|({ctex(z)})({ctex(w)})|$?"
    return Q(p, ans, [rad(1, mz2 + mw2), num(mz2 * mw2), rad(1, mz2 * mw2 + 1), rad(2, mz2 * mw2) if mz2 * mw2 < 400 else num(3), num(z[0] * w[0] + z[1] * w[1])], "$|zw| = |z||w|$.",
             "the modulus.", "multiply the moduli.", [f"$|{ctex(z)}| = {rad(1, mz2).tex}$, $|{ctex(w)}| = {rad(1, mw2).tex}$.", f"Product: ${ans.tex}$."], "adding the moduli.")


@reg(S, "basics")
def cp_arg_product(r):
    a, b = r.randint(10, 350), r.randint(10, 350)
    op = r.choice(["*", "/"])
    v = (a + b) % 360 if op == "*" else (a - b) % 360
    p = f"If $\\arg z = {a}^\\circ$ and $\\arg w = {b}^\\circ$, what is $\\arg\\left({'zw' if op == '*' else '\\frac{z}{w}'}\\right)$, between $0^\\circ$ and $360^\\circ$?"
    alt = (a - b) % 360 if op == "*" else (a + b) % 360
    return Q(p, DG(v), [DG(alt) if alt != v else DG((v + 90) % 360), DG(a * b % 360) if a * b % 360 != v else DG((v + 45) % 360), DG((v + 180) % 360), DG((360 - v) % 360) if (360 - v) % 360 != v else DG((v + 30) % 360), DG((v + 10) % 360)], "Multiplying adds arguments; dividing subtracts.",
             "the argument.", "use the polar form.", [f"${a} {'+' if op == '*' else '-'} {b} = {a + b if op == '*' else a - b}$, which reduces to ${v}^\\circ$."], "multiplying the angles.") if v else None


@reg(S, "basics")
def cp_power_arg(r):
    d = r.choice([15, 20, 25, 35, 40, 50, 70, 75, 80, 110])
    n = r.randint(3, 15)
    v = (d * n) % 360
    rr = r.randint(1, 3)
    p = f"If $z = " + (f"{rr}(\\cos {d}^\\circ + i\\sin {d}^\\circ)" if rr > 1 else f"\\cos {d}^\\circ + i\\sin {d}^\\circ") + f"$, what is the argument of $z^{{{n}}}$, between $0^\\circ$ and $360^\\circ$?"
    return Q(p, DG(v), [DG(d * n) if d * n != v else DG((v + 90) % 360), DG((d + n) % 360), DG((v + 180) % 360), DG((360 - v) % 360) if (360 - v) % 360 != v else DG((v + 45) % 360), DG(d)], "De Moivre's Theorem.",
             "the argument.", "$(r\\,\\text{cis}\\,\\theta)^n = r^n\\,\\text{cis}(n\\theta)$.", [f"${n} \\cdot {d} = {d * n}$, which reduces to ${v}^\\circ$."], "adding instead of multiplying.") if v else None


@reg(S, "basics")
def cp_mod_power_ratio(r):
    z, w = r.choice([(1, 1), (3, 4), (1, 2), (2, 1)]), r.choice([(1, 1), (1, 3), (3, 4), (2, 2)])
    m, n = r.randint(2, 6), r.randint(2, 6)
    v = F(z[0] ** 2 + z[1] ** 2) ** m / F(w[0] ** 2 + w[1] ** 2) ** n
    s = 1
    try:
        val = F(math.isqrt(v.numerator), math.isqrt(v.denominator))
        if val * val != v or val == 1:
            return None
    except ValueError:
        return None
    p = f"What is $\\left|\\dfrac{{({ctex(z)})^{{{m}}}}}{{({ctex(w)})^{{{n}}}}}\\right|$?"
    return Q(p, val, [v, val * 2, val / 2, val + 1, F(1) / val if F(1) / val != val else val + 2], "Moduli multiply and divide.",
             "the modulus.", "$|z^m/w^n| = |z|^m/|w|^n$.", [f"$|{ctex(z)}|^{{{m}}} / |{ctex(w)}|^{{{n}}} = {ft(val)}$."], "squaring when you shouldn't.")


@reg(S, "basics")
def cp_euler(r):
    d = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300, 330])
    part = r.choice(["real", "imaginary"])
    v = cosd(d) if part == "real" else sind(d)
    p = f"What is the {part} part of $e^{{i{deg_rad(d)}}}$?"
    return Q(p, EX(v), exw(v, r) if abs(v) > 1e-9 else [ex(.5), ex(1), ex(-1), ex(R2_ := math.sqrt(2) / 2), ex(-.5)], "$e^{i\\theta} = \\cos\\theta + i\\sin\\theta$.",
             f"the {part} part.", "Euler's formula.", [f"$\\{'cos' if part == 'real' else 'sin'}\\left({deg_rad(d)}\\right) = {EX(v).tex}$."], "mixing up sine and cosine.")


@reg(S, "basics")
def cp_conj_arg(r):
    d = r.randint(5, 355)
    op = r.choice(["conj", "neg", "inv"])
    v = {"conj": (360 - d) % 360, "neg": (d + 180) % 360, "inv": (360 - d) % 360}[op]
    form = {"conj": "\\overline{z}", "neg": "-z", "inv": "\\frac{1}{z}"}[op]
    p = f"If $\\arg z = {d}^\\circ$, what is $\\arg\\left({form}\\right)$, between $0^\\circ$ and $360^\\circ$?"
    return Q(p, DG(v), [DG(d), DG((d + 180) % 360) if op != "neg" else DG((360 - d) % 360), DG((180 - d) % 360) if (180 - d) % 360 != v else DG((v + 90) % 360), DG((d + 90) % 360), DG((v + 45) % 360)], "Picture the reflection.",
             "the argument.", {"conj": "conjugation reflects across the real axis.", "neg": "negation rotates by $180^\\circ$.", "inv": "$\\frac{1}{z} = \\frac{\\overline{z}}{|z|^2}$ has the same argument as $\\overline{z}$."}[op],
             [f"Result: ${v}^\\circ$."], "confusing conjugation with negation.") if d != 180 else None


@reg(S, "basics")
def cp_reciprocal_mod(r):
    rr = r.randint(2, 9)
    d = r.randint(10, 80)
    k = r.randint(1, 3)
    v = F(1, rr ** k)
    p = f"If $z = {rr}(\\cos {d}^\\circ + i\\sin {d}^\\circ)$, what is $\\left|z^{{-{k}}}\\right|$?".replace("^{-1}", "^{-1}")
    return Q(p, v, [F(rr ** k), F(1, rr * k), F(-rr ** k), v * 2, F(1, rr ** (k + 1))], "$|z^{-k}| = |z|^{-k}$.",
             "the modulus.", "negative powers invert the modulus.", [f"$\\frac{{1}}{{{rr}^{{{k}}}}} = {ft(v)}$."], "making the modulus negative.")


@reg(S, "basics")
def cp_sum_units(r):
    a, b = r.choice([(0, 60), (0, 90), (0, 120), (30, 90), (45, 135), (10, 70), (20, 140), (0, 180), (40, 100)])
    v = 2 * abs(cosd((b - a) / 2))
    p = f"What is $|\\text{{cis}}\\,{a}^\\circ + \\text{{cis}}\\,{b}^\\circ|$? (Here $\\text{{cis}}\\,\\theta = \\cos\\theta + i\\sin\\theta$.)"
    return Q(p, EX(v), exw(v, r) if v > 1e-9 else [ex(1), ex(2), ex(math.sqrt(2)), ex(math.sqrt(3)), ex(.5)], "Two unit vectors with an angle between them.",
             "the modulus.", f"$|\\text{{cis}}\\,\\alpha + \\text{{cis}}\\,\\beta| = 2\\left|\\cos\\frac{{\\beta - \\alpha}}{{2}}\\right|$.", [f"$2|\\cos {ft(F(b - a, 2))}^\\circ| = {EX(v).tex}$."], "adding the moduli to get 2.")


@reg(S, "basics")
def cp_cube_root_mod(r):
    n = r.randint(2, 5)
    m = r.randint(2, 4)
    big_ = m ** n
    w = r.choice([f"{big_}i", f"-{big_}", f"{big_}", f"-{big_}i"])
    p = f"What is the modulus of each solution of $z^{{{n}}} = {w}$?"
    return Q(p, m, [big_, m * n, F(big_, n), m + 1, n], "$|z|^{" + str(n) + "} = |" + w + "|$.",
             "the modulus.", "all the roots lie on one circle.", [f"$|z| = \\sqrt[{n}]{{{big_}}} = {m}$."], "dividing by " + str(n) + ".")


@reg(S, "basics")
def cp_arg_power_std(r):
    base, d = r.choice([("1 + i", 45), ("1 + i\\sqrt{3}", 60), ("\\sqrt{3} + i", 30), ("-1 + i", 135), ("1 - i", 315), ("-\\sqrt{3} + i", 150)])
    n = r.randint(2, 11)
    v = (d * n) % 360
    p = f"What is the argument of $({base})^{{{n}}}$, between $0^\\circ$ and $360^\\circ$?"
    return Q(p, DG(v), [DG(d), DG((v + 180) % 360), DG((d + n) % 360), DG((360 - v) % 360) if (360 - v) % 360 != v else DG((v + 90) % 360), DG((v + 30) % 360)], "Find the argument of the base first.",
             "the argument.", f"$\\arg({base}) = {d}^\\circ$; powers multiply the argument.", [f"${n} \\cdot {d} = {n * d}$, reducing to ${v}^\\circ$."], "forgetting to reduce mod $360^\\circ$.") if v else None


@reg(S, "basics")
def cp_product_three(r):
    a, b, c = r.randint(5, 100), r.randint(5, 100), r.randint(5, 100)
    s = a + b + c
    tgt = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300])
    c = tgt - a - b
    while c <= 0:
        c += 360
    s = a + b + c
    part = r.choice(["real", "imaginary"])
    v = cosd(s) if part == "real" else sind(s)
    p = f"What is the {part} part of $\\text{{cis}}\\,{a}^\\circ \\cdot \\text{{cis}}\\,{b}^\\circ \\cdot \\text{{cis}}\\,{c}^\\circ$?"
    return Q(p, EX(v), exw(v, r) if abs(v) > 1e-9 else [ex(1), ex(-1), ex(.5), ex(-.5), ex(math.sqrt(3) / 2)], "Add the angles.",
             f"the {part} part.", "$\\text{cis}\\,\\alpha \\cdot \\text{cis}\\,\\beta = \\text{cis}(\\alpha + \\beta)$.", [f"${a} + {b} + {c} = {s}^\\circ$.", f"Answer: ${EX(v).tex}$."], "multiplying the angles.")


@reg(S, "basics")
def cp_imag_power(r):
    d = r.choice([10, 15, 20, 30, 40, 45, 50, 75])
    n = r.randint(2, 12)
    s = (d * n) % 360
    if s % 30 and s % 45:
        return None
    part = r.choice(["real", "imaginary"])
    v = cosd(s) if part == "real" else sind(s)
    p = f"What is the {part} part of $(\\cos {d}^\\circ + i\\sin {d}^\\circ)^{{{n}}}$?"
    return Q(p, EX(v), exw(v, r) if abs(v) > 1e-9 else [ex(1), ex(-1), ex(.5), ex(-.5), ex(math.sqrt(2) / 2)], "De Moivre's Theorem.",
             f"the {part} part.", f"the power is $\\cos {d * n}^\\circ + i\\sin {d * n}^\\circ$.", [f"${d * n}^\\circ \\equiv {s}^\\circ$.", f"Answer: ${EX(v).tex}$."], "raising sine and cosine separately to the power.")


@reg(S, "basics")
def cp_mod_one(r):
    z = rz(r, -9, 9)
    p = f"What is $\\left|\\dfrac{{{ctex(z)}}}{{{ctex((z[0], -z[1]))}}}\\right|^{{{r.randint(2, 9)}}}$?"
    return Q(p, 1, [0, z[0] ** 2 + z[1] ** 2, -1, 2, F(1, 2)], "A number and its conjugate have the same modulus.",
             "the value.", "$|z| = |\\overline{z}|$, so the ratio has modulus $1$.", ["$1$ to any power is $1$."], "computing the quotient by hand and making an arithmetic slip.")


@reg(S, "basics")
def cp_polar_angle(r):
    zt, d = r.choice([("-1 + i", 135), ("-1 - i", 225), ("1 - i", 315), ("-2 + 2i", 135), ("3 - 3i", 315), ("-1 + i\\sqrt{3}", 120), ("-1 - i\\sqrt{3}", 240), ("1 - i\\sqrt{3}", 300),
                      ("-\\sqrt{3} + i", 150), ("-\\sqrt{3} - i", 210), ("\\sqrt{3} - i", 330), ("-5i", 270), ("-4", 180)])
    base = d % 90 if d % 90 else 90
    p = f"The number ${zt}$ equals $r(\\cos\\theta + i\\sin\\theta)$ with $r > 0$ and $0^\\circ \\le \\theta < 360^\\circ$. What is $\\theta$?"
    return Q(p, DG(d), [DG((d + 90) % 360), DG((d + 180) % 360), DG((360 - d) % 360) if (360 - d) % 360 != d else DG(90), DG((180 - d) % 360) if (180 - d) % 360 != d else DG(45), DG((d + 30) % 360)], "Check the quadrant.",
             "$\\theta$.", "find the reference angle from the ratio of the parts, then place it in the right quadrant.",
             [f"${zt}$ is at angle ${d}^\\circ$ (check the signs of the real and imaginary parts)."], "using the reference angle without adjusting for the quadrant.")


@reg(S, "basics")
def cp_mult_polar(r):
    r1, r2 = r.randint(1, 4), r.randint(1, 4)
    tgt = r.choice([30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])
    a = r.randint(5, tgt - 5) if tgt > 10 else 5
    b = tgt - a
    rr = r1 * r2
    try:
        t = ztex(rr, tgt)
        wr = [C(ztex(rr, x), cis_rect(rr, x)[0] * 100 + cis_rect(rr, x)[1]) for x in ((tgt + 90) % 360, (tgt + 180) % 360, (360 - tgt) % 360)]
        wr.append(C(ztex(r1 + r2, tgt), cis_rect(r1 + r2, tgt)[0] * 100 + cis_rect(r1 + r2, tgt)[1]) if r1 + r2 != rr else C(ztex(rr + 1, tgt), cis_rect(rr + 1, tgt)[0] * 100 + cis_rect(rr + 1, tgt)[1]))
    except ValueError:
        return None
    p = f"What is ${r1 if r1 > 1 else ''}(\\cos {a}^\\circ + i\\sin {a}^\\circ) \\cdot {r2 if r2 > 1 else ''}(\\cos {b}^\\circ + i\\sin {b}^\\circ)$ in the form $a + bi$?"
    return Q(p, C(t, cis_rect(rr, tgt)[0] * 100 + cis_rect(rr, tgt)[1]), wr, "Multiply moduli, add angles.",
             "the product.", "$r_1\\,\\text{cis}\\,\\alpha \\cdot r_2\\,\\text{cis}\\,\\beta = r_1 r_2\\,\\text{cis}(\\alpha + \\beta)$.",
             [f"Modulus ${rr}$, angle ${a} + {b} = {tgt}^\\circ$.", f"${rr}(\\cos {tgt}^\\circ + i\\sin {tgt}^\\circ) = {t}$."], "adding the moduli.")


@reg(S, "challenge")
def cpc_binomial_conj(r):
    n = r.choice([2, 4, 6, 8, 10, 12, 3, 5, 7, 9])
    v = round(2 * 2 ** (n / 2) * cosd(45 * n))
    p = f"What is $(1 + i)^{{{n}}} + (1 - i)^{{{n}}}$?"
    return Q(p, v, [v * 2 if v else 2, -v if v else 4, 2 ** n, 2 ** (n // 2), v + 2], "The two terms are conjugates.",
             "the sum.", f"$(1 + i)^{{{n}}} = 2^{{{n}/2}}\\,\\text{{cis}}({45 * n}^\\circ)$; adding the conjugate doubles the real part.",
             [f"$2 \\cdot 2^{{{n}/2}} \\cos {45 * n}^\\circ = {v}$."], "adding the imaginary parts too.")


@reg(S, "challenge")
def cpc_mixed_arg(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    v = (45 * a + 30 * b) % 360
    p = f"What is the argument of $(1 + i)^{{{a}}}(\\sqrt{{3}} + i)^{{{b}}}$, between $0^\\circ$ and $360^\\circ$?"
    return Q(p, DG(v), [DG((45 * b + 30 * a) % 360) if (45 * b + 30 * a) % 360 != v else DG((v + 15) % 360), DG((v + 180) % 360), DG((45 + 30) * (a + b) % 360) if (75 * (a + b)) % 360 != v else DG((v + 90) % 360), DG((360 - v) % 360) if (360 - v) % 360 != v else DG((v + 60) % 360), DG((v + 30) % 360)], "Arguments add when multiplying.",
             "the argument.", "$\\arg(1 + i) = 45^\\circ$ and $\\arg(\\sqrt{3} + i) = 30^\\circ$.", [f"${a} \\cdot 45 + {b} \\cdot 30 = {45 * a + 30 * b}$, which reduces to ${v}^\\circ$."], "mixing up the two arguments.") if v else None


@reg(S, "challenge")
def cpc_mod_sum(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    ang = r.choice([60, 90, 120])
    v2 = a * a + b * b + 2 * a * b * cosd(ang)
    v2 = round(v2)
    p = f"Complex numbers $z$ and $w$ have $|z| = {a}$, $|w| = {b}$, and the angle between them (as vectors from $0$) is ${ang}^\\circ$. What is $|z + w|$?"
    alt = round(a * a + b * b - 2 * a * b * cosd(ang))
    return Q(p, rad(1, v2), [rad(1, alt) if alt != v2 and alt > 0 else num(a + b + 1), num(a + b), rad(1, a * a + b * b) if a * a + b * b != v2 else num(abs(a - b) + 1), rad(1, v2 + 1), num(abs(a - b))], "Parallelogram rule.",
             "$|z + w|$.", "$|z + w|^2 = |z|^2 + |w|^2 + 2|z||w|\\cos\\theta$.", [f"${a * a} + {b * b} + 2 \\cdot {a} \\cdot {b} \\cos {ang}^\\circ = {v2}$.", f"$|z + w| = {rad(1, v2).tex}$."], "using the minus sign (that gives $|z - w|$).")


@reg(S, "challenge")
def cpc_imag_1i(r):
    n = r.randint(3, 20)
    z = (1, 0)
    for _ in range(n):
        z = cmul(z, (1, 1))
    part = r.choice(["real", "imaginary"])
    v = z[0] if part == "real" else z[1]
    p = f"What is the {part} part of $(1 + i)^{{{n}}}$?"
    return Q(p, v, [-v if v else 2 ** (n // 2), z[1] if part == "real" and z[1] != v else (z[0] if z[0] != v else v + 1), 2 ** (n // 2) if 2 ** (n // 2) != abs(v) else 2 ** (n // 2 + 1), 2 ** n, v + 2], "Write $1 + i = \\sqrt{2}\\,\\text{cis}\\,45^\\circ$.",
             f"the {part} part.", f"$(1 + i)^{{{n}}} = 2^{{{n}/2}}\\,\\text{{cis}}({45 * n}^\\circ)$.", [f"That equals ${ctex(z)}$.", f"{part.capitalize()} part: ${v}$."], "using $2^" + str(n) + "$ for the modulus.")


@reg(S, "challenge")
def cpc_rotate_about(r):
    z, c = rz(r, -6, 6), rz(r, -4, 4)
    k = r.choice([1, 2, 3])
    rot = {1: (0, 1), 2: (-1, 0), 3: (0, -1)}[k]
    d = (z[0] - c[0], z[1] - c[1])
    w = cmul(d, rot)
    w = (w[0] + c[0], w[1] + c[1])
    p = f"The point ${ctex(z)}$ is rotated ${90 * k}^\\circ$ counterclockwise about ${ctex(c)}$. What is its image?"
    w2 = cmul(z, rot)
    return Q(p, CZ(w), [CZ(w2) if w2 != w else CZ((w[0] + 1, w[1])), CZ((w[0] - c[0], w[1] - c[1])) if (w[0] - c[0], w[1] - c[1]) != w else CZ((w[0], w[1] + 1)), CZ((cmul(d, (rot[0], -rot[1]))[0] + c[0], cmul(d, (rot[0], -rot[1]))[1] + c[1])) if k != 2 else CZ((w[0] + 2, w[1])), CZ((w[0], w[1] - 2)), CZ((w[1], w[0])) if w[0] != w[1] else CZ((w[0] + 3, w[1]))], "Translate so the center is at 0, rotate, translate back.",
             "the image.", f"$w = c + i^{{{k}}}(z - c)$.", [f"$z - c = {ctex(d)}$.", f"Rotate: ${ctex(cmul(d, rot))}$.", f"Add back $c$: ${ctex(w)}$."], "rotating about the origin.") if d != (0, 0) else None


@reg(S, "challenge")
def cpc_unit_product(r):
    n = r.randint(5, 40)
    v = n * (n + 1) // 2 % 360
    p = f"What is the argument of $\\text{{cis}}\\,1^\\circ \\cdot \\text{{cis}}\\,2^\\circ \\cdots \\text{{cis}}\\,{n}^\\circ$, between $0^\\circ$ and $360^\\circ$?"
    return Q(p, DG(v), [DG(n % 360), DG((v + 180) % 360), DG(math.factorial(n) % 360) if math.factorial(n) % 360 != v else DG((v + 90) % 360), DG((360 - v) % 360) if (360 - v) % 360 != v else DG((v + 45) % 360), DG((v + 1) % 360)], "Add the angles.",
             "the argument.", f"$1 + 2 + \\cdots + {n} = {n * (n + 1) // 2}$.", [f"Reduced mod $360$: ${v}^\\circ$."], "multiplying the angles.") if v else None


@reg(S, "challenge")
def cpc_root_args(r):
    n = r.randint(2, 6)
    d = r.choice([60, 90, 120, 180, 240, 270])
    roots = [(d + 360 * k) / n for k in range(n)]
    s = sum(roots)
    if abs(s - round(s)) > 1e-9:
        return None
    s = round(s)
    p = f"The solutions of $z^{{{n}}} = \\text{{cis}}\\,{d}^\\circ$ are $\\text{{cis}}\\,\\theta_k$ with $0^\\circ \\le \\theta_k < 360^\\circ$. What is the sum of the $\\theta_k$?"
    return Q(p, s, [s + 360, round(d / n), d, 180 * (n - 1), s - 180 if s > 180 else s + 180], "The roots are equally spaced by $\\frac{360^\\circ}{" + str(n) + "}$.",
             "the sum of the angles.", f"$\\theta_k = \\frac{{{d} + 360k}}{{{n}}}$ for $k = 0, \\ldots, {n - 1}$.",
             ["Angles: " + ", ".join(f"${round(t, 2) if t != int(t) else int(t)}^\\circ$" for t in roots) + ".", f"Sum: ${s}^\\circ$."], "only using one root.")


# ================================================================ cx_roots_unity
S = "cx_roots_unity"


@reg(S, "basics")
def ru_product_all(r):
    n = r.randint(2, 12)
    v = (-1) ** (n + 1)
    p = f"What is the product of all ${n}$ solutions of $z^{{{n}}} = 1$?"
    return Q(p, v, [-v, 0, n, F(1, n), 2], "Vieta: the product of the roots of $z^n - 1$.",
             "the product.", f"for $z^{{{n}}} - 1 = 0$, the product of roots is $(-1)^{{{n}}} \\cdot (-1) = (-1)^{{{n + 1}}}$.", [f"$(-1)^{{{n + 1}}} = {v}$."], "assuming the product is always 1.")


@reg(S, "basics")
def ru_omega_expr(r):
    e, v = r.choice([("(1 + \\omega)(1 + \\omega^2)", 1), ("(1 - \\omega)(1 - \\omega^2)", 3), ("(1 + \\omega)^3", -1), ("\\omega + \\omega^2", -1), ("(1 + \\omega^2)^3", -1), ("(1 - \\omega)^2(1 - \\omega^2)^2", 9), ("\\omega^2 + \\omega^4 + \\omega^6", 0)])
    p = f"Let $\\omega \\ne 1$ satisfy $\\omega^3 = 1$. What is ${e}$?"
    return Q(p, v, [x for x in (-1, 0, 1, 2, 3, 9, -3) if x != v][:5], "Use $\\omega^2 + \\omega + 1 = 0$ and $\\omega^3 = 1$.",
             "the value.", "reduce powers mod 3 and replace $1 + \\omega$ with $-\\omega^2$ (and so on).", [f"Simplifying gives ${v}$."], "treating $\\omega$ as 1.")


@reg(S, "basics")
def ru_real_count(r):
    n = r.randint(2, 20)
    rhs = r.choice([1, -1])
    cnt = (2 if n % 2 == 0 else 1) if rhs == 1 else (0 if n % 2 == 0 else 1)
    p = f"How many real solutions does $z^{{{n}}} = {rhs}$ have?"
    return Q(p, cnt, [x for x in (0, 1, 2, n, 3) if x != cnt] + ([4] if cnt in (0, 1, 2, 3) and n in (0, 1, 2, 3) else []), "Real solutions are $\\pm 1$ at most.",
             "the count.", "check $z = 1$ and $z = -1$.", [f"$1^{{{n}}} = 1$ and $(-1)^{{{n}}} = {(-1) ** n}$.", f"Real solutions: ${cnt}$."], "counting all " + str(n) + " roots.")


@reg(S, "basics")
def ru_primitive(r):
    n = r.randint(3, 30)
    phi = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
    p = f"How many solutions of $z^{{{n}}} = 1$ are not solutions of $z^m = 1$ for any positive $m < {n}$?"
    return Q(p, phi, [n - 1, n, phi + 1, n // 2, phi - 1 if phi > 1 else 3], "These are the primitive roots.",
             "the count.", f"$\\text{{cis}}\\frac{{360^\\circ k}}{{{n}}}$ is primitive exactly when $\\gcd(k, {n}) = 1$.", [f"$\\varphi({n}) = {phi}$."], "counting all roots except 1.")


@reg(S, "basics")
def ru_filter_sum(r):
    n = r.randint(2, 40)
    v = 3 if n % 3 == 0 else 0
    p = f"Let $\\omega \\ne 1$ with $\\omega^3 = 1$. What is $1 + \\omega^{{{n}}} + \\omega^{{{2 * n}}}$?"
    return Q(p, v, [x for x in (0, 3, 1, -1, 2, n) if x != v][:5], "Reduce $" + str(n) + "$ mod 3.",
             "the value.", "if $3 \\mid n$ every term is 1; otherwise the terms are $1, \\omega, \\omega^2$ in some order.", [f"${n} \\equiv {n % 3} \\pmod 3$, so the sum is ${v}$."], "answering 0 every time.")


@reg(S, "basics")
def ru_half_plane(r):
    n = r.randint(3, 16)
    cond = r.choice(["re", "im", "both"])
    roots = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    test = {"re": lambda x, y: x > 1e-9, "im": lambda x, y: y > 1e-9, "both": lambda x, y: x > 1e-9 and y > 1e-9}[cond]
    cnt = sum(1 for x, y in roots if test(x, y))
    desc = {"re": "a positive real part", "im": "a positive imaginary part", "both": "positive real and imaginary parts"}[cond]
    p = f"How many solutions of $z^{{{n}}} = 1$ have {desc}?"
    return Q(p, cnt, [cnt + 1, cnt - 1 if cnt > 1 else cnt + 2, n // 2 if n // 2 != cnt else cnt + 3, n, cnt * 2 if cnt * 2 != n else cnt + 4], "Picture the regular " + str(n) + "-gon.",
             "the count.", f"the roots are at angles $\\frac{{360^\\circ k}}{{{n}}}$.", [f"Counting angles in the right region (excluding boundary): ${cnt}$."], "counting roots on the axes.")


@reg(S, "basics")
def ru_spacing(r):
    n = r.randint(3, 24)
    ans = F(360, n)
    p = f"What is the angle, in degrees, between two neighboring solutions of $z^{{{n}}} = {r.choice(['1', '-1', 'i', '16'])}$ (measured from the origin)?"
    return Q(p, ans, [F(180, n), F(360, n - 1), ans * 2, F(360 * n), F(90, n) if F(90, n) != ans else ans + 1], "The roots are equally spaced.",
             "the angle.", f"${n}$ roots spread evenly around a circle.", [f"$\\frac{{360^\\circ}}{{{n}}} = {ft(ans)}^\\circ$."], "using $180^\\circ$.")


@reg(S, "basics")
def ru_dist_one(r):
    n, v = r.choice([(3, math.sqrt(3)), (4, math.sqrt(2)), (6, 1), (12, (math.sqrt(6) - math.sqrt(2)) / 2)])
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. What is $|1 - \\omega|$?"
    return Q(p, ex(v) if n != 12 else C("\\frac{\\sqrt{6} - \\sqrt{2}}{2}", v), exw(v, r), "Chord length.",
             "the distance.", f"$|1 - \\omega| = 2\\sin\\frac{{180^\\circ}}{{{n}}}$.", [f"$2\\sin {180 // n}^\\circ = {ex(v).tex if n != 12 else '\\frac{\\sqrt{6} - \\sqrt{2}}{2}'}$."], "forgetting the factor of 2.")


@reg(S, "basics")
def ru_modulus(r):
    n = r.randint(2, 6)
    m = r.randint(2, 5)
    a = m ** n
    p = f"All solutions of $z^{{{n}}} = {r.choice([a, -a])}$ lie on a circle centered at the origin. What is its radius?"
    return Q(p, m, [a, m * n, F(a, n), m + 1, n], "$|z|^" + str(n) + " = " + str(a) + "$.",
             "the radius.", "take moduli of both sides.", [f"$|z| = \\sqrt[{n}]{{{a}}} = {m}$."], "dividing by " + str(n) + ".")


@reg(S, "basics")
def ru_conj_power(r):
    n = r.randint(3, 20)
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. For what $k$ with $0 < k < {n}$ is $\\overline{{\\omega}} = \\omega^k$?"
    return Q(p, n - 1, [1, n - 2, n // 2, n + 1, 2], "$\\overline{\\omega} = \\frac{1}{\\omega}$ for $|\\omega| = 1$.",
             "$k$.", f"$\\frac{{1}}{{\\omega}} = \\omega^{{{n} - 1}}$ since $\\omega^{{{n}}} = 1$.", [f"$k = {n - 1}$."], "answering $-1$, which is not in range.")


@reg(S, "basics")
def ru_reduce(r):
    n = r.randint(5, 13)
    a, b = r.randint(n, 5 * n), r.randint(n, 5 * n)
    k = (a + b) % n
    if k == 0:
        return None
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. If $\\omega^{{{a}}} \\cdot \\omega^{{{b}}} = \\omega^k$ with $0 \\le k < {n}$, what is $k$?"
    return Q(p, k, [(a * b) % n if (a * b) % n != k else (k + 1) % n or n - 1, (k + 1) % n, (a + b) % (n + 1) if (a + b) % (n + 1) != k else (k + 2) % n, (n - k) % n if (n - k) % n != k else (k + 3) % n, a + b], "Add exponents, then reduce mod " + str(n) + ".",
             "$k$.", f"$\\omega^{{{n}}} = 1$.", [f"${a} + {b} = {a + b} \\equiv {k} \\pmod{{{n}}}$."], "multiplying the exponents.")


@reg(S, "basics")
def ru_common_neg(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    roots_a = {F(k, a) for k in range(a)}
    roots_b = {F(2 * k + 1, 2 * b) for k in range(b)}
    cnt = len(roots_a & roots_b)
    p = f"How many complex numbers satisfy both $z^{{{a}}} = 1$ and $z^{{{b}}} = -1$?"
    return Q(p, cnt, [x for x in (0, 1, 2, math.gcd(a, b), 3, 4) if x != cnt][:5], "Write each root as a fraction of a full turn.",
             "the count.", f"roots of $z^{{{a}}} = 1$ are at $\\frac{{k}}{{{a}}}$ of a turn; roots of $z^{{{b}}} = -1$ are at $\\frac{{2j + 1}}{{{2 * b}}}$ of a turn.",
             [f"Common fractions: ${cnt}$."], "using $\\gcd(" + str(a) + ", " + str(b) + ")$ as if both equations were $= 1$.")


@reg(S, "basics")
def ru_eisenstein(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    n = a * a - a * b + b * b
    p = f"Let $\\omega = -\\frac{{1}}{{2}} + \\frac{{\\sqrt{{3}}}}{{2}}i$. What is $|{a} + {b}\\omega|^2$?"
    return Q(p, n, [a * a + b * b, a * a + a * b + b * b, (a - b) ** 2 if (a - b) ** 2 != n else n + 1, n + 1, abs(n - 2) if abs(n - 2) != n else n + 2], "Expand with $\\omega + \\overline{\\omega} = -1$ and $\\omega\\overline{\\omega} = 1$.",
             "the squared modulus.", f"$|a + b\\omega|^2 = (a + b\\omega)(a + b\\overline{{\\omega}}) = a^2 + ab(\\omega + \\overline{{\\omega}}) + b^2$.", [f"${a * a} - {a * b} + {b * b} = {n}$."], "using $+ab$.")


@reg(S, "basics")
def ru_power_sum(r):
    n = r.randint(3, 12)
    k = r.randint(1, 30)
    v = n if k % n == 0 else 0
    p = f"Let $z_1, z_2, \\ldots, z_{{{n}}}$ be the solutions of $z^{{{n}}} = 1$. What is $z_1^{{{k}}} + z_2^{{{k}}} + \\cdots + z_{{{n}}}^{{{k}}}$?"
    return Q(p, v, [x for x in (0, n, 1, -1, k) if x != v][:4] + [n + 1], "Is " + str(k) + " a multiple of " + str(n) + "?",
             "the sum.", f"if ${n} \\nmid k$, the $k$th powers are again a full set of roots (with repeats) summing to $0$; if ${n} \\mid k$, every term is $1$.",
             [f"${k} \\bmod {n} = {k % n}$, so the sum is ${v}$."], "answering 0 regardless.")


@reg(S, "basics")
def ru_order(r):
    a = r.randint(1, 40)
    b = r.randint(3, 40)
    if a % b == 0:
        return None
    n = b // math.gcd(a, b)
    p = f"What is the smallest positive integer $n$ such that $\\left(\\cos\\frac{{{2 * a}\\pi}}{{{b}}} + i\\sin\\frac{{{2 * a}\\pi}}{{{b}}}\\right)^n = 1$?"
    return Q(p, n, [b, a, n * 2 if n * 2 != b else n + 1, b - a if b - a > 0 and b - a != n else n + 2, math.gcd(a, b) if math.gcd(a, b) != n else n + 3], "Reduce the fraction $\\frac{" + str(a) + "}{" + str(b) + "}$.",
             "$n$.", f"we need $\\frac{{{a}n}}{{{b}}}$ to be an integer.", [f"$\\frac{{{a}}}{{{b}}} = \\frac{{{a // math.gcd(a, b)}}}{{{n}}}$ in lowest terms, so $n = {n}$."], "answering " + str(b) + " without reducing.")


@reg(S, "basics")
def ru_sum_all(r):
    n = r.randint(2, 15)
    c = r.randint(1, 5)
    p = f"What is the sum of all solutions of $z^{{{n}}} = {c ** n if r.random() < .5 else str(c ** n) + 'i'}$?"
    v = 0 if n > 1 else c
    return Q(p, v, [c * n, c, 1, n, -1], "Vieta, or symmetry.",
             "the sum.", f"$z^{{{n}}} - c = 0$ has no $z^{{{n - 1}}}$ term, so the roots sum to $0$.", ["The roots are evenly spaced around a circle, and they cancel."], "adding the moduli.") if n > 1 else None


@reg(S, "challenge")
def ruc_one_minus(r):
    n = r.randint(3, 15)
    p = f"Let $\\omega_1, \\ldots, \\omega_{{{n - 1}}}$ be the solutions of $z^{{{n}}} = 1$ other than $1$. What is $(1 - \\omega_1)(1 - \\omega_2)\\cdots(1 - \\omega_{{{n - 1}}})$?"
    return Q(p, n, [n - 1, 0, 1, 2 ** n - 1, -n], "Factor $z^n - 1$.",
             "the product.", f"$\\frac{{z^{{{n}}} - 1}}{{z - 1}} = 1 + z + \\cdots + z^{{{n - 1}}} = \\prod (z - \\omega_k)$.", [f"At $z = 1$: $1 + 1 + \\cdots + 1 = {n}$."], "plugging in $z = 1$ before dividing (getting 0).")


@reg(S, "challenge")
def ruc_recip_sum(r):
    n = r.randint(3, 20)
    v = F(n - 1, 2)
    p = f"Let $\\omega_1, \\ldots, \\omega_{{{n - 1}}}$ be the solutions of $z^{{{n}}} = 1$ other than $1$. What is $\\displaystyle\\sum_{{k=1}}^{{{n - 1}}} \\frac{{1}}{{1 - \\omega_k}}$?"
    return Q(p, v, [F(n, 2), F(n - 1), F(1, 2), v + 1, F(n + 1, 2)], "Pair $\\omega$ with $\\overline{\\omega}$.",
             "the sum.", "$\\frac{1}{1 - \\omega} + \\frac{1}{1 - \\overline{\\omega}} = 1$ when $|\\omega| = 1$, so each conjugate pair contributes $1$ (and $\\omega = -1$, if present, gives $\\frac{1}{2}$).",
             [f"Total: $\\frac{{{n - 1}}}{{2}} = {ft(v)}$."], "assuming the sum is 0.")


@reg(S, "challenge")
def ruc_one_plus_omega(r):
    k = r.randint(1, 12)
    v = (-1) ** k
    p = f"Let $\\omega \\ne 1$ satisfy $\\omega^3 = 1$. What is $(1 + \\omega)^{{{3 * k}}}$?"
    return Q(p, v, [-v, 2 ** (3 * k), 0, 3, 2], "$1 + \\omega = -\\omega^2$.",
             "the value.", f"$(1 + \\omega)^{{{3 * k}}} = (-\\omega^2)^{{{3 * k}}} = (-1)^{{{3 * k}}}\\omega^{{{6 * k}}}$.", [f"$\\omega^{{{6 * k}}} = 1$, so the value is $(-1)^{{{k}}} = {v}$."], "treating $\\omega$ as 1.")


@reg(S, "challenge")
def ruc_filter(r):
    n = r.randint(5, 15)
    m = r.choice([3, 4])
    res = r.randint(0, m - 1)
    v = sum(comb(n, k) for k in range(res, n + 1, m))
    tail = f"\\binom{{{n}}}{{{res}}} + \\binom{{{n}}}{{{res + m}}} + \\binom{{{n}}}{{{res + 2 * m}}} + \\cdots"
    p = f"What is ${tail}$ (all $\\binom{{{n}}}{{k}}$ with $k \\equiv {res} \\pmod {m}$)?"
    return Q(p, v, [2 ** n // m, v + 1, v - 1, 2 ** (n - 1), round(2 ** n / m) + 2 if round(2 ** n / m) + 2 != v else v + 2], "Roots of unity filter.",
             "the sum.", f"average $(1 + \\zeta)^{{{n}}}\\zeta^{{-{res}}}$ over all ${m}$th roots of unity $\\zeta$.",
             [f"This gives ${v}$ (close to, but not exactly, $\\frac{{2^{{{n}}}}}{{{m}}}$)."], "assuming exactly $\\frac{1}{" + str(m) + "}$ of $2^" + str(n) + "$.")


@reg(S, "challenge")
def ruc_cos_sum(r):
    n = r.choice([5, 7, 9, 11, 13])
    m = (n - 1) // 2
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{m}}} \\cos\\frac{{2k\\pi}}{{{n}}}$?"
    return Q(p, F(-1, 2), [0, F(1, 2), -1, F(m, n), F(-1, n)], "Use the real parts of the " + str(n) + "th roots of unity.",
             "the sum.", f"the ${n}$th roots sum to $0$; the real parts give $1 + 2\\sum_{{k=1}}^{{{m}}} \\cos\\frac{{2k\\pi}}{{{n}}} = 0$.", ["So the sum is $-\\frac{1}{2}$."], "forgetting the root $1$.")


@reg(S, "challenge")
def ruc_partial(r):
    n, m = r.choice([(6, 1), (6, 2), (4, 1), (12, 3), (8, 2), (6, 4), (12, 5), (12, 2)])
    w = cmath.exp(2j * math.pi / n)
    s = sum(w ** k for k in range(m + 1))
    v = abs(s) ** 2
    q = F(v).limit_denominator(4)
    if abs(float(q) - v) > 1e-9:
        sq = v
        cands = [(t, c) for t, nt, c in []]
        return None
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. What is $|" + {1: "1 + \\omega", 2: "1 + \\omega + \\omega^2"}.get(m, f"1 + \\omega + \\cdots + \\omega^{{{m}}}") + "|^2$?"
    return Q(p, q, [q + 1, F(m + 1) if F(m + 1) != q else q + 2, F((m + 1) ** 2) if (m + 1) ** 2 != q else q + 3, q - 1 if q > 1 else F(1, 2), q * 2], "Geometric series: $\\frac{1 - \\omega^{" + str(m + 1) + "}}{1 - \\omega}$.",
             "the squared modulus.", f"$|1 - \\omega^{{k}}| = 2\\sin\\frac{{k\\pi}}{{{n}}}$.", [f"$\\frac{{\\sin^2({m + 1}\\pi/{n})}}{{\\sin^2(\\pi/{n})}} = {ft(q)}$."], "adding the moduli of the terms.")


@reg(S, "challenge")
def ruc_quad_omega(r):
    a = r.choice([x for x in range(-6, 9) if x])
    v = a * a - a + 1
    p = f"Let $\\omega \\ne 1$ satisfy $\\omega^3 = 1$. What is $({a} + \\omega)({a} + \\omega^2)$?".replace("(-", "(-")
    return Q(p, v, [a * a + a + 1, a * a + 1, a * a - 1, v + 1, a * a], "Expand and use $\\omega + \\omega^2 = -1$, $\\omega^3 = 1$.",
             "the product.", f"$({a} + \\omega)({a} + \\omega^2) = {a * a}{sg(a)}(\\omega + \\omega^2) + \\omega^3$.", [f"$= {a * a} - {par(a)} + 1 = {v}$."], "using $\\omega + \\omega^2 = 1$.")
