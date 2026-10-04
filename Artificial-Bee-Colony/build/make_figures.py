"""Draw every figure used by the notebook, the slides and the README.

All figures use the honey palette of the bee template so that the deck
looks like one piece of work.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from dataclasses import replace

from abc_core import (ackley, run_abc, create_sources, selection_probabilities,
                      to_fitness, neighbour, SETTINGS, ABCSettings)

FIG = Path(__file__).resolve().parents[1] / "figures"
FIG.mkdir(exist_ok=True)

# ---------------------------------------------------------------- palette
BG       = "#F5F5F5"
BROWN    = "#6F251B"
AMBER    = "#FFC62A"
ORANGE   = "#FF9500"
DEEP     = "#E37E03"
HIVE     = "#CB6C29"
DARKWOOD = "#803B1B"
GREY     = "#9A8F8C"

# A honey colour map: deep brown in the valleys, bright honey on the peaks.
HONEY = LinearSegmentedColormap.from_list(
    "honey", ["#3B1410", "#6F251B", "#B04B26", "#E37E03", "#FFC62A", "#FFF0B8"])

plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": BG,
    "axes.facecolor": "white",
    "savefig.facecolor": BG,
    "font.size": 10.5,
    "font.family": "DejaVu Sans",
    "text.color": BROWN,
    "axes.labelcolor": BROWN,
    "axes.edgecolor": "#D8CFCB",
    "xtick.color": BROWN,
    "ytick.color": BROWN,
    "axes.grid": True,
    "grid.color": "#E6DEDA",
    "grid.alpha": 0.9,
    "axes.axisbelow": True,
    "legend.frameon": True,
    "legend.facecolor": "white",
    "legend.edgecolor": "#E0D7D3",
})


def save(fig, name):
    path = FIG / name
    fig.savefig(path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("wrote", path.name)


# ---------------------------------------------------------------- shared data
grid = np.linspace(SETTINGS.lower, SETTINGS.upper, 400)
X1, X2 = np.meshgrid(grid, grid)
Z = ackley(np.stack([X1, X2], axis=-1))

SNAPSHOTS = (0, 3, 8, 20, 50, 100)
result = run_abc(SETTINGS, verbose=False, snapshot_at=SNAPSHOTS)
history = result["history"]
best_x1, best_x2 = result["best_solution"]
best_f = result["best_value"]

rng0 = np.random.default_rng(SETTINGS.seed)
initial_sources = create_sources(rng0, SETTINGS)
initial_values = ackley(initial_sources)


# =====================================================================
# 01  the landscape
# =====================================================================
def fig_landscape():
    fig = plt.figure(figsize=(12.5, 5.0))

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.set_facecolor(BG)
    ax.plot_surface(X1[::3, ::3], X2[::3, ::3], Z[::3, ::3],
                    cmap=HONEY, linewidth=0, antialiased=True, alpha=0.97)
    ax.scatter([0], [0], [0], color=BROWN, marker="*", s=240,
               edgecolor="white", linewidth=0.8, depthshade=False)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); ax.set_zlabel("$f$")
    ax.set_title("One deep funnel, many ripples", color=BROWN, fontsize=12)
    ax.view_init(elev=40, azim=-58)

    ax = fig.add_subplot(1, 2, 2)
    filled = ax.contourf(X1, X2, Z, levels=45, cmap=HONEY)
    bar = fig.colorbar(filled, ax=ax)
    bar.set_label("Ackley value", color=BROWN)
    ax.scatter(0, 0, marker="*", s=300, color="white", edgecolor=BROWN,
               linewidth=1.6, zorder=5, label="global minimum $(0,0)$")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("Every dark ring is a trap (a local minimum)", color=BROWN, fontsize=12)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_aspect("equal")
    ax.grid(False)

    fig.tight_layout()
    save(fig, "01_ackley_landscape.png")


# =====================================================================
# 02  a one-dimensional slice
# =====================================================================
def fig_slice():
    line = np.linspace(-5, 5, 2000)
    values = ackley(np.stack([line, np.zeros_like(line)], axis=-1))

    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.plot(line, values, color=DEEP, linewidth=2.2)
    ax.fill_between(line, values, color=AMBER, alpha=0.22)
    ax.scatter([0], [0], color=BROWN, marker="*", s=230, zorder=5,
               edgecolor="white", linewidth=0.9,
               label="global minimum  $f(0,0)=0$")
    for k in (1, 2, 3, 4):
        for s in (-1, 1):
            ax.scatter([s * k], [ackley([s * k, 0])], s=28, color=HIVE, zorder=4)
    ax.annotate("local minima", xy=(2, ackley([2, 0])), xytext=(2.6, 9.2),
                color=HIVE, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=HIVE, lw=1.3))
    ax.set_xlabel("$x_1$   (with $x_2$ held at 0)")
    ax.set_ylabel("$f(x_1, 0)$")
    ax.set_title("A slice through the surface: every dip can stop a downhill search",
                 color=BROWN, fontsize=12)
    ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, "02_ackley_slice.png")


# =====================================================================
# 03  the initial food sources
# =====================================================================
def fig_initial_sources():
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    ax.contourf(X1, X2, Z, levels=45, cmap=HONEY, alpha=0.93)
    ax.scatter(initial_sources[:, 0], initial_sources[:, 1], s=90,
               color="white", edgecolor=BROWN, linewidth=1.2, zorder=4,
               label=f"{SETTINGS.n_sources} food sources")
    best0 = int(np.argmin(initial_values))
    ax.scatter(*initial_sources[best0], s=250, color=AMBER, edgecolor=BROWN,
               marker="h", linewidth=1.8, zorder=5, label="richest source so far")
    ax.scatter(0, 0, marker="*", s=300, color="white", edgecolor=BROWN,
               linewidth=1.6, zorder=6, label="true optimum")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); ax.set_aspect("equal")
    ax.set_title("Cycle 0 - the bees are scattered at random", color=BROWN, fontsize=12)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.grid(False)
    fig.tight_layout()
    save(fig, "03_initial_sources.png")


# =====================================================================
# 04  the onlooker roulette wheel
# =====================================================================
def _pie(ax, values, settings, n_labelled, title):
    """All 25 slices are drawn; only the richest few carry a text label."""
    probabilities = selection_probabilities(values, settings)
    order = np.argsort(probabilities)[::-1]                 # richest first

    sizes = probabilities[order]
    shades = [HONEY(t) for t in np.linspace(0.30, 0.95, len(order))]
    labels = [(f"#{i}\nf={values[i]:.3g}" if rank < n_labelled else "")
              for rank, i in enumerate(order)]

    ax.pie(sizes, labels=labels, colors=shades, startangle=90, counterclock=False,
           autopct=lambda pct: f"{pct:.1f}%" if pct >= 5.5 else "",
           textprops={"fontsize": 8, "color": BROWN}, labeldistance=1.08,
           wedgeprops={"edgecolor": BG, "linewidth": 1.4})
    ax.set_title(title, color=BROWN, fontsize=11.5)
    return probabilities


def fig_roulette():
    fig, ax = plt.subplots(figsize=(7.6, 7.6))
    p = _pie(ax, initial_values, SETTINGS, 8,
             "The waggle-dance wheel at cycle 0\n"
             f"all {SETTINGS.n_sources} food sources, 8 richest labelled")
    ax.text(0, -1.33, "richest slice %.2f%%   poorest slice %.2f%%   ratio %.2f"
            % (100 * p.max(), 100 * p.min(), p.max() / p.min()),
            ha="center", fontsize=10.5, color=BROWN)
    fig.tight_layout()
    save(fig, "04_roulette_pie_cycle0.png")


# =====================================================================
# 05  why the plain slide formula flattens out
# =====================================================================
def fig_probability_problem():
    """What actually happens to the onlooker wheel - measured, not assumed."""
    plain = SETTINGS            # the deck uses the slide formula as the default
    # Cycle 50 is NOT uniform yet (slices still run 2.05 % - 4.08 %); the wheel
    # only flattens completely at cycle 62, so the "after" panel uses cycle 100.
    early_sources, early_values, _ = result["snapshots"][8]
    late_sources, late_values, _ = result["snapshots"][100]

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.2))
    # At cycle 100 all 25 slices are equal, so adjacent labels would collide:
    # label fewer of them on that side.
    for ax, values, cycle, n_lab in [(axes[0], early_values, 8, 5),
                                     (axes[1], late_values, 100, 3)]:
        p = _pie(ax, values, plain, n_lab,
                 f"cycle {cycle}   -   best $f$ = {values.min():.2g}")
        ax.text(0, -1.32, "richest %.2f%%    poorest %.2f%%    ratio %.2f"
                % (100 * p.max(), 100 * p.min(), p.max() / p.min()),
                ha="center", fontsize=11.5, color=BROWN)
    axes[0].text(0, -1.52, "the wheel still has shape", ha="center",
                 fontsize=12, color=DEEP, weight="bold")
    axes[1].text(0, -1.52, "every slice is now 1/25 = 4.00 %", ha="center",
                 fontsize=12, color=HIVE, weight="bold")

    fig.suptitle("The onlooker wheel really does go flat: $fit=1/(1+f)\\to 1$ "
                 "once every $f$ is tiny", color=BROWN, fontsize=13.5)
    fig.tight_layout()
    save(fig, "05_roulette_early_vs_late.png")

    # why it happens, and when - both on one page
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.0))

    ax = axes[0]
    f = np.logspace(-10, 1.2, 400)
    ax.semilogx(f, 1.0 / (1.0 + f), color=DEEP, linewidth=2.6)
    ax.axhline(1.0, color=GREY, linestyle="--", linewidth=1.2)
    ax.fill_between(f, 1.0 / (1.0 + f), 1.0, color=AMBER, alpha=0.25)
    ax.annotate("sources still differ here",
                xy=(2.0, 0.33), xytext=(0.12, 0.62), color=BROWN, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.2))
    ax.annotate("below $f\\approx10^{-3}$ every source\nscores the same",
                xy=(1e-7, 0.995), xytext=(2e-10, 0.45), color=HIVE, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=HIVE, lw=1.3))
    ax.set_xlabel("objective value  $f$")
    ax.set_ylabel("nectar amount  $fit = 1/(1+f)$")
    ax.set_title("The cause: the nectar rule saturates", color=BROWN, fontsize=12)

    ax = axes[1]
    ax.plot(history["cycle"], history["wheel_ratio"], color=DEEP, linewidth=2.6)
    ax.axhline(1.0, color=GREY, linestyle="--", linewidth=1.2)
    ax.fill_between(history["cycle"], 1.0, history["wheel_ratio"],
                    color=AMBER, alpha=0.28)
    flat = int(np.argmax(np.asarray(history["wheel_ratio"]) < 1.001))
    ax.axvline(flat, color=HIVE, linestyle=":", linewidth=1.8)
    ax.annotate("uniform from cycle %d onwards:\nthe onlookers now pick at random" % flat,
                xy=(flat, 1.05), xytext=(flat + 4, 4.0), color=HIVE, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=HIVE, lw=1.3))
    ax.set_xlabel("cycle")
    ax.set_ylabel("richest slice / poorest slice")
    ax.set_title("The effect: selection pressure disappears", color=BROWN, fontsize=12)

    fig.tight_layout()
    save(fig, "06_wheel_pressure.png")


# =====================================================================
# 06  the neighbourhood step, drawn
# =====================================================================
def fig_neighbour_step():
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.3))

    xi = np.array([1.8, 1.2])
    xk = np.array([-0.9, 2.6])
    delta = xi - xk                     # (2.7, -1.4)

    ax = axes[0]
    g = np.linspace(-4.6, 4.6, 320)
    A, B = np.meshgrid(g, g)
    ax.contourf(A, B, ackley(np.stack([A, B], axis=-1)), levels=40, cmap=HONEY)
    ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.6, 4.6)
    ax.grid(False)

    # Only ONE coordinate changes per trial, so the candidate lands on the
    # horizontal segment (j = 1) or the vertical segment (j = 2) through x_i.
    ax.plot([xi[0] - abs(delta[0]), xi[0] + abs(delta[0])], [xi[1], xi[1]],
            color="white", linewidth=6.0, solid_capstyle="round", zorder=3)
    ax.plot([xi[0] - abs(delta[0]), xi[0] + abs(delta[0])], [xi[1], xi[1]],
            color=BROWN, linewidth=2.4, solid_capstyle="round", zorder=4,
            label=r"if $j=1$: $v$ lands here")
    ax.plot([xi[0], xi[0]], [xi[1] - abs(delta[1]), xi[1] + abs(delta[1])],
            color="white", linewidth=6.0, solid_capstyle="round", zorder=3)
    ax.plot([xi[0], xi[0]], [xi[1] - abs(delta[1]), xi[1] + abs(delta[1])],
            color=DEEP, linewidth=2.4, solid_capstyle="round", zorder=4,
            label=r"if $j=2$: $v$ lands here")

    ax.annotate("", xy=tuple(xi), xytext=tuple(xk), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color="white", lw=3.4,
                                shrinkA=0, shrinkB=0))
    ax.annotate("", xy=tuple(xi), xytext=tuple(xk), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=1.5,
                                shrinkA=0, shrinkB=0))
    ax.text(-4.25, 3.65, r"$x_i-x_k$  sets how big the step can be",
            color=BROWN, fontsize=11.5,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9))
    ax.scatter(*xi, s=250, color=AMBER, edgecolor=BROWN, linewidth=1.8,
               zorder=7, label="$x_i$  (this bee's source)")
    ax.scatter(*xk, s=220, color="white", edgecolor=BROWN, linewidth=1.8,
               marker="h", zorder=7, label="$x_k$  (a random partner)")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$"); ax.set_aspect("equal")
    ax.set_title(r"$v_{ij} = x_{ij} + \varphi_{ij}\,(x_{ij} - x_{kj})$,"
                 "\none random coordinate $j$ moves", color=BROWN, fontsize=12.5)
    ax.legend(loc="lower left", fontsize=8.5, framealpha=0.92)

    # the self-shrinking property
    ax = axes[1]
    cycles, spreads = [], []
    for cycle, (src, val, tr) in sorted(result["snapshots"].items()):
        pairs = src[:, None, :] - src[None, :, :]
        cycles.append(cycle)
        spreads.append(np.abs(pairs).mean())
    ax.semilogy(history["cycle"], np.maximum(history["spread"], 1e-17),
                color=DEEP, linewidth=2.4, label="spread of the food sources")
    ax.semilogy(history["cycle"], np.maximum(history["best"], 1e-17),
                color=BROWN, linewidth=2.0, linestyle="--", label="best objective value")
    ax.scatter(cycles, np.maximum(spreads, 1e-17), s=70, color=AMBER,
               edgecolor=BROWN, zorder=5, label="mean $|x_i-x_k|$ at snapshots")
    ax.set_xlabel("cycle")
    ax.set_ylabel("size (log scale)")
    ax.set_title("The step size shrinks on its own:\n"
                 r"$|x_i-x_k|$ gets small as the swarm gathers",
                 color=BROWN, fontsize=12)
    ax.legend(fontsize=9, loc="lower left")

    fig.tight_layout()
    save(fig, "07_neighbour_step.png")


# =====================================================================
# 07  convergence and diversity
# =====================================================================
def fig_convergence():
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.7))
    floor = 1e-17

    ax = axes[0]
    ax.semilogy(history["cycle"], np.maximum(history["best"], floor),
                color=BROWN, linewidth=2.6, label="best so far")
    ax.semilogy(history["cycle"], np.maximum(history["mean"], floor),
                color=DEEP, linewidth=1.9, label="colony mean")
    ax.semilogy(history["cycle"], np.maximum(history["worst"], floor),
                color=GREY, linewidth=1.3, linestyle="--", label="colony worst")
    ax.axvline(result["best_cycle"], color=AMBER, linestyle=":", linewidth=2.0,
               label=f"best found (cycle {result['best_cycle']})")
    ax.set_xlabel("cycle")
    ax.set_ylabel("Ackley value (log scale)")
    ax.set_title("The colony closes in on the global minimum", color=BROWN, fontsize=12)
    ax.legend(fontsize=8.5, loc="lower right")

    def smooth(series, window=7):
        series = np.asarray(series, dtype=float)
        kernel = np.ones(window) / window
        return np.convolve(series, kernel, mode="same") / np.convolve(
            np.ones_like(series), kernel, mode="same")

    ax = axes[1]
    cycles = history["cycle"][:-1]
    ax.fill_between(cycles, smooth(history["employed_improved"][:-1]),
                    color=DEEP, alpha=0.75, label="employed bees that improved")
    ax.fill_between(cycles, smooth(history["onlooker_improved"][:-1]),
                    color=AMBER, alpha=0.70, label="onlooker visits that improved")
    ax.set_xlabel("cycle")
    ax.set_ylabel("successful visits per cycle (smoothed)")
    ax.set_ylim(0, max(SETTINGS.n_sources, SETTINGS.n_onlookers) * 0.75)
    ax.set_title("Both phases keep paying off all the way to cycle 100",
                 color=BROWN, fontsize=12)
    ax.legend(fontsize=8.5, loc="lower left")

    twin = ax.twinx()
    twin.plot(history["cycle"], history["max_trial"], color=BROWN,
              linewidth=1.6, alpha=0.9)
    twin.axhline(SETTINGS.limit, color=BROWN, linestyle="--", linewidth=1.4)
    twin.set_ylim(0, SETTINGS.limit * 1.18)
    twin.set_ylabel("largest trial counter (dark brown)", color=BROWN)
    twin.tick_params(axis="y", labelcolor=BROWN)
    twin.grid(False)
    twin.annotate("limit = %d: never reached,\nso no scout was ever needed" % SETTINGS.limit,
                  xy=(52, SETTINGS.limit), xytext=(30, SETTINGS.limit * 0.72),
                  color=BROWN, fontsize=9.5,
                  bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=BROWN, lw=0.9),
                  arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.2))

    fig.tight_layout()
    save(fig, "08_convergence_and_work.png")


# =====================================================================
# 08  the path of the best solution
# =====================================================================
def fig_path():
    path = np.column_stack([history["best_x1"], history["best_x2"]])
    changed = np.r_[True, np.any(np.diff(path, axis=0) != 0, axis=1)]
    improvements = path[changed]

    fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.6))
    for ax, limit, label in [(axes[0], 5.0, "the whole search space"),
                             (axes[1], 0.45, "zoomed in on the optimum")]:
        g = np.linspace(-limit, limit, 400)
        A, B = np.meshgrid(g, g)
        filled = ax.contourf(A, B, ackley(np.stack([A, B], axis=-1)),
                             levels=45, cmap=HONEY)
        bar = fig.colorbar(filled, ax=ax, fraction=0.046)
        bar.set_label("Ackley value", color=BROWN)
        inside = np.all(np.abs(improvements) <= limit, axis=1)
        ax.plot(improvements[inside, 0], improvements[inside, 1], "o-",
                color="white", markeredgecolor=BROWN, markersize=6,
                linewidth=1.8, label="best-so-far path")
        ax.scatter(0, 0, marker="*", s=320, color="white", edgecolor=BROWN,
                   linewidth=1.6, zorder=6, label="true optimum $(0,0)$")
        ax.scatter(best_x1, best_x2, marker="h", s=150, color=AMBER,
                   edgecolor=BROWN, linewidth=1.4, zorder=6, label="ABC result")
        ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
        ax.set_title(f"Best-solution path - {label}", color=BROWN, fontsize=12)
        ax.set_aspect("equal")
        ax.grid(False)
        ax.legend(loc="upper right", fontsize=8.5)

    fig.tight_layout()
    save(fig, "09_best_solution_path.png")


# =====================================================================
# 09  snapshots of the food sources
# =====================================================================
def fig_snapshots():
    available = [c for c in SNAPSHOTS if c in result["snapshots"]]
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 8.8))

    for ax, cycle in zip(axes.ravel(), available):
        src, val, tr = result["snapshots"][cycle]
        limit = max(min(1.5 * np.abs(src).max(), 5.2), 1e-13)
        g = np.linspace(-limit, limit, 200)
        A, B = np.meshgrid(g, g)
        ax.contourf(A, B, ackley(np.stack([A, B], axis=-1)), levels=40, cmap=HONEY)
        ax.scatter(src[:, 0], src[:, 1], s=58, color="white", edgecolor=BROWN,
                   linewidth=1.1, zorder=4)
        ax.scatter(0, 0, marker="*", s=200, color="white", edgecolor=BROWN,
                   linewidth=1.3, zorder=5)
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit); ax.set_aspect("equal")
        ax.set_title("cycle %d   -   best f = %.2e\nview half-width = %.1e"
                     % (cycle, val.min(), limit), fontsize=9.5, color=BROWN)
        ax.set_xticks([-limit, 0, limit])
        ax.set_xticklabels([f"{-limit:.1e}", "0", f"{limit:.1e}"], fontsize=7.5)
        ax.set_yticks([-limit, 0, limit])
        ax.set_yticklabels([f"{-limit:.1e}", "0", f"{limit:.1e}"], fontsize=7.5)
        ax.grid(False)

    for ax in axes.ravel()[len(available):]:
        ax.axis("off")

    fig.suptitle("The food sources gather on the global minimum - watch the axis scale",
                 fontsize=13, color=BROWN)
    fig.tight_layout()
    save(fig, "10_source_snapshots.png")


# =====================================================================
# 10  reliability over 40 runs
# =====================================================================
def fig_reliability(n_runs=40):
    values, solutions, cycles = [], [], []
    for seed in range(n_runs):
        one = run_abc(replace(SETTINGS, seed=seed), verbose=False)
        values.append(one["best_value"])
        solutions.append(one["best_solution"])
        cycles.append(one["cycles_run"])
    values = np.asarray(values)
    solutions = np.asarray(solutions)
    distances = np.linalg.norm(solutions, axis=1)
    precise = values < 1e-6
    in_valley = distances < 0.5

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.4))

    ax = axes[0]
    ax.bar(np.arange(n_runs), np.maximum(values, 1e-18),
           color=[AMBER if p else "#B04B26" for p in precise],
           edgecolor=BROWN, linewidth=0.6)
    ax.set_yscale("log")
    ax.axhline(1e-6, color=BROWN, linestyle="--", linewidth=1.2,
               label="success threshold $10^{-6}$")
    ax.set_xlabel("run (seed)")
    ax.set_ylabel("final best $f$  (log scale)")
    ax.set_title("Final result of each of the %d runs" % n_runs, color=BROWN, fontsize=12)
    ax.legend(fontsize=8.5, loc="lower right")

    # On the full +-5 map all 40 points land on one pixel, so zoom right in.
    ax = axes[1]
    half = max(2.2 * np.abs(solutions).max(), 1e-13)
    g = np.linspace(-half, half, 200)
    A, B = np.meshgrid(g, g)
    ax.contourf(A, B, ackley(np.stack([A, B], axis=-1)), levels=45, cmap=HONEY)
    ax.scatter(solutions[in_valley, 0], solutions[in_valley, 1], s=95, color="white",
               edgecolor=BROWN, linewidth=1.3, zorder=4,
               label="%d runs inside this view" % in_valley.sum())
    if (~in_valley).any():
        ax.scatter(solutions[~in_valley, 0], solutions[~in_valley, 1], s=150,
                   color="#B04B26", marker="X", edgecolor="white", linewidth=1.0,
                   zorder=5, label="%d trapped run(s)" % (~in_valley).sum())
    ax.scatter(0, 0, marker="*", s=420, color=AMBER, edgecolors=BROWN,
               linewidths=1.4, zorder=6, label="true optimum $(0,0)$")
    ax.set_xlim(-half, half); ax.set_ylim(-half, half); ax.set_aspect("equal")
    ax.set_xticks([-half, 0, half]); ax.set_yticks([-half, 0, half])
    ax.set_xticklabels([f"{-half:.0e}", "0", f"{half:.0e}"], fontsize=8.5)
    ax.set_yticklabels([f"{-half:.0e}", "0", f"{half:.0e}"], fontsize=8.5)
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.set_title("Where the %d runs finished\n(zoomed to a half-width of %.0e)"
                 % (n_runs, half), color=BROWN, fontsize=12)
    ax.grid(False)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.93)

    fig.tight_layout()
    save(fig, "11_reliability_40_runs.png")
    return values, solutions, cycles


# =====================================================================
# 11  the three bee roles, as a diagram
# =====================================================================
def fig_bee_roles():
    fig, ax = plt.subplots(figsize=(13.0, 4.6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 4.6); ax.axis("off")
    ax.set_facecolor(BG)

    panels = [
        ("EMPLOYED BEES", f"{SETTINGS.n_sources} bees - one per food source",
         "Each one tries a nearby point.\nKeeps the better of the two.", AMBER, "Exploitation"),
        ("ONLOOKER BEES", f"{SETTINGS.n_onlookers} bees - choose by roulette wheel",
         "Richer sources get more visits.\nSame nearby search, more often.", DEEP, "Guided search"),
        ("SCOUT BEES", f"abandon after {SETTINGS.limit} failed tries",
         "A stuck source is thrown away\nand replaced at random.", HIVE, "Exploration"),
    ]
    for k, (title, sub, body, colour, purpose) in enumerate(panels):
        x = 0.25 + k * 4.25
        ax.add_patch(plt.Rectangle((x, 0.35), 3.95, 3.9, facecolor="white",
                                   edgecolor=colour, linewidth=2.4, zorder=1,
                                   joinstyle="round"))
        ax.add_patch(plt.Rectangle((x, 3.52), 3.95, 0.73, facecolor=colour,
                                   edgecolor=colour, linewidth=2.4, zorder=2))
        ax.text(x + 1.98, 3.86, title, ha="center", va="center", fontsize=13.5,
                color=BROWN if colour == AMBER else "white", weight="bold", zorder=3)
        ax.text(x + 1.98, 3.12, sub, ha="center", va="center", fontsize=10, color=BROWN)
        ax.text(x + 1.98, 2.15, body, ha="center", va="center", fontsize=11.5, color=BROWN)
        ax.text(x + 1.98, 0.85, purpose, ha="center", va="center", fontsize=12.5,
                color=colour, weight="bold")

    for x in (4.3, 8.55):
        ax.annotate("", xy=(x + 0.35, 2.3), xytext=(x - 0.1, 2.3),
                    arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=2.2))

    fig.tight_layout()
    save(fig, "12_bee_roles.png")


# =====================================================================
# 12  ABC vs GA vs random search, same budget
# =====================================================================
def fig_budget_comparison(budget):
    rng = np.random.default_rng(SETTINGS.seed)
    points = rng.uniform(SETTINGS.lower, SETTINGS.upper, size=(budget, 2))
    running = np.minimum.accumulate(ackley(points))

    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.semilogy(np.arange(1, budget + 1), np.maximum(running, 1e-18),
                color=GREY, linewidth=2.0, label="random search (same budget)")

    # Actual cost, not the budget: 25 employed + 25 onlooker trials per cycle,
    # plus one more only on a cycle where a scout really flew.
    per_cycle = SETTINGS.n_sources + SETTINGS.n_onlookers
    scouts_so_far = np.cumsum(np.asarray(history["scouts"]))
    used = (SETTINGS.n_sources + np.asarray(history["cycle"]) * per_cycle
            + scouts_so_far)
    ax.semilogy(used, np.maximum(history["best"], 1e-18),
                color=DEEP, linewidth=2.6, label="Artificial Bee Colony")
    ax.set_xlabel("Ackley evaluations used")
    ax.set_ylabel("best value found (log scale)")
    ax.set_title("Same number of evaluations, very different results",
                 color=BROWN, fontsize=12)
    ax.legend(fontsize=9.5)
    fig.tight_layout()
    save(fig, "13_budget_comparison.png")
    return float(running[-1])


if __name__ == "__main__":
    fig_landscape()
    fig_slice()
    fig_initial_sources()
    fig_roulette()
    fig_probability_problem()
    fig_neighbour_step()
    fig_convergence()
    fig_path()
    fig_snapshots()
    fig_bee_roles()
    values, solutions, cycles = fig_reliability()
    random_best = fig_budget_comparison(result["evaluations"])

    print()
    print("main run     : f = %.6e at (%+.3e, %+.3e), cycle %d, %d evaluations"
          % (best_f, best_x1, best_x2, result["best_cycle"], result["evaluations"]))
    print("random search: f = %.6e" % random_best)
    print("40 runs      : median %.3e  worst %.3e  success %.0f%%"
          % (np.median(values), values.max(), 100 * (values < 1e-6).mean()))
