#!/bin/env python

import os
import math
import click
import numpy as np
import pipe_parts
from pipe_parts import Dimensions


SPEED_OF_SOUND = 343.32 # m/s @ room temp
m_to_in = lambda x : x * 39.3701 # meters to inches

def compute_frequency(midi_note):
    """assumes equal temperament."""
    return 440.0 * np.power(2, (midi_note - 69)/12)

def compute_pipe_length(frequency):
    """calculate pipe length, L [meters]"""
    return SPEED_OF_SOUND / (2 * frequency)

def compute_pipe_inner_width(midi_note, halving_number):
    """calculate inner width of pipe, W [meters]"""
    # see https://www.mmdigest.com/Tech/pipesRecipe.html
    standard_440hz_width = compute_pipe_length(compute_frequency(69)) /12
    if midi_note == 69:
        return standard_440hz_width
    return standard_440hz_width * np.power(2, (69-midi_note)/halving_number)

def compute_flue_air_band_thickness(inner_width):
    """calculate flue air band thickness, D [meters]"""
    # see https://www.mmdigest.com/Tech/pipesRecipe.html
    return inner_width / 100

def compute_cut_up_height(freq, flue_air_band_thickness, blow_pressure, ising_number = 2):
    """calculate required cut up height (aperature) given frequency (F) [hz],
    flue air band thickness (D) [meters], blow pressure (P) [Pa], and
    optionally Ising number (defaults to 2).

    the Ising number can be varied from 2 (maximum efficiency) to
    3 or above (overblowing).
    see: https://www.mmdigest.com/Tech/isingform.html"""
    r = 1.2 # (air density) kg m-3
    P = blow_pressure
    D = flue_air_band_thickness
    I = ising_number
    F = freq
    return np.power((2*P*D)/(r*np.power(F*I, 2)), 1/3)

def compute_required_cfm(flue_air_band_thickness, flue_width, pressure):
    """given the flue air band thickness, D [meters], flue width, W [meters],
    and pressure, P [Pa], compute CFM required."""
    # see https://www.rwgiangiulio.com/math/flowrate.htm
    pa_to_psi = lambda x : x / 6894.76
    psi_to_in_h20 = lambda x : x * 27.7076
    flow_area = m_to_in(flue_air_band_thickness) * m_to_in(flue_width)
    air_density_factor = 27.86
    return air_density_factor * flow_area * math.sqrt(psi_to_in_h20(pa_to_psi(pressure)))


@click.command()
@click.option('-o','--output-dir', default="cad/step", help='output directory')
@click.option('-n','--midi-note', default=69, help='midi note number of pipe')
@click.option('-m','--halving-number', default=16, help='halving number of pipe ranks')
@click.option('-p','--blow-pressure', default=689.476, help='available blow pressure [Pa]')
@click.option('-i','--ising-number', default=2, help='Ising number for blow efficiency')
@click.option('-c','--foot-cavity-height', default=76.2, help='height of foot cavity [mm]')
@click.option('-d','--dado-depth', default=Dimensions.dado_depth, help='dado depth of pipe part thickness [mm]')
@click.option('-w','--dado-width', default=Dimensions.dado_width, help='dado width of pipe part thickness [mm]')
@click.option('-u','--upper-lip-height', default=Dimensions.upper_lip_height, help='height of upper lip peice [mm]')
@click.option('-T','--stock-thickness', default=Dimensions.stock_thickness, help='thickness of stock material [mm]')
@click.option('-W','--stock-width', default=Dimensions.stock_width, help='width of stock material [mm]')
@click.option('-H','--stock-height', default=Dimensions.stock_height, help='height of stock material [mm]')
@click.option('-P','--pipe-part-thickness', help='thickness of pipe parts (<= stock_thickness) [mm]')
@click.option('-F','--foot-hole-diameter', default=Dimensions.foot_hole_dia, help='foot hole diameter [mm]')
@click.option('-D','--lip-grade', default=Dimensions.lip_grade_degrees, help='angle grade of lip slope [degrees]')
@click.option('-O','--stopper-dowel-diameter', default=Dimensions.stopper_dowel_dia, help='diameter of stopper dowel [mm]')
@click.option('-e','--stopper-felt-tolerance', default=Dimensions.stopper_felt_tolerance, help='tolerance of felt on stopper [mm]')
@click.option('-A','--save-assembly', is_flag=True, help='save pipe assembly as a step file')
def generate(
        output_dir,
        midi_note,
        halving_number,
        blow_pressure,
        ising_number,
        foot_cavity_height,
        dado_depth,
        dado_width,
        upper_lip_height,
        stock_thickness,
        stock_width,
        stock_height,
        pipe_part_thickness,
        foot_hole_diameter,
        lip_grade,
        stopper_dowel_diameter,
        stopper_felt_tolerance,
        save_assembly
):
    """generates flue pipe dimensions according to provided specs."""
    # note: for default blow pressure, see https://en.wikipedia.org/wiki/Pipe_organ#:~:text=Pipe%20organ%20wind%20pressures%20are,two%20legs%20of%20the%20manometer.

    F = compute_frequency(midi_note)
    print(f'=== Parameters ===')
    print(f'Midi Note (N):      {midi_note}')
    print(f'Frequency (F):      {F} [hz]')
    print(f'Halving Number (M): {halving_number}')
    print(f'Blow Pressure (P):  {blow_pressure} [Pa]')
    print(f'Ising Number:       {ising_number}')
    print('=== Dimensions ===')
    L = compute_pipe_length(F)
    print(f'Pipe Length (L):             {L*1000:.3f} [mm] ({m_to_in(L):.3f} in)')
    W = compute_pipe_inner_width(midi_note, halving_number)
    print(f'Pipe Inner Width (W):        {W*1000:.3f} [mm] ({m_to_in(W):.3f} in)')
    D = compute_flue_air_band_thickness(W)
    print(f'Flue Air Band Thickness (D): {D*1000:.3f} [mm] ({m_to_in(D):.3f} in)')
    H = compute_cut_up_height(F, D, blow_pressure, ising_number)
    print(f'Cut-up Height (H):           {H*1000:.3f} [mm] ({m_to_in(H):.3f} in)')
    print(f'Required CFM:                {compute_required_cfm(D, W, blow_pressure):.3f}')

    dimensions = pipe_parts.Dimensions()
    dimensions.stock_thickness = stock_thickness
    dimensions.stock_width = stock_width
    dimensions.stock_height = stock_height
    dimensions.pipe_part_thickness = dimensions.stock_thickness if pipe_part_thickness is None else pipe_part_thickness
    dimensions.upper_lip_height = upper_lip_height
    dimensions.inner_width = W*1000
    dimensions.pipe_length = L*1000
    dimensions.foot_cavity_height = foot_cavity_height
    dimensions.dado_width = dado_width
    dimensions.dado_depth = dado_depth
    dimensions.foot_hole_dia = foot_hole_diameter
    dimensions.air_band_thickness = D*1000
    dimensions.aperature = H*1000
    dimensions.lip_grade_degrees = lip_grade
    dimensions.stopper_dowel_dia = stopper_dowel_diameter
    dimensions.stopper_felt_tolerance = stopper_felt_tolerance

    print(dimensions.pipe_part_thickness)

    pipe_parts.generate(
        f'pipe_{F}hz',
        dimensions,
        save=True,
        step_dir=output_dir,
        save_assembly=save_assembly
    )

if __name__ == '__main__':
    generate()
