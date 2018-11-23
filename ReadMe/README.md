zxcPy运行相关
================


# 快速启动脚本

# Windows

	run_zxcPy_Robot.bat


# Linux

	run_zxcPy_Robot.sh   (启动脚本-机器人、微信)
	run_zxcPy_Quote.sh   (启动脚本-行情监测)
	
	git_zxcPy.sh   		 (git脚本自动更新)
	
	
## 自写定时任务 

	每周一到周五 的9-15点 的每5分钟 时执行命令（启动脚本-行情监测）。
	*/1 9-15 * * 1-5 sh /root/Public/UpLoad/Temp/ReadMe/run_zxcPy_Quote.sh

	每天 的8-23点 的每2分钟 时执行命令（启动脚本-机器人、微信）。
	*/5 8-23 * * * sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh 
	
	每天 的0点 0分钟 时执行命令（脚本自动更新）。
	00 0 * * 5 sh /root/Public/myPrjs/zxcProj/ReadMe/git_zxcPy.sh
	
	命令： crontab -e