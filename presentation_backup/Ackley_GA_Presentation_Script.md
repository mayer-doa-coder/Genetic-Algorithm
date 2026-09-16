# Presentation Script — Finding the Global Minimum of the 2-D Ackley Function with a Genetic Algorithm

**18 slides · target 15–17 minutes · figures are in `presentation_figures/`**

---

## How to use this document

For every slide you get four things:

| Block | Meaning |
|---|---|
| **ON THE SLIDE** | the text, bullets or table that should actually be printed on the slide |
| **FIGURE** | which image file to place, and where |
| **SAY** | the spoken script — say it in your own words, do not read it out |
| **TIME** | how long to stay on that slide |

Two rules that make the whole talk work:

1. **Never read the slide out loud.** The slide holds the short version; your voice holds the explanation.
2. **Keep the running story in mind:** *a hard landscape → a population of guesses → four operators that improve
   the guesses → two weaknesses we found and fixed → the answer, checked.*

Suggested speaker split for a 5-person group: slides 1–4, 5–8, 9–12, 13–15, 16–18.

---

## SLIDE 1 — Title

**ON THE SLIDE**
- Title: **Finding the Global Minimum of the 2-D Ackley Function using a Genetic Algorithm**
- Course: CSE 4111 — Machine Learning
- Submitted to: *Dr. Al-Mahmud, Professor, Dept of CSE, KUET*
- Submitted by: 2107001, 2107004, 2107009, 2107015, 2107024, 2107047
- Date: 14 September, 2026

**FIGURE** — optional: a small, faded copy of `01_ackley_landscape.png` as the title background.

**SAY**
> Good morning. Our assignment was to find the lowest point of the two-dimensional Ackley function using a
> Genetic Algorithm. In the next fifteen minutes we will show what the function is, why it is hard, how a
> Genetic Algorithm works, two problems we discovered in our first version, and our final result.

**TIME** — 30 seconds.

---

## SLIDE 2 — The Problem and the Objective

**ON THE SLIDE**
- **Goal:** find $x_1$ and $x_2$ that make $f(x_1,x_2)$ as small as possible.
- **Search range:** $-5 \le x_1 \le 5$, $-5 \le x_2 \le 5$
- **Known answer:** $x^\* = (0,0)$, $f(x^\*) = 0$
- Box in a different colour:
  **The algorithm is never told the answer. It only gets the range, and permission to evaluate $f$ at points it chooses.**

**FIGURE** — none. Keep this slide clean.

**SAY**
> Here is the task in one sentence. We have a mathematical surface with two inputs, and we must find the point
> where it is lowest. Both inputs are restricted to minus five through plus five.
>
> We already know the correct answer — the origin, where the function equals zero. But we only use that to
> check ourselves at the end. The algorithm never sees it. All it may do is pick a point, ask "what is the
> value here", and use the answer to decide where to look next.

**TIME** — 1 minute.

---

## SLIDE 3 — The Ackley Function

**ON THE SLIDE**
- **General form for $n$ dimensions:**
  $$f(\mathbf{x}) = -a\exp\!\left(-b\sqrt{\tfrac{1}{n}\textstyle\sum x_i^2}\right) - \exp\!\left(\tfrac{1}{n}\textstyle\sum \cos(cx_i)\right) + a + e$$
- Constants: $a = 20$, $b = 0.2$, $c = 2\pi$
- A three-step chain: set $n=2$ → open the two sums → substitute back
- **The 2-D version we minimise:**
  $$f(x_1,x_2) = -20\exp\!\left(-0.2\sqrt{\tfrac{x_1^2+x_2^2}{2}}\right) - \exp\!\left(\tfrac{\cos 2\pi x_1 + \cos 2\pi x_2}{2}\right) + 20 + e$$

**FIGURE** — none; the equations are the content.

