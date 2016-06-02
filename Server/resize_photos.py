import cv2
import sys

img_name = sys.argv[1]
output_img_name = sys.argv[2]
img_width = int(sys.argv[3])
img_height = int(sys.argv[4])

img = cv2.imread(img_name)
img_resize = cv2.resize(img,(img_height,img_width))
cv2.imwrite(output_img_name,img_resize)