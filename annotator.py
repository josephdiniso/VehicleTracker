#!/usr/bin/env python3
import argparse
import os

import cv2
import numpy as np

import utils

RED = (0, 0, 255)

class Image:
    """
    Image class used for annotating an image and saving the crop data to a protobuf

    Args:
        path (str): Path to image for annotation
        json (str): Path to crop JSON
    """
    def __init__(self, path: str, json_path: str):
        # TODO: Cleanup class attributes
        self.path = path
        self.img = cv2.imread(path)
        self.json_path = json_path
        self.img = cv2.resize(self.img, (700, 500))
        self.img_copy = self.img.copy()
        # Specifies starting pt of bounding box
        self.start_pt = None
        # Specifies if r-button is held down
        self.held = False
        self.boxes = []
        # Used for undo feature
        self.box_stack = []


    def annotate_image(self):
        """
        Used to facilitate opening an image, showing, and appending annotations to JSON

        NOTE: self.boxes is of the form [(x_i, y_i), (x_f, y_f)), ...]

        """
        cv2.imshow("Img", self.img)
        cv2.setMouseCallback("Img", self.bounding)
        # Var to keep undo stack in order
        deleting = False
        while 1:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('z'):
                if len(self.boxes):
                    self.box_stack.append(self.boxes[-1])
                    del self.boxes[-1]
                    deleting = True
            if key == ord('y'):
                if deleting:
                    deleting = False
                    self.boxes.append(self.box_stack[-1])
                    del self.box_stack[-1]
            if key == ord('q'):
                utils.append_to_json(self.json_path, self.boxes, 0)
                cv2.destroyAllWindows()

    def bounding(self, event, x, y, flags, param):
        """
        Function for mouse callback
        """
        self.img[:] = self.img_copy[:]
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_pt = (x, y)
            self.held = True
        if self.held:
            cv2.rectangle(self.img, self.start_pt, (x, y), RED, 1)
        if event == cv2.EVENT_LBUTTONUP:
            self.boxes.append((self.start_pt, (x, y)))
            self.held = False
        for box in self.boxes:
            cv2.rectangle(self.img, box[0], box[1], RED, 1)
        cv2.imshow("Img", self.img)


def main():
    img = Image("/home/jdiniso/cars.jpg", "/home/jdiniso/test.json")
    img.annotate_image()


if __name__ == "__main__":
    main()