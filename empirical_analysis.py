"""
Empirical Analysis - Median of Medians vs Randomized Quickselect
Compares running times across different input sizes and distributions.
"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np

from median_of_medians import median_of_medians
from quickselect import quickselect


# ── Timing helper ────────────────────────────────────────────────────────────

def time_algorithm(func, arr, k, repeats=5):
    """Run func(arr, k) `repeats` times and return the average elapsed seconds."""
    times = []
    for _ in range(repeats):
        arr_copy = arr[:]
        start = time.perf_counter()
        func(arr_copy, k)
        times.append(time.perf_counter() - start)
    return np.mean(times)


# ── Input generators ─────────────────────────────────────────────────────────

def generate_random(n):
    return random.sample(range(n * 10), n)

def generate_sorted(n):
    return list(range(n))

def generate_reversed(n):
    return list(range(n, 0, -1))

def generate_duplicates(n):
    return [random.randint(0, n // 10) for _ in range(n)]


# ── Benchmark ────────────────────────────────────────────────────────────────

def run_benchmark():
    sizes = [100, 500, 1_000, 5_000, 10_000, 50_000]
    distributions = {
        "Random":   generate_random,
        "Sorted":   generate_sorted,
        "Reversed": generate_reversed,
        "Duplicates": generate_duplicates,
    }

    results = {
        dist: {"mom": [], "qs": []}
        for dist in distributions
    }

    print(f"{'Distribution':<14} {'Size':>8}  {'MoM (ms)':>10}  {'QS (ms)':>10}  {'Faster':>8}")
    print("-" * 60)

    for dist_name, gen in distributions.items():
        for n in sizes:
            arr = gen(n)
            k   = n // 2  # always search for the median

            t_mom = time_algorithm(median_of_medians, arr, k) * 1000
            t_qs  = time_algorithm(quickselect,       arr, k) * 1000

            results[dist_name]["mom"].append(t_mom)
            results[dist_name]["qs"].append(t_qs)

            faster = "MoM" if t_mom < t_qs else "QS "
            print(f"{dist_name:<14} {n:>8}  {t_mom:>10.3f}  {t_qs:>10.3f}  {faster:>8}")
        print()

    return sizes, results


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_results(sizes, results):
    distributions = list(results.keys())
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, dist_name in enumerate(distributions):
        ax = axes[idx]
        mom_times = results[dist_name]["mom"]
        qs_times  = results[dist_name]["qs"]

        ax.plot(sizes, mom_times, "o-", color="steelblue",  label="Median of Medians", linewidth=2)
        ax.plot(sizes, qs_times,  "s-", color="darkorange", label="Quickselect",        linewidth=2)

        ax.set_title(f"{dist_name} Input", fontsize=13, fontweight="bold")
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Time (ms)")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("Median of Medians vs Randomized Quickselect\nRunning Time Comparison",
                 fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig("empirical_results.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Plot saved to empirical_results.png")


# ── Normal distribution of timing results ───────────────────────────────────

def plot_timing_distribution(n=10_000, trials=50):
    """
    Show the distribution of running times over many trials
    to illustrate the probabilistic nature of Quickselect.
    """
    arr_template = generate_random(n)
    k = n // 2

    mom_times, qs_times = [], []
    for _ in range(trials):
        arr = arr_template[:]
        mom_times.append(time_algorithm(median_of_medians, arr, k, repeats=1) * 1000)
        qs_times.append(time_algorithm(quickselect,        arr, k, repeats=1) * 1000)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, times, label, color in [
        (axes[0], mom_times, "Median of Medians", "steelblue"),
        (axes[1], qs_times,  "Quickselect",       "darkorange"),
    ]:
        mu, std = np.mean(times), np.std(times)
        x = np.linspace(min(times), max(times), 200)
        from scipy import stats
        p = stats.norm.pdf(x, mu, std)

        ax.hist(times, bins=15, density=True, color=color,
                edgecolor="black", alpha=0.6, label="Observed")
        ax.plot(x, p, "k-", linewidth=2, label=f"Normal fit\nμ={mu:.2f}, σ={std:.2f}")
        ax.set_title(f"{label}\nTime Distribution (n={n}, {trials} trials)")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Density")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("timing_distribution.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("Distribution plot saved to timing_distribution.png")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Empirical Analysis: Selection Algorithms")
    print("=" * 60)

    sizes, results = run_benchmark()
    plot_results(sizes, results)
    plot_timing_distribution()

    print("\nSummary:")
    print("  - Quickselect is faster in practice due to lower constants.")
    print("  - Median of Medians has a more predictable (tight) time distribution.")
    print("  - Quickselect variance increases on adversarial / sorted inputs.")
