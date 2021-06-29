using System;

namespace zxcCore.zxcData.Analysis
{
    public interface IDataStatistics
    {
        /// <summary>标识
        /// </summary>
        string Tag { get; set; }
        /// <summary>最大值
        /// </summary>
        double Max { get; set; }
        /// <summary>最小值
        /// </summary>
        double Min { get; set; }
        /// <summary>当前数据
        /// </summary>
        double Value { get; set; }
        /// <summary>数据时间
        /// </summary>
        DateTime Time { get; set; }
        /// <summary>数据差值
        /// </summary>
        double Value_delta { get; set; }
        /// <summary>数据最小间隔（统计用，超过该间隔才加入统计）
        /// </summary>
        double Value_interval { get; set; }

        /// <summary>数据-前一个
        /// </summary>
        double Value_last { get; set; }
        /// <summary>数据时间-前一个
        /// </summary>
        DateTime Time_last { get; set; }
        /// <summary>间隔时长-s
        /// </summary>
        double Duration_S { get; set; }
        /// <summary>间隔时长-m
        /// </summary>
        double Duration_M { get; set; }

        /// <summary>是否已经初始
        /// </summary>
        bool IsInited { get; }

        /// <summary>数据初始
        /// </summary>
        /// <param name="value"></param>
        /// <param name="max"></param>
        /// <param name="min"></param>
        /// <param name="time"></param>
        /// <param name="interval">数据最小间隔（统计用，超过该间隔才加入统计）</param>
        /// <returns></returns>
        bool Init(double value, double max, double min, DateTime time, double interval = 0, string tag = "");
        /// <summary>数据统计
        /// </summary>
        /// <param name="value"></param>
        /// <param name="time"></param>
        /// <returns></returns>
        bool Statistics(double value, DateTime time);
    }
}