"""Extra AMC 12 problem types (part 1): trigonometry."""
import math
from fractions import Fraction as F

from algebra_more2 import rad
from common import NAMES, C, Q, comb, num

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ft(v):
    return num(F(v)).tex


R2, R3, R6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
CAND = [
    ("0", None, 0), ("1", None, 1), ("\\frac{1}{2}", None, .5), ("\\frac{\\sqrt{2}}{2}", None, R2 / 2), ("\\frac{\\sqrt{3}}{2}", None, R3 / 2),
    ("\\frac{\\sqrt{6} - \\sqrt{2}}{4}", None, (R6 - R2) / 4), ("\\frac{\\sqrt{6} + \\sqrt{2}}{4}", None, (R6 + R2) / 4), ("\\frac{\\sqrt{3}}{3}", None, R3 / 3),
    ("\\sqrt{3}", None, R3), ("2 - \\sqrt{3}", "\\sqrt{3} - 2", 2 - R3), ("2 + \\sqrt{3}", "-2 - \\sqrt{3}", 2 + R3), ("2", None, 2), ("\\sqrt{2}", None, R2),
    ("\\frac{2\\sqrt{3}}{3}", None, 2 * R3 / 3), ("\\sqrt{6} - \\sqrt{2}", "\\sqrt{2} - \\sqrt{6}", R6 - R2), ("\\sqrt{6} + \\sqrt{2}", "-\\sqrt{6} - \\sqrt{2}", R6 + R2),
    ("\\frac{3}{2}", None, 1.5), ("\\frac{1}{4}", None, .25), ("\\frac{\\sqrt{3}}{4}", None, R3 / 4), ("\\frac{3}{4}", None, .75),
    ("\\sqrt{2} - 1", "1 - \\sqrt{2}", R2 - 1), ("\\sqrt{2} + 1", "-1 - \\sqrt{2}", R2 + 1), ("\\frac{1 + \\sqrt{3}}{2}", "-\\frac{1 + \\sqrt{3}}{2}", (1 + R3) / 2),
    ("\\frac{\\sqrt{3} - 1}{2}", "\\frac{1 - \\sqrt{3}}{2}", (R3 - 1) / 2), ("\\frac{\\sqrt{6}}{2}", None, R6 / 2), ("\\frac{\\sqrt{3}}{8}", None, R3 / 8), ("\\frac{1}{8}", None, .125),
    ("\\frac{3\\sqrt{3}}{2}", None, 3 * R3 / 2), ("2\\sqrt{2}", None, 2 * R2), ("3", None, 3),
]


def ex(v):
    """Exact choice for a value from the table above."""
    for t, nt, c in CAND:
        if abs(abs(v) - c) < 1e-9:
            if v < -1e-12:
                return C(nt or "-" + t, v)
            return C(t, v)
    raise ValueError(f"no exact form for {v}")


def exw(v, r, k=6):
    """Wrong exact choices near v."""
    pool = []
    for t, nt, c in CAND:
        for s in (1, -1):
            w = s * c
            if abs(w - v) > 1e-9 and (s == 1 or c > 0):
                pool.append(ex(w))
    pool.sort(key=lambda ch: abs(ch.key - v))
    near = pool[:10]
    r.shuffle(near)
    return near[:k]


def sind(d):
    v = math.sin(math.radians(d))
    return 0.0 if abs(v) < 1e-12 else v


def cosd(d):
    v = math.cos(math.radians(d))
    return 0.0 if abs(v) < 1e-12 else v


def deg_rad(d):
    """d degrees as a multiple of pi, LaTeX."""
    k = F(d, 180)
    if k == 0:
        return "0"
    if k.denominator == 1:
        return ("" if k == 1 else "-" if k == -1 else str(k.numerator)) + "\\pi"
    return ("-" if k < 0 else "") + f"\\frac{{{'' if abs(k.numerator) == 1 else abs(k.numerator)}\\pi}}{{{k.denominator}}}"


def PI(k):
    k = F(k)
    return C(deg_rad(k * 180), float(k) * math.pi)


def DG(d):
    return C(f"{d}^\\circ", d)


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]

# ================================================================ trig_values
S = "trig_values"


@reg(S, "basics")
def tv_cos_deg(r):
    d = r.choice([a for a in range(0, 360, 15) if a % 90])
    v = cosd(d)
    p = f"What is $\\cos {d}^\\circ$?"
    ref = min(d % 180, 180 - d % 180)
    return Q(p, ex(v), exw(v, r), "Find the reference angle and the sign.",
             f"$\\cos {d}^\\circ$.", "cosine is positive in quadrants I and IV, negative in II and III.",
             [f"Reference angle: ${ref}^\\circ$, so $|\\cos {d}^\\circ| = \\cos {ref}^\\circ = {ex(abs(v)).tex}$.", f"Quadrant {['I', 'II', 'III', 'IV'][d // 90]}: cosine is {'positive' if v > 0 else 'negative'}.", f"$\\cos {d}^\\circ = {ex(v).tex}$."],
             "getting the sign wrong.")


@reg(S, "basics")
def tv_reciprocal(r):
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
    f = r.choice(["sec", "csc", "cot"])
    s, c = sind(d), cosd(d)
    v = {"sec": 1 / c, "csc": 1 / s, "cot": c / s}[f]
    base = {"sec": ("\\cos", c), "csc": ("\\sin", s), "cot": ("\\tan", s / c)}[f]
    p = f"What is $\\{f} {d}^\\circ$?"
    return Q(p, ex(v), exw(v, r), f"$\\{f}$ is the reciprocal of ${base[0]}$.",
             f"$\\{f} {d}^\\circ$.", f"$\\{f} x = \\frac{{1}}{{{base[0]} x}}$.",
             [f"${base[0]} {d}^\\circ = {ex(base[1]).tex}$.", f"Reciprocal: ${ex(v).tex}$."], f"using ${base[0]}$ itself instead of its reciprocal.")


@reg(S, "basics")
def tv_rad_to_deg(r):
    k = F(r.randint(1, 23), r.choice([3, 4, 6, 12, 5, 9]))
    d = k * 180
    if d.denominator != 1 or d > 720:
        return None
    d = int(d)
    p = f"What is ${deg_rad(d)}$ radians in degrees?"
    return Q(p, DG(d), [DG(int(k * 360)) if k * 360 < 1440 else DG(d + 90), DG(int(k * 90)) if (k * 90).denominator == 1 else DG(d + 30), DG(d + 180), DG(abs(d - 30)), DG(d + 45)], "$\\pi$ radians is $180^\\circ$.",
             "the angle in degrees.", "multiply by $\\frac{180^\\circ}{\\pi}$.",
             [f"${deg_rad(d)} \\cdot \\frac{{180^\\circ}}{{\\pi}} = {d}^\\circ$."], "using $\\pi = 360^\\circ$.")


@reg(S, "basics")
def tv_reference(r):
    d = r.choice([x for x in range(95, 360, 5) if x % 90])
    ref = d if d < 90 else 180 - d if d < 180 else d - 180 if d < 270 else 360 - d
    p = f"What is the reference angle of ${d}^\\circ$?"
    return Q(p, DG(ref), [DG(180 - ref) if 180 - ref != ref else DG(ref + 10), DG(abs(360 - d)) if abs(360 - d) != ref else DG(ref + 5), DG(abs(d - 180)) if abs(d - 180) != ref else DG(ref + 15), DG(90 - ref) if 90 - ref != ref else DG(ref + 20), DG(ref + 90)], "The acute angle to the $x$-axis.",
             "the reference angle.", "measure the acute angle between the terminal side and the $x$-axis.",
             [f"${d}^\\circ$ is in quadrant {['I', 'II', 'III', 'IV'][d // 90]}.", f"Reference angle: ${ref}^\\circ$."], "measuring to the $y$-axis.")


@reg(S, "basics")
def tv_coterminal(r):
    d = r.choice([r.randint(361, 1500), -r.randint(10, 900)])
    ans = d % 360
    if ans == 0:
        return None
    p = f"What angle between $0^\\circ$ and $360^\\circ$ is coterminal with ${d}^\\circ$?"
    return Q(p, DG(ans), [DG((360 - ans) % 360 or 180), DG((ans + 180) % 360 or 90), DG(abs(d) % 360) if abs(d) % 360 != ans else DG((ans + 90) % 360), DG((ans + 270) % 360 or 45), DG((ans + 30) % 360)], "Add or subtract $360^\\circ$.",
             "the coterminal angle.", "coterminal angles differ by multiples of $360^\\circ$.",
             [f"${d} {'-' if d > 0 else '+'} {abs(d - ans)} = {ans}$, a multiple of $360$ away."], "dropping the negative sign.")


@reg(S, "basics")
def tv_quadrant(r):
    q = r.randint(1, 4)
    sgn = {1: (1, 1), 2: (1, -1), 3: (-1, -1), 4: (-1, 1)}[q]
    pair = r.choice([("\\sin", "\\cos", sgn[0], sgn[1]), ("\\sin", "\\tan", sgn[0], sgn[0] * sgn[1]), ("\\cos", "\\tan", sgn[1], sgn[0] * sgn[1])])
    w = lambda s: ">" if s > 0 else "<"
    p = f"An angle $\\theta$ satisfies ${pair[0]}\\theta {w(pair[2])} 0$ and ${pair[1]}\\theta {w(pair[3])} 0$. Which quadrant is $\\theta$ in?"
    names = ["I", "II", "III", "IV"]
    ans = C(f"\\text{{{names[q - 1]}}}", q)
    wrong = [C(f"\\text{{{names[i - 1]}}}", i) for i in range(1, 5) if i != q] + [C("\\text{none}", 5)]
    return Q(p, ans, wrong, "All Students Take Calculus: All, Sine, Tangent, Cosine positive in I, II, III, IV.",
             "the quadrant.", "check the signs: sin is the $y$-coordinate, cos the $x$-coordinate, tan their ratio.",
             [f"Quadrant {names[q - 1]}: $\\sin$ {'+' if sgn[0] > 0 else '-'}, $\\cos$ {'+' if sgn[1] > 0 else '-'}, $\\tan$ {'+' if sgn[0] * sgn[1] > 0 else '-'}.", "It matches both conditions."], "mixing up which function is the $x$-coordinate.")


@reg(S, "basics")
def tv_arc(r):
    R = r.randint(2, 15)
    d = r.choice([20, 30, 36, 40, 45, 60, 72, 90, 120, 135, 150, 210, 240, 270])
    ans = F(R * d, 180)
    p = f"What is the length of an arc of a circle of radius ${R}$ cut off by a central angle of ${d}^\\circ$?"
    return Q(p, PI(ans), [PI(ans * 2), PI(ans / 2), C(ft(ans * 180 / 180 * 1), float(ans)), PI(F(R * R * d, 360)), PI(ans + 1)], "Arc length $= r\\theta$ with $\\theta$ in radians.",
             "the arc length.", "convert to radians, then multiply by the radius.",
             [f"${d}^\\circ = {deg_rad(d)}$.", f"${R} \\cdot {deg_rad(d)} = {deg_rad(ans * 180)}$."], "using the sector area formula.")


@reg(S, "basics")
def tv_sector_area(r):
    R = r.randint(2, 12)
    k = F(r.randint(1, 7), r.choice([3, 4, 6]))
    ans = F(R * R, 2) * k
    p = f"A sector of a circle of radius ${R}$ has central angle ${deg_rad(k * 180)}$ radians. What is its area?"
    return Q(p, PI(ans), [PI(ans * 2), PI(R * k), PI(ans / 2), PI(R * R * k), PI(ans + F(1, 2))], "Area $= \\frac{1}{2} r^2 \\theta$.",
             "the area.", "a sector is the fraction $\\frac{\\theta}{2\\pi}$ of the circle.",
             [f"$\\frac{{1}}{{2}} \\cdot {R * R} \\cdot {deg_rad(k * 180)} = {deg_rad(ans * 180)}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "basics")
def tv_negative(r):
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 240, 300, 330])
    f = r.choice(["sin", "cos", "tan"])
    v = {"sin": sind(-d), "cos": cosd(-d), "tan": sind(-d) / cosd(-d)}[f]
    p = f"What is $\\{f}(-{d}^\\circ)$?"
    return Q(p, ex(v), exw(v, r), "Sine and tangent are odd; cosine is even.",
             f"$\\{f}(-{d}^\\circ)$.", f"$\\{f}(-x) = {'' if f == 'cos' else '-'}\\{f} x$.",
             [f"$\\{f} {d}^\\circ = {ex(-v if f != 'cos' else v).tex}$.", f"So $\\{f}(-{d}^\\circ) = {ex(v).tex}$."], "treating every function as odd (or even).")


