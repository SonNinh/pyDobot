import cv2
from time import sleep
import numpy as np
from random import randint
from math import atan, pi, fabs, sqrt


rect_width = 33
delta_dir = 7*pi/180

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged


def get_distance(p1, p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def find_in_neighbour(line, ls_of_cen_and_dir):
    center = line[0]
    direction = line[1]
    res = [[],[]]

    for i, each in enumerate(ls_of_cen_and_dir):
        distance = get_distance(center, each[0])
        if distance < rect_width*1.5 and distance > rect_width*0.3:
            if fabs(direction-each[1]) < delta_dir:
                res[0].append(i)
            elif fabs(fabs(direction-each[1])-pi/2) < delta_dir:
                res[1].append(i)
        elif distance < rect_width*0.3:
            if fabs(direction-each[1]) < delta_dir:
                res[0].append(i)

    return res


def get_center_direction_len(ls_of_lines):
    res = list()

    for line in ls_of_lines:
        x1, y1, x2, y2 = line[0]
        p1 = (x1, y1)
        p2 = (x2, y2)
        line_center = [(x1+x2)//2, (y1+y2)//2]
        lenght = get_distance(p1, p2)

        if x1 != x2:
            line_direction = atan((y1-y2)/(x1-x2))
        else:
            line_direction = pi/2
        res.append([line_center, line_direction, lenght])

    return res

def retangle_detect(ls_of_lines):
    ls_of_rect = list()

    ls_of_cen_dir_len = get_center_direction_len(ls_of_lines)

    for line in ls_of_cen_dir_len:
        if line[2] > rect_width*0.5:
            ls_of_rect.append(find_in_neighbour(line, ls_of_cen_dir_len))
    
    print(len(ls_of_rect))
    return ls_of_rect


def main():

    while(True):
        crop_img = cv2.imread("photos/red_4_b.png")
        # blur = cv2.GaussianBlur(crop_img, (15, 15), 0) # loc nhieu
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = auto_canny(gray)
        # edged = cv2.Canny(gray, 20, 250)

        lines = cv2.HoughLinesP(edged, 1, np.pi/180, 15, maxLineGap=3)
        color = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
        if lines is not None:
            ls_of_rect = retangle_detect(lines)

            # for rect in ls_of_rect:
            #     output = np.zeros((250, 150, 3), dtype=crop_img.dtype)
            #     for i in rect[0]:
            #         x1, y1, x2, y2 = lines[i][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[0], 2)
            #     for i in rect[1]:
            #         x1, y1, x2, y2 = lines[i][0]
            #         cv2.line(output, (x1, y1), (x2, y2), color[1], 2)

            #     cv2.imshow("ouput", output)
            #     cv2.imshow('origin', crop_img)
            #     cv2.waitKey()

        

        break
        

if __name__ == '__main__':
    main()
