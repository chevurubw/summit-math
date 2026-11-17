"""Mock exam families shared by the AMC 10 and AMC 12, difficulty levels 4 to 6."""
import math
from fractions import Fraction as F
from itertools import combinations, product

from common import NAMES, comb, explain, num, var
from mock_common import family, surd

# ============================================================ LEVEL 4 (AMC 10 #16 to 20, AMC 12 #11 to 15)


@family("l4_alg_abs_sum", 4, "algebra", "alg_absolute")
def _(r):
    a, b = sorted(r.sample(range(-12, 13), 2))
    c = r.randint(b - a + 1, b - a + 20)
    sols = [x for x in range(-200, 201) if abs(x - a) + abs(x - b) <= c]
    ans = len(sols)
    extra = c - (b - a)
    fa = f"|x{' - ' if a >= 0 else ' + '}{abs(a)}|"
    fb = f"|x{' - ' if b >= 0 else ' + '}{abs(b)}|"
    p = f"How many integers $x$ satisfy ${fa} + {fb} \\le {c}$?"
    sol = explain(
        f"how many integers $x$ have total distance at most ${c}$ from the two points ${a}$ and ${b}$ on the number line.",
        f"$|x - a|$ is the distance from $x$ to $a$. So the left side is (distance to ${a}$) $+$ (distance to ${b}$).",
        [
            f"If $x$ is between ${a}$ and ${b}$, the two distances add to exactly the gap ${b} - ({a}) = {b - a}$. That is at most ${c}$, so all ${b - a + 1}$ integers from ${a}$ to ${b}$ work.",
            f"If $x$ is outside the segment, every step away adds $2$ to the total (one for each distance). We have ${c} - {b - a} = {extra}$ to spare, which allows $\\left\\lfloor \\frac{{{extra}}}{{2}} \\right\\rfloor = {extra // 2}$ extra steps on each side.",
            f"So $x$ runs from ${a} - {extra // 2} = {sols[0]}$ to ${b} + {extra // 2} = {sols[-1]}$.",
            f"Count: ${sols[-1]} - ({sols[0]}) + 1 = {ans}$.",
        ],
        f"${ans}$ integers.",
        "forgetting that both distances grow when you move outside the segment, so the total grows by $2$ per step, not $1$.",
    )
    return (p, ans, [ans - 1, ans + 1, c, 2 * c + 1, b - a + 1], ["Between the two points the sum is constant; outside it grows by $2$ per step."], sol)


@family("l4_alg_recip_power", 4, "algebra", "alg_factoring")
def _(r):
    k = r.randint(3, 9)
    ask = r.choice([3, 4])
    v2 = k * k - 2
    if ask == 3:
        ans = k ** 3 - 3 * k
        steps = [
            f"Cube both sides: $$ \\left(x + \\frac{{1}}{{x}}\\right)^3 = x^3 + 3x + \\frac{{3}}{{x}} + \\frac{{1}}{{x^3}} = x^3 + \\frac{{1}}{{x^3}} + 3\\left(x + \\frac{{1}}{{x}}\\right). $$",
            f"Plug in $x + \\frac{{1}}{{x}} = {k}$: ${k ** 3} = x^3 + \\frac{{1}}{{x^3}} + 3 \\cdot {k}$.",
            f"Solve: $x^3 + \\frac{{1}}{{x^3}} = {k ** 3} - {3 * k} = {ans}$.",
        ]
        trap = f"cubing to get ${k ** 3}$ and forgetting the middle terms $3\\left(x + \\frac{{1}}{{x}}\\right)$."
    else:
        ans = v2 * v2 - 2
        steps = [
            f"Square once: $\\left(x + \\frac{{1}}{{x}}\\right)^2 = x^2 + 2 + \\frac{{1}}{{x^2}}$, so $x^2 + \\frac{{1}}{{x^2}} = {k * k} - 2 = {v2}$.",
            f"Square again: $\\left(x^2 + \\frac{{1}}{{x^2}}\\right)^2 = x^4 + 2 + \\frac{{1}}{{x^4}}$, so $x^4 + \\frac{{1}}{{x^4}} = {v2}^2 - 2 = {v2 * v2} - 2 = {ans}$.",
        ]
        trap = f"computing ${k}^4 = {k ** 4}$. The cross terms $+2$ have to be removed each time you square."
    p = f"If $x + \\dfrac{{1}}{{x}} = {k}$, what is $x^{{{ask}}} + \\dfrac{{1}}{{x^{{{ask}}}}}$?"
    sol = explain(f"$x^{{{ask}}} + \\frac{{1}}{{x^{{{ask}}}}}$ without solving for $x$ (which would be messy).",
                  "raise $x + \\frac{1}{x}$ to a power. Because $x \\cdot \\frac{1}{x} = 1$, the cross terms are plain numbers.", steps, f"${ans}$.", trap)
    return (p, ans, [k ** ask, ans + 2, ans - 2, k ** ask - ask, v2], ["Square or cube the given equation."], sol)


@family("l4_alg_three_workers", 4, "algebra", "alg_rates")
def _(r):
    ta, tb, tc = [F(1, r.randint(2, 12)) for _ in range(3)]
    ab, bc, ac = ta + tb, tb + tc, ta + tc
    if any(x.numerator != 1 for x in (ab, bc, ac)):
        return None
    all3 = ta + tb + tc
    hours = 1 / all3
    n1, n2, n3 = r.sample(NAMES, 3)
    u, v, w = var(n1), var(n2), var(n3)
    A, B, Cc = ab.denominator, bc.denominator, ac.denominator
    p = (f"{n1} and {n2} together can paint a fence in ${A}$ hours, {n2} and {n3} in ${B}$ hours, and "
         f"{n1} and {n3} in ${Cc}$ hours. How many hours do all three take working together?")
    sol = explain(
        "the time for all three working together.",
        f"work with rates (fences per hour), not times. Let ${u}$, ${v}$, ${w}$ be the fraction of the fence {n1}, {n2} and {n3} each paint in one hour. Rates add; times do not.",
        [
            f"The three facts become $$ {u} + {v} = \\frac{{1}}{{{A}}}, \\quad {v} + {w} = \\frac{{1}}{{{B}}}, \\quad {u} + {w} = \\frac{{1}}{{{Cc}}}. $$",
            f"Add all three equations. Each person appears twice: $$ 2({u} + {v} + {w}) = \\frac{{1}}{{{A}}} + \\frac{{1}}{{{B}}} + \\frac{{1}}{{{Cc}}} = {num(2 * all3).tex}. $$",
            f"So together they paint ${u} + {v} + {w} = {num(all3).tex}$ of the fence per hour.",
            f"Time $= \\frac{{1}}{{\\text{{rate}}}} = {num(hours).tex}$ hours.",
        ],
        f"${num(hours).tex}$ hours.",
        "averaging or adding the times. Only rates can be added.",
    )
    return (p, hours, [F(A + B + Cc, 3), F(A + B + Cc, 6), hours + 1, hours * 2, F(3, 2) if hours != F(3, 2) else F(5, 2)], ["Add the three pairwise rates. Each person is counted twice."], sol)


@family("l4_geo_bisector", 4, "geometry", "geo_similar")
def _(r):
    b, c = r.sample(range(4, 16), 2)
    a = r.randint(abs(b - c) + 1, b + c - 1)
    BD = F(a * c, b + c)
    p = f"In triangle $ABC$, $AB = {c}$, $AC = {b}$, and $BC = {a}$. The bisector of angle $A$ meets $BC$ at $D$. What is $BD$?"
    sol = explain(
        "the length of the piece $BD$ of side $BC$.",
        "Angle Bisector Theorem: the bisector from $A$ splits $BC$ in the same ratio as the two sides next to angle $A$: $\\frac{BD}{DC} = \\frac{AB}{AC}$.",
        [
            f"$\\frac{{BD}}{{DC}} = \\frac{{AB}}{{AC}} = \\frac{{{c}}}{{{b}}}$, so $BD$ is ${c}$ parts and $DC$ is ${b}$ parts.",
            f"Together they make $BC = {a}$, which is ${b + c}$ parts.",
            f"$BD = {a} \\cdot \\frac{{{c}}}{{{b + c}}} = {num(BD).tex}$.",
        ],
        f"$BD = {num(BD).tex}$.",
        f"matching the ratio the wrong way round. $BD$ is next to $B$, so it goes with side $AB = {c}$; that gives ${num(F(a * b, b + c)).tex}$ if you swap them.",
    )
    return (p, BD, [F(a * b, b + c), F(a, 2), BD + 1, F(c * c, b + c), F(a * c, b)], ["The angle bisector splits $BC$ in the ratio $AB : AC$."], sol)


