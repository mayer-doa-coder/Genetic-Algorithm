# Easy Presentation Script — Ackley Function with a Genetic Algorithm

**18 slides · planned speaking time 16 min 15 sec · presentation date 14 September 2026**

The short text belongs on the slides. The SAY paragraphs are also in the PowerPoint speaker notes. Speak naturally and point to the diagrams. Allow about 17–19 minutes including pauses and speaker changes.

**Six-speaker option:** IDs 2107001: slides 1–3; 2107004: 4–6; 2107009: 7–9; 2107015: 10–12; 2107024: 13–15; 2107047: 16–18. Adjust within the group if needed.

**Pronunciation:** GA = “G A”; Ackley = “ACK-lee”; sigma = “SIG-ma”; 10⁻¹² = “ten to the minus twelve”; elitism = “keep the best”; convergence = “the result settles down”.

---

## Slide 1 — Finding the global minimum

**ON THE SLIDE**

- 2-D Ackley function using a Genetic Algorithm
- Submitted to: Dr. Al-Mahmud, Professor, Dept. of CSE, KUET
- Submitted by: 2107001, 2107004, 2107009, 2107015, 2107024, 2107047

**FIGURE / DELIVERY:** Original template DNA illustration.

**SAY**

> Good morning, sir. Our project is about finding the lowest point of the two-dimensional Ackley function using a Genetic Algorithm. We will explain the problem, show how our algorithm works, and discuss the results. We will also show two changes that improved our first version.

**TIME:** 30 seconds.

---

## Slide 2 — Find the lowest point

**ON THE SLIDE**

- Goal: choose x₁ and x₂ to make f as small as possible.
- Range: −5 ≤ x₁, x₂ ≤ 5
- Known minimum: (0, 0), with f = 0
- The search is not given the location (0, 0).

**FIGURE / DELIVERY:** Native coordinate diagram: allowed square and known optimum.

**SAY**

> We need to find two numbers, x-one and x-two, that give the smallest function value. Each number must stay between minus five and plus five. The known answer is zero, zero, where the function value is zero. We use this point to check our result. We do not insert it into the population or direct the search toward it. The search chooses points and evaluates their function values.

**TIME:** 45 seconds.

---

## Slide 3 — The Ackley function in 2-D

**ON THE SLIDE**

- General form: f(x) = −a exp(−b √(Σxᵢ²/n)) − exp(Σcos(cxᵢ)/n) + a + e
- Set n = 2, a = 20, b = 0.2, c = 2π.
- 2-D form: f(x₁,x₂) = −20 exp(−0.2 √((x₁²+x₂²)/2)) − exp((cos(2πx₁)+cos(2πx₂))/2) + 20 + e
- At (0, 0): −20 − e + 20 + e = 0.

**FIGURE / DELIVERY:** Typeset equations, with a three-step substitution guide.

**SAY**

> The top formula works for any number of variables. Our problem has two variables, so we set n equal to two. We use the standard constants: a is twenty, b is zero point two, and c is two pi. Each sum now contains just two terms. This gives the lower formula used in our code. To check the answer, put zero into both variables. The first part becomes minus twenty, and the second becomes minus e. The remaining terms cancel them, so the mathematical value is zero.

**TIME:** 55 seconds.

---

## Slide 4 — One deep minimum. Many small traps.

**ON THE SLIDE**

- The smooth part makes a wide funnel.
- The cosine part adds many small dips: local minima.
- A downhill search can stop in a local dip.
- A grid with spacing 10⁻⁶ needs about 10¹⁴ points.

**FIGURE / DELIVERY:** 01_ackley_landscape.png; 02_ackley_slice.png.

**SAY**

> These pictures show why Ackley is difficult. The overall surface slopes toward the centre, but it also contains many small dips. We call these local minima. They are lower than nearby points, but they are not the lowest point of the whole surface. A method that follows the local downhill direction can get stuck in one of them. Trying every point is also expensive. A grid with one-millionth spacing across this square would contain about ten to the fourteen points. We need a search that can explore several areas.

**TIME:** 55 seconds.

---

## Slide 5 — Search with a population

**ON THE SLIDE**

- Population → 50 candidate points
- Chromosome → one pair [x₁, x₂]
- Gene → one coordinate
- Fitness → chance of becoming a parent
- Evaluate → select → mix → mutate → repeat

**FIGURE / DELIVERY:** 03_initial_population.png.

**SAY**

