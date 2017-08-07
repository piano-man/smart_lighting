#define REDPIN 5
#define GREENPIN 6
#define BLUEPIN 3
 
#define FADESPEED 5 
#define DHTPIN 5  
#define DHTTYPE DHT22  
#include <VirtualWire.h>
#include <Wire.h>
#include <BH1750.h>

BH1750 lightMeter;
const int led_pin = 11;
const int transmit_pin = 12;

void setup(){

    vw_set_tx_pin(transmit_pin);
  vw_set_ptt_inverted(true); 
  vw_setup(2000);
  Serial.begin(9600);
    Wire.begin();

  lightMeter.begin();
  Serial.println(F("BH1750 Test"));

}

void loop() {

  int r, g, b;
      uint8_t lux = lightMeter.readLightLevel();
Serial.print(lux);
Serial.println(); 
char *data;
char msg[10];
sprintf(msg, "%d,%d.", 77, lux);
 vw_send((uint8_t *)msg, strlen(msg));
    vw_wait_tx();
    digitalWrite(led_pin, LOW);
      if(lux<=7)
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 0);
      }
      else if(lux >7&&lux<=35)
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 55);
      }
            else if(lux >35&&lux<=70)
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 85);
      }
            else if(lux >70&&lux<=100)
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 200);
      }
            else if(lux >100&&lux<=155)
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 255);
      }
            else
      {
                pinMode(BLUEPIN, OUTPUT);
          analogWrite(BLUEPIN, 255);
      }
//  pinMode(BLUEPIN, OUTPUT);
//  analogWrite(BLUEPIN, lux);

  delay(100);
}
