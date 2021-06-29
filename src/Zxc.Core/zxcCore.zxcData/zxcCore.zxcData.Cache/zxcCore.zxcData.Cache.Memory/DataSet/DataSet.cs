using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据对象类
    /// </summary>
    public class DataSet : IDataSet
    {
        internal string _tagName;
        public string Tag_Name
        {
            get { return _tagName; }
        }

        public DataSet(string tagName)
        {
            _tagName = tagName;
        }


        /// <summary>配置转为字符串
        /// </summary>
        public override string ToString()
        {
            return "";
        }
        /// <summary>字符串转配置
        /// </summary>
        public virtual void FromString()
        {
        }
    }
}
