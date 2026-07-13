"""
unfold_engine.py

Motore di unfolding della mesh triangolare.

Dipendenze:
    unfold.py
"""

from collections import deque
from unfold import Unfolder


class UnfoldEngine:
    """
    Coordina il processo di unfolding della mesh.
    """

    def __init__(self, mesh):
        self.mesh = mesh
        self.unfolder = Unfolder(mesh)

    def run(self):
        """
        Avvia lo sviluppo completo.
        """
        self.mesh.build_connectivity()

        self.unfolder.place_first_triangle()

        queue = deque()
        queue.append(0)

        visited = {0}

        while queue:

            current = queue.popleft()

            tri = self.mesh.triangles[current]

            for nb in tri.neighbours:

                if nb in visited:
                    continue

                # tenta di sviluppare il triangolo adiacente
                self.unfolder.unfold_triangle(nb)

                visited.add(nb)
                queue.append(nb)

        return self.unfolder.flat_vertices

    def statistics(self):

        return {
            "triangles": len(self.mesh.triangles),
            "developed": len(self.unfolder.done),
            "vertices2d": len(self.unfolder.flat_vertices),
        }


if __name__ == "__main__":

    print("Modulo unfold_engine.py")
    print("Questo file deve essere richiamato da main.py")
