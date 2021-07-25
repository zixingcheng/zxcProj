using System;
using System.Collections.Generic;
using System.IO;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Record
{
    /// <summary>汉字学习记录类型
    /// </summary>
    public enum typeWordRecord
    {
        [EnumAttr("字形", "0"), EnumValue(5)]
        字形 = 0,
        [EnumAttr("字义", "1"), EnumValue(5)]
        字义 = 1,
        [EnumAttr("字音", "2"), EnumValue(5)]
        字音 = 2,
        [EnumAttr("笔画", "3"), EnumValue(5)]
        笔画 = 3,
        [EnumAttr("拓展", "4"), EnumValue(5)]
        拓展 = 4
    }


    /// <summary>汉字学习日志类
    /// </summary>
    public class Word_Record : Data_Models
    {
        #region 属性及构造
        /// <summary>学习用户标识
        /// </summary>
        public string UserTag
        {
            get; set;
        }

        /// <summary>汉字字符串
        /// </summary>
        public string WordStr
        {
            get; set;
        }
        /// <summary>汉字顺序-自定义
        /// </summary>
        public int WordInd
        {
            get; set;
        }
        /// <summary>汉字分类-自定义
        /// </summary>
        public string WordType
        {
            get; set;
        }

        /// <summary>学习记录类型
        /// </summary>
        public typeWordRecord RecordType
        {
            get; set;
        }
        /// <summary>学习记录内容
        /// </summary>
        public string RecordInfo
        {
            get; set;
        }


        public Word_Record()
        {
        }
        ~Word_Record()
        {
            // 缓存数据？
        }

        #endregion

    }
}
