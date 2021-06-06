using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据对象类-IOT
    /// </summary>
    public class Data_Iot<T> : Data_Base, IData_Iot<T>
    {
        #region 属性及构造

        DateTime _dtTime;
        public DateTime Time
        {
            get { return _dtTime; }
            set { _dtTime = value; }
        }
        T _value;
        public T Value
        {
            get { return _value; }
            set { _value = value; }
        }

        public Data_Iot(DateTime time, T value)
        {
            Time = time;
            Value = value;
        }

        #endregion


        public override string ToString()
        {
            return "";
        }

    }
}
