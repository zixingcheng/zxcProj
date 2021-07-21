//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcEnum --时间设置类
// 创建标识：zxc   2021-07-21
// 修改标识： 
// 修改描述：
//===============================================================================
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using zxcCore.Extensions;

namespace zxcCore.Common.TimeSet
{
    /// <summary>时间设置类型
    /// </summary>
    public enum typeTimeSet
    {
        /// <summary>秒
        /// </summary>
        [EnumAttr("秒", 0), EnumValue(59)]
        S = 0,
        /// <summary>分
        /// </summary>
        [EnumAttr("分", 0), EnumValue(59)]
        M = 1,
        /// <summary>时
        /// </summary>
        [EnumAttr("时", 0), EnumValue(23)]
        H = 2,
        /// <summary>天
        /// </summary>
        [EnumAttr("天", 1), EnumValue(31)]
        D = 3,
        /// <summary>月
        /// </summary>
        [EnumAttr("月", 1), EnumValue(12)]
        m = 4,
        /// <summary>周
        /// </summary>
        [EnumAttr("周", 0), EnumValue(6)]
        w = 5
    }


    //时间设置
    public class zxcTimeSet
    {
        #region 属性及构造

        /// <summary>最大时间
        /// </summary>
        protected internal double _TimeMax = 0;
        public double TimeMax { get { return _TimeMax; } }
        /// <summary>最小时间
        /// </summary>
        protected internal double _TimeMin = 0;
        public double TimeMin { get { return _TimeMin; } }

        /// <summary>时间设置类型
        /// </summary>
        protected internal typeTimeSet _TypeTimeSet = 0;
        public typeTimeSet TypeTimeSet { get { return _TypeTimeSet; } }

        /// <summary>是否全部时间有效
        /// </summary>
        protected internal bool _IsVaildAll = false;
        public bool IsVaildAll { get { return _IsVaildAll; } }


        protected internal string _strSet = "";
        protected internal double _dMin = double.MinValue;
        protected internal double _dMax = double.MaxValue;
        protected internal List<double> _Values = null;
        protected internal List<zxcTimeSet> _Sets = null;
        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="dueTime">到期执行时间</param>
        /// <param name="periodTime">间隔时间</param>
        /// <param name="jobExcutor">任务执行者</param>
        public zxcTimeSet(string strSet = "*", typeTimeSet typeTime = typeTimeSet.M)
        {
            _strSet = strSet;
            _TypeTimeSet = typeTime;
            _dMin = (int)typeTime.Get_AttrValue();
            _dMax = (int)typeTime.Get_Value();

            _Values = new List<double>();
            this.Init(strSet);
        }

        #endregion


        //初始时间设置
        public virtual bool Init(string strSet)
        {
            if (string.IsNullOrEmpty(strSet) || strSet == "*")
            {
                this._IsVaildAll = true; return true;
            }

            string[] strSets = strSet.Split(",");
            if (strSets.Length > 1)
            {
                //多个配置
                this._Sets = new List<zxcTimeSet>();
                foreach (var item in strSets)
                {
                    zxcTimeSet pSet = new zxcTimeSet(item, this._TypeTimeSet);
                    this._Sets.Add(pSet);
                }
            }
            else
            {
                //区间配置
                if (strSet.IndexOf("-") > 0)
                {
                    string[] strTemps = strSet.Split("-");
                    double dMin = Convert.ToDouble(strTemps[0]);
                    double dMax = Convert.ToDouble(strTemps[1]);
                    if (_dMin <= dMin && dMax <= _dMax)
                    {
                        this._TimeMin = Convert.ToDouble(strTemps[0]);
                        this._TimeMax = Convert.ToDouble(strTemps[1]);
                    }
                }
                else
                {
                    if (strSet.IndexOf(".") > 0)
                        _Values.Add(Convert.ToDouble(strSet));
                    else
                        _Values.Add(Convert.ToInt32(strSet));
                }
            }
            return true;
        }

        //是否有效
        public virtual bool IsValid(double value)
        {
            if (this._IsVaildAll) return true;
            if (this.TimeMax > 0 && this.TimeMin > 0)
                return this.TimeMin <= value && this.TimeMax > value;
            if (this._Sets.Count > 0)
            {
                foreach (var item in this._Sets)
                {
                    if (item.IsValid(value))
                        return true;
                }
            }
            return this._Values.Contains(value);
        }

    }

    //时间设置
    //M: 分（0-59） H：时（0-23） D：天（1-31） m: 月（1-12） w: 周（0-6） 0为星期日(或用Sun或Mon简写来表示) 
    //* 9-11;13-15 * * 1-6   时间设置为每周一到周五的9-11点和13-15点
    public class zxcTimeSets
    {
        #region 属性及构造

        /// <summary>标签名称
        /// </summary>
        protected internal string _TagName = "";
        public string TagName { get { return _TagName; } }


        protected internal string _strSet = "";
        protected internal Dictionary<typeTimeSet, zxcTimeSet> _Sets = null;
        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="dueTime">到期执行时间</param>
        /// <param name="periodTime">间隔时间</param>
        /// <param name="jobExcutor">任务执行者</param>
        public zxcTimeSets(string strSet, string strTag = "")
        {
            _TagName = strTag;
            _Sets = new Dictionary<typeTimeSet, zxcTimeSet>();
            this.Init(strSet);
        }

        #endregion


        //初始时间设置
        public virtual bool Init(string strSet)
        {
            string[] temps = strSet.Replace(";", ",").Split(' ');
            if (temps.Length > 5)
            {
                _Sets[typeTimeSet.S] = new zxcTimeSet(temps[0], typeTimeSet.S);
                _Sets[typeTimeSet.M] = new zxcTimeSet(temps[1], typeTimeSet.M);
                _Sets[typeTimeSet.H] = new zxcTimeSet(temps[2], typeTimeSet.H);
                _Sets[typeTimeSet.D] = new zxcTimeSet(temps[3], typeTimeSet.D);
                _Sets[typeTimeSet.m] = new zxcTimeSet(temps[4], typeTimeSet.m);
                _Sets[typeTimeSet.w] = new zxcTimeSet(temps[5], typeTimeSet.w);
                return true;
            }
            return false;
        }

        //是否有效
        public virtual bool IsValid(DateTime dtTime)
        {
            if (dtTime == DateTime.MinValue)
                dtTime = DateTime.Now;
            return _Sets[typeTimeSet.S].IsValid(dtTime.Second)
                && (_Sets[typeTimeSet.M].IsValid(dtTime.Minute) || _Sets[typeTimeSet.M].IsValid(dtTime.Minute + dtTime.Second / 60))
                && (_Sets[typeTimeSet.H].IsValid(dtTime.Hour) || _Sets[typeTimeSet.H].IsValid(dtTime.Hour + dtTime.Minute / 60 + dtTime.Second / 3600))
                && _Sets[typeTimeSet.D].IsValid(dtTime.Day)
                && _Sets[typeTimeSet.m].IsValid(dtTime.Month)
                && _Sets[typeTimeSet.w].IsValid((int)dtTime.DayOfWeek);
        }

    }

}