
const int X_PIN = A2;
const int Y_PIN = A3; 
const int Z_PIN = A4; 

// defining function
void setupAccelSensor(){
  // assigning inputs pins as inputs
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
  }

  // done 
// defining new function
  void readAccelSensor(){
    // read from pins and store values inside ax, ay and az
    ax = analogRead(X_PIN);
    ay = analogRead(Y_PIN);
    az = analogRead(Z_PIN);
    }