> A Genetic Algorithm is inspired by natural selection. We start with fifty possible answers, shown by the points in this figure. Each answer is called a chromosome. It stores two genes: x-one and x-two. We evaluate all fifty points. Better points get a higher chance of becoming parents. We then mix the parents and make small random changes to their children. Repeating this process can move the population toward better areas. The method does not need a derivative, but it does not guarantee success on every problem.

**TIME:** 50 seconds.

---

## Slide 6 — One solution = two real numbers

**ON THE SLIDE**

- Value encoding: [x₁, x₂]
- Example chromosomes: [−4.0, 2.5] and [−1.5, −1.0]
- Each gene stays in [−5, +5].
- Real-valued encoding avoids a fixed binary grid; computer precision is still finite.

**FIGURE / DELIVERY:** Editable two-gene chromosome diagram.

**SAY**

> Our representation is simple. Each chromosome stores the two actual coordinate values. This is called value encoding. For example, minus four and two point five form one candidate answer. We use real-valued numbers instead of a fixed-length binary chromosome. This avoids choosing a binary grid size in advance. It does not give unlimited accuracy, because computers still use finite precision. Throughout the run, both coordinates stay inside the allowed range.

**TIME:** 40 seconds.

---

## Slide 7 — The settings we used

**ON THE SLIDE**

- Assignment: population 50; generations ≤ 100; crossover 80%; mutation 5% per gene; elite 1.
- Required method: value encoding, roulette selection, one-point crossover.
- Our choices: Gaussian mutation; σ = clip(f_best/4, 10⁻¹², 2); at most 15 exact copies.
- Stop after 20 improvements in a row below 10⁻¹⁰; main seed = 7.

**FIGURE / DELIVERY:** Two clearly separated settings panels.

**SAY**

> The left side contains the assignment settings: fifty chromosomes, up to one hundred generations, eighty percent crossover, five percent mutation per gene, and one elite. We also use the required value encoding, roulette selection, and one-point crossover. The right side shows our choices. We use Gaussian mutation, adjust its step size using the current best value, and limit duplicate chromosomes. We also choose a stopping tolerance and use seed seven for the main run. The seed lets us repeat the same experiment.

**TIME:** 45 seconds.

---

## Slide 8 — The search loop

**ON THE SLIDE**

- Start: create 50 points → evaluate → sort.
- Stop? Yes: report best. No: set mutation step and roulette probabilities.
- Select parents → crossover → mutate and clip → evaluate 50 children.
- Keep elite + fill 49 seats from the remaining 99 candidates, with the copy limit.
- Repeat with 50 survivors.

**FIGURE / DELIVERY:** Editable PowerPoint flowchart. Reveal the reproduction and survivor blocks on click.

**SAY**

> This is the full search loop. First, we create fifty random points, evaluate them, and sort them from best to worst. We check whether it is time to stop. If not, we calculate the mutation step and the roulette probabilities. We select parents, apply crossover, then mutate and clip the children. After evaluating fifty children, we have fifty parents and fifty children. We keep the elite and fill the other forty-nine places from the remaining candidates, while applying the duplicate limit. This gives the next population of fifty. Then the loop repeats.

**TIME:** 65 seconds.

---

## Slide 9 — Better points get larger slices

**ON THE SLIDE**

- Objective f: lower is better. Fitness F: higher is better.
- Fᵢ = (f_max − fᵢ) + δ; δ = 0.10(f_max − f_min) + 10⁻¹²
- pᵢ = Fᵢ / ΣFⱼ
- #7: f = 3.19, probability 4.83%; #46: 3.79, 4.57%; #14: 4.87, 4.10%; #45: 13.39, 0.44%.
- Chart: top 10 chromosomes shown; the other 40 are grouped.

**FIGURE / DELIVERY:** 04_roulette_pie_gen0.png; generation-0 table.

**SAY**

> Roulette selection needs a small adjustment for our problem. A smaller Ackley value is better, but roulette selection gives more chances to a larger fitness value. So we subtract each value from the worst value and add a small positive offset. Then we divide by the total fitness to get probabilities. The probabilities add up to one. In our initial population, chromosome seven has the best value, about three point one nine. It gets about four point eight three percent of the wheel. The worst still gets a small chance. The figure shows the ten largest slices separately and groups the other forty together. The actual selection still uses fifty separate probabilities.

**TIME:** 70 seconds.

---

## Slide 10 — Crossover swaps the second gene

**ON THE SLIDE**

- 80%: cut between x₁ and x₂, then swap the tails.
- [−4.0 | 2.5] + [−1.5 | −1.0] → [−4.0 | −1.0] + [−1.5 | 2.5]
- 20%: copy the parents without crossover.
- Crossover combines existing values; it does not create a new number.

