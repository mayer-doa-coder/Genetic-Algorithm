from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "Ackley_GA_Solution.ipynb"
BACKUP_DIR = ROOT / "presentation_backup"
BACKUP = BACKUP_DIR / "Ackley_GA_Solution_before_simplifying.ipynb"


INTRO = r"""# 2-D Ackley Function with a Genetic Algorithm

**Course:** CSE 4111 — Machine Learning  
**Goal:** Find a point close to $(0,0)$ where the Ackley function is close to $0$.

The GA uses 50 real-valued chromosomes, roulette-wheel selection, one-point crossover, Gaussian mutation, and one elite. Run the cells from top to bottom."""


GUIDES = {
    11: r"""## 1. Imports and display settings

- Import the numerical and plotting libraries used below.
- Set compact NumPy output and a consistent Matplotlib style.
- The printed versions make the run easier to reproduce.""",

    12: r"""## 2. Genetic Algorithm settings

- Store every GA parameter in one `GASettings` object.
- The assignment fixes the population, generation, crossover, mutation, and elitism values.
- The remaining fields record our choices, including adaptive mutation and the duplicate limit.""",

    14: r"""## 3. Ackley objective function

This cell implements

$$f(\mathbf{x})=-20e^{-0.2\sqrt{\frac{1}{n}\sum x_i^2}}-e^{\frac{1}{n}\sum\cos(2\pi x_i)}+20+e.$$

- It accepts one chromosome or a full population.
- Lower values are better; the theoretical minimum is at $(0,0)$.
- The example calls provide a quick formula check.""",

    16: r"""## 4. View the search landscape

- Evaluate Ackley on a grid over $[-5,5]^2$.
- Draw a 3-D surface and a contour map.
- The ripples are local minima; the red star marks the global minimum.""",

    17: r"""## 5. View a one-dimensional slice

- Hold $x_2=0$ and vary $x_1$ from $-5$ to $5$.
- This makes the repeated local dips easier to see.
- The printed values compare the centre with nearby integer locations.""",

    19: r"""## 6. Create the initial population

- Draw 50 chromosomes uniformly from the allowed range.
- Each chromosome has two real-valued genes: `[x1, x2]`.
- Evaluate the starting population and print a small sample.""",

    20: r"""## 7. Plot generation 0

- Show all initial chromosomes on the Ackley landscape.
- Highlight the best starting chromosome and the known optimum.
- The initial population is spread widely because it has not learned yet.""",

    22: r"""## 8. Convert objective values to selection probabilities

- Ackley is minimized, so a smaller objective value must produce higher fitness.
- `windowing` subtracts each value from the current worst value and adds a positive offset.
- The probabilities are normalized so they sum to one.""",

    24: r"""## 9. Roulette-wheel selection

- Build cumulative probability intervals around the wheel.
- Generate random spins and return the selected chromosome indices.
- A 20,000-spin check compares observed shares with the requested probabilities.""",

    26: r"""## 10. Plot the roulette wheel

- Draw the selection probabilities for generation 0.
- Label the 10 largest slices and group the other 40 for readability.
- The algorithm still keeps all 50 probabilities separately.""",

    27: r"""## 11. Inspect the strongest roulette candidates

- Rank the initial chromosomes by objective value.
- Print fitness, wheel share, and expected selections for the best eight.
- Also report the worst chromosome to confirm that it keeps a small chance.""",

    29: r"""## 12. One-point crossover

- With two genes, the only cut is between $x_1$ and $x_2$.
- With probability $P_c=0.80$, the parents exchange their second genes.
- Crossover rearranges existing values; it does not create a new value.""",

    31: r"""## 13. Mutation and boundary repair

- `mutation_sigma` chooses the Gaussian step size.
- Each gene mutates independently with probability $P_m=0.05$.
- Changed genes are clipped to $[-5,5]$ so every chromosome remains valid.""",

    33: r"""## 14. Produce one batch of children

- Convert objective values to roulette probabilities and select parents.
- Apply crossover, mutation, and boundary repair.
- Return 50 children and evaluate them with the Ackley function.""",

    35: r"""## 15. Select the next generation

- Preserve the elite and rank the remaining parents and children together.
- Fill the population with the best candidates while limiting exact duplicates.
- If the limit leaves empty seats, add and evaluate fresh random chromosomes.""",

    37: r"""## 16. Complete GA loop

- Combine initialization, evaluation, reproduction, and survivor selection.
- Track the best solution, population statistics, mutation step, and snapshots.
- Stop at 100 generations or after 20 consecutive improvements below the tolerance.""",

    39: r"""## 17. Run the main experiment

- Use random seed 7 so the main result can be repeated.
- Save populations at selected generations for later plots.
- Store the final result and its history for the remaining analysis.""",

    41: r"""## 18. Report the final solution

- Print the best coordinates, function value, and generation found.
- Compare the result with the theoretical optimum $(0,0)$.
- Report coordinate error, Euclidean distance, and the evaluation budget.""",

    44: r"""## 19. Plot convergence and diversity

- The left plot tracks best, mean, and worst objective values on a log scale.
- The right plot tracks population spread, mutation step, and distinct chromosomes.
- These curves show how the search narrows while keeping some variety.""",

    45: r"""## 20. Print selected generations

- Show the first few generations and then every tenth generation.
- Include objective values, best coordinates, mutation step, and diversity.
- The best column should never increase because the elite is preserved.""",

    48: r"""## 21. Plot the best-solution path

- Keep only generations that improved the best-so-far solution.
- Plot those points on a wide view and a zoomed view near the origin.
- The path shows exploration first and fine adjustment later.""",

    50: r"""## 22. Plot population snapshots

- Display all 50 chromosomes at six stages of the run.
- Use the same landscape and limits so the panels are comparable.
- The sequence shows the population moving toward the central valley.""",

    52: r"""## 23. Compare early and later roulette wheels

- Recalculate selection probabilities for generation 0 and a later snapshot.
- Plot both wheels using the same display rule.
- This shows how selection changes as objective values become closer.""",

    53: r"""## 24. Compare fitness transformations

- Measure the largest roulette slice under windowing and inverse fitness.
- Print the ratio between the largest and smallest selection probabilities.
- The table shows how selection pressure changes during the run.""",

    56: r"""## 25. Test the two proposed fixes

- Run four combinations of mutation-step rule and duplicate limit.
- Use the same 40 seeds for a fair comparison.
- Report median error, worst error, correct-valley count, and diversity.

This cell runs 160 GA experiments, so it may take a little time.""",

    59: r"""## 26. Reliability over 40 random seeds

- Run the final GA with seeds 0 through 39.
- Count a run as precise when its final value is below $10^{-6}$.
- Summarize the best, median, worst, distance, and generation statistics.""",

    60: r"""## 27. Plot the reliability results

- The bar chart shows the final value from each seed on a log scale.
- The contour plot shows where all 40 final solutions finished.
- The dashed line marks the chosen success threshold, $10^{-6}$.""",

    63: r"""## 28. Ablation study

- Change one GA component at a time and run each version with 15 seeds.
- Compare median result, worst result, and success rate.
- This identifies which operators have the largest effect on this experiment.

This cell runs 150 GA experiments and may take a little time.""",

    66: r"""## 29. Same-budget random-search baseline

- Give random search the same 5,050-point budget as the main GA run.
- Use the same seed for a reproducible comparison.
- Compare the smallest random-search value with the GA result.""",

    68: r"""## 30. Correctness checks

- Confirm the objective, population shape, bounds, elitism, and duplicate limit.
- Check that roulette probabilities are positive and sum to one.
- Rerun the seeded GA to confirm that the result is reproducible.""",
}


