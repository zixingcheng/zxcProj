# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-02 16:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Web操作模拟类
    @依赖库： urllib
"""
from requests import get, put, post, delete
import urllib,urllib.request
import http.cookiejar
import myDebug;

class myWeb:
    #初始构造 
    def __init__(self, Host = "http://127.0.0.1",Path = '',bPrint = True):
        self.Host = Host
        self.Path = Path
        self.Referer = Host + "/" + Path
        self.canPrint = bPrint
        
        #声明一个CookieJar对象实例来保存cookie
        self.cookie = http.cookiejar.CookieJar()

        #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
              
        #通过handler来构建opener
        self.opener = urllib.request.build_opener(self.handler)
        
    #定义param
    def __set_param__(self , Path): 
        self.Path = Path
        self.Referer =self.Host + "/" + Path
    #定义cookies
    def __set_cookies__(self , Path): 
        self.Path = Path
        self.Referer =self.Host + "/" + Path
        
    #定义Post方法
    def Do_Post(self, Path , strPostData, strTag = "", bUseHeaders = True, bInitCookie = False):
        self.__set_param__(Path)    #更新属性
        
        #urlencode转换，并强制为UTF8
        if(self.canPrint):
            myDebug.Debug("请求" + strTag + "页面：" + self.Referer)
        postdata = urllib.parse.urlencode(strPostData) 
        postdata = postdata.encode(encoding='UTF8')

        
        #模拟浏览器头
        header = ""
        if(bUseHeaders == True):
            user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)'
            header = {'User-Agent': user_agent}        

            
        #Cookie初始(强制)
        #urllib.request.install_opener(self.opener)  #初始cookie的handler
        if(bInitCookie == True):         
            self.opener = urllib.request.build_opener(self.handler)     # 通过handler来构建opener
            myDebug.Debug("    页面Cookie重建") 
        else:     
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))    # 利用urllib2的build_opener方法创建一个opener
            if(self.canPrint):
                myDebug.Debug("    页面Cookie重置ok") 
            
        #构造Requset
        request= urllib.request.Request( 
                   url = self.Referer, 
                   data = postdata, 
                   headers = header)
            
        #请求响应 
        #response = urllib.request.urlopen(request) 
        if(self.canPrint):
            myDebug.Debug("    页面请求中。。。") 
        response = self.opener.open(request)         

             
        #此处的open方法同urllib2的urlopen方法，也可以传入request
        #response = self.opener.open('http://www.baidu.com')
        for item in self.cookie:
            myDebug.Debug('Name = '+ item.name)
            myDebug.Debug('Value = '+ item.value)

        #更新相关记录信息，并返回相应
        page = response.read()
        self.status = response.status
        self.reason = response.reason 
        if(self.status == 200 or self.reason.tolower() == "ok"):
            if(self.canPrint):
                myDebug.Debug("    请求完毕。")
        else:
            if(self.canPrint):
                myDebug.Debug("    请求出错。")
        print("") 
        return page
    
    #定义rest API方法Get方法
    def Do_API_get(self, Path , strTag = ""):
        self.__set_param__(Path)    #更新属性

        #测试get
        try:
            if(self.canPrint):
                myDebug.Debug("请求" + strTag + "页面：" + self.Referer)
            request = get(self.Referer)
            return request.text
        except:
            pass
        return ""
        
    #定义web页面元素获取方法
    def Get_EleStr(self, strSource, strFliter_S, strFliter_E):
        strInfo = strSource
        nStart = strInfo.find(strFliter_S) + len(strFliter_S)
        nEnd = strInfo.find(strFliter_E, nStart )
        strInfo = strInfo[nStart: -1]
        strData = strInfo[0: nEnd - nStart]
        
        #print(nStart )
        #print(nEnd - nStart - 1)
        #print(strInfo)
        #print(strData)
        return strData
        

    #登录信息  
    #strLoginInfo = { 
    #    'method':'login', 
    #    'username':'zhangbin', 
    #    'pwd':'zxc123' 
    #    }
    #
    #r = Do_Post ("http://192.168.29.31:7003/ams//util/sys/login.do",strLoginInfo,True)
    #print(r.read().decode("UTF8"))
 
 
#主启动程序 
if __name__ == "__main__":
    pWeb = myWeb("http://hq.sinajs.cn/")
    aa = pWeb.Do_Post("list=sh600006,sh510050", "",)
    bb = aa.decode(encoding = "gbk")
    print(bb)
    
    pWeb = myWeb("http://127.0.0.1:8668")
    aa = pWeb.Do_API_get("weixin/茶叶一主号/网页测试py-0/TEXT", "",)
    print(aa)

    
    pWeb = myWeb("http://127.0.0.1:8668/zxcAPI/robot")
    robotPath = "reply/{'usrName': '信阳毛尖--杨帆桥', 'msgID': '', 'msg': '宝宝', 'usrNameNick': '信阳毛尖--杨帆桥', 'usrID': '@c1744fd767656b64a495d7cabeb1041674dec223e5de0438def46d78b6c90f2b','msgType': 'TEXT', 'plat': 'wx', 'groupID': ''}"
    strReturn = pWeb.Do_API_get(robotPath, "zxcAPI-py")
    print(strReturn)