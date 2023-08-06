from __future__ import annotations

from collections import deque
from logging import getLogger
from typing import Iterator, Optional, Sequence

import numpy as np

from .typing import Array, Int, Matrix, NpInt, Unsigned

logger = getLogger(__name__)


class Sudoku(Matrix[Unsigned]):
    """
    Sudoku generator and solver class, based on ``numpy.ndarray``.
    """

    n: Unsigned
    """
    N is the number of rows and columns in the square grid.
    """
    sr: Unsigned
    """
    SR is the square root of N.
    """

    def __new__(
        cls, grid: Sequence[Sequence[Int]] | Matrix[NpInt], _verify: bool = True
    ):
        """
        Creates a new grid that represents a Sudoku game board.
        Here we assume that the grid is a square matrix of integers,
        and require that the grid can be divided into square boxes,
        i.e., the grid size is N×N, where N is a perfect square.
        """
        obj = np.array(grid, dtype=Unsigned, copy=True).view(cls)

        obj.n = Unsigned(n := obj.shape[0])
        obj.sr = round_sr = Unsigned(sr := np.sqrt(n))

        if _verify:
            assert len(obj.shape) == 2, "Grid is not two-dimensional"
            assert n == obj.shape[1], "Grid is not square"
            assert sr == round_sr, "N is not a perfect square"
            assert np.logical_and(
                0 <= obj, obj <= n
            ).all(), "Grid contains invalid digits"

        return obj

    @classmethod
    def empty(cls, n: Int):
        """
        Creates an empty grid with size N×N.
        """
        return cls(np.zeros((n, n), dtype=Unsigned))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Sudoku):
            return np.array_equal(self, other)
        else:
            return super().__eq__(other)

    def __hash__(self) -> int:  # type: ignore
        return hash((self.__class__, self.tobytes()))

    def is_safe(self, row: Int, col: Int, digit: Int) -> bool:
        """
        Checks if it is safe to place the given digit at the given position.
        """
        return (
            self.row_safe(row, digit)
            and self.col_safe(col, digit)
            and self.box_safe(row, col, digit)
        )

    def box(self, row: Int, col: Int) -> Matrix[Unsigned]:
        """
        Returns the box that contains the given position.
        """
        r = row // self.sr * self.sr
        c = col // self.sr * self.sr
        return self[r : r + self.sr, c : c + self.sr]

    def row_safe(self, row: Int, digit: Int) -> bool:
        """
        Checks if it is safe to place the given digit at the given row.
        """
        return digit not in self[row, :]

    def col_safe(self, col: Int, digit: Int) -> bool:
        """
        Checks if it is safe to place the given digit at the given column.
        """
        return digit not in self[:, col]

    def box_safe(self, row: Int, col: Int, digit: Int) -> bool:
        """
        Checks if it is safe to place the given digit at the given box.
        """
        return digit not in self.box(row, col)

    @property
    def empty_cells(self) -> Iterator[tuple[Unsigned, Unsigned]]:
        """
        Returns an iterator over all empty cells in the grid.
        """
        for row, col in np.argwhere(self == 0):
            yield row, col

    def find_empty(self) -> Optional[tuple[Unsigned, Unsigned]]:
        """
        Finds one empty cell in the grid.
        """
        return next(self.empty_cells, None)

    def candidates(self, row: Int, col: Int) -> Iterator[Unsigned]:
        """
        Returns a generator of possible candidates for the given position.
        """
        return (
            candidate
            for candidate in np.arange(1, self.n + 1, dtype=Unsigned)
            if self.is_safe(row, col, candidate)
        )

    def random_candidates(self, row: Int, col: Int) -> Array[Unsigned]:
        """
        Returns an array of possible candidates for the given position.
        """
        candidates = np.asarray(tuple(self.candidates(row, col)))
        np.random.shuffle(candidates)
        return candidates

    def solve_inplace(self) -> Optional[Sudoku]:
        """
        Solves the Sudoku puzzle in-place.
        """
        if (empty_cell := self.find_empty()) is None:
            return self
        for candidate in self.random_candidates(*empty_cell):
            self[empty_cell] = candidate
            if (solution := self.solve_inplace()) is not None:
                return solution
        self[empty_cell] = 0
        return None

    def solve_all(self) -> frozenset[Sudoku]:
        """
        Returns a set of all possible solutions to the Sudoku puzzle.
        """
        s: set[Sudoku] = set()
        self._solve_all_helper(s)
        return frozenset(s)

    def _solve_all_helper(self, solutions: set[Sudoku]) -> None:
        if (empty_cell := self.find_empty()) is None:
            solutions.add(self)
            return
        for candidate in self.candidates(*empty_cell):
            (copy := Sudoku(self, _verify=False))[empty_cell] = candidate
            copy._solve_all_helper(solutions)

    def has_solution(self) -> bool:
        """
        Checks if the Sudoku puzzle has at least one solution.
        """
        return Sudoku(self, _verify=False).solve_inplace() is not None

    def is_unique(self) -> bool:
        """
        Checks if the Sudoku puzzle has exactly one solution.
        """
        return self._is_unique_helper(set())

    def _is_unique_helper(self, solutions: set[Sudoku]) -> bool:
        if (empty_cell := self.find_empty()) is None:
            solutions.add(self)
            return len(solutions) == 1
        for candidate in self.candidates(*empty_cell):
            (copy := Sudoku(self, _verify=False))[empty_cell] = candidate
            copy._solve_all_helper(solutions)
            if len(solutions) > 1:
                return False
        return True

    @classmethod
    def generate(
        cls,
        n: Int,
        k: Int = 0,
        grid: Optional[Sequence[Sequence[Int]] | Matrix[NpInt]] = None,
    ) -> Sudoku:
        """
        Generates a Sudoku puzzle with N×N size and K empty cells.
        It first randomly generates a puzzle, or takes in a complete grid,
        then removes K cells.
        """
        if grid is None:
            sudoku = cls.empty(n)
        else:
            sudoku = cls(grid)
            if sudoku.find_empty() is not None:
                raise ValueError("Grid is not a complete Sudoku puzzle")
        assert 0 <= k <= n**2, "K must be between 0 and N²"  # type: ignore

        sudoku.solve_inplace()

        for _ in range(k):
            while True:
                row, col = np.random.randint(0, n, size=2)  # type: ignore
                if sudoku[row, col] != 0:
                    break
            sudoku[row, col] = 0

        return sudoku

    @classmethod
    def generate_unique(
        cls,
        n: Int,
        k: Int = 0,
        grid: Optional[Sequence[Sequence[Int]] | Matrix[NpInt]] = None,
        attempt_limit: Int = 1_000,
    ) -> Sudoku:
        """
        Generates a Sudoku puzzle with N×N size and K empty cells.
        It first randomly generates a puzzle, or takes in a complete grid,
        then removes K cells while ensuring that the puzzle has a unique solution.
        """
        attempts = 0
        while True:
            attempts += 1
            if attempts >= attempt_limit:
                raise RuntimeError(
                    f"Could not generate a unique Sudoku puzzle within {attempt_limit} attempts."
                )
            logger.info(f"Attempt {attempts}...")

            sudoku = cls.generate(n, k, grid)
            logger.info(f"Generated Sudoku:\n{sudoku}")

            if k == 0:
                logger.info("No empty cells, skipping uniqueness check...")
                return sudoku

            if sudoku.is_unique():
                logger.info("Unique!")
                return sudoku
            else:
                logger.info("Not unique, trying again...")

    def __str__(self) -> str:
        max_digit_length = len(str(self.n))
        output = deque(
            ("┏", "━" * (self.n * (max_digit_length + 1) + 2 * self.sr - 1), "┓\n")
        )
        for i in range(self.n):
            output.append("┃")
            for j in range(self.n):
                output.append(f"{self[i, j]:>{max_digit_length + 1}}")
                if (j + 1) % self.sr == 0 and j != self.n - 1:
                    output.append(" │")
            if (i + 1) % self.sr == 0 and i != self.n - 1:
                output.extend(
                    (
                        " ┃\n┃",
                        *(
                            ("─" * (self.sr * (max_digit_length + 1) + 1), "┼")
                            * (self.sr - 1)
                        ),
                        "─" * (self.sr * (max_digit_length + 1) + 1),
                        "┃\n",
                    )
                )
            else:
                output.append(" ┃\n")
        output.extend(
            ("┗", "━" * (self.n * (max_digit_length + 1) + 2 * self.sr - 1), "┛")
        )
        return "".join(output)


__all__ = ["Sudoku"]
