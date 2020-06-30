#encoding: utf-8 
# -*- coding: utf-8 -*-
"""
Created on  张斌 2019-12-31 16:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    马萨售后工单去重
"""
import sys, os, time 
import mySystem


#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
sysDir = mySystem.Append_Us("")
sysDir = mySystem.Append_Dir("myFunction")
import myIO, myIO_xlsx, myData_Trans

    

#主启动程序 
if __name__ == "__main__":    
    # 载入表格数据    
    #['客户: Group&Dealer Name', '客户: ID', '客户: 潜在客户状态', '客户: 客户所有人', '客户: 创建日期', '客户: 本季度云电话拨打是否符合考核要求', '客户: 本季度云电话是否成功拨打', '是否DCC拨打', '云电话拨打记录：拨打记录编号', '客户: 客户名', '客户: 客户 ID', '客户: 最近展厅来访日期', '拨打时间', '客户: 手机', ...]
    pTable = myIO_xlsx.DtTable()
    #pTable.dataFieldType= ['', "", "", "", "int", "", "", "", "", "", "", "int"]
    #pTable.Load("D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\DCC.xlsx")
    pTable.Load("D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\售后工单查询.xls")
    indFields = pTable.Get_Index_Fields(pTable.dataField)
        
    pTable2 = myIO_xlsx.DtTable()
    pTable2.Load("D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\比对.xls")
    indFields2 = pTable2.Get_Index_Fields(pTable2.dataField)

    # 循环剔除重复
    dictDCC = {}
    lstRows = []
    rows = pTable._Rows()
    for i in range(0, rows):
        # 忽略已处理用户
        row = pTable[i]
        usrID = row[indFields['车架号']]
        if(dictDCC.get(usrID, None) != None):
            continue

        # 处理（循环所有，统计呼叫成功数、失败数）
        nTimes = 0
        nSuccees = 0
        dt_S = myData_Trans.Tran_ToDatetime("1999/9/9 00:00:00", "%Y/%m/%d %H:%M:%S")
        for j in range(i, rows):
            x = pTable[j]
            if(x[indFields['车架号']] != usrID):
                continue

            # 保留最近时间
            dt = myData_Trans.Tran_ToDatetime(x[indFields['开单日期']], "%Y/%m/%d %H:%M:%S")
            if(dt_S < dt):
                dt_S = dt
                row = pTable[j]
        lstRows.append(row)
        dictDCC[usrID] = row
        
    dictDCC2 = {}
    lstRows2 = []
    rows2 = pTable2._Rows()
    for i in range(0, rows2):
        row = pTable2[i]
        usrID = row[indFields2['车架号']]
        if(dictDCC2.get(usrID, None) != None):
            continue
            
        bSame = False
        for j in range(0, len(lstRows)):
            x = lstRows[j]
            if(x[indFields['车架号']] == usrID):
                bSame = True

        row.append(bSame)
        lstRows2.append(row)
        dictDCC2[usrID] = row


    # 保存文件
    strPath = "D:\\myCode\\zxcProj\\src\\Zxc.Python\\zxcPy.gsLog_Submits\\mySetting\\"
    pTable.dataMat = lstRows
    pTable.Save(strPath, "售后工单查询_Check")

    pTable2.dataField.append("Same")
    pTable2.dataMat = lstRows2
    pTable2.Save(strPath, "售后工单查询_Check_无比对项")

    print()
     