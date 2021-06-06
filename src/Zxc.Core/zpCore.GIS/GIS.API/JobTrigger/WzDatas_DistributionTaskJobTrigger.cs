using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using zpCore.Common.JobTrigger;
using zpCore.zpDataCache.Swap;
using zpCore.Common;
using zpCore.GIS.API.Common;
using zpCore.GIS.Models.Service;
using System.Globalization;
using System.Text;

namespace zpCore.GIS.API.Models.JobTrigger
{
    public class WzDatas_DistributionTaskJobTrigger : BaseJobTrigger
    {
        private static WzDatas_DistributionTaskJobExcutor ms_WzDatasJob = new WzDatas_DistributionTaskJobExcutor();
        public WzDatas_DistributionTaskJobTrigger() :
            base(TimeSpan.FromSeconds(20),
                TimeSpan.FromMinutes(30),
                ms_WzDatasJob)
        {
        }
    }

    public class WzDatas_DistributionTaskJobExcutor
                     : IJobExecutor
    {
        protected internal DataSwap_IOFiles _swapIOFiles = null;
        protected internal ConfigurationHelper _configDataCache = new ConfigurationHelper("appsettings.json");
        protected internal string _nameUsr = "", _pathMsg = "";

        public WzDatas_DistributionTaskJobExcutor()
        {
            string dirSwap = _configDataCache.config["DataCache.Swap:WzData.Swaps"] + "";
            _nameUsr = _configDataCache.config["Msgerset:Msger_Wx:usrName"] + "";
            _pathMsg = _configDataCache.config["Msgerset:Msger_Wx:pathMsg"] + "";
            _swapIOFiles = new DataSwap_IOFiles("dataWZ", dirSwap, 0, null);
            _swapIOFiles.SwapData_Change += new DataSwapChange_EventHandler(EventHandler_DataSwapChange);
        }
        ~WzDatas_DistributionTaskJobExcutor()
        {
            // 缓存数据？
        }

        public void StartJob()
        {
            Console.WriteLine("Do DatasTaskJob::");
            if (!_swapIOFiles.Is_Running)
                _swapIOFiles.Start(-1, 1, 1000 * 30);
            Console.WriteLine("Done DatasTaskJob.");
        }

        public void StopJob()
        {
            //LogUtil.Info("系统终止任务");
        }

        //交换文件事件
        private void EventHandler_DataSwapChange(object sender, DataSwap_EventArgs e)
        {
            Console.WriteLine(DateTime.Now + "::");
            foreach (dynamic item in e.Datas)
            {
                JObject pData = JObject.FromObject(item);
                if (pData == null) continue;

                if (this.DoDistributions(pData))
                    _swapIOFiles.ackDataSwap(pData);
            }
        }

        //微站数据分布图
        private bool DoDistributions(JObject data)
        {
            bool bResult = true;
            List<string> lstAttrName = new List<string>() { "Aqi", "Pm10", "Pm25", "O3", "O38h", "Voc", "So2", "No2", "Co" };

            string[] temps = data["tagAck"].ToString().Split("_");
            var path = data["filePath"].ToString();
            var dtFile = DateTime.ParseExact(temps[2].Replace(".geojson", ""), "yyyy-MM-dd-HH-mm-ss", System.Globalization.CultureInfo.InvariantCulture);
            var strTime = dtFile.ToString("yyyy-MM-dd hh:mm:ss");

            DateTime dtStart = DateTime.Now;
            Console.WriteLine("Job WzDatas_Distribution：" + path);
            foreach (var item in lstAttrName)
            {
                try
                {
                    DateTime dtStart0 = DateTime.Now;
                    Console.WriteLine("\t" + item + "：" + dtStart.ToString("yyyy-MM-dd hh:mm:ss"));

                    bResult = bResult && this.DoDistribution(item, path, temps[1], strTime);

                    Console.WriteLine("\t  --" + item + "end. 耗时({0}s)：", (DateTime.Now - dtStart0).TotalSeconds);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("\t" + item + "：" + ex.ToString());
                    //throw;
                }
            }
            Console.WriteLine("  --Job WzDatas_Distribution end. 耗时({0}s)：", (DateTime.Now - dtStart).TotalSeconds);
            return bResult;
        }
        private bool DoDistribution(string algAtrrName, string datasFile, string strTimeType, string strTime)
        {
            GdalCommon.RegisterAll();
            Servie_Distribution GdalServie = new Servie_Distribution();

            //初始参数
            string strParams = GdalServie.InitParam_Test(algAtrrName);
            if (strParams == "") return true;

            JObject pParams = JObject.Parse(strParams);
            pParams["dataTime"] = strTime;
            pParams["srcData"]["srcVectorFilename"] = datasFile;
            pParams["algParms"]["algAtrrName"] = algAtrrName;
            strParams = JsonConvert.SerializeObject(pParams);

            //分布图模型调用
            GdalServie.InitParams(strParams);
            GdalServie.RunModel("");

            // 通用转换（将绝对路径转换为网页路径）
            string result = GdalServie.GetResult();
            common.transResult_zpService(result);

            JObject temp = JObject.Parse(result);
            this.sendMsg("TEXT", string.Format("{0}-{1} --{2}", algAtrrName, strTimeType, strTime), "" + temp["renderer"]["renderer"]["route"].ToString() + temp["renderer"]["renderer"]["namePublish"].ToString());
            return true;
        }

        private bool sendMsg(string type, string text, string imgPath)
        {
            var msgWx = new
            {
                usrID = _nameUsr,
                usrName = _nameUsr,
                msgID = "",
                msgType = type,
                msg = text,

                groupID = _nameUsr,
                groupName = _nameUsr,
                usrPlat = "wx",
                time = DateTime.Now.Ticks
            };
            var msgWx2 = new
            {
                usrID = _nameUsr,
                usrName = _nameUsr,
                msgID = "",
                msgType = "IMAGE",
                msg = imgPath,

                groupID = _nameUsr,
                groupName = _nameUsr,
                usrPlat = "wx",
                time = DateTime.Now.Ticks
            };

            List<dynamic> lstData = new List<dynamic>() { msgWx, msgWx2 };
            var msg = JsonConvert.SerializeObject(lstData);
            File.WriteAllText(_pathMsg + "/msgWx_" + DateTime.Now.ToString("yyyy_MM_dd_HH_mm_ss") + ".json", msg, Encoding.UTF8);
            return true;
        }
    }
}