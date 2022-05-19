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
lower_limit = 0
files = glob.glob(os.path.join(image_dir, '*.jpg'))

# Shuffle the files
random.shuffle(files)

# Set the proportions
folders = {"train": 0.8, "val": 0.1, "test": 0.1}
check_sum = sum([folders[x] for x in folders])
assert check_sum == 1.0, "Split proportion is not equal to 1.0"

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
    limit = round(len(files) * folders[folder])
    for fil in files[lower_limit:lower_limit + limit]:
        copyfiles(fil, os.path.join(output_dir, folder))