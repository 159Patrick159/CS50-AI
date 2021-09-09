import sys
import math
import copy
from typing import Container, NewType
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
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
        from PIL import Image, ImageDraw, ImageFont
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
        font = ImageFont.truetype("arial.ttf", 80)
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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        a = self.enforce_node_consistency()
        b = self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate through all variables in domain
        for v in self.domains:
            # Collect a word from variable's domain
            domain_copy = self.domains[v].copy()
            for word in domain_copy:
                # Check if word matches variable lenght
                if v.length != len(word):
                    # If not remove word from variable's domain
                    self.domains[v].remove(word)
            

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        flag = False
        # Check if the two variables overlap;
        if self.crossword.overlaps[x,y] is None:
            # If they don't overlap then we dont need to make them arc consistent
            return(flag)
        else:  
            # Collect the indeces of the character where both variables overlap
            i = self.crossword.overlaps[x,y][0]
            j = self.crossword.overlaps[x,y][1]
            # Create array to keep track of which words are consitent with Y's domain
            candidates = []
            # Iterare through Y's domain of words
            for word2 in self.domains[y]:
                # Iterate through X's domain of words
                for word1 in self.domains[x]:
                    # Check for words that are consitent with Y's domain
                    if word1[i] == word2[j]:
                        # Add word to candidates array
                        candidates.append(word1)
                        # Mark that we have done revisions
                        flag = True  
            # Eliminate duplicates
            candidates_set = set(candidates)
            # Update the domain of X to the list of viable candidates
            self.domains[x] = list(candidates_set)
        # Return flag
        return(flag)


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Check if arcs is none
        if arcs is None:
            # Create a queue with arcs
            queue = []
            # Iterate through variables
            for x in self.domains:
                for y in self.domains:
                    # Ignore the same variable
                    if x == y:
                        continue
                    # Check if there is overlap between two variables
                    elif self.crossword.overlaps[x,y]:
                        # Add this arc to our queue
                        queue.append((x,y))
        else:
            # Otherwise use the existing arcs as our queue
            queue = list(arcs)
        # Start dequeing each arc in queue
        while len(queue) != 0:
            # Deque the arc
            X = queue[0][0]
            Y = queue[0][1]
            a = self.domains[X]
            r = self.domains[Y] 
            if (X,Y) in queue:
                queue.remove((X,Y))
            if (Y,X) in queue:
                queue.remove((Y,X))
            # Check if both variables are arc consistent
            if self.revise(X,Y):
                # If the domain of x is empty then we cant make x arc consistent
                if len(self.domains[X]) == 0:
                    return(False)
                neighbors = self.crossword.neighbors(X)
                neighbors_minusY = copy.deepcopy(neighbors)
                if Y in neighbors_minusY:
                    neighbors_minusY.remove(Y)
                    for Z in neighbors_minusY:
                        queue.append((Z,X))
                else:
                    for Z in neighbors:
                        queue.append((Z,X))
        return(True)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        a = self.crossword.variables
        # Check if we have assigned all variables
        if len(assignment) != len(self.crossword.variables):
            return False
        # Check every variables was assigned one word
        available_variables = self.crossword.variables
        for variabel in available_variables:
            # The type of the value would be a string instead of a list if there is only
            # one word assigned
            if type(assignment[variabel]) != str:
                return False
        # Return true if both conditions are met
        return True
            

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Iterate through variables in assignment dict
        for var in assignment:
            # Collect word from variable
            word = assignment[var]
            # Check for unary constraint to be met
            for i in range(len(assignment)):
                # If constraint is not met return false
                if len(word) != var.length:
                    return(False)

        # Check for repeated words
        words = list(assignment.values())
        words_set = set(words)
        # Sets eliminate repeated elements
        if len(words) != len(words_set):
            return(False)
        
        # Ensure arc consistency
        for var1 in assignment:
            neighbors = self.crossword.neighbors(var1)
            for var2 in neighbors:
                # Check if arc consistency holds
                if not self.revise(var1,var2):
                    # If arc consistency is not met return false
                    return(False)
        # If word has been assigned we need to check the word holds for arc-consistency with
        # other words in domains of the othe variables.
        for var in assignment:
            # If the value from the dictionary is a str then it means a word was assigned
            if type(assignment[var]) == str:
                for neighbor in self.crossword.neighbors(var):
                    assigned_word = assignment[var]
                    i = self.crossword.overlaps[var,neighbor][0]
                    j = self.crossword.overlaps[var,neighbor][1]
                    # Make variable consistent with neigbors that are
                    # assigned
                    if neighbor in assignment:
                        if type(assignment[neighbor]) == str:
                            neighbor_word = assignment[neighbor]
                            if neighbor_word[j] != assigned_word[i]:
                                return False
                    
        return(True)

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Find all neigbors for var
        neighbors = self.crossword.neighbors(var)
        # Select only the neighbors that have been left unassigned
        available_neighbors = [n for n in neighbors if n not in assignment.keys()]
        # Gather all words availble in var's domain
        var_domain = self.domains[var]
        # Create a dict where we will keep track of the words and how much it constraints the problem
        least_val_heu_raw = {}
        # Iterate through the words in var's domain
        for word in var_domain:
            word_constraint = 0
            # Iterate through var's neighbors
            for neighbor in available_neighbors:
                # Check if word leads to any constraits
                if word in self.domains[neighbor]:
                    word_constraint += 1 
            # Update dictionary with word and number of constraints
            least_val_heu_raw.update({word:word_constraint})
        # Sort the raw heuristc using dict comprehension
        least_val_heu = {word: rank for word, rank in sorted(least_val_heu_raw.items(), key=lambda item: item[1])}
        order_words = [word for word in least_val_heu.keys()]
        # Return words in order of heuristic
        return(order_words)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        available_variables = [var for var in self.crossword.variables if var not in assignment.keys()]
        #available_variables = self.crossword.variables
        best_variable = None
        # Create a value for the smallest number of elements in the domain
        best = math.inf
        # Iterate through the available variables
        for var in available_variables:
            var_domain = self.domains[var]
            # If var's domain is less then the best than we assign it to be the best option 
            if len(var_domain) < best:
                best = len(var_domain)
                best_variable = var
            # If there is a tie between best var and current bar we pick the one with more neighbors
            elif len(var_domain) == best:
                best_var_neighbors = self.crossword.neighbors(best_variable)
                current_var_neighbors = self.crossword.neighbors(var)
                # Compare the number of neighbors for each variable
                if len(best_var_neighbors) < len(current_var_neighbors):
                    # If current variable has more neighbors then its a better option
                    best_variable = var
        return(best_variable)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        # Check if we have finished assigning word to variables
        if self.assignment_complete(assignment):
            return(assignment)
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)
        flag = False
        # Iterate through best possible values for variable
        for word in self.order_domain_values(var,assignment):
            # Make assignment
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = word
            # Make sure assignment is consistent
            if self.consistent(new_assignment):
                # Gather variable's neighbors
                var_neighbors = self.crossword.neighbors(var)
                arcs = [(var,arc) for arc in var_neighbors]
                # Check for arc consistency and update arc's domain
                inference = self.ac3(arcs)
                # If inference was a success assign new domains to neighbors
                if inference:
                    flag = True
                    for neighbor in var_neighbors:
                        assignment[neighbor] = self.domains[neighbor]
                # Call backtrack recursively
                result = self.backtrack(new_assignment)
                # If backtrack isnt able to find a consistent assignment it will return None
                if result != None:
                    return(result)
            # If assignment is not consitent we need to remove last assignment
            new_assignment.pop(var)
            # See if inferences were made
            if flag:
                # Eliminate infereces made from previous assignment
                for neighbor in var_neighbors:
                    assignment.pop(neighbor)
        # Finally if backtrack finishes its recursive calling and doesnt finish assigning then
        # return None
        return(None)
            
                    
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
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