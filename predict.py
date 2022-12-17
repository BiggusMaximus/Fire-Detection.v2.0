from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import ConfigProto
import numpy as np
import cv2
from PIL import Image
from tensorflow.python.saved_model import tag_constants
from core.yolov4 import filter_boxes
import core.utils as utils
from absl.flags import FLAGS
from absl import app, flags, logging
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(
    tiny=False, model='yolov4')
input_size = 416
video_path = 416

path = './model/fire-v.1.0.tflite'
interpreter = tf.lite.Interpreter(model_path=path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


vid = cv2.VideoCapture(0)


def detection(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    frame_size = frame.shape[:2]
    image_data = cv2.resize(frame, (input_size, input_size))
    image_data = image_data / 255.
    image_data = image_data[np.newaxis, ...].astype(np.float32)
    start_time = time.time()

    interpreter.set_tensor(input_details[0]['index'], image_data)
    interpreter.invoke()
    pred = [interpreter.get_tensor(output_details[i]['index'])
            for i in range(len(output_details))]
    boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                    input_shape=tf.constant([input_size, input_size]))

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=0.6,
        score_threshold=0.5
    )
    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(),
                 valid_detections.numpy()]
    image = utils.draw_bbox(frame, pred_bbox)
    fps = 1.0 / (time.time() - start_time)
    print("FPS: %.2f" % fps)
    result = np.asarray(image)
    result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return result
