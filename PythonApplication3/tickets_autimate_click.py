"""
自动开启每个账号里的每个ticket

"""

from open_close_simulator import close_simulator,open_simulator

import gop3_restart
close_button="./images/Close_button.png";
close_button_2="./images/Close_button_2.png";
Sure_button="./images/Sure.png"

import adb_operate as ao
import time

def accomplish_mission(index):

    open_simulator(index)
    time.sleep(60)
    device_index=503+index*10

    device_name="127.0.0.1:21"+str(device_index)

    gop3_restart.gop3_stop(device_name)
    time.sleep(3)
    gop3_restart.gop3_start(device_name)
    time.sleep(70)

    ao.template_click(Sure_button,device_name)
    time.sleep(1)
    ao.template_click(close_button,device_name)
    time.sleep(1)
    ao.template_click(close_button_2,device_name)
    time.sleep(1)

    ao.adb_click((640,700),device_name=device_name)
    time.sleep(1)
    ao.adb_click((640,690),device_name=device_name)
    time.sleep(2)
    ao.adb_click((640,350),device_name=device_name)
    time.sleep(1)
    ao.adb_click((640,250),device_name=device_name)
    time.sleep(1)
    ao.adb_click((640,200),device_name=device_name)


    close_simulator(index)



if __name__=="__main__":
    device_name="127.0.0.1:21503"
#    ao.adb_click((900,2),device_name=device_name)#队伍图标的位置
