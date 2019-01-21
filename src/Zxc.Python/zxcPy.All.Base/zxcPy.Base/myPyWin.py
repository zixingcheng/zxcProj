#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-12-28 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的自动化操作接口(使用pywinauto、pyuserinput封装)
"""
import sys, os, time, mySystem 
from pywinauto import application
from pykeyboard import PyKeyboard

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", True) 
import myIO


# Python的Windows操作类
class myPyWin(object):
    """
    pywin framwork main class
    tool_name : 程序名称，支持带路径
    windows_name : 窗口名字
    """

    # 初始化方法，初始化一个app
    def __init__(self, nSleep = 0.2):
        self.SLEEP_TIME = nSleep
        self.app = application.Application()
    # 启动应用程序
    def run(self, tool_name):
        self.app.start(tool_name)
        time.sleep(self.SLEEP_TIME)

    # 连接应用程序
    # app.connect_(path = r"c:\windows\system32\notepad.exe")
    # app.connect_(process = 2341)
    # app.connect_(handle = 0x010f0c)
    def connect(self, window_name):
        self.app.connect(title = window_name)
        time.sleep(self.SLEEP_TIME)

    # 关闭应用程序
    def close(self, window_name):
        self.app[window_name].Close()
        time.sleep(self.SLEEP_TIME)
    # 最大化窗口
    def max_window(self, window_name):
        self.app[window_name].Maximize()
        time.sleep(self.SLEEP_TIME)

    # 菜单点击
    def menu_click(self, window_name, menulist):
        self.app[window_name].MenuSelect(menulist)
        time.sleep(self.SLEEP_TIME)
    # 输入内容
    def input(self, window_name, controller, content):
        self.app[window_name][controller].TypeKeys(content)
        time.sleep(self.SLEEP_TIME)
    # 鼠标左键点击, 下面两个功能相同,下面支持正则表达式 ('关于“记事本”)
    def click(self, window_name, controller):
        self.app[window_name][controller].Click()
        time.sleep(self.SLEEP_TIME)
    # 鼠标左键点击(双击)
    def double_click(self, window_name, controller, x = 0,y = 0):
        self.app[window_name][controller].DoubleClick(button = "left", pressed = "",  coords = (x, y))
        time.sleep(self.SLEEP_TIME)
    # 鼠标右键点击，下移进行菜单选择(窗口名，区域名，数字，第几个命令)
    def right_click(self, window_name, controller, order):
        self.app[window_name][controller].RightClick()
        k = PyKeyboard()
        for down in range(order):
            k.press_key(k.down_key)
            time.sleep(0.1)
        k.press_key(k.enter_key)
        time.sleep(self.SLEEP_TIME)


#测试
if __name__ ==  "__main__":
    # 启动程序，记事本只能开一个
    app = myPyWin()

    #定位记事本窗口
    controller = "Edit"
    bTest_notepad = False
    if(bTest_notepad):
        app.run("notepad.exe")
        window_name = u"无标题 - 记事本"
        app.connect(window_name)


        #打开帮助并关闭 
        app.menu_click(window_name, u"帮助->关于记事本")
        app.click(u'关于记事本', u'确定')
     

        #输入文本，通过Spy++ 获取controller，即窗口类名
        content = u"johnny"
        window_name_new = content + ".txt"
        app.input(window_name, controller, content)
     
        # Ctrl + a 全选
        app.input(window_name,controller, "^a")

        # 选择复制
        app.right_click(window_name,controller, 3)

        #选择粘贴
        app.right_click(window_name,controller, 4)
        k = PyKeyboard()
        k.press_key(k.enter_key)

        # Ctrl + v 粘贴
        app.input(window_name,controller, "^v")

        # Ctrl + s 保存
        app.input(window_name,controller, "^s")

        # 输入文件名
        strDir, strName = myIO.getPath_ByFile(__file__)
        path = strDir + "\\" + content + ".txt"
        app.input(u"另存为", controller, path)

        # 保存
        app.click(u"另存为","Button")
        try:
            app.click(u"确认另存为","Button")
            os.remove(path)
        except:
            pass
        finally:
            app.close(window_name_new)
    
            
    #app.run("D:\\Program Files (x86)\\WXWork\\WXWork.exe")
    #app.connect("D:\\Program Files (x86)\\国泰君安证券新富易\\bin\\RichEZ.exe")
    #app.run("D:/Program Files (x86)/国泰君安证券新富易/bin/oRichEZ.exe")
    
    
    bTest_gtja = True
    if(bTest_gtja): 
        app.run(u"D:\\Program Files (x86)\\国泰君安证券新富易\\bin\\RichEZ.exe")
        app.app.connect(path = u"D:\\Program Files (x86)\\国泰君安证券新富易\\bin\\RichEZ.exe")
        window_name = u"国泰君安证券|富易登录"
        #app.connect(window_name)
        
        #app.input(window_name, "Edit", "10309023") 
        
        #app.input(window_name, "Edit3", "10309023")
        pyK = PyKeyboard()
        #pyK.press_key('1')
        #pyK.press_key('3')
        #pyK.press_key('2')
        #pyK.press_key('9')
        #pyK.press_key('1')
        #pyK.press_key('6')

        # 定位当日成交查询
        window_name = u"富易 - 张斌"

        app.app[window_name].type_keys("{F6}")
        time.sleep(2)

        #app.click(window_name,"刷新(&F)")
        #time.sleep(8)
        app.click(window_name,"导出")
        time.sleep(2)
        
        # 输入文件名
        strDir, strName = myIO.getPath_ByFile(__file__)
        path = strDir + "\\" + window_name + ".xls"
        app.input(u"另存为", controller, path)

        # 保存
        app.click(u"另存为","Button")
        try:
            app.click(u"确认另存为","Button")
            os.remove(path)
        except:
            pass
        finally:
            app.close(window_name_new)

        #app.click(window_name , u"Button)")
        #app.click(window_name , u"Button)")
        #pyK.press_key(pyK.function_keys[6]) # Tap F5
        #aa = app.app[u'富易 - 张斌']['舒心'].Click()

        #app.input(window_name, "TFyPassEdit", "132916")
        #app.click(u"TFyPassEdit","TFyPassEdit")
        
        #app.click(window_name, u"登 录")
        
        #app.app.window_(title_re = u'富易 - 张斌').window_(title_re = u'ToolBar').window_(title_re = u'设置').Click()

        pg = app.app[u'富易 - 张斌'][u'ToolBar']
        pg.print_control_identifiers()
        #aa = app.app[u'富易 - 张斌']['Button20'].print_control_identifiers()

        #aa = app.app[u'富易 - 张斌']['重置成本'].Click()
        #aa = app.app[u'富易 - 张斌']['Button32'].Click()
        #aa = app.app[u'富易 - 张斌'].window_(handle = 0X00210D04).Click()
         
        #app.menu_click(window_name, u"TChildMenuBox->新股申购")
        
        #aa = pg.GetButton(0)
        

        bb =0
        
        # app.app[u'富易 - 张斌']['ToolBar'].ToolbarButton.Click()

        #app.click(window_name + "->ToolBar", u"其它(&O)")
        #app.click(window_name , u"Button3)")
        #app.click(window_name , u"Button4)")
        #app.click(window_name , u"Button5)")
        #app.click(window_name , u"Button6)")
        #app.click(window_name , u"Button7)")
        
        #打开帮助并关闭 
        #app.menu_click(window_name, u"设置")
        #app.click(u'关于记事本', u'确定')
        
