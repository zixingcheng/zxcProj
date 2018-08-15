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

使用API（myRobot_API.py），或直接使用消息队列方式（myRobot_Reply_MQ.py）

···
API： 使用myRobot_Reply来作处理，并将处理消息发送给消息管理器
队列： 使用myRobot_Reply_MQ，通过MQ队列（zxcMQ_robot）监听需处理消息
消息管理器： 使用myManager_Msg，自动转发消息(需注册平台转发api或消息队列)
···
