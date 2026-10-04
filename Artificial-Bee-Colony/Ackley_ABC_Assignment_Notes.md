# Assignment: Find the Global Minimum of the 2D Ackley Function Using the Artificial Bee Colony (ABC) Algorithm

This is the same assignment as the Genetic Algorithm version — same function, same search
range, same target, same budget, same accuracy report. **Only the search method changes.**
Everything below follows the course slides *"7. ABC Edited"*.

---

## 1. Objective

Find the **global minimum of the 2D Ackley function** using the **Artificial Bee Colony (ABC)** algorithm.

---

## 2. Ackley Function for \(n\) Dimensions

For

\[
\mathbf{x} = (x_1,x_2,\ldots,x_n),
\]

the Ackley function is

\[
f(x_1,\ldots,x_n)
= -a\exp\!\left(-b\sqrt{\tfrac{1}{n}\textstyle\sum_{i=1}^{n}x_i^2}\right)
  -\exp\!\left(\tfrac{1}{n}\textstyle\sum_{i=1}^{n}\cos(cx_i)\right)
  + a + e .
\]

### Recommended Parameters

\[
a=20,\qquad b=0.2,\qquad c=2\pi .
\]

---

## 3. Ackley Function for 2D

\[
f(x_1,x_2)
= -20\exp\!\left(-0.2\sqrt{\tfrac{x_1^2+x_2^2}{2}}\right)
  -\exp\!\left(\tfrac{\cos(2\pi x_1)+\cos(2\pi x_2)}{2}\right)
  + 20 + e ,
\qquad e \approx 2.71828 .
\]

### Search Range

\[
-5 \le x_1 \le 5, \qquad -5 \le x_2 \le 5 .
\]

### Known Global Minimum

\[
\boxed{x^*=(0,0), \qquad f(0,0)=0 }
\]

The algorithm is **not** told where the optimum is. It only evaluates \(f\) at points it chooses.
The known optimum is used **afterwards**, to measure precision.

---

## 4. ABC Settings

The assignment fixes a budget of 50 candidates and 100 rounds. In ABC the colony is split in
half (slide 20: *employed bees 50% of swarm, onlookers 50% of swarm*), so 50 bees means
**25 food sources**.

| Parameter | Value | Where it comes from |
|---|---:|---|
| Colony size (total bees) | 50 | the assignment's "population 50" |
| Employed bees = food sources, \(SN\) | 25 | 50% of the colony (slide 20) |
| Onlooker bees | 25 | 50% of the colony (slide 20) |
| Dimension, \(D\) | 2 | the problem is 2-D |
| Maximum cycles | 100 | the assignment's "100 generations" |
| `limit` (abandonment counter) | 50 | the usual choice \(SN \times D = 25\times 2\) |
| Scouts per cycle | at most 1 | slide 20: "1 or can be more than 1" |
| Tolerance / patience | \(10^{-10}\) / 20 cycles | our choice, second stopping rule |
| Random seed (main run) | 7 | so the result can be repeated |

### How the GA settings map onto ABC

| Genetic Algorithm | Artificial Bee Colony | Note |
|---|---|---|
| Population 50 | Colony 50 bees = 25 sources + 25 onlookers | same number of bees |
| 100 generations | 100 cycles | same |
| Crossover \(P_c = 80\%\) | — | ABC has no crossover |
| Mutation \(P_m = 5\%\) | — | ABC has no mutation probability |
| (the mutation step \(\sigma\)) | \(\varphi_{ij}(x_{ij}-x_{kj})\) | the step size comes from the swarm itself |
| Elitism = 1 | "Memorize the best solution" (slide 18, step 3d) | same effect |
| Roulette-wheel selection | Onlooker phase (slide 25) | **the same wheel** |
| — | `limit` + scout phase | ABC's own restart mechanism |

**ABC has fewer knobs than GA.** There is no crossover rate and no mutation rate to tune.
That is one of its advertised advantages (slide 31: *"few control parameters"*).

---

## 5. Solution Representation

A **food source** is one candidate solution, stored as two real numbers — the same value
encoding the GA used:

\[
\text{food source } i = [\,x_{i1},\, x_{i2}\,], \qquad -5 \le x_{ij} \le 5 .
\]

Example food sources: \([-4.0,\;2.5]\) and \([-1.5,\;-1.0]\).

The **nectar amount** of a source is its fitness. Because this is a minimisation problem and
roulette selection needs "bigger is better", the standard ABC fitness is used:

\[
fit_i = \begin{cases} \dfrac{1}{1+f_i} & f_i \ge 0 \\[2mm] 1+|f_i| & f_i < 0 \end{cases}
\]

Ackley is never negative, so only the first line is ever used here.

