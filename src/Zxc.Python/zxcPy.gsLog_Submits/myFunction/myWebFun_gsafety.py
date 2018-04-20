# -*- coding: utf-8 -*-
"""
Created on  张斌 2016-09-16 15:56:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Gsafety行政管理系统特定操作方法集，注意日报填写前必须先填写个特殊外出(再调用删除)，然后其他均可正常操作，原因不明
"""

import sys
import time,datetime
import urllib,urllib.parse
from lxml import etree


#引用根目录类文件夹
#sys.path.append(r'D:/我的工作/学习/MyProject/日报提交/myFunction')
sys.path.append(r'../myFunction')

import myWebFun_gsafety_prj


#删除所有特殊外出        
def __delet_All_外出__(clsWeb , Address, Content):
    #获取外出项ID，然后删除之
    r = clsWeb.Do_Post("attendance/AttendanceoutrecordBrowse.do?ctrl=attendanceoutrecordvalueobject&action=Refresh", "", "浏览-外出")
    strInfo = r.decode("UTF8")

    #lxml操作
    html = etree.HTML(strInfo)
    
    #筛选数据，14个td才是数据开始
    rr = html.xpath("/descendant::span[@id='klDemo']/descendant::table[position()=6]/descendant::td[/*]")
    nLen = len(rr)
    print(nLen) 
    if(nLen < 14):
        return 0

    #循环删除
    nStep = 0 
    for i in range(1, nLen):
        #print("Step is ")
        #print(i)
        #print(etree.tostring(rr[i]))

        #修正位移
        nNode_Offset = 8 + (i-1) * 8 
        #print(nNode_Offset) 

        #未超出范围则删除
        if(nNode_Offset + 8 <= nLen):
            if(__delet_Step_外出__(clsWeb, rr, nNode_Offset, Address, Content) == True):
                nStep = nStep + 1 
                print("删除外出(特殊) Step: ")
                print(nStep)
            #else:
                #print("Not same ")
        else:
            break
            
    return nStep
    
#删除所有特殊外出--单个
def __delet_Step_外出__(clsWeb, Node, nNode_Offset, Address, Content):
    #按位移依次提取页面信息
    strNode_Info = str(etree.tostring(Node[nNode_Offset + 6]))  #提取节点数据-Key，位移6位
    strKey = clsWeb.Get_EleStr(strNode_Info , "isUser&amp;param=",'" onclick="')
   
    strNode_Info = str(etree.tostring(Node[nNode_Offset + 1]))  #提取节点数据-位置，位移1位,<td>&#22269;&#21150;&#12289;&#20986;&#24046;</td>，中文反解析有问题
    strLocal = clsWeb.Get_EleStr(strNode_Info , "<td>", "</td>") 
    #strInfo = strLocal.decode("gbk").decode("UTF8")
    #strLocal = edcode(.unescape(strLocal)

    strNode_Info = str(etree.tostring(Node[nNode_Offset + 3]))  #提取节点数据-地点，位移3位,　
    strAddress = clsWeb.Get_EleStr(strNode_Info , "<td>", "</td>")
    
    strNode_Info = str(etree.tostring(Node[nNode_Offset + 2]))  #提取节点数据-内容，位移2位,　
    strContent = clsWeb.Get_EleStr(strNode_Info , "<td>", "</td>")

 
    
    #判断数据是否相同，相同则删除
    if(strAddress == Address and strContent == Content):
        r = clsWeb.Do_Post("attendance/AttendanceoutrecordDelete.do?attendanceoutrecordid=" + strKey, "", "删除外出(特殊)") 
        #print("删除外出(特殊)") 
        return True
    else:
        #print("删除外出(特殊)失败。 %s %s %s" % (strKey, strAddress, Address))
        return False

