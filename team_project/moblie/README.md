README.md
# YOLO 기반 객체 탐지 및 실시간 비디오 스트리밍 웹 애플리케이션
본 애플리케이션은 YOLO (You Only Look Once) 모델을 활용하여 실시간 객체 탐지를 수행하고, 노트북의 웹캠을 통해 인식된 화면을 모바일 웹에서 실시간으로 스트리밍할 수 있는 시스템입니다. 이를 통해 사용자는 자신의 핸드폰에서 직접 웹캠을 통해 탐지된 객체들의 실시간 정보를 확인할 수 있습니다.

## 주요 기능
실시간 객체 탐지: 노트북 웹캠을 통해 실시간으로 영상 데이터를 캡처하고, YOLO 모델을 사용하여 각 프레임에서 객체를 탐지합니다.
비디오 스트리밍: 노트북에서 실시간으로 전송되는 비디오 스트림을 웹 서버를 통해 모바일 웹 브라우저에서 스트리밍합니다.
모바일 호환: 핸드폰에서 해당 웹 페이지에 접속하여, 웹캠에서 인식한 객체들을 실시간으로 확인할 수 있습니다.
실시간 객체 수 표시: 탐지된 객체의 수를 실시간으로 업데이트하여 사용자가 얼마나 많은 객체가 탐지되었는지 확인할 수 있습니다.

## 동작 방식
### 노트북 웹캠으로 객체 탐지:

노트북의 웹캠을 통해 실시간 영상을 캡처합니다.
캡처된 영상은 YOLO 모델에 의해 처리되어, 각 프레임에서 객체들이 탐지됩니다.
탐지된 객체의 수는 웹 페이지에 실시간으로 전달되며, 객체 탐지 결과가 업데이트됩니다.

### 핸드폰에서 실시간 스트리밍:

Flask 서버와 SocketIO를 사용하여, 노트북에서 인식된 실시간 비디오 스트리밍을 모바일 웹으로 전송합니다.
사용자는 모바일 브라우저에서 해당 웹 페이지에 접속함으로써, 자신의 핸드폰 화면에서 실시간으로 객체 탐지와 비디오 스트리밍을 확인할 수 있습니다.

### ngrok을 이용한 HTTPS 보안 설정:

웹캠에서 실시간 스트리밍을 하기 위해서는 HTTPS 연결이 필수적입니다.
ngrok을 사용하여 로컬 서버를 안전한 HTTPS 프로토콜로 포워딩하여 모바일 브라우저에서 원활하게 접속할 수 있도록 지원합니다.
이 방법을 통해 외부에서도 안전하게 접속할 수 있습니다.

## 기술 스택

YOLO: 객체 탐지를 위한 딥러닝 모델 (YOLOv5 사용)
Flask: Python 웹 프레임워크, 실시간 비디오 스트리밍 및 객체 탐지 결과 제공
SocketIO: 실시간 데이터 통신을 위한 라이브러리
ngrok: 로컬 개발 서버를 HTTPS로 안전하게 포워딩하여 외부에서 접근 가능하도록 설정

### Flask와 SocketIO로 구현한 웹 애플리케이션입니다.
Flask는 웹 애플리케이션을 구축하는 데 사용되며, 이를 통해 웹 서버를 설정하고 실시간 비디오 스트리밍을 제공합니다.
SocketIO는 웹소켓을 사용하여 실시간 통신을 가능하게 합니다. 이로 인해 서버와 클라이언트 간의 실시간 객체 탐지 결과와 영상 데이터를 동적으로 업데이트할 수 있습니다.


## 파일 구성

```
/yolo-app
│
├── app.py                     # Flask 서버 코드
├── /templates                 # HTML 템플릿 폴더
│   └── index.html             # 기본 웹 페이지 템플릿
├── /static                    # 정적 파일 폴더 (CSS, JS, 이미지)
│   ├── /css
│   │   └── style.css          # CSS 파일 (선택 사항)
│   ├── /js
│   │   └── script.js          # JavaScript 파일 (클라이언트 로직)
└── yolo_model.h5              # YOLO 모델 파일 (예시)
```
### 1. AWS EC2 설정
AWS EC2 가입 및 인스턴스 생성: AWS EC2 공식 문서를 참조하여 EC2 인스턴스를 생성합니다.
Key Pair 권한 설정: EC2 인스턴스를 생성할 때 Key Pair를 설정하고, SSH 접속을 위한 키 파일을 로컬에 저장합니다.
보안 그룹 설정: 보안 그룹에서 5000 포트를 열어 Flask 서버에 접근할 수 있도록 설정합니다.
### 2. EC2 인스턴스 접속
CMD 실행 (Windows):
cd "C:\Users\young\OneDrive\바탕 화면\"와 같이 Key Pair가 있는 디렉토리로 이동합니다.
ssh -i "for_laptop.pem" ec2-user@[인스턴스 주소] 명령어를 통해 EC2 인스턴스에 접속합니다.
### 3. 기본 패키지 설치
시스템 패키지 업데이트:
```
sudo apt-get update
```
Python3 설치:
```
sudo apt-get install python3
```
pip 설치:
```
sudo apt-get install python3-pip
```
가상환경 관리자 설치:
```
sudo apt-get install python3-pip
```
### 4. 가상환경 설정
프로젝트를 위한 독립된 Python 환경을 만들어 패키지 충돌을 방지합니다:

가상환경 생성:
```
virtualenv dogserver
```
가상환경 디렉토리로 이동:
```
cd dogserver
```
가상환경 활성화:
```
source ./bin/activate
```
Flask 설치:
```
pip install flask
```
### 5. Flask 애플리케이션 설정
애플리케이션 파일을 생성하고 편집합니다:

