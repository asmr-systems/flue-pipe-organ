import math
import cadquery as cq
from dataclasses import dataclass
import rectpack

@dataclass
class Dimensions:
    """ all defaults in mm """
    stock_thickness: float = 9.53
    stock_width: float = 1219.2
    stock_height: float = 609.6
    pipe_part_thickness: float = stock_thickness
    upper_lip_height: float = 100
    inner_width: float = 20
    pipe_length: float = 500
    foot_cavity_height: float = 80
    dado_width: float = 6
    dado_depth: float = 6
    foot_hole_dia: float = 19 # 19 mm for 3/4" dowel, 28.5 mm diam of 1.1/8" dowel
    air_band_thickness: float = 1
    aperature: float = 4
    lip_grade_degrees: float = 30 # 30 for softer rounder tone, 45 for brighter
    stopper_dowel_dia: float = 12.7 # for 1/2" dowel
    stopper_felt_tolerance: float = 1

class Part:
    name: str
    dimensions: Dimensions = Dimensions()
    cad = None
    generate_cad_fn = None
    generate_cam_fn = None

    def __init__(
            self,
            name: str,
            dimensions: Dimensions,
            generate_cad_fn,
            generate_cam_fn
    ):
        self.name = name
        self.dimensions = dimensions
        self.generate_cad_fn = generate_cad_fn
        self.generate_cam_fn = generate_cam_fn

        self.generate_cad()

    def generate_cad(self, show=False):
        self.cad = self.generate_cad_fn(self.dimensions)
        if show:
            show_object(self.cad, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})

    def generate_cam(self, job):
        return self.generate_cam_fn(self, job)

    def bounding_box(self):
        if self.cad != None:
            return self.cad.val().BoundingBox()
        return None

    def width(self):
        return self.bounding_box().xlen

    def height(self):
        return self.bounding_box().ylen

    def show(self):
        show_object(self.cad, options={"alpha":0.5, "color": (0.3, 0.3, 0.3)})


class Layout:
    parts = []
    name: str
    wp = None

    def __init__(self, name, parts, width, height):
        self.parts = parts
        self.name = name
        self.width = width
        self.height = height
        self.wp = cq.Workplane("XY")
        for p in self.parts:
            self.wp.add(p.cad)

    def export_step(self, step_dir='.'):
        cq.exporters.export(self.wp.vals(), f'{step_dir}/{self.name}.step')

    def generate_cam_job(self, show=False):
        from ocp_freecad_cam import Endmill, Job
        from ocp_freecad_cam.api import Stock

        combined_solids = self.wp.combineSolids()
        top = self.parts[0].cad.faces(">Z").workplane()
        job = Job(top, combined_solids)
        for p in self.parts:
            job = p.generate_cam(job)
        # TODO export freecad or gcode.
        if show:
            show_object(job.show())

    def show(self, show_bounding_box=False):
        if show_bounding_box:
            box = (
                cq.Workplane("XY")
                .rect(self.width, self.height)
            )
            box = box.translate((self.width/2,self.height/2,0))
            show_object(box)
        show_object(self.wp, options={"alpha":0.5, "color": (0.3, 0.3, 0.3)})


def pipe_back_cad(D):
    total_height = D.pipe_length + D.foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.pipe_part_thickness,
            total_height,
        )
        .extrude(D.pipe_part_thickness)
        # right dado groove
        .faces(">Z")
        .workplane(origin=((D.inner_width+D.dado_width)/2, 0, 0))
        .rect(D.dado_width, total_height)
        .cutBlind(-D.dado_depth)
        # left dado groove
        .faces(">Z")
        .workplane(origin=(-(D.inner_width+D.dado_width)/2, 0, 0))
        .rect(D.dado_width, total_height)
        .cutBlind(-D.dado_depth)
        # foot cavity dado groove
        .faces(">Z")
        .workplane(origin=(
            0,
            -total_height/2 + D.foot_cavity_height - D.dado_width/2,
            0
        ))
        .rect(D.inner_width, D.dado_width)
        .cutBlind(-D.dado_depth)
    )
    return part

def get_extended_open_pocket_face(pocket_face, solid, extend_by=0):
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE
    from OCP.BRepTools import BRepTools
    from OCP.TopExp import TopExp
    from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
    from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE

    # get all edges of pocket face
    edges = pocket_face.edges()

    open_edges = []
    # get all adjacent faces of each edge
    for edge in edges.vals():
        mapping = TopTools_IndexedDataMapOfShapeListOfShape()
        # print(dir(TopExp))
        TopExp.MapShapesAndAncestors_s(
            solid.val().wrapped,
            TopAbs_EDGE,
            TopAbs_FACE,
            mapping
        )
        faces = []
        if mapping.Contains(edge.wrapped):
            faces = list(mapping.FindFromKey(edge.wrapped))

        print(faces)

        # A pocket bottom edge should have:
        # - This bottom face
        # - At least 1 wall face
        # If only bottom face → edge is open
        wall_faces = [
            f for f in faces
            if not f.IsSame(pocket_face.val().wrapped)
        ]
        print(wall_faces)
        if len(wall_faces) == 0:
            open_edges.append(e)

    print(open_edges)
    pass

