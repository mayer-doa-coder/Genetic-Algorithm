# Easy Presentation Script — Ackley Function with the Artificial Bee Colony

**19 slides · planned speaking time 17 min 30 sec · presentation date 14 September 2026**

The short text belongs on the slides. The SAY paragraphs are also in the PowerPoint speaker notes. Speak naturally and point at the diagrams. Allow about 19–21 minutes including pauses and speaker changes.

**Six-speaker option:** 2107001: slides 1–3; 2107004: slides 4–6; 2107009: slides 7–9; 2107015: slides 10–12; 2107024: slides 13–15; 2107047: slides 16–19. Adjust within the group if needed.

**Pronunciation:** ABC = “A B C”; Ackley = “ACK-lee”; Karaboga = “kah-rah-BOW-ah”; phi = “fy”; 10⁻¹³ = “ten to the minus thirteen”; onlooker = “ON-look-er”; exploitation = “using what you already know”; exploration = “looking somewhere new”.

---

## Slide 1 — Finding the global minimum

**ON THE SLIDE**

- The 2-D Ackley function, solved by an Artificial Bee Colony
- Submitted to: Dr. Al-Mahmud, Professor, Department of CSE, KUET
- Submitted by: 2107001, 2107004, 2107009, 2107015, 2107024, 2107047

**FIGURE / DELIVERY:** Title slide: honeycomb corners, flying bees and the beehive from the template.

**SAY**

> Good morning, sir. Our project finds the lowest point of the two-dimensional Ackley function using the Artificial Bee Colony algorithm. It is the same problem we solved earlier with a Genetic Algorithm, so at the end we can compare the two fairly. We will explain the problem, show how the three kinds of bee work, and present our results.

**TIME:** 30 seconds.

---

## Slide 2 — Find the lowest point

**ON THE SLIDE**

- Goal: choose x1 and x2 to make f as small as possible.
- Range: -5 <= x1, x2 <= 5
- Known minimum: (0, 0), where f = 0
- The bees are never told where (0, 0) is.

**FIGURE / DELIVERY:** Native coordinate diagram: the allowed square and the known optimum.

**SAY**

> We need two numbers, x-one and x-two, that give the smallest function value. Each number must stay between minus five and plus five. The known answer is zero, zero, where the function value is zero. We use that point only afterwards, to measure how close we got. We never put it into the colony and we never point the search towards it. The bees only choose points and taste how much nectar is there.

**TIME:** 45 seconds.

---

## Slide 3 — The Ackley function in 2-D

**ON THE SLIDE**

- General form: f(x) = -a exp(-b sqrt(sum xi^2 / n)) - exp(sum cos(c xi) / n) + a + e
- Set n = 2, a = 20, b = 0.2, c = 2 pi.
- 2-D form: f(x1,x2) = -20 exp(-0.2 sqrt((x1^2+x2^2)/2)) - exp((cos 2 pi x1 + cos 2 pi x2)/2) + 20 + e
- At (0, 0): -20 - e + 20 + e = 0.

**FIGURE / DELIVERY:** Typeset equations with a three-step substitution guide.

**SAY**

> The top formula works for any number of variables. Our problem has two variables, so we set n equal to two. We use the standard constants: a is twenty, b is zero point two, and c is two pi. Each sum now has just two terms, which gives the lower formula used in our code. To check it, put zero into both variables. The first part becomes minus twenty and the second becomes minus e. The remaining terms cancel them, so the value is exactly zero.

**TIME:** 55 seconds.

---

## Slide 4 — One deep minimum. Many small traps.

**ON THE SLIDE**

- The smooth part makes one wide funnel.
- The cosine part adds many small dips: local minima.
- A downhill search can stop in a local dip.
- A grid with spacing 10^-6 would need about 10^14 points.

**FIGURE / DELIVERY:** 01_ackley_landscape.png and 02_ackley_slice.png.

**SAY**

> These pictures show why Ackley is difficult. The whole surface slopes towards the centre, but it is also covered in small dips. We call those local minima. They are lower than everything nearby, but they are not the lowest point of the whole surface. A method that simply walks downhill can get stuck in one of them. Checking every point is far too expensive: a grid with one-millionth spacing across this square holds about ten to the fourteen points. So we need a search that can look in several places at once.

