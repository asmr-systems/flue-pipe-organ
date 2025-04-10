use <../pipe_parts.scad>


pipe_back(stock_thickness=9.53,
          inner_width=48.0136318583285,
          pipe_length=656.1285392838756,
          foot_cavity_height=76.2,
          dado_width=2.3825,
          dado_depth=2.3825);

// pipe side

translate([78.1786318583285, 0, 0])
pipe_side(stock_thickness=9.53,
          inner_width=48.0136318583285, 
          pipe_length=656.1285392838756, 
          upper_lip_pipe_length=50,
          foot_cavity_height=76.2, 
          dado_width=2.3825, 
          dado_depth=2.3825,
          right=true);