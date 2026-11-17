"""Extra Geometry problem types (part 2): area, circles, coordinate geometry, solids."""
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


def ptex(v):
    """A number in math form, wrapped in parentheses when negative (for substituting)."""
    return f"\\left({ftex(v)}\\right)" if v < 0 else ftex(v)


def kpi(k):
    """k * pi as a choice."""
    k = F(k)
    if k == 0:
        return num(0)
    if k.denominator == 1:
        t = ("" if k == 1 else "-" if k == -1 else str(k.numerator)) + "\\pi"
    else:
        t = ("-" if k < 0 else "") + f"\\frac{{{'' if abs(k.numerator) == 1 else abs(k.numerator)}\\pi}}{{{k.denominator}}}"
    return C(t, float(k) * math.pi)


def a_minus_bpi(a, b):
    """a - b*pi (or a + b*pi for negative b)."""
    a, b = F(a), F(b)
    pt = kpi(abs(b)).tex
    return C(f"{ftex(a)} {'-' if b > 0 else '+'} {pt}", float(a) - float(b) * math.pi)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (6, 8, 10), (9, 12, 15)]


# ================================================================ geo_area
S = "geo_area"


@reg(S, "basics")
def ar_parallelogram(r):
    b, h = r.randint(4, 20), r.randint(3, 15)
    s = r.randint(h + 1, h + 8)
    p = f"A parallelogram has a base of ${b}$, slanted sides of length ${s}$, and a height of ${h}$. What is its area?"
    return Q(p, b * h, [b * s, 2 * (b + s), F(b * h, 2), b * h + s, h * s], "Area is base times height, not base times slanted side.",
             "the area.", "a parallelogram can be cut and slid into a rectangle with the same base and height.",
             [f"Area $= {b} \\cdot {h} = {b * h}$."], "multiplying by the slanted side.")


@reg(S, "basics")
def ar_height_from_area(r):
    b, h = r.randint(4, 24), r.randint(3, 20)
    A = F(b * h, 2)
    p = f"A triangle has area ${ftex(A)}$ and a base of ${b}$. What is the height to that base?"
    return Q(p, h, [F(h, 2), F(A, b), 2 * h, h + 1, b], "Area $= \\frac{1}{2}bh$.",
             "the height.", "solve $\\frac{1}{2} \\cdot b \\cdot h = $ area for $h$.",
             [f"$\\frac{{1}}{{2}} \\cdot {b} \\cdot h = {ftex(A)}$.", f"$h = \\frac{{2 \\cdot {ftex(A)}}}{{{b}}} = {h}$."], "forgetting to double the area.")


