# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-10-08 10:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    自定义数据类型--数据转换操作
"""
import sys, string, re
import time, datetime
from struct import pack, unpack 
 

#是否为数字
def Is_Numberic(value):
    #调用正则 
    pRe = re.compile(r'^[-+]?[\d+](\.\d+)?$')
    result = pRe.match(value)
    if(result):
        return True
    else:
        return False 

    
#字符串转bool
def To_Bool(strData):
    if(type(strData) == str):
        if(strData.lower() == "true"):
            return True
    else:
        nValue = To_Int(strData, 0)
        if(nValue == 1): return True
    return False

#字符串转float
def To_Float(strData, default = 0):
    strValue = strData.strip() 
    if(strValue == ""): 
        return default
    else:
        return float(strValue)
 
#字符串转int
def To_Int(strData, default = 0):
    strValue = strData.strip() 
    if(strValue == ""): 
        return default
    else:
        return int(float(strValue))

#字符串转Ints
def To_Ints(strData, strSplit = ",", default = 0):
    strValue = strData.strip()
    strValues = strValue.split(strSplit)

    values = []
    for i in range(0, len(strValues)):
        values.append(To_Int(strValues[i], default))
    return values

#字符串转floats
def To_Floats(strData, strSplit = ",", default = 0):
    strValue = strData.strip() 
    strValues = strValue.split(strSplit)

    values = []
    for i in range(0, len(strValues)):
        values.append(To_Float(strValues[i], default))
             
    return values

# test test test
# 字符串转floats
def To_timeFloats(strData, strSplit=",", default=0):
    strValue = strData.strip()
    strValues = strValue.split(strSplit)

    values = []
    for i in range(0, len(strValues)):
        values.append(To_retain(strValues[i], default))

    return values

# test test test
#字符串保持不变
def To_retain(strData, default = 0):
    strValue = strData.strip()
    if(strValue == ""):
        return default
    else:
        return strValue

                      
#转bytes
def To_Bytes_By_Int(value):
    return pack('i', value)
def To_Bytes_By_Float(value):
    return pack('f', value)
def To_Bytes_By_Str(value, encod= "utf-8"):
    return value.encode(encoding = encod) 


#bytes转值
def To_Int_By_Bytes(value):
    return unpack('i', value)[0]
def To_Float_By_Bytes(value):
    return unpack('f', value)[0]
def To_Str_By_Bytes(value, encod= "utf-8"):
    return value.decode(encoding = encod)


#字符串转enum
def Tran_ToEnum(strKey, enum):
    nIndex = 0
    List = list(enum)
    if(strKey in List):
        nIndex = List.index(strKey)
        
    if(nIndex < 0):
        nIndex = 0 
    return enum[nIndex]
 

# 字符串转time
def Tran_ToTime(strTime, strFormat="%Y-%m-%d %H:%M:%S"):
    # 时间转换 
    dtTime = time.strptime(strTime, strFormat)     
    return dtTime
def Tran_ToTime_byInt(nTime = 0):
    #转换成localtime
    time_local = time.localtime(nTime) 
    return time_local

# 字符串转time
def Tran_ToTimes(strData, strSplit = ",", strFormat="%Y-%m-%d %H:%M:%S"):
    strValue = strData.strip()
    strValues = strValue.split(strSplit)

    values = []
    for i in range(0, len(strValues)):
        values.append(Tran_ToTime(strValues[i], strFormat))
    return values
# 字符串转time
def Tran_ToTimes(List, strFormat="%Y-%m-%d %H:%M:%S"):
    values = []
    for i in range(0, len(List)):
        values.append(Tran_ToTime(List[i], strFormat))    
    return values 

# 字符串转datetime
def Tran_ToDatetime(strTime, strFormat="%Y-%m-%d %H:%M:%S"):
    # 时间转换 
    dtDatetime = datetime.datetime.strptime(strTime, strFormat)   
    return dtDatetime

# datetime转字符串
def Tran_ToDatetime_str(Datetime = None, strFormat="%Y-%m-%d %H:%M:%S"):
    # 时间转换 
    if(Datetime == None):
        Datetime = datetime.datetime.now() 
    strTime = datetime.datetime.strftime(Datetime, strFormat)   
    return strTime
# time转字符串
def Tran_ToTime_str(Time = None, strFormat="%Y-%m-%d %H:%M:%S"):
    # 时间转换
    if(Time == None):
        Time = time.localtime() 
    strTime = time.strftime(strFormat, Time)
    return strTime
# time转字时间戳
def Tran_ToTime_int(Time = None):
    # 时间转换
    if(Time == None):
        Time = time.localtime()  

    #转换成时间戳
    timestamp = time.mktime(Time)
    return int(timestamp)

#转换为字符串
def Tran_ToStr(lstV = [], symbol = ','):
    strV = ""
    for x in lstV:
        strV += symbol + str(x)
    if(len(lstV) > 0): strV = strV[1:]
    return strV
#转换汉子首字母
def Tran_ToStr_FirstLetters(str_input, bUpper = False):
    if isinstance(str_input, str):
        unicode_str = str_input
    else:
        try:
            unicode_str = str_input.decode('utf8')
        except:
            try:
                unicode_str = str_input.decode('gbk')
            except:
                print ('unknown coding')
                return
      
    pStr = ''
    for one_unicode in unicode_str:
        pStr = pStr + str(Tran_ToStr_FirstLetter(one_unicode))
    if(bUpper): return pStr.upper()
    return pStr
def Tran_ToStr_FirstLetter(unicodeWord):
    str1 = unicodeWord.encode('gbk')
    try:        
        ord(str1)
        return unicodeWord
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''
    
#字符串变为转义字符（"转为\"）
def To_Escape_str(strData, bOneLine = False):
    strValue = strData.strip() 
    strValue = strValue.replace("\"","\\\"") 
    if(bOneLine):
        #换行、Tab及空格替换 
        #strValue = strValue.replace("\r\n","")
        strValue = strValue.replace("\r","")
        strValue = strValue.replace("\n","")
        strValue = strValue.replace("\t","")
        strValue = strValue.replace("	","") 
        while(strValue.find("  ") > 0):
            strValue = strValue.replace("  "," ")
        strValue = strValue.replace(" : ",":")
          
    return strValue    



if __name__ == '__main__':   
    #aa = Tran_ToTime("2016/11/21","%Y/%m/%d")
    #print(aa)
    #aa = To_Ints("0,2.0,3.0", ",",0)
    #print(aa)                     
    #print(Is_Numberic('-0.11'))
    #aa=To_Int("100")
    #print(aa)
    lstV = "".split("、")
    lstV.append('sdfsdf')
    strV = Tran_ToStr(lstV, "、")

    arr = To_Bytes_By_Float(106.509)
    value = To_Float_By_Bytes(arr)

    arr = To_Bytes_By_Int(89)
    value = To_Int_By_Bytes(arr)

    arr = To_Bytes_By_Str("Heelow!")
    value = To_Str_By_Bytes(arr)

    print(Tran_ToDatetime_str())
    print()

    #转换汉子首字母
    print(Tran_ToStr_FirstLetters(u'上证180公司治理指数', True))
    print(Tran_ToStr_FirstLetters(u'广联达', True))

    #转换成时间数组
    dt = "2016-05-05 20:28:54"
    print(dt)
    timeArray = Tran_ToTime(dt) 
    timestamp = Tran_ToTime_int(timeArray)
    print(timestamp)
     
    #转换成localtime
    dt = Tran_ToTime_byInt(timestamp)
    print (Tran_ToTime_str(dt))
    