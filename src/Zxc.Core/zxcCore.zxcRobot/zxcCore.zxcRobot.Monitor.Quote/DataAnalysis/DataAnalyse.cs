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
    public class DataAnalyse
    {
        #region 属性及构造

        /// <summary数据交换事件
        /// </summary>
        public event DataAnalyse_EventHandler DataAnalyse_Trigger;


        /// <summary>标识
        /// </summary>
        public string Tag { get; set; }
        /// <summary>基值
        /// </summary>
        protected double Value_base { get; set; }
        /// <summary>前值
        /// </summary>
        protected double Value { get; set; }
        /// <summary>前值（有效差值点）
        /// </summary>
        protected double Value_last { get; set; }
        /// <summary>有效差值范围
        /// </summary>
        protected double Value_delta { get; set; }

        /// <summary>前值方向（正向为1，负向为-1）
        /// </summary>
        protected double Value_last_direction { get; set; }
        /// <summary>前值时间
        /// </summary>
        protected DateTime Time_last { get; set; }


        /// <summary>数据对象缓存
        /// </summary>
        protected internal Datas Datas { get; set; }
        /// <summary>数据统计对象
        /// </summary>
        protected DataStatistics DataStatistics { get; set; }
        /// <summary>数据统计对象集（阶段）
        /// </summary>
        protected List<DataStatistics> lstDataStatistics { get; set; }

        /// <summary>是否已经初始
        /// </summary>
        bool _IsInited = false;
        public bool IsInited
        {
            get { return _IsInited; }
        }


        public DataAnalyse(string tag)
        {
            Tag = tag;
            this.Datas = new Datas(Tag);
        }

        #endregion


        //数据初始实现
        public virtual bool Init(double value, double valueBase, DateTime time, double max, double min, double valueDelta = 0.0025)
        {
            this.Value_delta = valueDelta;
            this.Value_base = valueBase;
            this.Value_last = valueBase;
            this.Value = valueBase;
            this.Time_last = time;

            this.Datas = new Datas(Tag);
            this.lstDataStatistics = new List<DataStatistics>();
            this.InitDataStatistics(value, time, max, min);

            //缓存及统计数据
            _IsInited = this.Analysis(value, time);
            return _IsInited;
        }
        //初始统计对象-阶段
        public virtual bool InitDataStatistics(double value, DateTime time, double max, double min)
        {
            this.DataStatistics = new DataStatistics();
            this.DataStatistics.Init(value, max, min, time, 0, Tag);

            this.lstDataStatistics.Add(this.DataStatistics);
            return true;
        }

        //数据分析（提取数据增大、减小、拐点信息）
        public virtual bool Analysis(double value, DateTime time)
        {
            //缓存及统计数据
            this.Datas.AddData(value, time);

            //数据处理
            this.dataHandle(value, time);
            return true;
        }

        //数据处理
        protected virtual bool dataHandle(double value, DateTime time, bool recursion = false)
        {
            //数据校正到固定区间
            bool bHitLimit = false;                 //是否超出范围，需要递归
            double dValue0 = value;
            double dValueLast = this.Value;
            double dDelta = Math.Round(dValue0 - dValueLast, 8);
            int nDirection = dDelta >= 0 ? 1 : -1;
            if (this.Value_delta > 0)
            {
                double dDelta_Step = Math.Round(this.Value_delta * this.Value_base, 8);
                if (dDelta * nDirection > dDelta_Step)
                {
                    dValue0 = this.DataStatistics.Value + dDelta_Step * nDirection;
                    dDelta = Math.Round(dValue0 - dValueLast, 8);
                    this.Value_last = dValue0; this.Time_last = time;
                    bHitLimit = true;
                }
            }
            this.DataStatistics.Statistics(dValue0, time);


            //计算变化区间
            typeMonitor monitorType = typeMonitor.NONE;
            typeMonitor2 monitorType2 = typeMonitor2.NONE;
            double dRatio = Math.Round(dDelta / this.Value_base, 6);
            ConsoleHelper.Debug("监测值：{0}-{1}，变动：{2}，时间：{3}", dValue0, value, dRatio, time.ToString("HH:mm:ss"));
            if (dRatio == 0) return true;

            //识别变化方向
            if (dRatio * this.Value_last_direction >= 0)    //同方向，超限触发超限点及该值
            {
                if (dRatio > 0)     //上升,新高       
                {
                    monitorType = typeMonitor.RAISE; monitorType2 = typeMonitor2.RAISE; this.Value_last_direction = 1;
                }
                else               //下降，新低
                {
                    monitorType = typeMonitor.FALL; monitorType2 = typeMonitor2.FALL; this.Value_last_direction = -1;
                }

                //超限跨区间限制处理
                if (Math.Abs(dRatio) < this.Value_delta)
                {
                    //前值记录
                    if (this.Value_last_direction * (dValue0 - this.Value) > 0)
                    {
                        this.Value = dValue0;
                    }
                    else
                    {
                        //标识波动
                        monitorType2 = this.Value_last_direction < 0 ? typeMonitor2.RAISE_WAVE : typeMonitor2.RAISE_WAVE;
                    }
                }
                else
                {
                    this.Value = dValue0;
                }

                //递归修正，不触发
                if (recursion)
                {
                    monitorType = typeMonitor.NONE;
                }

                //第一个数据直接退出
                if (this.Datas.Values.Count <= 1)
                    return true;
            }
            else
            {
                //拐点判断(反向超限即为拐点)
                double valueLimit = this.Value_last_direction > 0 ? this.DataStatistics.Max : this.DataStatistics.Min;
                double ratioLimit = (dValue0 - valueLimit) / this.Value_base * (4 / 3.0);
                if (Math.Abs(ratioLimit) > this.Value_delta)
                {
                    double dMin = this.Value_last_direction < 0 ? this.DataStatistics.Min : dValue0;
                    double dMax = this.Value_last_direction > 0 ? this.DataStatistics.Max : dValue0;
                    this.InitDataStatistics(dValue0, time, dMax, dMin);     //初始新统计对象
                    this.Value = dValue0;

                    monitorType = typeMonitor.BREAK; bHitLimit = true; this.Value_last_direction *= -1;
                    monitorType2 = this.Value_last_direction < 0 ? typeMonitor2.FALL_BREAK : typeMonitor2.RAISE_BREAK;
                }
            }

            //组装消息
            if (monitorType != typeMonitor.NONE)
            {
                double profit = Math.Round(this.DataStatistics.Value / this.Value_base - 1, 6);
                var msg = new { Type = monitorType, codeState = this.Value_last_direction, hitLimit = bHitLimit, Value = this.DataStatistics.Value, Ratio = dRatio, Profit = profit };

                if (this.DataAnalyse_Trigger != null)
                {
                    DataAnalyse_EventArgs pArgs = new DataAnalyse_EventArgs();
                    pArgs.MonitorType = monitorType;
                    pArgs.MonitorType2 = monitorType2;
                    pArgs.Value = dValue0;
                    this.DataAnalyse_Trigger(this, pArgs);
                }
                ConsoleHelper.Debug("{0}", msg.ToString());
                //self.datasMonitor.append([index, valueLast, monitorType, self.state, hitLimit])
            }

            //超限点递归处理
            if (bHitLimit)
            {
                return this.dataHandle(value, time, true);
            }

            //double dMin2 = this.Value_last_direction < 0 ? this.DataStatistics.Min : this.DataStatistics.Max;
            //value - this.
            //this.Value = value;     //前值（节点新高心底）
            //this.DataStatistics.Statistics(this.Value_last, this.Time_last);   //向前修正到节点
            return true;
        }
    }
}
