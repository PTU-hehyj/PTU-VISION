from ultralytics import YOLO
import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

# YOLO 모델 로드
model = YOLO("best.pt")

# 첫 번째 비디오 스트리밍 함수
def generate_frame_1():
    cap = cv2.VideoCapture("./Project/input1.mp4")
    return stream_video(cap)

# 두 번째 비디오 스트리밍 함수
def generate_frame_2():
    cap = cv2.VideoCapture("./Project/input2.mp4")  # 다른 비디오 파일
    return stream_video(cap)

# 공통 비디오 스트리밍 로직
def stream_video(cap):
    while True:
        success, frame = cap.read()
        if not success:
            print("프레임 확인")
            break
        
        # 프레임 크기 줄이기
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

        results = model(frame, conf=0.1)
        annotated_frame = results[0].plot()
        detected_objects_count = len(results[0].boxes)

        # 상태 메시지 정의
        status = f"COUNT: {detected_objects_count}"
        if detected_objects_count <= 1:
            status += " => Normal"
            color = (0, 0, 0)  # 검정
        elif detected_objects_count <= 3:
            status += " => Warning"
            color = (255, 0, 0)  # 블루
        else:
            status += " => Danger"
            color = (0, 0, 255)  # 레드
        
        cv2.putText(
            annotated_frame,
            status,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2)
        
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
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

@app.route('/video2')
def video_feed_2():
    return Response(generate_frame_2(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
