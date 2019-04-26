import threading
import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued0
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued=1)
    dType.SetPTPCoordinateParams(api, 150, 200, 200, 200, isQueued=1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued=1)
    dType.SetPTPJumpParams(api, 50, 100, isQueued=0)
    # dType.SetCPParams(api, 100, 100, 0, realTimeTrack = 0,  isQueued=1)

    #Async Home
    # dType.SetHOMECmd(api, temp = 0, isQueued = 1)
    print('start')
    # dType.SetWAITCmd(api, 2, isQueued=1)
    #Async PTP Motion
    dType.SetQueuedCmdStartExec(api)
    # while True:
    #     speed = int(input())
        
    #     # delta = int(input())
    #     # SetEMotorS
    #     STEP_PER_CIRCLE = 17400 #16625 
    #     MM_PER_CIRCLE = 3.1415926535898 * 36.0
    #     vel = speed * STEP_PER_CIRCLE / MM_PER_CIRCLE
    #     s = int(input())*vel
    #     # dType.SetEMotor(api, 0, 1, int(vel), isQueued=1)
    #     dType.SetEMotorSEx(api, 0, 1, int(vel), int(s), isQueued=1)

    # dType.SetWAITCmd(api, 1, isQueued=1)
    # lastIndex = dType.SetEMotor(api, 0, 1, 0,  isQueued=1)[0]
        
    # dType.dSleep(2000)
    for i in range(0, 5):
        print(dType.GetPTPJumpParams(api))
        if i % 2 == 0:
            offset = 20
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                                    230, 50, 50, 20, isQueued=1)[0]
        else:
            offset = -20
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode,
                                    -88, 198, -38, 20, isQueued=1)[0]
        # dType.SetWAITCmd(api, 1, isQueued=1)
        # print(lastIndex)

    # while True:
    #     print(dType.GetPose(api))
    #     dType.dSleep(500)

    # for i in range(0, 5):
    #     if i % 2 == 0:
    #         offset = 20
    #     else:
    #         offset = -20
    #     lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode,
    #                                 200 + offset, offset, offset, offset, isQueued=1)[0]
    #     print(lastIndex)
    #Start to Execute Command Queued
    
    # print('play:')

    # Wait for Executing Last Command
    cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]
    while lastIndex > cur_cmd:
        print(cur_cmd)
        dType.dSleep(500)
        cur_cmd = dType.GetQueuedCmdCurrentIndex(api)[0]

    # print(2)
    # Stop to Execute Command Queued
    # print(dType.GetPTPCoordinateParams(api))
    # dType.SetQueuedCmdStopExec(api)
#Disconnect Dobot
dType.DisconnectDobot(api)
