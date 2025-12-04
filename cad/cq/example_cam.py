# (coco|2025.12.04) i think we should try this
# (coco|2025.10.15) this experiment uses the ocp_freecad_cam python
# library to generate toolpaths which can be imported into freecad.
# the following code demonstrates doing a simple toolpath operation.
# the library isn't very well documented, but it seems workable. however,
# it doesn't look like its maintained and also it throws some errors in
# FreeCAD. however, it does generate g-code which would presumably work.
# just not sure how reliable it will be moving forward.
# see: https://github.com/voneiden/ocp-freecad-cam?tab=readme-ov-file
# see: https://ocp-freecad-cam.readthedocs.io/en/latest/examples/examples.html
# also see this for setup with a FreeCAD AppImage: https://github.com/voneiden/ocp-freecad-cam?tab=readme-ov-file#linux-appimage-installation-example-using-a-venv

import cadquery as cq

from ocp_freecad_cam import Endmill, Job
from ocp_freecad_cam.api import Stock

wp = cq.Workplane().box(50, 50, 20)

top = wp.faces(">Z").workplane()
profile_shape = wp.faces("<Z")


stock = Stock(50, 50, 50, 50, 0, 50)
tool = Endmill(diameter="1 mm")
job = Job(top, wp, stock=stock).profile(profile_shape, tool)


# a = job.show()
# show_object(a)

show_object(job.show())
show_object(wp)

job.save_fcstd("example_cam.FCstd")
