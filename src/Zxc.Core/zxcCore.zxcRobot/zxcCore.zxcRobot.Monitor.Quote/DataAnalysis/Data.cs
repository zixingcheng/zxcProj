using System;
using System.Collections.Generic;
using System.Linq;
using zpCore.zpDataCache.Memory;
using zxcCore.Common;

namespace zxcCore.zxcRobot.DataAnalysis
{
    /// <summary>数据对象
    /// </summary>
    /// 
    public class Data
    {
        #region 属性及构造

        /// <summary>当前值
        /// </summary>
        public double Value { get; set; }
        /// <summary>当前值时间
        /// </summary>
        public DateTime Time { get; set; }

        public Data(double value)
        {
            Value = value;
            Time = DateTime.Now;
        }
        public Data(double value, DateTime time)
        {
            Value = value;
            Time = time;
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
