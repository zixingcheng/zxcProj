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
using System.Linq;
using System.Collections.Generic;
using zxcCore.Common;
using zxcCore.Enums;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcData.Cache.Swap;
using zxcCore.zxcRobot.Monitor.DataCheck;
using zxcCore.zxcRobot.Quote;
using zxcCore.zxcRobot.Quote.Data;

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
            this.InitData_TimeFrequency(typeTimeFrequency.real, 60 * 2);            //秒级，2分钟数据 120 条
            //this.InitData_TimeFrequency(typeTimeFrequency.m1, 60 * 1);              //分钟级，1小时数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m5, 12 * 5);              //5分钟级，5小时数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m15, 4 * 15);             //15分钟级，4天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m30, 2 * 60);             //30分钟级，7.5天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m60, 4 * 15);             //60分钟级，15天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.m120, 2 * 30);            //120分钟级，30天数据 60 条
            this.InitData_TimeFrequency(typeTimeFrequency.day, 1 * 60);             //日级，60天数据 60 条
            //this.InitData_TimeFrequency(typeTimeFrequency.week, 1 * 30);            //周级，30周数据 30 条
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
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Risk<Data_Quote>));
                    this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Hourly<Data_Quote>));
                    break;
                case typeTimeFrequency.s30:
                    break;
                case typeTimeFrequency.m1:
                    break;
                case typeTimeFrequency.m10:
                    break;
                case typeTimeFrequency.m5:
                case typeTimeFrequency.m15:
                case typeTimeFrequency.m30:
                case typeTimeFrequency.m60:
                case typeTimeFrequency.m120:
                case typeTimeFrequency.day:
                    if (pDataChecks.DataCache.DataCache_Set.Info_Factor.Name == "50ETF")
                    {
                        this.InitDataCheck_Instance(pDataChecks, typeof(QuoteCheck_Risk_Quantify<Data_Quote>));
                    }
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
            if (pDataCache.DataCache_Set.Info_Factor.Name != "50ETF")
            {
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
                {
                    this.SetData(pCacheInfo, typeTimeFrequency.m5, typeTimeFrequency.m5);
                    this.SetData(pCacheInfo, typeTimeFrequency.m15, typeTimeFrequency.m5);
                    this.SetData(pCacheInfo, typeTimeFrequency.m30, typeTimeFrequency.m5);
                    this.SetData(pCacheInfo, typeTimeFrequency.m60, typeTimeFrequency.m5);
                    this.SetData(pCacheInfo, typeTimeFrequency.m120, typeTimeFrequency.m5);
                    this.SetData(pCacheInfo, typeTimeFrequency.day, typeTimeFrequency.m5);
                    //this.SetData(pCacheInfo, typeTimeFrequency.week, typeTimeFrequency.m5);
                }
            }
        }

        //设置正数据对象-修正为同时间频率数据
        public virtual bool SetData(CacheInfo<Data_Quote> pCacheInfo, typeTimeFrequency timeFrequency, typeTimeFrequency timeFrequency2)
        {
            Data_Quote pData = pCacheInfo.Data;
            if (pData == null) return false;
            StockInfo pStockInfo = pData.GetStockInfo();
            if (pStockInfo == null) return false;

            //获取当前时间频率数据
            DateTime dtEnd = zxcTimeHelper.CheckTime(pData.DateTime, typeTimeFrequency.m1, true);
            Data_Quote pDataNew = QuoteQuery._Query.Query(pStockInfo, pData.DateTime, timeFrequency, null);
            if (pDataNew == null)
                return false;
            bool bResult = this.SetData(pDataNew, timeFrequency);
            return bResult;


            //非时间频率数据，重新修正
            if (pData.QuoteTimeType != timeFrequency)
            {
                string exType = pStockInfo.StockExchange.ToString();
                IData_Factors pFactors = _managerCaches._GetFactors(exType);
                if (pFactors != null)
                {
                    IData_Factor pFactor = pFactors.GetData_Factor(pStockInfo.StockID_Tag);
                    DataCache<Data_Quote> pDataCache = (DataCache<Data_Quote>)_managerCaches.GetDataCache<Data_Quote>(pFactors, pFactor, "", timeFrequency);

                    //查询最后有效步长数据总数
                    int nCount = pDataCache.DataCaches.Values.Count(e => e.Data.IsDel == true);

                    //获取最数据
                    List<Data_Quote> lstQuotes = QuoteQuery._Query.Query(pStockInfo.StockID_Tag, pDataNew.DateTime, nCount, timeFrequency, true);
                    if (lstQuotes != null)
                    {
                        foreach (var item in lstQuotes)
                        {
                            int nSum = pDataCache.DataCaches.Values.Count(e => e.DateTime == item.DateTime && e.Data.IsDel != true);
                            if (nSum == 0)
                            {
                                item.SetStockInfo(pStockInfo);
                                bResult = bResult && this.SetData(item, timeFrequency);
                            }
                        }
                    }
                }
            }
            return bResult;
        }

    }
}