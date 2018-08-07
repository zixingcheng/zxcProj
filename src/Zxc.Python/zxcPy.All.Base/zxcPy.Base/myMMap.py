# -*- coding: utf-8 -*-
"""
Created on  张斌 2018-04-18 11:00:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    myMMap, Api接口操作, 共享内存，兼容linux
"""
import sys, os, string, time 
import mmap, contextlib, ast
import mySystem, myEnum, myData, myThread, myData_Trans 
myMMap_DataType = myEnum.enum_index('str', 'int', 'float', 'list', 'dict', 'object')

#共享内存类
class myMMap_Data(): 
    def __init__(self, value, nOffset = -1):             
        self.type = myMMap_DataType.str
        self.value = value
        self.offset = nOffset
        self.length = 0
        self.Set_Value(value, nOffset)
        
    #设置值
    def Set_Value(self, value, nOffset = -1): 
        self.value = value
        self.offset = nOffset

        #按类型处理
        pType = type(value)
        if(pType == int):
            self.type = myMMap_DataType.int
            self.arrValue = myData_Trans.To_Bytes_By_Int(value)
        elif(pType == float):
            self.type = myMMap_DataType.float
            self.arrValue = myData_Trans.To_Bytes_By_Float(value)
        elif(pType == str):
            self.type = myMMap_DataType.str
            self.arrValue = myData_Trans.To_Bytes_By_Str(value)
        elif(pType == list):
            self.type = myMMap_DataType.list
            self.arrValue = b''
            for x in value:                 #循环组装(str会有问题)
                pData = myMMap_Data(x)
                self.arrValue += myData_Trans.To_Bytes_By_Int(pData.type)       #记录数据类型
                self.arrValue += myData_Trans.To_Bytes_By_Int(pData.length)     #记录数据长度
                self.arrValue += pData.arrValue
        elif(pType == dict):
            self.type = myMMap_DataType.dict
            self.arrValue = myData_Trans.To_Bytes_By_Str(str(value)) 
        else:
            self.type = myMMap_DataType.object
            self.arrValue = myData_Trans.To_Bytes_By_Str(value.ToString())
        self.length = len(self.arrValue)
      
    #设置值(byte) 
    def Tran_Value(self, value): 
        self.type = myData_Trans.To_Int_By_Bytes(value[0:4])       #读取数据类型
        self.length = myData_Trans.To_Int_By_Bytes(value[4:8])     #读取数据长度
        nLen = 8 + self.length
        self.arrValue = value[8:nLen]      #读取值字节
        self.value = self.Get_Value()
        return nLen

    #获取值(转换为对应值类型返回)
    def Get_Value(self): 
        #按类型处理
        if(self.type == myMMap_DataType.int):
            self.value = myData_Trans.To_Int_By_Bytes(self.arrValue)
        elif(self.type == myMMap_DataType.float):
            self.value = myData_Trans.To_Float_By_Bytes(self.arrValue)
        elif(self.type == myMMap_DataType.str):
            self.value = myData_Trans.To_Str_By_Bytes(self.arrValue)
        elif(self.type == myMMap_DataType.list):
            arrTemp = self.arrValue
            lst = []
            while(len(arrTemp) > 0):
                pData = myMMap_Data(0)
                nOffset = pData.Tran_Value(arrTemp)
                arrTemp = arrTemp[nOffset:]
                lst.append(pData.value)
            self.value = lst
        elif(self.type == myMMap_DataType.dict):
            strValue = myData_Trans.To_Str_By_Bytes(self.arrValue)
            self.value = ast.literal_eval(strValue)
        else:
            #self.type = myMMap_DataType.object
            #self.value = myData_Trans.To_Str_By_Bytes(self.arrValue)
            return None
        return self.value

