import cv2
from time import sleep, time
from rect_regconition import detect_rects, get_distance_p2p
import threading
import DobotDllType as dType


ref_new = 10
command = None


class Rectangle(object):
    def __init__(self, location, orientation):
        self.location = location
        self.orientation = orientation


def is_new_obj(rect_center, ls_obj):
    if len(ls_obj) > 6:
        start_idx = -6
    else:
        start_idx = -len(ls_obj)

    for idx in range(start_idx, 0, 1):
        dist = get_distance_p2p(ls_obj[idx].location, rect_center)
        print("distance:", dist)
        if dist < ref_new:
            
            return False
    return True


def get_real_pos(img_pos, img_shape, delta_s):
    return [(img_pos[0]-img_shape[1]/2)*25/30, (img_pos[1]-img_shape[0]/2)*25/30 + delta_s]


def convert_base(ls_of_rects, img_shape, delta_s):
    for rect in ls_of_rects:
        rect[0] = get_real_pos(rect[0], img_shape, delta_s)


def main(threadname):
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    cap.set(5, 30)
    sleep(1)

    ls_obj = []
    last_time = 0
    timef2f = 0

    while True:
        
        start_time = time()

        frame = cap.read()[1]
        img = frame[frame.shape[0]//5:frame.shape[0]//5*4, 98:-98]
        ls_of_rects = detect_rects(img)

        # calculate time spent by rect_regconition 
        # print("num of detected rect:", len(ls_of_rects))
        # print("eslaped time:", time() - start_time)

        # show rect_regconition results
        color = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
        for rect in ls_of_rects:
            cv2.circle(img, rect[0], 2, color[0], thickness=1)
            cv2.putText(img,str(int(rect[1])), rect[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),1,cv2.LINE_AA)
        cv2.circle(img, (img.shape[1]//2, img.shape[0]//2), 2, color[2], thickness=1)
        cv2.imshow('origin', img)

        # convert coordinate base from image base to real base
        delta_s = (time()-start_time) * 20
        convert_base(ls_of_rects, img.shape, delta_s)

        delta_s = (time()-last_time) * 20
        last_time = time()
        for obj in ls_obj:
            obj.location[1] += delta_s

        for rect in ls_of_rects:
            if is_new_obj(rect[0], ls_obj):
                end_idx = -len(ls_obj)-1
                if end_idx < -7:
                    end_idx = -7
                inserted_flag = False
                for i in range(-1, end_idx, -1):
                    if rect[0][1] <= ls_obj[i].location[1]:
                        if i == -1:
                            ls_obj.append(Rectangle(rect[0], rect[1]))
                        else:
                            ls_obj.insert(i, Rectangle(rect[0], rect[1]))
                        inserted_flag = True
                        break
                if not inserted_flag:
                    ls_obj.insert(end_idx+1, Rectangle(rect[0], rect[1]))
        global command
        if ls_obj:
            if ls_obj[0].location[1] >= 317:
                command = 1
        print(len(ls_obj)) 

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def arm(threadname):
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    #Load Dll
    api = dType.load()

    #Connect Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    if state == dType.DobotConnect.DobotConnect_NoError:
        global command
        dType.SetQueuedCmdClear(api)
        dType.SetQueuedCmdStartExec(api)
        STEP_PER_CIRCLE = 17400 #16625 
        MM_PER_CIRCLE = 3.1415926535898 * 36.0
        vel = 20 * STEP_PER_CIRCLE / MM_PER_CIRCLE
        # s = int(input())*vel
        dType.SetEMotor(api, 0, 1, int(vel), isQueued=1)
        # dType.SetEMotorSEx(api, 0, 1, int(vel), int(s), isQueued=1)
        while command is None:
            continue
        command = None
        dType.SetEMotor(api, 0, 1, int(0), isQueued=1)
            

    dType.DisconnectDobot(api)


if __name__ == '__main__':
    thread_main = threading.Thread(target=main, args=('Thread-1', ))
    thread_main.start()

    thread_arm = threading.Thread(target=arm, args=('Thread-2', ))
    thread_arm.start()
