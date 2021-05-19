screwD = 3.9;
screwL = 40;

actuatorX = 12;
actuatorY = 12;
actuatorZ = 25;

slitX = 6.35;
slitY = 9.1;
slitZ = 8.97+screwD;

$fn = 40;
tol = 0.1;

module actuator_fit(){
    difference(){
    cube([actuatorX+2+2*tol,actuatorY+2+2*tol,actuatorZ+2],center=true);

    translate([0,0,-slitZ-1]){
        union(){
        cube([actuatorX+2*tol,actuatorY+2*tol,actuatorZ+2*tol],center = true);
            translate([0,0,(actuatorZ+slitZ)/2]){
            cube([slitX+2*tol,slitY+2*tol,slitZ],center = true);
    
            rotate([0,90,0]){
                translate([0,0,-screwL/2]){
                cylinder(d=screwD,h=screwL);
                }//end translate
            }//end rotate
        }//end translate
        }//end union
    }//end translate
    }//end difference
}//end module



    
    
actuator_fit();


