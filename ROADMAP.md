# Pipe Organ Roadmap

## Phases
### Pipe Design & Fabrication
0. Pipe CAD Generator
1. Pipe CAM Automation
   - import `.step` files from generator
   - automate generating gcode from `.step` files
     - parameterize tooltip paths
     - select sequence of edges for tooltip paths
     - probably going to use the FreeCAD python API
2. Pipe Milling on CNC
3. Pipe Assembly from milled parts
4. Pipe testing
   - does it sound good?
   - what things should we change?
   - is the design reliably fabricated?
   - will the pipe foot physically interface well with future pipe chassis
### Pipe Chassis Design & Fabrication
    - control valves for individual pipes
    - electrical valve control hardware
    - valve interface Chassis fabrication
### Windchest Design & Fabrication
    - physical air requirements for intended use cases
    - interface with control chassis and blower
### Air Supply Design & Fabrication
    - manual or motorized generation of air for sufficient physical requirements
### Musical Control System
    - API?
    - automated or manual midi controls
### AI Vocal Synthesis Through Pipes
    - let the silicon speak

### kitschy artisan music box product?!?
    -scalability for different use cases, size limitations of each component
### zine / workshop of DIY instrument building
