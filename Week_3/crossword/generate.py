import sys
from PIL import Image, ImageDraw, ImageFont
import copy
from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables  # set[str]
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self) -> None:
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in copy.deepcopy(self.domains).items():
            self.domains[variable] = {word for word in domain if len(word) == variable.length}

        return

    def revise(self, x: Variable, y: Variable) -> bool:
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False

        changes_made = False
        for x_word in copy.deepcopy(self.domains[x]):
            if not any(x_word[overlap[0]] == y_word[overlap[1]:overlap[1] + 1] for y_word in self.domains[y]):
                self.domains[x].remove(x_word)
                changes_made = True

        return changes_made

    def ac3(self, arcs: list[Variable, Variable] = None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        import time  # TODO delete this
        if not arcs:
            arcs = []
            for var1 in self.domains:
                for var2 in self.domains:
                    if var1 != var2:
                        arcs.append((var1, var2))

        while arcs:
            arc = tuple(arcs.pop(0))
            x_var, y_var = arc[0], arc[1]
            revised = self.revise(x_var, y_var)
            if not self.domains[x_var]:
                return False
            if revised:
                for var in self.domains.keys():
                    if x_var != var:
                        arcs.append((x_var, var))

        return True

    def assignment_complete(self, assignment: dict) -> bool:
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(assignment.get(variable) for variable in self.crossword.variables)

    def consistent(self, assignment: dict) -> bool:
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        correct_length = all(len(word) == variable.length for variable, word in assignment.items())
        distinct_values = len(set(assignment.values())) == len(list(assignment.values()))
        no_conflicts = True
        for x in assignment:
            for y in assignment:
                if x == y:
                    continue

                overlap = self.crossword.overlaps[x, y]
                if overlap:
                    no_conflicts = no_conflicts and assignment[x][overlap[0]] == assignment[y][overlap[1]]

        return correct_length and distinct_values and no_conflicts

    def order_domain_values(self, var: Variable, assignment: dict) -> list[str]:
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return sorted(list(self.domains[var]), key=lambda x: self.eliminated_neighbors(assignment, var, x))

    def eliminated_neighbors(self, assignment: dict, var: Variable, word) -> int:
        """Given <var> and a single <word> from its domain, returns how many options among <var>'s neighbors would be
        eliminated"""
        count = 0
        for neighbor in self.crossword.neighbors(var):
            if neighbor in assignment:
                continue

            overlap = self.crossword.overlaps[var, neighbor]
            if overlap:
                for neighbor_option in self.domains[neighbor]:
                    count += bool(word[overlap[0]] != neighbor_option[overlap[1]:overlap[1] + 1])

        return count

    def select_unassigned_variable(self, assignment: dict) -> Variable:
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = {var: len(self.domains[var]) for var in self.domains if var not in assignment}
        min_domain_vars = [var for var in unassigned if len(self.domains[var]) == min(unassigned.values())]
        if len(min_domain_vars) == 1:
            return min_domain_vars[0]

        return sorted(min_domain_vars, key=lambda x: len(self.crossword.neighbors(x)), reverse=True)[0]

    def backtrack(self, assignment: dict) -> None | dict:
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments  # TODO UNCOMMENT TEST LINES BELOW
    structure = sys.argv[1]
    # structure = ".\data\structure0.txt"
    words = sys.argv[2]
    # words = ".\data\words1.txt"
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
