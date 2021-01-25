# GIS底层库GDAL及依赖库编译--windows

GDAL依赖库有Curl、tiff、sqlite3、Proj等，可以直接使用Proj编译进行整体下载。

## 编译依赖库 PROJ

参照官方windows编译部署文档：
https://proj.org/install.html#building-on-windows-with-vcpkg-and-visual-studio-2017-or-2019

### 安装git

安装 [git](https://git-scm.com/download/win) 

### 安装Vcpkg
假设有ac：\ dev目录

```
	cd c:\dev
	git clone https://github.com/Microsoft/vcpkg.git

	cd vcpkg
	.\bootstrap-vcpkg.bat
```

### 安装PROJ依赖项

```
	vcpkg.exe install sqlite3[core,tool]:x86-windows tiff:x86-windows curl:x86-windows
	vcpkg.exe install sqlite3[core,tool]:x64-windows tiff:x64-windows curl:x64-windows
```
* 注意: 自从PROJ 7.0起，才需要依赖于tiff和curl。
* 注意: 实际库有jpeg.lib、libcurl.lib、lzma.lib、sqlite3.lib、tiff.lib、tiffxx.lib、turbojpeg.lib、zlib.lib。

### 下载PROJ来源

```
	cd c:\dev
	git clone https://github.com/OSGeo/PROJ.git
```

### 构建项目

```
	cd c:\dev\PROJ
	mkdir build_vs2019
	cd build_vs2019
	cmake -DCMAKE_TOOLCHAIN_FILE=C:\dev\vcpkg\scripts\buildsystems\vcpkg.cmake ..
	cmake --build . --config Debug -j 8
	cmake --build . --config Release -j 8
```

### 运行PROJ测试

```
	cd c:\dev\PROJ\build_vs2019
	ctest -V --build-config Debug
```

## 编译 GDAL (C++版)

### 下载GDAL来源

```
	cd c:\dev
	git clone https://github.com/zixingcheng/gdal.git

```

### 配置编译文件

1、进入库文件夹中，找到nmake.opt文件，用文本编译器（notepad++）或者vs打开。

```
第41行，设置MSVC_VER=设置为1920(VS2019版本，根据编译器来确定)。
	!IFNDEF MSVC_VER
	# assume msvc VS2019.
	MSVC_VER=1920
	!ENDIF
第57行，设置GDAL_HOME =生成文件的路径。
	!IFNDEF GDAL_HOME
	GDAL_HOME = "D:\myCode\zxcProj\src\Zxc.C++\src.Open\gdal\Build"
第210行，WIN64=为YES启动64位编译。
	# (x64). You'll need to have PATH, INCLUDE and LIB set up for 64-bit
	# compiles.
	WIN64=YES
	# Capture WIN64=1 if specified in NMAKE command line
	!IFDEF WIN64
	WIN64=YES
	!ENDIF
第218行，设置DLLBUILD=为1启动动态编译（dll）、 0为静态编译。
	!IFNDEF GDAL_LIB_NAME
	!IF "$(DLLBUILD)" == "1"
	# Uncomment the following if you are building for 64-bit windows	
第238行，将PROJ_INCLUDE PROJ_LIBRARY,分别设置为解压PROJ时的include(-I后为地址）和 lib文件路径。（proj路径）
	# PROJ stuff (required dependency: PROJ >= 6)
	# PROJ_INCLUDE = -Id:\install-proj\local\include
	PROJ_INCLUDE = -I D:\myCode\zxcProj\src\Zxc.C++\src.Open\PROJ\src
	
	# Note: add shell32.lib is needed starting with PROJ 7.0 in some circumstances
	# for static linking. See https://github.com/OSGeo/gdal/issues/2488
	# And ole32.lib also since PROJ 7.1 (see https://github.com/OSGeo/gdal/issues/2743)
	# PROJ_LIBRARY = d:\install-proj\local\lib\proj_6_0.lib shell32.lib ole32.lib
	PROJ_LIBRARY = d:\myCode\zxcProj\src\Zxc.C++\src.Open\vcpkg\installed\x64-windows\lib\proj_d.lib d:\myCode\zxcProj\src\Zxc.C++\src.Open\vcpkg\installed\x64-windows\lib\libcurl.lib 
	
第509行，设置SQLITE_INC SQLITE_LIB,路径同上。（sqlite路径）
	# SQLite Libraries
	# SQLITE_INC=-IN:\pkg\sqlite-win32
	# SQLITE_LIB=N:\pkg\sqlite-win32\sqlite3_i.lib
	SQLITE_INC = -I D:\myCode\zxcProj\src\Zxc.C++\src.Open\BUILD\SQLite3\include
	SQLITE_LIB = D:\myCode\zxcProj\src\Zxc.C++\src.Open\BUILD\SQLite3\lib\SQLite3.lib 
```

* 具体行数对于不同版本配置文件会有所不同，可按键名搜索进行设置。

2、打开x64 Native Tools Command Prompt for VS 2019进入库文件夹（nmake.opt所在文件夹），输入命令：
（也可以使用VCVARS64.BAT。以管理员身份执行cmd，（cd命令）找到并运行编译器下的VCVARS64.BAT。可在vs安装目录下搜索）

```
	nmake -f makefile.vc    
	nmake -f makefile.vc install		--- C#编译使用
	nmake -f makefile.vc devinstall		--- C#编译使用

	debug版：
	nmake /f makefile.vc DEBUG=1  
	nmake /f makefile.vc DEBUG=1 install  
	nmake /f makefile.vc DEBUG=1 devinstall
	
	同时还有其他的命令，如：
	nmake -f makefile.vc clean
```

3、常见错误问题

	a). libcurl报错，缺失符号之类;
		-- PROJ_LIBRARY 里增加 libcurl.lib 路径进行链接；

