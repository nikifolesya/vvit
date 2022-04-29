import os
import time
import cv2
from flask import Flask, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
from time import sleep
from flask import send_from_directory
from werkzeug.utils import secure_filename
import numpy as np

from threading import Thread
import gi

gi.require_version("Gst", "1.0")


from gi.repository import Gst, GLib

Gst.init()





UPLOAD_FOLDER = 'file_storage/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER






def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("index"))
    return '''
         <!doctype html>
         <title>Upload new File</title>
         <h1>Upload new File</h1>
         <form action="" method=post enctype=multipart/form-data>
           <p><input type=file name=file>
              <input type=submit value=Upload>
         </form>
         '''









#webcam2appsink_YUY2_640_480 = "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"

# mfxh264enc does all the HW encoding
#appsink2file = "appsrc ! videoconvert ! mfxh264enc ! \
       # video/x-h264, profile=baseline ! \
        #matroskamux ! filesink location = mem.mp4"
filepath = "file_storage/mem.mp4"
# Open the capture string
video = cv2.VideoCapture("filesrc location=mem.mp4 ! decodebin2 name=dec ! queue ! ffmpegcolorspace ! autovideosink dec. ! queue ! audioconvert ! audioresample ! autoaudiosink", cv2.CAP_GSTREAMER)

# Hardcoded image properties. Mind here to change them to your needs.
frame_width = 640
frame_height = 480
fps = 30.
show = True
# Create videowriter
#out = cv2.VideoWriter(appsink2file, 0, fps, (frame_width, frame_height), True)



#video = cv2.VideoCapture(0)
    #'filesrc location={} ! decodebin ! videoconvert ! appsink'.format(filepath),
    #cv2.CAP_GSTREAMER




@app.route('/your_video', methods=['GET', 'POST'])
def uploaded_file():
    if not video.isOpened():
        print("Cannot capture video. Exiting.")
        quit()
    while True:
        ret, frame = video.read()
        if ret == False:
            break




@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(uploaded_file(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug = True)