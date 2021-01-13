import cv2
import pytesseract
import difflib
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input dataset of images")
args = vars(ap.parse_args())

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import re
from difflib import get_close_matches

img = cv2.imread(args["image"])

img_data = pytesseract.image_to_string(img)

print(img_data)

img_lines = img_data.splitlines()

# turn to lower case and remove empty lines
img_lines = [line.lower() for line in img_lines if line.strip()]


date_pattern = "(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/\d\d"

# find date_str
date_str = None
for line in img_lines:
    # print(line)
    match = re.match(date_pattern, line)
    if match:
        date_str = match.group(0)


MARKETS = ["walmart", "costco"]

# find market_str
market_str = None
accuracy = 0.6

for market in MARKETS:
    for line in img_lines:
        words = line.split()
        # Get the single best match in line
        matches = get_close_matches(market, words, n=1, cutoff=accuracy)
        if matches:
            market_str = market

# Printing
print("Date: {}".format(date_str))
print("Market: {}".format(market_str))
print("")