#共享内存类
class myMMap(myThread.myThread): 
    def __init__(self, IsWrite = True, filePath = "pyMMap.dat", maxSize = 1024):
        super().__init__("", 0) # 必须调用
        self.mmapPath = filePath
        self.mmapFile = None
        self.mmap = None
        self.isWrite = IsWrite
        self.maxSize = maxSize
        self.offset = 0
        self.createdFile = False
    def __del__(self):
        if(self.createdFile):
            self.Close()
        
    #打开文件创建内存映射
    def Create_File(self, newCreate = False): 
        needCreat = newCreate
        if(os.path.exists(self.mmapPath) == False):
            needCreat = True
        else:
            fsize = os.path.getsize(self.mmapPath)
            if(fsize != self.maxSize): needCreat = True

        #创建内存映射文件
        if(needCreat):
            with open(self.mmapPath, "w") as f:
                f.write('\x00' * self.maxSize)
            self.createdFile = True
    #删除文件创建内存映射
    def Delete_File(self): 
        if(os.path.exists(self.mmapPath)):
            os.remove(self.mmapPath)

    #打开文件创建内存映射
    def Open(self, bReadOnly = False, bCreate = True): 
        if(bCreate): self.Create_File()

        #打开文件，映射内存
        self.mmapFile = open(self.mmapPath, 'r+') 
        if(bReadOnly):
            self.mmap = mmap.mmap(self.mmapFile.fileno(), self.maxSize, access = mmap.ACCESS_READ)
        else:
            self.mmap = mmap.mmap(self.mmapFile.fileno(), self.maxSize, access = mmap.ACCESS_WRITE)
    #关闭文件、内存映射
    def Close(self): 
        try:
            self.mmap.close()
            self.mmapFile.close()
            self.Delete_File()
            return True
        except:
            return False

    #写入内存映射
    def Write(self, value, nPosion = -1, bFull = True): 
        #按类型处理
        pData = myMMap_Data(value, nPosion)
        return self.Write_Data(pData, bFull) 
    def Write_Data(self, value, bFull = True): 
        #初始索引位置
        nOffet = myData.iif(value.offset < 0, self.offset, value.offset)
        self.mmap.seek(nOffet)

        #记录数据类型、长度
        nLen_Head = 0
        if(bFull):  
            self.mmap.write(myData_Trans.To_Bytes_By_Int(value.type))    #记录数据类型
            self.mmap.write(myData_Trans.To_Bytes_By_Int(value.length))  #记录数据长度
            nLen_Head += 8     
            
        #写入信息
        self.mmap.write(value.arrValue)
        self.mmap.flush()

        #记录位置
        nOffet += value.length + nLen_Head
        self.offset = myData.iif(nOffet < self.maxSize, nOffet, self.maxSize)
        return nOffet
         
    #读取内存映射 
    def Read(self, nPosion = 0): 
        pData = myMMap_Data(0, nPosion)
        nOffet = self.Read_Data(pData)
        return pData.Get_Value(), nOffet
    def Read_Data(self, value, bFull = True): 
        #初始索引位置
        nOffet = myData.iif(value.offset < 0, self.offset, value.offset)
        self.mmap.seek(nOffet)
        
        #读取数据类型、长度
        nLen_Head = 0
        if(bFull):  
            value.type = myData_Trans.To_Int_By_Bytes(self.mmap.read(4))    #读取数据类型
            value.length = myData_Trans.To_Int_By_Bytes(self.mmap.read(4))  #读取数据长度
            nLen_Head += 8   
         
        #读取信息
        value.arrValue = self.mmap.read(value.length)

        #记录位置 
        nOffet += value.length + nLen_Head
        self.offset = myData.iif(nOffet < self.maxSize, nOffet, self.maxSize)
        return nOffet
    
#共享内存管理类(索引、内存数据对象结构,轮次写入)
class myMMap_Manager(): 
    def __init__(self, filePath = "pyMMap.dat", isRead = False, indNum = 10, maxSize = 10240):
        self.mmap = myMMap(True, filePath, maxSize) 
        self.mmap.Open()
        if(isRead):
            #读取当前管理类信息
            self.ver, nOffet = self.mmap.Read(0)
            self.verR = self.ver
            self.size = nOffet
            self.ind, nOffet = self.mmap.Read(nOffet)
            self.ind_read, nOffet = self.mmap.Read(nOffet)
            self.indNum, nOffet = self.mmap.Read(nOffet)
            self.maxSize, nOffet = self.mmap.Read(nOffet)
            self._offset0 = nOffet
            self.offsets, nOffet = self.mmap.Read(nOffet)
            self._offset = nOffet
            self.offset = nOffet
        else:
            self.indNum = indNum 
            self.maxSize = self.mmap.maxSize
            self.ver = 0
            self.verR = 0
            self.ind = 0
            self.ind_read = 0
            self.offsets = [0] * indNum

            #记录当前管理类信息
            nOffet = self.mmap.Write(self.ver, 0)
            self.size = nOffet
            nOffet = self.mmap.Write(self.ind, nOffet)
            nOffet = self.mmap.Write(self.ind_read, nOffet)
            nOffet = self.mmap.Write(indNum, nOffet)
            nOffet = self.mmap.Write(maxSize, nOffet)
            self._offset0 = nOffet
            nOffet = self.mmap.Write(self.offsets, nOffet)
            self._offset = nOffet
            self.offset = nOffet
    def __del__(self):
        self.mmap.Close()
        
    #写入内存数据对象
    def Write(self, value, ind = -1): 
        #纠正内存数据偏移为当前偏移
        if(ind < 0): ind = self.ind 
        if(ind >= self.indNum): ind = 0             #索引步进(循环)
        value.offset = self.offset                  #偏移顺序，累加
        if(value.offset + value.length > self.maxSize):
            value.offset = self._offset             #超过最大，回到起始位置

        #写入并更新当前索引
        self.offsets[ind] = self.offset             #记录索引
        self.Write_Ind(self.offset, ind)            #索引对应偏移
        self.offset = self.mmap.Write_Data(value)   #数据写入偏移位置
        if(self.offset == value.offset):            #写入失败
            return ind
        self.ind += 1                               #索引步进(循环)
        if(self.ind >= self.indNum):
            self.offset = self._offset              #偏移恢复到起始位置
            self.ind = 0
            self.ver += 1                           #版本增加
        return ind                                  #返回索引
    #写入索引偏移信息
    def Write_Ind(self, offset, ind = -1): 
        if(ind < 0): ind = self.ind                 
        self.mmap.Write(offset, self._offset0 + ind * self.size + 8)
        if(ind == 0):                               #版本记录(起始时)
            self.mmap.Write(self.ver, 0)             
        self.mmap.Write(self.ind, self.size)        #写入当前写索引
    
    #读取内存数据对象
    def Read(self, ind = -1, bDelete = False): 
        #读取索引偏移
        if(ind < 0): ind = self.ind_read
        if(ind >= self.indNum): ind = 0             #索引步进(循环)
        if(bDelete):                                #检查是否过界
            if(self.Check_Ind(ind) == False):       #过界则忽略    
                return None, ind
        offset = self.Read_Ind(ind)                 #记录的索引偏移
        if(offset <= 0):
            return None, ind

        #读取内存数据
        pData = myMMap_Data(0, offset)
        self.mmap.Read_Data(pData)
        pData.Get_Value()

        if(bDelete):
            self.offsets[ind] = -1                  #记录索引（删除） 
            self.Write_Ind(-1, ind)                 #索引对应偏移（删除） 
        #ind = myData.iif(ind == self.indNum - 1, 0, ind + 1)
        self.ind_read += 1                          #索引步进(循环)
        if(self.ind_read >= self.indNum):           
            self.ind_read = 0                       #索引初始，版本更新
            self.verR += 1                          #版本步进
        return pData, self.ind_read                 #返回内存对象
    #读取索引偏移信息
    def Read_Ind(self, ind = -1): 
        if(ind < 0): ind = self.ind_read
        value, nOffet = self.mmap.Read(self._offset0 + ind * self.size + 8)
        #self.mmap.Write(self.ind_read, self.size * 2)   #记录读取索引(多方读，记录无意义)
        return value
    #读取索引偏移信息
    def Check_Ind(self, ind = -1): 
        if(ind < 0): ind = self.ind_read
        self.ver, nOffet = self.mmap.Read(0)        #读取当前写版本
        self.ind, nOffet = self.mmap.Read(self.size)#读取当前写索引

        #print("verR:" , self.verR, ",ver: " , self.ver,",indR:" , ind, ",ind: " , self.ind)
        if(self.ver * self.indNum + self.ind < self.verR * self.indNum + ind):
            return False                            #版本过界
        else:
            #修正为最新版本号
            self.verR = myData.iif(self.ind < ind, self.ver - 1, self.ver)  
            return True                             #版本未过界


