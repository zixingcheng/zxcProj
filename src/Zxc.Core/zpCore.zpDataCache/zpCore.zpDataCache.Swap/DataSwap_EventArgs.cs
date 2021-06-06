using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Swap
{
    public class DataSwap_EventArgs : EventArgs
    {
        #region 属性及构造

        protected internal List<dynamic> _Datas = null;
        public List<dynamic> Datas
        {
            get { return _Datas; }
        }

        public DataSwap_EventArgs()
        {
        }
        ~DataSwap_EventArgs()
        {
            // 缓存数据？
        }

        #endregion
    }
}