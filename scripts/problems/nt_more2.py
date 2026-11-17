"""Extra Number Theory problem types (part 2): powers and units digits, bases, factorials."""
import math
from fractions import Fraction as F

from common import C, Q, num, text_choice
from nt_more1 import divisors, factorint, ftex_fact, is_prime, ndiv

MORE = {}


def reg(skill, level):
    def deco(fn):
        MORE.setdefault(skill, {"basics": [], "challenge": []})[level].append(fn)
        return fn
    return deco


def ftex(v):
    return num(F(v)).tex


def cycle(base, m, start=1):
    """Remainders of base^k mod m for k = start, start+1, ... until they repeat."""
    seen, out, k = {}, [], start
    while True:
        v = pow(base, k, m)
        if v in seen:
            return out[seen[v]:], seen[v]
        seen[v] = len(out)
        out.append(v)
        k += 1


def to_base(n, b):
    if n == 0:
        return "0"
    ds = []
    while n:
        ds.append("0123456789ABCDEF"[n % b])
        n //= b
    return "".join(reversed(ds))


def bchoice(n, b):
    return C(f"{to_base(n, b)}_{{{b}}}", n)


def bwrong(ans, b, wrong):
    """Base-b wrong choices with no repeated text; topped up with nearby values if needed."""
    seen, out = {ans.tex}, []
    for w in wrong:
        if w.tex not in seen and w.key != ans.key:
            seen.add(w.tex)
            out.append(w)
    k = 2
    while len(out) < 4:
        c = bchoice(int(ans.key) + k * (1 if k % 2 else -1), b) if int(ans.key) + k * (1 if k % 2 else -1) > 0 else bchoice(int(ans.key) + 10 * k, b)
        if c.tex not in seen:
            seen.add(c.tex)
            out.append(c)
        k += 1
    return out


def vp(n, p):
    """Exponent of prime p in n!."""
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


# ================================================================ nt_powers
S = "nt_powers"


@reg(S, "basics")
def pw_units_product(r):
    a, b = r.sample([2, 3, 7, 8, 12, 13, 17, 18], 2)
    m, n = r.randint(20, 300), r.randint(20, 300)
    ans = pow(a, m, 10) * pow(b, n, 10) % 10
    p = f"What is the units digit of ${a}^{{{m}}} \\cdot {b}^{{{n}}}$?"
    return Q(p, ans, [pow(a, m, 10), pow(b, n, 10), (pow(a, m, 10) + pow(b, n, 10)) % 10 if (pow(a, m, 10) + pow(b, n, 10)) % 10 != ans else (ans + 2) % 10, (ans + 5) % 10, (ans + 1) % 10], "Find each units digit separately, then multiply.",
             "the units digit.", "units digits of powers repeat in cycles of length at most $4$.",
             [f"Units digit of ${a}^{{{m}}}$: ${pow(a, m, 10)}$ (cycle {', '.join(str(pow(a, k, 10)) for k in range(1, 5))}; ${m} \\bmod 4 = {m % 4}$).",
              f"Units digit of ${b}^{{{n}}}$: ${pow(b, n, 10)}$ (cycle {', '.join(str(pow(b, k, 10)) for k in range(1, 5))}; ${n} \\bmod 4 = {n % 4}$).",
              f"Product: ${pow(a, m, 10)} \\cdot {pow(b, n, 10)} = {pow(a, m, 10) * pow(b, n, 10)}$, units digit ${ans}$."],
             "adding the units digits instead of multiplying.")


@reg(S, "basics")
def pw_units_minus(r):
    a = r.choice([2, 3, 7, 8, 9])
    n = r.randint(10, 400)
    k = r.randint(1, 9)
    ans = (pow(a, n, 10) - k) % 10
    p = f"What is the units digit of ${a}^{{{n}}} - {k}$?"
    return Q(p, ans, [pow(a, n, 10), (pow(a, n, 10) + k) % 10, (ans + 1) % 10, abs(pow(a, n, 10) - k), (ans + 4) % 10], "Find the units digit of the power first.",
             "the units digit.", "subtracting can borrow; work mod $10$.",
             [f"Units digits of ${a}^k$ cycle: {', '.join(str(pow(a, j, 10)) for j in range(1, 5))}.", f"${n} \\bmod 4 = {n % 4}$, so ${a}^{{{n}}}$ ends in ${pow(a, n, 10)}$.", f"${pow(a, n, 10)} - {k} \\equiv {ans} \\pmod{{10}}$."],
             "taking the absolute difference instead of borrowing.")


@reg(S, "basics")
def pw_mod7(r):
    a = r.choice([2, 3, 4, 5, 6])
    m = r.choice([7, 9, 11, 13])
    n = r.randint(20, 500)
    cyc, off = cycle(a, m)
    ans = pow(a, n, m)
    p = f"What is the remainder when ${a}^{{{n}}}$ is divided by ${m}$?"
    return Q(p, ans, [(ans + 1) % m, (ans + 2) % m, (a * n) % m, pow(a, n + 1, m), (ans + m - 1) % m], "List the first few remainders and find the cycle.",
             "the remainder.", "powers repeat their remainders in a cycle.",
             [f"Remainders of ${a}^1, {a}^2, \\ldots$ mod ${m}$: {', '.join(str(pow(a, k, m)) for k in range(1, len(cyc) + 2))}; cycle length ${len(cyc)}$.",
              f"${n} \\bmod {len(cyc)} = {n % len(cyc)}$, so ${a}^{{{n}}} \\equiv {a}^{{{n % len(cyc) if n % len(cyc) else len(cyc)}}} \\equiv {ans}$."],
             "an off by one when matching the exponent to the cycle.")


@reg(S, "basics")
def pw_self_power(r):
    n = r.choice([12, 13, 14, 17, 18, 19, 22, 23, 27, 28, 33, 37, 38, 43, 47])
    ans = pow(n, n, 10)
    p = f"What is the units digit of ${n}^{{{n}}}$?"
    u = n % 10
    return Q(p, ans, [u, (ans + 2) % 10, pow(u, 4, 10) if pow(u, 4, 10) != ans else (ans + 4) % 10, (ans + 5) % 10, n % 4], "Only the units digit of the base matters.",
             "the units digit.", f"${n}^{{{n}}}$ has the same units digit as ${u}^{{{n}}}$.",
             [f"Units digits of ${u}^k$: {', '.join(str(pow(u, k, 10)) for k in range(1, 5))}.", f"${n} \\bmod 4 = {n % 4}$, so the units digit is ${ans}$."], "using the exponent's last digit instead of its remainder mod $4$.")


@reg(S, "basics")
def pw_two_bases(r):
    a, b = r.sample([2, 3, 4, 7, 8, 9], 2)
    n = r.randint(10, 300)
    ans = (pow(a, n, 10) + pow(b, n, 10)) % 10
    p = f"What is the units digit of ${a}^{{{n}}} + {b}^{{{n}}}$?"
    return Q(p, ans, [pow(a, n, 10), pow(b, n, 10) if pow(b, n, 10) != pow(a, n, 10) else (ans + 3) % 10, pow(a, n, 10) * pow(b, n, 10) % 10 if pow(a, n, 10) * pow(b, n, 10) % 10 != ans else (ans + 5) % 10, (ans + 1) % 10, (ans + 2) % 10], "Find each units digit separately.",
             "the units digit.", "add the two units digits and keep the last digit.",
             [f"${a}^{{{n}}}$ ends in ${pow(a, n, 10)}$; ${b}^{{{n}}}$ ends in ${pow(b, n, 10)}$ (using ${n} \\bmod 4 = {n % 4}$).", f"Sum: ${pow(a, n, 10) + pow(b, n, 10)}$, units digit ${ans}$."],
             "multiplying the units digits.")


@reg(S, "basics")
def pw_ten_mod(r):
    n = r.randint(5, 200)
    m = r.choice([9, 11, 3])
    ans = pow(10, n, m)
    p = f"What is the remainder when $10^{{{n}}}$ is divided by ${m}$?"
    return Q(p, ans, [0, (ans + 1) % m, m - 1 if m - 1 != ans else 2, n % m if n % m != ans else (ans + 2) % m, 1 if ans != 1 else 3], "What is $10$ mod " + str(m) + "?",
             "the remainder.", f"$10 \\equiv {10 % m if 10 % m <= m // 2 else 10 % m - m} \\pmod{{{m}}}$, so powers of $10$ are easy.",
             [f"$10 \\equiv {10 % m if m != 11 else -1} \\pmod{{{m}}}$.", f"$10^{{{n}}} \\equiv {(10 % m if m != 11 else -1)}^{{{n}}} \\equiv {ans}$."], "thinking any power of $10$ is divisible by " + str(m) + ".")


