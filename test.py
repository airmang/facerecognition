from utils1 import *
import cv2

# 원하는 이미지 너비와 높이 설정
w, h = 360, 240

# PID 컨트롤러 게인 초기화
pid = [0.7, 0.5, 0]

# 이전 오차 초기화
pError = 0

# 시작 카운터 초기화
startCounter = 0

# 얼굴을 감지하기 위한 Haar Cascade 분류기 초기화
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Tello 드론 초기화
myDrone = initializeTello()

while True:
    # 시작 카운터가 0인 경우 드론 이륙
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # Tello 드론에서 프레임 가져오기
    img = telloGetFrame(myDrone, w, h)

    # 얼굴 감지 함수 호출하여 얼굴 위치와 정보 가져오기
    img, info = findFace(img)

    # 얼굴 추적 함수 호출하여 드론을 얼굴 방향으로 이동시키고 오차 갱신
    pError = trackFace(myDrone, info, w, pid, pError)

    # 이미지 창에 프레임 표시
    cv2.imshow('Image', img)

    # 'q' 키를 누르면 드론 착륙하고 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
