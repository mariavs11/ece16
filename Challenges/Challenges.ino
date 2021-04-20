int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; 
int ay = 0;
int az = 0;
double numTaps = 0;
int state = 0;
int zero_state = 0;
int counting_state = 1;
int countdown_state = 2;
unsigned long start_time = 0;              //Start time timing variable
unsigned long end_time = 0;  //End time timing variable
int previous_state= 0;
void setupDisplay();
void setupAccelSensor();
void setupMotor();
void writeDisplay(const char * message, int row, bool erase);
bool sampleSensors();
bool detectTaps();
void activateMotor(int motorPower);
void deactivateMotor();
void resetifpressed ();
void readAccelSensor();
bool buttonpress (); 
const int BUTTON_PIN = 14; 

void setup() {
     //initialize button_pin as an input
     pinMode(BUTTON_PIN, INPUT);
     setupDisplay();
     setupAccelSensor();
     setupMotor();
     Serial.begin(9600);
     String message = String(numTaps) + "Taps";
     writeDisplay(message.c_str(), 0, true);
}

void loop() {
  // put your main code here, to run repeatedly:
if(sampleSensors() && Serial.availableForWrite()) {
          Serial.print(ax);
          Serial.print(",");
          Serial.print(ay);
          Serial.print(",");
          Serial.println(az);
          
       // state zero 

       if(state == zero_state){
          if(detectTaps()){
            deactivateMotor(); // stops buzzing
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            previous_state = 0;
            state = counting_state; // sets state to counting
            }
          else {
            previous_state = 0;
            numTaps = 0;
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            activateMotor(255); // starts buzzing to the highest intensity 
            
            }
          
        }
        // done with state zero
        // counting state
       if(state == counting_state){
            Serial.println("INSIDE COUNTING");
          resetifpressed();
          end_time = millis(); // initialized to zero 
          if(detectTaps()){
             if (previous_state == 0 ){ // stalls until it's ready to count
              String message = String(numTaps) + "Taps";
              writeDisplay(message.c_str(), 0, true); // writes onto display
              previous_state = counting_state;  
              Serial.println("TAP1");
              } 
     
            else if ( previous_state == counting_state or  previous_state == 2 ){ 
            Serial.println("TAP2"); 
            numTaps+=1;
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            start_time = end_time;
            
             }     
          }
            // still in counting state 
            
          else if(end_time-start_time >= 4000){
            // no taps detected in 4 s
            Serial.println("GOING INTO COUNTDOWN");
            state = countdown_state;
            }
        }
       // done with counting state
       // countdown state

       if(state == countdown_state){ // countdown state
           Serial.println(" INSIDE COUNTDOWN ");
          resetifpressed();   // if button pushed for 2+s goes to zero_state
          if( previous_state == 1 ){

            if(numTaps == 0 ){
              state = zero_state;
               }
            else{ 
            numTaps-=1;
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            Serial.println("TAP IN");
              }
          }
         // no taps detected : keep counting down
          if (!detectTaps()){
              // go to state zero           
              if(numTaps == 0 ){
              state = zero_state;
              }
            else {
            numTaps-=1;
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            Serial.println("TAP IN");
               }
            
             }
          else {
            numTaps+=1;
            String message = String(numTaps) + "Taps";
            writeDisplay(message.c_str(), 0, true); // writes onto display
            Serial.println("TAP IN COUNTDOWN");
            previous_state = countdown_state; // sets to 2
            state = counting_state; 
            start_time= millis(); // for keeping track in case 4 seconds pass (it will be useful inside counting_state)
            Serial.println(state);
            } 

          }
        }

       // done
       
         
     }
