"""Extra Algebra problem types (part 2): exponents and radicals, factoring, quadratics, absolute value."""
import math
from fractions import Fraction as F

from common import NAMES, C, Q, num, par, sg, simplify_sqrt, var

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def rad(k, n):
    """k * sqrt(n) simplified, as a choice."""
    a, b = simplify_sqrt(n)
    k = F(k) * a
    if b == 1:
        return num(k)
    coef = "" if k == 1 else ("-" if k == -1 else ftex(k))
    if k.denominator != 1:
        top = ("" if abs(k.numerator) == 1 else str(abs(k.numerator))) + f"\\sqrt{{{b}}}"
        return C(("-" if k < 0 else "") + f"\\frac{{{top}}}{{{k.denominator}}}", float(k) * math.sqrt(b))
    return C(f"{coef}\\sqrt{{{b}}}", float(k) * math.sqrt(b))


def factorint(n):
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def pw(base, e):
    return C(f"{base}^{{{e}}}", e * math.log(base))


# ================================================================ alg_exponents
S = "alg_exponents"


@reg(S, "basics")
def ex_ten_power(r):
    a = r.randint(3, 9)
    k = r.randint(1, a - 1)
    ans = 10 ** k
    p = f"What is $\\dfrac{{2^{{{a}}} \\cdot 5^{{{a}}}}}{{10^{{{a - k}}}}}$?"
    return Q(p, ans, [10 ** (k + 1), 10 ** a, 7 ** k, 2 ** k, 10 ** (k - 1) if k > 1 else 1000], "Pair each 2 with a 5.",
             "the value of the fraction.", "$2^n \\cdot 5^n = (2 \\cdot 5)^n = 10^n$, because the exponents match.",
             [f"$2^{{{a}}} \\cdot 5^{{{a}}} = 10^{{{a}}}$.", f"$\\frac{{10^{{{a}}}}}{{10^{{{a - k}}}}} = 10^{{{a} - {a - k}}} = 10^{{{k}}} = {ans}$."],
             "adding the bases to get $7^" + str(a) + "$; when exponents match, the bases multiply.")


@reg(S, "basics")
def ex_power_of_power(r):
    a, b, c = r.randint(2, 6), r.randint(2, 5), r.randint(1, 9)
    ans = a * b + c
    p = f"Write $(x^{{{a}}})^{{{b}}} \\cdot x^{{{c}}}$ as a single power of $x$. What is the exponent?"
    return Q(p, ans, [a + b + c, a * b * c, a ** b + c, ans + 1, a * (b + c)], "A power of a power multiplies exponents.",
             "the exponent of the single power.", "$(x^a)^b = x^{ab}$, and multiplying powers of the same base adds exponents.",
             [f"$(x^{{{a}}})^{{{b}}} = x^{{{a * b}}}$.", f"$x^{{{a * b}}} \\cdot x^{{{c}}} = x^{{{a * b} + {c}}} = x^{{{ans}}}$."],
             "adding $" + str(a) + " + " + str(b) + "$ for the power of a power.")


@reg(S, "basics")
def ex_neg_fraction(r):
    a, b = r.sample(range(1, 7), 2)
    n = r.choice([1, 2, 3])
    ans = F(b, a) ** n
    p = f"What is $\\left(\\dfrac{{{a}}}{{{b}}}\\right)^{{-{n}}}$?"
    return Q(p, ans, [F(a, b) ** n, -ans, F(-a * n, b), F(b, a) * n, -F(a, b) ** n], "A negative exponent flips the fraction.",
             "the value.", "$\\left(\\frac{a}{b}\\right)^{-n} = \\left(\\frac{b}{a}\\right)^n$. Negative exponents mean reciprocal, not negative.",
             [f"Flip: $\\left(\\frac{{{b}}}{{{a}}}\\right)^{{{n}}}$.", f"$= \\frac{{{b ** n}}}{{{a ** n}}} = {ftex(ans)}$."],
             "making the answer negative; the negative exponent flips the fraction.")


@reg(S, "basics")
def ex_frac_power(r):
    base, root, pw_ = r.choice([(8, 3, 2), (27, 3, 2), (16, 4, 3), (32, 5, 2), (64, 3, 2), (81, 4, 3), (125, 3, 2), (4, 2, 3), (9, 2, 3), (64, 2, 3), (16, 2, 3)])
    rt = round(base ** (1 / root))
    ans = rt ** pw_
    p = f"What is ${base}^{{\\frac{{{pw_}}}{{{root}}}}}$?"
    return Q(p, ans, [base * pw_ // root if base * pw_ % root == 0 else ans + 2, rt * pw_, ans * rt, rt, base ** 2 // ans if base ** 2 // ans != ans else ans - 1], "Take the root first, then the power.",
             "the value.", "$b^{p/q} = (\\sqrt[q]{b})^p$: the bottom of the exponent is the root, the top is the power.",
             [f"$\\sqrt[{root}]{{{base}}} = {rt}$.", f"${rt}^{{{pw_}}} = {ans}$."],
             "multiplying the base by the fraction.")


@reg(S, "basics")
def ex_add_radicals(r):
    k = r.choice([2, 3, 5, 6, 7])
    a, b = r.sample([1, 2, 3, 4, 5], 2)
    ans = rad(a + b, k)
    p = f"Simplify $\\sqrt{{{a * a * k}}} + \\sqrt{{{b * b * k}}}$."
    return Q(p, ans, [rad(1, (a * a + b * b) * k), rad(a * b, k), rad(a + b, 2 * k), num(a + b), rad(a + b + 1, k)], "Simplify each root first.",
             "one simplified radical.", "you can only add radicals with the same number under the root, so simplify each one.",
             [f"$\\sqrt{{{a * a * k}}} = \\sqrt{{{a * a}}}\\sqrt{{{k}}} = {rad(a, k).tex}$.", f"$\\sqrt{{{b * b * k}}} = {rad(b, k).tex}$.", f"Add like terms: ${ans.tex}$."],
             "adding under the root: $\\sqrt{x} + \\sqrt{y}$ is not $\\sqrt{x + y}$.")


@reg(S, "basics")
def ex_mult_radicals(r):
    a, b = r.sample([2, 3, 6, 8, 10, 12, 15, 18, 20, 24, 27], 2)
    ans = rad(1, a * b)
    p = f"Simplify $\\sqrt{{{a}}} \\cdot \\sqrt{{{b}}}$."
    return Q(p, ans, [rad(1, a + b), num(a * b), rad(2, a * b), rad(1, a * b * 2), rad(1, abs(a - b) or 7)], "Multiply under one root, then simplify.",
             "the product in simplest form.", "$\\sqrt{a}\\sqrt{b} = \\sqrt{ab}$; then pull out any square factors.",
             [f"$\\sqrt{{{a} \\cdot {b}}} = \\sqrt{{{a * b}}}$.", f"Pull out squares: $\\sqrt{{{a * b}}} = {ans.tex}$."],
             "leaving a perfect square factor inside the root.")


@reg(S, "basics")
def ex_rationalize(r):
    m = r.choice([2, 3, 5, 6, 7, 10])
    k = r.choice([x for x in range(1, 13) if x % m != 0] + [m * 2])
    ans = rad(F(k, m), m)
    p = f"Write $\\dfrac{{{k}}}{{\\sqrt{{{m}}}}}$ with a rational denominator."
    return Q(p, ans, [rad(F(k), m), rad(F(m, k), m), rad(F(k, m * m), m), num(F(k, m)), rad(F(k, m), 2 * m)], "Multiply top and bottom by $\\sqrt{" + str(m) + "}$.",
             "an equal fraction with no root in the bottom.", "multiplying by $\\frac{\\sqrt{m}}{\\sqrt{m}}$ (which is $1$) turns $\\sqrt{m}\\sqrt{m}$ into $m$.",
             [f"$\\frac{{{k}}}{{\\sqrt{{{m}}}}} \\cdot \\frac{{\\sqrt{{{m}}}}}{{\\sqrt{{{m}}}}} = \\frac{{{k}\\sqrt{{{m}}}}}{{{m}}}$.", f"Simplify: ${ans.tex}$."],
             "multiplying only the bottom by $\\sqrt{" + str(m) + "}$, which changes the value.")


@reg(S, "basics")
def ex_sci_notation(r):
    a, b = r.choice([(2, 3), (4, 2), (1.5, 4), (2.5, 2), (3, 3), (5, 2), (1.2, 5)])
    m, n = r.randint(3, 9), r.randint(-6, 6)
    prod = a * b
    e = m + n
    if prod >= 10:
        prod, e = prod / 10, e + 1
    ans = C(f"{prod:g} \\times 10^{{{e}}}", e + math.log10(prod))
    wrong = [C(f"{prod:g} \\times 10^{{{e + d}}}", e + d + math.log10(prod)) for d in (-2, -1, 1)] + [C(f"{a + b:g} \\times 10^{{{e}}}", e + math.log10(a + b))]
    p = f"What is $({a:g} \\times 10^{{{m}}})({b:g} \\times 10^{{{n}}})$ in scientific notation?"
    return Q(p, ans, wrong, "Multiply the front numbers; add the exponents.",
             "the product written as $a \\times 10^n$ with $1 \\le a < 10$.", "rearrange: $(a \\cdot b) \\times 10^{m + n}$, then fix the front number if it is $10$ or more.",
             [f"Front numbers: ${a:g} \\cdot {b:g} = {a * b:g}$.", f"Powers: $10^{{{m}}} \\cdot 10^{{{n}}} = 10^{{{m + n}}}$."] + ([f"${a * b:g} = {prod:g} \\times 10$, so add $1$ to the exponent."] if a * b >= 10 else []) + [f"Result: ${ans.tex}$."],
             "multiplying the exponents instead of adding them.")


@reg(S, "basics")
def ex_compare(r):
    k = r.randint(1, 4)
    opts = [(2, 6 * k, 64), (3, 4 * k, 81), (5, 3 * k, 125), (7, 2 * k, 49), (6, 2 * k, 36)]
    r.shuffle(opts)
    best = max(opts, key=lambda t: t[2])
    ans = pw(best[0], best[1])
    p = "Which of these numbers is largest?"
    return Q(p, ans, [pw(b_, e) for b_, e, _ in opts if (b_, e) != best[:2]], "Write each as a power with exponent " + str(k) + ".",
             "the largest of five powers.", f"all the exponents are multiples of ${k}$, so rewrite each as (something)$^{{{k}}}$ and compare the somethings.",
             ["Rewrite: " + ", ".join(f"${b_}^{{{e}}} = ({b_}^{{{e // k}}})^{{{k}}} = {v}^{{{k}}}$" for b_, e, v in opts) + ".", f"The largest inside number is ${best[2]}$, so ${ans.tex}$ is largest."],
             "picking the biggest exponent or the biggest base.", sort=False)


@reg(S, "basics")
def ex_solve_frac_exp(r):
    t = r.randint(2, 6)
    k = t * t
    ans = t ** 3
    p = f"If $x^{{\\frac{{2}}{{3}}}} = {k}$ and $x > 0$, what is $x$?"
    return Q(p, ans, [k * k, t, k, t ** 2 * 3, round(k ** 1.5) + 1], "Raise both sides to the $\\frac{3}{2}$ power.",
             "$x$.", "undo the exponent $\\frac{2}{3}$ with its reciprocal $\\frac{3}{2}$.",
             [f"$x = {k}^{{\\frac{{3}}{{2}}}}$.", f"$\\sqrt{{{k}}} = {t}$, and ${t}^3 = {ans}$."],
             "raising to the $\\frac{2}{3}$ power again instead of undoing it.")


@reg(S, "basics")
def ex_factor_power(r):
    k = r.randint(3, 10)
    x = r.randint(2, 9)
    total = 3 * 2 ** k
    p = f"If $2^{{x + 1}} + 2^{{x}} = {total}$, what is $x$?"
    return Q(p, k, [k + 1, k - 1, F(total, 3), k + 2, 2 * k], "Factor out $2^x$.",
             "$x$.", "pull out the common factor: $2^{x+1} + 2^x = 2^x(2 + 1) = 3 \\cdot 2^x$.",
             [f"$3 \\cdot 2^x = {total}$.", f"$2^x = {total // 3} = 2^{{{k}}}$.", f"$x = {k}$."],
             "adding the exponents to get $2^{2x + 1}$.")


@reg(S, "basics")
def ex_cube_root(r):
    n = r.randint(2, 12)
    N = n ** 3
    p = f"What is $\\sqrt[3]{{{N}}}$?"
    return Q(p, n, [n + 1, n - 1, N // 3, round(math.sqrt(N)), n * 3], "Which whole number cubed gives " + str(N) + "?",
             "the cube root.", "the cube root of $N$ is the number whose cube is $N$.",
             [f"Try nearby cubes: ${n - 1}^3 = {(n - 1) ** 3}$, ${n}^3 = {N}$.", f"So $\\sqrt[3]{{{N}}} = {n}$."],
             "dividing by $3$.")


@reg(S, "basics")
def ex_base_change(r):
    a = r.randint(1, 6)
    x = 3 * a
    p = f"Solve $9^{{x}} = 27^{{x - {a}}}$."
    return Q(p, x, [a, 2 * a, x + 1, F(3 * a, 2), -x], "Write both sides as powers of $3$.",
             "$x$.", "with the same base on both sides, the exponents must match.",
             [f"$9^x = 3^{{2x}}$ and $27^{{x - {a}}} = 3^{{3(x - {a})}}$.", f"$2x = 3x - {3 * a}$.", f"$x = {x}$."],
             "setting $x = x - " + str(a) + "$ without converting the bases.")


@reg(S, "basics")
def ex_conj_product(r):
    a, b = r.sample([2, 3, 5, 6, 7, 10, 11, 13], 2)
    if a < b:
        a, b = b, a
    p = f"What is $(\\sqrt{{{a}}} + \\sqrt{{{b}}})(\\sqrt{{{a}}} - \\sqrt{{{b}}})$?"
    return Q(p, a - b, [a + b, a * b, b - a, (a - b) ** 2, rad(1, a * b)], "Difference of squares.",
             "the product.", "$(x + y)(x - y) = x^2 - y^2$; squaring a square root removes it.",
             [f"$(\\sqrt{{{a}}})^2 - (\\sqrt{{{b}}})^2 = {a} - {b} = {a - b}$."],
             "expanding and keeping the middle terms; they cancel.")


@reg(S, "basics")
def ex_binomial_square(r):
    a, b = r.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (6, 24), (2, 32), (8, 18)])
    ans = a + b + 2 * math.isqrt(a * b)
    p = f"What is $(\\sqrt{{{a}}} + \\sqrt{{{b}}})^2$?"
    return Q(p, ans, [a + b, ans - math.isqrt(a * b), (a + b) ** 2, ans + 2, 2 * a * b], "Expand: $(x + y)^2 = x^2 + 2xy + y^2$.",
             "the value.", "square a sum with the middle term: $(\\sqrt{a} + \\sqrt{b})^2 = a + b + 2\\sqrt{ab}$.",
             [f"$a + b = {a + b}$.", f"$2\\sqrt{{{a} \\cdot {b}}} = 2\\sqrt{{{a * b}}} = {2 * math.isqrt(a * b)}$.", f"Total: ${ans}$."],
             "forgetting the middle term, giving $" + str(a + b) + "$.")


