using System;
using System.Collections.Generic;
using Microsoft.Extensions.FileProviders;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.IO;

namespace zxcCore.zxcData.Cache.Swap
{
    public class DataSwap_IOFiles : DataSwap
    {
        #region 属性及构造

        protected internal string _dirSwap = "";           //文件交换目录
        protected internal string _dirSwap_back = "";      //文件交换目录-备份   

        public DataSwap_IOFiles(string tagName, string dirSwap, int delayedTime = 0, Type classType = null, string nameMethod = "", bool canDebug = true, bool useAck = false) : base(tagName, delayedTime, classType, nameMethod, canDebug, useAck)
        {
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

        public override List<dynamic> SwapData_In(int nStepSwaps, out AckInfo ackInfo)
        {
            int nums = 0;
            ackInfo = null;
            List<string> errs = new List<string>();
            List<dynamic> lstDatas = new List<dynamic>();
            nStepSwaps = nStepSwaps <= 0 ? int.MaxValue : nStepSwaps;

            var provider = new PhysicalFileProvider(_dirSwap);
            var contents = provider.GetDirectoryContents(string.Empty);
            if (contents.Count() > 0)
            {
                if (_canDebug)
                {
                    Console.WriteLine(DateTime.Now.ToLongTimeString() + "  DataSwap IOFiles::");
                    Console.WriteLine("\t" + _dirSwap);
                    Console.WriteLine("\tSwap IOFiles(" + contents.Count() + ")");
                }
                foreach (var item in contents)
                {
                    if (SwapData_AckNeed(item.PhysicalPath)) continue;
                    if (item.IsDirectory) continue;
                    if (_delayedTime > 0)  //解析时间并校检
                    {
                        if ((DateTime.Now - item.LastModified.LocalDateTime).TotalSeconds > _delayedTime)
                        {
                            this.SwapData_BackUp(item.PhysicalPath, _dirSwap_back);
                            continue;
                        }
                    }
                    if (item.Length == 0)
                    {
                        File.Delete(item.PhysicalPath);
                        continue;
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
                            JToken jsonFile = JToken.ReadFrom(reader);
                            JArray jsonDatas = null;

                            //提取数据，兼容多种格式
                            if (jsonFile.Type == JTokenType.Array)
                            {
                                jsonDatas = (JArray)jsonFile;
                            }
                            else
                            {
                                jsonDatas = (JArray)jsonFile["datas"];
                            }

                            //循环生成数据对象
                            foreach (var jsonData in jsonDatas)
                            {
                                var data = this.CreateData_ClassObj(jsonData);
                                lstDatas.Add(data);
                            }
                        }
                        if (this.SwapData_BackUp(item.PhysicalPath, _dirSwap_back))         // 备份文件
                        {
                            if (_useAck)    //生成确认信息
                                ackInfo = new AckInfo(item.Name, item.PhysicalPath);
                            this.SwapData_Buffer(item.Name, item.PhysicalPath);
                        }
                        nums++;
                        if (nums >= nStepSwaps) break;
                    }
                }

                if (_canDebug)
                {
                    Console.WriteLine("DataSwap IOFiles End." + "\tMargin Swap IOFiles(" + (contents.Count()) + ")\n");
                }
            }
            return lstDatas;
        }
        public override bool SwapData_Out(dynamic value)
        {
            return false;
        }

    }
}
