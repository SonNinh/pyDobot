import cv2
from time import sleep
import numpy as np


title_window = 'Linear Blend'
cv2.namedWindow(title_window)

def on_trackbar(val):
    pass

cv2.createTrackbar("Hmax", title_window , 0, 255, on_trackbar)
cv2.createTrackbar("Hmin", title_window , 0, 255, on_trackbar)
cv2.createTrackbar("Smax", title_window , 0, 255, on_trackbar)
cv2.createTrackbar("Smin", title_window , 0, 255, on_trackbar)
cv2.createTrackbar("Vmax", title_window , 0, 255, on_trackbar)
cv2.createTrackbar("Vmin", title_window , 0, 255, on_trackbar)


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    # # brightness
    cap.set(5, 30)
    # #contrast
    # cap.set(11, 255)
    # #saturation
    # cap.set(12, 122)
    # #gain
    # cap.set(14, 150)
    sleep(2)
    while(True):
        frame = cap.read()[1]
        width = frame.shape[1]
        crop_img = frame[:, 115:240]



        Hmax = cv2.getTrackbarPos('Hmax',title_window)
        Hmin = cv2.getTrackbarPos('Hmin',title_window)
        Smax = cv2.getTrackbarPos('Smax',title_window)
        Smin = cv2.getTrackbarPos('Smin',title_window)
        Vmax = cv2.getTrackbarPos('Vmax',title_window)
        Vmin = cv2.getTrackbarPos('Vmin',title_window)

        lower = [Hmin, Smin, Vmin]
        upper = [Hmax, Smax, Vmax]
        # lower = [6, 152, 138] # gioi han duoi mau lua trong he mau HSV
        # upper = [48, 248, 255]

        blur = cv2.GaussianBlur(crop_img, (21, 21), 0) # loc nhieu
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) # chuyen doi khong gian mau

        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(crop_img, crop_img, mask = mask)

        # blur = cv2.GaussianBlur(frame,(9,9),0)

        # hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        cv2.imshow(title_window, output)
        cv2.imshow('origin', frame)
        # cv2.imshow('res', hsv)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    