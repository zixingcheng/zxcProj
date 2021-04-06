# -*- coding: utf-8 -*-
"""
Created on  张斌 2020-11-20 11:30:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    纳指python版AES加解密接口 
"""
import os, mySystem
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto.Util.Padding import pad,unpad

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("", False)  
import myFTP, myIO

BLOCK_SIZE = 16
key = 'AD42F6691B035B7580E4FEF93BE10BAD'.encode('utf-8')    #密钥
iv = b'AD42F6691B035B7580E4FEF93BE10BAD'[:16]               #偏移量16


# 加密函数
def encrypt(rpath,wpath):
    fr = open(rpath, 'r', encoding='utf-8')
    text = fr.read()
    # text = json.dumps(text)
    fw = open(wpath, 'wb+')
    mode = AES.MODE_CBC #CBC模式 
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(pad(text.encode("utf-8"), BLOCK_SIZE))#采用pkcs5补全

    fw.write(cipher_text)
    fr.close()
    fw.close()
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)

# 解密后，去掉补足的空格用strip() 去掉
def decrypt(rpath,wpath):
    fr = open(rpath, 'rb')
    content = fr.read()
    content = b2a_hex(content)
    # content = int(content,16)
    mode = AES.MODE_CBC         #CBC模式
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(content))

    # data = eval(plain_text)
    # json.loads(data)
    fw = open(wpath, 'wb+')
    fw.write(unpad(plain_text, BLOCK_SIZE))
    fr.close()
    fw.close()
    return bytes.decode(plain_text).rstrip('\0')

# 解密文件夹文件，解密后删除
def DecryptFiles(file_dir, autoDel = True): 
    files = myIO.getFiles(file_dir)
    for x in files:
        if(os.path.exists(x)): 
            fileName = myIO.getFileName(x)
            if(fileName[len(fileName)-4:] == "_key"):
                path = x.replace("_key.json", ".json")
                try:
                    strJson = decrypt(x, path)  # 解密

                    # 解密后删除
                    if(os.path.exists(path)):
                        os.remove(x)
                except Exception as err:
                    print('文件解密失败(%s)' % fileName + " ,具体错误描述为：%s" % err)
                    pass
    


if __name__ == '__main__':
    DecryptFiles("D:/myCode/zxcProj/src/Zxc.Core/zpCore.MicroStation/ftpData/alarm")
    DecryptFiles("D:/myCode/zxcProj/src/Zxc.Core/zpCore.MicroStation/ftpData/task")

    e = encrypt("E:\encrypt\python\step_20201119_0010.json","E:\encrypt\python\encrypt\step_20201119_0010_key.json")  # 加密
    d = decrypt("E:\encrypt\python\encrypt\step_20201119_0010_key.json","E:\encrypt\python\dencrypt\step_20201119_0010.json")  # 解密
    print("加密:", e)
    print("解密:", d)


    e = encrypt("E:\encrypt\python\\user_20201120_0300.json", "E:\encrypt\python\encrypt\\user_20201120_0300_key.json")  # 加密
    d = decrypt("E:\encrypt\python\encrypt\\user_20201120_0300_key.json","E:\encrypt\python\dencrypt\\user_20201120_0300.json")  # 解密
    print("加密:", e)
    print("解密:", d)

    e = encrypt("E:\encrypt\python\\user_group_20201120_0300.json", "E:\encrypt\python\encrypt\\user_group_20201120_0300_key.json")  # 加密
    d = decrypt("E:\encrypt\python\encrypt\\user_group_20201120_0300_key.json","E:\encrypt\python\dencrypt\\user_group_20201120_0300.json")  # 解密
    # print("加密:", e)
    print("解密:", d)

    e = encrypt("E:\encrypt\python\info_20201119_0010.json", "E:\encrypt\python\encrypt\info_20201119_0010_key.json")  # 加密
    d = decrypt("E:\encrypt\python\encrypt\info_20201119_0010_key.json","E:\encrypt\python\dencrypt\info_20201119_0010.json")  # 解密
    # print("加密:", e)
    print("解密:", d)