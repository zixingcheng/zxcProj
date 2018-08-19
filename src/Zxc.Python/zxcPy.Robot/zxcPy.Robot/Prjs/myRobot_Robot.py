#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--聊天机器人
"""
import sys, ast, os, time ,mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myRobot, myData_Json, myDebug, myWeb_urlLib
from myGlobal import gol   

    
#机器人类--聊天机器人
class myRobot_Robot(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "聊天机器人"     #说明 
        self.prjName = "聊天机器人"     #功能名
        self.doCmd = "@@ChatRobot"      #启动命令 

        #创建机器人api  
        self.apiRobot = myWeb_urlLib.myWeb("http://openapi.tuling123.com", "", False)    #图灵机器人
        self.apiKeys = ["de79dec1dc6b41f59ed3e4c743b1f089", "de79dec1dc6b41f59ed3e4c743b1f089", "45722107eece483baae1d36a82e33fc1"]
        self.apiKey_ind = 0
        self.data = {
	                    "reqType":0,
                        "perception": {
                            "inputText": {
                                "text": "附近的酒店"
                            }
                        },
                        "userInfo": {
                            "apiKey": "de79dec1dc6b41f59ed3e4c743b1f089",
                            "userId": "zxcRobot"
                        }
                    }
        self.data = {
                        "key": self.apiKeys[self.apiKey_ind],
	                    "info": "",
	                    "loc": "",
	                    "userid": "zxcRobot"
                    }


    #消息处理接口
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = "", usrID = "", usrName = ""):
        #聊天机器人(接入第三方接口进行处理)
        strText = self._Done_ByTuling(Text)
        return strText 

    def _Title_User_Opened(self): 
        return "发送任何消息均机器人回复..."
    
    #图灵机器人
    def _Done_ByTuling(self, Text):
        #组装post数据
        #self.data["perception"]["inputText"] = Text
        self.data["info"] = Text

        #请求数据
        data = self.apiRobot.Do_Post("openapi/api", self.data, "myRobot_Robot")
        body = data.decode(encoding = "utf-8")
        msg = ast.literal_eval(body) 

        #key超过次数
        if(msg['code'] == 40004):
            self.apiKey_ind += 1
            if(self.apiKey_ind >= len(self.apiKey_ind)):
                return "累了，不想说话。。。"
            self.data["key"] = self.apiKeys[self.apiKey_ind]
        return msg['text']
         

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Robot("zxc", "zxcID");
    pp = pR.Done("@@ChatRobot")
    myDebug.Debug(pR.Done("Hello"))
    myDebug.Debug(pR.Done("北京 天气"))
    myDebug.Debug(pR.Done("光山 天气"))
    pR.Done("@@ChatRobot")
    print()

    time.sleep (2)
    pp = pR.Done("Hello")
    print(pp)
    
    pR.Done("@@ChatRobot")
    pR.Done("@@ChatRobot")
    print()
    
