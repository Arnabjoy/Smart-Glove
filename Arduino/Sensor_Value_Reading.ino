const int analogInPin =  A0; // Analog input pin for thumb sensor 
const int analogInPin2 = A1; // Analog input pin for index finger sensor 
const int analogInPin3 = A2; // Analog input pin for middle finger sensor 
const int analogInPin4 = A3; // Analog input pin for ring finger sensor 
const int analogInPin5 = A4; // Analog input pin for little finger sensor 
const int analogInPin6 = A5; // Analog input pin for palm sensor 

int thumb_sensorValue = 0, index_sensorValue = 0, // Raw value read from the pin
middle_sensorValue = 0, ring_sensorValue = 0,
little_sensorValue = 0, palm_sensorvalue = 0; 

bool printToSerial = false; // Used for controlling the board
bool label = true; // Used for printing the labels of the sensor value once

String datalabel1 = "Thumb sensor", datalabel2 = "Index sensor",
datalabel3 = "Middle sensor", datalabel4 = "Ring sensor",
datalabel5 = "Little sensor", datalabel6 = "Palm sensor"; 

void setup() {
  // Initialize serial communications at 9600 bps:
  Serial.begin(9600);

  // Initialize pins
  pinMode(analogInPin, INPUT);
  pinMode(analogInPin2, INPUT);
  pinMode(analogInPin3, INPUT);
  pinMode(analogInPin4, INPUT);
  pinMode(analogInPin5, INPUT);
  pinMode(analogInPin6, INPUT);

}

void loop() {
  // Check for incoming commands
  if (Serial.available()) {
    byte command = Serial.read();
    // If command is 0, stop printing
    // If it is 1, start printing
    if (command == '0') {
      digitalWrite(LED_BUILTIN, LOW);
      printToSerial = false;
    } else if (command == '1') {
      digitalWrite(LED_BUILTIN, HIGH);
      printToSerial = true;
    }
  }

  while(label){ // runs once for printing the labels
  Serial.print(datalabel1);
  Serial.print(",");
  Serial.print(datalabel2);
  Serial.print(",");
  Serial.print(datalabel3);
  Serial.print(",");
  Serial.print(datalabel4);
  Serial.print(",");
  Serial.print(datalabel5);
  Serial.print(",");
  Serial.println(datalabel6);
  label = false;
  }

  // Read the analog in value:
  thumb_sensorValue = analogRead(analogInPin);
  index_sensorValue = analogRead(analogInPin2);
  middle_sensorValue = analogRead(analogInPin3);
  ring_sensorValue = analogRead(analogInPin4);
  little_sensorValue = analogRead(analogInPin5);
  palm_sensorvalue = analogRead(analogInPin6);

  if (printToSerial) {
    // Print the results to the Serial Monitor:
    Serial.print(thumb_sensorValue);
    Serial.print(",");
    Serial.print(index_sensorValue);
    Serial.print(",");
    Serial.print(middle_sensorValue);
    Serial.print(",");
    Serial.print(ring_sensorValue);
    Serial.print(",");
    Serial.print(little_sensorValue);
    Serial.print(",");
    Serial.println(palm_sensorvalue);

  }
  
  // Wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading
  delay(2);
}
