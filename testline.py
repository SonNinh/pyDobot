import cv2
import numpy as np
from time import time


title_window = 'Linear Blend'
cv2.namedWindow(title_window)

def on_trackbar(val):
    pass

cv2.createTrackbar("thres", title_window , 0, 50, on_trackbar)
cv2.createTrackbar("lin", title_window , 0, 50, on_trackbar)
cv2.createTrackbar("minlen", title_window , 0, 50, on_trackbar)
cv2.createTrackbar("maxgap", title_window , 0, 50, on_trackbar)


def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged


while True:
	start_time = time()
	crop_img = cv2.imread("photos/red_4_b.png")
	# blur = cv2.GaussianBlur(crop_img, (15, 15), 0) # loc nhieu
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = auto_canny(gray)
	# edged = cv2.Canny(gray, 20, 250)

	thres = cv2.getTrackbarPos('thres',title_window)
	lin = cv2.getTrackbarPos('lin',title_window)
	minlen = cv2.getTrackbarPos('minlen',title_window)
	maxgap = cv2.getTrackbarPos('maxgap',title_window)
	lines = cv2.HoughLinesP(edged, 1, np.pi/180, thres, lin, minlen, maxgap)

	print(len(lines))
	output = np.zeros(crop_img.shape, dtype=crop_img.dtype)
	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 1)
	print("time eslaped:", time()-start_time)
	cv2.imshow("asd", output)
	cv2.imshow("canny", edged)
	key = cv2.waitKey(1) & 0xff

	if key == ord('q'):
		break

cv2.destroyAllWindows()


