using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>五行
    /// </summary>
    public enum typeWuXing
    {
        None = 0,
        [EnumAttr("金", "1"), EnumValue(0)]
        金 = 1,
        [EnumAttr("木", "2"), EnumValue(0)]
        木 = 2,
        [EnumAttr("水", "3"), EnumValue(0)]
        水 = 3,
        [EnumAttr("火", "4"), EnumValue(0)]
        火 = 4,
        [EnumAttr("土", "5"), EnumValue(0)]
        土 = 5,
    }


    public class Word : Data_Models
    {
        #region 属性及构造

        /// <summary>汉字字符串
        /// </summary>
        public string WordStr
        {
            get; set;
        }
        /// <summary>对应英语字符串集
        /// </summary>
        public List<string> WordStrs_EN
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

        /// <summary>读音
        /// </summary>
        public List<string> Pinyins
        {
            get; set;
        }
        /// <summary>字体集合
        /// </summary>
        public List<typeFace> Fonts
        {
            get; set;
        }

        /// <summary>汉字笔画数
        /// </summary>
        public int WordStrokeNum
        {
            get; set;
        }
        /// <summary>汉字笔画顺序
        /// </summary>
        public List<typeStrokes> WordStrokes
        {
            get; set;
        }

        /// <summary>汉字部首
        /// </summary>
        public string WordRadical
        {
            get; set;
        }
        /// <summary>汉字五行归属
        /// </summary>
        public typeWuXing WordWuXing
        {
            get; set;
        }
        /// <summary>汉字标识（百度）
        /// </summary>
        public string WordTag_bd
        {
            get; set;
        }

        /// <summary>汉字版本标签（用于标识对应信息版本）
        /// </summary>
        public string VerTag
        {
            get; set;
        }


        public Word()
        {
            WordStrs_EN = new List<string>();
            Pinyins = new List<string>();
            Fonts = new List<typeFace>();
            WordStrokes = new List<typeStrokes>();
        }
        ~Word()
        {
            // 缓存数据？
        }

        #endregion


        //初始Json缓存信息
        public bool Init_JsonFile()
        {
            string strJson = this.ToJsonStr();
            string filePath = Word_Manager._Manager._dirWordBase + "WordInfos/" + this.WordStr + ".json";
            File.WriteAllText(filePath, strJson);
            return true;
        }

        //设置汉字拼音信息 
        protected internal bool Set_Pinyin(string strPinyin, string urlVedio)
        {
            bool bResult = true;
            Word_Pingyin pPingyin = Word_Manager._Manager.GetWord_Pinyin(strPinyin);
            if (pPingyin == null)
            {
                bResult = Word_Manager._Manager.InitWord_Pinyin(strPinyin, urlVedio);
            }

            //加入新读音
            if (bResult && !Pinyins.Contains(strPinyin))
                Pinyins.Add(strPinyin);
            return bResult;
        }
        //设置汉字字体信息 
        protected internal bool Set_Font(typeFace typeFace, string urlImgFont, string urlImgFontStroke)
        {
            Word_Font pFont = new Word_Font()
            {
                TypeFace = typeFace,
                WordStr = this.WordStr
            };
            if (pFont.Init_ByUrl(urlImgFont, Word_Manager._Manager._dirWordBase + "Fonts/")
                && pFont.InitStroke_ByUrl(urlImgFontStroke, Word_Manager._Manager._dirWordBase + "Strokes/"))
            {
                if (!Fonts.Contains(typeFace))
                    this.Fonts.Add(typeFace);
                return true;
            }
            return false;
        }


        //提取汉字拼音信息
        public Word_Pingyin Get_Pinyin(int ind = 0)
        {
            if (ind >= this.Pinyins.Count) return null;
            return Word_Manager._Manager.GetWord_Pinyin(this.Pinyins[ind]);
        }
        //提取汉字字体图片 
        public string Get_Sound(int ind = 0)
        {
            Word_Pingyin pWord_Pingyin = this.Get_Pinyin(ind);
            if (pWord_Pingyin == null) return "";
            return pWord_Pingyin.Get_Sound(Word_Manager._Manager._dirWordBase + "Sounds/");
        }
        //提取汉字字体图片 
        public string Get_Image(typeFace typeFace = typeFace.中宋体)
        {
            Word_Font pFont = new Word_Font()
            {
                TypeFace = typeFace,
                WordStr = this.WordStr
            };
            return pFont.Get_Image(Word_Manager._Manager._dirWordBase + "Fonts/");
        }
        //提取汉字笔画图片 
        public string Get_StrokesImage(typeFace typeFace = typeFace.中宋体)
        {
            Word_Font pFont = new Word_Font()
            {
                TypeFace = typeFace,
                WordStr = this.WordStr
            };
            return pFont.Get_StrokesImage(Word_Manager._Manager._dirWordBase + "Strokes/");
        }


        //转换为json字符串
        public string ToJsonStr()
        {
            var result = JsonConvert.SerializeObject(this, Formatting.Indented);
            return result;
        }

    }

}
