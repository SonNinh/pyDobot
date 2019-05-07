import cv2
import numpy
from math import atan, pi, fabs, sqrt, tan
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from time import sleep
import sys


def get_dist_3d_p2p(color, center):
    return sqrt((color[0]-center[0])**2 + (color[1]-center[1])**2 + (color[2]-center[2])**2)


def get_nearest_color(color_mean, color_center):
    nearest_dist = get_dist_3d_p2p(color_mean, color_center[3])
    print(nearest_dist)
    nearest_color = 3
    for idx, center in enumerate(color_center[:3]):
        dist = get_dist_3d_p2p(color_mean, center)
        print(dist)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest_color = idx
    
    return nearest_color


def detect_color(color_center, hsv_img, p_blue, p_green, p_red, p_yellow):
    '''
    '''
    fig = pyplot.figure()
    ax = Axes3D(fig)
    color_ls = ['red', 'green', 'blue', 'yellow']
    
    color_mean = hsv_img.mean(axis=0).mean(axis=0).astype(int)
    color_id = get_nearest_color(color_mean, color_center)
    # ax.scatter(color_mean[0], color_mean[1], color_mean[2], c=color_ls[color_id], s=60)
    print(color_ls[color_id])
    # ax.scatter(p_blue[0], p_blue[1], p_blue[2], c=color_ls[2])
    # ax.scatter(p_green[0], p_green[1], p_green[2], c=color_ls[1])
    # ax.scatter(p_red[0], p_red[1], p_red[2], c=color_ls[0])
    # ax.scatter(p_yellow[0], p_yellow[1], p_yellow[2], c=color_ls[3])

    # pyplot.show()


def get_color_center():
    color_ls = ['red', 'green', 'blue', 'yellow']
    color_center = []
    for color in color_ls:
        img = cv2.imread('photos/'+color+'.png')
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        p = img.mean(axis=0).mean(axis=0).astype(int)
        color_center.append(list(p))

    return color_center


def main():
    cap = cv2.VideoCapture(int(sys.argv[1]))
    cap.set(3, 320)
    cap.set(4, 240)
    # cap.set(5, 30)
    sleep(0.5)

    red = cv2.imread("photos/red.png")
    hsv = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
    p_red = hsv.mean(axis=0).mean(axis=0).astype(int)
    green = cv2.imread("photos/green.png")
    hsv = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    p_green = hsv.mean(axis=0).mean(axis=0).astype(int)
    blue = cv2.imread("photos/blue.png")
    hsv = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
    p_blue = hsv.mean(axis=0).mean(axis=0).astype(int)
    yellow = cv2.imread("photos/yellow.png")
    hsv = cv2.cvtColor(yellow, cv2.COLOR_BGR2HSV)
    p_yellow = hsv.mean(axis=0).mean(axis=0).astype(int)
    

    color_center = get_color_center()
    while(True):
        frame = cap.read()[1]
        crop_img = frame[100:120, 100:120]

        cv2.imshow('edges', crop_img)
        # hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        detect_color(color_center, crop_img, p_blue, p_green, p_red, p_yellow)

        # cv2.imshow('res', hsv)
        key = cv2.waitKey(100) & 0xFF
        if key == 27:
            break
        # elif key == ord("c"):
        #     cv2.imwrite("photos/"+sys.argv[2], frame)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


# fig = pyplot.figure()
# ax = Axes3D(fig)

# img = cv2.imread("photos/red.png")
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# p = hsv.mean(axis=0).mean(axis=0).astype(int)
# ax.scatter(p[0], p[1], p[2], c='red')
# # print(p)

# img = cv2.imread("photos/green.png")
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# p = hsv.mean(axis=0).mean(axis=0).astype(int)
# ax.scatter(p[0], p[1], p[2], c='green')

# img = cv2.imread("photos/blue.png")
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# p = hsv.mean(axis=0).mean(axis=0).astype(int)
# ax.scatter(p[0], p[1], p[2], c='blue')

# img = cv2.imread("photos/yellow.png")
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# p = hsv.mean(axis=0).mean(axis=0).astype(int)
# ax.scatter(p[0], p[1], p[2], c='yellow')

# # print(p)



# # sequence_containing_x_vals = list(range(0, 100))
# # sequence_containing_y_vals = list(range(0, 100))
# # sequence_containing_z_vals = list(range(0, 100))

# # print(sequence_containing_x_vals)

# # random.shuffle(sequence_containing_x_vals)
# # random.shuffle(sequence_containing_y_vals)
# # random.shuffle(sequence_containing_z_vals)

# pyplot.show()

# import numpy as np
# import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 1])

# for i in range(10):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.05)

# plt.show()