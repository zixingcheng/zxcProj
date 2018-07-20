# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-10-07 14:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    参数字典集约化初始及管理操作，参数对象定义

参数字典数据格式如下：(名称,名称(EN),编号,编号起始,编号终止,父系编号,单位,参数类型,参数范围,参数默认值,备注)

示例数据：
名称,名称(EN),编号,编号起始,编号终止,父系编号,单位,参数类型,参数范围,参数默认值,备注
模型常规参数,Usual_Sets,101000,101000,103000,,,,,,模型的常见参数集合，如天气、物理量、化学量等
时间,MilliSecond,101001,,,,ms,long,"[0,∞)",,毫秒
时间,Second,101002,,,,s,double,"[0.0,∞)",,秒
时间,Minute,101003,,,,min,double,"[0.0,∞)",,分
时间,Hour,101004,,,,h,double,"[0.0,∞)",,时

"""
import sys, os, string, json, codecs
import interval 

#加载自定义库
import myEnum, myData, myData_Trans
  
#定义数据结构枚举
myDataType = myEnum.enum('object', 'int', 'long', 'double', 'arrays', 'array_d', 'bool', 'datetime', 'string', 'enum', 'array', 'str_obj', 'array_obj')
#DataType = myDataType.int
#print (myDataType)
#print (DataType)

#data11 = "{'b':789,'c':456,'a':123}"
#data1 = eval(data11)
#d1 = json.dumps(data1,sort_keys=False,indent=4)
#print( d1 ) 
#print( data1 )

       
#定义结构体--Field 
class Item_Field:
    def __init__(self):     
        self.Name = ""      #参数名称 
        self.Name_En = ""   #参数_英文
        
        self.ID = -1        #参数编号
        self.ID_Start = -1  #参数集起始编号 
        self.ID_End = -1    #参数集结束编号  
        self.ID_Node = -1   #参数编号-所在节点编号
        self.ID_Parent = -1 #参数编号-父编号(继承对象)
        
        self.Unit = "无"    #参数单位
        self.Unit_En = "HH" #参数单位_英文
        self.DataType = myDataType.object       #参数类型
        
        self.ValueRange_str = ""                #参数范围字串
        self.ValueRange = myData.Interval()     #参数范围对象 
        self.Value_Default = ""                 #参数默认值
        
        self.Remark = ""    #参数备注 
        self.IsNode = False #是否为节点
        self.List = []      #下属节点信息 

    #转换为Json串 
    def To_String(self, bID = True):
        #下属节点处理，区分节点
        Data = "{"
        if(self.IsNode):
            #print(len(self.List))
            nLen = len(self.List)
            for i in range(0, nLen):
                pField = self.List[i]
                strKey = myData.iif(bID, str(pField.ID), pField.Name_En)
                if(pField.IsNode):
                    #print(pField.Name) 
                    #print("Object")  
                    Data += "'" + strKey + "':" + pField.To_String(bID)
                else:  
                    Data += "'" + strKey + "':" + pField.Get_String_Value()

                if(nLen - 1 > i):
                    Data += ","
        else:
            #非节点直接处理   
            strKey = myData.iif(bID, str(self.ID), self.Name_En)     
            Data += "'" + strKey + "':" + self.Get_String_Value() 

        Data += "}"
        #ss = json.dumps(Data, sort_keys = False, indent = 4)
        #print(ss)
        return Data
    
    def To_String3(self, bID = True):
        Data = json.loads("{}") 

        #下属节点处理，区分节点 
        if(self.IsNode):
            #print(len(self.List)) 
            for i in range(0,len(self.List)):
                pField = self.List[i]
                strKey = myData.iif(bID, str(pField.ID), pField.Name_En)
                if(pField.IsNode):
                    #print(pField.Name) 
                    #print("Object") 
                    Data[strKey] = pField.To_String(bID)
                else: 
                    Data[strKey] = pField.Value_Default     
        else:
            #非节点直接处理   
            strKey = myData.iif(bID, str(self.ID), self.Name_En)     
            Data[strKey] = self.Value_Default 
        
        #ss = json.dumps(Data, sort_keys = False, indent = 4)
        #print(ss)
        return Data

    #值转换为Str串--@需完善 
    def Get_String_Value(self):
        Data = "\"" + self.Value_Default + "\""
        return Data
       
#定义结构体--参数字典
class Dict_Field:
    def __init__(self, path):     
        self.pDicts = []                 #参数字典 
        self.pDicts_Index = []           #参数字典_键列表
        self.pDicts_Value = []           #参数字典_参数对象列表
        self.pDict_Node = Item_Field()

        #载入参数
        self._Get_Dicts_(path)


    #是否为Dict节点(通用) -- ,分隔
    def __IsDic__(self, strNode, strFirt ="," ,nCount =11):    
        strInfo = strNode.strip()
        if(strInfo.count(strFirt) < nCount):
            return False
      
        #名称为空则忽略    
        strInfo = strInfo[0: strInfo.find(strFirt)]
        if(strInfo == strFirt): 
            return False
        return True
     
    #生成Dict节点对象(通用) -- ,分隔
    def __Get_DictInfo__(self, strNode, strFirt =",",strSec = '"'):
        #容错处理,双引号包含内容可能含有分隔符
        strInfo = strNode.strip()
        strInfo_Check = ""
        #print(strNode)
        
        if(strInfo.count(strSec) != 0):
            #按双引号拆分数据
            #print(strNode)
            strTemps = strInfo.split(strSec)
            nTemps = len(strTemps)
            List_Temps = {}
             
            #提取双引号间数据，单独记录，并重新组装数据
            for i in range(0, nTemps):
                #单数时替换处理
                if(i % 2 == 1):
                    strKey = "@@@" + str(len(List_Temps))
                    List_Temps[strKey] = strTemps[i].strip() 
                    strInfo_Check = strInfo_Check + strKey 
                else:
                    strInfo_Check = strInfo_Check + strTemps[i].strip() 
        else:
            strInfo_Check = strInfo 
        
        #解析数据 
        strSets = strInfo_Check.split(strFirt) 
        nSets = len(strSets)
        if(nSets < 1):
            return []
            
        #依次塞入List 
        List = []
        for i in range(0, nSets):
            #记录数据单独处理
            if(strSets[i].count("@@@") == 1):            
                List.append(List_Temps[strSets[i]]) 
            else:                                    
                List.append(strSets[i].strip())            
        return List


    #生成Dict节点对象
    def __CreateDict__(self, strNode):
        #解析数据   
        List = self.__Get_DictInfo__(strNode)
        if(List[2] == ""):
            return False
                            
        #初始参数对象   
        pDict = self.__CreateDict_Field__(List)

                
        #添加到对应节点（编号检测）
        pDict_Node = self.pDict_Node
        pDicts_Index = self.pDicts_Index
        pDicts_Value = self.pDicts_Value

        #存在节点，判断范围是否吻合，吻合则直接添加
        if(pDict_Node.IsNode and pDict.ID > pDict_Node.ID_Start and pDict.ID < pDict_Node.ID_End):
            pDict.ID_Node = pDict_Node.ID 
            pDict_Node.List.append(pDict)       #添加进上级节点 
        else:
            #节点不吻合,查询上级节点
            pDict_Node2 = self.__SearchDictNode__(pDict)
            if(pDict_Node2.ID <= 0):
                pDict.ID_Node = 0
                self.pDicts.append(pDict)       #无上级节点，则为顶级记录                 
            else:
                pDict.ID_Node = pDict_Node2.ID
                pDict_Node = pDict_Node2        #更新上级节点为当前节点
                pDict_Node.List.append(pDict)   #有上级节点，直接添加                 
                
                 
        #级联继承属性修正--@未完善
        if(pDict.ID_Parent > 0 and pDict.ID_Parent in pDicts_Index): 
            nIndex = pDicts_Index.index(pDict.ID_Parent)
            pParent = pDicts_Value[nIndex]
            
            if(pDict.ID == 110530):
                pp = 1
            pDict.Unit = pParent.Unit
            pDict.Unit_En = pParent.Unit_En

            if(pDict.DataType.count('array') <= 0):
                pDict.DataType = pParent.DataType
            if(pDict.ValueRange_str == ""):
                pDict.ValueRange_str = pParent.ValueRange_str
                pDict.ValueRange = myData.Interval(pDict.ValueRange_str)    #参数范围字串
                
            if(pDict.Value_Default == ""):
                pDict.Value_Default = pParent.Value_Default
                
            if(pDict.Remark == ""):
                pDict.Remark = pParent.Remark
            else:
                pDict.Remark += "[[" + pParent.Remark + "]]"            

        #参数为节点则更新为当前节点
        if(pDict.IsNode):
            pDict_Node = pDict
            
            
        #索引，便于检索 
        pDicts_Index.append(pDict.ID)
        pDicts_Value.append(pDict)
        
        self.pDict_Node = pDict_Node
        #self.pDict_Node.List = pDict_Node.List
        #self.pDicts_Index = pDicts_Index
        #self.pDicts_Value = pDicts_Value                  
        return True

    #查询Dict节点上级对象
    def __SearchDictNode__(self, pDict):
        #遍历字典获取上级节点，倒序搜索第一个符合的
        nLen = len(self.pDicts_Index)
        if(nLen < 1):
            return Item_Field()
        
        Range = range(0, nLen)
        for i in Range[::-1]: 
            pTemp = self.pDicts_Value[i] 
            if(pTemp.IsNode):
                if(pDict.ID > pTemp.ID_Start and pDict.ID < pTemp.ID_End):
                    return pTemp
                
        return Item_Field()  

    #生成Dict_Field节点对象
    def __CreateDict_Field__(self, pList):
        #解析数据  
        pDict = Item_Field() 
        if(pList[2] == ""):
            return pDict
             
        #初始对象             
        pDict.Name = pList[0]           #参数名称 
        pDict.Name_En = pList[1]        #参数_英文
        pDict.ID_Node = 10                                  #参数编号-所在节点编号
        pDict.ID = myData_Trans.To_Int(pList[2])           #参数集编号
            
        pDict.ID_Start = myData_Trans.To_Int(pList[3])     #参数集起始编号 
        pDict.ID_End = myData_Trans.To_Int(pList[4])       #参数集结束编号
        pDict.ID_Parent = 0                                #参数编号-父编号
        if(pDict.ID_Start > 0 and pDict.ID_End <= 0):
            pDict.ID_Parent = pDict.ID_Start               #参数编号-父编号

          
        pDict.IsNode = False            #是否为节点
        if(pDict.ID_Start > 0 and pDict.ID_End > 0): 
            pDict.IsNode = True 
            
        pDict.Unit = pList[6]           #参数单位                             
        pDict.Unit_En = pList[7]        #参数单位_英文      
        
        if(pDict.ID == 110530):
            pp = 2
        pDict.DataType = myData_Trans.Tran_ToEnum(pList[8], myDataType) #参数类型                
        pDict.ValueRange_str = pList[9] #参数范围字串
        if(pList[9] != ""):
            pDict.ValueRange = myData.Interval(pDict.ValueRange_str)    #参数范围字串
        pDict.Value_Default = pList[10] #参数默认值   
        pDict.Remark = pList[11]        #备注信息    
        pDict.List = []                 #下属节点信息
        
        #print("Fields.Name: %s" ,len(pList))   
        #print("Fields.Na22me: %s" ,pList[8])                
        return pDict


    #查询Dict节点上级对象
    def Find(self, ID): 
        nID = 0
        try:
            if(type(ID) == str):
                ID = ID.replace('_@@', '')
            nID = int(ID)
            nIndex = self.pDicts_Index.index(nID)
        except :
            return None
        return self.pDicts_Value[nIndex] 
    

    #打印节点信息      
    def OutPut(self, pDicts): 
        #循环输出结果
        print(len(pDicts))
        for i in range(0, len(pDicts)):                   
            pDict = pDicts[i]      
            print("Fields.Count: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (len(pDict.List),pDict.Name ,pDict.Name_En ,pDict.ID ,pDict.ID_Start ,pDict.ID_End ,
                                     pDict.ID_Parent ,pDict.ID_Node, pDict.Unit, pDict.Unit_En, pDict.DataType, pDict.ValueRange_str, pDict.Value_Default, pDict.Remark))        
            for j in range(0, len(pDict.List)):
                pChild = pDict.List[j]
                print("Fields.Count: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (len(pChild.List),pChild.Name ,pChild.Name_En ,pChild.ID ,pChild.ID_Start ,pChild.ID_End ,
                                     pChild.ID_Parent, pChild.ID_Node, pChild.Unit, pChild.Unit_En, pChild.DataType, pChild.ValueRange_str, pChild.Value_Default, pChild.Remark))        

                if(len(pChild.List) > 0):
                   self.OutPut(pChild.List)                   
                   
    #打印节点信息-索引信息                
    def OutPut_Index(self): 
        #循环输出结果 
        Keys = self.pDicts_Index
        Range = range(0, len(Keys))
        for i in Range:                
            pDict = self.pDicts_Value[i]      
            print("Fields.Count: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (len(pDict.List) ,pDict.Name ,pDict.Name_En,pDict.ID ,pDict.ID_Start ,pDict.ID_End ,
                                      pDict.ID_Parent ,pDict.ID_Node, pDict.Unit, pDict.Unit_En, pDict.DataType, pDict.ValueRange_str, pDict.Value_Default, pDict.Remark))        

    #转换为Json串 
    def To_String(self, bID = True):
        #循环输出结果
        Data = json.loads("{}") 
        for i in range(0, len(self.pDicts)):                   
            pDict = self.pDicts[i]
            strKey = myData.iif(bID, str(pDict.ID), pDict.Name_En)
            Data[strKey] = pDict.To_String(bID) 

        #print(self.pDicts[0].To_String(bID))
        strJson = json.dumps(Data , sort_keys = False, indent = 4) 
        return strJson
    

    #提取Json中所有ID及Name
    def Get_IDs_All(self, strText):    
        keys_En = []
        keys = []

        #循环所有字节，提取""内包含数据对比
        nLen = len(strText)
        nOffset = 0 
        nOffset2 = 0
        for i in range(0, nLen):
            nOffset = strText.find("\"", nOffset2 + 1, nLen)
            if(nOffset > 0):
                nOffset2 = strText.find("\"", nOffset + 1, nLen)
                #提取引号对内数据
                if(nOffset2 > 0):
                    strKey = strText[nOffset + 1 : nOffset2]
                    #if(myData_Trans.Is_Numberic(strKey) == False): continue
                  
                    #处理，替换ID为对应Name
                    pField = self.Find(strKey)
                    if(pField != None):
                        keys_En.append(strKey)
                        keys.append(pField.Name)   
        return keys_En, keys

    #解析配置文件      
    def _Get_Dicts_(self, path, encodingset = 'utf-8'):    
        #提取配置文件
        if (os.path.exists(path) == False):
            print(path)
            return False
        if(encodingset != ''):
            f = codecs.open(path, 'r', encodingset)
        else:
            f = open(path, 'r')  
        lists = f.readlines()
        
        pDicts_Index = {'0': Item_Field()}
        pDict_Node = Item_Field()

        #解析，以行进行分割，分隔符","
        nLines = len(lists) 
        for i in range(1, nLines): 
            #Dic节点 
            if(self.__IsDic__(lists[i]) == True):
                #生成参数对象
                self.__CreateDict__(lists[i])  
 
        
        #关闭文件      
        f.close() 
        return True
    
     
#引用根目录类文件夹
#sys.path.append(r'D:/我的工作/学习/MyProject/日报提交/myFunction')
sys.path.append(r'../myFunction')

#获取路径信息
baseDir = os.getcwd()
baseDir_Root = os.path.abspath(os.path.join(os.getcwd(), "..//..//.."))

pathDict = baseDir_Root + "/Public/Program/ModelData/Base/Dicts/Model_FieldDict.csv"    #Note_Now配置文件路径，py脚本上级目录  
#print("test %s" % (pathDict))

     
if __name__ == '__main__':
    #print(pathDict)
    pDict_Fields = Dict_Field(pathDict)
    pField = pDict_Fields.Find(110051)
    
    pField = pDict_Fields.Find(110530)

    #循环输出结果      
    #pDict_Fields.OutPut(pDict_Fields.pDicts)    
    #pDict_Fields.OutPut_Index()
     
    print(pDict_Fields.To_String(False)) 
    
    ss = U'{"name":"Think","share":50, "price":12, "other":{"H":"a","GG":"aa","A":"aa"},"other2" : [{"aa2":0},{"aa3":0}]}'
    keys_En,keys = pDict_Fields.Get_IDs_All(ss) 
 
