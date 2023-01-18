from __future__ import print_function
import os
import sys
import cv2 as cv
from PIL import Image
import numpy as np

#A Python script that detects faces in an image using OpenCV, and saves the headshots of the detected faces to a specified directory.
#arg1 : Path to image
#arg 2: headshot directory
#output: number of faces detected

def detectAndDisplay(image, location, file_format):
    # -- Change the color space and apply histogram equalization
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image_gray = cv.equalizeHist(image_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(image_gray)
    count=1
    for (x,y,w,h) in faces:
        # -- Draw bounding rectangle
        detected_frame = cv.rectangle(image, (x,y), (x+h, y+w), (255, 0, 0), 4)
        # -- Crop the image with PIL
        cv.imwrite('temp.jpeg', detected_frame)
        PIL_image = Image.open('temp.jpeg')
        cropped_image=PIL_image.crop((x,y ,x+h, y+w))
        # -- Return image to opencv format
        open_cv_image = np.array(cropped_image)
        # -- change the color space to rgb
        rgb_headshot=cv.cvtColor(open_cv_image, cv.COLOR_BGR2RGB)
        cv.imwrite(f"{location}/face{count}{file_format}", rgb_headshot)
        count=count+1
    return detected_frame, count-1
# -- define the path of the face cascade xml file
face_cascade_name = 'C:/Users/Software/PycharmProjects/Problem1/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml'
face_cascade = cv.CascadeClassifier()
#-- 1. Load the cascade
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
# -- get image path and name from args
arg1 = sys.argv[1]
if os.path.exists(arg1):
    arg1= (os.path.basename(arg1))

# -- get headshot path
arg2 = sys.argv[2]
if os.path.exists(arg2):
    fn1= (os.path.basename(arg2))

# -- Read the image
img = cv.imread(arg1)
if img is None:
    print('--(!) Cannot read the image')
# -- extract the file format
sub_idx=arg1.index('.')
formt=arg1[sub_idx:]

# Run the detection
img, c=detectAndDisplay(img, arg2, formt)
#Print output
print (f"Number of faces detected: {c}")

cv.imshow("image", img)
cv.waitKey(0)

