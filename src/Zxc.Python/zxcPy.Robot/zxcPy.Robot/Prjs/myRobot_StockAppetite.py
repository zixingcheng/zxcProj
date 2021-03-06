#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-08-30 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--股票偏好(群信息统计)
"""
import sys, string, ast, os, time, datetime, random, mySystem
from urllib.parse import quote
from decimal import Decimal

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("../Prjs/Base", False, __file__)
mySystem.Append_Us("", False) 
import myDebug, myData, myData_Trans, myRobot, myIO, myAI_Baidu, myWeb_urlLib
import myRobot_Robot, myManager_Msg, myDataDB_StockReturns
from myGlobal import gol   

    
#机器人类--股票偏好(群信息统计) 
class myRobot_StockAppetite(myRobot.myRobot):
    def __init__(self, usrID = "", usrName = ""):
        super().__init__(usrID, usrName)
        self.doTitle = "Robot_StockAppetite"     #说明 
        self.prjName = "股票偏好"                #功能名
        self.doCmd = "@@zxcRobot_StockAppetite"  #启动命令 
        self.isBackUse = True                    #后台运行
        self.maxTime = -1                        #永久有效 
                
    #消息处理接口
    def _Done(self, Text, msgID = "", msgType = "TEXT", usrInfo = {}):
        #按消息类型处理
        msgType = msgType.upper()
        strReturn = ""
        if(msgType == "TEXT") :
            strReturn = self._Done_Text(Text, msgID, usrInfo)
        elif(msgType == "PICTURE") :
            strReturn = self._Done_Image(Text, msgID, usrInfo)
            pass
        return strReturn 
    
    #消息处理接口-Text
    def _Done_Text(self, Text, msgID = "", usrInfo = {}):
        #提取命令内容@*
        if(Text.count("@*") != 1): return ""
        cmds = Text.strip()[2:].split(" ")
        cmd = cmds[0].strip()
        nNum = len(cmds)
        myDebug.Print(Text.strip())
        
        #命令处理
        strReturn = ""
        if(cmd == "帮助"):
            return self._Title_Helper()  
        elif(cmd == "排名"):
            if("墨紫" == usrInfo.get('usrNameNick', "")):  
                #提取排名信息
                pDB = gol._Get_Setting('zxcdbStockReturns')
                nTop = 10
                if(len(cmds) > 1 and myData_Trans.Is_Numberic(cmds[1])):
                    nTop = myData_Trans.To_Int(cmds[1])
                lstRanks = pDB.Get_Ranks(nTop = nTop)
                strRanks = "年收益排名(" + str(datetime.datetime.now().year) + ")：" + myData_Trans.Tran_ToStr(lstRanks, "\r\n")
                return strRanks
        return strReturn
        
    #匹配指定字符集
    def Matching_strs(self, Text, usrWords = {}):
        for x in usrWords.keys():
            num = int(usrWords[x])
            if(Text.count(x) != num):
                return False
        return True

    #消息处理接口-Image
    def _Done_Image(self, Text, msgID = "", usrInfo = {}):
        #图片判别，只处理手机截图（图片行列比）

        #提取图片内容,ORC通用识别
        #Text = "E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.All.Base\\Temps\\Images\\Test.png"
        txtInfo = myAI_Baidu.ORC(Text, "", out_debug=False)
        myDebug.Debug(str(txtInfo))

        #按文字内容组合定义图片类型
        dictInfos = {'收益率':"", '日期':""}
        num = txtInfo['wordText'].count('资产分析')
        if(num >= 1):            
            # 使用文字匹配方式解析
            year = myData_Trans.Tran_ToTime_str(None, "%Y") 
            if(txtInfo['wordText'].count('同花顺-资产分析') == 1):     #同花顺截图
                #'u中国联通令\n下午3:10\n64%\n同花顺-资产分析\n2019-01-01~2019-08-27\n分享\n本月\n近三月\n近半年\n今年\n近两年\n30.0%\n10.0%\n0.0%\n-10.0%\n01-01\n04-01\n07-01\n我上证○深证○创业板○上证50\nC沪深30中证500收益走势\n今年跑嬴上证指数\n23.03%\n我\n3940%\n上证\n16.37%\n深证\n30.43%\n创业板\n30.19%' 
                ind = txtInfo['words'].index('我')
                if(ind > 0):
                    txt = txtInfo['words'][ind + 1]
                    dictInfos['收益率'] = float(txt.replace('%', "")) / 100
                    if(txt.count('.') == 0): 
                        dictInfos['收益率'] = dictInfos['收益率'] / 100   #小数点未正确识别修正
                        
                    # 提取日期
                    lst = [n for n in txtInfo['words'] if n.count(year)==2]
                    if(len(lst) == 1):
                        times = lst[0].split('~')
                        if(times[0][0:10] == year + "-01-01"):  #日期校检，必须当年开始
                            dictInfos['日期'] = myData_Trans.Tran_ToDatetime(times[1], '%Y-%m-%d')
                pass
            else:   #君弘截图
                #'10:09:1l\n(80\n资产分析\n20190101~20190828\n今年收益率17.48%\n今日本月近三个月近半年今年2018\n30%\n20%\n2019.01.31\n我:-0.11\n10%\n上证:3.64%\n10%\n01.31\n03.29\n05.31\n07.31\n●我○上证深证○创业\n1.46%\n跑赢上证\n1.46%\n跑输深证\n-12.56%\n跑输创业\n-12.47%\n资产分析\n证券分析\n月度分析\n账单'
                # 提取今年收益率
                lst = [n for n in txtInfo['words'] if n.count('今年收益率')==1]
                if(len(lst) == 1):
                    txt = lst[0]
                    dictInfos['收益率'] = float(txt.replace('今年收益率', "").replace('%', "")) / 100
                    if(txt.count('.') == 0): 
                        dictInfos['收益率'] = dictInfos['收益率'] / 100   #小数点未正确识别修正

                    # 提取日期
                    lst = [n for n in txtInfo['words'] if n.count(year)==2]
                    if(len(lst) == 1):
                        times = lst[0].split('~')
                        if(times[0][0:8] == year + "0101"):  #日期校检，必须当年开始
                            dictInfos['日期'] = myData_Trans.Tran_ToDatetime(times[1], '%Y%m%d')
                pass
            if(dictInfos['收益率'] == 0): return ""

            # 修正日期为字符串、收益率格式等
            usrName = usrInfo.get('usrNameNick', "") 
            usrProfit = dictInfos['收益率']
            if(dictInfos.get('日期', "") != ""):
                dictInfos['日期-前'] = myData_Trans.Tran_ToDatetime_str(dictInfos['日期'] + datetime.timedelta(days=1), '%Y-%m-%d')
                dictInfos['日期'] = myData_Trans.Tran_ToDatetime_str(dictInfos['日期'], '%Y-%m-%d')
            if(dictInfos.get('收益率', "") != ""):
                dictInfos['收益率'] = str(Decimal((usrProfit * 100)).quantize(Decimal('0.00'))) + "%"

            #记录信息
            pDB = gol._Get_Setting('zxcdbStockReturns')
            lstQuery = pDB.Query("isDel==False && 日期>=" + dictInfos['日期-前'], "日期", True)
            if(len(lstQuery) > 0): return ""    #必须比已有日期大
            myDebug.Debug(pDB.Add_Row({'用户名': usrName, '收益': usrProfit, '日期': dictInfos['日期']}, True))
            
            #组装返回
            lstR = pDB.Get_Ranks(usrName, True)
            if(len(lstR) < 1):
                return "@" + usrName + " 收益信息记录失败！当前收益率：" + dictInfos['收益率'] + "."
            dicRand = lstR[0]
            strRank = " 您的收益排名：第 " + dicRand['ranking'] + ", 收益率：" + dicRand['profit'] + " "
            return "@" + usrName + " " + strRank
        return ""
    
    def _Title_User_Opened(self): 
        return "自动处理所有股票偏好消息..."
    def _Title_Helper(self): 
        strReturn = "消息命令提示："
        strReturn += self.perfix + "@￥帮助：输出所有命令说明"
        strReturn += self.perfix + "@￥：输入君弘APP截图自己记录." 
        strReturn += "\n命令参数以空格区分，如：\"@￥帮助\""
        return strReturn
        
""" IORC接口有调用总限制，改为通用文件进行匹配解析
            if(myData.Matching_strs(txtInfo['wordText'], {"今年": 2, "近半年": 1, "本月": 1, "近三": 1})):
                if(num == 2):       #君弘截图
                    #'10:09:1l\n(80\n资产分析\n20190101~20190828\n今年收益率17.48%\n今日本月近三个月近半年今年2018\n30%\n20%\n2019.01.31\n我:-0.11\n10%\n上证:3.64%\n10%\n01.31\n03.29\n05.31\n07.31\n●我○上证深证○创业\n1.46%\n跑赢上证\n1.46%\n跑输深证\n-12.56%\n跑输创业\n-12.47%\n资产分析\n证券分析\n月度分析\n账单'
                    #'10:09i\n@(80\n资产分析\n20190101~20190828\n今年收益率17.48%\n今日本月近三个月近半年今年2018\n30%\n20%\n2019.01.31\n我:-0.11%\n10%\n上证:3.64%\n10%\n01.31\n03.29\n05.31\n07.31\n我\n上证\n深证\n○创业\n1.46%\n跑嬴上证\n1.46%\n跑输深证\n-12.56%\n跑输创业\n-12.47%\n资产分析\n证券分析\n月度分析\n账单'
                    imageInfo = myAI_Baidu.IORC(Text, "18ed022a1b51ef96b130bd4226b89f64", out_debug=False)
                    dictInfos['收益率'] = imageInfo['收益率']['word'].replace('今年收益率', "").replace('%', "")
                    times = imageInfo['时间段']['word'].split('~')
                    if(times[0][0:4] == times[1][0:4]):
                        dictInfos['日期'] = myData_Trans.Tran_ToDatetime(times[1], '%Y%m%d')
                elif(num == 1 and txtInfo['wordText'].count('同花顺-资产分析') == 1):     #同花顺截图
                    #'u中国联通令\n下午3:10\n64%\n同花顺-资产分析\n2019-01-01~2019-08-27\n分享\n本月\n近三月\n近半年\n今年\n近两年\n30.0%\n10.0%\n0.0%\n-10.0%\n01-01\n04-01\n07-01\n我上证○深证○创业板○上证50\nC沪深30中证500收益走势\n今年跑嬴上证指数\n23.03%\n我\n3940%\n上证\n16.37%\n深证\n30.43%\n创业板\n30.19%' 
                    imageInfo = myAI_Baidu.IORC(Text, "c0f24215c88dcee9c9f5111238b31c96", out_debug=False)
                    dictInfos['收益率'] = imageInfo['收益率']['word'].replace('%', "")
                    times = imageInfo['时间段']['word'].split('~')
                    if(times[0][0:4] == times[1][0:4]):
                        dictInfos['日期'] = myData_Trans.Tran_ToDatetime(times[1], '%Y-%m-%d') 
