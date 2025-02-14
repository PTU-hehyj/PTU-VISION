from ultralytics import YOLO
import cv2
from flask import Flask, Response, render_template, jsonify

app = Flask(__name__)

# YOLO 모델 로드
model = YOLO("yolov8s.pt")
socketio = SocketIO(app)  # SocketIO 객체 생성
# 현재 상태 저장 변수
current_status = {
    "marker1": {"count": 0, "status": "Normal", "color": (0, 0, 0)},  # marker1에 대한 상태
}

# 첫 번째 웹캠 스트리밍 함수
def generate_frame_1():
    cap = cv2.VideoCapture(0)  # 웹캠 사용
    return stream_video(cap, "marker1")

# 공통 비디오 스트리밍 로직
def stream_video(cap, marker):
    global current_status
    
    if not cap.isOpened():  # 카메라 연결 확인
        print("카메라 열기 실패")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            print("프레임 읽기 실패")
            break
        
        # YOLO 모델 추론
        results = model(frame, conf=0.1)
        annotated_frame = results[0].plot()  # 객체가 그려진 프레임
        detected_objects_count = len(results[0].boxes)  # 탐지된 객체 수

        # 상태 메시지 정의
        status_text = f"COUNT: {detected_objects_count}"
        if detected_objects_count <= 1:
            status_text += " => Normal"
            color = (0, 0, 0)  # 검정
        elif detected_objects_count <= 3:
            status_text += " => Warning"
            color = (255, 0, 0)  # 블루
        else:
            status_text += " => Danger"
            color = (0, 0, 255)  # 레드

        # 현재 상태 업데이트
        current_status[marker] = {
            "count": detected_objects_count,
            "status": status_text,
            "color": color
        }

        # 텍스트 추가 (객체 수와 상태를 이미지에 표시)
        cv2.putText(
            annotated_frame,
            status_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        # 이미지 해상도 축소
        resized_frame = cv2.resize(annotated_frame, (640, 480))  # 원하는 해상도로 축소
        _, buffer = cv2.imencode('.jpg', resized_frame)
        frame_bytes = buffer.tobytes()

        # Base64로 인코딩하여 클라이언트에 전송 (불필요한 부분 제거)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()


# Flask 라우트 설정
@app.route('/')
def index():
    return render_template("page1.html")

@app.route('/video1')
def video_feed_1():
    return Response(generate_frame_1(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 현재 상태를 반환하는 API
@app.route('/get_status')
def get_status():
    return jsonify(current_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
