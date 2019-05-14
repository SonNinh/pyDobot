import cv2
from time import sleep, time
from rect_regconition import detect_rects, get_distance_p2p
import threading
import DobotDllType as dType

# khoang cach gioi han nho nhat giua 2 vat the
ref_new = 10
# khoang cach tu tam camera den truc x cua robot
d_robot_cam = 332
# toc do bang tai (mm/s)
mm_per_sec = 40
# flag dieu khien ket thuc thread 'arm'
end_thread =False
# list cac vat the dang duoc theo doi
ls_obj = []


class Rectangle(object):
    '''
    moi vat the duoc dinh nghia bang 1 object Rectangle
    '''
    def __init__(self, location, orientation, color):
        self.location = location
        self.orientation = orientation
        self.color = color


def is_new_obj(rect_center, ls_obj):
    '''
    Kiem tra xem vat the o khung hinh hien tai va vat the o khung hinh truoc do 
    co phai la 1 vat the khong.
    Kiem tra toi da 6 vat the
    '''

    if len(ls_obj) > 6:
        start_idx = -6
    else:
        start_idx = -len(ls_obj)

    for idx in range(start_idx, 0, 1):
        dist = get_distance_p2p(ls_obj[idx].location, rect_center)
        # neu khoang cach tu vat the dang xet tai khung hinh hien tai den 6 vat the o khung hinh truoc do nho hon ref_new ko?
        if dist < ref_new:
            return False
    return True


def get_real_pos(img_pos, img_shape, delta_s):
    '''
    Chuyen doi tu toa do vat the tren anh sang toa do robot.
    Ty le chuyen doi: 25 pixel ~ 30 mmm
    '''
    return [(img_pos[0]-img_shape[1]/2)*25/30, (img_pos[1]-img_shape[0]/2)*25/31 + delta_s]


def convert_base(ls_of_rects, img_shape, delta_s):
    '''
    Chuyen doi toa do danh sach vat the tren anh sang toa do robot.
    '''
    for rect in ls_of_rects:
        rect[0] = get_real_pos(rect[0], img_shape, delta_s)


def get_color_center():
    '''
    tinh sample color cua 4 mau
    '''
    color_ls = ['red', 'green', 'blue', 'yellow', 'black']
    color_center = []
    for color in color_ls:
        img = cv2.imread('photos/'+color+'.png')
        # tinh gia tri trung binh cua cac diem anh tren 3 thang mau RGB        
        p = img.mean(axis=0).mean(axis=0).astype(int)
        # chuyen doi tu dinh dang numpy sang dinh dang list
        color_center.append(list(p))

    return color_center


def main(threadname):
    # mo camera so 0
    cap = cv2.VideoCapture(0)
    # setup ty le khung hinh
    cap.set(3, 320)
    cap.set(4, 240)
    # setup FPS
    cap.set(5, 30)
    sleep(1)

    last_time = 0
    timef2f = 0

    # tinh sample color cua 5 mau
    color_center = get_color_center()
    
    while True:
        
        start_time = time()

        # doc 1 anh tu camera
        frame = cap.read()[1]

        # cat khung hinh lay phan chua bang bang chuyen
        img = frame[frame.shape[0]//3:frame.shape[0]//3*2, 98:-98]

        # tim tat ca hinh vuong trong img
        # ls_of_rects = [   [[x, y], orientation, color]   , [], ...]
        ls_of_rects = detect_rects(img, color_center)
        
        # calculate time spent by rect_regconition
        # print("num of detected rect:", len(ls_of_rects))
        # print("eslaped time:", time() - start_time)

        # show rect_regconition results
        color = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
        for rect in ls_of_rects:
            cv2.circle(img, rect[0], 2, color[0], thickness=1)
            cv2.putText(img,str(int(rect[2])), rect[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),1,cv2.LINE_AA)
        cv2.circle(img, (img.shape[1]//2, img.shape[0]//2), 2, color[2], thickness=1)
        cv2.imshow('origin', img)

        # convert coordinate base from image base to robot base 
        delta_s = (time()-start_time) * mm_per_sec
        # print('time1:', time()-start_time)
        convert_base(ls_of_rects, img.shape, delta_s)

        # khai bao ls_obj la global de co the sua doi du lieu
        global ls_obj

        # can chinh lai toa do cac vat the
        delta_s = (time()-last_time) * mm_per_sec
        # print('delta:', delta_s)

        last_time = time()
        for obj in ls_obj:
            obj.location[1] += delta_s

        # cap nhat danh sach cac vat the ls_obj
        for rect in ls_of_rects:
            if is_new_obj(rect[0], ls_obj):
                end_idx = -len(ls_obj)-1
                if end_idx < -7:
                    end_idx = -7
                inserted_flag = False
                for i in range(-1, end_idx, -1):
                    if rect[0][1] <= ls_obj[i].location[1]:
                        if i == -1:
                            ls_obj.append(Rectangle(rect[0], rect[1], rect[2]))
                        else:
                            ls_obj.insert(i, Rectangle(rect[0], rect[1], rect[2]))
                        inserted_flag = True
                        break
                if not inserted_flag:
                    ls_obj.insert(end_idx+1, Rectangle(rect[0], rect[1], rect[2]))
        

        if cv2.waitKey(1) & 0xFF == 27:
            global end_thread
            end_thread = True
            break

    cv2.destroyAllWindows()


def pick_up(api, location, orientation, color, cur_pos_wh, size_wh):
    # vi tri goc cua kho
    warehouse_base = [-88, 198, -42]

    # dieu khien arm den vi tri x, y, z
    x = location[0] + 217
    y = d_robot_cam - location[1]
    z = 12
    print(x,y,z)
    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                    x, y, z, 0, isQueued=1)

    dType.SetEndEffectorSuctionCup(api, 1,  1, isQueued=1)

    # dieu khien arm den vi tri trong trong kho chua
    x = cur_pos_wh[color][0]*35 + warehouse_base[0] + 40*color
    y = cur_pos_wh[color][1]*35 + warehouse_base[1]
    z = cur_pos_wh[color][2]*26 + warehouse_base[2]
    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                    x, y, z, orientation, isQueued=1)[0]
    dType.SetEndEffectorSuctionCup(api, 1,  0, isQueued=1)

    # luu chi so cua lenh cuoi cung
    lastIndex = dType.SetWAITCmd(api, 0.2, isQueued=1)[0]
    
    # cap nhat tri trong trong kho chua
    if cur_pos_wh[color][0] == size_wh[0]-1:
        cur_pos_wh[color][0] = 0
        if cur_pos_wh[color][1] == size_wh[1]-1:
            cur_pos_wh[color][1] = 0
            # if cur_pos_wh[color][2] < size_wh[2]-1:
            cur_pos_wh[color][2] += 1
        else:
            cur_pos_wh[color][1] += 1
    else:
        cur_pos_wh[color][0] += 1

    # doi robot thuc hien xong qua trinh, sau do ket thuc
    cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]
    while lastIndex > cur_cmd:
        # print(cur_cmd)
        dType.dSleep(10)
        cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]


