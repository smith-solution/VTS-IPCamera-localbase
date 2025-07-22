from flask import Flask, Response
from picamera2 import Picamera2
import cv2
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()


def generate():
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # ✅ RGB → BGR 변환
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/stream')
def stream():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<img src="/stream">'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
