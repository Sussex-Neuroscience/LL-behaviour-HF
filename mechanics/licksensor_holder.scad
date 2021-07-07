screwD = 3.9;
screwL = 40;

actuatorX = 12;
actuatorY = 12;
actuatorZ = 25;

slitX = 6.45;//added.1mm
slitY = 9.2;//added.1mm
slitZ = 8.97+screwD;

sensorX = 10;
sensorY = 20;
sensorZ = 10;

platformX = 10;
platformY = 50;
platformZ = 5;

$fn = 40;
tol = 0.1;

module actuator_fit(){
    difference(){
    cube([actuatorX+2+2*tol,actuatorY+2+2*tol,actuatorZ+10],center=true);

    translate([0,0,-slitZ-1]){
        union(){
        cube([actuatorX+0.5+2*tol,actuatorY+0.5+2*tol,actuatorZ+2*tol],center = true);
            translate([0,0,(actuatorZ+slitZ)/2]){
            cube([slitX+2*tol,slitY+2*tol,slitZ],center = true);
    
            rotate([0,90,0]){
                translate([2,0,-screwL/2]){
                cylinder(d=screwD,h=screwL);
                }//end translate
            }//end rotate
        }//end translate
        }//end union
    }//end translate
    }//end difference
    
     translate([4.6,0,17]){   
rotate([0,90,0]){
    difference(){
    union(){
cube([platformX,platformY,platformZ],center = true);
 translate([0,0,-actuatorX/2]){
cube([platformX,actuatorY+2+2*tol,actuatorX],center = true);
 }//endtranslate
    
    translate([0,(platformY-sensorY)/2,(platformZ-2)/2]){
cylinder(d=sensorY+3,h=2,center=true);

    }//end translate
        translate([0,-(platformY-sensorY)/2,(platformZ-2)/2]){
cylinder(d=sensorY+3,h=2,center=true);
            
    }//end translate
}//end union
union(){
        translate([0,-(platformY-sensorY)/2,(platformZ-2)/2]){
            cylinder(d=screwD+2*tol,h=20,center=true);
    }//end translate
    translate([0,(platformY-sensorY)/2,(platformZ-2)/2]){

        cylinder(d=screwD+2*tol,h=20,center=true);
    }//end translate
}//end union
}//end difference
}//end rotate
}//end translate

}//end module


module lick_sensor_fit(){
    difference(){
        union(){
        cube([3.5,sensorY+2,sensorZ+2],center=true);
        translate([sensorX/2+screwD,0,-(sensorZ)/2]){
        cylinder(d=sensorY+3,h=2,center=true);
            }//end translate
        }
        //union(){
        //translate([0,0,1.1]){
        //%cube([sensorX,sensorY,sensorZ],center=true);
        //}//end translate
        

        rotate([0,90,0]){    
        cylinder(d=screwD+2*tol,h=sensorX+5,center=true);
        }//end rotate
         translate([sensorX/2+screwD+1,0,-(sensorZ)/2]){
        cylinder(d=screwD+2*tol,h=5,center=true);
        }//end translate
    //}//end union
           }//end difference
    }//end module
    


translate([30,50,0]){
lick_sensor_fit();    
}

translate([30,-50,0]){
lick_sensor_fit();    
}
rotate([0,90,0]){
actuator_fit();
}

