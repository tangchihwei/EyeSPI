#still need to run apt-get install python-picamera or apt-get install python3-picamera
#still need to run apt-get install python-numpy

import os
import cv2
import sys

from time import sleep
import glob
import numpy as np
import RPi.GPIO as GPIO
import time
import requests
import json
import base64

#Define Seat Position Constants
'''
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
'''

#set haar cascade file
#cascPath = config.xml
# Create the haar cascade
#faceCascade = cv2.CascadeClassifier(cascPath)

# Initialize GPIO for motion sensor
sensorPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPin,GPIO.IN)
State_MotionDetect False
State_FacialDetect False
counter = 0

controllerId = 0
userAppId = 1
rpiReqId = 2
faceDetId = 3
motionDetId = 4


# Firebase URL
firebase_url = 'https://fordeyespi.firebaseio.com'
message_url = firebase_url+'/EyeSPI'+'/message.json'
picture_url = firebase_url + '/EyeSPI' + '/picture.json'
    
# Capture an image and push it to firebase
def captureImage():
    # Capture the image
	os.system('fswebcam image.jpg')
	image = 'image.jpg'
        # Encode image as base64 string
	with open(image, "rb") as imageFile:
            image64str = base64.b64encode(imageFile.read())
    # Push image to firebase
	payload = {'picID':image64str}
	result = requests.post(picture_url, data = json.dumps(payload))
	print "pic post status"
	print result.status_code
        # Push message to firebase
	firebaseID = result.json()['name']
	payload = {'id':userAppId, 'picID':firebaseID, 'FL':0, 'FR':0, 'RL':0, 'RC':0, 'RR':0, 'used':0}
	result = requests.post(message_url, data = json.dumps(payload))
	print "message post status"
	print result.status_code
	return

#face detection
def faceDetectSequence():#<----------------------Function 2, Nitin
    for shot in range(0,6,1):
        #sleep(5)
        camera.capture("file"+str(shot)+".jpg")``````#concatenate names
    #access taken pictures
    os.chdir("/mydir")

    FL=0
    FR=0
    RL=0
    RC=0
    RR=0
    
   # loop_ind=0
        
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
                FL=1
            #Front Right
        elif (FR_BLP_x < (x+w/2) && FR_TRP_x > (x+w/2) && FR_BLP_y < (y+h/2) && FR_TRP._ > (y+h/2)):
                FR=1
            #Rear Left
        elif (RL_BLP_x < (x+w/2) && RL_TRP_x > (x+w/2) && RL_BLP_y < (y+h/2) && RL_TRP_y > (y+h/2)):
                RL=1
            #Rear Middle
        elif (RC_BLP_x < (x+w/2) && RC_TRP_x > (x+w/2) && RC_BLP_y < (y+h/2) && RM_TRP_y > (y+h/2)):
                RC=1
            #Rear Right
        elif (RR_BLP_x < (x+w/2) && RR_TRP_x > (x+w/2) && RR_BLP_y < (y+h/2) && RR_TRP_y > (y+h/2)):
                RR=1

        # loop_ind+=1
            
    # FL = np.mean(FL_detect)
#     if FL >= 0.5:
#         FL = 1
#     else
#         FL = 0
#     FR = np.mean(FR_detect)
#     if FR >= 0.5:
#         FR = 1
#     else
#         FR = 0
#     RL = np.mean(RL_detect)
#     if RL >= 0.5:
#         RL = 1
#     else
#         RL = 0
#     RC = np.mean(RC_detect)
#     if RC >= 0.5:
#         RC = 1
#     else
#         RC = 0
#     RR = np.mean(RR_detect)
#     if RR >= 0.5:
#         RR = 1
#     else
#         RR = 0

    return (FL,FR,RL,RC,RR)

#CONTROL

while 1:
    #execute every 5 seconds
    sleep(5)
    
	result = requests.get(message_url)
	resultStr = result.text
	if resultStr == "null":
		print "no message"
    else:
        response = result.json()
        key = ''.join(response.keys())
        fileId = response[key]['id']
        result = requests.delete(firebase_url + '/EyeSPI' + '/message'+'/' + key + '.json')
        
        if fileId is rpiReqId:
            #pi take a picture and send back.
        elif fileId is faceDetId:
            #start facial detection
            State_FacialDetect = True
            State_MotionDetect = False
        elif fileId is motionDetId:
            #start motion detection
            State_FacialDetect = False
            State_MotionDetect = True
        else: 
            print "Error: Unexpected Id"
            
    #main control 
    if State_FacialDetect is True:
        if counter is 0:
        #function to trigger facial detect
            faceDetResult = faceDetectSequence()
            payload = {'id':controllerId, 'picID':0, 'FL':faceDetResult[0], 'FR':faceDetResult[1], 'RL':faceDetResult[2], 'RC':faceDetResult[3], 'RR':faceDetResult[4], 'used':0} 
        	result = requests.post(message_url, data = json.dumps(payload))
            #Next execution: ~60 seconds
            counter = 12
    elif State_MotionDetect is True:
        if counter is 0:
            #check Motion sensor input pin
            if GPIO_input(sensorPin):
                print "Motion Detected"
                captureimage()
                #Next execution: ~60 seconds
                counter = 12
    #decrement counter            
    if counter is not 0:
        counter = counter - 1
            
'''
    # Motion detect event triggered by the motion sensor
        if GPIO.input(sensorPin):
                print "Motion detected"
                captureImage()
        else:
        #Scan firebase for file
                result = requests.get(message_url)
                
		if len(result.text) > 15:
            # Parse the file
                        response = result.json()
                        key = ''.join(response.keys())
                        fileID = response[key]['id']
            # Delete the file

                        result = requests.delete(firebase_url + '/EyeSPI' + '/message'+'/' + key + '.json')
			print key
			#print "deleted message"
                        if fileID is 2:
				print "fileID is 2"
                                captureImage()
                        elif fileID is 3:
				print "fileID is 3"
'''
