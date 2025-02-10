document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startBtn');  // 시작 버튼
    const stopButton = document.getElementById('stopBtn');    // 중지 버튼
    const videoElement = document.getElementById('videoElement');  // 비디오 태그
    const statusMessage = document.getElementById('statusMessage'); // 상태 메시지

    let mediaStream;  // 스트림을 저장할 변수

    // 비디오 스트리밍 시작
    startButton.addEventListener('click', function() {
        // 사용자의 웹캠 접근 요청
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                // 스트림이 정상적으로 시작되면 비디오 태그에 연결
                videoElement.srcObject = stream;
                mediaStream = stream;
                statusMessage.textContent = '스트리밍 중...';
                statusMessage.style.color = 'green';
                startButton.disabled = true;  // 시작 버튼 비활성화
                stopButton.disabled = false;  // 중지 버튼 활성화
            })
            .catch(function(error) {
                // 에러가 발생하면 에러 메시지 표시
                console.log('Error accessing the camera: ', error);
                statusMessage.textContent = '카메라 접근 실패';
                statusMessage.style.color = 'red';
            });
    });

    // 비디오 스트리밍 중지
    stopButton.addEventListener('click', function() {
        if (mediaStream) {
            // 스트림을 종료하고 비디오 태그에서 제거
            const tracks = mediaStream.getTracks();
            tracks.forEach(function(track) {
                track.stop();
            });
            videoElement.srcObject = null;  // 비디오 스트림 제거
            statusMessage.textContent = '스트리밍이 중지되었습니다.';
            statusMessage.style.color = 'orange';
            startButton.disabled = false;  // 시작 버튼 활성화
            stopButton.disabled = true;    // 중지 버튼 비활성화
        }
    });
});
