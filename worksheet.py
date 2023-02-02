from modules.open_digraph import *
from random import randrange, randint


def print_matrix(mat: list[list[int]]) -> None:
    for i in range(len(mat)):
        print(mat[i])


def random_int_list(n: int, bound: int) -> list[int]:
    """
    Return a list containing `n` integers between 0 and `bound` (included).

    Parameters
    ----------
    n: int
          The size of the list.

    bound: int
          The maximum value that the elements of the list can take (included).

    Return
    ----------
    A list containing `n` integers randomly chosen between 0 and `bound` (included).
    """
    return [randrange(0, bound+1, 1) for _ in range(n)]


def random_int_matrix(n: int, bound: int, null_diag: bool = True) -> list[list[int]]:
    """
    Return a `n*n` matrix whose elements are integers randomly chosen between 0 and `bound` (included).

    Parameters
    ----------
    n: int
          The size of the matrix.

    bound: int
          The maximum value that the elements of the matrix can take (included).

    null_diag: bool
          If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

    Return
    ----------
    A matrix (list[list[int]]) containing `n*n` integers randomly chosen between 0 and `bound` (included).
    """
    res: list[list[int]] = [random_int_list(n, bound) for _ in range(n)]
    if null_diag:
        for i in range(n):
            res[i][i] = 0
    return res


def random_symetric_int_matrix(n: int, bound: int, null_diag: bool = True) -> list[list[int]]:
    """
    Return a `n*n` symetric matrix whose elements are integers randomly chosen between 0 and `bound` (included).

    Parameters
    ----------
    n: int
          The size of the matrix.

    bound: int
          The maximum value that the elements of the matrix can take (included).

    null_diag: bool
          If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

    Return
    ----------
    A symetric matrix (list[list[int]]) containing `n*n` integers randomly chosen between 0 and `bound` (included).
    """
    res: list[list[int]] = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            res[j][i] = res[i][j]
    return res


def random_oriented_int_matrix(n: int, bound: int, null_diag: bool = True) -> list[list[int]]:
    """
    Return a `n*n` matrix of an oriented graph whose elements are integers randomly chosen between 0 and `bound` (included).

    Parameters
    ----------
    n: int
          The size of the matrix.

    bound: int
          The maximum value that the elements of the matrix can take (included).

    null_diag: bool
          If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

    Return
    ----------
    A matrix (list[list[int]]) of an oriented graph containing `n*n` integers randomly chosen between 0 and `bound` (included).
    """
    res: list[list[int]] = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            # to add randomness, otherwise it would always be a triangular matrix
            if randint(0, 1):
                if res[i][j] != 0:
                    res[j][i] = 0
            else:
                if res[j][i] != 0:
                    res[i][j] = 0
    return res


def random_triangular_int_matrix(n: int, bound: int, null_diag: bool = True) -> list[list[int]]:
    """
    Return a `n*n` triangular matrix of an oriented acyclic graph whose elements are integers randomly chosen between 0 and `bound` (included).

    Parameters
    ----------
    n: int
          The size of the matrix.

    bound: int
          The maximum value that the elements of the matrix can take (included).

    null_diag: bool
          If set to `True`, the diagonal will contain only 0, otherwise it will contain random integers like every other element.

    Return
    ----------
    A triangular matrix (list[list[int]]) of an oriented acyclic graph containing `n*n` integers randomly chosen between 0 and `bound` (included).
    """
    res: list[list[int]] = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i):
            res[i][j] = 0
    return res


def graph_from_adjacency_matrix(mat: list[list[int]]) -> open_digraph:
    """
    Return the open_digraph corresponding to the adjacency matrix `mat`.

    Parameters
    ----------
    mat: list[list[int]]
          The square matrix we want a graph of.

    Return
    ----------
    The open_digraph corresponding to the adjacency matrix `mat`.
    """
    G: open_digraph = open_digraph(
        [], [], [node(i, f"{i}", {}, {}) for i in range(len(mat))])
    for i in range(len(mat)):
        for j in range(len(mat)):
            G.add_edges([(i, j) for _ in range(mat[i][j])])

    return G


for f in [random_int_matrix, random_symetric_int_matrix, random_oriented_int_matrix, random_triangular_int_matrix]:
    mat = f(5, 5)
    g = graph_from_adjacency_matrix(mat)
    assert mat == g.adjacencyMatrix()
