:: zxcpy依赖库安装
:: pip升级
python -m pip install --upgrade pip


:: 区间处理库
pip install interval

:: Excel操作库
pip install xlrd
pip install xlwt


:: PythonWEB框架
pip install flask

:: Web页面操作模块
pip install requests
pip install urllib3


:: 微信模块 
pip install itchat
pip install flask-restful
pip install flask_wtf

:: RabbitMQ python模块 
pip install pika

:: 语音生成 baidu python模块 
pip install baidu-aip
pip install scipy
pip install pydub


:: 股票行情模块 
pip install jqdatasdk


:: 数学操作相关模块 （重装 pandas，跟jqdatasdk版本冲突)
pip uninstall pandas
pip install pandas==0.25.3
pip install matplotlib


:: 数据库操作相关模块 
pip install pymysql

