"""Artificial Bee Colony (ABC) for the 2-D Ackley function.

This is the reference implementation. The notebook re-creates the same
functions step by step; this file exists so that the figures, the slide
numbers and the notebook all come from one tested source.

Everything follows the course slides "7. ABC Edited":

    Step 1  assign control parameters
    Step 2  initialise solutions          x_ij = x_min + rand(0,1)(x_max - x_min)
    Step 3  repeat until the stopping rule fires
              employed bee phase          v_ij = x_ij + phi_ij (x_ij - x_kj)
              onlooker bee phase          P_i = fit_i / sum(fit), roulette wheel
              scout bee phase             trial_i > limit -> new random source
              memorise the best solution
    Step 4  stop
"""

import math
from dataclasses import dataclass, replace

import numpy as np


# ----------------------------------------------------------------------
# 1. The objective function
# ----------------------------------------------------------------------

def ackley(x, a=20.0, b=0.2, c=2.0 * math.pi):
    """Ackley objective value. Smaller is better; f(0,0) = 0.

    Accepts one food source of shape (n_dimensions,) or a whole array of
    food sources of shape (n_sources, n_dimensions).
    """
    x = np.asarray(x, dtype=float)
    n = x.shape[-1]

    mean_of_squares = np.sum(x ** 2, axis=-1) / n
    mean_of_cosines = np.sum(np.cos(c * x), axis=-1) / n

    exponential_part = -a * np.exp(-b * np.sqrt(mean_of_squares))
    cosine_part = -np.exp(mean_of_cosines)

    return exponential_part + cosine_part + a + math.e


GLOBAL_OPTIMUM = np.array([0.0, 0.0])


# ----------------------------------------------------------------------
# 2. Control parameters  (slide 20)
# ----------------------------------------------------------------------

@dataclass
class ABCSettings:
    """Every knob of the Artificial Bee Colony, in one place."""

    # --- fixed by the assignment -------------------------------------
    colony_size: int = 50            # 50 bees in total, like the 50 chromosomes
    n_dimensions: int = 2            # food source = [x1, x2]
    lower: float = -5.0              # lower bound of every coordinate
    upper: float = 5.0               # upper bound of every coordinate
    max_cycles: int = 100            # stopping criterion 1

    # --- standard ABC parameters (slide 20) --------------------------
    # employed bees = onlookers = 50% of the colony, so
    #   n_sources = n_employed = n_onlookers = colony_size // 2
    limit: int = 50                  # n_sources * n_dimensions = 25 * 2
    n_scouts_per_cycle: int = 1      # at most one scout per cycle

    # --- our own implementation choices ------------------------------
    fitness_kind: str = "karaboga"   # "karaboga" or "windowing"        (S7)
    probability_kind: str = "plain"  # "plain" (the slide), "scaled", "rank" (S9)
    neighbour_kind: str = "one_dim"  # "one_dim" or "all_dims"          (S8)
    use_onlookers: bool = True       # ablation switch only
    use_scouts: bool = True          # ablation switch only
    tolerance: float = 1e-10         # stopping criterion 2
    patience: int = 20               # ... held for this many cycles
    seed: int = 7                    # reproducibility

    @property
    def n_sources(self):
        """Number of food sources = number of employed bees = 50% of colony."""
        return self.colony_size // 2

    @property
    def n_onlookers(self):
        """Onlookers are the other 50% of the colony."""
        return self.colony_size - self.n_sources


SETTINGS = ABCSettings()


# ----------------------------------------------------------------------
# 3. Initial food sources  (slide 21)
# ----------------------------------------------------------------------

def create_sources(rng, settings):
    """Step 2:  x_ij = x_min,j + rand(0,1) * (x_max,j - x_min,j)."""
    shape = (settings.n_sources, settings.n_dimensions)
    return settings.lower + rng.random(shape) * (settings.upper - settings.lower)


# ----------------------------------------------------------------------
# 4. Nectar amount = fitness  (minimisation -> maximisation)
# ----------------------------------------------------------------------

def to_fitness(values, kind="karaboga"):
    """Turn objective values (lower is better) into fitness (higher is better).

    "karaboga" is the standard ABC rule:
        fit = 1 / (1 + f)        when f >= 0
        fit = 1 + |f|            when f <  0
    Ackley is never negative, so only the first line is used here.
    """
    values = np.asarray(values, dtype=float)

    if kind == "karaboga":
        return np.where(values >= 0.0, 1.0 / (1.0 + values), 1.0 + np.abs(values))

    if kind == "windowing":
        worst, best = values.max(), values.min()
        offset = 0.10 * (worst - best) + 1e-12
        return (worst - values) + offset

    raise ValueError(f"unknown fitness kind: {kind!r}")