@reg(S, "basics")
def ex_half_power(r):
    n = r.randint(5, 30)
    ans = pw(2, 2 * n - 1)
    p = f"What is half of $4^{{{n}}}$?"
    return Q(p, ans, [pw(2, n), pw(4, n - 1), pw(2, 2 * n - 2), pw(2, n - 1), C(f"2^{{{2 * n + 1}}}", (2 * n + 1) * math.log(2))], "Write $4^{" + str(n) + "}$ as a power of $2$.",
             "$\\frac{1}{2} \\cdot 4^{" + str(n) + "}$.", "halving a power of $2$ lowers its exponent by $1$.",
             [f"$4^{{{n}}} = (2^2)^{{{n}}} = 2^{{{2 * n}}}$.", f"Half: $\\frac{{2^{{{2 * n}}}}}{{2}} = 2^{{{2 * n - 1}}}$."],
             "halving the exponent ($2^{" + str(n) + "}$); that is the square root, not half.")


@reg(S, "challenge")
def exc_chain(r):
    m = r.choice([3, 5, 6, 7])
    k = r.choice([x for x in [4, 8, 9, 16, 25, 27] if x != m])
    p = f"If $2^{{a}} = {m}$ and ${m}^{{b}} = {k}$, what is $2^{{ab}}$?"
    return Q(p, k, [m * k, 2 * k, k + m, m ** 2, 2 ** (m + k) if m + k < 12 else k * 4], "$2^{ab} = (2^a)^b$.",
             "$2^{ab}$.", "power of a power: $2^{ab} = (2^a)^b$, and you know $2^a$.",
             [f"$2^{{ab}} = (2^a)^b = {m}^b$.", f"${m}^b = {k}$."],
             "trying to find $a$ and $b$ as decimals first.")


@reg(S, "challenge")
def exc_simplify_ratio(r):
    b = r.choice([2, 3, 5])
    p1, p2, q1, q2 = r.sample(range(0, 5), 4)
    if p1 == p2 or q1 == q2:
        return None
    num_ = b ** p1 + b ** p2
    den = b ** q1 - b ** q2
    if den == 0:
        return None
    ans = F(num_, den)
    show = lambda e: f"{b}^{{n + {e}}}" if e else f"{b}^n"
    p = f"For every positive integer $n$, what is $\\dfrac{{{show(p1)} + {show(p2)}}}{{{show(q1)} - {show(q2)}}}$?"
    return Q(p, ans, [F(b ** (p1 + p2), b ** (q1 + q2)), F(p1 + p2, q1 - q2) if q1 != q2 else 2, ans + 1, -ans, F(num_, abs(den) + 1)], "Factor $" + f"{b}^n" + "$ out of the top and bottom.",
             "the value of the fraction (it doesn't depend on $n$).", f"every term has a factor ${b}^n$, which cancels.",
             [f"Top: ${b}^n({b ** p1} + {b ** p2}) = {b}^n \\cdot {num_}$.", f"Bottom: ${b}^n({b ** q1} - {b ** q2}) = {b}^n \\cdot {den}$.", f"Ratio: $\\frac{{{num_}}}{{{den}}} = {ftex(ans)}$."],
             "combining the powers by adding exponents across the plus sign.")


