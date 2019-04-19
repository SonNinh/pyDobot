import cv2
from time import sleep, time
from rect_regconition import detect_rects


class Rectangle(object):
    def __init__(self, location, orientation, velocity):
        self.location = location
        self.orientation = orientation
        self.velocity = velocity


def main():
    cap = cv2.VideoCapture(1)
    cap.set(3, 320)
    cap.set(4, 240)
    cap.set(5, 30)
    sleep(1)
    while True:
        start_time = time()

        frame = cap.read()[1]
        img = frame[frame.shape[0]//5:frame.shape[0]//5*4, 115:240]
        ls_of_rects = detect_rects(img)

        print("num of detected rect:", len(ls_of_rects))
        print("eslaped time:", time() - start_time) 

        color = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
        for rect in ls_of_rects:
            cv2.circle(img, rect[0], 2, color[0], thickness=1)
            cv2.putText(img,str(int(rect[1])), rect[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),1,cv2.LINE_AA)
        cv2.imshow('origin', img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()