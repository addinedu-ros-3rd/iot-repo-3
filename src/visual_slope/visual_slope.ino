#include <Servo.h>
#include <MPU6050_tockn.h>
#include <Wire.h>

//MPU6050 객체 선언
MPU6050 mpu6050(Wire);

//SERVO 신호 선 설정 및 서보 객체 선언.
int Servo_Pin1 = 9;
int Servo_Pin2 = 10;

Servo Servo1;
Servo Servo2;

//X,Y,Z축 각도를 받아올 변수 선언
int Deg_X;
int Deg_Y;
int Deg_Z;

void setup() {
  //MPU사용 ON
  Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();

  //서보모터 사용할 핀 연결
  Servo1.attach(Servo_Pin1);
  Servo2.attach(Servo_Pin2);

  // 서보모터 초기 각도 설정
  Servo1.write(90);
  Servo2.write(90);
  // put your setup code here, to run once:

}

void loop() {
  mpu6050.update();
  Deg_X = mpu6050.getAngleX();
  Deg_Y = mpu6050.getAngleY();
  Deg_Z = mpu6050.getAngleZ();

  Servo1.write(90-Deg_Y);
  Servo2.write(90+Deg_Y);
  //Servo3.write(90-Deg_Z);
  // put your main code here, to run repeatedly:
  Serial.print(Deg_X); Serial.print("|");
  Serial.print(Deg_Y); Serial.print("|");
  Serial.print(Deg_Z); Serial.print("|");
  Serial.print(90-Deg_Y); Serial.print("|");
  Serial.println(90-Deg_Y);
}