@reg(S, "basics")
def pw_digits_2_5(r):
    a, b = r.randint(5, 30), r.randint(5, 30)
    N = 2 ** a * 5 ** b
    d = len(str(N))
    p = f"How many digits does $2^{{{a}}} \\cdot 5^{{{b}}}$ have?"
    k = min(a, b)
    rest = 2 ** (a - k) * 5 ** (b - k)
    return Q(p, d, [a + b, max(a, b), d + 1, d - 1, k], "Pair 2s with 5s to make tens.",
             "the digit count.", "each $2 \\cdot 5$ pair makes a factor of $10$, which just adds a zero.",
             [f"$2^{{{a}}} \\cdot 5^{{{b}}} = 10^{{{k}}} \\cdot {'2' if a > b else '5'}^{{{abs(a - b)}}}$." if a != b else f"$2^{{{a}}} \\cdot 5^{{{b}}} = 10^{{{a}}}$.",
              f"${rest}$ has ${len(str(rest))}$ digit{'s' if len(str(rest)) > 1 else ''}, plus ${k}$ zeros: ${d}$ digits."],
             "adding the exponents.")


@reg(S, "basics")
def pw_cycle_length(r):
    b = r.choice([2, 3, 4, 7, 8, 9, 12, 13, 14, 17])
    cyc = []
    k = 1
    while True:
        v = pow(b, k, 10)
        if v in cyc:
            break
        cyc.append(v)
        k += 1
    p = f"The units digits of ${b}^1, {b}^2, {b}^3, \\ldots$ repeat in a cycle. How long is the cycle?"
    return Q(p, len(cyc), [4 if len(cyc) != 4 else 2, 10, len(cyc) + 1, b % 10 if b % 10 not in (len(cyc), 4, 10, len(cyc) + 1) else 3, 1], "Write out the units digits until one repeats.",
             "the cycle length.", "only the units digit of the base matters, and each step multiplies the units digit by it.",
             [f"Units digits: {', '.join(map(str, cyc))}, then ${cyc[0]}$ again.", f"Cycle length: ${len(cyc)}$."], "assuming every cycle has length $4$.")


@reg(S, "basics")
def pw_mod6(r):
    a = r.choice([4, 5, 2, 8, 10])
    m = r.choice([6, 12, 9])
    n = r.randint(5, 200)
    ans = pow(a, n, m)
    p = f"What is the remainder when ${a}^{{{n}}}$ is divided by ${m}$?"
    return Q(p, ans, [(ans + 1) % m, a % m if a % m != ans else (ans + 2) % m, 0 if ans else 1, (ans + 3) % m, pow(a, n + 1, m) if pow(a, n + 1, m) != ans else (ans + 4) % m], "Compute the first few powers mod " + str(m) + ".",
             "the remainder.", "the remainders settle into a pattern quickly.",
             [f"Remainders: " + ", ".join(f"${a}^{{{k}}} \\equiv {pow(a, k, m)}$" for k in range(1, 5)) + ".", f"Following the pattern, ${a}^{{{n}}} \\equiv {ans}$."], "assuming the pattern starts repeating from the first term when it doesn't.")


@reg(S, "basics")
def pw_exceed(r):
    k = r.randint(2, 12)
    ans = next(n for n in range(1, 200) if 2 ** n > 10 ** k)
    p = f"What is the smallest positive integer $n$ such that $2^n > 10^{{{k}}}$?"
    return Q(p, ans, [ans - 1, ans + 1, 3 * k, 4 * k, ans + 2], "$2^{10} = 1024$ is a little more than $10^3$.",
             "the smallest $n$.", "$2^{10} \\approx 10^3$; use it to estimate, then check nearby values.",
             [f"$2^{{{ans - 1}}} = {2 ** (ans - 1)} \\le 10^{{{k}}}$.", f"$2^{{{ans}}} = {2 ** ans} > 10^{{{k}}}$."], "using $n = 3k$ exactly, which is slightly too small or too big.")


@reg(S, "basics")
def pw_nines_digit_sum(r):
    n = r.randint(5, 60)
    p = f"What is the sum of the digits of $10^{{{n}}} - 1$?"
    return Q(p, 9 * n, [9 * (n - 1), 9 * (n + 1), n, 10 * n, 9 * n + 1], "Write it out.",
             "the digit sum.", "$10^n - 1$ is a string of $n$ nines.",
             [f"$10^{{{n}}} - 1 = \\underbrace{{99\\ldots9}}_{{{n}}}$.", f"Digit sum: $9 \\cdot {n} = {9 * n}$."], "counting $n + 1$ digits.")


@reg(S, "basics")
def pw_perfect_powers(r):
    N = r.choice([100, 200, 500, 1000, 2000, 5000])
    sq, cu = math.isqrt(N), round(N ** (1 / 3))
    while cu ** 3 > N:
        cu -= 1
    while (cu + 1) ** 3 <= N:
        cu += 1
    six = 1
    while (six + 1) ** 6 <= N:
        six += 1
    ans = sq + cu - six
    p = f"How many integers from $1$ to ${N}$ are perfect squares or perfect cubes (or both)?"
    return Q(p, ans, [sq + cu, sq, ans + 1, sq + cu - 1 if sq + cu - 1 != ans else ans - 1, ans + six], "Inclusion and exclusion: numbers that are both are sixth powers.",
             "the count.", "squares plus cubes minus the overlap (sixth powers).",
             [f"Squares: ${sq}$. Cubes: ${cu}$. Sixth powers: ${six}$.", f"${sq} + {cu} - {six} = {ans}$."], "forgetting to subtract numbers counted twice.")


@reg(S, "basics")
def pw_plus_one_mod(r):
    m = r.randint(3, 20)
    n = r.randint(10, 999)
    p = f"What is the remainder when ${m + 1}^{{{n}}}$ is divided by ${m}$?"
    return Q(p, 1, [0, m - 1, n % m if n % m != 1 else 2, (m + 1) % m + 1, 2 if m > 2 else 3], "What is " + str(m + 1) + " mod " + str(m) + "?",
             "the remainder.", f"${m + 1} \\equiv 1 \\pmod{{{m}}}$, and $1$ to any power is $1$.",
             [f"${m + 1}^{{{n}}} \\equiv 1^{{{n}}} = 1 \\pmod{{{m}}}$."], "trying to compute the power.")


@reg(S, "basics")
def pw_mod7_two(r):
    n = r.randint(20, 900)
    m = 7
    ans = pow(2, n, 7)
    p = f"What is the remainder when $2^{{{n}}}$ is divided by $7$?"
    return Q(p, ans, [pow(2, n + 1, 7), pow(2, n + 2, 7), 0, (ans + 3) % 7, 6 if ans != 6 else 5], "$2^3 = 8 \\equiv 1 \\pmod{7}$.",
             "the remainder.", "$2^3 \\equiv 1$, so powers of $2$ mod $7$ repeat every $3$: $2, 4, 1$.",
             [f"${n} = 3 \\cdot {n // 3} + {n % 3}$.", f"$2^{{{n}}} = (2^3)^{{{n // 3}}} \\cdot 2^{{{n % 3}}} \\equiv 2^{{{n % 3}}} = {2 ** (n % 3)} \\equiv {ans}$."], "using a cycle of length $4$ like units digits.")


@reg(S, "basics")
def pw_trailing_zeros(r):
    a, b = r.randint(1, 15), r.randint(1, 15)
    twos, fives = 2 * a + 0 * b, a + b
    p = f"How many zeros are at the end of $20^{{{a}}} \\cdot 15^{{{b}}}$?"
    ans = min(2 * a, a + b)
    return Q(p, ans, [a + b, 2 * a, a, max(2 * a, a + b), ans + 1], "Count factors of $2$ and of $5$.",
             "the number of trailing zeros.", "each trailing zero needs one $2$ and one $5$.",
             [f"$20^{{{a}}} = 2^{{{2 * a}}} \\cdot 5^{{{a}}}$ and $15^{{{b}}} = 3^{{{b}}} \\cdot 5^{{{b}}}$.", f"Twos: ${2 * a}$. Fives: ${a + b}$.", f"Zeros: $\\min({2 * a}, {a + b}) = {ans}$."],
             "counting only the fives.")