def main():
    # 创建内存映射
    pMMap = myMMap()  
    try:
        pMMap.Create_File(True)
        bWrite = True
        pMMap_Manager = myMMap_Manager("pyMMap2.dat")
    except:
        bWrite = False
        pMMap_Manager = myMMap_Manager("pyMMap2.dat", True)
    pMMap.Open(not bWrite)
    
    # 创建内存映射
    if(bWrite):
        for i in range(1, 1000):
            nOffet = pMMap.Write(i, 0)
            print(i)

            nOffet = pMMap.Write("Test_" + str(i), nOffet)
            print("Test_" + str(i))
            
            dict0 = {'FromUserName': 'user', 'Text': 'text', 'Type': 'type'}
            nOffet = pMMap.Write(dict0, nOffet)
            print(dict0)

            lst = [0] * 3
            lst[0] = i - 1
            lst[1] = i - 0
            lst[2] = i + 1
            nOffet = pMMap.Write(lst, nOffet)
            print(lst)
            print("")
            
            #myMMap_Manager
            lst.append("ind--" + str(i))
            pMMdata = myMMap_Data(lst, 0)
            ind2 = pMMap_Manager.Write(pMMdata)
            pMMdata_M2, ind3 = pMMap_Manager.Read(ind2)
            if(pMMdata_M2 != None):
                print(str(ind2) + ":", pMMdata_M2.value)  
            pMMap_Manager.Read
            time.sleep(1)
    else:
        pMMdata = myMMap_Data(0, 0)
        nOffet = pMMap.Read_Data(pMMdata)
        
        pMMdata2 = myMMap_Data("", nOffet)
        nOffet = pMMap.Read_Data(pMMdata2)

        dict0, nOffet = pMMap.Read(nOffet)

        pMMdata3 = myMMap_Data([], nOffet)
        nOffet = pMMap.Read_Data(pMMdata3)

        ind = 0
        bPrint = True
        while True:
            if(pMMdata.value > 10):
                pMMdata_M, ind = pMMap_Manager.Read(ind, True)
            else:
                pMMdata_M, ind = pMMap_Manager.Read(ind)

            if(pMMdata_M != None):
                bPrint = True
                print(pMMdata_M.value)
            else:
                bPrint = False 
            
            if(bPrint):
                pMMap.Read_Data(pMMdata)
                pMMdata.Get_Value()
                print(pMMdata.Get_Value())
                print(pMMap.Read(pMMdata2.offset))
                print(dict0)
                print(pMMap.Read(pMMdata3.offset))
                print("")
            time.sleep(0.1)

    pMMap.Close()
    print("Exiting Main MMap...")

if __name__ == '__main__':   
    main()