#!/bin/sh

#kill进程 Zxc.Python
PROCESS=`ps -ef|grep Zxc.Python|grep -v grep|grep -v PPID|awk '{ print $2}'`
for i in $PROCESS
do
  echo "Kill the $1 process [ $i ]"
  kill -9 $i
done


#git更新
echo "git pull"
cd /root/Public/myPrjs/zxcProj/
git pull
sleep 1s 


#重启
sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh
#sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Quote.sh

