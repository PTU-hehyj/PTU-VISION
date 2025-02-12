from flask import Flask, jsonify
from flask_cors import CORS  # CORS 문제 해결

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 API 요청 허용

# 경로 접속 시 연결되는 Rest API 서버 생성
@app.route('/users', methods=['GET'])
def users():
    # users 데이터를 Json 형식으로 반환
    return jsonify(
    {"members" : [{ "id" : 1, "name" : "cho" },
                         { "id" : 2, "name" : "chuing"}]}
    )

# flask 애플리케이션 실행
if __name__ == "__main__": # 현재 파일로만 서버 실행 가능 => 다른 파일 실행 x
    app.run(debug = True) # 코드 수정 시 자동 서버 재시작 및 디버그 메시지