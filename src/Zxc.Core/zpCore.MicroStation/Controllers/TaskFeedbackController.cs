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
/// <summary>任务反馈接口集
/// </summary>
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class TaskFeedbackController : ControllerBase
    {
        private db_MicroStationContext _context;
        public TaskFeedbackController(db_MicroStationContext context)
        {
            _context = context;
        }


        /// <summary>新增任务反馈信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> add(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            string oid = Convert.ToString(jsonParams.Taskoid);
            string id = Convert.ToString(jsonParams.Taskid);
            int times = getTimes_Feedback(Convert.ToString(jsonParams.Taskoid));

            // 查询任务信息
            string sql = "TaskOrderOid = @0 and Taskid = @1 And Taskstatus != @2 And Taskstatus != @3";
            var query = _context.TaskOrder
                                .AsQueryable()
                                    .Where(sql, oid, id, "已回退", "已完成");
            string resOid = "";
            int result = 0;
            if (query.Count() == 1)
            {
                TaskOrder oder = query.Take(1).Single();
                TaskFeedback obj = new TaskFeedback
                {
                    TaskFeedbackOid = Guid.NewGuid().ToString("D"),
                    Taskordeid = jsonParams.Taskoid,
                    Taskid = jsonParams.Taskid,
                    Supervision = jsonParams.Supervision,
                    Isitnecessarytorectify = jsonParams.Isitnecessarytorectify,
                    Islawenforcementnecessary = jsonParams.Islawenforcementnecessary,
                    Isitnecessarytopunish = jsonParams.Isitnecessarytopunish,
                    Picturenames = jsonParams.Picturenames,

                    Taskfeedbackperson = jsonParams.Taskfeedbackperson,
                    Taskfeedbackpersonphone = jsonParams.Taskfeedbackpersonphone,
                    Taskfeedbacktimes = times,
                    Taskfeedbacktime = DateTime.Now,

                    Tasktype = oder.Tasktype,
                    Taskstatus = "开展中",
                    TaskTypeSrc = oder.TaskTypeSrc,
                    TaskTypesubSrc = oder.TaskTypesubSrc
                };
                UserInfo usr = common.getUserInfo(jsonParams.userName);
                if (usr != null)
                {
                    obj.TaskfeedbackpersonId = usr.Useroid;
                    obj.Taskfeedbackperson = usr.Username;
                    obj.Taskfeedbackpersonphone = usr.Userphone;
                }
                _context.Add(obj);
                result = _context.SaveChanges();
                if (result == 1)
                {
                    result = updateTimes_Feedback(Convert.ToString(jsonParams.Taskoid));
                }
                resOid = obj.TaskFeedbackOid;
            }
            var data = new { TaskFeedbackOid = resOid, result = result };
            return common.transResult(data);
        }

        //查询任务反馈次数
        public int getTimes_Feedback(string taskid)
        {
            string sql = "Taskordeid = @0 And Taskstatus == @1";
            var query = _context.TaskFeedback
                                .AsQueryable()
                                    .Where(sql, taskid, "开展中");
            return query.Count() + 1;
        }
        //查询任务反馈次数
        public int updateTimes_Feedback(string taskoid)
        {
            var query = _context.TaskOrder.Where(s => s.TaskOrderOid == taskoid);
            TaskOrder oder = query.Take(1).Single();

            oder.Taskstatus = "开展中";
            oder.Taskfeedbacktimes += 1;
            oder.Taskfeedbacktime = DateTime.Now;
            oder.Taskstatusupdatetime = DateTime.Now;

            int result = _context.SaveChanges();
            return result;
        }

        /// <summary>提取任务反馈数据
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);

            string sql = "";
            string taskordeid = jsonParams.Taskordeid;
            if (taskordeid != null && taskordeid != "")
                sql += "Taskordeid = @0";

            string taskid = jsonParams.Taskid;
            if (taskid != null && taskid != "")
            {
                if (sql != "") sql += " And ";
                sql += "Taskid = @1";
            }

            string taskstatus = jsonParams.Taskstatus;
            if (taskstatus != null && taskstatus != "")
            {
                sql += " And Taskstatus = @2";
            }

            var query = _context.TaskFeedback
                                .AsQueryable()
                                    .Where(sql, taskordeid, taskid, taskstatus)
                                    .OrderByDescending(e => e.Taskfeedbacktime);
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

    }
}
