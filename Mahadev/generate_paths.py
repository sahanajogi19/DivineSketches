import cv2
import json

IMAGE_PATH = "mahakal_exact.png"
OUTPUT_JSON = "mahakal_paths.json"

img = cv2.imread(IMAGE_PATH)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Binary threshold for neon lines
_, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_NONE
)

height, width = gray.shape
paths = []

for contour in contours:
    if len(contour) < 30:
        continue

    path = []

    for point in contour:
        x, y = point[0]

        turtle_x = x - width / 2
        turtle_y = height / 2 - y

        path.append([float(turtle_x), float(turtle_y)])

    if len(path) > 1:
        paths.append(path)

with open(OUTPUT_JSON, "w") as f:
    json.dump({"paths": paths}, f)

print(f"Saved {len(paths)} paths")