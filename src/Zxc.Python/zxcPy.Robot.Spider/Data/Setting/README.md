# 行情设置
	http://127.0.0.1:8667/zxcAPI/robot/stock/QuoteSet?setInfo={'spiderName': "ceshi2", 'spiderTag': 'webPage', 'spiderUrl': "", "spiderRule": "", 'isValid':'False', 'isDel':'True', "timeSet" = "* * * * *", 'mark':'测试设置' }

## 行情设置-查询
	http://127.0.0.1:8667/zxcAPI/robot/stock/QuoteSet/Query?spiderName=sh000001
	
# 股票模糊查
	http://127.0.0.1:8667/zxcAPI/robot/stock/Query?code_id=sh.000001&code_name=
	
# 行情查询
	http://127.0.0.1:8667/zxcAPI/robot/quote/Query?queryIDs=sh.000001