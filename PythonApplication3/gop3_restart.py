


"""
gop3在无法下注的时间长达2分钟时，重启游戏


start:adb -s "device_name" shell am start -n com.youdagames.gop3multiplayer/com.google.firebase.MessagingUnityPlayerActivity

stop:adb -s "device_name" shell am force-stop  com.youdagames.gop3multiplayer

"""

import os
import time

def gop3_start(device_name=None):
    try:

        if not device_name:
            os.system("adb shell am start -n com.youdagames.gop3multiplayer/com.google.firebase.MessagingUnityPlayerActivity")
        else:
            os.system("adb -s %s shell am start -n com.youdagames.gop3multiplayer/com.google.firebase.MessagingUnityPlayerActivity"%(device_name))
    except :
        print("gop3_start_exception:")

def gop3_stop(device_name=None):
    try:
        if not device_name:
            os.system("adb  shell am force-stop  com.youdagames.gop3multiplayer")
        else:
            os.system("adb -s %s  shell am force-stop  com.youdagames.gop3multiplayer" %(device_name))
    except :
        print("gop3_stop_exeption:")



if __name__=="__main__":
    gop3_stop("127.0.0.1:21523")
    time.sleep(10)
    gop3_start("127.0.0.1:21523")
