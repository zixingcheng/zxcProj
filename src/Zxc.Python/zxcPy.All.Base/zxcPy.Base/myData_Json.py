# -*- coding: utf-8 -*-
"""
Created on  张斌 2017-10-07 14:05:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com
    @参考资料: http://blog.csdn.net/gamer_gyt/article/details/53577477
               http://python3-cookbook.readthedocs.io/zh_CN/latest/c06/p02_read-write_json_data.html
    
    Json操作，自定义Json对象，Json_Object 顺序输出，Json_Object2失败为乱序(暂留，但不使用便于知识积累)
""" 
import os, json
from collections import OrderedDict


#自定义Json对象--无序失败(Dict无法实现无序)
class Json_Object2:        
    def __init__(self, pDict = {}):
        self.__dict__ = pDict 

    #转换为字符串   
    def ToString(self):
        strJson = json.dumps(self, default = __serialize_instance__, indent = 4) 
        return strJson



#自定义Json对象 
class Json_Object:        
    def __init__(self, pDict = OrderedDict()):
        #setattr(self, "_dict_" ,pDict)
        self._dict_ = pDict        
        self.Trans_FromStr('{}')
        

    #字符串转Json对象
    def Trans_FromStr(self,  objStr):
        #去除BOM头
        if objStr.startswith(u'\ufeff'): 
            objStr = objStr.encode('utf8')[3:].decode('utf8')
            
        #字符串转对
        data = json.loads(objStr, object_pairs_hook = OrderedDict)
        self._dict_ = data 
        
        #print(json.dumps(data, indent = 4))
        return data

    #转换为字符串   
    def ToString(self, decode = 'unicode_escape', ispretty = True):
        strJson = json.dumps(self._dict_, default = __serialize_instance__, indent = 4)

        #中文编码解码
        if(decode != ""):
            strJson =  strJson.encode('utf-8').decode(decode)

        #漂亮输出
        if(ispretty):
            lines = strJson.split("\n")
            strPretty = ""
            strPreffix = ""
            nCheck = 0
            for strline in lines: 
                if(strline.find(":") > 0):
                   
                    temps = strline.split(":")
                    temp = temps[1].strip()
                    if(temp == "["):    #修正[：同行
                        nCheck = 1
                        strPreffix = temps[0][0 : (temps[0].count(" "))]
                        strPretty += strline.replace("\r","")
                        continue
                    elif(temp == "{"):   #修正{：换行，步进
                        strPretty += temps[0] + ":\n"
                        strPretty += temps[0][0 : (temps[0].count(" ") - 1)] 
                        strPretty += temps[1] + "\n" 
                        continue

                if(nCheck == 1):
                    temp = strline.strip()
                    if(temp == "{"):         #屏蔽数组复杂对象
                        strPretty = strPretty[:-1] + "\n"
                        strPretty += strPreffix + "[\n" 
                        strPretty += strline + "\n"
                        nCheck = 0 
                        continue
                    
                    #修正[：同行     
                    strPretty += " " + temp.replace("\r","").replace("\n","")  
                    if(temp.count("]") == 1):
                        nCheck = 0 
                        strPretty += "\n"
                    continue
                strPretty += strline + "\n"
            strJson = strPretty        
        return strJson 
    
    #增加Json对象   
    def Add_Json(self, key, value):  
        data = json.loads(value.ToString(), object_pairs_hook = OrderedDict)
        self[key] = data;
        

    #获取所有键值
    def GetKeys(self):        
        return self._dict_.keys() 
    def GetKeys_Child(self, value):   
        if(self.IsObject(value) == False): return []; 
        dict0 = OrderedDict(value)
        return list(dict0.keys())
    def GetItems(self):        
        return self._dict_.items() 
    
    #是否为数组
    def IsArray(self, value):   
        strJosn = str(value)  
        if(strJson[0:1] == "["):
            return True
        else: return False
    #是否为Object
    def IsObject(self, value):   
        strJson = str(value)  
        if(len(strJson) > 11 and strJson[0:11].lower() == "ordereddict"):
            return True
        else: return False


    def __getitem__(self, key):
        return self._dict_[key]       
    def __setitem__(self, key, value):
        self._dict_[key]  = value 
    def __delitem__(self, key):
        self._dict_.__delitem__(key)

    #属性不存在时调用
    def __getattr__(self, item):
        #setattr(self, key, self._dict_[key]) 
        #return getattr(self, key, setattr(self, key, value)) 
        
        #print("%s %s" % (item, item))
        return self._dict_[item]
    def __setattr__(self, item, value):  
        #setattr(self, "_dict2_" ,"dd")
        
        #print("%s %s" % (item, value))

        #增加自类型操作
        #if(str(type(value) == Json_Object):       
        #    data = json.loads(value.ToString(), object_pairs_hook = OrderedDict)
        #    print(str(typeof(value)).replace(".",""))
        #    print("ddddddddddddddddddddddddddd" + data)
        #    value = data       
        
        self.__dict__[item] = value
        if(item != "_dict_"):
            self._dict_[item]  = value  
        
