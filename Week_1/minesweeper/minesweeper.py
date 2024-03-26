import random
import copy


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self) -> set:
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

        return set()

    def known_safes(self) -> set:
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell) -> None:
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        return

    def mark_safe(self, cell) -> None:
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

        return


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # My additions
        self.all_cells = {(i, j) for i in range(height) for j in range(width)}
        self.subsets_pairs_used = []

    def mark_mine(self, cell: tuple[int, int]) -> None:
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

        return

    def mark_safe(self, cell: tuple[int, int]) -> None:
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        return

    def add_knowledge(self, cell: tuple[int, int], count: int) -> None:
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self._add_new_sentence_to_knowledge(cell, count)
        self._update_knowledge()

        return

    def _update_knowledge(self) -> None:
        changes_made = True
        while changes_made:
            changes_made = False

            # Mark cells as mines if that cell is in a Sentence where all cells are mines
            for sentence in copy.deepcopy(self.knowledge):
                if sentence.known_mines() == sentence.cells:
                    for cell in copy.deepcopy(sentence.cells):
                        self.mark_mine(cell)
                    changes_made = True

            # Mark cells as safe if new inferences can be reached based on the previous action of marking mines
            for sentence in copy.deepcopy(self.knowledge):
                if sentence.cells and (sentence.known_safes() == sentence.cells):
                    for cell in copy.deepcopy(sentence.cells):
                        self.mark_safe(cell)
                    changes_made = True

            # Try to create new sentences using the subset rule
            for sentence in copy.deepcopy(self.knowledge):
                if sentence.cells and self._create_new_subset_sentence(sentence):
                    changes_made = True

            # Remove empty knowledge sentences created as a result of marking safe and mine cells above
            self._remove_empty_sentences_from_knowledge()

        return

    def _create_new_subset_sentence(self, sentence1: Sentence) -> bool:
        """Tries to add new Sentences to self.knowledge based on the subset inference. Returns True if any new sentences
         were created, and false otherwise."""
        sets_created = False
        for sentence2 in self.knowledge:
            if (sentence1, sentence2) in self.subsets_pairs_used:
                continue

            if sentence2 and sentence1.cells.issubset(sentence2.cells) and (sentence1 != sentence2):
                self.subsets_pairs_used.append((sentence1, sentence2))
                new_sentence = Sentence(sentence2.cells.difference(sentence1.cells), sentence2.count - sentence1.count)
                self.knowledge.append(new_sentence)
                sets_created = True

        return sets_created

    def _remove_empty_sentences_from_knowledge(self) -> None:
        for sentence in copy.deepcopy(self.knowledge):
            if not sentence.cells:
                self.knowledge.remove(sentence)

        return

    def _add_new_sentence_to_knowledge(self, cell: tuple[int, int], count: int) -> None:
        """Creates a new Sentence to <self.knowledge> from the given <cell> and the <count> of adjacent cells that are
        mines. Takes into account the possibility that an adjacent mine may already be known, adjusts the count
        accordingly, and doesn't include that mine cell in the resulting Sentence."""
        new_cells = set()
        for neighbor_cell in self._get_neighbors(cell):
            if neighbor_cell in self.mines:
                count -= 1
            elif neighbor_cell in self.safes:
                continue
            else:
                new_cells.add(neighbor_cell)

        new_sentence = Sentence(new_cells, count)
        if new_sentence.cells:
            self.knowledge.append(new_sentence)
        return

    def _get_neighbors(self, cell: tuple[int, int]) -> set[tuple[int, int]]:
        """Returns all adjacent cell to given cell that are within the boundaries of the game's minefield"""
        neighboring_cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_cell = (cell[0] + i, cell[1] + j)
                if self._is_cell_in_game_boundaries(new_cell):
                    neighboring_cells.add(new_cell)

        return neighboring_cells

    def _is_cell_in_game_boundaries(self, cell: tuple[int, int]) -> bool:
        row = cell[0]
        column = cell[1]
        return (0 <= row < self.height) and (0 <= column < self.width)

    def make_safe_move(self) -> None | tuple[int, int]:
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        available_moves = list(self.safes.difference(self.moves_made))
        if available_moves:
            return available_moves[0]

        return None

    def make_random_move(self) -> None | tuple[int, int]:
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        already_chosen_or_mines = self.moves_made.union(self.mines)
        available_moves = list(self.all_cells.difference(already_chosen_or_mines))
        return random.choice(available_moves) if available_moves else None
