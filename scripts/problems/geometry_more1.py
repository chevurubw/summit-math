"""Extra Geometry problem types (part 1): angles, right triangles, similar triangles."""
import math
from fractions import Fraction as F

from algebra_more2 import rad
from common import NAMES, C, Q, num, par, sg

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def deg(v):
    return C(f"{ftex(v)}^\\circ", float(v))


def QD(p, ans, wrong, *args, **kw):
    """Q with every choice shown in degrees."""
    a = deg(ans)
    kw.setdefault("ans_tex", a.tex)
    return Q(p, a, [deg(w) for w in wrong], *args, **kw)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10), (12, 16, 20)]


# ================================================================ geo_angles
S = "geo_angles"


@reg(S, "basics")
def an_interior_regular(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    ans = F(180 * (n - 2), n)
    p = f"What is the measure of each interior angle of a regular polygon with ${n}$ sides?"
    return QD(p, ans, [F(360, n), F(180 * n, n + 2), 180 * (n - 2), ans - 10, 180 - F(180, n)], "Each exterior angle is $\\frac{360^\\circ}{n}$.",
              "one interior angle.", "interior and exterior angles at a vertex add to $180^\\circ$, and the exterior angles of any polygon add to $360^\\circ$.",
              [f"Exterior angle: $\\frac{{360^\\circ}}{{{n}}} = {ftex(F(360, n))}^\\circ$.", f"Interior: $180^\\circ - {ftex(F(360, n))}^\\circ = {ftex(ans)}^\\circ$."],
              "answering the exterior angle.")


@reg(S, "basics")
def an_sum_interior(r):
    n = r.randint(5, 20)
    ans = 180 * (n - 2)
    p = f"What is the sum of the interior angles of a convex polygon with ${n}$ sides?"
    return QD(p, ans, [180 * n, 180 * (n - 1), 360 * (n - 2), ans - 180 if ans > 180 else 360, 360], "Split the polygon into triangles from one vertex.",
              "the angle sum.", "drawing diagonals from one vertex splits an $n$-gon into $n - 2$ triangles, each with $180^\\circ$.",
              [f"${n} - 2 = {n - 2}$ triangles.", f"${n - 2} \\cdot 180^\\circ = {ans}^\\circ$."],
              "using $n$ triangles instead of $n - 2$.")


@reg(S, "basics")
def an_complement(r):
    k = r.choice([2, 3, 4, 5, 8, 9])
    x = F(90, k + 1)
    p = f"The complement of an angle is ${k}$ times the angle. What is the angle?"
    return QD(p, x, [F(180, k + 1), F(90, k), 90 - x, F(90 * k, k + 1), x + 10], "Complementary angles add to $90^\\circ$.",
              "the angle $x$.", "its complement is $90^\\circ - x$.",
              [f"$90 - x = {k}x$, so ${k + 1}x = 90$.", f"$x = {ftex(x)}^\\circ$."],
              "using $180^\\circ$ (that's for supplements).")


@reg(S, "basics")
def an_supplement(r):
    a, b = r.randint(2, 4), r.randint(5, 40)
    x = F(180 - b, a + 1)
    if x.denominator != 1:
        return None
    p = f"The supplement of an angle is ${b}^\\circ$ more than ${a}$ times the angle. What is the angle?"
    return QD(p, x, [180 - x, F(90 - b, a + 1) if 90 > b else x + 5, F(180 + b, a + 1), x + b, F(180, a + 1)], "Supplementary angles add to $180^\\circ$.",
              "the angle $x$.", "the supplement is $180^\\circ - x$.",
              [f"$180 - x = {a}x + {b}$.", f"${a + 1}x = {180 - b}$, so $x = {ftex(x)}^\\circ$."],
              "answering the supplement.")


@reg(S, "basics")
def an_vertical(r):
    a, c = r.sample(range(2, 9), 2)
    x = r.randint(5, 20)
    b = r.randint(-20, 30)
    ang = a * x + b
    d = ang - c * x
    if not 0 < ang < 180:
        return None
    p = f"Two lines cross, forming vertical angles of $({a}x{sg(b)})^\\circ$ and $({c}x{sg(d)})^\\circ$. What is the measure of each of these angles?"
    return QD(p, ang, [x, 180 - ang, ang + a, F(180 - b - d, a + c), 2 * ang if 2 * ang < 360 else ang - 10], "Vertical angles are equal.",
              "the angle measure.", "angles opposite each other at a crossing are equal.",
              [f"${a}x{sg(b)} = {c}x{sg(d)}$, so ${a - c}x = {d - b}$ and $x = {x}$.", f"Angle: ${a} \\cdot {x}{sg(b)} = {ang}^\\circ$."],
              "stopping at $x$.")


@reg(S, "basics")
def an_ratio_triangle(r):
    a, b, c = sorted(r.sample(range(1, 10), 3))
    s = a + b + c
    if 180 % s:
        return None
    ans = c * 180 // s
    p = f"The angles of a triangle are in the ratio ${a}:{b}:{c}$. What is the largest angle?"
    return QD(p, ans, [a * 180 // s, b * 180 // s, F(180, 3), c * 360 // s if c * 360 // s < 360 else ans + 20, 180 - ans], "The angles add to $180^\\circ$.",
              "the largest angle.", "split $180^\\circ$ into " + str(s) + " equal parts.",
              [f"One part: $\\frac{{180}}{{{s}}} = {180 // s}^\\circ$.", f"Largest: ${c} \\cdot {180 // s} = {ans}^\\circ$."],
              "using $360^\\circ$ for the triangle's angle sum.")


@reg(S, "basics")
def an_alternate(r):
    a, c = r.sample(range(2, 9), 2)
    x = r.randint(4, 18)
    b = r.randint(-10, 30)
    ang = a * x + b
    d = ang - c * x
    if not 0 < ang < 180:
        return None
    p = f"Two parallel lines are cut by a transversal. A pair of alternate interior angles measure $({a}x{sg(b)})^\\circ$ and $({c}x{sg(d)})^\\circ$. What is $x$?"
    return Q(p, x, [ang, F(180 - b - d, a + c) if F(180 - b - d, a + c) != x else x + 2, x + 1, x - 1, F(d - b, a + c) if F(d - b, a + c) != x else x + 3], "Alternate interior angles are equal.",
             "$x$.", "with parallel lines, alternate interior angles are equal (not supplementary).",
             [f"${a}x{sg(b)} = {c}x{sg(d)}$.", f"${a - c}x = {d - b}$, so $x = {x}$."],
             "setting the angles to add to $180^\\circ$.")


@reg(S, "basics")
def an_sides_from_interior(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 36])
    ang = F(180 * (n - 2), n)
    p = f"Each interior angle of a regular polygon is ${ftex(ang)}^\\circ$. How many sides does it have?"
    return Q(p, n, [n + 1, n - 1, n + 2, F(360, ang).__ceil__() if F(360, ang).__ceil__() != n else n * 2, 2 * n], "Find the exterior angle first.",
             "the number of sides.", "exterior angle $= 180^\\circ - $ interior, and $n = \\frac{360^\\circ}{\\text{exterior}}$.",
             [f"Exterior: $180 - {ftex(ang)} = {ftex(180 - ang)}^\\circ$.", f"$n = \\frac{{360}}{{{ftex(180 - ang)}}} = {n}$."],
             "dividing $360^\\circ$ by the interior angle.")


@reg(S, "basics")
def an_around_point(r):
    ks = [r.randint(1, 5) for _ in range(4)]
    bs = [r.randint(0, 30) for _ in range(4)]
    tot_k, tot_b = sum(ks), sum(bs)
    if (360 - tot_b) % tot_k:
        return None
    x = (360 - tot_b) // tot_k
    angs = [k * x + b for k, b in zip(ks, bs)]
    if min(angs) <= 0:
        return None
    exprs = [f"({k if k > 1 else ''}x{sg(b)})^\\circ" if b else f"{k if k > 1 else ''}x^\\circ" for k, b in zip(ks, bs)]
    p = f"Four angles around a point measure ${exprs[0]}$, ${exprs[1]}$, ${exprs[2]}$, and ${exprs[3]}$. What is the largest of them?"
    return QD(p, max(angs), [x, min(angs), F(180 - tot_b, tot_k) * max(ks) if F(180 - tot_b, tot_k) > 0 else max(angs) + 10, max(angs) - 5, 90], "Angles all the way around a point add to $360^\\circ$.",
              "the largest angle.", "a full turn is $360^\\circ$.",
              [f"Sum: ${tot_k}x + {tot_b} = 360$, so $x = {x}$.", "Angles: " + ", ".join(f"${a}^\\circ$" for a in angs) + f". Largest: ${max(angs)}^\\circ$."],
              "using $180^\\circ$ for a full turn.")


@reg(S, "basics")
def an_right_acute(r):
    k = r.randint(4, 40)
    if k % 2:
        k += 1
    small = (90 - k) // 2
    p = f"In a right triangle, one acute angle is ${k}^\\circ$ more than the other. What is the smaller acute angle?"
    return QD(p, small, [small + k, 90 - k, (180 - k) // 2, small + 5, 45], "The two acute angles add to $90^\\circ$.",
              "the smaller acute angle.", "in a right triangle the two acute angles share the remaining $90^\\circ$.",
              [f"$x + (x + {k}) = 90$, so $2x = {90 - k}$.", f"$x = {small}^\\circ$."],
              "using $180^\\circ$ instead of $90^\\circ$.")


@reg(S, "basics")
def an_iso_vertex(r):
    base = r.randint(20, 85)
    ans = 180 - 2 * base
    p = f"Each base angle of an isosceles triangle measures ${base}^\\circ$. What is the vertex angle?"
    return QD(p, ans, [180 - base, base, F(180 - base, 2), 90 - base if base < 90 else 10, ans + 10], "The two base angles are equal.",
              "the vertex angle.", "the three angles add to $180^\\circ$, and two of them are " + str(base) + "°.",
              [f"$180 - 2 \\cdot {base} = {ans}$."], "subtracting only one base angle.")


@reg(S, "basics")
def an_quad_missing(r):
    angs = [r.randint(50, 130) for _ in range(3)]
    last = 360 - sum(angs)
    if not 20 < last < 180:
        return None
    p = f"Three angles of a quadrilateral measure ${angs[0]}^\\circ$, ${angs[1]}^\\circ$, and ${angs[2]}^\\circ$. What is the fourth angle?"
    return QD(p, last, [180 - sum(angs) % 180 if 180 - sum(angs) % 180 != last else last + 10, 540 - sum(angs) if 540 - sum(angs) < 360 else last - 10, last + 20, 90, 360 - max(angs)], "A quadrilateral's angles add to $360^\\circ$.",
              "the missing angle.", "any quadrilateral splits into two triangles, so its angles add to $360^\\circ$.",
              [f"${angs[0]} + {angs[1]} + {angs[2]} = {sum(angs)}$.", f"$360 - {sum(angs)} = {last}^\\circ$."],
              "using $180^\\circ$ as the angle sum.")


@reg(S, "basics")
def an_exterior_missing(r):
    ext = [r.randint(40, 100) for _ in range(4)]
    last = 360 - sum(ext)
    if not 10 < last < 180:
        return None
    p = f"Four exterior angles of a convex pentagon (one at each of four vertices) are ${ext[0]}^\\circ$, ${ext[1]}^\\circ$, ${ext[2]}^\\circ$, and ${ext[3]}^\\circ$. What is the interior angle at the fifth vertex?"
    return QD(p, 180 - last, [last, 540 - sum(180 - e for e in ext) if 540 - sum(180 - e for e in ext) != 180 - last else last + 5, 180 - last + 10, 108, 360 - last], "Exterior angles of a polygon add to $360^\\circ$.",
              "the fifth interior angle.", "one exterior angle per vertex always adds to $360^\\circ$; then interior $= 180^\\circ -$ exterior.",
              [f"Fifth exterior angle: $360 - {sum(ext)} = {last}^\\circ$.", f"Interior: $180 - {last} = {180 - last}^\\circ$."],
              "giving the exterior angle.")


@reg(S, "basics")
def an_bisector_angle(r):
    A, B = r.randint(30, 90), r.randint(30, 80)
    Cc = 180 - A - B
    if Cc < 20 or Cc % 2:
        return None
    ans = 180 - A - Cc // 2
    p = f"In triangle $ABC$, $\\angle A = {A}^\\circ$ and $\\angle B = {B}^\\circ$. The bisector of $\\angle C$ meets $AB$ at $D$. What is $\\angle ADC$?"
    return QD(p, ans, [180 - B - Cc // 2, Cc // 2, 180 - ans, ans + 5, 90], "Find $\\angle C$, then half of it.",
              "$\\angle ADC$.", "look at triangle $ADC$: it has $\\angle A$, half of $\\angle C$, and $\\angle ADC$.",
              [f"$\\angle C = 180 - {A} - {B} = {Cc}^\\circ$, so $\\angle ACD = {Cc // 2}^\\circ$.", f"In triangle $ADC$: $\\angle ADC = 180 - {A} - {Cc // 2} = {ans}^\\circ$."],
              "using triangle $BDC$ instead, which gives $\\angle BDC$.")


@reg(S, "basics")
def an_arith_triangle(r):
    a = r.randint(15, 55)
    ans = 120 - a
    p = f"The angles of a triangle form an arithmetic sequence, and the smallest is ${a}^\\circ$. What is the largest?"
    return QD(p, ans, [60, 180 - 2 * a, 60 + a, ans - 10, 90], "The middle angle of an arithmetic sequence is the average.",
              "the largest angle.", "three angles in arithmetic sequence average to $60^\\circ$, so the middle one is $60^\\circ$.",
              [f"Middle: $60^\\circ$. The common difference is $60 - {a} = {60 - a}$.", f"Largest: $60 + {60 - a} = {ans}^\\circ$."],
              "assuming the middle angle is unknown and getting stuck.")


@reg(S, "basics")
def an_linear_pair(r):
    a, c = r.randint(2, 6), r.randint(1, 4)
    b, d = r.randint(-10, 30), r.randint(-10, 30)
    if (180 - b - d) % (a + c):
        return None
    x = (180 - b - d) // (a + c)
    A_, B_ = a * x + b, c * x + d
    if min(A_, B_) <= 0:
        return None
    p = f"Two angles form a linear pair (they make a straight line). One is $({a}x{sg(b)})^\\circ$ and the other is $({c if c > 1 else ''}x{sg(d)})^\\circ$. What is the larger angle?"
    return QD(p, max(A_, B_), [min(A_, B_), x, 90, F(360 - b - d, a + c) * a if 360 > b + d else max(A_, B_) + 10, max(A_, B_) - 10], "A straight line is $180^\\circ$.",
              "the larger angle.", "angles on a straight line add to $180^\\circ$.",
              [f"${a + c}x + {b + d} = 180$, so $x = {x}$.", f"Angles: ${A_}^\\circ$ and ${B_}^\\circ$."],
              "setting them equal (that's for vertical angles).")


@reg(S, "challenge")
def anc_pentagon_ap(r):
    d = r.randint(2, 15)
    small = 108 - 2 * d
    p = f"The interior angles of a convex pentagon form an arithmetic sequence with common difference ${d}^\\circ$. What is the largest angle?"
    return QD(p, 108 + 2 * d, [108, 108 + d, 108 + 4 * d, small, 108 + 3 * d], "A pentagon's angles add to $540^\\circ$.",
              "the largest angle.", "five angles in arithmetic sequence average to the middle one, which is $\\frac{540}{5} = 108^\\circ$.",
              [f"Middle angle: $108^\\circ$. The angles are $108 - {2 * d}, 108 - {d}, 108, 108 + {d}, 108 + {2 * d}$.", f"Largest: ${108 + 2 * d}^\\circ$."],
              "putting $108^\\circ$ as the smallest angle.")


@reg(S, "challenge")
def anc_two_polygons(r):
    pairs = [(n, n + k) for n in range(3, 40) for k in (1, 2, 3, 4, 6) if (F(360, n) - F(360, n + k)).denominator == 1]
    n, m = r.choice(pairs)
    D = F(360, n) - F(360, m)
    p = f"Two regular polygons have ${m - n}$ sides difference, and each interior angle of the one with more sides is ${ftex(D)}^\\circ$ larger than each interior angle of the other. How many sides does the smaller polygon have?"
    return Q(p, n, [m, n + 1, n - 1, 2 * n, F(360, D) if F(360, D).denominator == 1 and F(360, D) != n else n + 3], "Interior angles differ exactly when exterior angles do (in the other direction).",
             "the smaller polygon's side count.", "the exterior angles $\\frac{360}{n}$ and $\\frac{360}{n + " + str(m - n) + "}$ differ by " + ftex(D) + "°.",
             [f"$\\frac{{360}}{{n}} - \\frac{{360}}{{n + {m - n}}} = {ftex(D)}$.", f"Try values: $n = {n}$ gives ${ftex(F(360, n))} - {ftex(F(360, m))} = {ftex(D)}$. It works."],
             "setting up the difference with interior angles and making an algebra slip; exterior angles are simpler.")


@reg(S, "challenge")
def anc_bisector_altitude(r):
    B, Cc = r.sample(range(30, 90), 2)
    if 180 - B - Cc < 10 or (B - Cc) % 2:
        return None
    ans = abs(B - Cc) // 2
    p = f"In triangle $ABC$, $\\angle B = {B}^\\circ$ and $\\angle C = {Cc}^\\circ$. What is the angle between the altitude from $A$ and the bisector of $\\angle A$?"
    return QD(p, ans, [abs(B - Cc), F(180 - B - Cc, 2), 90 - max(B, Cc), ans + 5, F(B + Cc, 2)], "Find where each line sits relative to side $AB$.",
              "the angle between the altitude and the angle bisector.", "measure both lines from side $AB$: the altitude makes $90^\\circ - \\angle B$ with it, the bisector makes $\\frac{\\angle A}{2}$.",
              [f"$\\angle A = {180 - B - Cc}^\\circ$, so the bisector makes ${ftex(F(180 - B - Cc, 2))}^\\circ$ with $AB$.", f"The altitude makes $90 - {B} = {90 - B}^\\circ$ with $AB$.", f"Difference: $|{ftex(F(180 - B - Cc, 2))} - {90 - B}| = {ans}^\\circ$, which is always $\\frac{{|\\angle B - \\angle C|}}{{2}}$."],
              "subtracting the two base angles without halving.")


@reg(S, "challenge")
def anc_comp_supp(r):
    k = r.choice([F(1, 3), F(1, 4), F(1, 5), F(2, 5), F(1, 6), F(2, 7)])
    x = (90 - 180 * k) / (1 - k)
    if x <= 0 or x >= 90:
        return None
    p = f"The complement of an angle is ${ftex(k)}$ of its supplement. What is the angle?"
    return QD(p, x, [90 - x, 180 - x, x + 10, 90 * k, F(90, 2)], "Write both the complement and the supplement in terms of $x$.",
              "the angle $x$.", "complement $= 90 - x$, supplement $= 180 - x$.",
              [f"$90 - x = {ftex(k)}(180 - x)$.", f"$90 - x = {ftex(180 * k)} - {ftex(k)}x$, so ${ftex(1 - k)}x = {ftex(90 - 180 * k)}$.", f"$x = {ftex(x)}^\\circ$."],
              "putting the fraction on the wrong side.")


@reg(S, "challenge")
def anc_integer_angles(r):
    N = r.randint(10, 100)
    ns = [n for n in range(3, N + 1) if 360 % n == 0]
    p = f"For how many integers $n$ with $3 \\le n \\le {N}$ does a regular $n$-gon have interior angles that are a whole number of degrees?"
    return Q(p, len(ns), [len(ns) + 1, len(ns) - 1, len([n for n in range(3, N + 1) if 180 % n == 0]) if len([n for n in range(3, N + 1) if 180 % n == 0]) != len(ns) else len(ns) + 2, N - 2, 22], "The interior angle is whole exactly when the exterior angle is.",
             "the count of valid $n$.", "interior $= 180 - \\frac{360}{n}$, so it's a whole number exactly when $n$ divides $360$.",
             [f"Divisors of $360$ that are at least $3$ and at most ${N}$: " + ", ".join(map(str, ns)) + ".", f"That's ${len(ns)}$ values."],
             "counting divisors of $180$ instead of $360$.")


@reg(S, "challenge")
def anc_overlap_time(r):
    h = r.randint(1, 10)
    m = F(60 * h, 11)
    p = f"After {h}:00, how many minutes pass before the hour and minute hands of a clock first point in exactly the same direction?"
    return Q(p, m, [5 * h, F(60 * h, 12), m + 1, F(30 * h, 6), F(60 * h, 10)], "The minute hand gains $5.5^\\circ$ per minute on the hour hand.",
             "the minutes until the hands overlap.", "the minute hand moves $6^\\circ$ per minute and the hour hand $0.5^\\circ$, so the gap closes at $5.5^\\circ$ per minute.",
             [f"At {h}:00 the hour hand is ${30 * h}^\\circ$ ahead.", f"Time to close the gap: $\\frac{{{30 * h}}}{{5.5}} = {ftex(m)}$ minutes."],
             "answering " + str(5 * h) + " minutes, forgetting the hour hand keeps moving.")


@reg(S, "challenge")
def anc_external_bisectors(r):
    A = r.randint(20, 140)
    if A % 2:
        A += 1
    ans = 90 - A // 2
    p = f"In triangle $ABC$, $\\angle A = {A}^\\circ$. The bisectors of the exterior angles at $B$ and $C$ meet at $P$. What is $\\angle BPC$?"
    return QD(p, ans, [90 + A // 2, 180 - A, A // 2, ans + 10, 90], "Each exterior angle at $B$ is $180^\\circ - \\angle B$.",
              "$\\angle BPC$.", "in triangle $BPC$, the angles at $B$ and $C$ are half of the exterior angles.",
              [f"$\\angle PBC = \\frac{{180 - B}}{{2}}$ and $\\angle PCB = \\frac{{180 - C}}{{2}}$.", f"They add to $\\frac{{360 - (B + C)}}{{2}} = \\frac{{360 - {180 - A}}}{{2}} = {90 + A // 2}^\\circ$.", f"$\\angle BPC = 180 - {90 + A // 2} = {ans}^\\circ$."],
              "using the interior bisector formula, $90 + \\frac{A}{2}$.")


# ================================================================ geo_right
S = "geo_right"


@reg(S, "basics")
def rt_hyp(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 4)
    p = f"A right triangle has legs ${a * k}$ and ${b * k}$. What is the hypotenuse?"
    return Q(p, c * k, [(a + b) * k, c * k + 1, (b - a) * k + c, rad(1, a * a * k * k + b * b * k * k + 1) if False else c * k + k, b * k + 1], "Pythagorean Theorem.",
             "the hypotenuse $c$.", "$c^2 = a^2 + b^2$.",
             [f"$c^2 = {a * k}^2 + {b * k}^2 = {(a * k) ** 2} + {(b * k) ** 2} = {(c * k) ** 2}$.", f"$c = {c * k}$."],
             "adding the legs without squaring.")


@reg(S, "basics")
def rt_45_hyp(r):
    s = r.randint(2, 15)
    ans = rad(s, 2)
    p = f"An isosceles right triangle has legs of length ${s}$. What is its hypotenuse?"
    return Q(p, ans, [num(2 * s), rad(s, 3), num(s), rad(2 * s, 2), rad(F(s, 2), 2)], "In a $45$-$45$-$90$ triangle the hypotenuse is $\\sqrt{2}$ times a leg.",
             "the hypotenuse.", "the sides of a $45$-$45$-$90$ triangle are in the ratio $1 : 1 : \\sqrt{2}$.",
             [f"$c = \\sqrt{{{s}^2 + {s}^2}} = \\sqrt{{{2 * s * s}}} = {ans.tex}$."], "doubling the leg.")


@reg(S, "basics")
def rt_45_leg(r):
    h = r.randint(2, 16)
    ans = rad(F(h, 2), 2)
    p = f"An isosceles right triangle has hypotenuse ${h}$. How long is each leg?"
    return Q(p, ans, [num(F(h, 2)), rad(h, 2), rad(F(h, 3), 3), num(h - 1), rad(F(h, 4), 2)], "Divide the hypotenuse by $\\sqrt{2}$.",
             "a leg.", "leg $= \\frac{\\text{hypotenuse}}{\\sqrt{2}}$.",
             [f"$\\frac{{{h}}}{{\\sqrt{{2}}}} = \\frac{{{h}\\sqrt{{2}}}}{{2}} = {ans.tex}$."], "multiplying by $\\sqrt{2}$ instead of dividing.")


@reg(S, "basics")
def rt_3060_hyp(r):
    s = r.randint(1, 9)
    long = rad(s, 3)
    p = f"In a $30$-$60$-$90$ triangle, the leg opposite the $60^\\circ$ angle is ${long.tex}$. What is the hypotenuse?"
    return Q(p, 2 * s, [s, rad(2 * s, 3), 3 * s, rad(s, 2), s + 2], "Sides are in the ratio $1 : \\sqrt{3} : 2$.",
             "the hypotenuse.", "short leg $: $ long leg $: $ hypotenuse $= 1 : \\sqrt{3} : 2$.",
             [f"Long leg $= \\sqrt{{3}} \\times$ short leg, so the short leg is ${s}$.", f"Hypotenuse $= 2 \\times {s} = {2 * s}$."],
             "doubling the long leg.")


@reg(S, "basics")
def rt_sq_diag(r):
    s = r.randint(2, 15)
    p = f"What is the length of a diagonal of a square with side ${s}$?"
    return Q(p, rad(s, 2), [num(2 * s), rad(s, 3), num(s * s), rad(2 * s, 2), num(s + 1)], "The diagonal makes two isosceles right triangles.",
             "the diagonal.", "diagonal $= s\\sqrt{2}$.",
             [f"$d^2 = {s}^2 + {s}^2 = {2 * s * s}$, so $d = {rad(s, 2).tex}$."], "doubling the side.")


@reg(S, "basics")
def rt_sq_side(r):
    s = r.randint(2, 15)
    d = rad(s, 2)
    p = f"A square has diagonal ${d.tex}$. What is its area?"
    return Q(p, s * s, [2 * s * s, s, 4 * s, s * s * 2 // 1 + s, F(s * s, 2)], "Area of a square is half the diagonal squared.",
             "the area.", "the side is $\\frac{d}{\\sqrt{2}}$, so area $= \\frac{d^2}{2}$.",
             [f"$d^2 = {2 * s * s}$.", f"Area $= \\frac{{{2 * s * s}}}{{2}} = {s * s}$."], "squaring the diagonal without halving.")


@reg(S, "basics")
def rt_eq_height(r):
    s = r.choice([2, 4, 6, 8, 10, 12, 14])
    ans = rad(F(s, 2), 3)
    p = f"What is the height of an equilateral triangle with side ${s}$?"
    return Q(p, ans, [num(s), rad(s, 3), num(F(s, 2)), rad(F(s, 2), 2), rad(F(s, 4), 3)], "The height splits it into two $30$-$60$-$90$ triangles.",
             "the height.", "the height is the long leg of a $30$-$60$-$90$ triangle whose hypotenuse is a side.",
             [f"Short leg: $\\frac{{{s}}}{{2}} = {s // 2}$.", f"Height: ${s // 2}\\sqrt{{3}} = {ans.tex}$."], "using $\\frac{s}{2}$ as the height.")


@reg(S, "basics")
def rt_shortcut(r):
    a, b, c = r.choice(TRIPLES)
    k = r.choice([10, 20, 30])
    save = (a + b - c) * k
    p = f"A rectangular field is ${a * k}$ m by ${b * k}$ m. How many meters shorter is it to walk diagonally across than along two sides?"
    return Q(p, save, [c * k, (a + b) * k, save + k, (b - a) * k, a * k], "Find the diagonal.",
             "the distance saved.", "walking along two sides is $a + b$; the diagonal is $\\sqrt{a^2 + b^2}$.",
             [f"Two sides: ${a * k} + {b * k} = {(a + b) * k}$ m.", f"Diagonal: $\\sqrt{{{(a * k) ** 2} + {(b * k) ** 2}}} = {c * k}$ m.", f"Saved: ${save}$ m."],
             "answering the diagonal length.")


@reg(S, "basics")
def rt_iso_height(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    p = f"An isosceles triangle has two sides of length ${c * k}$ and a base of ${2 * a * k}$. What is the height to the base?"
    return Q(p, b * k, [a * k, c * k, F(c * k, 2), b * k + 1, 2 * b * k], "The height cuts the base in half.",
             "the height.", "the height from the top meets the base at its midpoint, making two right triangles.",
             [f"Half the base: ${a * k}$.", f"Height: $\\sqrt{{{c * k}^2 - {a * k}^2}} = {b * k}$."], "using the full base in the Pythagorean Theorem.")


@reg(S, "basics")
def rt_iso_area(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    area = a * b * k * k
    p = f"An isosceles triangle has sides ${c * k}$, ${c * k}$, and ${2 * a * k}$. What is its area?"
    return Q(p, area, [2 * area, F(area, 2), c * k * a * k, area + a * k, a * c * k * k], "Find the height to the base first.",
             "the area.", "the height to the base splits it into two right triangles.",
             [f"Height: $\\sqrt{{{c * k}^2 - {a * k}^2}} = {b * k}$.", f"Area $= \\frac{{1}}{{2}} \\cdot {2 * a * k} \\cdot {b * k} = {area}$."],
             "forgetting the $\\frac{1}{2}$.")


@reg(S, "basics")
def rt_rhombus_side(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    p = f"A rhombus has diagonals of lengths ${2 * a * k}$ and ${2 * b * k}$. What is the length of each side?"
    return Q(p, c * k, [2 * c * k, (a + b) * k, c * k + 1, F((a + b) * k, 2) if F((a + b) * k, 2) != c * k else c * k + 2, a * b * k], "The diagonals of a rhombus bisect each other at right angles.",
             "a side length.", "the diagonals cut each other in half at $90^\\circ$, forming four right triangles.",
             [f"Half-diagonals: ${a * k}$ and ${b * k}$.", f"Side: $\\sqrt{{{a * k}^2 + {b * k}^2}} = {c * k}$."],
             "using the full diagonals as the legs.")


@reg(S, "basics")
def rt_3060_perim(r):
    h = r.choice([2, 4, 6, 8, 10, 12])
    s = h // 2
    tex = f"{s + h} + {'' if s == 1 else s}\\sqrt{{3}}"
    ans = C(tex, s + h + s * math.sqrt(3))
    p = f"A right triangle has a $30^\\circ$ angle and hypotenuse ${h}$. What is its perimeter?"
    return Q(p, ans, [C(f"{3 * s} + {'' if s == 1 else s}\\sqrt{{3}}", 3 * s + s * math.sqrt(3)), C(f"{h + s}", h + s), C(f"{h} + {'' if s == 1 else s}\\sqrt{{2}}", h + s * math.sqrt(2)), C(f"{s + h} + {2 * s}\\sqrt{{3}}", s + h + 2 * s * math.sqrt(3))],
             "Find both legs from the $1 : \\sqrt{3} : 2$ ratio.", "the perimeter.", "a $30$-$60$-$90$ triangle has sides $s$, $s\\sqrt{3}$, $2s$.",
             [f"Hypotenuse ${h} = 2s$, so $s = {s}$.", f"Legs: ${s}$ and ${'' if s == 1 else s}\\sqrt{{3}}$.", f"Perimeter: ${tex}$."],
             "mixing up which leg goes with which angle.", sort=False)


@reg(S, "basics")
def rt_area_leg(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    A = a * b * k * k // 2
    p = f"A right triangle has area ${A}$ and one leg of length ${a * k}$. What is its hypotenuse?"
    return Q(p, c * k, [b * k, (a + b) * k, F(2 * A, a * k) + a * k, c * k + 1, A // (a * k) if A % (a * k) == 0 and A // (a * k) != c * k else c * k + 2], "Use the area to find the other leg.",
             "the hypotenuse.", "area $= \\frac{1}{2} \\cdot$ leg $\\cdot$ leg.",
             [f"Other leg: $\\frac{{2 \\cdot {A}}}{{{a * k}}} = {b * k}$.", f"Hypotenuse: $\\sqrt{{{a * k}^2 + {b * k}^2}} = {c * k}$."],
             "forgetting to double the area.")


@reg(S, "basics")
def rt_screen(r):
    k = r.randint(2, 12)
    d = 5 * k
    area = 12 * k * k
    p = f"A screen has width and height in the ratio $4:3$ and a diagonal of ${d}$ inches. What is its area, in square inches?"
    return Q(p, area, [d * d, 4 * k + 3 * k, area * 2, F(d * d, 2), 7 * k * k], "Width, height, diagonal are $4k$, $3k$, $5k$.",
             "the area.", "the $4:3$ sides with the diagonal make a $3$-$4$-$5$ right triangle.",
             [f"$5k = {d}$, so $k = {k}$.", f"Width ${4 * k}$, height ${3 * k}$.", f"Area $= {4 * k} \\cdot {3 * k} = {area}$."],
             "squaring the diagonal.")


@reg(S, "basics")
def rt_ratio_leg(r):
    k = r.randint(2, 15)
    p = f"The legs of a right triangle are in the ratio $3:4$, and its hypotenuse is ${5 * k}$. What is the shorter leg?"
    return Q(p, 3 * k, [4 * k, 5 * k, 3 * k + 1, F(15 * k, 4), k], "The sides are $3k$, $4k$, $5k$.",
             "the shorter leg.", "a $3:4$ leg ratio means a $3$-$4$-$5$ triangle scaled by some $k$.",
             [f"$5k = {5 * k}$, so $k = {k}$.", f"Shorter leg: $3 \\cdot {k} = {3 * k}$."], "answering the longer leg.")


@reg(S, "basics")
def rt_median_hyp(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 4)
    p = f"A right triangle has legs ${a * k}$ and ${b * k}$. How long is the median from the right angle to the hypotenuse?"
    return Q(p, F(c * k, 2), [c * k, F(a * k + b * k, 2), F(a * b * k, c), F(c * k, 3), b * k], "The midpoint of the hypotenuse is the center of the circumscribed circle.",
             "the median length.", "in a right triangle, the midpoint of the hypotenuse is equally far from all three vertices.",
             [f"Hypotenuse: ${c * k}$.", f"Median $= \\frac{{{c * k}}}{{2}} = {ftex(F(c * k, 2))}$."], "confusing the median with the altitude.")


@reg(S, "challenge")
def rtc_sum_hyp_area(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    Sm, Cc = (a + b) * k, c * k
    area = a * b * k * k // 2
    p = f"A right triangle has legs adding to ${Sm}$ and hypotenuse ${Cc}$. What is its area?"
    return Q(p, area, [2 * area, area + Sm, F(Sm * Sm - Cc * Cc, 2), F(Sm * Cc, 4), area - 1], "Square $a + b$.",
             "the area $\\frac{ab}{2}$.", "$(a + b)^2 = a^2 + b^2 + 2ab = c^2 + 2ab$.",
             [f"${Sm}^2 = {Cc}^2 + 2ab$, so $2ab = {Sm * Sm} - {Cc * Cc} = {Sm * Sm - Cc * Cc}$.", f"Area $= \\frac{{ab}}{{2}} = \\frac{{{Sm * Sm - Cc * Cc}}}{{4}} = {area}$."],
             "stopping at $2ab$ or $ab$.")


@reg(S, "challenge")
def rtc_ladder(r):
    L, a, b = r.choice([(25, 7, 24), (13, 5, 12), (17, 8, 15), (10, 6, 8), (25, 15, 20), (26, 10, 24)])
    s = r.choice([x for x in range(1, b) if math.isqrt(L * L - (b - x) ** 2) ** 2 == L * L - (b - x) ** 2] or [None])
    if s is None:
        return None
    new = math.isqrt(L * L - (b - s) ** 2)
    p = f"A ${L}$ foot ladder leans against a wall with its foot ${a}$ feet from the wall. If the top slides down ${s}$ feet, how many feet does the foot slide out?"
    return Q(p, new - a, [s, new, a + s, new - a + 1, b - s], "Find the new height, then the new base.",
             "how far the foot moves.", "the ladder's length never changes, so use the Pythagorean Theorem twice.",
             [f"Starting height: $\\sqrt{{{L}^2 - {a}^2}} = {b}$.", f"New height: ${b} - {s} = {b - s}$.", f"New base: $\\sqrt{{{L}^2 - {b - s}^2}} = {new}$.", f"Moved: ${new} - {a} = {new - a}$."],
             "assuming the foot moves the same distance the top drops.")


@reg(S, "challenge")
def rtc_alt_geo_mean(r):
    p_, q_ = r.choice([(1, 4), (1, 9), (4, 9), (2, 8), (3, 12), (4, 16), (9, 16), (1, 16), (5, 20)])
    h = math.isqrt(p_ * q_)
    p = f"The altitude to the hypotenuse of a right triangle splits the hypotenuse into pieces of ${p_}$ and ${q_}$. How long is the altitude?"
    return Q(p, h, [F(p_ + q_, 2), p_ * q_, h + 1, q_ - p_, rad(1, p_ * p_ + q_ * q_)], "The two small triangles are similar.",
             "the altitude $h$.", "the altitude to the hypotenuse is the geometric mean of the two pieces: $h^2 = pq$.",
             [f"Similar triangles give $\\frac{{h}}{{{p_}}} = \\frac{{{q_}}}{{h}}$.", f"$h^2 = {p_} \\cdot {q_} = {p_ * q_}$, so $h = {h}$."],
             "averaging the two pieces.")


@reg(S, "challenge")
def rtc_british_flag(r):
    a, b, c = [r.randint(2, 12) for _ in range(3)]
    d2 = a * a + c * c - b * b
    if d2 <= 0:
        return None
    ans = rad(1, d2)
    p = f"Point $P$ is inside rectangle $ABCD$ with $PA = {a}$, $PB = {b}$, and $PC = {c}$. What is $PD$?"
    return Q(p, ans, [rad(1, a * a + b * b - c * c) if a * a + b * b - c * c > 0 else num(a + c - b + 1), num(a + c - b) if a + c - b > 0 else num(b + 1), rad(1, d2 + 1), rad(1, b * b + c * c - a * a) if b * b + c * c - a * a > 0 else num(c + 2), num(F(a + b + c, 3))],
             "Opposite corners pair up.", "$PD$.", "British Flag Theorem: $PA^2 + PC^2 = PB^2 + PD^2$ for any point in a rectangle.",
             [f"Drop perpendiculars from $P$ to the sides; each squared distance splits into two pieces, and opposite corners share the same pieces.",
              f"$PD^2 = PA^2 + PC^2 - PB^2 = {a * a} + {c * c} - {b * b} = {d2}$.", f"$PD = {ans.tex}$."],
             "pairing adjacent corners instead of opposite ones.")


@reg(S, "challenge")
def rtc_eq_from_height(r):
    h = r.randint(2, 12)
    area = rad(F(h * h, 3), 3)
    p = f"An equilateral triangle has height ${h}$. What is its area?"
    return Q(p, area, [rad(F(h * h, 2), 3), num(h * h), rad(F(h * h, 4), 3), rad(F(h * h, 3), 2), num(F(h * h, 2))], "Find the side first.",
             "the area.", "height $= \\frac{\\sqrt{3}}{2}s$, so $s = \\frac{2h}{\\sqrt{3}}$.",
             [f"$s = \\frac{{2 \\cdot {h}}}{{\\sqrt{{3}}}}$.", f"Area $= \\frac{{1}}{{2}} \\cdot s \\cdot h = \\frac{{{h}^2}}{{\\sqrt{{3}}}} = {area.tex}$."],
             "using the height as the side.")


@reg(S, "challenge")
def rtc_spiral(r):
    n = r.randint(5, 40)
    ans = rad(1, n + 1)
    p = f"Start with a right triangle with legs $1$ and $1$. On its hypotenuse, build a right triangle with the other leg $1$; repeat, each time using the newest hypotenuse as a leg and adding a leg of $1$. What is the hypotenuse of the ${n}$th triangle?"
    return Q(p, ans, [rad(1, n), num(n), rad(1, n + 2), rad(1, 2 * n), num(F(n + 1, 2))], "Track the squares of the hypotenuses.",
             "the " + str(n) + "th hypotenuse.", "each new hypotenuse squared is the old one squared plus $1$.",
             ["Triangle 1: $1^2 + 1^2 = 2$. Triangle 2: $2 + 1 = 3$. Triangle 3: $3 + 1 = 4$.", f"Triangle ${n}$: hypotenuse squared $= {n + 1}$, so it is ${ans.tex}$."],
             "an off by one: the first hypotenuse is already $\\sqrt{2}$.")


@reg(S, "challenge")
def rtc_iso_perim_area(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    P = 2 * c * k + 2 * a * k
    area = a * b * k * k
    p = f"An isosceles triangle has a base of ${2 * a * k}$ and a perimeter of ${P}$. What is its area?"
    return Q(p, area, [2 * area, F(area, 2), c * k * a * k, area + a * k, P * a * k // 2], "Find the equal sides from the perimeter.",
             "the area.", "the equal sides share the rest of the perimeter, and the height cuts the base in half.",
             [f"Equal sides: $\\frac{{{P} - {2 * a * k}}}{{2}} = {c * k}$.", f"Height: $\\sqrt{{{c * k}^2 - {a * k}^2}} = {b * k}$.", f"Area: $\\frac{{1}}{{2}} \\cdot {2 * a * k} \\cdot {b * k} = {area}$."],
             "using half the base as the full base in the area formula.")


# ================================================================ geo_similar
S = "geo_similar"


@reg(S, "basics")
def si_perimeter(r):
    sides = r.sample(range(4, 15), 3)
    k = F(r.randint(2, 5), r.choice([1, 2]))
    if (sides[0] * k).denominator != 1:
        return None
    P = sum(sides)
    p = f"Triangle $ABC$ has sides ${sides[0]}$, ${sides[1]}$, and ${sides[2]}$. A similar triangle has a side of ${ftex(sides[0] * k)}$ matching the side of length ${sides[0]}$. What is its perimeter?"
    return Q(p, P * k, [P + sides[0] * k - sides[0], P * k * k, P * k + 1, P, P * k / 2], "Perimeters scale by the same factor as sides.",
             "the perimeter of the similar triangle.", "all lengths, including perimeter, scale by the same ratio.",
             [f"Scale factor: $\\frac{{{ftex(sides[0] * k)}}}{{{sides[0]}}} = {ftex(k)}$.", f"Perimeter: ${P} \\cdot {ftex(k)} = {ftex(P * k)}$."],
             "adding the difference instead of multiplying.")


@reg(S, "basics")
def si_side_from_area(r):
    s1 = r.randint(3, 15)
    k = r.choice([2, 3, 4, F(3, 2), F(5, 2)])
    A1 = r.randint(5, 40)
    p = f"Two similar triangles have areas ${A1}$ and ${ftex(A1 * k * k)}$. A side of the smaller one is ${s1}$. How long is the matching side of the larger one?"
    return Q(p, s1 * k, [s1 * k * k, s1 + k, F(s1 * A1 * k * k, A1 + 1) if False else s1 * 2 if s1 * 2 != s1 * k else s1 * 3, s1 * k + 1, F(s1, k)], "Area ratio is the square of the side ratio.",
             "the matching side.", "if sides scale by $k$, areas scale by $k^2$.",
             [f"Area ratio: $\\frac{{{ftex(A1 * k * k)}}}{{{A1}}} = {ftex(k * k)}$.", f"Side ratio: $\\sqrt{{{ftex(k * k)}}} = {ftex(k)}$.", f"Side: ${s1} \\cdot {ftex(k)} = {ftex(s1 * k)}$."],
             "scaling the side by the area ratio.")


@reg(S, "basics")
def si_volume_ratio(r):
    a, b = r.sample([1, 2, 3, 4, 5], 2)
    V = r.choice([8, 16, 24, 27, 54, 64, 81, 125])
    ans = F(V * b ** 3, a ** 3)
    if ans.denominator != 1 or ans > 5000:
        return None
    p = f"Two similar statues have heights in the ratio ${a}:{b}$. The first uses ${V}$ liters of clay. How many liters does the second use?"
    return Q(p, ans, [F(V * b, a), F(V * b * b, a * a), ans + V, ans / 2, F(V * b ** 3, a ** 2)], "Volume scales with the cube of length.",
             "the second volume.", "if lengths scale by $k$, volumes scale by $k^3$.",
             [f"Length ratio: ${ftex(F(b, a))}$.", f"Volume ratio: $\\left({ftex(F(b, a))}\\right)^3 = {ftex(F(b ** 3, a ** 3))}$.", f"Volume: ${V} \\cdot {ftex(F(b ** 3, a ** 3))} = {ftex(ans)}$."],
             "squaring the ratio (that's for area).")


@reg(S, "basics")
def si_model(r):
    k = r.choice([12, 18, 24, 25, 32, 48, 50, 64, 100])
    L = r.randint(3, 20) * k
    p = f"A model car is built at a scale of $1:{k}$. The real car is ${L}$ inches long. How long is the model, in inches?"
    return Q(p, F(L, k), [L * k, F(L, k) * 2, F(L, k) + 1, L - k, F(L, k * k)], "Every real inch becomes $\\frac{1}{" + str(k) + "}$ inch.",
             "the model's length.", "a $1:k$ scale divides every length by $k$.",
             [f"$\\frac{{{L}}}{{{k}}} = {ftex(F(L, k))}$ inches."], "multiplying by the scale.")


@reg(S, "basics")
def si_leg_segment(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    seg = F(a * a * k, c)
    p = f"A right triangle has legs ${a * k}$ and ${b * k}$. The altitude to the hypotenuse divides it into two pieces. How long is the piece next to the leg of length ${a * k}$?"
    return Q(p, seg, [F(b * b * k, c), F(a * b * k, c), F(c * k, 2), seg + 1, F(a * k, 2)], "Each leg squared equals the hypotenuse times the adjacent piece.",
             "the piece of the hypotenuse next to the leg " + str(a * k) + ".", "the small triangle and the whole triangle are similar: $\\text{leg}^2 = \\text{hypotenuse} \\times \\text{adjacent piece}$.",
             [f"Hypotenuse: ${c * k}$.", f"Piece: $\\frac{{{a * k}^2}}{{{c * k}}} = {ftex(seg)}$."], "using the other leg.")


@reg(S, "basics")
def si_midsegment(r):
    a, b, c = r.sample(range(6, 30), 3)
    if a + b <= c or a + c <= b or b + c <= a:
        return None
    p = f"Triangle $ABC$ has $AB = {a}$, $BC = {b}$, and $CA = {c}$. $M$ and $N$ are the midpoints of $AB$ and $AC$. What is $MN$?"
    return Q(p, F(b, 2), [b, F(a, 2), F(c, 2), F(a + c, 2), F(b, 3)], "The segment joining two midpoints is parallel to the third side.",
             "$MN$.", "the midsegment is parallel to the third side and half as long.",
             [f"$MN \\parallel BC$ and $MN = \\frac{{BC}}{{2}} = {ftex(F(b, 2))}$."], "halving the wrong side.")


@reg(S, "basics")
def si_rectangles(r):
    a, b = r.sample(range(2, 12), 2)
    if a > b:
        a, b = b, a
    k = F(r.randint(2, 6), r.choice([1, 2]))
    p = f"A ${a} \\times {b}$ rectangle is similar to a rectangle whose long side is ${ftex(b * k)}$. What is the short side of the second rectangle?"
    return Q(p, a * k, [a + b * k - b, b * k, a * k + 1, F(a * b, b * k) if F(a * b, b * k) != a * k else a * k + 2, a * k / 2], "Match long side to long side.",
             "the short side.", "similar rectangles have the same ratio of short side to long side.",
             [f"Scale: $\\frac{{{ftex(b * k)}}}{{{b}}} = {ftex(k)}$.", f"Short side: ${a} \\cdot {ftex(k)} = {ftex(a * k)}$."], "adding instead of multiplying.")


@reg(S, "basics")
def si_mirror(r):
    h = F(r.randint(10, 12), 2)
    d1 = r.randint(2, 6)
    d2 = r.randint(10, 60)
    H = h * d2 / d1
    if H.denominator > 2:
        return None
    n = r.choice(NAMES)
    p = f"{n}'s eyes are ${ftex(h)}$ feet above the ground. {n} stands ${d1}$ feet from a mirror lying on the ground and sees the top of a building that is ${d2}$ feet from the mirror on the other side. How tall is the building, in feet?"
    return Q(p, H, [h * d1 / d2, h + d2 - d1, H / 2, d2, H + h], "Light reflects at equal angles, making similar triangles.",
             "the building's height.", "the angle of incidence equals the angle of reflection, so the two right triangles are similar.",
             [f"$\\frac{{\\text{{height}}}}{{{d2}}} = \\frac{{{ftex(h)}}}{{{d1}}}$.", f"Height $= {d2} \\cdot \\frac{{{ftex(h)}}}{{{d1}}} = {ftex(H)}$ feet."],
             "flipping the ratio.")


@reg(S, "basics")
def si_photo(r):
    a, b = r.choice([(4, 6), (5, 7), (3, 5), (8, 10), (4, 5)])
    k = F(r.randint(2, 5), r.choice([1, 2]))
    p = f"A ${a} \\times {b}$ photo is enlarged so its short side becomes ${ftex(a * k)}$ inches. How long is the long side?"
    return Q(p, b * k, [b + a * k - a, a * k + (b - a), b * k * k, b * k + 1, b * a * k / a + 2], "Both sides scale by the same factor.",
             "the new long side.", "enlarging keeps the shape, so sides scale by the same factor.",
             [f"Scale: $\\frac{{{ftex(a * k)}}}{{{a}}} = {ftex(k)}$.", f"Long side: ${b} \\cdot {ftex(k)} = {ftex(b * k)}$."],
             "adding the same number of inches to each side.")


@reg(S, "basics")
def si_pentagon_area(r):
    P1, P2 = r.sample([10, 15, 20, 25, 30, 40, 45, 50, 60], 2)
    A1 = r.choice([16, 20, 24, 36, 40, 48, 50, 64, 80, 100])
    A2 = A1 * F(P2, P1) ** 2
    p = f"Two similar pentagons have perimeters ${P1}$ and ${P2}$. The first has area ${A1}$. What is the area of the second?"
    return Q(p, A2, [A1 * F(P2, P1), A2 + 1, A1 * F(P1, P2) ** 2, F(A1 * P2, P1) ** 2 / 10, A1 + P2 - P1], "Perimeter ratio is the side ratio.",
             "the second area.", "areas scale by the square of the length ratio.",
             [f"Length ratio: $\\frac{{{P2}}}{{{P1}}} = {ftex(F(P2, P1))}$.", f"Area: ${A1} \\cdot \\left({ftex(F(P2, P1))}\\right)^2 = {ftex(A2)}$."],
             "scaling the area by the perimeter ratio without squaring.")


@reg(S, "basics")
def si_medial(r):
    A = r.choice([24, 36, 40, 48, 60, 64, 80, 100, 120])
    p = f"Triangle $ABC$ has area ${A}$. What is the area of the triangle whose vertices are the midpoints of the sides of $ABC$?"
    return Q(p, F(A, 4), [F(A, 2), F(A, 3), F(A, 8), A, F(3 * A, 4)], "The midpoint triangle is similar with half the side lengths.",
             "the area of the midpoint triangle.", "each side of the midpoint triangle is half of a side of $ABC$, so the area is $\\left(\\frac{1}{2}\\right)^2 = \\frac{1}{4}$ as much.",
             [f"The three midsegments cut $ABC$ into $4$ congruent triangles.", f"Area: $\\frac{{{A}}}{{4}} = {ftex(F(A, 4))}$."], "halving the area.")


@reg(S, "basics")
def si_pyramid_section(r):
    B = r.choice([36, 48, 64, 72, 81, 100, 144])
    f = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4)])
    ans = B * f * f
    p = f"A pyramid has a base of area ${B}$. A plane parallel to the base cuts it ${ftex(f)}$ of the way down from the top. What is the area of the cross-section?"
    return Q(p, ans, [B * f, B * (1 - f) ** 2, ans + 1, B - ans, B * f * f * f], "The cut makes a smaller similar pyramid on top.",
             "the cross-section's area.", "the small pyramid on top is similar with ratio " + ftex(f) + ", so areas scale by " + ftex(f * f) + ".",
             [f"Length ratio: ${ftex(f)}$. Area ratio: ${ftex(f * f)}$.", f"Area: ${B} \\cdot {ftex(f * f)} = {ftex(ans)}$."], "scaling area by the length ratio.")


@reg(S, "basics")
def si_right_scale(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(2, 6)
    p = f"A right triangle has legs ${a}$ and ${b}$. A similar triangle has hypotenuse ${c * k}$. What is the sum of its legs?"
    return Q(p, (a + b) * k, [a + b + c * k - c, c * k, (a + b) * k + 1, a * b * k, (a + b) * k * k], "Find the hypotenuse of the first triangle.",
             "the sum of the second triangle's legs.", "find the scale factor from the hypotenuses.",
             [f"First hypotenuse: $\\sqrt{{{a}^2 + {b}^2}} = {c}$.", f"Scale: $\\frac{{{c * k}}}{{{c}}} = {k}$.", f"Legs: ${a * k}$ and ${b * k}$; sum ${(a + b) * k}$."],
             "adding instead of scaling.")


@reg(S, "basics")
def si_transversals(r):
    a, b = r.sample(range(2, 10), 2)
    k = F(r.randint(3, 9), 2)
    p = f"Three parallel lines cut two transversals. On the first transversal they cut segments of ${a}$ and ${b}$. On the second, the segment matching the ${a}$ is ${ftex(a * k)}$. How long is the segment matching the ${b}$?"
    return Q(p, b * k, [b + a * k - a, a * k * F(a, b), b * k + 1, b, F(b, k)], "Parallel lines cut transversals proportionally.",
             "the matching segment.", "parallel lines divide any two transversals in the same ratio.",
             [f"Ratio: $\\frac{{{ftex(a * k)}}}{{{a}}} = {ftex(k)}$.", f"Segment: ${b} \\cdot {ftex(k)} = {ftex(b * k)}$."], "adding the difference instead of multiplying.")


@reg(S, "basics")
def si_cone_fill(r):
    f = r.choice([F(1, 2), F(1, 3), F(2, 3), F(3, 4), F(1, 4)])
    V = r.choice([64, 81, 108, 128, 216, 256])
    ans = V * f ** 3
    p = f"A cone-shaped cup (point down) holds ${V}$ mL when full. It is filled to ${ftex(f)}$ of its height. How many mL of water are in it?"
    return Q(p, ans, [V * f, V * f * f, ans * 2, V - ans, V * (1 - f) ** 3], "The water forms a smaller similar cone.",
             "the water volume.", "the water is a cone similar to the cup with ratio " + ftex(f) + "; volumes scale by the cube.",
             [f"Volume ratio: $\\left({ftex(f)}\\right)^3 = {ftex(f ** 3)}$.", f"Water: ${V} \\cdot {ftex(f ** 3)} = {ftex(ans)}$ mL."], "using the height fraction directly.")


@reg(S, "basics")
def si_perimeter_split(r):
    a, b, c = r.sample(range(2, 10), 3)
    k = r.randint(2, 6)
    P = (a + b + c) * k
    p = f"The sides of a triangle are in the ratio ${a}:{b}:{c}$, and its perimeter is ${P}$. What is its longest side?"
    return Q(p, max(a, b, c) * k, [min(a, b, c) * k, P // 3, max(a, b, c), max(a, b, c) * k + 1, (max(a, b, c) + 1) * k], "Each ratio part is the same length.",
             "the longest side.", "split the perimeter into " + str(a + b + c) + " equal parts.",
             [f"One part: $\\frac{{{P}}}{{{a + b + c}}} = {k}$.", f"Longest: ${max(a, b, c)} \\cdot {k} = {max(a, b, c) * k}$."], "answering the shortest side.")


@reg(S, "challenge")
def sic_poles(r):
    a, b = r.choice([(3, 6), (4, 12), (6, 12), (10, 15), (12, 24), (5, 20), (6, 18), (8, 24), (3, 7)])
    d = r.randint(5, 40)
    h = F(a * b, a + b)
    p = f"Two vertical poles of heights ${a}$ and ${b}$ stand ${d}$ feet apart. A wire runs from the top of each pole to the bottom of the other. How high above the ground do the wires cross?"
    return Q(p, h, [F(a + b, 2), F(a * b, d), h + 1, F(a * b, b - a) if b != a else 3, F(d, 2)], "The distance between the poles doesn't matter.",
             "the crossing height.", "similar triangles give $\\frac{1}{h} = \\frac{1}{a} + \\frac{1}{b}$.",
             [f"If the crossing is at height $h$, then $\\frac{{h}}{{{a}}} + \\frac{{h}}{{{b}}} = 1$ (the two fractions of the ground distance add to the whole).",
              f"$h\\left(\\frac{{1}}{{{a}}} + \\frac{{1}}{{{b}}}\\right) = 1$, so $h = \\frac{{{a} \\cdot {b}}}{{{a} + {b}}} = {ftex(h)}$."],
             "averaging the heights.")


@reg(S, "challenge")
def sic_trap_diag(r):
    a, b = r.sample(range(2, 12), 2)
    if a > b:
        a, b = b, a
    A_total = (a + b) ** 2
    small = a * a
    p = f"Trapezoid $ABCD$ has bases $AB = {a}$ and $CD = {b}$, and its diagonals meet at $E$. The trapezoid's area is ${A_total}$. What is the area of triangle $ABE$?"
    return Q(p, small, [b * b, a * b, F(A_total * a, a + b), small + a, F(A_total, 4)], "Triangles $ABE$ and $CDE$ are similar.",
             "the area of triangle $ABE$.", "triangles $ABE$ and $CDE$ are similar with ratio $a : b$; the two side triangles each have area proportional to $ab$.",
             [f"The four triangles have areas in the ratio $a^2 : ab : ab : b^2 = {a * a} : {a * b} : {a * b} : {b * b}$, adding to $(a + b)^2 = {A_total}$ parts.",
              f"Triangle $ABE$ is $\\frac{{{a * a}}}{{{A_total}}}$ of the trapezoid: $\\frac{{{a * a}}}{{{A_total}}} \\cdot {A_total} = {small}$."],
             "splitting the area evenly among the four triangles.")


@reg(S, "challenge")
def sic_equal_area(r):
    L = r.randint(4, 20)
    ans = rad(F(L, 2), 2)
    p = f"In triangle $ABC$, $AB = {L}$. A line parallel to $BC$ meets $AB$ at $D$ and cuts the triangle into two pieces of equal area. What is $AD$?"
    return Q(p, ans, [num(F(L, 2)), rad(F(L, 3), 3), num(F(3 * L, 4)), rad(F(L, 4), 2), num(L - 1)], "Triangle $ADE$ has half the area of $ABC$.",
             "$AD$.", "the small triangle $ADE$ is similar to $ABC$; half the area means a length ratio of $\\frac{1}{\\sqrt{2}}$.",
             ["Area ratio $\\frac{1}{2}$, so length ratio $\\sqrt{\\frac{1}{2}} = \\frac{\\sqrt{2}}{2}$.", f"$AD = {L} \\cdot \\frac{{\\sqrt{{2}}}}{{2}} = {ans.tex}$."], "using half of $AB$.")


@reg(S, "challenge")
def sic_square_in_triangle(r):
    b, h = r.sample([4, 6, 8, 10, 12, 15, 20, 24], 2)
    s = F(b * h, b + h)
    p = f"A square sits inside a triangle with one side on the triangle's base. The base is ${b}$ and the height to it is ${h}$. The square's top corners touch the other two sides. What is the square's side?"
    return Q(p, s, [F(b + h, 4), F(b, 2), F(h, 2), s + 1, F(b * h, 2 * (b + h))], "The triangle above the square is similar to the whole triangle.",
             "the side $s$.", "the small triangle above the square has base $s$ and height $h - s$, similar to the big one.",
             [f"$\\frac{{s}}{{{b}}} = \\frac{{{h} - s}}{{{h}}}$.", f"${h}s = {b}({h} - s)$, so ${b + h}s = {b * h}$.", f"$s = {ftex(s)}$."],
             "setting the square's side to half the base.")


@reg(S, "challenge")
def sic_trap_harmonic(r):
    a, b = r.sample([2, 3, 4, 6, 8, 10, 12, 15, 20], 2)
    L = F(2 * a * b, a + b)
    p = f"A trapezoid has bases ${a}$ and ${b}$. A segment parallel to the bases passes through the point where the diagonals cross, with its ends on the legs. How long is it?"
    return Q(p, L, [F(a + b, 2), F(a * b, a + b), L + 1, rad(1, a * b) if math.isqrt(a * b) ** 2 != a * b else num(math.isqrt(a * b) + 1), max(a, b)], "Each half of the segment comes from similar triangles.",
             "the segment's length.", "the segment is the harmonic mean of the bases: $\\frac{2ab}{a + b}$.",
             [f"The diagonals split each other in the ratio ${a}:{b}$.", f"Each half of the segment is $\\frac{{ab}}{{a + b}} = {ftex(F(a * b, a + b))}$ by similar triangles.", f"Total: ${ftex(L)}$."],
             "taking the average of the bases (that's the midsegment, which is different).")


@reg(S, "challenge")
def sic_antiparallel(r):
    AD, AE = r.randint(2, 9), r.randint(2, 9)
    AB = r.randint(max(AD, AE) + 1, 20)
    AC = F(AD * AB, AE)
    if AC <= AE or AC.denominator > 4:
        return None
    p = f"In triangle $ABC$, points $D$ on $AB$ and $E$ on $AC$ satisfy $\\angle ADE = \\angle ACB$. If $AD = {AD}$, $AE = {AE}$, and $AB = {AB}$, what is $AC$?"
    return Q(p, AC, [F(AE * AB, AD), AB - AD + AE, AC + 1, F(AD * AE, AB), AB], "Triangle $ADE$ is similar to triangle $ACB$, not $ABC$.",
             "$AC$.", "matching angles: $\\angle A$ is shared and $\\angle ADE = \\angle ACB$, so $ADE \\sim ACB$.",
             ["Corresponding sides: $AD \\leftrightarrow AC$ and $AE \\leftrightarrow AB$.", f"$\\frac{{AD}}{{AC}} = \\frac{{AE}}{{AB}}$, so $AD \\cdot AB = AE \\cdot AC$.", f"$AC = \\frac{{{AD} \\cdot {AB}}}{{{AE}}} = {ftex(AC)}$."],
             "matching $D$ with $B$ as if $DE$ were parallel to $BC$.")


@reg(S, "challenge")
def sic_alt_areas(r):
    a, b, c = r.choice(TRIPLES)
    ans = F(a * a, b * b)
    p = f"A right triangle has legs ${a}$ and ${b}$. The altitude to the hypotenuse splits it into two smaller triangles. What is the ratio of the smaller triangle's area to the larger one's?"
    return Q(p, ans, [F(a, b), F(a, c), F(a * a, c * c), 1 / ans, F(b, c)], "Both small triangles are similar to the original.",
             "the area ratio.", "the two pieces are similar to each other with ratio $a : b$ (their hypotenuses are the legs).",
             [f"Hypotenuses of the small triangles: ${a}$ and ${b}$.", f"Area ratio $= \\left(\\frac{{{a}}}{{{b}}}\\right)^2 = {ftex(ans)}$."],
             "using $\\frac{a}{b}$ without squaring.")
