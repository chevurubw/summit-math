"""Mock exam families shared by the AMC 10 and AMC 12, difficulty levels 1 to 3."""
import math
from collections import Counter
from fractions import Fraction as F

from common import NAMES, comb, explain, num, text_choice, var
from mock_common import PLACES, family, pi_mult


def ordinal(n):
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


# ============================================================ LEVEL 1 (AMC 10 #1 to 5)


@family("l1_alg_diffsq", 1, "algebra", "alg_factoring")
def _(r):
    n = r.randint(1500, 2100)
    m = n - r.randint(3, 40)
    k = r.choice([1, 2, 4])
    ans = F(n * n - m * m, k * (n - m))
    if ans.denominator != 1:
        return None
    d = k * (n - m)
    sol = explain(
        f"the value of a fraction whose top is ${n}^2 - {m}^2$. Squaring four digit numbers by hand would take far too long, so look for a shortcut.",
        "a difference of two squares factors: $a^2 - b^2 = (a - b)(a + b)$.",
        [
            f"Factor the top with $a = {n}$ and $b = {m}$: $$ {n}^2 - {m}^2 = ({n} - {m})({n} + {m}) = {n - m} \\cdot {n + m}. $$",
            f"The bottom is ${d}$" + (f", which is ${k} \\cdot {n - m}$." if k > 1 else ", the same as $n - m$."),
            f"Cancel the common factor ${n - m}$: $$ \\frac{{{n - m} \\cdot {n + m}}}{{{d}}} = \\frac{{{n + m}}}{{{k}}} = {ans}. $$",
        ],
        f"the value is ${ans}$.",
        f"stopping after factoring, or forgetting to divide ${n + m}$ by ${k}$." if k > 1 else f"choosing ${n - m}$, the difference, instead of the sum ${n + m}$.",
    )
    p = f"What is the value of $\\dfrac{{{n}^2 - {m}^2}}{{{d}}}$?"
    return (p, ans, [n - m, F(n + m, 2 * k) if k == 1 else n + m, ans + 1, ans - k, (n * n - m * m) // 1000],
            ["Factor the top as a difference of squares."], sol)


@family("l1_alg_shopping", 1, "algebra", "alg_linear")
def _(r):
    a, b = r.randint(2, 9), r.randint(10, 25)
    x, y = r.randint(2, 9), r.randint(2, 9)
    total = a * x + b * y
    nm = r.choice(NAMES)
    place = r.choice(PLACES)
    p = (f"At {place}, pencils cost ${a}$ cents each and notebooks cost ${b}$ cents each. {nm} buys ${x}$ pencils and some notebooks "
         f"and pays $\\${total / 100:.2f}$ in all. How many notebooks did {nm} buy?")
    sol = explain(
        f"the number of notebooks {nm} bought. Call it $n$.",
        "work entirely in cents so every number is a whole number, then subtract the part you already know.",
        [
            f"Convert the total to cents: $\\${total / 100:.2f} = {total}$ cents.",
            f"The pencils cost ${x} \\cdot {a} = {a * x}$ cents.",
            f"That leaves ${total} - {a * x} = {total - a * x}$ cents for notebooks, so $$ {b}n = {total - a * x}. $$",
            f"Divide: $n = \\frac{{{total - a * x}}}{{{b}}} = {y}$.",
        ],
        f"{nm} bought ${y}$ notebooks.",
        "mixing dollars and cents. Pick one unit before doing any arithmetic.",
    )
    return (p, y, [y + 1, y - 1, x, total // b if total // b != y else y + 2, y + 3], ["Work in cents."], sol)


@family("l1_alg_percent", 1, "algebra", "alg_ratios")
def _(r):
    up, down = r.choice([(20, 20), (25, 20), (10, 10), (50, 20), (25, 40), (20, 25), (40, 25), (30, 10)])
    final = F(100 + up, 100) * F(100 - down, 100) * 100
    mid = 100 + up
    cut = F(mid * down, 100)
    p = f"The price of a jacket is raised by ${up}\\%$. Later the new price is lowered by ${down}\\%$. The final price is what percent of the original price?"
    sol = explain(
        "the final price as a percent of the starting price.",
        "the second change is a percent of the new price, not of the original. Using a starting price of $\\$100$ makes percents easy to read.",
        [
            "Start with a price of $\\$100$.",
            f"Raising by ${up}\\%$ adds $\\${up}$: the price becomes $\\${mid}$.",
            f"Lowering by ${down}\\%$ removes ${down}\\%$ of $\\${mid}$, which is $\\${num(cut).tex}$. The price becomes $$ {mid} - {num(cut).tex} = {num(final).tex}. $$",
            f"We started at $100$, so the final price is ${num(final).tex}\\%$ of the original.",
        ],
        f"${num(final).tex}\\%$.",
        f"adding and subtracting the percents to get ${100 + up - down}\\%$. The ${down}\\%$ cut is taken from the larger price, so it removes more than $\\${down}$.",
    )
    return (p, final, [100 + up - down, 100, final + 5, final - 4, 100 - down], ["Use a starting price of $100$."], sol)


@family("l1_geo_ratio_angles", 1, "geometry", "geo_angles")
def _(r):
    while True:
        a, b, c = sorted(r.sample(range(1, 10), 3))
        if 180 % (a + b + c) == 0:
            break
    u = 180 // (a + b + c)
    ask = r.choice(["largest", "smallest"])
    ans = c * u if ask == "largest" else a * u
    p = f"The angles of a triangle are in the ratio ${a} : {b} : {c}$. What is the measure of the {ask} angle, in degrees?"
    sol = explain(
        f"the {ask} angle of the triangle.",
        "a ratio $a : b : c$ means the angles are $ak$, $bk$ and $ck$ for some number $k$, and the angles of a triangle add to $180^\\circ$.",
        [
            f"Write the angles as ${a}k$, ${b}k$ and ${c}k$.",
            f"Add them: $$ {a}k + {b}k + {c}k = {a + b + c}k = 180, $$ so $k = {u}$.",
            f"The angles are ${a * u}^\\circ$, ${b * u}^\\circ$ and ${c * u}^\\circ$. Check: ${a * u} + {b * u} + {c * u} = 180$.",
        ],
        f"the {ask} angle is ${ans}^\\circ$.",
        f"answering with $k = {u}$ itself, or picking the {'smallest' if ask == 'largest' else 'largest'} angle.",
    )
    return (p, ans, [b * u, (a * u if ask == "largest" else c * u), ans + u, 180 - ans, u], ["The three angles add to $180^\\circ$."], sol)


@family("l1_geo_ladder", 1, "geometry", "geo_right")
def _(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)])
    k = r.randint(1, 3)
    a, b, c = a * k, b * k, c * k
    if c > 30:
        return None
    p = f"A ${c}$ foot ladder leans against a wall. Its foot is ${a}$ feet from the base of the wall. How high up the wall does the ladder reach, in feet?"
    sol = explain(
        "the height $h$ where the top of the ladder touches the wall.",
        "the wall, the ground and the ladder form a right triangle. The ladder is the hypotenuse.",
        [
            f"The legs are the ground distance ${a}$ and the height $h$; the hypotenuse is ${c}$.",
            f"Pythagorean Theorem: $$ {a}^2 + h^2 = {c}^2 \\quad\\Rightarrow\\quad {a * a} + h^2 = {c * c}. $$",
            f"So $h^2 = {c * c} - {a * a} = {b * b}$ and $h = {b}$.",
        ],
        f"the ladder reaches ${b}$ feet up the wall.",
        f"adding the squares instead of subtracting. The ladder is the longest side, so $h$ must be less than ${c}$.",
    )
    return (p, b, [c - a, c + a, b + 1, b - 1, (a + c) // 2], ["The ladder, the wall and the ground form a right triangle."], sol)


@family("l1_geo_rect_square", 1, "geometry", "geo_area")
def _(r):
    s = r.randint(4, 15)
    w = r.randint(2, s * 2)
    if (s * s) % w or s * s // w == w:
        return None
    l = s * s // w
    ans = 2 * (w + l)
    p = f"A rectangle has width ${w}$ and the same area as a square with side ${s}$. What is the perimeter of the rectangle?"
    sol = explain(
        "the perimeter of the rectangle, which needs both its width and its length.",
        "find the area from the square, then use it to get the missing length.",
        [
            f"The square's area is ${s}^2 = {s * s}$.",
            f"The rectangle has the same area, so its length $L$ satisfies ${w} \\cdot L = {s * s}$, giving $L = {l}$.",
            f"Perimeter: $$ 2({w} + {l}) = 2 \\cdot {w + l} = {ans}. $$",
        ],
        f"the perimeter is ${ans}$.",
        f"giving the square's perimeter (${4 * s}$) or the area (${s * s}$). Same area does not mean same perimeter.",
    )
    return (p, ans, [4 * s, w + l, s * s, ans + 2, ans - 4], ["Find the rectangle's length first."], sol)


@family("l1_nt_multiples", 1, "number_theory", "nt_divisibility")
def _(r):
    lo, hi = r.randint(10, 60), r.randint(150, 400)
    k, m = r.choice([(3, 5), (4, 6), (5, 7), (6, 9), (3, 7), (4, 10)])
    cnt = sum(1 for x in range(lo, hi + 1) if x % k == 0 and x % m != 0)
    total_k = sum(1 for x in range(lo, hi + 1) if x % k == 0)
    L = math.lcm(k, m)
    both = total_k - cnt
    first_k = next(x for x in range(lo, hi + 1) if x % k == 0)
    last_k = max(x for x in range(lo, hi + 1) if x % k == 0)
    p = f"How many integers from ${lo}$ to ${hi}$, inclusive, are multiples of ${k}$ but not multiples of ${m}$?"
    sol = explain(
        f"how many numbers in the range are multiples of ${k}$, after throwing out the ones that are also multiples of ${m}$.",
        f"count all multiples of ${k}$, then subtract those that are multiples of both. A number is a multiple of both ${k}$ and ${m}$ exactly when it is a multiple of $\\operatorname{{lcm}}({k}, {m}) = {L}$.",
        [
            f"Multiples of ${k}$ in the range run from ${first_k}$ to ${last_k}$: that is $\\frac{{{last_k} - {first_k}}}{{{k}}} + 1 = {total_k}$ numbers.",
            f"Multiples of ${L}$ in the range: there are ${both}$ of them.",
            f"Subtract: ${total_k} - {both} = {cnt}$.",
        ],
        f"${cnt}$ integers.",
        f"subtracting the multiples of ${m}$ instead of the multiples of ${L}$. Only numbers that are multiples of both should be removed.",
    )
    return (p, cnt, [total_k, cnt + 1, cnt - 1, total_k - cnt, cnt + 2], [f"Count the multiples of ${k}$, then remove those that are also multiples of ${m}$."], sol)


@family("l1_nt_digitsum", 1, "number_theory", "nt_divisibility")
def _(r):
    n = r.randint(8, 30)
    k = r.randint(2, 999)
    v = 10 ** n - k
    ans = sum(int(d) for d in str(v))
    L = len(str(k))
    tail_s = str(10 ** L - k).zfill(L)
    nines = n - L
    p = f"What is the sum of the digits of $10^{{{n}}} - {k}$?"
    sol = explain(
        f"the digit sum of a ${n}$ digit number.",
        "look at what subtracting a small number from a power of ten does to the digits.",
        [
            f"Try a small case: $10^6 - {k} = {10 ** 6 - k}$. Most digits become $9$, and only the last few change.",
            f"Here ${k}$ has ${L}$ digit{'s' if L > 1 else ''}, so the number ends in $10^{{{L}}} - {k} = {tail_s}$, and the ${nines}$ digits before that are all $9$.",
            f"Add: $$ {nines} \\cdot 9 + ({' + '.join(tail_s)}) = {9 * nines} + {sum(map(int, tail_s))} = {ans}. $$",
        ],
        f"the digit sum is ${ans}$.",
        f"counting ${n}$ nines instead of ${nines}$. The number has ${n}$ digits in all, and the last ${L}$ are not all nines.",
    )
    return (p, ans, [9 * n, ans + 9, ans - 9, 9 * (n - 1), ans + 1], ["Write out $10^n - k$ for a small $n$ first and look at the pattern."], sol)


@family("l1_nt_weekday", 1, "number_theory", "nt_modular")
def _(r):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    start = r.randrange(7)
    n = r.randint(40, 1000)
    ans = (start + n) % 7
    choices = [text_choice(days[(ans + d) % 7], d) for d in (1, 2, 3, 6)]
    rem = n % 7
    p = f"Today is {days[start]}. What day of the week will it be ${n}$ days from today?"
    sol = explain(
        f"the weekday ${n}$ days after {days[start]}.",
        "every $7$ days the weekday repeats, so only the remainder when dividing by $7$ matters.",
        [
            f"Divide: ${n} = 7 \\cdot {n // 7} + {rem}$.",
            f"The ${n // 7}$ full weeks bring us back to {days[start]}.",
            (f"Count ${rem}$ more day{'s' if rem != 1 else ''} forward from {days[start]}: " + ", ".join(days[(start + i) % 7] for i in range(1, rem + 1)) + ".") if rem else "There are no extra days, so it is the same weekday.",
        ],
        f"{days[ans]}.",
        "counting today as day $1$. Day $1$ is tomorrow.",
    )
    return (p, text_choice(days[ans], 0), choices, ["Days of the week repeat every $7$ days."], sol, False)


@family("l1_cp_outfits", 1, "counting_probability", "cp_counting")
def _(r):
    s, pnt, h = r.randint(3, 8), r.randint(2, 6), r.randint(2, 5)
    ans = s * pnt * (h + 1)
    nm = r.choice(NAMES)
    p = f"{nm} has ${s}$ shirts, ${pnt}$ pairs of pants, and ${h}$ hats. An outfit is a shirt and a pair of pants, with or without one hat. How many outfits are possible?"
    sol = explain(
        "the number of different outfits.",
        "Multiplication Principle: when you make several independent choices, multiply the number of options for each.",
        [
            f"Shirt: ${s}$ choices. Pants: ${pnt}$ choices.",
            f"Hat: ${h}$ hats, plus the option of no hat, so ${h + 1}$ choices.",
            f"Multiply: $$ {s} \\cdot {pnt} \\cdot {h + 1} = {ans}. $$",
        ],
        f"${ans}$ outfits.",
        f"forgetting the no hat option, which gives ${s * pnt * h}$.",
    )
    return (p, ans, [s * pnt * h, s + pnt + h, s * pnt + h, ans + s * pnt, s * pnt], ["Not wearing a hat counts as one more hat choice."], sol)


@family("l1_cp_couples", 1, "counting_probability", "cp_combinations")
def _(r):
    n = r.randint(4, 12)
    ans = comb(2 * n, 2) - n
    p = f"At a party there are ${n}$ married couples. Everyone shakes hands once with every other person except their own spouse. How many handshakes are there?"
    sol = explain(
        "the number of handshakes, where each handshake is a pair of people.",
        "count every possible pair, then remove the pairs that do not shake hands.",
        [
            f"There are ${2 * n}$ people. The number of pairs is $$ \\binom{{{2 * n}}}{{2}} = \\frac{{{2 * n} \\cdot {2 * n - 1}}}{{2}} = {comb(2 * n, 2)}. $$",
            f"The ${n}$ married couples do not shake hands, so remove ${n}$ pairs.",
            f"${comb(2 * n, 2)} - {n} = {ans}$.",
        ],
        f"${ans}$ handshakes.",
        f"computing ${2 * n} \\cdot {2 * n - 2}$ and forgetting to divide by $2$. Each handshake involves two people, so that way counts it twice.",
    )
    return (p, ans, [comb(2 * n, 2), ans - n, 2 * n * (2 * n - 2), n * (n - 1), ans + 1], ["Count all pairs of people, then remove the spouses."], sol)


@family("l1_cp_dice_sum", 1, "counting_probability", "cp_probability")
def _(r):
    s = r.randint(3, 11)
    pairs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s]
    ways = len(pairs)
    pr = F(ways, 36)
    p = f"Two fair six sided dice are rolled. What is the probability that the sum is ${s}$?"
    sol = explain(
        f"the chance that the two dice add to ${s}$.",
        "there are $6 \\times 6 = 36$ equally likely ordered outcomes. Count the ones that work.",
        [
            "Treat the dice as different (first die, second die), so $(1, 2)$ and $(2, 1)$ are different outcomes.",
            f"List the pairs adding to ${s}$: " + ", ".join(f"$({a}, {b})$" for a, b in pairs) + f". That is ${ways}$ outcomes.",
            f"Probability $= \\frac{{{ways}}}{{36}} = {num(pr).tex}$.",
        ],
        f"${num(pr).tex}$.",
        "treating $(1, 2)$ and $(2, 1)$ as the same outcome. Then the outcomes are no longer equally likely.",
    )
    return (p, pr, [F(1, 6), F(1, 36), F(ways + 1, 36), F(ways, 18) if F(ways, 18) != pr else F(1, 9), F(1, 11)], ["List the pairs that give this sum."], sol)


# ============================================================ LEVEL 2 (AMC 10 #6 to 10, AMC 12 #1 to 5)


@family("l2_alg_avg_removed", 2, "algebra", "alg_stats")
def _(r):
    n = r.randint(6, 15)
    m1 = r.randint(20, 80)
    x = r.randint(5, 150)
    if (n * m1 - x) % (n - 1):
        return None
    m2 = (n * m1 - x) // (n - 1)
    if m2 == m1:
        return None
    p = f"The average of ${n}$ numbers is ${m1}$. When one of the numbers is removed, the average of the remaining numbers is ${m2}$. What number was removed?"
    sol = explain(
        "the number that was taken away.",
        "an average hides the total: total $=$ average $\\times$ count. Compare the totals before and after.",
        [
            f"Before: ${n}$ numbers with average ${m1}$, so the total is ${n} \\cdot {m1} = {n * m1}$.",
            f"After: ${n - 1}$ numbers with average ${m2}$, so the total is ${n - 1} \\cdot {m2} = {(n - 1) * m2}$.",
            f"The removed number is the difference: ${n * m1} - {(n - 1) * m2} = {x}$.",
        ],
        f"the removed number is ${x}$.",
        f"subtracting the averages (${m1} - {m2}$). Averages cannot be subtracted directly; work with totals.",
    )
    return (p, x, [m1 - m2, abs(n * (m1 - m2)), x + (n - 1), m1 + m2, x - 1], ["Compare the totals before and after."], sol)


@family("l2_alg_meet", 2, "algebra", "alg_rates")
def _(r):
    a, b = r.randint(30, 70), r.randint(30, 70)
    t = F(r.randint(1, 12), 4)
    d = (a + b) * t
    if d.denominator != 1:
        return None
    gap = r.choice([0, 15, 30])
    d = int(d) + a * F(gap, 60)
    if d.denominator != 1:
        return None
    d = int(d)
    head = a * F(gap, 60)
    rest = d - head
    t2 = rest / (a + b)
    if (t2 * 60).denominator != 1:
        return None
    ans = gap + int(t2 * 60)
    n1, n2 = r.sample(NAMES, 2)
    later = f" {n2} leaves ${gap}$ minutes after {n1}." if gap else " They leave at the same time."
    p = (f"{n1} and {n2} live ${d}$ miles apart and drive toward each other, {n1} at ${a}$ mph and {n2} at ${b}$ mph.{later} "
         f"How many minutes after {n1} leaves do they meet?")
    steps = []
    if gap:
        steps.append(f"For the first ${gap}$ minutes ($= {num(F(gap, 60)).tex}$ hour) only {n1} drives, covering ${a} \\cdot {num(F(gap, 60)).tex} = {num(head).tex}$ miles. The gap shrinks to ${d} - {num(head).tex} = {num(rest).tex}$ miles.")
    steps.append(f"Once both are driving toward each other, the gap closes at ${a} + {b} = {a + b}$ miles per hour.")
    steps.append(f"Time to close the {'remaining ' if gap else ''}gap: $\\frac{{{num(rest).tex}}}{{{a + b}}} = {num(t2).tex}$ hours $= {int(t2 * 60)}$ minutes.")
    if gap:
        steps.append(f"Add the head start: ${gap} + {int(t2 * 60)} = {ans}$ minutes after {n1} leaves.")
    sol = explain(
        f"how long after {n1} starts the two cars meet.",
        "when two objects move toward each other, the distance between them shrinks at the sum of their speeds.",
        steps,
        f"they meet ${ans}$ minutes after {n1} leaves.",
        f"forgetting that {n1} drove alone for ${gap}$ minutes first, or measuring time from when {n2} leaves." if gap else "dividing by one speed instead of the sum of the speeds.",
    )
    return (p, ans, [int(F(d, a + b) * 60), ans + gap if gap else ans + 10, ans - 5, int(F(d * 60, max(a, b))), ans + 15],
            ["Once both are driving, the gap closes at the sum of their speeds."], sol)


@family("l2_alg_ages", 2, "algebra", "alg_linear")
def _(r):
    y = r.randint(4, 15)
    x = r.randint(y + 5, 50)
    k1 = r.randint(2, 6)
    if (x + k1) % (y + k1):
        return None
    m = (x + k1) // (y + k1)
    if m < 2:
        return None
    k2 = r.randint(1, y - 1)
    if (x - k2) % (y - k2):
        return None
    m2 = (x - k2) // (y - k2)
    if m2 <= m or m2 > 6:
        return None
    n1, n2 = r.sample(NAMES, 2)
    u, w = var(n1), var(n2)
    p = (f"In ${k1}$ years, {n1} will be ${m}$ times as old as {n2}. ${k2}$ years ago, {n1} was ${m2}$ times as old as {n2}. "
         f"How old is {n1} now?")
    c1 = m * k1 - k1
    c2 = m2 * k2 - k2
    sol = explain(
        f"{n1}'s age today. Let ${u}$ be {n1}'s age now and ${w}$ be {n2}'s age now.",
        "turn each sentence into an equation, then solve the system.",
        [
            f"In ${k1}$ years they will be ${u} + {k1}$ and ${w} + {k1}$: $$ {u} + {k1} = {m}({w} + {k1}) \\quad\\Rightarrow\\quad {u} = {m}{w} + {c1}. $$",
            f"${k2}$ years ago they were ${u} - {k2}$ and ${w} - {k2}$: $$ {u} - {k2} = {m2}({w} - {k2}) \\quad\\Rightarrow\\quad {u} = {m2}{w} - {c2}. $$",
            f"Set the two expressions for ${u}$ equal: ${m}{w} + {c1} = {m2}{w} - {c2}$, so ${m2 - m}{w} = {c1 + c2}$ and ${w} = {y}$.",
            f"Then ${u} = {m} \\cdot {y} + {c1} = {x}$. Check: in ${k1}$ years they are ${x + k1}$ and ${y + k1}$, and ${x + k1} = {m} \\cdot {y + k1}$.",
        ],
        f"{n1} is ${x}$ now.",
        f"adding ${k1}$ years to only one person's age. Time passes for both people.",
    )
    return (p, x, [y, x + k1, x - k2, x + y, x + 1], ["Let the current ages be unknowns and write two equations."], sol)


@family("l2_geo_square_circle", 2, "geometry", "geo_circles")
def _(r):
    from common import C
    s = r.choice([2, 4, 6, 8, 10, 12])
    kind = r.choice(["in", "out"])
    if kind == "in":
        p = f"A circle is inscribed in a square with side length ${s}$. What is the area of the region inside the square but outside the circle?"
        k = F(s * s, 4)
        ans = C(f"{s * s} - {pi_mult(k).tex}", s * s - math.pi * float(k))
        wrong = [C(f"{s * s} - {pi_mult(s * s).tex}", s * s - math.pi * s * s), C(f"{s * s} - {pi_mult(F(s * s, 2)).tex}", s * s - math.pi * s * s / 2),
                 C(f"{pi_mult(k).tex} - {s}", math.pi * float(k) - s), C(f"{4 * s} - {pi_mult(s).tex}", 4 * s - math.pi * s)]
        sol = explain(
            "the area of the four corner pieces between the square and the circle.",
            "shaded area $=$ (big shape) $-$ (small shape). An inscribed circle touches all four sides, so its diameter equals the side of the square.",
            [
                f"Square: area ${s}^2 = {s * s}$.",
                f"Circle: diameter ${s}$, so radius ${num(F(s, 2)).tex}$ and area $\\pi \\cdot {num(F(s, 2)).tex}^2 = {pi_mult(k).tex}$.",
                f"Subtract: ${ans.tex}$.",
            ],
            f"${ans.tex}$.",
            f"using ${s}$ as the radius. ${s}$ is the diameter.",
        )
    else:
        p = f"A square with side length ${s}$ is inscribed in a circle. What is the area of the region inside the circle but outside the square?"
        k = F(s * s, 2)
        ans = C(f"{pi_mult(k).tex} - {s * s}", math.pi * float(k) - s * s)
        wrong = [C(f"{pi_mult(F(s * s, 4)).tex} - {s * s}", math.pi * s * s / 4 - s * s + 100), C(f"{pi_mult(s * s).tex} - {s * s}", math.pi * s * s - s * s),
                 C(f"{s * s} - {pi_mult(F(s * s, 4)).tex}", s * s - math.pi * s * s / 4), C(f"{pi_mult(2 * s).tex} - {s * s}", 2 * math.pi * s - s * s)]
        sol = explain(
            "the area of the four curved pieces between the circle and the square.",
            "shaded area $=$ (circle) $-$ (square). A square inscribed in a circle has its diagonal as a diameter.",
            [
                f"Square: area ${s}^2 = {s * s}$, and its diagonal is ${s}\\sqrt{{2}}$.",
                f"Circle: diameter ${s}\\sqrt{{2}}$, so $r = \\frac{{{s}\\sqrt{{2}}}}{{2}}$ and $r^2 = \\frac{{{2 * s * s}}}{{4}} = {num(k).tex}$. The area is ${pi_mult(k).tex}$.",
                f"Subtract: ${ans.tex}$.",
            ],
            f"${ans.tex}$.",
            "using half the side length as the radius. That circle would fit inside the square, not around it.",
        )
    return (p, ans, wrong, ["Find the circle's radius from the square."], sol, False)


@family("l2_geo_shoelace", 2, "geometry", "geo_coordinate")
def _(r):
    pts = [(r.randint(-6, 8), r.randint(-6, 8)) for _ in range(3)]
    (x1, y1), (x2, y2), (x3, y3) = pts
    a2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if a2 == 0:
        return None
    ans = F(a2, 2)
    s1 = x1 * y2 + x2 * y3 + x3 * y1
    s2 = y1 * x2 + y2 * x3 + y3 * x1
    p = f"What is the area of the triangle with vertices $({x1}, {y1})$, $({x2}, {y2})$, and $({x3}, {y3})$?"
    sol = explain(
        "the area of a triangle given only its corners.",
        "the Shoelace Formula: for vertices $(x_1, y_1), (x_2, y_2), (x_3, y_3)$, the area is $\\frac{1}{2}\\left|(x_1y_2 + x_2y_3 + x_3y_1) - (y_1x_2 + y_2x_3 + y_3x_1)\\right|$.",
        [
            f"First sum: ${x1} \\cdot {y2} + {x2} \\cdot {y3} + {x3} \\cdot {y1} = {s1}$.",
            f"Second sum: ${y1} \\cdot {x2} + {y2} \\cdot {x3} + {y3} \\cdot {x1} = {s2}$.",
            f"Area $= \\frac{{1}}{{2}}\\left|{s1} - ({s2})\\right| = \\frac{{{a2}}}{{2}} = {num(ans).tex}$.",
        ],
        f"the area is ${num(ans).tex}$.",
        f"forgetting the $\\frac{{1}}{{2}}$, which gives ${a2}$. To double check, draw a box around the triangle and subtract the three right triangles outside it.",
    )
    return (p, ans, [a2, ans + 1, ans + F(1, 2), ans - 2 if ans > 2 else ans + 3, ans * 2 + 1], ["Use the shoelace formula, or box the triangle in a rectangle and subtract."], sol)


@family("l2_geo_polygon", 2, "geometry", "geo_angles")
def _(r):
    n = r.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
    kind = r.choice(["angle", "sides", "diag"])
    if kind == "angle":
        ang = F(180 * (n - 2), n)
        ext = 180 - ang
        p = f"Each interior angle of a regular polygon measures ${num(ang).tex}^\\circ$. How many sides does the polygon have?"
        sol = explain(
            "the number of sides, given one interior angle.",
            "exterior angles are easier: each exterior angle is $180^\\circ$ minus the interior angle, and the exterior angles of a convex polygon add to $360^\\circ$.",
            [
                f"Each exterior angle is $180 - {num(ang).tex} = {num(ext).tex}$ degrees.",
                f"All exterior angles are equal and add to $360$, so the number of sides is $$ \\frac{{360}}{{{num(ext).tex}}} = {n}. $$",
                f"Check: $\\frac{{180({n} - 2)}}{{{n}}} = {num(ang).tex}$.",
            ],
            f"${n}$ sides.",
            "dividing $360$ by the interior angle instead of the exterior angle.",
        )
        return (p, n, [n - 1, n + 1, n + 2, 2 * n if 2 * n < 60 else n - 2, n * 2 - 1], ["Each exterior angle is $180^\\circ$ minus the interior angle."], sol)
    if kind == "sides":
        ext = F(360, n)
        ans = 180 * (n - 2)
        p = f"Each exterior angle of a regular polygon measures ${num(ext).tex}^\\circ$. What is the sum of its interior angles, in degrees?"
        sol = explain(
            "the total of all interior angles.",
            "first find the number of sides from the exterior angle, then use the interior angle sum $180(n - 2)$.",
            [
                f"The exterior angles add to $360^\\circ$, so $n = \\frac{{360}}{{{num(ext).tex}}} = {n}$.",
                f"Interior angle sum: $180({n} - 2) = 180 \\cdot {n - 2} = {ans}$.",
            ],
            f"${ans}$ degrees.",
            "using $180n$. A polygon with $n$ sides splits into $n - 2$ triangles, not $n$.",
        )
        return (p, ans, [180 * n, 180 * (n - 1), 180 * (n - 3), 360 * n // 2 + 180, ans + 360], ["Find the number of sides first."], sol)
    d = n * (n - 3) // 2
    p = f"How many diagonals does a convex polygon with ${n}$ sides have?"
    sol = explain(
        "the number of diagonals: segments joining two corners that are not neighbors.",
        "count from each vertex, then fix the double counting.",
        [
            f"Each of the ${n}$ vertices has a diagonal to every vertex except itself and its two neighbors: ${n} - 3 = {n - 3}$ diagonals.",
            f"That gives ${n} \\cdot {n - 3} = {n * (n - 3)}$, but every diagonal was counted from both ends.",
            f"Divide by $2$: $\\frac{{{n * (n - 3)}}}{{2}} = {d}$.",
        ],
        f"${d}$ diagonals.",
        f"counting $\\binom{{{n}}}{{2}} = {n * (n - 1) // 2}$, which includes the ${n}$ sides.",
    )
    return (p, d, [n * (n - 1) // 2, n * (n - 3), d + n, d - n, n * n // 4], ["Each vertex connects to all but itself and its two neighbors."], sol)


@family("l2_nt_blink", 2, "number_theory", "nt_gcd")
def _(r):
    a, b = r.sample([4, 6, 8, 9, 10, 12, 14, 15, 18, 20], 2)
    L = math.lcm(a, b)
    T = r.randint(5, 30)
    ans = T * 60 // L + 1
    p = f"Two lights blink together at midnight. One blinks every ${a}$ seconds and the other every ${b}$ seconds. Counting midnight, how many times do they blink together in the first ${T}$ minutes after midnight (including the end of the ${T}$th minute)?"
    sol = explain(
        f"how many moments in the first ${T}$ minutes both lights blink at once.",
        f"both blink at times that are multiples of ${a}$ and of ${b}$, which means multiples of $\\operatorname{{lcm}}({a}, {b})$.",
        [
            f"$\\operatorname{{lcm}}({a}, {b}) = {L}$, so they blink together every ${L}$ seconds.",
            f"${T}$ minutes is ${T * 60}$ seconds. The shared blinks are at $0, {L}, {2 * L}, \\ldots$ up to ${T * 60}$.",
            f"After midnight there are $\\left\\lfloor \\frac{{{T * 60}}}{{{L}}} \\right\\rfloor = {T * 60 // L}$ of them. Add $1$ for midnight itself: ${ans}$.",
        ],
        f"${ans}$ times.",
        "multiplying the two periods instead of using the least common multiple, or forgetting to count midnight.",
    )
    return (p, ans, [ans - 1, T * 60 // (a * b) + 1, ans + 1, T * 60 // math.gcd(a, b) // 10, T * 60 // (a + b)], ["They blink together every $\\operatorname{lcm}$ of the two periods."], sol)


@family("l2_nt_divisors", 2, "number_theory", "nt_divisors")
def _(r):
    ps = r.sample([2, 3, 5, 7, 11], r.choice([2, 3]))
    es = [r.randint(1, 4) for _ in ps]
    N = 1
    for p_, e in zip(ps, es):
        N *= p_ ** e
    if N > 50000:
        return None
    d = 1
    for e in es:
        d *= e + 1
    ask = r.choice(["all", "odd"])
    fact = " \\cdot ".join(f"{p_}^{{{e}}}" for p_, e in zip(ps, es))
    if ask == "odd":
        if 2 not in ps:
            return None
        d = d // (es[ps.index(2)] + 1)
        p = f"How many positive odd divisors does ${N}$ have?"
        odd = [e for p_, e in zip(ps, es) if p_ != 2]
        steps = [f"Prime factorization: ${N} = {fact}$.",
                 "An odd divisor cannot use the prime $2$, so its exponent of $2$ must be $0$.",
                 "Each other prime can appear with any exponent from $0$ up to its power, so multiply: $$" + " \\cdot ".join(f"({e} + 1)" for e in odd) + f" = {d}.$$"]
        trap = "counting all divisors, including the even ones."
    else:
        p = f"How many positive divisors does ${N}$ have?"
        steps = [f"Prime factorization: ${N} = {fact}$.",
                 "A divisor picks an exponent for each prime, from $0$ up to the power in the factorization.",
                 "Multiply the number of choices: $$" + " \\cdot ".join(f"({e} + 1)" for e in es) + f" = {d}.$$"]
        trap = "adding the exponents, or forgetting the $+1$ (an exponent of $0$ is allowed)."
    sol = explain(f"the number of {'odd ' if ask == 'odd' else ''}divisors of ${N}$.", "every divisor is built from the same primes, each to a power no bigger than in the number itself.", steps, f"${d}$.", trap)
    return (p, d, [d + 1, d - 1, d * 2, sum(es), d + 2], ["Factor into primes and add one to each exponent."], sol)


@family("l2_nt_units", 2, "number_theory", "nt_powers")
def _(r):
    a, b = r.sample([2, 3, 7, 8, 13, 17, 19, 23, 27], 2)
    m, n = r.randint(20, 3000), r.randint(20, 3000)
    ua, ub = pow(a, m, 10), pow(b, n, 10)
    ans = (ua + ub) % 10

    def cyc(x):
        out, v = [], x % 10
        while v not in out:
            out.append(v)
            v = v * (x % 10) % 10
        return out
    ca, cb = cyc(a), cyc(b)
    pa = m % len(ca) or len(ca)
    pb = n % len(cb) or len(cb)
    p = f"What is the units digit of ${a}^{{{m}}} + {b}^{{{n}}}$?"
    sol = explain(
        "only the last digit of a huge sum.",
        "the units digit of a power depends only on the units digit of the base, and it repeats in a short cycle.",
        [
            f"Units digits of powers of ${a}$ cycle through ${', '.join(map(str, ca))}$ (length ${len(ca)}$). The exponent ${m}$ leaves remainder ${m % len(ca)}$ when divided by ${len(ca)}$, so it is position ${pa}$ in the cycle: ${a}^{{{m}}}$ ends in ${ua}$.",
            f"Units digits of powers of ${b}$ cycle through ${', '.join(map(str, cb))}$ (length ${len(cb)}$). The exponent ${n}$ is position ${pb}$: ${b}^{{{n}}}$ ends in ${ub}$.",
            f"Add the units digits: ${ua} + {ub} = {ua + ub}$, which ends in ${ans}$.",
        ],
        f"the units digit is ${ans}$.",
        "treating a remainder of $0$ as the first position. When the exponent is a multiple of the cycle length, use the last digit in the cycle.",
    )
    return (p, ans, [d for d in range(10) if d != ans][:5], ["Units digits of powers repeat in cycles of length at most 4."], sol)


@family("l2_cp_committee", 2, "counting_probability", "cp_combinations")
def _(r):
    g, b = r.randint(4, 8), r.randint(4, 8)
    k = r.randint(3, 4)
    ans = comb(g + b, k) - comb(g, k) - comb(b, k)
    p = f"A club has ${g}$ girls and ${b}$ boys. In how many ways can a committee of ${k}$ be chosen that has at least one girl and at least one boy?"
    sol = explain(
        f"committees of ${k}$ that are mixed (not all one gender).",
        "complementary counting: count everything, then subtract what you don't want.",
        [
            f"All committees of ${k}$ from ${g + b}$ people: $\\binom{{{g + b}}}{{{k}}} = {comb(g + b, k)}$.",
            f"All girl committees: $\\binom{{{g}}}{{{k}}} = {comb(g, k)}$. All boy committees: $\\binom{{{b}}}{{{k}}} = {comb(b, k)}$.",
            f"Mixed committees: ${comb(g + b, k)} - {comb(g, k)} - {comb(b, k)} = {ans}$.",
        ],
        f"${ans}$ committees.",
        f"choosing one girl, one boy, then anyone for the rest: ${g} \\cdot {b} \\cdot \\binom{{{g + b - 2}}}{{{k - 2}}}$. That counts many committees more than once.",
    )
    return (p, ans, [comb(g + b, k), g * b * comb(g + b - 2, k - 2), ans + comb(g, k), comb(g, 1) * comb(b, k - 1), ans - 1],
            ["Count all committees, then remove the ones that are all girls or all boys."], sol)


@family("l2_cp_word_arrange", 2, "counting_probability", "cp_permutations")
def _(r):
    w = r.choice(["BANANA", "LETTER", "COOKIE", "PEPPER", "BALLOON", "COFFEE", "MISSISSIPPI", "TOMATO", "SUCCESS", "ACCESS", "GAGGLE", "BOOKKEEPER"])
    c = Counter(w)
    ans = math.factorial(len(w))
    for v in c.values():
        ans //= math.factorial(v)
    reps = [(ch, v) for ch, v in c.items() if v > 1]
    p = f"How many different arrangements of the letters in the word {w} are there?"
    sol = explain(
        f"the number of different strings you can make by rearranging all ${len(w)}$ letters of {w}.",
        "arrange as if every letter were different, then divide out the swaps of identical letters, which don't make anything new.",
        [
            f"With ${len(w)}$ different letters there would be ${len(w)}! = {math.factorial(len(w))}$ arrangements.",
            "Repeated letters: " + ", ".join(f"{ch} appears ${v}$ times" for ch, v in reps) + ". Swapping copies of the same letter gives the same word.",
            f"Divide: $$ \\frac{{{len(w)}!}}{{{' \\cdot '.join(f'{v}!' for _, v in reps)}}} = {ans}. $$",
        ],
        f"${ans}$ arrangements.",
        f"answering ${len(w)}!$ and forgetting the repeated letters.",
    )
    return (p, ans, [math.factorial(len(w)), ans * 2, ans // 2, math.factorial(len(c)), ans + len(w)], ["Divide by the arrangements of each repeated letter."], sol)


@family("l2_cp_coins", 2, "counting_probability", "cp_probability")
def _(r):
    n = r.randint(4, 8)
    k = r.randint(1, n - 1)
    kind = r.choice(["exact", "atleast"])
    if kind == "exact":
        pr = F(comb(n, k), 2 ** n)
        p = f"A fair coin is flipped ${n}$ times. What is the probability of getting exactly ${k}$ heads?"
        steps = [f"There are $2^{{{n}}} = {2 ** n}$ equally likely sequences of heads and tails.",
                 f"A sequence with exactly ${k}$ heads is fixed by choosing which ${k}$ of the ${n}$ flips are heads: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$ ways.",
                 f"Probability $= \\frac{{{comb(n, k)}}}{{{2 ** n}}} = {num(pr).tex}$."]
        trap = f"answering $\\frac{{{k}}}{{{n}}}$. That is the fraction of flips that are heads, not a probability."
    else:
        good = sum(comb(n, j) for j in range(k, n + 1))
        pr = F(good, 2 ** n)
        p = f"A fair coin is flipped ${n}$ times. What is the probability of getting at least ${k}$ heads?"
        steps = [f"There are $2^{{{n}}} = {2 ** n}$ equally likely sequences.",
                 f"Count sequences with ${k}$, ${k + 1}$, up to ${n}$ heads: $$" + " + ".join(f"\\binom{{{n}}}{{{j}}}" for j in range(k, n + 1)) + f" = {good}.$$",
                 f"Probability $= \\frac{{{good}}}{{{2 ** n}}} = {num(pr).tex}$."]
        trap = f"counting only exactly ${k}$ heads. At least ${k}$ includes every larger number too."
    sol = explain(f"the chance of {'exactly' if kind == 'exact' else 'at least'} ${k}$ heads in ${n}$ flips.", "count the favorable sequences of flips and divide by all $2^n$ sequences.", steps, f"${num(pr).tex}$.", trap)
    return (p, pr, [F(k, n), F(1, 2), pr + F(1, 2 ** n), F(comb(n, k), 2 ** (n - 1)) if F(comb(n, k), 2 ** (n - 1)) < 1 else F(1, 4), 1 - pr],
            ["There are $2^n$ equally likely sequences."], sol)


# ============================================================ LEVEL 3 (AMC 10 #11 to 15, AMC 12 #6 to 10)


@family("l3_alg_vieta_sq", 3, "algebra", "alg_quadratics")
def _(r):
    b, c = r.randint(-12, 12), r.randint(-30, 30)
    if c == 0 or b == 0:
        return None
    ask = r.choice(["sq", "recip", "cube"])
    s, pr = -b, c
    if ask == "sq":
        ans = s * s - 2 * pr
        expr = "r^2 + s^2"
        work = ["Square the sum: $(r + s)^2 = r^2 + 2rs + s^2$, so $$ r^2 + s^2 = (r + s)^2 - 2rs. $$",
                f"Plug in: $({s})^2 - 2({pr}) = {s * s} - ({2 * pr}) = {ans}$."]
    elif ask == "recip":
        ans = F(s, pr)
        expr = "\\frac{1}{r} + \\frac{1}{s}"
        work = ["Combine over a common denominator: $$ \\frac{1}{r} + \\frac{1}{s} = \\frac{r + s}{rs}. $$",
                f"Plug in: $\\frac{{{s}}}{{{pr}}} = {num(ans).tex}$."]
    else:
        ans = s ** 3 - 3 * s * pr
        expr = "r^3 + s^3"
        work = ["Cube the sum: $(r + s)^3 = r^3 + s^3 + 3rs(r + s)$, so $$ r^3 + s^3 = (r + s)^3 - 3rs(r + s). $$",
                f"Plug in: $({s})^3 - 3({pr})({s}) = {s ** 3} - ({3 * pr * s}) = {ans}$."]
    poly = f"x^2{' + ' if b > 0 else ' - '}{abs(b) if abs(b) != 1 else ''}x{' + ' if c > 0 else ' - '}{abs(c)}"
    p = f"Let $r$ and $s$ be the roots of ${poly} = 0$. What is ${expr}$?"
    sol = explain(
        f"${expr}$ for the two roots. You do not need the roots themselves, which may be messy.",
        "Vieta's formulas: for $x^2 + bx + c = 0$, the roots satisfy $r + s = -b$ and $rs = c$. Rewrite the expression using only $r + s$ and $rs$.",
        [f"From ${poly} = 0$: $r + s = {s}$ and $rs = {pr}$."] + work,
        f"${expr} = {num(F(ans)).tex}$.",
        f"getting the sign of $r + s$ wrong. It is the negative of the $x$ coefficient, so here it is ${s}$.",
    )
    return (p, ans, [s * s + 2 * pr if ask == "sq" else -ans, s, pr, ans + 1, (ans * 2 if ans else 3)], ["Use $r + s$ and $rs$ from Vieta's formulas."], sol)


@family("l3_alg_compose", 3, "algebra", "alg_functions")
def _(r):
    a, b = r.choice([2, 3, -2, 4, -3]), r.randint(-9, 9)
    c, d = r.randint(2, 5), r.randint(-6, 6)
    k = r.randint(-5, 9)
    x = F(k - d, c)
    ans = a * x + b
    inner = f"{c}x{' + ' if d >= 0 else ' - '}{abs(d)}"
    outer = f"{a}x{' + ' if b >= 0 else ' - '}{abs(b)}"
    p = f"A function satisfies $f({inner}) = {outer}$ for all real $x$. What is $f({k})$?"
    sol = explain(
        f"the output of $f$ when its input is ${k}$.",
        f"the rule gives $f$ of the expression ${inner}$, not $f(x)$. Choose the $x$ that makes ${inner}$ equal to ${k}$.",
        [
            f"Solve ${inner} = {k}$: ${c}x = {k - d}$, so $x = {num(x).tex}$.",
            f"Plug that $x$ into the right side: $${a} \\cdot \\left({num(x).tex}\\right){' + ' if b >= 0 else ' - '}{abs(b)} = {num(ans).tex}.$$",
        ],
        f"$f({k}) = {num(ans).tex}$.",
        f"plugging $x = {k}$ straight into ${outer}$, which gives ${a * k + b}$. That computes $f({c * k + d})$, not $f({k})$.",
    )
    return (p, ans, [a * k + b, ans + a, F(a * k + b, c), ans - 1, a * (k + d) + b], ["Choose $x$ so that the input equals the number you want."], sol)


@family("l3_alg_arith_sum", 3, "algebra", "alg_sequences")
def _(r):
    a1, d = r.randint(-20, 20), r.randint(-6, 7)
    if d == 0:
        return None
    p_, q_ = sorted(r.sample(range(3, 20), 2))
    n = r.randint(15, 40)
    ap, aq = a1 + (p_ - 1) * d, a1 + (q_ - 1) * d
    an = a1 + (n - 1) * d
    S = n * (a1 + an) // 2
    p = f"In an arithmetic sequence, the {ordinal(p_)} term is ${ap}$ and the {ordinal(q_)} term is ${aq}$. What is the sum of the first ${n}$ terms?"
    sol = explain(
        f"$a_1 + a_2 + \\cdots + a_{{{n}}}$.",
        "an arithmetic sequence is fixed by its first term $a_1$ and common difference $d$, with $a_k = a_1 + (k - 1)d$. The sum of $n$ terms is $\\frac{n}{2}(a_1 + a_n)$.",
        [
            f"From the {ordinal(p_)} term to the {ordinal(q_)} term there are ${q_ - p_}$ steps, so $${q_ - p_}d = {aq} - ({ap}) = {aq - ap}, \\quad d = {d}.$$",
            f"First term: $a_1 = a_{{{p_}}} - {p_ - 1}d = {ap} - ({(p_ - 1) * d}) = {a1}$.",
            f"Term number ${n}$: $a_{{{n}}} = {a1} + {n - 1} \\cdot ({d}) = {an}$.",
            f"Sum: $\\frac{{{n}}}{{2}}({a1} + {an}) = \\frac{{{n}}}{{2}} \\cdot {a1 + an} = {S}$.",
        ],
        f"the sum is ${S}$.",
        f"dividing by ${q_}$ or ${p_}$ instead of the number of steps between the terms, ${q_ - p_}$.",
    )
    return (p, S, [S + n * d, S - n * d, n * (ap + aq) // 2, S + d, an], ["Find the common difference, then the first term."], sol)


@family("l3_geo_parallel_cut", 3, "geometry", "geo_similar")
def _(r):
    m, n = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)])
    base = r.choice([10, 12, 15, 20, 24, 30, 35, 40])
    A = r.choice([n * n * k for k in range(1, 6)])
    small = F(A * m * m, n * n)
    ask = r.choice(["trap", "seg"])
    if ask == "trap":
        ans = A - small
        p = (f"A line parallel to side $BC$ of triangle $ABC$ meets $AB$ at $D$ and $AC$ at $E$, with $AD : DB = {m} : {n - m}$. "
             f"The area of triangle $ABC$ is ${A}$. What is the area of quadrilateral $DBCE$?")
        sol = explain(
            "the area of the bottom piece, between the parallel line and $BC$.",
            "a line parallel to one side cuts off a smaller triangle similar to the original. Areas of similar figures scale by the square of the side ratio.",
            [
                f"$AD : DB = {m} : {n - m}$ means $AD : AB = {m} : {n}$, so triangle $ADE$ is a scaled copy of $ABC$ with ratio $\\frac{{{m}}}{{{n}}}$.",
                f"Area of $ADE = {A} \\cdot \\left(\\frac{{{m}}}{{{n}}}\\right)^2 = {A} \\cdot \\frac{{{m * m}}}{{{n * n}}} = {num(small).tex}$.",
                f"The quadrilateral is what is left: ${A} - {num(small).tex} = {num(ans).tex}$.",
            ],
            f"${num(ans).tex}$.",
            f"using $\\frac{{{m}}}{{{n - m}}}$ as the scale factor. The scale factor compares $AD$ to the whole side $AB$, which is $\\frac{{{m}}}{{{n}}}$. Also, areas scale by its square.",
        )
        wrong = [small, A * F(n - m, n), A - A * F(m, n), ans + 1, A * F(m, n)]
    else:
        ans = F(base * m, n)
        p = (f"A line parallel to side $BC$ of triangle $ABC$ meets $AB$ at $D$ and $AC$ at $E$, and it cuts off triangle $ADE$ with area "
             f"$\\frac{{{m * m}}}{{{n * n}}}$ of the area of $ABC$. If $BC = {base}$, what is $DE$?")
        sol = explain(
            "the length of $DE$.",
            "triangle $ADE$ is similar to triangle $ABC$. If lengths scale by $k$, areas scale by $k^2$.",
            [
                f"The area ratio is $k^2 = \\frac{{{m * m}}}{{{n * n}}}$.",
                f"Take the square root: $k = \\frac{{{m}}}{{{n}}}$.",
                f"$DE$ matches $BC$, so $DE = {base} \\cdot \\frac{{{m}}}{{{n}}} = {num(ans).tex}$.",
            ],
            f"$DE = {num(ans).tex}$.",
            f"multiplying ${base}$ by the area ratio directly, which gives ${num(F(base * m * m, n * n)).tex}$.",
        )
        wrong = [F(base * m * m, n * n), base - ans, F(base, 2), ans + 1, F(base * (n - m), n) if n - m != m else ans + 2]
    return (p, ans, wrong, ["Areas of similar figures scale by the square of the side ratio."], sol)


@family("l3_geo_trapezoid", 3, "geometry", "geo_area")
def _(r):
    h, x = r.choice([(4, 3), (12, 5), (8, 6), (15, 8), (12, 9), (24, 7), (8, 15)])
    b1 = r.randint(3, 20)
    b2 = b1 + 2 * x
    leg = int(math.isqrt(h * h + x * x))
    ans = F((b1 + b2) * h, 2)
    p = f"An isosceles trapezoid has bases ${b1}$ and ${b2}$ and legs of length ${leg}$. What is its area?"
    sol = explain(
        "the area, which needs the height of the trapezoid.",
        "drop perpendiculars from the ends of the short base. They cut off two matching right triangles, and the height is a leg of each.",
        [
            f"The long base is ${b2 - b1}$ longer than the short base, split evenly between the two ends: each overhang is $\\frac{{{b2} - {b1}}}{{2}} = {x}$.",
            f"Each right triangle has hypotenuse ${leg}$ and one leg ${x}$, so the height is $$ h = \\sqrt{{{leg}^2 - {x}^2}} = \\sqrt{{{leg * leg - x * x}}} = {h}. $$",
            f"Trapezoid area: $\\frac{{b_1 + b_2}}{{2}} \\cdot h = \\frac{{{b1} + {b2}}}{{2}} \\cdot {h} = {num(ans).tex}$.",
        ],
        f"${num(ans).tex}$.",
        f"using the slanted leg ${leg}$ as the height. The height must be perpendicular to the bases.",
    )
    return (p, ans, [(b1 + b2) * leg // 2, (b1 + b2) * h, ans + h, b2 * h, b1 * leg], ["Drop heights from the ends of the shorter base."], sol)


@family("l3_geo_chord", 3, "geometry", "geo_circles")
def _(r):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15), (20, 21, 29)])
    ask = r.choice(["chord", "dist", "between"])
    idea = "the perpendicular from the center to a chord hits the chord at its midpoint. The radius to an end of the chord is the hypotenuse of a right triangle."
    if ask == "chord":
        p = f"A chord of a circle with radius ${c}$ is ${a}$ units from the center. How long is the chord?"
        sol = explain("the full length of the chord.", idea, [
            f"The right triangle has hypotenuse ${c}$ (the radius) and one leg ${a}$ (the distance to the chord).",
            f"The other leg, half the chord, is $\\sqrt{{{c}^2 - {a}^2}} = \\sqrt{{{c * c - a * a}}} = {b}$.",
            f"The whole chord is $2 \\cdot {b} = {2 * b}$."], f"${2 * b}$.", f"stopping at half the chord, ${b}$.")
        return (p, 2 * b, [b, 2 * a, c + a, 2 * c - a, 2 * b + 2], ["The perpendicular from the center bisects the chord."], sol)
    if ask == "dist":
        p = f"A chord of length ${2 * b}$ lies in a circle of radius ${c}$. How far is the chord from the center?"
        sol = explain("the distance from the center to the chord.", idea, [
            f"Half the chord is ${b}$, and the radius is ${c}$.",
            f"Distance $= \\sqrt{{{c}^2 - {b}^2}} = \\sqrt{{{c * c - b * b}}} = {a}$."], f"${a}$.", f"using the full chord ${2 * b}$ instead of half of it.")
        return (p, a, [b, c - b, 2 * a, a + 1, c - a], ["The perpendicular from the center bisects the chord."], sol)
    p = f"Two parallel chords of a circle with radius ${c}$ have lengths ${2 * a}$ and ${2 * b}$ and lie on opposite sides of the center. How far apart are they?"
    sol = explain("the distance between the two chords.", idea + " Find each chord's distance from the center separately.", [
        f"Chord of length ${2 * a}$: half is ${a}$, so its distance from the center is $\\sqrt{{{c * c} - {a * a}}} = {b}$.",
        f"Chord of length ${2 * b}$: half is ${b}$, so its distance is $\\sqrt{{{c * c} - {b * b}}} = {a}$.",
        f"They are on opposite sides of the center, so add: ${b} + {a} = {a + b}$."], f"${a + b}$.",
        f"subtracting the distances (${abs(b - a)}$). That is only right when both chords are on the same side.")
    return (p, a + b, [abs(b - a), c, a + b + 2, 2 * c - 1, a * b // c + 1], ["Find each chord's distance from the center."], sol)


@family("l3_nt_base_find", 3, "number_theory", "nt_bases")
def _(r):
    b = r.randint(5, 16)
    d = [r.randint(1, b - 1), r.randint(0, b - 1), r.randint(0, b - 1)]
    if any(x >= 10 for x in d):
        return None
    N = d[0] * b * b + d[1] * b + d[2]
    digits = "".join(map(str, d))
    p = f"The base $b$ number ${digits}_b$ is equal to ${N}$ in base $10$. What is $b$?"
    sol = explain(
        f"the base $b$ that makes ${digits}_b$ worth ${N}$.",
        "in base $b$, the places are worth $b^2$, $b$ and $1$. Write the number as a polynomial in $b$ and solve.",
        [
            f"${digits}_b = {d[0]}b^2 + {d[1]}b + {d[2]}$, so we need $${d[0]}b^2 + {d[1]}b + {d[2]} = {N}.$$",
            f"Every digit must be less than the base, so $b \\ge {max(d) + 1}$.",
            f"Try $b = {b}$: ${d[0]} \\cdot {b * b} + {d[1]} \\cdot {b} + {d[2]} = {d[0] * b * b} + {d[1] * b} + {d[2]} = {N}$. It works.",
            "The left side grows as $b$ grows, so no other base works.",
        ],
        f"$b = {b}$.",
        "reading the number as base ten, or trying bases smaller than the biggest digit.",
    )
    return (p, b, [b + 1, b - 1, b + 2, b - 2, max(d) + 1 if max(d) + 1 != b else b + 3], ["Write the base $b$ number as a polynomial in $b$."], sol)


@family("l3_nt_factorial_power", 3, "number_theory", "nt_factorials")
def _(r):
    p_ = r.choice([2, 3, 5, 7])
    n = r.randint(30, 300)
    terms = []
    q = p_
    while q <= n:
        terms.append((q, n // q))
        q *= p_
    e = sum(t for _, t in terms)
    if p_ == 5:
        p = f"How many zeros are at the end of ${n}!$?"
        need = f"the number of trailing zeros of ${n}!$. Each trailing zero comes from a factor $10 = 2 \\cdot 5$, and there are far more $2$s than $5$s, so count the factors of $5$."
    else:
        p = f"What is the largest integer $k$ such that ${p_}^k$ divides ${n}!$?"
        need = f"how many times the prime ${p_}$ divides the product $1 \\cdot 2 \\cdot 3 \\cdots {n}$."
    sol = explain(
        need,
        f"Legendre's formula: every multiple of ${p_}$ gives one factor, every multiple of ${p_}^2$ gives one more, and so on.",
        [f"Multiples of ${qq}$ up to ${n}$: $\\left\\lfloor \\frac{{{n}}}{{{qq}}} \\right\\rfloor = {t}$." for qq, t in terms]
        + [f"Add them: ${' + '.join(str(t) for _, t in terms)} = {e}$."],
        f"${e}$.",
        f"counting only the multiples of ${p_}$ (${n // p_}$). Numbers like ${p_ * p_}$ contribute two factors.",
    )
    return (p, e, [n // p_, e + 1, e - 1, e + n // (p_ ** 3) + 1, n // p_ + n // (p_ * 2)], [f"Count multiples of ${p_}$, of ${p_}^2$, and so on."], sol)


@family("l3_nt_gcd_lcm_count", 3, "number_theory", "nt_gcd")
def _(r):
    g = r.randint(2, 12)
    L = g * r.choice([6, 10, 12, 15, 18, 20, 30, 36])
    a = r.choice([x for x in range(g, L + 1, g) if L % x == 0])
    sols = [n for n in range(1, L + 1) if math.gcd(a, n) == g and math.lcm(a, n) == L]
    if len(sols) != 1:
        return None
    n = sols[0]
    p = f"A positive integer $n$ satisfies $\\gcd({a}, n) = {g}$ and $\\operatorname{{lcm}}({a}, n) = {L}$. What is $n$?"
    sol = explain(
        "the one number $n$ with this gcd and lcm.",
        "for any two positive integers, $\\gcd(a, n) \\cdot \\operatorname{lcm}(a, n) = a \\cdot n$.",
        [
            f"Plug in: ${g} \\cdot {L} = {a} \\cdot n$, so ${g * L} = {a}n$.",
            f"Divide: $n = \\frac{{{g * L}}}{{{a}}} = {n}$.",
            f"Check: $\\gcd({a}, {n}) = {math.gcd(a, n)}$ and $\\operatorname{{lcm}}({a}, {n}) = {math.lcm(a, n)}$.",
        ],
        f"$n = {n}$.",
        f"answering $\\frac{{{L}}}{{{g}}} = {L // g}$ without using ${a}$.",
    )
    return (p, n, [L // g, g * L // a + g, L, a, n + g], ["$\\gcd(a, n) \\cdot \\operatorname{lcm}(a, n) = an$."], sol)


@family("l3_cp_grid_through", 3, "counting_probability", "cp_combinations")
def _(r):
    w, h = r.randint(4, 7), r.randint(3, 6)
    px, py = r.randint(1, w - 1), r.randint(1, h - 1)
    kind = r.choice(["through", "avoid"])
    first = comb(px + py, px)
    second = comb(w - px + h - py, w - px)
    thr = first * second
    tot = comb(w + h, w)
    ans = thr if kind == "through" else tot - thr
    word = "pass through" if kind == "through" else "avoid"
    p = f"A path from $(0, 0)$ to $({w}, {h})$ moves one unit right or one unit up at each step. How many such paths {word} the point $({px}, {py})$?"
    steps = [
        "A path from $(0, 0)$ to $(a, b)$ is a string of $a$ R's and $b$ U's, so there are $\\binom{a + b}{a}$ of them.",
        f"From $(0, 0)$ to $({px}, {py})$: $\\binom{{{px + py}}}{{{px}}} = {first}$ paths.",
        f"From $({px}, {py})$ to $({w}, {h})$: ${w - px}$ R's and ${h - py}$ U's, so $\\binom{{{w - px + h - py}}}{{{w - px}}} = {second}$ paths.",
        f"Paths through the point: ${first} \\cdot {second} = {thr}$.",
    ]
    if kind == "avoid":
        steps.append(f"All paths: $\\binom{{{w + h}}}{{{w}}} = {tot}$. Paths that avoid the point: ${tot} - {thr} = {ans}$.")
    sol = explain(f"the number of up and right paths that {word} $({px}, {py})$.",
                  "a path through a point is a path to the point followed by a path from it, so multiply. To avoid a point, subtract the paths through it from all paths.",
                  steps, f"${ans}$ paths.",
                  "adding the two partial counts instead of multiplying them." if kind == "through" else "subtracting only the paths that reach the point, instead of the full paths through it.")
    return (p, ans, [tot, tot - ans, first + second, ans + 1, comb(w + h, 2)], ["Count paths to the point, then from the point to the end."], sol)


@family("l3_cp_repeat_digit", 3, "counting_probability", "cp_casework")
def _(r):
    k = r.choice([3, 4, 5])
    kind = r.choice(["repeat", "has_d"])
    tot = 9 * 10 ** (k - 1)
    if kind == "repeat":
        distinct = 9
        factors = ["9"]
        for i in range(1, k):
            distinct *= 10 - i
            factors.append(str(10 - i))
        ans = tot - distinct
        p = f"How many {k} digit positive integers have at least two digits that are the same?"
        sol = explain(
            f"{k} digit numbers with some repeated digit.",
            "at least one repeat has many cases, but the opposite, all digits different, is easy. Count that and subtract.",
            [
                f"All {k} digit numbers: the first digit is $1$ to $9$ and the rest are $0$ to $9$, so $9 \\cdot 10^{{{k - 1}}} = {tot}$.",
                f"All digits different: the first digit has $9$ choices (not $0$), the next has $9$ (any digit except the first, and $0$ is now allowed), then $8$, and so on: $${' \\cdot '.join(factors)} = {distinct}.$$",
                f"Subtract: ${tot} - {distinct} = {ans}$.",
            ],
            f"${ans}$.",
            "allowing $0$ as the first digit, or giving the second digit only $8$ choices (it can be $0$).",
        )
    else:
        d = r.randint(1, 9)
        none = 8 * 9 ** (k - 1)
        ans = tot - none
        p = f"How many {k} digit positive integers have at least one digit equal to ${d}$?"
        sol = explain(
            f"{k} digit numbers containing the digit ${d}$ somewhere.",
            f"count the opposite, numbers with no ${d}$ at all, then subtract from the total.",
            [
                f"All {k} digit numbers: $9 \\cdot 10^{{{k - 1}}} = {tot}$.",
                f"No ${d}$ anywhere: the first digit can't be $0$ or ${d}$ ($8$ choices), and every other digit can't be ${d}$ ($9$ choices). That gives $8 \\cdot 9^{{{k - 1}}} = {none}$.",
                f"Subtract: ${tot} - {none} = {ans}$.",
            ],
            f"${ans}$.",
            f"counting exactly one ${d}$ instead of at least one.",
        )
    return (p, ans, [tot - ans, ans + 9, ans - 10, 10 ** (k - 1), tot // 2], ["Count the complement."], sol)


@family("l3_cp_inclusion", 3, "counting_probability", "cp_inclusion")
def _(r):
    N = r.randint(100, 1000)
    a, b, c = r.choice([(2, 3, 5), (2, 3, 7), (3, 5, 7), (2, 5, 7)])
    kind = r.choice(["none", "any"])
    cnt = sum(1 for x in range(1, N + 1) if x % a == 0 or x % b == 0 or x % c == 0)
    ans = cnt if kind == "any" else N - cnt
    word = "divisible by at least one of" if kind == "any" else "divisible by none of"
    s1 = N // a + N // b + N // c
    s2 = N // (a * b) + N // (a * c) + N // (b * c)
    s3 = N // (a * b * c)
    assert s1 - s2 + s3 == cnt
    p = f"How many integers from $1$ to ${N}$ are {word} ${a}$, ${b}$, and ${c}$?"
    steps = [
        f"Singles: $\\lfloor {N}/{a} \\rfloor + \\lfloor {N}/{b} \\rfloor + \\lfloor {N}/{c} \\rfloor = {N // a} + {N // b} + {N // c} = {s1}$.",
        f"Pairs, which were counted twice above, so subtract: $\\lfloor {N}/{a * b} \\rfloor + \\lfloor {N}/{a * c} \\rfloor + \\lfloor {N}/{b * c} \\rfloor = {N // (a * b)} + {N // (a * c)} + {N // (b * c)} = {s2}$.",
        f"All three, added back once: $\\lfloor {N}/{a * b * c} \\rfloor = {s3}$.",
        f"Divisible by at least one: ${s1} - {s2} + {s3} = {cnt}$.",
    ]
    if kind == "none":
        steps.append(f"Divisible by none: ${N} - {cnt} = {ans}$.")
    sol = explain(f"how many numbers up to ${N}$ are {word} ${a}$, ${b}$, ${c}$.",
                  "Inclusion and Exclusion: add the single counts, subtract the overlaps of two, add back the overlap of all three.", steps, f"${ans}$.",
                  f"stopping at the singles sum ${s1}$, which counts numbers like ${a * b}$ more than once.")
    return (p, ans, [s1 if kind == "any" else N - s1, N - ans, ans + 1, ans - 2, N // (a * b * c)], ["Use inclusion and exclusion."], sol)
