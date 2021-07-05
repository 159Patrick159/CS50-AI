import itertools
import random
import copy

def Resolve(Knowledge):
    temp_KB = []
    for sentence1 in Knowledge:
        for sentence2 in Knowledge:
            # Ignore the the same sentence
            if sentence1 == sentence2:
                continue
            # Check if sentence 2 is a subset of sentence 1
            if sentence2.cells.issubset(sentence1.cells):
                # If the cell is a subset then we create a new sentence
                temp_cells = sentence1.cells - sentence2.cells
                temp_count = sentence1.count - sentence2.count
                temp_sentence = Sentence(temp_cells,temp_count)
                temp_KB.append(temp_sentence)
            # Check if sentence 1 is a subset of sentence 2
            elif sentence1.cells.issubset(sentence2.cells):
                temp_cells = sentence2.cells - sentence1.cells
                temp_count = sentence2.count - sentence1.count
                temp_sentence = Sentence(temp_cells,temp_count)
                temp_KB.append(temp_sentence)
    return(temp_KB)

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
        if len(self.cells) == self.count and self.count != 0:
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

    def add_knowledge(self, cell, count):
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
        # Add cell to moves set
        self.moves_made.add(cell)
        # Add cell to safe set
        self.safes.add(cell)

        cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Make sure cell is within the bounds of the board
                if 0 <= i < self.height and 0 <= j < self.width:
                    # Add cell to logical sentence
                    if ((i,j)) not in self.moves_made:
                        cells.add((i,j))
        # Create a sentence with the cells and their count
        new_knowledge = Sentence(cells,count)
        self.knowledge.append(new_knowledge)
        # Infer new sentences from our KB
        inferred_knowledge = Resolve(self.knowledge)

        # Add the known safe cells to safe set
        for sentence in inferred_knowledge:
            if sentence.known_safes():
                for cell in sentence.known_safes():
                    self.safes.add(cell)
        # Mark the safe cells from our set in our sentences  
        for sentence in inferred_knowledge:
            for cell in self.safes:
                sentence.mark_safe(cell)
        
        # Add the known mines cells to mine set
        for sentence in inferred_knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines():
                    self.mines.add(cell)
        # Mark the mine cells from our set in our sentences  
        for sentence in inferred_knowledge:
            for cell in self.mines:
                sentence.mark_mine(cell)

        # Add the known safe cells to safe set
        for sentence in self.knowledge:
            if sentence.known_safes():
                for cell in sentence.known_safes():
                    self.safes.add(cell)
        # Mark the safe cells from our set in our sentences  
        for sentence in self.knowledge:
                for cell in self.safes:
                    sentence.mark_safe(cell)
        
        # Add the known mines cells to mine set
        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines():
                    self.mines.add(cell)
        # Mark the mine cells from our set in our sentences  
        for sentence in self.knowledge:
            for cell in self.mines:
                sentence.mark_mine(cell)
            
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Look for known safe cells
        for cell in self.safes:
            # Check if cell has not been played
            if cell not in self.moves_made:
                return(cell)
        return(None)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Generate a random cell within bounds of board
        i = random.randint(0,self.height-1)
        j = random.randint(0,self.width-1)
        cell = (i,j)
        flag = True
        # If 56 moves have been made then have played all the safe cells
        if len(self.moves_made) == 56:
            return(None)
         # Check if created cell has been played or is a known mine
        while flag:
            if cell not in self.moves_made:
                if cell not in self.mines:
                    flag = False
            # Continue creating cell
            if flag:
                i = random.randint(0,self.height-1)
                j = random.randint(0,self.width-1)
                cell = (i,j)
        return (cell)


