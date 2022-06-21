import cv2
import numpy as np

# Load Yoloy
net = cv2.dnn.readNet("yolov3_training_final.weights", "yolov3_testing.cfg")

#net = cv2.dnn.readNetFromONNX("drive/MyDrive/objectdetection/best.torchscript.pt")
classes = []  
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


# Loading image

def prediksi(namafile):
  img = cv2.imread(namafile)
  img = cv2.resize(img, None,fx=0.4, fy=0.4)
  height, width, channels = img.shape

  # Detecting objects
  blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
  net.setInput(blob)
  outs = net.forward(output_layers)

  # Showing informations on the screen
  #%matplotlib inline
  #from matplotlib import pyplot as plt
  class_ids = []
  confidences = []
  boxes = []
  for out in outs:
      for detection in out:
          scores = detection[5:]
          class_id = np.argmax(scores)
          confidence = scores[class_id]
          if confidence > 0.5:
              # Object detected
              center_x = int(detection[0] * width)
              center_y = int(detection[1] * height)
              w = int(detection[2] * width)
              h = int(detection[3] * height)

              # Rectangle coordinates
              # extract the upper left corners positions in order to present them with use of opencv
              x = int(center_x - w / 2)
              y = int(center_y - h / 2)

              boxes.append([x, y, w, h])
              confidences.append(float(confidence))
              class_ids.append(class_id)

  indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
  #print(indexes)
  font = cv2.FONT_HERSHEY_PLAIN
  for i in range(len(boxes)):
      if i in indexes:
          x, y, w, h = boxes[i]
          label = str(classes[class_ids[i]])
          color = colors[class_ids[i]]
          cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        #   cv2.putText(img, label, (x, y + 30), font, 1, color, 3)

  cv2.imwrite("static/output.jpg", img)
  print("File telah tersimpan di output.jpg")
