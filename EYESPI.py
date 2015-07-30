#THIS HAS NOT BEEN TESTED

#still need to run apt-get install python-picamera or apt-get install python3-picamera
#still need to run apt-get install python-numpy

import cv2
import sys
import picamera
from time import sleep
import glob, os
import numpy as np

#Define Seat Position Constants

#Front Left
FL_BLP_x =  #Bottom left point (x,y)
FL_BLP_y =  #Bottom left point
FL_TRP_x =  #Top right point
FL_TRP_y =  #Top right point

#Front Right
FR_BLP_x =  #Bottom left point
FR_BLP_y =  #Bottom left point
FR_TRP_x =  #Top right point
FR_TRP_y =  #Top right point

#Rear Left
RL_BLP_x =  #Bottom left point
RL_BLP_y =  #Bottom left point
RL_TRP_x =  #Top right point
RL_TRP_y =  #Top right point

#Rear Middle
RM_BLP_x =  #Bottom left point
RM_BLP_y =  #Bottom left point
RM_TRP_x =  #Top right point
RM_TRP_y =  #Top right point

#Rear Right
RR_BLP_x =  #Bottom left point
RR_BLP_y =  #Bottom left point
RR_TRP_x =  #Top right point
RR_TRP_y =  #Top right point

#intilize camera
camera = picamera.PiCamera()

#set haar cascade file
cascPath = config.xml
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

#taking an image
#camera.capture('image.jpg')<--------------------Function 1, Nitin

#face detection
def faceDetectSequence():#<----------------------Function 2, Nitin
    for shot in range(0,6,1):
        sleep(5)
        camera.capture("file"+str(shot)+".jpg")``````#concatenate names
    #access taken pictures
    os.chdir("/mydir")

    FL_detect=[0,0,0,0,0,0]
    FR_detect=[0,0,0,0,0,0]
    RL_detect=[0,0,0,0,0,0]
    RM_detect=[0,0,0,0,0,0]
    RR_detect=[0,0,0,0,0,0]
    loop_ind=0
    for file in glob.glob("*.jpg"):
        
        # Read the image
        gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
                                             gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(30, 30),
                                             flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                                             )
        
        #set seat pos to true for each captured image if face within bounds
        for (x, y, w, h) in faces:
            #check if faces in seat region
            #Front Left
            if (FL_BLP_x < (x+w/2) && FL_TRP_x > (x+w/2) && FL_BLP_y < (y+h/2) && FL_TRP_y > (y+h/2)):
                FL_detect[loop_ind]=1
            #Front Right
            elif (FR_BLP_x < (x+w/2) && FR_TRP_x > (x+w/2) && FR_BLP_y < (y+h/2) && FR_TRP._ > (y+h/2)):
                FR_detect[loop_ind]=1
            #Rear Left
            elif (RL_BLP_x < (x+w/2) && RL_TRP_x > (x+w/2) && RL_BLP_y < (y+h/2) && RL_TRP_y > (y+h/2)):
                RL_detect[loop_ind]=1
            #Rear Middle
            elif (RM_BLP_x < (x+w/2) && RM_TRP_x > (x+w/2) && RM_BLP_y < (y+h/2) && RM_TRP_y > (y+h/2)):
                RM_detect[loop_ind]=1
            #Rear Right
            elif (RR_BLP_x < (x+w/2) && RR_TRP_x > (x+w/2) && RR_BLP_y < (y+h/2) && RR_TRP_y > (y+h/2)):
                RR_detect[loop_ind]=1

        loop_ind+=1
            
    FL = np.mean(FL_detect)
    FR = np.mean(FR_detect)
    RL = np.mean(RL_detect)
    RM = np.mean(RM_detect)
    RR = np.mean(RR_detect)

    return (FL,FR,RL,RM,RR)







