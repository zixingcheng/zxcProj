#!/bin/sh

#定义路径
dirPath=/root/Public/myPrjs/zxcProj
dirPath_srcPy=/root/Public/myPrjs/zxcProj/src/Zxc.Python

#调试判断-存在文件中断(用于调试)
file_Debug=$dirPath/ReadMe/zxcPy_Debug.log 
if [ -d $file_Debug]; then  
　　exit
fi


#启动行情监测
logfile_Quote=$dirPath/Logs/myQuote_API.log
file_Quote=$dirPath_srcPy/zxcPy.Quote/myQuote_API.py

count_Quote=`ps -ef |grep $file_Quote |grep -v "grep" |wc -l`
if [ 0 == $count_Quote ];then
	#nohup python $file_Quote  >  /dev/null 2>&1 &
	nohup python $file_Quote > $logfile_Quote 2>&1 &
echo $count_Quote
fi

