using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>库表数据对象-日志
    /// </summary>
    public class DataModels_Log : Data_Models
    {
        /// <summary>操作类型
        /// </summary>
        public typePermission_DB OpType { get; set; }
        /// <summary>操作类型
        /// </summary>
        public string OpTable { get; set; }
        /// <summary>操作内容-原始
        /// </summary>
        public string OpInfo_Src { get; set; }
        /// <summary>操作内容-结果
        /// </summary>
        public string OpInfo_To { get; set; }
        /// <summary>操作内容-改变
        /// </summary>
        public string OpInfo_Dif { get; set; }
        /// <summary>备注
        /// </summary>
        public string Remarks { get; set; }
    }
}