using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.Common;

namespace zxcCore.zxcRobot.DataAnalysis
{
    /// <summary>数据统计
    /// </summary>
    /// 
    public class DataStatistics : IDataStatistics
    {
        #region 属性及构造

        /// <summary>标识
        /// </summary>
        public string Tag { get; set; }
        /// <summary>最大值
        /// </summary>
        public double Max { get; set; }
        /// <summary>最小值
        /// </summary>
        public double Min { get; set; }
        /// <summary>当前值-修正值
        /// </summary>
        public double Value { get; set; }
        /// <summary>前值-原始值
        /// </summary>
        public double Value_Original { get; set; }
        /// <summary>当前值时间
        /// </summary>
        public DateTime Time { get; set; }

        /// <summary>最大值-前值
        /// </summary>
        public double Max_last { get; set; }
        /// <summary>最小值-前值
        /// </summary>
        public double Min_last { get; set; }
        /// <summary>前值-修正值
        /// </summary>
        public double Value_last { get; set; }
        /// <summary>前值-原始值
        /// </summary>
        public double Value_Original_last { get; set; }
        /// <summary>前值时间
        /// </summary>
        public DateTime Time_last { get; set; }

        /// <summary>数据生效与前值的数据差（间隔倍数）
        /// </summary>
        public double Value_delta { get; set; }
        /// <summary>生效数据间隔
        /// </summary>
        public double Value_interval { get; set; }
        /// <summary>数据生效与前值的时间间隔（总秒）
        /// </summary>
        public double Duration_S { get; set; }
        /// <summary>数据生效与前值的时间间隔（总分钟）
        /// </summary>
        public double Duration_M { get; set; }

        /// <summary>是否已经初始
        /// </summary>
        bool _IsInited = false;
        public bool IsInited
        {
            get { return _IsInited; }
        }

        public DataStatistics()
        {
            Time = DateTime.MinValue;
            Time_last = DateTime.MinValue;
        }

        #endregion


        //数据初始实现
        public virtual bool Init(double value, double max, double min, DateTime time, double interval = 0, string tag = "")
        {
            Tag = tag;
            Max = max; Max_last = max;
            Min = min; Min_last = min;
            Value_interval = Math.Round(interval, 4);
            double value0 = value;
            int times = 0;

            //值修正为区间大小倍数
            if (Value_interval > 0)
            {
                times = (int)Math.Round(value / Value_interval);
                value = times * Value_interval;
            }
            _IsInited = this.Statistics(value, time);

            Value_Original_last = value0;
            Value_last = value; Time_last = time;
            zxcConsoleHelper.Debug(false, "****** {7}: {0}，差值：{1}，前值：{2}，当前：{6}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", value0, value0, 0, value, Value_interval, times, value, Tag);
            return _IsInited;
        }
        //数据统计实现
        public virtual bool Statistics(double value, DateTime time)
        {
            //最小间隔
            double value0 = value;
            int times = 0;
            if (_IsInited && Value_interval >= 0)
            {
                double delta = value - Value;

                //值修正为区间大小倍数
                Value_delta = delta;
                if (Value_interval > 0)
                {
                    value = Math.Round(value / Value_interval) * Value_interval;
                    times = (int)Math.Round(delta / Value_interval);
                    Value_delta = times * Value_interval;
                }

                //不到最小间隔，忽略
                if (Math.Abs(delta) <= Value_interval)
                {
                    //ConsoleHelper.Debug("***###{7: {0}，差值：{2}，前值：{1}，当前：{6}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", value0, Value_last, delta, Value_delta, Value_interval, times, Value,Tag);
                    return false;
                }

                //if (delta < 0)
                //{
                //    int a = 0;
                //}
                zxcConsoleHelper.Debug(false, "******{7}: {0}，差值：{2}，前值：{1}，当前：{6}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", value0, Value, delta, Value_delta, Value_interval, times, value, Tag);
            }

            //值更新 
            Value_last = Value; Time_last = Time;
            Value = value; Time = time;
            Value_Original_last = Value_Original; Value_Original = value0;

            //计算
            if (Time_last != DateTime.MinValue)
            {
                Duration_S = (Time - Time_last).TotalSeconds;
                Duration_M = (Time - Time_last).TotalMinutes;
            }

            //统计
            if (value > Max)
            {
                Max_last = Max;
                Max = value;
            }
            else if (value < Min)
            {
                Min_last = Min;
                Min = value;
            }
            return true;
        }

    }
}