def pipe_back_cam(part, job):
    tool = Endmill(diameter="1 mm")
    profile_shape = part.cad.faces("<Z")
    pocket_shape = part.cad.faces(">Z[1]")

    p = get_extended_open_pocket_face(pocket_shape, part.cad, extend_by=2)

    # ---- STEP 1: Extract the outer wire ----
    outer_wire = pocket_shape.val().outerWire()
    # ---- STEP 2: Offset the wire in 2D ----
    # offset2D(distance) → expands a planar wire
    expanded_wire = outer_wire.offset2D(2.0)
    # ---- STEP 3: Rebuild a face from the new wire ----
    pocket_shape = cq.Face.makeFromWires(expanded_wire[0])
    # TODO we need to be able to cut the existing shape or something....
    return (
        job
        .profile(profile_shape, tool)
        .pocket(pocket_shape, tool, pattern="zigzag_offset")
    )

def pipe_side_cad(D, right_side=False):
    total_height = D.pipe_length + D.foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.dado_depth,
            total_height,
        )
        .extrude(D.pipe_part_thickness)
        # back dado groove
        .faces(">Z")
        .workplane(
            origin=(
                (-1 if not right_side else 1) * (D.inner_width+D.dado_depth)/2,
                0,
                0
            )
        )
        .rect(D.dado_depth, total_height)
        .cutBlind(-(D.pipe_part_thickness-D.dado_width))
        # front dado groove
        .faces(">Z")
        .workplane(
            origin=(
                (1 if not right_side else -1) * (D.inner_width+D.dado_depth)/2,
                (D.foot_cavity_height+D.upper_lip_height)/2,
                0)
        )
        .rect(D.dado_depth, total_height-D.upper_lip_height-D.foot_cavity_height)
        .cutBlind(-(D.pipe_part_thickness-D.dado_width))
    )
    return part

def pipe_side_cam(part, job):
    tool = Endmill(diameter="1 mm")
    profile_shape = part.cad.faces("<Z")
    return job.profile(profile_shape, tool)

def pipe_front_cad(D):
    total_height = D.pipe_length + D.foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.pipe_part_thickness,
            D.pipe_length-D.upper_lip_height,
        )
        .extrude(D.pipe_part_thickness)
        # left dado groove
        .faces(">Z")
        .workplane(origin=((D.inner_width+D.dado_width)/2,0,0))
        .rect(D.dado_width, D.pipe_length-D.upper_lip_height)
        .cutBlind(-D.dado_depth)
        # right dado groove
        .faces(">Z")
        .workplane(origin=(-(D.inner_width+D.dado_width)/2,0,0))
        .rect(D.dado_width, D.pipe_length-D.upper_lip_height)
        .cutBlind(-D.dado_depth)
    )
    return part

def pipe_front_cam(part, job):
    return job

def pipe_languid_cad(D):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(D.inner_width, D.inner_width+D.dado_depth)
        .extrude(D.pipe_part_thickness)
        # dado
        .faces("<Y")
        .workplane(origin=(0,0,D.dado_width/2))
        .rect(D.inner_width, D.dado_width)
        .extrude(D.dado_depth)
    )
    return part

def pipe_languid_cam(part, job):
    return job

def pipe_foot_base_cad(D):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.pipe_part_thickness,
            D.inner_width+2*D.pipe_part_thickness,
        )
        .extrude(D.pipe_part_thickness-D.dado_depth)
        # non-dado face
        .faces(">Z")
        .workplane()
        .rect(D.inner_width, D.inner_width)
        .extrude(D.dado_depth)
        # foot base hole
        .faces(">Z")
        .workplane()
        .circle(D.foot_hole_dia/2)
        .cutThruAll()
    )
    return part

def pipe_foot_base_cam(part, job):
    return job

