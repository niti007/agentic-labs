"""Lab 3.3 (Claude-native) - implementation under test (TDD).

For the TDD demo, START with `divide` raising NotImplementedError (or buggy),
run the tests RED, then iterate until GREEN. The other functions are done so
the suite mostly passes and you focus on one failing case.
"""


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b