**TIME:** 55 seconds.

---

## Slide 5 — A colony instead of a population

**ON THE SLIDE**

- Food source  ->  one candidate answer [x1, x2]
- Nectar amount  ->  fitness, higher is better
- Employed bee  ->  improves its own source
- Onlooker bee  ->  helps the richest sources
- Scout bee  ->  replaces a source that is stuck

**FIGURE / DELIVERY:** 03_initial_sources.png next to the biology-to-program table.

**SAY**

> The Artificial Bee Colony copies how real honey bees collect food. It was published by Dervis Karaboga in two thousand five. A food source is one possible answer, stored as the pair x-one and x-two. The nectar amount of a source is its fitness: the better the answer, the more nectar. Three kinds of bee then do three different jobs, and the picture shows our twenty-five sources scattered at the very start.

**TIME:** 50 seconds.

---

## Slide 6 — Three bees, three jobs

**ON THE SLIDE**

- Employed bees: 25 bees, one per food source. Try a nearby point, keep the better one.
- Onlooker bees: 25 bees. Watch the waggle dance, choose a source by roulette wheel, search near it.
- Scout bees: when a source fails 50 times in a row, throw it away and start somewhere new.
- Exploitation, guided search, exploration.

**FIGURE / DELIVERY:** Native three-panel bee-role diagram with hexagon badges. Reveal one panel per click.

**SAY**

> Here are the three jobs. An employed bee sits on one food source and keeps testing points right next to it, keeping whichever is better. That is careful local improvement, which we call exploitation. An onlooker bee does not own a source. It waits in the hive, watches the waggle dances, and chooses which source to visit, with the richer sources more likely to be chosen. That is guided search. A scout bee handles failure: if one source has refused to improve fifty times in a row, the colony gives up on it and starts again somewhere random. That is exploration.

**TIME:** 60 seconds.

---

## Slide 7 — The settings we used

**ON THE SLIDE**

- Slide-20 control parameters: colony 50; employed 25; onlookers 25; scouts <= 1; limit 50; D = 2.
- Colony 50 = the assignment population of 50, split 50-50 as the slide requires.
- limit = SN x D = 25 x 2 = 50, the usual textbook choice.
- Stop after 100 cycles, or 20 cycles with improvement below 10^-10. Seed = 7.

**FIGURE / DELIVERY:** Two settings panels: the six control parameters, and the GA-to-ABC mapping.

**SAY**

> The left panel holds the six control parameters listed on slide twenty. The colony has fifty bees, matching the fifty chromosomes of our Genetic Algorithm. Slide twenty says employed bees are half the swarm and onlookers the other half, so we get twenty-five food sources and twenty-five onlookers. The limit is fifty, which is the usual choice of sources times dimension. The right panel maps the Genetic Algorithm settings onto this one. Notice the empty rows: ABC has no crossover rate and no mutation rate at all. There is far less to tune.

**TIME:** 50 seconds.

---

## Slide 8 — The ABC cycle

**ON THE SLIDE**

- Step 1: assign the control parameters.
- Step 2: initialise 25 random food sources and evaluate them.
- Step 3, repeated: employed bees -> onlookers -> memorise the best -> scouts.
- Step 4: stop after 100 cycles, or when progress stalls.
- Memorise before scouting, so a scout can never delete the best answer.

**FIGURE / DELIVERY:** Native PowerPoint flowchart. Reveal the three phase blocks on click.

**SAY**

> This is the whole algorithm, exactly as slide eighteen gives it. Step one, set the control parameters. Step two, create twenty-five random food sources and taste all of them. Step three repeats until we stop: send the employed bees, then the onlookers, then memorise the best solution, then send the scouts. Step four, stop and report. One detail matters a lot. We memorise the best solution before the scouts run. If we did it the other way around, a scout could delete the best answer we had found. Memorising first is this algorithm’s version of elitism.

**TIME:** 65 seconds.

---

## Slide 9 — Every solution is two real numbers

**ON THE SLIDE**

