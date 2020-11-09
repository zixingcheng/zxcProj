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
/// <summary>告警接口集
/// </summary>
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class InfoAlarmController : ControllerBase
    {
        private db_MicroStationContext _context;
        public InfoAlarmController(db_MicroStationContext context)
        {
            _context = context;
        }


        /// <summary>新增告警信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> add(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            int id = jsonParams.DeployId == null ? 0 : Convert.ToInt32(jsonParams.DeployId);
            DateTime dtTime = common.checkTime(jsonParams.Alarmtime);

            //if (!_context.Infoalarm.Any())
            Infoalarm obj = new Infoalarm { InfoalarmOid = Guid.NewGuid().ToString("D"), DeployId = id, AlarmType = jsonParams.AlarmType, Alarmindex = jsonParams.Alarmindex, Alarmlevel = jsonParams.Alarmlevel, Alarmcontent = jsonParams.Alarmcontent, Alarmtime = dtTime, Cratetime = DateTime.Now };
            _context.Add(obj);
            int result = _context.SaveChanges();
            var data = new { InfoalarmOid = obj.InfoalarmOid, result = result };
            return common.transResult(data);
        }

        /// <summary>提取站点告警数据
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            DateTime dtStart = common.checkTimeH(jsonParams.dtStart);
            DateTime dtEnd = common.checkTimeH(jsonParams.dtEnd);
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);

            string sql = "Alarmtime < @0";
            if (jsonParams.dtStart != null)
                sql += " And Alarmtime >= @1";

            string type = jsonParams.AlarmType;
            if (type != null && type != "")
                sql += " And AlarmType = @2";

            string lv = jsonParams.Alarmlevel;
            if (lv != null && lv != "")
                sql += " And Alarmlevel = @3";

            string index = jsonParams.Alarmindex;
            if (index != null && index != "")
                sql += " And Alarmindex = @4";

            int id = Convert.ToInt32(jsonParams.DeployId);
            if (id > 0)
                sql += " And DeployId = " + id;
            List<int> delopyss = common.checkCondition_ID(jsonParams, "DeployId", 6, ref sql);

            #region 数据权限控制

            //List<int> delopyIds = common.checkPermission_IDs(Convert.ToString(jsonParams.userName), _context);
            // 合并前端查询ID进行查询

            #endregion

            var query = _context.Infoalarm
                                .AsQueryable()
                                    .Where(sql, dtEnd, dtStart, type, lv, index, id, delopyss)
                                    .OrderBy("Alarmtime")
                                    .ThenByDescending(e => e.DeployId)
                                    .Select("new (DeployId, AlarmType, Alarmindex, Alarmlevel, Alarmcontent, Alarmtime)");
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

    }
}


///// <summary>修改告警信息
///// </summary>
///// <param name="param"></param>
///// <returns></returns>
//[HttpPost]
//public ActionResult<string> updata(dynamic param)
//{
//    var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
//    string oid = Convert.ToString(jsonParams.InfoalarmOid);

//    var v1 = _context.Infoalarm.Where(c => c.InfoalarmOid == oid); //得到数据库中的一行。
//    Infoalarm user = v1.Take(1).Single();
//    user.Alarmcontent = "test";
//    int result = _context.SaveChanges();
//    return common.transResult(result);
//}