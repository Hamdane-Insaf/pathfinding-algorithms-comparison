"""Visualisations : grille 2D, nuage 3D interactif, graphiques en barres."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def plot_2d(grid, start, goal, res_bfs, res_astar, filename):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    cmap = ListedColormap(["white", "black", "lightskyblue", "gold"])
    for ax, name, r in zip(axes, ["BFS", "A*"], [res_bfs, res_astar]):
        img = grid.copy()
        for c in r["explored"]:
            img[c] = 2
        for c in r["path"]:
            img[c] = 3
        ax.imshow(img, cmap=cmap, vmin=0, vmax=3)
        ax.scatter(start[1], start[0], c="green", s=80, marker="s", label="Départ")
        ax.scatter(goal[1], goal[0], c="red", s=80, marker="*", label="Arrivée")
        ax.set_title(f"{name}\n{r['n_explored']} nœuds explorés, "
                     f"chemin = {r['length']} pas, {r['time_ms']:.2f} ms")
        ax.set_xticks([]); ax.set_yticks([])
    axes[0].legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"-> {filename}")


def plot_3d(grid, start, goal, res_bfs, res_astar, filename):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "scatter3d"}, {"type": "scatter3d"}]],
        subplot_titles=[
            f"BFS : {res_bfs['n_explored']} nœuds, chemin {res_bfs['length']}",
            f"A* : {res_astar['n_explored']} nœuds, chemin {res_astar['length']}",
        ],
    )
    walls = np.argwhere(grid == 1)
    for col, r in enumerate([res_bfs, res_astar], start=1):
        ex = np.array(r["explored"])
        pa = np.array(r["path"])
        fig.add_trace(go.Scatter3d(
            x=walls[:, 0], y=walls[:, 1], z=walls[:, 2], mode="markers",
            marker=dict(size=2, color="black", opacity=0.08),
            name="Murs", showlegend=(col == 1)), row=1, col=col)
        fig.add_trace(go.Scatter3d(
            x=ex[:, 0], y=ex[:, 1], z=ex[:, 2], mode="markers",
            marker=dict(size=3, color="deepskyblue", opacity=0.25),
            name="Explorés", showlegend=(col == 1)), row=1, col=col)
        fig.add_trace(go.Scatter3d(
            x=pa[:, 0], y=pa[:, 1], z=pa[:, 2], mode="lines+markers",
            line=dict(color="red", width=6), marker=dict(size=3, color="red"),
            name="Chemin", showlegend=(col == 1)), row=1, col=col)
        for pt, color, nm in [(start, "green", "Départ"), (goal, "purple", "Arrivée")]:
            fig.add_trace(go.Scatter3d(
                x=[pt[0]], y=[pt[1]], z=[pt[2]], mode="markers",
                marker=dict(size=8, color=color), name=nm,
                showlegend=(col == 1)), row=1, col=col)
    fig.update_layout(title="BFS vs A* en 3D", height=650)
    fig.write_html(filename)
    print(f"-> {filename}")


def plot_bars(df, filename, title):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, col in zip(axes, ["Nœuds explorés", "Temps (ms)", "Longueur chemin"]):
        df.pivot(index="Grille", columns="Algo", values=col).plot.bar(ax=ax, rot=0)
        ax.set_title(col)
        ax.set_xlabel("")
    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"-> {filename}")
