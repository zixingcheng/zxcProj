using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    public enum typeTimeFrequency
    {
        None = 0,
        Second = 1,
        Second_30 = 30,
        Minute_1 = 60,
        Minute_5 = 300,
        Minute_10 = 600,
        Minute_15 = 900,
        Minute_30 = 1800,
        Hour = 3600,
        Day = 86400
    }

    /// <summary>数据缓存设置对象类
    /// </summary>
    public interface IDataCache_Set : IDataSet
    {
        /// <summary>唯一编码-自定义，便于快速遍历
        /// </summary>
        string ID { get; }
        /// <summary>因子信息
        /// </summary>
        IData_Factor Info_Factor { get; }
        /// <summary>
        /// 数据时间类型
        /// </summary>
        typeTimeFrequency Time_Frequency { get; }
        /// <summary>父设置对象
        /// </summary>
        IDataCache_Set Parent { get; }
        /// <summary>是否已经初始
        /// </summary>
        bool IsInited { get; }

        /// <summary>
        /// 基时间(一般为启动时整点)
        /// </summary>
        DateTime Time_Base { get; }
        /// <summary>
        /// 当前数据开始时间
        /// </summary>
        DateTime Time_Start { get; }
        /// <summary>最后数据时间
        /// </summary>
        DateTime Time_Last { get; }
        DateTime Time_LastBase { get; }
        /// <summary>当前数据时间
        /// </summary>
        DateTime Time_End { get; }

        /// <summary>
        /// 数据时间间隔（秒）
        /// </summary>
        int Time_Step { get; }
        /// <summary>
        /// 数据总间隔数（对应当前起止区间）
        /// </summary>
        int Sum_Step { get; }
        /// <summary>
        /// 数据结束索引（对应当前结束时间，保持总间隔数固定，不断移动）
        /// </summary>
        int Ind_Step { get; }
        /// <summary>是否允许更新数据（覆盖之前）
        /// </summary>
        bool Can_Refesh { get; set; }

        /// <summary>设置最后更新数据时间
        /// </summary>
        /// <param name="dtLast"></param>
        /// <returns></returns>
        bool SetLastTime(DateTime dtLast);

        /// <summary>提取数据序号对应的时间（队列模式时有效）
        /// </summary>
        /// <param name="ind"></param>
        /// <returns></returns>
        DateTime GetDateTime(int ind);
        /// <summary>提取时间对应的数据序号（队列模式时有效）
        /// </summary>
        /// <param name="dtData"></param>
        /// <returns></returns>
        int GetInd(DateTime dtData);

        /// <summary>提取时间区间内的数据序号集（队列模式时有效）
        /// </summary>
        /// <param name="dtStart"></param>
        /// <param name="dtEnd"></param>
        /// <returns></returns>
        List<int> GetInds(DateTime dtStart, DateTime dtEnd);
        /// <summary>提取时间频率+自定义标识组装的统一标识（字典缓存标识）
        /// </summary>
        /// <param name="typeTimeFrequency"></param>
        /// <param name="strTag"></param>
        /// <returns></returns>
        string GetTagName(typeTimeFrequency typeTimeFrequency, string strTag = "");

        /// <summary>标识数据已经初始，避免重复初始
        /// </summary>
        /// <returns></returns>
        bool Inited();
        /// <summary>校正时间为对应时间频率的整点/整分修正时间
        /// </summary>
        /// <param name="dtBase"></param>
        /// <returns></returns>
        DateTime CheckTime(DateTime dtBase);
    }
}
