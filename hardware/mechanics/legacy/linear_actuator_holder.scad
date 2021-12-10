poleDia = 12.9;
poleHei = 45;
tol = 0.1;
actuatorX = 18;
actuatorY = 20;
actuatorZ = 50;

rotatorDia = actuatorX+actuatorY+30;
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
    
module actuatorFit(){
    difference(){
        union(){
        cube([actuatorX+6+2*tol,actuatorY+6+2*tol,actuatorZ],center=true);
        translate([0,(actuatorY+6-1)/2,actuatorZ/2-5]){
            cube([actuatorX+4+2*tol,5,10],center=true);    
        }//end translate
            translate([0,(actuatorY+6-1)/2,-actuatorZ/2+5]){
            cube([actuatorX+4+2*tol,5,10],center=true);    
        }//end translate
        }//end union //cube([actuatorX+30,screwDia+10,screwDia+10],center=true);
        union(){
            translate([-2.5*actuatorX,0,0]){
            rotate([0,90,0]){
            cylinder(d=screwDia+2*tol,h=5*actuatorX);
            }//end rotate
        }//end translate
        translate([0,3,0]){
        cube([actuatorX+2*tol,actuatorY+3*tol,actuatorZ+5],center=true);
        }//end translate
    }//end union
    }//end difference
    
        rotate([-90,0,0]){
    translate([(actuatorX+nutHei+8)/2,0,-.95]){
        
    nutpocket();
        }
    }
    
    rotate([-90,0,0]){
        translate([-(actuatorX+nutHei+8)/2,0,-.95]){
            
    nutpocket();
            }
    }
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



difference(){
    cylinder(d=80,h=5);
    translate([0,0,-4]){
        cylinder(d=screwDia+2*tol,h=10);
    }//end translate
    }//end translate
rotate([-90,0,0]){
    translate([20,8.1,15]){
    actuatorFit();
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



//poleFit();



////////////legacy

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
