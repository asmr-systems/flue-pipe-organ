
module pipe_side(stock_thickness=9.53, 
                 inner_width=20, 
                 pipe_length=500,
                 upper_lip_pipe_length = 50,
                 foot_cavity_height=50, 
                 dado_width=3, 
                 dado_depth=4,
                 right=false) 
 {
    // TODO add screw holes?
    total_height = pipe_length+foot_cavity_height;
    difference() {
        translate([0, 0, 0])
            cube([inner_width+(2*dado_depth), 
                  total_height, 
                  stock_thickness]);
        translate([right?inner_width+dado_depth:0, 0, dado_width])
            cube([dado_depth, 
                  total_height, 
                  stock_thickness-dado_width]);
        translate([right?0:inner_width+dado_depth,
                   foot_cavity_height+upper_lip_pipe_length, 
                   dado_width])
            cube([dado_depth, 
                  total_height-upper_lip_pipe_length-foot_cavity_height, 
                  stock_thickness-dado_width]);
        translate([dado_depth+(inner_width/2)-(dado_width/2),
                   total_height-dado_depth,
                   stock_thickness-dado_width])
            #cube([dado_width, dado_depth, dado_width]);
    }
}

module pipe_back(stock_thickness=9.53, 
                 inner_width=20, 
                 pipe_length=500, 
                 foot_cavity_height=50, 
                 dado_width=3, 
                 dado_depth=4) 
{
    total_height = pipe_length+foot_cavity_height;
    difference() {
        translate([0, 0, 0])
            cube([inner_width+(2*stock_thickness), 
                  total_height,              
                  stock_thickness]);
        translate([stock_thickness-dado_width, 
                   0, 
                   stock_thickness-dado_depth])
            cube([dado_width, 
                  total_height, 
                  dado_depth]);
        translate([inner_width+stock_thickness, 
                   0, 
                   stock_thickness-dado_depth])
            cube([dado_width, 
                  total_height, 
                  dado_depth]);
        // languid dado
        translate([stock_thickness, 
                   foot_cavity_height-dado_width, 
                   stock_thickness-dado_depth])
            cube([inner_width, dado_width, dado_depth]);
    }
}

module pipe_front(stock_thickness=9.53, 
                 inner_width=20, 
                 pipe_length=500,
                 upper_lip_pipe_length = 50,
                 foot_cavity_height=50, 
                 dado_width=3, 
                 dado_depth=4) 
{
    difference() {
        cube([inner_width+(2*stock_thickness),
              pipe_length-upper_lip_pipe_length, 
              stock_thickness]);
        translate([stock_thickness-dado_width, 
                   0, 
                   stock_thickness-dado_depth])
            cube([dado_width, 
                  pipe_length, 
                  dado_depth]);
        translate([inner_width+stock_thickness, 
                   0, 
                   stock_thickness-dado_depth])
            cube([dado_width, 
                  pipe_length, 
                  dado_depth]);
    }
}

module languid(stock_thickness=9.53,
               inner_width=20,
               dado_width=3, 
               dado_depth=4) 
{
    difference() {
        cube([inner_width,
              inner_width+2*dado_depth,
              stock_thickness]);
        translate([0, 0, dado_width])
            cube([inner_width, dado_depth, stock_thickness-dado_width]);
    }
}

module foot_base(stock_thickness=9.53,
                 inner_width=20, 
                 dado_depth=4,
                 foot_hole_dia=10) 
{
    difference() {
        cube([inner_width+2*stock_thickness,
              inner_width+2*stock_thickness,
              stock_thickness]);
        translate([0, 0, stock_thickness-dado_depth])
            cube([inner_width+2*stock_thickness,
                  stock_thickness,
                  dado_depth]);
        translate([0, inner_width+stock_thickness, stock_thickness-dado_depth])
            cube([inner_width+2*stock_thickness,
                  stock_thickness,
                  dado_depth]);
        translate([stock_thickness, 0, stock_thickness-dado_depth])
            rotate([0, 0, 90])
                cube([inner_width+2*stock_thickness,
                      stock_thickness,
                      dado_depth]);
        translate([2*stock_thickness+inner_width, 0, stock_thickness-dado_depth])
            rotate([0, 0, 90])
                cube([inner_width+2*stock_thickness,
                      stock_thickness,
                      dado_depth]);
                      
        translate([stock_thickness+(inner_width/2),
                   stock_thickness+(inner_width/2), 
                   0])
            cylinder(h=stock_thickness, r=foot_hole_dia/2);
    }
}

