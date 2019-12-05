#TODO Change File name and class name, then change imports in webstreaming.py
# import the necessary packages
import numpy as np
import imutils
import cv2
from skimage import measure
import math
class instrument_:
    def __init__(self):

        self.playable = True

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
        self.coords = {}
        self.coords["left"] = (0, 100)
        self.coords["right"] = (300, 100)
        #   self.previous_coords_one = -1
        #   self.previous_coords_two = -1
        #   self.current_coords_one = -1
        #   self.current_coords_two = -1
        #   self.tracked_objects_int = 9999

        
        sounds = ["66", "69", "70", "71", "72", "73", "74", "75", "82", "86"] 


        self.instruments_ = {}

        for item in sounds:
            self.instruments_[item] = instrument_()

        # TODO We have to load the instruments and save the rgb values
        # May be array of classes
        # self.instruments = {}
        # TODO make instrument class
    def find_nearest_coord(self, coords):

        def calculateDistance(coord2, distances):  
            for item in ["left", "right"]:
                coord1 = self.coords[item]
                (x1, y1), (x2, y2) = coord1, coord2
                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
                distances.append([dist, item, coord2])
                
        def dista(coord1, coord2):
            (x1, y1), (x2, y2) = coord1, coord2
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return dist
        
        def get_direction(coord1, coord2):
            if dista(coord1, coord2) > 7:
                if coord1[1] < coord2[1]:
                    direction = "Down"
                else:
                    direction = "Up"
                if coord1[0] > coord2[0]:
                    direction += " Left"
                else:
                    direction += " Right"
                print(direction, coord1,"-->", coord2)

        distances = []
        for coord in coords:
            calculateDistance(coord, distances)

        distances.sort(key=lambda x: x[0])  

        while len(distances) > 0:
            closer_key = distances[0][1]
            closer_points = distances[0][2]
            cond1 = closer_key == "left" and self.coords["right"] != closer_points
            cond2 = closer_key == "right" and self.coords["left"] != closer_points
            if  cond1 or cond2:
                if distances[0][0] > 10:
                    print(closer_key)
                    get_direction(self.coords[closer_key], closer_points)
                self.coords[closer_key] = closer_points
            for item in distances:
                if item[2] == closer_points or item[1] == closer_key:
                    distances.remove(item)
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
                q85, q15 = np.percentile(imcrop[:,:,c], [90, 10])
                self.lower.append(q15)
                self.upper.append(q85)
            self.trys = 1
            cv2.destroyAllWindows()

        detected_color_binary = cv2.inRange(color_image, np.array(self.lower), np.array(self.upper))
        combined_binary = detected_color_binary

        """Float Values"""
        #detected_motion_floats = cv2.absdiff(self.bg.astype("uint8"), gray_image) 
     
        """Binary Values"""
        #detected_motion_binary = cv2.threshold(detected_motion_floats, tVal, 255, cv2.THRESH_BINARY)[1]

        #combined_binary = cv2.bitwise_and(detected_color_binary, detected_motion_binary)

        # TODO Figure out the erosion and dilations========================= 
        # Need to do these until there are only two objects left in the image 

        # tracked_objects_int, current_coords_one, current_coords_two = analyze_objects_in_binary(combined_color_and_motion_binary, previous_coords_one, previous_coords_two)
        
        # Create For While Loop based on 
        # available_morphological_transformations = 5 # Max limit of how many 
        # times we will apply morphological transformation before moving on to next step
        #while tracked_objects_int > 2 and available_morphological_transformations > 0:
        #   available_morphological_transformations -= 1
        #   <insert morphological operations>
        #   tracked_objects_int, coords_one, coords_two = def analyze_objects_in_binary(combined_color_and_motion_binary, previous_coords_one, previous_coords_two)
        temp_binary = cv2.erode(combined_binary,kernel = np.ones((2, 2),np.uint8), iterations=3)
        detected_color_binary = cv2.erode(combined_binary,kernel = np.ones((2, 2),np.uint8), iterations=3)
        detected_motion_binary = cv2.erode(combined_binary,kernel = np.ones((2, 2),np.uint8), iterations=3)


        temp_binary = cv2.dilate(temp_binary,kernel = np.ones((2, 2),np.uint8), iterations=5)
        detected_color_binary = cv2.dilate(detected_color_binary,kernel = np.ones((4, 4),np.uint8), iterations=5)
        detected_motion_binary = cv2.dilate(detected_motion_binary,kernel = np.ones((5, 5),np.uint8), iterations=5)




        combined_binary = temp_binary

        # TODO Figure out the erosion and dilations=========================
        # TODO return two bounding boxes based on the two points we find
        
        n = 4
        labels = measure.label(combined_binary, n)
        features = measure.regionprops(labels)
        properties = sorted(features, key=lambda p: p.area, reverse=True)

        if len(properties) == 0:
            return None
        else:
            self.find_nearest_coord([properties[0].centroid])            

            minY = properties[0].bbox[0] 
            minX = properties[0].bbox[1] 
            maxY = properties[0].bbox[2] 
            maxX = properties[0].bbox[3] 
            minY2 = None
            minX2 = None 
            maxY2 = None
            maxX2 = None
            sounds = ["66", "69", "70", "71", "72", "73", "74", "75", "82", "86"] 
            counter = 0
            return_string = ""
            for sound, x in zip(sounds, range(0,401,40)):
                if self.instruments_[sound].playable:
                    if minX < x and minY > 150:
                        return_string = return_string + sound+" "
                        self.instruments_[sound].playable = False
                else:
                    if minX > x or minY < 150:
                        self.instruments_[sound].playable = True

            print("return"+return_string)
                    
            """
            if minY < 20 and minX < 20:
                if instruments["66"] = True:
                    return_string = 0
                return_string = "66"
            elif minY > 30 and minY < 50 and minX > 30 and minX < 50:
                return_string = "69"
            elif minY > 60 and minY < 80 and minX > 60 and minX < 80:
                return_string = "70"
            elif minY > 90 and minY < 110 and minX > 90 and minX < 110:
                return_string = "71"
            """
            #elif minY < 150 and minX < 150:
            #    return_string = "72"
            #elif minY < 180 and minX < 180:
             #   return_string = "73"
            #elif minY < 210 and minX < 210:
              #  return_string = "74"
            #elif minY < 240 and minX < 240:
               # return_string = "75"
            #elif minY < 270 and minX < 270:
             #   return_string = "82"
            #else:
            #    return_string = "86"

        
            #else:
            #self.find_nearest_coord([properties[0].centroid, properties[1].centroid])
            #return_string = "\t".join([str(x) for x in [properties[0].centroid, properties[1].centroid]])
            """return_string = ""
            minY = properties[0].bbox[0] 
            minX = properties[0].bbox[1] 
            maxY = properties[0].bbox[2] 
            maxX = properties[0].bbox[3] 
            minY2 = properties[1].bbox[0] 
            minX2 = properties[1].bbox[1] 
            maxY2 = properties[1].bbox[2] 
            maxX2 = properties[1].bbox[3] """
        


        return return_string, combined_binary, minX, minY, maxX, maxY, minX2, minY2, maxX2, maxY2, detected_color_binary, detected_motion_binary
