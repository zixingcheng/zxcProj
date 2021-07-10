using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据因子类
    /// </summary>
    public class Data_Factor : IData_Factor
    {
        string _id;
        public string ID
        {
            get { return _id; }
            set { _id = value; }
        }
        string _code;
        public string Code
        {
            get { return _code; }
            set { _code = value; }
        }
        string _name;
        public string Name
        {
            get { return _name; }
            set { _name = value; }
        }
        string _standard;
        public string Standard
        {
            get { return _standard; }
            set { _standard = value; }
        }
        public DateTime DateTime
        {
            get; set;
        }


        public Data_Factor(string id, string code, string name, string standard)
        {
            _id = id;
            _code = code;
            _name = name;
            _standard = standard;
        }
    }
}
