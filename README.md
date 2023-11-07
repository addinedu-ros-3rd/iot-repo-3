# 주제: Self-Balancing Chair
+ Self-Balancing Chair를 통해서 간이 댐퍼를 구현함으로써 흔들림을 감소시켜 편안한 승차감을 제공하는 것이 목적.
+ 실제 댐퍼는 유압 실린더를 사용한다는 점에서 기계적인 구조는 다르지만 HW 제어 방법은 동일하기 때문에 Servo Motor로 대체.

# 조직원
**김태헌 조장**
+ UI 제작 및 DB 구축
+ MCU, DB 연동

**박성준**
+ 수평 유지 알고리즘
+ 구조물 기울기 시각화

**홍석진**
+ 로봇 링크 구성
+ 3D 모델링 및 출력
+ 구조물 안전성 점검 및 개선

# 사용 툴 
+ Window10
  + Autodesk Fusion360
+ Ubuntu 22.04
  + Arduino IDE
  + Vscode

# 사용 장비
+ Raspbain 3B+
+ Amazon RDS
+ Arduino uno
+ MG-996R

# 구조 및 개념도
## 최종 결과물 3D 모델링
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/3bf96650-a7c3-47b8-9f93-1a56324ecf90) 

## 시스템 구조
![Untitled Diagram (3)](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/143505396/83ff6690-b04e-4618-befa-dba7cb806518)

## DB
![Screenshot from 2023-11-07 13-42-16](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/143505396/88d7b755-baed-4a36-b974-cb475cb4cf30)

변수 5개 Deg_X, Deg_Y, Deg_Z, Servo R, Servo L를 데이터베이스에 실시간으로 저장하였다.

# 순서도
## MCU
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/4b2f5ef3-edb4-48ad-8f19-d8525d8412cd)

## AUTO Mode
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/2392ad6b-61fd-4ad9-8796-62dcf27f3c48)

## MANUAL Mode
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/7406febb-ccf5-4081-95e3-73543f5e14a1)

# UI
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/3f48f908-1141-411d-839a-1d16ebdc1dbc)

1.STATUS. 아두이노의 status 변수에 따라 값이 변함.
+ status = 1일 경우, ON으로 표시되어 제품이 수동/자동 모드로 동작될 수 있는 상태.
+ status = 0일 경우, OFF로 표시되어 제품이 어떠한 동작을 하지 않는 상태.

2.Mode. 아두이노의 Mode 변수에 따라 값이 변함.
+ Mode = 1일 경우, AUTO로 표시되어 제품이 자동 모드로 동작.
+ Mode = 0일 경우, MANUAL로 표시되어 제품이 수동 모드로 동작

3.시작/정지 버튼: 누를 경우 시리얼 통신으로 아두이노에 's'라는 문자를 전달.
+ status = 1일 경우, '정지'로 표시되어 제품이 OFF 모드에 들어갈 수 있다는 것을 표시.
+ status = 0일 경우, '시작'으로 표시되어 제품이 ON 모드에 들어갈 수 있다는 것을 표시.

4.자동/수동 버튼: 누를 경우 시리얼 통신으로 아두이노에 'm'이라는 문자를 전달.
* 자동으로 밸런싱 의자가 작동하기 전에 테스트용으로 확인하기 위해서 의도적으로 수동 설정 추가함.   
+ mode = 1일 경우, '수동'으로 표시되어 제품이 '자동' 모드에 들어갈 수 있다는 것을 표시.
+ mode = 0일 경우, '자동'으로 표시되어 제품이 '수동' 모드에 들어갈 수 있다는 것을 표시.

5.각도 설정
+ 버튼 각도 : 수동 모드에서만 동작. 각도를 입력하면 8번에 각도가 표시되고, set을 눌러 기울기 각도를 반영.
+ 슬라이더 각도  : 슬라이더를 이동시키면 값이 8번에 나타남. 5번의 set을 눌러 기울기 각도를 반영.

6.(미구현) 기울기 시각화
+ 현재 제품의 기울기를 시각적으로 표현

# HW 테스트
<p>
<img src="https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/1a06b8bf-b6ab-437a-9204-3089748e1502">
</p>

# 기울기 시각화 테스트
<p aling="center">
<img src="https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/249c65d6-2cfa-49ad-b56c-311da40c7e41">
</p>

# 결과물 테스트
<p aling="center">
<img src="https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/b0c172eb-9457-4566-b3ed-cfee55c09b50">
</p>

# 결론 
UART 통신으로 아두이노와 PyQt 통신 성공.
x축으로 수평 제어할 수 있었고 이를 graphwidget으로 x축 기울기 실기산 변화를 시각화함.

# 향후 계획
기계적 구조를 변형하여 X, Y축에 대한 수평을 유지할 수 있도록 제품을 개선할 것.

