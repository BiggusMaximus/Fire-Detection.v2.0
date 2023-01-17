import pandas as pd
import numpy as np
import glob
import os
import cv2
import matplotlib.pyplot as plt
import pybboxes as pbx

PATH = os.path.join(os.getcwd(), "dataset\onlyfire")
PATH_RESULT = "annotatation_onlyfire.txt"

with open(PATH_RESULT, "w") as result:
    for i in os.listdir(PATH):
        if i.endswith(".txt") and not i == "classes.txt":
            PATH_ALL = PATH + r"/" + i
            PATH_ALL = PATH_ALL.replace("\\", "/")
            with open(PATH_ALL, encoding='utf8') as f:
                img = cv2.imread(PATH_ALL.replace(
                    ".txt", ".jpg"), cv2.IMREAD_UNCHANGED)
                height = img.shape[0]
                width = img.shape[1]
                text = PATH_ALL.replace(".txt", ".jpg") + " "

                for line in f:
                    data = line.strip("\n").split(" ")
                    coordinate = (float(data[1]), float(
                        data[2]), float(data[3]), float(data[4]))
                    coordinate = pbx.convert_bbox(
                        coordinate, from_type="yolo", to_type="voc", image_size=(width, height))
                    text += f"{coordinate[0]},{coordinate[1]},{coordinate[2]},{coordinate[3]},{data[0]} "
                text += "\n"
                result.write(text)
                print(text)
                f.close()