**FIGURE / DELIVERY:** Editable, colour-coded parent and child genes. Reveal the children on click.

**SAY**

> Crossover mixes two parents. With only two genes, there is just one place to cut: between x-one and x-two. We swap the second genes. In this example, the first child gets minus four from the first parent and minus one from the second. The other child gets the remaining pair. This happens with eighty percent probability. Otherwise, the children are copies of the parents. Notice that all four numbers already existed. Crossover changes how they are paired, but does not create a new coordinate value.

**TIME:** 50 seconds.

---

## Slide 11 — Mutation creates new values

**ON THE SLIDE**

- Check each gene independently.
- 5% chance: add Gaussian noise, xᵢ ← xᵢ + N(0, σ²).
- Clip any changed value back into [−5, +5].
- Illustration: [−1.5, −1.0] → [−0.5, −1.0].
- The probability stays fixed. The step size σ changes.

**FIGURE / DELIVERY:** Editable before-and-after chromosome and boundary-repair diagram.

**SAY**

> Mutation gives us new coordinate values. We check each gene separately. Each gene has a five percent chance of changing. When it changes, we add a random value from a Gaussian distribution. The example shows only the first gene changing; it is an illustration, not the recorded random output. After a change, we clip the value to the allowed range. For example, five point three becomes five. The mutation probability always stays at five percent. The amount of change depends on sigma, which we explain next. Fresh random replacements in the survivor step can also add new values.

**TIME:** 50 seconds.

---

## Slide 12 — Let progress control the step size

**ON THE SLIDE**

- Timed schedule: steps shrink even when a run is stuck.
- Our rule: σ = clip(f_best / 4, 10⁻¹², 2).
- Examples: 5 → 1.25; 2.6 → 0.65; 10⁻³ → 2.5 × 10⁻⁴; 10⁻¹² → 10⁻¹² (floor).
- Near the origin: s = √((x₁²+x₂²)/2), f ≈ 4s.
- Ackley-specific rule: f/4 estimates a local coordinate scale, not exact Euclidean distance.

**FIGURE / DELIVERY:** Rule card and exact example table.

**SAY**

> Our first version reduced the step size according to the generation number. The problem is that the steps become small even if the run is still stuck in a local dip. Our final version uses the current best function value divided by four. We keep sigma between ten to the minus twelve and two. A poor result therefore keeps larger steps, while a good result gets smaller steps for fine tuning. For example, a best value of two point six gives sigma zero point six five. The factor one quarter comes from the local shape of Ackley. Near the origin, the function is about four times the root-mean-square size of the coordinates. This is a rule chosen for Ackley, not a general distance formula. It uses function knowledge, but does not give the search the answer coordinates.

**TIME:** 80 seconds.

---

## Slide 13 — Keep the best. Limit exact copies.

**ON THE SLIDE**

- 50 parents + 50 children = 100 candidates.
- Reserve the best parent: elitism = 1.
- Fill 49 more seats in order of quality; allow at most 15 exact copies per chromosome.
- If seats remain empty, add fresh random points and evaluate them.
- The best-so-far value cannot get worse.

**FIGURE / DELIVERY:** Editable 100 → 1 elite + 49 survivors diagram. Reveal the survivor rules on click.

**SAY**

> We choose the next generation from the parents and children together. First, we reserve the best parent. This is elitism, and it means our best-so-far result cannot get worse. Then we fill the other forty-nine seats in order of quality. We allow at most fifteen exact copies of the same chromosome. This prevents one identical point from taking all fifty places. If too few candidates fit the rule, the code fills the remaining seats with fresh random points and evaluates them. The copy limit helps keep different chromosomes in the population, although they may still be very close together.

**TIME:** 55 seconds.

---

## Slide 14 — Stop after 100 rounds—or little progress

**ON THE SLIDE**

- Stop at 100 generations, OR when improvement < 10⁻¹⁰ for 20 consecutive generations.
- One flat generation is normal; patience avoids stopping too soon.
- Seed 7: f ≈ 5.87 × 10⁻³ at generation 20; best result at generation 100.

**FIGURE / DELIVERY:** 05_convergence_and_diversity.png. Caption clarifies that σ is clipped in code.

**SAY**

> We stop after one hundred generations, or when the improvement is below ten to the minus ten for twenty generations in a row. One generation without improvement is normal in a random search, so we do not stop immediately. The graph uses a logarithmic scale to show improvements over many orders of magnitude. In the main run, the value is already about zero point zero zero six at generation twenty, but that is not our final precision. The best result is found at generation one hundred. A small improvement is a stopping rule, not proof that the exact optimum has been reached.

