# example usage:
"""
  cap = video.read()
  fmodel = flight_model(...)
  while cap:
    frame = cap.get_frame()
    
    directions = fmodel.get_flight_directions(frame)
    
    .... send directions to drone
    
"""

import murph_utils as murph
import cv2
from darknet import Darknet
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pprint import pprint
import numpy as np

"""
  fmodel = flight_model(cfg_file: 'path/somewhere', weights_file: "path/somewehere", ...)
  fmodel
"""
class FlightModel:    
    
    def __init__(self):
        self.hello           = 'world'
        self.cfg_file        = '../cfg/yolov3.cfg'
        self.weight_file     = '../weights/yolov3.weights'
        self.namesfile       = '../data/coco.names'
        self.m               = Darknet(self.cfg_file)
        
        self.z_threshold     = .25
        self.distance_factor = 20

    # -- public functions
    def get_flight_directions(self, img, boxes = None):
        if boxes == None:
            rgb_image  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = self.get_boxes(rgb_image)
        
        # -- run box selection process
        # box = _pick_best_box(...)
        box = boxes[0] # TODO
        
        center_of_frame_coordinates = self._get_center_of_frame_coordinates(img)
        adjustments = self._get_adjustments(box, center_of_frame_coordinates)
        directions = self._determine_flight_directions(adjustments)
        return directions
    
    
    def get_boxes(self, img):
        resized_image   = self.resize_image(img)
        class_names     = self._load_class_names()
        tensors         = self._load_tensors(resized_image)
        return murph.get_all_boxes(img, tensors, class_names)

    def resize_image(self, img):    
        return cv2.resize(img, (self.m.width, self.m.height))
    
    def plot_boxes(self, img, boxes):
        height, width, _ = img.shape
        # Create a figure and plot the image
        fig, a = plt.subplots(1,1)
        a.imshow(img)
    
        for i in range(len(boxes)):
            box = boxes[i]

            # Set the postion and size of the bounding box. (x1, y2) is the pixel coordinate of the
            # lower-left corner of the bounding box relative to the size of the image.
            rect = patches.Rectangle((box['x1'], box['y1']),
                                     box['width'], box['height'],
                                     linewidth = 2,
                                     edgecolor = box['rgb'],
                                     facecolor = 'none')            
            # Draw the bounding box on top of the image
            a.add_patch(rect)
            
            circle = patches.Circle(box['centroid'], 10)
            a.add_patch(circle)
            
        center_y = int(height/2)
        center_x = int(width/2)
        z_factor = .01
        z_target = patches.Circle((center_x, center_y), int(height*z_factor), color = 'r', fill = False)
        a.add_patch(z_target)
        plt.axhline(y=center_y, color='r', linestyle='-')
        plt.axvline(x=center_x, color='r', linestyle='-')
        
#         plt.grid(True)
        plt.grid(color='g', linestyle='-', linewidth=1)
        plt.yticks(np.arange(0, height+1, 20.0))


        plt.show()
        
    # -- private functions
    def _load_class_names(self):
        return murph.load_class_names(self.namesfile)
    
    def _load_tensors(self, img):
        self.m.load_weights(self.weight_file)
        nms_thresh = 0.6  
        iou_thresh = 0.4
        return murph.detect_objects(self.m, img, iou_thresh, nms_thresh)   
    
    def _get_center_of_frame_coordinates(self, img):
        imageHeight, imageWidth, _ = img.shape
        return [imageWidth / 2.0, imageHeight / 2.0]
        

    def _get_adjustments(self, box, center_of_frame_coordinates):
        fX, fY = center_of_frame_coordinates
        cX = box["centroid_x"]
        cY = box["centroid_y"]
        cZ = box["height"] / (center_of_frame_coordinates[1] * 2)
    
        x = cX - fX
        y = cY - fY
        z = (cZ - self.z_threshold) * self.distance_factor

        return [x, y, z]


    def _determine_flight_directions(self, adjustments):
        horiz, vert, dist = adjustments
        directions = list()
            
        if horiz > 0:
            directions.append(["move_right", abs(horiz)])
        elif horiz < 0:
            directions.append(["move_left", abs(horiz)])
        else:
            directions.append("")

        if vert < 0:
            directions.append(["move_up", abs(vert)])
        elif vert > 0:
            directions.append(["move_down", abs(vert)])
        else:
            directions.append("")


        if dist < 0:
            directions.append(["move_forward", abs(dist)])
        elif dist > 0:
            directions.append(["move_backward", abs(dist)])
        else:
            directions.append("")

        print("directions:", directions)
        return directions

    def fly_drone():
        cap = cv2.capture()
        while True:
            ret, frame = cap.read()
            width, height = frame.shape()
            center_of_frame_coordinates = [int(width/2), int(height/2)]

            box = get_box("stuff")

            adjustments = get_adjustments(box, center_of_frame_coordinates)
            fly_drone(adjustments)
