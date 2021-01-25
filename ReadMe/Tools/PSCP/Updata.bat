:: 设置路径信息
set varPath_py=D:\myCode\zxcProj\src\Zxc.Python\zxcPy.All.Base\zxcPy.Base
set varPath_base=D:\myCode\zxcProj
set varPath=%varPath_base%\ReadMe\Tools\PSCP\UpLoad
set varPath_Url=root@106.13.206.223:
set varPath_Linux=%varPath_Url%/root/Public
set varPath_Prj=%varPath_Linux%/myPrjs/zxcProj
:: ./pscp -r D:\myCode\zxcProj\ReadMe\Tools\PSCP\UpLoad root@106.13.206.223:/root/Public/UpLoad


:: 下载git项目
:: git clone https://github.com/zixingcheng/zxcProj.git

:: 上传文件到Linux目录
echo zxcvbnm!@#456|pscp -r %varPath%\Updata %varPath_Linux%/UpLoad

:: 基础库-python
:: echo zxcvbnm!@#456|pscp -r %varPath_py%\myPy_Libs %varPath_Url%/opt/python3.5/lib/python3.5/site-packages



:: 下载Linux文件
:: echo zxcvbnm!@#456|pscp -r %varPath_Linux%/UpLoad/Updata %varPath%

:: 下载备份Linux配置文件
:: echo zxcvbnm123*|pscp -r %varPath_Prj%/src/Zxc.Python/zxcPy.Quote/Setting %varPath%/Setting/Quote
:: echo zxcvbnm123*|pscp -r %varPath_Prj%/src/Zxc.Python/zxcPy.Robot/Setting %varPath%/Setting/Robot

:: echo zxcvbnm123*|pscp -r %varPath_Prj%/src/Zxc.Python/zxcPy.Robot/Data/DB_Bill %varPath%\Setting\Robot\Data 
:: echo zxcvbnm123*|pscp -r %varPath_Prj%/src/Zxc.Python/zxcPy.Weixin/Data/Pic/QR.png %varPath%\Setting\Weixin\Data



:: 上传配置文件到Linux目录
:: echo zxcvbnm123*|pscp -r %varPath_base%\src\Zxc.Python\zxcPy.Quote\Setting %varPath_Prj%/src/Zxc.Python/zxcPy.Quote
:: echo zxcvbnm123*|pscp -r %varPath_base%\src\Zxc.Python\zxcPy.Robot\Setting %varPath_Prj%/src/Zxc.Python/zxcPy.Robot

:: echo zxcvbnm123*|pscp -r %varPath_base%\src\Zxc.Python\zxcPy.Robot\Data\DB_Bill %varPath_Prj%/src/Zxc.Python/zxcPy.Robot/Data/DB_Bill/

