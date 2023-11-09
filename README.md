# 프로젝트 소개
<h3>수평 유지 밸런싱 체어</h3>
<h3>험준한 곳에서도 안정감을 유지할 수 있는 밸런싱 의자 구현<h3><h3>지면과 링크의 각도를 기준으로 밸런싱을 측정<h3>  

# 시스템 구조
![Untitled Diagram (3)](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/143505396/83ff6690-b04e-4618-befa-dba7cb806518)

# 조직원
**김태헌** 조장
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

<img src="https://img.shields.io/badge/Ubuntu 22.04-E95420?style=flat-square&logo=Ubuntu&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Arduino-00878F?style=flat-square&logo=Arduino&logoColor=white"/>
<img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>
<img src="https://img.shields.io/badge/Autodesk Fusion 360-000000?style=flat-square&logo=autodesk&logoColor=white"/>
<img src="https://img.shields.io/badge/AMAZON RDS-527FFF?style=flat-square&logo=amazonrds&logoColor=white"/>

# 사용 장비
+ Raspbain 3B+
+ MG-996R

# 구조 및 개념도
## 최종 결과물 3D 모델링
![image](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/146147393/3bf96650-a7c3-47b8-9f93-1a56324ecf90) 

## 시퀸스 다이어그램
![Screenshot from 2023-11-08 15-09-16](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/143505396/4af92f7e-b3aa-41e9-9a83-c10a6f69de26)

안전성을 확인하기 위하여 수동모드를 구현했다. 

변수 Deg_X, Deg_Y, Deg_Z, Target Degree를 데이터베이스에 실시간으로 저장하였다.

# 순서도
## MCU
![Screenshot from 2023-11-07 18-14-23](https://github.com/addinedu-ros-3rd/iot-repo-3/assets/143505396/ea17349c-2ba5-4a4d-abfa-2f13a47d05d0)

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

