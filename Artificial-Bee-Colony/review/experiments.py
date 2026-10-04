"""Every number quoted on the slides, reproduced from scratch."""
import sys, json, math
from pathlib import Path
import numpy as np
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from abc_core import run_abc, ackley, SETTINGS, ABCSettings

N = 40
def sweep(label, changes, n=N):
    v, d, cy, bc, ev, sc = [], [], [], [], [], []
    for s in range(n):
        r = run_abc(replace(SETTINGS, seed=s, **changes), verbose=False)
        v.append(r["best_value"]); d.append(float(np.linalg.norm(r["best_solution"])))
        cy.append(r["cycles_run"]); bc.append(r["best_cycle"]); ev.append(r["evaluations"])
        sc.append(int(np.sum(r["history"]["scouts"])))
    v = np.asarray(v); d = np.asarray(d)
    return dict(label=label, best=float(v.min()), median=float(np.median(v)), worst=float(v.max()),
                valley=int((d < 0.5).sum()), success=int((v < 1e-6).sum()), runs=n,
                mean_cycles=float(np.mean(cy)), mean_best_cycle=float(np.mean(bc)),
                mean_evals=float(np.mean(ev)), total_scouts=int(np.sum(sc)))

ABLATION = [
    ("full ABC as taught", {}),
    ("no onlooker phase", {"use_onlookers": False}),
    ("no scout phase", {"use_scouts": False}),
    ("scaled P (Karaboga variant)", {"probability_kind": "scaled"}),
    ("rank-based P", {"probability_kind": "rank"}),
    ("windowing fitness", {"fitness_kind": "windowing"}),
    ("perturb both coordinates", {"neighbour_kind": "all_dims"}),
    ("limit = 5", {"limit": 5}),
    ("limit = 10", {"limit": 10}),
    ("limit = 25", {"limit": 25}),
    ("limit = 100", {"limit": 100}),
    ("colony 10  (5 sources)", {"colony_size": 10, "limit": 10}),
    ("colony 20  (10 sources)", {"colony_size": 20, "limit": 20}),
    ("colony 100 (50 sources)", {"colony_size": 100, "limit": 100}),
]

def ga_reference(n_runs):
    """Re-run the sister project's GA notebook code, same seeds, for comparison."""
    import io, json as js, contextlib, dataclasses
    import matplotlib
    matplotlib.use("Agg")
    nb = js.loads((Path(__file__).resolve().parents[2] / "Ackley_GA_Solution.ipynb")
                  .read_text(encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    ns = {}
    wanted = ("import math", "class GASettings", "def ackley", "def create_population",
              "def to_fitness", "def roulette_wheel", "def one_point_crossover",
              "def mutation_sigma", "def make_offspring", "def select_survivors", "def run_ga")
    with contextlib.redirect_stdout(io.StringIO()):
        for cell in code:
            src = "".join(cell["source"])
            if any(w in src for w in wanted):
                exec(compile(src, "<ga-notebook>", "exec"), ns)
    run_ga, gs = ns["run_ga"], ns["SETTINGS"]
    values = np.asarray([run_ga(dataclasses.replace(gs, seed=s), verbose=False)["best_value"]
                         for s in range(n_runs)])
    return {"best": float(values.min()), "median": float(np.median(values)),
            "worst": float(values.max()), "success": int((values < 1e-6).sum()),
            "runs": n_runs,
            "evaluations": int(gs.population_size * (gs.max_generations + 1))}


if __name__ == "__main__":
    out = {"ablation": [sweep(l, c) for l, c in ABLATION]}

    main = run_abc(SETTINGS, verbose=False)
    out["main_run"] = {
        "x1": float(main["best_solution"][0]), "x2": float(main["best_solution"][1]),
        "f": float(main["best_value"]), "cycle": main["best_cycle"],
        "cycles_run": main["cycles_run"], "stop_reason": main["stop_reason"],
        "distance": float(np.linalg.norm(main["best_solution"])),
        "evaluations": main["evaluations"],
        "evaluation_budget": main["evaluation_budget"],
        "scout_events": [[int(c), [int(i) for i in s]] for c, s in main["scout_events"]],
    }

    rng = np.random.default_rng(SETTINGS.seed)
    pts = rng.uniform(SETTINGS.lower, SETTINGS.upper, size=(main["evaluations"], 2))
    out["random_search"] = {"budget": main["evaluations"], "f": float(ackley(pts).min())}

    # head to head against the genetic algorithm of the sister project
    out["genetic_algorithm"] = ga_reference(N)

    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for r in out["ablation"]:
        print("%-28s best %9.3e  med %9.3e  worst %9.3e  valley %2d/%d  ok %2d/%d  cyc %5.1f  scouts %3d"
              % (r["label"], r["best"], r["median"], r["worst"], r["valley"], r["runs"],
                 r["success"], r["runs"], r["mean_cycles"], r["total_scouts"]))
    print()
    print("main:", out["main_run"])
    print("random:", out["random_search"])
    print("GA:", out["genetic_algorithm"])
