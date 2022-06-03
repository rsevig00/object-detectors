from PIL import Image, ImageDraw
import random
import os

def yolo_to_xml_bbox(bbox, w, h):
    width_half = (bbox[2] * w) / 2
    heigh_half = (bbox[3] * h) / 2
    xmin = int(bbox[0] * w - width_half)
    ymin = int(bbox[1] * h - heigh_half)
    xmax = int(bbox[0] * w + width_half)
    ymax = int(bbox[1] * h + heigh_half)
    return [xmin, ymin, xmax, ymax]

def draw_image(img, bboxes):
    draw = ImageDraw.Draw(img)
    for bbox in bboxes:
        draw.rectangle(bbox, outline="red", width=2)
    img.show()

# Randomly select an image
input_dir = input("Type the name of the folder containing the database: ")
train_image_dir = os.path.join(input_dir, "train/images/")
train_label_dir = os.path.join(input_dir, "train/labels/")
image_filename = random.choice(os.listdir(train_image_dir))
split_filename = image_filename.split(".")
label_filename = split_filename[0] + "." + split_filename[1] + "." + split_filename[2] + ".txt"
if not os.path.exists(os.path.join(train_image_dir, image_filename)):
        print(f"{image_filename} image does not exist!")
        exit(1)

image_dir = train_image_dir + image_filename
label_dir = train_label_dir + label_filename
bboxes = []

# Collect the bboxes corresponding to the image in the PVOC format (because Pillow works with pixels so more convenient)
img = Image.open(image_dir)
with open(label_dir, 'r', encoding='utf8') as f:
    for line in f:
        data = line.strip().split(' ')
        bbox = [float(x) for x in data[1:]]
        bboxes.append(yolo_to_xml_bbox(bbox, img.width, img.height))

draw_image(img, bboxes)