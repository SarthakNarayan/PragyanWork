// Code for esp8266 on bot

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <stdlib.h>
#include <Drive.h>


char* ssid = "Sarthak"; //Enter your wifi network SSID
char* password = "sarthakn"; //Enter your wifi network password

int SERVER_PORT = 1111;
int BAUD_RATE = 9600;

int packetSize = 20;
byte packetBuffer[20];
int arr[20];

int forward=0;
int backward=0;
int left=0;
int right=0;

const int IN1 = 16;
const int IN2 = 5;
const int IN3 = 4;
const int IN4 = 0;

Drive drive(IN1, IN2, IN3, IN4);  //Create an instance of the function

WiFiUDP Udp;

void connectWifi() {
  Serial.println();
  Serial.println();
  Serial.print("Connecting to WIFI network");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("NodeMCU IP Address : ");
  Serial.println(WiFi.localIP() );
  Udp.begin(SERVER_PORT);
  digitalWrite(2,HIGH);
}

void setup(){
    Serial.begin(BAUD_RATE);
    delay(10);     
    pinMode(12,OUTPUT);
    pinMode(2,OUTPUT);
    digitalWrite(12,HIGH);
    connectWifi();
}


void loop() {
  int noBytes = Udp.parsePacket();
  String received_command = "";
  String extractor = "";
  
  if ( noBytes ) {    
    Udp.read(packetBuffer,noBytes);
    int j = 0;
    int k = 0;
    for(int i = 0; i < packetSize; i++) {
          received_command += (char)packetBuffer[i];
      }
      forward = ((int(received_command[0])-48)*1000)+((int(received_command[1])-48)*100)+((int(received_command[2])-48)*10)+((int(received_command[3])-48));
      backward = ((int(received_command[4])-48)*1000)+((int(received_command[5])-48)*100)+((int(received_command[6])-48)*10)+((int(received_command[7])-48));
      left = ((int(received_command[8])-48)*1000)+((int(received_command[9])-48)*100)+((int(received_command[10])-48)*10)+((int(received_command[11])-48));
      right = ((int(received_command[12])-48)*1000)+((int(received_command[13])-48)*100)+((int(received_command[14])-48)*10)+((int(received_command[15])-48));
      Serial.print(forward);
      Serial.print(backward);
      Serial.print(left);
      Serial.println(right);
    }
    
    if (left !=0)
    {
      analogWrite(IN2,left);
      analogWrite(IN3,left);
    }
    if (right !=0)
    {
      analogWrite(IN1,right);
      analogWrite(IN4,right);
    }
    if (backward != 0)
    {
      analogWrite(IN2,backward);
      analogWrite(IN4,backward);
    }
    if (forward != 0)
    {
      analogWrite(IN1,forward);
      analogWrite(IN3,forward);
    }
    else
    {
      analogWrite(IN1,0);
      analogWrite(IN2,0);
      analogWrite(IN3,0);
      analogWrite(IN4,0);
    }

}
