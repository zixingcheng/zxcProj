#-*- coding: utf-8 -*-
"""
Created on  张斌 2019-09-17 22:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    
    自定义简易库表操作-股票收益
"""
import sys, os, time, copy, datetime, mySystem
from collections import OrderedDict
from operator import itemgetter, attrgetter
from decimal import Decimal

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("", False) 
import myEnum, myIO, myIO_xlsx, myData, myData_DB, myData_Trans, myDebug 



# 自定义简易库表操作-股票收益 
class myDataDB_StockReturns(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB_StockReturns", dir = ""):  
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Data/"
            myIO.mkdir(self.Dir_DataDB, False) 
        super().__init__(nameDB, self.Dir_DataDB, True) 
        

    # 检查是否相同--继承需重写  
    def _IsSame(self, rowInfo, rowInfo_Base): 
        bResult, sameID = super()._IsSame(rowInfo, rowInfo_Base)
        if(bResult): return bResult, sameID

        if(rowInfo['用户名'] == rowInfo_Base['用户名']):
            if (rowInfo['日期'] - rowInfo_Base['日期']).days < 1:
               return True, sameID
        return False, sameID
    
    #单条有效修正
    def _Check_oneValid(self, rowInfo): 
        if(rowInfo.get('用户名', '') != ""):
            datas = self._Find_ByFliter("用户名", '== ' + rowInfo['用户名'])
            for x in datas:
                datas[x]['isDel'] = True
        return True

    #转换行格子数据为日期类型 "%Y-%m-%d"
    def _Trans_Value_Datetime(self, value):  
        if(value.count(":") == 2):
            return myData_Trans.Tran_ToDatetime(value)
        return myData_Trans.Tran_ToDatetime(value, "%Y-%m-%d")
    
    #获取排名-所有或单一
    def Get_Ranks(self, usrID = '', bOnlyRank = False, nTop = 1024):  
        # 获取所有
        datas = self.Query("isDel==False", "收益", True)
       
        # 循环组装排名
        ind = 1
        ranks = []
        for x in datas:
            data = x[1]
            if(usrID == "" or usrID == data['用户名']):
                if(bOnlyRank == False):
                    strRank = "第" + str(ind) + "名：" + data['用户名'] + "(" + str(Decimal((data['收益'] * 100)).quantize(Decimal('0.0'))) + "%)"
                else:
                    strRank = {'name': data['用户名'], 'ranking': str(ind), 'profit': str(Decimal((data['收益'] * 100)).quantize(Decimal('0.0'))) + "%"}
                ranks.append(strRank)
            ind += 1
            if(nTop < ind): break
        return ranks
    

# 自定义简易库表操作-股票收益排名(按月更新) 
class myDataDB_StockReturns_Rank(myData_DB.myData_Table):
    def __init__(self, nameDB = "zxcDB_StockReturns_Rank", dir = ""):  
        #初始根目录信息
        if(dir == ""):
            strDir, strName = myIO.getPath_ByFile(__file__)
            self.Dir_Base = os.path.abspath(os.path.join(strDir, "../../.."))  
            self.Dir_DataDB = self.Dir_Base + "/Data/DB_Data/"
            myIO.mkdir(self.Dir_DataDB, False) 
        super().__init__(nameDB, self.Dir_DataDB, False) 


#初始全局消息管理器
from myGlobal import gol 
gol._Init()     #先必须在主模块初始化（只在Main模块需要一次即可）
gol._Set_Setting('zxcdbStockReturns', myDataDB_StockReturns())      #实例 股票收益库对象 
gol._Get_Setting('zxcdbStockReturns').Add_Fields(['用户名', '姓名', '收益', '日期'], ['string','string','float','datetime'], [])     



#主启动程序
if __name__ == "__main__":
    #测试库表操作
    pDB = gol._Get_Setting('zxcdbStockReturns')
    
    # 添加行数据
    print(pDB.Add_Row({'用户名': '茶叶一主号', '收益': 0.1576, '日期': '2019-08-27'}))
    print(pDB.Add_Row({'用户名': '墨紫', '收益': '0.1476', '日期': '2019-08-26'}))
    print(pDB.Add_Row({'用户名': '墨紫', '收益': '0.1976', '日期': '2019-08-27'}))
    print(pDB.Add_Row({'用户名': '墨紫', '收益': '0.2976', '日期': '2019-08-27'}, True))
    

    # 自定义筛选
    print("查询：", pDB.Query("用户名== 墨紫 && isDel==False"))
    print("查询：", pDB.Query("isDel==False", "收益", True))
    print("查询：", pDB.Query("isDel==False && 日期>=2019-08-28", "收益", True))


    # 排名查询
    print(pDB.Get_Ranks())
    print(pDB.Get_Ranks(nTop = 1))
    print(pDB.Get_Ranks(nTop = 2, bOnlyRank = True))
    print(pDB.Get_Ranks('茶叶一主号'))
    print(pDB.Get_Ranks('茶叶一主号', True))


    print()

