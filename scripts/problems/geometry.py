"""Geometry unit: original problems modeled on AMC 10/12 problem types."""
import math
from fractions import Fraction as F

from common import Bank, C, explain, num, sqrt_form, simplify_sqrt
from geometry_more1 import MORE as M1
from geometry_more2 import MORE as M2

MORE = {**M1, **M2}

banks = []


def bank(skill_id):
    b = Bank(skill_id)
    banks.append(b)
    return b


def pi_form(k):
    """k*pi as a choice (k int or Fraction)."""
    k = F(k)
    if k == 1:
        t = "\\pi"
    elif k.denominator == 1:
        t = f"{k.numerator}\\pi"
    else:
        t = f"\\frac{{{k.numerator}\\pi}}{{{k.denominator}}}"
    return C(t, float(k) * math.pi)


def coef_root(k, rad):
    """k * sqrt(rad) as a simplified choice, with k a Fraction."""
    k = F(k)
    a, b2 = simplify_sqrt(rad)
    k = k * a
    r_ = "" if b2 == 1 else f"\\sqrt{{{b2}}}"
    if k.denominator == 1:
        t = (f"{k.numerator}" if k.numerator != 1 or not r_ else "") + r_
    else:
        t = f"\\frac{{{(str(k.numerator) if k.numerator != 1 or not r_ else '') + r_}}}{{{k.denominator}}}"
    return C(t, float(k) * math.sqrt(b2))


def over_pi(k):
    """k / pi as a simplified choice."""
    k = F(k)
    t = f"\\frac{{{k.numerator}}}{{\\pi}}" if k.denominator == 1 else f"\\frac{{{k.numerator}}}{{{k.denominator}\\pi}}"
    return C(t, float(k) / math.pi)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


# ---------------------------------------------------------------- angles and polygons
b = bank("geo_angles")


