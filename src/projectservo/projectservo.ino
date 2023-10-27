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

char command = 'N'; // 시리얼에서 커맨드 값을 읽어오기 위한 변수
int n = 90;  // 수동 제어 모드일 때 각도를 읽어오기 위한 변수

// 각 모드의 상태 값
bool status = 0;  // 시작-정지. 시작이면 True, 정지면 False
bool mode = 0; // 자동-수동 모드. 자동이면 True, 수동이면 False

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
}

void loop()
{

  if (Serial.available())  // 시리얼 버퍼가 차있을 때만 읽어옴
  {
    command = Serial.read();
    // 시리얼에서 문자를 읽음.
    if (command == 's')  // start 혹은 stop 문자를 읽으면?
    {
      if (status == 1) // 현재 시작 중이라면?
      {
        status = !status; // 시작-정지 상태 반전. 즉, 여기선 정지가 됨.
        mode = 0; // 그리고 모드도 일단 수동 모드로 초기화
      }
      else // 현재 정지 상태라면?
      {
        status = !status; // 시작-정지 상태 반전. 즉, 여기선 시작이 됨.
        mode = 0; // 수동 모드로 초기화.
      }
      
    }
    if (command == 'm') // 자동 혹은 수동 문자를 읽으면?
    {
      mode = !mode;
    }
  }

  if (status == 1) // 장치가 start 상태이고...
  {
    if (mode == 1) // 자동 모드일 경우라면?
    {
      active_auto();  // 자동 모드 실행.
    }
    else  // 그렇지 않으면
    {
      active_manual();  // 수동 모드 실행.
    }  
  }
}

void active_manual()
{
  if (Serial.available())
  {
    n = Serial.parseInt(); // 시리얼에서 서보모터를 기울일 각도를 가져옴.
    //  = command - 48;
    Serial.println(n);
    Servo1.write(n);
    Servo2.write(n);
  }
}

void active_auto()
{
  mpu6050.update();
  Deg_X = mpu6050.getAngleX();
  Deg_Y = mpu6050.getAngleY();
  Deg_Z = mpu6050.getAngleZ();

  Servo1.write(90-Deg_Y);
  Servo2.write(90+Deg_Y);
  //Servo3.write(90-Deg_Z);
  // put your main code here, to run repeatedly:
  Serial.print("Deg_X: "); Serial.print(Deg_X);
  Serial.print(" | Deg_Y: "); Serial.print(Deg_Y);
  Serial.print(" | Deg_Z: "); Serial.print(Deg_Z);
  Serial.print(" | ServoL: "); Serial.print(90-Deg_Y);
  Serial.print(" | ServoR: "); Serial.println(90-Deg_Y);

  n = Deg_Y;  // 자동에서 수동으로 넘어갈 때, 갑작스런 움직임을 방지하기 위함.
}
