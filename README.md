# Flue Pipe Organ

## Generating Pipe Dimensions
### Setup
``` shell
# create python virtual env
python -m venv venv

# activate venv
source venv/bin/activate      # if using bash
source venv/bin/activate.fish # if using fish

# install dependencies
pip install -r requirements.txt
```
### Generate
``` shell
# make sure the python venv is still activated

# view all input parameters
python pipe_gen.py --help
```

## Future Ideas
### Generate CAD files
generate [OpenSCAD](https://openscad.org/) files from pipe dimensions and then generate an STL file using the openscad commadline tool:
``` shell
openscad -o result.stl my_generated_pipe_dimensions.scad
```
then, we can use [FreeCAD](https://www.freecad.org/) to convert to an STEP file and generate gcode for cnc.

## Bill of Materials
* [1/4inch DC 12V 2 Way Normally Closed Electric Solenoid Air Valve, Stainless Steel](https://a.co/d/bLPSXj3)
 * Flow Rate: 22 SCFM at 100 PSI (Air Flow)
* [One-Way Air Valve](https://a.co/d/e5XyaxP)
 * this could be used to pressurize the wind chest from a simple compression source (bike pump? to start with)


## References
* [Recipe for Wooden Organ Flue Pipes](https://www.mmdigest.com/Tech/pipesRecipe.html)
* [The physics of voicing organ flue pipes ](https://www.colinpykett.org.uk/physics-of-voicing-organ-flue-pipes.htm#Cutup)
* [Pipes made of glued wood lumber](https://www.yamaha.com/en/musical_instrument_guide/pipeorgan/mechanism/mechanism003.html)
* [Pipes](http://www.fonema.se/organ/pipes/pipes.htm)
* [Pipe Scaling](https://www.rwgiangiulio.com/math/pipescaling.htm)
* [Calculating the Flowrate Requirement for a Pipe](https://www.rwgiangiulio.com/math/flowrate.htm)
* [Pipe Anatomy](https://www.researchgate.net/publication/315100298/figure/fig5/AS:668883253985299@1536485603642/The-parts-of-a-reed-lingual-a-and-a-flue-labial-b-organ-pipe-As-shown-in-b-the.ppm)
* [Pipe cut-up and flue dimensioning chart](http://www.fonema.se/ising/isint.htm)
* [Ising's Formula](https://www.mmdigest.com/Tech/isingform.html)
* [Pushing and bouncing air](https://www.mmdigest.com/Tech/airbounc.htm)
* [The physics of organ blowing](https://www.colinpykett.org.uk/physics-of-organ-blowing.htm)
* [Wikipedia: Typical Organ Wind Pressures](https://en.wikipedia.org/wiki/Pipe_organ#:~:text=Pipe%20organ%20wind%20pressures%20are,two%20legs%20of%20the%20manometer.)
