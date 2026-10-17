# Réponses aux questions du TD

## 1. Pourquoi A* est plus efficace ?

BFS explore la grille de façon uniforme, couche par couche, dans toutes les directions, sans savoir où se trouve l'arrivée. A* est **guidé vers le but** : il explore en priorité les cases dont le coût total estimé `f(n) = g(n) + h(n)` est le plus faible, et laisse de côté celles qui s'éloignent de l'arrivée.

Dans nos mesures (grille 2D 100x100) : BFS explore 7430 nœuds, A* en explore 3093, soit environ 58 % de moins, avec le même chemin de 200 pas. Sur la visualisation 2D, BFS « inonde » presque toute la grille alors qu'A* se concentre sur un couloir vers l'arrivée.

Cette efficacité dépend de la grille : en 3D avec 20 % de murs, A* ne gagne que 10 % de nœuds (19783 contre 21632 sur 30x30x30), et il est même plus lent en temps (214 ms contre 143 ms), car la file de priorité coûte plus cher qu'une simple file et que les murs obligent à des détours que l'heuristique ne voit pas.

## 2. Quel rôle joue la fonction heuristique ?

L'heuristique `h(n)` estime la distance restante entre une case et l'arrivée. Elle donne à A* son « sens de l'orientation » :

- **Plus elle est précise, moins on explore de nœuds.** Avec `h = 0`, A* devient Dijkstra, et équivaut à BFS quand tous les coûts valent 1.
- **Si elle est admissible** (elle ne surestime jamais la vraie distance), A* garantit un chemin optimal. C'est le cas de la distance de Manhattan avec des déplacements à 4 voisins (2D) ou 6 voisins (3D).
- **Si elle surestime**, A* devient plus rapide mais perd la garantie d'optimalité. Avec Manhattan x2 sur la grille 100x100, A* n'explore que 313 nœuds (contre 3093) mais trouve un chemin de 222 pas au lieu de 200, soit 11 % plus long.

C'est précisément la différence « exact » contre « heuristique » du sujet : BFS garantit toujours l'optimum, A* avec une heuristique non admissible échange la qualité de la solution contre la vitesse.

## 3. Dans quel cas BFS reste-t-il préférable ?

- **Quand il n'existe pas de bonne heuristique** : graphe abstrait sans coordonnées, où l'on ne peut pas estimer la distance restante.
- **Quand l'heuristique guide peu** : grilles très denses en obstacles, comme notre cas 3D avec 20 % de murs, où A* explore presque autant que BFS pour un coût plus élevé par nœud.
- **Quand le graphe est petit ou l'arrivée très proche** : le surcoût de la file de priorité n'est pas rentable (10x10x10 : BFS 5,4 ms, A* 6,1 ms).
- **Quand on veut les distances vers tous les nœuds** depuis une source, et non un seul chemin.
- **Pour sa simplicité** : implémentation courte, comportement facile à prouver, mémoire prévisible, et optimalité garantie sans condition sur une heuristique.