@reg(S, "challenge")
def exc_nested(r):
    k = r.randint(2, 9)
    x = k * k - k
    p = f"The expression $\\sqrt{{x + \\sqrt{{x + \\sqrt{{x + \\cdots}}}}}}$ continues forever and equals ${k}$. What is $x$?"
    return Q(p, x, [k * k, k * k + k, k, x + 1, k * (k + 1) // 2], "The part inside the first root contains the whole expression again.",
             "$x$.", "an infinite expression contains a copy of itself. Replace that copy with its value.",
             [f"Let the whole thing be $y = {k}$. Inside the first root is $x + y$.", f"So $y = \\sqrt{{x + y}}$, which gives $y^2 = x + y$.", f"$x = y^2 - y = {k * k} - {k} = {x}$."],
             "forgetting that the inside contains the whole expression, giving $x = " + str(k * k) + "$.")


@reg(S, "challenge")
def exc_system(r):
    x, y = r.randint(1, 8), r.randint(1, 5)
    A, B = x + 2 * y, x - 2 * y
    p = f"If $2^{{x}} \\cdot 4^{{y}} = 2^{{{A}}}$ and $\\dfrac{{3^{{x}}}}{{9^{{y}}}} = 3^{{{B}}}$, what is $x$?"
    return Q(p, x, [y, A, B, F(A + B, 4), x + 1], "Rewrite $4$ and $9$ as powers of $2$ and $3$.",
             "$x$.", "turn each equation into an equation of exponents.",
             [f"$2^x \\cdot 2^{{2y}} = 2^{{x + 2y}}$, so $x + 2y = {A}$.", f"$3^x \\div 3^{{2y}} = 3^{{x - 2y}}$, so $x - 2y = {B}$.", f"Add: $2x = {A + B}$, so $x = {x}$."],
             "treating $4^y$ as $2^y$.")


@reg(S, "challenge")
def exc_digits(r):
    a = r.randint(3, 12)
    extra = r.randint(1, 6)
    b = 2 * a + extra
    N = 4 ** a * 5 ** b
    d = len(str(N))
    p = f"How many digits does $4^{{{a}}} \\cdot 5^{{{b}}}$ have?"
    return Q(p, d, [d + 1, d - 1, a + b, 2 * a, b + 1], "Make as many 10s as you can.",
             "the digit count.", "pair each $2$ with a $5$ to make factors of $10$, which only add zeros.",
             [f"$4^{{{a}}} = 2^{{{2 * a}}}$. So the number is $2^{{{2 * a}}} \\cdot 5^{{{b}}} = 10^{{{2 * a}}} \\cdot 5^{{{extra}}}$.", f"$5^{{{extra}}} = {5 ** extra}$ has ${len(str(5 ** extra))}$ digits.", f"Total digits: ${len(str(5 ** extra))} + {2 * a} = {d}$."],
             "counting digits as $a + b$ without making the tens.")


@reg(S, "challenge")
def exc_conj_frac(r):
    a, b = r.choice([(3, 2), (5, 3), (7, 5), (6, 2), (5, 1), (8, 6), (7, 3)])
    # (sqrt a + sqrt b)/(sqrt a - sqrt b) = (a + b + 2 sqrt(ab)) / (a - b)
    k, m = simplify_sqrt(a * b)
    whole = F(a + b, a - b)
    coef = F(2 * k, a - b)
    ans_val = float(whole) + float(coef) * math.sqrt(m)
    tex = f"{ftex(whole)} + {('' if coef == 1 else ftex(coef))}\\sqrt{{{m}}}" if m > 1 else ftex(whole + coef)
    ans = C(tex, ans_val)
    p = f"Simplify $\\dfrac{{\\sqrt{{{a}}} + \\sqrt{{{b}}}}}{{\\sqrt{{{a}}} - \\sqrt{{{b}}}}}$."
    wrong = [C(f"{ftex(whole)} + \\sqrt{{{m}}}", float(whole) + math.sqrt(m)) if coef != 1 else C(f"{ftex(whole + 1)} + \\sqrt{{{m}}}", float(whole) + 1 + math.sqrt(m)),
             num(-1) if True else None, C(f"{a + b} + 2\\sqrt{{{a * b}}}", a + b + 2 * math.sqrt(a * b)), C(f"{ftex(whole)} - {('' if coef == 1 else ftex(coef))}\\sqrt{{{m}}}", float(whole) - float(coef) * math.sqrt(m))]
    return Q(p, ans, wrong, "Multiply top and bottom by $\\sqrt{" + str(a) + "} + \\sqrt{" + str(b) + "}$.",
             "the fraction without roots in the denominator.", "multiply by the conjugate of the bottom to use $(x - y)(x + y) = x^2 - y^2$.",
             [f"Bottom: $(\\sqrt{{{a}}} - \\sqrt{{{b}}})(\\sqrt{{{a}}} + \\sqrt{{{b}}}) = {a} - {b} = {a - b}$.", f"Top: $(\\sqrt{{{a}}} + \\sqrt{{{b}}})^2 = {a + b} + 2\\sqrt{{{a * b}}} = {a + b} + {2 * k if k > 1 else 2}\\sqrt{{{m}}}$.",
              f"Divide each term by ${a - b}$: ${tex}$."],
             "forgetting to divide the root term by the denominator too.", sort=False)


@reg(S, "challenge")
def exc_three_powers(r):
    a, b = r.sample([2, 3, 5], 2)
    x = r.randint(2, 5)
    total = a ** x + a ** (x + 1) + a ** (x + 2)
    p = f"If ${a}^{{x}} + {a}^{{x + 1}} + {a}^{{x + 2}} = {total}$, what is $x$?"
    return Q(p, x, [x + 1, x - 1, x + 2, total // (1 + a + a * a) // a if total // (1 + a + a * a) // a != x else x + 3, 3 * x], "Factor out $" + str(a) + "^x$.",
             "$x$.", f"each term has ${a}^x$ as a factor.",
             [f"${a}^x(1 + {a} + {a * a}) = {total}$, so ${a}^x \\cdot {1 + a + a * a} = {total}$.", f"${a}^x = {total // (1 + a + a * a)} = {a}^{{{x}}}$, so $x = {x}$."],
             "adding the exponents of the three terms.")


# ================================================================ alg_factoring
S = "alg_factoring"


@reg(S, "basics")
def fa_monic(r):
    m, n = r.sample([x for x in range(-9, 10) if x], 2)
    if m < n:
        m, n = n, m
    p = f"The expression $x^2{sg(m + n)}x{sg(m * n)}$ factors as $(x + m)(x + n)$ with $m > n$. What is $m - n$?"
    return Q(p, m - n, [m + n, m * n, abs(m) + abs(n) if abs(m) + abs(n) != m - n else m - n + 2, m, (m - n) * 2], "Find two numbers with the right sum and product.",
             "$m - n$.", "$(x + m)(x + n) = x^2 + (m + n)x + mn$, so you need two numbers with sum " + str(m + n) + " and product " + str(m * n) + ".",
             [f"Sum ${m + n}$, product ${m * n}$: the numbers are ${m}$ and ${n}$.", f"$m - n = {m} - {par(n)} = {m - n}$."],
             "mixing up which number gets the sign.")


@reg(S, "basics")
def fa_gcf_value(r):
    a = r.randint(2, 9)
    k = r.randint(-10, 15)
    p = f"If $x + y = {k}$, what is ${a}x + {a}y$?"
    return Q(p, a * k, [a + k, k, a * k + a, 2 * a * k, F(k, a)], "Factor out the " + str(a) + ".",
             "the value of the expression.", "a common factor can be pulled out: $ax + ay = a(x + y)$.",
             [f"${a}x + {a}y = {a}(x + y)$.", f"$= {a} \\cdot {par(k)} = {a * k}$."],
             "trying to find $x$ and $y$ separately; you can't, and you don't need to.")


@reg(S, "basics")
def fa_grouping(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    pp, qq = r.randint(-8, 12), r.randint(-8, 12)
    ans = pp * qq
    p = f"If $x + {b} = {pp}$ and $y + {a} = {qq}$, what is $xy + {a}x + {b}y + {a * b}$?"
    return Q(p, ans, [pp + qq, ans + a * b, ans - a * b, (pp - b) * (qq - a), 2 * ans], "Group the terms in pairs.",
             "the value.", "factor by grouping: $xy + ax + by + ab = x(y + a) + b(y + a) = (x + b)(y + a)$.",
             [f"$xy + {a}x + {b}y + {a * b} = x(y + {a}) + {b}(y + {a}) = (x + {b})(y + {a})$.", f"$= {par(pp)} \\cdot {par(qq)} = {ans}$."],
             "solving for $x$ and $y$ and then making an arithmetic slip; the factoring makes it one multiplication.")


@reg(S, "basics")
def fa_perfect_square_k(r):
    c = r.randint(2, 12)
    a = r.choice([1, 1, 4, 9])
    k = 2 * math.isqrt(a) * c
    p = f"For what positive number $k$ is ${a if a > 1 else ''}x^2 + kx + {c * c}$ a perfect square?"
    return Q(p, k, [c, c * c, k // 2, 2 * k, c * c * 2], "A perfect square looks like $(px + q)^2 = p^2x^2 + 2pqx + q^2$.",
             "the middle coefficient $k$.", "match the expression to $(px + q)^2$.",
             [f"$p^2 = {a}$ gives $p = {math.isqrt(a)}$; $q^2 = {c * c}$ gives $q = {c}$.", f"Middle term: $2pq = 2 \\cdot {math.isqrt(a)} \\cdot {c} = {k}$."],
             "forgetting the factor $2$ in the middle term.")


@reg(S, "basics")
def fa_diff_sq_sum(r):
    a, b = r.sample(range(3, 30), 2)
    if a < b:
        a, b = b, a
    N = a * a - b * b
    d = a - b
    p = f"If $a^2 - b^2 = {N}$ and $a - b = {d}$, what is $a + b$?"
    return Q(p, a + b, [N - d, F(N, 2), a, N + d, F(N, d) + d], "$a^2 - b^2 = (a - b)(a + b)$.",
             "$a + b$.", "factor the difference of squares and divide.",
             [f"$(a - b)(a + b) = {N}$.", f"${d}(a + b) = {N}$, so $a + b = {a + b}$."],
             "subtracting " + str(d) + " instead of dividing.")


@reg(S, "basics")
def fa_diff_sq_from_sum(r):
    a, b = r.randint(-8, 12), r.randint(-8, 12)
    s, pr = a + b, a * b
    ans = (a - b) ** 2
    p = f"If $a + b = {s}$ and $ab = {pr}$, what is $(a - b)^2$?"
    return Q(p, ans, [s * s, s * s + 4 * pr, s * s - 2 * pr, ans + 4, abs(s * s - pr)], "Compare $(a + b)^2$ and $(a - b)^2$.",
             "$(a - b)^2$.", "$(a - b)^2 = a^2 - 2ab + b^2 = (a + b)^2 - 4ab$.",
             [f"$(a + b)^2 = {s * s}$.", f"$(a - b)^2 = {s * s} - 4 \\cdot {par(pr)} = {ans}$."],
             "subtracting only $2ab$ (that gives $a^2 + b^2$).")


@reg(S, "basics")
def fa_nonmonic_root(r):
    a, c = r.choice([(2, 3), (3, 2), (2, 5), (3, 4), (4, 3), (5, 2), (2, 1), (3, 1)])
    pp, qq = r.randint(1, 7), r.randint(1, 7)
    # (a x - pp)(c x + qq) = 0 -> positive root pp/a
    A, B, Cc = a * c, a * qq - c * pp, -pp * qq
    root = F(pp, a)
    p = f"What is the positive solution of ${A}x^2{sg(B)}x{sg(Cc)} = 0$?"
    return Q(p, root, [F(qq, c), F(pp, c), F(-qq, c) * -1 + 1, root + 1, F(a, pp)], "Factor into two binomials.",
             "the positive root.", "factor the quadratic, then set each factor to zero.",
             [f"${A}x^2{sg(B)}x{sg(Cc)} = ({a}x - {pp})({c}x + {qq})$. Check: the outer and inner terms give ${a * qq}x - {c * pp}x = {B}x$.", f"${a}x - {pp} = 0$ gives $x = {ftex(root)}$; the other root, $-{ftex(F(qq, c))}$, is negative."],
             "solving $" + f"{a}x - {pp} = 0" + "$ as $x = " + str(pp * a) + "$.")


@reg(S, "basics")
def fa_simplify_rational(r):
    a = r.randint(1, 6)
    b, c = r.sample([x for x in range(-6, 7) if x and x != -a and x != a], 2)
    k = r.randint(-5, 9)
    if k in (0, a, -a, -b, -c, c) or k + c == 0:
        return None
    # (x^2 - a^2)/((x + a)(x + c)) = (x - a)/(x + c)
    val = F(k - a, k + c)
    p = f"What is the value of $\\dfrac{{x^2 - {a * a}}}{{x^2{sg(a + c)}x{sg(a * c)}}}$ when $x = {k}$?"
    return Q(p, val, [F(k * k - a * a, k * k), val + 1, -val if val else 1, F(k + a, k + c), F(k - a, k - c) if k != c else 2], "Factor the top and bottom.",
             "the value at $x = " + str(k) + "$.", "factor both, cancel the common factor, then substitute.",
             [f"Top: $x^2 - {a * a} = (x - {a})(x + {a})$. Bottom: $(x + {a})(x{sg(c)})$.", f"Cancel $(x + {a})$: $\\frac{{x - {a}}}{{x{sg(c)}}}$.", f"At $x = {k}$: $\\frac{{{k - a}}}{{{k + c}}} = {ftex(val)}$."],
             "canceling the $x^2$ terms, which isn't allowed across a sum.")


@reg(S, "basics")
def fa_cube_diff(r):
    a = r.randint(10, 40)
    ans = a ** 3 - (a - 1) ** 3
    p = f"What is ${a}^3 - {a - 1}^3$?"
    return Q(p, ans, [1, 3 * a * a, ans + 1, ans - 2 * a, (2 * a - 1) ** 2], "Use $x^3 - y^3 = (x - y)(x^2 + xy + y^2)$.",
             "the difference of cubes.", "with $x - y = 1$, the difference of cubes is just $x^2 + xy + y^2$.",
             [f"$x = {a}$, $y = {a - 1}$, so $x - y = 1$.", f"$x^2 + xy + y^2 = {a * a} + {a * (a - 1)} + {(a - 1) ** 2} = {ans}$."],
             "answering $1^3 = 1$ by subtracting before cubing.")


@reg(S, "basics")
def fa_sq_sum_diff(r):
    x, y = r.randint(-9, 12), r.randint(-9, 12)
    A, B = (x + y) ** 2, (x - y) ** 2
    if A == B:
        return None
    p = f"If $(x + y)^2 = {A}$ and $(x - y)^2 = {B}$, what is $xy$?"
    return Q(p, x * y, [F(A - B, 2), A - B, F(A + B, 4), x * y + 1, -x * y if x * y else 2], "Subtract the two expansions.",
             "$xy$.", "$(x + y)^2 - (x - y)^2 = 4xy$: the squares cancel.",
             [f"$(x + y)^2 - (x - y)^2 = (x^2 + 2xy + y^2) - (x^2 - 2xy + y^2) = 4xy$.", f"$4xy = {A} - {B} = {A - B}$, so $xy = {x * y}$."],
             "dividing by $2$ instead of $4$.")


@reg(S, "basics")
def fa_grouping_roots(r):
    a = r.randint(-6, 8)
    s = r.randint(2, 7)
    b = s * s
    roots = sorted({a, s, -s})
    co = [1, -a, -b, a * b]
    p = f"What is the largest real solution of $x^3{sg(-a)}x^2{sg(-b)}x{sg(a * b)} = 0$?"
    return Q(p, max(roots), [min(roots), a if a != max(roots) else -a, b, s + 1, sum(roots)], "Group the first two terms and the last two.",
             "the largest root.", "factor by grouping: pull $x^2$ out of the first pair and a number out of the second.",
             [f"$x^2(x{sg(-a)}) - {b}(x{sg(-a)}) = (x{sg(-a)})(x^2 - {b})$.", f"Roots: $x = {a}$ and $x = \\pm {s}$.", f"Largest: ${max(roots)}$."],
             "missing the negative square root of $" + str(b) + "$, or a sign slip when grouping.")


@reg(S, "basics")
def fa_sum_squares3(r):
    a, b, c = [r.randint(-6, 8) for _ in range(3)]
    s, e2 = a + b + c, a * b + b * c + c * a
    ans = a * a + b * b + c * c
    p = f"If $a + b + c = {s}$ and $ab + bc + ca = {e2}$, what is $a^2 + b^2 + c^2$?"
    return Q(p, ans, [s * s, s * s + 2 * e2, s * s - e2, ans + 2, abs(s * s - 4 * e2)], "Square $a + b + c$.",
             "$a^2 + b^2 + c^2$.", "$(a + b + c)^2 = a^2 + b^2 + c^2 + 2(ab + bc + ca)$.",
             [f"$(a + b + c)^2 = {s * s}$.", f"$a^2 + b^2 + c^2 = {s * s} - 2 \\cdot {par(e2)} = {ans}$."],
             "subtracting $ab + bc + ca$ only once.")


@reg(S, "basics")
def fa_expand_diff(r):
    a, b, c, d = [r.randint(-6, 8) for _ in range(4)]
    if a + b == c + d:
        return None
    x0 = r.randint(-5, 8)
    val = (x0 + a) * (x0 + b) - (x0 + c) * (x0 + d)
    co1, co0 = (a + b) - (c + d), a * b - c * d
    p = f"What is $(x{sg(a)})(x{sg(b)}) - (x{sg(c)})(x{sg(d)})$ when $x = {x0}$?"
    return Q(p, val, [val + co1, (x0 + a) * (x0 + b), val - co0, -val if val else 3, co1 * x0], "The $x^2$ terms cancel.",
             "the value at $x = " + str(x0) + "$.", "expand both products; the $x^2$ terms cancel, leaving a linear expression.",
             [f"First: $x^2{sg(a + b)}x{sg(a * b)}$. Second: $x^2{sg(c + d)}x{sg(c * d)}$.", f"Difference: ${co1}x{sg(co0)}$.", f"At $x = {x0}$: ${co1} \\cdot {par(x0)}{sg(co0)} = {val}$."],
             "subtracting only the first term of the second product.")


@reg(S, "basics")
def fa_near_square(r):
    N = r.choice([100, 1000, 50, 200, 500, 300])
    k = r.randint(1, 9)
    ans = N * N - k * k
    p = f"What is ${N + k} \\times {N - k}$?"
    return Q(p, ans, [N * N, N * N + k * k, ans - 1 if k > 1 else ans - 2, N * N - 2 * k, ans + 2 * k], "This is $(a + b)(a - b)$.",
             "the product.", "$(a + b)(a - b) = a^2 - b^2$, with $a = " + str(N) + "$ and $b = " + str(k) + "$.",
             [f"${N}^2 - {k}^2 = {N * N} - {k * k} = {ans}$."],
             "adding $" + str(k * k) + "$ instead of subtracting.")


@reg(S, "basics")
def fa_two_var_squares(r):
    x, y = r.randint(1, 9), r.randint(1, 9)
    A, B = 4 * x * x - 9 * y * y, 2 * x + 3 * y
    if A == 0:
        return None
    p = f"If $4x^2 - 9y^2 = {A}$ and $2x + 3y = {B}$, what is $2x - 3y$?"
    return Q(p, 2 * x - 3 * y, [A - B, F(A, 2), -(2 * x - 3 * y) if 2 * x != 3 * y else 4, A + B, 2 * x + 3 * y + 1], "$4x^2 - 9y^2 = (2x)^2 - (3y)^2$.",
             "$2x - 3y$.", "factor the difference of squares.",
             [f"$(2x + 3y)(2x - 3y) = {A}$.", f"${B}(2x - 3y) = {A}$, so $2x - 3y = {2 * x - 3 * y}$."],
             "subtracting instead of dividing.")


@reg(S, "basics")
def fa_quartic_quotient(r):
    a = r.choice([1, 2, 3, 4])
    k = r.randint(2, 9)
    ans = k * k - a * a
    p = f"What is $\\dfrac{{x^4 - {a ** 4}}}{{x^2 + {a * a}}}$ when $x = {k}$?"
    return Q(p, ans, [k * k + a * a, k ** 4 - a ** 4, ans + 2 * a * a, ans * 2, k - a], "Factor the top as a difference of squares.",
             "the value.", "$x^4 - " + str(a ** 4) + " = (x^2 + " + str(a * a) + ")(x^2 - " + str(a * a) + ")$, so the fraction simplifies.",
             [f"$\\frac{{(x^2 + {a * a})(x^2 - {a * a})}}{{x^2 + {a * a}}} = x^2 - {a * a}$.", f"At $x = {k}$: ${k * k} - {a * a} = {ans}$."],
             "dividing $x^4$ by $x^2$ and $" + str(a ** 4) + "$ by $" + str(a * a) + "$ separately.")


@reg(S, "challenge")
def fac_fourth_powers(r):
    a, b = r.randint(-5, 7), r.randint(-5, 7)
    s, t = a + b, a * a + b * b
    pr = a * b
    ans = a ** 4 + b ** 4
    p = f"If $a + b = {s}$ and $a^2 + b^2 = {t}$, what is $a^4 + b^4$?"
    return Q(p, ans, [t * t, t * t - pr * pr, s ** 4, ans + 2 * pr, t * t + 2 * pr * pr], "Find $ab$ first.",
             "$a^4 + b^4$.", "$a^4 + b^4 = (a^2 + b^2)^2 - 2a^2b^2$, and $ab$ comes from $(a + b)^2$.",
             [f"$(a + b)^2 = a^2 + b^2 + 2ab$: ${s * s} = {t} + 2ab$, so $ab = {pr}$.", f"$a^4 + b^4 = {t}^2 - 2 \\cdot {par(pr)}^2 = {t * t} - {2 * pr * pr} = {ans}$."],
             "subtracting $2ab$ instead of $2a^2b^2$.")


@reg(S, "challenge")
def fac_alt_squares(r):
    n = r.randint(5, 50)
    ans = n * (2 * n + 1)
    p = f"What is $2^2 - 1^2 + 4^2 - 3^2 + 6^2 - 5^2 + \\cdots + {2 * n}^2 - {2 * n - 1}^2$?"
    return Q(p, ans, [n * n, 2 * n * n, ans + n, n * (2 * n - 1), 4 * n], "Each pair is a difference of squares.",
             "the alternating sum.", "$(2k)^2 - (2k - 1)^2 = (2k - (2k - 1))(2k + 2k - 1) = 4k - 1$.",
             [f"Each pair simplifies: $2^2 - 1^2 = 3$, $4^2 - 3^2 = 7$, ..., ${2 * n}^2 - {2 * n - 1}^2 = {4 * n - 1}$.", f"These are just $1 + 2 + 3 + \\cdots + {2 * n}$ (each pair is the sum of its two numbers).", f"Sum: $\\frac{{{2 * n} \\cdot {2 * n + 1}}}{{2}} = {ans}$."],
             "computing each square separately.")


@reg(S, "challenge")
def fac_cubes_zero_sum(r):
    a, b = r.randint(-9, 9), r.randint(-9, 9)
    c = -a - b
    if 0 in (a, b, c):
        return None
    ans = 3 * a * b * c
    p = f"What is ${par(a)}^3 + {par(b)}^3 + {par(c)}^3$?"
    return Q(p, ans, [a * b * c, 0, ans + 3, a + b + c, -ans], "Notice that the three numbers add to $0$.",
             "the sum of cubes.", "$x^3 + y^3 + z^3 - 3xyz = (x + y + z)(\\ldots)$, so when $x + y + z = 0$, the sum of cubes is $3xyz$.",
             [f"${a} + {par(b)} + {par(c)} = 0$.", f"So the sum of cubes is $3 \\cdot {par(a)} \\cdot {par(b)} \\cdot {par(c)} = {ans}$."],
             "thinking the sum of cubes must be $0$ because the numbers add to $0$.")


@reg(S, "challenge")
def fac_largest_prime(r):
    m = r.choice([100, 1000, 120, 210, 300, 500])
    k = r.choice([1, 3, 7, 9, 11, 13])
    N = m * m - k * k
    pf = factorint(N)
    big = max(pf)
    if big < 20:
        return None
    p = f"What is the largest prime factor of ${N}$?"
    second = sorted(pf)[-2] if len(pf) > 1 else big - 2
    return Q(p, big, [m - k, m + k if m + k != big else m + k + 2, second, big + 2, k], f"${N} = {m}^2 - {k}^2$.",
             "the largest prime factor.", "spot the difference of squares to factor a large number quickly.",
             [f"${N} = {m * m} - {k * k} = {m}^2 - {k}^2 = ({m - k})({m + k})$.", f"${m - k} = " + " \\cdot ".join(f"{q}^{{{e}}}" if e > 1 else str(q) for q, e in factorint(m - k).items()) + f"$ and ${m + k} = " + " \\cdot ".join(f"{q}^{{{e}}}" if e > 1 else str(q) for q, e in factorint(m + k).items()) + "$.",
              f"The largest prime is ${big}$."],
             "stopping at $" + str(m + k) + "$, which isn't prime.")


@reg(S, "challenge")
def fac_reciprocal_trick(r):
    k = r.choice([x for x in range(-9, 10) if x not in (0, 1)])
    p = f"Distinct nonzero numbers $x$ and $y$ satisfy $x - y = {k}\\left(\\dfrac{{1}}{{y}} - \\dfrac{{1}}{{x}}\\right)$. What is $xy$?"
    return Q(p, k, [-k, 1, F(1, k), k * k, 2 * k], "Combine the fractions on the right.",
             "$xy$.", "$\\frac{1}{y} - \\frac{1}{x} = \\frac{x - y}{xy}$, which has the same $x - y$ as the left side.",
             [f"Right side: ${k} \\cdot \\frac{{x - y}}{{xy}}$.", f"Divide both sides by $x - y$ (not zero since $x \\ne y$): $1 = \\frac{{{k}}}{{xy}}$.", f"$xy = {k}$."],
             "subtracting the fractions in the wrong order and getting the opposite sign.")


@reg(S, "challenge")
def fac_four_consecutive(r):
    k = r.randint(1, 30)
    val = (k + 2) * (k + 3) * (k + 4) * (k + 5) + 1
    rt = k * k + 7 * k + 11
    assert rt * rt == val
    p = f"What is $\\sqrt{{{k + 2} \\cdot {k + 3} \\cdot {k + 4} \\cdot {k + 5} + 1}}$?"
    return Q(p, rt, [rt + 1, rt - 1, (k + 3) * (k + 4), (k + 2) * (k + 5), rt + 2], "Pair the outer two and the inner two factors.",
             "the square root.", "a product of four consecutive integers plus $1$ is always a perfect square.",
             [f"Outer pair: ${k + 2} \\cdot {k + 5} = {(k + 2) * (k + 5)}$. Inner pair: ${k + 3} \\cdot {k + 4} = {(k + 3) * (k + 4)}$. They differ by $2$.",
              f"If the two products are $m - 1$ and $m + 1$ with $m = {rt}$, then $(m - 1)(m + 1) + 1 = m^2$.", f"So the square root is ${rt}$."],
             "multiplying everything out; the pairing makes it quick.")


@reg(S, "challenge")
def fac_cube_recip(r):
    k = r.randint(3, 9)
    ans = k ** 3 - 3 * k
    p = f"If $x + \\dfrac{{1}}{{x}} = {k}$, what is $x^3 + \\dfrac{{1}}{{x^3}}$?"
    return Q(p, ans, [k ** 3, k ** 3 - k, k ** 3 + 3 * k, 3 * k, ans - 3], "Cube both sides.",
             "$x^3 + \\frac{1}{x^3}$.", "$\\left(x + \\frac{1}{x}\\right)^3 = x^3 + \\frac{1}{x^3} + 3\\left(x + \\frac{1}{x}\\right)$.",
             [f"Cube: ${k}^3 = x^3 + \\frac{{1}}{{x^3}} + 3 \\cdot {k}$.", f"$x^3 + \\frac{{1}}{{x^3}} = {k ** 3} - {3 * k} = {ans}$."],
             "cubing and forgetting the middle terms, giving $" + str(k ** 3) + "$.")


# ================================================================ alg_quadratics
S = "alg_quadratics"


@reg(S, "basics")
def q_vieta_sum(r):
    a = r.randint(2, 7)
    b, c = r.randint(-20, 20), r.randint(-20, 20)
    ans = F(-b, a)
    p = f"What is the sum of the roots of ${a}x^2{sg(b)}x{sg(c)} = 0$?"
    return Q(p, ans, [-ans if ans else 1, F(c, a), b, F(-b, c) if c else 2, ans + 1], "Use Vieta's formula.",
             "the sum of the two roots.", "for $ax^2 + bx + c = 0$, the roots add to $-\\frac{b}{a}$.",
             [f"$a = {a}$, $b = {b}$.", f"Sum $= -\\frac{{{b}}}{{{a}}} = {ftex(ans)}$."],
             "forgetting the minus sign.")


@reg(S, "basics")
def q_vieta_product(r):
    a = r.randint(2, 7)
    b, c = r.randint(-20, 20), r.choice([x for x in range(-20, 21) if x])
    ans = F(c, a)
    p = f"What is the product of the roots of ${a}x^2{sg(b)}x{sg(c)} = 0$?"
    return Q(p, ans, [-ans, F(-b, a) if b else 3, c, F(a, c), ans + 1], "Use Vieta's formula.",
             "the product of the two roots.", "for $ax^2 + bx + c = 0$, the roots multiply to $\\frac{c}{a}$.",
             [f"$a = {a}$, $c = {c}$.", f"Product $= \\frac{{{c}}}{{{a}}} = {ftex(ans)}$."],
             "adding a minus sign; only the sum has one.")


@reg(S, "basics")
def q_formula(r):
    b = r.randint(1, 8)
    c = r.randint(-10, b * b - 1)
    D = b * b - c
    k, m = simplify_sqrt(D)
    if m == 1:
        return None
    big = C(f"{b} + {'' if k == 1 else k}\\sqrt{{{m}}}", b + k * math.sqrt(m))
    p = f"What is the larger root of $x^2 - {2 * b}x{sg(c)} = 0$?"
    return Q(p, big, [C(f"{b} - {'' if k == 1 else k}\\sqrt{{{m}}}", b - k * math.sqrt(m)), C(f"{2 * b} + {'' if k == 1 else k}\\sqrt{{{m}}}", 2 * b + k * math.sqrt(m)),
                      C(f"{b} + \\sqrt{{{b * b + c}}}", b + math.sqrt(b * b + c)) if b * b + c > 0 and b * b + c != D else C(f"{b + 1} + \\sqrt{{{m}}}", b + 1 + math.sqrt(m)),
                      C(f"{b} + {2 * k}\\sqrt{{{m}}}", b + 2 * k * math.sqrt(m))],
             "Complete the square or use the quadratic formula.", "the larger root.", "complete the square: $x^2 - 2bx = (x - b)^2 - b^2$.",
             [f"$x^2 - {2 * b}x = -({c})$ becomes $(x - {b})^2 = {b * b} - ({c}) = {D}$.", f"$x - {b} = \\pm\\sqrt{{{D}}} = \\pm {'' if k == 1 else k}\\sqrt{{{m}}}$.", f"Larger root: ${big.tex}$."],
             "forgetting to halve the middle coefficient.")


@reg(S, "basics")
def q_min_value(r):
    h = r.randint(-6, 6)
    k = r.randint(-15, 15)
    b, c = -2 * h, h * h + k
    p = f"What is the smallest value of $x^2{sg(b)}x{sg(c)}$?"
    return Q(p, k, [c, h, -k if k else 1, k - h * h, h * h], "Complete the square.",
             "the minimum value of the expression.", "$(x - h)^2 \\ge 0$, so in the form $(x - h)^2 + k$ the minimum is $k$.",
             [f"$x^2{sg(b)}x{sg(c)} = (x{sg(-h)})^2 - {h * h}{sg(c)} = (x{sg(-h)})^2{sg(k)}$.", f"The square is smallest ($0$) at $x = {h}$, so the minimum is ${k}$."],
             "answering the $x$ value where the minimum happens.")


@reg(S, "basics")
def q_projectile(r):
    v = r.choice([32, 48, 64, 80, 96])
    h0 = r.choice([0, 6, 16, 20, 36, 48])
    t = F(v, 32)
    hmax = -16 * t * t + v * t + h0
    p = f"A ball's height, in feet, $t$ seconds after it is thrown is $h = -16t^2 + {v}t{sg(h0) if h0 else ''}$. What is its greatest height?"
    return Q(p, hmax, [hmax - h0 if h0 else hmax + 16, v, t, hmax + 16, v * t], "The highest point is at the vertex.",
             "the maximum height.", "a downward parabola is highest at its vertex, $t = -\\frac{b}{2a}$.",
             [f"$t = -\\frac{{{v}}}{{2 \\cdot (-16)}} = {ftex(t)}$.", f"$h = -16({ftex(t)})^2 + {v} \\cdot {ftex(t)}{sg(h0) if h0 else ''} = {ftex(hmax)}$."],
             "answering the time instead of the height.")


@reg(S, "basics")
def q_complete_square(r):
    h = r.randint(-7, 7)
    k = r.randint(-12, 12)
    if h == 0:
        return None
    b, c = 2 * h, h * h + k
    p = f"When $x^2{sg(b)}x{sg(c)}$ is written as $(x + h)^2 + k$, what is $h + k$?"
    return Q(p, h + k, [h - k, b + c, k, h * h + k, -h + k], "$h$ is half the coefficient of $x$.",
             "$h + k$.", "completing the square: $x^2 + 2hx = (x + h)^2 - h^2$.",
             [f"$h = \\frac{{{b}}}{{2}} = {h}$.", f"$(x{sg(h)})^2 = x^2{sg(b)}x + {h * h}$, so $k = {c} - {h * h} = {k}$.", f"$h + k = {h + k}$."],
             "using the whole coefficient " + str(b) + " for $h$.")


@reg(S, "basics")
def q_count_roots(r):
    a = r.randint(1, 4)
    b = r.randint(-9, 9)
    want = r.choice([0, 1, 2])
    if want == 1:
        if b % (2 * math.isqrt(a)) if math.isqrt(a) ** 2 == a else True:
            return None
        c = F(b * b, 4 * a)
    elif want == 0:
        c = F(b * b, 4 * a) + r.randint(1, 9)
    else:
        c = F(b * b, 4 * a) - r.randint(1, 9)
    if c.denominator != 1:
        return None
    c = int(c)
    D = b * b - 4 * a * c
    p = f"How many real solutions does ${a if a > 1 else ''}x^2{sg(b)}x{sg(c)} = 0$ have?"
    word = {0: "negative, so no real solutions", 1: "zero, so exactly one (a double root)", 2: "positive, so two real solutions"}[want]
    return Q(p, want, [0, 1, 2, 3, 4], "Compute the discriminant $b^2 - 4ac$.",
             "the number of real solutions.", "the discriminant $b^2 - 4ac$ tells you: positive means two, zero means one, negative means none.",
             [f"$b^2 - 4ac = {par(b)}^2 - 4 \\cdot {a} \\cdot {par(c)} = {b * b} - {par(4 * a * c)} = {D}$.", f"It is {word}."],
             "sign slips with $-4ac$ when $c$ is negative.")


@reg(S, "basics")
def q_other_root(r):
    r1, r2 = r.sample(range(-9, 10), 2)
    b = -(r1 + r2)
    p = f"One root of $x^2{sg(b)}x + c = 0$ is ${r1}$. What is the other root?"
    return Q(p, r2, [-r2 if r2 else 1, r1 * r2, -b, r2 + 1, -r1], "Use the sum of the roots.",
             "the other root.", "the roots add to $-b$, and you know one of them.",
             [f"Sum of roots: $-({b}) = {-b}$.", f"Other root: ${-b} - {par(r1)} = {r2}$."],
             "subtracting in the wrong direction.")


@reg(S, "basics")
def q_build(r):
    p1, p2 = r.sample(range(-8, 9), 2)
    b, c = -(p1 + p2), p1 * p2
    p = f"The equation $x^2 + bx + c = 0$ has roots ${p1}$ and ${p2}$. What is $b + c$?"
    return Q(p, b + c, [p1 + p2 + c, b - c, -(b + c) if b + c else 3, c, b], f"Write it as $(x{sg(-p1)})(x{sg(-p2)})$.",
             "$b + c$.", "a quadratic with roots $r$ and $s$ is $(x - r)(x - s) = x^2 - (r + s)x + rs$.",
             [f"$b = -({p1} + {par(p2)}) = {b}$.", f"$c = {par(p1)} \\cdot {par(p2)} = {c}$.", f"$b + c = {b + c}$."],
             "forgetting the minus sign on $b$.")


@reg(S, "basics")
def q_area_word(r):
    w = r.randint(3, 15)
    k = r.randint(1, 8)
    A = w * (w + k)
    p = f"A garden's length is ${k}$ m more than its width, and its area is ${A}$ square meters. What is its width, in meters?"
    return Q(p, w, [w + k, F(A, 2), w - 1, A // k if A % k == 0 else w + 2, round(math.sqrt(A))], "Let the width be $w$.",
             "the width.", "write the area as a quadratic in $w$ and factor.",
             [f"$w(w + {k}) = {A}$, so $w^2 + {k}w - {A} = 0$.", f"Factor: $(w - {w})(w + {w + k}) = 0$.", f"Width must be positive: $w = {w}$."],
             "answering the length.")


@reg(S, "basics")
def q_consecutive_product(r):
    n = r.randint(5, 40)
    P = n * (n + 1)
    p = f"The product of two consecutive positive integers is ${P}$. What is their sum?"
    return Q(p, 2 * n + 1, [n, n + 1, 2 * n, 2 * n + 3, round(math.sqrt(P)) * 2], "Estimate with a square root.",
             "the sum of the two integers.", "two consecutive integers are close to $\\sqrt{P}$.",
             [f"$\\sqrt{{{P}}}$ is between ${n}$ and ${n + 1}$.", f"Check: ${n} \\cdot {n + 1} = {P}$.", f"Sum: ${2 * n + 1}$."],
             "answering one of the numbers instead of the sum.")


@reg(S, "basics")
def q_intercept_gap(r):
    r1, r2 = r.sample(range(-9, 10), 2)
    a = r.choice([1, 2, -1])
    b, c = -a * (r1 + r2), a * r1 * r2
    p = f"How far apart are the two $x$-intercepts of $y = {'' if a == 1 else '-' if a == -1 else a}x^2{sg(b)}x{sg(c)}$?"
    return Q(p, abs(r1 - r2), [abs(r1 + r2), abs(r1 * r2), abs(c), abs(r1 - r2) + 1, max(abs(r1), abs(r2))], "Find the roots.",
             "the distance between the roots.", "the $x$-intercepts are the roots; factor to find them.",
             [f"$y = {'' if a == 1 else '-' if a == -1 else a}(x{sg(-r1)})(x{sg(-r2)})$.", f"Roots: ${min(r1, r2)}$ and ${max(r1, r2)}$.", f"Distance: ${abs(r1 - r2)}$."],
             "adding the roots instead of subtracting.")


@reg(S, "basics")
def q_symmetry(r):
    a_, b_ = r.sample(range(-10, 11), 2)
    k = r.randint(-10, 10)
    ax = F(a_ + b_, 2)
    p = f"A parabola passes through $({a_}, {k})$ and $({b_}, {k})$. What is the $x$-coordinate of its vertex?"
    return Q(p, ax, [a_ + b_, k, abs(a_ - b_), ax + 1, F(abs(a_ - b_), 2)], "Points at the same height are mirror images.",
             "the vertex's $x$-coordinate.", "a parabola is symmetric about the vertical line through its vertex.",
             [f"Same height ${k}$, so the axis is halfway between $x = {a_}$ and $x = {b_}$.", f"$\\frac{{{a_} + {par(b_)}}}{{2}} = {ftex(ax)}$."],
             "using the $y$-coordinate.")


@reg(S, "basics")
def q_recip_sum(r):
    r1, r2 = r.sample([x for x in range(-9, 10) if x], 2)
    b, c = -(r1 + r2), r1 * r2
    ans = F(r1 + r2, r1 * r2)
    p = f"Let $r$ and $s$ be the roots of $x^2{sg(b)}x{sg(c)} = 0$. What is $\\dfrac{{1}}{{r}} + \\dfrac{{1}}{{s}}$?"
    return Q(p, ans, [F(c, -b) if b else 4, -ans if ans else 1, F(1, r1 + r2) if r1 + r2 else 5, F(r1 * r2, 1), ans + 1], "Combine the fractions.",
             "$\\frac{1}{r} + \\frac{1}{s}$.", "$\\frac{1}{r} + \\frac{1}{s} = \\frac{r + s}{rs}$, and Vieta gives both pieces.",
             [f"$r + s = {-b}$ and $rs = {c}$.", f"$\\frac{{{-b}}}{{{c}}} = {ftex(ans)}$."],
             "flipping the fraction to $\\frac{rs}{r + s}$.")


@reg(S, "basics")
def q_square_solutions(r):
    a = r.randint(-8, 8)
    b = r.choice([4, 9, 16, 25, 2, 3, 5])
    p = f"What is the sum of the solutions of $(x{sg(-a)})^2 = {b}$?"
    return Q(p, 2 * a, [a, b, 2 * a + 1, -2 * a if a else 2, 2 * b], "The two solutions are mirror images around " + str(a) + ".",
             "the sum of the solutions.", "$(x - a)^2 = b$ gives $x = a \\pm \\sqrt{b}$; the $\\pm$ parts cancel when added.",
             [f"$x{sg(-a)} = \\pm\\sqrt{{{b}}}$, so $x = {a} \\pm \\sqrt{{{b}}}$.", f"Sum: $2 \\cdot {par(a)} = {2 * a}$."],
             "forgetting the negative square root and answering one solution.")


@reg(S, "basics")
def q_sum_squares_roots(r):
    b = r.randint(2, 12)
    c = r.randint(1, b * b // 4)
    ans = b * b - 2 * c
    p = f"What is the sum of the squares of the solutions of $x + \\dfrac{{{c}}}{{x}} = {b}$?"
    return Q(p, ans, [b * b, b * b + 2 * c, ans + c, b, c], "Multiply by $x$ to get a quadratic.",
             "$r^2 + s^2$.", "clear the fraction, then use $r^2 + s^2 = (r + s)^2 - 2rs$.",
             [f"$x^2 - {b}x + {c} = 0$, so $r + s = {b}$ and $rs = {c}$.", f"$r^2 + s^2 = {b * b} - {2 * c} = {ans}$."],
             "forgetting to subtract $2rs$.")


@reg(S, "challenge")
def qc_root_gap(r):
    b = r.randint(-12, 12)
    c = r.randint(-30, b * b // 4)
    D = b * b - 4 * c
    if D <= 0:
        return None
    ans = rad(1, D)
    p = f"What is the positive difference between the roots of $x^2{sg(b)}x{sg(c)} = 0$?"
    return Q(p, ans, [rad(1, abs(b * b - 2 * c) or 3), num(abs(b)), rad(2, D), rad(F(1, 2), D), num(abs(c))], "$(r - s)^2 = (r + s)^2 - 4rs$.",
             "$|r - s|$.", "you don't need the roots themselves: $(r - s)^2 = (r + s)^2 - 4rs$, both from Vieta.",
             [f"$r + s = {-b}$ and $rs = {c}$.", f"$(r - s)^2 = {b * b} - 4 \\cdot {par(c)} = {D}$.", f"$|r - s| = \\sqrt{{{D}}} = {ans.tex}$."],
             "using $2rs$ instead of $4rs$.")


@reg(S, "challenge")
def qc_reciprocal_roots(r):
    r1, r2 = r.sample([x for x in range(-6, 7) if x], 2)
    b, c = -(r1 + r2), r1 * r2
    pp = -F(r1 + r2, r1 * r2)
    qq = F(1, r1 * r2)
    p = f"Let $r$ and $s$ be the roots of $x^2{sg(b)}x{sg(c)} = 0$. The equation $x^2 + px + q = 0$ has roots $\\dfrac{{1}}{{r}}$ and $\\dfrac{{1}}{{s}}$. What is $p + q$?"
    return Q(p, pp + qq, [-(pp + qq) if pp + qq else 1, F(b, c), pp - qq, F(b + 1, c), b + c], "New sum: $\\frac{1}{r} + \\frac{1}{s}$. New product: $\\frac{1}{rs}$.",
             "$p + q$.", "$p = -(\\text{sum of new roots})$ and $q = \\text{product of new roots}$.",
             [f"$r + s = {-b}$, $rs = {c}$.", f"New sum $= \\frac{{r + s}}{{rs}} = {ftex(F(-b, c))}$, so $p = {ftex(pp)}$.", f"New product $= \\frac{{1}}{{rs}} = {ftex(qq)}$, so $q = {ftex(qq)}$.", f"$p + q = {ftex(pp + qq)}$."],
             "forgetting the minus sign that turns the new sum into $p$.")


@reg(S, "challenge")
def qc_double_root_k(r):
    a = r.randint(1, 5)
    c0 = r.randint(1, 20)
    # x^2 - 2kx + (a k + c0) = 0 double root: k^2 = a k + c0 -> k^2 - a k - c0 = 0; sum of k = a
    D = a * a + 4 * c0
    p = f"For which values of $k$ does $x^2 - 2kx + {a if a > 1 else ''}k + {c0} = 0$ have exactly one real solution? Give the sum of all such $k$."
    return Q(p, a, [-a, c0, 2 * a, a + c0, -c0], "Set the discriminant to $0$.",
             "the sum of the valid $k$.", "exactly one solution means the discriminant is $0$; that gives a quadratic in $k$.",
             [f"Discriminant: $(2k)^2 - 4({a if a > 1 else ''}k + {c0}) = 0$, so $k^2 - {a if a > 1 else ''}k - {c0} = 0$.", f"Its discriminant is ${D} > 0$, so there are two real $k$.", f"By Vieta, their sum is ${a}$."],
             "solving for each $k$ separately; Vieta gives the sum directly.")


@reg(S, "challenge")
def qc_min_c(r):
    b = r.choice([2, 4, 6, 8, 10, -4, -6])
    m = r.randint(-5, 10)
    c = m + b * b // 4
    p = f"What is the smallest number $c$ such that $x^2{sg(b)}x + c \\ge {m}$ for every real $x$?"
    return Q(p, c, [m, b * b // 4, c + 1, m - b * b // 4, b * b], "The left side is smallest at its vertex.",
             "the least $c$ that keeps the expression at least " + str(m) + ".", "the minimum of $x^2 + bx + c$ is $c - \\frac{b^2}{4}$.",
             [f"Minimum of $x^2{sg(b)}x + c$: $c - \\frac{{{b * b}}}{{4}} = c - {b * b // 4}$.", f"Need $c - {b * b // 4} \\ge {m}$, so $c \\ge {c}$."],
             "forgetting the vertex and just setting $c = " + str(m) + "$.")


@reg(S, "challenge")
def qc_max_product(r):
    a, b = r.sample([1, 2, 3, 4, 5], 2)
    cc = r.choice([12, 24, 36, 48, 60]) // (1 if True else 1)
    ans = F(cc * cc, 4 * a * b)
    p = f"Positive numbers $x$ and $y$ satisfy ${a if a > 1 else ''}x + {b if b > 1 else ''}y = {cc}$. What is the largest possible value of $xy$?"
    return Q(p, ans, [F(cc * cc, 4), F(cc * cc, a * b), ans * 2, F(cc, 2), ans + 1], "Write $y$ in terms of $x$; you get a downward parabola.",
             "the maximum of $xy$.", "the product is a quadratic in $x$; its maximum is at the vertex.",
             [f"$y = \\frac{{{cc} - {a}x}}{{{b}}}$, so $xy = \\frac{{{cc}x - {a}x^2}}{{{b}}}$.", f"Vertex: $x = \\frac{{{cc}}}{{{2 * a}}} = {ftex(F(cc, 2 * a))}$, then $y = {ftex(F(cc, 2 * b))}$.", f"$xy = {ftex(F(cc, 2 * a))} \\cdot {ftex(F(cc, 2 * b))} = {ftex(ans)}$."],
             "setting $x = y$; that maximizes only when the coefficients are equal.")


@reg(S, "challenge")
def qc_r2s_rs2(r):
    r1, r2 = r.sample(range(-7, 8), 2)
    b, c = -(r1 + r2), r1 * r2
    ans = c * (-b)
    p = f"Let $r$ and $s$ be the roots of $x^2{sg(b)}x{sg(c)} = 0$. What is $r^2s + rs^2$?"
    return Q(p, ans, [-ans if ans else 2, c + (-b), c * c, b * b - 2 * c, ans + c], "Factor out $rs$.",
             "$r^2s + rs^2$.", "$r^2s + rs^2 = rs(r + s)$.",
             [f"$rs = {c}$ and $r + s = {-b}$.", f"$rs(r + s) = {par(c)} \\cdot {par(-b)} = {ans}$."],
             "using $b$ instead of $-b$ for the sum.")


@reg(S, "challenge")
def qc_three_points(r):
    a, b, c = r.choice([-3, -2, -1, 1, 2, 3]), r.randint(-6, 6), r.randint(-8, 8)
    f = lambda x: a * x * x + b * x + c
    p = f"The parabola $y = ax^2 + bx + c$ passes through $(-1, {f(-1)})$, $(0, {f(0)})$, and $(2, {f(2)})$. What is $a + b + c$?"
    return Q(p, f(1), [f(-1), f(2), a + b, f(1) + 1, f(0) + f(2)], "$a + b + c$ is the value at $x = 1$.",
             "$a + b + c$.", "find $a$, $b$, $c$ from the three points, then add.",
             [f"$x = 0$ gives $c = {c}$.", f"$x = -1$: $a - b{sg(c)} = {f(-1)}$, so $a - b = {a - b}$.", f"$x = 2$: $4a + 2b{sg(c)} = {f(2)}$, so $2a + b = {2 * a + b}$.",
              f"Adding: $3a = {3 * a}$, so $a = {a}$ and $b = {b}$.", f"$a + b + c = {f(1)}$."],
             "answering one of the given $y$ values.")


# ================================================================ alg_absolute
S = "alg_absolute"


@reg(S, "basics")
def ab_nested_eval(r):
    a, b, c = [r.randint(-12, 12) for _ in range(3)]
    ans = abs(a - abs(b - c))
    p = f"What is $\\left|{a} - \\left|{b} - {par(c)}\\right|\\right|$?"
    return Q(p, ans, [abs(a - (b - c)), abs(a) + abs(b - c), a - abs(b - c), ans + 2, abs(a + abs(b - c))], "Work from the inside out.",
             "the value.", "evaluate the inner absolute value first.",
             [f"$|{b} - {par(c)}| = |{b - c}| = {abs(b - c)}$.", f"$|{a} - {abs(b - c)}| = |{a - abs(b - c)}| = {ans}$."],
             "dropping the inner absolute value.")


@reg(S, "basics")
def ab_larger_solution(r):
    a, b = r.randint(-10, 10), r.randint(1, 12)
    p = f"What is the larger solution of $|x{sg(-a)}| = {b}$?"
    return Q(p, a + b, [a - b, b, a, -a + b, 2 * b], "The number $x$ is " + str(b) + " units from " + str(a) + ".",
             "the larger solution.", "$|x - a| = b$ means $x$ is $b$ units from $a$ on the number line.",
             [f"$x{sg(-a)} = {b}$ or $x{sg(-a)} = -{b}$.", f"$x = {a + b}$ or $x = {a - b}$.", f"Larger: ${a + b}$."],
             "only using the positive case and making a sign slip with $a$.")


@reg(S, "basics")
def ab_equal_distance(r):
    a, b = r.sample(range(-10, 15), 2)
    ans = F(a + b, 2)
    p = f"Solve $|x{sg(-a)}| = |x{sg(-b)}|$."
    return Q(p, ans, [a + b, F(a - b, 2), ans + 1, a, F(abs(a - b), 2)], "$x$ is the same distance from " + str(a) + " and " + str(b) + ".",
             "$x$.", "equal distances from two points means the midpoint.",
             [f"$x$ is equally far from ${a}$ and ${b}$.", f"Midpoint: $\\frac{{{a} + {par(b)}}}{{2}} = {ftex(ans)}$."],
             "setting $x - a = x - b$, which has no solution; you need the case $x - a = -(x - b)$.")


@reg(S, "basics")
def ab_compound(r):
    lo, hi = r.randint(-20, 5), r.randint(8, 30)
    a = r.choice([2, 3])
    b = r.randint(-5, 5)
    xs = [x for x in range(-100, 100) if lo < a * x + b < hi]
    p = f"How many integers $x$ satisfy ${lo} < {a}x{sg(b)} < {hi}$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, hi - lo, len(xs) + 2, F(hi - lo, a)], "Undo the operations on all three parts.",
             "the integer count.", "subtract and divide through all three parts of the inequality.",
             [f"Subtract ${b}$: ${lo - b} < {a}x < {hi - b}$.", f"Divide by ${a}$: ${ftex(F(lo - b, a))} < x < {ftex(F(hi - b, a))}$.", f"Integers from ${xs[0]}$ to ${xs[-1]}$: ${len(xs)}$."],
             "including the endpoints when the inequalities are strict.")


@reg(S, "basics")
def ab_outside(r):
    a = r.randint(-5, 5)
    b = r.randint(2, 6)
    N = r.randint(8, 12)
    xs = [x for x in range(-N, N + 1) if abs(x - a) >= b]
    p = f"How many integers $x$ with $-{N} \\le x \\le {N}$ satisfy $|x{sg(-a)}| \\ge {b}$?"
    return Q(p, len(xs), [2 * N + 1 - len(xs), len(xs) + 1, 2 * N + 1, len(xs) - 1, 2 * b - 1], "Count the integers that fail, then subtract.",
             "the count.", "$|x - a| < b$ is a short interval; everything else in the range works.",
             [f"Total integers from $-{N}$ to ${N}$: ${2 * N + 1}$.", f"Failing ones: $|x{sg(-a)}| < {b}$, so ${a - b + 1} \\le x \\le {a + b - 1}$: ${2 * b - 1}$ integers.", f"Working: ${2 * N + 1} - {2 * N + 1 - len(xs)} = {len(xs)}$."],
             "counting the failing integers as the answer.")


@reg(S, "basics")
def ab_largest_int(r):
    a = r.randint(1, 20)
    b = r.randint(3, 15)
    xs = [x for x in range(-100, 100) if abs(2 * x - a) <= b]
    p = f"What is the largest integer $x$ with $|2x - {a}| \\le {b}$?"
    return Q(p, xs[-1], [xs[0], xs[-1] + 1, F(a + b, 2) if F(a + b, 2) != xs[-1] else xs[-1] - 1, a + b, b], "Rewrite without the absolute value.",
             "the largest integer that works.", "$|y| \\le b$ means $-b \\le y \\le b$.",
             [f"$-{b} \\le 2x - {a} \\le {b}$.", f"${a - b} \\le 2x \\le {a + b}$, so ${ftex(F(a - b, 2))} \\le x \\le {ftex(F(a + b, 2))}$.", f"Largest integer: ${xs[-1]}$."],
             "rounding up past the boundary.")


@reg(S, "basics")
def ab_flip(r):
    a = r.randint(2, 6)
    b, c = r.randint(-10, 10), r.randint(-20, 20)
    xs = [x for x in range(-100, 100) if -a * x + b > c]
    p = f"What is the largest integer $x$ with $-{a}x{sg(b)} > {c}$?"
    return Q(p, xs[-1], [xs[-1] + 1, -xs[-1] if xs[-1] else 1, F(c - b, -a), xs[-1] - 1, F(b - c, a) + 1], "Dividing by a negative flips the inequality.",
             "the largest integer solution.", "when you divide both sides by a negative number, the inequality sign reverses.",
             [f"$-{a}x > {c - b}$.", f"Divide by $-{a}$ and flip: $x < {ftex(F(c - b, -a))}$.", f"Largest integer: ${xs[-1]}$."],
             "forgetting to flip the sign.")


@reg(S, "basics")
def ab_neg_simplify(r):
    k = r.randint(2, 20)
    p = f"If $x = -{k}$, what is $\\big|x - |x|\\big|$?"
    return Q(p, 2 * k, [0, k, -2 * k, k * k, 2 * k + 1], "Start with $|x|$.",
             "the value.", "for a negative $x$, $|x| = -x$.",
             [f"$|x| = {k}$.", f"$x - |x| = -{k} - {k} = -{2 * k}$.", f"$|-{2 * k}| = {2 * k}$."],
             "thinking $x - |x|$ is always $0$.")


@reg(S, "basics")
def ab_box_area(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    p = f"What is the area of the region of points $(x, y)$ with $|x| \\le {a}$ and $|y| \\le {b}$?"
    return Q(p, 4 * a * b, [a * b, 2 * a * b, (a + b) ** 2, 2 * (a + b), 4 * (a + b)], "Draw it: it's a rectangle.",
             "the area.", "$|x| \\le a$ means $-a \\le x \\le a$: a strip of width $2a$.",
             [f"Width: $2 \\cdot {a} = {2 * a}$. Height: $2 \\cdot {b} = {2 * b}$.", f"Area: ${2 * a} \\cdot {2 * b} = {4 * a * b}$."],
             "using width $a$ instead of $2a$.")


@reg(S, "basics")
def ab_extraneous(r):
    a = r.randint(1, 10)
    b = r.randint(-5, 10)
    # |x + a| = 2x + b
    sols = []
    x1 = F(a - b, 1)       # x + a = 2x + b -> x = a - b, need x + a >= 0
    if x1 + a >= 0 and 2 * x1 + b >= 0:
        sols.append(x1)
    x2 = F(-a - b, 3)      # -(x + a) = 2x + b -> x = (-a - b)/3, need x + a < 0
    if x2 + a < 0 and 2 * x2 + b >= 0:
        sols.append(x2)
    if len(sols) != 1:
        return None
    ans = sols[0]
    p = f"Solve $|x + {a}| = 2x{sg(b)}$."
    return Q(p, ans, [x2 if ans != x2 else x1, ans + 1, -ans if ans else 2, F(a + b, 1), F(a - b, 3)], "Split into two cases and check each answer.",
             "the solution.", "split on the sign inside the absolute value, then check: an absolute value can't equal a negative number.",
             [f"Case $x + {a} \\ge 0$: $x + {a} = 2x{sg(b)}$ gives $x = {ftex(x1)}$." + ("" if x1 in sols else " Check fails."), f"Case $x + {a} < 0$: $-x - {a} = 2x{sg(b)}$ gives $x = {ftex(x2)}$." + ("" if x2 in sols else " Check fails."),
              f"Only $x = {ftex(ans)}$ works."],
             "keeping an answer that makes the right side negative.")


@reg(S, "basics")
def ab_plans(r):
    f1, r1 = r.randint(10, 30), r.choice([F(10, 100), F(15, 100), F(20, 100), F(25, 100)])
    f2, r2 = f1 + r.randint(5, 25), r1 - F(r.choice([5, 10]), 100)
    if r2 <= 0:
        return None
    x = (f2 - f1) / (r1 - r2)
    m = math.floor(x) + 1
    p = f"Phone plan A costs \\${f1} a month plus \\${float(r1):.2f} per minute. Plan B costs \\${f2} a month plus \\${float(r2):.2f} per minute. What is the least whole number of minutes for which plan B costs less?"
    return Q(p, m, [m - 1, m + 1, math.ceil(x * 2), f2 - f1, m + 10], "Set up an inequality for B less than A.",
             "the smallest number of minutes that makes B cheaper.", "write each cost as fee $+$ rate $\\times$ minutes and solve B $<$ A.",
             [f"${f2} + {float(r2):.2f}m < {f1} + {float(r1):.2f}m$.", f"${f2 - f1} < {float(r1 - r2):.2f}m$, so $m > {ftex(x)}$.", f"Least whole number: ${m}$."],
             "giving the break even point, where the plans cost the same.")


@reg(S, "basics")
def ab_interval_form(r):
    p_, q_ = sorted(r.sample(range(-15, 20), 2))
    m, rad_ = F(p_ + q_, 2), F(q_ - p_, 2)
    p = f"The inequality ${p_} \\le x \\le {q_}$ can be written as $|x - m| \\le r$. What is $m + r$?"
    return Q(p, m + rad_, [m, rad_, q_ - p_, p_ + q_, m - rad_ if m - rad_ != m + rad_ else 1], "$m$ is the center; $r$ is the distance from the center to an end.",
             "$m + r$.", "$|x - m| \\le r$ is the interval from $m - r$ to $m + r$.",
             [f"Center: $m = \\frac{{{p_} + {par(q_)}}}{{2}} = {ftex(m)}$.", f"Radius: $r = \\frac{{{q_} - {par(p_)}}}{{2}} = {ftex(rad_)}$.", f"$m + r = {ftex(m + rad_)}$ (which is just the right end, ${q_}$)."],
             "using the full width for $r$.")


@reg(S, "basics")
def ab_sum_integers(r):
    a = r.randint(-10, 10)
    b = r.randint(2, 8)
    xs = [x for x in range(-50, 50) if abs(x - a) < b]
    p = f"What is the sum of all integers $x$ with $|x{sg(-a)}| < {b}$?"
    return Q(p, sum(xs), [a, sum(xs) + a, len(xs), sum(xs) - a, a * (2 * b + 1)], "The integers are symmetric around " + str(a) + ".",
             "the sum.", "the solutions pair up symmetrically around $" + str(a) + "$, so the sum is $" + str(a) + "$ times the count.",
             [f"${a - b + 1} \\le x \\le {a + b - 1}$: ${len(xs)}$ integers.", f"Average ${a}$, so sum $= {a} \\cdot {len(xs)} = {sum(xs)}$."],
             "including the endpoints, which the strict inequality excludes.")


@reg(S, "basics")
def ab_path(r):
    a, b, c = r.sample(range(-15, 16), 3)
    ans = abs(a - b) + abs(b - c)
    p = f"An ant walks along a number line from ${a}$ to ${b}$, then from ${b}$ to ${c}$. How far does it walk in total?"
    return Q(p, ans, [abs(a - c), abs(a - b), ans + 1, abs(a + b + c), abs(a - b) + abs(c)], "Add the two distances.",
             "the total distance.", "distance on a number line is the absolute value of the difference.",
             [f"First leg: $|{a} - {par(b)}| = {abs(a - b)}$.", f"Second leg: $|{b} - {par(c)}| = {abs(b - c)}$.", f"Total: ${ans}$."],
             "using only the start and end points; the ant may double back.")


@reg(S, "basics")
def ab_xy_values(r):
    a, b = r.sample(range(1, 13), 2)
    vals = sorted({abs(x + y) for x in (a, -a) for y in (b, -b)})
    p = f"If $|x| = {a}$ and $|y| = {b}$, what is the sum of all possible values of $|x + y|$?"
    return Q(p, sum(vals), [a + b, abs(a - b), 2 * (a + b), sum(vals) + abs(a - b), 2 * max(a, b)], "List the four sign combinations.",
             "the sum of the different values of $|x + y|$.", "$x = \\pm" + str(a) + "$, $y = \\pm" + str(b) + "$; same signs add, opposite signs subtract.",
             [f"Same signs: $|x + y| = {a + b}$. Opposite signs: $|x + y| = {abs(a - b)}$.", f"Sum of different values: ${a + b} + {abs(a - b)} = {sum(vals)}$."],
             "counting the same value twice.")


@reg(S, "basics")
def ab_sqrt_square(r):
    a, b = sorted(r.sample(range(-10, 15), 2))
    k = r.randint(a + 1, b - 1) if b - a > 1 else None
    if k is None:
        return None
    ans = (k - a) + (b - k)
    p = f"If $x = {k}$, what is $\\sqrt{{(x{sg(-a)})^2}} + \\sqrt{{(x{sg(-b)})^2}}$?"
    return Q(p, ans, [abs(2 * k - a - b), (k - a) - (b - k) if (k - a) != (b - k) else 1, ans + 2, k - a, a + b], "$\\sqrt{y^2} = |y|$.",
             "the value.", "a square root of a square is the absolute value, not the original number.",
             [f"$\\sqrt{{({k}{sg(-a)})^2}} = |{k - a}| = {k - a}$.", f"$\\sqrt{{({k}{sg(-b)})^2}} = |{k - b}| = {b - k}$.", f"Sum: ${ans}$."],
             "writing $\\sqrt{y^2} = y$, which gives a negative value for the second term.")


@reg(S, "challenge")
def abc_three_abs_min(r):
    a, b, c = sorted(r.sample(range(-12, 13), 3))
    ans = c - a
    p = f"What is the minimum value of $|x{sg(-a)}| + |x{sg(-b)}| + |x{sg(-c)}|$ over all real $x$?"
    return Q(p, ans, [c - a + abs(b), abs(a) + abs(b) + abs(c), (c - a) + (b - a), ans + 1, F(c - a, 2)], "Think of distances on a number line.",
             "the smallest total distance.", "the sum of distances to several points is smallest at the median point.",
             [f"The points are ${a}$, ${b}$, ${c}$; the median is ${b}$.", f"At $x = {b}$: ${b - a} + 0 + {c - b} = {ans}$."],
             "choosing $x$ at the average instead of the median.")


@reg(S, "challenge")
def abc_double_abs(r):
    a = r.randint(-5, 5)
    b, c = r.randint(1, 8), r.randint(1, 8)
    sols = {a + s1 * (b + s2 * c) for s1 in (1, -1) for s2 in (1, -1) if b + s2 * c >= 0}
    p = f"How many real solutions does $\\big||x{sg(-a)}| - {b}\\big| = {c}$ have?"
    return Q(p, len(sols), [4, 2, 3, 1, 0], "Peel off one absolute value at a time.",
             "the number of solutions.", "$|u| = c$ gives $u = \\pm c$; then each value of $|x - a|$ must be nonnegative.",
             [f"$|x{sg(-a)}| - {b} = \\pm {c}$, so $|x{sg(-a)}| = {b + c}$ or $|x{sg(-a)}| = {b - c}$.",
              (f"${b - c} < 0$ is impossible for an absolute value." if b - c < 0 else (f"$|x{sg(-a)}| = 0$ has one solution." if b == c else f"Both are positive, so each gives two solutions.")),
              f"Total: ${len(sols)}$."],
             "counting all four cases without checking for negative values.", sort=True)


@reg(S, "challenge")
def abc_v_area(r):
    a = r.randint(-6, 6)
    b = r.randint(2, 10)
    p = f"What is the area of the region enclosed by $y = |x{sg(-a)}|$ and $y = {b}$?"
    return Q(p, b * b, [2 * b * b, F(b * b, 2), b, 2 * b, b * b + a], "It's a triangle.",
             "the area.", "the V shape and the horizontal line form a triangle with apex at $(" + str(a) + ", 0)$.",
             [f"The line $y = {b}$ meets the V at $x = {a - b}$ and $x = {a + b}$: base ${2 * b}$.", f"Height ${b}$. Area $= \\frac{{1}}{{2}} \\cdot {2 * b} \\cdot {b} = {b * b}$."],
             "using half the base.")


@reg(S, "challenge")
def abc_rhombus(r):
    a = r.randint(2, 12)
    k = r.choice([2, 3])
    area = F(2 * a * a, k)
    p = f"What is the area of the region enclosed by the graph of $|x| + {k}|y| = {a}$?"
    return Q(p, area, [a * a, 2 * a * a, F(a * a, k), area * 2, 4 * a], "Find where the graph meets the axes.",
             "the area of the diamond.", "the graph is a rhombus; its area is half the product of its diagonals.",
             [f"$x$-intercepts $\\pm {a}$: horizontal diagonal ${2 * a}$.", f"$y$-intercepts $\\pm {ftex(F(a, k))}$: vertical diagonal ${ftex(F(2 * a, k))}$.", f"Area $= \\frac{{1}}{{2}} \\cdot {2 * a} \\cdot {ftex(F(2 * a, k))} = {ftex(area)}$."],
             "treating it as a square with side " + str(a) + ".")


@reg(S, "challenge")
def abc_rational_ineq(r):
    a, b = sorted(r.sample(range(-10, 15), 2))
    if b - a < 2:
        return None
    xs = [x for x in range(a + 1, b)]
    p = f"How many integers $x$ satisfy $\\dfrac{{x{sg(-a)}}}{{x{sg(-b)}}} < 0$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) + 2, b - a, len(xs) - 1, 0], "A fraction is negative when its top and bottom have opposite signs.",
             "the integer count.", "the sign changes only at $x = " + str(a) + "$ and $x = " + str(b) + "$; check the region between them.",
             [f"Between ${a}$ and ${b}$, the top is positive and the bottom negative, so the fraction is negative.", "Outside, both have the same sign. At the endpoints the fraction is $0$ or undefined.", f"Integers from ${a + 1}$ to ${b - 1}$: ${len(xs)}$."],
             "including an endpoint.")


@reg(S, "challenge")
def abc_square_abs(r):
    a = r.choice([10, 15, 20, 25, 30, 40, 50])
    b = r.randint(5, 20)
    xs = [x for x in range(-100, 101) if abs(x * x - a) < b]
    if not xs:
        return None
    p = f"How many integers $x$ satisfy $|x^2 - {a}| < {b}$?"
    return Q(p, len(xs), [len(xs) // 2 if len(xs) > 1 else 3, len(xs) + 2, len(xs) - 1 if len(xs) > 1 else 4, 2 * b, len(xs) + 1], "Solve for $x^2$ first.",
             "the integer count.", "find the range of $x^2$, then remember both $x$ and $-x$.",
             [f"${a - b} < x^2 < {a + b}$.", "Squares in that range: " + ", ".join(f"${x * x}$" for x in sorted({abs(x) for x in xs})) + ".", f"Each nonzero one gives $\\pm x$: total ${len(xs)}$."],
             "forgetting the negative values of $x$.")


@reg(S, "challenge")
def abc_graph_count(r):
    a, b = sorted(r.sample(range(-8, 9), 2))
    c = r.randint(b - a + 1, b - a + 10)
    xs = [x for x in range(-50, 51) if abs(x - a) + abs(x - b) <= c]
    p = f"For how many integers $x$ is $|x{sg(-a)}| + |x{sg(-b)}| \\le {c}$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, c, b - a + 1, 2 * c], "Between " + str(a) + " and " + str(b) + " the sum is constant.",
             "the integer count.", "the sum of distances to " + str(a) + " and " + str(b) + " equals " + str(b - a) + " between them and grows outside.",
             [f"For ${a} \\le x \\le {b}$ the sum is ${b - a} \\le {c}$: all work.", f"Outside, the sum is $|2x{sg(-(a + b))}|$. Setting it $\\le {c}$ gives ${ftex(F(a + b - c, 2))} \\le x \\le {ftex(F(a + b + c, 2))}$.", f"Integers from ${xs[0]}$ to ${xs[-1]}$: ${len(xs)}$."],
             "forgetting that the sum is flat between the two points.")
