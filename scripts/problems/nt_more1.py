"""Extra Number Theory problem types (part 1): divisors, gcd and lcm, divisibility, modular arithmetic."""
import math
from fractions import Fraction as F

from common import NAMES, C, Q, num, par, sg

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def factorint(n):
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def ftex_fact(n):
    return " \\cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in sorted(factorint(n).items()))


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def ndiv(n):
    out = 1
    for e in factorint(n).values():
        out *= e + 1
    return out


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


def smooth(r, primes=(2, 3, 5, 7), lo=30, hi=3000):
    while True:
        n = 1
        for p in primes:
            n *= p ** r.randint(0, 4)
        if lo <= n <= hi:
            return n


# ================================================================ nt_divisors
S = "nt_divisors"


@reg(S, "basics")
def dv_odd_count(r):
    n = smooth(r, (2, 3, 5, 7), 60, 5000)
    m = n
    while m % 2 == 0:
        m //= 2
    if m == n:
        return None
    ans = ndiv(m)
    p = f"How many odd positive divisors does ${n}$ have?"
    return Q(p, ans, [ndiv(n), ndiv(n) - ans, ans + 1, ans * 2, len(factorint(n))], "Odd divisors can't use any factor of $2$.",
             "the count of odd divisors.", "an odd divisor uses only the odd primes, so ignore the power of $2$.",
             [f"${n} = {ftex_fact(n)}$.", f"Odd part: ${m} = {ftex_fact(m) if m > 1 else '1'}$.", f"Divisors of the odd part: " + (" \\cdot ".join(f"({e} + 1)" for p, e in sorted(factorint(m).items())) if m > 1 else "1") + f" $= {ans}$."],
             "counting all divisors.")


