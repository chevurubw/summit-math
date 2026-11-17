"""Number theory unit: original problems modeled on AMC 10/12 problem types. Answers are brute forced."""
import math
from fractions import Fraction as F

from common import Bank, explain, num, text_choice
from nt_more1 import MORE as M1
from nt_more2 import MORE as M2

MORE = {**M1, **M2}

banks = []


def bank(skill_id):
    b = Bank(skill_id)
    banks.append(b)
    return b


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def factor(n):
    f, out = 2, {}
    while f * f <= n:
        while n % f == 0:
            out[f] = out.get(f, 0) + 1
            n //= f
        f += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def ftex(n):
    return " \\cdot ".join(f"{p}^{{{e}}}" if e > 1 else str(p) for p, e in sorted(factor(n).items()))


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


# ---------------------------------------------------------------- primes and divisors
b = bank("nt_divisors")


def dv1(r):
    n = r.randint(24, 720)
    d = len(divisors(n))
    if d < 6:
        return None
    f = sorted(factor(n).items())
    p = f"How many positive divisors does ${n}$ have?"
    sol = explain(
        f"the number of positive divisors of ${n}$.",
        "every divisor is built from the same primes, each raised to a power from $0$ up to its power in the factorization. Multiply the number of choices.",
        [
            f"Prime factorization: ${n} = {ftex(n)}$.",
            "Choices for each prime's exponent: " + ", ".join(f"${p_}$ can use $0$ to ${e}$ (${e + 1}$ choices)" for p_, e in f) + ".",
            "Multiply: $" + " \\cdot ".join(str(e + 1) for _, e in f) + f" = {d}$.",
        ],
        f"${d}$.",
        "multiplying the exponents themselves, or forgetting that exponent $0$ is allowed (that is where the $+1$ comes from).",
    )
    return (p, d, [d - 1, d + 2, d // 2, sum(factor(n).values()), d + 1], ["Write the prime factorization, then multiply one more than each exponent."], sol)


def dv2(r):
    n = r.randint(30, 400)
    ds = divisors(n)
    if len(ds) < 4:
        return None
    s = sum(ds)
    f = sorted(factor(n).items())
    parts = [" + ".join(str(p_ ** i) for i in range(e + 1)) for p_, e in f]
    vals = [sum(p_ ** i for i in range(e + 1)) for p_, e in f]
    p = f"What is the sum of all positive divisors of ${n}$?"
    sol = explain(
        f"the sum of every positive divisor of ${n}$, including $1$ and ${n}$.",
        "if $n = p^a q^b$, every divisor appears exactly once when you expand $(1 + p + \\cdots + p^a)(1 + q + \\cdots + q^b)$.",
        [
            f"Factor: ${n} = {ftex(n)}$.",
            "Prime power sums: " + ", ".join(f"$({pt}) = {v}$" for pt, v in zip(parts, vals)) + ".",
            "Multiply: $" + " \\cdot ".join(map(str, vals)) + f" = {s}$.",
            "Check by listing: " + ", ".join(map(str, ds)) + f" add to ${s}$." if len(ds) <= 12 else f"(There are ${len(ds)}$ divisors in all.)",
        ],
        f"${s}$.",
        f"leaving out ${n}$ itself or $1$.",
    )
    return (p, s, [s - n, s + 1, 2 * n, s - 1, sum(ds[:-1]) + 1], ["Use $(1 + p + p^2 + \\cdots)(1 + q + \\cdots)\\cdots$ over the prime factorization."], sol)


def dv3(r):
    n = r.randint(100, 2000)
    fs = sorted(factor(n))
    if len(fs) < 2:
        return None
    ask = r.choice(["largest", "sum"])
    ans = max(fs) if ask == "largest" else sum(fs)
    words = "the largest prime factor" if ask == "largest" else "the sum of the distinct prime factors"
    p = f"What is {words} of ${n}$?"
    m = n
    divs = []
    for q in fs:
        while m % q == 0:
            divs.append(f"${m} \\div {q} = {m // q}$")
            m //= q
    sol = explain(
        f"{words} of ${n}$.",
        "divide out the smallest primes one at a time until you reach $1$.",
        ["Repeated division: " + ", ".join(divs) + ".", f"So ${n} = {ftex(n)}$, and the distinct primes are " + ", ".join(f"${q}$" for q in fs) + ".",
         (f"The largest is ${ans}$." if ask == "largest" else f"Their sum: ${' + '.join(map(str, fs))} = {ans}$.")],
        f"${ans}$.",
        "counting a repeated prime more than once." if ask == "sum" else "stopping before the last factor is prime.",
    )
    return (p, ans, [sum(fs) if ask == "largest" else max(fs), ans + 2, min(fs), sum(p_ * e for p_, e in factor(n).items()), ans * 2], ["Find the prime factorization."], sol)


def dv4(r):
    lo = r.randint(10, 80)
    hi = lo + r.randint(15, 40)
    primes = [x for x in range(lo, hi + 1) if is_prime(x)]
    cnt = len(primes)
    p = f"How many prime numbers are between ${lo}$ and ${hi}$, inclusive?"
    sol = explain(
        f"how many primes lie in the range ${lo}$ to ${hi}$.",
        f"a number up to ${hi}$ is prime if no prime up to $\\sqrt{{{hi}}} \\approx {math.isqrt(hi)}$ divides it. Check odd numbers against $3$, $5$, $7$ (and $11$ if needed).",
        [
            "Skip even numbers and multiples of $5$ right away.",
            f"Test the rest for divisibility by $3$, $7$" + (", $11$" if hi >= 121 else "") + ".",
            "The primes left are " + ", ".join(map(str, primes)) + ".",
        ],
        f"${cnt}$.",
        "counting numbers like $91 = 7 \\cdot 13$ or $119 = 7 \\cdot 17$ that look prime but are not.",
    )
    return (p, cnt, [cnt + 1, cnt - 1 if cnt > 1 else cnt + 2, cnt + 2, (hi - lo) // 3], ["Check each odd number for small prime factors: 3, 5, 7, and 11 are enough below 169."], sol)


def dvc1(r):
    k = r.choice([6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    ans = next(n for n in range(1, 10 ** 5) if len(divisors(n)) == k)
    p = f"What is the smallest positive integer with exactly ${k}$ positive divisors?"
    sol = explain(
        f"the smallest $n$ with exactly ${k}$ divisors.",
        f"if $n = p^a q^b \\cdots$, then $n$ has $(a + 1)(b + 1)\\cdots$ divisors. So write ${k}$ as a product of factors, then give the biggest exponents to the smallest primes.",
        [
            f"Ways to write ${k}$ as a product (each factor is an exponent plus one): try each one, like ${k}$ alone ($p^{{{k - 1}}}$), or two or three factors.",
            f"For each pattern, put the largest exponent on $2$, the next on $3$, and so on, and compare the results.",
            f"The smallest is ${ans} = {ftex(ans)}$, which has " + " \\cdot ".join(f"({e} + 1)" for e in sorted(factor(ans).values(), reverse=True)).join("$$") + f" $= {k}$ divisors.",
        ],
        f"${ans}$.",
        f"using a single prime power like $2^{{{k - 1}}} = {2 ** (k - 1)}$, which is usually much bigger.",
    )
    return (p, ans, [ans * 2, ans + 6, 2 ** (k - 1) if 2 ** (k - 1) < 10 ** 6 and 2 ** (k - 1) != ans else ans * 3, ans - 4 if ans > 10 else ans + 4, ans + 12],
            ["If $n = p^a q^b \\cdots$, then $(a + 1)(b + 1)\\cdots = $ the divisor count. Put the larger exponents on the smaller primes."], sol)


def dvc2(r):
    a, bb = r.randint(2, 6), r.randint(2, 6)
    n = 2 ** a * 3 ** bb * r.choice([1, 5, 25])
    f = sorted(factor(n).items())
    ask = r.choice(["square", "even"])
    total = len(divisors(n))
    if ask == "square":
        ans = sum(1 for d in divisors(n) if math.isqrt(d) ** 2 == d)
        p = f"How many positive divisors of ${n}$ are perfect squares?"
        steps = [f"${n} = {ftex(n)}$.", "A divisor is a perfect square exactly when every exponent is even.",
                 "Even exponent choices: " + ", ".join(f"${q}$ can use " + ", ".join(str(i) for i in range(0, e + 1, 2)) + f" (${e // 2 + 1}$ choices)" for q, e in f) + ".",
                 "Multiply: $" + " \\cdot ".join(str(e // 2 + 1) for _, e in f) + f" = {ans}$."]
        hint = "A divisor is a perfect square when every exponent in its factorization is even."
        trap = "forgetting that $0$ is an even exponent, which drops the choice of leaving a prime out."
    else:
        ans = sum(1 for d in divisors(n) if d % 2 == 0)
        p = f"How many positive divisors of ${n}$ are even?"
        steps = [f"${n} = {ftex(n)}$, which has ${total}$ divisors in all.", "Odd divisors leave out $2$ entirely: " + " \\cdot ".join(str(e + 1) for q, e in f if q != 2).join("$$") + f" $= {total - ans}$ of them.",
                 f"Even divisors: ${total} - {total - ans} = {ans}$. (Or count directly: the exponent of $2$ is $1$ to ${a}$, so ${a}$ choices, times the rest.)"]
        hint = "An even divisor must use at least one factor of 2."
        trap = "counting all divisors, including the odd ones."
    sol = explain(f"how many divisors of ${n}$ are {'perfect squares' if ask == 'square' else 'even'}.", "count exponent choices prime by prime, keeping only the ones that satisfy the condition.", steps, f"${ans}$.", trap)
    return (p, ans, [total, total - ans, ans + 1, ans * 2, ans - 1 if ans > 1 else ans + 3], [hint], sol)


def dvc3(r):
    p_ = r.choice([2, 3, 5])
    q_ = r.choice([q for q in (2, 3, 5, 7) if q != p_])
    a, bb = r.randint(1, 4), r.randint(1, 3)
    n = p_ ** a * q_ ** bb
    d = (a + 1) * (bb + 1)
    e = F(a * d, 2)
    if e.denominator != 1:
        return None
    p = f"The product of all positive divisors of ${n}$ is written as ${p_}^{{x}} \\cdot {q_}^{{y}}$. What is $x$?"
    sol = explain(
        f"the power of ${p_}$ in the product of all divisors of ${n}$.",
        "pair each divisor $d$ with $\\frac{n}{d}$: each pair multiplies to $n$. With $\\tau$ divisors there are $\\frac{\\tau}{2}$ pairs, so the product is $n^{\\tau/2}$.",
        [
            f"${n} = {p_}^{{{a}}} \\cdot {q_}^{{{bb}}}$ has $({a} + 1)({bb} + 1) = {d}$ divisors.",
            f"Product of all divisors: ${n}^{{{d}/2}} = {n}^{{{num(F(d, 2)).tex}}}$.",
            f"The power of ${p_}$: ${a} \\cdot {num(F(d, 2)).tex} = {e}$.",
        ],
        f"$x = {e}$.",
        f"forgetting to halve, which gives ${a * d}$.",
    )
    return (p, e, [a * d, d, e + 1, F(bb * d, 2), a * (a + 1) // 2], ["Pair each divisor $d$ with $\\frac{n}{d}$. The product of all divisors is $n^{\\tau(n)/2}$."], sol)


b.fill_unique("basics", [dv1, dv2, dv3, dv4] + MORE[b.skill_id]["basics"], 2101)
b.fill_unique("challenge", [dvc1, dvc2, dvc3] + MORE[b.skill_id]["challenge"], 2102)


# ---------------------------------------------------------------- gcd and lcm
b = bank("nt_gcd")


def euclid_steps(a, b_):
    out = []
    x, y = max(a, b_), min(a, b_)
    while y:
        out.append(f"${x} = {y} \\cdot {x // y} + {x % y}$")
        x, y = y, x % y
    return out


def g1(r):
    a, bb = r.randint(12, 300), r.randint(12, 300)
    if a == bb:
        return None
    ask = r.choice(["gcd", "lcm"])
    g, l = math.gcd(a, bb), a * bb // math.gcd(a, bb)
    if ask == "gcd":
        p = f"What is the greatest common divisor of ${a}$ and ${bb}$?"
        sol = explain(f"the largest number dividing both ${a}$ and ${bb}$.", "use prime factorizations: the GCD takes each shared prime to the smaller power.",
                      [f"${a} = {ftex(a)}$ and ${bb} = {ftex(bb)}$.", f"Shared primes at the smaller power give ${g}$." if g > 1 else "They share no prime, so the GCD is $1$.",
                       "Check with the Euclidean algorithm: " + "; ".join(euclid_steps(a, bb)) + f". The last nonzero remainder is ${g}$."],
                      f"${g}$.", "taking the larger power of each prime, which gives the LCM instead.")
        return (p, g, [l, g * 2, max(g // 2, 1) if g > 2 else g + 3, abs(a - bb), g + 1], ["Use prime factorizations, or the Euclidean algorithm."], sol)
    if l > 5000:
        return None
    p = f"What is the least common multiple of ${a}$ and ${bb}$?"
    sol = explain(f"the smallest number that both ${a}$ and ${bb}$ divide.", "the LCM takes every prime to the larger of its two powers. Equivalently, $\\operatorname{lcm}(a, b) = \\frac{ab}{\\gcd(a, b)}$.",
                  [f"${a} = {ftex(a)}$ and ${bb} = {ftex(bb)}$.", f"$\\gcd = {g}$, so $\\operatorname{{lcm}} = \\frac{{{a} \\cdot {bb}}}{{{g}}} = \\frac{{{a * bb}}}{{{g}}} = {l}$."],
                  f"${l}$.", f"multiplying the numbers (${a * bb}$) without dividing by the GCD.")
    return (p, l, [a * bb, l * 2, g, l // 2 if l % 2 == 0 else l + a, l + bb], ["Take the highest power of each prime that appears."], sol)


def g2(r):
    a, bb, c = r.sample([4, 6, 8, 9, 10, 12, 15, 18, 20], 3)
    l = math.lcm(a, bb, c)
    if l > 360:
        return None
    p = f"Three lights blink every {a}, {bb}, and {c} seconds. They all blink together at noon. After how many seconds will they next blink together?"
    sol = explain("the next time all three blink at once.", "each light blinks at multiples of its period, so all three blink together at common multiples. The first one is the LCM.",
                  [f"${a} = {ftex(a)}$, ${bb} = {ftex(bb)}$, ${c} = {ftex(c)}$.", f"Take each prime at its highest power: $\\operatorname{{lcm}}({a}, {bb}, {c}) = {ftex(l)} = {l}$."],
                  f"${l}$ seconds.", f"multiplying the three periods (${a * bb * c}$), which is a common multiple but not the smallest.")
    return (p, l, [a * bb * c, a + bb + c, l * 2, max(a, bb, c) * 2, l // 2 if l % 2 == 0 else l + a], ["They blink together at common multiples of the three times."], sol)


def g3(r):
    w, h = r.randint(4, 40) * r.randint(1, 6), r.randint(4, 40) * r.randint(1, 6)
    g = math.gcd(w, h)
    if g < 2 or w == h:
        return None
    tiles = (w // g) * (h // g)
    p = f"A {w} by {h} rectangle is covered exactly by identical square tiles with whole number side lengths, as large as possible. How many tiles are used?"
    sol = explain("the number of tiles when the tiles are as big as possible.", "the tile side must divide both the width and the height, so the largest possible tile has side $\\gcd(w, h)$.",
                  [f"$\\gcd({w}, {h}) = {g}$, so each tile is ${g} \\times {g}$.", f"Along the width: $\\frac{{{w}}}{{{g}}} = {w // g}$ tiles. Along the height: $\\frac{{{h}}}{{{g}}} = {h // g}$ tiles.", f"Total: ${w // g} \\cdot {h // g} = {tiles}$."],
                  f"${tiles}$ tiles.", f"answering with the tile size ${g}$ instead of the number of tiles.")
    return (p, tiles, [g, w * h // 4, tiles * 2, tiles + w // g, w * h], ["The largest tile has side length $\\gcd(w, h)$."], sol)


def g4(r):
    g = r.randint(2, 12)
    x, y = r.randint(2, 15), r.randint(2, 15)
    if math.gcd(x, y) != 1:
        return None
    a, bb = g * x, g * y
    l = g * x * y
    p = f"Two positive integers have greatest common divisor ${g}$ and least common multiple ${l}$. One of them is ${a}$. What is the other?"
    sol = explain("the second number $n$.", "for any two positive integers, $\\gcd \\times \\operatorname{lcm} = $ the product of the numbers.",
                  [f"${g} \\cdot {l} = {a} \\cdot n$, so ${g * l} = {a}n$.", f"$n = \\frac{{{g * l}}}{{{a}}} = {bb}$.", f"Check: $\\gcd({a}, {bb}) = {math.gcd(a, bb)}$ and $\\operatorname{{lcm}}({a}, {bb}) = {math.lcm(a, bb)}$."],
                  f"${bb}$.", f"dividing the LCM by the given number without the GCD: $\\frac{{{l}}}{{{a}}} = {num(F(l, a)).tex}$.")
    return (p, bb, [l // a * g if l // a * g != bb else bb + g, l, g * y + g, a, l // g], ["For any two positive integers, $\\gcd \\cdot \\text{lcm}$ equals their product."], sol)


def gc1(r):
    g = r.randint(1, 6)
    primes = r.sample([2, 3, 5, 7], r.randint(2, 3))
    L = g
    for p_ in primes:
        L *= p_ ** r.randint(1, 2)
    cnt = sum(1 for a in range(1, L + 1) if L % a == 0 for bb in range(a, L + 1) if L % bb == 0 and math.gcd(a, bb) == g and math.lcm(a, bb) == L)
    if cnt == 0:
        return None
    k = len(factor(L // g))
    p = f"How many pairs of positive integers $a \\le b$ have $\\gcd(a, b) = {g}$ and $\\text{{lcm}}(a, b) = {L}$?"
    sol = explain(
        "the number of pairs with this exact GCD and LCM.",
        f"factor out the GCD: $a = {g}x$ and $b = {g}y$ with $\\gcd(x, y) = 1$. Then $\\operatorname{{lcm}}(a, b) = {g}xy$, so $xy = \\frac{{{L}}}{{{g}}} = {L // g}$.",
        [
            f"${L // g} = {ftex(L // g)}$ has ${k}$ distinct prime{'s' if k != 1 else ''}.",
            "Since $x$ and $y$ share no prime, each prime power must go entirely into $x$ or entirely into $y$: $2$ choices for each.",
            f"Ordered pairs $(x, y)$: $2^{{{k}}} = {2 ** k}$. Requiring $a \\le b$ cuts this in half: ${cnt}$." if L // g > 1 else f"Only $x = y = 1$ works, giving ${cnt}$ pair.",
        ],
        f"${cnt}$.",
        "splitting a prime power between $x$ and $y$, which would make their GCD bigger than $1$.",
    )
    return (p, cnt, [2 ** k if 2 ** k != cnt else cnt + 2, cnt + 1, cnt * 2 if cnt * 2 != 2 ** k else cnt + 3, k if k != cnt else k + 1, cnt - 1 if cnt > 1 else cnt + 4],
            [f"Write $a = {g}x$ and $b = {g}y$ with $\\gcd(x, y) = 1$ and $xy = {L // g}$.", "Each prime power of $xy$ goes entirely to $x$ or entirely to $y$."], sol)


def gc2(r):
    a, bb = r.randint(2, 6), r.randint(1, 9)
    c, d = r.randint(2, 6), r.randint(1, 9)
    det = abs(a * d - bb * c)
    if det < 2:
        return None
    best = max(math.gcd(a * n + bb, c * n + d) for n in range(1, 2000))
    nbest = next(n for n in range(1, 2000) if math.gcd(a * n + bb, c * n + d) == best)
    p = f"As $n$ ranges over the positive integers, what is the largest possible value of $\\gcd({a}n + {bb}, {c}n + {d})$?"
    sol = explain(
        "the largest value this GCD ever takes.",
        "anything that divides two numbers also divides any combination of them. Choose a combination that cancels $n$.",
        [
            f"If $g$ divides both ${a}n + {bb}$ and ${c}n + {d}$, it divides ${c}({a}n + {bb}) - {a}({c}n + {d}) = {c * bb - a * d}$.",
            f"So $g$ must divide ${det}$, and the GCD is at most ${det}$.",
            f"Check which divisors of ${det}$ are actually reached: at $n = {nbest}$ the numbers are ${a * nbest + bb}$ and ${c * nbest + d}$, with GCD ${best}$." + ("" if best == det else f" The value ${det}$ is never reached, because no $n$ makes both expressions multiples of it."),
        ],
        f"${best}$.",
        f"stopping at the bound ${det}$ without checking that some $n$ actually reaches it." if best != det else "trying small values of $n$ only, which can miss the maximum.",
    )
    return (p, best, [det if det != best else best + 1, best * 2, a * c, bb + d, 1], ["Any common divisor also divides combinations like $c(an + b) - a(cn + d)$."], sol)


def gc3(r):
    k = r.choice([6, 12, 18, 20, 24, 30])
    m = k * r.choice([2, 3, 4, 5, 6])
    ns = [n for n in range(1, m + 1) if math.lcm(n, k) == m]
    cnt = len(ns)
    if cnt == 0:
        return None
    fm, fk = factor(m), factor(k)
    choices = []
    for q, e in sorted(fm.items()):
        ek = fk.get(q, 0)
        if ek < e:
            choices.append(f"for ${q}$, ${k}$ has only ${q}^{{{ek}}}$, so $n$ must have exactly ${q}^{{{e}}}$ (1 choice)")
        else:
            choices.append(f"for ${q}$, ${k}$ already has ${q}^{{{e}}}$, so $n$ can have ${q}^0$ to ${q}^{{{e}}}$ (${e + 1}$ choices)")
    p = f"How many positive integers $n$ satisfy $\\text{{lcm}}(n, {k}) = {m}$?"
    sol = explain(
        f"all $n$ whose LCM with ${k}$ is exactly ${m}$.",
        "the LCM takes, for each prime, the larger exponent. Compare prime by prime.",
        [f"${m} = {ftex(m)}$ and ${k} = {ftex(k)}$. $n$ must divide ${m}$.", "Prime by prime: " + "; ".join(choices) + ".", "Multiply the choices: $" + " \\cdot ".join(str(fm[q] + 1 if fk.get(q, 0) >= fm[q] else 1) for q in sorted(fm)) + f" = {cnt}$."],
        f"${cnt}$.",
        f"counting all divisors of ${m}$. Some of them have an LCM with ${k}$ smaller than ${m}$.",
    )
    return (p, cnt, [cnt + 1, cnt + 2, len(divisors(m)), len(divisors(m // k)) if len(divisors(m // k)) != cnt else cnt + 3, cnt * 2], [f"$n$ must divide ${m}$. Compare prime powers of $n$, ${k}$, and ${m}$."], sol)


b.fill_unique("basics", [g1, g2, g3, g4] + MORE[b.skill_id]["basics"], 2201)
b.fill_unique("challenge", [gc1, gc2, gc3] + MORE[b.skill_id]["challenge"], 2202)


# ---------------------------------------------------------------- divisibility and digits
b = bank("nt_divisibility")


def di1(r):
    m = r.choice([3, 9, 11])
    digits = [r.randint(1, 9)] + [r.randint(0, 9) for _ in range(3)]
    s = "".join(map(str, digits))
    pos = r.randint(1, 3)
    opts = [d for d in range(10) if int(s[:pos] + str(d) + s[pos + 1:]) % m == 0]
    if len(opts) != 1:
        return None
    shown = s[:pos] + "A" + s[pos + 1:]
    ans = opts[0]
    full = int(s[:pos] + str(ans) + s[pos + 1:])
    known = [int(c) for i, c in enumerate(s) if i != pos]
    p = f"The four-digit number ${shown}$ is divisible by ${m}$, where $A$ is a single digit. What is $A$?"
    if m in (3, 9):
        ks = sum(known)
        steps = [f"Rule: a number is divisible by ${m}$ exactly when its digit sum is.", f"Known digits add to ${' + '.join(map(str, known))} = {ks}$, so we need ${ks} + A$ to be a multiple of ${m}$.",
                 f"The only digit that works is $A = {ans}$ (sum ${ks + ans}$)."]
    else:
        dd = [int(c) if i != pos else None for i, c in enumerate(s)]
        terms = " - ".join([]) if False else ""
        alt = " ".join((("+ " if i % 2 == 0 else "- ") if i else "") + (str(dd[i]) if dd[i] is not None else "A") for i in range(4))
        steps = ["Rule: a number is divisible by $11$ exactly when its alternating digit sum (first $-$ second $+$ third $-$ fourth) is a multiple of $11$ (including $0$).",
                 f"Alternating sum: ${alt}$.", f"Only $A = {ans}$ makes it a multiple of $11$."]
    steps.append(f"Check: ${full} = {m} \\cdot {full // m}$.")
    sol = explain(f"the missing digit $A$.", f"use the divisibility rule for ${m}$ instead of dividing.", steps, f"$A = {ans}$.", "adding all the digits for the $11$ rule; it needs the alternating sum." if m == 11 else "forgetting that the digit sum only needs to be a multiple, not exactly equal to it.")
    return (p, ans, [d for d in range(10) if d != ans][:6], [f"Use the divisibility rule for ${m}$."], sol)


def di2(r):
    lo, hi = r.randint(1, 50), r.randint(200, 1000)
    a, bb = r.sample([2, 3, 4, 5, 6, 7], 2)
    L = math.lcm(a, bb)
    ca = sum(1 for x in range(lo, hi + 1) if x % a == 0)
    cb = sum(1 for x in range(lo, hi + 1) if x % bb == 0)
    both = sum(1 for x in range(lo, hi + 1) if x % L == 0)
    cnt = ca + cb - both
    p = f"How many integers from ${lo}$ to ${hi}$, inclusive, are divisible by ${a}$ or ${bb}$ (or both)?"
    sol = explain(
        f"numbers in the range divisible by at least one of ${a}$ and ${bb}$.",
        "Inclusion and Exclusion: add the two counts, then subtract the numbers counted twice (those divisible by both, which means by the LCM).",
        [
            f"Multiples of ${a}$ from ${lo}$ to ${hi}$: $\\lfloor {hi}/{a} \\rfloor - \\lfloor {lo - 1}/{a} \\rfloor = {ca}$.",
            f"Multiples of ${bb}$: ${cb}$.",
            f"Multiples of both, that is of $\\operatorname{{lcm}}({a}, {bb}) = {L}$: ${both}$.",
            f"Total: ${ca} + {cb} - {both} = {cnt}$.",
        ],
        f"${cnt}$.",
        f"forgetting to subtract the overlap (giving ${ca + cb}$), or using ${a} \\cdot {bb}$ instead of the LCM when they share a factor.",
    )
    return (p, cnt, [cnt + both, cnt - 1, cnt + 1, ca, cnt - both], ["Count the multiples of each, then subtract the numbers counted twice."], sol)


def di3(r):
    n = r.randint(100, 99999)
    ds = sum(map(int, str(n)))
    k = r.randint(2, 5)
    m = n * k
    ans = sum(map(int, str(m)))
    p = f"What is the sum of the digits of ${n} \\times {k}$?"
    sol = explain("the digit sum of the product.", "multiply first; digit sums do not simply scale, because carrying changes the digits.",
                  [f"${n} \\times {k} = {m}$.", f"Digits: ${' + '.join(str(m))} = {ans}$."], f"${ans}$.", f"multiplying the digit sum of ${n}$ by ${k}$ (${ds * k}$), which ignores carrying.")
    return (p, ans, [ds * k, ans + 1, ans - 1, ans + 9, ds + k], ["Multiply first, then add the digits."], sol)


def di4(r):
    k = r.choice([6, 12, 15, 18, 24, 36, 45])
    s = r.choice([9, 18]) if k % 9 == 0 else r.choice([6, 9, 12, 15])
    ans = next((x for x in range(k, 10 ** 6, k) if sum(map(int, str(x))) == s), None)
    if ans is None:
        return None
    p = f"What is the smallest positive multiple of ${k}$ whose digits add up to ${s}$?"
    sol = explain(f"the first multiple of ${k}$ with digit sum ${s}$.", "list multiples in order and check digit sums; divisibility rules tell you which digit sums are even possible.",
                  [f"Multiples of ${k}$ have digit sums that are multiples of $3$" + (" (even $9$)" if k % 9 == 0 else "") + f", so ${s}$ is possible.",
                   "Check multiples in increasing order: " + ", ".join(f"${x}$ (sum ${sum(map(int, str(x)))}$)" for x in range(k, ans + 1, k)[-4:]) + ".",
                   f"The first one with digit sum ${s}$ is ${ans}$."],
                  f"${ans}$.", "skipping a smaller multiple. Check every multiple in order.")
    return (p, ans, [ans + k, ans + 2 * k, ans - k if ans > k else ans + 3 * k, k * s, ans + 9], ["Check multiples in order, and use divisibility rules to skip impossible ones."], sol)


def dic1(r):
    a, bb = r.randint(1, 30), r.randint(1, 6)
    val = bb * bb + a
    ns = [n for n in range(1, val + bb + 1) if (n * n + a) % (n + bb) == 0]
    if not 1 <= len(ns) <= 10:
        return None
    ds = [d for d in divisors(val) if d > bb]
    p = f"For how many positive integers $n$ is $\\dfrac{{n^2 + {a}}}{{n + {bb}}}$ an integer?"
    sol = explain(
        "the positive $n$ that make the fraction a whole number.",
        "divide the polynomials so the remainder is a plain number; then the denominator must divide that number.",
        [
            f"$n^2 + {a} = (n + {bb})(n - {bb}) + {val}$, so $\\frac{{n^2 + {a}}}{{n + {bb}}} = n - {bb} + \\frac{{{val}}}{{n + {bb}}}$.",
            f"This is an integer exactly when $n + {bb}$ divides ${val}$.",
            f"Divisors of ${val}$ bigger than ${bb}$ (so $n \\ge 1$): " + ", ".join(map(str, ds)) + ".",
            "Each gives $n = d - " + str(bb) + "$: " + ", ".join(map(str, ns)) + ".",
        ],
        f"${len(ns)}$.",
        f"counting all divisors of ${val}$, including ones that give $n \\le 0$.",
    )
    return (p, len(ns), [len(ns) + 1, len(ns) + 2, len(divisors(val)) if len(divisors(val)) != len(ns) else len(ns) + 3, len(ns) - 1 if len(ns) > 1 else 4, len(ns) * 2],
            [f"Divide: $n^2 + {a} = (n + {bb})(n - {bb}) + {val}$.", f"So $n + {bb}$ must divide ${val}$."], sol)


def dic2(r):
    a = r.choice([7, 11, 13, 17])
    dcount = r.choice([3, 4])
    hi = 10 ** dcount - 1
    ask = r.choice(["largest", "count"])
    if ask == "largest":
        ans = hi - hi % a
        p = f"What is the largest {dcount}-digit multiple of ${a}$?"
        sol = explain(f"the biggest {dcount} digit number divisible by ${a}$.", f"start from the biggest {dcount} digit number and remove its remainder.",
                      [f"The largest {dcount} digit number is ${hi}$.", f"${hi} = {a} \\cdot {hi // a} + {hi % a}$.", f"Subtract the remainder: ${hi} - {hi % a} = {ans}$."],
                      f"${ans}$.", "adding instead of subtracting, which goes past the largest " + str(dcount) + " digit number.")
        return (p, ans, [ans - a, ans + a if ans + a <= hi else ans - 2 * a, hi, ans - 1, hi - a], [f"Divide ${hi}$ by ${a}$ and drop the remainder."], sol)
    lo = 10 ** (dcount - 1)
    cnt = hi // a - (lo - 1) // a
    p = f"How many {dcount}-digit positive integers are multiples of ${a}$?"
    sol = explain(f"how many multiples of ${a}$ lie from ${lo}$ to ${hi}$.", "count multiples up to the top, then subtract those below the bottom.",
                  [f"Multiples of ${a}$ up to ${hi}$: $\\lfloor {hi}/{a} \\rfloor = {hi // a}$.", f"Multiples below ${lo}$ (up to ${lo - 1}$): $\\lfloor {lo - 1}/{a} \\rfloor = {(lo - 1) // a}$.", f"Difference: ${hi // a} - {(lo - 1) // a} = {cnt}$."],
                  f"${cnt}$.", f"forgetting the small multiples below ${lo}$ and answering ${hi // a}$.")
    return (p, cnt, [cnt + 1, cnt - 1, hi // a, (hi - lo) // a, cnt + 2], ["Count multiples up to the largest, minus those below the smallest."], sol)


def dic3(r):
    a, bb = r.randint(1, 9), r.randint(0, 9)
    if a <= bb:
        return None
    n = 10 * a + bb
    m = 10 * bb + a
    diff = n - m
    sols = [x for x in range(10, 100) if x - int(str(x)[::-1]) == diff and sum(map(int, str(x))) == a + bb]
    if len(sols) != 1:
        return None
    p = f"A two-digit number is ${diff}$ more than the number formed by reversing its digits. Its digits add to ${a + bb}$. What is the number?"
    sol = explain("the two digit number. Call its tens digit $a$ and ones digit $b$.", "a two digit number $\\overline{ab}$ is worth $10a + b$; reversed it is $10b + a$.",
                  [f"Difference: $(10a + b) - (10b + a) = 9a - 9b = 9(a - b) = {diff}$, so $a - b = {a - bb}$.", f"Digit sum: $a + b = {a + bb}$.",
                   f"Add the equations: $2a = {2 * a}$, so $a = {a}$ and $b = {bb}$.", f"The number is ${n}$. Check: ${n} - {m:02d} = {diff}$."],
                  f"${n}$.", f"answering with the reversed number ${m}$.")
    return (p, n, [m, n + 9, n - 9, diff, a * 10 + a], ["Write the number as $10a + b$. Reversing gives $10b + a$, and the difference is $9(a - b)$."], sol)


b.fill_unique("basics", [di1, di2, di3, di4] + MORE[b.skill_id]["basics"], 2301)
b.fill_unique("challenge", [dic1, dic2, dic3] + MORE[b.skill_id]["challenge"], 2302)


# ---------------------------------------------------------------- modular arithmetic
b = bank("nt_modular")


def mo1(r):
    a, bb = r.randint(100, 9999), r.randint(100, 9999)
    m = r.randint(3, 13)
    op = r.choice(["+", "\\times"])
    ra, rb = a % m, bb % m
    val = (a + bb) % m if op == "+" else (a * bb) % m
    p = f"What is the remainder when ${a} {op} {bb}$ is divided by ${m}$?"
    sol = explain(f"$({a} {op} {bb}) \\bmod {m}$ without computing the full {'sum' if op == '+' else 'product'}.", "remainders can be added or multiplied first: replace each number by its remainder, then reduce again.",
                  [f"${a} = {m} \\cdot {a // m} + {ra}$, so ${a} \\equiv {ra}$.", f"${bb} = {m} \\cdot {bb // m} + {rb}$, so ${bb} \\equiv {rb}$.",
                   f"{'Add' if op == '+' else 'Multiply'}: ${ra} {op} {rb} = {ra + rb if op == '+' else ra * rb}$, which leaves remainder ${val}$ when divided by ${m}$."],
                  f"${val}$.", "forgetting to reduce the final result, which can be bigger than " + str(m) + ".")
    return (p, val, [(val + 1) % m, (ra + rb) if op != "+" else ra * rb % m, (val + 2) % m, m - 1 - val if m - 1 - val != val else (val + 3) % m, 0 if val else 1], ["Reduce each number mod " + str(m) + " first."], sol)


def mo2(r):
    n = r.randint(20, 400)
    m = r.choice([7, 9, 11, 12, 13])
    k = r.randint(2, 5)
    rem = n % m
    ans = (k * rem) % m
    p = f"When $n$ is divided by ${m}$, the remainder is ${rem}$. What is the remainder when ${k}n$ is divided by ${m}$?"
    sol = explain(f"the remainder of ${k}n$.", f"write $n = {m}q + {rem}$; multiplying by ${k}$ multiplies the remainder by ${k}$ too (then reduce).",
                  [f"${k}n = {k}({m}q + {rem}) = {m}({k}q) + {k * rem}$.", f"The part ${m}({k}q)$ is a multiple of ${m}$, so only ${k * rem}$ matters.", f"${k * rem} = {m} \\cdot {k * rem // m} + {ans}$."],
                  f"${ans}$.", f"answering ${k * rem}$ without reducing it below ${m}$." if k * rem >= m else "adding instead of multiplying.")
    return (p, ans, [k * rem if k * rem != ans else ans + m, (rem + k) % m, rem, (k * rem + 1) % m, (k * rem - 1) % m], [f"If $n \\equiv {rem}$, then ${k}n \\equiv {k} \\cdot {rem} \\pmod{{{m}}}$."], sol)


def mo3(r):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    start = r.randint(0, 6)
    n = r.randint(30, 1000)
    ans = (start + n) % 7
    choices = [text_choice(days[(ans + k) % 7], (ans + k) % 7 + 0.1 * k) for k in (1, 2, 3, 5)]
    p = f"Today is {days[start]}. What day of the week will it be ${n}$ days from today?"
    sol = explain(f"the weekday ${n}$ days from now.", "weekdays repeat every $7$ days, so only the remainder of " + str(n) + " divided by $7$ matters.",
                  [f"${n} = 7 \\cdot {n // 7} + {n % 7}$.", f"After ${n // 7}$ full weeks it is {days[start]} again; then go ${n % 7}$ more day{'s' if n % 7 != 1 else ''}."],
                  f"{days[ans]}.", "counting today as the first day.")
    return (p, text_choice(days[ans], ans + 10), choices, ["Days repeat every 7. Find the remainder when dividing by 7."], sol, False)


def mo4(r):
    m = r.choice([7, 9, 11, 13, 17])
    a = r.randint(2, m - 1)
    if math.gcd(a, m) != 1:
        return None
    x = r.randint(1, m - 1)
    bb = (a * x) % m
    tries = [f"${a} \\cdot {t} = {a * t} \\equiv {a * t % m}$" for t in range(1, x + 1)]
    p = f"What is the smallest positive integer $x$ such that ${a}x \\equiv {bb} \\pmod{{{m}}}$?"
    sol = explain(f"the smallest $x > 0$ with ${a}x$ leaving remainder ${bb}$ when divided by ${m}$.", f"since ${a}$ and ${m}$ share no factor, exactly one $x$ from $1$ to ${m - 1}$ works. Try them in order (or use an inverse).",
                  ["Try $x = 1, 2, \\ldots$: " + "; ".join(tries[-5:]) + ("" if len(tries) <= 5 else " (earlier values do not work)") + ".", f"The first match is $x = {x}$."],
                  f"$x = {x}$.", f"answering ${bb}$, the right side, instead of solving for $x$.")
    return (p, x, [(x + 1) % m or m, bb if bb != x else (x + 3) % m or 1, (x + 2) % m or m, m - x if m - x != x else (x + 4) % m or 2, (bb * a) % m or 1], [f"Try $x = 1, 2, 3, \\ldots$, or multiply by the inverse of ${a}$ mod ${m}$."], sol)


def moc1(r):
    m1, m2, m3 = r.sample([3, 4, 5, 7], 3)
    r1, r2, r3 = r.randint(1, m1 - 1), r.randint(1, m2 - 1), r.randint(1, m3 - 1)
    n = next(x for x in range(1, m1 * m2 * m3 + 1) if x % m1 == r1 and x % m2 == r2 and x % m3 == r3)
    L = m1 * m2 * m3
    big = max(m1, m2, m3)
    rb = {m1: r1, m2: r2, m3: r3}[big]
    cands = [x for x in range(rb, n + 1, big)]
    p = (f"What is the smallest positive integer that leaves remainder ${r1}$ when divided by ${m1}$, remainder ${r2}$ when divided by ${m2}$, "
         f"and remainder ${r3}$ when divided by ${m3}$?")
    sol = explain("the smallest number meeting all three remainder conditions.", "list the numbers that satisfy the condition with the largest divisor (fewest candidates), and test them against the others.",
                  [f"Numbers with remainder ${rb}$ when divided by ${big}$: " + ", ".join(map(str, cands)) + ", ...",
                   "Test each against the other two conditions; the first that passes is " + f"${n}$.",
                   f"Check: ${n} = {m1} \\cdot {n // m1} + {r1}$, ${n} = {m2} \\cdot {n // m2} + {r2}$, ${n} = {m3} \\cdot {n // m3} + {r3}$.",
                   f"(All solutions differ by $\\operatorname{{lcm}}({m1}, {m2}, {m3}) = {L}$, so ${n}$ is the smallest positive one.)"],
                  f"${n}$.", f"adding the next multiple of ${L}$; the question asks for the smallest.")
    return (p, n, [n + L, n + m1 * m2, L - n if L - n != n else n + 1, n + m3, n + 2], ["List numbers that fit the first condition, and check them against the others."], sol)


def moc2(r):
    m = r.choice([5, 7, 8, 9, 10, 12])
    a = r.choice(sorted({x * x % m for x in range(m)}))
    N = r.choice([50, 100, 120, 200])
    res = [x for x in range(m) if x * x % m == a]
    cnt = sum(1 for n in range(1, N + 1) if n * n % m == a)
    full, left = N // m, N % m
    extra = sum(1 for x in res if 1 <= x <= left)
    p = f"How many integers $n$ with $1 \\le n \\le {N}$ satisfy $n^2 \\equiv {a} \\pmod{{{m}}}$?"
    sol = explain(f"how many $n$ up to ${N}$ have $n^2$ leaving remainder ${a}$ when divided by ${m}$.", f"$n^2 \\bmod {m}$ depends only on $n \\bmod {m}$, so test the ${m}$ remainders once, then count.",
                  [f"Squares of $0, 1, \\ldots, {m - 1}$ mod ${m}$: " + ", ".join(str(x * x % m) for x in range(m)) + ".", f"The remainders that work: " + ", ".join(map(str, res)) + f" (${len(res)}$ of them).",
                   f"${N} = {m} \\cdot {full} + {left}$: ${full}$ full blocks give ${full * len(res)}$; the last partial block (remainders $1$ to ${left}$) adds ${extra}$.", f"Total: ${cnt}$."],
                  f"${cnt}$.", "forgetting the partial block at the end, or counting the remainder $0$ as if $n = 0$ were allowed.")
    return (p, cnt, [N // m, cnt + len(res), cnt - 1, cnt + 1, len(res) * (N // m + 1) if len(res) * (N // m + 1) != cnt else cnt + 2], [f"Find which remainders mod ${m}$ work, then count how often each appears up to ${N}$."], sol)


def moc3(r):
    n = r.randint(20, 200)
    m = r.choice([7, 9, 11, 13])
    which = r.choice(["sum", "sq"])
    if which == "sum":
        total = n * (n + 1) // 2
        p = f"What is the remainder when $1 + 2 + 3 + \\cdots + {n}$ is divided by ${m}$?"
        hint = "Use $\\frac{n(n + 1)}{2}$."
        form = f"\\frac{{{n} \\cdot {n + 1}}}{{2}}"
    else:
        total = n * (n + 1) * (2 * n + 1) // 6
        p = f"What is the remainder when $1^2 + 2^2 + \\cdots + {n}^2$ is divided by ${m}$?"
        hint = "Use $\\frac{n(n + 1)(2n + 1)}{6}$."
        form = f"\\frac{{{n} \\cdot {n + 1} \\cdot {2 * n + 1}}}{{6}}"
    ans = total % m
    sol = explain("the remainder of a long sum.", "use the closed formula for the sum, then divide.",
                  [f"The sum equals ${form} = {total}$.", f"${total} = {m} \\cdot {total // m} + {ans}$."], f"${ans}$.", "trying to reduce each term and losing track; the formula is faster.")
    return (p, ans, [(ans + 1) % m, (ans + 3) % m, (ans + m - 1) % m, n % m if n % m != ans else (ans + 2) % m, (ans + 5) % m], [hint], sol)


b.fill_unique("basics", [mo1, mo2, mo3, mo4] + MORE[b.skill_id]["basics"], 2401)
b.fill_unique("challenge", [moc1, moc2, moc3] + MORE[b.skill_id]["challenge"], 2402)


# ---------------------------------------------------------------- units digits and powers
b = bank("nt_powers")


def cycle10(a):
    cyc, x = [], a % 10
    while x not in cyc:
        cyc.append(x)
        x = x * a % 10
    return cyc


def pw1(r):
    a = r.randint(2, 99)
    n = r.randint(10, 2030)
    ans = pow(a, n, 10)
    cyc = cycle10(a)
    pos = n % len(cyc) or len(cyc)
    p = f"What is the units digit of ${a}^{{{n}}}$?"
    sol = explain(f"the last digit of ${a}^{{{n}}}$.", f"the last digit of a power depends only on the last digit of the base, ${a % 10}$, and it repeats in a short cycle.",
                  [f"Last digits of ${a % 10}^1, {a % 10}^2, \\ldots$: " + ", ".join(map(str, cyc)) + f", then it repeats (cycle length ${len(cyc)}$).",
                   f"${n} = {len(cyc)} \\cdot {n // len(cyc)} + {n % len(cyc)}$, so ${a}^{{{n}}}$ is in position ${pos}$ of the cycle.",
                   f"Position ${pos}$ is ${cyc[pos - 1]}$."],
                  f"${ans}$.", "treating remainder $0$ as the first position. A remainder of $0$ means the last position in the cycle.")
    return (p, ans, [d for d in range(10) if d != ans][:5], ["Units digits of powers repeat in a cycle of length at most 4."], sol)


def pw2(r):
    a, bb = r.randint(2, 30), r.randint(2, 30)
    m, n = r.randint(5, 200), r.randint(5, 200)
    ua, ub = pow(a, m, 10), pow(bb, n, 10)
    ans = (ua + ub) % 10
    p = f"What is the units digit of ${a}^{{{m}}} + {bb}^{{{n}}}$?"
    ca, cb = cycle10(a), cycle10(bb)
    sol = explain("the last digit of the sum.", "find each last digit from its cycle, then add the last digits.",
                  [f"${a}$: last digits cycle " + ", ".join(map(str, ca)) + f"; ${m}$ lands on ${ua}$.", f"${bb}$: last digits cycle " + ", ".join(map(str, cb)) + f"; ${n}$ lands on ${ub}$.",
                   f"${ua} + {ub} = {ua + ub}$, which ends in ${ans}$."],
                  f"${ans}$.", "adding the bases or the exponents first. Only the last digits of the two powers matter.")
    return (p, ans, [d for d in range(10) if d != ans][:5], ["Find each units digit separately, then add."], sol)


def pw3(r):
    a = r.choice([2, 3, 4, 5, 6, 7])
    m = r.choice([3, 5, 7, 9, 11, 13])
    if math.gcd(a, m) != 1:
        return None
    n = r.randint(20, 500)
    ans = pow(a, n, m)
    order = next(k for k in range(1, m) if pow(a, k, m) == 1)
    pw = [pow(a, k, m) for k in range(1, order + 1)]
    p = f"What is the remainder when ${a}^{{{n}}}$ is divided by ${m}$?"
    sol = explain(f"${a}^{{{n}}} \\bmod {m}$.", f"find the first power of ${a}$ that leaves remainder $1$; after it the remainders repeat.",
                  [f"Remainders of ${a}^1, \\ldots, {a}^{{{order}}}$ mod ${m}$: " + ", ".join(map(str, pw)) + f". So ${a}^{{{order}}} \\equiv 1$.",
                   f"${n} = {order} \\cdot {n // order} + {n % order}$, so ${a}^{{{n}}} \\equiv (1)^{{{n // order}}} \\cdot {a}^{{{n % order}}}$.",
                   f"${a}^{{{n % order}}} \\equiv {ans} \\pmod{{{m}}}$."],
                  f"${ans}$.", "using the exponent's remainder as the answer instead of the power's remainder.")
    return (p, ans, [(ans + 1) % m, (ans + 2) % m, (ans + m - 1) % m, 1 if ans != 1 else 0, (a * ans) % m], [f"Find the smallest $k$ with ${a}^k \\equiv 1 \\pmod{{{m}}}$."], sol)


def pw4(r):
    a = r.choice([3, 7, 9, 11, 13])
    n = r.randint(10, 300)
    ans = pow(a, n, 100)
    order = next(k for k in range(1, 101) if pow(a, k, 100) == 1)
    p = f"What are the last two digits of ${a}^{{{n}}}$? (Give the two-digit number they form.)"
    sol = explain(f"${a}^{{{n}}} \\bmod 100$.", f"the last two digits of powers of ${a}$ repeat with some period; find it, then reduce the exponent.",
                  [f"Multiply by ${a}$ repeatedly, keeping only the last two digits: " + ", ".join(f"{pow(a, k, 100):02d}" for k in range(1, min(order, 6) + 1)) + (", ..." if order > 6 else "") + f". The first time we get $01$ is at ${a}^{{{order}}}$.",
                   f"${n} = {order} \\cdot {n // order} + {n % order}$, so ${a}^{{{n}}} \\equiv {a}^{{{n % order}}} \\pmod{{100}}$.",
                   f"${a}^{{{n % order}}} \\bmod 100 = {ans}$."],
                  f"${ans:02d}$.", "using a cycle of length $4$, which only works for the last digit, not the last two.")
    return (p, ans, [(ans + 10) % 100, (ans + 20) % 100, pow(a, n % 4 or 4, 100) if pow(a, n % 4 or 4, 100) != ans else (ans + 40) % 100, (ans + 50) % 100, pow(a, n, 10) if pow(a, n, 10) != ans else (ans + 30) % 100],
            ["Work mod 100. Powers of " + str(a) + " repeat mod 100; find the cycle."], sol)


def pwc1(r):
    m = r.choice([5, 7, 13])
    n = r.randint(50, 999)
    a, bb = r.sample([2, 3, 4, 5, 6], 2)
    if m in (a, bb) or math.gcd(a, m) != 1 or math.gcd(bb, m) != 1:
        return None
    ra, rb = pow(a, n, m), pow(bb, n, m)
    ans = (ra + rb) % m
    oa = next(k for k in range(1, m) if pow(a, k, m) == 1)
    ob = next(k for k in range(1, m) if pow(bb, k, m) == 1)
    p = f"What is the remainder when ${a}^{{{n}}} + {bb}^{{{n}}}$ is divided by ${m}$?"
    sol = explain("the remainder of the sum.", "handle each power separately with its repeating cycle, then add.",
                  [f"${a}^{{{oa}}} \\equiv 1 \\pmod{{{m}}}$, and ${n} \\equiv {n % oa} \\pmod{{{oa}}}$, so ${a}^{{{n}}} \\equiv {a}^{{{n % oa}}} \\equiv {ra}$.",
                   f"${bb}^{{{ob}}} \\equiv 1 \\pmod{{{m}}}$, and ${n} \\equiv {n % ob} \\pmod{{{ob}}}$, so ${bb}^{{{n}}} \\equiv {bb}^{{{n % ob}}} \\equiv {rb}$.",
                   f"Sum: ${ra} + {rb} = {ra + rb} \\equiv {ans} \\pmod{{{m}}}$."],
                  f"${ans}$.", "using the same cycle length for both bases. Each base has its own period.")
    return (p, ans, [(ans + 1) % m, (ans + 2) % m, (ans + 3) % m, (ans + m - 1) % m, (ans + m - 2) % m], [f"Use cycles of powers mod ${m}$ for each term."], sol)


def pwc2(r):
    a = r.choice([7, 3, 9, 13, 17, 23])
    n = r.randint(20, 400)
    last2 = pow(a, n, 100)
    ans = last2 // 10
    order = next(k for k in range(1, 101) if pow(a, k, 100) == 1)
    p = f"What is the tens digit of ${a}^{{{n}}}$?"
    sol = explain(f"the second to last digit of ${a}^{{{n}}}$.", "the tens digit comes from the last two digits, so work mod $100$.",
                  [f"Powers of ${a}$ mod $100$ repeat every ${order}$ (since ${a}^{{{order}}} \\equiv 01$).", f"${n} \\equiv {n % order} \\pmod{{{order}}}$, so ${a}^{{{n}}} \\equiv {a}^{{{n % order}}} \\equiv {last2:02d} \\pmod{{100}}$.",
                   f"The last two digits are ${last2:02d}$, so the tens digit is ${ans}$."],
                  f"${ans}$.", "giving the units digit instead of the tens digit.")
    return (p, ans, [d for d in range(10) if d != ans][:5], ["Find the last two digits by working mod 100."], sol)


def pwc3(r):
    trip = r.choice([(2, 3, 5), (3, 4, 6), (2, 5, 7), (3, 5, 7), (2, 3, 7)])
    e = r.choice([(60, 40, 24), (30, 20, 15), (12, 8, 6)])
    vals = list(zip(trip, e))
    for b_, x_ in [(trip[0] * trip[1], e[2]), (trip[2], e[0] // 2)]:
        vals.append((b_, x_))
    if len(set(vals)) < len(vals) or len({round(t[1] * math.log(t[0]), 9) for t in vals}) < len(vals):
        return None
    logs = sorted(t[1] * math.log(t[0]) for t in vals)
    if logs[-1] - logs[-2] < 1e-9:
        return None
    best = max(vals, key=lambda t: t[1] * math.log(t[0]))
    g = math.gcd(*[t[1] for t in vals])
    choices = [text_choice(f"${b_}^{{{x_}}}$", i) for i, (b_, x_) in enumerate(vals) if (b_, x_) != best]
    if len(choices) < 4:
        return None
    reduced = [f"${b_}^{{{x_}}} = ({b_}^{{{x_ // g}}})^{{{g}}} = {b_ ** (x_ // g)}^{{{g}}}$" for b_, x_ in vals]
    p = "Which of these numbers is the largest?"
    sol = explain("the largest of several huge powers.", f"write every number with the same outer exponent ${g}$ (the GCD of the exponents). Then just compare the insides.",
                  ["Rewrite: " + "; ".join(reduced) + ".", f"With the same exponent ${g}$, the biggest base wins: ${best[0] ** (best[1] // g)}$ is the largest inside value."],
                  f"${best[0]}^{{{best[1]}}}$.", "picking the one with the biggest exponent or the biggest base alone. Both matter together.")
    return (p, text_choice(f"${best[0]}^{{{best[1]}}}$", 99), choices[:4], ["Rewrite each number with the same exponent by taking a common root."], sol, False)


b.fill_unique("basics", [pw1, pw2, pw3, pw4] + MORE[b.skill_id]["basics"], 2501)
b.fill_unique("challenge", [pwc1, pwc2, pwc3] + MORE[b.skill_id]["challenge"], 2502)


# ---------------------------------------------------------------- number bases
b = bank("nt_bases")


def to_base(n, k):
    if n == 0:
        return "0"
    out = ""
    while n:
        out = "0123456789ABCDEF"[n % k] + out
        n //= k
    return out


def ba1(r):
    k = r.randint(2, 9)
    n = r.randint(10, 400)
    s = to_base(n, k)
    terms = [(int(dg), len(s) - 1 - i) for i, dg in enumerate(s)]
    p = f"What is the base-ten value of ${s}_{{{k}}}$?"
    sol = explain(f"the ordinary value of ${s}_{{{k}}}$.", f"in base ${k}$ the places from right to left are worth $1, {k}, {k}^2, \\ldots$",
                  ["Expand: $" + " + ".join(f"{dg} \\cdot {k}^{{{e}}}" for dg, e in terms) + "$.", "Evaluate: $" + " + ".join(str(dg * k ** e) for dg, e in terms) + f" = {n}$."],
                  f"${n}$.", f"reading it as the base ten number ${int(s)}$.")
    return (p, n, [int(s), n + k, n - 1, n + 1, int(s, k + 1) if all(int(c) < k + 1 for c in s) else n * 2], ["Each place is a power of the base."], sol)


def ba2(r):
    k = r.randint(2, 9)
    n = r.randint(20, 500)
    s = to_base(n, k)
    steps_div = []
    x = n
    while x:
        steps_div.append(f"${x} \\div {k} = {x // k}$ R ${x % k}$")
        x //= k
    wrong = [int(to_base(n + 1, k)), int(to_base(n - 1, k)), int(s[::-1]) if s[::-1][0] != "0" else int(to_base(n + 2, k)), int(to_base(n, k + 1)) if k < 9 else int(to_base(n + 3, k))]
    p = f"What is ${n}$ written in base ${k}$?"
    sol = explain(f"the base ${k}$ digits of ${n}$.", f"divide by ${k}$ again and again; the remainders are the digits, read from last to first.",
                  ["Divisions: " + "; ".join(steps_div) + ".", f"Read the remainders from the bottom up: ${s}_{{{k}}}$.", f"Check: " + " + ".join(f"{dg} \\cdot {k}^{{{len(s) - 1 - i}}}" for i, dg in enumerate(s)).join("$$") + f" $= {n}$."],
                  f"${s}_{{{k}}}$.", "reading the remainders top to bottom, which reverses the digits.")
    return (p, text_choice(f"${s}_{{{k}}}$", int(s)), [text_choice(f"${w}_{{{k}}}$", w) for w in wrong], ["Repeatedly divide by the base and read the remainders from the bottom up."], sol)


def ba3(r):
    k = r.randint(3, 9)
    d = r.randint(2, 4)
    ask = r.choice(["largest", "smallest"])
    ans = k ** d - 1 if ask == "largest" else k ** (d - 1)
    digits = (str(k - 1) * d) if ask == "largest" else "1" + "0" * (d - 1)
    p = f"What is the {ask} {d}-digit number in base ${k}$, written in base ten?"
    sol = explain(f"the {ask} base ${k}$ number with exactly ${d}$ digits.", f"base ${k}$ digits go from $0$ to ${k - 1}$, and the first digit can't be $0$.",
                  [f"The {ask} is ${digits}_{{{k}}}$.", (f"That is one less than $1\\underbrace{{0 \\cdots 0}}_{{{d}}}{{}}_{{{k}}} = {k}^{{{d}}}$, so it equals ${k ** d} - 1 = {ans}$." if ask == "largest" else f"That is ${k}^{{{d - 1}}} = {ans}$.")],
                  f"${ans}$.", "thinking in base ten (like $999$ or $100$).")
    return (p, ans, [k ** d, k ** (d - 1) - 1 if ask == "largest" else k ** d - 1, 10 ** d - 1 if ask == "largest" else 10 ** (d - 1), ans + k, d * k], [f"A {d}-digit base-{k} number is at least ${k}^{{{d - 1}}}$ and less than ${k}^{{{d}}}$."], sol)


def ba4(r):
    k = r.randint(4, 9)
    a, bb = r.randint(10, 200), r.randint(10, 200)
    s = to_base(a + bb, k)
    sa, sb = to_base(a, k), to_base(bb, k)
    wrong = [to_base(a + bb + 1, k), to_base(a + bb - 1, k), str(int(sa) + int(sb)), to_base(a + bb + k, k)]
    wrong = [w for w in wrong if w != s]
    p = f"In base ${k}$, what is ${sa}_{{{k}}} + {sb}_{{{k}}}$?"
    sol = explain(f"the sum, written in base ${k}$.", "the safest way: convert to base ten, add, convert back. (Or add column by column, carrying a $1$ whenever a column reaches " + str(k) + ".)",
                  [f"${sa}_{{{k}}} = {a}$ and ${sb}_{{{k}}} = {bb}$.", f"Sum in base ten: ${a + bb}$.", f"Convert back: ${a + bb} = {s}_{{{k}}}$."],
                  f"${s}_{{{k}}}$.", "adding as if in base ten and carrying at $10$ instead of at " + str(k) + ".")
    return (p, text_choice(f"${s}_{{{k}}}$", a + bb), [text_choice(f"${w}_{{{k}}}$", int(w, 10) + 1000) for w in wrong], [f"Add column by column, carrying whenever a column reaches ${k}$."], sol)


def bac1(r):
    bse = r.randint(5, 16)
    d1, d2 = r.randint(1, 4), r.randint(1, 4)
    val = d1 * bse + d2
    p = f"In some base $b$, the number ${d1}{d2}_b$ equals ${val}$ in base ten. What is $b$?"
    sol = explain("the base $b$.", "a two digit number $\\overline{xy}_b$ is worth $xb + y$.",
                  [f"${d1}{d2}_b = {d1}b + {d2}$.", f"Set equal: ${d1}b + {d2} = {val}$, so ${d1}b = {val - d2}$ and $b = {bse}$.", f"Check: the digits ${d1}$ and ${d2}$ are less than ${bse}$, so this is a valid base."],
                  f"$b = {bse}$.", "forgetting to subtract the ones digit first.")
    return (p, bse, [bse + 1, bse - 1, val // d1 if val // d1 != bse else bse + 3, bse + 2, 10], [f"${d1}{d2}_b = {d1}b + {d2}$."], sol)


def bac2(r):
    k = r.choice([2, 3])
    N = r.randint(50, 300)
    ask = r.choice(["ones", "digits"])
    if ask == "digits":
        ans = len(to_base(N, k))
        p = f"How many digits does ${N}$ have when written in base ${k}$?"
        sol = explain(f"the number of base ${k}$ digits of ${N}$.", f"a number has $d$ digits in base ${k}$ when ${k}^{{d - 1}} \\le N < {k}^d$.",
                      [f"Powers of ${k}$: " + ", ".join(f"${k}^{{{i}}} = {k ** i}$" for i in range(ans + 1)) + ".", f"${k}^{{{ans - 1}}} = {k ** (ans - 1)} \\le {N} < {k ** ans}$, so there are ${ans}$ digits. ($({N} = {to_base(N, k)}_{{{k}}})$.)"],
                      f"${ans}$.", "counting the base ten digits.")
        return (p, ans, [ans + 1, ans - 1, len(str(N)) if len(str(N)) != ans else ans + 2, ans + 3, int(math.log(N, k)) if int(math.log(N, k)) != ans else ans - 2], [f"Find the largest power of ${k}$ that is at most ${N}$."], sol)
    ans = sum(1 for n in range(1, N + 1) if to_base(n, 2).count("1") == 2)
    L = len(to_base(N, 2))
    full = math.comb(L - 1, 2)
    p = f"How many integers from $1$ to ${N}$ have exactly two 1s when written in base $2$?"
    sol = explain("numbers with exactly two $1$s in binary, up to " + f"${N}$.", "such a number is $2^i + 2^j$ with $i > j \\ge 0$: choose two places for the $1$s.",
                  [f"${N} = {to_base(N, 2)}_2$ has ${L}$ binary digits.", f"Numbers with at most ${L - 1}$ binary digits are all below ${N}$: choose $2$ of ${L - 1}$ places, $\\binom{{{L - 1}}}{{2}} = {full}$.",
                   f"Numbers $2^{{{L - 1}}} + 2^j$ with ${L}$ digits: check which are at most ${N}$; there are ${ans - full}$.", f"Total: ${full} + {ans - full} = {ans}$."],
                  f"${ans}$.", f"counting $\\binom{{{L}}}{{2}}$, which includes numbers bigger than ${N}$.")
    return (p, ans, [ans + 1, ans - 1, ans + 2, L if L != ans else ans + 3, ans * 2], ["Such numbers are sums of two different powers of 2."], sol)


def bac3(r):
    for _ in range(200):
        b1, b2 = r.sample(range(3, 10), 2)
        n = r.randint(10, 300)
        s1, s2 = to_base(n, b1), to_base(n, b2)
        if len(s1) == 2 and s2 == s1[::-1]:
            x, y = int(s1[0]), int(s1[1])
            p = f"A number $N$ is written as ${s1}$ in base ${b1}$ and as ${s2}$ in base ${b2}$. What is $N$ in base ten?"
            sol = explain("the value of $N$.", "write each base expansion as a formula and evaluate.",
                          [f"${s1}_{{{b1}}} = {x} \\cdot {b1} + {y} = {n}$.", f"Check the other form: ${s2}_{{{b2}}} = {y} \\cdot {b2} + {x} = {n}$. They agree."],
                          f"${n}$.", f"reading ${s1}$ as a base ten number.")
            return (p, n, [int(s1), int(s2), n + 1, n - b1, int(s1, b2) if all(int(c) < b2 for c in s1) and int(s1, b2) != n else n + b2], ["Set the two base expansions equal."], sol)
    return None


b.fill_unique("basics", [ba1, ba2, ba3, ba4] + MORE[b.skill_id]["basics"], 2601)
b.fill_unique("challenge", [bac1, bac2, bac3] + MORE[b.skill_id]["challenge"], 2602)


# ---------------------------------------------------------------- factorials
b = bank("nt_factorials")


def legendre(n, p_):
    s, q = 0, p_
    while q <= n:
        s += n // q
        q *= p_
    return s


def legendre_steps(n, p_):
    out, q = [], p_
    while q <= n:
        out.append((q, n // q))
        q *= p_
    return out


def fc1(r):
    n = r.randint(15, 200)
    z = legendre(n, 5)
    parts = legendre_steps(n, 5)
    p = f"How many zeros are at the end of ${n}!$?"
    sol = explain(f"the number of trailing zeros of ${n}!$.", "each trailing zero is a factor of $10 = 2 \\cdot 5$. There are always more $2$s than $5$s, so count the factors of $5$.",
                  [f"Multiples of ${q}$ up to ${n}$: $\\lfloor {n}/{q} \\rfloor = {t}$." for q, t in parts] + [f"Add: ${' + '.join(str(t) for _, t in parts)} = {z}$. (Multiples of $25$ give an extra $5$, which is why we count them again.)"],
                  f"${z}$.", f"counting only multiples of $5$ (${n // 5}$) and missing the extra factors from $25$, $125$, ...")
    return (p, z, [n // 5 if n // 5 != z else z + 2, z + 1, z - 1, legendre(n, 2), n // 10], ["Each zero needs a factor of 10 = 2 × 5, and factors of 5 are scarcer. Count them, including extra 5s from 25, 125, and so on."], sol)


def fc2(r):
    a = r.randint(5, 12)
    k = r.randint(1, 3)
    bb = a + k
    ans = math.factorial(bb) // math.factorial(a)
    p = f"What is $\\dfrac{{{bb}!}}{{{a}!}}$?"
    sol = explain("the value of the fraction of factorials.", f"${bb}! = {bb} \\cdot {bb - 1} \\cdots 1$ contains ${a}!$ as its tail, so most factors cancel.",
                  [f"${bb}! = " + " \\cdot ".join(str(x) for x in range(bb, a, -1)) + f" \\cdot {a}!$.", f"Cancel ${a}!$: " + " \\cdot ".join(str(x) for x in range(a + 1, bb + 1)) + f" $= {ans}$.".join(["$", ""])],
                  f"${ans}$.", f"computing $({bb} - {a})! = {math.factorial(k)}$. Factorials don't subtract like that.")
    return (p, ans, [math.factorial(k), bb - a, ans // bb, ans * (bb + 1), a * bb], ["Cancel the common factors of the factorials."], sol)


def fc3(r):
    n = r.randint(8, 60)
    p_ = r.choice([2, 3, 7])
    e = legendre(n, p_)
    parts = legendre_steps(n, p_)
    p = f"What is the largest power of ${p_}$ that divides ${n}!$? (Give the exponent.)"
    sol = explain(f"how many factors of ${p_}$ are in $1 \\cdot 2 \\cdots {n}$.", f"Legendre's formula: count multiples of ${p_}$, then add one more for each multiple of ${p_}^2$, and so on.",
                  [f"Multiples of ${q}$: $\\lfloor {n}/{q} \\rfloor = {t}$." for q, t in parts] + [f"Total: ${' + '.join(str(t) for _, t in parts)} = {e}$."],
                  f"${e}$.", f"counting only the multiples of ${p_}$, which misses the extra factors in ${p_ * p_}$ and beyond.")
    return (p, e, [n // p_ if n // p_ != e else e + 2, e + 1, e - 1, legendre(n, 5), e * 2], ["Count multiples of $p$, then $p^2$, then $p^3$, and so on."], sol)


def fc4(r):
    m = r.choice([36, 48, 72, 99, 121, 169, 250, 343, 400, 1000, 2024, 588])
    n = next(k for k in range(1, 200) if math.factorial(k) % m == 0)
    f = sorted(factor(m).items())
    need = []
    for q, e in f:
        first = next(k for k in range(1, 200) if legendre(k, q) >= e)
        need.append(f"${q}^{{{e}}}$ needs $n \\ge {first}$")
    p = f"What is the smallest positive integer $n$ such that $n!$ is a multiple of ${m}$?"
    sol = explain(f"the first $n$ with ${m} \\mid n!$.", "factor the target; $n!$ must contain enough of each prime. The answer is the most demanding prime's requirement.",
                  [f"${m} = {ftex(m)}$.", "For each prime power: " + "; ".join(need) + ".", f"The largest requirement is $n = {n}$."],
                  f"${n}$.", f"stopping at the largest prime factor; a squared prime like ${max(factor(m))}^2$ needs two multiples of it." if any(e > 1 for _, e in f) else "missing that every prime factor must be covered.")
    return (p, n, [n + 1, n - 1, max(factor(m)) if max(factor(m)) != n else n + 2, n + 2, sum(factor(m).values()) if sum(factor(m).values()) != n else n - 2], [f"Factor ${m} = {ftex(m)}$ and find when $n!$ has enough of each prime."], sol)


def fcc1(r):
    n = r.randint(10, 200)
    m = r.choice([7, 9, 11, 13])
    cut = next(k for k in range(1, 50) if math.factorial(k) % m == 0)
    small = [math.factorial(k) % m for k in range(1, min(n, cut - 1) + 1)]
    total = sum(math.factorial(k) for k in range(1, n + 1)) % m
    p = f"What is the remainder when $1! + 2! + 3! + \\cdots + {n}!$ is divided by ${m}$?"
    sol = explain("the remainder of a huge sum of factorials.", f"from ${cut}!$ on, every factorial is a multiple of ${m}$, so those terms add $0$ to the remainder.",
                  [f"${cut}! $ is the first factorial divisible by ${m}$, and all later ones contain it.", f"Remainders of $1!, 2!, \\ldots, {cut - 1}!$ mod ${m}$: " + ", ".join(map(str, small)) + ".",
                   f"Add them: ${sum(small)} \\equiv {total} \\pmod{{{m}}}$."],
                  f"${total}$.", f"stopping at ${m - 1}!$ when ${m}$ is not prime: a smaller factorial can already be divisible by ${m}$." if m == 9 else "including terms that are already multiples of " + str(m) + ".")
    return (p, total, [(total + 1) % m, (total + 2) % m, (total + m - 1) % m, (total + 3) % m, 0 if total else 1], [f"From some point on, $k!$ is a multiple of ${m}$, so only the first few terms matter."], sol)


def fcc2(r):
    n = r.randint(10, 60)
    bse = r.choice([6, 12, 8, 9, 16, 18])
    fb = factor(bse)
    z = min(legendre(n, p_) // e for p_, e in fb.items())
    p = f"How many zeros are at the end of ${n}!$ when it is written in base ${bse}$?"
    sol = explain(f"how many times ${bse}$ divides ${n}!$.", f"a trailing zero in base ${bse}$ is a factor of ${bse}$. Count each prime in ${n}!$ and see how many copies of ${bse} = {ftex(bse)}$ you can build.",
                  [f"Prime ${q}$ appears ${legendre(n, q)}$ times in ${n}!$; each copy of ${bse}$ uses ${e}$, allowing $\\lfloor {legendre(n, q)}/{e} \\rfloor = {legendre(n, q) // e}$ copies." for q, e in sorted(fb.items())]
                  + [f"The scarcest prime limits us: ${z}$."],
                  f"${z}$.", "counting factors of $5$ out of habit; trailing zeros depend on the base.")
    return (p, z, [z + 1, z - 1, legendre(n, 5), legendre(n, max(fb)) if legendre(n, max(fb)) != z else z + 2, z * 2], [f"Count how many times ${bse} = {ftex(bse)}$ divides ${n}!$."], sol)


def fcc3(r):
    k = r.randint(5, 60)
    ns = [n for n in range(1, 400) if legendre(n, 5) == k]
    p = f"For how many positive integers $n$ does $n!$ end in exactly ${k}$ zeros?"
    if ns:
        ans = len(ns)
        sol = explain(f"how many $n$ give exactly ${k}$ trailing zeros.", "the zero count only changes when $n$ reaches a multiple of $5$, and then it stays the same for $5$ numbers in a row.",
                      [f"$\\lfloor {ns[0]}/5 \\rfloor + \\lfloor {ns[0]}/25 \\rfloor + \\cdots = {k}$, and $n = {ns[0] - 1}$ gives {legendre(ns[0] - 1, 5)}.", f"The count stays ${k}$ until the next multiple of $5$: $n = {ns[0]}$ through ${ns[-1]}$."],
                      f"${ans}$.", "assuming every zero count is reached. Some counts are skipped at multiples of $25$.")
        return (p, ans, [0, 1 if ans != 1 else 4, 2, 3, 6], ["The number of trailing zeros only changes when $n$ passes a multiple of 5."], sol)
    jump = next(n for n in range(5, 400, 5) if legendre(n, 5) > k)
    sol = explain(f"how many $n$ give exactly ${k}$ trailing zeros.", "at a multiple of $25$, the zero count jumps by $2$ or more, skipping some values.",
                  [f"$n = {jump - 1}$ gives ${legendre(jump - 1, 5)}$ zeros, and $n = {jump}$ gives ${legendre(jump, 5)}$ zeros.", f"${k}$ is skipped, so no $n$ works."],
                  "$0$.", "assuming every number of zeros happens for exactly five values of $n$.")
    return (p, 0, [5, 1, 4, 2, 3], ["The number of trailing zeros jumps by more than 1 at multiples of 25."], sol)


b.fill_unique("basics", [fc1, fc2, fc3, fc4] + MORE[b.skill_id]["basics"], 2701)
b.fill_unique("challenge", [fcc1, fcc2, fcc3] + MORE[b.skill_id]["challenge"], 2702)
