int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool saving;
int BUTTON_PIN = 32;

#define ARRAYSIZE 512

// Initialize the arrays as data buffers
int sampleTime1[ARRAYSIZE] = {};
int ax1[ARRAYSIZE] = {};
int ay1[ARRAYSIZE] = {};
int az1[ARRAYSIZE] = {};

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  saving = false;
  writeDisplay("Sleep", 0, true);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

String command = "sleep";
String numStep = "0";
bool heldDown = false;
int buttonState;
int L1Norm;

void loop() {
  String command = receiveMessage();
  // Button Check
  buttonState = digitalRead(BUTTON_PIN);

  // If the button is pressed, send the information
  if (buttonState == LOW && heldDown == false) {
    heldDown = true;
    // Sends the information 
    for (int i = 0; i < ARRAYSIZE; i++) {
      String response = String(sampleTime1[i]) + ",";
      response += String(ax1[i]) + "," + String(ay1[i]) + "," + String(az1[i]);
      sendMessage(response);
    }
  }
  // Used to make sure that it only sends information when the button is pressed
  // and not when it is held down
  else if (buttonState == HIGH) {
    heldDown = false;
  }

  //  States
  if (command == "sleep") {
    saving = false;
    writeDisplay("Sleep", 0, true);
  }
  else if (command == "wearable") {
    saving = true;
    writeDisplay("Wearable", 0, true);
  }
  
  // If the MCU is on, it'll check for changes in the counter
  // MCU entered the wearable state
  else if (saving == true) {
    // Only updates display if the number of Jumping Jacks Count changes
    if (numStep != command) {
      String message = String("Jumping Jacks: ,") + command;
      writeDisplayCSV(message, 1);
      numStep = command;
    }
  }

// If the MCU is collecting accelerometer information
  if (saving && sampleSensors()) {
    //  Save data in arrays
    for (int i = 1; i < ARRAYSIZE; i++) {
      sampleTime1[i - 1] = sampleTime1[i];
    }
    sampleTime1[ARRAYSIZE - 1] = sampleTime;

    for (int i = 1; i < ARRAYSIZE; i++) {
      ax1[i - 1] = ax1[i];
    }
    ax1[ARRAYSIZE - 1] = ax;

    for (int i = 1; i < ARRAYSIZE; i++) {
      ay1[i - 1] = ay1[i];
    }
    ay1[ARRAYSIZE - 1] = ay;

    for (int i = 1; i < ARRAYSIZE; i++) {
      az1[i - 1] = az1[i];
    }
    az1[ARRAYSIZE - 1] = az;
  }
}
