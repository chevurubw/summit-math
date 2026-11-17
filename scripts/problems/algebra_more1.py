"""Extra Algebra problem types (part 1): linear equations, rates, ratios and percents.
Every template is a different idea, so each problem in a bank is its own type."""
import math
from fractions import Fraction as F

from common import NAMES, C, Q, num, par, sg, var

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def money(v):
    """Dollar amount text: whole dollars stay whole, otherwise two decimals."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{float(v):.2f}"


def pct(v):
    """A percent choice: 20%, 12.5%, or 16 2/3% for repeating decimals."""
    v = F(v)
    if v.denominator == 1:
        t = f"{v.numerator}"
    elif 10 ** 6 % v.denominator == 0:
        t = f"{float(v):g}"
    else:
        sign, a = ("-" if v < 0 else ""), abs(v)
        whole, rest = int(a), a - int(a)
        t = sign + (str(whole) if whole else "") + f"\\tfrac{{{rest.numerator}}}{{{rest.denominator}}}"
    return C(t + "\\%", float(v))


def QP(p, ans, wrong, *args, ans_tex=None, **kw):
    """Like Q, but every choice is shown as a percent."""
    a = pct(ans)
    return Q(p, a, [pct(w) for w in wrong], *args, ans_tex=a.tex, **kw)


# ================================================================ alg_linear
S = "alg_linear"


@reg(S, "basics")
def lin_both_sides(r):
    a, c = r.sample(range(2, 10), 2)
    x = r.randint(-9, 12)
    b = r.randint(-15, 15)
    d = a * x + b - c * x
    if a == c:
        return None
    p = f"Solve for $x$: ${a}x{sg(b)} = {c}x{sg(d)}$."
    return Q(p, x, [-x, x + 1, F(d - b, a + c), x - 2, F(b + d, a - c) if F(b + d, a - c) != x else x + 3], "Collect the $x$ terms on one side and the numbers on the other.",
             "the $x$ that makes both sides equal.", "move every $x$ term to one side and every plain number to the other, then divide.",
             [f"Subtract ${c}x$ from both sides: ${a - c}x{sg(b)} = {d}$.", f"{'Subtract' if b >= 0 else 'Add'} ${abs(b)}$: ${a - c}x = {d - b}$.", f"Divide by ${a - c}$: $x = {x}$.",
              f"Check: left side ${a}({x}){sg(b)} = {a * x + b}$, right side ${c}({x}){sg(d)} = {c * x + d}$. Equal."],
             "moving a term across the equals sign without changing its sign.")


@reg(S, "basics")
def lin_fractions(r):
    a, b = r.sample([2, 3, 4, 5, 6], 2)
    L = a * b // math.gcd(a, b)
    x = L * r.randint(1, 6)
    s = x // a + x // b
    p = f"If $\\dfrac{{x}}{{{a}}} + \\dfrac{{x}}{{{b}}} = {s}$, what is $x$?"
    return Q(p, x, [s, x // 2, s * a, x + L, F(s * a * b, a + b + 1)], f"Multiply both sides by ${L}$ to clear the fractions.",
             "$x$.", f"clear the fractions by multiplying everything by the least common denominator, ${L}$.",
             [f"Multiply each term by ${L}$: ${L // a}x + {L // b}x = {s * L}$.", f"Combine: ${L // a + L // b}x = {s * L}$.", f"Divide: $x = \\frac{{{s * L}}}{{{L // a + L // b}}} = {x}$."],
             "multiplying only one fraction by the common denominator; every term must be multiplied.")


@reg(S, "basics")
def lin_distribute(r):
    a, c = r.randint(2, 6), r.randint(2, 6)
    b, d = r.randint(1, 8), r.randint(1, 8)
    x = r.randint(-6, 10)
    if a == c:
        return None
    e = a * (x + b) - c * (x - d)
    p = f"Solve ${a}(x + {b}) - {c}(x - {d}) = {e}$."
    return Q(p, x, [-x, x + 2, F(e - a * b - c * d, a - c) if a * b + c * d else x + 4, F(e - a * b + c * d, a - c), x - 1], "Distribute first. Watch the minus sign in front of the second group.",
             "$x$.", "distribute, being careful that the minus sign multiplies every term inside the second parentheses.",
             [f"Distribute: ${a}x + {a * b} - {c}x + {c * d} = {e}$. (Minus times $-{d}$ is $+{c * d}$.)", f"Combine: ${a - c}x + {a * b + c * d} = {e}$.",
              f"${a - c}x = {e - a * b - c * d}$, so $x = {x}$."],
             f"writing $-{c}x - {c * d}$; the minus sign flips the sign of both terms inside.")


@reg(S, "basics")
def lin_consecutive(r):
    k = r.choice([3, 4, 5])
    kind = r.choice(["integers", "even integers", "odd integers"])
    step = 1 if kind == "integers" else 2
    first = r.randint(5, 40)
    if kind == "even integers" and first % 2:
        first += 1
    if kind == "odd integers" and first % 2 == 0:
        first += 1
    terms = [first + i * step for i in range(k)]
    S_ = sum(terms)
    p = f"The sum of {k} consecutive {kind} is ${S_}$. What is the largest of them?"
    mid = F(S_, k)
    return Q(p, terms[-1], [terms[0], int(mid) if mid.denominator == 1 else terms[-1] + 1, terms[-1] + step, terms[-2], S_ // k + k],
             f"Call the smallest $n$; the others are $n + {step}$, $n + {2 * step}$, and so on.",
             "the largest of the numbers.", f"name the smallest number $n$; the rest are $n + {step}, n + {2 * step}, \\ldots$ Their sum is a simple equation.",
             [f"Sum: $n + (n + {step}) + \\cdots + (n + {(k - 1) * step}) = {k}n + {sum(i * step for i in range(k))} = {S_}$.", f"${k}n = {S_ - sum(i * step for i in range(k))}$, so $n = {first}$.",
              "The numbers are " + ", ".join(f"${t}$" for t in terms) + f"; the largest is ${terms[-1]}$."],
             "answering the smallest number, or the average.")


@reg(S, "basics")
def lin_rect_area(r):
    w = r.randint(3, 15)
    k = r.randint(2, 9)
    L = w + k
    P = 2 * (w + L)
    p = f"A rectangle is ${k}$ cm longer than it is wide, and its perimeter is ${P}$ cm. What is its area, in square cm?"
    return Q(p, w * L, [P, w * w, L * L, 2 * w * L, (w + 1) * (L + 1)], "Let the width be $w$. Then the length is $w + " + str(k) + "$.",
             "the area, so first the width and length.", "write the perimeter in terms of the width, solve, then multiply.",
             [f"Width $w$, length $w + {k}$. Perimeter: $2w + 2(w + {k}) = 4w + {2 * k} = {P}$.", f"$4w = {P - 2 * k}$, so $w = {w}$ and the length is ${L}$.", f"Area $= {w} \\cdot {L} = {w * L}$."],
             "using the perimeter formula with only one width and one length ($w + l$ instead of $2w + 2l$).")


@reg(S, "basics")
def lin_slope(r):
    x1, y1 = r.randint(-8, 8), r.randint(-8, 8)
    x2 = x1 + r.choice([i for i in range(-7, 8) if i])
    y2 = r.randint(-8, 8)
    m = F(y2 - y1, x2 - x1)
    p = f"What is the slope of the line through $({x1}, {y1})$ and $({x2}, {y2})$?"
    return Q(p, m, [-m if m else 1, 1 / m if m else 2, F(x2 - x1, y2 - y1) if y2 != y1 else 3, m + 1, F(y2 + y1, x2 + x1) if x2 + x1 else 4], "Slope is rise over run.",
             "the slope.", "slope $= \\frac{\\text{change in } y}{\\text{change in } x} = \\frac{y_2 - y_1}{x_2 - x_1}$.",
             [f"Change in $y$: ${y2} - {par(y1)} = {y2 - y1}$.", f"Change in $x$: ${x2} - {par(x1)} = {x2 - x1}$.", f"Slope $= \\frac{{{y2 - y1}}}{{{x2 - x1}}} = {ftex(m)}$."],
             "putting the change in $x$ on top (run over rise).")


@reg(S, "basics")
def lin_intercepts(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    c = a * b * r.randint(1, 4) * r.choice([1, -1])
    xi, yi = F(c, a), F(c, b)
    p = f"The line ${a}x + {b}y = {c}$ crosses the $x$-axis at $(p, 0)$ and the $y$-axis at $(0, q)$. What is $p + q$?"
    return Q(p, xi + yi, [xi * yi, xi - yi if xi != yi else 1, F(c, a + b), -(xi + yi), F(c, a) + F(c, a)], "On the $x$-axis $y = 0$; on the $y$-axis $x = 0$.",
             "the sum of the two intercepts.", "an intercept is where the line meets an axis, so set the other variable to $0$.",
             [f"$x$-intercept: put $y = 0$. ${a}x = {c}$, so $p = {ftex(xi)}$.", f"$y$-intercept: put $x = 0$. ${b}y = {c}$, so $q = {ftex(yi)}$.", f"$p + q = {ftex(xi + yi)}$."],
             "dividing by the wrong coefficient (for example $\\frac{c}{b}$ for the $x$-intercept).")


@reg(S, "basics")
def lin_cost_model(r):
    fee, rate = r.randint(15, 60), r.randint(8, 30)
    h = r.randint(2, 9)
    tot = fee + rate * h
    n = r.choice(NAMES)
    p = f"A plumber charges a \\${fee} visit fee plus \\${rate} per hour. {n}'s bill was \\${tot}. How many hours did the plumber work?"
    return Q(p, h, [F(tot, rate), h + 1, F(tot - fee, rate + 1), F(tot + fee, rate), h - 1], "Take off the visit fee first.",
             "the number of hours.", "the bill is the fixed fee plus the hourly rate times hours: $\\text{cost} = " + f"{fee} + {rate}h" + "$.",
             [f"${fee} + {rate}h = {tot}$.", f"Subtract the fee: ${rate}h = {tot - fee}$.", f"$h = {h}$."],
             "dividing the whole bill by the hourly rate, forgetting the fixed fee.")


@reg(S, "basics")
def lin_number_puzzle(r):
    a = r.randint(3, 6)
    b = r.randint(2, 15)
    n = r.randint(3, 20)
    c = (a - 1) * n - b
    if c <= 0:
        return None
    p = f"When a number is multiplied by ${a}$ and then decreased by ${b}$, the result is ${c}$ more than the number itself. What is the number?"
    return Q(p, n, [F(c + b, a), n + 1, F(c - b, a - 1) if c != b else n + 2, F(c + b, a + 1), 2 * n], "Let the number be $n$ and translate each phrase.",
             "the number.", "translate the words into one equation, one phrase at a time.",
             [f"'Multiplied by ${a}$ and decreased by ${b}$': ${a}n - {b}$. '${c}$ more than the number': $n + {c}$.", f"${a}n - {b} = n + {c}$.", f"${a - 1}n = {c + b}$, so $n = {n}$."],
             "forgetting that the right side is the number plus " + str(c) + ", not just " + str(c) + ".")


@reg(S, "basics")
def lin_age_self(r):
    n = r.choice(NAMES)
    v = var(n)
    k = r.choice([2, 3])
    a_, b_ = r.randint(2, 9), r.randint(2, 9)
    age = (k * b_ + a_) // (k - 1) if (k * b_ + a_) % (k - 1) == 0 else None
    if age is None or age - b_ <= 0:
        return None
    p = f"In ${a_}$ years, {n} will be {'twice' if k == 2 else 'three times'} as old as {n} was ${b_}$ years ago. How old is {n} now?"
    return Q(p, age, [age + a_, age - b_, F(a_ + b_, k), age + 1, k * age], f"Let ${v}$ be {n}'s age now.",
             f"{n}'s age today.", f"write both ages in terms of today's age ${v}$.",
             [f"In ${a_}$ years: ${v} + {a_}$. ${b_}$ years ago: ${v} - {b_}$.", f"${v} + {a_} = {k}({v} - {b_}) = {k}{v} - {k * b_}$.",
              f"${k - 1 if k > 2 else ''}{v} = {a_} + {k * b_} = {a_ + k * b_}$, so ${v} = {age}$."],
             "multiplying only the variable by " + str(k) + " instead of the whole expression in parentheses.")


@reg(S, "basics")
def lin_parallel(r):
    m = F(r.choice([1, 2, 3, -1, -2, -3]), r.choice([1, 1, 2]))
    b0 = r.randint(-9, 9)
    px, py = r.randint(-6, 6) * m.denominator, r.randint(-9, 9)
    yint = py - m * px
    p = f"A line is parallel to $y = {ftex(m)}x{sg(b0)}$ and passes through $({px}, {py})$. What is its $y$-intercept?"
    return Q(p, yint, [b0, py + m * px, -yint if yint else 1, py, yint + m], "Parallel lines have the same slope.",
             "the $y$-intercept $b$ of the new line.", "parallel means same slope, so the new line is $y = " + ftex(m) + "x + b$. Plug in the point to find $b$.",
             [f"The new line: $y = {ftex(m)}x + b$.", f"Put in $({px}, {py})$: ${py} = {ftex(m)} \\cdot {par(px)} + b = {ftex(m * px)} + b$.", f"$b = {py} - {par(m * px)} = {ftex(yint)}$."],
             "keeping the old $y$-intercept; only the slope carries over.")


@reg(S, "basics")
def lin_intersect(r):
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    x = r.randint(-5, 6)
    y = r.randint(-8, 8)
    b1, b2 = y - m1 * x, y - m2 * x
    p = f"The lines $y = {m1}x{sg(b1)}$ and $y = {m2}x{sg(b2)}$ meet at the point $(a, b)$. What is $a + b$?"
    return Q(p, x + y, [x - y, x * y, y, -x - y if x + y else 1, x + y + 1], "Set the two expressions for $y$ equal.",
             "the sum of the coordinates of the intersection.", "at the meeting point both equations give the same $y$, so set them equal to find $x$.",
             [f"${m1}x{sg(b1)} = {m2}x{sg(b2)}$, so ${m1 - m2}x = {b2 - b1}$ and $x = {x}$.", f"Then $y = {m1}({x}){sg(b1)} = {y}$.", f"$a + b = {x} + {par(y)} = {x + y}$."],
             "stopping after finding $x$ and forgetting to add $y$.")


@reg(S, "basics")
def lin_param(r):
    x0 = r.randint(-4, 6)
    if x0 == 0:
        return None
    b, c, d = r.randint(1, 12), r.randint(2, 5), r.randint(-10, 10)
    num_ = c * x0 + d + b
    if num_ % x0:
        return None
    a = num_ // x0
    p = f"For what value of $a$ is $x = {x0}$ a solution of $ax - {b} = {c}x{sg(d)}$?"
    return Q(p, a, [a + 1, -a if a else 2, c, F(c * x0 + d - b, x0), a - c], "Put $x = " + str(x0) + "$ into the equation.",
             "the value of $a$.", "a solution makes the equation true, so substitute it and solve for $a$.",
             [f"Substitute $x = {x0}$: ${par(x0)}a - {b} = {c} \\cdot {par(x0)}{sg(d)} = {c * x0 + d}$.", f"${par(x0)}a = {c * x0 + d + b}$.", f"$a = {a}$."],
             "forgetting to move the $-" + str(b) + "$ before dividing.")


@reg(S, "basics")
def lin_collinear(r):
    x1, y1 = r.randint(-5, 3), r.randint(-6, 6)
    dx = r.randint(1, 4)
    m = r.choice([-3, -2, -1, 1, 2, 3])
    x2, y2 = x1 + dx, y1 + m * dx
    x3 = x2 + r.randint(1, 5)
    k = y1 + m * (x3 - x1)
    p = f"The points $({x1}, {y1})$, $({x2}, {y2})$, and $({x3}, k)$ lie on one line. What is $k$?"
    return Q(p, k, [k + m, k - m, y2 + (x3 - x2), -k if k else 1, y1 + (x3 - x1)], "Points on one line have the same slope between every pair.",
             "the missing $y$-coordinate.", "the slope from the first point to the second must equal the slope to the third.",
             [f"Slope of the first two: $\\frac{{{y2} - {par(y1)}}}{{{x2} - {par(x1)}}} = {m}$.", f"From $({x2}, {y2})$, move ${x3 - x2}$ to the right: $y$ changes by ${m} \\cdot {x3 - x2} = {m * (x3 - x2)}$.", f"$k = {y2} + {par(m * (x3 - x2))} = {k}$."],
             "adding the $x$ change to $y$ directly, as if the slope were $1$.")


@reg(S, "basics")
def lin_proportion_eq(r):
    b, d = r.sample([2, 3, 4, 5, 6], 2)
    x = r.randint(-5, 15)
    a = r.randint(1, 9)
    # (x + a)/b = (x - c)/d  ->  d(x + a) = b(x - c)
    num_ = d * (x + a) - b * x
    if num_ % b:
        return None
    c = -num_ // b
    p = f"Solve $\\dfrac{{x + {a}}}{{{b}}} = \\dfrac{{x{sg(-c)}}}{{{d}}}$."
    return Q(p, x, [-x if x else 1, x + 1, F(b * c + d * a, d - b) if d != b else 2, x - 2, x + a], "Cross multiply.",
             "$x$.", "when two fractions are equal, cross multiply to clear the denominators.",
             [f"${d}(x + {a}) = {b}(x{sg(-c)})$.", f"${d}x + {d * a} = {b}x{sg(-b * c)}$.", f"${d - b}x = {-b * c - d * a}$, so $x = {x}$."],
             "multiplying only the $x$ by the other denominator and not the number with it.")


@reg(S, "basics")
def lin_no_solution(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    t = r.randint(2, 4)
    c, f = r.randint(1, 9), r.randint(1, 30)
    if f == t * c:
        f += 1
    k = t * b
    p = f"For what value of $k$ does the system ${a}x + {b}y = {c}$ and ${t * a}x + ky = {f}$ have no solution?"
    return Q(p, k, [b, t * a, k + 1, F(f, c), a * b], "No solution means the lines are parallel but not the same line.",
             "the $k$ that makes the lines parallel.", "two lines have no common point when they are parallel and different: same ratio of $x$ and $y$ coefficients, different constants.",
             [f"The $x$ coefficient went from ${a}$ to ${t * a}$: multiplied by ${t}$.", f"For parallel lines, the $y$ coefficient must also be multiplied by ${t}$: $k = {t} \\cdot {b} = {k}$.",
              f"Check: the constant ${f}$ is not ${t} \\cdot {c} = {t * c}$, so the lines are different. No solution."],
             "making the constants match too, which gives the same line (infinitely many solutions).")


@reg(S, "challenge")
def linc_sym3(r):
    x, y, z = [r.randint(-5, 9) for _ in range(3)]
    A, B, C_ = 2 * x + y + z, x + 2 * y + z, x + y + 2 * z
    p = f"If $2x + y + z = {A}$, $x + 2y + z = {B}$, and $x + y + 2z = {C_}$, what is $x + y + z$?"
    s = x + y + z
    return Q(p, s, [A + B + C_, F(A + B + C_, 3), s + 1, F(A + B + C_, 2), 2 * s], "Add all three equations.",
             "$x + y + z$, without finding each variable.", "the equations are symmetric. Adding them makes every variable appear the same number of times.",
             [f"Add: $4x + 4y + 4z = {A} + {par(B)} + {par(C_)} = {A + B + C_}$.", f"Divide by $4$: $x + y + z = {s}$."],
             "dividing by $3$ (the number of equations) instead of $4$ (the number of times each variable appears).")


@reg(S, "challenge")
def linc_digits(r):
    t, u = r.randint(1, 8), r.randint(2, 9)
    if u <= t:
        return None
    n = 10 * t + u
    D = 9 * (u - t)
    p = f"The digits of a two-digit number add up to ${t + u}$. Reversing the digits increases the number by ${D}$. What is the number?"
    return Q(p, n, [10 * u + t, n + 9, n - 9, t * u, 10 * (t + 1) + (u - 1)], "Write the number as $10a + b$.",
             "the original two-digit number $10a + b$.", "reversing gives $10b + a$. The difference is $9(b - a)$, which tells you how far apart the digits are.",
             [f"$a + b = {t + u}$.", f"$(10b + a) - (10a + b) = 9(b - a) = {D}$, so $b - a = {u - t}$.",
              f"Add and subtract: $2b = {t + u + u - t}$ gives $b = {u}$, and $a = {t}$.", f"The number is ${n}$. Check: ${10 * u + t} - {n} = {D}$."],
             "answering the reversed number.")


@reg(S, "challenge")
def linc_backwards(r):
    n = r.choice(NAMES)
    left = r.randint(2, 12)
    a2, a1 = r.randint(1, 6), r.randint(1, 6)
    after1 = 2 * (left + a2)
    start = 2 * (after1 + a1)
    p = (f"{n} spent half of her money plus \\${a1} at a bookstore, then half of what was left plus \\${a2} at a cafe. "
         f"She had \\${left} left. How many dollars did she start with?")
    return Q(p, start, [2 * left + a1 + a2, start - 2 * a1, 4 * left, after1, start + a1], "Work backwards from the end.",
             "the starting amount.", "undo each step in reverse: 'half plus $a$' is undone by adding $a$ back, then doubling.",
             [f"Before the cafe she had $({left} + {a2}) \\cdot 2 = {after1}$ dollars.", f"Before the bookstore she had $({after1} + {a1}) \\cdot 2 = {start}$ dollars.",
              f"Check: half of ${start}$ plus ${a1}$ is ${start // 2 + a1}$, leaving ${after1}$; half of that plus ${a2}$ is ${after1 // 2 + a2}$, leaving ${left}$."],
             "undoing in the wrong order: doubling before adding the extra amount back.")


@reg(S, "challenge")
def linc_linear_func(r):
    m = r.choice([-4, -3, -2, 2, 3, 4, F(1, 2), F(3, 2)])
    b0 = r.randint(-10, 10)
    a, b_ = r.sample(range(-6, 8), 2)
    c = r.randint(-6, 12)
    f = lambda x: m * x + b0
    if any(F(f(x)).denominator != 1 for x in (a, b_, c)):
        return None
    p = f"A linear function $f$ has $f({a}) = {f(a)}$ and $f({b_}) = {f(b_)}$. What is $f({c})$?"
    return Q(p, f(c), [f(c) + m, f(c) - m, f(a) + f(b_), F(f(a) * c, a) if a else 7, -f(c) if f(c) else 1], "Find the slope first.",
             f"$f({c})$.", "a linear function changes by the same amount for each step of $1$ in $x$ (its slope).",
             [f"Slope: $\\frac{{{f(b_)} - {par(f(a))}}}{{{b_} - {par(a)}}} = {ftex(m)}$.", f"From $x = {a}$ to $x = {c}$ is a change of ${c - a}$, so $f$ changes by ${ftex(m)} \\cdot {par(c - a)} = {ftex(m * (c - a))}$.",
              f"$f({c}) = {f(a)} + {par(m * (c - a))} = {ftex(f(c))}$."],
             "assuming $f(x)$ is proportional to $x$ (forgetting the constant term).")


@reg(S, "challenge")
def linc_swap_coeffs(r):
    a, b = r.sample(range(1, 8), 2)
    x, y = r.randint(-5, 9), r.randint(-5, 9)
    P, Qv = a * x + b * y, b * x + a * y
    ans = x * x - y * y
    p = f"If ${a}x + {b}y = {P}$ and ${b}x + {a}y = {Qv}$, what is $x^2 - y^2$?"
    return Q(p, ans, [(x + y) ** 2, x * y, x - y, ans + 1, -ans if ans else 2], "Add the equations, then subtract them.",
             "$x^2 - y^2 = (x + y)(x - y)$.", "the coefficients are swapped, so adding and subtracting the equations gives $x + y$ and $x - y$ directly.",
             [f"Add: ${a + b}(x + y) = {P + Qv}$, so $x + y = {x + y}$.", f"Subtract: ${a - b}(x - y) = {P - Qv}$, so $x - y = {x - y}$.", f"$x^2 - y^2 = ({x + y})({x - y}) = {ans}$."],
             "solving for $x$ and $y$ separately; it works but takes much longer and invites arithmetic slips.")


@reg(S, "challenge")
def linc_triangle_area(r):
    m1, m2 = r.choice([1, 2, 3]), -r.choice([1, 2, 3])
    x0, y0 = r.randint(-4, 4), r.randint(2, 9)
    xa, xb = x0 - F(y0, m1), x0 - F(y0, m2)
    area = F(1, 2) * abs(xb - xa) * y0
    p = f"What is the area of the triangle bounded by the lines $y = {m1}x{sg(y0 - m1 * x0)}$, $y = {m2}x{sg(y0 - m2 * x0)}$, and the $x$-axis?"
    return Q(p, area, [area * 2, abs(xb - xa), F(y0 * y0, 2), area + 1, y0 * abs(xb - xa)], "Find where the lines meet each other and where each meets the $x$-axis.",
             "the area of the triangle.", "the base lies on the $x$-axis between the two $x$-intercepts; the height is the $y$-coordinate where the lines cross.",
             [f"The lines meet where ${m1}x{sg(y0 - m1 * x0)} = {m2}x{sg(y0 - m2 * x0)}$, at $({x0}, {y0})$. Height $= {y0}$.",
              f"$x$-intercepts: $x = {ftex(xa)}$ and $x = {ftex(xb)}$. Base $= {ftex(abs(xb - xa))}$.", f"Area $= \\frac{{1}}{{2}} \\cdot {ftex(abs(xb - xa))} \\cdot {y0} = {ftex(area)}$."],
             "forgetting the $\\frac{1}{2}$ in the triangle area formula.")


@reg(S, "challenge")
def linc_diophantine(r):
    a, b = r.sample([2, 3, 4, 5, 7], 2)
    c = r.randint(30, 90)
    sols = [(x, (c - a * x) // b) for x in range(1, c // a + 1) if (c - a * x) > 0 and (c - a * x) % b == 0]
    if not sols:
        return None
    n = len(sols)
    p = f"How many ordered pairs of positive integers $(x, y)$ satisfy ${a}x + {b}y = {c}$?"
    first = sols[0]
    return Q(p, n, [n + 1, n - 1 if n > 1 else n + 2, c // (a * b), n + 2, c // a], "Find one solution, then step: $x$ goes up by " + str(b) + " while $y$ goes down by " + str(a) + ".",
             "the count of positive whole number solutions.", f"once you have one solution, the others come from adding ${b}$ to $x$ and subtracting ${a}$ from $y$ (this keeps ${a}x + {b}y$ the same).",
             [f"Smallest positive $x$ that works: $x = {first[0]}$, $y = {first[1]}$.", f"Step $x$ by ${b}$ and $y$ by $-{a}$ while $y$ stays positive: " + ", ".join(f"$({x}, {y})$" for x, y in sols) + ".", f"That is ${n}$ pairs."],
             "including solutions with $y = 0$ or negative $y$.")


# ================================================================ alg_rates
S = "alg_rates"


@reg(S, "basics")
def rate_time_minutes(r):
    v = r.choice([30, 40, 45, 48, 50, 60, 72])
    t_min = r.choice([10, 15, 20, 25, 30, 40, 45, 50, 75, 90])
    d = F(v * t_min, 60)
    if d.denominator != 1:
        return None
    n = r.choice(NAMES)
    p = f"{n} drives ${d}$ miles at a steady ${v}$ miles per hour. How many minutes does the trip take?"
    return Q(p, t_min, [F(d, v), F(v, d) * 60, t_min + 5, F(d * 60, v + 10), 2 * t_min], "Time $=$ distance $\\div$ speed, then convert hours to minutes.",
             "the trip time in minutes.", "time $= \\frac{\\text{distance}}{\\text{speed}}$ gives hours; multiply by $60$ for minutes.",
             [f"$\\frac{{{d}}}{{{v}}} = {ftex(F(d, v))}$ hours.", f"${ftex(F(d, v))} \\cdot 60 = {t_min}$ minutes."],
             "leaving the answer in hours.")


@reg(S, "basics")
def rate_units(r):
    v = r.choice([5, 10, 15, 20, 25, 30])
    ans = F(v * 18, 5)
    p = f"A cyclist travels ${v}$ meters per second. What is this speed in kilometers per hour?"
    return Q(p, ans, [F(v * 60, 1000) * 60 / 1000 if False else F(v * 5, 18), v * 60, F(v * 3600, 100), ans + 10, F(v, 1)], "Multiply by $3600$ seconds per hour, divide by $1000$ meters per kilometer.",
             "the speed in km per hour.", "convert one unit at a time: seconds to hours (there are $3600$ seconds in an hour) and meters to kilometers ($1000$ m in a km).",
             [f"Per hour: ${v} \\cdot 3600 = {v * 3600}$ meters.", f"In kilometers: $\\frac{{{v * 3600}}}{{1000}} = {ftex(ans)}$."],
             "multiplying by $60$ only once (that converts to minutes, not hours).")


@reg(S, "basics")
def rate_opposite(r):
    v1, v2 = r.randint(30, 70), r.randint(30, 70)
    t = F(r.choice([1, 2, 3, 4, 5]), r.choice([1, 2]))
    D = (v1 + v2) * t
    if D.denominator != 1:
        return None
    p = f"Two cars leave the same town at the same time, one heading east at ${v1}$ mph and the other west at ${v2}$ mph. After how many hours are they ${D}$ miles apart?"
    return Q(p, t, [F(D, abs(v1 - v2)) if v1 != v2 else t * 2, F(D, v1), t * 2, F(D, max(v1, v2)), t + 1], "Moving apart, their speeds add.",
             "the time until they are " + str(D) + " miles apart.", "in opposite directions the gap grows by the sum of the speeds each hour.",
             [f"Gap grows ${v1} + {v2} = {v1 + v2}$ miles per hour.", f"Time $= \\frac{{{D}}}{{{v1 + v2}}} = {ftex(t)}$ hours."],
             "subtracting the speeds; that is for cars going the same way.")


@reg(S, "basics")
def rate_meet(r):
    n1, n2 = r.sample(NAMES, 2)
    v1, v2 = r.randint(3, 8), r.randint(3, 8)
    t = r.randint(2, 6)
    D = (v1 + v2) * t
    p = f"{n1} and {n2} live ${D}$ miles apart. They walk toward each other, {n1} at ${v1}$ mph and {n2} at ${v2}$ mph. How many miles has {n1} walked when they meet?"
    return Q(p, v1 * t, [v2 * t, F(D, 2), t, v1 * t + v1, D - v2 * t + v2], "First find how long until they meet.",
             f"the distance {n1} covers.", "walking toward each other, the gap shrinks by the sum of the speeds.",
             [f"Gap shrinks ${v1} + {v2} = {v1 + v2}$ miles each hour, so they meet after $\\frac{{{D}}}{{{v1 + v2}}} = {t}$ hours.", f"{n1} walks ${v1} \\cdot {t} = {v1 * t}$ miles."],
             "assuming they meet halfway, which only happens if their speeds are equal.")


@reg(S, "basics")
def rate_work_alone(r):
    a = r.choice([3, 4, 5, 6, 8, 10, 12])
    b = r.choice([3, 4, 5, 6, 8, 10, 12, 15, 20, 24])
    if a == b:
        return None
    t = F(a * b, a + b)
    n1, n2 = r.sample(NAMES, 2)
    p = f"{n1} and {n2} together can mow a lawn in ${ftex(t)}$ hours. {n1} alone takes ${a}$ hours. How many hours would {n2} take alone?"
    return Q(p, b, [abs(t - a) if t != a else 1, a + t, F(a, 2), F(a + b, 2), b + 1], "Work with rates: fractions of the lawn per hour.",
             f"{n2}'s time alone.", "rates add: (together rate) $=$ (one rate) $+$ (other rate). Each rate is $\\frac{1}{\\text{time}}$.",
             [f"Together: $\\frac{{1}}{{{ftex(t)}}} = {ftex(1 / t)}$ of the lawn per hour. {n1}: $\\frac{{1}}{{{a}}}$.", f"{n2}'s rate: ${ftex(1 / t)} - \\frac{{1}}{{{a}}} = {ftex(1 / t - F(1, a))}$.", f"Time $= \\frac{{1}}{{{ftex(1 / t - F(1, a))}}} = {b}$ hours."],
             "subtracting the times instead of the rates.")


@reg(S, "basics")
def rate_avg_times(r):
    v1, v2 = r.randint(20, 60), r.randint(20, 60)
    t1, t2 = r.randint(1, 4), r.randint(1, 4)
    if v1 == v2:
        return None
    avg = F(v1 * t1 + v2 * t2, t1 + t2)
    p = f"A bus travels for ${t1}$ hour{'s' if t1 > 1 else ''} at ${v1}$ mph and then for ${t2}$ hour{'s' if t2 > 1 else ''} at ${v2}$ mph. What is its average speed for the whole trip, in mph?"
    return Q(p, avg, [F(v1 + v2, 2), avg + 1, F(2 * v1 * v2, v1 + v2), F(v1 * t2 + v2 * t1, t1 + t2), max(v1, v2)], "Average speed is total distance over total time.",
             "the average speed.", "average speed $= \\frac{\\text{total distance}}{\\text{total time}}$, not the average of the two speeds.",
             [f"Distances: ${v1} \\cdot {t1} = {v1 * t1}$ and ${v2} \\cdot {t2} = {v2 * t2}$; total ${v1 * t1 + v2 * t2}$ miles.", f"Total time: ${t1 + t2}$ hours.", f"Average: $\\frac{{{v1 * t1 + v2 * t2}}}{{{t1 + t2}}} = {ftex(avg)}$ mph."],
             "averaging the two speeds; that only works when the times are equal.")


@reg(S, "basics")
def rate_walk_run(r):
    w, ru = r.choice([3, 4]), r.choice([6, 8, 9, 10, 12])
    tr = F(r.randint(1, 4), 2)
    tw = F(r.randint(1, 4), 2)
    D = w * tw + ru * tr
    T = tw + tr
    if D.denominator != 1:
        return None
    n = r.choice(NAMES)
    p = f"{n} covers ${D}$ miles in ${ftex(T)}$ hours, walking part of the way at ${w}$ mph and running the rest at ${ru}$ mph. How many hours did {n} spend running?"
    return Q(p, tr, [tw, F(D, ru), T - F(D, ru), tr + F(1, 2), F(T, 2)], "Let $t$ be the running time; the walking time is the rest.",
             "the running time $t$.", "write the total distance using the two times, which must add to the total time.",
             [f"Walking time: ${ftex(T)} - t$.", f"Distance: ${ru}t + {w}({ftex(T)} - t) = {D}$.", f"${ru - w}t = {D} - {ftex(w * T)} = {ftex(D - w * T)}$, so $t = {ftex(tr)}$ hours."],
             "answering the walking time instead.")


@reg(S, "basics")
def rate_reading(r):
    ppm = r.choice([F(1, 2), F(2, 3), F(3, 4), 1, F(3, 2), 2])
    N = r.choice([180, 240, 300, 360, 420, 480])
    mins = N / ppm
    hrs = mins / 60
    if F(hrs).denominator not in (1, 2, 4):
        return None
    n = r.choice(NAMES)
    p = f"{n} reads ${ftex(ppm)}$ of a page per minute. How many hours will it take {n} to read a ${N}$ page book?" if ppm < 1 else f"{n} reads ${ftex(ppm)}$ pages per minute. How many hours will it take {n} to read a ${N}$ page book?"
    return Q(p, hrs, [N * ppm / 60, mins, hrs * 2, hrs + 1, F(N, 60)], "Minutes $=$ pages $\\div$ pages per minute.",
             "the reading time in hours.", "time $= \\frac{\\text{amount}}{\\text{rate}}$; then convert minutes to hours.",
             [f"Minutes: $\\frac{{{N}}}{{{ftex(ppm)}}} = {ftex(mins)}$.", f"Hours: $\\frac{{{ftex(mins)}}}{{60}} = {ftex(hrs)}$."],
             "multiplying by the rate instead of dividing.")


@reg(S, "basics")
def rate_gas(r):
    mpg = r.choice([20, 24, 25, 28, 30, 32, 35, 40])
    miles = mpg * r.randint(3, 12)
    price = F(r.randint(250, 450), 100)
    cost = F(miles, mpg) * price
    p = f"A car gets ${mpg}$ miles per gallon. Gas costs \\${float(price):.2f} per gallon. How many dollars does gas cost for a ${miles}$ mile trip?"
    ans = C(f"\\${float(cost):.2f}", float(cost))
    return Q(p, ans, [C(f"\\${float(miles * price / 10):.2f}", float(miles * price / 10)), C(f"\\${float(cost + price):.2f}", float(cost + price)), C(f"\\${float(cost * 2):.2f}", float(cost * 2)),
                      C(f"\\${float(F(mpg, 1) * price):.2f}", float(mpg * price)), C(f"\\${float(cost - price):.2f}", float(cost - price))],
             "First find how many gallons the trip uses.", "the cost of the trip.", "gallons $= \\frac{\\text{miles}}{\\text{miles per gallon}}$; cost $=$ gallons $\\times$ price.",
             [f"Gallons: $\\frac{{{miles}}}{{{mpg}}} = {miles // mpg}$.", f"Cost: ${miles // mpg} \\cdot {float(price):.2f} = {float(cost):.2f}$ dollars."],
             "multiplying the miles by the price per gallon.", ans_tex=f"\\${float(cost):.2f}")


@reg(S, "basics")
def rate_fill(r):
    B = r.choice([4, 5, 6, 8, 10, 12])
    t = r.choice([15, 20, 24, 30, 40, 45])
    T = B * r.randint(5, 30)
    secs = F(T, B) * t
    mins = secs / 60
    if mins.denominator not in (1, 2, 4):
        return None
    p = f"A hose fills a ${B}$ liter bucket in ${t}$ seconds. At this rate, how many minutes does it take to fill a ${T}$ liter tank?"
    return Q(p, mins, [secs, F(T, t), mins * 2, F(T * B, t * 60), mins + 1], "Find how many buckets fit in the tank.",
             "the filling time in minutes.", "the rate is fixed, so time scales with volume.",
             [f"The tank holds $\\frac{{{T}}}{{{B}}} = {T // B}$ buckets.", f"Time: ${T // B} \\cdot {t} = {ftex(secs)}$ seconds $= {ftex(mins)}$ minutes."],
             "forgetting to convert seconds to minutes.")


@reg(S, "basics")
def rate_laps(r):
    L = r.choice([200, 300, 400])
    t = r.choice([60, 75, 80, 90, 100, 120])
    M = r.randint(10, 30)
    laps = (M * 60) // t
    p = f"A runner completes one ${L}$ meter lap every ${t}$ seconds. How many complete laps does she finish in ${M}$ minutes?"
    return Q(p, laps, [laps + 1, M * 60 * t // L if M * 60 * t // L != laps else laps + 3, F(M * L, t) if F(M * L, t).denominator == 1 else laps - 1, M, laps * 2], "Convert minutes to seconds.",
             "the number of full laps.", "laps $= \\frac{\\text{total time}}{\\text{time per lap}}$, rounded down to whole laps.",
             [f"${M}$ minutes $= {M * 60}$ seconds.", f"$\\frac{{{M * 60}}}{{{t}}} = {ftex(F(M * 60, t))}$, so she completes ${laps}$ full laps." + (" The lap length doesn't matter." if True else "")],
             "using the lap length; the time per lap already accounts for it.")


@reg(S, "basics")
def rate_workers_days(r):
    w1 = r.randint(3, 12)
    d1 = r.randint(4, 20)
    total = w1 * d1
    w2 = r.choice([x for x in range(2, 30) if total % x == 0 and x != w1] or [None])
    if w2 is None:
        return None
    d2 = total // w2
    p = f"${w1}$ workers can paint a building in ${d1}$ days. How many days would ${w2}$ workers take, working at the same rate?"
    return Q(p, d2, [F(d1 * w2, w1), d1 + w1 - w2, d2 + 1, total, F(d1, 2)], "More workers means fewer days: multiply to find the total worker-days.",
             "the number of days for " + str(w2) + " workers.", "the job takes a fixed number of worker-days (workers $\\times$ days).",
             [f"Total work: ${w1} \\cdot {d1} = {total}$ worker-days.", f"With ${w2}$ workers: $\\frac{{{total}}}{{{w2}}} = {d2}$ days."],
             "scaling the days up when there are more workers (treating it as direct, not inverse, variation).")


@reg(S, "basics")
def rate_fraction_done(r):
    n = r.choice(NAMES)
    frac = r.choice([F(1, 3), F(1, 4), F(2, 5), F(3, 8), F(2, 3), F(3, 5)])
    h = r.choice([2, 3, 4, 6])
    total = h / frac
    rest = total - h
    p = f"{n} finished ${ftex(frac)}$ of a puzzle in ${h}$ hours. Working at the same rate, how many more hours will {n} need to finish it?"
    return Q(p, rest, [total, h, rest + 1, h * (1 - frac), F(h, 2)], "First find the time for the whole puzzle.",
             "the remaining time.", "if a fraction takes some time, the whole job takes that time divided by the fraction.",
             [f"Whole puzzle: $\\frac{{{h}}}{{{ftex(frac)}}} = {ftex(total)}$ hours.", f"Remaining: ${ftex(total)} - {h} = {ftex(rest)}$ hours."],
             "answering the total time instead of the remaining time.")


@reg(S, "basics")
def rate_mph_from_minutes(r):
    d = r.choice([1, 2, 3, 4, 5, 6])
    t = r.choice([8, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45])
    v = F(d * 60, t)
    p = f"A jogger covers ${d}$ mile{'s' if d > 1 else ''} in ${t}$ minutes. What is her speed in miles per hour?"
    return Q(p, v, [F(d, t), F(t, d), v * 2, F(d * 60, t + 10), v + 1], "There are $60$ minutes in an hour.",
             "the speed in mph.", "speed $= \\frac{\\text{distance}}{\\text{time}}$, with the time in hours.",
             [f"${t}$ minutes $= \\frac{{{t}}}{{60}} = {ftex(F(t, 60))}$ hour.", f"Speed: $\\frac{{{d}}}{{{ftex(F(t, 60))}}} = {ftex(v)}$ mph."],
             "dividing distance by minutes and calling it mph.")


@reg(S, "basics")
def rate_train_pole(r):
    L = r.choice([120, 150, 180, 200, 240, 300])
    v = r.choice([10, 12, 15, 20, 24, 25, 30])
    t = F(L, v)
    p = f"A train ${L}$ meters long travels at ${v}$ meters per second. How many seconds does it take to pass a signal pole completely?"
    return Q(p, t, [F(L, 2 * v), t * 2, F(v, 1), t + 5, F(L, v + 5)], "The front reaches the pole, then the whole length must go by.",
             "the time to pass the pole.", "the train has passed when its back end reaches the pole, so it must travel its own length.",
             [f"Distance traveled: the train's length, ${L}$ m.", f"Time: $\\frac{{{L}}}{{{v}}} = {ftex(t)}$ seconds."],
             "thinking the time is zero because a pole has no width; the train's own length still has to pass.")


@reg(S, "basics")
def rate_race_gap(r):
    n1, n2 = r.sample(NAMES, 2)
    v1, v2 = r.sample([4, 5, 6, 8, 10, 12], 2)
    if v1 < v2:
        v1, v2 = v2, v1
    D = r.choice([3, 4, 6, 8, 10, 12])
    gap = F(D, v2) * 60 - F(D, v1) * 60
    p = f"In a ${D}$ mile race, {n1} runs at ${v1}$ mph and {n2} at ${v2}$ mph. How many minutes before {n2} does {n1} finish?"
    return Q(p, gap, [F(D, v1) * 60, F(D, v2) * 60, F(D, v1 - v2), gap / 60, gap + 10], "Find each runner's time in minutes.",
             "the gap between finishing times.", "each finishing time is distance over speed; subtract them.",
             [f"{n1}: $\\frac{{{D}}}{{{v1}}}$ h $= {ftex(F(D, v1) * 60)}$ min.", f"{n2}: $\\frac{{{D}}}{{{v2}}}$ h $= {ftex(F(D, v2) * 60)}$ min.", f"Gap: ${ftex(gap)}$ minutes."],
             "dividing the distance by the difference in speeds, which gives the wrong kind of quantity.")


@reg(S, "challenge")
def ratec_escalator(r):
    a, b = r.sample([20, 24, 30, 36, 40, 45, 60, 90], 2)
    t = F(a * b, a + b)
    n = r.choice(NAMES)
    p = f"Standing still on a moving escalator, {n} reaches the top in ${a}$ seconds. Walking up the escalator while it is turned off takes ${b}$ seconds. How many seconds does it take if {n} walks up while it moves?"
    return Q(p, t, [F(a + b, 2), abs(a - b), t + 5, min(a, b), F(a * b, abs(a - b))], "Add the rates, in escalators per second.",
             "the time with both moving.", "think of rates: each second the escalator does $\\frac{1}{" + str(a) + "}$ of the trip and walking does $\\frac{1}{" + str(b) + "}$.",
             [f"Combined rate: $\\frac{{1}}{{{a}}} + \\frac{{1}}{{{b}}} = {ftex(F(1, a) + F(1, b))}$ of the trip per second.", f"Time: $\\frac{{1}}{{{ftex(F(1, a) + F(1, b))}}} = {ftex(t)}$ seconds."],
             "averaging the two times; working together must be faster than either alone.")


@reg(S, "challenge")
def ratec_platform(r):
    v = r.choice([10, 12, 15, 20, 25])
    t1 = r.choice([6, 8, 10, 12])
    L = v * t1
    P = v * r.randint(5, 20)
    t2 = (L + P) // v
    p = f"A train passes a pole in ${t1}$ seconds and passes completely through a ${P}$ meter long station platform in ${t2}$ seconds. How long is the train, in meters?"
    return Q(p, L, [P, L + P, v, F(P, t2 - t1) * t2, L * 2], "Passing the platform means traveling the platform's length plus its own.",
             "the train's length.", "passing a pole means traveling one train length; passing a platform means traveling train length plus platform length.",
             [f"The extra ${t2} - {t1} = {t2 - t1}$ seconds cover the platform's ${P}$ m, so the speed is $\\frac{{{P}}}{{{t2 - t1}}} = {v}$ m/s.", f"Train length $= {v} \\cdot {t1} = {L}$ m."],
             "using only the platform length as the distance for the second time.")


@reg(S, "challenge")
def ratec_three_legs(r):
    vs = r.sample([10, 12, 15, 20, 30, 40, 60], 3)
    avg = F(3, sum(F(1, v) for v in vs))
    p = f"A cyclist rides up a hill at ${vs[0]}$ km/h, across a flat stretch at ${vs[1]}$ km/h, and down at ${vs[2]}$ km/h. All three stretches are the same length. What is the average speed for the ride, in km/h?"
    return Q(p, avg, [F(sum(vs), 3), avg + 2, F(sum(vs), 2), max(vs) - min(vs), F(3 * vs[0] * vs[1], vs[0] + vs[1])], "Pick a convenient length for each stretch.",
             "the average speed.", "with equal distances, the time spent at each speed differs, so use total distance over total time.",
             [f"Let each stretch be $d$. Times: $\\frac{{d}}{{{vs[0]}}} + \\frac{{d}}{{{vs[1]}}} + \\frac{{d}}{{{vs[2]}}} = {ftex(sum(F(1, v) for v in vs))}d$.", f"Average $= \\frac{{3d}}{{{ftex(sum(F(1, v) for v in vs))}d}} = {ftex(avg)}$ km/h."],
             "averaging the three speeds; more time is spent at the slow speed, which pulls the average down.")


@reg(S, "challenge")
def ratec_leaves(r):
    a, b = r.sample([4, 5, 6, 8, 10, 12], 2)
    h = r.randint(1, 2)
    done = h * (F(1, a) + F(1, b))
    if done >= 1:
        return None
    rest = (1 - done) * b
    total = h + rest
    n1, n2 = r.sample(NAMES, 2)
    p = f"{n1} can build a fence in ${a}$ hours and {n2} in ${b}$ hours. They work together for ${h}$ hour{'s' if h > 1 else ''}, then {n1} leaves and {n2} finishes alone. How many hours does the whole job take?"
    return Q(p, total, [F(a * b, a + b), rest, total + 1, F(a + b, 2), b], "Find the fraction done together first.",
             "the total time from start to finish.", "add up the fractions of the job: together for " + str(h) + " hour(s), then " + n2 + " alone for the rest.",
             [f"Together they do $\\frac{{1}}{{{a}}} + \\frac{{1}}{{{b}}} = {ftex(F(1, a) + F(1, b))}$ per hour, so ${ftex(done)}$ of the job in ${h}$ hour{'s' if h > 1 else ''}.",
              f"Left: ${ftex(1 - done)}$. {n2} alone needs ${ftex(1 - done)} \\cdot {b} = {ftex(rest)}$ hours.", f"Total: ${h} + {ftex(rest)} = {ftex(total)}$ hours."],
             "answering only the time " + n2 + " works alone.")


@reg(S, "challenge")
def ratec_track(r):
    v1, v2 = r.sample([2, 3, 4, 5, 6, 8], 2)
    if v1 < v2:
        v1, v2 = v2, v1
    L = r.choice([240, 300, 360, 400, 480])
    t_opp = F(L, v1 + v2)
    t_same = F(L, v1 - v2)
    p = f"Two runners on a ${L}$ meter circular track start together. Running in opposite directions they meet every ${ftex(t_opp)}$ seconds; running in the same direction, the faster one laps the slower every ${ftex(t_same)}$ seconds. What is the faster runner's speed, in m/s?"
    return Q(p, v1, [v2, v1 + v2, v1 - v2, F(v1 + v2, 2), v1 + 1], "Opposite directions: speeds add. Same direction: they subtract.",
             "the faster speed.", "meeting from opposite directions closes the track length at the sum of speeds; lapping closes it at the difference.",
             [f"Sum of speeds: $\\frac{{{L}}}{{{ftex(t_opp)}}} = {v1 + v2}$ m/s.", f"Difference: $\\frac{{{L}}}{{{ftex(t_same)}}} = {v1 - v2}$ m/s.", f"Faster speed: $\\frac{{{v1 + v2} + {v1 - v2}}}{{2}} = {v1}$ m/s."],
             "matching the sum with the same direction case, which swaps the two speeds' roles.")


@reg(S, "challenge")
def ratec_clock(r):
    h = r.randint(1, 11)
    m = r.choice([0, 10, 15, 20, 30, 40, 45, 50])
    hour_deg = F(h * 60 + m, 2)
    minute_deg = 6 * m
    diff = abs(hour_deg - minute_deg) % 360
    ang = min(diff, 360 - diff)
    p = f"What is the smaller angle, in degrees, between the hour and minute hands of a clock at {h}:{m:02d}?"
    return Q(p, ang, [abs(30 * h - minute_deg) % 360 if abs(30 * h - minute_deg) % 360 != ang else ang + 15, 360 - ang if 360 - ang != ang else ang + 30, ang + F(m, 2), ang + 5, 30 * h % 360 if 30 * h % 360 != ang else ang - 10],
             "The hour hand also moves: half a degree per minute.", "the smaller angle between the hands.", "the minute hand moves $6^\\circ$ per minute; the hour hand moves $30^\\circ$ per hour plus $\\frac{1}{2}^\\circ$ per minute.",
             [f"Minute hand: ${m} \\cdot 6 = {minute_deg}^\\circ$ from 12.", f"Hour hand: ${h} \\cdot 30 + {m} \\cdot \\frac{{1}}{{2}} = {ftex(hour_deg)}^\\circ$ from 12.",
              f"Difference: ${ftex(diff)}^\\circ$; the smaller angle is ${ftex(ang)}^\\circ$."],
             "keeping the hour hand exactly on the " + str(h) + "; it creeps forward as the minutes pass.")


@reg(S, "challenge")
def ratec_late_early(r):
    v1, v2 = r.sample([30, 36, 40, 45, 48, 50, 60, 72, 75, 80, 90], 2)
    if v1 > v2:
        v1, v2 = v2, v1
    m = r.choice([5, 6, 10, 12, 15, 20])
    D = F(2 * m, 60) / (F(1, v1) - F(1, v2))
    if D.denominator != 1:
        return None
    n = r.choice(NAMES)
    p = f"If {n} drives to work at ${v1}$ mph, {n} arrives ${m}$ minutes late. At ${v2}$ mph, {n} arrives ${m}$ minutes early. How many miles is the drive?"
    return Q(p, D, [D / 2, D * 2, F(v1 + v2, 2), D + v1, F(m * (v1 + v2), 60)], "The two trip times differ by " + str(2 * m) + " minutes.",
             "the distance $d$.", "late by " + str(m) + " and early by " + str(m) + " means the two travel times differ by " + str(2 * m) + " minutes.",
             [f"$\\frac{{d}}{{{v1}}} - \\frac{{d}}{{{v2}}} = \\frac{{{2 * m}}}{{60}}$ hours.", f"$d\\left(\\frac{{1}}{{{v1}}} - \\frac{{1}}{{{v2}}}\\right) = d \\cdot {ftex(F(1, v1) - F(1, v2))} = {ftex(F(2 * m, 60))}$.", f"$d = {ftex(D)}$ miles."],
             "using a time difference of " + str(m) + " minutes instead of " + str(2 * m) + ".")


# ================================================================ alg_ratios
S = "alg_ratios"


@reg(S, "basics")
def rp_percent_change(r):
    old = r.choice([20, 25, 40, 50, 60, 80, 120, 150, 200])
    pc = r.choice([-60, -40, -25, -20, -10, 10, 15, 20, 25, 30, 50, 75])
    new = F(old * (100 + pc), 100)
    if new.denominator != 1:
        return None
    p = f"A price changed from \\${old} to \\${new}. By what percent did it {'increase' if pc > 0 else 'decrease'}?"
    return QP(p, abs(pc), [F(abs(new - old) * 100, new), abs(new - old), abs(pc) + 5, 100 - abs(pc) if 100 - abs(pc) != abs(pc) else 40, abs(pc) * 2], "Percent change is change over the original.",
             "the percent change.", "percent change $= \\frac{\\text{change}}{\\text{original}} \\times 100\\%$; always divide by the starting value.",
             [f"Change: ${abs(new - old)}$ dollars.", f"$\\frac{{{abs(new - old)}}}{{{old}}} = {ftex(F(abs(new - old), old))} = {abs(pc)}\\%$."],
             "dividing by the new price instead of the original.", ans_tex=f"{abs(pc)}\\%")


@reg(S, "basics")
def rp_percent_of_percent(r):
    a, b = r.choice([10, 20, 25, 40, 50, 75]), r.choice([10, 20, 30, 40, 50, 60, 80])
    N = r.choice([200, 400, 500, 800, 1000, 1200])
    ans = F(a * b * N, 10000)
    if ans.denominator != 1:
        return None
    p = f"What is ${a}\\%$ of ${b}\\%$ of ${N}$?"
    return Q(p, ans, [F((a + b) * N, 100), F(a * N, 100), F(b * N, 100), ans * 10, ans + a], "Turn each percent into a fraction and multiply.",
             "the value.", "'of' means multiply. Convert each percent to a decimal or fraction.",
             [f"${b}\\%$ of ${N}$: ${ftex(F(b, 100))} \\cdot {N} = {ftex(F(b * N, 100))}$.", f"${a}\\%$ of that: ${ftex(F(a, 100))} \\cdot {ftex(F(b * N, 100))} = {ftex(ans)}$."],
             "adding the percents to get " + str(a + b) + "%.")


@reg(S, "basics")
def rp_recipe(r):
    s1 = r.choice([4, 6, 8, 12])
    c1 = F(r.randint(1, 6), r.choice([1, 2, 3, 4]))
    s2 = r.choice([x for x in [2, 3, 9, 10, 15, 18, 20] if x != s1])
    c2 = c1 * s2 / s1
    p = f"A recipe for ${s1}$ servings uses ${ftex(c1)}$ cups of flour. How many cups are needed for ${s2}$ servings?"
    return Q(p, c2, [c1 + s2 - s1, c1 * s1 / s2, c2 + 1, c1 * s2, c2 * 2], "Find the flour per serving.",
             "the flour for " + str(s2) + " servings.", "amounts scale in proportion to the number of servings.",
             [f"Per serving: $\\frac{{{ftex(c1)}}}{{{s1}}} = {ftex(c1 / s1)}$ cup.", f"For ${s2}$: ${s2} \\cdot {ftex(c1 / s1)} = {ftex(c2)}$ cups."],
             "adding the difference in servings instead of scaling.")


@reg(S, "basics")
def rp_map_scale(r):
    k = r.choice([5, 10, 20, 25, 50])
    d = F(r.randint(3, 30), 2)
    p = f"On a map, $1$ cm represents ${k}$ km. Two towns are ${ftex(d)}$ cm apart on the map. How many km apart are they?"
    return Q(p, d * k, [d / k, d + k, d * k * 10, d * k / 2, k], "Multiply the map distance by the scale.",
             "the real distance.", "every map centimeter stands for " + str(k) + " km.",
             [f"${ftex(d)} \\cdot {k} = {ftex(d * k)}$ km."], "dividing by the scale.")


@reg(S, "basics")
def rp_three_part(r):
    a, b, c = r.sample(range(1, 10), 3)
    m = r.randint(2, 12)
    N = (a + b + c) * m
    hi, lo = max(a, b, c) * m, min(a, b, c) * m
    p = f"Prize money of \\${N} is split among three winners in the ratio ${a}:{b}:{c}$. How many dollars more does the largest share get than the smallest?"
    return Q(p, hi - lo, [hi, lo, max(a, b, c) - min(a, b, c), F(N, 3), hi - lo + m], "Each 'part' is worth the same amount.",
             "the gap between the largest and smallest shares.", "a ratio $a:b:c$ splits the total into $a + b + c$ equal parts.",
             [f"Parts: ${a} + {b} + {c} = {a + b + c}$; one part is $\\frac{{{N}}}{{{a + b + c}}} = {m}$ dollars.", f"Largest share ${max(a, b, c)} \\cdot {m} = {hi}$, smallest ${min(a, b, c)} \\cdot {m} = {lo}$.", f"Difference: ${hi - lo}$."],
             "subtracting the ratio numbers without multiplying by the size of one part.")


@reg(S, "basics")
def rp_tax_back(r):
    t = r.choice([5, 6, 8, 10, 20, 25])
    orig = r.choice([20, 40, 50, 60, 80, 100, 120, 150, 200])
    tot = F(orig * (100 + t), 100)
    p = f"After a ${t}\\%$ sales tax is added, a bike costs \\${money(tot)}. What was the price before tax, in dollars?"
    return Q(p, orig, [tot * (100 - t) / 100, tot - t, orig + t, tot / 2, orig - t], "The total is " + str(100 + t) + "% of the original price.",
             "the price before tax.", f"adding ${t}\\%$ means the total is ${100 + t}\\%$ of the original, so divide by ${ftex(F(100 + t, 100))}$.",
             [f"Total $= {ftex(F(100 + t, 100))} \\times$ original.", f"Original $= \\frac{{{ftex(tot)}}}{{{ftex(F(100 + t, 100))}}} = {orig}$."],
             f"taking ${t}\\%$ off the total; the tax was ${t}\\%$ of the smaller original price.")


@reg(S, "basics")
def rp_discount_back(r):
    d = r.choice([10, 20, 25, 30, 40, 50, 60])
    orig = r.choice([40, 60, 80, 100, 120, 150, 200, 250])
    sale = F(orig * (100 - d), 100)
    p = f"A jacket is on sale for ${d}\\%$ off. The sale price is \\${money(sale)}. What was the original price, in dollars?"
    return Q(p, orig, [sale * (100 + d) / 100, sale + d, sale / (1 - F(d, 50)) if d < 50 else orig + 10, orig - 10, sale * 2], "The sale price is " + str(100 - d) + "% of the original.",
             "the original price.", f"after ${d}\\%$ off, ${100 - d}\\%$ of the price is left.",
             [f"${ftex(F(100 - d, 100))} \\times \\text{{original}} = {ftex(sale)}$.", f"Original $= {ftex(sale)} \\div {ftex(F(100 - d, 100))} = {orig}$."],
             f"adding ${d}\\%$ of the sale price back on.")


@reg(S, "basics")
def rp_more_girls(r):
    a, b = r.sample(range(2, 9), 2)
    if a > b:
        a, b = b, a
    m = r.randint(2, 8)
    diff = (b - a) * m
    p = f"In a club, the ratio of boys to girls is ${a}:{b}$. There are ${diff}$ more girls than boys. How many members are there in all?"
    return Q(p, (a + b) * m, [diff * (a + b), b * m, a * m, (a + b) * diff // max(1, b - a) + 1, a + b], "The difference is " + str(b - a) + " parts.",
             "the total number of members.", "girls minus boys is " + str(b) + " $-$ " + str(a) + " parts, so you can find the size of one part.",
             [f"Difference in parts: ${b} - {a} = {b - a}$, which is ${diff}$ people, so one part is ${m}$.", f"Total: $({a} + {b}) \\cdot {m} = {(a + b) * m}$."],
             "treating the difference as one part.")


@reg(S, "basics")
def rp_undo_increase(r):
    pc = r.choice([20, 25, 50, 60, 100, 150])
    dec = F(pc * 100, 100 + pc)
    p = f"A price is increased by ${pc}\\%$. By what percent must the new price be decreased to return to the original price?"
    return QP(p, dec, [pc, F(pc, 2), 100 - pc if pc < 100 else 50, dec + 5, F(100, pc) * 10], "Use a starting price of \\$100.",
             "the percent decrease that undoes the increase.", "the decrease is a percent of the bigger, new price, so it is a smaller percent than the increase.",
             [f"Start at \\$100. After ${pc}\\%$ up: \\${100 + pc}.", f"To get back, drop \\${pc} out of \\${100 + pc}: $\\frac{{{pc}}}{{{100 + pc}}} = {ftex(dec)}\\%$."],
             "decreasing by the same " + str(pc) + "%, which overshoots.", ans_tex=f"{ftex(dec)}\\%")


@reg(S, "basics")
def rp_simple_interest(r):
    P = r.choice([500, 800, 1000, 1200, 1500, 2000, 2500])
    rate = r.choice([2, 3, 4, 5, 6, 8])
    yrs = r.randint(2, 6)
    I = F(P * rate * yrs, 100)
    p = f"\\${P} earns simple interest at ${rate}\\%$ per year. How many dollars of interest does it earn in ${yrs}$ years?"
    return Q(p, I, [P + I, F(P * rate, 100), I * 2, F(P * (rate + yrs), 100), I + rate], "Simple interest: principal $\\times$ rate $\\times$ years.",
             "the total interest.", "simple interest is the same amount each year: $I = Prt$.",
             [f"Each year: ${ftex(F(rate, 100))} \\cdot {P} = {ftex(F(P * rate, 100))}$ dollars.", f"Over ${yrs}$ years: ${ftex(F(P * rate, 100))} \\cdot {yrs} = {ftex(I)}$."],
             "giving the final balance (principal plus interest) instead of just the interest.")


@reg(S, "basics")
def rp_unit_price(r):
    q1, q2 = r.sample([6, 8, 10, 12, 15, 16, 20, 24], 2)
    u1 = F(r.randint(20, 60), 100)
    u2 = u1 + F(r.choice([-10, -5, 5, 10]), 100)
    if u2 <= 0:
        return None
    c1, c2 = q1 * u1, q2 * u2
    cheaper = min(u1, u2)
    n = max(q1, q2) * 2
    save = n * abs(u1 - u2)
    p = f"Pack A has ${q1}$ pens for \\${float(c1):.2f}; pack B has ${q2}$ pens for \\${float(c2):.2f}. How many cents per pen does the cheaper pack save?"
    return Q(p, abs(u1 - u2) * 100, [abs(c1 - c2) * 100, abs(u1 - u2) * 1000, abs(q1 - q2), cheaper * 100, abs(u1 - u2) * 50], "Find the cost of one pen in each pack.",
             "the difference in price per pen, in cents.", "compare unit prices: cost divided by the number of items.",
             [f"Pack A: $\\frac{{{float(c1):.2f}}}{{{q1}}} = {float(u1):.2f}$ dollars per pen.", f"Pack B: $\\frac{{{float(c2):.2f}}}{{{q2}}} = {float(u2):.2f}$ dollars per pen.", f"Difference: ${int(abs(u1 - u2) * 100)}$ cents."],
             "comparing the pack prices instead of the price per pen.")


@reg(S, "basics")
def rp_what_percent(r):
    A = r.choice([40, 50, 60, 80, 120, 150, 200, 250])
    pc = r.choice([5, 10, 15, 20, 30, 40, 60, 75, 120, 150])
    B = F(A * pc, 100)
    if B.denominator != 1:
        return None
    p = f"${B}$ is what percent of ${A}$?"
    return QP(p, pc, [F(A * 100, B), pc + 10, F(B, A), 100 - pc if pc < 100 else pc - 50, pc * 2], "Divide the part by the whole.",
             "the percent.", "percent $= \\frac{\\text{part}}{\\text{whole}} \\times 100$.",
             [f"$\\frac{{{B}}}{{{A}}} = {ftex(F(B, A))}$.", f"Times $100$: ${pc}\\%$."],
             "dividing the whole by the part.", ans_tex=f"{pc}\\%")


@reg(S, "basics")
def rp_inverse(r):
    x1 = r.choice([2, 3, 4, 5, 6, 8])
    y1 = r.choice([6, 9, 10, 12, 15, 18, 20])
    k = x1 * y1
    x2 = r.choice([x for x in [2, 3, 4, 5, 6, 9, 10, 12, 15] if x != x1])
    y2 = F(k, x2)
    p = f"$y$ varies inversely with $x$. When $x = {x1}$, $y = {y1}$. What is $y$ when $x = {x2}$?"
    return Q(p, y2, [F(y1 * x2, x1), y1 + x1 - x2, y2 + 1, F(x2, k), k], "Inverse variation means $xy$ stays the same.",
             "$y$ when $x = " + str(x2) + "$.", "inverse variation: $xy = k$, a constant.",
             [f"$k = {x1} \\cdot {y1} = {k}$.", f"$y = \\frac{{{k}}}{{{x2}}} = {ftex(y2)}$."],
             "using direct variation ($y$ grows with $x$).")


@reg(S, "basics")
def rp_square_variation(r):
    x1 = r.choice([2, 3, 4, 5])
    k = r.choice([1, 2, 3, 4, F(1, 2)])
    y1 = k * x1 * x1
    x2 = r.choice([x for x in [2, 3, 4, 6, 8, 10] if x != x1])
    y2 = k * x2 * x2
    p = f"The stopping distance $d$ of a car varies directly with the square of its speed $s$. At $s = {x1 * 10}$ mph, $d = {ftex(y1 * 10)}$ feet. What is $d$ at $s = {x2 * 10}$ mph?"
    return Q(p, y2 * 10, [y1 * 10 * x2 / x1, y2 * 10 * 2, y1 * 10 + (x2 - x1) * 10, y2 * 10 + 10, y1 * 10 * x2 * x2], "Compare the speeds: how many times faster?",
             "the stopping distance at the new speed.", "$d = ks^2$. If the speed is multiplied by some factor, the distance is multiplied by that factor squared.",
             [f"Speed ratio: $\\frac{{{x2 * 10}}}{{{x1 * 10}}} = {ftex(F(x2, x1))}$.", f"Distance ratio: $\\left({ftex(F(x2, x1))}\\right)^2 = {ftex(F(x2 * x2, x1 * x1))}$.", f"$d = {ftex(y1 * 10)} \\cdot {ftex(F(x2 * x2, x1 * x1))} = {ftex(y2 * 10)}$ feet."],
             "scaling the distance by the speed ratio instead of its square.")


@reg(S, "basics")
def rp_fraction_rest(r):
    a, b = r.sample([F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(1, 6), F(2, 5), F(1, 8)], 2)
    rest = 1 - a - b
    if rest <= 0:
        return None
    k = r.randint(5, 40)
    if (k / rest).denominator != 1:
        return None
    tot = k / rest
    p = f"Of the students in a school, ${ftex(a)}$ walk, ${ftex(b)}$ ride bikes, and the other ${k}$ take the bus. How many students are there?"
    return Q(p, tot, [k / (1 - a), k * 3, tot + k, tot / 2, k / rest + 2], "The bus riders are the fraction left over.",
             "the total number of students.", "the bus riders are $1 - " + ftex(a) + " - " + ftex(b) + "$ of all students.",
             [f"Leftover fraction: $1 - {ftex(a)} - {ftex(b)} = {ftex(rest)}$.", f"${ftex(rest)}$ of the total is ${k}$, so the total is $\\frac{{{k}}}{{{ftex(rest)}}} = {ftex(tot)}$."],
             "forgetting one of the fractions when finding the leftover part.")


@reg(S, "basics")
def rp_tip_split(r):
    bill = r.choice([40, 60, 80, 90, 100, 120, 150])
    tip = r.choice([15, 18, 20, 25])
    n = r.choice([2, 3, 4, 5, 6])
    each = F(bill * (100 + tip), 100 * n)
    p = f"A dinner bill is \\${bill}. The group adds a ${tip}\\%$ tip and splits the total evenly among ${n}$ people. How many dollars does each person pay?"
    show = lambda v: C(f"\\${float(v):.2f}", float(v))
    return Q(p, show(each), [show(F(bill, n)), show(each + 1), show(F(bill, n) + tip), show(F(bill * tip, 100 * n)), show(each * 2)], "Find the total with tip first.",
             "each person's share.", "the tip is a percent of the bill; add it, then divide by the number of people.",
             [f"Tip: ${ftex(F(tip, 100))} \\cdot {bill} = {ftex(F(bill * tip, 100))}$.", f"Total: ${ftex(F(bill * (100 + tip), 100))}$.", f"Each: $\\frac{{{ftex(F(bill * (100 + tip), 100))}}}{{{n}}} = {float(each):.2f}$."],
             "adding the tip percent as dollars.", ans_tex=f"\\${float(each):.2f}")


@reg(S, "challenge")
def rpc_alloys(r):
    a, b = r.sample(range(1, 6), 2)
    c, d = r.sample(range(1, 6), 2)
    fa, fb = F(a, a + b), F(c, c + d)
    mix = (fa + fb) / 2
    ratio = mix / (1 - mix)
    p = f"Alloy X is copper and zinc in the ratio ${a}:{b}$, and alloy Y is copper and zinc in the ratio ${c}:{d}$. Equal weights of X and Y are melted together. What is the ratio of copper to zinc in the mix, written as a single number (copper divided by zinc)?"
    return Q(p, ratio, [F(a + c, b + d), F(a * c, b * d), ratio + F(1, 2), 1 / ratio if ratio != 1 else 2, F(a, b) + F(c, d)], "Convert each ratio to a fraction of the whole.",
             "copper $\\div$ zinc in the mix.", "with equal weights, average the copper fractions, not the ratios.",
             [f"Copper fraction in X: ${ftex(fa)}$; in Y: ${ftex(fb)}$.", f"Equal weights: copper fraction in the mix $= \\frac{{{ftex(fa)} + {ftex(fb)}}}{{2}} = {ftex(mix)}$; zinc $= {ftex(1 - mix)}$.", f"Ratio: $\\frac{{{ftex(mix)}}}{{{ftex(1 - mix)}}} = {ftex(ratio)}$."],
             "adding the ratio parts directly ($" + f"{a + c}:{b + d}" + "$), which is wrong when the alloys' part sizes differ.")


@reg(S, "challenge")
def rpc_glasses(r):
    boys = r.choice([30, 40, 45, 50, 55, 60])
    pb, pg = r.sample([10, 20, 25, 30, 40, 50, 60], 2)
    tot = F(boys * pb + (100 - boys) * pg, 100)
    p = f"At a school, ${boys}\\%$ of students are boys. ${pb}\\%$ of the boys and ${pg}\\%$ of the girls wear glasses. What percent of all students wear glasses?"
    return QP(p, tot, [F(pb + pg, 2), pb + pg, tot + 5, F(pb * pg, 100), abs(pb - pg)], "Imagine 100 students.",
             "the overall percent with glasses.", "it's a weighted average: the bigger group counts more.",
             [f"Out of $100$ students: ${boys}$ boys and ${100 - boys}$ girls.", f"Boys with glasses: ${ftex(F(boys * pb, 100))}$; girls: ${ftex(F((100 - boys) * pg, 100))}$.", f"Total: ${ftex(tot)}$ of $100$, so ${ftex(tot)}\\%$."],
             "averaging the two percents equally.", ans_tex=f"{ftex(tot)}\\%")


@reg(S, "challenge")
def rpc_revenue(r):
    up = r.choice([10, 20, 25, 30, 40, 50])
    down = r.choice([10, 20, 25, 30, 40])
    rev = F((100 + up) * (100 - down), 100) - 100
    p = f"A theater raises ticket prices by ${up}\\%$, and as a result sells ${down}\\%$ fewer tickets. By what percent does its ticket revenue change? (Negative means a decrease.)"
    return QP(p, rev, [up - down, rev + 5, -rev if rev else 5, F(up * down, 100), up + down], "Revenue is price times tickets sold.",
             "the percent change in revenue.", "multiply the two factors: price $\\times$ quantity.",
             [f"New revenue $= {ftex(F(100 + up, 100))} \\times {ftex(F(100 - down, 100))} = {ftex(F((100 + up) * (100 - down), 10000))}$ of the old revenue.", f"Change: ${ftex(rev)}\\%$."],
             "adding and subtracting the percents, which ignores the cross term.", ans_tex=f"{ftex(rev)}\\%")


@reg(S, "challenge")
def rpc_add_same(r):
    a, b = r.sample(range(2, 12), 2)
    k = r.randint(2, 6)
    A, B = a * k, b * k
    x = r.randint(2, 20)
    g = math.gcd(A + x, B + x)
    c, d = (A + x) // g, (B + x) // g
    if (c, d) == (a, b):
        return None
    p = f"Two numbers are in the ratio ${a}:{b}$. When ${x}$ is added to each, the ratio becomes ${c}:{d}$. What is the smaller of the original numbers?"
    return Q(p, min(A, B), [max(A, B), min(A, B) + x, min(a, b), min(A, B) - x if min(A, B) > x else min(A, B) + 2 * x, a * b], "Call the numbers " + str(a) + "k and " + str(b) + "k.",
             "the smaller original number.", "write the numbers with one unknown $k$, then cross multiply the new ratio.",
             [f"Numbers: ${a}k$ and ${b}k$.", f"$\\frac{{{a}k + {x}}}{{{b}k + {x}}} = \\frac{{{c}}}{{{d}}}$, so ${d}({a}k + {x}) = {c}({b}k + {x})$.", f"${a * d - b * c}k = {c * x - d * x}$, so $k = {k}$.", f"Smaller: ${min(a, b)} \\cdot {k} = {min(A, B)}$."],
             "adding " + str(x) + " to the ratio numbers themselves.")


@reg(S, "challenge")
def rpc_chain_percent(r):
    p1 = r.choice([10, 20, 25, 50, 60])
    p2 = r.choice([10, 20, 25, 40, 50])
    res = F((100 + p1) * (100 - p2), 100)
    p = f"$A$ is ${p1}\\%$ more than $B$, and $B$ is ${p2}\\%$ less than $C$. $A$ is what percent of $C$?"
    return QP(p, res, [100 + p1 - p2, res + 10, F(100 * 100, res) if res else 1, 100 - p1 + p2, res - 5], "Pick $C = 100$.",
             "$A$ as a percent of $C$.", "choose a convenient value for $C$ and work through the chain.",
             [f"$C = 100$, so $B = 100 - {p2} = {100 - p2}$.", f"$A = {100 - p2} \\cdot {ftex(F(100 + p1, 100))} = {ftex(res)}$.", f"So $A$ is ${ftex(res)}\\%$ of $C$."],
             "adding and subtracting percents directly.", ans_tex=f"{ftex(res)}\\%")


@reg(S, "challenge")
def rpc_drain_replace(r):
    V = r.choice([10, 12, 15, 20, 24, 30])
    p1 = r.choice([20, 25, 30, 40, 50])
    p2 = r.choice([x for x in [40, 50, 60, 70, 75, 80] if x > p1])
    x = F(V * (p2 - p1), 100 - p1)
    p = f"A ${V}$ liter radiator is full of a ${p1}\\%$ antifreeze mixture. How many liters must be drained and replaced with pure antifreeze to make it ${p2}\\%$ antifreeze?"
    return Q(p, x, [F(V * (p2 - p1), 100), F(V * (p2 - p1), p2), x + 1, F(V * p2, 100), x / 2], "Track the amount of antifreeze.",
             "the amount to drain and replace, $x$.", "draining removes " + str(p1) + "% antifreeze; refilling adds 100% antifreeze. The volume stays the same.",
             [f"Start: ${ftex(F(V * p1, 100))}$ L of antifreeze.", f"After: ${ftex(F(V * p1, 100))} - {ftex(F(p1, 100))}x + x = {ftex(F(V * p2, 100))}$.", f"${ftex(F(100 - p1, 100))}x = {ftex(F(V * (p2 - p1), 100))}$, so $x = {ftex(x)}$ L."],
             "forgetting that the drained liquid already contained some antifreeze.")


@reg(S, "challenge")
def rpc_ratio_expr(r):
    a, b = r.sample(range(1, 9), 2)
    c1, c2, c3, c4 = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    val = F(c1 * a + c2 * b, c3 * a + c4 * b)
    p = f"If $\\dfrac{{x}}{{y}} = \\dfrac{{{a}}}{{{b}}}$, what is $\\dfrac{{{c1 if c1 > 1 else ''}x + {c2 if c2 > 1 else ''}y}}{{{c3 if c3 > 1 else ''}x + {c4 if c4 > 1 else ''}y}}$?"
    return Q(p, val, [F(c1 + c2, c3 + c4), F(c1 * a + c2, c3 * a + c4), 1 / val if val != 1 else 2, val + F(1, 2), F(a, b)], "Pick $x = " + str(a) + "$ and $y = " + str(b) + "$.",
             "the value of the expression.", "only the ratio matters, so choose numbers with that ratio.",
             [f"Let $x = {a}$, $y = {b}$.", f"Top: ${c1 * a} + {c2 * b} = {c1 * a + c2 * b}$. Bottom: ${c3 * a} + {c4 * b} = {c3 * a + c4 * b}$.", f"Value: ${ftex(val)}$."],
             "plugging in the ratio's numbers backwards ($x = " + str(b) + "$).")
