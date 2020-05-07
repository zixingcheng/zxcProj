#!/bin/sh

#定义路径
dirPath=/root/Public/myPrjs/zxcProj
dirPath_srcPy=/root/Public/myPrjs/zxcProj/src/Zxc.Python


#启动行情监测
logfile_Quote=$dirPath/Logs/myQuote_API.log
file_Quote=$dirPath_srcPy/zxcPy.Quote/myQuote_API.py

count_Quote=`ps -ef |grep $file_Quote |grep -v "grep" |wc -l`
if [ 0 == $count_Quote ];then
	nohup python $file_Quote > $logfile_Wx 2>&1 &
echo $count_Quote
fi


