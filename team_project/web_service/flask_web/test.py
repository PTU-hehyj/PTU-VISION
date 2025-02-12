import numpy as np

"""
# 특정 좌표 설정
region_points = {
    "region-01" : [(x // 5, y // 5) for x, y in [(798, 199), (94, 1042), (919, 1035), (1213, 36)]] # 리스트 컨프리헨션 사용용
}

print(region_points)
"""

# 비디오 영상 내 구간 좌표 검색하기
import cv2

# 비디오 객체 생성q
cap = cv2.VideoCapture("C:/Users/USER/Documents/dogfind/PTU-VISION/team_project/web_service/flask_web/static/video05.mp4")
# cap = cv2.VideoCapture(0)

path_list = []
xyTuple = ()
# 마우스 이벤트 처리 함수
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"CLICKED : {x}, {y}")
        xyTuple = (x,y)
        path_list.append(xyTuple)

# 윈도우 생성
cv2.namedWindow("cap")

# 콜백 함수 등록
cv2.setMouseCallback("cap", mouse_callback)

# 비디오 프레임 읽기 및 종료
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("프레임 확인 요청")
        break
    
    cv2.imshow("cap", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    

# 비디오 해제
cap.release()
cv2.destroyAllWindows()


print(path_list)