import cv2
import numpy as np
import pytesseract.pytesseract as pyt
import sys

#pytesseract config
pyt.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'  #req for versions > 3.05

#video mode config
frameWidth = 640
frameHeight = 480

def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions)

print("...Enter Video path for video feed or camera number to take webcam feed...")
strs = input()

try:
    a = int(strs)
    cap = cv2.VideoCapture(a)
except ValueError:
    cap = cv2.VideoCapture(strs)

print("starting OCR....press 'E' to exit process", sep="\n")
cap.set(3, frameWidth)
cap.set(4, frameHeight)

kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])   #kernel value for sharpening

#main code

while True:
    success, img = cap.read()
    if success is False:
        sys.exit()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    img = rescaleFrame(img, 0.5)

    #displaying original video frame
    img1 = img.copy()
    img1 = rescaleFrame(img, 0.4)
    cv2.imshow("Result_initial", img1)

    data_obj = pyt.image_to_data(img, config=tessdata_dir_config)
    #print(data_obj)

    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:  # whole words come as lists with 12 elements
                txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                #print(txt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                cv2.putText(img, txt, (x - 9, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    #displaying ocr detected video frame
    cv2.imshow("frm_final", img)

    #exit sequence
    if cv2.waitKey(1) & 0xFF == ord('e'):   # press 'e' to exit
        break

cap.release()
cv2.destroyAllWindows()
sys.exit()