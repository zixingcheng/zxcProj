# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-07-22 20:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    注册表操作 
"""
import winreg

#创建专属注册表信息
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software")
key = winreg.CreateKey(key,"zxcSoft")
key = winreg.CreateKey(key,"Monitor")


#自封装注册表操作  
class myRegistry():
    def __init__(self, keyBase='Test', intHKEY=winreg.HKEY_CURRENT_USER): 
        self.keyRoot = r"Software\zxcSoft\Monitor"
        self.keyBase = keyBase
        self.typePath = intHKEY

        self.key = self.addKey(keyBase)
        self.keyPath = "Software\\zxcSoft\\Monitor\\" + keyBase

    #获取默认Key
    def getKey(self, namePath = ""):
        if(namePath == ""):
            namePath = self.keyRoot
        key = winreg.OpenKeyEx(self.typePath, namePath)
        return key
    #获取键值
    def getValue(self, valueName, key = -1):
        if(key == -1):
            key = self.getKey()
        data = ["", 1]
        try:
            data = winreg.QueryValueEx(key, valueName)
        except:
            pass
        return data

    #添加新键
    def addKey(self, name, key = -1):
        if(key == -1):
            key = self.getKey()
        newKey = winreg.CreateKey(key, name)
        return newKey
    #添加新键值
    def setValue(self, valueName, value, key = -1):
        if(key == -1):
            key = self.getKey()
        return winreg.SetValueEx(key, valueName, 0, winreg.REG_SZ, value)

    #删除键
    def delKey(self, name, key = -1):
        if(key == -1):
            key = self.getKey()
        return winreg.DeleteKey(key, name)
    #删除键值
    def delValue(self, name, key = -1):
        if(key == -1):
            key = self.getKey()
        return winreg.DeleteValue(key, name)
        

#测试
if __name__ ==  "__main__":
    pReg = myRegistry()
    res = pReg.setValue("TestValue", "value", pReg.key)
    res = pReg.setValue("TestValue2", "value2", pReg.key)

    data = pReg.getValue("TestValue2", pReg.key)

    pReg.delKey("Test")

