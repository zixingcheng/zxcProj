# 阿里云部署说明

## 安装系统

	建议使用linux ，可选centos7以上，最好直接镜像市场安装 rabbitmq环境镜像
	
### rabbitmq镜像

	https://oneinstack.com/docs/rabbitmq-image-guide/
	按操作打开远程访问，可以正常访问rabbitmq即可。 
	
	
	

### 图形界面
		 
1. 先安装 MATE Desktop

	yum groups install "MATE Desktop"
 
	命令输入之后，会列出一大堆文字的，然后显示这个
	y/d/n ，输入y，按回车下载安装；

	安装完成，显示下面图片complete

2. 安装好 MATE Desktop 后，再安装 X Window System。

	yum groups install "X Window System"

3. 设置默认通过桌面环境启动服务器：

	systemctl  set-default  graphical.target
	
4. 安装完成后，通过 reboot 等指令重启服务器，或者在 ECS 服务器控制台重启服务器。


### 文件互传

使用pscp，pscp.exe属于Putty的重要组件工具之一，同时也可以单独使用，可以通过pscp.exe实现本地windows下的文件下载、上传到linux上，有需要的赶快下载吧！

配置如下.bat文件，可实现本地与linux远程目录的上下同传：

	echo ******|pscp -r D:\UpLoad\Temp root@39.105.196.175:/root/Public/UpLoad			(本地上传至Linux)
	echo ******|pscp -r root@39.105.196.175:/root/Public/UpLoad/Updata D:\UpLoad\		(本地下载Linux)
		  
* 直接使用bat文件进行执行，更方便，亦可手动操作。


### rabbitmq安装

未完成测试, 需进一步实测：

···

	安装
	方式一：已经测试成功	

		wget --content-disposition https://packagecloud.io/rabbitmq/erlang/packages/el/7/erlang-20.3-1.el7.centos.x86_64.rpm/download.rpm
		yum install erlang-20.3-1.el7.centos.x86_64.rpm
		———————————————


		wget https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.6/rabbitmq-server-3.7.6-1.el7.noarch.rpm
		yum install rabbitmq-server-3.7.6-1.el7.noarch.rpm
		————————————————


		systemctl status firewalld
		systemctl start firewalld


		iptables -A INPUT -p tcp --dport 5672 -j ACCEPT	#后续调整为iptables
		iptables -A INPUT -p tcp --dport 15672 -j ACCEPT	#后续调整为iptables
		firewall-cmd --zone=public --add-port=15672/tcp --permanent
		firewall-cmd --reload    		#重新载入，更新防火墙规则
		firewall-cmd --list-port		#查看已开启的端口
		————————————————

		rabbitmqctl status
		service rabbitmq-server restart
		rabbitmqctl status
		

		rabbitmq-plugins enable rabbitmq_management


		rabbitmqctl add_user admin(账号) 123456(密码)
		rabbitmqctl add_user admin a123456
		rabbitmqctl set_user_tags admin administrator			#用户设置为administrator才能远程访问
		rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"   #给用户”djs“赋予了权限，结果ok了，nice。


		添加用户可能报错：
		chown rabbitmq:rabbitmq .erlang.cookie
		chmod 400 .erlang.cookie


		rabbitmqctl status
		echo 106.13.206.223 rabbitmq>>/etc/hosts

		service rabbitmq-server restart
		rabbitmqctl status
		
		chkconfig rabbitmq-server on
 


	方式二：本人的选则的方式

	  第一步：

	      首先下载 erlang rpm ：wget http://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm

	（这里有一个大坑网上很多都没写，被坑惨了，因为安装erlang需要依赖epel 源，如果没有该源需要先下载安装如下方式：1：wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

	2：rpm -ivh epel-release-latest-7.noarch.rpm

	3：查看 yum repolist

	）

	第二步：完成以上操作一下这条命令

	    1：rpm -Uvh erlang-solutions-1.0-1.noarch.rpm

	    2：安装 yum install erlang

	    3：检查是否安装完成：erl -version
	        


	第三步：因为erlang 是不断更新，但rabbitMq 是要和erlang版本对应比较严谨，如官方对应关系（传送门）所以需要将erlang自动更新关闭，操作命令如下：

	1：安装禁用指令   yum install yum-plugin-versionlock 

	2：yum versionlock erlang （要锁定的组件）

	3：yum versionlock list       ——查看已锁定的组件列表

	4：这一步要执行；yum versionlock clear 清楚禁用组件

	作者：ystwo
	链接：https://www.jianshu.com/p/acd07acb14fa
	來源：简书
	简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。、

	二：安装RabbitMq  

	    正主来了

	第一步：wget https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.7/rabbitmq-server-3.7.7-1.el7.noarch.rpm
			rpm --import https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.7/rabbitmq-server-3.7.7-1.el7.noarch.rpm.asc

	第二步：yum install -y rabbitmq-server-3.7.7-1.el7.noarch.rpm

	第三步：（1）systemctl enable rabbitmq-server   开机启动设置

	              （2）systemctl restart rabbitmq-serve  重启

	              （3）rabbitmqctl status 查看状态

	第四步：启用web组件  rabbitmq-plugins enable rabbitmq_management

	作者：ystwo
	链接：https://www.jianshu.com/p/acd07acb14fa
	來源：简书
	简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
	 
