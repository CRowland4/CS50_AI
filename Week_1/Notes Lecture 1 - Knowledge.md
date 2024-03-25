# Week 1 - Knowledge



## Terms

- **knowledge-based agents**: agents that reason by operating on internal representations of knowledge

- **sentence**: an assertion about the world in a knowledge representation language

- **proposition symbols**: conventionally `P`, `Q`, and `R`; represent some fact, or "sentence", about the world

- **logical connectives**: `not`, `and`, `or`, `conditional`, `biconditional`
  - Note to remember: `biconditional` can be read as "if and only if", or "iff" in mathematical shorthand
- **model**: assignment of a truth value to every propositional symbol (a "possible world")
- **knowledge base**: a set of sentences known by a knowledge-based agent
- **entailment**: `α ╞ ß`; in every model in which sentence `α` is true, sentence `ß` is also true
- **inference**: the process of deriving new sentences from old ones
- **inference algorithm**: answers the central question of entailment: `KB ╞ α`? where `KB` is the knowledge base
- **knowledge engineering**: the process of distilling knowledge down into a form that is representable by a computer
- **disjunction**: things connected with `∨`
- **conjunction**: things connected with `∧`
- **literal**: a proposition symbol or its opposite
- **clause**: a disjunction of literals
- **conjunctive normal form (CNF)**: logical sentence that is a conjunction of clauses
- **empty clause**: clause without any literals; always resolves to false



## Model Checking Algorithm

- to determine if `KB ╞ α`:
  - enumerate all possible models (consider all possible combinations of true and false for the variables in the model)
  - if in every model where `KB` is true, `α` is true, then `KB ╞ α`
  - otherwise, `KB` does not entail `α`



## Inference Rules

### Taking knowledge that already exists and translating it into new forms of knowledge

- **modus ponens**: `((α → ß) ∧ α) → ß`
- **and elimination**: `((α ∧ ß) → ß`,  `((α ∧ ß) → α`
- **double negation elimination**: `¬(¬α) → α`
- **implication elimination**: `(α → ß) → (¬α ∨ ß)`
- **biconditional elimination**: `(α ↔ ß) → ((α → ß) ∧ (ß → α))`
- **De Morgan's laws**
  - `¬(α ∧ ß) → (¬α ∨ ¬ß)`
  - `¬(α ∨ ß) → (¬α ∧ ¬ß)`
- **distributive property**
  - `(α ∧ (ß ∨ Γ)) → ((α ∧ ß) ∨ (α ∧ Γ))`
  - `(α ∨ (ß ∧ Γ)) → ((α ∨ ß) ∧ (α ∨ Γ))`
- **unit resolution rule**: `((α ∨ ß) ∧ ¬α) → ß`
  - generalization: `((α ∨ ß) ∧ (¬α ∨ Γ)) → (ß ∨ Γ)`



## Theorem Proving as a form of Search Problem

- *initial state*: starting knowledge base
- *actions*: inference rules
- *transition model*: new knowledge base after inference (output of `result` function)
- *goal test*: check statement we're trying to prove
- *path cost function*: number of steps in proof



## Conversion to Conjunctive Normal Form

- eliminate biconditionals, with the *biconditional elimination* inference rule
- eliminate implications, with the *implication elimination* inference rule
- move `¬` inwards using *De Morgan's Laws*
- use *distributive laws* to distribute `∨` wherever possible



## Inference by Resolution

### converting a logic statement to CNF, then using the resolution inference rules to "resolve" or "reduce" the statement

- to determine if `KB ╞ α`:
  - convert `KB ∧ ¬α` to *CNF*
  - use inference and resolution rules to "resolve" or "reduce" the statement
  - if the final product of resolution is the *empty clause*, `KB ∧ ¬α` led to a contradiction, so `KB ╞ α`
  - otherwise, if the final product is NOT the *empty clause*, `KB ∧ ¬α` did NOT lead to a contradiction, so there is no entailment (I would like to see the proof of this, because in a standard analytical proof by contradiction, *not* reaching a contradiction doesn't prove the opposite of the original statement)



## First-Order Logic

- two types of symbols:
  - **constant**:  things
  - **predicate**: functions that will either hold `true` or `false` for each constant (or constants if the function takes more than one argument)
- **quantifiers**:
  - **universal quantification**: a statement is true for all values of `x`; this is `∀` from the logic I'm familiar with
  - **existential quantification**: a statement is true for some value of `x`; this is `∃` from the logic I'm familiar with

