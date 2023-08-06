from numbers import Integral
from typing import TypeVar

from numpy import dtype, generic, integer, ndarray, uint8

_T = TypeVar("_T", bound=generic, covariant=True)

PyInt = int | Integral
NpInt = integer
Unsigned = uint8
Int = PyInt | NpInt
Matrix = ndarray[tuple[int, int], dtype[_T]]
Array = ndarray[tuple[int], dtype[_T]]

__all__ = ["Array", "Int", "Matrix", "NpInt", "PyInt", "Unsigned"]
