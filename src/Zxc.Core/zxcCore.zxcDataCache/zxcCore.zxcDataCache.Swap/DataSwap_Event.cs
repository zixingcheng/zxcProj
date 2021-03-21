using System;
using System.Collections.Generic;

namespace zxcCore.zxcDataCache.Swap
{
    public delegate void DataSwapChange_EventHandler(object sender, DataSwap_Event e);

    public class DataSwap_Event : EventArgs
    {
        #region 属性及构造

        protected internal List<dynamic> _Datas = null;
        public List<dynamic> Datas
        {
            get { return _Datas; }
        }

        public DataSwap_Event()
        {
        }
        ~DataSwap_Event()
        {
            // 缓存数据？
        }

        #endregion
    }

}