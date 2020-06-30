#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-12-31 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    马萨CRM电话接通率去重
"""

import sys, os, time 
import mySystem


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myIO_xlsx 

    

#主启动程序 
if __name__ == "__main__":    
    # 载入表格数据    
    #['客户: Group&Dealer Name', '客户: ID', '客户: 潜在客户状态', '客户: 客户所有人', '客户: 创建日期', '客户: 本季度云电话拨打是否符合考核要求', '客户: 本季度云电话是否成功拨打', '是否DCC拨打', '云电话拨打记录：拨打记录编号', '客户: 客户名', '客户: 客户 ID', '客户: 最近展厅来访日期', '拨打时间', '客户: 手机', ...]
    pTable = myIO_xlsx.DtTable()
    #pTable.dataFieldType= ['', "", "", "", "int", "", "", "", "", "", "", "int"]
    pTable.Load("D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\DCC.xlsx")
    indFields = pTable.Get_Index_Fields(pTable.dataField)


    # 循环剔除重复
    dictDCC = {}
    lstRows = []
    rows = pTable._Rows()
    for i in range(0, rows):
        # 忽略已处理用户
        row = pTable[i]
        usrID = row[indFields['客户: ID']]
        if(dictDCC.get(usrID, None) != None):
            continue

        # 处理（循环所有，统计呼叫成功数、失败数）
        nTimes = 0
        nSuccees = 0
        for j in range(i, rows):
            x = pTable[j]
            if(x[indFields['客户: ID']] != usrID):
                continue

            #统计
            nTimes += 1
            if(x[indFields['呼叫结果']] == "呼叫成功"):
                nSuccees += 1
            
        # 记录已处理
        if(nSuccees > 0):
            row[indFields['呼叫结果']] = '呼叫成功'
        row.append(nTimes)
        row.append(nSuccees)

        # 修正日期字段
        if(type(row[indFields['客户: 创建日期']]) == float):
            row[indFields['客户: 创建日期']] = str(int(row[indFields['客户: 创建日期']]))
        if(type(row[indFields['客户: 最近展厅来访日期']]) == float):
            row[indFields['客户: 最近展厅来访日期']] = str(int(row[indFields['客户: 最近展厅来访日期']]))
        lstRows.append(row)
        dictDCC[usrID] = row

    # 保存文件
    pTable.dataField.append("呼叫总数")
    pTable.dataField.append("呼叫成功次数")
    strPath = "D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\"
    pTable.dataMat = lstRows
    pTable.Save(strPath, "DCC_Check")

    print()
     