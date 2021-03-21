using System;
using System.Collections.Generic;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据模型对象类
    /// </summary>
    public abstract class Data_Models : IData
    {
        #region 属性及构造

        public Data_Models()
        {
        }

        #endregion


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
