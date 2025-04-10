import os
import math
import click
import numpy as np
from jinja2 import Environment, FileSystemLoader

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


# create separate step files or one with multiple parts
# we need to also take the stock width and height into account
# TODO
def generate_scad(pipe_length,             # [mm]
                  inner_width,             # [mm]
                  air_band_thickness,      # [mm]
                  cutup_height,            # [mm]
                  stock_thickness=9.53,    # [mm]
                  foot_cavity_height=76.2, # [mm]
                  dado_depth_percent=0.25, # [%]
                  lip_grade=45,            # [degrees]
                  foot_hole_dia=10):       # [mm]
    # NOTE: making dado depth and width equal here. but
    # we don't have to do that if we don't want to.
    return f"""use <pipe_parts.scad>

pipe_back(stock_thickness={stock_thickness},
    inner_width={inner_width},
    pipe_length={pipe_length},
    foot_cavity_height={foot_cavity_height},
    dado_width={dado_depth_percent*stock_thickness},
    dado_depth={dado_depth_percent*stock_thickness});
"""

@click.command()
@click.option('-o','--output-filename', help='output filename (no extension)')
@click.option('-n','--midi-note', default=69, help='midi note number of pipe')
@click.option('-m','--halving-number', default=16, help='halving number of pipe ranks')
@click.option('-p','--blow-pressure', default=689.476, help='available blow pressure [Pa]')
@click.option('-i','--ising-number', default=2, help='Ising number for blow efficiency')
@click.option('-c','--foot-cavity-height', default=76.2, help='height of foot cavity [mm]')
@click.option('-d','--dado-depth-percent', default=0.25, help='dado depth as percentage of stock thickness (<0.5) [%]')
def generate(output_filename, midi_note, halving_number, blow_pressure, ising_number, foot_cavity_height, dado_depth_percent):
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

    fn = f'cad/scad/generated/{output_filename}'
    environment = Environment(loader=FileSystemLoader("cad/templates/"))
    template = environment.get_template("parts.scad.jinja2")
    with open(f'{fn}.scad', 'w') as scad_file:
        o = template.render(
            pipe_length=L*1000,                    # [mm]
            inner_width=W*1000,                    # [mm]
            air_band_thickness=D*1000,             # [mm]
            cut_up_height=H*1000,                  # [mm]
            stock_thickness=9.53,                  # [mm]
            foot_cavity_height=foot_cavity_height, # [mm]
            dado_depth_percent=dado_depth_percent, # [%]
            parts_margin=25.4,                     # [mm]
            upper_lip_pipe_length=50 # TODO IDK what this is...
        )
        scad_file.write(o)

    # output stl using scad commandline tool
    os.system(f'openscad -o {fn}.stl {fn}.scad')

    # convert stl to setp file using freecad commandline
    os.system(f'freecadcmd stl_to_step.py {fn}.stl')

if __name__ == '__main__':
    generate()
