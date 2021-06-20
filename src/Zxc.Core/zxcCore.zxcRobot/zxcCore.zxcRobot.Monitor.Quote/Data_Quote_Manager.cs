using System;
using System.Collections.Generic;
using zpCore.zpDataCache.Memory;
using zxcCore.zxcDataCache.Swap;
using zxcCore.Common;
using zxcCore.zxcRobot.Monitor.DataCheck;
using System.Reflection;
using zxcCore.zxcRobot.Monitor.Msger;

namespace zxcCore.zxcRobot.Monitor.Quote
{
    /// <summary>数据对象管理类-Quote
    /// </summary>
    public class Data_Quote_Manager
    {
        #region 属性及构造

        protected internal DataSwap_IOFiles _swapIOFiles = null;
        protected internal DataCheck_Msger_Quote _msger = null;
        protected internal DataCaches_Manager _managerCaches = null;
        protected internal Dictionary<string, bool> _dictQuotes = null;
        protected internal zxcConfigurationHelper _configDataCache = new zxcConfigurationHelper("appsettings.json");
        public Data_Quote_Manager()
        {
            _dictQuotes = new Dictionary<string, bool>();
            _msger = new DataCheck_Msger_Quote(true, 1000);
            _managerCaches = new DataCaches_Manager();
            _managerCaches.Init(DateTime.Now);

            string dirSwap = _configDataCache.config["DataCache.Swap:Monitor_Quote"] + "";
            _swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 0, typeof(Data_Quote), "", false);
            //_swapIOFiles = new DataSwap_IOFiles("Quote", dirSwap, 60 * 5, typeof(Data_Quote), "", true);      //忽略5分钟前数据
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);
        }
        ~Data_Quote_Manager()
        {
            // 缓存数据？
        }

        #endregion


        //数据对象监测开始
        public bool Start(int nSteps = -1, int nStepSwaps = 88, int nFrequency = 200)
        {
            return _swapIOFiles.Start(nSteps, nStepSwaps, nFrequency);
        }
        //数据对象监测结束
        public bool Stop()
        {
            return _swapIOFiles.Stop();
        }


        //统一初始数据缓存相关
        public bool InitDataCache(Data_Quote data)
        {
            if (data == null) return false;

            bool bExist = true, bResult = true;
            IData_Factors pFactors = _managerCaches._GetFactors(data._exType);
            if (pFactors == null)
            {
                //提取信息
                pFactors = new Data_Factors(data._exType, data._exType, "", "");
                bExist = false;
            }

            IData_Factor pFactor = pFactors.GetData_Factor(data.idTag);
            if (bExist == false || pFactor == null)
            {
                //提取信息
                pFactor = new Data_Factor(data.idTag, data.idTag, data.name, "");


                //初始数据缓存对象
                _managerCaches.InitDataCache<Data_Quote>(pFactors, pFactor, "", typeTimeFrequency.Second, 30 * 12);
                _managerCaches.InitDataCache<Data_Quote>(pFactors, pFactor, "", typeTimeFrequency.Minute_1, 6 * 60);

                //初始规则信息集合-Caches
                bResult = this.InitDataChecks_Caches(pFactors, pFactor);

                //初始规则信息集合-Cache
                bResult = bResult && this.InitDataChecks_Cache(pFactors, pFactor, data);
                return bResult;
            }
            return false;
        }
        //设置缓存数据对象
        public bool SetDataCache(Data_Quote pData)
        {
            string tag = _getTag(pData);
            if (!_dictQuotes.ContainsKey(tag))
                this.InitDataCache(pData);

            bool bResult = _managerCaches.SetData<Data_Quote>(pData._exType, pData.idTag, "", pData.Time, pData, typeTimeFrequency.Second);
            bResult = bResult && _managerCaches.SetData<Data_Quote>(pData._exType, pData.idTag, "", pData.Time, pData, typeTimeFrequency.Minute_1);
            return bResult;
        }


        //初始规则信息集合-Caches
        public bool InitDataChecks_Caches(IData_Factors pFactors, IData_Factor pFactor)
        {
            IDataCaches dataCaches = _managerCaches.GetDataCaches(pFactors, pFactor);
            IDataChecks poDataChecks_Caches = new DataChecks_Quote(dataCaches.ID, dataCaches);
            bool bResult = dataCaches.InitDataChecks(poDataChecks_Caches);

            return bResult;
        }
        //初始规则信息集合-Cache
        public bool InitDataChecks_Cache(IData_Factors pFactors, IData_Factor pFactor, Data_Quote data)
        {
            IDataCaches dataCaches = _managerCaches.GetDataCaches(pFactors, pFactor);

            //分钟数据
            IDataCache<Data_Quote> poDataCache_M = dataCaches.GetDataCache<Data_Quote>("", typeTimeFrequency.Minute_1);
            IDataChecks poDataChecks_Cache = new DataChecks_Quote(poDataCache_M.ID, poDataCache_M, null, _msger);
            bool bResult = poDataCache_M.InitDataChecks(poDataChecks_Cache);
            bResult = bResult && this.InitDataChecks_M(poDataChecks_Cache);

            //秒数据
            IDataCache<Data_Quote> poDataCache_S = dataCaches.GetDataCache<Data_Quote>("", typeTimeFrequency.Minute_1);
            return bResult;
        }
        //初始数据检查对象集合-分钟级别
        public bool InitDataChecks_M(IDataChecks pDataChecks)
        {
            this.InitDataCheck(pDataChecks, typeof(DataCheck_Print<Data_Quote>));
            this.InitDataCheck(pDataChecks, typeof(DataCheck_Hourly<Data_Quote>));
            this.InitDataCheck(pDataChecks, typeof(DataCheck_RiseFall_Fixed<Data_Quote>));
            this.InitDataCheck(pDataChecks, typeof(DataCheck_Risk<Data_Quote>));
            return true;
        }

        //初始数据检查对象
        public bool InitDataCheck(IDataChecks pDataChecks, Type dest_ClassType)
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
        protected internal dynamic CreateData_CheckObj<T>(Type dest_ClassType, IDataCache<T> dataCache, string setting)
        {
            if (dest_ClassType == null) return null;
            var instance = Activator.CreateInstance(dest_ClassType, new object[] { dest_ClassType.Name, dataCache, setting });
            return instance;
        }


        //交换文件监测变化事件
        private void EventHandler_DataSwapChange(object sender, DataSwap_Event e)
        {
            //ConsoleHelper.Debug(false, DateTime.Now + "::");
            foreach (var item in e.Datas)
            {
                Data_Quote pData = (Data_Quote)item;
                if (pData == null) continue;

                //调试筛选
                //if (pData.name != "50ETF")   //50ETF购3月3500
                //    continue;

                this.SetDataCache(pData);
                //ConsoleHelper.Debug("\t**********" + pData.Time);
            }
        }


        //提取对象标识名
        private string _getTag(Data_Quote pData)
        {
            return pData._exType + "_" + pData.idTag;
        }
    }
}