@reg(S, "basics")
def tv_tan_from_cos(r):
    a, b, c = r.choice(TRIPLES)
    q = r.choice([2, 3, 4])
    cs = {2: -1, 3: -1, 4: 1}[q]
    sn = {2: 1, 3: -1, 4: -1}[q]
    cosv, tanv = F(cs * a, c), F(sn * b, cs * a)
    p = f"An angle $\\theta$ in quadrant {['', 'I', 'II', 'III', 'IV'][q]} has $\\cos\\theta = {ft(cosv)}$. What is $\\tan\\theta$?"
    return Q(p, tanv, [-tanv, F(b, c), F(a, b), -F(a, b) if -F(a, b) != tanv else F(a, b) + 1, F(sn * b, c)], "Find $\\sin\\theta$ with the Pythagorean identity.",
             "$\\tan\\theta$.", "$\\sin^2\\theta = 1 - \\cos^2\\theta$; the quadrant gives the sign.",
             [f"$\\sin\\theta = {'' if sn > 0 else '-'}\\frac{{{b}}}{{{c}}}$ (quadrant {['', 'I', 'II', 'III', 'IV'][q]}).", f"$\\tan\\theta = \\frac{{\\sin\\theta}}{{\\cos\\theta}} = {ft(tanv)}$."], "ignoring the quadrant's signs.")


@reg(S, "basics")
def tv_point(r):
    a, b, c = r.choice(TRIPLES)
    k = r.randint(1, 3)
    x, y = r.choice([1, -1]) * a * k, r.choice([1, -1]) * b * k
    f = r.choice(["sin", "cos"])
    v = F(y, c * k) if f == "sin" else F(x, c * k)
    p = f"The terminal side of angle $\\theta$ passes through $({x}, {y})$. What is $\\{f}\\theta$?"
    return Q(p, v, [-v, F(x, c * k) if f == "sin" else F(y, c * k), F(y, x), F(x, y), F(y if f == "sin" else x, a + b)], "Use the distance from the origin.",
             f"$\\{f}\\theta$.", "$\\sin\\theta = \\frac{y}{r}$, $\\cos\\theta = \\frac{x}{r}$, with $r = \\sqrt{x^2 + y^2}$.",
             [f"$r = \\sqrt{{{x * x} + {y * y}}} = {c * k}$.", f"$\\{f}\\theta = {ft(v)}$."], "swapping $x$ and $y$.")


@reg(S, "basics")
def tv_product(r):
    items = [("\\sin 60^\\circ \\tan 60^\\circ", 1.5), ("\\sin 45^\\circ \\cos 45^\\circ", .5), ("\\tan 30^\\circ \\tan 60^\\circ", 1), ("\\sin 30^\\circ \\cos 60^\\circ", .25),
             ("\\sec 60^\\circ \\cos 60^\\circ", 1), ("\\sin 60^\\circ \\cos 30^\\circ", .75), ("\\tan 45^\\circ \\sin 30^\\circ", .5), ("\\cos 30^\\circ \\tan 30^\\circ", .5),
             ("\\csc 30^\\circ \\sin 45^\\circ", R2), ("\\sec 45^\\circ \\sin 45^\\circ", 1), ("\\cos 30^\\circ \\sin 30^\\circ", R3 / 4)]
    e, v = r.choice(items)
    p = f"What is ${e}$?"
    return Q(p, ex(v), exw(v, r), "Replace each function with its exact value.",
             "the value.", "use the $30$-$60$-$90$ and $45$-$45$-$90$ triangles.", [f"Multiplying the exact values gives ${ex(v).tex}$."], "mixing up $\\sin 30^\\circ$ and $\\sin 60^\\circ$.")


@reg(S, "basics")
def tv_inverse(r):
    f, v, ans = r.choice([("\\arcsin", R3 / 2, 60), ("\\arcsin", -.5, -30), ("\\arccos", -.5, 120), ("\\arccos", -R2 / 2, 135), ("\\arctan", -1, -45), ("\\arctan", R3, 60),
                          ("\\arccos", R3 / 2, 30), ("\\arcsin", -R2 / 2, -45), ("\\arctan", -R3 / 3, -30), ("\\arccos", -R3 / 2, 150)])
    p = f"What is ${f}\\left({ex(v).tex}\\right)$, in degrees?"
    return Q(p, DG(ans), [DG(-ans), DG(180 - ans), DG(ans + 360 if ans < 0 else 360 - ans), DG(90 - ans), DG(ans + 180)], "Remember the principal ranges.",
             "the angle.", "$\\arcsin$ and $\\arctan$ give angles from $-90^\\circ$ to $90^\\circ$; $\\arccos$ gives $0^\\circ$ to $180^\\circ$.",
             [f"The angle in that range with the right value is ${ans}^\\circ$."], "giving an angle outside the principal range.")


@reg(S, "basics")
def tv_clock(r):
    h = r.randint(1, 11)
    ang = min(h, 12 - h) * 30
    p = f"What is the smaller angle between the hands of a clock at {h}:00, in radians?"
    return Q(p, PI(F(ang, 180)), [PI(F(360 - ang, 180)), PI(F(h, 6)) if h <= 6 else PI(F(ang, 180) + F(1, 6)), PI(F(ang, 360)), PI(F(ang, 180) + F(1, 12)), C(ft(F(ang, 30)), ang / 30 + 0.001)], "Each hour mark is $30^\\circ$.",
             "the angle.", "count hour marks between the hands.",
             [f"${min(h, 12 - h)} \\cdot 30^\\circ = {ang}^\\circ = {deg_rad(ang)}$."], "giving the larger angle.")


@reg(S, "basics")
def tv_sin_plus_cos(r):
    d = r.choice([a for a in range(0, 360, 30) if a % 90] + [45, 135, 225, 315])
    v = sind(d) + cosd(d)
    p = f"What is $\\sin {d}^\\circ + \\cos {d}^\\circ$?"
    return Q(p, ex(v), exw(v, r), "Find each value, then add.",
             "the sum.", "use the reference angle and signs for each.",
             [f"$\\sin {d}^\\circ = {ex(sind(d)).tex}$, $\\cos {d}^\\circ = {ex(cosd(d)).tex}$.", f"Sum: ${ex(v).tex}$."], "using the wrong sign for one of them.")


@reg(S, "basics")
def tv_tan_deg(r):
    d = r.choice([a for a in range(0, 360, 15) if a % 90])
    v = sind(d) / cosd(d)
    p = f"What is $\\tan {d}^\\circ$?"
    return Q(p, ex(v), exw(v, r), "Tangent repeats every $180^\\circ$.",
             f"$\\tan {d}^\\circ$.", "use the reference angle; tangent is positive in quadrants I and III.",
             [f"$\\tan {d}^\\circ = \\tan {d % 180}^\\circ = {ex(v).tex}$" + (" (using $\\tan 15^\\circ = 2 - \\sqrt{3}$ and $\\tan 75^\\circ = 2 + \\sqrt{3}$)." if d % 45 and d % 30 else ".")], "getting the sign wrong.")


@reg(S, "challenge")
def tvc_polygon_area(r):
    n = r.choice([3, 4, 6, 8, 12])
    R_ = r.randint(1, 4)
    v = F(n, 2) * R_ * R_
    fac = {3: R3 / 2, 4: 1, 6: R3 / 2, 8: R2 / 2, 12: .5}[n]
    val = float(v) * fac
    tex = {3: rad(v / 2, 3), 4: num(v), 6: rad(v / 2, 3), 8: rad(v / 2, 2), 12: num(v / 2)}[n]
    p = f"A regular ${n}$-gon is inscribed in a circle of radius ${R_}$. What is its area?"
    w = [rad(v / 2, 2) if n != 8 else rad(v / 2, 3), num(v) if n != 4 else num(v + 1), rad(v, 3) if n not in (3, 6) else rad(v / 4, 3), num(v / 2 + 1), rad(v / 3, 3)]
    return Q(p, tex, w, "Split it into " + str(n) + " triangles from the center.",
             "the area.", f"each triangle has two sides ${R_}$ with angle $\\frac{{360^\\circ}}{{{n}}} = {360 // n}^\\circ$ between them.",
             [f"One triangle: $\\frac{{1}}{{2}} \\cdot {R_}^2 \\sin {360 // n}^\\circ$.", f"Times ${n}$: ${tex.tex}$."], "using the side length as the radius.")


@reg(S, "challenge")
def tvc_half_angles(r):
    e, v = r.choice([("\\tan 22.5^\\circ", R2 - 1), ("\\tan 67.5^\\circ", R2 + 1), ("\\tan 15^\\circ", 2 - R3), ("\\tan 75^\\circ", 2 + R3), ("\\tan 105^\\circ", -2 - R3), ("\\tan 165^\\circ", R3 - 2)])
    p = f"What is ${e}$?"
    return Q(p, ex(v), exw(v, r), "Use $\\tan\\frac{\\theta}{2} = \\frac{1 - \\cos\\theta}{\\sin\\theta}$ or angle sums.",
             "the exact value.", "write the angle as half of, or a sum of, standard angles.",
             [f"Working it out gives ${ex(v).tex}$."], "using the reciprocal value.")


@reg(S, "challenge")
def tvc_sin_sq_sum(r):
    n = r.randint(3, 12)
    ans = F(n, 2)
    p = f"What is $\\displaystyle\\sum_{{k=0}}^{{{n - 1}}} \\sin^2\\left(\\frac{{k\\pi}}{{{n}}}\\right)$?"
    return Q(p, ans, [F(n - 1, 2), F(n + 1, 2), F(n, 1), F(n, 4), F(n - 1, 1)], "Write $\\sin^2 x = \\frac{1 - \\cos 2x}{2}$.",
             "the sum.", "the cosines of $\\frac{2k\\pi}{" + str(n) + "}$ for $k = 0, \\ldots, " + str(n - 1) + "$ add to $0$ (roots of unity).",
             [f"$\\sum \\frac{{1 - \\cos(2k\\pi/{n})}}{{2}} = \\frac{{{n}}}{{2}} - \\frac{{1}}{{2}} \\cdot 0 = {ft(ans)}$."], "pairing terms incorrectly.")