**SAY**
> This is the Ackley function. The top formula is the general version for any number of variables. We set n
> equal to two, and the two summation signs open up into two terms each. The average of the squares becomes
> x-one squared plus x-two squared over two, and the average of the cosines becomes cosine two-pi-x-one plus
> cosine two-pi-x-two, over two.
>
> Substituting those back gives the bottom formula, which is what our code minimises.
>
> A quick check you can do in your head: at the origin the square-root term is zero, so the first part is minus
> twenty. Both cosines are one, so the second part is minus e. We then add twenty and e back, and everything
> cancels to exactly zero. That is why the minimum value is zero.

**TIME** — 1 minute 15 seconds.

---

## SLIDE 4 — Why This Function Is Hard

**ON THE SLIDE**
- Two-row table:
  | Part of the formula | Shape it creates |
  |---|---|
  | the exponential term | one wide smooth funnel pointing at the origin |
  | the cosine term | many small ripples spread over that funnel |
- Three short bullets:
  - **Multimodal** — one global minimum, surrounded by rings of local minima about one unit apart.
  - **Gradient descent** walks into the nearest ripple and stops there.
  - **Grid search** to 6 decimals would need about $10^{14}$ evaluations.

**FIGURE** — `01_ackley_landscape.png`, large. Optionally `02_ackley_slice.png` as a strip along the bottom.

**SAY**
> Why do we need a Genetic Algorithm at all? Look at the picture.
>
> The function is made of two parts that fight each other. The exponential part makes one big smooth funnel
> sloping down to the centre — that part is helpful. The cosine part lays a grid of small ripples over the
> whole funnel, and those ripples are the problem.
>
> Every one of those little dips is a local minimum. If you stand inside one, every direction you can step goes
> uphill. So a method like gradient descent, which only ever walks downhill, gets stuck in the first dip it
> falls into and confidently reports the wrong answer.
>
> We also cannot simply try every point. To get six decimal places by brute force over this square you would
> need about ten to the fourteen evaluations. So we need something smarter.

**TIME** — 1 minute 15 seconds.

---

## SLIDE 5 — Why a Genetic Algorithm

**ON THE SLIDE**
- Big quote at the top: **"Select the best, discard the rest."**
- One line: *A GA is a search and optimisation technique based on Darwin's principle of natural selection.*
- Nature-to-computer table:
  | Nature | Our program |
  |---|---|
  | Population | 50 candidate solutions |
  | Individual | one point in the plane |
  | Chromosome | `[x1, x2]` |
  | Gene | one coordinate |
  | Fitness | how small $f$ is |
  | Reproduction | crossover |
- Right-hand bullets: **no derivative needed · many points searched at once · mutation escapes ripples**

**FIGURE** — optional: a simple icon-style loop (population → evaluate → select → reproduce → population).

**SAY**
> A Genetic Algorithm copies the idea of natural selection. Instead of tracking one point, we keep a population
> of fifty candidate answers. We score them all, let the better ones have more children, mix and slightly
> disturb those children, and repeat. Over generations the population drifts towards the good regions, the same
> way a species adapts to its environment.
>
> This table is the translation between biology and our program. A population is a set of fifty candidate
> solutions. An individual is one point. A chromosome is the pair x-one, x-two. A gene is one coordinate.
>
> Three reasons this fits our problem: it needs no derivative, only the ability to evaluate the function; it
> keeps many points at once, so many ripples get explored in parallel; and mutation gives any individual a
> chance to jump out of a ripple.

**TIME** — 1 minute.

---

## SLIDE 6 — How We Represent a Solution

**ON THE SLIDE**
- **Value encoding** — the actual real numbers are stored, not binary strings.
- Big diagram:
  ```
        gene 1     gene 2
      +---------+---------+
      |   x1    |   x2    |
      +---------+---------+
  ```
- Examples: `[-4.0, 2.5]` and `[-1.5, -1.0]`
- Rule: every gene must stay inside $[-5, +5]$ at all times.
- Small note: *Binary encoding fixes the precision in advance — 20 bits over $[-5,5]$ can never go finer than about $10^{-5}$.*

