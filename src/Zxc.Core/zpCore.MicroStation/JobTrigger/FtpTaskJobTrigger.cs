using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.MicroStation;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;

using zpCore.MicroStation.Models;
using zpCore.MicroStation.Common;
using Microsoft.Extensions.Options;
using System.Text;
using Microsoft.Extensions.DependencyInjection;
using System.Diagnostics;
using System.Threading;

namespace zpCore.MicroStation.JobTrigger
{
    public class FtpTaskJobTrigger : BaseJobTrigger
    {
        public FtpTaskJobTrigger() :
            base(TimeSpan.Zero,
                TimeSpan.FromMinutes(10),
                new FtpTaskJobExcutor())
        {
        }
    }

    public class FtpTaskJobExcutor
                     : IJobExecutor
    {
        private db_MicroStationContext _context = new db_MicroStationContext(new DbContextOptionsBuilder<db_MicroStationContext>().UseMySql(common.coon).Options);
        private PictureOptions _pictureOptions;
        public void StartJob()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var services = new ServiceCollection();
            var provider = services.BuildServiceProvider();
            this._pictureOptions = provider.GetService<PictureOptions>();
            // (this._pictureOptions == null) return;

            DoDowndata_Task();      // 下载任务信息
            DoUpdata_Task();        // 更新及反馈任务信息
        }
        public void StartJob(IOptions<PictureOptions> options) => this._pictureOptions = options.Value;

