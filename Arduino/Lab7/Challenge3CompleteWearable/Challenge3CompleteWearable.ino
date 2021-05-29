/*
   Global variables
*/
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
int BUTTON_PIN = 14;
void setupCommunication();
void setupDisplay();
void setupMotor();
void setupPhotoSensor();
void setupAccelSensor();
void setupPhotoSensor();
void readPhotoSensor();
bool sampleSensors();
/*
   Initialize the various components of the wearable
*/
void writeDisplay(const char * message, int row, bool erase);
void writeDisplayCSV(String message, int commaCount);
void activateMotor(int motorPower);
void deactivateMotor();
String receiveMessage();
void sendMessage(String message);

void setup() {
  setupAccelSensor();
  setupPhotoSensor();
  setupCommunication();
  setupDisplay();
  setupMotor();
  sending = false;
  writeDisplay("Sleep", 0, true);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
}

/*
   The main processing loop
*/

String local = "0";
bool heldDown = false;
bool stepCount = false;
int buttonState;

void loop() {
  String command = receiveMessage();

  // Button Check
  buttonState = digitalRead(BUTTON_PIN);

  // If the button is pressed, toggle Pedometer data on or off
  if (buttonState == LOW && heldDown == false) {
    Serial.println("Button held down");
    heldDown = true;
    // Sends the information
    activateMotor(256);
    delay(1000);
    if (sending) {
      if (stepCount == false) {
        stepCount = true;
      }
      else {
        stepCount = false;
      }
    }
  }
  // Used to make sure that it only toggles when the button is pressed
  // and not when it is held down
  else if (buttonState == HIGH) {
    heldDown = false;
    deactivateMotor();
  }

  // States
  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
    stepCount = false;
  }
  else if (command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  // Prints the message onto OLED
  else if (sending) {
    if (command != "") {
      // Checks if the new message is the same as the local message already on the OLED 
      // Only updates OLED if the message is different to reduce MCU slowdowns
      if (local != command) {
        writeDisplayCSV(command, 3);
        local = command;
      }
    }
  }

  // Sends the Photodetector and Accelerometer data
  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    
    // Send accelerometer data
    if (stepCount) { // If stepCount is true, send the accelerometer data
      response += String(ax) + "," + String(ay) + "," + String(az);
    }
    else { // If stepCount is off, send only zeros
      response += String(0) + "," + String(0) + "," + String(0);
    }
    // Appends final Photodetector data
    response += "," + String(ppg);
    sendMessage(response);
  }



 

}