module wedge(inner_width=10,
             stock_thickness=9.53,
             lip_grade=45,
             dado_depth=4) 
{
    difference() {
        union() {
            cube([inner_width, 
                  (stock_thickness-dado_depth)*tan(90-lip_grade), 
                  stock_thickness]);
            translate([-stock_thickness, 0, stock_thickness-dado_depth])
                cube([inner_width+2*stock_thickness,
                      stock_thickness*tan(90-lip_grade), 
                      dado_depth]);
            }
            rotate([lip_grade, 0, 0])
                translate([0, 0, -stock_thickness])
                    cube([inner_width,
                          2*stock_thickness/sin(lip_grade),
                          stock_thickness]);
        }
}

module upper_lip(stock_thickness=9.53,
                 inner_width=20,
                 upper_lip_pipe_length = 50,
                 foot_cavity_height=50,
                 dado_depth=4,
                 air_band_thickness=1,
                 aperature=4,
                 lip_grade=45) 
{
    difference() {
        cube([inner_width+2*stock_thickness,
              foot_cavity_height+upper_lip_pipe_length,
              stock_thickness]);
        translate([0, 0, stock_thickness-dado_depth])
            cube([stock_thickness,
                  foot_cavity_height+
                    upper_lip_pipe_length+
                    stock_thickness-dado_depth,
                  dado_depth]);
        translate([stock_thickness+inner_width, 0, stock_thickness-dado_depth])
            cube([stock_thickness,
                  foot_cavity_height+
                    upper_lip_pipe_length+
                    stock_thickness-dado_depth,
                  dado_depth]);
        translate([0, 0, stock_thickness-dado_depth])
            cube([inner_width+2*stock_thickness,
                  dado_depth,
                  dado_depth]);
        // inset for languid
        translate([0, 
                   foot_cavity_height-stock_thickness, 
                   stock_thickness-dado_depth])
            cube([inner_width+2*stock_thickness,
                  stock_thickness,
                  dado_depth]);
        // aperature
        translate([stock_thickness, foot_cavity_height, 0])
            cube([inner_width, aperature, stock_thickness]);
        // upper lip
        translate([stock_thickness, foot_cavity_height+aperature, 0])
            wedge(inner_width=inner_width,
                  stock_thickness=stock_thickness,
                  dado_depth=dado_depth,
                  lip_grade=lip_grade);       
        // channel opening
        translate([stock_thickness, 
                   foot_cavity_height-stock_thickness-aperature, 
                   0])
            cube([inner_width, aperature, stock_thickness]);
    }
}

module face(stock_thickness=9.53,
            inner_width=20,
            foot_cavity_height=50,
            air_band_thickness=1,
            aperature=4) 
{
    difference() {
            cube([inner_width+2*stock_thickness, 
                  foot_cavity_height,
                  stock_thickness]);
            translate([stock_thickness, 
                       foot_cavity_height-stock_thickness-aperature, 
                       stock_thickness-air_band_thickness])
                cube([inner_width, 
                      stock_thickness+aperature,
                      air_band_thickness]);
    }
}

module stopper(stock_thickness=9.53,
               inner_width=20,
               dado_width=3, 
               dado_depth=4) 
{

    cube([inner_width+2*stock_thickness,
          inner_width+2*stock_thickness,
          stock_thickness-dado_depth]);
    translate([0,
               stock_thickness+(inner_width/2)-(dado_width/2), 
               stock_thickness-dado_depth])
        cube([dado_width, dado_width, dado_depth]);
    translate([inner_width+2*stock_thickness-dado_width,
               stock_thickness+(inner_width/2)-(dado_width/2),
               stock_thickness-dado_depth])
        cube([dado_width, dado_width, dado_depth]);
}

