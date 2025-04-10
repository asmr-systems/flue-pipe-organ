# import Mesh
# import Part
# import sys

# stl_file = sys.argv[1]
# stp_file = stl_file.replace(".stl", ".stp")

# mesh = Mesh.Mesh(stl_file)
# shape = Part.Shape()
# shape.makeShapeFromMesh(mesh.Mesh.Topology, 0.1)
# # shape = Part.Shape(mesh)
# # solid = Part.Solid(shape)

# # Part.export(solid, stp_file)

import sys
import FreeCAD, Mesh, Part

stl_file = sys.argv[1]
stp_file = stl_file.replace(".stl", ".stp")

doc = FreeCAD.newDocument()
obj = Mesh.Mesh(doc.addObject('Mesh::Feature', 'Mesh'))
obj.Mesh = Mesh.read(stl_file)
solid = Part.makeSolid(Part.makeShell(obj.Mesh.Topology[0]))
Part.show(solid)
Part.export([solid], step_file)
