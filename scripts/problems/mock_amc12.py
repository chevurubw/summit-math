"""Mock exam families on AMC 12 only topics, difficulty levels 2 to 6."""
import cmath
import math
from fractions import Fraction as F

from common import explain, num
from mock_common import family, pi_mult, polystr, surd

T = "amc12"

# ============================================================ LEVEL 2 (AMC 12 #1 to 5)


@family("x2_trig_double", 2, "trigonometry", "trig_identities", T)
def _(r):
    c2 = F(r.choice([1, 2, 3, 4, 5, 7]), r.choice([8, 9, 25, 5, 4, 10]))
    if abs(c2) >= 1:
        return None
    if r.random() < 0.5:
        c2 = -c2
    ask = r.choice(["sin2", "cos2"])
    ans = (1 - c2) / 2 if ask == "sin2" else (1 + c2) / 2
    fn = "\\sin" if ask == "sin2" else "\\cos"
    form = "1 - 2\\sin^2\\theta" if ask == "sin2" else "2\\cos^2\\theta - 1"
    p = f"If $\\cos 2\\theta = {num(c2).tex}$, what is ${fn}^2\\theta$?"
    sol = explain(
        f"${fn}^2\\theta$ from the value of $\\cos 2\\theta$.",
        f"the double angle formula has a version written only in terms of ${fn}$: $\\cos 2\\theta = {form}$.",
        [
            f"Set it equal to the given value: ${form} = {num(c2).tex}$.",
            (f"Solve: $2\\sin^2\\theta = 1 - ({num(c2).tex}) = {num(1 - c2).tex}$, so $\\sin^2\\theta = {num(ans).tex}$." if ask == "sin2"
             else f"Solve: $2\\cos^2\\theta = 1 + ({num(c2).tex}) = {num(1 + c2).tex}$, so $\\cos^2\\theta = {num(ans).tex}$."),
        ],
        f"${num(ans).tex}$.",
        "using the version of the formula with the other function, which gives $1$ minus the right answer.",
    )
    return (p, ans, [1 - ans, c2 / 2, ans + F(1, 4), abs(c2), (1 - c2)], ["$\\cos 2\\theta = 1 - 2\\sin^2\\theta = 2\\cos^2\\theta - 1$."], sol)


@family("x2_log_product", 2, "logarithms", "log_rules", T)
def _(r):
    b = r.choice([2, 3, 5])
    k = r.randint(4, 9)
    n = b ** k
    a = r.choice([d for d in range(2, n) if n % d == 0 and d != b])
    ans = k + 1
    p = f"What is $\\log_{{{b}}} {a} + \\log_{{{b}}} {n // a} + \\log_{{{b ** 2}}} {b ** 2}$?"
    sol = explain(
        "the value of three logarithms added together.",
        "logs with the same base add by multiplying their inputs: $\\log_b x + \\log_b y = \\log_b(xy)$. And $\\log_b b = 1$ for any base.",
        [
            f"Combine the first two: $\\log_{{{b}}}({a} \\cdot {n // a}) = \\log_{{{b}}} {n}$.",
            f"${n} = {b}^{{{k}}}$, so $\\log_{{{b}}} {n} = {k}$.",
            f"The last term asks what power of ${b ** 2}$ gives ${b ** 2}$: the answer is $1$.",
            f"Total: ${k} + 1 = {ans}$.",
        ],
        f"${ans}$.",
        f"adding the inputs (${a} + {n // a}$) instead of multiplying them.",
    )
    return (p, ans, [k, k + 2, a + n // a, 2 * k, k - 1], ["Combine logs with the same base."], sol)


@family("x2_cx_power", 2, "complex_numbers", "cx_arithmetic", T)
def _(r):
    a, b = r.choice([(1, 1), (1, -1), (2, 1), (1, 2), (2, -1), (3, 1)])
    n = r.choice([2, 3, 4])
    z = complex(a, b)
    pw = [z]
    for _ in range(n - 1):
        pw.append(pw[-1] * z)
    vals = [(round(w.real), round(w.imag)) for w in pw]
    re_, im_ = vals[-1]
    ask = r.choice(["re", "im"])
    ans = re_ if ask == "re" else im_
    ct = lambda x, y: f"{x}{' + ' if y >= 0 else ' - '}{abs(y) if abs(y) != 1 else ''}i"
    zt = ct(a, b)
    steps = [f"Square: $({zt})^2 = {a * a} {'+' if 2 * a * b >= 0 else '-'} {abs(2 * a * b)}i + ({b})^2 i^2 = {a * a} {'+' if 2 * a * b >= 0 else '-'} {abs(2 * a * b)}i - {b * b} = {ct(*vals[1])}$."]
    for i in range(2, n):
        steps.append(f"Multiply by ${zt}$ again: $({ct(*vals[i - 1])})({zt}) = {ct(*vals[i])}$.")
    p = f"What is the {'real' if ask == 're' else 'imaginary'} part of $({zt})^{{{n}}}$?"
    sol = explain(f"the {'real' if ask == 're' else 'imaginary'} part of $({zt})^{{{n}}}$.", "multiply out step by step, replacing $i^2$ with $-1$ each time.", steps + [f"So $({zt})^{{{n}}} = {ct(re_, im_)}$."],
                  f"the {'real' if ask == 're' else 'imaginary'} part is ${ans}$.", f"forgetting that $i^2 = -1$ flips the sign of the $({b})^2$ term." if n == 2 else "dropping the $i^2 = -1$ sign change in one of the steps.")
    return (p, ans, [im_ if ask == "re" else re_, a ** n, -ans if ans else 1, ans + 2, b ** n], ["Expand step by step, using $i^2 = -1$."], sol)


@family("x2_poly_remainder", 2, "polynomials", "poly_remainder", T)
def _(r):
    co = [r.randint(1, 3)] + [r.randint(-6, 6) for _ in range(r.randint(3, 4))]
    a = r.choice([-2, -1, 1, 2, 3])
    val = 0
    for c in co:
        val = val * a + c
    v2 = 0
    for c in co:
        v2 = v2 * (-a) + c
    deg = len(co) - 1
    terms = " + ".join(f"{c} \\cdot ({a})^{{{deg - i}}}" if deg - i > 1 else (f"{c} \\cdot ({a})" if deg - i == 1 else str(c)) for i, c in enumerate(co) if c != 0)
    p = f"What is the remainder when ${polystr(co)}$ is divided by $x{' - ' if a > 0 else ' + '}{abs(a)}$?"
    sol = explain(
        "the remainder of a polynomial division, without doing long division.",
        f"Remainder Theorem: dividing $P(x)$ by $x - a$ leaves remainder $P(a)$. Here the divisor is $x - ({a})$, so plug in $x = {a}$.",
        [f"$P({a}) = {terms}$.", f"Evaluate: $P({a}) = {val}$."],
        f"the remainder is ${val}$.",
        f"plugging in $x = {-a}$ (the number you see in the divisor). Dividing by $x{' - ' if a > 0 else ' + '}{abs(a)}$ means plugging in the root, $x = {a}$. That mistake gives ${v2}$.",
    )
    return (p, val, [v2, val + 1, co[-1], sum(co) if sum(co) != val else val - 2, val - a], ["Remainder Theorem: plug in the root of the divisor."], sol)


@family("x2_ser_geometric", 2, "sequences_series", "ser_geometric", T)
def _(r):
    rr = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2), F(-1, 3), F(2, 5)])
    s = F(r.randint(2, 30))
    a = s * (1 - rr)
    ask = r.choice(["second", "first"])
    ans = a if ask == "first" else a * rr
    p = f"An infinite geometric series has common ratio ${num(rr).tex}$ and sum ${num(s).tex}$. What is its {ask} term?"
    steps = [f"The sum formula is $S = \\frac{{a}}{{1 - r}}$, so $a = S(1 - r)$.",
             f"$a = {num(s).tex}\\left(1 - {num(rr).tex}\\right) = {num(s).tex} \\cdot {num(1 - rr).tex} = {num(a).tex}$."]
    if ask == "second":
        steps.append(f"The second term is $ar = {num(a).tex} \\cdot {num(rr).tex} = {num(ans).tex}$.")
    sol = explain(f"the {ask} term of the series.", "an infinite geometric series with $|r| < 1$ adds to $S = \\frac{a}{1 - r}$, where $a$ is the first term.", steps, f"${num(ans).tex}$.",
                  "using $1 + r$ instead of $1 - r$, or multiplying $S$ by $r$.")
    return (p, ans, [s * rr, s / (1 - rr), ans + 1, a * rr * rr if ask == "second" else a * rr, s * (1 + rr)], ["$S = \\frac{a}{1 - r}$."], sol)


