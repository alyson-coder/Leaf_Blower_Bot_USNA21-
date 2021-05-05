# Ivan A. Chavez
#CV_ObjectDetection_master
#This file reads in the videos and displays the detected Object

# import the necessary packages
import cv2
import numpy as np
import Thresholds
import myTools
import Signatures as sig


#This is to play a raw Video, Recording or Photos #
webcam = False           #<<< 1)False for Photos True for Video & Recording
# Still photo

path1 = 'Photo1.jpeg'
path2 = 'Photo2.jpeg'
path3 = 'Photo3.jpeg'

# Different recording clips
vid1 = 'Vid1.mov'
vid2 = 'Vid2.mov'
vid3 = 'Vid3.mov'
vid4 = 'Vid4.mov'
vid5 = 'Vid5.mov'
vid6 = 'Vid6.mov'
vid7 = 'Vid7.mov'
vid8 = 'Vid8.mov'
vid9 = 'Vid9.mov'
vid10 = 'Vid10.mov'
vid11 = 'pingpong1.mov'
vid12 = 'pingpong2.mov'
vid13 = 'pingpong3.mov'
vid14 = 'pingpong4.mov'

frameWidth,frameHieght = 640,480
cap = cv2.VideoCapture(vid1) #<<< 2) cv2.VideoCapture(vid1) is for Recording. cv2.VideoCapture(0) is for raw feed
cap.set(3, frameWidth)
cap.set(4, frameHieght)

while True:
    if webcam:success,img = cap.read()
    else: img = cv2.imread(path1)
    img = cv2.resize(img,(640,480))
    imgContour =img.copy()
    
    s1=sig.colorSig1(img,imgContour,True)
    s2=sig.colorSig2(img,imgContour,True)

    #Video Display                   
    cv2.imshow("Video Feed",imgContour)

    #Multiple Displays
    #stack=myTools.stackImages(0.7,([img,s2,imgContour]))
    #cv2.imshow("1",stack)

    
    # check keyboard for a keypress
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == 27 or key == ord("q"):
            break


# cleanup the camera and close any open windows
cam.release()
cv2.destroyAllWindows()
