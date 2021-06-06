using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Swap
{
    /// <summary>数据交换接口
    /// </summary>
    public interface IDataSwap
    {
        /// <summary>标识名称
        /// </summary>
        string Tag_Name { get; }
        /// <summary>标识是否运行中
        /// </summary>
        bool Is_Running { get; }
        /// <summary>交换后目标数据类型
        /// </summary>
        Type Dest_ObjType { get; }
        /// <summary>交换数据改变事件
        /// </summary>
        event DataSwapChange_EventHandler SwapData_Change;

        /// <summary>任务执行持续监测
        /// </summary>
        /// <param name="nSteps">执行次数，<0为永不停止/param>
        /// <param name="nStepSwaps">每次交换数据数量</param>
        /// <param name="nFrequency">任务频率</param>
        /// <returns></returns>
        bool Start(int nSteps = 0, int nStepSwaps = 1, int nFrequency = 1000);
        /// <summary>停止持续监测
        /// </summary>
        /// <returns></returns>
        bool Stop();

        /// <summary>提取及转换数据
        /// </summary>
        /// <param name="delayedTime">有效延迟时间，超过无效</param>
        /// <param name="nStepSwaps">单次处理交换数据条数</param>
        /// <returns></returns>
        List<dynamic> SwapData_In(int nStepSwaps = 1);
        /// <summary>转换及输出数据
        /// </summary>
        /// <returns></returns>
        bool SwapData_Out(dynamic value);

        /// <summary>确认文件是否已经确认交换完毕
        /// </summary>
        /// <param name="fileName"></param>
        /// <returns></returns>
        bool checkNeedAck(string fileName);
        /// <summary>交换确认
        /// </summary>
        /// <param name="ackInfo">原始交换文件信息</param>
        /// <returns></returns>
        bool ackDataSwap(dynamic ackInfo);

        /// <summary>缓存数据备份
        /// </summary>
        /// <param name="path">文件路径</param>
        /// <param name="dir">目标文件夹路径</param>
        /// <returns></returns>
        bool SwapData_BackUp(string path, string dir);

        /// <summary>配置转为字符串
        /// </summary>
        string ToString();
        /// <summary>字符串转配置
        /// </summary>
        void FromString();
    }

}