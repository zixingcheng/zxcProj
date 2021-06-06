using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using zxcCore.zxcDataCache.MemoryDB;

namespace zxcCore.zxcRobot.Msger
{
    /// <summary>数据对象集类-表-消息
    /// </summary>
    public class DataTable_Msg<T> : Data_Table<T> where T : Msg
    {
        #region 属性及构造

        public DataTable_Msg()
        {
            //Data_Test = new Data_Table<Data_TestObj>(); this.InitModel(Data_Test);
            this._dtName = "dataMsg";
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
            return this.FindAll(e => e.msgID == item.msgID && e.IsDel == false);
        }

    }
}