**FIGURE** — none; the chromosome diagram is the visual.

**SAY**
> Our chromosome is simple. The problem has two variables, so each chromosome has exactly two genes: the first
> is x-one, the second is x-two. Here are two examples, taken straight from the assignment sheet.
>
> This is value encoding, and the assignment asks for it — but there is a good reason behind it too. With
> binary encoding we would have to decide the number of bits in advance, and that decision puts a ceiling on
> how accurate we can ever be. Twenty bits over this range can never express anything finer than about ten to
> the minus five. With real numbers there is no such ceiling, and you will see that our final answer has twelve
> correct decimal places.
>
> One rule holds for the whole run: every gene must stay between minus five and plus five.

**TIME** — 1 minute.

---

## SLIDE 7 — GA Settings

**ON THE SLIDE**
One clean table, with the assignment-given values visually separated from our own choices.

| Parameter | Value |
|---|---|
| Population size | 50 |
| Maximum generations | 100 |
| Crossover probability $P_c$ | 0.80 |
| Mutation probability $P_m$ | 0.05 per gene |
| Elitism | 1 |
| Encoding | real value, 2 genes |
| Selection | roulette wheel |
| Crossover | 1-point |
| Mutation | Gaussian, then clipped |
| *Mutation step $\sigma$* | *best value ÷ 4* |
| *Max copies of one chromosome* | *15 of 50* |
| *Convergence tolerance* | *$10^{-10}$, held for 20 generations* |
| *Random seed* | *7, for reproducibility* |

**FIGURE** — none.

**SAY**
> These are our settings. Everything above the line is fixed by the assignment: fifty chromosomes, at most a
> hundred generations, eighty percent crossover, five percent mutation per gene, and elitism of one.
>
> The four items in italics are our own decisions, because the assignment leaves them open. The first two —
> the mutation step and the copy limit — are the interesting ones, and we will come back to them on slide
> sixteen, because they are how we fixed two real problems.

**TIME** — 45 seconds.

---

## SLIDE 8 — The Algorithm, Step by Step

**ON THE SLIDE**
Vertical flow diagram on the left, ten steps as a numbered list on the right.

```
   Initialise 50 chromosomes
             |
   Evaluate f for all 50      <-----------+
             |                            |
   Sort, and remember the elite           |
             |                            |
     stop? --- yes ---> report best       |
             | no                         |
   sigma = best value / 4                 |
   Fitness -> roulette probabilities      |
   1-point crossover  (80%)               |
   Mutation per gene  (5%)                |
   Clip every gene into [-5, 5]           |
             |                            |
   Keep the best 50 of 100 candidates ----+
```

1 Initialise · 2 Evaluate · 3 Sort · 4 Keep the elite · 5 Select–Crossover–Mutate ·
6 Roulette probabilities · 7 Clip into range · 8 Re-evaluate · 9 Form next generation · 10 Repeat

**FIGURE** — draw with PowerPoint shapes so you can animate it one box at a time.

**SAY**
> This is the whole algorithm on one slide. We scatter fifty random chromosomes across the square, evaluate the
> Ackley value of each, sort them, and remember the best one — our elite.
>
> If a stopping condition is met we report the best and finish. Otherwise we go around the loop: set the
> mutation step size, convert the values into selection probabilities, spin a roulette wheel to choose parents,
> apply one-point crossover, apply mutation gene by gene, and clip anything that has fallen out of range.
>
> That gives fifty children. We then have a hundred candidates in total — fifty parents and fifty children —
> and we keep the best fifty as the next generation. Then we go around again.
>
> The next four slides look at the operators in this loop one at a time.

**TIME** — 1 minute 15 seconds.

---

## SLIDE 9 — Selection: Fitness and the Roulette Wheel

