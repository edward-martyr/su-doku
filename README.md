# `su-doku`: a Sudoku solver and generator in Python

## Installation

```bash
python -m pip install git+https://github.com/edward-martyr/su-doku
```

## Usage

```pycon
>>> from su_doku import Sudoku
>>> # Let's create a unique 9x9 Sudoku puzzle with 50 empty cells
>>> puzzle = Sudoku.generate_unique(9, 50)
>>> print(puzzle)
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 0 0 2 │ 0 8 0 │ 7 0 0 ┃
┃ 0 0 0 │ 0 0 0 │ 5 2 0 ┃
┃ 0 5 0 │ 7 2 6 │ 8 9 1 ┃
┃───────┼───────┼───────┃
┃ 0 6 0 │ 4 0 1 │ 0 0 2 ┃
┃ 2 0 0 │ 0 0 3 │ 0 4 0 ┃
┃ 0 0 0 │ 0 5 0 │ 0 7 0 ┃
┃───────┼───────┼───────┃
┃ 0 3 0 │ 1 9 0 │ 4 5 0 ┃
┃ 0 0 6 │ 0 0 0 │ 0 0 0 ┃
┃ 5 1 0 │ 0 3 0 │ 0 8 0 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
>>> # Solve the puzzle
>>> sol = puzzle.solve()
>>> print(sol)
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 1 9 2 │ 3 8 5 │ 7 6 4 ┃
┃ 6 8 7 │ 9 1 4 │ 5 2 3 ┃
┃ 4 5 3 │ 7 2 6 │ 8 9 1 ┃
┃───────┼───────┼───────┃
┃ 8 6 5 │ 4 7 1 │ 9 3 2 ┃
┃ 2 7 9 │ 8 6 3 │ 1 4 5 ┃
┃ 3 4 1 │ 2 5 9 │ 6 7 8 ┃
┃───────┼───────┼───────┃
┃ 7 3 8 │ 1 9 2 │ 4 5 6 ┃
┃ 9 2 6 │ 5 4 8 │ 3 1 7 ┃
┃ 5 1 4 │ 6 3 7 │ 2 8 9 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Documentation

See <https://www.nyoeghau.com/su-doku>.
