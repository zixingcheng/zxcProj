# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-16 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    语音接口操作，百度api转换文字为语音文件，然后播放语音
"""
import sys, os, time, threading
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '11547400'
API_KEY = 'HXUjHRdb71ewmGv90LhiUl64'
SECRET_KEY = 'TDCdErf6vpntoBldAuvKBaxG1NH1KfeC'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
global m_thrdSay 
m_words =[]


#文字转语音输出
def Say(word, times = 1):
    #aipSpeech.synthesis(word, 'zh', 1, {'vol': 5,})
    result = aipSpeech.synthesis(word, 'zh', 1, {'vol': 5, 'spd': 6, 'aue': 3, 'per': 0})

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)

        #播放声音
        #track = pygame.mixer.music.load("D:\\myGit\\zxcProj\\src\\Zxc.Python\\zxcPy.All.Base\\auido.mp3")
        #pygame.mixer.music.play()
        for x in range(0, times):
            os.system('auido.mp3')
            time.sleep(len(word) / 4)   #按文字长度延时，非准确方式
    return True

#文字转语音输出（线程）
def Say_words():
    for x in m_words:
        Say(x, 1)
    m_words.clear()
m_thrdSay = threading.Thread(target=Say_words) 
def Say_thrd(word, times = 1):
    if(len(m_words) > 0):
        m_words.append(word)
    else:
        m_words.append(word)
    if(m_thrdSay.isAlive() == False):
        m_thrdSay.start()


if __name__ == '__main__':
    for x in range(0, 10):
        Say_thrd(str(x) + '.建设银行，大幅上涨，涨幅5%！', 1)
        print(x)
        time.sleep(3)
    print("end...")
    #Say('你好，hello world！', 2)
    