        public void DoDowndata_Task()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var provider = new PhysicalFileProvider(Directory.GetCurrentDirectory() + @"/ftpData/task");
            Console.WriteLine(Directory.GetCurrentDirectory() + @"/ftpData/task");
            var contents = provider.GetDirectoryContents(string.Empty);
            foreach (var item in contents)
            {
                if (item.IsDirectory == false)
                {
                    int result = 0;
                    List<string> errs = new List<string>();
                    using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                    {
                        Console.WriteLine("new file task:: " + item.PhysicalPath);
                        using (JsonTextReader reader = new JsonTextReader(file))
                        {
                            // 循环解析文件json数据
                            JObject jsonObject = (JObject)JToken.ReadFrom(reader);
                            JArray jsonValues = (JArray)jsonObject["RECORDS"];
                            if (jsonValues.Count > 0)
                            {
                                var optionsBuilder = new DbContextOptionsBuilder<db_MicroStationContext>();
                                optionsBuilder.UseMySql(common.coon);
                                using (var context = new db_MicroStationContext(optionsBuilder.Options))
                                {
                                    foreach (var value in jsonValues)
                                    {
                                        string srcOid = (string)value["id"];
                                        Console.WriteLine("srcOid:: " + srcOid);

                                        string taskType = (string)value["taskType"];
                                        string subtype = (string)value["subtype"];
                                        if (!(taskType == "2")) continue;

                                        if ((string)value["taskObjective"] == null) continue;
                                        var taskObj = (JObject)JToken.Parse((string)value["taskObjective"]);

                                        if (taskObj["entMessageList"] == null) continue;
                                        var listTrac = (JArray)taskObj["entMessageList"];
                                        if (listTrac.Count < 1) continue;

                                        var query = context.TaskOrder.AsQueryable().Where("Taskid = @0", srcOid);
                                        if (query.Count() > 0) continue;
                                        try
                                        {
                                            // 循环企业清单列表
                                            foreach (var trace in listTrac)
                                            {
                                                TaskOrder obj = new TaskOrder
                                                {
                                                    TaskOrderOid = Guid.NewGuid().ToString("D"),
                                                    Taskid = (string)value["id"],
                                                    TaskTypeSrc = taskType,
                                                    TaskTypesubSrc = subtype,
                                                    Tasktitle = (string)value["brief"],
                                                    Tasktype = (string)value["targetType"],
                                                    Taskstatus = (string)value["status"] == "ASSIGNING" ? "待查收" : (string)value["status"],
                                                    Taskobjectname = (string)value["targetName"],
                                                    TaskTownStreet = (string)taskObj["townName"],
                                                    TaskCommunity = ((string)taskObj["warningTargetName"]).Split("-")[0],

                                                    AlarmStationnumber = (int)taskObj["warningTargetId"],
                                                    AlarmStationname = (string)taskObj["warningTargetName"],
                                                    Alarmcontent = (string)taskObj["warningContent"],
                                                    Alarmtime = (DateTime)taskObj["dataTime"],
                                                    Alarmfactor = (string)taskObj["warningFactory"],

                                                    Tasksubobjectname = (string)trace["targetName"],
                                                    TasksubobjectOrgcode = (string)trace["orgCode"],
                                                    TasksubTownStreet = (string)trace["townName"],
                                                    TasksubCommunity = (string)trace["streetName"],
                                                    Tasksubobjectaddress = (string)trace["addr"],
                                                    Contributionrateranking = (int)trace["rank"],
                                                    Contributionrate = (float)trace["rate"],

                                                    //Contributionrate= (float)value["warningIndicator"],
                                                    //Contributionrateranking = (int)value["warningIndicator"],

                                                    Collectorid = (string)taskObj["agentId"],
                                                    Collector = (string)taskObj["agentName"],
                                                    Collectorphone = (string)taskObj["agentContact"],
                                                    CollectorunitId = (string)taskObj["agentOrgId"],
                                                    CollectorunitName = (string)taskObj["agentOrgName"],

                                                    Taskcontent = (string)value["detail"],
                                                    Tasknotes = (string)value["remark"],
                                                    Taskstarttime = (DateTime)value["implStartTime"],
                                                    Taskdeadline = (DateTime)value["implEndTime"],
                                                    Taskreceivingtime = DateTime.Now,
                                                    Taskfallback = (ulong?)(((string)value["backReason"]) + "" == "" ? 0 : 1),
                                                    Taskfallbackreason = (string)value["backReason"],

                                                    //Checktime = null,
                                                    //Taskfeedbacktimes = 0,
                                                    //Taskfeedbacktime = null,
                                                    //Taskcompletetime = null,
                                                    Taskstatusupdatetime = DateTime.Now
                                                };
                                                if (!string.IsNullOrEmpty((string)value["Taskfallbacktime"]))
                                                    obj.Taskfallbacktime = (DateTime)value["Taskfallbacktime"];
                                                context.Add(obj);

                                                //TaskOrder objSub = obj. 
                                                //Taskobjectaddress = (string)value["targetAddress"],
                                                //TaskTraceability objTrac = new TaskTraceability
                                                //{
                                                //    TaskTraceabilityOid = Guid.NewGuid().ToString("D"),
                                                //    Taskordeid = obj.TaskOrderOid,
                                                //    Taskid = obj.Taskid,
                                                //    Sitecode = (int)trace["stationCode"],
                                                //    TargetName = (string)trace["targetName"],
                                                //    TownStreet = (string)trace["townName"],
                                                //    OrgCode = (string)trace["orgCode"],
                                                //    TargetAddr = (string)trace["addr"],
                                                //    PollutionRank = (int)trace["rank"],
                                                //    PollutionRate = (float)trace["rate"]
                                                //};
                                            }
                                        }
                                        catch (Exception)
                                        {
                                            Console.WriteLine("err srcID::" + srcOid);
                                            errs.Add((string)value["id"]);
                                            throw;
                                        }
                                    }
                                    result = context.SaveChanges();
                                    Console.WriteLine("res count::" + result.ToString());

                                    // 记录操作
                                    TaskDocking docking = new TaskDocking
                                    {
                                        TaskDockingOid = Guid.NewGuid().ToString("D"),
                                        Filename = item.Name,
                                        Filepath = item.PhysicalPath,
                                        Dockingtype = "站点任务",
                                        AssociationId = "",
                                        Dockingmode = "download",
                                        Dockingtime = DateTime.Now,
                                        Dockingresults = errs.Count > 0 ? "失败" : "完成",
                                        Dockingtimes = 1,
                                        Dockmark = string.Join(",", errs),
                                        Createtime = DateTime.Now
                                    };
                                    context.Add(docking);
                                    int result2 = context.SaveChanges();
                                }
                            }
                            Task.Run(() =>
                            {
                            });
                        }
                    }

                    // 转移文件
                    if (result > errs.Count || errs.Count == 0)
                    {
                        File.Copy(item.PhysicalPath, Directory.GetCurrentDirectory() + @"/ftpData/task_old/" + item.Name);
                        Thread.Sleep(1000);
                        File.Delete(item.PhysicalPath);
                    }
                }
            }
        }

        public void DoUpdata_Task()
        {
            DoUpdata_Task_back();
        }
        public void DoUpdata_Task_back()
        {
            // 任务回退信息
            DateTime dtStart = getDock_time(true, "站点任务-反馈");
            DateTime dtEnd = DateTime.Now;

            string sql = "Taskfeedbacktime > @0 And Taskfeedbacktime <= @1";
            var query = _context.TaskFeedback
                                .AsQueryable()
                                    .Where(sql, dtStart, dtEnd)
                                    .OrderBy(e => e.Taskfeedbacktime);
            if (query.Count() == 0) return;

            int size = 100, page = 1;
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            int ind = 1;
            JArray datas = new JArray();
            foreach (var item in query)
            {
                JObject data = new JObject();
                data["taskType"] = item.TaskTypeSrc;
                data["subType"] = item.TaskTypesubSrc;
                data["excelTemplate"] = null;
                data["id"] = item.Taskfeedbacktimes;
                data["completeRate"] = item.Taskstatus == "已完成" ? 100 : 0;
                data["feedbackTime"] = ((DateTime)item.Taskfeedbacktime).ToString("yyyy-MM-dd hh:mm:ss");
                data["feedbackType"] = item.Taskstatus == "已完成" ? 0 : item.Taskstatus == "开展中" ? 1 : 2;
                data["feedbackContent"] = item.Supervision;

                //APP反馈选择，当选择是 / 否时，提交到平台的内容改为对应的文字。
                //对应关系：
                //是否需要整改：是 - 需要整改；否 - 不需要整改；
                //是否需要执法：是 - 需要执法；否 - 不需要执法；
                //是否需要处罚：是 - 需要处罚；否 - 不需要处罚。
                data["isItnecessaryToRectify"] = item.Isitnecessarytorectify == 1 ? "需要整改" : "不需要整改";
                data["isLawEnforcementNecessary"] = item.Islawenforcementnecessary == 1 ? "需要执法" : "不需要执法";
                data["isItnecessaryToPunish"] = item.Isitnecessarytopunish == 1 ? "需要处罚" : "不需要处罚";
                if (item.Taskstatus != "开展中")
                {
                    data["isItnecessaryToRectify"] = null;
                    data["isLawEnforcementNecessary"] = null;
                    data["isItnecessaryToPunish"] = null;
                }
                data["taskId"] = item.Taskid;
                data["taskStatus"] = item.Taskstatus;
                data["tasktargetName"] = item.Taskobjectname;   
                data["imgUrlList"] = checkFileNames(item.Picturenames, dtEnd, ref ind);
                data["attach"] = null;
                datas.Add(data);
            }

            // 保存文件
            var result = JsonConvert.SerializeObject(new { RECORDS = datas });
            string fileName = "fk_" + dtEnd.ToString("yyyyMMdd_hhmm") + ".json";
            string strPath = Directory.GetCurrentDirectory() + @"/ftpData/taskfeed/" + dtEnd.ToString("yyyyMM") + "/" + dtEnd.ToString("yyyyMMdd") + "/" + fileName;
            this.checkFileFloder(strPath);
            FileStream fileStream = new FileStream(strPath, FileMode.CreateNew);
            using (StreamWriter writer = new StreamWriter(fileStream))
            {
                writer.Write(result);
            }

            // 记录对接信息
            TaskDocking docking = new TaskDocking
            {
                TaskDockingOid = Guid.NewGuid().ToString("D"),
                Filename = fileName,
                Filepath = strPath,
                Dockingtype = "站点任务-反馈",
                AssociationId = "",
                Dockingmode = "upload",
                Dockingtime = DateTime.Now,
                Dockingresults = (File.Exists(strPath)) ? "完成" : "失败",
                Dockingtimes = 1,
                Dockmark = "",
                Createtime = DateTime.Now
            };
            _context.Add(docking);
            int result2 = _context.SaveChanges();
        }
        public void checkFileFloder(string path)
        {
            FileInfo fi = new FileInfo(path);
            if (!fi.Exists)
            {
                var di = fi.Directory;
                if (!di.Exists)
                    di.Create(); Thread.Sleep(100);
            }
        }

        public bool checkFile(string[] strFiles, List<string> arrFiles)
        {
            bool bRes = true;
            string dir = Directory.GetCurrentDirectory() + common.ftpDir + "/";
            for (int i = 0; i < strFiles.Length; i++)
            {
                string pathSrc = dir + strFiles[i];
                string pathDest = Directory.GetCurrentDirectory() + @"/ftpData/taskfeed/" + arrFiles[i];

                this.checkFileFloder(pathDest);
                if (!File.Exists(pathDest) && File.Exists(pathSrc))
                    File.Copy(pathSrc, pathDest); Thread.Sleep(10);
            }
            return bRes;
        }
        public string checkFileNames(string strFiles, DateTime dtNow, ref int ind)
        {
            if (strFiles + "" == "") return null;
            string prefix = dtNow.ToString("yyyyMM") + "/" + dtNow.ToString("yyyyMMdd") + "/pic_" + dtNow.ToString("yyyyMMdd_hhmm") + "/pic_" + dtNow.ToString("yyyyMMdd_hhmm") + "_";
            List<string> arrFiles = new List<string>();
            string[] files = strFiles.Split(";");
            for (int i = 0; i < files.Length; i++)
            {
                string suffix = files[i].Split(".")[1];
                arrFiles.Add(prefix + ind.ToString().PadLeft(4, '0') + "." + suffix);
                ind += 1;
            }
            checkFile(files, arrFiles);
            return string.Join(",", arrFiles);
        }
        // 提取对接类型最后时间
        public DateTime getDock_time(bool bIsUp, string dockTyp)
        { 
            string dockmode = bIsUp ? "upload" : "download";
            string sql = "Dockingtype == @0 And Dockingmode == @1 And Dockingresults == @2";
            var query = _context.TaskDocking
                                .AsQueryable()
                                    .Where(sql, dockTyp, dockmode, "完成")
                                    .OrderByDescending(o => o.Dockingtime);
            if (query.Count() > 0)
            {
                TaskDocking dock = query.Take(1).Single();
                return (DateTime)dock.Dockingtime;
            }
            else
                return new DateTime(2020, 01, 01);
            //LogUtil.Info("系统终止任务");
        }

        public void StopJob()
        {
            //LogUtil.Info("系统终止任务");
        }
    }
}