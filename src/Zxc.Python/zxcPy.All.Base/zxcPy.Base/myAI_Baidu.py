# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-16 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    AI-百度接口操作
""" 
import sys, os, datetime
from aip import AipSpeech, AipOcr

# 加载自定义库
import myIO, myData_Trans, myVoice

# 百度语音识别API配置参数 
APP_ID = '17073439'                                     # 你的 APPID
API_KEY = 'LDg5YKueHGye7GHYSmlmKxyA'                    # 你的 AK
SECRET_KEY = '0LrjcVugAtyY0crrXGN9ZXP9u9tHwEfX'         # 你的 SK
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
aipORC = AipOcr(APP_ID, API_KEY, SECRET_KEY)



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
def Speech_Recognition_Standard(path, out_debug=False):
    # 读取录音文件
    dtStart = datetime.datetime.now()
    with open(path, 'rb') as fp: 
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        if(out_debug): print('\n接口调用（在线百度语AI接口，请耐心等待）')
        result = aipSpeech.asr(voices, 'pcm', 16000, {'dev_pid': 1537, })
        result_text = result["result"][0]

        if(out_debug): print("==> Speech_Recognition_Standard @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))
        return result_text
    except KeyError:
        # print("KeyError")
        # speaker.Speak("我没有听清楚，请再说一遍...")
        return ""
    
# 将语音转文本STT-
def Speech_Recognition(path, silence_thresh=-50, out_debug=False):
    # 自动分割
    dtStart = datetime.datetime.now()
    paths = myVoice.split_audio_on_silence(path, silence_thresh=-50,min_silence_len=1000,length_limit=60,keep_silence=0, out_debug=out_debug)
    if(len(paths) == 0): return ""

    # 语音识别转换
    result_text = ""
    if(out_debug): print('\n接口调用，请耐心等待')
    for x in paths:
        result_text += Speech_Recognition_Standard(x, out_debug=False) + "\n"
    if(out_debug): print("==> Speech_Recognition @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))
    return result_text


# 通用文字识别
def ORC(path, templateSign, options = {}, out_debug=False):
    # 读取图片文件
    dtStart = datetime.datetime.now()
    dicResult = {'words': [], 'wordText': ""}
    with open(path, 'rb') as fp: 
        image = fp.read()
    try: 
        # 带参数调用通用文字识别  
        result = aipORC.basicGeneral(image, options)
        if(out_debug): print("==> ORC @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))

        # 转换为易识别结果
        words = []
        for x in result['words_result']: 
            words.append(x['words'])
        dicResult = {'words': words, 'wordText': myData_Trans.Tran_ToStr(words, "\n")}
        return dicResult
    except KeyError:
        return dicResult
# 通用文字识别
def IORC(path, templateSign, classifierId = 0, out_debug=False):
    # 读取图片文件
    dtStart = datetime.datetime.now()
    dicResult = {}
    with open(path, 'rb') as fp: 
        image = fp.read()
    try:
        # 设置可选参数 
        options = {}
        options["templateSign"] = templateSign
        options["classifierId"] = classifierId


        # 带参数调用自定义模板文字识别  
        result = aipORC.custom(image, options)
        if(out_debug): print("==> IORC @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))

        # 转换为易识别结果
        for x in result['data']['ret']: 
            values= {}
            values['word'] = x['word'] 
            values['location'] = x['location']
            values['probability'] = x['probability']
            dicResult[x['word_name']] = values
        return dicResult
    except KeyError:
        return dicResult



if __name__ == '__main__':
    # 语音合成 
    dir = "D:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/"
    #path = Speech_Synthesis('你好，世界！', dir + "auido.mp3") 
    
    # 语音文件播放
    # os.system(path)
    
    # 将语音转文本STT
    # strText = Speech_Recognition_Standard(dir + "audio.pcm", out_debug=True)
    # strText = Speech_Recognition(dir + "Voices/audio.wav", out_debug=True)
    # print("you said: " + strText)

    # ORC识别-自定义模板
    strText = ORC(dir + "Images/Test5.jpg", "49a1e68d3cd776bec750b8718a479bfa", out_debug=True)
    print("you image: \n" + str(strText))
    
    strText = ORC(dir + "Images/Test.png", "49a1e68d3cd776bec750b8718a479bfa", out_debug=True)
    strText = IORC(dir + "Images/Test.png", "18ed022a1b51ef96b130bd4226b89f64", out_debug=True)
    
    strText = ORC(dir + "Images/Test2.jpg", "c0f24215c88dcee9c9f5111238b31c96", out_debug=True)
    strText = IORC(dir + "Images/Test2.jpg", "c0f24215c88dcee9c9f5111238b31c96", out_debug=True)
    print()
    