# ============================================================ LEVEL 3 (AMC 12 #6 to 10)


@family("x3_trig_cosines", 3, "trigonometry", "trig_laws", T)
def _(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    ang = r.choice([60, 120])
    cosv = "\\frac{1}{2}" if ang == 60 else "-\\frac{1}{2}"
    c2 = a * a + b * b - (a * b if ang == 60 else -a * b)
    ans = surd(1, c2)
    area = surd(F(a * b, 4), 3)
    ask = r.choice(["side", "area"])
    if ask == "side":
        p = f"Triangle $ABC$ has $AC = {a}$, $BC = {b}$, and $\\angle C = {ang}^\\circ$. What is $AB$?"
        sol = explain(
            "the side across from the known angle.",
            "Law of Cosines: $c^2 = a^2 + b^2 - 2ab\\cos C$, where $c$ is across from angle $C$.",
            [
                f"$\\cos {ang}^\\circ = {cosv}$.",
                f"$AB^2 = {a}^2 + {b}^2 - 2 \\cdot {a} \\cdot {b} \\cdot \\left({cosv}\\right) = {a * a} + {b * b} {'-' if ang == 60 else '+'} {a * b} = {c2}$.",
                f"$AB = \\sqrt{{{c2}}} = {ans.tex}$.",
            ],
            f"$AB = {ans.tex}$.",
            "getting the sign of $\\cos 120^\\circ$ wrong. It is negative, so the side gets longer." if ang == 120 else "using the Pythagorean Theorem; the angle is not $90^\\circ$.",
        )
        return (p, ans, [surd(1, a * a + b * b), surd(1, a * a + b * b + (a * b if ang == 60 else -a * b)), num(a + b), surd(1, c2 + 1), surd(1, max(c2 - 2, 2))], ["Use the Law of Cosines."], sol)
    p = f"Triangle $ABC$ has $AC = {a}$, $BC = {b}$, and $\\angle C = {ang}^\\circ$. What is its area?"
    sol = explain(
        "the area from two sides and the angle between them.",
        "Area $= \\frac{1}{2}ab\\sin C$, using the two sides that form angle $C$.",
        [f"$\\sin {ang}^\\circ = \\frac{{\\sqrt{{3}}}}{{2}}$ (for both $60^\\circ$ and $120^\\circ$).",
         f"Area $= \\frac{{1}}{{2}} \\cdot {a} \\cdot {b} \\cdot \\frac{{\\sqrt{{3}}}}{{2}} = {area.tex}$."],
        f"${area.tex}$.",
        "forgetting the $\\frac{1}{2}$, or using $\\cos$ instead of $\\sin$.",
    )
    return (p, area, [surd(F(a * b, 2), 3), num(F(a * b, 2)), surd(F(a * b, 4), 2), surd(F(a * b, 8), 3), num(F(a * b, 4))], ["Area $= \\frac{1}{2}ab\\sin C$."], sol)


@family("x3_log_equation", 3, "logarithms", "log_equations", T)
def _(r):
    b = r.choice([2, 3, 4, 6])
    x = r.randint(2, 12)
    a = r.randint(1, 8)
    prod = x * (x + a)
    e = math.log(prod, b)
    if abs(e - round(e)) > 1e-9:
        return None
    e = round(e)
    p = f"Solve $\\log_{{{b}}} x + \\log_{{{b}}}(x + {a}) = {e}$."
    sol = explain(
        "the value of $x$.",
        "combine the logs into one, rewrite as an exponential equation, and remember that a log's input must be positive.",
        [
            f"Combine: $\\log_{{{b}}}\\big(x(x + {a})\\big) = {e}$.",
            f"Rewrite without logs: $x(x + {a}) = {b}^{{{e}}} = {prod}$, so $x^2 + {a}x - {prod} = 0$.",
            f"Factor: $(x - {x})(x + {x + a}) = 0$, so $x = {x}$ or $x = {-x - a}$.",
            f"$x = {-x - a}$ is negative, and $\\log_{{{b}}}$ of a negative number is undefined. Only $x = {x}$ works.",
        ],
        f"$x = {x}$.",
        f"keeping the negative root ${-x - a}$.",
    )
    return (p, x, [-x - a, x + a, b ** e // 2, x + 1, b ** e - a], ["Combine the logs; remember the inputs must be positive."], sol)


@family("x3_cx_modulus_eq", 3, "complex_numbers", "cx_arithmetic", T)
def _(r):
    a, b = r.randint(2, 12), r.randint(1, 12)
    x = F(a * a - b * b, 2 * a)
    mod = a - x
    ask = r.choice(["mod2", "re"])
    ans = mod * mod if ask == "mod2" else x
    p = f"A complex number $z$ satisfies $z + |z| = {a} + {b}i$. What is {'$|z|^2$' if ask == 'mod2' else 'the real part of $z$'}?"
    sol = explain(
        f"{'$|z|^2$' if ask == 'mod2' else 'the real part of $z$'}.",
        "$|z|$ is a real number, so adding it to $z$ changes only the real part. Write $z = x + yi$ and match real and imaginary parts.",
        [
            f"Imaginary parts: $y = {b}$.",
            f"Real parts: $x + \\sqrt{{x^2 + {b * b}}} = {a}$.",
            f"Isolate the root and square: $\\sqrt{{x^2 + {b * b}}} = {a} - x$, so $x^2 + {b * b} = {a * a} - {2 * a}x + x^2$.",
            f"The $x^2$ terms cancel: ${2 * a}x = {a * a - b * b}$, so $x = {num(x).tex}$.",
        ] + ([f"Then $|z| = {a} - x = {num(mod).tex}$ and $|z|^2 = {num(ans).tex}$."] if ask == "mod2" else []),
        f"${num(ans).tex}$.",
        f"assuming $|z| = \\sqrt{{{a}^2 + {b}^2}}$. That is the size of $z + |z|$, not of $z$.",
    )
    return (p, ans, [a * a + b * b, F(a * a + b * b, 2), ans + 1, -ans if ans else 2, b * b], ["$|z|$ is real, so the imaginary part of $z$ is $" + str(b) + "$. Write $z = x + " + str(b) + "i$."], sol)


@family("x3_poly_coeffs", 3, "polynomials", "poly_remainder", T)
def _(r):
    a, b = r.randint(1, 4), r.randint(-4, 4)
    n = r.randint(3, 9)
    if b == 0:
        return None
    ask = r.choice(["sum", "alt", "even"])
    s1, sm1 = (a + b) ** n, (-a + b) ** n
    if ask == "sum":
        ans, words = s1, "the sum of all the coefficients"
        steps = [f"Plug in $x = 1$: every power of $x$ becomes $1$, leaving the sum of the coefficients.", f"$P(1) = ({a} + ({b}))^{{{n}}} = {a + b}^{{{n}}} = {s1}$."]
    elif ask == "alt":
        ans, words = sm1, "the sum of the coefficients of the even powers of $x$ minus the sum for the odd powers"
        steps = ["Plug in $x = -1$: even powers become $+1$ and odd powers become $-1$.", f"$P(-1) = ({-a} + ({b}))^{{{n}}} = {b - a}^{{{n}}} = {sm1}$."]
    else:
        ans, words = F(s1 + sm1, 2), "the sum of the coefficients of the even powers of $x$ (including the constant term)"
        steps = [f"$P(1) = {a + b}^{{{n}}} = {s1}$ adds all coefficients.", f"$P(-1) = {b - a}^{{{n}}} = {sm1}$ adds even ones and subtracts odd ones.",
                 f"Adding these doubles the even coefficients and cancels the odd ones: $\\frac{{{s1} + ({sm1})}}{{2}} = {num(F(ans)).tex}$."]
    poly = f"({a if a > 1 else ''}x{' + ' if b > 0 else ' - '}{abs(b)})^{{{n}}}"
    p = f"When ${poly}$ is expanded, what is {words}?"
    sol = explain(words + ".", "plugging $x = 1$ or $x = -1$ into a polynomial adds up its coefficients (with signs for $-1$), with no expanding needed.", steps, f"${num(F(ans)).tex}$.",
                  "expanding term by term, which is slow and error prone.")
    return (p, ans, [s1 if ask != "sum" else sm1, F(s1 - sm1, 2), a ** n + b ** n, ans + 1, 2 ** n], ["Plug in $x = 1$ and $x = -1$."], sol)


@family("x3_con_circle_centers", 3, "conics", "con_parabolas", T)
def _(r):
    h1, k1, h2, k2 = [r.randint(-7, 7) for _ in range(4)]
    dx, dy = h2 - h1, k2 - k1
    d2 = dx * dx + dy * dy
    if d2 < 25 or math.isqrt(d2) ** 2 != d2:
        return None
    r1, r2 = r.randint(1, 9), r.randint(1, 9)
    d = math.isqrt(d2)

    def eq(h, k, rad):
        D, E, Fc = -2 * h, -2 * k, h * h + k * k - rad * rad
        return f"x^2 + y^2{' + ' if D >= 0 else ' - '}{abs(D)}x{' + ' if E >= 0 else ' - '}{abs(E)}y{' + ' if Fc >= 0 else ' - '}{abs(Fc)} = 0", D, E
    e1, D1, E1 = eq(h1, k1, r1)
    e2, D2, E2 = eq(h2, k2, r2)
    p = f"What is the distance between the centers of the circles ${e1}$ and ${e2}$?"
    sol = explain(
        "the two centers, then the distance between them.",
        "completing the square turns $x^2 + y^2 + Dx + Ey + F = 0$ into $(x - h)^2 + (y - k)^2 = r^2$ with center $(h, k) = \\left(-\\frac{D}{2}, -\\frac{E}{2}\\right)$.",
        [
            f"First circle: $D = {D1}$, $E = {E1}$, so the center is $({h1}, {k1})$.",
            f"Second circle: $D = {D2}$, $E = {E2}$, so the center is $({h2}, {k2})$.",
            f"Distance: $\\sqrt{{({h2} - ({h1}))^2 + ({k2} - ({k1}))^2}} = \\sqrt{{{dx * dx} + {dy * dy}}} = {d}$.",
        ],
        f"${d}$.",
        "taking the center as $(D, E)$ or $\\left(\\frac{D}{2}, \\frac{E}{2}\\right)$. The signs flip and the numbers halve.",
    )
    return (p, d, [r1 + r2, abs(dx) + abs(dy), d + 1, abs(r1 - r2) if abs(r1 - r2) != d else d + 2, d2], ["Complete the square to find each center."], sol)


# ============================================================ LEVEL 4 (AMC 12 #11 to 15)


@family("x4_trig_count", 4, "trigonometry", "trig_equations", T)
def _(r):
    n = r.randint(2, 7)
    fn = r.choice(["sin", "cos"])
    A, B = set(), set()
    for k in range(-3 * n, 3 * n + 1):
        c1 = F(2 * k, n - 1)
        c2 = F(2 * k + 1, n + 1) if fn == "sin" else F(2 * k, n + 1)
        if 0 <= c1 < 2:
            A.add(c1)
        if 0 <= c2 < 2:
            B.add(c2)
    sols = A | B
    ans = len(sols)
    for s in sols:
        x = float(s) * math.pi
        f = math.sin if fn == "sin" else math.cos
        assert abs(f(n * x) - f(x)) < 1e-9
    both = A & B
    pis = lambda S: ", ".join(f"${pi_mult(v).tex}$" for v in sorted(S))
    p = f"How many values of $x$ with $0 \\le x < 2\\pi$ satisfy $\\{fn}({n}x) = \\{fn} x$?"
    if fn == "sin":
        cases = [f"Case 1, ${n}x = x + 2\\pi k$: ${n - 1}x = 2\\pi k$, so $x = \\frac{{2\\pi k}}{{{n - 1}}}$. In range: {pis(A)} (${len(A)}$ values).",
                 f"Case 2, ${n}x = \\pi - x + 2\\pi k$: ${n + 1}x = \\pi + 2\\pi k$, so $x = \\frac{{(2k + 1)\\pi}}{{{n + 1}}}$. In range: {pis(B)} (${len(B)}$ values)."]
        idea = "$\\sin A = \\sin B$ exactly when $A = B + 2\\pi k$ or $A = \\pi - B + 2\\pi k$ for some integer $k$."
    else:
        cases = [f"Case 1, ${n}x = x + 2\\pi k$: $x = \\frac{{2\\pi k}}{{{n - 1}}}$. In range: {pis(A)} (${len(A)}$ values).",
                 f"Case 2, ${n}x = -x + 2\\pi k$: $x = \\frac{{2\\pi k}}{{{n + 1}}}$. In range: {pis(B)} (${len(B)}$ values)."]
        idea = "$\\cos A = \\cos B$ exactly when $A = \\pm B + 2\\pi k$ for some integer $k$."
    sol = explain(
        f"the number of solutions of $\\{fn}({n}x) = \\{fn} x$ in one full turn.",
        idea,
        cases + [f"Values in both lists ({pis(both)}) count once. Total: ${len(A)} + {len(B)} - {len(both)} = {ans}$." if both else f"No value appears in both lists, so the total is ${len(A)} + {len(B)} = {ans}$."],
        f"${ans}$.",
        "forgetting the second case, or counting a shared value like $x = 0$ twice.",
    )
    return (p, ans, [2 * n, 2 * n + 2 if 2 * n + 2 != ans else 2 * n - 2, ans + 1, ans - 1, n + 1], ["Solve each case of the identity separately, then remove repeats."], sol)


@family("x4_log_ineq", 4, "logarithms", "log_change_base", T)
def _(r):
    b = r.choice([2, 3])
    r1, r2 = sorted(r.sample(range(1, 8), 2))
    if r2 - r1 < 2:
        return None
    s, pr = r1 + r2, r1 * r2
    cnt = b ** r2 - b ** r1 - 1
    L = f"\\log_{{{b}}} n"
    p = f"How many positive integers $n$ satisfy $({L})^2 - {s}{L} + {pr} < 0$?"
    sol = explain(
        "the integers $n$ that make this inequality true.",
        f"treat ${L}$ as a single unknown $t$. Then it is an ordinary quadratic inequality.",
        [
            f"Let $t = {L}$: $t^2 - {s}t + {pr} < 0$ factors as $(t - {r1})(t - {r2}) < 0$.",
            f"A product of two factors is negative when they have opposite signs, which happens for ${r1} < t < {r2}$.",
            f"Undo the log: ${b}^{{{r1}}} < n < {b}^{{{r2}}}$, that is ${b ** r1} < n < {b ** r2}$.",
            f"Integers strictly between: ${b ** r2} - {b ** r1} - 1 = {cnt}$.",
        ],
        f"${cnt}$.",
        "including the endpoints. The inequality is strict, so the endpoints give $0$, not a negative number.",
    )
    return (p, cnt, [cnt + 2, cnt + 1, r2 - r1 - 1, b ** r2 - b ** r1 if b ** r2 - b ** r1 != cnt + 1 else cnt + 3, b ** (r2 - r1)], ["Factor as a quadratic in $\\log_b n$."], sol)


@family("x4_cx_polygon", 4, "complex_numbers", "cx_roots_unity", T)
def _(r):
    n = r.choice([3, 4, 6, 8, 12])
    R = r.randint(1, 5)
    rr = R * R
    exact = {3: surd(F(3 * rr, 4), 3), 4: num(2 * rr), 6: surd(F(3 * rr, 2), 3), 8: surd(2 * rr, 2), 12: num(3 * rr)}
    sins = {3: "\\frac{\\sqrt{3}}{2}", 4: "1", 6: "\\frac{\\sqrt{3}}{2}", 8: "\\frac{\\sqrt{2}}{2}", 12: "\\frac{1}{2}"}
    ans = exact[n]
    assert abs(ans.key - n / 2 * rr * math.sin(2 * math.pi / n)) < 1e-9
    p = f"The solutions of $z^{{{n}}} = {R ** n}$ are the vertices of a polygon in the complex plane. What is its area?"
    sol = explain(
        "the area of the polygon whose corners are all solutions of the equation.",
        f"the solutions of $z^n = R^n$ all have $|z| = R$ and are spaced evenly around the circle of radius $R$. So they form a regular $n$-gon.",
        [
            f"${R ** n} = {R}^{{{n}}}$, so every solution has $|z| = {R}$. There are ${n}$ solutions, $\\frac{{360^\\circ}}{{{n}}}$ apart.",
            f"Split the ${n}$-gon into ${n}$ triangles from the center. Each has two sides of length ${R}$ with angle $\\frac{{360^\\circ}}{{{n}}}$ between them.",
            f"One triangle's area: $\\frac{{1}}{{2}} \\cdot {R} \\cdot {R} \\cdot \\sin\\frac{{360^\\circ}}{{{n}}} = \\frac{{{rr}}}{{2}} \\cdot {sins[n]}$.",
            f"Multiply by ${n}$: area $= {ans.tex}$.",
        ],
        f"${ans.tex}$.",
        f"using ${R ** n}$ as the radius. The radius is the ${n}$th root, ${R}$.",
    )
    wrong = [v for k, v in exact.items() if k != n][:3] + [num(n * rr), pi_mult(rr)]
    return (p, ans, wrong, [f"The solutions lie on a circle of radius ${R}$, equally spaced."], sol)


@family("x4_poly_int_roots", 4, "polynomials", "poly_vieta", T)
def _(r):
    roots = sorted(r.randint(1, 9) for _ in range(3))
    s = sum(roots)
    q = roots[0] * roots[1] + roots[1] * roots[2] + roots[0] * roots[2]
    pr = roots[0] * roots[1] * roots[2]
    others = {(a, b, c) for a in range(1, 30) for b in range(a, 30) for c in range(b, 30) if a + b + c == s and a * b * c == pr}
    if len(others) != 1:
        return None
    x, y, z = roots
    p = f"The polynomial $x^3 - {s}x^2 + bx - {pr}$ has three positive integer roots. What is $b$?"
    sol = explain(
        "the middle coefficient $b$.",
        "Vieta's formulas for $x^3 - px^2 + qx - r$: the roots add to $p$, their pairwise products add to $q$, and they multiply to $r$.",
        [
            f"The roots $r_1, r_2, r_3$ satisfy $r_1 + r_2 + r_3 = {s}$ and $r_1 r_2 r_3 = {pr}$.",
            f"List ways to write ${pr}$ as a product of three positive integers and check which one adds to ${s}$: only ${x}, {y}, {z}$ works.",
            f"Then $b = r_1r_2 + r_2r_3 + r_1r_3 = {x * y} + {y * z} + {x * z} = {q}$.",
        ],
        f"$b = {q}$.",
        "mixing up which coefficient goes with which Vieta sum. The $x$ coefficient matches the sum of products of pairs.",
    )
    return (p, q, [q + 1, s * s // 3, pr // s if pr // s != q else q - 2, q - 1, sum(t * t for t in roots)], ["The roots add to " + str(s) + " and multiply to " + str(pr) + "."], sol)


@family("x4_ser_rationalize", 4, "sequences_series", "ser_telescoping", T)
def _(r):
    m = r.randint(4, 30)
    N = m * m - 1
    ans = m - 1
    p = f"What is $\\displaystyle\\sum_{{n=1}}^{{{N}}} \\frac{{1}}{{\\sqrt{{n}} + \\sqrt{{n + 1}}}}$?"
    sol = explain(
        f"the sum of ${N}$ fractions with square roots in the denominators.",
        "rationalize each denominator: multiply top and bottom by the conjugate. The terms then telescope.",
        [
            "$\\frac{1}{\\sqrt{n} + \\sqrt{n + 1}} \\cdot \\frac{\\sqrt{n + 1} - \\sqrt{n}}{\\sqrt{n + 1} - \\sqrt{n}} = \\frac{\\sqrt{n + 1} - \\sqrt{n}}{(n + 1) - n} = \\sqrt{n + 1} - \\sqrt{n}$.",
            f"The sum becomes $(\\sqrt{{2}} - \\sqrt{{1}}) + (\\sqrt{{3}} - \\sqrt{{2}}) + \\cdots + (\\sqrt{{{N + 1}}} - \\sqrt{{{N}}})$.",
            f"Everything cancels except the last and first: $\\sqrt{{{N + 1}}} - 1 = {m} - 1 = {ans}$.",
        ],
        f"${ans}$.",
        f"forgetting the $-1$ from the first term and answering ${m}$.",
    )
    return (p, ans, [m, m + 1, ans * 2, F(m, 2), N // m], ["Rationalize each denominator."], sol)


# ============================================================ LEVEL 5 (AMC 12 #16 to 20)


@family("x5_trig_power_sum", 5, "trigonometry", "trig_identities", T)
def _(r):
    k = F(r.randint(5, 20), r.choice([2, 3]))
    if k < 2:
        return None
    sc = 1 / k
    ask = r.choice([4, 6])
    ans = 1 - 2 * sc * sc if ask == 4 else 1 - 3 * sc * sc
    p = f"If $\\tan x + \\cot x = {num(k).tex}$, what is $\\sin^{{{ask}}} x + \\cos^{{{ask}}} x$?"
    if ask == 4:
        id_step = "$\\sin^4 x + \\cos^4 x = (\\sin^2 x + \\cos^2 x)^2 - 2\\sin^2 x\\cos^2 x = 1 - 2(\\sin x\\cos x)^2$."
    else:
        id_step = "$\\sin^6 x + \\cos^6 x = (\\sin^2 x + \\cos^2 x)^3 - 3\\sin^2 x\\cos^2 x(\\sin^2 x + \\cos^2 x) = 1 - 3(\\sin x\\cos x)^2$."
    sol = explain(
        f"$\\sin^{{{ask}}} x + \\cos^{{{ask}}} x$, without finding $x$.",
        "both the given and the target can be written using only $\\sin x \\cos x$.",
        [
            "Combine the given: $\\tan x + \\cot x = \\frac{\\sin x}{\\cos x} + \\frac{\\cos x}{\\sin x} = \\frac{\\sin^2 x + \\cos^2 x}{\\sin x \\cos x} = \\frac{1}{\\sin x\\cos x}$.",
            f"So $\\sin x \\cos x = \\frac{{1}}{{{num(k).tex}}} = {num(sc).tex}$.",
            id_step,
            f"Plug in: $1 - {2 if ask == 4 else 3} \\cdot \\left({num(sc).tex}\\right)^2 = 1 - {num((2 if ask == 4 else 3) * sc * sc).tex} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"using the wrong multiplier: it is $2$ for fourth powers and $3$ for sixth powers.",
    )
    return (p, ans, [1 - sc * sc, 1 - (3 if ask == 4 else 2) * sc * sc, sc, 1 - 4 * sc * sc, ans + sc * sc], ["$\\tan x + \\cot x = \\frac{1}{\\sin x \\cos x}$."], sol)


@family("x5_log_system", 5, "logarithms", "log_equations", T)
def _(r):
    b = r.choice([2, 3])
    t, u = r.sample(range(1, 7), 2)
    m = t + u
    k = F(t, u) + F(u, t)
    x, y = b ** t, b ** u
    ans = x + y
    p = f"Positive real numbers $x$ and $y$ satisfy $\\log_x y + \\log_y x = {num(k).tex}$ and $xy = {b}^{{{m}}}$. What is $x + y$?"
    sol = explain(
        "$x + y$, which means finding $x$ and $y$.",
        f"switch to base ${b}$ logs. Let $t = \\log_{{{b}}} x$ and $u = \\log_{{{b}}} y$; then both equations become simple equations in $t$ and $u$.",
        [
            f"$xy = {b}^{{{m}}}$ gives $t + u = {m}$.",
            "Change of base: $\\log_x y = \\frac{u}{t}$ and $\\log_y x = \\frac{t}{u}$. So $\\frac{u}{t} + \\frac{t}{u} = " + num(k).tex + "$, which means $t^2 + u^2 = " + num(k).tex + "\\,tu$.",
            f"Since $t^2 + u^2 = (t + u)^2 - 2tu = {m * m} - 2tu$, we get ${m * m} = ({num(k).tex} + 2)tu$, so $tu = {t * u}$.",
            f"$t$ and $u$ add to ${m}$ and multiply to ${t * u}$: they are ${t}$ and ${u}$.",
            f"So $x$ and $y$ are ${b}^{{{t}}} = {x}$ and ${b}^{{{u}}} = {y}$, and $x + y = {ans}$.",
        ],
        f"${ans}$.",
        "assuming $x = y$. The first equation would then give $2$, not $" + num(k).tex + "$.",
    )
    return (p, ans, [b ** m, 2 * b ** (m // 2) if m % 2 == 0 else b ** m // 2, ans + b, x * 2, abs(x - y)], [f"Let $t = \\log_{{{b}}} x$ and $u = \\log_{{{b}}} y$."], sol)


@family("x5_cx_chord_sum", 5, "complex_numbers", "cx_roots_unity", T)
def _(r):
    n = r.randint(5, 30)
    kind = r.choice(["sq", "recip"])
    w = [cmath.exp(2j * math.pi * k / n) for k in range(1, n)]
    om = f"\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}"
    if kind == "sq":
        ans = 2 * n
        assert abs(sum(abs(1 - x) ** 2 for x in w) - ans) < 1e-6
        p = f"Let ${om}$. What is $\\displaystyle\\sum_{{k=1}}^{{{n - 1}}} |1 - \\omega^k|^2$?"
        sol = explain(
            "the sum of the squared distances from $1$ to the other roots of unity.",
            "for any complex $z$, $|z|^2 = z\\bar{z}$. And on the unit circle, $\\overline{\\omega^k} = \\omega^{-k}$.",
            [
                "Expand one term: $|1 - \\omega^k|^2 = (1 - \\omega^k)(1 - \\omega^{-k}) = 2 - \\omega^k - \\omega^{-k}$.",
                f"Sum over $k = 1$ to ${n - 1}$: the $2$s give $2 \\cdot {n - 1} = {2 * (n - 1)}$.",
                f"All ${n}$ roots of $z^{{{n}}} = 1$ add to $0$, so $\\omega + \\omega^2 + \\cdots + \\omega^{{{n - 1}}} = -1$. The same holds for the $\\omega^{{-k}}$ terms.",
                f"Total: ${2 * (n - 1)} - (-1) - (-1) = {ans}$.",
            ],
            f"${ans}$.",
            f"forgetting that the powers of $\\omega$ add to $-1$, not $0$, once $k = 0$ is left out.",
        )
        wrong = [2 * (n - 1), n, n * n, 4 * n, n - 1]
    else:
        ans = F(n - 1, 2)
        assert abs(sum(1 / (1 - x) for x in w) - float(ans)) < 1e-6
        p = f"Let ${om}$. What is $\\displaystyle\\sum_{{k=1}}^{{{n - 1}}} \\frac{{1}}{{1 - \\omega^k}}$?"
        sol = explain(
            "a sum of complex fractions that turns out to be real.",
            "pair each term with its partner $k \\leftrightarrow n - k$, since $\\omega^{n - k} = \\omega^{-k}$.",
            [
                "Pair: $\\frac{1}{1 - \\omega^k} + \\frac{1}{1 - \\omega^{-k}}$. Multiply the second by $\\frac{\\omega^k}{\\omega^k}$: it becomes $\\frac{\\omega^k}{\\omega^k - 1} = -\\frac{\\omega^k}{1 - \\omega^k}$.",
                "So the pair adds to $\\frac{1 - \\omega^k}{1 - \\omega^k} = 1$.",
                f"Adding all ${n - 1}$ terms counts each pair twice when we sum over all $k$: $2S = {n - 1}$, so $S = {num(ans).tex}$.",
            ],
            f"${num(ans).tex}$.",
            f"counting each pair once and getting ${n - 1}$.",
        )
        wrong = [n - 1, F(n, 2), 0, F(n + 1, 2), 1]
    return (p, ans, wrong, ["$\\omega^{-k} = \\overline{\\omega^k}$; pairing or Vieta helps."], sol)


@family("x5_poly_interp", 5, "polynomials", "poly_roots", T)
def _(r):
    n = r.randint(2, 5)
    pts = list(range(1, n + 2))

    def P(x):
        tot = F(0)
        for i in pts:
            term = F(1, i)
            for j in pts:
                if j != i:
                    term *= F(x - j, i - j)
            tot += term
        return tot
    ask = r.choice([0, n + 2])
    ans = P(ask)
    fact = math.factorial(n + 1)
    c = F((-1) ** (n + 2), fact)
    p = f"A polynomial $P$ of degree ${n}$ satisfies $P(k) = \\dfrac{{1}}{{k}}$ for $k = 1, 2, \\ldots, {n + 1}$. What is $P({ask})$?"
    prod_ = " ".join(f"(x - {k})" for k in pts)
    steps = [
        f"Let $Q(x) = xP(x) - 1$. It has degree ${n + 1}$, and $Q(k) = k \\cdot \\frac{{1}}{{k}} - 1 = 0$ for $k = 1, \\ldots, {n + 1}$. So $$ Q(x) = c{prod_}. $$",
        f"Find $c$ by plugging in $x = 0$: $Q(0) = 0 \\cdot P(0) - 1 = -1$, and the product at $0$ is $(-1)^{{{n + 1}}} \\cdot {n + 1}! = {(-1) ** (n + 1) * fact}$. So $c = \\frac{{-1}}{{{(-1) ** (n + 1) * fact}}} = {num(c).tex}$.",
    ]
    if ask == 0:
        steps.append(f"$P(0)$ cannot come from $Q(0)$ directly (it is multiplied by $0$). Instead, $P(0)$ is the $x$ coefficient of $Q$. Expanding, that coefficient is $c \\cdot (-1)^{{{n}}} \\cdot {n + 1}!\\left(1 + \\frac{{1}}{{2}} + \\cdots + \\frac{{1}}{{{n + 1}}}\\right)$, which works out to $1 + \\frac{{1}}{{2}} + \\cdots + \\frac{{1}}{{{n + 1}}} = {num(ans).tex}$.")
    else:
        val = c * math.prod(ask - k for k in pts)
        steps.append(f"At $x = {ask}$: $Q({ask}) = {num(c).tex} \\cdot {math.prod(ask - k for k in pts)} = {num(val).tex}$.")
        steps.append(f"So ${ask}P({ask}) - 1 = {num(val).tex}$, giving $P({ask}) = \\frac{{1 + ({num(val).tex})}}{{{ask}}} = {num(ans).tex}$.")
    sol = explain(f"$P({ask})$, where $P$ matches $\\frac{{1}}{{k}}$ at ${n + 1}$ points.", "build a helper polynomial that is zero at all the known points, so it factors completely.", steps, f"${num(ans).tex}$.",
                  f"assuming $P({ask}) = \\frac{{1}}{{{ask}}}$. The polynomial only matches $\\frac{{1}}{{x}}$ at the given points." if ask else "trying to find every coefficient of $P$, which is slow. The helper polynomial is the shortcut.")
    return (p, ans, [F(1, n + 2) if ask else F(n + 1), -ans if ans else 1, ans + 1, F(1, n + 1), ans * 2], ["Look at $Q(x) = xP(x) - 1$: it has degree " + str(n + 1) + " and known roots."], sol)


@family("x5_con_tangent_line", 5, "conics", "con_ellipses", T)
def _(r):
    a, b = r.randint(2, 6), r.randint(1, 5)
    if a == b:
        return None
    m = r.choice([1, 2, -1, 3, F(1, 2)])
    m = F(m)
    c2 = F(a * a) * m * m + b * b
    ans = surd(1, int(c2)) if c2.denominator == 1 else surd(F(1, c2.denominator), c2.numerator * c2.denominator)
    mt = num(m).tex if m not in (1, -1) else ("" if m == 1 else "-")
    A_ = F(1, a * a) + m * m / (b * b)
    p = f"The line $y = {mt}x + c$ with $c > 0$ is tangent to the ellipse $\\dfrac{{x^2}}{{{a * a}}} + \\dfrac{{y^2}}{{{b * b}}} = 1$. What is $c$?"
    sol = explain(
        "the intercept $c$ that makes the line touch the ellipse at exactly one point.",
        "substitute the line into the ellipse. A tangent line meets the ellipse once, so the resulting quadratic in $x$ has discriminant $0$.",
        [
            f"Substitute $y = {mt}x + c$: $\\frac{{x^2}}{{{a * a}}} + \\frac{{({mt}x + c)^2}}{{{b * b}}} = 1$.",
            f"Multiply by ${a * a * b * b}$ and collect: $({b * b} + {num(a * a * m * m).tex})x^2 + {num(2 * a * a * m).tex}c\\,x + {a * a}(c^2 - {b * b}) = 0$.",
            f"Set the discriminant to $0$. After simplifying, it reduces to $c^2 = a^2m^2 + b^2 = {a * a} \\cdot {num(m * m).tex} + {b * b} = {num(c2).tex}$.",
            f"$c = {ans.tex}$ (taking the positive root).",
        ],
        f"$c = {ans.tex}$.",
        "using $c^2 = a^2 + b^2$, which forgets the slope.",
    )
    return (p, ans, [surd(1, a * a + b * b) if c2 != a * a + b * b else num(a + b), num(a + b), num(max(a, b)), surd(1, abs(a * a - b * b)), num(2 * max(a, b))],
            ["Substitute the line into the ellipse; tangent means the resulting quadratic has discriminant $0$."], sol)


# ============================================================ LEVEL 6 (AMC 12 #21 to 25)


@family("x6_trig_tan_squares", 6, "trigonometry", "trig_identities", T)
def _(r):
    n = r.randint(3, 7)
    m = 2 * n + 1
    ans = n * m
    assert abs(sum(math.tan(k * math.pi / m) ** 2 for k in range(1, n + 1)) - ans) < 1e-6
    p = f"What is $\\tan^2\\frac{{\\pi}}{{{m}}} + \\tan^2\\frac{{2\\pi}}{{{m}}} + \\cdots + \\tan^2\\frac{{{n}\\pi}}{{{m}}}$?"
    sol = explain(
        f"the sum of ${n}$ squared tangents.",
        f"the numbers $\\tan^2\\frac{{k\\pi}}{{{m}}}$ for $k = 1, \\ldots, {n}$ are exactly the roots of one polynomial. Vieta then gives their sum.",
        [
            f"Let $\\theta = \\frac{{k\\pi}}{{{m}}}$. Then $\\tan({m}\\theta) = 0$.",
            f"De Moivre writes $\\tan({m}\\theta)$ as a fraction in $t = \\tan\\theta$; its top is $\\binom{{{m}}}{{1}}t - \\binom{{{m}}}{{3}}t^3 + \\binom{{{m}}}{{5}}t^5 - \\cdots$, which must be $0$.",
            f"Divide by $t$ and set $u = t^2$: the result is a degree ${n}$ polynomial in $u$ whose roots are $\\tan^2\\frac{{k\\pi}}{{{m}}}$ for $k = 1, \\ldots, {n}$.",
            f"Its top two coefficients (up to sign) are $\\binom{{{m}}}{{{m}}} = 1$ and $\\binom{{{m}}}{{{m - 2}}} = {comb_(m, 2)}$, so the roots add to ${comb_(m, 2)}$.",
        ],
        f"${ans}$.",
        "trying to approximate each tangent. The values are irrational, but their sum is a whole number.",
    )
    return (p, ans, [n * n, m * m, ans + n, n * (m - 1), ans - n], [f"The numbers $\\tan^2\\frac{{k\\pi}}{{{m}}}$ for $k = 1, \\ldots, {n}$ are the roots of one polynomial; use Vieta."], sol)


def comb_(a, b):
    return math.comb(a, b)


@family("x6_log_integer_pairs", 6, "logarithms", "log_rules", T)
def _(r):
    N = r.choice([50, 64, 81, 100, 125, 150, 200, 243, 256, 300])
    cnt = 0
    rows = []
    for x in range(2, N + 1):
        k, p_ = 0, x
        while p_ <= N:
            k += 1
            p_ *= x
        cnt += k
        if k > 1:
            rows.append((x, k))
    big = sum(k for _, k in rows)
    singles = (N - 1) - len(rows)
    p = f"How many ordered pairs of integers $(x, y)$ with $2 \\le x \\le {N}$ and $1 \\le y \\le {N}$ make $\\log_x y$ a positive integer?"
    sol = explain(
        "pairs where $y$ is a positive integer power of $x$.",
        "$\\log_x y = k$ means $y = x^k$. For each $x$, count the powers $x^1, x^2, \\ldots$ that stay at most " + str(N) + ".",
        [
            f"Bases with more than one power up to ${N}$: " + ", ".join(f"$x = {x}$ (${k}$ powers)" for x, k in rows) + f". These give ${big}$ pairs.",
            f"Every other base from $2$ to ${N}$ has only $x^1 = x$: that is ${singles}$ more bases, ${singles}$ pairs.",
            f"Total: ${big} + {singles} = {cnt}$.",
        ],
        f"${cnt}$.",
        "forgetting $k = 1$ (where $y = x$), or allowing $y = 1$, which gives $\\log_x 1 = 0$, not positive.",
    )
    return (p, cnt, [cnt + 1, cnt - 1, N - 1, cnt + math.isqrt(N), cnt + 10], ["$\\log_x y = k$ means $y = x^k$. Count, for each $x$, the powers of $x$ up to " + str(N) + "."], sol)


@family("x6_cx_product", 6, "complex_numbers", "cx_roots_unity", T)
def _(r):
    n = r.randint(3, 8)
    a = r.randint(2, 4)
    w = [cmath.exp(2j * math.pi * k / n) for k in range(1, n)]
    prod = 1
    for x in w:
        prod *= (a - x) * (a - x.conjugate())
    single = F(a ** n - 1, a - 1)
    ans = single ** 2
    assert abs(prod.real - float(ans)) < 1e-3 * float(ans)
    p = f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. What is $\\displaystyle\\prod_{{k=1}}^{{{n - 1}}} \\left|{a} - \\omega^k\\right|^2$?"
    sol = explain(
        f"a product over all roots of unity except $1$.",
        "$z^n - 1 = (z - 1)(z - \\omega)(z - \\omega^2)\\cdots(z - \\omega^{n-1})$. Dividing out $(z - 1)$ leaves $1 + z + z^2 + \\cdots + z^{n-1}$.",
        [
            f"So $\\prod_{{k=1}}^{{{n - 1}}}(z - \\omega^k) = 1 + z + \\cdots + z^{{{n - 1}}}$. Plug in $z = {a}$: $$ \\prod({a} - \\omega^k) = 1 + {a} + \\cdots + {a}^{{{n - 1}}} = \\frac{{{a}^{{{n}}} - 1}}{{{a} - 1}} = {single}. $$",
            f"$|{a} - \\omega^k|^2 = ({a} - \\omega^k)\\overline{{({a} - \\omega^k)}}$. The conjugates $\\overline{{\\omega^k}} = \\omega^{{-k}}$ run over the same roots in another order, so the conjugate product is also ${single}$.",
            f"Multiply: ${single} \\cdot {single} = {ans}$.",
        ],
        f"${ans}$.",
        f"forgetting the square and answering ${single}$.",
    )
    return (p, ans, [single, (a ** n - 1) ** 2, ans + 1, a ** (2 * n), single * a], ["$\\prod_{k=1}^{n-1}(x - \\omega^k) = 1 + x + \\cdots + x^{n-1}$."], sol)


@family("x6_poly_quartic", 6, "polynomials", "poly_remainder", T)
def _(r):
    vals = [r.randint(-10, 10) for _ in range(4)]

    def Q(x):
        tot = F(0)
        for i in range(4):
            term = F(vals[i])
            for j in range(4):
                if j != i:
                    term *= F(x - (j + 1), i - j)
            tot += term
        return tot
    P = lambda x: F((x - 1) * (x - 2) * (x - 3) * (x - 4)) + Q(x)
    ans = P(0) + P(5)
    q0, q5 = Q(0), Q(5)
    p = f"A polynomial $P(x) = x^4 + ax^3 + bx^2 + cx + d$ has $P(1) = {vals[0]}$, $P(2) = {vals[1]}$, $P(3) = {vals[2]}$, and $P(4) = {vals[3]}$. What is $P(0) + P(5)$?"
    sol = explain(
        "$P(0) + P(5)$ without finding all four unknown coefficients.",
        "split $P$ into a piece that is zero at $1, 2, 3, 4$ plus a cubic $Q$ that carries the given values.",
        [
            "Write $P(x) = (x - 1)(x - 2)(x - 3)(x - 4) + Q(x)$, where $Q$ has degree at most $3$. (The first part supplies the $x^4$.)",
            f"Then $Q(1) = {vals[0]}$, $Q(2) = {vals[1]}$, $Q(3) = {vals[2]}$, $Q(4) = {vals[3]}$.",
            "The quartic part at $0$: $(-1)(-2)(-3)(-4) = 24$. At $5$: $4 \\cdot 3 \\cdot 2 \\cdot 1 = 24$.",
            f"A cubic is determined by four values. Using finite differences on $Q(1), \\ldots, Q(4)$ (the third differences are constant) and extending one step each way gives $Q(0) = {num(q0).tex}$ and $Q(5) = {num(q5).tex}$.",
            f"$P(0) + P(5) = 24 + ({num(q0).tex}) + 24 + ({num(q5).tex}) = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "forgetting the quartic part (the two $24$s), which every monic quartic contributes.",
    )
    return (p, ans, [ans - 48, P(0), P(5), ans + 24, sum(vals)], ["Write $P(x) = (x - 1)(x - 2)(x - 3)(x - 4) + Q(x)$ where $Q$ is a cubic."], sol)


@family("x6_ser_power_sums", 6, "sequences_series", "ser_geometric", T)
def _(r):
    a = r.randint(2, 7)
    kind = r.choice(["n2", "n", "prod"])
    if kind == "n2":
        ans = F(a * (a + 1), (a - 1) ** 3)
        assert abs(sum(n * n / a ** n for n in range(1, 400)) - float(ans)) < 1e-9
        x = F(1, a)
        p = f"What is $\\displaystyle\\sum_{{n=1}}^{{\\infty}} \\frac{{n^2}}{{{a}^n}}$?"
        steps = [
            "Start from $\\sum_{n \\ge 0} x^n = \\frac{1}{1 - x}$ for $|x| < 1$.",
            "Differentiate and multiply by $x$: $\\sum n x^n = \\frac{x}{(1 - x)^2}$.",
            "Do it again: $\\sum n^2 x^n = \\frac{x(1 + x)}{(1 - x)^3}$.",
            f"Plug in $x = \\frac{{1}}{{{a}}}$: $\\frac{{\\frac{{1}}{{{a}}} \\cdot \\frac{{{a + 1}}}{{{a}}}}}{{\\left(\\frac{{{a - 1}}}{{{a}}}\\right)^3}} = \\frac{{{a}({a + 1})}}{{({a - 1})^3}} = {num(ans).tex}$.",
        ]
        trap = "stopping after one derivative, which gives the sum of $\\frac{n}{" + str(a) + "^n}$."
        wrong = [F(a, (a - 1) ** 2), F(a * a, (a - 1) ** 3), ans + 1, F(a + 1, (a - 1) ** 2), ans * 2]
    elif kind == "n":
        k = r.randint(1, 3)
        A1, A2 = F(a, (a - 1) ** 2), F(k, a - 1)
        ans = A1 + A2
        p = f"What is $\\displaystyle\\sum_{{n=1}}^{{\\infty}} \\frac{{n + {k}}}{{{a}^n}}$?"
        steps = [
            f"Split: $\\sum \\frac{{n}}{{{a}^n}} + {k}\\sum \\frac{{1}}{{{a}^n}}$.",
            f"Geometric part: $\\sum_{{n \\ge 1}} \\frac{{1}}{{{a}^n}} = \\frac{{1/{a}}}{{1 - 1/{a}}} = \\frac{{1}}{{{a - 1}}}$, so ${k}$ times it is ${num(A2).tex}$.",
            f"For $S = \\sum \\frac{{n}}{{{a}^n}}$: $S - \\frac{{S}}{{{a}}} = \\sum \\frac{{1}}{{{a}^n}} = \\frac{{1}}{{{a - 1}}}$, so $S \\cdot \\frac{{{a - 1}}}{{{a}}} = \\frac{{1}}{{{a - 1}}}$ and $S = {num(A1).tex}$.",
            f"Total: ${num(A1).tex} + {num(A2).tex} = {num(ans).tex}$.",
        ]
        trap = "treating the whole thing as one geometric series. The $n$ in the numerator breaks the constant ratio."
        wrong = [A1, F(k * a, a - 1), ans + 1, F(a + k, (a - 1) ** 2), ans - F(1, a)]
    else:
        ans = F(1, 4)
        p = "What is $\\displaystyle\\sum_{n=1}^{\\infty} \\frac{1}{n(n + 1)(n + 2)}$?"
        steps = [
            "Partial fractions: $\\frac{1}{n(n + 1)(n + 2)} = \\frac{1}{2}\\left(\\frac{1}{n(n + 1)} - \\frac{1}{(n + 1)(n + 2)}\\right)$. (Check: the difference on the right has numerator $(n + 2) - n = 2$.)",
            "Write out the sum: $\\frac{1}{2}\\left[\\left(\\frac{1}{1 \\cdot 2} - \\frac{1}{2 \\cdot 3}\\right) + \\left(\\frac{1}{2 \\cdot 3} - \\frac{1}{3 \\cdot 4}\\right) + \\cdots\\right]$.",
            "Everything cancels except the first piece, $\\frac{1}{1 \\cdot 2} = \\frac{1}{2}$, and the tail goes to $0$.",
            "Total: $\\frac{1}{2} \\cdot \\frac{1}{2} = \\frac{1}{4}$.",
        ]
        trap = "forgetting the factor $\\frac{1}{2}$ from the partial fractions."
        wrong = [F(1, 2), F(1, 6), F(1, 3), F(1, 8), F(3, 4)]
    sol = explain("the value of an infinite sum.", "start from the geometric series or a telescoping split, depending on the form.", steps, f"${num(ans).tex}$.", trap)
    return (p, ans, wrong, ["Start from the geometric series and differentiate, or telescope."], sol)
