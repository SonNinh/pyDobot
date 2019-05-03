# import cv2
# import numpy
# from matplotlib import pyplot
# from mpl_toolkits.mplot3d import Axes3D
# import random


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

import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

plt.show()