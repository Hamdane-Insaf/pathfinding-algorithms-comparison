"""Mesures : nœuds explorés, temps d'exécution, longueur du chemin."""
import time

import numpy as np
import pandas as pd

from .astar import astar
from .bfs import bfs
from .grid import make_grid


def run(algo, grid, start, goal, moves, repeats=5, **kw):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        path, explored = algo(grid, start, goal, moves, **kw)
        times.append(time.perf_counter() - t0)
    return {
        "path": path,
        "explored": explored,
        "n_explored": len(explored),
        "time_ms": 1000 * float(np.mean(times)),
        "length": len(path) - 1 if path else None,   # nombre de pas
    }


def benchmark(shapes, density, moves, seed=0):
    rows, results = [], {}
    for shape in shapes:
        grid, s, g = make_grid(shape, density, moves, seed)
        label = "x".join(map(str, shape))
        for name, algo, kw in [
            ("BFS", bfs, {}),
            ("A* (Manhattan)", astar, {}),
            ("A* (Manhattan x2)", astar, {"weight": 2.0}),
        ]:
            r = run(algo, grid, s, g, moves, **kw)
            results[(label, name)] = r
            rows.append({
                "Grille": label,
                "Algo": name,
                "Nœuds explorés": r["n_explored"],
                "Temps (ms)": round(r["time_ms"], 3),
                "Longueur chemin": r["length"],
            })
        results[(label, "grid")] = (grid, s, g)
    return pd.DataFrame(rows), results
