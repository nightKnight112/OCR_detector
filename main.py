import cv2
import sys
import numpy as np
import pytesseract.pytesseract as pyt

#print("Specify if OCR detection is to be applied on Video feed or Image")

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

#img = cv2.imread("Capture_1.PNG")

pyt.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'  #req for versions > 3.05


#charecter detection
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#h_img, w_img, _ = img.shape
#print(h_img, w_img)

#only charecter recognition
#data_obj = pyt.image_to_data(img, config=tessdata_dir_config)
#print(data_obj)

#individual charecter recognition
'''
for data in data_obj.splitlines():
    data = data.split(' ')
    txt, x, y, w, h = data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4])
    cv2.rectangle(img, (x, h_img-y), (w, h_img-h), (0, 255, 0), 1)
    #cv2.circle(img, (w-9, h_img-h), 1, (0, 0, 255), 2)
    cv2.putText(img, txt, (w-9, h_img-h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
'''

'''
#full word recognition part
for count, data in enumerate(data_obj.splitlines()):
    if count != 0:
        data = data.split()
        if len(data) == 12:  #whole words come as lists with 12 elements
            txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


cv2.imshow("final", img)

if cv2.waitKey(0) or 0xff == ord('c'):
   sys.exit()
'''
while cap.isOpened():
    ret, frm = cap.read()
    frm = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    h_img, w_img, _ = frm.shape
    data_obj = pyt.image_to_data(frm, config=tessdata_dir_config)

    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:  # whole words come as lists with 12 elements
                txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frm, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("frm_final", frm)

    if cv2.waitKey(0) or 0xff == ord('c'):
        sys.exit()
