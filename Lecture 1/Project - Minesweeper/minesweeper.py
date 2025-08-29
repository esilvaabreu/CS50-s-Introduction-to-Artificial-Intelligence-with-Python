import itertools
import random


class Minesweeper():
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
                row.append(False)    # Cells that do not contain mines are represented as False
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True   # Mines are represented as True

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

                # Update count if cell in bounds (board lower and upper limits) and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:   # Check if the cell has value True (mine)
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines   # Returns True or False


class Sentence():
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

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) > 0 and self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # Creates an empty set to keep track of the cells that will be removed
        cells_to_remove = set()

        # Loop through each cell inside a sentence and update cell_to_remove if necessary
        for known_cell in self.cells:
            if known_cell == cell:
                cells_to_remove.add(cell)
            continue

        # Updates the sentence cells and count
        self.cells -= cells_to_remove
        self.count -= len(cells_to_remove)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # Creates an empty set to keep track of the cells that will be removed
        cells_to_remove = set()

        # Loop through each cell inside a sentence and update cell_to_remove if necessary
        for known_cell in self.cells:
            if known_cell == cell:
                cells_to_remove.add(cell)
            continue

        # Updates the sentence cells
        self.cells -= cells_to_remove

class MinesweeperAI():
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

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def update_knowledge(self):
        """
        Checks all the sentences that are part of the knowledge and try to find if is possible
        to conclude if there are any mines or safe cells
        """

        changed = True
        while changed:
            changed = False
            knowledge_copy = self.knowledge.copy()

            for sentence in knowledge_copy:
                # Skip if sentence was removed
                if sentence not in self.knowledge:
                    continue

                # Remove empty sentences
                if len(sentence.cells) == 0:
                    self.knowledge.remove(sentence)
                    changed = True
                    continue

                # Mine detection
                mines = sentence.known_mines()
                if mines:
                    for cell in mines.copy():
                        self.mark_mine(cell)
                    changed = True
                    continue

                # Safe detection
                safes = sentence.known_safes()
                if safes:
                    for cell in safes.copy():
                        self.mark_safe(cell)
                    changed = True
                    continue

                # Subset inference
                for other_sentence in knowledge_copy:
                    if (sentence != other_sentence and
                            other_sentence.cells.issubset(sentence.cells) and
                            other_sentence in self.knowledge and
                            sentence in self.knowledge):

                        # Create new cells and count based on the inference
                        new_cells = sentence.cells - other_sentence.cells
                        new_count = sentence.count - other_sentence.count

                        if new_cells and new_count >= 0:
                            # Update the sentence
                            sentence.cells = new_cells
                            sentence.count = new_count
                            changed = True
                            break  # Restart while loop

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        new_sentence = Sentence(set(), count)

        # Loop through the boundaries of the cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add the boundaries of the cell to the sentence
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_sentence.cells.add((i, j))

        # Check for known mines and safe cells
        for cell in new_sentence.cells.copy():
            if cell in self.mines:
                new_sentence.cells.remove(cell)
                new_sentence.count -= 1

            if cell in self.safes:
                new_sentence.cells.remove(cell)

        self.knowledge.append((new_sentence))

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # 5) loop through all the sentences and create new ones based if one is a subset of the other
        self.update_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for safe_cell in self.safes:
            if safe_cell not in self.moves_made and safe_cell not in self.mines:
                self.moves_made.add(safe_cell)
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        """

        # Create a cell with only the available cells
        grid_available = {(i, j) for i in range(8) for j in range(8)} - self.moves_made - self.mines

        # Check if there is a possible move to be made in the available grid and return a random cell or None
        return None if len(grid_available) == 0 else random.choice(list(grid_available))
