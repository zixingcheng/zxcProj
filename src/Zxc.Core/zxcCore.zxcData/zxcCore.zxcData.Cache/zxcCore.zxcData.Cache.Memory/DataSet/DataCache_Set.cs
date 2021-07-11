using System;
using System.Collections.Generic;
using System.Linq;
using zxcCore.Common;
using zxcCore.Enums;
using zxcCore.Extensions;

namespace zxcCore.zxcData.Cache.Memory
{
    /// <summary>数据缓存设置对象类
    /// </summary>
    public class DataCache_Set : DataSet, IDataCache_Set
    {
        #region 属性及构造

        string _id = "";
        public string ID
        {
            get { return _id; }
        }

        IData_Factor _Info_Factor = null;
        public IData_Factor Info_Factor
        {
            get { return _Info_Factor; }
        }
        typeTimeFrequency _Time_Frequency = typeTimeFrequency.none;
        public typeTimeFrequency Time_Frequency
        {
            get { return _Time_Frequency; }
        }

        IDataCache_Set _Parent = null;
        public IDataCache_Set Parent
        {
            get { return _Parent; }
        }

        bool _IsInited = false;
        public bool IsInited
        {
            get { return _IsInited; }
        }

        DateTime _dtBase;
        public DateTime Time_Base
        {
            get { return _dtBase; }
        }
        DateTime _dtStart;
        public DateTime Time_Start
        {
            get { return _dtStart; }
        }
        DateTime _dtLast;
        public DateTime Time_Last
        {
            get { return _dtLast; }
        }
        DateTime _dtLast_Base;
        public DateTime Time_LastBase
        {
            get { return _dtLast_Base; }
        }
        DateTime _dtEnd;
        public DateTime Time_End
        {
            get { return _dtEnd; }
        }

        int _dtStep = 60;
        public int Time_Step
        {
            get { return _dtStep; }
        }
        int _sumStep = 0;
        public int Sum_Step
        {
            get { return _sumStep; }
        }
        int _indStep = -1;
        public int Ind_Step
        {
            get { return _indStep; }
        }

        bool _canRefesh = true;
        public bool Can_Refesh
        {
            get { return _canRefesh; }
            set { _canRefesh = value; }
        }


        DateTime _dtDataNow;        //当前数据时间步    
        public DataCache_Set(string tagName, DateTime dtBase, typeTimeFrequency typeTimeFrequency, int cacheNums, IData_Factor infoFactor, IDataCache_Set srcDataCache_Set = null) : base(tagName)
        {
            if (tagName == "") tagName = infoFactor.ID;
            _id = tagName;
            _Info_Factor = infoFactor;
            _tagName = tagName;
            _Time_Frequency = typeTimeFrequency;
            _sumStep = cacheNums;
            _dtStep = (int)_Time_Frequency.Get_Value();
            _dtBase = dtBase;
            _Parent = srcDataCache_Set;
            this.InitTime(dtBase, typeTimeFrequency);
        }
        ~DataCache_Set()
        {
            // 清理数据
        }

        #endregion


        public bool InitTime(DateTime dtBase, typeTimeFrequency typeTimeFrequency)
        {
            _dtEnd = CheckTime(dtBase); ;
            _dtStart = _dtEnd.AddSeconds(-_dtStep * (_sumStep - 1));
            _indStep = this.GetInd(_dtEnd);

            //DateTime dtNow = DateTime.Now.AddDays(-1);
            //_dtLast = new DateTime(dtNow.Year, dtNow.Month, dtNow.Day, 0, 0, 0);
            _dtDataNow = _dtEnd;
            return this.SetLastTime(_dtEnd);
        }
        public bool Inited()
        {
            _IsInited = true;
            return _IsInited;
        }
        public bool SetLastTime(DateTime dtLast)
        {
            if (dtLast > this._dtEnd)
                this._dtEnd = dtLast;
            this._dtLast_Base = dtLast;
            this._dtLast = CheckTime(dtLast);
            return true;
        }


        public List<int> GetInds(DateTime dtStart, DateTime dtEnd)
        {
            int ind_S = this.GetInd(dtStart);
            int ind_E = this.GetInd(dtEnd);

            List<int> inds = new List<int>();
            for (int i = ind_S; i <= ind_E; i++)
            {
                inds.Add(i);
            }
            return inds;
        }
        public int GetInd(DateTime dtData)
        {
            //计算当前时间相对基时间的间隔数()
            TimeSpan delatTime = dtData - this._dtStart;
            int ind = (int)(Math.Floor(delatTime.TotalSeconds / this._dtStep) % this._sumStep);
            return ind;
        }
        public DateTime GetDateTime(int ind)
        {
            DateTime dt = this._dtStart.AddSeconds(ind * this._dtStep);
            return dt;
        }


        public DateTime CheckTime(DateTime dtBase)
        {
            return zxcTimeHelper.CheckTime(dtBase, _Time_Frequency, false);
        }
        public bool IsNewDataTime(DateTime dtTime)
        {
            bool isVaild = false;
            int nSeconds = (int)typeTimeFrequency.day;
            int nDeltas = (int)((dtTime - this._dtDataNow).TotalSeconds);

            //有效性判断
            if (nDeltas > nSeconds)
            {
                isVaild = true;
                _dtDataNow = dtTime;
            }
            return isVaild;
        }


        public string GetTagName(typeTimeFrequency typeTimeFrequency, string strTag = "")
        {
            _tagName = strTag;
            string tag = _Info_Factor.ID + "_" + typeTimeFrequency + (_tagName == "" ? "" : "_" + _tagName);
            return tag;
        }

    }
}
