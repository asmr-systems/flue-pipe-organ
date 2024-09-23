import math
import click
import numpy as np

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
    """calculate required cut up height given frequency (F) [hz],
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
@click.option('-n','--midi-note', default=69, help='midi note number of pipe')
@click.option('-m','--halving-number', default=16, help='halving number of pipe ranks')
@click.option('-p','--blow-pressure', default=689.476, help='available blow pressure [Pa]')
@click.option('-i','--ising-number', default=2, help='Ising number for blow efficiency')
def generate(midi_note, halving_number, blow_pressure, ising_number):
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


if __name__ == '__main__':
    generate()
