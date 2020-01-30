

import cv2
import numpy as np
import csv
import os

csv_open = open("labels.csv",'r',encoding='utf-8')
csv_reader = csv.reader(csv_open)

image_resize = 244,244
past_image = None
image_names = []
points = []

for idx,line in enumerate(csv_reader):
    if line[0] not in image_names:
        image_names.append(line[0])
csv_open.close()


#print(image_names)

for i in image_names:
    print(i)
    csv_open = open("labels.csv", 'r', encoding='utf-8')
    csv_reader = csv.reader(csv_open)
    line_points = []
    for li in csv_reader:
        if li[0] == i:
            #print(li[0],i)
            li[1:-2] = list(map(int, li[1:-2]))
            x1, y1, x2, y2, x3, y3, x4, y4 = li[1:-2]

            type_id = li[-2]
            type_name = li[-1]

            image = cv2.imread("./original_images/" + i, cv2.IMREAD_ANYCOLOR)
            point1 = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], np.int32)
            line_points.append([x1,y1,x2,y2,x3,y3,x4,y4])
            #mask = np.zeros(image.shape[:2], dtype="uint8")
            # img = cv2.fillPoly(mask, [point1], (255, 255, 255))

            points.append(point1)

    #for q in points:
        #image = cv2.fillPoly(image, [q], (1, 1, 1))
    for p in line_points:
        image = cv2.line(image, (p[0], p[1]), (p[2], p[3]), (0, 0, 255), 2)
        image = cv2.line(image, (p[2], p[3]), (p[4], p[5]), (0, 0, 255), 2)
        image = cv2.line(image, (p[4], p[5]), (p[6], p[7]), (0, 0, 255), 2)
        image = cv2.line(image, (p[6], p[7]), (p[0], p[1]), (0, 0, 255), 2)
    if not os.path.exists("./view_label_info"):
        os.mkdir("./view_label_info")

    cv2.imwrite("./view_label_info/" + str(i), image)
    points.clear()
    csv_open.close()