**ON THE SLIDE**
- One line: **objective value — lower is better. Fitness — higher must be better. So we flip it.**
- The transform: $F_i = (f_{\max} - f_i) + \delta$, then $p_i = F_i / \sum_j F_j$
- Two bullets:
  - the best chromosome gets the widest slice,
  - the worst keeps a thin non-zero slice, so diversity survives.
- Small worked table:
  | # | $f$ | % of the wheel | expected picks in 50 spins |
  |---|---|---|---|
  | 7 | 3.19 | 4.83 % | 2.41 |
  | 46 | 3.79 | 4.57 % | 2.28 |
  | 14 | 4.87 | 4.10 % | 2.05 |
  | 45 (worst) | 13.39 | 0.44 % | 0.22 |

**FIGURE** — `04_roulette_pie_gen0.png` on the right half. **This is the pie chart the assignment asks for.**

**SAY**
> Selection decides who becomes a parent, and there is one trap here that is easy to get wrong.
>
> Ours is a minimisation problem, so a *small* Ackley value is good. But roulette-wheel selection hands out
> probability in proportion to fitness, and assumes a *large* fitness is good. So we must flip the direction
> first. We take the worst value in the population and subtract each chromosome's value from it. The best
> chromosome then gets the biggest number and the worst gets nearly zero. We add a small offset so the worst
> still keeps a thin slice — we do not want to throw away diversity completely.
>
> Dividing by the total gives fifty probabilities that add up to one, and that is exactly what this pie chart
> shows for our real first generation.
>
> Look at the table. Chromosome seven is the best in that generation, value about three point two, and it owns
> almost five percent of the wheel — so in fifty spins we expect it to be chosen about two and a half times.
> The worst chromosome owns less than half a percent. Unlikely to be picked, but not impossible, and that small
> chance is deliberate.

**TIME** — 1 minute 30 seconds.

---

## SLIDE 10 — Crossover: One-Point, 80 %

**ON THE SLIDE**
- Large diagram:
  ```
   Parent 1 :  [ a | b ]              Child 1 : [ a | d ]
   Parent 2 :  [ c | d ]     ==>      Child 2 : [ c | b ]
                   ^ the only possible cut
  ```
- Real example from our code:
  `[-4.0, 2.5] + [-1.5, -1.0]` → `[-4.0, -1.0]` and `[-1.5, 2.5]`
- Two bullets:
  - With 2 genes there is exactly **one legal cut** — between $x_1$ and $x_2$.
  - Crossover **cannot invent a new number**; it only re-pairs coordinates the population already has.
- With probability 20 % no cut happens and the children are copies of the parents.

**FIGURE** — none; animate the swap if you can.

**SAY**
> Crossover is the mixing step. We take two parents, cut at one point, and swap the tails.
>
> Our chromosome has only two genes, so there is only one place the cut can go: between x-one and x-two. That
> means one-point crossover here has a very simple meaning — take the x-one of one parent and the x-two of the
> other.
>
> Here is a real example from our code. Minus four, two point five, combined with minus one point five, minus
> one, gives minus four, minus one, and minus one point five, two point five.
>
> Notice what did *not* happen: no new number was created. The four coordinates are the same four coordinates,
> paired differently. That is exactly crossover's job — if one parent has found a good x-one and another has
> found a good x-two, crossover puts them into a single child in one step.
>
> And with twenty percent probability we make no cut at all, and the children are simply copies.

**TIME** — 1 minute 15 seconds.

---

## SLIDE 11 — Mutation: 5 % per Gene

**ON THE SLIDE**
- **We walk along the chromosome gene by gene.** For each gene draw a random number; if it is below 0.05,
  change that gene.
- Gaussian mutation: $x_i \leftarrow x_i + \mathcal{N}(0,\sigma^2)$, then **clip back into $[-5,+5]$**
- Example from the assignment sheet: `[-1.5, -1.0]` → `[-0.5, -1.0]`
- One line: *Mutation is the only operator that can create a value the population has never held.*
- Teaser box: **How big should the step $\sigma$ be? → next slide.**

