solD = 19.16;
solH = 25;
wall = 4;
tol = 0.1;
holH = 10;

poleDia = 12.9;
poleHei = 30;


screwDia=3.95;
nutDia = 6.91;
nutHei = 3.25;

$fn=60;
//%cylinder(d=solD,h=solH,center=true);
module poleFit(){
    difference(){
    cylinder(d=poleDia+10,h=poleHei);
        translate([0,0,-1]){
        cylinder(d=poleDia+2*tol,h=poleHei+5);
        }//end translate
    translate([-(poleDia),0,poleHei/2+1]){
        rotate([0,90,0]){
        cylinder(d=screwDia+1,h=poleDia+20);
        }//end rotate
    }//end translate
    }//end difference
    translate([(poleDia+10)/2+2.5,0,poleHei/2]){
        nutpocket();
    }//end translate
}//end module

module nutpocket(){
    difference(){
        cube([nutHei+5,nutDia+5,nutDia+6],center=true);
        union(){
            translate([0,0,nutDia/2-2.5]){
                rotate([0,90,0]){
                    translate([0,0,-10]){
                        cylinder(d=screwDia+2*tol,h=nutHei+20);
                        }//end translate
                }//end rotate
                cube([nutHei+2*tol,nutDia+2*tol,nutDia+4+2*tol],center=true);
                }//end translate
            }//end union
        }//end differece
    }//end module

module solenoid_holder(){
    
    difference(){
    union(){
    cylinder(d=solD+2*(wall+tol),h=holH);
    translate([-10,solD/2,0]){
    cube([20,40,holH]);
    }//end translate
}//end union
union(){
        translate([0,0,-1]){
    cylinder(d=solD+2*(tol),h=holH+2);
        }//end translate
    }//end difference
        translate([0,40,-1]){
    cylinder(d=poleDia+2*(tol),h=holH+2);
        }//end translate
    //translate([0,(solD/2)+20,0]){
    // cube([30,20,holH]);
    //}//end translate
    }
    }//end module

rotate([0,0,45]){
    translate([0,-40,0])
solenoid_holder();
}

rotate([0,0,-45]){
    translate([0,-40,0])
solenoid_holder();
}
    /*
    translate([59,0,0]){
    mirror([1,0,0]){
        solenoid_holder();
    }//end translate
        }
    */


poleFit();