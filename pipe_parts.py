import math
import cadquery as cq
from dataclasses import dataclass

@dataclass
class Dimensions:
    """ all defaults in mm """
    stock_thickness: float = 9.53
    stock_width: float = 1219.2
    stock_height: float = 609.6
    pipe_part_thickness: float = stock_thickness
    upper_lip_height: float = 50
    inner_width: float = 20
    pipe_length: float = 500
    foot_cavity_height: float = 40
    dado_width: float = 5
    dado_depth: float = 4
    foot_hole_dia: float = 10
    air_band_thickness: float = 1
    aperature: float = 4
    lip_grade_degrees: float = 20
    stopper_dowel_dia: float = 13
    stopper_felt_tolerance: float = 1

def pipe_back(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_side(D, right_side=False, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_front(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_languid(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_foot_base(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_upper_lip(D, show=False):
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

    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_face(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_stopper(D, show=False):
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
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def layout_parts(
        back,
        right_side,
        step_dir="."
):

    back = back.translate((100, 100, 0))
    right_side = right_side.translate((-100, 0, 0))

    # TODO translate all parts so they fit on a stock piece
    wp = (cq.Workplane("XY")
          .add(back)
          .add(right_side)
    )
    cq.exporters.export(wp.vals(), f'{step_dir}/combined.step')

    # TODO Okay, i think this is the move:
    # layout parts, and hold onto references to the moved parts.
    # then for each moved part, run appropriate selectors in order
    # to define the CAM workpath for each moved part,
    # then add operations to the CAM job from the selected shape from
    # the shape
    from ocp_freecad_cam import Endmill, Job
    from ocp_freecad_cam.api import Stock
    profile_shape1 = back.faces("<Z")
    profile_shape2 = right_side.faces("<Z")
    top = back.faces(">Z").workplane()
    # stock = Stock(50, 50, 50, 50, 0, 50)
    tool = Endmill(diameter="1 mm")
    job = (
        Job(top, wp.combineSolids())
        .profile(profile_shape1, tool)
        .profile(profile_shape2, tool)
    )
    show_object(job.show())


def generate(
        D = Dimensions(),
        show_assembly=False,
        save=False,
        step_dir=".",
        exploded_by=10.0,
):
    back = pipe_back(D)
    right_side = pipe_side(D, right_side=True)
    left_side = pipe_side(D, right_side=False)
    front = pipe_front(D)
    languid = pipe_languid(D)
    foot_base = pipe_foot_base(D)
    upper_lip = pipe_upper_lip(D)
    face = pipe_face(D)
    stopper = pipe_stopper(D)

    layout_parts(
        back,
        right_side,
        step_dir=step_dir
    )

    if save:
        back.export(f'{step_dir}/back.step')

    if show_assembly:
        assembly = cq.Assembly()
        assembly.add(back,
                 name="back",
                 color=cq.Color(0.92, 0.67, 0.97, 0.3)
        )
        assembly.add(
            right_side,
            name="right_side",
            color=cq.Color(1.0, 0.94, 0.4, 0.3),
            loc=cq.Location(
                D.inner_width/2,
                0,
                D.inner_width/2+D.pipe_part_thickness + exploded_by*1,
                0, 90, 0
            )
        )
        assembly.add(
            left_side,
            name="left_side",
            color=cq.Color(1.0, 0.94, 0.4, 0.3),
            loc=cq.Location(
                -D.inner_width/2,
                0,
                D.inner_width/2+D.pipe_part_thickness + exploded_by*1,
                0, -90, 0
            )
        )
        assembly.add(
            front,
            name="front",
            color=cq.Color(0.44, 0.94, 0.4, 0.3),
            loc=cq.Location(
                0,
                 (D.foot_cavity_height+D.upper_lip_height)/2,
                D.pipe_part_thickness*2 + D.inner_width + exploded_by*2,
                0, 180, 0
            )
        )
        assembly.add(
            languid,
            name="languid",
            color=cq.Color(0.44, 0.94, 0.9, 0.3),
            loc=cq.Location(
                0,
                -D.pipe_length/2 + D.foot_cavity_height/2,
                ((D.inner_width+D.dado_depth)/2 - D.pipe_part_thickness) + D.pipe_part_thickness*2 + exploded_by*2,
                90, 0, 0
            )
        )
        assembly.add(
            foot_base,
            name="foot_base",
            color=cq.Color(0.74, 0.44, 0.1, 0.3),
            loc=cq.Location(
                0,
                -D.pipe_length/2 - D.foot_cavity_height/2 - (D.pipe_part_thickness-D.dado_depth),
                (D.inner_width/2 - D.pipe_part_thickness) + D.pipe_part_thickness*2 + exploded_by*2,
                -90, 0, 0
            )
        )
        assembly.add(
            upper_lip,
            name="upper_lip",
            color=cq.Color(0.94, 0.94, 0.1, 0.3),
            loc=cq.Location(
                0,
                -(D.pipe_length + D.foot_cavity_height)/2 + (D.foot_cavity_height+D.upper_lip_height)/2,
                D.pipe_part_thickness*2 + D.inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            face,
            name="face",
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                -(D.pipe_length)/2,
                D.pipe_part_thickness*3 + D.inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            stopper,
            name="stopper",
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                (D.pipe_length)/2,
                D.pipe_part_thickness + D.inner_width/2 + exploded_by*2,
                -90, 0, 0
            )
        )
        show_object(assembly)


generate(show_assembly=False, exploded_by=0)