#字符串转Json对象
def Trans_ToJson(objStr):
    #字符串转对象
    #data = json.loads(objStr, object_hook = Json_Object2)
    data = json.loads(objStr, object_hook = OrderedDict)
    return data

    
#序列化对象实例，提供一个函数，它的输入是一个实例，返回一个可序列化的字典
def __serialize_instance__(obj):
    #d = { '__classname__' : type(obj).__name__}
    d = OrderedDict()
    #d = {}
    d.update(vars(obj))
    return d
 
    
if __name__ == "__main__":
    #实例json对象
    s = '{"name":"Think","share":50, "price":12,"array" : [1,2,3,4], "array2" : [{"aa2":0},{"aa3":0}]}'
    ss = U'{"name":"Think","share":50, "price":12, "other":{"H":"a","GG":"aa","A":"aa"},"other2" : [{"aa2":0},{"aa3":0}]}'

    #无子节点顺序测试
    data = json.loads(s, object_pairs_hook = OrderedDict)
    data ["aa"] ="d"
    print("无子节点顺序测试：")
    print(type(data))
    print(json.dumps(data, indent = 4))


    #完整Json对象(无序)-测试
    pJson = Json_Object()
    pJson.Trans_FromStr(ss)
    
    pJson["bb"] = "aa"
    pJson.__delitem__("bb")
    pJson.aa = 100
    pJson.a = "aaa"
    setattr(pJson, "dd" ,111)
    pJson.obj = data
    pJson.bl = True
    
    pJson2 = Json_Object()
    pJson2.aa = "aa"
    pJson2.bb = False
    pJson.Add_Json("obj2",pJson2) 
    
    
    keys = pJson.GetKeys()
    print(keys)

    print(pJson["other"])
    li = pJson.GetKeys_Child(pJson["other"])
    st = str(pJson["other2"])
    
    print("完整Json对象(无序)-测试：")
    print(pJson )
    print(pJson.dd )
    print(pJson.name )
    print(pJson.__dict__)
    print(pJson.ToString() )
    
    
    #字符串转对象-无序失败
    data = json.loads(s, object_hook = Json_Object2)
    print("字符串转对象,顺序测试：")
    print(type(data))
    print(data)
    #print(data.name)
    #print(data.price)
    print(json.dumps(data, default = __serialize_instance__, indent = 4))

 
    #转换为Json对象-无序失败
    print("字符串转复杂对象,顺序测试：")
    pJson2 = Json_Object2()
    pJson2 = json.loads(ss, object_hook = Json_Object2) 
    print(pJson2.ToString())
    
    pJson2.pp = "pp"
    print(pJson2.ToString())



    pJson3 = Json_Object()
    pJson3 = Trans_ToJson('{"name":"Think","share":50, "price":12}')
    print(pJson3)
    print(type(pJson3))
    
    pJson3 = Trans_ToJson('["2016-11-24","2016-11-22","2016-11-23"] ')
    print(pJson3)
    print(type(pJson3))
    if(type(pJson3)== list):
        print(type(pJson3))

    lista = []
    lista = pJson3;
    print(pJson3)


    s1 = u'话大地方法'
    b = s1.encode('utf-8')
    c = b.decode('utf-8')
    print(s1)
    print(type(s1))
    print(b)
    print(type(b))
    print(c)
    print(type(c))
    
 