def selection_probabilities(values, settings):
    """Slide 25:  P_i = fit_i / sum_j fit_j, with two safer variants.

    "plain"  - exactly the slide formula.
    "scaled" - Karaboga's own published variant, 0.9 * fit_i / fit_max + 0.1.
               Needed because 1/(1+f) flattens to 1 for every source once the
               colony is close to the optimum, which makes the wheel uniform.
    "rank"   - probability from the rank instead of the value.
    """
    fitness = to_fitness(values, settings.fitness_kind)

    if settings.probability_kind == "plain":
        weights = fitness
    elif settings.probability_kind == "scaled":
        weights = 0.9 * fitness / fitness.max() + 0.1
    elif settings.probability_kind == "rank":
        order = np.argsort(np.argsort(values))          # 0 = best
        weights = (len(values) - order).astype(float)
    else:
        raise ValueError(f"unknown probability kind: {settings.probability_kind!r}")

    total = weights.sum()
    if not np.isfinite(total) or total <= 0:
        return np.full(len(weights), 1.0 / len(weights))
    return weights / total


def roulette_wheel(probabilities, rng, k=1):
    """Spin a fitness-proportional wheel k times; return the chosen indices."""
    wheel = np.cumsum(probabilities)
    wheel[-1] = 1.0                                     # floating-point guard
    return np.searchsorted(wheel, rng.random(k), side="right")


# ----------------------------------------------------------------------
# 5. Neighbourhood search  (slide 23)
# ----------------------------------------------------------------------

def neighbour(sources, i, rng, settings):
    """v_ij = x_ij + phi_ij (x_ij - x_kj),  phi in (-1, 1),  k != i.

    The new source starts as an exact copy of source i, then one randomly
    chosen coordinate j is changed. Only that coordinate moves, so the new
    source always stays in the neighbourhood of the old one.
    """
    if settings.n_sources < 2:
        raise ValueError("ABC needs at least 2 food sources, because the neighbourhood "
                         "equation has to pick a partner k != i "
                         f"(colony_size={settings.colony_size} gives only "
                         f"{settings.n_sources})")

    candidate = sources[i].copy()

    partner = int(rng.integers(settings.n_sources - 1))  # k = rand(1, n), k != i
    if partner >= i:
        partner += 1

    if settings.neighbour_kind == "all_dims":
        dims = np.arange(settings.n_dimensions)
    else:
        dims = [int(rng.integers(settings.n_dimensions))]

    for j in dims:
        phi = rng.uniform(-1.0, 1.0)
        candidate[j] = sources[i, j] + phi * (sources[i, j] - sources[partner, j])
        # Keep the source inside the search space (slide 21 bounds).
        candidate[j] = min(max(candidate[j], settings.lower), settings.upper)

    return candidate


def greedy_select(sources, values, trials, i, candidate, candidate_value):
    """Keep the better of x_i and v_i; reset or raise the trial counter."""
    if candidate_value < values[i]:
        sources[i] = candidate
        values[i] = candidate_value
        trials[i] = 0                                   # improvement found
        return True
    trials[i] += 1                                      # no improvement
    return False


# ----------------------------------------------------------------------
# 6. The three bee phases
# ----------------------------------------------------------------------

def employed_bee_phase(sources, values, trials, rng, settings):
    """Every employed bee tries one new source next to the one it owns."""
    improved = 0
    for i in range(settings.n_sources):
        candidate = neighbour(sources, i, rng, settings)
        improved += greedy_select(sources, values, trials, i,
                                  candidate, float(ackley(candidate)))
    return improved


def onlooker_bee_phase(sources, values, trials, rng, settings):
    """Onlookers watch the waggle dance and pick sources by roulette wheel."""
    probabilities = selection_probabilities(values, settings)
    improved = 0
    picks = roulette_wheel(probabilities, rng, settings.n_onlookers)
    for i in picks:
        i = int(i)
        candidate = neighbour(sources, i, rng, settings)
        improved += greedy_select(sources, values, trials, i,
                                  candidate, float(ackley(candidate)))
    return improved, probabilities, picks


def scout_bee_phase(sources, values, trials, rng, settings):
    """A source that has not improved for `limit` tries is abandoned."""
    scouted = []
    for _ in range(settings.n_scouts_per_cycle):
        worst = int(np.argmax(trials))
        if trials[worst] <= settings.limit:
            break
        sources[worst] = settings.lower + rng.random(settings.n_dimensions) * (
            settings.upper - settings.lower)
        values[worst] = float(ackley(sources[worst]))
        trials[worst] = 0
        scouted.append(worst)
    return scouted


# ----------------------------------------------------------------------
# 7. The complete ABC loop  (slide 18)
# ----------------------------------------------------------------------