**FIGURE** — none.

**SAY**
> Mutation is the only operator that can create a number the population has never had. We go along the
> chromosome one gene at a time, and for each gene we roll a dice. If it comes below five percent we change
> that gene by adding a small random amount from a normal distribution. Then we immediately clip it, so it can
> never leave the range minus five to plus five.
>
> The mutation probability is fixed at five percent by the assignment. But the *size* of the change — the
> standard deviation sigma — is ours to choose, and it turned out to be the single most important decision in
> the whole implementation. So it gets its own slide.

**TIME** — 1 minute.

---

## SLIDE 12 — Choosing the Mutation Step Size

**ON THE SLIDE**
- **The obvious approach:** shrink $\sigma$ on a timetable, 1.0 at generation 0 down to $10^{-8}$ at generation 100.
  Big steps early to explore, small steps late to polish.
- **The flaw, in red:** the step shrinks *whether or not the search is making progress*. A run still stuck in
  the wrong ripple at generation 40 already has $\sigma \approx 10^{-3}$ — far too small to escape.
- **Our rule:** $\boxed{\sigma = f_{\text{best}} \,/\, 4}$
- Why divide by 4: near the origin $f \approx 4s$, so $f/4$ **is the distance still to be covered**.
- Small table:
  | Situation | $f_{\text{best}}$ | $\sigma$ |
  |---|---:|---:|
  | random start | 5 | 1.2 |
  | stuck in a ripple | 2.6 | **0.65 — still big enough to jump out** |
  | inside the central dip | $10^{-3}$ | $10^{-4}$ |
  | nearly solved | $10^{-9}$ | $10^{-10}$ |

**FIGURE** — none, or the right-hand panel of `05_convergence_and_diversity.png`.

**SAY**
> Our first version did the obvious thing: shrink the mutation step on a timetable. Start at one, shrink
> smoothly to ten to the minus eight by generation one hundred. Big steps early to explore, tiny steps late to
> polish. It worked — we got about ten to the minus nine.
>
> But it has a flaw that only shows up when you run it many times. The step shrinks whether or not the search
> is actually making progress. If a run is still stuck in the wrong ripple at generation forty, sigma has
> already fallen to about a thousandth — far too small to jump the one-unit gap it needs. That run is locked in
> for the rest of its life.
>
> So instead of asking "how late is it?", we ask "how far away are we still?". We set sigma to the current best
> value divided by four.
>
> Why divide by four? Near the origin the Ackley function is almost a straight cone, and if you expand both
> exponentials you find f is approximately four times the distance. So dividing the best value by four gives
> you, near the optimum, the distance that still has to be covered. The mutation step is always about the size
> of the remaining gap.
>
> Look at the table — that is the whole point. A run stuck at two point six keeps a step of zero point six five
> and keeps trying to escape. A run that is nearly finished automatically slows down and polishes. The rule is
> self-correcting.

**TIME** — 1 minute 45 seconds.

---

## SLIDE 13 — Elitism, Survivors, and Keeping the Population Diverse

**ON THE SLIDE**
- **Elitism = 1** — the single best chromosome is copied into the next generation untouched.
  → in a box: **the best-so-far value can never get worse.**
- **Forming the next generation:**
  ```
   50 parents  +  50 children  =  100 candidates
                    |
             sort by Ackley value
                    |
             keep the best 50
  ```
- **One extra rule, in a second colour:**
  **no chromosome may occupy more than 15 of the 50 seats.**
  Without it, by generation 11 all 50 chromosomes were *literally the same point*.

**FIGURE** — none. Animate the 100 → 50 arrow.

