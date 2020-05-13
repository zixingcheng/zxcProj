#!/bin/sh

#定义路径
dirPath=/root/Public/myPrjs/zxcProj
dirPath_srcPy=/root/Public/myPrjs/zxcProj/src/Zxc.Python


#启动行情监测
logfile_Quote=$dirPath/Logs/myQuote_API.log
file_Quote=$dirPath_srcPy/zxcPy.Quote/myQuote_API.py
file_Quote_Debug=$dirPath_srcPy/zxcPy.Quote/myQuote_API_Debug.py 

#调试判断-存在文件中断(用于调试)
count_Wx_Debug=`ps -ef |grep $file_Quote_Debug |grep -v "grep" |wc -l`
if [ 1 == $count_Wx_Debug ];then
exit
fi

count_Quote=`ps -ef |grep $file_Quote |grep -v "grep" |wc -l`
if [ 0 == $count_Quote ];then
	nohup python $file_Quote  >  /dev/null 2>&1 &
	#nohup python $file_Quote > $logfile_Quote 2>&1 &
echo $count_Quote
fi

