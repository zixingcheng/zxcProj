# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-05-15 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    透明移动悬浮窗口, 图标文字 基于pyqt5
    @依赖库： pyqt5
"""
import time, threading, random
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QCursor, QBitmap, QColor, QFont, QPalette
from PyQt5.QtCore import Qt, QRectF



# 透明悬浮窗口
class myWinForm(QWidget):
    def __init__(self, type = "", name = "", parent=None, icoUrl = "", imgDir = "", alpha = 0.8, randomXY = True, autoMove = True, typeMove = 0, range = [200,900,200,650]):  
        random.seed(a=None, version=2)
        super(myWinForm, self).__init__(parent)

        self.name = name            #窗口名称
        self.type = type            #窗口标识-类型
        self.tag = ""               #窗口标识
        self.imgDir = imgDir        #图标路径
        self.icoUrl = icoUrl        #图标
        self.alpha = alpha          #窗口透明度
        self.alpha_now = alpha      #窗口透明度-当前
        self.alpha_limit = 0.01     #窗口透明度-最小
        self.alpha_gradient = 0.97  #渐变幅度
        self.randomXY = randomXY    #随机窗口位置
        self.autoMove = autoMove    #自动移动
        self.typeMove = typeMove    #移动模式
        self.alive = False          #是否激活
        self.rangHwnd = range       #限定范围
        self.hitCode = 0            #命中码，简易密码组合以激活窗体
        self.isUsed = False         #是否使用中
        self.text = ""              #窗口显示内容
        self.moveX = 0; self.moveY = 0; 
        self._initForm()
        
    #随机窗口位置
    def _randomXY(self):
        if(self.rangHwnd == None):
            self.rangHwnd = [200,900,200,650] 
        self.x = random.randint(self.rangHwnd[0], self.rangHwnd[1])
        self.y = random.randint(self.rangHwnd[2], self.rangHwnd[3])
    #初始窗口
    def _initForm(self, x = 300, y = 300, w = 99, h = 99):
        #记录位置大小
        self.x = x;  self.y = y
        self.w = w; self.h = h
        if(self.randomXY): self._randomXY()
        #print(self.x, self.y)

        #初始窗口
        self.setWindowTitle("不规则窗体的实现例子")
        self.setWindowFlag(Qt.FramelessWindowHint)          # 设置无边框
        self.setWindowFlag(Qt.Tool)                         # 设置无边框
        self.setWindowFlag(Qt.WindowStaysOnTopHint)         # 窗口置顶
        self.setWindowOpacity(0.8)                          # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)      # 设置窗口背景透明
        self.setHidden(True)                                # 设置窗口隐藏
        self.resize(self.w, self.h)
        self.setGeometry(self.x, self.y, self.w, self.h)
        self._initForm_urs(None)                            # 自定义窗口设置，便于重载界面

        #遮掩蒙板
        #self.pix = QBitmap(self.icoUrl)
        #self.resize(self.pix.size())
        #self.setMask(self.pix)
        #self.dragPosition = None
        #print(self.pix.size())

        # 窗口背景透明渐变-线程方式
        self._thrdSet_Alpha()
    #初始窗口--自定义
    def _initForm_urs(self, msg):
        pass

    #重载窗体绘制事件，一般 paintEvent 在窗体首次绘制加载， 要重新加载paintEvent 需要重新加载窗口使用 self.update() or  self.repaint()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap(self.imgDir + self.icoUrl))

        painter.setPen(Qt.blue)
        painter.setFont(QFont('Decorative', 7))     # QFont.Bold
        rect = QRectF(self.w/4,self.h/2,self.w/3*2,self.h/2)
        painter.drawText(rect, Qt.AlignCenter, self.text)  
    #重载鼠标进入控件事件 
    def enterEvent(self, event):
        self.alive = True; self.hitCode = 1
    #重载鼠标离开控件事件 
    def leaveEvent(self, event):
        self.alive = False; self.hitCode = 0
    #重载鼠标按下事件 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            
            #窗体激活处理
            self.hitCode *= 2
            self._active(event)
            self.moveX = event.x
            self.moveY = event.y
        elif event.button() == Qt.RightButton:
            #窗体激活处理
            self.hitCode *= 3
            self._active(event)
        elif event.buttons () == Qt.MidButton:  
            self.hitCode /= 24
            self._active(event)   
    #重载鼠标移动事件 
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            # 当左键移动窗体修改偏移值
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()
    #重载鼠标弹起事件 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

        #窗体激活处理
        self.moveX = None
        self.moveY = None
    #初始窗口信息
    def initHwnd(self, strText = '', icoUrl = "", isShow = True, infCmd = None):
        self.icoUrl = icoUrl                         # 图标
        self.text = strText
        if(infCmd != None):
            self.tag = infCmd.get("tag", "")
            self.text = infCmd.get("msg", "")
        self.setWindowOpacity(self.alpha); self.alpha_now = self.alpha
        self.setHidden(not isShow)
        if(isShow == False): 
            self.alpha_now = 0.03                    # 模拟隐藏
            self.setWindowOpacity(self.alpha);       # 设置窗口透明度
        self.isUsed = isShow                         # 使用中情况
        self.update()
        pass
    
    #鼠标单击-激活
    def _active(self, event):
        if(self.hitCode == 0.5):
            self.alpha_now = self.alpha
            self.setWindowOpacity(self.alpha_now)      # 设置窗口透明度
            self._active_usr(event)                    # 自定鼠标单击-激活，便于重载操作
    #鼠标单击-激活--自定义
    def _active_usr(self, event):
        pass
    #渐变消失线程   
    def _thrdSet_Alpha(self): 
        self.thrdSet_Alpha = threading.Thread(target = self._Set_Alpha)
        self.thrdSet_Alpha.setDaemon(False)
        self.thrdSet_Alpha.start() 
    #渐变消失线程-实现
    def _Set_Alpha(self):
        while(True):
            if(self.alive == False and self.alpha_now > self.alpha_limit):
                self.alpha_now *= self.alpha_gradient 
                self.setWindowOpacity(self.alpha_now)   # 设置窗口透明度
            elif(self.alpha_now < self.alpha_limit):
                self.setHidden(True)
                self.isUsed = False                     # 取消使用中
            time.sleep(0.5)                             # 延时
 
# 初始QT程序
def _initApp():
    return QApplication(sys.argv)
def _exitApp(app):
    sys.exit(app.exec_())



if __name__ == '__main__':
    app = _initApp()

    frm = myWinForm(icoUrl = "aa2.png", imgDir = "D:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/Images/test/")
    frm.initHwnd("测试", "aa2.png")
    frm.show()

    _exitApp(app)
    
        
