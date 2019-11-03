#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-10-28 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    物联网IOT -智能物联网综合管理平台
"""
import sys, os, time
import re, json, requests
import mySystem
import urllib,urllib.parse,urllib.request,http.cookiejar 
from bs4 import BeautifulSoup


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myData, myData_Trans, myIOT
from myWeb_urlLib import myWeb



# 物联网IOT-电表对象
class myIOT_Dianbiao(myIOT.myIOT):
    def __init__(self, dictSets = None):  
        super().__init__(dictSets)   

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        dictSets = super().Trans_ToDict(dictSets)   
        return dictSets
    # 转换为对象，由字典结构
    def Trans_FromDict(self, dictSets):   
        bResult = super().Trans_FromDict(dictSets)  
        if(bResult == False): return False

        #解析信息  
        return True
        
# 物联网IOT-电表对象集
class myIOTs_Dianbiao(myIOT.myIOTs): 
    def __init__(self, dbName = 'zxcDB_IOTs_Dianbiao', dir = ""):
        super().__init__(dbName, dir)  
    
    # 初始物联网对象集
    def _new_Iot(self, dictSet):
        return myIOT_Dianbiao(dictSet)


# 物联网IOT -智能物联网综合管理平台-智能电表(上海人民)
class myIOT_Plat_Dianbiao_tq(myIOT.myIOT_Plat): 
    def __init__(self, host = ""):
        super().__init__("https://168.tqdianbiao.com")  

    # 模拟登录
    def Login(self, urlLogin = "", urlDoLogin = "", url_img_code = "", cookie_str = ""):   
        #方便调试区分真实登录，和本地cookie
        cookie_str = r'Av2dfsdf_admin_username=%E7%AE%80%E6%98%93%E7%94%9F%E6%B4%BB; Av2dfsdf_language=zh-CN; sign=3q754sqbuk1pto5str9ad1n242; Hm_lvt_2510c71771575460d26bb883a51bde54=1572361282,1572414162,1572509480,1572749055; Hm_lpvt_2510c71771575460d26bb883a51bde54=1572749163'

        #固定模拟登陆网址参数
        urlLogin = "admin/public/login"
        urlDoLogin = "admin/public/dologin"
        url_img_code = "index.php?g=admin&m=checkcode&a=index&length=4&font_size=25&width=235&height=52&use_noise=1&use_curve=0&time=Math.random()"
        super().Login(urlLogin , urlDoLogin, url_img_code, cookie_str)  
        

    # 控制--状态
    def Control_State(self, iotID, state = ""):
        if(super().Control_State(iotID, state) == False): return False

        # 提取IOT对象
        pIot = self.Get_Iot(iotID, True)        #更新状态
        if(pIot == None): return False

        #分类型操作
        if(pIot.iotConnected):
            if(state == "open"):
                resp = self._DoWeb_Get("", "admin/card_opr/pull_on_off/mid/{pIot.usrID}/action/pull_on", {})
            return True
        return {'err': '未连接'}
    

    # 获取Iot基本信息
    def _getIot_Info_Base(self, pIot):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("基本信息", F"admin/card_opr/index/tab/1/mid/{pIot.usrID}", {})
        soup = BeautifulSoup(resp.text,'lxml')

        #提取基本信息内容
        divs = soup.find_all('div')

        #提取行数据    
        baseInfo = pIot.iotInfo
        baseInfo['编号'] = divs[1].find('label').string
        baseInfo['连接状态'] = divs[1].find('font').string
        baseInfo['连接地址'] = divs[4].string.strip()
        baseInfo['电表类型'] = divs[6].find('a').string

        baseInfo['电表参数集']= {}
        for x in divs[7].find_all('option'):
            value = x.attrs.get('value', "0")
            if(x.attrs.get('selected', "noSelect") == ''):
                baseInfo['电表参数'] = x.string
            baseInfo['电表参数集'][value] = x.string

        baseInfo['户号'] = divs[9].find('span').string
        baseInfo['绑定用户'] = divs[11].find('a').string
        baseInfo['绑定用户编号'] = divs[11].find('a').attrs.get('data-href', "-1").replace("/admin/custom/index/id/", "")
        baseInfo['绑定卡号'] = divs[14].string.strip()
        baseInfo['描述'] = divs[16].string.strip()
        baseInfo['购电次数'] = divs[17].contents[3].next.string.replace('已于', "").strip()
        baseInfo['开户时间'] = divs[17].find('span').attrs.get('title', "")
        baseInfo['互感器变比'] = divs[20].find('input').attrs.get('value', "")
        baseInfo['继电器状态'] = divs[24].find('font').string

        #更新Iot信息
        self.iotConnected = myData.iif(baseInfo['连接状态'] == '已连接', True, False)
        return baseInfo
    # 获取Iot基本信息-电量电费
    def _getIot_Info_PowerMoney(self, pIot):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("基本信息-电量电费", F"admin/card_opr/index/tab/3/mid/{pIot.usrID}", {})
        soup = BeautifulSoup(resp.text,'lxml')

        #提取基本信息内容
        divs = soup.find_all('div')
        
        #提取行数据    
        baseInfo = pIot.iotInfo
        baseInfo['购电次数'] = divs[10].string.strip()
        baseInfo['当前总电量'] = divs[15].find('input').attrs.get('value', "0.00kwh")
        baseInfo['当前总电量同步时间'] = divs[18].find('input').attrs.get('value', "")
        
        baseInfo['当前剩余金额'] = divs[19].find('input').attrs.get('value', "0.00")
        baseInfo['当前剩余金额同步时间'] = divs[21].find('input').attrs.get('value', "")
        
        baseInfo['总充值金额'] = divs[23].find('input').attrs.get('value', "0.00元")

        #更新Iot信息
        return baseInfo
    # 获取Iot命令执行状态-只要
    def _getIot_Info_CmdsState(self, pIot, bOnlyFail = True):
        rows = self._getIot_Info_CmdsState_Order(pIot, bOnlyFail)
        rows += self._getIot_Info_CmdsState_Meter(pIot, bOnlyFail)
        return rows
    # 获取Iot命令执行状态-控制命令
    def _getIot_Info_CmdsState_Order(self, pIot, bOnlyFail = True):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("操作记录", F"admin/ele_opration/index/mid/{pIot.usrID}/tab/4/controller/CardOpr", {})
        soup = BeautifulSoup(resp.text,'lxml')

        #提取表内容
        trs = soup.find_all('tr')
        fileds = []

        #初始字段
        for x in trs[0].find_all('th'):
            fileds.append(x.string.replace("\xa0", ""))
        fileds.append("aliasname")          #电表别名
        fileds.append("data-id")            #任务编号
        fileds.append("data-state")         #任务状态
        fileds.append("data-update")        #任务更新
        fileds.append("data-time")          #任务下发时间
        fileds.append("data-logurl")        #任务日志url 
        fileds.append("命令状态")           #命令状态

        #提取行数据    
        pCmds_ok = pIot.iotInfo['命令']['已完成']        #命令操作已完成信息
        pCmds_doing = pIot.iotInfo['命令']['未完成']     #命令操作未完成信息
        rows = []
        for tr in trs[1:]:
            row = {'命令类型': 'order', '命令状态': '', '执行时间': 0}
            tds = tr.find_all('td')
            for x in range(len(fileds) - 7):
                row[fileds[x]] = tds[x].string

            #特殊属性信息提取
            if(len(tds) > 8):
                row['aliasname'] = tds[1].next.attrs['title']
                row['data-time'] = tds[4].next.attrs['title']
                row['data-id'] = tds[7].attrs['data-id']
                row['data-state'] = tds[7].attrs['data-state']
                row['data-update'] = tds[7].attrs['data-update']
                row['data-logurl'] = ""
                if(len(tds[9].contents) > 1):
                    row['data-logurl'] = ""
                    row['cmd-cancelurl'] = ""
                    for xx in tds[9].find_all('a'):
                        if(xx.string == '日志'):
                            row['data-logurl'] = xx.attrs.get('data-href', "")[1:]
                        elif(xx.string == '取消'):
                            row['cmd-cancelurl'] = xx.attrs.get('href', "")[1:]
                            row['命令状态'] = "doing"

            #命令完成状态判别
            if(row['状态'] in ['已完成', '已取消', '超时']):
                row['命令状态'] = myData.iif(row['状态'] == '已完成', "ok", "fail")
                row['执行时间'] = myData_Trans.Tran_ToTime(row['data-time'], "%Y-%m-%d %H:%M:%S")  

            #区分更新
            key = row['data-time']
            if(row['命令状态'] == "doing"):
                if(pCmds_doing.get(key, None) == None):
                    row['命令校检'] = {'校检次数': 0, '命令ID': row['data-id'], '命令状态': "doing", '校检提示': ""}
                    pCmds_doing[key] = row
                    self._iotCmds[key] = row            #传址同步修改值
            else:
                if(pCmds_ok.get(key, None) == None):
                    pCmds_ok[key] = row

                #剔除完成
                if(bOnlyFail ):
                    continue

            #缓存用于返回
            rows.append(row)
        return rows
    # 获取Iot命令执行状态-抄表命令
    def _getIot_Info_CmdsState_Meter(self, pIot, bOnlyFail = True):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("操作记录", F"admin/meter_task/index/_afid/1096", {})
        soup = BeautifulSoup(resp.text,'lxml')

        #提取表内容
        trs = soup.find_all('tr')
        fileds = []

        #初始字段
        for x in trs[0].find_all('th'):
            fileds.append(x.string.replace("\xa0", ""))
        fileds.append("aliasname")          #电表别名
        fileds.append("data-id")            #任务编号
        fileds.append("data-state")         #任务状态
        fileds.append("data-update")        #任务更新
        fileds.append("data-time")          #任务下发时间
        fileds.append("data-logurl")        #任务日志url 
        fileds.append("命令状态")           #命令状态

        #提取行数据    
        pCmds_ok = pIot.iotInfo['命令']['已完成']        #命令操作已完成信息
        pCmds_doing = pIot.iotInfo['命令']['未完成']     #命令操作未完成信息
        rows = []
        for tr in trs[1:]:
            row = {'命令类型': 'meter', '命令状态': '', '执行时间': 0}
            tds = tr.find_all('td')
            for x in range(len(fileds) - 7):
                row[fileds[x]] = tr.contents[x*2 + 1].string
            if(pIot.iotId != row['采集器编号']):         #只提取相同
                continue

                #特殊属性信息提取
            if(len(tds) > 7):
                row['aliasname'] = tds[2].next.attrs['title']
                row['data-time'] = tds[4].next.attrs['title']
                row['data-id'] = tds[7].attrs['data-id']
                row['data-state'] = tds[7].attrs['data-state']
                row['data-update'] = tds[7].attrs['data-update']
                row['data-logurl'] = ""
                if(len(tds[8].contents) > 1):
                    row['data-logurl'] = ""
                    row['cmd-cancelurl'] = ""
                    for xx in tds[8].find_all('a'):
                        if(xx.string == '日志'):
                            row['data-logurl'] = xx.attrs.get('data-href', "")[1:]
                        elif(xx.string == '取消'):
                            row['cmd-cancelurl'] = xx.attrs.get('href', "")[1:]
                            row['命令状态'] = "doing"

            #命令完成状态判别
            if(row['状态'] in ['已完成', '已取消', '超时']):
                row['命令状态'] = myData.iif(row['状态'] == '已完成', "ok", "fail")
                row['执行时间'] = myData_Trans.Tran_ToTime(row['data-time'], "%Y-%m-%d %H:%M:%S")  

            #区分更新
            key = row['data-time']
            if(row['命令状态'] == "doing"):
                if(pCmds_doing.get(key, None) == None):
                    row['命令校检'] = {'校检次数': 0, '命令ID': row['data-id'], '命令状态': "doing", '校检提示': ""}
                    pCmds_doing[key] = row
                    self._iotCmds[key] = row            #传址同步修改值
            else:
                if(pCmds_ok.get(key, None) == None):
                    pCmds_ok[key] = row

                #剔除完成
                if(bOnlyFail ):
                    continue

            #缓存用于返回
            rows.append(row)
        return rows
    
    # Iot命令状态校检-所有执行中-重写按实际分类实现True
    def _checkIot_CmdsState_doing(self):
        #提取未完成操作编号集
        ids_Order = []
        ids_Meter = []
        for x in self._iotCmds:
            # 提取命令信息
            pCmd = self._iotCmds[x]
            pCheck = pCmd['命令校检']

            if(pCheck['命令状态'] == "doing"):
                if(pCmd['命令类型'] == 'order'):
                    ids_Order.append(pCmd['data-id']) 
                elif(pCmd['命令类型'] == 'meter'):
                    ids_Meter.append(pCmd['data-id']) 

        # 命令状态分类校检
        bRes = self._checkIot_CmdsState_doing_Order(ids_Order)
        bRes = bRes & self._checkIot_CmdsState_doing_Meter(ids_Meter)
        return bRes
    
    # Iot命令状态校检-Order
    def _checkIot_CmdsState_doing_Order(self, ids):
        return True
    # Iot命令状态校检-抄表
    def _checkIot_CmdsState_doing_Meter(self, ids):
        return True

    
    # 获取Iot电量信息
    def _getIot_Info_Power(self, pIot):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("查询电量", F"admin/card_opr/query_now/mid/{pIot.usrID}/q/power", {})
        soup = BeautifulSoup(resp.content.decode('unicode-escape'),'lxml')

        #提取基本信息内容
        res = myData_Trans.Tran_ToDict(soup.find('p').string)
        if(res['state'] == 'fail'):
            return False
        elif(res['state'] == 'success'):
            baseInfo['当前总电量'] = divs[1].find('label').string
            baseInfo['电量同步时间'] = divs[1].find('font').string

        info: "已成功添加任务 <br>&nbsp;&nbsp;请稍后刷新本页面或打开下方手动抄表界面等待抄表结果"
        #提取行数据    
        baseInfo = pIot.iotInfo
        baseInfo['当前总电量'] = divs[1].find('label').string
        baseInfo['电量同步时间'] = divs[1].find('font').string
        return baseInfo
    # 获取Iot费用信息
    def _getIot_Info_Money(self, pIot):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        #https://168.tqdianbiao.com/admin/card_opr/query_now/mid/1290780/q/money
        resp = self._DoWeb_Get("", F"admin/card_opr/index/tab/1/mid/{pIot.usrID}", {})
        soup = BeautifulSoup(resp.text,'lxml')

        #提取基本信息内容
        divs = soup.find_all('div')

        #提取行数据    
        baseInfo = pIot.iotInfo
        baseInfo['当前总电量'] = divs[1].find('label').string
        baseInfo['电量同步时间'] = divs[1].find('font').string
        return baseInfo


    # 初始物联网对象集
    def _Init_Iots(self, dir = ""):
        self.typeIot = "电表"
        self.Iots = myIOTs_Dianbiao(dir = dir)  



#主启动程序 
if __name__ == "__main__":    
    #添加Iot信息
    pIOT_Plat = myIOT_Plat_Dianbiao_tq()
    #pIOT_Plat.Add_Iot({'设备编号': '190801207866', '设备名称': '测试电表-01', '通讯地址': "190801207866", '用户名': 'zxc', '用户编号': '1290780', '日期': '2019-08-27 11:12:00'})
    #pIOT_Plat.Add_Iot({'设备编号': '190500004102', '设备名称': '测试电表-02', '通讯地址': "190500004102", '用户名': 'zxc', '用户编号': '1290799', '日期': '2019-08-27 11:12:00'})

    
    # 模拟登录
    pIOT_Plat.Login()

    # 电表控制-开合闸
    pIOT_Plat.Control_State('190801207866', 'open')
    

    exit(0)
    
    '''
    https://168.tqdianbiao.com/admin/card_opr/index/tab/1/mid/1290799
    https://168.tqdianbiao.com/admin/card_opr/index/tab/1/mid/1290780

    #新旧节点比对，提取执行任务编号 data-update="1"
    https://168.tqdianbiao.com/admin/ele_opration/index/mid/1290780/tab/4/controller/CardOpr
    https://168.tqdianbiao.com/admin/ele_opration/index/mid/1290799/tab/4/controller/CardOpr

    https://168.tqdianbiao.com/admin/ele_opration/state_update
    ids: 935143
    ids: 935221,935143
    ids: 935245
    '''