def pipe_upper_lip_cad(D):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.pipe_part_thickness,
            D.foot_cavity_height+D.upper_lip_height,
        )
        .extrude(D.pipe_part_thickness-D.dado_depth)
        # cut out channel opening
        .faces(">Z")
        .workplane(origin=(
            0,
            -(D.aperature/2 + (D.upper_lip_height-D.foot_cavity_height)/2 + D.pipe_part_thickness),
            0
        ))
        .rect(D.inner_width, D.aperature)
        .cutThruAll()
        # aperature
        .faces(">Z")
        .workplane(origin=(
            0,
            -(-D.aperature/2 + (D.upper_lip_height-D.foot_cavity_height)/2),
            0
        ))
        .rect(D.inner_width, D.aperature)
        .cutThruAll()
        # inset for languid
        .faces(">Z")
        .tag("upper_lip_face")
        .workplane(origin=(
            0,
            -(D.upper_lip_height+D.foot_cavity_height)/2 + (D.foot_cavity_height-D.aperature-D.pipe_part_thickness)/2,
            0
        ))
        .rect(D.inner_width, D.foot_cavity_height-D.aperature-D.pipe_part_thickness)
        .extrude(D.dado_depth)
        # upper lip wedge
        .faces(tag="upper_lip_face")
        .workplane(origin=(
            0,
            (D.upper_lip_height - D.aperature)/2 - (D.upper_lip_height-D.foot_cavity_height)/2 + D.aperature,
            0
        ))
        .rect(D.inner_width, D.upper_lip_height - D.aperature)
        .extrude(D.dado_depth)
    )

    # wedge
    wedge_length = D.pipe_part_thickness/math.tan(D.lip_grade_degrees*math.pi/180)
    pts = [(0,0), (D.pipe_part_thickness, 0), (D.pipe_part_thickness, wedge_length)]
    wedge_part = (
       cq.Workplane(
           "ZY",
           origin=(
               D.inner_width/2,
            -(-D.aperature/2 + (D.upper_lip_height-D.foot_cavity_height)/2) + D.aperature/2,
               0)
       )
        .polyline(pts)
        .close()
        .extrude(D.inner_width)
    )

    part = part.cut(wedge_part)
    return part

def pipe_upper_lip_cam(part, job):
    return job

def pipe_face_cad(D):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width+2*D.pipe_part_thickness,
            D.foot_cavity_height,
        )
        .extrude(D.pipe_part_thickness)
        # channel
        .faces(">Z")
        .workplane(origin=(
            0,
            D.foot_cavity_height/2 - (D.aperature+D.pipe_part_thickness)/2,
            0
        ))
        .rect(D.inner_width, D.aperature+D.pipe_part_thickness)
        .cutBlind(-D.air_band_thickness)
    )
    return part

def pipe_face_cam(part, job):
    return job

def pipe_stopper_cad(D):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            D.inner_width-D.stopper_felt_tolerance,
            D.inner_width-D.stopper_felt_tolerance,
        )
        .extrude(D.pipe_part_thickness)
        # dowel hole
        .faces(">Z")
        .workplane()
        .circle(D.stopper_dowel_dia/2)
        .cutBlind(-D.pipe_part_thickness*0.75)
    )
    return part

def pipe_stopper_cam(part, job):
    return job

def layout_parts(parts, stock_width, stock_height, step_dir=".", margin_mm=15):
    packer = rectpack.newPacker(
        pack_algo=rectpack.SkylineMwf,
        sort_algo=rectpack.SORT_SSIDE,
        rotation=True
    )
    for idx, p in enumerate(parts):
        packer.add_rect(
            math.ceil(p.width()) + margin_mm*2,
            math.ceil(p.height()) + margin_mm*2,
            rid=idx
        )
    packer.add_bin(stock_width, stock_height, count=float("inf"))
    packer.pack()

    layouts = []
    for b in range(len(packer)):
        arranged_parts = []
        for i in range(len(packer[b])):
            p = parts[packer[b][i].rid]
            x = packer[b][i].x # bottom-left corner
            y = packer[b][i].y # bottom-left corner
            w = packer[b][i].width
            h = packer[b][i].height
            old_w = math.ceil(p.width()) + margin_mm*2
            if old_w == h:
                p.cad = p.cad.rotate((0, 0, 0), (0, 0, 1), 90)
            p.cad = p.cad.translate((w/2 + x, h/2 + y, 0))
            arranged_parts.append(p)
        layouts.append(Layout(f'layout_{b}', arranged_parts, stock_width, stock_height))

    return layouts

    # # TODO translate all parts so they fit on a stock piece
    # wp = (cq.Workplane("XY")
    #       .add(back)
    #       .add(right_side)
    # )
    # cq.exporters.export(wp.vals(), f'{step_dir}/combined.step')

    # TODO Okay, i think this is the move:
    # layout parts, and hold onto references to the moved parts.
    # then for each moved part, run appropriate selectors in order
    # to define the CAM workpath for each moved part,
    # then add operations to the CAM job from the selected shape from
    # the shape
    # from ocp_freecad_cam import Endmill, Job
    # from ocp_freecad_cam.api import Stock
    # profile_shape1 = back.faces("<Z")
    # profile_shape2 = right_side.faces("<Z")
    # top = back.faces(">Z").workplane()
    # # stock = Stock(50, 50, 50, 50, 0, 50)
    # tool = Endmill(diameter="1 mm")
    # job = (
    #     Job(top, wp.combineSolids())
    #     .profile(profile_shape1, tool)
    #     .profile(profile_shape2, tool)
    # )
    # show_object(job.show())


