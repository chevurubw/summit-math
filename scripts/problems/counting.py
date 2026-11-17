"""Counting and probability unit: original problems. Answers are checked by brute force where practical."""
import itertools
import math
from collections import Counter
from fractions import Fraction as F

from common import NAMES, Bank, C, comb, explain, num, var
from counting_more1 import MORE as M1
from counting_more2 import MORE as M2

MORE = {**M1, **M2}

banks = []


def bank(skill_id):
    b = Bank(skill_id)
    banks.append(b)
    return b


def big(v):
    return f"{v:,}".replace(",", "{,}")


# ---------------------------------------------------------------- counting principle
b = bank("cp_counting")


def ct1(r):
    s, p_, d = r.randint(2, 8), r.randint(2, 8), r.randint(2, 6)
    n = r.choice(NAMES)
    ans = s * p_ * d
    p = f"{n} has {s} shirts, {p_} pairs of pants, and {d} pairs of shoes. How many different outfits of one shirt, one pair of pants, and one pair of shoes are possible?"
    sol = explain("the number of different outfits.", "Multiplication Principle: for a sequence of independent choices, multiply the number of options at each step.",
                  [f"Shirt: ${s}$ options. For each shirt, pants: ${p_}$ options. That is ${s} \\cdot {p_} = {s * p_}$ shirt and pants combos.", f"Each combo can go with any of ${d}$ pairs of shoes: ${s * p_} \\cdot {d} = {ans}$."],
                  f"${ans}$ outfits.", f"adding the choices (${s} + {p_} + {d} = {s + p_ + d}$), which counts single items, not outfits.")
    return (p, ans, [s + p_ + d, s * p_ + d, ans * 2, s * p_, ans - d], ["Multiply the number of choices for each item."], sol)


def ct2(r):
    L, D = r.randint(1, 3), r.randint(2, 4)
    rep = r.choice([True, False])
    fmt = lambda v: C(big(v), v)
    if rep:
        ans = 26 ** L * 10 ** D
        p = f"A license plate has {L} letter{'s' if L > 1 else ''} followed by {D} digits. Letters and digits may repeat. How many plates are possible?"
        sol = explain("the number of possible plates.", "each position is an independent choice: $26$ letters or $10$ digits. Multiply.",
                      [f"Letter positions: $26$ choices each, ${L}$ positions: $26^{{{L}}} = {big(26 ** L)}$.", f"Digit positions: $10$ choices each, ${D}$ positions: $10^{{{D}}} = {big(10 ** D)}$.", f"Total: ${big(26 ** L)} \\cdot {big(10 ** D)} = {big(ans)}$."],
                      f"${big(ans)}$.", "adding the letter count and the digit count instead of multiplying.")
        wrong = [26 * L * 10 * D, 26 ** L + 10 ** D, 26 ** L * math.perm(10, D), 36 ** (L + D)]
    else:
        ans = math.perm(26, L) * math.perm(10, D)
        p = f"A code has {L} letter{'s' if L > 1 else ''} followed by {D} digits, with no letter or digit repeated. How many codes are possible?"
        lf = " \\cdot ".join(str(26 - i) for i in range(L))
        df = " \\cdot ".join(str(10 - i) for i in range(D))
        sol = explain("the number of possible codes.", "with no repeats, each new position has one fewer choice than the last of its kind.",
                      [f"Letters: ${lf} = {big(math.perm(26, L))}$.", f"Digits: ${df} = {big(math.perm(10, D))}$.", f"Total: ${big(math.perm(26, L))} \\cdot {big(math.perm(10, D))} = {big(ans)}$."],
                      f"${big(ans)}$.", "allowing repeats, or using combinations (which ignore order, but order matters in a code).")
        wrong = [26 ** L * 10 ** D, comb(26, L) * comb(10, D), math.perm(26, L) + math.perm(10, D), math.perm(36, L + D)]
    return (p, fmt(ans), [fmt(w) for w in wrong], ["Multiply the number of options for each position."], sol)


