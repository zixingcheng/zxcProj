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
	方式一：将下载的安装文件    放入linux 目录

	执行：yum install esl-erlang_21.0.5-1_centos_7_amd64.rpm

	    一路通行之后执行： erl -version 检查是否安装成功，如果提示如图：则表示成功


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

	/opt/python3.5/bin/pip3 install --upgrade pip
	ln -s /opt/python3.5/bin/pip /usr/bin/pip
	
	
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

	每周一到周五 的9-15点 的每5分钟 时执行命令（启动脚本-行情监测）。
	*/1 9-15 * * 1-5 sh /root/Public/UpLoad/Temp/ReadMe/run_zxcPy_Quote.sh

	每天 的8-23点 的每2分钟 时执行命令（启动脚本-机器人、微信）。
	*/5 8-23 * * * sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh 
	
	每天 的0点 0分钟 时执行命令（脚本自动更新）。
	00 0 * * 5 sh /root/Public/myPrjs/zxcProj/ReadMe/git_zxcPy.sh
	
	命令： crontab -e
	*/1 8-23 * * * python /root/Public/UpLoad/Temp/hello.py

### 脚本启动

git 更新脚本：
	
	sh /root/Public/myPrjs/zxcProj/ReadMe/git_zxcPy.sh

启动脚本
	sh /root/Public/myPrjs/zxcProj/ReadMe/run_zxcPy_Robot.sh	(Robot+Weixin)
	sh /root/Public/UpLoad/Temp/ReadMe/run_zxcPy_Quote.sh		(Qoute)
	 

单个启动：
	#启动微信后台
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Weixin/zxcPy.Weixin/myWeixin_ItChat.py

	#启动微信API
	python /root/Public/myPrjs/zxcProj/src/Zxc.Python/zxcPy.Robot/myRobot_API.py

	#启动行情监测 
	python /root/Public/myPrjs/zxcProj/src/zxcPy.Quote/zxcPy.Quotation/myQuote_Source.py

#### 查看进程python：

	ps -ef  | grep python
 
#### 停止脚本的运行：

	kill -9  进程号