···



## 安装 Python-3.5

### 准备工作
	
基础环境安装：
	yum -y groupinstall "Development tools"
	yum -y install openssl-devel sqlite-devel bzip2-devel ncurses-devel gdbm-devel readline-devel tcl-devel tk-devel xz-devel zlib-devel db4-devel libpcap-devel

### 安装python3.5

	下载：
　　wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tgz

	解压：
　　tar -zxvf Python-3.5.3.tgz
　　cd Python-3.5.3


	配置及安装：
	./configure --prefix=/opt/python3.5 --enable-shared	
	make && make install
	
	软链接：
	ln -s /opt/python3.5/bin/python3 /usr/bin/python3	（默认安装到opt避免路径链接问题）
	ln -s /opt/python3.5/bin/python3 /usr/bin/python	（需要按替换系统中的python）
	
	
	配置库链接：
	echo "/opt/python3.5/lib" > /etc/ld.so.conf.d/python3.5.conf
	ldconfig 

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
	ln -sf /opt/python3.7/bin/python3.7 /usr/bin/python	（需要按替换系统中的python）
	ln -s /opt/python3.7/bin/pip3.7 /usr/bin/pip3

	
	配置库链接：
	echo "/opt/python3.7/lib" > /etc/ld.so.conf.d/python3.7.conf
	ldconfig 
	
安装完毕，/usr/local/目录下就会有python3了
	
* 注意部分链接已经存在pyton2.7的快捷方式，可以直接删除，再创建python3的链接。
	

### 替换系统中的python

注意，设置的软连接名称不能是python，因为yum用的到，如果你想将其设置成python，即ln -s /opt/python3.5/bin/python3 /usr/bin/python，还需要修改yum配置。

使用vi打开 /usr/bin/yum 即：vi /usr/bin/yum 

	#! /usr/bin/python 修改为 #! /usr/bin/python2
	 
	完整示例： （i插入，esc退出 :wq保存并退出 :q!直接退出）
	# vi /usr/bin/yum
	FROM:
	#!/usr/bin/python
	TO:
	#!/usr/bin/python2.7
	Similarly: Error message:
	Downloading packages:
	  File "/usr/libexec/urlgrabber-ext-down", line 28
		except OSError, e:
					  ^
	SyntaxError: invalid syntax
	Exiting on user cancel
	The issue is also related to Python 3 set as a default global version. To fix this error update/usr/libexec/urlgrabber-ext-down script:
	# vi /usr/libexec/urlgrabber-ext-down
	FROM:
	#!/usr/bin/python
	TO:
	#!/usr/bin/python2.7

同理 vi /usr/libexec/urlgrabber-ext-down 

	#! /usr/bin/python 也要修改为#! /usr/bin/python2


* 设置软连接--非opt路径可能存在链接问题，未完成测试

　　./configure --prefix=/usr/local/python3 --enable-shared
	ln -s /usr/local/python3/bin/python3 /usr/bin/python3.5 
　　ln -s /usr/local/python3.5/bin/python3 /usr/bin/python

　　由于更改系统默认的python会影响yum，需修改如下两个文件：

　　/usr/bin/yum和/usr/libexec/urlgrabber-ext-down

Known problems with Fedora Linux and Python 3 version: Error message:



### 安装pip

	/opt/python3.7/bin/pip3 install --upgrade pip
	ln -sf /opt/python3.7/bin/pip3 /usr/bin/pip
	
	
	或：
