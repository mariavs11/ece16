void setup() {
  // put your setup code here, to run once:
setupDisplay();

}

void loop() {
  // put your main code here, to run repeatedly:
    writeDisplay("Display on Row 0", 0, true);
    delay(1000);
    writeDisplay("Display on Row 1", 1, false);
    delay(1000);
    writeDisplay("Display on Row 2", 2, false);
    delay(1000);
    writeDisplay("Cleared Display", 0, true);
    delay(1000);

}
