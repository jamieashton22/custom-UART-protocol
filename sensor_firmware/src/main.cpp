// Arduino Firmware

//==========================================================


#include <Arduino.h>

#define TRIG 5 // trig pin
#define ECHO 6 // echo pin

#define FLAG 0x7E 
#define ESC 0x7D 

byte header[2];
byte payload[2];
byte frame[5]; 

// escaping function

void EscapeAndSend(byte _byte);

void setup(){

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  Serial.begin(9600);

}

void loop(){

  //payload

  digitalWrite(TRIG, LOW);
  delay(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(TRIG, LOW);

  unsigned long duration = pulseIn(ECHO, HIGH); // returns integer in microseconds

  // convert duration from integer to bytes 
  uint16_t duration_int = uint16_t(duration);
  payload[0] = highByte(duration_int);
  payload[1] = lowByte(duration_int);
  
  // header

  byte type = 0x01;
  byte length = 2;
  header[0] = type;
  header[1] = length;

  // checksum 
  byte checksum = header[0] ^ header[1] ^ payload[0] ^ payload[1];


  // construct the frame
  frame[0] = header[0];
  frame[1] = header[1];
  frame[2] = payload[0];
  frame[3] = payload[1];
  frame[4] = checksum;

  // send the frame
  Serial.write(FLAG);
  for(int i = 0; i<5 ; i++) EscapeAndSend(frame[i]);
  Serial.write(FLAG);

  delay(100); // small delay
}

void EscapeAndSend(byte _byte){

  if(_byte == FLAG || _byte == ESC) {

    Serial.write(ESC);            // send escape byte
    Serial.write(_byte ^ 0x20);   // send original byte XORed with 0x20
  }

  else {
    Serial.write(_byte);
  }
  
}