## 编译 GDAL (C#版)

### 下载swig

下载swig：http://prdownloads.sourceforge.net/swig/swigwin-3.0.12.zip 并解压，将swig.exe根目录设置为path下的环境变量。

### 增加算法swig进行编译

1、修改 /swig/include/Operations.i 编译文件，增加 GridCreate 函数的wrap实现；

```
/************************************************************************/
/*                             GridCreate()                             */
/************************************************************************/

#ifdef SWIGJAVA
%rename (GridCreate) wrapper_GridCreate;
%apply (int nCount, double *x, double *y, double *z) { (int points, double *x, double *y, double *z) };
%apply (void* nioBuffer, long nioBufferSize) { (void* nioBuffer, long nioBufferSize) };
%inline %{
int wrapper_GridCreate( char* algorithmOptions,
                        int points, double *x, double *y, double *z,
                        double xMin, double xMax, double yMin, double yMax,
                        int xSize, int ySize, GDALDataType dataType,
                        void* nioBuffer, long nioBufferSize,
                        GDALProgressFunc callback = NULL,
                        void* callback_data = NULL)
{
    GDALGridAlgorithm eAlgorithm = GGA_InverseDistanceToAPower;
    void* pOptions = NULL;

    CPLErr eErr = CE_Failure;

    CPLErrorReset();

    if (xSize * ySize * (GDALGetDataTypeSize(dataType) / 8) > nioBufferSize)
    {
        CPLError( eErr, CPLE_AppDefined, "Buffer too small" );
        return eErr;
    }

    if ( algorithmOptions )
    {
        eErr = ParseAlgorithmAndOptions( algorithmOptions, &eAlgorithm, &pOptions );
    }
    else
    {
        eErr = ParseAlgorithmAndOptions( szAlgNameInvDist, &eAlgorithm, &pOptions );
    }

    if ( eErr != CE_None )
    {
        CPLError( eErr, CPLE_AppDefined, "Failed to process algorithm name and parameters.\n" );
        return eErr;
    }

    eErr = GDALGridCreate( eAlgorithm, pOptions, points, x, y, z,
                           xMin, xMax, yMin, yMax, xSize, ySize, dataType, nioBuffer,
                           callback, callback_data );

    CPLFree(pOptions);

    return eErr;
}
%}
%clear (void *nioBuffer, long nioBufferSize);
#endif


#ifndef SWIGJAVA
%feature( "kwargs" ) GridCreate;
#endif
%apply Pointer NONNULL {GDALRasterBandShadow *srcBand};
%apply (double *inout) {(double*)};
%apply (int nList, double *pList ) { (int fixedLevelCount, double *fixedLevels ) };
%inline %{ 
int GridCreate( char* algorithmOptions,
                        int points, double *x, double *y, double *z,
                        double xMin, double xMax, double yMin, double yMax,
                        int xSize, int ySize, GDALDataType dataType,
                        double *nioBuffer, long nioBufferSize,
                        GDALProgressFunc callback = NULL,
                        void* callback_data = NULL)
{
    GDALGridAlgorithm eAlgorithm = GGA_InverseDistanceToAPower;
    void* pOptions = NULL;

    CPLErr eErr = CE_Failure;

    CPLErrorReset();

    if (xSize * ySize * (GDALGetDataTypeSize(dataType) / 8) > nioBufferSize)
    {
        CPLError( eErr, CPLE_AppDefined, "Buffer too small" );
        return eErr;
    }


    if ( algorithmOptions )
    {
        eErr = ParseAlgorithmAndOptions( algorithmOptions, &eAlgorithm, &pOptions );
    }
    else
    {
        eErr = ParseAlgorithmAndOptions( szAlgNameInvDist, &eAlgorithm, &pOptions );
    }
    

    if ( eErr != CE_None )
    {
        CPLError( eErr, CPLE_AppDefined, "Failed to process algorithm name and parameters.\n" );
        return eErr;
    }

    eErr = GDALGridCreate( eAlgorithm, pOptions, points, x, y, z,
                           xMin, xMax, yMin, yMax, xSize, ySize, dataType, nioBuffer,
                           callback, callback_data );

    CPLFree(pOptions);

    return eErr;
}
%}
%clear  (double *x, double *y, double *z);
%clear (void *nioBuffer, long nioBufferSize);

```




