using System;
using System.Collections.Generic;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据因子集类
    /// </summary>
    public class Data_Factors : IData_Factors
    {
        #region 属性及构造

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

        Dictionary<string, IData_Factor> _factors = null;
        public Dictionary<string, IData_Factor> Factors
        {
            get { return _factors; }
            set { _factors = value; }
        }


        public Data_Factors(string id, string code, string name, string standard)
        {
            _id = id;
            _code = code;
            _name = name;
            _standard = standard;
            _factors = new Dictionary<string, IData_Factor>();
        }
        ~Data_Factors()
        {
            // 缓存数据？

            // 清理数据
            this._factors.Clear();
        }

        #endregion


        /// <summary>索引因子集对象（便于用标识查找因子集）
        /// </summary>
        /// <param name="infoFactors">因子对象集</param>
        /// <param name="infoFactor">因子对象</param>
        /// <returns></returns>
        public bool IndexData_Factor(IData_Factor infoFactor)
        {
            if (infoFactor == null) return false;
            if (this.GetData_Factor(infoFactor.ID) == null)
                _factors.Add(infoFactor.ID, infoFactor);
            return true;
        }
        /// <summary>提取指定标识的因子集对象
        /// </summary>
        /// <param name="strTag"></param>
        /// <returns></returns>
        public IData_Factor GetData_Factor(string strTag)
        {
            if (strTag + "" == "") return null;

            IData_Factor pFactor = null;
            if (_factors.TryGetValue(strTag, out pFactor))
            {
            }
            return pFactor;
        }
    }
}
