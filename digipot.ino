#include "FastX9CXXX.h"
FastX9C103  pot(5,7,6);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  pinMode(13,OUTPUT);
}

bool started = false;
bool calibrated = false;
int maximum = 90;


void loop() {
    // put your main code here, to run repeatedly:

  if (not started)
  {
    Serial.println("Resetting");
    pot.Reset();
    pot.JumpToStep(99);
    Serial.print("Pot Value: ");
    Serial.println(pot.GetStep());
    started = true;
    Serial.println("Calibrating.. Type 100 When At Max Voltage");
    Serial.println("Type Any Other Number To Up Voltage");
  }
  //adjustPot(99);
  
  
  while (Serial.available() > 0)
  {
    
    int dataIn = Serial.parseInt();
    if(dataIn == 0){continue;}
    //Serial.print("Recieved Message: ");
    //Serial.println(dataIn);
    //Do something with the data - like print it

    if(dataIn<95){digitalWrite(13,HIGH);}
    else{digitalWrite(13,LOW);}

    if(!calibrated)
    {
      if (dataIn == 100)
      {
        maximum = pot.GetStep();
        calibrated = true;
        adjustPot(99);
        Serial.print("Calibrated at: ");
        Serial.println(maximum);
      }
      else
      {
        pot.Down();
        Serial.print("Calibrating - Pot Value: ");
        Serial.println(pot.GetStep());
      }
    }
    else
    { 
      adjustPotPercent(dataIn);
      //Serial.print("Pot Value: ");
      //Serial.println(pot.GetStep());
    }
  }
}

void adjustPot(int num)
{
   
   if (num>99){num = 99;}
   if (num<maximum){num = maximum;}
   pot.JumpToStep(num);
}

void adjustPotPercent(int num)
{
  float pot_value = (99-maximum)*(num/100.0) + maximum;
  adjustPot(round(pot_value));
}
