


void setup() {
  // put your setup code here, to run once:
setupMotor();
}

void loop() {
  // put your main code here, to run repeatedly:
     deactivateMotor();
     delay(2000);
     activateMotor(127);
     delay(2000);
     activateMotor(255);
     delay(2000);
     activateMotor(90);
     delay(2000);

}
