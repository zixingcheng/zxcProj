using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Swap
{
    public class DataSwap_AckInfo
    {
        #region 属性及构造

        public bool IsAcked { get; set; }
        public DateTime Time { get; set; }
        public DateTime TimeAcked { get; set; }
        public int Retrys { get; set; }
        public string Path { get; set; }

        public DataSwap_AckInfo(string path, DateTime time, int retrys = 0, bool isAcked = false)
        {
            Path = path;
            Retrys = retrys;
            Time = time;
            IsAcked = isAcked;
        }
        ~DataSwap_AckInfo()
        {
            // 缓存数据？
        }

        #endregion
    }
}