using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Linq.Expressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.MicroStation.Models;
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class MicroStation_KPRController : ControllerBase
    {
        private dg_dbContext _context;
        public MicroStation_KPRController(dg_dbContext context)
        {
            _context = context;
        }


        /// <summary>提取站点小时数据（卡普瑞）
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData_H(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);
            var moreHours = jsonParams.moreHours == null ? 0 : (int)Convert.ToInt32(jsonParams.moreHours);
            DateTime dtStart = common.checkTimeH(jsonParams.dtTime).AddHours(-moreHours);
            DateTime dtEnd = dtStart.AddHours(1 + moreHours);

            int id = Convert.ToInt32(jsonParams.DeployId);
            string sql = id == 0 ? "" : " And DeployId = " + id.ToString();
            sql = "Pubtime >= @0 And Pubtime < @1" + sql;

            var query = _context.KprMonitorDataDeviceHour
                            .AsQueryable()
                                .Where(sql, dtStart, dtEnd)
                                .OrderBy("DeployId")
                                .OrderByDescending(e => e.Pubtime)
                                .Select("new (DeployId, AddressDetail, Aqi, Pm25, Pm10, So2, No2, Co, O3, O38h, Voc," +
                                    //"WindSpeed, WindDirection, Temperature, AirPressure, " +
                                    "Pubtime, CreateDt)");

            //var query = _context.KprMonitorDataDeviceHour
            //                .Where(s => s.Pubtime >= dtStart & s.Pubtime < dtEnd)
            //                .OrderBy(b => b.DeployId)
            //                .Select(c => new {
            //                    c.DeployId,
            //                    c.AddressDetail,
            //                    c.Aqi, c.Pm25, c.Pm10, c.So2, c.No2, c.Co, c.O3, c.O38h, c.Voc,
            //                    c.WindSpeed, c.WindDirection, c.Temperature, c.AirPressure,
            //                    c.Pubtime, c.CreateDt
            //                });
            //return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(query)));
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

        /// <summary>提取站点小时数据集-自定义（卡普瑞）
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData_Hs(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            DateTime dtStart = common.checkTimeH(jsonParams.dtStart);
            DateTime dtEnd = common.checkTimeH(jsonParams.dtEnd, false);
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);
            int id = Convert.ToInt32(jsonParams.DeployId);

            string sql = id == 0 ? "" : " And DeployId = " + id.ToString();
            sql = "Pubtime >= @0 And Pubtime < @1" + sql;

            var query = _context.KprMonitorDataDeviceHour
                            .AsQueryable()
                                .Where(sql, dtStart, dtEnd)
                                .OrderBy("DeployId")
                                .OrderByDescending(e => e.Pubtime)
                                .Select("new (DeployId, AddressDetail, Aqi, Pm25, Pm10, So2, No2, Co, O3, O38h, Voc," +
                                    //"WindSpeed, WindDirection, Temperature, AirPressure, " +
                                    "Pubtime, CreateDt)");
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }


        /// <summary>提取站点日数据（卡普瑞）
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData_D(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);
            DateTime dtStart = common.checkTimeD(jsonParams.dtTime);
            DateTime dtEnd = dtStart.AddDays(1);

            int id = Convert.ToInt32(jsonParams.DeployId);
            string sql = id == 0 ? "" : " And DeployId = " + id.ToString();
            sql = "Pubtime >= @0 And Pubtime < @1" + sql;

            var query = _context.KprMonitorDataDeviceDay
                            .AsQueryable()
                                .Where(sql, dtStart, dtEnd)
                                .OrderBy("DeployId")
                                .Select("new (DeployId, AddressDetail, Aqi, Pm25, Pm10, So2, No2, Co, O3, O38h, Voc," +
                                    //"WindSpeed, WindDirection, Temperature, AirPressure, " +
                                    "Pubtime, UpdateDt, CreateDt)");
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

        /// <summary>提取站点小时数据集-自定义（卡普瑞）
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getData_Ds(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            DateTime dtStart = common.checkTimeD(jsonParams.dtStart);
            DateTime dtEnd = common.checkTimeD(jsonParams.dtEnd);
            var page = jsonParams.pageInd == null ? 1 : (int)Convert.ToInt32(jsonParams.pageInd) + 1;
            var size = jsonParams.pageSize == null ? common.pageSize : (int)Convert.ToInt32(jsonParams.pageSize);
            int id = Convert.ToInt32(jsonParams.DeployId);

            string sql = id == 0 ? "" : " And DeployId = " + id.ToString();
            sql = "Pubtime >= @0 And Pubtime < @1" + sql;

            var query = _context.KprMonitorDataDeviceDay
                            .AsQueryable()
                                .Where(sql, dtStart, dtEnd)
                                .OrderBy("DeployId")
                                .OrderByDescending(e => e.Pubtime)
                                .Select("new (DeployId, AddressDetail, Aqi, Pm25, Pm10, So2, No2, Co, O3, O38h, Voc," +
                                    //"WindSpeed, WindDirection, Temperature, AirPressure, " +
                                    "Pubtime, UpdateDt, CreateDt)");
            var queryFen = query.Skip(size * (page - 1)).Take(size);
            JObject objRes = common.transResult_page(page, size, queryFen.Count());
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(queryFen)), objRes);
        }

    }
}
