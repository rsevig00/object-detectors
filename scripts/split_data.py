from cgi import test
from decimal import Decimal
import random
import glob
import os

def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    # image
    src = fil
    dest = os.path.join(root_dir, "images/", f"{filename}.jpg")
    command = "cp " + src + " " + dest
    os.system(command)

    # label
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, "annotations/", f"{filename}.txt")
    if os.path.exists(src):
        command = "cp " + src + " " + dest
        os.system(command)


input_dir = input("Type the name of the folder containing non-splitted images and annotations: ")
image_dir = os.path.join(input_dir, "images/")
label_dir = os.path.join(input_dir, "annotations")
output_dir = input("Type the name of the folder containing the new splitted data: ")
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
lower_limit_small = 0
lower_limit_medium = 0
lower_limit_large = 0
files = glob.glob(os.path.join(image_dir, '*.jpg'))

# Shuffle the files
random.shuffle(files)

# Set the proportions
train_value = Decimal(input("Type the percentage of data to use for training: "))
val_value = Decimal(input("Type the percentage of data to use for validation: "))
test_value = Decimal(input("Type the percentage of data to use for testing: "))
folders = {"train": train_value, "val": val_value, "test": test_value}
assert train_value + val_value + test_value == 1.0, "Split proportion is not equal to 1.0"

# Separate files in small, medium, and large bbox
small = []
medium = []
large = []
for fil in files:
    bboxes = []
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    label_filename = os.path.join(label_dir, f"{filename}.txt")

    # Collect the bboxes of the file
    if os.path.exists(label_filename):
        with open(label_filename, 'r', encoding='utf8') as f:
            for line in f:
                data = line.strip().split(' ')
                bb = [float(x) for x in data[1:]]
                bboxes.append(bb)
    
    # Determine if there is a large or a small bbox in the image (since there is more small
    # bboxes than medium and large in SARD we clasify the image depending on the largest
    # bbox in the image)
    max_size = 0
    for bbox in bboxes:
        w, h = bbox[2], bbox[3]
        if w*h > max_size:
            max_size = w*h
    if max_size < 32^2:
        small.append(fil)
    elif max_size < 96^2 and max_size > 32^2:
        medium.append(fil)
    else:
        large.append(fil)

# Create folders and put images in it (no balancing of image proportion for now)
for folder in folders:
    if not os.path.isdir(os.path.join(output_dir, folder)):
        os.mkdir(os.path.join(output_dir, folder))
    temp_label_dir = os.path.join(output_dir, folder, "annotations/")
    if not os.path.isdir(temp_label_dir):
        os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(output_dir, folder, "images/")
    if not os.path.isdir(temp_image_dir):
        os.mkdir(temp_image_dir)

    # For each category we remember the lower limit (can be optimized)
    limit_small = round(len(small) * folders[folder])
    for fil in small[lower_limit_small: lower_limit_small + limit_small]:
        copyfiles(fil, os.path.join(output_dir, folder))
    lower_limit_small = lower_limit_small + limit_small

    limit_medium = round(len(medium) * folders[folder])
    for fil in medium[lower_limit_medium: lower_limit_medium + limit_medium]:
        copyfiles(fil, os.path.join(output_dir, folder))
    lower_limit_medium = lower_limit_medium + limit_medium

    limit_large = round(len(large) * folders[folder])
    for fil in large[lower_limit_large: lower_limit_large + limit_large]:
        copyfiles(fil, os.path.join(output_dir, folder))
    lower_limit_large = lower_limit_large + limit_large