　　wget --no-check-certificate  https://pypi.python.org/packages/source/p/pip/pip-8.0.2.tar.gz#md5=3a73c4188f8dbad6a1e6f6d44d117eeb

　　tar -zxvf pip-8.0.2.tar.gz
　　cd pip-8.0.2

　　python3 setup.py build
　　python3 setup.py install

　　使用pip安装包测试：
　　　　如报错，则缺少yum install openssl-devel,安装完成后一样需要重新编译python3.5（make&&make install）

升级pip	因为python3.5自带pip，setuptools
	
	升级pip：
	 
	
	升级setuptools：
	
	wget https://bootstrap.pypa.io/ez_setup.py -O - | python3
	ln -s /opt/python3.5/bin/easy_install /usr/bin/easy_install

### 安装setuptools

	wget https://bootstrap.pypa.io/ez_setup.py -O - | python3
	ln -s /opt/python3.5/bin/easy_install /usr/bin/easy_install
	
	或： 
　　wget --no-check-certificate  https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz#md5=c607dd118eae682c44ed146367a17e26

　　tar -zxvf setuptools-19.6.tar.gz
　　cd setuptools-19.6

　　python3 setup.py build
　　python3 setup.py install

　　(如有报错： RuntimeError: Compression requires the (missing) zlib module，则需要安装yum install zlib-devel，安装后要重新编译 python3.5:   


### mysql数据库安装 

	参考 centos7下安装mysql5.7（rpm） https://blog.csdn.net/wudinaniya/article/details/81094578
	
	实测一：参考 https://blog.csdn.net/qq_32074527/article/details/93176210
	一、安装配置MySQL的yum源
		# 安装MySQL的yum源，下面是RHEL6系列的下载地址
		rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm

		# 安装yum-config-manager
		yum install yum-utils -y

		# 禁用MySQL5.6的源
		yum-config-manager --disable mysql56-community

		# 启用MySQL5.7的源
		yum-config-manager --enable mysql57-community-dmr

		# 用下面的命令查看是否配置正确		
		yum repolist enabled | grep mysql 
	
	二、yum安装MySQL5.7
	yum install mysql-community-server

 
	报错； 您可以尝试添加 --skip-broken 选项来解决该问题  您可以尝试执行：rpm -Va --nofiles --nodigest
	修改/etc/yum.repos.d/mysql-community.repo 源文件，修改为el/7/
	vim /etc/yum.repos.d/mysql-community.repo 
	
	然后再次执行yum install mysql-community-server
	
	三、启动MySQL
	
		禁用selinux
		setenforce 0
		sed -i '/^SELINUX=/c\SELINUX=disabled' /etc/selinux/config 

		启动mysqld，启动之前先修改/etc/my.cnf配置文件，本文用默认的配置。
		service mysqld start
	
	四、连接MySQL并修改密码
	
		grep "password" /var/log/mysqld.log
		mysql -uroot -p
		
		update user set authentication_string=password('a123456') where user='root';
		update user set host = '%' where user = 'root' and host = 'localhost';
		
		mysql> set global validate_password_policy=0;
		mysql> set global validate_password_length=1;
		mysql> set password=password('a123456');
	
	五、使用Navicat远程连接MySQL报错1103
		
		mysql> grant all privileges on *.* to 'root'@'%' identified by 'Zxcvbnm!@#45678' with grant option;
			   grant all privileges on *.* to 'root'@'%' identified by 'Zxcvbnm!@#45678' with grant option;
			   grant all privileges on *.* to 'root'@'%' identified by 'Zxcvbnm!@#45678';
		mysql> flush privileges; 
	
	开放3306端口；
	[root@iZrj98hvt5pgeax2pgdjw3Z ~]# vi  /etc/sysconfig/iptables

	防火墙开放3306端口
		1、打开防火墙配置文件
		vi  /etc/sysconfig/iptables
		如果没有这个文件，需要安装iptables

		先检查是否安装了iptables
		service iptables status
		安装iptables
		yum install -y iptables
		升级iptables
		yum update iptables 
		安装iptables-services
		yum install iptables-services
		禁用/停止自带的firewalld服务

		停止firewalld服务
		systemctl stop firewalld
		禁用firewalld服务
		systemctl mask firewalld
		开启iptables服务 


		注册iptables服务
		相当于以前的chkconfig iptables on
		systemctl enable iptables.service
		开启服务
		systemctl start iptables.service
		查看状态
		systemctl status iptables.service
		vi /etc/sysconfig/iptables

		2、增加下面一行
		注意：增加的开放3306端口的语句一定要在icmp-host-prohibited之前
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
		
		3、重启防火墙
		service  iptables restart
		附：个人配置



	# Firewall configuration written by system-config-firewall
	# Manual customization of this file is not recommended.
	*filter
	:INPUT ACCEPT [0:0]
	:FORWARD ACCEPT [0:0]
	:OUTPUT ACCEPT [0:0]
	-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	-A INPUT -p icmp -j ACCEPT
	-A INPUT -i lo -j ACCEPT
	-A INPUT -i eth0 -j ACCEPT
	-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
	-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
	-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
	-A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
	-A FORWARD -p icmp -j ACCEPT
	-A FORWARD -i lo -j ACCEPT
	-A FORWARD -i eth0 -j ACCEPT
	-A INPUT -j REJECT --reject-with icmp-host-prohibited
	-A FORWARD -j REJECT --reject-with icmp-host-prohibited
	COMMIT


	实测二:	
	第一步：下载地址；https://dev.mysql.com/downloads/mysql/，可以选择 RPM Bundle,下载完记得解压  tar -xvf xxx.tar
		wget https://downloads.mysql.com/archives/get/p/23/file/mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz
		wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz
		tar -xvf xxx.tar
	
	第二步：卸载旧版本的MySql
	
		查看旧版本MySql： rpm -qa | grep mysql
      	逐个删除掉旧的组件： rpm -e --nodeps {-file-name}

    第三步：使用 rpm 命令安装MySql组件

    	使用命令rpm -ivh {-file-name}进行安装操作。按照依赖关系依次安装rpm包 依赖关系依次为common→libs→client→server

		rpm -ivh mysql-community-common-5.7.22-1.el7.x86_64.rpm
		rpm -ivh mysql-community-libs-5.7.22-1.el7.x86_64.rpm
		rpm -ivh mysql-community-client-5.7.22-1.el7.x86_64.rpm
		rpm -ivh mysql-community-server-5.7.22-1.el7.x86_64.rpm

		注：ivh中， i-install安装；v-verbose进度条；h-hash哈希校验

	第四步：登录并创建MySql密码
	
    	1.启动MySql service mysqld start 或 systemctl start mysqld.service 启动MySQL服务。（如果mysql服务无法启动，就重启一下系统）
 
			systemctl start mysqld.service    启动mysql
			systemctl status mysqld.service   查看mysql状态
			systemctl stop mysqld.service     关闭mysql

			查看mysql进程 ps -ef|grep mysql
			查看3306端口 netstat -anop|grep 3306
			
			
		2.登陆mysql修改root密码
		
        	由于MySQL5.7.4之前的版本中默认是没有密码的，登录后直接回车就可以进入数据库，进而进行设置密码等操作。其后版本对密码等安全相关操作进行了一些改变，在安装过程中，会在安装日志中生成一个临时密码。
			grep 'temporary password' /var/log/mysqld.log  可查询到类似于如下的一条日志记录：
				[root@nfs_client tools]# grep 'temporary password' /var/log/mysqld.log    # 在/var/log/mysqld.log文件中搜索字段‘temporary password’
					2018-07-18T06:02:23.579753Z 1 [Note] A temporary password is generated for root@localhost: n(jPp4l-C33#
			
			n(jPp4l-C33#即为登录密码。使用这个随机密码登录进去，然后修改密码，使用命令： mysql -uroot -p

			'''
			[root@nfs_client tools]# mysql -uroot -p
				Enter password:   # 在这里输入密码
				Welcome to the MySQL monitor.  Commands end with ; or \g.
				Your MySQL connection id is 2
				Server version: 5.7.22
				 
				Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.
				 
				Oracle is a registered trademark of Oracle Corporation and/or its
				affiliates. Other names may be trademarks of their respective
				owners.
				 
				Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
				 
				mysql> quit      # 输入quit 或 exit 都能退出mysql
				Bye
			'''
			
			执行下面的命令修改MySql root密码： alter user root@localhost identified by 'zxcvbnm,./123*';
			
		3.授予root用户远程访问权限：
			mysql> grant all privileges on *.* to root@'%' identified by 'zxcvbnm1238';

		4.刷新权限，使设置生效， OK。
			mysql> flush privileges;
			
		5.在远程机器上测试远程连接：  mysql -h 172.17.39.35 -P 3306 -u root -p
		
		6.使用Navicat进行界面级操作。
			


## 配置运维

使用定时任务与脚本进行操作。

### 安装定时任务

vixie-cron软件包是cron的主程序； 
crontabs软件包是用来安装、卸装、或列举用来驱动 cron 守护进程的表格的程序。

	yum install vixie-cron
	yum install crontabs
	
### 开启定时任务

用以下的方法启动、关闭这个cron服务： 

	service crond start		//启动服务 
	service crond stop		//关闭服务 
	service crond restart	//重启服务 
	service crond reload	//重新载入配置
	service crond status    //查看crontab服务状态


查看crontab服务是否已设置为开机启动，执行命令：
	ntsysv 

加入开机自动启动: 
	chkconfig –level 35 crond on

也可以用设置开机自动启动crond服务: 
	[root@CentOS ~]# chkconfig crond on 



查看各个开机级别的crond服务运行情况 
	[root@CentOS ~]# chkconfig –list crond 
	crond 0:关闭 1:关闭 2:启用 3:启用 4:启用 5:启用 6:关闭 
可以看到2、3、4、5级别开机会自动启动crond服务 

取消开机自动启动crond服务: 
	[root@CentOS ~]# chkconfig crond off

### 设置需要执行的脚本 

新增调度任务可用两种方法： 

	1)、在命令行输入: crontab -e 然后添加相应的任务，wq存盘退出。 
	2)、直接编辑/etc/crontab 文件，即vi /etc/crontab，添加相应的任务。	
	crontab -e配置是针对某个用户的，而编辑/etc/crontab是针对系统的任务
	
查看调度任务 :
	crontab -l //列出当前的所有调度任务 
	crontab -l -u jp //列出用户jp的所有调度任务 

删除任务调度工作: 
	crontab -r //删除所有任务调度工作 

直接编辑 vim /etc/crontab ,默认的文件形式如下：
	前四行是有关设置cron任务运行的环境变量。SHELL变量的值指定系统使用的SHELL环境(该样例为bash shell)，PATH变量定义了执行命令的路径。Cron的输出以电子邮件的形式发给MAILTO变量定义的用户名。如果MAILTO变量定义为空字符串(MAILTO="")，电子邮件不会被发送。执行命令或脚本时HOME变量可用来设置基目录。

	文件/etc/crontab中每行任务的描述格式如下: 
	crontab命令格式：

	M H D m d command
	M: 分（0-59） H：时（0-23） D：天（1-31） m: 月（1-12） d: 周（0-6） 0为星期日(或用Sun或Mon简写来表示) 
	* 代表取值范围内的数字 / 代表"每" - 代表从某个数字到某个数字 , 代表离散的取值(取值的列表), 例如*在指代month时表示每月执行(需要符合其他限制条件)该命令。
	整数间的连字号(-)表示整数列，例如1-4意思是整数1,2,3,4
	符号“/”指定步进设置。“/<interger>”表示步进值。如0-59/2定义每两分钟执行一次。步进值也可用星号表示。如*/3用来运行每三个月份运行指定任务。

	command - 需要执行的命令(可用as ls /proc >> /tmp/proc或 执行自定义脚本的命令) 
	root表示以root用户身份来运行
	run-parts表示后面跟着的是一个文件夹，要执行的是该文件夹下的所有脚本
	以“#”开头的为注释行,不会被执行。


几个例子:
 
	每天早上6点
	0 6 * * * echo "Good morning." >> /tmp/test.txt //注意单纯echo，从屏幕上看不到任何输出，因为cron把任何输出都email到root的信箱了。
 
	每两个小时(第一个为15，指明没两个小时的第15min中执行一次)
	15 */2 * * * echo "Have a break now." >> /tmp/test.txt 
 
	晚上11点到早上8点之间每两个小时和早上八点
	0 23-7/2，8 * * * echo "Have a good dream" >> /tmp/test.txt
 
	每个月的4号和每个礼拜的礼拜一到礼拜三的早上11点
	0 11 4 * 1-3 command line
 
	1月1日早上4点
	0 4 1 1 * command line
 
	每小时（第一分钟）执行/etc/cron.hourly内的脚本
	01 * * * * root run-parts /etc/cron.hourly
 
	每天（凌晨4：02）执行/etc/cron.daily内的脚本
	02 4 * * * root run-parts /etc/cron.daily
 
	每星期（周日凌晨4：22）执行/etc/cron.weekly内的脚本
	22 4 * * 0 root run-parts /etc/cron.weekly
 
	每月（1号凌晨4：42）去执行/etc/cron.monthly内的脚本
	42 4 1 * * root run-parts /etc/cron.monthly
 
	注意:  "run-parts"这个参数了，如果去掉这个参数的话，后面就可以写要运行的某个脚本名，而不是文件夹名。 　
 
	每天的下午4点、5点、6点的5 min、15 min、25 min、35 min、45 min、55 min时执行命令。
	5，15，25，35，45，55 16，17，18 * * * command
 
	每周一，三，五的下午3：00系统进入维护状态，重新启动系统。
	00 15 * *1，3，5 shutdown -r +5
 
	每小时的10分，40分执行用户目录下的innd/bbslin这个指令：
	10，40 * * * * innd/bbslink
 
	每小时的1分执行用户目录下的bin/account这个指令：
	1 * * * * bin/account
 
	每天早晨三点二十分执行用户目录下如下所示的两个指令（每个指令以;分隔）：
	203 * * * （/bin/rm -f expire.ls logins.bad;bin/expire$#@62;expire.1st）　　
 
	每年的一月和四月，4号到9号的3点12分和3点55分执行/bin/rm -f expire.1st这个指令，并把结果添加在mm.txt这个文件之后（mm.txt文件位于用户自己的目录位置）。
	12,553 4-91,4 * /bin/rm -f expire.1st$#@62;$#@62;mm.txt

	

### 自写定时任务 

	每周一，周四 00点 时执行命令（重启动）。
	00 0 * * 1,3,5 root sudo reboot 
	
	
	每周一到周五 的9-15点 的每5分钟 时执行命令（启动脚本-行情监测）。
	25-59/2 9-15 * * 1-5 root sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Quote.sh
	*/3 10-15 * * 1-5 root sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Quote.sh

	每天 的8-23点 的每2分钟 时执行命令（启动脚本-机器人、微信）。
	*/5 8-23 * * * root sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh 
	
	每天 的0点 0分钟 每八个时执行命令（脚本自动更新）。
	00 8,16,21 * * * root sh /root/Public/myPrjs/zxcProj/ReadMe/git_zxcPy.sh
	
	命令： crontab -e
	*/1 8-23 * * * python /root/Public/UpLoad/Temp/hello.py

### 自定义进程CPU占用 
	
	限制进程cpu占用最高50
	cpulimit --pid `ps aux|awk '{if($3 > 60) print $2}'` --limit 50
	

### 脚本启动

git 更新脚本：
	
	sh /root/Public/myPrjs/zxcProj/ReadMe/git_zxcPy.sh

启动脚本
	sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh	(Robot + Weixin)
	sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Quote.sh		(Qoute)
	 

单个启动：
	#启动微信后台
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Weixin/zxcPy.Weixin/myWeixin_ItChat.py

	#启动微信API
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Robot/myRobot_API.py

	#启动行情监测 
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Quote/zxcPy.Quotation/myQuote_Source.py
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Quote/myQuote_API.py
	
	
	#启动阻塞进程 
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Weixin/zxcPy.Weixin/myWeixin_ItChat_Debug.py
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Quote/myQuote_API_Debug.py 

#### 查看进程python：

	ps -ef  | grep python
 
#### 停止脚本的运行：

	kill -9  进程号

	

## 防火墙设置
	原因：因为centos7默认的防火墙是firewalld防火墙，不是使用iptables，因此需要先关闭firewalld服务，或者干脆使用默认的firewalld防火墙。

操作步骤：

	关闭防火墙
	1.systemctl stop firewalld 
	2.systemctl mask firewalld

	--在使用iptables服务,开放443端口(HTTPS)	
	3.iptables -A INPUT -p tcp --dport 443 -j ACCEPT
	  iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
	  iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 15672 -j ACCEPT
	  iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8666 -j ACCEPT
	  iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8668 -j ACCEPT
	  iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8669 -j ACCEPT
		  
	--保存上述规则
	4.service iptables save

	--开启服务
	5.systemctl restart iptables.service
	
## 本地WIFI密码查看命令
	
	windows：netsh wlan show profiles
			 netsh wlan show profiles HUAWEI-NNRZ key=clear

	
