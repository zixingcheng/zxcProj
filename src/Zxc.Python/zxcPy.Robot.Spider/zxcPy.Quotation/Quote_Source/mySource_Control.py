#-*- coding: utf-8 -*-
"""
Created on  张斌 2020-06-23 18:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    行情爬取--统一源类(多源) 
"""
import sys, copy, os, time, mySystem 
import threading

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../../zxcPy.Setting", False, __file__)
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Listener')
mySystem.Append_Us("", False)    
import myIO, myData_Trans, myData_Json, myDebug
import mySpider_Setting, myQuote, myQuote_Data, myData_Stock, myQuote_Listener, myQuote_Source  
import mySource_Sina_Stock, mySource_JQData_Stock



#行情源--控制
class Source_Control(myQuote_Source.Quote_Source):
    def __init__(self, params = ""):
        myQuote_Source.Quote_Source.__init__(self, params, 'Control')                 #设置类型

        #初始行情源对象(多源)
        self.srcQuotes = {}
        self.setsStock = gol._Get_Value('setsStock', myQuote.myStocks())              #标的信息
        self.srcQuotes['SinaAPI'] = gol._Get_Value('quoteSource_Sina', None)          #新浪源
        self.srcQuotes['JqDataAPI'] = gol._Get_Value('quoteSource_JqData', None)      #聚宽源

    def _Stoped(self):
        return False 
        
    #添加监听
    def addListener(self, listener):
        for x in self.srcQuotes.keys():
            self.srcQuotes[x].addListener(listener)


    #查询行情
    def query(self, checkTime = True, nReturn = 0, params = None): 
        apiQuote = self.getQuoteAPI(params)
        if(apiQuote != None):
            return apiQuote.query(checkTime, nReturn, params)
        return []
    #查询行情-历史
    def queryHistory(self, checkTime = True, nReturn = 0, params = None): 
        apiQuote = self.srcQuotes['JqDataAPI']
        if(apiQuote != None):
            return apiQuote.query(checkTime, nReturn, params)
        return []
    
    #提取行情API对象
    def getQuoteAPI(self,parms = None): 
        typeAPI = "SinaAPI"
        if(parms != None and parms.get('typeAPI', '') != ""):
            typeAPI = parms.get('typeAPI', 'SinaAPI')
        return self.srcQuotes.get(typeAPI, self.srcQuotes['SinaAPI'])
     

    
#行情监听线程
class Quote_Thread(threading.Thread):
    def __init__(self, source, intervalSecs = 3):
        self.source = source
        self.interval = intervalSecs
        self.threadRunning = False
        self.stopped = False
        threading.Thread.__init__(self)

        #初始根目录信息
        strDir, strName = myIO.getPath_ByFile(__file__)
        self.Dir_Base = os.path.abspath(os.path.join(strDir, "../.."))  
        self.Dir_Swaps = self.Dir_Base + "/Data/Swaps/"
        
    def getParams(self):
        setsSpider = gol._Get_Value('setsSpider')       #实例 爬虫设置 
        lstStock = setsSpider._Find_ByTypes("quote")

        lstIDs = []
        for x in lstStock:
            if(x.IsValid()):
                lstIDs.append(x.spiderName)
        if(len(lstIDs) < 1): return None

        stockIds = myData_Trans.Tran_ToStr(lstIDs).replace(".", "")
        parms = {"queryIDs": stockIds}
        return parms
    def run(self):
        time.sleep(10)   
        myDebug.Print("Spider Quote Thread Start...")
        while(self.source.setTime() == False):
            time.sleep(30)   
            #myDebug.Print('Spider Quote Stoped.\n         -- not quote time.\n')
            #myDebug.Print("nSpider Quote Thread ReStart...")
            #self.stop()
            #return 

        myDebug.Print('Spider Quote Run...')
        self.threadRunning = True;
        while self.threadRunning:
            try:
                #发生错误时继续
                parms = self.getParams();
                lstReturn = self.source.query(params = parms) 
                self.output(lstReturn)
                time.sleep(self.interval)   

                #判断结束
                if(self.source._Stoped()):
                    break
            except Exception as ex:
                pass
        self.stop()
    def stop(self):
        myDebug.Print('Spider Quote Stoped\n')
        self.threadRunning = False
        self.stopped = True
        time.sleep(2)

    #输出到文件用于交换
    def output(self, lstReturn):
        pMsg = copy.deepcopy(gol._Get_Setting('Return_strFormat', {}))
        if(lstReturn != None and len(lstReturn) > 1):
            datas = []
            for x in lstReturn:
                datas.append(x.toDict())
            pMsg['datas'] = datas
            pMsg['result'] = True

            strJson = myData_Json.Trans_ToJson_str(pMsg);
            path = self.Dir_Swaps + "/Quote_" + myData_Trans.Tran_ToDatetime_str(None, "%Y-%m-%d-%H-%M-%S") + ".json"
            myIO.Save_File(path, strJson, isUtf = True, isNoBoom = True)
            return True
        return False

#缓存全局对象
from myGlobal import gol 
gol._Init()                 #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Value('quoteSource', Source_Control())   #实例 行情对象
quoteSource = gol._Get_Value('quoteSource')



#线程执行-行情监测
def quoteStart():
    global quoteSource
    if(quoteSource == None):
        quoteSource = initSource()
        
    thrdQuote = gol._Get_Value('quoteSourceThread', None)
    if(quoteSource != None and (thrdQuote == None or thrdQuote.threadRunning == False)):
        thrdQuote = Quote_Thread(quoteSource)
        thrdQuote.setDaemon(True)
        thrdQuote.start()
        gol._Set_Value('quoteSourceThread', thrdQuote)
#初始行情数据源
def initSource(addListener = True):
    #初始全局行情对象
    pQuoteSrc = gol._Get_Value('quoteSource', None)
    if(pQuoteSrc == None):
        pQuoteSrc = Source_Control()
        gol._Set_Value('quoteSource', pQuoteSrc)    #实例 行情对象
        
    #添加监听对象
    if(addListener):
        import myListener_Printer
        pQuoteSrc.addListener(myListener_Printer.Quote_Listener_Printer())
    return pQuoteSrc




#主启动程序
if __name__ == "__main__":
    import myListener_Printer
    pSource = gol._Get_Value('quoteSource')
    pSource.addListener(myListener_Printer.Quote_Listener_Printer())
    
    # 单独查询，不纪录
    qd = pSource.query(False, 1, {"typeAPI" : "", "queryIDs" : "sh510050"}) 
    qd = pSource.queryHistory(False, 1, {'dataFrequency': "1d", 'stockBars': 1, 'stockTag': "10003418.XSHG"})
    qd = pSource.queryHistory(False, 1, {'dataFrequency': "1d", 'datetimeStart': "2021-06-23 09:00:00", 'stockTag': "10003418.XSHG"}) 

    #线程执行   
    quoteStart()

    # 通用查询，并记录
    while True:
        #pSource.query() 
        time.sleep(5)