def ct3(r):
    lo, hi = 100, 999
    cond = r.choice(["distinct", "odd", "no5", "even_sum"])
    if cond == "distinct":
        ans = 648
        p = "How many three-digit numbers have three different digits?"
        steps = ["Hundreds digit: $1$ to $9$, so $9$ choices.", "Tens digit: any of $0$ to $9$ except the hundreds digit, so $9$ choices.", "Ones digit: not either of those, so $8$ choices.", "$9 \\cdot 9 \\cdot 8 = 648$."]
        trap = "giving the tens digit only $8$ choices; $0$ is allowed there."
    elif cond == "odd":
        ans = 125
        p = "How many three-digit numbers have only odd digits?"
        steps = ["Each digit must be one of $1, 3, 5, 7, 9$: $5$ choices.", "The first digit can't be $0$, but $0$ is even anyway, so nothing changes.", "$5 \\cdot 5 \\cdot 5 = 125$."]
        trap = "including $0$ as an odd digit."
    elif cond == "no5":
        ans = 648
        p = "How many three-digit numbers do not contain the digit 5?"
        steps = ["Hundreds digit: $1$ to $9$ except $5$: $8$ choices.", "Tens and ones digits: $0$ to $9$ except $5$: $9$ choices each.", "$8 \\cdot 9 \\cdot 9 = 648$."]
        trap = "giving the first digit $9$ choices; it can't be $0$ or $5$."
    else:
        k = r.randint(2, 6)
        nums = [n for n in range(lo, hi + 1) if sum(map(int, str(n))) == k]
        ans = len(nums)
        p = f"How many three-digit numbers have digits that add up to ${k}$?"
        steps = [f"Write the number as $\\overline{{abc}}$ with $a \\ge 1$ and $a + b + c = {k}$.",
                 "Casework on $a$: " + "; ".join(f"$a = {a}$: $b + c = {k - a}$ has ${k - a + 1}$ solutions" for a in range(1, k + 1)) + ".",
                 f"Add: ${' + '.join(str(k - a + 1) for a in range(1, k + 1))} = {ans}$."]
        trap = "letting $a = 0$, which would not be a three digit number."
    sol = explain("a count of three digit numbers with a digit condition.", "count the choices for each digit position, remembering the hundreds digit can't be $0$.", steps, f"${ans}$.", trap)
    return (p, ans, [ans + 9, ans - 9, ans * 2 if ans < 400 else ans // 2, 900 - ans, ans + 1], ["Count the choices for the hundreds, tens, and units digits separately, remembering the first digit cannot be 0."], sol)


def ct4(r):
    m, n = r.randint(2, 6), r.randint(2, 6)
    ans = comb(m + n, m)
    p = f"How many paths of length ${m + n}$ go from $(0, 0)$ to $({m}, {n})$ using only steps right (one unit in $x$) and up (one unit in $y$)?"
    sol = explain("the number of up and right paths.", f"every path is a string of ${m}$ R's and ${n}$ U's in some order. Choosing where the R's go fixes the path.",
                  [f"The path has ${m + n}$ steps.", f"Choose which ${m}$ of them are R: $\\binom{{{m + n}}}{{{m}}} = {ans}$."],
                  f"${ans}$.", f"using ${m + n}!$, which treats the R's as different from each other.")
    return (p, ans, [m * n, 2 ** (m + n), math.perm(m + n, m), ans + 1, comb(m + n, m - 1)], ["Every path uses $" + str(m) + "$ right steps and $" + str(n) + "$ up steps in some order."], sol)


def ctc1(r):
    m, n = r.randint(3, 6), r.randint(3, 6)
    bx, by = r.randint(1, m - 1), r.randint(1, n - 1)
    total = comb(m + n, m)
    first, second = comb(bx + by, bx), comb(m - bx + n - by, m - bx)
    through = first * second
    ans = total - through
    p = f"How many paths from $(0, 0)$ to $({m}, {n})$ using unit steps right and up avoid the point $({bx}, {by})$?"
    sol = explain(f"paths that never touch $({bx}, {by})$.", "complementary counting: all paths minus the paths through the bad point.",
                  [f"All paths: $\\binom{{{m + n}}}{{{m}}} = {total}$.", f"Paths to $({bx}, {by})$: $\\binom{{{bx + by}}}{{{bx}}} = {first}$. Paths from it to $({m}, {n})$: $\\binom{{{m - bx + n - by}}}{{{m - bx}}} = {second}$.",
                   f"Paths through it: ${first} \\cdot {second} = {through}$.", f"Avoiding it: ${total} - {through} = {ans}$."],
                  f"${ans}$.", "adding the two partial path counts instead of multiplying them.")
    return (p, ans, [total, through, ans + 1, total - first, ans - 1], ["Count all paths, then subtract the paths that pass through the bad point."], sol)


def ctc2(r):
    m, n = r.randint(2, 6), r.randint(2, 6)
    ans = comb(m + 1, 2) * comb(n + 1, 2)
    p = f"How many rectangles of any size are in a ${m} \\times {n}$ grid of unit squares?"
    sol = explain("rectangles of every size, not just the unit squares.", "a rectangle is determined by its left and right sides (two vertical grid lines) and its top and bottom (two horizontal grid lines).",
                  [f"There are ${m + 1}$ vertical lines: choose $2$ in $\\binom{{{m + 1}}}{{2}} = {comb(m + 1, 2)}$ ways.", f"There are ${n + 1}$ horizontal lines: choose $2$ in $\\binom{{{n + 1}}}{{2}} = {comb(n + 1, 2)}$ ways.", f"Multiply: ${comb(m + 1, 2)} \\cdot {comb(n + 1, 2)} = {ans}$."],
                  f"${ans}$.", f"using ${m}$ and ${n}$ lines instead of ${m + 1}$ and ${n + 1}$; a grid of ${m}$ squares has ${m + 1}$ lines.")
    return (p, ans, [m * n, comb(m, 2) * comb(n, 2), ans + m * n, (m + 1) * (n + 1), ans - 1], ["A rectangle is chosen by picking 2 of the vertical grid lines and 2 of the horizontal ones."], sol)


def ctc3(r):
    n, k = r.randint(4, 8), r.randint(3, 5)
    ans = k * (k - 1) ** (n - 1)
    p = f"A row of ${n}$ fence posts is painted using ${k}$ colors so that no two neighboring posts have the same color. How many colorings are possible?"
    sol = explain("colorings where neighbors differ.", "paint left to right. Each post only has to avoid the color of the post just before it.",
                  [f"First post: ${k}$ colors.", f"Each of the other ${n - 1}$ posts: any color except its left neighbor's, so ${k - 1}$ choices.", f"Total: ${k} \\cdot {k - 1}^{{{n - 1}}} = {ans}$."],
                  f"${ans}$.", f"giving every post ${k - 1}$ choices, including the first, which has no left neighbor.")
    return (p, ans, [k ** n, k * (k - 1) ** n, ans + k, ans - k, (k - 1) ** n], ["The first post has $" + str(k) + "$ choices; each later post just needs to differ from the one before it."], sol)


b.fill_unique("basics", [ct1, ct2, ct3, ct4] + MORE[b.skill_id]["basics"], 3101)
b.fill_unique("challenge", [ctc1, ctc2, ctc3] + MORE[b.skill_id]["challenge"], 3102)


# ---------------------------------------------------------------- permutations
b = bank("cp_permutations")


def pe1(r):
    n = r.randint(4, 8)
    ans = math.factorial(n)
    p = f"In how many ways can ${n}$ different books be arranged in a row on a shelf?"
    sol = explain("the number of orders for the books.", "fill the shelf from left to right; each spot has one fewer book available than the last.",
                  [f"First spot: ${n}$ books. Second: ${n - 1}$. And so on down to $1$.", f"${' \\cdot '.join(str(i) for i in range(n, 0, -1))} = {n}! = {ans}$."],
                  f"${ans}$.", f"using ${n}^{{{n}}}$, which allows the same book in several spots.")
    return (p, ans, [n ** n, n * (n - 1), math.factorial(n - 1), 2 ** n, ans // 2], ["Choose the first book, then the second, and so on."], sol)


def pe2(r):
    word = r.choice(["LEVEL", "BANANA", "PEPPER", "LETTER", "COOKIE", "BALLOON", "COFFEE", "SETTLE", "TATTOO", "PUZZLE", "GAMMA", "ALPACA"])
    cnt = len(set(itertools.permutations(word)))
    c = Counter(word)
    reps = [(ch, v) for ch, v in c.items() if v > 1]
    denom = " \\cdot ".join(f"{v}!" for _, v in reps)
    p = f"How many different arrangements of the letters in the word {word} are there?"
    sol = explain(f"distinct rearrangements of {word}.", "count as if all letters were different, then divide out swaps of identical letters, which don't create new words.",
                  [f"${len(word)}$ letters, all different, would give ${len(word)}! = {math.factorial(len(word))}$ orders.", "Repeats: " + ", ".join(f"{ch} $\\times {v}$" for ch, v in reps) + ".",
                   f"$\\frac{{{len(word)}!}}{{{denom}}} = {cnt}$."],
                  f"${cnt}$.", f"answering ${len(word)}!$ and forgetting the repeated letters.")
    return (p, cnt, [math.factorial(len(word)), cnt * 2, cnt // 2 if cnt % 2 == 0 else cnt + 3, cnt + len(word), math.factorial(len(word) - 1)], ["Divide $n!$ by the factorial of each repeated letter's count."], sol)


def pe3(r):
    n, k = r.randint(6, 12), r.choice([2, 3])
    roles = ["president", "vice president", "treasurer"][:k]
    ans = math.perm(n, k)
    p = f"A club has ${n}$ members. In how many ways can it choose a " + ", ".join(roles[:-1]) + f" and {roles[-1]}, if no one holds two jobs?"
    sol = explain("ways to fill the jobs.", "the jobs are different, so order matters. Fill one job at a time.",
                  [f"{roles[0].capitalize()}: ${n}$ choices. " + " ".join(f"{roles[i].capitalize()}: ${n - i}$ choices (someone not already chosen)." for i in range(1, k)), f"${' \\cdot '.join(str(n - i) for i in range(k))} = {ans}$."],
                  f"${ans}$.", f"using $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$, which ignores who gets which job.")
    return (p, ans, [comb(n, k), n ** k, ans + n, math.factorial(n) // math.factorial(k), ans // 2], ["The order matters because the jobs are different."], sol)


def pe4(r):
    n = r.randint(4, 7)
    a, bb = r.sample(NAMES, 2)
    ans = 2 * math.factorial(n - 1)
    p = f"${n}$ people, including {a} and {bb}, line up in a row. In how many orders do {a} and {bb} stand next to each other?"
    sol = explain(f"orders with {a} and {bb} side by side.", "glue the two into a single block. Then arrange the block with everyone else, and finally choose the order inside the block.",
                  [f"With {a} and {bb} glued, there are ${n - 1}$ units to line up: $({n - 1})! = {math.factorial(n - 1)}$ orders.", f"Inside the block they can be {a} then {bb}, or {bb} then {a}: $2$ ways.", f"Total: $2 \\cdot {math.factorial(n - 1)} = {ans}$."],
                  f"${ans}$.", "forgetting the factor $2$ for the order inside the block.")
    return (p, ans, [math.factorial(n - 1), math.factorial(n), math.factorial(n) - ans, ans * 2, (n - 1) * 2], ["Glue the two friends into one block, then remember the block can be flipped."], sol)


def pec1(r):
    n = r.randint(5, 8)
    a, bb = r.sample(NAMES, 2)
    tog = 2 * math.factorial(n - 1)
    ans = math.factorial(n) - tog
    p = f"${n}$ people, including {a} and {bb}, line up in a row. In how many orders are {a} and {bb} NOT next to each other?"
    sol = explain(f"orders where {a} and {bb} are apart.", "complementary counting: all orders minus the orders where they are together.",
                  [f"All orders: ${n}! = {math.factorial(n)}$.", f"Together: glue them into a block, $({n - 1})! \\cdot 2 = {tog}$.", f"Apart: ${math.factorial(n)} - {tog} = {ans}$."],
                  f"${ans}$.", "trying to count 'apart' directly, which leads to messy cases. The complement is cleaner.")
    return (p, ans, [math.factorial(n), tog, ans + math.factorial(n - 2), math.factorial(n - 1), ans // 2], ["Subtract the arrangements where they are together from all arrangements."], sol)


def pec2(r):
    n = r.randint(4, 8)
    ans = math.factorial(n - 1)
    p = f"In how many ways can ${n}$ people sit around a round table, if two seatings are the same when one is a rotation of the other?"
    sol = explain("seatings around a round table, counting rotations as the same.", "rotating everyone gives the same seating, so pin one person in place to remove the rotations.",
                  [f"Seat one person anywhere; every seat looks the same, so this choice doesn't matter.", f"The other ${n - 1}$ people fill the remaining seats in order: $({n - 1})! = {ans}$ ways.", f"(Equivalently, ${n}!$ row orders divided by ${n}$ rotations.)"],
                  f"${ans}$.", f"answering ${n}! = {math.factorial(n)}$, which counts each seating ${n}$ times.")
    return (p, ans, [math.factorial(n), ans // 2, ans * 2, math.factorial(n - 2), n ** 2], ["Fix one person's seat to remove rotations."], sol)


def pec3(r):
    digits = sorted(r.sample(range(0, 10), r.randint(4, 6)))
    nums = [q for q in itertools.permutations(digits, 3) if q[0] != 0 and q[-1] % 2 == 0]
    ans = len(nums)
    if ans == 0:
        return None
    evens = [d for d in digits if d % 2 == 0]
    k = len(digits)
    lines = []
    for e in evens:
        rest = [d for d in digits if d != e]
        first_ok = len([d for d in rest if d != 0])
        cnt = first_ok * (k - 2)
        lines.append(f"ending in ${e}$: first digit from ${first_ok}$ choices (not ${e}${', not $0$' if 0 in rest else ''}), middle from ${k - 2}$, so ${cnt}$")
    p = f"How many three-digit even numbers can be formed using the digits ${', '.join(map(str, digits))}$, with no digit used twice?"
    sol = explain("three digit even numbers from these digits with no repeats.", "the last digit must be even and the first can't be $0$. Handle the last digit first, splitting into cases.",
                  ["Even digits available for the end: " + ", ".join(f"${e}$" for e in evens) + ".", "Cases: " + "; ".join(lines) + ".", f"Total: ${ans}$."],
                  f"${ans}$.", "forgetting that $0$ can't be the first digit, or that using $0$ at the end frees up the first digit.")
    return (p, ans, [ans + 2, ans * 2, len([q for q in itertools.permutations(digits, 3) if q[0] != 0]), ans - 2 if ans > 2 else ans + 5, math.perm(len(digits), 3)], ["Handle the last digit first (it must be even), being careful with 0, which cannot be first."], sol)


b.fill_unique("basics", [pe1, pe2, pe3, pe4] + MORE[b.skill_id]["basics"], 3201)
b.fill_unique("challenge", [pec1, pec2, pec3] + MORE[b.skill_id]["challenge"], 3202)


# ---------------------------------------------------------------- combinations
b = bank("cp_combinations")


def cb1(r):
    n, k = r.randint(5, 15), r.randint(2, 5)
    if k >= n:
        return None
    ans = comb(n, k)
    p = f"In how many ways can a committee of ${k}$ be chosen from ${n}$ people?"
    sol = explain(f"groups of ${k}$ people, where order doesn't matter.", "count ordered choices, then divide by the number of orders of the same group: $\\binom{n}{k} = \\frac{n!}{k!(n - k)!}$.",
                  [f"Ordered choices: ${' \\cdot '.join(str(n - i) for i in range(k))} = {math.perm(n, k)}$.", f"Each committee was counted ${k}! = {math.factorial(k)}$ times (once per order).", f"$\\frac{{{math.perm(n, k)}}}{{{math.factorial(k)}}} = {ans}$."],
                  f"${ans}$.", f"leaving the answer as ${math.perm(n, k)}$, which treats the same committee chosen in different orders as different.")
    return (p, ans, [math.perm(n, k), n * k, comb(n, k - 1), comb(n + 1, k), ans + n], ["Order does not matter, so use $\\binom{n}{k}$."], sol)


def cb2(r):
    bo, gi = r.randint(4, 9), r.randint(4, 9)
    kb, kg = r.randint(1, 3), r.randint(1, 3)
    ans = comb(bo, kb) * comb(gi, kg)
    p = f"A team of {kb} boy{'s' if kb > 1 else ''} and {kg} girl{'s' if kg > 1 else ''} is chosen from {bo} boys and {gi} girls. How many teams are possible?"
    sol = explain("the number of teams with exactly this mix.", "choose the boys and the girls separately, then multiply (each boy group goes with each girl group).",
                  [f"Boys: $\\binom{{{bo}}}{{{kb}}} = {comb(bo, kb)}$.", f"Girls: $\\binom{{{gi}}}{{{kg}}} = {comb(gi, kg)}$.", f"Teams: ${comb(bo, kb)} \\cdot {comb(gi, kg)} = {ans}$."],
                  f"${ans}$.", f"choosing ${kb + kg}$ from everyone, $\\binom{{{bo + gi}}}{{{kb + kg}}}$, which ignores the required mix.")
    return (p, ans, [comb(bo + gi, kb + kg), comb(bo, kb) + comb(gi, kg), ans * 2, math.perm(bo, kb) * math.perm(gi, kg), ans + 1], ["Choose the boys and the girls separately, then multiply."], sol)


def cb3(r):
    n = r.randint(5, 12)
    ask = r.choice(["handshakes", "diagonals", "triangles"])
    if ask == "handshakes":
        ans = comb(n, 2)
        p = f"${n}$ people each shake hands once with every other person. How many handshakes happen?"
        sol = explain("the number of handshakes.", "a handshake is a pair of people, and order doesn't matter.",
                      [f"Each person shakes ${n - 1}$ hands: ${n} \\cdot {n - 1} = {n * (n - 1)}$, but that counts every handshake twice.", f"$\\frac{{{n * (n - 1)}}}{{2}} = \\binom{{{n}}}{{2}} = {ans}$."], f"${ans}$.", "forgetting to divide by $2$.")
    elif ask == "diagonals":
        ans = n * (n - 3) // 2
        p = f"How many diagonals does a convex polygon with ${n}$ sides have?"
        sol = explain("the number of diagonals.", "every pair of vertices makes a segment; the ones that aren't sides are diagonals.",
                      [f"Pairs of vertices: $\\binom{{{n}}}{{2}} = {comb(n, 2)}$.", f"Subtract the ${n}$ sides: ${comb(n, 2)} - {n} = {ans}$."], f"${ans}$.", "counting the sides as diagonals.")
    else:
        ans = comb(n, 3)
        p = f"${n}$ points lie on a circle. How many triangles have all three vertices among these points?"
        sol = explain("triangles from points on a circle.", "no three points on a circle are in a line, so every choice of $3$ points makes a triangle.",
                      [f"$\\binom{{{n}}}{{3}} = \\frac{{{n} \\cdot {n - 1} \\cdot {n - 2}}}{{6}} = {ans}$."], f"${ans}$.", f"using ${n} \\cdot {n - 1} \\cdot {n - 2}$, which counts each triangle $6$ times.")
    return (p, ans, [n * (n - 1), ans + n, comb(n, 2) if ask != "handshakes" else n * n, ans - 1, math.perm(n, 3) if ask == "triangles" else ans * 2], ["Choose the points (or people) involved; order does not matter."], sol)


def cb4(r):
    n, k = r.randint(4, 12), r.randint(2, 4)
    pos = r.choice([True, False])
    if pos:
        ans = comb(n - 1, k - 1)
        p = f"In how many ways can ${n}$ identical candies be given to ${k}$ children so that each child gets at least one?"
        sol = explain("ways to split identical candies with everyone getting at least one.", "Stars and Bars: line up the candies and place dividers in the gaps between them.",
                      [f"Line up ${n}$ candies. There are ${n - 1}$ gaps between them.", f"Place ${k - 1}$ dividers in different gaps to split them into ${k}$ nonempty groups: $\\binom{{{n - 1}}}{{{k - 1}}} = {ans}$."],
                      f"${ans}$.", f"using $\\binom{{{n + k - 1}}}{{{k - 1}}}$, which allows a child to get zero.")
    else:
        ans = comb(n + k - 1, k - 1)
        p = f"In how many ways can ${n}$ identical candies be given to ${k}$ children (some may get none)?"
        sol = explain("ways to split identical candies, zero allowed.", "Stars and Bars: arrange the candies (stars) and the dividers (bars) in a row.",
                      [f"We need ${k - 1}$ bars to make ${k}$ groups. Together with ${n}$ stars that is ${n + k - 1}$ symbols.", f"Choose which ${k - 1}$ positions are bars: $\\binom{{{n + k - 1}}}{{{k - 1}}} = {ans}$."],
                      f"${ans}$.", f"using ${k}^{{{n}}}$, which treats the candies as different.")
    return (p, ans, [comb(n + k - 1, k - 1) if pos else comb(n - 1, k - 1), k ** n, comb(n, k), ans + 1, comb(n + k, k)], ["Line up the candies and place dividers between them."], sol)


def cbc1(r):
    m, w = r.randint(4, 8), r.randint(3, 7)
    k = r.randint(3, 4)
    ans = comb(m + w, k) - comb(m, k)
    p = f"A committee of ${k}$ is chosen from ${m}$ men and ${w}$ women. How many committees include at least one woman?"
    sol = explain("committees with one or more women.", "complementary counting: 'at least one' is everything minus 'none'.",
                  [f"All committees: $\\binom{{{m + w}}}{{{k}}} = {comb(m + w, k)}$.", f"No women (all men): $\\binom{{{m}}}{{{k}}} = {comb(m, k)}$.", f"At least one woman: ${comb(m + w, k)} - {comb(m, k)} = {ans}$."],
                  f"${ans}$.", f"picking one woman first and then anyone, ${w} \\cdot \\binom{{{m + w - 1}}}{{{k - 1}}}$, which counts committees with several women more than once.")
    return (p, ans, [comb(m + w, k), w * comb(m + w - 1, k - 1), comb(m, k), ans + 1, comb(w, 1) * comb(m, k - 1)], ["Count all committees, then subtract the ones with no women."], sol)


def cbc2(r):
    n, k, cap = r.randint(6, 14), 3, r.randint(3, 6)
    ans = sum(1 for t in itertools.product(range(0, cap + 1), repeat=k) if sum(t) == n)
    if ans == 0:
        return None
    free = comb(n + 2, 2)
    terms = []
    j = 0
    while j <= 3 and n - j * (cap + 1) >= 0:
        terms.append((j, comb(3, j), comb(n - j * (cap + 1) + 2, 2)))
        j += 1
    p = f"How many ordered triples of integers $(a, b, c)$ with $0 \\le a, b, c \\le {cap}$ satisfy $a + b + c = {n}$?"
    sol = explain("solutions with each variable between $0$ and " + f"${cap}$.", "Stars and Bars counts all nonnegative solutions; then subtract the ones where some variable is bigger than " + f"${cap}$ (inclusion and exclusion).",
                  [f"No cap: $\\binom{{{n} + 2}}{{2}} = {free}$ solutions.",
                   f"If $a > {cap}$, set $a' = a - {cap + 1} \\ge 0$; then $a' + b + c = {n - cap - 1}$" + (f", which has $\\binom{{{n - cap - 1 + 2}}}{{2}} = {comb(n - cap + 1, 2)}$ solutions. Same for $b$ and $c$." if n - cap - 1 >= 0 else ", impossible."),
                   "Inclusion and exclusion: $" + " ".join(f"{'-' if j % 2 else '+'} {a_} \\cdot {b_}" for j, a_, b_ in terms).lstrip("+ ") + f" = {ans}$."],
                  f"${ans}$.", f"stopping at ${free}$ and ignoring the cap.")
    return (p, ans, [free, ans + 3, ans - 1 if ans > 1 else ans + 2, free - ans, ans * 2], ["Use stars and bars, then subtract the cases where a variable is too big.", "Or list the possibilities for $a$ and count each case."], sol)


def cbc3(r):
    n = r.randint(5, 12)
    k = r.randint(2, 4)
    ans = comb(n - k + 1, k)
    p = f"How many ${k}$-element subsets of $\\{{1, 2, \\ldots, {n}\\}}$ contain no two consecutive numbers?"
    sol = explain(f"${k}$-element subsets with gaps between all chosen numbers.", "squeeze out the forced gaps: this turns the problem into an ordinary choice with no restriction.",
                  [f"Write the chosen numbers in order: $a_1 < a_2 < \\cdots < a_{{{k}}}$, with each at least $2$ more than the previous.",
                   f"Subtract $0, 1, \\ldots, {k - 1}$: $b_i = a_i - (i - 1)$. Now $b_1 < b_2 < \\cdots$ with no restriction, and the largest is at most ${n} - {k - 1} = {n - k + 1}$.",
                   f"This matches every ${k}$-subset of $\\{{1, \\ldots, {n - k + 1}\\}}$ exactly once: $\\binom{{{n - k + 1}}}{{{k}}} = {ans}$."],
                  f"${ans}$.", f"answering $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$, which includes subsets with consecutive numbers.")
    return (p, ans, [comb(n, k), comb(n - k, k), ans + 1, comb(n - 1, k), ans * 2], ["Subtract $0, 1, 2, \\ldots$ from the chosen numbers in increasing order to remove the gaps."], sol)


b.fill_unique("basics", [cb1, cb2, cb3, cb4] + MORE[b.skill_id]["basics"], 3301)
b.fill_unique("challenge", [cbc1, cbc2, cbc3] + MORE[b.skill_id]["challenge"], 3302)


# ---------------------------------------------------------------- casework and complementary counting
b = bank("cp_casework")


def cw1(r):
    lo, hi = r.choice([(1, 100), (1, 200), (100, 999), (1, 500)])
    d = r.choice(["3", "7", "0", "1", "5"])
    total = hi - lo + 1
    ans = sum(1 for n in range(lo, hi + 1) if d in str(n))
    p = f"How many integers from ${lo}$ to ${hi}$ contain the digit ${d}$ at least once?"
    sol = explain(f"numbers in the range that use the digit ${d}$ somewhere.", f"counting 'at least once' directly needs many cases. Count the numbers with no ${d}$ at all, then subtract.",
                  [f"There are ${total}$ numbers in the range.", f"Numbers with no ${d}$: count digit choices position by position (avoiding ${d}$, and avoiding a leading $0$): ${total - ans}$.", f"At least one ${d}$: ${total} - {total - ans} = {ans}$."],
                  f"${ans}$.", f"double counting numbers like ${d}{d}$ that contain the digit twice.")
    return (p, ans, [ans + 1, ans - 1, total - ans, ans + 9, ans - 10], ["Count the numbers that do NOT contain the digit, then subtract."], sol)


def cw2(r):
    n = r.randint(4, 8)
    ans = 2 ** n - 1 - n
    p = f"A coin is flipped ${n}$ times. In how many of the $2^{{{n}}}$ sequences of heads and tails are there at least two heads?"
    sol = explain("sequences with two or more heads.", "complementary counting: remove the sequences with $0$ or $1$ head.",
                  [f"All sequences: $2^{{{n}}} = {2 ** n}$.", f"Zero heads: $1$ (all tails). Exactly one head: ${n}$ (choose its position).", f"At least two: ${2 ** n} - 1 - {n} = {ans}$."],
                  f"${ans}$.", "forgetting the all tails sequence.")
    return (p, ans, [2 ** n - n, 2 ** n - 1, comb(n, 2), ans + 1, 2 ** (n - 1)], ["Subtract the sequences with zero heads or exactly one head."], sol)


def cw3(r):
    k = r.randint(3, 11)
    pairs = [(a, k - a) for a in range(1, 7) if 1 <= k - a <= 6]
    ans = len(pairs)
    p = f"Two standard dice are rolled, one red and one blue. In how many of the 36 outcomes do the numbers add to ${k}$?"
    sol = explain(f"ordered pairs (red, blue) adding to ${k}$.", "the dice are different colors, so $(1, 2)$ and $(2, 1)$ are different outcomes. List by the red die.",
                  [f"Red $= a$ forces blue $= {k} - a$, which must be from $1$ to $6$.", "Valid pairs: " + ", ".join(f"$({a}, {c})$" for a, c in pairs) + "."],
                  f"${ans}$.", "counting $(a, b)$ and $(b, a)$ as one outcome.")
    return (p, ans, [ans + 1, ans - 1 if ans > 1 else ans + 2, 12 - k if 12 - k != ans else ans + 3, k - 1 if k - 1 != ans else k + 1, 6 if ans != 6 else 5], ["List the pairs (red, blue)."], sol)


def cw4(r):
    N = r.randint(30, 300)
    a, bb = r.sample([2, 3, 5], 2)
    ans = sum(1 for n in range(1, N + 1) if n % a and n % bb)
    p = f"How many integers from $1$ to ${N}$ are divisible by neither ${a}$ nor ${bb}$?"
    sol = explain(f"numbers up to ${N}$ avoiding both ${a}$ and ${bb}$.", "count the numbers divisible by at least one (inclusion and exclusion), then subtract from the total.",
                  [f"Multiples of ${a}$: ${N // a}$. Multiples of ${bb}$: ${N // bb}$. Multiples of both (of ${a * bb}$): ${N // (a * bb)}$.", f"At least one: ${N // a} + {N // bb} - {N // (a * bb)} = {N // a + N // bb - N // (a * bb)}$.", f"Neither: ${N} - {N // a + N // bb - N // (a * bb)} = {ans}$."],
                  f"${ans}$.", "forgetting to add back the multiples of both, which were subtracted twice.")
    return (p, ans, [N - N // a - N // bb, ans + 1, N - ans, ans - 1, N // (a * bb)], ["Subtract the multiples of either number, using inclusion and exclusion for the overlap."], sol)


def cwc1(r):
    P = r.randint(9, 30)
    tris = [(a, bb, c) for a in range(1, P) for bb in range(a, P) for c in [P - a - bb] if c >= bb and a + bb > c]
    ans = len(tris)
    if ans == 0:
        return None
    cs = sorted({t[2] for t in tris})
    p = f"How many non-congruent triangles with integer side lengths have perimeter ${P}$?"
    sol = explain(f"different triangles (up to rearranging sides) with whole number sides and perimeter ${P}$.", "order the sides $a \\le b \\le c$ so each triangle is counted once, and use the triangle inequality $a + b > c$.",
                  [f"Since $a + b > c$ and $a + b + c = {P}$, we need $c < \\frac{{{P}}}{{2}}$. Also $c \\ge \\frac{{{P}}}{{3}}$ because it is the largest side.",
                   "Casework on $c$: " + "; ".join(f"$c = {c}$: " + ", ".join(f"$({x}, {y}, {z})$" for x, y, z in tris if z == c) for c in cs) + "."],
                  f"${ans}$.", "forgetting that $a + b$ must be strictly greater than $c$; equal means the triangle is flat.")
    return (p, ans, [ans + 1, ans - 1 if ans > 1 else ans + 2, ans + 2, P // 3 if P // 3 != ans else ans + 3, ans * 2], ["Order the sides $a \\le b \\le c$ and use the triangle inequality $a + b > c$.", "Do casework on the largest side $c$."], sol)


def cwc2(r):
    n, k = r.randint(5, 20), r.randint(3, 6)
    ask = r.choice(["sum", "prod"])
    if ask == "sum":
        ans = sum(1 for a in range(1, n + 1) for bb in range(1, n + 1) if (a + bb) % k == 0)
        cnt = [sum(1 for x in range(1, n + 1) if x % k == rr) for rr in range(k)]
        p = f"How many ordered pairs $(a, b)$ of integers from $1$ to ${n}$ have $a + b$ divisible by ${k}$?"
        pairs = [f"remainders $({rr}, {(k - rr) % k})$: ${cnt[rr]} \\cdot {cnt[(k - rr) % k]} = {cnt[rr] * cnt[(k - rr) % k]}$" for rr in range(k)]
        sol = explain(f"ordered pairs whose sum is a multiple of ${k}$.", f"$a + b$ is a multiple of ${k}$ exactly when the remainders of $a$ and $b$ add to $0$ or ${k}$. Group the numbers by remainder.",
                      [f"How many of $1, \\ldots, {n}$ have each remainder $0, 1, \\ldots, {k - 1}$: " + ", ".join(map(str, cnt)) + ".", "Matching remainders for $(a, b)$: " + "; ".join(pairs) + ".", f"Total: ${ans}$."],
                      f"${ans}$.", "counting unordered pairs, or forgetting pairs where $a = b$.")
        hint = f"Group the numbers by remainder mod ${k}$."
    else:
        odd = (n + 1) // 2
        ans = n * n - odd * odd
        p = f"How many ordered pairs $(a, b)$ of integers from $1$ to ${n}$ have an even product $ab$?"
        sol = explain("ordered pairs with an even product.", "a product is odd only when both numbers are odd. Count the complement.",
                      [f"All pairs: ${n}^2 = {n * n}$.", f"Odd numbers from $1$ to ${n}$: ${odd}$. Both odd: ${odd}^2 = {odd * odd}$ pairs.", f"Even product: ${n * n} - {odd * odd} = {ans}$."],
                      f"${ans}$.", "thinking both numbers must be even for an even product. One even factor is enough.")
        hint = "Count pairs with both numbers odd, and subtract."
    return (p, ans, [ans + 1, ans - 1, n * n - ans, ans + n, ans // 2], [hint], sol)


def cwc3(r):
    n = r.randint(5, 14)
    f = [1, 1]
    for _ in range(n):
        f.append(f[-1] + f[-2])
    ans = f[n]
    p = f"In how many ways can you climb a staircase of ${n}$ steps if you take either 1 or 2 steps at a time? (Order matters.)"
    sol = explain("the number of step sequences that add to " + f"${n}$.", "think about the last move: it is either a single step (from step $n - 1$) or a double step (from step $n - 2$). So $w(n) = w(n - 1) + w(n - 2)$.",
                  ["Start: $w(1) = 1$ and $w(2) = 2$ ($1 + 1$ or $2$).", "Build up: " + ", ".join(f"$w({i}) = {f[i]}$" for i in range(3, n + 1)) + "."],
                  f"${ans}$.", f"using $2^{{{n - 1}}}$ or listing by hand and missing sequences.")
    return (p, ans, [f[n - 1], f[n + 1], 2 ** (n - 1), ans + 1, n * (n - 1) // 2], ["Let $w(n)$ be the number of ways. The last move is 1 step or 2 steps, so $w(n) = w(n - 1) + w(n - 2)$."], sol)


b.fill_unique("basics", [cw1, cw2, cw3, cw4] + MORE[b.skill_id]["basics"], 3401)
b.fill_unique("challenge", [cwc1, cwc2, cwc3] + MORE[b.skill_id]["challenge"], 3402)


# ---------------------------------------------------------------- inclusion and exclusion
b = bank("cp_inclusion")


def ie1(r):
    tot = r.randint(25, 60)
    a, bb = r.randint(8, tot - 5), r.randint(8, tot - 5)
    both = r.randint(max(0, a + bb - tot), min(a, bb))
    neither = tot - (a + bb - both)
    s1, s2, verb = r.choice([("soccer", "basketball", "play"), ("French", "Spanish", "take"), ("band", "choir", "are in"), ("math club", "chess club", "are in")])
    p = f"In a class of ${tot}$ students, ${a}$ {verb} {s1}, ${bb}$ {verb} {s2}, and ${both}$ {verb} both. How many {verb} neither?"
    sol = explain("students in neither group.", "Inclusion and Exclusion: students in at least one group $=$ group 1 $+$ group 2 $-$ both (because those were counted twice).",
                  [f"At least one: ${a} + {bb} - {both} = {a + bb - both}$.", f"Neither: ${tot} - {a + bb - both} = {neither}$."],
                  f"${neither}$.", f"subtracting both groups from the total without adding back the ${both}$ counted twice.")
    return (p, neither, [tot - a - bb if tot - a - bb >= 0 else neither + 3, neither + both, a + bb - both, neither + 1, both], ["Students in either group: add the two groups and subtract the overlap."], sol)


def ie2(r):
    N = r.randint(50, 500)
    a, bb, c = r.choice([(2, 3, 5), (2, 3, 7), (3, 5, 7), (2, 5, 7)])
    s1 = N // a + N // bb + N // c
    s2 = N // (a * bb) + N // (a * c) + N // (bb * c)
    s3 = N // (a * bb * c)
    ans = s1 - s2 + s3
    p = f"How many integers from $1$ to ${N}$ are divisible by at least one of ${a}$, ${bb}$, or ${c}$?"
    sol = explain("numbers divisible by at least one of the three.", "Inclusion and Exclusion for three sets: add singles, subtract pairs, add back the triple.",
                  [f"Singles: ${N // a} + {N // bb} + {N // c} = {s1}$.", f"Pairs (multiples of ${a * bb}$, ${a * c}$, ${bb * c}$): ${N // (a * bb)} + {N // (a * c)} + {N // (bb * c)} = {s2}$.",
                   f"Triple (multiples of ${a * bb * c}$): ${s3}$.", f"${s1} - {s2} + {s3} = {ans}$."],
                  f"${ans}$.", "forgetting to add back the triple overlap, which was subtracted three times after being added three times.")
    return (p, ans, [s1, ans + 1, N - ans, ans - 1, ans + s3], ["Add the three counts, subtract the pairwise overlaps, then add back the triple overlap."], sol)


def ie3(r):
    tot = r.randint(30, 80)
    both = r.randint(2, 10)
    onlyA, onlyB = r.randint(3, 20), r.randint(3, 20)
    neither = tot - both - onlyA - onlyB
    if neither < 0:
        return None
    a, bb = onlyA + both, onlyB + both
    p = f"Out of ${tot}$ people surveyed, ${a}$ like tea, ${bb}$ like coffee, and ${neither}$ like neither. How many like both?"
    sol = explain("the overlap (people who like both).", "people who like at least one $=$ tea $+$ coffee $-$ both. Solve for both.",
                  [f"At least one: ${tot} - {neither} = {tot - neither}$.", f"${tot - neither} = {a} + {bb} - \\text{{both}}$, so both $= {a + bb} - {tot - neither} = {both}$."],
                  f"${both}$.", f"answering ${a + bb - tot}$ by forgetting the people who like neither.")
    return (p, both, [a + bb - tot, both + 1, tot - neither, onlyA, both - 1 if both > 1 else both + 2], ["People who like at least one: total minus neither. Compare with tea plus coffee."], sol)


def ie4(r):
    tot = r.randint(30, 60)
    a, bb = r.randint(10, 25), r.randint(10, 25)
    both = r.randint(1, min(a, bb) - 1)
    if a + bb - both > tot:
        return None
    ans = a + bb - 2 * both
    p = f"Of ${tot}$ students, ${a}$ take art, ${bb}$ take music, and ${both}$ take both. How many take exactly one of the two?"
    sol = explain("students in exactly one class.", "remove the overlap from each group separately.",
                  [f"Only art: ${a} - {both} = {a - both}$.", f"Only music: ${bb} - {both} = {bb - both}$.", f"Exactly one: ${a - both} + {bb - both} = {ans}$."],
                  f"${ans}$.", f"answering ${a + bb - both}$, which also includes students taking both.")
    return (p, ans, [a + bb - both, a + bb, ans + both, tot - ans, ans - 1], ["Remove the students in both from each group."], sol)


def iec1(r):
    n = r.randint(3, 6)
    ans = sum(1 for pmt in itertools.permutations(range(n)) if all(pmt[i] != i for i in range(n)))
    terms = [((-1) ** k) * math.factorial(n) // math.factorial(k) for k in range(n + 1)]
    p = f"${n}$ friends each bring a gift and put it in a pile. Each friend then takes one gift at random. In how many ways can the gifts be handed out so that no one gets their own gift?"
    sol = explain("handouts where nobody gets their own gift (a derangement).", "Inclusion and Exclusion: start with all handouts, subtract those where some given person gets their own, add back those where two do, and so on.",
                  [f"All handouts: ${n}! = {math.factorial(n)}$.", f"For $k$ chosen people fixed, the rest can be anything: $\\binom{{{n}}}{{k}}({n} - k)!$ handouts, which equals $\\frac{{{n}!}}{{k!}}$.",
                   "Alternate signs: $" + " ".join(f"{'+' if t >= 0 else '-'} {abs(t)}" for t in terms).lstrip("+ ") + f" = {ans}$."],
                  f"${ans}$.", f"answering ${math.factorial(n)} - 1$, which only removes the case where everyone gets their own.")
    return (p, ans, [math.factorial(n) - 1, math.factorial(n - 1), ans + 1, math.factorial(n) // 2, ans - 1], ["Use inclusion and exclusion on the friends who get their own gift."], sol)


def iec2(r):
    n, k = r.randint(4, 6), r.choice([2, 3])
    ans = sum(1 for f in itertools.product(range(k), repeat=n) if len(set(f)) == k)
    p = f"In how many ways can ${n}$ different toys be given to ${k}$ children so that every child gets at least one toy?"
    if k == 2:
        steps = [f"All ways: each toy goes to one of $2$ children, $2^{{{n}}} = {2 ** n}$.", "Bad ways: all toys to one child: $2$.", f"Good: ${2 ** n} - 2 = {ans}$."]
    else:
        steps = [f"All ways: $3^{{{n}}} = {3 ** n}$.", f"Some specific child gets nothing: $2^{{{n}}}$ ways, for each of $3$ children: $3 \\cdot {2 ** n} = {3 * 2 ** n}$.",
                 f"Two specific children get nothing (all to the third): $1$ way, for each of $3$ pairs: $3$. These were subtracted twice, so add them back.", f"Good: ${3 ** n} - {3 * 2 ** n} + 3 = {ans}$."]
    sol = explain("handouts where no child is left out.", "count all handouts, then use inclusion and exclusion to remove those that miss a child.", steps, f"${ans}$.", f"using Stars and Bars, $\\binom{{{n - 1}}}{{{k - 1}}}$. That is for identical items; these toys are different.")
    return (p, ans, [k ** n, k ** n - k, comb(n - 1, k - 1), ans + k, math.perm(n, k)], ["Count all ways, then subtract the ways that leave some child out (inclusion and exclusion)."], sol)


def iec3(r):
    A, B, Cc = r.randint(15, 30), r.randint(15, 30), r.randint(15, 30)
    ab, ac, bc = r.randint(4, 9), r.randint(4, 9), r.randint(4, 9)
    abc = r.randint(1, min(ab, ac, bc) - 1)
    union = A + B + Cc - ab - ac - bc + abc
    p = (f"In a survey, ${A}$ people read magazine A, ${B}$ read B, and ${Cc}$ read C. ${ab}$ read A and B, ${ac}$ read A and C, ${bc}$ read B and C, "
         f"and ${union}$ people read at least one. How many read all three?")
    sol = explain("the number who read all three, $x$.", "Inclusion and Exclusion for three sets: $|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|$.",
                  [f"Plug in: ${union} = {A} + {B} + {Cc} - {ab} - {ac} - {bc} + x$.", f"Simplify: ${union} = {A + B + Cc - ab - ac - bc} + x$, so $x = {abc}$."],
                  f"${abc}$.", "forgetting the $+x$ term, or adding the pairwise overlaps instead of subtracting them.")
    return (p, abc, [abc + 1, abc + 2, A + B + Cc - union, abc - 1 if abc > 1 else abc + 3, ab + ac + bc - union % 10], ["Write the inclusion and exclusion formula for three sets and solve for the triple overlap."], sol)


b.fill_unique("basics", [ie1, ie2, ie3, ie4] + MORE[b.skill_id]["basics"], 3501)
b.fill_unique("challenge", [iec1, iec2, iec3] + MORE[b.skill_id]["challenge"], 3502)


# ---------------------------------------------------------------- probability
b = bank("cp_probability")


def pr1(r):
    red, blue, green = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    tot = red + blue + green
    ans = F(red, tot)
    p = f"A bag holds ${red}$ red, ${blue}$ blue, and ${green}$ green marbles. One marble is drawn at random. What is the probability it is red?"
    sol = explain("the chance of drawing red.", "with equally likely outcomes, probability $= \\frac{\\text{favorable}}{\\text{total}}$.",
                  [f"Total marbles: ${red} + {blue} + {green} = {tot}$.", f"Red: ${red}$. Probability: $\\frac{{{red}}}{{{tot}}} = {num(ans).tex}$."], f"${num(ans).tex}$.", "dividing red by the non red marbles (that is the odds, not the probability).")
    return (p, ans, [F(red, blue + green), F(1, 3), F(blue + green, tot), F(red, tot - 1), F(red + 1, tot)], ["Probability is favorable outcomes over total outcomes."], sol)


def pr2(r):
    k = r.randint(2, 12)
    pairs = [(a, k - a) for a in range(1, 7) if 1 <= k - a <= 6]
    ways = len(pairs)
    ans = F(ways, 36)
    p = f"Two fair six-sided dice are rolled. What is the probability that the sum is ${k}$?"
    sol = explain(f"the chance the dice add to ${k}$.", "there are $36$ equally likely ordered outcomes (first die, second die).",
                  ["Pairs that work: " + ", ".join(f"$({a}, {c})$" for a, c in pairs) + f" (${ways}$ of them).", f"Probability: $\\frac{{{ways}}}{{36}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "treating the $11$ possible sums as equally likely. They are not: middle sums happen more often.")
    return (p, ans, [F(1, 11), F(ways, 21), F(ways + 1, 36), F(1, 6) if ans != F(1, 6) else F(1, 9), F(ways, 12)], ["There are 36 equally likely ordered outcomes."], sol)


def pr3(r):
    red, blue = r.randint(3, 9), r.randint(3, 9)
    tot = red + blue
    ans = F(red, tot) * F(red - 1, tot - 1)
    p = f"A box has ${red}$ red and ${blue}$ blue balls. Two balls are drawn without replacement. What is the probability both are red?"
    sol = explain("the chance both draws are red.", "multiply the chance of the first event by the chance of the second given the first. Without replacement, the box changes after the first draw.",
                  [f"First red: $\\frac{{{red}}}{{{tot}}}$.", f"Then ${red - 1}$ red remain out of ${tot - 1}$: $\\frac{{{red - 1}}}{{{tot - 1}}}$.", f"Both: $\\frac{{{red}}}{{{tot}}} \\cdot \\frac{{{red - 1}}}{{{tot - 1}}} = {num(ans).tex}$. (Or $\\frac{{\\binom{{{red}}}{{2}}}}{{\\binom{{{tot}}}{{2}}}}$.)"],
                  f"${num(ans).tex}$.", f"squaring $\\frac{{{red}}}{{{tot}}}$, which assumes the ball is put back.")
    return (p, ans, [F(red, tot) ** 2, F(red, tot), F(red - 1, tot), ans * 2, F(comb(red, 2), comb(tot, 2) + 1)], ["Multiply: the first draw, then the second draw from what is left."], sol)


def pr4(r):
    n = r.randint(3, 7)
    k = r.randint(0, n)
    ans = F(comb(n, k), 2 ** n)
    p = f"A fair coin is flipped ${n}$ times. What is the probability of getting exactly ${k}$ heads?"
    sol = explain(f"the chance of exactly ${k}$ heads.", "all $2^n$ sequences are equally likely; count those with the right number of heads.",
                  [f"Sequences: $2^{{{n}}} = {2 ** n}$.", f"Choose which ${k}$ flips are heads: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$.", f"Probability: $\\frac{{{comb(n, k)}}}{{{2 ** n}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "answering $\\frac{1}{2^n}$, which is the chance of one specific sequence.")
    return (p, ans, [F(1, 2), F(k, n) if k else F(1, n), F(1, 2 ** n), F(comb(n, k), 2 ** (n - 1)), F(comb(n, k) + 1, 2 ** n)], ["Count the sequences with exactly that many heads, over $2^n$."], sol)


def prc1(r):
    n = r.randint(2, 4)
    ans = 1 - F(5, 6) ** n
    p = f"A fair die is rolled ${n}$ times. What is the probability of rolling at least one 6?"
    sol = explain("the chance of one or more sixes.", "'at least one' is easiest through the complement: $1 - P(\\text{none})$.",
                  [f"No six on one roll: $\\frac{{5}}{{6}}$. On all ${n}$ rolls: $\\left(\\frac{{5}}{{6}}\\right)^{{{n}}} = {num(F(5, 6) ** n).tex}$.", f"At least one six: $1 - {num(F(5, 6) ** n).tex} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"adding $\\frac{{1}}{{6}}$ ${n}$ times to get $\\frac{{{n}}}{{6}}$. That double counts rolls with two sixes.")
    return (p, ans, [F(n, 6), F(5, 6) ** n, F(1, 6) ** n, 1 - F(1, 6) ** n, ans + F(1, 36)], ["Find the probability of no sixes, then subtract from 1."], sol)


def prc2(r):
    pr = r.choice([F(1, 2), F(2, 3), F(1, 3), F(3, 4), F(3, 5), F(2, 5)])
    q = 1 - pr
    ans = pr ** 2 + 2 * pr * pr * q
    p = f"Team A beats Team B in any single game with probability ${num(pr).tex}$, independently. They play until one team wins two games. What is the probability Team A wins?"
    sol = explain("the chance Team A wins the series.", "list the ways A can win: 2 to 0, or 2 to 1. For 2 to 1, A must win the last game and split the first two.",
                  [f"Win 2 to 0: $p^2 = {num(pr * pr).tex}$.", f"Win 2 to 1: the loss is in game 1 or game 2 ($2$ orders), then A wins game 3: $2 \\cdot p \\cdot (1 - p) \\cdot p = {num(2 * pr * pr * q).tex}$.",
                   f"Total: ${num(pr * pr).tex} + {num(2 * pr * pr * q).tex} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "including orders where A wins the first two and then a third game is played; the series stops at two wins.")
    return (p, ans, [pr ** 2, pr, pr ** 2 + pr * pr * q, 1 - ans, ans + F(1, 27)], ["Team A wins 2 to 0, or wins 2 to 1 (losing one of the first two games)."], sol)


def prc3(r):
    n = r.randint(5, 10)
    combos = list(itertools.combinations(range(1, n + 1), 3))
    odd = (n + 1) // 2
    ev = n // 2
    ask = r.choice(["even_sum", "odd_prod"])
    if ask == "even_sum":
        fav = sum(1 for c in combos if sum(c) % 2 == 0)
        p = f"Three different numbers are chosen at random from $\\{{1, 2, \\ldots, {n}\\}}$. What is the probability that their sum is even?"
        steps = [f"There are ${odd}$ odd and ${ev}$ even numbers, and $\\binom{{{n}}}{{3}} = {len(combos)}$ choices.", "The sum is even when the number of odd numbers chosen is $0$ or $2$.",
                 f"No odds: $\\binom{{{ev}}}{{3}} = {comb(ev, 3)}$. Two odds: $\\binom{{{odd}}}{{2}}\\binom{{{ev}}}{{1}} = {comb(odd, 2) * ev}$. Total ${fav}$."]
    else:
        fav = sum(1 for c in combos if (c[0] * c[1] * c[2]) % 2 == 1)
        p = f"Three different numbers are chosen at random from $\\{{1, 2, \\ldots, {n}\\}}$. What is the probability that their product is odd?"
        steps = [f"There are ${odd}$ odd numbers, and $\\binom{{{n}}}{{3}} = {len(combos)}$ choices.", "A product is odd only when all three numbers are odd.", f"All odd: $\\binom{{{odd}}}{{3}} = {fav}$."]
    ans = F(fav, len(combos))
    steps.append(f"Probability: $\\frac{{{fav}}}{{{len(combos)}}} = {num(ans).tex}$.")
    sol = explain("a probability about the parity of three chosen numbers.", "parity only depends on how many of the chosen numbers are odd. Count by that.", steps, f"${num(ans).tex}$.", "assuming the answer is $\\frac{1}{2}$ by symmetry; the counts of odd and even numbers may differ.")
    return (p, ans, [F(1, 2) if ans != F(1, 2) else F(1, 3), 1 - ans if 1 - ans != ans else F(2, 3), F(fav, len(combos) + 1), F(1, 8), ans + F(1, len(combos))], ["Count by how many of the chosen numbers are odd."], sol)


b.fill_unique("basics", [pr1, pr2, pr3, pr4] + MORE[b.skill_id]["basics"], 3601)
b.fill_unique("challenge", [prc1, prc2, prc3] + MORE[b.skill_id]["challenge"], 3602)


# ---------------------------------------------------------------- expected value
b = bank("cp_expected")


def ev1(r):
    sides = r.choice([4, 6, 8, 10, 12, 20])
    ans = F(sides + 1, 2)
    p = f"What is the expected value of a roll of a fair ${sides}$-sided die numbered $1$ through ${sides}$?"
    sol = explain("the average roll in the long run.", "expected value $= \\sum (\\text{value}) \\times (\\text{probability})$. With equally likely values it is just the average.",
                  [f"Each face has probability $\\frac{{1}}{{{sides}}}$.", f"$E = \\frac{{1 + 2 + \\cdots + {sides}}}{{{sides}}} = \\frac{{{sides * (sides + 1) // 2}}}{{{sides}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering $\\frac{{{sides}}}{{2}}$. The values start at $1$, not $0$.")
    return (p, ans, [F(sides, 2), sides, ans + 1, F(sides - 1, 2), F(sides + 2, 2)], ["Average all the equally likely outcomes."], sol)


def ev2(r):
    win, cost = r.choice([(10, 3), (20, 5), (6, 2), (12, 4), (30, 8), (15, 4)])
    pr = r.choice([F(1, 4), F(1, 5), F(1, 3), F(1, 6), F(2, 5)])
    ans = pr * win - cost
    p = f"A game costs \\${cost} to play. With probability ${num(pr).tex}$ you win \\${win}; otherwise you win nothing. What is the expected net gain, in dollars?"
    sol = explain("the average profit per game.", "expected winnings minus the cost (you pay the cost every time).",
                  [f"Expected winnings: ${num(pr).tex} \\cdot {win} = {num(pr * win).tex}$.", f"Net: ${num(pr * win).tex} - {cost} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "subtracting the cost only when you lose. You pay it whether you win or not.")
    return (p, ans, [pr * win, win - cost, -cost, ans + 1, pr * (win - cost)], ["Expected winnings minus the cost."], sol)


def ev3(r):
    n = r.randint(4, 20)
    pr = r.choice([F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(2, 3)])
    ans = n * pr
    p = f"A spinner lands on blue with probability ${num(pr).tex}$. It is spun ${n}$ times. What is the expected number of blue results?"
    sol = explain("the average number of blues over many repeats of the whole experiment.", "linearity of expectation: each spin adds its probability of blue to the expected count.",
                  [f"Each spin contributes ${num(pr).tex}$ on average.", f"${n}$ spins: ${n} \\cdot {num(pr).tex} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "thinking the expected value must be a whole number. It is an average.")
    return (p, ans, [pr, n * pr + 1, n - n * pr, F(n, 2), n * pr * pr], ["Expected count is the number of trials times the probability."], sol)


def ev4(r):
    vals = sorted(r.sample(range(1, 20), 3))
    probs = r.choice([(F(1, 2), F(1, 3), F(1, 6)), (F(1, 4), F(1, 4), F(1, 2)), (F(1, 5), F(2, 5), F(2, 5)), (F(1, 3), F(1, 3), F(1, 3))])
    ans = sum(v * q for v, q in zip(vals, probs))
    p = (f"A prize wheel pays \\${vals[0]} with probability ${num(probs[0]).tex}$, \\${vals[1]} with probability ${num(probs[1]).tex}$, "
         f"and \\${vals[2]} with probability ${num(probs[2]).tex}$. What is the expected payout, in dollars?")
    sol = explain("the average payout.", "multiply each payout by its probability, then add.",
                  ["Products: " + ", ".join(f"${v} \\cdot {num(q).tex} = {num(v * q).tex}$" for v, q in zip(vals, probs)) + ".", f"Sum: ${' + '.join(num(v * q).tex for v, q in zip(vals, probs))} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "averaging the three payouts equally, which ignores the different probabilities.")
    return (p, ans, [F(sum(vals), 3) if F(sum(vals), 3) != ans else ans + 2, ans + 1, vals[1], max(vals) * max(probs), ans - F(1, 2)], ["Multiply each payout by its probability and add."], sol)


def evc1(r):
    k = r.choice([2, 3, 4, 5, 6, 8, 10])
    p = f"A weighted coin with probability ${num(F(1, k)).tex}$ of landing heads is flipped until the first heads appears. What is the expected number of flips?"
    sol = explain("the average number of flips to the first heads.", "condition on the first flip. Let $E$ be the expected number of flips.",
                  [f"The first flip always counts as $1$. With probability ${num(F(1, k)).tex}$ it is heads and we stop.", f"With probability ${num(1 - F(1, k)).tex}$ it is tails, and we start over, needing $E$ more flips on average.",
                   f"So $E = 1 + {num(1 - F(1, k)).tex}E$. Then ${num(F(1, k)).tex}E = 1$ and $E = {k}$."],
                  f"${k}$.", f"answering ${k - 1}$ by not counting the successful flip itself.")
    return (p, k, [k - 1, k + 1, F(k, 2), 2 * k, F(1, k)], ["Let $E$ be the expected number. After one flip, with probability $1 - p$ you are back where you started."], sol)


def evc2(r):
    n = r.randint(5, 12)
    ask = r.choice(["fixed", "adjacent"])
    if ask == "fixed":
        ans = F(1)
        p = f"${n}$ letters are put into ${n}$ addressed envelopes at random, one per envelope. What is the expected number of letters in the correct envelope?"
        sol = explain("the average number of correctly placed letters.", "linearity of expectation: add up, letter by letter, the chance each one is correct. The events don't need to be independent.",
                      [f"Any single letter lands in its own envelope with probability $\\frac{{1}}{{{n}}}$.", f"Add over all ${n}$ letters: ${n} \\cdot \\frac{{1}}{{{n}}} = 1$."],
                      "$1$.", "trying to find the full probability distribution. Linearity skips all that.")
        wrong = [F(1, n), F(n, 2), F(1, 2), 2, F(n - 1, n)]
    else:
        ans = F(n - 1, 4)
        p = f"A fair coin is flipped ${n}$ times. What is the expected number of times a head is immediately followed by a tail?"
        sol = explain("the average number of HT patterns.", "linearity of expectation: add the probability of HT at each spot.",
                      [f"There are ${n - 1}$ neighboring pairs (flips 1 and 2, 2 and 3, ...).", "Each pair is HT with probability $\\frac{1}{2} \\cdot \\frac{1}{2} = \\frac{1}{4}$.", f"Expected count: ${n - 1} \\cdot \\frac{{1}}{{4}} = {num(ans).tex}$."],
                      f"${num(ans).tex}$.", f"using ${n}$ pairs instead of ${n - 1}$.")
        wrong = [F(n, 4), F(n - 1, 2), F(n, 2), F(1, 4), ans + 1]
    return (p, ans, wrong, ["Use linearity of expectation: add the probabilities of each small event."], sol)


def evc3(r):
    sides = r.choice([4, 6, 8])
    which = r.choice(["max", "min"])
    f = max if which == "max" else min
    outs = [(a, bb) for a in range(1, sides + 1) for bb in range(1, sides + 1)]
    ans = F(sum(f(a, bb) for a, bb in outs), sides * sides)
    counts = [sum(1 for a, bb in outs if f(a, bb) == v) for v in range(1, sides + 1)]
    p = f"Two fair ${sides}$-sided dice (numbered $1$ to ${sides}$) are rolled. What is the expected value of the {'larger' if which == 'max' else 'smaller'} of the two numbers?"
    rule = "The larger equals $v$ in $2v - 1$ outcomes (one die shows $v$, the other at most $v$)." if which == "max" else f"The smaller equals $v$ in $2({sides} - v) + 1$ outcomes."
    sol = explain(f"the average of the {'larger' if which == 'max' else 'smaller'} die.", "find how many of the equally likely outcomes give each value, then take the weighted average.",
                  [f"There are ${sides * sides}$ outcomes.", rule + " Counts for $v = 1, 2, \\ldots$: " + ", ".join(map(str, counts)) + ".",
                   "$E = \\frac{" + " + ".join(f"{v} \\cdot {c}" for v, c in zip(range(1, sides + 1), counts)) + f"}}{{{sides * sides}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering the single die average ${num(F(sides + 1, 2)).tex}$.")
    return (p, ans, [F(sides + 1, 2), ans + F(1, 2), sides + 1 - ans, ans - F(1, sides), F(sides, 2) + 1], ["Find the probability the result equals each value $k$, or the probability it is at least $k$."], sol)


b.fill_unique("basics", [ev1, ev2, ev3, ev4] + MORE[b.skill_id]["basics"], 3701)
b.fill_unique("challenge", [evc1, evc2, evc3] + MORE[b.skill_id]["challenge"], 3702)


# ---------------------------------------------------------------- geometric probability
b = bank("cp_geometric")


def gp1(r):
    a, bb = sorted(r.sample(range(0, 20), 2))
    L = r.randint(bb + 1, 30)
    ans = F(bb - a, L)
    p = f"A number is chosen uniformly at random from the interval $[0, {L}]$. What is the probability it is between ${a}$ and ${bb}$?"
    sol = explain("the chance a random point lands in a smaller interval.", "for a uniform choice, probability $=$ (length of the good part) $\\div$ (total length).",
                  [f"Good length: ${bb} - {a} = {bb - a}$. Total length: ${L}$.", f"Probability: $\\frac{{{bb - a}}}{{{L}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "counting whole numbers in the interval; the number can be any real value.")
    return (p, ans, [F(bb, L), F(a, L) if a else F(1, L), F(bb - a, L + 1), 1 - ans, F(bb - a + 1, L)], ["Probability is the length of the good interval over the total length."], sol)


def gp2(r):
    s = r.randint(2, 10)
    rad = F(s, 2)
    ans = C("\\frac{\\pi}{4}", math.pi / 4)
    wrong = [C("\\frac{\\pi}{2}", math.pi / 2), C("\\frac{1}{4}", 0.25), C("\\frac{\\pi}{" + str(s) + "}", math.pi / s) if s != 4 else C("\\frac{3}{4}", 0.75), C("\\frac{\\pi}{8}", math.pi / 8), C("\\frac{2}{\\pi}", 2 / math.pi)]
    p = f"A point is chosen at random inside a square of side ${s}$. What is the probability it lies inside the circle inscribed in the square?"
    sol = explain("the chance a random point in the square is also in the circle.", "probability $=$ circle area $\\div$ square area.",
                  [f"The inscribed circle has diameter ${s}$, so radius ${num(rad).tex}$ and area $\\pi \\cdot {num(rad).tex}^2 = {num(rad * rad).tex}\\pi$.", f"Square area: ${s * s}$.", f"Ratio: $\\frac{{{num(rad * rad).tex}\\pi}}{{{s * s}}} = \\frac{{\\pi}}{{4}}$. (The side length cancels; it is always $\\frac{{\\pi}}{{4}}$.)"],
                  "$\\frac{\\pi}{4}$.", f"using ${s}$ as the radius.")
    return (p, ans, wrong, ["Divide the circle's area by the square's area."], sol)


def gp3(r):
    w, h = r.randint(2, 10), r.randint(2, 10)
    if w >= h:
        area = w * h - F(h * h, 2)
        shape = f"the rectangle minus the triangle above $y = x$ (legs ${h}$ and ${h}$): ${w * h} - \\frac{{{h}^2}}{{2}} = {num(area).tex}$"
    else:
        area = F(w * w, 2)
        shape = f"the triangle below $y = x$ with legs ${w}$ and ${w}$: $\\frac{{{w}^2}}{{2}} = {num(area).tex}$"
    ans = area / (w * h)
    p = f"A point $(x, y)$ is chosen at random in the rectangle with $0 \\le x \\le {w}$ and $0 \\le y \\le {h}$. What is the probability that $x > y$?"
    sol = explain("the chance the point is below the line $y = x$.", "probability $=$ good area $\\div$ total area. Draw the line $y = x$ through the rectangle.",
                  [f"Total area: ${w * h}$.", f"Good region ($x > y$): {shape}.", f"Probability: $\\frac{{{num(area).tex}}}{{{w * h}}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", "assuming the answer is $\\frac{1}{2}$; that only holds for a square.")
    return (p, ans, [F(1, 2) if ans != F(1, 2) else F(1, 3), 1 - ans if 1 - ans != ans else F(2, 3), F(w, w + h), ans + F(1, 10), F(min(w, h), max(w, h))], ["Sketch the line $y = x$ and find the area of the part of the rectangle below it."], sol)


def gp4(r):
    k = r.choice([10, 12, 15, 20, 30])
    t = r.randint(1, k - 1)
    ans = F(t, k)
    p = f"Buses arrive exactly every ${k}$ minutes. You arrive at the stop at a random time. What is the probability you wait less than ${t}$ minutes?"
    sol = explain(f"the chance your wait is under ${t}$ minutes.", f"your wait is equally likely to be anything from $0$ to ${k}$ minutes, so this is a length ratio.",
                  [f"Good waits: $0$ to ${t}$ minutes, length ${t}$.", f"Probability: $\\frac{{{t}}}{{{k}}} = {num(ans).tex}$."], f"${num(ans).tex}$.", f"computing $\\frac{{{k - t}}}{{{k}}}$, the chance of waiting longer.")
    return (p, ans, [F(k - t, k), F(t, 60), F(1, 2) if ans != F(1, 2) else F(1, 3), F(t, k + 1), ans + F(1, k)], ["Your wait is equally likely to be any time from 0 to the gap between buses."], sol)


def gpc1(r):
    a = r.choice([F(1, 2), F(1, 3), F(2, 3), F(3, 2), F(4, 3), F(5, 4), F(3, 4)])
    if a <= 1:
        ans = a * a / 2
        shape = f"the triangle below $x + y = {num(a).tex}$, with legs ${num(a).tex}$: area $\\frac{{({num(a).tex})^2}}{{2}} = {num(ans).tex}$"
    else:
        ans = 1 - (2 - a) ** 2 / 2
        shape = f"the whole square minus the corner triangle above the line, whose legs are $2 - {num(a).tex} = {num(2 - a).tex}$: $1 - \\frac{{({num(2 - a).tex})^2}}{{2}} = {num(ans).tex}$"
    p = f"Two numbers $x$ and $y$ are chosen independently and uniformly from $[0, 1]$. What is the probability that $x + y < {num(a).tex}$?"
    sol = explain("the chance the sum is below " + f"${num(a).tex}$.", "every pair $(x, y)$ is a point in the unit square (area $1$), so probability equals area.",
                  [f"The line $x + y = {num(a).tex}$ cuts the square.", f"Good region: {shape}.", f"Probability $= {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering $\\frac{{{num(a).tex}}}{{2}}$, as if the sum were uniform. It is more likely to be near $1$.")
    return (p, ans, [a / 2, a * a if a * a < 1 else F(1, 2), 1 - ans, ans + F(1, 8), F(1, 2) if ans != F(1, 2) else F(1, 3)], ["Draw the unit square and the line $x + y = $ constant. Find the area on the correct side."], sol)


def gpc2(r):
    t = r.choice([10, 15, 20, 30])
    miss = (60 - t) ** 2
    ans = 1 - F(miss, 3600)
    p = f"Two friends each arrive at a cafe at a random time between 1:00 and 2:00. Each waits ${t}$ minutes for the other, then leaves. What is the probability that they meet?"
    sol = explain("the chance their visits overlap.", "plot the two arrival times (minutes after 1:00) as a point in a $60 \\times 60$ square. They meet when the times differ by at most " + str(t) + ".",
                  [f"Total area: $60 \\cdot 60 = 3600$.", f"They miss when $|x - y| > {t}$: two corner triangles, each with legs $60 - {t} = {60 - t}$. Together: $2 \\cdot \\frac{{{60 - t}^2}}{{2}} = {miss}$.",
                   f"Meet: $1 - \\frac{{{miss}}}{{3600}} = {num(ans).tex}$."],
                  f"${num(ans).tex}$.", f"answering $\\frac{{{t}}}{{60}}$ or $\\frac{{{2 * t}}}{{60}}$, which treats the problem as one dimensional.")
    return (p, ans, [F(t, 60), F(2 * t, 60), F(miss, 3600), ans + F(1, 36), F(t, 30)], ["Plot both arrival times on a $60 \\times 60$ square. They meet when $|x - y| \\le " + str(t) + "$."], sol)


def gpc3(r):
    s = r.randint(2, 8)
    d = r.randint(1, s)
    k = F(d * d, 4 * s * s)
    tex = f"\\frac{{{k.numerator}\\pi}}{{{k.denominator}}}" if k.numerator != 1 else f"\\frac{{\\pi}}{{{k.denominator}}}"
    ans = C(tex, float(k) * math.pi)
    p = f"A point is chosen at random inside a square of side ${s}$. What is the probability that it is within ${d}$ unit{'s' if d > 1 else ''} of a particular corner?"
    wrong = [C(f"\\frac{{{d}}}{{{s}}}", d / s), C(f"\\frac{{{F(d * d, s * s).numerator}\\pi}}{{{F(d * d, s * s).denominator}}}", float(F(d * d, s * s)) * math.pi),
             C(f"\\frac{{{F(d * d, 2 * s * s).numerator}\\pi}}{{{F(d * d, 2 * s * s).denominator}}}", float(F(d * d, 2 * s * s)) * math.pi),
             C(f"\\frac{{{F(d * d, 4 * s * s).numerator}}}{{{F(d * d, 4 * s * s).denominator}}}", float(F(d * d, 4 * s * s)))]
    sol = explain("the chance the point is close to one corner.", "points within distance $d$ of a corner form a circle of radius $d$; inside the square only a quarter of it fits.",
                  [f"Quarter circle area: $\\frac{{1}}{{4}}\\pi \\cdot {d}^2 = \\frac{{{d * d}\\pi}}{{4}}$.", f"Square area: ${s * s}$.", f"Probability: $\\frac{{{d * d}\\pi}}{{4 \\cdot {s * s}}} = {tex}$."],
                  f"${tex}$.", "using the full circle instead of a quarter.")
    return (p, ans, wrong, ["The points within a distance of the corner form a quarter circle inside the square."], sol)


b.fill_unique("basics", [gp1, gp2, gp3, gp4] + MORE[b.skill_id]["basics"], 3801)
b.fill_unique("challenge", [gpc1, gpc2, gpc3] + MORE[b.skill_id]["challenge"], 3802)