**TIME:** 45 seconds.

---

## Slide 15 — Our result is very close to (0, 0)

**ON THE SLIDE**

- Seed 7: x₁ = −3.436 × 10⁻¹³; x₂ = −1.730 × 10⁻¹³; f = 1.088 × 10⁻¹².
- Best found at generation 100; 5,050 function evaluations.
- Distance to (0, 0): 3.847 × 10⁻¹³.
- Random search, same seed and budget: f = 0.7693.
- Coordinates have absolute error < 10⁻¹²; the answer is approximate.

**FIGURE / DELIVERY:** 06_best_solution_path.png.

**SAY**

> These are the numbers from our main run with seed seven. Both coordinates are within ten to the minus twelve of zero. The final function value is about one point one times ten to the minus twelve. The best point was found at generation one hundred, using five thousand and fifty function evaluations. Its distance from the true answer is about three point eight times ten to the minus thirteen. For comparison, random search with the same seed and evaluation budget reached about zero point seven seven. The GA gives a much smaller objective value in this comparison. This is one baseline experiment, not a universal speed or accuracy guarantee. Our result is very close to zero, but it is still an approximation.

**TIME:** 65 seconds.

---

## Slide 16 — Two changes solve different problems

**ON THE SLIDE**

- Same 40 seeds for every version.
- Timed/no cap: median 5.52 × 10⁻⁹; worst 2.58; correct valley 39/40; distinct 3.
- Timed/cap 15: median 6.76 × 10⁻⁹; worst 2.58; correct valley 39/40; distinct 9.
- Adaptive/no cap: median 5.00 × 10⁻¹³; worst 2.31 × 10⁻¹¹; correct valley 40/40; distinct 8.
- Adaptive/cap 15: median 1.64 × 10⁻¹²; worst 3.14 × 10⁻¹¹; correct valley 40/40; distinct 13.
- Correct valley: distance < 0.5. Distinct: median over the second half of each run, then across runs.

**FIGURE / DELIVERY:** Four-row comparison table, with the final version highlighted.

**SAY**

> We tested four versions using the same forty seeds. The top two rows use a timed mutation schedule. Both leave one run stuck at about two point five eight, whether the copy limit is present or not. The bottom two rows use the adaptive step. All forty runs then finish in the correct valley. Their median values are also much smaller. Now look at the last column. The copy limit increases the number of different chromosomes: from three to nine with the timed schedule, and from eight to thirteen with the adaptive step. So the adaptive step mainly improves the result, while the copy limit mainly improves diversity. The adaptive version without the cap actually has the lower median error here. We keep the cap to maintain more distinct candidates.

**TIME:** 80 seconds.

---

## Slide 17 — All 40 runs met the accuracy target

**ON THE SLIDE**

- Seeds 0–39; same final settings.
- Success: f < 10⁻⁶. Result: 40/40.
- Median f = 1.636 × 10⁻¹²; best = 1.106 × 10⁻¹³; worst = 3.137 × 10⁻¹¹.
- Strong evidence for these tests; not a guarantee for every future run.

**FIGURE / DELIVERY:** 09_reliability_40_runs.png. Points visually overlap the optimum; they are approximate.

**SAY**

> To check reliability, we ran the final version with forty different seeds, from zero to thirty-nine. We defined success as a function value below ten to the minus six. All forty runs passed. The median was about one point six times ten to the minus twelve, and even the worst was about three point one times ten to the minus eleven. The points overlap near the origin in the figure, but they are not mathematically exact zero. These tests show that the method worked consistently in our experiments. They do not guarantee that every future run will succeed.

**TIME:** 55 seconds.

---

## Slide 18 — What we learned

**ON THE SLIDE**

- Result: f ≈ 1.1 × 10⁻¹² in the main run; 40/40 tests below 10⁻⁶.
- Selection favours better points.
- Crossover mixes coordinates; mutation creates new values.
- Adaptive steps improve precision; elitism preserves the best; the copy limit supports diversity.
- Test a random algorithm with many seeds.
- Thank you. Questions?

**FIGURE / DELIVERY:** Native summary cards and the original DNA illustration.

**SAY**

> To conclude, our Genetic Algorithm found a point very close to the known minimum. The main run reached a function value of about ten to the minus twelve, and all forty reliability tests met our accuracy target. Each part had a job: selection favoured better points, crossover mixed coordinates, mutation created new values, and elitism protected the best result. The adaptive step improved precision, while the copy limit kept more distinct candidates. Our main lesson is to test a random algorithm with many seeds, rather than judging it from one good run. Thank you, sir. We are ready for questions.

