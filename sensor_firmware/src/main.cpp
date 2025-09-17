#include <Arduino.h>

#define TRIG 5 // trig pin
#define ECHO 6 // echo pin

float duration;


void setup(){

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

}

void loop(){

  digitalWrite(TRIG, LOW);
  delay(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIG, LOW);

  duration = pulseIn(ECHO, HIGH);

}



