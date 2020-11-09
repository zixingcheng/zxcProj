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
/// <summary>微站接口集
/// </summary>
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class MicroStationController : ControllerBase
    {
        private db_MicroStationContext _context;
        public MicroStationController(db_MicroStationContext context)
        {
            _context = context;
        }


        /// <summary>提取站点信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> getInfo_Station(dynamic param)
        {
            var query = _context.MicroStation
                            .AsQueryable()
                                .Where("DeployId > 0")
                                .OrderBy("DeployId")
                                .Select("new (DeployId as deploy_id, SiteName as site_name, LatitudeBd as latitude, LongitudeBd as longitude)");
            //var query = _context.MicroStation.Where(s => s.deploy_id > 0).OrderBy(b => b.deploy_id)
            //    .Select(c => new { 
            //        c.deploy_id, c.site_name, c.latitude, c.longitude 
            //    });
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(query)));
        }

        public ActionResult<string> getInfo_StationPerm(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            string strSql = "DeployId > 0";

            #region 数据权限控制

            List<int> delopyIds = common.checkPermission_IDs(Convert.ToString(jsonParams.userName), _context);

            #endregion

            var query = _context.MicroStation
                            .AsQueryable()
                                .Where("@0.Contains(DeployId)", delopyIds)
                                .OrderBy("DeployId")
                                .Select("new (DeployId as deploy_id, SiteName as site_name, StreetName as stree_name,CommunityName as community_name, LatitudeBd as latitude, LongitudeBd as longitude)");
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(query)));
        }


        /// <summary>提取站点信息
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public async Task<ActionResult<string>> getInfo_StationsAsync(dynamic param)
        {
            var query = _context.MicroStation
                        .Where(s => s.DeployId > 0)
                            .OrderBy(b => b.DeployId)
                            .Select(s => new { s.DeployId, s.SiteName, s.StreetName, s.CommunityName });
                            //.GroupBy(g => new { g.StreetName, g.CommunityName });
                            //.Select("new (DeployId as deploy_id, SiteName as site_name)");
            JObject objRes = new JObject();
            foreach (var item in query)
            {
                // 镇街节点
                if (!objRes.ContainsKey(item.StreetName))
                    objRes.Add(item.StreetName, new JObject());
                JObject objStreet = (JObject)objRes[item.StreetName];

                // 村社区节点
                if (!objStreet.ContainsKey(item.CommunityName))
                    objStreet.Add(item.CommunityName, new JArray());
                JArray objCommunity = (JArray)objStreet[item.CommunityName];

                // 站点信息
                JObject objDeploy = new JObject();
                objDeploy["id"] = item.DeployId;
                objDeploy["site_name"] = item.SiteName;
                objCommunity.Add(objDeploy);
            }
            return common.transResult(objRes);

            //foreach (var item in allStreets)
            //{
            //    var allCommunitys = 
            //    item.StreetName 
            //}



            //var allCommunitys = query.GroupBy("CommunityName");


            //var query = _context.MicroStation.Where(s => s.deploy_id > 0).OrderBy(b => b.deploy_id)
            //    .Select(c => new { 
            //        c.deploy_id, c.site_name, c.latitude, c.longitude 
            //    });
            //return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(allStreets)));
        }

        /// <summary>更新经纬度信息(DB09)
        /// </summary>
        /// <param name="param"></param>
        /// <returns></returns>
        [HttpPost]
        public ActionResult<string> updataInfo_coordinates(dynamic param)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            int id = Convert.ToInt32(jsonParams.DeployId);

            // 查询单条
            var query = _context.MicroStation
                                .AsQueryable()
                                    .Where("DeployId = @0", id)
                                    .OrderByDescending(e => e.DeployId);

            int rows = query.Count();
            if (rows == 1)
            {
                Models.MicroStation station = query.Take(1).Single();
                station.LongitudeBd = Convert.ToSingle(jsonParams.Longitude);
                station.LatitudeBd = Convert.ToSingle(jsonParams.Latitude);

                int result = _context.SaveChanges();
                var data = new { result = result, desc = "DB经纬度坐标已更新为：" + jsonParams.Longitude + ";" + jsonParams.Longitude };
                return common.transResult(data);
            }
            else
            {
                if (rows == 0)
                    return common.transResult("", "数据不存在！");
                else
                    return common.transResult("", "数据存在多条！");
            }

    //        // 更新百度经纬度信息
    //        function upInfo_Coors(DeployId, point)
    //        {
    //            var dataJson = dataDevices;
	   //         $.ajax({
    //            type: "POST",
		  //          async: false,	
		  //          url: root2 + '/api/MicroStation/updataInfo_coordinates',
		  //          type: "POST",   //post请求方式
		  //          async: false,
		  //          contentType: "application/json",
		  //          data: JSON.stringify({
    //                    "DeployId": "111",
			 //           "Longitude": point.lng,
			 //           "Latitude": point.lat
    //                }),
    //                success: function(data)
    //    {
    //    },
		  //          error :function()
    //    {
    //    }
    //});
	   //         return dataJson;
    //        }
        }

        //[HttpPost]
        //public ActionResult<string> geInfo_Station(dynamic value)
        //{
        //    JObject jobject = (JObject)JsonConvert.DeserializeObject(_context.microStation);
        //    return common.creatResult(jobject);


        //    var query = _context.microStation.ToList();
        //    int a = 0;

        //    var page = 1;
        //    var size = 8;
        //    var fen = dbContext.microStation.Where(s => s.deploy_id > 2716).OrderBy(b => b.deploy_id).Skip(size * (page - 1)).Take(size).Select(c => new { c.deploy_id, c.latitude, c.longitude });

        //    var fen2 = dbContext.microStation.Where(s => s.deploy_id > 2716);
        //    int dsw = fen2.Count() / size + 1;


        //    using (var dbContext = new db_MicroStationContext(dbOptionBuilder.Options))
        //    {
        //        var query = _context.microStation.ToList();
        //        int a = 0;

        //        var page = 1;
        //        var size = 8;
        //        var fen = dbContext.microStation.Where(s => s.deploy_id > 2716).OrderBy(b => b.deploy_id).Skip(size * (page - 1)).Take(size).Select(c => new { c.deploy_id, c.latitude, c.longitude });

        //        var fen2 = dbContext.microStation.Where(s => s.deploy_id > 2716);
        //        int dsw = fen2.Count() / size + 1;

        //        //string strJson = JsonConvert.SerializeObject(aa);

        //        var des = new { 编号 = "", 经度 = "" };
        //    }

        //    //JObject jobject = (JObject)JsonConvert.DeserializeObject(str);
        //    //return common.creatResult(jobject);
        //    return "";
        //}
    }
}