@reg(S, "basics")
def pw_four_sum(r):
    n = r.randint(10, 400)
    s = (1 + pow(2, n, 10) + pow(3, n, 10) + pow(4, n, 10)) % 10
    p = f"What is the units digit of $1^{{{n}}} + 2^{{{n}}} + 3^{{{n}}} + 4^{{{n}}}$?"
    return Q(p, s, [4 if s != 4 else 0, (s + 1) % 10, 0 if s else 2, (s + 5) % 10, 1], "Use the cycles for $2$, $3$, $4$.",
             "the units digit.", "add the units digits of each power.",
             [f"${n} \\bmod 4 = {n % 4}$.", f"Units digits: $1, {pow(2, n, 10)}, {pow(3, n, 10)}, {pow(4, n, 10)}$.", f"Sum: ${1 + pow(2, n, 10) + pow(3, n, 10) + pow(4, n, 10)}$, units digit ${s}$."], "using the cycle for $4$ wrongly (it has length $2$).")


@reg(S, "challenge")
def pwc_tower(r):
    a = r.choice([2, 3, 7, 8])
    b, c = r.randint(2, 9), r.randint(2, 5)
    e = b ** c
    ans = pow(a, e, 10)
    p = f"What is the units digit of ${a}^{{{b}^{{{c}}}}}$?"
    return Q(p, ans, [pow(a, b * c, 10), pow(a, b, 10), (ans + 2) % 10, (ans + 5) % 10, pow(a, c, 10) if pow(a, c, 10) not in (ans, pow(a, b * c, 10), pow(a, b, 10)) else (ans + 1) % 10], "Find the exponent mod $4$.",
             "the units digit.", f"units digits of ${a}^k$ repeat every $4$, so only ${b}^{{{c}}} \\bmod 4$ matters.",
             [f"${b}^{{{c}}} = {e}$, and ${e} \\bmod 4 = {e % 4}$.", f"${a}^{{{e % 4 if e % 4 else 4}}}$ ends in ${ans}$."], "multiplying the exponents ($" + f"{b} \\cdot {c}" + "$) instead of raising.")


@reg(S, "challenge")
def pwc_euler(r):
    m = r.choice([11, 13, 17, 19])
    a = r.randint(2, 9)
    n = r.randint(100, 2000)
    ans = pow(a, n, m)
    p = f"What is the remainder when ${a}^{{{n}}}$ is divided by ${m}$?"
    return Q(p, ans, [(ans + 1) % m, pow(a, n % m, m) if pow(a, n % m, m) != ans else (ans + 2) % m, (a * n) % m, 1 if ans != 1 else m - 1, (ans + m - 1) % m], "Fermat's Little Theorem.",
             "the remainder.", f"Fermat's Little Theorem: ${a}^{{{m - 1}}} \\equiv 1 \\pmod{{{m}}}$, so reduce the exponent mod ${m - 1}$.",
             [f"${n} = {m - 1} \\cdot {n // (m - 1)} + {n % (m - 1)}$.", f"${a}^{{{n}}} \\equiv {a}^{{{n % (m - 1)}}} = {a ** (n % (m - 1))} \\equiv {ans} \\pmod{{{m}}}$."], "reducing the exponent mod " + str(m) + " instead of " + str(m - 1) + ".")


@reg(S, "challenge")
def pwc_last_two_2(r):
    n = r.randint(20, 500)
    ans = pow(2, n, 100)
    p = f"What are the last two digits of $2^{{{n}}}$? (Give the two-digit number they form.)"
    return Q(p, ans, [pow(2, n + 1, 100), pow(2, n % 20, 100) if pow(2, n % 20, 100) != ans else (ans + 4) % 100, (ans + 50) % 100, pow(2, n, 10) * 11 % 100 if pow(2, n, 10) * 11 % 100 != ans else (ans + 8) % 100, (ans + 20) % 100], "From $2^2$ on, the last two digits repeat every $20$.",
             "the last two digits.", "mod $100$, powers of $2$ (from $2^2$) repeat with period $20$, because $2^{22} \\equiv 2^2$.",
             [f"Reduce the exponent: ${n} \\equiv {(n - 2) % 20 + 2} \\pmod{{20}}$ (keeping it at least $2$).", f"$2^{{{(n - 2) % 20 + 2}}} = {2 ** ((n - 2) % 20 + 2)}$, ending in ${ans:02d}$."], "using a period of $4$ (that's only for the last digit).")


