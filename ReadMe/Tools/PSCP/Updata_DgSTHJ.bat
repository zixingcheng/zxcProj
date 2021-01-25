:: 设置路径信息
set varPath_base=D:\myCode\zxcProj
set varPath=%varPath_base%\ReadMe\Tools\PSCP\UpLoad
set varPath_Url=huawei@19.104.44.133:
set varPath_Linux=%varPath_Url%/home/huawei


:: 上传文件到Linux目录
echo huawei133|pscp -r %varPath%\Updata %varPath_Linux%