- Food source i = [x1, x2], each coordinate inside [-5, +5].
- Initialise with x_ij = x_min,j + rand(0,1) (x_max,j - x_min,j).
- The scout phase reuses this very same equation.
- Example sources: [-4.0, 2.5] and [-1.5, -1.0].

**FIGURE / DELIVERY:** Editable two-coordinate food-source diagram plus the initialisation equation.

**SAY**

> Our representation is the simplest possible. A food source stores the two coordinate values directly, which is the same value encoding the Genetic Algorithm used. Slide twenty-one gives the initialisation equation: take the lower bound, and add a random fraction of the full width. Here that means minus five plus a random number times ten. The nice part is that the scout phase uses exactly the same equation, so we only write it once. Throughout the run both coordinates stay inside the allowed range.

**TIME:** 45 seconds.

---

## Slide 10 — How a bee searches nearby

**ON THE SLIDE**

- v_ij = x_ij + phi_ij (x_ij - x_kj)
- phi = rand(-1, 1); k is another source, k != i; j is one random coordinate.
- Only one coordinate moves. The other is copied unchanged.
- The step size is set by the gap to another bee, so it shrinks by itself.

**FIGURE / DELIVERY:** 07_neighbour_step.png: where the trial point can land, and the self-shrinking step.

**SAY**

> This single equation is the heart of the algorithm. To search near its own source, a bee picks another bee at random, picks one of the two coordinates, and moves that coordinate by a random fraction of the gap between the two bees. Phi is a random number between minus one and plus one, so the bee may step towards the other source or away from it. The left picture shows exactly where the new point can land. Now look at the right picture, because this is the clever part. The step size is the gap between two bees. As the colony gathers near the answer, that gap shrinks, so the steps shrink too. Nobody has to design a shrinking schedule. In our Genetic Algorithm we had to invent one by hand.

**TIME:** 70 seconds.

---

## Slide 11 — Keep the better one

**ON THE SLIDE**

- Compare f(x_i) with f(v_i). Greedy selection: keep whichever is smaller.
- If the new point wins: replace the source and reset its trial counter to 0.
- If it loses: keep the old source and add 1 to the trial counter.
- The trial counter is what the scout phase watches.

**FIGURE / DELIVERY:** Native before-and-after diagram with the trial counter.

**SAY**

> After a bee makes a trial point, it tastes it and compares. If the new point is better, it replaces the old source and the trial counter for that source goes back to zero. If the new point is worse, the old source stays and the trial counter goes up by one. This is called greedy selection, and it means no food source can ever get worse. The trial counter is a simple record of how long a source has been stuck, and it is the number the scouts watch.

**TIME:** 45 seconds.

---

## Slide 12 — Better sources get larger slices

**ON THE SLIDE**

- Minimisation needs a flip: nectar fit_i = 1 / (1 + f_i), since Ackley is never negative.
- P_i = fit_i / sum of all fit  -  slide 25, the roulette wheel.
- At cycle 0: richest source 9.56 %, poorest 3.03 %, ratio 3.16.
- Each of the 25 onlookers spins the wheel once.

**FIGURE / DELIVERY:** 04_roulette_pie_cycle0.png with the cycle-0 table.

**SAY**

> Roulette selection gives more chances to a bigger number, but for us a smaller Ackley value is better. So we flip it: the nectar amount is one divided by one plus the function value. Ackley is never negative, so this is always between zero and one, and a lower function value always gives more nectar. Slide twenty-five then divides each nectar amount by the total, which gives the probability of each source. The pie chart shows all twenty-five slices at cycle zero. The richest source owns about nine and a half percent of the wheel and the poorest about three percent, so even the worst source keeps a real chance.

**TIME:** 65 seconds.

---

## Slide 13 — Something the slides do not mention

**ON THE SLIDE**

- fit = 1/(1+f) is squeezed into (0, 1].
- Once every f is below about 10^-3, every nectar value rounds to 1.
- From cycle 62 every slice is exactly 1/25 = 4.00 %: the onlookers pick at random.
- We measured whether this costs accuracy. It does not - see the next slide.

**FIGURE / DELIVERY:** 05_roulette_early_vs_late.png and 06_wheel_pressure.png.

