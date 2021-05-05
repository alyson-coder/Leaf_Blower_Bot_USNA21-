## Ivan A. Chavez
#myTools
#This file provides functions to run in Master file
# DO NOT TOUCH!!!!!!

import cv2
import numpy as np

##1) Parameter Functions:
def nothing(a):
        pass

#Trackbar window: copy values when identified
cv2.namedWindow("Paramters")
cv2.resizeWindow("Paramters",300,400)
                 
#Hue:
cv2.createTrackbar("H min","Paramters",0,180,nothing)
cv2.createTrackbar("H max","Paramters",180,180,nothing)
#Saturation:
cv2.createTrackbar("S min","Paramters",0,255,nothing)
cv2.createTrackbar("S max","Paramters",255,255,nothing)
#Value:
cv2.createTrackbar("V min","Paramters",0,255,nothing)
cv2.createTrackbar("V max","Paramters",255,255,nothing)
#Area Coverage:
cv2.createTrackbar("A min","Paramters",10,30000,nothing)
cv2.createTrackbar("A max","Paramters",307200,307200,nothing)

#Edge Detection:
cv2.createTrackbar("Edge Lo","Paramters",150,255,nothing)
cv2.createTrackbar("Edge Hi","Paramters",255,255,nothing)                        

def Parameters():
   
    #Set Parameters:
    l_h=cv2.getTrackbarPos("H min","Paramters")
    l_s=cv2.getTrackbarPos("S min","Paramters")
    l_v=cv2.getTrackbarPos("V min","Paramters")
    u_h=cv2.getTrackbarPos("H max","Paramters")
    u_s=cv2.getTrackbarPos("S max","Paramters")
    u_v=cv2.getTrackbarPos("V max","Paramters")
    Amin = cv2.getTrackbarPos("A min","Paramters")
    Amax = cv2.getTrackbarPos("A max","Paramters")
    sensitvity1 = cv2.getTrackbarPos("Edge Lo","Paramters")
    sensitvity2 = cv2.getTrackbarPos("Edge Hi","Paramters")
    
    # Color Thresholding
    lower_color = np.array([l_h,l_s,l_v])
    upper_color = np.array([u_h,u_s,u_v])
    

    return lower_color,upper_color, Amin, Amax,sensitvity1,sensitvity2;

##2) Function: StackedImages = stackImages(0.5,([img1,img2,img3,img4]))

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray)
    rowsAvailable = isinstance(imgArray[0],list)
    width =imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0,rows):
            for y in range(0,cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y],(0,0),None,scale,scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y],(imgArray[0][0].shape[1],imgArray[0][0].shape[0]),None,scale,scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor(imgArray[x][y],cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width,3),np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0,rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)

    else:
        for x in range(0,rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x],(0,0),None,scale,scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x],(imgArray[0].shape[1],imgArray[0].shape[0]),None,scale,scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x],cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

#XX) Function: directions = cameraCenter(horizontial centroid coordinate)               
def frameAxis(frame):
    x1, y1 = int(frameWidth/2), 0
    x2, y2 = int(frameWidth/2),frameHieght
    x3,y3 = 310,230
    x4,y4 = 330,250
    line_thickness = 2
    VAxis=cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0),line_thickness)
    Center=cv2.rectangle(VAxis,(x3,y3),(x4, y4),(0,255,0),line_thickness)
    Target=cv2.imshow("Frame",Center)
    return Target;

def HuMom(img):
    M =cv2.moments(img)
    H =cv2.HuMoments(M)
    print("Hu's moment=",H[0],H[1],H[2])
    return H;
