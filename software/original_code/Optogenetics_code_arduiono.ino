#include <digitalWriteFast.h>

int mirrorinputPin = 9;      // digital input connected to AO1 of Dev2 that sends signal to Pockels cell.
//This signal is LOW when the mirrors are turning, hence our need to invert
//Make sure that Power is set to 100% in the Power Control Panel

int gatePin = 7;      // gating signal from labjack connected connected to digital in 7.  Tells us when LED should be driven
int outputPin = 13;   // output connected tp PWM pin 13
int gateval = 0;
int mirrorval = 0;

bool goingdown = true;
bool trippedup = false;
bool trippeddown = false;


#define FASTADC 1

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif



void setup()
{
  pinMode(outputPin, OUTPUT);
  pinMode(gatePin, INPUT);        // sets the digital pin 7 as input
  pinMode(mirrorinputPin, INPUT);  //sets digital pin 9 as input   
  digitalWrite(outputPin, LOW); 
}


void loop() 
{
 gateval=digitalRead(gatePin);
 if(gateval==HIGH)
  {
   mirrorval = digitalRead(mirrorinputPin); 
   if(mirrorval==HIGH)
    {
      digitalWrite(outputPin, LOW);
    }
  if(mirrorval==LOW)
    {
      digitalWrite(outputPin, HIGH);
    }
  }
 
 if(gateval==LOW)
  {
    digitalWrite(outputPin, LOW);
  }
  
}  