@family("l4_geo_altitude", 4, "geometry", "geo_area")
def _(r):
    base = r.choice([(13, 14, 15), (5, 5, 6), (5, 5, 8), (10, 13, 13), (9, 10, 17), (7, 15, 20), (13, 20, 21), (11, 13, 20), (25, 25, 14), (17, 25, 26)])
    k = r.randint(1, 3)
    a, b, c = [x * k for x in base]
    s = F(a + b + c, 2)
    prod = s * (s - a) * (s - b) * (s - c)
    A = math.isqrt(int(prod))
    assert A * A == prod
    heron = [f"Semiperimeter: $s = \\frac{{{a} + {b} + {c}}}{{2}} = {num(s).tex}$.",
             f"Heron's formula: $$ \\text{{Area}} = \\sqrt{{s(s - a)(s - b)(s - c)}} = \\sqrt{{{num(s).tex} \\cdot {num(s - a).tex} \\cdot {num(s - b).tex} \\cdot {num(s - c).tex}}} = \\sqrt{{{int(prod)}}} = {A}. $$"]
    ask = r.choice(["alt", "inr"])
    if ask == "alt":
        L = max(a, b, c)
        ans = F(2 * A, L)
        p = f"A triangle has sides ${a}$, ${b}$, and ${c}$. What is the length of its shortest altitude?"
        steps = heron + [f"Area $= \\frac{{1}}{{2}} \\cdot \\text{{side}} \\cdot \\text{{altitude}}$, so the altitude to a side is $\\frac{{2 \\cdot \\text{{Area}}}}{{\\text{{side}}}}$. It is shortest when the side is longest, ${L}$.",
                         f"Shortest altitude $= \\frac{{2 \\cdot {A}}}{{{L}}} = {num(ans).tex}$."]
        trap = "dropping the altitude to the shortest side. A longer base needs a shorter height for the same area."
        wrong = [F(2 * A, min(a, b, c)), F(A, L), ans + 1, F(2 * A, sorted([a, b, c])[1]), F(a + b + c, 3)]
    else:
        ans = F(A) / s
        p = f"A triangle has sides ${a}$, ${b}$, and ${c}$. What is the radius of its inscribed circle?"
        steps = heron + ["Split the triangle into three triangles from the incenter. Each has height $r$, so Area $= r \\cdot s$.",
                         f"$r = \\frac{{\\text{{Area}}}}{{s}} = \\frac{{{A}}}{{{num(s).tex}}} = {num(ans).tex}$."]
        trap = "dividing the area by the full perimeter instead of the semiperimeter, which gives half the answer."
        wrong = [ans * 2, F(A, a + b + c), ans + 1, F(a * b * c, 4 * A), ans * F(3, 2)]
    sol = explain(f"the {'shortest altitude' if ask == 'alt' else 'inradius'} of a triangle given only its sides.", "find the area first with Heron's formula, then connect the area to the length you want.", steps, f"${num(ans).tex}$.", trap)
    return (p, ans, wrong, ["Find the area first, with Heron's formula."], sol)


