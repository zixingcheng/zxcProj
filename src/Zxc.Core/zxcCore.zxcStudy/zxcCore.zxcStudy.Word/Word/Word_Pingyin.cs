using System;
using System.IO;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>汉字四声类型
    /// </summary>
    public enum typeSiSheng
    {
        [EnumAttr("轻声", "0"), EnumValue(0)]
        轻声 = 0,
        [EnumAttr("平声", "1"), EnumValue(0)]
        一声 = 1,
        [EnumAttr("上声", "2"), EnumValue(0)]
        二声 = 2,
        [EnumAttr("去声", "3"), EnumValue(0)]
        三声 = 3,
        [EnumAttr("入声", "4"), EnumValue(0)]
        四声 = 4,
    }


    /// <summary>汉字拼音类
    /// </summary>
    public class Word_Pingyin : Data_Models
    {
        #region 属性及构造

        /// <summary>读音字符串
        /// </summary>
        public string Pinyin
        {
            get; set;
        }
        /// <summary>读音字符串(不含读音)
        /// </summary>
        public string Pinyin_Alias
        {
            get; set;
        }
        /// <summary>声母
        /// </summary>
        public string Shengmu
        {
            get; set;
        }
        /// <summary>韵母
        /// </summary>
        public string Yunmu
        {
            get; set;
        }
        /// <summary>四声
        /// </summary>
        public typeSiSheng Sisheng
        {
            get; set;
        }
        /// <summary>字读音
        /// </summary>
        public string Sound
        {
            get; set;
        }


        public Word_Pingyin()
        {
        }
        ~Word_Pingyin()
        {
            // 缓存数据？
        }

        #endregion


        //初始汉字拼音信息 
        public bool Init_ByUrl(string strPinyin, string urlVedio, string dirBase)
        {
            this.Pinyin = strPinyin;

            //分析四声
            string fileName = Path.GetFileNameWithoutExtension(urlVedio);
            string strSiSheng = fileName.Substring(fileName.Length - 1);
            strSiSheng = string.IsNullOrEmpty(strSiSheng) ? "0" : strSiSheng;
            this.Sisheng = (typeSiSheng)Enum.Parse(typeof(typeSiSheng), strSiSheng);
            this.Pinyin_Alias = fileName.Substring(0, fileName.Length - strSiSheng.Length);

            this.Sound = Path.GetFileName(urlVedio);
            string filePath = dirBase + this.Sound;
            try
            {
                byte[] bytBuffer = zxcNetHelper.Download_Image(urlVedio);
                return zxcIOHelper.WriteBytesToFile(filePath, bytBuffer);
            }
            catch (Exception)
            {
                throw;
            }
        }

        //提取汉字读音
        public string Get_Sound(string dirBase)
        {
            return dirBase + this.Sound;
        }

    }
}
