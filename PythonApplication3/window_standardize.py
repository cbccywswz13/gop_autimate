#将某个程序窗口设置为固定的大小分辨率 以匹配脚本的图片点击


import win32gui
import win32con


def match_windows(win_title):
    """
    查找指定窗口
    :param win_title: 窗口名称
    :return: 句柄列表
    """

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            win_text = win32gui.GetWindowText(hwnd)
            # 模糊匹配
            if win_text.find(win_title) > -1:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)  # 列出所有顶级窗口，并传递它们的指针给callback函数
    return hwnds


def win_active(win_title):
    """
    激活指定窗口
    :param win_title: 窗口名称
    :return:
    """
    assert win_title, "win_title不能为空！"
    hwnds = match_windows(win_title)
    if hwnds:
        win32gui.ShowWindow(hwnds[0], win32con.SW_SHOWNORMAL)  # SW_SHOWNORMAL 默认大小，SW_SHOWMAXIMIZED 最大化显示
        win32gui.SetForegroundWindow(hwnds[0])
        win32gui.SetActiveWindow(hwnds[0])

def init_GOP3():
    win_active("GOP3")
    hwnd=win32gui.FindWindow(None,"GOP3")
    win32gui.MoveWindow(hwnd,0,0,1440,900,True)


if __name__=="__main__":
#    hwnd = win32gui.GetForegroundWindow()
## 将当前窗口缩放至指定位置及大小
#    win32gui.MoveWindow(hwnd, 0, 0, 1440, 900, True)
#    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    win_active("GOP3")
    hwnd=win32gui.FindWindow(None,"GOP3")
    win32gui.MoveWindow(hwnd,0,0,1440,900,True)