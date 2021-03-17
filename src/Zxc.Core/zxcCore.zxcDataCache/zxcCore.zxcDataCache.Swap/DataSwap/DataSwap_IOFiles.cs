using System;
using System.Collections.Generic;
using Microsoft.Extensions.FileProviders;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace zxcCore.zxcDataCache.Swap
{
    public class DataSwap_IOFiles : DataSwap
    {
        #region 属性及构造

        /// <summary数据交换事件
        /// </summary>
        public new event DataSwapChange_EventHandler SwapData_Change;

        protected internal bool _canDebug = false;         //是否允许打印调试信息
        protected internal string _dirSwap = "";           //文件交换目录
        protected internal string _dirSwap_back = "";      //文件交换目录-备份   
        protected internal Task<bool> _taskSwap = null;

        public DataSwap_IOFiles(string tagName, string dirSwap, int delayedTime = 0, Type classType = null, string nameMethod = "", bool canDebug = true) : base(tagName, delayedTime, classType, nameMethod)
        {
            _canDebug = canDebug;
            _dirSwap = dirSwap;
            _delayedTime = delayedTime;
            _dirSwap_back = dirSwap + "_back/" + tagName;
        }
        public DataSwap_IOFiles() : base("")
        {
        }
        ~DataSwap_IOFiles()
        {
            // 缓存数据？
        }

        #endregion


        public override bool Start(int nSteps = -1, int nStepSwaps = 1, int nFrequency = 1000)
        {
            _nSteps = nSteps;
            if (_taskSwap == null || _taskSwap.Status != TaskStatus.Running)
                _taskSwap = Task.Run(() => thrdSwapData_Out(nStepSwaps, nFrequency));
            _is_Running = _taskSwap.Status == TaskStatus.Running;
            return true;
        }
        public override bool Stop()
        {
            _nSteps = 0;
            if (_taskSwap != null)
            {
                _taskSwap.Dispose();
                _taskSwap = null;
            }
            return true;
        }

        protected virtual bool thrdSwapData_Out(int nStepSwaps = 1, int nFrequency = 1000)
        {
            while (_nSteps != 0)
            {
                try
                {
                    _nSteps--;
                    List<dynamic> lstDatas = SwapData_In(nStepSwaps);

                    if (this.SwapData_Change != null)
                    {
                        if (lstDatas.Count > 0)
                            this.SwapData_Change(this, this.CreateDataSwap_EventArgs(lstDatas));
                    }
                    Thread.Sleep(nFrequency);         //模拟长时间运算
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error(DataSwap IOFiles)：" + e.ToString());
                    //throw;
                }
            }
            return true;
        }

        public override List<dynamic> SwapData_In(int nStepSwaps = 1)
        {
            if (_canDebug)
            {
                Console.WriteLine("DataSwap IOFiles::");
                Console.WriteLine("\t" + _dirSwap);
            }

            int result = 0, nums = 0;
            List<string> errs = new List<string>();
            List<dynamic> lstDatas = new List<dynamic>();
            nStepSwaps = nStepSwaps <= 0 ? int.MaxValue : nStepSwaps;

            var provider = new PhysicalFileProvider(_dirSwap);
            var contents = provider.GetDirectoryContents(string.Empty);
            if (_canDebug)
            {
                Console.WriteLine("\tSwap IOFiles(" + contents.Count() + ")");
            }
            foreach (var item in contents)
            {
                if (item.IsDirectory) continue;
                if (_delayedTime > 0)  //解析时间并校检
                {
                    if ((DateTime.Now - item.LastModified.LocalDateTime).TotalSeconds > _delayedTime)
                    {
                        this.SwapData_BackUp(item.PhysicalPath, _dirSwap_back);
                        continue;
                    }
                }
                string strExtension = System.IO.Path.GetExtension(item.Name);
                if (strExtension != ".json" && strExtension != ".geojson") continue;
                if (item.Name.Substring(0, _tagName.Length) != _tagName) continue;

                using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                {
                    if (_canDebug)
                    {
                        Console.WriteLine("\tnew file swap:: " + item.PhysicalPath);
                    }
                    using (JsonTextReader reader = new JsonTextReader(file))
                    {
                        //循环解析文件json数据
                        JObject jsonFile = (JObject)JToken.ReadFrom(reader);
                        JArray jsonDatas = (JArray)jsonFile["datas"];

                        foreach (var jsonData in jsonDatas)
                        {
                            var data = this.CreateData_ClassObj(jsonData);
                            lstDatas.Add(data);
                        }
                    }
                    this.SwapData_BackUp(item.PhysicalPath, _dirSwap_back);         // 备份文件
                    nums++;
                    if (nums >= nStepSwaps) break;
                }
            }

            if (_canDebug)
            {
                Console.WriteLine("DataSwap IOFiles End." + "\tMargin Swap IOFiles(" + (contents.Count()) + ")\n");
            }
            return lstDatas;
        }
        public override bool SwapData_Out(dynamic value)
        {
            return false;
        }

    }
}
