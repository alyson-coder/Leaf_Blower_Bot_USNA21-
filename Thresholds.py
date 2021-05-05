# Ivan A. Chavez
#CV_ObjectDetection_master
#This file provides functions that threshold Color,Edge,and shapes
#NOTE: MAY HAVE TO ADJUST.

import cv2
import numpy as np
import myTools
import math

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
PINK =(255,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
         


#01) Function: dilated binary image = colorThresh(vid,lowerthreshold,lowerthreshold):CREATES A BINARY IMAGE
def colorThresh(img,lower_color,upper_color):
    # Convert to HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv,lower_color,upper_color)
    kernel = np.ones((5,5),np.uint8)
    imgErd = cv2.erode(color_mask,kernel)
    imgDil = cv2.dilate(imgErd,kernel,iterations=1)
    return imgDil;


#02) Function: cx,cy = centroid(vid,binaryShapeImage): CALCULATES THE CENTROID OF AN OBJECT
def centroid(frame,c):
    M = cv2.moments(c)
    cx = int(M["m10"]/M["m00"])
    cy = int(M["m01"]/M["m00"])
    return cx,cy;

#03) Function: Creates contour image = getContours(filter1,imgContour,Amin,filter2=2,draw=False,): IDENTIFIES AND CREATES A DISPLAY TO DETECT OBJECTS
def getContours(filter1,imgContour,Amin,filter2=2,draw=False):
        #Extracts all shapes and contours
        contours,hierarchy =cv2.findContours(filter1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        #Beacon
        depth1 = 75 # cm
        objwidth1 = 4.1 #cm
        F1 = 563.39#
        #Ping pong
        depth2 = 25 # cm
        width2 = 3.8 #cm
        F2 = 525#
        
        
        i = 0               #starts the count for items
        for c in contours:
            
                area =cv2.contourArea(c) #creats an area of pixles
                
                if (area>= Amin):
                    
                    prmtr = cv2.arcLength(c,True)                 #this is the perimeter of the shape
                    approx = cv2.approxPolyDP(c,0.001*prmtr,True) #this is the number of corners the shape has
                    x,y,w,h = cv2.boundingRect(approx)            #the green box around the object
                    
                    box,imgwidth=find_Width(c)
             
                    if len(approx)>filter2:
                        i =i+1 # adds the count to new item when detected
                        if draw:
                            HuMom(filter1)                                              #extracts Hu's Moment from Object
                            
                            #d = Distance_finder(F1,objwidth1,imgwidth)                 #discribes the distance of the Ping Pong Ball in cm
    
                            #cv2.drawContours(imgContour,[approx], -1,PINK,7)    #creates a pink contour lines around an object
                            cv2.rectangle(imgContour,(x,y),(x+w, y+h),GREEN,2)      #displays a green boudnig box around an object
                            cv2.drawContours(imgContour,[box], -1,RED,2)            #displays a red box around an object
                            cv2.putText(imgContour, "Vertex: "+str(len(approx)),(x+w+20,y+20), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays number of connors around an object
                            cv2.putText(imgContour, "Area: "+str(int(area)),(x+w+20,y+45), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)    #displays pixel area around an object
                            cv2.putText(imgContour, "Item: "+str(int(i)),(x+w+20,y+65), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)        #displays which item number the object is
                            #cv2.putText(imgContour, "Distance: "+str(float(d)),(x+w+20,y+85), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays from the object to the camera for a ping pong only
                            cx,cy=centroid(filter1,c) #creats centroid
                            
                            #Indicates centroid
                            cv2.circle(imgContour,(cx,cy),7,WHITE,-1) #displays centroid of object 
                            cv2.putText(imgContour, "Centroid",(cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX,0.5,GREEN,1) #displays the word "centroid"
                            alpha=cameraCenter(cx,i)
                            #cv2.putText(imgContour, "From Center: "+str(int(alpha)),(x+w+20,y+85), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)
                           
                            
                else:
                    pass

        #print("items",count)
        return imgwidth;
#04) Function: distance from camera = distMes(Area of object): CALCULATES THE DISTANCE OF A PING PONG BALL FROM THE CAMERA.    
    
#05) Function: dilated edge image = edgeDetect(img,sensitvity1,sensitvity2): CURRENTLY NOT IN USE
def edgeDetec(img,sensitvity1,sensitvity2):
    # Edge Thresholding
    kernel = np.ones((5,5),np.uint8)
    imgBlur = cv2.medianBlur(img,5)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray,sensitvity1,sensitvity2)   
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
    return imgDil;

#06) Function: directions = cameraCenter(horizontial centroid coordinate, item number): TELLS THE DISTANCE FROM THE CENTER.
def cameraCenter(cx,i):
        MidRT = 330
        MidLF = 310
        y=cx-320
        y=int(abs(y))
        if cx > MidRT:
                print("item:",i,"come left")
        
        elif cx < MidLF:
                print("item:",i,"come right")

        elif (MidLF<=cx)&(cx<=MidRT):
                print("item:",i,"hold steady")
        else:
                print("Searching for Beacon")

        #print("discrpency",y) 
        return y;

#07) Function: Hu's Momemt = HuMom(binshape): IDENTIFIES THE NUMBER ASSOCIATED WITH A SHAPE
def HuMom(img):
    M =cv2.moments(img)
    H =cv2.HuMoments(M)
    print("Hu's moment=",H[0],H[1],H[2])
    return H;

#08) Function: dilated binary image = colorThresh(vid,lowerthreshold,lowerthreshold):FOCAL LENGTH FINDER 
def FocalLength(measured_depth, real_width,width_in_rf_image):
    focal_length = (width_in_rf_image*measured_depth)/ real_width
    return focal_length;

#09) Function: dilated binary image = colorThresh(vid,lowerthreshold,lowerthreshold):DISTANCE ESTIMATION
def Distance_finder(focal_length, real_object_width,object_width_in_frame):
    distance = (real_object_width*focal_length)/object_width_in_frame
    return distance;
#10) Function: dilated binary image = colorThresh(vid,lowerthreshold,lowerthreshold):DISTANCE ESTIMATION
def find_Width(c):
    rect = cv2.minAreaRect(c)
    cnt,dim,q=rect
    box1 = cv2.boxPoints(rect)
    box = np.int0(box1)
    if dim[1]>=dim[0]:
        w=dim[0]
    elif dim[0]>dim[1]:
        w=dim[1]
    else:
        w=640
    
    return box,w;
