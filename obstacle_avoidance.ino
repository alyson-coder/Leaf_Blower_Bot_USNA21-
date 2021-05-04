// This CODE will run the rangefinder function as a ticker object and print/return 
// a distance value every X seconds. When between a specified distance in front of the 
// vehicle will stop, reverse, and turn right then continue moving forward

// #include <Servo.h>
#include <Ticker.h>

#define trigPin 3 //pwm pin
#define echoPin 2
                       // 100mS set timer duration in microseconds 

// Initialize Servo Object 
// Servo servo1; 
// int joint1 = 0;

// MOTOR A -Right
const int in1 = 7 ; //IN1 -> pin7
const int in2 = 8 ; //IN2 -> pin8
const int pwmA = 9 ; //EN1 -> pin6 (pwm enable line)
// MOTOR B -Left
const int in3 = 12; //IN3 -> pin12
const int in4 = 13; //IN4 -> pin13
const int pwmB = 11; //EN2 -> pin11 (pwm enable line)

// Global Variables 
float duration, distance;
void range_finder(); 
void drivestraight(); 
void reverse();
void CW90_turn();
void CC90_turn();
void turnoff(); 

// Declare Ticker Object
Ticker tickerObject(range_finder, 50); 

// For providing logic to L298 IC to choose the direction of the DC motor
// Before starting, HERE ARE SOME NOTES: 
//   1) Stalls at speeds less than 50
void setup() {
  
  // Attach the rangefinder  
   pinMode(trigPin, OUTPUT);
   pinMode(echoPin, INPUT);
  // // Attach the Servo 
  // servo1.attach(5); 
  // Attach the Motor Control Pins 
   // LEFT   
   pinMode(in1,OUTPUT) ; // we have to set PWM pin as output
   pinMode(in2,OUTPUT) ;
   // RIGHT 
   pinMode(in3,OUTPUT) ;
   pinMode(in4,OUTPUT) ; 
   // Enable Pins
   pinMode(pwmA,OUTPUT) ; // LEFT Motors 
   pinMode(pwmB,OUTPUT) ; // RIGHT Motors //Logic pins are also set as output
   
  Serial.begin (9600); // DEFINE THE BAUD RATE HERE<--------
   
  // Create Ticker Object
   tickerObject.start(); //start the ticker.
}

void loop()
{  // this function will run the motors in both directions at a fixed speed

  // This if statement set the motors to off if an object is detected, otherwise motors 
  // will be set to on
  if (25 <= distance && distance <=50){
  turnoff(); 
  reverse();
  delay(100);
  CW90_turn();
  delay(1000); // The turn rate is slower when coming from the reverse direction
  
  }
  else{
  // Drive Straight Forward for X seconds
  drivestraight();
  
  // // Turn to the Right 90 degrees
  // CW90_turn();
  // delay(500); // The turn rate is faster when coming from forward direction 
  
  // // Move forward a hair
  // drivestraight(); 
  // delay(100); 
  
  // // Turn rt again to sweep the area you just came from 
  // CW90_turn(); 
  // delay(800); // The turn rate should be a bit slower when coming from lower speed
  
  // // Drive Straight from in the direction you came from before 
  // drivestraight(); 
  // delay(5000); 
  
  // // Turn to the Left 90 degrees
  // CC90_turn();
  // delay(500); // The turn rate is faster when coming from forward direction 
  
  // // Move forward a hair
  // drivestraight(); 
  // delay(100); 
  
  // // Turn left again to sweep the area you just came from 
  // CC90_turn(); 
  // delay(800); // The turn rate should be a bit slower when coming from lower speed
  
  // // AND Repeat.... back to the top
  
  }
  
    // Run Rangefinder
  tickerObject.update(); //range_finder();
  
  
  } // END MAIN LOOP

// -------------------------- FUNCTIONS BELOW------------------------
// Range Finder Function 
void range_finder(){
   // Attach the rangefinder 
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) * 0.0344;
  
  // if (25 <= distance && distance <=50){
  //   Serial.print("Distance = ");
  //   Serial.print(distance);
  //   Serial.println(" | Object Detected!");
  // }
  // else{
  // Serial.print("Distance = ");
  // Serial.print(distance);
  // Serial.println(" cm");
  // }
  return distance;
}
  

// Drive Straight Forward ------------------------------
 void drivestraight(){
  // turn on motor A
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmA, 70); //125);
 
  // turn on motor B
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmB, 70); //80);
 } 
 
// Reverse Motor Direction
void reverse(){
  // turn on motor A
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmA, 70); //125);
 
  // turn on motor B
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmB, 70); //80);
 } 
 
  // Turn 90 degrees (CW)  ---------------------
 void CW90_turn(){    //delay 800 ms for 90 degree turn
  //servo1.write(100); // lock servo facing front
  // Motor A
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmA, 100); //125

   // Motor B
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmB, 100); //80
  
  }
  
   // Turn 90 degrees (CC)  ---------------------
 void CC90_turn(){    //delay 800 ms for 90 degree turn
  //servo1.write(100); // lock servo facing front
  // Motor A
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmA, 100); //125

   // Motor B
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  // set speed to 200 out of possible range 0~255
  analogWrite(pwmB, 100); //80
 }
 
  // Turn off motors ------------------------------------------
  void turnoff(){
  //servo1.write(100); // lock servo facing front
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);  
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
