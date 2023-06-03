// Código B_RX_2 (BASE)

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <RF24.h>

RF24 radio(8,10); // CE, CSN
const byte address[6] = "00001";

float AcX, AcY, AcZ, GyX, GyY, GyZ, ALTITUD;

void setup() 
{
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setChannel(90);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening(); 
}

void loop()
{
  if (radio.available())     
  {  
    float datos[7];
    radio.read(datos, sizeof(datos));
    AcX = datos[0];
    AcY = datos[1];
    AcZ = datos[2];
    GyX = datos[3];
    GyY = datos[4];
    GyZ = datos[5];
    ALTITUD = datos[6];

    Serial.print(AcX); Serial.print(","); Serial.print(AcY); Serial.print(","); Serial.print(AcZ); Serial.print(",");
    Serial.print(GyX); Serial.print(","); Serial.print(GyY); Serial.print(","); Serial.print(GyZ); Serial.print(",");
    Serial.println(ALTITUD);
    
  }
  delay(50);
}
