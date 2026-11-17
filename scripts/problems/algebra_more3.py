"""Extra Algebra problem types (part 3): mean/median/mode, sequences, functions."""
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


def lst(xs):
    return ", ".join(str(x) for x in xs)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


# ================================================================ alg_stats
S = "alg_stats"


@reg(S, "basics")
def st_median_even(r):
    xs = r.sample(range(1, 60), r.choice([6, 8]))
    m = median(xs)
    p = f"What is the median of $\\{{{lst(xs)}\\}}$?"
    s = sorted(xs)
    n = len(s)
    return Q(p, m, [F(sum(xs), n), F(xs[n // 2 - 1] + xs[n // 2], 2) if F(xs[n // 2 - 1] + xs[n // 2], 2) != m else m + 1, s[n // 2], s[n // 2 - 1], m + F(1, 2)], "Sort the list first.",
             "the median.", "sort the numbers; with an even count, the median is the average of the two middle numbers.",
             [f"Sorted: ${lst(s)}$.", f"Middle two: ${s[n // 2 - 1]}$ and ${s[n // 2]}$.", f"Median: $\\frac{{{s[n // 2 - 1]} + {s[n // 2]}}}{{2}} = {ftex(m)}$."],
             "taking the middle of the unsorted list.")


@reg(S, "basics")
def st_range(r):
    xs = [r.randint(-20, 60) for _ in range(r.randint(6, 9))]
    p = f"What is the range of the data set $\\{{{lst(xs)}\\}}$?"
    rg = max(xs) - min(xs)
    return Q(p, rg, [max(xs), max(xs) + min(xs) if max(xs) + min(xs) != rg else rg + 3, rg + 1, abs(min(xs)), max(xs) - sorted(xs)[1]], "Largest minus smallest.",
             "the range.", "range $=$ maximum $-$ minimum.",
             [f"Largest: ${max(xs)}$. Smallest: ${min(xs)}$.", f"Range: ${max(xs)} - {par(min(xs))} = {rg}$."],
             "using the first and last numbers as listed instead of the largest and smallest.")


@reg(S, "basics")
def st_mean(r):
    n = r.randint(5, 8)
    m = r.randint(10, 40)
    xs = [m + r.randint(-12, 12) for _ in range(n - 1)]
    last = m * n - sum(xs)
    if last <= 0:
        return None
    xs.append(last)
    r.shuffle(xs)
    p = f"What is the mean of ${lst(xs)}$?"
    return Q(p, m, [median(xs) if median(xs) != m else m + 2, F(sum(xs), n - 1), m + 1, F(max(xs) + min(xs), 2) if F(max(xs) + min(xs), 2) != m else m - 1, sum(xs) // 10], "Add them and divide by how many there are.",
             "the mean.", "mean $= \\frac{\\text{sum}}{\\text{count}}$.",
             [f"Sum: ${sum(xs)}$.", f"Count: ${n}$.", f"Mean: $\\frac{{{sum(xs)}}}{{{n}}} = {m}$."],
             "dividing by the wrong count.")


@reg(S, "basics")
def st_shift(r):
    m = r.randint(20, 80)
    k = r.randint(2, 12)
    n = r.randint(5, 30)
    p = f"The mean of ${n}$ test scores is ${m}$. The teacher adds ${k}$ points to every score. What is the new mean?"
    return Q(p, m + k, [m, m + k * n, F(m + k, 2), m * k, m + F(k, n)], "Every score goes up by the same amount.",
             "the new mean.", "adding the same amount to every number adds that amount to the mean.",
             [f"The sum goes up by ${n} \\cdot {k}$, and dividing by ${n}$ adds ${k}$ to the mean.", f"New mean: ${m} + {k} = {m + k}$."],
             "adding " + str(k) + " to the sum only once.")


@reg(S, "basics")
def st_scale(r):
    m = r.randint(5, 40)
    k = r.choice([2, 3, 4, 5, 10])
    b = r.randint(-10, 10)
    p = f"A list of numbers has mean ${m}$. Each number is multiplied by ${k}$ and then ${b}$ is added. What is the new mean?" if b >= 0 else f"A list of numbers has mean ${m}$. Each number is multiplied by ${k}$ and then ${-b}$ is subtracted. What is the new mean?"
    return Q(p, k * m + b, [k * m, k * (m + b), m + b, k * m - b, k + m + b], "Do to the mean what you do to each number.",
             "the new mean.", "if every number is transformed by $x \\to kx + b$, the mean is transformed the same way.",
             [f"Multiplying every number by ${k}$ multiplies the mean: ${k * m}$.", f"Then {'adding' if b >= 0 else 'subtracting'} ${abs(b)}$: ${k * m + b}$."],
             "adding before multiplying.")


@reg(S, "basics")
def st_sum_from_mean(r):
    n, m = r.randint(4, 12), F(r.randint(20, 160), r.choice([1, 2]))
    if (n * m).denominator != 1:
        return None
    p = f"The mean of ${n}$ numbers is ${ftex(m)}$. What is their sum?"
    return Q(p, n * m, [m, m / n, n + m, n * m + n, (n - 1) * m], "Sum $=$ mean $\\times$ count.",
             "the sum.", "mean $= \\frac{\\text{sum}}{\\text{count}}$, so sum $=$ mean $\\times$ count.",
             [f"${ftex(m)} \\cdot {n} = {ftex(n * m)}$."], "dividing by the count.")


@reg(S, "basics")
def st_median_add(r):
    xs = sorted(r.sample(range(1, 50), r.choice([5, 7])))
    v = r.randint(50, 90)
    m1, m2 = median(xs), median(xs + [v])
    p = f"The list ${lst(xs)}$ has median ${ftex(m1)}$. If ${v}$ is added to the list, what is the new median?"
    return Q(p, m2, [m1, F(sum(xs) + v, len(xs) + 1), m1 + 1, xs[len(xs) // 2 + 1], F(m1 + v, 2)], "With one more number, the count becomes even.",
             "the new median.", "a list with an even count has its median halfway between the two middle numbers.",
             [f"New sorted list: ${lst(sorted(xs + [v]))}$, with ${len(xs) + 1}$ numbers.", f"Middle two: ${sorted(xs + [v])[len(xs) // 2]}$ and ${sorted(xs + [v])[len(xs) // 2 + 1]}$.", f"Median: ${ftex(m2)}$."],
             "assuming the median doesn't change.")


@reg(S, "basics")
def st_mode(r):
    base = r.sample(range(1, 30), 5)
    mode = base[0]
    xs = base + [mode, mode] + [base[1]]
    r.shuffle(xs)
    p = f"What is the mode of $\\{{{lst(xs)}\\}}$?"
    return Q(p, mode, [base[1], median(xs) if median(xs) != mode else mode + 1, F(sum(xs), len(xs)) if F(sum(xs), len(xs)) != mode else mode + 2, max(xs) if max(xs) != mode else mode - 1, len(xs)], "Count how often each value appears.",
             "the mode.", "the mode is the value that appears most often.",
             [f"${mode}$ appears $3$ times; ${base[1]}$ appears twice; every other value appears once.", f"Mode: ${mode}$."],
             "picking a value that appears twice.")


@reg(S, "basics")
def st_odd_avg(r):
    a = r.choice(range(1, 40, 2))
    n = r.randint(6, 20)
    b = a + 2 * (n - 1)
    p = f"What is the average of all the odd numbers from ${a}$ to ${b}$, inclusive?"
    return Q(p, F(a + b, 2), [F(a + b, 2) + 1, F(b - a, 2), n, F(a + b, 2) - 1, F(b, 2)], "Evenly spaced numbers average to the middle.",
             "the average.", "for an evenly spaced list, the average is the average of the first and last.",
             [f"$\\frac{{{a} + {b}}}{{2}} = {ftex(F(a + b, 2))}$."], "dividing by the wrong count after adding them by hand.")


@reg(S, "basics")
def st_weighted(r):
    w1 = r.choice([40, 50, 60, 70, 75, 80])
    t, h = r.randint(60, 98), r.randint(60, 100)
    ans = F(w1 * t + (100 - w1) * h, 100)
    n = r.choice(NAMES)
    p = f"Tests count for ${w1}\\%$ of a grade and homework for ${100 - w1}\\%$. {n} averages ${t}$ on tests and ${h}$ on homework. What is {n}'s grade?"
    return Q(p, ans, [F(t + h, 2), ans + 1, F((100 - w1) * t + w1 * h, 100), max(t, h), min(t, h)], "Multiply each average by its weight.",
             "the weighted grade.", "weighted average: multiply each part by its weight and add.",
             [f"${ftex(F(w1, 100))} \\cdot {t} = {ftex(F(w1 * t, 100))}$.", f"${ftex(F(100 - w1, 100))} \\cdot {h} = {ftex(F((100 - w1) * h, 100))}$.", f"Grade: ${ftex(ans)}$."],
             "averaging the two scores equally.")


@reg(S, "basics")
def st_first_n(r):
    n = r.randint(5, 99)
    ans = F(n + 1, 2)
    p = f"What is the mean of the integers $1, 2, 3, \\ldots, {n}$?"
    return Q(p, ans, [F(n, 2), F(n * (n + 1), 2), ans + 1, n, F(n - 1, 2)], "Average the first and last.",
             "the mean.", "the sum is $\\frac{n(n + 1)}{2}$; dividing by $n$ gives $\\frac{n + 1}{2}$.",
             [f"Sum: $\\frac{{{n} \\cdot {n + 1}}}{{2}} = {n * (n + 1) // 2}$.", f"Mean: $\\frac{{{n * (n + 1) // 2}}}{{{n}}} = {ftex(ans)}$."],
             "answering $\\frac{n}{2}$.")


@reg(S, "basics")
def st_freq_mean(r):
    vals = sorted(r.sample(range(1, 10), 3))
    cnts = [r.randint(1, 8) for _ in vals]
    tot = sum(v * c for v, c in zip(vals, cnts))
    m = F(tot, sum(cnts))
    p = "A survey asked students how many books they read. " + "; ".join(f"${c}$ students read ${v}$" for v, c in zip(vals, cnts)) + ". What is the mean number of books per student?"
    return Q(p, m, [F(sum(vals), 3), F(tot, 3), m + 1, F(sum(cnts), 3), median([v for v, c in zip(vals, cnts) for _ in range(c)]) if median([v for v, c in zip(vals, cnts) for _ in range(c)]) != m else m - F(1, 2)],
             "Multiply each value by how many students gave it.", "the mean.", "weighted mean: total books divided by total students.",
             [f"Total books: " + " + ".join(f"{v} \\cdot {c}" for v, c in zip(vals, cnts)) .join(["$", f" = {tot}$"]) + ".", f"Students: ${sum(cnts)}$.", f"Mean: $\\frac{{{tot}}}{{{sum(cnts)}}} = {ftex(m)}$."],
             "averaging the three book counts without the student counts.")


@reg(S, "basics")
def st_other_number(r):
    a, b = r.sample(range(-20, 60), 2)
    avg = F(a + b, 2)
    p = f"The average of two numbers is ${ftex(avg)}$. One of them is ${a}$. What is the other?"
    return Q(p, b, [avg - (a - avg) + 1 if b != avg - (a - avg) + 1 else b + 2, 2 * avg + a, avg, a - b, b - 1], "The two numbers add to twice the average.",
             "the other number.", "sum $= 2 \\times$ average.",
             [f"Sum: $2 \\cdot {ftex(avg)} = {a + b}$.", f"Other: ${a + b} - {par(a)} = {b}$."],
             "subtracting " + str(a) + " from the average instead of from the sum.")


@reg(S, "basics")
def st_range_from_mean(r):
    xs = [r.randint(10, 60) for _ in range(4)]
    m = r.randint(25, 50)
    last = 5 * m - sum(xs)
    if last <= 0:
        return None
    rg = max(xs + [last]) - min(xs + [last])
    p = f"Five numbers have a mean of ${m}$. Four of them are ${lst(xs)}$. What is the range of all five?"
    return Q(p, rg, [max(xs) - min(xs) if max(xs) - min(xs) != rg else rg + 1, last, rg + 2, abs(last - m), 5 * m], "Find the fifth number first.",
             "the range.", "use the mean to find the missing number, then take largest minus smallest.",
             [f"Sum of all five: $5 \\cdot {m} = {5 * m}$. Fifth number: ${5 * m} - {sum(xs)} = {last}$.", f"Largest: ${max(xs + [last])}$; smallest: ${min(xs + [last])}$.", f"Range: ${rg}$."],
             "finding the range of only the four given numbers.")


@reg(S, "basics")
def st_freq_median(r):
    vals = [1, 2, 3, 4, 5]
    cnts = [r.randint(1, 7) for _ in vals]
    data = [v for v, c in zip(vals, cnts) for _ in range(c)]
    if len(data) % 2 == 0:
        return None
    m = median(data)
    p = "Students rated a movie from 1 to 5 stars. " + ", ".join(f"${c}$ gave ${v}$" for v, c in zip(vals, cnts)) + ". What is the median rating?"
    return Q(p, m, [3, F(sum(data), len(data)) if F(sum(data), len(data)) != m else m + F(1, 2), max(vals, key=lambda v: cnts[v - 1]) if max(vals, key=lambda v: cnts[v - 1]) != m else m - 1, m + 1, F(len(data) + 1, 2)], "Find the middle position.",
             "the median rating.", "the median is the middle value when all ratings are listed in order.",
             [f"There are ${len(data)}$ ratings; the middle is position ${(len(data) + 1) // 2}$.", "Running totals: " + ", ".join(f"through ${v}$: ${sum(cnts[:i + 1])}$" for i, v in enumerate(vals)) + ".", f"Position ${(len(data) + 1) // 2}$ is a ${m}$."],
             "picking the middle rating value (3) without using the counts.")


@reg(S, "basics")
def st_ages_later(r):
    k = r.randint(3, 6)
    a = r.randint(15, 40)
    y = r.randint(2, 10)
    p = f"The average age of the ${k}$ members of a family is ${a}$. What will their average age be in ${y}$ years?"
    return Q(p, a + y, [a + k * y, a, a * y, a + F(y, k), a + y + k], "Everyone ages the same amount.",
             "the future average.", "each person gains " + str(y) + " years, so the average goes up by " + str(y) + ".",
             [f"Each age goes up by ${y}$, so the average does too: ${a} + {y} = {a + y}$."], "adding " + str(k * y) + " to the average (the total increase of the sum).")


@reg(S, "challenge")
def stc_mean_equals_mode(r):
    x = r.randint(8, 30)
    a = r.randint(1, 3 * x - 3)
    b = r.randint(1, 3 * x - a - 1)
    c = 3 * x - a - b
    xs = [x, a, b, c]
    if len(set(xs)) < 4 or c <= 0:
        return None
    r.shuffle(xs)
    p = f"The list ${lst(xs)}, x$ has a mean equal to its mode. What is $x$?"
    return Q(p, x, [F(sum(xs), 4), median(xs) if median(xs) != x else x + 1, x + 2, max(xs) if max(xs) != x else x - 1, sum(xs)], "For there to be a mode, $x$ must repeat one of the numbers.",
             "$x$.", "the four given numbers are different, so the only possible mode is $x$ itself, matching one of them.",
             [f"Mode $= x$, so $\\frac{{{sum(xs)} + x}}{{5}} = x$.", f"${sum(xs)} + x = 5x$, so $x = {ftex(F(sum(xs), 4))}$.", f"$x = {x}$ is in the list, so it really is the mode."],
             "forgetting to check that $x$ matches a number already in the list.")


@reg(S, "challenge")
def stc_distinct_max(r):
    n = r.randint(5, 8)
    m = r.randint(10, 30)
    ans = n * m - sum(range(1, n))
    p = f"${n}$ different positive integers have a mean of ${m}$. What is the largest possible value of the largest one?"
    return Q(p, ans, [n * m, ans + 1, n * m - n + 1, ans - (n - 1), m * 2], "Make the others as small as possible.",
             "the largest possible maximum.", "the sum is fixed, so to make one number big, make the others as small as possible while staying different.",
             [f"Sum: ${n} \\cdot {m} = {n * m}$.", f"Smallest possible others: $1, 2, \\ldots, {n - 1}$, summing to ${sum(range(1, n))}$.", f"Largest: ${n * m} - {sum(range(1, n))} = {ans}$."],
             "using $1$ for every other number, which breaks the 'different' condition.")


@reg(S, "challenge")
def stc_drop_ends(r):
    n = r.randint(6, 12)
    m = r.randint(40, 80)
    hi, lo = m + r.randint(10, 30), m - r.randint(10, 30)
    tot = n * m
    ans = F(tot - hi - lo, n - 2)
    p = f"Judges give ${n}$ scores with a mean of ${m}$. The highest score, ${hi}$, and the lowest, ${lo}$, are dropped. What is the mean of the rest?"
    return Q(p, ans, [m, F(tot - hi - lo, n), ans + 1, F(hi + lo, 2), m - F(hi - lo, n)], "Find the total first.",
             "the mean of the remaining scores.", "work with sums: subtract the dropped scores, then divide by the new count.",
             [f"Total: ${n} \\cdot {m} = {tot}$.", f"Remove ${hi}$ and ${lo}$: ${tot - hi - lo}$.", f"Mean of ${n - 2}$ scores: ${ftex(ans)}$."],
             "dividing by " + str(n) + " instead of " + str(n - 2) + ".")


@reg(S, "challenge")
def stc_pair_avgs(r):
    x, y, z = [r.randint(1, 60) for _ in range(3)]
    A, B, Cc = F(x + y, 2), F(y + z, 2), F(x + z, 2)
    p = f"The average of $x$ and $y$ is ${ftex(A)}$, of $y$ and $z$ is ${ftex(B)}$, and of $x$ and $z$ is ${ftex(Cc)}$. What is the average of $x$, $y$, and $z$?"
    ans = F(x + y + z, 3)
    return Q(p, ans, [F(A + B + Cc, 3) * 2 if F(A + B + Cc, 3) * 2 != ans else ans + 1, A + B + Cc, ans + F(1, 3), F(A + B + Cc, 2), max(A, B, Cc)], "Turn each average into a sum.",
             "the average of all three.", "add the three pair sums: each variable appears twice.",
             [f"$x + y = {x + y}$, $y + z = {y + z}$, $x + z = {x + z}$.", f"Adding: $2(x + y + z) = {2 * (x + y + z)}$, so $x + y + z = {x + y + z}$.", f"Average: ${ftex(ans)}$."],
             "averaging the three averages, which equals the average already (a coincidence only if you double count correctly).")


@reg(S, "challenge")
def stc_class_size(r):
    n = r.randint(10, 40)
    d = F(r.choice([1, 2, 3, 4, 5]), r.choice([1, 2, 4]))
    k = n * d
    if k.denominator != 1:
        return None
    p = f"If one student in a class had scored ${k}$ more points on a test, the class average would have gone up by ${ftex(d)}$ points. How many students are in the class?"
    return Q(p, n, [k, F(k, 2) if F(k, 2) != n else n + 2, n + 1, k * d, n * 2], "Extra points spread over the whole class.",
             "the class size.", "raising the total by $k$ raises the mean by $\\frac{k}{n}$.",
             [f"$\\frac{{{k}}}{{n}} = {ftex(d)}$.", f"$n = \\frac{{{k}}}{{{ftex(d)}}} = {n}$."],
             "multiplying instead of dividing.")


@reg(S, "challenge")
def stc_group_ratio(r):
    b_avg, g_avg = r.sample(range(60, 96), 2)
    if b_avg > g_avg:
        b_avg, g_avg = g_avg, b_avg
    bb, gg = r.randint(1, 5), r.randint(1, 5)
    avg = F(bb * b_avg + gg * g_avg, bb + gg)
    ratio = F(bb, gg)
    p = f"On a test the boys averaged ${b_avg}$, the girls averaged ${g_avg}$, and the whole class averaged ${ftex(avg)}$. What is the ratio of boys to girls, as a single number (boys divided by girls)?"
    return Q(p, ratio, [1 / ratio if ratio != 1 else 2, F(b_avg, g_avg), ratio + 1, F(g_avg - b_avg, 10), F(1, 2) if ratio != F(1, 2) else 3], "The overall average sits between the two, closer to the bigger group.",
             "boys $\\div$ girls.", "weighted average: $b \\cdot " + str(b_avg) + " + g \\cdot " + str(g_avg) + " = (b + g) \\cdot " + ftex(avg) + "$.",
             [f"$b({ftex(avg)} - {b_avg}) = g({g_avg} - {ftex(avg)})$.", f"$\\frac{{b}}{{g}} = \\frac{{{ftex(g_avg - avg)}}}{{{ftex(avg - b_avg)}}} = {ftex(ratio)}$."],
             "flipping the ratio: the group farther from the overall average is the smaller group.")


@reg(S, "challenge")
def stc_misread(r):
    n = r.randint(8, 25)
    m = F(r.randint(40, 90))
    pv, qv = r.sample(range(10, 99), 2)
    new = m + F(pv - qv, n)
    p = f"The mean of ${n}$ numbers was computed as ${ftex(m)}$, but one number was misread as ${qv}$ when it was really ${pv}$. What is the correct mean?"
    return Q(p, new, [m + pv - qv, m - F(pv - qv, n), new + 1, F(n * m + pv, n + 1), m], "Fix the total, not the mean.",
             "the corrected mean.", "the wrong total was too " + ("low" if pv > qv else "high") + " by " + str(abs(pv - qv)) + "; fix it, then divide.",
             [f"Wrong total: ${n} \\cdot {ftex(m)} = {ftex(n * m)}$.", f"Correct total: ${ftex(n * m)} + ({pv} - {qv}) = {ftex(n * m + pv - qv)}$.", f"Correct mean: ${ftex(new)}$."],
             "adding the difference to the mean without dividing by " + str(n) + ".")


# ================================================================ alg_sequences
S = "alg_sequences"


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


@reg(S, "basics")
def sq_diff_from_terms(r):
    a1, d = r.randint(-10, 20), r.choice([x for x in range(-7, 8) if x])
    k = r.randint(5, 20)
    ak = a1 + (k - 1) * d
    p = f"An arithmetic sequence has first term ${a1}$ and {ordinal(k)} term ${ak}$. What is the common difference?"
    return Q(p, d, [F(ak - a1, k), -d, d + 1, ak - a1, F(ak, k)], f"There are ${k - 1}$ steps from term 1 to term {k}.",
             "the common difference $d$.", "term $k$ is the first term plus $(k - 1)$ steps of $d$.",
             [f"${a1} + {k - 1}d = {ak}$.", f"${k - 1}d = {ak - a1}$, so $d = {d}$."],
             "dividing by " + str(k) + " instead of " + str(k - 1) + ".")


@reg(S, "basics")
def sq_which_term(r):
    a1, d = r.randint(-5, 15), r.randint(2, 9)
    k = r.randint(10, 60)
    N = a1 + (k - 1) * d
    p = f"Which term of the arithmetic sequence ${a1}, {a1 + d}, {a1 + 2 * d}, \\ldots$ is ${N}$?"
    return Q(p, k, [k - 1, k + 1, F(N, d) if F(N, d) != k else k + 2, N - a1, F(N - a1, d) + 2], "How many steps of " + str(d) + " get you there?",
             "the position of " + str(N) + ".", "the number of steps is $\\frac{N - a_1}{d}$, and the position is one more than that.",
             [f"Steps: $\\frac{{{N} - {par(a1)}}}{{{d}}} = {k - 1}$.", f"Position: ${k - 1} + 1 = {k}$."],
             "forgetting to add $1$ for the first term.")


@reg(S, "basics")
def sq_odd_sum(r):
    n = r.randint(5, 60)
    last = 2 * n - 1
    p = f"What is $1 + 3 + 5 + \\cdots + {last}$?"
    return Q(p, n * n, [last * last, n * (n + 1), n * n + n, F(last * (last + 1), 2), n * n - 1], "How many odd numbers are there?",
             "the sum of the odd numbers.", "the first $n$ odd numbers add to $n^2$.",
             [f"Number of terms: $\\frac{{{last} + 1}}{{2}} = {n}$.", f"Sum: average $\\times$ count $= \\frac{{1 + {last}}}{{2}} \\cdot {n} = {n} \\cdot {n} = {n * n}$."],
             "squaring the last term.")


@reg(S, "basics")
def sq_geo_ratio(r):
    a, rr = r.randint(1, 6), r.choice([2, 3, 4, 5])
    i, j = 2, r.randint(4, 6)
    ai, aj = a * rr ** (i - 1), a * rr ** (j - 1)
    p = f"A geometric sequence of positive numbers has {ordinal(i)} term ${ai}$ and {ordinal(j)} term ${aj}$. What is the common ratio?"
    return Q(p, rr, [F(aj - ai, j - i), rr * rr, F(aj, ai), rr + 1, j - i], f"From term {i} to term {j} you multiply by the ratio ${j - i}$ times.",
             "the ratio $r$.", "each step multiplies by $r$.",
             [f"$a_{j} = a_{i} \\cdot r^{{{j - i}}}$, so $r^{{{j - i}}} = \\frac{{{aj}}}{{{ai}}} = {aj // ai}$.", f"$r = \\sqrt[{j - i}]{{{aj // ai}}} = {rr}$."],
             "dividing the terms and forgetting the root.")


@reg(S, "basics")
def sq_geo_sum(r):
    a, rr, n = r.randint(1, 5), r.choice([2, 3]), r.randint(4, 8)
    S_ = a * (rr ** n - 1) // (rr - 1)
    terms = [a * rr ** i for i in range(n)]
    p = f"What is ${' + '.join(map(str, terms))}$?"
    return Q(p, S_, [S_ + a, terms[-1] * rr, S_ - a, a * rr ** n, S_ + terms[-1]], "Use the geometric sum formula, or add carefully.",
             "the sum.", "$a + ar + \\cdots + ar^{n-1} = a \\cdot \\frac{r^n - 1}{r - 1}$.",
             [f"$a = {a}$, $r = {rr}$, $n = {n}$.", f"${a} \\cdot \\frac{{{rr}^{{{n}}} - 1}}{{{rr - 1}}} = {a} \\cdot \\frac{{{rr ** n - 1}}}{{{rr - 1}}} = {S_}$."],
             "using $r^{n+1}$ or $r^{n-1}$ in the formula.")


@reg(S, "basics")
def sq_arith_mean(r):
    a, b = r.sample(range(-30, 60), 2)
    if (a + b) % 2:
        b += 1
    p = f"If ${a}, x, {b}$ is an arithmetic sequence, what is $x$?"
    return Q(p, F(a + b, 2), [b - a, F(b - a, 2), a + b, F(a + b, 2) + 1, F(a * b, 2) if a * b else 4], "The middle term is the average.",
             "$x$.", "in an arithmetic sequence each middle term is the average of its neighbors.",
             [f"$x = \\frac{{{a} + {par(b)}}}{{2}} = {ftex(F(a + b, 2))}$."], "taking half the difference.")


@reg(S, "basics")
def sq_geo_mean(r):
    a, rr = r.randint(1, 8), r.randint(2, 5)
    b = a * rr * rr
    p = f"If ${a}, x, {b}$ is a geometric sequence with $x > 0$, what is $x$?"
    return Q(p, a * rr, [F(a + b, 2), a * rr * rr // 2 if a * rr * rr % 2 == 0 and a * rr * rr // 2 != a * rr else a * rr + 1, b - a, rr, a * b], "The middle term squared is the product of its neighbors.",
             "$x$.", "in a geometric sequence, $x^2 = (\\text{previous})(\\text{next})$.",
             [f"$x^2 = {a} \\cdot {b} = {a * b}$.", f"$x = {a * rr}$."], "taking the average instead.")


@reg(S, "basics")
def sq_pattern(r):
    a = r.randint(3, 8)
    d = r.randint(2, 6)
    n = r.randint(10, 40)
    p = f"Figure 1 is made with ${a}$ toothpicks, figure 2 with ${a + d}$, figure 3 with ${a + 2 * d}$, and so on, adding ${d}$ each time. How many toothpicks are in figure ${n}$?"
    ans = a + (n - 1) * d
    return Q(p, ans, [a + n * d, n * d, ans + d, a * n, ans - 1], "Count the steps from figure 1.",
             "the toothpicks in figure " + str(n) + ".", "it is an arithmetic sequence: start at " + str(a) + " and add " + str(d) + " for each step.",
             [f"From figure 1 to figure {n}: ${n - 1}$ steps.", f"${a} + {n - 1} \\cdot {d} = {ans}$."],
             "adding " + str(d) + " " + str(n) + " times instead of " + str(n - 1) + ".")


@reg(S, "basics")
def sq_even_sum(r):
    n = r.randint(5, 60)
    p = f"What is $2 + 4 + 6 + \\cdots + {2 * n}$?"
    return Q(p, n * (n + 1), [n * n, 2 * n * n, n * (n + 1) // 2, (2 * n) * (2 * n + 1) // 2, n * (n + 2)], "Factor out a $2$.",
             "the sum.", "$2 + 4 + \\cdots + 2n = 2(1 + 2 + \\cdots + n)$.",
             [f"$2(1 + 2 + \\cdots + {n}) = 2 \\cdot \\frac{{{n} \\cdot {n + 1}}}{{2}} = {n * (n + 1)}$."], "using $n^2$, which is the sum of odd numbers.")


@reg(S, "basics")
def sq_count_terms(r):
    a, d = r.randint(-20, 30), r.randint(2, 9)
    n = r.randint(8, 60)
    L = a + (n - 1) * d
    p = f"How many numbers are in the list ${a}, {a + d}, {a + 2 * d}, \\ldots, {L}$?"
    return Q(p, n, [n - 1, n + 1, F(L, d) if F(L, d) != n else n + 2, L - a, F(L - a, d) - 1], "Count steps, then add one.",
             "how many numbers.", "count the steps of " + str(d) + " from the first to the last, then add one for the first number.",
             [f"Steps: $\\frac{{{L} - {par(a)}}}{{{d}}} = {n - 1}$.", f"Numbers: ${n - 1} + 1 = {n}$."],
             "forgetting the first number (fencepost error).")


@reg(S, "basics")
def sq_multiples_sum(r):
    k = r.randint(3, 9)
    N = r.randint(50, 200)
    m = N // k
    ans = k * m * (m + 1) // 2
    p = f"What is the sum of all positive multiples of ${k}$ that are at most ${N}$?"
    return Q(p, ans, [ans + k * (m + 1), m * (m + 1) // 2, ans - k * m, k * m * m, ans + k], "List them: " + f"{k}, {2 * k}, \\ldots, {k * m}" + ".",
             "the sum.", "factor out " + str(k) + ": the multiples are " + str(k) + " times $1, 2, \\ldots, " + str(m) + "$.",
             [f"Largest multiple $\\le {N}$: ${k * m}$, which is ${k} \\cdot {m}$.", f"Sum: ${k}(1 + 2 + \\cdots + {m}) = {k} \\cdot \\frac{{{m} \\cdot {m + 1}}}{{2}} = {ans}$."],
             "including the next multiple, " + str(k * (m + 1)) + ", which is past " + str(N) + ".")


@reg(S, "basics")
def sq_sum_from_avg(r):
    a, d = r.randint(1, 20), r.randint(1, 7)
    n = r.randint(8, 30)
    L = a + (n - 1) * d
    S_ = n * (a + L) // 2 if n * (a + L) % 2 == 0 else None
    if S_ is None:
        return None
    p = f"An arithmetic sequence has ${n}$ terms. Its first term is ${a}$ and its last term is ${L}$. What is the sum of all the terms?"
    return Q(p, S_, [n * L, S_ + a, (n - 1) * (a + L) // 2, n * (a + L), S_ - L], "Average the first and last terms.",
             "the sum.", "sum $=$ (number of terms) $\\times$ (average of first and last).",
             [f"Average: $\\frac{{{a} + {L}}}{{2}} = {ftex(F(a + L, 2))}$.", f"Sum: ${n} \\cdot {ftex(F(a + L, 2))} = {S_}$."],
             "forgetting to divide by $2$.")


@reg(S, "basics")
def sq_theater(r):
    a, d, rows = r.randint(10, 25), r.randint(1, 4), r.randint(8, 20)
    S_ = rows * (2 * a + (rows - 1) * d) // 2
    p = f"A theater has ${a}$ seats in the first row, and each row has ${d}$ more seats than the row in front of it. How many seats are in the first ${rows}$ rows?"
    return Q(p, S_, [rows * a, a + (rows - 1) * d, S_ + rows * d, rows * (a + rows * d), S_ - d], "Find the seats in the last row first.",
             "the total number of seats.", "the rows form an arithmetic sequence; sum $=$ rows $\\times$ average row.",
             [f"Last row: ${a} + {rows - 1} \\cdot {d} = {a + (rows - 1) * d}$.", f"Average row: $\\frac{{{a} + {a + (rows - 1) * d}}}{{2}} = {ftex(F(2 * a + (rows - 1) * d, 2))}$.", f"Total: ${rows} \\cdot {ftex(F(2 * a + (rows - 1) * d, 2))} = {S_}$."],
             "answering the number of seats in the last row.")


@reg(S, "basics")
def sq_term_from_sum(r):
    A, B = r.randint(1, 5), r.randint(-5, 8)
    n = r.randint(5, 30)
    ans = A * (2 * n - 1) + B
    p = f"The sum of the first $n$ terms of a sequence is ${A if A > 1 else ''}n^2{sg(B)}n$. What is the {ordinal(n)} term?"
    return Q(p, ans, [A * n * n + B * n, ans + 2 * A, A * n + B, ans - 1, 2 * A * n + B], "The " + ordinal(n) + " term is the sum through " + str(n) + " minus the sum through " + str(n - 1) + ".",
             "the " + ordinal(n) + " term.", "$a_n = S_n - S_{n-1}$.",
             [f"$S_{{{n}}} = {A * n * n + B * n}$ and $S_{{{n - 1}}} = {A * (n - 1) ** 2 + B * (n - 1)}$.", f"$a_{{{n}}} = {A * n * n + B * n} - {par(A * (n - 1) ** 2 + B * (n - 1))} = {ans}$."],
             "answering $S_n$ itself.")


@reg(S, "basics")
def sq_doubling(r):
    N = r.choice([50, 100, 200, 300, 500])
    h = r.choice([2, 3, 4, 5, 6])
    T = h * r.randint(3, 7)
    ans = N * 2 ** (T // h)
    p = f"A colony of ${N}$ bacteria doubles every ${h}$ hours. How many bacteria are there after ${T}$ hours?"
    return Q(p, ans, [N * 2 * (T // h), N * 2 ** T if T < 12 else ans * 2, ans // 2, N + 2 ** (T // h), N * (T // h + 1)], "Count the doublings.",
             "the population after " + str(T) + " hours.", "geometric growth: multiply by $2$ once per doubling period.",
             [f"Doublings: $\\frac{{{T}}}{{{h}}} = {T // h}$.", f"${N} \\cdot 2^{{{T // h}}} = {ans}$."],
             "multiplying by $2 \\times " + str(T // h) + "$ instead of $2^{" + str(T // h) + "}$.")


@reg(S, "basics")
def sq_alternating(r):
    n = r.randint(10, 101)
    ans = (n + 1) // 2 if n % 2 else -(n // 2)
    p = f"What is $1 - 2 + 3 - 4 + \\cdots {'+' if n % 2 else '-'} {n}$?"
    return Q(p, ans, [-ans, n, F(n, 2) if n % 2 == 0 else n // 2, ans + 1, 0], "Group the terms in pairs.",
             "the alternating sum.", "pair $(1 - 2), (3 - 4), \\ldots$; each pair is $-1$.",
             ([f"${n // 2}$ pairs, each $-1$: total $-{n // 2}$."] if n % 2 == 0 else [f"${n // 2}$ pairs make $-{n // 2}$, then the last term $+{n}$ remains.", f"$-{n // 2} + {n} = {ans}$."]),
             "forgetting the unpaired last term when there is an odd number of terms.")


@reg(S, "challenge")
def sqc_two_blocks(r):
    a, d, n = r.randint(-5, 10), r.choice([x for x in range(-5, 6) if x]), r.randint(4, 10)
    S1 = n * (2 * a + (n - 1) * d) // 2 if n * (2 * a + (n - 1) * d) % 2 == 0 else None
    if S1 is None:
        return None
    S2 = S1 + n * n * d
    p = f"In an arithmetic sequence, the first ${n}$ terms add to ${S1}$ and the next ${n}$ terms add to ${S2}$. What is the common difference?"
    return Q(p, d, [F(S2 - S1, n), -d, d * n, d + 1, F(S2 - S1, 2 * n)], "Compare the two blocks term by term.",
             "the common difference.", "each term in the second block is exactly " + str(n) + " steps after its partner in the first block.",
             [f"Each of the ${n}$ terms in the second block is ${n}d$ bigger than its partner.", f"So the second sum is bigger by ${n} \\cdot {n}d = {n * n}d$: ${n * n}d = {S2 - S1}$.", f"$d = {d}$."],
             "dividing the difference of sums by " + str(n) + " only once.")


@reg(S, "challenge")
def sqc_three_terms(r):
    m, d = r.randint(2, 12), r.randint(1, 8)
    S_, P = 3 * m, (m - d) * m * (m + d)
    p = f"Three numbers in arithmetic sequence add to ${S_}$ and multiply to ${P}$. What is the largest of them?"
    return Q(p, m + d, [m, m - d, d, m + 2 * d, S_ - m], "Write them as $m - d$, $m$, $m + d$.",
             "the largest number.", "centering the terms on the middle one makes the sum easy.",
             [f"Sum: $3m = {S_}$, so $m = {m}$.", f"Product: $({m} - d)({m})({m} + d) = {m}({m * m} - d^2) = {P}$, so $d^2 = {d * d}$.", f"Numbers: ${m - d}, {m}, {m + d}$. Largest: ${m + d}$."],
             "naming them $a, a + d, a + 2d$, which makes the algebra much harder.")


@reg(S, "challenge")
def sqc_geo_three(r):
    a, rr = r.randint(1, 6), r.randint(2, 5)
    b, c = a * rr, a * rr * rr
    p = f"Three positive numbers $a$, ${b}$, $c$ form a geometric sequence, and $a + c = {a + c}$. What is $c$?"
    return Q(p, c, [a, b * 2, a + c - b, c + 1, rr], "$ac = " + str(b) + "^2$.",
             "$c$.", "in a geometric sequence, the middle term squared is the product of the other two.",
             [f"$ac = {b}^2 = {b * b}$ and $a + c = {a + c}$.", f"$a$ and $c$ are the roots of $t^2 - {a + c}t + {b * b} = 0$: $t = {a}$ or ${c}$.", f"$c$ is the larger one if the ratio exceeds $1$; checking ${a}, {b}, {c}$ works, so $c = {c}$."],
             "assuming $c = 2b$ as in an arithmetic sequence.")


@reg(S, "challenge")
def sqc_odd_positions(r):
    a, d, n = r.randint(1, 15), r.randint(2, 7), r.choice([10, 12, 20, 21, 30, 31])
    odd = [a + (i - 1) * d for i in range(1, n + 1, 2)]
    ans = sum(odd)
    p = f"An arithmetic sequence has first term ${a}$ and common difference ${d}$. What is the sum of its 1st, 3rd, 5th, ... terms, up to the {ordinal(n if n % 2 else n - 1)} term?"
    return Q(p, ans, [sum(a + (i - 1) * d for i in range(1, n + 1)), ans + d, ans - a, len(odd) * a, sum(a + (i - 1) * d for i in range(2, n + 1, 2))], "The odd-position terms form their own arithmetic sequence.",
             "the sum of the odd-position terms.", "every other term of an arithmetic sequence is arithmetic with difference $2d$.",
             [f"Terms: ${odd[0]}, {odd[1]}, \\ldots, {odd[-1]}$, with difference ${2 * d}$; there are ${len(odd)}$ of them.", f"Sum: ${len(odd)} \\cdot \\frac{{{odd[0]} + {odd[-1]}}}{{2}} = {ans}$."],
             "counting the wrong number of odd positions.")


@reg(S, "challenge")
def sqc_swap_terms(r):
    m, n = r.sample(range(3, 30), 2)
    # a_m = n, a_n = m  -> d = -1, a_1 = m + n - 1
    ans = m + n - 1
    p = f"In an arithmetic sequence, the {ordinal(m)} term is ${n}$ and the {ordinal(n)} term is ${m}$. What is the first term?"
    return Q(p, ans, [m + n, m + n + 1, abs(m - n), 1, ans - 2], "Find $d$ first.",
             "the first term.", "two terms give the common difference.",
             [f"$d = \\frac{{{m} - {n}}}{{{n} - {m}}} = -1$.", f"First term: $a_{{{m}}} - ({m} - 1)d = {n} + {m - 1} = {ans}$."],
             "getting the sign of $d$ wrong.")


@reg(S, "challenge")
def sqc_two_digit_multiples(r):
    k = r.randint(3, 13)
    xs = [x for x in range(10, 100) if x % k == 0]
    ans = sum(xs)
    p = f"What is the sum of all two-digit positive integers that are divisible by ${k}$?"
    return Q(p, ans, [ans + xs[0], ans - xs[-1], len(xs) * k, sum(x for x in range(1, 100) if x % k == 0), ans + k], "List the first and last ones.",
             "the sum.", "the two-digit multiples form an arithmetic sequence.",
             [f"First: ${xs[0]}$. Last: ${xs[-1]}$. Count: $\\frac{{{xs[-1]} - {xs[0]}}}{{{k}}} + 1 = {len(xs)}$.", f"Sum: ${len(xs)} \\cdot \\frac{{{xs[0]} + {xs[-1]}}}{{2}} = {ans}$."],
             "including one-digit multiples.")


@reg(S, "challenge")
def sqc_geo_first(r):
    a = r.randint(1, 9)
    rr = r.choice([2, 3, -2, F(1, 2)])
    a3, a6 = a * rr ** 2, a * rr ** 5
    if F(a3).denominator != 1 or F(a6).denominator != 1 and F(a6).denominator > 16:
        return None
    p = f"In a geometric sequence, the 3rd term is ${ftex(a3)}$ and the 6th term is ${ftex(a6)}$. What is the first term?"
    return Q(p, a, [a3, F(a3, rr) if F(a3, rr) != a else a + 1, a * rr if a * rr != a else a + 2, -a, F(a6, a3)], "Find the ratio from the two terms.",
             "the first term.", "from term 3 to term 6 you multiply by $r$ three times.",
             [f"$r^3 = \\frac{{{ftex(a6)}}}{{{ftex(a3)}}} = {ftex(F(rr) ** 3)}$, so $r = {ftex(rr)}$.", f"$a_1 = \\frac{{a_3}}{{r^2}} = \\frac{{{ftex(a3)}}}{{{ftex(F(rr) ** 2)}}} = {a}$."],
             "dividing by $r$ only once to get from term 3 to term 1.")


# ================================================================ alg_functions
S = "alg_functions"


@reg(S, "basics")
def fn_domain(r):
    a, b = r.randint(1, 20), r.randint(1, 4)
    top = a // b
    p = f"What is the largest integer in the domain of $f(x) = \\sqrt{{{a} - {b if b > 1 else ''}x}}$?"
    return Q(p, top, [top + 1, a, F(a, b) if F(a, b) != top else top - 1, -top, top - 1], "The expression under the square root must be at least $0$.",
             "the largest allowed integer.", "a square root is only defined for nonnegative inputs.",
             [f"${a} - {b if b > 1 else ''}x \\ge 0$, so $x \\le {ftex(F(a, b))}$.", f"Largest integer: ${top}$."],
             "rounding up.")


@reg(S, "basics")
def fn_two_points(r):
    m, b = r.choice([-4, -3, -2, 2, 3, 4, 5]), r.randint(-10, 10)
    x1, x2 = r.sample(range(-5, 8), 2)
    p = f"A linear function has $f({x1}) = {m * x1 + b}$ and $f({x2}) = {m * x2 + b}$. If $f(x) = mx + b$, what is $m + b$?"
    return Q(p, m + b, [m - b, m * b, b, m, m + b + 1], "$m + b$ is $f(1)$.",
             "$m + b$.", "find the slope from two values, then the intercept.",
             [f"$m = \\frac{{{m * x2 + b} - {par(m * x1 + b)}}}{{{x2} - {par(x1)}}} = {m}$.", f"$b = f({x1}) - {par(m)} \\cdot {par(x1)} = {b}$.", f"$m + b = {m + b}$."],
             "swapping $m$ and $b$.")


@reg(S, "basics")
def fn_piecewise(r):
    c = r.randint(-3, 3)
    a, b = r.randint(2, 5), r.randint(-5, 5)
    x0 = r.choice([c - r.randint(1, 4), c + r.randint(0, 4)])
    val = x0 * x0 + b if x0 < c else a * x0 - 1
    p = f"Let $f(x) = x^2{sg(b)}$ if $x < {c}$, and $f(x) = {a}x - 1$ if $x \\ge {c}$. What is $f({x0})$?"
    other = a * x0 - 1 if x0 < c else x0 * x0 + b
    return Q(p, val, [other, val + 1, -val if val else 2, val - 1, x0 * x0], "Check which rule applies.",
             f"$f({x0})$.", "a piecewise function uses different formulas on different parts of the number line.",
             [f"${x0} {'<' if x0 < c else '\\ge'} {c}$, so use {'the first' if x0 < c else 'the second'} rule.", f"$f({x0}) = {val}$."],
             "using the wrong piece.")


@reg(S, "basics")
def fn_max_vee(r):
    a, b = r.randint(-10, 20), r.randint(-6, 6)
    p = f"What is the largest value of $f(x) = {a} - |x{sg(-b)}|$?"
    return Q(p, a, [b, a - b, a + b, 0, abs(a)], "The absolute value is never negative.",
             "the maximum.", f"$|x{sg(-b)}| \\ge 0$, so subtracting it can only lower the value.",
             [f"The largest $f$ happens when $|x{sg(-b)}| = 0$, at $x = {b}$.", f"$f({b}) = {a}$."],
             "answering the $x$ value instead of the function value.")


@reg(S, "basics")
def fn_shifted_input(r):
    a, b, c = r.randint(1, 3), r.randint(-5, 5), r.randint(-5, 5)
    k = r.randint(-3, 6)
    x = k - 1
    val = a * x * x + b * x + c
    p = f"If $f(x + 1) = {a if a > 1 else ''}x^2{sg(b)}x{sg(c)}$ for all $x$, what is $f({k})$?"
    return Q(p, val, [a * k * k + b * k + c, val + 1, a * (k + 1) ** 2 + b * (k + 1) + c, val - b, c], "Find which $x$ makes $x + 1 = " + str(k) + "$.",
             f"$f({k})$.", "pick the $x$ that turns the input into " + str(k) + ".",
             [f"$x + 1 = {k}$ means $x = {x}$.", f"$f({k}) = {a if a > 1 else ''}({x})^2{sg(b)}({x}){sg(c)} = {val}$."],
             "plugging " + str(k) + " directly into the right side.")


@reg(S, "basics")
def fn_compose_diff(r):
    a, b, c, d = r.randint(2, 5), r.randint(-6, 6), r.randint(2, 5), r.randint(-6, 6)
    x0 = r.randint(-4, 5)
    fg = a * (c * x0 + d) + b
    gf = c * (a * x0 + b) + d
    if fg == gf:
        return None
    p = f"Let $f(x) = {a}x{sg(b)}$ and $g(x) = {c}x{sg(d)}$. What is $f(g({x0})) - g(f({x0}))$?"
    return Q(p, fg - gf, [gf - fg, 0, fg, gf, fg + gf], "Compute each composition separately.",
             "the difference of the two compositions.", "work from the inside out: $f(g(x))$ means apply $g$ first.",
             [f"$g({x0}) = {c * x0 + d}$, so $f(g({x0})) = {a} \\cdot {par(c * x0 + d)}{sg(b)} = {fg}$.", f"$f({x0}) = {a * x0 + b}$, so $g(f({x0})) = {c} \\cdot {par(a * x0 + b)}{sg(d)} = {gf}$.", f"Difference: ${fg} - {par(gf)} = {fg - gf}$."],
             "assuming the order of composition doesn't matter.")


@reg(S, "basics")
def fn_mirror(r):
    h = r.randint(-5, 6)
    c = r.randint(-9, 9)
    p0 = r.randint(-8, 10)
    if p0 == h:
        return None
    p = f"Let $f(x) = x^2{sg(-2 * h)}x{sg(c)}$. Besides $x = {p0}$, what other value of $x$ gives $f(x) = f({p0})$?"
    return Q(p, 2 * h - p0, [-p0, h, p0 - 2 * h, 2 * h + p0, h - p0], "The parabola is symmetric about its axis.",
             "the other input with the same output.", "points with equal heights on a parabola are mirror images across the axis $x = -\\frac{b}{2a}$.",
             [f"Axis: $x = {h}$.", f"${p0}$ is ${abs(p0 - h)}$ {'right' if p0 > h else 'left'} of the axis, so its mirror is ${abs(p0 - h)}$ {'left' if p0 > h else 'right'}: $x = {2 * h - p0}$."],
             f"using ${-p0}$, which is a mirror across $x = 0$.")


@reg(S, "basics")
def fn_odd(r):
    k = r.randint(1, 9)
    v = r.randint(-12, 12)
    p = f"A function $f$ is odd, meaning $f(-x) = -f(x)$ for all $x$. If $f({k}) = {v}$, what is $f(-{k}) + f(0)$?"
    return Q(p, -v, [v, 0, -v + 1, 2 * v if v else 3, -2 * v if v else 4], "What must $f(0)$ be for an odd function?",
             "$f(-" + str(k) + ") + f(0)$.", "odd means $f(-x) = -f(x)$; plugging in $x = 0$ gives $f(0) = -f(0)$, so $f(0) = 0$.",
             [f"$f(-{k}) = -f({k}) = {-v}$.", "$f(0) = 0$.", f"Sum: ${-v}$."],
             "thinking $f(0)$ can't be found.")


@reg(S, "basics")
def fn_inverse_rational(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    y0 = r.randint(2, 7)
    x = F(a + b * y0, y0 - 1)
    p = f"If $f(x) = \\dfrac{{x + {a}}}{{x - {b}}}$, what is $f^{{-1}}({y0})$?"
    return Q(p, x, [F(y0 + a, y0 - b) if y0 != b else 2, F(1, y0), x + 1, -x, F(y0 - 1, a + b * y0)], "Solve $f(x) = " + str(y0) + "$.",
             "the input that gives output " + str(y0) + ".", "$f^{-1}(y)$ is the $x$ with $f(x) = y$.",
             [f"$\\frac{{x + {a}}}{{x - {b}}} = {y0}$, so $x + {a} = {y0}x - {y0 * b}$.", f"${y0 - 1}x = {a + y0 * b}$, so $x = {ftex(x)}$."],
             "computing $f(" + str(y0) + ")$ instead.")


@reg(S, "basics")
def fn_iterate(r):
    a, b = r.randint(-3, 3), r.randint(-6, 6)
    k = r.randint(-3, 4)
    f = lambda x: x * x + a * x + b
    ans = f(f(k))
    if abs(ans) > 3000:
        return None
    p = f"If $f(x) = x^2{sg(a)}x{sg(b)}$, what is $f(f({k}))$?"
    return Q(p, ans, [f(k) ** 2, f(k), 2 * f(k), ans + 1, f(k * k)], "Find $f(" + str(k) + ")$ first.",
             f"$f(f({k}))$.", "evaluate from the inside out.",
             [f"$f({k}) = {f(k)}$.", f"$f({f(k)}) = {par(f(k))}^2{sg(a)} \\cdot {par(f(k))}{sg(b)} = {ans}$."],
             "squaring $f(" + str(k) + ")$ instead of applying $f$ again.")


@reg(S, "basics")
def fn_shift_vertex(r):
    a, b = r.randint(-6, 6), r.randint(-6, 6)
    p = f"The graph of $y = x^2$ is shifted to get $y = (x{sg(-a)})^2{sg(b)}$. What is the sum of the coordinates of the new vertex?"
    return Q(p, a + b, [-a + b, a - b, -a - b, a * b, a + b + 1], "$y = (x - h)^2 + k$ has vertex $(h, k)$.",
             "the sum of the vertex coordinates.", "replacing $x$ with $x - h$ shifts right by $h$; adding $k$ shifts up by $k$.",
             [f"Vertex: $({a}, {b})$.", f"Sum: ${a + b}$."],
             "moving the wrong way: $x - " + str(a) + "$ shifts right, not left." if a > 0 else "getting the sign of the horizontal shift backwards.")


@reg(S, "basics")
def fn_rate_change(r):
    a, b = r.randint(1, 3), r.randint(-6, 6)
    x1, x2 = r.sample(range(-4, 8), 2)
    f = lambda x: a * x * x + b * x
    ans = F(f(x2) - f(x1), x2 - x1)
    p = f"What is the average rate of change of $f(x) = {a if a > 1 else ''}x^2{sg(b)}x$ from $x = {min(x1, x2)}$ to $x = {max(x1, x2)}$?"
    return Q(p, ans, [f(x2) - f(x1), F(f(x2) + f(x1), 2), ans + 1, -ans if ans else 2, F(f(x2), x2) if x2 else 7], "Change in $f$ over change in $x$.",
             "the average rate of change.", "it is the slope of the line through the two points on the graph.",
             [f"$f({x1}) = {f(x1)}$ and $f({x2}) = {f(x2)}$.", f"$\\frac{{{f(max(x1, x2))} - {par(f(min(x1, x2)))}}}{{{max(x1, x2)} - {par(min(x1, x2))}}} = {ftex(ans)}$."],
             "forgetting to divide by the change in $x$.")


@reg(S, "basics")
def fn_floor(r):
    x = r.randint(10, 99)
    a, b = r.sample([2, 3, 4, 5, 6, 7], 2)
    ans = x // a + x // b
    p = f"Let $f(x) = \\left\\lfloor \\dfrac{{x}}{{{a}}} \\right\\rfloor + \\left\\lfloor \\dfrac{{x}}{{{b}}} \\right\\rfloor$, where $\\lfloor t \\rfloor$ is the greatest integer at most $t$. What is $f({x})$?"
    return Q(p, ans, [F(x, a) + F(x, b) if F(x, a) + F(x, b) != ans else ans + 1, ans + 1, x // (a + b), x // a, ans - 1], "Divide and round down each part.",
             f"$f({x})$.", "the floor rounds down to the nearest integer.",
             [f"$\\frac{{{x}}}{{{a}}} = {ftex(F(x, a))}$, which rounds down to ${x // a}$.", f"$\\frac{{{x}}}{{{b}}} = {ftex(F(x, b))}$, which rounds down to ${x // b}$.", f"Sum: ${ans}$."],
             "rounding to the nearest integer instead of down.")


@reg(S, "basics")
def fn_lines_meet(r):
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    x = F(r.randint(-12, 12), r.choice([1, 1, 2]))
    b1 = r.randint(-8, 8)
    b2 = m1 * x + b1 - m2 * x
    if F(b2).denominator != 1:
        return None
    p = f"For what $x$ does $f(x) = {m1}x{sg(b1)}$ equal $g(x) = {m2}x{sg(int(b2))}$?"
    return Q(p, x, [-x if x else 1, F(b1 - b2, m1 - m2) if F(b1 - b2, m1 - m2) != x else x + 1, x + 1, m1 * x + b1 if m1 * x + b1 != x else x - 1, F(b2 + b1, m1 + m2) if m1 + m2 and F(b2 + b1, m1 + m2) != x else x + 2], "Set them equal.",
             "the input where the two outputs match.", "solve $f(x) = g(x)$ as one linear equation.",
             [f"${m1}x{sg(b1)} = {m2}x{sg(int(b2))}$.", f"${m1 - m2}x = {int(b2) - b1}$, so $x = {ftex(x)}$."],
             "giving the common output value instead of $x$.")


@reg(S, "basics")
def fn_scaled_input(r):
    m, c = r.randint(2, 8), r.randint(-9, 9)
    k = r.randint(-5, 10)
    # f(2x) = m x + c -> f(t) = m t / 2 + c
    ans = F(m * k, 2) + c
    p = f"If $f(2x) = {m}x{sg(c)}$ for all $x$, what is $f({k})$?"
    return Q(p, ans, [m * k + c, F(m * k + c, 2), m * 2 * k + c, ans + 1, F(m * k, 2)], "Which $x$ makes $2x = " + str(k) + "$?",
             f"$f({k})$.", "choose the input so that $2x$ equals " + str(k) + ".",
             [f"$2x = {k}$ means $x = {ftex(F(k, 2))}$.", f"$f({k}) = {m} \\cdot {ftex(F(k, 2))}{sg(c)} = {ftex(ans)}$."],
             "plugging " + str(k) + " straight into the right side.")


@reg(S, "basics")
def fn_odd_part(r):
    a, b = r.randint(1, 6), r.randint(1, 6)
    c = r.randint(1, 12)
    k = r.randint(1, 5)
    m = r.randint(-30, 30)
    ans = 2 * c - m
    p = f"Let $f(x) = ax^3 + bx + {c}$. If $f(-{k}) = {m}$, what is $f({k})$?"
    return Q(p, ans, [-m, m, ans + c, m - 2 * c, c], "The $ax^3 + bx$ part changes sign when $x$ does.",
             f"$f({k})$.", "$g(x) = ax^3 + bx$ is odd, so $g(-k) = -g(k)$.",
             [f"$f(-{k}) = g(-{k}) + {c} = {m}$, so $g(-{k}) = {m - c}$.", f"$g({k}) = {c - m}$.", f"$f({k}) = {c - m} + {c} = {ans}$."],
             f"answering ${-m}$ and forgetting the constant term.")


@reg(S, "challenge")
def fnc_recip_eq(r):
    c = r.choice([3, 6, 9, 12])
    k = r.choice([2, 3, 4, F(1, 2), F(1, 3)])
    val = (F(2 * c) / k - c * k) / 3
    p = f"A function satisfies $f(x) + 2f\\!\\left(\\dfrac{{1}}{{x}}\\right) = {c}x$ for every nonzero $x$. What is $f({ftex(k)})$?"
    return Q(p, val, [c * k, F(c, k), -val if val else 1, val + c, F(c * k, 3)], "Replace $x$ with $\\frac{1}{x}$ to get a second equation.",
             f"$f({ftex(k)})$.", "swapping $x$ and $\\frac{1}{x}$ gives a second equation; solve the two together.",
             [f"With $x = {ftex(k)}$: $f({ftex(k)}) + 2f({ftex(1 / F(k))}) = {ftex(c * F(k))}$.", f"With $x = {ftex(1 / F(k))}$: $f({ftex(1 / F(k))}) + 2f({ftex(k)}) = {ftex(c / F(k))}$.",
              f"Double the second and subtract the first: $3f({ftex(k)}) = {ftex(2 * c / F(k))} - {ftex(c * F(k))}$.", f"$f({ftex(k)}) = {ftex(val)}$."],
             "assuming $f(x) = " + str(c) + "x$, which ignores the second term.")


@reg(S, "challenge")
def fnc_linear_square(r):
    a = r.randint(2, 6)
    b = r.randint(-6, 8)
    p = f"Let $f(x) = ax + b$ with $a > 0$. If $f(f(x)) = {a * a}x{sg(a * b + b)}$ for all $x$, what is $f(1)$?"
    return Q(p, a + b, [a * a + a * b + b, a, b, a - b, a + b + 1], "Expand $f(f(x))$.",
             "$f(1) = a + b$.", "compose and match coefficients.",
             [f"$f(f(x)) = a(ax + b) + b = a^2x + ab + b$.", f"$a^2 = {a * a}$ with $a > 0$ gives $a = {a}$.", f"$ab + b = {a + 1}b = {a * b + b}$, so $b = {b}$.", f"$f(1) = {a + b}$."],
             "taking $a = -" + str(a) + "$, which the condition rules out.")


@reg(S, "challenge")
def fnc_abs_iterate(r):
    a, b = r.randint(-4, 4), r.randint(1, 5)
    # f(x) = |x - a| - b; f(f(x)) = 0 -> f(x) = a +- b; then |x - a| = y + b must be >= 0
    ys = {a + b, a - b}
    sols = set()
    for y in ys:
        t = y + b
        if t > 0:
            sols |= {a + t, a - t}
        elif t == 0:
            sols.add(a)
    p = f"Let $f(x) = |x{sg(-a)}| - {b}$. How many real solutions does $f(f(x)) = 0$ have?"
    lines = []
    for y in sorted(ys):
        t = y + b
        lines.append(f"$f(x) = {y}$ means $|x{sg(-a)}| = {t}$: " + ("two solutions" if t > 0 else "one solution" if t == 0 else "none"))
    return Q(p, len(sols), [0, 1, 2, 3, 4], "Solve $f(y) = 0$ first, then $f(x) = y$.",
             "the number of solutions.", "peel the composition: first find which outputs of $f$ work, then which $x$ give them.",
             [f"$f(y) = 0$ means $|y{sg(-a)}| = {b}$, so $y = {a + b}$ or $y = {a - b}$.", "; ".join(lines) + ".", f"Total: ${len(sols)}$."],
             "counting four solutions without checking for negative absolute values.")


@reg(S, "challenge")
def fnc_pair_sum(r):
    k = r.randint(3, 12)
    ans = F(2 * k - 1, 2)
    p = f"Let $f(x) = \\dfrac{{x}}{{x + 1}}$. What is $f\\!\\left(\\tfrac{{1}}{{{k}}}\\right) + \\cdots + f\\!\\left(\\tfrac{{1}}{{2}}\\right) + f(1) + f(2) + \\cdots + f({k})$?"
    return Q(p, ans, [k, F(k, 2), ans + 1, 2 * k - 1, k - 1], "Compute $f(x) + f\\left(\\frac{1}{x}\\right)$.",
             "the sum.", "$f(x) + f\\left(\\frac{1}{x}\\right) = \\frac{x}{x + 1} + \\frac{1}{1 + x} = 1$, so the terms pair up.",
             [f"Pair $f(n)$ with $f\\left(\\frac{{1}}{{n}}\\right)$ for $n = 2, \\ldots, {k}$: ${k - 1}$ pairs, each worth $1$.", "$f(1) = \\frac{1}{2}$ is left alone.", f"Total: ${k - 1} + \\frac{{1}}{{2}} = {ftex(ans)}$."],
             "pairing $f(1)$ with itself.")


@reg(S, "challenge")
def fnc_period4(r):
    a = r.choice([F(2), F(3), F(1, 2), F(1, 3), F(-2), F(5)])
    n = r.randint(10, 100)
    vals = [a]
    for _ in range(4):
        x = vals[-1]
        vals.append((1 + x) / (1 - x))
    assert vals[4] == a
    ans = vals[(n - 1) % 4]
    p = f"A sequence has $f(1) = {ftex(a)}$ and $f(n + 1) = \\dfrac{{1 + f(n)}}{{1 - f(n)}}$. What is $f({n})$?"
    return Q(p, ans, [vals[n % 4], vals[(n + 1) % 4], vals[(n + 2) % 4], -ans if ans else 1, ans + 1], "Compute a few terms and look for a repeat.",
             f"$f({n})$.", "the values cycle, so only $n$ modulo the cycle length matters.",
             ["Terms: " + ", ".join(f"$f({i + 1}) = {ftex(v)}$" for i, v in enumerate(vals)) + ".", f"$f(5) = f(1)$, so the period is $4$.", f"${n} = 4 \\cdot {(n - 1) // 4} + {(n - 1) % 4 + 1}$, so $f({n}) = f({(n - 1) % 4 + 1}) = {ftex(ans)}$."],
             "an off by one error in matching the remainder to a position.")


@reg(S, "challenge")
def fnc_inverse_compose(r):
    a, b = r.randint(-6, 6), r.randint(-6, 6)
    k = r.randint(-5, 8)
    ginv = 3 * k + b
    ans = F(ginv - a, 2)
    p = f"Let $f(x) = 2x{sg(a)}$ and $g(x) = \\dfrac{{x{sg(-b)}}}{{3}}$. What is $f^{{-1}}(g^{{-1}}({k}))$?"
    return Q(p, ans, [2 * F(k - b, 3) + a, ginv, F(ginv + a, 2), ans + 1, F(k - a, 2)], "Undo $g$, then undo $f$.",
             "$f^{-1}(g^{-1}(" + str(k) + "))$.", "inverse functions undo the original: solve $g(y) = " + str(k) + "$, then $f(x) = y$.",
             [f"$g^{{-1}}({k})$: $\\frac{{y{sg(-b)}}}{{3}} = {k}$ gives $y = {ginv}$.", f"$f^{{-1}}({ginv})$: $2x{sg(a)} = {ginv}$ gives $x = {ftex(ans)}$."],
             "applying $f$ and $g$ forwards instead of undoing them.")


@reg(S, "challenge")
def fnc_floor_sqrt(r):
    n = r.randint(10, 60)
    ans = sum(math.isqrt(k) for k in range(1, n + 1))
    m = math.isqrt(n)
    lines = [f"$\\lfloor\\sqrt{{k}}\\rfloor = {j}$ for $k = {j * j}$ to ${min((j + 1) ** 2 - 1, n)}$: ${min((j + 1) ** 2 - 1, n) - j * j + 1}$ values" for j in range(1, m + 1)]
    p = f"What is $\\lfloor\\sqrt{{1}}\\rfloor + \\lfloor\\sqrt{{2}}\\rfloor + \\cdots + \\lfloor\\sqrt{{{n}}}\\rfloor$?"
    return Q(p, ans, [ans + m, ans - m, n * m // 2, sum(round(math.sqrt(k)) for k in range(1, n + 1)) if sum(round(math.sqrt(k)) for k in range(1, n + 1)) != ans else ans + 1, ans + 1], "Group the terms with the same floor value.",
             "the sum of the floors.", "$\\lfloor\\sqrt{k}\\rfloor = j$ for all $k$ from $j^2$ up to $(j + 1)^2 - 1$, which is $2j + 1$ values.",
             ["; ".join(lines) + ".", "Add: $" + " + ".join(f"{j} \\cdot {min((j + 1) ** 2 - 1, n) - j * j + 1}" for j in range(1, m + 1)) + f" = {ans}$."],
             "forgetting that the last group may be cut short at " + str(n) + ".")