"""


#主启动程序
if __name__ == "__main__": 
    #消息处理
    pRobot_Stock = myRobot_StockAppetite()
    pRobot_Stock.Done("@@zxcRobot_StockAppetite")
    
    #组装请求
    usrInfo = {}
    noteMsg = {}
    if(True):
        usrInfo["usrID"] = "zxcID"
        usrInfo["usrName"] = "zxcName"
        usrInfo["usrNameNick"] = "茶叶一主号"
        usrInfo['usrNameSelf'] = ""             #自己发自己标识 
        usrInfo["groupID"] = ""
        usrInfo["groupName"] = "" 


    #图片自动处理
    myDebug.Debug(pRobot_Stock.Done("E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.All.Base\\Temps\\Images\\Test4.jpg", msgType = "PICTURE", usrNameNick='茶叶一主号',)['msg'])  
    myDebug.Debug(pRobot_Stock.Done("E:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.All.Base\\Temps\\Images\\Test.png", msgType = "PICTURE", usrNameNick='茶叶一主号',)['msg'])  

    #排名
    pRobot_Stock.Done("@*排名", usrNameNick='墨紫')  
    pRobot_Stock.Done("@*排名 1")   


    #退出
    pRobot_Stock.Done("@@zxcRobot_StockAppetite")
    print()
    