@reg(S, "basics")
def ar_l_shape(r):
    W, H = r.randint(8, 20), r.randint(8, 20)
    w, h = r.randint(2, W - 3), r.randint(2, H - 3)
    ans = W * H - w * h
    p = f"An L-shaped room is a ${W} \\times {H}$ rectangle with a ${w} \\times {h}$ rectangle cut out of one corner. What is its area?"
    return Q(p, ans, [W * H, ans + w * h // 2, 2 * (W + H), W * H - w - h, ans - w], "Big rectangle minus the cut-out.",
             "the area of the L shape.", "subtract the missing corner from the full rectangle.",
             [f"Full: ${W} \\cdot {H} = {W * H}$.", f"Cut-out: ${w} \\cdot {h} = {w * h}$.", f"L shape: ${ans}$."], "forgetting to subtract the corner.")


@reg(S, "basics")
def ar_frame(r):
    a, b, w = r.randint(5, 20), r.randint(5, 20), r.randint(1, 3)
    ans = (a + 2 * w) * (b + 2 * w) - a * b
    p = f"A ${a} \\times {b}$ picture has a frame ${w}$ inch{'es' if w > 1 else ''} wide all around it. What is the area of the frame alone?"
    return Q(p, ans, [(a + w) * (b + w) - a * b, 2 * w * (a + b), ans + 4 * w * w, (a + 2 * w) * (b + 2 * w), ans - 2 * w], "The outer rectangle is " + str(2 * w) + " longer in each direction.",
             "the frame's area.", "outer rectangle minus the picture.",
             [f"Outer: ${a + 2 * w} \\times {b + 2 * w} = {(a + 2 * w) * (b + 2 * w)}$.", f"Frame: ${(a + 2 * w) * (b + 2 * w)} - {a * b} = {ans}$."],
             "adding the width only once to each dimension.")


@reg(S, "basics")
def ar_rhombus_diag(r):
    d1, d2 = r.randint(4, 30), r.randint(4, 30)
    p = f"A rhombus has diagonals of lengths ${d1}$ and ${d2}$. What is its area?"
    return Q(p, F(d1 * d2, 2), [d1 * d2, F(d1 * d2, 4), d1 + d2, 2 * (d1 + d2), F(d1 * d2, 2) + 1], "Half the product of the diagonals.",
             "the area.", "the diagonals split a rhombus into four right triangles; together they make half of the $d_1 \\times d_2$ rectangle.",
             [f"Area $= \\frac{{{d1} \\cdot {d2}}}{{2}} = {ftex(F(d1 * d2, 2))}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "basics")
def ar_hexagon(r):
    s = r.randint(2, 10)
    ans = rad(F(3 * s * s, 2), 3)
    p = f"What is the area of a regular hexagon with side ${s}$?"
    return Q(p, ans, [rad(F(s * s, 4), 3), rad(F(3 * s * s, 4), 3), num(6 * s * s), rad(3 * s * s, 3), rad(F(3 * s * s, 2), 2)], "Split it into equilateral triangles.",
             "the area.", "a regular hexagon is six equilateral triangles, each with area $\\frac{\\sqrt{3}}{4}s^2$.",
             [f"One triangle: $\\frac{{\\sqrt{{3}}}}{{4}} \\cdot {s * s} = {rad(F(s * s, 4), 3).tex}$.", f"Six: $6 \\cdot {rad(F(s * s, 4), 3).tex} = {ans.tex}$."],
             "using only one triangle's area.")


@reg(S, "basics")
def ar_corner_triangle(r):
    s = r.choice([4, 6, 8, 10, 12, 14, 16])
    ans = F(7 * s * s, 8)
    p = f"A square has side ${s}$. A triangle is cut off one corner by joining the midpoints of two adjacent sides. What is the area of the remaining piece?"
    return Q(p, ans, [F(3 * s * s, 4), F(s * s, 8), F(s * s, 2), s * s, F(7 * s * s, 4)], "The cut triangle has legs of half the side.",
             "the remaining area.", "subtract the small corner triangle from the square.",
             [f"Corner triangle legs: ${s // 2}$ each, area $\\frac{{1}}{{2}} \\cdot {s // 2}^2 = {ftex(F(s * s, 8))}$.", f"Remaining: ${s * s} - {ftex(F(s * s, 8))} = {ftex(ans)}$."],
             "giving the triangle's area instead of the remaining area.")


@reg(S, "basics")
def ar_path(r):
    a, b, w = r.randint(6, 25), r.randint(6, 25), r.randint(1, 3)
    ans = (a + 2 * w) * (b + 2 * w) - a * b
    p = f"A ${a}$ m by ${b}$ m garden has a path ${w}$ m wide running all the way around the outside. What is the area of the path?"
    return Q(p, ans, [2 * w * (a + b), (a + w) * (b + w) - a * b, ans + 4 * w * w, a * b, ans - 4 * w * w if ans - 4 * w * w != 2 * w * (a + b) else ans + 2], "Outer rectangle minus garden.",
             "the path's area.", "the path's outer edge is a rectangle " + str(2 * w) + " m longer each way.",
             [f"Outer rectangle: ${a + 2 * w} \\times {b + 2 * w} = {(a + 2 * w) * (b + 2 * w)}$.", f"Path: ${(a + 2 * w) * (b + 2 * w)} - {a * b} = {ans}$."],
             "forgetting the four corner squares of the path.")


@reg(S, "basics")
def ar_rect_from_perim(r):
    a, b = r.randint(2, 30), r.randint(2, 30)
    P = 2 * (a + b)
    p = f"A rectangle has perimeter ${P}$ and one side of length ${a}$. What is its area?"
    return Q(p, a * b, [a * (P - a), a * (P // 2), a * b + a, P * a // 4, b * b], "The two different sides add to half the perimeter.",
             "the area.", "length $+$ width $= \\frac{P}{2}$.",
             [f"Other side: $\\frac{{{P}}}{{2}} - {a} = {b}$.", f"Area: ${a} \\cdot {b} = {a * b}$."], "using $P - a$ for the other side.")


@reg(S, "basics")
def ar_shoelace_quad(r):
    pts = [(r.randint(-6, 0), r.randint(-6, 0)), (r.randint(1, 7), r.randint(-6, 0)), (r.randint(1, 7), r.randint(1, 7)), (r.randint(-6, 0), r.randint(1, 7))]
    s2 = sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))
    A = F(abs(s2), 2)
    p = "What is the area of the quadrilateral with vertices " + ", ".join(f"$({x}, {y})$" for x, y in pts) + ", in that order?"
    return Q(p, A, [abs(s2), A + 1, A - 1 if A > 1 else A + 2, (max(x for x, _ in pts) - min(x for x, _ in pts)) * (max(y for _, y in pts) - min(y for _, y in pts)), A * 2 - 3], "Use the shoelace formula, or a box minus corner triangles.",
             "the area.", "Shoelace Formula: area $= \\frac{1}{2}|x_1y_2 - x_2y_1 + x_2y_3 - x_3y_2 + \\cdots|$.",
             ["Cross products: " + ", ".join(f"${pts[i][0]} \\cdot {ptex(pts[(i + 1) % 4][1])} - {ptex(pts[(i + 1) % 4][0])} \\cdot {ptex(pts[i][1])} = {pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1]}$" for i in range(4)) + ".",
              f"Sum: ${s2}$. Area: $\\frac{{{abs(s2)}}}{{2}} = {ftex(A)}$."],
             "forgetting to halve the shoelace sum.")


@reg(S, "basics")
def ar_ratio_base(r):
    m, n = r.sample(range(1, 7), 2)
    A1 = m * r.randint(2, 12)
    tot = F(A1 * (m + n), m)
    p = f"Point $D$ is on side $BC$ of triangle $ABC$ with $BD : DC = {m} : {n}$. Triangle $ABD$ has area ${A1}$. What is the area of triangle $ABC$?"
    return Q(p, tot, [F(A1 * n, m), A1 + n, tot + 1, A1 * (m + n), F(A1 * m, n)], "The triangles share the same height from $A$.",
             "the area of $ABC$.", "triangles with the same height have areas proportional to their bases.",
             [f"$ABD$ is $\\frac{{{m}}}{{{m + n}}}$ of $ABC$.", f"Area of $ABC = {A1} \\cdot \\frac{{{m + n}}}{{{m}}} = {ftex(tot)}$."], "using the ratio the wrong way.")


@reg(S, "basics")
def ar_trap_base(r):
    a, b, h = r.randint(3, 20), r.randint(3, 20), r.randint(2, 12)
    A = F((a + b) * h, 2)
    p = f"A trapezoid has area ${ftex(A)}$, height ${h}$, and one base of length ${a}$. How long is the other base?"
    return Q(p, b, [F(A, h) - a, 2 * A / h, b + a, F(2 * A, h) + a, b + 1], "Area $= \\frac{(a + b)}{2}h$.",
             "the other base.", "solve the trapezoid area formula for the unknown base.",
             [f"$\\frac{{{a} + b}}{{2}} \\cdot {h} = {ftex(A)}$, so ${a} + b = {a + b}$.", f"$b = {b}$."], "forgetting the factor $\\frac{1}{2}$.")


@reg(S, "basics")
def ar_sq_from_diag(r):
    d = r.randint(3, 20)
    p = f"A square has a diagonal of length ${d}$. What is its area?"
    return Q(p, F(d * d, 2), [d * d, F(d * d, 4), 2 * d, rad(F(d, 2), 2), d * d * 2], "Area of a square is half its diagonal squared.",
             "the area.", "a square is a rhombus, so its area is half the product of its (equal) diagonals.",
             [f"Area $= \\frac{{{d}^2}}{{2}} = {ftex(F(d * d, 2))}$."], "squaring the diagonal.")


@reg(S, "basics")
def ar_percent_increase(r):
    p_ = r.choice([10, 20, 25, 30, 40, 50])
    ans = (100 + p_) ** 2 // 100 - 100 if ((100 + p_) ** 2) % 100 == 0 else F((100 + p_) ** 2, 100) - 100
    p = f"Each side of a square is increased by ${p_}\\%$. By what percent does its area increase?"
    return Q(p, ans, [p_, 2 * p_, ans + 10, F(p_ * p_, 100), p_ + 10], "Square the scale factor.",
             "the percent increase in area.", "area scales by the square of the length factor.",
             [f"Length factor: ${ftex(F(100 + p_, 100))}$.", f"Area factor: $\\left({ftex(F(100 + p_, 100))}\\right)^2 = {ftex(F((100 + p_) ** 2, 10000))}$.", f"Increase: ${ftex(ans)}\\%$."],
             "doubling the percent and forgetting the cross term.", ans_tex=f"{ftex(ans)}\\%")


@reg(S, "basics")
def ar_vertex_midpoints(r):
    s = r.choice([4, 6, 8, 10, 12, 16, 20])
    ans = F(3 * s * s, 8)
    p = f"Square $ABCD$ has side ${s}$. $M$ is the midpoint of $BC$ and $N$ is the midpoint of $CD$. What is the area of triangle $AMN$?"
    return Q(p, ans, [F(s * s, 4), F(s * s, 2), F(s * s, 8), F(5 * s * s, 8), ans + s], "Subtract the three corner triangles from the square.",
             "the area of triangle $AMN$.", "the square minus three right triangles leaves triangle $AMN$.",
             [f"Triangles $ABM$ and $ADN$: each $\\frac{{1}}{{2}} \\cdot {s} \\cdot {s // 2} = {ftex(F(s * s, 4))}$.", f"Triangle $MCN$: $\\frac{{1}}{{2}} \\cdot {s // 2} \\cdot {s // 2} = {ftex(F(s * s, 8))}$.",
              f"$AMN = {s * s} - 2 \\cdot {ftex(F(s * s, 4))} - {ftex(F(s * s, 8))} = {ftex(ans)}$."],
             "forgetting the small corner triangle at $C$.")


@reg(S, "basics")
def ar_kite_area(r):
    a, b, c = r.choice(TRIPLES)
    d = r.randint(a + 1, a + 10)
    # kite with diagonals: one diagonal 2a split, other diagonal = b + d? keep simple: diagonals d1 = 2a, d2 = b + e
    e = r.randint(2, 12)
    d1, d2 = 2 * a, b + e
    p = f"A kite's diagonals are perpendicular. One has length ${d1}$; the other is split into pieces of ${b}$ and ${e}$ by the first. What is the kite's area?"
    return Q(p, F(d1 * d2, 2), [d1 * d2, F(d1 * b, 2), a * (b + e), F(d1 * d2, 2) + a, d1 + d2], "A kite with perpendicular diagonals has area $\\frac{1}{2}d_1d_2$.",
             "the area.", "split the kite along the long diagonal into two triangles.",
             [f"Second diagonal: ${b} + {e} = {d2}$.", f"Area: $\\frac{{1}}{{2}} \\cdot {d1} \\cdot {d2} = {ftex(F(d1 * d2, 2))}$."], "using only one piece of the second diagonal.")


@reg(S, "challenge")
def arc_altitude_heron(r):
    k = r.randint(1, 4)
    a, b, c = 13 * k, 14 * k, 15 * k
    area = 84 * k * k
    side = r.choice([a, b, c])
    h = F(2 * area, side)
    p = f"A triangle has sides ${a}$, ${b}$, and ${c}$. What is the length of the altitude to the side of length ${side}$?"
    return Q(p, h, [F(area, side), area, h + 1, F(2 * area, b if side != b else a), F(side, 2)], "Find the area with Heron's formula.",
             "the altitude.", "area $= \\frac{1}{2} \\cdot$ base $\\cdot$ height, so height $= \\frac{2 \\cdot \\text{area}}{\\text{base}}$.",
             [f"$s = {(a + b + c) // 2}$; area $= \\sqrt{{{(a + b + c) // 2} \\cdot {(a + b + c) // 2 - a} \\cdot {(a + b + c) // 2 - b} \\cdot {(a + b + c) // 2 - c}}} = {area}$.", f"Height: $\\frac{{2 \\cdot {area}}}{{{side}}} = {ftex(h)}$."],
             "forgetting to double the area.")


@reg(S, "challenge")
def arc_overlap_squares(r):
    s = r.choice([4, 6, 8, 10, 12])
    p = f"Two squares with side ${s}$ overlap so that a corner of one is at the center of the other. What is the area of the overlap?"
    return Q(p, F(s * s, 4), [F(s * s, 2), F(s * s, 8), s * s, F(s * s, 3), F(3 * s * s, 8)], "Rotate the second square: the overlap never changes.",
             "the overlap area.", "the overlap is always exactly a quarter of the square, however the corner square is turned.",
             ["Draw lines from the center to the midpoints of two sides; rotating the second square swaps a small triangle out and an equal one in.", f"So the overlap is always $\\frac{{1}}{{4}} \\cdot {s * s} = {ftex(F(s * s, 4))}$."],
             "thinking the overlap grows when the square is turned.")


@reg(S, "challenge")
def arc_centroid(r):
    A = r.choice([30, 36, 45, 60, 72, 90, 120])
    p = f"Triangle $ABC$ has area ${A}$, and $G$ is where its three medians meet. What is the area of triangle $GBC$?"
    return Q(p, F(A, 3), [F(A, 2), F(A, 6), F(A, 4), F(2 * A, 3), F(A, 9)], "$G$ is two thirds of the way down each median.",
             "the area of $GBC$.", "the distance from $G$ to $BC$ is $\\frac{1}{3}$ of the height from $A$.",
             [f"Same base $BC$, one third the height.", f"Area: $\\frac{{{A}}}{{3}} = {ftex(F(A, 3))}$."], "using $\\frac{2}{3}$ of the height.")


@reg(S, "challenge")
def arc_octagon(r):
    s = r.randint(1, 8)
    k = 2 * s * s
    tex = f"{k} + {k}\\sqrt{{2}}"
    ans = C(tex, k + k * math.sqrt(2))
    p = f"A regular octagon has side ${s}$. What is its area?"
    return Q(p, ans, [C(f"{k}\\sqrt{{2}}", k * math.sqrt(2)), C(f"{2 * k}", 2 * k), C(f"{k} + {2 * k}\\sqrt{{2}}", k + 2 * k * math.sqrt(2)), C(f"{4 * s * s} + {s * s}\\sqrt{{2}}", 4 * s * s + s * s * math.sqrt(2))],
             "Put the octagon inside a square and cut off the corners.", "the area.", "a regular octagon is a square with four isosceles right triangles cut off its corners.",
             [f"Each corner triangle has hypotenuse ${s}$, so legs $\\frac{{{s}}}{{\\sqrt{{2}}}}$.", f"The square's side: ${s} + 2 \\cdot \\frac{{{s}}}{{\\sqrt{{2}}}} = {s}(1 + \\sqrt{{2}})$, so its area is ${s * s}(3 + 2\\sqrt{{2}})$.",
              f"Corners: $4 \\cdot \\frac{{1}}{{2}} \\cdot \\frac{{{s * s}}}{{2}} = {s * s}$.", f"Octagon: ${s * s}(3 + 2\\sqrt{{2}}) - {s * s} = {tex}$."],
             "using $s$ as the leg of the corner triangles instead of the hypotenuse.", sort=False)


@reg(S, "challenge")
def arc_picks(r):
    I, B = r.randint(2, 30), r.randint(3, 20)
    A = F(I) + F(B, 2) - 1
    p = f"A polygon drawn on graph paper has all its corners on grid points. ${I}$ grid points lie strictly inside it and ${B}$ lie on its boundary. What is its area?"
    return Q(p, A, [I + B, A + 1, F(I + B, 2), I + B - 1, A - F(1, 2)], "Pick's Theorem.",
             "the area.", "Pick's Theorem: area $= I + \\frac{B}{2} - 1$.",
             [f"${I} + \\frac{{{B}}}{{2}} - 1 = {ftex(A)}$."], "forgetting the $-1$.")


@reg(S, "challenge")
def arc_point_in_rect(r):
    x, y, z = r.randint(5, 30), r.randint(5, 30), r.randint(5, 30)
    w = x + z - y
    if w <= 0:
        return None
    p = f"Point $P$ is inside rectangle $ABCD$. The areas of triangles $PAB$, $PBC$, and $PCD$ are ${x}$, ${y}$, and ${z}$. What is the area of triangle $PDA$?"
    return Q(p, w, [y, x + y + z, w + 1, F(x + y + z, 3), y + z - x if y + z - x > 0 else w + 2], "Opposite triangles together make half the rectangle.",
             "the area of $PDA$.", "$PAB + PCD$ is half the rectangle (bases are opposite sides, heights add to the full height); so is $PBC + PDA$.",
             [f"$PAB + PCD = {x + z}$ is half the rectangle.", f"$PBC + PDA = {x + z}$ too, so $PDA = {x + z} - {y} = {w}$."], "averaging the given areas.")


@reg(S, "challenge")
def arc_routh(r):
    t = r.choice([F(1, 4), F(1, 3), F(1, 5), F(2, 5)])
    S_ = r.choice([60, 75, 90, 100, 120, 150])
    frac = 1 - 3 * t + 3 * t * t
    ans = S_ * frac
    if ans.denominator > 4:
        return None
    p = f"Triangle $ABC$ has area ${S_}$. Points $D$, $E$, $F$ lie on $AB$, $BC$, $CA$ with $AD = {ftex(t)}AB$, $BE = {ftex(t)}BC$, and $CF = {ftex(t)}CA$. What is the area of triangle $DEF$?"
    return Q(p, ans, [S_ * t, S_ * (1 - t), S_ * t * (1 - t), ans + 5, S_ * (1 - 3 * t * (1 - t)) / 2], "Subtract the three corner triangles.",
             "the area of $DEF$.", "each corner triangle shares an angle with $ABC$, so its area is the product of the two side fractions times the whole.",
             [f"Corner at $A$: $AD = {ftex(t)}AB$ and $AF = {ftex(1 - t)}AC$, so its area is ${ftex(t)} \\cdot {ftex(1 - t)} = {ftex(t * (1 - t))}$ of the whole. The same holds at $B$ and $C$.",
              f"$DEF = 1 - 3 \\cdot {ftex(t * (1 - t))} = {ftex(frac)}$ of the whole.", f"Area: ${S_} \\cdot {ftex(frac)} = {ftex(ans)}$."],
             "using $t^2$ for each corner instead of $t(1 - t)$.")


# ================================================================ geo_circles
S = "geo_circles"


@reg(S, "basics")
def ci_circ_from_area(r):
    rr = r.randint(2, 15)
    p = f"A circle has area ${kpi(rr * rr).tex}$. What is its circumference?"
    return Q(p, kpi(2 * rr), [kpi(rr), kpi(rr * rr), kpi(4 * rr), kpi(rr * rr * 2), kpi(F(rr, 2))], "Find the radius from the area.",
             "the circumference.", "area $= \\pi r^2$ gives $r$; circumference $= 2\\pi r$.",
             [f"$\\pi r^2 = {kpi(rr * rr).tex}$, so $r = {rr}$.", f"Circumference $= 2\\pi \\cdot {rr} = {kpi(2 * rr).tex}$."], "using $\\pi r$ for the circumference.")


@reg(S, "basics")
def ci_sector(r):
    rr = r.randint(2, 12)
    ang = r.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 240, 270])
    ans = kpi(F(ang, 360) * rr * rr)
    p = f"What is the area of a sector with radius ${rr}$ and central angle ${ang}^\\circ$?"
    return Q(p, ans, [kpi(F(ang, 360) * 2 * rr), kpi(rr * rr), kpi(F(ang, 180) * rr * rr), kpi(F(ang, 360) * rr), kpi(F(ang, 360) * rr * rr + 1)], "The sector is a fraction of the whole circle.",
             "the sector's area.", "a sector with angle $\\theta$ is $\\frac{\\theta}{360}$ of the circle's area.",
             [f"Fraction: $\\frac{{{ang}}}{{360}} = {ftex(F(ang, 360))}$.", f"Area: ${ftex(F(ang, 360))} \\cdot \\pi \\cdot {rr}^2 = {ans.tex}$."], "using the circumference instead of the area.")


@reg(S, "basics")
def ci_radius_from_circ(r):
    rr = r.randint(2, 20)
    p = f"A circle has circumference ${kpi(2 * rr).tex}$. What is its radius?"
    return Q(p, rr, [2 * rr, F(rr, 2), rr * rr, rr + 1, 4 * rr], "Circumference $= 2\\pi r$.",
             "the radius.", "divide the circumference by $2\\pi$.",
             [f"$2\\pi r = {kpi(2 * rr).tex}$, so $r = {rr}$."], "giving the diameter.")


@reg(S, "basics")
def ci_angle_from_arc(r):
    rr = r.randint(2, 12)
    ang = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 240])
    L = F(ang, 360) * 2 * rr
    p = f"An arc of a circle with radius ${rr}$ has length ${kpi(L).tex}$. What is its central angle, in degrees?"
    return Q(p, ang, [ang // 2, 2 * ang if 2 * ang < 360 else ang - 15, 360 - ang, ang + 30, F(L * 180, rr)], "Compare the arc to the whole circumference.",
             "the central angle.", "an arc's angle is the same fraction of $360^\\circ$ as its length is of the circumference.",
             [f"Circumference: ${kpi(2 * rr).tex}$.", f"Fraction: $\\frac{{{kpi(L).tex}}}{{{kpi(2 * rr).tex}}} = {ftex(F(ang, 360))}$.", f"Angle: ${ftex(F(ang, 360))} \\cdot 360 = {ang}^\\circ$."],
             "comparing to the area instead of the circumference.")


@reg(S, "basics")
def ci_semicircle_angle(r):
    a = r.randint(15, 75)
    p = f"Triangle $ABC$ is drawn inside a circle with $AB$ as a diameter and $C$ on the circle. If $\\angle A = {a}^\\circ$, what is $\\angle B$?"
    return Q(p, 90 - a, [a, 180 - a, 90, 180 - 2 * a, 90 - a + 10], "An angle inscribed in a semicircle is a right angle.",
             "$\\angle B$.", "Thales' Theorem: $\\angle C = 90^\\circ$ because it subtends a diameter.",
             ["$\\angle C = 90^\\circ$.", f"$\\angle B = 180 - 90 - {a} = {90 - a}^\\circ$."], "forgetting the right angle at $C$.")


@reg(S, "basics")
def ci_cyclic(r):
    a = r.randint(40, 140)
    p = f"Quadrilateral $ABCD$ is inscribed in a circle, and $\\angle A = {a}^\\circ$. What is $\\angle C$?"
    return Q(p, 180 - a, [a, 360 - a, 90, 180 - a + 10, F(a, 2)], "Opposite angles of a cyclic quadrilateral are supplementary.",
             "$\\angle C$.", "opposite angles of a cyclic quadrilateral add to $180^\\circ$ (their arcs make the whole circle).",
             [f"$\\angle C = 180 - {a} = {180 - a}^\\circ$."], "assuming opposite angles are equal.")


@reg(S, "basics")
def ci_tangent_angle(r):
    c = r.randint(40, 160)
    p = f"Two tangent lines from point $P$ touch a circle at $A$ and $B$. The central angle $\\angle AOB = {c}^\\circ$. What is $\\angle APB$?"
    return Q(p, 180 - c, [c, F(c, 2), 360 - c, 90 - F(c, 2), 180 - c + 10], "A radius is perpendicular to the tangent at the point of contact.",
             "$\\angle APB$.", "quadrilateral $OAPB$ has two right angles at $A$ and $B$.",
             ["$\\angle OAP = \\angle OBP = 90^\\circ$.", f"$\\angle APB = 360 - 90 - 90 - {c} = {180 - c}^\\circ$."], "taking half the central angle.")


@reg(S, "basics")
def ci_ring(r):
    R, rr = r.sample(range(2, 15), 2)
    if R < rr:
        R, rr = rr, R
    p = f"What is the area of the ring between two circles with the same center and radii ${R}$ and ${rr}$?"
    return Q(p, kpi(R * R - rr * rr), [kpi((R - rr) ** 2), kpi(R * R), kpi(2 * (R - rr)), kpi(R * R + rr * rr), kpi(R * R - rr * rr + 1)], "Big circle minus small circle.",
             "the ring's area.", "subtract the inner circle's area from the outer circle's.",
             [f"$\\pi \\cdot {R}^2 - \\pi \\cdot {rr}^2 = {kpi(R * R - rr * rr).tex}$."], "squaring the difference of the radii.")


@reg(S, "basics")
def ci_square_circum(r):
    s = r.randint(2, 14)
    p = f"A square with side ${s}$ is inscribed in a circle (all four corners on the circle). What is the circle's area?"
    return Q(p, kpi(F(s * s, 2)), [kpi(s * s), kpi(F(s * s, 4)), kpi(2 * s * s), kpi(s), kpi(F(s * s, 2) + 1)], "The diagonal of the square is a diameter.",
             "the circle's area.", "the square's diagonal $s\\sqrt{2}$ is the diameter.",
             [f"Diameter: ${s}\\sqrt{{2}}$; radius squared: $\\frac{{{2 * s * s}}}{{4}} = {ftex(F(s * s, 2))}$.", f"Area: ${kpi(F(s * s, 2)).tex}$."], "using the side as the diameter.")


@reg(S, "basics")
def ci_square_corners(r):
    s = r.choice([2, 4, 6, 8, 10, 12])
    ans = a_minus_bpi(s * s, F(s * s, 4))
    p = f"A circle is inscribed in a square with side ${s}$. What is the total area inside the square but outside the circle?"
    return Q(p, ans, [a_minus_bpi(s * s, s * s), kpi(F(s * s, 4)), a_minus_bpi(s * s, F(s * s, 2)), a_minus_bpi(4 * s, F(s * s, 4)), a_minus_bpi(s * s, F(s, 2))], "The circle's diameter is the side.",
             "the four corner regions' total area.", "square area minus circle area; the circle's radius is half the side.",
             [f"Square: ${s * s}$. Circle: radius ${s // 2}$, area ${kpi(F(s * s, 4)).tex}$.", f"Difference: ${ans.tex}$."], "using the side as the radius.", sort=False)


@reg(S, "basics")
def ci_wheel(r):
    rr = r.choice([7, 14, 21, 35])
    D = r.choice([2, 4, 5, 10]) * 44 * rr
    revs = F(D, 2 * rr) * F(7, 22)
    p = f"A wheel has radius ${rr}$ cm. Using $\\pi \\approx \\frac{{22}}{{7}}$, how many full turns does it make rolling ${D}$ cm?"
    return Q(p, revs, [revs * 2, F(D, rr), F(D * 7, 22 * rr * rr) if F(D * 7, 22 * rr * rr) != revs else revs + 3, revs / 2, revs + 1], "One turn covers one circumference.",
             "the number of turns.", "each turn rolls the wheel forward one circumference, $2\\pi r$.",
             [f"Circumference: $2 \\cdot \\frac{{22}}{{7}} \\cdot {rr} = {44 * rr // 7}$ cm.", f"Turns: $\\frac{{{D}}}{{{44 * rr // 7}}} = {ftex(revs)}$."], "dividing by the radius or diameter instead of the circumference.")


@reg(S, "basics")
def ci_through_point(r):
    h, k = r.randint(-6, 6), r.randint(-6, 6)
    a, b = r.randint(-8, 8), r.randint(-8, 8)
    r2 = (a - h) ** 2 + (b - k) ** 2
    if r2 == 0:
        return None
    p = f"A circle has center $({h}, {k})$ and passes through $({a}, {b})$. What is its area?"
    return Q(p, kpi(r2), [kpi(2 * r2), num(r2), kpi(F(r2, 2)), kpi(abs(a - h) + abs(b - k)), kpi(r2 + 1)], "The radius is the distance from the center to the point.",
             "the area.", "radius squared is the squared distance from the center to the point.",
             [f"$r^2 = ({a} - {ptex(h)})^2 + ({b} - {ptex(k)})^2 = {(a - h) ** 2} + {(b - k) ** 2} = {r2}$.", f"Area $= {kpi(r2).tex}$."], "forgetting $\\pi$, or taking a square root you don't need.")


@reg(S, "basics")
def ci_diameter_center(r):
    x1, y1, x2, y2 = [r.randint(-10, 12) for _ in range(4)]
    cx, cy = F(x1 + x2, 2), F(y1 + y2, 2)
    p = f"A diameter of a circle has endpoints $({x1}, {y1})$ and $({x2}, {y2})$. What is the sum of the coordinates of the center?"
    return Q(p, cx + cy, [x1 + x2 + y1 + y2, cx - cy, F(x2 - x1 + y2 - y1, 2), cx + cy + 1, cx], "The center is the midpoint of any diameter.",
             "the coordinate sum of the center.", "the center bisects every diameter.",
             [f"Center: $\\left(\\frac{{{x1} + {ptex(x2)}}}{{2}}, \\frac{{{y1} + {ptex(y2)}}}{{2}}\\right) = ({ftex(cx)}, {ftex(cy)})$.", f"Sum: ${ftex(cx + cy)}$."], "forgetting to divide by $2$.")


@reg(S, "basics")
def ci_tangent_secant(r):
    a, b = r.choice([(1, 4), (2, 8), (4, 9), (3, 12), (4, 16), (1, 9), (2, 18), (5, 20), (9, 16)])
    t = math.isqrt(a * b)
    p = f"From a point $P$ outside a circle, a tangent touches the circle at $T$, and a secant meets the circle at $A$ and $B$ with $PA = {a}$ and $PB = {b}$. What is $PT$?"
    return Q(p, t, [F(a + b, 2), b - a, a * b, t + 1, rad(1, a * a + b * b)], "Power of a point.",
             "$PT$.", "Power of a Point: $PT^2 = PA \\cdot PB$.",
             [f"$PT^2 = {a} \\cdot {b} = {a * b}$.", f"$PT = {t}$."], "averaging the two lengths.")


@reg(S, "basics")
def ci_chord_angle(r):
    a1, a2 = r.randint(30, 160), r.randint(30, 160)
    if a1 + a2 >= 340 or (a1 + a2) % 2:
        return None
    ans = (a1 + a2) // 2
    p = f"Two chords cross inside a circle. The arcs cut off by one of the angles at the crossing and by its vertical angle measure ${a1}^\\circ$ and ${a2}^\\circ$. What is that angle?"
    return Q(p, ans, [a1 + a2, abs(a1 - a2) // 2, 180 - ans, ans + 10, max(a1, a2)], "Average the two arcs.",
             "the angle.", "an angle formed by two chords inside a circle is half the sum of the intercepted arcs.",
             [f"$\\frac{{{a1} + {a2}}}{{2}} = {ans}^\\circ$."], "using half the difference (that's for angles outside the circle).")


@reg(S, "basics")
def ci_right_circum(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    p = f"A right triangle has legs ${a * k}$ and ${b * k}$. What is the radius of the circle through all three of its corners?"
    return Q(p, F(c * k, 2), [c * k, F(a * b * k, c), F(a * k + b * k, 2), F(c * k, 3), F(a * k * b * k, 2)], "The hypotenuse is a diameter.",
             "the circumradius.", "in a right triangle, the hypotenuse is a diameter of the circumscribed circle.",
             [f"Hypotenuse: ${c * k}$.", f"Radius: ${ftex(F(c * k, 2))}$."], "using the hypotenuse as the radius.")


@reg(S, "challenge")
def cic_external_tangent(r):
    a, b = r.choice([(1, 4), (2, 8), (4, 9), (3, 12), (1, 9), (9, 16), (4, 16), (2, 18)])
    t = 2 * math.isqrt(a * b)
    p = f"Circles of radius ${a}$ and ${b}$ touch each other on the outside. A line is tangent to both circles at different points. How far apart are the two tangent points?"
    return Q(p, t, [a + b, b - a, math.isqrt(a * b), t + 1, rad(1, a * a + b * b)], "Draw the radii to the tangent points and the segment joining the centers.",
             "the distance between tangent points.", "the radii are parallel (both perpendicular to the tangent), making a right trapezoid.",
             [f"Centers are ${a + b}$ apart. The radii differ by ${b - a}$.", f"Tangent length: $\\sqrt{{{a + b}^2 - {b - a}^2}} = \\sqrt{{4 \\cdot {a} \\cdot {b}}} = {t}$."], "adding the radii.")


@reg(S, "challenge")
def cic_inradius_equilateral(r):
    s = r.choice([6, 12, 18, 24, 30])
    ans = rad(F(s, 6), 3)
    p = f"What is the radius of the circle inscribed in an equilateral triangle with side ${s}$?"
    return Q(p, ans, [rad(F(s, 3), 3), rad(F(s, 2), 3), num(F(s, 3)), rad(F(s, 6), 2), num(F(s, 2))], "The center is one third of the way up the height.",
             "the inradius.", "the incenter is also the centroid, which sits $\\frac{1}{3}$ of the way up each height.",
             [f"Height: $\\frac{{\\sqrt{{3}}}}{{2}} \\cdot {s} = {rad(F(s, 2), 3).tex}$.", f"Inradius: $\\frac{{1}}{{3}} \\cdot {rad(F(s, 2), 3).tex} = {ans.tex}$."], "using $\\frac{2}{3}$ of the height (that's the circumradius).")


@reg(S, "challenge")
def cic_hexagon_gap(r):
    s = r.choice([2, 4, 6, 8, 10])
    hexa = F(3 * s * s, 2)
    tex = f"{kpi(s * s).tex} - {'' if hexa == 1 else ftex(hexa)}\\sqrt{{3}}"
    ans = C(tex, math.pi * s * s - float(hexa) * math.sqrt(3))
    p = f"A regular hexagon with side ${s}$ is inscribed in a circle. What is the area inside the circle but outside the hexagon?"
    wrong = [C(f"{kpi(s * s).tex} - {ftex(hexa / 2)}\\sqrt{{3}}", math.pi * s * s - float(hexa / 2) * math.sqrt(3)), C(f"{kpi(4 * s * s).tex} - {ftex(hexa)}\\sqrt{{3}}", 4 * math.pi * s * s - float(hexa) * math.sqrt(3)),
             C(f"{kpi(s * s).tex} - {6 * s * s}", math.pi * s * s - 6 * s * s), C(f"{kpi(s * s).tex} - {ftex(hexa * 2)}\\sqrt{{3}}", math.pi * s * s - float(hexa * 2) * math.sqrt(3))]
    return Q(p, ans, wrong, "The circle's radius equals the hexagon's side.", "the area of the six circular slivers.", "circle area minus hexagon area; the hexagon is six equilateral triangles.",
             [f"Circle: radius ${s}$, area ${kpi(s * s).tex}$.", f"Hexagon: $6 \\cdot \\frac{{\\sqrt{{3}}}}{{4}} \\cdot {s * s} = {ftex(hexa)}\\sqrt{{3}}$.", f"Difference: ${tex}$."],
             "using the hexagon's height as the radius.", sort=False)


@reg(S, "challenge")
def cic_three_tangent(r):
    a, b, c = r.choice([(1, 2, 3), (2, 3, 10), (1, 3, 12), (2, 4, 6), (3, 4, 12), (1, 1, 2), (2, 2, 7)])
    area2 = (a + b + c) * a * b * c
    k = math.isqrt(area2)
    ans = num(k) if k * k == area2 else rad(1, area2)
    p = f"Three circles with radii ${a}$, ${b}$, and ${c}$ are each tangent to the other two from the outside. What is the area of the triangle formed by their centers?"
    return Q(p, ans, [num((a + b + c) * 2), rad(1, area2 + 1), num(F(a * b * c, 2)), rad(F(1, 2), area2), num(a * b + b * c + c * a)], "The sides are sums of pairs of radii.",
             "the area of the centers' triangle.", "the sides are $a + b$, $b + c$, $c + a$; use Heron's formula.",
             [f"Sides: ${a + b}$, ${b + c}$, ${c + a}$. Semiperimeter: $s = {a + b + c}$.", f"$s - $ each side gives ${c}$, ${a}$, ${b}$.", f"Area $= \\sqrt{{{a + b + c} \\cdot {a} \\cdot {b} \\cdot {c}}} = {ans.tex}$."],
             "using the radii themselves as the sides.")


@reg(S, "challenge")
def cic_outside_angle(r):
    big, small = r.randint(100, 250), r.randint(10, 90)
    if (big - small) % 2 or big + small >= 360:
        return None
    ans = (big - small) // 2
    p = f"Two secants from a point $P$ outside a circle cut off a far arc of ${big}^\\circ$ and a near arc of ${small}^\\circ$. What is the angle at $P$?"
    return Q(p, ans, [(big + small) // 2 if (big + small) % 2 == 0 else ans + 15, big - small, F(big, 2), ans + 10, 180 - ans], "Half the difference of the arcs.",
             "the angle at $P$.", "an angle formed outside a circle by two secants is half the difference of the intercepted arcs.",
             [f"$\\frac{{{big} - {small}}}{{2}} = {ans}^\\circ$."], "using half the sum (that's for chords crossing inside).")


@reg(S, "challenge")
def cic_tangent_axes(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    tot = 2 * (a + b)
    disc = 2 * a * b
    p = f"Two circles are each tangent to both coordinate axes and pass through $({a}, {b})$. What is the sum of their radii?"
    return Q(p, tot, [a + b, 2 * a * b, a * a + b * b, tot + 2, F(a + b, 2)], "A circle tangent to both axes in the first quadrant has center $(r, r)$.",
             "the sum of the radii.", "the condition gives a quadratic in $r$; Vieta gives the sum of its roots.",
             [f"$(x - r)^2 + (y - r)^2 = r^2$ through $({a}, {b})$: $({a} - r)^2 + ({b} - r)^2 = r^2$.", f"Expand: $r^2 - {2 * (a + b)}r + {a * a + b * b} = 0$ (discriminant $8 \\cdot {a} \\cdot {b} > 0$).", f"Sum of roots: ${tot}$."],
             "forgetting that there are two such circles.")


@reg(S, "challenge")
def cic_parallel_chords(r):
    R = r.choice([5, 10, 13, 17, 25])
    ds = [d for d in range(0, R) if math.isqrt(R * R - d * d) ** 2 == R * R - d * d]
    if len(ds) < 2:
        return None
    d1, d2 = r.sample(ds, 2)
    L1, L2 = 2 * math.isqrt(R * R - d1 * d1), 2 * math.isqrt(R * R - d2 * d2)
    D = abs(d1 - d2)
    if D == 0:
        return None
    p = f"Two parallel chords on the same side of a circle's center have lengths ${L1}$ and ${L2}$ and are ${D}$ units apart. What is the radius?"
    return Q(p, R, [F(L1 + L2, 4), max(L1, L2), R + 1, F(L1, 2), R - 1], "Let the shorter chord be $x$ from the center; write $r^2$ two ways.",
             "the radius.", "each half-chord, its distance from the center, and the radius form a right triangle.",
             [f"Half-chords: ${L1 // 2}$ and ${L2 // 2}$. The longer chord is closer to the center.",
              f"With distances $d$ and $d + {D}$: $({min(L1, L2) // 2})^2 + (d + {D})^2 = ({max(L1, L2) // 2})^2 + d^2$.", f"This gives $d = {min(d1, d2)}$, so $r^2 = {max(L1, L2) // 2}^2 + {min(d1, d2)}^2 = {R * R}$, and $r = {R}$."],
             "assuming one chord passes through the center.")


# ================================================================ geo_coordinate
S = "geo_coordinate"


@reg(S, "basics")
def co_midpoint_sum(r):
    x1, y1, x2, y2 = [r.randint(-12, 12) for _ in range(4)]
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    p = f"What is the sum of the coordinates of the midpoint of the segment from $({x1}, {y1})$ to $({x2}, {y2})$?"
    return Q(p, mx + my, [x1 + x2 + y1 + y2, mx - my, mx + my + 1, F(x2 - x1 + y2 - y1, 2), mx * my], "Average the $x$'s and average the $y$'s.",
             "the coordinate sum of the midpoint.", "the midpoint is the average of the endpoints.",
             [f"Midpoint: $({ftex(mx)}, {ftex(my)})$.", f"Sum: ${ftex(mx + my)}$."], "adding without dividing by $2$.")


@reg(S, "basics")
def co_y_intercept(r):
    x1, x2 = r.sample(range(-6, 8), 2)
    m = F(r.choice([-3, -2, -1, 1, 2, 3]), r.choice([1, 2]))
    b = r.randint(-8, 8)
    y1, y2 = m * x1 + b, m * x2 + b
    if y1.denominator != 1 or y2.denominator != 1:
        return None
    p = f"What is the $y$-intercept of the line through $({x1}, {ftex(y1)})$ and $({x2}, {ftex(y2)})$?"
    return Q(p, b, [m, -b if b else 1, y1, b + m, F(y1 + y2, 2) if F(y1 + y2, 2) != b else b - 2], "Find the slope, then use one point.",
             "the $y$-intercept $b$.", "write $y = mx + b$, find $m$ from the points, then solve for $b$.",
             [f"Slope: $\\frac{{{ftex(y2)} - {ptex(y1)}}}{{{x2} - {ptex(x1)}}} = {ftex(m)}$.", f"$b = {ftex(y1)} - {ptex(m)} \\cdot {ptex(x1)} = {b}$."], "answering the slope.")


@reg(S, "basics")
def co_point_on_line(r):
    m, b = r.randint(-5, 5), r.randint(-10, 10)
    a = r.randint(-8, 8)
    p = f"The point $({a}, k)$ lies on the line $y = {m}x{sg(b)}$. What is $k$?" if m else None
    if p is None:
        return None
    return Q(p, m * a + b, [m + a + b, m * a - b, F(a - b, m), m * a, -(m * a + b) if m * a + b else 3], "Substitute $x = " + str(a) + "$.",
             "$k$.", "a point is on a line exactly when its coordinates satisfy the equation.",
             [f"$k = {m} \\cdot {ptex(a)}{sg(b)} = {m * a + b}$."], "substituting into $x$ instead of solving for $y$.")


@reg(S, "basics")
def co_double_reflect(r):
    a, b = r.randint(-10, 10), r.randint(-10, 10)
    which = r.choice(["x-axis then the y-axis", "y-axis then the line y = x", "x-axis then the line y = x"])
    if which == "x-axis then the y-axis":
        img = (-a, -b)
        steps = [f"Over the $x$-axis: $({a}, {-b})$.", f"Over the $y$-axis: $({-a}, {-b})$."]
    elif which == "y-axis then the line y = x":
        img = (b, -a)
        steps = [f"Over the $y$-axis: $({-a}, {b})$.", f"Over $y = x$ (swap): $({b}, {-a})$."]
    else:
        img = (-b, a)
        steps = [f"Over the $x$-axis: $({a}, {-b})$.", f"Over $y = x$ (swap): $({-b}, {a})$."]
    p = f"The point $({a}, {b})$ is reflected over the {which.replace('y = x', '$y = x$').replace('x-axis', '$x$-axis').replace('y-axis', '$y$-axis')}. What is the sum of the coordinates of the final point?"
    return Q(p, img[0] + img[1], [a + b, -(img[0] + img[1]) if img[0] + img[1] else 2, a - b if a - b != img[0] + img[1] else a - b + 1, img[0] + img[1] + 2, b - a + 1], "Do one reflection at a time.",
             "the coordinate sum after both reflections.", "over the $x$-axis negate $y$; over the $y$-axis negate $x$; over $y = x$ swap the coordinates.",
             steps + [f"Sum: ${img[0] + img[1]}$."], "doing the reflections in the wrong order.")


@reg(S, "basics")
def co_translate(r):
    a, b = r.randint(-8, 8), r.randint(-8, 8)
    da, db = r.randint(-8, 8), r.randint(-8, 8)
    nx, ny = a + da, b + db
    d2 = nx * nx + ny * ny
    p = f"The point $({a}, {b})$ is moved ${abs(da)}$ units {'right' if da >= 0 else 'left'} and ${abs(db)}$ units {'up' if db >= 0 else 'down'}. How far is the new point from the origin?"
    return Q(p, rad(1, d2) if math.isqrt(d2) ** 2 != d2 else math.isqrt(d2), [rad(1, a * a + b * b) if a * a + b * b else num(1), num(abs(nx) + abs(ny)), rad(1, d2 + 2), rad(1, abs(d2 - 4)) if d2 > 4 else num(5), num(d2)],
             "Find the new point first.", "the distance from the origin.", "translate, then use the distance formula.",
             [f"New point: $({nx}, {ny})$.", f"Distance: $\\sqrt{{{ptex(nx)}^2 + {ptex(ny)}^2}} = \\sqrt{{{d2}}}$" + (f" $= {math.isqrt(d2)}$." if math.isqrt(d2) ** 2 == d2 else ".")], "measuring from the original point.")


@reg(S, "basics")
def co_rect_area(r):
    x1, x2 = sorted(r.sample(range(-10, 11), 2))
    y1, y2 = sorted(r.sample(range(-10, 11), 2))
    p = f"A rectangle has corners at $({x1}, {y1})$, $({x2}, {y1})$, $({x2}, {y2})$, and $({x1}, {y2})$. What is its area?"
    A = (x2 - x1) * (y2 - y1)
    return Q(p, A, [2 * (x2 - x1 + y2 - y1), A + 1, abs(x1 * y2 - x2 * y1) or 7, (x2 - x1) * (y2 - y1) // 2 or 3, (x2 + x1) * (y2 + y1) if (x2 + x1) * (y2 + y1) != A else A + 2], "Width and height come from differences of coordinates.",
             "the area.", "the side lengths are the differences in $x$ and in $y$.",
             [f"Width: ${x2} - {ptex(x1)} = {x2 - x1}$. Height: ${y2} - {ptex(y1)} = {y2 - y1}$.", f"Area: ${A}$."], "adding coordinates instead of subtracting.")


@reg(S, "basics")
def co_parallel_slope(r):
    a, b = r.randint(1, 9), r.choice([x for x in range(-9, 10) if x])
    c = r.randint(-20, 20)
    m = F(-a, b)
    p = f"What is the slope of any line parallel to ${a}x{sg(b)}y = {c}$?"
    return Q(p, m, [F(a, b), F(b, a), F(-b, a), F(c, b) if c else 2, -m + 1], "Solve for $y$.",
             "the slope.", "parallel lines have the same slope; rewrite in $y = mx + b$ form to read it off.",
             [f"${b}y = {-a}x{sg(c)}$, so $y = {ftex(m)}x + \\ldots$", f"Slope: ${ftex(m)}$."], "forgetting the sign when moving $" + str(a) + "x$.")


@reg(S, "basics")
def co_x_intercept(r):
    m = r.choice([x for x in range(-6, 7) if x])
    b = r.randint(-15, 15)
    xi = F(-b, m)
    p = f"Where does the line $y = {m}x{sg(b)}$ cross the $x$-axis? Give the $x$-coordinate."
    return Q(p, xi, [F(b, m), b, -xi + 1, m, F(-m, b) if b else 4], "On the $x$-axis, $y = 0$.",
             "the $x$-intercept.", "set $y = 0$ and solve.",
             [f"$0 = {m}x{sg(b)}$.", f"$x = {ftex(xi)}$."], "giving the $y$-intercept.")


@reg(S, "basics")
def co_section(r):
    x1, y1, x2, y2 = [r.randint(-12, 12) for _ in range(4)]
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3)])
    px, py = F(n * x1 + m * x2, m + n), F(n * y1 + m * y2, m + n)
    p = f"Point $P$ is on segment $AB$ with $A = ({x1}, {y1})$, $B = ({x2}, {y2})$, and $AP : PB = {m} : {n}$. What is the sum of the coordinates of $P$?"
    other = F(m * x1 + n * x2, m + n) + F(m * y1 + n * y2, m + n)
    return Q(p, px + py, [other if other != px + py else px + py + 1, F(x1 + x2 + y1 + y2, 2), px + py + 1, px - py, F(x1 + y1, 1)], "$P$ is " + ftex(F(m, m + n)) + " of the way from $A$ to $B$.",
             "the coordinate sum of $P$.", f"move ${ftex(F(m, m + n))}$ of the way from $A$ toward $B$.",
             [f"Change from $A$ to $B$: $({x2 - x1}, {y2 - y1})$.", f"$P = ({x1} + {ftex(F(m, m + n))} \\cdot {ptex(x2 - x1)}, {y1} + {ftex(F(m, m + n))} \\cdot {ptex(y2 - y1)}) = ({ftex(px)}, {ftex(py)})$.", f"Sum: ${ftex(px + py)}$."],
             "measuring from $B$ instead of $A$.")


@reg(S, "basics")
def co_triangle_perim(r):
    a, b, c = r.choice(TRIPLES)
    x0, y0 = r.randint(-5, 5), r.randint(-5, 5)
    p = f"What is the perimeter of the triangle with vertices $({x0}, {y0})$, $({x0 + a}, {y0})$, and $({x0}, {y0 + b})$?"
    return Q(p, a + b + c, [a + b, a + b + c + 1, F(a * b, 2), 2 * (a + b), a + b + a + b - c], "It's a right triangle with legs along the grid.",
             "the perimeter.", "two sides are horizontal and vertical; the third is the hypotenuse.",
             [f"Legs: ${a}$ and ${b}$.", f"Hypotenuse: $\\sqrt{{{a}^2 + {b}^2}} = {c}$.", f"Perimeter: ${a + b + c}$."], "forgetting the slanted side.")


@reg(S, "basics")
def co_rotate90(r):
    a, b = r.randint(-10, 10), r.randint(-10, 10)
    cw = r.random() < 0.5
    img = (b, -a) if cw else (-b, a)
    p = f"The point $({a}, {b})$ is rotated $90^\\circ$ {'clockwise' if cw else 'counterclockwise'} around the origin. What is the sum of the coordinates of its image?"
    other = (-b, a) if cw else (b, -a)
    return Q(p, img[0] + img[1], [other[0] + other[1] if other[0] + other[1] != img[0] + img[1] else img[0] + img[1] + 2, a + b, -(a + b), img[0] - img[1] if img[0] - img[1] != img[0] + img[1] else 1, img[0] + img[1] + 1], "Swap the coordinates and change one sign.",
             "the image's coordinate sum.", f"a $90^\\circ$ {'clockwise' if cw else 'counterclockwise'} turn sends $(x, y)$ to {'$(y, -x)$' if cw else '$(-y, x)$'}.",
             [f"Image: $({img[0]}, {img[1]})$.", f"Sum: ${img[0] + img[1]}$."], "turning the wrong direction.")


@reg(S, "basics")
def co_hit_level(r):
    x0, y0 = r.randint(-6, 6), r.randint(-6, 6)
    m = r.choice([-3, -2, -1, 1, 2, 3, F(1, 2), F(-1, 2)])
    k = r.randint(-10, 10)
    x = x0 + (k - y0) / F(m)
    p = f"A line with slope ${ftex(m)}$ passes through $({x0}, {y0})$. At what $x$ does it reach $y = {k}$?"
    return Q(p, x, [x0 + (k - y0) * F(m), F(k, 1), x + 1, x0 - (k - y0) / F(m), y0 + (k - x0) * F(m)], "Rise needed over slope gives the run.",
             "the $x$-coordinate where $y = " + str(k) + "$.", "the change in $y$ divided by the slope is the change in $x$.",
             [f"Change in $y$: ${k} - {ptex(y0)} = {k - y0}$.", f"Change in $x$: $\\frac{{{k - y0}}}{{{ftex(m)}}} = {ftex((k - y0) / F(m))}$.", f"$x = {x0} + {ptex((k - y0) / F(m))} = {ftex(x)}$."],
             "multiplying by the slope instead of dividing.")


@reg(S, "basics")
def co_centroid(r):
    pts = [(r.randint(-10, 10), r.randint(-10, 10)) for _ in range(3)]
    gx, gy = F(sum(x for x, _ in pts), 3), F(sum(y for _, y in pts), 3)
    p = "What is the sum of the coordinates of the centroid of the triangle with vertices " + ", ".join(f"$({x}, {y})$" for x, y in pts) + "?"
    return Q(p, gx + gy, [sum(x + y for x, y in pts), F(sum(x + y for x, y in pts), 2), gx + gy + 1, gx - gy, gx], "The centroid averages the three vertices.",
             "the centroid's coordinate sum.", "the centroid is the average of the vertices.",
             [f"Centroid: $({ftex(gx)}, {ftex(gy)})$.", f"Sum: ${ftex(gx + gy)}$."], "dividing by $2$ instead of $3$.")


@reg(S, "basics")
def co_parallelogram_vertex(r):
    A, B, Cc = [(r.randint(-8, 8), r.randint(-8, 8)) for _ in range(3)]
    D = (A[0] + Cc[0] - B[0], A[1] + Cc[1] - B[1])
    p = f"$ABCD$ is a parallelogram with $A = {A}$, $B = {B}$, and $C = {Cc}$. What is the sum of the coordinates of $D$?".replace("(", "(").replace(", ", ", ")
    p = f"$ABCD$ is a parallelogram with $A = ({A[0]}, {A[1]})$, $B = ({B[0]}, {B[1]})$, and $C = ({Cc[0]}, {Cc[1]})$. What is the sum of the coordinates of $D$?"
    wrong = [B[0] + Cc[0] - A[0] + B[1] + Cc[1] - A[1], A[0] + B[0] - Cc[0] + A[1] + B[1] - Cc[1], sum(D) + 1, sum(A) + sum(Cc), sum(D) - 2]
    return Q(p, sum(D), wrong, "The diagonals bisect each other.",
             "the coordinate sum of $D$.", "in parallelogram $ABCD$, $D = A + C - B$ (the move from $B$ to $A$ equals the move from $C$ to $D$).",
             [f"$D = ({A[0]} + {ptex(Cc[0])} - {ptex(B[0])}, {A[1]} + {ptex(Cc[1])} - {ptex(B[1])}) = ({D[0]}, {D[1]})$.", f"Sum: ${sum(D)}$."], "using $B + C - A$, which gives a different parallelogram.")


@reg(S, "basics")
def co_square_perim(r):
    a, b = r.randint(-8, 8), r.randint(-8, 8)
    dx, dy = r.randint(1, 8), r.randint(0, 8)
    s2 = dx * dx + dy * dy
    side = rad(1, s2) if math.isqrt(s2) ** 2 != s2 else num(math.isqrt(s2))
    perim = rad(4, s2) if math.isqrt(s2) ** 2 != s2 else num(4 * math.isqrt(s2))
    p = f"Two adjacent corners of a square are $({a}, {b})$ and $({a + dx}, {b + dy})$. What is the square's perimeter?"
    return Q(p, perim, [side, num(s2), rad(2, s2) if math.isqrt(s2) ** 2 != s2 else num(2 * math.isqrt(s2)), num(4 * (dx + dy)), rad(4, s2 + 1)], "Adjacent corners give one side.",
             "the perimeter.", "the distance between adjacent corners is the side length.",
             [f"Side: $\\sqrt{{{dx}^2 + {dy}^2}} = {side.tex}$.", f"Perimeter: $4 \\cdot {side.tex} = {perim.tex}$."], "giving the area or a single side.")


@reg(S, "basics")
def co_equidistant_axis(r):
    a, b, c, d = [r.randint(-8, 8) for _ in range(4)]
    if b == d:
        return None
    y = F(c * c + d * d - a * a - b * b, 2 * (d - b))
    p = f"Point $P$ is on the $y$-axis and is the same distance from $({a}, {b})$ and $({c}, {d})$. What is the $y$-coordinate of $P$?"
    return Q(p, y, [F(b + d, 2), -y if y else 1, y + 1, F(a + c, 2), F(c * c + d * d - a * a - b * b, d - b)], "Write $P = (0, y)$ and set the squared distances equal.",
             "the $y$-coordinate of $P$.", "equal distances means equal squared distances, and the $y^2$ terms cancel.",
             [f"${ptex(a)}^2 + (y{sg(-b)})^2 = {ptex(c)}^2 + (y{sg(-d)})^2$.", f"Expanding, $y^2$ cancels: ${a * a + b * b}{sg(-2 * b)}y = {c * c + d * d}{sg(-2 * d)}y$.", f"${2 * (d - b)}y = {c * c + d * d - a * a - b * b}$, so $y = {ftex(y)}$."],
             "taking the average of the $y$-coordinates, which only works if the $x$-coordinates match.")


@reg(S, "challenge")
def coc_perp_bisector(r):
    x1, y1, x2, y2 = [r.randint(-8, 8) for _ in range(4)]
    if y1 == y2 or x1 == x2:
        return None
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    m = F(-(x2 - x1), y2 - y1)
    b = my - m * mx
    p = f"What is the $y$-intercept of the perpendicular bisector of the segment from $({x1}, {y1})$ to $({x2}, {y2})$?"
    return Q(p, b, [my, my - F(y2 - y1, x2 - x1) * mx, -b if b else 1, b + 1, m], "Find the midpoint and the perpendicular slope.",
             "the $y$-intercept.", "the perpendicular bisector passes through the midpoint with slope $-\\frac{1}{m}$.",
             [f"Midpoint: $({ftex(mx)}, {ftex(my)})$.", f"Segment slope: ${ftex(F(y2 - y1, x2 - x1))}$, so the perpendicular slope is ${ftex(m)}$.", f"$b = {ftex(my)} - {ptex(m)} \\cdot {ptex(mx)} = {ftex(b)}$."],
             "using the segment's own slope.")


@reg(S, "challenge")
def coc_reflect_line(r):
    c = r.randint(-6, 6)
    a, b = r.randint(-8, 8), r.randint(-8, 8)
    img = (b - c, a + c)
    p = f"The point $({a}, {b})$ is reflected over the line $y = x{sg(c)}$. What is the sum of the coordinates of its image?"
    return Q(p, img[0] + img[1], [a + b, b + a + 2 * c + 1, img[0] - img[1], b - a, a + b + c], "Shift so the line becomes $y = x$, swap, shift back.",
             "the image's coordinate sum.", "shift down by " + str(c) + " so the line is $y = x$, swap the coordinates, then shift back up.",
             [f"Shift down by ${c}$: $({a}, {b - c})$.", f"Swap: $({b - c}, {a})$.", f"Shift back up: $({b - c}, {a + c})$.", f"Sum: ${img[0] + img[1]}$."],
             "just swapping the coordinates as if the line were $y = x$.")


@reg(S, "challenge")
def coc_parallel_distance(r):
    a, b, c5 = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)])
    c1 = r.randint(-30, 30)
    d = r.randint(1, 4)
    c2 = c1 + d * c5
    p = f"What is the distance between the parallel lines ${a}x + {b}y = {c1}$ and ${a}x + {b}y = {c2}$?"
    return Q(p, d, [c2 - c1, F(c2 - c1, a + b), d + 1, F(c2 - c1, a), F(d, 2)], "Divide the difference of constants by $\\sqrt{a^2 + b^2}$.",
             "the distance.", "for $ax + by = c_1$ and $ax + by = c_2$, the distance is $\\frac{|c_1 - c_2|}{\\sqrt{a^2 + b^2}}$.",
             [f"$\\sqrt{{{a}^2 + {b}^2}} = {c5}$.", f"Distance: $\\frac{{{c2 - c1}}}{{{c5}}} = {d}$."], "forgetting to divide by $\\sqrt{a^2 + b^2}$.")


