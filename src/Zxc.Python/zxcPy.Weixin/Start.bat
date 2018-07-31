@echo off 

::启动微信后台
start python zxcPy.Weixin/myWeixin_ItChat.py
::延时5秒
choice /t 5 /d y /n >nu

::启动微信API
start python myWeixin_API.py


exit
 