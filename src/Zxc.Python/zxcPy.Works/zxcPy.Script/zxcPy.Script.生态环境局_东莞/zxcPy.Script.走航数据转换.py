# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-09-07 15:58:00 
    @author: zhang bin
    @email:  zhangbin@qq.com

    走航数据转json --用于supermap数据展示
""" 
import os, time, mySystem 

# 引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)  
import myData_Json, myData_Trans, myData_Geometry, myIO, myIO_xlsx



# 转换对应类型数据为json格式
def transData(dataType):
    dir = "D:\\myDevEvn\\UCMLCoreYunUMS7.6.1.8\\Standard\\Html\\BPObject\\sln_12002\\BusinessUnit\\我的测试\\data\\"
    pTable = myIO_xlsx.DtTable()
    pTable.Load_csv(dir + "dcjd_2020_08_20_pm.csv")
   
    indFields = pTable.Get_Index_Fields(pTable.dataField)
    ind_data = indFields[dataType]
    ind_name = indFields['"时间"']
    ind_lng = indFields['"经度"']
    ind_lat = indFields['"纬度"']
    
    # 循环提取数据
    maxValue = -999999
    lstRows = []
    rows = pTable._Rows()
    for i in range(0, rows):
        row = pTable[i]
        value = myData_Trans.To_Float(row[ind_data].replace('"', ''))
        if(value > maxValue):
            maxValue = value

        name = row[ind_name].replace('"', '')
        name = ""
        lng = myData_Trans.To_Float(row[ind_lng].replace('"', ''))
        lat = myData_Trans.To_Float(row[ind_lat].replace('"', ''))
        jsonInfo = {"name": name, "value": [lng, lat, value]}
        lstRows.append(jsonInfo)

    # 插值加密
    dataAdds = []
    deltaDic = 1.0 / 111000 * 5
    for i in range(0, rows - 1):
        value0 = lstRows[i]['value']; value1 = lstRows[i + 1]['value']; name = lstRows[i]['name']
        _deltaDic, linePoints = myData_Geometry.breakLine(value0[0], value0[1], value1[0], value1[1], deltaDic)
        if(len(linePoints) > 0):
            #计算插值
            dicT = myData_Geometry.distance(value0[0], value0[1], value1[0], value1[1])
            valueT = (value1[2] - value0[2]) / 2
            x0 = value0[0]; y0 = value0[1];

            numPoint = len(linePoints)
            for x in range(0, numPoint, 2):
                x1 = linePoints[x]; y1 = linePoints[x + 1];
                dicTemp = myData_Geometry.distance(x0, y0, x1, y1)
                valueTemp = value0[2] + valueT * (dicTemp / dicT)
                jsonInfo = {"name": name, "value": [x1, y1, valueTemp]}
                dataAdds.append({"index": i, "jsonInfo": jsonInfo})

    # 添加插值
    for i in range(len(dataAdds)-1, -1, -1):
        dataAdd = dataAdds[i]
        jsonInfo = dataAdd["jsonInfo"]
        ind = dataAdd["index"]
        lstRows.insert(ind, jsonInfo)
    dataInfo = [lstRows, maxValue]
    strData = str(dataInfo).replace("'", '"')

    path = dir + dataType.replace('"', '') + ".json"
    myIO.Save_File(path, strData, True, False)
    pass



if __name__ == '__main__':
     transData('"TVOC"')