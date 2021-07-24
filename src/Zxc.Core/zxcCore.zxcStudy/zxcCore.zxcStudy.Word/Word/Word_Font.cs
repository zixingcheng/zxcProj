using System;
using System.IO;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>汉字字体类型
    /// </summary>
    public enum typeFace
    {
        /// <summary>中宋体
        /// </summary>
        [EnumAttr("中宋体", "0"), EnumValue(0)]
        中宋体 = 0,
        /// <summary>仿宋体
        /// </summary>
        [EnumAttr("仿宋体", "1"), EnumValue(0)]
        仿宋体 = 1,
        /// <summary>楷体
        /// </summary>
        [EnumAttr("楷体", "10"), EnumValue(0)]
        楷体 = 10,
        /// <summary>黑体
        /// </summary>
        [EnumAttr("黑体", "20"), EnumValue(0)]
        黑体 = 20,
    }


    /// <summary>汉字字体类
    /// </summary>
    public class Word_Font : Data_Models
    {
        #region 属性及构造

        /// <summary>汉字字符串
        /// </summary>
        public string WordStr
        {
            get; set;
        }

        /// <summary>字体
        /// </summary>
        public typeFace TypeFace
        {
            get; set;
        }


        public Word_Font()
        {
        }
        ~Word_Font()
        {
            // 缓存数据？
        }

        #endregion


        //初始汉字字体图片  
        public bool Init_ByUrl(string urlImgFont, string dirBase)
        {
            string nameFace = this.TypeFace == typeFace.中宋体 ? "" : "_" + this.WordStr;
            string filePath = dirBase + WordStr + nameFace + ".png";
            try
            {
                byte[] bytBuffer = zxcNetHelper.Download_Image(urlImgFont);
                return zxcIOHelper.WriteBytesToFile(filePath, bytBuffer);
            }
            catch (Exception)
            {
                throw;
            }
        }
        //初始汉字字体笔顺图片 
        public bool InitStroke_ByUrl(string urlImgFontStroke, string dirBase)
        {
            string nameFace = this.TypeFace == typeFace.中宋体 ? "" : "_" + this.WordStr;
            string filePath = dirBase + WordStr + nameFace + ".gif";
            try
            {
                byte[] bytBuffer = zxcNetHelper.Download_Image(urlImgFontStroke);
                return zxcIOHelper.WriteBytesToFile(filePath, bytBuffer);
            }
            catch (Exception)
            {
                throw;
            }
        }

        //提取汉字字体图片 
        public string Get_Image(string dirBase)
        {
            string nameFace = this.TypeFace == typeFace.中宋体 ? "" : "_" + this.WordStr;
            string filePath = dirBase + WordStr + nameFace + ".png";
            return filePath;
        }
        //提取汉字字体笔顺图片 
        public string Get_StrokesImage(string dirBase)
        {
            string nameFace = this.TypeFace == typeFace.中宋体 ? "" : "_" + this.WordStr;
            string filePath = dirBase + WordStr + nameFace + ".gif";
            return filePath;
        }

    }

}