**SAY**
> Crossover and mutation are random, so the best chromosome can easily be destroyed by bad luck. Elitism
> prevents that: we copy the single best chromosome straight into the next generation untouched. The result is
> that our best-so-far curve can go down or stay flat, but never up.
>
> Then we build the next generation. At that moment we have a hundred candidates — fifty parents and fifty
> children. We sort all hundred and keep the best fifty. That keeps the population size constant and guarantees
> a generation is never worse than the one before.
>
> But here is the second problem we found. Truncating a hundred down to fifty is very strong pressure, and with
> only five percent mutation most children are exact copies of their parents. So the copies took over: by
> generation eleven, all fifty chromosomes were literally the same point. We had a population of one, and a
> population of clones cannot explore its way out of anything.
>
> The fix is one rule: no single chromosome may hold more than fifteen of the fifty seats. When a candidate
> would exceed its quota, the seat goes to the next different candidate instead.

**TIME** — 1 minute 30 seconds.

---

## SLIDE 14 — When Do We Stop?

**ON THE SLIDE**
- We stop when **either** happens:
  1. **100 generations** are complete, **or**
  2. the improvement between two generations stays below **$10^{-10}$**.
- Small box: *The assignment gives no number, so we chose the tolerance ourselves.*
- Key point: **One flat generation is completely normal** — mutation simply found nothing that round.
  So we require the improvement to stay small for **20 generations in a row**.

**FIGURE** — none.

**SAY**
> We stop for one of two reasons: a hundred generations are complete, or the algorithm has stopped improving.
>
> The assignment does not say how small "stopped improving" should be, so we chose ten to the minus ten.
>
> One practical detail. In a Genetic Algorithm it is completely normal for a generation to produce no
> improvement — mutation just did not get lucky that round. If we stopped at the first flat generation we would
> end far too early. So we require the improvement to stay below the tolerance for twenty generations in a row.

**TIME** — 45 seconds.

---

## SLIDE 15 — Results

**ON THE SLIDE**
Two columns side by side.

| Theoretical optimum | Our GA result (seed 7) |
|---|---|
| $x_1^\* = 0$ | $x_1 = -3.44 \times 10^{-13}$ |
| $x_2^\* = 0$ | $x_2 = -1.73 \times 10^{-13}$ |
| $f(x^\*) = 0$ | $f = 1.09 \times 10^{-12}$ |

Underneath:
- **12 correct decimal places** in each coordinate, **11** in the function value
- Distance to $(0,0)$: $3.85\times10^{-13}$ · **5050** function evaluations
- *Visually* converged by generation 20 ($f \approx 6\times10^{-3}$); the remaining 80 generations add the decimals

Small box: **Random search with the same 5050 evaluations reached only $f = 0.77$ — the GA is about $7\times10^{11}$ times more accurate.**

**FIGURE** — `06_best_solution_path.png` at the bottom or to one side.

**SAY**
> These are our results. The true optimum is zero, zero, with value zero. Our algorithm returned minus three
> point four times ten to the minus thirteen and minus one point seven times ten to the minus thirteen, with a
> function value of about one times ten to the minus twelve. That is twelve correct decimal places in each
> coordinate.
>
> It is not exactly zero, and it is not supposed to be. A Genetic Algorithm is a random search method — it
> samples the space, it does not solve an equation. The standard is whether the remaining error is negligible,
> and at ten to the minus twelve it clearly is.
>
> Two numbers worth pointing out. First, the answer is visually found by about generation twenty; everything
> after that is adding decimal places, which matters because the assignment asks us to report precision.
> Second, the cost: about five thousand function evaluations. We gave pure random search exactly the same five
> thousand evaluations, and it only reached zero point seven seven. So the Genetic Algorithm is roughly seven
> hundred billion times more accurate for the same amount of work.

**TIME** — 1 minute 30 seconds.

---

## SLIDE 16 — Two Weaknesses We Found, and How We Fixed Them

**ON THE SLIDE**
Headline: **Our first version worked. Running it 40 times showed it was not reliable.**

The 2 × 2 comparison, 40 seeds each:

