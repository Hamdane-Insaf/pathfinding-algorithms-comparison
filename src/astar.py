"""Algorithme heuristique : A* avec distance de Manhattan."""
import heapq

from .grid import manhattan, neighbors, reconstruct


def astar(grid, start, goal, moves, weight=1.0):
    """weight = 1 : heuristique admissible (chemin optimal).
    weight > 1 : heuristique non admissible (plus rapide, chemin possiblement plus long)."""
    counter = 0                         # départage les égalités dans le tas
    open_heap = [(weight * manhattan(start, goal), counter, start)]
    g = {start: 0}
    parent = {start: None}
    closed = set()
    explored = []
    while open_heap:
        _, _, node = heapq.heappop(open_heap)
        if node in closed:
            continue
        closed.add(node)
        explored.append(node)
        if node == goal:
            return reconstruct(parent, goal), explored
        for nb in neighbors(grid, node, moves):
            new_g = g[node] + 1
            if new_g < g.get(nb, float("inf")):
                g[nb] = new_g
                parent[nb] = node
                counter += 1
                f = new_g + weight * manhattan(nb, goal)
                heapq.heappush(open_heap, (f, counter, nb))
    return None, explored