---

## 6. The Three Kinds of Bee (slides 3, 4)

| Bee | What it does in nature | What it does in the program | Purpose |
|---|---|---|---|
| **Employed** | stays on one food source, remembers it | each of the 25 bees tries one point near its own source | exploitation |
| **Onlooker** | watches the waggle dance, picks a patch | 25 visits handed out by roulette wheel, then the same nearby search | guided search |
| **Scout** | looks for brand-new flowers | a source that failed `limit` times is thrown away and replaced at random | exploration |

---

## 7. The Equations (slides 21, 23, 25, 30)

### 7.1 Initialisation — and scouting

\[
x_{ij} = x_{\min,j} + \mathrm{rand}(0,1)\,(x_{\max,j}-x_{\min,j})
\]

with \(i = 1,2,\ldots,SN\) and \(j = 1,\ldots,D\). The **scout phase uses this same equation**
to replace an abandoned source.

### 7.2 Neighbourhood search (employed and onlooker phases)

\[
v_{ij} = x_{ij} + \varphi_{ij}\,(x_{ij} - x_{kj})
\]

where

* \(\varphi_{ij} = \mathrm{rand}(-1,1)\),
* \(k = \mathrm{rand}(1,SN)\) with \(k \ne i\),
* \(j\) is **one randomly chosen coordinate**; the other coordinate is copied unchanged.

Then **greedy selection**: keep \(v_i\) if \(f(v_i) < f(x_i)\), otherwise keep \(x_i\) and add one
to that source's trial counter.

Note what this equation does for free: the step size is \(|x_{ij}-x_{kj}|\), the distance to
another bee. As the colony gathers around the optimum, that distance shrinks, so the steps
shrink too. **ABC does not need a mutation-step schedule** — the GA version had to add one.

### 7.3 Onlooker probability

\[
P_i = \frac{fit_i}{\sum_{m=1}^{SN} fit_m}
\]

Onlookers are then assigned to sources with a **roulette wheel** (slide 25).

### 7.4 Abandonment

If a source's trial counter exceeds `limit`, it is abandoned and a scout replaces it using the
initialisation equation.

After every operation each coordinate is clipped back into \([-5,+5]\).

---

## 8. Correct ABC Sequence (slide 18)

**Step 1 — Assign control parameters.** Colony 50, \(SN = 25\), \(D = 2\), `limit` 50, 100 cycles.

**Step 2 — Initialise solutions.** Create 25 random food sources, evaluate them, set every
trial counter to 0, and remember the best one.

**Step 3 — Repeat until the stopping rule fires:**

  1. **Employed bee phase.** For each of the 25 sources: build \(v_i\), evaluate it,
     greedy-select, update the trial counter.
  2. **Onlooker bee phase.** Compute \(P_i\) for all 25 sources, spin the roulette wheel 25
     times, and repeat the same neighbourhood search and greedy selection on each chosen source.
  3. **Memorise the best solution** found so far. (This is ABC's elitism.)
  4. **Scout bee phase.** If a trial counter is above `limit`, replace that source at random.

**Step 4 — Stop** and report the memorised best solution.

> The order matters: the best solution is memorised **before** the scout runs, so a scout can
> never throw away the best answer found so far.

---

## 9. Stopping Criteria

Stop when either:

1. **100 cycles** have been completed, or
2. the improvement of the best value stays below the tolerance \(10^{-10}\) for **20 cycles in a row**.

---

## 10. Expected Final Result

Report:

* best \(x_1\), best \(x_2\)
* best Ackley value \(f(x_1,x_2)\)
* the cycle at which the best solution was found
* the error against the true optimum: \(|x_1-0|\), \(|x_2-0|\), the distance to \((0,0)\), and \(|f-0|\)
* the number of Ackley evaluations used

The expected answer is \(x_1 \approx 0\), \(x_2 \approx 0\), \(f \approx 0\).

### What we actually obtained (seed 7)

| Quantity | Value |
|---|---|
| Best \(x_1\) | \(+2.278\times10^{-13}\) |
| Best \(x_2\) | \(-3.938\times10^{-14}\) |
| Best \(f(x_1,x_2)\) | \(6.541\times10^{-13}\) |
| Distance to \((0,0)\) | \(2.312\times10^{-13}\) |
| Found at | cycle 99 of 100 |
| Ackley evaluations (actual) | 5,025 |
| Worst-case budget | 5,125 |
| Scouts needed | 0 |

Across seeds 0–39: **40 / 40 runs** finished below \(10^{-6}\); median \(5.476\times10^{-13}\),
worst \(1.034\times10^{-11}\).

All of these numbers are reproduced by `review/experiments.py`.