@reg(S, "challenge")
def coc_tangent_line(r):
    rr = r.randint(1, 6)
    m = r.choice([0, 1, 2, 3, F(3, 4), F(4, 3)])
    c2 = rr * rr * (1 + F(m) ** 2)
    c = rad(1, c2) if F(c2).denominator == 1 else None
    if c is None:
        return None
    p = f"For what positive $c$ is the line $y = {ftex(m)}x + c$ tangent to the circle $x^2 + y^2 = {rr * rr}$?" if m else f"For what positive $c$ is the line $y = c$ tangent to the circle $x^2 + y^2 = {rr * rr}$?"
    return Q(p, c, [num(rr), rad(1, rr * rr + 1), num(rr * rr), rad(rr, 2) if m != 1 else num(2 * rr), rad(1, c2 + 1)], "The distance from the center to the line must equal the radius.",
             "$c$.", "a line is tangent when its distance from the center equals the radius.",
             [f"Line: ${ftex(m)}x - y + c = 0$. Distance from $(0, 0)$: $\\frac{{c}}{{\\sqrt{{{ftex(F(m) ** 2)} + 1}}}}$.", f"Set it to ${rr}$: $c = {rr}\\sqrt{{{ftex(1 + F(m) ** 2)}}} = {c.tex}$."],
             "setting $c$ equal to the radius, which only works for a horizontal line.")


