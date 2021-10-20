# OCR_Detector_CV
A OCR detector which identifies text in images, video feeds(both in videos and webcam feeds) and also by capturing the entire screen


## NOTES

1. Video OCR done in seperate file Video_OCR_part.py, and it also accepts webcam feeds
2. Both video and image part is dynamic, we only have to provide the correct path location for our image/video
3. Screen capture captures the entire screen by default, can also be used to capture a specific ROI and use OCR there
4. Screen capture part records the screen capture and saves it as screen_cap_rcrd_final.avi in the project dir, which can be used for reevaluation later on
5. 1.mp4 is the video by which video_OCR_part.py was tested and Test_1.PNG was used to test the still image OCR part in main.py
