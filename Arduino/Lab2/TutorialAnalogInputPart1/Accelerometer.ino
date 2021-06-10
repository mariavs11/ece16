// Initialize accel. analog pins (A0-5)
const int X_PIN = A4;
const int Y_PIN = A3;
const int Z_PIN = A2;

void setupAccelSensor() {
  pinMode(X_PIN,INPUT);
  pinMode(Y_PIN,INPUT);
  pinMode(Z_PIN,INPUT);
}

void readAccelSensor() {
  ax = analogRead(X_PIN);
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
}
