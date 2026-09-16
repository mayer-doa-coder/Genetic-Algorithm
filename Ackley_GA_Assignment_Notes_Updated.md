# Assignment: Find the Global Minimum of the 2D Ackley Function Using a Genetic Algorithm (GA)

## 1. Objective

Find the **global minimum of the 2D Ackley function** using a **Genetic Algorithm (GA)**.

---

## 2. Ackley Function for \(n\) Dimensions

For

\[
\mathbf{x} = (x_1,x_2,\ldots,x_n),
\]

the Ackley function is

\[
f(x_1,x_2,\ldots,x_n)
=
-a\exp\left(
-b\sqrt{\frac{1}{n}\sum_{i=1}^{n}x_i^n}
\right)
-
\exp\left(
\frac{1}{n}\sum_{i=1}^{n}\cos(cx_i)
\right)
+a+e.
\]

### Recommended Parameters

\[
a=20,\qquad b=0.2,\qquad c=2\pi.
\]

---

## 3. Ackley Function for 2D

For two variables \(x_1\) and \(x_2\),

\[
f(x_1,x_2)
=
-20\exp\left(
-0.2\sqrt{\frac{x_1^2+x_2^2}{2}}
\right)
-
\exp\left(
\frac{\cos(2\pi x_1)+\cos(2\pi x_2)}{2}
\right)
+20+e.
\]

Using

\[
e \approx 2.71828.
\]

### Search Range

\[
-5 \le x_1 \le 5,
\qquad
-5 \le x_2 \le 5.
\]

### Known Global Minimum

The Ackley function has its global minimum at

\[
f(x^*)=0,\qquad x^*=0.
\]

For the 2D case,

\[
x^*=(0,0),
\]

so

\[
f(0,0)=0.
\]

Therefore, the GA should try to find a solution \((x_1,x_2)\) as close as possible to \((0,0)\), with

\[
f(x_1,x_2)\approx 0.
\]

The obtained solution should also be checked for **precision**, i.e., how close the final function value and variables are to the true optimum.

---

## 4. GA Settings

| Parameter | Value |
|---|---:|
| Population size | 50 |
| Maximum number of generations | 100 |
| Crossover probability, \(P_c\) | 80% |
| Mutation probability, \(P_m\) | 5% |
| Elitism | 1 |

The handwritten note also mentions approximately **20–25 iterations** as a possible practical convergence region, while the configured maximum is **100 generations**.

---

## 5. Chromosome Representation

Use the **value encoding technique**.

Each chromosome contains the two decision variables:

\[
\text{Chromosome}=[x_1,x_2].
\]

Each gene must remain within

\[
[-5,+5].
\]

Example chromosomes:

\[
[-4,\;2.5]
\]

and

\[
[-1.5,\;-1.0].
\]

---

## 6. Genetic Operators

### 6.1 Selection

Use **Roulette Wheel Selection**.

For roulette-wheel selection, calculate a selection probability for each chromosome based on its fitness.

Since this is a **minimization problem**, a chromosome with a lower Ackley function value should be treated as a better solution.

A **pie chart** may be used to show the roulette-wheel selection probabilities.

### 6.2 Crossover

Use **1-point crossover**.

For a chromosome of the form

\[
[x_1,x_2],
\]

the crossover point can be placed between \(x_1\) and \(x_2\).

### 6.3 Mutation

Mutation changes one gene value while keeping it inside the allowed range.

For example,

\[
[-1.5,-1.0]
\]

may mutate to

\[
[-0.5,-1.0].
\]

Mutation **might use array traversal** to go through the genes and decide whether each gene should be mutated.

A new value may be generated randomly, and a **Gaussian distribution** can also be used for mutation.

After mutation, every gene must still satisfy

\[
-5\le x_i\le5.
\]

---

## 7. Correct GA Sequence

### Step 1 — Initialize the Population

Generate an initial population of **50 chromosomes**.

Each chromosome is

\[
[x_1,x_2],
\]

where both values are randomly generated within

\[
[-5,+5].
\]

### Step 2 — Calculate the Objective/Fitness

For every chromosome, calculate the Ackley function value.

A lower Ackley function value means a better solution.

### Step 3 — Sort the Population

Sort the chromosomes according to solution quality.

The chromosome with the **lowest Ackley function value** is the best solution.

### Step 4 — Find and Preserve the Elite

Find the best chromosome of the current generation.

Because

\[
\text{Elitism}=1,
\]

preserve the best chromosome so that it is not lost in the next generation.

### Step 5 — Generate New Solutions

Inside the reproduction loop, perform:

1. **Selection**
2. **Crossover**
3. **Mutation**

to create new offspring.

### Step 6 — Roulette-Wheel Probabilities

Calculate the selection probability of each chromosome according to fitness.

These probabilities can be represented using a **pie chart** for the roulette wheel.

### Step 7 — Keep Solutions Inside the Search Space

While generating new chromosomes, make sure that all gene values remain inside

\[
[-5,+5].
\]

Continue generating new candidate solutions through crossover and mutation.

### Step 8 — Recalculate Fitness

After generating the new solutions, calculate their Ackley function values again.

### Step 9 — Form the Next Generation

For the next generation, keep the **best 50 chromosomes** from the available candidates while ensuring that the elite solution is preserved.

This keeps the **population size constant at 50**.

### Step 10 — Repeat

Repeat the GA process generation by generation.

---

## 8. Stopping Criteria

Stop the algorithm when either:

1. **100 generations** have been completed, or
2. the improvement between two consecutive generations becomes smaller than the chosen **precision/tolerance value**.

The handwritten note does not specify an exact numerical tolerance, so that value must be defined in the implementation.

---

## 9. Expected Final Result

At the end of the GA, report:

- Best \(x_1\)
- Best \(x_2\)
- Best Ackley function value
- Generation at which the best solution was found
- Error/precision relative to the true optimum

The expected result is approximately

\[
x_1\approx0,\qquad x_2\approx0,
\]

and

\[
f(x_1,x_2)\approx0.
\]

The exact theoretical global minimum is

\[
\boxed{f(x^*)=0,\qquad x^*=0}.
\]

For the 2D case,

\[
\boxed{x^*=(0,0),\qquad f(0,0)=0}.
\]
