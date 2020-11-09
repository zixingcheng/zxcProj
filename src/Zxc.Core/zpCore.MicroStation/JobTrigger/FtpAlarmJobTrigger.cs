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
using System.Threading;

namespace zpCore.MicroStation.JobTrigger
{
    public class FtpAlarmJobTrigger : BaseJobTrigger
    {
        public FtpAlarmJobTrigger() :
            base(TimeSpan.Zero,
                TimeSpan.FromMinutes(10),
                new FtpAlarmJobExcutor())
        {
        }
    }

    public class FtpAlarmJobExcutor
                     : IJobExecutor
    {
        public void StartJob()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var provider = new PhysicalFileProvider(Directory.GetCurrentDirectory() + @"/ftpData/alarm");
            var contents = provider.GetDirectoryContents(string.Empty);
            foreach (var item in contents)
            {
                if (item.IsDirectory == false)
                {
                    int result = 0;
                    List<string> errs = new List<string>();
                    using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                    {
                        Console.WriteLine("new file alarm:: " + item.PhysicalPath);
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
                                    var queryAll = context.Infoalarm.AsQueryable().Where("srcOID != @0", "").OrderByDescending(d => d.Alarmtime).Take(1000).ToList();
                                    foreach (var value in jsonValues)
                                    {
                                        string srcOid = (string)value["id"];
                                        Console.WriteLine("srcOid:: " + srcOid);
                                        var query = queryAll.Where(s => s.SrcOid == srcOid).FirstOrDefault();
                                        if (query != null) continue;
                                        try
                                        {
                                            Infoalarm obj = new Infoalarm
                                            {
                                                InfoalarmOid = Guid.NewGuid().ToString("D"),
                                                DeployId = (int)value["targetId"],
                                                SrcOid = (string)value["id"],
                                                AlarmType = (string)value["targetType"] == "station" ? "监测站点实时告警" : "",
                                                Alarmindex = (string)value["warningIndicator"],
                                                Alarmlevel = (string)value["warningLevel"],
                                                Alarmtitle = (string)value["warningTitle"],
                                                Alarmcontent = (string)value["warningContent"],
                                                Alarmtime = (DateTime)value["createTime"],
                                                Datatime = (DateTime)value["lastTime"],
                                                Cratetime = DateTime.Now
                                            };
                                            if (!string.IsNullOrEmpty((string)value["normalTime"]))
                                                obj.AlarmtimeNormal = (DateTime)value["normalTime"];
                                            if (!string.IsNullOrEmpty((string)value["lastTime"]))
                                                obj.AlarmtimeLast = (DateTime)value["lastTime"];
                                            context.Add(obj);
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
                                        Dockingtype = "站点告警",
                                        AssociationId = "",
                                        Dockingmode = "download",
                                        Dockingtime = DateTime.Now,
                                        Dockingresults = errs.Count > 0 ? "失败" : "完成",
                                        Dockingtimes = 1,
                                        Dockmark = errs.ToString(),
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
                        File.Copy(item.PhysicalPath, Directory.GetCurrentDirectory() + @"/ftpData/alarm_old/" + item.Name);
                        Thread.Sleep(1000);
                        File.Delete(item.PhysicalPath);
                    }
                }
            }
        }

        public void StopJob()
        {
            //LogUtil.Info("系统终止任务");
        }
    }
}