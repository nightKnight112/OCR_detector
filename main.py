import cv2
import sys
import numpy as np
import pytesseract.pytesseract as pyt
from PIL import ImageGrab
import pyautogui

#basic setup
pyt.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'  #req for versions > 3.05
frameWidth = 640
frameHeight = 480

#rescale and capture function for screen capture configuration
#extra functions, can be used if needed
def captureScreen():
    capScr = np.array(ImageGrab.grab(bbox=None))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr

def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions)

print("Specify if OCR detection is to be applied on Image or Video feed", "1. Still Image(enter 1)",
      "2. Screen Capture(enter 2)", sep="\n")

i = input()
#print(i)


#for image feed
if int(i) == 1:
    print("Enter full image path: ")
    img = cv2.imread(input())
    print("to stop execution, press 'E'")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #h_img, w_img, _ = img.shape
    #print(h_img, w_img)

    data_obj = pyt.image_to_data(img, config=tessdata_dir_config)   #use pyt.image_to_data() is individual charecter recog is needed

    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:  # whole words come as lists with 12 elements
                txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("final", img)

    #exit sequence
    if cv2.waitKey(0) or 0xff == ord('e'):
        sys.exit()


#for screen capture
elif int(i) == 2:

    print("Starting screen capture, press 'E' to exit",
          "OCR processed screen capture will be saved as 'screen_cap_rcrd_final.avi' in the project dir",
          sep="\n", end="\n")

    # screen capture record settings

    res = (1920, 1080)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    fname = "screen_cap_rcrd_final.avi"
    fps = 30.0
    output_final = cv2.VideoWriter(fname, codec, fps, res)

    cv2.namedWindow("Screen Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Screen Capture", 480, 270)

    cv2.namedWindow("frm_final", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("frm_final", 480, 270)

    while True:

            #uncomment the commented part if fps display is req

            '''
            timer = cv2.getTickCount()
            img = captureScreen()
            img = rescaleFrame(img, 0.5)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            cv2.putText(img, 'FPS {}'.format(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 230, 20), 2)
            '''

            img = pyautogui.screenshot()
            frm = np.array(img)

            frm = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

            #uncomment if initial unprocessed frame display is req
            #cv2.imshow('Screen Capture', frm)

            data_obj = pyt.image_to_data(frm, config=tessdata_dir_config)   #use pyt.image_to_data() is individual charecter recog is needed

            for count, data in enumerate(data_obj.splitlines()):
                if count != 0:
                    data = data.split()
                    if len(data) == 12:  # whole words come as lists with 12 elements
                        txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                        #print(txt)
                        cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frm, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

            output_final.write(frm)
            cv2.imshow("frm_final", frm)

            #exit sequence
            if cv2.waitKey(1) & 0xff == ord('e'):
                output_final.release()
                sys.exit()


#execption case
else:
    print("Unspecified input found, please rerun application again!!!")
    sys.exit()