### 使用swig进行编译

1、进入C#编译目录，在cmd中输入：

```
	cd swig\csharp
```

2、编译, 在cmd中输入：

```
	nmake /f makefile.vc
```

* 可能会错：NMAKE : fatal error U1073: 不知道如何生成“ogr_wrap.obj”

3、修复错误"U1073", 在cmd中输入：

```
	nmake /f makefile.vc interface
```
* 重新生成swig的wrap接口cpp文件。 
 
4、重新编译，在cmd中输入：

```
	nmake /f makefile.vc
```

5、生成dll文件，在cmd中输入：

```
	nmake /f makefile.vc install
```


# GIS底层库GDAL及依赖库编译--linux-centos7

GDAL依赖库有Curl、tiff、sqlite3、Proj等，未找到整体下载编译方法，需要依次下载编译。

## 编译依赖库 PROJ

参照官方windows编译部署文档--从源代码编译和安装（linux）：
https://proj.org/install.html#building-on-windows-with-vcpkg-and-visual-studio-2017-or-2019

* 官方文档对linux编译说明不清晰，以下面安装说明为准。

### 安装git

centos7升级git版本控制工具

1、第一步卸载原有的git。
```
	yum remove git
```

2、安装相关依赖

```
	yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel asciidoc
	yum install gcc perl-ExtUtils-MakeMaker
```

3、安装git
```
	// 将压缩包解压到/usr/local/src目录 
	wget https://www.kernel.org/pub/software/scm/git/git-2.7.3.tar.gz
	tar -C /usr/local/src -vxf git-2.7.4.tar.gz
	cd /usr/local/src/git-2.7.4
	
	// 编译
	make 		//prefix=/usr/local/git
	
	// 安装
	make install
	
	// 写入到环境变量中（方法一）
	echo "export PATH=$PATH:/usr/local/lib" >> /etc/profile && source /etc/profile
	
	// 写入到环境变量中(方法二)
	export PATH=$PATH:/usr/local/lib
```

4、检查版本
```
	// 查看是否已经安装成功
	git --version
```

