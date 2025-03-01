from .dlx_node import Node


# DLX-based Sudoku solver using Dancing Links.
class DLXSudoku:

    def __init__(self, board):
        self.board = board.copy()
        self.size = 9
        self.numbers = set(range(1, 10))
        # Build the list of valid options from blank cells.
        self.options = self.get_all_options()
        # Create the universe of constraints from these options.
        self.constraints = self.get_constraint_universe()
        # Build the DLX matrix.
        self.header = Node()  # master header
        self.header.is_header = True
        self.column_list = []  # list of column header nodes
        self.column_index = {}  # mapping from constraint name to its column node
        self.create_column_headers()
        self.create_rows()
        self.solution = []  # will store chosen nodes representing a solution

    # For each blank cell, check all candidate numbers and include only valid moves.
    def valid_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    for k in self.numbers:
                        if self.is_valid_move(i, j, k):
                            moves.append((i, j, k))
        return moves

    # Standard sudoku move validation.
    def is_valid_move(self, i, j, k):
        # Row check.
        if k in self.board[i]:
            return False
        # Column check.
        for r in range(self.size):
            if self.board[r][j] == k:
                return False
        # 3x3 sub-grid check.
        box_row, box_col = 3 * (i // 3), 3 * (j // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.board[r][c] == k:
                    return False
        return True

    # Build the list of options.
    # Each option is a tuple of four constraint labels:
    #   - Cell constraint: "pij" (cell at row i, col j is filled)
    #   - Row constraint: "r{i}{k}" (row i gets value k)
    #   - Column constraint: "c{j}{k}" (col j gets value k)
    #   - Box constraint: "b{x}{k}" (box x gets value k, with x = 3*(i//3)+(j//3))
    def get_all_options(self):
        options = []
        for (i, j, k) in self.valid_moves():
            box = 3 * (i // 3) + (j // 3)
            option = (f"p{i}{j}", f"r{i}{k}", f"c{j}{k}", f"b{box}{k}")
            options.append(option)
        return options

    # Get the sorted list of all constraints.
    def get_constraint_universe(self):
        cons = set()
        for option in self.options:
            for c in option:
                cons.add(c)
        return sorted(list(cons))  # sorting fixes the order

    # Create column header nodes and link them in a circular doubly linked list.
    def create_column_headers(self):
        # Initialize header's pointers to itself.
        self.header.rlink = self.header
        self.header.llink = self.header
        # For each constraint, create a header node.
        for cons in self.constraints:
            col = Node(s=0)
            col.name = cons
            col.is_header = True
            # Insert col to the right of the current last node.
            col.llink = self.header.llink
            col.rlink = self.header
            self.header.llink.rlink = col
            self.header.llink = col
            self.column_list.append(col)
            self.column_index[cons] = col

    # Create the DLX matrix rows from the options.
    def create_rows(self):
        self.row_nodes = []  # list of lists; each inner list holds nodes for one option row
        for option_index, option in enumerate(self.options):
            first_node = None
            row_nodes = []
            for cons in option:
                col = self.column_index[cons]
                new_node = Node(c=col, s=option_index)
                # Insert new_node into the bottom of column col.
                new_node.dlink = col
                new_node.ulink = col.ulink
                col.ulink.dlink = new_node
                col.ulink = new_node
                col.s += 1
                # Link new_node horizontally into this row.
                if first_node is None:
                    first_node = new_node
                    new_node.rlink = new_node
                    new_node.llink = new_node
                else:
                    last = first_node.llink
                    last.rlink = new_node
                    new_node.llink = last
                    new_node.rlink = first_node
                    first_node.llink = new_node
                row_nodes.append(new_node)
            self.row_nodes.append(row_nodes)

    # Cover a column: remove the column header and all rows in that column.
    def cover(self, col):
        col.cover_h()  # remove col header from horizontal list
        r = col.dlink
        while r != col:
            j = r.rlink
            while j != r:
                j.cover_v()
                j.c.s -= 1
                j = j.rlink
            r = r.dlink

    # Uncover a column: restore the column header and rows.
    def uncover(self, col):
        r = col.ulink
        while r != col:
            j = r.llink
            while j != r:
                j.c.s += 1
                j.uncover_v()
                j = j.llink
            r = r.ulink
        col.uncover_h()

    # Choose the column with the fewest nodes.
    def choose_column(self):
        min_count = float('inf')
        chosen = None
        col = self.header.rlink
        while col != self.header:
            if col.s < min_count:
                min_count = col.s
                chosen = col
            col = col.rlink
        return chosen

    # Recursive search for a solution.
    def search(self):
        # If header links to itself, all constraints are satisfied.
        if self.header.rlink == self.header:
            return True
        col = self.choose_column()
        if col.s == 0:
            return False  # dead end: no option for this constraint
        self.cover(col)
        r = col.dlink
        while r != col:
            self.solution.append(r)
            # Cover all columns for nodes in row r.
            j = r.rlink
            while j != r:
                self.cover(j.c)
                j = j.rlink
            next_r = r.dlink  # store pointer to next row before recursing
            if self.search():
                return True
            # Backtrack: remove r from solution and uncover columns.
            r = self.solution.pop()
            j = r.llink
            while j != r:
                self.uncover(j.c)
                j = j.llink
            r = next_r
        self.uncover(col)
        return False

    # Fill the board with the values from the solution.
    def fill_board(self):
        for node in self.solution:
            option_index = node.s
            option = self.options[option_index]
            # option is a tuple like ("pij", "rik", "cjk", "bxk")
            # Extract row and column from the cell constraint "pij"
            cell = option[0]
            i = int(cell[1])
            j = int(cell[2])
            # Extract the value from the row constraint "rik"
            val = int(option[1][2])
            self.board[i][j] = val
        return self.board

    # Solve the sudoku: return the filled board or None if no solution.
    def solve(self):
        if self.search():
            return self.fill_board()
        else:
            return None
