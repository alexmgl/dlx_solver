from src.dlx_solver.sudoku import SudokuBoard

very_hard_board = [
    [0, 0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 3, 5, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 3],
    [0, 5, 0, 0, 0, 0, 0, 9, 0],
    [7, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 0, 0, 4, 1, 0, 0, 0, 0],
    [9, 2, 0, 0, 0, 0, 0, 0, 0]
]

board = SudokuBoard(very_hard_board)
board.solve(verbose=True)


board = SudokuBoard.generate_board(num_holes=10)
board.solve(verbose=True)


