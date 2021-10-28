//////////////////////////
// Holder for servo motors
// and licking spouts
// CC BY SA 4.0 
// Andre M Chagas
// 22/10/2021
///////////////////////////
//uses a gear library:
//https://github.com/chrisspen/gears

use <gears/gears.scad>

//thorlabs pole which holds the system in position
poleDia = 12.9;
poleHei = 25;

tol = 0.1;

//servo motor dimensions
servoX = 16;
servoY = 24;
servoZ = 25.6;
servoPocketH = 9;

//wall thickness of the servo holder
holderWall = 2;



//rotatorDia = 68;
//rotatorHei = 8;


//information about nut and screws that are used to fix things
screwDia=3.95;
nutDia = 6.91;
nutHei = 3.25;

$fn=60;


//gear fit information
fitX=1.7;
fitY=4.6;
fitZ=6;
fitDispla=1.5;


//gear and rail information
gearModule = 1;
nTeeth = 25;
gearW = 10;
centralBoreD = 5;
pressureAngle = 30;
helixAngle = 10;
railL = 30;
railH=5;




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
    
module gear(){

    difference(){
        translate([0,0,-fitDispla]){
            cylinder(d=8,h=fitZ);
        }//end translate
        translate([0,0,fitDispla-0.1]){
            cube([fitX+2*tol,fitY+2*tol,fitZ],center=true);
            rotate([0,0,90]){
                cube([fitX+2*tol,4.71+2*tol,fitZ],center=true);
                }//end rotate
        }//end translate
        }//end difference
    //spur_gear (modul, zahnzahl, breite, bohrung, eingriffswinkel=20, schraegungswinkel=0, optimiert=true) 
    spur_gear (gearModule, nTeeth, gearW, centralBoreD, pressure_angle=pressureAngle, helix_angle=helixAngle, optimized=true) ;
    
}//end module

module servo_fit(){
    difference(){
        union(){
    cube([servoX+2*holderWall,servoY+2*holderWall,servoPocketH+2*holderWall]);
    translate([holderWall,(servoY+2*holderWall),3]){
        cube([servoX,5,8]);
        }//end translate
    translate([holderWall,-2*holderWall-1,3]){
        cube([servoX,5,8]);
        }//end translate
    }//end union
    translate([holderWall,holderWall,holderWall]){
        cube([servoX+2*tol,servoY+2*tol,servoZ+2*tol]);    
    rotate([0,90,0]){    
    translate([-5,servoY+4.2,-1]){
    cylinder(d=3,h=servoX+2);
    }//end translate
}//end rotate
    rotate([0,90,0]){    
    translate([-5,-4.2,-1]){
    cylinder(d=3,h=servoX+2);
    }//end translate
}//end rotate
    }//end translate
    
    }//end difference
    
    
    translate([(servoX)+gearW/2+railH,0,0]){
        cube([5,servoY+2*holderWall,servoZ+gearW]);
    translate([-7,0,0])
        cube([8,servoY+2*holderWall,5]);
        }//end translate
     
    
    }//end module
    
    
 
module linear_rail_pos(leng = railL){
    difference(){
    union(){
    translate([-leng/2-2,-railH,-2]){
    cube([leng,1,gearW+4]);
        }//end translate
    //rack(module, length, height, width, pressure_angle=20, helix_angle=0)
    rack(gearModule, leng, railH, gearW, pressure_angle=pressureAngle, helix_angle=-helixAngle);
    }//end union
    translate([-leng/2+2,-railH-1,(gearW-3.5)/2]){
    cube([15,10,3.5]);
        }//end translate
}//end difference
/*
translate([-leng/2-2,-railH,-2]){
    cube([leng,1,gearW+4]);
        }//end translate
*/
}//module

module linear_rail_neg(leng = railL){
    
    translate([-leng/2,-railH,-2]){
    cube([leng+4*tol,1+4*tol,gearW+4+4*tol]);
        }//end translate
    //rack(module, length, height, width, pressure_angle=20, helix_angle=0)
    rack(gearModule, leng+2*tol, railH+2*tol, gearW+2*tol, pressure_angle=pressureAngle, helix_angle=helixAngle);
    }//module


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


/*
difference(){
    cylinder(d=50,h=5);
    translate([0,0,-4]){
        cylinder(d=screwDia+2*tol,h=10);
    }//end translate
    }//end translate
rotate([0,90,0]){
    translate([5,-14,40]){
    servo_fit();
  }
    }

translate([100,100,0]){

difference(){
cylinder(d=50,h=5);
translate([0,0,-4]){
cylinder(d=screwDia+2*tol,h=10);
}
}
rotate([0,-90,0]){
    translate([12.5,20,-20]){
poleFit();
    }
}
}
*/







/*
difference(){
servo_fit();
    */
rotate([0,0,90]){
translate([-5,-servoX-12.75,servoZ-4]){
    difference(){
    cube([40,6,gearW+8]);
        
    translate([20,railH+5-2,(gearW-3)/2]){
        linear_rail_neg(leng = 45);
    }//end translate
    }//end difference
}//end translate
}//end rotate
//}//end difference

translate([10,0,0])
translate([(servoX)+gearW/2,servoY/2,servoZ])
rotate([0,0,90])
linear_rail_pos(leng = 40);
//translate([0,0,0])
//servo_fit();
//translate([(servoX+holderWall)/2,(servoY+holderWall)/2,servoZ])
//gear();

