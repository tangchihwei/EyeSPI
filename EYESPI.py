#THIS HAS NOT BEEN TESTED

#still need to run apt-get install python-picamera or apt-get install python3-picamera
#still need to run apt-get install python-numpy

import cv2
import sys
import picamera
from time import sleep
import glob, os
import numpy as np
import Rpi.GPIO as GPIO
import time
import requests
import json
import base64

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

# Initialize GPIO for motion sensor
sensorPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPin,GPIO.IN)

# Firebase URL
firebase_url = 'https://fordeyespi.firebaseio.com'
message_url = firebase_url+'/EyeSPI'+'/message.json'
picture_url = firebase_url + '/EyeSPI' + '/picture.json'

#Control loop

while 1:
    # Motion detect event triggered by the motion sensor
    if GPIO.input(sensorPin):
        print "Motion detected"
        captureImage()
    else:
        #Scan firebase for file
        result = requests.get(message_url, data = json.dumps(payload))
        if result:
            # Parse the file
            response = result.json()
            key = ''.join(response.keys())
            fileID = response[key]['id']
            # Delete the file
            requests.delete(firebase_url + '/EyeSPI' + '/message' + key + '.json')
            if fileID = 2:
                captureImage()
            elif fileID = 3:
                #faceDetectSequence()
    sleep(5)

# Capture an image and push it to firebase
def captureImage():
    # Capture the image
    camera.capture('image.jpg')
        image = image.jpg
        # Encode image as base64 string
        with open(image, "rb") as imageFile:
            image64str = base64.b64encode(imageFile.read())
    # Push image to firebase
    payload = {'picID':image64str}
        result = requests.post(picture_url, data = json.dumps(payload))
        # Push message to firebase
        firebaseID = result.json()['name']
        payload = {'id':1, 'picID':firebaseID, 'FL':0, 'FR':0, 'RL':0, 'RC':0, 'RR':0, 'used':0}
        result = requests.post(message_url, data = json.dumps(payload))

    return

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
    if FL >= 0.5:
        FL = 1
    else
        FL = 0
    FR = np.mean(FR_detect)
    if FR >= 0.5:
        FR = 1
    else
        FR = 0
    RL = np.mean(RL_detect)
    if RL >= 0.5:
        RL = 1
    else
        RL = 0
    RM = np.mean(RM_detect)
    if RM >= 0.5:
        RM = 1
    else
        RM = 0
    RR = np.mean(RR_detect)
    if RR >= 0.5:
        RR = 1
    else
        RR = 0

    return (FL,FR,RL,RM,RR)







