import logging

import boto3
import os
import sys
from PIL import Image

# -- function for checking transparency in file
def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False

# -- function for setting log
def log_to_file(filename):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
def log_to_std_out():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

# -- start aws session with credentials | getting them from user
aws_access=input("Please enter AWS access key id: ")
aws_secret=input("Please enter AWS secret access key: ")
session = boto3.Session(
aws_access_key_id=aws_access,
aws_secret_access_key=aws_secret
)
# -- get first bucket name
arg1 = sys.argv[1]
if os.path.exists(arg1):
    arg1= (os.path.basename(arg1))

# -- get second bucket name
arg2 = sys.argv[2]
if os.path.exists(arg2):
    fn1= (os.path.basename(arg2))

# -- initiate s3 resource for download
s3 = session.resource('s3')
# -- select bucket
my_bucket = s3.Bucket(arg1)
try:
    # -- iterating through the files in first bucket
    for s3_object in my_bucket.objects.all():
        # -- split s3_object.key into path and file name, else it will give error file not found.
        path, filename = os.path.split(s3_object.key)
        my_bucket.download_file(s3_object.key, filename)
        image=Image.open(filename)
        # -- check for transparency if yes log, else upload it to the other bucket
        if has_transparency(image):
            log_to_file("transparent.log")
            logging.info(f'{filename} has transparent pixels')
        else:
            s3_2 = session.client('s3')
            with open(filename, "rb") as f2:
                s3_2.upload_fileobj(f2, arg2, s3_object.key)
except:
    log_to_std_out()
    logging.error("Exception occurred", exc_info=True)