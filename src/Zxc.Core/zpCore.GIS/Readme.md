# 项目结构说明

```
GDAL                    //详见GDAL相关说明
    | gdal_csharp       //GDAL基础库
    | ogr_csharp        //GDAL基础库-坐标系及数据格式转换，偏矢量数据
    | osr_csharp        //GDAL基础库-偏栅格数据
AutoJob                 //自动任务相关
    | Swaps             //数据交换
        | zpCore.zpDataCache.Swap   //数据缓存数据交换-文件型已实现
Base                    //基础库
    | Base.Common       //基础库-常用功能及扩展
    | Base.Image        //基础库-图像操作
GIS                     //GIS相关
    | GIS.Base          //GIS底层库-已封装GDAL相关接口
    | API
        | Gis.API       //GIS开放接口API-包含分布图模型
    | Models
        | GIS.Models.DistributionMap    //分布图模型-已实反距离权重插值
Test
    | TestAPP           //测试程序-控制台方式测试调试
ReadMe                  //相关说明文档
    | Readme.md                         //项目结构说明
    | GIS底层库GDAL及依赖库编译.md       //GDAL编译说明

```

# 其他

1. GDAL源码由官方下载，本地编译，参见 《GIS底层库GDAL及依赖库编译.md》。