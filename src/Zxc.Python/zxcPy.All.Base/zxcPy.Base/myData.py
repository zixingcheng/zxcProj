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
def Cut_str(text = "", segTag_S = "(", segTag_E = ")", offset = 0):
    # 提取类代码段
    nNum_start = 0
    nNum_end = 0
    ind = text.find(segTag_S, offset)
    end = ind
    if(ind >=0 ): nNum_start += 1
    
    #查找，直到成对闭合则结束 
    ind_S = ind
    while(nNum_start > nNum_end):  
        end = text.find(segTag_E, end + 1)
        if(end < 0): break 
        nNum_end += 1

        #未闭合则继续
        if(nNum_end < nNum_start or (ind >= 0 and text.find(segTag_S, ind + 1, end) > 0)):
            ind = text.find(segTag_S, ind + 1)
            if(ind >=0 ): nNum_start += 1
    strCut = iif(ind_S != end, text[ind_S + len(segTag_S): end], "")
    return ind_S, end, strCut
     

if __name__ == '__main__':
    pp = Interval("(-∞,∞)")
    pp = Interval()
    print(pp)
    print(0 in pp)

    ind_S, ind_E, strV = Cut_str("<<summary>>创建模型对象(返回模型uid)</summary><param name=\"111\">111</param>", "<", ">")
    print(ind_S, ind_E, strV)