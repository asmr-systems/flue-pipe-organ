use <../pipe_parts.scad>


pipe_back();
translate([1*50, 0, 0])
pipe_side(right=true);
translate([2*50, 0, 0])
pipe_side(right=false);
translate([3*50, 0, 0])
pipe_front();
translate([4*50, 0, 0])
languid();
translate([5*50, 0, 0])
foot_base();
translate([6*50, 0, 0])
wedge();
translate([7*50, 0, 0])
upper_lip();
translate([8*50, 0, 0])
face();
translate([9*50, 0, 0])
stopper();
