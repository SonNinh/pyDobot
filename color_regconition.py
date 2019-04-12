import cv2
from time import sleep
import numpy as np
from random import randint

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged


def find_color(img_hsv, lower, upper):
    lower_np = np.array(lower, dtype="uint8")
    upper_np = np.array(upper, dtype="uint8")
    return cv2.inRange(img_hsv, lower_np, upper_np)


def main():

    while(True):
        crop_img = cv2.imread("photos/red_4_a.png")
        # blur = cv2.GaussianBlur(crop_img, (15, 15), 0) # loc nhieu
        # hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # chuyen doi khong gian mau

        # #red
        # lower = [120, 93, 123]
        # upper = [185, 255, 255]
        # mask_red = find_color(hsv, lower, upper)

        # lower = [0, 136, 123]
        # upper = [56, 255, 255]
        # mask_red += find_color(hsv, lower, upper)
        
        # output = cv2.bitwise_and(crop_img, crop_img, mask = mask_red)
        # gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(crop_img, (5, 5), 0) # loc nhieu
        # median = cv2.medianBlur(gray,11)
        edged = auto_canny(crop_img)
        # edged = cv2.Canny(gray, 20, 250)

        lines = cv2.HoughLinesP(edged, 1, np.pi/180, 12, maxLineGap=5)
        color = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(crop_img, (x1, y1), (x2, y2), color[randint(0, 2)], 2)

        # cv2.imshow('res', output)
        cv2.imshow('edges', edged)
        cv2.imshow('origin', crop_img)

        if cv2.waitKey(500) & 0xFF == 27:
            break


if __name__ == '__main__':
    main()
    