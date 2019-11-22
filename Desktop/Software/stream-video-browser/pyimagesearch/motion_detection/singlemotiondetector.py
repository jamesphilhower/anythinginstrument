#TODO Change File name and class name, then change imports in webstreaming.py
# import the necessary packages
import numpy as np
import imutils
import cv2
from skimage import measure


class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight
        self.trys = 0
        self.lower = []
        self.upper = []
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
    def detect(self, gray_image, color_image,  tVal=25):
        # TODO OVERALL GOAL IN CHANGING FUNCTION 
        # change detect to detect things only of a certain color that are moving 
        
        # compute the absolute difference between the background model
        # and the gray_image passed in, then threshold the detected_motion_floats gray_image
        colors = ["b","g","r"]

        if self.trys == 0:
            still = color_image
            r = cv2.selectROI(still)
            imcrop = still[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            for c, color in enumerate(colors):
                q85, q15 = np.percentile(imcrop[:,:,c], [99, 1])
                self.lower.append(q15 - 10)
                self.upper.append(q85 + 10)
            self.trys = 1
            cv2.destroyAllWindows()

        """for c, color in enumerate(colors):           
            color_select = np.copy(color_image)
            for e, row in enumerate(color_select[:,:,c]):
                for f, pixel in enumerate(row):
                    if pixel != 0 and (pixel > self.q[c][0] or pixel < self.q[c][1]):
                        color_select[e][f][0] = 0
                        color_select[e][f][1] = 0
                        color_select[e][f][2] = 0

        """
        detected_color_binary = cv2.inRange(color_image, np.array(self.lower), np.array(self.upper))
        

        #detected_color_floats = cv2.cvtColor(color_select, cv2.COLOR_BGR2GRAY)

        """Float Values"""
        #detected_motion_floats = cv2.absdiff(self.bg.astype("uint8"), gray_image) 
        
        # Debugging
        #cv2.imshow("self.bg", self.bg)
        #cv2.imshow("detected_motion_floats", detected_motion_floats)


        """Binary Values"""
        #detected_motion_binary = cv2.threshold(detected_motion_floats, tVal, 255, cv2.THRESH_BINARY)[1]
        #detected_color_binary = cv2.threshold(detected_color_floats, 1, 255, cv2.THRESH_BINARY)[1]

        #combined_binary = cv2.bitwise_and(detected_color_binary, detected_motion_binary)

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
        combined_binary = detected_color_binary
        combined_binary = cv2.erode(combined_binary, None, iterations=2)
        combined_binary = cv2.dilate(combined_binary, None, iterations=2)

        # TODO Figure out the erosion and dilations=========================
        # TODO return two bounding boxes based on the two points we find
        
        n = 4
        labels = measure.label(combined_binary, n)
        features = measure.regionprops(labels)
        properties = sorted(features, key=lambda p: p.area, reverse=True)

        if len(properties) == 0:
            return None
        elif len(properties) == 1:
            return_string = "\t".join([str(x) for x in [properties[0].centroid]])
        else:
            return_string = "\t".join([str(x) for x in [properties[0].centroid, properties[1].centroid]])

        minY = properties[0].bbox[0] 
        minX = properties[0].bbox[1] 
        maxY = properties[0].bbox[2] 
        maxX = properties[0].bbox[3] 

        print("Coords",minX, maxX, minY, maxY)
        return return_string, combined_binary, minX, minY, maxX, maxY#, detected_color_binary, detected_motion_binary