CONCLUSION = r"""## Result

For seed 7, the GA returns a point extremely close to $(0,0)$ with an Ackley value near $10^{-12}$. All 40 tested seeds finish below the chosen success threshold of $10^{-6}$.

The experiment shows the separate roles of selection, crossover, mutation, adaptive step size, elitism, and diversity control."""


def markdown_cell(source: str, cell_id: str) -> dict:
    lines = source.strip().splitlines(keepends=True)
    if lines:
        lines[-1] = lines[-1].rstrip("\r\n")
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": lines,
    }


def main() -> None:
    BACKUP_DIR.mkdir(exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(NOTEBOOK, BACKUP)

    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code_cells = [(index, cell) for index, cell in enumerate(notebook["cells"])
                  if cell.get("cell_type") == "code"]

    missing = [index for index, _ in code_cells if index not in GUIDES]
    extra = sorted(set(GUIDES) - {index for index, _ in code_cells})
    if missing or extra:
        raise RuntimeError(f"Guide mapping mismatch. Missing={missing}, extra={extra}")

    new_cells = [markdown_cell(INTRO, "short-introduction")]
    for original_index, code_cell in code_cells:
        new_cells.append(markdown_cell(GUIDES[original_index], f"guide-{original_index:02d}"))
        new_cells.append(code_cell)
    new_cells.append(markdown_cell(CONCLUSION, "short-conclusion"))

    notebook["cells"] = new_cells
    NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )

    print(f"Saved {NOTEBOOK.name}: {len(new_cells)} cells, {len(code_cells)} code cells.")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
