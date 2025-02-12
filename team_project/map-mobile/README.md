README.md
# YOLO 기반 객체 탐지 및 실시간 비디오 스트리밍 웹 애플리케이션
이 애플리케이션은 YOLO (You Only Look Once) 모델을 사용하여 실시간 객체 탐지를 수행하고, 노트북의 웹캠을 통해 인식된 화면을 모바일 웹에서 실시간으로 스트리밍하는 시스템입니다. 사용자는 자신의 핸드폰에서 웹캠을 통해 탐지된 객체들의 실시간 정보를 확인할 수 있습니다.


## 주요 기능
실시간 객체 탐지: 웹캠을 통해 실시간 영상 데이터를 캡처하고, YOLO 모델을 사용하여 각 프레임에서 객체를 탐지합니다.
비디오 스트리밍: 노트북에서 실시간으로 전송되는 비디오 스트림을 Flask 서버를 통해 모바일 웹 브라우저에서 스트리밍합니다.
모바일 호환: 핸드폰에서 해당 웹 페이지에 접속하여, 웹캠에서 인식한 객체들을 실시간으로 확인할 수 있습니다.
실시간 객체 수 표시: 탐지된 객체의 수를 실시간으로 업데이트하여 사용자가 얼마나 많은 객체가 탐지되었는지 확인할 수 있습니다.

## 동작 방식
### 1. 노트북 웹캠으로 객체 탐지:

노트북의 웹캠을 통해 실시간 영상을 캡처합니다.
캡처된 영상은 YOLO 모델에 의해 처리되어, 각 프레임에서 객체들을 탐지합니다.
탐지된 객체의 수와 상태는 Flask 서버를 통해 실시간으로 웹 페이지에 전달되며, 객체 탐지 결과가 업데이트됩니다.

### 2. 핸드폰에서 실시간 스트리밍:

Flask와 SocketIO를 사용하여, 노트북에서 인식된 실시간 비디오 스트리밍을 웹 서버를 통해 모바일 웹 브라우저로 전송합니다.
사용자는 모바일 브라우저에서 해당 웹 페이지에 접속하여, 웹캠에서 실시간으로 객체 탐지와 비디오 스트리밍을 확인할 수 있습니다.

### 3. 실시간 상태 및 색상 변경:

웹캠에서 객체가 탐지되면 실시간으로 객체 수에 따라 상태가 업데이트됩니다.
객체 수가 적으면 "Normal" 상태로 검정색으로 표시됩니다.
탐지된 객체가 1개를 초과하면 "Warning" 상태로 파란색으로 표시됩니다.
객체가 많을 경우 "Danger" 상태로 빨간색으로 표시됩니다.
이 상태 정보는 SocketIO를 통해 실시간으로 업데이트되며, Flask와 통신하여 웹 페이지에서 이를 확인할 수 있습니다.

### 4. ngrok을 통한 HTTPS 보안 설정:
외부에서 안전하게 접속할 수 있도록 ngrok을 사용하여 로컬 서버를 HTTPS로 포워딩하여 보안을 유지합니다.
이를 통해 사용자는 외부에서도 안전하게 모바일 웹을 통해 실시간 객체 탐지와 비디오 스트리밍을 확인할 수 있습니다.

```
/yolo-app
│
├── project_flask.py                     # Flask 서버 코드
├── /templates                 # HTML 템플릿 폴더
│   └── page1.html             # 기본 웹 페이지 템플릿
├── /static                    # 정적 파일 폴더 (CSS, JS, 이미지)
│   ├── /css
│   │   └── style.css          # CSS 파일 (선택 사항)
│   ├── /js
│   │   └── script.js          # JavaScript 파일 (클라이언트 로직)
└── yolo_model.h5              # YOLO 모델 파일 (예시)
```

## 기술 스택
YOLO: 객체 탐지를 위한 딥러닝 모델 (YOLOv8 사용)
Flask: Python 웹 프레임워크, 실시간 비디오 스트리밍 및 객체 탐지 결과 제공
SocketIO: 실시간 데이터 통신을 위한 라이브러리
ngrok: 로컬 개발 서버를 HTTPS로 안전하게 포워딩하여 외부에서 접근 가능하도록 설정
Flask와 SocketIO로 구현한 웹 애플리케이션
Flask는 웹 애플리케이션을 구축하는 데 사용되며, 이를 통해 웹 서버를 설정하고 실시간 비디오 스트리밍을 제공합니다.
SocketIO는 웹소켓을 사용하여 실시간 통신을 가능하게 합니다. 이로 인해 서버와 클라이언트 간의 실시간 객체 탐지 결과와 영상 데이터를 동적으로 업데이트할 수 있습니다.

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
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>project huhyj</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}"> <!-- css 부분 -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap" /> <!-- 돋보기 아이콘 -->
</head>
<body>
    <img src="{{ url_for('static', filename='marker.png') }}" alt="Logo" class="logo">
    <div class="title-container">
        <div class="title" id="title">PET FINDER</div>
    </div>
    <div class="speak">펫파인더 로고에 마우스를 올리면 실시간 화면을 볼 수 있어요!</div>
    <div class="map-container">
        <img src="{{ url_for('static', filename='map.JPG') }}" alt="안성스타필드_1층지도" class="map_img">

        <!-- 비디오 객체 1 -->
        {# 마커 색상 변경을 위한 data 속성 설정 #}
        <div class="marker" id="marker1" 
             data-black="{{ url_for('static', filename='marker_black.png') }}"
             data-blue="{{ url_for('static', filename='marker_blue.png') }}"
             data-red="{{ url_for('static', filename='marker_red.png') }}">
            <img src="{{ url_for('static', filename='marker.png') }}" alt="마커 1">
            <div class="video-box" id="video1">
                <!-- MJPEG 스트리밍을 위한 이미지 표시 -->
                <img class="hover-video" src="{{ url_for('video_feed_1') }}" alt="Marker 1 Video" width="100%">
            </div>
        </div>
    </div>

    <script>
        /**
         * 마커의 상태를 업데이트하는 함수
         * - Flask API '/get_status'에서 데이터를 가져와서 마커 색상 변경
         */
        function updateMarkers() {
            fetch('/get_status')
                .then(response => response.json())
                .then(data => {
                    const marker1 = document.getElementById("marker1").querySelector("img");

                    // 마커1 상태 적용
                    let color1 = "black";
                    if (data.marker1.status.includes("Warning")) {
                        color1 = "blue";
                    } else if (data.marker1.status.includes("Danger")) {
                        color1 = "red";
                    }

                    // 마커 1 색상 적용 (data- 속성 활용)
                    marker1.src = document.getElementById("marker1").dataset[color1];
                })
                .catch(error => console.error("Error fetching status:", error));
        }

        // 1초마다 상태 업데이트
        setInterval(updateMarkers, 1000);
    </script>
</body>
</html>
```











