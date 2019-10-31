#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-10-28 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    物联网IOT  智能物联网综合管理平台
"""

import sys, os, time, datetime
import re, requests
import urllib,urllib.parse,urllib.request,http.cookiejar 
from lxml import etree
import mySystem


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myData_DB, myData_Trans, myDebug
from myWeb_urlLib import myWeb  



# 物联网IOT对象
class myIOT(): 
    def __init__(self, dictSets = None):  
        self.iotId = ""             #自定义IOT编号
        self.iotName = ""           #自定义IOT名称
        self.iotType = ""           #自定义IOT类型
        self.iotState = ""          #自定义IOT状态
        self.iotAddress_Postal = "" #自定义IOT通讯地址
        self.iotAddress = ""        #自定义IOT地址
        self.iotCoor_X = ""         #自定义IOT坐标X
        self.iotCoor_Y = ""         #自定义IOT坐标Y
        
        self.usrID = ""             #自定义IOT关联用户id
        self.usrName = ""           #自定义IOT关联用户名
        
        self.datetime = datetime.datetime.now()  
        self.remark = ""            #备注
        self.valid = True           #是否有效
        self.dictSets = {}          #字典型设置信息
        self.Trans_FromDict(dictSets)

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        if(dictSets == None): dictSets = self.dictSets
        dictSets['ID'] = self.ID
        dictSets['设备编号'] = self.iotId
        dictSets['设备名称'] = self.iotName
        dictSets['设备类型'] = self.iotType
        dictSets['设备状态'] = self.iotState
        dictSets['通讯地址'] = self.iotAddress_Postal
        dictSets['用户编号'] = self.usrID
        dictSets['用户名'] = self.usrName

        dictSets['地址'] = self.iotAddress
        dictSets['坐标X'] = self.iotCoor_X
        dictSets['坐标Y'] = self.iotCoor_Y

        dictSets['日期'] = self.datetime
        dictSets['isDel'] = not self.valid 
        dictSets['备注'] = self.remark
        return dictSets
    # 转换为对象，由字典结构
    def Trans_FromDict(self, dictSets):     
        #信息必须存在
        if(dictSets == None): return False

        #解析信息
        self.ID = dictSets.get('ID',-1)
        self.iotId = dictSets['设备编号']
        self.iotName = dictSets.get('设备名称', self.iotName)   
        self.iotType = dictSets.get('设备类型', self.iotType) 
        self.iotState = dictSets.get('设备状态', self.iotState)  
        self.iotAddress_Postal = dictSets.get('通讯地址', self.iotAddress_Postal)   
        
        self.usrID = dictSets.get('用户编号', self.usrID)   
        self.usrName = dictSets.get('用户名', self.usrName)   
        
        self.iotAddress = dictSets.get('地址', self.iotAddress)   
        self.iotCoor_X = dictSets.get('坐标X', self.iotCoor_X)  
        self.iotCoor_Y = dictSets.get('坐标Y', self.iotCoor_Y)  

        self.datetime = dictSets.get("日期", self.datetime)
        self.remark = dictSets.get("备注", self.remark)
        self.isDel = not dictSets.get('isDel', not self.valid)  
        return True

# 物联网IOT对象集
class myIOTs(myData_DB.myData_Table): 
    def __init__(self, dbName = 'zxcDB_IOTs', dir = ""):
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Iot/Iots/"
            myIO.mkdir(self.Dir_DataDB, False) 
        super().__init__(dbName, self.Dir_DataDB, True) 

        #固定字段
        self.Add_Fields(['设备编号', '设备名称', '设备类型', '设备状态', '通讯地址', '用户名', '用户编号', '地址', '坐标X', "坐标Y", '日期', '备注'], ['string','string','string','string','string','string','string','string','string','string','datetime','string'], [])
    
    # 提取IOT对象，指定设备编号
    def getIOT(self, iotId): 
        # 组装查询条件
        strFilter = F"isDel=={str(False)} && 设备编号=={iotId}" 

        # 查询数据 
        dictSet = self.Query(strFilter, "", True)

        # 返回Iot对象
        if(dictSet == None): return None
        return self._new_Iot(dictSet)
    # 初始物联网对象集
    def _new_Iot(self, dictSet):
        return myIOT(dictSet)

    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base): 
        if(super()._IsSame(rowInfo, rowInfo_Base)): return True

        # 必须ID相同、是否删除相同
        if(rowInfo['ID'] > 0):
            if(rowInfo['ID'] != rowInfo_Base['ID']): return False
        if(rowInfo['isDel'] != rowInfo_Base['isDel']): return False
        if(rowInfo['用户名'] == rowInfo_Base['用户名']):
            if(rowInfo['设备编号'] == rowInfo_Base['设备编号']):
                if (rowInfo['设备状态'] != rowInfo_Base['设备状态']or rowInfo['日期'] - rowInfo_Base['日期']).days < 1024:
                    return True
        return False
    # 更新
    def _Updata(self, x, rowInfo, bSave = False, bCheck = True): 
        #参数设置更新
        if(bCheck == True):
            pIOT = myIOT(self.rows[x])
            pIOT.Trans_FromDict(rowInfo)
            pIOT.Trans_ToDict(rowInfo)

        #调用基类更新
        super()._Updata(x, rowInfo, bSave)


# 物联网IOT -智能物联网综合管理平台
class myIOT_Plat(): 
    def __init__(self, host = ""):
        # 获取session对象（操作对象是浏览器，而不是html页面），用于处理动态变化的cookie（有cookie的就用session）
        self._webHost = host
        self._webCookies = {}
        self._webSession = requests.Session()   #构造Session
        self._webImg_ind = 0                    #图片下载序号，避免重复
        self._Init_Iots()                       #初始物联网对象集
        self._Init_ctrlState()                  #初始IOT状态集 
        
        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self._Dir_Base = os.path.abspath(os.path.join(strDir, ".."))  
        self._Dir_Image = self._Dir_Base + "/Temps/Images"
        self._Dir_Image = myIO.checkPath(self._Dir_Image)
        myIO.mkdir(self._Dir_Image, False, True)#覆盖    

    # 模拟登录
    def Login(self, urlLogin = "", urlDoLogin = "", url_img_code = "", cookie_str = ""):   
        # 创建连接
        self._webHeaders = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        
        #方便调试区分真实登录，和本地cookie
        if(cookie_str != ""):
            # 生成cookie，浏览器登录后得到的cooki, 把cookie字符串处理成字典，以便接下来使用
            for line in cookie_str.split(';'):
                key, value = line.split('=', 1)
                self._webCookies[key] = value

            #在发送get请求时带上请求头和cookies
            #r = self.web.Do_API_get(urlLogin, "验证码结果").strip().replace("\"", "")   # 不兼容封装调用
            return self._DoWeb_Get("登录页面", urlLogin, {})
        else:
            # 登录页面
            resp = self._DoWeb_Get("登录页面", urlLogin, {})

            # 获取验证码信息
            captcha_code = ""
            imgPath = self._Dir_Image + F'/code_{str(self._webImg_ind)}.jpg'
            if(imgPath != ""):
                # 获取验证码图片，文本实际上是图片的二进制文本
                response = self._DoWeb_Get("验证码下载", url_img_code, {})
                img = response.content

                # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
                with open(imgPath, 'wb' ) as f:
                    f.write(img)

                # 获取验证码
                captcha_code = self.Login_getCaptcha(imgPath, True)

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
                resp = self._DoWeb_Post("验证码下载", urlDoLogin, data, {})
                print(resp.content.decode('utf-8'))

            # 登录成功验证
            return True
    # 获取验证码 
    def Login_getCaptcha(self, imgPath, useLoacal = False):   
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
    
    # Iot信息--添加
    def Add_Iot(self, dictSet):
        dictSet['设备类型'] = self.typeIot
        return self.Iots.Add_Row(dictSet, True)

    # 控制--状态
    def Control_State(self, state = ""):
        if(state not in self.ctrlStates): return False
        pass  
    
    # 操作webApi接口-Post方式
    def _DoWeb_Post(self, strTag = "", url = "", data = None, checkInfo = {}, bDebug = True):
        self._webReferer = self._webHost + "/" + url
        if(bDebug): myDebug.Debug("请求" + strTag + "页面：" + self._webReferer)

        #方便调试区分真实登录，和本地cookie
        if(len(self._webCookies) > 0):
            resp = requests.post(self._webReferer, data, headers = self._webHeaders, cookies = self._webCookies)
        else:
            resp = self._webSession.post(self._webReferer, data)

        # 输出结果
        print(resp.content.decode('utf-8'))
        if(bDebug): myDebug.Debug("    请求完毕。")

        # 验证信息
        if(len(checkInfo) > 0):
            pass
        return resp
    # 操作webApi接口-Get方式
    def _DoWeb_Get(self, strTag = "", url = "", checkInfo = {}, bDebug = True):
        self._webReferer = self._webHost + "/" + url
        if(bDebug): myDebug.Debug("请求" + strTag + "页面：" + self._webReferer)

        #方便调试区分真实登录，和本地cookie
        if(len(self._webCookies) > 0):
            resp = requests.get(self._webReferer, headers = self._webHeaders, cookies = self._webCookies)
        else:
            resp = self._webSession.get(self._webReferer)
            
        # 输出结果
        #print(resp.content.decode('utf-8'))
        if(bDebug): myDebug.Debug("    请求完毕。")
            
        # 验证信息
        if(len(checkInfo) > 0):
            pass
        return resp


    # 初始物联网对象集
    def _Init_Iots(self, dir = ""):
        self.typeIot = "电表"
        self.Iots = myIOTs(dir = dir)    
    # 初始IOT状态集
    def _Init_ctrlState(self):
        self.ctrlStates = ["open", "close"]   



#主启动程序 
if __name__ == "__main__":    
    # 模拟登录
    pIOT_Plat = myIOT_Plat("https://168.tqdianbiao.com")
    
    cookie_str = r'Av2dfsdf_admin_username=%E7%AE%80%E6%98%93%E7%94%9F%E6%B4%BB; Hm_lvt_2510c71771575460d26bb883a51bde54=1571463497,1572248265,1572361282,1572414162; Av2dfsdf_language=zh-CN; sign=qtkkoajhh292bm9fqr5daak99m; Hm_lpvt_2510c71771575460d26bb883a51bde54=1572485723'
    pIOT_Plat.Login("admin/public/login", "admin/public/dologin", "index.php?g=admin&m=checkcode&a=index&length=4&font_size=25&width=235&height=52&use_noise=1&use_curve=0&time=Math.random()", cookie_str)
    
    pIOT_Plat.Add_Iot({'设备编号': '190801207866', '设备名称': '测试电表-01', '通讯地址': "190801207866", '用户名': 'zxc', '日期': '2019-08-27 11:12:00'})


    exit(0)