@reg(S, "basics")
def dv_square_divisors(r):
    n = smooth(r, (2, 3, 5), 100, 20000)
    fs = factorint(n)
    ans = 1
    for e in fs.values():
        ans *= e // 2 + 1
    p = f"How many positive divisors of ${n}$ are perfect squares?"
    return Q(p, ans, [ndiv(n), ans + 1, ans * 2, math.isqrt(n) // 10 or 3, len(fs)], "A square divisor uses only even exponents.",
             "the number of square divisors.", "a divisor is a square exactly when every prime appears to an even power.",
             [f"${n} = {ftex_fact(n)}$.", "Even exponent choices: " + ", ".join(f"for ${p}$: ${e // 2 + 1}$ (0" + "".join(f", {k}" for k in range(2, e + 1, 2)) + ")" for p, e in sorted(fs.items())) + ".", f"Product: ${ans}$."],
             "counting all divisors.")


@reg(S, "basics")
def dv_smallest_prime(r):
    p1 = r.choice([7, 11, 13, 17, 19, 23, 29, 31])
    p2 = r.choice([x for x in [13, 17, 19, 23, 29, 31, 37, 41, 43] if x > p1])
    n = p1 * p2
    p = f"What is the smallest prime factor of ${n}$?"
    return Q(p, p1, [p2, 3, p1 + 2 if is_prime(p1 + 2) else p1 + 4, n, 2], "Test small primes in order.",
             "the smallest prime divisor.", "check divisibility by $2, 3, 5, 7, \\ldots$ until one works.",
             [f"${n}$ is odd, not divisible by $3$ (digit sum ${sum(map(int, str(n)))}$), and doesn't end in $0$ or $5$.", f"${n} = {p1} \\cdot {p2}$."],
             "answering the larger factor.")


@reg(S, "basics")
def dv_exponent_sum(r):
    n = smooth(r, (2, 3, 5, 7), 100, 10000)
    ans = sum(factorint(n).values())
    p = f"When ${n}$ is written as a product of primes, how many primes are used, counting repeats?"
    return Q(p, ans, [len(factorint(n)), ans + 1, ndiv(n), ans - 1, ans * 2], "Write the prime factorization.",
             "the total number of prime factors with repetition.", "factor completely, then add the exponents.",
             [f"${n} = {ftex_fact(n)}$.", f"Exponent sum: ${' + '.join(str(e) for e in factorint(n).values())} = {ans}$."], "counting only the distinct primes.")


@reg(S, "basics")
def dv_divisible_by_k(r):
    n = smooth(r, (2, 3, 5), 60, 5000)
    ks = [k for k in (2, 3, 4, 5, 6, 10, 12, 15) if n % k == 0 and k < n]
    if not ks:
        return None
    k = r.choice(ks)
    ans = ndiv(n // k)
    p = f"How many positive divisors of ${n}$ are multiples of ${k}$?"
    return Q(p, ans, [ndiv(n), ndiv(n) - ans, ans + 1, n // k, ndiv(k)], "Divisors that are multiples of $k$ look like $k$ times a divisor of $\\frac{n}{k}$.",
             "the count.", f"$d$ is a multiple of ${k}$ dividing ${n}$ exactly when $\\frac{{d}}{{{k}}}$ divides $\\frac{{{n}}}{{{k}}} = {n // k}$.",
             [f"$\\frac{{{n}}}{{{k}}} = {n // k} = {ftex_fact(n // k) if n // k > 1 else '1'}$.", f"Its divisors: ${ans}$."], "counting all divisors of " + str(n) + ".")


@reg(S, "basics")
def dv_prime_sum(r):
    n = smooth(r, (2, 3, 5, 7, 11, 13), 100, 30000)
    ans = sum(factorint(n))
    p = f"What is the sum of the different prime factors of ${n}$?"
    return Q(p, ans, [sum(p_ * e for p_, e in factorint(n).items()), ans + 2, max(factorint(n)), ans - 2 if ans > 2 else ans + 3, len(factorint(n))], "Factor completely.",
             "the sum of the distinct primes.", "list each prime once, no matter its exponent.",
             [f"${n} = {ftex_fact(n)}$.", f"Distinct primes: ${' + '.join(map(str, sorted(factorint(n))))} = {ans}$."], "adding a prime once for each time it appears.")


@reg(S, "basics")
def dv_square_count(r):
    n = smooth(r, (2, 3, 5, 7), 6, 300)
    ans = ndiv(n * n)
    p = f"How many positive divisors does ${n}^2 = {n * n}$ have?"
    return Q(p, ans, [ndiv(n) ** 2, 2 * ndiv(n), ndiv(n), ans + 1, ans - 1], "Square the factorization.",
             "the divisor count of $n^2$.", "squaring doubles every exponent; then multiply (exponent $+ 1$).",
             [f"${n} = {ftex_fact(n)}$, so ${n}^2 = {ftex_fact(n * n)}$.", f"Divisors: " + " \\cdot ".join(f"({2 * e} + 1)" for e in factorint(n).values()) .join(["$", f" = {ans}$."])],
             "squaring the divisor count of " + str(n) + ".")


@reg(S, "basics")
def dv_proper_sum(r):
    n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 48, 56, 60, 66, 70, 72, 84, 88, 90, 96, 100])
    s = sum(divisors(n)) - n
    p = f"What is the sum of the proper divisors of ${n}$ (all positive divisors except ${n}$ itself)?"
    return Q(p, s, [s + n, s - 1, n, ndiv(n), s + 1], "List the divisors in pairs.",
             "the sum of the proper divisors.", "pair each divisor $d$ with $\\frac{n}{d}$ to list them all quickly.",
             [f"Divisors: ${', '.join(map(str, divisors(n)))}$.", f"Sum without ${n}$: ${s}$."], "including " + str(n) + " itself.")


@reg(S, "basics")
def dv_three_divisors(r):
    N = r.randint(30, 500)
    ps = [p for p in range(2, math.isqrt(N) + 1) if is_prime(p)]
    ans = len(ps)
    p = f"How many positive integers at most ${N}$ have exactly three positive divisors?"
    return Q(p, ans, [ans + 1, ans - 1 if ans > 1 else ans + 2, math.isqrt(N), len([q for q in range(2, N + 1) if is_prime(q)]) // 5 or 2, ans * 2], "What does a number with exactly 3 divisors look like?",
             "the count.", "a number has exactly three divisors exactly when it is the square of a prime: $1$, $p$, $p^2$.",
             [f"Need $p^2 \\le {N}$, so $p \\le {math.isqrt(N)}$.", f"Primes up to ${math.isqrt(N)}$: ${', '.join(map(str, ps))}$. That's ${ans}$."], "counting all perfect squares.")


@reg(S, "basics")
def dv_below_root(r):
    n = smooth(r, (2, 3, 5, 7), 50, 3000)
    if math.isqrt(n) ** 2 == n:
        return None
    ans = ndiv(n) // 2
    p = f"How many positive divisors of ${n}$ are less than $\\sqrt{{{n}}}$?"
    return Q(p, ans, [ndiv(n), ans + 1, ans - 1, math.isqrt(n), ndiv(n) - 1], "Divisors come in pairs $d$ and $\\frac{n}{d}$.",
             "the count of small divisors.", "each pair $(d, \\frac{n}{d})$ has exactly one member below $\\sqrt{n}$ (since $n$ isn't a square).",
             [f"${n} = {ftex_fact(n)}$ has ${ndiv(n)}$ divisors.", f"Half are below $\\sqrt{{{n}}}$: ${ans}$."], "counting the square root itself, which isn't a whole number here.")


@reg(S, "basics")
def dv_product_pairs(r):
    n = smooth(r, (2, 3, 5), 20, 2000)
    d = ndiv(n)
    ans = (d + 1) // 2
    p = f"In how many ways can ${n}$ be written as $a \\times b$ with positive integers $a \\le b$?"
    return Q(p, ans, [d, ans + 1, d // 2 if d // 2 != ans else ans - 1, d - 1, 2 * d], "Each divisor $a \\le \\sqrt{n}$ gives one way.",
             "the number of factor pairs.", "pairs $(a, b)$ correspond to divisors $a$ at most $\\sqrt{n}$.",
             [f"${n}$ has ${d}$ divisors.", ("It's a perfect square, so " if d % 2 else "It's not a square, so ") + f"the number of pairs is $\\lceil \\frac{{{d}}}{{2}} \\rceil = {ans}$."], "counting ordered pairs.")


@reg(S, "basics")
def dv_largest_proper(r):
    n = r.choice([x for x in range(100, 1000) if not is_prime(x)])
    sp = min(factorint(n))
    ans = n // sp
    p = f"What is the largest divisor of ${n}$ that is less than ${n}$?"
    return Q(p, ans, [n - 1, sp, n // max(factorint(n)), ans - 1, F(n, 2) if n % 2 else ans + 1], "Divide by the smallest prime factor.",
             "the largest proper divisor.", "the largest proper divisor is $n$ divided by its smallest prime factor.",
             [f"Smallest prime factor of ${n}$: ${sp}$.", f"${n} \\div {sp} = {ans}$."], "answering $n - 1$.")


@reg(S, "basics")
def dv_radical(r):
    n = smooth(r, (2, 3, 5, 7, 11), 100, 20000)
    ans = math.prod(factorint(n))
    p = f"What is the product of the different prime factors of ${n}$?"
    return Q(p, ans, [n, sum(factorint(n)), ans * 2, max(factorint(n)), ans + 1], "List each prime once.",
             "the product of distinct primes.", "factor, then multiply each prime once.",
             [f"${n} = {ftex_fact(n)}$.", f"Product: ${' \\cdot '.join(map(str, sorted(factorint(n))))} = {ans}$."], "keeping the exponents.")


@reg(S, "basics")
def dv_odd_number_divisors(r):
    N = r.randint(20, 400)
    ans = math.isqrt(N)
    p = f"How many integers from $1$ to ${N}$ have an odd number of positive divisors?"
    return Q(p, ans, [ans + 1, N // 2, ans - 1, N - ans, ans * 2], "Divisors pair up unless one is paired with itself.",
             "the count.", "divisors come in pairs $d, \\frac{n}{d}$; the count is odd only when $d = \\frac{n}{d}$, meaning $n$ is a perfect square.",
             [f"Perfect squares up to ${N}$: $1^2$ through ${ans}^2$.", f"That's ${ans}$."], "counting odd numbers.")


@reg(S, "basics")
def dv_twin(r):
    a = r.randint(1, 80)
    b = a + r.randint(20, 60)
    tw = [p for p in range(a, b - 1) if is_prime(p) and is_prime(p + 2)]
    p = f"Twin primes are pairs of primes that differ by $2$, like $11$ and $13$. How many twin prime pairs have both primes between ${a}$ and ${b}$, inclusive?"
    return Q(p, len(tw), [len(tw) + 1, len([q for q in range(a, b + 1) if is_prime(q)]), len(tw) - 1 if tw else 2, len(tw) * 2, 0 if tw else 3], "List the primes in the range first.",
             "the number of twin prime pairs.", "list the primes, then check which ones are $2$ apart.",
             [f"Primes: ${', '.join(str(q) for q in range(a, b + 1) if is_prime(q))}$.", "Twin pairs: " + (", ".join(f"$({q}, {q + 2})$" for q in tw) if tw else "none") + "."], "counting a prime in two pairs twice, or missing a pair at the edge.")


@reg(S, "basics")
def dv_power_sigma(r):
    pr = r.choice([2, 3])
    k = r.randint(3, 9 if pr == 2 else 6)
    ans = (pr ** (k + 1) - 1) // (pr - 1)
    p = f"What is the sum of all positive divisors of ${pr ** k}$?"
    return Q(p, ans, [pr ** (k + 1), ans - 1, pr ** k, k + 1, ans + pr], "The divisors are powers of " + str(pr) + ".",
             "the divisor sum.", f"the divisors of ${pr}^{{{k}}}$ are $1, {pr}, {pr}^2, \\ldots, {pr}^{{{k}}}$, a geometric series.",
             [f"$1 + {pr} + \\cdots + {pr}^{{{k}}} = \\frac{{{pr}^{{{k + 1}}} - 1}}{{{pr - 1}}} = {ans}$."], "forgetting the divisor $1$.")


@reg(S, "challenge")
def dvc_cube_divisors(r):
    n = smooth(r, (2, 3, 5), 1000, 200000)
    fs = factorint(n)
    ans = math.prod(e // 3 + 1 for e in fs.values())
    p = f"How many positive divisors of ${n}$ are perfect cubes?"
    return Q(p, ans, [math.prod(e // 2 + 1 for e in fs.values()), ans + 1, ndiv(n), ans * 2, len(fs)], "Each exponent must be a multiple of $3$.",
             "the number of cube divisors.", "a divisor is a cube when every exponent is a multiple of $3$.",
             [f"${n} = {ftex_fact(n)}$.", "Choices: " + ", ".join(f"${p_}$: ${e // 3 + 1}$" for p_, e in sorted(fs.items())) + f". Product: ${ans}$."], "using even exponents (that's squares).")


@reg(S, "challenge")
def dvc_odd_sigma(r):
    n = smooth(r, (2, 3, 5, 7), 60, 5000)
    m = n
    while m % 2 == 0:
        m //= 2
    if m == n or m == 1:
        return None
    ans = sum(divisors(m))
    p = f"What is the sum of all odd positive divisors of ${n}$?"
    return Q(p, ans, [sum(divisors(n)), ans + 1, sum(divisors(n)) - ans, m, ans - m], "The odd divisors are the divisors of the odd part.",
             "the sum of odd divisors.", "drop the power of $2$, then use the divisor sum formula $\\prod (1 + p + \\cdots + p^e)$.",
             [f"Odd part: ${m} = {ftex_fact(m)}$.", "Sum: " + " \\cdot ".join(f"({' + '.join(str(p_ ** i) for i in range(e + 1))})" for p_, e in sorted(factorint(m).items())).join(["$", f" = {ans}$."])],
             "adding all divisors.")


@reg(S, "challenge")
def dvc_smallest_odd_k(r):
    k = r.choice([4, 6, 8, 9, 10, 12])
    ans = next(n for n in range(1, 10 ** 6, 2) if ndiv(n) == k)
    p = f"What is the smallest odd positive integer with exactly ${k}$ positive divisors?"
    return Q(p, ans, [next(n for n in range(1, 10 ** 6) if ndiv(n) == k), ans + 2, 3 ** (k - 1) if 3 ** (k - 1) != ans else ans * 3, ans * 3, ans - 2], "Use the smallest odd primes with large exponents on smaller primes.",
             "the smallest odd number with " + str(k) + " divisors.", "write " + str(k) + " as a product of (exponent $+ 1$) factors and assign the biggest exponents to the smallest odd primes.",
             [f"${ans} = {ftex_fact(ans)}$ has " + " \\cdot ".join(f"({e} + 1)" for e in factorint(ans).values()).join(["$", f" = {k}$ divisors."]), "Other ways to make " + str(k) + " divisors with odd primes give larger numbers."],
             "using the prime $2$, which makes the number even.")


@reg(S, "challenge")
def dvc_four_divisors(r):
    N = r.randint(30, 120)
    xs = [n for n in range(1, N + 1) if ndiv(n) == 4]
    p = f"How many integers from $1$ to ${N}$ have exactly four positive divisors?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, len([n for n in range(1, N + 1) if ndiv(n) == 3]) + len(xs), len(xs) + 3, len([n for n in range(1, N + 1) if is_prime(n)])],
             "Four divisors means $p^3$ or $pq$.", "the count.", "$n$ has exactly 4 divisors when $n = p^3$ or $n = pq$ for different primes $p, q$.",
             [f"Cubes of primes up to ${N}$: " + ", ".join(str(p_ ** 3) for p_ in range(2, 10) if is_prime(p_) and p_ ** 3 <= N) + ".", f"Products of two different primes up to ${N}$, listed and counted with the cubes: ${len(xs)}$ in total."],
             "forgetting the prime cubes like $8$ and $27$.")


@reg(S, "challenge")
def dvc_double_divisors(r):
    a = r.randint(1, 4)
    dm = r.choice([2, 3, 4, 6])
    dn, d2n, d4n = (a + 1) * dm, (a + 2) * dm, (a + 3) * dm
    p = f"A positive integer $n$ has ${dn}$ positive divisors and $2n$ has ${d2n}$. How many positive divisors does $4n$ have?"
    return Q(p, d4n, [2 * d2n - dn + dm if 2 * d2n - dn + dm != d4n else d4n + 2, 2 * dn, d2n + dm + 1, d4n - dm, d2n * 2], "Write $n = 2^a \\cdot m$ with $m$ odd.",
             "the divisor count of $4n$.", "doubling raises the exponent of $2$ by one; the odd part's divisor count stays the same.",
             [f"$(a + 1)d(m) = {dn}$ and $(a + 2)d(m) = {d2n}$.", f"Subtracting: $d(m) = {dm}$, so $a + 1 = {a + 1}$.", f"$4n$ has $(a + 3)d(m) = {a + 3} \\cdot {dm} = {d4n}$ divisors."],
             "assuming the divisor count goes up by the same amount every time without finding $d(m)$.")


@reg(S, "challenge")
def dvc_reciprocal_sum(r):
    n = r.choice([6, 12, 18, 20, 24, 28, 30, 36, 40, 48, 60])
    ans = F(sum(divisors(n)), n)
    p = f"What is the sum of the reciprocals of all positive divisors of ${n}$?"
    return Q(p, ans, [F(ndiv(n), n), ans + 1, F(n, sum(divisors(n))), F(sum(divisors(n)), ndiv(n)), F(sum(divisors(n)) - n, n)], "Pair $\\frac{1}{d}$ with $\\frac{d'}{n}$ where $d' = \\frac{n}{d}$.",
             "$\\sum \\frac{1}{d}$.", "$\\frac{1}{d} = \\frac{n/d}{n}$, and as $d$ runs over divisors so does $\\frac{n}{d}$; so the sum is $\\frac{\\sigma(n)}{n}$.",
             [f"Sum of divisors: $\\sigma({n}) = {sum(divisors(n))}$.", f"$\\frac{{{sum(divisors(n))}}}{{{n}}} = {ftex(ans)}$."], "dividing the number of divisors by $n$.")


@reg(S, "challenge")
def dvc_most_divisors(r):
    N = r.choice([30, 50, 60, 80, 100, 120, 150, 200])
    best = max(ndiv(n) for n in range(1, N + 1))
    winners = [n for n in range(1, N + 1) if ndiv(n) == best]
    p = f"Among the integers from $1$ to ${N}$, what is the largest number of positive divisors any one of them has?"
    return Q(p, best, [best - 2, best + 2, best - 1 if best - 1 != best - 2 else best + 4, ndiv(N) if ndiv(N) not in (best, best - 2, best + 2, best - 1) else best + 3, N // 10], "Look at numbers built from small primes.",
             "the maximum divisor count.", "highly divisible numbers use small primes with decreasing exponents.",
             [f"Candidates like ${', '.join(map(str, winners))}$ have ${best}$ divisors: " + f"for example ${winners[0]} = {ftex_fact(winners[0])}$.", "Checking other numbers built from $2, 3, 5, 7$ shows none in range has more."],
             "picking the largest number in range, which isn't usually the most divisible.")


# ================================================================ nt_gcd
S = "nt_gcd"


@reg(S, "basics")
def g_lcm_two(r):
    a, b = r.sample([4, 6, 8, 9, 10, 12, 14, 15, 18, 20, 21, 24, 28, 30, 35, 36, 42, 45], 2)
    ans = math.lcm(a, b)
    p = f"What is the least common multiple of ${a}$ and ${b}$?"
    return Q(p, ans, [a * b if a * b != ans else ans * 2, math.gcd(a, b), ans + math.gcd(a, b), ans // 2 if ans % 2 == 0 and ans // 2 not in (a, b) else ans + a, max(a, b)], "Take the highest power of each prime.",
             "the LCM.", "LCM uses each prime to its highest power in either number.",
             [f"${a} = {ftex_fact(a)}$ and ${b} = {ftex_fact(b)}$.", f"LCM $= {ftex_fact(ans)} = {ans}$."], "multiplying the numbers when they share a factor.")


@reg(S, "basics")
def g_gcd_three(r):
    g = r.choice([2, 3, 4, 5, 6, 7, 8, 9, 12])
    ms = r.sample([3, 5, 7, 11, 13, 4, 9], 3)
    if math.gcd(math.gcd(ms[0], ms[1]), ms[2]) != 1:
        return None
    nums = [g * m for m in ms]
    p = f"What is the greatest common divisor of ${nums[0]}$, ${nums[1]}$, and ${nums[2]}$?"
    return Q(p, g, [math.gcd(nums[0], nums[1]) if math.gcd(nums[0], nums[1]) != g else g * 2, g * 2, min(nums), 1, g + 1], "Factor each number.",
             "the GCD.", "the GCD uses each prime to its lowest power among all the numbers.",
             [", ".join(f"${x} = {ftex_fact(x)}$" for x in nums) + ".", f"Common part: ${g}$."], "finding the GCD of only two of them.")


@reg(S, "basics")
def g_product_rule(r):
    g = r.choice([2, 3, 4, 5, 6])
    a, b = g * r.choice([2, 3, 5, 7]), g * r.choice([4, 9, 11, 13])
    if math.gcd(a, b) != g:
        return None
    P = a * b
    p = f"Two positive integers have product ${P}$ and greatest common divisor ${g}$. What is their least common multiple?"
    return Q(p, P // g, [P, P // (g * g), g * g, P // g + g, P - g], "$\\gcd \\times \\text{lcm} = $ product.",
             "the LCM.", "for any two positive integers, $\\gcd(a, b) \\cdot \\text{lcm}(a, b) = ab$.",
             [f"$\\text{{lcm}} = \\frac{{{P}}}{{{g}}} = {P // g}$."], "dividing by the GCD twice.")


@reg(S, "basics")
def g_reduce(r):
    g = r.randint(2, 15)
    a, b = r.sample(range(2, 30), 2)
    if math.gcd(a, b) != 1:
        return None
    p = f"When $\\dfrac{{{a * g}}}{{{b * g}}}$ is written in lowest terms $\\dfrac{{m}}{{n}}$, what is $m + n$?"
    return Q(p, a + b, [a * g + b * g, (a + b) * 2, a + b + g, a * b, (a + b) * g // 2 if (a + b) * g % 2 == 0 else a + b + 1], "Divide top and bottom by their GCD.",
             "$m + n$.", "lowest terms means dividing out the GCD.",
             [f"$\\gcd({a * g}, {b * g}) = {g}$.", f"$\\frac{{{a}}}{{{b}}}$, so $m + n = {a + b}$."], "dividing by a common factor that isn't the greatest one.")


@reg(S, "basics")
def g_euclid(r):
    g = r.randint(3, 40)
    a, b = r.sample(range(10, 80), 2)
    if math.gcd(a, b) != 1:
        return None
    x, y = g * a, g * b
    p = f"What is $\\gcd({x}, {y})$?"
    steps, u, v = [], max(x, y), min(x, y)
    while v:
        steps.append(f"${u} = {u // v} \\cdot {v} + {u % v}$")
        u, v = v, u % v
    return Q(p, g, [g * 2, 1, abs(x - y), g + 1, math.gcd(x, y + 1)], "Use the Euclidean algorithm.",
             "the GCD.", "Euclidean algorithm: $\\gcd(a, b) = \\gcd(b, a \\bmod b)$; repeat until the remainder is $0$.",
             ["; ".join(steps) + ".", f"The last nonzero remainder is ${g}$."], "stopping at the first remainder.")


@reg(S, "basics")
def g_gift_bags(r):
    g = r.randint(3, 12)
    a, b = r.sample(range(2, 15), 2)
    if math.gcd(a, b) != 1:
        return None
    p = f"A teacher has ${a * g}$ pens and ${b * g}$ pencils. She makes identical gift bags using all of them, with no leftovers. What is the greatest number of bags she can make?"
    return Q(p, g, [a + b, a * g + b * g, g * 2, math.lcm(a * g, b * g) if math.lcm(a * g, b * g) < 5000 else g + 1, a], "Each bag gets the same number of pens and the same number of pencils.",
             "the most bags.", "the number of bags must divide both counts; the largest such is the GCD.",
             [f"$\\gcd({a * g}, {b * g}) = {g}$.", f"Each bag gets ${a}$ pens and ${b}$ pencils."], "answering the contents of one bag.")


@reg(S, "basics")
def g_buses(r):
    a, b = r.sample([6, 8, 10, 12, 15, 18, 20, 24, 30, 40, 45], 2)
    L = math.lcm(a, b)
    h0 = r.randint(6, 9)
    p = f"Bus A leaves the station every ${a}$ minutes and bus B every ${b}$ minutes. Both leave at {h0}:00 a.m. How many minutes later do they next leave together?"
    return Q(p, L, [a * b if a * b != L else L * 2, math.gcd(a, b), a + b, L // 2 if L // 2 not in (a, b) else L + 10, max(a, b)], "Find the least common multiple.",
             "the minutes until they coincide.", "they leave together at common multiples of both intervals; the first is the LCM.",
             [f"${a} = {ftex_fact(a)}$, ${b} = {ftex_fact(b)}$.", f"$\\text{{lcm}} = {L}$ minutes."], "multiplying the intervals.")


@reg(S, "basics")
def g_phi(r):
    n = r.choice([12, 15, 18, 20, 21, 24, 28, 30, 36, 40, 42, 45, 48, 50, 60])
    ans = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
    p = f"How many integers from $1$ to ${n}$ share no common factor with ${n}$ other than $1$?"
    return Q(p, ans, [n - len(factorint(n)), ans + 1, ans * 2, n // 2, ndiv(n)], "Remove multiples of each prime factor of " + str(n) + ".",
             "the count of numbers relatively prime to " + str(n) + ".", "Euler's totient: $\\varphi(n) = n\\prod\\left(1 - \\frac{1}{p}\\right)$ over the primes dividing $n$.",
             [f"${n} = {ftex_fact(n)}$.", f"$\\varphi({n}) = {n}" + "".join(f" \\cdot \\left(1 - \\frac{{1}}{{{p_}}}\\right)" for p_ in sorted(factorint(n))) + f" = {ans}$."], "subtracting only the multiples of one prime.")


@reg(S, "basics")
def g_lcm_range(r):
    k = r.randint(5, 12)
    ans = math.lcm(*range(1, k + 1))
    p = f"What is the smallest positive integer divisible by every integer from $1$ to ${k}$?"
    return Q(p, ans, [math.factorial(k) if math.factorial(k) != ans else ans * 2, ans // 2, ans * 2, math.lcm(*range(1, k)) if math.lcm(*range(1, k)) != ans else ans * 3, ans + k], "Use the highest prime power at most " + str(k) + ".",
             "the LCM of $1$ through " + str(k) + ".", "the LCM needs the largest power of each prime that is at most " + str(k) + ".",
             [f"Prime powers: " + ", ".join(f"${p_}^{{{int(math.log(k, p_) + 1e-9)}}}$" for p_ in range(2, k + 1) if is_prime(p_)) + ".", f"Product: ${ans}$."], "multiplying all the numbers ($" + str(k) + "!$).")


@reg(S, "basics")
def g_ratio_gcd(r):
    a, b = r.sample(range(2, 11), 2)
    if math.gcd(a, b) != 1:
        return None
    g = r.randint(2, 15)
    p = f"Two numbers are in the ratio ${a}:{b}$, and their greatest common divisor is ${g}$. What is their least common multiple?"
    return Q(p, a * b * g, [a * b * g * g, g * (a + b), a * b, a * b * g + g, max(a, b) * g], "The numbers are " + f"{a}g" + " and " + f"{b}g" + ".",
             "the LCM.", "with a reduced ratio $a:b$, the numbers are $ag$ and $bg$ where $g$ is the GCD.",
             [f"Numbers: ${a * g}$ and ${b * g}$.", f"LCM $= {a} \\cdot {b} \\cdot {g} = {a * b * g}$."], "multiplying the two numbers.")


@reg(S, "basics")
def g_gears(r):
    a, b = r.sample([12, 15, 16, 18, 20, 24, 28, 30, 36, 40, 45], 2)
    L = math.lcm(a, b)
    p = f"Two meshing gears have ${a}$ and ${b}$ teeth. A tooth on each is marked, and the marks start touching. How many full turns does the ${a}$-tooth gear make before the marks touch again?"
    return Q(p, L // a, [L // b, L, math.gcd(a, b), L // a + 1, b], "The same number of teeth pass for both gears.",
             "the turns of the smaller... " if False else "turns of the " + str(a) + "-tooth gear.", "the marks meet again after a number of teeth that is a multiple of both tooth counts: the LCM.",
             [f"Teeth passed: $\\text{{lcm}}({a}, {b}) = {L}$.", f"Turns of the ${a}$-tooth gear: $\\frac{{{L}}}{{{a}}} = {L // a}$."], "answering the turns of the other gear.")


@reg(S, "basics")
def g_remainder_one(r):
    ks = sorted(r.sample([2, 3, 4, 5, 6, 7, 8, 9, 10], 3))
    rem = r.choice([1, 1, 2])
    if rem >= min(ks):
        return None
    L = math.lcm(*ks)
    ans = L + rem
    p = f"What is the smallest integer greater than $1$ that leaves a remainder of ${rem}$ when divided by each of ${ks[0]}$, ${ks[1]}$, and ${ks[2]}$?" if rem == 1 else f"What is the smallest integer greater than ${rem}$ that leaves a remainder of ${rem}$ when divided by each of ${ks[0]}$, ${ks[1]}$, and ${ks[2]}$?"
    return Q(p, ans, [math.prod(ks) + rem if math.prod(ks) + rem != ans else ans * 2, L, L - rem, ans + L, L + rem + 1], "Subtract the remainder.",
             "the number.", "$n - " + str(rem) + "$ must be a multiple of all three, so $n - " + str(rem) + "$ is a common multiple.",
             [f"$\\text{{lcm}}({ks[0]}, {ks[1]}, {ks[2]}) = {L}$.", f"$n = {L} + {rem} = {ans}$."], "multiplying the divisors instead of using the LCM.")


@reg(S, "basics")
def g_exponent_lcm(r):
    a, b, c, d = [r.randint(0, 8) for _ in range(4)]
    ans = max(a, c) + max(b, d)
    p = f"The least common multiple of $2^{{{a}}} \\cdot 3^{{{b}}}$ and $2^{{{c}}} \\cdot 3^{{{d}}}$ is $2^x \\cdot 3^y$. What is $x + y$?"
    return Q(p, ans, [min(a, c) + min(b, d), a + b + c + d, ans + 1, max(a, c) + min(b, d) if max(a, c) + min(b, d) != ans else ans - 1, max(a, b, c, d)], "Take the larger exponent of each prime.",
             "$x + y$.", "the LCM uses the larger exponent for each prime; the GCD uses the smaller.",
             [f"$x = \\max({a}, {c}) = {max(a, c)}$ and $y = \\max({b}, {d}) = {max(b, d)}$.", f"$x + y = {ans}$."], "using the smaller exponents (that's the GCD).")


@reg(S, "basics")
def g_gcd_factored(r):
    e = [r.randint(0, 6) for _ in range(5)]
    A = 2 ** e[0] * 3 ** e[1] * 5 ** e[2]
    B = 2 ** e[3] * 3 ** e[4] * 7
    g = math.gcd(A, B)
    p = f"What is $\\gcd(2^{{{e[0]}}} \\cdot 3^{{{e[1]}}} \\cdot 5^{{{e[2]}}},\\ 2^{{{e[3]}}} \\cdot 3^{{{e[4]}}} \\cdot 7)$?"
    return Q(p, g, [g * 2, g * 3 if g * 3 != g * 2 else g + 1, 2 ** max(e[0], e[3]) * 3 ** max(e[1], e[4]) if 2 ** max(e[0], e[3]) * 3 ** max(e[1], e[4]) != g else g * 5, 1 if g != 1 else 2, g * 35], "Take the smaller exponent of each shared prime.",
             "the GCD.", "only primes in both numbers count, each to its smaller exponent.",
             [f"$2^{{\\min({e[0]}, {e[3]})}} = 2^{{{min(e[0], e[3])}}}$, $3^{{\\min({e[1]}, {e[4]})}} = 3^{{{min(e[1], e[4])}}}$; $5$ and $7$ are not shared.", f"GCD $= {g}$."], "including $5$ or $7$.")


@reg(S, "basics")
def g_ropes(r):
    g = r.randint(2, 12)
    ms = r.sample(range(2, 12), 3)
    if math.gcd(math.gcd(ms[0], ms[1]), ms[2]) != 1:
        return None
    L = [m * g for m in ms]
    p = f"Three ropes are ${L[0]}$, ${L[1]}$, and ${L[2]}$ meters long. They are cut into pieces that are all the same whole number of meters long, as long as possible, with nothing left over. How many pieces are there?"
    return Q(p, sum(ms), [g, sum(L), sum(ms) + 1, max(ms), sum(ms) * 2], "The piece length is the GCD.",
             "the total number of pieces.", "the longest piece length that divides all three lengths is their GCD.",
             [f"$\\gcd({L[0]}, {L[1]}, {L[2]}) = {g}$.", f"Pieces: ${ms[0]} + {ms[1]} + {ms[2]} = {sum(ms)}$."], "answering the piece length instead of the count.")


@reg(S, "basics")
def g_common_divisors(r):
    g = smooth(r, (2, 3, 5), 6, 200)
    a, b = r.sample([7, 11, 13, 1, 17], 2)
    x, y = g * a, g * b
    p = f"How many positive integers divide both ${x}$ and ${y}$?"
    return Q(p, ndiv(g), [ndiv(x), ndiv(y), ndiv(g) + 1, g, ndiv(x) + ndiv(y) - ndiv(g)], "Common divisors are the divisors of the GCD.",
             "the number of common divisors.", "$d$ divides both numbers exactly when $d$ divides their GCD.",
             [f"$\\gcd({x}, {y}) = {g} = {ftex_fact(g)}$.", f"Its divisor count: ${ndiv(g)}$."], "answering the GCD itself.")


@reg(S, "challenge")
def gc_pairs_gcd_lcm(r):
    g = r.choice([1, 2, 3, 6])
    k = smooth(r, (2, 3, 5, 7), 6, 500)
    L = g * k
    m = len(factorint(k))
    ans = 2 ** m
    p = f"How many ordered pairs of positive integers $(a, b)$ have $\\gcd(a, b) = {g}$ and $\\text{{lcm}}(a, b) = {L}$?"
    return Q(p, ans, [ans // 2 if ans > 1 else 3, ndiv(k), ans + 1, ans * 2, m], "Divide everything by the GCD.",
             "the count of ordered pairs.", f"write $a = {g}x$, $b = {g}y$ with $\\gcd(x, y) = 1$ and $xy = {k}$. Each prime power of ${k}$ goes entirely to $x$ or to $y$.",
             [f"${k} = {ftex_fact(k)}$ has ${m}$ different primes.", f"Each goes to $x$ or $y$: $2^{{{m}}} = {ans}$ ordered pairs."], "counting unordered pairs, or splitting prime powers between $x$ and $y$.")


@reg(S, "challenge")
def gc_mersenne(r):
    a, b = r.sample(range(4, 30), 2)
    g = math.gcd(a, b)
    ans = 2 ** g - 1
    p = f"What is $\\gcd(2^{{{a}}} - 1,\\ 2^{{{b}}} - 1)$?"
    return Q(p, ans, [2 ** g, 1 if ans != 1 else 3, 2 ** (g + 1) - 1, 2 ** abs(a - b) - 1 if abs(a - b) != g else ans * 2 + 1, g], "The Euclidean algorithm on the exponents.",
             "the GCD.", "$\\gcd(2^a - 1, 2^b - 1) = 2^{\\gcd(a, b)} - 1$, because $2^a - 1 \\equiv 2^{a - b} - 1 \\pmod{2^b - 1}$, which mirrors the Euclidean algorithm on exponents.",
             [f"$\\gcd({a}, {b}) = {g}$.", f"So the GCD is $2^{{{g}}} - 1 = {ans}$."], "computing $\\gcd(a, b)$ and stopping.")


@reg(S, "challenge")
def gc_phi_composite(r):
    n = smooth(r, (2, 3, 5, 7, 11), 100, 3000)
    ans = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
    p = f"How many integers from $1$ to ${n}$ are relatively prime to ${n}$?"
    return Q(p, ans, [n - sum(n // p_ for p_ in factorint(n)), ans + 1, ans * 2, n // 2, n - len(factorint(n))], "Use Euler's totient function.",
             "$\\varphi(" + str(n) + ")$.", "$\\varphi(n) = n\\prod_{p \\mid n}\\left(1 - \\frac{1}{p}\\right)$, from inclusion and exclusion on the prime factors.",
             [f"${n} = {ftex_fact(n)}$.", f"$\\varphi = {n}" + "".join(f" \\cdot \\frac{{{p_ - 1}}}{{{p_}}}" for p_ in sorted(factorint(n))) + f" = {ans}$."], "subtracting the multiples of each prime without adding back the overlaps.")


@reg(S, "challenge")
def gc_max_gcd_sum(r):
    S_ = r.choice([x for x in range(30, 400) if not is_prime(x)])
    d = min(x for x in divisors(S_) if x >= 3)
    ans = S_ // d
    p = f"Two different positive integers add to ${S_}$. What is the largest their greatest common divisor can be?"
    return Q(p, ans, [S_ // 2 if S_ % 2 == 0 and S_ // 2 != ans else ans + 1, min(factorint(S_)), S_ - 1, ans - 1, max(factorint(S_)) if max(factorint(S_)) != ans else ans + 2], "The GCD divides the sum.",
             "the maximum GCD.", f"write the numbers as $gx$ and $gy$ with $x \\ne y$. Then $g(x + y) = {S_}$, and $x + y \\ge 3$.",
             [f"To make $g$ large, make $x + y$ the smallest divisor of ${S_}$ that is at least $3$: that's ${d}$.", f"$g = \\frac{{{S_}}}{{{d}}} = {ans}$, for example with ${ans}$ and ${S_ - ans}$."],
             "allowing the two numbers to be equal, which would give $" + str(S_ // 2 if S_ % 2 == 0 else ans) + "$.")


@reg(S, "challenge")
def gc_not_lowest(r):
    k = r.choice([6, 10, 12, 14, 15, 18, 20, 21, 30])
    N = r.randint(20, 80)
    ans = sum(1 for n in range(1, N + 1) if math.gcd(n, k) > 1)
    p = f"For how many integers $n$ from $1$ to ${N}$ is the fraction $\\dfrac{{n}}{{n + {k}}}$ not in lowest terms?"
    return Q(p, ans, [N - ans, ans + 1, N // k, ans - 1, sum(1 for n in range(1, N + 1) if math.gcd(n, n + k) == 1) // 2], "$\\gcd(n, n + k) = \\gcd(n, k)$.",
             "the count.", f"$\\gcd(n, n + {k}) = \\gcd(n, {k})$, so the fraction reduces exactly when $n$ shares a prime with ${k}$.",
             [f"${k} = {ftex_fact(k)}$.", f"Count $n \\le {N}$ divisible by any of ${', '.join(map(str, sorted(factorint(k))))}$ (inclusion and exclusion): ${ans}$."], "counting the fractions that ARE in lowest terms.")


@reg(S, "challenge")
def gc_always_divides(r):
    expr, ans = r.choice([("n^3 - n", 6), ("n^5 - n", 30), ("n^7 - n", 42), ("n^4 - n^2", 12), ("n^2 + n", 2), ("n(n + 1)(n + 2)(n + 3)", 24), ("n^3 + 3n^2 + 2n", 6)])
    vals = []
    for n in range(2, 40):
        v = eval(expr.replace("^", "**").replace("n(", "n*(").replace(")(", ")*(").replace("3n", "3*n").replace("2n", "2*n"))
        vals.append(v)
    g = 0
    for v in vals:
        g = math.gcd(g, v)
    assert g == ans, (expr, g)
    p = f"What is the largest integer that divides ${expr}$ for every integer $n$?"
    return Q(p, ans, [ans // 2, ans * 2, vals[0] if vals[0] != ans else ans + 6, ans + 6, 1 if ans != 1 else 3], "Try $n = 2$ and $n = 3$; the answer must divide both.",
             "the largest guaranteed divisor.", "test small values to find a candidate, then explain why it always works (Fermat's little theorem or consecutive factors).",
             [f"$n = 2$ gives ${vals[0]}$; $n = 3$ gives ${vals[1]}$. Their GCD is ${math.gcd(vals[0], vals[1])}$; checking more values brings it to ${ans}$.", f"${ans} = {ftex_fact(ans) if ans > 1 else '1'}$, and each prime power always divides the expression (by factoring into consecutive numbers or by Fermat's little theorem)."],
             "trusting just one value of $n$.")


@reg(S, "challenge")
def gc_diagonal_squares(r):
    a, b = r.randint(4, 30), r.randint(4, 30)
    ans = a + b - math.gcd(a, b)
    p = f"A ${a} \\times {b}$ rectangle is drawn on graph paper. How many unit squares does one of its diagonals pass through (going through the inside of the square, not just touching a corner)?"
    return Q(p, ans, [a + b, a * b, a + b - 1, ans + 1, max(a, b)], "Count grid lines crossed; subtract the times it crosses two at once.",
             "the number of squares crossed.", "each time the diagonal crosses a grid line it enters a new square, except when it passes exactly through a lattice point (crossing two lines at once).",
             [f"Crossings: ${a - 1}$ vertical and ${b - 1}$ horizontal lines.", f"Lattice points inside: $\\gcd({a}, {b}) - 1 = {math.gcd(a, b) - 1}$.", f"Squares: $1 + ({a - 1} + {b - 1}) - ({math.gcd(a, b) - 1}) = {ans}$."],
             "forgetting to subtract the lattice points where it crosses two lines at once.")


# ================================================================ nt_divisibility
S = "nt_divisibility"


@reg(S, "basics")
def di_eleven(r):
    while True:
        digits = [r.randint(1, 9)] + [r.randint(0, 9) for _ in range(3)]
        pos = r.randint(1, 3)
        sols = [d for d in range(10) if int("".join(map(str, digits[:pos] + [d] + digits[pos + 1:]))) % 11 == 0]
        if len(sols) == 1:
            break
    s = "".join(str(x) if i != pos else "A" for i, x in enumerate(digits))
    p = f"The four-digit number ${s}$ is divisible by $11$. What digit is $A$?"
    full = int(s.replace("A", str(sols[0])))
    return Q(p, sols[0], [(sols[0] + 1) % 10, (sols[0] + 5) % 10, (sols[0] + 3) % 10, (9 - sols[0]) if 9 - sols[0] != sols[0] else 7], "Alternating digit sum.",
             "the digit $A$.", "a number is divisible by $11$ exactly when its alternating digit sum (add, subtract, add, ...) is divisible by $11$.",
             [f"With $A = {sols[0]}$: ${full}$ has alternating sum $" + " - ".join(str(full)[i] if i % 2 == 0 else "" for i in range(4)).replace(" -  - ", " - ") + "$" if False else f"With $A = {sols[0]}$, the number is ${full}$ and its alternating sum is ${sum(int(c) * (1 if i % 2 == 0 else -1) for i, c in enumerate(str(full)))}$, a multiple of $11$.",
              "No other digit works."], "using the digit sum, which is the test for $3$ and $9$.")


@reg(S, "basics")
def di_four(r):
    pre = r.randint(10, 99)
    last = r.randint(0, 9)
    opts = [d for d in range(10) if (d * 10 + last) % 4 == 0]
    p = f"The number ${pre}A{last}$ has a missing tens digit $A$. For how many digits $A$ is the number divisible by $4$?"
    return Q(p, len(opts), [len(opts) + 1, 10 - len(opts), 2 if len(opts) != 2 else 3, 5 if len(opts) != 5 else 4, len(opts) - 1 if len(opts) > 1 else 6], "Only the last two digits matter.",
             "how many digits work.", "divisibility by $4$ depends only on the number formed by the last two digits.",
             [f"Need ${'A'}{last}$ divisible by $4$: " + ", ".join(f"${d}{last}$" for d in opts) + (" work." if opts else ": none work."), f"That's ${len(opts)}$."], "checking the whole number's digit sum.")


@reg(S, "basics")
def di_six(r):
    pre = [r.randint(1, 9)] + [r.randint(0, 9) for _ in range(2)]
    last_even = r.choice([0, 2, 4, 6, 8])
    opts = [d for d in range(10) if int("".join(map(str, pre)) + str(d) + str(last_even)) % 6 == 0]
    if not opts:
        return None
    s = "".join(map(str, pre)) + "A" + str(last_even)
    p = f"What is the smallest digit $A$ that makes ${s}$ divisible by $6$?"
    return Q(p, opts[0], [opts[0] + 1, opts[0] + 2, opts[-1] if opts[-1] != opts[0] else opts[0] + 4, (opts[0] + 5) % 10 if (opts[0] + 5) % 10 not in (opts[0], opts[0] + 1, opts[0] + 2) else 9], "Divisible by $6$ means divisible by $2$ and by $3$.",
             "the smallest digit.", "it already ends in an even digit, so only the digit sum (test for $3$) matters.",
             [f"Digit sum without $A$: ${sum(pre) + last_even}$.", f"Smallest $A$ making the sum a multiple of $3$: $A = {opts[0]}$ (sum ${sum(pre) + last_even + opts[0]}$)."], "forgetting the evenness condition is already met and testing for $6$ by digit sum alone.")


@reg(S, "basics")
def di_mod9(r):
    n = r.randint(10 ** 5, 10 ** 7)
    p = f"What is the remainder when ${n}$ is divided by $9$?"
    ds = sum(map(int, str(n)))
    return Q(p, n % 9, [(n % 9 + 1) % 9, ds, n % 10, (n % 9 + 4) % 9, n % 3 if n % 3 != n % 9 else 8], "Add the digits.",
             "the remainder mod $9$.", "a number and its digit sum leave the same remainder when divided by $9$.",
             [f"Digit sum: ${' + '.join(str(n))} = {ds}$.", f"${ds} \\div 9$ leaves remainder ${n % 9}$."], "answering the digit sum itself.")


@reg(S, "basics")
def di_count_range(r):
    k = r.randint(3, 17)
    a, b = sorted(r.sample(range(10, 1000), 2))
    ans = b // k - (a - 1) // k
    p = f"How many multiples of ${k}$ are between ${a}$ and ${b}$, inclusive?"
    return Q(p, ans, [ans + 1, ans - 1, F(b - a, k).__floor__(), b // k, ans + 2], "Count multiples up to " + str(b) + " minus those below " + str(a) + ".",
             "the count.", "multiples of $k$ up to $N$: $\\left\\lfloor \\frac{N}{k} \\right\\rfloor$.",
             [f"Up to ${b}$: $\\left\\lfloor \\frac{{{b}}}{{{k}}} \\right\\rfloor = {b // k}$.", f"Up to ${a - 1}$: ${(a - 1) // k}$.", f"Between: ${b // k} - {(a - 1) // k} = {ans}$."], "subtracting the multiples up to " + str(a) + " instead of " + str(a - 1) + ".")


@reg(S, "basics")
def di_eight(r):
    pre = r.randint(1, 9)
    t, u = r.randint(0, 9), r.choice([0, 2, 4, 6, 8])
    opts = [d for d in range(10) if (d * 100 + t * 10 + u) % 8 == 0]
    if len(opts) == 0:
        return None
    p = f"For how many digits $A$ is the number ${pre}A{t}{u}$ divisible by $8$?"
    return Q(p, len(opts), [len(opts) + 1, 10 - len(opts), 0 if opts else 2, len(opts) + 2, 1 if len(opts) != 1 else 3], "Only the last three digits matter.",
             "how many digits work.", "a number is divisible by $8$ exactly when its last three digits form a multiple of $8$.",
             [f"Check $A{t}{u}$ for $A = 0, \\ldots, 9$: " + ", ".join(f"${d}{t}{u}$" for d in opts) + " work.", f"Count: ${len(opts)}$."], "checking only the last two digits (that's the test for 4).")


@reg(S, "basics")
def di_largest_3digit(r):
    k = r.randint(7, 99)
    ans = 999 - 999 % k
    p = f"What is the largest three-digit multiple of ${k}$?"
    return Q(p, ans, [ans + k if ans + k < 1000 else ans - 2 * k, ans - k, 999 - k, 1000 - 1000 % k if 1000 % k else ans - 3 * k, ans + 1], "Divide $999$ by " + str(k) + ".",
             "the largest multiple.", "$999 = " + str(k) + "q + r$; the answer is $999 - r$.",
             [f"$999 = {k} \\cdot {999 // k} + {999 % k}$.", f"$999 - {999 % k} = {ans}$."], "rounding up past $999$.")


@reg(S, "basics")
def di_nines(r):
    n = r.randint(4, 20)
    k = r.choice([1, 2, 3, 5, 7])
    N = 10 ** n - k
    ans = sum(map(int, str(N)))
    p = f"What is the sum of the digits of $10^{{{n}}} - {k}$?"
    return Q(p, ans, [9 * n, ans + 9, ans - 9, n + 10 - k, 9 * (n - 1)], "Write out what $10^n - " + str(k) + "$ looks like.",
             "the digit sum.", "$10^n - " + str(k) + "$ is a string of $9$s ending in $" + str(10 - k) + "$.",
             [f"$10^{{{n}}} - {k} = {'9' * (n - 1)}{10 - k}$ (${n - 1}$ nines then ${10 - k}$).", f"Digit sum: $9 \\cdot {n - 1} + {10 - k} = {ans}$."], "counting $n$ nines.")


@reg(S, "basics")
def di_both(r):
    a, b = r.sample([4, 6, 8, 9, 10, 12, 14, 15], 2)
    N = r.randint(100, 1000)
    L = math.lcm(a, b)
    ans = N // L
    p = f"How many integers from $1$ to ${N}$ are divisible by both ${a}$ and ${b}$?"
    return Q(p, ans, [N // (a * b) if N // (a * b) != ans else ans + 1, N // a + N // b - ans, ans + 1, N // max(a, b), N // a], "Divisible by both means divisible by the LCM.",
             "the count.", "a number divisible by both is a multiple of their LCM.",
             [f"$\\text{{lcm}}({a}, {b}) = {L}$.", f"$\\left\\lfloor \\frac{{{N}}}{{{L}}} \\right\\rfloor = {ans}$."], "dividing by $" + str(a * b) + "$ (the product) when the numbers share a factor.")


@reg(S, "basics")
def di_fifteen_digit(r):
    pre = r.randint(10, 99)
    opts = [d for d in (0, 5) if int(f"{pre}{d}") % 15 == 0]
    if len(opts) != 1:
        return None
    p = f"The three-digit number ${pre}A$ is divisible by $15$. What digit is $A$?"
    return Q(p, opts[0], [5 - opts[0] if 5 - opts[0] != opts[0] else 1, 3, 6, 9, (opts[0] + 2) % 10], "$15 = 3 \\cdot 5$.",
             "the digit $A$.", "divisible by $15$ means divisible by both $5$ (last digit $0$ or $5$) and $3$ (digit sum).",
             [f"$A$ must be $0$ or $5$.", f"Digit sums: ${sum(map(int, str(pre)))} + 0 = {sum(map(int, str(pre)))}$ and ${sum(map(int, str(pre)))} + 5 = {sum(map(int, str(pre))) + 5}$. Only $A = {opts[0]}$ gives a multiple of $3$."],
             "checking only one of the two conditions.")


@reg(S, "basics")
def di_smallest_multiplier(r):
    a, b = r.randint(2, 30), r.randint(12, 90)
    ans = b // math.gcd(a, b)
    p = f"What is the smallest positive integer $n$ such that ${a}n$ is a multiple of ${b}$?"
    return Q(p, ans, [b, math.lcm(a, b), math.gcd(a, b), ans * 2, ans + 1], "Cancel the common factor of " + str(a) + " and " + str(b) + ".",
             "the smallest $n$.", f"${a}n$ is a multiple of ${b}$ exactly when $n$ is a multiple of $\\frac{{{b}}}{{\\gcd({a}, {b})}}$.",
             [f"$\\gcd({a}, {b}) = {math.gcd(a, b)}$.", f"$n = \\frac{{{b}}}{{{math.gcd(a, b)}}} = {ans}$."], "answering " + str(b) + " without canceling.")


@reg(S, "basics")
def di_reverse_99(r):
    a, b, c = r.randint(1, 9), r.randint(0, 9), r.randint(0, 9)
    if a == c or c == 0:
        return None
    n, rev = 100 * a + 10 * b + c, 100 * c + 10 * b + a
    ans = F(n - rev, 99)
    p = f"What is $\\dfrac{{{n} - {rev}}}{{99}}$?"
    return Q(p, ans, [n - rev, a + c, a * c, ans + 1, -ans], "Write each number as $100a + 10b + c$.",
             "the value.", "$\\overline{abc} - \\overline{cba} = 99(a - c)$: the middle digit cancels.",
             [f"$a = {a}$, $c = {c}$.", f"$\\frac{{99({a} - {c})}}{{99}} = {a - c}$."], "doing the long subtraction and then dividing incorrectly.")


@reg(S, "basics")
def di_mod11(r):
    n = r.randint(10 ** 4, 10 ** 6)
    s = str(n)
    alt = sum(int(c) * (1 if i % 2 == 0 else -1) for i, c in enumerate(reversed(s)))
    p = f"What is the remainder when ${n}$ is divided by $11$?"
    return Q(p, n % 11, [(n % 11 + 1) % 11, sum(map(int, s)) % 11 if sum(map(int, s)) % 11 != n % 11 else (n % 11 + 3) % 11, n % 10 if n % 10 != n % 11 else (n % 11 + 5) % 11, (n % 11 + 2) % 11, n % 9 if n % 9 != n % 11 else 10], "Alternate signs on the digits, starting from the right.",
             "the remainder mod $11$.", "$10 \\equiv -1 \\pmod{11}$, so digits alternate between $+$ and $-$ starting from the units digit.",
             [f"From the right: " + " ".join(f"{'+' if i % 2 == 0 else '-'} {c}" for i, c in enumerate(reversed(s))).lstrip("+ ") + f" $= {alt}$.", f"${alt}$ leaves remainder ${n % 11}$ mod $11$."], "using the plain digit sum.")


@reg(S, "basics")
def di_three_not_nine(r):
    N = r.randint(50, 500)
    ans = N // 3 - N // 9
    p = f"How many integers from $1$ to ${N}$ are divisible by $3$ but not by $9$?"
    return Q(p, ans, [N // 3, N // 9, ans + 1, N // 3 + N // 9, ans - 1], "Multiples of $3$ minus multiples of $9$.",
             "the count.", "every multiple of $9$ is also a multiple of $3$, so subtract.",
             [f"Multiples of $3$: ${N // 3}$. Multiples of $9$: ${N // 9}$.", f"${N // 3} - {N // 9} = {ans}$."], "adding instead of subtracting.")


@reg(S, "basics")
def di_digit_perms(r):
    digits = sorted(r.sample(range(1, 10), 4))
    import itertools as it
    good = [s for s in it.combinations(digits, 3) if sum(s) % 3 == 0]
    ans = 6 * len(good)
    p = f"How many three-digit numbers with three different digits, all chosen from ${', '.join(map(str, digits))}$, are divisible by $3$?"
    return Q(p, ans, [len(good), ans + 6, 24, ans // 2 if ans else 6, 4 * 6 - ans if 24 - ans != ans else 12], "Divisibility by $3$ only depends on which digits are used.",
             "the count.", "pick the set of three digits (their sum must be a multiple of $3$), then arrange it in $3! = 6$ ways.",
             [f"Digit sets with sum divisible by $3$: " + (", ".join("$\\{" + ", ".join(map(str, s)) + "\\}$" for s in good) if good else "none") + ".", f"Each gives $6$ numbers: ${6} \\cdot {len(good)} = {ans}$."], "counting digit sets without arranging them.")


@reg(S, "basics")
def di_sum_parity(r):
    a, b = sorted(r.sample(range(1, 60), 2))
    if b - a < 5:
        return None
    nums = list(range(a, b + 1))
    s = sum(nums)
    ans = s % 2
    odd_count = sum(1 for x in nums if x % 2)
    p = f"Is the sum $" + f"{a} + {a + 1} + \\cdots + {b}" + "$ even or odd? Answer with its remainder when divided by $2$."
    return Q(p, ans, [1 - ans, 2, 3, 4], "Count the odd numbers in the sum.",
             "the remainder mod 2.", "a sum is odd exactly when it has an odd number of odd terms.",
             [f"Odd numbers from ${a}$ to ${b}$: ${odd_count}$.", f"${odd_count}$ is {'odd' if odd_count % 2 else 'even'}, so the sum is {'odd' if ans else 'even'}: remainder ${ans}$."], "counting all terms instead of only the odd ones.")


@reg(S, "challenge")
def dic_cubic_divides(r):
    a = r.randint(2, 12)
    b = r.randint(-200, 400)
    K = abs(b - a ** 3)
    if K == 0 or K - a <= 0:
        return None
    ans = K - a
    p = f"What is the largest positive integer $n$ for which $n + {a}$ divides $n^3 {'+' if b >= 0 else '-'} {abs(b)}$?"
    return Q(p, ans, [K, K + a, ans - 1, a ** 3, abs(b)], "Find the remainder when $n^3 " + ("+" if b >= 0 else "-") + f" {abs(b)}$ is divided by $n + {a}$.",
             "the largest $n$.", f"$n \\equiv -{a} \\pmod{{n + {a}}}$, so $n^3 {'+' if b >= 0 else '-'} {abs(b)} \\equiv (-{a})^3 {'+' if b >= 0 else '-'} {abs(b)} = {b - a ** 3}$. So $n + {a}$ must divide ${K}$.",
             [f"Remainder Theorem: $n + {a}$ divides $n^3{sg(b)}$ exactly when it divides ${K}$.", f"The largest is $n + {a} = {K}$, so $n = {ans}$."], "setting $n = " + str(K) + "$ and forgetting to subtract " + str(a) + ".")


@reg(S, "challenge")
def dic_repunit(r):
    pr = r.choice([3, 7, 11, 13, 37, 41, 27])
    k = next(k for k in range(1, 100) if int("1" * k) % pr == 0)
    p = f"What is the smallest number of $1$s in a number $11\\ldots1$ (all digits $1$) that is divisible by ${pr}$?"
    return Q(p, k, [k + 1, k - 1 if k > 1 else k + 3, pr - 1, k * 2, pr], "Track remainders of $1, 11, 111, \\ldots$ mod " + str(pr) + ".",
             "the smallest length.", "each repunit is $10 \\times$ the previous $+ 1$, so remainders follow $r \\to 10r + 1 \\pmod{" + str(pr) + "}$.",
             ["Remainders: " + ", ".join(str(int("1" * j) % pr) for j in range(1, k + 1)) + ".", f"The first zero is at length ${k}$."], "guessing $p - 1$, which is a multiple of the answer but not always the smallest.")


@reg(S, "challenge")
def dic_concat(r):
    n = r.randint(12, 60)
    m = r.choice([9, 3])
    s = n * (n + 1) // 2
    p = f"The number $N = 123456789101112\\ldots{n}$ is formed by writing the integers $1$ to ${n}$ in order. What is the remainder when $N$ is divided by ${m}$?"
    return Q(p, s % m, [(s + 1) % m, n % m, (s + 2) % m, 0 if s % m else 1, (s * 2) % m if (s * 2) % m != s % m else (s + 4) % m], "Digit sums of the pieces add up.",
             "the remainder mod " + str(m) + ".", "mod $9$ (and mod $3$), a number is congruent to its digit sum, and each piece $k$ is congruent to $k$ itself.",
             [f"$N \\equiv 1 + 2 + \\cdots + {n} = {s} \\pmod{{{m}}}$.", f"${s} \\bmod {m} = {s % m}$."], "adding only the single-digit pieces.")


@reg(S, "challenge")
def dic_zero_one(r):
    k = r.choice([3, 6, 12, 15, 18, 24, 30, 36, 45])
    ans = next(int(bin(i)[2:]) for i in range(1, 10 ** 4) if int(bin(i)[2:]) % k == 0)
    p = f"What is the smallest positive multiple of ${k}$ whose digits are all $0$s and $1$s?"
    ln = len(str(ans))
    return Q(p, ans, [int("1" * ln), ans * 10, int("1" * (ln - 1) + "0") if int("1" * (ln - 1) + "0") != ans else ans + 1, int("1" * (ln + 1)), ans // 10 if ans % 10 == 0 else ans + 10], "Split " + str(k) + " into factors that force the last digits and the digit sum.",
             "the smallest such number.", f"${k} = {ftex_fact(k)}$: factors of $2$ and $5$ force trailing zeros; factors of $3$ or $9$ force the number of $1$s.",
             [f"${ans}$ has digit sum ${sum(map(int, str(ans)))}$ and ends in ${len(str(ans)) - len(str(ans).rstrip('0'))}$ zero(s), which meets every requirement.", "Any shorter string of $0$s and $1$s fails one of them."], "forgetting the trailing zeros needed for factors of $2$ or $5$.")


@reg(S, "challenge")
def dic_all_integers(r):
    a, b = r.randint(1, 20), r.randint(1, 20)
    K = a + b
    ans = 2 * ndiv(K)
    p = f"For how many integers $n$ (positive, negative, or zero) is $\\dfrac{{n + {a}}}{{n - {b}}}$ an integer?"
    return Q(p, ans, [ndiv(K), ans - 1, ans + 2, K, ans // 2 + 1], "Write it as $1 + \\frac{" + str(K) + "}{n - " + str(b) + "}$.",
             "the count.", f"$\\frac{{n + {a}}}{{n - {b}}} = 1 + \\frac{{{K}}}{{n - {b}}}$, so $n - {b}$ must divide ${K}$ (positive or negative divisor).",
             [f"${K}$ has ${ndiv(K)}$ positive divisors, so ${ans}$ divisors counting negatives.", f"Each gives one $n$: ${ans}$."], "counting only positive divisors.")


@reg(S, "challenge")
def dic_consecutive_product(r):
    k = r.randint(3, 6)
    ans = math.factorial(k)
    expr = "".join(f"(n + {i})" if i else "n" for i in range(k))
    p = f"What is the largest integer that divides ${expr}$ for every positive integer $n$?"
    return Q(p, ans, [ans // 2, ans * 2, k, math.factorial(k + 1), ans + k], "Try $n = 1$.",
             "the largest guaranteed divisor.", f"the product of ${k}$ consecutive integers is ${k}!$ times a binomial coefficient, so it's always a multiple of ${k}!$.",
             [f"$n = 1$ gives ${k}! = {ans}$, so the answer is at most ${ans}$.", f"And $\\frac{{n(n + 1)\\cdots(n + {k - 1})}}{{{k}!}} = \\binom{{n + {k - 1}}}{{{k}}}$ is always an integer."], "guessing $" + str(k) + "$ or the product of the first few primes.")


@reg(S, "challenge")
def dic_digit_sum_mult5(r):
    s = r.randint(5, 20)
    xs = [n for n in range(100, 1000) if n % 5 == 0 and sum(map(int, str(n))) == s]
    p = f"How many three-digit multiples of $5$ have digits adding to ${s}$?"
    z = sum(1 for n in xs if n % 10 == 0)
    return Q(p, len(xs), [len(xs) + 1, z, len(xs) - z, len(xs) + 2, len(xs) * 2 if len(xs) * 2 != len(xs) + 2 else len(xs) + 3], "The last digit is $0$ or $5$; count each case.",
             "the count.", "split by the last digit, then count first two digits with the right sum.",
             [f"Last digit $0$: first two digits sum to ${s}$, ${z}$ ways.", f"Last digit $5$: first two digits sum to ${s - 5}$, ${len(xs) - z}$ ways.", f"Total: ${len(xs)}$."], "letting the first digit be $0$.")


# ================================================================ nt_modular
S = "nt_modular"


@reg(S, "basics")
def mo_sum_mod(r):
    m = r.randint(5, 13)
    xs = [r.randint(100, 999) for _ in range(3)]
    p = f"What is the remainder when ${xs[0]} + {xs[1]} + {xs[2]}$ is divided by ${m}$?"
    return Q(p, sum(xs) % m, [(sum(xs) + 1) % m, sum(x % m for x in xs), (sum(xs) + 2) % m, (sum(xs) - 1) % m, 0 if sum(xs) % m else 1], "Reduce each number first.",
             "the remainder.", "remainders add: reduce each number mod " + str(m) + ", add, and reduce again.",
             ["Remainders: " + ", ".join(f"${x} \\equiv {x % m}$" for x in xs) + ".", f"Sum: ${sum(x % m for x in xs)} \\equiv {sum(xs) % m} \\pmod{{{m}}}$."], "forgetting to reduce the sum of remainders.")


@reg(S, "basics")
def mo_negative(r):
    m = r.randint(5, 12)
    k = r.randint(m + 1, 60)
    p = f"What is the remainder when $-{k}$ is divided by ${m}$? (Remainders are between $0$ and ${m - 1}$.)"
    return Q(p, (-k) % m, [k % m, m - 1, -(k % m) if k % m else 1, (k + 1) % m, 0 if (-k) % m else 2], "Add multiples of " + str(m) + " until you reach a number in range.",
             "the remainder.", "a remainder must be between $0$ and $m - 1$, even for negative numbers.",
             [f"$-{k} = {m} \\cdot ({-((k + m - 1) // m)}) + {(-k) % m}$.", f"Remainder: ${(-k) % m}$."], "giving the remainder of $" + str(k) + "$ instead.")


@reg(S, "basics")
def mo_clock(r):
    t = r.randint(1, 12)
    h = r.randint(25, 500)
    ans = (t - 1 + h) % 12 + 1
    p = f"It is {t} o'clock now. What hour will a 12-hour clock show ${h}$ hours from now?"
    return Q(p, ans, [(t + h) % 12, (t + h) % 24 if (t + h) % 24 != ans else ans + 1, ans % 12 + 1, h % 12, (ans + 5) % 12 + 1], "Only the remainder of " + str(h) + " mod 12 matters.",
             "the hour shown.", "every $12$ hours the clock comes back to the same hour.",
             [f"${h} = 12 \\cdot {h // 12} + {h % 12}$.", f"{t} o'clock plus ${h % 12}$ hours is {ans} o'clock."], "writing $0$ instead of $12$ for a remainder of zero.")


@reg(S, "basics")
def mo_square(r):
    m = r.randint(5, 13)
    a = r.randint(1, m - 1)
    p = f"When $n$ is divided by ${m}$, the remainder is ${a}$. What is the remainder when $n^2$ is divided by ${m}$?"
    return Q(p, a * a % m, [a * a, (2 * a) % m, (a * a + 1) % m, a, (a * a + m - 1) % m], "Remainders multiply.",
             "the remainder of $n^2$.", "if $n \\equiv a$, then $n^2 \\equiv a^2 \\pmod{m}$.",
             [f"$n^2 \\equiv {a}^2 = {a * a} \\pmod{{{m}}}$.", f"${a * a} \\equiv {a * a % m}$."], "forgetting to reduce $" + str(a * a) + "$.")


@reg(S, "basics")
def mo_cube(r):
    m = r.randint(5, 11)
    a = r.randint(2, m - 1)
    b = r.randint(1, 20)
    ans = (a ** 3 + b) % m
    p = f"When $n$ is divided by ${m}$, the remainder is ${a}$. What is the remainder when $n^3 + {b}$ is divided by ${m}$?"
    return Q(p, ans, [(a ** 3) % m, (3 * a + b) % m, (ans + 1) % m, a ** 3 + b, (a + b) % m], "Replace $n$ with " + str(a) + ".",
             "the remainder.", "substitute the remainder for $n$ and reduce.",
             [f"$n^3 + {b} \\equiv {a}^3 + {b} = {a ** 3 + b} \\pmod{{{m}}}$.", f"${a ** 3 + b} \\equiv {ans}$."], "cubing without reducing.")


@reg(S, "basics")
def mo_count_class(r):
    m = r.randint(3, 12)
    rr = r.randint(0, m - 1)
    N = r.randint(50, 500)
    ans = sum(1 for n in range(1, N + 1) if n % m == rr)
    p = f"How many integers from $1$ to ${N}$ leave a remainder of ${rr}$ when divided by ${m}$?"
    return Q(p, ans, [ans + 1, ans - 1, N // m + 1 if N // m + 1 != ans else ans + 2, N - ans, N // rr if rr and N // rr != ans else ans + 3], "List them: they form an arithmetic sequence.",
             "the count.", f"the numbers are ${rr if rr else m}, {(rr if rr else m) + m}, \\ldots$, stepping by ${m}$.",
             [f"First: ${rr if rr else m}$. Last at most ${N}$: ${max(n for n in range(1, N + 1) if n % m == rr)}$.", f"Count: $\\frac{{{max(n for n in range(1, N + 1) if n % m == rr)} - {rr if rr else m}}}{{{m}}} + 1 = {ans}$."],
             "including $0$, which isn't in the range.")


@reg(S, "basics")
def mo_shifted(r):
    m = r.randint(5, 15)
    a, b = r.randint(1, 50), r.randint(0, m - 1)
    base = (b - a) % m
    ans = next(x for x in range(101, 101 + m) if x % m == base)
    p = f"What is the smallest integer $x > 100$ with $x + {a} \\equiv {b} \\pmod{{{m}}}$?"
    return Q(p, ans, [ans + m, ans - 1, base, ans + 1, 100 + base if 100 + base != ans else ans + 2], "Find which remainder $x$ needs.",
             "the smallest $x$ above $100$.", f"subtract ${a}$: $x \\equiv {b} - {a} \\equiv {base} \\pmod{{{m}}}$.",
             [f"$x \\equiv {base} \\pmod{{{m}}}$.", f"$100 \\equiv {100 % m}$, so step up to the next number $\\equiv {base}$: ${ans}$."], "solving for $x$ but forgetting the $x > 100$ condition.")


@reg(S, "basics")
def mo_mod4(r):
    n = r.randint(10 ** 6, 10 ** 9)
    m = r.choice([4, 8, 25])
    p = f"What is the remainder when ${n}$ is divided by ${m}$?"
    last = n % 100 if m in (4, 25) else n % 1000
    return Q(p, n % m, [(n % m + 1) % m, n % 10 % m if n % 10 % m != n % m else (n % m + 2) % m, sum(map(int, str(n))) % m if sum(map(int, str(n))) % m != n % m else (n % m + 3) % m, (n % m + m - 1) % m], "Only the last few digits matter.",
             "the remainder.", f"${'100' if m != 8 else '1000'}$ is a multiple of ${m}$, so only the last {'two' if m != 8 else 'three'} digits matter.",
             [f"Last digits: ${last}$.", f"${last} \\bmod {m} = {n % m}$."], "using the digit sum, which works for $3$ and $9$ only.")


@reg(S, "basics")
def mo_consecutive_product(r):
    m = r.randint(5, 13)
    a = r.randint(100, 900)
    k = r.choice([2, 3])
    prod = math.prod(range(a, a + k))
    p = f"What is the remainder when ${' \\times '.join(str(a + i) for i in range(k))}$ is divided by ${m}$?"
    return Q(p, prod % m, [(prod + 1) % m, sum(range(a, a + k)) % m, (a % m) ** k % m if (a % m) ** k % m != prod % m else (prod % m + 2) % m, (prod % m + m - 1) % m, 0 if prod % m else 1], "Reduce each factor first.",
             "the remainder.", "remainders multiply: reduce each factor, multiply, reduce again.",
             ["Factors mod " + str(m) + ": " + ", ".join(f"${a + i} \\equiv {(a + i) % m}$" for i in range(k)) + ".", f"Product: ${' \\cdot '.join(str((a + i) % m) for i in range(k))} = {math.prod((a + i) % m for i in range(k))} \\equiv {prod % m}$."],
             "adding the remainders instead of multiplying.")


@reg(S, "basics")
def mo_sum_squares(r):
    n = r.randint(10, 40)
    m = r.choice([5, 7, 9, 10, 11])
    s = n * (n + 1) * (2 * n + 1) // 6
    p = f"What is the remainder when $1^2 + 2^2 + \\cdots + {n}^2$ is divided by ${m}$?"
    return Q(p, s % m, [(s + 1) % m, (n * (n + 1) // 2) % m, (s + 2) % m, (s % m + m - 1) % m, 0 if s % m else 3], "Use $\\frac{n(n + 1)(2n + 1)}{6}$.",
             "the remainder.", "the sum of the first $n$ squares is $\\frac{n(n + 1)(2n + 1)}{6}$.",
             [f"Sum: $\\frac{{{n} \\cdot {n + 1} \\cdot {2 * n + 1}}}{{6}} = {s}$.", f"${s} \\bmod {m} = {s % m}$."], "using the sum of the first $n$ numbers instead of squares.")


@reg(S, "basics")
def mo_combo(r):
    m = r.randint(5, 13)
    a, b = r.randint(0, m - 1), r.randint(0, m - 1)
    c1, c2 = r.randint(2, 6), r.randint(2, 6)
    ans = (c1 * a + c2 * b) % m
    p = f"If $x \\equiv {a} \\pmod{{{m}}}$ and $y \\equiv {b} \\pmod{{{m}}}$, what is the remainder when ${c1}x + {c2}y$ is divided by ${m}$?"
    return Q(p, ans, [(a + b) % m, (c1 * b + c2 * a) % m if (c1 * b + c2 * a) % m != ans else (ans + 1) % m, c1 * a + c2 * b if c1 * a + c2 * b != ans else (ans + 2) % m, (ans + 3) % m, (ans + m - 1) % m], "Substitute the remainders.",
             "the remainder.", "linear combinations respect remainders.",
             [f"${c1} \\cdot {a} + {c2} \\cdot {b} = {c1 * a + c2 * b}$.", f"${c1 * a + c2 * b} \\equiv {ans} \\pmod{{{m}}}$."], "swapping the coefficients.")


@reg(S, "basics")
def mo_repeated_digits(r):
    block = str(r.randint(100, 9999))
    k = r.randint(3, 9)
    N = block * k
    ds = sum(map(int, N))
    p = f"What is the remainder when the ${len(N)}$-digit number formed by writing ${block}$ ${k}$ times in a row is divided by $9$?"
    return Q(p, ds % 9, [sum(map(int, block)) % 9 if sum(map(int, block)) % 9 != ds % 9 else (ds + 1) % 9, (ds + 1) % 9, k % 9 if k % 9 != ds % 9 else (ds + 2) % 9, (ds + 4) % 9, 0 if ds % 9 else 3], "A number and its digit sum agree mod 9.",
             "the remainder mod 9.", "add the digits: each copy of the block adds the same amount.",
             [f"Block digit sum: ${sum(map(int, block))}$.", f"Total: ${k} \\cdot {sum(map(int, block))} = {ds}$.", f"${ds} \\bmod 9 = {ds % 9}$."], "using only one copy of the block.")


@reg(S, "basics")
def mo_repeating_decimal(r):
    d = r.choice([7, 13, 11, 27, 37, 41])
    num_ = r.randint(1, d - 1)
    if math.gcd(num_, d) != 1:
        return None
    digits, rem = [], num_
    for _ in range(60):
        rem *= 10
        digits.append(rem // d)
        rem %= d
    per = next(k for k in range(1, 60) if digits[:k] == digits[k:2 * k])
    pos = r.randint(20, 300)
    ans = digits[(pos - 1) % per]
    p = f"What is the ${pos}$th digit after the decimal point in $\\dfrac{{{num_}}}{{{d}}}$?"
    return Q(p, ans, [digits[pos % per], digits[(pos + 1) % per], (ans + 1) % 10, (ans + 5) % 10 if (ans + 5) % 10 not in (digits[pos % per], digits[(pos + 1) % per]) else (ans + 7) % 10], "Find the repeating block.",
             "the digit in position " + str(pos) + ".", "the decimal repeats with a fixed block; reduce the position mod the block length.",
             [f"$\\frac{{{num_}}}{{{d}}} = 0.\\overline{{{''.join(map(str, digits[:per]))}}}$, block length ${per}$.", f"${pos} = {per} \\cdot {(pos - 1) // per} + {(pos - 1) % per + 1}$, so it's digit ${(pos - 1) % per + 1}$ of the block: ${ans}$."],
             "an off by one when matching the remainder to a position in the block.")


@reg(S, "basics")
def mo_triangular_units(r):
    n = r.randint(20, 300)
    s = n * (n + 1) // 2
    p = f"What is the units digit of $1 + 2 + 3 + \\cdots + {n}$?"
    return Q(p, s % 10, [(s + 1) % 10, n % 10, (s + 5) % 10, (n * n) % 10 if (n * n) % 10 != s % 10 else (s + 3) % 10, (s + 9) % 10], "Use the formula, then keep only the last digit.",
             "the units digit.", "$1 + \\cdots + n = \\frac{n(n + 1)}{2}$.",
             [f"$\\frac{{{n} \\cdot {n + 1}}}{{2}} = {s}$.", f"Units digit: ${s % 10}$."], "adding only the units digits of the terms without carrying correctly.")


@reg(S, "basics")
def mo_sum_class(r):
    m = r.randint(3, 9)
    rr = r.randint(1, m - 1)
    N = r.randint(30, 120)
    xs = [n for n in range(1, N + 1) if n % m == rr]
    p = f"What is the sum of all integers from $1$ to ${N}$ that leave a remainder of ${rr}$ when divided by ${m}$?"
    return Q(p, sum(xs), [sum(xs) + xs[-1] + m, sum(xs) - xs[-1], len(xs), sum(xs) + rr, sum(range(1, N + 1)) // m], "They form an arithmetic sequence.",
             "the sum.", "the numbers $" + f"{rr}, {rr + m}, \\ldots" + "$ form an arithmetic sequence: sum $=$ count $\\times$ average.",
             [f"From ${xs[0]}$ to ${xs[-1]}$ in steps of ${m}$: ${len(xs)}$ terms.", f"Sum: ${len(xs)} \\cdot \\frac{{{xs[0]} + {xs[-1]}}}{{2}} = {sum(xs)}$."], "including one term past " + str(N) + ".")


@reg(S, "basics")
def mo_mod_product_big(r):
    m = r.choice([7, 9, 11, 13])
    a, b = r.randint(10 ** 3, 10 ** 4), r.randint(10 ** 3, 10 ** 4)
    p = f"What is the remainder when ${a} \\times {b} - {a}$ is divided by ${m}$?"
    ans = (a * b - a) % m
    return Q(p, ans, [(a * b) % m, (a * b + a) % m if (a * b + a) % m != ans else (ans + 1) % m, (ans + 2) % m, (b - 1) % m if (b - 1) % m != ans else (ans + 3) % m, (ans + m - 1) % m], "Factor: $a(b - 1)$.",
             "the remainder.", "factor first, then reduce each factor.",
             [f"${a} \\times {b} - {a} = {a}({b} - 1) = {a} \\cdot {b - 1}$.", f"${a} \\equiv {a % m}$ and ${b - 1} \\equiv {(b - 1) % m}$; product $\\equiv {(a % m) * ((b - 1) % m)} \\equiv {ans}$."], "forgetting to subtract " + str(a) + ".")


@reg(S, "challenge")
def moc_crt2(r):
    m1, m2 = r.sample([3, 4, 5, 7, 8, 9, 11], 2)
    if math.gcd(m1, m2) != 1:
        return None
    a, b = r.randint(0, m1 - 1), r.randint(0, m2 - 1)
    ans = next(x for x in range(1, m1 * m2 + 1) if x % m1 == a and x % m2 == b)
    p = f"What is the smallest positive integer that leaves remainder ${a}$ when divided by ${m1}$ and remainder ${b}$ when divided by ${m2}$?"
    return Q(p, ans, [ans + m1 * m2, m1 * m2 - ans if m1 * m2 - ans > 0 else ans + 1, a + b, ans + m1, ans - m2 if ans > m2 else ans + 2 * m2], "List numbers with the first remainder and test the second.",
             "the smallest such number.", "Chinese Remainder Theorem: there's exactly one answer between $1$ and " + str(m1 * m2) + ".",
             [f"Numbers $\\equiv {a} \\pmod{{{m1}}}$: " + ", ".join(str(x) for x in range(a if a else m1, a + m1 * m2 + 1, m1) if x > 0)[:80] + ", ...", f"The first that is $\\equiv {b} \\pmod{{{m2}}}$: ${ans}$."],
             "adding the remainders.")


@reg(S, "challenge")
def moc_sqrt_one(r):
    n = r.choice([8, 12, 15, 16, 20, 21, 24, 30, 35, 40, 48])
    xs = [x for x in range(n) if x * x % n == 1]
    p = f"How many integers $x$ with $0 \\le x < {n}$ satisfy $x^2 \\equiv 1 \\pmod{{{n}}}$?"
    return Q(p, len(xs), [2, len(xs) + 2, len(xs) - 1 if len(xs) > 3 else 6, len(xs) * 2, 1], "$1$ and $" + str(n - 1) + "$ always work. Are there more?",
             "the number of solutions.", f"$x^2 \\equiv 1$ means ${n}$ divides $(x - 1)(x + 1)$; when ${n}$ has several prime factors there can be extra solutions.",
             [f"Checking $x = 0, 1, \\ldots, {n - 1}$: solutions are ${', '.join(map(str, xs))}$.", f"That's ${len(xs)}$."], "assuming only $\\pm 1$ work, as for prime moduli.")


@reg(S, "challenge")
def moc_linear(r):
    m = r.choice([17, 19, 23, 29, 31, 37])
    a = r.randint(2, m - 1)
    b = r.randint(1, m - 1)
    ans = next(x for x in range(1, m) if a * x % m == b)
    inv = pow(a, -1, m)
    p = f"What is the smallest positive integer $x$ with ${a}x \\equiv {b} \\pmod{{{m}}}$?"
    return Q(p, ans, [inv, (ans + 1) % m or m, b, m - ans, (b * a) % m if (b * a) % m != ans else (ans + 2) % m], "Find the inverse of " + str(a) + " mod " + str(m) + ".",
             "$x$.", f"multiply both sides by the inverse of ${a}$ (the number $u$ with ${a}u \\equiv 1$).",
             [f"${a} \\cdot {inv} = {a * inv} \\equiv 1 \\pmod{{{m}}}$, so the inverse is ${inv}$.", f"$x \\equiv {b} \\cdot {inv} = {b * inv} \\equiv {ans} \\pmod{{{m}}}$."], "dividing " + str(b) + " by " + str(a) + " as ordinary numbers.")


@reg(S, "challenge")
def moc_products_sum(r):
    n = r.randint(10, 50)
    m = r.choice([5, 7, 9, 11, 13])
    s = sum(k * (k + 1) for k in range(1, n + 1))
    p = f"What is the remainder when $1 \\cdot 2 + 2 \\cdot 3 + 3 \\cdot 4 + \\cdots + {n} \\cdot {n + 1}$ is divided by ${m}$?"
    return Q(p, s % m, [(s + 1) % m, (n * (n + 1)) % m, (s + 2) % m, (s % m + m - 1) % m, 0 if s % m else 2], "$k(k + 1)$ sums to $\\frac{n(n + 1)(n + 2)}{3}$.",
             "the remainder.", "$\\sum_{k=1}^n k(k + 1) = \\frac{n(n + 1)(n + 2)}{3}$ (it telescopes).",
             [f"Sum: $\\frac{{{n} \\cdot {n + 1} \\cdot {n + 2}}}{{3}} = {s}$.", f"${s} \\bmod {m} = {s % m}$."], "using only the last term.")


@reg(S, "challenge")
def moc_wilson(r):
    pr = r.choice([7, 11, 13, 17, 19, 23, 29])
    which = r.choice([1, 2])
    ans = pr - 1 if which == 1 else 1
    p = f"What is the remainder when ${pr - which}!$ is divided by ${pr}$?"
    return Q(p, ans, [0, pr - 1 if ans != pr - 1 else 1, 2, pr - 2, (pr - 1) // 2], "Pair each number with its inverse mod " + str(pr) + ".",
             "the remainder.", "Wilson's Theorem: $(p - 1)! \\equiv -1 \\pmod{p}$ for prime $p$.",
             ([f"$({pr} - 1)! \\equiv -1 \\equiv {pr - 1} \\pmod{{{pr}}}$."] if which == 1 else [f"$({pr} - 1)! = ({pr} - 1) \\cdot ({pr} - 2)! \\equiv -1$.", f"Since ${pr} - 1 \\equiv -1$, we get $-({pr} - 2)! \\equiv -1$, so $({pr} - 2)! \\equiv 1$."]),
             "thinking a factorial is always divisible by " + str(pr) + "; it isn't until the factorial reaches " + str(pr) + ".")


@reg(S, "challenge")
def moc_n3_minus_n(r):
    m = r.choice([24, 12, 48, 16])
    N = r.randint(30, 150)
    xs = [n for n in range(1, N + 1) if (n ** 3 - n) % m == 0]
    p = f"For how many integers $n$ from $1$ to ${N}$ is $n^3 - n$ divisible by ${m}$?"
    per = [n for n in range(1, m + 1) if (n ** 3 - n) % m == 0]
    return Q(p, len(xs), [len(xs) + 1, N, N // 2, len(xs) - 1, len(per)], "$n^3 - n = (n - 1)n(n + 1)$; check one full cycle of " + str(m) + " values.",
             "the count.", f"divisibility by ${m}$ depends only on $n \\bmod {m}$, so count good residues in one cycle and repeat.",
             [f"In each block of ${m}$, the good residues are ${', '.join(str(x % m) for x in per)}$: ${len(per)}$ of them.", f"Over $1$ to ${N}$: ${len(xs)}$."], "assuming the product of three consecutive numbers is always divisible by " + str(m) + ".")


@reg(S, "challenge")
def moc_rem_one_all(r):
    k = r.randint(4, 10)
    L = math.lcm(*range(2, k + 1))
    p = f"What is the smallest integer greater than $1$ that leaves remainder $1$ when divided by every integer from $2$ to ${k}$?"
    return Q(p, L + 1, [L, math.factorial(k) + 1 if math.factorial(k) != L else L * 2 + 1, L - 1, 2 * L + 1, L + k], "Subtract $1$.",
             "the number.", "$n - 1$ is divisible by $2, 3, \\ldots, " + str(k) + "$, so it's a multiple of their LCM.",
             [f"$\\text{{lcm}}(2, \\ldots, {k}) = {L}$.", f"$n = {L} + 1 = {L + 1}$."], "using $" + str(k) + "! + 1$.")
