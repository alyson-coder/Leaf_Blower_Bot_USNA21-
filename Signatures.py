## Color,Edge,Shape Threshold functions
#NOTE: un these functions in this order

import cv2
import numpy as np
import myTools
import math
import imutils

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
PINK =(255,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

pi=math.pi

def HuMom(img):
    M =cv2.moments(img)
    H =cv2.HuMoments(M)
    #print("Hu's moment=",H[0],H[1],H[2])
    return H;

#XX) Function: cx,cy = centroid(vid,binaryShapeImage)
def centroid(frame,c):
    M = cv2.moments(c)
    cx = int(M["m10"]/M["m00"])
    cy = int(M["m01"]/M["m00"])
    return cx,cy;

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

def deviantCal(cx,i):
        MidRT = 330
        MidLF = 310
        deviation=cx-320
        deviation=int(deviation)
        if cx > MidRT:
                print("item:",i,"pivot cw")
        
        elif cx < MidLF:
                print("item:",i,"pivot ccw")

        elif (MidLF<=cx)&(cx<=MidRT):
                print("item:",i,"hold steady")
        else:
                print("Searching for Beacon")

        #print("deviation:",deviation) 
        return deviation;
    
def Distance_finder(focal_length, real_object_width,object_width_in_frame):
    distance = (real_object_width*focal_length)/object_width_in_frame
    return distance;

def colorSig1(img,imgContour,draw=False):
    # Set Parameters:
    l_h=54
    u_h=102
    l_s=122
    u_s=255
    l_v=96
    u_v=255
    Amin = 1000
    i = 0 
    mesdepth1 = 75 # cm
    meswidth1 = 4.1 #cm
    F1 = 563.39#
    vertex=15

    # Color Thresholding:
    lower_color = np.array([l_h,l_s,l_v])
    upper_color = np.array([u_h,u_s,u_v])

    # Convert to HSV:
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv,lower_color,upper_color)
    kernel = np.ones((5,5),np.uint8)
    imgErd = cv2.erode(color_mask,kernel)
    imgDil = cv2.dilate(imgErd,kernel,iterations=1)
    
    #Video Display                   
    #cv2.imshow("Video Feed",imgDil)
  

    #Extracts all shapes and contours
    contours,hierarchy =cv2.findContours(imgDil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)   
    
    
    for c in contours:
        
            area =cv2.contourArea(c) #creats an area of pixles
            
            if (area>= Amin):
                
                prmtr = cv2.arcLength(c,True)                 #this is the perimeter of the shape
                approx = cv2.approxPolyDP(c,0.01*prmtr,True) #this is the number of corners the shape has
                x,y,w,h = cv2.boundingRect(approx)            #the green box around the object
                
                box,imgwidth=find_Width(c)
         
                if len(approx)<vertex:
                    i =i+1 # adds the count to new item when detected
                    HuMom(imgDil)                                              #extracts Hu's Moment from Object
                    d = Distance_finder(F1,meswidth1,imgwidth)                  #discribes the distance of the Ping Pong Ball in cm
                    cx,cy=centroid(imgDil,c)                                    #creats centroid
                    deviation=deviantCal(cx,i)
                    if draw:
                        
                        #cv2.drawContours(imgContour,[approx], -1,PINK,7)    #creates a pink contour lines around an object
                        cv2.rectangle(imgContour,(x,y),(x+w, y+h),GREEN,2)      #displays a green boudnig box around an object
                        cv2.drawContours(imgContour,[box], -1,RED,2)            #displays a red box around an object

                        cv2.putText(imgContour, "Item: Beacon "+str(int(i)),(x+w+20,y+20), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)        #displays which item number the object is
                        cv2.putText(imgContour, "Depth(cm): "+str(float(d)),(x+w+20,y+40), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays from the object to the camera for a ping pong only
                        cv2.putText(imgContour, "Deviation(pixels): "+str(int(deviation)),(x+w+20,y+60), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)
                        #cv2.putText(imgContour, "Vertex: "+str(len(approx)),(x+w+20,y+80), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays number of connors around an object
                        #cv2.putText(imgContour, "Area: "+str(int(area)),(x+w+20,y+100), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)    #displays pixel area around an object
                        cv2.circle(imgContour,(cx,cy),7,WHITE,-1) #displays centroid of object 
                        cv2.putText(imgContour, "Centroid",(cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX,0.5,GREEN,1) #displays the word "centroid"
                        a=np.array([i,d,deviation])
                        print(a)
                        return a;
                                           
            else:
                a=np.array([i,0,0])
                print("Searching for Beacon")
                return a;


def colorSig2(img,imgContour,draw=False):
    # Set Parameters:
    l_h=0
    u_h=37
    l_s=112
    u_s=255
    l_v=144
    u_v=255
    Amin = 10
    vert=8
    Circ=0.30
    Conv=0.20
    i = 0 
    mesdepth2 = 40 # cm
    meswidth2 = 3.7 #cm
    F2 = 525.0#
    


    # Color Thresholding:
    lower_color = np.array([l_h,l_s,l_v])
    upper_color = np.array([u_h,u_s,u_v])

    # Convert to HSV:
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv,lower_color,upper_color)
    kernel = np.ones((3,3),np.uint8)
    imgErd = cv2.erode(color_mask,kernel)
    imgDil = cv2.dilate(imgErd,kernel,iterations=1)

    #Video Display                   
    #cv2.imshow("Video Feed",imgDil)
  

    #Extracts all shapes and contours
    contours,hierarchy =cv2.findContours(imgDil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(contours)
    
    
    for c in contours:
        
            area =cv2.contourArea(c) #creats an area of pixles

              
            if (area>= Amin):
                
                k = max(c, key=cv2.contourArea)
                ((kx, ky), radius) = cv2.minEnclosingCircle(c)

               
                prmtr = cv2.arcLength(c,True)                 #this is the perimeter of the shape
                approx = cv2.approxPolyDP(c,0.001*prmtr,True) #this is the number of corners the shape has
                x,y,w,h = cv2.boundingRect(approx)            #the green box around the object
                H = HuMom(imgDil)                                              #extracts Hu's Moment from Object
                cir = (4*pi*area)/(prmtr**2)
                cirA =pi*(radius**2)

                conv=area/cirA
                
                if Circ<= cir <=1:
                    #if Conv<=conv<=1:
                        if len(approx)>vert: ##or ((0.00062942<H[0]<0.00072982) or (3.9727206e-8<H[1]<9.46251117e-8) or (8.718473224e-13<H[2]<1.5991493e-10)):
                            if radius >6:
                                i =i+1 # adds the count to new item when detected
                                d = Distance_finder(F2,meswidth2,w)                  #discribes the distance of the Ping Pong Ball in cm
                                cx,cy=centroid(imgDil,c)                                    #creats centroid
                                deviation=deviantCal(cx,i)
                                if draw:
                                    cv2.circle(imgContour, (int(kx), int(ky)), int(radius),RED, 2)
                                    #cv2.circle(frame, center, 5, (0, 0, 255), -1)
                                    #cv2.drawContours(imgContour,[approx], -1,PINK,7)    #creates a pink contour lines around an object
                                    cv2.rectangle(imgContour,(x,y),(x+w, y+h),GREEN,2)      #displays a green boudnig box around an object
                                    #cv2.drawContours(imgContour,[box], -1,RED,2)            #displays a red box around an object
                                    cv2.putText(imgContour, "Item: Target "+str(int(i)),(x+w+20,y+20), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)        #displays which item number the object is
                                    cv2.putText(imgContour, "Depth(cm): "+str(float(d)),(x+w+20,y+40), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays from the object to the camera for a ping pong only
                                    cv2.putText(imgContour, "Deviation(pixels): "+str(int(deviation)),(x+w+20,y+60), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)
                                    #cv2.putText(imgContour, "Vertex: "+str(len(approx)),(x+w+20,y+80), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1) #displays number of connors around an object
                                    #cv2.putText(imgContour, "Area: "+str(int(area)),(x+w+20,y+100), cv2.FONT_HERSHEY_COMPLEX,0.5,GREEN,1)    #displays pixel area around an object
                                    cv2.circle(imgContour,(cx,cy),7,WHITE,-1) #displays centroid of object 
                                    cv2.putText(imgContour, "Centroid",(cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX,0.5,GREEN,1) #displays the word "centroid"
                                    a=np.array(['target',i,d,deviation])
                                    print(a)
                                    return a;
                                       
            elif area<Amin:
                a=np.array([i,0,0])
                print("Searching for target")
                return a;
