import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import util

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# define constants
model_cfg_path = "yolo-license-plate-detection-master/model/config/darknet-yolov3.cfg"
model_weights_path = "yolo-license-plate-detection-master/model/weights/model.weights"
class_names_path = "yolo-license-plate-detection-master/model/classes.names"

img_path = "12_6_2014_20_20_53_909.bmp"

# load class names
with open(class_names_path, 'r') as f:
    class_names = [j[:-1] for j in f.readlines() if len(j) > 2]
    f.close()

# load model
net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

# load image

img = cv2.imread(img_path)

H, W, _ = img.shape

# convert image
blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)

# get detections
net.setInput(blob)

detections = util.get_outputs(net)

# bboxes, class_ids, confidences
bboxes = []
class_ids = []
scores = []

for detection in detections:
    # [x1, x2, x3, x4, x5, x6, ..., x85]
    bbox = detection[:4]

    xc, yc, w, h = bbox
    bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]

    bbox_confidence = detection[4]

    class_id = np.argmax(detection[5:])
    score = np.amax(detection[5:])

    bboxes.append(bbox)
    class_ids.append(class_id)
    scores.append(score)

# apply nms
bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

# plot

for bbox_, bbox in enumerate(bboxes):
    xc, yc, w, h = bbox

    """""
    cv2.putText(img,
                class_names[class_ids[bbox_]],
                (int(xc - (w / 2)), int(yc + (h / 2) - 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                7,
                (0, 255, 0),
                15)
    """""
    img = cv2.rectangle(img,
                        (int(xc - (w / 2)), int(yc - (h / 2))),
                        (int(xc + (w / 2)), int(yc + (h / 2))),
                        (0, 255, 0),
                        10)

    license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :]

plt.figure()
#plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

plt.figure()
h = (cv2.cvtColor(license_plate, cv2.COLOR_RGB2GRAY))
#plt.imshow(h, cmap='gray')

#plt.show()

num_plate = pytesseract.image_to_string(
    h,
    config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUWXYZ0123456789')

print('Номер авто: ', num_plate)
