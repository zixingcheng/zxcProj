#!/bin/sh

#定义路径
dirPath=/root/Public/myPrjs/zxcProj
dirPath_srcPy=/root/Public/myPrjs/zxcProj/src/Zxc.Python


#启动微信后台
logfile_Wx=$dirPath/Logs/myWeixin_ItChat.log
file_Wx=$dirPath_srcPy/zxcPy.Weixin/zxcPy.Weixin/myWeixin_ItChat.py

count_Wx=`ps -ef |grep $file_Wx |grep -v "grep" |wc -l`
if [ 0 == $count_Wx ];then
	nohup python $file_Wx  > $logfile_Wx 2>&1 &
echo $count_Wx
fi
sleep 10s


#启动微信API
logfile_API=$dirPath/Logs/myRobot_API.log
file_API=$dirPath_srcPy/zxcPy.Robot/myRobot_API.py

count_API=`ps -ef |grep $file_API |grep -v "grep" |wc -l`
if [ 0 == $count_API ];then
	nohup python $file_API  > $logfile_API 2>&1 &
echo $count_API
fi


