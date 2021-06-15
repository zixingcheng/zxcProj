#-*- coding: utf-8 -*-
"""
Created on  张斌 2021-01-24 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的数据交换接口实现
"""
import sys, os, ast, re, copy, threading, mySystem  
import time, datetime 

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类  
mySystem.Append_Us("", False) 
import myDebug, myData, myData_Trans, myData_Json, myError, myIO
from myGlobal import gol 



#数据交换类-文件交换
class myData_Swap_FileIO():
    def __init__(self, tagName, dirSwap, stepSwaps = 1, delayedTime = 0, useAck = True, nameSwap = 'zxcTest', isSender = False, dirSwap_out = ""):
        self.tagName = tagName
        self.nameSwap = nameSwap 
        self.dirSwap = dirSwap
        self.dirSwap_out = myData.iif(dirSwap_out == "", dirSwap, dirSwap_out)
        self.stepSwaps = stepSwaps
        self.isSender = isSender
        self.useAck = useAck
        self.dirSwap_back = dirSwap + "_back/" + tagName
        self.delayedTime = delayedTime 
        
        self.dataOut = []
        self.ackDict = {}
        self.ackInfo = {"isAcked": False, "time": None, "retrys": 0, "path": ""}
        self.functionDict = {}
        self.funChange = None
        
    #初始交换设置    
    def Init_Swap(self, tagName = "", isAuto_ack = True):
        if(tagName != ""):
            self.tagName = tagName
        self.useAck = isAuto_ack

    # 文件交换-in
    def SwapData_In(self, nStepSwaps = 1): 
        nums = 0
        lstDatas = []
        nStepSwaps = myData.iif(nStepSwaps <= 0 , sys.maxsize, nStepSwaps)
        lstFiles = myIO.getFiles(self.dirSwap, wildcard = ".json", iswalk = False)
        if(len(lstFiles) < 1): return lstDatas

        myDebug.Print("DataSwap IOFiles::")
        myDebug.Print("\t" + self.dirSwap)
        myDebug.Print("\tSwap IOFiles(" + str(len(lstFiles)) + ")");
        for file in lstFiles:
            fileName = myIO.getFileName(file, True)
            if(fileName[0: len(self.tagName)] != self.tagName): continue;
            if(self.checkNeedAck(fileName)): continue;

            # 超时校检
            if (self.delayedTime > 0):      #解析时间并校检
                timeTag = fileName[len(self.tagName)+1:]
                timeData = myData_Trans.Tran_ToDatetime(timeTag, "%Y-%m-%d-%H-%M-%S")
                dtNow = datetime.datetime.now()
                if((dtNow - timeData).seconds > self.delayedTime):
                    self.SwapData_BackUp(file);
                    continue;

            #读取文件内容
            myDebug.Print("\tnew file swap:: " + myIO.getFileName(file, False));
            strJson = myIO.getContent(file, noBOM = True)
            pJson = myData_Json.Json_Object()
            pJson.Trans_FromStr(strJson)

            #组装交换信息
            data = {"path": file, "fileInfo": pJson._dict_}
            lstDatas.append({"tagAck": fileName, "data": data})

            #记录Ackinfo
            if(self.useAck):
                ackInfo = {"isAcked": False, "time": datetime.datetime.now(), "retrys": 0, "path": file}
                self.ackDict[fileName] = ackInfo
            else:
                self.SwapData_BackUp(file);

            nums += 1
            if (nums >= nStepSwaps): break;

        myDebug.Print("DataSwap IOFiles End." + "\tMargin Swap IOFiles(" + str(len(lstFiles) - len(lstDatas)) + ")\n");
        return lstDatas;
    # 文件交换-out
    def SwapData_Out(self, dictData): 
        msg = copy.copy(dictData)
        msg['msg'] = msg['msg'].replace("\r", "※r※").replace("\n", "※n※").replace('"', "※i※").replace("\t", "※t※")
        msg['msgContent'] = msg.get('msgContent',"").replace("\r", "※r※").replace("\n", "※n※").replace('"', "※i※").replace("\t", "※t※")
        self.dataOut.append(msg)
    # 文件交换输出-out
    def SwapData_OutFile(self, tagName = "", dirDest = ""): 
        dataOut = copy.copy(self.dataOut)
        self.dataOut = []
        if(len(dataOut) < 1): return False
        jsonData = myData_Json.Json_Object(dataOut)

        dirOut = myData.iif(dirDest != "", dirDest, self.dirSwap_out) + "/" 
        if(tagName == ""): tagName = self.tagName
        if(tagName == "" and dirOut == ""): return False

        fileName = tagName + myData_Trans.Tran_ToDatetime_str(None, "_%Y_%m_%d_%H_%M_%S") + ".json"
        content = jsonData.ToString(autoFormat = False).replace("\\", "/")
        myIO.Save_File(dirOut + fileName, content, True, False);
        #myDebug.Print("DataSwap Out IOFiles::" + dirOut + fileName)
        myDebug.Print("DataSwap Out IOFiles::" + fileName)
        return True

    # 交换文件备份
    def SwapData_BackUp(self, path, dir = ""): 
        fileName = myIO.getFileName(path, False)
        if(dir == ""): dir = self.dirSwap_back
        destDir = dir + "/" + fileName[len(self.tagName)+1: len(self.tagName)+11];

        try:
            myIO.mkdir(destDir, False, False)
            if(os.path.exists(destDir + "/" + fileName) == False):
                myIO.copyFile(path, destDir, fileName, False)
            if(os.path.exists(destDir + "/" + fileName)):
                os.remove(path)
        except :
            pass

        
    # 判断是否需要确认
    def checkNeedAck(self, fileName): 
        if(self.useAck == False): return False
        ackInfo = self.ackDict.get(fileName, None)
        if(ackInfo == None): return False

        bAcked = False
        if(ackInfo["isAcked"]): 
            bAcked = True
            self.SwapData_BackUp(ackInfo["path"])
        else:
            dtNow = datetime.datetime.now()
            if((dtNow - ackInfo["time"]).seconds > 10):
                ackInfo["time"] = dtNow
                ackInfo["retrys"] += 1
            else:
                bAcked = True

            # 重试过多则忽略
            if(ackInfo["retrys"] > 10):
                bAcked = True   
                self.SwapData_BackUp(ackInfo["path"])
        return bAcked
    # 交换数据确认
    def ackDataSwap(self, ackInfo): 
        if(ackInfo == None): return False
        fileName = ackInfo.get("tagAck", None)
        if(fileName == ""): return False

        if(self.useAck == False): return False
        ackInfo = self.ackDict.get(fileName, None)
        if(ackInfo == None): return False

        ackInfo["isAcked"] = True;
        ackInfo["timeAcked"] = datetime.datetime.now()

    # 开始 
    def startSwap(self):
        self.isRuning = True
        self.thrd_Handle = threading.Thread(target = self.thrdDataSwap)
        self.thrd_Handle.setDaemon(False)
        self.thrd_Handle.start()
    # 停止 
    def closeSwap(self):
        self.isRuning = False
        self.thrd_Handle.stop()
    # 交换-线程实现
    def thrdDataSwap(self):
        nSleep = 0.5
        sumSleep = 0
        while(True):
            try:
                if(self.isSender):
                    # 交换文件夹变化监测
                    lstData = self.SwapData_In(self.stepSwaps)
                
                    # 触发变化事件
                    if(len(lstData) > 0):
                        self.funChange(lstData)
                time.sleep(nSleep)
                sumSleep += nSleep

                # 保存输出
                if(sumSleep > 1):
                    sumSleep = 0
                    self.SwapData_OutFile()
            except Exception as ex:
                myDebug.Error(str(ex))
                time.sleep(nSleep)
                pass 
            
    # 变动信息装饰函数
    def changeDataSwap(self):
        # 定义一个嵌套函数
        def _change(fn):
            self.funChange = fn
        return _change



#主启动程序
if __name__ == "__main__":
    gol._Init()             #先必须在主模块初始化（只在Main模块需要一次即可）
    gol._Set_Setting("CanPrint_Debug", True)
    
    # 装饰函数，文件变动触发
    pDataSwap = myData_Swap_FileIO("Quote", "D:/myCode/zxcProj/src/Zxc.Python/zxcPy.Robot.Spider/Data/Swaps")
    @pDataSwap.changeDataSwap()
    def Reply(lstData): 
        for x in lstData:
            print(lstData)
            pDataSwap.ackDataSwap(x)
            pass

    #文件交换处理
    pDataSwap.SwapData_In(1)
    pDataSwap.startSwap();

    print()

