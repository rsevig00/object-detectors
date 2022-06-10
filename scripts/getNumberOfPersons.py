from cgi import test
from email.mime import base
import random
import glob
import os

input_dir = input("Type the name of the folder containing dataset: ")

total_bboxes = 0
image_path = os.path.join(input_dir, "test/", "images/")
label_path = os.path.join(input_dir, "test/", "labels/")

files = glob.glob(os.path.join(image_path, '*.jpg'))

for fil in files :

        basename = os.path.basename(fil)
        split_filename = basename.split(".")
        filename = split_filename[0] + "." + split_filename[1] + "." + split_filename[2]
        label_filename = os.path.join(label_path, f"{filename}.txt")

        # Check bboxes of every labeled image
        if os.path.exists(label_filename):
            with open(label_filename, 'r', encoding='utf8') as f:
                for line in f:
                    total_bboxes += 1

print("Number of person in the test dataset : " + str(total_bboxes) + "\n");