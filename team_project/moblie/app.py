import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import base64

# Flask 앱 초기화
app = Flask(__name__)

# SocketIO 객체 생성 시 CORS 설정
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 허용 설정

# YOLO 모델 로드 (best.pt 모델)
model = YOLO("yolov8s.pt")  # 학습된 best.pt 모델 로드

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
        results = model(frame)  # 모델 추론
        predictions = results[0].plot()

        # 객체 수 갱신
        object_count = len(results[0].boxes)  # 탐지된 객체의 개수

        # MJPEG 스트리밍을 위한 이미지 인코딩
        ret, jpeg = cv2.imencode('.jpg', predictions)
        if ret:
            frame_bytes = jpeg.tobytes()

            # Base64로 인코딩하여 클라이언트로 전송
            image_data = base64.b64encode(frame_bytes).decode('utf-8')
            
            # SocketIO를 통해 객체 탐지 결과와 이미지 전송
            socketio.emit('object_count', {'object_count': object_count})  # 실시간 객체 수 전송

            # MJPEG 스트리밍 형식으로 이미지 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()

# 메인 페이지 (index)에서 HTML 템플릿을 렌더링
@app.route('/')
def index():
    return render_template('index.html')  # 템플릿 파일에서 이미지 스트리밍과 텍스트를 표시

# 카메라 스트리밍
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# WebSocket 연결 시 처리
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to server'})  # 연결 메시지 전송

# 실행
if __name__ == '__main__':
    print("Starting the Flask app...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
