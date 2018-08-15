# 依赖库

## Flask (0.12.2)
	itsdangerous (0.24)
	Jinja2 (2.9.6)
	Werkzeug (0.12.2)
	click (6.7)
	MarkupSafe (1.0)
	
## Flask-RESTful (0.3.6)
	six (1.10.0)
	Flask (0.12.2)
	pytz (2016.7)
	aniso8601 (1.3.0)
	itsdangerous (0.24)
	Jinja2 (2.9.6)
	Werkzeug (0.12.2)
	click (6.7)
	MarkupSafe (1.0)
	python-dateutil (2.6.0)
	

#通讯说明

主程序：myWeixin_ItChat.py, 支持消息队列（优先）或共享内存(需配和api使用)
API（myWeixin_API.py），支持消息队列或共享内存，消息队列接口也可通过直接写消息队列数据实现，只是对外接口
消息处理：myReply_Factory.py，调用robotAPI或发送消息队列（zxcMQ_robot）


···
API： 接口转发消息到myWeixin_ItChat来作处理（共享内存/消息队列）
队列： 使用myWeixin_ItChat，通过MQ队列（zxcMQ_wx）监听需发送消息
消息管理器： 使用myManager_Msg，自动转发消息(需注册平台转发api或消息队列)
···