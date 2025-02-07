import cv2
import numpy as np
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from ultralytics import YOLO

# Flask 앱 초기화
app = Flask(__name__)

# SocketIO 객체 생성 시 CORS 설정
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 허용 설정

# YOLO 모델 로드 (best.pt 모델)
model = YOLO("best.pt")  # 학습된 best.pt 모델 로드

# 기본 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')  # index.html 템플릿 반환

# 카메라 스트리밍을 위한 함수 (실시간 스트리밍 및 모델 추론)
def gen():
    cap = cv2.VideoCapture(0)  # 카메라 연결
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지를 모델에 맞게 전처리 (YOLO 모델은 640x640 입력을 사용)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 색상 공간 변환 (BGR -> RGB)
        img = cv2.resize(img, (640, 640))  # YOLO 모델에 맞는 크기로 리사이즈
        img = np.array(img) / 255.0  # YOLO 모델에 맞게 정규화

        # YOLO 모델을 사용하여 추론
        results = model(img)  # 모델 추론
        predictions = results.pred[0]  # 첫 번째 이미지에서 예측된 결과

        # 결과에서 예측된 객체 정보 추출
        labels = model.names  # 클래스 이름 (예: 'animals', 'stroller' 등)

        # 예측된 객체에 대한 로그 출력
        print(f"Predictions: {predictions}")  # 추론된 결과 로그 출력

        # 예측된 객체에 사각형과 레이블 표시
        for *box, conf, cls in predictions:
            label = labels[int(cls)]  # 클래스 레이블
            confidence = conf.item()

            # 객체가 감지되었을 때 사각형 표시
            if confidence > 0.1:  # 신뢰도가 10% 이상인 경우에만 표시
                print(f"Detected: {label} with confidence {confidence}")  # 디버깅을 위한 로그 추가
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # 'animals' 클래스가 감지되었을 때만 메시지 출력
            if label.lower() == 'animals':  # 'animals' 클래스를 감지했을 경우
                print("Detected: Dog or Animal!")  # 로그 출력
                cv2.putText(frame, "Dog or Animal Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (50, 50), (300, 300), (0, 255, 0), 2)  # 감지 박스

        # MJPEG 스트리밍을 위한 이미지 인코딩
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

# 카메라 스트리밍을 위한 video_feed 라우트
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# WebSocket을 통한 실시간 데이터 처리 (예: 카메라 스트리밍 처리)
@socketio.on('camera_stream')
def handle_camera_stream(data):
    # 클라이언트에서 받은 스트리밍 데이터를 처리
    print("Received camera stream data")  # 클라이언트로부터 받은 스트리밍 데이터 로그 출력
    emit('stream', data, broadcast=True)  # 받은 데이터를 다른 클라이언트로 전송

# WebSocket 연결 시 처리
@socketio.on('connect')
def handle_connect():
    print("Client connected")  # 클라이언트 연결 시 로그 출력
    emit('message', {'data': 'Connected to server'})  # 연결 메시지 전송

# 실행
if __name__ == '__main__':
    print("Starting the Flask app...")  # 서버 시작 로그 출력
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
