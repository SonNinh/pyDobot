import time
from glob import glob

import dobot
import message


available_ports = glob('/dev/ttyUSB*')  # mask for OSX Dobot port
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
print("end")
# print(device.go_home())
time.sleep(1)
print(device.go(250.0, 50.0, 80.0))
print(device.set_conveyor(1, 0, 0))

# print("end")
# print(device._get_pose())
# print('adfgd')
# time.sleep(2)
device.close()
