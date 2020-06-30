# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-14 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    透明移动悬浮窗口, 图标文字 基于tkinter
    @依赖库： tkinter
"""
import time, threading, random
import tkinter
from PIL import Image, ImageTk


# 透明悬浮窗口
class myWinForm():
    def __init__(self, name = "", icoUrl = "", alpha = 0.2, randomHwnd = True, autoMove = True, typeMove = 0, range = [200,900,200,650]):  
        random.seed(a=None, version=2)
        self.name = name            #窗口名称
        self.icoUrl = icoUrl        #图标
        self.alpha = alpha          #窗口透明度
        self.alpha_now = alpha      #窗口透明度-当前
        self.randomHwnd = randomHwnd#随机窗口位置
        self.autoMove = autoMove    #自动移动
        self.typeMove = typeMove    #移动模式
        self.alive = False          #是否激活
        self.rangHwnd = range       #限定范围
        self.savePos = range        #记忆位置
        self.hitCode = 0            #命中码，简易密码组合以激活窗体
        self.moveX = 0; self.moveY = 0
        
        self.icoUrl = "D:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/Images/test/aa3.png"
        self._initForm()
        
    #随机窗口位置
    def _randomXY(self):
        self.x = random.randint(self.rangHwnd[0], self.rangHwnd[1])
        self.y = random.randint(self.rangHwnd[2], self.rangHwnd[3])
    #初始窗口
    def _initForm(self, x = 300, y = 300, w = 86, h = 86):
        #记录位置大小
        self.x = x;  self.y = y
        self.w = w; self.h = h
        if(self.randomHwnd): self._randomXY()

        #初始窗口
        self.hWnd = tkinter.Tk()
        self.hWnd.title(self.name)
        self.hWnd.geometry("%sx%s+%s+%s" % (self.w, self.h, self.x, self.y))
        self.hWnd.resizable(0, 0)                               # 设置窗口宽高固定
        self.hWnd.overrideredirect(True)                        # 去除边框
        self.hWnd["background"] = "white"                       # 窗口背景色设置为白色
        #self.hWnd.withdraw()

        #from tkinter import *
        #self.hWnd.wm_attributes("-transparentcolor", TRANSCOLOUR)
        self.hWnd.attributes("-transparentcolor", "#ffffff")      # 底色透明，实现异形
        self.hWnd.attributes("-alpha", self.alpha)   
        self.hWnd.wm_attributes('-topmost', 1)
        self.hWnd.bind("<Enter>", self._onFocusIn)
        self.hWnd.bind("<Button-1>", self._onClickButton_1)
        self.hWnd.bind("<Button-2>", self._onClickButton_2)
        self.hWnd.bind("<Button-3>", self._onClickButton_3)
        self.hWnd.bind("<ButtonRelease-1>", self._onReleaseButton_1)
        self.hWnd.bind("<B1-Motion>", self._onMotion)
        self.hWnd.bind("<Leave>", self._onFocusOut)

        #增加背景图片
        pilImage = Image.open(self.icoUrl)
        img = pilImage.resize((self.w, self.h), Image.ANTIALIAS)
        tkImage = ImageTk.PhotoImage(image=img)
        self.strLbText = tkinter.StringVar() 
        self.theLabel = tkinter.Label(self.hWnd, textvariable=self.strLbText, justify=tkinter.LEFT, image=tkImage, compound = tkinter.CENTER, font=("华文行楷",20), fg = "white")
        self.theLabel.pack()
        
        self._thrdSet_Alpha()
        self.hWnd.mainloop()
    #鼠标进入
    def _onFocusIn(self, event):
        #self.hWnd.attributes('-alpha', 1.0)
        self.alive = True; self.hitCode = 1
    #鼠标离开
    def _onFocusOut(self, event):
        self.alive = False; self.hitCode = 0
    #鼠标单击-左键
    def _onClickButton_1(self, event):
        self.hitCode *= 2
        self._active(event)
        self.moveX = event.x
        self.moveY = event.y
    #鼠标单击-中键
    def _onClickButton_2(self, event):
        self.hitCode /= 24
        self._active(event)
    #鼠标单击-右键
    def _onClickButton_3(self, event):
        self.hitCode *= 3
        self._active(event)
    #鼠标弹起-左键
    def _onReleaseButton_1(self, event):
        self.moveX = None
        self.moveY = None
    #鼠标移动-左键
    def _onMotion(self, event):
        deltax = event.x - self.moveX
        deltay = event.y - self.moveY
        x = self.hWnd.winfo_x() + deltax
        y = self.hWnd.winfo_y() + deltay
        self.hWnd.geometry("+%s+%s" % (x, y))
    #鼠标单击-激活
    def _active(self, event):
        #print(self.hitCode)
        if(self.hitCode == 0.5):
            self.alpha_now = 0.8
            self.hWnd.attributes('-alpha', self.alpha_now)
            self.savePos = True
            #self.initHwnd("逮着你了！")

    #初始窗口
    def initHwnd(self, strText = '', x = 300, y = 300, w = 86, h = 86):
        self.strLbText.set(strText)
        self.hWnd.geometry("%sx%s+%s+%s" % (self.w, self.h, self.x, self.y))

    #渐变消失线程   
    def _thrdSet_Alpha(self): 
        self.thrdSet_Alpha = threading.Thread(target = self._Set_Alpha_)
        self.thrdSet_Alpha.setDaemon(False)
        self.thrdSet_Alpha.start() 
    #开始监听
    def _Set_Alpha_(self):
        while(True):
            if(self.alive == False and self.alpha_now > 0.01):
                self.alpha_now *= 0.98
                self.hWnd.attributes('-alpha', self.alpha_now)
                print(self.alpha_now)
            time.sleep(0.2)     #延时
    

if __name__ == '__main__':
    frm = myWinForm()