#创建外出数据
def __add_考勤外出__(clsWeb, Address, Content):
    #写考勤外出
    #time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    strTime = time.strftime("%Y-%m-%d", time.localtime()) + " 12:00"    #定义时间到当天12点
    strDataInfo_Out = { 
        'btnBack':'',
        'btnReset':'',
        'btnSave':'clicked',
        'formid':'frmCreate',
        'outrecbegindate':strTime,
        'outrecmark':'1',
        'outrecremark':'',
        'outrectargetenddate':strTime,
        'outrecworkaddress':Address,
        'outrecworkcontent':Content
        }
    r = clsWeb.Do_Post("attendance/AttendanceoutrecordAdd.do", strDataInfo_Out, "考勤外出填写")
    #print(r.decode("UTF8"))
    #print("ok34")

    #获取外出项ID，然后删除之
    r = clsWeb.Do_Post("attendance/AttendanceoutrecordBrowse.do?ctrl=attendanceoutrecordvalueobject&action=Refresh", "", "浏览-外出")
    #strInfo = r.decode("UTF8")
    #print(r.decode("UTF8"))


#检查时间段是否已存在数据
def Check_Time(clsWeb, strTime_S, strTime_E):
    #时间段检查
    strTimeInfo = { 
        'beginTime':strTime_S,
        'endTime':strTime_E,
        'method':'chackTime'
        }
    r = clsWeb.Do_Post("ams_weekly/chackTime.do", strTimeInfo, "时间段检查")
    strInfo = r.decode("UTF8")
    if(strInfo != ""):    
        print("时间冲突如下：/r/n" + strInfo) 
        return False

    #时间段列表检查
    strTimeInfo = { 
        'beginTime':strTime_S,
        'endTime':strTime_S,
        'method':'chackTimeList'
        }
    r = clsWeb.Do_Post("ams_weekly/chackTime.do", strTimeInfo, "时间段列表检查")
    strInfo = r.decode("UTF8")
    if(strInfo != ""):    
        print("时间冲突如下：/r/n" + strInfo)
        return False
    
    return True

    