def an1(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    ask = r.choice(["interior", "exterior", "sum"])
    interior = F(180 * (n - 2), n)
    ans = {"interior": interior, "exterior": F(360, n), "sum": 180 * (n - 2)}[ask]
    words = {"interior": "each interior angle", "exterior": "each exterior angle", "sum": "the sum of the interior angles"}[ask]
    p = f"What is the measure, in degrees, of {words} of a regular polygon with {n} sides?"
    steps = [f"A polygon with ${n}$ sides splits into ${n} - 2 = {n - 2}$ triangles from one corner, so its interior angles add to $180 \\cdot {n - 2} = {180 * (n - 2)}$ degrees."]
    if ask == "interior":
        steps.append(f"In a regular polygon all ${n}$ angles are equal: $\\frac{{{180 * (n - 2)}}}{{{n}}} = {num(interior).tex}$ degrees.")
    elif ask == "exterior":
        steps = [f"Walking around any convex polygon you turn a full $360^\\circ$, so the exterior angles add to $360^\\circ$.",
                 f"In a regular polygon they are equal: $\\frac{{360}}{{{n}}} = {num(F(360, n)).tex}$ degrees."]
    sol = explain(f"{words} of a regular ${n}$-gon.", "interior angles of an $n$-gon add to $180(n - 2)$; exterior angles always add to $360^\\circ$.", steps, f"${num(F(ans)).tex}$.",
                  "using $180n$ for the interior sum, or mixing up interior and exterior angles. They add to $180^\\circ$ at each corner.")
    return (p, ans, [interior, F(360, n), 180 * (n - 2), 180 * n, F(180 * (n - 1), n), 180 * (n - 2) + 180],
            ["The interior angles of an $n$-gon add to $180(n - 2)$ degrees, and the exterior angles add to $360$."], sol)


def an2(r):
    a, bb = r.randint(25, 80), r.randint(25, 80)
    if a + bb >= 170:
        return None
    p = (f"In triangle $ABC$, $\\angle A = {a}^\\circ$ and $\\angle B = {bb}^\\circ$. Side $BC$ is extended past $C$ to point $D$. "
         f"What is $\\angle ACD$, in degrees?")
    sol = explain(
        "the exterior angle at $C$.",
        "the exterior angle and the interior angle at $C$ form a straight line, so they add to $180^\\circ$.",
        [
            f"Interior angle at $C$: $180 - {a} - {bb} = {180 - a - bb}^\\circ$.",
            f"Exterior angle: $180 - {180 - a - bb} = {a + bb}^\\circ$.",
            f"Shortcut: an exterior angle always equals the sum of the two far interior angles, ${a} + {bb} = {a + bb}$.",
        ],
        f"${a + bb}^\\circ$.",
        f"giving the interior angle ${180 - a - bb}^\\circ$ instead of the exterior one.",
    )
    return (p, a + bb, [180 - a - bb, 180 - a, 180 - bb, abs(a - bb), 90 + a // 2], ["An exterior angle of a triangle equals the sum of the two remote interior angles."], sol)


def an3(r):
    top = r.randint(20, 100)
    if top % 2:
        return None
    base = (180 - top) // 2
    ask = r.choice(["base", "top"])
    if ask == "base":
        p = f"An isosceles triangle has a vertex angle (between the two equal sides) of ${top}^\\circ$. What is the measure of each base angle, in degrees?"
        ans = base
        steps = [f"The two base angles are equal; call each $x$.", f"$x + x + {top} = 180$, so $2x = {180 - top}$ and $x = {base}$."]
        trap = f"subtracting ${top}$ from $180$ and forgetting to split the result between two angles."
    else:
        p = f"Each base angle of an isosceles triangle measures ${base}^\\circ$. What is the vertex angle, in degrees?"
        ans = top
        steps = ["Both base angles are " + f"${base}^\\circ$.", f"Vertex angle: $180 - {base} - {base} = {top}$."]
        trap = f"subtracting only one base angle, which gives ${180 - base}$."
    sol = explain("the missing angle of the isosceles triangle.", "the angles opposite the equal sides (the base angles) are equal, and all three angles add to $180^\\circ$.", steps, f"${ans}^\\circ$.", trap)
    return (p, ans, [180 - top, 90 - top // 2 + 10, top, base, 180 - 2 * top if top < 90 else 45, base + 10], ["The two base angles are equal and the three angles add to $180^\\circ$."], sol)


def an4(r):
    a, k = r.randint(2, 5), r.randint(5, 40)
    x = r.randint(10, 30)
    ang1 = a * x + k
    ang2 = 180 - ang1
    if ang2 <= 10:
        return None
    bb = r.randint(1, 4)
    m = ang2 - bb * x
    e2 = f"{bb if bb > 1 else ''}x {'+' if m >= 0 else '-'} {abs(m)}"
    p = (f"Two parallel lines are cut by a transversal, forming same-side interior angles that measure $({a}x + {k})^\\circ$ "
         f"and $({e2})^\\circ$. What is $x$?")
    sol = explain(
        "the value of $x$.",
        "when a transversal crosses parallel lines, same-side interior angles (between the parallels, on the same side of the transversal) add to $180^\\circ$.",
        [
            f"$({a}x + {k}) + ({e2}) = 180$.",
            f"Combine: ${a + bb}x + {k + m} = 180$, so ${a + bb}x = {180 - k - m}$ and $x = {x}$.",
            f"Check: the angles are ${ang1}^\\circ$ and ${ang2}^\\circ$, which add to $180^\\circ$.",
        ],
        f"$x = {x}$.",
        "setting the two angles equal. Equal angles come from alternate or corresponding pairs, not same-side pairs.",
    )
    return (p, x, [x + 5, x - 3, F(180 - k - m, a + bb) + 2, ang1, (180 - k) // a], ["Same-side interior angles add to $180^\\circ$."], sol)


def anc1(r):
    A = r.choice(range(30, 121, 2))
    half = (180 - A) // 2
    ans = 90 + A // 2
    p = f"In triangle $ABC$, $\\angle A = {A}^\\circ$. The bisectors of angles $B$ and $C$ meet at point $I$. What is $\\angle BIC$, in degrees?"
    sol = explain(
        "the angle at $I$ in triangle $BIC$.",
        "we don't know $\\angle B$ and $\\angle C$ separately, but we know their sum, and the bisectors take half of each.",
        [
            f"$\\angle B + \\angle C = 180 - {A} = {180 - A}$.",
            f"$\\angle IBC + \\angle ICB = \\frac{{1}}{{2}}(\\angle B + \\angle C) = {half}$.",
            f"In triangle $BIC$: $\\angle BIC = 180 - {half} = {ans}$.",
            f"(General fact: $\\angle BIC = 90 + \\frac{{\\angle A}}{{2}}$.)",
        ],
        f"${ans}^\\circ$.",
        f"answering $180 - {A} = {180 - A}$, which forgets that the bisectors only take half of each angle.",
    )
    return (p, ans, [180 - A, 90 - A // 2, A * 2 if A < 90 else 120, 180 - A // 2, 90 + A], ["$\\angle B + \\angle C = 180 - \\angle A$, and $I$ splits each of those angles in half."], sol)


def anc2(r):
    k = r.choice([2, 3, 4, 5, 7, 8, 9, 11])
    n = 2 * (k + 1)
    e = F(180, k + 1)
    p = f"Each interior angle of a regular polygon is {k} times as large as each exterior angle. How many sides does the polygon have?"
    sol = explain(
        "the number of sides.",
        "at each corner the interior and exterior angles form a straight line ($180^\\circ$), and the exterior angles add to $360^\\circ$.",
        [
            f"Let the exterior angle be $e$. Then the interior angle is ${k}e$, and $e + {k}e = 180$.",
            f"So ${k + 1}e = 180$ and $e = {num(e).tex}$.",
            f"Number of sides: $\\frac{{360}}{{{num(e).tex}}} = {n}$.",
        ],
        f"${n}$ sides.",
        f"dividing $360$ by the interior angle instead of the exterior angle.",
    )
    return (p, n, [n + 2, n - 2, k + 2, 2 * k, n + 4], ["Interior plus exterior is $180^\\circ$, and the exterior angles add to $360^\\circ$."], sol)


def anc3(r):
    h, m = r.randint(1, 12), r.choice(range(0, 60, 2))
    ang = abs(F(60 * h - 11 * m, 2)) % 360
    if ang > 180:
        ang = 360 - ang
    if ang == 0:
        return None
    hour = 30 * (h % 12) + F(m, 2)
    diff = abs(hour - 6 * m)
    p = f"What is the smaller angle, in degrees, between the hour hand and the minute hand of a clock at {h}:{m:02d}?"
    sol = explain(
        "the smaller angle between the hands.",
        "measure each hand's angle from 12 o'clock. The minute hand moves $6^\\circ$ per minute. The hour hand moves $30^\\circ$ per hour, plus $0.5^\\circ$ per minute.",
        [
            f"Minute hand: ${m} \\cdot 6 = {6 * m}^\\circ$.",
            f"Hour hand: ${h % 12} \\cdot 30 + {m} \\cdot 0.5 = {30 * (h % 12)} + {num(F(m, 2)).tex} = {num(hour).tex}^\\circ$.",
            f"Difference: $|{num(hour).tex} - {6 * m}| = {num(diff).tex}^\\circ$." + (f" That is more than $180^\\circ$, so the smaller angle is $360 - {num(diff).tex} = {num(ang).tex}^\\circ$." if diff > 180 else ""),
        ],
        f"${num(ang).tex}^\\circ$.",
        "keeping the hour hand fixed on the hour mark. It moves as the minutes pass.",
    )
    wrong0 = abs(30 * h - 6 * m) % 360
    return (p, ang, [wrong0 if wrong0 <= 180 else 360 - wrong0, ang + 5, 360 - ang, ang - F(m, 2), ang + 30], ["The hour hand moves $0.5^\\circ$ per minute and the minute hand moves $6^\\circ$ per minute."], sol)


b.fill_unique("basics", [an1, an2, an3, an4] + MORE[b.skill_id]["basics"], 1101)
b.fill_unique("challenge", [anc1, anc2, anc3] + MORE[b.skill_id]["challenge"], 1102)


# ---------------------------------------------------------------- right triangles
b = bank("geo_right")


def rt1(r):
    a, bb, c = r.choice(TRIPLES)
    k = r.randint(1, 4)
    a, bb, c = a * k, bb * k, c * k
    ask = r.choice(["hyp", "leg"])
    if ask == "hyp":
        p = f"A right triangle has legs of length ${a}$ and ${bb}$. What is the length of the hypotenuse?"
        sol = explain("the hypotenuse $c$.", "Pythagorean Theorem: $a^2 + b^2 = c^2$, where $c$ is across from the right angle.",
                      [f"$c^2 = {a}^2 + {bb}^2 = {a * a} + {bb * bb} = {c * c}$.", f"$c = \\sqrt{{{c * c}}} = {c}$."] + ([f"(This is the ${a // k}$-${bb // k}$-${c // k}$ triple scaled by ${k}$.)"] if k > 1 else []),
                      f"${c}$.", f"adding the legs, ${a} + {bb} = {a + bb}$. Side lengths don't add; their squares do.")
        return (p, c, [a + bb, c + 1, c - 1, max(a, bb) + 2, (a + bb) // 2 + 3], ["Use the Pythagorean Theorem."], sol)
    p = f"A right triangle has hypotenuse ${c}$ and one leg ${a}$. What is the other leg?"
    sol = explain("the missing leg $b$.", "Pythagorean Theorem: $a^2 + b^2 = c^2$, so $b^2 = c^2 - a^2$.",
                  [f"$b^2 = {c}^2 - {a}^2 = {c * c} - {a * a} = {bb * bb}$.", f"$b = {bb}$."], f"${bb}$.", f"subtracting the lengths, ${c} - {a} = {c - a}$.")
    return (p, bb, [c - a, bb + 1, bb - 1, c + a - bb, (c + a) // 2], ["Use the Pythagorean Theorem."], sol)


def rt2(r):
    s = r.randint(2, 15)
    kind = r.choice(["45", "30"])
    if kind == "45":
        p = f"An isosceles right triangle has legs of length ${s}$. What is the length of its hypotenuse?"
        sol = explain("the hypotenuse.", "an isosceles right triangle is a $45$-$45$-$90$ triangle; its sides are in the ratio $1 : 1 : \\sqrt{2}$.",
                      [f"Pythagorean check: $c^2 = {s}^2 + {s}^2 = {2 * s * s}$, so $c = \\sqrt{{{2 * s * s}}} = {s}\\sqrt{{2}}$."], f"${s}\\sqrt{{2}}$.", f"doubling the leg (${2 * s}$).")
        return (p, sqrt_form(s, 2), [C(str(2 * s), 2 * s), sqrt_form(s, 3), C(str(s), s), sqrt_form(2 * s, 2), sqrt_form(s + 1, 2)], ["In a $45$-$45$-$90$ triangle the hypotenuse is $\\sqrt{2}$ times a leg."], sol)
    p = f"In a $30$-$60$-$90$ triangle, the side opposite the $30^\\circ$ angle has length ${s}$. What is the length of the side opposite the $60^\\circ$ angle?"
    sol = explain("the longer leg.", "a $30$-$60$-$90$ triangle has sides in the ratio $1 : \\sqrt{3} : 2$ (opposite $30^\\circ$, $60^\\circ$, $90^\\circ$).",
                  [f"The short leg is ${s}$, so the hypotenuse is $2 \\cdot {s} = {2 * s}$.", f"The long leg is $\\sqrt{{3}}$ times the short leg: ${s}\\sqrt{{3}}$. (Check: ${s}^2 + 3 \\cdot {s}^2 = {4 * s * s} = ({2 * s})^2$.)"],
                  f"${s}\\sqrt{{3}}$.", f"giving the hypotenuse ${2 * s}$ instead of the leg.")
    return (p, sqrt_form(s, 3), [C(str(2 * s), 2 * s), sqrt_form(s, 2), sqrt_form(2 * s, 3), C(str(s), s), sqrt_form(s + 1, 3)], ["The sides of a $30$-$60$-$90$ triangle are in the ratio $1 : \\sqrt{3} : 2$."], sol)


def rt3(r):
    a, bb, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    ans = a * bb * k * k
    p = f"A rectangle has a diagonal of length ${c * k}$ and one side of length ${a * k}$. What is its area?"
    sol = explain("the area, which needs both sides.", "the diagonal splits the rectangle into two right triangles, with the diagonal as hypotenuse.",
                  [f"Other side: $\\sqrt{{{c * k}^2 - {a * k}^2}} = \\sqrt{{{(c * k) ** 2 - (a * k) ** 2}}} = {bb * k}$.", f"Area: ${a * k} \\cdot {bb * k} = {ans}$."],
                  f"${ans}$.", f"multiplying the side by the diagonal (${a * k} \\cdot {c * k}$). The diagonal is not a side.")
    return (p, ans, [c * k * a * k, (a + bb) * k * 2, ans // 2, ans + a * k, (c * k) ** 2 // 2], ["Find the other side with the Pythagorean Theorem."], sol)


def rt4(r):
    a, bb, c = r.choice(TRIPLES[:4])
    k = r.randint(1, 5)
    n1, e1 = r.randint(1, a * k - 1), r.randint(1, bb * k - 1)
    p = (f"Starting from home, a hiker walks {n1} miles north, {e1} miles east, {a * k - n1} miles north, and {bb * k - e1} miles east. "
         f"How far is the hiker from home, in miles, in a straight line?")
    sol = explain("the straight line distance from start to finish.", "only the total north and total east movements matter; they are the legs of a right triangle.",
                  [f"Total north: ${n1} + {a * k - n1} = {a * k}$. Total east: ${e1} + {bb * k - e1} = {bb * k}$.", f"Distance: $\\sqrt{{{a * k}^2 + {bb * k}^2}} = \\sqrt{{{(a * k) ** 2 + (bb * k) ** 2}}} = {c * k}$."],
                  f"${c * k}$ miles.", f"adding all the walking (${(a + bb) * k}$ miles), which is the path length, not the straight line distance.")
    return (p, c * k, [(a + bb) * k, c * k + 1, c * k - 2, a * k + 1, bb * k + 2], ["Add up the total north and the total east distances."], sol)


def rtc1(r):
    a, bb, c = r.choice(TRIPLES[:4])
    k = r.randint(1, 3)
    a, bb, c = a * k, bb * k, c * k
    h = F(a * bb, c)
    p = f"A right triangle has legs ${a}$ and ${bb}$. What is the length of the altitude to the hypotenuse?"
    sol = explain("the height $h$ drawn from the right angle to the hypotenuse.", "compute the area two ways: legs as base and height, or hypotenuse as base and $h$ as height.",
                  [f"Hypotenuse: $\\sqrt{{{a}^2 + {bb}^2}} = {c}$.", f"Area using the legs: $\\frac{{{a} \\cdot {bb}}}{{2}} = {num(F(a * bb, 2)).tex}$.",
                   f"Area using the hypotenuse: $\\frac{{{c} \\cdot h}}{{2}}$. Set them equal: ${c}h = {a * bb}$, so $h = {num(h).tex}$."],
                  f"${num(h).tex}$.", "taking the altitude to be half the hypotenuse, which is the distance to the hypotenuse's midpoint, not the perpendicular distance.")
    return (p, h, [F(a + bb, 2), F(c, 2), F(a * bb, 2), h + 1, F(a * a, c)], ["Compute the area two ways: with the legs, and with the hypotenuse as the base."], sol)


def rtc2(r):
    s = r.randint(2, 12)
    ans = coef_root(F(s * s, 4), 3)
    wrong = [coef_root(F(s * s, 2), 3), C(str(s * s), s * s), coef_root(s * s, 3), coef_root(F(s * s, 4), 2), coef_root(F(s * s, 3), 3)]
    p = f"What is the area of an equilateral triangle with side length ${s}$?"
    sol = explain("the area, which needs the height.", "an altitude of an equilateral triangle cuts it into two $30$-$60$-$90$ triangles.",
                  [f"The altitude splits the base into halves of ${num(F(s, 2)).tex}$. The altitude is the long leg: ${num(F(s, 2)).tex}\\sqrt{{3}}$.",
                   f"Area: $\\frac{{1}}{{2}} \\cdot {s} \\cdot \\frac{{{s}\\sqrt{{3}}}}{{2}} = \\frac{{{s * s}\\sqrt{{3}}}}{{4}} = {ans.tex}$.", "(General formula: $\\frac{\\sqrt{3}}{4}s^2$.)"],
                  f"${ans.tex}$.", "forgetting the $\\frac{1}{2}$ in the triangle area formula.")
    return (p, ans, wrong, ["Drop an altitude: it splits the triangle into two $30$-$60$-$90$ triangles."], sol)


def rtc3(r):
    combos = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (2, 10, 11, 15), (3, 4, 12, 13),
              (8, 9, 12, 17), (2, 5, 14, 15), (4, 5, 20, 21), (6, 10, 15, 19)]
    a, bb, c, d = r.choice(combos)
    k = r.randint(1, 3)
    A, B, Cc, D = a * k, bb * k, c * k, d * k
    p = f"A rectangular box measures ${A}$ by ${B}$ by ${Cc}$. What is the length of the longest segment that fits inside the box (from one corner to the opposite corner)?"
    sol = explain("the space diagonal of the box.", "use the Pythagorean Theorem twice: first across the bottom face, then up to the far top corner.",
                  [f"Bottom diagonal: $\\sqrt{{{A}^2 + {B}^2}} = \\sqrt{{{A * A + B * B}}}$.", f"That diagonal and the height ${Cc}$ form a right triangle: $\\sqrt{{{A * A + B * B} + {Cc * Cc}}} = \\sqrt{{{D * D}}} = {D}$.",
                   "(In one formula: $\\sqrt{a^2 + b^2 + c^2}$.)"],
                  f"${D}$.", "using only a face diagonal, which is shorter.")
    return (p, D, [(a + bb + c) * k, D + 1, D - 1, Cc + 1, (a + bb) * k], ["The space diagonal is $\\sqrt{a^2 + b^2 + c^2}$."], sol)


b.fill_unique("basics", [rt1, rt2, rt3, rt4] + MORE[b.skill_id]["basics"], 1201)
b.fill_unique("challenge", [rtc1, rtc2, rtc3] + MORE[b.skill_id]["challenge"], 1202)


# ---------------------------------------------------------------- similar triangles
b = bank("geo_similar")


def si1(r):
    a, bb, c = r.randint(3, 12), r.randint(3, 12), r.randint(3, 12)
    if a + bb <= c or a + c <= bb or bb + c <= a:
        return None
    k = F(r.randint(2, 5), r.choice([1, 1, 2]))
    if (a * k).denominator != 1:
        return None
    ans = (a + bb + c) * k
    p = (f"Triangle $ABC$ has sides $AB = {a}$, $BC = {bb}$, $CA = {c}$. Triangle $DEF$ is similar to it with $DE = {a * k}$ "
         f"($DE$ corresponds to $AB$). What is the perimeter of $DEF$?")
    sol = explain("the perimeter of the larger (or smaller) similar triangle.", "in similar triangles every length is multiplied by the same scale factor, so the perimeter is too.",
                  [f"Scale factor: $\\frac{{DE}}{{AB}} = \\frac{{{a * k}}}{{{a}}} = {num(k).tex}$.", f"Perimeter of $ABC$: ${a} + {bb} + {c} = {a + bb + c}$.", f"Perimeter of $DEF$: ${a + bb + c} \\cdot {num(k).tex} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "squaring the scale factor. That is for areas, not lengths.")
    return (p, ans, [a + bb + c, ans + a, (a + bb + c) * k * k, ans - c, ans + 1], ["All sides scale by the same factor."], sol)


def si2(r):
    h1, s1 = r.randint(4, 7), r.randint(2, 9)
    k = r.randint(3, 12)
    p = f"A {h1}-foot post casts a shadow {s1} feet long. At the same time, a tree casts a shadow {s1 * k} feet long. How tall is the tree, in feet?"
    sol = explain("the tree's height $t$.", "at the same moment the sun's rays hit at the same angle, so object and shadow form similar right triangles.",
                  [f"Height to shadow is the same ratio for both: $\\frac{{t}}{{{s1 * k}}} = \\frac{{{h1}}}{{{s1}}}$.", f"Multiply: $t = {s1 * k} \\cdot \\frac{{{h1}}}{{{s1}}} = {h1 * k}$."],
                  f"${h1 * k}$ feet.", "flipping the ratio (shadow over height on one side, height over shadow on the other).")
    return (p, h1 * k, [s1 * h1, h1 * k + s1, s1 * k + h1, h1 + s1 * k - s1, F(s1 * k * s1, h1)], ["The post and its shadow form a triangle similar to the tree and its shadow."], sol)


def si3(r):
    a, bb = r.randint(1, 5), r.randint(2, 7)
    if a >= bb or math.gcd(a, bb) != 1:
        return None
    A = r.randint(2, 20) * bb * bb
    ans = F(A * a * a, bb * bb)
    p = f"Two similar triangles have corresponding sides in the ratio ${a}:{bb}$. The larger triangle has area ${A}$. What is the area of the smaller triangle?"
    sol = explain("the smaller triangle's area.", "if lengths scale by $k$, areas scale by $k^2$ (area uses two lengths multiplied together).",
                  [f"Length ratio $k = \\frac{{{a}}}{{{bb}}}$.", f"Area ratio $k^2 = \\frac{{{a * a}}}{{{bb * bb}}}$.", f"Smaller area: ${A} \\cdot \\frac{{{a * a}}}{{{bb * bb}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"using the side ratio directly, which gives ${num(F(A * a, bb)).tex}$.")
    return (p, ans, [F(A * a, bb), F(A * a ** 3, bb ** 3), ans * 2, A - ans, ans + a], ["Areas scale by the square of the side ratio."], sol)


def si4(r):
    AD, DB = r.randint(2, 9), r.randint(2, 9)
    BC = (AD + DB) * r.randint(1, 4)
    DE = F(AD * BC, AD + DB)
    p = f"In triangle $ABC$, point $D$ is on $AB$ and $E$ is on $AC$ with $DE \\parallel BC$. If $AD = {AD}$, $DB = {DB}$, and $BC = {BC}$, what is $DE$?"
    sol = explain("the length of $DE$.", "a segment parallel to one side cuts off a smaller triangle similar to the whole triangle ($ADE \\sim ABC$).",
                  [f"Matching sides: $AD$ goes with $AB = {AD} + {DB} = {AD + DB}$, and $DE$ goes with $BC$.", f"$\\frac{{DE}}{{{BC}}} = \\frac{{{AD}}}{{{AD + DB}}}$, so $DE = {BC} \\cdot \\frac{{{AD}}}{{{AD + DB}}} = {num(DE).tex}$."],
                  f"${num(DE).tex}$.", f"using $\\frac{{AD}}{{DB}} = \\frac{{{AD}}}{{{DB}}}$. The matching side for $AD$ is the whole side $AB$, not the piece $DB$.")
    return (p, DE, [F(AD * BC, DB), F(DB * BC, AD + DB), BC - AD, DE + 1, F(BC, 2)], ["Triangle $ADE$ is similar to triangle $ABC$."], sol)


def sic1(r):
    AD, DB = r.randint(1, 6), r.randint(1, 6)
    A = (AD + DB) ** 2 * r.randint(1, 4)
    small = F(A * AD * AD, (AD + DB) ** 2)
    trap = A - small
    p = (f"Triangle $ABC$ has area ${A}$. Point $D$ is on $AB$ with $AD : DB = {AD} : {DB}$, and the line through $D$ parallel to $BC$ meets $AC$ at $E$. "
         f"What is the area of quadrilateral $DBCE$?")
    sol = explain("the area of the trapezoid $DBCE$.", "area of $DBCE$ $=$ area of $ABC$ $-$ area of $ADE$, and $ADE$ is similar to $ABC$.",
                  [f"Scale factor: $\\frac{{AD}}{{AB}} = \\frac{{{AD}}}{{{AD + DB}}}$.", f"Area of $ADE$: ${A} \\cdot \\left(\\frac{{{AD}}}{{{AD + DB}}}\\right)^2 = {A} \\cdot \\frac{{{AD * AD}}}{{{(AD + DB) ** 2}}} = {num(small).tex}$.",
                   f"Area of $DBCE$: ${A} - {num(small).tex} = {num(trap).tex}$."],
                  f"${num(trap).tex}$.", "using the ratio $\\frac{AD}{DB}$ instead of $\\frac{AD}{AB}$, or forgetting to square it.")
    return (p, trap, [small, F(A * DB, AD + DB), F(A * DB * DB, (AD + DB) ** 2), trap + 1, F(A, 2)], ["Triangle $ADE$ is similar to $ABC$ with ratio $\\frac{AD}{AB}$. Subtract its area."], sol)


def sic2(r):
    AB, AC = r.randint(4, 15), r.randint(4, 15)
    if AB == AC:
        return None
    BC = r.randint(abs(AB - AC) + 1, AB + AC - 1)
    BD = F(BC * AB, AB + AC)
    p = f"In triangle $ABC$, $AB = {AB}$, $AC = {AC}$, and $BC = {BC}$. The bisector of angle $A$ meets $BC$ at $D$. What is $BD$?"
    sol = explain("the piece $BD$ of side $BC$.", "Angle Bisector Theorem: $\\frac{BD}{DC} = \\frac{AB}{AC}$. The bisector splits the opposite side in the ratio of the two sides next to the angle.",
                  [f"$BD : DC = {AB} : {AC}$, so $BC$ is split into ${AB + AC}$ equal parts, with ${AB}$ of them in $BD$.", f"$BD = {BC} \\cdot \\frac{{{AB}}}{{{AB + AC}}} = {num(BD).tex}$."],
                  f"${num(BD).tex}$.", f"pairing $BD$ with $AC$. $BD$ touches $B$, so it pairs with side $AB$.")
    return (p, BD, [F(BC * AC, AB + AC), F(BC, 2), BD + 1, F(AB * AC, BC), F(BC * AB, AC)], ["The angle bisector splits the opposite side in the ratio of the adjacent sides: $\\frac{BD}{DC} = \\frac{AB}{AC}$."], sol)


def sic3(r):
    a, bb, c = r.choice(TRIPLES[:5])
    k = r.randint(1, 3)
    a, bb = a * k, bb * k
    s = F(a * bb, a + bb)
    p = (f"A right triangle has legs ${a}$ and ${bb}$. A square is placed inside it with one corner at the right angle and the opposite corner on the hypotenuse. "
         f"What is the side length of the square?")
    sol = explain("the side $s$ of the square.", "the small triangle above the square is similar to the whole triangle.",
                  [f"Put the right angle at the origin, legs along the axes: the hypotenuse runs from $({bb}, 0)$ to $(0, {a})$, with equation $\\frac{{x}}{{{bb}}} + \\frac{{y}}{{{a}}} = 1$.",
                   "The square's far corner is $(s, s)$, and it lies on the hypotenuse: $\\frac{s}{" + str(bb) + "} + \\frac{s}{" + str(a) + "} = 1$.",
                   f"Combine: $s \\cdot \\frac{{{a} + {bb}}}{{{a * bb}}} = 1$, so $s = \\frac{{{a * bb}}}{{{a + bb}}} = {num(s).tex}$."],
                  f"${num(s).tex}$.", "assuming the square's corner is at the middle of the hypotenuse.")
    return (p, s, [F(a + bb, 2), F(a * bb, c * k), F(min(a, bb), 2), s + 1, F(a * bb, 2 * (a + bb))], ["The small triangle above the square is similar to the whole triangle."], sol)


b.fill_unique("basics", [si1, si2, si3, si4] + MORE[b.skill_id]["basics"], 1301)
b.fill_unique("challenge", [sic1, sic2, sic3] + MORE[b.skill_id]["challenge"], 1302)


# ---------------------------------------------------------------- area and perimeter
b = bank("geo_area")


def ar1(r):
    b1, b2, h = r.randint(3, 20), r.randint(3, 20), r.randint(2, 15)
    if b1 == b2:
        return None
    ans = F((b1 + b2) * h, 2)
    p = f"A trapezoid has parallel sides of lengths ${b1}$ and ${b2}$ and height ${h}$. What is its area?"
    sol = explain("the trapezoid's area.", "a trapezoid's area is the average of the two parallel sides times the height. (Two copies, one flipped, make a parallelogram.)",
                  [f"Average of the bases: $\\frac{{{b1} + {b2}}}{{2}} = {num(F(b1 + b2, 2)).tex}$.", f"Area: ${num(F(b1 + b2, 2)).tex} \\cdot {h} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"forgetting to divide by $2$, which gives ${(b1 + b2) * h}$.")
    return (p, ans, [(b1 + b2) * h, b1 * b2 * h // 2 if b1 * b2 * h % 2 == 0 else b1 * h, ans + h, F(max(b1, b2) * h, 1), ans - 2], ["Area of a trapezoid is the average of the bases times the height."], sol)


def ar2(r):
    pts = [(r.randint(-6, 8), r.randint(-6, 8)) for _ in range(3)]
    (x1, y1), (x2, y2), (x3, y3) = pts
    A2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if A2 == 0:
        return None
    ans = F(A2, 2)
    p = f"What is the area of the triangle with vertices $({x1}, {y1})$, $({x2}, {y2})$, and $({x3}, {y3})$?"
    sol = explain("the area from the three corners.", "Shoelace Formula: area $= \\frac{1}{2}\\left|x_1(y_2 - y_3) + x_2(y_3 - y_1) + x_3(y_1 - y_2)\\right|$.",
                  [f"${x1}({y2} - ({y3})) = {x1 * (y2 - y3)}$, ${x2}({y3} - ({y1})) = {x2 * (y3 - y1)}$, ${x3}({y1} - ({y2})) = {x3 * (y1 - y2)}$.",
                   f"Sum: ${x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)}$. Absolute value and half: $\\frac{{{A2}}}{{2}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "forgetting the $\\frac{1}{2}$ or the absolute value.")
    return (p, ans, [A2, ans + 1, ans - F(1, 2) if ans > 1 else ans + 2, F(A2, 4), ans + 3], ["Use the shoelace formula, or enclose the triangle in a rectangle and subtract the corner triangles."], sol)


def ar3(r):
    tri = r.choice([(5, 5, 6), (5, 5, 8), (13, 14, 15), (10, 13, 13), (9, 10, 17), (13, 13, 10), (7, 15, 20), (6, 25, 29), (11, 13, 20), (17, 17, 16)])
    k = r.randint(1, 2)
    a, bb, c = [t * k for t in tri]
    s = F(a + bb + c, 2)
    prod = s * (s - a) * (s - bb) * (s - c)
    A = math.isqrt(int(prod))
    assert A * A == prod
    p = f"What is the area of a triangle with side lengths ${a}$, ${bb}$, and ${c}$?"
    sol = explain("the area from the three side lengths.", "Heron's Formula: with semiperimeter $s = \\frac{a + b + c}{2}$, area $= \\sqrt{s(s - a)(s - b)(s - c)}$.",
                  [f"$s = \\frac{{{a} + {bb} + {c}}}{{2}} = {num(s).tex}$.", f"$s - a = {num(s - a).tex}$, $s - b = {num(s - bb).tex}$, $s - c = {num(s - c).tex}$.",
                   f"Area $= \\sqrt{{{num(s).tex} \\cdot {num(s - a).tex} \\cdot {num(s - bb).tex} \\cdot {num(s - c).tex}}} = \\sqrt{{{int(prod)}}} = {A}$."],
                  f"${A}$.", "using the full perimeter instead of the semiperimeter in Heron's formula.")
    return (p, A, [A * 2, F(a * bb, 2), A + a, A - bb, a + bb + c], ["Use Heron's formula, or drop an altitude and use the Pythagorean Theorem."], sol)


def ar4(r):
    s = r.randint(2, 20)
    k = r.randint(2, 4)
    p = f"The side length of a square is multiplied by ${k}$. The original square had area ${s * s}$. What is the perimeter of the new square?"
    sol = explain("the new square's perimeter.", "find the original side, scale it, then compute the perimeter.",
                  [f"Original side: $\\sqrt{{{s * s}}} = {s}$.", f"New side: ${s} \\cdot {k} = {s * k}$.", f"Perimeter: $4 \\cdot {s * k} = {4 * s * k}$."],
                  f"${4 * s * k}$.", "confusing the area with the perimeter, or squaring the scale factor (that is for area).")
    return (p, 4 * s * k, [4 * s * k * k, s * k, 4 * s, s * s * k, 2 * s * k], ["Find the original side length first."], sol)


def arc1(r):
    a, bb, c = r.choice(TRIPLES[:5])
    k = r.randint(1, 2)
    d1, d2 = 2 * a * k, 2 * bb * k
    side = c * k
    ans = d1 * d2 // 2
    p = f"A rhombus has side length ${side}$ and one diagonal of length ${d1}$. What is its area?"
    sol = explain("the rhombus's area.", "the diagonals of a rhombus cut each other in half at right angles, making four right triangles with the side as hypotenuse.",
                  [f"Half the known diagonal: ${a * k}$.", f"Half the other diagonal: $\\sqrt{{{side}^2 - {a * k}^2}} = {bb * k}$, so the full diagonal is ${d2}$.",
                   f"Area of a rhombus: $\\frac{{d_1 d_2}}{{2}} = \\frac{{{d1} \\cdot {d2}}}{{2}} = {ans}$."],
                  f"${ans}$.", f"using side times side (${side * side}$). A rhombus is not a square unless its angles are right angles.")
    return (p, ans, [d1 * d2, side * side, side * d1 // 2, ans + side, d1 * side], ["The diagonals of a rhombus are perpendicular and bisect each other."], sol)


def arc2(r):
    w, h = r.randint(4, 16) * 2, r.randint(4, 16) * 2
    area = F(w * h) - F(w * h, 4) - F(w * h, 4) - F(w * h, 8)
    p = (f"Rectangle $ABCD$ has $AB = {w}$ and $BC = {h}$. Point $M$ is the midpoint of $BC$ and $N$ is the midpoint of $CD$. "
         f"What is the area of triangle $AMN$?")
    sol = explain("the area of the slanted triangle $AMN$.", "subtract the three right triangles in the corners from the rectangle.",
                  [f"Rectangle area: ${w} \\cdot {h} = {w * h}$.",
                   f"Triangle $ABM$: legs ${w}$ and ${h // 2}$, area $\\frac{{{w} \\cdot {h // 2}}}{{2}} = {num(F(w * h, 4)).tex}$.",
                   f"Triangle $ADN$: legs ${h}$ and ${w // 2}$, area ${num(F(w * h, 4)).tex}$.",
                   f"Triangle $MCN$: legs ${h // 2}$ and ${w // 2}$, area ${num(F(w * h, 8)).tex}$.",
                   f"$[AMN] = {w * h} - {num(F(w * h, 4)).tex} - {num(F(w * h, 4)).tex} - {num(F(w * h, 8)).tex} = {num(area).tex}$."],
                  f"${num(area).tex}$.", "forgetting the small corner triangle $MCN$.")
    return (p, area, [F(w * h, 2), F(w * h, 4), F(w * h, 8), area + 2, F(w * h, 3)], ["Subtract the three right triangles in the corners from the rectangle."], sol)


def arc3(r):
    L = r.randint(10, 60) * 4
    area = F(L * L, 8)
    p = f"A farmer has {L} meters of fence to make a rectangular pen against a long wall, so only three sides need fence. What is the largest possible area of the pen, in square meters?"
    sol = explain("the maximum area.", "write the area in terms of one side; it becomes a downward parabola, whose maximum is at its vertex.",
                  [f"Let the two sides touching the wall be $y$. The side parallel to the wall is then ${L} - 2y$.",
                   f"Area: $A = y({L} - 2y) = {L}y - 2y^2$.",
                   f"The vertex is at $y = \\frac{{{L}}}{{2 \\cdot 2}} = {L // 4}$ (halfway between the zeros $y = 0$ and $y = {L // 2}$).",
                   f"Then the long side is ${L} - {L // 2} = {L // 2}$, and $A = {L // 4} \\cdot {L // 2} = {num(area).tex}$."],
                  f"${num(area).tex}$.", f"making a square with sides ${L // 3}$. With a wall on one side, the best shape is twice as long as it is wide.")
    return (p, area, [F(L * L, 16), F(L * L, 4), F(L * L, 12), area + L, F(L * L, 9)], ["If the two sides touching the wall are $y$, the side parallel to the wall is $L - 2y$."], sol)


b.fill_unique("basics", [ar1, ar2, ar3, ar4] + MORE[b.skill_id]["basics"], 1401)
b.fill_unique("challenge", [arc1, arc2, arc3] + MORE[b.skill_id]["challenge"], 1402)


# ---------------------------------------------------------------- circles
b = bank("geo_circles")


def ci1(r):
    rad = r.randint(2, 15)
    ask = r.choice(["area", "circ"])
    if ask == "area":
        p = f"A circle has a diameter of ${2 * rad}$. What is its area?"
        sol = explain("the circle's area.", "area $= \\pi r^2$, and the radius is half the diameter.",
                      [f"$r = \\frac{{{2 * rad}}}{{2}} = {rad}$.", f"Area $= \\pi \\cdot {rad}^2 = {rad * rad}\\pi$."], f"${rad * rad}\\pi$.", f"using the diameter as the radius, which gives ${4 * rad * rad}\\pi$.")
        return (p, pi_form(rad * rad), [pi_form(4 * rad * rad), pi_form(2 * rad), pi_form(rad), pi_form(2 * rad * rad)], ["Area is $\\pi r^2$, and the radius is half the diameter."], sol)
    p = f"A circle has area ${rad * rad}\\pi$. What is its circumference?"
    sol = explain("the circumference.", "get the radius from the area ($\\pi r^2$), then use $C = 2\\pi r$.",
                  [f"$\\pi r^2 = {rad * rad}\\pi$, so $r^2 = {rad * rad}$ and $r = {rad}$.", f"$C = 2\\pi \\cdot {rad} = {2 * rad}\\pi$."], f"${2 * rad}\\pi$.", "using $\\pi r$ (missing the $2$).")
    return (p, pi_form(2 * rad), [pi_form(rad), pi_form(rad * rad), pi_form(4 * rad), pi_form(2 * rad * rad)], ["Find the radius from the area first."], sol)


def ci2(r):
    rad = r.randint(2, 12)
    ang = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150])
    k = F(ang, 360)
    ask = r.choice(["arc", "sector"])
    if ask == "arc":
        val = 2 * rad * k
        p = f"A circle has radius ${rad}$. What is the length of an arc with central angle ${ang}^\\circ$?"
        sol = explain("the arc length.", "an arc is a fraction of the whole circle: $\\frac{\\text{angle}}{360}$ of the circumference.",
                      [f"Fraction of the circle: $\\frac{{{ang}}}{{360}} = {num(k).tex}$.", f"Circumference: $2\\pi \\cdot {rad} = {2 * rad}\\pi$.", f"Arc: ${num(k).tex} \\cdot {2 * rad}\\pi = {pi_form(val).tex}$."],
                      f"${pi_form(val).tex}$.", "using the area $\\pi r^2$ instead of the circumference.")
        return (p, pi_form(val), [pi_form(rad * rad * k), pi_form(rad * k), pi_form(2 * rad * (1 - k)), pi_form(val * 2)], ["Arc length is the fraction $\\frac{\\theta}{360}$ of the circumference."], sol)
    val = rad * rad * k
    p = f"What is the area of a sector of a circle with radius ${rad}$ and central angle ${ang}^\\circ$?"
    sol = explain("the sector's area.", "a sector is a slice: $\\frac{\\text{angle}}{360}$ of the circle's area.",
                  [f"Fraction: $\\frac{{{ang}}}{{360}} = {num(k).tex}$.", f"Circle area: $\\pi \\cdot {rad}^2 = {rad * rad}\\pi$.", f"Sector: ${num(k).tex} \\cdot {rad * rad}\\pi = {pi_form(val).tex}$."],
                  f"${pi_form(val).tex}$.", "using the circumference instead of the area.")
    return (p, pi_form(val), [pi_form(2 * rad * k), pi_form(rad * rad * (1 - k)), pi_form(rad * rad), pi_form(val * 2)], ["Sector area is the fraction $\\frac{\\theta}{360}$ of the circle's area."], sol)


def ci3(r):
    arc = r.choice(range(40, 300, 4))
    ask = r.choice(["ins", "cent"])
    if ask == "ins":
        p = f"Points $A$, $B$, $C$ lie on a circle, and arc $AB$ (not containing $C$) measures ${arc}^\\circ$. What is $\\angle ACB$, in degrees?"
        sol = explain("the inscribed angle $\\angle ACB$.", "Inscribed Angle Theorem: an angle with its vertex on the circle is half the arc it cuts off.",
                      [f"$\\angle ACB$ cuts off arc $AB = {arc}^\\circ$.", f"$\\angle ACB = \\frac{{{arc}}}{{2}} = {arc // 2}^\\circ$."], f"${arc // 2}^\\circ$.", "using the full arc. That is the central angle, with its vertex at the center.")
        return (p, arc // 2, [arc, 180 - arc // 2, 360 - arc, arc // 4 if arc % 4 == 0 else arc // 2 + 10, 90], ["An inscribed angle is half of the arc it intercepts."], sol)
    if arc >= 180:
        return None
    p = f"An inscribed angle in a circle measures ${arc // 2}^\\circ$. What is the central angle that intercepts the same arc, in degrees?"
    sol = explain("the central angle.", "a central angle equals its arc, and an inscribed angle is half of its arc. So the central angle is twice the inscribed angle.",
                  [f"Arc $= 2 \\cdot {arc // 2} = {arc}^\\circ$.", f"Central angle $=$ arc $= {arc}^\\circ$."], f"${arc}^\\circ$.", "halving instead of doubling.")
    return (p, arc, [arc // 2, 180 - arc, 360 - arc, arc // 4 if arc % 4 == 0 else arc + 10, 2 * arc], ["The central angle equals the arc; the inscribed angle is half the arc."], sol)


def ci4(r):
    a, bb, c = r.choice(TRIPLES[:5])
    k = r.randint(1, 3)
    rad, t, d = a * k, bb * k, c * k
    p = f"A point $P$ is ${d}$ units from the center of a circle of radius ${rad}$. A line through $P$ is tangent to the circle at $T$. What is $PT$?"
    sol = explain("the tangent length $PT$.", "a radius drawn to the point of tangency is perpendicular to the tangent line, so $OTP$ is a right triangle with hypotenuse $OP$.",
                  [f"$OT = {rad}$ (radius) and $OP = {d}$.", f"$PT = \\sqrt{{{d}^2 - {rad}^2}} = \\sqrt{{{d * d - rad * rad}}} = {t}$."], f"${t}$.", f"subtracting lengths, ${d} - {rad} = {d - rad}$.")
    return (p, t, [d - rad, d + rad, t + 1, (d + rad) // 2, rad + 2], ["A tangent is perpendicular to the radius at the point of tangency."], sol)


def cic1(r):
    a, bb, c = r.choice(TRIPLES[:5])
    k = r.randint(1, 3)
    half, dist, rad = a * k, bb * k, c * k
    p = f"A chord of length ${2 * half}$ is drawn in a circle of radius ${rad}$. How far is the chord from the center of the circle?"
    sol = explain("the perpendicular distance from the center to the chord.", "the perpendicular from the center to a chord bisects it, making a right triangle with the radius as hypotenuse.",
                  [f"Half the chord: ${half}$.", f"Distance: $\\sqrt{{{rad}^2 - {half}^2}} = \\sqrt{{{rad * rad - half * half}}} = {dist}$."], f"${dist}$.", f"using the whole chord ${2 * half}$ in the Pythagorean Theorem.")
    return (p, dist, [rad - half, half, dist + 1, rad - dist if rad - dist != dist else rad, 2 * dist], ["The perpendicular from the center bisects the chord."], sol)


def cic2(r):
    a, bb, c = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
    d = F(a * bb, c)
    if d.denominator != 1 or d == c:
        return None
    p = f"Chords $AB$ and $CD$ of a circle intersect at point $P$. If $AP = {a}$, $PB = {bb}$, and $CP = {c}$, what is $PD$?"
    sol = explain("the missing piece $PD$.", "Intersecting Chords (Power of a Point): when two chords cross, the products of their pieces are equal: $AP \\cdot PB = CP \\cdot PD$.",
                  [f"${a} \\cdot {bb} = {c} \\cdot PD$, so ${a * bb} = {c} \\cdot PD$.", f"$PD = \\frac{{{a * bb}}}{{{c}}} = {d}$."], f"${d}$.", "adding the pieces instead of multiplying them.")
    return (p, d, [F(a * c, bb), F(bb * c, a), a + bb - c, d + 1, F(a + bb, 2)], ["For intersecting chords, $AP \\cdot PB = CP \\cdot PD$."], sol)


def cic3(r):
    a, bb, c = r.choice(TRIPLES[:5])
    k = r.randint(1, 3)
    a, bb, c = a * k, bb * k, c * k
    rin = F(a + bb - c, 2)
    p = f"A circle is inscribed in a right triangle with legs ${a}$ and ${bb}$. What is the radius of the circle?"
    sol = explain("the inradius $r$.", "tangent segments from the same point to a circle are equal. At the right angle, the two radii and the legs form a square of side $r$.",
                  [f"Hypotenuse: $\\sqrt{{{a}^2 + {bb}^2}} = {c}$.", f"From the acute corners, the tangent lengths are ${a} - r$ and ${bb} - r$; together they make the hypotenuse: $({a} - r) + ({bb} - r) = {c}$.",
                   f"So $2r = {a} + {bb} - {c} = {a + bb - c}$ and $r = {num(rin).tex}$."],
                  f"${num(rin).tex}$.", f"using half the hypotenuse (${num(F(c, 2)).tex}$), which is the radius of the circle around the triangle, not inside it.")
    return (p, rin, [F(c, 2), F(a * bb, a + bb + c) * 2, rin + 1, F(a * bb, 2 * c), F(min(a, bb), 2)], ["For a right triangle, $r = \\frac{a + b - c}{2}$, or use area $= r \\cdot s$."], sol)


b.fill_unique("basics", [ci1, ci2, ci3, ci4] + MORE[b.skill_id]["basics"], 1501)
b.fill_unique("challenge", [cic1, cic2, cic3] + MORE[b.skill_id]["challenge"], 1502)


# ---------------------------------------------------------------- coordinate geometry
b = bank("geo_coordinate")


def co1(r):
    a, bb, c = r.choice(TRIPLES[:4])
    k = r.randint(1, 2)
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    sx, sy = r.choice([1, -1]), r.choice([1, -1])
    x2, y2 = x1 + sx * a * k, y1 + sy * bb * k
    p = f"What is the distance between $({x1}, {y1})$ and $({x2}, {y2})$?"
    sol = explain("the straight line distance between the points.", "the distance formula is the Pythagorean Theorem: the horizontal and vertical changes are the legs.",
                  [f"Horizontal change: $|{x2} - ({x1})| = {a * k}$. Vertical change: $|{y2} - ({y1})| = {bb * k}$.", f"Distance: $\\sqrt{{{a * k}^2 + {bb * k}^2}} = \\sqrt{{{(a * k) ** 2 + (bb * k) ** 2}}} = {c * k}$."],
                  f"${c * k}$.", f"adding the changes (${(a + bb) * k}$), which is the distance along the grid, not straight across.")
    return (p, c * k, [(a + bb) * k, c * k + 1, abs(x2 - x1) + 1, c * k - 1, a * k * 2], ["Use the distance formula."], sol)


def co2(r):
    x1, y1, x2, y2 = [r.randint(-9, 9) for _ in range(4)]
    if x1 == x2:
        return None
    m = F(y2 - y1, x2 - x1)
    bint = y1 - m * x1
    ask = r.choice(["slope", "int"])
    slope_step = f"Slope: $m = \\frac{{y_2 - y_1}}{{x_2 - x_1}} = \\frac{{{y2} - ({y1})}}{{{x2} - ({x1})}} = \\frac{{{y2 - y1}}}{{{x2 - x1}}} = {num(m).tex}$."
    if ask == "slope":
        p = f"What is the slope of the line through $({x1}, {y1})$ and $({x2}, {y2})$?"
        sol = explain("the slope.", "slope is rise over run: change in $y$ divided by change in $x$, in the same order.", [slope_step], f"${num(m).tex}$.", "dividing run by rise, or subtracting in different orders on top and bottom.")
        return (p, m, [-m if m else 1, 1 / m if m else 2, F(x2 - x1, y2 - y1) if y2 != y1 else 3, m + 1, -1 / m if m else -2], ["Slope is rise over run."], sol)
    p = f"What is the $y$-intercept of the line through $({x1}, {y1})$ and $({x2}, {y2})$?"
    sol = explain("the $y$-intercept $b$ in $y = mx + b$.", "find the slope first, then plug in one point to solve for $b$.",
                  [slope_step, f"Plug in $({x1}, {y1})$: ${y1} = {num(m).tex} \\cdot ({x1}) + b$, so $b = {y1} - ({num(m * x1).tex}) = {num(bint).tex}$."],
                  f"${num(bint).tex}$.", "giving the slope instead of the intercept.")
    return (p, bint, [m, -bint if bint else 4, bint + 1, y1 - x1, bint - m], ["Find the slope, then plug in a point to find $b$ in $y = mx + b$."], sol)


def co3(r):
    a, bb = r.randint(1, 7), r.randint(1, 7)
    sg = r.choice([1, -1])
    m = F(sg * a, bb)
    c0 = r.randint(1, 9)
    ans = -1 / m
    p = f"Line $\\ell$ has equation $y = {num(m).tex}x + {c0}$. What is the slope of a line perpendicular to $\\ell$?"
    sol = explain("the perpendicular slope.", "perpendicular slopes are negative reciprocals: flip the fraction and change the sign. They multiply to $-1$.",
                  [f"The slope of $\\ell$ is ${num(m).tex}$.", f"Flip and change sign: $-\\frac{{1}}{{{num(m).tex}}} = {num(ans).tex}$.", f"Check: ${num(m).tex} \\cdot {num(ans).tex} = -1$."],
                  f"${num(ans).tex}$.", "flipping without changing the sign, or changing the sign without flipping.")
    return (p, ans, [m, -m, 1 / m, ans + 1, F(-bb * 2, a) if a else 2], ["Perpendicular slopes multiply to $-1$."], sol)


def co4(r):
    x1, y1, mx, my = [r.randint(-9, 9) for _ in range(4)]
    x2, y2 = 2 * mx - x1, 2 * my - y1
    ans = x2 + y2
    p = f"The midpoint of segment $AB$ is $({mx}, {my})$, and $A = ({x1}, {y1})$. What is the sum of the coordinates of $B$?"
    sol = explain("the coordinates of $B$, then their sum.", "the midpoint is the average of the endpoints, so $B = 2M - A$ (go from $A$ to $M$, then the same amount again).",
                  [f"$x$: $\\frac{{{x1} + x_B}}{{2}} = {mx}$, so $x_B = 2 \\cdot {mx} - ({x1}) = {x2}$.", f"$y$: $y_B = 2 \\cdot {my} - ({y1}) = {y2}$.", f"$B = ({x2}, {y2})$; sum $= {ans}$."],
                  f"${ans}$.", "averaging $A$ and $M$, which gives a point between them, not past $M$.")
    return (p, ans, [mx + my, x1 + y1, F(x1 + y1 + mx + my, 2), ans + 2, 2 * (mx + my)], ["The midpoint is the average of the endpoints."], sol)


def coc1(r):
    a, bb = r.randint(1, 9), r.randint(1, 9)
    c = a * bb * r.randint(1, 4)
    xi, yi = F(c, a), F(c, bb)
    area = xi * yi / 2
    p = f"What is the area of the triangle bounded by the line ${a}x + {bb}y = {c}$ and the two coordinate axes?"
    sol = explain("the area of the right triangle cut off by the line.", "find the intercepts; they are the legs of the right triangle at the origin.",
                  [f"$x$-intercept (set $y = 0$): ${a}x = {c}$, so $x = {num(xi).tex}$.", f"$y$-intercept (set $x = 0$): ${bb}y = {c}$, so $y = {num(yi).tex}$.",
                   f"Area: $\\frac{{1}}{{2}} \\cdot {num(xi).tex} \\cdot {num(yi).tex} = {num(area).tex}$."],
                  f"${num(area).tex}$.", "forgetting the $\\frac{1}{2}$.")
    return (p, area, [xi * yi, area + 1, F(c, 2), xi + yi, area * 4], ["Find where the line crosses each axis."], sol)


def coc2(r):
    x1, y1 = r.randint(-10, 10), r.randint(-10, 10)
    dx, dy = r.randint(1, 30), r.randint(1, 30)
    g = math.gcd(dx, dy)
    if g == 1:
        return None
    x2, y2 = x1 + dx, y1 + dy
    p = f"How many points with integer coordinates lie on the segment from $({x1}, {y1})$ to $({x2}, {y2})$, including the endpoints?"
    sol = explain("the lattice points on the segment.", "the smallest whole number step along the segment is $\\left(\\frac{\\Delta x}{g}, \\frac{\\Delta y}{g}\\right)$ where $g = \\gcd(\\Delta x, \\Delta y)$.",
                  [f"$\\Delta x = {dx}$, $\\Delta y = {dy}$, and $\\gcd({dx}, {dy}) = {g}$.", f"Smallest step: $({dx // g}, {dy // g})$. It takes ${g}$ steps to cross the segment.",
                   f"${g}$ steps give ${g} + 1 = {g + 1}$ points, counting both ends."],
                  f"${g + 1}$.", f"forgetting one endpoint (answer ${g}$).")
    return (p, g + 1, [g, g + 2, dx + 1, min(dx, dy) + 1, g - 1 if g > 2 else g + 3], ["Step along the segment by $\\left(\\frac{\\Delta x}{g}, \\frac{\\Delta y}{g}\\right)$ where $g = \\gcd(\\Delta x, \\Delta y)$."], sol)


def coc3(r):
    a, bb, c = r.choice(TRIPLES[:3])
    x0, y0 = r.randint(-6, 6), r.randint(-6, 6)
    const = r.randint(-20, 20)
    val = a * x0 + bb * y0 + const
    if val % c:
        return None
    d = abs(val) // c
    if d == 0:
        return None
    line = f"{a}x + {bb}y {'+' if const >= 0 else '-'} {abs(const)} = 0"
    p = f"What is the distance from the point $({x0}, {y0})$ to the line ${line}$?"
    sol = explain("the shortest (perpendicular) distance from the point to the line.", "for $Ax + By + C = 0$, the distance from $(x_0, y_0)$ is $\\frac{|Ax_0 + By_0 + C|}{\\sqrt{A^2 + B^2}}$.",
                  [f"Top: $|{a}({x0}) + {bb}({y0}) {'+' if const >= 0 else '-'} {abs(const)}| = |{val}| = {abs(val)}$.", f"Bottom: $\\sqrt{{{a}^2 + {bb}^2}} = {c}$.", f"Distance: $\\frac{{{abs(val)}}}{{{c}}} = {d}$."],
                  f"${d}$.", "forgetting to divide by $\\sqrt{A^2 + B^2}$.")
    return (p, d, [abs(val), d + 1, F(abs(val), a + bb), d * 2, abs(val) // a if val % a == 0 else d + 3], ["Use $\\frac{|ax_0 + by_0 + c|}{\\sqrt{a^2 + b^2}}$."], sol)


b.fill_unique("basics", [co1, co2, co3, co4] + MORE[b.skill_id]["basics"], 1601)
b.fill_unique("challenge", [coc1, coc2, coc3] + MORE[b.skill_id]["challenge"], 1602)


# ---------------------------------------------------------------- 3D solids
b = bank("geo_solids")


def so1(r):
    l, w, h = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
    ask = r.choice(["vol", "sa"])
    if ask == "vol":
        p = f"What is the volume of a rectangular box that measures ${l}$ by ${w}$ by ${h}$?"
        sol = explain("the space inside the box.", "volume of a box $=$ length $\\times$ width $\\times$ height.", [f"${l} \\cdot {w} \\cdot {h} = {l * w * h}$."], f"${l * w * h}$.", "computing the surface area instead.")
        return (p, l * w * h, [2 * (l * w + w * h + l * h), l + w + h, l * w * h + l, l * w * h // 2 if l * w * h % 2 == 0 else l * w, 4 * (l + w + h)], ["Volume is length times width times height."], sol)
    sa = 2 * (l * w + w * h + l * h)
    p = f"What is the surface area of a rectangular box that measures ${l}$ by ${w}$ by ${h}$?"
    sol = explain("the total area of the six faces.", "a box has three pairs of matching faces.",
                  [f"Face areas: ${l} \\cdot {w} = {l * w}$, ${w} \\cdot {h} = {w * h}$, ${l} \\cdot {h} = {l * h}$.", f"Each appears twice: $2({l * w} + {w * h} + {l * h}) = {sa}$."], f"${sa}$.", "counting each face only once, which gives half the answer.")
    return (p, sa, [l * w * h, sa // 2, sa + 2 * l, 4 * (l + w + h), l * w + w * h + l * h + l * h], ["Add the areas of all six faces."], sol)


def so2(r):
    rad, h = r.randint(1, 9), r.randint(1, 12)
    ask = r.choice(["cyl", "cone"])
    if ask == "cyl":
        p = f"What is the volume of a cylinder with radius ${rad}$ and height ${h}$?"
        sol = explain("the cylinder's volume.", "volume $=$ base area $\\times$ height, and the base is a circle: $V = \\pi r^2 h$.",
                      [f"Base area: $\\pi \\cdot {rad}^2 = {rad * rad}\\pi$.", f"Volume: ${rad * rad}\\pi \\cdot {h} = {pi_form(rad * rad * h).tex}$."], f"${pi_form(rad * rad * h).tex}$.", "using $2\\pi r$ (the circumference) instead of the base area.")
        return (p, pi_form(rad * rad * h), [pi_form(F(rad * rad * h, 3)), pi_form(2 * rad * h), pi_form(rad * h), pi_form(4 * rad * rad * h)], ["$V = \\pi r^2 h$."], sol)
    v = F(rad * rad * h, 3)
    p = f"What is the volume of a cone with radius ${rad}$ and height ${h}$?"
    sol = explain("the cone's volume.", "a cone holds exactly one third of the cylinder with the same base and height: $V = \\frac{1}{3}\\pi r^2 h$.",
                  [f"Cylinder: $\\pi \\cdot {rad}^2 \\cdot {h} = {rad * rad * h}\\pi$.", f"Cone: $\\frac{{1}}{{3}} \\cdot {rad * rad * h}\\pi = {pi_form(v).tex}$."], f"${pi_form(v).tex}$.", "forgetting the $\\frac{1}{3}$.")
    return (p, pi_form(v), [pi_form(rad * rad * h), pi_form(F(rad * h, 3)), pi_form(F(rad * rad * h, 2)), pi_form(v * 2)], ["$V = \\frac{1}{3}\\pi r^2 h$."], sol)


def so3(r):
    rad = r.randint(1, 9) * 3
    ask = r.choice(["vol", "sa"])
    if ask == "vol":
        v = F(4 * rad ** 3, 3)
        p = f"What is the volume of a sphere with radius ${rad}$?"
        sol = explain("the sphere's volume.", "$V = \\frac{4}{3}\\pi r^3$.", [f"$r^3 = {rad}^3 = {rad ** 3}$.", f"$V = \\frac{{4}}{{3}} \\cdot {rad ** 3}\\pi = {pi_form(v).tex}$."], f"${pi_form(v).tex}$.", "using $4\\pi r^2$, which is the surface area.")
        return (p, pi_form(v), [pi_form(4 * rad * rad), pi_form(rad ** 3), pi_form(v * 2), pi_form(F(rad ** 3, 3))], ["$V = \\frac{4}{3}\\pi r^3$."], sol)
    p = f"What is the surface area of a sphere with radius ${rad}$?"
    sol = explain("the sphere's surface area.", "$SA = 4\\pi r^2$ (exactly four times the area of a great circle).", [f"$4\\pi \\cdot {rad}^2 = 4 \\cdot {rad * rad}\\pi = {pi_form(4 * rad * rad).tex}$."], f"${pi_form(4 * rad * rad).tex}$.", "using the volume formula.")
    return (p, pi_form(4 * rad * rad), [pi_form(F(4 * rad ** 3, 3)), pi_form(2 * rad * rad), pi_form(rad * rad), pi_form(8 * rad * rad)], ["$SA = 4\\pi r^2$."], sol)


def so4(r):
    s = r.randint(2, 12)
    p = f"A cube has surface area ${6 * s * s}$. What is its volume?"
    sol = explain("the volume, which needs the edge length.", "a cube has $6$ square faces, each with area $s^2$.",
                  [f"$6s^2 = {6 * s * s}$, so $s^2 = {s * s}$ and $s = {s}$.", f"Volume: $s^3 = {s}^3 = {s ** 3}$."], f"${s ** 3}$.", "taking the square root of the whole surface area, forgetting there are six faces.")
    return (p, s ** 3, [s * s, 6 * s ** 3, s ** 3 + s, (s + 1) ** 3, 6 * s], ["Each of the 6 faces is a square of area $s^2$."], sol)


def soc1(r):
    n = r.randint(3, 10)
    k = r.choice([0, 1, 2, 3])
    counts = {0: (n - 2) ** 3, 1: 6 * (n - 2) ** 2, 2: 12 * (n - 2), 3: 8}
    ans = counts[k]
    p = f"A ${n} \\times {n} \\times {n}$ cube is painted on the outside and cut into ${n ** 3}$ unit cubes. How many unit cubes have exactly {k} painted face{'s' if k != 1 else ''}?"
    where = {0: "inside, touching no outer face", 1: "in the middle of a face (not on an edge)", 2: "on an edge but not at a corner", 3: "at the corners"}[k]
    sol = explain(f"the number of small cubes with exactly ${k}$ painted face{'s' if k != 1 else ''}.", "a small cube's painted faces depend on where it sits: corners get $3$, edges get $2$, face middles get $1$, the inside gets $0$.",
                  [f"Cubes with ${k}$ painted face{'s' if k != 1 else ''} are the ones {where}.",
                   f"Corners: $8$. Edges: each of the $12$ edges has ${n} - 2 = {n - 2}$ non corner cubes, so $12 \\cdot {n - 2} = {12 * (n - 2)}$. Face middles: each of $6$ faces has a $({n - 2}) \\times ({n - 2})$ middle, so $6 \\cdot {(n - 2) ** 2} = {6 * (n - 2) ** 2}$. Inside: $({n} - 2)^3 = {(n - 2) ** 3}$.",
                   f"Check: $8 + {12 * (n - 2)} + {6 * (n - 2) ** 2} + {(n - 2) ** 3} = {n ** 3}$."],
                  f"${ans}$.", f"using ${n}$ instead of ${n} - 2$ for each edge or face, which counts the corners and edges again.")
    return (p, ans, [counts[(k + 1) % 4], counts[(k + 2) % 4], ans + 8, n ** 3 - ans if n ** 3 - ans != ans else ans + 1, 6 * n * n], ["Corners have 3 painted faces, edge pieces (not corners) have 2, face centers have 1, and interior cubes have 0."], sol)


def soc2(r):
    R = r.randint(2, 6)
    s = r.randint(1, 4) * R
    rise = F(s ** 3, R * R)
    ans = over_pi(rise)
    wrong = [num(rise), over_pi(F(s ** 3, 2 * R)), over_pi(F(s * s, R)), pi_form(rise), over_pi(F(s ** 3, R))]
    p = (f"A cylindrical tank with radius ${R}$ is partly filled with water. A solid cube with edge length ${s}$ is dropped in and sinks completely under water. "
         f"By how much does the water level rise?")
    sol = explain("the height $h$ the water rises.", "the water pushed up has the same volume as the cube. That extra water is a cylinder of radius " + str(R) + " and height $h$.",
                  [f"Cube volume: ${s}^3 = {s ** 3}$.", f"Extra water: $\\pi \\cdot {R}^2 \\cdot h = {R * R}\\pi h$.", f"Set equal: ${R * R}\\pi h = {s ** 3}$, so $h = \\frac{{{s ** 3}}}{{{R * R}\\pi}} = {ans.tex}$."],
                  f"${ans.tex}$.", "forgetting the $\\pi$ from the circular base.")
    return (p, ans, wrong, ["The volume of the rise equals the volume of the cube."], sol)


def soc3(r):
    a, bb, c = r.choice(TRIPLES[:4])
    k = r.randint(1, 2)
    rad, h, sl = a * k, bb * k, c * k
    tot = rad * sl + rad * rad
    p = f"A cone has radius ${rad}$ and height ${h}$. What is its total surface area, including the base?"
    sol = explain("the curved surface plus the circular base.", "the curved part of a cone has area $\\pi r \\ell$, where $\\ell$ is the slant height (from tip to the edge of the base).",
                  [f"Slant height: $\\ell = \\sqrt{{{rad}^2 + {h}^2}} = {sl}$.", f"Curved part: $\\pi \\cdot {rad} \\cdot {sl} = {rad * sl}\\pi$. Base: $\\pi \\cdot {rad}^2 = {rad * rad}\\pi$.", f"Total: ${rad * sl}\\pi + {rad * rad}\\pi = {pi_form(tot).tex}$."],
                  f"${pi_form(tot).tex}$.", "using the height instead of the slant height, or leaving out the base.")
    return (p, pi_form(tot), [pi_form(rad * sl), pi_form(rad * h + rad * rad), pi_form(F(rad * rad * h, 3)), pi_form(2 * rad * sl)], ["The slant height is $\\sqrt{r^2 + h^2}$, and the curved part has area $\\pi r \\ell$."], sol)


b.fill_unique("basics", [so1, so2, so3, so4] + MORE[b.skill_id]["basics"], 1701)
b.fill_unique("challenge", [soc1, soc2, soc3] + MORE[b.skill_id]["challenge"], 1702)
