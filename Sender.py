# Sending data to esp8266

#include <SoftwareSerial.h>
#define rxPin 8
#define txPin 7
#define Samplesize   13         // filterSample number

SoftwareSerial mySerial(rxPin, txPin); // RX, TX

int Array_x [Samplesize];  
int Array_y [Samplesize];      // array for holding raw sensor values for sensor

int rawData_x,rawData_y;      
int smoothData_x,smoothData_y;
String toSend_x,toSend_y;

void setup(){
  Serial.begin(9600);
  pinMode(6,OUTPUT);
  pinMode(5,OUTPUT);
}

void loop()
{     
  digitalWrite(6,HIGH);
  digitalWrite(5,LOW);
  rawData_x = analogRead(A0);                              // read X-axis of accelerometer
  rawData_y = analogRead(A1);
  
  smoothData_x = digitalSmooth(rawData_x, Array_x);  
  smoothData_y = digitalSmooth(rawData_y, Array_y); 
  
  toSend_x = String(smoothData_x);
  toSend_y = String(smoothData_y);

//  Serial.write(smoothData_x);
//  Serial.println(smoothData_x);
  Serial.print(toSend_y + " ");
  
  delay(100);
}

  int digitalSmooth(int rawIn, int *sensSmoothArray){         // "int *sensSmoothArray" passes an array to the function - the asterisk indicates the array name is a pointer
  int j, k, temp, top, bottom;
  long total;
  static int i;
  static int sorted[Samplesize];
  boolean done;

  i = (i + 1) % Samplesize;                  // increment counter and roll over if necc. -  % (modulo operator) rolls over variable
  sensSmoothArray[i] = rawIn;           // input new data into the oldest slot

  for (j=0; j<Samplesize; j++){           // transfer data array into anther array for sorting and averaging
    sorted[j] = sensSmoothArray[j];
  }

  done = 0;                    // flag to know when we're done sorting              
  while(done != 1){        // simple swap sort, sorts numbers from lowest to highest
    done = 1;
    for (j = 0; j < (Samplesize - 1); j++){
      if (sorted[j] > sorted[j + 1]){        // numbers are out of order - swap
        temp = sorted[j + 1];
        sorted [j+1] =  sorted[j] ;
        sorted [j] = temp;
        done = 0;
      }
    }
  }

  bottom = max(((Samplesize * 15)  / 100), 1); 
  top = min((((Samplesize * 85) / 100) + 1  ), (Samplesize - 1));   // the + 1 is to make up for asymmetry caused by integer rounding
  k = 0;
  total = 0;
  for ( j = bottom; j< top; j++){
    total += sorted[j];         // total remaining indices
    k++; 

  }

  return total / k;            // divide by number of samples
}
