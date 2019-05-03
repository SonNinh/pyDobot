import cv2
from time import sleep
import sys


def main():
    cap = cv2.VideoCapture(int(sys.argv[1]))
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(5, 30)
    sleep(1)
    while(True):
        frame = cap.read()[1]
        # crop_img = frame[:, 115:240]

        # cv2.imshow('edges', crop_img)
        cv2.imshow('origin', frame)
        # cv2.imshow('res', hsv)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord("c"):
            cv2.imwrite(sys.argv[2], frame)


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()