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
using zxcCore.zxcData.Cache.Memory;
using zxcCore.zxcData.Cache.Swap;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.DataCheck;
using System.Reflection;
using zxcCore.zxcRobot.Monitor.Msger;
using zxcCore.Enums;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.Quote
{
    /// <summary>行情监测管理器
    /// </summary>
    public class QuoteMonitor_Manager
    {
        #region 属性及构造

        /// <summary>监测设置管理对象
        /// </summary>
        public MonitorSet_Manage _MonitorSets = new MonitorSet_Manage();

        protected internal DateTime _timeDataLast;
        protected internal DataSwap_IOFiles _swapIOFiles = null;
        protected internal DataCheck_Msger_Quote _msger = null;
        protected internal DataCaches_Manager _managerCaches = null;
        protected internal Dictionary<string, bool> _dictQuotes = null;
        protected internal Dictionary<typeTimeFrequency, int> _setsDataCache = null;
        protected internal zxcConfigurationHelper _configDataCache = new zxcConfigurationHelper("appsettings.json");

        public QuoteMonitor_Manager()
        {
            _setsDataCache = new Dictionary<typeTimeFrequency, int>();
            _dictQuotes = new Dictionary<string, bool>();
            _msger = new DataCheck_Msger_Quote(true, 1000);
            _managerCaches = new DataCaches_Manager();
            _managerCaches.Init(DateTime.Now);

            this.InitDataSawp();        //初始数据交换对象信息

            //事件注册
            _managerCaches.DataCache_Load += new DataCacheLoad_EventHandler(EventHandler_DataCacheLoad);
            _managerCaches.DataCacheChecks_Initial += new DataCacheChecksInitial_EventHandler(EventHandler_DataCacheChecksInitial);
            _managerCaches.DataCache_Change += new DataCacheChange_EventHandler(EventHandler_DataCacheChange);
            _managerCaches.DataCachesChecks_Initial += new DataCachesChecksInitial_EventHandler(EventHandler_DataCachesChecksInitial);
            _managerCaches.DataCachesManageChecks_Initial += new DataCachesManageChecksInitial_EventHandler(EventHandler_DataCachesManageChecksInitial);
        }
        ~QuoteMonitor_Manager()
        {
            // 缓存数据？
        }

        #endregion


        //初始数据交换对象信息
        public virtual bool InitDataSawp()
        {
            string dirSwap = _configDataCache.config["DataCache.Swap:Monitor_Quote"] + "";
            _swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote_Swap), "", false);
            //_swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 60 * 5, typeof(Data_Quote), "", true);      //忽略5分钟前数据
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);

            //初始时间频率信息
            this.InitData_TimeFrequency(typeTimeFrequency.real, 30 * 12);
            this.InitData_TimeFrequency(typeTimeFrequency.m1, 6 * 60);
            return true;
        }
        //初始时间频率信息
        public virtual bool InitData_TimeFrequency(typeTimeFrequency timeFrequency, int nNums)
        {
            _setsDataCache[timeFrequency] = nNums;
            return true;
        }
        //数据对象监测开始
        public virtual bool Start(int nSteps = -1, int nStepSwaps = 88, int nFrequency = 200)
        {
            return _swapIOFiles.Start(nSteps, nStepSwaps, nFrequency);
        }
        //数据对象监测结束
        public virtual bool Stop()
        {
            return _swapIOFiles.Stop();
        }


        //统一初始数据缓存相关
        public virtual bool InitDataCache(Data_Quote pData)
        {
            if (pData == null) return false;
            StockInfo stockInfo = pData.GetStockInfo();
            if (stockInfo == null) return false;

            string exType = stockInfo.StockExchange.ToString();
            bool bExist = true, bResult = true;
            IData_Factors pFactors = _managerCaches._GetFactors(exType);
            if (pFactors == null)
            {
                //提取信息
                pFactors = new Data_Factors(exType, exType, "", "");
                bExist = false;
            }

            IData_Factor pFactor = pFactors.GetData_Factor(stockInfo.StockID_Tag);
            if (bExist == false || pFactor == null)
            {
                //提取信息
                pFactor = new Data_Factor(stockInfo.StockID_Tag, stockInfo.StockID_Tag, stockInfo.StockName, "");

                //初始数据所有缓存对象
                foreach (var item in _setsDataCache)
                {
                    //提取数据缓存对象、及检查对象集
                    IDataCache<Data_Quote> poDataCache = _managerCaches.GetDataCache<Data_Quote>(pFactors, pFactor, "", item.Key, true, item.Value);

                    //IDataCache poDataCache = null;
                    //if (item.Key == typeTimeFrequency.real)
                    //    poDataCache = _managerCaches.GetDataCache<Data_Quote>(pFactors, pFactor, "", item.Key, true, item.Value);
                    //else
                    //    poDataCache = _managerCaches.GetDataCache<Data_Quote>(pFactors, pFactor, "", item.Key, true, item.Value);
                    //_managerCaches.InitDataCache<Data_Quote_Swap>(pFactors, pFactor, "", item.Key, item.Value);
                }

                //初始规则信息集合-Caches
                //bResult = this.InitDataChecks_Caches(pFactors, pFactor);

                //初始规则信息集合-Cache
                //bResult = bResult && this.InitDataChecks_Cache(pFactors, pFactor, data);
                _dictQuotes[_getTag(pData)] = true;
                return bResult;
            }
            return false;
        }
        //设置缓存数据对象
        public virtual bool SetDataCache(Data_Quote pData)
        {
            bool bInited = false;
            string tag = _getTag(pData);
            _dictQuotes.TryGetValue(tag, out bInited);
            if (!bInited)
                this.InitDataCache(pData);
            return this.SetData(pData, pData.QuoteTimeType);
        }
        //设置缓存数据对象
        public virtual bool SetData(Data_Quote pData, typeTimeFrequency timeFrequency)
        {
            StockInfo stockInfo = pData.GetStockInfo();
            if (stockInfo == null) return false;
            Type p = typeof(Data_Quote);

            //默认只设置最底级数据，
            bool bResult = true;
            string exType = stockInfo.StockExchange.ToString();

            Data_Quote dataCheck = this.SetData_ValueCheck(pData, timeFrequency);
            if (dataCheck != null)
            {
                bResult = bResult && _managerCaches.SetData<Data_Quote>(exType, stockInfo.StockID_Tag, "", dataCheck.DateTime, dataCheck, timeFrequency);
            }

            //foreach (var item in _setsDataCache)
            //{
            //    Data_Quote dataCheck = this.SetDataCache_ValueCheck(pData, item.Key);
            //    if (dataCheck != null)
            //    {
            //        bResult = bResult && _managerCaches.SetData<Data_Quote>(exType, stockInfo.StockID_Tag, "", dataCheck.DateTime, dataCheck, item.Key);
            //    }
            //}
            return bResult;
        }
        //设置缓存数据对象-修正
        public virtual Data_Quote SetData_ValueCheck(Data_Quote pData, typeTimeFrequency timeFrequency)
        {
            pData.QuoteTimeType = timeFrequency;
            return pData;
        }



        //初始规则信息集合-Caches-弃用
        private bool InitDataChecks_Caches(IData_Factors pFactors, IData_Factor pFactor)
        {
            IDataCaches dataCaches = _managerCaches.GetDataCaches(pFactors, pFactor);
            IDataChecks poDataChecks_Caches = new DataChecks_Quote(dataCaches.ID, dataCaches);
            bool bResult = dataCaches.InitDataChecks(poDataChecks_Caches);

            return bResult;
        }
        //初始规则信息集合-Cache-弃用
        private bool InitDataChecks_Cache(IData_Factors pFactors, IData_Factor pFactor, Data_Quote data)
        {
            //数据缓存集检查
            IDataCaches dataCaches = _managerCaches.GetDataCaches(pFactors, pFactor);
            if (dataCaches == null)
                return false;

            //初始检查集
            bool bResult = this.InitDataChecks_CheckAll(dataCaches);
            return bResult;
        }
        //初始规则信息集合-全部-弃用
        private bool InitDataChecks_CheckAll(IDataCaches dataCaches)
        {
            bool bResult = true;
            foreach (var item in _setsDataCache)
            {
                bResult = bResult && this.InitDataChecks_Check(dataCaches, item.Key);
            }
            return bResult;
        }
        //初始规则信息集合-指定时间级别-弃用
        private bool InitDataChecks_Check(IDataCaches dataCaches, typeTimeFrequency timeFrequency)
        {
            //数据缓存集检查
            if (dataCaches == null) return false;

            //提取数据缓存对象、及检查对象集
            IDataCache<Data_Quote> poDataCache = dataCaches.GetDataCache<Data_Quote>("", timeFrequency);
            IDataChecks poDataChecks_Cache = new DataChecks_Quote(poDataCache.ID, poDataCache, null, _msger);

            //初始检查集
            bool bResult = poDataCache.InitDataChecks(poDataChecks_Cache);
            bResult = bResult && this.InitDataCheck(poDataChecks_Cache, timeFrequency);
            return bResult;
        }



        //初始数据检查对象集合-分钟级别
        public virtual bool InitDataCheck(IDataChecks pDataChecks, typeTimeFrequency timeFrequency)
        {
            switch (timeFrequency)
            {
                case typeTimeFrequency.none:
                    break;
                case typeTimeFrequency.real:
                    this.InitDataCheck_Instance(pDataChecks, typeof(DataCheck_Print<Data_Quote>));
                    break;
                case typeTimeFrequency.s30:
                    break;
                case typeTimeFrequency.m1:
                    break;
                case typeTimeFrequency.m5:
                    break;
                case typeTimeFrequency.m10:
                    break;
                case typeTimeFrequency.m15:
                    break;
                case typeTimeFrequency.m30:
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
        //初始数据检查对象
        public virtual bool InitDataCheck_Instance(IDataChecks pDataChecks, Type dest_ClassType)
        {
            if (pDataChecks == null) return false;

            string setting = "";
            var instance = this.CreateData_CheckObj<Data_Quote>(dest_ClassType, null, setting);
            DataCheck_Quote<Data_Quote> pDataCheck = (DataCheck_Quote<Data_Quote>)instance;
            if (pDataCheck != null)
            {
                pDataChecks.InitDataCheck<Data_Quote>(pDataCheck.Tag, pDataCheck, true);
            }
            return true;
        }
        //创建对象-泛型实现
        protected internal virtual dynamic CreateData_CheckObj<T>(Type dest_ClassType, IDataCache<T> dataCache, string setting)
        {
            if (dest_ClassType == null) return null;
            var instance = Activator.CreateInstance(dest_ClassType, new object[] { dest_ClassType.Name, dataCache, setting });
            return instance;
        }


        //交换文件监测变化事件
        protected internal virtual void EventHandler_DataSwapChange(object sender, DataSwap_Event e)
        {
            //ConsoleHelper.Debug(false, DateTime.Now + "::");
            foreach (var item in e.Datas)
            {
                if (item == null) continue;
                this.SetDataCache(item);

                //调试筛选
                //if (pData.name != "50ETF")   //50ETF购3月3500
                //    continue;
                //ConsoleHelper.Debug("\t**********" + pData.Time);
            }
        }

        //缓存数据初始装载事件
        public virtual void EventHandler_DataCacheLoad(object sender, DataCache_Event e)
        {

        }
        //缓存数据检查对象初始事件
        public virtual void EventHandler_DataCacheChecksInitial(object sender, DataCache_Event e)
        {
            //提取数据缓存对象、及检查对象集
            IDataCache poDataCache = e.DataCache;
            if (poDataCache != null)
            {
                IDataChecks poDataChecks_Cache = poDataCache.DataChecks;
                if (poDataChecks_Cache == null)
                    poDataChecks_Cache = new DataChecks_Quote(poDataCache.ID, poDataCache, null, _msger);

                //初始检查集
                bool bResult = poDataCache.InitDataChecks(poDataChecks_Cache);
                bResult = bResult && this.InitDataCheck(poDataChecks_Cache, poDataCache.DataCache_Set.Time_Frequency);
            }
        }
        //缓存数据变动事件
        public virtual void EventHandler_DataCacheChange(object sender, DataCache_Event e)
        {

        }
        //缓存数据集检查对象初始事件
        public virtual void EventHandler_DataCachesChecksInitial(object sender, DataCaches_Event e)
        {
            DataCaches dataCaches = e.DataCaches;
            if (dataCaches != null)
            {
                IDataChecks poDataChecks_Caches = dataCaches.DataChecks;
                if (poDataChecks_Caches == null)
                    poDataChecks_Caches = new DataChecks_Quote(dataCaches.ID, dataCaches);

                //初始检查集--未具体初始检查对象
                bool bResult = dataCaches.InitDataChecks(poDataChecks_Caches);
            }
        }
        //缓存数据集管理对象检查对象初始事件
        public virtual void EventHandler_DataCachesManageChecksInitial(object sender, DataCachesManage_Event e)
        {
            //忽略
        }


        //提取对象标识名
        protected internal virtual string _getTag(Data_Quote pData)
        {
            StockInfo pStockInfo = pData.GetStockInfo();
            return pStockInfo.StockExchange.ToString() + "_" + pStockInfo.StockID_Tag;
        }

    }
}