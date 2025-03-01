import random
import numpy as np
from .dlx import DLXSudoku


class SudokuBoard:

    def __init__(self, board):
        """
        Initialise the Sudoku board.
        :param board: 2D list representing the board (raw input with holes, where 0 denotes an empty cell).
        """
        self.initial_board = np.array(board)  # Raw board input with holes.
        # Create a working copy that might be modified during solving.
        self.board = self.initial_board.copy()
        self.solved_board = None
        self.dim = self.initial_board.shape

    def __repr__(self):
        output = "Initial Board\n" + self.get_sudoku_string(self.initial_board)
        if self.solved_board is not None:
            output += "\nSolved Board\n" + self.get_sudoku_string(self.solved_board)
        return output


    @staticmethod
    def is_solved(board):
        """
        Static method to check if a given board is solved.
        A board is solved if every row, every column, and every 3x3 block contains
        exactly the numbers 1 to 9.
        Prints detailed error messages if issues are found.

        :param board: 2D array-like (list or numpy array) representing the board.
        :return: True if solved, False otherwise.
        """
        errors = []

        # Check rows.
        for i in range(9):
            row = board[i]
            if 0 in row:
                errors.append(f"Row {i + 1} error: contains empty cell(s).")
            counts = {}
            for num in row:
                if num != 0:
                    counts[num] = counts.get(num, 0) + 1
            for num, count in counts.items():
                if count > 1:
                    errors.append(f"Row {i + 1} error: number {num} appears {count} times.")

        # Check columns.
        for j in range(9):
            col = [board[i][j] for i in range(9)]
            if 0 in col:
                errors.append(f"Column {j + 1} error: contains empty cell(s).")
            counts = {}
            for num in col:
                if num != 0:
                    counts[num] = counts.get(num, 0) + 1
            for num, count in counts.items():
                if count > 1:
                    errors.append(f"Column {j + 1} error: number {num} appears {count} times.")

        # Check 3x3 blocks.
        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                block = []
                for i in range(block_row, block_row + 3):
                    for j in range(block_col, block_col + 3):
                        block.append(board[i][j])
                if 0 in block:
                    errors.append(
                        f"Block starting at ({block_row + 1}, {block_col + 1}) error: contains empty cell(s).")
                counts = {}
                for num in block:
                    if num != 0:
                        counts[num] = counts.get(num, 0) + 1
                for num, count in counts.items():
                    if count > 1:
                        errors.append(
                            f"Block starting at ({block_row + 1}, {block_col + 1}) error: number {num} appears {count} times.")

        if errors:
            for error in errors:
                print(error)
            return False
        return True

    def display(self):
        """
        Display the current working board in a formatted way.
        """
        for row in self.board:
            print(" ".join(str(num) for num in row))

    def _can_place(self, row, col, num):
        """
        Check if it's valid to place `num` in cell (row, col).
        """
        # Check row.
        if num in self.board[row]:
            return False
        # Check column.
        for i in range(9):
            if self.board[i][col] == num:
                return False
        # Check 3x3 block.
        block_row = 3 * (row // 3)
        block_col = 3 * (col // 3)
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def _fill_board(self):
        """
        Fill the board using backtracking to generate a complete solution.
        Returns True if the board is successfully filled.
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self._can_place(i, j, num):
                            self.board[i][j] = num
                            if self._fill_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    @classmethod
    def generate_board(cls, num_holes=5):
        # Start with an empty board.
        board = [[0 for _ in range(9)] for _ in range(9)]
        instance = cls(board)
        # Fill the board to get a complete solution.
        instance._fill_board()

        # Optionally remove cells (set them to 0) to create a puzzle.
        if num_holes > 0:
            holes = random.sample(range(81), num_holes)
            for index in holes:
                row = index // 9
                col = index % 9
                instance.board[row][col] = 0

        # Update initial_board to reflect the board with holes.
        instance.initial_board = instance.board.copy()

        return instance

    def solve(self):
        """
        Solve the Sudoku puzzle using the DLX algorithm and check the validity of the solution.
        The initial board (raw input with holes) is preserved.

        :return: Solved board if a valid solution exists, None otherwise.
        """

        solved_board = DLXSudoku(self.initial_board).solve()

        if self.is_solved(solved_board):
            self.solved_board = solved_board
        else:
            return None

        return solved_board

    @staticmethod
    def get_sudoku_string(board):
        # Define the border strings
        top_border = "╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\n"
        middle_border = "╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\n"
        block_border = "╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n"
        bottom_border = "╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝\n"

        result = top_border
        for i, row in enumerate(board):
            line = "║"
            for j, cell in enumerate(row):
                cell_str = f" {cell} " if cell != 0 else "   "
                line += cell_str
                if j == 8:
                    line += "║"
                elif (j + 1) % 3 == 0:
                    line += "║"
                else:
                    line += "│"
            result += line + "\n"
            if i == 8:
                result += bottom_border
            elif (i + 1) % 3 == 0:
                result += block_border
            else:
                result += middle_border
        return result