def arm(threadname):
    '''
    Thread dieu khien robot arm
    '''

    # kich thuoc kho chua hang doi voi tung mau. Dinh dang [x, y, z]
    size_wh = [1, 3, 4]

    # vi tri hien tai cua tung mau trong kho hang. Red Green Blue Yellow
    cur_pos_wh = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    #Load Dll
    api = dType.load()

    #Connect Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    # dType.SetHOMEParams(api, 200, 0, 50, 0, isQueued=1)
    dType.SetPTPCoordinateParams(api, 150, 200, 200, 200, isQueued=1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued=1)
    dType.SetPTPJumpParams(api, 60, 150, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                    200, 0, 50, 0, isQueued=1)
    lastIndex = dType.SetHOMECmd(api, temp = 0, isQueued = 1)[0]

    cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]
    while lastIndex > cur_cmd:
        dType.dSleep(10)
        cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]

    global mm_per_sec

    dType.SetQueuedCmdClear(api)
    dType.SetQueuedCmdStartExec(api)

    f = open('step', 'r')
    STEP_PER_CIRCLE = float(f.read().strip('\n'))
    f.close()
    # so buoc de truc quay du 1 vong
    # STEP_PER_CIRCLE = 17400 #16625 
    # chu vi truc quay bang chuyen
    MM_PER_CIRCLE = 3.1415926535898 * 36.0
    # so buoc trong 1 giay
    pulse_per_sec = mm_per_sec * STEP_PER_CIRCLE / MM_PER_CIRCLE
    # dieu khien stepper
    dType.SetEMotor(api, 0, 1, int(pulse_per_sec), isQueued=1)

    
    while state == dType.DobotConnect.DobotConnect_NoError:
        # print('number:', len(ls_obj))
        if ls_obj:
            # print("ab")
            if ls_obj[0].location[1] >= d_robot_cam-20:
                while True:
                    try: 
                        if ls_obj[0].location[1] >= d_robot_cam-100:
                            print(cur_pos_wh)
                            # neu kho hang cua mau dang xet chua day
                            if cur_pos_wh[ls_obj[0].color][2] < size_wh[2]:
                                # dung bang chuyen
                                dType.SetEMotor(api, 0, 1, int(0), isQueued=1)
                                mm_per_sec = 0
                                # gap vat the tu bang chuyen vao kho
                                pick_up(api, ls_obj[0].location, ls_obj[0].orientation, ls_obj[0].color, cur_pos_wh, size_wh)

                            # xoa vat the vua gap
                            ls_obj.pop(0)
                        else:
                            break
                    except Exception:
                        break
                
                # bang chuyen tiep tuc chay
        f = open('step', 'r')
        STEP_PER_CIRCLE = float(f.read().strip('\n'))
        f.close()

        # # chu vi truc quay bang chuyen
        MM_PER_CIRCLE = 3.1415926535898 * 36.0
        # # so buoc trong 1 giay
        mm_per_sec = 40
        pulse_per_sec = mm_per_sec * STEP_PER_CIRCLE / MM_PER_CIRCLE
        dType.SetEMotor(api, 0, 1, int(pulse_per_sec), isQueued=1)
                

        if end_thread:
            dType.SetEMotor(api, 0, 1, 0, isQueued=1)
            print('End process')
            dType.DisconnectDobot(api)
            break


if __name__ == '__main__':
    thread_main = threading.Thread(target=main, args=('Thread-1', ))
    thread_main.start()

    thread_arm = threading.Thread(target=arm, args=('Thread-2', ))
    thread_arm.start()