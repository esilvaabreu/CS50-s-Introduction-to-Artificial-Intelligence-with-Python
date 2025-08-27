# {D, E, G} = 0 means that there are no mines on this cells
# {A, B, C, D, E} = 1 means that there are one mine on this cells.

# If the number of cells = count, all the cells are mines
# {A, B, C} = 3

# set2 - set1 = count2 - count1
# {A, B, C, D, E} = 2   {A, B, C} = 1   {D, E} = 1

# A, B, C etc will be a tuple of row,col representing a cell in the board
import random

from minesweeper import Sentence
from minesweeper import Minesweeper
from minesweeper import MinesweeperAI


safes = set(((4, 1), (1, 1)))
moves_made = set(((4, 1), (1, 1), (0, 1)))
mines = set(((1, 1), (2, 2), (3, 1), (3, 2), (2, 0)))

ia = MinesweeperAI()
ia.safes = safes
ia.mines = mines
ia.moves_made = moves_made

# Creates an empty set to keep track of the cells that will be removed
cells_to_remove = set()

my_sentence2 = Sentence(moves_made, 1)
my_sentence3 = Sentence(mines, 1)

knowledge = [my_sentence2, my_sentence3]

cell = (0, 1)
nearby = 3
my_sentence = Sentence(set(), nearby)

for i in range(cell[0] - 1, cell[0] + 2):
    for j in range(cell[1] - 1, cell[1] + 2):

        # Ignore the cell itself
        if (i, j) == cell:
            continue

        # Update count if cell in bounds (board lower and upper limits) and is mine
        if 0 <= i < 8 and 0 <= j < 8:
            my_sentence.cells.add((i, j))

print(my_sentence)

move = ({0, 1}, 3)
(0,0), (1, 0), (1, 1), (1, 2), (0, 2)