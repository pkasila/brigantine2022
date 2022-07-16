import cv2
import numpy as np
import argparse

# Parse arguments
parser = argparse.ArgumentParser("latex_img_optimizer")
parser.add_argument("src", help="Source image path", type=str)
parser.add_argument("out", help="Output image path", type=str)
args = parser.parse_args()

img = cv2.imread(args.src, 0)

_, threshed = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnt = np.vstack(cnts)

x, y, w, h = cv2.boundingRect(cnt)
img = img[y:y + h, x:x + w]

_, alpha = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGRA)

b, g, r, _ = cv2.split(img)

bgra = [b, g, r, alpha]

dst = cv2.merge(bgra)

cv2.imwrite(args.out, dst)
