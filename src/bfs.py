"""Algorithme exact : parcours en largeur (BFS)."""
from collections import deque

from .grid import neighbors, reconstruct


def bfs(grid, start, goal, moves):
    queue = deque([start])
    parent = {start: None}
    explored = []                      # ordre d'exploration (pour la visu)
    while queue:
        node = queue.popleft()
        explored.append(node)
        if node == goal:
            return reconstruct(parent, goal), explored
        for nb in neighbors(grid, node, moves):
            if nb not in parent:
                parent[nb] = node
                queue.append(nb)
    return None, explored