### 安装Vcpkg--无效，忽略

假设有ac：\ dev目录

```
	cd c:\dev
	git clone https://github.com/Microsoft/vcpkg.git

	cd vcpkg
	sh bootstrap-vcpkg.sh


	export PATH=/usr/local/bin:$PATH

	export PATH=/root/App/GDAL-Compile/vcpkg/downloads/tools/cmake-3.18.4-linux/cmake-3.18.4-Linux-x86_64/bin:$PATH

```

### 安装PROJ依赖项--无效，忽略

```
	./vcpkg install sqlite3[core,tool]:x86-linux tiff:x86-linux curl:x86-linux
	./vcpkg install sqlite3[core,tool]:x64-linux tiff:x64-linux curl:x64-linux

	./vcpkg install lzma:x64-linux
	./vcpkg install tiff:x64-linux
```
* 注意: 自从PROJ 7.0起，才需要依赖于tiff和curl。
* 注意: 实际库有jpeg.lib、libcurl.lib、lzma.lib、sqlite3.lib、tiff.lib、tiffxx.lib、turbojpeg.lib、zlib.lib。
* 注意：Linux下编译报错的话，检查gcc版本为7.0以上。


### 安装PROJ依赖项-SQLite3

官网 https://www.sqlite.org/download.html 下载 sqlite-autoconf-3340000.tar.gz。

1、解压、进入解压目录、配置安装目录，生成makefile：

```
	cd /root/App/GDAL-Compile
	wget https://www.sqlite.org/*******/sqlite-autoconf-3340000.tar.gz
	
	tar -zxvf sqlite-autoconf-3330000.tar.gz
	cd sqlite-autoconf-3340000/
	
	sudo ./configure
```
 
2、继续编译，安装：

```
	sudo make
	sudo make install
```

3、设置 pkg-config

``` 
	export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/SQLite3/lib/pkgconfig 
``` 
 
### 安装PROJ依赖项-libtiff

1、查看libtiff 可安装列表：

``` 
	yum list | grep "libtiff"
``` 

2、选择64位的进行安装：

``` 
	yum -y install libtiff.x86_64
``` 

### 下载PROJ来源

```
	cd /root/App/GDAL-Compile
	wget https://download.osgeo.org/proj/proj-7.2.0.tar.gz
	
	tar -zxvf proj-7.2.0.tar.gz
	cd proj-7.2.0
```

### 构建项目

1、设置 pkg-config，解决SQLite3已编译但找不到的问题；

```
	//vcpkg安装的路径，无效-忽略
	export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/root/App/GDAL-Compile/vcpkg/install/x64-linux/lib/pkgconfig

	//SQLite3安装路径
	export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/SQLite3/lib/pkgconfig

	//统一安装在 usr/local/lib 
	export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig/

	//增加 PROJ7 的安装路径
	export PKG_CONFIG_PATH=/usr/PROJ7/lib/pkgconfig/:$PKG_CONFIG_PATH
	export PKG_CONFIG_PATH=:$PKG_CONFIG_PATH/usr/local/lib/pkgconfig/
	
	//打印 PKG_CONFIG_PATH，及可找到的 pkg
	echo $PKG_CONFIG_PATH
	pkg-config --list-all
	
	//添加 库的查找路径，最好直接都默认 ./configure 安装到 /usr/local/
	echo /usr/local/lib > /etc/ld.so.conf.d/local.conf
```

* 注意，如果无法找到SQLite3等路径时使用上面命令，否则忽略。


2、编译
``` 
	sudo ./configure 
 
	sudo make
	sudo make install	
```


## 编译 GDAL (C++版)

1、下载GDAL来源

```
	cd /root/App/GDAL-Compile 
	wget https://github.com/OSGeo/gdal/releases/download/v3.2.0/gdal-3.2.0.tar.gz
	
	tar -zxvf gdal-3.2.0.tar.gz
	cd gdal-3.2.0
```

2、编译
``` 
	sudo ./configure
 
	sudo make
	sudo make install
	
```

## 编译 GDAL (C#版)

### 安装swig

