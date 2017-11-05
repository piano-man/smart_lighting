#include <VirtualWire.h>
#include <Wire.h>
#include <SPI.h>


const int receive_pin = 11;
const int led_pin = 3;

void setup()
{
    delay(1000);
    Serial.begin(9600);	// Debugging only
    Serial.println("setup");

    vw_set_rx_pin(receive_pin);
   
    vw_set_ptt_inverted(true); // Required for DR3100
    vw_setup(2000);	 // Bits per sec

    vw_rx_start();       // Start the receiver PLL running
}

void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;

    if (vw_get_message(buf, &buflen)) // Non-blocking
    {
	int i;
        buf[buflen] = '\0';
        digitalWrite(led_pin, HIGH);
	// Message with a good checksum received, print it.
	Serial.print("Got: ");
	Serial.print(buflen);
        Serial.print("Got: ");
	for (i = 0; i < buflen; i++)
	{
	    Serial.write(buf[i]);
            
            
            
	}
	Serial.println();
       // digitalWrite(led_pin, LOW);

    char tt[5]={buf[0],buf[1], buf[2],buf[3],'\0'};
    char rh[5]={buf[6],buf[7], buf[8],buf[9],'\0'};
 
    
 
    delay(100);
    digitalWrite(led_pin, LOW); 
 
  }
    
    
    
}
