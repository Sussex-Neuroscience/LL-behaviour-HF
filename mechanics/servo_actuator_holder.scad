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
poleDia = 12.9;
poleHei = 45;

tol = 0.1;
servoX = 16;
servoY = 24;
servoZ = 25.6;
servoPocketH = 9;
holderWall = 2;

rotatorDia = 68;
rotatorHei = 8;

screwDia=3.95;
nutDia = 6.91;
nutHei = 3.25;

$fn=60;


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
    
module servoFit(){
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
    
    
    
    }//end module
module linear_rail(){
    translate([-12.5,-5,-2]){
    cube([25,1,14]);
        }//end transalte
    rack(2, 50, 5, 10, pressure_angle=20, helix_angle=0);
    }//module

module gear(){
    fitX=1.82;
    fitY=4.71;
    fitZ=4;
    difference(){
    translate([0,0,-3/2]){
    cylinder(d=8,h=3);
    }//end translate
    cube([fitX+2*tol,fitY+2*tol,fitZ],center=true);
    rotate([0,0,90]){
        cube([fitX+2*tol,4.71+2*tol,fitZ],center=true);}//end rotate
    }//end difference
    spur_gear (2, 10, 10, 5, pressure_angle=20, helix_angle=0, optimized=true) ;
}//end module

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
    cylinder(d=80,h=5);
    translate([0,0,-4]){
        cylinder(d=screwDia+2*tol,h=10);
    }//end translate
    }//end translate
rotate([0,90,0]){
    translate([5,-14,40]){
    servoFit();
  }
    }

translate([100,100,0]){

difference(){
cylinder(d=80,h=5);
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


//poleFit();
translate([10,20,0]){
gear();
}
linear_rail();
//servoFit();

////////////legacy
/*
module teeth(tx = 5,ty=5,tz=10){
union(){
    for (i= [0:15:360]){
    rotate([0,0,i])   {
        //translate([0,-(rotatorDia+2)/2,0]){
    
            cube([tx,ty,tz],center=true);
        //}//end translate
    }//end rotate
    }//end for
}//end union
}//end module
*/