# DLX Solver

**DLX Solver** is a **Python implementation** of Donald Knuth's **Dancing Links (DLX)** algorithm, an efficient method for solving exact cover problems. This repository applies DLX to **9x9 Sudoku puzzles**, transforming them into an exact cover problem and leveraging Knuth’s algorithm for fast and optimal solutions.

![Language](https://img.shields.io/badge/language-Python-blue)
![Version](https://img.shields.io/badge/version-v0.1.0-brightgreen)

---

## 📥 Installation
To install the package directly from GitHub, use:

```bash
pip install git+https://github.com/alexmgl/dlx_solver.git
```

## 🚀 Usage

### 1️⃣ Solving a Custom Sudoku Puzzle
You can input a Sudoku puzzle as a 9×9 grid (0 represents empty cells) and solve it:
```python
from dlx_solver import SudokuBoard

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
```

### 2️⃣ Generating and Solving a Random Puzzle
You can generate a random Sudoku board with a specified number of empty cells and solve it:
```python
from dlx_solver import SudokuBoard

board = SudokuBoard.generate_board(num_holes=10)

board.solve(verbose=True)
```

## 📜 Example Output
Once solved, the board is printed in a formatted Sudoku grid:
```md
Attempting to solve the board:
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │   ║   │   │   ║   │ 1 │ 2 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │ 3 │ 5 ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │ 1 ║   │   │   ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║ 6 │   │   ║   │   │ 3 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 5 │   ║   │   │   ║   │ 9 │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 7 │   │   ║   │   │ 1 ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │   │   ║ 5 │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║ 4 │ 1 │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 9 │ 2 │   ║   │   │   ║   │   │   ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

Solution found:
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║ 5 │ 8 │ 9 ║ 7 │ 6 │ 4 ║ 3 │ 1 │ 2 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 2 │ 6 │ 7 ║ 1 │ 3 │ 5 ║ 9 │ 4 │ 8 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 3 │ 4 │ 1 ║ 9 │ 2 │ 8 ║ 7 │ 5 │ 6 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 4 │ 1 │ 2 ║ 6 │ 5 │ 9 ║ 8 │ 7 │ 3 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 6 │ 5 │ 3 ║ 2 │ 8 │ 7 ║ 1 │ 9 │ 4 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 7 │ 9 │ 8 ║ 3 │ 4 │ 1 ║ 6 │ 2 │ 5 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 1 │ 3 │ 4 ║ 8 │ 9 │ 2 ║ 5 │ 6 │ 7 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 8 │ 7 │ 5 ║ 4 │ 1 │ 6 ║ 2 │ 3 │ 9 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 9 │ 2 │ 6 ║ 5 │ 7 │ 3 ║ 4 │ 8 │ 1 ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝

```

Copyright (c) 2025 Alex Gardner