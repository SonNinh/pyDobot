import cv2
from time import sleep, time
from rect_regconition import detect_rects, get_distance_p2p
import threading
import DobotDllType as dType


ref_new = 10
d_robot_cam = 315
mm_per_sec = 50
command = None
end_thread =False
ls_obj = []


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
        # print("distance:", dist)
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

    last_time = 0
    timef2f = 0

    while True:
        
        start_time = time()

        frame = cap.read()[1]
        img = frame[frame.shape[0]//3:frame.shape[0]//3*2, 98:-98]
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
        delta_s = (time()-start_time) * mm_per_sec
        convert_base(ls_of_rects, img.shape, delta_s)

        global ls_obj

        delta_s = (time()-last_time) * mm_per_sec
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
        
        # print(len(ls_obj)) 

        if cv2.waitKey(1) & 0xFF == 27:
            global end_thread
            end_thread = True
            break

    cv2.destroyAllWindows()


def pick_up(api, location, orientation, cur_pos_wh):
    warehouse_base = [-88, 198, -38]

    x = location[0] + 189
    y = d_robot_cam - location[1]
    z = 12
    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                    x, y, z, orientation, isQueued=1)

    dType.SetEndEffectorSuctionCup(api, 1,  1, isQueued=1)

    x = cur_pos_wh[0]*35 + warehouse_base[0]
    y = cur_pos_wh[1]*35 + warehouse_base[1]
    z = cur_pos_wh[2]*27 + warehouse_base[2]
    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                    x, y, z, 0, isQueued=1)[0]
    
    lastIndex = dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)[0]
    

    if cur_pos_wh[0] == 1:
        cur_pos_wh[0] = 0
        if cur_pos_wh[1] == 1:
            cur_pos_wh[1] = 0
            cur_pos_wh[2] += 1
        else:
            cur_pos_wh[1] += 1
    else:
        cur_pos_wh[0] += 1

    cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]
    while lastIndex > cur_cmd:
        # print(cur_cmd)
        dType.dSleep(10)
        cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]

    


def arm(threadname):
    size_wh = [3, 3]
    cur_pos_wh = [0, 0, 0]
    # size_wh = [[0, 0, 0],
    #            [0, 0, 0],
    #            [0, 0, 0]]

    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    #Load Dll
    api = dType.load()

    #Connect Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    # dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued=1)
    dType.SetPTPCoordinateParams(api, 150, 200, 200, 200, isQueued=1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued=1)
    dType.SetPTPJumpParams(api, 50, 150, isQueued=1)

    global command
    global mm_per_sec

    dType.SetQueuedCmdClear(api)
    dType.SetQueuedCmdStartExec(api)
    STEP_PER_CIRCLE = 17400 #16625 
    MM_PER_CIRCLE = 3.1415926535898 * 36.0
    pulse_per_sec = mm_per_sec * STEP_PER_CIRCLE / MM_PER_CIRCLE
    dType.SetEMotor(api, 0, 1, int(pulse_per_sec), isQueued=1)
    while state == dType.DobotConnect.DobotConnect_NoError:
        # print("a")
        if ls_obj:
            # print("ab")
            if ls_obj[0].location[1] >= d_robot_cam:
                # print("abc")
                mm_per_sec = 0
                dType.SetEMotor(api, 0, 1, int(0), isQueued=1)
                pick_up(api, ls_obj[0].location, ls_obj[0].orientation, cur_pos_wh)
                dType.SetEMotor(api, 0, 1, int(pulse_per_sec), isQueued=1)
                mm_per_sec = 50
                ls_obj.pop(0)
                print(len(ls_obj)) 
        if end_thread or cur_pos_wh[2] == 3:
            break
    print("end tread 9hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    dType.DisconnectDobot(api)


if __name__ == '__main__':
    thread_main = threading.Thread(target=main, args=('Thread-1', ))
    thread_main.start()

    thread_arm = threading.Thread(target=arm, args=('Thread-2', ))
    thread_arm.start()