module exploded_view(stock_thickness=9.53, 
                     inner_width=20, 
                     pipe_length=500, 
                     upper_lip_pipe_length = 50,
                     foot_cavity_height=50, 
                     dado_width=3, 
                     dado_depth=4,
                     foot_hole_dia=10,
                     air_band_thickness=1,
                     aperature=4,
                     lip_grade=45,
                     explode_by=5) 
{
        // pipe back
        pipe_back(stock_thickness=stock_thickness,
                  inner_width=inner_width, 
                  pipe_length=pipe_length, 
                  foot_cavity_height=foot_cavity_height, 
                  dado_width=dado_width, 
                  dado_depth=dado_depth);

        // pipe side
        translate([stock_thickness+inner_width, 
                   0, 
                   inner_width+2*dado_depth + stock_thickness-dado_depth +               explode_by])
            rotate([0, 90, 0])
                pipe_side(stock_thickness=stock_thickness,
                          inner_width=inner_width, 
                          pipe_length=pipe_length, 
                          upper_lip_pipe_length=upper_lip_pipe_length,
                          foot_cavity_height=foot_cavity_height, 
                          dado_width=dado_width, 
                          dado_depth=dado_depth,
                          right=true);

        // pipe side
        translate([stock_thickness, 
                   0, 
                   stock_thickness-dado_depth + explode_by])
            rotate([0, -90, 0])
                pipe_side(stock_thickness=stock_thickness,
                          inner_width=inner_width, 
                          pipe_length=pipe_length, 
                          upper_lip_pipe_length=upper_lip_pipe_length,
                          foot_cavity_height=foot_cavity_height, 
                          dado_width=dado_width, 
                          dado_depth=dado_depth);
            
        // pipe front
        translate([inner_width+2*stock_thickness, 
                   foot_cavity_height+upper_lip_pipe_length,
                   2*stock_thickness
                     + inner_width+2*explode_by])
            rotate([0, 180, 0])
                pipe_front(stock_thickness=stock_thickness,
                           inner_width=inner_width, 
                           pipe_length=pipe_length,
                           upper_lip_pipe_length=upper_lip_pipe_length,
                           foot_cavity_height=foot_cavity_height, 
                           dado_width=dado_width, 
                           dado_depth=dado_depth);
        
        // languid
        translate([stock_thickness,
                   foot_cavity_height,
                   stock_thickness-dado_depth + explode_by])
            rotate([90, 0, 0])
                languid(stock_thickness=stock_thickness,
                        dado_width=dado_width, 
                        dado_depth=dado_depth);
          
         // foot base
         translate([0, 
                    -stock_thickness+dado_depth - explode_by,
                    inner_width+2*stock_thickness + explode_by])
            rotate([270, 0, 0])
                foot_base(stock_thickness=stock_thickness,
                          inner_width=inner_width, 
                          dado_depth=dado_depth,
                          foot_hole_dia=foot_hole_dia);
         // upper lip
         translate([inner_width+2*stock_thickness,
                    0,
                    2*stock_thickness+inner_width+3*explode_by])
            rotate([0,180,0])
                upper_lip(stock_thickness=stock_thickness,
                          inner_width=inner_width,
                          upper_lip_pipe_length = upper_lip_pipe_length,
                          foot_cavity_height=foot_cavity_height,
                          dado_depth=dado_depth,
                          air_band_thickness=air_band_thickness,
                          aperature=aperature,
                          lip_grade=lip_grade);
        // face                 
        translate([inner_width+2*stock_thickness,
                   0,
                   3*stock_thickness+inner_width+4*explode_by])
            rotate([0, 180, 0])
                face(stock_thickness=9.53,
                     inner_width=20,
                     foot_cavity_height=50,
                     air_band_thickness=1,
                     aperature=4);
        // stopper
        translate([0,
                   foot_cavity_height+
                     pipe_length+
                     stock_thickness-dado_depth + 
                     explode_by,
                   explode_by])
            rotate([90, 0, 0])
                stopper(stock_thickness=stock_thickness,
                        inner_width=inner_width,
                        dado_width=dado_width, 
                        dado_depth=dado_depth);        
                     
}
