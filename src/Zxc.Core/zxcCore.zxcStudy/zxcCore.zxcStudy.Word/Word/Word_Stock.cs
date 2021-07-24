using System;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>汉字笔画类型 
    /// </summary>
    public enum typeStrokes
    {
        [EnumValue(typeStrokes_Base.点)]
        点 = 1,
        [EnumValue(typeStrokes_Base.横)]
        横 = 2,
        [EnumValue(typeStrokes_Base.竖)]
        竖 = 3,
        [EnumValue(typeStrokes_Base.撇)]
        撇 = 4,
        [EnumValue(typeStrokes_Base.捺)]
        捺 = 5,
        [EnumValue(typeStrokes_Base.提)]
        提 = 6,
        [EnumValue(typeStrokes_Base.横折)]
        横折 = 7,
        [EnumValue(typeStrokes_Base.竖钩)]
        竖钩 = 8
    }

    /// <summary>汉字笔画类型 
    /// </summary>
    public enum typeStrokes_Base
    {
        None = 0,
        [EnumWord_Stocks("点", "", "CJK STROKE D", "㇔", "平笔", 0)]
        点 = 1,
        [EnumWord_Stocks("横", "", "CJK STROKE H", "㇐", "平笔", 0)]
        横 = 2,
        [EnumWord_Stocks("竖", "", "CJK STROKE S", "㇑", "平笔", 0)]
        竖 = 3,
        [EnumWord_Stocks("撇", "", "CJK STROKE SP", "㇓", "平笔", 0)]
        撇 = 4,
        [EnumWord_Stocks("捺", "", "CJK STROKE N", "㇏", "平笔", 0)]
        捺 = 5,
        [EnumWord_Stocks("提", "", "CJK STROKE T", "㇀", "平笔", 0)]
        提 = 6,
        [EnumWord_Stocks("横折", "", "CJK STROKE HZ", "㇕", "折笔", 1)]
        横折 = 7,
        [EnumWord_Stocks("竖钩", "", "CJK STROKE SG", "㇚", "平笔", 0)]
        竖钩 = 8,

        [EnumWord_Stocks("横钩", "", "CJK STROKE HG", "㇖", "折笔", 1)]
        横钩 = 210,
        [EnumWord_Stocks("横撇", "", "CJK STROKE HP", "㇇", "折笔", 1)]
        横撇 = 211,
        [EnumWord_Stocks("横折钩", "横折竖钩", "CJK STROKE HZG", "㇆", "折笔", 2)]
        横折钩 = 220,
        [EnumWord_Stocks("横折折", "横折竖折横", "CJK STROKE HZZ", "㇅", "折笔", 2)]
        横折折 = 221,
        [EnumWord_Stocks("横折提", "横折竖折提", "CJK STROKE HZT", "㇊", "折笔", 2)]
        横折提 = 222,
        [EnumWord_Stocks("横折弯", "横折竖折提", "CJK STROKE HZW", "㇍", "折笔", 2)]
        横折弯 = 223,
        [EnumWord_Stocks("横折弯钩", "", "CJK STROKE HZWG", "㇈", "折笔", 2)]
        横折弯钩 = 224,
        [EnumWord_Stocks("横撇弯钩", "", "CJK STROKE HPWG", "㇌", "折笔", 3)]
        横撇弯钩 = 230,
        [EnumWord_Stocks("横折竖折横折撇", "", "CJK STROKE HZZP", "㇋", "折笔", 3)]
        横折折撇 = 231,
        [EnumWord_Stocks("横折折折", "横折竖折横折竖", "CJK STROKE HZZZ", "㇎", "折笔", 3)]
        横折折折 = 232,
        [EnumWord_Stocks("横折折折钩", "横折竖折横折竖钩", "CJK STROKE HZZZ", "㇡", "折笔", 4)]
        横折折折钩 = 240,

        [EnumWord_Stocks("竖弯", "", "CJK STROKE SW", "㇄", "折笔", 1)]
        竖弯 = 310,
        [EnumWord_Stocks("竖折", "", "CJK STROKE SZ", "㇗", "折笔", 1)]
        竖折 = 311,
        [EnumWord_Stocks("竖提", "", "CJK STROKE ST", "㇙", "折笔", 1)]
        竖提 = 312,
        [EnumWord_Stocks("竖折折", "竖折横折竖", "CJK STROKE SZZ", "㇞", "折笔", 2)]
        竖折折 = 320,
        [EnumWord_Stocks("竖弯钩", "竖弯横钩", "CJK STROKE SWG", "㇟", "折笔", 2)]
        竖弯钩 = 321,
        [EnumWord_Stocks("竖折折钩", "竖折横折竖钩", "CJK STROKE SWG", "㇉", "折笔", 3)]
        竖折折钩 = 330,

        [EnumWord_Stocks("弯钩", "弯竖钩", "CJK STROKE WG", "㇁", "折笔", 1)]
        弯钩 = 410,
        [EnumWord_Stocks("撇点", "", "CJK STROKE PD", "㇛", "折笔", 1)]
        撇点 = 411,
        [EnumWord_Stocks("撇折", "", "CJK STROKE PZ", "㇜", "折笔", 1)]
        撇折 = 412,
        [EnumWord_Stocks("斜钩", "捺钩", "CJK STROKE XG", "㇂", "折笔", 1)]
        斜钩 = 510,
        [EnumWord_Stocks("卧钩", "扁斜钩", "CJK STROKE BXG", "㇃", "折笔", 1)]
        卧钩 = 511
    }


    /// <summary>Enum特性（笔画）
    /// </summary>
    [AttributeUsage(AttributeTargets.Field)]
    public class EnumWord_Stocks : Attribute
    {
        /// <summary>笔画名称
        /// </summary>
        public string Name { get; set; }
        /// <summary>笔画别名
        /// </summary>
        public string NameAlias { get; set; }
        /// <summary>统一码字符名
        /// </summary>
        public string NameStr { get; set; }
        /// <summary>笔画
        /// </summary>
        public string BiHua { get; set; }
        /// <summary>笔形
        /// </summary>
        public string BiXing { get; set; }
        /// <summary>折数
        /// </summary>
        public int ZheShu { get; set; }


        public EnumWord_Stocks(string name, string nameAlias, string nameStr, string biHua, string biXing, int zheShu)
        {
            this.Name = name;
            this.NameAlias = nameAlias;
            this.NameStr = nameStr;
            this.BiHua = biHua;
            this.BiXing = biXing;
            this.ZheShu = zheShu;
        }

    }

}
