int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
  String command = "sleep";
}

void loop() {
  String command = receiveMessage();
//  States
  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if (command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else {
    String message = "Step Count," + command
    writeDisplayCSV(message, 1);
  }


  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);
  }
}
