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
        if len(self.cells) == self.count:
            return self.cells
        
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) == 0:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """   
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    safe_marking = {} # key is xy and value is why it was marked safe

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
        # adds a cell to self.mines, so the AI knows that it is a mine
        # loops over all sentences in the AI’s knowledge and informs each sentence that the cell is a mine
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

    def find_neighbors(self, cell):
        nb = set()
        for dx, dy in self.dirs:
            x = cell[0] + dx
            y = cell[1] + dy
            
            if ((x < 0) or (x >= self.width) or (y < 0) or (y >= self.height)):
                continue

            nb.add((x, y))
        return nb


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
        if cell in self.moves_made:
            print("Move already made!")
            exit(1)
        
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # mark the cell as safe
        self.safe_marking[str(cell[0]) + str(cell[1])] = "Already played"
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        nb = self.find_neighbors(cell)

        if count == 0:
            for c in nb:
                self.safe_marking[str(c[0]) + str(c[1])] = "Adjacent to zero marked move with xy=" + str(cell[0]) + str(cell[1])
                self.mark_safe(c)
        else:
            removed_cells = set()
            for x, y in nb:
                if (x, y) in self.safes:
                    removed_cells.add((x, y))
                elif (x, y) in self.mines:
                    removed_cells.add((x, y))
                    count -= 1
            for (x, y) in removed_cells:
                nb.remove((x, y))

            # checks
            if count < 0:
                print("Count < 0")
                exit(1)

            if len(nb) == 0:
                if count > 0:
                    print("Empty set has mines")
                    exit(1)
                else:
                    return
            
            self.knowledge.append(Sentence(nb, count))

            # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
            n = len(self.knowledge)
            for sen in self.knowledge[:n-1]:
                if cell in sen.cells:
                    sen.cells.remove(cell)
                    if count is None:
                        sen.count -= 1
                
            for sen in self.knowledge[:n-1]:

                if sen.count == 0:
                    continue

                intersecting_set = nb.intersection(sen.cells)
                print("intersect =", intersecting_set, ";sen.cells =", sen.cells, ";current play =", nb)
                if len(intersecting_set) == len(nb):
                    if (sen.count - count) == 0:
                        for c in (sen.cells - intersecting_set):
                            self.safe_marking[str(c[0]) + str(c[1])] = "Subtraction of sets"
                            self.mark_safe(c)
                    elif (sen.count - count) == 1:
                        if len(sen.cells - intersecting_set) == 1:
                            self.mark_mine(list(sen.cells - intersecting_set)[0])                           
                    else:
                        self.knowledge.append(Sentence(sen.cells - nb, sen.count - count))
                elif len(intersecting_set) == len(sen.cells):
                    if (count - sen.count) == 0:
                        for c in (nb - intersecting_set):
                            self.safe_marking[str(c[0]) + str(c[1])] = "Subtraction of sets"
                            self.mark_safe(c)
                    elif (count - sen.count) == 1:
                        if len(nb - intersecting_set) == 1:
                            self.mark_mine(list(nb - intersecting_set)[0])
                    else:
                        self.knowledge.append(Sentence(nb - sen.cells, count - sen.count))              

        # add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
 

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for c in self.safes:
            if c not in self.moves_made:
                return c

    def make_mine_move(self):        
        for c in self.mines:
            if c not in self.moves_made:
                return c
            
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        from random import randrange
        # print(randrange(10))
        x = randrange(self.width)
        y = randrange(self.height)
        while ((x, y)  in self.moves_made) or ((x, y) in self.mines):
            x = randrange(self.width)
            y = randrange(self.height)
            
        return (x, y)



