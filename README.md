# `su-doku`: a Sudoku solver and generator in Python

## Documentation

### _class_ su_doku.Sudoku(grid: Sequence[Sequence[int | Integral | integer]] | ndarray[tuple[int, int], dtype[integer]], \_verify: bool = True)

Bases: `ndarray`[`tuple`[`int`, `int`], `dtype`[`uint8`]]

Sudoku generator and solver class, based on `numpy.ndarray`.

#### box(row: int | Integral | integer, col: int | Integral | integer)

Returns the box that contains the given position.

#### box_safe(row: int | Integral | integer, col: int | Integral | integer, digit: int | Integral | integer)

Checks if it is safe to place the given digit at the given box.

#### candidates(row: int | Integral | integer, col: int | Integral | integer)

Returns a generator of possible candidates for the given position.

#### col_safe(col: int | Integral | integer, digit: int | Integral | integer)

Checks if it is safe to place the given digit at the given column.

#### _classmethod_ empty(n: int | Integral | integer)

Creates an empty grid with size N×N.

#### _property_ empty_cells*: Iterator[tuple[numpy.uint8, numpy.uint8]]*

Returns an iterator over all empty cells in the grid.

#### find_empty()

Finds one empty cell in the grid.

#### _classmethod_ generate(n: int | Integral | integer, k: int | Integral | integer = 0, grid: Sequence[Sequence[int | Integral | integer]] | ndarray[tuple[int, int], dtype[integer]] | None = None)

Generates a Sudoku puzzle with N×N size and K empty cells.
It first randomly generates a puzzle, or takes in a complete grid,
then removes K cells.

#### _classmethod_ generate_unique(n: int | Integral | integer, k: int | Integral | integer = 0, grid: Sequence[Sequence[int | Integral | integer]] | ndarray[tuple[int, int], dtype[integer]] | None = None, attempt_limit: int | Integral | integer = 1000)

Generates a Sudoku puzzle with N×N size and K empty cells.
It first randomly generates a puzzle, or takes in a complete grid,
then removes K cells while ensuring that the puzzle has a unique solution.

#### has_solution()

Checks if the Sudoku puzzle has at least one solution.

#### is_safe(row: int | Integral | integer, col: int | Integral | integer, digit: int | Integral | integer)

Checks if it is safe to place the given digit at the given position.

#### is_unique()

Checks if the Sudoku puzzle has exactly one solution.

#### n*: uint8*

N is the number of rows and columns in the square grid.

#### random_candidates(row: int | Integral | integer, col: int | Integral | integer)

Returns an array of possible candidates for the given position.

#### row_safe(row: int | Integral | integer, digit: int | Integral | integer)

Checks if it is safe to place the given digit at the given row.

#### solve_all()

Returns a set of all possible solutions to the Sudoku puzzle.

#### solve_inplace()

Solves the Sudoku puzzle in-place.

#### sr*: uint8*

SR is the square root of N.
