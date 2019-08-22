# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-16 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    AI-百度接口操作
""" 
import sys, os
from aip import AipSpeech

# 百度语音识别API配置参数 
APP_ID = '11547400'                                     # 你的 APPID
API_KEY = 'HXUjHRdb71ewmGv90LhiUl64'                    # 你的 AK
SECRET_KEY = 'TDCdErf6vpntoBldAuvKBaxG1NH1KfeC'         # 你的 SK
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



# 语音合成，文字转语音输出
def Speech_Synthesis(word, path_audio=''):
    # 设置语音播报设置
    #aipSpeech.synthesis(word, 'zh', 1, {'vol': 5,})
    result = aipSpeech.synthesis(word, 'zh', 1, {'vol': 5, 'spd': 6, 'aue': 3, 'per': 0})

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if(path_audio == ''): path_audio = "./Temps/Voices/auido.mp3"
    if not isinstance(result, dict):
        with open(path_audio, 'wb') as f:
            f.write(result)
            return path_audio
    return ''

# 将语音转文本STT
def Speech_Recognition(path):
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = aipSpeech.asr(voices, 'pcm', 16000, {'dev_pid': 1537, })
        # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
        # print(result)
        # print(result['result'][0])
        # print(result)
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")
        #speaker.Speak("我没有听清楚，请再说一遍...")
        


if __name__ == '__main__':
    # 语音合成 
    dir = "E:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/Voices/"
    path = Speech_Synthesis('你好，世界！', dir + "auido.mp3") 
    
    # 语音文件播放
    # os.system(path)
    
    # 将语音转文本STT
    strText = Speech_Recognition(dir + "audio.pcm")
    print(strText)

    print()
    