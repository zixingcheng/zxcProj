
# Linux信息
    
python ~/App/Company-DGS/zxcPy.Form.生态环境局_东莞/runserver.py
       http://120.197.152.99:18668/zxcWebs/companyinfos/<int:page>
       http://120.197.152.99:18668/zxcWebs/companyinfo


	*/5 8-23 * * * sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh 
	
定时脚本：8-23点，每五分钟检测执行

	vim /etc/crontab


	*/5 8-23 * * * root python /run/media/root/_Data/App/Company-DGS/zxcPy.Form.生态环境局_东莞/runserver.py
	*/5 8-23 * * * root python /run/media/root/_Data/App/Model-DGS/zxcPy.WebAPI.模型_大气扩散/runserver.py

	
	service crond reload	//重新载入配置
	service crond restart	//重启服务 
	service crond status    //查看crontab服务状态


	其他操作命令：

		cp -r /run/media/root/_Data/App/Model-DGS/zxcProj/src/Zxc.Python/zxcPy.Works/zxcPy.WebAPI/zxcPy.WebAPI.模型_大气扩散/ /run/media/root/_Data/App/Model-DGS/
		
		测试命令：

		mount /dev/vdb /run/media/root/_Data
		/dev/vdb                 376G   80M  357G    1% /run/media/root/_Data