@reg(S, "challenge")
def coc_foot(r):
    a, b = r.choice([(1, 1), (1, 2), (2, 1), (1, -1), (3, 1), (1, 3)])
    x0, y0 = r.randint(-6, 6), r.randint(-6, 6)
    c = r.randint(-10, 10)
    t = F(c - a * x0 - b * y0, a * a + b * b)
    fx, fy = x0 + a * t, y0 + b * t
    line = f"{a if a != 1 else ''}x {'+' if b > 0 else '-'} {abs(b) if abs(b) != 1 else ''}y = {c}"
    p = f"What is the sum of the coordinates of the point on the line ${line}$ closest to $({x0}, {y0})$?"
    return Q(p, fx + fy, [x0 + y0, fx - fy, fx + fy + 1, F(c, 1), F(c, a + b) if a + b else 2], "Move from the point along the line's normal direction $(" + f"{a}, {b}" + ")$.",
             "the foot of the perpendicular.", "the closest point is where a perpendicular from the point meets the line; the perpendicular direction is $(a, b)$.",
             [f"Points along the perpendicular: $({x0} + {a}t, {y0} + {ptex(b)}t)$.", f"Put into the line: ${a}({x0} + {a}t) + {ptex(b)}({y0} + {ptex(b)}t) = {c}$, so ${a * a + b * b}t = {c - a * x0 - b * y0}$ and $t = {ftex(t)}$.",
              f"Foot: $({ftex(fx)}, {ftex(fy)})$; sum ${ftex(fx + fy)}$."],
             "moving in the line's own direction instead of perpendicular to it.")


