#!/usr/bin/env python3
from typing import List
import json
import os

def write_json(data: List, json_path: str):
    """
    Writes data to JSON file
    :param data (List): Appended list with new bounding boxes
    :param json_path (str): Path to JSON file
    :return (None):
    """
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)


def append_to_json(json_path: str, boxes: List, id: int):
    """
    Appends bounding box to JSON file

    :param json_path (str): Path to JSON file
    :param boxes (List): List of bounding boxes
        In the form of [(x_i, y_i), (x_f, y_f), ...]
    :param id (int): Image id number
    :return (None)
    """
    if not os.path.exists(json_path):
        create_coco_json(json_path)
    with open(json_path) as f:
        data = json.load(f)
        for box in boxes:
            width = box[1][0] - box[0][0]
            height = box[1][1] - box[0][1]
            area = width * height
            annotation = {"annotation": 0,
                          "image_id": id,
                          "category_id": 0,
                          "segmentation": "RLE",
                          "area": area,
                          "bbox": [box[0][0], box[0][1], width, height],
                          "iscrowd": 0
                          }
            data.append(annotation)
    write_json(data, json_path)


def create_coco_json(json_path: str):
    """
    If JSON does not yet exist, creates one with COCOApi format for categories
    :param json_path (str): Path to JSON file
    :return (None):
    """
    data = [{"categories":
                 [{"id":0,
                   "name":"vehicle",
                   "supercategory":"vehicle"
                   }]}]
    with open(json_path, "a") as f:
        json.dump(data, f, indent=2)


