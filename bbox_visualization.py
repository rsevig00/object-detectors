from PIL import Image, ImageDraw
import random
import os

def yolo_to_xml_bbox(bbox, w, h):
    width_half = bbox[2] / 2
    heigh_half = bbox[3] / 2
    xmin = int(bbox[0] - width_half)
    ymin = int(bbox[1] - heigh_half)
    xmax = int(bbox[0] + width_half)
    ymax = int(bbox[1] + heigh_half)
    return [xmin, ymin, xmax, ymax]

def draw_image(img, bboxes):
    draw = ImageDraw.Draw(img)
    for bbox in bboxes:
        draw.rectangle(bbox, outline="red", width=2)
    img.show()

# Randomly select an image
input_dir = input("Type the name of the folder containing images and annotations: ")
image_dir = os.path.join(input_dir, "images/")
annotation_dir = os.path.join(input_dir, "annotations/")
num_of_images = len([file for file in os.listdir(image_dir)]) + 1
image_num = random.randint(1, num_of_images)
filename = f"gss{image_num}"
if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
        print(f"{filename} image does not exist!")
        exit(1)

image_filename = image_dir + f"{filename}.jpg"
label_filename = annotation_dir + f"{filename}.txt"
bboxes = []

# Collect the bboxes corresponding to the image in the PVOC format (because Pillow works with pixels so more convenient)
img = Image.open(image_filename)
with open(label_filename, 'r', encoding='utf8') as f:
    for line in f:
        data = line.strip().split(' ')
        bbox = [float(x) for x in data[1:]]
        bboxes.append(yolo_to_xml_bbox(bbox, img.width, img.height))

draw_image(img, bboxes)