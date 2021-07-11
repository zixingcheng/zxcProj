using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据趋势关键线对象
    /// </summary>
    public class DataTrend_KeyLine
    {
        #region 属性及构造

        protected internal string _Tag = "";
        /// <summary>当前标签（对应指标名称）
        /// </summary>
        public string Tag { get { return _Tag; } }

        protected internal double _Value_Line = double.NaN;
        /// <summary>关键重点线位置值
        /// </summary>
        public virtual double Value_Line { get { return _Value_Line; } }
        protected internal bool _IsSupportLine = false;
        /// <summary>是否为支撑线（否则为压力线）
        /// </summary>
        public virtual bool IsSupportLine { get { return _IsSupportLine; } }

        protected internal bool _IsValid = false;
        /// <summary>是否有效
        /// </summary>
        public virtual bool IsValid { get { return _IsValid; } }


        protected internal bool _autoSupportLine = false;           //自动切换，压力线、支撑线自动转换
        protected internal double _valueDelta = 0.191;              //压力线区间幅度
        protected internal double _Value_Line_Min = double.NaN;     //压力线区间下线
        protected internal double _Value_Line_Max = 0.191;          //压力线区间上线
        protected internal double _valueLine_Last = double.NaN;     //前值
        protected internal Dictionary<int, double> _Values_Line;    //压力线区间上线
        public DataTrend_KeyLine(double value, bool isSupportLine = true, string tag = "", double valueDelta = 0.0191, bool autoSupportLine = true)
        {
            _Tag = tag;
            _Value_Line = value;
            _valueDelta = valueDelta;
            _autoSupportLine = autoSupportLine;
            _IsSupportLine = isSupportLine;

            if (value < 0)
                _valueDelta = -_valueDelta;
            _Value_Line_Min = (1 - _valueDelta) * _Value_Line;
            _Value_Line_Max = (1 + _valueDelta) * _Value_Line;
            _Values_Line = new Dictionary<int, double>()
            {
                { 0 ,_Value_Line_Min },
                { 1, _Value_Line },
                { 2, _Value_Line_Max }
            };
            _IsValid = true;
        }

        #endregion


        //自动检测修正支撑线、压力线
        public virtual bool Check_SupportLine(double value)
        {
            if (double.IsNaN(_valueLine_Last))
            {
                _valueLine_Last = value;
            }

            //自动纠正
            if (_autoSupportLine)
            {
                if (_valueLine_Last > _Value_Line_Max)
                    this._IsSupportLine = true;
                else if (_valueLine_Last < _Value_Line_Min)
                    this._IsSupportLine = false;
                _valueLine_Last = double.IsNaN(_valueLine_Last) ? value : _valueLine_Last;
            }
            return true;
        }

        /// <summary>趋势分析-关键线
        /// </summary>
        /// <param name="value">当前值</param>
        /// <param name="valueLast">前一个值</param>
        /// <returns></returns>
        public virtual (typeDataTrend, typeDataTrend_KeyPoint, double) Analysis(double value)
        {
            this.Check_SupportLine(value);
            if (this.IsSupportLine)
                return this.Analysis_LineSupport(value);
            else
                return this.Analysis_LinePressure(value);
        }
        //趋势分析-关键线(压力线)
        protected internal virtual (typeDataTrend, typeDataTrend_KeyPoint, double) Analysis_LinePressure(double value)
        {
            double dValue_KeyPoint = this._Value_Line;
            typeDataTrend pTrend = typeDataTrend.NONE;
            typeDataTrend_KeyPoint pTrend_KeyPoint = typeDataTrend_KeyPoint.NONE;

            if (this._IsValid && !this.IsSupportLine)
            {
                //压力线(前值在上线下方)
                double dValue = value, dValueLast = _valueLine_Last;

                //确定前置区间段
                int nInterval = this.Analysis_Interval(dValue);
                int nInterval_Last = this.Analysis_Interval(dValueLast);


                //判断方向: -1、0、1 对应 typeDataTrend
                int nTrend = nInterval - nInterval_Last;
                nTrend = nTrend > 1 ? 1 : nTrend < -1 ? -1 : nTrend;
                pTrend = (typeDataTrend)Enum.Parse(typeof(typeDataTrend), nTrend.ToString());

                //计算关键点信息
                if (nTrend > 0)
                    nInterval = nInterval - 1;      //向上 修正实际位置 -1

                int nTrend_Point = 10 + nInterval;
                if (nTrend != 0 && Math.Abs(value / _valueLine_Last) > _valueDelta * 0.382)
                {
                    pTrend_KeyPoint = (typeDataTrend_KeyPoint)Enum.Parse(typeof(typeDataTrend_KeyPoint), nTrend_Point.ToString());
                    dValue_KeyPoint = _Values_Line[nInterval];
                }
                _valueLine_Last = value;
            }
            return (pTrend, pTrend_KeyPoint, dValue_KeyPoint);
        }
        //趋势分析-关键线(支撑线)
        protected internal virtual (typeDataTrend, typeDataTrend_KeyPoint, double) Analysis_LineSupport(double value)
        {
            double dValue_KeyPoint = this._Value_Line;
            typeDataTrend pTrend = typeDataTrend.NONE;
            typeDataTrend_KeyPoint pTrend_KeyPoint = typeDataTrend_KeyPoint.NONE;

            if (this._IsValid)
            {
                //压力线(前值在上线下方)
                double dValue = value, dValueLast = _valueLine_Last;

                //确定前置区间段
                int nInterval = this.Analysis_Interval(dValue);
                int nInterval_Last = this.Analysis_Interval(dValueLast);


                //判断方向: -1、0、1 对应 typeDataTrend
                int nTrend = nInterval - nInterval_Last;
                nTrend = nTrend > 1 ? 1 : nTrend < -1 ? -1 : nTrend;
                pTrend = (typeDataTrend)Enum.Parse(typeof(typeDataTrend), nTrend.ToString());

                //计算关键点信息
                if (nTrend > 0)
                    nInterval = nInterval - 1;      //向上 修正实际位置 -1

                int nTrend_Point = -12 + nInterval;
                if (nTrend != 0 && Math.Abs(value / _valueLine_Last) > _valueDelta * 0.382)
                {
                    pTrend_KeyPoint = (typeDataTrend_KeyPoint)Enum.Parse(typeof(typeDataTrend_KeyPoint), nTrend_Point.ToString());
                    dValue_KeyPoint = _Values_Line[nInterval];
                }
                _valueLine_Last = value;
            }
            return (pTrend, pTrend_KeyPoint, dValue_KeyPoint);
        }

        //分析对应的区间段
        protected internal virtual int Analysis_Interval(double value)
        {
            foreach (var item in _Values_Line)
            {
                if (value < item.Value)
                    return item.Key;
            }
            return 3;
        }

    }

}
