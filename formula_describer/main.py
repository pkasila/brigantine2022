import json
import os.path

import cv2
import argparse
import glob

# Parse arguments
parser = argparse.ArgumentParser("formula_describer")
parser.add_argument("src", help="Source directory path", type=str)
parser.add_argument("out", help="Output JSON path", type=str)
args = parser.parse_args()

images = []

for file in glob.glob("tmp/out/*.png"):
    img = cv2.imread(file, 0)
    width, height, *_ = img.shape
    images.append({
        "file": os.path.basename(file),
        "size": {
            "width": width,
            "height": height
        }
    })

dataset = {
    "images": images,
    "total": len(images)
}

with open(args.out, "wb") as f:
    f.write(json.dumps(dataset, indent=2).encode('utf8'))
