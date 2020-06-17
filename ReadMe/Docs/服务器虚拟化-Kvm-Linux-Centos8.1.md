# 服务器虚拟化Kvm部署说明

## 安装系统

	物理机使用linux centos8.1及以上, 官网下载： https://www.centos.org/download/
		
### 图形界面
	系统安装时，可以选择安装图形化，则无需下面操作。	 
		 
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


## 安装KVM与配置

1. 查看系统版本

	cat /etc/centos-release

2. 查看是否支持kvm模块

	lsmod |grep kvm
	
3. 关闭防火墙和系统增强功能，可以忽略

	systemctl stop firewalld
	systemctl disable firewalld
	
	vi /etc/selinux/config
	将SELINUX=enforcing改为SELINUX=disabled，重启计算机生效。
	
4. KVM管理软件安装

	yum -y install qemu-kvm  libvirt libvirt-daemon  libvirt-client  libvirt-daemon-driver-qemu  virt-manager virt-install  virt-viewer virt-v2v

	软件包介绍：
		qemu-kvm: 为kvm提供底层仿真支持；
		libvirt-daemon: libvirtd守护进程，管理虚拟机；
		libvirt-client: 用户端软件，提供客户端管理命令；
		libvirt-daemon-driver-qemu: libvirtd连接qemu的驱动；
		libvirt: 虚拟管理模块；
		virt-manager: 图形界面管理工具；
		virt-install: 虚拟机命令行安装工具；
		virt-v2v: 虚拟机迁移工具；

5. 启动KVM并设为开机启动

	systemctl start libvirtd 
	systemctl enable libvirtd

6. 安装完成，验证命令是否可用

	virsh list --all

7. 创建虚拟机

	virt-install --name=test01 --memory=512,maxmemory=1024 --vcpus=1,maxvcpus=2 --os-type=linux --os-variant=rhel7 --location=/kvm_data/iso/CentOS-7-x86_64-DVD-1810.iso --disk path=/kvm_data/img/test01.img,size=10 --bridge=br0 --graphics=none --console=pty,target_type=serial --extra-args="console=tty0 console=ttyS0"
	
	图形界面管理工具命令：	virt-manager		
	
	*注：命令方式创建比较麻烦，可使用图形界面管理工具进行操作。
	
	
### 安装Web控制台Cockpit
	
1. 安装Cockpit

	yum install cockpit

2. 安装好 cockpit，Web控制台默认情况下未启动，你使用以下命令启用它：

	systemctl enable --now cockpit.socket
	
3. 虚拟机模块安装

	yum install cockpit-machines
	
4. Web控制台
	
	打开Web浏览器， cockpit使用9090端口，例如：https://127.0.0.1:9090
	
*注：web控制台查看、管理比较方便，但创建虚拟机可能不成功，优先使用


### 安装VNC与配置

1. 安装VNC

	yum install -y tigervnc-server

2. 编辑VNC配置

	拷贝一个新的配置文件，以开启1号窗口为例（想要同时开启多个窗口，修改其中数字即可）
	cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@:1.service
	
	编辑配置：
	vi /etc/systemd/system/vncserver@:1.service

	将文中的“<USER>”替换为你系统的用户名root
	```
		[Unit]
		Description=Remote desktop service (VNC)
		After=syslog.target network.target

		[Service]
		Type=simple

		# Clean any existing files in /tmp/.X11-unix environment
		ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'
		ExecStart=/usr/bin/vncserver_wrapper <USER> %i   		#将文中的“<USER>”替换为你系统的用户名root

		ExecStop=/bin/sh -c '/usr/bin/vncserver -kill %i > /dev/null 2>&1 || :'

		[Install]
		WantedBy=multi-user.target
		
	```
	
3. 更新配置文件

	systemctl daemon-reload		//重新加载服务
	
4. 启动VNC
	
	vncserver :1　　			//启动VNC :1
	
	[root@localhost ~]# vncserver :1
	```
		Warning: localhost.localdomain:1 is taken because of /tmp/.X11-unix/X1
		Remove this file if there is no X server localhost.localdomain:1
		A VNC server is already running as :1

		Warning: localhost.localdomain:1 is taken because of /tmp/.X11-unix/X1
		Remove this file if there is no X server localhost.localdomain:1

		You will require a password to access your desktops.	//提示需要密码

		Password:
		Verify:
		Would you like to enter a view-only password (y/n)? n
		A view-only password is not used
		xauth:  file /root/.Xauthority does not exist

		New 'localhost.localdomain:2 (root)' desktop is localhost.localdomain:2

		Creating default startup script /root/.vnc/xstartup
		Creating default config /root/.vnc/config
		Starting applications specified in /root/.vnc/xstartup
		Log file is /root/.vnc/localhost.localdomain:2.log
	```
	
	设置root的vncserver密码: 
	vncpasswd 			//上面已经设置，可以修改密码
	
