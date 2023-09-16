from djitellopy import Tello
import cv2
import numpy as np

# Tello 드론 초기화 함수
def initializeTello():
    # Tello 객체 생성
    myDrone = Tello()
    # Tello 드론과 연결
    myDrone.connect()
    # 드론의 속도 및 이동 속도 초기화
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    # 드론 배터리 상태 출력
    print(myDrone.get_battery())
    # 비디오 스트리밍 끄기
    myDrone.streamoff()
    # 비디오 스트리밍 켜기
    myDrone.streamon()
    return myDrone

# Tello 드론 프레임 가져오는 함수
def telloGetFrame(myDrone, w=360, h=240):
    # Tello 드론에서 프레임 읽기
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    # 프레임 크기 조정
    img = cv2.resize(myFrame, (w, h))
    return img

# 얼굴을 찾는 함수
def findFace(img):
    # Haar Cascade 분류기를 사용하여 얼굴을 찾음
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 이미지를 흑백으로 변환
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 얼굴 검출
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)

    myFaceListC = []
    myFaceListArea = []

    for(x, y, w, h) in faces:
        # 찾은 얼굴 주위에 사각형 그리기
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    if len(myFaceListArea) != 0:
        # 가장 큰 얼굴 선택
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        # 얼굴을 찾지 못한 경우 빈 리스트 반환
        return img, [[0, 0], 0]

# 얼굴을 추적하는 함수
def trackFace(myDrone, info, w, pid, pError):
    # 오차 계산
    error = info[0][0] - w // 2
    # PID 컨트롤러를 사용하여 이동 속도 계산
    speed = pid[0] * error + pid[1] * (error - pError)
    # 이동 속도를 일정 범위 내로 제한
    speed = np.clip(speed, -100, 100)
    speed = int(speed)
    print(speed)

    if info[0][0] != 0:
        # 얼굴이 감지된 경우 드론의 yaw_velocity 설정
        myDrone.yaw_velocity = speed
    else:
        # 얼굴을 찾지 못한 경우 드론 이동 및 yaw_velocity 초기화
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
    if myDrone.send_rc_control:
        # 드론에 RC 제어 명령을 보냄
        myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity, myDrone.up_down_velocity, myDrone.yaw_velocity)

    return error
