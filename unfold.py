"""unfold.py - Versione 0.1"""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math
EPS=1e-9
@dataclass(frozen=True)
class Vec3:
    x:float; y:float; z:float
    def __sub__(self,o): return Vec3(self.x-o.x,self.y-o.y,self.z-o.z)
    def length(self): return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
@dataclass(frozen=True)
class Vec2:
    x:float; y:float
@dataclass
class Triangle:
    id:int; v0:int; v1:int; v2:int
    neighbours:List[int]=field(default_factory=list)
    def vertices(self): return (self.v0,self.v1,self.v2)
class TriangleMesh:
    def __init__(self):
        self.vertices=[]; self.triangles=[]; self.edge_map={}
    def add_vertex(self,p): self.vertices.append(p); return len(self.vertices)-1
    def add_triangle(self,a,b,c):
        t=Triangle(len(self.triangles),a,b,c); self.triangles.append(t); return t.id
    def edge_length(self,a,b): return (self.vertices[a]-self.vertices[b]).length()
    def build_connectivity(self):
        self.edge_map.clear()
        for t in self.triangles:
            for e in ((t.v0,t.v1),(t.v1,t.v2),(t.v2,t.v0)):
                self.edge_map.setdefault(tuple(sorted(e)),[]).append(t.id)
        for t in self.triangles: t.neighbours.clear()
        for ids in self.edge_map.values():
            if len(ids)==2:
                a,b=ids
                self.triangles[a].neighbours.append(b)
                self.triangles[b].neighbours.append(a)
class Unfolder:
    def __init__(self,mesh):
        self.mesh=mesh; self.flat_vertices={}; self.done=set()
    def place_first_triangle(self):
        t=self.mesh.triangles[0]
        ab=self.mesh.edge_length(t.v0,t.v1)
        ac=self.mesh.edge_length(t.v0,t.v2)
        bc=self.mesh.edge_length(t.v1,t.v2)
        self.flat_vertices[t.v0]=Vec2(0.0,0.0)
        self.flat_vertices[t.v1]=Vec2(ab,0.0)
        x=(ab*ab+ac*ac-bc*bc)/(2.0*ab)
        y=math.sqrt(max(0.0,ac*ac-x*x))
        self.flat_vertices[t.v2]=Vec2(x,y)
        self.done.add(t.id)
if __name__=="__main__":
    print("unfold.py caricato.")
