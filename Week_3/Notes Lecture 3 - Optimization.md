# Week 3 - Optimization



## Terms

- **optimization**: choosing the best option from a set of options
  - when the best option is a maximum, you're trying to optimize an objective function
  - when the best option is a minimum, you're trying to optimize a cost function
- **local search**: search algorithms that maintain a single node and search by moving to a neighboring node
  - useful in contexts where the concern is just the solution, and not the path used to get to the solution
- **linear programming**: family of algorithms trying to optimize some mathematical function, often with continuous real values instead of discrete real values; only dealing with linear equations and linear constraints



## Local Search Algorithms

### Hill Climbing algorithm

- function `Hill-Climbing(problem)`

  - `current` = initial state of `problem`
  - repeat:
    - `neighbor` = highest valued neighbor of `current`
    - if `neighhbor` not better than `current`
      - return `current`
    - `current = neighbor`

  ### Variants

  - **steepest-ascent**: choose the highest-valued neighbor
  - **stochastic**: choose randomly from higher-valued neighbors
  - **first-choice**: choose the first higher-valued neighbor
  - **random-restart**: conduct hill climbing multiple times
  - **local beam search**: chooses the *k* highest-valued neighbors



### Simulated Annealing  # TODO review this in more detail

-  Early on, higher "temperature": more likely to accept neighbors that are worse than current state

- Later on, lower "temperature": less likely to accept neighbors that are worse than current state

  ### Algorithm

  - function `simulated-annealing(problem, max)`
    - `max` is the maximum number of times we're going to run the process
  - `current` = initial state of `problem`
  - for `t = 1` to `max`:
    - `T= temperatur(t)`, where `t` is the current time
    - `neighbor` = random neighbor of `current` 
    - `ΔE`= how much better `neighbor` is than `current`
    - if `ΔE` > 0:
      - `current = neighbor`
    - with probability `e^(ΔE/T)` set `current = neighbor`  # TODO where did that probability come from 
    - return `current` 



### Application: Traveling Salesman Problem

**How can I visit every location and end up back where I started in the most efficient way possible?**

- np complete problem - no known efficient way to solve
- one definition of a "neighbor state" in this problem is to pick two edges between nodes and switch them to point to different nodes



## Linear Programming Algorithms  # TODO explore these in more detail

- Simplex
- Interior-Point 



## Constraint Satisfaction Problems

- Set of variables `{X1, X2, ..., Xn}`
- Set of domains for each variable `{D1, D2, ..., Dn}`
- Set of constraints `C`
  - **hard constraints**: constraints that must be satisfied in a correct solution
  - **soft constraints**: constraints that express some notion of which solutions are preferred over others
  - **unary constraint**: constraint involving a single variable
  - **binary constraint**: constraint involving two variables
  - **node consistency**: when all the values in a variable's domain satisfy the variable's unary constraints
  - **arc (edge) consistency**: when all the values in a variable's domain satisfy the variable's binary constraints; to make `X` arc-consistent with respect to `Y`, remove elements from `X`'s domain until every choice for `X` has a possible choice for `Y`
    - function `revise(csp, X, Y)` - takes `csp` (constraint satisfaction problem) and makes `X` arc-consistent with respect to `Y`
      - `revised = false`
      - for `x` in `X.domain`:
        - if no `y` in `Y.domain` satisfies constraint for `(X, Y)` 
          - delete `x` from `X.domain`
          - `revised = true` 
      - return `revised`
    - function `AC-3(csp)` - takes `csp` and enforces arc-consistency across the entire problem
      - `queue` = all arcs in `csp`
      - while `queue` non-empty:
        - `(X, Y) = dequeue(queue)` (doesn't really have to be a queue structure, but that's conventional)
        - if `revise(csp, X, Y)`
          - if size of `X.domain` = 0:
            - return `false`
          - for each `Z` in `X.neighbors - {Y}`
            - `enqueue(queue, (Z, X))
        - return `true`



## CSPs as Search Problems

- initial state: empty assignment (no variable)
- actions: add a `{variable = value}` to assignment
- transition model: shows how adding an assignment changes the assignment
- goal test: check if all variables assigned and constraints all satisfied
- path cost function: all paths have same cost (kinda irrelevant in CSPs)