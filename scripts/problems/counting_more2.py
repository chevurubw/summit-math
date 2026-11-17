"""Extra Counting problem types (part 2): inclusion and exclusion, probability, expected value, geometric probability."""
import itertools
import math
from fractions import Fraction as F

from common import NAMES, C, Q, comb, num

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ft(v):
    return num(F(v)).tex


def big(v):
    return f"{v:,}".replace(",", "{,}")


def B(v):
    return C(big(v), v)


def P(tex, val):
    return C(tex, val)


def pfrac(k):
    """k * pi for a Fraction k, as LaTeX."""
    k = F(k)
    if k.denominator == 1:
        return ("" if k == 1 else str(k.numerator)) + "\\pi"
    return f"\\frac{{{'' if k.numerator == 1 else k.numerator}\\pi}}{{{k.denominator}}}"


def PI(k):
    """k * pi as a choice."""
    return C(pfrac(k), float(k) * math.pi)


def PIR3(k):
    """k * pi * sqrt(3) as a choice."""
    k = F(k)
    t = f"\\frac{{{'' if k.numerator == 1 else k.numerator}\\pi\\sqrt{{3}}}}{{{k.denominator}}}" if k.denominator > 1 else f"{'' if k == 1 else k.numerator}\\pi\\sqrt{{3}}"
    return C(t, float(k) * math.pi * math.sqrt(3))


def D(n):
    d = [1, 0]
    for i in range(2, n + 1):
        d.append((i - 1) * (d[-1] + d[-2]))
    return d[n]


# ================================================================ cp_inclusion
S = "cp_inclusion"


