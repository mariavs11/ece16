String receiveMessage();


void setup() {
  // put your setup code here, to run once:
  // Serial.begin(115200)
  setupCommunication();
  setupDisplay();
  
}

void loop() {
  String message = receiveMessage();
  if(message != "") {
    writeDisplayCSV(message.c_str(), 1);
    sendMessage(message);
  }

}