def generate(
        pipe_id,
        D = Dimensions(),
        save=False,
        step_dir=".",
        save_assembly=False,
        show_assembly=False,
        exploded_by=0.0,
):
    back = Part("back", D, pipe_back_cad, pipe_back_cam)
    right_side = Part("right_side", D, lambda d : pipe_side_cad(d, right_side=True), pipe_side_cam)
    left_side = Part("left_side", D, lambda d : pipe_side_cad(d, right_side=False), pipe_side_cam)
    front = Part("front", D, pipe_front_cad, pipe_front_cam)
    languid = Part("languid", D, pipe_languid_cad, pipe_languid_cam)
    foot_base = Part("foot_base", D, pipe_foot_base_cad, pipe_foot_base_cam)
    upper_lip = Part("upper_lip", D, pipe_upper_lip_cad, pipe_upper_lip_cam)
    face = Part("face", D, pipe_face_cad, pipe_face_cam)
    stopper = Part("stopper", D, pipe_stopper_cad, pipe_stopper_cam)

    parts = [
        back,
        right_side,
        left_side,
        front,
        languid,
        foot_base,
        #upper_lip,
        face,
        stopper
    ]

    if save_assembly:
        assembly = cq.Assembly()
        assembly.add(
            back.cad,
            name=back.name,
            color=cq.Color(0.92, 0.67, 0.97, 0.3)
        )
        assembly.add(
            right_side.cad,
            name=right_side.name,
            color=cq.Color(1.0, 0.94, 0.4, 0.3),
            loc=cq.Location(
                D.inner_width/2,
                0,
                D.inner_width/2+D.pipe_part_thickness + exploded_by*1,
                0, 90, 0
            )
        )
        assembly.add(
            left_side.cad,
            name=left_side.name,
            color=cq.Color(1.0, 0.94, 0.4, 0.3),
            loc=cq.Location(
                -D.inner_width/2,
                0,
                D.inner_width/2+D.pipe_part_thickness + exploded_by*1,
                0, -90, 0
            )
        )
        assembly.add(
            front.cad,
            name=front.name,
            color=cq.Color(0.44, 0.94, 0.4, 0.3),
            loc=cq.Location(
                0,
                 (D.foot_cavity_height+D.upper_lip_height)/2,
                D.pipe_part_thickness*2 + D.inner_width + exploded_by*2,
                0, 180, 0
            )
        )
        assembly.add(
            languid.cad,
            name=languid.name,
            color=cq.Color(0.44, 0.94, 0.9, 0.3),
            loc=cq.Location(
                0,
                -D.pipe_length/2 + D.foot_cavity_height/2,
                ((D.inner_width+D.dado_depth)/2 - D.pipe_part_thickness) + D.pipe_part_thickness*2 + exploded_by*2,
                90, 0, 0
            )
        )
        assembly.add(
            foot_base.cad,
            name=foot_base.name,
            color=cq.Color(0.74, 0.44, 0.1, 0.3),
            loc=cq.Location(
                0,
                -D.pipe_length/2 - D.foot_cavity_height/2 - (D.pipe_part_thickness-D.dado_depth),
                (D.inner_width/2 - D.pipe_part_thickness) + D.pipe_part_thickness*2 + exploded_by*2,
                -90, 0, 0
            )
        )
        assembly.add(
            upper_lip.cad,
            name=upper_lip.name,
            color=cq.Color(0.94, 0.94, 0.1, 0.3),
            loc=cq.Location(
                0,
                -(D.pipe_length + D.foot_cavity_height)/2 + (D.foot_cavity_height+D.upper_lip_height)/2,
                D.pipe_part_thickness*2 + D.inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            face.cad,
            name=face.name,
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                -(D.pipe_length)/2,
                D.pipe_part_thickness*3 + D.inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            stopper.cad,
            name=stopper.name,
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                (D.pipe_length)/2,
                D.pipe_part_thickness + D.inner_width/2 + exploded_by*2,
                -90, 0, 0
            )
        )

        assembly.export(f'{step_dir}/{pipe_id}_assembly.step')
        if show_assembly:
            show_object(assembly)

    layouts = layout_parts(
        parts,
        D.stock_width,
        D.stock_height,
        step_dir=step_dir
    )

    for idx, l in enumerate(layouts):
        # l.show(show_bounding_box=True)
        # l.generate_cam_job(show=True)
        if save:
            cq.exporters.export(l.wp.vals(), f'{step_dir}/{pipe_id}_layout_{idx}.step')



# generate(save=True, show_assembly=False, exploded_by=0)