파일 존재 여부 확인: ```ls```

새 파일 생성 및 편집: ```nano app.py```

### 6. 파일 저장 방법
nano 에디터에서 코드를 입력한 후:

Ctrl + X를 눌러 저장 모드로 진입
'Y'를 입력하여 저장 확인
파일명 확인 후 Enter로 저장 완료
### 7. Flask 서버 실행
서버를 실행하고 동작을 확인합니다:

python3 app.py
### 8. 인바운드 규칙 수정
EC2 보안 그룹에서 포트 5000을 열어 Flask 서버에 접근할 수 있도록 설정해야 합니다.
보안 그룹의 인바운드 규칙에 다음과 같이 설정합니다:

Type: Custom TCP Rule
Port Range: 5000
Source: 0.0.0.0/0 (모든 IP 허용)
이 설정 후, 외부에서 EC2 인스턴스의 5000번 포트로 접속할 수 있습니다.

### 9. index.html 파일
index.html 파일은 클라이언트 측에서 비디오 스트리밍과 객체 탐지 결과를 표시하는 템플릿 파일입니다. 해당 파일은 다음과 같은 내용을 포함하고 있습니다:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Feed</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script> <!-- SocketIO 라이브러리 추가 -->
    <script>
        // SocketIO 연결
        const socket = io();

        // 객체 개수 업데이트 함수
        socket.on('object_count', (data) => {
            document.getElementById('object_count').textContent = 'Objects detected: ' + data.object_count;
        });
    </script>
</head>
<body>
    <h1>Live Video Feed</h1>
    <img src="{{ url_for('video_feed') }}" width="100%" />
    <div>
        <h2 id="object_count">Objects detected: 0</h2> <!-- 객체 수를 표시할 부분 -->
    </div>
</body>
</html>
```
이 HTML 파일은 실시간으로 카메라 비디오 스트리밍을 표시하고, 객체가 탐지되면 탐지된 객체의 수를 화면에 업데이트합니다.
### 10. app.py (Flask 서버 코드)
Flask 애플리케이션 코드입니다. YOLO 모델을 사용하여 객체 탐지를 수행하고, MJPEG 스트리밍을 통해 클라이언트에 실시간 비디오를 제공합니다. 또한, SocketIO를 사용하여 객체 수를 클라이언트에 실시간으로 전송합니다.
```
import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import base64

# Flask 앱 초기화
app = Flask(__name__)

# SocketIO 객체 생성 시 CORS 설정
socketio = SocketIO(app, cors_allowed_origins="*")

# YOLO 모델 로드
model = YOLO("yolo_model.h5")  # YOLO 모델 파일 로드

# 객체 수를 저장하는 변수
object_count = 0

# 카메라 스트리밍을 위한 함수 (실시간 스트리밍 및 모델 추론)
def gen():
    global object_count  # 객체 수를 전역 변수로 사용

    cap = cv2.VideoCapture(0)  # 카메라 연결

    if not cap.isOpened():  # 카메라 연결 확인
        print("카메라 열기 실패")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print("프레임 확인 실패")
            break

        # YOLO 모델을 사용하여 추론
        results = model(frame)
        predictions = results[0].plot()

        # 객체 수 갱신
        object_count = len(results[0].boxes)

        # MJPEG 스트리밍을 위한 이미지 인코딩
        ret, jpeg = cv2.imencode('.jpg', predictions)
        if ret:
            frame_bytes = jpeg.tobytes()

            # Base64로 인코딩하여 클라이언트로 전송
            image_data = base64.b64encode(frame_bytes).decode('utf-8')

            # SocketIO를 통해 객체 탐지 결과와 이미지 전송
            socketio.emit('object_count', {'object_count': object_count})

            # MJPEG 스트리밍 형식으로 이미지 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# 카메라 스트리밍
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# WebSocket 연결 시 처리
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to server'})

# 실행
if __name__ == '__main__':
    print("Starting the Flask app...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```
### 11. ngrok을 통한 HTTPS 설정
웹 애플리케이션이 HTTP를 사용하게 되면, 모바일 장치에서 보안 문제로 인해 카메라를 사용할 수 없을 수 있습니다. 이를 해결하기 위해 ngrok을 사용하여 로컬 서버를 HTTPS로 포워딩할 수 있습니다.

설정 방법
ngrok 다운로드 및 설치: ngrok 다운로드 페이지에서 운영체제에 맞는 ngrok을 다운로드하여 설치합니다.

ngrok 실행: ngrok을 실행하여 로컬 Flask 서버를 HTTPS로 포워딩합니다. 터미널에서 다음 명령어를 입력합니다:

ngrok http 5000
ngrok URL 확인: ngrok이 실행되면, https://xxxxxx.ngrok.io와 같은 HTTPS URL이 생성됩니다. 이 URL을 통해 외부에서 안전하게 접속할 수 있습니다.

모바일에서 접속: 생성된 ngrok HTTPS URL을 모바일 브라우저에 입력하여 카메라와 객체 탐지를 테스트할 수 있습니다.

### ngrok을 사용한 이유
HTTPS 보안: 모바일 브라우저에서 HTTP로 카메라를 사용할 수 없는 경우, HTTPS를 통해 보안을 강화하고 웹 애플리케이션을 안전하게 사용할 수 있습니다.
외부 접속: ngrok을 사용하면, 로컬 서버를 인터넷상에서 안전하게 외부와 연결할 수 있어, 외부 기기에서 서버에 접근할 수 있습니다.
