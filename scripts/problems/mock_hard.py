"""Level 7 mock families: the true end of the exam (AMC 10 #21 to 25, AMC 12 #21 to 25).

Each problem needs two or three ideas chained together, and every answer is checked
against an independent brute force or numeric computation before it is accepted.
"""
import cmath
import math
from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product
from math import comb, gcd

from common import NAMES, explain, num  # noqa: F401
from mock_common import family, surd


def _lcm(a, b):
    return a * b // gcd(a, b)


# ============================================================ SHARED (both tests)


@family("l7_alg_floor_values", 7, "algebra", "alg_functions")
def _(r):
    S = r.choice([(1, 2, 3), (2, 3, 4), (1, 2, 4), (2, 3), (1, 3, 4), (2, 4, 6), (3, 4)])
    M = r.randint(3, 10)
    # brute force: f only changes at points k/a, and increases at every one of them
    pts = {F(k, a) for a in S for k in range(a * M + 1)}
    ans = len(pts)
    vals = {sum(math.floor(a * x) for a in S) for x in pts}
    assert len(vals) == ans
    fx = " + ".join(f"\\lfloor {'' if a == 1 else a}x \\rfloor" for a in S)
    # inclusion and exclusion over subsets
    terms = []
    total = 0
    for size in range(1, len(S) + 1):
        for sub in combinations(S, size):
            g = reduce(gcd, sub)
            c = g * M + 1
            total += c if size % 2 else -c
            terms.append((sub, g, c, size))
    assert total == ans
    single = sum(a * M + 1 for a in S)
    p = f"How many different values does $f(x) = {fx}$ take as $x$ ranges over all real numbers with $0 \\le x \\le {M}$?"
    pieces = ", ".join(f"$\\tfrac{{k}}{{{a}}}$" for a in S)
    steps = [
        f"$f$ never decreases, and it jumps up exactly when one of the terms jumps, at a number of the form {pieces}. Between jumps it is constant. So the number of values is the number of jump points in $[0, {M}]$, counting $x = 0$.",
        "Multiples of $\\tfrac{1}{a}$ in $[0, " + str(M) + "]$: there are $" + str(M) + "a + 1$ of them. A number is a multiple of both $\\tfrac{1}{a}$ and $\\tfrac{1}{b}$ exactly when it is a multiple of $\\tfrac{1}{\\gcd(a, b)}$.",
        "Inclusion and exclusion: " + "; ".join(
            f"{'add' if sz % 2 else 'subtract'} ${c}$ for {'$a = ' + str(sub[0]) + '$' if sz == 1 else 'the overlap of ' + ', '.join(map(str, sub)) + ' (multiples of $\\tfrac{1}{' + str(g) + '}$)'}"
            for sub, g, c, sz in terms) + ".",
        f"Total: ${ans}$.",
    ]
    sol = explain(
        f"how many distinct outputs $f$ has on $[0, {M}]$.",
        "a step function that never decreases takes one new value at each jump, so count the jump points.",
        steps,
        f"${ans}$.",
        f"assuming every integer from $0$ to $f({M}) = {sum(S) * M}$ is reached. Several terms can jump at the same point, so many integers are skipped.",
    )
    wrong = [sum(S) * M + 1, single, ans - 1, ans + M, max(S) * M + 1]
    return (p, ans, wrong, ["$f$ only changes where some term jumps. Count those points, being careful when two terms jump at the same place."], sol)