**SAY**

> Here is something we noticed that the slides do not mention. The nectar formula is squeezed between zero and one. Once every source has a function value below about one thousandth, every nectar value rounds to one, so every slice of the wheel becomes exactly one twenty-fifth. From cycle sixty-two onwards our onlookers are choosing completely at random. That sounds like a serious bug, so we tested it instead of guessing. We also tried two published alternatives that keep the wheel sharp. The next slide shows the measurement, and the answer is not what we expected.

**TIME:** 65 seconds.

---

## Slide 14 — Which part of ABC actually matters?

**ON THE SLIDE**

- Each row changes one thing and runs the same 40 seeds.
- Remove the onlookers: 500,000 times worse. They supply the precision.
- Remove the scouts: no change at all. They never fired on this problem.
- limit = 5: over 2,000 scouts, and not one run reaches the target.

**FIGURE / DELIVERY:** Measured ablation table, 40 seeds per row.

**SAY**

> This table is the most useful thing we did. Each row changes one thing and runs the same forty seeds. Three results stand out. First, the onlooker phase is what makes the answer precise. Taking it away makes the median result five hundred thousand times worse, and four runs miss the target. Second, and this surprised us, the scout phase never fires at all on this problem. Turning it off changes nothing, because the bees always find some improvement before any counter reaches fifty. Third, the limit is the dangerous knob. Set it to five and the colony panics, sends over two thousand scouts, throws away good sources faster than it can refine them, and not a single run reaches the target. The probability rule hardly matters, which also answers the previous slide: by the time the wheel goes flat, every source is already in the right valley.

**TIME:** 75 seconds.

---

## Slide 15 — Our result is very close to (0, 0)

**ON THE SLIDE**

- Best x1 = +2.278 x 10^-13,  best x2 = -3.938 x 10^-14
- Best f = 6.541 x 10^-13, found at cycle 99 of 100
- Distance to (0, 0) = 2.312 x 10^-13
- 5,025 Ackley evaluations, and zero scouts were needed.

**FIGURE / DELIVERY:** 09_best_solution_path.png with the headline numbers.

**SAY**

> Here is our main run, with seed seven so anyone can repeat it exactly. The best point sits about two times ten to the minus thirteen away from the true answer, and the function value there is six point five times ten to the minus thirteen. The left picture shows the path of the best answer across the whole square, and the right picture zooms in near the centre. You can see the bees exploring widely at first, then making smaller and smaller corrections. The whole run used five thousand and twenty-five evaluations, and needed no scouts at all.

**TIME:** 55 seconds.

---

## Slide 16 — The colony closing in

**ON THE SLIDE**

- The best value never gets worse, because it is memorised every cycle.
- Both bee phases keep finding improvements right up to cycle 100.
- The largest trial counter peaked at 23, well below the limit of 50.
- Each snapshot panel is zoomed in further than the one before it.

**FIGURE / DELIVERY:** 08_convergence_and_work.png and 10_source_snapshots.png.

**SAY**

> The left graph tracks the best, the average and the worst source. The best line only ever goes down, because we memorise it every cycle. The middle graph shows that both bee phases keep finding improvements all the way to cycle one hundred: the search never actually finishes. The dark brown line is the largest trial counter. It peaked at twenty-three, nowhere near the limit of fifty, which is why no scout was ever sent. In the snapshots, please read the axis numbers. Each panel is zoomed in much further than the one before. By cycle one hundred the whole picture is only about two times ten to the minus ten wide.

**TIME:** 55 seconds.

---

## Slide 17 — All 40 runs met the target

**ON THE SLIDE**

- Seeds 0 to 39, nothing else changed.
- Median 5.476 x 10^-13, worst 1.034 x 10^-11, best 2.887 x 10^-14.
- 40 / 40 runs finished below 10^-6.
- Random search with the same 5,025 evaluations: f = 0.769.

**FIGURE / DELIVERY:** 11_reliability_40_runs.png.

**SAY**

