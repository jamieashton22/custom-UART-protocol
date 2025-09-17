// Arduino Firmware

// loop: assemble frame (header, payload, checksum)
//        send start flag
//        call escaping function on every byte in frame
//        send end flag

// need function to perform escaping ...
//==========================================================


#include <Arduino.h>

#define TRIG 5 // trig pin
#define ECHO 6 // echo pin

#define FLAG 0x7E 
#define ESC 0x7D 

byte header[2];

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

  float duration = pulseIn(ECHO, HIGH); // returns integer in microseconds

  // convert duration from integer to bytes 
  byte duration_int = uint16_t(duration);
  byte payload_high = highByte(duration_int);
  byte payload_low = lowByte(duration_int);   // these are the payload bytes

  // header

  byte type = 0x01;
  byte length = 2;
  header[0] = type;
  header[1] = length;

  // checksum 
  byte checksum = header[0] ^ header[1] ^ payload_high ^ payload_low;
  


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

