from flask import Flask, Response
from flask_cors import CORS
from picamera2 import Picamera2
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

# 1. Camera parameters (originally calibrated at 2592x1944)
scale_x = 640 / 2592
scale_y = 480 / 1944

K = np.array([
    [908.248874*scale_x, 0.0,1194.71816*scale_x],
    [0.0,899.015826*scale_y , 1032.28973*scale_y],
    [0.0,0.0,1.0]
], dtype=np.float32)

D = np.array([[-0.22773718, 0.03887236, 0.0085078, 0.00710741, -0.00269294]], dtype=np.float32)

# 2. Initialize PiCamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# 3. Prepare undistortion maps
frame = picam2.capture_array()
h, w = frame.shape[:2]
alpha = 0.0
new_K, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), alpha, newImgSize=(w, h))
#new_K[0, 2] = K[0, 2]  # restore cx
##new_K[1, 2] = K[1, 2]  # restore cy
new_K = np.array([
    [908.248874*scale_x, 0.0,1194.71816*scale_x],
    [0.0,899.015826*scale_y, 1206.28973*scale_y],
    [0.0,0.0,1.0]
], dtype=np.float32)
map1, map2 = cv2.initUndistortRectifyMap(K, D, None, new_K, (w, h), cv2.CV_16SC2)

# 4. MJPEG stream generator
def generate():
    while True:
        frame = picam2.capture_array()
        if frame is None:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        undistorted = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)
        _, buffer = cv2.imencode('.jpg', undistorted)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# 5. Routes
@app.route('/stream')
def stream():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<img src="/stream">'

# 6. Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
