unsigned long time1 = 0;              //Start time timing variable
unsigned long time2 = 0;                  //End time timing variable


bool buttonpress (){
  if(digitalRead(BUTTON_PIN) == LOW){
    return true;
    }
  else{
    return false;
    }
  }

void resetifpressed (){
      time2 = millis();
       if(!buttonpress()){ // not pressed
            // stay in this state
            time1 = time2;
            }
          else if(buttonpress()){ // if button pressed
            if(time2-time1 >= 2000){
              // go to state zero
              // time1 = time2; // to start counting again idk if i need this line
              Serial.println("RESET PRESSED");
              state = zero_state;
              
              }
            }
         }