@reg(S, "basics")
def ie_div_a_or_b(r):
    a, b = r.sample([2, 3, 5, 7, 11], 2)
    N = r.randint(50, 300)
    ans = N // a + N // b - N // (a * b)
    p = f"How many integers from $1$ to ${N}$ are divisible by ${a}$ or ${b}$?"
    return Q(p, ans, [N // a + N // b, N - ans, ans + N // (a * b) * 2, N // (a * b), ans - 1], "Add the two counts, then subtract the overlap.",
             "the count.", f"inclusion and exclusion: numbers divisible by both are multiples of ${a * b}$ and were counted twice.",
             [f"Multiples of ${a}$: ${N // a}$. Multiples of ${b}$: ${N // b}$.", f"Multiples of ${a * b}$: ${N // (a * b)}$.", f"${N // a} + {N // b} - {N // (a * b)} = {ans}$."], "forgetting to subtract the multiples of " + str(a * b) + ".")


@reg(S, "basics")
def ie_none_of_235(r):
    N = r.choice([30, 60, 90, 100, 120, 150, 200])
    ans = sum(1 for x in range(1, N + 1) if x % 2 and x % 3 and x % 5)
    s1 = N // 2 + N // 3 + N // 5
    s2 = N // 6 + N // 10 + N // 15
    s3 = N // 30
    p = f"How many integers from $1$ to ${N}$ are divisible by none of $2$, $3$, and $5$?"
    return Q(p, ans, [N - s1, N - s1 + s2, N - ans, ans + s3, ans - 1], "Count those divisible by at least one, then subtract from " + str(N) + ".",
             "the count.", "inclusion and exclusion for three sets, then take the complement.",
             [f"Singles: ${N // 2} + {N // 3} + {N // 5} = {s1}$.", f"Pairs (multiples of $6, 10, 15$): ${N // 6} + {N // 10} + {N // 15} = {s2}$.", f"All three (multiples of $30$): ${s3}$.",
              f"Divisible by at least one: ${s1} - {s2} + {s3} = {s1 - s2 + s3}$.", f"Divisible by none of them: ${N} - {s1 - s2 + s3} = {ans}$."], "stopping after subtracting the pairs.")


@reg(S, "basics")
def ie_min_both(r):
    n = r.randint(20, 60)
    a = r.randint(n // 2 + 1, n - 2)
    b = r.randint(n - a + 1, n - 1)
    ans = a + b - n
    p = f"In a class of ${n}$ students, ${a}$ play soccer and ${b}$ play basketball. What is the smallest possible number of students who play both?"
    return Q(p, ans, [0, min(a, b), n - max(a, b), ans + 1, abs(a - b) if abs(a - b) != ans else ans + 2], "Too many students for the sets not to overlap.",
             "the minimum overlap.", "$|A \\cup B| = |A| + |B| - |A \\cap B| \\le " + str(n) + "$.",
             [f"${a} + {b} - x \\le {n}$ gives $x \\ge {a + b - n}$.", f"This is reached when everyone plays at least one: ${ans}$."], "answering 0, which would need " + str(a + b) + " students.")


@reg(S, "basics")
def ie_max_neither(r):
    n = r.randint(25, 60)
    a, b = r.randint(5, n // 2), r.randint(5, n // 2)
    ans = n - max(a, b)
    p = f"Of ${n}$ people at a party, ${a}$ drink coffee and ${b}$ drink tea. What is the largest possible number who drink neither?"
    return Q(p, ans, [n - a - b, n - min(a, b), ans - 1, max(a, b), n - abs(a - b)], "Make the two groups overlap as much as possible.",
             "the maximum for neither.", "the union is smallest when the smaller group lies inside the larger one.",
             [f"Smallest union: $\\max({a}, {b}) = {max(a, b)}$.", f"Neither: ${n} - {max(a, b)} = {ans}$."], "assuming the groups don't overlap.")


@reg(S, "basics")
def ie_only_a(r):
    a = r.randint(10, 40)
    both = r.randint(2, a - 3)
    b = r.randint(both + 2, 40)
    n = a + b - both + r.randint(0, 10)
    ask = r.choice(["only", "exactly one"])
    ans = a - both if ask == "only" else a + b - 2 * both
    p = f"In a survey of ${n}$ people, ${a}$ own a cat, ${b}$ own a dog, and ${both}$ own both. How many own {'a cat but not a dog' if ask == 'only' else 'exactly one of the two pets'}?"
    return Q(p, ans, [a, a + b - both, a - both if ask != "only" else a + b - 2 * both, n - (a + b - both), ans + both], "Draw a Venn diagram.",
             "the count.", "fill the overlap first, then the rest of each circle.",
             [f"Cat only: ${a} - {both} = {a - both}$.", f"Dog only: ${b} - {both} = {b - both}$."] + ([f"Exactly one: ${a - both} + {b - both} = {ans}$."] if ask != "only" else []), "forgetting to remove the overlap.")


@reg(S, "basics")
def ie_three_union(r):
    t = r.randint(1, 4)
    ab, bc, ca = [t + r.randint(1, 5) for _ in range(3)]
    a, b, c = ab + ca - t + r.randint(2, 10), ab + bc - t + r.randint(2, 10), bc + ca - t + r.randint(2, 10)
    ans = a + b + c - ab - bc - ca + t
    p = f"At a school, ${a}$ students take art, ${b}$ take band, and ${c}$ take chorus. ${ab}$ take art and band, ${bc}$ take band and chorus, ${ca}$ take chorus and art, and ${t}$ take all three. How many take at least one of these classes?"
    return Q(p, ans, [a + b + c, a + b + c - ab - bc - ca, ans + t, ans - t, a + b + c - ab - bc - ca - t], "Three-set inclusion and exclusion.",
             "the size of the union.", "add the singles, subtract the pairs, add back the triple.",
             [f"Singles: ${a + b + c}$. Pairs: ${ab + bc + ca}$.", f"${a + b + c} - {ab + bc + ca} + {t} = {ans}$."], "forgetting to add back the students in all three.")


@reg(S, "basics")
def ie_div_a_not_b(r):
    a = r.choice([2, 3, 4, 5, 6])
    m = r.choice([2, 3, 5])
    b = a * m
    N = r.randint(60, 300)
    ans = N // a - N // b
    p = f"How many integers from $1$ to ${N}$ are divisible by ${a}$ but not by ${b}$?"
    return Q(p, ans, [N // a, N // a - N // b + 1, N // b, N // a + N // b, N - ans], "Every multiple of " + str(b) + " is also a multiple of " + str(a) + ".",
             "the count.", f"take the multiples of ${a}$ and remove the multiples of ${b}$, which are among them.",
             [f"Multiples of ${a}$: ${N // a}$. Of ${b}$: ${N // b}$.", f"${N // a} - {N // b} = {ans}$."], "also subtracting multiples of " + str(a * b) + ".")


@reg(S, "basics")
def ie_squares_cubes(r):
    N = r.choice([100, 200, 500, 1000, 2000, 5000])
    sq, cu, six = math.isqrt(N), round(N ** (1 / 3)), round(N ** (1 / 6))
    while cu ** 3 > N:
        cu -= 1
    while (cu + 1) ** 3 <= N:
        cu += 1
    while six ** 6 > N:
        six -= 1
    while (six + 1) ** 6 <= N:
        six += 1
    ans = sq + cu - six
    p = f"How many integers from $1$ to ${N}$ are perfect squares or perfect cubes?"
    return Q(p, ans, [sq + cu, sq, ans - 1, sq + cu + six, ans + 1], "Some numbers are both: the sixth powers.",
             "the count.", "a number that is both a square and a cube is a sixth power.",
             [f"Squares: ${sq}$ (up to ${sq}^2 = {sq * sq}$). Cubes: ${cu}$ (up to ${cu}^3 = {cu ** 3}$).", f"Sixth powers: ${six}$.", f"${sq} + {cu} - {six} = {ans}$."], "forgetting that the sixth powers were counted twice.")


@reg(S, "basics")
def ie_binary_start_end(r):
    n = r.randint(5, 10)
    a = 2 ** (n - 1)
    b = 2 ** (n - 2)
    ab = 2 ** (n - 3)
    ans = a + b - ab
    p = f"How many binary strings of length ${n}$ start with $1$ or end with $00$?"
    return Q(p, ans, [a + b, a, ans + ab, 2 ** n - ans, b + ab], "Count each condition, then the strings with both.",
             "the count.", "inclusion and exclusion; each fixed bit halves the count.",
             [f"Start with $1$: $2^{{{n - 1}}} = {a}$.", f"End with $00$: $2^{{{n - 2}}} = {b}$.", f"Both: $2^{{{n - 3}}} = {ab}$.", f"${a} + {b} - {ab} = {ans}$."], "adding the counts without removing the overlap.")


@reg(S, "basics")
def ie_heart_or_rank(r):
    k = r.randint(1, 4)
    ranks = ["K", "Q", "J", "10"][:k]
    ans = 13 + 4 * k - k
    p = f"How many cards in a standard $52$-card deck are hearts or have rank " + (", ".join(ranks[:-1]) + (", or " if k > 2 else " or ") + ranks[-1] if k > 1 else ranks[0]) + "?"
    return Q(p, ans, [13 + 4 * k, 13 + k, 4 * k, ans + 1, 52 - ans], "Some hearts have those ranks.",
             "the count.", "hearts plus those ranks, minus the cards that are both.",
             [f"Hearts: $13$. Cards of those ranks: $4 \\cdot {k} = {4 * k}$.", f"Both (hearts of those ranks): ${k}$.", f"$13 + {4 * k} - {k} = {ans}$."], "counting the overlap twice.")


@reg(S, "basics")
def ie_letter_and_digit(r):
    k = r.randint(2, 4)
    ans = 36 ** k - 26 ** k - 10 ** k
    p = f"A password has exactly ${k}$ characters, each a capital letter or a digit. It must contain at least one letter and at least one digit. How many passwords are possible?"
    return Q(p, B(ans), [B(36 ** k - 26 ** k), B(36 ** k), B(26 * 10 * 36 ** (k - 2) * k), B(ans + 10 ** k)], "Remove all-letter and all-digit passwords.",
             "the count.", "complement: the bad passwords are all letters or all digits (these can't overlap).",
             [f"All: $36^{{{k}}} = {big(36 ** k)}$.", f"All letters: $26^{{{k}}} = {big(26 ** k)}$. All digits: $10^{{{k}}} = {big(10 ** k)}$.", f"Good: ${big(ans)}$."], "removing only one of the two bad cases.", ans_tex=big(ans))


@reg(S, "basics")
def ie_lcm(r):
    a, b = r.choice([(4, 6), (6, 8), (6, 9), (4, 10), (10, 15), (6, 10), (8, 12), (9, 12)])
    N = r.randint(60, 300)
    L = a * b // math.gcd(a, b)
    ans = N // a + N // b - N // L
    p = f"How many integers from $1$ to ${N}$ are divisible by ${a}$ or ${b}$?"
    return Q(p, ans, [N // a + N // b - N // (a * b), N // a + N // b, ans + 1, N // L, ans - 1], f"The overlap is multiples of $\\text{{lcm}}({a}, {b})$, not ${a * b}$.",
             "the count.", f"numbers divisible by both are the multiples of $\\text{{lcm}}({a}, {b}) = {L}$.",
             [f"Multiples of ${a}$: ${N // a}$. Of ${b}$: ${N // b}$. Of ${L}$: ${N // L}$.", f"${N // a} + {N // b} - {N // L} = {ans}$."], f"using ${a * b}$ for the overlap.")


@reg(S, "basics")
def ie_dice_1_and_6(r):
    k = r.randint(2, 5)
    ans = 6 ** k - 2 * 5 ** k + 4 ** k
    p = f"${k}$ dice of different colors are rolled. In how many of the $6^{{{k}}}$ outcomes do both a $1$ and a $6$ appear?"
    return Q(p, ans, [6 ** k - 2 * 5 ** k, 6 ** k - 5 ** k, ans + 4 ** k // 2, k * (k - 1) * 6 ** (k - 2), 4 ** k], "Remove outcomes missing a 1 or missing a 6.",
             "the count.", "complement with inclusion and exclusion.",
             [f"No $1$: $5^{{{k}}}$. No $6$: $5^{{{k}}}$. Neither: $4^{{{k}}}$.", f"$6^{{{k}}} - 2 \\cdot 5^{{{k}}} + 4^{{{k}}} = {6 ** k} - {2 * 5 ** k} + {4 ** k} = {ans}$."], "forgetting to add back outcomes with neither a 1 nor a 6.")


@reg(S, "basics")
def ie_coprime(r):
    M = r.choice([12, 15, 18, 20, 21, 28, 30, 36, 42, 45])
    N = r.choice([M, 2 * M, 100])
    ps = [p_ for p_ in (2, 3, 5, 7) if M % p_ == 0]
    ans = sum(1 for x in range(1, N + 1) if math.gcd(x, M) == 1)
    p = f"How many integers from $1$ to ${N}$ share no common factor (other than $1$) with ${M}$?"
    return Q(p, ans, [N - ans, ans + 1, N - sum(N // q for q in ps), ans - 1, N // len(ps)], "Which primes divide " + str(M) + "?",
             "the count.", f"${M}$ has prime factors " + ", ".join(f"${q}$" for q in ps) + "; remove numbers divisible by any of them.",
             [f"Divisible by at least one of " + ", ".join(map(str, ps)) + f" (by inclusion and exclusion): ${N - ans}$.", f"The rest: ${N} - {N - ans} = {ans}$."], "subtracting the singles without adding back the overlaps.")


@reg(S, "basics")
def ie_exactly_two(r):
    t = r.randint(1, 4)
    ab, bc, ca = [t + r.randint(1, 6) for _ in range(3)]
    ans = ab + bc + ca - 3 * t
    p = f"In a club, ${ab}$ members play chess and go, ${bc}$ play go and poker, ${ca}$ play poker and chess, and ${t}$ play all three. How many members play exactly two of the three games?"
    return Q(p, ans, [ab + bc + ca, ab + bc + ca - t, ans + t, ab + bc + ca - 2 * t, ans - t if ans - t > 0 else ans + 2 * t], "Each pairwise count includes the people who play all three.",
             "the count.", "the triple-players appear in all three pairwise counts; remove them from each.",
             [f"Exactly chess and go: ${ab} - {t} = {ab - t}$; go and poker: ${bc - t}$; poker and chess: ${ca - t}$.", f"Total: ${ans}$."], "subtracting the triple-players once instead of three times.")


@reg(S, "basics")
def ie_none_survey(r):
    a, b = r.randint(10, 30), r.randint(10, 30)
    both = r.randint(2, min(a, b) - 2)
    n = a + b - both + r.randint(3, 15)
    ans = n - (a + b - both)
    p = f"Of ${n}$ students, ${a}$ are in the math club, ${b}$ are in the science club, and ${both}$ are in both. How many are in neither club?"
    return Q(p, ans, [n - a - b if n - a - b > 0 else ans + both * 2, ans + both, n - (a + b), a + b - both, ans - 1], "Find the union first.",
             "the count of neither.", "neither = total minus union.",
             [f"Union: ${a} + {b} - {both} = {a + b - both}$.", f"Neither: ${n} - {a + b - both} = {ans}$."], "forgetting the students in both clubs were counted twice.")


@reg(S, "challenge")
def iec_all_three_faces(r):
    k = r.randint(3, 5)
    ans = 6 ** k - 3 * 5 ** k + 3 * 4 ** k - 3 ** k
    p = f"${k}$ dice of different colors are rolled. In how many of the $6^{{{k}}}$ outcomes do the numbers $1$, $2$, and $3$ all appear?"
    return Q(p, ans, [6 ** k - 3 * 5 ** k, 6 ** k - 3 * 5 ** k + 3 * 4 ** k, ans + 3 ** k, math.perm(k, 3) * 6 ** (k - 3), ans - 6], "Subtract outcomes missing at least one of them.",
             "the count.", "let $A_i$ be the outcomes with no $i$; use inclusion and exclusion on $A_1 \\cup A_2 \\cup A_3$.",
             [f"One missing: $3 \\cdot 5^{{{k}}} = {3 * 5 ** k}$. Two missing: $3 \\cdot 4^{{{k}}} = {3 * 4 ** k}$. All three missing: $3^{{{k}}} = {3 ** k}$.",
              f"Good: $6^{{{k}}} - {3 * 5 ** k} + {3 * 4 ** k} - {3 ** k} = {ans}$."], "stopping after one or two terms.")


@reg(S, "challenge")
def iec_exact_fixed(r):
    n = r.randint(4, 8)
    j = r.randint(1, n - 2)
    ans = comb(n, j) * D(n - j)
    p = f"${n}$ students put their names in a hat, and each draws one name at random. In how many of the ${n}!$ outcomes do exactly ${j}$ students draw their own name?"
    return Q(p, ans, [comb(n, j) * math.factorial(n - j), D(n), comb(n, j), ans + comb(n, j), comb(n, j) * (n - j - 1)], "Choose the lucky ones; the rest must all miss.",
             "the count.", f"pick the ${j}$ who get their own name; the other ${n - j}$ form a derangement.",
             [f"Choose: $\\binom{{{n}}}{{{j}}} = {comb(n, j)}$.", f"Derangements of ${n - j}$: $D_{{{n - j}}} = {D(n - j)}$ (from $D_n = (n - 1)(D_{{n-1}} + D_{{n-2}})$).", f"Total: ${ans}$."], "letting the others be arranged in any order.")


@reg(S, "challenge")
def iec_squarefree(r):
    N = r.choice([30, 50, 60, 80, 100, 120, 150])
    ans = sum(1 for x in range(1, N + 1) if all(x % (q * q) for q in (2, 3, 5, 7, 11)))
    p = f"How many integers from $1$ to ${N}$ are not divisible by any perfect square greater than $1$?"
    return Q(p, ans, [ans - 1, ans + 1, N - N // 4 - N // 9 - N // 25 - N // 49, N - ans, ans + N // 36], "Only squares of primes matter.",
             "the count.", "a number is divisible by a square $>1$ exactly when it is divisible by $p^2$ for some prime $p$. Remove multiples of $4, 9, 25, 49, \\ldots$ by inclusion and exclusion.",
             [f"Multiples of $4$: ${N // 4}$; $9$: ${N // 9}$; $25$: ${N // 25}$; $49$: ${N // 49}$" + (f"; $121$: ${N // 121}$" if N >= 121 else "") + ".",
              f"Add back multiples of $36$: ${N // 36}$" + (f", of $100$: ${N // 100}$" if N >= 100 else "") + ".", f"Result: ${ans}$."], "counting $36$ twice.")


@reg(S, "challenge")
def iec_couples_apart(r):
    n = r.choice([2, 3])
    people = list(range(2 * n))
    good = sum(1 for p_ in itertools.permutations(people) if all(abs(p_.index(2 * i) - p_.index(2 * i + 1)) != 1 for i in range(n)))
    tot = math.factorial(2 * n)
    p = f"${n}$ married couples sit in a row of ${2 * n}$ chairs. In how many seatings does no couple sit side by side?"
    terms = [(-1) ** k * comb(n, k) * 2 ** k * math.factorial(2 * n - k) for k in range(n + 1)]
    return Q(p, good, [tot - n * 2 * math.factorial(2 * n - 1), tot - good, good + 2 ** n, good * 2, tot // (n + 1)], "Inclusion and exclusion on the couples who sit together.",
             "the count.", "if $k$ chosen couples sit together, glue each into a block: $\\binom{" + str(n) + "}{k} \\cdot 2^k \\cdot (" + str(2 * n) + " - k)!$ seatings.",
             [" ".join(("+" if t > 0 and i else "-" if t < 0 else "") + f" {abs(t)}" for i, t in enumerate(terms)).strip().join(["$", f" = {good}$."])], "subtracting the together cases without adding back overlaps.")


@reg(S, "challenge")
def iec_avoid_words(r):
    letters = "ABCDEF"[:r.choice([5, 6])]
    w1, w2 = "AB", r.choice(["CD", "BC", "DE"])
    good = sum(1 for p_ in itertools.permutations(letters) if w1 not in "".join(p_) and w2 not in "".join(p_))
    n = len(letters)
    both = math.factorial(n - 2) if set(w1) & set(w2) == set() else math.factorial(n - 2)
    p = f"How many arrangements of the letters {letters} contain neither {w1} nor {w2} as consecutive letters?"
    return Q(p, good, [math.factorial(n) - 2 * math.factorial(n - 1), math.factorial(n) - good, good + math.factorial(n - 2), math.factorial(n) - math.factorial(n - 1), good - 2], "Treat each forbidden pair as a glued block.",
             "the count.", "subtract arrangements containing " + w1 + " or " + w2 + "; add back those containing both.",
             [f"All: ${n}! = {math.factorial(n)}$.", f"Containing {w1}: $({n - 1})! = {math.factorial(n - 1)}$; containing {w2}: also ${math.factorial(n - 1)}$.",
              f"Containing both: ${'(' + str(n - 2) + ')! = ' + str(math.factorial(n - 2)) if not set(w1) & set(w2) else 'the block ABC, so (' + str(n - 2) + ')! = ' + str(math.factorial(n - 2))}$.",
              f"Neither: ${math.factorial(n)} - {2 * math.factorial(n - 1)} + {math.factorial(n - 2)} = {good}$."], "forgetting to add back the arrangements that contain both.") if good == math.factorial(n) - 2 * math.factorial(n - 1) + both else None


@reg(S, "challenge")
def iec_paths_avoid_two(r):
    m, n = r.randint(4, 6), r.randint(4, 6)
    P1 = (r.randint(1, m - 2), r.randint(1, n - 2))
    P2 = (r.randint(P1[0], m - 1), r.randint(P1[1], n - 1))
    if P1 == P2:
        return None
    paths = lambda a, b: comb(a[0] - b[0] + a[1] - b[1], a[0] - b[0]) if a[0] >= b[0] and a[1] >= b[1] else 0
    O, T = (0, 0), (m, n)
    tot = paths(T, O)
    via1 = paths(P1, O) * paths(T, P1)
    via2 = paths(P2, O) * paths(T, P2)
    via12 = paths(P1, O) * paths(P2, P1) * paths(T, P2)
    ans = tot - via1 - via2 + via12
    p = f"How many shortest grid paths (steps right or up) from $(0, 0)$ to $({m}, {n})$ avoid both $({P1[0]}, {P1[1]})$ and $({P2[0]}, {P2[1]})$?"
    return Q(p, ans, [tot - via1 - via2, tot - via1, tot, ans + via12, ans - 1], "Subtract paths through each point, then add back paths through both.",
             "the count.", "inclusion and exclusion on the two bad points.",
             [f"All: $\\binom{{{m + n}}}{{{m}}} = {tot}$.", f"Through $({P1[0]}, {P1[1]})$: ${via1}$. Through $({P2[0]}, {P2[1]})$: ${via2}$.", f"Through both: ${via12}$.", f"${tot} - {via1} - {via2} + {via12} = {ans}$."], "forgetting paths that go through both points.")


@reg(S, "challenge")
def iec_one_of_each(r):
    a, b, c = r.randint(2, 4), r.randint(2, 4), r.randint(2, 4)
    n = a + b + c
    k = r.randint(3, 5)
    ans = comb(n, k) - comb(n - a, k) - comb(n - b, k) - comb(n - c, k) + comb(c, k) + comb(a, k) + comb(b, k)
    p = f"A team of ${k}$ is chosen from ${a}$ freshmen, ${b}$ sophomores, and ${c}$ juniors. How many teams include at least one student from each grade?"
    return Q(p, ans, [comb(n, k), a * b * c * comb(n - 3, k - 3), comb(n, k) - comb(n - a, k) - comb(n - b, k) - comb(n - c, k), ans + 1, ans - comb(a, k) - comb(b, k) - comb(c, k) if ans - comb(a, k) - comb(b, k) - comb(c, k) > 0 else ans + 3],
             "Subtract teams missing a grade; add back teams missing two.", "the count.", "inclusion and exclusion on the grades that are missing.",
             [f"All: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$.", f"Missing freshmen: $\\binom{{{n - a}}}{{{k}}} = {comb(n - a, k)}$; sophomores: ${comb(n - b, k)}$; juniors: ${comb(n - c, k)}$.",
              f"Missing two grades (all from one grade): ${comb(a, k)} + {comb(b, k)} + {comb(c, k)}$.", f"Total: ${ans}$."], "choosing one from each grade first and then any others, which double counts.")


# ================================================================ cp_probability
S = "cp_probability"


@reg(S, "basics")
def pr_red_or_rank(r):
    rank = r.choice(["king", "queen", "jack", "ace", "7"])
    ans = F(26 + 2, 52)
    p = f"A card is drawn from a standard $52$-card deck. What is the probability it is red or a {rank}?"
    return Q(p, ans, [F(30, 52), F(26, 52), F(2, 52), F(24, 52), F(4, 52)], "Two of the " + rank + "s are already red.",
             "the probability.", "count the red cards plus the black " + rank + "s.",
             ["Red: $26$. Black " + rank + "s: $2$.", f"$\\frac{{28}}{{52}} = {ft(ans)}$."], "counting the red " + rank + "s twice.")


@reg(S, "basics")
def pr_dice_diff(r):
    d = r.randint(0, 4)
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == d)
    ans = F(ways, 36)
    p = f"Two fair dice are rolled. What is the probability that the two numbers differ by exactly ${d}$?"
    return Q(p, ans, [F(6 - d, 36), F(ways, 21), F(ways + 2, 36), F(1, 6), F(2 * ways, 36) if d else F(1, 3)], "List the pairs, counting each order.",
             "the probability.", "count ordered pairs $(a, b)$ with $|a - b| = " + str(d) + "$.",
             [f"Pairs: ${ways}$ out of $36$.", f"${ft(ans)}$."], "counting $(a, b)$ and $(b, a)$ as one outcome.")


@reg(S, "basics")
def pr_dice_beats(r):
    d = r.randint(1, 3)
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a - b >= d)
    ans = F(ways, 36)
    nm = r.sample(NAMES, 2)
    p = f"{nm[0]} and {nm[1]} each roll a fair die. What is the probability that {nm[0]}'s number is at least ${d}$ more than {nm[1]}'s?"
    return Q(p, ans, [F(2 * ways, 36), F(ways + 6, 36), F(1, 2), F(ways, 30), F(ways - 1, 36)], "Fix " + nm[1] + "'s roll and count.",
             "the probability.", "casework on the smaller roll.",
             [f"Favorable pairs: ${ways}$.", f"$\\frac{{{ways}}}{{36}} = {ft(ans)}$."], "counting the differences in both directions.")


@reg(S, "basics")
def pr_committee_both(r):
    n, k = r.randint(6, 12), r.randint(2, 5)
    a, b = r.sample(NAMES, 2)
    ans = F(comb(n - 2, k - 2), comb(n, k))
    p = f"A group of ${k}$ is chosen at random from ${n}$ people, including {a} and {b}. What is the probability both {a} and {b} are chosen?"
    return Q(p, ans, [F(k, n) * F(k, n), F(k, n), F(2, n), F(comb(n - 2, k - 1), comb(n, k)), F(k - 1, n - 1)], "Count groups with both of them.",
             "the probability.", "favorable groups over all groups.",
             [f"With both: $\\binom{{{n - 2}}}{{{k - 2}}} = {comb(n - 2, k - 2)}$. All: $\\binom{{{n}}}{{{k}}} = {comb(n, k)}$.", f"$\\frac{{{comb(n - 2, k - 2)}}}{{{comb(n, k)}}} = {ft(ans)}$."], "multiplying $\\frac{k}{n}$ by itself as if the choices were independent.")


@reg(S, "basics")
def pr_line_adjacent(r):
    n = r.randint(4, 10)
    a, b = r.sample(NAMES, 2)
    ans = F(2, n)
    p = f"${n}$ people, including {a} and {b}, line up in random order. What is the probability {a} and {b} are next to each other?"
    return Q(p, ans, [F(1, n), F(2, n - 1), F(1, n - 1), F(n - 1, comb(n, 2) * 2), F(2, n + 1)], "Glue them together.",
             "the probability.", f"together: $2 \\cdot ({n} - 1)!$ orders out of ${n}!$.",
             [f"$\\frac{{2 \\cdot {n - 1}!}}{{{n}!}} = \\frac{{2}}{{{n}}}$."], "forgetting they can be in either order.")


@reg(S, "basics")
def pr_all_same(r):
    k = r.randint(3, 7)
    ans = F(2, 2 ** k)
    p = f"${k}$ fair coins are flipped. What is the probability they all land the same way?"
    return Q(p, ans, [F(1, 2 ** k), F(1, 2), F(k, 2 ** k), F(2, k), F(1, 2 ** (k - 1) + 1)], "All heads or all tails.",
             "the probability.", "two favorable outcomes out of $2^" + str(k) + "$.",
             [f"$\\frac{{2}}{{2^{{{k}}}}} = {ft(ans)}$."], "counting only all heads.")


@reg(S, "basics")
def pr_number_divisible(r):
    a, b = r.sample([2, 3, 5, 7], 2)
    N = r.choice([30, 50, 60, 100, 120])
    cnt = N // a + N // b - N // (a * b)
    ans = F(cnt, N)
    p = f"An integer is chosen at random from $1$ to ${N}$. What is the probability it is divisible by ${a}$ or ${b}$?"
    return Q(p, ans, [F(N // a + N // b, N), F(1, a) * F(1, b), F(1, a) + F(1, b) if F(1, a) + F(1, b) != ans else ans + F(1, N), F(N - cnt, N), F(cnt - 1, N)], "Inclusion and exclusion.",
             "the probability.", f"count multiples of ${a}$ or ${b}$, subtracting multiples of ${a * b}$.",
             [f"${N // a} + {N // b} - {N // (a * b)} = {cnt}$.", f"$\\frac{{{cnt}}}{{{N}}} = {ft(ans)}$."], "not subtracting the overlap.")


@reg(S, "basics")
def pr_same_color_two(r):
    a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
    n = a + b + c
    ans = F(comb(a, 2) + comb(b, 2) + comb(c, 2), comb(n, 2))
    p = f"A bag holds ${a}$ red, ${b}$ green, and ${c}$ yellow marbles. Two are drawn without replacement. What is the probability they are the same color?"
    wr = F(a * a + b * b + c * c, n * n)
    return Q(p, ans, [wr if wr != ans else ans + F(1, n * n), F(1, 3), F(comb(a, 2), comb(n, 2)), 1 - ans, F(comb(a, 2) + comb(b, 2) + comb(c, 2), n * (n - 1))], "Add the cases for each color.",
             "the probability.", "pairs of the same color over all pairs.",
             [f"Same-color pairs: $\\binom{{{a}}}{{2}} + \\binom{{{b}}}{{2}} + \\binom{{{c}}}{{2}} = {comb(a, 2) + comb(b, 2) + comb(c, 2)}$.", f"All pairs: $\\binom{{{n}}}{{2}} = {comb(n, 2)}$.", f"${ft(ans)}$."], "drawing with replacement.")


@reg(S, "basics")
def pr_replace_diff(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    n = a + b
    ans = F(2 * a * b, n * n)
    p = f"A bag holds ${a}$ white and ${b}$ black balls. A ball is drawn, its color noted, and it is put back. Then a second ball is drawn. What is the probability the two balls are different colors?"
    return Q(p, ans, [F(a * b, n * n), F(2 * a * b, n * (n - 1)), F(1, 2), F(a * a + b * b, n * n), ans + F(1, n * n)], "White then black, or black then white.",
             "the probability.", "with replacement the draws are independent; add the two orders.",
             [f"White then black: $\\frac{{{a}}}{{{n}}} \\cdot \\frac{{{b}}}{{{n}}}$. Black then white: the same.", f"$\\frac{{2 \\cdot {a} \\cdot {b}}}{{{n}^2}} = {ft(ans)}$."], "counting only one order.")


@reg(S, "basics")
def pr_spinner_even(r):
    a, b = r.randint(3, 9), r.randint(3, 9)
    ways = sum(1 for x in range(1, a + 1) for y in range(1, b + 1) if (x + y) % 2 == 0)
    ans = F(ways, a * b)
    p = f"Spinner A has sections $1$ to ${a}$ and spinner B has sections $1$ to ${b}$, each equally likely. Both are spun. What is the probability the sum is even?"
    return Q(p, ans, [F(1, 2) if ans != F(1, 2) else F(ways + 1, a * b), F(ways, a * b + 1), 1 - ans if 1 - ans != ans else F(ways - 1, a * b), F((a // 2) * (b // 2), a * b), F(ways + 2, a * b)], "Even sum: both even or both odd.",
             "the probability.", "count parity matches.",
             [f"Spinner A: ${a // 2}$ even, ${(a + 1) // 2}$ odd. Spinner B: ${b // 2}$ even, ${(b + 1) // 2}$ odd.", f"Both even: ${(a // 2) * (b // 2)}$; both odd: ${((a + 1) // 2) * ((b + 1) // 2)}$.", f"$\\frac{{{ways}}}{{{a * b}}} = {ft(ans)}$."], "assuming the answer is always one half.")


@reg(S, "basics")
def pr_at_least_one_indep(r):
    p1, p2 = F(r.randint(1, 4), 5), F(r.randint(1, 5), 6)
    ans = 1 - (1 - p1) * (1 - p2)
    a, b = r.sample(NAMES, 2)
    p = f"{a} hits a target with probability ${ft(p1)}$ and {b} with probability ${ft(p2)}$, independently. Each shoots once. What is the probability the target is hit at least once?"
    return Q(p, ans, [p1 * p2, min(p1 + p2, F(99, 100)) if p1 + p2 < 1 else p1 + p2 - p1 * p2 * 2, (1 - p1) * (1 - p2), p1 + p2 - p1 * p2 + F(1, 30), 1 - p1 * p2], "Find the chance both miss.",
             "the probability.", "complement: at least one hit $= 1 -$ (both miss).",
             [f"Both miss: ${ft(1 - p1)} \\cdot {ft(1 - p2)} = {ft((1 - p1) * (1 - p2))}$.", f"$1 - {ft((1 - p1) * (1 - p2))} = {ft(ans)}$."], "adding the two probabilities.")


@reg(S, "basics")
def pr_max_two_dice(r):
    m = r.randint(2, 6)
    ans = F(2 * m - 1, 36)
    p = f"Two fair dice are rolled. What is the probability that the larger of the two numbers is ${m}$?"
    return Q(p, ans, [F(m * m, 36), F(2 * m, 36), F(1, 6), F((m - 1) ** 2, 36), F(2 * m + 1, 36)], "Both at most " + str(m) + ", minus both at most " + str(m - 1) + ".",
             "the probability.", f"max $\\le {m}$ has ${m}^2$ outcomes; subtract those with max $\\le {m - 1}$.",
             [f"${m}^2 - {m - 1}^2 = {2 * m - 1}$.", f"$\\frac{{{2 * m - 1}}}{{36}}$."], "counting the double " + str(m) + " twice.")


@reg(S, "basics")
def pr_side_of_polygon(r):
    n = r.randint(5, 12)
    ans = F(n, comb(n, 2))
    p = f"Two different vertices of a regular ${n}$-gon are chosen at random. What is the probability they are joined by a side of the polygon (not a diagonal)?"
    return Q(p, ans, [F(1, n), F(2, n), F(n - 3, n - 1), F(n, n * n), F(3, n - 1)], "Count sides versus all pairs.",
             "the probability.", f"${n}$ sides out of $\\binom{{{n}}}{{2}}$ pairs.",
             [f"$\\frac{{{n}}}{{{comb(n, 2)}}} = {ft(ans)}$."], "using the number of diagonals as the total.")


@reg(S, "basics")
def pr_all_distinct(r):
    n, k = r.randint(4, 10), r.randint(2, 4)
    if k > n:
        return None
    ans = F(math.perm(n, k), n ** k)
    p = f"${k}$ friends each pick a whole number from $1$ to ${n}$ at random. What is the probability they all pick different numbers?"
    return Q(p, ans, [F(comb(n, k), n ** k), 1 - ans, F(n - k + 1, n), F(math.perm(n, k), n ** k) * F(n - 1, n), F(1, math.factorial(k))], "Each friend in turn must avoid the earlier picks.",
             "the probability.", "multiply the chances that each new pick is new.",
             [" \\cdot ".join(f"\\frac{{{n - i}}}{{{n}}}" for i in range(k)).join(["$", f" = {ft(ans)}$."])], "using combinations, which ignore who picked what.")


@reg(S, "basics")
def pr_conditional_dice(r):
    kind = r.choice(["six", "sum"])
    if kind == "six":
        good, cond = 1, 11
        p = "Two fair dice are rolled. Given that at least one die shows a $6$, what is the probability that both dice show $6$?"
        steps = ["Outcomes with at least one $6$: $36 - 25 = 11$.", "Both $6$: $1$.", "$\\frac{1}{11}$."]
    else:
        s = r.randint(7, 10)
        outs = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b >= s]
        good, cond = sum(1 for a, b in outs if a == b), len(outs)
        p = f"Two fair dice are rolled. Given that the sum is at least ${s}$, what is the probability the two numbers are equal?"
        steps = [f"Outcomes with sum at least ${s}$: ${cond}$.", f"Among them, doubles: ${good}$.", f"${ft(F(good, cond))}$."]
    ans = F(good, cond)
    return Q(p, ans, [F(good, 36), F(1, 6), F(good, cond + 1), F(good + 1, cond), F(1, 36) if kind == "six" else F(good, 21)], "Shrink the sample space to the given outcomes.",
             "the conditional probability.", "only count outcomes that satisfy the condition.", steps, "dividing by 36 instead of the restricted count.")


@reg(S, "basics")
def pr_word_ends(r):
    word = r.choice(["PLANET", "CASTLE", "MOUNTAIN", "GARDEN", "FOREST", "BRIDGE", "SILVER", "MARBLE"])
    if len(set(word)) != len(word):
        return None
    n = len(word)
    c = sum(1 for ch in word if ch not in "AEIOU")
    ans = F(c * (c - 1), n * (n - 1))
    p = f"The letters of {word} are arranged in random order. What is the probability the first and last letters are both consonants?"
    return Q(p, ans, [F(c * c, n * n), F(c, n), F(c - 1, n - 1), F(comb(c, 2), comb(n, 2) * 2), 1 - ans], "Fill the first spot, then the last.",
             "the probability.", "first letter a consonant, then last letter one of the remaining consonants.",
             [f"Consonants: ${c}$ of ${n}$.", f"$\\frac{{{c}}}{{{n}}} \\cdot \\frac{{{c - 1}}}{{{n - 1}}} = {ft(ans)}$."], "treating the two spots as independent.")


@reg(S, "challenge")
def prc_first_success(r):
    p1 = F(1, r.choice([2, 3, 4, 6]))
    q = 1 - p1
    ans = p1 / (1 - q * q)
    a, b = r.sample(NAMES, 2)
    what = {F(1, 2): "flips a coin; the first to flip heads wins", F(1, 3): "rolls a die; the first to roll a $1$ or $2$ wins", F(1, 4): "draws a card (with replacement); the first to draw a heart wins", F(1, 6): "rolls a die; the first to roll a $6$ wins"}[p1]
    p = f"{a} and {b} take turns, {a} first. Each turn, the player {what}. What is the probability {a} wins?"
    return Q(p, ans, [F(1, 2), p1, 1 - ans, p1 / (1 - q), ans + F(1, 20)], "Sum a geometric series over " + a + "'s turns.",
             "the probability.", f"{a} wins on turn $1$, $3$, $5$, ...; each full round of misses has probability ${ft(q)}^2$.",
             [f"$P = {ft(p1)} + {ft(q * q)} \\cdot {ft(p1)} + \\cdots = \\frac{{{ft(p1)}}}{{1 - {ft(q * q)}}} = {ft(ans)}$."], "assuming both players have equal chances.")


@reg(S, "challenge")
def prc_bayes(r):
    r1, b1, r2, b2 = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    pa, pb = F(r1, r1 + b1), F(r2, r2 + b2)
    if pa == pb:
        return None
    ans = pa / (pa + pb)
    p = f"Box 1 has ${r1}$ red and ${b1}$ blue balls; box 2 has ${r2}$ red and ${b2}$ blue. A box is picked at random and a ball is drawn from it. The ball is red. What is the probability it came from box 1?"
    return Q(p, ans, [F(r1, r1 + r2), F(1, 2) if ans != F(1, 2) else F(r1 + 1, r1 + r2 + 1), pa, pa / 2, 1 - ans if 1 - ans != ans else ans + F(1, 10)], "Compare the chances of 'box 1 and red' and 'box 2 and red'.",
             "the conditional probability.", "Bayes: P(box 1 | red) = P(box 1 and red) / P(red).",
             [f"Box 1 and red: $\\frac{{1}}{{2}} \\cdot {ft(pa)}$. Box 2 and red: $\\frac{{1}}{{2}} \\cdot {ft(pb)}$.", f"$\\frac{{{ft(pa)}}}{{{ft(pa)} + {ft(pb)}}} = {ft(ans)}$."], "comparing red ball counts instead of probabilities.")


@reg(S, "challenge")
def prc_increasing_dice(r):
    kind = r.choice(["strictly", "non"])
    cnt = comb(6, 3) if kind == "strictly" else comb(8, 3)
    ans = F(cnt, 216)
    p = f"Three fair dice are rolled one after another. What is the probability the numbers are {'strictly increasing' if kind == 'strictly' else 'in non-decreasing order (each at least the one before)'}?"
    return Q(p, ans, [F(comb(6, 3), 216) if kind != "strictly" else F(comb(8, 3), 216), F(1, 6), F(math.perm(6, 3), 216), F(cnt, 120), F(cnt + 6, 216)], "Each set of numbers has one good order.",
             "the probability.", ("choose 3 different numbers; only one order is increasing." if kind == "strictly" else "a non-decreasing sequence is a multiset of 3 numbers from 6: Stars and Bars."),
             [(f"$\\binom{{6}}{{3}} = 20$" if kind == "strictly" else f"$\\binom{{6 + 3 - 1}}{{3}} = \\binom{{8}}{{3}} = 56$") + " good outcomes.", f"$\\frac{{{cnt}}}{{216}} = {ft(ans)}$."], "dividing by 3! for repeated numbers too.")


@reg(S, "challenge")
def prc_three_dice_sum(r):
    kind = r.choice(["prime", "square", "mult"])
    m = r.choice([3, 4, 5])
    test = {"prime": lambda s: s > 1 and all(s % d for d in range(2, s)), "square": lambda s: math.isqrt(s) ** 2 == s, "mult": lambda s: s % m == 0}[kind]
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if test(a + b + c))
    ans = F(ways, 216)
    desc = {"prime": "a prime number", "square": "a perfect square", "mult": f"a multiple of ${m}$"}[kind]
    good_s = [s for s in range(3, 19) if test(s)]
    cnt = {s: sum(1 for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if a + b + c == s) for s in good_s}
    p = f"Three fair dice are rolled. What is the probability the sum is {desc}?"
    return Q(p, ans, [F(len(good_s), 16), F(ways + 3, 216), F(ways - 3, 216), 1 - ans, F(ways, 6 ** 2 * 5)], "Count the outcomes for each possible sum.",
             "the probability.", "sums go from $3$ to $18$; count ordered outcomes for each qualifying sum.",
             ["Sums: " + ", ".join(f"${s}$: ${cnt[s]}$" for s in good_s) + ".", f"Total: ${ways}$ of $216$, so ${ft(ans)}$."], "treating the 16 sums as equally likely.")


@reg(S, "challenge")
def prc_gambler(r):
    N = r.randint(5, 12)
    a = r.randint(1, N - 1)
    ans = F(a, N)
    nm = r.choice(NAMES)
    p = f"{nm} starts with $\\${a}$ and bets $\\$1$ at a time on fair coin flips, winning or losing $\\$1$ each flip. {nm} stops upon reaching $\\${N}$ or $\\$0$. What is the probability {nm} reaches $\\${N}$?"
    return Q(p, ans, [F(1, 2), F(a, N + 1), F(N - a, N), F(a + 1, N + 1), F(a, 2 * N)], "A fair game: the expected amount never changes.",
             "the probability.", "the game is fair, so " + nm + "'s expected final amount equals the starting amount.",
             [f"If $p$ is the chance of reaching ${N}$: $p \\cdot {N} + (1 - p) \\cdot 0 = {a}$.", f"$p = {ft(ans)}$."], "guessing one half.")


@reg(S, "challenge")
def prc_same_suit_hand(r):
    k = r.randint(2, 4)
    ans = F(4 * comb(13, k), comb(52, k))
    p = f"${k}$ cards are dealt from a well-shuffled $52$-card deck. What is the probability they are all the same suit?"
    return Q(p, ans, [F(comb(13, k), comb(52, k)), F(1, 4 ** (k - 1)), F(1, 4 ** k), ans * 2, F(math.perm(12, k - 1), math.perm(51, k - 1)) * F(1, 2)], "Every card after the first must match its suit.",
             "the probability.", "the first card sets the suit; each next card must match from what's left.",
             [" \\cdot ".join(f"\\frac{{{12 - i}}}{{{51 - i}}}" for i in range(k - 1)).join(["$", f" = {ft(ans)}$."])], "using $\\frac{1}{4}$ for each card, as if with replacement.")


@reg(S, "challenge")
def prc_round_neighbors(r):
    n = r.randint(5, 10)
    a, b, c = r.sample(NAMES, 3)
    ans = F(2, (n - 1) * (n - 2))
    p = f"${n}$ people, including {a}, {b}, and {c}, sit at random around a round table. What is the probability {a} sits between {b} and {c} (next to both)?"
    return Q(p, ans, [F(2, n - 1), F(1, (n - 1) * (n - 2)), F(2, n * (n - 1)), F(4, (n - 1) * (n - 2)), F(1, comb(n - 1, 2) * 3)], "Fix " + a + "'s seat.",
             "the probability.", f"{a}'s two neighbors are a random pair from the other ${n - 1}$ people.",
             [f"Ordered pairs of neighbors (left, right): ${n - 1} \\cdot {n - 2} = {(n - 1) * (n - 2)}$.", f"Good: $2$ ({b} left and {c} right, or the reverse).", f"${ft(ans)}$."], "forgetting the two orders.")


# ================================================================ cp_expected
S = "cp_expected"


@reg(S, "basics")
def ev_sum_dice(r):
    k = r.randint(2, 8)
    ans = F(7 * k, 2)
    p = f"${k}$ fair dice are rolled. What is the expected value of the sum?"
    return Q(p, ans, [F(6 * k, 2), 6 * k, F(7, 2), 7 * k, ans + 1], "Add the expected value of each die.",
             "the expected sum.", "linearity of expectation: each die averages $\\frac{7}{2}$.",
             [f"${k} \\cdot \\frac{{7}}{{2}} = {ft(ans)}$."], "using 3 as the average roll.")


@reg(S, "basics")
def ev_biased_heads(r):
    n = r.randint(5, 30)
    pr = F(r.randint(1, 4), 5)
    ans = n * pr
    p = f"A coin lands heads with probability ${ft(pr)}$. It is flipped ${n}$ times. What is the expected number of heads?"
    return Q(p, ans, [F(n, 2), n * (1 - pr), ans + 1, n * pr * pr, F(n, 5)], "Each flip contributes its probability.",
             "the expected count.", "linearity: $n \\cdot p$.",
             [f"${n} \\cdot {ft(pr)} = {ft(ans)}$."], "assuming a fair coin.")


@reg(S, "basics")
def ev_red_drawn(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    k = r.randint(2, min(a + b - 1, 6))
    ans = F(k * a, a + b)
    p = f"A bag holds ${a}$ red and ${b}$ green marbles. ${k}$ marbles are drawn without replacement. What is the expected number of red marbles drawn?"
    return Q(p, ans, [F(k, 2), F(a, a + b), F(k * a, a + b - 1), F(a, k), ans + F(1, 2)], "Each draw is red with the same probability.",
             "the expected count.", "by symmetry each of the " + str(k) + " draws is red with probability $\\frac{" + str(a) + "}{" + str(a + b) + "}$; add them up.",
             [f"${k} \\cdot \\frac{{{a}}}{{{a + b}}} = {ft(ans)}$."], "thinking 'without replacement' changes the expected value.")


@reg(S, "basics")
def ev_guess_score(r):
    n = r.randint(10, 30)
    k = r.choice([4, 5])
    w, l = r.choice([(4, 1), (6, 1), (5, 2), (3, 1)])
    ans = n * (F(w, k) - F(l * (k - 1), k))
    p = f"A test has ${n}$ questions with ${k}$ choices each. A correct answer earns ${w}$ points and a wrong answer loses ${l}$. A student guesses randomly on every question. What is the expected score?"
    return Q(p, ans, [n * F(w, k), 0 if ans != 0 else F(n, k), n * (F(w, k) - F(l, k)), F(n * w, 2), ans + w], "Find the expected points on one question.",
             "the expected score.", "per question: (chance right)(points) minus (chance wrong)(penalty); then multiply by " + str(n) + ".",
             [f"One question: $\\frac{{1}}{{{k}}} \\cdot {w} - \\frac{{{k - 1}}}{{{k}}} \\cdot {l} = {ft(F(w, k) - F(l * (k - 1), k))}$.", f"Total: ${n} \\cdot {ft(F(w, k) - F(l * (k - 1), k))} = {ft(ans)}$."], "ignoring the penalty.")


@reg(S, "basics")
def ev_shared_month(r):
    n = r.randint(4, 12)
    ans = F(comb(n, 2), 12)
    p = f"${n}$ people each have a birthday month chosen at random (all $12$ months equally likely). What is the expected number of pairs of people who share a birth month?"
    return Q(p, ans, [F(n, 12), F(comb(n, 2), 144), F(n * n, 12), ans + 1, F(comb(n, 2), 11)], "Each pair shares a month with probability $\\frac{1}{12}$.",
             "the expected number of pairs.", "linearity over all pairs.",
             [f"Pairs: $\\binom{{{n}}}{{2}} = {comb(n, 2)}$.", f"${comb(n, 2)} \\cdot \\frac{{1}}{{12}} = {ft(ans)}$."], "using $\\frac{1}{144}$ for one pair.")


@reg(S, "basics")
def ev_square_uniform(r):
    n = r.randint(3, 10)
    ans = F((n + 1) * (2 * n + 1), 6)
    p = f"An integer $x$ is chosen at random from $1$ to ${n}$. What is the expected value of $x^2$?"
    return Q(p, ans, [F((n + 1) ** 2, 4), F(n * (n + 1) * (2 * n + 1), 6), F(n * n, 2), ans + 1, F(n * (n + 1), 2)], "Average the squares.",
             "the expected value.", "$\\frac{1^2 + 2^2 + \\cdots + n^2}{n}$, with the sum of squares formula.",
             [f"Sum: $\\frac{{{n} \\cdot {n + 1} \\cdot {2 * n + 1}}}{{6}} = {n * (n + 1) * (2 * n + 1) // 6}$.", f"Divide by ${n}$: ${ft(ans)}$."], "squaring the average instead of averaging the squares.")


@reg(S, "basics")
def ev_product_spinners(r):
    a, b = r.randint(3, 10), r.randint(3, 10)
    ans = F((a + 1) * (b + 1), 4)
    p = f"Spinner A shows $1$ to ${a}$ and spinner B shows $1$ to ${b}$, all equally likely. What is the expected value of the product of the two results?"
    return Q(p, ans, [F(a * b, 4), F(a * b, 2), F((a + 1) + (b + 1), 2), ans + 1, F((a + 1) * (b + 1), 2)], "The spinners are independent.",
             "the expected product.", "for independent results, $E[XY] = E[X] \\cdot E[Y]$.",
             [f"$E[X] = \\frac{{{a + 1}}}{{2}}$, $E[Y] = \\frac{{{b + 1}}}{{2}}$.", f"Product: ${ft(ans)}$."], "using $\\frac{a}{2}$ for the average of $1$ to $a$.")


@reg(S, "basics")
def ev_mixed_pairs(r):
    b, g = r.randint(2, 8), r.randint(2, 8)
    n = b + g
    ans = F(2 * b * g, n)
    p = f"${b}$ boys and ${g}$ girls stand in a random order in a line. What is the expected number of neighboring pairs made up of one boy and one girl?"
    return Q(p, ans, [F(b * g, n), F(n - 1, 2), F(2 * b * g, n - 1), ans + 1, F(b * g, n - 1)], "There are " + str(n - 1) + " neighboring spots; find the chance each is mixed.",
             "the expected count.", "linearity over the $" + str(n - 1) + "$ neighboring pairs.",
             [f"A given pair is mixed with probability $\\frac{{2 \\cdot {b} \\cdot {g}}}{{{n} \\cdot {n - 1}}}$.", f"Times ${n - 1}$: ${ft(ans)}$."], "using one half for each pair.")


@reg(S, "basics")
def ev_empty_boxes(r):
    n, k = r.randint(2, 5), r.randint(2, 4)
    ans = n * F(n - 1, n) ** k
    p = f"${k}$ balls are each tossed into one of ${n}$ boxes at random. What is the expected number of empty boxes?"
    return Q(p, ans, [F(n - k, 1) if n > k else F(1, n), F(n - 1, n) ** k, n * F(1, n) ** k, ans + F(1, 2), n * F(n - 1, n) ** (k - 1)], "Find the chance a given box stays empty.",
             "the expected number.", "linearity: each box is empty with probability $\\left(\\frac{" + str(n - 1) + "}{" + str(n) + "}\\right)^{" + str(k) + "}$.",
             [f"One box empty: $\\left(\\frac{{{n - 1}}}{{{n}}}\\right)^{{{k}}} = {ft(F(n - 1, n) ** k)}$.", f"Times ${n}$: ${ft(ans)}$."], "subtracting the number of balls from the number of boxes.")


@reg(S, "basics")
def ev_runs(r):
    n = r.randint(4, 20)
    ans = 1 + F(n - 1, 2)
    p = f"A fair coin is flipped ${n}$ times. A run is a maximal block of identical results (HHTHH has $3$ runs). What is the expected number of runs?"
    return Q(p, ans, [F(n, 2), F(n - 1, 2), F(n + 2, 2), ans + 1, F(n, 3)], "Count the places where the result changes.",
             "the expected number of runs.", "runs $= 1 +$ (number of changes); each of the $" + str(n - 1) + "$ gaps is a change with probability $\\frac{1}{2}$.",
             [f"$1 + \\frac{{{n - 1}}}{{2}} = {ft(ans)}$."], "forgetting the first run.")


@reg(S, "basics")
def ev_blue_before_red(r):
    a, b = r.randint(1, 6), r.randint(2, 10)
    ans = F(b, a + 1)
    p = f"A bag holds ${a}$ red and ${b}$ blue marbles. Marbles are drawn one at a time without replacement until a red one appears. What is the expected number of blue marbles drawn before it?"
    return Q(p, ans, [F(b, a), F(b, 2), F(b + 1, a + 1), F(b, a + b), ans + 1], "Where does each blue marble land relative to the reds?",
             "the expected count.", f"the ${a}$ reds split the order into ${a + 1}$ gaps; each blue marble is equally likely to be in any gap, so it comes before every red with probability $\\frac{{1}}{{{a + 1}}}$.",
             [f"${b} \\cdot \\frac{{1}}{{{a + 1}}} = {ft(ans)}$."], f"using $\\frac{{{b}}}{{{a}}}$.")


@reg(S, "basics")
def ev_pay_square(r):
    n = r.choice([4, 6, 8])
    ans = F((n + 1) * (2 * n + 1), 6)
    nm = r.choice(NAMES)
    p = f"{nm} rolls a fair ${n}$-sided die (faces $1$ to ${n}$) and wins the square of the roll in dollars. What is the expected amount won, in dollars?"
    return Q(p, ans, [F((n + 1) ** 2, 4), F(n * n, 2), F(n * (n + 1) * (2 * n + 1), 6), ans + 1, F(n + 1, 2)], "Average the squares.",
             "the expected winnings.", "$E[X^2]$ is not $(E[X])^2$.",
             [f"$\\frac{{1^2 + \\cdots + {n}^2}}{{{n}}} = \\frac{{{n * (n + 1) * (2 * n + 1) // 6}}}{{{n}}} = {ft(ans)}$."], "squaring the average roll.")


@reg(S, "basics")
def ev_subset_sum(r):
    n = r.randint(4, 15)
    ans = F(n * (n + 1), 4)
    p = f"A subset of $\\{{1, 2, \\ldots, {n}\\}}$ is chosen at random (all $2^{{{n}}}$ subsets equally likely). What is the expected sum of its elements?"
    return Q(p, ans, [F(n * (n + 1), 2), F(n + 1, 2), F(n * (n + 1), 8), ans + 1, F(n * n, 4)], "Each number is in the subset half the time.",
             "the expected sum.", "linearity: each element contributes itself times $\\frac{1}{2}$.",
             [f"$\\frac{{1}}{{2}}(1 + 2 + \\cdots + {n}) = \\frac{{1}}{{2}} \\cdot {n * (n + 1) // 2} = {ft(ans)}$."], "forgetting the factor of one half.")


@reg(S, "basics")
def ev_two_cards(r):
    n = r.randint(5, 20)
    ans = n + 1
    p = f"Two cards are drawn without replacement from cards numbered $1$ to ${n}$. What is the expected sum of the two numbers?"
    return Q(p, ans, [F(n + 1, 2), n, 2 * n, n + 2, F(n * (n + 1), 4)], "Each card drawn averages the same.",
             "the expected sum.", "linearity still works without replacement: each draw averages $\\frac{" + str(n + 1) + "}{2}$.",
             [f"$2 \\cdot \\frac{{{n + 1}}}{{2}} = {n + 1}$."], "thinking the second draw has a different average.")


@reg(S, "basics")
def ev_shots(r):
    a, b = r.randint(2, 8), r.randint(2, 8)
    p2, p3 = F(r.randint(2, 7), 10), F(r.randint(1, 5), 10)
    ans = 2 * a * p2 + 3 * b * p3
    nm = r.choice(NAMES)
    p = f"{nm} takes ${a}$ two-point shots, each made with probability ${ft(p2)}$, and ${b}$ three-point shots, each made with probability ${ft(p3)}$. What is the expected number of points?"
    return Q(p, ans, [a * p2 + b * p3, 2 * a + 3 * b, 2 * a * p2 + 3 * b * p2, ans + 1, (a + b) * (p2 + p3)], "Add the expected points of every shot.",
             "the expected points.", "linearity over all the shots.",
             [f"Two-pointers: ${a} \\cdot 2 \\cdot {ft(p2)} = {ft(2 * a * p2)}$.", f"Three-pointers: ${b} \\cdot 3 \\cdot {ft(p3)} = {ft(3 * b * p3)}$.", f"Total: ${ft(ans)}$."], "forgetting the point values.")


@reg(S, "basics")
def ev_distinct_faces(r):
    k = r.randint(2, 4)
    ans = 6 * (1 - F(5, 6) ** k)
    p = f"${k}$ fair dice are rolled. What is the expected number of different numbers that appear?"
    return Q(p, ans, [F(k, 1), 6 * F(1, 6) * k, 6 * (1 - F(1, 6) ** k), ans + F(1, 6), 6 - k * F(5, 6)], "For each face, find the chance it appears.",
             "the expected count.", "linearity over the $6$ faces: face $j$ appears with probability $1 - \\left(\\frac{5}{6}\\right)^{" + str(k) + "}$.",
             [f"$1 - \\left(\\frac{{5}}{{6}}\\right)^{{{k}}} = {ft(1 - F(5, 6) ** k)}$.", f"Times $6$: ${ft(ans)}$."], "answering " + str(k) + ", forgetting repeats.")


@reg(S, "challenge")
def evc_coupon(r):
    n = r.randint(2, 6)
    ans = n * sum(F(1, i) for i in range(1, n + 1))
    p = f"A fair ${n}$-sided die is rolled until every face has appeared at least once. What is the expected number of rolls?"
    return Q(p, ans, [F(n * n, 1), F(n * (n + 1), 2), ans + 1, n * sum(F(1, i) for i in range(1, n)), F(2 * n, 1)], "Split the wait into stages: waiting for the next new face.",
             "the expected number of rolls.", f"when $i$ faces are already seen, a new face appears with probability $\\frac{{{n} - i}}{{{n}}}$, so that stage takes $\\frac{{{n}}}{{{n} - i}}$ rolls on average.",
             [" + ".join(f"\\frac{{{n}}}{{{n - i}}}" for i in range(n)).join(["$", f" = {ft(ans)}$."])], "assuming it takes " + str(n) + " rolls.")


@reg(S, "challenge")
def evc_heads_in_row(r):
    k = r.randint(2, 4)
    ans = 2 ** (k + 1) - 2
    p = f"A fair coin is flipped until ${k}$ heads in a row appear. What is the expected number of flips?"
    return Q(p, ans, [2 ** k, 2 * k, 2 ** (k + 1), ans - 2, 2 ** k + k], "Let $E_j$ be the expected remaining flips when the current streak is $j$.",
             "the expected number of flips.", "a tail resets the streak; set up equations for each streak length.",
             [f"$E_j = 1 + \\frac{{1}}{{2}} E_{{j+1}} + \\frac{{1}}{{2}} E_0$, with $E_{{{k}}} = 0$.", f"Solving gives $E_0 = 2^{{{k + 1}}} - 2 = {ans}$."], "using $2^" + str(k) + "$, the waiting time for a fixed pattern of length " + str(k) + " without overlaps.")


@reg(S, "challenge")
def evc_inversions(r):
    n = r.randint(3, 12)
    ans = F(n * (n - 1), 4)
    p = f"The numbers $1, 2, \\ldots, {n}$ are arranged in random order. An inversion is a pair of positions where the larger number comes first. What is the expected number of inversions?"
    return Q(p, ans, [F(n * (n - 1), 2), F(n, 2), F(n - 1, 2), ans + 1, F(n * n, 4)], "Each pair is inverted half the time.",
             "the expected number.", "linearity over all pairs.",
             [f"Pairs: $\\binom{{{n}}}{{2}} = {comb(n, 2)}$.", f"Half are inverted on average: ${ft(ans)}$."], "counting all pairs.")


@reg(S, "challenge")
def evc_walk_time(r):
    N = r.randint(4, 12)
    a = r.randint(1, N - 1)
    ans = a * (N - a)
    nm = r.choice(NAMES)
    p = f"{nm} starts at $\\${a}$ and bets $\\$1$ on each fair coin flip, stopping at $\\$0$ or $\\${N}$. What is the expected number of flips?"
    return Q(p, ans, [N, a * N, (N - a) ** 2, ans + 1, a + N], "If $E_x$ is the expected flips from $x$: $E_x = 1 + \\frac{1}{2}E_{x-1} + \\frac{1}{2}E_{x+1}$.",
             "the expected number of flips.", "solve the recurrence with $E_0 = E_{" + str(N) + "} = 0$; the solution is $E_x = x(" + str(N) + " - x)$.",
             [f"$E_{{{a}}} = {a} \\cdot {N - a} = {ans}$."], "using the probability of winning instead of the time.")


@reg(S, "challenge")
def evc_peaks(r):
    n = r.randint(3, 12)
    ans = 1 + F(n - 2, 3)
    p = f"The numbers $1, 2, \\ldots, {n}$ are arranged in a random row. A number is a peak if it is larger than each of its neighbors (an end number has one neighbor). What is the expected number of peaks?"
    return Q(p, ans, [F(n, 3), F(n - 2, 3), F(n, 2), ans + F(1, 3), 1 + F(n - 2, 2)], "Ends and middle positions have different chances.",
             "the expected number.", "an end is a peak with probability $\\frac{1}{2}$; a middle position with probability $\\frac{1}{3}$ (it must be the largest of 3).",
             [f"$2 \\cdot \\frac{{1}}{{2}} + {n - 2} \\cdot \\frac{{1}}{{3}} = {ft(ans)}$."], "treating the ends like middle positions.")


@reg(S, "challenge")
def evc_until_special(r):
    n = r.choice([10, 12, 20, 24, 52])
    a = r.choice([1, 2, 3, 4])
    ans = F(n + 1, a + 1)
    p = f"A deck of ${n}$ cards contains ${a}$ special card{'s' if a > 1 else ''}. Cards are turned over one at a time. What is the expected number of cards turned over, up to and including the first special card?"
    return Q(p, ans, [F(n, a), F(n, a + 1), F(n + 1, a), ans + 1, F(n, 2)], "The special cards split the others into equal gaps on average.",
             "the expected position.", f"the ${n - a}$ ordinary cards are spread evenly over ${a + 1}$ gaps, so ${ft(F(n - a, a + 1))}$ come before the first special card on average.",
             [f"$1 + \\frac{{{n - a}}}{{{a + 1}}} = {ft(ans)}$."], f"using $\\frac{{{n}}}{{{a}}}$.")


@reg(S, "challenge")
def evc_reroll(r):
    n = r.choice([4, 6, 8, 10])
    k = r.randint(1, 2)
    E = F(n + 1, 2)
    hist = [E]
    for _ in range(k):
        E = sum(max(F(x), E) for x in range(1, n + 1)) / n
        hist.append(E)
    ans = E
    p = f"In a game you roll a fair ${n}$-sided die. After seeing the result you may reroll up to ${k}$ time{'s' if k > 1 else ''}, keeping only the final roll. With the best strategy, what is your expected final roll?"
    return Q(p, ans, [F(n + 1, 2), hist[-2] if len(hist) > 1 and hist[-2] != ans else ans - F(1, 2), F(n, 1), ans + F(1, 4), F(3 * n, 4)], "Work backwards: reroll whenever the roll is below the value of rerolling.",
             "the expected value.", "with no rerolls left the value is $\\frac{" + str(n + 1) + "}{2}$; with one left, keep any roll above that value.",
             [f"No rerolls left: ${ft(hist[0])}$."] + [f"With {j} reroll{'s' if j > 1 else ''} left: keep rolls above ${ft(hist[j - 1])}$, giving ${ft(hist[j])}$." for j in range(1, k + 1)], "always rerolling, or never rerolling.")


# ================================================================ cp_geometric
S = "cp_geometric"


@reg(S, "basics")
def gp_ring(r):
    a = r.randint(1, 6)
    b = a + r.randint(1, 6)
    ans = F(b * b - a * a, b * b)
    p = f"A dart lands at a random point on a circular target of radius ${b}$. What is the probability it lands outside the bullseye, a circle of radius ${a}$ with the same center?"
    return Q(p, ans, [F(b - a, b), F(a * a, b * b), F(a, b), ans + F(1, b * b), F((b - a) ** 2, b * b)], "Compare areas, not radii.",
             "the probability.", "the ring area over the whole area.",
             [f"Whole: ${b * b}\\pi$. Bullseye: ${a * a}\\pi$.", f"$\\frac{{{b * b - a * a}}}{{{b * b}}} = {ft(ans)}$."], "using the ratio of radii.")


@reg(S, "basics")
def gp_square_in_circle(r):
    R = r.randint(1, 10)
    ans = C("\\frac{2}{\\pi}", 2 / math.pi)
    p = f"A point is chosen at random inside a circle of radius ${R}$. What is the probability it lies inside the square inscribed in the circle?"
    return Q(p, ans, [C("\\frac{1}{\\pi}", 1 / math.pi), C("\\frac{\\pi}{4}", math.pi / 4), C("\\frac{1}{2}", 0.5), C("\\frac{4}{\\pi}", 4 / math.pi) if False else C("\\frac{\\sqrt{2}}{\\pi}", math.sqrt(2) / math.pi), C("\\frac{2}{3}", 2 / 3)], "The square's diagonal is a diameter.",
             "the probability.", "square area over circle area.",
             [f"Diagonal $= {2 * R}$, so the square's area is $\\frac{{{2 * R}^2}}{{2}} = {2 * R * R}$.", f"Circle: ${R * R}\\pi$.", f"$\\frac{{{2 * R * R}}}{{{R * R}\\pi}} = \\frac{{2}}{{\\pi}}$."], "using the diameter as the square's side.")


@reg(S, "basics")
def gp_near_center(r):
    s = r.choice([4, 6, 8, 10, 12])
    rr = r.randint(1, s // 2)
    ans = PI(F(rr * rr, s * s))
    p = f"A point is chosen at random inside a square of side ${s}$. What is the probability it is within ${rr}$ of the square's center?"
    return Q(p, ans, [PI(F(rr, s * s)), PI(F(rr * rr, s)), C(ft(F(rr * rr, s * s)), rr * rr / (s * s)), PI(F(4 * rr * rr, s * s)), PI(F(rr * rr, 2 * s * s))], "The good region is a circle.",
             "the probability.", "circle area over square area.",
             [f"Circle: $\\pi \\cdot {rr}^2 = {rr * rr}\\pi$.", f"Square: ${s * s}$.", f"${pfrac(F(rr * rr, s * s))}$."], "forgetting the $\\pi$.")


@reg(S, "basics")
def gp_square_lt(r):
    k = r.randint(2, 9)
    c = F(r.randint(1, k - 1), k) ** 2
    ans = F(c.numerator ** 0.5 if False else math.isqrt(c.numerator), math.isqrt(c.denominator))
    p = f"A real number $x$ is chosen at random from $0$ to $1$. What is the probability that $x^2 < {ft(c)}$?"
    return Q(p, ans, [c, 1 - ans, ans * ans * ans if ans ** 3 != c else ans / 2, F(1, 2), 1 - c], "Solve for $x$.",
             "the probability.", f"$x^2 < {ft(c)}$ means $x < {ft(ans)}$.",
             [f"Interval length: ${ft(ans)}$ out of $1$."], f"answering ${ft(c)}$.")


@reg(S, "basics")
def gp_minute_hand(r):
    a = r.randint(1, 11)
    b = r.randint(a + 1, 12)
    ans = F(b - a, 12)
    p = f"You glance at a clock at a random moment. What is the probability the minute hand is between the ${a}$ and the ${b if b < 12 else 12}$?"
    return Q(p, ans, [F(b - a, 60), F(b - a, 24), F(b - a + 1, 12), F(1, b - a), F(b - a, 11)], "The minute hand sweeps the 12 marks evenly.",
             "the probability.", "fraction of the dial.",
             [f"The arc from ${a}$ to ${b}$ covers ${b - a}$ of the $12$ spaces.", f"${ft(ans)}$."], "dividing by 60.")


@reg(S, "basics")
def gp_real_roots(r):
    c = r.randint(1, 9) ** 2
    Bm = 2 * math.isqrt(c) + r.randint(1, 10)
    ans = F(Bm - 2 * math.isqrt(c), Bm)
    p = f"A number $b$ is chosen at random from $0$ to ${Bm}$. What is the probability that $x^2 + bx + {c}$ has real roots?"
    return Q(p, ans, [F(Bm - math.isqrt(c), Bm), F(Bm - 4 * c, Bm) if Bm > 4 * c else F(1, 2), F(2 * math.isqrt(c), Bm), 1 - ans if 1 - ans != ans else ans + F(1, Bm), F(Bm - c, Bm) if Bm > c else ans + F(1, Bm)], "Discriminant.",
             "the probability.", f"real roots need $b^2 - {4 * c} \\ge 0$, so $b \\ge {2 * math.isqrt(c)}$.",
             [f"Good interval: ${2 * math.isqrt(c)}$ to ${Bm}$, length ${Bm - 2 * math.isqrt(c)}$.", f"${ft(ans)}$."], "forgetting the factor of 4 in the discriminant.")


@reg(S, "basics")
def gp_inner_cube(r):
    s = r.randint(3, 10)
    t = r.randint(1, s - 1)
    ans = F(t ** 3, s ** 3)
    p = f"A point is chosen at random inside a cube of edge ${s}$. A smaller cube of edge ${t}$ sits inside it. What is the probability the point lies in the smaller cube?"
    return Q(p, ans, [F(t, s), F(t * t, s * s), F(t ** 3, s ** 2) if t ** 3 < s ** 2 else F(t, 2 * s), ans * 2, F(t ** 3 + 1, s ** 3)], "Compare volumes.",
             "the probability.", "volume ratio.",
             [f"$\\frac{{{t}^3}}{{{s}^3}} = {ft(ans)}$."], "comparing edges or faces.")


@reg(S, "basics")
def gp_sector(r):
    ang = r.choice([30, 40, 45, 60, 72, 80, 90, 120, 135, 150])
    ans = F(ang, 360)
    p = f"A spinner is a circle with a shaded sector of central angle ${ang}^\\circ$. The pointer stops at a random angle. What is the probability it stops in the shaded sector?"
    return Q(p, ans, [F(ang, 180), F(ang, 100), 1 - ans, F(ang, 300), ans * 2 if ans * 2 < 1 else ans / 2], "Fraction of the full turn.",
             "the probability.", "the angle over $360^\\circ$.",
             [f"$\\frac{{{ang}}}{{360}} = {ft(ans)}$."], "dividing by 180.")


@reg(S, "basics")
def gp_break_ratio(r):
    k = r.randint(2, 6)
    ans = F(2, k + 1)
    L = r.randint(6, 30)
    p = f"A stick of length ${L}$ is cut at a random point. What is the probability the longer piece is at least ${k}$ times as long as the shorter piece?"
    return Q(p, ans, [F(1, k + 1), F(1, k), F(2, k), F(k - 1, k + 1), F(1, 2)], "Where can the cut go?",
             "the probability.", f"the shorter piece must be at most $\\frac{{1}}{{{k + 1}}}$ of the stick, at either end.",
             [f"Good cuts: within $\\frac{{{L}}}{{{k + 1}}}$ of either end, total $\\frac{{{2 * L}}}{{{k + 1}}}$.", f"Divide by ${L}$: ${ft(ans)}$."], "counting only one end.")


@reg(S, "basics")
def gp_triangle_incircle(r):
    s = r.randint(2, 12)
    ans = PIR3(F(1, 9))
    p = f"A point is chosen at random inside an equilateral triangle with side ${s}$. What is the probability it lies inside the triangle's inscribed circle?"
    return Q(p, ans, [PIR3(F(1, 6)), PI(F(1, 3)), PI(F(1, 4)), PIR3(F(2, 9)), PIR3(F(1, 12))], "Inradius of an equilateral triangle: $\\frac{s\\sqrt{3}}{6}$.",
             "the probability.", "circle area over triangle area; the side cancels.",
             [f"$r = \\frac{{{s}\\sqrt{{3}}}}{{6}}$, so circle area $= \\pi \\cdot \\frac{{{3 * s * s}}}{{36}} = {pfrac(F(s * s, 12))}$.", f"Triangle area: $\\frac{{\\sqrt{{3}}}}{{4}} \\cdot {s * s}$.",
              "Ratio: $\\frac{\\pi/12}{\\sqrt{3}/4} = \\frac{\\pi}{3\\sqrt{3}} = \\frac{\\pi\\sqrt{3}}{9}$."], "using the circumradius.")


@reg(S, "basics")
def gp_semicircle(r):
    s = r.randint(2, 12)
    ans = PI(F(1, 8))
    p = f"A semicircle is drawn inside a square of side ${s}$, with one side of the square as its diameter. A point is chosen at random in the square. What is the probability it is inside the semicircle?"
    return Q(p, ans, [PI(F(1, 4)), PI(F(1, 2)), PI(F(1, 16)), C("\\frac{1}{2}", 0.5), C("\\frac{1}{8}", 0.125)], "The radius is half the side.",
             "the probability.", "semicircle area over square area.",
             [f"Radius ${ft(F(s, 2))}$: semicircle area $\\frac{{1}}{{2}} \\pi \\left({ft(F(s, 2))}\\right)^2 = {pfrac(F(s * s, 8))}$.", f"Divide by ${s * s}$: $\\frac{{\\pi}}{{8}}$."], "using a full circle.")


@reg(S, "basics")
def gp_coin_tile(r):
    s = r.randint(4, 12)
    d = r.randint(1, s - 1)
    ans = F((s - d) ** 2, s * s)
    p = f"A floor is covered with square tiles of side ${s}$ cm. A coin of diameter ${d}$ cm is tossed onto the floor at random. What is the probability it lands entirely within one tile?"
    return Q(p, ans, [F(s - d, s), F((s - 2 * d) ** 2, s * s) if s > 2 * d else F(1, s), F(d * d, s * s), 1 - ans, F((s - d) ** 2, (s + d) ** 2)], "Track the coin's center.",
             "the probability.", f"the center must be at least ${ft(F(d, 2))}$ from every edge of its tile: a smaller square of side ${s} - {d}$.",
             [f"$\\frac{{{s - d}^2}}{{{s}^2}} = {ft(ans)}$."], "subtracting only the radius once instead of twice.")


@reg(S, "basics")
def gp_hexagon_circle(r):
    s = r.randint(2, 10)
    ans = PIR3(F(1, 6))
    p = f"A point is chosen at random inside a regular hexagon of side ${s}$. What is the probability it lies inside the circle inscribed in the hexagon?"
    return Q(p, ans, [PIR3(F(1, 9)), PI(F(1, 2)), PIR3(F(1, 3)), PI(F(2, 3)), PIR3(F(1, 4))], "The inradius is the height of one of the six equilateral triangles.",
             "the probability.", "circle area over hexagon area.",
             [f"Inradius: $\\frac{{{s}\\sqrt{{3}}}}{{2}}$, so circle area $= {pfrac(F(3 * s * s, 4))}$.", f"Hexagon: $\\frac{{3\\sqrt{{3}}}}{{2}} \\cdot {s * s}$.", "Ratio: $\\frac{3/4 \\, \\pi}{3\\sqrt{3}/2} = \\frac{\\pi}{2\\sqrt{3}} = \\frac{\\pi\\sqrt{3}}{6}$."], "using the side as the radius.")


@reg(S, "basics")
def gp_top_triangle(r):
    a, b = r.randint(1, 5), r.randint(2, 7)
    if a >= b:
        return None
    k = F(a, b)
    ans = k * k
    p = f"A line parallel to the base of a triangle cuts the height so the piece next to the top vertex has ${ft(k)}$ of the height. A point is chosen at random in the triangle. What is the probability it lies in the small triangle at the top?"
    return Q(p, ans, [k, 1 - k * k, k / 2, 1 - k, k * k * k], "Similar triangles: areas scale by the square.",
             "the probability.", f"the top triangle is similar with ratio ${ft(k)}$, so its area is ${ft(k)}^2$ of the whole.",
             [f"$\\left({ft(k)}\\right)^2 = {ft(ans)}$."], "using the height ratio directly.")


@reg(S, "basics")
def gp_closest_bottom(r):
    w = r.randint(3, 12)
    h = r.randint(2, w)
    ans = F(2 * w - h, 4 * w)
    p = f"A point is chosen at random inside a ${w} \\times {h}$ rectangle (width ${w}$, height ${h}$). What is the probability it is closer to the bottom side than to any of the other three sides?"
    return Q(p, ans, [F(1, 4), F(1, 2), F(h, 4 * w), F(w, 2 * (w + h)), ans + F(1, 4 * w)], "The region is bounded by angle bisectors from the bottom corners.",
             "the probability.", "points closer to the bottom than the left and right sides lie between the $45^\\circ$ lines from the bottom corners, and below the middle line.",
             [f"Region: a trapezoid of height $\\frac{{{h}}}{{2}}$ with bases ${w}$ and ${w - h}$.", f"Area: $\\frac{{{h}}}{{2}} \\cdot \\frac{{{w} + {w - h}}}{{2}} = {ft(F(h * (2 * w - h), 4))}$.", f"Divide by ${w * h}$: ${ft(ans)}$."], "assuming each side gets a quarter.")


@reg(S, "basics")
def gp_two_intervals(r):
    a = r.randint(4, 20)
    lo = r.randint(0, a - 3)
    hi = r.randint(lo + 1, a - 1)
    lo2 = r.randint(hi, a - 1)
    hi2 = r.randint(lo2 + 1, a)
    ans = F(hi - lo + hi2 - lo2, a)
    p = f"A number is chosen at random from $0$ to ${a}$. What is the probability it lies between ${lo}$ and ${hi}$ or between ${lo2}$ and ${hi2}$?"
    return Q(p, ans, [F(hi - lo, a), F(hi2 - lo, a) if hi2 - lo != hi - lo + hi2 - lo2 else F(1, 2), F(hi - lo + hi2 - lo2, a + 1), ans / 2, 1 - ans if 1 - ans != ans else ans + F(1, a)], "Add the lengths of the pieces.",
             "the probability.", "total good length over total length.",
             [f"Lengths: ${hi - lo}$ and ${hi2 - lo2}$.", f"$\\frac{{{hi - lo + hi2 - lo2}}}{{{a}}} = {ft(ans)}$."], "including the gap between the pieces.") if hi < lo2 else None


@reg(S, "challenge")
def gpc_three_pieces(r):
    L = r.randint(9, 30)
    m = r.randint(1, (L - 1) // 3)
    ans = F(L - 3 * m, L) ** 2
    p = f"A stick of length ${L}$ is broken at two random points (chosen independently). What is the probability all three pieces have length at least ${m}$?"
    return Q(p, ans, [F(L - 3 * m, L), F(L - 2 * m, L) ** 2, F(L - 3 * m, L) ** 3, ans / 2, F(1, 4)], "Shrink each piece by " + str(m) + ".",
             "the probability.", f"set each piece to ${m}$ + extra; the extras share ${L - 3 * m}$, and the good region is a scaled copy of the whole.",
             [f"Breaking points $(x, y)$ fill a ${L} \\times {L}$ square. The good region is two triangles scaled by $\\frac{{{L - 3 * m}}}{{{L}}}$.", f"Probability: $\\left(\\frac{{{L - 3 * m}}}{{{L}}}\\right)^2 = {ft(ans)}$."], "using the ratio without squaring.")


@reg(S, "challenge")
def gpc_three_sum(r):
    k = F(r.randint(1, 4), r.randint(4, 6))
    if k > 1:
        return None
    ans = k ** 3 / 6
    p = f"Three numbers $x, y, z$ are each chosen at random from $0$ to $1$. What is the probability that $x + y + z < {ft(k)}$?"
    return Q(p, ans, [k ** 3, k ** 3 / 3, k ** 2 / 2, k / 3, k ** 3 / 2], "The region is a corner pyramid of the unit cube.",
             "the probability.", "the region $x + y + z < k$ is a tetrahedron with three perpendicular edges of length $k$.",
             [f"Volume: $\\frac{{1}}{{6}} \\cdot \\left({ft(k)}\\right)^3 = {ft(ans)}$.", "The cube has volume $1$."], "forgetting the $\\frac{1}{6}$.")


@reg(S, "challenge")
def gpc_obtuse(r):
    a = r.randint(2, 8)
    b = r.randint((a + 1) // 2 + 1, 12)
    ans = PI(F(a, 8 * b))
    p = f"Rectangle $ABCD$ has $AB = {a}$ and $BC = {b}$. A point $P$ is chosen at random inside it. What is the probability that $\\angle APB$ is obtuse?"
    return Q(p, ans, [PI(F(a, 4 * b)), PI(F(a, 2 * b)), PI(F(a * a, 8 * b * b)), C("\\frac{1}{2}", 0.5), PI(F(b, 8 * a))], "Thales: $\\angle APB = 90^\\circ$ on the circle with diameter $AB$.",
             "the probability.", "$\\angle APB$ is obtuse exactly when $P$ is inside the semicircle on $AB$.",
             [f"Semicircle radius ${ft(F(a, 2))}$: area $\\frac{{\\pi}}{{2}} \\cdot {ft(F(a * a, 4))} = {pfrac(F(a * a, 8))}$.", f"Rectangle: ${a * b}$.", f"${pfrac(F(a, 8 * b))}$."], "using a full circle.")


@reg(S, "challenge")
def gpc_chord_midpoint(r):
    R = r.randint(3, 12)
    Lc = r.randint(1, 2 * R - 1)
    ans = F(4 * R * R - Lc * Lc, 4 * R * R)
    p = f"A point $M$ is chosen at random inside a circle of radius ${R}$, and the chord with midpoint $M$ is drawn. What is the probability the chord is longer than ${Lc}$?"
    return Q(p, ans, [F(2 * R - Lc, 2 * R), F(Lc * Lc, 4 * R * R), 1 - F(Lc, 2 * R), ans + F(1, 4 * R * R), F(R - Lc // 2, R) if R - Lc // 2 > 0 else F(1, 2)], "A chord's length depends only on its distance from the center.",
             "the probability.", "a chord with midpoint at distance $d$ from the center has half-length $\\sqrt{R^2 - d^2}$.",
             [f"Longer than ${Lc}$: $R^2 - d^2 > {ft(F(Lc * Lc, 4))}$, so $d^2 < {ft(F(4 * R * R - Lc * Lc, 4))}$.", f"Area ratio: $\\frac{{d^2}}{{R^2}} = {ft(ans)}$."], "using lengths instead of areas.")


@reg(S, "challenge")
def gpc_cube_ball(r):
    s = r.randint(2, 8)
    rr = r.randint(1, s)
    ans = PI(F(rr ** 3, 6 * s ** 3))
    p = f"A point is chosen at random inside a cube of edge ${s}$. What is the probability it is within distance ${rr}$ of a particular vertex?"
    return Q(p, ans, [PI(F(4 * rr ** 3, 3 * s ** 3)), PI(F(rr ** 3, 3 * s ** 3)), PI(F(rr ** 2, 4 * s ** 2)), PI(F(rr ** 3, 8 * s ** 3)), C(ft(F(rr ** 3, 6 * s ** 3)), rr ** 3 / (6 * s ** 3))], "Only an eighth of the ball is inside the cube.",
             "the probability.", "the region is one eighth of a ball of radius " + str(rr) + ".",
             [f"$\\frac{{1}}{{8}} \\cdot \\frac{{4}}{{3}}\\pi \\cdot {rr ** 3} = {pfrac(F(rr ** 3, 6))}$.", f"Divide by ${s ** 3}$: ${pfrac(F(rr ** 3, 6 * s ** 3))}$."], "using the whole ball.")


@reg(S, "challenge")
def gpc_small_area(r):
    k = F(r.randint(1, 3), r.randint(4, 6))
    ans = 1 - (1 - k) ** 2
    p = f"A point $P$ is chosen at random inside triangle $ABC$. What is the probability that the area of triangle $PBC$ is less than ${ft(k)}$ of the area of $ABC$?"
    return Q(p, ans, [k, k * k, (1 - k) ** 2, 2 * k, 1 - k], "Area of $PBC$ depends only on $P$'s height above $BC$.",
             "the probability.", f"$[PBC] < {ft(k)}[ABC]$ means $P$ is within ${ft(k)}$ of the height from $BC$; the rest is a similar triangle at $A$ with ratio ${ft(1 - k)}$.",
             [f"Top triangle: $\\left({ft(1 - k)}\\right)^2 = {ft((1 - k) ** 2)}$ of the area.", f"Probability: $1 - {ft((1 - k) ** 2)} = {ft(ans)}$."], "answering " + ft(k) + ".")


@reg(S, "challenge")
def gpc_chord_short(r):
    m = r.choice([("R", 60, "", "R"), ("R\\sqrt{2}", 90, "", "R\\sqrt{2}"), ("R\\sqrt{3}", 120, "", "R\\sqrt{3}")])
    ans = F(m[1] * 2, 360)
    p = f"Two points are chosen at random on a circle of radius $R$. What is the probability the distance between them is less than ${m[0]}$?"
    return Q(p, ans, [F(m[1], 360), 1 - ans, F(1, 2) if ans != F(1, 2) else F(1, 4), F(m[1], 180) / 2 + F(1, 12), F(m[1] * 2, 360) + F(1, 6)], "Fix the first point; the chord length depends on the central angle.",
             "the probability.", f"a chord of length ${m[0]}$ subtends a central angle of ${m[1]}^\\circ$.",
             [f"The second point must be within ${m[1]}^\\circ$ of the first on either side: ${2 * m[1]}^\\circ$ out of $360^\\circ$.", f"${ft(ans)}$."], "counting only one side.")