@reg(S, "challenge")
def pwc_count_units(r):
    N = r.randint(20, 500)
    a = r.choice([3, 7, 9, 2, 8])
    target = r.choice(sorted({pow(a, k, 10) for k in range(1, 5)}))
    ans = sum(1 for n in range(1, N + 1) if pow(a, n, 10) == target)
    p = f"For how many $n$ from $1$ to ${N}$ does ${a}^n$ end in the digit ${target}$?"
    per = len({pow(a, k, 10) for k in range(1, 5)})
    return Q(p, ans, [N // 4, N // per + 1 if N // per + 1 != ans else ans + 2, ans + 1, ans - 1, N // 2], "Find the cycle and where " + str(target) + " sits in it.",
             "the count.", "the units digit cycles; count how many $n$ land on the right spot.",
             [f"Units digits of ${a}^n$: {', '.join(str(pow(a, k, 10)) for k in range(1, 5))}, repeating.", f"Positions with ${target}$: every ${per}$ terms, starting at $n = {next(k for k in range(1, 5) if pow(a, k, 10) == target)}$.", f"Up to ${N}$: ${ans}$."],
             "dividing by $4$ regardless of where the digit sits in the cycle.")


@reg(S, "challenge")
def pwc_digit_sum_25(r):
    a, b = r.randint(3, 15), r.randint(3, 15)
    N = 2 ** a * 5 ** b
    ans = sum(map(int, str(N)))
    k = min(a, b)
    rest = 2 ** (a - k) * 5 ** (b - k)
    p = f"What is the sum of the digits of $2^{{{a}}} \\cdot 5^{{{b}}}$?"
    return Q(p, ans, [a + b, ans + 1, 2 * a + 5 * b if 2 * a + 5 * b != ans else ans + 3, k, sum(map(int, str(2 ** a))) + sum(map(int, str(5 ** b)))], "Make tens.",
             "the digit sum.", "the factors of $10$ only add zeros, which don't change the digit sum.",
             [f"$2^{{{a}}} \\cdot 5^{{{b}}} = {rest} \\cdot 10^{{{k}}}$.", f"Digit sum of ${rest}$: ${ans}$."], "adding the digit sums of the two powers separately.")


@reg(S, "challenge")
def pwc_lte(r):
    n = r.choice([2, 4, 6, 8, 10, 12, 16, 20, 24, 32])
    v = 3 ** n - 1
    k = 0
    while v % 2 == 0:
        v //= 2
        k += 1
    p = f"What is the largest integer $k$ such that $2^k$ divides $3^{{{n}}} - 1$?"
    return Q(p, k, [k + 1, k - 1, n, n + 1 if n + 1 != k else n + 2, 2], "Factor using difference of squares repeatedly.",
             "the exponent of $2$.", "for even $n$, the power of $2$ in $3^n - 1$ is (power of $2$ in $n$) $+ 2$.",
             [f"Example: $3^2 - 1 = 8 = 2^3$. Each time the exponent doubles, $3^{{2m}} - 1 = (3^m - 1)(3^m + 1)$ and $3^m + 1$ adds exactly one factor of $2$.", f"For $n = {n}$: $k = {k}$."],
             "assuming the power of $2$ equals $n$.")


@reg(S, "challenge")
def pwc_squares_end6(r):
    N = r.randint(100, 2000)
    ans = sum(1 for k in range(1, math.isqrt(N - 1) + 1) if (k * k) % 10 == 6)
    p = f"How many perfect squares less than ${N}$ end in the digit $6$?"
    return Q(p, ans, [math.isqrt(N - 1) // 5, ans + 1, ans - 1, math.isqrt(N - 1) // 10, 2 * ans + 1], "A square ends in $6$ exactly when its root ends in $4$ or $6$.",
             "the count.", "the units digit of $k^2$ depends only on the units digit of $k$: $4^2 = 16$ and $6^2 = 36$.",
             [f"Roots go up to $\\lfloor \\sqrt{{{N - 1}}} \\rfloor = {math.isqrt(N - 1)}$.", f"Roots ending in $4$ or $6$: ${ans}$."], "counting only roots ending in $4$.")


# ================================================================ nt_bases
S = "nt_bases"


@reg(S, "basics")
def ba_to_dec(r):
    b = r.randint(3, 9)
    n = r.randint(b ** 2, b ** 4)
    s = to_base(n, b)
    p = f"What is ${s}_{{{b}}}$ in base ten?"
    return Q(p, n, [int(s), n + b, n - 1, int(s, b + 1) if all(int(c) <= b for c in s) else n + 2, n + 1], "Multiply each digit by its place value.",
             "the base-ten value.", f"place values in base ${b}$ are $1, {b}, {b * b}, \\ldots$",
             [" + ".join(f"{c} \\cdot {b}^{{{len(s) - 1 - i}}}" for i, c in enumerate(s)).join(["$", f" = {n}$."])], "reading the digits as a base-ten number.")


@reg(S, "basics")
def ba_binary_ones(r):
    n = r.randint(20, 1000)
    s = to_base(n, 2)
    ans = s.count("1")
    p = f"When ${n}$ is written in base $2$, how many of its digits are $1$?"
    return Q(p, ans, [len(s), len(s) - ans, ans + 1, ans - 1 if ans > 1 else 4, sum(map(int, str(n)))], "Write " + str(n) + " as a sum of powers of $2$.",
             "the number of 1s.", "each $1$ in binary is one power of $2$ in the sum.",
             [f"${n} = " + " + ".join(f"2^{{{len(s) - 1 - i}}}" for i, c in enumerate(s) if c == "1") + "$.", f"Binary: ${s}_2$, with ${ans}$ ones."], "counting all the digits.")


@reg(S, "basics")
def ba_subtract(r):
    b = r.randint(4, 9)
    x, y = sorted(r.sample(range(b ** 2, b ** 3), 2))
    p = f"In base ${b}$, what is ${to_base(y, b)}_{{{b}}} - {to_base(x, b)}_{{{b}}}$?"
    ans = bchoice(y - x, b)
    wrong = [bchoice(y - x + 1, b), bchoice(y - x - 1, b) if y - x > 1 else bchoice(y - x + 2, b), C(f"{int(to_base(y, b)) - int(to_base(x, b))}_{{{b}}}", 10 ** 6 + 1) if str(int(to_base(y, b)) - int(to_base(x, b))) != to_base(y - x, b) else bchoice(y - x + b, b), bchoice(y - x + b, b) if y - x + b != y - x + 2 else bchoice(y - x + 3, b)]
    return Q(p, ans, bwrong(ans, b, wrong), "Convert to base ten, subtract, convert back; or borrow " + str(b) + " instead of 10.",
             "the difference in base " + str(b) + ".", f"in base ${b}$, borrowing gives ${b}$, not $10$.",
             [f"${to_base(y, b)}_{{{b}}} = {y}$ and ${to_base(x, b)}_{{{b}}} = {x}$.", f"${y} - {x} = {y - x} = {to_base(y - x, b)}_{{{b}}}$."], "borrowing $10$ as if in base ten.", sort=False)


@reg(S, "basics")
def ba_multiply(r):
    b = r.randint(4, 9)
    x, y = r.randint(2, b - 1), r.randint(b, b * b - 1)
    p = f"In base ${b}$, what is ${to_base(y, b)}_{{{b}}} \\times {x}$?"
    ans = bchoice(x * y, b)
    wrong = [bchoice(x * y + 1, b), bchoice(x * y - 1, b), bchoice(x * y + b, b), C(f"{x * int(to_base(y, b))}_{{{b}}}", 10 ** 6 + 2) if str(x * int(to_base(y, b))) != to_base(x * y, b) else bchoice(x * y + 2 * b, b)]
    return Q(p, ans, bwrong(ans, b, wrong), "Work in base ten, then convert.",
             "the product in base " + str(b) + ".", "convert, multiply, and convert back.",
             [f"${to_base(y, b)}_{{{b}}} = {y}$.", f"${y} \\cdot {x} = {x * y} = {to_base(x * y, b)}_{{{b}}}$."], "multiplying the digits as if in base ten.", sort=False)


@reg(S, "basics")
def ba_largest_3digit(r):
    b = r.randint(3, 9)
    k = r.choice([2, 3, 4])
    ans = b ** k - 1
    p = f"What is the largest ${k}$-digit number in base ${b}$, written in base ten?"
    return Q(p, ans, [b ** k, b ** (k - 1), int(str(b - 1) * k), ans - 1, b ** k - b], "It's all digits " + str(b - 1) + ".",
             "the largest " + str(k) + "-digit base-" + str(b) + " number.", f"the largest digit is ${b - 1}$; and ${str(b - 1) * k}_{{{b}}}$ is one less than $1{'0' * k}_{{{b}}} = {b}^{{{k}}}$.",
             [f"${str(b - 1) * k}_{{{b}}} = {b}^{{{k}}} - 1 = {ans}$."], "reading the $" + str(b - 1) + "$s as a base-ten number.")


@reg(S, "basics")
def ba_bin_to_oct(r):
    n = r.randint(64, 4000)
    s2 = to_base(n, 2)
    p = f"What is ${s2}_2$ written in base $8$?"
    ans = bchoice(n, 8)
    wrong = [bchoice(n + 1, 8), bchoice(n - 8, 8), bchoice(n + 8, 8), C(f"{to_base(n, 4)}_{{8}}", 10 ** 6 + 3) if to_base(n, 4) != to_base(n, 8) else bchoice(n + 64, 8)]
    groups = []
    s = s2.zfill((len(s2) + 2) // 3 * 3)
    for i in range(0, len(s), 3):
        groups.append(s[i:i + 3])
    return Q(p, ans, bwrong(ans, 8, wrong), "Group binary digits in threes from the right.",
             "the base-8 form.", "$8 = 2^3$, so each group of three binary digits becomes one base-8 digit.",
             [f"Groups: {' | '.join(groups)}.", f"Each group: {', '.join(str(int(g, 2)) for g in groups)}. So ${to_base(n, 8)}_8$."], "grouping from the left.", sort=False)


@reg(S, "basics")
def ba_hex(r):
    n = r.randint(200, 5000)
    s = to_base(n, 16)
    if not any(c.isalpha() for c in s):
        return None
    p = f"In base $16$ the digits $A$ through $F$ stand for $10$ through $15$. What is ${s}_{{16}}$ in base ten?"
    return Q(p, n, [n + 16, n - 16, n + 1, sum(int(c, 16) for c in s), int(s, 16) - 10 * 16 ** (len(s) - 1) if int(s, 16) - 10 * 16 ** (len(s) - 1) > 0 else n + 256], "Place values are $1, 16, 256, \\ldots$",
             "the base-ten value.", "multiply each digit by its power of $16$.",
             [" + ".join(f"{int(c, 16)} \\cdot 16^{{{len(s) - 1 - i}}}" for i, c in enumerate(s)).join(["$", f" = {n}$."])], "treating a letter digit as $1$.")


@reg(S, "basics")
def ba_count_kdigit(r):
    b = r.randint(3, 9)
    k = r.randint(2, 4)
    ans = (b - 1) * b ** (k - 1)
    p = f"How many positive integers have exactly ${k}$ digits when written in base ${b}$?"
    return Q(p, ans, [b ** k, b ** k - 1, (b - 1) ** k, b ** (k - 1), ans + 1], "The first digit can't be $0$.",
             "the count.", f"first digit: ${b - 1}$ choices; each other digit: ${b}$ choices.",
             [f"${b - 1} \\cdot {b}^{{{k - 1}}} = {ans}$."], "letting the first digit be $0$.")


@reg(S, "basics")
def ba_last_digit(r):
    b = r.randint(3, 9)
    n = r.randint(100, 5000)
    p = f"What is the last digit of ${n}$ when it is written in base ${b}$?"
    return Q(p, n % b, [(n % b + 1) % b, n % 10 if n % 10 != n % b else (n % b + 2) % b, int(to_base(n, b)[0]) if int(to_base(n, b)[0]) != n % b else (n % b + 3) % b, b - 1 if b - 1 != n % b else 0], "The last digit is the remainder.",
             "the last base-" + str(b) + " digit.", f"the last digit in base ${b}$ is the remainder when dividing by ${b}$.",
             [f"${n} = {b} \\cdot {n // b} + {n % b}$.", f"Last digit: ${n % b}$. (Full form: ${to_base(n, b)}_{{{b}}}$.)"], "giving the first digit.")


@reg(S, "basics")
def ba_base3_digit_sum(r):
    n = r.randint(30, 2000)
    s = to_base(n, 3)
    ans = sum(map(int, s))
    p = f"What is the sum of the digits of ${n}$ when written in base $3$?"
    return Q(p, ans, [ans + 1, ans - 1, len(s), sum(map(int, str(n))), ans + 2], "Convert to base 3 first.",
             "the digit sum.", "find the base-3 digits by repeated division by $3$.",
             [f"${n} = {s}_3$.", f"Digit sum: ${' + '.join(s)} = {ans}$."], "adding the base-ten digits.")


@reg(S, "basics")
def ba_four_to_two(r):
    n = r.randint(20, 2000)
    s4 = to_base(n, 4)
    p = f"What is ${s4}_4$ written in base $2$?"
    ans = bchoice(n, 2)
    wrong = [bchoice(n + 1, 2), bchoice(n - 1, 2), bchoice(n * 2, 2), bchoice(n // 2, 2) if n // 2 != n - 1 else bchoice(n + 2, 2)]
    return Q(p, ans, bwrong(ans, 2, wrong), "Each base-4 digit becomes two binary digits.",
             "the binary form.", "$4 = 2^2$, so replace each base-4 digit with its 2-digit binary form.",
             [f"Digits: {', '.join(s4)} $\\to$ {', '.join(to_base(int(c), 2).zfill(2) for c in s4)}.", f"Result: ${to_base(n, 2)}_2$ (dropping a leading zero)."], "converting each digit to one binary digit.", sort=False)


@reg(S, "basics")
def ba_smallest_base(r):
    digits = [r.randint(1, 8)] + [r.randint(0, 8) for _ in range(r.randint(2, 3))]
    s = "".join(map(str, digits))
    ans = max(digits) + 1
    if ans < 3:
        return None
    p = f"The number ${s}$ is written in some base $b$. What is the smallest possible value of $b$?"
    return Q(p, ans, [max(digits), ans + 1, 10, len(s), sum(digits)], "Every digit must be less than the base.",
             "the smallest base.", "in base $b$, digits run from $0$ to $b - 1$.",
             [f"Largest digit: ${max(digits)}$.", f"So $b \\ge {ans}$."], "using the largest digit itself as the base.")


@reg(S, "basics")
def ba_base5_digit_sum(r):
    n = r.randint(50, 3000)
    s = to_base(n, 5)
    p = f"When ${n}$ is written in base $5$, what is its leading (leftmost) digit?"
    ans = int(s[0])
    return Q(p, ans, [n % 5 if n % 5 != ans else (ans + 1) % 5, len(s), int(str(n)[0]) if int(str(n)[0]) != ans and int(str(n)[0]) < 5 else (ans + 2) % 5, (ans + 3) % 5, 4 if ans != 4 else 1], "Find the largest power of $5$ that fits.",
             "the leading digit.", "the leading digit is how many times the largest power of $5$ (at most the number) fits.",
             [f"Powers of $5$: $1, 5, 25, 125, 625, 3125$. The largest at most ${n}$ is ${5 ** (len(s) - 1)}$.", f"${n} \\div {5 ** (len(s) - 1)} = {n // 5 ** (len(s) - 1)}$ (rounded down). Full form: ${s}_5$."], "giving the last digit.")


@reg(S, "basics")
def ba_ones_binary(r):
    a, b = sorted(r.sample(range(2, 15), 2), reverse=True)
    n = 2 ** a + 2 ** b - 1
    ans = to_base(n, 2).count("1")
    p = f"How many $1$s are in the base-$2$ form of $2^{{{a}}} + 2^{{{b}}} - 1$?"
    return Q(p, ans, [2, b, a, ans + 1, a + b], "What does $2^b - 1$ look like in binary?",
             "the number of 1s.", "$2^b - 1$ is $b$ ones in binary; adding $2^a$ puts one more $1$ higher up.",
             [f"$2^{{{b}}} - 1 = \\underbrace{{11\\ldots1}}_{{{b}}}{{}}_2$.", f"Adding $2^{{{a}}}$ (a single $1$ in position ${a}$) gives ${b + 1}$ ones."], "counting $2$ (one for each power).")


@reg(S, "basics")
def ba_fraction(r):
    b = r.randint(2, 9)
    d1, d2 = r.randint(0, b - 1), r.randint(1, b - 1)
    ans = F(d1, b) + F(d2, b * b)
    p = f"What is $0.{d1}{d2}_{{{b}}}$ as a fraction in base ten?"
    return Q(p, ans, [F(d1 * 10 + d2, 100), F(d1 * b + d2, b), ans + F(1, b * b), F(d2, b) + F(d1, b * b) if d1 != d2 else ans * 2, F(d1 + d2, b)], "Places after the point are $\\frac{1}{b}, \\frac{1}{b^2}, \\ldots$",
             "the value.", f"in base ${b}$ the first place after the point is $\\frac{{1}}{{{b}}}$ and the second is $\\frac{{1}}{{{b * b}}}$.",
             [f"$\\frac{{{d1}}}{{{b}}} + \\frac{{{d2}}}{{{b * b}}} = {ftex(ans)}$."], "treating it as a base-ten decimal.")


@reg(S, "basics")
def ba_compare(r):
    target = r.randint(30, 200)
    reps = []
    for bb in r.sample([2, 3, 4, 5, 6, 7, 8, 9], 5):
        reps.append((bb, target + r.randint(-25, 25)))
    vals = [v for _, v in reps]
    if len(set(vals)) < 5:
        return None
    best = max(reps, key=lambda t: t[1])
    p = "Which of these is largest?"
    return Q(p, bchoice(best[1], best[0]), [bchoice(v, bb) for bb, v in reps if (bb, v) != best], "Convert each to base ten.",
             "the largest value.", "compare values only after converting to base ten.",
             ["Values: " + ", ".join(f"${to_base(v, bb)}_{{{bb}}} = {v}$" for bb, v in reps) + ".", f"Largest: ${to_base(best[1], best[0])}_{{{best[0]}}}$."], "comparing the digit strings directly.", sort=False)


@reg(S, "challenge")
def bac_121(r):
    b = r.randint(3, 20)
    n = (b + 1) ** 2
    p = f"In some base $b$, the number written $121_b$ equals ${n}$ in base ten. What is $b$?"
    return Q(p, b, [b + 1, b - 1, math.isqrt(n), F(n - 1, 2), b + 2], "$121_b = b^2 + 2b + 1$.",
             "$b$.", "$121_b = b^2 + 2b + 1 = (b + 1)^2$.",
             [f"$(b + 1)^2 = {n}$, so $b + 1 = {b + 1}$.", f"$b = {b}$."], "answering $b + 1$.")


@reg(S, "challenge")
def bac_mult_base(r):
    b = r.randint(5, 12)
    a, c = r.randint(2, b - 1), r.randint(2, b - 1)
    prod = a * c
    if prod < b:
        return None
    d1, d2 = prod // b, prod % b
    if d1 >= b or d1 >= 10 or d2 >= 10:
        return None
    p = f"In some base $b$, the multiplication ${a} \\times {c} = {d1}{d2}_b$ is correct. What is $b$?"
    return Q(p, b, [b + 1, b - 1, prod - d2, prod, 10], "Write $" + f"{d1}{d2}_b" + "$ in base ten.",
             "$b$.", f"${d1}{d2}_b = {d1}b + {d2}$.",
             [f"${a} \\cdot {c} = {prod}$.", f"${d1}b + {d2} = {prod}$, so $b = \\frac{{{prod - d2}}}{{{d1}}} = {b}$."], "assuming the base is $10$.")


def bac_trailing_base6(r):  # not registered: nt_bases already has 10 challenge types
    a, b = r.randint(2, 20), r.randint(2, 20)
    p = f"How many zeros are at the end of $2^{{{a}}} \\cdot 3^{{{b}}}$ when it is written in base $6$?"
    return Q(p, min(a, b), [max(a, b), a + b, min(a, b) + 1, abs(a - b) if abs(a - b) != min(a, b) else min(a, b) - 1, F(a + b, 2) if F(a + b, 2) != min(a, b) else min(a, b) + 2], "Each zero in base 6 is a factor of $6 = 2 \\cdot 3$.",
             "the number of trailing zeros.", "trailing zeros in base $6$ count factors of $6$, each needing one $2$ and one $3$.",
             [f"Pairs of $2$ and $3$: $\\min({a}, {b}) = {min(a, b)}$."], "adding the exponents.")


@reg(S, "challenge")
def bac_bit_sum(r):
    k = r.randint(3, 12)
    ans = k * 2 ** (k - 1)
    p = f"Each integer from $1$ to $2^{{{k}}} - 1$ is written in base $2$. How many $1$s are written in all?"
    return Q(p, ans, [2 ** k - 1, k * 2 ** k, ans + 1, 2 ** (k - 1), k * (2 ** k - 1)], "Count by position.",
             "the total number of 1s.", f"include $0$ (which has no 1s): the numbers $0$ to $2^{{{k}}} - 1$ are every ${k}$-bit string. In each position, exactly half have a $1$.",
             [f"There are $2^{{{k}}}$ strings; each of the ${k}$ positions has $2^{{{k - 1}}}$ ones.", f"Total: ${k} \\cdot {2 ** (k - 1)} = {ans}$."], "counting the numbers instead of the 1s.")


@reg(S, "challenge")
def bac_palindromes(r):
    N = r.randint(30, 300)
    xs = [n for n in range(1, N + 1) if to_base(n, 2) == to_base(n, 2)[::-1]]
    p = f"How many integers from $1$ to ${N}$ are palindromes when written in base $2$?"
    return Q(p, len(xs), [len(xs) + 1, len(xs) - 1, len([n for n in range(1, N + 1) if str(n) == str(n)[::-1]]), int(math.log2(N)) * 2, len(xs) + 3], "Count palindromes by length.",
             "the count.", "a binary palindrome of length $L$ starts and ends with $1$ and is fixed by its first half.",
             [f"Lengths $1$ to ${len(to_base(N, 2))}$: a palindrome of length $L$ has $2^{{\\lceil L/2 \\rceil - 1}}$ choices.", "Count the full lengths, then check the longest length against " + str(N) + f": total ${len(xs)}$."],
             "allowing a leading zero.")


@reg(S, "challenge")
def bac_repeating(r):
    b = r.randint(3, 9)
    d1, d2 = r.randint(0, b - 1), r.randint(0, b - 1)
    if d1 == d2:
        return None
    val = F(d1 * b + d2, b * b - 1)
    p = f"What is $0.\\overline{{{d1}{d2}}}_{{{b}}}$ (the block ${d1}{d2}$ repeating forever in base ${b}$) as a fraction in base ten?"
    return Q(p, val, [F(d1 * 10 + d2, 99), F(d1 * b + d2, b * b), val + F(1, b * b - 1), F(d1 + d2, b - 1) if F(d1 + d2, b - 1) != val else val * 2, F(d2 * b + d1, b * b - 1) if d2 * b + d1 != d1 * b + d2 else val + 1], "Multiply by $b^2$ and subtract.",
             "the value.", f"the repeating block is ${d1}{d2}_{{{b}}} = {d1 * b + d2}$; dividing by $b^2 - 1$ gives the value (like $\\frac{{\\text{{block}}}}{{99}}$ in base ten).",
             [f"Let $x = 0.\\overline{{{d1}{d2}}}_{{{b}}}$. Then ${b * b}x = {d1}{d2}_{{{b}}} + x = {d1 * b + d2} + x$.", f"${b * b - 1}x = {d1 * b + d2}$, so $x = {ftex(val)}$."], "dividing by $99$ as in base ten.")


@reg(S, "challenge")
def bac_ends_in_one(r):
    N = r.randint(20, 300)
    bases = [bb for bb in range(2, N) if N % bb == 1]
    p = f"For how many bases $b \\ge 2$ does ${N}$, written in base $b$, end in the digit $1$?"
    return Q(p, len(bases), [ndiv(N - 1), len(bases) + 1, len(bases) - 1 if bases else 2, ndiv(N), N - 2], "Ending in $1$ means remainder $1$.",
             "the count of bases.", f"${N}$ ends in $1$ in base $b$ exactly when $b$ divides ${N - 1}$ (and $b \\ge 2$).",
             [f"${N - 1} = {ftex_fact(N - 1) if N - 1 > 1 else '1'}$ has ${ndiv(N - 1)}$ divisors.", f"Excluding $1$: ${len(bases)}$ bases."], "including $b = 1$.")


@reg(S, "challenge")
def bac_reversed(r):
    pairs = [(n, b1, b2) for b1 in range(3, 10) for b2 in range(3, 10) if b1 != b2 for a in range(1, min(b1, b2)) for c in range(1, min(b1, b2)) for n in [a * b1 + c] if n == c * b2 + a and a != c]
    if not pairs:
        return None
    n, b1, b2 = r.choice(pairs)
    s1 = to_base(n, b1)
    p = f"A number is written $\\overline{{AB}}$ in base ${b1}$ and $\\overline{{BA}}$ in base ${b2}$, where $A$ and $B$ are digits. What is the number in base ten?"
    others = [m for m, x, y in pairs if (x, y) == (b1, b2) and m != n]
    if others:
        return None
    return Q(p, n, [n + 1, int(s1), n + b1, n - 1, b1 * b2], "Write both forms as equations.",
             "the number.", f"$\\overline{{AB}}_{{{b1}}} = {b1}A + B$ and $\\overline{{BA}}_{{{b2}}} = {b2}B + A$.",
             [f"${b1}A + B = {b2}B + A$, so ${b1 - 1}A = {b2 - 1}B$.", f"With digits valid in both bases: $A = {s1[0]}$, $B = {s1[1]}$.", f"Number: ${b1} \\cdot {s1[0]} + {s1[1]} = {n}$."], "mixing up which digit is in which place.")


# ================================================================ nt_factorials
S = "nt_factorials"


@reg(S, "basics")
def fc_units_sum(r):
    n = r.randint(4, 100)
    ans = sum(math.factorial(k) for k in range(1, min(n, 5) + 1)) % 10
    p = f"What is the units digit of $1! + 2! + 3! + \\cdots + {n}!$?"
    return Q(p, ans, [0, (ans + 1) % 10, (ans + 5) % 10, 9, 1 if ans != 1 else 7], "From $5!$ on, every factorial ends in $0$.",
             "the units digit.", "$5!$ and beyond contain $2 \\cdot 5 = 10$, so they end in $0$.",
             [f"$1! + 2! + 3! + 4! = 1 + 2 + 6 + 24 = 33$.", f"Units digit: ${ans}$."], "trying to add all the factorials.")


@reg(S, "basics")
def fc_power2(r):
    n = r.randint(10, 100)
    ans = vp(n, 2)
    p = f"What is the largest power of $2$ that divides ${n}!$? (Give the exponent.)"
    terms = []
    q = 2
    while q <= n:
        terms.append(f"\\left\\lfloor \\frac{{{n}}}{{{q}}} \\right\\rfloor")
        q *= 2
    return Q(p, ans, [n // 2, ans + 1, ans - 1, vp(n, 5), n], "Count multiples of $2$, $4$, $8$, ...",
             "the exponent of $2$.", "Legendre's formula: add $\\lfloor n/2 \\rfloor + \\lfloor n/4 \\rfloor + \\lfloor n/8 \\rfloor + \\cdots$",
             [" + ".join(terms).join(["$", "$"]) + ".", " + ".join(str(n // 2 ** k) for k in range(1, len(terms) + 1)) .join(["$", f" = {ans}$."])], "counting only the multiples of $2$.")


@reg(S, "basics")
def fc_diff_ratio(r):
    n = r.randint(3, 50)
    p = f"What is $\\dfrac{{({n} + 1)! - {n}!}}{{{n}!}}$?"
    return Q(p, n, [n + 1, 1, n - 1, math.factorial(n) if n < 6 else 2 * n, n * n], "Factor out $" + str(n) + "!$.",
             "the value.", "$(n + 1)! = (n + 1) \\cdot n!$.",
             [f"$({n + 1})! - {n}! = {n}!({n + 1} - 1) = {n} \\cdot {n}!$.", f"Divide by ${n}!$: ${n}$."], "answering $n + 1$.")


@reg(S, "basics")
def fc_digits(r):
    n = r.randint(6, 15)
    ans = len(str(math.factorial(n)))
    p = f"How many digits does ${n}!$ have?"
    return Q(p, ans, [ans + 1, ans - 1, n, ans + 2, n // 2 + 1], "Compute it, or estimate step by step.",
             "the digit count.", "multiply it out carefully.",
             [f"${n}! = {math.factorial(n)}$.", f"Digits: ${ans}$."], "counting trailing zeros only.")


@reg(S, "basics")
def fc_smallest_prime_power(r):
    pr = r.choice([3, 5, 7])
    k = r.randint(3, 8)
    ans = next(n for n in range(1, 200) if vp(n, pr) >= k)
    p = f"What is the smallest positive integer $n$ such that ${n if False else ''}n!$ is divisible by ${pr}^{{{k}}}$?"
    return Q(p, ans, [pr * k, ans - pr if ans > pr else ans + 1, ans + pr, pr ** k, ans + 1], "Each multiple of " + str(pr) + " adds at least one factor; multiples of " + str(pr * pr) + " add two.",
             "the smallest $n$.", "count factors of " + str(pr) + " in $n!$ with Legendre's formula as $n$ grows.",
             [f"${ans}!$ has $\\left\\lfloor \\frac{{{ans}}}{{{pr}}} \\right\\rfloor + \\left\\lfloor \\frac{{{ans}}}{{{pr * pr}}} \\right\\rfloor = {vp(ans, pr)}$ factors of ${pr}$, which is at least ${k}$.", f"${ans - 1}!$ has only ${vp(ans - 1, pr)}$."],
             "answering $" + f"{pr} \\cdot {k}" + "$, which ignores extra factors from " + str(pr * pr) + ".")


@reg(S, "basics")
def fc_falling(r):
    n = r.randint(5, 30)
    val = n * (n - 1) * (n - 2)
    p = f"For what positive integer $n$ is $\\dfrac{{n!}}{{(n - 3)!}} = {val}$?"
    return Q(p, n, [n - 1, n + 1, n - 2, round(val ** (1 / 3)) + 2 if round(val ** (1 / 3)) + 2 != n else n + 2, 3], "The fraction is a product of three consecutive integers.",
             "$n$.", "$\\frac{n!}{(n - 3)!} = n(n - 1)(n - 2)$.",
             [f"$n(n - 1)(n - 2) = {val}$.", f"$\\sqrt[3]{{{val}}} \\approx {val ** (1 / 3):.1f}$, so try around there: ${n} \\cdot {n - 1} \\cdot {n - 2} = {val}$.", f"$n = {n}$."],
             "taking the cube root and stopping, which gives the middle factor.")


@reg(S, "basics")
def fc_prime_count(r):
    n = r.randint(10, 60)
    ans = sum(1 for k in range(2, n + 1) if is_prime(k))
    p = f"How many different primes divide ${n}!$?"
    return Q(p, ans, [ans + 1, ans - 1, n // 2, vp(n, 2), ans + 2], "Which primes appear as factors in $1 \\cdot 2 \\cdots n$?",
             "the number of prime divisors.", "a prime divides $n!$ exactly when it is at most $n$.",
             [f"Primes up to ${n}$: {', '.join(str(k) for k in range(2, n + 1) if is_prime(k))}.", f"Count: ${ans}$."], "counting primes with multiplicity.")


@reg(S, "basics")
def fc_zeros_product(r):
    a, b = r.randint(10, 60), r.randint(10, 60)
    ans = min(vp(a, 2) + vp(b, 2), vp(a, 5) + vp(b, 5))
    p = f"How many zeros are at the end of ${a}! \\cdot {b}!$?"
    return Q(p, ans, [vp(a, 5), vp(b, 5), ans + 1, vp(a + b, 5), vp(a * b, 5) if vp(a * b, 5) != ans else ans + 2], "Count factors of $5$ in each factorial and add.",
             "the number of trailing zeros.", "zeros come from pairs of $2$ and $5$; there are always more $2$s, so count the $5$s.",
             [f"Fives in ${a}!$: ${vp(a, 5)}$. Fives in ${b}!$: ${vp(b, 5)}$.", f"Total: ${vp(a, 5) + vp(b, 5)}$ (and there are plenty of $2$s)."], "using $" + f"({a} + {b})!" + "$ instead.")


@reg(S, "basics")
def fc_digit_sum(r):
    n = r.randint(6, 12)
    ans = sum(map(int, str(math.factorial(n))))
    p = f"What is the sum of the digits of ${n}!$?"
    return Q(p, ans, [ans + 9, ans - 9, ans + 1, n * (n + 1) // 2, ans * 2], "Compute it.",
             "the digit sum.", f"for $n \\ge 6$, $n!$ is divisible by $9$, so the digit sum is a multiple of $9$ (a good check).",
             [f"${n}! = {math.factorial(n)}$.", f"Digit sum: ${ans}$."], "adding $1 + 2 + \\cdots + " + str(n) + "$.")


@reg(S, "basics")
def fc_square_zeros(r):
    n = r.randint(10, 100)
    ans = 2 * vp(n, 5)
    p = f"How many zeros are at the end of $({n}!)^2$?"
    return Q(p, ans, [vp(n, 5), ans + 1, vp(n * n, 5), vp(2 * n, 5), ans * 2], "Squaring doubles every exponent.",
             "the number of trailing zeros.", "count the $5$s in $" + str(n) + "!$, then double.",
             [f"Fives in ${n}!$: ${vp(n, 5)}$.", f"In the square: ${ans}$."], "using $(" + str(n * n) + ")!$.")


@reg(S, "basics")
def fc_divisor_count(r):
    n = r.randint(5, 10)
    ans = ndiv(math.factorial(n))
    p = f"How many positive divisors does ${n}!$ have?"
    return Q(p, ans, [ans + 2, math.factorial(n) // 10 if math.factorial(n) // 10 != ans else ans * 2, ans - 2, n * n, 2 ** n], "Factor $" + str(n) + "!$ into primes.",
             "the divisor count.", "use the prime factorization and multiply (exponent $+ 1$).",
             [f"${n}! = {ftex_fact(math.factorial(n))}$.", "Divisors: " + " \\cdot ".join(f"({e} + 1)" for e in factorint(math.factorial(n)).values()).join(["$", f" = {ans}$."])], "multiplying the exponents instead of the exponents plus one.")


@reg(S, "basics")
def fc_gcd(r):
    a, b = r.sample(range(3, 9), 2)
    ans = math.factorial(min(a, b))
    p = f"What is $\\gcd({a}!, {b}!)$?"
    return Q(p, ans, [math.factorial(max(a, b)), min(a, b), ans * 2, math.factorial(abs(a - b)), ans // 2 if ans > 2 else 5], "The smaller factorial divides the larger.",
             "the GCD.", f"${min(a, b)}!$ divides ${max(a, b)}!$, so it is the GCD.",
             [f"${max(a, b)}! = {max(a, b)} \\cdots {min(a, b) + 1} \\cdot {min(a, b)}!$.", f"GCD $= {min(a, b)}! = {ans}$."], "giving the larger factorial.")


@reg(S, "basics")
def fc_small_sum(r):
    n = r.randint(3, 7)
    ans = sum(math.factorial(k) for k in range(0, n + 1))
    p = f"What is $0! + 1! + 2! + \\cdots + {n}!$?"
    return Q(p, ans, [ans - 1, ans + 1, math.factorial(n + 1), ans - math.factorial(n), ans * 2], "Remember that $0! = 1$.",
             "the sum.", "list each factorial; $0! = 1$ by definition.",
             [", ".join(f"${k}! = {math.factorial(k)}$" for k in range(0, n + 1)) + ".", f"Sum: ${ans}$."], "taking $0! = 0$.")


@reg(S, "basics")
def fc_exceed(r):
    k = r.randint(3, 12)
    ans = next(n for n in range(1, 50) if math.factorial(n) > 10 ** k)
    p = f"What is the smallest $n$ such that $n! > 10^{{{k}}}$?"
    return Q(p, ans, [ans - 1, ans + 1, k, ans + 2, k + 1 if k + 1 != ans else k + 3], "List factorials until they pass the target.",
             "the smallest $n$.", "factorials grow quickly; compute them in order.",
             [f"${ans - 1}! = {math.factorial(ans - 1)} \\le 10^{{{k}}}$.", f"${ans}! = {math.factorial(ans)} > 10^{{{k}}}$."], "stopping one step early.")


@reg(S, "basics")
def fc_ratio_simplify(r):
    n = r.randint(5, 20)
    k = r.randint(2, 4)
    ans = math.factorial(n + k) // math.factorial(n)
    p = f"What is $\\dfrac{{{n + k}!}}{{{n}!}}$?"
    return Q(p, ans, [math.factorial(k), ans // (n + k), (n + k) * k, ans + n, F(n + k, n) if F(n + k, n) != ans else ans * 2], "Cancel the common part.",
             "the value.", f"${n + k}! = {n + k} \\cdot \\cdots \\cdot {n + 1} \\cdot {n}!$.",
             [f"$\\frac{{{n + k}!}}{{{n}!}} = " + " \\cdot ".join(str(n + i) for i in range(k, 0, -1)) + f" = {ans}$."], "computing $" + str(k) + "!$ (dividing the numbers instead of cancelling).")


@reg(S, "basics")
def fc_power3(r):
    n = r.randint(10, 90)
    ans = vp(n, 3)
    p = f"What is the largest power of $3$ that divides ${n}!$? (Give the exponent.)"
    return Q(p, ans, [n // 3, ans + 1, ans - 1, vp(n, 2), n // 9], "Count multiples of $3$, $9$, $27$, ...",
             "the exponent of $3$.", "Legendre: $\\lfloor n/3 \\rfloor + \\lfloor n/9 \\rfloor + \\lfloor n/27 \\rfloor + \\cdots$",
             [" + ".join(str(n // 3 ** k) for k in range(1, 6) if 3 ** k <= n).join(["$", f" = {ans}$."])], "counting only multiples of $3$.")


@reg(S, "challenge")
def fcc_largest_square(r):
    n = r.randint(6, 12)
    f = math.factorial(n)
    sq = 1
    for p_, e in factorint(f).items():
        sq *= p_ ** (e - e % 2)
    p = f"What is the largest perfect square that divides ${n}!$? Give its square root."
    root = math.isqrt(sq)
    return Q(p, root, [root * 2, root // 2 if root % 2 == 0 else root + 1, math.isqrt(f), root * 3, n], "Round each exponent down to an even number.",
             "the square root of the largest square divisor.", "a square divisor uses even exponents; take each exponent down to the nearest even number.",
             [f"${n}! = {ftex_fact(f)}$.", f"Largest square: {ftex_fact(sq).join(['$', '$'])}, whose square root is ${ftex_fact(root) if root > 1 else '1'} = {root}$."], "using $\\lfloor \\sqrt{n!} \\rfloor$.")


@reg(S, "challenge")
def fcc_base12(r):
    n = r.randint(10, 60)
    ans = min(vp(n, 2) // 2, vp(n, 3))
    p = f"How many zeros are at the end of ${n}!$ when written in base $12$?"
    return Q(p, ans, [vp(n, 3), vp(n, 2) // 2 if vp(n, 2) // 2 != ans else ans + 1, vp(n, 5), ans + 1, n // 12], "$12 = 2^2 \\cdot 3$.",
             "the number of trailing zeros in base 12.", "each zero needs one factor of $12 = 2^2 \\cdot 3$: two $2$s and one $3$.",
             [f"Twos in ${n}!$: ${vp(n, 2)}$, enough for ${vp(n, 2) // 2}$ factors of $4$.", f"Threes: ${vp(n, 3)}$.", f"Zeros: $\\min({vp(n, 2) // 2}, {vp(n, 3)}) = {ans}$."], "counting factors of $12$ in the numbers $1$ to $n$.")


@reg(S, "challenge")
def fcc_smallest_zeros(r):
    k = r.choice([x for x in range(5, 60) if any(vp(n, 5) == x for n in range(1, 400))])
    ans = next(n for n in range(1, 400) if vp(n, 5) == k)
    p = f"What is the smallest $n$ for which $n!$ ends in exactly ${k}$ zeros?"
    return Q(p, ans, [5 * k, ans + 5, ans - 5, ans + 1, 4 * k], "Each multiple of $5$ adds a zero; multiples of $25$ add two.",
             "the smallest $n$.", "the zero count of $n!$ is $\\lfloor n/5 \\rfloor + \\lfloor n/25 \\rfloor + \\cdots$, and only increases at multiples of $5$.",
             [f"${ans}!$: $\\left\\lfloor \\frac{{{ans}}}{{5}} \\right\\rfloor + \\left\\lfloor \\frac{{{ans}}}{{25}} \\right\\rfloor + \\left\\lfloor \\frac{{{ans}}}{{125}} \\right\\rfloor = {vp(ans, 5)}$.", f"${ans - 5}!$ has only ${vp(ans - 5, 5)}$."],
             "answering $5k$, which overshoots when multiples of $25$ are involved.")


@reg(S, "challenge")
def fcc_last_nonzero(r):
    n = r.randint(5, 15)
    f = math.factorial(n)
    while f % 10 == 0:
        f //= 10
    ans = f % 10
    p = f"What is the last nonzero digit of ${n}!$?"
    return Q(p, ans, [(ans + 2) % 10, (ans + 4) % 10, (ans + 6) % 10, (ans + 8) % 10], "Remove the factors that make tens, then track the last digit.",
             "the last nonzero digit.", "strip out pairs of $2$ and $5$ (they make the zeros), then multiply what's left mod $10$.",
             [f"${n}! = {math.factorial(n)}$.", f"After removing trailing zeros: ${f}$, whose last digit is ${ans}$."], "forgetting to remove the zeros first.")


@reg(S, "challenge")
def fcc_square_divisors(r):
    n = r.randint(5, 10)
    fs = factorint(math.factorial(n))
    ans = math.prod(e // 2 + 1 for e in fs.values())
    p = f"How many positive divisors of ${n}!$ are perfect squares?"
    return Q(p, ans, [ndiv(math.factorial(n)), ans * 2, ans + 1, math.prod(e // 3 + 1 for e in fs.values()), len(fs)], "Choose even exponents for each prime.",
             "the number of square divisors.", "a square divisor uses an even exponent of each prime, from $0$ up to the exponent in $" + str(n) + "!$.",
             [f"${n}! = {ftex_fact(math.factorial(n))}$.", "Even choices: " + ", ".join(f"${p_}$: ${e // 2 + 1}$" for p_, e in sorted(fs.items())) + f". Product: ${ans}$."], "counting all divisors.")


@reg(S, "challenge")
def fcc_superfactorial(r):
    n = r.randint(5, 15)
    pr = r.choice([3, 5])
    ans = sum(vp(k, pr) for k in range(1, n + 1))
    p = f"What is the exponent of ${pr}$ in the product $1! \\cdot 2! \\cdot 3! \\cdots {n}!$?"
    return Q(p, ans, [vp(n, pr), ans + 1, ans - 1, sum(k // pr for k in range(1, n + 1)), n // pr], "Add the exponent of " + str(pr) + " in each factorial.",
             "the total exponent.", f"the exponent of ${pr}$ in a product is the sum over its factors.",
             ["Exponents in $k!$ for $k = 1, \\ldots, " + str(n) + "$: " + ", ".join(str(vp(k, pr)) for k in range(1, n + 1)) + ".", f"Sum: ${ans}$."], "counting only the exponent in $" + str(n) + "!$.")


@reg(S, "challenge")
def fcc_sum_factor(r):
    n = r.randint(5, 20)
    val = math.factorial(n) * (n + 2)
    big = max(factorint(val))
    p = f"What is the largest prime factor of ${n}! + {n + 1}!$?"
    return Q(p, big, [n + 1 if n + 1 != big else n + 3, max(q for q in range(2, n + 1) if is_prime(q)) if max(q for q in range(2, n + 1) if is_prime(q)) != big else big + 2, n + 2 if n + 2 != big else big + 4, big + 1, n], "Factor out $" + str(n) + "!$.",
             "the largest prime factor.", "$n! + (n + 1)! = n!(1 + (n + 1)) = n!(n + 2)$.",
             [f"${n}! + {n + 1}! = {n}! \\cdot {n + 2}$.", f"Primes in ${n}!$ go up to ${max(q for q in range(2, n + 1) if is_prime(q))}$; ${n + 2} = {ftex_fact(n + 2)}$.", f"Largest prime: ${big}$."],
             "assuming the largest prime is " + str(n + 1) + ".")
