import cadquery as cq

height = 60.0
width = 80.0
thickness = 10.0
diameter = 22.0

result = (cq.Workplane("XY")
          .box(height, width, thickness)
          .edges("|Z")
          .fillet(20)
          .faces(">Z")
          .workplane()
          .hole(diameter)
)

highlight = result.faces('>Z')

show_object(result)
show_object(highlight,'highlight',options=dict(alpha=1.0,color=(1.,0,0)))
