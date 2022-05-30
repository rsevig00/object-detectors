from cgi import test
import random
import glob
import os

input_dir = input("Type the name of the folder containing splitted dataset: ")

sets = ["train", "valid", "test"]

for set in sets :
    
    small_bboxes = 0
    medium_bboxes = 0
    large_bboxes = 0
    total_bboxes = 0
    image_path = os.path.join(input_dir, set, "images/")
    label_path = os.path.join(input_dir, set, "labels/")

    files = glob.glob(os.path.join(image_path, '*.jpg'))

    for fil in files :

        bboxes = []
        basename = os.path.basename(fil)
        filename = os.path.splitext(basename)[0]
        label_filename = os.path.join(label_path, f"{filename}.txt")

        # Check bboxes of every labeled image
        if os.path.exists(label_filename):
            with open(label_filename, 'r', encoding='utf8') as f:
                for line in f:
                    data = line.strip().split(' ')
                    bb = [float(x) for x in data[1:]]
                    bboxes.append(bb)
                
        for bbox in bboxes:
            total_bboxes += 1
            w, h = bbox[2]*416, bbox[3]*416 # images stretched to 416pxs
            size = w*h
            if size < 32^2:
                small_bboxes += 1
            elif size < 96^2 and size > 32^2:
                medium_bboxes += 1
            else:
                large_bboxes += 1
    
    ratios = [small_bboxes / total_bboxes, medium_bboxes / total_bboxes, large_bboxes / total_bboxes]
    print("Ratios of [small, medium, large] images in the " + set + " set")
    print(ratios)
    print("\n")
