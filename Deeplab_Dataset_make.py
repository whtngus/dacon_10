import cv2
import numpy as np
import csv
import os

csv_open = open("labels.csv",'r',encoding='utf-8')
csv_reader = csv.reader(csv_open)

image_resize = 244,244
past_image = None

points = []

for idx,line in enumerate(csv_reader):
    line[1:-2] = list(map(int, line[1:-2]))
    image_name = line[0]
    x1,y1,x2,y2,x3,y3,x4,y4 = line[1:-2]

    type_id = line[-2]
    type_name = line[-1]


    xMin = min(x1,x2,x3,x4)
    yMin = min(y1,y2,y3,y4)
    xMax = max(x1,x2,x3,x4)
    yMax = max(y1,y2,y3,y4)
    if xMin<0:
        xMin = 0
    if xMax<0:
        xMax = 0
    if yMin<0:
        yMin = 0
    if yMax < 0:
        yMax = 0

    image = cv2.imread("./original_images/" + image_name, cv2.IMREAD_ANYCOLOR)
    point1 = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4]],np.int32)

    mask = np.zeros(image.shape[:2],dtype="uint8")

    #img = cv2.fillPoly(mask, [point1], (255, 255, 255))

    print(idx)
    if past_image == image_name or idx == 0:
        points.append(point1)
    elif past_image != image_name and idx != 0:

        for i in points:
            mask = cv2.fillPoly(mask, [i], (1, 1, 1))

        if not os.path.exists("./segmentation1"):
            os.mkdir("./segmentation1")
        cv2.imwrite("./segmentation1/"+str(image_name) +".png",mask)
        points.clear()

    past_image = line[0]

    #cv2.imshow("",resize)
    #cv2.waitKey(0)