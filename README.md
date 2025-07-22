# VTS-IPCamera-localbase



## ver.1

```bash
python3.11 -m venv camenv --system-site-packages
source camenv/bin/activate
sudo apt update
sudo apt install -y libcamera-dev libcamera-apps
sudo apt install -y python3-picamera2
pip install picamera2
pip install numpy==1.26.4
pip install opencv-python
pip install flask
pip install flask_cors
python stream_app.py
```





## ver.2

```bash
python3.11 -m venv camenv --system-site-packages
source camenv/bin/activate
sudo apt update
sudo apt install -y libcamera-dev libcamera-apps
sudo apt install -y python3-picamera2
pip install numpy==1.24.4
pip install simplejpeg --no-binary :all:
pip install picamera2
pip install opencv-python
pip install flask
pip install flask_cors
python stream_app.py
```











