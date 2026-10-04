# Review folder

What is here, and what was checked.

- `slides/` — the final 1920 × 1080 PowerPoint slide exports, one PNG per slide.
- `contact_sheet_*.jpg` — a visual overview of all 19 slides.
- `layout_check.json` — PowerPoint's own measurement of every text box and table cell against
  the shape it sits in. The final deck reports **0 text-overflow warnings**.
- `results.json` — every number quoted on the slides and in the README, reproduced from
  scratch by `experiments.py`.
- `experiments.py` — the 40-seed studies: the ablation, the reliability run, the same-budget
  random-search baseline, and the head-to-head against the Genetic Algorithm notebook in the
  parent folder.
- `assets/` — the equation images rendered for the slides.

## What was verified

- The notebook executes top to bottom with **0 errors** and its outputs are stored in the file.
- The notebook's assertions pass: `f(0,0) = 0`; the colony stays 25 × 2 and inside `[-5, +5]`;
  every stored value matches `f` of its stored source; the memorised best never gets worse; no
  trial counter passes the `limit`; the onlooker probabilities are all positive and sum to 1;
  and the seeded run reproduces exactly.
- The main-run numbers on the slides match the notebook output and `results.json`.
- Slides 6 and 8 have click reveals (18 and 12 animation steps). The PNG and PDF exports show
  the completed state.

## Corrections made while building

These were caught by measuring rather than assuming, and the slides were changed to match:

- The cycle-0 wheel shares were first written as 4.95 % / 2.27 %; the measured values are
  **9.56 % / 3.03 %**, ratio 3.16.
- The onlooker wheel was first said to go uniform at cycle 49; measured, it is **cycle 62**.
- An early draft claimed the scaled probability variant "gives the good sources their lead
  back". The 40-seed test showed no meaningful difference (5.5 vs 6.0 × 10⁻¹³), so that claim
  was removed and the honest result reported instead.
- The default probability rule was switched to the plain slide-25 formula, because it measured
  at least as well as the variants and is what the course notes actually teach.
- "The trial counter never reaches the limit" was sharpened to the measured peak of **23**.

---

## Second audit (re-check of the whole folder)

A fresh pass over the code, the notebook and every figure. Six real problems were found
and fixed; the algorithm's behaviour did not change (seed 7 still returns
`6.54143406109142e-13`, bit for bit).

### Bugs found and fixed

1. **The evaluation count was wrong.** `run_abc` reported 5,125 Ackley evaluations by assuming
   a scout flew every cycle. No scout ever flew, so the true number of calls was **5,025**. The
   counter now counts the calls that actually happen, and reports the worst case separately as
   `evaluation_budget`. Verified by wrapping `ackley` in a call counter: reported == actual on
   four different runs, including ones where scouts do fire.
   *All slides, the README, the notes and the script were updated from 5,125 to 5,025.*

2. **Figure 05 made a claim its own data contradicted.** The right-hand pie was drawn at
   cycle 50 under the caption "every slice is now 1/25 = 4.00 %". At cycle 50 the slices
   actually run from 2.05 % to 4.08 % (ratio 1.99) — not uniform. The wheel only flattens
   completely at cycle 62. The panel now uses **cycle 100**, where every slice really is
   4.00 % and the ratio really is 1.00.

3. **`keep_best` was a dead parameter.** It was declared in `ABCSettings` and never read, which
   implied the best-solution memory could be switched off. It cannot. Removed.

4. **A notebook assertion stated an invariant that is not guaranteed.**
   `assert np.all(trials <= limit)` passed for seed 7, but only one scout flies per cycle, so if
   two sources pass the limit at once the second has to wait. Reproduced with `limit=2`: the
   counter reached 6. The assertion now checks a bound that genuinely holds, and the printed
   summary reports the *measured* peak (23) instead of claiming the limit was never passed.

5. **A tiny colony crashed with a cryptic error.** `colony_size=2` gives one food source, and
   the neighbourhood equation then has no partner `k != i` to choose; NumPy raised
   `ValueError: high <= 0`. It now raises a clear message explaining why at least two sources
   are needed.

6. **Figure 13's x-axis used the budget, not the actual cost**, so the ABC curve ran to 5,125
   while the random-search curve stopped at 5,025. Both now use real evaluation counts.

Also removed an unused `asdict` import.

### Checks that passed

- **The notebook and `build/abc_core.py` are two independent copies of the algorithm.** They
  were run head to head on seeds 0–24: identical best value, best solution, best cycle and
  cycles run on every seed, and the complete per-cycle history for seed 7 matches element for
  element.
- **The Ackley implementation is exact.** Compared against a hand-written, pure-`math`
  transcription of the assignment formula at 11 points: maximum difference `0.0e+00`. The
  vectorised and scalar paths agree to `0.0e+00` over 500 random points, a 2001×2001 grid search
  puts the minimum at exactly `(0, 0)`, and `f(0,0)` evaluates to `4.441e-16` — floating-point
  zero, from the `−20 − e + 20 + e` cancellation. Our result of `6.5e-13` sits about 1,200×
  above that numerical floor, so it is a real result and not rounding noise.
- **Invariants over 12 seeds:** every coordinate stayed inside `[-5, +5]`, every stored value
  matched `f` of its stored source, all values finite, and the memorised best never increased.
- **All 13 figure-embedded claims** were recomputed from fresh runs and matched, except the
  cycle-50 caption listed above.
- **All 17 documented numbers** (slides, README, notes) were re-checked against a regenerated
  `results.json`: 0 mismatches.
- The deck re-renders with **0 text-overflow warnings**, 19 slides, 19 PDF pages, and the
  notebook re-executes with **0 errors**.
