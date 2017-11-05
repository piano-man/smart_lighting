


#include <VirtualWire.h>


#define DHTPIN 5     // what pin we're connected to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)

const int led_pin = 11;
const int transmit_pin = 12;
//const int receive_pin = 2;
//const int transmit_en_pin = 3;

void setup()
{
  // Initialise the IO and ISR
  vw_set_tx_pin(transmit_pin);
 // vw_set_rx_pin(receive_pin);
//  vw_set_ptt_pin(transmit_en_pin);
  vw_set_ptt_inverted(true); // Required for DR3100
  vw_setup(2000);	 // Bits per sec
 
   Serial.begin(9600);	// Debugging only
   Serial.println("DHT22 Tx");
}



char buffT[6];
char buffH[6];
char buff[15];

void loop()
{

  
  // check if returns are valid, if they are NaN (not a number) then something went wrong!

;
      

    Serial.print("Mess= "); 
char *data;
     data="1";
 vw_send((uint8_t *)data, strlen(data));
  // Flash a light to show transmitting
    vw_wait_tx(); // Wait until the whole message is gone
    digitalWrite(led_pin, LOW);
    delay(10000);
  
  


}
