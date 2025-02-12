from ultralytics import YOLO, solutions
import cv2
from flask import Flask, Response, render_template, jsonify
import numpy as np

app = Flask(__name__)

# 현재 상태 저장 변수
current_status = {
    "marker1": {"count": 0, "status": "Normal", "color": "black"},
    "marker2": {"count": 0, "status": "Normal", "color": "black"},
}

# 첫 번째 비디오 스트리밍 함수
def generate_frame_1():
    cap = cv2.VideoCapture("C:/Users/USER/Documents/dogfind/PTU-VISION/team_project/web_service/flask_web/static/video05.mp4")

    # 특정 좌표 설정
    region_points = {
        "region-01": [(x // 2, y // 2) for x, y in [(17, 20), (1906, 12), (1906, 1043), (582, 1038)]]
    }

    region = solutions.RegionCounter(
        show=True,
        region=region_points,
        model='C:/Users/USER/Documents/dogfind/PTU-VISION/team_project/web_service/flask_web/best_ver12.pt', # 모델로드
        region_color = (34, 34, 178),
        conf=0.1 
    )

    return stream_video(cap, "marker1", region)


# 두 번째 비디오 스트리밍 함수
def generate_frame_2():
    cap = cv2.VideoCapture("C:/Users/USER/Documents/dogfind/PTU-VISION/team_project/web_service/flask_web/static/video03.mp4")

    region_points = {
        "region-01": [(x // 2, y // 2) for x, y in [(0, 598), (6, 1043), (1908, 1046), (1908, 4), (641, 250)]]
    }

    region = solutions.RegionCounter(
        show=True,
        region=region_points,
        model='C:/Users/USER/Documents/dogfind/PTU-VISION/team_project/web_service/flask_web/best_ver9.pt',
        region_color = (34, 34, 178),
        conf=0.1
    )

    return stream_video(cap, "marker2", region)


# 공통 비디오 스트리밍 로직
def stream_video(cap, marker, region):
    global current_status
    while True:
        success, frame = cap.read()
        if not success:
            print("프레임 확인")
            break

        # 프레임 크기 줄이기
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

        # 특정 구역 내 객체 탐지 (YOLO 중복 실행 방지)
        frame, obj_list = region.count(frame) # solutions.RegionCounter.count 내부 클래스에서 필터링 코드 수정 확인 가능능

        print(f"어떤 객체가 인식됐는가?: {obj_list}") # 특정 영역 내에 원하는 인식 객체 이름
        detected_objects_count = len(obj_list) # 객체 인식 총 갯수수



        # 상태 메시지 정의
        status = f"COUNT: {detected_objects_count}"
        print(status)
        if detected_objects_count <= 1:
            status += "Normal"
            color = "black"
        elif detected_objects_count <= 3:
            status += "Warning"
            color = "blue"
        else:
            status += "Danger"
            color = "red"

        # 상태 저장
        current_status[marker] = {"count": detected_objects_count, "status": status, "color": color}

        _, buffer = cv2.imencode('.jpg', frame)
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

# 현재 상태를 반환하는 API
@app.route('/get_status')
def get_status():
    return jsonify(current_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
