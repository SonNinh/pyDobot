import time
from glob import glob

import dobot
import message


def main():
    available_ports = glob('/dev/cu.SLAB*')  # mask for OSX Dobot port
    if len(available_ports) == 0:
        print('no port found for Dobot Magician')
        exit(1)

    device = dobot.Dobot(port=available_ports[0])

    time.sleep(0.5)
    # device.speed(100)
    # print(device.go(250.0, 0.0, 80.0))
    # print('hajs')
    # device.speed(100)
    # print(device.go(250.0, 0.0, 0.0))

    print("start")

    # device.set_home(250, 100, 50, 0)
    # print(device.go_home())
    while False:
        for i in range(80, 150, 10):
            print(device.set_conveyor(1, 1, i))
            time.sleep(2)
        break
        # print(device.go(260.8829040527344, -103.0121078491211, 12.091949462890625))
        # print(device.set_cupper(1, 1))
        # time.sleep(0.5)
        # print(device.go(260.11785888671875, 42.92505645751953, 90.23689270019531))

        # print(device.go(258.7375183105469, 168.59320068359375, 12.011768341064453))
        # time.sleep(0.5)
        # print(device.set_cupper(1, 0))
        # print(device.go(261.3182678222656, 16.561960220336914, 90.10472106933594))
        # time.sleep(0.5)

    while True:
        try:
            cmd = (input('enter command: ')).split()
            param = list(map(int, cmd[1:]))
            cmd = cmd[0]
            if cmd:
                if cmd == 'conveyor':
                    print(param[0])
                    print(device.set_conveyor(1, 0, param[0]))
                elif cmd == 'cupper':
                    print(device.set_cupper(1, param[0]))
                elif cmd == 'go_home':
                    print(device.go_home())
                elif cmd == 'set_home':
                    print(device.set_home(param[0], param[1], param[2], param[3]))
                elif cmd == 'get_home':
                    print(device.get_home())
                elif cmd == 'go':
                    print(device.go(param[0], param[1], param[2], param[3]))
                elif cmd == 'get_pose':
                    print(device.get_pose())
                elif cmd == 'setvelacc':
                    print(device.speed(param[0], param[1]))
                elif cmd == 'clear':
                    print(device.clear_alarm())
        except Exception as e:
            print(e)
        pass

    print('end')
    # print(device._get_pose())
    # print('adfgd')
    # time.sleep(2)
    device.close()


if __name__ == '__main__':
    main()
    

