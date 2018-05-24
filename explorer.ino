#include <Servo.h>

const int pinServo = 3,
          Trig = A5,
          Echo = A4,
          default_head = 90,
          in1 = 6,
          in2 = 7,
          in3 = 8,
          in4 = 9,
          ENA = 5,
          ENB = 11,
          ABS = 120,
          ABT = 137,
          distance_changement = 30;
const String end_signal = "EOF";
const unsigned long MEASURE_TIMEOUT = 25000UL; // 25ms = ~8m à 340m/s
const float SOUND_SPEED = 343.0 / 20000; // cm
Servo head;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // activate usb communication
  head.attach(pinServo); // prepare head
  head.write(default_head); // setup head position
  pinMode(Echo, INPUT);
  pinMode(Trig, OUTPUT);
  digitalWrite(Trig, LOW);
  // Wheels pins
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  _mStop();
}

/// ========= MAIN =========
void loop() {
  // put your main code here, to run repeatedly:
  head.write(default_head);
  move_decision();
}

/// ========= DATAS TREATMENT (RASPI) =========
void multiple_scans(int loops) {
  for (int i = 0; i < loops; i++) {
    Serial.println("plan");
    scan_environment(0, 180);
  }
}

void find_self() {
  Serial.println("position");
  scan_environment(60, 120);
}

void scan_environment(int rangeB, int rangeE) {
  if (need_permission() == "measure")
  {
    for (int i = rangeB; i < rangeE; i++) {
      head.write(i);
      send_point_measure();
      delayMicroseconds(MEASURE_TIMEOUT);
    }
    Serial.println(end_signal);
    head.write(default_head);
  }
}

String need_permission() {
  String msg = "";
  char temp = ' ';
  while (!Serial.available()) {
    Serial.println("permission_needed");
    delay(10);
  }
  Serial.println("received");
  msg = receive();
  return msg;
}

String receive() {
  String msg = "";
  char temp = ' ';
  while (Serial.available()) {
    temp = Serial.read();
    if (temp != '\n' or temp != '\r' or temp != ' ') {
      msg += temp;
    }
    return msg;
  }
}

float get_measure() {
  // function to measure distance
  float fdistance = 0;
  long measure = 0;
  delayMicroseconds(MEASURE_TIMEOUT);
  digitalWrite(Trig, LOW);
  delayMicroseconds(3);
  digitalWrite(Trig, HIGH);
  delayMicroseconds(20);
  digitalWrite(Trig, LOW);
  measure = pulseIn(Echo, HIGH, MEASURE_TIMEOUT); // echo time
  fdistance = measure * SOUND_SPEED;
  if (fdistance) {
    fdistance -= 2;
  }
  return fdistance;
}

void send_point_measure() {
  float distance = get_measure(), angle = head.read(); // TOCHANGE
  Serial.print(distance);
  Serial.print(" "); // separator
  Serial.println(angle);
}

/// =========== MOVEMENTS ===========

void move_decision() {
  int middleDistance = get_measure(),
      rightDistance = 0,
      leftDistance = 0; // distances for movements decision
  if (middleDistance <= distance_changement) {
    _mStop();
    // Tests left and right distances
    // RIGHT
    head.write(0);
    rightDistance = get_measure();
    head.write(45);
    rightDistance += get_measure();
    rightDistance /= 2;

    // LEFT
    head.write(180);
    leftDistance = get_measure();
    head.write(135);
    leftDistance += get_measure();
    leftDistance /= 2;

    // Send measures to raspi
    multiple_scans(3);

    // MOVE
    if (rightDistance > leftDistance) {
      _mright();
    }
    else if (rightDistance < leftDistance) {
      _mleft();
    }
    else if ((rightDistance <= distance_changement) or (leftDistance <= distance_changement)) {
      _mBack();
    }

    // RESCAN FOR TESTS
    multiple_scans(3);
    find_self();
  }
  _mForward();
}

void _mStop()
{
  digitalWrite(ENA, LOW);
  digitalWrite(ENB, LOW);
}

void _mForward()
{
  analogWrite(ENA, ABT);
  analogWrite(ENB, ABS);
  digitalWrite(in1, HIGH); //digital output
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void _mBack()
{
  analogWrite(ENA, ABT);
  analogWrite(ENB, ABS);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void _mleft()
{
  analogWrite(ENA, ABT);
  analogWrite(ENB, ABS);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  Serial.println("left");
}

void _mright()
{
  analogWrite(ENA, ABT);
  analogWrite(ENB, ABS);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  Serial.println("right");
}