> One good run proves very little, so we ran forty, changing only the random seed. Every single one finished below our target of ten to the minus six. The median was five point five times ten to the minus thirteen and even the worst run reached ten to the minus eleven. The right panel is zoomed to a width of about seven times ten to the minus twelve, which is the only way to see the forty points separately. For comparison, pure random search with exactly the same number of evaluations only reached zero point seven seven. This is good evidence of reliability, but it is forty runs on one problem, not a guarantee.

**TIME:** 55 seconds.

---

## Slide 18 — Bees next to genes

**ON THE SLIDE**

- Same problem, same 40 seeds, almost the same budget.
- GA: 5,050 evaluations, median 1.636 x 10^-12, 40/40 below 10^-6.
- ABC: 5,025 evaluations, median 5.476 x 10^-13, 40/40 below 10^-6.
- ABC needed one parameter tuned. The GA needed five.

**FIGURE / DELIVERY:** Side-by-side comparison table and 13_budget_comparison.png.

**SAY**

> Because we solved the same problem twice, we can compare honestly. Both methods are reliable: forty out of forty runs for each. The bee colony landed about three times closer to zero, using one and a half percent more evaluations. But the clearer difference is on the last row. For the Genetic Algorithm we had to choose a crossover rate, a mutation rate, a mutation step rule, elitism, and a duplicate cap. For the bee colony we chose one number, the limit, and the step size took care of itself. That is what slide thirty-one means by "few control parameters". We should be careful though: this is one function, in two dimensions, with one budget.

**TIME:** 60 seconds.

---

## Slide 19 — What we learned

**ON THE SLIDE**

- Three simple roles, repeated 100 times, reach 10^-13 accuracy.
- The step size comes free from the distance between bees.
- Test the algorithm, do not just trust the diagram: the scouts never fired.
- Honest limits: one function, two dimensions, 40 seeds.

**FIGURE / DELIVERY:** Closing panels with the hive illustration.

**SAY**

> To finish, four things we learned. First, three very simple bee roles, repeated one hundred times, are enough to find the answer to thirteen decimal places. Second, the step size comes free from the distance between bees, which removes the hardest thing we had to tune in the Genetic Algorithm. Third, and most important for us as students, we should test an algorithm rather than trust its diagram. The scout phase looks essential on every flowchart, and on this problem it never ran once. And fourth, we should state our limits honestly: this is one function, in two dimensions, measured over forty seeds. Thank you, sir. We are happy to take questions.

**TIME:** 50 seconds.

---

## Short answers for teacher questions

### Why 25 food sources when the assignment says a population of 50?

Slide 20 of the course notes says employed bees are 50 % of the swarm and onlookers the other 50 %. The number of food sources equals the number of employed bees. So a colony of 50 bees means 25 sources plus 25 onlookers. The evaluation budget stays the same as the GA version: 5,025 against 5,050.

### Where is crossover and mutation in ABC?

There is none. ABC has a single move, v_ij = x_ij + phi_ij (x_ij - x_kj). It takes the place of both operators: it mixes information from two sources, like crossover, and it adds randomness through phi, like mutation. That is why ABC has fewer control parameters.

### What is the elitism of ABC?

Step 3d of slide 18, "memorize the best solution". We copy the best source found so far into a separate variable every cycle, before the scout phase runs. That guarantees the reported answer can never get worse, exactly like elitism = 1 in the GA.

### Why is the fitness 1 / (1 + f)?

Roulette selection needs larger to mean better, but we are minimising. Dividing one by one plus the objective value flips the order while staying positive. It is the standard ABC rule. The second branch, 1 + |f| for negative f, never applies here because Ackley is never negative.

### How many times is the Ackley function evaluated?

25 at initialisation, then per cycle 25 employed-bee trials plus 25 onlooker trials plus at most 1 scout. No scout ever fired in our run, so the count is 25 + 100 x 50 = 5,025, and that is the number on the slides. If a scout had flown every cycle the worst case would have been 5,125.

### You said the scouts never ran. Then why keep them?

Because the measurement is specific to this problem. On 2-D Ackley with 25 sources, the bees always find some improvement before a counter reaches 50. On a harder or higher-dimensional function a source can genuinely stall, and then the scout is the only way out. We left it in and reported honestly that it never fired here. We did not test a harder function.

