using System;
using System.Collections.Generic;
using System.Linq;

namespace zxcCore.zxcData.Analysis
{
    /// <summary>数据对象
    /// </summary>
    /// 
    public class Data
    {
        #region 属性及构造

        protected internal double _Value = 0;
        /// <summary>当前标签（对应指标名称）
        /// </summary>
        public double Value { get { return _Value; } }

        protected internal DateTime _Time = DateTime.MinValue;
        /// <summary>当前标签（对应指标名称）
        /// </summary>
        public DateTime Time { get { return _Time; } }


        public Data(double value)
        {
            _Value = value;
            _Time = DateTime.Now;
        }
        public Data(double value, DateTime time)
        {
            _Value = value;
            _Time = time;
        }

        #endregion

    }

    /// <summary>数据对象集合
    /// </summary>
    /// 
    public class Datas
    {
        #region 属性及构造

        /// <summary>标识
        /// </summary>
        public string Tag { get; set; }
        /// <summary>数据集
        /// </summary>
        public List<Data> Values { get; set; }

        public Datas(string tag)
        {
            Tag = tag;
            Values = new List<Data>();
        }

        public bool AddData(double value, DateTime time)
        {
            Values.Add(new Data(value, time));
            return true;
        }
        public bool AddData(Data data)
        {
            Values.Add(data);
            return true;
        }

        #endregion

    }

}
