self.minY = properties[0].bbox[0] 
self.minX = properties[0].bbox[1] 
self.maxY = properties[0].bbox[2] 
self.maxX = properties[0].bbox[3] 
self.minY2 = None
self.minX2 = None 
self.maxY2 = None
self.maxX2 = None


class Borders_box:
    def __init__(self):
        self.set = False
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
    def get_borders(self):
        if self.set:
            return (self.minX, self.maxX, self.minY, self.maxY)
        return None

def initialize_detect():
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