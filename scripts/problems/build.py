"""Builds every unit file and problem bank in /content.

Run from the project root:  python3 scripts/problems/build.py
Each skill gets 20 basics and 10 challenge problems. Re-running with the same
seeds produces the same problems, so ids stay stable for students' history.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CONTENT = os.path.join(ROOT, "content")

import algebra  # noqa: E402
import amc12  # noqa: E402
import counting  # noqa: E402
import geometry  # noqa: E402
import numbertheory  # noqa: E402

UNITS = [
    ("algebra", "Algebra", "Equations, word problems, exponents, quadratics, statistics, sequences and functions.", "both", algebra, [
        ("alg_linear", "Linear equations and systems", "Solve one and two variable linear equations and systems."),
        ("alg_rates", "Rates, work and motion", "Distance, speed, time and combined work problems."),
        ("alg_ratios", "Ratios and percents", "Ratios, proportions, mixtures and percent change."),
        ("alg_exponents", "Exponents and radicals", "Exponent rules, simplifying radicals and rationalizing."),
        ("alg_factoring", "Factoring and special products", "Difference of squares, perfect squares and clever factoring."),
        ("alg_quadratics", "Quadratics", "Roots, the discriminant, vertex form and Vieta for quadratics."),
        ("alg_absolute", "Absolute value and inequalities", "Absolute value equations and solving inequalities."),
        ("alg_stats", "Mean, median and mode", "Averages, medians, modes and how changes affect them."),
        ("alg_sequences", "Arithmetic and geometric sequences", "Find terms and sums of arithmetic and geometric sequences."),
        ("alg_functions", "Functions", "Evaluate, compose and invert functions; solve functional equations."),
    ]),
    ("geometry", "Geometry", "Angles, triangles, circles, area, coordinates and solids.", "both", geometry, [
        ("geo_angles", "Angles and polygons", "Angle chasing, parallel lines and polygon angle sums."),
        ("geo_right", "Right triangles", "The Pythagorean theorem, triples and special right triangles."),
        ("geo_similar", "Similar triangles", "Similarity ratios and how they scale lengths and areas."),
        ("geo_area", "Area", "Areas of triangles, quadrilaterals and composite shapes."),
        ("geo_circles", "Circles", "Arcs, chords, tangents, inscribed angles and sectors."),
        ("geo_coordinate", "Coordinate geometry", "Distance, midpoint, slope, lines and areas on the grid."),
        ("geo_solids", "3D solids", "Volume and surface area of prisms, cylinders, cones and spheres."),
    ]),
    ("number_theory", "Number Theory", "Divisors, primes, remainders, bases and factorials.", "both", numbertheory, [
        ("nt_divisors", "Primes and divisors", "Prime factorization and counting and summing divisors."),
        ("nt_gcd", "GCD and LCM", "Greatest common divisors, least common multiples and their uses."),
        ("nt_divisibility", "Divisibility rules", "Test divisibility and find missing digits."),
        ("nt_modular", "Remainders and modular arithmetic", "Work with remainders and congruences."),
        ("nt_powers", "Units digits and cycles of powers", "Find last digits and remainders of large powers."),
        ("nt_bases", "Number bases", "Convert between bases and do arithmetic in other bases."),
        ("nt_factorials", "Factorials", "Trailing zeros, prime powers in factorials and factorial divisibility."),
    ]),
    ("counting_probability", "Counting and Probability", "Systematic counting, arrangements, choices, probability and expected value.", "both", counting, [
        ("cp_counting", "Counting principles", "Multiplication principle and counting lists."),
        ("cp_permutations", "Permutations", "Arrangements, including letters with repeats and restrictions."),
        ("cp_combinations", "Combinations", "Choosing groups, committees and paths on a grid."),
        ("cp_casework", "Casework and complements", "Split into cases or count what you don't want."),
        ("cp_inclusion", "Inclusion and exclusion", "Count overlapping sets without double counting."),
        ("cp_probability", "Probability", "Dice, coins, cards and drawing without replacement."),
        ("cp_expected", "Expected value", "Average outcomes of games and random processes."),
        ("cp_geometric", "Geometric probability", "Probability as a ratio of lengths or areas."),
    ]),
    ("trigonometry", "Trigonometry", "The unit circle, identities, the Laws of Sines and Cosines, and trig equations.", "amc12", amc12, [
        ("trig_values", "Unit circle values", "Exact sine, cosine and tangent values and radian measure."),
        ("trig_identities", "Trig identities", "Pythagorean, double angle and sum identities."),
        ("trig_laws", "Law of Sines and Cosines", "Solve triangles and find areas and circumradii."),
        ("trig_equations", "Trig equations and graphs", "Count and find solutions; periods of trig graphs."),
    ]),
    ("logarithms", "Logarithms", "Log rules, exponential and log equations, and change of base.", "amc12", amc12, [
        ("log_rules", "Logarithm rules", "Evaluate and combine logarithms."),
        ("log_equations", "Exponential and log equations", "Solve equations with exponents and logs."),
        ("log_change_base", "Change of base and digits", "Change of base, counting digits and bounding logs."),
    ]),
    ("complex_numbers", "Complex Numbers", "Complex arithmetic, polar form, De Moivre's theorem and roots of unity.", "amc12", amc12, [
        ("cx_arithmetic", "Complex arithmetic", "Add, multiply and divide complex numbers; modulus and conjugates."),
        ("cx_polar", "Polar form and De Moivre", "Write complex numbers with angles and raise them to powers."),
        ("cx_roots_unity", "Roots of unity", "Solutions of z^n = 1 and how they add and multiply."),
    ]),
    ("polynomials", "Polynomials", "Vieta's formulas, the Remainder Theorem and finding roots.", "amc12", amc12, [
        ("poly_vieta", "Vieta's formulas", "Relate roots to coefficients for higher degree polynomials."),
        ("poly_remainder", "Remainder and Factor Theorems", "Find remainders and missing coefficients."),
        ("poly_roots", "Finding roots", "Rational roots, double roots and conjugate roots."),
    ]),
    ("conics", "Conics and Analytic Geometry", "Circles, parabolas, ellipses, hyperbolas and 3D coordinates.", "amc12", amc12, [
        ("con_parabolas", "Circles and parabolas", "Complete the square; vertices, foci, tangents and chords."),
        ("con_ellipses", "Ellipses and hyperbolas", "Axes, foci, asymptotes and eccentricity."),
        ("con_analytic", "Analytic geometry in 2D and 3D", "Distances, reflections, intersections and 3D shapes."),
    ]),
    ("sequences_series", "Sequences and Series", "Recursion, telescoping sums and infinite geometric series.", "amc12", amc12, [
        ("ser_recursion", "Recursive sequences", "Compute terms, find cycles and closed forms."),
        ("ser_telescoping", "Telescoping sums and products", "Sums and products that collapse."),
        ("ser_geometric", "Infinite geometric series", "Sums of infinite series and repeating decimals."),
    ]),
]


def main():
    units_dir = os.path.join(CONTENT, "units")
    probs_dir = os.path.join(CONTENT, "problems")
    # Unit files are all generated here; problem files only for the units below,
    # so hand written problem files in content/problems are left alone.
    for f in os.listdir(units_dir):
        if f.endswith(".json"):
            os.remove(os.path.join(units_dir, f))
    for uid, *_ in UNITS:
        p = os.path.join(probs_dir, f"{uid}.json")
        if os.path.exists(p):
            os.remove(p)
    for f in ("placeholder_skill_one.mdx", "placeholder_skill_two.mdx"):
        p = os.path.join(CONTENT, "lessons", f)
        if os.path.exists(p):
            os.remove(p)

    total = 0
    for order, (uid, title, desc, track, mod, skills) in enumerate(UNITS, 1):
        by_id = {b.skill_id: b for b in mod.banks}
        unit = {"id": uid, "title": title, "description": desc, "track": track, "order": order,
                "skills": [{"id": s, "title": t, "description": d} for s, t, d in skills]}
        with open(os.path.join(units_dir, f"{order:02d}-{uid}.json"), "w") as f:
            json.dump(unit, f, indent=2, ensure_ascii=False)
            f.write("\n")
        problems = []
        for s, _, _ in skills:
            b = by_id[s]
            nb, nc = len(b.items["basics"]), len(b.items["challenge"])
            assert nb >= 20 and nc >= 10, (s, nb, nc)
            problems.extend(b.all())
        with open(os.path.join(probs_dir, f"{uid}.json"), "w") as f:
            json.dump(problems, f, indent=1, ensure_ascii=False)
            f.write("\n")
        total += len(problems)
        print(f"{uid}: {len(skills)} skills, {len(problems)} problems")
    print(f"total {total} problems")


if __name__ == "__main__":
    main()
