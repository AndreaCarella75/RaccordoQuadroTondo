"""
freecad_bridge.py

Bridge tra la mesh generata in FreeCAD e il motore di unfolding.

Uso:

    import freecad_bridge
    mesh = freecad_bridge.mesh_from_freecad("Raccordo_Radiale")

Restituisce un oggetto TriangleMesh compatibile con unfold.py
"""

import Mesh
from unfold import TriangleMesh, Vec3


def mesh_from_freecad(object_name="Raccordo_Radiale"):
    """
    Cerca un oggetto Mesh nel documento attivo di FreeCAD
    e lo converte in una TriangleMesh.
    """
    import FreeCAD as App

    doc = App.ActiveDocument
    if doc is None:
        raise RuntimeError("Nessun documento FreeCAD attivo.")

    obj = doc.getObject(object_name)
    if obj is None:
        raise RuntimeError(f"Oggetto '{object_name}' non trovato.")

    if not hasattr(obj, "Mesh"):
        raise RuntimeError(f"L'oggetto '{object_name}' non contiene una Mesh.")

    fcmesh = obj.Mesh

    mesh = TriangleMesh()

    vertex_map = {}

    def key(v):
        return (
            round(v.x, 9),
            round(v.y, 9),
            round(v.z, 9)
        )

    for facet in fcmesh.Facets:
        ids = []

        for p in facet.Points:
            k = key(p)

            if k not in vertex_map:
                idx = mesh.add_vertex(
                    Vec3(p.x, p.y, p.z)
                )
                vertex_map[k] = idx

            ids.append(vertex_map[k])

        mesh.add_triangle(ids[0], ids[1], ids[2])

    mesh.build_connectivity()

    return mesh


if __name__ == "__main__":

    try:
        m = mesh_from_freecad()

        print("Vertici :", len(m.vertices))
        print("Triangoli:", len(m.triangles))

    except Exception as e:
        print(e)
