#coding:utf-8
# 查找窗口并点击
# 定时截图
import win32gui
import win32process
import win32con
import win32api
import pygetwindow as gw
import time
import random
import subprocess


def grabScreen():
    grabcmd = "ffmpeg -f gdigrab -s 900x900 -offset_x 100 -offset_y 100 -i desktop -frames:v 1 imgs/{}.png".format(time.ctime().replace(":","-").replace(" ","_"))
    result = subprocess.run(grabcmd, check=True, capture_output = True,text =True)
    print(result.stdout)


# 点击屏幕位置
# leftclik : 是否左键点击该位置
def clickPose(pose,leftclik=False):
    click_x,click_y = pose
    # 将鼠标移动到指定位置
    win32api.SetCursorPos((click_x, click_y))

    if leftclik:
        # 模拟鼠标左键按下
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # 模拟鼠标左键释放
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 激活窗口
def ActivateWindowByHwnd(hid):
    print("activate ")
    tid, procid = win32process.GetWindowThreadProcessId(hid)
    print(tid, procid)
    win32gui.SetForegroundWindow(hid)
    print("done")
    
    # 先置底再置顶
    win32gui.SetWindowPos(hid, win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(hid, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    #win32gui.SetWindowPos(hid, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)




def autorun():
    window_title = "轻速云培训考试平台" # 替换成你要查找的窗口标题
    hwnd = win32gui.FindWindow(None, window_title)
    
    if hwnd:
        print(f"找到窗口，句柄为: {hwnd}")
        window_text = win32gui.GetWindowText(hwnd)
        print(f"窗口标题: {window_text}")
    
        ActivateWindowByHwnd(hwnd)
    
        print(win32api.GetCursorPos())
    
        # 播放按钮位置
        #playBUttonPose = (498,785)
        #clickPose(playBUttonPose)
    
        # click random pose 
        if 1:
            for i in range(60*300):
                dx = random.randint(-30,30)
                playBUttonPose = (498+dx,835)
                clickPose(playBUttonPose)
                time.sleep(5)
                ActivateWindowByHwnd(hwnd)
                if i%12==0:
                    grabScreen()
    
    else:
        print(f"未找到标题为 '{window_title}' 的窗口")



#window = gw.getWindowsWithTitle(window_title)[0]
#print(window)
#dir(window)
#window.setAlwaysOnTop(True)
#window.activate()
try:
    autorun()
except Exception as e:
    print("error : {}".format(e))
