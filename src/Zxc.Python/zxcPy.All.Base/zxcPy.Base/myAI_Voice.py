# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-07-16 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    AI-语音接口操作，语音分割与转换等
"""
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from pydub.silence import split_on_silence
import sys, os, datetime
import myIO



# 语音分割--保持原有录音长度，可以默认开始时间
'''
    将声音文件按正常语句停顿拆分，并限定单句最长时间，返回结果为列表形式
    Args:
        path：文件路径
        silence_thresh：小于-n dBFS以下的为静默，默认-50dBFS。
        min_silence_len：静默超过n毫秒则拆分，默认1秒。
        keep_silence：默认开始时间，之前忽略,默认0秒
        length_limit：拆分后每段不得超过n秒，默认60秒。
        joint_silence_len：段拼接时加入1000毫秒间隔用于断句
        out_debug：是否输出调试信息
        save_path：保存路径
''' 
def split_audio_on_silence(path, silence_thresh=-50, min_silence_len=1000, length_limit=60, keep_silence=0, abandon_chunk_len=500, joint_silence_len=1000, out_debug=True, save_path=''):
    # 按句子停顿，拆分成长度不大于1分钟录音片段
    if(out_debug): print('开始拆分(如果录音较长，请耐心等待)\n',' *'*30) 
    dtStart = datetime.datetime.now()
    audio_segment = AudioSegment.from_wav(path)
    chunks = split_chunks_on_silence(audio_segment, silence_thresh=silence_thresh, min_silence_len=min_silence_len, length_limit=length_limit, keep_silence=keep_silence)
    if(out_debug): print('拆分结束，返回段数:',len(chunks),'\n',' *'*30)

    # 放弃长度小于0.5秒的录音片段
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= abandon_chunk_len: 
            chunks.pop(i)
    if(out_debug): print('取有效分段：',len(chunks))

    # 时间过短的相邻段合并，单段不超过设定秒
    chunks_adjust = []
    if(len(chunks) >= 0):
        length_limit = 60 * 1000
        temp = AudioSegment.empty()
        silence = AudioSegment.silent(duration = joint_silence_len)  
        nsegmental = 0
        for chunk in chunks:
            length = len(temp) + len(silence) + len(chunk)  # 预计合并后长度
            if length < length_limit:                       # 小于1分钟，可以合并
                temp += silence + chunk                     # 单独一段的话会多段间隔
            else:                                           # 大于1分钟，先将之前的保存，重新开始累加
                chunks_adjust.append(temp)
                temp = chunk 
        else:
            chunks_adjust.append(temp)
        if(out_debug): print('合并后段数：',len(chunks_adjust))

    # 保存所有分段
    if(True):
        # 保存前处理一下路径文件名
        if(save_path == ''): 
            save_path = "%s/chunks/%s" %(os.path.dirname(path), os.path.basename(path))
        myIO.mkdir(os.path.dirname(save_path), False) 
        namef, namec = os.path.splitext(save_path)
        namec = namec[1:]

        # 保存所有分段
        breaks = len(chunks_adjust)
        for i in range(breaks):
            new = chunks_adjust[i]
            save_name = '%s_%04d.%s'%(namef, i, namec)      # 生成保存路径
            new.export(save_name, format=namec)             # 保存文件
            if(out_debug): print('%04d'%i, len(new), os.path.basename(path))
        if(out_debug): print('保存完毕')
        print("==> split audio on silence end @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))
        return True
    print("==> split audio on silence failed @ %s, 耗时 %s 秒" % (os.path.basename(path), str((datetime.datetime.now() - dtStart).seconds)))
    return False

# 语音分割--保持原有录音长度，可以默认开始时间
'''
    将声音文件按正常语句停顿拆分，并限定单句最长时间，返回结果为列表形式
    Args:
        audio_segment: 录音文件
        silence_thresh：小于-n dBFS以下的为静默，默认-50dBFS。
        min_silence_len：静默超过n毫秒则拆分，默认1秒。
        keep_silence：默认开始时间，之前忽略,默认0秒
        length_limit：拆分后每段不得超过n秒，默认60秒。
    Return:
        chunk_splits：拆分后的列表
''' 
def split_chunks_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-50, keep_silence=0, length_limit=60, seek_step=1):
    # 初始返回分段语音信息
    chunks = []

    # 校检，短时忽略
    if(audio_segment.duration_seconds - keep_silence < length_limit * 1000):
        chunks.append(audio_segment[keep_silence: len(audio_segment) - keep_silence])
        return chunks
    
    # 长时语音分割，pydub-检测非回音
    split_ranges = detect_nonsilent(audio_segment, min_silence_len, silence_thresh, seek_step)

    # 语音个数
    num = len(split_ranges)
    if num==1:
        chunks.append(audio_segment)
    else:
        for index in range(len(split_ranges)):
            if index == 0:
                start_i = 0 + keep_silence
            else:
                start_i = round((split_ranges[index][0] + split_ranges[index-1][1])/2)

            if index == len(split_ranges) - 1:
                end_i = len(audio_segment)
            else:
                end_i = round((split_ranges[index + 1][0] + split_ranges[index][1]) / 2) 

            # 添加分段信息
            #print(index)
            #print([start_i,end_i])
            chunks.append(audio_segment[start_i: end_i])
    return chunks
 



# 运行
if __name__ == '__main__':
    # 语音分割--限长
    path = "E:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/Voices/audio.wav"
    # sound = AudioSegment.from_wav(path)
    # sounds = split_on_silence(sound, silence_thresh=-50,min_silence_len=1000,length_limit=60,keep_silence=0)
    split_audio_on_silence(path, silence_thresh=-50,min_silence_len=1000,length_limit=60,keep_silence=0)
    
    print()
    #my_record("Temps/Voices/myvoices.wav")
     

def main():
    # 载入
    path = "E:/myCode/zxcProj/src/Zxc.Python/zxcPy.All.Base/Temps/Voices/audio2.wav"
    sound = AudioSegment.from_wav(path)

    #sound = sound[:3*60*1000] # 如果文件较大，先取前3分钟测试，根据测试结果，调整参数
    
    # 设置参数
    silence_thresh=-50      # 小于-70dBFS以下的为静默
    min_silence_len=1000    # 静默超过700毫秒则拆分
    length_limit=60*1000    # 拆分后每段不得超过1分钟
    abandon_chunk_len=500   # 放弃小于500毫秒的段
    joint_silence_len=1300  # 段拼接时加入1300毫秒间隔用于断句
    
    # 将录音文件拆分成适合百度语音识别的大小
    #print(time.time())
    #total = prepare_for_baiduaip(name,sound,silence_thresh,min_silence_len,length_limit,abandon_chunk_len,joint_silence_len)
    #print(time.time())


     