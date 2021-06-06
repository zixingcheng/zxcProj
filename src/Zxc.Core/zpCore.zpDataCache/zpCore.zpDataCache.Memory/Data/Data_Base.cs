using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据对象类
    /// </summary>
    public class Data_Base : IData
    {
        #region 属性及构造

        public Data_Base()
        {
        }

        #endregion


        public override string ToString()
        {
            return "";
        }
        public virtual void FromString()
        {
        }
        public virtual dynamic ToJson()
        {
            return null;
        }
        public virtual bool FromJson(dynamic jsonData)
        {
            return false;
        }

    }
}
