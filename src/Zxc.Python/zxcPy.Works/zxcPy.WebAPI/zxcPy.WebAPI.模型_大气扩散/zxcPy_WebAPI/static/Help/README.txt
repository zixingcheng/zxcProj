
# 模型WebAPI-大气扩散模型-高斯
    
    WebAPI路径：注意替换为实际的地址和端口，param为json格式参数，参看模型参数说明。
       http://127.0.0.1:8686/zxcAPI/Model/Leak/<param>
       http://192.168.1.200:8686/static/Help/README.txt
       http://120.197.152.99:18686/static/Help/README.txt
       http://120.197.152.99:18686/zxcAPI/Model/Leak/{"tag": "ADDFSDGDG", "infoLeak": {"longitude": 113.8, "latitude": 22.8, "height_leak": 45, "massrate_leak": 720, "timestart_leak": "2020-06-09 12:00:00", "chimney": {"diameter": 1, "temperature_outlet": 100, "smoke_speed_outlet": 5, "wind_speed_outlet": ""}}, "infoTarget": [{"id": "1", "longitude": 113.83, "latitude": 22.83, "height": 0}, {"id": "2", "longitude": 113.835, "latitude": 22.835, "height": 0}], "infoEnvironment": {"wind_speed": 2, "wind_direction": "SW", "wind_height": 10, "air_stability": "C", "temperature": 26, "cloudy_is": true}}
       http://127.0.0.1:9035/zxcAPI/Model/Leak/{"tag": "ADDFSDGDG", "infoLeak": {"longitude": [113.8,113.8008], "latitude": [22.8,22.80066], "height_leak": 45, "massrate_leak": 10720, "timestart_leak": "2020-06-09 12:00:00", "chimney": {"diameter": 1, "temperature_outlet": 100, "smoke_speed_outlet": 5, "wind_speed_outlet": ""}}, "infoTarget": [{"id": "1", "longitude": 113.83, "latitude": 22.83, "height": 0}, {"id": "2", "longitude": 113.835, "latitude": 22.835, "height": 0}], "infoEnvironment": {"wind_speed": 2, "wind_direction": "SW", "wind_height": 10, "air_stability": "C", "temperature": 26, "cloudy_is": true}}
       

## 模型参数
    
    示例参数：未注明--非必须参数，则为必须参数。
    param = { 
                "tag": "ADDFSDGDG",                                             //计算标识，用于异步调用信息拾取，--非必须参数
                "infoLeak": { 
                                    "longitude": 113.8,                         //泄漏处经度, 可以为线[113.8,113.8008]
                                    "latitude": 22.8,                           //泄漏处纬度, 可以为线[22.8,22.80066]
                                    "height_leak": 45,                          //泄漏处高度(m)，> 0     
                                    "massrate_leak": 720,                       //泄漏质量速率(mg/s)，> 0   
                                    "timestart_leak": "2020-06-09 12:00:00",    //泄漏开始时间
                                    "chimney":{                                 //烟囱信息，--非必须参数，没有烟囱的去除该节点信息
                                            "diameter": 1,                      //烟囱口直径(m)，> 0   
                                            "temperature_outlet": 100,          //烟囱口烟气温度(℃)，> 0  
                                            "smoke_speed_outlet": 5,            //烟囱口烟气速度(m/s)，> 0   
                                            "wind_speed_outlet": ""             //烟囱口风速(m/s)，--非必须参数，> 0   
                                    }
                               },
                  "infoTarget": [{ 
                                    "id": "1",                                  //计算位置ID,字符串型，自定义
                                    "longitude": 113.83,                        //计算位置经度
                                    "latitude": 22.83,                          //计算位置纬度
                                    "height": 0                                 //计算位置高度(m)，> 0   
                               },
                                 { 
                                    "id": "2",                                  //计算位置ID,字符串型，自定义
                                    "longitude": 113.835,                       //计算位置经度
                                    "latitude": 22.835,                         //计算位置纬度
                                    "height": 0                                 //计算位置高度(m)，> 0   
                               }],
                 "infoEnvironment": {
                                    "wind_speed": 2,                            //泄漏区风速(m/s)，>= 0.5   
                                    "wind_direction": "SW",                     //泄漏区风向(十六风向："北","北东北","东北","东东北","东","东东南","东南","南东南","南","南西南","西南","西西南","西","西西北","西北","北西北")
                                    "wind_height": 10,                          //泄漏区风速风向取值高度(m)，> 0   
                                    "air_stability": "C",                       //泄漏区大气稳定度("A","B","C","D","E","F")，--非必须参数
                                    "temperature": 26,                          //泄漏区温度，> 0   
                                    "cloudy_is": True                           //泄漏区是否为多云天气
                                    }
                }


# 模型返回
            
    { 
        "success": 1,           //执行成功与否，1：成功，0：失败
        "data":                 //执行成功返回的数据
            {
                "tag": "ADDFSDGDG",                                         //计算标识，用于异步调用信息拾取
                "concentration_unit": "mg/m3",                              //浓度值单位
                "results":[{
                                 "id": "1",                                 //点ID标识，字符串，返回传入值
                                 "concentration": 0.0007670322196640719,    //浓度值(mg/m3)
                            },
                            {
                                 "id": "2",                                 //点ID标识，字符串，返回传入值
                                 "concentration": 0.0005830072425849703,    //浓度值(mg/m3)
                            }]
            }, 
        "msg": "",              //补充描述信息
        "err": ""               //执行失败错误信息
    }


