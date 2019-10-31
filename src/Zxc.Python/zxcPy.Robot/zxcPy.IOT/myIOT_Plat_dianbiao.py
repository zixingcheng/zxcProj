#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-10-28 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    物联网IOT -智能物联网综合管理平台
"""

import sys, os, time
import re, requests
import mySystem
import urllib,urllib.parse,urllib.request,http.cookiejar 
from bs4 import BeautifulSoup


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myData_Trans, myIOT
from myWeb_urlLib import myWeb  



# 物联网IOT-电表对象
class myIOT_Dianbiao(myIOT.myIOT): 
    def __init__(self, dictSets = None):  
        super().__init__(id, dictSets)   

    # 转换为字典结构
    def Trans_ToDict(self, dictSets = None):  
        dictSets = super().Trans_ToDict(id, dictSets)   
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
        cookie_str = r'Av2dfsdf_admin_username=%E7%AE%80%E6%98%93%E7%94%9F%E6%B4%BB; Hm_lvt_2510c71771575460d26bb883a51bde54=1571463497,1572248265,1572361282,1572414162; Av2dfsdf_language=zh-CN; sign=qtkkoajhh292bm9fqr5daak99m; Hm_lpvt_2510c71771575460d26bb883a51bde54=1572485723'

        #固定模拟登陆网址参数
        urlLogin = "admin/public/login"
        urlDoLogin = "admin/public/dologin"
        url_img_code = "index.php?g=admin&m=checkcode&a=index&length=4&font_size=25&width=235&height=52&use_noise=1&use_curve=0&time=Math.random()"
        super().Login(urlLogin , urlDoLogin, url_img_code, cookie_str)  
        
    # 控制--状态
    def Control_State(self, state = ""):
        if(state not in self.ctrlStates): return False

        #分类型操作
        if(state == "open"):
            resp = self._DoWeb_Get("", "admin/card_opr/pull_on_off/mid/1290780/action/pull_on", {})
            self._getTable_Actions("1290780")
        pass
        return True
    

    # 查询操作记录列表（区分是否已经完成更新）
    def _getTable_Actions(self, id, bUpdated = True):
        #使用BeautifulSoup解析代码,并锁定页码指定标签内容
        resp = self._DoWeb_Get("", F"admin/ele_opration/index/mid/{id}/tab/4/controller/CardOpr", {})
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

        #提取行数据    
        rows = []
        for tr in trs[1:]:
            row = {}
            tds = tr.find_all('td')
            for x in range(len(fileds) - 6):
                row[fileds[x]] = tds[x].string

                #特殊属性信息提取
                row['aliasname'] = tds[1].next.attrs['title']
                row['data-time'] = tds[4].next.attrs['title']
                row['data-id'] = tds[7].attrs['data-id']
                row['data-state'] = tds[7].attrs['data-state']
                row['data-update'] = tds[7].attrs['data-update']
                row['data-logurl'] = ""
                if(len(tds[9].contents) > 1):
                    row['data-logurl'] = tds[9].contents[1].attrs.get('data-href', "")

            #区分更新
            if(bUpdated):
                if(row['data-update'] == '0'):
                    continue
            rows.append(row)
        return rows

    # 初始物联网对象集
    def _Init_Iots(self, dir = ""):
        self.typeIot = "电表"
        self.Iots = myIOTs_Dianbiao(dir = dir)  



#主启动程序 
if __name__ == "__main__":    
    #添加Iot信息
    pIOT_Plat = myIOT_Plat_Dianbiao_tq()
    pIOT_Plat.Add_Iot({'设备编号': '190801207866', '设备名称': '测试电表-01', '通讯地址': "190801207866", '用户名': 'zxc', '用户编号': '1290780', '日期': '2019-08-27 11:12:00'})
    pIOT_Plat.Add_Iot({'设备编号': '190500004102', '设备名称': '测试电表-02', '通讯地址': "190500004102", '用户名': 'zxc', '用户编号': '1290799', '日期': '2019-08-27 11:12:00'})

    
    # 模拟登录
    pIOT_Plat.Login()
    pIOT_Plat.Control_State('open')
    

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
