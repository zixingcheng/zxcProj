# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-10-07 16:45:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    自定义数据类型操作

"""
import sys, string
import interval 


#三元运算
def iif(condition, true_part, false_part):  
    return (condition and [true_part] or [false_part])[0]


#字符串转区间对象
def Interval(intervals = ""):
    #校正
    strInfo = intervals.strip()
    if(strInfo == ""):
        strInfo = "(-∞,∞)"
        
    #解析
    bFirst = iif(strInfo[0:1] == "(" ,True ,False)
    bEnd = iif(strInfo[-1:] == ")" ,True ,False)

    #特殊字符修正
    strInfo = strInfo.replace("π", "3.14159265")
    strInfo = strInfo.replace("∞", "inf")
    strSets = strInfo[1:-1].split(',') 

    pInterval = interval.Interval(float("-inf"), float("-inf"), lower_closed = False)
    if(len(strSets) != 2):
        return pInterval

    #转换值
    dLower = float(strSets[0])
    dUpper = float(strSets[1])
        
    if(bFirst != bEnd):
        #前后不等
        if(bFirst):
            pInterval = interval.Interval(dLower, dUpper, lower_closed = False)
        else:
            pInterval = interval.Interval(dLower, dUpper, upper_closed = False)
    else:
        if(bFirst):
            pInterval = interval.Interval(dLower, dUpper, closed = False)
        else:
            pInterval = interval.Interval(dLower, dUpper, closed = True)
    return pInterval


#Trim运算
def Trim(text):  
    while (text[0:1] == " "):
        text = text[1]

    while (text[-1:] == " "):
        text = text[:-1]
    return  text

#循环替换所有符号为目标符号
def Replace_ALL(text, symbol = "  ", re = " "):  
    while(text.count(symbol) > 0):
        text = text.replace(symbol, re)
    return text.strip()
#查找指定标识字符出现的有效位置,屏蔽指定符号内标识字符
def Find(text, sep, offset = 0, segTag_S = "\"", segTag_E = "\""):
    #提取所有引号对
    lstSeg = []
    text.replace("\"", "'")                      #去除转义引号
    ind_0 = text.find(segTag_S, offset)          #引号起始位置 
    while(ind_0 >= 0):
        ind_1 = text.find(segTag_E, ind_0 + 1)   #引号结束位置
        if(ind_1 > 0):
            lstSeg.append(ind_0)                 #记录引号对位置
            lstSeg.append(ind_1)
            ind_0 = text.find(segTag_S, ind_1 + 1)         
        else: break

    ind = text.find(sep, offset)                 #标识出现位置
    numSet = len(lstSeg)
    while(ind >= 0 and numSet > 1):
        bInSeg = False
        for x in range(0, numSet, 2):            #循环校检是否在指定符号内
            if(ind > lstSeg[x] and ind < lstSeg[x + 1]):
                offset = ind + 1
                bInSeg = True
                ind = -1
                break
        if(bInSeg == False): return ind          #不在Seg内，直接返回
        if(offset >= len(text)):break
        ind = text.find(sep, offset)             #标识出现位置
    return ind
#查找指定标识字符出现的次数,屏蔽指定符号内标识字符
def Count(text, sep, offset = 0, end = -1, segTag_S = "\"", segTag_E = "\""):
    #提取所有引号对
    lstSeg = []
    text.replace("\"", "'")                      #去除转义引号
    ind_0 = text.find(segTag_S, offset)          #引号起始位置 
    while(ind_0 >= 0):
        ind_1 = text.find(segTag_E, ind_0 + 1)   #引号结束位置
        if(ind_1 > 0):
            lstSeg.append(ind_0)                 #记录引号对位置
            lstSeg.append(ind_1)
            ind_0 = text.find(segTag_S, ind_1 + 1)         
        else: break

    lstPos = []
    if(end < 0): end = len(text)
    ind = text.find(sep, offset, end)            #标识出现位置
    while(ind >= 0):
        lstPos.append(ind)
        ind = text.find(sep, ind + 1, end)       #标识出现位置

    #Count累加
    nNum = 0
    numSet = len(lstSeg)
    for ind in lstPos:
        bInSeg = False
        for x in range(0, numSet, 2):            #循环校检是否在指定符号内
            if(ind > lstSeg[x] and ind < lstSeg[x + 1]):
                bInSeg = True
                break
        if(bInSeg == False): nNum += 1
    return nNum
#截取指定符号间的字符串
def Cut_str(text = "", segTag_S = "(", segTag_E = ")", offset = 0):
    # 提取类代码段
    nNum_start = 0
    nNum_end = 0
    ind_S = Find(text, segTag_S, offset)                #查找有效起始
    ind_E = ind_S
    if(ind_S >=0 ): nNum_start += 1
    
    #查找，直到成对闭合则结束 
    ind_S = ind_S
    while(nNum_start > nNum_end):  
        ind_E = Find(text, segTag_E, ind_E + 1)         #查找有效结束
        if(ind_E < 0): break 
        nNum_end += 1

        #未闭合则继续--起始符号到终止符号间是否存在有效起始符号
        ind = Find(text, segTag_S, ind_S + 1)      
        if(ind >= 0 and ind < ind_E):
            ind_S = ind
            nNum_start += 1
    strCut = iif(ind_S != ind_E, text[ind_S + len(segTag_S): ind_E], "")
    return ind_S, ind_E, strCut
     
#匹配指定字符集
def Matching_strs(Text, usrWords = {}):
    for x in usrWords.keys():
        num = int(usrWords[x])
        if(Text.count(x) != num):
            return False
    return True



if __name__ == '__main__':
    pp = Interval("(-∞,∞)")
    pp = Interval()
    print(pp)
    print(0 in pp)

    str0 = "_gT_Replace(strAppPath, string(\"//\"), string(\"/\"))";
    ind = Find(str0, "//")
    print(Count(str0, "//"))
    print(Count(str0, "T", 0, 4))

    ind_S, ind_E, strV = Cut_str("<<summary>>创建模型对象(返回模型uid)</summary><param name=\"1<11\">111</param>", "<", ">", 30)
    print(ind_S, ind_E, strV)


    print(Matching_strs("你哎好aa！a", {'哎':1, "aa": 2}))