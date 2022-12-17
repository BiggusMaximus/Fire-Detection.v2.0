import predict
from flask import Blueprint, render_template, request, flash, Response, redirect, url_for, redirect
import cv2
import os
from werkzeug.utils import secure_filename
from fileinput import filename
import sys
sys.path.append("..")

UPLOAD_FOLDER = './data/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# it has a bunch of root
detection = Blueprint('detection', __name__)


@detection.route('/upload_image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        print("upload")
        f = request.files['upload', False]
        print(f)
        f.save(f.filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detection.route('/webstreaming')
def webstreaming():
    return render_template("webstreaming.html")


@detection.route('/image')
def image():
    return render_template("image.html")


@detection.route('/video')
def video():
    if request.method == 'POST':
        print("video")
        return render_template("webstreaming.html")


def gen_frames():
    global camera
    camera = cv2.VideoCapture(0)
    global video_camera
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = predict.detection(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@detection.route('/status_streaming', methods=['GET', 'POST'])
def status_streaming():
    if request.method == 'POST':
        if request.form.get('status_streaming') == 'Start Streaming':
            print("Start")
            return render_template("start_streaming.html")
        elif request.form.get('status_streaming') == 'Close Streaming':
            print("Close")
            global camera
            camera = cv2.VideoCapture(0)
            if camera.isOpened():
                print("Releasing cam feed")
                camera.release()
            return render_template("webstreaming.html")
        elif request.form.get('status_streaming') == 'Back to Home':
            print("Back to Home")
            return render_template("home.html")


@detection.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
