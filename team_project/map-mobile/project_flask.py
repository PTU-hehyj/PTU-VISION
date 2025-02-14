from ultralytics import YOLO
import cv2
from flask import Flask, Response, render_template, jsonify

app = Flask(__name__)

# YOLO 모델 로드
model = YOLO("best_ver12.pt")

# 현재 상태 저장 변수
current_status = {
    "marker1": {"count": 0, "status": "Normal", "color": (0, 0, 0)},
    "marker2": {"count": 0, "status": "Normal", "color": (0, 0, 0)},
}

# 웹캠 스트리밍 (마커1)
def generate_frame_1():
    cap = cv2.VideoCapture(0)  # 웹캠 사용
    return stream_video(cap, "marker1")

# 영상 파일 스트리밍 (마커2)
def generate_frame_2():
    cap = cv2.VideoCapture("./static/video03.mp4")  # video03.mp4 재생
    return stream_video(cap, "marker2")

# 공통 비디오 스트리밍 함수
def stream_video(cap, marker):
    global current_status

    if not cap.isOpened():
        print(f"{marker} - 비디오 열기 실패")
        return

    while True:
        success, frame = cap.read()
        if not success:
            print(f"{marker} - 프레임 읽기 실패")
            break

        # YOLO 모델 추론
        results = model(frame, conf=0.1)
        annotated_frame = results[0].plot()  # 객체가 그려진 프레임
        detected_objects_count = len(results[0].boxes)

        # 상태 메시지 설정
        status_text = f"COUNT: {detected_objects_count}"
        if detected_objects_count <= 1:
            status_text += " => Normal"
            color = (0, 0, 0)  # 검정
        elif detected_objects_count <= 3:
            status_text += " => Warning"
            color = (255, 0, 0)  # 파랑
        else:
            status_text += " => Danger"
            color = (0, 0, 255)  # 빨강

        # 현재 상태 업데이트
        current_status[marker] = {
            "count": detected_objects_count,
            "status": status_text,
            "color": color
        }

        # 상태 표시 텍스트 추가
        cv2.putText(
            annotated_frame,
            status_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

        # 프레임 크기 조정
        resized_frame = cv2.resize(annotated_frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', resized_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# Flask 라우트
@app.route('/')
def index():
    return render_template("page1.html")

@app.route('/video1')
def video_feed_1():
    return Response(generate_frame_1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video_feed_2():
    return Response(generate_frame_2(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 현재 상태 반환 API
@app.route('/get_status')
def get_status():
    return jsonify(current_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
