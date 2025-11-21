import math
import cadquery as cq
from dataclasses import dataclass

@dataclass
class Defaults:
    """ all defaults in mm """
    stock_thickness: float = 9.53
    inner_width: float = 20
    pipe_length: float = 500
    upper_lip_pipe_length: float = 50
    foot_cavity_height: float = 40
    dado_width: float = 3
    dado_depth: float = 4
    foot_hole_dia: float = 10
    air_band_thickness: float = 1
    aperature: float = 4
    lip_grade_degrees: float = 20
    stopper_dowel_dia: float = 13
    stopper_felt_tolerance: float = 1

def pipe_back(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        pipe_length=Defaults.pipe_length,
        foot_cavity_height=Defaults.foot_cavity_height,
        dado_width=Defaults.dado_width,
        dado_depth=Defaults.dado_depth,
        show=False
):
    total_height = pipe_length + foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*stock_thickness,
            total_height,
        )
        .extrude(stock_thickness)
        # right dado groove
        .faces(">Z")
        .workplane(origin=((inner_width+dado_width)/2, 0, 0))
        .rect(dado_width, total_height)
        .cutBlind(-dado_depth)
        # left dado groove
        .faces(">Z")
        .workplane(origin=(-(inner_width+dado_width)/2, 0, 0))
        .rect(dado_width, total_height)
        .cutBlind(-dado_depth)
        # foot cavity dado groove
        .faces(">Z")
        .workplane(origin=(
            0,
            -total_height/2 + foot_cavity_height - dado_width/2,
            0
        ))
        .rect(inner_width, dado_width)
        .cutBlind(-dado_depth)
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_side(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        pipe_length=Defaults.pipe_length,
        upper_lip_pipe_length=Defaults.upper_lip_pipe_length,
        foot_cavity_height=Defaults.foot_cavity_height,
        dado_width=Defaults.dado_width,
        dado_depth=Defaults.dado_depth,
        right_side=False,
        show=False
):
    total_height = pipe_length + foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*dado_depth,
            total_height,
        )
        .extrude(stock_thickness)
        # back dado groove
        .faces(">Z")
        .workplane(
            origin=(
                (-1 if not right_side else 1) * (inner_width+dado_depth)/2,
                0,
                0
            )
        )
        .rect(dado_depth, total_height)
        .cutBlind(-(stock_thickness-dado_width))
        # front dado groove
        .faces(">Z")
        .workplane(
            origin=(
                (1 if not right_side else -1) * (inner_width+dado_depth)/2,
                (foot_cavity_height+upper_lip_pipe_length)/2,
                0)
        )
        .rect(dado_depth, total_height-upper_lip_pipe_length-foot_cavity_height)
        .cutBlind(-(stock_thickness-dado_width))
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_front(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        pipe_length=Defaults.pipe_length,
        upper_lip_pipe_length=Defaults.upper_lip_pipe_length,
        foot_cavity_height=Defaults.foot_cavity_height,
        dado_width=Defaults.dado_width,
        dado_depth=Defaults.dado_depth,
        show=False,
):
    total_height = pipe_length + foot_cavity_height
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*stock_thickness,
            pipe_length-upper_lip_pipe_length,
        )
        .extrude(stock_thickness)
        # left dado groove
        .faces(">Z")
        .workplane(origin=((inner_width+dado_width)/2,0,0))
        .rect(dado_width, pipe_length-upper_lip_pipe_length)
        .cutBlind(-dado_depth)
        # right dado groove
        .faces(">Z")
        .workplane(origin=(-(inner_width+dado_width)/2,0,0))
        .rect(dado_width, pipe_length-upper_lip_pipe_length)
        .cutBlind(-dado_depth)
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_languid(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        dado_width=Defaults.dado_width,
        dado_depth=Defaults.dado_depth,
        show=False
):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(inner_width, inner_width+dado_depth)
        .extrude(stock_thickness)
        # dado
        .faces("<Y")
        .workplane(origin=(0,0,dado_width/2))
        .rect(inner_width, dado_width)
        .extrude(dado_depth)
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_foot_base(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        dado_depth=Defaults.dado_depth,
        foot_hole_dia=Defaults.foot_hole_dia,
        show=False
):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*stock_thickness,
            inner_width+2*stock_thickness,
        )
        .extrude(stock_thickness-dado_depth)
        # non-dado face
        .faces(">Z")
        .workplane()
        .rect(inner_width, inner_width)
        .extrude(dado_depth)
        # foot base hole
        .faces(">Z")
        .workplane()
        .circle(foot_hole_dia/2)
        .cutThruAll()
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_upper_lip(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        upper_lip_pipe_length=Defaults.upper_lip_pipe_length,
        foot_cavity_height=Defaults.foot_cavity_height,
        dado_depth=Defaults.dado_depth,
        aperature=Defaults.aperature,
        lip_grade_degrees=Defaults.lip_grade_degrees,
        show=False
):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*stock_thickness,
            foot_cavity_height+upper_lip_pipe_length,
        )
        .extrude(stock_thickness-dado_depth)
        # cut out channel opening
        .faces(">Z")
        .workplane(origin=(
            0,
            -(aperature/2 + (upper_lip_pipe_length-foot_cavity_height)/2 + stock_thickness),
            0
        ))
        .rect(inner_width, aperature)
        .cutThruAll()
        # aperature
        .faces(">Z")
        .workplane(origin=(
            0,
            -(-aperature/2 + (upper_lip_pipe_length-foot_cavity_height)/2),
            0
        ))
        .rect(inner_width, aperature)
        .cutThruAll()
        # inset for languid
        .faces(">Z")
        .tag("upper_lip_face")
        .workplane(origin=(
            0,
            -(upper_lip_pipe_length+foot_cavity_height)/2 + (foot_cavity_height-aperature-stock_thickness)/2,
            0
        ))
        .rect(inner_width, foot_cavity_height-aperature-stock_thickness)
        .extrude(dado_depth)
        # upper lip wedge
        .faces(tag="upper_lip_face")
        .workplane(origin=(
            0,
            (upper_lip_pipe_length - aperature)/2 - (upper_lip_pipe_length-foot_cavity_height)/2 + aperature,
            0
        ))
        .rect(inner_width, upper_lip_pipe_length - aperature)
        .extrude(dado_depth)
        # wedge
    )

    wedge_length = stock_thickness/math.tan(lip_grade_degrees*math.pi/180)
    pts = [(0,0), (stock_thickness, 0), (stock_thickness, wedge_length)]
    wedge_part = (
       cq.Workplane(
           "ZY",
           origin=(
               inner_width/2,
            -(-aperature/2 + (upper_lip_pipe_length-foot_cavity_height)/2) + aperature/2,
               0)
       )
        .polyline(pts)
        .close()
        .extrude(inner_width)
    )

    part = part.cut(wedge_part)

    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_face(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        foot_cavity_height=Defaults.foot_cavity_height,
        air_band_thickness=Defaults.air_band_thickness,
        aperature=Defaults.aperature,
        show=False
):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width+2*stock_thickness,
            foot_cavity_height,
        )
        .extrude(stock_thickness)
        # channel
        .faces(">Z")
        .workplane(origin=(
            0,
            foot_cavity_height/2 - (aperature+stock_thickness)/2,
            0
        ))
        .rect(inner_width, aperature+stock_thickness)
        .cutBlind(-air_band_thickness)
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part

