using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.MicroStation.Common;
using zpCore.MicroStation.Models;
/// <summary>任务工单接口集
/// </summary>
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class TaskOrderController : ControllerBase
    {
        private db_MicroStationContext _context;
        public TaskOrderController(db_MicroStationContext context)
        {
            _context = context;
        }


        /// <summary>新增任务信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> add(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            TaskOrder obj = new TaskOrder
            {
                TaskOrderOid = Guid.NewGuid().ToString("D"),
                Taskid = jsonParams.Taskid,
                Tasktitle = jsonParams.Tasktitle,
                Tasktype = jsonParams.Tasktype,
                Taskstatus = jsonParams.Taskstatus,

                Taskobjectname = jsonParams.Taskobjectname,
                TaskTownStreet = jsonParams.TaskTownStreet,
                TaskCommunity = jsonParams.TaskCommunity,

                AlarmStationnumber = jsonParams.AlarmStationnumber,
                AlarmStationname = jsonParams.AlarmStationname,
                Alarmcontent = jsonParams.Alarmcontent,
                Alarmfactor = jsonParams.Alarmfactor,
                Alarmtime = jsonParams.Alarmtime,

                Contributionrate = jsonParams.Contributionrate,
                Contributionrateranking = jsonParams.Contributionrateranking,

                Collector = "-",
                Collectorphone = "-",
                Taskfeedbacktimes = 0,

                Taskcontent = jsonParams.Taskcontent,
                Tasknotes = jsonParams.Tasknotes,
                Taskfallback = 0,
                Taskfallbackreason = "",

                Checktime = jsonParams.Checktime,
                Taskfallbacktime = jsonParams.Taskfallbacktime,
                Taskdeadline = jsonParams.Taskdeadline,
                Taskfeedbacktime = jsonParams.Taskfeedbacktime,
                Taskcompletetime = jsonParams.Taskcompletetime,
                Taskstatusupdatetime = DateTime.Now,
                Taskreceivingtime = DateTime.Now
            };

            _context.Add(obj);
            int result = _context.SaveChanges();
            var data = new { TaskOrderOid = obj.TaskOrderOid, result = result };
            return common.transResult(data);
        }

        /// <summary>提取任务数据
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            DateTime dtEnd = common.checkTime(jsonParams.dtTime);
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);

            string sql = "Taskreceivingtime <= @0";
            string type = jsonParams.Tasktype;
            if (type != null && type != "")
                sql += " And Tasktype = @1";

            string status = jsonParams.Taskstatus;
            if (status != null && status != "")
                sql += " And Taskstatus = @2";

            string factor = jsonParams.Alarmfactor;
            if (factor != null && factor != "")
                sql += " And Alarmfactor = @3";

            string taskid = jsonParams.Taskid;
            if (taskid != null && taskid != "")
                sql += " And Taskid = @4";
            string taskoid = jsonParams.TaskOrderOid;
            if (taskoid != null && taskoid != "")
                sql += " And TaskOrderOid = @5";

            string taskobj = jsonParams.keyword;
            if (taskobj != null && taskobj != "")
                sql += " And Tasksubobjectname.Contains(@6)";

            int id = Convert.ToInt32(jsonParams.DeployId);
            if (id > 0)
                sql += " And AlarmStationnumber = " + id;
            sql += " And Taskstatus != @7 And Taskstatus != @8";

            #region 数据权限控制

            var queryPerm = _context.TaskOrder;
            UserPermission permissions = common.checkPermissions(Convert.ToString(jsonParams.userName));
            if (permissions.HasPermission)
            {
                if (permissions.DelopyIds.Count > 0)
                {
                    sql += " And @9.Contains(AlarmStationnumber)";
                }
                else
                {
                    if (permissions.Communitys.Count > 0)
                    {
                        sql += " And @10.Contains(TasksubCommunity)";
                    }
                    else
                    {
                        if (permissions.TownStreets.Count > 0)
                        {
                            sql += " And @11.Contains(TasksubTownStreet)";
                        }
                    }
                }
            }
            else
                sql += " And AlarmStationnumber == -1";

            #endregion

            var query = _context.TaskOrder
                                .AsQueryable()
                                    .Where(sql, dtEnd, type, status, factor, taskid, taskoid, taskobj, "已回退", "已完成", permissions.DelopyIds, permissions.Communitys, permissions.TownStreets)
                                    .OrderBy("AlarmStationnumber")
                                    .ThenByDescending(e => e.Taskreceivingtime)
                                    .Select("new (TaskOrderOid, Taskid, Tasktitle, Tasktype, Taskstatus,Tasksubobjectname,TasksubTownStreet,TasksubCommunity,Tasksubobjectaddress,AlarmStationnumber,AlarmStationname,Alarmcontent, Alarmtime, Alarmfactor, Contributionrate, Contributionrateranking, Taskcontent, Tasknotes, Taskdeadline, Taskreceivingtime, Taskfallback, Taskfallbackreason, Taskfallbacktime, Collector, Collectorphone, Checktime, Taskfeedbacktimes, Taskfeedbacktime, Taskstatusupdatetime)");
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

        /// <summary>更新信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> updata(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());

            string sql = "";
            string taskordeid = jsonParams.Taskordeid;
            if (taskordeid != null && taskordeid != "")
                sql += "TaskOrderOid = @0";

            string taskid = jsonParams.Taskid;
            if (taskid != null && taskid != "")
            {
                if (sql != "") sql += " And ";
                sql += "Taskid = @1";
            }

            string objname = jsonParams.Taskobjname;
            if (objname != null && objname != "")
                sql += " And Taskobjectname = @2";
            sql += " And Taskstatus != @3 And Taskstatus != @4";

            // 查询单条
            var query = _context.TaskOrder
                                .AsQueryable()
                                    .Where(sql, taskordeid, taskid, objname, "已回退", "已完成")
                                    .OrderByDescending(e => e.Taskfeedbacktime);

            int rows = query.Count();
            if (rows == 1)
            {
                TaskOrder oder = query.Take(1).Single();
                oder.Taskstatus = jsonParams.Taskstatus;

                DateTime dtNow = DateTime.Now;
                switch (oder.Taskstatus)
                {
                    //["已发送", "待查收", "未开展", "开展中", "已完成", "已回退", "已查收"]
                    case "未开展":
                        UserInfo usr = common.getUserInfo(jsonParams.userName);
                        if (usr != null)
                        {
                            oder.Collectorid = usr.Useroid;
                            oder.Collector = usr.Username;
                            oder.Collectorphone = usr.Userphone;
                            oder.CollectorunitId = usr.Organizationoid;
                            oder.CollectorunitName = usr.Groupname;
                        }
                        oder.Taskfeedbacktimes = 0;
                        oder.Taskstatusupdatetime = dtNow;
                        oder.Checktime = dtNow;
                        break;
                    case "开展中":
                        oder.Taskfeedbacktimes += 1;
                        oder.Taskfeedbacktime = dtNow;
                        oder.Taskstatusupdatetime = dtNow;
                        break;
                    case "已完成":
                        oder.Taskcompletetime = dtNow;
                        oder.Taskstatusupdatetime = dtNow;
                        break;
                    case "已回退":
                        oder.Taskfeedbacktimes = 0;
                        oder.Taskfallback = 1;
                        oder.Taskfallbackreason = jsonParams.back_reason;
                        oder.Taskfallbacktime = dtNow;
                        oder.Taskstatusupdatetime = dtNow;
                        break;
                }

                int result = _context.SaveChanges();
                if (oder.Taskstatus != "开展中")
                {
                    result = updateInfo_Feedback(oder, Convert.ToString(jsonParams.userName));
                }
                var data = new { result = result, desc = "状态已更新为：" + jsonParams.Taskstatus, updatetime = dtNow };
                return common.transResult(data);
            }
            else
            {
                if (rows == 0)
                    return common.transResult("", "数据不存在！");
                else
                    return common.transResult("", "数据存在多条！");
            }
        }

        //更新任务反馈信息
        public int updateInfo_Feedback(TaskOrder oder, string usrName)
        {
            int nTimes = (int)(oder.Taskstatus == "" ? 0 : oder.Taskfeedbacktimes);
            TaskFeedback obj = new TaskFeedback
            {
                TaskFeedbackOid = Guid.NewGuid().ToString("D"),
                Taskordeid = oder.TaskOrderOid,
                Taskid = oder.Taskid,
                Taskobjectname = oder.Tasksubobjectname,

                //Supervision = oder.Supervision,
                //Isitnecessarytorectify = jsonParams.Isitnecessarytorectify,
                //Islawenforcementnecessary = jsonParams.Islawenforcementnecessary,
                //Isitnecessarytopunish = jsonParams.Isitnecessarytopunish,
                //Picturenames = jsonParams.Picturenames,

                //Taskfeedbackperson = jsonParams.Taskfeedbackperson,
                //Taskfeedbackpersonphone = jsonParams.Taskfeedbackpersonphone,
                Taskfeedbacktimes = nTimes,
                Taskfeedbacktime = oder.Taskfeedbacktime,

                Tasktype = oder.Tasktype,
                Taskstatus = oder.Taskstatus,
                TaskTypeSrc = oder.TaskTypeSrc,
                TaskTypesubSrc = oder.TaskTypesubSrc
            };
            UserInfo usr = common.getUserInfo(usrName);
            if (usr != null)
            {
                obj.TaskfeedbackpersonId = usr.Useroid;
                obj.Taskfeedbackperson = usr.Username;
                obj.Taskfeedbackpersonphone = usr.Userphone;
            }

            // 更新完成时信息
            if (oder.Taskstatus == "未开展")
            {
                obj.Taskfeedbacktime = oder.Checktime;
            }
            else if (oder.Taskstatus == "完成")
            {
                var query = _context.TaskFeedback.Where(s => s.Taskordeid == oder.TaskOrderOid);
                obj.Taskfeedbacktimes = query.Count() - 1;
            }
            else if (oder.Taskstatus == "已回退")
            {
                obj.Supervision = oder.Taskfallbackreason;
                obj.Taskfeedbacktime = oder.Taskfeedbacktime;
            }
            _context.Add(obj);
            int result = _context.SaveChanges();
            return result;
        }

    }
}
