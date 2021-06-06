


## 参数示例及说明

```
{
  "srcData": { 
    //插值源数据文件名
    "srcVectorFilename": "D:/myCode/zxcProj/src/Zxc.Core/zpCore.zpGis/zpCore.zpGis_Base/Data/Data_Temp/test.json" 
  },
  "algType": "IDW",             //插值类型
  "algParms": {                 //插值参数
    "algAtrrName": "Aqi",       //插值数据属性名
    "algCellSize": 0.0005,      //插值格网大小（经纬度）
    "algEnvelope_offsetX": 0,   //插值范围偏移X（）
    "algEnvelope_offsetY": 0,   //插值范围偏移Y（）
    "Power": 2,                 //IDW权重值
    "Smoothing": 0,             //IDW平滑参数
    "Radius1": 0,               //IDW搜索椭圆的第一个半径（如果旋转角度为0，则为X轴）
    "Radius2": 0,               //IDW搜索椭圆的第二半径（Y轴，如果旋转角度为0）
    "NoDataValue": -9999        //无数据标记值
  },
  "clipData": {
    "infoDivision": "",             //裁剪用的行政区划（广东省.东莞市）
    "clipWhere": "O_Name='南城区'"  //区划名称筛选条件
  },
  "dstContour": {
    "LevelIntervals": [ 30, 40, 50, 60 ],   //等值线提取的固定值，单一个时为固定间隔
    "LevelBase": 10,                        //等值线提取的起始值
    "IsPolygon": true,                      //等值线是否为等值面
    "dstFileName": ""                       //等值线提结果文件名，为空，则自动命名
  }
}

```