@reg(S, "challenge")
def coc_min_triangle(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    p = f"A line through $({a}, {b})$ crosses the positive $x$-axis and the positive $y$-axis, forming a triangle with them. What is the smallest possible area of that triangle?"
    return Q(p, 2 * a * b, [a * b, 4 * a * b, F(a * b, 2), (a + b) ** 2 // 2, 2 * a * b + 1], "The point turns out to be the midpoint of the hypotenuse.",
             "the minimum area.", "the area is smallest when the point is the midpoint of the segment between the intercepts.",
             [f"Intercepts $(p, 0)$ and $(0, q)$ with $\\frac{{{a}}}{{p}} + \\frac{{{b}}}{{q}} = 1$. Area $= \\frac{{pq}}{{2}}$.",
              f"By AM-GM, $1 = \\frac{{{a}}}{{p}} + \\frac{{{b}}}{{q}} \\ge 2\\sqrt{{\\frac{{{a * b}}}{{pq}}}}$, so $pq \\ge {4 * a * b}$.", f"Smallest area: $\\frac{{{4 * a * b}}}{{2}} = {2 * a * b}$, when $p = {2 * a}$ and $q = {2 * b}$."],
             "using the rectangle $" + f"{a} \\times {b}" + "$ as the answer.")


@reg(S, "challenge")
def coc_parabola_triangle(r):
    a, b, c = sorted(r.sample(range(-5, 6), 3))
    area = F(abs((a - b) * (b - c) * (c - a)), 2)
    p = f"Points on the parabola $y = x^2$ have $x$-coordinates ${a}$, ${b}$, and ${c}$. What is the area of the triangle they form?"
    return Q(p, area, [area * 2, area + 1, F(abs((a - b) * (b - c)), 2), abs(c - a) * max(a * a, c * c) // 2, area / 2], "Use the shoelace formula; it factors nicely.",
             "the area.", "for points $(t, t^2)$, the shoelace formula simplifies to $\\frac{1}{2}|(a - b)(b - c)(c - a)|$.",
             [f"Points: $({a}, {a * a})$, $({b}, {b * b})$, $({c}, {c * c})$.", f"Area $= \\frac{{1}}{{2}}|({a} - {ptex(b)})({b} - {ptex(c)})({c} - {ptex(a)})| = \\frac{{{abs((a - b) * (b - c) * (c - a))}}}{{2}} = {ftex(area)}$."],
             "forgetting the $\\frac{1}{2}$.")


# ================================================================ geo_solids
S = "geo_solids"


@reg(S, "basics")
def so_box_volume(r):
    a, b, c = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
    p = f"What is the volume of a box measuring ${a}$ by ${b}$ by ${c}$?"
    return Q(p, a * b * c, [2 * (a * b + b * c + c * a), a + b + c, a * b + c, a * b * c + a, 4 * (a + b + c)], "Multiply the three dimensions.",
             "the volume.", "volume of a rectangular box $=$ length $\\times$ width $\\times$ height.",
             [f"${a} \\cdot {b} \\cdot {c} = {a * b * c}$."], "computing the surface area instead.")


@reg(S, "basics")
def so_cone_volume(r):
    rr, h = r.randint(2, 9), r.randint(3, 15)
    p = f"What is the volume of a cone with radius ${rr}$ and height ${h}$?"
    return Q(p, kpi(F(rr * rr * h, 3)), [kpi(rr * rr * h), kpi(F(rr * h, 3)), kpi(F(rr * rr * h, 2)), kpi(F(rr * rr * h, 6)), kpi(F(rr * rr * h, 3) + 1)], "A cone is one third of a cylinder.",
             "the volume.", "$V = \\frac{1}{3}\\pi r^2 h$.",
             [f"$\\frac{{1}}{{3}} \\cdot \\pi \\cdot {rr}^2 \\cdot {h} = {kpi(F(rr * rr * h, 3)).tex}$."], "forgetting the $\\frac{1}{3}$.")


@reg(S, "basics")
def so_sphere_area(r):
    rr = r.randint(1, 12)
    p = f"What is the surface area of a sphere with radius ${rr}$?"
    return Q(p, kpi(4 * rr * rr), [kpi(rr * rr), kpi(F(4 * rr ** 3, 3)), kpi(2 * rr * rr), kpi(4 * rr), kpi(8 * rr * rr)], "$4\\pi r^2$.",
             "the surface area.", "a sphere's surface area is $4\\pi r^2$, four times the area of its flat cross-section through the center.",
             [f"$4\\pi \\cdot {rr}^2 = {kpi(4 * rr * rr).tex}$."], "using the volume formula.")


@reg(S, "basics")
def so_cyl_total(r):
    rr, h = r.randint(1, 9), r.randint(2, 15)
    p = f"What is the total surface area (including both ends) of a cylinder with radius ${rr}$ and height ${h}$?"
    return Q(p, kpi(2 * rr * rr + 2 * rr * h), [kpi(2 * rr * h), kpi(rr * rr * h), kpi(rr * rr + 2 * rr * h), kpi(2 * rr * rr + rr * h), kpi(4 * rr * rr + 2 * rr * h)], "Two circles plus the curved side.",
             "the total surface area.", "the curved side unrolls into a rectangle $2\\pi r$ by $h$; add the two circular ends.",
             [f"Ends: $2 \\cdot \\pi \\cdot {rr}^2 = {kpi(2 * rr * rr).tex}$.", f"Side: $2\\pi \\cdot {rr} \\cdot {h} = {kpi(2 * rr * h).tex}$.", f"Total: ${kpi(2 * rr * rr + 2 * rr * h).tex}$."],
             "forgetting one of the ends.")


@reg(S, "basics")
def so_cube_from_volume(r):
    s = r.randint(2, 12)
    p = f"A cube has volume ${s ** 3}$. What is its surface area?"
    return Q(p, 6 * s * s, [s * s, 4 * s * s, s ** 3, 12 * s, 6 * s], "Find the edge first.",
             "the surface area.", "edge $= \\sqrt[3]{V}$; surface area $= 6s^2$.",
             [f"Edge: $\\sqrt[3]{{{s ** 3}}} = {s}$.", f"Surface area: $6 \\cdot {s}^2 = {6 * s * s}$."], "counting only four faces.")


@reg(S, "basics")
def so_pyramid(r):
    s, h = r.randint(2, 12), r.randint(3, 15)
    p = f"A pyramid has a square base with side ${s}$ and height ${h}$. What is its volume?"
    return Q(p, F(s * s * h, 3), [s * s * h, F(s * s * h, 2), F(s * h, 3), F(4 * s * h, 3), F(s * s * h, 6)], "One third of base times height.",
             "the volume.", "any pyramid has volume $\\frac{1}{3} \\cdot$ base area $\\cdot$ height.",
             [f"Base area: ${s * s}$.", f"$V = \\frac{{1}}{{3}} \\cdot {s * s} \\cdot {h} = {ftex(F(s * s * h, 3))}$."], "forgetting the $\\frac{1}{3}$.")


@reg(S, "basics")
def so_double_edges(r):
    V = r.choice([5, 6, 10, 12, 15, 20, 24])
    k = r.choice([2, 3])
    p = f"A box has volume ${V}$. Every edge is multiplied by ${k}$. What is the new volume?"
    return Q(p, V * k ** 3, [V * k, V * k * k, V + k ** 3, V * 3 * k, V * k ** 3 // 2], "Each of three dimensions scales.",
             "the new volume.", "multiplying each of the three dimensions by $k$ multiplies the volume by $k^3$.",
             [f"${V} \\cdot {k}^3 = {V * k ** 3}$."], "multiplying the volume by just " + str(k) + ".")


@reg(S, "basics")
def so_fit_cubes(r):
    k = r.choice([2, 3])
    a, b, c = [k * r.randint(1, 5) for _ in range(3)]
    n = (a // k) * (b // k) * (c // k)
    p = f"How many ${k} \\times {k} \\times {k}$ cubes fit exactly inside a ${a} \\times {b} \\times {c}$ box?"
    return Q(p, n, [a * b * c, F(a * b * c, k), n * k, n + 1, (a + b + c) // k], "Count how many fit along each edge.",
             "the number of cubes.", "along each edge, " + str(k) + " divides the length evenly.",
             [f"Along each edge: ${a // k}$, ${b // k}$, ${c // k}$.", f"Total: ${a // k} \\cdot {b // k} \\cdot {c // k} = {n}$."], "dividing the volume by " + str(k) + " instead of " + str(k ** 3) + ".")


@reg(S, "basics")
def so_tri_prism(r):
    a, b, h = r.randint(2, 12), r.randint(2, 12), r.randint(2, 15)
    p = f"A prism has a right triangle base with legs ${a}$ and ${b}$, and length ${h}$. What is its volume?"
    return Q(p, F(a * b * h, 2), [a * b * h, F(a * b * h, 3), F(a * b, 2) + h, a * b * h * 2, F((a + b) * h, 2)], "Base area times length.",
             "the volume.", "any prism has volume $=$ base area $\\times$ length.",
             [f"Base: $\\frac{{1}}{{2}} \\cdot {a} \\cdot {b} = {ftex(F(a * b, 2))}$.", f"Volume: ${ftex(F(a * b, 2))} \\cdot {h} = {ftex(F(a * b * h, 2))}$."], "forgetting the $\\frac{1}{2}$ in the triangle.")


@reg(S, "basics")
def so_hemisphere(r):
    rr = r.choice([3, 6, 9, 12])
    p = f"What is the volume of a solid hemisphere (half a ball) with radius ${rr}$?"
    return Q(p, kpi(F(2 * rr ** 3, 3)), [kpi(F(4 * rr ** 3, 3)), kpi(2 * rr * rr), kpi(F(rr ** 3, 3)), kpi(rr ** 3), kpi(3 * rr * rr)], "Half of $\\frac{4}{3}\\pi r^3$.",
             "the volume.", "a hemisphere is half a sphere.",
             [f"Sphere: $\\frac{{4}}{{3}}\\pi \\cdot {rr}^3 = {kpi(F(4 * rr ** 3, 3)).tex}$.", f"Half: ${kpi(F(2 * rr ** 3, 3)).tex}$."], "giving the full sphere's volume.")


@reg(S, "basics")
def so_tank_rise(r):
    L, W = r.choice([(50, 40), (100, 50), (60, 50), (80, 25), (40, 25)])
    liters = r.choice([10, 20, 30, 40, 50, 60])
    rise = F(liters * 1000, L * W)
    p = f"A rectangular tank has a base ${L}$ cm by ${W}$ cm. How many cm does the water rise when ${liters}$ liters are poured in? (One liter is $1000$ cubic cm.)"
    return Q(p, rise, [F(liters * 100, L * W), F(liters, L * W) * 100, rise * 2, F(liters * 1000, L + W), rise + 1], "Volume added equals base area times rise.",
             "the rise in water level.", "the poured water forms a thin box with the tank's base and height equal to the rise.",
             [f"Volume: ${liters} \\cdot 1000 = {liters * 1000}$ cm$^3$.", f"Rise: $\\frac{{{liters * 1000}}}{{{L} \\cdot {W}}} = {ftex(rise)}$ cm."], "forgetting to convert liters to cubic centimeters.")


@reg(S, "basics")
def so_prism_edges(r):
    n = r.randint(3, 20)
    ask = r.choice(["edges", "faces", "vertices"])
    val = {"edges": 3 * n, "faces": n + 2, "vertices": 2 * n}[ask]
    p = f"A prism has bases that are ${n}$-sided polygons. How many {ask} does it have?"
    return Q(p, val, [3 * n if ask != "edges" else 2 * n, n + 2 if ask != "faces" else n, 2 * n if ask != "vertices" else n + 2, val + 1, val + n], "Count the two bases, then what connects them.",
             "the number of " + ask + ".", "a prism has two copies of the base polygon joined by rectangles.",
             [f"Vertices: ${n}$ on each base, ${2 * n}$ total. Edges: ${n}$ on each base plus ${n}$ connecting, ${3 * n}$ total. Faces: ${n}$ sides plus $2$ bases, ${n + 2}$ total."],
             "forgetting the edges that connect the two bases.")


@reg(S, "basics")
def so_euler(r):
    F_, V = r.randint(5, 20), r.randint(5, 20)
    E = V + F_ - 2
    p = f"A convex polyhedron has ${V}$ vertices and ${F_}$ faces. How many edges does it have?"
    return Q(p, E, [V + F_, V + F_ + 2, E + 1, abs(V - F_) + 2, 2 * E], "Euler's formula.",
             "the number of edges.", "Euler's formula: $V - E + F = 2$.",
             [f"${V} - E + {F_} = 2$, so $E = {V} + {F_} - 2 = {E}$."], "using $+2$ instead of $-2$.")


@reg(S, "basics")
def so_cyl_radius(r):
    rr, h = r.randint(1, 10), r.randint(2, 12)
    p = f"A cylinder has volume ${kpi(rr * rr * h).tex}$ and height ${h}$. What is its radius?"
    return Q(p, rr, [rr * rr, 2 * rr, F(rr * rr, 2), rr + 1, rr * h], "$V = \\pi r^2 h$.",
             "the radius.", "solve $\\pi r^2 h = V$ for $r$.",
             [f"$\\pi r^2 \\cdot {h} = {kpi(rr * rr * h).tex}$, so $r^2 = {rr * rr}$.", f"$r = {rr}$."], "stopping at $r^2$.")


@reg(S, "basics")
def so_melt(r):
    R = r.choice([3, 6, 9])
    rr = r.choice([x for x in [1, 2, 3, 6] if (4 * R ** 3) % (3 * x * x) == 0])
    h = F(4 * R ** 3, 3 * rr * rr)
    p = f"A metal ball of radius ${R}$ is melted down and recast as a solid cylinder of radius ${rr}$. How tall is the cylinder?"
    return Q(p, h, [F(4 * R ** 3, rr * rr), F(R ** 3, rr * rr), h / 2, h + 1, F(4 * R * R, 3 * rr)], "The volume stays the same.",
             "the cylinder's height.", "set the sphere's volume equal to the cylinder's.",
             [f"Sphere: $\\frac{{4}}{{3}}\\pi \\cdot {R}^3 = {kpi(F(4 * R ** 3, 3)).tex}$.", f"$\\pi \\cdot {rr}^2 \\cdot h = {kpi(F(4 * R ** 3, 3)).tex}$, so $h = {ftex(h)}$."], "forgetting the $\\frac{4}{3}$.")


@reg(S, "basics")
def so_cube_from_diag(r):
    s = r.randint(1, 10)
    d = rad(s, 3)
    p = f"A cube's space diagonal (corner to opposite corner, through the inside) is ${d.tex}$. What is its surface area?"
    return Q(p, 6 * s * s, [s * s, 3 * s * s, 6 * s, 4 * s * s, s ** 3], "Space diagonal $= s\\sqrt{3}$.",
             "the surface area.", "the space diagonal of a cube with edge $s$ is $s\\sqrt{3}$.",
             [f"$s\\sqrt{{3}} = {d.tex}$, so $s = {s}$.", f"Surface area: $6 \\cdot {s * s} = {6 * s * s}$."], "using $s\\sqrt{2}$ (the face diagonal).")


@reg(S, "challenge")
def soc_corner_cut(r):
    s = r.choice([3, 6, 9, 12])
    cut = F(s ** 3, 6)
    p = f"A cube with edge ${s}$ is cut by a plane through the three corners next to one vertex, removing a small pyramid. What is the volume of the larger remaining piece?"
    return Q(p, s ** 3 - cut, [cut, F(s ** 3, 2), s ** 3 - F(s ** 3, 3), F(2 * s ** 3, 3), s ** 3 - F(s ** 3, 8)], "The cut-off piece is a pyramid with a right triangle base.",
             "the remaining volume.", "the corner pyramid has three perpendicular edges of length " + str(s) + ".",
             [f"Pyramid: base $\\frac{{1}}{{2}} \\cdot {s} \\cdot {s}$, height ${s}$: volume $\\frac{{1}}{{3}} \\cdot \\frac{{{s * s}}}{{2}} \\cdot {s} = {ftex(cut)}$.", f"Remaining: ${s ** 3} - {ftex(cut)} = {ftex(s ** 3 - cut)}$."],
             "giving the volume of the cut-off piece.")


@reg(S, "challenge")
def soc_ant(r):
    a, b, c = sorted([r.randint(1, 10) for _ in range(3)])
    best2 = min((a + b) ** 2 + c * c, (b + c) ** 2 + a * a, (a + c) ** 2 + b * b)
    ans = rad(1, best2) if math.isqrt(best2) ** 2 != best2 else num(math.isqrt(best2))
    p = f"An ant walks on the outside of a ${a} \\times {b} \\times {c}$ box from one corner to the opposite corner. What is the length of the shortest path?"
    sd = a * a + b * b + c * c
    return Q(p, ans, [rad(1, sd) if math.isqrt(sd) ** 2 != sd else num(math.isqrt(sd)), num(a + b + c), rad(1, max((a + b) ** 2 + c * c, (b + c) ** 2 + a * a)) if max((a + b) ** 2 + c * c, (b + c) ** 2 + a * a) != best2 else num(a + b + c + 1), rad(1, best2 + 1), num(a + b + c - 1)],
             "Unfold two faces into a flat rectangle.", "the shortest surface path.", "unfold the two faces the ant crosses into a flat rectangle; the path is its diagonal. Try each way of unfolding.",
             [f"Options: $\\sqrt{{({a} + {b})^2 + {c}^2}} = \\sqrt{{{(a + b) ** 2 + c * c}}}$, $\\sqrt{{({b} + {c})^2 + {a}^2}} = \\sqrt{{{(b + c) ** 2 + a * a}}}$, $\\sqrt{{({a} + {c})^2 + {b}^2}} = \\sqrt{{{(a + c) ** 2 + b * b}}}$.",
              f"Smallest: ${ans.tex}$ (the two shorter edges are added)."],
             "using the space diagonal, which goes through the inside of the box.")


@reg(S, "challenge")
def soc_frustum(r):
    V = r.choice([24, 48, 64, 80, 96, 120, 160])
    f = r.choice([F(1, 2), F(1, 3), F(2, 3)])
    top = V * f ** 3
    ans = V - top
    p = f"A cone has volume ${V}$. It is cut by a plane parallel to its base, ${ftex(f)}$ of the way down from the tip. What is the volume of the bottom piece?"
    return Q(p, ans, [V * (1 - f), top, V - V * f * f, ans + 1, V * (1 - f) ** 3], "The top piece is a small similar cone.",
             "the bottom piece's volume.", "the top is a similar cone with length ratio " + ftex(f) + ", so volume ratio " + ftex(f ** 3) + ".",
             [f"Top cone: ${V} \\cdot {ftex(f ** 3)} = {ftex(top)}$.", f"Bottom: ${V} - {ftex(top)} = {ftex(ans)}$."], "using the length fraction as the volume fraction.")


@reg(S, "challenge")
def soc_archimedes(r):
    rr = r.choice([3, 6, 9])
    ans = kpi(F(2 * rr ** 3, 3))
    p = f"A ball of radius ${rr}$ fits snugly in a cylinder (touching the top, bottom, and sides). What is the volume of the space inside the cylinder around the ball?"
    return Q(p, ans, [kpi(2 * rr ** 3), kpi(F(4 * rr ** 3, 3)), kpi(F(rr ** 3, 3)), kpi(rr ** 3), kpi(F(2 * rr ** 3, 3) + 1)], "The cylinder has radius " + str(rr) + " and height " + str(2 * rr) + ".",
             "the empty volume.", "cylinder volume minus ball volume.",
             [f"Cylinder: $\\pi \\cdot {rr}^2 \\cdot {2 * rr} = {kpi(2 * rr ** 3).tex}$.", f"Ball: $\\frac{{4}}{{3}}\\pi \\cdot {rr}^3 = {kpi(F(4 * rr ** 3, 3)).tex}$.", f"Difference: ${ans.tex}$, exactly one third of the cylinder."],
             "using the radius as the cylinder's height.")


@reg(S, "challenge")
def soc_unpainted(r):
    a, b, c = r.randint(3, 10), r.randint(3, 10), r.randint(3, 10)
    p = f"A ${a} \\times {b} \\times {c}$ block is painted on the outside and cut into unit cubes. How many unit cubes have no paint at all?"
    ans = (a - 2) * (b - 2) * (c - 2)
    return Q(p, ans, [(a - 1) * (b - 1) * (c - 1), a * b * c - 2 * (a * b + b * c + c * a), ans + 1, (a - 2) * (b - 2) * c, a * b * c - ans], "Peel off one layer on every side.",
             "the unpainted cubes.", "the unpainted cubes form an inner block, one layer in from every face.",
             [f"Inner block: $({a} - 2)({b} - 2)({c} - 2) = {a - 2} \\cdot {b - 2} \\cdot {c - 2} = {ans}$."], "removing only one layer per dimension instead of two.")


@reg(S, "challenge")
def soc_tetra(r):
    s = r.choice([3, 6, 12])
    ans = rad(F(s ** 3, 12), 2)
    p = f"What is the volume of a regular tetrahedron (four equilateral triangle faces) with edge ${s}$?"
    return Q(p, ans, [rad(F(s ** 3, 6), 2), rad(F(s ** 3, 12), 3), rad(F(s ** 3, 4), 3), num(F(s ** 3, 6)), rad(F(s ** 3, 24), 2)], "Find its height: the top is above the base's center.",
             "the volume.", "height comes from the right triangle formed by the edge, the height, and the distance from a base corner to the base's center.",
             [f"Base area: $\\frac{{\\sqrt{{3}}}}{{4}} \\cdot {s * s}$.", f"A base corner is $\\frac{{{s}}}{{\\sqrt{{3}}}}$ from the center, so height $= \\sqrt{{{s * s} - \\frac{{{s * s}}}{{3}}}} = {s}\\sqrt{{\\frac{{2}}{{3}}}}$.",
              f"$V = \\frac{{1}}{{3}} \\cdot \\frac{{\\sqrt{{3}}}}{{4}}{s * s} \\cdot {s}\\sqrt{{\\frac{{2}}{{3}}}} = \\frac{{{s ** 3}\\sqrt{{2}}}}{{12}} = {ans.tex}$."],
             "using the slant height of a face as the height.")


@reg(S, "challenge")
def soc_face_areas(r):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    p = f"A rectangular box has faces with areas ${a * b}$, ${b * c}$, and ${c * a}$. What is its volume?"
    return Q(p, a * b * c, [a * b + b * c + c * a, (a * b) * (b * c) * (c * a), a * b * c * 2, a * b * c + 1, F(a * b * b * c * c * a, a * b + b * c)], "Multiply the three areas.",
             "the volume $abc$.", "the product of the three face areas is $(ab)(bc)(ca) = (abc)^2$.",
             [f"$(abc)^2 = {a * b} \\cdot {b * c} \\cdot {c * a} = {(a * b * c) ** 2}$.", f"$abc = {a * b * c}$."], "multiplying the areas without taking the square root.")
