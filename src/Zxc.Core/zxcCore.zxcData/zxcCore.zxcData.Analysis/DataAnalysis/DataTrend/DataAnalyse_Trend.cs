using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using zxcCore.Common;
using zxcCore.Enums;
using zxcCore.Extensions;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据趋势分析--基类
    /// </summary> 
    public class DataAnalyse_Trend
    {
        #region 属性及构造

        /// <summary数据趋势分析事件
        /// </summary>
        public event DataAnalyse_Trend_EventHandler DataAnalyse_Trend_Trigger;

        ///// <summary数据交换事件
        ///// </summary>
        //public event DataAnalyse_KeyPoints_EventHandler DataAnalyse_Trigger;
        protected typeTimeFrequency _ValueTimeType = typeTimeFrequency.none;
        /// <summary>数据时间类型
        /// </summary>
        public typeTimeFrequency ValueTimeType
        {
            get { return _ValueTimeType; }
        }

        /// <summary>有效差值范围
        /// </summary>
        protected double _valueDelta { get; set; }
        /// <summary>有效差值步长
        /// </summary>
        protected double _valueStep { get; set; }
        /// <summary>当前阶段最大值
        /// </summary>
        protected double _valueMax { get; set; }
        /// <summary>当前阶段最小值
        /// </summary>
        protected double _valueMin { get; set; }

        /// <summary>基值-不变（未指定时自动初始为第一个数据）
        /// </summary>
        protected DataTrend_Index _valueBase { get; set; }
        /// <summary>当前值
        /// </summary>（实际值）
        protected DataTrend_Index _value { get; set; }
        /// <summary>当前值(修正)
        /// </summary>
        protected DataTrend_Index _value_Amend { get; set; }
        /// <summary>前一值（实际值）
        /// </summary>
        protected DataTrend_Index _valueLast { get; set; }
        /// <summary>前一值-修正（有效差值点）
        /// </summary>
        protected DataTrend_Index _valueLast_Amend { get; set; }
        /// <summary>数据对象集
        /// </summary>
        protected internal List<DataTrend_Index> _dataIndexCaches = null;


        ///// <summary>数据统计对象
        ///// </summary>
        protected DataStatistics _dataStatistics { get; set; }
        /// <summary>数据统计对象集（阶段）
        /// </summary>
        protected List<DataStatistics> lstDataStatistics { get; set; }

        /// <summary>是否已经初始
        /// </summary>
        protected internal bool _IsInited = false;
        public bool IsInited
        {
            get { return _IsInited; }
        }


        protected internal int _indTag = 0;
        protected internal string _tag = "";
        protected internal double _valueDelta_half = 0;
        protected internal bool _useFixed = false;
        protected internal bool _useConsole = false;
        protected internal Dictionary<string, DataTrend_KeyLine> _dataKeyLines = null;      //关键点位线集
        public DataAnalyse_Trend(string tag = "", typeTimeFrequency valueTimeType = typeTimeFrequency.none)
        {
            _tag = string.IsNullOrEmpty(tag) ? "DataAnalyse_Index" : tag;
            _ValueTimeType = valueTimeType;
            this._dataIndexCaches = new List<DataTrend_Index>();
            this._dataKeyLines = new Dictionary<string, DataTrend_KeyLine>();
        }

        #endregion


        /// <summary>数据初始实现
        /// </summary>
        /// <param name="value"></param>
        /// <param name="valueBase">基值</param>
        /// <param name="time">基值时间</param>
        /// <param name="max">最大值</param>
        /// <param name="min">最小值</param>
        /// <param name="valueDelta">数据变化幅度有效值</param>
        /// <returns></returns>
        public virtual bool Init(double valueBase, DateTime dtTime, double valueDelta = 0.0025, double valueMax = double.MinValue, double valueMin = double.MaxValue, double valueSetp = double.NaN)
        {
            if (_IsInited) return true;
            this._valueDelta = valueDelta;
            this._valueDelta_half = valueDelta / 2 * 100;
            this._valueBase = this.Create_IndexData(valueBase, dtTime);
            this._value = _valueBase;
            this._valueLast = _valueBase;
            this._valueStep = !double.IsNaN(valueSetp) ? valueSetp : Math.Round(this._valueDelta * this._valueBase.Value, 8);  //计算有效值步长（对应有效值区间）

            this.lstDataStatistics = new List<DataStatistics>();
            this.InitStatistics(_valueBase.Value, _valueBase.Time, valueMax, valueMin);

            //缓存及统计数据
            //_IsInited = this.dataHandle(_valueBase);

            _useFixed = valueDelta != 0;        //标识是否细分到固定间隔
            if (_useFixed)
            {
                this._value_Amend = _valueBase;
                this._valueLast_Amend = _valueBase;
            }

            _IsInited = true;
            return _IsInited;
        }
        //初始统计对象-阶段
        public virtual bool InitStatistics(double value, DateTime time, double valueMax = double.MinValue, double valueMin = double.MaxValue)
        {
            this._dataStatistics = new DataStatistics();
            this._dataStatistics.Init(value, time, this._valueStep, _indTag.ToString(), valueMax, valueMin);
            this._dataStatistics._useConsole = this._useConsole;
            this.lstDataStatistics.Add(this._dataStatistics);

            _valueMax = _dataStatistics.Max;
            _valueMin = _dataStatistics.Min;
            _indTag++;
            return true;
        }
        //初始趋势分析关键点位线对象
        public virtual bool InitTrend_KeyLine(string tag, double value, bool isSupport, double valueDelta = 0.0191, bool bCover = true)
        {
            DataTrend_KeyLine pKeyLine = null;
            if (_dataKeyLines.TryGetValue(tag, out pKeyLine))
            {
            }

            //初始
            if (bCover || pKeyLine == null)
            {
                pKeyLine = new DataTrend_KeyLine(value, isSupport, tag, valueDelta);
                _dataKeyLines[tag] = pKeyLine;
            }
            return pKeyLine != null;
        }



        //数据分析（趋势、趋势详情、关键点信息等）
        public virtual bool Analysis(double value, DateTime time, bool bVaild = true)
        {
            //实例数据
            DataTrend_Index pData = this.Create_IndexData(value, time, this._valueLast);
            pData._IsValid = bVaild;

            //数据处理
            if (this.dataHandle(pData))
                return true;
            return false;
        }


        /// <summary>数据处理
        /// </summary>
        /// <param name="data">当前值</param>
        /// <param name="dataLast_Recursion">递归用前值</param>
        /// <returns></returns>
        protected virtual bool dataHandle(DataTrend_Index data, DataTrend_Index dataLast_Recursion = null)
        {
            //计算差值区间
            DataTrend_Index pDataSetp = data;
            double dValue_Last = dataLast_Recursion == null ? this.getValue_Last(true).Value : dataLast_Recursion.Value;
            double dDelta = Math.Round(pDataSetp.Value - dValue_Last, 8);       //与前一个值的差值

            //数据校正到固定区间
            bool bHitLimit = false;                         //是否超出范围，需要递归
            int nDirection = dDelta >= 0 ? 1 : -1;          //升降标识，升为正，降为负
            if (_useFixed)
            {
                // 差值超过一个步长，拆分到固定区间再计算
                if (Math.Abs(dDelta * nDirection) >= _valueStep)
                {
                    dDelta = _valueStep * nDirection;       //修正为步长
                    bHitLimit = true;

                    //修正数据到固定间隔位置，递归计算
                    pDataSetp = this.Create_IndexData(dValue_Last + dDelta, pDataSetp.Time, this._value_Amend, data);
                    pDataSetp._IsHitPoint = true;
                    pDataSetp._IsValid = true;
                }
            }
            this._value = data;
            if (pDataSetp._IsHitPoint)
                this._value_Amend = _useFixed ? pDataSetp : null;
            else
                //未命中修正为当前修正对象
                pDataSetp._DataTrend_Index_Last = _useFixed ? this._value_Amend : null;

            //更新差值并统计更新
            pDataSetp.LabelInfo.Difference = dDelta;
            pDataSetp.LabelInfo.Difference_Ratio = Math.Round(dDelta / this._valueBase.Value, 8);
            pDataSetp.LabelInfo.Value = Math.Round(pDataSetp.Value, 8);
            pDataSetp.LabelInfo.Value_Amend = Math.Round(this.getValue(true).Value, 8);
            pDataSetp.LabelInfo.Value_Profit = this.getProfit(pDataSetp);
            this._dataStatistics.Statistics(pDataSetp.Value, pDataSetp.Time);
            _dataIndexCaches.Add(pDataSetp);


            //数据处理
            bool bResult = this.dataHandle_DataTrend(pDataSetp);
            if (pDataSetp._DataTrend_Index_Last._DataTrend_Index_Last != null)
            {
                //bResult = bResult && dataHandle_DataTrend_Detail(pDataSetp);
                bResult = bResult && dataHandle_DataTrend_KeyLine(pDataSetp);
                bResult = bResult && dataHandle_DataTrend_KeyPoint(pDataSetp, data);
                bResult = bResult && dataHandle_User(pDataSetp, data);
            }
            if (bResult)
                bResult = this.dataHandle_Event(pDataSetp);


            //超限点递归处理
            if (bHitLimit)
                return this.dataHandle(data, pDataSetp);

            //更新前值
            if (!data.IsVirtual)
            {
                this._valueLast = _value;
                this._valueLast_Amend = _useFixed ? _value_Amend : null;
            }
            return bResult;
        }
        //数据处理--数据趋势
        protected virtual bool dataHandle_DataTrend(DataTrend_Index data)
        {
            //趋势判断
            DataTrend_LabelInfo pLabelInfo = data.LabelInfo;
            double dDelta = pLabelInfo.Difference_Ratio;
            if (Math.Abs(dDelta) >= _valueDelta)
            {
                pLabelInfo.DataTrend = dDelta > 0 ? typeDataTrend.RAISE : dDelta < 0 ? typeDataTrend.FALL : typeDataTrend.NONE;
            }
            else
            {
                pLabelInfo.DataTrend = typeDataTrend.NONE;
            }
            return true;
        }
        //数据处理--数据趋势详情
        protected virtual bool dataHandle_DataTrend_Detail(DataTrend_Index data)
        {
            //趋势详情判断
            DataTrend_LabelInfo pLabelInfo = data.LabelInfo;
            double dDelta = pLabelInfo.Difference;

            //利用前值进行计算(屏蔽第一个值)
            if (data._DataTrend_Index_Last._DataTrend_Index_Last != null)
            {
                double dDelta1 = data._DataTrend_Index_Last.LabelInfo.Difference;
                double dDirection = dDelta * dDelta1;               //同向标识，升为正，降为负
                double dDRatio = dDelta / dDelta1;                  //前后差值升降幅度

                pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.NONE;
                if (dDirection > 0)
                {
                    if (dDRatio > 1.125 && dDRatio < 1.5)
                    {
                        pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SPEEDUP;
                    }
                    else if (dDRatio >= 1.5)
                    {
                        pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SPEEDTOP;
                    }
                    else if (dDRatio < -0.25 && dDRatio > -1)
                    {
                        pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SLOWDOWN;
                    }
                    else if (dDRatio <= -1)
                    {
                        pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SLOWTOP;
                    }
                }
                else
                {
                    // 波动处
                    if (dDelta1 > 0)
                    {
                        if (dDRatio < -0.25 && dDRatio > -1)
                        {
                            pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SLOWDOWN;
                        }
                        else if (dDRatio <= -1)
                        {
                            pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SLOWTOP;
                        }
                    }
                    else
                    {
                        if (dDRatio > 1.125 && dDRatio < 1.5)
                        {
                            pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SPEEDUP;
                        }
                        else if (dDRatio >= 1.5)
                        {
                            pLabelInfo.DataTrend_Detail = typeDataTrend_Detail.SPEEDTOP;
                        }
                    }
                }
            }
            return true;
        }
        //数据处理--数据趋势关键线
        protected virtual bool dataHandle_DataTrend_KeyLine(DataTrend_Index data)
        {
            bool bResult = true;
            DataTrend_LabelInfo pLabelInfo = data.LabelInfo;
            DataTrend_LabelInfo pLabelInfo_Orgin = null;

            foreach (var item in _dataKeyLines)
            {
                (typeDataTrend, typeDataTrend_KeyPoint, double) pResult = item.Value.Analysis(data.Value);
                if (pResult.Item1 != typeDataTrend.NONE)
                {
                    if (_useConsole)
                        zxcConsoleHelper.Debug(true, "监测值：{3}, {0} {1} ({2})", pResult.Item1.ToString(), pResult.Item2.ToString(), pResult.Item3, Math.Round(data.Value, 6));

                    //复制备用
                    if (pLabelInfo_Orgin == null)
                        pLabelInfo_Orgin = zxcCloneDeep.Clone<DataTrend_LabelInfo>(pLabelInfo);

                    //更新值
                    pLabelInfo.Tag = item.Key;
                    pLabelInfo.DataTrend = pResult.Item1;
                    pLabelInfo.DataTrend_KeyPoint = pResult.Item2;
                    pLabelInfo.Value_KeyLine = pResult.Item3;
                    bResult = bResult && this.dataHandle_Event(data);
                }
            }

            //还原 
            if (pLabelInfo_Orgin != null)
            {
                pLabelInfo.Tag = pLabelInfo_Orgin.Tag;
                pLabelInfo.DataTrend = pLabelInfo_Orgin.DataTrend;
                pLabelInfo.DataTrend_KeyPoint = pLabelInfo_Orgin.DataTrend_KeyPoint;
                pLabelInfo.Value_KeyLine = pLabelInfo_Orgin.Value_KeyLine;
            }
            return bResult;
        }
        //数据处理--数据趋势关键点
        protected virtual bool dataHandle_DataTrend_KeyPoint(DataTrend_Index data, DataTrend_Index dataLast_Recursion = null)
        {
            //计算变化幅度
            DataTrend_LabelInfo pLabelInfo = data.LabelInfo;
            double dRatio = Math.Round(pLabelInfo.Difference / this._valueBase.Value, 6);

            pLabelInfo.Difference_Ratio = dRatio;
            if (_useConsole)
                zxcConsoleHelper.Debug(true, "监测值：{1} ({0})，变动：{2}，时间：{3}", Math.Round(data.Value, 6), dataLast_Recursion.Value, dRatio, data.Time.ToString("HH:mm:ss"));
            if (dRatio == 0) return true;


            //识别变化方向
            double dValue = data.Value;
            int nDirection_Last = (int)this._valueLast_Amend.LabelInfo.DataTrend;           //升降标识，升为正，降为负
            if (dRatio * nDirection_Last >= 0)                  //同方向，超限触发超限点及该值
            {
                if (dRatio > 0 && _valueMax <= data.Value)      //上升,关键点--阶段新高       
                {
                    if (data.Value - _valueMax >= 0.5 * _dataStatistics.Value_interval)
                    {
                        _valueMax = data.IsHitPoint ? this._dataStatistics.Max : this._dataStatistics.Max + 0.5 * _dataStatistics.Value_interval;
                        pLabelInfo.DataTrend_KeyPoint = typeDataTrend_KeyPoint.MAX;
                    }
                }
                else if (dRatio < 0 && _valueMin >= data.Value)     //下降，关键点--阶段新低
                {
                    if (_valueMin - data.Value >= 0.5 * _dataStatistics.Value_interval)
                    {
                        _valueMin = data.IsHitPoint ? this._dataStatistics.Min : this._dataStatistics.Min - 0.5 * _dataStatistics.Value_interval;
                        pLabelInfo.DataTrend_KeyPoint = typeDataTrend_KeyPoint.MIN;
                    }
                }
            }
            else
            {
                //拐点判断(反向超限即为拐点)
                double valueLimit = nDirection_Last > 0 ? this._dataStatistics.Max_Original : this._dataStatistics.Min_Original;
                double ratioLimit = dValue - valueLimit;
                if (Math.Abs(ratioLimit) - this._valueStep > -0.00000001)
                {
                    //初始新统计对象
                    double dMin = nDirection_Last < 0 ? this._dataStatistics.Min_Original : dValue;
                    double dMax = nDirection_Last > 0 ? this._dataStatistics.Max_Original : dValue;
                    this.InitStatistics(dValue, data.Time, dMax, dMin);

                    //标识关键点--拐点信息
                    pLabelInfo.Value_KeyLine = valueLimit + _valueStep * nDirection_Last;
                    pLabelInfo.DataTrend_KeyPoint = typeDataTrend_KeyPoint.INFLECTION;
                    pLabelInfo.DataTrend = ratioLimit > 0 ? typeDataTrend.RAISE : typeDataTrend.FALL;   //修正当前方向
                    this._valueLast_Amend.LabelInfo.DataTrend = pLabelInfo.DataTrend;                   //修正前一(缓存修正对象)方向
                }
            }
            return true;
        }
        //数据处理--自定义
        protected virtual bool dataHandle_User(DataTrend_Index data, DataTrend_Index dataLast_Recursion = null)
        {
            return true;
        }

        //数据处理事件
        protected virtual bool dataHandle_Event(DataTrend_Index data)
        {
            //组装消息
            if (data._IsValid && this.DataAnalyse_Trend_Trigger != null)
            {
                DataAnalyse_Trend_EventArgs pArgs = this.dataHandle_EventArgs(data);
                if (pArgs != null)
                    this.DataAnalyse_Trend_Trigger(this, pArgs);
                return true;
            }
            return true;
        }
        //数据处理事件返回对象
        protected virtual DataAnalyse_Trend_EventArgs dataHandle_EventArgs(DataTrend_Index data)
        {
            //组装消息
            DataAnalyse_Trend_EventArgs pArgs = new DataAnalyse_Trend_EventArgs()
            {
                _data = data
            };

            //输出信息
            if (_useConsole)
            {
                double profit = data.LabelInfo.Value_Profit;
                var msg = new { DataTrend = data.LabelInfo.DataTrend, DataTrend_Detail = data.LabelInfo.DataTrend_Detail, DataTrend_KeyPoint = data.LabelInfo.DataTrend_KeyPoint, hitLimit = data.IsHitPoint, Value = data.Value, Ratio = data.LabelInfo.Difference_Ratio, Profit = profit };
                zxcConsoleHelper.Debug(true, "{0}", msg.ToString());
            }
            return pArgs;
        }



        //提取当前值
        protected virtual DataTrend_Index getValue(bool isAmend = false)
        {
            return isAmend && _useFixed ? _value_Amend : _value;
        }
        //提取前一对象
        protected virtual DataTrend_Index getValue_Last(bool isAmend = false)
        {
            return isAmend && _useFixed ? _valueLast_Amend : _valueLast;
        }
        //计算涨跌幅
        protected virtual double getProfit(DataTrend_Index data, int decimals = 6)
        {
            double profit = Math.Round(data.Value / this._valueBase.Value - 1, decimals);
            return profit;
        }


        //设置输出状态
        protected virtual bool setConsoleState(bool useConsole)
        {
            this._useConsole = useConsole;
            if (this._dataStatistics != null)
                this._dataStatistics._useConsole = useConsole;
            return true;
        }


        /// <summary>生成数据对象-指标
        /// </summary>
        /// <param name="value"></param>
        /// <param name="time"></param>
        /// <param name="dataLast">前一值</param>
        /// <param name="dataVirtualBase">虚拟值绑定对象</param>
        /// <returns></returns>
        protected internal virtual DataTrend_Index Create_IndexData(double value, DateTime time, DataTrend_Index dataLast = null, DataTrend_Index dataVirtualBase = null)
        {
            //实例数据
            DataTrend_Index pData = new DataTrend_Index(value, time, this, dataVirtualBase);
            pData._LabelInfo = new DataTrend_LabelInfo();
            pData._LabelInfo.Tag = "DataTrend";
            if (dataLast != null)
                pData.InitLastValue(dataLast);
            return pData;
        }

    }

}
