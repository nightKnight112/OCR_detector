import cv2
import sys
import numpy as np
import pytesseract.pytesseract as pyt
from PIL import ImageGrab

# basic setup
pyt.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'  # req for versions > 3.05
frameWidth = 640
frameHeight = 480


# rescale and capture function for screen capture configuration
def captureScreen(bbox=(50, 50, 1920, 1080)):
    capScr = np.array(ImageGrab.grab(bbox))
    capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    return capScr


def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions)


print("Specify if OCR detection is to be applied on Video feed or Image", "1. Still Image(enter 1)",
      "2. Video Feed(enter 2)", "3. Screen Capture(enter 3)", sep="\n")
i = input()
# print(i)


# for image feed
if int(i) == 1:
    print("Enter full image path: ")
    img = cv2.imread(input())
    print("to stop execution, press Q")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h_img, w_img, _ = img.shape
    # print(h_img, w_img)

    data_obj = pyt.image_to_data(img, config=tessdata_dir_config)

    for count, data in enumerate(data_obj.splitlines()):
        if count != 0:
            data = data.split()
            if len(data) == 12:  # whole words come as lists with 12 elements
                txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("final", img)

    if cv2.waitKey(0) or 0xff == ord('q'):
        sys.exit()


# for video feed
elif int(i) == 2:
    print("Enter full video path: ")
    cap = cv2.VideoCapture(input())
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    print("to stop execution, press Q")

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # kernel value for sharpening

    while True:
        ret, img = cap.read()
        if ret is False:
            print("No frame found, try again")
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.filter2D(src=img, ddepth=-5, kernel=kernel)

        # most probably not req this part
        kernel_new = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_new)

        # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_new)
        cv2.imshow("Result_initial", img)

        data_obj = pyt.image_to_data(img, config=tessdata_dir_config)
        # print(data_obj)

        for count, data in enumerate(data_obj.splitlines()):
            if count != 0:
                data = data.split()
                if len(data) == 12:  # whole words come as lists with 12 elements
                    txt, x, y, w, h = data[11], int(data[6]), int(data[7]), int(data[8]), int(data[9])
                    print(txt)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, txt, (x - 9, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("frm_final", img)

        if cv2.waitKey(0) or 0xff == ord('q'):
            sys.exit()


# for screen capture
elif int(i) == 3:
    print("Starting screen capture, press Q to exit")

    # not completed from here onwards
    # include tesseract and fix screen tiles
    # remove fps counter
    while True:
        timer = cv2.getTickCount()
        img = captureScreen()
        img = rescaleFrame(img, 0.5)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(img, 'FPS {}'.format(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 230, 20), 2)
        cv2.imshow('Screen Capture', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            sys.exit()


# execption case
else:
    print("Unspecified input found, please rerun application again!!!")
    sys.exit()
