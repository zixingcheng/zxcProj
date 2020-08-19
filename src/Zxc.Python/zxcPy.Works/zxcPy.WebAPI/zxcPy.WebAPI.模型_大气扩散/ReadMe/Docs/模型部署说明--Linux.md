# 模型部署说明-Linux

目标服务器：
	huawei/huawei133  root/Desktop4you.133  端口 9035

## 安装 Python-3

### 安装python3.7

	下载：
	wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

	解压：
	tar -zxvf Python-3.7.0.tgz
　　cd Python-3.7.0

	安装依赖包
	yum -y install openssl-devel
	yum install libffi-devel 

	配置及安装：
	./configure --prefix=/opt/python3.7 --enable-shared	
	make && make install
	
	编译报错：
	
		第一、update最新版本系统软件
		yum update
		这个必须要执行后才可以安装我们的系统软件或者一键包。
		
		第二、编译缺失关联软件
		yum install gcc build-essential
		编译执行完毕之后，我们在执行./configure && make这类的执行命令就可以解决问题。


		第二种：
		一、Linux下各种依赖都已经安装,是因为没有找到makefile。
		如果是自己写的，确定在当前目录下；如果是源码安装，先运行./configure，生成makefile，再执行make，即可正常运行。

		二、如果没有安装其他依赖先安装依赖
		yum install gcc gcc-c++ autoconf automake
		yum -y install zlib zlib-devel openssl openssl-devel pcre pcre-devel （安装依赖zlib、openssl和pcre）
		
	
	软链接：
	ln -s /opt/python3.7/bin/python3.7 /usr/bin/python3	（默认安装到opt避免路径链接问题） 
	ln -s /opt/python3.7/bin/pip3.7 /usr/bin/pip3

	
	配置库链接：
	echo "/opt/python3.7/lib" > /etc/ld.so.conf.d/python3.7.conf
	ldconfig 
	

### python依赖

	pip3 install Flask
	pip3 install Flask-Pagination
	pip3 install Flask-RESTful
	pip3 install Flask-WTF
	pip3 install Werkzeug
	pip3 install interval
	pip3 install urllib3
	pip3 install requests


## 模型部署

### 文件拷贝
	
	拷贝文件到 /home/huawei/zxcPy.WebAPI.DG_STHJ
	
	具体操作: 
	1). 拷贝文件到 /home/huawei/Updata， 通过 Updata_DgSTHJ.bat
	2). 拷贝文件到 /home/huawei	
		cd /home/huawei
		cp -r Updata/zxcPy.WebAPI.DG_STHJ /home/huawei
	3). 拷贝文件到 /opt/python3.7/lib/python3.7/site-packages	
		cp -r /home/huawei/Updata/myPy_Libs /opt/python3.7/lib/python3.7/site-packages
		cp -r /opt/python3.7/lib/python3.7/site-packages/myPy_Libs/mySystem.py /opt/python3.7/lib/python3.7/site-packages
	4). 删除 /home/huawei/Updata	
		rm -rf Updata

### 配置端口

	vim /home/huawei/zxcPy.WebAPI.DG_STHJ/zxcPy_WebAPI/__init__.py
	
	将8686，修改为对应端口号保存9035
	'''
		#提取端口号(环境变量)
		HOST, PORT, dirBase = myWeb.get_InfoServer(__file__, 'SERVER_HOST', 'SERVER_PORT', 8686)  
		gol._Set_Setting("serverUrl", "http://" + HOST + ":" + str(PORT))
		gol._Set_Setting("serverBaseDir", dirBase)
	'''


### 配置定时任务 

用以下的方法启动、关闭这个cron服务： 

	service crond start		//启动服务 
	service crond stop		//关闭服务 
	service crond restart	//重启服务 
	service crond reload	//重新载入配置
	service crond status    //查看crontab服务状态

	chkconfig crond on 		//设置开机自动启动crond服务
 
 
 新增配置：vim /etc/crontab	
	*/5 * * * * root python3 /home/huawei/zxcPy.WebAPI.DG_STHJ/runserver.py
	
## 其他

### 日志查看

	路径： /home/huawei/zxcPy.WebAPI.DG_STHJ/zxcPy_WebAPI/static/Log
	

