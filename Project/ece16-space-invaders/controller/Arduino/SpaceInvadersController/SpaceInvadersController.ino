/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
int FIRE_BUTTON = 16;
int PAUSE_BUTTON = 12;

const int X_ZERO = 1920;
const int Y_ZERO = 1930;
const int Z_ZERO = 2480;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  setupMotor();
  pinMode(FIRE_BUTTON,INPUT_PULLUP);
  pinMode(PAUSE_BUTTON,INPUT_PULLUP);

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}


bool heldDown1,heldDown2 = false;
bool fire = false;
bool pause_ = false;
bool buzz = false;
int buttonState_Fire, buttonState_Pause;
int x = 0;
int y = 0;
int z = 0;
int last_buzzed;

/*
 * The main processing loop
 */
void loop() {

  // Read the button states 
  buttonState_Fire = digitalRead(FIRE_BUTTON);
  buttonState_Pause = digitalRead(PAUSE_BUTTON);
  
  
  // Fire Button Logic: Fire only when button is first pressed
  if (sending && buttonState_Fire == LOW && heldDown1 == false) {
    fire = true;
    heldDown1 = true;
  }
  // Resets once the button is released
  else if (buttonState_Fire == HIGH) {
    heldDown1 = false;
  }

  // Pause Button Logic: Send pause command only when button is first pressed
  if (sending && buttonState_Pause == LOW && heldDown2 == false) {
    pause_ = true;
    heldDown2 = true;
  }
  // Resets once the button is released
  else if (buttonState_Pause == HIGH) {
    heldDown2 = false;
  }
  
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();

  // if it received 'stop', turns the controller off
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }

  // if it received 'start', turns controller on
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
  // if it received 'BUZZ', buzzes motor
  else if(command == "BUZZ"){
    buzz = true;
    writeDisplay("Shot",2,false);
    activateMotor(255);
    last_buzzed = millis();
    }

  // displays score if the previous statements are not true
  else if (command != "") {
    String score = String("Score: ") + command;
    writeDisplay(score.c_str(), 1, false);
  }

  // makes sure that the motor buzzes for 1 second
  if(buzz && (millis() - last_buzzed >= 1000)){
    // deactivates motor after 1 second
    deactivateMotor();
    writeDisplay("          ",2,false);
    buzz = false;
  }

  // Sends the accelerometer values, pause binary, and fire binary
  if(sending && sampleSensors()) {
    x = ax - X_ZERO;
    y = ay - Y_ZERO;
    z = az - Z_ZERO;
    
    String message = String(x) + "," + String(y) + "," + String(z);
    
    if (fire) {

      message += ", 1";
      fire = false;
    }
    else {
      message += ", 0";
    }

    if (pause_) {
      message += ", 1";
      pause_ = false;
    }
    else {
      message += ", 0";
    }
    sendMessage(message);
  }
}
