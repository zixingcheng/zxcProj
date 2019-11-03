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
        self.iotConnected = False   #自定义IOT是否连接

        self.iotAddress = ""        #自定义IOT地址
        self.iotCoor_X = ""         #自定义IOT坐标X
        self.iotCoor_Y = ""         #自定义IOT坐标Y
        
        self.usrID = ""             #自定义IOT关联用户id
        self.usrName = ""           #自定义IOT关联用户名
        
        self.datetime = datetime.datetime.now()  
        self.remark = ""            #备注
        self.valid = True           #是否有效
        self.loaded = False         #是否已加载
        self.dictSets = {}          #字典型设置信息
        self.iotInfo = {'命令': {'未完成': {}, '已完成': {}}}  #设备其他信息-自定义
        self.Trans_FromDict(dictSets)

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        if(dictSets == None): dictSets = self.dictSets
        dictSets['ID'] = self.ID
        dictSets['设备编号'] = self.iotId
        dictSets['设备名称'] = self.iotName
        dictSets['设备类型'] = self.iotType
        dictSets['设备状态'] = self.iotState
        dictSets['设备信息'] = self.iotInfo
        dictSets['通讯地址'] = self.iotAddress_Postal
        dictSets['是否连接'] = self.iotConnected
        dictSets['用户编号'] = self.usrID
        dictSets['用户名'] = self.usrName

        dictSets['地址'] = self.iotAddress
        dictSets['坐标X'] = self.iotCoor_X
        dictSets['坐标Y'] = self.iotCoor_Y

        dictSets['日期'] = self.datetime
        dictSets['isDel'] = not self.valid 
        dictSets['isLoad'] = self.loaded 
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
        self.iotInfo = dictSets.get('设备信息', self.iotInfo)  
        self.iotAddress_Postal = dictSets.get('通讯地址', self.iotAddress_Postal)   
        self.iotConnected = dictSets.get('是否连接', self.iotConnected) 
        
        self.usrID = dictSets.get('用户编号', self.usrID)   
        self.usrName = dictSets.get('用户名', self.usrName)   
        
        self.iotAddress = dictSets.get('地址', self.iotAddress)   
        self.iotCoor_X = dictSets.get('坐标X', self.iotCoor_X)  
        self.iotCoor_Y = dictSets.get('坐标Y', self.iotCoor_Y)  

        self.datetime = dictSets.get("日期", self.datetime)
        self.remark = dictSets.get("备注", self.remark)
        self.isDel = not dictSets.get('isDel', not self.valid)  
        self.valid = not self.isDel
        self.loaded = dictSets.get('isLoad', self.loaded)  
        return True
    
    # Iot命令状态检查-多种类型
    def Check_CmdState(self, cmdType):
        # 提取命令
        isDone = False
        for x in self._iotCmds:

            # 命令已完成，超过10分钟后移入已完成
            pass
        return 'done'

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
        if(dictSet == None or len(dictSet) != 1): 
            return None
        return self._new_Iot(list(dictSet.values())[0])
    # 初始物联网对象集
    def _new_Iot(self, dictSet):
        return myIOT(dictSet)
    
    # 检查是否已经存在   
    def _Check(self, rowInfo, updata = False): 
        #修正数据类型 
        if(rowInfo.get('操作日志', "") == ""):
            pIot = myIOT()
            pIot.Trans_FromDict(rowInfo)

            #调用基类更新
            pIot.Trans_ToDict(rowInfo)
        return super()._Check(rowInfo, updata)
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
        self._iotCmds = {}                      #待执行命令集   
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
        self._webHeaders = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
            'X-Requested-With': 'XMLHttpRequest'
            }
        
        #方便调试区分真实登录，和本地cookie
        if(cookie_str != ""):
            # 生成cookie，浏览器登录后得到的cooki, 把cookie字符串处理成字典，以便接下来使用
            for line in cookie_str.split(';'):
                key, value = line.split('=', 1)
                self._webCookies[key] = value

            #在发送get请求时带上请求头和cookies
            #r = self.web.Do_API_get(urlLogin, "验证码结果").strip().replace("\"", "")   # 不兼容封装调用
            return self._DoWeb_Get("登录", urlLogin, {})
        else:
            # 登录页面
            resp = self._DoWeb_Get("登录", urlLogin, {})

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
    

    # Iot状态信息--更新
    '''
    1.提取基本信息，电量电费信息，以及命令、抄表信息等，区分未执行；
    2.未执行的命令、抄表添加进监测命令队列；
    3.命令监测线程，监测命令队列，未完成定时查询执行状态，并更新，已完成的推送通知，统一处理；

    '''
    def Updata_Iot_State(self, pIot):
        self._getIot_Info_Base(pIot)                #更新Iot基本信息
        self._getIot_Info_PowerMoney(pIot)          #更新Iot基本信息-电量、费用信息      
        
        self._getIot_Info_CmdsState(pIot, True)     #提取未执行完成命令，并更新当前未完成


        #@Test 命令状态校检
        self._checkIot_CmdsState_Monitor()

        return self.Updata_Iot_Info(pIot)
    # Iot信息同步--更新
    def Updata_Iot_Info(self, pIot):
        pIot.loaded = True                          #标识已加载
        self.Iots._Updata(pIot.ID, pIot.Trans_ToDict(), False, False)
        return True
    

    
    # Iot命令状态校检-后台监测线程
    def _checkIot_CmdsState_Monitorthread(self):
        # 循环所有执行中命令
        pass
    # Iot命令状态校检
    def _checkIot_CmdsState_Monitor(self):
        # 提取命令、抄表未完成状态信息
        self._checkIot_CmdsState_doing()


        # 循环所有执行中命令
        timeNow = time.time()
        for x in self._iotCmds:
            # 提取命令信息
            pCmd = self._iotCmds[x]
            isOvertime = False          #是否超时
            timesCheck = pCmd['命令校检']['校检次数']


            # 对未完成信息计数，超过次数/超时，则执行取消
            if(row['执行时间'] == 0):
                timeCmd = myData_Trans.Tran_ToTime(row['data-time'], "%Y-%m-%d %H:%M:%S")

                # 超时，超次数检查
                if(timeNow - timeCmd > 60):
                    isOvertime = True
                elif(timesCheck > 30):
                    # 超次数检查
                    isOvertime = True
                else:
                    #检查次数累加
                    pCmd['命令校检']['校检次数'] = isOvertime + 1
            else:
                # 已执行，超过10分钟后移入已完成
                pass

                    
            if(timeNow - pCmd['执行时间']):
                pass

                row['执行时间'] = myData_Trans.Tran_ToTime(row['data-time'], "%Y-%m-%d %H:%M:%S")  


            #  #time类型，便于超时计算，统一记录为操作时间，注意未执行时直接计算为超时


            #self._iotCmds[key] = row            #传址同步修改值

            # 命令已完成，超过10分钟后移入已完成
            pass
        pass
    # Iot命令状态校检-所有执行中-重写按实际分类实现
    def _checkIot_CmdsState_doing(self):
        pass
    


    # 控制--状态
    def Control_State(self, iotID, state = ""):
        # 提取IOT对象
        if(state not in self.ctrlStates): return False
        return True
    # 控制--命令任务
    def Control_Cmd(self, iotID, cmdType = ""):
        # 提取IOT对象
        if(state not in self.ctrlStates): return False
        return True


    # Iot信息管理
    #region Iot信息管理

    # Iot信息--添加
    def Add_Iot(self, dictSet):
        dictSet['设备类型'] = self.typeIot
        return self.Iots.Add_Row(dictSet, True)
    # Iot信息--获取
    def Get_Iot(self, iotID, bRefresh = True):
        pIot = self.Iots.getIOT(iotID)
        if(bRefresh):
            self.Updata_Iot_State(pIot)
        return pIot
    
    
    # 获取Iot基本信息
    def _getIot_Info_Base(self, pIot):
        return pIot.iotInfo
    # 获取Iot基本信息-电量、费用
    def _getIot_Info_PowerMoney(self, pIot):
        return pIot.iotInfo
    # 获取Iot命令执行状态
    def _getIot_Info_CmdsState(self, pIot, bOnlyFail = True):
        #row = {'命令状态': '', '执行时间': ''}
        return []

    #endregion
    

    # 初始物联网对象集
    def _Init_Iots(self, dir = ""):
        self.typeIot = "电表"         
        self.Iots = myIOTs(dir = dir)    
    # 初始IOT状态集
    def _Init_ctrlState(self):
        self.ctrlStates = ["open", "close"]   


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
        if(bDebug): myDebug.Debug(" ---请求完毕。\n")

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
        if(bDebug): myDebug.Debug(" ---请求完毕。\n")
            
        # 验证信息
        if(len(checkInfo) > 0):
            pass
        return resp



#主启动程序 
if __name__ == "__main__":    
    # 模拟登录
    pIOT_Plat = myIOT_Plat("https://168.tqdianbiao.com")
    
    cookie_str = r'Av2dfsdf_admin_username=%E7%AE%80%E6%98%93%E7%94%9F%E6%B4%BB; Hm_lvt_2510c71771575460d26bb883a51bde54=1571463497,1572248265,1572361282,1572414162; Av2dfsdf_language=zh-CN; sign=qtkkoajhh292bm9fqr5daak99m; Hm_lpvt_2510c71771575460d26bb883a51bde54=1572485723'
    pIOT_Plat.Login("admin/public/login", "admin/public/dologin", "index.php?g=admin&m=checkcode&a=index&length=4&font_size=25&width=235&height=52&use_noise=1&use_curve=0&time=Math.random()", cookie_str)
    
    pIOT_Plat.Add_Iot({'设备编号': '190801207866', '设备名称': '测试电表-01', '通讯地址': "190801207866", '用户名': 'zxc', '日期': '2019-08-27 11:12:00'})


    exit(0)

