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
            int times = getTimes_Feedback(Convert.ToString(jsonParams.Taskordeid));
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
                Taskfeedbacktime = DateTime.Now
            };

            _context.Add(obj);
            int result = _context.SaveChanges();
            var data = new { TaskFeedbackOid = obj.TaskFeedbackOid, result = result };
            return common.transResult(data);
        }

        //查询任务反馈次数
        public int getTimes_Feedback(string taskid)
        {
            var query = _context.TaskFeedback.Where(s => s.Taskordeid == taskid);
            return query.Count() + 1;
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

            var query = _context.TaskFeedback
                                .AsQueryable()
                                    .Where(sql, taskordeid, taskid)
                                    .OrderByDescending(e => e.Taskfeedbacktime);
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

    }
}