### What happens if the limit is too small?

The colony destroys its own progress. At limit = 5 our 40 runs sent over 2,000 scouts between them and not one reached 10^-6; the median was 5.4 x 10^-4. Good sources were abandoned before the bees had time to refine them.

### Your onlooker wheel becomes uniform. Is that not a failure?

It is a real effect and we measured it: from cycle 62 every slice is exactly 4.00 %. It does not cost accuracy here, because by cycle 62 all 25 sources are already inside the central valley, so choosing among them at random is nearly as good as choosing by nectar. We also ran two published alternatives that keep the wheel sharp, and the medians were 5.5, 6.0 and 24.3 x 10^-13 for plain, scaled and rank. The difference is not meaningful.

### Is ABC better than the Genetic Algorithm?

On this problem, with this budget, it reached a median about three times closer to zero and needed one parameter tuned instead of five. Both were reliable: 40 out of 40 runs each. That is evidence for this problem, not a general claim. A different function could easily reverse it.

### How do you know the answer is correct and not luck?

Three ways. The seeded run reproduces exactly. The notebook asserts that the reported value really is f of the reported point, that every coordinate stayed in range, and that the memorised best never got worse. And the 40-seed study shows the result is typical, not a lucky draw.

### Why does ABC not need a shrinking step size, when the GA did?

Because the step is phi times (x_i - x_k), a fraction of the distance to another bee. As the colony contracts around the optimum that distance contracts too, so the steps become small automatically. In the GA the mutation step was an absolute number, so we had to shrink it by hand with sigma = clip(f_best / 4, 10^-12, 2).

### Could the bees get trapped in a local minimum?

Yes, and the course slides list exactly that as the disadvantage: the search space is limited by the initial solutions. With only 5 sources instead of 25 it happened often - just 11 of our 40 runs reached the target. With 25 sources all 40 runs found the correct valley.


---

## Where every number comes from

All results were produced by `Ackley_ABC_Solution.ipynb` and independently re-run by `review/experiments.py`, which writes `review/results.json`. The main run uses seed 7.

- Main run: x₁ = +2.278e-13, x₂ = −3.938e-14, f = 6.541e-13, best at cycle 99 of 100, distance 2.312e-13, 5,025 evaluations, 0 scouts.
- 40 seeds (0–39): best 2.887e-14, median 5.476e-13, worst 1.034e-11, 40/40 below 1e-6, 40/40 in the correct valley.
- Random search, same 5,025-evaluation budget, same seed: f = 0.7693.
- Genetic Algorithm, same 40 seeds, 5,050 evaluations: best 1.106e-13, median 1.636e-12, worst 3.137e-11, 40/40 below 1e-6.
- Cycle-0 wheel: richest slice 9.56 % (source #7, f = 3.19), poorest 3.03 % (source #3, f = 12.23), ratio 3.16.
- The wheel becomes exactly uniform (every slice 4.00 %) from cycle 62 onwards.
- The largest trial counter in the main run reached 23, against a limit of 50, so no scout was ever sent.

## Things to be careful about when answering

- 5,025 is the number of Ackley calls that actually happened. 5,125 is the worst-case budget, which assumes a scout flies every cycle; none did. The slides quote the actual count.
- “Success” means f < 1e-6. “Correct valley” means the distance to (0,0) is below 0.5. Neither means the answer is exactly zero.
- Floating-point numbers do not have unlimited precision. Quote the measured errors rather than claiming an unlimited number of decimals.
- The claim that the scout phase does not matter applies to **this** problem only. We did not test a harder or higher-dimensional function.
- The comparison with the Genetic Algorithm is one problem at one budget. It is evidence, not proof that ABC is generally better.
- The onlooker wheel going flat is real and measured, but it costs no measurable accuracy here; do not present it as a bug we fixed.

## Rehearsal and slide use

Use Presenter View for the notes. Slides 6 and 8 reveal their blocks on click; the PDF and the screenshots show the completed state. Rehearse slides 10, 13 and 14 most carefully, because they carry the reasoning. For a strict 18-minute slot, shorten the formula explanation on slide 3 and the ablation discussion on slide 14.
