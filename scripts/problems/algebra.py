"""Algebra unit: original problems modeled on AMC 10/12 problem types."""
import math
from fractions import Fraction as F

from common import NAMES, Bank, C, explain, num, sqrt_form, simplify_sqrt, two_names, var, par
from algebra_more1 import MORE as M1
from algebra_more2 import MORE as M2
from algebra_more3 import MORE as M3

MORE = {**M1, **M2, **M3}

banks = []


def bank(skill_id):
    b = Bank(skill_id)
    banks.append(b)
    return b


def sgn(c):
    """' + 3' or ' - 3'."""
    return f" + {c}" if c >= 0 else f" - {abs(c)}"


# ---------------------------------------------------------------- linear equations and systems
b = bank("alg_linear")


def lin1(r):
    a, x = r.randint(2, 9), r.randint(-12, 15)
    c = r.randint(-20, 20)
    d = a * x + c
    p = f"If ${a}x{sgn(c)} = {d}$, what is the value of $x$?"
    sol = explain(
        "the value of $x$ that makes the equation true.",
        "undo the operations on $x$ in reverse order: first the added or subtracted number, then the multiplication.",
        [
            f"{'Subtract' if c >= 0 else 'Add'} ${abs(c)}$ {'from' if c >= 0 else 'to'} both sides: $${a}x = {d} {'-' if c >= 0 else '+'} {abs(c)} = {d - c}.$$",
            f"Divide both sides by ${a}$: $x = \\frac{{{d - c}}}{{{a}}} = {x}$.",
            f"Check: ${a} \\cdot ({x}){sgn(c)} = {a * x}{sgn(c)} = {d}$. It works.",
        ],
        f"$x = {x}$.",
        f"{'adding' if c >= 0 else 'subtracting'} ${abs(c)}$ instead, which moves the number the wrong way.",
    )
    return (p, x, [x + 1, x - 1, -x, (d + c) // a if a else x + 2, x + 2], ["Undo the constant first, then divide by the coefficient of $x$."], sol)


def lin2(r):
    x, y = r.randint(-6, 12), r.randint(-6, 12)
    a1, b1, a2, b2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(-5, -1)
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    t = r.choice(["x + y", "x - y", "xy"])
    val = {"x + y": x + y, "x - y": x - y, "xy": x * y}[t]
    p = f"If ${a1}x + {b1}y = {c1}$ and ${a2}x {'-' if b2 < 0 else '+'} {abs(b2)}y = {c2}$, what is ${t}$?"
    L = math.lcm(b1, abs(b2))
    m1, m2 = L // b1, L // abs(b2)
    sol = explain(
        f"the value of ${t}$, which needs both $x$ and $y$.",
        "elimination: scale the equations so the $y$ terms are opposites, then add to cancel $y$.",
        [
            f"Multiply the first equation by ${m1}$ and the second by ${m2}$: $${a1 * m1}x + {b1 * m1}y = {c1 * m1}, \\qquad {a2 * m2}x - {abs(b2) * m2}y = {c2 * m2}.$$",
            f"Add them; the $y$ terms cancel: ${a1 * m1 + a2 * m2}x = {c1 * m1 + c2 * m2}$, so $x = {x}$.",
            f"Put $x = {x}$ into the first equation: ${a1} \\cdot ({x}) + {b1}y = {c1}$, so ${b1}y = {c1 - a1 * x}$ and $y = {y}$.",
            f"Then ${t} = {val}$.",
        ],
        f"${t} = {val}$.",
        "a sign slip when the second equation has a minus. Check your $x$ and $y$ in both original equations.",
    )
    return (p, val, [x + y + 1, x - y, y - x, x * y, val + 2, val - 2], ["Eliminate one variable by scaling and adding the equations."], sol)


def lin3(r):
    n1, n2 = two_names(r)
    u, w = var(n1), var(n2)
    a = r.randint(8, 30)
    diff = r.randint(2, 12)
    total = 2 * a + diff
    p = f"{n1} and {n2} have {total} stickers together. {n1} has {diff} more stickers than {n2}. How many stickers does {n2} have?"
    sol = explain(
        f"{n2}'s number of stickers. Let ${w}$ be {n2}'s stickers and ${u}$ be {n1}'s.",
        "turn each sentence into an equation, then substitute one into the other.",
        [
            f"Together: ${u} + {w} = {total}$. Difference: ${u} = {w} + {diff}$.",
            f"Substitute: $({w} + {diff}) + {w} = {total}$, so $2{w} + {diff} = {total}$.",
            f"$2{w} = {total - diff}$, so ${w} = {a}$. (And ${u} = {a + diff}$; check: ${a} + {a + diff} = {total}$.)",
        ],
        f"{n2} has ${a}$ stickers.",
        f"splitting ${total}$ in half (${total // 2}$) and ignoring the difference, or answering with {n1}'s count, ${a + diff}$.",
    )
    return (p, a, [a + diff, total // 2, a + 1, a - 1, diff], [f"Let {n2} have ${w}$ stickers. Then {n1} has ${w} + {diff}$."], sol)


def lin4(r):
    pa, pc = r.randint(8, 15), r.randint(3, 7)
    na, nc = r.randint(10, 60), r.randint(10, 60)
    n = na + nc
    rev = pa * na + pc * nc
    p = (f"A school play sold {n} tickets for a total of \\${rev}. Adult tickets cost \\${pa} and student tickets cost \\${pc}. "
         f"How many adult tickets were sold?")
    sol = explain(
        "the number of adult tickets. Let $a$ be adult tickets and $s$ be student tickets.",
        "write one equation for the number of tickets and one for the money, then substitute.",
        [
            f"Tickets: $a + s = {n}$, so $s = {n} - a$.",
            f"Money: ${pa}a + {pc}s = {rev}$.",
            f"Substitute: ${pa}a + {pc}({n} - a) = {rev}$, so ${pa}a + {pc * n} - {pc}a = {rev}$.",
            f"Simplify: ${pa - pc}a = {rev - pc * n}$, so $a = {na}$. (Check: ${pa} \\cdot {na} + {pc} \\cdot {nc} = {rev}$.)",
        ],
        f"${na}$ adult tickets.",
        f"answering with the student tickets (${nc}$).",
    )
    return (p, na, [nc, na + 2, na - 2, n // 2, abs(na - nc) + 1], ["Let $a$ be adult tickets and $s$ student tickets. Write one equation for tickets and one for money."], sol)


def linc1(r):
    x, y, z = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)
    s1, s2, s3 = x + y, y + z, x + z
    tot = (s1 + s2 + s3) // 2
    p = f"Real numbers $x$, $y$, $z$ satisfy $x + y = {s1}$, $y + z = {s2}$, and $z + x = {s3}$. What is $xyz$?"
    sol = explain(
        "the product $xyz$, so we need each of $x$, $y$, $z$.",
        "add all three equations: each variable appears exactly twice. That gives $x + y + z$, and then each variable falls out by subtraction.",
        [
            f"Add: $2(x + y + z) = {s1} + {s2} + {s3} = {s1 + s2 + s3}$, so $x + y + z = {tot}$.",
            f"$z = (x + y + z) - (x + y) = {tot} - {s1} = {z}$.",
            f"$x = (x + y + z) - (y + z) = {tot} - {s2} = {x}$.",
            f"$y = (x + y + z) - (z + x) = {tot} - {s3} = {y}$.",
            f"$xyz = {x} \\cdot {y} \\cdot {z} = {x * y * z}$.",
        ],
        f"$xyz = {x * y * z}$.",
        f"forgetting to divide by $2$, which gives $x + y + z = {s1 + s2 + s3}$.",
    )
    return (p, x * y * z, [tot, x * y + z, x + y + z, x * y * z + tot, (x + 1) * y * z], ["Add all three equations to find $x + y + z$.", "Subtract each equation from $x + y + z$."], sol)


def linc2(r):
    n1, n2 = two_names(r)
    now_old = r.randint(30, 50)
    now_young = r.randint(5, 15)
    k = r.randint(2, 4)
    num_ = now_old - k * now_young
    den = k - 1
    if num_ <= 0 or num_ % den:
        return None
    t = num_ // den
    if t > 40:
        return None
    p = f"{n1} is {now_old} years old and {n2} is {now_young} years old. In how many years will {n1} be exactly {k} times as old as {n2}?"
    sol = explain(
        f"the number of years $t$ until {n1}'s age is {k} times {n2}'s.",
        "both people age by the same amount, so add $t$ to both ages.",
        [
            f"In $t$ years: {n1} is ${now_old} + t$ and {n2} is ${now_young} + t$.",
            f"Set up the condition: ${now_old} + t = {k}({now_young} + t) = {k * now_young} + {k}t$.",
            f"Collect $t$ terms: ${now_old} - {k * now_young} = {k}t - t$, so ${num_} = {den}t$ and $t = {t}$.",
            f"Check: in ${t}$ years they are ${now_old + t}$ and ${now_young + t}$, and ${now_old + t} = {k} \\cdot {now_young + t}$.",
        ],
        f"${t}$ years.",
        f"adding $t$ to only one age, or forgetting to multiply the whole $({now_young} + t)$ by ${k}$.",
    )
    return (p, t, [t + 1, t - 1, t + k, now_old - now_young, 2 * t], [f"After $t$ years, the ages are ${now_old} + t$ and ${now_young} + t$."], sol)


def linc3(r):
    q, d = r.randint(4, 25), r.randint(4, 25)
    total_c = q + d
    val = 25 * q + 10 * d
    extra = r.randint(2, 6)
    p = (f"A jar holds {total_c} coins, all dimes and quarters, worth \\${val / 100:.2f}. If {extra} more quarters were added, "
         f"what fraction of the coins would be quarters?")
    ans = F(q + extra, total_c + extra)
    sol = explain(
        f"the fraction of quarters after adding ${extra}$ more. First find how many quarters there are now. Let $q$ be quarters and $d$ be dimes.",
        "two equations: one counts coins, one counts value in cents.",
        [
            f"Count: $q + d = {total_c}$. Value: $25q + 10d = {val}$ cents.",
            f"Multiply the count by $10$: $10q + 10d = {10 * total_c}$. Subtract from the value equation: $15q = {val - 10 * total_c}$, so $q = {q}$.",
            f"After adding ${extra}$ quarters: ${q + extra}$ quarters out of ${total_c + extra}$ coins.",
            f"Fraction: $\\frac{{{q + extra}}}{{{total_c + extra}}} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"adding the quarters to the top but forgetting that the total number of coins also grows by ${extra}$.",
    )
    return (p, ans, [F(q, total_c), F(d, total_c + extra), F(q + extra, total_c), F(q, total_c + extra), F(d + extra, total_c + extra)],
            ["Find the number of quarters first using value: $25q + 10d$ cents."], sol)


b.fill_unique("basics", [lin1, lin2, lin3, lin4] + MORE[b.skill_id]["basics"], 101)
b.fill_unique("challenge", [linc1, linc2, linc3] + MORE[b.skill_id]["challenge"], 102)


# ---------------------------------------------------------------- rates, work and mixtures
b = bank("alg_rates")


def rate1(r):
    n = r.choice(NAMES)
    v1, v2 = r.choice([(30, 60), (40, 60), (20, 30), (45, 90), (36, 45), (40, 120), (60, 90)])
    d = r.choice([60, 90, 120, 180, 360])
    if (d / v1) % 0.25 or (d / v2) % 0.25:
        return None
    t1, t2 = F(d, v1), F(d, v2)
    avg = F(2 * d) / (t1 + t2)
    p = (f"{n} drives {d} miles to a lake at {v1} miles per hour and returns along the same road at {v2} miles per hour. "
         f"What is the average speed for the whole trip, in miles per hour?")
    sol = explain(
        "the average speed for the round trip.",
        "average speed $=$ total distance $\\div$ total time. It is not the average of the two speeds, because more time is spent at the slower speed.",
        [
            f"Going: $\\frac{{{d}}}{{{v1}}} = {num(t1).tex}$ hours. Returning: $\\frac{{{d}}}{{{v2}}} = {num(t2).tex}$ hours.",
            f"Total distance: $2 \\cdot {d} = {2 * d}$ miles. Total time: ${num(t1).tex} + {num(t2).tex} = {num(t1 + t2).tex}$ hours.",
            f"Average speed: $\\frac{{{2 * d}}}{{{num(t1 + t2).tex}}} = {num(avg).tex}$ miles per hour.",
        ],
        f"${num(avg).tex}$ mph.",
        f"averaging the speeds to get ${num(F(v1 + v2, 2)).tex}$. That overweights the faster leg.",
    )
    return (p, avg, [F(v1 + v2, 2), v1, v2, avg + 2, avg - 3], ["Average speed is total distance divided by total time, not the average of the speeds."], sol)


def rate2(r):
    a, b_ = r.choice([(3, 6), (4, 12), (6, 12), (5, 20), (10, 15), (12, 24), (6, 3), (8, 24), (9, 18), (20, 30)])
    n1, n2 = two_names(r)
    t = F(a * b_, a + b_)
    rate = F(1, a) + F(1, b_)
    p = (f"{n1} can paint a fence in {a} hours and {n2} can paint the same fence in {b_} hours. Working together at these rates, "
         f"how many hours will it take them to paint the fence?")
    sol = explain(
        "the time for both working together.",
        "work with rates. Someone who finishes in $h$ hours paints $\\frac{1}{h}$ of the fence each hour, and rates of people working together add.",
        [
            f"{n1}'s rate: $\\frac{{1}}{{{a}}}$ fence per hour. {n2}'s rate: $\\frac{{1}}{{{b_}}}$ fence per hour.",
            f"Together: $\\frac{{1}}{{{a}}} + \\frac{{1}}{{{b_}}} = {num(rate).tex}$ fence per hour.",
            f"Time $= \\frac{{1 \\text{{ fence}}}}{{\\text{{rate}}}} = \\frac{{1}}{{{num(rate).tex}}} = {num(t).tex}$ hours.",
        ],
        f"${num(t).tex}$ hours.",
        f"averaging or adding the times. Together they must be faster than either alone, so the answer is less than ${min(a, b_)}$.",
    )
    return (p, t, [F(a + b_, 2), a + b_, min(a, b_), F(a * b_, a + b_ + 1), abs(a - b_)], ["Add the rates: each person paints a fraction of the fence per hour."], sol)


def rate3(r):
    v1, p1, p2, target = r.choice([(10, 20, 50, 30), (20, 10, 40, 20), (12, 25, 75, 50), (30, 10, 60, 30),
                                    (8, 15, 45, 25), (15, 20, 80, 40), (40, 5, 35, 15), (18, 30, 90, 50)])
    x = F(v1 * (target - p1), p2 - target)
    if x.denominator != 1:
        return None
    sub = r.choice(["salt", "juice", "acid"])
    p = (f"A chemist has {v1} liters of a {p1}\\% {sub} solution. How many liters of a {p2}\\% {sub} solution must be added "
         f"to make a {target}\\% {sub} solution?")
    sol = explain(
        f"how many liters $x$ of the stronger solution to add.",
        f"track the pure {sub}. The amount of pure {sub} before mixing equals the amount after.",
        [
            f"Pure {sub} now: ${p1}\\%$ of ${v1}$ liters $= {num(F(p1 * v1, 100)).tex}$ liters.",
            f"Pure {sub} added: ${p2}\\%$ of $x$, which is ${num(F(p2, 100)).tex}x$.",
            f"After mixing there are ${v1} + x$ liters at ${target}\\%$, so ${num(F(p1 * v1, 100)).tex} + {num(F(p2, 100)).tex}x = {num(F(target, 100)).tex}({v1} + x)$.",
            f"Multiply by $100$: ${p1 * v1} + {p2}x = {target * v1} + {target}x$, so ${p2 - target}x = {target * v1 - p1 * v1}$ and $x = {x}$.",
        ],
        f"${x}$ liters.",
        "averaging the percents, or forgetting that the total volume grows when you add solution.",
    )
    return (p, x, [x + 2, x - 1, v1, 2 * x, F(v1 * target, p2)], ["Track the amount of pure substance before and after mixing."], sol)


def rate4(r):
    m, items, mins = r.randint(3, 8), r.randint(2, 6), r.randint(3, 9)
    k_m, k_t = r.randint(2, 5), r.randint(2, 6)
    ans = items * k_m * k_t
    p = (f"If {m} machines make {items} gadgets in {mins} minutes, how many gadgets do {m * k_m} machines make in {mins * k_t} minutes, "
         f"working at the same rate?")
    sol = explain(
        "the output when both the number of machines and the time change.",
        "output is proportional to the number of machines and also to the time. Scale by each factor.",
        [
            f"Machines go from ${m}$ to ${m * k_m}$: that is ${k_m}$ times as many, so ${k_m}$ times the output.",
            f"Minutes go from ${mins}$ to ${mins * k_t}$: that is ${k_t}$ times as long, so ${k_t}$ times the output again.",
            f"Output: ${items} \\cdot {k_m} \\cdot {k_t} = {ans}$ gadgets.",
        ],
        f"${ans}$ gadgets.",
        "scaling by only one of the two changes.",
    )
    return (p, ans, [items * k_m, items * k_t, ans + items, ans // 2 if ans % 2 == 0 else ans + 1, items * (k_m + k_t)], ["Output is proportional to both the number of machines and the time."], sol)


def ratec1(r):
    n1, n2 = two_names(r)
    v1, v2 = r.randint(3, 6), r.randint(7, 12)
    head = r.randint(1, 3)
    t = F(v1 * head, v2 - v1)
    if t.denominator not in (1, 2, 3, 4, 6):
        return None
    minutes = t * 60
    if minutes.denominator != 1:
        return None
    m = int(minutes)
    p = (f"{n1} leaves home walking at {v1} miles per hour. {head} hour{'s' if head > 1 else ''} later, {n2} leaves the same home "
         f"on a bike riding at {v2} miles per hour along the same path. How many minutes after leaving does {n2} catch up to {n1}?")
    sol = explain(
        f"how long {n2} rides before reaching {n1}.",
        "when one person chases another in the same direction, the gap shrinks at the difference of their speeds.",
        [
            f"In the first ${head}$ hour{'s' if head > 1 else ''}, {n1} walks ${v1} \\cdot {head} = {v1 * head}$ miles. That is the head start.",
            f"Once {n2} starts, the gap shrinks by ${v2} - {v1} = {v2 - v1}$ miles every hour.",
            f"Time to close the gap: $\\frac{{{v1 * head}}}{{{v2 - v1}}} = {num(t).tex}$ hours $= {num(t).tex} \\cdot 60 = {m}$ minutes.",
        ],
        f"${m}$ minutes.",
        "adding the speeds. That would be right if they were moving toward each other.",
    )
    return (p, m, [m + 10, m - 10 if m > 10 else m + 20, head * 60, int(F(v1 * head * 60, v2)), m + 30],
            [f"When {n2} starts, {n1} is ${v1 * head}$ miles ahead.", "The gap closes at the difference of the speeds."], sol)


def ratec2(r):
    a, b_, c = r.choice([(4, 6, 12), (3, 6, 4), (6, 9, 18), (5, 10, 15), (4, 12, 8), (8, 12, 24), (10, 15, 20), (6, 8, 12)])
    rate = F(1, a) + F(1, b_) - F(1, c)
    if rate <= 0:
        return None
    t = 1 / rate
    L = math.lcm(a, b_, c)
    p = (f"Pipe A fills a tank in {a} hours and pipe B fills it in {b_} hours. A drain empties the full tank in {c} hours. "
         f"If all three are open, starting with an empty tank, how many hours does it take to fill the tank?")
    sol = explain(
        "the time to fill the tank with two pipes filling and one drain emptying.",
        "rates add, and the drain's rate counts as negative.",
        [
            f"Rates in tanks per hour: A is $\\frac{{1}}{{{a}}}$, B is $\\frac{{1}}{{{b_}}}$, the drain is $-\\frac{{1}}{{{c}}}$.",
            f"Over a common denominator ${L}$: $\\frac{{{L // a}}}{{{L}}} + \\frac{{{L // b_}}}{{{L}}} - \\frac{{{L // c}}}{{{L}}} = \\frac{{{L // a + L // b_ - L // c}}}{{{L}}} = {num(rate).tex}$ tank per hour.",
            f"Time $= \\frac{{1}}{{{num(rate).tex}}} = {num(t).tex}$ hours.",
        ],
        f"${num(t).tex}$ hours.",
        "adding the drain's rate instead of subtracting it.",
    )
    return (p, t, [1 / (F(1, a) + F(1, b_)), t + 1, 1 / (F(1, a) + F(1, b_) + F(1, c)), 2 * t, t + 2], ["Rates add, and the drain's rate counts as negative."], sol)


def ratec3(r):
    boat, cur = r.randint(8, 16), r.randint(1, 4)
    d = (boat - cur) * (boat + cur) * r.choice([1, 2]) // math.gcd(boat - cur, boat + cur)
    t_up, t_down = F(d, boat - cur), F(d, boat + cur)
    if t_up.denominator != 1 or t_down.denominator != 1 or t_up > 30:
        return None
    p = (f"A boat travels {d} km downstream in {t_down} hours and returns the same {d} km upstream in {t_up} hours. "
         f"What is the speed of the current, in km per hour?")
    sol = explain(
        "the speed $c$ of the current. Let $b$ be the boat's speed in still water.",
        "going downstream the current helps ($b + c$); going upstream it hurts ($b - c$).",
        [
            f"Downstream speed: $\\frac{{{d}}}{{{t_down}}} = {boat + cur}$, so $b + c = {boat + cur}$.",
            f"Upstream speed: $\\frac{{{d}}}{{{t_up}}} = {boat - cur}$, so $b - c = {boat - cur}$.",
            f"Subtract the equations: $2c = {boat + cur} - {boat - cur} = {2 * cur}$, so $c = {cur}$. (And $b = {boat}$.)",
        ],
        f"${cur}$ km per hour.",
        f"answering with the boat's speed (${boat}$) instead of the current's.",
    )
    return (p, cur, [boat, cur + 1, 2 * cur, boat - cur, F(boat + cur, 2)], ["Downstream speed is boat plus current. Upstream speed is boat minus current."], sol)


b.fill_unique("basics", [rate1, rate2, rate3, rate4] + MORE[b.skill_id]["basics"], 201)
b.fill_unique("challenge", [ratec1, ratec2, ratec3] + MORE[b.skill_id]["challenge"], 202)


# ---------------------------------------------------------------- ratios, percents, proportions
b = bank("alg_ratios")


def rp1(r):
    a, bb = r.randint(2, 7), r.randint(2, 7)
    if math.gcd(a, bb) != 1 or a == bb:
        return None
    k = r.randint(3, 12)
    total = (a + bb) * k
    thing = r.choice(["red and blue marbles", "boys and girls in a club", "cats and dogs at a shelter", "fiction and nonfiction books"])
    first, second = thing.split(" and ")
    second = second.split(" ")[0]
    p = f"The ratio of {thing} is ${a}:{bb}$. There are {total} in all. How many are {first}?"
    sol = explain(
        f"the number of {first}.",
        f"a ratio ${a}:{bb}$ splits the total into ${a} + {bb} = {a + bb}$ equal parts.",
        [
            f"Each part is $\\frac{{{total}}}{{{a + bb}}} = {k}$.",
            f"{first.capitalize()} get ${a}$ parts: ${a} \\cdot {k} = {a * k}$. ({second.capitalize()} get ${bb} \\cdot {k} = {bb * k}$; check: ${a * k} + {bb * k} = {total}$.)",
        ],
        f"${a * k}$.",
        f"dividing ${total}$ by ${a}$ or by ${bb}$ instead of by the total number of parts, ${a + bb}$.",
    )
    return (p, a * k, [bb * k, total // 2 if total % 2 == 0 else a * k + 1, a * k + k, a * (k + 1) - 1, total - a], [f"Split {total} into ${a + bb}$ equal parts."], sol)


def rp2(r):
    up, down = r.choice([(20, 20), (25, 20), (10, 10), (50, 50), (20, 25), (30, 20), (40, 25), (10, 20)])
    res = F(100 + up, 100) * F(100 - down, 100)
    change = (res - 1) * 100
    mid = 100 + up
    p = (f"A store raises the price of a jacket by {up}\\%, then later lowers the new price by {down}\\%. "
         f"By what percent did the final price change from the original? (Negative means a decrease.)")
    sol = explain(
        "the overall percent change.",
        "the second change is a percent of the new price. Use a starting price of $\\$100$ to make the percents easy to read.",
        [
            f"Start at $\\$100$. After the ${up}\\%$ raise: $\\${mid}$.",
            f"The ${down}\\%$ cut removes ${down}\\%$ of $\\${mid}$, which is $\\${num(F(mid * down, 100)).tex}$. New price: $\\${num(res * 100).tex}$.",
            f"Change from $\\$100$: ${num(res * 100).tex} - 100 = {num(change).tex}$, so the price changed by ${num(change).tex}\\%$.",
        ],
        f"${num(change).tex}\\%$.",
        f"adding the percents: ${up} - {down} = {up - down}$. The cut applies to a bigger number, so it removes more.",
    )
    return (p, change, [up - down, change + 2, -change if change else 5, F(up * down, 100), -(up + down) // 2], ["Multiply the two percent changes as factors: $(1 + \\text{up})(1 - \\text{down})$."], sol)


def rp3(r):
    pct = r.choice([12, 15, 20, 25, 30, 35, 40, 60, 75])
    part = r.randint(3, 30) * (100 // math.gcd(100, pct))
    if part * 100 % pct:
        return None
    whole = part * 100 // pct
    p = f"{part} is {pct}\\% of what number?"
    sol = explain(
        f"the number $N$ whose ${pct}\\%$ is ${part}$.",
        f"'${pct}\\%$ of $N$' means $\\frac{{{pct}}}{{100}} \\cdot N$.",
        [
            f"Write the equation: $\\frac{{{pct}}}{{100}} \\cdot N = {part}$.",
            f"Multiply both sides by $\\frac{{100}}{{{pct}}}$: $N = {part} \\cdot \\frac{{100}}{{{pct}}} = {whole}$.",
            f"Check: ${pct}\\%$ of ${whole}$ is ${num(F(pct * whole, 100)).tex}$.",
        ],
        f"${whole}$.",
        f"finding ${pct}\\%$ of ${part}$ instead, which goes the wrong direction.",
    )
    return (p, whole, [part * pct // 100 if part * pct % 100 == 0 else whole + 10, whole + part, whole // 2, part + pct, whole * 2], ["Write $\\frac{" + str(pct) + "}{100} \\cdot N = " + str(part) + "$."], sol)


def rp4(r):
    a, bb, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    d = r.randint(2, 6)
    ans = F(a * c, bb * d)
    p = f"If $x : y = {a} : {bb}$ and $y : z = {c} : {d}$, what is $\\dfrac{{x}}{{z}}$?"
    sol = explain(
        "the ratio of $x$ to $z$, linking two ratios that share $y$.",
        "multiply the fractions: $\\frac{x}{z} = \\frac{x}{y} \\cdot \\frac{y}{z}$, because the $y$ cancels.",
        [
            f"$\\frac{{x}}{{y}} = \\frac{{{a}}}{{{bb}}}$ and $\\frac{{y}}{{z}} = \\frac{{{c}}}{{{d}}}$.",
            f"$\\frac{{x}}{{z}} = \\frac{{{a}}}{{{bb}}} \\cdot \\frac{{{c}}}{{{d}}} = \\frac{{{a * c}}}{{{bb * d}}} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"using $\\frac{{{a}}}{{{d}}}$, the first and last numbers. The two ratios use different scales for $y$.",
    )
    return (p, ans, [F(a, d), F(a * d, bb * c), F(a + c, bb + d), F(bb * d, a * c), F(a, bb)], ["Multiply $\\frac{x}{y}$ by $\\frac{y}{z}$."], sol)


def rpc1(r):
    a, bb = r.randint(2, 5), r.randint(2, 5)
    if a == bb or math.gcd(a, bb) != 1:
        return None
    k = r.randint(3, 10)
    add = r.randint(2, 12)
    na, nb = a * k + add, bb * k
    g = math.gcd(na, nb)
    c, d = na // g, nb // g
    if c > 20 or d > 20:
        return None
    p = (f"A bag holds red and green candies in the ratio ${a}:{bb}$. After {add} more red candies are added, the ratio becomes ${c}:{d}$. "
         f"How many green candies are in the bag?")
    sol = explain(
        "the number of green candies, which does not change.",
        f"a ratio ${a}:{bb}$ means there are ${a}k$ red and ${bb}k$ green for some whole number $k$.",
        [
            f"After adding: $\\frac{{{a}k + {add}}}{{{bb}k}} = \\frac{{{c}}}{{{d}}}$.",
            f"Cross multiply: ${d}({a}k + {add}) = {c} \\cdot {bb}k$, so ${d * a}k + {d * add} = {c * bb}k$.",
            f"${d * add} = {c * bb - d * a}k$, so $k = {k}$.",
            f"Green candies: ${bb}k = {bb * k}$. (Check: red goes from ${a * k}$ to ${na}$, and ${na}:{nb} = {c}:{d}$.)",
        ],
        f"${bb * k}$ green candies.",
        "forgetting that only the red count changes; the green count stays the same.",
    )
    return (p, bb * k, [a * k, bb * k + add, bb * (k + 1), (a + bb) * k, nb + 1], [f"Let there be ${a}k$ red and ${bb}k$ green candies."], sol)


def rpc2(r):
    p1, p2 = r.choice([(20, 25), (10, 20), (30, 10), (25, 40), (15, 20), (50, 20), (40, 50), (20, 30)])
    if (100 - p1) * (100 - p2) % 100:
        return None
    paid = (100 - p1) * (100 - p2) // 100
    single = 100 - paid
    p = (f"A sale takes {p1}\\% off the price, and a coupon takes another {p2}\\% off the sale price. "
         f"What single percent discount gives the same final price?")
    sol = explain(
        "one discount that matches the two discounts in a row.",
        "find what percent of the original price is actually paid. The discount is $100\\%$ minus that.",
        [
            f"After the ${p1}\\%$ sale, you pay ${100 - p1}\\%$ of the price.",
            f"The coupon takes ${p2}\\%$ off that, so you pay ${100 - p2}\\%$ of ${100 - p1}\\%$: $\\frac{{{100 - p2}}}{{100}} \\cdot {100 - p1}\\% = {paid}\\%$.",
            f"Single discount: $100\\% - {paid}\\% = {single}\\%$.",
        ],
        f"${single}\\%$.",
        f"adding the discounts to get ${p1 + p2}\\%$. The coupon applies to the already reduced price.",
    )
    return (p, single, [p1 + p2, single - 2, single + 3, max(p1, p2) + 5, (p1 + p2) // 2], ["Find what fraction of the original price is paid."], sol)


def rpc3(r):
    n = r.choice([200, 400, 500, 800, 1000, 1200])
    g = r.choice([10, 20, 25, 50])
    left = r.choice([F(1, 4), F(1, 5), F(1, 3), F(2, 5)])
    grown = F(n * (100 + g), 100)
    after = grown * (1 - left)
    if after.denominator != 1:
        return None
    p = (f"A town has {n} residents. The population grows by {g}\\% one year, and the next year ${num(left).tex}$ of the residents move away. "
         f"How many residents are left?")
    sol = explain(
        "the population after both changes.",
        "apply the changes one at a time, in order. Each change acts on the current population.",
        [
            f"Growth of ${g}\\%$: ${n} \\cdot {num(F(100 + g, 100)).tex} = {num(grown).tex}$ residents.",
            f"${num(left).tex}$ move away, so ${num(1 - left).tex}$ stay: ${num(grown).tex} \\cdot {num(1 - left).tex} = {num(after).tex}$.",
        ],
        f"${num(after).tex}$ residents.",
        f"taking ${num(left).tex}$ of the original ${n}$ instead of the grown population.",
    )
    return (p, after, [grown, n * (1 - left), after + n // 10, n, after - 20], ["Apply the changes one at a time, in order."], sol)


b.fill_unique("basics", [rp1, rp2, rp3, rp4] + MORE[b.skill_id]["basics"], 301)
b.fill_unique("challenge", [rpc1, rpc2, rpc3] + MORE[b.skill_id]["challenge"], 302)


# ---------------------------------------------------------------- exponents and radicals
b = bank("alg_exponents")


def ex1(r):
    base = r.choice([2, 3, 5])
    a, bb, c = r.randint(2, 9), r.randint(2, 9), r.randint(1, 8)
    e = a + bb - c
    p = f"Write $\\dfrac{{{base}^{{{a}}} \\cdot {base}^{{{bb}}}}}{{{base}^{{{c}}}}}$ as a power of ${base}$. What is the exponent?"
    sol = explain(
        f"the single exponent $n$ with the expression equal to ${base}^n$.",
        "with the same base, multiplying adds exponents and dividing subtracts them: $b^m \\cdot b^n = b^{m+n}$ and $\\frac{b^m}{b^n} = b^{m-n}$.",
        [
            f"Top: ${base}^{{{a}}} \\cdot {base}^{{{bb}}} = {base}^{{{a} + {bb}}} = {base}^{{{a + bb}}}$.",
            f"Divide: $\\frac{{{base}^{{{a + bb}}}}}{{{base}^{{{c}}}}} = {base}^{{{a + bb} - {c}}} = {base}^{{{e}}}$.",
        ],
        f"the exponent is ${e}$.",
        f"multiplying exponents (${a} \\cdot {bb}$). Exponents multiply only for a power of a power, like $({base}^{{{a}}})^{{{bb}}}$.",
    )
    return (p, e, [a * bb - c, a + bb + c, a * bb // c if c else e + 1, e + 1, e - 1], ["Multiplying powers adds exponents; dividing subtracts them."], sol)


def ex2(r):
    n = r.randint(2, 30)
    k = r.choice([2, 3, 5, 6, 7])
    sq = n * n * k
    a, bb = simplify_sqrt(sq)
    p = f"Simplify $\\sqrt{{{sq}}}$."
    sol = explain(
        f"$\\sqrt{{{sq}}}$ in simplest form $a\\sqrt{{b}}$, where $b$ has no square factor.",
        "pull out the largest perfect square: $\\sqrt{m^2 \\cdot k} = m\\sqrt{k}$.",
        [
            f"Factor out the biggest perfect square: ${sq} = {n * n} \\cdot {k}$, and ${n * n} = {n}^2$.",
            f"$\\sqrt{{{sq}}} = \\sqrt{{{n * n}}} \\cdot \\sqrt{{{k}}} = {n}\\sqrt{{{k}}}$.",
            f"${k}$ has no square factor bigger than $1$, so this is simplest form.",
        ],
        f"${n}\\sqrt{{{k}}}$.",
        "pulling out a smaller square and stopping too early, which leaves a square factor under the root.",
    )
    return (p, sqrt_form(a, bb), [sqrt_form(n, k * 2) if k * 2 not in (4, 9) else sqrt_form(n + 1, k), sqrt_form(n * 2, k),
                                   sqrt_form(n - 1 if n > 2 else n + 2, k), C(str(n * k), n * k), C(f"{n}{k}", n * 10 + k)],
            ["Find the largest perfect square that divides the number."], sol)


def ex3(r):
    base = r.choice([2, 3])
    x = r.randint(2, 8)
    m = r.randint(2, 4)
    big = base ** m
    k = r.randint(1, 4)
    p = f"If ${big}^{{x}} = {base}^{{{m * x + k}}} \\div {base}^{{{k}}}$, what is $x$?"
    sol = explain(
        "the exponent $x$.",
        "write both sides as powers of the same base, then set the exponents equal.",
        [
            f"Left: ${big} = {base}^{{{m}}}$, so ${big}^x = ({base}^{{{m}}})^x = {base}^{{{m}x}}$.",
            f"Right: ${base}^{{{m * x + k}}} \\div {base}^{{{k}}} = {base}^{{{m * x + k} - {k}}} = {base}^{{{m * x}}}$.",
            f"Same base, so ${m}x = {m * x}$ and $x = {x}$.",
        ],
        f"$x = {x}$.",
        f"setting $x = {m * x}$ without rewriting ${big}$ as a power of ${base}$ first.",
    )
    return (p, x, [m * x, x + 1, x + m, x - 1, m * x + k], [f"Write ${big}$ as a power of ${base}$."], sol)


def ex4(r):
    a = r.choice([4, 8, 9, 16, 25, 27, 32, 64, 81, 125])
    roots = {4: (2, 2), 8: (2, 3), 9: (3, 2), 16: (2, 4), 25: (5, 2), 27: (3, 3), 32: (2, 5), 64: (2, 6), 81: (3, 4), 125: (5, 3)}
    base, e = roots[a]
    q = r.choice([d for d in (2, 3, 4, 5, 6) if e % d == 0])
    pw = r.randint(1, 3)
    if math.gcd(pw, q) != 1:
        return None
    rt = base ** (e // q)
    val = rt ** pw
    neg = r.random() < 0.4
    ans = F(1, val) if neg else val
    expo = f"-\\frac{{{pw}}}{{{q}}}" if neg else f"\\frac{{{pw}}}{{{q}}}"
    p = f"What is ${a}^{{{expo}}}$?"
    steps = [
        f"The bottom of the fraction is the root: $\\sqrt[{q}]{{{a}}} = {rt}$, because ${rt}^{{{q}}} = {a}$.",
        f"The top is the power: ${rt}^{{{pw}}} = {val}$.",
    ]
    if neg:
        steps.append(f"The minus sign means reciprocal: ${a}^{{{expo}}} = \\frac{{1}}{{{val}}}$.")
    sol = explain(f"${a}$ raised to a fractional{' negative' if neg else ''} exponent.", f"$a^{{p/q}} = \\left(\\sqrt[q]{{a}}\\right)^p$: take the root first (smaller numbers), then the power.{' A negative exponent means take the reciprocal.' if neg else ''}",
                  steps, f"${num(ans).tex}$.", "treating the exponent as multiplication, like $" + str(a) + " \\cdot \\frac{" + str(pw) + "}{" + str(q) + "}$." + (" Or ignoring the minus sign, which gives " + str(val) + "." if neg else ""))
    return (p, ans, [val if neg else F(1, val), -val, rt, F(a * pw, q), base ** (e // q * pw + 1)], [f"Take the root first, then raise to the power ${pw}$."], sol)


def exc1(r):
    a = r.choice([2, 3, 5])
    v = r.randint(3, 9)
    if v % a == 0:
        return None
    k = r.randint(1, 3)
    ans = v * v * a ** k
    p = f"If ${a}^{{x}} = {v}$, what is ${a}^{{2x + {k}}}$?"
    sol = explain(
        f"${a}^{{2x + {k}}}$ without finding $x$ (which is not a nice number).",
        "split the exponent into pieces you know: $a^{m + n} = a^m \\cdot a^n$ and $a^{2x} = (a^x)^2$.",
        [
            f"${a}^{{2x + {k}}} = {a}^{{2x}} \\cdot {a}^{{{k}}}$.",
            f"${a}^{{2x}} = ({a}^x)^2 = {v}^2 = {v * v}$.",
            f"Multiply: ${v * v} \\cdot {a ** k} = {ans}$.",
        ],
        f"${ans}$.",
        f"adding instead of multiplying: ${v}^2 + {a}^{{{k}}} = {v * v + a ** k}$. Adding exponents means multiplying the powers.",
    )
    return (p, ans, [v * v + a ** k, 2 * v * a ** k, v ** 2 * a, v * a ** k, (v * a) ** 2], ["Split the exponent: $a^{2x + k} = (a^x)^2 \\cdot a^k$."], sol)


def exc2(r):
    m, n = r.randint(2, 12), r.randint(2, 12)
    if m == n or (math.isqrt(m) ** 2 == m and math.isqrt(n) ** 2 == n):
        return None
    a_, b_ = max(m, n), min(m, n)
    p = f"The number $\\sqrt{{{m + n} + 2\\sqrt{{{m * n}}}}}$ can be written as $\\sqrt{{a}} + \\sqrt{{b}}$ for positive integers $a > b$. What is $a - b$?"
    sol = explain(
        "the two numbers $a$ and $b$ hidden inside the nested root.",
        "square the target form: $(\\sqrt{a} + \\sqrt{b})^2 = a + b + 2\\sqrt{ab}$. Match it with the expression under the big root.",
        [
            f"Matching parts: $a + b = {m + n}$ and $ab = {m * n}$.",
            f"Find two numbers that add to ${m + n}$ and multiply to ${m * n}$: they are ${a_}$ and ${b_}$.",
            f"Check: $(\\sqrt{{{a_}}} + \\sqrt{{{b_}}})^2 = {a_} + {b_} + 2\\sqrt{{{a_ * b_}}}$. It matches.",
            f"$a - b = {a_} - {b_} = {a_ - b_}$.",
        ],
        f"${a_ - b_}$.",
        "forgetting the factor $2$ in front of $\\sqrt{ab}$ when matching.",
    )
    return (p, a_ - b_, [a_ + b_, a_ * b_, a_ - b_ + 1, abs(a_ - b_ - 2) or 7, a_], ["Square $\\sqrt{a} + \\sqrt{b}$ and match the two parts."], sol)


def exc3(r):
    k = r.randint(1, 3)
    t = r.choice([4, 8, 16, 32])
    c = t * t - (2 ** k) * t
    x = int(math.log2(t))
    if c <= 0:
        return None
    other = c // t
    p = f"What real number $x$ satisfies $4^{{x}} - 2^{{x + {k}}} = {c}$?"
    sol = explain(
        "the exponent $x$.",
        "everything is a power of $2$. Let $t = 2^x$; then $4^x = (2^2)^x = t^2$ and $2^{x + " + str(k) + "} = " + str(2 ** k) + "t$, giving a quadratic.",
        [
            f"Substitute: $t^2 - {2 ** k}t = {c}$, so $t^2 - {2 ** k}t - {c} = 0$.",
            f"Factor: $(t - {t})(t + {other}) = 0$, so $t = {t}$ or $t = -{other}$.",
            f"$t = 2^x$ is always positive, so $t = {t}$.",
            f"$2^x = {t} = 2^{{{x}}}$, so $x = {x}$.",
        ],
        f"$x = {x}$.",
        f"stopping at $t = {t}$ and answering ${t}$. Remember $t$ stands for $2^x$.",
    )
    return (p, x, [x + 1, x - 1, 2 * x, k + 1, x + k], ["Let $t = 2^x$. Then $4^x = t^2$."], sol)


b.fill_unique("basics", [ex1, ex2, ex3, ex4] + MORE[b.skill_id]["basics"], 401)
b.fill_unique("challenge", [exc1, exc2, exc3] + MORE[b.skill_id]["challenge"], 402)


# ---------------------------------------------------------------- factoring and identities
b = bank("alg_factoring")


def fa1(r):
    a = r.randint(51, 999)
    d = r.randint(1, 9)
    x, y = a + d, a - d
    ans = x * x - y * y
    p = f"What is ${x}^2 - {y}^2$?"
    sol = explain(
        "the difference of two big squares, without squaring them.",
        "difference of squares: $x^2 - y^2 = (x - y)(x + y)$.",
        [
            f"$x - y = {x} - {y} = {x - y}$ and $x + y = {x} + {y} = {x + y}$.",
            f"Multiply: ${x - y} \\cdot {x + y} = {ans}$.",
        ],
        f"${ans}$.",
        f"computing $({x} - {y})^2 = {(x - y) ** 2}$. Subtracting the numbers before squaring is not the same.",
    )
    return (p, ans, [(x - y) ** 2, 2 * a * d, ans + 4 * d, ans * 2, x + y], ["Use the difference of squares $x^2 - y^2 = (x - y)(x + y)$."], sol)


def fa2(r):
    s, pr = r.randint(3, 15), r.randint(2, 40)
    ans = s * s - 2 * pr
    p = f"If $a + b = {s}$ and $ab = {pr}$, what is $a^2 + b^2$?"
    sol = explain(
        "$a^2 + b^2$ using only $a + b$ and $ab$.",
        "square the sum: $(a + b)^2 = a^2 + 2ab + b^2$. The $a^2 + b^2$ part is inside.",
        [
            f"$(a + b)^2 = {s}^2 = {s * s}$.",
            f"$a^2 + b^2 = (a + b)^2 - 2ab = {s * s} - 2 \\cdot {pr} = {ans}$.",
        ],
        f"${ans}$.",
        f"forgetting the middle term and answering ${s * s}$.",
    )
    return (p, ans, [s * s, s * s + 2 * pr, s * s - pr, ans + 1, 2 * s], ["Expand $(a + b)^2$."], sol)


def fa3(r):
    a = r.choice([10, 12, 15, 20, 30, 40])
    b_ = r.randint(1, a - 1)
    n = a * a - b_ * b_
    pairs = []
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            e = n // d
            if (d + e) % 2 == 0 and e > d:
                pairs.append((d, e))
    cnt = len(pairs)
    if cnt < 1 or cnt > 9:
        return None
    p = f"For how many ordered pairs of positive integers $(x, y)$ is $x^2 - y^2 = {n}$?"
    sol = explain(
        f"the number of positive integer solutions of $x^2 - y^2 = {n}$.",
        "factor: $(x - y)(x + y) = " + str(n) + "$. Each solution comes from a factor pair of " + str(n) + ".",
        [
            f"Let $u = x - y$ and $v = x + y$. Then $uv = {n}$, $x = \\frac{{u + v}}{{2}}$ and $y = \\frac{{v - u}}{{2}}$.",
            "For $x, y$ to be positive integers: $u < v$, and $u$, $v$ must have the same parity (both odd or both even) so the halves are whole.",
            "Factor pairs that work: " + ", ".join(f"$({u}, {v}) \\to (x, y) = ({(u + v) // 2}, {(v - u) // 2})$" for u, v in pairs) + ".",
        ],
        f"${cnt}$.",
        "counting factor pairs with opposite parity, which give fractions, or the pair with $u = v$, which gives $y = 0$.",
    )
    return (p, cnt, [cnt + 1, cnt - 1 if cnt > 1 else cnt + 2, 2 * cnt, cnt + 3], ["Factor: $(x - y)(x + y) = " + str(n) + "$.", "Both factors must have the same parity, and $x - y < x + y$."], sol)


def fa4(r):
    m = r.randint(2, 9)
    xv = r.randint(2, 9) + 10
    ans = xv * xv + m * xv + m * m
    p = f"What is the value of $\\dfrac{{x^3 - {m ** 3}}}{{x - {m}}}$ when $x = {xv}$?"
    sol = explain(
        f"the value of the fraction at $x = {xv}$.",
        "factor the top as a difference of cubes, $a^3 - b^3 = (a - b)(a^2 + ab + b^2)$, and cancel.",
        [
            f"${m ** 3} = {m}^3$, so $x^3 - {m}^3 = (x - {m})(x^2 + {m}x + {m * m})$.",
            f"Cancel $(x - {m})$: the expression equals $x^2 + {m}x + {m * m}$.",
            f"At $x = {xv}$: ${xv * xv} + {m * xv} + {m * m} = {ans}$.",
        ],
        f"${ans}$.",
        f"factoring as $(x - {m})(x^2 - {m}x + {m * m})$ or $(x - {m})^3$. The signs in the difference of cubes formula matter.",
    )
    return (p, ans, [xv * xv - m * m, xv * xv + m * m, (xv - m) ** 2, ans + m, xv ** 2 + 2 * m * xv + m * m], ["Factor the difference of cubes."], sol)


def fac1(r):
    s, pr = r.randint(2, 9), r.randint(1, 12)
    ans = s ** 3 - 3 * pr * s
    p = f"Real numbers $a$ and $b$ satisfy $a + b = {s}$ and $ab = {pr}$. What is $a^3 + b^3$?"
    sol = explain(
        "$a^3 + b^3$ using only $a + b$ and $ab$.",
        "cube the sum: $(a + b)^3 = a^3 + 3a^2b + 3ab^2 + b^3 = a^3 + b^3 + 3ab(a + b)$.",
        [
            f"So $a^3 + b^3 = (a + b)^3 - 3ab(a + b)$.",
            f"Plug in: ${s}^3 - 3 \\cdot {pr} \\cdot {s} = {s ** 3} - {3 * pr * s} = {ans}$.",
        ],
        f"${ans}$.",
        f"forgetting the extra factor $(a + b)$ in the middle term, which gives ${s ** 3} - {3 * pr} = {s ** 3 - 3 * pr}$.",
    )
    return (p, ans, [s ** 3, s ** 3 - pr * s, s ** 3 + 3 * pr * s, ans + s, s ** 3 - 3 * pr], ["Use $a^3 + b^3 = (a + b)^3 - 3ab(a + b)$."], sol)


def fac2(r):
    a, b_ = r.randint(1, 6), r.randint(1, 6)
    N = r.choice([24, 30, 36, 40, 48, 60, 72])
    c = N - a * b_
    if c <= 0:
        return None
    sols = [(x, y) for x in range(1, 200) for y in range(1, 200) if x * y + a * x + b_ * y == c]
    if not 1 <= len(sols) <= 12:
        return None
    n = len(sols)
    p = f"How many ordered pairs of positive integers $(x, y)$ satisfy $xy + {a}x + {b_}y = {c}$?"
    sol = explain(
        "the number of positive integer solutions.",
        "Simon's Favorite Factoring Trick: add a constant to both sides so the left side factors as a product.",
        [
            f"Notice $(x + {b_})(y + {a}) = xy + {a}x + {b_}y + {a * b_}$. So add ${a * b_}$ to both sides: $(x + {b_})(y + {a}) = {N}$.",
            f"Since $x, y \\ge 1$: $x + {b_} \\ge {b_ + 1}$ and $y + {a} \\ge {a + 1}$.",
            f"Factor pairs of ${N}$ that meet both bounds: " + ", ".join(f"$({x + b_}, {y + a})$" for x, y in sols) + ".",
            f"Each gives one solution $(x, y)$: " + ", ".join(f"$({x}, {y})$" for x, y in sols) + ".",
        ],
        f"${n}$.",
        f"counting every factor pair of ${N}$ without checking that $x$ and $y$ come out positive.",
    )
    return (p, n, [n + 1, n + 2, n - 1 if n > 1 else n + 3, 2 * n], [f"Add ${a * b_}$ to both sides and factor."], sol)


def fac3(r):
    k = r.randint(3, 9)
    which = r.choice([2, 3])
    ans = k * k - 2 if which == 2 else k ** 3 - 3 * k
    p = f"If $x + \\dfrac{{1}}{{x}} = {k}$, what is $x^{{{which}}} + \\dfrac{{1}}{{x^{{{which}}}}}$?"
    if which == 2:
        steps = [f"Square: $\\left(x + \\frac{{1}}{{x}}\\right)^2 = x^2 + 2 \\cdot x \\cdot \\frac{{1}}{{x}} + \\frac{{1}}{{x^2}} = x^2 + 2 + \\frac{{1}}{{x^2}}$.",
                 f"So $x^2 + 2 + \\frac{{1}}{{x^2}} = {k}^2 = {k * k}$, and $x^2 + \\frac{{1}}{{x^2}} = {k * k} - 2 = {ans}$."]
        trap = f"answering ${k * k}$ and forgetting the middle term $2$."
    else:
        steps = [f"Cube: $\\left(x + \\frac{{1}}{{x}}\\right)^3 = x^3 + 3x + \\frac{{3}}{{x}} + \\frac{{1}}{{x^3}} = x^3 + \\frac{{1}}{{x^3}} + 3\\left(x + \\frac{{1}}{{x}}\\right)$.",
                 f"So ${k ** 3} = x^3 + \\frac{{1}}{{x^3}} + 3 \\cdot {k}$, and $x^3 + \\frac{{1}}{{x^3}} = {k ** 3} - {3 * k} = {ans}$."]
        trap = f"answering ${k ** 3}$ and forgetting the middle terms."
    sol = explain(f"$x^{{{which}}} + \\frac{{1}}{{x^{{{which}}}}}$ without solving for $x$.", "raise the given equation to a power. Since $x \\cdot \\frac{1}{x} = 1$, the cross terms are just numbers.", steps, f"${ans}$.", trap)
    return (p, ans, [k ** which, k ** which - 1, ans + 2, k * k + 2 if which == 2 else k ** 3 - k, ans - k], ["Square (or cube) both sides of the given equation and expand."], sol)


b.fill_unique("basics", [fa1, fa2, fa3, fa4] + MORE[b.skill_id]["basics"], 501)
b.fill_unique("challenge", [fac1, fac2, fac3] + MORE[b.skill_id]["challenge"], 502)


# ---------------------------------------------------------------- quadratics
b = bank("alg_quadratics")


def q1(r):
    p_, q_ = r.randint(-9, 9), r.randint(-9, 9)
    if p_ == q_ or p_ == 0 or q_ == 0:
        return None
    s, pr = p_ + q_, p_ * q_
    if s == 0:
        return None
    ask = r.choice(["sum", "product", "larger"])
    poly = f"x^2 {'-' if s > 0 else '+'} {abs(s)}x {'+' if pr > 0 else '-'} {abs(pr)}"
    ans = {"sum": s, "product": pr, "larger": max(p_, q_)}[ask]
    words = {"sum": "the sum of the roots", "product": "the product of the roots", "larger": "the larger root"}[ask]
    p = f"What is {words} of ${poly} = 0$?"
    f1 = f"(x {'-' if p_ > 0 else '+'} {abs(p_)})"
    f2 = f"(x {'-' if q_ > 0 else '+'} {abs(q_)})"
    sol = explain(
        f"{words}.",
        "find two numbers that multiply to the constant term and add to the negative of the $x$ coefficient; they are the roots.",
        [
            f"We need two numbers with product ${pr}$ and sum ${s}$: they are ${p_}$ and ${q_}$.",
            f"So ${poly} = {f1}{f2}$, and the roots are $x = {p_}$ and $x = {q_}$.",
            f"{words.capitalize()}: ${ans}$." + (" (Vieta's formulas give this directly: sum $= -b$, product $= c$.)" if ask != "larger" else ""),
        ],
        f"${ans}$.",
        "flipping a sign. The roots are the numbers that make each factor zero, so $(x - 3)$ gives the root $3$, not $-3$.",
    )
    return (p, ans, [-s, -pr, s, pr, min(p_, q_), max(p_, q_), ans + 1], ["Factor, or use $r_1 + r_2 = -\\frac{b}{a}$ and $r_1 r_2 = \\frac{c}{a}$."], sol)


def q2(r):
    h, k = r.randint(-8, 8), r.randint(-20, 20)
    if h == 0:
        return None
    a = r.choice([1, 2, 3])
    bq, cq = -2 * a * h, a * h * h + k
    ask = r.choice(["min", "at"])
    poly = f"{a if a > 1 else ''}x^2 {'+' if bq >= 0 else '-'} {abs(bq)}x {'+' if cq >= 0 else '-'} {abs(cq)}"
    p = f"What is the minimum value of $f(x) = {poly}$?" if ask == "min" else f"For what value of $x$ is $f(x) = {poly}$ smallest?"
    ans = k if ask == "min" else h
    sol = explain(
        "the lowest point of the parabola (its vertex)." if ask == "min" else "the $x$ where the parabola is lowest (the vertex).",
        "the vertex of $ax^2 + bx + c$ is at $x = -\\frac{b}{2a}$. Plug that $x$ back in to get the minimum value.",
        [
            f"Here $a = {a}$ and $b = {bq}$, so $x = -\\frac{{{bq}}}{{2 \\cdot {a}}} = {h}$.",
            f"$f({h}) = {a} \\cdot {h * h} + ({bq})({h}) + {cq} = {a * h * h} - {abs(bq * h) if bq * h > 0 else -bq * h} + {cq} = {k}$." if bq * h > 0 else f"$f({h}) = {a} \\cdot {h * h} + ({bq})({h}) + {cq} = {k}$.",
            f"(Completed square form: $f(x) = {a if a > 1 else ''}(x {'-' if h >= 0 else '+'} {abs(h)})^2 {'+' if k >= 0 else '-'} {abs(k)}$, and a square is never negative.)",
        ],
        f"${ans}$.",
        ("answering with the $x$ value of the vertex instead of the minimum value." if ask == "min" else "answering with the minimum value instead of the $x$ where it happens.") + " Also watch the sign: the vertex is at $-\\frac{b}{2a}$.",
    )
    return (p, ans, [h if ask == "min" else k, cq, -h if h else 4, ans + a, ans - 1], ["Complete the square, or use $x = -\\frac{b}{2a}$."], sol)


def q3(r):
    a = r.choice([1, 2, 3, 4])
    m = r.randint(1, 8)
    c = m * m
    k = 2 * a * m
    p = f"For what positive value of $k$ does ${a if a > 1 else ''}x^2 + kx + {a * c} = 0$ have exactly one real solution?"
    sol = explain(
        "the $k$ that makes the quadratic have a single (repeated) root.",
        "a quadratic $Ax^2 + Bx + C = 0$ has exactly one real solution when its discriminant $B^2 - 4AC$ is $0$.",
        [
            f"Here $A = {a}$, $B = k$, $C = {a * c}$.",
            f"Set the discriminant to zero: $k^2 - 4 \\cdot {a} \\cdot {a * c} = 0$, so $k^2 = {4 * a * a * c}$.",
            f"$k = \\pm{k}$; the positive value is $k = {k}$.",
        ],
        f"$k = {k}$.",
        f"forgetting the $4$ in $4AC$, which gives ${a * m}$.",
    )
    return (p, k, [a * m, 2 * m, k + 2, 4 * a * m, m], ["A quadratic has exactly one solution when the discriminant $b^2 - 4ac$ is zero."], sol)


def q4(r):
    p_, q_ = r.randint(-7, 9), r.randint(-7, 9)
    s, pr = p_ + q_, p_ * q_
    if s == 0 or pr == 0:
        return None
    poly = f"x^2 {'-' if s > 0 else '+'} {abs(s)}x {'+' if pr > 0 else '-'} {abs(pr)}"
    ans = s * s - 2 * pr
    p = f"Let $r$ and $s$ be the roots of ${poly} = 0$. What is $r^2 + s^2$?"
    sol = explain(
        "$r^2 + s^2$ for the two roots.",
        "Vieta's formulas give $r + s$ and $rs$ straight from the coefficients; then rewrite $r^2 + s^2$ in terms of those.",
        [
            f"For $x^2 + bx + c$: $r + s = -b = {s}$ and $rs = c = {pr}$.",
            "$(r + s)^2 = r^2 + 2rs + s^2$, so $r^2 + s^2 = (r + s)^2 - 2rs$.",
            f"Plug in: ${s}^2 - 2({pr}) = {s * s} - ({2 * pr}) = {ans}$.",
        ],
        f"${ans}$.",
        "using $r + s = b$ instead of $-b$.",
    )
    return (p, ans, [s * s, s * s + 2 * pr, s * s - pr, ans + 2, abs(pr) * 2], ["Use $r^2 + s^2 = (r + s)^2 - 2rs$ with Vieta's formulas."], sol)


def qc1(r):
    p_, q_ = r.randint(-6, 8), r.randint(-6, 8)
    k = r.randint(1, 5)
    s, pr = p_ + q_, p_ * q_
    if s == 0 or pr == 0:
        return None
    poly = f"x^2 {'-' if s > 0 else '+'} {abs(s)}x {'+' if pr > 0 else '-'} {abs(pr)}"
    ans = (p_ + k) * (q_ + k)
    p = f"The roots of ${poly} = 0$ are $r$ and $s$. The quadratic $x^2 + bx + c = 0$ has roots $r + {k}$ and $s + {k}$. What is $c$?"
    sol = explain(
        "the constant term $c$ of the new quadratic.",
        "for $x^2 + bx + c$, the constant $c$ is the product of the roots. Expand that product and use Vieta on the original quadratic.",
        [
            f"From the original: $r + s = {s}$ and $rs = {pr}$.",
            f"$c = (r + {k})(s + {k}) = rs + {k}(r + s) + {k * k}$.",
            f"Plug in: ${pr} + {k} \\cdot {s} + {k * k} = {pr} + {k * s} + {k * k} = {ans}$.",
        ],
        f"$c = {ans}$.",
        f"forgetting the cross term ${k}(r + s)$ when expanding.",
    )
    return (p, ans, [pr + k, pr + k * k, pr + k * s, ans + k, (p_ - k) * (q_ - k)], ["$c$ is the product of the new roots. Expand $(r + k)(s + k)$."], sol)


def qc2(r):
    p_, q_ = sorted(r.sample(range(-5, 25), 2))
    if q_ - p_ < 3:
        return None
    s, pr = p_ + q_, p_ * q_
    poly = f"n^2 {'-' if s > 0 else '+'} {abs(s)}n {'+' if pr > 0 else '-'} {abs(pr)}" if s else f"n^2 {'+' if pr > 0 else '-'} {abs(pr)}"
    cnt = q_ - p_ - 1
    p = f"How many integers $n$ satisfy ${poly} < 0$?"
    sol = explain(
        "the integers that make the quadratic negative.",
        "an upward parabola is negative exactly between its two roots.",
        [
            f"Factor: ${poly} = (n {'-' if p_ >= 0 else '+'} {abs(p_)})(n {'-' if q_ >= 0 else '+'} {abs(q_)})$, with roots ${p_}$ and ${q_}$.",
            f"The product is negative when one factor is positive and the other negative, which happens for ${p_} < n < {q_}$.",
            f"Integers strictly between ${p_}$ and ${q_}$: ${q_} - ({p_}) - 1 = {cnt}$.",
        ],
        f"${cnt}$.",
        "including the roots themselves. At the roots the value is $0$, which is not less than $0$.",
    )
    return (p, cnt, [cnt + 1, cnt + 2, cnt - 1, q_ - p_ + 1, s], ["Factor and find where the parabola is below zero."], sol)


def qc3(r):
    N = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48])
    pairs = [(d, N // d) for d in range(1, math.isqrt(N) + 1) if N % d == 0]
    ks = sorted({d + e for d, e in pairs})
    cnt = 2 * len(ks)
    p = f"For how many integers $k$ does $x^2 - kx + {N} = 0$ have two integer roots (not necessarily different)?"
    sol = explain(
        f"how many values of $k$ give integer roots.",
        f"if the roots are integers $r$ and $s$, Vieta says $rs = {N}$ and $r + s = k$. So each factor pair of ${N}$ gives a value of $k$.",
        [
            "Positive factor pairs: " + ", ".join(f"${d} \\cdot {e}$" for d, e in pairs) + ".",
            "Their sums: " + ", ".join(f"${d + e}$" for d, e in pairs) + ".",
            f"Both roots can also be negative (their product is still positive), which gives the negatives of these sums.",
            f"So there are ${len(ks)}$ positive and ${len(ks)}$ negative values: ${cnt}$ in all.",
        ],
        f"${cnt}$.",
        "forgetting the pairs of negative roots, which halves the count.",
    )
    return (p, cnt, [cnt // 2, cnt + 2, cnt - 2, cnt + 1, len([d for d in range(1, N + 1) if N % d == 0])],
            [f"If the roots are integers $r$ and $s$, then $rs = {N}$ and $k = r + s$.", "Both roots can be negative."], sol)


b.fill_unique("basics", [q1, q2, q3, q4] + MORE[b.skill_id]["basics"], 601)
b.fill_unique("challenge", [qc1, qc2, qc3] + MORE[b.skill_id]["challenge"], 602)


# ---------------------------------------------------------------- absolute value and inequalities
b = bank("alg_absolute")


def ab1(r):
    a, c = r.randint(-10, 10), r.randint(2, 15)
    lo, hi = a - c, a + c
    cnt = hi - lo + 1
    p = f"How many integers $x$ satisfy $|x {'-' if a >= 0 else '+'} {abs(a)}| \\le {c}$?"
    sol = explain(
        f"the integers within distance ${c}$ of ${a}$.",
        "$|x - a| \\le c$ means $x$ is at most $c$ away from $a$ on the number line: $a - c \\le x \\le a + c$.",
        [
            f"Here the center is ${a}$ and the distance is ${c}$, so ${a} - {c} \\le x \\le {a} + {c}$, that is ${lo} \\le x \\le {hi}$.",
            f"Integers from ${lo}$ to ${hi}$ inclusive: ${hi} - ({lo}) + 1 = {cnt}$.",
        ],
        f"${cnt}$.",
        f"forgetting the $+1$ when counting from one integer to another inclusive, which gives ${2 * c}$.",
    )
    return (p, cnt, [cnt - 1, 2 * c, cnt + 1, c + 1, 2 * c - 1], ["$|x - a| \\le c$ means $a - c \\le x \\le a + c$."], sol)


def ab2(r):
    a, c = r.randint(-10, 10), r.randint(1, 12)
    k = r.randint(2, 4)
    s = F(2 * a, k)
    x1, x2 = F(a + c, k), F(a - c, k)
    p = f"What is the sum of all solutions to $|{k}x {'-' if a >= 0 else '+'} {abs(a)}| = {c}$?"
    sol = explain(
        "both solutions of the absolute value equation, then their sum.",
        "$|A| = c$ (with $c > 0$) means $A = c$ or $A = -c$.",
        [
            f"Case 1: ${k}x {'-' if a >= 0 else '+'} {abs(a)} = {c}$, so ${k}x = {a + c}$ and $x = {num(x1).tex}$.",
            f"Case 2: ${k}x {'-' if a >= 0 else '+'} {abs(a)} = -{c}$, so ${k}x = {a - c}$ and $x = {num(x2).tex}$.",
            f"Sum: ${num(x1).tex} + ({num(x2).tex}) = {num(s).tex}$.",
        ],
        f"${num(s).tex}$.",
        "solving only the positive case.",
    )
    return (p, s, [F(a, k), F(2 * c, k), F(a + c, k), 2 * a, -s if s else 1], ["Split into the two cases $kx - a = c$ and $kx - a = -c$."], sol)


def ab3(r):
    a, bb, c = r.randint(2, 7), r.randint(-15, 15), r.randint(-20, 30)
    bound = F(c - bb, a)
    sm = math.floor(bound) + 1
    p = f"What is the smallest integer $x$ such that ${a}x {'+' if bb >= 0 else '-'} {abs(bb)} > {c}$?"
    sol = explain(
        "the first integer that makes the inequality true.",
        "solve like an equation, keeping the inequality sign. Dividing by a positive number keeps the direction.",
        [
            f"{'Subtract' if bb >= 0 else 'Add'} ${abs(bb)}$: ${a}x > {c - bb}$.",
            f"Divide by ${a}$: $x > {num(bound).tex}$.",
            f"The smallest integer strictly greater than ${num(bound).tex}$ is ${sm}$.",
        ],
        f"${sm}$.",
        f"choosing ${num(bound).tex}$ itself when it is a whole number. The inequality is strict, so that value does not work." if bound.denominator == 1 else "rounding down instead of up.",
    )
    return (p, sm, [sm - 1, sm + 1, math.ceil(bound) if math.ceil(bound) != sm else sm + 2, c - bb, sm + a], ["Solve for $x$, then find the first integer strictly greater than the bound."], sol)


def ab4(r):
    a, bb = sorted(r.sample(range(-12, 15), 2))
    if bb - a < 2:
        return None
    p = f"What is the minimum value of $|x {'-' if a >= 0 else '+'} {abs(a)}| + |x {'-' if bb >= 0 else '+'} {abs(bb)}|$ over all real $x$?"
    sol = explain(
        f"the smallest possible total distance from a point $x$ to both ${a}$ and ${bb}$.",
        "$|x - a|$ is the distance from $x$ to $a$ on the number line.",
        [
            f"If $x$ is anywhere between ${a}$ and ${bb}$, the two distances together cover the gap exactly: ${bb} - ({a}) = {bb - a}$.",
            f"If $x$ is outside that gap, you travel the gap and then extra, so the total is more than ${bb - a}$.",
        ],
        f"${bb - a}$.",
        "thinking the minimum is $0$. Both distances can't be $0$ at the same time.",
    )
    return (p, bb - a, [0, abs(a) + abs(bb), (bb - a) // 2, bb - a + 1, abs(a + bb)], ["The sum of distances from $x$ to two points is smallest when $x$ is between them."], sol)


def abc1(r):
    n = r.randint(2, 9)
    cnt = 2 * n * n + 2 * n + 1
    rows = [2 * (n - abs(y)) + 1 for y in range(-n, n + 1)]
    p = f"How many ordered pairs of integers $(x, y)$ satisfy $|x| + |y| \\le {n}$?"
    sol = explain(
        "the number of lattice points inside a diamond shape.",
        "count row by row. For a fixed $y$, the condition becomes $|x| \\le " + str(n) + " - |y|$.",
        [
            f"For a fixed $y$ with $|y| = k$, $x$ runs from $-({n} - k)$ to ${n} - k$: that is $2({n} - k) + 1$ values.",
            f"Rows from $y = -{n}$ to $y = {n}$ have " + ", ".join(map(str, rows)) + " points.",
            f"Add them: ${cnt}$. (In general $2n^2 + 2n + 1$.)",
        ],
        f"${cnt}$.",
        f"counting the square $|x| \\le {n}$, $|y| \\le {n}$, which has ${(2 * n + 1) ** 2}$ points.",
    )
    return (p, cnt, [(2 * n + 1) ** 2, 4 * n * n, cnt - 4 * n, cnt + 1, 2 * n * n], ["Count row by row: for each $y$, $|x| \\le n - |y|$."], sol)


def abc2(r):
    a, bb = sorted(r.sample(range(-8, 12), 2))
    c = (bb - a) + 2 * r.randint(1, 6)
    x1 = F(a + bb - c, 2)
    x2 = F(a + bb + c, 2)
    ans = x1 * x2
    p = f"What is the product of the solutions of $|x {'-' if a >= 0 else '+'} {abs(a)}| + |x {'-' if bb >= 0 else '+'} {abs(bb)}| = {c}$?"
    sol = explain(
        "both solutions, then their product.",
        f"the left side is the total distance from $x$ to ${a}$ and ${bb}$. Between them it equals ${bb - a}$, which is less than ${c}$, so the solutions are outside.",
        [
            f"Right of ${bb}$: both expressions are positive, so $(x {'-' if a >= 0 else '+'} {abs(a)}) + (x {'-' if bb >= 0 else '+'} {abs(bb)}) = {c}$, giving $2x = {c + a + bb}$ and $x = {num(x2).tex}$.",
            f"Left of ${a}$: both are negative, so $({a} - x) + ({bb} - x) = {c}$, giving $2x = {a + bb - c}$ and $x = {num(x1).tex}$.",
            f"Product: $({num(x1).tex}) \\cdot ({num(x2).tex}) = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "looking for a solution between the two points. There the total distance is fixed at the gap.",
    )
    return (p, ans, [x1 + x2, a * bb, ans + 1, -ans if ans else 3, x2 * x2], ["For $x$ outside the interval between the two points, the expression is $|2x - (a + b)|$."], sol)


def abc3(r):
    c = r.randint(2, 9)
    a, bb = r.randint(-5, 5), r.randint(-5, 5)
    ans = 2 * c * c
    p = f"What is the area of the region of points $(x, y)$ with $|x {'-' if a >= 0 else '+'} {abs(a)}| + |y {'-' if bb >= 0 else '+'} {abs(bb)}| \\le {c}$?"
    sol = explain(
        "the area of the region.",
        "$|X| + |Y| \\le c$ is a square tilted $45^\\circ$ (a diamond) with corners $c$ units from its center along the axes. Shifting the center does not change the area.",
        [
            f"The center is $({a}, {bb})$, and the corners are ${c}$ units away: up, down, left and right.",
            f"So both diagonals have length $2 \\cdot {c} = {2 * c}$.",
            f"Area of a square (or any rhombus) from its diagonals: $\\frac{{d_1 d_2}}{{2}} = \\frac{{{2 * c} \\cdot {2 * c}}}{{2}} = {ans}$.",
        ],
        f"${ans}$.",
        f"using ${2 * c}$ as the side length, which gives ${4 * c * c}$. ${2 * c}$ is the diagonal.",
    )
    return (p, ans, [c * c, 4 * c * c, (2 * c) ** 2 // 2 + c, 2 * c, ans + 2 * c], ["The region is a square turned 45 degrees with diagonals of length $2c$."], sol)


b.fill_unique("basics", [ab1, ab2, ab3, ab4] + MORE[b.skill_id]["basics"], 701)
b.fill_unique("challenge", [abc1, abc2, abc3] + MORE[b.skill_id]["challenge"], 702)


# ---------------------------------------------------------------- mean, median, mode
b = bank("alg_stats")


def st1(r):
    n = r.randint(4, 7)
    vals = [r.randint(50, 99) for _ in range(n)]
    target = r.randint(75, 95)
    need = target * (n + 1) - sum(vals)
    if not 0 <= need <= 100:
        return None
    nm = r.choice(NAMES)
    p = (f"{nm} scored " + ", ".join(map(str, vals[:-1])) + f", and {vals[-1]} on {n} quizzes. What score on the next quiz "
         f"would make the average of all {n + 1} quizzes exactly {target}?")
    sol = explain(
        f"the score $s$ on quiz ${n + 1}$ that brings the average to ${target}$.",
        "an average is a total divided by a count, so work with totals: needed total $=$ average $\\times$ count.",
        [
            f"Needed total for ${n + 1}$ quizzes: ${target} \\cdot {n + 1} = {target * (n + 1)}$.",
            f"Current total: " + " + ".join(map(str, vals)) + f" $= {sum(vals)}$.",
            f"Missing amount: $s = {target * (n + 1)} - {sum(vals)} = {need}$.",
        ],
        f"${need}$.",
        f"answering ${target}$. One more score of ${target}$ only works if the average is already ${target}$.",
    )
    return (p, need, [target, need + n, need - n, target * n - sum(vals) + target, need + 1], ["The total of all scores must be the average times the number of quizzes."], sol)


def st2(r):
    n = r.choice([5, 6, 7, 8])
    vals = sorted(r.randint(1, 40) for _ in range(n))
    shuffled = vals[:]
    r.shuffle(shuffled)
    med = F(vals[n // 2]) if n % 2 else F(vals[n // 2 - 1] + vals[n // 2], 2)
    mean = F(sum(vals), n)
    ask = r.choice(["median", "diff"])
    sorted_line = "Sort the list: " + ", ".join(map(str, vals)) + "."
    med_line = (f"There are ${n}$ numbers (odd), so the median is the middle one, number ${n // 2 + 1}$: ${num(med).tex}$." if n % 2
                else f"There are ${n}$ numbers (even), so the median is the average of the two middle ones, ${vals[n // 2 - 1]}$ and ${vals[n // 2]}$: ${num(med).tex}$.")
    if ask == "median":
        p = "What is the median of the list " + ", ".join(map(str, shuffled)) + "?"
        sol = explain("the median, the middle value once the list is in order.", "always sort first; the median depends on order, not on the position in the original list.", [sorted_line, med_line], f"${num(med).tex}$.",
                      "taking the middle entry of the unsorted list.")
        return (p, med, [mean, F(shuffled[n // 2]), vals[n // 2 - 1] if n % 2 == 0 else vals[n // 2 + 1], F(vals[0] + vals[-1], 2), med + 1], ["Sort the list first."], sol)
    d = mean - med
    p = "What is the mean minus the median of the list " + ", ".join(map(str, shuffled)) + "?"
    sol = explain("the mean and the median, then their difference.", "the mean is the total divided by the count; the median is the middle value after sorting.",
                  [f"Mean: $\\frac{{{sum(vals)}}}{{{n}}} = {num(mean).tex}$.", sorted_line, med_line, f"Mean minus median: ${num(mean).tex} - {num(med).tex} = {num(d).tex}$."],
                  f"${num(d).tex}$.", "subtracting in the wrong order (median minus mean), which flips the sign.")
    return (p, d, [med - mean, mean, d + 1, 0 if d else 1, F(vals[-1] - vals[0], 2)], ["Find the mean and median separately."], sol)


def st3(r):
    n1, n2 = r.randint(10, 30), r.randint(10, 30)
    a1, a2 = r.randint(70, 90), r.randint(70, 90)
    if a1 == a2:
        return None
    comb_ = F(n1 * a1 + n2 * a2, n1 + n2)
    p = f"In a class, {n1} students averaged {a1} on a test and the other {n2} students averaged {a2}. What was the class average?"
    sol = explain(
        "the average over all students.",
        "averages of groups of different sizes can't just be averaged. Rebuild the total of all scores.",
        [
            f"First group total: ${n1} \\cdot {a1} = {n1 * a1}$. Second group total: ${n2} \\cdot {a2} = {n2 * a2}$.",
            f"Class total: ${n1 * a1 + n2 * a2}$ over ${n1 + n2}$ students.",
            f"Class average: $\\frac{{{n1 * a1 + n2 * a2}}}{{{n1 + n2}}} = {num(comb_).tex}$.",
        ],
        f"${num(comb_).tex}$.",
        f"averaging ${a1}$ and ${a2}$ to get ${num(F(a1 + a2, 2)).tex}$, which ignores that the groups have different sizes.",
    )
    return (p, comb_, [F(a1 + a2, 2), comb_ + 1, comb_ - 1, F(n1 * a2 + n2 * a1, n1 + n2), max(a1, a2)], ["Find the total of all scores, then divide by the number of students."], sol)


def st4(r):
    n = r.randint(5, 12)
    m1 = r.randint(10, 40)
    m2 = m1 + r.choice([-3, -2, -1, 1, 2, 3])
    removed = n * m1 - (n - 1) * m2
    if removed <= 0:
        return None
    p = f"The mean of {n} numbers is {m1}. When one number is removed, the mean of the rest is {m2}. What number was removed?"
    sol = explain(
        "the removed number.",
        "compare totals: total $=$ mean $\\times$ count.",
        [f"Total before: ${n} \\cdot {m1} = {n * m1}$.", f"Total after: ${n - 1} \\cdot {m2} = {(n - 1) * m2}$.", f"Removed: ${n * m1} - {(n - 1) * m2} = {removed}$."],
        f"${removed}$.",
        "multiplying both means by the same count. After removing a number there is one fewer.",
    )
    return (p, removed, [m1, m2, abs(m1 - m2) * n, removed + n, n * m1 - n * m2], ["Compare the totals before and after."], sol)


def stc1(r):
    mean = r.randint(8, 20)
    med = mean - r.randint(0, 3)
    mode = med - r.randint(1, 4)
    if mode < 1:
        return None
    d = med + 1
    e = 5 * mean - (2 * mode + med + d)
    if e <= d:
        return None
    p = (f"A list of 5 positive integers has mean {mean}, median {med}, and a unique mode of {mode}. "
         f"What is the largest possible value of the largest number in the list?")
    sol = explain(
        "the biggest the largest number can be.",
        "the five numbers have a fixed total. To make the largest one big, make the other four as small as the rules allow.",
        [
            f"The total is $5 \\cdot {mean} = {5 * mean}$. Write the sorted list as $a \\le b \\le c \\le d \\le e$.",
            f"The median is the middle number: $c = {med}$.",
            f"The mode ${mode}$ must appear at least twice, and it is below the median, so $a = b = {mode}$.",
            f"$d$ must be at least ${med}$. But $d = {med}$ would make ${med}$ appear twice too, tying the mode, which is not allowed. So the smallest choice is $d = {d}$.",
            f"Then $e = {5 * mean} - ({mode} + {mode} + {med} + {d}) = {e}$.",
        ],
        f"${e}$.",
        f"using $d = {med}$, which creates a second mode.",
    )
    return (p, e, [e + 1, e - 1, 5 * mean - 3 * mode - med, 5 * mean - mode - 2 * med, e + 2],
            ["To make the largest number big, make the others as small as the rules allow.", "The mode must appear more often than any other value."], sol)


def stc2(r):
    vals = sorted(r.sample(range(1, 30), 4))
    s = sum(vals)
    sols = []
    for x in range(-200, 300):
        L = sorted(vals + [x])
        if F(s + x, 5) == L[2]:
            sols.append(x)
    if not sols or len(sols) > 3:
        return None
    n = len(sols)
    v1, v2 = vals[1], vals[2]
    p = "For how many integers $x$ is the mean of " + ", ".join(map(str, vals)) + ", $x$ equal to its median?"
    cases = [
        f"If $x \\le {v1}$, the median is ${v1}$. Mean $= {v1}$ means ${s} + x = {5 * v1}$, so $x = {5 * v1 - s}$" + (" (it works)." if (5 * v1 - s) in sols else f", but that is not $\\le {v1}$, so it fails."),
        f"If ${v1} \\le x \\le {v2}$, the median is $x$. Mean $= x$ means ${s} + x = 5x$, so $x = {num(F(s, 4)).tex}$" + (" (it works)." if F(s, 4) in [F(v) for v in sols] else ", which fails (not an integer in that range)."),
        f"If $x \\ge {v2}$, the median is ${v2}$. Mean $= {v2}$ means $x = {5 * v2 - s}$" + (" (it works)." if (5 * v2 - s) in sols else f", but that is not $\\ge {v2}$, so it fails."),
    ]
    sol = explain(f"how many integers $x$ make the mean of the five numbers equal the median.", "where $x$ falls in the sorted list decides which number is the median. Split into cases.",
                  [f"The sum of the given numbers is ${s}$, so the mean is $\\frac{{{s} + x}}{{5}}$."] + cases, f"${n}$.", "assuming $x$ is always the median, which skips the other cases.")
    return (p, n, [n + 1, n + 2, 0 if n else 4, 4, 5], ["The median is either $x$ itself or one of the two middle given numbers. Try each case."], sol)


def stc3(r):
    k = r.choice([5, 7, 9, 11])
    start = r.randint(1, 40)
    seq = list(range(start, start + k))
    s = sum(seq)
    mid = seq[k // 2]
    p = f"The sum of {k} consecutive integers is {s}. What is the largest of these integers?"
    sol = explain(
        "the largest of the consecutive integers.",
        "for an odd number of consecutive integers, the average is the middle one.",
        [
            f"Average: $\\frac{{{s}}}{{{k}}} = {mid}$, so the middle integer is ${mid}$.",
            f"There are ${k // 2}$ integers above the middle, so the largest is ${mid} + {k // 2} = {seq[-1]}$.",
        ],
        f"${seq[-1]}$.",
        f"answering with the middle number ${mid}$.",
    )
    return (p, seq[-1], [seq[-2], mid, seq[0], seq[-1] + 1, s // k + k], ["The average of consecutive integers is the middle one."], sol)


b.fill_unique("basics", [st1, st2, st3, st4] + MORE[b.skill_id]["basics"], 801)
b.fill_unique("challenge", [stc1, stc2, stc3] + MORE[b.skill_id]["challenge"], 802)


# ---------------------------------------------------------------- sequences
b = bank("alg_sequences")


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def sq1(r):
    a, d, n = r.randint(-10, 20), r.randint(-6, 9), r.randint(10, 60)
    if d == 0:
        return None
    ans = a + (n - 1) * d
    terms = ", ".join(str(a + i * d) for i in range(4))
    p = f"What is the {ordinal(n)} term of the arithmetic sequence {terms}, ...?"
    sol = explain(
        f"term number ${n}$.",
        "an arithmetic sequence adds the same difference $d$ each step. To get from term $1$ to term $n$ takes $n - 1$ steps: $a_n = a_1 + (n - 1)d$.",
        [
            f"First term $a_1 = {a}$. Common difference $d = {a + d} - ({a}) = {d}$.",
            f"$a_{{{n}}} = {a} + ({n} - 1) \\cdot ({d}) = {a} + {(n - 1) * d} = {ans}$.",
        ],
        f"${ans}$.",
        f"using $n \\cdot d$ instead of $(n - 1)d$, which gives ${a + n * d}$, one step too far.",
    )
    return (p, ans, [a + n * d, ans - d, a * n, ans + 1, a + (n - 2) * d], ["The $n$th term is $a + (n - 1)d$."], sol)


def sq2(r):
    a, d, n = r.randint(1, 15), r.randint(1, 8), r.randint(10, 40)
    s = n * (2 * a + (n - 1) * d) // 2
    last = a + (n - 1) * d
    p = "What is the sum of the arithmetic sequence $" + " + ".join(str(a + i * d) for i in range(3)) + f" + \\cdots + {last}$?"
    sol = explain(
        "the sum of all the terms.",
        "sum of an arithmetic sequence $=$ (number of terms) $\\times$ (average of first and last term).",
        [
            f"Count the terms: from ${a}$ to ${last}$ in steps of ${d}$ is $\\frac{{{last} - {a}}}{{{d}}} + 1 = {n}$ terms.",
            f"Average of first and last: $\\frac{{{a} + {last}}}{{2}} = {num(F(a + last, 2)).tex}$.",
            f"Sum: ${n} \\cdot {num(F(a + last, 2)).tex} = {s}$.",
        ],
        f"${s}$.",
        "forgetting the $+1$ when counting terms, or forgetting to divide by $2$.",
    )
    return (p, s, [n * (a + last), s - last, s + d, n * last, (n - 1) * (a + last) // 2], ["Count the terms, then multiply the number of terms by the average of the first and last."], sol)


def sq3(r):
    a, rr = r.randint(1, 6), r.choice([2, 3, -2])
    n = r.randint(5, 9)
    ans = a * rr ** (n - 1)
    terms = ", ".join(str(a * rr ** i) for i in range(4))
    p = f"What is the {ordinal(n)} term of the geometric sequence {terms}, ...?"
    sol = explain(
        f"term number ${n}$.",
        "a geometric sequence multiplies by the same ratio $r$ each step: $a_n = a_1 \\cdot r^{n - 1}$.",
        [
            f"First term ${a}$, ratio $\\frac{{{a * rr}}}{{{a}}} = {rr}$.",
            f"$a_{{{n}}} = {a} \\cdot ({rr})^{{{n - 1}}} = {a} \\cdot {rr ** (n - 1)} = {ans}$.",
        ],
        f"${ans}$.",
        "using the exponent $n$ instead of $n - 1$." + (" With a negative ratio, also watch the sign: even powers are positive." if rr < 0 else ""),
    )
    return (p, ans, [a * rr ** n, a * rr ** (n - 2), -ans, a * rr * (n - 1), ans // abs(rr) * (abs(rr) + 1)], ["Each term is the previous term times the common ratio."], sol)


def sq4(r):
    a, d = r.randint(-10, 20), r.randint(-5, 7)
    if d == 0:
        return None
    i, j, k = sorted(r.sample(range(2, 30), 3))
    ti, tj = a + (i - 1) * d, a + (j - 1) * d
    tk = a + (k - 1) * d
    p = f"In an arithmetic sequence, term {i} is ${ti}$ and term {j} is ${tj}$. What is term {k}?"
    sol = explain(
        f"term number ${k}$.",
        "the common difference is the change between two terms divided by the number of steps between them.",
        [
            f"From term ${i}$ to term ${j}$ is ${j - i}$ steps, and the value changes by ${tj} - ({ti}) = {tj - ti}$. So $d = \\frac{{{tj - ti}}}{{{j - i}}} = {d}$.",
            f"From term ${j}$ to term ${k}$ is ${k - j}$ more steps: ${tj} + {k - j} \\cdot ({d}) = {tk}$.",
        ],
        f"${tk}$.",
        f"dividing the change by ${j}$ or ${i}$ instead of the number of steps, ${j - i}$.",
    )
    return (p, tk, [tk + d, tk - d, ti + tj, tj + (k - j), a + k * d], ["Find the common difference from the two given terms."], sol)


def sqc1(r):
    m, N = r.randint(3, 13), r.randint(100, 999)
    res = r.randint(0, m - 1)
    nums = [x for x in range(1, N + 1) if x % m == res]
    cnt = len(nums)
    p = f"How many integers from $1$ to ${N}$ leave a remainder of ${res}$ when divided by ${m}$?"
    sol = explain(
        f"how many numbers from $1$ to ${N}$ have the form ${m}q + {res}$.",
        f"these numbers form an arithmetic sequence with difference ${m}$. Find the first and last, then count.",
        [
            f"First one in range: ${nums[0]}$. Last one: ${nums[-1]}$ (the next would be ${nums[-1] + m}$, past ${N}$).",
            f"Count: $\\frac{{{nums[-1]} - {nums[0]}}}{{{m}}} + 1 = {cnt}$.",
        ],
        f"${cnt}$.",
        f"using $\\left\\lfloor \\frac{{{N}}}{{{m}}} \\right\\rfloor = {N // m}$ without checking where the sequence starts and ends." + (" With remainder $0$, the first number is " + str(m) + ", not $0$." if res == 0 else ""),
    )
    return (p, cnt, [cnt + 1, cnt - 1, N // m if N // m != cnt else cnt + 2, N // m + 1 if N // m + 1 != cnt else N // m - 1, cnt + 3], ["These numbers form an arithmetic sequence with difference $" + str(m) + "$. Find the first and last."], sol)


def sqc2(r):
    a = r.randint(2, 6)
    rr = r.choice([2, 3])
    g = [a, a * rr, a * rr * rr]
    mid = F(g[0] + g[2], 2)
    k = mid - g[1]
    if k.denominator != 1 or k <= 0:
        return None
    p = (f"The numbers ${g[0]}$, ${g[1]}$, ${g[2]}$ form a geometric sequence. What number must be added to the middle term only "
         f"so that the three numbers form an arithmetic sequence?")
    sol = explain(
        "the amount to add to the middle term.",
        "in an arithmetic sequence of three terms, the middle term is the average of the outer two.",
        [
            f"The outer terms ${g[0]}$ and ${g[2]}$ stay the same, so the middle must become $\\frac{{{g[0]} + {g[2]}}}{{2}} = {num(mid).tex}$.",
            f"It is currently ${g[1]}$, so add ${num(mid).tex} - {g[1]} = {num(k).tex}$.",
            f"Check: ${g[0]}, {num(mid).tex}, {g[2]}$ has equal steps of ${num(mid - g[0]).tex}$.",
        ],
        f"${num(k).tex}$.",
        f"answering with the new middle term ${num(mid).tex}$ instead of the amount added.",
    )
    return (p, k, [k + 1, mid, g[2] - g[1], g[1] - g[0], k - 1 if k > 1 else k + 2], ["In an arithmetic sequence the middle term is the average of its neighbors."], sol)


def sqc3(r):
    a, d = r.randint(1, 5), r.randint(2, 4)
    n = r.randint(8, 25)
    s = n * (2 * a + (n - 1) * d) // 2
    A, B, Cq = d, 2 * a - d, -2 * s
    p = f"How many terms of the arithmetic sequence ${a}, {a + d}, {a + 2 * d}, \\ldots$ must be added to get a sum of ${s}$?"
    sol = explain(
        "the number of terms $n$.",
        "use the sum formula $S_n = \\frac{n}{2}\\big(2a_1 + (n - 1)d\\big)$ and solve for $n$.",
        [
            f"Here $a_1 = {a}$ and $d = {d}$: $\\frac{{n}}{{2}}\\big({2 * a} + {d}(n - 1)\\big) = {s}$.",
            f"Multiply by $2$ and expand: $n({2 * a} + {d}n - {d}) = {2 * s}$, so ${A}n^2 + {B}n - {2 * s} = 0$." if B >= 0 else f"Multiply by $2$ and expand: ${A}n^2 - {abs(B)}n - {2 * s} = 0$.",
            f"Try $n = {n}$: ${A} \\cdot {n * n} + ({B}) \\cdot {n} = {A * n * n + B * n} = {2 * s}$. It works. The other root is negative, so it is not a count.",
        ],
        f"${n}$ terms.",
        "solving for the last term instead of the number of terms.",
    )
    return (p, n, [n + 1, n - 1, s // (a + d), n + 2, 2 * n], ["Set $\\frac{n}{2}(2a + (n - 1)d)$ equal to the sum and solve."], sol)


b.fill_unique("basics", [sq1, sq2, sq3, sq4] + MORE[b.skill_id]["basics"], 901)
b.fill_unique("challenge", [sqc1, sqc2, sqc3] + MORE[b.skill_id]["challenge"], 902)


# ---------------------------------------------------------------- functions and operations
b = bank("alg_functions")


def fn1(r):
    a, bb, c = r.randint(1, 5), r.randint(-6, 6), r.randint(-5, 5)
    x = r.randint(-4, 6)
    ans = a * x * x + bb * x + c
    p = f"If $f(x) = {a if a > 1 else ''}x^2 {'+' if bb >= 0 else '-'} {abs(bb)}x {'+' if c >= 0 else '-'} {abs(c)}$, what is $f({x})$?"
    sol = explain(
        f"the output when the input is ${x}$.",
        "replace every $x$ with the number, in parentheses, then follow the order of operations.",
        [
            f"$f({x}) = {a}({x})^2 + ({bb})({x}) + ({c})$.",
            f"$({x})^2 = {x * x}$, so the first term is ${a * x * x}$. The second term is ${bb * x}$.",
            f"Add: ${a * x * x} + ({bb * x}) + ({c}) = {ans}$.",
        ],
        f"${ans}$.",
        "squaring a negative input without parentheses, like $-3^2 = -9$ instead of $(-3)^2 = 9$." if x < 0 else "forgetting to square the input before multiplying.",
    )
    return (p, ans, [a * x + bb * x + c, ans + 2 * bb, ans - c, -ans if ans else 3, a * x * x - bb * x + c], ["Substitute carefully, keeping track of signs."], sol)


def fn2(r):
    a, bb = r.randint(2, 5), r.randint(-6, 6)
    c, d = r.randint(2, 5), r.randint(-6, 6)
    x = r.randint(-3, 5)
    inner = c * x + d
    ans = a * inner + bb
    other = c * (a * x + bb) + d
    p = f"Let $f(x) = {a}x {'+' if bb >= 0 else '-'} {abs(bb)}$ and $g(x) = {c}x {'+' if d >= 0 else '-'} {abs(d)}$. What is $f(g({x}))$?"
    sol = explain(
        f"$f$ applied to the output of $g({x})$.",
        "work from the inside out: compute $g$ first, then feed its answer into $f$.",
        [f"$g({x}) = {c} \\cdot ({x}) + ({d}) = {inner}$.", f"$f({inner}) = {a} \\cdot ({inner}) + ({bb}) = {ans}$."],
        f"${ans}$.",
        f"computing $g(f({x}))$ instead, which gives ${other}$. The function written closest to the input goes first.",
    )
    return (p, ans, [other, a * x + bb + inner, ans + a, inner, (a * x + bb) * inner], ["Work from the inside out: find $g(" + str(x) + ")$ first."], sol)


def fn3(r):
    k1, k2 = r.randint(1, 3), r.randint(1, 3)
    a, bb = r.randint(2, 7), r.randint(2, 7)
    c = r.randint(1, 5)
    op = lambda x, y: x * y + k1 * x - k2 * y
    inner = op(a, bb)
    ans = op(inner, c)
    other = op(a, op(bb, c))
    p = f"Define $x \\diamond y = xy + {k1 if k1 > 1 else ''}x - {k2 if k2 > 1 else ''}y$. What is $({a} \\diamond {bb}) \\diamond {c}$?"
    sol = explain(
        "the result of applying the operation twice.",
        "a made up operation is just a rule: plug the left number in for $x$ and the right number in for $y$. Do the parentheses first.",
        [
            f"Inner: ${a} \\diamond {bb} = {a} \\cdot {bb} + {k1} \\cdot {a} - {k2} \\cdot {bb} = {a * bb} + {k1 * a} - {k2 * bb} = {inner}$.",
            f"Outer: ${inner} \\diamond {c} = {inner} \\cdot {c} + {k1} \\cdot {inner} - {k2} \\cdot {c} = {inner * c} + {k1 * inner} - {k2 * c} = {ans}$.",
        ],
        f"${ans}$.",
        f"grouping the other way, ${a} \\diamond ({bb} \\diamond {c})$, which gives ${other}$. This operation is not associative.",
    )
    return (p, ans, [other, inner, inner * c, ans + c, ans - k1], ["Compute the inside operation first."], sol)


def fn4(r):
    a, bb = r.randint(2, 7), r.randint(-10, 10)
    y = r.randint(-10, 30)
    x = F(y - bb, a)
    p = f"If $f(x) = {a}x {'+' if bb >= 0 else '-'} {abs(bb)}$, what is $f^{{-1}}({y})$?"
    sol = explain(
        f"the input that $f$ sends to ${y}$.",
        "$f^{-1}(y)$ answers the question: what $x$ gives $f(x) = y$? It is not $\\frac{1}{f(y)}$.",
        [
            f"Set $f(x) = {y}$: ${a}x {'+' if bb >= 0 else '-'} {abs(bb)} = {y}$.",
            f"Solve: ${a}x = {y - bb}$, so $x = {num(x).tex}$.",
            f"Check: $f\\left({num(x).tex}\\right) = {a} \\cdot {num(x).tex} {'+' if bb >= 0 else '-'} {abs(bb)} = {y}$.",
        ],
        f"${num(x).tex}$.",
        f"computing $f({y}) = {a * y + bb}$ instead of undoing $f$.",
    )
    return (p, x, [a * y + bb, F(y + bb, a), F(1, a * y + bb) if a * y + bb else 7, x + 1, F(y, a)], ["$f^{-1}(y)$ is the input that gives output $y$."], sol)


def fnc1(r):
    k = r.randint(2, 3)
    c = r.randint(1, 6)
    a, bb = r.randint(1, 4), r.randint(-5, 5)
    t = r.randint(-3, 6)
    g = lambda x: a * x + bb
    gt, gs = g(t), g(c - t)
    val = F(gt - k * gs, 1 - k * k)
    other = gs - k * val
    rhs = f"{a if a > 1 else ''}x {'+' if bb >= 0 else '-'} {abs(bb)}"
    p = f"A function satisfies $f(x) + {k}f({c} - x) = {rhs}$ for all real $x$. What is $f({t})$?"
    sol = explain(
        f"$f({t})$, with no formula for $f$ given.",
        f"plugging in $x = {t}$ involves $f({t})$ and $f({c - t})$. Plugging in $x = {c - t}$ involves the same two values. Two equations, two unknowns.",
        [
            f"At $x = {t}$: $f({t}) + {k}f({c - t}) = {gt}$.",
            f"At $x = {c - t}$: $f({c - t}) + {k}f({t}) = {gs}$.",
            f"Let $P = f({t})$ and $Q = f({c - t})$. From the second equation, $Q = {gs} - {k}P$.",
            f"Substitute into the first: $P + {k}({gs} - {k}P) = {gt}$, so $P - {k * k}P = {gt} - {par(k * gs)}$, that is ${1 - k * k}P = {gt - k * gs}$.",
            f"$P = {num(val).tex}$. (Check: $Q = {num(other).tex}$ and ${num(val).tex} + {k}({num(other).tex}) = {gt}$.)",
        ],
        f"$f({t}) = {num(val).tex}$.",
        f"plugging $x = {t}$ into the right side and stopping, which gives ${gt}$.",
    )
    return (p, val, [-val if val else 2, val + 1, F(gt, 1 + k), F(gt, k), val - 1], [f"Replace $x$ with ${c} - x$ to get a second equation, then solve the system."], sol)


def fnc2(r):
    x0 = r.choice([2, 3, 4, F(1, 2), -1, 5, -2, F(1, 3)])
    n = r.randint(20, 200)
    f = lambda x: 1 / (1 - F(x))
    seq = [F(x0)]
    for _ in range(3):
        seq.append(f(seq[-1]))
    ans = seq[n % 3]
    p = f"Let $f(x) = \\dfrac{{1}}{{1 - x}}$. What is $f$ applied {n} times to ${num(F(x0)).tex}$?"
    sol = explain(
        f"the result after ${n}$ applications of $f$.",
        "apply $f$ a few times by hand and look for a repeating cycle.",
        [
            f"$f({num(seq[0]).tex}) = \\frac{{1}}{{1 - ({num(seq[0]).tex})}} = {num(seq[1]).tex}$.",
            f"$f({num(seq[1]).tex}) = {num(seq[2]).tex}$.",
            f"$f({num(seq[2]).tex}) = {num(seq[3]).tex}$, back where we started. So the values repeat every $3$ applications.",
            f"${n} = 3 \\cdot {n // 3} + {n % 3}$, so ${n}$ applications act like ${n % 3}$.",
            f"After ${n % 3}$ application{'s' if n % 3 != 1 else ''}, the value is ${num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        "being off by one in the cycle. Zero applications gives the starting value.",
    )
    return (p, ans, [seq[(n + 1) % 3], seq[(n + 2) % 3], -ans if ans != 0 else 3, ans + 1, 1], ["Apply $f$ a few times and look for a pattern."], sol)


def fnc3(r):
    c = r.randint(1, 5)
    n = r.randint(5, 15)
    ans = n * c + n * (n - 1) // 2
    vals = [c]
    for a in range(1, 4):
        vals.append(vals[-1] + c + a)
    p = f"A function satisfies $f(1) = {c}$ and $f(a + b) = f(a) + f(b) + ab$ for all positive integers $a$ and $b$. What is $f({n})$?"
    sol = explain(
        f"$f({n})$ from a rule that relates values at different inputs.",
        "set $b = 1$ to step from $f(a)$ to $f(a + 1)$, then add up all the steps.",
        [
            f"With $b = 1$: $f(a + 1) = f(a) + f(1) + a = f(a) + {c} + a$.",
            f"So $f(2) = {vals[1]}$, $f(3) = {vals[2]}$, $f(4) = {vals[3]}$, and so on.",
            f"Going from $f(1)$ to $f({n})$ takes ${n - 1}$ steps, each adding ${c}$ plus $a$ for $a = 1, \\ldots, {n - 1}$.",
            f"$f({n}) = {c} + {n - 1} \\cdot {c} + (1 + 2 + \\cdots + {n - 1}) = {n * c} + {n * (n - 1) // 2} = {ans}$.",
        ],
        f"${ans}$.",
        f"assuming $f$ is linear, $f(n) = {c}n$. The extra $ab$ term adds more each step.",
    )
    return (p, ans, [n * c, ans + n, n * c + n * n, ans - c, n * (c + n)], ["Find $f(2)$, $f(3)$, $f(4)$ by setting $b = 1$, then look for a pattern."], sol)


b.fill_unique("basics", [fn1, fn2, fn3, fn4] + MORE[b.skill_id]["basics"], 1001)
b.fill_unique("challenge", [fnc1, fnc2, fnc3] + MORE[b.skill_id]["challenge"], 1002)
