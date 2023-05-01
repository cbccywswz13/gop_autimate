
import os
import subprocess
import time
import psutil
import re
path=r"D:\\xyaz\\Microvirt\\Memu\\"

def open_simulator(simulator_index):
    "open simulator"

    command=path+"MEmu.exe MEmu_"+str(simulator_index)
    print(command)
    subprocess.Popen(command)

#def close_simulator(simulator_index):
#    command=path+"memuc stop -n MEmu_"+str(simulator_index)
#    print(command)
#    os.system(command)

def close_simulator(simulator_index):
    # 获取所有的 MEmu 进程
    processes = [p for p in psutil.process_iter() if "MEmu" in p.name()]

    # 关闭指定编号的模拟器
    for process in processes:
        cmdline = " ".join(process.cmdline())
        if re.search(r"\bMEmu_"+str(simulator_index)+r"\b",cmdline):
            process.kill()


if __name__=="__main__":
    close_simulator(17)
    #test
    #time.sleep(20)
    #qrq6545646