#日报填写
def __add_日报__(clsWeb, tTime, dHour, Content, strPrjName, strPrjID, strComplete, strPlan, strProblem, strRemark, tTime_DayStart, bIsOverTime):
    #Time_Start = time.strptime(strTime_S, "%Y-%m-%d %H:%M:%S")
    bNormal = True     #是否有正常工时 
    bMore = False      #是否有加班工时 

    #时间转换
    dtTime_S_Day = datetime.datetime.fromtimestamp(time.mktime(tTime_DayStart))  #开始时间--上班起始
    dtTime_S = datetime.datetime.fromtimestamp(time.mktime(tTime))  #开始时间--当前工作内容
    delta_H_Now = datetime.timedelta(hours = dHour)                 #时长--当前工作内容
    delta_H_Day = datetime.timedelta(hours = 9)                     #正常8小时,中午吃饭1小时，实际9小时

    #计算结束时间
    dtTime_E = dtTime_S + delta_H_Now           #结束时间--当前工作内容
    dtTime_E_Day = dtTime_S_Day + delta_H_Day   #正常下班时间

    #中午时间修正(含12-13时间段的)
    dtTime_Next = dtTime_E
    if(dtTime_S.hour <= 12 and dtTime_E.hour >= 12):
        dtTime_E = dtTime_E + datetime.timedelta(hours = 1) #加1小时避过12-13点

    
    #时长超出可用工时则为加班
    if(bIsOverTime or dtTime_E > dtTime_E_Day):
        bMore = True

        #工作起始时间大于下班，即为全加班
        if(bIsOverTime or dtTime_S > dtTime_E_Day):
            bNormal = False
            dtTime_SS = dtTime_S      #加班开始
            dtTime_EE = dtTime_E      #加班结束 
        else:            
            #部分加班，部分正常
            dtTime_SS = dtTime_E_Day  #加班开始
            dtTime_EE = dtTime_E      #加班结束
            dtTime_E = dtTime_E_Day   #正常上班结束
                         
    
    #时间字串生成(正常、加班)
    strTime_S = ''
    strTime_S_str = ','
    strTime_E = ''
    strTime_E_str = ','
    if(bNormal == True):    
        strTime_S = datetime.datetime.strftime(dtTime_S, "%Y-%m-%d %H:%M") 
        strTime_S_str = datetime.datetime.strftime(dtTime_S, "%Y-%m-%d %H:%M") + ','
        strTime_E =  datetime.datetime.strftime(dtTime_E, "%Y-%m-%d %H:%M") 
        strTime_E_str = datetime.datetime.strftime(dtTime_E, "%Y-%m-%d %H:%M") + ','
        dtTime_Next = dtTime_E

        #时间段检查--失败则忽略
        if(Check_Time(clsWeb, strTime_S, strTime_E) == False):
            return (False, dtTime_Next)
        
    strTime_SS = ''
    strTime_SS_str = ','
    strTime_EE = ''
    strTime_EE_str = ','
    if(bMore == True):
        strTime_SS = datetime.datetime.strftime(dtTime_SS, "%Y-%m-%d %H:%M")
        strTime_SS_str = datetime.datetime.strftime(dtTime_SS, "%Y-%m-%d %H:%M") + ','
        strTime_EE = datetime.datetime.strftime(dtTime_EE, "%Y-%m-%d %H:%M") 
        strTime_EE_str = datetime.datetime.strftime(dtTime_EE, "%Y-%m-%d %H:%M") + ','
        dtTime_Next = dtTime_EE
        
        #时间段检查--失败则忽略
        if(Check_Time(clsWeb, strTime_SS, strTime_EE) == False):
            return (False, dtTime_Next)


    #项目信息获取名称筛选
    #strPrjID = strPrjID
    #strPrjName = strPrjName
    #strComplete = strComplete
    #strPlan = strPlan
    #strProblem = strProblem
    #strRemark = strRemark
  

    #组装请求信息
    strDataInfo = { 
        'btnAdd':'',
        'btnBack':'',
        'btnSave':'clicked',
        'endstr':strTime_E_str,
        'endtime':strTime_E,
        'formid':'frmCreate',
        'iscomplete':strComplete,
        'otherprojerctid':'',
        'overendstr':strTime_EE_str,
        'overstartstr':strTime_SS_str,
        'overtimestart':strTime_SS,
        'overtimeend':strTime_EE,
        'plancontent':strPlan,
        'problem':strProblem,
        'projectid':strPrjID,
        'projectname':strPrjName,
        'remark':strRemark,
        'startstr':strTime_S_str,
        'starttime':strTime_S, 
        'weeklycontent':Content
        }

    #填写请求
    print(datetime.datetime.strftime(dtTime_E, "%Y-%m-%d %H:%M"))
    print("日报填写：%s  %sH(%s -- %s)" % (strPrjName, dHour, datetime.datetime.strftime(dtTime_S,"%Y-%m-%d %H:%M"), datetime.datetime.strftime(dtTime_Next,"%Y-%m-%d %H:%M")))
    print("    请求内容： \r\n        %s " % (strDataInfo))
    
    r = clsWeb.Do_Post("ams_weekly/WeeklyweeklyAdd.do", strDataInfo, "日报填写")
    
    #print(r.decode("UTF8"))
    print("    --填写OK")
    return (True, dtTime_Next) 

