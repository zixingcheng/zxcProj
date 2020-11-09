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
    public class FtpUserJobTrigger : BaseJobTrigger
    {
        public FtpUserJobTrigger() :
            base(TimeSpan.Zero,
                TimeSpan.FromMinutes(60 * 6),
                new FtpUserJobExcutor())
        {
        }
    }

    public class FtpUserJobExcutor
                     : IJobExecutor
    {
        private Dictionary<string, JObject> dictGroups = new Dictionary<string, JObject>();
        private Dictionary<string, string> dictUsrGroups = new Dictionary<string, string>();

        public void StartJob()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            this.JobInfo_Group();
            this.JobInfo_UserGroup();
            this.JobInfo_User();
        }

        public void JobInfo_Group()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var provider = new PhysicalFileProvider(Directory.GetCurrentDirectory() + @"/ftpData/task");
            var contents = provider.GetDirectoryContents(string.Empty);
            foreach (var item in contents)
            {
                if (!item.Name.Contains("group_")) continue;
                if (item.IsDirectory == false)
                {
                    int result = 0;
                    List<string> errs = new List<string>();
                    using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                    {
                        Console.WriteLine("new file group:: " + item.PhysicalPath);
                        using (JsonTextReader reader = new JsonTextReader(file))
                        {
                            // 循环解析文件json数据
                            JObject jsonObject = (JObject)JToken.ReadFrom(reader);
                            JArray jsonValues = (JArray)jsonObject["RECORDS"];
                            if (jsonValues.Count > 0)
                            {
                                //按逻辑结构组织对象
                                //for (int i = 0; i < jsonValues.Count; i++)
                                //{
                                //    dictObjs[jsonValues[i]["id"].ToString()] = (JObject)jsonValues[i];
                                //}
                                //
                                //按逻辑结构组织对象
                                //Dictionary<string, JObject> dictOrg = new Dictionary<string, JObject>();
                                //for (int i = 0; i < jsonValues.Count; i++)
                                //{
                                //    JObject obj = (JObject)jsonValues[i];
                                //}dictObjs

                                var optionsBuilder = new DbContextOptionsBuilder<db_MicroStationContext>();
                                using (var context = new db_MicroStationContext(optionsBuilder.Options))
                                {
                                    var queryAll = context.Organization.AsQueryable().Where("OrganizationOid != @0", "").ToList();
                                    foreach (var value in jsonValues)
                                    {
                                        string Nodepath = (string)value["path"];
                                        if (Nodepath == null || !Nodepath.Contains("东莞市生态环境局")) continue;

                                        string srcOid = (string)value["id"];
                                        Console.WriteLine("srcOid:: " + srcOid);
                                        var query = queryAll.Where(s => s.OrganizationOid == srcOid).FirstOrDefault();
                                        try
                                        {
                                            if (query == null)
                                            {
                                                Organization obj = new Organization
                                                {
                                                    OrganizationOid = srcOid,
                                                    Organizationcategory = (int)value["category"],
                                                    Departmenttype = (int)value["departmentType"],
                                                    Groupname = (string)value["groupName"],
                                                    GroupType = (int)value["groupType"],
                                                    Organizationcode = (string)value["orgCode"],
                                                    Organizationlevel = (int)value["orgLevel"],
                                                    Parentnodecode = (string)value["parentId"],
                                                    Nodepath = (string)value["path"],
                                                };
                                                context.Add(obj);
                                            }
                                            else
                                            {
                                                query.OrganizationOid = srcOid;
                                                query.Organizationcategory = (int)value["category"];
                                                query.Departmenttype = (int)value["departmentType"];
                                                query.Groupname = (string)value["groupName"];
                                                query.GroupType = (int)value["groupType"];
                                                query.Organizationcode = (string)value["orgCode"];
                                                query.Organizationlevel = (int)value["orgLevel"];
                                                query.Parentnodecode = (string)value["parentId"];
                                                query.Nodepath = (string)value["path"];
                                            }
                                            dictGroups[srcOid] = (JObject)value;
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
                                        Dockingtype = "组织机构",
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
                        }
                    }

                    // 转移文件
                    if (result > errs.Count)
                    {
                        //File.Copy(item.PhysicalPath, AppContext.BaseDirectory + @"ftpData/user_old/" + item.Name);
                        //File.Delete(item.PhysicalPath);
                    }
                }
            }
        }
        public void JobInfo_UserGroup()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var provider = new PhysicalFileProvider(Directory.GetCurrentDirectory() + @"/ftpData/task");
            var contents = provider.GetDirectoryContents(string.Empty);
            foreach (var item in contents)
            {
                if (!item.Name.Contains("user_group")) continue;
                if (item.IsDirectory == false)
                {
                    int result = 0;
                    List<string> errs = new List<string>();
                    using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                    {
                        Console.WriteLine("new file user: " + item.PhysicalPath);
                        using (JsonTextReader reader = new JsonTextReader(file))
                        {
                            // 循环解析文件json数据
                            JObject jsonObject = (JObject)JToken.ReadFrom(reader);
                            JArray jsonValues = (JArray)jsonObject["RECORDS"];
                            if (jsonValues.Count > 0)
                            {
                                //按逻辑结构组织对象
                                for (int i = 0; i < jsonValues.Count; i++)
                                {
                                    string groupOid = jsonValues[i]["groupId"].ToString();
                                    if (dictGroups.ContainsKey(groupOid))
                                    {
                                        dictUsrGroups[jsonValues[i]["userId"].ToString()] = groupOid;
                                    }
                                }
                            }
                        }
                    }

                    // 转移文件
                    if (result > errs.Count)
                    {
                        //File.Copy(item.PhysicalPath, AppContext.BaseDirectory + @"ftpData/user_old/" + item.Name);
                        //File.Delete(item.PhysicalPath);
                    }
                }
            }
        }
        public void JobInfo_User()
        {
            // 读取文件夹列表
            if (common.coon == "") return;
            var provider = new PhysicalFileProvider(Directory.GetCurrentDirectory() + @"/ftpData/task");
            var contents = provider.GetDirectoryContents(string.Empty);
            foreach (var item in contents)
            {
                if (!item.Name.Contains("user_")) continue;
                if (item.Name.Contains("user_group")) continue;
                if (item.IsDirectory == false)
                {
                    int result = 0;
                    List<string> errs = new List<string>();
                    using (System.IO.StreamReader file = System.IO.File.OpenText(item.PhysicalPath))
                    {
                        Console.WriteLine("new file user: " + item.PhysicalPath);
                        using (JsonTextReader reader = new JsonTextReader(file))
                        {
                            // 循环解析文件json数据
                            JObject jsonObject = (JObject)JToken.ReadFrom(reader);
                            JArray jsonValues = (JArray)jsonObject["RECORDS"];
                            if (jsonValues.Count > 0)
                            {
                                var optionsBuilder = new DbContextOptionsBuilder<db_MicroStationContext>();
                                using (var context = new db_MicroStationContext(optionsBuilder.Options))
                                {
                                    var queryAll = context.UserInfo.AsQueryable().Where("Useroid != @0", "").ToList();
                                    foreach (var value in jsonValues)
                                    {
                                        //提取suer的group信息
                                        string userId = (string)value["id"];
                                        Console.WriteLine("userId:: " + userId);
                                        if (!dictUsrGroups.ContainsKey(userId)) continue;

                                        var query = queryAll.Where(s => s.Useroid == userId).FirstOrDefault();
                                        try
                                        {
                                            JObject objGroup = dictGroups[dictUsrGroups[userId]];
                                            if (query == null)
                                            {
                                                UserInfo obj = new UserInfo
                                                {
                                                    UserInfoOid = Guid.NewGuid().ToString("D"),
                                                    Useroid = (string)value["id"],
                                                    Userid = (string)value["userName"],
                                                    Username = (string)value["displayName"],
                                                    UserPwd = "On8U4+dy1Rs=",       //默认密码12345678
                                                    Userphone = (string)value["mobile"],
                                                    Isitavailable = (ulong)value["enable"],
                                                    Organizationoid = dictUsrGroups[userId],
                                                    Groupname = (string)objGroup["groupName"],
                                                    Nodepath = (string)objGroup["path"],
                                                };
                                                checkPermission(ref obj);
                                                context.Add(obj);
                                            }
                                            else
                                            {
                                                query.Useroid = (string)value["id"];
                                                query.Userid = (string)value["userName"];
                                                query.Username = (string)value["displayName"];
                                                query.Userphone = (string)value["mobile"];
                                                query.Isitavailable = (ulong)value["enable"];
                                                query.Organizationoid = dictUsrGroups[userId];
                                                query.Groupname = (string)objGroup["groupName"];
                                                query.Nodepath = (string)objGroup["path"];
                                                checkPermission(ref query);
                                            }
                                        }
                                        catch (Exception)
                                        {
                                            Console.WriteLine("err srcID::" + userId);
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
                                        Dockingtype = "用户信息",
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
                        }
                    }

                    // 转移文件
                    Thread.Sleep(1000);
                    if (result > errs.Count || errs.Count == 0)
                    {
                        File.Copy(item.PhysicalPath, Directory.GetCurrentDirectory() + @"/ftpData/task_old/" + item.Name);
                        File.Copy(item.PhysicalPath.Replace("user_", "user_group"), Directory.GetCurrentDirectory() + @"/ftpData/task_old/" + item.Name.Replace("user_", "user_group"));
                        File.Copy(item.PhysicalPath.Replace("user_", "group_"), Directory.GetCurrentDirectory() + @"/ftpData/task_old/" + item.Name.Replace("user_", "group_"));
                        Thread.Sleep(2000);
                        File.Delete(item.PhysicalPath);
                        File.Delete(item.PhysicalPath.Replace("user_", "user_group"));
                        File.Delete(item.PhysicalPath.Replace("user_", "group_"));
                        common.userManger.Init();       // 用户信息重载
                    }
                }
            }
        }

        public void checkPermission(ref UserInfo usrInfo)
        {
            if (usrInfo.Nodepath == "") return;
            string node = usrInfo.Nodepath.Replace("/政府系统", "");
            string[] nodes = node.Substring(1).Split("/");

            string permission = null;
            if (nodes[0] == "东莞市" && nodes[1] == "东莞市生态环境局")
            {

                if (nodes.Length == 2)
                    permission = "";
                else if (nodes.Length > 2)
                {
                    if (nodes[2].Contains("分局"))
                    {
                        if (nodes.Length == 3)
                        {
                            permission = "." + nodes[2].Replace("东莞市生态环境局", "").Replace("分局", "");
                        }
                        if (nodes.Length > 3 && (nodes[3].Contains("股") || nodes[3].Contains("领导")))
                        {
                            permission = "." + nodes[2].Replace("东莞市生态环境局", "").Replace("分局", "");
                        }
                    }
                    else if (nodes[2].Contains("执法") || nodes[2].Contains("大气环境科") || nodes[2].Contains("领导") || nodes[2].Contains("信息"))
                    {
                        permission = "";
                    }
                }
            }
            usrInfo.Permission = permission;
        }

        public void StopJob()
        {
            //LogUtil.Info("系统终止任务");
        }
    }
}