1、官网下载swig-4.0.0.tar.gz；

2、解压到指定目录；

3、进入解压后的目录，依次运行指令：
``` 
	bash ./configure --without-pcre【即不需要安装pcre依赖】

	make && make install
``` 

4、配置环境变量：
``` 
	export PATH=/usr/local/swig-4.0.12/bin:$PATH
``` 

5、运行swig -version查看版本信息：
``` 
	SWIG Version 4.0.0

	Compiled with g++ [x86_64-pc-linux-gnu]
``` 

### 安装mono

1、下载mono安装包

在mono官网 http://download.mono-project.com/sources/mono/ 下载需要的程序安装包，下面就以mono-3.12.1.tar.bz2这个文件包为例。

* 可以离线下载，上传到linux再安装。

2、解压程序包
``` 
	tar -jxvf mono-3.12.1.tar.bz2
	
	cd mono-3.12.1
```

3、编译安装
``` 
	./configure --prefix=/usr/local/lib/mono

	make
	make install
```
* 对mono软件进行安装。整个编译安装过程约10到15分钟左右。

4、路径配置

程序编译完成之后，执行“ln -s /usr/local/lib/mono/bin/mono-sgen /usr/bin/mono”命令将mono启动程序添加到系统的搜索路径，然后重启系统或注销重新登录。

5、检查mono是否安装成功
``` 
	mono
```

### 修改 swig 相关配置信息

1、修改 /swig/csharp/GNUmakefile 编译文件，增加-fPIC，便于后续生成.so文件；

```
	%.$(OBJ_EXT): %.cpp
		$(CXX) $(CFLAGS) $(SUPPRESSW) $(GDAL_INCLUDE) -c -fPIC $<

	%.$(OBJ_EXT): %.cxx
		$(CXX) $(CFLAGS) $(SUPPRESSW) $(GDAL_INCLUDE) -c -fPIC $<

	%.$(OBJ_EXT): %.c
		$(CC) $(CFLAGS) $(SUPPRESSW) $(GDAL_INCLUDE) -c -fPIC $<
```

2、修改 /swig/csharp/csharp.opt 编译文件；

```
#
# csharp.opt - C# specific user defined options
#
# $Id$
#

#Uncomment the following line if you want to compile with MONO on windows
MONO = NO

#Comment the following line out if you want to link against the gdal dll
CSHARP_STATIC_LINKAGE = YES

#Uncomment these lines if we are targeting .NET standard/core
NETSTANDARD = netstandard2.0
NETCORE = netcoreapp3.1
```

3、修改 /swig/include/Operations.i 编译文件，增加 GridCreate 函数的wrap实现；

* 具体参见windows版说明。


### 使用swig进行编译

1、进入C#编译目录：

```
	cd swig\csharp
```

2、编译，生成wrap接口文件：

```
	make interface
```

2、编译：

```
	make
```

3、编译生成.so文件；

```
	g++ -fPIC -shared -o libgdalconst_wrap.so gdalconst_wrap.o /usr/local/lib/libgdal.so
	g++ -fPIC -shared -o libgdal_wrap.so gdal_wrap.o /usr/local/lib/libgdal.so
	g++ -fPIC -shared -o libosr_wrap.so osr_wrap.o /usr/local/lib/libgdal.so
	g++ -fPIC -shared -o libogr_wrap.so ogr_wrap.o /usr/local/lib/libgdal.so
```
* 注：可拷贝文件到 /usr/local/lib64/ 将用户用到的库统一放到一个目录

```
	1.将用户用到的库统一放到一个目录，如 /usr/loca/lib64
	# cp libXXX.so.X /usr/loca/lib64/           

	2.向库配置文件中，写入库文件所在目录
	# vim /etc/ld.so.conf.d/usr-libs64.conf    
	/usr/local/lib64  

	3.更新/etc/ld.so.cache文件
	# ldconfig  
```

4、测试：

```
	mono **.exe
```
 
5、常见错误问题

	a). 无法找 *_wrap 动态库，.so文件真实存在;
		-- 可能为动态库的链接，关联库未链接生成；