def run_abc(settings=SETTINGS, verbose=True, snapshot_at=()):
    """Run the full Artificial Bee Colony and return everything worth reporting."""
    rng = np.random.default_rng(settings.seed)

    sources = create_sources(rng, settings)                      # Step 2
    values = ackley(sources)
    trials = np.zeros(settings.n_sources, dtype=int)

    best_index = int(np.argmin(values))
    best_solution = sources[best_index].copy()                   # memorise best
    best_value = float(values[best_index])
    best_cycle = 0

    history = {key: [] for key in
               ("cycle", "best", "mean", "worst", "best_x1", "best_x2",
                "spread", "max_trial", "scouts", "distinct",
                "employed_improved", "onlooker_improved", "wheel_ratio")}
    snapshots = {}
    scout_events = []
    stagnation = 0
    stop_reason = f"reached the maximum of {settings.max_cycles} cycles"

    # Count every Ackley call for real, rather than assuming a scout flies each
    # cycle. Step 2 already tasted all the initial sources.
    evaluations = settings.n_sources

    for cycle in range(settings.max_cycles + 1):
        history["cycle"].append(cycle)
        history["best"].append(best_value)
        history["mean"].append(float(values.mean()))
        history["worst"].append(float(values.max()))
        history["best_x1"].append(float(best_solution[0]))
        history["best_x2"].append(float(best_solution[1]))
        history["spread"].append(float(np.mean(np.std(sources, axis=0))))
        history["max_trial"].append(int(trials.max()))
        history["distinct"].append(int(len(np.unique(sources, axis=0))))
        wheel = selection_probabilities(values, settings)
        history["wheel_ratio"].append(float(wheel.max() / wheel.min()))
        if cycle in snapshot_at:
            snapshots[cycle] = (sources.copy(), values.copy(), trials.copy())

        # --- stopping criteria ---------------------------------------
        if cycle == settings.max_cycles:
            history["scouts"].append(0)
            history["employed_improved"].append(0)
            history["onlooker_improved"].append(0)
            break
        if stagnation >= settings.patience:
            stop_reason = (f"improvement stayed below {settings.tolerance:g} "
                           f"for {settings.patience} cycles in a row")
            history["scouts"].append(0)
            history["employed_improved"].append(0)
            history["onlooker_improved"].append(0)
            break

        previous_best = best_value

        n_employed = employed_bee_phase(sources, values, trials, rng, settings)
        evaluations += settings.n_sources           # one trial point per employed bee
        if settings.use_onlookers:
            n_onlooker, _, _ = onlooker_bee_phase(sources, values, trials, rng, settings)
            evaluations += settings.n_onlookers     # one trial point per onlooker visit
        else:
            n_onlooker = 0

        # Memorise the best source before the scout can overwrite it.
        cycle_best = int(np.argmin(values))
        if values[cycle_best] < best_value:
            best_value = float(values[cycle_best])
            best_solution = sources[cycle_best].copy()
            best_cycle = cycle + 1

        scouted = (scout_bee_phase(sources, values, trials, rng, settings)
                   if settings.use_scouts else [])
        evaluations += len(scouted)                 # a scout only costs when it flies
        if scouted:
            scout_events.append((cycle + 1, scouted))

        history["scouts"].append(len(scouted))
        history["employed_improved"].append(n_employed)
        history["onlooker_improved"].append(n_onlooker)

        stagnation = stagnation + 1 if (previous_best - best_value) < settings.tolerance else 0

    result = {
        "best_solution": best_solution,
        "best_value": best_value,
        "best_cycle": best_cycle,
        "cycles_run": history["cycle"][-1],
        "stop_reason": stop_reason,
        "history": {key: np.asarray(value) for key, value in history.items()},
        "sources": sources,
        "values": values,
        "trials": trials,
        "snapshots": snapshots,
        "scout_events": scout_events,
        "settings": settings,
        # "evaluations" is the number of Ackley calls that actually happened.
        # "evaluation_budget" is the worst case, assuming every scout slot is used.
        "evaluations": evaluations,
        "evaluation_budget": settings.n_sources
                             + history["cycle"][-1] * (settings.n_sources
                                                       + settings.n_onlookers
                                                       + settings.n_scouts_per_cycle),
    }

    if verbose:
        print("stopped because : " + stop_reason)
        print("cycles run      : %d" % result["cycles_run"])
        print("best found at   : cycle %d" % best_cycle)
        print("best x1         : %+.14f" % best_solution[0])
        print("best x2         : %+.14f" % best_solution[1])
        print("best f(x1, x2)  : %.12e" % best_value)

    return result


if __name__ == "__main__":
    out = run_abc()
    print()
    print("distance to (0,0) :", np.linalg.norm(out["best_solution"]))
    print("evaluations       :", out["evaluations"])
    print("scout events      :", out["scout_events"][:10])
