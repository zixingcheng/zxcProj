using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据统计
    /// </summary>
    /// 
    public class DataStatistics
    {
        #region 属性及构造

        /// <summary>标识
        /// </summary>
        public string Tag { get; set; }
        /// <summary>最大值
        /// </summary>
        public double Max { get; set; }
        /// <summary>最大值-原始值
        /// </summary>
        public double Max_Original { get; set; }
        /// <summary>最小值
        /// </summary>
        public double Min { get; set; }
        /// <summary>最小值-原始值
        /// </summary>
        public double Min_Original { get; set; }
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
        protected double Value_delta = 0;
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


        /// <summary>统计数据初始
        /// </summary>
        /// <param name="valueBase">基础值(不参与计算)</param>
        /// <param name="time">基时间</param>
        /// <param name="interval">有效数据间隔</param>
        /// <param name="tag">标签</param>
        /// <param name="valueMax">最大值</param>
        /// <param name="valueMin">最小值</param>
        /// <returns></returns>
        public virtual bool Init(double valueBase, DateTime time, double interval = 0, string tag = "", double valueMax = double.MinValue, double valueMin = double.MaxValue)
        {
            Tag = tag;
            Max = valueMax; Max_last = valueMax;
            Min = valueMin; Min_last = valueMin;
            Min_Original = valueBase; Max_Original = valueBase;
            Value_interval = Math.Round(interval, 8);


            //值修正为区间大小倍数
            int times = 0;
            double value = valueBase;
            if (Value_interval > 0)
            {
                //value = Math.Round(value / Value_interval) * Value_interval;
                //times = (int)Math.Round(value / Value_interval);
                //Value_delta = 0;
            }

            Value = value;
            Value_Original = valueBase;
            Value_Original_last = valueBase;
            Value_last = value; Time_last = time;
            zxcConsoleHelper.Debug(false, "***Debug*** {7}: {0} (修正：{6})，前值：{2}，差值：{1}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", valueBase, value - valueBase, double.NaN, times * Value_interval, Value_interval, times, value, Tag);

            _IsInited = true;
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
                //值修正为区间大小倍数
                double delta = Math.Round(value - Value, 8);
                Value_delta = delta;
                if (Value_interval > 0)
                {
                    value = Math.Floor((value - Value_Original_last) / Value_interval) * Value_interval + Value_Original_last;
                    times = (int)Math.Floor(Math.Abs(delta / Value_interval)) * delta < 0 ? -1 : 1;
                    Value_delta = times * Value_interval;

                    if (Math.Abs(times) > 1)
                    {
                        int a = 0;
                    }
                }

                //不到最小间隔，忽略
                if (Math.Abs(delta) < Value_interval)
                {
                    value = Value;
                    zxcConsoleHelper.Debug(false, "***Debug***{7}: {0} (修正：{6})，前值：{1}，差值：{2}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", value0, Value, delta, 0, Value_interval, 0, value, Tag);
                }
                else
                    zxcConsoleHelper.Debug(false, "***Debug***{7}: {0} (修正：{6})，前值：{1}，差值：{2}，有效间隔：{3}，最小间隔：{4}，倍数：{5}", value0, Value, delta, Value_delta, Value_interval, times, value, Tag);
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

            //统计-原始值
            if (Value_Original > Max_Original)
            {
                Max_Original = Value_Original;
            }
            else if (Value_Original < Min_Original)
            {
                Min_Original = Value_Original;
            }
            return true;
        }

    }

}
