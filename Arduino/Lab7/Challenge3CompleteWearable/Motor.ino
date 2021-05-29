const int pwmFrequency = 5000;  // Set the PWM frequency to 5KHz
const int pwmChannel = 0;       // Use PWM channel 0
const int pwmBitResolution = 8; // Set a PWM resolution of 8-bits
const int MOTOR_PIN = 12;

// define function
void setupMotor(){
  ledcSetup (pwmChannel, pwmFrequency, pwmBitResolution);
  ledcAttachPin(MOTOR_PIN, pwmChannel); // attaches pwmchannel to motor pin
  }

 // done 

 // new function

  void activateMotor(int motorPower){
    ledcWrite(pwmChannel, motorPower);
    }
// done
// new function

 void deactivateMotor(){
  // sets dutycycle to zero
  ledcWrite(pwmChannel, 0);
  }