def pipe_stopper(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        stopper_dowel_dia=Defaults.stopper_dowel_dia,
        stopper_felt_tolerance=Defaults.stopper_felt_tolerance,
        show=False
):
    part = (
        # stock
        cq.Workplane("XY")
        .rect(
            inner_width-stopper_felt_tolerance,
            inner_width-stopper_felt_tolerance,
        )
        .extrude(stock_thickness)
        # dowel hole
        .faces(">Z")
        .workplane()
        .circle(stopper_dowel_dia/2)
        .cutBlind(-stock_thickness*0.75)
    )
    if show:
        show_object(part, options={"alpha":0.5, "color": (1.0, 1.0, 1.0)})
    return part


def generate(
        stock_thickness=Defaults.stock_thickness,
        inner_width=Defaults.inner_width,
        pipe_length=Defaults.pipe_length,
        upper_lip_pipe_length=Defaults.upper_lip_pipe_length,
        foot_cavity_height=Defaults.foot_cavity_height,
        dado_width=Defaults.dado_width,
        dado_depth=Defaults.dado_depth,
        foot_hole_dia=Defaults.foot_hole_dia,
        air_band_thickness=Defaults.air_band_thickness,
        aperature=Defaults.aperature,
        lip_grade_degrees=Defaults.lip_grade_degrees,
        stopper_dowel_dia=Defaults.stopper_dowel_dia,
        stopper_felt_tolerance=Defaults.stopper_felt_tolerance,
        show_assembly=False,
        save=False,
        exploded_by=10.0,
):
    back = pipe_back(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        pipe_length=pipe_length,
        foot_cavity_height=foot_cavity_height,
        dado_width=dado_width,
        dado_depth=dado_depth,
    )
    right_side = pipe_side(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        pipe_length=pipe_length,
        upper_lip_pipe_length=upper_lip_pipe_length,
        foot_cavity_height=foot_cavity_height,
        dado_width=dado_width,
        dado_depth=dado_depth,
        right_side=True
    )

    left_side = pipe_side(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        pipe_length=pipe_length,
        upper_lip_pipe_length=upper_lip_pipe_length,
        foot_cavity_height=foot_cavity_height,
        dado_width=dado_width,
        dado_depth=dado_depth,
        right_side=False
    )

    front = pipe_front(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        pipe_length=pipe_length,
        upper_lip_pipe_length=upper_lip_pipe_length,
        foot_cavity_height=foot_cavity_height,
        dado_width=dado_width,
        dado_depth=dado_depth
    )
    languid = pipe_languid(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        dado_width=dado_width,
        dado_depth=dado_depth
    )
    foot_base = pipe_foot_base(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        dado_depth=dado_depth,
        foot_hole_dia=foot_hole_dia
    )
    upper_lip = pipe_upper_lip(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        upper_lip_pipe_length=upper_lip_pipe_length,
        foot_cavity_height=foot_cavity_height,
        dado_depth=dado_depth,
        aperature=aperature,
        lip_grade_degrees=lip_grade_degrees
    )
    face = pipe_face(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        foot_cavity_height=foot_cavity_height,
        air_band_thickness=air_band_thickness,
        aperature=aperature
    )
    stopper = pipe_stopper(
        stock_thickness=stock_thickness,
        inner_width=inner_width,
        stopper_dowel_dia=stopper_dowel_dia,
        stopper_felt_tolerance=stopper_felt_tolerance,
    )

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
                inner_width/2,
                0,
                inner_width/2+stock_thickness + exploded_by*1,
                0, 90, 0
            )
        )
        assembly.add(
            left_side,
            name="left_side",
            color=cq.Color(1.0, 0.94, 0.4, 0.3),
            loc=cq.Location(
                -inner_width/2,
                0,
                inner_width/2+stock_thickness + exploded_by*1,
                0, -90, 0
            )
        )
        assembly.add(
            front,
            name="front",
            color=cq.Color(0.44, 0.94, 0.4, 0.3),
            loc=cq.Location(
                0,
                 (foot_cavity_height+upper_lip_pipe_length)/2,
                stock_thickness*2 + inner_width + exploded_by*2,
                0, 180, 0
            )
        )
        assembly.add(
            languid,
            name="languid",
            color=cq.Color(0.44, 0.94, 0.9, 0.3),
            loc=cq.Location(
                0,
                -pipe_length/2 + foot_cavity_height/2,
                ((inner_width+dado_depth)/2 - stock_thickness) + stock_thickness*2 + exploded_by*2,
                90, 0, 0
            )
        )
        assembly.add(
            foot_base,
            name="foot_base",
            color=cq.Color(0.74, 0.44, 0.1, 0.3),
            loc=cq.Location(
                0,
                -pipe_length/2 - foot_cavity_height/2 - (stock_thickness-dado_depth),
                (inner_width/2 - stock_thickness) + stock_thickness*2 + exploded_by*2,
                -90, 0, 0
            )
        )
        assembly.add(
            upper_lip,
            name="upper_lip",
            color=cq.Color(0.94, 0.94, 0.1, 0.3),
            loc=cq.Location(
                0,
                -(pipe_length + foot_cavity_height)/2 + (foot_cavity_height+upper_lip_pipe_length)/2,
                stock_thickness*2 + inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            face,
            name="face",
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                -(pipe_length)/2,
                stock_thickness*3 + inner_width + exploded_by*2,
                180, 0, 180
            )
        )
        assembly.add(
            stopper,
            name="stopper",
            color=cq.Color(0.04, 0.34, 0.7, 0.3),
            loc=cq.Location(
                0,
                (pipe_length)/2,
                stock_thickness + inner_width/2 + exploded_by*2,
                -90, 0, 0
            )
        )

        show_object(assembly)

generate(show_assembly=True, exploded_by=0)
# pipe_stopper(show=True)
