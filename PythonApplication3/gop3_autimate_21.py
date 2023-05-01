import adb_operate as ao

import time

import pytesseract.pytesseract

import gop3_restart

from PIL import Image
import cv2
from strantegy_21_dict import strantegy_dict
from open_close_simulator import close_simulator,open_simulator
import logging



"""
1bet click

2 take_screen_shot 

3 analyse screen

    3.1 if hit_button exist:
        analyse number of dealer    
        position of dealer(612,165) area(30,58)
        
        analyse number of player
        position of player(610,475) area(30,62)
        


        3.1.1 stand_click

        3.1.2 hit_click

        analyse screen
        
    else 
        break
        bet click
"""


point_17="./images/point_17.png";
point_18="./images/point_18.png";
point_19="./images/point_19.png";
point_20="./images/point_20.png";
hit_button="./images/Hit_button.png";
stand_button="./images/Stand_button.png";
close_button="./images/Close_button.png";
close_button_2="./images/Close_button_2.png";
room_21="./images/room_21.png";
room_21_fenzy="./images/room_21_fenzy.png"
Yes_button="./images/Yes.png"
Sure_button="./images/Sure.png"
Exit_button="./images/Exit.png"
Team_sure_button="./images/team_sure_button.png"

level_10m="./images/level_10m.png";
level_100m="./images/level_100m.png";
level_250k="./images/level_250k.png";
level_25b="./images/level_25b.png";

private_room="./images/private_room.png";
game_start_button="./images/game_start_button.png";

double_bet_button="./images/double_bet_button.png";
hit_button="./images/hit_button.png";
stop_button="./images/stop_button.png";
split_cards_button="./images/split_cards_button.png";

bet_10k="./images/bet_size_10k.png";
bet_200k="./images/bet_size_200k.png";
bet_1m="./images/bet_size_1m.png";
bet_2m="./images/bet_size_2m.png";
bet_5m="./images/bet_size_5m.png";
bet_100m="./images/bet_size_100m.png";

def img_to_number(img):
    try:
        #number=pytesseract.image_to_string(img,config="-c tessedit_char_whitelist=0123456789  --psm 6")
        number=pytesseract.image_to_string(img,config=" --psm 6")
       # number=pytesseract.image_to_string(img,config="--oem 3 --psm 6 outputbase digits")
        result="".join(list(filter(str.isdigit,number)))
        return result
    except Exception as e:
        print("img_to_number")
        logging.debug(str(e))
        logging.debug(repr(e))
        return

def img_to_number2(img):
    try:
        number=pytesseract.image_to_string(img,config="-c tessedit_char_whitelist=0123456789  --psm 13")
        #number=pytesseract.image_to_string(img,config=" --psm 6")
       # number=pytesseract.image_to_string(img,config="--oem 3 --psm 6 outputbase digits")
        result="".join(list(filter(str.isdigit,number)))
        return result
    except Exception as e:
        print("img_to_number2")

        logging.debug(str(e))
        logging.debug(repr(e))
        return





def analyse_screen(device_name=None):
    """
    screen:png path
    screen_img:Image 
    """
    screen_path=ao.take_screenshot(device_name)
    screen=cv2.imread(screen_path)
    if(ao.image_exist_check(hit_button,screen)):

        screen_img=Image.open(screen_path)
        player_hand=screen_img.crop((614,476,666,504))
        player_number=img_to_number(player_hand)
        print("player_number:"+player_number)

        if player_number==""or player_number=="49":
            #playerhand=screen_img.crop((627,476,651,504))
            #player_number=img_to_number2(player_hand)
            #print("player_number2:"+"undetected")
            player_number="9"#pytesseract 无法识别9和717 统一为9

        dealer_hand=screen_img.crop((614,165,666,195))
        dealer_number=img_to_number(dealer_hand)
        if dealer_number=="":
            dealer_hand=screen_img.crop((629,165,651,195))
            dealer_number=img_to_number2(dealer_hand)
            #print("dealer_number2:"+dealer_number)
        if dealer_number=="19":
            dealer_number="9"
        if dealer_number=="":
            dealer_number="11"
        print("dealer_number:"+dealer_number)

        #print("dealer:"+dealer_number+"player:"+player_number)
        try:
            return strantegy_dict[player_number][dealer_number]#"H" "S" "D"
        
        except Exception as e :
            print("analyse_screen")
            logging.debug(str(e))
            logging.debug(repr(e))
            return "S"
    else:
        #print("hit_button_not_exist")
        return "S"



def click_based_on_decision(decision=None,device_name=None):
    try:
        if decision=="S":
            ao.template_click(stop_button,device_name)
        elif decision=="D":
            #print("D")
            ao.template_click(double_bet_button,device_name,max_similarity=0.67)
            ao.template_click(hit_button,device_name,max_similarity=0.77)
            time.sleep(2)
            decision2=analyse_screen(device_name)
            #print("D decision:"+decision2)
            click_based_on_decision(decision2,device_name)

        elif decision=="H":
            #print("H")
            ao.template_click(hit_button,device_name)
            time.sleep(2)
            decision2=analyse_screen(device_name)
            #print("H decision:"+decision2)

            click_based_on_decision(decision2,device_name)

        elif decision=="P":
            ao.template_click(split_cards_button,device_name,max_similarity=0.7)
            time.sleep(2)
            ao.template_click(stop_button,device_name)
            time.sleep(1)
            ao.template_click(stop_button,device_name)
        else:
            ao.template_click(stop_button,device_name)
    except Exception as e:
        print("click_based_on_decision error:")
        logging.debug(str(e))
        logging.debug(repr(e))
        return






