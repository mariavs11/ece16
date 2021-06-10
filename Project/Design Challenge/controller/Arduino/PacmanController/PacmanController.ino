/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
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
  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}


bool heldDown1 = false;
bool buzz = false;
int x = 0;
int y = 0;
int z = 0;
int last_buzzed;

/*
 * The main processing loop
 */
void loop() {

  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }

  // if received 'start', turns on controller
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On ", 0, true);
  }

  // if received "BUZZ", buzzes the motor
  else if(command == "BUZZ"){
    buzz = true;
    activateMotor(255);
    last_buzzed = millis();
    }

  // displays score and lives if the previous if/elseif statements are not true
  else if (command != "") {

    // if received score, display score onto the OLED on row 1
    if (command[0] == 'S') {
      writeDisplay(command.c_str(), 1, false);
    }
    // if received score, displays lives onto the OLED on row 2
    else if (command[0] == 'L') {

    // displays Game over once you've lost all your lives
      if (command[7] == '-') {
        writeDisplay("Game Over", 2, false);
      }

      else {
        command += String("     ");
        writeDisplay(command.c_str(), 2, false);
      }
    }
  }
    
  if(buzz && (millis() - last_buzzed >= 1000)){
    // deactivates motor after 1 second
    deactivateMotor();
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

    sendMessage(message);
  }
}
