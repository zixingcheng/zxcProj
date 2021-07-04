//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：QuoteMonitor_Manager --行情监测管理器
// 创建标识：zxc   2021-07-02
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.Reflection;
using zxcCore.Common;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcData.Cache.Swap;
using zxcCore.zxcRobot.Monitor.Msger;
using zxcCore.zxcRobot.Monitor.DataCheck;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Quote.Data;
using zxcCore.Enums;

namespace zxcCore.zxcRobot.Monitor.Quote
{
    /// <summary>行情监测管理器
    /// </summary>
    public class QuoteMonitor : QuoteMonitor_Manager
    {
        #region 属性及构造

        public QuoteMonitor() : base()
        {
        }
        ~QuoteMonitor()
        {
            // 缓存数据？
        }

        #endregion


        //初始数据交换对象信息
        public override bool InitDataSawp()
        {
            string dirSwap = _configDataCache.config["DataCache.Swap:Monitor_Quote"] + "";
            _swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote_Swap), "", false);
            //_swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 60 * 5, typeof(Data_Quote_Swap), "", true);      //忽略5分钟前数据
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);


            //初始时间频率信息
            this.InitData_TimeFrequency(typeTimeFrequency.real, 60 * 2);            //2分钟数据 120 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m1, 60 * 1);              //1小时数据 120 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m5, 12 * 5);              //5小时数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m15, 4 * 15);             //4天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m30, 2 * 60);             //7.5天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m60, 4 * 15);             //15天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m120, 2 * 30);            //30天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.day, 1 * 60);             //60天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.week, 1 * 60);            //60周数据 60 条
            return true;
        }



        //初始数据检查对象集合-分钟级别
        public override bool InitDataCheck(IDataChecks pDataChecks, typeTimeFrequency timeFrequency)
        {
            //集成基类实现
            if (!base.InitDataCheck(pDataChecks, timeFrequency))
                return false;

            //按时间频率分类设置
            switch (timeFrequency)
            {
                case typeTimeFrequency.none:
                    break;
                case typeTimeFrequency.real:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_RiseFall_Fixed<Data_Quote>));
                    break;
                case typeTimeFrequency.s30:
                    break;
                case typeTimeFrequency.m1:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Risk<Data_Quote>));
                    break;
                case typeTimeFrequency.m5:
                    break;
                case typeTimeFrequency.m10:
                    break;
                case typeTimeFrequency.m15:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Risk_Quantify<Data_Quote>));
                    break;
                case typeTimeFrequency.m30:
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Hourly<Data_Quote>));
                    break;
                case typeTimeFrequency.m60:
                    break;
                case typeTimeFrequency.m120:
                    break;
                case typeTimeFrequency.day:
                    break;
                default:
                    break;
            }
            return true;
        }


        //缓存数据初始装载数据
        public virtual int DataCacheLoad(IDataCache pDataCache, DateTime dtEnd, int nCaches = -1)
        {
            typeTimeFrequency timeFrequency = pDataCache.DataCache_Set.Time_Frequency;
            DataCache<Data_Quote> dataCache = (DataCache<Data_Quote>)pDataCache;
            if (dataCache == null) return 0;
            if (timeFrequency == typeTimeFrequency.real)
            {
                dataCache.InitDatas(null, false, true);
                return 0;
            }

            //校正行情标的
            IDataCache_Set pSet = dataCache.DataCache_Set;
            StockInfo pStockInfo = Quote_Manager._Manager.Stocks.Get_StockInfo(pSet.Info_Factor.ID);
            if (pStockInfo == null) return 0;

            //查询数据
            dtEnd = dtEnd == DateTime.MinValue ? pSet.Time_End : dtEnd;
            nCaches = nCaches < 0 ? pSet.Sum_Step : nCaches;
            List<Data_Quote> lstQuotes = QuoteQuery._Query.Query(pStockInfo.StockID_Tag, dtEnd, nCaches, timeFrequency, true);
            if (lstQuotes.Count == pSet.Sum_Step)
            {
                //重新初始数据
                Dictionary<DateTime, Data_Quote> poData_Quotes = new Dictionary<DateTime, Data_Quote>();
                foreach (var item in lstQuotes)
                {
                    poData_Quotes[item.DateTime] = item;
                }
                return dataCache.InitDatas(poData_Quotes, true, true);
            }
            return 0;
        }


        //缓存数据初始装载事件--载入数据
        public override void EventHandler_DataCacheLoad(object sender, DataCache_Event e)
        {
            //载入缓存数据
            int nNums = this.DataCacheLoad(e.DataCache, DateTime.MinValue);
        }
        //缓存数据变动事件
        public override void EventHandler_DataCacheChange(object sender, DataCache_Event e)
        {
            CacheInfo<Data_Quote> pCacheInfo = (CacheInfo<Data_Quote>)e.CacheInfo;
            if (pCacheInfo.Data.QuoteTimeType == typeTimeFrequency.real)
            {
                if (pCacheInfo.Data.GetStockName() == "50ETF")
                    this.SetData(pCacheInfo.Data, typeTimeFrequency.m15);
            }

        }

    }
}