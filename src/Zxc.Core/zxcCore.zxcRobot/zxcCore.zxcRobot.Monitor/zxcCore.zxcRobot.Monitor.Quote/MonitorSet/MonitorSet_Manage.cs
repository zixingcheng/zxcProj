//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：DataMonitor_Set --行情API监测设置(python)
// 创建标识：zxc   2021-06-27
// 修改标识： 
// 修改描述：
//===============================================================================
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcRobot.Quote.Data;

namespace zxcCore.zxcRobot.Monitor.Quote
{
    public class MonitorSet_Manage
    {

        #region 属性及构造

        protected internal string _urlAPI_Set = "";           //行情API接口-设置
        protected internal string _urlAPI_SetQuery = "";      //行情API接口-查询


        public MonitorSet_Manage()
        {
            Stopwatch watch = new Stopwatch();
            watch.Start();


            ////提取行情API配置
            _urlAPI_Set = zxcConfigHelper.ConfigurationHelper.config["ZxcRobot.Quote:QuoteAPI_Monitor:SetAPI_Url"] + "";
            _urlAPI_SetQuery = zxcConfigHelper.ConfigurationHelper.config["ZxcRobot.Quote:QuoteAPI_Monitor:SetQueryAPI_Url"] + "";

            //同步本地配置信息到Python接口
            this.SyncData_MonitorSet();


            watch.Stop();
            zxcConsoleHelper.Print("行情监测设置::同步数据 \n   >> 已同步.  -- {1}, 耗时：{0} 秒.", watch.Elapsed.TotalSeconds, DateTime.Now.ToString());
        }
        ~MonitorSet_Manage()
        {
            // 缓存数据？
        }

        #endregion


        /// <summary>同步本地配置信息--由Python监测接口
        /// </summary>
        /// <param name="setInfo"></param>
        /// <returns></returns>
        public bool SyncData_MonitorSet(string spiderTag = "quote")
        {
            //同步API接口设置数据
            try
            {
                List<MonitorSet> pSets = this.Get_APISets("");
                bool bRes = this.Updata_MonitorSets(pSets);


                //更新本地数据到API接口 
                pSets = Quote_Datas._Datas._setsMoitor.FindAll(e => e.SpiderTag == spiderTag && e.IsDel == false);
                foreach (var item in pSets)
                {
                    bRes = bRes && this.Updata_APISets(item);
                }
                return bRes;
            }
            catch (Exception)
            {
                return false;
                //throw;
            }
        }

        /// <summary>提取本地监测设置信息
        /// </summary>
        /// <param name="spiderName"></param> 
        /// <param name="spiderTag"></param> 
        /// <returns></returns>
        public MonitorSet Get_MonitorSet(string spiderName, string spiderTag = "quote")
        {
            MonitorSet pSet = Quote_Datas._Datas._setsMoitor.Find(e => e.SpiderName == spiderName && e.SpiderTag == spiderTag && e.IsValid == true && e.IsDel == false);
            return pSet;
        }
        /// <summary>提取本地监测设置信息
        /// </summary>
        /// <param name="spiderName"></param>
        /// <param name="isValid"></param>
        /// <param name="spiderTag"></param>
        /// <param name="timeSet"></param>
        /// <param name="mark"></param>
        /// <param name="autoCreate"></param>
        /// <returns></returns>
        public MonitorSet Get_MonitorSet(string spiderName, bool isValid, string mark = "", string spiderTag = "quote", string timeSet = "", bool autoCreate = true)
        {
            MonitorSet pSet = this.Get_MonitorSet(spiderName, spiderTag);

            //自动生成
            if (pSet == null && autoCreate)
                pSet = new MonitorSet
                {
                    SpiderName = spiderName,
                    SpiderTag = spiderTag,
                    Mark = mark,
                    TimeSet = timeSet != "" ? timeSet : "* 9.45-11.5;13-15.1 * * 1-6"
                };
            pSet.IsValid = isValid;
            return pSet;
        }
        /// <summary>提取配置信息集--Python监测接口
        /// </summary>
        /// <param name="spiderName"></param>
        /// <returns></returns>
        public List<MonitorSet> Get_APISets(string spiderName)
        {
            //GET请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Get_ByHttpClient(_urlAPI_SetQuery, spiderName, out statusCode);

            if (statusCode.ToLower() != "ok") return null;
            return this.TransTo_MonitorSet(result);
        }


        /// <summary>更新配置信息--Python监测接口
        /// </summary>
        /// <param name="spiderName"></param>
        /// <param name="isValid"></param>
        /// <param name="mark"></param>
        /// <param name="spiderTag"></param>
        /// <param name="timeSet"></param>
        /// <param name="autoCreate"></param>
        /// <returns></returns>
        public bool Updata_APISets(string spiderName, bool isValid, string mark = "", string spiderTag = "quote", string timeSet = "", bool autoCreate = true)
        {
            MonitorSet pSet = this.Get_MonitorSet(spiderName, isValid, mark, spiderTag, timeSet, autoCreate);
            return this.Updata_APISets(pSet);
        }
        /// <summary>更新配置信息--Python监测接口
        /// </summary>
        /// <param name="setInfo"></param>
        /// <returns></returns>
        public bool Updata_APISets(MonitorSet setInfo)
        {
            if (setInfo == null) return false;

            //GET请求并等待结果
            string statusCode = "";
            var result = zxcNetHelper.Get_ByHttpClient(_urlAPI_Set, setInfo.ToJson_Str(), out statusCode);

            if (statusCode.ToLower() != "ok") return false;
            if (!setInfo.IsValid)
            {
                int ind = Quote_Datas._Datas._setsMoitor.FindIndex(e => e.IsValid == false && e.SpiderName == setInfo.SpiderName);
                Quote_Datas._Datas._setsMoitor.RemoveAt(ind);
                Quote_Datas._Datas._setsMoitor.SaveChanges(true);
                return true;
            }

            List<MonitorSet> pSets = this.TransTo_MonitorSet(result);
            return this.Updata_MonitorSets(pSets);
        }

        /// <summary>更新本地监测设置信息
        /// </summary>
        /// <param name="setsInfo"></param>
        /// <returns></returns>
        protected internal bool Updata_MonitorSets(List<MonitorSet> setsInfo)
        {
            if (setsInfo == null) return false;
            foreach (var item in setsInfo)
            {
                StockInfo pStockInfo = Quote_Datas._Datas.Get_StockInfo(item.SpiderName);
                if (pStockInfo != null)
                    Quote_Datas._Datas._setsMoitor.Add(item);
            }
            return true;
        }


        /// <summary>将行情数据转换为Json
        /// </summary>
        /// <param name="strData"></param>
        /// <param name="barUnit">bar的时间单位</param>
        /// <returns></returns>
        protected internal List<MonitorSet> TransTo_MonitorSet(string strData)
        {
            JObject pRes = JObject.Parse(strData);
            JArray jsonDatas = (JArray)pRes["datas"];
            if (jsonDatas == null) return null;

            List<MonitorSet> pSets = new List<MonitorSet>();
            foreach (var item in jsonDatas)
            {
                MonitorSet pSet = new MonitorSet();
                if (pSet.FromJson(item))
                {
                    pSets.Add(pSet);
                }
            }
            return pSets;
        }

    }
}
