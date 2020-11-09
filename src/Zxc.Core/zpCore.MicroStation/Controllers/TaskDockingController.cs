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
    public class TaskDockingController : ControllerBase
    {
        private db_MicroStationContext _context;
        public TaskDockingController(db_MicroStationContext context)
        {
            _context = context;
        }


        /// <summary>新增任务对接信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpGet]
        public ActionResult<string> add(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            string Filename = Convert.ToString(jsonParams.Filename);

            // 按文件名识别文件格式信息
            DateTime dtNow = DateTime.Now;
            DateTime Createtime = DateTime.Now;
            var Dockingtype = "任务工单";
            var AssociationId = "";
            var Dockingresults = "";
            int Dockingtimes = 1;

            // 查询是否已入库
            TaskDocking docking = null;
            var query = _context.TaskDocking.Where(s => s.Filename == Filename).OrderByDescending(b => b.Createtime);
            if (query.Count() >= 1)
            {
                docking = query.Take(1).Single();
                Dockingtimes = (int)(docking.Dockingtimes + 1);
                Createtime = (DateTime)docking.Createtime;
            }
            // 按类型操作
            dynamic res = false;
            switch (Dockingtype)
            {
                case "任务工单":
                    res = addTask(param);
                    break;
                case "告警":
                    res = addTask(param);
                    break;
                default:
                    break;
            }
            Dockingresults = res.result ? "完成" : "失败";

            // 创建或更新对象
            if (docking == null)
            {
                docking = new TaskDocking
                {
                    TaskDockingOid = Guid.NewGuid().ToString("D"),
                    Filename = jsonParams.Filename,
                    Filepath = jsonParams.Filepath,
                    Dockingtype = Dockingtype,
                    AssociationId = AssociationId,
                    Dockingmode = jsonParams.Dockingmode,       //download/upload
                    Dockingresults = Dockingresults,
                    Dockingtimes = Dockingtimes,
                    Dockingtime = dtNow,
                    Createtime = dtNow
                };
                _context.Add(docking);
            }
            else
            {
                docking.Dockingresults = Dockingresults;
                docking.Dockingtimes += 1;
                docking.Dockingtime = dtNow;
            }
            int result = _context.SaveChanges();
            var data = new { TaskOrderOid = docking.TaskDockingOid, result = res.result };
            return common.transResult(data);
        }

        // 添加告警对接信息
        public dynamic addAlarm(dynamic param)
        {
            bool bRes = false;

            return new { result = bRes };
        }

        // 添加告警对接信息
        public dynamic addTask(dynamic param)
        {
            bool bRes = false;

            bRes = true;
            return new { result = bRes, AssociationId = "22bb6162-0f83-11eb-babb-52540075fa19" };
        }

    }
}
