# Lecture 0 - Search

#### A problem when an "agent" is in a situation searching for a solution to a problem

## Terms

- **agent**: an entity that perceives its environment and acts upon that environment
- **state**: a configuration of the agent and its environment
  - **initial state**: the state in which the agent begins - the starting point for the search algorithm
- **actions**: choices that can be made in a state
  - `actions(s)` is a function that returns the set of actions that can be executed in state `s`
- **transition model**: a description of what state results from performing any applicable action in any state
  - result(s, a)` returns the state resulting from performing action `a` in state `s`
- **state space**: the set of all states reachable from the initial state by any sequence of actions
  - the state space can be represented by a graph (think graph theory graph, not Cartesian graph)
- **goal test**: a way to determine whether a given state is a goal state
- **path cost**: a numerical cost associated with a given path/action
- **solution**: a sequence of actions that leads from the initial state to a goal state
- **optimal solution**: a solution that has the lowest path cost among all solutions
- **node**: a data structure that keeps track of
  - a state
  - a parent (node that generated this node)
  - an action (action applied to parent to get node)
  - a path cost (from initial state to node)
- **frontier**: a data structure that represents all the things that we could explore next that have yet to be visited
- **uninformed searches**: search strategy that uses no problem-specific knowledge
  - **breadth-first search (BFS)**: search algorithm that always expands the shallowest node in the frontier
  - **depth-first search (DFS)**:  search algorithm that always expands the deepest node in the frontier
    - If there is an infinite state space, dfs can potentially never find the solution
- **informed searches**: search strategy that uses problem-specific knowledge to find solutions more efficiently
  - **greedy best-first search (gbfs)**: search algorithm that expands the node that is closest to the goal, as estimated by a heuristic function `h(n)`
    - The heuristic is an estimate, not a guarantee, of the distance of a node to the goal
  - **A* search**: search algorithm that expands node with lowest value of `g(n) + h(n)`, where `g(n)` is the cost to reach the `n` from the initial state. This algorithm is optimal if:
    1. the heuristic is **admissible**: never overestimates the true cost
    2. the heuristic is **consistent**: for every node `n` and successor `n'` with step cost `c` from `n` to `n'` , `h(n) <= h(n') + c` 
- **adversarial search**: there is an agent with intentions in opposition to you or your own agent, like tic-tac-toe
  - **minimax algorithm**:
    - Assigned numbers to each possible outcome
    - **max player** aims to maximize the score
    - **min player** aims to minimize the score



## Search Algorithm Approach

* start with a frontier (which implements a stack) that contains the initial state
* repeat:
  * if the frontier is empty, then no solution
  * remove a node from the frontier
  * if node contains goal state, return the solution
  * Otherwise, expand the node, adding the resulting nodes to the frontier

There's a potential issue with this approach - if I can go from A -> B, but also from B -> A, I could end up in an infinite loop.



## Revised Search Algorithm Approach (depth-first)

- start with a frontier that contains the initial state
- start with an empty explored set
- Repeat:
  - if the frontier is empty, then no solution
  - remove a node from the frontier
  - if node contains goal state, return the solution
  - add the node to the explored set
  - expand node, add resulting nodes to the frontier if they aren't already in the frontier or the explored set



## Game

- `S_o`: initial state
- `player(s)`: returns which player to move in state `s`
- `action(s)`: returns legal moves in state `s`
- `result(s, a)`: returns state after action `a` taken in state `s` 
- `terminal(s)`: checks if state `s` is a terminal state (game is over)
- `utility(s)`: final numerical value for terminal state `s`



## Minimax Algorithm (an adversarial algorithm)

- Given state `s`:

  - `MAX` player picks action `a` in `actions(s)` that produces the highest value of `min_value(result(s, a))`
  - `MIN` player picks action `a` in `actions(s)` that produces smallest value of `max_value(result(s, a))`

- **alpha-beta pruning**: an optimization to the minimax algorithm where you keep track of the best and worst outcomes of a potential state, and don't analyze states that are guaranteed to give you a result smaller than your current maximum or bigger than your current minimum

- **depth-limited minimax**: a version of the minimax algorithm that only considers a certain amount of actions, rather than going to a terminal state

  - **evaluation function**: a function that estimates the expected utility of the game from a given state. Necessary in depth-limited minimax algorithms because without a terminal state, an action wouldn't otherwise be able to have a value assigned to it

  

### `max_value(state)` function

- if `terminal(state)`:

  - return `utility(state)`

- else:

  - `v = -∞`

  - for `action` in `actions(state)`:

    - `v = max(v, min_value(result(state, action)))`

  - return `v`

    

### `min_value(state)` function

- if `terminal(state)`:
  - return `utility(state)`
- else:
  - `v = ∞`
  - for `action` in `actions(state)`:
    - `v = min(v, max_value(result(state, action)))`
  - return `v`