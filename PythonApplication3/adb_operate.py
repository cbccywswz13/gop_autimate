import os
import cv2
import random
import time
import subprocess


def take_screenshot(device_name=None):
    """
    将手机里的屏幕截图保存到电脑
    device_name:设备名称
    """
    if not device_name:
        os.system("adb shell screencap -p /data/screenshot.png")
        os.system("adb pull /data/screenshot.png ./images/temp.png")
        return "./images/temp.png"
    else:
        os.system("adb -s %s shell  screencap -p /data/screenshot%s.png"%(device_name,device_name.replace(":","")))
        os.system("adb -s %s pull /data/screenshot%s.png  ./images/temp%s.png"%(device_name,device_name.replace(":",""),device_name.replace(":","")))
        return "./images/temp%s.png"%(device_name.replace(":",""))

def adb_click(center,offset=(0,0),device_name=None):
    """
    center:点击图像的中心
    offset:偏移量
    """
    (x,y)=center
    x+=offset[0]
    y+=offset[1]
    if not device_name:
        os.system("adb shell input tap %s %s"%(x,y))
    else:
        os.system("adb -s %s shell input tap %s %s"%(device_name,x,y))


def get_device_state(device_id=None):
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.append("get-state")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    if error:
        return None
    return output.decode().strip()



def adb_input_text(text,device_name=None):
    "输入文字"
    if not device_name:
        os.system("adb shell input text %s"%text)
    else:
        os.system("adb -s %s shell input text %s"%(str(device_name),text))


"""
查询当前运行的程序的Activity
adb shell dumpsys activity activities 

停止某个应用
adb shell am force-stop (name of the activitiy)

开启某个应用需要提供包名以及Activity
adb shell am start -W -n tw.sonet.princessconnect/jp.co.cygames.activity.OverrideUnityActivity 
"""

def image_to_position(template_path,device_name=None,max_similarity=0.78):
    """
    screen:屏幕截图 png文件
    template:匹配图片 png文件
    """
    screen=cv2.imread(take_screenshot(device_name))
    template=cv2.imread(template_path)
    image_x,image_y=template.shape[:2]#匹配图片大小
    result=cv2.matchTemplate(screen,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  
    #最小匹配度 最大匹配度 最小匹配位置  最大匹配位置
    print("max_val:"+str(max_val))
    if max_val>max_similarity:
        global center
        center=(max_loc[0]+image_y/2,max_loc[1]+image_x/2)
        return center
    else:
        return False

def image_exist_check(template_path,screen):
    template=cv2.imread(template_path)
    result=cv2.matchTemplate(screen,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  
    print("maxval:"+str(max_val))
    if max_val>0.78:
        return True
    else :
        return False


def hit_or_stand(device_name=None):
    screen=cv2.imread(take_screenshot(device_name))
    if  image_exist_check(point_17,screen) or image_exist_check(point_18,screen) or image_exist_check(point_19,screen)or image_exist_check(point_20,screen):
        #stand
        template_click(stand_button,device_name)
        #return True
    else :
        #hit
        template_click(hit_button,device_name)
        time.sleep(2)
        template_click(stand_button,device_name)
        #hit_or_stand(device_name)




def template_click(template_path,device_name,max_similarity=0.78):
    center=image_to_position(template_path,device_name,max_similarity)
    if center:
        adb_click(center,(random.randint(-4,4),random.randint(-4,4)),device_name)
        return True
    else:
        #print("not found"+str(template_path))
        return False




if __name__=="__main__":


    
    device_id="127.0.0.1:21583";
    k=get_device_state(device_id)
    print(k)
    #device_name="127.0.0.1:21503"
    #adb_click((900,2),device_name=device_name)
    #adb_click((500,20),device_name=device_name)
    #adb_click((900,360),device_name=device_name)
    #is_device_online(device_name)
    #if not os.path.exists("./images"):
    #    os.mkdir("./images")
    #level=input("输入级别/10k/25k/50k/100k/200k/")
    #if level=="10k":
    #    level="./images/bet_size_10k.png"
    #elif level=="25k":
    #    level="./images/bet_size_25k.png"
    #elif level=="50k":
    #    level="./images/bet_size_50k.png"
    #elif level=="100k":
    #    level="./images/bet_size_100k.png"
    #elif level=="200k":
    #    level="./images/bet_size_200k.png"
    #else:
    #    level="./images/bet_size_10k.png"
    ####级别输入###

    #device_name=input("输入设备名称")
    ####设备名称###


    #while True:
    #    time.sleep(1)
    #    if template_click(level,device_name):
    #        time.sleep(3)
    #        hit_or_stand(device_name)
    #        #template_click(stand_button,device_name)



