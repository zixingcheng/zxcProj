#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-10-28 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    智能物联网综合管理平台--上海人民智能电表
"""

import sys, os, time
import re, requests
import urllib,urllib.parse,urllib.request,http.cookiejar 
from lxml import etree
import mySystem


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myData_Trans
from myWeb_urlLib import myWeb  



#API-平台注册
class myIOT(): 
    def __init__(self, host = ""):
        # 获取session对象（操作对象是浏览器，而不是html页面），用于处理动态变化的cookie（有cookie的就用session）
        self.host = host
        self.ind = 0
        self.session = requests.Session()       #构造Session

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self.Dir_Image = self.Dir_Base + "/Temps/Images"
        self.Dir_Image = myIO.checkPath(self.Dir_Image)
        myIO.mkdir(self.Dir_Image, False, True) #覆盖     

    # 模拟登录
    def Login(self, urlLogin = "", urlDoLogin = "", url_img_code = "", useLocal = True):   
        # 创建连接
        # headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        

        #方便调试区分真实登录，和本地cookie
        if(useLocal):
            # 生成cookie，浏览器登录后得到的cooki, 把cookie字符串处理成字典，以便接下来使用
            cookie_str = r'Av2dfsdf_admin_username=%E7%AE%80%E6%98%93%E7%94%9F%E6%B4%BB; sign=3q3g41aeve7k2nvsfbh2ai7j2p; Hm_lvt_2510c71771575460d26bb883a51bde54=1571463497,1572248265,1572361282,1572414162; Av2dfsdf_language=zh-CN; Hm_lpvt_2510c71771575460d26bb883a51bde54=1572425283'
            self.cookies = {}
            for line in cookie_str.split(';'):
                key, value = line.split('=', 1)
                self.cookies[key] = value

            #设置请求头
            headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

            #在发送get请求时带上请求头和cookies
            resp = requests.get(self.host + "/" + urlLogin, headers = headers, cookies = self.cookies)
            print(resp.content.decode('utf-8'))
            
            # 不兼容封装调用
            #r = self.web.Do_API_get(urlLogin, "验证码结果").strip().replace("\"", "")
        else:
            # 登录页面
            resp = self.session.get(self.host + "/" + urlLogin)

            # 获取验证码信息
            captcha_code = ""
            imgPath = self.Dir_Image + F'/code_{str(self.ind)}.jpg'
            if(imgPath != ""):
                # 获取验证码图片，文本实际上是图片的二进制文本
                response = self.session.get(self.host + "/" + url_img_code)
                img = response.content

                # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
                with open(imgPath, 'wb' ) as f:
                    f.write(img)

                # 获取验证码
                captcha_code = self.Get_Captcha(imgPath, True)

            # 登录请求
            if(captcha_code != ""):
                # 组装请求参数
                data = {
                    'username': '简易生活', 
                    'password': 'zxcvbnm,./123', 
                    'verify': captcha_code,
                    'submit': ''
                }
            
                # 登录
                resp = self.session.post(self.host + "/" + urlDoLogin, data)
                print(resp.content.decode('utf-8'))
    # 获取验证码 
    def Get_Captcha(self, imgPath, useLoacal = False):   
        if(useLoacal):
            captcha_code = input("输入验证码：")
        else:
            # 读取图片文件 
            img_str = myIO.getImage_Str(imgPath)
            if(img_str == ""):
                return ""
            else:                
                # 调用API，人工识别验证码
                pWeb = myWeb("http://39.105.196.175:8668")
               
                # 组装请求参数
                req = {
                    "params": {
                        "imgName": myIO.getFileName(imgPath, False),
                        "imgData": img_str,
                        "usrName": "茶叶一主号"
                        }
                }

                # 调用API，轮询请求打码结果
                r = pWeb.Do_Post("zxcAPI/robot/captcha_img", req, "验证码", True, True, True) 
                res = myData_Trans.Tran_ToDict(r.decode())
                if(res.get("res", "" == "OK")):
                    msgID = res['msgID']
                    ind = 0

                    # 轮询调用API
                    while(True):
                        # 轮询提取人工识别结果 
                        r = pWeb.Do_API_get(F"zxcAPI/robot/captcha/code/{msgID}", "验证码结果").strip().replace("\"", "")
                        if(r != ""):
                            lstR = r.split(',')
                            captcha_code = lstR[len(lstR) - 1]
                            break
                            
                        # 超时检测
                        if(ind > 60): return False
                        ind += 1
                        time.sleep(3)
        return captcha_code



#主启动程序 
if __name__ == "__main__":    

    # 模拟登录
    pIOT = myIOT("https://168.tqdianbiao.com")
    pIOT.Login("admin/public/login", "admin/public/dologin", "index.php?g=admin&m=checkcode&a=index&length=4&font_size=25&width=235&height=52&use_noise=1&use_curve=0&time=Math.random()")

    exit(0)