@family("l4_geo_tangent_circles", 4, "geometry", "geo_circles")
def _(r):
    r1, r2 = r.sample([1, 2, 3, 4, 6, 8, 9, 12, 16, 18], 2)
    kind = r.choice(["ext", "dist"])
    if kind == "ext":
        ans = surd(2, r1 * r2)
        p = f"Circles with radii ${r1}$ and ${r2}$ are externally tangent. A line is tangent to both circles at points $P$ and $Q$, not crossing between them. What is $PQ$?"
        sol = explain(
            "the length of the common tangent segment $PQ$.",
            "radii to the points of tangency are both perpendicular to the tangent line. Sliding one radius over makes a right triangle.",
            [
                f"The centers are ${r1} + {r2} = {r1 + r2}$ apart because the circles touch.",
                f"Draw the trapezoid with corners at the two centers, $P$ and $Q$. Its parallel sides are ${r1}$ and ${r2}$. Draw a line from the smaller center parallel to $PQ$: it forms a right triangle with hypotenuse ${r1 + r2}$ and one leg ${abs(r1 - r2)}$.",
                f"The other leg equals $PQ$: $$ PQ = \\sqrt{{{r1 + r2}^2 - {abs(r1 - r2)}^2}} = \\sqrt{{{(r1 + r2) ** 2 - (r1 - r2) ** 2}}} = {ans.tex}. $$",
                f"(In general this is $2\\sqrt{{r_1 r_2}}$.)",
            ],
            f"$PQ = {ans.tex}$.",
            f"using the distance between centers, ${r1 + r2}$, as the tangent length.",
        )
        wrong = [num(r1 + r2), surd(1, r1 * r2), num(abs(r1 - r2)), surd(1, r1 * r1 + r2 * r2), surd(4, r1 * r2)]
    else:
        d = r1 + r2 + r.randint(1, 10)
        val = d * d - (r1 + r2) ** 2
        ans = surd(1, val)
        p = f"Two circles with radii ${r1}$ and ${r2}$ have centers ${d}$ apart. What is the length of a common tangent segment that crosses between the circles?"
        sol = explain(
            "the length of a tangent segment that crosses the line between the centers.",
            "both radii to the tangent points are perpendicular to the tangent, but they point in opposite directions. Extending one radius by the other makes a right triangle.",
            [
                f"Extend the radius of one circle by the radius of the other: a segment of length ${r1} + {r2} = {r1 + r2}$ perpendicular to the tangent.",
                f"This makes a right triangle with hypotenuse ${d}$ (the distance between the centers) and one leg ${r1 + r2}$.",
                f"The other leg is the tangent: $$ \\sqrt{{{d}^2 - {r1 + r2}^2}} = \\sqrt{{{val}}} = {ans.tex}. $$",
            ],
            f"${ans.tex}$.",
            f"using the difference of the radii (${abs(r1 - r2)}$). That is for a tangent that does not cross between the circles.",
        )
        wrong = [surd(1, d * d - (r1 - r2) ** 2), num(d - r1 - r2), surd(1, d * d + (r1 + r2) ** 2), num(d), surd(2, max(val // 4, 2))]
    return (p, ans, wrong, ["Draw the radii to the tangent points; they are both perpendicular to the tangent line."], sol)


@family("l4_nt_power_mod", 4, "number_theory", "nt_modular")
def _(r):
    a = r.choice([2, 3, 5, 6, 7, 10, 11])
    m = r.choice([7, 9, 11, 13])
    if math.gcd(a, m) != 1:
        return None
    n = r.randint(100, 5000)
    ans = pow(a, n, m)
    order = next(k for k in range(1, m) if pow(a, k, m) == 1)
    pw = [pow(a, k, m) for k in range(1, order + 1)]
    p = f"What is the remainder when ${a}^{{{n}}}$ is divided by ${m}$?"
    sol = explain(
        f"${a}^{{{n}}} \\bmod {m}$, without computing a giant number.",
        f"find the first power of ${a}$ that leaves remainder $1$. After that, the remainders repeat.",
        [
            f"Remainders of ${a}^1, {a}^2, \\ldots$ when divided by ${m}$: ${', '.join(map(str, pw))}$. So ${a}^{{{order}}} \\equiv 1 \\pmod{{{m}}}$.",
            f"Divide the exponent by ${order}$: ${n} = {order} \\cdot {n // order} + {n % order}$.",
            f"Then ${a}^{{{n}}} = \\left({a}^{{{order}}}\\right)^{{{n // order}}} \\cdot {a}^{{{n % order}}} \\equiv 1 \\cdot {a}^{{{n % order}}} \\equiv {ans} \\pmod{{{m}}}$.",
        ],
        f"the remainder is ${ans}$.",
        f"using the cycle position ${n % order}$ as the remainder itself, instead of the remainder of ${a}^{{{n % order}}}$.",
    )
    return (p, ans, [x for x in range(m) if x != ans][:4] + [(ans + 1) % m], [f"Find the smallest power of ${a}$ that leaves remainder $1$."], sol)


@family("l4_nt_digit_cond", 4, "number_theory", "nt_divisibility")
def _(r):
    s = r.randint(8, 20)
    d = r.choice([2, 4, 5, 6, 8, 11])
    nums = [x for x in range(100, 1000) if sum(map(int, str(x))) == s and x % d == 0]
    cnt = len(nums)
    if cnt < 2 or cnt > 30:
        return None
    total = sum(1 for x in range(100, 1000) if sum(map(int, str(x))) == s)
    rule = {2: "the last digit is even", 4: "the last two digits form a multiple of $4$", 5: "the last digit is $0$ or $5$",
            6: "it is even and its digit sum is a multiple of $3$", 8: "the whole number is a multiple of $8$ (check directly)", 11: "the alternating sum of digits (first $-$ second $+$ third) is a multiple of $11$"}[d]
    p = f"How many three digit positive integers have digits that add to ${s}$ and are divisible by ${d}$?"
    sol = explain(
        f"three digit numbers with digit sum ${s}$ that are multiples of ${d}$.",
        f"use the divisibility rule for ${d}$: a number is divisible by ${d}$ when {rule}. Combine it with the digit sum condition and list carefully.",
        [
            f"Write the number as $\\overline{{abc}}$ with $a \\ge 1$ and $a + b + c = {s}$.",
            "Apply the divisibility rule to cut down the choices for the last digit(s), then find the matching first digits."
            + (f" Since the digit sum ${s}$ is {'' if s % 3 == 0 else 'not '}a multiple of $3$, {'every candidate passes the $3$ part' if s % 3 == 0 else 'no number can be divisible by $6$'}." if d == 6 else ""),
            "The numbers that work are " + ", ".join(map(str, nums)) + ".",
            f"Count them: ${cnt}$.",
        ],
        f"${cnt}$.",
        "forgetting that the first digit can't be $0$, or missing cases where a digit is $0$.",
    )
    return (p, cnt, [total, cnt + 1, cnt - 1, total // d if total // d != cnt else cnt + 3, cnt + 2], ["Use the divisibility rule to fix the last digit (or digits), then count."], sol)


@family("l4_nt_square_divisors", 4, "number_theory", "nt_divisors")
def _(r):
    ps = r.sample([2, 3, 5, 7], r.choice([2, 3]))
    es = [r.randint(2, 7) for _ in ps]
    kind = r.choice(["square", "cube"])
    k = 2 if kind == "square" else 3
    ans = 1
    for e in es:
        ans *= e // k + 1
    total = 1
    for e in es:
        total *= e + 1
    fact = " \\cdot ".join(f"{p_}^{{{e}}}" for p_, e in zip(ps, es))
    p = f"How many positive divisors of ${fact}$ are perfect {kind}s?"
    opts = []
    for p_, e in zip(ps, es):
        allowed = list(range(0, e + 1, k))
        opts.append(f"the exponent of ${p_}$ can be ${', '.join(map(str, allowed))}$ (${len(allowed)}$ choices)")
    sol = explain(
        f"divisors that are perfect {kind}s.",
        f"a number is a perfect {kind} exactly when every exponent in its prime factorization is a multiple of ${k}$.",
        [
            f"A divisor of ${fact}$ looks like " + " \\cdot ".join(f"{p_}^{{?}}" for p_ in ps).join("$$") + " with each exponent between $0$ and the power shown.",
            f"For a perfect {kind}, each exponent must be a multiple of ${k}$: " + "; ".join(opts) + ".",
            "Multiply the choices: $" + " \\cdot ".join(str(e // k + 1) for e in es) + f" = {ans}$.",
        ],
        f"${ans}$.",
        f"counting all ${total}$ divisors, or forgetting that exponent $0$ is a multiple of ${k}$.",
    )
    return (p, ans, [total, ans + 1, ans * 2, total // k, ans - 1 if ans > 1 else 3], [f"A perfect {kind} divisor uses each prime to a multiple of ${k}$."], sol)


@family("l4_cp_expected_max", 4, "counting_probability", "cp_expected")
def _(r):
    n = r.choice([2, 3])
    sides = r.choice([4, 6])
    kind = r.choice(["max", "min"])
    outs = list(product(range(1, sides + 1), repeat=n))
    tot = len(outs)
    f = max if kind == "max" else min
    ev = F(sum(f(o) for o in outs), tot)
    counts = [sum(1 for o in outs if f(o) == v) for v in range(1, sides + 1)]
    word = "largest" if kind == "max" else "smallest"
    if kind == "max":
        cnt_line = f"The largest is at most $v$ in $v^{n}$ outcomes, so it equals exactly $v$ in $v^{n} - (v - 1)^{n}$ outcomes."
    else:
        cnt_line = f"The smallest is at least $v$ in $({sides + 1} - v)^{n}$ outcomes, so it equals exactly $v$ in $({sides + 1} - v)^{n} - ({sides} - v)^{n}$ outcomes."
    p = f"{['', '', 'Two', 'Three'][n]} fair {sides} sided dice are rolled. What is the expected value of the {word} number rolled?"
    sol = explain(
        f"the average value of the {word} die over all ${tot}$ equally likely outcomes.",
        "expected value $= \\sum v \\cdot P(\\text{value} = v)$. It is easiest to count 'at most' or 'at least' first, then subtract.",
        [
            f"There are ${sides}^{n} = {tot}$ outcomes.",
            cnt_line,
            "Counts for $v = 1, 2, \\ldots$: " + ", ".join(f"${c}$" for c in counts) + f" (they add to ${tot}$).",
            "Expected value: $$ \\frac{" + " + ".join(f"{v} \\cdot {c}" for v, c in zip(range(1, sides + 1), counts)) + f"}}{{{tot}}} = \\frac{{{sum(v * c for v, c in zip(range(1, sides + 1), counts))}}}{{{tot}}} = {num(ev).tex}. $$",
        ],
        f"${num(ev).tex}$.",
        f"answering the average of one die, ${num(F(sides + 1, 2)).tex}$. The {word} of several dice is pulled {'up' if kind == 'max' else 'down'}.",
    )
    return (p, ev, [F(sides + 1, 2), ev + F(1, 2), ev - F(1, 3), F(sides * n, n + 1), ev + F(1, sides)], [f"Find how many outcomes have each value of the {word} die."], sol)


@family("l4_cp_round_table", 4, "counting_probability", "cp_permutations")
def _(r):
    n = r.randint(5, 9)
    kind = r.choice(["apart", "together"])
    tot = math.factorial(n - 1)
    tog = 2 * math.factorial(n - 2)
    ans = tog if kind == "together" else tot - tog
    n1, n2 = r.sample(NAMES, 2)
    word = "must sit next to each other" if kind == "together" else "refuse to sit next to each other"
    p = f"${n}$ people, including {n1} and {n2}, sit around a round table. Seatings that are rotations of each other count as the same. If {n1} and {n2} {word}, how many seatings are possible?"
    steps = [
        f"Around a round table, $n$ people can sit in $(n - 1)!$ ways, because rotations are the same. (Fix one person's seat and arrange the rest.) So with no rule there are $({n - 1})! = {tot}$ seatings.",
        f"Glue {n1} and {n2} into one block. Now there are ${n - 1}$ units around the table: $({n - 2})! = {math.factorial(n - 2)}$ arrangements.",
        f"Inside the block they can sit in $2$ orders, so seatings with them together: $2 \\cdot {math.factorial(n - 2)} = {tog}$.",
    ]
    if kind == "apart":
        steps.append(f"Seatings with them apart: ${tot} - {tog} = {ans}$.")
    sol = explain(f"seatings where {n1} and {n2} are {'together' if kind == 'together' else 'not next to each other'}.",
                  "handle 'next to each other' by gluing the pair into one block. For 'not next to each other', subtract from the total.", steps, f"${ans}$ seatings.",
                  f"using ${n}!$ instead of $({n - 1})!$, which treats rotations as different, or forgetting the $2$ orders inside the block.")
    return (p, ans, [math.factorial(n) - 2 * math.factorial(n - 1), tot, tot - ans, ans // 2, math.factorial(n - 2)], ["Glue the two people into one block, then arrange the block and everyone else in a circle."], sol)


@family("l4_cp_draw", 4, "counting_probability", "cp_probability")
def _(r):
    R, B = r.randint(3, 8), r.randint(3, 8)
    k = r.randint(3, 4)
    kind = r.choice(["each", "exact"])
    tot = comb(R + B, k)
    if kind == "each":
        good = tot - comb(R, k) - comb(B, k)
        p = f"A bag holds ${R}$ red marbles and ${B}$ blue marbles. ${k}$ marbles are drawn at random without replacement. What is the probability that both colors are drawn?"
        steps = [f"All ways to choose ${k}$ marbles: $\\binom{{{R + B}}}{{{k}}} = {tot}$.",
                 f"One color only: all red $\\binom{{{R}}}{{{k}}} = {comb(R, k)}$, all blue $\\binom{{{B}}}{{{k}}} = {comb(B, k)}$.",
                 f"Both colors: ${tot} - {comb(R, k)} - {comb(B, k)} = {good}$."]
        need = "the chance the draw is not all one color"
        trap = "computing the chance of one specific mix only, like exactly one red."
    else:
        j = r.randint(1, k - 1)
        good = comb(R, j) * comb(B, k - j)
        p = f"A bag holds ${R}$ red marbles and ${B}$ blue marbles. ${k}$ marbles are drawn at random without replacement. What is the probability that exactly ${j}$ are red?"
        steps = [f"All ways to choose ${k}$ marbles: $\\binom{{{R + B}}}{{{k}}} = {tot}$.",
                 f"Choose ${j}$ of the ${R}$ red ones and ${k - j}$ of the ${B}$ blue ones: $\\binom{{{R}}}{{{j}}}\\binom{{{B}}}{{{k - j}}} = {comb(R, j)} \\cdot {comb(B, k - j)} = {good}$."]
        need = f"the chance exactly ${j}$ of the ${k}$ marbles are red"
        trap = "using the probabilities with replacement, $\\left(\\frac{R}{R + B}\\right)^j$, which ignores that the bag changes after each draw."
    pr = F(good, tot)
    steps.append(f"Probability $= \\frac{{{good}}}{{{tot}}} = {num(pr).tex}$.")
    sol = explain(need + ".", "every set of marbles is equally likely, so count favorable sets and divide by all sets, using combinations.", steps, f"${num(pr).tex}$.", trap)
    return (p, pr, [1 - pr, pr + F(1, tot), F(R, R + B), F(1, 2) if pr != F(1, 2) else F(1, 3), pr / 2], ["Count with combinations."], sol)


# ============================================================ LEVEL 5 (AMC 10 #21 to 25, AMC 12 #16 to 20)


@family("l5_alg_func_eq", 5, "algebra", "alg_functions")
def _(r):
    a = r.choice([2, 3, -2, 4])
    p1, p0 = r.randint(-5, 5), r.randint(-9, 9)
    kind = r.choice(["oneminus", "recip"])
    k = r.choice([2, 3, 4, 5, -1, -2])
    g = lambda x: p1 * x + p0
    rhs = (f"{p1 if p1 not in (1, -1) else ('' if p1 == 1 else '-')}x{' + ' if p0 >= 0 else ' - '}{abs(p0)}") if p1 else str(p0)
    sign = " + " if a > 0 else " - "
    if kind == "oneminus":
        x, y = F(k), 1 - F(k)
        inner_t, partner = "1 - x", f"1 - ({k})"
        p = f"A function $f$ satisfies $f(x){sign}{abs(a)}f(1 - x) = {rhs}$ for all real $x$. What is $f({k})$?"
    else:
        if k in (0, 1, -1):
            k = 2
        x, y = F(k), 1 / F(k)
        inner_t, partner = "\\frac{1}{x}", f"\\frac{{1}}{{{k}}}"
        p = f"A function $f$ satisfies $f(x){sign}{abs(a)}f\\left(\\dfrac{{1}}{{x}}\\right) = {rhs}$ for all $x \\ne 0$. What is $f({k})$?"
    gx, gy = g(x), g(y)
    fx = (gx - a * gy) / (1 - a * a)
    fy = gy - a * fx
    A_, B_ = f"f({num(x).tex})", f"f\\left({num(y).tex}\\right)"
    sol = explain(
        f"the single value $f({k})$. We do not know a formula for $f$.",
        f"plugging in one $x$ gives an equation with two unknowns. Plugging in the partner value (the one that swaps $x$ and ${inner_t}$) gives a second equation, and two equations solve for two unknowns.",
        [
            f"Plug in $x = {k}$: $$ {A_}{sign}{abs(a)}{B_} = {num(gx).tex}. $$",
            f"Plug in $x = {num(y).tex}$ (because ${partner} = {num(y).tex}$ swaps the roles): $$ {B_}{sign}{abs(a)}{A_} = {num(gy).tex}. $$",
            f"Call $P = {A_}$ and $Q = {B_}$. The system is $P {sign.strip()} {abs(a)}Q = {num(gx).tex}$ and $Q {sign.strip()} {abs(a)}P = {num(gy).tex}$. From the second, $Q = {num(gy).tex} {'-' if a > 0 else '+'} {abs(a)}P$.",
            f"Substitute into the first: $P {sign.strip()} {abs(a)}({num(gy).tex} {'-' if a > 0 else '+'} {abs(a)}P) = {num(gx).tex}$, so $(1 - {a * a})P = {num(gx).tex} - ({num(a * gy).tex})$ and $P = {num(fx).tex}$.",
            f"Check: $Q = {num(fy).tex}$, and ${num(fx).tex}{sign}{abs(a)}({num(fy).tex}) = {num(fx + a * fy).tex}$.",
        ],
        f"$f({k}) = {num(fx).tex}$.",
        f"plugging $x = {k}$ into the right side and stopping (that gives ${num(gx).tex}$). The left side has two unknowns, so one equation is not enough.",
    )
    return (p, fx, [gx, gx / (1 + a), -fx if fx else 1, fx + 1, (gx + a * gy) / (1 + a * a)], ["Substitute so that $f$ of the two related inputs appears twice, then solve the system."], sol)


@family("l5_alg_diff_squares_pairs", 5, "algebra", "alg_factoring")
def _(r):
    N = r.choice([24, 45, 48, 60, 72, 96, 105, 120, 135, 144, 180, 210])
    kind = r.choice(["pos", "all"])
    pairs = [(d, N // d) for d in range(1, N + 1) if N % d == 0 and d <= N // d and (d + N // d) % 2 == 0]
    sols = [(x, y) for x in range(-N, N + 1) for y in range(-N, N + 1) if x * x - y * y == N]
    if kind == "pos":
        sols = [s for s in sols if s[0] > 0 and s[1] > 0]
        p = f"How many ordered pairs of positive integers $(x, y)$ satisfy $x^2 - y^2 = {N}$?"
    else:
        p = f"How many ordered pairs of integers $(x, y)$ satisfy $x^2 - y^2 = {N}$?"
    ans = len(sols)
    lines = ", ".join(f"$({a_}, {b_}) \\to (x, y) = ({(a_ + b_) // 2}, {(b_ - a_) // 2})$" for a_, b_ in pairs)
    steps = [
        f"Factor: $(x - y)(x + y) = {N}$. Call $a = x - y$ and $b = x + y$, so $x = \\frac{{a + b}}{{2}}$ and $y = \\frac{{b - a}}{{2}}$.",
        f"For $x$ and $y$ to be integers, $a$ and $b$ must have the same parity (both even or both odd).",
        f"Positive factor pairs $a \\le b$ of ${N}$ with the same parity: {lines}.",
    ]
    if kind == "pos":
        steps.append(f"For positive $y$ we need $a < b$ strictly. That leaves ${ans}$ pairs.")
        trap = "including pairs with $a = b$, which give $y = 0$, or pairs of opposite parity, which give fractions."
    else:
        steps.append(f"Each solution with $x, y \\ne 0$ comes in four sign versions $(\\pm x, \\pm y)$; solutions with $y = 0$ come in two. Counting all of them gives ${ans}$.")
        trap = "counting only positive solutions. With integers allowed, signs multiply the count."
    sol = explain(f"the number of {'positive ' if kind == 'pos' else ''}integer pairs with $x^2 - y^2 = {N}$.", "a difference of squares factors, so solutions match factor pairs of the number.", steps, f"${ans}$.", trap)
    return (p, ans, [ans * 2 if kind == "pos" else ans // 2, ans + 1, ans - 1 if ans > 1 else ans + 2, ans + 2, ans + 4], ["Factor: $(x - y)(x + y) = N$. Both factors have the same parity."], sol)


@family("l5_alg_floor_sqrt", 5, "algebra", "alg_sequences")
def _(r):
    m = r.randint(6, 15)
    N = m * m + r.randint(-m, m)
    S = sum(math.isqrt(k) for k in range(1, N + 1))
    top = math.isqrt(N)
    full = sum(j * (2 * j + 1) for j in range(1, top))
    last = top * (N - top * top + 1)
    assert full + last == S
    p = f"What is $\\lfloor\\sqrt{{1}}\\rfloor + \\lfloor\\sqrt{{2}}\\rfloor + \\lfloor\\sqrt{{3}}\\rfloor + \\cdots + \\lfloor\\sqrt{{{N}}}\\rfloor$?"
    sol = explain(
        f"the sum of ${N}$ floor values. Adding them one by one is slow; group equal terms.",
        "$\\lfloor\\sqrt{k}\\rfloor = j$ exactly when $j^2 \\le k < (j + 1)^2$. That range has $2j + 1$ numbers.",
        [
            "Value $1$ for $k = 1$ to $3$ ($3$ terms), value $2$ for $k = 4$ to $8$ ($5$ terms), value $3$ for $k = 9$ to $15$ ($7$ terms), and so on.",
            f"Full groups $j = 1$ to ${top - 1}$ contribute $\\sum j(2j + 1) = {full}$.",
            f"The last group has value ${top}$, from $k = {top * top}$ to ${N}$: that is ${N - top * top + 1}$ terms, contributing ${top} \\cdot {N - top * top + 1} = {last}$.",
            f"Total: ${full} + {last} = {S}$.",
        ],
        f"${S}$.",
        "assuming the last group is complete. Check exactly where the sum stops.",
    )
    return (p, S, [S + 1, S - top, S + top, N * top // 2 + N, S - 1], ["$\\lfloor\\sqrt{k}\\rfloor = j$ for $j^2 \\le k \\le j^2 + 2j$, which is $2j + 1$ values."], sol)


@family("l5_geo_rect_diag", 5, "geometry", "geo_coordinate")
def _(r):
    a, b = r.randint(4, 12), r.randint(3, 10)
    x = r.randint(1, a - 1)
    t = F(a, x + a)
    Fy = t * b
    h = b - Fy
    area = F(x) * h / 2
    p = f"Rectangle $ABCD$ has $AB = {a}$ and $BC = {b}$. Point $E$ lies on side $CD$ with $DE = {x}$. Segment $AE$ meets diagonal $BD$ at $F$. What is the area of triangle $DEF$?"
    sol = explain(
        "the area of the small triangle $DEF$ near side $CD$.",
        "$DE$ and $AB$ are parallel, so triangles $DEF$ and $BAF$ are similar (they form an hourglass through $F$).",
        [
            f"The similarity ratio is $\\frac{{DE}}{{AB}} = \\frac{{{x}}}{{{a}}}$. So $F$ splits every segment through it in the ratio ${x} : {a}$.",
            f"The heights of the two triangles (from $F$ to $CD$ and from $F$ to $AB$) are in the ratio ${x} : {a}$ and add to $BC = {b}$.",
            f"Height of triangle $DEF$: ${b} \\cdot \\frac{{{x}}}{{{x + a}}} = {num(h).tex}$.",
            f"Area $= \\frac{{1}}{{2}} \\cdot DE \\cdot \\text{{height}} = \\frac{{1}}{{2}} \\cdot {x} \\cdot {num(h).tex} = {num(area).tex}$.",
        ],
        f"${num(area).tex}$.",
        f"assuming $F$ is at the middle of the rectangle. It is closer to the shorter parallel side $DE$.",
    )
    return (p, area, [F(x * b, 2), area * 2, F(x * b, 4), area + 1, F(a * b, 2) - area], ["Triangles $DEF$ and $BAF$ are similar."], sol)


@family("l5_geo_incircle_tangent", 5, "geometry", "geo_right")
def _(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 35, 37), (9, 40, 41)])
    k = r.randint(1, 3)
    a, b, c = a * k, b * k, c * k
    s = (a + b + c) // 2
    ask = r.choice(["prod", "r"])
    rr = s - c
    if ask == "prod":
        ans = (s - a) * (s - b)
        p = f"The incircle of a right triangle with legs ${a}$ and ${b}$ touches the hypotenuse at $D$, splitting it into segments of lengths $m$ and $n$. What is $mn$?"
        steps = [
            f"The hypotenuse is $\\sqrt{{{a}^2 + {b}^2}} = {c}$, and the semiperimeter is $s = \\frac{{{a} + {b} + {c}}}{{2}} = {s}$.",
            "Tangent segments from one vertex to the incircle are equal. The tangent length from a vertex is $s$ minus the opposite side.",
            f"The two pieces of the hypotenuse are the tangent lengths from the two acute vertices: $s - {a} = {s - a}$ and $s - {b} = {s - b}$.",
            f"Product: ${s - a} \\cdot {s - b} = {ans}$. (Nice fact: this always equals the area of a right triangle, $\\frac{{{a} \\cdot {b}}}{{2}} = {a * b // 2}$.)",
        ]
        trap = "assuming the incircle touches the hypotenuse at its midpoint."
        wrong = [c * c // 4, a * b, ans + c, (s - a) + (s - b), ans - k]
    else:
        ans = rr
        p = f"A circle is tangent to both legs and the hypotenuse of a right triangle with legs ${a}$ and ${b}$. What is its radius?"
        steps = [
            f"Hypotenuse: $\\sqrt{{{a}^2 + {b}^2}} = {c}$.",
            "At the right angle, the two radii to the legs and the legs themselves form a small square of side $r$. So the tangent length from the right angle vertex is $r$.",
            f"Tangent lengths from the other two vertices are ${a} - r$ and ${b} - r$, and together they make the hypotenuse: $({a} - r) + ({b} - r) = {c}$.",
            f"Solve: $2r = {a} + {b} - {c} = {a + b - c}$, so $r = {ans}$.",
        ]
        trap = f"using half the hypotenuse, ${num(F(c, 2)).tex}$. That is the radius of the circle through the vertices, not the circle inside."
        wrong = [F(c, 2), F(a * b, a + b + c) * 2, ans + 1, ans - 1, F(a * b, c)]
    sol = explain("a length related to the incircle of a right triangle.", "tangent segments from the same point to a circle are equal. Label every tangent length.", steps, f"${num(F(ans)).tex}$.", trap)
    return (p, ans, wrong, ["Tangent segments from the same point are equal."], sol)


@family("l5_geo_sphere_in_cone", 5, "geometry", "geo_solids")
def _(r):
    R, H, L = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15), (20, 21, 29)])
    k = r.randint(1, 3)
    R, H, L = R * k, H * k, L * k
    rad = F(R * H, R + L)
    p = f"A sphere sits inside a right circular cone and touches the base and the curved surface all the way around. The cone has base radius ${R}$ and height ${H}$. What is the radius of the sphere?"
    sol = explain(
        "the radius of the sphere that fits snugly in the cone.",
        "slice the cone straight down through its tip. The cone becomes an isosceles triangle and the sphere becomes the circle inscribed in it.",
        [
            f"The cross section is a triangle with base ${2 * R}$ and height ${H}$. Each slanted side is $\\sqrt{{{R}^2 + {H}^2}} = {L}$.",
            f"Its area is $\\frac{{1}}{{2}} \\cdot {2 * R} \\cdot {H} = {R * H}$, and its semiperimeter is $\\frac{{{L} + {L} + {2 * R}}}{{2}} = {L + R}$.",
            f"Inradius $= \\frac{{\\text{{Area}}}}{{s}} = \\frac{{{R * H}}}{{{R + L}}} = {num(rad).tex}$.",
        ],
        f"${num(rad).tex}$.",
        "using the full perimeter instead of the semiperimeter, or forgetting that the triangle's base is the cone's diameter, not its radius.",
    )
    return (p, rad, [F(R, 2), F(H, 3), F(R * H, L), rad + 1, F(R * H, R + H)], ["Take a cross section through the axis: the sphere becomes the incircle of an isosceles triangle."], sol)


@family("l5_nt_lcm_pairs", 5, "number_theory", "nt_gcd")
def _(r):
    N = r.choice([12, 18, 20, 24, 30, 36, 40, 45, 48, 60, 72, 84, 90, 100, 108, 120, 144, 180])
    kind = r.choice(["ordered", "unordered"])
    divs = [d for d in range(1, N + 1) if N % d == 0]
    ordered = [(a, b) for a in divs for b in divs if math.lcm(a, b) == N]
    fac, m, pp = [], N, 2
    while m > 1:
        e = 0
        while m % pp == 0:
            m //= pp
            e += 1
        if e:
            fac.append((pp, e))
        pp += 1
    prod_ = 1
    for _, e in fac:
        prod_ *= 2 * e + 1
    assert prod_ == len(ordered)
    if kind == "unordered":
        ans = (prod_ + 1) // 2
        p = f"How many unordered pairs $\\{{a, b\\}}$ of positive integers (with $a \\le b$) have $\\operatorname{{lcm}}(a, b) = {N}$?"
    else:
        ans = prod_
        p = f"How many ordered pairs $(a, b)$ of positive integers have $\\operatorname{{lcm}}(a, b) = {N}$?"
    fact = " \\cdot ".join(f"{q}^{{{e}}}" for q, e in fac)
    steps = [
        f"Factor: ${N} = {fact}$.",
        "Work one prime at a time. If the prime's power in $N$ is $p^e$, the exponents of $p$ in $a$ and $b$ are between $0$ and $e$, and at least one of them must equal $e$ (that is what lcm means).",
        "Count those exponent pairs: $(e + 1)^2$ pairs in all, minus $e^2$ pairs where both are below $e$, which leaves $2e + 1$.",
        "Multiply over the primes: $" + " \\cdot ".join(f"(2 \\cdot {e} + 1)" for _, e in fac) + f" = {prod_}$ ordered pairs.",
    ]
    if kind == "unordered":
        steps.append(f"Only $(N, N)$ has $a = b$. The other ${prod_ - 1}$ ordered pairs come in swapped twins, so unordered pairs number $\\frac{{{prod_} - 1}}{{2}} + 1 = {ans}$.")
    sol = explain(f"the number of {'unordered' if kind == 'unordered' else 'ordered'} pairs with lcm ${N}$.", "lcm takes the larger exponent of each prime, so count exponent choices prime by prime.", steps, f"${ans}$.",
                  "forgetting that at least one exponent must reach the full power, or halving the ordered count without adding back the pair $(N, N)$.")
    return (p, ans, [len(divs) ** 2, len(divs), ans + 1, ans - 1, ans * 2 if kind == "unordered" else (ans + 1) // 2], ["Work one prime at a time: at least one of $a$, $b$ uses the full power."], sol)


@family("l5_nt_poly_divis", 5, "number_theory", "nt_modular")
def _(r):
    N = r.randint(50, 300)
    form, f, m = r.choice([("n^2 + n", lambda n: n * n + n, r.choice([6, 10, 12, 14])), ("n^3 - n", lambda n: n ** 3 - n, r.choice([10, 14, 15, 21, 35])),
                           ("n^2 + 1", lambda n: n * n + 1, r.choice([5, 10, 13, 17])), ("n^2 - 1", lambda n: n * n - 1, r.choice([12, 15, 21, 24]))])
    cnt = sum(1 for n in range(1, N + 1) if f(n) % m == 0)
    res = sorted({n % m for n in range(m) if f(n) % m == 0})
    full = N // m
    leftover = N - full * m
    extra = sum(1 for x in res if 1 <= x <= leftover) if leftover else 0
    if 0 in res and leftover >= m:
        pass
    p = f"For how many integers $n$ with $1 \\le n \\le {N}$ is ${form}$ divisible by ${m}$?"
    sol = explain(
        f"how many $n$ up to ${N}$ make ${form}$ a multiple of ${m}$.",
        f"whether ${m}$ divides ${form}$ depends only on the remainder of $n$ when divided by ${m}$. Check the ${m}$ remainders once, then count.",
        [
            f"Test $n = 0, 1, \\ldots, {m - 1}$: ${form}$ is divisible by ${m}$ exactly for the remainders ${', '.join(map(str, res))}$. That is ${len(res)}$ of every ${m}$ consecutive numbers.",
            f"${N} = {m} \\cdot {full} + {leftover}$, so there are ${full}$ complete blocks of ${m}$, giving ${full} \\cdot {len(res)} = {full * len(res)}$ values.",
            f"The leftover numbers ${full * m + 1}$ to ${N}$ have remainders $1$ to ${leftover}$; ${extra}$ of those are good." if leftover else "There are no leftover numbers.",
            f"Total: ${full * len(res)} + {extra} = {cnt}$.",
        ],
        f"${cnt}$.",
        "forgetting to check the partial block at the end.",
    )
    assert full * len(res) + extra == cnt
    return (p, cnt, [N // m, cnt + 1, cnt - 1, N * len(res) // m + 2, N - cnt], [f"Look at $n$ modulo ${m}$: only certain remainders work."], sol)


@family("l5_nt_binary_ones", 5, "number_theory", "nt_bases")
def _(r):
    N = r.randint(40, 300)
    kind = r.choice(["more1", "exactly", "palin"])
    nb = len(bin(N)) - 2
    if kind == "more1":
        cnt = sum(1 for n in range(1, N + 1) if bin(n).count("1") > bin(n)[2:].count("0"))
        p = f"How many integers from $1$ to ${N}$ have more $1$s than $0$s when written in base $2$?"
        rule = "with $L$ binary digits, the first is $1$; choose positions for the other $1$s so they outnumber the $0$s"
    elif kind == "exactly":
        k = r.randint(2, 4)
        cnt = sum(1 for n in range(1, N + 1) if bin(n).count("1") == k)
        p = f"How many integers from $1$ to ${N}$ have exactly ${k}$ ones when written in base $2$?"
        rule = f"with $L$ binary digits, the first is $1$, so choose ${k - 1}$ of the other $L - 1$ places for the remaining ones: $\\binom{{L - 1}}{{{k - 1}}}$"
    else:
        cnt = sum(1 for n in range(1, N + 1) if bin(n)[2:] == bin(n)[2:][::-1])
        p = f"How many integers from $1$ to ${N}$ are palindromes when written in base $2$?"
        rule = "with $L$ binary digits, the first (and so the last) digit is $1$, and the first half determines the rest: $2^{\\lceil L/2 \\rceil - 1}$ palindromes"
    pow2 = 2 ** (nb - 1)
    below = sum(1 for n in range(1, pow2) if (kind == "more1" and bin(n).count("1") > bin(n)[2:].count("0")) or (kind == "exactly" and bin(n).count("1") == k) or (kind == "palin" and bin(n)[2:] == bin(n)[2:][::-1]))
    sol = explain(
        f"a count of numbers up to ${N}$ based on their binary digits.",
        "group the numbers by how many binary digits they have. Numbers with $L$ digits run from $2^{L-1}$ to $2^L - 1$.",
        [
            f"${N}$ in binary is ${bin(N)[2:]}_2$, which has ${nb}$ digits.",
            f"For each length $L$ from $1$ to ${nb - 1}$, every number of that length is at most ${N}$. Count: {rule}. Adding these lengths gives ${below}$.",
            f"Numbers with ${nb}$ digits only go up to ${N}$, so check $2^{{{nb - 1}}} = {pow2}$ through ${N}$ separately: ${cnt - below}$ more.",
            f"Total: ${below} + {cnt - below} = {cnt}$.",
        ],
        f"${cnt}$.",
        f"counting all ${nb}$ digit numbers up to $2^{{{nb}}} - 1$, past ${N}$.",
    )
    return (p, cnt, [cnt + 1, cnt - 1, cnt + 2, N // 2, cnt + 4], ["Group the numbers by how many binary digits they have."], sol)


@family("l5_cp_stars_bars", 5, "counting_probability", "cp_combinations")
def _(r):
    n, k = r.randint(8, 20), r.randint(3, 4)
    lo, hi = r.randint(0, 2), r.randint(4, 9)
    if hi >= n - (k - 1) * lo:
        return None
    cnt = sum(1 for t in product(range(lo, hi + 1), repeat=k) if sum(t) == n)
    if cnt < 3:
        return None
    m = n - k * lo
    cap = hi - lo
    free = comb(m + k - 1, k - 1)
    terms = []
    j = 0
    while j <= k and m - j * (cap + 1) >= 0:
        terms.append((j, comb(k, j), comb(m - j * (cap + 1) + k - 1, k - 1)))
        j += 1
    assert sum((-1) ** j * a * b for j, a, b in terms) == cnt
    p = f"In how many ways can ${n}$ identical candies be given to ${k}$ children so that each child gets at least ${lo}$ and at most ${hi}$ candies?"
    sol = explain(
        f"the number of ways to write ${n}$ as a sum of ${k}$ amounts, each between ${lo}$ and ${hi}$ (order matters, since the children are different).",
        "Stars and Bars counts ways to split identical items among people: $m$ items among $k$ people (any amount, including $0$) can be split in $\\binom{m + k - 1}{k - 1}$ ways. Handle the limits by giving out minimums first and subtracting cases that break the maximum.",
        [
            (f"Give each child ${lo}$ first. That uses ${k * lo}$, leaving ${m}$ candies, and now each child can get $0$ to ${cap}$ more." if lo else f"Each child can get $0$ to ${cap}$ candies, and we split all ${m}$."),
            f"Without the upper limit: $\\binom{{{m} + {k - 1}}}{{{k - 1}}} = {free}$ ways.",
            f"Remove the ways where some child gets more than ${cap}$ extra: give that child ${cap + 1}$ up front and split the rest freely. Inclusion and exclusion over how many children break the limit: $$" + " ".join(f"{'-' if j % 2 else '+'} \\binom{{{k}}}{{{j}}}\\binom{{{m - j * (cap + 1) + k - 1}}}{{{k - 1}}}" for j, _, _ in terms).lstrip("+ ") + f" = {cnt}.$$",
        ],
        f"${cnt}$ ways.",
        f"stopping at ${free}$ and ignoring the maximum of ${hi}$ per child.",
    )
    return (p, cnt, [free, cnt + k, comb(n - 1, k - 1), cnt - 1, cnt + 1], ["Give each child the minimum first, then use stars and bars with the upper limit removed by complementary counting."], sol)


@family("l5_cp_two_numbers", 5, "counting_probability", "cp_geometric")
def _(r):
    a = r.randint(2, 10)
    kind = r.choice(["close", "sum"])
    if kind == "close":
        d = F(r.randint(1, 2 * a - 1), 2)
        if d >= a:
            return None
        bad = (F(a) - d) ** 2
        pr = 1 - bad / (a * a)
        p = f"Two real numbers are chosen independently and uniformly at random from the interval $[0, {a}]$. What is the probability that they differ by less than ${num(d).tex}$?"
        steps = [f"Picture every possible pair $(x, y)$ as a point in the ${a} \\times {a}$ square, area ${a * a}$. Every point is equally likely, so probability $=$ (good area) $\\div$ {a * a}.".replace("$\\div$ " + str(a * a), f"${a * a}$"),
                 f"The bad region $|x - y| \\ge {num(d).tex}$ is two corner triangles, each a right isosceles triangle with legs ${a} - {num(d).tex} = {num(F(a) - d).tex}$.",
                 f"Together they have area $2 \\cdot \\frac{{1}}{{2}} \\cdot {num(F(a) - d).tex}^2 = {num(bad).tex}$.",
                 f"Probability $= 1 - \\frac{{{num(bad).tex}}}{{{a * a}}} = {num(pr).tex}$."]
        trap = f"answering $\\frac{{{num(d).tex}}}{{{a}}}$, which treats the problem as one dimensional."
    else:
        s = F(r.randint(1, 2 * a - 1))
        if s <= a:
            area = s * s / 2
            shape = f"the triangle under the line $x + y = {s}$, with legs ${s}$: area $\\frac{{{s}^2}}{{2}} = {num(area).tex}$"
        else:
            area = a * a - (2 * a - s) ** 2 / 2
            shape = f"the whole square minus the corner triangle above the line $x + y = {s}$, whose legs are ${2 * a} - {s} = {2 * a - s}$: area ${a * a} - \\frac{{{2 * a - s}^2}}{{2}} = {num(area).tex}$"
        pr = area / (a * a)
        p = f"Two real numbers are chosen independently and uniformly at random from the interval $[0, {a}]$. What is the probability that their sum is less than ${num(s).tex}$?"
        steps = [f"Picture every possible pair $(x, y)$ as a point in the ${a} \\times {a}$ square, area ${a * a}$.",
                 f"The good region $x + y < {num(s).tex}$ is {shape}.",
                 f"Probability $= \\frac{{{num(area).tex}}}{{{a * a}}} = {num(pr).tex}$."]
        trap = f"answering $\\frac{{{num(s).tex}}}{{{2 * a}}}$. The sum of two uniform numbers is not uniform."
    sol = explain("a probability about two random real numbers.", "with two random numbers, draw the square of all possible pairs. Probability becomes area.", steps, f"${num(pr).tex}$.", trap)
    return (p, pr, [1 - pr, pr * 2 if pr < F(1, 2) else pr / 2, F(1, 2) if pr != F(1, 2) else F(1, 3), pr + F(1, 8) if pr + F(1, 8) < 1 else pr - F(1, 8), F(3, 4) if pr != F(3, 4) else F(2, 3)],
            ["Draw the square of all possible pairs and shade the good region."], sol)


@family("l5_cp_tiling", 5, "counting_probability", "cp_casework")
def _(r):
    kind = r.choice(["stairs", "tiles", "nocons"])
    n = r.randint(7, 12)
    if kind == "stairs":
        f = [1, 1, 2]
        for i in range(3, n + 1):
            f.append(f[-1] + f[-2] + f[-3])
        ans = f[n]
        p = f"A staircase has ${n}$ steps. You climb it taking $1$, $2$, or $3$ steps at a time. In how many ways can you reach the top?"
        steps = ["Let $w_k$ be the number of ways to reach step $k$. Your last move onto step $k$ was a $1$, $2$ or $3$, so $$ w_k = w_{k-1} + w_{k-2} + w_{k-3}. $$",
                 "Start: $w_0 = 1$ (stand still), $w_1 = 1$, $w_2 = 2$.",
                 "Build up: " + ", ".join(f"$w_{{{i}}} = {f[i]}$" for i in range(3, n + 1)) + "."]
        trap = "trying to list sequences by hand, which misses cases. Build the table instead."
    elif kind == "tiles":
        f = [1, 1]
        for i in range(2, n + 1):
            f.append(f[-1] + f[-2])
        ans = f[n]
        p = f"In how many ways can a $2 \\times {n}$ rectangle be tiled with $1 \\times 2$ dominoes?"
        steps = ["Let $t_k$ be the tilings of a $2 \\times k$ strip. Look at the left end: either one vertical domino (leaving $2 \\times (k - 1)$) or two stacked horizontal dominoes (leaving $2 \\times (k - 2)$). So $t_k = t_{k-1} + t_{k-2}$.",
                 "Start: $t_1 = 1$, $t_2 = 2$.",
                 "Build up: " + ", ".join(f"$t_{{{i}}} = {f[i]}$" for i in range(3, n + 1)) + "."]
        trap = "allowing a single horizontal domino at the left end; it must be paired with another below it."
    else:
        a_ = [1, 2, 3]
        for i in range(3, n + 1):
            a_.append(a_[-1] + a_[-2])
        ans = a_[n]
        assert ans == sum(1 for bits in product([0, 1], repeat=n) if all(not (bits[i] and bits[i + 1]) for i in range(n - 1)))
        p = f"How many strings of ${n}$ characters, each $A$ or $B$, have no two $B$s next to each other?"
        steps = ["Let $a_k$ count good strings of length $k$. A good string either ends in $A$ (anything good before it) or ends in $AB$ (anything good before that). So $a_k = a_{k-1} + a_{k-2}$.",
                 "Start: $a_1 = 2$ ($A$, $B$) and $a_2 = 3$ ($AA$, $AB$, $BA$).",
                 "Build up: " + ", ".join(f"$a_{{{i}}} = {a_[i]}$" for i in range(3, n + 1)) + "."]
        trap = f"counting all $2^{{{n}}}$ strings and guessing a fraction. Use the recursion."
    sol = explain("a count that would be painful to list by hand.", "find a recursion: think about the first or last move, which reduces the problem to a smaller version of itself.", steps, f"${ans}$.", trap)
    return (p, ans, [ans + 1, ans - 1, 2 ** n // 2, ans * 2, ans + n], ["Think about what happens at the first (or last) move, and find a recursion."], sol)


# ============================================================ LEVEL 6 (AMC 12 #21 to 25)


@family("l6_alg_power_one", 6, "algebra", "alg_quadratics")
def _(r):
    def roots(A, B, Cc):
        disc = B * B - 4 * A * Cc
        if disc < 0:
            return []
        s = math.isqrt(disc)
        if s * s != disc:
            return None
        return sorted({F(-B + s, 2 * A), F(-B - s, 2 * A)})
    while True:
        a, b = r.randint(-9, 9), r.randint(-12, 12)
        c, d = r.randint(-9, 9), r.randint(-12, 12)
        base = lambda x: x * x - a * x + b
        ex = lambda x: x * x - c * x + d
        r1, r2, r3 = roots(1, -a, b - 1), roots(1, -c, d), roots(1, -a, b + 1)
        if r1 is None or r2 is None or r3 is None:
            continue
        case1 = list(r1)
        case2 = [x for x in r2 if base(x) != 0]
        case2_bad = [x for x in r2 if base(x) == 0]
        case3 = [x for x in r3 if ex(x).denominator == 1 and ex(x).numerator % 2 == 0]
        case3_bad = [x for x in r3 if x not in case3]
        sols = set(case1) | set(case2) | set(case3)
        if len(sols) >= 3:
            break
    ans = sum(sols)
    B_ = f"x^2{' - ' if a >= 0 else ' + '}{abs(a)}x{' + ' if b >= 0 else ' - '}{abs(b)}"
    E_ = f"x^2{' - ' if c >= 0 else ' + '}{abs(c)}x{' + ' if d >= 0 else ' - '}{abs(d)}"
    fmt = lambda xs: ", ".join(f"${num(x).tex}$" for x in xs) if xs else "none"
    p = f"What is the sum of all real numbers $x$ for which $\\left({B_}\\right)^{{{E_}}} = 1$?"
    sol = explain(
        "every real $x$ that makes this power equal $1$, then their sum.",
        "a real power $b^e$ equals $1$ in exactly three ways: the base is $1$; the exponent is $0$ (and the base is not $0$); or the base is $-1$ and the exponent is an even integer.",
        [
            f"Base $= 1$: ${B_} = 1$. Solutions: {fmt(case1)}.",
            f"Exponent $= 0$: ${E_} = 0$. Solutions: {fmt(r2)}." + (f" Throw out {fmt(case2_bad)}, where the base is $0$ ($0^0$ is undefined)." if case2_bad else " The base is not $0$ at any of them, so all count."),
            f"Base $= -1$: ${B_} = -1$. Solutions: {fmt(r3)}." + (f" Keep only those where the exponent is an even integer: {fmt(case3)}." if r3 else "") + (f" ({fmt(case3_bad)} fail{'s' if len(case3_bad) == 1 else ''} because $(-1)^{{\\text{{odd}}}} = -1$.)" if case3_bad else ""),
            f"All distinct solutions: {fmt(sorted(sols))}. Their sum is ${num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "forgetting the base $-1$ case, or adding Vieta sums of the quadratics without checking which roots actually work.",
    )
    naive = F(a) + F(c)
    return (p, ans, [naive, ans + a, ans - c if ans - c != naive else ans + 1, F(a), F(c) if F(c) != ans else ans + 2],
            ["Three ways to get $1$: the base is $1$; the exponent is $0$ and the base is not $0$; the base is $-1$ and the exponent is an even integer."], sol)


@family("l6_alg_egyptian", 6, "algebra", "alg_factoring")
def _(r):
    k = r.choice([6, 8, 10, 12, 15, 18, 20, 24, 30, 36, 60])
    kind = r.choice(["ordered", "unordered"])
    sols = [(m, k * m // (m - k)) for m in range(k + 1, k * k + k + 1) if (k * m) % (m - k) == 0]
    dk2 = sum(1 for d in range(1, k * k + 1) if (k * k) % d == 0)
    assert dk2 == len(sols)
    if kind == "unordered":
        sols = [s for s in sols if s[0] <= s[1]]
        p = f"How many pairs of positive integers $(m, n)$ with $m \\le n$ satisfy $\\dfrac{{1}}{{m}} + \\dfrac{{1}}{{n}} = \\dfrac{{1}}{{{k}}}$?"
    else:
        p = f"How many ordered pairs of positive integers $(m, n)$ satisfy $\\dfrac{{1}}{{m}} + \\dfrac{{1}}{{n}} = \\dfrac{{1}}{{{k}}}$?"
    ans = len(sols)
    dk = sum(1 for d in range(1, k + 1) if k % d == 0)
    steps = [
        f"Multiply both sides by ${k}mn$: ${k}n + {k}m = mn$, so $mn - {k}m - {k}n = 0$.",
        f"Add ${k * k}$ to both sides to factor (Simon's Favorite Factoring Trick): $$ (m - {k})(n - {k}) = {k * k}. $$",
        f"Both $m$ and $n$ must exceed ${k}$ (since $\\frac{{1}}{{m}} < \\frac{{1}}{{{k}}}$), so $m - {k}$ and $n - {k}$ are positive divisor pairs of ${k * k}$.",
        f"${k * k}$ has ${dk2}$ positive divisors, and each gives one ordered pair.",
    ]
    if kind == "unordered":
        steps.append(f"Swapping $m$ and $n$ pairs them up, except the one with $m = n = {2 * k}$. So there are $\\frac{{{dk2} - 1}}{{2}} + 1 = {ans}$ pairs with $m \\le n$.")
    sol = explain("the number of ways to write $\\frac{1}{" + str(k) + "}$ as a sum of two unit fractions.", "clear denominators, then factor by adding a constant to both sides.", steps, f"${ans}$.",
                  f"counting divisors of ${k}$ (${dk}$) instead of ${k}^2$.")
    return (p, ans, [dk, ans + 1, ans - 1, ans * 2 if kind == "unordered" else (ans + 1) // 2, dk * 2], ["Clear denominators and use Simon's Favorite Factoring Trick."], sol)


@family("l6_geo_british_flag", 6, "geometry", "geo_right")
def _(r):
    while True:
        w, h = r.randint(6, 16), r.randint(6, 16)
        px, py = r.randint(1, w - 1), r.randint(1, h - 1)
        A2 = px * px + py * py
        B2 = (w - px) ** 2 + py * py
        C2 = (w - px) ** 2 + (h - py) ** 2
        D2 = px * px + (h - py) ** 2
        ints = [math.isqrt(v) ** 2 == v for v in (A2, B2, C2)]
        if sum(ints) >= 2 and D2 not in (A2, B2, C2):
            break
    fmt = lambda v: str(math.isqrt(v)) if math.isqrt(v) ** 2 == v else f"\\sqrt{{{v}}}"
    ans = surd(1, D2)
    p = f"Point $P$ lies inside rectangle $ABCD$ (vertices in order) with $PA = {fmt(A2)}$, $PB = {fmt(B2)}$, and $PC = {fmt(C2)}$. What is $PD$?"
    sol = explain(
        "the fourth distance $PD$, given the other three. There is not enough information to find the rectangle itself, so look for a relation between the four distances.",
        "drop perpendiculars from $P$ to all four sides. Each corner distance becomes the hypotenuse of a right triangle whose legs are two of those perpendiculars.",
        [
            "Call the distances from $P$ to the four sides $w$ (to $AD$), $x$ (to $AB$), $y$ (to $BC$), and $z$ (to $CD$).",
            "Then $PA^2 = w^2 + x^2$, $PB^2 = x^2 + y^2$, $PC^2 = y^2 + z^2$, and $PD^2 = z^2 + w^2$.",
            "So $PA^2 + PC^2 = w^2 + x^2 + y^2 + z^2 = PB^2 + PD^2$. This is the British Flag Theorem.",
            f"Plug in: $PD^2 = PA^2 + PC^2 - PB^2 = {A2} + {C2} - {B2} = {D2}$.",
            f"$PD = {ans.tex}$.",
        ],
        f"$PD = {ans.tex}$.",
        "pairing the wrong corners. The two sums use opposite corners: $A$ with $C$, and $B$ with $D$.",
    )
    return (p, ans, [surd(1, A2 + B2 - C2) if A2 + B2 - C2 > 0 else num(1), surd(1, B2 + C2 - A2) if B2 + C2 - A2 > 0 else num(2), surd(1, D2 + 2), surd(1, abs(A2 - B2) + C2 + 1), surd(1, max(D2 - 3, 1))],
            ["Drop perpendiculars from $P$ to all four sides and write each squared distance as a sum of two squares."], sol)


@family("l6_geo_corner_tetra", 6, "geometry", "geo_solids")
def _(r):
    a, b, c = r.choice([(2, 3, 6), (1, 2, 2), (3, 6, 6), (2, 4, 4), (4, 4, 2), (6, 3, 2), (2, 2, 1), (4, 12, 6), (12, 4, 3)])
    k = r.randint(1, 2)
    a, b, c = a * k, b * k, c * k
    inv = F(1, a * a) + F(1, b * b) + F(1, c * c)
    dist2 = 1 / inv
    if dist2.denominator == 1 and math.isqrt(int(dist2)) ** 2 == int(dist2):
        ans = num(math.isqrt(int(dist2)))
    else:
        ans = surd(F(1, dist2.denominator), dist2.numerator * dist2.denominator)
    assert abs(ans.key - float(dist2) ** 0.5) < 1e-9
    V = F(a * b * c, 6)
    area2 = F(a * a * b * b + b * b * c * c + c * c * a * a, 4)
    p = f"Three edges of a tetrahedron meet at vertex $O$ at right angles to one another and have lengths ${a}$, ${b}$, and ${c}$. What is the distance from $O$ to the plane through the other three vertices?"
    sol = explain(
        "the height $h$ of the tetrahedron measured from $O$ to the opposite face.",
        "compute the volume two ways. Using the right angle corner as the base is easy; using the far face as the base brings in $h$.",
        [
            f"Put $O$ at the origin with the edges along the axes: the other vertices are $({a}, 0, 0)$, $(0, {b}, 0)$, $(0, 0, {c})$.",
            f"Volume from the corner: $V = \\frac{{1}}{{3}} \\cdot \\frac{{{a} \\cdot {b}}}{{2}} \\cdot {c} = {num(V).tex}$.",
            f"Area of the far face: its square equals the sum of the squares of its three shadows on the coordinate planes, $$ \\left(\\tfrac{{{a * b}}}{{2}}\\right)^2 + \\left(\\tfrac{{{b * c}}}{{2}}\\right)^2 + \\left(\\tfrac{{{c * a}}}{{2}}\\right)^2 = {num(area2).tex}. $$",
            f"Volume from the far face: $V = \\frac{{1}}{{3}} \\cdot \\text{{Area}} \\cdot h$, so $h = \\frac{{3V}}{{\\text{{Area}}}}$. This simplifies to $\\frac{{1}}{{h^2}} = \\frac{{1}}{{{a}^2}} + \\frac{{1}}{{{b}^2}} + \\frac{{1}}{{{c}^2}} = {num(inv).tex}$.",
            f"So $h^2 = {num(dist2).tex}$ and $h = {ans.tex}$.",
        ],
        f"${ans.tex}$.",
        "using the average edge or the shortest edge as the height. The height is shorter than all three edges.",
    )
    return (p, ans, [num(F(a * b * c, a + b + c)), num(F(a + b + c, 3)), surd(1, a * a + b * b + c * c), num(min(a, b, c)), num(F(a * b * c, a * b + b * c + c * a))],
            ["Compute the volume two ways: from $O$'s corner, and as $\\frac{1}{3} \\cdot$ (area of the far face) $\\cdot$ (height)."], sol)


@family("l6_nt_square_product", 6, "number_theory", "nt_divisors")
def _(r):
    k = r.choice([4, 6, 8, 10, 12, 14, 15, 16, 20, 21, 24, 28, 30])
    sols = [n for n in range(1, k * k) if math.isqrt(n * (n + k)) ** 2 == n * (n + k)]
    if not sols:
        return None
    ask = r.choice(["sum", "count"])
    ans = sum(sols) if ask == "sum" else len(sols)
    K = k * k
    pairs = [(u, K // u) for u in range(1, k) if K % u == 0 and (u + K // u) % 2 == 0]
    p = f"What is the {'sum' if ask == 'sum' else 'number'} of all positive integers $n$ for which $n(n + {k})$ is a perfect square?"
    sol = explain(
        f"all $n > 0$ with $n^2 + {k}n = m^2$ for some integer $m$.",
        "complete the square, then factor as a difference of squares.",
        [
            f"Multiply by $4$ and complete the square: $4n^2 + {4 * k}n = 4m^2$ becomes $(2n + {k})^2 - (2m)^2 = {K}$.",
            f"Factor: $(2n + {k} - 2m)(2n + {k} + 2m) = {K}$. Call the factors $u < v$; they have the same parity and $u \\cdot v = {K}$.",
            "From $u + v = 2(2n + " + str(k) + ")$ we get $n = \\frac{u + v}{4} - \\frac{" + str(k) + "}{2}$. Try each factor pair: " + ", ".join(f"$({u_}, {v_}) \\to n = {num(F(u_ + v_, 4) - F(k, 2)).tex}$" for u_, v_ in pairs) + ".",
            f"Keep the positive integers: $n = {', '.join(map(str, sols))}$." + (f" Their sum is ${ans}$." if ask == "sum" else f" That is ${ans}$ values."),
        ],
        f"${ans}$.",
        "forgetting that both factors must have the same parity, or keeping $n = 0$ or fractions.",
    )
    return (p, ans, [ans + k, ans - sols[0] if len(sols) > 1 else ans + 1, ans * 2, ans + 1, max(sols) if max(sols) != ans else ans + 3], ["Complete the square, then factor as a difference of squares."], sol)


@family("l6_nt_tower_digits", 6, "number_theory", "nt_powers")
def _(r):
    a = r.choice([3, 7, 13, 17, 19, 23])
    b, c = r.randint(2, 9), r.randint(2, 6)
    E = b ** c
    order = next(k for k in range(1, 101) if pow(a, k, 100) == 1)
    ans = pow(a, E, 100)
    p = f"What are the last two digits of ${a}^{{{b}^{{{c}}}}}$? Give the answer as a number from $0$ to $99$."
    sol = explain(
        f"${a}^{{{E}}} \\bmod 100$.",
        f"since ${a}$ shares no factor with $100$, its powers mod $100$ repeat. Find the period, then reduce the exponent.",
        [
            f"The exponent is ${b}^{{{c}}} = {E}$.",
            f"Compute powers of ${a}$ mod $100$ until you get $1$: the first is ${a}^{{{order}}} \\equiv 1 \\pmod{{100}}$. So the period is ${order}$.",
            f"Reduce the exponent: ${E} = {order} \\cdot {E // order} + {E % order}$, so ${a}^{{{E}}} \\equiv {a}^{{{E % order}}} \\pmod{{100}}$.",
            f"${a}^{{{E % order}}} \\bmod 100 = {ans}$.",
        ],
        f"the last two digits are ${ans:02d}$.",
        f"reducing the exponent mod $10$ or mod $4$ instead of the real period ${order}$.",
    )
    return (p, ans, [pow(a, b * c, 100), pow(a, E % 20 + 1, 100), (ans + 20) % 100, (ans + 40) % 100, pow(a, c ** b, 100) if pow(a, c ** b, 100) != ans else (ans + 60) % 100],
            ["Powers of a number coprime to $100$ repeat with period dividing $20$. Reduce the exponent modulo the period first."], sol)


@family("l6_cp_lattice_triangles", 6, "counting_probability", "cp_casework")
def _(r):
    m, n = r.choice([(2, 2), (2, 3), (3, 3), (2, 4), (3, 4)])
    pts = [(x, y) for x in range(m + 1) for y in range(n + 1)]
    cnt = sum(1 for p1, p2, p3 in combinations(pts, 3) if (p2[0] - p1[0]) * (p3[1] - p1[1]) != (p3[0] - p1[0]) * (p2[1] - p1[1]))
    total = comb(len(pts), 3)
    rows = (n + 1) * comb(m + 1, 3)
    cols = (m + 1) * comb(n + 1, 3)
    slants = total - cnt - rows - cols
    p = f"How many triangles with positive area have all three vertices among the ${len(pts)}$ points $(x, y)$ with $x \\in \\{{0, 1, \\ldots, {m}\\}}$ and $y \\in \\{{0, 1, \\ldots, {n}\\}}$?"
    sol = explain(
        "the number of triples of grid points that are not on a straight line.",
        "count all triples, then subtract the collinear ones. Collinear triples lie on rows, columns, or slanted lines.",
        [
            f"All triples: $\\binom{{{len(pts)}}}{{3}} = {total}$.",
            f"Rows: ${n + 1}$ rows of ${m + 1}$ points give ${n + 1} \\cdot \\binom{{{m + 1}}}{{3}} = {rows}$.",
            f"Columns: ${m + 1}$ columns of ${n + 1}$ points give ${m + 1} \\cdot \\binom{{{n + 1}}}{{3}} = {cols}$.",
            f"Slanted lines (slopes like $\\pm 1$, $\\pm 2$, $\\pm\\frac{{1}}{{2}}$) with three or more grid points: ${slants}$ more collinear triples.",
            f"Triangles: ${total} - {rows} - {cols} - {slants} = {cnt}$.",
        ],
        f"${cnt}$.",
        "subtracting rows and columns but forgetting the diagonal and other slanted lines.",
    )
    return (p, cnt, [total, cnt + 4, cnt - 4, total - rows - cols, cnt + 8], ["Count all triples, then subtract the collinear ones: rows, columns, and every slanted line."], sol)


@family("l6_cp_reach_sum", 6, "counting_probability", "cp_probability")
def _(r):
    kind = r.choice(["coin12", "die_first"])
    if kind == "coin12":
        n = r.randint(5, 12)
        P = [F(1), F(1, 2)]
        for i in range(2, n + 1):
            P.append(F(1, 2) * P[-1] + F(1, 2) * P[-2])
        ans = P[n]
        p = f"A token starts at $0$ on a number line. Each turn a fair coin is flipped: heads moves it $1$ to the right, tails moves it $2$ to the right. What is the probability that the token ever lands exactly on ${n}$?"
        sol = explain(
            f"the chance the token stops on ${n}$ at some point, rather than jumping over it.",
            "let $p_k$ be the chance of ever landing on $k$. To land on $k$, the token must land on $k - 1$ and then flip heads, or land on $k - 2$ and then flip tails.",
            [
                "So $p_k = \\frac{1}{2}p_{k-1} + \\frac{1}{2}p_{k-2}$, with $p_0 = 1$ and $p_1 = \\frac{1}{2}$.",
                "Build the table: " + ", ".join(f"$p_{{{i}}} = {num(P[i]).tex}$" for i in range(2, n + 1)) + ".",
                "(The values approach $\\frac{2}{3}$, alternating above and below it.)",
            ],
            f"${num(ans).tex}$.",
            "using $\\frac{2}{3}$, which is only the long run value.",
        )
        wrong = [F(2, 3), F(1, 2), ans + F(1, 2 ** n), 1 - ans, F(3, 5)]
    else:
        n1, n2 = r.sample(NAMES, 2)
        k = r.choice([2, 3])
        a = F(1, 6)
        q_b = F(5, 6) ** k
        b = 1 - q_b
        pass_ = (1 - a) * q_b
        ans = a / (1 - pass_)
        p = (f"{n1} and {n2} take turns, {n1} first. On each turn {n1} rolls one fair die and wins with a $6$; {n2} rolls ${k}$ fair dice and wins if at least one shows a $6$. "
             f"What is the probability that {n1} wins?")
        sol = explain(
            f"the chance {n1} wins this back and forth game.",
            f"look at one full round ({n1} then {n2}). Either {n1} wins in the round, or {n2} wins, or nobody does and the game restarts.",
            [
                f"{n1} wins on a turn with probability $\\frac{{1}}{{6}}$.",
                f"{n2} misses only if all ${k}$ dice avoid $6$: $\\left(\\frac{{5}}{{6}}\\right)^{{{k}}} = {num(q_b).tex}$. So {n2} wins on a turn with probability $1 - {num(q_b).tex} = {num(b).tex}$.",
                f"A round passes with no winner with probability $\\frac{{5}}{{6}} \\cdot {num(q_b).tex} = {num(pass_).tex}$.",
                f"{n1} wins in round $1$, or round $2$, and so on: $$ \\frac{{1}}{{6}}\\left(1 + {num(pass_).tex} + {num(pass_).tex}^2 + \\cdots\\right) = \\frac{{\\frac{{1}}{{6}}}}{{1 - {num(pass_).tex}}} = {num(ans).tex}. $$",
            ],
            f"${num(ans).tex}$.",
            f"treating {n2}'s chance as ${k} \\cdot \\frac{{1}}{{6}}$; the chance of at least one $6$ must be found through the complement.",
        )
        wrong = [F(1, 2), F(1, k + 1), 1 - ans, F(6, 11), ans + F(1, 20)]
    return (p, ans, wrong, ["Set up a recursion or a geometric series over rounds."], sol)
