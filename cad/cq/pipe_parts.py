import cadquery as cq
from dataclasses import dataclass

@dataclass
class Defaults:
    """ all defaults in mm """
    stock_thickness: float = 9.53
    inner_width: float = 20
    pipe_length: float = 500
    upper_lip_pipe_length: float = 50
    foot_cavity_height: float = 50
    dado_width: float = 3
    dado_depth: float = 4

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
        .workplane(origin=(0, -total_height/2 + foot_cavity_height + dado_width/2, 0))
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
        cq.Workplane("XY")
        .rect(
            inner_width+2*dado_depth,
            total_height,
        )
        .extrude(stock_thickness)
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
        .faces(">Z")
        .workplane(
            origin=(
                (1 if not right_side else -1) * (inner_width+dado_depth)/2,
                foot_cavity_height+upper_lip_pipe_length,
                0)
        )
        .rect(dado_depth, total_height-upper_lip_pipe_length-foot_cavity_height)
        .cutBlind(-(stock_thickness-dado_width))
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
        show_object(assembly)

generate(show_assembly=True, exploded_by=10)
