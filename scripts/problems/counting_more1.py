"""Extra Counting problem types (part 1): counting principle, permutations, combinations, casework."""
import itertools
import math
from collections import Counter
from fractions import Fraction as F

from common import NAMES, C, Q, comb, num, var

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def big(v):
    return f"{v:,}".replace(",", "{,}")


def B(v):
    """A large integer choice shown with thousands separators."""
    return C(big(v), v)


# ================================================================ cp_counting
S = "cp_counting"


@reg(S, "basics")
def ct_menu_optional(r):
    a, m, d = r.randint(2, 6), r.randint(3, 8), r.randint(2, 5)
    ans = a * m * (d + 1)
    p = f"A dinner special includes one of ${a}$ appetizers and one of ${m}$ main dishes. Dessert is optional: a diner may pick one of ${d}$ desserts or skip it. How many different dinners are possible?"
    return Q(p, ans, [a * m * d, a + m + d, a * m + d, ans + 1, a * m * (d + 2)], "Skipping dessert counts as one more dessert choice.",
             "the number of dinners.", "multiply the choices; 'no dessert' is an extra option for dessert.",
             [f"Dessert choices: ${d}$ desserts plus 'none' $= {d + 1}$.", f"Total: ${a} \\cdot {m} \\cdot {d + 1} = {ans}$."], "forgetting the option to skip dessert.")


@reg(S, "basics")
def ct_repetition_code(r):
    k = r.randint(3, 6)
    n = r.randint(2, 5)
    letters = "ABCDE"[:n]
    p = f"A code is ${k}$ characters long, and each character is one of the letters ${', '.join(letters)}$ (repeats allowed). How many codes are possible?"
    return Q(p, n ** k, [k ** n, n * k, math.perm(n, min(n, k)) if math.perm(n, min(n, k)) != n ** k else n ** k + 1, n ** (k - 1), comb(n + k - 1, k)], "Each character is chosen independently.",
             "the number of codes.", f"${n}$ choices for each of ${k}$ positions.",
             [f"${n}^{{{k}}} = {n ** k}$."], "computing " + f"${k}^{{{n}}}$" + " (exponent and base swapped).")


