import cv2
import sys
import numpy as np
import pytesseract.pytesseract as pyt

#cap = cv2.VideoCapture(0)
img = cv2.imread("Test_1.png")
pyt.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

#charecter detection

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h_img, w_img, _ = img.shape
print(h_img, w_img)

data_obj = pyt.image_to_boxes(img)
print(data_obj)

for data in data_obj.splitlines():
    data = data.split(' ')
    txt, x, y, w, h = data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4])
    cv2.rectangle(img, (x, h_img-y), (w, h_img-h), (0, 255, 0), 1)
    #cv2.circle(img, (w-9, h_img-h), 1, (0, 0, 255), 2)
    cv2.putText(img, txt, (w-9, h_img-h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)


cv2.imshow("final", img)

if cv2.waitKey(0) or 0xff == ord('c'):
    sys.exit()
