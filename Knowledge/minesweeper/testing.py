import random
import copy
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
        # Create empty set for mines
        mines = set()
        # If the # of cells is equal to count then the cells are known mines
        if len(self.cells) == self.count:
            # Add cells to mines set
            for cell in self.cells:
                mines.add(cell)
            return(mines)


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Create emtpy set for safe cells
        safe = set()
        # if the count is zero then we know all cells are safe
        if self.count == 0:
            # Add cells to safe set
            for cell in self.cells:
                safe.add(cell)
            return(safe)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check if cell is in sentence
        if cell in self.cells:
            # Remove cell from sentence
            self.cells.remove(cell)
            # Reduce the count by one
            self.count -= 1

            

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check if cell is in sentence
        if cell in self.cells:
            # Remove cell from sentencs
            self.cells.remove(cell)

cells1 =  set()
cells1.add((1,3))
cells1.add((2,5))
cells1.add((9,2))
cells1.add((3,8))
cells1.add((2,2))
cells1.add((9,8))
x = Sentence(cells1,3)

cells2 = set()
cells2.add((9,8))
cells2.add((2,2))
y = Sentence(cells2,1)

cells3 = set()
cells3.add((9,5))
cells3.add((2,1))
cells3.add((1,1))
z = Sentence(cells3,3)
knowledge =[x,z]
board = [(1,1),(1,2),(1,3),
        (2,1),(2,3),
        (3,1),(3,2)]
board2 = [(1,1),(2,2)]
print("x: ",x)
print('y: ',y)
print('z: ',z)
KB = [x,y,z]

def Resolve(Knowledge):
    temp_KB = []
    for sentence1 in Knowledge:
        for sentence2 in Knowledge:
            # Ignore the the same sentence
            if sentence1 == sentence2:
                continue
            if sentence2.cells.issubset(sentence1.cells):
                # If the cell is a subset then we create a new sentence
                temp_cells = sentence1.cells - sentence2.cells
                temp_count = sentence1.count - sentence2.count
                temp_sentence = Sentence(temp_cells,temp_count)
                temp_KB.append(temp_sentence)
        # This process of resolution is kept only once
        break
    return(temp_KB)
for cell in z.known_mines():
    z.mark_mine(cell)
print(z)