**TIME:** 40 seconds.

---

## Short answers for teacher questions

### Why is the answer not exactly zero?

The GA samples candidate points; it does not solve the equation exactly. Floating-point rounding also affects very small values. Report the measured error, not exact equality.

### Does real-valued encoding have unlimited precision?

No. It avoids a chosen binary grid, but floating-point arithmetic and mutation step size still limit precision.

### Does the adaptive rule use knowledge of Ackley?

Yes. The factor 1/4 is motivated by Ackley near its zero minimum. It uses the current objective value and Ackley-specific scaling, but does not insert the coordinates (0,0). A different or shifted objective may need a different rule.

### Is f/4 the distance to the origin?

Only an approximate local scale. If s = sqrt((x₁²+x₂²)/2), then f ≈ 4s near the origin. The Euclidean distance is sqrt(2) times s.

### What are the exact mutation bounds?

The code sets sigma = min(max(best_value/4, 1e-12), 2.0). Mutation probability stays 5% per gene.

### Why use a copy limit of 15?

It is our implementation choice. The 40-run comparison shows more distinct chromosomes with the cap. The notebook does not establish that 15 is the best possible cap.

### Can a population of clones recover?

It can recover through mutation or fresh random points. However, exact copies reduce the variety available to crossover.

### Does elitism protect the whole population average?

No. It protects the best-so-far result. The mean or worst value can change, especially when new random points are added.

### How many function evaluations are used?

For the main seed-7 run, 50 initial evaluations plus 100 × 50 child evaluations = 5,050. I instrumented the objective to verify this. Other runs can stop earlier, and random replacement points can add evaluations.

### Does 40/40 prove the global optimum is always found?

No. All tested seeds passed f < 1e-6. That is empirical success under these settings, not a mathematical guarantee.

### Why is the stopping tolerance different from the success target?

The stopping tolerance measures change between generations. The success target measures the final objective value. Small change alone does not prove a good solution.

### Why one-point crossover?

The assignment requires it. With two genes there is only one legal cut, so it swaps the second coordinates.

### Can the code handle more variables?

The core operators use the configured gene count and can be adapted. The plots and this experiment are 2-D; higher-dimensional performance was not tested here.

### What is the running cost?

Ignoring dimension and objective cost, one generation evaluates about N children and sorts about 2N candidates: roughly O(N log N). With G generations, this is roughly O(G N log N).


## Notebook check and corrections

The numerical results were independently reproduced from the notebook code, including the main run and the four configurations with 40 seeds each. Verification data: `presentation_review/notebook_verification.json`. The notebook itself has not been edited.

- The exact adaptive rule includes clipping: `sigma = clip(best_value / 4, 1e-12, 2.0)`.
- The local scale `sqrt((x1²+x2²)/2)` is not the Euclidean distance. The step rule is Ackley-specific and uses knowledge of its local shape.
- Floating-point numbers do not have unlimited precision. Use the measured absolute errors instead of claiming an unlimited number of decimals.
- The final run found its best at generation 100. Generation 20 only reached about 0.00587.
- Success is defined as `f < 1e-6`. Correct valley is a separate check: distance to the origin below 0.5. Neither means exact equality with zero.
- The timed versions reached the correct valley in 39 of 40 runs: exactly 97.5%, shown as 98% by the notebook formatting. The slides use counts to avoid rounding confusion.
- The copy limit counts exact chromosomes. Different chromosomes can still be very close. Fresh random fill points are allowed and are also a source of new coordinate values.
- Elitism guarantees that the best-so-far value cannot worsen; it does not guarantee that the population average cannot worsen.
- The seed-7 run used exactly 5,050 objective-point evaluations, verified by counting calls. Random fill points would add evaluations in a run that needs them.
- The baseline result is one same-budget comparison. Removed the broad “700 billion times more accurate” claim.
- Removed unsupported claims that cap values 10–25 had been systematically validated, and that both fixes are necessary for every successful run.
- The roulette pie groups the other 40 chromosomes for display; actual selection uses all 50 probabilities.

## Rehearsal and slide use

Use Presenter View for the notes. Slides 8, 10 and 13 have click reveals. The PDF and screenshots show their completed state. Rehearse slides 12 and 16 most carefully. Keep the pace near the suggested times, and pause after explaining each figure. For a strict 15-minute slot, shorten the formula explanation and the comparison table discussion.
