import cv2
from ultralytics import YOLO
model = YOLO("best.pt")

# 비디오 객체 생성
cap = cv2.VideoCapture("./Project\input1.mp4")

# 윈도우 생성
cv2.namedWindow('Video')

while cap.isOpened():
    ret, im0 = cap.read()
    if not ret :
        print("프레임 확인 요청")
        break
    
    results = model(im0, conf=0.4)
    
    # 예시: 예측 결과를 첫 번째 이미지로 표시 (각 모델에 따라 달라질 수 있음)
    annotated_frame = results[0].plot()
    
    
    annotated_frame = cv2.resize(annotated_frame,None, fx=0.5,fy=0.5)
    cv2.imshow('Video', annotated_frame)
    
    # q 눌러서 종료
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
# 비디오 해제
cap.release()
cv2.destroyAllWindows()

# 모델 예측 
# results = model(
    # "./V6_yolo/input4.jpg",
    # conf=0.4, # => confidence score가 0.9 이상인 것만 출력한다. https://docs.ultralytics.com/ko/modes/predict/#inference-arguments => 추론인수
    # max_det => 이미지당 허용되는 최대 감지 횟수. 모델이 한 번의 추론에서 감지할 수 있는 총 오브젝트 수를 제한하여 밀집된 장면에서 과도한 출력을 방지합니다.
    # classes => 클래스 ID 집합으로 예측을 필터링합니다. 지정된 클래스에 속하는 탐지만 반환됩니다. 다중 클래스 탐지 작업에서 관련 개체에 집중하는 데 유용합니다.
    # 각 모델에 맞는 yaml 파일 구글링해서 찾기
    # classes = [0,56] # => 사람하구 의자
# )
