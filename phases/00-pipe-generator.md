# Pipe CAD Generator Phase

## Scope
The scope of this phase is limited to being able to generate `.step` CAD files for all the separate pieces of a parameterized flue pipe.
### Sequential Deliverables ($1200)
1. a research document overview of how the pipe generator will work ($300)
   - how to specify pipe parameters
   - how to interface with some open source CAD software
   - document thoroughly the pros/cons of different approaches
   - describe what you've tried, what things worked, what things failed
   - think through absolute indexing for all part surfaces in a way that could be useful during the CAM automation
2. a software pipeline implementation that takes a declarative set of flue pipe parameters and generates `.step` files for each individual part ($900)
### Requirements
- the generated `.step` files must be importable into FreeCAD
- the pipeline shall be able to output individual `.step` files for each part of the pipe
- the pipeline shall be able to output an "exploded" assembly of all the parts of the pipe fitting together
- the pipeline shall be able to output an optimized "work-piece" layout (optional, potentially part of next phase)
- each piece shall be designed so milling only has to be performed on one side
- design each piece so that no or minimal "planing" has to be performed