//Scaffold-DbContext "server=120.197.152.99;userid=zpkj;pwd=Zp.666888!@#;port=8606;database=db_MicroStation;sslmode=none;" Pomelo.EntityFrameworkCore.MySql -OutputDir Models -Force
//Scaffold-DbContext "server=8.129.80.187;userid=dbuser_dg;pwd=kPr@2020#!dGCambRi;port=3306;database=dg_db;sslmode=none;" Pomelo.EntityFrameworkCore.MySql -OutputDir Models -Force

//[HttpPost]
//public ActionResult<string> DoPost([FromBody] string value)
//{
//    return value;
//    //return "Hello World222!";
//}
//[HttpPost]
//public ActionResult<string> DoPost2(string value)
//{
//    return value;
//    //return "Hello World222!";
//}
//[HttpPost]
//public void DoPost3(JObject jsonObject)
//{
//string b = value.ToString();//两种转换都可以，但是  string b = value；不行
//    //把jsonObject反序列化成dynamic
//    string jsonStr = JsonConvert.SerializeObject(jsonObject);
//    var jsonParams = JsonConvert.DeserializeObject<dynamic>(jsonStr);
// return new JsonResult(JsonConvert.SerializeObject(jobject));

//    //获取dynamic里边的数据
//    string destId = jsonParams.destId;
//    string token = jsonParams.token;
//}