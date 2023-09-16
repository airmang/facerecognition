# Tello Drone Face Tracking

이 프로젝트는 Tello 드론을 이용하여 얼굴 추적하는 애플리케이션입니다. OpenCV와 Haar Cascade 분류기를 사용하여 얼굴을 감지하고, PID 컨트롤러를 이용해 드론이 얼굴을 따라가게 합니다.

## 파일 설명

1. `main.py`: 메인 실행 스크립트로서, 웹캠에서 영상을 읽어오고 얼굴 인식 캐스케이드 파일을 읽어옵니다. 인식된 얼굴에 사각형을 출력하며 화면에 출력합니다.
2. `drone_control.py`: Tello 드론 초기화 및 프레임 가져오기, 얼굴 찾기, 얼굴 추적 등의 기능이 구현된 스크립트입니다.
3. `utils.py`: Tello 드론과 관련된 유틸리티 함수들이 정의되어 있는 스크립트입니다.

## 사용 방법

1. 먼저 해당 코드를 클론합니다: 
    ```
    git clone https://github.com/your_username/your_repository.git
    ```

2. 필요한 라이브러리를 설치합니다:
    ```
    pip install -r requirements.txt
    ```

3. 코드를 실행합니다:
    ```
    python main.py
    ```

## 주의 사항

- 이 코드는 Tello 드론과 연결되어 있어야 정상 작동합니다.
- 해당 프로그램은 Python 3.x에서 테스트되었습니다.