def restart(level_room,bet_size,device_name=None,if_first=True):
    if if_first:
        logging.basicConfig(filename="./images/info %s log.log"%(device_name.replace(":","")),level=logging.DEBUG)

    if not if_first:
        gop3_restart.gop3_stop(device_name)
        time.sleep(3)
        gop3_restart.gop3_start(device_name)
        time.sleep(70)
        #ao.template_click(Yes_button,device_name)
        #time.sleep(3)
        #ao.template_click(Yes_button,device_name)
        #time.sleep(20)

    """
    进入某个21点的房间
    """
    ao.template_click(Sure_button,device_name)
    time.sleep(1)
    ao.template_click(close_button,device_name)
    time.sleep(1)
    ao.template_click(close_button_2,device_name)
    time.sleep(1)
    ao.template_click(Team_sure_button,device_name)
    time.sleep(1)
    ao.template_click(close_button_2,device_name)
    time.sleep(1)
    ao.template_click(close_button,device_name)
    time.sleep(1)
    #ao.template_click(Exit_button,device_name)
    #time.sleep(4)
    ao.template_click(room_21,device_name)
    time.sleep(1)
    ao.template_click(room_21_fenzy,device_name)
    time.sleep(1)
    if level_room=="250k":
        ao.template_click(level_250k,device_name)
    elif level_room=="10m":
        ao.template_click(level_10m,device_name)
    elif level_room=="20m":
        ao.template_click(level_100m,device_name)
    elif level_room=="50m":
        ao.template_click(level_100m,device_name)
    elif level_room=="100m":
        ao.template_click(level_100m,device_name)
    elif level_room=="25b":
        ao.template_click(level_25b,device_name)
    else:
        ao.template_click(level_250k,device_name)
    time.sleep(6)
    ao.template_click(private_room,device_name)
    time.sleep(1)
    ao.template_click(game_start_button,device_name)

    play_game(level_room,bet_size,device_name)

    return


def bonus_click(device_name):
    ao.adb_click((3,3),device_name=device_name)
    time.sleep(1)
    ao.adb_click((40,680),device_name=device_name)
    time.sleep(1)
    ao.adb_click((40,680),device_name=device_name)




def team_points_bonus_click(device_name):
    """
    队伍积分的奖励
    """

    ao.adb_click((900,2),device_name=device_name)#队伍图标的位置
    time.sleep(2)
    ao.adb_click((500,21),device_name=device_name)#奖励的位置
    time.sleep(2)
    ao.adb_click((500,21),device_name=device_name)#奖励的位置
    time.sleep(2)
    for i in range(7):
        ao.adb_click((900,360),device_name=device_name)#奖励确定的位置
        time.sleep(2)


def play_game(level_room,bet_size,device_name=None):
    restart_count=0
    games_of_limit=0 #每个mission的局数限制

    #bonus_count=0#双倍经验时间计数
    bonus_click(device_name)
    while True:
        try:
            time.sleep(1)
            if(ao.template_click(bet_size,device_name,max_similarity=0.75)):
                time.sleep(4)
                decision=analyse_screen(device_name)
                #print("decision:"+decision)

                click_based_on_decision(decision,device_name)
                restart_count=0
                #bonus_count+=1
                ao.adb_click((666,404),device_name=device_name)
                games_of_limit+=1
                if games_of_limit>=105:
                    team_points_bonus_click(device_name)
                    break
                #if bonus_count>=50:
                #    bonus_click(device_name)
                #    bonus_count=0

            else:
                ao.template_click(close_button,device_name,0.7)
                #ao.template_click(close_button_2,device_name,0.75)
                ao.adb_click((666,404),device_name=device_name)
                restart_count+=1
                if restart_count>=6:
                    break
        except :
            break

    if games_of_limit<2 and ao.get_device_state(device_name):
         
        restart(level_room,bet_size,device_name=device_name,if_first=False)



def accomplish_mission(index):

    open_simulator(index)
    time.sleep(60)

    level="100m"
    bet_size=bet_5m
    device_index=503+index*10

    device_name="127.0.0.1:21"+str(device_index)
    restart(level,bet_size,device_name,if_first=False)

    close_simulator(index)
    time.sleep(2)



if __name__=="__main__":

    lis=input("输入需要的序列1/23456")
    ls=[]
    if lis=="1":
        ls=[3,5,6,7,8,9,11,12,13,0,1]

    elif lis=="2":
        ls=[23,19,20,21,22,24,25,14,15,17,18]

    elif lis=="3":
        ls=[]

    elif lis=="4":
        ls=[8,9,11,12,13,0,7]
    elif lis=="5":
        ls=[5,6,24,25,14,1,3,15]
    elif lis=="6":
        ls=[23,21,22,17,18,19,20]
    else:
        ls=[1]
    while True:

        #for i in [18,0,3,6,8,10,12,14,16,]:
        #for i in [17,1,5,7,9,11,13,15]:
        for i in ls:
            accomplish_mission(i)











    #level=input("输入级别/250k/10m/20m/50m/100m/25b")
    #if level=="250k":
    #    bet_size=bet_10k
    #elif level=="10m":
    #    bet_size=bet_200k
    #elif level=="20m":
    #    bet_size=bet_1m
    #elif level=="50m":
    #    bet_size=bet_2m
    #elif level=="100m":
    #    bet_size=bet_5m
    #elif level=="25b":
    #    bet_size=bet_100m
    #else:
    #    bet_size=bet_10k

    #device_name=input("输入设备名称")
    #device_name="127.0.0.1:21"+device_name

    #restart(level,bet_size,device_name,if_first=True)
