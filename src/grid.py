"""Modélisation : grille 2D/3D, voisins, heuristique, génération."""
import numpy as np

MOVES_2D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
MOVES_3D = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def neighbors(grid, node, moves):
    """Voisins libres (dans la grille et non-mur) d'une case."""
    for d in moves:
        nb = tuple(n + m for n, m in zip(node, d))
        if all(0 <= c < s for c, s in zip(nb, grid.shape)) and grid[nb] == 0:
            yield nb


def manhattan(a, b):
    """Heuristique admissible pour des déplacements à 4 (2D) ou 6 (3D) voisins."""
    return sum(abs(x - y) for x, y in zip(a, b))


def reconstruct(parent, goal):
    """Remonte les parents de l'arrivée vers le départ."""
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def make_grid(shape, density, moves, seed=0):
    """Grille aléatoire (0 = libre, 1 = mur) avec un chemin garanti."""
    from .bfs import bfs  # import local pour éviter la dépendance circulaire

    rng = np.random.default_rng(seed)
    start = tuple(0 for _ in shape)
    goal = tuple(s - 1 for s in shape)
    while True:
        grid = (rng.random(shape) < density).astype(int)
        grid[start] = 0
        grid[goal] = 0
        path, _ = bfs(grid, start, goal, moves)
        if path is not None:
            return grid, start, goal
