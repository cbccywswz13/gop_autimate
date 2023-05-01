import cv2
import pyautogui
import time
import os
import window_standardize

#蓝色home按钮
home_blue="images/home_blue.PNG"
room_21="images/room.PNG"
level="images/level_10m.PNG"
private_game="images/private_game.PNG"
game_start_button="images/game_start.PNG"
def get_xy(mg_model_path):
    """
    获得指定路径图片的坐标
    :param imag_model_path :用来检测的图片的路径
    :return :以元组的形式返回检测的区域的中心坐标
    """
    #将屏幕截图
    pyautogui.screenshot().save("./images/screenshot.png")
    #载入截图
    img=cv2.imread("./images/screenshot.png")

    #图像模板
    img_terminal=cv2.imread(mg_model_path)
    #读取模板的高度和宽度和通道
    height,width,channel=img_terminal.shape
    ###模式匹配###cv2自带的函数
    result=cv2.matchTemplate(img,img_terminal,cv2.TM_SQDIFF  )
    #解析出匹配区域的左上角坐标
    upper_left=cv2.minMaxLoc(result)[2]
    #匹配区域右下角坐标
    lower_right=(upper_left[0]+width,upper_left[1]+height)
    #计算中心区域坐标并返回
    avg=(int((upper_left[0]+lower_right[0])/2),int((upper_left[1]+lower_right[1])/2))
    #avg=(int(upper_left[0]+1),int(upper_left[1]+1))
    os.remove("./images/screenshot.png")
    return avg

def auto_click(var_avg):
    """
    接受一个元组函数，自动点击
    param :坐标元组
    return :None
    """
    pyautogui.click(var_avg[0],var_avg[1],button='left')
    time.sleep(1)


def routine(imag_model_path,name=None):
    avg=get_xy(imag_model_path)
    if(name):
        print(name)
    auto_click(avg)



if __name__=="__main__":
    #print("start")
    ##img=cv2.imread(r"D:\VsPython\PythonApplication3\stop_card.jpg")
    #img=cv2.imread(r"images\stop_card.jpg")
    #gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    ##cv2.imshow("input",img)
    #cv2.imshow("gray",gray)
    #cv2.imshow("hsv",hsv)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #routine("images\home_page.jpg","clicked homepage")
    window_standardize.init_GOP3()
    routine(home_blue)
    routine(room_21)
    routine(level)
    routine(private_game)
    routine(game_start_button)

    #while true:
        #bet 200k
