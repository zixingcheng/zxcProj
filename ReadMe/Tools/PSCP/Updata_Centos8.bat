:: 设置路径信息
set varPath_base=D:\myCode\zxcProj
set varPath=%varPath_base%\ReadMe\Tools\PSCP\UpLoad
set varPath_Url=root@192.168.1.9:
set varPath_Linux=%varPath_Url%/home/upData


:: 上传文件到Linux目录
echo zp.666888!@#|pscp -r %varPath%\Updata_app %varPath_Linux%

::echo zp.666888!@#|pscp -r D:\myCode\publish\myApp_Prj root@192.168.1.9:/home/upData

pause