@family("l7_alg_hex_norm", 7, "algebra", "alg_quadratics")
def _(r):
    N = r.choice([7, 13, 19, 21, 31, 37, 39, 43, 49, 57, 61, 63, 91, 93, 133])
    sols = [(x, y) for x in range(-40, 41) for y in range(-40, 41) if x * x + x * y + y * y == N]
    ans = len(sols)
    work = []
    for y in range(0, 40):
        rest = 4 * N - 3 * y * y
        if rest < 0:
            break
        u = math.isqrt(rest)
        if u * u == rest:
            xs = sorted({(u - y) // 2, (-u - y) // 2}) if (u - y) % 2 == 0 else []
            if xs:
                work.append(f"$y = {y}$: $(2x + {y})^2 = {rest}$, so $2x + {y} = \\pm {u}$ and $x = {', '.join(map(str, xs))}$")
    p = f"How many ordered pairs of integers $(x, y)$ satisfy $x^2 + xy + y^2 = {N}$?"
    sol = explain(
        "every integer solution, counting $(x, y)$ and $(y, x)$ and sign changes separately.",
        "complete the square: multiply by $4$ to get $(2x + y)^2 + 3y^2 = " + str(4 * N) + "$. Now $y$ is trapped in a small range, and for each $y$ the rest must be a perfect square.",
        [
            f"Since $3y^2 \\le {4 * N}$, we need $|y| \\le {math.isqrt(4 * N // 3)}$.",
            "Checking $y \\ge 0$: " + "; ".join(work) + ".",
            f"Each solution with $y > 0$ has a partner $(-x, -y)$. Collecting every pair gives ${ans}$ solutions: " + ", ".join(f"$({x}, {y})$" for x, y in sols) + ".",
        ],
        f"${ans}$.",
        "counting only positive solutions, or forgetting that $(x, y) \\to (-x, -y)$ and $(x, y) \\to (y, x)$ give new ordered pairs.",
    )
    pos = sum(1 for x, y in sols if x > 0 and y > 0)
    wrong = [ans // 2, ans + 6, max(ans - 6, 1) if ans - 6 != ans // 2 else ans + 12, pos, 6 if ans != 6 else 18]
    return (p, ans, wrong, ["Multiply by $4$ and complete the square in $x$: $(2x + y)^2 + 3y^2 = 4N$."], sol)


@family("l7_geo_euler_oi", 7, "geometry", "geo_circles")
def _(r):
    a, b, c = r.choice([(13, 14, 15), (7, 15, 20), (13, 20, 21), (9, 10, 17), (11, 13, 20), (10, 17, 21), (5, 5, 6), (5, 5, 8)])
    s = F(a + b + c, 2)
    K2 = s * (s - a) * (s - b) * (s - c)
    K = F(math.isqrt(K2.numerator), math.isqrt(K2.denominator))
    assert K * K == K2
    R = F(a * b * c) / (4 * K)
    rr = K / s
    OI2 = R * (R - 2 * rr)
    # numeric check with coordinates
    Ax, Ay = 0.0, 0.0
    Bx, By = float(c), 0.0
    Cx = (b * b + c * c - a * a) / (2 * c)
    Cy = math.sqrt(b * b - Cx * Cx)
    Ix = (a * Ax + b * Bx + c * Cx) / (a + b + c)
    Iy = (a * Ay + b * By + c * Cy) / (a + b + c)
    Ox = c / 2
    Oy = (Cx * Cx + Cy * Cy - c * Cx) / (2 * Cy)
    assert abs((Ix - Ox) ** 2 + (Iy - Oy) ** 2 - float(OI2)) < 1e-6
    ans = surd(F(1, OI2.denominator), OI2.numerator * OI2.denominator)
    p = f"A triangle has side lengths ${a}$, ${b}$, and ${c}$. What is the distance between the center of its inscribed circle and the center of its circumscribed circle?"
    sol = explain(
        "the distance $OI$ between the circumcenter $O$ and the incenter $I$.",
        "Euler's formula $OI^2 = R(R - 2r)$ turns this into finding the two radii, and both come from the area.",
        [
            f"Heron: $s = {num(s).tex}$ and the area is $K = \\sqrt{{{num(s).tex} \\cdot {num(s - a).tex} \\cdot {num(s - b).tex} \\cdot {num(s - c).tex}}} = {num(K).tex}$.",
            f"Inradius $r = \\frac{{K}}{{s}} = {num(rr).tex}$. Circumradius $R = \\frac{{abc}}{{4K}} = \\frac{{{a * b * c}}}{{{num(4 * K).tex}}} = {num(R).tex}$.",
            f"$OI^2 = R(R - 2r) = {num(R).tex}\\left({num(R).tex} - {num(2 * rr).tex}\\right) = {num(OI2).tex}$.",
            f"$OI = {ans.tex}$.",
        ],
        f"${ans.tex}$.",
        "using $R - r$ or $R - 2r$ as the distance. Those are lengths, but not the distance between the centers.",
    )
    wrong = [R - rr, R - 2 * rr, surd(F(1, (R * R + 2 * R * rr).denominator), (R * R + 2 * R * rr).numerator * (R * R + 2 * R * rr).denominator),
             surd(F(1, (R * R - rr * rr).denominator), (R * R - rr * rr).numerator * (R * R - rr * rr).denominator), rr]
    return (p, ans, wrong, ["Euler's formula: $OI^2 = R(R - 2r)$. Find the area first, then $r = K/s$ and $R = abc/(4K)$."], sol, True)


@family("l7_geo_three_tangent", 7, "geometry", "geo_circles")
def _(r):
    a, b = sorted(r.sample(range(1, 7), 2))
    if b / a > 5:
        return None
    r1, r2 = a * a, b * b
    ans = F(a * a * b * b, (a + b) ** 2)
    # numeric check: distance between tangent points along the line
    d = lambda u, v: 2 * math.sqrt(u * v)  # noqa: E731
    x = float(ans)
    assert abs(d(r1, r2) - d(r1, x) - d(r2, x)) < 1e-9
    p = (f"Two circles with radii ${r1}$ and ${r2}$ are tangent to each other and to a line $\\ell$, on the same side of $\\ell$. "
         "A third circle fits in the gap between them: it is tangent to $\\ell$ and to both circles. What is its radius?")
    sol = explain(
        "the radius $x$ of the small circle squeezed between the two big ones and the line.",
        "for two circles of radii $R$ and $S$ that touch each other and the same line, the points where they touch the line are $2\\sqrt{RS}$ apart (a right triangle with hypotenuse $R + S$ and leg $R - S$).",
        [
            f"The big circles touch $\\ell$ at points $2\\sqrt{{{r1} \\cdot {r2}}} = {2 * a * b}$ apart.",
            f"The small circle touches $\\ell$ between them, $2\\sqrt{{{r1}x}} = {2 * a}\\sqrt{{x}}$ from the first point and $2\\sqrt{{{r2}x}} = {2 * b}\\sqrt{{x}}$ from the second.",
            f"So ${2 * a}\\sqrt{{x}} + {2 * b}\\sqrt{{x}} = {2 * a * b}$, giving $\\sqrt{{x}} = \\frac{{{a * b}}}{{{a + b}}}$.",
            f"$x = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "stopping at $\\sqrt{x}$ and forgetting to square.",
    )
    wrong = [F(a * b, a + b), 2 * ans, F((b - a) ** 2, 4), F(a * a * b * b, a * a + b * b), F(r1 + r2, 4) if F(r1 + r2, 4) != ans else ans + 1]
    return (p, ans, wrong, ["Two circles that touch each other and a line touch the line $2\\sqrt{Rr}$ apart. Write the gap two ways."], sol)


def _vp_fact(n, p):
    v, q = 0, p
    while q <= n:
        v += n // q
        q *= p
    return v


def _factor(n):
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


@family("l7_nt_trailing_base", 7, "number_theory", "nt_factorials")
def _(r):
    base = r.choice([12, 18, 20, 24, 45, 72, 36, 48, 50])
    n = r.randint(20, 90)
    fac = _factor(base)
    per = {p: (_vp_fact(n, p), e, _vp_fact(n, p) // e) for p, e in fac.items()}
    ans = min(t for _, _, t in per.values())
    # brute force: write n! in the base and count zeros
    m, z = math.factorial(n), 0
    while m % base == 0:
        m //= base
        z += 1
    assert z == ans
    p = f"When ${n}!$ is written in base ${base}$, how many zeros does it end with?"
    fstr = " \\cdot ".join(f"{q}^{{{e}}}" if e > 1 else str(q) for q, e in fac.items())
    sol = explain(
        f"the largest $k$ with ${base}^k$ dividing ${n}!$.",
        f"each trailing zero in base ${base}$ is one factor of ${base} = {fstr}$. Count each prime in ${n}!$ (Legendre's formula), then see which one runs out first.",
        [f"Prime ${q}$: ${n}!$ has ${v}$ factors of ${q}$, enough for $\\lfloor {v}/{e} \\rfloor = {t}$ copies of ${q}^{{{e}}}$." if e > 1
         else f"Prime ${q}$: ${n}!$ has ${v}$ factors of ${q}$." for q, (v, e, t) in per.items()]
        + [f"The smallest of these limits is ${ans}$."],
        f"${ans}$.",
        "using the count for the largest prime, or forgetting to divide by the exponent when a prime appears squared or cubed in the base.",
    )
    wrong = [min(v for v, _, _ in per.values()), per[max(fac)][0], _vp_fact(n, 5), ans + 1, ans - 1, max(t for _, _, t in per.values())]
    return (p, ans, wrong, ["Factor the base into primes. For each prime, count how many times it divides $n!$, then divide by its exponent in the base."], sol)


def _tau(n):
    return reduce(lambda acc, e: acc * (e + 1), _factor(n).values(), 1)


@family("l7_nt_square_divisors", 7, "number_theory", "nt_divisors")
def _(r):
    exps = r.choice([(2, 1), (3, 2), (4, 1), (2, 2), (3, 1), (5, 2), (2, 1, 1), (3, 1, 1)])
    primes = r.choice([(2, 3, 5), (2, 5, 3), (3, 2, 5)])
    N = 1
    for q, e in zip(primes, exps):
        N *= q ** e
    if N > 3000:
        return None
    N2 = N * N
    brute = sum(1 for d in range(1, N) if N2 % d == 0 and N % d != 0)
    tN2, tN = _tau(N2), _tau(N)
    ans = (tN2 - 1) // 2 - (tN - 1)
    assert brute == ans
    fstr = " \\cdot ".join(f"{q}^{{{e}}}" if e > 1 else str(q) for q, e in zip(primes, exps))
    p = f"How many positive divisors of ${N}^2$ are less than ${N}$ but do not divide ${N}$?"
    sol = explain(
        f"divisors $d$ of ${N}^2$ with $d < {N}$ and $d \\nmid {N}$.",
        f"divisors of ${N}^2$ pair up as $d \\leftrightarrow \\frac{{{N}^2}}{{d}}$, one below ${N}$ and one above, with ${N}$ paired with itself. Then remove the ones that divide ${N}$.",
        [
            f"${N} = {fstr}$, so ${N}^2$ has ${tN2}$ divisors and ${N}$ has ${tN}$.",
            f"Leaving out ${N}$ itself, the other ${tN2 - 1}$ divisors of ${N}^2$ split evenly: ${(tN2 - 1) // 2}$ are less than ${N}$.",
            f"Every divisor of ${N}$ except ${N}$ is less than ${N}$: that is ${tN - 1}$ of them, and they must be removed.",
            f"${(tN2 - 1) // 2} - {tN - 1} = {ans}$.",
        ],
        f"${ans}$.",
        "forgetting that $N$ pairs with itself, or subtracting all of $N$'s divisors including $N$.",
    )
    wrong = [(tN2 - 1) // 2, tN2 - tN, ans + 1, (tN2 - 1) // 2 - tN, ans * 2]
    return (p, ans, wrong, ["Pair each divisor $d$ of $N^2$ with $N^2/d$. Exactly one of each pair is below $N$."], sol)


@family("l7_cp_runs", 7, "counting_probability", "cp_casework")
def _(r):
    n = r.randint(8, 15)
    even_letter, odd_letter = r.choice([("A", "B"), ("B", "A")])

    def ok(sq):
        i = 0
        while i < len(sq):
            j = i
            while j < len(sq) and sq[j] == sq[i]:
                j += 1
            L = j - i
            if sq[i] == even_letter and L % 2:
                return False
            if sq[i] == odd_letter and L % 2 == 0:
                return False
            i = j
        return True

    brute = sum(1 for sq in product("AB", repeat=n) if ok(sq))
    e = {1: 0, 2: 1}
    o = {1: 1, 2: 0}
    for k in range(3, n + 1):
        e[k] = e[k - 2] + o[k - 2]
        o[k] = e[k - 1] + o[k - 2]
    ans = e[n] + o[n]
    assert ans == brute
    table = ", ".join(f"$({e[k]}, {o[k]})$" for k in range(1, n + 1))
    p = (f"How many strings of ${n}$ letters, each $A$ or $B$, have the property that every run of consecutive {even_letter}'s has even length "
         f"and every run of consecutive {odd_letter}'s has odd length? (For example, {'AABAA' if even_letter == 'A' else 'BBABB'} works and "
         f"{'ABB' if even_letter == 'A' else 'BAA'} does not.)")
    sol = explain(
        "the number of valid strings of length " + str(n) + ".",
        f"build the strings from the end. Let $e_k$ count valid strings of length $k$ ending in {even_letter} and $o_k$ those ending in {odd_letter}.",
        [
            f"A string ending in {even_letter} ends with a run of even length: either the last two letters start that run (so the first $k - 2$ letters form any valid string ending in {odd_letter}), or they extend a valid string that already ended in {even_letter}. So $e_k = e_{{k-2}} + o_{{k-2}}$.",
            f"A string ending in {odd_letter} either ends with a single {odd_letter} after a string ending in {even_letter}, or adds two more {odd_letter}'s to a string ending in {odd_letter}. So $o_k = e_{{k-1}} + o_{{k-2}}$.",
            f"Start with $(e_1, o_1) = (0, 1)$ and $(e_2, o_2) = (1, 0)$. The pairs $(e_k, o_k)$ for $k = 1$ to ${n}$ are " + table + ".",
            f"Total for length ${n}$: ${e[n]} + {o[n]} = {ans}$.",
        ],
        f"${ans}$.",
        "a recursion that only tracks the total, which loses which letter the string ends with.",
    )
    wrong = [e[n], o[n], ans + e[n - 1], 2 ** (n // 2), ans - o[n - 1] if ans - o[n - 1] > 0 else ans + 3]
    return (p, ans, wrong, ["Track two counts: strings ending in each letter. Then add a run of the right length at the end."], sol)


@family("l7_cp_obtuse_ngon", 7, "counting_probability", "cp_probability")
def _(r):
    n = r.randint(7, 14)
    tri = list(combinations(range(n), 3))
    obt = 0
    for t in tri:
        a, b, c = t
        arcs = [b - a, c - b, n - c + a]
        if 2 * max(arcs) > n:
            obt += 1
    m = (n - 1) // 2
    assert obt == n * comb(m, 2)
    ans = F(obt, len(tri))
    right = (n // 2) * (n - 2) if n % 2 == 0 else 0
    p = f"Three different vertices of a regular ${n}$-gon are chosen at random. What is the probability that they form an obtuse triangle?"
    sol = explain(
        f"the fraction of the $\\binom{{{n}}}{{3}} = {len(tri)}$ vertex triples that make an obtuse triangle.",
        "the triangle is inscribed in the circle, and an inscribed angle is obtuse exactly when the arc opposite it is more than half the circle. So the triangle is obtuse exactly when all three vertices lie within an arc shorter than a semicircle.",
        [
            f"Go around the circle and let $P$ be the first of the three vertices (counterclockwise) in that short arc. The other two must be among the next ${m}$ vertices, since those are the ones less than halfway around from $P$.",
            f"So each of the ${n}$ choices of $P$ gives $\\binom{{{m}}}{{2}} = {comb(m, 2)}$ obtuse triangles, and each obtuse triangle is counted once: ${n} \\cdot {comb(m, 2)} = {obt}$.",
            (f"(With ${n}$ even, the ${right}$ triangles that use a diameter are right, not obtuse, so they are not counted.)" if right else
             f"(With ${n}$ odd, no triangle is a right triangle, because no two vertices are opposite each other.)"),
            f"Probability: $\\frac{{{obt}}}{{{len(tri)}}} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "counting right triangles as obtuse, or counting each obtuse triangle once for every vertex instead of once.",
    )
    cands = [1 - ans, F(obt + right, len(tri)), F(3, 4), F(1, 2), F(obt, comb(n, 3) + n), F(2 * obt, 3 * len(tri)), F(1, 4), F(3, 5)]
    wrong = [w for w in cands if 0 < w < 1 and w != ans]
    return (p, ans, wrong, ["An inscribed triangle is obtuse exactly when all three vertices fit inside an arc smaller than a semicircle."], sol)


# ============================================================ AMC 12 ONLY

T = "amc12"


@family("l7_trig_products", 7, "trigonometry", "trig_identities", T)
def _(r):
    n = r.randint(2, 6)
    m = 2 * n + 1
    kind = r.choice(["sin", "cos"])
    fn = "\\sin" if kind == "sin" else "\\cos"
    val = 1.0
    for k in range(1, n + 1):
        val *= math.sin(k * math.pi / m) if kind == "sin" else math.cos(k * math.pi / m)
    if kind == "sin":
        ans = surd(F(1, 2 ** n), m)
        wrong = [num(F(1, 2 ** n)), surd(F(1, 2 ** (n - 1)), m), surd(F(1, 2 ** n), n), num(F(m, 4 ** n))]
    else:
        ans = num(F(1, 2 ** n))
        wrong = [surd(F(1, 2 ** n), m), num(F(1, 2 ** (n + 1))), num(F(1, 2 ** (n - 1))), num(F(m, 4 ** n))]
    assert abs(ans.key - val) < 1e-12
    terms = " ".join(f"{fn}\\frac{{{'' if k == 1 else k}\\pi}}{{{m}}}" for k in range(1, n + 1))
    p = f"What is ${terms}$?"
    if kind == "sin":
        steps = [
            f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{m}}} + i\\sin\\frac{{2\\pi}}{{{m}}}$. The numbers $\\omega^k$ for $k = 1, \\ldots, {m - 1}$ are the roots of $\\frac{{z^{{{m}}} - 1}}{{z - 1}} = 1 + z + \\cdots + z^{{{m - 1}}}$, so $\\prod_{{k=1}}^{{{m - 1}}} (1 - \\omega^k) = {m}$ (plug in $z = 1$).",
            f"Each factor has size $|1 - \\omega^k| = 2\\sin\\frac{{k\\pi}}{{{m}}}$, so $\\prod_{{k=1}}^{{{m - 1}}} 2\\sin\\frac{{k\\pi}}{{{m}}} = {m}$.",
            f"Since $\\sin\\frac{{k\\pi}}{{{m}}} = \\sin\\frac{{({m} - k)\\pi}}{{{m}}}$, that product is the square of ours times $2^{{{2 * n}}}$: $2^{{{2 * n}}} P^2 = {m}$.",
            f"$P = \\frac{{\\sqrt{{{m}}}}}{{2^{{{n}}}}} = {ans.tex}$.",
        ]
        idea = "connect the sines to the $" + str(m) + "$th roots of unity, whose distances from $1$ are $2\\sin\\frac{k\\pi}{" + str(m) + "}$."
    else:
        steps = [
            f"Call the product $P$ and let $S = \\prod_{{k=1}}^{{{n}}} \\sin\\frac{{k\\pi}}{{{m}}}$, which is not zero.",
            f"Using $2\\sin x\\cos x = \\sin 2x$ on each factor: $2^{{{n}}} S P = \\prod_{{k=1}}^{{{n}}} \\sin\\frac{{2k\\pi}}{{{m}}}$.",
            f"The angles $\\frac{{2k\\pi}}{{{m}}}$ are $\\frac{{2\\pi}}{{{m}}}, \\frac{{4\\pi}}{{{m}}}, \\ldots$; replacing any angle above $\\frac{{\\pi}}{{2}}$ by $\\pi$ minus it (same sine) gives exactly the angles $\\frac{{\\pi}}{{{m}}}, \\ldots, \\frac{{{n}\\pi}}{{{m}}}$ again. So the right side equals $S$.",
            f"$2^{{{n}}} S P = S$, so $P = {ans.tex}$.",
        ]
        idea = "multiply by the matching product of sines and use the double angle formula, then notice the sines come back in a different order."
    sol = explain(f"the value of the product of ${n}$ {kind}ines.", idea, steps, f"${ans.tex}$.", "trying to multiply decimal approximations; the exact value needs the symmetry argument.")
    return (p, ans, wrong, ["Pair the product with roots of unity or with the double angle formula $\\sin 2x = 2\\sin x\\cos x$."], sol)


@family("l7_log_sum_squares", 7, "logarithms", "log_rules", T)
def _(r):
    pp = r.randint(4, 14)
    q = r.randint(2, pp * pp // 3)
    if pp * pp - 2 * q <= 0:
        return None
    ans = surd(1, pp * pp - 2 * q)
    # check that real logs exist: a + b + c = p and ab + bc + ca = q need p^2 >= 3q
    assert pp * pp >= 3 * q
    p = (f"Positive real numbers $x$, $y$, and $z$ satisfy $xyz = 10^{{{pp}}}$ and $(\\log x)(\\log yz) + (\\log y)(\\log z) = {q}$, where $\\log$ is base $10$. "
         "What is $\\sqrt{(\\log x)^2 + (\\log y)^2 + (\\log z)^2}$?")
    sol = explain(
        "a symmetric expression in three logs.",
        "name the logs $a = \\log x$, $b = \\log y$, $c = \\log z$. Both conditions become statements about $a + b + c$ and $ab + bc + ca$.",
        [
            f"$\\log(xyz) = a + b + c = {pp}$.",
            f"$\\log yz = b + c$, so the second condition is $a(b + c) + bc = ab + bc + ca = {q}$.",
            f"$a^2 + b^2 + c^2 = (a + b + c)^2 - 2(ab + bc + ca) = {pp * pp} - {2 * q} = {pp * pp - 2 * q}$.",
            f"The square root is ${ans.tex}$.",
        ],
        f"${ans.tex}$.",
        "expanding $(a + b + c)^2$ but forgetting the factor $2$ on the cross terms.",
    )
    wrong = [surd(1, pp * pp + 2 * q), surd(1, pp * pp - q), num(pp), surd(1, abs(pp * pp - 4 * q)) if pp * pp != 4 * q else num(pp + 1), num(F(pp * pp - 2 * q, 2))]
    return (p, ans, wrong, ["Let $a = \\log x$, $b = \\log y$, $c = \\log z$. Rewrite both conditions in $a$, $b$, $c$."], sol)


@family("l7_cx_reciprocal_sum", 7, "complex_numbers", "cx_roots_unity", T)
def _(r):
    n = r.randint(3, 7)
    c = r.choice([2, 3])
    w = cmath.exp(2j * math.pi / n)
    val = sum(1 / (c - w ** k) for k in range(n))
    ans = F(n * c ** (n - 1), c ** n - 1)
    assert abs(val.real - float(ans)) < 1e-9 and abs(val.imag) < 1e-9
    p = (f"Let $\\omega = \\cos\\frac{{2\\pi}}{{{n}}} + i\\sin\\frac{{2\\pi}}{{{n}}}$. What is "
         f"$\\displaystyle\\sum_{{k=0}}^{{{n - 1}}} \\frac{{1}}{{{c} - \\omega^k}}$?")
    sol = explain(
        "a sum over all " + str(n) + "th roots of unity.",
        f"the roots of unity are the roots of $P(z) = z^{{{n}}} - 1$. For any polynomial with roots $r_k$, $\\sum \\frac{{1}}{{x - r_k}} = \\frac{{P'(x)}}{{P(x)}}$ (take the log of $P(x) = \\prod (x - r_k)$ and differentiate).",
        [
            f"Here $P(x) = x^{{{n}}} - 1$ and $P'(x) = {n}x^{{{n - 1}}}$.",
            f"At $x = {c}$: $\\frac{{{n} \\cdot {c}^{{{n - 1}}}}}{{{c}^{{{n}}} - 1}} = \\frac{{{n * c ** (n - 1)}}}{{{c ** n - 1}}}$.",
            f"Simplified: ${num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"treating every $\\omega^k$ as $1$, which gives $\\frac{{{n}}}{{{c} - 1}}$.",
    )
    wrong = [F(n, c - 1), F(n * c ** n, c ** n - 1), F(n, c), F(c ** (n - 1), c ** n - 1), F(n * c ** (n - 1), c ** n + 1)]
    return (p, ans, wrong, ["Use $\\frac{P'(x)}{P(x)} = \\sum \\frac{1}{x - r_k}$ for $P(x) = x^n - 1$."], sol)


@family("l7_poly_lagrange_trick", 7, "polynomials", "poly_remainder", T)
def _(r):
    n = r.randint(3, 8)
    xs = list(range(n + 1))
    ys = [F(k, k + 1) for k in xs]

    def P(x):
        tot = F(0)
        for i, xi in enumerate(xs):
            term = ys[i]
            for j, xj in enumerate(xs):
                if j != i:
                    term *= F(x - xj, xi - xj)
            tot += term
        return tot

    ans = P(n + 1)
    assert ans == F(n + 1 + (-1) ** (n + 1), n + 2)
    p = f"A polynomial $P$ of degree ${n}$ satisfies $P(k) = \\dfrac{{k}}{{k + 1}}$ for $k = 0, 1, 2, \\ldots, {n}$. What is $P({n + 1})$?"
    sign = "+" if (n + 1) % 2 == 0 else "-"
    sol = explain(
        f"one more value of a polynomial pinned down by ${n + 1}$ values.",
        "clear the fraction. $Q(x) = (x + 1)P(x) - x$ is a polynomial that is zero at every given point, so it is easy to write down.",
        [
            f"$Q(k) = (k + 1)\\frac{{k}}{{k + 1}} - k = 0$ for $k = 0, \\ldots, {n}$, and $Q$ has degree ${n + 1}$. So $Q(x) = a\\,x(x - 1)(x - 2)\\cdots(x - {n})$.",
            f"Find $a$ with $x = -1$: $Q(-1) = 0 \\cdot P(-1) + 1 = 1$, and the product is $(-1)(-2)\\cdots(-{n + 1}) = (-1)^{{{n + 1}}}\\,{n + 1}!$. So $a = \\frac{{(-1)^{{{n + 1}}}}}{{{n + 1}!}}$.",
            f"At $x = {n + 1}$: $Q({n + 1}) = a \\cdot {n + 1}! = (-1)^{{{n + 1}}} = {sign}1$.",
            f"$({n + 2})P({n + 1}) - {n + 1} = {sign}1$, so $P({n + 1}) = \\frac{{{n + 1} {sign} 1}}{{{n + 2}}} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"assuming the pattern continues and answering $\\frac{{{n + 1}}}{{{n + 2}}}$. A polynomial can't equal $\\frac{{x}}{{x + 1}}$ everywhere, so it must break off.",
    )
    wrong = [F(n + 1, n + 2), F(1), F(n, n + 2), F(n + 3, n + 2), F(n - 1, n + 2), F(0)]
    return (p, ans, wrong, ["Look at $Q(x) = (x + 1)P(x) - x$. Where is it zero?"], sol)


@family("l7_ser_weighted", 7, "sequences_series", "ser_geometric", T)
def _(r):
    k = r.choice([2, 3, 4, 5])
    kind = r.choice(["square", "fib"])
    if kind == "square":
        ans = F(k * (k + 1), (k - 1) ** 3)
        val = sum(n * n / k ** n for n in range(1, 400))
        p = f"What is $\\displaystyle\\sum_{{n=1}}^{{\\infty}} \\frac{{n^2}}{{{k}^n}}$?"
        steps = [
            f"Start from $\\sum_{{n \\ge 0}} x^n = \\frac{{1}}{{1 - x}}$. Differentiating and multiplying by $x$ gives $\\sum n x^n = \\frac{{x}}{{(1 - x)^2}}$.",
            "Do it again: $\\sum n^2 x^n = x \\cdot \\frac{d}{dx}\\frac{x}{(1 - x)^2} = \\frac{x(1 + x)}{(1 - x)^3}$.",
            f"Put $x = \\frac{{1}}{{{k}}}$: $\\frac{{\\frac{{1}}{{{k}}} \\cdot \\frac{{{k + 1}}}{{{k}}}}}{{\\left(\\frac{{{k - 1}}}{{{k}}}\\right)^3}} = \\frac{{{k * (k + 1)}}}{{{(k - 1) ** 3}}}$.",
        ]
        idea = "build the sum from the geometric series by repeatedly differentiating and multiplying by $x$."
        wrong = [F(k, (k - 1) ** 2), F(k * (k + 1), (k - 1) ** 2), F(2 * k, (k - 1) ** 3), F(k * k, (k - 1) ** 3), ans + 1]
        hint = "Start with $\\sum x^n = \\frac{1}{1 - x}$ and apply \"differentiate, then multiply by $x$\" twice."
    else:
        ans = F(k, k * k - k - 1)
        fib = [0, 1]
        while len(fib) < 200:
            fib.append(fib[-1] + fib[-2])
        val = sum(fib[n] / k ** n for n in range(1, 200))
        p = (f"The Fibonacci numbers are $F_1 = F_2 = 1$ and $F_{{n+2}} = F_{{n+1}} + F_n$. "
             f"What is $\\displaystyle\\sum_{{n=1}}^{{\\infty}} \\frac{{F_n}}{{{k}^n}}$?")
        steps = [
            f"Call the sum $S$. Write $S = \\frac{{F_1}}{{{k}}} + \\frac{{F_2}}{{{k}^2}} + \\sum_{{n \\ge 3}} \\frac{{F_{{n-1}} + F_{{n-2}}}}{{{k}^n}}$.",
            f"The last part splits into $\\frac{{1}}{{{k}}}\\left(S - \\frac{{1}}{{{k}}}\\right) + \\frac{{1}}{{{k}^2}}S$.",
            f"So $S = \\frac{{1}}{{{k}}} + \\frac{{1}}{{{k * k}}} + \\frac{{S}}{{{k}}} - \\frac{{1}}{{{k * k}}} + \\frac{{S}}{{{k * k}}}$, which gives $S\\left(1 - \\frac{{1}}{{{k}}} - \\frac{{1}}{{{k * k}}}\\right) = \\frac{{1}}{{{k}}}$.",
            f"$S = \\frac{{{k}}}{{{k * k} - {k} - 1}} = {num(ans).tex}$.",
        ]
        idea = "use the Fibonacci rule inside the sum, so the sum reappears in terms of itself."
        wrong = [F(1, k * k - k - 1), F(k, (k - 1) ** 2), F(k, k * k - k + 1), F(k * k, k * k - k - 1), ans + F(1, 2)]
        hint = "Use $F_n = F_{n-1} + F_{n-2}$ inside the sum and solve for the sum."
    assert abs(val - float(ans)) < 1e-9
    sol = explain("the value of an infinite sum.", idea, steps, f"${num(ans).tex}$.", "adding many terms and guessing; the sum has an exact value.")
    return (p, ans, wrong, [hint], sol)
