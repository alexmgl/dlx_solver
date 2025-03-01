from src.dlx_solver.sudoku import SudokuBoard, NoSolutionFound
import random


def is_valid(board, row, col, num):
    """Check if it's valid to place num at board[row][col]."""
    # Check the row.
    if num in board[row]:
        return False

    # Check the column.
    if num in (board[i][col] for i in range(9)):
        return False

    # Check the 3x3 sub-grid.
    box_start_row = (row // 3) * 3
    box_start_col = (col // 3) * 3
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if board[i][j] == num:
                return False
    return True


def find_empty(board):
    """Find an empty cell on the board. Return (row, col) or None if full."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def fill_board(board):
    """Recursively fill the board with valid numbers using backtracking."""
    empty = find_empty(board)
    if not empty:
        return True  # Board is complete
    row, col = empty

    numbers = list(range(1, 10))
    random.shuffle(numbers)  # Shuffle to ensure randomness
    for num in numbers:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if fill_board(board):
                return True
            board[row][col] = 0  # Reset cell if num doesn't lead to a solution
    return False


def generate_full_sudoku():
    """Generate a complete 9x9 Sudoku board."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    return board


def generate_sudoku(n_missing):
    """
    Generate a 9x9 Sudoku board with n_missing cells removed (set to 0).

    Parameters:
        n_missing (int): Number of cells to clear.

    Returns:
        list of list: A 9x9 Sudoku board with n_missing empty cells.
    """
    board = generate_full_sudoku()

    # Create a list of all positions and shuffle them.
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    # Remove n_missing cells by setting them to 0.
    for i in range(min(n_missing, 81)):
        row, col = positions[i]
        board[row][col] = 0

    return board


if __name__ == "__main__":
    # List of test cases with varying numbers of missing cells.
    test_cases = [20, 30, 40, 50, 60]

    for n_missing in test_cases:
        print("\n=======================================")
        print(f"Testing board with {n_missing} missing cells:")
        board = generate_sudoku(n_missing)
        sudoku = SudokuBoard(board)
        try:
            sudoku.solve()
            print("Solution found:")
            print(sudoku)
        except NoSolutionFound as e:
            print("Error:", e)
