screwD = 3.9;
screwL = 40;

actuatorX = 12;
actuatorY = 12;
actuatorZ = 20;

slitX = 6.1;
slitY = 8.99;
slitZ = 8.97;

$fn = 40;
tol = 0.1;

module actuator_fit(){
    difference(){
        union(){
        cube([actuatorX+2+2*tol,actuatorY+2+2*tol,actuatorZ+slitZ+2],center=true);
        cube([screwD+2+2*tol,screwD+2+2*tol,screwD+2+5],center=true);
        }//end union
        union(){
            translate([0,0,slitZ]){
            cube([actuatorX+2*tol,actuatorY+2*tol,actuatorZ],center = true);
            }//end translate
            translate([0,0,0]){
            cube([slitX+2*tol,slitY+2*tol,actuatorZ+slitZ],center = true);
        
            }//end translate
            rotate([0,90,0]){
                translate([(actuatorZ+slitZ)/2-screwD,0,-screwL/2]){
                cylinder(d=screwD,h=screwL);
                }//end translate
            }//end rotate
        }//end union
    }//end difference
}//end module


    
    
actuator_fit();