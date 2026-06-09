"""Lab 3.3 (optional) - tests for the TDD loop.

Demo flow:
  1. Break calc.divide (e.g. `raise NotImplementedError`) -> run `py -m pytest` -> RED.
  2. Ask Claude to make the failing test pass -> iterate -> GREEN.
"""
import pytest
from calc import add, multiply, divide


def test_add():
    assert add(2, 3) == 5


def test_multiply():
    assert multiply(4, 5) == 20


def test_divide_ok():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)
