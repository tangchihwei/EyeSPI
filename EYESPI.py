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

#Front Left
FL_TLP_x =  733
FL_TLP_y =  200 #Bottom left point
FL_BRP_x =  900 #Top right point
FL_BRP_y =  500 #Top right point

#Front Right
FR_TLP_x =  150 #Bottom left point
FR_TLP_y =  200 #Bottom left point
FR_BRP_x =  323 #Top right point
FR_BRP_y =  500 #Top right point

#Rear Left
RL_TLP_x =  640 #Bottom left point
RL_TLP_y =  125 #Bottom left point
RL_BRP_x =  750 #Top right point
RL_BRP_y =  351 #Top right point

#Rear Middle
RM_TLP_x =  480 #Bottom left point
RM_TLP_y =  125 #Bottom left point
RM_BRP_x =  590 #Top right point
RM_BRP_y =  351 #Top right point

#Rear Right
RR_TLP_x =  323 #Bottom left point
RR_TLP_y =  125 #Bottom left point
RR_BRP_x =  430 #Top right point
RR_BRP_y =  351 #Top right point


#set haar cascade file
cascPath = 'config.xml'
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Initialize GPIO for motion sensor
sensorPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPin,GPIO.IN)
State_MotionDetect = False
State_FacialDetect = False
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
	os.system('fswebcam image.jpg -r 1280x720')
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
   # for shot in range(0,6,1):
        #sleep(5)
    #    camera.capture("file"+str(shot)+".jpg")``````#concatenate names
    #access taken pictures
    

    #os.chdir("/mydir")

    os.system('fswebcam imagePi.jpg -r 1280x720')
    
    file = cv2.imread('imagePi.jpg')

    cv2.imshow("Faces", file)
    
    print "in face detection sequence"
	
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
                                             scaleFactor=1.15,
                                             minNeighbors=5,
                                             minSize=(30, 30),
                                             flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                                             )
        

    print str(faces)

# Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    	cv2.rectangle(file, (x, y), (x+w, y+h), (0, 255, 0), 2)
    	print str(x) + " " + str(y) + " " + str(x+w) + " " + str(y+h) 

#Draw test rectangle 
#RL 323 125 430 351
#RC 480 125 590 351
#RR 640 125 750 351
#FL 150 200 323 500
#FR 733 200 900 500 

    cv2.rectangle(file, (323, 125), (430,351), (255, 0, 0), 2)
    cv2.rectangle(file, (480, 125), (590,351), (255, 0, 0), 2)
    cv2.rectangle(file, (640, 125), (750,351), (255, 0, 0), 2)
    cv2.rectangle(file, (150, 200), (323,500), (255, 0, 0), 2)
    cv2.rectangle(file, (733, 200), (900,500), (255, 0, 0), 2)

        #set seat pos to true for each captured image if face within bounds
    for (x, y, w, h) in faces:
            #check if faces in seat region
            #Front Left
        if (FL_TLP_x < (x+w/2) and  FL_BRP_x > (x+w/2) and FL_TLP_y < (y+h/2) and FL_BRP_y > (y+h/2)):
                FL=1
		print "FL"
            #Front Right
        elif (FR_TLP_x < (x+w/2) and FR_BRP_x > (x+w/2) and FR_TLP_y < (y+h/2) and FR_BRP_y > (y+h/2)):
                FR=1
		print "FR"
            #Rear Left
        elif (RL_TLP_x < (x+w/2) and RL_BRP_x > (x+w/2) and RL_TLP_y < (y+h/2) and RL_BRP_y > (y+h/2)):
                RL=1
		print "RL"
            #Rear Middle
        elif (RM_TLP_x < (x+w/2) and RM_BRP_x > (x+w/2) and RM_TLP_y < (y+h/2) and RM_BRP_y > (y+h/2)):
                RC=1
		print "RC"
            #Rear Right
        elif (RR_TLP_x < (x+w/2) and RR_BRP_x > (x+w/2) and RR_TLP_y < (y+h/2) and RR_BRP_y > (y+h/2)):
                RR=1
		print "RR"
#	print str(x) + " " + str(y) + " " + str(w) + " " + str(h)

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
	sleep(3)
    
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
			captureImage()
       		elif fileId is faceDetId:
            #start facial detection
        		State_FacialDetect = True
        		State_MotionDetect = False
        	elif fileId is motionDetId:
            #start motion detection
        		State_FacialDetect = False
        		State_MotionDetect = True
			print "enable motion detect"
        	else: 
        		print "Error: Unexpected Id"
            
    #main control 
	if State_FacialDetect is True:
		if counter is 0:
        #function to trigger facial detect
            		faceDetResult = faceDetectSequence()
			print "FL FR RL RC RR "+str(faceDetResult)
        	    	payload = {'id':controllerId, 'picID':0, 'FL':faceDetResult[0], 'FR':faceDetResult[1], 'RL':faceDetResult[2], 'RC':faceDetResult[3], 'RR':faceDetResult[4], 'used':0} 
        		result = requests.post(message_url, data = json.dumps(payload))
            #Next execution: ~60 seconds
            		counter = 12
	elif State_MotionDetect is True:
		print "in motion detect loop"
		if counter is 0:
            #check Motion sensor input pin
			print "counter 0"
			if GPIO.input(sensorPin):
        	       		print "Motion Detected"
               		 	captureImage()
                #Next execution: ~60 seconds
               			counter = 12
    #decrement counter            
	if counter is not 0:
		counter=counter-1
            
