using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.MicroStation.Models;

namespace zpCore.MicroStation
{
    public class common
    {
        public static readonly int pageSize = 3;    //默认分页条数

        /// <summary> 返回Json串(不带双引号)
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public static ActionResult<string> transResult(dynamic objDatas, dynamic objMsg = null)
        {
            var data = new { code = 0, is_success = true, msg = objMsg, datas = objDatas };
            var result = JsonConvert.SerializeObject(new { data = data });
            return new ContentResult { Content = result, ContentType = "application/json" };
        }
        public static JObject transResult_page(int pageInd, int pageSize, int pageCount)
        {
            JObject objRes = new JObject();
            objRes["pageInfo "] = new JObject();
            objRes["pageInfo "]["pageInd"] = pageInd;
            objRes["pageInfo "]["pageSize"] = pageSize;
            objRes["pageInfo "]["pageCount"] = pageCount / pageSize + 1;
            return objRes;
        }

        public static DateTime checkTime(dynamic varTime)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null)
                dtTime = Convert.ToDateTime(varTime);
            return dtTime;
        }
        public static DateTime checkTimeH(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null)
                dtTime = Convert.ToDateTime(varTime);
            int offset = bzero ? -1 : 1;
            dtTime = dtTime.AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset).AddHours(0);
            return dtTime;
        }
        public static DateTime checkTimeD(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null)
                dtTime = Convert.ToDateTime(varTime);
            int offset = bzero ? -1 : 1;
            dtTime = dtTime.AddHours(-dtTime.Hour).AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset);
            return dtTime;
        }


        public static ActionResult<string> errResult(string errInfo)
        {
            return new ContentResult { Content = errInfo, ContentType = "application/json" };
        }


        public dynamic transParam(dynamic param, List<string> lstNames)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            JObject objParm = new JObject();
            foreach (var item in lstNames)
            {
                objParm[item] = jsonParams[item];
            }
            return objParm;
        }
    }
}
