using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace zxcCore.zxcDataCache.Swap
{
    public class AckInfo
    {
        #region 属性及构造

        /// <summary>确认标识信息
        /// </summary>
        public string AckTag
        {
            get; set;
        }
        /// <summary>交换信息
        /// </summary>
        public string SwapInfo
        {
            get; set;
        }
        /// <summary>是否确认
        /// </summary>
        public bool Acked
        {
            get; set;
        }
        /// <summary>时间
        /// </summary>
        public DateTime Time
        {
            get; set;
        }

        public AckInfo(string ackTag, string swapInfo)
        {
            AckTag = ackTag;
            SwapInfo = swapInfo;
            Time = DateTime.Now;
        }
        ~AckInfo()
        {
            // 缓存数据？
        }

        #endregion

        public virtual bool Ack()
        {
            Acked = true;
            return Acked;
        }
    }
}
