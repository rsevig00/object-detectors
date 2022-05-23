from ctypes.wintypes import WORD
import xml.etree.ElementTree as ET
import glob
import os

def xml_to_yolo_bbox(bbox, w, h):
    x_center = ((bbox[2] + bbox[0])/2) / w
    y_center = ((bbox[3] + bbox[1])/2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

classes = ["Person"] # We will only use one class here
input_dir = input("Type the name of the folder containing images and XML files: ")
image_dir = input_dir
new_dir = input("Type the name of the new directory which will contain files and annotations: ")
if not os.path.isdir(new_dir):
    os.mkdir(new_dir)
output_dir = os.path.join(new_dir, "annotations/")
image_output = os.path.join(new_dir, "images/")

# If directory for annotations and images do not exist, make them
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
if not os.path.isdir(image_output):
    os.mkdir(image_output)

files = glob.glob(os.path.join(input_dir, '*.xml'))
for fil in files:

    # Get the XML files and copy the images into the new folder
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
        print(f"{filename} image does not exist!")
    # copy the images to the new image folder
    else:
        command = "cp " + os.path.join(image_dir, f"{filename}.jpg") + " " + image_output + f"{filename}.jpg"
        os.system(command)

    # Parse content of XML files
    result = []
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    for obj in root.findall('object'):
        # Convert from pvoc to yolo format
        pvoc_bbox = [int(x.text) for x in obj.find("bndbox")]
        yolo_bbox = xml_to_yolo_bbox(pvoc_bbox, width, height)
        # Convert to string
        bbox_string = " ".join([str(x) for x in yolo_bbox])
        result.append(f"0 {bbox_string}") # Index is always zero since we are working with only one class
    #If no error write the txt file corresponding to the image
    if result:
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))