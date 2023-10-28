import cv2
import numpy as np
import time
import argparse

parser = argparse.ArgumentParser()
# Input argument
parser.add_argument("--video", help = "Path to input video file. Skip this argument to capture frames from a camera.")

args = parser.parse_args()

print("""
Harry: Greetings, dear friend! 
	   Would you care to experience the wonders of my invisibility cloak? 
	   It's nothing short of magical, I assure you! 
	   Ready yourself for a spellbinding adventure... 
	   Prepare to dissolve into the realm of the unseen! 
    """)

# Creating an VideoCapture object
# This will be used for image acquisition later in the code.
cap = cv2.VideoCapture(args.video if args.video else 0)

# We give some time for the camera to setup
time.sleep(3)
count = 0
background=0

# Step 1: Capturing and storing the static background frame
for i in range(60):
	ret,background = cap.read()

#background = np.flip(background,axis=1)

while(cap.isOpened()):
	ret, img = cap.read()
	if not ret:
		break
	count+=1
	#img = np.flip(img,axis=1)
	
	# Step 2: Red color detection
    # Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Generating mask to detect red color
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2

    # Step 3: Segmenting out the detected red colored cloth
	# Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)


    # Step 4: Generating the final augmented output to create a magical effect
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	final_output = cv2.addWeighted(res1,1,res2,1,0)

	cv2.imshow('Welcome to the world of magic..',final_output)
	k = cv2.waitKey(10)
	
    # Hit escape to stop the program
	if k == 27:
		break