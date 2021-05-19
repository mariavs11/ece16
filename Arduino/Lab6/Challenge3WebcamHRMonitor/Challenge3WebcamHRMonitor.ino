/*
   Global variables
*/
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
String currentHR = "";
int firstpeak = 0;
/*
   Initialize the various components of the wearable
*/
void setup() {
  setupCommunication();
  setupDisplay();
  // setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

/*
   The main processing loop
*/



void loop() {
  String command = receiveMessage();
  if (command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if (command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if (sending){
    if(command == "NOT ENOUGH DATA" & firstpeak == 0){
      writeDisplay("No peaks", 0, true);
      firstpeak = 1; 
      }
     else  {
      // update OLED if heart rate changed
      if (currentHR != command) { 
          String displaymessage = "HR: " + command ;
          writeDisplay(displaymessage.c_str(), 0, true); // displays HR
          currentHR = command;
        }
      }
    }
  

}