@reg(S, "challenge")
def tvc_count_compare(r):
    step = r.choice([10, 15, 30])
    kind = r.choice(["sc", "tan", "abs"])
    test = {"sc": lambda d: sind(d) > cosd(d) + 1e-9, "tan": lambda d: abs(cosd(d)) > 1e-9 and sind(d) / cosd(d) > 1 + 1e-9, "abs": lambda d: abs(sind(d)) > abs(cosd(d)) + 1e-9}[kind]
    cnt = sum(1 for d in range(0, 360, step) if test(d))
    desc = {"sc": "$\\sin\\theta > \\cos\\theta$", "tan": "$\\tan\\theta > 1$", "abs": "$|\\sin\\theta| > |\\cos\\theta|$"}[kind]
    p = f"How many angles $\\theta$ among $0^\\circ, {step}^\\circ, {2 * step}^\\circ, \\ldots, {360 - step}^\\circ$ satisfy {desc}?"
    return Q(p, cnt, [cnt + 1, cnt - 1, 360 // step // 2, cnt + 2, cnt * 2 if cnt * 2 != 360 // step // 2 else cnt + 3], "Find the arcs where it holds; watch the endpoints.",
             "the count.", {"sc": "$\\sin\\theta > \\cos\\theta$ exactly for $45^\\circ < \\theta < 225^\\circ$.", "tan": "$\\tan\\theta > 1$ for $45^\\circ < \\theta < 90^\\circ$ and $225^\\circ < \\theta < 270^\\circ$.", "abs": "$|\\sin\\theta| > |\\cos\\theta|$ when $\\theta$ is within $45^\\circ$ of $90^\\circ$ or $270^\\circ$."}[kind],
             [f"Counting the listed angles strictly inside those arcs: ${cnt}$."], "including the endpoints where equality holds.")


@reg(S, "challenge")
def tvc_cos_product(r):
    e, v = r.choice([("\\cos 20^\\circ \\cos 40^\\circ \\cos 80^\\circ", .125), ("\\sin 20^\\circ \\sin 40^\\circ \\sin 80^\\circ", R3 / 8), ("\\sin 10^\\circ \\sin 50^\\circ \\sin 70^\\circ", .125),
                     ("\\cos 10^\\circ \\cos 50^\\circ \\cos 70^\\circ", R3 / 8), ("\\sin 15^\\circ \\cos 15^\\circ", .25), ("\\cos^2 15^\\circ - \\sin^2 15^\\circ", R3 / 2)])
    p = f"What is ${e}$?"
    return Q(p, ex(v), exw(v, r), "Use $\\sin x \\sin(60^\\circ - x)\\sin(60^\\circ + x) = \\frac{1}{4}\\sin 3x$ (and the cosine version), or double angles.",
             "the value.", "triple-angle product identities: $\\cos x \\cos(60^\\circ - x)\\cos(60^\\circ + x) = \\frac{1}{4}\\cos 3x$.",
             [f"Applying the identity gives ${ex(v).tex}$."], "multiplying approximate decimals.")


@reg(S, "challenge")
def tvc_tan_product(r):
    a = r.randint(1, 30)
    p = f"What is $\\tan {a}^\\circ \\cdot \\tan {a + 1}^\\circ \\cdots \\tan {89 - a}^\\circ \\cdot \\tan {90 - a}^\\circ$?"
    return Q(p, 1, [0, F(1, 2), 2, 90 - 2 * a, -1], "Pair $\\tan x$ with $\\tan(90^\\circ - x)$.",
             "the product.", "$\\tan x \\tan(90^\\circ - x) = \\tan x \\cot x = 1$.",
             [f"The angles pair up as $({a}, {90 - a})$, $({a + 1}, {89 - a})$, ...; the middle one, if any, is $\\tan 45^\\circ = 1$.", "Every pair gives $1$, so the product is $1$."], "thinking the product is 0.")


@reg(S, "challenge")
def tvc_cos_sum_pi(r):
    n = r.randint(3, 12)
    m = r.randint(1, n - 1)
    ans = sum(math.cos(2 * math.pi * k * m / n) for k in range(n))
    p = f"What is $\\displaystyle\\sum_{{k=1}}^{{{n}}} \\cos\\left(\\frac{{{2 * m}k\\pi}}{{{n}}}\\right)$?"
    return Q(p, 0, [1, -1, n, F(n, 2), F(-1, 2)], "These are real parts of roots of unity.",
             "the sum.", f"$e^{{{2 * m}k\\pi i/{n}}}$ for $k = 1$ to ${n}$ runs over the ${n}$th roots of unity" + ("" if math.gcd(m, n) == 1 else " (with repeats)") + ", which add to $0$ since $" + str(m) + "$ is not a multiple of $" + str(n) + "$.",
             ["Real part of $0$: $0$."], "assuming the sum is $1$.") if abs(ans) < 1e-9 else None


# ================================================================ trig_identities
S = "trig_identities"


@reg(S, "basics")
def ti_sin2(r):
    a, b, c = r.choice(TRIPLES)
    v = F(2 * a * b, c * c)
    p = f"If $\\sin\\theta = \\frac{{{a}}}{{{c}}}$ and $\\theta$ is acute, what is $\\sin 2\\theta$?"
    return Q(p, v, [F(2 * a, c), F(b * b - a * a, c * c), F(a * b, c * c), F(2 * a * a, c * c), F(2 * b, c)], "$\\sin 2\\theta = 2\\sin\\theta\\cos\\theta$.",
             "$\\sin 2\\theta$.", "find $\\cos\\theta$, then use the double-angle formula.",
             [f"$\\cos\\theta = \\frac{{{b}}}{{{c}}}$.", f"$2 \\cdot \\frac{{{a}}}{{{c}}} \\cdot \\frac{{{b}}}{{{c}}} = {ft(v)}$."], "doubling $\\sin\\theta$.")


@reg(S, "basics")
def ti_tan2(r):
    t = F(r.randint(1, 5), r.randint(2, 7))
    if t * t == 1:
        return None
    v = 2 * t / (1 - t * t)
    p = f"If $\\tan\\theta = {ft(t)}$, what is $\\tan 2\\theta$?"
    return Q(p, v, [2 * t, 2 * t / (1 + t * t), t * t, -v, 1 / v if v != 0 else F(1, 2)], "$\\tan 2\\theta = \\frac{2\\tan\\theta}{1 - \\tan^2\\theta}$.",
             "$\\tan 2\\theta$.", "the double-angle formula for tangent.",
             [f"$\\frac{{2 \\cdot {ft(t)}}}{{1 - {ft(t * t)}}} = {ft(v)}$."], "doubling the tangent.")


@reg(S, "basics")
def ti_simplify(r):
    items = [("\\dfrac{\\sin\\theta}{\\csc\\theta} + \\dfrac{\\cos\\theta}{\\sec\\theta}", "1"), ("(1 + \\tan^2\\theta)\\cos^2\\theta", "1"), ("\\dfrac{\\sec\\theta - \\cos\\theta}{\\tan\\theta}", "\\sin\\theta"),
             ("\\sin\\theta \\cot\\theta", "\\cos\\theta"), ("\\dfrac{1 - \\cos^2\\theta}{\\sin\\theta}", "\\sin\\theta"), ("\\tan\\theta \\cos\\theta \\csc\\theta", "1"),
             ("\\sec^2\\theta - \\tan^2\\theta", "1"), ("\\dfrac{\\tan\\theta}{\\sec\\theta}", "\\sin\\theta"), ("\\cos\\theta (\\sec\\theta - \\cos\\theta)", "\\sin^2\\theta"), ("\\dfrac{\\cot\\theta}{\\csc\\theta}", "\\cos\\theta")]
    e, a = r.choice(items)
    opts = ["1", "\\sin\\theta", "\\cos\\theta", "\\tan\\theta", "\\sin^2\\theta", "\\sec\\theta"]
    keys = {o: i for i, o in enumerate(opts)}
    p = f"Which expression equals ${e}$ for all $\\theta$ where it is defined?"
    return Q(p, C(a, keys[a]), [C(o, keys[o]) for o in opts if o != a], "Rewrite everything in sines and cosines.",
             "the simplified form.", "use $\\sec = \\frac{1}{\\cos}$, $\\csc = \\frac{1}{\\sin}$, $\\tan = \\frac{\\sin}{\\cos}$, and $\\sin^2 + \\cos^2 = 1$.",
             [f"Simplifying gives ${a}$."], "canceling terms that aren't factors.")


@reg(S, "basics")
def ti_cos_diff(r):
    (a1, b1, c1), (a2, b2, c2) = r.sample(TRIPLES, 2)
    sA, cA, sB, cB = F(a1, c1), F(b1, c1), F(a2, c2), F(b2, c2)
    kind = r.choice(["cos-", "cos+", "sin+", "sin-"])
    v = {"cos-": cA * cB + sA * sB, "cos+": cA * cB - sA * sB, "sin+": sA * cB + cA * sB, "sin-": sA * cB - cA * sB}[kind]
    form = {"cos-": "\\cos(A - B)", "cos+": "\\cos(A + B)", "sin+": "\\sin(A + B)", "sin-": "\\sin(A - B)"}[kind]
    alt = {"cos-": cA * cB - sA * sB, "cos+": cA * cB + sA * sB, "sin+": sA * cB - cA * sB, "sin-": sA * cB + cA * sB}[kind]
    p = f"Acute angles $A$ and $B$ have $\\sin A = {ft(sA)}$ and $\\sin B = {ft(sB)}$. What is ${form}$?"
    return Q(p, v, [alt, -v, sA * sB, cA * cB, sA + sB if sA + sB < 2 else alt + 1], "Find the cosines, then use the sum/difference formula.",
             f"${form}$.", "angle addition formulas.",
             [f"$\\cos A = {ft(cA)}$, $\\cos B = {ft(cB)}$.", f"${form} = {ft(v)}$."], "using the wrong sign in the formula.")


@reg(S, "basics")
def ti_cos2_from_cos(r):
    a, b, c = r.choice(TRIPLES)
    cv = F(r.choice([a, b]), c)
    v = 2 * cv * cv - 1
    p = f"If $\\cos\\theta = {ft(cv)}$, what is $\\cos 2\\theta$?"
    return Q(p, v, [2 * cv, 1 - 2 * cv * cv, cv * cv, 2 * cv * cv, -v + F(1, c * c)], "$\\cos 2\\theta = 2\\cos^2\\theta - 1$.",
             "$\\cos 2\\theta$.", "double-angle formula in terms of cosine.",
             [f"$2 \\cdot {ft(cv * cv)} - 1 = {ft(v)}$."], "doubling $\\cos\\theta$.")


@reg(S, "basics")
def ti_half(r):
    cv = F(r.randint(-7, 7), r.choice([8, 9, 25]))
    v = (1 + cv) / 2
    p = f"If $\\cos\\theta = {ft(cv)}$, what is $\\cos^2\\frac{{\\theta}}{{2}}$?"
    return Q(p, v, [(1 - cv) / 2, cv / 2, cv * cv, (1 + cv), v + F(1, 4)], "Half-angle formula.",
             "$\\cos^2\\frac{\\theta}{2}$.", "$\\cos^2\\frac{\\theta}{2} = \\frac{1 + \\cos\\theta}{2}$.",
             [f"$\\frac{{1 {'+' if cv > 0 else '-'} {ft(abs(cv))}}}{{2}} = {ft(v)}$."], "using $1 - \\cos\\theta$.") if cv != 0 else None


@reg(S, "basics")
def ti_diff_sq(r):
    k = F(r.randint(1, 4), r.randint(5, 9))
    v = 1 - 2 * k
    p = f"If $\\sin x \\cos x = {ft(k)}$, what is $(\\sin x - \\cos x)^2$?"
    return Q(p, v, [1 + 2 * k, 1 - k, 2 * k, k * k, 1 - 4 * k if 1 - 4 * k != v else v + 1], "Expand the square.",
             "the value.", "$(\\sin x - \\cos x)^2 = \\sin^2 x + \\cos^2 x - 2\\sin x\\cos x$.",
             [f"$1 - 2 \\cdot {ft(k)} = {ft(v)}$."], "using $+2\\sin x \\cos x$.")


@reg(S, "basics")
def ti_tan_cot(r):
    k = F(r.randint(1, 4), r.randint(5, 11))
    v = 1 / k
    p = f"If $\\sin x \\cos x = {ft(k)}$, what is $\\tan x + \\cot x$?"
    return Q(p, v, [k, 2 * k, 2 / k, 1 - k, 1 / (2 * k)], "Combine into one fraction.",
             "the value.", "$\\tan x + \\cot x = \\frac{\\sin^2 x + \\cos^2 x}{\\sin x \\cos x} = \\frac{1}{\\sin x\\cos x}$.",
             [f"$\\frac{{1}}{{{ft(k)}}} = {ft(v)}$."], "adding the numerators without a common denominator.")


@reg(S, "basics")
def ti_cos4_sin4(r):
    a, b, c = r.choice(TRIPLES)
    cv = F(r.choice([a, b]), c)
    v = 2 * cv * cv - 1
    p = f"If $\\cos\\theta = {ft(cv)}$, what is $\\cos^4\\theta - \\sin^4\\theta$?"
    return Q(p, v, [cv ** 4 - (1 - cv * cv) ** 2 + F(1, c), 1 - 2 * cv * cv, cv ** 4, 1, cv * cv], "Factor as a difference of squares.",
             "the value.", "$\\cos^4 - \\sin^4 = (\\cos^2 + \\sin^2)(\\cos^2 - \\sin^2) = \\cos 2\\theta$.",
             [f"$\\cos^2\\theta - \\sin^2\\theta = {ft(cv * cv)} - {ft(1 - cv * cv)} = {ft(v)}$."], "computing $\\sin^4$ with the wrong sign.")


@reg(S, "basics")
def ti_sq_range(r):
    a, b = r.sample(range(1, 10), 2)
    c = r.randint(-5, 5)
    ask = r.choice(["max", "min"])
    v = (max(a, b) if ask == "max" else min(a, b)) + c
    p = f"What is the {'maximum' if ask == 'max' else 'minimum'} value of ${a}\\sin^2 x + {b}\\cos^2 x {'+' if c >= 0 else '-'} {abs(c)}$?"
    return Q(p, v, [a + b + c, (min(a, b) if ask == "max" else max(a, b)) + c, v + 1, F(a + b, 2) + c, v - 1], "Replace $\\cos^2 x$ with $1 - \\sin^2 x$.",
             "the extreme value.", f"the expression is ${b} + ({a} - {b})\\sin^2 x {'+' if c >= 0 else '-'} {abs(c)}$, and $\\sin^2 x$ ranges from $0$ to $1$.",
             [f"At the extremes: ${b + c}$ and ${a + c}$.", f"The {'larger' if ask == 'max' else 'smaller'}: ${v}$."], "adding both coefficients.")


@reg(S, "basics")
def ti_cofunction(r):
    x = r.randint(5, 85)
    p = f"If $\\sin {x}^\\circ = \\cos y^\\circ$ with $0 < y < 90$, what is $y$?"
    return Q(p, 90 - x, [x, 180 - x, 90 + x if 90 + x < 180 else x + 1, 360 - x, abs(45 - x) if abs(45 - x) not in (x, 90 - x) else x + 2], "Complementary angles.",
             "$y$.", "$\\sin x^\\circ = \\cos(90 - x)^\\circ$.", [f"$y = 90 - {x} = {90 - x}$."], "answering $" + str(x) + "$.")


@reg(S, "basics")
def ti_sum_product(r):
    e, v = r.choice([("\\sin 75^\\circ + \\sin 15^\\circ", R6 / 2), ("\\cos 75^\\circ + \\cos 15^\\circ", R6 / 2), ("\\sin 75^\\circ - \\sin 15^\\circ", R2 / 2),
                     ("\\cos 15^\\circ - \\cos 75^\\circ", R2 / 2), ("\\sin 105^\\circ + \\sin 15^\\circ", R6 / 2), ("\\cos 105^\\circ + \\cos 15^\\circ", R2 / 2)])
    p = f"What is ${e}$?"
    return Q(p, ex(v), exw(v, r), "Sum-to-product.",
             "the value.", "$\\sin A \\pm \\sin B$ and $\\cos A \\pm \\cos B$ turn into products of half-sum and half-difference angles.",
             [f"Applying sum-to-product gives ${ex(v).tex}$."], "adding the angles first.")


@reg(S, "basics")
def ti_tan_diff(r):
    a, b = F(r.randint(1, 6), r.randint(2, 7)), F(r.randint(1, 6), r.randint(2, 7))
    if a == b or a * b == -1:
        return None
    v = (a - b) / (1 + a * b)
    p = f"If $\\tan A = {ft(a)}$ and $\\tan B = {ft(b)}$, what is $\\tan(A - B)$?"
    return Q(p, v, [a - b, (a - b) / (1 - a * b) if a * b != 1 else v + 1, (a + b) / (1 - a * b) if a * b != 1 else v + 2, -v, v + F(1, 2)], "$\\tan(A - B) = \\frac{\\tan A - \\tan B}{1 + \\tan A \\tan B}$.",
             "$\\tan(A - B)$.", "the tangent difference formula.",
             [f"$\\frac{{{ft(a)} - {ft(b)}}}{{1 + {ft(a * b)}}} = {ft(v)}$."], "using $1 - \\tan A\\tan B$ in the denominator.")


@reg(S, "basics")
def ti_sin3(r):
    s = F(r.randint(1, 4), r.randint(5, 6))
    v = 3 * s - 4 * s ** 3
    p = f"If $\\sin\\theta = {ft(s)}$, what is $\\sin 3\\theta$?"
    return Q(p, v, [3 * s, 4 * s ** 3 - 3 * s, 3 * s - s ** 3, s ** 3, 3 * s - 4 * s * s], "$\\sin 3\\theta = 3\\sin\\theta - 4\\sin^3\\theta$.",
             "$\\sin 3\\theta$.", "the triple-angle formula.",
             [f"$3 \\cdot {ft(s)} - 4 \\cdot {ft(s ** 3)} = {ft(v)}$."], "tripling $\\sin\\theta$.")


@reg(S, "basics")
def ti_sec_from_tan(r):
    a, b, c = r.choice(TRIPLES)
    t = F(a, b)
    v = F(c * c, b * b)
    p = f"If $\\tan\\theta = {ft(t)}$, what is $\\sec^2\\theta$?"
    return Q(p, v, [t * t, 1 - t * t, F(c, b), F(b * b, c * c), v + 1], "$1 + \\tan^2\\theta = \\sec^2\\theta$.",
             "$\\sec^2\\theta$.", "Pythagorean identity divided by $\\cos^2\\theta$.",
             [f"$1 + {ft(t * t)} = {ft(v)}$."], "forgetting to add 1.")


@reg(S, "basics")
def ti_sin_cos_sum_sq(r):
    k = F(r.randint(1, 5), r.randint(3, 6))
    if k * k > 2:
        return None
    v = (k * k - 1) / 2
    p = f"If $\\sin x + \\cos x = {ft(k)}$, what is $\\sin 2x$?"
    return Q(p, 2 * v, [v, k * k, 1 - k * k, k * k + 1, 2 * k], "Square both sides.",
             "$\\sin 2x$.", "$(\\sin x + \\cos x)^2 = 1 + 2\\sin x\\cos x = 1 + \\sin 2x$.",
             [f"${ft(k * k)} = 1 + \\sin 2x$.", f"$\\sin 2x = {ft(2 * v)}$."], "forgetting that $2\\sin x\\cos x$ is already $\\sin 2x$.") if k * k != 1 else None


@reg(S, "challenge")
def tic_tan_pairs(r):
    a = r.randint(1, 20)
    n = 46 - 2 * a
    ans = 2 ** (n // 2)
    p = f"What is $(1 + \\tan {a}^\\circ)(1 + \\tan {a + 1}^\\circ)\\cdots(1 + \\tan {45 - a}^\\circ)$?"
    return Q(p, ans, [2 ** n, 2 ** (n // 2 + 1), n, 2 ** (n // 2 - 1), 1], "Pair angles adding to $45^\\circ$.",
             "the product.", "if $x + y = 45^\\circ$ then $(1 + \\tan x)(1 + \\tan y) = 2$, since $\\tan x + \\tan y = 1 - \\tan x\\tan y$.",
             [f"There are ${n}$ factors, forming ${n // 2}$ pairs.", f"Product: $2^{{{n // 2}}} = {ans}$."], "pairing to $90^\\circ$ instead.")


@reg(S, "challenge")
def tic_fourth(r):
    m = F(r.randint(1, 5), r.randint(6, 9))
    v = 1 - m * m / 2
    p = f"If $\\sin 2x = {ft(m)}$, what is $\\sin^4 x + \\cos^4 x$?"
    return Q(p, v, [1 - m * m, 1 - m / 2, 1 - 2 * m * m, m * m / 2, 1 + m * m / 2], "$(\\sin^2 x + \\cos^2 x)^2 = 1$.",
             "the value.", "$\\sin^4 x + \\cos^4 x = 1 - 2\\sin^2 x\\cos^2 x = 1 - \\frac{1}{2}\\sin^2 2x$.",
             [f"$1 - \\frac{{1}}{{2}} \\cdot {ft(m * m)} = {ft(v)}$."], "using $1 - \\sin^2 2x$.")


@reg(S, "challenge")
def tic_cos3(r):
    c = F(r.randint(-4, 4), r.randint(5, 6))
    v = 4 * c ** 3 - 3 * c
    p = f"If $\\cos\\theta = {ft(c)}$, what is $\\cos 3\\theta$?"
    return Q(p, v, [3 * c, 3 * c - 4 * c ** 3 if 3 * c - 4 * c ** 3 != v else v + 1, c ** 3, 4 * c ** 3 + 3 * c, 4 * c * c - 3 * c], "$\\cos 3\\theta = 4\\cos^3\\theta - 3\\cos\\theta$.",
             "$\\cos 3\\theta$.", "the cosine triple-angle formula.",
             [f"$4 \\cdot {ft(c ** 3)} - 3 \\cdot {ft(c)} = {ft(v)}$."], "using the sine version's signs.") if c != 0 else None


@reg(S, "challenge")
def tic_triangle_tan(r):
    a, b = F(r.randint(1, 5), r.randint(1, 4)), F(r.randint(1, 5), r.randint(1, 4))
    if a * b == 1:
        return None
    v = -(a + b) / (1 - a * b)
    if v <= 0 and a * b < 1:
        pass
    p = f"In triangle $ABC$, $\\tan A = {ft(a)}$ and $\\tan B = {ft(b)}$. What is $\\tan C$?"
    return Q(p, v, [-v, (a + b) / (1 + a * b), a * b, a + b, 1 / v if v else 1], "$C = 180^\\circ - (A + B)$.",
             "$\\tan C$.", "$\\tan C = -\\tan(A + B)$.",
             [f"$\\tan(A + B) = \\frac{{{ft(a)} + {ft(b)}}}{{1 - {ft(a * b)}}} = {ft(-v)}$.", f"$\\tan C = {ft(v)}$."], "forgetting the minus sign.")


@reg(S, "challenge")
def tic_weierstrass(r):
    t = F(r.randint(1, 5), r.randint(2, 7))
    s, c = 2 * t / (1 + t * t), (1 - t * t) / (1 + t * t)
    f = r.choice(["sin", "cos"])
    v = s if f == "sin" else c
    p = f"If $\\tan\\frac{{x}}{{2}} = {ft(t)}$, what is $\\{f} x$?"
    return Q(p, v, [c if f == "sin" else s, 2 * t, 2 * t / (1 - t * t) if t != 1 else F(1, 2), -v, t * t], "Use the half-angle tangent substitution.",
             f"$\\{f} x$.", "with $t = \\tan\\frac{x}{2}$: $\\sin x = \\frac{2t}{1 + t^2}$, $\\cos x = \\frac{1 - t^2}{1 + t^2}$.",
             [f"Here $\\{f} x = {ft(v)}$."], "using $\\tan x$ in place of $\\tan\\frac{x}{2}$.") if v != 0 else None


@reg(S, "challenge")
def tic_cos_sq_sum(r):
    x = r.randint(1, 29)
    p = f"What is $\\cos^2 {x}^\\circ + \\cos^2 {60 - x}^\\circ + \\cos^2 {60 + x}^\\circ$?"
    return Q(p, F(3, 2), [1, 3, F(3, 4), 2, F(1, 2)], "Use $\\cos^2 t = \\frac{1 + \\cos 2t}{2}$.",
             "the sum.", f"the three cosines $\\cos {2 * x}^\\circ$, $\\cos {120 - 2 * x}^\\circ$, $\\cos {120 + 2 * x}^\\circ$ add to $0$.",
             ["Sum $= \\frac{3}{2} + \\frac{1}{2}(\\cos 2x + \\cos(120^\\circ - 2x) + \\cos(120^\\circ + 2x)) = \\frac{3}{2} + 0$."], "assuming each term is $\\frac{1}{2}$ only by coincidence.")


@reg(S, "challenge")
def tic_tan_triple(r):
    x, v = r.choice([(10, R3 / 3), (5, 2 - R3), (15, 1), (25, 2 + R3)])
    p = f"What is $\\tan {x}^\\circ \\tan {60 - x}^\\circ \\tan {60 + x}^\\circ$?"
    return Q(p, ex(v), exw(v, r), "$\\tan x \\tan(60^\\circ - x)\\tan(60^\\circ + x) = \\tan 3x$.",
             "the product.", "the tangent triple-angle product identity.",
             [f"$\\tan {3 * x}^\\circ = {ex(v).tex}$."], "multiplying the angles.")


# ================================================================ trig_laws
S = "trig_laws"


@reg(S, "basics")
def tl_cos120(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    c2 = a * a + b * b + a * b
    p = f"In triangle $ABC$, $a = {a}$, $b = {b}$, and $\\angle C = 120^\\circ$. What is $c$?"
    return Q(p, rad(1, c2), [rad(1, a * a + b * b - a * b), rad(1, a * a + b * b), num(a + b), rad(1, c2 + a * b), rad(1, c2 - 1)], "Law of Cosines with $\\cos 120^\\circ = -\\frac{1}{2}$.",
             "side $c$.", "$c^2 = a^2 + b^2 - 2ab\\cos C$.",
             [f"$c^2 = {a * a} + {b * b} + {a * b} = {c2}$.", f"$c = {rad(1, c2).tex}$."], "using $+\\frac{1}{2}$ for $\\cos 120^\\circ$.")


@reg(S, "basics")
def tl_area_angle(r):
    a, b = r.randint(2, 14), r.randint(2, 14)
    d = r.choice([30, 45, 60, 135, 120, 150])
    s = {30: (F(1, 2), 1), 150: (F(1, 2), 1), 45: (F(1, 2), 2), 135: (F(1, 2), 2), 60: (F(1, 2), 3), 120: (F(1, 2), 3)}[d]
    ans = rad(F(a * b, 2) * s[0], s[1])
    p = f"What is the area of a triangle with sides ${a}$ and ${b}$ and a ${d}^\\circ$ angle between them?"
    return Q(p, ans, [rad(F(a * b, 1) * s[0], s[1]), num(F(a * b, 2)), rad(F(a * b, 4), 3 if s[1] != 3 else 2), rad(F(a * b, 2) * s[0] + 1, s[1]), num(F(a * b, 4) + 1)], "Area $= \\frac{1}{2}ab\\sin C$.",
             "the area.", "two sides and the included angle.",
             [f"$\\sin {d}^\\circ = {ex(sind(d)).tex}$.", f"$\\frac{{1}}{{2}} \\cdot {a} \\cdot {b} \\cdot {ex(sind(d)).tex} = {ans.tex}$."], "forgetting the $\\frac{1}{2}$.")


@reg(S, "basics")
def tl_sines(r):
    A, B = r.choice([(30, 45), (45, 30), (30, 60), (60, 30), (45, 60), (60, 45), (30, 90), (30, 120), (45, 135)])
    if A + B >= 180:
        return None
    a = r.randint(2, 12)
    ratio = {(30, 45): (1, 2), (45, 30): (F(1, 2), 2), (30, 60): (1, 3), (60, 30): (F(1, 3), 3), (45, 60): (F(1, 2), 6), (60, 45): (F(1, 3), 6), (30, 90): (2, 1), (30, 120): (1, 3), (45, 135): (1, 1)}[(A, B)]
    ans = rad(a * F(ratio[0]), ratio[1])
    if abs(ans.key - a * sind(B) / sind(A)) > 1e-9:
        return None
    p = f"In triangle $ABC$, $\\angle A = {A}^\\circ$, $\\angle B = {B}^\\circ$, and $a = {a}$. What is $b$?"
    return Q(p, ans, [rad(a, 2) if ratio != (1, 2) else rad(a, 3), num(a), num(2 * a) if ans.key != 2 * a else rad(a, 3), rad(F(a, 2), 3) if abs(ans.key - a * R3 / 2) > 1e-9 else num(a + 1), rad(F(a, 2), 2) if abs(ans.key - a * R2 / 2) > 1e-9 else num(a + 2)], "Law of Sines.",
             "side $b$.", "$\\frac{a}{\\sin A} = \\frac{b}{\\sin B}$.",
             [f"$b = {a} \\cdot \\frac{{\\sin {B}^\\circ}}{{\\sin {A}^\\circ}} = {a} \\cdot \\frac{{{ex(sind(B)).tex}}}{{{ex(sind(A)).tex}}} = {ans.tex}$."], "flipping the ratio.")


@reg(S, "basics")
def tl_circumradius(r):
    d = r.choice([30, 45, 60, 90, 120, 135, 150])
    a = r.randint(2, 14)
    val = a / (2 * sind(d))
    ans = {30: num(a), 150: num(a), 90: num(F(a, 2)), 45: rad(F(a, 2), 2), 135: rad(F(a, 2), 2), 60: rad(F(a, 3), 3), 120: rad(F(a, 3), 3)}[d]
    p = f"In triangle $ABC$, $BC = {a}$ and $\\angle A = {d}^\\circ$. What is the circumradius?"
    return Q(p, ans, [num(2 * a), num(F(a, 2)) if d != 90 else num(a), rad(a, 2) if d not in (45, 135) else rad(a, 3), rad(a, 3) if d not in (60, 120) else rad(a, 2), num(a * 2 + 1)], "Extended Law of Sines.",
             "the circumradius $R$.", "$\\frac{a}{\\sin A} = 2R$.",
             [f"$2R = \\frac{{{a}}}{{{ex(sind(d)).tex}}}$.", f"$R = {ans.tex}$."], "forgetting to halve.") if abs(ans.key - val) < 1e-9 else None


@reg(S, "basics")
def tl_cos_value(r):
    while True:
        a, b, c = sorted(r.sample(range(3, 16), 3))
        if a + b > c:
            break
    v = F(a * a + b * b - c * c, 2 * a * b)
    p = f"A triangle has sides ${a}$, ${b}$, and ${c}$. What is the cosine of the angle opposite the side of length ${c}$?"
    return Q(p, v, [-v, F(a * a + b * b - c * c, a * b), F(c * c - a * a - b * b, 2 * a * b) - F(1, a * b) if -v + 0 != v else v + 1, F(a * a + c * c - b * b, 2 * a * c), F(c, a + b)], "Law of Cosines, solved for the cosine.",
             "the cosine.", "$\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}$.",
             [f"$\\frac{{{a * a} + {b * b} - {c * c}}}{{2 \\cdot {a} \\cdot {b}}} = {ft(v)}$."], "forgetting the factor of 2.") if v != 0 else None


@reg(S, "basics")
def tl_parallelogram(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    ask = r.choice(["long", "short"])
    d2 = a * a + b * b + (a * b if ask == "long" else -a * b)
    p = f"A parallelogram has sides ${a}$ and ${b}$ with a $60^\\circ$ angle between them. What is the length of its {'longer' if ask == 'long' else 'shorter'} diagonal?"
    return Q(p, rad(1, d2), [rad(1, a * a + b * b + (-a * b if ask == "long" else a * b)), rad(1, a * a + b * b), num(a + b), rad(1, d2 + 1), rad(1, d2 + 2 * a * b) if ask == "short" else rad(1, d2 - 1)], "The diagonals cut the parallelogram into triangles.",
             "the diagonal.", "the " + ("longer diagonal is opposite the $120^\\circ$ angle." if ask == "long" else "shorter diagonal is opposite the $60^\\circ$ angle."),
             [f"$d^2 = {a * a} + {b * b} - 2 \\cdot {a} \\cdot {b} \\cos {120 if ask == 'long' else 60}^\\circ = {d2}$.", f"$d = {rad(1, d2).tex}$."], "pairing the diagonal with the wrong angle.")


HERON = [(13, 14, 15, 84), (5, 5, 6, 12), (5, 5, 8, 12), (10, 13, 13, 60), (9, 10, 17, 36), (7, 15, 20, 42), (13, 13, 24, 60), (6, 25, 29, 60), (11, 13, 20, 66), (13, 20, 21, 126), (10, 17, 21, 84), (15, 26, 37, 156)]


@reg(S, "basics")
def tl_heron(r):
    a, b, c, K = r.choice(HERON)
    k = r.choice([1, 1, 2])
    a, b, c, K = a * k, b * k, c * k, K * k * k
    p = f"What is the area of a triangle with sides ${a}$, ${b}$, and ${c}$?"
    s = (a + b + c) // 2
    return Q(p, K, [K * 2, K // 2, s * s // 2, a * b // 2, K + s], "Heron's formula.",
             "the area.", "$K = \\sqrt{s(s - a)(s - b)(s - c)}$ with $s$ the semiperimeter.",
             [f"$s = {s}$.", f"$K = \\sqrt{{{s} \\cdot {s - a} \\cdot {s - b} \\cdot {s - c}}} = \\sqrt{{{K * K}}} = {K}$."], "using the full perimeter for $s$.")


@reg(S, "basics")
def tl_inradius(r):
    a, b, c, K = r.choice(HERON)
    s = F(a + b + c, 2)
    v = K / s
    p = f"What is the inradius of a triangle with sides ${a}$, ${b}$, and ${c}$?"
    return Q(p, v, [2 * v, v / 2, F(K, a + b + c + 1), F(a * b * c, 4 * K), v + 1], "$K = rs$.",
             "the inradius.", "area equals inradius times semiperimeter.",
             [f"Area (Heron): ${K}$. $s = {ft(s)}$.", f"$r = \\frac{{{K}}}{{{ft(s)}}} = {ft(v)}$."], "dividing by the full perimeter.")


@reg(S, "basics")
def tl_bisector(r):
    b, c = r.sample(range(3, 15), 2)
    a = r.randint(abs(b - c) + 1, b + c - 1)
    BD = F(a * c, b + c)
    p = f"In triangle $ABC$, $AB = {c}$, $AC = {b}$, and $BC = {a}$. The bisector of angle $A$ meets $BC$ at $D$. What is $BD$?"
    return Q(p, BD, [F(a * b, b + c), F(a, 2), BD + 1, F(c, 2), F(a * c, b)], "Angle Bisector Theorem.",
             "$BD$.", "$\\frac{BD}{DC} = \\frac{AB}{AC}$.",
             [f"$BD : DC = {c} : {b}$.", f"$BD = {a} \\cdot \\frac{{{c}}}{{{b + c}}} = {ft(BD)}$."], "matching $BD$ with $AC$.")


@reg(S, "basics")
def tl_ssa(r):
    A = r.choice([30, 45, 60])
    b = r.randint(4, 16)
    h = b * sind(A)
    kind = r.choice([0, 1, 2, 1])
    a = {0: max(1, math.floor(h - 0.5)), 1: b + r.randint(1, 4), 2: None}[kind]
    if kind == 2:
        cands = [x for x in range(1, b) if x > h + 1e-9]
        if not cands:
            return None
        a = r.choice(cands)
    if kind == 0 and a >= h:
        return None
    n = 0 if a < h - 1e-9 else 1 if abs(a - h) < 1e-9 or a >= b else 2
    p = f"How many non-congruent triangles have $\\angle A = {A}^\\circ$, $b = {b}$, and $a = {a}$?"
    return Q(p, n, [x for x in (0, 1, 2, 3) if x != n] + [C("\\text{infinitely many}", 9)], "Compare $a$ with the height $b\\sin A$ and with $b$.",
             "the number of triangles.", "the ambiguous case (SSA).",
             [f"Height: $b\\sin A = {b} \\cdot {ex(sind(A)).tex} \\approx {h:.2f}$.", "Compare with $a = " + str(a) + "$" + (": too short, no triangle." if n == 0 else ": at least $b$, so one triangle." if n == 1 else ": between the height and $b$, so two triangles.")],
             "assuming SSA always gives one triangle.")


@reg(S, "basics")
def tl_sin_from_area(r):
    a, b = r.randint(3, 15), r.randint(3, 15)
    s = F(r.randint(1, 9), 10)
    K = F(a * b, 2) * s
    p = f"A triangle has sides ${a}$ and ${b}$ and area ${ft(K)}$. What is the sine of the angle between those sides?"
    return Q(p, s, [2 * s if 2 * s < 1 else s / 2, K / (a * b), s + F(1, 10), 1 - s, F(K, a + b) if F(K, a + b) != s else s + F(1, 5)], "Area $= \\frac{1}{2}ab\\sin C$.",
             "$\\sin C$.", "solve the area formula for the sine.",
             [f"$\\sin C = \\frac{{2K}}{{ab}} = \\frac{{{ft(2 * K)}}}{{{a * b}}} = {ft(s)}$."], "forgetting the factor of 2.")


@reg(S, "basics")
def tl_cos_given(r):
    a, b = r.randint(2, 12), r.randint(2, 12)
    cv = F(r.randint(-6, 6), r.choice([4, 6, 8]))
    c2 = a * a + b * b - 2 * a * b * cv
    if c2.denominator != 1 or cv == 0 or abs(cv) >= 1:
        return None
    c2 = int(c2)
    p = f"In triangle $ABC$, $a = {a}$, $b = {b}$, and $\\cos C = {ft(cv)}$. What is $c$?"
    alt = a * a + b * b + 2 * a * b * cv
    return Q(p, rad(1, c2), [rad(1, int(alt)) if alt.denominator == 1 and alt > 0 and alt != c2 else rad(1, c2 + 3), rad(1, a * a + b * b), rad(1, c2 + 1), rad(1, c2 - 1), num(a + b)], "Law of Cosines.",
             "side $c$.", "$c^2 = a^2 + b^2 - 2ab\\cos C$.",
             [f"$c^2 = {a * a} + {b * b} - 2 \\cdot {a} \\cdot {b} \\cdot {ft(cv)} = {c2}$.", f"$c = {rad(1, c2).tex}$."], "dropping the minus sign.")


@reg(S, "basics")
def tl_sine_ratio(r):
    a, b = r.sample(range(2, 15), 2)
    sA = F(r.randint(1, 5), 10)
    sB = sA * b / a
    if sB >= 1:
        return None
    p = f"In triangle $ABC$, $a = {a}$, $b = {b}$, and $\\sin A = {ft(sA)}$. What is $\\sin B$?"
    return Q(p, sB, [sA * a / b, sA, sB / 2, 1 - sB, sB + F(1, 10)], "Law of Sines.",
             "$\\sin B$.", "$\\frac{\\sin A}{a} = \\frac{\\sin B}{b}$.",
             [f"$\\sin B = {ft(sA)} \\cdot \\frac{{{b}}}{{{a}}} = {ft(sB)}$."], "flipping the ratio.")


@reg(S, "basics")
def tl_polygon_side(r):
    n = r.choice([3, 4, 6])
    R_ = r.randint(2, 12)
    ans = {3: rad(R_, 3), 4: rad(R_, 2), 6: num(R_)}[n]
    p = f"A regular ${'triangle' if n == 3 else 'square' if n == 4 else 'hexagon'}$ is inscribed in a circle of radius ${R_}$. What is its side length?".replace("$triangle$", "triangle").replace("$square$", "square").replace("$hexagon$", "hexagon")
    return Q(p, ans, [rad(R_, 2) if n != 4 else rad(R_, 3), num(2 * R_), num(R_) if n != 6 else rad(R_, 3), rad(F(R_, 2), 3), rad(R_, 5)], "Each side subtends a central angle of $\\frac{360^\\circ}{n}$.",
             "the side.", f"Law of Cosines on the triangle from the center: side $= 2R\\sin\\frac{{180^\\circ}}{{{n}}}$.",
             [f"$2 \\cdot {R_} \\sin {180 // n}^\\circ = {ans.tex}$."], "using the radius as the side.")


@reg(S, "basics")
def tl_elevation(r):
    d = r.randint(5, 60)
    ang = r.choice([30, 45, 60])
    ans = {30: rad(F(d, 3), 3), 45: num(d), 60: rad(d, 3)}[ang]
    p = f"From a point ${d}$ m from the base of a tower on level ground, the angle of elevation to the top is ${ang}^\\circ$. How tall is the tower, in meters?"
    return Q(p, ans, [rad(d, 3) if ang != 60 else rad(F(d, 3), 3), num(d) if ang != 45 else rad(d, 2), num(2 * d), rad(F(d, 2), 3), num(F(d, 2))], "Height $= d\\tan\\theta$.",
             "the height.", "right triangle: opposite over adjacent is the tangent.",
             [f"${d} \\tan {ang}^\\circ = {ans.tex}$."], "using sine instead of tangent.")


@reg(S, "basics")
def tl_isosceles_base(r):
    L = r.randint(2, 15)
    d = r.choice([90, 120, 60])
    ans = {90: rad(L, 2), 120: rad(L, 3), 60: num(L)}[d]
    p = f"An isosceles triangle has two sides of length ${L}$ meeting at a ${d}^\\circ$ angle. What is the length of the third side?"
    return Q(p, ans, [rad(L, 2) if d != 90 else rad(L, 3), num(2 * L), num(L) if d != 60 else rad(L, 2), rad(F(L, 2), 3), rad(L, 5)], "Law of Cosines.",
             "the third side.", f"$c^2 = 2 \\cdot {L}^2 - 2 \\cdot {L}^2 \\cos {d}^\\circ$.",
             [f"$c^2 = {2 * L * L} - {2 * L * L} \\cdot {ex(cosd(d)).tex} = {round(2 * L * L * (1 - cosd(d)))}$.", f"$c = {ans.tex}$."], "using the wrong sign of the cosine.")


@reg(S, "challenge")
def tlc_stewart(r):
    a, b, c = r.randint(5, 15), r.randint(5, 15), r.randint(5, 15)
    if not (a < b + c and b < a + c and c < a + b):
        return None
    m, n = r.randint(1, a - 1), None
    n = a - m
    d2 = F(b * b * m + c * c * n, a) - m * n
    if d2.denominator != 1 or d2 <= 0:
        return None
    d2 = int(d2)
    p = f"In triangle $ABC$, $AB = {c}$, $AC = {b}$, and $BC = {a}$. Point $D$ is on $BC$ with $BD = {m}$. What is $AD$?"
    return Q(p, rad(1, d2), [rad(1, d2 + m * n) if d2 + m * n != d2 else rad(1, d2 + 1), rad(1, d2 + 1), rad(1, abs(d2 - 2)) if d2 > 2 else rad(1, d2 + 3), num(F(b + c, 2)), rad(1, d2 + 5)], "Stewart's Theorem.",
             "$AD$.", "$b^2 m + c^2 n = a(d^2 + mn)$, where $m = BD$, $n = DC$.",
             [f"$m = {m}$, $n = {n}$.", f"${b * b} \\cdot {m} + {c * c} \\cdot {n} = {a}(d^2 + {m * n})$.", f"$d^2 = {d2}$, $d = {rad(1, d2).tex}$."], "pairing $b^2$ with $n$ instead of $m$.")


@reg(S, "challenge")
def tlc_circumradius_heron(r):
    a, b, c, K = r.choice(HERON)
    v = F(a * b * c, 4 * K)
    p = f"What is the circumradius of a triangle with sides ${a}$, ${b}$, and ${c}$?"
    return Q(p, v, [F(a * b * c, 2 * K), F(K * 2, a + b + c), v + 1, F(max(a, b, c), 2), v * 2], "$R = \\frac{abc}{4K}$.",
             "the circumradius.", "find the area by Heron's formula, then use $R = \\frac{abc}{4K}$.",
             [f"Area: ${K}$.", f"$R = \\frac{{{a} \\cdot {b} \\cdot {c}}}{{4 \\cdot {K}}} = {ft(v)}$."], "using $\\frac{abc}{2K}$.")


@reg(S, "challenge")
def tlc_ratio_angle(r):
    tri = list(r.choice([(3, 5, 7), (5, 7, 8), (3, 7, 8), (7, 8, 13), (5, 3, 7), (8, 5, 7), (3, 4, 5), (5, 12, 13), (7, 15, 13), (1, 1, 1)]))
    r.shuffle(tri)
    a, b, c = tri
    good = []
    for i in range(3):
        z = tri[i]
        x, y = [tri[j] for j in range(3) if j != i]
        cv = F(x * x + y * y - z * z, 2 * x * y)
        ang = math.degrees(math.acos(float(cv)))
        if abs(ang - round(ang)) < 1e-9:
            good.append((z, x, y, cv, round(ang)))
    if not good:
        return None
    z, x, y, cv, ang = r.choice(good)
    letter = "ABC"[tri.index(z)]
    p = f"In triangle $ABC$, $\\sin A : \\sin B : \\sin C = {a} : {b} : {c}$. What is angle ${letter}$, in degrees?"
    return Q(p, DG(ang), [DG(180 - ang) if ang != 90 else DG(45), DG(150) if ang != 150 else DG(100), DG(30) if ang != 30 else DG(40), DG(135), DG(75)], "The sines are proportional to the sides.",
             "the angle.", f"by the Law of Sines, the sides are in ratio ${a} : {b} : {c}$; take sides ${a}k$, ${b}k$, ${c}k$.",
             [f"$\\cos {letter} = \\frac{{{x}^2 + {y}^2 - {z}^2}}{{2 \\cdot {x} \\cdot {y}}} = {ft(cv)}$.", f"So ${letter} = {ang}^\\circ$."], "treating the ratio as angle measures.")


@reg(S, "challenge")
def tlc_brahmagupta(r):
    for _ in range(50):
        a, b, c, d = [r.randint(2, 12) for _ in range(4)]
        s = F(a + b + c + d, 2)
        k2 = (s - a) * (s - b) * (s - c) * (s - d)
        if max(a, b, c, d) * 2 < a + b + c + d and k2.denominator == 1 and math.isqrt(int(k2)) ** 2 == int(k2) and k2 > 0:
            break
    else:
        return None
    K = math.isqrt(int(k2))
    p = f"A quadrilateral inscribed in a circle has sides ${a}$, ${b}$, ${c}$, and ${d}$. What is its area?"
    return Q(p, K, [K + 2, K * 2, a * b + c * d, int(s) * 2 if int(s) * 2 != K else K + 4, K - 1], "Brahmagupta's formula.",
             "the area.", "$K = \\sqrt{(s - a)(s - b)(s - c)(s - d)}$ for a cyclic quadrilateral.",
             [f"$s = {ft(s)}$.", f"$K = \\sqrt{{{ft(s - a)} \\cdot {ft(s - b)} \\cdot {ft(s - c)} \\cdot {ft(s - d)}}} = {K}$."], "using Heron's formula with an extra factor of $s$.")


@reg(S, "challenge")
def tlc_bisector_length(r):
    b, c = r.randint(3, 12), r.randint(3, 12)
    a = r.randint(abs(b - c) + 1, b + c - 1)
    t2 = F(b * c * ((b + c) ** 2 - a * a), (b + c) ** 2)
    if t2.denominator != 1:
        return None
    t2 = int(t2)
    p = f"In triangle $ABC$, $AB = {c}$, $AC = {b}$, $BC = {a}$. What is the length of the bisector of angle $A$ (from $A$ to $BC$)?"
    return Q(p, rad(1, t2), [rad(1, t2 + 1), rad(1, b * c), rad(1, max(t2 - 2, 1)) if t2 > 3 else rad(1, t2 + 2), num(F(b + c, 2)), rad(1, t2 + 3)], "Use the bisector length formula or Stewart's Theorem.",
             "the bisector length.", "$t_a^2 = bc\\left(1 - \\frac{a^2}{(b + c)^2}\\right)$.",
             [f"$t_a^2 = {b * c}\\left(1 - \\frac{{{a * a}}}{{{(b + c) ** 2}}}\\right) = {t2}$.", f"$t_a = {rad(1, t2).tex}$."], "using the median formula.")


@reg(S, "challenge")
def tlc_ships(r):
    v1, v2 = r.randint(2, 15), r.randint(2, 15)
    t = r.randint(1, 4)
    d = r.choice([60, 120])
    a, b = v1 * t, v2 * t
    d2 = a * a + b * b - (a * b if d == 60 else -a * b)
    p = f"Two ships leave port at the same time, one at ${v1}$ km/h and one at ${v2}$ km/h, on straight courses ${d}^\\circ$ apart. How far apart are they after ${t}$ hour{'s' if t > 1 else ''}, in km?"
    return Q(p, rad(1, d2), [rad(1, a * a + b * b + (a * b if d == 60 else -a * b)), rad(1, a * a + b * b), num(a + b), rad(1, d2 + 1), num(abs(a - b) + 1)], "Law of Cosines.",
             "the distance.", "the port and the two ships form a triangle with the given angle at the port.",
             [f"Distances: ${a}$ and ${b}$.", f"$d^2 = {a * a} + {b * b} - 2 \\cdot {a} \\cdot {b} \\cos {d}^\\circ = {d2}$.", f"$d = {rad(1, d2).tex}$."], "using the wrong sign for the cosine.")


@reg(S, "challenge")
def tlc_tan_angle(r):
    a, b, c, K = r.choice(HERON)
    x, y, z = r.sample([a, b, c], 3)
    den = x * x + y * y - z * z
    if den == 0:
        return None
    v = F(4 * K, den)
    p = f"A triangle has sides ${x}$, ${y}$, and ${z}$. What is the tangent of the angle opposite the side of length ${z}$?"
    return Q(p, v, [F(2 * K, den), -v, F(2 * K, x * y), F(den, 2 * x * y), v + 1], "Find the sine (from the area) and the cosine (from the Law of Cosines).",
             "$\\tan C$.", "$\\sin C = \\frac{2K}{xy}$ and $\\cos C = \\frac{x^2 + y^2 - z^2}{2xy}$, so $\\tan C = \\frac{4K}{x^2 + y^2 - z^2}$.",
             [f"Area: ${K}$.", f"$\\tan C = \\frac{{4 \\cdot {K}}}{{{den}}} = {ft(v)}$."], "dropping the factor of 2 in the sine.")


# ================================================================ trig_equations
S = "trig_equations"


@reg(S, "basics")
def te_period_tan(r):
    f = r.choice(["tan", "sin", "cos"])
    k = F(r.randint(1, 6), r.choice([1, 1, 2, 3]))
    base = F(1) if f == "tan" else F(2)
    ans = base / k
    arg = f"{ft(k) if k != 1 else ''}x" if k.denominator == 1 else f"\\frac{{{k.numerator if k.numerator != 1 else ''}x}}{{{k.denominator}}}"
    p = f"What is the period of $y = \\{f}\\left({arg}\\right)$?"
    return Q(p, PI(ans), [PI(ans * 2) if f == "tan" else PI(ans / 2), PI(base * k), PI(base), PI(ans + 1), PI(ans * 4)], f"The period of $\\{f} x$ is ${'\\pi' if f == 'tan' else '2\\pi'}$.",
             "the period.", f"$\\{f}(kx)$ has period $\\frac{{{'\\pi' if f == 'tan' else '2\\pi'}}}{{k}}$.",
             [f"$\\frac{{{deg_rad(base * 180)}}}{{{ft(k)}}} = {deg_rad(ans * 180)}$."], "using $2\\pi$ for tangent." if f == "tan" else "multiplying by $k$.")


@reg(S, "basics")
def te_max(r):
    a = r.randint(2, 9) * r.choice([1, -1])
    b = r.randint(1, 5)
    c = r.randint(-6, 6)
    ask = r.choice(["max", "min"])
    v = abs(a) + c if ask == "max" else -abs(a) + c
    p = f"What is the {'maximum' if ask == 'max' else 'minimum'} value of $y = {a}\\sin({b}x) {'+' if c >= 0 else '-'} {abs(c)}$?"
    return Q(p, v, [a + c if a + c != v else v + 1, -v, abs(a), v + b, c], "Sine ranges from $-1$ to $1$.",
             "the extreme value.", "the inner coefficient doesn't change the range; the amplitude is $|" + str(a) + "|$.",
             [f"$y$ ranges from ${-abs(a) + c}$ to ${abs(a) + c}$."], "letting the negative coefficient flip the maximum into the minimum the wrong way.")


@reg(S, "basics")
def te_count_cos(r):
    k = r.randint(1, 6)
    val, per = r.choice([("\\frac{1}{2}", 2), ("-\\frac{\\sqrt{2}}{2}", 2), ("1", 1), ("0", 2), ("-1", 1)])
    f = r.choice(["sin", "cos"])
    if f == "sin" and val in ("1", "-1"):
        per = 1
    ans = per * k
    p = f"How many solutions does $\\{f}({k if k > 1 else ''}x) = {val}$ have with $0 \\le x < 2\\pi$?"
    return Q(p, ans, [per, ans + 1, ans * 2, max(ans - 1, 0) if ans - 1 != per else ans + 2, k], f"$\\{f} t = {val}$ has {per} solution{'s' if per > 1 else ''} per period.",
             "the count.", f"as $x$ runs over $[0, 2\\pi)$, ${k}x$ runs over ${k}$ full periods.",
             [f"{per} per period times ${k}$ periods: ${ans}$."], "counting only one period.")


@reg(S, "basics")
def te_deg_sum(r):
    f, v = r.choice([("sin", .5), ("sin", -.5), ("cos", .5), ("cos", -R3 / 2), ("sin", R2 / 2), ("cos", -R2 / 2), ("tan", 1), ("tan", -R3)])
    sols = [d for d in range(360) if abs({"sin": sind, "cos": cosd}.get(f, lambda d: sind(d) / cosd(d) if abs(cosd(d)) > 1e-9 else 1e9)(d) - v) < 1e-9]
    p = f"What is the sum, in degrees, of all solutions of $\\{f} x = {ex(v).tex}$ with $0^\\circ \\le x < 360^\\circ$?"
    s = sum(sols)
    return Q(p, s, [sols[0], s + 180, s - 180 if s > 180 else s + 360, 360, sols[-1]], "Find the two solutions using the reference angle.",
             "the sum.", "each value is hit twice per full turn.",
             ["Solutions: " + ", ".join(f"${d}^\\circ$" for d in sols) + ".", f"Sum: ${s}^\\circ$."], "missing the second solution.")


@reg(S, "basics")
def te_tan_count(r):
    n = r.randint(1, 6)
    val = r.choice(["\\sqrt{3}", "1", "-1", "0", "2"])
    ans = n
    p = f"How many solutions does $\\tan x = {val}$ have with $0 \\le x < {n if n > 1 else ''}\\pi$?"
    return Q(p, ans, [2 * n, n + 1, max(n - 1, 0) if n > 1 else 3, n * 4, n + 2], "Tangent has period $\\pi$.",
             "the count.", "$\\tan x = c$ has exactly one solution in each interval of length $\\pi$.",
             [f"${n}$ periods, one solution each: ${n}$."], "using period $2\\pi$.")


@reg(S, "basics")
def te_smallest(r):
    k = r.randint(2, 9)
    f, base = r.choice([("sin", 90), ("cos", 180), ("sin", 270), ("cos", 360)])
    val = {("sin", 90): "1", ("cos", 180): "-1", ("sin", 270): "-1", ("cos", 360): "1"}[(f, base)]
    ans = F(base, k)
    if base == 360:
        p = f"What is the smallest positive $x$, in degrees, with $\\{f}({k}x) = 1$?"
    else:
        p = f"What is the smallest positive $x$, in degrees, with $\\{f}({k}x) = {val}$?"
    return Q(p, ans, [F(base * k, 1), F(base, 2 * k), ans + F(360, k), F(90, k) if base != 90 else F(180, k), F(base, k + 1)], "Find the smallest positive value of the inner angle first.",
             "the smallest $x$.", f"the smallest positive $t$ with $\\{f} t = {val}$ is ${base}^\\circ$.",
             [f"${k}x = {base}^\\circ$, so $x = {ft(ans)}^\\circ$."], "forgetting to divide by $" + str(k) + "$.")


@reg(S, "basics")
def te_factor(r):
    e, cnt = r.choice([("\\sin x \\cos x = 0", 4), ("\\sin x(2\\cos x - 1) = 0", 4), ("\\cos x(2\\sin x + 1) = 0", 4), ("\\sin^2 x = \\sin x", 3), ("\\cos^2 x = \\cos x", 3),
                       ("\\tan x(\\tan x - 1) = 0", 4), ("(2\\sin x - 1)(\\sin x + 1) = 0", 3), ("\\sin 2x = \\cos x", 4)])
    p = f"How many solutions does ${e}$ have with $0 \\le x < 2\\pi$?"
    return Q(p, cnt, [x for x in (1, 2, 3, 4, 5, 6) if x != cnt][:5], "Set each factor equal to zero.",
             "the count.", "solve each factor separately; watch for shared solutions.",
             [f"Listing the solutions of each factor and removing repeats: ${cnt}$."], "dividing by a factor that can be zero.")


@reg(S, "basics")
def te_sin_cos_equal(r):
    n = r.randint(1, 5)
    p = f"How many solutions does $\\sin x = \\cos x$ have with $0 \\le x < {2 * n}\\pi$?"
    return Q(p, 2 * n, [n, 4 * n, 2 * n + 1, 2 * n - 1, 2 * n + 2], "Divide by $\\cos x$.",
             "the count.", "$\\tan x = 1$: one solution every $\\pi$.",
             [f"Interval length ${2 * n}\\pi$, so ${2 * n}$ solutions."], "counting one per $2\\pi$.")


@reg(S, "basics")
def te_cos2_eq(r):
    kind = r.choice(["count", "sum"])
    sols = [0, 120, 240]
    p = f"{'How many solutions does' if kind == 'count' else 'What is the sum, in degrees, of all solutions of'} $\\cos 2x = \\cos x$ {'have ' if kind == 'count' else ''}with $0^\\circ \\le x < 360^\\circ$?"
    ans = 3 if kind == "count" else 360
    return Q(p, ans, [2, 4, 1, 6, 5] if kind == "count" else [240, 120, 480, 180, 300], "Use $\\cos 2x = 2\\cos^2 x - 1$.",
             "the " + ("count." if kind == "count" else "sum."), "$2\\cos^2 x - \\cos x - 1 = 0$ factors as $(2\\cos x + 1)(\\cos x - 1) = 0$.",
             ["$\\cos x = 1$: $x = 0^\\circ$. $\\cos x = -\\frac{1}{2}$: $x = 120^\\circ, 240^\\circ$.", f"Answer: ${ans}$."], "missing $x = 0$.")


@reg(S, "basics")
def te_abs_count(r):
    f = r.choice(["sin", "cos"])
    v = r.choice(["\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}", "\\frac{\\sqrt{2}}{2}", "1", "0"])
    cnt = 2 if v in ("1", "0") else 4
    k = r.randint(1, 3)
    p = f"How many solutions does $|\\{f} x| = {v}$ have with $0 \\le x < {2 * k}\\pi$?"
    return Q(p, cnt * k, [cnt * k // 2, cnt * k + 2, cnt * k * 2, cnt * k - 1, k], "$|\\{f} x| = c$ means $\\{f} x = c$ or $-c$.".replace("\\{f}", "\\" + f),
             "the count.", "solve both signs; each has two solutions per $2\\pi$ (one if $c = 1$, and $0$ is a single equation).",
             [f"Per $2\\pi$: ${cnt}$ solutions; times ${k}$: ${cnt * k}$."], "forgetting the negative case.")


@reg(S, "basics")
def te_quad_sin(r):
    e, fac, sols = r.choice([("2\\sin^2 x - \\sin x - 1 = 0", "(2\\sin x + 1)(\\sin x - 1)", [90, 210, 330]), ("2\\sin^2 x + \\sin x - 1 = 0", "(2\\sin x - 1)(\\sin x + 1)", [30, 150, 270]),
                             ("2\\sin^2 x - 3\\sin x + 1 = 0", "(2\\sin x - 1)(\\sin x - 1)", [30, 90, 150]), ("2\\sin^2 x + 3\\sin x + 1 = 0", "(2\\sin x + 1)(\\sin x + 1)", [210, 270, 330]),
                             ("2\\sin^2 x + 5\\sin x - 3 = 0", "(2\\sin x - 1)(\\sin x + 3)", [30, 150])])
    s_ = sum(sols)
    p = f"What is the sum, in degrees, of all solutions of ${e}$ with $0^\\circ \\le x < 360^\\circ$?"
    return Q(p, s_, [s_ - sols[0], s_ + 180, s_ + 90, sols[-1], 360 if s_ != 360 else 540], "Factor as a quadratic in $\\sin x$.",
             "the sum.", f"${e[:-4]} = {fac}$.",
             ["Solutions: " + ", ".join(f"${d}^\\circ$" for d in sols) + ".", f"Sum: ${s_}^\\circ$."], "keeping only one root of the quadratic, or an impossible one.")


@reg(S, "basics")
def te_phase(r):
    c = r.choice([15, 20, 30, 40, 45, 60, 75])
    f = r.choice(["sin", "cos"])
    first = (90 + c) if f == "sin" else c
    p = f"What is the smallest positive $x$, in degrees, where $y = \\{f}(x - {c}^\\circ)$ reaches its maximum?"
    return Q(p, first, [abs(90 - c) if abs(90 - c) != first else first + 10, 90, first + 360 if first + 360 != first else 5, first + 180, c + 180 if c + 180 != first else 2 * c], "Shift the usual maximum.",
             "the location of the first maximum.", f"$\\{f} t$ first peaks at $t = {90 if f == 'sin' else 0}^\\circ$ (or $360^\\circ$); set $x - {c} = $ that.",
             [f"$x = {first}^\\circ$."], "shifting in the wrong direction.")


@reg(S, "basics")
def te_inverse_comp(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    f, g, v = r.choice([("sin", "arccos", F(b, c)), ("cos", "arcsin", F(b, c)), ("tan", "arccos", F(b, a)), ("tan", "arcsin", F(a, b))])
    inner = F(a, c)
    p = f"What is $\\{f}\\left(\\{g} {ft(inner)}\\right)$?"
    return Q(p, v, [inner, 1 / v, 1 - inner, -v, F(a, b) if F(a, b) != v else F(b, a)], "Draw the right triangle.",
             "the value.", f"let $\\theta = \\{g} {ft(inner)}$; build a ${a}$-${b}$-${c}$ right triangle.",
             [f"Then $\\{f}\\theta = {ft(v)}$."], "assuming the functions cancel.")


@reg(S, "basics")
def te_tan_cot(r):
    k = r.randint(1, 3)
    p = f"How many solutions does $\\tan x = \\cot x$ have with $0 \\le x < {2 * k}\\pi$?"
    return Q(p, 4 * k, [2 * k, 4 * k + 2, k, 8 * k, 4 * k - 1], "$\\tan^2 x = 1$.",
             "the count.", "$\\tan x = \\pm 1$: two solutions per $\\pi$.",
             [f"${2 * k}$ intervals of length $\\pi$, two each: ${4 * k}$."], "solving only $\\tan x = 1$.")


@reg(S, "basics")
def te_period_sum(r):
    a, b = r.sample(range(1, 7), 2)
    L = F(2, math.gcd(a, b))
    p = f"What is the period of $y = \\sin({a if a > 1 else ''}x) + \\cos({b if b > 1 else ''}x)$?"
    return Q(p, PI(L), [PI(F(2, a * b)), PI(F(2, max(a, b))), PI(F(2, min(a, b))) if F(2, min(a, b)) != L else PI(L * 2), PI(L / 2), PI(F(2 * a * b, 1)) if F(2 * a * b, 1) != L else PI(L + 1)], "Find the least common multiple of the two periods.",
             "the period.", f"periods $\\frac{{2\\pi}}{{{a}}}$ and $\\frac{{2\\pi}}{{{b}}}$; the sum repeats at their least common multiple.",
             [f"$\\text{{lcm}} = \\frac{{2\\pi}}{{\\gcd({a}, {b})}} = {deg_rad(L * 180)}$."], "taking the smaller period.")


@reg(S, "basics")
def te_sec(r):
    f, v, sols = r.choice([("sec", "2", [60, 300]), ("csc", "2", [30, 150]), ("sec", "-2", [120, 240]), ("csc", "-2", [210, 330]), ("sec", "\\sqrt{2}", [45, 315]), ("cot", "1", [45, 225])])
    s = sum(sols)
    p = f"What is the sum, in degrees, of all solutions of $\\{f} x = {v}$ with $0^\\circ \\le x < 360^\\circ$?"
    return Q(p, s, [sols[0], s + 180, abs(s - 180) if abs(s - 180) != s else s + 90, 2 * sols[0] + 180 if 2 * sols[0] + 180 != s else s + 60, 180 if s != 180 else 270], "Take reciprocals.",
             "the sum.", "rewrite in terms of $\\sin$, $\\cos$, or $\\tan$.",
             ["Solutions: " + ", ".join(f"${d}^\\circ$" for d in sols) + ".", f"Sum: ${s}^\\circ$."], "solving $\\cos x = " + v + "$ directly.")


@reg(S, "challenge")
def tec_sin_plus_cos(r):
    v = r.choice([1, -1, 0])
    sols = [d for d in range(0, 360, 15) if abs(sind(d) + cosd(d) - v) < 1e-9]
    s = sum(sols)
    p = f"What is the sum, in degrees, of all solutions of $\\sin x + \\cos x = {v}$ with $0^\\circ \\le x < 360^\\circ$?"
    return Q(p, s, [sols[0], s + 90, s + 180, abs(s - 90), 360 if s != 360 else 450], "Write $\\sin x + \\cos x = \\sqrt{2}\\sin(x + 45^\\circ)$.",
             "the sum.", "solve $\\sin(x + 45^\\circ) = \\frac{" + str(v) + "}{\\sqrt{2}}$.",
             ["Solutions: " + ", ".join(f"${d}^\\circ$" for d in sols) + ".", f"Sum: ${s}^\\circ$."], "squaring both sides and keeping extraneous roots.")


@reg(S, "challenge")
def tec_max_mixed(r):
    a = r.randint(-5, 5)
    if abs(a) <= 2:
        v = 1 + F(a * a, 4)
    else:
        v = F(abs(a))
    p = f"What is the maximum value of $\\sin^2 x {'+' if a >= 0 else '-'} {abs(a)}\\cos x$?"
    return Q(p, v, [1 + abs(a), F(abs(a)) if v != abs(a) else v + 1, 1 + F(a * a, 2), F(a * a, 4), v + F(1, 4)], "Write $\\sin^2 x = 1 - \\cos^2 x$ and set $c = \\cos x \\in [-1, 1]$.",
             "the maximum.", f"maximize $1 - c^2 {'+' if a >= 0 else '-'} {abs(a)}c$ over $-1 \\le c \\le 1$.",
             [f"The vertex is at $c = {ft(F(a, 2))}$" + (" (inside the interval)." if abs(a) <= 2 else f", outside the interval, so use $c = {1 if a > 0 else -1}$."), f"Maximum: ${ft(v)}$."], "ignoring that $\\cos x$ is limited to $[-1, 1]$.") if a != 0 else None


@reg(S, "challenge")
def tec_tan_kx(r):
    k = r.randint(2, 5)
    sols = [F(45 + 180 * j, k) for j in range(k)]
    s = sum(sols)
    p = f"What is the sum, in degrees, of all solutions of $\\tan({k}x) = 1$ with $0^\\circ \\le x < 180^\\circ$?"
    return Q(p, s, [sols[0], s + 45, s * 2, F(45 * k, 1), s - sols[0]], "Find all $x$ with $" + str(k) + "x = 45^\\circ + 180^\\circ n$.",
             "the sum.", f"$x = \\frac{{45^\\circ + 180^\\circ n}}{{{k}}}$ for $n = 0, \\ldots, {k - 1}$.",
             ["Solutions: " + ", ".join(f"${ft(x)}^\\circ$" for x in sols) + ".", f"Sum: ${ft(s)}^\\circ$."], "keeping only $n = 0$.")


@reg(S, "challenge")
def tec_cos_kx_count(r):
    k = r.randint(2, 6)
    v, t0 = r.choice([("\\frac{1}{2}", 60), ("-\\frac{\\sqrt{3}}{2}", 150), ("1", 0), ("-1", 180), ("0", 90)])
    m = r.randint(1, 3)
    top = 180 * k * m
    ts = {t0 % 360, (-t0) % 360}
    cnt = sum(1 for n_ in range(k * m + 2) for t in ts if t + 360 * n_ < top)
    p = f"How many solutions does $\\cos({k}x) = {v}$ have with $0 \\le x < {m if m > 1 else ''}\\pi$?"
    return Q(p, cnt, [cnt + 1, max(cnt - 1, 1), cnt * 2, len(ts) * k * m + 3, cnt + 2], f"Let $t = {k}x$; then $0 \\le t < {k * m}\\pi$.",
             "the count.", f"count solutions of $\\cos t = {v}$ for $0 \\le t < {k * m}\\pi$.",
             [f"$\\cos t = {v}$ at $t = " + ", ".join(f"{d}^\\circ" for d in sorted(ts)) + "$ plus multiples of $360^\\circ$.", f"Those below ${top}^\\circ$: ${cnt}$."], "counting over $2\\pi$ in $x$ instead.")


@reg(S, "challenge")
def tec_sin_kx_sin_x(r):
    k = r.randint(2, 5)
    sols = set()
    for n_ in range(-20, 21):
        for x in (F(2 * n_, k - 1), F(2 * n_ + 1, k + 1)):
            if 0 <= x < 2:
                sols.add(x)
    cnt = len(sols)
    p = f"How many solutions does $\\sin({k}x) = \\sin x$ have with $0 \\le x < 2\\pi$?"
    return Q(p, cnt, [cnt + 1, cnt - 1, 2 * k, cnt + 2, 2 * k + 2 if 2 * k + 2 != cnt else cnt - 2], "$\\sin A = \\sin B$ when $A = B + 2\\pi n$ or $A = \\pi - B + 2\\pi n$.",
             "the count.", f"${k}x = x + 2\\pi n$ gives $x = \\frac{{2\\pi n}}{{{k - 1}}}$; ${k}x = \\pi - x + 2\\pi n$ gives $x = \\frac{{(2n + 1)\\pi}}{{{k + 1}}}$.",
             [f"First family: ${k - 1}$ values; second: ${k + 1}$ values.", f"Removing overlaps: ${cnt}$."], "forgetting the second family.")


@reg(S, "challenge")
def tec_measure(r):
    f = r.choice(["sin", "cos"])
    v, ang = r.choice([("\\frac{1}{2}", 60), ("\\frac{\\sqrt{2}}{2}", 45), ("\\frac{\\sqrt{3}}{2}", 30), ("0", 90), ("-\\frac{1}{2}", 120)])
    meas = F(2 * (180 - ang) if f == "sin" else 2 * ang, 180) if v != "0" else F(1)
    if f == "sin":
        meas = {60: F(2, 3), 45: F(1, 2), 30: F(1, 3), 90: F(1), 120: F(4, 3)}[ang]
    else:
        meas = {60: F(2, 3), 45: F(1, 2), 30: F(1, 3), 90: F(1), 120: F(4, 3)}[ang]
    p = f"What is the total length of the set of $x$ in $[0, 2\\pi)$ where $\\{f} x > {v}$?"
    return Q(p, PI(meas), [PI(2 - meas), PI(meas / 2), PI(meas + F(1, 3)), PI(F(1)) if meas != 1 else PI(F(3, 2)), PI(meas * 2) if meas * 2 != 2 - meas else PI(F(5, 3))], "Find where equality holds, then pick the right arcs.",
             "the length.", f"on the unit circle, $\\{f} x > {v}$ is one arc.",
             [f"The arc has length ${deg_rad(meas * 180)}$."], "taking the complementary arc.")


@reg(S, "challenge")
def tec_double_quad(r):
    e, roots, sols = r.choice([("\\cos 2x + 3\\sin x = 2", "\\sin x = 1 \\text{ or } \\frac{1}{2}", [30, 90, 150]),
                               ("\\cos 2x - 3\\sin x = 2", "\\sin x = -1 \\text{ or } -\\frac{1}{2}", [210, 270, 330]),
                               ("\\cos 2x + \\cos x = 0", "\\cos x = -1 \\text{ or } \\frac{1}{2}", [60, 180, 300]),
                               ("\\cos 2x = \\sin x", "\\sin x = -1 \\text{ or } \\frac{1}{2}", [30, 150, 270]),
                               ("\\cos 2x + 5\\cos x + 3 = 0", "\\cos x = -\\frac{1}{2} \\text{ (the other root, } -2\\text{, is impossible)}", [120, 240])])
    s = sum(sols)
    p = f"What is the sum, in degrees, of all solutions of ${e}$ with $0^\\circ \\le x < 360^\\circ$?"
    return Q(p, s, [s - sols[0], s + 180, sols[-1], s + 90, 360 if s != 360 else 540], "Rewrite $\\cos 2x$ to get a quadratic in one function.",
             "the sum.", "use $\\cos 2x = 1 - 2\\sin^2 x$ or $2\\cos^2 x - 1$, then factor.",
             [f"The quadratic gives ${roots}$.", "Solutions: " + ", ".join(f"${d}^\\circ$" for d in sols) + ".", f"Sum: ${s}^\\circ$."], "keeping an impossible root or missing a solution.")
