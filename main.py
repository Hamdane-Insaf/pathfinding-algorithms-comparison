"""
TD : Comparaison BFS (exact) vs A* (heuristique), en 2D et en 3D.

Usage :
    python main.py              # 2D + 3D
    python main.py --mode 2d
    python main.py --mode 3d
"""
import argparse
import os

from src.benchmark import benchmark
from src.grid import MOVES_2D, MOVES_3D
from src.visualization import plot_2d, plot_3d, plot_bars

TABLES = os.path.join("results", "tables")
FIGURES = os.path.join("results", "figures")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["2d", "3d", "all"], default="all")
    args = ap.parse_args()

    os.makedirs(TABLES, exist_ok=True)
    os.makedirs(FIGURES, exist_ok=True)

    if args.mode in ("2d", "all"):
        print("\n===== 2D (25 % de murs) =====")
        df, res = benchmark([(20, 20), (50, 50), (100, 100)], 0.25, MOVES_2D)
        print(df.to_string(index=False))
        df.to_csv(os.path.join(TABLES, "resultats_2d.csv"), index=False)
        plot_bars(df, os.path.join(FIGURES, "barres_2d.png"), "Comparaison 2D")
        g, s, goal = res[("50x50", "grid")]
        plot_2d(g, s, goal, res[("50x50", "BFS")], res[("50x50", "A* (Manhattan)")],
                os.path.join(FIGURES, "visu_2d.png"))

    if args.mode in ("3d", "all"):
        print("\n===== 3D (20 % de murs) =====")
        df, res = benchmark([(10, 10, 10), (20, 20, 20), (30, 30, 30)], 0.20, MOVES_3D)
        print(df.to_string(index=False))
        df.to_csv(os.path.join(TABLES, "resultats_3d.csv"), index=False)
        plot_bars(df, os.path.join(FIGURES, "barres_3d.png"), "Comparaison 3D")
        g, s, goal = res[("20x20x20", "grid")]
        plot_3d(g, s, goal, res[("20x20x20", "BFS")], res[("20x20x20", "A* (Manhattan)")],
                os.path.join(FIGURES, "visu_3d.html"))


if __name__ == "__main__":
    main()