| mutation step | duplicates | median $f$ | worst $f$ | correct valley | distinct chromosomes |
|---|---|---|---|---|---|
| clock timetable | no cap | $5.5\times10^{-9}$ | **2.58** | 98 % | **3** |
| clock timetable | cap 15 | $6.8\times10^{-9}$ | **2.58** | 98 % | 9 |
| $f_{\text{best}}/4$ | no cap | $5.0\times10^{-13}$ | $2.3\times10^{-11}$ | 100 % | 8 |
| **$f_{\text{best}}/4$** | **cap 15** | $1.6\times10^{-12}$ | $3.1\times10^{-11}$ | **100 %** | **13** |

Two takeaway lines:
- **The copy limit fixes diversity** — but it does not rescue a trapped run.
- **The adaptive step fixes the trapping *and* the precision** — three orders of magnitude better.

**FIGURE** — none; the table is the slide. Highlight the "2.58" cells in red.

**SAY**
> This is the slide we are most pleased with, because it is about something that went wrong.
>
> Our first version used the two obvious choices: the clock-based mutation timetable, and plain truncation of a
> hundred candidates down to fifty. It reached ten to the minus nine and looked fine. Then we ran it forty
> times, and two problems appeared.
>
> First, the population became clones — by generation eleven all fifty chromosomes were the same point.
> Second, one run in forty ended trapped at two point five eight, sitting on the first ring of local minima,
> because the mutation step had shrunk below the distance it needed to escape.
>
> This table switches each fix on and off independently, so you can see what each one is actually responsible
> for. Read down the last column: the copy limit is what lifts diversity, from three distinct chromosomes up to
> nine or thirteen. But look at the "worst" column in those top two rows — the copy limit does *not* rescue the
> trapped run. Two point five eight is still there.
>
> Now read the bottom two rows. The adaptive step size removes the trapped run completely — every run ends in
> the correct valley — and at the same time improves the accuracy by about three orders of magnitude, because
> the step size no longer runs out before the search does.
>
> So the two fixes solve two different problems, and we needed both.

**TIME** — 2 minutes.

---

## SLIDE 17 — Is One Good Run Just Luck?

**ON THE SLIDE**
- Headline: **40 independent runs, 40 different random seeds, nothing else changed.**
- Results:
  | | |
  |---|---|
  | median $f$ | $1.6 \times 10^{-12}$ |
  | best $f$ | $1.1 \times 10^{-13}$ |
  | worst $f$ | $3.1 \times 10^{-11}$ |
  | reached the global optimum | **40 / 40 (100 %)** |
- One line: *A randomised algorithm should always be reported as a median over many runs, not as one lucky run.*

**FIGURE** — `09_reliability_40_runs.png`, full width.

**SAY**
> One good run proves nothing about a random algorithm, so we ran the whole thing forty times with forty
> different seeds and changed nothing else.
>
> All forty reached the global minimum, and look at the scale on the left — every single bar is between ten to
> the minus thirteen and ten to the minus eleven, far below our success threshold. The spread is narrow, which
> means the result is repeatable, not lucky.
>
> On the right, all forty final points are stacked inside the star at the origin. Before our two fixes, one of
> those points would have been sitting out on a ring, about one unit away.
>
> And this is the honest way to report a randomised algorithm: not one impressive run, but a median over many.

**TIME** — 1 minute 15 seconds.

---

## SLIDE 18 — Conclusion

**ON THE SLIDE**
- **Result:** $x_1, x_2 \approx 0$ to 12 decimals, $f \approx 1.1\times10^{-12}$, ~5000 evaluations, 40 / 40 runs successful.
- What each part did, one line each:
  - value encoding → no ceiling on precision
  - roulette wheel → better chromosomes get more children
  - one-point crossover → combines a good $x_1$ with a good $x_2$
  - Gaussian mutation → the only source of new values
  - $\sigma = f_{\text{best}}/4$ → steps always match the distance left
  - elitism + copy limit → never lose the best, never become clones
- Closing line: **A GA needs no derivative and no formula — only the ability to compare two candidates.**
- **Thank you · Questions?**

