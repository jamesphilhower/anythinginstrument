# USAGE
# python webstreaming.py --ip 127.0.0.1 --port 8000


# Initialization ==================================================
# TODO change the import statement below
from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

from flask import Flask, jsonify, render_template, request
import time

string_test = ""

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

location = None

# James Initizalize the output sound and a lock used to ensure thread-safe
outputSound = None
sound_lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

# ^ Initialization ================================================

# Routes ==========================================================

# Typical Order for new User Between Routes
"""Optional"""
# TODO
# "/" - index.html - Overview of what our app does
# Image of instruments
# Name of App
# Link to Login Page
# Instructions for how to use app
""" ^ Optional"""

"""Required"""
# TODO
# "/login" - login.html - Login
# "/instruments" - instruments.html - Look at instruments and settings you've used before
# Table of instruments played before 
# Dropdown Option that starts with "New Instrument" and has all instruments played before 
# and has a button that links to to go to setup.html to create a new mapping for a new instrument
""" ^ Required"""

"""Optional"""
# "/setup" - setup.html - Take still image and assign drums to objects in frame, form data
	# TODO add
	# Category of Instrument: Percussion, Wind, Brass  -- Dropdown
	# Based on Above: Choose correct Instrument -- Dropdown
	# Select How you want to associate keys
		# Previous 
	# Associate Instrument Keys with Places in the Real World -- 
	# 	Background -- image of selected instrument
	# 	Foreground -- clickable buttons that will change color and
	#   have the note associated with that part of the instrument and the background
	#   color of the button will be based on the selection from the real image data 
	#   that are located above the respective notes. 
	# Associate Instrument Keys Automatic

	# Each a button based on an image of an insrument, on button press, show image, 
	# 
""" ^ Optional"""

"""Required"""
# "/play" - play.html - decode which instrument you are using from form in setup
# Create Javascript to play sound
""" ^ Required"""

"""Optional"""
# "/download" - download.html - download selected items
""" ^ Optional"""



# Explanation of site concept page ================================
# TODO:
# Determine content required and implement
@app.route("/")
def index():
	# return the rendered template
	#return render_template("index.html")
    return render_template('main.html', reload = time.time())

# ^ Explanation of site concept page ===============================


# Backend Motion Detection =========================================
@app.route("/vid")
def video_test_zone():
	# TODO Create a javascript function in test.html that plays a simple sound when told to from the backend 
	# return the rendered template
	return render_template("test.html")
# ^ Backend Motion Detection ========================================

# TODO
"""
# Login page
@app.route("/login")

# Configure your play settings
@app.route("/setup")

# Play insrument
@app.route("/play")

# Download songs
@app.route("/download")
"""

# ^ Routes ==========================================================

# Main function, goes from the input to the output, but doesn't package the output, that is done via generate
# Frame count is from args, it is used to establish background image with enough pictures
def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, location, lock

	# initialize the motion detector and the total number of frames
	# read thus far
	# TODO figure out how accumWeight changes things
	md = SingleMotionDetector(accumWeight=0.1)
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		color = np.copy(frame)
		color = cv2.GaussianBlur(color, (7, 7), 0)
		motion = None
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# TODO expreiment not blurring vs blurring and how much
		gray = cv2.GaussianBlur(gray, (7, 7), 0)

		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		if total > frameCount:
			# detect motion in the image, passing grayscale image to class
			motion = md.detect(gray, color)
			# check to see if motion was found in the frame
			if motion is None:
				continue

		# update the background model and increment the total number
		# of frames read thus far
		md.update(gray)
		total += 1

		# acquire the lock, set the output frame, and release the
		# lock
		# TODO may want to copy something other than frame, like _detected_motion_binary_
		with lock:
			location = motion
		
def generate():
	# grab global references to the output frame and lock variables
	global location, lock
	with lock:
		if location is None:
			return None
		return location


import random
import string		
def audio_connection():
	# grab global references to the output frame and lock variables	
	global string_test
	
	#string_test = randomString()
	string_test = str(random.randint(69,75))
	return string_test

@app.route("/classtest")
def test_feed_class():
	return render_template("index_orig.html")

@app.route("/test")
def test_feed():
	return render_template("test.html")


@app.route("/james")
def test_feeder():
	return render_template("temp_class.html")


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	# Generate grabs the global variable outputFrame and encodes it so it can be sent to the user
	#return Response(generate(),
	#	mimetype = "multipart/x-mixed-replace; boundary=frame")
	global location
	print(location)
	return  Response(generate(), mimetype='text/xml')

@app.route("/text_feed")
def text_feed():
	# return the response generated along with the specific media
	# type (mime type)
	# Generate grabs the global variable outputFrame and encodes it so it can be sent to the user
	return  Response(audio_connection(), mimetype='text/xml')



@app.route("/info")
def api_info():
    info = {
       "ip" : "127.0.0.1",
       "hostname" : "everest",
       "description" : "Main server",
       "load" : [ 3.21, 7, 14 ]
    }
    return jsonify(info)


# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()