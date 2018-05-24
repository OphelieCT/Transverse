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
          ABS = 170,
          ABT = 171,
          distance_changement = 30,
          del = 500;
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
  delay(500);
}

/// ========= DATAS TREATMENT (RASPI) =========
void multiple_scans(int loops, String order) {
  for (int i = 0; i < loops; i++) {
    need_permission(order);
    scan_environment(0, 180, "measure");
    delay(100);
  }
}

void find_self() {
  need_permission("position");
  scan_environment(30, 160, "measure");
}

void scan_environment(int rangeB, int rangeE, String perm) {
  if (need_permission(perm) == "measure")
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

String need_permission(String perm) {
  String msg = "";
  while (!Serial.available()) {
    Serial.println(perm);
    delay(500);
  }
  msg = receive();
  Serial.println("received");
  return msg;
}

String receive() {
  String msg = "";
  char temp = ' ';
  while (Serial.available()) {
    temp = Serial.read();
    if ((97 <= temp and temp <= 122) or ( 65 <= temp and temp <= 90)) {
      msg += temp;
    }
  }
  return msg;
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
    head.write(90);
    // Send measures to raspi
    find_self();
    multiple_scans(3, "plan");

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
    delay(del);
    _mStop();
    // RESCAN FOR TESTS
    multiple_scans(3, "plan");
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
  need_permission("left");
}

void _mright()
{
  analogWrite(ENA, ABT);
  analogWrite(ENB, ABS);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  need_permission("right");
}