def __add_日报_byNote__(clsWeb, pNote):
    #开始工作时间
    strTime_DayStart = pNote.Time
    tTime_S_Day = time.strptime(strTime_DayStart, "%Y-%m-%d %H:%M")                 #开始时间--上班起始
    dtTime_S_Day = datetime.datetime.strptime(strTime_DayStart, "%Y-%m-%d %H:%M")   #开始时间--上班起始
    dtTime_S_Now = dtTime_S_Day

    
    #提取子节点(系统)，用于拼装日志
    bIsOverTime = pNote.IsOverTime
    nPrjs = len(pNote.List)
    if(nPrjs < 1):
        return False

    #提取全局信息
    strPlan_Prj = ''
    strProblem_Prj = ''
    strRemark_Prj = '' 
    for j in range(0, nPrjs):
        
        #非系统日志节点有效
        pChild = pNote.List[j] 
        if(pChild.IsSys == True):
            pChild_Sys = pNote.List[j]

            #组装系统信息（循环对比所有子子节点）
            for k in range(0, len(pChild.List)):
                pChild2 = pChild.List[k]
                if(pChild2.Name == "下周安排"):
                    for k in range(0, len(pChild2.List)):
                        strPlan_Prj += pChild2.List[k] + "\r\n" 
                    #print(strPlan_Prj)
                    
                if(pChild2.Name == "问题"):
                    for k in range(0, len(pChild2.List)):
                        strProblem_Prj += pChild2.List[k] + "\r\n"  
                    #print(strProblem_Prj)
                    
                if(pChild2.Name == "备注"):
                    for k in range(0, len(pChild2.List)):
                        strRemark_Prj += pChild2.List[k] + "\r\n"   
                    #print(strRemark_Prj)
            break
            
            
    #提取子节点，用于拼装日志
    for j in range(0, nPrjs):
        
        #非系统日志节点有效
        pChild = pNote.List[j]
        strContent = ""
        if(pChild.IsSys == True):
            continue
            
        #组装子节点内容
        strContent = ""
        for k in range(0, len(pChild.List)):
            strContent += pChild.List[k] + "\r\n"


        #项目信息
        strPrjName = pChild.Name
        strHours = pChild.Hours
        strComplete = pChild.Computed
        dHour = float(clsWeb.Get_EleStr(pChild.Hours, "(", "h)"))

        #按项目名称查询项目编号
        #strPrjID = '2c90827051e6b8fd0151eb665f730013'
        pDict2 = myWebFun_gsafety_prj.__get_prj__(strPrjName)
        if(len(pDict2) == 0): 
            print("项目： %s 名称模糊查询无结果，无法定位项目，重新设置为唯一" % (strPrjName))
            return 
        if(len(pDict2) > 1) :
            print("项目： %s 名称模糊查询到多个，无法定位项目，重新设置为唯一" % (strPrjName))
            print(pDict2)
            return
        else:
            for key in pDict2.keys():
                strPrjName = key                
                strPrjID = pDict2[strPrjName]
                pChild.Name = strPrjName
                pChild.ID = strPrjID
 
        strPlan = ''
        strProblem = ''
        strRemark = ''
        if(j == 0):
            strPlan = strPlan_Prj
            strProblem = strProblem_Prj
            strRemark = strRemark_Prj
     
 
        #计算结束时间-作为下一起始时间
        #delta_H = datetime.timedelta(hours = dHour)
        #dtTime_S_E = dtTime_S_Now + delta_H
        #时间段检查--失败则忽略
        #tTime_S = dtTime_S_Now.timetuple()
        #strTime_S = datetime.datetime.strftime(dtTime_S_Now, "%Y-%m-%d %H:%M") 
        #strTime_E = datetime.datetime.strftime(dtTime_S_E, "%Y-%m-%d %H:%M")
        #if(Check_Time(clsWeb, strTime_S, strTime_E) == False):
            #continue

    
        #添加日志--返回执行结果及下一工作起始时间
        tTime_S = dtTime_S_Now.timetuple() 
        x,y = __add_日报__(clsWeb, tTime_S , dHour, strContent, strPrjName, strPrjID, strComplete, strPlan, strProblem, strRemark, tTime_S_Day, bIsOverTime)
        #print(x)  
        #print(datetime.datetime.strftime(y, "%Y-%m-%d %H:%M"))
     
        #更新开始时间
        dtTime_S_Now = y     