5. 启动服务并设为开机启动

	systemctl start vncserver@:1.service
	systemctl enable vncserver@:1.service

6. 开放VNC的端口

	ss -antup | grep vnc　　//看一下VNC的端口号，注意可能不同
	```		
	tcp LISTEN 0 5 *:5901 *:* users:(("Xvnc",pid=6913,fd=9))
	tcp LISTEN 0 128 *:6001 *:* users:(("Xvnc",pid=6913,fd=6))
	tcp LISTEN 0 5 :::5901 :::* users:(("Xvnc",pid=6913,fd=10))
	tcp LISTEN 0 128 :::6001 :::* users:(("Xvnc",pid=6913,fd=5))
	```	
* 参见：防火墙设置，增加iptables对应端口开放设置。

7. 使用VNC Viewer软件连接
	
	下载地址：https://www.realvnc.com/download/file/viewer.files/VNC-Viewer-6.20.113-Windows.exe


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
	chkconfig crond on 

	查看各个开机级别的crond服务运行情况：
	chkconfig –list crond 
		crond 0:关闭 1:关闭 2:启用 3:启用 4:启用 5:启用 6:关闭 
		可以看到2、3、4、5级别开机会自动启动crond服务 

	取消开机自动启动crond服务: 
	chkconfig crond off

### 设置需要执行的脚本 

1. 新增调度任务可用两种方法： 

	1)、在命令行输入: crontab -e 然后添加相应的任务，wq存盘退出。 
	2)、直接编辑/etc/crontab 文件，即vi /etc/crontab，添加相应的任务。	
	crontab -e配置是针对某个用户的，而编辑/etc/crontab是针对系统的任务
	
	查看调度任务 :
	crontab -l 			//列出当前的所有调度任务 
	crontab -l -u jp 	//列出用户jp的所有调度任务 

	删除任务调度工作: 
	crontab -r 			//删除所有任务调度工作 

2. 直接编辑 vim /etc/crontab ,默认的文件形式如下：

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


3. 几个例子:
 
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
	

## 防火墙设置
	原因：因为centos默认的防火墙是firewalld防火墙，不是使用iptables，因此需要先关闭firewalld服务，或者干脆使用默认的firewalld防火墙。

### 防火墙安装

1. 先检查是否安装了iptables
	
	service iptables status
	
2. 安装iptables
	
	yum install -y iptables
	
3. 升级iptables，新装则忽略
	
	yum update iptables 
	
4. 安装iptables-services

	yum install iptables-services
	
5. 禁用/停止自带的firewalld服务

	systemctl stop firewalld
	systemctl mask firewalld

6. 开启iptables服务 

	systemctl enable iptables.service
	systemctl start iptables.service
	systemctl status iptables.service
	systemctl stop iptables.service
	
	
### 防火墙配置

1. 打开配置文件

	vi /etc/sysconfig/iptables
	 
2. 编辑配置信息

	增加下面一行：
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
		
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 5901 -j ACCEPT
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 5902 -j ACCEPT
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 6001 -j ACCEPT
		-A INPUT -m state --state NEW -m tcp -p tcp --dport 6002 -j ACCEPT
		
3. 命令添加配置信息

	iptables -A INPUT -p tcp --dport 443 -j ACCEPT
	iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
	iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 15672 -j ACCEPT
		
	--保存上述规则
	service iptables save
	
4、重启防火墙
	
	service  iptables reload
	service  iptables restart


## 其他


### 文件互传

使用pscp，pscp.exe属于Putty的重要组件工具之一，同时也可以单独使用，可以通过pscp.exe实现本地windows下的文件下载、上传到linux上，有需要的赶快下载吧！

配置如下.bat文件，可实现本地与linux远程目录的上下同传：

	echo ******|pscp -r D:\UpLoad\Temp root@39.105.196.175:/root/Public/UpLoad			(本地上传至Linux)
	echo ******|pscp -r root@39.105.196.175:/root/Public/UpLoad/Updata D:\UpLoad\		(本地下载Linux)
		  
* 直接使用bat文件进行执行，更方便，亦可手动操作。

	
### 查看进程python：

	ps -ef  | grep python
 
### 停止脚本的运行：

	kill -9  进程号
	
### 本地WIFI密码查看命令
	
	windows：netsh wlan show profiles
			 netsh wlan show profiles HUAWEI-NNRZ key=clear

	
