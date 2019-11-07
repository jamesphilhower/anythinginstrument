#TODO Change File name and class name, then change imports in webstreaming.py
# import the necessary packages
import numpy as np
import imutils
import cv2

class SingleMotionDetector:
	def __init__(self, accumWeight=0.5):
		# store the accumulated weight factor
		self.accumWeight = accumWeight

		# initialize the background model
		# TODO Change this initialization to be what we
		# use to select the pieces see update()
		self.bg = None
		# tracked_objects_int, number of items in the picture
		# current_coords_one, [x, y] - based on closest previous of previous_coords
		# current_coords_two, [x, y] - based on closest previous of previous_coords
		# 	self.previous_coords_one = -1
		#	self.previous_coords_two = -1
		# 	self.current_coords_one = -1
		#	self.current_coords_two = -1
		# 	self.tracked_objects_int = 9999

		# TODO We have to load the instruments and save the rgb values
		# May be array of classes
		# self.instruments = {}
		# TODO make instrument class


	# This Function is used to update the frame from the webcame that
	# we are analyzing
	def update(self, image):
		# if the background model is None, initialize it
		if self.bg is None:
			# TODO Chahnge this initialization to be what we
			# use to select the pieces
			self.bg = image.copy().astype("float")
			return

		# update the background model by accumulating the weighted
		# average
		#arg1, current image, arg2 image that is being updated, arg3, rate of update, or how much we weight image
		cv2.accumulateWeighted(image, self.bg, self.accumWeight)

	#tVal is a value to determine what motion is, things greater than tval -> 255, else 0
	def detect(self, image, tVal=25):
		# TODO OVERALL GOAL IN CHANGING FUNCTION 
		# change detect to detect things only of a certain color that are moving 
		
		# compute the absolute difference between the background model
		# and the image passed in, then threshold the detected_motion_floats image
		"""Float Values"""
		detected_motion_floats = cv2.absdiff(self.bg.astype("uint8"), image) 


		# TODO create a function that checks an image for certain colors
		# detected_drum_sticks_image = def extractColors() by using rgb value
		
		# Debugging
		#cv2.imshow("self.bg", self.bg)
		#cv2.imshow("detected_motion_floats", detected_motion_floats)


		"""Binary Values"""
		detected_motion_binary = cv2.threshold(detected_motion_floats, tVal, 255, cv2.THRESH_BINARY)[1]

		# TODO calculate the threshold for detected_drum_sticks
		# Correct the following function
		# detected_color_binary = cv2.threshold(detected_motion_floats, tVal, 255, cv2.THRESH_BINARY)[1]

		# TODO AND && detected_motion_floats and detected_color_binary
		# combined_color_and_motion_binary = cv2.bitwise_and(detected_color_binary, detected_motion_binary)

		# Debugging
		#cv2.imshow(combined_color_and_motion_binary)
		# cv2.imshow("detected_motion_binary", detected_motion_binary)


		# perform a series of erosions and dilations to remove small
		# blobs

		# TODO Figure out the erosion and dilations========================= 
		# Need to do these until there are only two objects left in the image 

		# tracked_objects_int, current_coords_one, current_coords_two = analyze_objects_in_binary(combined_color_and_motion_binary, previous_coords_one, previous_coords_two)
		
		# Create For While Loop based on 
		# available_morphological_transformations = 5 # Max limit of how many 
		# times we will apply morphological transformation before moving on to next step
		#while tracked_objects_int > 2 and available_morphological_transformations > 0:
		# 	available_morphological_transformations -= 1
		# 	<insert morphological operations>
		#	tracked_objects_int, coords_one, coords_two = def analyze_objects_in_binary(combined_color_and_motion_binary, previous_coords_one, previous_coords_two)

		detected_motion_binary = cv2.erode(detected_motion_binary, None, iterations=2)
		detected_motion_binary = cv2.dilate(detected_motion_binary, None, iterations=2)

		# Debugging
		#cv2.imshow("changed_detected_motion_binary", detected_motion_binary)
		#cv2.waitKey(0)

		# TODO Figure out the erosion and dilations=========================



		# TODO Change into getting the bounding boxes, or centroids, or whatever, from 
		# detected_motion_binary , may already be done from count_objects_in_binary, 
		# 
		# find contours in the thresholded image and initialize the
		# minimum and maximum bounding box regions for motion
		cnts = cv2.findContours(detected_motion_binary.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		(minX, minY) = (np.inf, np.inf)
		(maxX, maxY) = (-np.inf, -np.inf)

		# if no contours were found, return None
		if len(cnts) == 0:
			return None

		# otherwise, loop over the contours
		for c in cnts:
			# compute the bounding box of the contour and use it to
			# update the minimum and maximum bounding box regions
			(x, y, w, h) = cv2.boundingRect(c)
			(minX, minY) = (min(minX, x), min(minY, y))
			(maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))

		# otherwise, return a tuple of the thresholded image along
		# with bounding box
		# TODO return two bounding boxes based on the two points we find
		return (detected_motion_binary, (minX, minY, maxX, maxY))