@reg(S, "basics")
def ct_divisible_3digit(r):
    k = r.choice([2, 4, 5, 10, 25])
    ans = 999 // k - 99 // k
    p = f"How many three-digit numbers are divisible by ${k}$?"
    return Q(p, ans, [ans + 1, 900 // k + 1 if 900 // k + 1 != ans else ans - 1, 1000 // k, ans * 2, 999 // k], "Count multiples up to $999$ and subtract those up to $99$.",
             "the count.", "multiples of $k$ up to $N$: $\\lfloor N/k \\rfloor$.",
             [f"Up to $999$: ${999 // k}$. Up to $99$: ${99 // k}$.", f"Three-digit: ${ans}$."], "including $1000$ or a two-digit multiple.")


@reg(S, "basics")
def ct_roads(r):
    a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(1, 4)
    ans = a * b + c
    p = f"There are ${a}$ roads from town A to town B, ${b}$ roads from B to C, and ${c}$ direct road{'s' if c > 1 else ''} from A to C. How many routes go from A to C without passing through any town twice?"
    return Q(p, ans, [a * b * c, a + b + c, a * b, (a + c) * b, ans + 1], "Split into cases: through B, or direct.",
             "the number of routes.", "routes through B use the multiplication principle; direct routes add on.",
             [f"Through B: ${a} \\cdot {b} = {a * b}$.", f"Direct: ${c}$.", f"Total: ${ans}$."], "multiplying all three numbers.")


@reg(S, "basics")
def ct_sandwich(r):
    b, m, t = r.randint(2, 5), r.randint(2, 6), r.randint(3, 6)
    ans = b * m * 2 ** t
    p = f"A sandwich uses one of ${b}$ breads, one of ${m}$ meats, and any combination of ${t}$ toppings (including none or all). How many sandwiches are possible?"
    return Q(p, ans, [b * m * t, b * m * (t + 1), b + m + 2 ** t, b * m * 2 ** (t - 1), b * m * (2 ** t - 1)], "Each topping is either on or off.",
             "the number of sandwiches.", f"each of ${t}$ toppings has $2$ states (on or off), giving $2^{{{t}}}$ topping combinations.",
             [f"Toppings: $2^{{{t}}} = {2 ** t}$.", f"Total: ${b} \\cdot {m} \\cdot {2 ** t} = {ans}$."], "multiplying by the number of toppings instead of $2^" + str(t) + "$.")


@reg(S, "basics")
def ct_nonzero_first(r):
    L, D = r.randint(1, 3), r.randint(3, 5)
    ans = 26 ** L * 9 * 10 ** (D - 1)
    p = f"A license plate is ${L}$ letter{'s' if L > 1 else ''} followed by ${D}$ digits. The first digit can't be $0$. Repeats are allowed. How many plates are possible?"
    return Q(p, B(ans), [B(26 ** L * 10 ** D), B(26 ** L * 9 ** D), B(26 * L * 9 * 10 * (D - 1)), B(ans + 26 ** L)], "Only the first digit has a restriction.",
             "the number of plates.", "multiply choices position by position.",
             [f"Letters: $26^{{{L}}}$. First digit: $9$. Other digits: $10^{{{D - 1}}}$.", f"Total: ${big(ans)}$."], "allowing $0$ as the first digit.", ans_tex=big(ans))


@reg(S, "basics")
def ct_test_answers(r):
    n = r.randint(4, 10)
    k = r.choice([4, 5])
    ans = (k + 1) ** n
    p = f"A quiz has ${n}$ multiple-choice questions, each with ${k}$ choices. A student may also leave any question blank. In how many ways can the student fill out the answer sheet?"
    return Q(p, B(ans), [B(k ** n), B((k + 1) * n), B(n ** (k + 1)), B(ans - 1)], "Blank is a sixth option for each question." if k == 5 else "Blank is a fifth option.",
             "the number of answer sheets.", f"each question has ${k}$ answers plus blank: ${k + 1}$ options.",
             [f"$({k + 1})^{{{n}}} = {big(ans)}$."], "forgetting the blank option.", ans_tex=big(ans))


@reg(S, "basics")
def ct_subsets(r):
    n = r.randint(4, 12)
    ask = r.choice(["all", "nonempty"])
    ans = 2 ** n if ask == "all" else 2 ** n - 1
    p = f"How many {'subsets' if ask == 'all' else 'nonempty subsets'} does a set with ${n}$ elements have?"
    return Q(p, ans, [2 ** n - 1 if ask == "all" else 2 ** n, n * n, 2 * n, math.factorial(n) if math.factorial(n) < 10 ** 6 else 2 ** (n + 1), 2 ** (n - 1)], "Each element is either in or out.",
             "the number of subsets.", "for each element choose in or out: $2^n$ choices" + (", minus the empty set." if ask != "all" else ", including the empty set."),
             [f"$2^{{{n}}} = {2 ** n}$" + (f", minus $1$ for the empty set: ${ans}$." if ask != "all" else ".")], "forgetting the empty set, or including it when asked to exclude it.")


@reg(S, "basics")
def ct_through_point(r):
    m, n = r.randint(3, 7), r.randint(3, 7)
    a, b = r.randint(1, m - 1), r.randint(1, n - 1)
    ans = comb(a + b, a) * comb(m - a + n - b, m - a)
    p = f"How many shortest paths along grid lines go from $(0, 0)$ to $({m}, {n})$ and pass through $({a}, {b})$? (Each step is one unit right or one unit up.)"
    return Q(p, ans, [comb(a + b, a) + comb(m - a + n - b, m - a), comb(m + n, m), comb(m + n, m) - ans, ans + 1, comb(a + b, a)], "Count each leg, then multiply.",
             "the paths through the point.", "a path through the point is a path to it followed by a path from it.",
             [f"To $({a}, {b})$: $\\binom{{{a + b}}}{{{a}}} = {comb(a + b, a)}$.", f"From there: $\\binom{{{m - a + n - b}}}{{{m - a}}} = {comb(m - a + n - b, m - a)}$.", f"Product: ${ans}$."], "adding the two legs.")


@reg(S, "basics")
def ct_forbidden_pair(r):
    s, pn = r.randint(3, 8), r.randint(3, 8)
    ans = s * pn - 1
    n = r.choice(NAMES)
    p = f"{n} has ${s}$ shirts and ${pn}$ pairs of pants, but refuses to wear the red shirt with the green pants. How many outfits are left?"
    return Q(p, ans, [s * pn, s * pn - s, s * pn - pn, (s - 1) * (pn - 1), s + pn - 1], "Count all outfits, then remove the forbidden one.",
             "the number of allowed outfits.", "complementary counting: all outfits minus the one forbidden combination.",
             [f"All: ${s} \\cdot {pn} = {s * pn}$.", f"Minus $1$: ${ans}$."], "removing every outfit with the red shirt.")


@reg(S, "basics")
def ct_increasing_units(r):
    k = r.choice(["greater than", "less than"])
    ans = 9 * 45
    p = f"How many three-digit numbers have a units digit {k} its tens digit?"
    return Q(p, ans, [9 * 50, 9 * 55, 45, 900 // 2, 9 * 36], "For each tens digit, count the units digits that work.",
             "the count.", "the hundreds digit is free (9 choices); the tens and units digits form a pair with the right order.",
             [f"Pairs (tens, units) of different digits: $10 \\cdot 9 = 90$; exactly half have units {k} tens: $45$.", f"With $9$ hundreds digits: $9 \\cdot 45 = {ans}$."], "including pairs where the two digits are equal.")


@reg(S, "basics")
def ct_distinct_dice(r):
    k = r.randint(2, 4)
    ans = math.perm(6, k)
    p = f"${k}$ dice of different colors are rolled. In how many of the $6^{{{k}}}$ outcomes do all the dice show different numbers?"
    return Q(p, ans, [6 ** k - ans, comb(6, k), 6 ** k, ans + 6, 6 * k], "First die anything, second die one fewer option, ...",
             "the number of outcomes with all different numbers.", "the dice are distinguishable, so order matters: choose for each die in turn.",
             [" \\cdot ".join(str(6 - i) for i in range(k)).join(["$", f" = {ans}$."])], "using combinations, which ignore which die shows which number.")


@reg(S, "basics")
def ct_phone(r):
    L = r.randint(4, 7)
    ans = 8 * 10 ** (L - 1)
    p = f"A phone number has ${L}$ digits and cannot start with $0$ or $1$. How many phone numbers are possible?"
    return Q(p, B(ans), [B(10 ** L), B(9 * 10 ** (L - 1)), B(8 ** L), B(10 ** L - 2)], "Only the first digit is restricted.",
             "the count.", "first digit: $8$ choices ($2$ to $9$); the others: $10$ each.",
             [f"$8 \\cdot 10^{{{L - 1}}} = {big(ans)}$."], "subtracting just $2$ from the total.", ans_tex=big(ans))


@reg(S, "basics")
def ct_squares_board(r):
    n = r.randint(3, 10)
    ans = sum(k * k for k in range(1, n + 1))
    p = f"How many squares of all sizes are on an ${n} \\times {n}$ checkerboard?"
    return Q(p, ans, [n * n, ans - n * n, comb(n + 1, 2) ** 2, ans + n, n * (n + 1) // 2], "Count $1 \\times 1$, $2 \\times 2$, ... separately.",
             "the total number of squares.", f"a $k \\times k$ square fits in $({n} - k + 1)^2$ positions.",
             ["Sizes: " + ", ".join(f"${k} \\times {k}$: ${(n - k + 1) ** 2}$" for k in range(1, n + 1)) + ".", f"Total: $1^2 + 2^2 + \\cdots + {n}^2 = {ans}$."], "counting only the unit squares.")


@reg(S, "basics")
def ct_prizes_repeat(r):
    k, n = r.randint(2, 4), r.randint(3, 8)
    ans = n ** k
    p = f"${k}$ different prizes are each given to one of ${n}$ students, and a student may win more than one prize. In how many ways can the prizes be given out?"
    return Q(p, ans, [k ** n, math.perm(n, k), comb(n, k), n * k, comb(n + k - 1, k)], "Decide prize by prize.",
             "the number of ways.", f"each prize independently goes to one of ${n}$ students.",
             [f"${n}^{{{k}}} = {ans}$."], "computing " + f"${k}^{{{n}}}$" + " (each student choosing a prize).")


@reg(S, "basics")
def ct_palindromes(r):
    L = r.randint(3, 7)
    ans = 9 * 10 ** ((L + 1) // 2 - 1)
    p = f"A palindrome reads the same forwards and backwards, like $12321$. How many ${L}$-digit palindromes are there?"
    return Q(p, B(ans), [B(10 ** ((L + 1) // 2)), B(9 * 10 ** (L // 2)) if L % 2 else B(ans * 10), B(9 * 10 ** (L - 1)), B(ans - 9) if ans > 9 else B(ans + 10)], "The first half determines the whole number.",
             "the count.", f"choosing the first $\\left\\lceil \\frac{{{L}}}{{2}} \\right\\rceil = {(L + 1) // 2}$ digits fixes the rest.",
             [f"First digit: $9$ choices (not $0$). The next ${(L + 1) // 2 - 1}$ digits: $10$ each.", f"$9 \\cdot 10^{{{(L + 1) // 2 - 1}}} = {big(ans)}$."], "letting the first digit be $0$.", ans_tex=big(ans))


@reg(S, "challenge")
def ctc_dominoes(r):
    n = r.randint(4, 12)
    f = [1, 1]
    for _ in range(n):
        f.append(f[-1] + f[-2])
    ans = f[n]
    p = f"In how many ways can a $2 \\times {n}$ strip be completely covered by $1 \\times 2$ dominoes?"
    return Q(p, ans, [f[n - 1], f[n + 1], 2 ** (n - 1), ans + 1, n], "Look at the left end: one vertical domino, or two horizontal ones stacked.",
             "the number of tilings.", "the left end is either a vertical domino (leaving $2 \\times (n - 1)$) or two stacked horizontal dominoes (leaving $2 \\times (n - 2)$): $T(n) = T(n - 1) + T(n - 2)$.",
             ["$T(1) = 1$, $T(2) = 2$.", "Build up: " + ", ".join(f"$T({i}) = {f[i]}$" for i in range(3, n + 1)) + "."], "forgetting the stacked-horizontal case.")


@reg(S, "challenge")
def ctc_3d_paths(r):
    a, b, c = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    ans = math.factorial(a + b + c) // (math.factorial(a) * math.factorial(b) * math.factorial(c))
    p = f"A bug moves from $(0, 0, 0)$ to $({a}, {b}, {c})$, each step increasing exactly one coordinate by $1$. How many paths can it take?"
    return Q(p, ans, [comb(a + b + c, a) * comb(b + c, b) * 2 if comb(a + b + c, a) * comb(b + c, b) * 2 != ans else ans + 1, 3 ** (a + b + c), comb(a + b + c, a) + comb(b + c, b), math.factorial(a + b + c), ans * 2],
             "Each path is an arrangement of " + f"{a} x's, {b} y's, {c} z's" + ".", "the number of paths.", "count arrangements of the step letters, dividing out repeated letters.",
             [f"Total steps: ${a + b + c}$.", f"$\\frac{{{a + b + c}!}}{{{a}! \\, {b}! \\, {c}!}} = {ans}$."], "using $3^{" + str(a + b + c) + "}$, which allows any number of each step.")


@reg(S, "challenge")
def ctc_coin_amounts(r):
    q, d, n_ = r.randint(1, 3), r.randint(1, 4), r.randint(1, 3)
    amts = {25 * x + 10 * y + 5 * z for x in range(q + 1) for y in range(d + 1) for z in range(n_ + 1)} - {0}
    p = f"Using some of ${q}$ quarter{'s' if q > 1 else ''}, ${d}$ dime{'s' if d > 1 else ''}, and ${n_}$ nickel{'s' if n_ > 1 else ''} (at least one coin), how many different amounts of money can be made?"
    tot = (q + 1) * (d + 1) * (n_ + 1) - 1
    return Q(p, len(amts), [tot, len(amts) + 1, len(amts) - 1, tot - len(amts) if tot - len(amts) not in (len(amts), tot) else tot + 1, q + d + n_], "Different coin choices can give the same amount (two dimes and a nickel equal a quarter).",
             "the number of distinct amounts.", "every amount is a multiple of $5$ cents; list which multiples are reachable.",
             [f"Total value of all the coins: ${25 * q + 10 * d + 5 * n_}$ cents.", f"Checking each multiple of $5$ from $5$ up: ${len(amts)}$ are reachable.", f"There are ${tot}$ coin choices, but some give the same amount."],
             "counting coin choices instead of amounts.")


@reg(S, "challenge")
def ctc_subset_chain(r):
    n = r.randint(3, 10)
    p = f"How many ordered pairs of sets $(A, B)$ satisfy $A \\subseteq B \\subseteq \\{{1, 2, \\ldots, {n}\\}}$?"
    return Q(p, B(3 ** n), [B(2 ** n), B(4 ** n), B(2 ** (2 * n - 1)), B(3 ** n - 1)], "Decide, for each element, where it goes.",
             "the number of pairs.", "each element is in neither set, in $B$ only, or in both. It can't be in $A$ without $B$.",
             [f"$3$ choices for each of ${n}$ elements: $3^{{{n}}} = {big(3 ** n)}$."], "using $4$ choices per element, which allows elements in $A$ but not $B$.", ans_tex=big(3 ** n))


@reg(S, "challenge")
def ctc_distinct_digits(r):
    k = r.randint(2, 5)
    ans = sum(9 * math.perm(9, d - 1) for d in range(1, k + 1))
    p = f"How many positive integers less than $10^{{{k}}}$ have all different digits?"
    return Q(p, B(ans), [B(9 * math.perm(9, k - 1)), B(10 ** k - 1), B(ans + 1), B(sum(math.perm(10, d) for d in range(1, k + 1)))], "Split by number of digits.",
             "the count.", "count $d$-digit numbers with distinct digits for $d = 1$ to " + str(k) + "; the first digit can't be $0$.",
             [", ".join(f"${d}$-digit: $9 \\cdot {'' if d == 1 else ' \\cdot '.join(str(9 - i) for i in range(d - 1))} = {9 * math.perm(9, d - 1)}$" if d > 1 else "$1$-digit: $9$" for d in range(1, k + 1)) + ".", f"Total: ${big(ans)}$."],
             "allowing $0$ as a leading digit.", ans_tex=big(ans))


@reg(S, "challenge")
def ctc_delannoy(r):
    m, n = r.randint(2, 5), r.randint(2, 5)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            D[i][j] = 1 if i == 0 or j == 0 else D[i - 1][j] + D[i][j - 1] + D[i - 1][j - 1]
    ans = D[m][n]
    p = f"A king moves from $(0, 0)$ to $({m}, {n})$ using steps of one unit right, one unit up, or one unit diagonally up and right. How many paths are there?"
    return Q(p, ans, [comb(m + n, m), 3 ** max(m, n), ans + 1, ans - comb(m + n, m) if ans - comb(m + n, m) > 0 else ans + 2, 2 * comb(m + n, m)], "Count paths to each point by adding the three points it can come from.",
             "the number of paths.", "paths to $(i, j)$ = paths to $(i - 1, j)$ + paths to $(i, j - 1)$ + paths to $(i - 1, j - 1)$.",
             ["Points on the axes have exactly $1$ path.", "Filling the grid row by row: " + "; ".join(f"row ${j}$: " + ", ".join(str(D[i][j]) for i in range(m + 1)) for j in range(n + 1)) + ".", f"At $({m}, {n})$: ${ans}$."],
             "forgetting the diagonal steps.")


@reg(S, "challenge")
def ctc_restricted_digits(r):
    N = r.randint(100, 3000)
    digits = sorted(r.sample(range(1, 10), 3))
    xs = [x for x in range(1, N + 1) if set(str(x)) <= set(map(str, digits))]
    p = f"How many integers from $1$ to ${N}$ use only the digits ${', '.join(map(str, digits))}$?"
    return Q(p, len(xs), [len(xs) + 1, 3 ** len(str(N)), len(xs) - 1, sum(3 ** k for k in range(1, len(str(N)) + 1)), len(xs) + 3], "Count by number of digits; be careful with the top end.",
             "the count.", "each $k$-digit number made from these digits gives $3^k$ choices, but numbers above " + str(N) + " must be removed.",
             [f"Shorter numbers: " + " + ".join(f"3^{{{k}}}" for k in range(1, len(str(N)))).join(["$", "$"]) + f" $= {sum(3 ** k for k in range(1, len(str(N))))}$.", f"${len(str(N))}$-digit ones at most ${N}$: ${len(xs) - sum(3 ** k for k in range(1, len(str(N))))}$.", f"Total: ${len(xs)}$."],
             "counting all " + str(len(str(N))) + "-digit numbers from these digits, even those above " + str(N) + ".")


# ================================================================ cp_permutations
S = "cp_permutations"


@reg(S, "basics")
def pe_fixed_first(r):
    n = r.randint(4, 9)
    nm = r.choice(NAMES)
    p = f"${n}$ students, including {nm}, line up for a photo. In how many orders is {nm} first in line?"
    return Q(p, math.factorial(n - 1), [math.factorial(n), math.factorial(n) // 2, math.factorial(n - 2), n, (n - 1) * (n - 1)], "Put " + nm + " first; arrange the rest.",
             "the number of orders.", f"with {nm} fixed in front, the other ${n - 1}$ can be in any order.",
             [f"$({n - 1})! = {math.factorial(n - 1)}$."], "multiplying by " + str(n) + " for " + nm + "'s position, which is already fixed.")


@reg(S, "basics")
def pe_vowels_together(r):
    word = r.choice(["FORMAT", "TRIANGLE", "PLANET", "MOUSE", "CHAIR", "GRAPHITE", "DOUBLE", "FIGURE", "COUSIN", "BRAVE"])
    if len(set(word)) != len(word):
        return None
    v = [c for c in word if c in "AEIOU"]
    k, n = len(v), len(word)
    ans = math.factorial(n - k + 1) * math.factorial(k)
    p = f"In how many arrangements of the letters of {word} are all the vowels next to each other?"
    return Q(p, ans, [math.factorial(n - k + 1), math.factorial(n), math.factorial(n) - ans, ans * 2, math.factorial(n - k) * math.factorial(k)], "Glue the vowels into one block.",
             "the number of arrangements.", f"treat the ${k}$ vowels ({', '.join(v)}) as one block, then arrange the block internally.",
             [f"Units: ${n - k}$ consonants + $1$ block $= {n - k + 1}$: $({n - k + 1})! = {math.factorial(n - k + 1)}$.", f"Inside the block: ${k}! = {math.factorial(k)}$.", f"Total: ${ans}$."],
             "forgetting to arrange the vowels inside the block.")


@reg(S, "basics")
def pe_alternate(r):
    b = r.randint(2, 6)
    g = b + r.choice([0, 1])
    ans = (2 if b == g else 1) * math.factorial(b) * math.factorial(g)
    p = f"${b}$ boys and ${g}$ girls line up so that boys and girls alternate. How many orders are possible?"
    return Q(p, ans, [math.factorial(b) * math.factorial(g) * (1 if b == g else 2), math.factorial(b + g), ans + 1, math.factorial(b + g) // 2, b * g], "Fix the pattern first (who goes first), then arrange each group.",
             "the number of orders.", "the pattern of B and G positions is forced " + ("up to which group starts." if b == g else "(the larger group must be at both ends)."),
             [("Patterns: $2$ (start with a boy or a girl). " if b == g else "Pattern: girls at both ends, so only $1$. ") + f"Boys: ${b}! = {math.factorial(b)}$; girls: ${g}! = {math.factorial(g)}$.", f"Total: ${ans}$."],
             "forgetting the factor of 2 when the groups are equal (or adding it when they aren't).")


@reg(S, "basics")
def pe_two_ends(r):
    n = r.randint(4, 9)
    a, b = r.sample(NAMES, 2)
    ans = 2 * math.factorial(n - 2)
    p = f"${n}$ people, including {a} and {b}, line up. In how many orders are {a} and {b} at the two ends of the line?"
    return Q(p, ans, [math.factorial(n - 2), math.factorial(n), 2 * math.factorial(n - 1), ans + 2, n * (n - 1)], "Place " + a + " and " + b + " first.",
             "the number of orders.", f"{a} and {b} take the ends in $2$ ways; the rest fill the middle.",
             [f"Ends: $2$ ways.", f"Middle: $({n - 2})! = {math.factorial(n - 2)}$.", f"Total: ${ans}$."], "forgetting that the two could swap ends.")


@reg(S, "basics")
def pe_block_fixed_order(r):
    n = r.randint(5, 9)
    k = r.randint(2, 4)
    ans = math.factorial(n - k + 1)
    p = f"${n}$ different books go on a shelf. ${k}$ of them form a series that must stay together in order (volume 1, then 2, ...). How many arrangements are possible?"
    return Q(p, ans, [ans * math.factorial(k), math.factorial(n), math.factorial(n - k), math.factorial(n) // math.factorial(k), ans + 1], "The series acts as one block that can't be rearranged.",
             "the number of arrangements.", "glue the series into one block; its internal order is fixed.",
             [f"Units: ${n - k} + 1 = {n - k + 1}$.", f"$({n - k + 1})! = {ans}$."], "multiplying by " + str(k) + "! for the series, whose order is fixed.")


@reg(S, "basics")
def pe_even_digits(r):
    n = r.randint(4, 7)
    evens = n // 2
    ans = evens * math.factorial(n - 1)
    p = f"The digits $1, 2, \\ldots, {n}$ are each used once to form a ${n}$-digit number. How many such numbers are even?"
    return Q(p, ans, [math.factorial(n) // 2 if math.factorial(n) // 2 != ans else ans + 1, math.factorial(n), (n - evens) * math.factorial(n - 1), math.factorial(n - 1), ans // 2], "The last digit must be even.",
             "the count of even numbers.", "choose the last digit first (it must be even), then arrange the rest.",
             [f"Even digits available: ${evens}$.", f"Then the other ${n - 1}$ digits in any order: ${evens} \\cdot ({n - 1})! = {ans}$."], "assuming exactly half the numbers are even, which fails when " + str(n) + " is odd." if n % 2 else "multiplying by the number of odd digits.")


@reg(S, "basics")
def pe_before(r):
    n = r.randint(3, 8)
    ans = math.factorial(n) // 2
    a, b = r.sample(NAMES, 2)
    p = f"${n}$ runners, including {a} and {b}, finish a race with no ties. In how many finishing orders does {a} finish ahead of {b}?"
    return Q(p, ans, [math.factorial(n), math.factorial(n - 1), math.factorial(n - 2), ans - 1, math.factorial(n) // 3], "Pair each order with the one where " + a + " and " + b + " swap.",
             "the number of orders.", f"swapping {a} and {b} matches each order with {a} ahead to one with {b} ahead.",
             [f"All orders: ${n}! = {math.factorial(n)}$.", f"Exactly half have {a} ahead: ${ans}$."], "fixing them in adjacent spots.")


@reg(S, "basics")
def pe_last_not_first(r):
    n = r.randint(4, 8)
    a, b = r.sample(NAMES, 2)
    ans = math.factorial(n - 1) - math.factorial(n - 2)
    p = f"${n}$ runners form a relay team. {a} must run last, and {b} refuses to run first. How many running orders are possible?"
    return Q(p, ans, [math.factorial(n - 1), math.factorial(n - 2), math.factorial(n) - math.factorial(n - 1), ans + math.factorial(n - 2) * 2, (n - 2) * math.factorial(n - 2) - 1], "Fix " + a + " last, then remove orders with " + b + " first.",
             "the number of orders.", f"place {a}, then use complementary counting for {b}.",
             [f"With {a} last: $({n - 1})! = {math.factorial(n - 1)}$ orders.", f"Of those, {b} first: $({n - 2})! = {math.factorial(n - 2)}$.", f"Allowed: ${ans}$."], "subtracting the cases with " + b + " first from all " + str(n) + "! orders.")


def pe_div5(r):
    n = r.randint(5, 8)
    ans = math.factorial(n - 1)
    p = f"The digits $1, 2, \\ldots, {n}$ are each used once to make a ${n}$-digit number. How many such numbers are divisible by $5$?"
    return Q(p, ans, [math.factorial(n) // 5, math.factorial(n), ans * 2, math.factorial(n - 2), ans + 1], "What must the last digit be?",
             "the count.", "divisible by $5$ means the last digit is $0$ or $5$; only $5$ is available.",
             [f"Last digit: $5$.", f"The other ${n - 1}$ digits: $({n - 1})! = {ans}$."], "dividing the total by 5.")


@reg(S, "basics")
def pe_two_rows(r):
    k = r.randint(2, 6)
    ans = math.factorial(k) ** 2
    p = f"${2 * k}$ students of different heights pose in two rows of ${k}$. The ${k}$ shortest must be in front. How many arrangements are possible?"
    return Q(p, ans, [math.factorial(2 * k), comb(2 * k, k), 2 * ans, math.factorial(k), ans * comb(2 * k, k)], "The rows are decided; only the order within each row varies.",
             "the number of arrangements.", "the front row is fixed as a group; arrange within each row.",
             [f"Front row: ${k}! = {math.factorial(k)}$. Back row: ${k}! = {math.factorial(k)}$.", f"Total: ${ans}$."], "also choosing who goes in front, which is already decided.")


@reg(S, "basics")
def pe_start_vowel(r):
    word = r.choice(["ORANGE", "ISLAND", "ACTOR", "UNDER", "EXPLAIN", "OCEAN", "AUTHOR", "OUTLINE", "IDEAL"])
    if len(set(word)) != len(word):
        return None
    v = [c for c in word if c in "AEIOU"]
    n = len(word)
    ans = len(v) * math.factorial(n - 1)
    p = f"How many arrangements of the letters of {word} begin with a vowel?"
    return Q(p, ans, [math.factorial(n), math.factorial(n - 1), (n - len(v)) * math.factorial(n - 1), ans // 2, len(v) * math.factorial(n - 2)], "Choose the first letter, then arrange the rest.",
             "the count.", "first letter: one of the vowels; the rest: any order.",
             [f"Vowels: {', '.join(v)} (${len(v)}$ choices).", f"Remaining ${n - 1}$ letters: $({n - 1})! = {math.factorial(n - 1)}$.", f"Total: ${ans}$."], "counting the vowels as consonants or vice versa.")


@reg(S, "basics")
def pe_three_order(r):
    n = r.randint(4, 8)
    ans = math.factorial(n) // 6
    p = f"${n}$ different tasks are done one at a time. Task A must come before task B, and B before task C. How many orders are possible?"
    return Q(p, ans, [math.factorial(n) // 2, math.factorial(n) // 3, math.factorial(n - 3), ans * 2, math.factorial(n)], "Only one of the $3! = 6$ orders of A, B, C is allowed.",
             "the number of orders.", "by symmetry, each of the $6$ relative orders of A, B, C happens equally often.",
             [f"All orders: ${n}! = {math.factorial(n)}$.", f"One sixth: ${ans}$."], "dividing by $3$ instead of $6$.")


@reg(S, "basics")
def pe_opposite(r):
    n = r.choice([6, 8, 10])
    a, b = r.sample(NAMES, 2)
    ans = math.factorial(n - 2)
    p = f"${n}$ people sit at a round table with ${n}$ evenly spaced seats; rotations count as the same seating. In how many seatings do {a} and {b} sit directly across from each other?"
    return Q(p, ans, [math.factorial(n - 1), 2 * math.factorial(n - 2), math.factorial(n - 1) // (n - 1), ans + 1, math.factorial(n - 3)], "Seat " + a + " first to remove rotations.",
             "the number of seatings.", f"fix {a}'s seat (this removes rotations); {b}'s seat is then forced.",
             [f"{a} anywhere; {b} directly across: $1$ way.", f"The other ${n - 2}$ fill the rest: $({n - 2})! = {ans}$."], "multiplying by 2 for " + b + "'s position, which is forced.")


@reg(S, "basics")
def pe_pair_together(r):
    word = r.choice(["LETTER", "BALLET", "COFFEE", "BUTTON", "PEPPER", "APPLE", "GALLON", "RABBIT"])
    cnt = Counter(word)
    dbl = [c for c, v in cnt.items() if v == 2]
    if not dbl:
        return None
    ch = dbl[0]
    merged = word.replace(ch * 2, "#", 1) if ch * 2 in word else word.replace(ch, "", 1).replace(ch, "#", 1)
    c2 = Counter(merged)
    total = math.factorial(len(merged))
    for v in c2.values():
        total //= math.factorial(v)
    full = math.factorial(len(word))
    for v in cnt.values():
        full //= math.factorial(v)
    p = f"In how many arrangements of the letters of {word} are the two {ch}'s next to each other?"
    return Q(p, total, [full, full - total, total * 2, total // 2 if total % 2 == 0 else total + 1, math.factorial(len(word) - 1)], "Glue the two " + ch + "'s together.",
             "the count.", f"treat {ch}{ch} as one tile; then divide out any other repeated letters.",
             [f"Tiles: ${len(merged)}$ (with {ch}{ch} as one).", "Other repeats: " + (", ".join(f"{c} $\\times {v}$" for c, v in c2.items() if v > 1 and c != "#") or "none") + ".", f"Arrangements: ${total}$."],
             "multiplying by 2 for the order of the identical letters inside the tile.")


@reg(S, "basics")
def pe_choose_include(r):
    n = r.randint(6, 10)
    k = r.randint(3, 4)
    ans = k * math.perm(n - 1, k - 1)
    nm = r.choice(NAMES)
    p = f"{nm} chooses ${k}$ of ${n}$ different books and arranges them in a row on a shelf. A particular book must be among them. How many arrangements are possible?"
    return Q(p, ans, [math.perm(n, k), math.perm(n - 1, k - 1), comb(n - 1, k - 1), ans + k, math.perm(n, k) - ans], "Choose where the required book goes, then fill the other spots.",
             "the number of arrangements.", f"the required book takes one of ${k}$ positions; the other ${k - 1}$ spots are filled in order from the remaining ${n - 1}$ books.",
             [f"Position of the required book: ${k}$ ways.", f"Other spots: ${' \\cdot '.join(str(n - 1 - i) for i in range(k - 1))} = {math.perm(n - 1, k - 1)}$.", f"Total: ${ans}$."], "forgetting that the required book can be in any position.")


@reg(S, "basics")
def pe_couples(r):
    n = r.randint(2, 5)
    ans = math.factorial(n) * 2 ** n
    p = f"${n}$ couples sit in a row of ${2 * n}$ seats so that each couple sits together. How many seatings are possible?"
    return Q(p, ans, [math.factorial(n), math.factorial(2 * n), math.factorial(n) * 2, ans * 2, 2 ** n], "Each couple is a block, and each block can flip.",
             "the count.", f"arrange the ${n}$ couple blocks, then choose the order within each.",
             [f"Blocks: ${n}! = {math.factorial(n)}$.", f"Flips: $2^{{{n}}} = {2 ** n}$.", f"Total: ${ans}$."], "multiplying by just 2 for the flips instead of $2^" + str(n) + "$.")


@reg(S, "basics")
def pe_distinct_kdigit(r):
    k = r.randint(2, 5)
    ans = 9 * math.perm(9, k - 1)
    p = f"How many ${k}$-digit numbers have all different digits?"
    return Q(p, B(ans), [B(math.perm(10, k)), B(9 * 10 ** (k - 1)), B(math.perm(9, k)), B(ans + math.perm(9, k - 1))], "The first digit can't be $0$.",
             "the count.", "first digit: $9$ choices; then each next digit has one fewer option, but $0$ is now allowed.",
             [f"$9 \\cdot {' \\cdot '.join(str(9 - i) for i in range(k - 1))} = {big(ans)}$."], "using $10 \\cdot 9 \\cdots$, which allows a leading $0$.", ans_tex=big(ans))


@reg(S, "challenge")
def pec_bracelet(r):
    n = r.randint(4, 9)
    ans = math.factorial(n - 1) // 2
    p = f"${n}$ different beads are strung on a bracelet. Two bracelets are the same if one can be rotated or flipped over to match the other. How many different bracelets are possible?"
    return Q(p, ans, [math.factorial(n - 1), math.factorial(n), math.factorial(n) // 2, ans + 1, math.factorial(n - 2)], "Start from the round-table count.",
             "the number of bracelets.", f"circular arrangements give $({n} - 1)!$; flipping pairs them up, halving the count.",
             [f"Up to rotation: $({n - 1})! = {math.factorial(n - 1)}$.", f"Flipping matches each with its mirror image: $\\frac{{{math.factorial(n - 1)}}}{{2}} = {ans}$."], "not dividing by 2 for flips.")


@reg(S, "challenge")
def pec_round_apart(r):
    n = r.randint(5, 9)
    a, b = r.sample(NAMES, 2)
    ans = math.factorial(n - 1) - 2 * math.factorial(n - 2)
    p = f"${n}$ people sit around a round table (rotations count as the same). In how many seatings are {a} and {b} NOT next to each other?"
    return Q(p, ans, [math.factorial(n - 1), 2 * math.factorial(n - 2), math.factorial(n) - 2 * math.factorial(n - 1), ans + math.factorial(n - 2), (n - 3) * math.factorial(n - 3)], "Count seatings with them together, then subtract.",
             "the count.", "fix " + a + "'s seat; " + b + " is adjacent in $2$ of the remaining " + str(n - 1) + " seats.",
             [f"All seatings: $({n - 1})! = {math.factorial(n - 1)}$.", f"Together: {b} in one of $2$ seats next to {a}, others $({n - 2})!$: ${2 * math.factorial(n - 2)}$.", f"Apart: ${ans}$."], "using row formulas for a round table.")


@reg(S, "challenge")
def pec_two_fixed(r):
    n = r.randint(4, 8)
    ans = math.factorial(n) - 2 * math.factorial(n - 1) + math.factorial(n - 2)
    p = f"${n}$ students sit in ${n}$ assigned seats in a row, but the seats are reshuffled at random. In how many arrangements is neither student 1 in seat 1 nor student 2 in seat 2?"
    return Q(p, ans, [math.factorial(n) - 2 * math.factorial(n - 1), math.factorial(n) - math.factorial(n - 1), ans + math.factorial(n - 2), math.factorial(n - 2) * (n - 2) ** 2, math.factorial(n)], "Inclusion and exclusion.",
             "the count.", "subtract arrangements with student 1 in place or student 2 in place, then add back those with both.",
             [f"All: ${n}! = {math.factorial(n)}$.", f"Student 1 fixed: $({n - 1})!$; student 2 fixed: $({n - 1})!$; both: $({n - 2})!$.", f"${math.factorial(n)} - 2 \\cdot {math.factorial(n - 1)} + {math.factorial(n - 2)} = {ans}$."], "forgetting to add back the cases where both are in place.")


@reg(S, "challenge")
def pec_rank(r):
    letters = sorted(r.sample("ABCDEFGH", r.randint(4, 5)))
    word = "".join(r.sample(letters, len(letters)))
    perms = sorted("".join(p) for p in itertools.permutations(letters))
    ans = perms.index(word) + 1
    p = f"All arrangements of the letters ${', '.join(letters)}$ are listed in alphabetical order. In what position is {word}?"
    return Q(p, ans, [ans - 1, ans + 1, len(perms) - ans + 1, ans + math.factorial(len(letters) - 1), ans * 2 if ans * 2 <= len(perms) else ans - 2], "Count the words that come before it, letter by letter.",
             "the position of " + word + ".", "for each position, count how many words start the same way but have a smaller next letter.",
             [f"Total words: ${len(letters)}! = {len(perms)}$.", f"Words before {word}: ${ans - 1}$ (counting earlier first letters, then earlier second letters, and so on).", f"Position: ${ans}$."], "forgetting to add $1$ for the word itself.")


@reg(S, "challenge")
def pec_records(r):
    n = r.randint(3, 10)
    ans = 2 ** (n - 1)
    p = f"How many arrangements of $1, 2, \\ldots, {n}$ have the property that every number is either larger than all numbers before it or smaller than all numbers before it?"
    return Q(p, ans, [2 ** n, math.factorial(n) // 2, n, 2 ** (n - 1) + 1, 2 * n - 2], "Look at the arrangement from the end.",
             "the count.", f"the last number must be $1$ or ${n}$ (the smallest or largest of all); remove it and repeat.",
             [f"Working backwards, each of the last ${n - 1}$ positions has $2$ choices (current smallest or current largest of what's left).", f"The first number is then forced: $2^{{{n - 1}}} = {ans}$."], "using $2^n$, giving the first number a choice too.")


@reg(S, "challenge")
def pec_no_adjacent_same(r):
    word = r.choice(["AABBC", "AABBCC", "AAB BC".replace(" ", ""), "ABBCC", "AABCD", "AAABB", "AABBB"])
    perms = set(itertools.permutations(word))
    good = [p_ for p_ in perms if all(p_[i] != p_[i + 1] for i in range(len(p_) - 1))]
    p = f"How many arrangements of the letters {word} have no two identical letters next to each other?"
    return Q(p, len(good), [len(perms), len(perms) - len(good), len(good) + 2, len(good) // 2 if len(good) > 2 else 3, len(good) + 6], "List or count carefully, using complementary counting for the repeated letters.",
             "the count.", "count all distinct arrangements, then remove those with an adjacent identical pair (inclusion and exclusion if needed).",
             [f"Distinct arrangements: ${len(perms)}$.", f"Removing those with any adjacent equal letters leaves ${len(good)}$."], "removing the 'pair together' cases twice.")


@reg(S, "challenge")
def pec_digit_perm_sum(r):
    digits = sorted(r.sample(range(1, 10), 4))
    ans = sum(int("".join(map(str, p_))) for p_ in itertools.permutations(digits))
    p = f"What is the sum of all four-digit numbers formed by arranging the digits ${', '.join(map(str, digits))}$ (each used once)?"
    return Q(p, B(ans), [B(sum(digits) * 1111), B(sum(digits) * 24), B(ans + 1111), B(sum(digits) * 6 * 1000)], "Each digit appears in each place the same number of times.",
             "the sum.", "each digit sits in each place in $3! = 6$ of the $24$ numbers.",
             [f"Each place sums to $6 \\cdot ({' + '.join(map(str, digits))}) = 6 \\cdot {sum(digits)} = {6 * sum(digits)}$.", f"Total: ${6 * sum(digits)} \\cdot 1111 = {big(ans)}$."], "multiplying by 24 instead of 6.", ans_tex=big(ans))


# ================================================================ cp_combinations
S = "cp_combinations"


@reg(S, "basics")
def cb_include_person(r):
    n, k = r.randint(6, 14), r.randint(3, 5)
    nm = r.choice(NAMES)
    ans = comb(n - 1, k - 1)
    p = f"A committee of ${k}$ is chosen from ${n}$ people, one of whom is {nm}. How many committees include {nm}?"
    return Q(p, ans, [comb(n, k), comb(n - 1, k), comb(n, k - 1), ans * k, comb(n, k) - ans], nm + " is already in; choose the rest.",
             "the count.", f"put {nm} on the committee and choose the other ${k - 1}$ from the remaining ${n - 1}$.",
             [f"$\\binom{{{n - 1}}}{{{k - 1}}} = {ans}$."], "counting the committees without " + nm + ".")


@reg(S, "basics")
def cb_chair(r):
    n, k = r.randint(5, 12), r.randint(3, 5)
    ans = n * comb(n - 1, k - 1)
    p = f"A club of ${n}$ members chooses a committee of ${k}$, one of whom is named chair. How many ways are there?"
    return Q(p, ans, [comb(n, k), math.perm(n, k), n * comb(n - 1, k), comb(n, k) * (k - 1), ans + n], "Pick the chair, then the other members.",
             "the count.", "choose the chair, then the rest of the committee (order among them doesn't matter).",
             [f"Chair: ${n}$ ways. Others: $\\binom{{{n - 1}}}{{{k - 1}}} = {comb(n - 1, k - 1)}$.", f"Total: ${ans}$. (Or $\\binom{{{n}}}{{{k}}} \\cdot {k}$.)"], "forgetting to choose the chair.")


@reg(S, "basics")
def cb_at_most(r):
    n = r.randint(5, 12)
    k = r.randint(2, 3)
    ans = sum(comb(n, i) for i in range(k + 1))
    p = f"A pizza can have at most ${k}$ of ${n}$ available toppings (no topping twice). How many different pizzas are possible, including a plain one?"
    return Q(p, ans, [comb(n, k), ans - 1, 2 ** n, sum(comb(n, i) for i in range(1, k + 1)) + 2, ans + n], "Add up the counts for $0$, $1$, ..., " + str(k) + " toppings.",
             "the count.", "cases by the number of toppings.",
             [" + ".join(f"\\binom{{{n}}}{{{i}}}" for i in range(k + 1)).join(["$", "$"]) + " $= " + " + ".join(str(comb(n, i)) for i in range(k + 1)) + f" = {ans}$."], "forgetting the plain pizza.")


@reg(S, "basics")
def cb_two_specific(r):
    n, k = r.randint(7, 15), r.randint(3, 6)
    ans = comb(n - 2, k - 2)
    p = f"How many ${k}$-element subsets of $\\{{1, 2, \\ldots, {n}\\}}$ contain both $1$ and $2$?"
    return Q(p, ans, [comb(n, k), comb(n - 2, k), comb(n - 1, k - 1), ans * 2, comb(n - 2, k - 1)], "Include $1$ and $2$, then choose the rest.",
             "the count.", f"with $1$ and $2$ already in, choose the other ${k - 2}$ from the remaining ${n - 2}$.",
             [f"$\\binom{{{n - 2}}}{{{k - 2}}} = {ans}$."], "choosing " + str(k) + " more elements instead of " + str(k - 2) + ".")


@reg(S, "basics")
def cb_casework_mix(r):
    a, b = r.randint(4, 8), r.randint(3, 7)
    ans = comb(a, 2) * b + comb(a, 3)
    p = f"From ${a}$ teachers and ${b}$ parents, a team of $3$ is chosen with at least $2$ teachers. How many teams are possible?"
    return Q(p, ans, [comb(a + b, 3), comb(a, 2) * b, comb(a, 3), comb(a, 2) * comb(a + b - 2, 1), ans + b], "Cases: exactly 2 teachers, or exactly 3.",
             "the count.", "split by how many teachers are on the team.",
             [f"Exactly 2 teachers: $\\binom{{{a}}}{{2}} \\cdot {b} = {comb(a, 2) * b}$.", f"3 teachers: $\\binom{{{a}}}{{3}} = {comb(a, 3)}$.", f"Total: ${ans}$."], "choosing 2 teachers then any 1 person, which double counts all-teacher teams.")


@reg(S, "basics")
def cb_split_teams(r):
    n = r.randint(2, 6)
    ans = comb(2 * n, n) // 2
    p = f"In how many ways can ${2 * n}$ people be split into two teams of ${n}$, if the teams have no names?"
    return Q(p, ans, [comb(2 * n, n), ans * 2 + 1, comb(2 * n, n - 1), math.factorial(2 * n) // (math.factorial(n) ** 2 * 2) + 1 if math.factorial(2 * n) // (math.factorial(n) ** 2 * 2) + 1 != ans else ans + 2, 2 ** (2 * n - 1)], "Picking one team picks the other.",
             "the count.", f"choosing the ${n}$ people for 'team 1' counts each split twice (team 1 vs team 2 swapped).",
             [f"$\\binom{{{2 * n}}}{{{n}}} = {comb(2 * n, n)}$.", f"Divide by $2$: ${ans}$."], "forgetting to divide by $2$.")


@reg(S, "basics")
def cb_increasing(r):
    k = r.randint(2, 5)
    ans = comb(9, k)
    p = f"How many ${k}$-digit numbers have digits that strictly increase from left to right?"
    return Q(p, ans, [comb(10, k), math.perm(9, k), ans + 1, comb(9, k - 1), 9 ** k], "Choose the digits; the order is forced.",
             "the count.", "any set of " + str(k) + " different digits can be arranged in increasing order in exactly one way; $0$ can't appear (it would have to be first).",
             [f"Choose ${k}$ digits from $1$ to $9$: $\\binom{{9}}{{{k}}} = {ans}$."], "including $0$ as an option.")


@reg(S, "basics")
def cb_same_suit(r):
    k = r.randint(2, 3)
    ans = 4 * comb(13, k)
    p = f"How many ${k}$-card hands from a standard $52$-card deck have all cards of the same suit?"
    return Q(p, ans, [comb(13, k), comb(52, k), 13 * comb(4, k), ans * 2, 4 * math.perm(13, k)], "Pick the suit, then the cards.",
             "the count.", "choose one of $4$ suits, then " + str(k) + " of its $13$ cards.",
             [f"$4 \\cdot \\binom{{13}}{{{k}}} = 4 \\cdot {comb(13, k)} = {ans}$."], "forgetting to choose the suit.")


@reg(S, "basics")
def cb_coefficient(r):
    n = r.randint(5, 12)
    k = r.randint(2, n - 2)
    ans = comb(n, k)
    p = f"What is the coefficient of $x^{{{k}}}$ in the expansion of $(1 + x)^{{{n}}}$?"
    return Q(p, ans, [comb(n, k - 1), n * k, comb(n + 1, k), 2 ** k, ans + 1], "Binomial Theorem.",
             "the coefficient.", f"$(1 + x)^{{{n}}} = \\sum \\binom{{{n}}}{{k}} x^k$: each $x^k$ term comes from choosing $x$ in $k$ of the ${n}$ factors.",
             [f"$\\binom{{{n}}}{{{k}}} = {ans}$."], "using $\\binom{n}{k - 1}$.")


@reg(S, "basics")
def cb_even_subsets(r):
    n = r.randint(3, 12)
    ans = 2 ** (n - 1)
    p = f"How many subsets of a ${n}$-element set have an even number of elements (counting the empty set)?"
    return Q(p, ans, [2 ** n, 2 ** (n - 1) - 1, 2 ** (n - 1) + 1, n // 2 + 1, comb(n, n // 2)], "Pair subsets by toggling one fixed element.",
             "the count.", "adding or removing a fixed element switches between even and odd sizes, so exactly half the subsets are even.",
             [f"$\\frac{{2^{{{n}}}}}{{2}} = {ans}$."], "forgetting the empty set.")


@reg(S, "basics")
def cb_avoid_pair(r):
    n, k = r.randint(6, 12), r.randint(3, 5)
    a, b = r.sample(NAMES, 2)
    ans = comb(n, k) - comb(n - 2, k - 2)
    p = f"A team of ${k}$ is chosen from ${n}$ players. {a} and {b} refuse to be on the same team. How many teams are possible?"
    return Q(p, ans, [comb(n, k), comb(n - 2, k), comb(n - 2, k - 2), ans - comb(n - 2, k - 1), comb(n - 1, k)], "Subtract the teams with both.",
             "the count.", "complementary counting: all teams minus teams containing both.",
             [f"All: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$.", f"With both: $\\binom{{{n - 2}}}{{{k - 2}}} = {comb(n - 2, k - 2)}$.", f"Allowed: ${ans}$."], "removing every team with either of them.")


@reg(S, "basics")
def cb_diagonal_crossings(r):
    n = r.randint(5, 12)
    ans = comb(n, 4)
    p = f"All the diagonals of a convex ${n}$-gon are drawn, and no three meet at a single point inside. How many points inside the polygon are crossing points of two diagonals?"
    return Q(p, ans, [comb(n, 2) - n, comb(n, 3), ans * 2, comb(n - 3, 2), n * (n - 3)], "Each crossing comes from 4 vertices.",
             "the number of crossings.", "any 4 vertices form a quadrilateral whose two diagonals cross exactly once.",
             [f"$\\binom{{{n}}}{{4}} = {ans}$."], "counting pairs of diagonals, many of which don't cross.")


@reg(S, "basics")
def cb_pairings(r):
    n = r.randint(2, 5)
    ans = math.prod(range(1, 2 * n, 2))
    p = f"In how many ways can ${2 * n}$ people be split into ${n}$ pairs?"
    return Q(p, ans, [math.factorial(2 * n) // 2 ** n, comb(2 * n, 2), ans * math.factorial(n), math.factorial(n), ans + 1], "Pair up the first person, then the next unpaired person, ...",
             "the count.", "the first unpaired person has $" + str(2 * n - 1) + "$ choices of partner, the next has $" + str(2 * n - 3) + "$, and so on.",
             [" \\cdot ".join(str(i) for i in range(2 * n - 1, 0, -2)).join(["$", f" = {ans}$."])], "not dividing by the order of the pairs.")


@reg(S, "basics")
def cb_min_each(r):
    k = r.randint(3, 4)
    m = r.randint(2, 3)
    n = r.randint(k * m + 1, k * m + 8)
    ans = comb(n - k * m + k - 1, k - 1)
    p = f"In how many ways can ${n}$ identical marbles be split among ${k}$ children so each gets at least ${m}$?"
    return Q(p, ans, [comb(n - 1, k - 1), comb(n + k - 1, k - 1), comb(n - k * m, k - 1) if n - k * m >= k - 1 and comb(n - k * m, k - 1) != ans else ans + 1, ans + k, comb(n - k * m + k, k)], "Hand out the minimums first.",
             "the count.", f"give each child ${m}$ first; then share the remaining marbles freely (Stars and Bars).",
             [f"Left after minimums: ${n} - {k * m} = {n - k * m}$.", f"Stars and Bars: $\\binom{{{n - k * m} + {k - 1}}}{{{k - 1}}} = {ans}$."], "using a minimum of 1 instead of " + str(m) + ".")


@reg(S, "basics")
def cb_symmetry(r):
    n = r.randint(8, 20)
    j = r.randint(2, n // 2 - 1)
    p = f"The number $\\binom{{{n}}}{{{j}}}$ equals $\\binom{{{n}}}{{k}}$ for one value of $k$ other than ${j}$. What is $k$?"
    return Q(p, n - j, [j + 1, n, n - j + 1, n - 2 * j, 2 * j], "Choosing who's in equals choosing who's out.",
             "$k$.", "$\\binom{n}{j} = \\binom{n}{n - j}$, because choosing $j$ items is the same as choosing the $n - j$ to leave out.",
             [f"$k = {n} - {j} = {n - j}$."], "guessing $j + 1$.")


@reg(S, "basics")
def cb_exactly_one_ace(r):
    k = r.randint(2, 4)
    j = r.randint(1, min(2, k - 1)) if k > 2 else 1
    ans = comb(4, j) * comb(48, k - j)
    p = f"How many ${k}$-card hands from a standard $52$-card deck contain exactly ${j}$ ace{'s' if j > 1 else ''}?"
    return Q(p, B(ans), [B(comb(52, k) - comb(48, k)), B(comb(4, j) * comb(52, k - j)), B(comb(48, k - j)), B(ans * 2)], "Choose the aces and the non-aces separately.",
             "the count.", f"pick ${j}$ of the $4$ aces, then ${k - j}$ of the $48$ non-aces.",
             [f"Aces: $\\binom{{4}}{{{j}}} = {comb(4, j)}$. Others: $\\binom{{48}}{{{k - j}}} = {big(comb(48, k - j))}$.", f"Total: ${big(ans)}$."], "choosing the other cards from all 52, which allows extra aces.", ans_tex=big(ans))


@reg(S, "challenge")
def cbc_at_least_two_each(r):
    a, b, k = r.randint(4, 7), r.randint(4, 7), r.choice([4, 5])
    ans = sum(comb(a, i) * comb(b, k - i) for i in range(2, k - 1))
    p = f"A committee of ${k}$ is chosen from ${a}$ juniors and ${b}$ seniors, with at least $2$ of each. How many committees are possible?"
    return Q(p, ans, [comb(a + b, k), comb(a, 2) * comb(b, 2) * comb(a + b - 4, k - 4) if k > 4 else ans + 10, ans + comb(a, 2), comb(a, 2) * comb(b, 2), comb(a + b, k) - ans], "Split by the number of juniors.",
             "the count.", "list the allowed (juniors, seniors) splits, count each, and add.",
             ["Cases: " + "; ".join(f"${i}$ juniors, ${k - i}$ seniors: $\\binom{{{a}}}{{{i}}}\\binom{{{b}}}{{{k - i}}} = {comb(a, i) * comb(b, k - i)}$" for i in range(2, k - 1)) + ".", f"Total: ${ans}$."],
             "choosing 2 of each first and then filling, which double counts.")


@reg(S, "challenge")
def cbc_hockey(r):
    k = r.randint(2, 4)
    n = r.randint(k + 4, 15)
    ans = comb(n + 1, k + 1)
    p = f"What is $\\binom{{{k}}}{{{k}}} + \\binom{{{k + 1}}}{{{k}}} + \\binom{{{k + 2}}}{{{k}}} + \\cdots + \\binom{{{n}}}{{{k}}}$?"
    return Q(p, ans, [comb(n, k + 1), comb(n + 1, k), ans + 1, comb(n + 2, k + 2), 2 ** n], "Hockey Stick Identity.",
             "the sum.", "Hockey Stick Identity: $\\sum_{i=k}^{n} \\binom{i}{k} = \\binom{n + 1}{k + 1}$. (Count $(k+1)$-subsets of $\\{1, \\ldots, n + 1\\}$ by their largest element.)",
             [f"$\\binom{{{n + 1}}}{{{k + 1}}} = {ans}$."], "using $\\binom{n}{k+1}$, an off by one.")


@reg(S, "challenge")
def cbc_le_n(r):
    n = r.randint(3, 15)
    ans = comb(n + 3, 3)
    p = f"How many ordered triples $(x, y, z)$ of nonnegative integers satisfy $x + y + z \\le {n}$?"
    return Q(p, ans, [comb(n + 2, 2), comb(n + 3, 2), ans + 1, (n + 1) ** 3, comb(n + 2, 3)], "Add a slack variable $w$.",
             "the count.", "introduce $w = " + str(n) + " - (x + y + z) \\ge 0$; then $x + y + z + w = " + str(n) + "$ exactly.",
             [f"Stars and Bars with $4$ variables: $\\binom{{{n} + 3}}{{3}} = {ans}$."], "counting only the solutions with sum exactly " + str(n) + ".")


@reg(S, "challenge")
def cbc_even_sum(r):
    n = r.randint(6, 16)
    o, e = (n + 1) // 2, n // 2
    ans = comb(e, 3) + comb(o, 2) * e
    p = f"How many ways are there to choose $3$ different numbers from $\\{{1, 2, \\ldots, {n}\\}}$ whose sum is even?"
    return Q(p, ans, [comb(n, 3) // 2, comb(n, 3) - ans, comb(e, 3), comb(o, 2) * e, ans + 1], "Count by how many odd numbers are chosen.",
             "the count.", "a sum is even when it contains $0$ or $2$ odd numbers.",
             [f"Odds: ${o}$, evens: ${e}$.", f"No odds: $\\binom{{{e}}}{{3}} = {comb(e, 3)}$. Two odds: $\\binom{{{o}}}{{2}} \\cdot {e} = {comb(o, 2) * e}$.", f"Total: ${ans}$."], "assuming exactly half of the choices work.")


@reg(S, "challenge")
def cbc_largest_is(r):
    k = r.randint(2, 4)
    m = r.randint(k + 2, 14)
    n = r.randint(m, 18)
    ans = comb(m - 1, k - 1)
    p = f"How many ${k}$-element subsets of $\\{{1, 2, \\ldots, {n}\\}}$ have largest element ${m}$?"
    return Q(p, ans, [comb(m, k), comb(m - 1, k), comb(n - m, k - 1) if comb(n - m, k - 1) != ans else ans + 1, comb(n - 1, k - 1), ans * 2], "The other elements are all less than " + str(m) + ".",
             "the count.", f"${m}$ is in the subset; the other ${k - 1}$ come from $\\{{1, \\ldots, {m - 1}\\}}$.",
             [f"$\\binom{{{m - 1}}}{{{k - 1}}} = {ans}$."], "letting the other elements be bigger than " + str(m) + ".")


@reg(S, "challenge")
def cbc_no_couple(r):
    n = r.randint(4, 8)
    k = r.randint(2, min(4, n))
    ans = comb(n, k) * 2 ** k
    p = f"A committee of ${k}$ is chosen from ${n}$ married couples so that no couple is on it together. How many committees are possible?"
    return Q(p, ans, [comb(2 * n, k), comb(2 * n, k) - n * comb(2 * n - 2, k - 2), comb(n, k), ans // 2, comb(n, k) * k], "Choose which couples are represented, then which spouse.",
             "the count.", f"pick ${k}$ different couples, then one person from each.",
             [f"Couples: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$. One spouse from each: $2^{{{k}}} = {2 ** k}$.", f"Total: ${ans}$."], "subtracting committees with a couple only once, missing overlaps.")


@reg(S, "challenge")
def cbc_parallel_lines(r):
    a, b = r.randint(3, 8), r.randint(3, 8)
    ans = comb(a, 2) * b + a * comb(b, 2)
    p = f"${a}$ points are marked on one line and ${b}$ points on a parallel line. How many triangles have all three vertices among these points?"
    return Q(p, ans, [comb(a + b, 3), comb(a, 2) * b, ans + comb(a, 3), a * b * (a + b - 2), comb(a + b, 3) - comb(a, 3)], "A triangle needs points on both lines.",
             "the count.", "three points on one line don't make a triangle, so take 2 from one line and 1 from the other.",
             [f"Two from the first line: $\\binom{{{a}}}{{2}} \\cdot {b} = {comb(a, 2) * b}$.", f"Two from the second: ${a} \\cdot \\binom{{{b}}}{{2}} = {a * comb(b, 2)}$.", f"Total: ${ans}$."], "counting collinear triples as triangles.")


# ================================================================ cp_casework
S = "cp_casework"


@reg(S, "basics")
def cw_digit_sum_k(r):
    N = r.choice([100, 200, 500, 999, 1000])
    k = r.randint(3, 15)
    xs = [n for n in range(1, N + 1) if sum(map(int, str(n))) == k]
    p = f"How many integers from $1$ to ${N}$ have digits that add up to ${k}$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, comb(k + 2, 2), len(xs) + 3, k], "Split by the number of digits.",
             "the count.", "casework on the number of digits (and the leading digit).",
             [f"Listing by number of digits and checking against ${N}$: ${len(xs)}$ numbers."], "including numbers above " + str(N) + " or with a leading zero.")


@reg(S, "basics")
def cw_some_repeat(r):
    k = r.randint(2, 4)
    tot = 9 * 10 ** (k - 1)
    dist = 9 * math.perm(9, k - 1)
    ans = tot - dist
    p = f"How many ${k}$-digit numbers have at least two digits that are the same?"
    return Q(p, ans, [dist, tot, ans + 9, tot - 9 * 9 ** (k - 1), ans - 1], "Count the ones with all different digits, and subtract.",
             "the count.", "complementary counting: all " + str(k) + "-digit numbers minus those with all different digits.",
             [f"All: ${tot}$.", f"All different: $9 \\cdot {' \\cdot '.join(str(9 - i) for i in range(k - 1))} = {dist}$.", f"At least one repeat: ${ans}$."], "counting only numbers with a pair repeated next to each other.")


@reg(S, "basics")
def cw_change(r):
    n = r.choice([25, 30, 40, 50, 60, 75, 100])
    ways = [(q, d, ni) for q in range(n // 25 + 1) for d in range(n // 10 + 1) for ni in range(n // 5 + 1) if 25 * q + 10 * d + 5 * ni == n]
    p = f"In how many ways can you make ${n}$ cents using nickels, dimes, and quarters?"
    return Q(p, len(ways), [len(ways) + 1, len(ways) - 1, n // 5, len(ways) + 2, len(ways) * 2], "Fix the number of quarters, then count dime choices.",
             "the number of ways.", "casework on quarters; for each, the dimes can range freely and nickels fill the rest.",
             ["; ".join(f"${q}$ quarter{'s' if q != 1 else ''}: ${sum(1 for x in ways if x[0] == q)}$ ways" for q in range(n // 25 + 1)) + ".", f"Total: ${len(ways)}$."], "forgetting the case with no quarters.")


@reg(S, "basics")
def cw_dice_product(r):
    k = r.choice([2, 3, 4, 5, 6])
    good = sum(1 for a in range(1, 7) for b in range(1, 7) if (a * b) % k == 0)
    p = f"Two dice are rolled (one red, one blue). In how many of the $36$ outcomes is the product of the numbers a multiple of ${k}$?"
    return Q(p, good, [36 - good, good + 1, 36 // k, good - 1, 2 * (6 // k) * 6 if 2 * (6 // k) * 6 != good else good + 2], "Use complementary counting or list carefully.",
             "the count.", "casework on which die supplies the factor (or count the outcomes that fail).",
             [f"Counting the pairs $(a, b)$ with ${k} \\mid ab$: ${good}$."], "adding the cases for each die without removing double counts.")


@reg(S, "basics")
def cw_goldbach(r):
    n = r.choice(range(20, 101, 2))
    pr = lambda x: x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))
    ways = [(p_, n - p_) for p_ in range(2, n // 2 + 1) if pr(p_) and pr(n - p_)]
    p = f"In how many ways can ${n}$ be written as the sum of two primes? (Order doesn't matter: $3 + 5$ and $5 + 3$ count once.)"
    return Q(p, len(ways), [len(ways) * 2, len(ways) + 1, len(ways) - 1 if len(ways) > 1 else 3, len([x for x in range(2, n) if pr(x)]) // 2, len(ways) + 2], "Check each prime up to " + str(n // 2) + ".",
             "the count.", "for each prime $p \\le \\frac{n}{2}$, check whether $n - p$ is prime.",
             ["Pairs: " + ", ".join(f"${a} + {b}$" for a, b in ways) + ".", f"Count: ${len(ways)}$."], "counting $a + b$ and $b + a$ separately.")


@reg(S, "basics")
def cw_isosceles(r):
    P = r.randint(10, 40)
    tris = {tuple(sorted((a, a, P - 2 * a))) for a in range(1, P) if P - 2 * a > 0 and 2 * a > P - 2 * a}
    p = f"How many non-congruent isosceles triangles (including equilateral) have integer side lengths and perimeter ${P}$?"
    return Q(p, len(tris), [len(tris) + 1, len(tris) - 1 if len(tris) > 1 else 3, P // 4, P // 2 - 1, len(tris) * 2], "Let the equal sides be $a$; the base is $" + str(P) + " - 2a$.",
             "the count.", "the base must be positive and less than $2a$ (triangle inequality).",
             [f"Base $= {P} - 2a > 0$ gives $a < {ftex(F(P, 2))}$; $2a > {P} - 2a$ gives $a > {ftex(F(P, 4))}$.", f"Valid $a$: " + ", ".join(str(t[0] if t[0] == t[1] else t[1]) for t in sorted(tris)) + f". That's ${len(tris)}$."], "forgetting the triangle inequality.")


@reg(S, "basics")
def cw_vowel_plate(r):
    k = r.randint(2, 4)
    ans = 26 ** k - 21 ** k
    p = f"How many ${k}$-letter strings (any letters, repeats allowed) contain at least one vowel (A, E, I, O, U)?"
    return Q(p, B(ans), [B(5 * 26 ** (k - 1)), B(26 ** k), B(21 ** k), B(5 ** k)], "Count strings with no vowels.",
             "the count.", "complementary counting: all strings minus strings with only consonants.",
             [f"All: $26^{{{k}}} = {big(26 ** k)}$.", f"No vowels: $21^{{{k}}} = {big(21 ** k)}$.", f"At least one vowel: ${big(ans)}$."], "multiplying 5 vowel choices by $26^{" + str(k - 1) + "}$, which double counts.", ans_tex=big(ans))


@reg(S, "basics")
def cw_some_six(r):
    k = r.randint(2, 5)
    ans = 6 ** k - 5 ** k
    p = f"${k}$ different-colored dice are rolled. In how many of the $6^{{{k}}}$ outcomes does at least one die show a $6$?"
    return Q(p, ans, [k * 6 ** (k - 1), 5 ** k, 6 ** k, ans + 1, k * 5 ** (k - 1)], "Count the outcomes with no 6.",
             "the count.", "complementary counting.",
             [f"No sixes: $5^{{{k}}} = {5 ** k}$.", f"At least one: $6^{{{k}}} - 5^{{{k}}} = {ans}$."], "counting $" + str(k) + " \\cdot 6^{" + str(k - 1) + "}$, which double counts outcomes with several sixes.")


@reg(S, "basics")
def cw_even_digit(r):
    k = r.randint(2, 5)
    ans = 9 * 10 ** (k - 1) - 5 ** k
    p = f"How many ${k}$-digit numbers have at least one even digit?"
    return Q(p, B(ans), [B(9 * 10 ** (k - 1)), B(5 ** k), B(ans + 5 ** (k - 1)), B(9 * 10 ** (k - 1) - 4 * 5 ** (k - 1))], "Count the numbers with all odd digits.",
             "the count.", "all odd digits: $5$ choices for each place (and $0$ isn't odd, so the leading digit is fine).",
             [f"All " + str(k) + f"-digit: $9 \\cdot 10^{{{k - 1}}} = {big(9 * 10 ** (k - 1))}$.", f"All odd: $5^{{{k}}} = {5 ** k}$.", f"Difference: ${big(ans)}$."], "treating $0$ as odd.", ans_tex=big(ans))


@reg(S, "basics")
def cw_lattice_disk(r):
    R = r.randint(2, 6)
    ans = sum(1 for x in range(-R, R + 1) for y in range(-R, R + 1) if x * x + y * y < R * R)
    p = f"How many points with integer coordinates lie strictly inside the circle $x^2 + y^2 = {R * R}$?"
    return Q(p, ans, [ans + 4, (2 * R - 1) ** 2, round(math.pi * R * R), ans - 4, (2 * R + 1) ** 2], "Go row by row: for each $y$, count the allowed $x$.",
             "the count.", "casework on $y$; for each $y$, $x^2 < " + str(R * R) + " - y^2$.",
             ["; ".join(f"$y = \\pm{y}$: ${sum(1 for x in range(-R, R + 1) if x * x + y * y < R * R)}$" if y else f"$y = 0$: ${sum(1 for x in range(-R, R + 1) if x * x < R * R)}$" for y in range(0, R) if sum(1 for x in range(-R, R + 1) if x * x + y * y < R * R)) + ".", f"Total: ${ans}$."],
             "including points on the circle.")


@reg(S, "basics")
def cw_product_le(r):
    N = r.randint(8, 30)
    ans = sum(N // a for a in range(1, N + 1))
    p = f"How many ordered pairs of positive integers $(a, b)$ satisfy $ab \\le {N}$?"
    return Q(p, ans, [ans + 1, ans - 1, N * (N + 1) // 2, ans // 2, N + ans // 3], "For each $a$, $b$ can be any integer up to $\\lfloor " + str(N) + "/a \\rfloor$.",
             "the count.", "casework on $a$.",
             [" + ".join(str(N // a) for a in range(1, N + 1)).join(["$", f" = {ans}$."])], "counting only pairs with $a \\le b$.")


@reg(S, "basics")
def cw_grid_triangles(r):
    n = r.choice([3, 4])
    pts = [(x, y) for x in range(n) for y in range(n)]
    tri = sum(1 for a, b, c in itertools.combinations(pts, 3) if (b[0] - a[0]) * (c[1] - a[1]) != (b[1] - a[1]) * (c[0] - a[0]))
    col = comb(n * n, 3) - tri
    p = f"How many triangles (with positive area) have all three vertices among the ${n * n}$ points of an ${n} \\times {n}$ square grid of points?"
    return Q(p, tri, [comb(n * n, 3), tri + n, col, tri - 2 * n, comb(n * n, 3) - 2 * n], "Count all triples, then remove the ones on a line.",
             "the count.", "complementary counting: subtract collinear triples (rows, columns, diagonals).",
             [f"All triples: $\\binom{{{n * n}}}{{3}} = {comb(n * n, 3)}$.", f"Collinear triples: ${col}$.", f"Triangles: ${tri}$."], "forgetting the diagonal lines.")


@reg(S, "basics")
def cw_three_dice_sum(r):
    k = r.randint(4, 17)
    ans = sum(1 for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if a + b + c == k)
    p = f"Three dice of different colors are rolled. In how many of the $216$ outcomes is the sum ${k}$?"
    return Q(p, ans, [ans + 3, ans - 3 if ans > 3 else ans + 6, comb(k - 1, 2), ans * 2, 216 - ans], "Fix the first die and count pairs for the others.",
             "the count.", "casework on the first die, then count two-dice sums.",
             ["; ".join(f"first $= {a}$: ${sum(1 for b in range(1, 7) for c in range(1, 7) if a + b + c == k)}$" for a in range(1, 7)) + ".", f"Total: ${ans}$."], "using Stars and Bars without the upper limit of 6.")


@reg(S, "basics")
def cw_square_units(r):
    N = r.randint(30, 200)
    d = r.choice([1, 4, 6, 9, 5])
    ans = sum(1 for x in range(1, N + 1) if (x * x) % 10 == d)
    units = [u for u in range(10) if (u * u) % 10 == d]
    p = f"For how many integers $x$ from $1$ to ${N}$ does $x^2$ end in the digit ${d}$?"
    return Q(p, ans, [ans + 1, ans - 1, N // 10, N // 5 if N // 5 != ans else ans + 2, len(units) * (N // 10) + 1 if len(units) * (N // 10) + 1 != ans else ans + 3], "Only the units digit of $x$ matters.",
             "the count.", f"$x^2$ ends in ${d}$ exactly when $x$ ends in " + " or ".join(map(str, units)) + ".",
             [f"Count numbers up to ${N}$ ending in " + " or ".join(map(str, units)) + f": ${ans}$."], "using only one of the possible units digits.")


@reg(S, "basics")
def cw_linear_count(r):
    N = r.randint(8, 30)
    ans = sum(1 for x in range(1, N) for y in range(1, N) if x + 2 * y <= N)
    p = f"How many ordered pairs of positive integers $(x, y)$ satisfy $x + 2y \\le {N}$?"
    return Q(p, ans, [ans + 1, ans - 1, N * N // 4, sum(1 for x in range(1, N) for y in range(1, N) if x + 2 * y < N), ans * 2], "For each $y$, count the allowed $x$.",
             "the count.", "casework on $y$: $x$ can be anything from $1$ to $" + str(N) + " - 2y$.",
             [" + ".join(str(N - 2 * y) for y in range(1, N) if N - 2 * y >= 1).join(["$", f" = {ans}$."])], "counting $x = 0$.")


@reg(S, "basics")
def cw_rect_perimeter(r):
    P = r.choice(range(8, 61, 2))
    ans = (P // 2 - 1 + 1) // 2 if True else 0
    rects = [(a, P // 2 - a) for a in range(1, P // 2) if a <= P // 2 - a]
    p = f"How many non-congruent rectangles have integer side lengths and perimeter ${P}$?"
    return Q(p, len(rects), [len(rects) + 1, P // 2 - 1, len(rects) - 1, P // 4 + 2 if P // 4 + 2 != len(rects) else len(rects) + 2, len(rects) * 2], "Length plus width is " + str(P // 2) + ".",
             "the count.", "the sides satisfy $l + w = " + str(P // 2) + "$ with $l \\ge w \\ge 1$ (to avoid counting a rectangle twice).",
             [f"$w$ from $1$ to $\\left\\lfloor \\frac{{{P // 2}}}{{2}} \\right\\rfloor = {P // 4}$.", f"That's ${len(rects)}$ rectangles."], "counting $l \\times w$ and $w \\times l$ separately.")


@reg(S, "challenge")
def cwc_digit_sum_4(r):
    k = r.randint(3, 4)
    s = r.randint(5, 9 * k - 5)
    ans = sum(1 for n in range(10 ** (k - 1), 10 ** k) if sum(map(int, str(n))) == s)
    p = f"How many ${k}$-digit numbers have digits that add up to ${s}$?"
    return Q(p, ans, [comb(s + k - 1, k - 1), comb(s + k - 2, k - 1), ans + 1, ans - 1, ans + k], "Stars and Bars with the first digit at least $1$ and every digit at most $9$.",
             "the count.", "substitute $d_1' = d_1 - 1$; then count nonnegative solutions and remove those with a digit over $9$.",
             [f"$d_1' + d_2 + \\cdots + d_{{{k}}} = {s - 1}$ has $\\binom{{{s - 1 + k - 1}}}{{{k - 1}}} = {comb(s + k - 2, k - 1)}$ nonnegative solutions.", f"Removing the ones where a digit exceeds $9$ (inclusion and exclusion) leaves ${ans}$."],
             "forgetting the limit of 9 on each digit, or allowing a leading 0.")


@reg(S, "challenge")
def cwc_rooks(r):
    n = r.randint(3, 8)
    ans = comb(n * n, 2) - 2 * n * comb(n, 2)
    p = f"In how many ways can two identical rooks be placed on an ${n} \\times {n}$ board so they don't attack each other (not in the same row or column)?"
    return Q(p, ans, [comb(n * n, 2), n * n * (n - 1) ** 2, ans * 2, comb(n * n, 2) - n * comb(n, 2), comb(n, 2) ** 2], "Subtract the pairs in the same row or column.",
             "the count.", "all pairs of squares minus pairs sharing a row or column.",
             [f"All pairs: $\\binom{{{n * n}}}{{2}} = {comb(n * n, 2)}$.", f"Same row: ${n} \\cdot \\binom{{{n}}}{{2}} = {n * comb(n, 2)}$; same column: also ${n * comb(n, 2)}$.", f"Safe: ${ans}$. (Check: $\\frac{{{n * n} \\cdot {(n - 1) ** 2}}}{{2}} = {n * n * (n - 1) ** 2 // 2}$.)"],
             "counting ordered placements for identical rooks.")


@reg(S, "challenge")
def cwc_ap_digits(r):
    k = r.choice([3, 4])
    xs = [n for n in range(10 ** (k - 1), 10 ** k) if len({int(str(n)[i + 1]) - int(str(n)[i]) for i in range(k - 1)}) == 1]
    p = f"How many ${k}$-digit numbers have digits that form an arithmetic sequence (left to right)? (Constant digits like ${'5' * k}$ count.)"
    return Q(p, len(xs), [len(xs) + 9, len(xs) - 9, len(xs) + 1, 9 * k, len(xs) // 2 + 3], "Casework on the common difference.",
             "the count.", "for each common difference $d$, count starting digits that keep every digit between 0 and 9 (and the first not 0).",
             ["; ".join(f"$d = {d}$: ${sum(1 for n in xs if int(str(n)[1]) - int(str(n)[0]) == d)}$" for d in range(-9, 10) if any(int(str(n)[1]) - int(str(n)[0]) == d for n in xs)) + ".", f"Total: ${len(xs)}$."],
             "forgetting negative differences.")


@reg(S, "challenge")
def cwc_no_diff_k(r):
    n = r.randint(5, 10)
    k = r.choice([1, 2])
    cnt = sum(1 for m in range(2 ** n) if not any((m >> i) & 1 and (m >> (i + k)) & 1 for i in range(n - k)))
    p = f"How many subsets of $\\{{1, 2, \\ldots, {n}\\}}$ (including the empty set) contain no two numbers that differ by exactly ${k}$?"
    return Q(p, cnt, [cnt + 1, cnt - 1, 2 ** n - cnt, 2 ** (n - 1), cnt * 2], "Build the subsets in chains of numbers that differ by " + str(k) + ".",
             "the count.", ("consecutive numbers can't both be chosen; count by whether the last number is in, giving Fibonacci-like growth." if k == 1 else "split the numbers into odd and even chains; within each chain no two neighbors can both be chosen, and multiply the counts."),
             [f"Counting carefully gives ${cnt}$ subsets."], "forgetting the empty set.")


@reg(S, "challenge")
def cwc_no_adjacent_digits(r):
    N = r.choice([100, 500, 1000, 2000])
    xs = [n for n in range(1, N + 1) if all(str(n)[i] != str(n)[i + 1] for i in range(len(str(n)) - 1))]
    p = f"How many integers from $1$ to ${N}$ have no two neighboring digits equal?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, N - len(xs), 9 + 81 + 729 if 819 != len(xs) else len(xs) + 9, len(xs) + 10], "Count by number of digits: each next digit just has to differ from the one before.",
             "the count.", "a $d$-digit number with no equal neighbors: $9$ choices for the first digit and $9$ for each next one.",
             [f"Counting by length (and handling the top of the range): ${len(xs)}$."], "requiring all digits to be different, not just neighbors.")


@reg(S, "challenge")
def cwc_square_coloring(r):
    k = r.randint(3, 6)
    ans = (k - 1) ** 4 + (k - 1)
    p = f"Each side of a square is painted one of ${k}$ colors so that sides sharing a corner have different colors. How many colorings are possible? (Rotations count as different.)"
    return Q(p, ans, [k * (k - 1) ** 3, k * (k - 1) ** 2 * (k - 2), (k - 1) ** 4, ans + k, k ** 4], "Casework on whether opposite sides match.",
             "the count.", "color sides 1, 2, 3, 4 in order around the square; side 4 must differ from both side 3 and side 1, so split on whether sides 1 and 3 are the same.",
             [f"Sides 1 and 3 same: ${k}$ choices, then sides 2 and 4 each have ${k - 1}$: ${k * (k - 1) ** 2}$.", f"Sides 1 and 3 different: ${k} \\cdot {k - 1}$ ways; sides 2 and 4 must each avoid both colors, ${k - 2}$ choices each: ${k * (k - 1) * (k - 2) ** 2}$.",
              f"Total: ${k * (k - 1) ** 2 + k * (k - 1) * (k - 2) ** 2} = {ans}$."],
             "treating it as a line of 4, forgetting side 4 also touches side 1.") if k * (k - 1) ** 2 + k * (k - 1) * (k - 2) ** 2 == ans else None


@reg(S, "challenge")
def cwc_right_leg(r):
    n = r.choice([12, 15, 16, 20, 21, 24, 30, 36, 40, 48])
    sols = [(n, b) for b in range(1, n * n) if math.isqrt(n * n + b * b) ** 2 == n * n + b * b]
    p = f"How many right triangles with integer side lengths have a leg of length ${n}$?"
    return Q(p, len(sols), [len(sols) + 1, len(sols) - 1, len(sols) * 2, len([d for d in range(1, n + 1) if n % d == 0]), len(sols) + 2], "Write $c^2 - b^2 = " + str(n * n) + "$ and factor.",
             "the count.", f"$(c - b)(c + b) = {n * n}$ with both factors the same parity and $c - b < c + b$.",
             ["Triangles: " + ", ".join(f"$({n}, {b}, {math.isqrt(n * n + b * b)})$" for _, b in sols) + ".", f"Count: ${len(sols)}$."], "missing factor pairs where both factors are even.")
