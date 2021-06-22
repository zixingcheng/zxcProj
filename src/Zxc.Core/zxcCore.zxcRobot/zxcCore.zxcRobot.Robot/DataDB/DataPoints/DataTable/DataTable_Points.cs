using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.zxcDataCache.MemoryDB;
using zxcCore.zxcRobot.User;

namespace zxcCore.zxcRobot.Robot.Power
{
    /// <summary>数据对象集类-积分表
    /// </summary>
    public class DataTable_Points<T> : Data_Table<T> where T : Data_Points
    {
        #region 属性及构造

        /// <summary>库表--积分记录表
        /// </summary>
        protected internal DataTable_PointsLog<Data_PointsLog> _logPoints { get; set; }
        protected internal string _pointsType = "base";
        protected internal bool _bInited = false;


        public DataTable_Points(string dtName = "dataTable_Points") : base(dtName)
        {
            //this._dtName = string.IsNullOrEmpty(_dtName) ? "dataTable_Points" : _dtName;
            this.Init_PointsLog();
        }

        #endregion


        /// <summary>对象是否存在
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override bool IsExist(T item)
        {
            return this.Contains(item) || this.IsSame(item);
        }
        /// <summary>查询相同对象-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public override List<T> Query_Sames(T item)
        {
            return this.FindAll(e => (e.UID == item.UID && e.IsDel == false) || (e.PointsType == item.PointsType && e.PointsUser == item.PointsUser && e.IsDel == false));
        }


        /// <summary>初始相关表--积分记录表
        /// </summary>
        /// <returns></returns>
        public virtual bool Init_PointsLog(string dtLogName = "dataTable_PointsLog")
        {
            //初始积分记录表
            if (_bInited) return true;
            if (_logPoints == null)
                _logPoints = new DataTable_PointsLog<Data_PointsLog>(dtLogName);
            if (this._dbContext != null)
            {
                this._dbContext.InitDBModel(_logPoints);
                _bInited = true;
            }
            return true;
        }

        /// <summary>添加成长宝贝点
        /// </summary>
        /// <param name="pGrowthPoints"></param>
        /// <returns></returns>
        public virtual Data_PointsLog Add_Points(CmdInfos_PointsGrowth pGrowthPoints, string opUser = "", bool checkPoints = true)
        {
            //查找用户信息
            Data_Points pDataPoints = this.Find(e => e.PointsType == _pointsType && e.PointsUser == pGrowthPoints.NoteUserTag && e.IsDel == false);
            if (pDataPoints == null)
            {
                //初始
                pDataPoints = new Data_Points()
                {
                    PointsNum = 0,
                    PointExChange = 0,
                    PointsUser = pGrowthPoints.NoteUserTag,
                    PointsType = _pointsType,
                    IsValid = true,
                    RelID = "",
                    Remark = ""
                };
            }

            //添加积分记录
            Data_PointsLog pDataPointsLog = new Data_PointsLog()
            {
                PointExChange = pGrowthPoints.PointsNum,
                PointsLast = pDataPoints.PointsNum,
                PointsNow = pDataPoints.PointsNum + pGrowthPoints.PointsNum,
                PointsUser = pGrowthPoints.NoteUserTag,
                PointsType = _pointsType,
                PointsNote = pGrowthPoints.NoteInfo,
                PointsNote_Label = pGrowthPoints.NoteLabel,
                PointsUser_OP = opUser,
                RelID = pDataPoints.RelID,
                IsValid = true,
                Remark = pGrowthPoints.Remark
            };

            //数据校正
            if (checkPoints && pDataPointsLog.PointsNow < 0)
            {
                pDataPointsLog.PointsNow = pDataPoints.PointsNum;
                pDataPointsLog.IsValid = false;
                return pDataPointsLog;
            }
            this._logPoints.Add(pDataPointsLog, true, true);

            //更新记录积分信息 
            pDataPoints.RelID = pDataPointsLog.UID;
            pDataPoints.PointsNum = pDataPointsLog.PointsNow;
            pDataPoints.PointExChange = pDataPointsLog.PointExChange;
            this.Add((T)pDataPoints, true, true);
            return pDataPointsLog;
        }
    }

}
