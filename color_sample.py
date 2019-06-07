import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

while True:
    # doc 1 anh tu camera
    frame = cap.read()[1]
    cv2.imshow("adad", frame)
    cv2.waitKey(10)

cv2.destroyAllWindows()