**FIGURE** — optional: a small copy of `07_population_snapshots.png`.

**SAY**
> To conclude. We minimised the two-dimensional Ackley function with the settings the assignment specified,
> reaching about ten to the minus twelve in roughly five thousand function evaluations, and all forty
> independent runs succeeded.
>
> Each part had a distinct job: value encoding removed the ceiling on precision, the roulette wheel gave better
> chromosomes more children, crossover combined good coordinates, mutation created new ones, the adaptive step
> size kept the search moving at the right scale, and elitism plus the copy limit kept the population both safe
> and diverse.
>
> Two general points to take away. First, at no stage did the algorithm need a derivative or any knowledge of
> the shape of the function — it only needed to compare two candidates, which is why the same method transfers
> to problems where no formula exists at all. Second, a version that *works* is not the same as a version that
> works *reliably*; both of our weaknesses were invisible in a single run and obvious after forty.
>
> Thank you. We are happy to take questions.

**TIME** — 1 minute 15 seconds.

---

# Questions You Should Be Ready For

| Likely question | Short answer |
|---|---|
| **Why is your answer not exactly zero?** | A GA samples the space, it does not solve an equation. Our error is $10^{-12}$, far below any practical tolerance. Exact zero would mean solving the function analytically, which defeats the purpose. |
| **Why does $\sigma$ depend on the objective value? Is that still a valid GA?** | Yes. The mutation *probability* stays fixed at the required 5 %; only the size of a change adapts, which is standard practice in real-valued GAs. Slide 16 shows the clock-based alternative is three orders of magnitude worse and leaves runs trapped. |
| **Isn't $f_{\text{best}}/4$ using knowledge of the answer?** | No. It uses only the *current best value*, which the algorithm computes anyway. The factor $1/4$ comes from the local slope of the function, not from knowing where the optimum is. |
| **Why one-point crossover if there is only one cut position?** | Because the assignment specifies it, and with two genes that single cut *is* the operator — it swaps $x_2$ between the parents. Our code is written for a general chromosome length, so it works unchanged in higher dimensions. |
| **Why convert $f$ into fitness instead of using $f$ directly?** | The roulette wheel gives probability in proportion to fitness and assumes higher is better. Ours is a minimisation, so feeding $f$ in directly would give the *worst* chromosomes the biggest slices. |
| **Why cap copies at 15 and not some other number?** | We tested several values. Anything in the 10–25 range keeps diversity roughly ten times higher than no cap, with no measurable cost in accuracy. 15 sits in the middle of that flat region. |
| **What is the time complexity?** | Each generation is 50 evaluations plus a sort of 100 items, so $O(G \cdot N \log N)$. The whole run takes well under a second. |
| **Would this work for higher-dimensional Ackley?** | Yes — all our code is written for a general number of genes. It would need more generations or a larger population, because the search space grows exponentially with dimension. |
| **Why 20 generations of patience and not 1?** | Because a single generation with no improvement is normal in a GA. Stopping on the first one would cut almost every run short. |

---

# Practical Notes for Building the Deck

1. **Figures** are exported in `presentation_figures/`. Insert them at native size — they are high resolution
   and will not blur on a projector.
2. **Do not put full sentences on slides.** Everything in the *SAY* blocks belongs in speaker notes, not on
   screen.
3. **Animate slides 8, 10 and 13.** The flow diagram, the crossover swap, and the 100 → 50 arrow are much
   clearer appearing one piece at a time.
4. **Figure 04 (the pie chart) is explicitly required by the assignment.** Do not drop it if you run short of
   time — shorten slide 3 instead.
5. **Rehearse slides 12 and 16.** They carry the two ideas that make this submission different from a
   textbook implementation, and they are the most likely to be questioned.
6. **Timing check:** the times above total roughly 20 minutes without pauses. For a strict 15-minute slot,
   merge slides 13 and 14, and cut slide 3's derivation down to just the final 2-D formula.
