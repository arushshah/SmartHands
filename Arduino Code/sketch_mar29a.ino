const int buttonPin2 = 2;
const int buttonPin3 = 3;
const int buttonPin4 = 4;

int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;

#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(13,12,11,10,9,8);
String readString;

void setup() {
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
  lcd.begin(16, 2);
  // Print a message to the LCD.
  
  Serial.begin(9600);
}

void loop(){
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);

  if (buttonState2 == HIGH) {     
    Serial.println('1');
    delay(300);
    
  }

  if (buttonState3 == HIGH) {     
    // turn LED on:    
    Serial.println('2');
    
    delay(300);
  }
  if (buttonState4 == HIGH) {     
    // turn LED on: 
    Serial.println('3');
    
    delay(300);
  }
}

